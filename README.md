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

**Definition:** A request for information or help of any kind.

**Example 1:**
>"Hello [user], I have a spare Pioneer drive, is it possible to flash this for 4k?"

**Example 2:**
>"The buffalo burner has been discontinued. (Days before I bought one) What's next?"

### `opinion`

**Definition:** A general claim about drives, vendors or the market, with little or no support.

**Example 1:**
>"Crossflashing is not possible for this drive."

**Example 2:**
>"This is a great release, and we should all be glad someone released their software for free!"

### `advice`

**Definition:** A suggestion telling someone what to do or not to do, as a single tip or a series of steps.

**Example 1:**
>"Do not use MakeMKV v2.0.0. Install v1.18.4 and yes, extract the files before running the flasher."

**Example 2:**
>"The important part is what your drive's BIOS says about its software. If it was flashed recently, it may be locked out. That's why posting your drive information is important."

### `report`

**Definition:** A description of what happened to the writer, success or failure, that does not ask for anything.

**Example 1:**
>"Worked flawlessly, thank you [user]!"

**Example 2:**
>"Okay, I washed the disc with water mixed with dish soap and carefully cleaned it using a microfiber cloth, avoiding circular motions. Unfortunately, the PC still doesn't recognize the disc."

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
| `question` | 68 | 30.9% |
| `advice` | 60 | 27.3% |
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
> I first labelled it `advice`, then changed it after checking my own rules. The post's main purpose is to get the reader to do something for the writer (back up and share their firmware), not to tell the reader what to do for themselves - that's a request for help, which is `question` by definition, not `advice`. The flasher notice is incidental context for the request, not a recommendation aimed at the reader.

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

### Second training run

For a second run, I changed only the number of epochs from 3 to 4. The learning rate, batch size, seed, model, maximum sequence length, dataset, and split stayed the same.

| Measure | First run | Second run | Change |
|---|---:|---:|---:|
| Overall accuracy | 0.455 | 0.455 | 0.000 |
| Macro F1 | 0.310 | 0.310 | 0.000 |
| F1 - `question` | 0.526 | 0.526 | 0.000 |
| F1 - `advice` | 0.714 | 0.714 | 0.000 |
| F1 - `opinion` | 0.000 | 0.000 | 0.000 |
| F1 - `report` | 0.000 | 0.000 | 0.000 |

The accuracy, macro F1, and per-label F1 scores did not move. The confidence metrics did change: mean confidence when correct increased from 0.324 to 0.348, mean confidence when wrong increased from 0.320 to 0.339, and least-confident-third accuracy decreased from 0.455 to 0.364. Increasing the epochs did not improve predictive performance on this held-out split.

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

**Moment 3**

- *What I asked for:*
Help figure out why `baseline.py`'s accuracy with `label_definitions.txt` loaded looked worse than expected.
- *What came back:*
The original definitions were full verb-first sentences that didn't fit the hypothesis template (`"This post is {}."`), and the `report` definition was built on a negation, which NLI models handle poorly.
- *What I changed:*
Reworded `question`, `opinion`, and `advice` for grammar only, with no change in meaning. Kept the negation in `report`'s definition, since it's the exact clause my hardest-boundary rule depends on, after testing a negation-free version and finding it produced identical results. Updated the Label Taxonomy definitions above to match.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.485 | 0.455 | -0.030 |
| Macro F1 | 0.366 | 0.310 | -0.056 |
| F1 — `advice` | 0.480 | 0.714 | +0.234 |
| F1 — `opinion` | 0.200 | 0.000 | -0.200 |
| F1 — `question` | 0.783 | 0.526 | -0.256 |
| F1 — `report` | 0.000 | 0.000 | +0.000 |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

I believe that my trained model will perform better on my dataset, I also believe that the f1 scores will be better overall.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

Whatever the training run did pushed the model toward a worse, more skewed prediction pattern than it started with. This isn't noise its a real regression that I ned to diagnose before trusting the trained model over the baseline.

**Re-run with corrected baseline definitions:**

