# ADDENDUM_R76 — registration freeze for the R76-A amended pass

Frozen against baseline HEAD `b839464209fc8710b261f403874868ef0044bd35` (post-R75-V),
2026-08-24, BEFORE any R76 monitor call and BEFORE any scored probe. Spec: the R76
program instruction as amended by [AUTHOR-1]'s in-session RULING (path (a)); that ruling
governs where it and the original R76 instruction differ. Governing rules inherited from
R74/R75: **nothing unregistered may be reported**; no committed value is ever recomputed;
registered verdicts are never re-adjudicated; publish-regardless — every result below
prints under its frozen text, nulls and flipped directions included.

Ledger of record for R76 results: `r74/NUMBERS_R74.md`, new keys `AUX-R76-*`. Verifier:
`r74/tools/verify_r74.py`, extended to the AUX-R76 keys. Manuscript scan:
`iclr2027_monitoring_submission/tools/trace_scan_v12.py` (unchanged instrument).
Deviations continue in `iclr2027_monitoring_submission/DEVIATIONS_R74.md` under continued
numbering (D-R74-12, D-R74-13 opened by this pass).

Bootstrap spec, all sections: the committed estimators
(`e1_metamemory/tools/score_ladder.py::auroc_ci`, `score_e1.py::auroc`), 1,000 resamples,
seed 42, percentile method, single-class draws discarded.

Metered budget for this pass: **$0.35 projected, hard ceiling $40** (the R76 instruction's
ceiling, carried). The lane's projection is reported before launch; the run stops at the
ceiling.

---

## §A1 — NS-3 and NS-4 are STRUCK before any computation

The original R76-R registration would have frozen NS-3 (blind NOK interval includes 0.50
on the matched-84 for mini and Opus 5) and NS-4 (indexed-minus-blind NOK delta excludes
zero on every completed lane, mini included), both to be measured on an authorship-matched
re-rendering of the committed 84-item FR-Bank cell. Both are struck. The findings below
were established from committed files during the pre-freeze premise check and are recorded
here verbatim as **findings, not failures**. They print nowhere in the manuscript; they
live in this registration and in the DESCOPE report.

### A1.1 — the 84-cell cannot be authorship-matched under the frozen X5 protocol

The target cell is `e1xv_crossvendor/manifests/cell_84.json` (`expect` = `rebuilt` =
{n 84, n_fok_pos 54, n_nok_pos 40}); it is the population behind Table 7's committed
`0.7972 [0.6949, 0.8927]`. It is a **different item universe** from the X5 cell: item ids
are `frbank:*` against E1-NS's `ns:*`, with zero overlap, so R76-G's disjoint branch fires
and the instruction routes to "render all 84." That step cannot execute:

1. **Slot-vocabulary absence.** `e1_metamemory/build/items_final.json` carries no `slot`
   key on any of its 2,653 items (key census: `absent_mechanism`, `attack_vector`,
   `backend`, `intent`, `item_id`, `label`, `label_pre`, `n_removed`, `persona`,
   `pn_evidence`, `question_id`, `subtype`, `tier`, `variant` at 2,653; `pn_members` 122;
   `question` 426; no `slot` at any count). The X5 renderer's input tuple is
   `(entity, slot, CURRENT)`; E1-NS has slots because the slice was **constructed** around
   a closed 12-token vocabulary. FR-Bank has no counterpart to read.

2. **Intent hardcoding in both frozen instruments.** 22 of the 84 items are non-CURRENT
   intents (UPCOMING 15, CHANGE-AWARE 6, PAST-EVENT 1). The frozen renderer
   (`r74/tools/x5_render.py::RENDER`) emits "what {entity}'s current {slot_phrase} is, as
   of today"; the frozen checker (`x5_check.py`, `x5_render.py::work`) requires
   `extracted["intent"] == "CURRENT"`. Rendering those 22 as CURRENT would change the
   intents, which the R76-R freeze forbade ("intents byte-identical"); running the checker
   unchanged fails them by construction, capping label transfer at **62/84 = 0.7381**
   against the registered 0.95 bar — an automatic S1 stop before any monitor call.

