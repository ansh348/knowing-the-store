# PREREG — E2-OP, the NOK operating-point experiment (FROZEN)

**Frozen 2026-08-13, before any contact between thresholds and control outcomes.** No
aggregate over eval control outputs has been computed or observed. Everything below is fixed
from monitoring rows (`gates_eval.json`) and construction labels only.

**Question.** The missing run named in `E2_IMPORT_MEMO.md`: does **NOK-targeted** caution beat
**rate-matched random** caution, and does it retain blanket caution's benefit while instructing
only a subset?

**Substrate.** E2 eval split, n = 529, 32 personas. Retrieval artifact `78e9b39a…` immutable.
Answerer `gpt-5.4`. Judge `claude-sonnet-4-6`, unchanged. Gate draw **1** — the same draw
`run_answers.py:78` used to build the committed policies; not a choice made here.

---

## 0. Route — ASSEMBLY, verified not assumed

Every arm below is assembled from committed rows. **No new elicitation, no new judging, no new
API spend.** Verification in `E2OP_ROUTE.md` §1; headline: `answers_eval.json` holds
**529/529** items in each of `S0-nofacts`, `S1-facts`, `S2-facts-caution`, and **1587/1587**
answer rows resolve to a verdict in `cache/judgments_eval.json` under the committed
`item_id|response_sha[:24]` key. Zero gaps.

**Assembly is itself a scored computation and waits for the same go as any other scoring
step.**

## 1. τ selection rule — FROZEN

**Rule.** *τ is the lowest grid value whose precision for the PN label, on the operative
population, is at least that population's PN base rate.* Operative population = the **362
retrieved items** (`fok ≥ τ_FOK = 0.20`), because the caution instruction acts only where
retrieval happened; on non-retrieved items S0 is served and no instruction exists to target.

**Applied: τ_OP = 0.20.** Selects **197 of 362 retrieved items (54.4%)**; precision 0.218
against a base rate of 0.204.

**Precondition — PASSES on the letter.** The NOK draw-1 distribution is non-degenerate: 9
distinct values, 244 zeros and 285 non-zeros across 529 items; the selected fraction is
strictly between 0 and 1.

**Precondition — FAILS on the substance, and this is declared before any outcome is seen.**
NOK barely discriminates PN on the operative population at **any** threshold:

| τ | selected / 362 | precision | recall | Youden J |
|---|---|---|---|---|
| 0.05 | 265 | 0.200 | 0.716 | −0.020 |
| 0.10 | 214 | 0.206 | 0.595 | +0.004 |
| **0.20** | **197** | **0.218** | **0.581** | **+0.046** |
| 0.30 | 196 | 0.219 | 0.581 | +0.050 |
| 0.40 | 143 | 0.217 | 0.419 | +0.030 |
| 0.50 | 42 | **0.190** | 0.108 | −0.010 |
| 0.60 | 41 | 0.195 | 0.108 | −0.007 |

Base rate on the operative population is **0.204**. **No threshold clears it by more than
0.015, and Youden's J never exceeds +0.05.** The mechanism is legible: the FOK gate has
already enriched PN from 0.155 (all 529) to 0.204 (retrieved), consuming most of the signal
NOK would otherwise supply.

**Departure from the brief's default rule, logged as D40-E2.** The stated default —
τ matching the eval set's ground-truth PN prevalence (82/529 = 0.155) — lands at **τ = 0.5**
under either denominator, where precision is **0.190, below the 0.204 base rate**. That
operating point is anti-informative by construction: it would guarantee H-OP1's failure for a
reason unrelated to the hypothesis. The frozen rule above is monitoring-only, uses no control
outcome, is a derived threshold of the same family as E2's own τ_FOK derivation, and gives the
hypothesis its best legitimate operating point.

**Declared expectation, pre-number.** On this monitoring evidence **H-OP1 is expected to
fail.** That expectation is recorded now so a null reads as pre-declared rather than as
post-hoc rationalisation, and so a *pass* would be the surprising result it would deserve to
be.

