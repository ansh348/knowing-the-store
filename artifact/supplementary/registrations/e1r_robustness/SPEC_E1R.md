# E1-R: frozen analysis specification for the $0 robustness pass

**Frozen: 2026-08-15, before any number in this pass was computed.**

## What freezing does and does not buy here

This is **not a preregistration**. The monitoring data already exist, and the item-level
results are already published in v0.9. Freezing this document before computation buys exactly
one thing: the interpretation rules, contingency readings, and STOP conditions below were
written without knowledge of the numbers they will be applied to, so the reading of each
result cannot be selected after seeing it. It does not buy the inferential protection of a
true preregistration, and no sentence in the manuscript may claim that it does.

Every computation specified here is offline and costs $0. No inference API is called. Where a
requested analysis cannot be run at $0, this document says so and the pass reports
`NOT MEASURABLE WITHOUT A RUN` with a projected cost rather than substituting something else
silently.

Reviewer items addressed: **B2** (clustered statistics), **B1** (non-LLM baselines),
**B4** (BELIEVED-index NOK), **B5** and **A4** (calibration intervals and reliability).

## Common definitions

| Term | Frozen definition |
|---|---|
| Cluster unit | `persona`, parsed from `item_id` of the form `backend:persona:question_id:variant`. 40 personas in the E1 populations; 33 in the 84-item cross-vendor cell. |
| AUROC | Mann–Whitney rank statistic with ties contributing 0.5, exactly as `e1_metamemory/tools/score_e1.py`. |
| ECE | 10 equal-width bins, bin gap weighted by bin mass, exactly as `score_e1.py`. |
| Primary estimate | Unchanged. The preregistered item-level point estimate and its item-level bootstrap CI remain the paper's primary endpoint everywhere. |
| Sensitivity | Everything in this document enters as a **registered sensitivity**, reported beside the primary, never replacing it. |
| Seed | 42 throughout, matching the preregistered scorer. |
| Draws | 1,000 throughout, matching the preregistered scorer. |

**Populations.** All analyses use the same populations as the published monitor rows, joined
by the same keys the committed scorer uses (`blind` by question text, indexed arms by
`item_id`):

| Row ID | Population | n | Published Δ | Published item-level CI |
|---|---|---:|---:|---|
| R-FOK-HARD | pooled hard tier, indexed-TRUE | 588 | +0.2272 | [+0.1177, +0.3504] |
| R-FOK-FRB | FR-Bank hard tier, indexed-TRUE | 307 | +0.2037 | [+0.0935, +0.3191] |
| R-NOK-FRB | FR-Bank, NOK, indexed-TRUE | 661 | +0.2393 | [+0.1801, +0.2949] |
| R-FOK-MEM0 | Mem0, indexed-TRUE | 238 | −0.0969 | [−0.169, −0.025] |
| R-FOK-AMEM | A-MEM, indexed-TRUE | 284 | −0.1065 | [−0.173, −0.040] |
| R-FOK-EASY | easy contrast, indexed-TRUE | 595 | +0.1914 | none published |
| R-LADDER-* | luna, sol × FOK, NOK on the 84-item matched cell | 84 | as Table 4 | as Table 4 |
| R-XV-* | Opus 5, Haiku 4.5, K3 × FOK, NOK on the same cell | 84 | as Table 4 | as Table 4 |

`mini` ladder rows are computed but flagged: mini blind NOK is constant at 0.0 across all 84
items, so its AUROC is an all-tie artifact and no clustered interval is interpretable. This
flag is carried into every output row rather than applied afterwards.

---

## (a) Persona-clustered bootstrap and leave-one-persona-out

### Frozen procedure

**Clustered bootstrap.** Draw `n_personas` personas with replacement. The resampled item
multiset is the concatenation of all items belonging to the drawn personas, so cluster size
enters the resample naturally and the total item count varies between draws. Both arms move
together on the identical drawn multiset, preserving pairing. Draws whose resampled label
vector is single-class are discarded, matching the preregistered rule. The interval is the
2.5th and 97.5th percentile of the retained delta distribution. The point estimate is **not**
recomputed — it remains the full-sample item-level delta.

**Leave-one-persona-out.** For each persona `p`, drop every item with `persona == p` and
recompute the delta on the remainder. Report the minimum, maximum, and the number of folds in
which the delta changes sign relative to the full-sample delta. LOPO is a fragility
diagnostic, not an interval.

### Pre-derived expectation

Under the standard design-effect approximation `DEFF ≈ 1 + (m̄ − 1)·ρ`, the interval width
scales by `√DEFF`. Setting the widened half-width equal to the point estimate gives the
intracluster correlation `ρ*` at which each row's CI would first touch zero:

