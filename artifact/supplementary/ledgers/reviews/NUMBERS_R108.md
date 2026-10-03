# NUMBERS_R108.md — deterministic values of the v15-to-v16 pass (R108, 2026-09-14)

Purpose. On the R103/R104/R107 precedent (`tools/trace_scan_v13.py` LEDGERS): values computed in this pass with no model call, each from a committed artifact named in its row. The amendment's own numbers (the retrieved view under the store's own marks; Haiku 4.5's lanes) are in `resp_review/NUMBERS_RESP.md` section 7.

## A. AUX-R108-GOLDSPLIT — the 174 licensed items split by whether the licensed record is among the five retrieved (`reviews/v16/tools/gold_in_view_split.py` → `reviews/v16/gold_in_view_split.json`)

PRESENT items answered under the policy, split by `stage1.json` `gold_in_view`; correct = the committed detector at the gold threshold (`AUX-DS-STAGE2`'s rule). Under retrieval alone the view is the same for every PRESENT item, so ORACLE's split equals ALWAYS's.

| policy (GPT-4.1 mini, the D.4 prompt) | licensed record in view: correct / n | rate | not in view: correct / n | rate | abstained |
|---|---|---:|---|---:|---:|
| **ALWAYS** (retrieval alone) | **37 / 65** | **0.5692** | **9 / 109** | **0.0826** | 0 |
| ORACLE | 37 / 65 | 0.5692 | 9 / 109 | 0.0826 | 0 |
| MODEL | 35 / 60 | 0.5833 | 9 / 95 | 0.0947 | 19 |
| LOOKUP | 33 / 56 | 0.5893 | 7 / 90 | 0.0778 | 28 |
| MODEL-ALL | 35 / 60 | 0.5833 | 9 / 95 | 0.0947 | 19 |
| LOOKUP-ALL | 33 / 56 | 0.5893 | 6 / 90 | 0.0667 | 28 |
| Haiku 4.5, ALWAYS (`AUX-DS-A2-STAGE2-H45` rows) | 38 / 65 | 0.5846 | 10 / 109 | 0.0917 | 0 |

Printed form (Section 8): "right for $37$ of the $65$ items whose licensed record is among the five and for $9$ of the $109$ whose record is not".

## B. AUX-R108-MECH-FR — Table 22's cells from the recorded bootstrap (`e1_metamemory/results/mechanism_scores.json`, `SECONDARY_frbank.arms[*].delta_vs_intact`, `bootstrap_vs_intact`; item-level, 1,000 draws)

| arm (FR-Bank hard tier, n = 307, intact 0.7003) | AUROC | Δ vs intact | item-level 95% | ECE |
|---|---:|---:|---|---:|
| A1 counts jittered | 0.7018 | +0.0015 | [−0.0310, +0.0366] | 0.1888 |
| A2 counts coarsened | 0.7015 | +0.0012 | [−0.0472, +0.0509] | 0.1813 |
| A3 names only | 0.7283 | +0.0279 | [−0.0231, +0.0801] | 0.0904 |

The pooled row's cells (Table 21) were already printed from the same file (`PRIMARY_pooled`); the FR-Bank endpoints were in the artifact and had not been printed.

## C. AUX-R108-TAGS — the store's own lifecycle marks on the five retrieved lines (from `resp_review/run/lock_amend1.json`, the amendment's $0 census)

Of the 3,305 rendered lines (661 views × 5), **1,273 change tag** between the ground-truth join and FR-Bank's own marks (565 of 661 views change at least one line). The store's non-active mark against the join's non-active flag: over lines tp 188, fp 1,201, fn 29, tn 1,887 (precision **0.1353**, recall **0.8664**); over the forbidding records in view (the 104 obligations' `pn_members` among the five): tp 47, fp 23, fn 13, tn 16 (precision **0.6714**, recall **0.7833**).

## D. AUX-R108-FACTORIAL — the monitoring-side factorial's main effects with intervals, recomputed from its recorded rows (`reviews/v16/tools/factorial_intervals.py` → `reviews/v16/factorial_intervals.json`; rows `e2_metamemory/m1_factorial_raw.json`, 661 items × 8 cells)

Reproduction before any interval: the eight cell AUROCs and the three main effects match `e2_metamemory/RESULTS_E2.md` §3.9 at four decimals (L +0.1980, W +0.0134, D −0.0193; the E1-configuration cell L1W1D1 0.7344). A main effect is the mean AUROC of the four cells with the factor on minus the mean of the four with it off. Intervals: item-level bootstrap (1,000 draws, seed 42, every cell rescored on the same draw) and persona-clustered.

| main effect | point | item-level 95% | persona-clustered 95% |
|---|---:|---|---|
| L, the lifecycle columns of the summary | **+0.1980** | [+0.1522, +0.2423] | [+0.1297, +0.2639] |
| W, the worked examples in the prompt | +0.0134 | [−0.0105, +0.0354] | [−0.0073, +0.0348] |
| D, the two-step detection in the prompt | −0.0193 | [−0.0451, +0.0034] | [−0.0396, +0.0011] |

Cells: L0W0D0 0.5636, L0W0D1 0.5181, L0W1D0 0.5735, L0W1D1 0.6132, L1W0D0 0.7958, L1W0D1 0.7602, L1W1D0 0.7702, L1W1D1 0.7344.
