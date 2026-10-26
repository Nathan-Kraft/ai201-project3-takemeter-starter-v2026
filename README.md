# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

This project builds a text classifier for posts from the MakeMKV forums, especially discussions about UHD-capable optical drives, firmware flashing, and disc-reading problems. It sorts each substantive post into `question`, `advice`, `report`, or `opinion`. The goal is to make a useful first pass over forum conversations by separating requests for help from troubleshooting guidance, personal experiences, and general claims. Posts containing only thanks, ads, bumps, or pasted drive information are excluded.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `question`

**Definition:** Asking for information or help of any kind.

**Example 1:**
>“Hello [user], I have a spare Pioneer drive, is it possible to flash this for 4k?”

**Example 2:**
>“The buffalo burner has been discontinued. (Days before I bought one) What’s next?”

### `opinion`

**Definition:** States a general claim about drives, vendors or the market, with little or no support.

**Example 1:**
>“Crossflashing is not possible for this drive.”

**Example 2:**
>“This is a great release, and we should all be glad someone released their software for free!”

### `advice`

**Definition:** Tells someone what to do or not to do, as a single suggestion or as a series of steps.

**Example 1:**
>“Do not use MakeMKV v2.0.0. Install v1.18.4 and yes, extract the files before running the flasher.”

**Example 2:**
>“The important part is what your drive’s BIOS says about its software. If it was flashed recently, it may be locked out. That’s why posting your drive information is important.”

### `report`

**Definition:** Describes what happened to the writer, success or failure, without asking for anything.

**Example 1:**
>“Worked flawlessly, thank you [user]!”

**Example 2:**
>“Okay, I washed the disc with water mixed with dish soap and carefully cleaned it using a microfiber cloth, avoiding circular motions. Unfortunately, the PC still doesn’t recognize the disc.”

### The hardest boundary

**Which two labels:** `advice` and `report`

**The decision rule I used every time:** If the post tells the reader to do something, it's `advice`, even if it also describes what happened to the writer. If it only describes what happened and asks and recommends nothing, it's `report`.

A second rule: label a post `question` when its main purpose is to obtain information or help from the reader. A diagnostic question inside a reply is not enough by itself to make the post `question`; if the main purpose is to tell the reader what to do, label it `advice`.

A third rule: a plain statement about a drive, vendor or the market, with no event from the writer's own experience, is `opinion`, even when it is probably true.

### Posts that get no label

Posts with no question, claim, event or recommendation are skipped and not put in `labels.csv`. That covers thanks with nothing else, "PM sent.", bumps, ads, and posts that are only a pasted drive readout. If a post has a readout plus real text, I keep the text and delete the readout. I counted the skipped posts so I can report them in The Dataset.

---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:**
All the posts came from the MakeMKV forums. Most posts are from subforms within the UHD drives subforum.

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->
For 20 posts I labeled them cold, then had claude check them over against my rules for a second opinion. I agreed with its changes after discussing them. For the rest of them I had claude run through and label them.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `question` | 69 | 31.4% |
| `advice` | 59 | 26.8% |
| `report` | 54 | 24.5% |
| `opinion` | 38 | 17.3% |
| **Total** | **220** | **100%** |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1. (third rule: opinion vs. report)**
> *The post:*
> "Crossflashing is not possible for this drive."
>
> *Could have been:*
> `report` or `opinion`
>
> *I chose `opinion`, because:*
> It states a claim about a drive, not an event in the writer's experience. Nothing in the post says the writer tried it.

**2. (second rule: question vs. advice)**
> *The post:*
> "Would you be willing to backup your UD02 firmware and upload it to say Google drive? Your firmware could then be used to rescue misflashed UD02 drives. A new free firmware flasher is avaialble since a couple of days. Just need to know on which OS you are."
>
> *Could have been:*
> `question` or `advice`
>
> *I chose `question`, because:*
> I first labelled it `advice`, then changed it after checking my own rules. It asks the reader to do something for the writer, and my second rule says any ask makes it `question`. The flasher notice is a recommendation, but the ask comes first and the rule applies first.

**3. (first rule: advice vs. report)**
> *The post:*
> "I ended up successfully flashing the drive by running the commands [user] posted in a terminal." [...] "At some point it'd be nice if someone could add information about the SDFtool Flasher to the main UHD flashing guide thread. Then on the tool's page, maybe put what seems an unusual requirement of 1st installing an older MM version in a red font." [...] "Thanks for everyone's help getting all this sorted!"
>
> *Could have been:*
> `report` or `advice`
>
> *I chose `advice`, because:*
> I first labelled it `report`, because nearly all of it describes what happened to the writer. Then I checked it against my decision rule, which says a post that recommends anything is `advice`, even if it also describes what happened. The post suggests changes to the guide and the tool page, so it recommends something. The suggestion is aimed at the guide's maintainers, not the reader, so `report` is defensible. I kept the rule as written and chose `advice`.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**
`distilbert-base-uncased`

**Settings:** <!-- epochs, learning rate, batch size, seed -->
3 epochs, learning rate `2e-5`, batch size `16`, seed `42`, and maximum sequence length `128`.

**Hardware:**
Training ran on an NVIDIA GeForce RTX 3070 Laptop GPU using CUDA and PyTorch 2.6.0+cu124.

**Anything I changed from the defaults, and why:**
I did not change the notebook's training defaults. I finalized the dataset at 220 labelled posts after reviewing the labels and removing five skip-only posts.

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->
Using seed 42, the split is 154 train / 33 validation / 33 test. The test split contains `advice` 9, `opinion` 6, `question` 10, and `report` 8. `opinion` has only 6 test examples, so its F1 may vary substantially across seeds.

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:*
Asked Claude to pre-label the remaining unlabeled posts in raw_posts.csv using the label definitions and decision rules in this README.
- *What came back:*
  Proposed labels of `question`, `opinion`, `advice`, or `report`, along with `SKIP` flags for posts containing only thanks, ads, bumps, or pasted drive information. Ten posts had already been set aside in `fresh_test_posts.csv` for later testing, so they were kept separate from the 220 labeled training posts.
- *What I changed:*
  I reviewed the suggestions against my decision rules instead of accepting them automatically. I corrected labels where the post's main purpose was different, removed five skip-only posts from `labels.csv`, and kept 220 labeled posts for training. I also marked technically debatable examples as hard cases for later discussion.

**Moment 2**

- *What I asked for:*
Reconsider replies that begin with a diagnostic question but then give troubleshooting instructions.
- *What came back:*
The question-versus-advice boundary should use the post's main purpose: a diagnostic question inside an instructional reply does not automatically make the post `question`.
- *What I changed:*
I updated the rule in this README and classified instruction-focused support replies as `advice` while keeping genuine information requests as `question`.

**Pre-labelling disclosure:**
I labelled 20 posts cold first and used Claude to check them. Claude pre-labelled the remaining posts; I reviewed the labels against my written rules and corrected the disagreements before training.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