| Row | m̄ | half-width | width multiple to reach 0 | implied DEFF | **ρ\*** | pre-derived verdict |
|---|---:|---:|---:|---:|---:|---|
| R-FOK-HARD | 14.7 | 0.1163 | 1.95 | 3.81 | **0.205** | at genuine risk |
| R-FOK-FRB | 7.7 | 0.1128 | 1.81 | 3.26 | **0.339** | at moderate risk |
| R-NOK-FRB | 16.5 | 0.0574 | 4.17 | 17.38 | **1.055** | **cannot** cross zero: ρ ≤ 1 by definition |
| R-FOK-MEM0 | 6.0 | 0.0720 | 1.35 | 1.81 | **0.164** | at genuine risk |
| R-FOK-AMEM | 7.1 | 0.0665 | 1.60 | 2.56 | **0.257** | at moderate risk |

This is recorded as a stated prior so the observed result can be judged against an
expectation formed before computation. Two caveats are frozen with it: the DEFF formula
governs means rather than rank-statistic differences, and it is therefore an approximation
here; and for a two-sample rank statistic the binding quantity is the number of
**positive-bearing** clusters, not the number of clusters. On R-FOK-HARD the 35 positives sit
in only **23 of 40** personas at 1–3 each, so the positive-side standard error inflates by at
least `√(35/23) ≈ 1.23` from cluster counting alone, before any within-persona correlation.
The R-NOK-FRB row's 104 positives sit in 28 of 40 personas.

### STOP condition

For any row whose published item-level CI excludes zero, if the persona-clustered CI
**includes** zero, computation halts at the end of this sub-step and the result is reported to
the principal investigator **before any manuscript sentence is edited**. Prose does not move
ahead of a failed row.

### Frozen contingency readings

Written before the numbers are seen; exactly one branch is selected per row by the observed
result.

- **Clustered CI excludes zero.** Reading: the effect is not an artifact of within-persona
  correlation. The preregistered item-level interval is retained as primary; the clustered
  interval is reported as a registered sensitivity in one appendix table with one sentence
  beside the headline.
- **Clustered CI includes zero.** Reading: the item-level interval overstates precision for
  that row because items are not independent within a persona. The row's claim is restated as
  directional, the clustered interval is printed beside it, and B2 is dispositioned as a
  **conceded** item rather than a rebutted one. No row in this state may keep a sentence that
  asserts a demonstrated effect.
- **LOPO sign change in ≥ 1 fold.** Reading: the row depends materially on a single persona,
  and the manuscript must name that dependence wherever the row is used, regardless of what
  the clustered interval does.

---

## (b) Non-LLM baselines over the same committed serialized indexes

### Why this is the sharpest item in the review set

B1 asks whether the paper measures "LLM metamemory" or merely "metadata makes classification
easier." That question is answerable only by running non-LLM readers over the **identical**
serialized index strings the monitor saw. Those strings are committed in
`e1_metamemory/indexes_v2.json`, keyed `backend:persona:variant:{TRUE,BELIEVED}`, so the
comparison is exact rather than approximate.

### Frozen baselines

All five read only the serialized index text and the question. None receives the item's
category, label, tier, or any ground-truth field.

| ID | Baseline | Definition |
|---|---|---|
| **NB-1** | Deterministic lifecycle rule | Parse the index into per-category ENTRIES/ACTIVE/SUPRSD/RETRACT/EXPIRED counts, supersession-event totals, and attribute-name lists. Assign the question to a category by maximum content-token overlap with that category's attribute names; ties break to the higher-ENTRIES category. FOK score = assigned-category ENTRIES ÷ store max category ENTRIES. NOK score = (assigned SUPRSD + RETRACT + EXPIRED) ÷ max(1, assigned ENTRIES). Where a backend marks the per-category breakdown "not expressible", fall back to store-total entries, which is constant within a store. |
| **NB-2** | Logistic over index features | Numeric features only: store totals, category count, lifecycle totals, supersession events, assigned-category counts, token-overlap statistics, matched-attribute count, whether the top matched attribute appears in the superseded-content list, and recency-band counts. `sklearn` LogisticRegression, L2, C=1.0, `max_iter=2000`, standardized. |
| **NB-3** | TF–IDF over index text | Word 1–2 grams, `min_df=2`, over the serialized index concatenated with the question; same classifier as NB-2. |
| **NB-4** | Lexical query↔index match | Unsupervised. Score = maximum content-token Jaccard between the question and each attribute name exposed by the index. |
| **NB-5** | Embedding query↔index match | Unsupervised. Encoder `sentence-transformers/all-MiniLM-L6-v2` from the local HuggingFace cache — no network, $0. Score = maximum cosine similarity between the question and each attribute-name string. |

**Supervised-baseline evaluation is persona-grouped.** NB-2 and NB-3 are label-supervised, so
they are scored by `GroupKFold(n_splits=5)` on persona with out-of-fold predictions pooled
before a single AUROC is computed. Fitting and scoring on the same personas would leak and is
prohibited. NB-1, NB-4, and NB-5 are unsupervised and are scored directly.

**Disclosed deviation.** NB-5 uses a local open-weights encoder, not the OpenAI embedder used
by the two-channel presence control. The two numbers are therefore not interchangeable, and
the manuscript must not present NB-5 as the presence control's embedding channel.

