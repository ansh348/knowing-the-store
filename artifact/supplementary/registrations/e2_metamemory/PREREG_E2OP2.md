# PREREG — E2-OP2, the mechanism's predicted habitat

**FROZEN before any aggregate over control outcomes.** Everything below is derived from
**monitoring data only** — NOK scores and PN labels — plus a coverage check that counted rows
without reading a single judge verdict as an outcome. **No confabulation rate on the ungated
population has been computed.**

E2-OP found that NOK-targeted caution does not beat rate-matched random **on the population a
FOK gate hands downstream**, and named the reason: *gate-consumes-signal*. That finding makes a
prediction, and E2-OP2 tests it where it should hold — **with the gate removed**.

---

## 1. Feasibility — assembly-constructible, no gaps

| check | result |
|---|---|
| eval items | **529** |
| items with **both** an `S1-facts` and an `S2-facts-caution` row | **529 / 529** |
| judge verdicts resolving for those rows | **1,058 / 1,058** |
| items with a NOK monitoring score | **529 / 529** |
| **gaps** | **none** |

**The ungated policy never uses `S0-nofacts`**: with no FOK gate, every item is answered with
facts, and the only choice is whether the caution instruction is attached. Cost is **$0.00** —
this is a re-partition of rows already generated and already judged.

## 2. τ from monitoring data only — D40-E2's rule on the ungated population

**Rule (carried, not re-invented):** the lowest grid τ whose PN precision on the operative
population clears that population's base rate. **Ungated base rate = 82/529 = 0.1550.**

| τ | selected | precision | recall | Youden J | strict subset |
|---|---|---|---|---|---|
| 0.00 | 529 | 0.1550 | 1.0000 | 0.0000 | **no — selects everything** |
| **0.05** | **285** | **0.2000** | **0.6951** | **0.1851** | **yes** |
| 0.10 | 216 | 0.2130 | 0.5610 | 0.1807 | yes |
| 0.20 | 199 | 0.2261 | 0.5488 | **0.2043** | yes |
| 0.30 | 197 | 0.2234 | 0.5366 | 0.1943 | yes |
| 0.40 | 144 | 0.2222 | 0.3902 | 0.1397 | yes |
| 0.50 | 42 | 0.1905 | 0.0976 | 0.0215 | yes |
| 0.60 | 41 | 0.1951 | 0.0976 | 0.0237 | yes |
| 0.70 | 2 | 0.5000 | 0.0122 | 0.0100 | yes |

> **τ_OP2 = 0.05.** Selected **285 / 529**, instructed fraction **0.5388**, precision **0.2000**
> against a base rate of **0.1550**. Strict subset: yes. **Not degenerate**, so the run proceeds.

τ = 0.00 is excluded by the strict-subset requirement, not by preference: it instructs every
item and is definitionally identical to blanket caution.

**The contrast that motivates this cell, and it is visible before any outcome is seen:**

| | gated population (E2-OP) | **ungated population (here)** |
|---|---|---|
| base rate | 0.2044 | **0.1550** |
| precision range across the grid | 0.1905 – 0.2194 | **0.1905 – 0.2261** |
| margin over base at the chosen τ | +0.014 | **+0.045** |
| **max Youden J** | **0.0498** | **0.2043** |

**NOK discriminates PN about four times better once the gate is removed.** That is
gate-consumes-signal stated in its own terms, measured on monitoring rows, before any control
outcome enters.

## 3. Arms

| | policy | assembly |
|---|---|---|
| **(i)** | **ungated NOK-targeted** — `S2` iff `nok ≥ 0.05`, else `S1`, for all 529 | committed rows |
| **(ii)** | **rate-matched random** — 285 items drawn uniformly → `S2`, rest `S1`; **10,000 draws** | committed rows |
| **(iii)** | **blanket** — `S2` for all 529 | existing S2 aggregate |
| **(iv)** | **gated OP restated** — E2-OP's (vi-OP) and (vii-NOK), for the before/after contrast | already scored |

**Baseline for "benefit" in this family is `S1` for all 529** — facts, no caution — because with
no gate there is no `S0` arm. Blanket's benefit is `rate(S2 all) − rate(S1 all)`.

**10,000 draws, not 1,000 (D98).** E2-OP's permutation p carried a Monte Carlo SE of 0.0093 on a
28-valued endpoint with 6.09% tie mass. The draw count is raised so the reference is stable
against the claim, and **the permutation p ships with its Monte Carlo SE**, using the
Davison–Hinkley form `(n_le + 1) / (N + 1)`.

## 4. Registered predictions

**Endpoint: H-C2's exact endpoint** — confabulation rate over the 529 eval items, fixed
denominator. **Estimator:** the committed scorers, imported — `score_e2.adjusted` (OLS on
persona and coverage-label fixed effects, sum-to-zero, intercept is the estimate) and
`score_e2.boot_ci` (persona-clustered, 1,000 resamples, seed 42).

> ### H-OP2a — targeting beats rate-matched random, ungated
> **(i) − (ii)** on the H-C2 endpoint, adjusted, with the 95% CI **excluding 0**.

> ### H-OP2b — targeting retains at least half of blanket's benefit
> **(i) − S1-all ≤ 0.5 × ((iii) − S1-all)**.
> The instructed fraction is **0.5388**; E2-OP found random retention tracking the instructed
> fraction to within 0.0004, so that value is the null this bar is read against.

## 5. FAILS texts — frozen, gate and verdict only (D93)

> **H-OP2a FAILS.** The ungated targeted-minus-random CI does not exclude zero.

> **H-OP2b FAILS.** Ungated targeted caution does not retain half of blanket's benefit.

No mechanism clause, no downstream conclusion, no explanation. **What failed and nothing else.**

## 6. Paper-1 import criteria — frozen before any number

**Imported if and only if H-OP2a holds:** one figure and **≤150 words**.

**Figure:** four bars on the H-C2 endpoint — ungated targeted, ungated rate-matched random,
blanket — **with E2-OP's gated null beside them**, so the contrast the cell exists to show is in
the figure rather than the caption.

**Caption, drafted now:**

> *Targeting the caution instruction by the monitor's negative-obligation judgment reduces
> confabulation relative to instructing the same number of answers at random — but only where a
> retrieval gate has not already consumed the signal. On the gated population the same policy is
> indistinguishable from random (grey).*

**If H-OP2a FAILS: Paper 1 is untouched** — no figure, no words, no edit to §7.2 or §7.3 — and
the result reports in Paper 2 beside the gated null. The drafted caption stays in this prereg as
the record of what would have been claimed.

## 7. Scope and budget

**$0.00 projected** — every arm is a re-partition of committed, already-judged rows. Cap $2.
No frozen artifact edited. No paper text written in this run. Deviations continue at **D98**.

**Nothing has been assembled or scored. No control outcome on the ungated population has been
observed.**
