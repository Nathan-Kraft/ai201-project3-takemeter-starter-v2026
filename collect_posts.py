"""Collect post text from MakeMKV forum threads into data/raw_posts.csv.

HOW TO USE
    python collect_posts.py urls.txt

    urls.txt has one thread-page URL per line. Blank lines and lines that
    start with # are ignored. Example line:
        https://forum.makemkv.com/forum/viewtopic.php?t=42594

    A thread longer than one page needs one URL per page. Page two of a
    thread adds &start=15, page three adds &start=30, and so on.

WHAT YOU GET
    data/raw_posts.csv with two columns: thread (the thread number) and
    text (the post). Usernames, dates and links are never saved. This file
    is raw material. You read it and label posts yourself, then put the
    ones you keep into labels.csv.

WHAT IT DOES NOT DO
    It reads only the pages you list. It does not follow links, log in, or
    search the forum. It waits between requests. Use it for a small sample.
"""
import csv
import os
import re
import sys
import time
from html.parser import HTMLParser

import requests

# ---- Settings you can change ------------------------------------------------

# Where collected posts are saved. The data folder already holds your other
# files, and this one is kept apart from labels.csv on purpose.
OUT = os.path.join("data", "raw_posts.csv")

# Seconds to wait between page requests. Keep this at 5 or more so the
# script does not put load on the forum's server.
DELAY = 5

# Posts with fewer words than this are dropped. It removes things like
# "thanks", "bump" and "PM sent." that your skip rule would discard anyway.
MIN_WORDS = 4

# Sent with every request so the site can see who is asking. It says what
# this is. Do not change it to look like a browser.
USER_AGENT = "student-classifier-project (class assignment, small sample)"

# ---- What to keep and what to ignore in a page -----------------------------

# Tags that never have a closing tag, such as <br>. The parser below keeps
# a list of open tags, and these must not be added to it, or it would wait
# forever for a closing tag that never comes.
VOID = {"br", "img", "hr", "input", "meta", "link", "wbr"}

# Parts of a post we do not want, found by their CSS class:
#   codebox            pasted code or drive readouts in a code box
#   signature          the line under a user's posts
#   attachbox          file attachments
#   inline-attachment  images and files placed inside the text
SKIP_CLASSES = {"codebox", "signature", "attachbox", "inline-attachment"}

# Tags we do not want, found by their name:
#   blockquote and cite  the quoted text in a reply. Dropping it stops the
#                        same words from appearing in two posts.
#   script and style     page code that is not post text
SKIP_TAGS = {"blockquote", "cite", "script", "style"}

# Lines of a pasted MakeMKV drive readout, such as "Manufacturer: PIONEER".
# They add nothing to a label, so clean() deletes any line that starts
# with one of these. English, French and Dutch readouts are matched.
READOUT_LINE = re.compile(
    r"^\s*(Drive Information|LibreDrive Information|No disc inserted"
    r"|OS device name:|Manufacturer:|Product:|Revision:|Serial number:"
    r"|Firmware date:|Bus encryption flags:|Highest AACS version:"
    r"|Status:|Drive platform:|Firmware name:|Firmware type:"
    r"|Firmware version:|DVD all regions:|BD raw data read:"
    r"|BD raw metadata read:|Unrestricted read speed:"
    r"|Informations lecteur|Drive informatie|Nom du lecteur"
    r"|Naam OS-apparaat|Fabricant|Fabrikant|Produit|Révision|Revisie"
    r"|Numéro de série|Serienummer|Date micrologiciel|Firmware datum"
    r"|Marqueurs d'encryptage|Bus encryptie|Huidig profiel"
    r"|Aucun disque).*$",
    re.MULTILINE,
)

# Usernames to hide. Any of these found in a post is replaced with the
# placeholder below. Add more names here as you spot them. Matching ignores
# capital letters, so "martymcnuts" is caught too.
USERNAMES = [
    "Billycar11", "Coopervid", "Coppervid", "MartyMcNuts", "AstralWanderer",
    "Robbie56", "Yarci", "SiliconDragon", "mike admin", "heisenberg",
    "skyrider", "Yethidran", "zittrig", "MattJackson", "babagaya",
    "Mr.Penguin", "blackened2857", "asmcoms", "agent_x007", "RibShark",
    "Voxelium", "boguslecina", "DennisOlof", "Chris Kelly",
    "jibanyanlnewells", "macdev", "F1nkNasty", "vtedogs", "Andyyy1",
]
PLACEHOLDER = "[user]"

# One pattern for all the names. It also catches a trailing s, as in
# "Coopervids help".
USER_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(n) for n in USERNAMES) + r")(?:'s|’s|s)?\b",
    re.IGNORECASE,
)


