# NUMBERS — E2-OP

Every figure here is produced by `tools/score_e2op.py` into `results/e2op_scores.json` and
re-derived by `tools/verify_e2op.py` along an independent path. **Nothing in this file is
typed by hand from prose.**

**Scope note.** The brief said *"extend NUMBERS.md"*. The only `NUMBERS.md` in the repo is
`e1_metamemory/NUMBERS.md`, and this run's scope fence forbids touching E1 artifacts. The
E2-OP rows therefore land here, in E2's own scope, rather than in E1's numbers file.

**Route: assembly. 0 API calls, $0.00.** E2 remains at $5.81 of $25; the $12 sub-cap is
untouched.

## Assembly fidelity — the route validates against the committed policy table

| quantity | assembled | committed (`RESULTS_E2.md` §3.1) |
|---|---|---|
| eval items | 529 | 529 |
| (v) confabulation count | 149 | 149 |
| (vi) confabulation count | 120 | 120 |
| (v) retrieval rate | 0.6843 | 0.684 |

**PASS.** The assembly reproduces the committed policy table exactly, which is what licenses
every row below.

## Cells

| quantity | value |
|---|---|
| retrieved (`fok ≥ 0.20`) | 362 |
| selected (`nok ≥ τ_OP = 0.20`) | 197 |
| selected fraction of retrieved | 0.5442 |

## Confabulation rates, eval split, fixed denominator 529

| arm | confabulation |
|---|---|
| (v) gate only | 0.2817 |
| (vi) blanket caution | 0.2268 |
| **(vi-OP) NOK-targeted** | **0.259** |
| (vii-NOK) rate-matched random, mean of 1,000 seeds | 0.2519 |
| (vii-NOK) sd across seeds | 0.00622 |
| (vii-NOK) min / max across seeds | 0.2325 / 0.2684 |

## H-OP1 — targeted vs rate-matched random, H-C2's exact endpoint

| quantity | value |
|---|---|
| adjusted | +0.00929 |
| unadjusted | +0.00713 |
| 95% CI | [−0.00702, +0.02477] |
| analytic cross-check of the random arm | +0.0094 |
| permutation p, one-sided | 0.8931 |
| random draws at or below the targeted rate | 893 of 1000 |
| **verdict** | **FAILS** |

CI includes zero, and the point estimate is **positive** — targeted confabulates slightly
*more* than random at the same instruction volume.

## H-OP2 — does targeted retain ≥ half of blanket's benefit?

| quantity | value |
|---|---|
| targeted − (v), adjusted | −0.02209 |
| targeted − (v), unadjusted | −0.02268 |
| 95% CI | [−0.04358, −0.00305] |
| blanket − (v), unadjusted | −0.05482 |
| half of blanket (the bar) | −0.02741 |
| **retention, targeted** | **0.4138** |
| retention, rate-matched random | 0.5438 |
| instructed fraction of blanket | 0.5442 |
| **verdict** | **FAILS** |

**Random retention (0.5438) tracks the instructed fraction (0.5442) almost exactly.** Benefit
scales with how many answers carry the instruction. Targeted retention (0.4138) falls *below*
that line.

## τ derivation — reproduces `PREREG_E2OP.md` §1

Monitoring rows and construction labels only; no control outcome enters.

| quantity | value |
|---|---|
| PN base rate, all 529 items | 0.155 |
| PN base rate, 362 retrieved | 0.2044 |
| max Youden J over the grid | 0.0498 |

| τ | selected | precision | recall | Youden J |
|---|---|---|---|---|
| 0.0 | 362 | 0.2044 | 1.0 | 0.0 |
| 0.05 | 265 | 0.2 | 0.7162 | −0.0199 |
| 0.1 | 214 | 0.2056 | 0.5946 | 0.0043 |
| **0.2** | **197** | **0.2183** | **0.5811** | **0.0464** |
| 0.3 | 196 | 0.2194 | 0.5811 | 0.0498 |
| 0.4 | 143 | 0.2168 | 0.4189 | 0.03 |
| 0.5 | 42 | 0.1905 | 0.1081 | −0.0099 |
| 0.6 | 41 | 0.1951 | 0.1081 | −0.0065 |
| 0.7 | 2 | 0.5 | 0.0135 | 0.01 |

Precision spans **0.1905–0.2194** on every cell with usable n against a base rate of
**0.2044**. The τ = 0.7 cell reads 0.5 on **two items** and is noise, not signal.

## Verifier

`tools/verify_e2op.py` — 14 independent rederivation checks, **0 failures**, plus a
figure-accounting pass over this file.
