# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

<!-- Your criterion. It must name a number. -->

Counted once, on the final set of 200 labelled posts and before any training, no single label makes up more than 40% of the posts (80 or fewer) and no label makes up less than 10% (20 or more). If any one of the four labels falls outside that range, the criterion is missed.

**Why this target:**

With four labels an even split is 25% each. A label above 40% means a model that always guesses it scores 40% without learning anything, and training would lean toward it. A label below 10% is 20 posts, which leaves about 3 in the test split (15%), too few for an F1. My smallest label, [label], has [N] posts.

---

## 2.

<!-- Your criterion. -->

On each of the three seeds, every label has an F1 of at least 0.65 on the held-out test split, except the smallest label, which needs at least 0.50. F1 is computed per label from precision and recall on the test posts. If any label is below its number on any seed, the criterion is missed.


**Why this target:**

Four labels means guessing gets about 25%, so an F1 of 0.65 is well above chance. I set it below the 0.75 in criterion 5 because the worst label is always below the overall average. The smallest label, [label], has only about [N] test posts out of about 30, so one post can move its F1 by 15 points or more. I set it looser, at 0.50, for that reason. Opinion and advice overlap, so I expect them to be the closest calls.

---

## 3.

<!-- Your criterion. -->

Across the three seeds, I take the highest overall accuracy on the held-out test split minus the lowest. That difference is no more than 0.10. If it is larger than 0.10, the criterion is missed.

**Why this target:**

A model that scores 0.80 on one seed and 0.65 on another can't be trusted to score either number next time. The seed changes both training and which posts land in the test split, so some of the gap comes from the split and not the model. One post is worth about 3 points on a test split of about 30 posts (15% of 200), so a gap of 0.10 is about three posts. I did not go tighter because that would mostly measure luck in the split. Criterion 5 sets the level of accuracy. This one checks that the level holds from run to run.

---

## 4.

<!-- Your criterion. -->

On 10 new posts that I label myself and that are not among the 200 labelled posts, the model labels at least 8 correctly on each of the three seeds. If any one seed gets 7 or fewer right, the criterion is missed.


**Why this target:**

All my posts come from one forum, so this does not test a different community. It does test posts that were never in my 200, which guards against a split that shares near-duplicates or a quirk of when I collected. I label the ten before the model runs so I cannot bend a label toward its answer. I set 8 of 10 because it is the nearest whole number to the 0.75 in criterion 5 and allows two misses. Ten posts is too few to separate 0.70 from 0.85, so this is a sanity check, and criterion 5 is the precise measurement.

---

## 5.

<!-- Your criterion. -->
Overall accuracy on the held-out test split (about 30 of the 200 labelled posts) is at least 0.75 on each of the three seeds. If any one seed falls below 0.75, the criterion is missed.




**Why this target:**
I have four labels, so guessing gets about 25%. 0.75 is three times that, which I would call useful for sorting posts. On about 30 test posts, 0.75 means getting about 23 right, and one seed with 22 right (0.73) is a miss. Because it has to hold on all three seeds, I did not set it higher. Opinion and advice overlap, so I expect most errors there.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