While diagnosing this gap, I found that `label_definitions.txt`'s original wording didn't fit `baseline.py`'s hypothesis template (`"This post is {}."`), since the definitions were full verb-first sentences, which read as ungrammatical when slotted into that template, and one (`report`) was defined partly by a negation, which NLI models handle poorly. That's a flaw in the baseline's input, not a finding about my trained model, so I rewrote the definitions as grammatical noun phrases (now reflected in the Label Taxonomy above) and reran the baseline.

| Measure | Baseline (corrected) | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.606 | 0.424 | -0.182 |
| Macro F1 | 0.479 | 0.282 | -0.197 |
| F1 — `advice` | 0.640 | 0.615 | -0.025 |
| F1 — `opinion` | 0.444 | 0.000 | -0.444 |
| F1 — `question` | 0.833 | 0.513 | -0.321 |
| F1 — `report` | 0.000 | 0.000 | +0.000 |

Even with the fixed baseline, the conclusion is the same: training regressed macro F1 instead of improving it, and the trained model still scores 0.000 on both `opinion` and `report`. The corrected baseline shows the gap was overstated before, not that it was wrong in direction.

---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Balance | No label above 40% or below 10% of 220 | 17.3%-30.9% | 17.3%-30.9% | 17.3%-30.9% | MET |
| 2. Per-label F1 | question/advice/report >=0.65, opinion >=0.50 | q 0.513, o 0.000, a 0.615, r 0.000 | q 0.588, o 0.000, a 0.667, r 0.000 | q 0.606, o 0.000, a 0.842, r 0.000 | MISS |
| 3. Seed stability | Accuracy spread <=0.10 | 0.424 | 0.485 | 0.545 | MISS (spread 0.121) |
| 4. Fresh posts | >=8/10 correct | 5/10 | 4/10 | 5/10 | MISS |
| 5. Overall accuracy | >=0.75 | 0.424 | 0.485 | 0.545 | MISS |

Row 1 is measured once on the full 220-post set, before any split - the
value is the same across seeds by construction, not because it happened to
land that way.

Row 3 reuses the same three accuracy numbers as row 5 - the spread is
computed from those, not a separate measurement.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

**Device:** cuda (NVIDIA GeForce RTX 3070 Laptop GPU)

| true \ predicted | question | opinion | advice | report |
|---|---|---|---|---|
| **question** | 10 | 0 | 0 | 0 |
| **opinion** | 6 | 0 | 0 | 0 |
| **advice** | 5 | 0 | 4 | 0 |
| **report** | 8 | 0 | 0 | 0 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

8 real `report` posts were called `question`, and 0 real `question` posts were called `report`. The model didn't learn the report/advice/opinion boundaries at all; it just collapsed almost everything that wasn't `advice` into `question`.

---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Balance | No label above 40% or below 10% of 220 | MET | Counted labels.csv once: 17.3%-30.9% across the four labels, inside the range on both ends. |
| 2 | Per-label F1 | question/advice/report >=0.65, opinion >=0.50, on every seed | MISS | opinion and report scored 0.000 F1 on all three seeds; that alone misses the target regardless of question/advice. |
| 3 | Seed stability | Accuracy spread <=0.10 across seeds | MISS | Accuracies were 0.424, 0.485, 0.545; spread is 0.545-0.424 = 0.121, over the limit. |
| 4 | Fresh posts | >=8/10 correct on every seed | MISS | Got 5/10, 4/10, and 5/10 across the three seeds, well short on all of them. |
| 5 | Overall accuracy | >=0.75 on every seed | MISS | Accuracies were 0.424, 0.485, 0.545, all far below 0.75. |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**Criterion 2 (per-label F1) - `opinion` and `report` both 0.000 across all three seeds:**

Two different causes, not one. `opinion` is the smallest label (38/220) and the thinnest in the test split - only 6 examples on seed 42, below the ~8 I flagged as a risk when I set this split up. That little signal, with no distinguishing surface marker, isn't enough for the model to find what separates it from the rest.