class PostParser(HTMLParser):
    """Reads one page of HTML and collects the text of each post.

    phpBB, the software the forum runs on, puts the text of every post in
    a <div class="content">. The parser walks through the page from top to
    bottom. It keeps a list (the stack) of every tag it is currently
    inside. It saves text only while inside a post body, and ignores text
    inside quotes, code boxes, signatures and attachments within it.

    HTMLParser calls the three handle_ methods below as it reads the page.
    """

    def __init__(self):
        super().__init__()
        # Every tag we are currently inside, as (tag name, kind) pairs.
        # kind is one of:
        #   "content"  the start of a post body
        #   "skip"     a part we throw away
        #   "other"    anything else
        self.stack = []
        self.buf = []      # text pieces of the post being read right now
        self.posts = []    # finished posts, one string for each

    def _inside(self, kind):
        # True if any tag we are inside of has this kind. This is how we
        # know "are we in a post body" and "are we in a skipped part".
        return any(k == kind for _, k in self.stack)

    def handle_starttag(self, tag, attrs):
        # Called for every opening tag, such as <div class="content">.
        # tag is the name. attrs is a list of (name, value) pairs.

        if tag in VOID:
            # These tags have no end. Do not add them to the stack. The
            # one useful one is <br>, a line break inside a post.
            if tag == "br" and self._inside("content") and not self._inside("skip"):
                self.buf.append("\n")
            return

        # The class attribute can hold several names, such as "post bg2".
        # Turn it into a list. A tag with no class gives an empty list.
        classes = (dict(attrs).get("class") or "").split()

        kind = "other"
        if tag == "div" and "content" in classes and not self._inside("content"):
            # A post body starts here. The "not already inside" check means
            # a content div nested inside another is not treated as a
            # second post.
            kind = "content"
        elif tag in SKIP_TAGS or SKIP_CLASSES & set(classes):
            # A quote, code box, signature or attachment. The "&" finds
            # any class name that is in both sets.
            kind = "skip"
        self.stack.append((tag, kind))

    def handle_endtag(self, tag):
        # Called for every closing tag, such as </div>.
        # Search the stack from the end for the matching open tag. Going
        # backwards, and removing everything above the match, copes with
        # pages that forget to close a tag such as <p> or <li>.
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                kind = self.stack[i][1]
                del self.stack[i:]
                if kind == "content":
                    # The post body has ended. Join its text pieces into
                    # one string, save it, and start a fresh buffer.
                    self.posts.append("".join(self.buf))
                    self.buf = []
                return

    def handle_data(self, data):
        # Called for the text between tags. Keep it only when we are inside
        # a post body and not inside a skipped part of it.
        if self._inside("content") and not self._inside("skip"):
            self.buf.append(data)


def clean(text):
    # Tidy one post before it is saved.
    # 0. Delete pasted drive readout lines. This has to happen first,
    #    while each readout line is still on its own line.
    text = READOUT_LINE.sub("", text)
    # 1. Remove web links, since they identify sources and add noise.
    #    This covers full links and the forum's own relative links such as
    #    viewtopic.php?t=28257. Then remove leftover BBCode tags such as
    #    [/b] or [url=...].
    text = re.sub(r"(https?://|viewtopic\.php\?)\S+", "", text)
    text = re.sub(r"\[/?[a-zA-Z]+(=[^\]]*)?\]", "", text)
    # 2. Remove anything that looks like an email address.
    text = re.sub(r"\S+@\S+\.\S+", "", text)
    # 3. Replace usernames with a placeholder. This runs after step 1 so
    #    the placeholder is not mistaken for a BBCode tag.
    text = USER_PATTERN.sub(PLACEHOLDER, text)
    # 4. Turn every run of spaces and line breaks into one space, so each
    #    post is a single line in the CSV, then trim the ends.
    return re.sub(r"\s+", " ", text).strip()


def thread_id(url):
    # Pull the thread number out of a URL like ...viewtopic.php?t=42594.
    # It is saved so you can see which thread a post came from. It is
    # blank if the URL has no t= part.
    match = re.search(r"[?&]t=(\d+)", url)
    return match.group(1) if match else ""


def read_urls(path):
    # Read the list of pages to fetch. One URL per line. Blank lines and
    # lines starting with # are ignored, so you can leave notes in the file.
    with open(path, encoding="utf-8") as f:
        lines = [line.strip() for line in f]
    return [line for line in lines if line and not line.startswith("#")]


def main(url_file):
    # ---- Step 1: load posts we already have --------------------------------
    # If the output file exists from an earlier run, read its posts into a
    # set. Later, any post already in the set is skipped, so running the
    # script twice does not create duplicates.
    seen = set()
    new_file = not os.path.exists(OUT)
    if not new_file:
        with open(OUT, encoding="utf-8", newline="") as f:
            seen = {row["text"] for row in csv.DictReader(f)}

    # ---- Step 2: fetch each page and pull out its posts --------------------
    rows = []
    for n, url in enumerate(read_urls(url_file)):
        if n:
            # Wait between requests, but not before the first one.
            time.sleep(DELAY)

        # Download one page. raise_for_status stops the script with an
        # error if the site answers with something like 404 or 429, so a
        # bad URL or a "slow down" reply is noticed and not ignored.
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
        resp.raise_for_status()

        # Feed the page's HTML to the parser. When feed() returns,
        # parser.posts holds the text of every post on the page.
        parser = PostParser()
        parser.feed(resp.text)

        kept = 0
        for raw in parser.posts:
            text = clean(raw)
            # Drop very short posts and posts we already have.
            if len(text.split()) < MIN_WORDS or text in seen:
                continue
            seen.add(text)
            # Save only the thread number and the text. No username, no
            # date and no link is ever stored.
            rows.append({"thread": thread_id(url), "text": text})
            kept += 1

        # ---- Step 3: report what happened on this page ---------------------
        # "found" is every post the parser saw. "kept" is what survived the
        # filters. If found is much lower than the posts you can count in
        # your browser, the page layout is not what the script expects.
        print(f"{url}: {len(parser.posts)} posts found, {kept} kept")
        if not parser.posts:
            print("  no posts found - the page markup may differ")

    # ---- Step 4: write the results -----------------------------------------
    # Open in append mode so earlier runs are kept. Write the header row
    # only when the file is new, or it would repeat on every run.
    os.makedirs("data", exist_ok=True)
    with open(OUT, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["thread", "text"])
        if new_file:
            writer.writeheader()
        writer.writerows(rows)
    print(f"added {len(rows)} posts to {OUT}")


if __name__ == "__main__":
    # The script needs exactly one argument: the file listing the URLs.
    if len(sys.argv) != 2:
        sys.exit("usage: python collect_posts.py urls.txt")
    main(sys.argv[1])
