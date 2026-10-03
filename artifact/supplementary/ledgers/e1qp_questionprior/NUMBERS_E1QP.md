# NUMBERS — E1-QP

Every figure is produced by `tools/probes.py` and `tools/score_e1qp.py` into
`results/e1qp_scores.json` and re-derived by `tools/verify_e1qp.py`. **Nothing here is typed by
hand from prose.**

**Scope note.** The brief said *"NUMBERS.md rows"*. The only `NUMBERS.md` is
`e1_metamemory/NUMBERS.md`, which this run's fence forbids editing, so the rows land here — as
they did for E2-OP and E1-XV. Prereg `f4dafdd1…`. **No store contact: every probe input is a
question string; every model number is recomputed from committed rows.**

## Populations

| | n | composition |
|---|---|---|
| **P1** — matched FR-Bank 84 cell | 84 | 30 ABSENT · 14 PRESENT · 40 PN |
| **P2** — FR-Bank hard row with a question string | 307 | 272 ABSENT · 35 PN |

P2 excludes 39 UNRESOLVED hard items that carry no question string. On P2 the only non-ABSENT
label is PN, so **PN-vs-rest and non-ABSENT-vs-ABSENT are the same partition** and are reported
once.

## (a)(i) TF-IDF + logistic regression, question strings only, persona-grouped CV

| probe | n | pos | AUROC | 95% CI | includes 0.50 |
|---|---|---|---|---|---|
| P1 full · PN-vs-rest | 84 | 40 | **0.7972** | [0.6949, 0.8927] | no |
| P1 full · non-ABSENT-vs-ABSENT | 84 | 54 | 0.7176 | [0.585, 0.8393] | no |
| P1 matched · PN-vs-slot-ablated | 49 | 40 | 0.4944 | [0.1777, 0.7874] | yes |
| P1 strict slot-ablated | 21 | 12 | 0.8565 | [0.5874, 1.0] | no |
| **P2 full · PN-vs-rest** | 307 | 35 | **0.9199** | [0.8869, 0.9472] | no |
| **P2 matched · PN-vs-slot-ablated** | 162 | 35 | **0.8436** | [0.7813, 0.899] | **no** |

## (a)(ii) LLM text-only classifier — `gpt-4.1-mini`, zero-shot, frozen minimal prompt

| probe | n | pos | AUROC | 95% CI | includes 0.50 |
|---|---|---|---|---|---|
| P1 full · `y_nok` | 84 | 40 | **0.4804** | [0.3587, 0.5935] | **yes** |
| P1 full · `y_fok` | 84 | 54 | 0.546 | [0.4037, 0.6736] | yes |
| P1 matched | 49 | 40 | 0.2514 | [0.102, 0.4269] | no |
| P2 full · `y_nok` | 307 | 35 | **0.6283** | [0.5583, 0.6942] | no |
| P2 matched | 162 | 35 | 0.3749 | [0.2814, 0.4651] | no |

**362 calls, $0.0237** against a $2 cap. 0 unparsed.

## Ceilings

| population | TF-IDF (supervised) | LLM (zero-shot) | **CEILING** | source |
|---|---|---|---|---|
| **P1** | 0.7972 | 0.4804 | **0.7972** | TF-IDF |
| **P2** | 0.9199 | 0.6283 | **0.9199** | TF-IDF |

## QP-1 — blind NOK on P1 against CEILING(P1) = 0.7972

| lineage | blind NOK | under ceiling | verdict |
|---|---|---|---|
| `gpt-4.1-mini` | 0.5 ⚠ᵈ | yes | HOLDS |
| `gpt-5.6-luna` | 0.5585 | yes | HOLDS |
| `gpt-5.6-sol` | 0.529 | yes | HOLDS |
| **`claude-opus-5`** | **0.6994** | **yes** | **HOLDS** |
| `claude-haiku-4-5-20251001` | 0.3688 | yes | HOLDS |
| `kimi-k3` | 0.5983 | yes | HOLDS |

**QP-1 HOLDS on all six.** Against the *zero-shot* ceiling (0.4804) rather than the supervised
one, four of six sit above it — see `RESULTS_E1QP.md`.

## QP-2 — neutralisation check

| population | n | AUROC | 95% CI | includes 0.50 | verdict |
|---|---|---|---|---|---|
| P1 matched | 49 | 0.4944 | [0.1777, 0.7874] | yes | holds, but 9 negatives |
| **P2 matched (powered)** | **162** | **0.8436** | **[0.7813, 0.899]** | **no** | **FAILS** |