`report` is a different problem: it has 54 examples, more than `opinion`, so it isn't a count issue. The confusion matrix shows all 8 real `report` test posts predicted `question`, and 0 real `question` posts went the other way - a one-directional error, not noise. Checking the text directly: only 11% of `report` posts contain a "?", versus 77% of `question` posts. The model has a strong, learnable lexical cue for `question` and nothing comparable for `report`, so `report` and `question` collapse together on the one surface feature the model actually picked up. That's a genuinely hard label pair here, not a labeling mistake - I checked the question/advice boundary for exactly this kind of inconsistency (see Agreement Report) and found only one real offender in the whole dataset, now fixed, which didn't touch `report` at all.

**Criterion 3 (seed stability) and Criterion 5 (overall accuracy):**

Both trace back to the same collapse. The model learned two reliable cues - "?" for `question` and imperative phrasing for `advice`, the only two labels with non-zero F1 on any seed - and defaults to `question` for everything else. Since `opinion` and `report` are 42% of the dataset, that alone caps accuracy well under 0.75 regardless of seed. The seed-to-seed swing (0.424/0.485/0.545) comes from how much `advice` happens to benefit from this default behavior depending on which examples land in its small test slice (9 posts) each seed - `advice`'s F1 moved from 0.615 to 0.842 across seeds while `question` and the two zero labels barely moved at all.

**Criterion 4 (fresh posts):**

Same root cause as above, just measured on new posts: 5/10, 4/10, 5/10 correct is consistent with a model that only reliably recognizes `question` and `advice` and defaults to `question` otherwise, rather than something specific to the fresh set.

**What the agreement report rules out:** 29/30 (96.7%) agreement on the staff set, with the one disagreement a rule I applied loosely rather than a gap or genuine ambiguity, argues against broad labeling inconsistency as the explanation for `opinion` and `report`'s zero F1. The one real inconsistency I found in my own 220 posts (the `question`/`advice` "any ask" contradiction) was narrow, isolated to a single post, and already corrected - it doesn't reach `report` or `opinion` at all.

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 29 / 30 = 96.7%

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
> "The club championship scoring changed in 2019 from top-6 to top-10. Since then our B team has finished above the A team twice. That's not depth improving, it's the scoring rewarding turnout."
>
> *Staff said / I said:*
>
> Staff said `analysis`. I said `hot-take`.
>
> *My call, and why:*
>
> Staff is right. Rule 1 asks whether the fact is load-bearing or decoration. This post's conclusion ("it's the scoring rewarding turnout") rests entirely on the specific fact - the 2019 scoring change plus B team beating A team twice - remove that fact and there's no argument left. That matches the taxonomy's own worked example almost exactly: "Times are down 3% since 2017, and the shoe rule changed in 2017" is `analysis` because the number is the argument. I called it `hot-take`, because the "that's not X, it's Y" phrasing reads rhetorically like an opinion, which pulled me off the actual test the rule asks for.
>
> *Which pile:*
>
> (a) the rule covered it and I applied it loosely.

**What the pattern in my disagreements tells me:**

With only one disagreement out of 30, and that one a rule I applied loosely rather than a gap or genuine ambiguity, my general rule-following discipline looks solid on this exercise. But it's a narrow kind of inconsistency: I know the rule and can still get pulled off it by a post's rhetorical framing instead of testing the rule's actual criterion. That matters for my own 200 labels, where the same thing could happen on a boundary with stronger lexical pull - like "any ask" pulling toward `question` regardless of the main-purpose rule.



---

## The Improvement

**What I changed:**

Added opinion-labeled examples sourced from new MakeMKV forum posts, raising `opinion` from 38 to 65 of the 248 rows in `labels.csv`. No training settings or other label boundaries were changed.

**Which diagnosis pointed at it:**

Criterion 2's diagnosis for `opinion`'s 0.000 F1: it was the smallest label (38/220, only 6 in the seed-42 test split) with no distinguishing surface marker, so there wasn't enough signal for the model to learn it - a too-few-examples problem, not a labeling inconsistency (the agreement report ruled that out).

