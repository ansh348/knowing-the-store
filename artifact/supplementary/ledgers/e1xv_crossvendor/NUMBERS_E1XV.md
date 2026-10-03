# NUMBERS — E1-XV

Every figure here is produced by `tools/score_e1xv.py` into `results/e1xv_scores.json` and
re-derived by `tools/verify_e1xv.py` along an independent path. **Nothing in this file is typed
by hand from prose.**

**Scope note.** The brief said *"extend NUMBERS.md"*. The only `NUMBERS.md` in the repo is
`e1_metamemory/NUMBERS.md`, and this run's scope fence forbids touching E1 artifacts. The
E1-XV rows therefore land here, in this cell's own scope, as `NUMBERS_E2OP.md` did for E2-OP.

Cell: the matched FR-Bank 84 (30 ABSENT · 14 PRESENT · 40 PRESENT-NEGATIVE). FOK positive =
non-ABSENT (54). NOK positive = PRESENT-NEGATIVE (40). k=5, `MIN_DRAWS=3`, per-item mean over
surviving draws. Prereg `386d334`.

## Elicitation

| lane | rows | parse fail, blind | parse fail, indexed | truncated, indexed | excluded < MIN_DRAWS | $ |
|---|---|---|---|---|---|---|
| `claude-opus-5` | 840 | 0 (0.00%) | 0 (0.00%) | 0 | **0** | 5.2776 |
| `claude-haiku-4-5-20251001` | 840 | 0 (0.00%) | 0 (0.00%) | 366 | **0** | 0.6778 |
| `kimi-k3` | 840 | 1 (0.2381%) | 5 (1.1905%) | 6 | **0** | 13.6401 |

**No lane is flagged** — the registered threshold is >5% in any arm; the worst observed is
1.1905%. Zero API errors on 2,520 calls. Every row's `served_model` equals the model requested.

## The three-lineage table

| | `claude-opus-5` | `claude-haiku-4-5-20251001` | `kimi-k3` |
|---|---|---|---|
| **FOK** blind | 0.5855 | 0.3136 | 0.6651 |
| **FOK** indexed | **0.7068** | **0.7287** | **0.7222** |
| **FOK** delta | +0.1213 | +0.4151 | +0.0571 |
| **NOK** blind | **0.6994** | **0.3688** | 0.5983 |
| **NOK** indexed | **0.8523** | **0.8199** | **0.8588** |
| **NOK** delta | +0.1528 | +0.4511 | +0.2605 |

**95% CIs** — paper's committed bootstrap, 1,000 item-level resamples, seed 42, paired arms
moving together.

| lineage | judgment | blind CI | indexed CI | delta CI | delta excludes 0 |
|---|---|---|---|---|---|
| `claude-opus-5` | FOK | [0.4492, 0.7168] | [0.5692, 0.8222] | [+0.0047, +0.2449] | yes |
| `claude-opus-5` | NOK | [0.5712, 0.8135] | [0.7501, 0.9330] | [+0.0659, +0.2509] | yes |
| `claude-haiku-4-5-20251001` | FOK | [0.2051, 0.4383] | [0.6041, 0.8361] | [+0.2336, +0.5712] | yes |
| `claude-haiku-4-5-20251001` | NOK | [0.2571, 0.4789] | [0.7251, 0.9023] | [+0.3265, +0.5741] | yes |
| `kimi-k3` | FOK | [0.5326, 0.7912] | [0.5967, 0.8358] | [−0.0954, +0.2052] | **no** |
| `kimi-k3` | NOK | [0.4629, 0.7160] | [0.7636, 0.9307] | [+0.1456, +0.3866] | yes |

**No cell is tie-degenerate.** Distinct per-item values, blind / indexed: Opus 5 FOK 53/72,
NOK 76/68 · Haiku FOK 18/11, NOK 18/25 · K3 FOK 50/71, NOK 53/69. E1's ⚠ᵈ annotation on
`gpt-4.1-mini` has no counterpart here — every blind arm in this run is a measurement.

## Where the blind NOK CI sits relative to chance — the XV-1 gate

| lineage | blind NOK | 95% CI | position |
|---|---|---|---|
| `claude-opus-5` | 0.6994 | [0.5712, 0.8135] | **entirely ABOVE 0.50** |
| `claude-haiku-4-5-20251001` | 0.3688 | [0.2571, 0.4789] | **entirely BELOW 0.50** |
| `kimi-k3` | 0.5983 | [0.4629, 0.7160] | **includes 0.50** |

## Draw-stability (ruling 3) — descriptive, beside every AUROC

Per-item SD across surviving draws, and count of item-arm cells whose 5 draws are identical.

