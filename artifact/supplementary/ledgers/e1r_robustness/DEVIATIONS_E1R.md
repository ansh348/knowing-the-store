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

## D-E1R-10 — the own-name census keyed entry ids without the persona; 7 of 104 is 74 of 104

**What happened.** `AUX-E1R-NB6-COMPOSITION` (`NUMBERS_E1R.md` §12, "The matcher is not reading
the item's own label") reports that an obligation's own attribute name appears in the
superseded-names section it was shown for 7 of 104 items under TRUE (5 of 63 supersession, 2 of
26 retraction, 0 of 15 expiry) and 13 of 104 under BELIEVED, and the manuscript prints the TRUE
figure (`paper_v6.tex:1861`). The script, `tools/nb6_composition.py::slot_map` (L54–57), builds
`{entry_id: slot}` over `e1_metamemory/backend_entries/frbank.json` **without the persona**.
FR-Bank entry ids restart at `lb_00001` in every persona bank: the file holds 18,936 entries
under 622 distinct ids, each reused by up to 40 personas, so the map returns the slot of
whichever persona came last in the file. Spot check: aisha's `lb_00131` is `gym_location` in
aisha's bank; the map returns `family_heirloom:jebena_from_khartoum`.

**The census, keyed by (persona, entry id), 2026-09-12** (`reviews/RESP_REG_REPORT.md` Phase 1;
the same exact-slot-match rule on the scrubbed `pn_members` slots):

| Provenance | supersession (63) | retraction (26) | expiry (15) | all (104) |
|---|---:|---:|---:|---:|
| TRUE, printed | 5 | 2 | 0 | 7 (0.067) |
| **TRUE, corrected** | **63 (1.000)** | **11 (0.423)** | **0** | **74 (0.712)** |
| BELIEVED, printed | 10 | 1 | 2 | 13 (0.125) |
| BELIEVED, corrected | 24 | 3 | 4 | 31 (0.298) |

**What this changes.** Every supersession-derived obligation carries its own name in the TRUE
section it was shown. The §12 heading "The matcher is not reading the item's own label" is
unsupported; D-E1R-9's caveat, written for a 7-of-104 world, loses its premise — the exact
match is not a miss to be explained by near-synonyms, it is a hit on the whole state. The
per-state rows of §12 and §13 (0.9534 / 0.4823 / 0.4053; the monitor's 0.8572 / 0.5110 /
0.5638) are untouched: they never read `slot_map`. The "named across all three index
variants" clause (`paper_v6.tex:1861`) and the FULL 3/47, SLOT-ABLATED 3/35, CAT-ABLATED 1/22
breakdown (`NUMBERS_E1R.md:350–351`) fall with the figure; corrected, the per-variant rates are
FULL 32/47, SLOT-ABLATED 29/35, CAT-ABLATED 13/22 (TRUE, all states).

**Sites that print the figure or the hedge.** `paper_v6.tex:1861` (7 of 104), `:1862` (the
near-synonym hedge that rests on it); `NUMBERS_E1R.md:340` (heading), `:347–348` (table), `:350–351`
(per-variant rates), `:358–366` (the exact-match paragraph); `CLAIMS.md` POSTHOC-R81-2 (L261–266,
"it did support it"); `DEVIATIONS_E1R.md` D-E1R-9 (its premise). `results/nb6_composition.json`
fields `pn_named_in_index`, `pn_named_rate`, `named_by_lifecycle_state`, `n_named_pn`,
`n_unnamed_pn`, `nb6_*_auroc_{named,unnamed}_pn`, `monitor_auroc_{named,unnamed}_pn`,
`mean_nb6_emb_{named,unnamed}_pn` carry the collision; no other field does.

**Why this is admissible.** The census is post hoc and unregistered (POSTHOC-R81-2); no frozen
text or registered verdict rests on it. The correction moves against the manuscript's
convenience: the lookup now looks like a read of the item's own name on the one state the
index names, which is the reading D-E1R-9 declined to claim and the reviewer's W3 suspects.

**What is NOT claimed.** That the *monitor* reads the name. That is the registered question of
`ADDENDUM_RESP` §L1 (the own-name ablation) and is not settled by this census.

**Disposition.** `NUMBERS_E1R.md` §12: the table gains the corrected rows with the printed
figures retained as the pre-correction record (D-E1R-8's convention), the heading is retitled
"Own-name presence in the section the matcher reads (corrected, D-E1R-10)", and the
exact-match paragraph is rewritten to state the corrected count and stop. `nb6_composition.py`
`slot_map` is patched to key by (persona, entry id) and re-run; the diff of
`results/nb6_composition.json` is confined to the fields listed above and is recorded in the
commit. `paper_v6.tex:1861–1862`, `CLAIMS.md` POSTHOC-R81-2 and Appendix G's deviation index are
corrected under R97 authorization blocks (`reviews/RESP_REG_REPORT.md` §5 item 11).
`resp_review/tools/verify_resp.py` pins the corrected census.

## D-E1R-11 — the 661 index parser scores the empty-section marker `(none)` as an attribute name

**What happened (found 2026-09-14, `nb6_sweep/tools/step1_reproduce.py`).** `index_v2.py`
prints the line `  (none)` under `ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT` when a summary
has no superseded name. `index_features.parse` (`e1r_robustness/tools/index_features.py`, the
`sup` branch) returns that line through `_names` as the one-element list `["(none)"]`, and
`run_nb6.name_lists` hands it to the lexical and embedding scorers as a name. On R-NOK-FRB
under TRUE, **63 of the 242 summaries have an empty section; 195 of 661 items read them (178
negatives, 17 positives: 12 of the 15 expiry obligations and 5 of the 26 retraction
obligations)**. Those items were scored on cosine(question, "(none)") rather than 0.0, and the
marker is counted in the ledger's names-per-item figure. The 444 path does not share the fault:
`r82_counterfactual/index_v3.named_sections` returns `[]` for the same line, so
`AUX-CF2-NB6-V2` and `AUX-R104-MARGIN` are unaffected. This is a divergence between two
parsers reading the same rendered line, not a design choice. No BELIEVED list is empty on the
661, so `R-NOK-FRB|BELIEVED` (0.5858) is unaffected.

**Every printed number that moves, marker stripped** (`nb6_sweep/results/step1_reproduce.json`):

| figure | site | as committed | marker stripped |
|---|---|---:|---:|
| NB-6 embedding, R-NOK-FRB TRUE | §11 obligation row; NB6-1 | 0.7484 | **0.7442** |
| NB-6 embedding, supersession positives vs all negatives | §12, §13 | 0.9534 | **0.9599** |
| NB-6 embedding, expiry positives vs all negatives | §12, §13 | 0.4823 | **0.2570** (see mechanism) |
| NB-6 embedding, retraction positives vs all negatives | §12, §13 | 0.4053 | 0.5026 |
| TRUE superseded names per item | §11 "averages 1.75" | 1.7474 | **1.4523** |
| 444 v2 superseded names per item (not printed in this ledger; `parse` also read it) | — | 1.98 | 1.76 |
| NB-6 lexical, R-NOK-FRB TRUE | §11 | 0.5738 | 0.5738 (unchanged: "none" never overlaps a question's content tokens) |

Downstream, `NUMBERS_SIDE.md` AUX-SIDE-S2-CENSUS's recall of TRUE names carries the marker in
its denominator: BELIEVED rendered 0.2996 → 0.3604 against real names; uncapped 0.6658 →
0.8010. Its precision figures (0.0348 / 0.0357) do not move.

**Mechanism behind the expiry figure — do not print 0.2570 bare.** With the marker stripped,
every item that reads an empty section receives the constant score 0.0: 12 of the 15 expiry
positives and 178 of the 557 negatives tie there, and the remaining 379 negatives, which read a
non-empty list, all score above 0.0. The AUROC is set by where that tie block sits against the
varied negatives (half credit against the 178, none against the 379), not by any anti-prediction
in the scores. The committed 0.4823 was the same block scored on cosine(question, "(none)"),
which varies with the question and so ranked the block arbitrarily rather than as a tie.

**What this changes.** NB6-1's outcome does not change: the monitor's 0.7339 is below the
matcher on both readings (margin −0.0145 as committed, −0.0103 stripped), inside the ±0.05
tolerance either way, and the registered statement fails on both. NB6-2 is untouched. The §12
reading that the aggregate is carried by supersession-derived items strengthens (0.9599 on that
state); the expiry and retraction rows lose their standing as per-state measurements of the
matcher, since on those states the matcher mostly reads an empty list.

**Direction.** Against the manuscript's interest on the headline (the mechanical reader's
aggregate falls by 0.0042, and the list it reads is shorter than printed, 1.45 rather than
1.75 names), which sharpens the short-list objection the sweep in `nb6_sweep/` was built to
test.

**Disposition.** Recorded here; no number in `NUMBERS_E1R.md` is changed by this entry. The
committed rows stand as the record of the computation that was run, under D-E1R-8's convention;
a correction to the printed rows, to `paper_*.tex` sites that quote 1.75 / 0.7484 / 0.4823, and
to `index_features.parse` is a separate ruling and is not made here. The sweep in `nb6_sweep/`
uses the marker-stripped list as its base (0.7442 at 1.45 names) and prints 0.7484 as the
reproduction of the committed computation.
