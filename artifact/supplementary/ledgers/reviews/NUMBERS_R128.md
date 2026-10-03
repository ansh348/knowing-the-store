# NUMBERS_R128.md: the pass ledger of programs R127, R127b and R128 (2026-09-20)

Written by `reviews/v22/tools/ledger_r128.py` from the artifacts named in each section; no number is typed by hand.

## AUX-R128-DS-DENOM — tab:ds-body with both denominators (the counts are tab:ds's; Wilson score intervals, z = 1.96; the answered-subset intervals reproduce the printed ones)

| policy | reached scorable (sup. + ret. in view) | answered scorable (answered minus expiry answered) | abstained | stale | rate over reached (Wilson) | rate over answered (Wilson) |
|---|---:|---:|---:|---:|---|---|
| Top-5 retrieval | 42 | 42 | 0 | 8 | 0.1905 [0.100, 0.333] | 0.1905 [0.100, 0.333] |
| Model rule | 73 | 62 | 11 | 8 | 0.1096 [0.057, 0.202] | 0.1290 [0.067, 0.234] |
| Lookup rule | 73 | 58 | 15 | 6 | 0.0822 [0.038, 0.168] | 0.1034 [0.048, 0.208] |
| Model rule, all states named and scored | 76 | 65 | 11 | 11 | 0.1447 [0.083, 0.241] | 0.1692 [0.097, 0.278] |
| Literal lookup rule (descriptive) | 82 | 82 | 0 | 13 | 0.1585 [0.095, 0.253] | 0.1585 [0.095, 0.253] |
| Oracle | 85 | 85 | 0 | 16 | 0.1882 [0.119, 0.284] | 0.1882 [0.119, 0.284] |

The Wilson interval tab:ds-body-lower lacked, the model rule with all states named and scored, 11 of 65: [0.097, 0.278] (printed at two decimals in tab:ds-body as [0.10,0.28]).

## AUX-R128-CF3-DRAW1 — Opus 5's expiry rows at draw 1 on every pair (`reviews/v22/results/r128_cf3_draw1.json`; the recorded pooled row reproduced first)

| reading | summary | AUROC | persona CI | delta vs blind | item interval | persona interval |
|---|---|---:|---|---:|---|---|
| pooled, recorded (k = 5 on the 30, k = 1 on the 14) | sup. only | 0.5914 | [0.5303, 0.6593] | +0.0914 | [-0.0061, +0.1930] | [+0.0303, +0.1593] |
| pooled, recorded (k = 5 on the 30, k = 1 on the 14) | all three | 0.9232 | [0.8769, 0.9654] | +0.4232 | [+0.3246, +0.5218] | [+0.3769, +0.4654] |
| pooled, recorded (k = 5 on the 30, k = 1 on the 14) | totals rand. | 0.6068 | [0.5587, 0.6779] | +0.1068 | [+0.0115, +0.1974] | [+0.0587, +0.1779] |
| pooled, draw 1 on every pair | sup. only | 0.5917 | [0.5281, 0.6615] | +0.0917 | [-0.0053, +0.1869] | [+0.0281, +0.1615] |
| pooled, draw 1 on every pair | all three | 0.9247 | [0.8815, 0.9626] | +0.4247 | [+0.3291, +0.5149] | [+0.3815, +0.4626] |
| pooled, draw 1 on every pair | totals rand. | 0.6043 | [0.5612, 0.6698] | +0.1043 | [+0.0081, +0.1967] | [+0.0612, +0.1698] |
| the 30 pairs at draw 1 | sup. only | 0.6169 | [0.5386, 0.7025] | +0.1169 | [+0.0059, +0.2313] | [+0.0386, +0.2025] |
| the 30 pairs at draw 1 | all three | 0.9231 | [0.8616, 0.9722] | +0.4231 | [+0.3006, +0.5502] | [+0.3616, +0.4722] |
| the 30 pairs at draw 1 | totals rand. | 0.6047 | [0.5453, 0.6872] | +0.1047 | [-0.0081, +0.2187] | [+0.0453, +0.1872] |

## AUX-R128-POOLED66 — the pooled 66 external questions (ADDENDUM_E1_5.md Run A: the external part of the 150-item stratified subsample of the E1 universe, seed 42, quota PRESENT 50 / ABSENT 60 / PN 40, which resolves by backend to FR-Bank 84, Mem0 29, A-MEM 37; `e1_metamemory/run_a_frontier_indexed.json`)

| store | PRESENT (full-store questions) | ABSENT (natural-absent probes) | total |
|---|---:|---:|---:|
| mem0 | 15 | 14 | 29 |
| amem | 21 | 16 | 37 |
| both | 36 | 30 | 66 |

Personas: 29.

## AUX-R128-GROUPS — the R127 and R127b readings (reported in REPORT_R127.md and REPORT_R128.md, not printed): `reviews/v22/results/r127_groups.json` (the 104 PN against the three PRESENT groups, per reader) and `r127b_groups.json` (question-only and with-summary means and the paired gains); the groups are AUX-R126-E3-INTENT's.