| lineage | judgment | arm | SD mean | SD median | SD max | identical / 84 |
|---|---|---|---|---|---|---|
| `claude-opus-5` | FOK | blind | 0.0366 | 0.0349 | 0.1071 | **0** |
| `claude-opus-5` | FOK | indexed | 0.0363 | 0.0303 | 0.1542 | **0** |
| `claude-opus-5` | NOK | blind | 0.0415 | 0.0361 | 0.1176 | **0** |
| `claude-opus-5` | NOK | indexed | 0.0364 | 0.0268 | 0.1854 | **0** |
| `claude-haiku-4-5-20251001` | FOK | blind | 0.0124 | 0.0 | 0.1807 | **62** |
| `claude-haiku-4-5-20251001` | FOK | indexed | 0.0045 | 0.0 | 0.1643 | **63** |
| `claude-haiku-4-5-20251001` | NOK | blind | 0.0191 | 0.0 | 0.2848 | **62** |
| `claude-haiku-4-5-20251001` | NOK | indexed | 0.0101 | 0.0 | 0.1521 | **63** |
| `kimi-k3` | FOK | blind | 0.0962 | 0.0922 | 0.2161 | **0** |
| `kimi-k3` | FOK | indexed | 0.0779 | 0.0653 | 0.2102 | **0** |
| `kimi-k3` | NOK | blind | 0.0581 | 0.0359 | 0.1759 | **0** |
| `kimi-k3` | NOK | indexed | 0.0613 | 0.0329 | 0.2460 | **0** |

**The lane that can pin `T=0` is the only one with reproducible draws.** Haiku 4.5 repeats
itself exactly on 62–63 of 84 cells; Opus 5 and K3, both without temperature pinning (D86),
repeat on **0 of 84** — 336 item-arm cells, not one identical. K3 carries the widest dispersion
of the three (FOK blind SD mean 0.0962, against 0.0366 for Opus 5 and 0.0124 for Haiku 4.5).

## Mean elicited values (calibration level, descriptive)

| lineage | FOK blind | FOK indexed | NOK blind | NOK indexed |
|---|---|---|---|---|
| `claude-opus-5` | 0.6186 | 0.6461 | 0.3541 | 0.3455 |
| `claude-haiku-4-5-20251001` | 0.3392 | 0.5775 | 0.1805 | 0.2056 |
| `kimi-k3` | 0.5 | 0.6457 | 0.167 | 0.3319 |

## Registered predictions

| | verdict | detail |
|---|---|---|
| **XV-1** | **FAILS** (2 of 3) | holds on `kimi-k3` only; fails **above** chance on Opus 5, **below** chance on Haiku 4.5 |
| **XV-2** | **HOLDS** (both frontier) | Opus 5 +0.1528 [+0.0659, +0.2509] · K3 +0.2605 [+0.1456, +0.3866] |
| **XV-3** | **HOLDS** | 0.5855 > 0.3136 |
| **XV-4** | **HOLDS** (all 3) | window [0.659, 0.7963]; observed 0.7068 · 0.7287 · 0.7222 |
| **XV-5** | **reports** | XV-1 held on `kimi-k3` |

**Paper pre-commitment: NOT met.** Under both readings — "both new lineages" (frontier subset)
and XV-1's own registered "every new model" — the gate is **False**, because XV-1 fails on
`claude-opus-5`. The limitations sentence stands.

## The OpenAI reference rows (`NUMBERS.md` §9, k=5, same cell)

| | `gpt-4.1-mini` | `gpt-5.6-luna` | `gpt-5.6-sol` |
|---|---|---|---|
| FOK blind / indexed | 0.4488 / 0.709 | 0.5735 / 0.7417 | 0.7099 / 0.7463 |
| NOK blind / indexed | 0.5 ⚠ᵈ / 0.7139 | 0.5585 / 0.8526 | 0.529 / 0.8588 |
| FOK delta | +0.2602 | +0.1682 | +0.0364 |
| NOK delta | +0.2139 | +0.294 | +0.3298 |

⚠ᵈ tie-degenerate, not a measurement (D23-E1); the annotation travels with the cell.

## Cross-vendor convergence — six models, three vendors, one cell

Computed by the scorer over this run's three lineages plus the three cited `NUMBERS.md` §9
reference rows; not derived by hand.

| | blind span | indexed span | tightening |
|---|---|---|---|
| **FOK** | 0.3963 | **0.0395** | **10.03×** |
| **NOK** | 0.3307 | 0.1449 | 2.28× |
| **NOK**, excluding `gpt-4.1-mini`'s tie-degenerate blind cell | 0.3307 | **0.0389** | **8.5×** |

**Indexed FOK, all six, sorted:** 0.7068 · 0.709 · 0.7222 · 0.7287 · 0.7417 · 0.7463.
**Indexed NOK, all six, sorted:** 0.7139 · 0.8199 · 0.8523 · 0.8526 · 0.8588 · 0.8588.
**Blind NOK, all six, sorted:** 0.3688 · 0.5 · 0.529 · 0.5585 · 0.5983 · 0.6994.

## Spend

| | |
|---|---|
| `claude-opus-5` | $5.2776 (registered line $5.03) |
| `claude-haiku-4-5-20251001` | $0.6778 (registered $0.7) |
| `kimi-k3` | $13.6401 (registered $16.29) |
| **elicitation total** | **$19.5955** (registered run total $22.02) |
| prior — STEP 0, pilots, batch verification | $1.122 |
| **grand total** | **$20.7175 of $28.0** |

## Verifier

`tools/verify_e1xv.py` — **92 independent rederivation checks, 0 failures**, plus a
figure-accounting pass over this file. AUROC is rederived by **brute-force pairwise
concordance** against the committed scorer's rank-sum form, and the per-item collapse is
rebuilt from the raw JSONL without importing the scorer.