## 2. Arms — three, two of them new

| arm | rule | source |
|---|---|---|
| **(vi-OP) targeted** | retrieve per FOK gate; caution **iff `nok ≥ 0.20`** | assembled: retrieved∧selected → S2, retrieved∧¬selected → S1, else S0 |
| **(vii-NOK) rate-matched random** | retrieve per FOK gate; caution on a **uniform random 197 of the 362** retrieved | assembled, **1,000 seeds** (seeds 0–999) |
| **(vi) blanket** | retrieve per FOK gate; caution on **all** retrieved | **existing committed result, reused unchanged** |

**Why 1,000 random draws and not the brief's ≥3.** The route is pure re-indexing of committed
rows, so draws are free. 1,000 seeds turn the comparator from three point estimates into a
**permutation reference distribution**, which is the correct null for "is this subset special"
and is strictly better inference at identical cost. Frozen here at 1,000.

**Nothing else changes.** Same gate, same retrieval, same answerer, same judge, same items.
The arms differ only in *which* retrieved items receive the frozen `CAUTION_INSTRUCTION`.

## 3. Hypotheses

**Primary H-OP1.** Targeted beats rate-matched random on **H-C2's exact endpoint** —
confabulation rate, covariate-adjusted paired comparison, persona-clustered bootstrap, 1,000
resamples, seed 42, unadjusted sensitivity alongside. **HOLDS iff the CI on
`confab(vi-OP) − confab(vii-NOK)` excludes 0 in the negative direction**, with (vii-NOK)
summarised as the mean over its 1,000 seeds and the permutation distribution reported.

**Secondary H-OP2.** Targeted retains **≥ half** of blanket's measured benefit while
instructing only 54.4% of what blanket instructs. **HOLDS iff
`confab(vi-OP) − confab(v) ≤ 0.5 × (confab(vi) − confab(v))`**, i.e. ≤ −0.0274 against
blanket's committed −0.0548 unadjusted.

**FAILS texts, written now, printed verbatim if they fire:**

> **H-OP1 FAILS.** Targeting the caution instruction by the NOK judgment does not beat
> instructing a random subset of the same size; the application-layer effect is induced
> caution, not lifecycle content, and Paper 1's §7.2 stands as written.

> **H-OP2 FAILS.** Targeted caution does not retain half of blanket caution's benefit; the
> benefit scales with how many answers carry the instruction, not with which ones.

## 4. Import criteria — pre-committed, no middle outcome

- **If H-OP1 HOLDS:** Paper 1 imports **one figure** (targeted / random / blanket) **+ ≤150
  words**. Caption drafted now, to be used as written:

  > **Targeted caution beats matched-rate random caution.** Applying the caution instruction
  > only where the NOK judgment fires (τ = 0.20, 197 of 362 retrieved answers) reduces
  > confabulation by *[X]*pp relative to instructing a uniformly random subset of the same
  > size (95% CI *[L, U]*, 1,000 random draws), and retains *[Y]*% of the benefit of
  > instructing every retrieved answer.

- **If H-OP1 FAILS:** **Paper 1 is untouched.** No figure, no words, no edit to §7.2 or §7.3.
  The result reports in **Paper 2** as the caution-mechanism finding.

**No middle outcome exists.** H-OP2 does not license an import on its own.

## 5. Hygiene

- No aggregate over eval control outputs observed before the scoring step. **None has been
  observed as of this freeze.**
- τ was derived from monitoring rows and construction labels only; it has touched **no**
  control outcome.
- Assembly is a scored computation and waits for the go.
- Judge frozen, cache keyed as committed. No re-judging.
- **Scope fence:** no E1/E1-B artifacts touched; no judge changes; no policies beyond the two
  new arms; no Paper 1 or Paper 2 prose in this run.

## 6. Cap

Sub-cap **$12** inside E2's $25 absolute. **Projected spend: $0.00** — the route is assembly.
E2 has spent $5.81 of $25; this run is expected to leave that unchanged.

---

**FROZEN.** Any change from here is a numbered deviation logged before first use.
