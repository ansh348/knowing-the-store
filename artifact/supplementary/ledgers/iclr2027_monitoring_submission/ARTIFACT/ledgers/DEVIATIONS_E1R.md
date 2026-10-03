# Deviations and instrument failures — E1-R

Spec frozen at `9ac91a2`. Every departure from it, and every instrument failure found while
executing it, is recorded here. Two of these are failures of instruments built *for this
pass*, which is the same class of error the paper's own ledger exists to record.

## D-E1R-1 — NB-1 category assignment strengthened after the freeze

**What changed.** `SPEC_E1R` §(b) NB-1 said "assign the question to a category by maximum
content-token overlap". The first implementation scored overlap by Jaccard alone and assigned
a category to almost nothing, because attribute names are terse relative to question length.
The assignment was changed to score by overlap **count**, to singularize tokens, and to let
the category name itself act as an additional surface form. Assignment rate on FR-Bank rose
to 399/661.

**Why this is admissible.** The change was made **before any baseline AUROC was computed**,
and it makes the opposing baseline **stronger**, not weaker. A baseline adjustment after a
freeze is allowed to move in exactly one direction — against the paper's interest — and this
one does. Had it moved the other way it would be inadmissible regardless of timing.

## D-E1R-2 — NB-3 disqualified as an index-reading baseline

**What happened.** NB-3 was frozen as TF–IDF over the serialized index text **concatenated
with the question**. It scored 0.9625 on Mem0 and 0.9512 on A-MEM — backends whose indexes
declare nearly every field "not expressible by this backend". A text classifier cannot read
structure that is not present, so the score had to be coming from somewhere else.

**Diagnosis.** The three-way ablation (index+question / index-only / question-only) shows
index-only at 0.4464–0.6909 and question-only at 0.8707–0.9667, with question-only *exceeding*
the concatenated version on every one of the ten population-provenance cells. NB-3 was
reading question templates — the E1-QP authorship confound already disclosed as D94 — and the
index text was diluting that signal rather than contributing to it.

**Disposition.** NB-3 is excluded from the baseline comparison of record. Its index-only
ablation is retained as `NB-3-idx`, which is what the frozen spec was attempting to measure.
The full ablation is kept in `NUMBERS_E1R.md` §7 as an instrument-failure record.

**Lesson, in the paper's own terms.** A baseline that concatenates the question with the
store description is not a store-reading baseline. This is the same semantic assumption
hidden inside a mechanical operation that the manuscript's instrument ledger already
documents five times over; it recurred while building an instrument to answer a reviewer
about baselines.

## D-E1R-3 — NB-5 encoder is local open-weights, not the presence control's embedder

Disclosed in the frozen spec and repeated here. NB-5 uses
`sentence-transformers/all-MiniLM-L6-v2` from the local HuggingFace cache, run fully offline,
because embedding through the study's original OpenAI embedder would require a paid call and
this pass is fenced at $0. The NB-5 figure is therefore **not** interchangeable with the
two-channel presence control's embedding channel, and the manuscript must not present it as
such.

## D-E1R-4 — pooled hard-tier absolute levels are backend-confounded

**Found while executing (b), not anticipated by the spec.** All 35 positives in the pooled
hard tier are FR-Bank items, so the one-bit rule "this item is FR-Bank" attains AUROC
**0.7541** — above the monitor's pooled indexed AUROC of 0.7530.

**Scope of the problem.** This affects the interpretation of *absolute levels* on the pooled
row for every reader, monitor and baseline alike. It does **not** affect the paired delta,
because a score constant across arms cannot produce a delta; the blind arm on the identical
population scores 0.5258. The manuscript already reports the within-FR-Bank row (+0.2037)
for a related reason, but it does not currently state the magnitude of the trivial separator.

## D-E1R-5 — the frozen branch set was incomplete in two places

Recorded rather than papered over. Where no frozen branch fits, none is claimed to have
fired.

| Sub-step | Observed pattern | Frozen branches | Disposition |
|---|---|---|---|
| (b) baselines | Monitor beats every index-reading baseline on FR-Bank FOK (both arms) and NOK-TRUE; ties the best baseline on NOK-BELIEVED | Four branches, none covering "loses on TRUE, ties on BELIEVED for one judgment only" | Branch 3 applies to the TRUE arm and to BELIEVED-FOK. NOK-BELIEVED is an unanticipated cell and is reported as such, not force-fit. |
| (d) reliability | Indexed arms are monotone-but-misscaled rankers (ρ = 0.90, 1.00); the **blind** arm is neither (ρ = 0.10, p = 0.87) | Branch required the pattern across the arms jointly | The substantive disposition still follows for the arms the paper's claims rest on: A4/B5 conceded for the indexed arms, and the blind arm is disclosed as failing to rank as well. |

Sub-steps (a) and (c) and the ECE half of (d) each selected a frozen branch cleanly with no
ambiguity.

## D-E1R-6 — cross-vendor aggregation reimplementation drifted; replaced by the committed scorer

The first implementation of the 84-item cross-vendor aggregation reproduced 8 of 12 published
rows exactly and drifted in the third-to-fourth decimal on the other 4. Cause: the frozen
protocol dedups draws by `(item_id, arm, draw, prompt_hash)` with first-wins, and averages
NOK draws independently of FOK draws. The reimplementation was discarded and
`e1xv_crossvendor/tools/score_e1xv.py`'s own `load` and `collapse` are imported directly. All
12 rows then reproduced exactly. No sensitivity was computed against the drifting version;
the reproduction gate blocked it.

## D-E1R-7 — the R81 order's third prediction was not a prediction; withdrawn before scoring