**Arms.** Every baseline is run on both the **TRUE** and the **BELIEVED** index for every
population, so the oracle-versus-self-reported contrast B4 raises is available for the
baselines as well as for the monitor.

### Frozen contingency readings

The first of these was dictated in the pass instruction and is reproduced verbatim in intent;
the remainder are frozen here so that no branch is chosen after the fact.

- **Rule matches the LLM on TRUE but collapses on BELIEVED.** Reading: *rules read oracle
  metadata; judgment survives corruption.* The contribution is the monitor's robustness to a
  store's own corrupted self-description, and the manuscript says exactly that.
- **A baseline matches or beats the monitor on BOTH TRUE and BELIEVED.** Reading: the paper's
  contribution is the measurement construct and the index design, not an LLM-specific
  capability. The manuscript must state this explicitly, narrow "metamemory" to a
  monitoring-judgment framing wherever the baseline dominates, and disposition B1 as
  **conceded**. This branch is to be reported even though it is the costly one.
- **Baselines fall clearly below the monitor on both arms.** Reading: the monitor adds
  information beyond mechanical index features; the headline is reported in its
  baseline-controlled form with the baselines printed beside it.
- **Baselines beat the monitor on FOK but not NOK.** Reading: NOK is where the monitor
  contributes, and the FOK headline is re-scoped accordingly in both the abstract and §4.

A baseline "matches" the monitor when the two AUROCs differ by less than the ±0.05 tolerance
already frozen for the count-destruction probe. That tolerance is inherited deliberately so
this pass does not invent a second, more convenient threshold.

---

## (c) BELIEVED-index NOK

### Inventory result (census, not a scored outcome)

`e1_metamemory/elicitation_main.json` contains **1,183 `INDEXED-BELIEVED` rows, all status
`OK`**, covering the full scoreable population. Restricted to the FR-Bank NOK population,
**661 of 661** items join to a BELIEVED row with a non-null `nok` value on both arms.

**The 661-row NOK population is fully covered. The answer is YES, and the result is
computable offline at $0.** B4 named this result CENTRAL and believed it missing; it was never
missing from the data, only from the scorer, which calls `row(..., judgment="nok")` on the
TRUE index alone while computing BELIEVED rows for FOK only.

### Frozen procedure

Compute `row(frbank_items, blind, idxBELIEVED, judgment="nok")` with the committed scorer's
own function, then retention `= believed_delta ÷ true_delta`, matching the definition already
used for FOK in `H_BELIEVED`. Report beside the published FOK retention figure of 101.4%.

### Frozen contingency readings

- **Retention ≥ 60% and delta CI excludes zero.** Reading: NOK survives the store's own
  corrupted self-description. The 60% threshold is inherited from the scorer's existing
  `holds_ge_60pct` gate rather than chosen now.
- **Retention < 60% and delta CI excludes zero.** Reading: NOK degrades materially under
  believed metadata but remains positive; the manuscript reports the degradation as a
  quantified limit on the practical claim.
- **Delta CI includes zero.** Reading: NOK is not demonstrated on believed indexes. The
  oracle-index dependence B4 names is **confirmed**, and it is stated in the limitations and
  the abstract, not buried in an appendix.

---

## (d) ECE intervals and reliability diagrams

### Frozen procedure

Rows: the five calibration arms already printed in the count-destruction table — blind,
intact index, counts jittered, counts coarsened, and names only — each on the pooled hard
tier, n = 588.

For each arm: ECE by the committed 10-bin estimator; a 1,000-draw item-level bootstrap at
seed 42 giving a percentile interval; the same bootstrap under persona clustering, for
consistency with sub-step (a); and the paired difference against the blind arm with its own
interval. Reliability diagrams use the same 10 equal-width bins, plotting bin mean predicted
probability against bin observed frequency with bin masses shown, rendered to PDF and PNG for
the appendix.

### Frozen contingency readings

- **Blind−intact ECE difference CI includes zero.** Reading: the intact index leaves
  calibration statistically unchanged. The manuscript's existing word "unimproved" is then
  exactly right and stays; it may not be upgraded to "worse".
- **Blind−intact ECE difference CI excludes zero with intact worse.** Reading: the index
  measurably degrades calibration while improving discrimination, which is reported as a
  genuine cost of the method rather than a neutral negative result.
- **Reliability diagrams show monotone but poorly-scaled curves.** Reading: the monitor
  outputs a ranking signal rather than a calibrated probability. A4 and B5 are then
  **conceded**, and the manuscript's use of the word "probability" is narrowed wherever it
  describes an elicited output rather than a defined target.

---

## Outputs and gating

All figures produced under this specification are written to `e1r_robustness/results/`,
transcribed into `e1r_robustness/NUMBERS_E1R.md`, and keyed into a new section of the central
`e1_metamemory/NUMBERS.md`. A two-direction verifier, `e1r_robustness/tools/verify_e1r.py`,
must pass — every ledger figure re-derived from artifacts, and every ledger numeral accounted
for — **before any manuscript sentence uses any of these numbers**. That gate is absolute and
applies even to numbers that confirm the existing text.