### Run Log — After

**Device:** cuda (NVIDIA GeForce RTX 3070 Laptop GPU)

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Balance | No label above 40% or below 10% of 220 | 23.0%-26.2% | 23.0%-26.2% | 23.0%-26.2% | MET |
| 2. Per-label F1 | question/advice/report >=0.65, opinion >=0.50 | q 0.696, o 0.667, a 0.720, r 0.308 | q 0.571, o 0.750, a 0.609, r 0.000 | q 0.640, o 0.556, a 0.750, r 0.000 | MISS |
| 3. Seed stability | Accuracy spread <=0.10 | 0.632 | 0.553 | 0.579 | MET (spread 0.079) |
| 4. Fresh posts | >=8/10 correct | 8/10 | 5/10 | 5/10 | MISS |
| 5. Overall accuracy | >=0.75 | 0.632 | 0.553 | 0.579 | MISS |

Row 1 is measured on the full 248-post `labels.csv` now in place (up from 220
when the before-run criterion was set) - the 10%-40% bounds are unchanged,
only the post count grew.

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

Yes, for what it targeted. `opinion`'s F1 went from 0.000 on all three seeds to 0.667, 0.750, and 0.556 - clearing its own 0.50 target on every seed, something it missed by the maximum possible margin before. Seed stability also improved as a side effect (spread 0.121 -> 0.079, now MET) and overall accuracy rose on every seed (0.42-0.55 before, 0.55-0.63 after).

Criterion 2 as a whole is still a MISS, but for a different reason now: `question` and `report`, not `opinion`, are the labels missing their 0.65 bar (`report` drops to 0.000 on two of three seeds). That matches the diagnosis I already had for `report` - a genuinely hard boundary with `question`, not a low-example problem - so adding opinion examples wasn't expected to fix it, and it didn't. Fresh-post accuracy and overall accuracy are both still short of target for the same reason.



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

**Criterion 2 (per-label F1) - `question` and `report` still miss 0.65:**

`report` is worst: F1 is 0.308, 0.000, 0.000 across seeds. Same one-directional error as the before run, just not fully fixed: 4, 7, and 4 of 9 real `report` posts were predicted `question` each seed, almost none the other way. The cause already diagnosed holds: `question` posts usually have a "?", `report` posts usually don't, and the model leans on that cue instead of purpose. `question` itself misses 0.65 on two seeds for the same reason in reverse.

What I'd do: add `report` examples that still lack a "?", or weight the loss against the `report`->`question` error.

Why I stopped: ran out of time - this milestone's scope was the one opinion fix.

Update: I tried exactly this as the stretch improvement below - `report`'s F1 improved on all three seeds, though it's still a MISS on two of them, and it came with a new `opinion` regression on seed 7. See A Second Measured Improvement.

**Criterion 4 (fresh posts) and Criterion 5 (overall accuracy):**

Both downstream of the same collapse, not separate problems. Fresh posts: 8/10 on seed 42, 5/10 on the other two - swings with how many of the test split's `report` posts happen to lack the "?" cue. Overall accuracy (0.632/0.553/0.579) stays under 0.75 for the same reason at larger scale.

What I'd do: same fix as Criterion 2 - if `report`'s F1 moves, these should move with it.

Why I stopped: same - no time to retrain and re-diagnose past the one change this milestone.

Update: both moved in the stretch run too - fresh posts improved on all three seeds, overall accuracy only ticked up on seed 42. Still short of target; see A Second Measured Improvement.

**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->

I meant `report` to be identified by purpose - describing an outcome, asking for nothing - but the model is still reading it mostly by the one surface cue it found, since `question` posts usually contain a "?" and `report` posts usually don't. Across the three after-run seeds, 4 to 7 of the 9 real `report` test posts were predicted `question` each time, while almost no `question` posts were mistaken for `report` - a one-directional error that confirms the model learned a lexical shortcut for `question`, not the purpose-based distinction my taxonomy actually draws.