**QP-2 FAILS on the powered population.**

## (b) Matched contrast — blind and indexed NOK

**Coverage.** Only `gpt-4.1-mini` has committed rows across the P2 matched slice (162/162).
The other five cover **21/162** — the intersection with the 84-item cell. Their P2 rows are
that 21-item subset and are **not** comparable in power to mini's.

| lineage | slice | n | blind | blind CI | inc 0.50 | indexed | indexed CI | inc 0.50 | delta | excl 0 |
|---|---|---|---|---|---|---|---|---|---|---|
| `gpt-4.1-mini` | P1 matched | 49 | 0.5 | [0.5, 0.5] | yes | 0.6319 | [0.4767, 0.7636] | yes | +0.1319 | no |
| **`gpt-4.1-mini`** | **P2 matched** | **162** | **0.4921** | [0.4797, 0.5] | yes | **0.7263** | [0.6168, 0.8376] | **no** | **+0.2342** | **yes** |
| `gpt-5.6-luna` | P1 matched | 49 | 0.5833 | [0.3178, 0.8324] | yes | 0.7069 | [0.4951, 0.8861] | yes | +0.1236 | no |
| `gpt-5.6-sol` | P1 matched | 49 | 0.5139 | [0.2832, 0.7359] | yes | 0.7444 | [0.4999, 0.9558] | yes | +0.2306 | yes |
| `claude-opus-5` | P1 matched | 49 | 0.6736 | [0.3665, 0.9231] | yes | 0.75 | [0.4882, 0.9639] | yes | +0.0764 | no |
| `claude-haiku-4-5-20251001` | P1 matched | 49 | 0.3306 | [0.1479, 0.5184] | yes | 0.6833 | [0.4845, 0.8566] | yes | +0.3528 | yes |
| `kimi-k3` | P1 matched | 49 | 0.5542 | [0.2888, 0.8004] | yes | 0.7694 | [0.5666, 0.9436] | no | +0.2153 | yes |

**Degeneracy in the powered cell.** `gpt-4.1-mini`'s blind NOK on the P2 matched slice takes
**2 distinct values**, with a modal share of **0.9877** — 0.0 on 160 of 162 items. Its indexed
arm takes 7. **`blind_near_degenerate` = true.**

## QP-3 — index effect on the matched slice

**HOLDS mechanically** on `gpt-4.1-mini` / P2 matched: blind CI includes 0.50, indexed CI
excludes it, delta +0.2342 with CI excluding 0. **Carried with its caveat:** the gate is
satisfied by a blind arm that barely varies, not by a varying arm that fails to discriminate.

## (c) Blind NOK residualised against the probe scores — descriptive

Linear partialling of the out-of-fold TF-IDF prediction and the LLM likelihood out of each
model's per-item blind NOK, on P1.

| lineage | raw blind | residual | residual CI | includes 0.50 |
|---|---|---|---|---|
| `gpt-4.1-mini` | 0.5 | 0.5 | [0.5, 0.5] | yes |
| `gpt-5.6-luna` | 0.5585 | 0.708 | [0.5842, 0.8148] | no |
| `gpt-5.6-sol` | 0.529 | 0.529 | [0.3993, 0.6547] | yes |
| **`claude-opus-5`** | **0.6994** | **0.6687** | [0.54, 0.7789] | **no** |
| `claude-haiku-4-5-20251001` | 0.3688 | 0.5847 | [0.4485, 0.7075] | yes |
| `kimi-k3` | 0.5983 | 0.6193 | [0.4875, 0.7347] | yes |

## (c) E1-XV restated beside the ceiling

| lineage | blind NOK | NOK delta | CEILING(P1) |
|---|---|---|---|
| `gpt-4.1-mini` | 0.5 ⚠ᵈ | +0.2139 | 0.7972 |
| `gpt-5.6-luna` | 0.5585 | +0.294 | 0.7972 |
| `gpt-5.6-sol` | 0.529 | +0.3298 | 0.7972 |
| `claude-opus-5` | 0.6994 | +0.1528 | 0.7972 |
| `claude-haiku-4-5-20251001` | 0.3688 | +0.4511 | 0.7972 |
| `kimi-k3` | 0.5983 | +0.2605 | 0.7972 |

## Spend

**$0.0237**, LLM classifier arm only, against a **$2** cap. Everything else is local or a
recompute over committed rows.