3. **Eight items have no entity and no slot.** The NATURAL_ABSENT items are second-person
   ("What kind of music do you usually listen to when relaxing at home?"), all ABSENT.
   They are unrenderable from the tuple and undroppable under the freeze ("84 items,
   labels byte-identical").

4. **The label-transfer gate is undefined on this cell.** For E1-NS the carried label is a
   registered function of (intent, store state) given a clean slot. FR-Bank labels depend
   on the specific fact's version history — "Is Nadia planning to stage at Noma?" is PN
   only because that plan was superseded. The checker re-derives (entity, slot, intent);
   it cannot re-derive an FR-Bank label at all.

5. **The label is content-borne, so re-rendering cannot move blind levels toward chance.**
   Deterministic census on committed labels (§A4.1 below): attack vector alone attains
   AUROC **0.9736** on this cell, above the committed supervised TF–IDF 0.7972 it was
   meant to decompose, and six of eight strata are single-class. By contrast the X5 cell
   holds P(PN | slot) = 1/3 **exactly** on all four of its tokens. NS-3 is therefore not
   merely likely to fail on the matched-84 — it is **structurally precluded**, and the
   original registration's stated expectation ("expected to hold per the n=36 result")
   does not transfer between these two populations.

### A1.2 — NS-4 is unreachable from the existing E1-NS pool

Read instead as powering the E1-NS cell itself, NS-4 fails on arithmetic settled here
before any run:

- Measured at n=36 (mini, `AUX-R74-X5-MINI-NOK`): Δ = +0.2028, percentile CI
  [−0.1121, +0.4984]. Lower-side half-width h₋ = 0.2028 − (−0.1121) = **0.3149**;
  upper-side h₊ = 0.2956; symmetric mean h = 0.30525.
- Percentile-bootstrap half-width for a paired AUROC difference scales as n^(−1/2).
  NS-4 requires h₋(n) < Δ:
  n > 36·(0.3149/0.2028)² = 36 × 2.4109 = **86.80 → n ≥ 87**
  (n ≥ 82 on the symmetric mean, 36 × 2.2661 = 81.56).
- The E1-NS cell size is **3 × (confirmed PN)** — the registered removal rule keeps two
  non-PN per PN per slot token, which is what holds P(PN | slot) = 1/3 exact
  (`x5_render.py`, lines 29–35; verified: 36 = 3 × 12). n ≥ 87 therefore needs **≥ 29
  confirmed PN** of the 33 PN candidates.
- The pool cannot supply them. `WORKBOOK_EVIDENCE_ADDENDUM.json` disposes the 33
  candidates as **12 confirmed PN / 11 finalized rejections / 10 routed-back**. The 11
  finalized rejections are not re-openable, capping confirmed PN at **22** and the cell at
  **n = 66** — the committed optimistic census, which agrees.
- At the ceiling n = 66: h₋ ≈ 0.3149·√(36/66) = **0.2326** > 0.2028 → the mini interval
  still includes zero. At the base-rate expectation (12 PN of 23 finalized = 52%, so ≈5 of
  the 10 routed-back return PN → 17 PN → n = 51): h₋ ≈ **0.2646** → includes zero.

**Conclusion frozen here:** NS-4 for mini is not reachable by any disposition of the
routed-back rows. Closing it requires constructing roughly 17 further confirmed-PN E1-NS
items — new item generation plus human adjudication, a data build, not a monitor pass.
NS-2's registered mini failure (D-R74-11, `AUX-R74-X5-MINI-NOK`) therefore stands as the
final word on that quantity for this submission, in its frozen words, unre-adjudicated.

## §A2 — the paraphrase replication (option 4) is DECLINED for this submission

Frozen rationale, written before any further work: the label on lifecycle cells is
**content-borne**, not merely style-borne — attack vector alone scores 0.9736 on the
matched-84, above the supervised probe it would explain. A content-preserving paraphrase
must by construction retain the question's attack-vector semantics, so it cannot move
blind levels toward chance; its blind-side result is determined in advance, and its
delta-side null is near-foregone at the achievable n. The prior-controlled instrument for
this claim already exists and is already measured: the balanced E1-NS cell with
P(PN | slot) = 1/3 exact. Building a second, weaker instrument would add cost and a
publication surface without adding evidence.

**Disposition:** DECLINED for this submission. Revisitable as rebuttal material only, and
if revisited it must not be described as authorship matching in the E1-NS sense — it is a
paraphrase-robustness check, and NS-3-class predictions must not be attached to it.

## §A3 — NS-5: Haiku 4.5 on the authorship-matched cell (metered, ≈$0.35)

**Population.** The existing X5 cell, unchanged and not rebuilt: the ruling-(a) rendered
n=36 authorship-matched E1-NS cell (12 PN, 17 PRESENT, 7 ABSENT; 29 personas; 4 slot
tokens; label transfer 36/36 = 1.0, `AUX-R74-X5-TRANSFER`). Question surfaces are the
frozen renders in `r74/x5/x5_render.json`, byte-unchanged. No re-render, no re-check.

**Lane.** `claude-haiku-4-5-20251001` at the committed X4 lane configuration: E1-XV
protocol, temperature 0.0 (D86 records Haiku accepts the frozen temperature),
max_tokens 200, k=5, Batch API (D92), system-role assembly (D88), price (1.00, 5.00) per
1M tokens with the 0.5 batch multiplier. Arms BLIND and INDEXED-TRUE, index =
`frbank:{persona}:FULL:TRUE`, prompts byte-unchanged from frozen `prompts_e1` with both
digests asserted, parse on the frozen E1 path. Exact served model identifier recorded and
checked before launch (E1.7 preventive rule); identifier mismatch = do not launch.

**Projection rule.** Two probe calls, then a projection from measured probe tokens
reported before submission. Reference projection from the committed Opus rows (562,335
input / 77,445 output tokens over 360 OK rows, which recompute the ledgered $2.3739
exactly): Haiku at the same input volume costs **$0.335 at 60 output tokens/call, $0.389
at 120, and $0.461 at the max_tokens=200 ceiling** — the lane cannot exceed $0.47.

**Estimator.** 360 calls (36 items × 2 arms × k=5), draws averaged per the committed
ladder estimator, then the committed `auroc` / `auroc_ci`. Zero-parse-failure standard;
any anomaly gets a D-entry, never a silent fix.

**Registered reading — three outcomes, DESCRIPTIVE ("reports", XV-5 style).** This
adjudicates nothing: **XV-1's registered failed verdict is untouched in every branch**, no
paired-delta claim moves, and the slogan is not touched (D-R74-11 precedent). The question
is only: does Haiku 4.5's blind NOK remain below chance when the question text is
authorship-matched? Frozen sentences, one of which prints in Appendix C beside D93:

- **(i) interval entirely below 0.50** → *"On the authorship-matched cell the Haiku 4.5
  blind NOK interval lies entirely below chance, so the inverted blind-NOK prior of XV-1
  survives authorship matching on this $n=36$ cell; that is consistent with a property of
  the model rather than of how the questions were written, and XV-1's registered verdict is
  unchanged."*
- **(ii) interval includes 0.50 and point ≥ 0.45** → *"On the authorship-matched cell the
  Haiku 4.5 blind NOK interval includes chance, which is consistent with the inverted
  prior of XV-1 attenuating once question authorship is matched; at $n=36$ this is
  suggestive and not a test of XV-1, whose registered verdict is unchanged."*
- **(iii) interval includes 0.50 and point < 0.45** → *"On the authorship-matched cell the
  Haiku 4.5 blind NOK point stays below chance while its interval includes chance, so the
  matched cell is indeterminate at $n=36$ on whether the inverted prior of XV-1 reflects a
  property of the model or of question authorship; XV-1's registered verdict is unchanged."*

The measured blind, indexed, and delta values print as a row in the matched-cell appendix
table (§A5.3) in every branch, NOK primary, FOK descriptive.

**PRE-RUN AMENDMENT (R76-A2, logged before launch; amendments close at Batch submission).**
[AUTHOR-1]'s launch note required every branch sentence to (a) carry $n=36$ explicitly,
(b) claim consistency rather than confirmation, and (c) state in the same sentence that
XV-1's registered verdict is unchanged. Branch (ii) already satisfied all three and is
**unchanged**. Branch (i) failed (b) — its frozen text ended "…survives authorship matching
**and is a property of the model** rather than of how the questions were written," asserting
as established what one 36-item cell can only leave standing; it also carried neither the
explicit $n$ nor the XV-1 clause. It is amended above to "survives authorship matching on
this $n=36$ cell; that is **consistent with** a property of the model…, and XV-1's
registered verdict is unchanged." Branch (iii) satisfied (a) and (b) but omitted (c); the
XV-1 clause is appended and "is a model property or an artifact" is softened to "reflects a
property of the model or of question authorship." Both amendments are strictly weakening,
move against the paper's interest, and were made before the probe call. No other clause of
this registration is touched.

## §A4 — the two $0 items (NS-6 replaced)

### A4.1 — AV-CENSUS: the attack-vector one-feature diagnostic

**Class.** A **deterministic census on committed labels** — the same family as the
committed one-bit is-FR-Bank rule (0.7541, §4.3) and the Table 16 registration census. It
fits no model, holds out nothing, and draws no samples: it scores each item by the
observed PN rate of its committed `attack_vector` stratum and ranks. **No sampling
interval is defined or reported**, exactly as for the is-FR-Bank rule.

**Quantity.** Committed matched-84 labels (`cell_84.json` y_nok crossed with
`items_final.json` attack_vector): stratum counts and P(PN | attack vector), plus the
resulting AUROC with 0.5 tie credit (40 positives × 44 negatives = 1,760 pairs, 77 tied).

**PROVENANCE DISCLOSED (D-R74-13).** This quantity was computed **before this freeze**, as
the premise diagnostic that produced the R76 STOP. It is not a post-hoc addition. The
registered script recomputes it after the freeze and returns the identical value —
necessarily, since it is deterministic — so the post-freeze run is a reproducibility
artifact, not a second draw, and the reported number is the pre-freeze one in substance.
Because the quantity is a deterministic function of committed labels with no seed, no
sampling, and no fitted parameter, its value is invariant to when it was run; that is why
a pre-freeze computation is admissible here and would not be for a fitted or sampled
estimate. This registration fixes its interpretation before it enters the manuscript, and
the disclosure states the ordering rather than relying on the invariance silently.

**Frozen reading.** The label on lifecycle cells is carried by what the question is about,
not only by who wrote it. Attack vector is a designed axis of the item taxonomy and is
recoverable from question surface form; that it out-scores the supervised text probe means
the probe's signal is bounded by designed content structure, of which generator-template
style is a fraction. This is disclosed as a property of the benchmark's construction, not
as a defect and not as a failure of any monitor.

### A4.2 — MATCHED-PROBE: supervised TF–IDF on the 36 matched questions

**Apparatus.** The committed E1-QP probe, unchanged: `e1qp_questionprior/tools/probes.py`
`oof_tfidf` — TF–IDF (lowercase, ngram (1,2), min_df 1, sublinear_tf), logistic regression
(C=1.0, max_iter 2000, class_weight balanced, lbfgs), StratifiedGroupKFold grouped by
persona, n_splits = min(5, personas, positives, negatives), seed 42; then the committed
`auroc` and `auroc_ci`. Identical featurization and CV protocol to the Table 7 rows.

**Population.** The 36 matched `rendered_question` strings from `r74/x5/x5_render.json`,
target y_nok (12 PN vs 24 non-PN), persona as the grouping key only and never a feature.
n_splits resolves to 5 (29 personas, 12 positives, 24 negatives).

**Frozen reading.** A near-chance interval supports the matched cell's by-construction
neutrality — the E1-NS slice was built so question text carries no label signal, and the
probe is the direct check of that construction. Any separable signal prints as-is, with no
reinterpretation. **A wide interval is expected at n=36 with 12 positives and is disclosed
as such**; this row is a construction check on the E1-NS cell, not a measurement of the
FR-Bank populations, and it is not compared against the committed 0.7972 as if the two
sat on one population.

**Zero-shot reader row: SKIPPED, and the reason prints.** The committed zero-shot cache
`e1qp_questionprior/results/probe_llm_raw.jsonl` holds 362 rows, **zero** of them `ns:*`
items, and the matched questions are newly rendered text with no cached responses. The row
would require fresh metered calls, so under the $0 rule it is not run; the appendix states
that the zero-shot reader was not re-run on the matched cell.

## §A5 — integration text, frozen BEFORE NS-5 returns

Page discipline: main-text census target **no worse than the current 5 lines over** the
page-9 boundary at review line 485. Funded by §A5.1 first. Appendix additions are below
the boundary and are page-neutral for the gate.

### A5.1 — §5.4 dedup (funding; executed first)

Three of the five prose sentences after `tab:economics` restate its caption: the
$207-against-$234 projection, the $360-against-$233 reversal with both causes, and the
output-telemetry line. **Constraint honored:** X3's frozen non-confirming branch requires
that "both numbers print and the text states the discrepancy" **in the text**, not only in
a caption. The compression therefore keeps one sentence carrying both numbers and the
discrepancy, keeps the registered 25× price-range sentence and the registered Scope line
untouched, and drops only the caption-duplicated causal clauses and the output-telemetry
sentence, replacing them with a pointer at Table 2. Expected yield ~2–3 lines.

### A5.2 — §7.1 rewrite (frozen; replaces the fingerprint-only story)

The existing authorship-mismatch sentence and the "prevents treating the blind levels as
prior-controlled" sentence are replaced by the decomposition, in this order and with this
content:

(i) the question taxonomy is content-borne label structure — attack vector alone scores
$0.9736$, above the supervised probe's $0.7972$, with six of eight strata single-class —
so blind levels on lifecycle cells cannot be made prior-controlled by rewording, by
design; (ii) the supervised probe's signal is bounded by that designed structure, with the
generator-template component a fraction of it; (iii) the prior-controlled quantities are
the paired deltas and the balanced authorship-matched cell (P(PN | slot) = 1/3), where
blind NOK is at chance on both measured lanes; (iv) within-stratum probing is possible on
one stratum only (AV2, $n=16$) and is not offered as evidence.

At most two headline decimals enter the main text ($0.9736$ beside the committed
$0.7972$); every other value points at the appendix. **D94's record is appended to, never
rewritten**: the existing D94 disclosure line and its Appendix D pointer stand unchanged.
The zero-shot and matched-slice clauses of the existing sentence stand. Paired-delta
wording is untouched.

### A5.3 — matched-cell appendix table (layout ruling: Appendix D)

**Ruling:** the material lands in **Appendix D, `app:questionprior`**, as a new subsection,
not Appendix G. Appendix D already holds Table 7, the probe family this decomposition
explains; Appendix G is the registration record and carries no data tables. The MATCHED-
PROBE row lands in the new matched-cell table and is **not** duplicated into Table 7
(R75-F6 discipline: one row per quantity).

Contents, all keyed and traced:
- X5's four n=36 intervals from `AUX-R74-X5-MINI-NOK` / `-OP5-NOK` / `-MINI-FOK` /
  `-OP5-FOK` — blind, indexed, delta; NOK primary, FOK descriptive. **This closes the R75
  read-aloud flag that these values are stated in §7.2 but never printed.**
- the NS-5 Haiku 4.5 row (`AUX-R76-NS5-*`), same columns.
- the MATCHED-PROBE row (`AUX-R76-MATCHED-PROBE`), with the wide-interval disclosure and
  the skipped-zero-shot statement.
- the AV-CENSUS strata table (`AUX-R76-AVCENSUS`): stratum, n, PN, P(PN), plus the 0.9736
  headline, marked as a deterministic census with no interval.

### A5.4 — §7.2 update

The existing authorship-matched sentence ("An authorship-matched robustness slice ($n=36$;
one generator voice for every label) has since been measured on two lanes…") is updated to
the measured state including NS-5's fired branch — lane count corrected to three, the
Haiku direction stated per §A3's frozen sentence, the existing NS-1 and NS-2 clauses
preserved verbatim including the mini failure. No new decimals.

### A5.5 — untouchable in this pass

The **abstract** and the **conclusion** are [AUTHOR-1]-PASS-REQUIRED and are not edited; where
a one-clause upgrade would belong, a `%` comment is left and nothing else. **No slogan
change** — census data triggers nothing (D-R74-11 precedent). No registered verdict is
re-adjudicated: XV-1 stays failed, NS-2 stays split, D94's record stands. The concurrent
session's staged `FoK_working_draft_v0_5.tex` and dirty `e1_metamemory/NUMBERS.md` are not
touched.

### A5.6 — contradiction rule

If any result contradicts a frozen branch above, it is reported as its own cell with a new
D-entry under the D-E1R-5 / D-R74-1 / D-R74-11 precedent, and no interpretation is
improvised.

---

## Registration mechanics

One Table-15 (`tab:registrations`) row for this pass, added with this file's freeze-commit
hash after the freeze commit exists (the hash cannot cite itself); the Outcome cell starts
"pending" and is updated only per the frozen text above. Deviations ledger:
`iclr2027_monitoring_submission/DEVIATIONS_R74.md` (D-R74-12 records the R76 STOP and
rescope; D-R74-13 records the AV-CENSUS pre-freeze provenance).