---

## Stretch Features

### Confidence check

**Stretch: Confidence check** - I'll report whether the model's confident predictions are right more often than its unsure ones, using the `confidence` data already in `results_three_seeds_after.json` (mean confidence when right vs. wrong, accuracy on the most- vs. least-confident third) across the three after-run seeds.

Yes, but the gap shows up more in accuracy by confidence tier than in the raw confidence numbers themselves. Mean confidence when right (0.307 average across seeds) and when wrong (0.286 average) are close, so the model doesn't clearly "know" when it's guessing. But accuracy on the most-confident third of predictions (0.83 average) is much higher than on the least-confident third (0.39 average) - so confidence still ranks predictions usefully even though its absolute values don't separate right from wrong by much.

### Per-label error write-up

**Stretch: Per-label error write-up** - I'll analyze `report`, the worst-performing label (F1 0.308, 0.000, 0.000 across the three after-run seeds), using the confusion matrices already in `results_three_seeds_after.json` to confirm it's confused with `question`, then read the actual misclassified `report` posts to describe what they have in common.

Reading the seed-42 misses, the "?" theory only explains one of the four `report`→`question` mistakes - the other three have no question mark at all, just hedging or casual phrasing ("I'm not sure if...", "if for some reason I may need it," a one-line "Thx... Thank you!"). So the model seems to be picking up on uncertain or casual tone generally, not just punctuation. The three `report`→`advice` misses are different: each one narrates a fix in first person - "I replaced the drive and it worked," a step-by-step "How It Works" writeup - which reads a lot like my `advice` posts even though the writer is just describing what they did, not telling someone else to do it. Same root problem either way: `report` is supposed to be about purpose, but its posts borrow sentence patterns from the labels around it.

### A Second Measured Improvement

**Stretch: A second measured improvement** - I'll add new `report` training examples written with the hedging/casual tone and first-person fix-narration patterns the per-label write-up found (rather than loss class-weighting), retrain across the three after-run seeds, and report whether `report`'s F1 improves.

### Run Log — Stretch

**Device:** cuda (NVIDIA GeForce RTX 3070 Laptop GPU)

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Balance | No label above 40% or below 10% of 252 | 24.2%-25.8% | 24.2%-25.8% | 24.2%-25.8% | MET |
| 2. Per-label F1 | question/advice/report >=0.65, opinion >=0.50 | q 0.737, o 0.625, a 0.696, r 0.556 | q 0.667, o 0.182, a 0.500, r 0.727 | q 0.615, o 0.533, a 0.696, r 0.333 | MISS |
| 3. Seed stability | Accuracy spread <=0.10 | 0.658 | 0.553 | 0.579 | MISS (spread 0.105) |
| 4. Fresh posts | >=8/10 correct | 9/10 | 6/10 | 7/10 | MISS |
| 5. Overall accuracy | >=0.75 | 0.658 | 0.553 | 0.579 | MISS |

Row 1 is measured on the full 252-post `labels.csv` now in place (up from 248 after the opinion fix) - bounds are unchanged, only the post count grew.

**Did it help, and how do I know:**

Yes, for what it targeted, but not for free. `report`'s F1 went from 0.308/0.000/0.000 to 0.556/0.727/0.333 - a real improvement on all three seeds, even though two still miss the 0.65 bar. Fresh-post accuracy improved too (8/10, 5/10, 5/10 -> 9/10, 6/10, 7/10). But seed 7's `opinion` F1 collapsed from 0.750 to 0.182, with 8 of 10 test posts called `advice` instead. I checked: it's the same 10 test posts both times, not a different split, so this is a real effect of retraining with three more `report` rows in the training set - on a dataset this small, a few new examples of one label can shift the decision boundary for a completely different pair. Several of the newly-misclassified `opinion` posts were already borderline, written as hedged recommendations ("Don't think it is any better," "We will do this..."), so the fix didn't create a new problem so much as expose one that was already close to the line.

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