**What happened.** The R81 order registered three predictions for NB-6. NB6-3 read: "monitor
FOK-TRUE (0.7003) exceeds best NB-6 FOK-TRUE by more than the tolerance." But the order also
defined the FOK-6 score as the maximum similarity over **all names in the per-category name
map** — which is, token for token, what NB-4 (lexical) and NB-5 (embedding) already compute.
Same name list (`attr_by_cat` flattened), same tokenizer (`index_features.toks`), same
encoder (`all-MiniLM-L6-v2`), same estimator. FOK-6's value was therefore already fixed by
the committed `results/baselines_final.json` before the R81 pass began, and its comparison
against the monitor was already printed in Table 18.

**What changed.** NB6-3 is withdrawn as a prediction before any NB-6 score was computed, and
replaced by a declared **reproduction check**: FOK-6 must reproduce the committed NB-4 and
NB-5 values at four decimal places on `R-FOK-FRB` TRUE and BELIEVED. A fifth-decimal
difference from float summation order is not a failure; a four-decimal mismatch is a STOP,
because it would mean one of the two code paths is wrong. Consequently Table 18's NB-6 column
carries the NOK rows only, prints a dash on every coverage row, and states the reason in its
footnote; the finalizer does not recompute `best` or the monitor delta on any coverage row.

**Why this is admissible.** It moves in the only direction a post-freeze adjustment may move:
it **removes** a claim the paper would otherwise have made. Registering a prediction whose
outcome is already determined by committed artifacts, and then reporting it as confirmed,
would have manufactured a third piece of apparent evidence out of a number already in the
table under two other names. The alternative — printing the same value twice under two
different instrument names — would have invited a reviewer to ask what the new column adds,
and the honest answer would have been "nothing on these rows". Recorded before scoring, so
the disclosure cannot be read as a response to a result.

**Disposition.** `ADDENDUM_R81.md` §3 and §5 carry the withdrawal and the replacement check.
The R81 registration table row records two registered predictions (NB6-1, NB6-2) and one
reproduction check, not three predictions. The R81 report states the identity in the same
sentence that reports the check.

## D-E1R-8 — a registered measurement refuted a printed claim; the claim is corrected, not the measurement

**What happened.** NB6-1 predicted that the monitor's NOK-TRUE AUROC (0.7339) would exceed
the best superseded-names matcher by more than the ±0.05 tolerance. It did not. The embedding
variant reaches **0.7484**, above the monitor, with a margin of **−0.0145**. The prediction
was registered on 2026-08-29 at HEAD `2bb7fd9` with both outcome sentences frozen, before any
value existed.

**What this refuted.** Two statements that were already in print:

| Site | Before | After |
|---|---|---|
| §4.3 | "Mechanical readers of the same index do not reach the monitor where lifecycle structure exists." | scoped to coverage; the obligation sentence pair from the frozen FAILS branch lands beside it |
| §4.3 | "Its NOK-TRUE margin is +0.1365." | removed from main text; the margin of record on that row is now −0.0145 |
| Table 18 caption | "the monitor outranks every mechanical reader" on both FR-Bank populations | scoped to coverage; the obligation row states NB-6's lead |
| Table 18 footnote | "The two rows where a baseline outranks the monitor are both of this kind or on a structureless backend." | three kinds now, the TRUE obligation row named as the third |

**Why this is admissible.** It is not a departure from the spec; it is the spec working.
Publish-regardless was the rule under which NB-6 was registered, and the frozen FAILS text was
written before the number existed precisely so that this outcome could not be renegotiated
afterwards. The correction moves against the paper in every instance: a margin claim becomes
a no-margin statement.

**What is NOT claimed.** |−0.0145| is inside the ±0.05 tolerance, so NB-6 does not beat the
monitor under the suite's own convention. The honest statement is that the monitor holds **no
margin** over a superseded-names matcher on that row, not that the matcher is the better
judge. The manuscript says exactly that, in §4.3 and in F.8.

**Disposition.** `+0.1365` remains in `NUMBERS_E1R.md` §6 as the pre-NB-6 record and in §11's
"Effect on the table of record", so the change is visible rather than overwritten. The R81
report carries the before/after. U9 is untouched: F.8's NB-6 paragraph deliberately omits the
retention figure so that no connective can join the two.

## D-E1R-9 — the 003818b appendix over-read an exact-match test

**What happened.** The composition census landed at `003818b` reported that an obligation's own
attribute name appears in the superseded-names section only 7 times in 104, and concluded:
"this is not a per-item label lookup; what the matcher recovers is which kinds of content the
store marks as superseded."

**Why that was wrong.** The 7/104 test is an **exact slot match**. The NB-6 variant carrying
the result is the embedding matcher, which scores near-synonyms: a question about one hiking
slot can match `hiking_preference` without an exact hit. An exact-match miss is therefore not
evidence that the matcher failed to read the item's own name. The test cannot separate

  (a) the matcher reading a near-synonym of the item's own name, from
  (b) the matcher recovering which content classes the store marks as superseded,

and the appendix presented (b) as established. It was the stronger and more interesting of the
two, which is exactly why it needed evidence it did not have.

**What changed.** Both the appendix paragraph and `NUMBERS_E1R.md` §12 now state the test as an
exact slot match, state that it does not separate the two readings, and stop. No sentence
presents the class-level reading as established.

**What survives, and on what evidence.** The naming-versus-counting sentence stays, because it
rests on the per-state rows and not on the 7/104 test: the matcher reaches 0.9534 on
supersession, which the index names, and 0.4823 and 0.4053 on expiry and retraction, which it
only counts.

**Why this is admissible.** It removes a claim. The correction landed before Phase 2 wrote any
section against the over-read sentence, so nothing downstream inherited it.
