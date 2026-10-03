# NUMBERS_R102.md — printed forms of the v10 clarity rewrite (R102, 2026-09-13)

Purpose. The v10 brief (rule 1.2) lets main-text prose print a four-decimal ledger value at two decimals. `trace_scan_v13.py` accounts every printed token against the ledger family by string, so each two-decimal form is recorded here against the four-decimal key it rounds (Decimal, ROUND_HALF_UP), on the R86/R87/R97 precedent (`tools/trace_scan_v13.py` LEDGERS). No new measurement enters through this file; every source value is a ledger key that already prints in a v9 table or appendix, and the four-decimal form still prints in v10 (rule 1.3).

Method. `numeric_diff.py --round2` pairs each two-decimal token added in `paper_v10.tex` with a base token that rounds to it and prints the pair under ROUNDED-ACCEPTED; that pairing is set-based (any base token that rounds to the printed form), so the intended source is recorded here from the sentence that prints it (`reviews/v10/NUMBER_MOVES.md` section C; `reviews/v10/REPORT.md`). Signed forms are listed with and without their sign because the scan may strip the sign before matching.

## Rounded forms (printed | source value | source key or v9 table | v10 site)

| printed | source | key / table | v10 site |
|---|---|---|---|
| 0.72 | 0.7167 | NUMBERS_CF2.md AUX-CF2-MINI-V2 (v9 Table 9) | abstract, 1, 5 |
| 0.77 | 0.7663 | NUMBERS_CF2.md AUX-CF2-NB6-V2 (v9 Table 9) | abstract, 1, 5 |
| 0.83 | 0.8303 | NUMBERS_RESP.md AUX-RESP-L2-MINI-NOK (v9 Table 26) | 1, 8 |
| 0.80 | 0.7972 | NUMBERS_R74.md / NUMBERS_E1QP.md (v9 Table 6) | 4 |
| 0.97 | 0.9662 | NUMBERS_R74.md AUX-R74-X1-POOLED (v9 Table 6) | 4 |
| 0.76 | 0.7566 | NUMBERS_CF2.md AUX-CF2-H45-V2 (v9 Table 9) | 5 |
| 0.84 | 0.8405 | NUMBERS_CF2.md AUX-CF2-OP5-V2 (v9 Table 9) | 5 |
| 0.88 | 0.8756 | NUMBERS_CF2.md AUX-CF2-ALLSTATES-V3 (v9 Table 9) | 5, 8 |
| 0.88 | 0.8773 | NUMBERS_CF2.md AUX-CF2-H45-V3 (v9 Table 9) | 5 |
| 0.91 | 0.9079 | NUMBERS_CF2.md AUX-CF2-OP5-V3 (v9 Table 9) | 5 |
| +0.29, 0.29 | +0.2948 | NUMBERS_CF2.md AUX-CF2-NAMEDVSCOUNTED (v9 Table 9) | 5 |
| +0.32, 0.32 | +0.3237 | NUMBERS_CF2.md AUX-CF2-NAMEDVSCOUNTED (v9 Table 9) | 5 |
| +0.33, 0.33 | +0.3295 | NUMBERS_CF2.md AUX-CF2-NAMEDVSCOUNTED (v9 Table 9) | 5 |
| +0.02, 0.02 | +0.0203 | NUMBERS_CF2.md AUX-CF2-NAMEDVSCOUNTED all-states (v9 D.2) | 5 |
| +0.01, 0.01 | +0.0072 | NUMBERS_CF2.md AUX-CF2-EQUIV-V2R (v9 Table 9) | 5 |
| +0.20, 0.20 | +0.2037 | NUMBERS.md FOK FR-Bank hard (v9 Table 1) | 6 |
| +0.19, 0.19 | +0.1914 | NUMBERS.md FOK easy contrast (v9 Table 1) | 6 |
| 0.55 | 0.5517 | NUMBERS.md absence split, genuine absence (v9 L472) | 6 |
| 0.88 | 0.8782 | NUMBERS.md absence split, genuine absence (v9 L472) | 6 |
| 0.43 | 0.4336 | NUMBERS.md absence split, deleted record (v9 L473) | 6 |
| 0.50 | 0.4972 | NUMBERS.md absence split, deleted record (v9 L473) | 6 |
| +0.08, 0.08 | +0.0817 | NUMBERS_E1R.md AUX-E1R-BASELINES (v9 Table 20) | 6 |
| +0.08, 0.08 | +0.0819 | NUMBERS_E1R.md AUX-E1R-BASELINES (v9 Table 20) | 6 |
| +0.37, 0.37 | +0.3687 | NUMBERS_R74.md AUX-R74-X4 luna NOK 661 (v9 Table 3) | 6 |
| +0.19, 0.19 | +0.1898 | NUMBERS_R74.md AUX-R74-X4 Opus 5 NOK 661 (v9 Table 3) | 6 |
| +0.41, 0.41 | +0.4060 | NUMBERS_R74.md AUX-R74-X4 Haiku 4.5 NOK 661 (v9 Table 3) | 6 |
| 0.04 | 0.0389 | NUMBERS_E1XV.md convergence span (v9 App B L1078) | 6 |
| 0.33 | 0.3307 | NUMBERS_E1XV.md convergence span (v9 App B L1078) | 6 |
| 0.70 | 0.7003 | NUMBERS_R74.md AUX-R77-SWAP (v9 Table 16) | 6 |
| 0.36 | 0.3631 | NUMBERS_R74.md AUX-R77-SWAP (v9 Table 16) | 6 |
| 0.73 | 0.7339 | NUMBERS.md NOK FR-Bank indexed (v9 Table 1, 16, 26) | 6, 8 |
| 0.47 | 0.4659 | NUMBERS_R74.md AUX-R77-SWAP (v9 Table 16) | 6 |
| +0.00, 0.00 | +0.0031 | NUMBERS_R74.md AUX-R77-SWAP shuffle FOK (v9 Table 16) | 6 |
| -0.02, 0.02 | -0.0217 | NUMBERS_R74.md AUX-R77-SWAP shuffle NOK (v9 Table 16) | 6 |
| 0.17 | 0.1741 | NUMBERS_E1R.md AUX-E1R-ECE intact (v9 Table 14) | 6 |
| 0.16 | 0.1596 | NUMBERS_E1R.md AUX-E1R-ECE blind (v9 Table 14) | 6 |
| 0.01 | 0.0146 | NUMBERS_R82.md AUX-R82-CAL isotonic ECE (v9 App H) | 6 |
| 0.45 | 0.4526 | NUMBERS.md FOK A-MEM indexed (v9 Table 1) | 7 |
| 0.90 | 0.8974 | NUMBERS_SIDE.md AUX-SIDE-S1-MINI-AMEM (v9 Table 19) | 7 |
| 0.48 | 0.4777 | NUMBERS.md FOK Mem0 indexed (v9 Table 1) | 7 |
| 0.88 | 0.8751 | NUMBERS_SIDE.md AUX-SIDE-S1-MINI-MEM0 (v9 Table 19) | 7 |
| +0.44, 0.44 | +0.4448 | NUMBERS_SIDE.md AUX-SIDE-S1-MINI-AMEM (v9 Table 19) | 7 |
| 0.86 | 0.8554 | NUMBERS_SIDE.md AUX-SIDE-S1-NB5 A-MEM (v9 Table 19) | 7 |
| 0.87 | 0.8700 | NUMBERS_SIDE.md AUX-SIDE-S1-NB5 Mem0 (v9 Table 19) | 7 |
| 0.10 | 0.0969 | NUMBERS.md FOK Mem0 delta (v9 Table 1, 17) | 7 |
| 0.11 | 0.1065 | NUMBERS.md FOK A-MEM delta (v9 Table 1, 17) | 7 |
| 0.34 | 0.3380 | NUMBERS.md luna external pooled delta (v9 Table 17) | 7 |
| 0.10 | 0.1046 | NUMBERS.md sol external pooled delta (v9 Table 17) | 7 |
| -0.11, 0.11 | -0.1065 | NUMBERS_R74.md AUX-R74-X2 A-MEM intact (v9 Table 18) | 7 |
| -0.04, 0.04 | -0.0368 | NUMBERS_R74.md AUX-R74-X2 A-MEM count+markers removed (v9 Table 18) | 7 |
| 0.52 | 0.5192 | NUMBERS_RESP.md AUX-RESP-L2-REACH (v9 Table 26) | 8 |
| 0.71 | 0.7115 | NUMBERS_RESP.md AUX-RESP-L2-REACH ten items (v9 Table 26) | 8 |
| 0.69 | 0.6851 | NUMBERS_RESP.md AUX-RESP-L2-MINI-NOK (v9 Table 26) | 8 |
| -0.05, 0.05 | -0.0488 | NUMBERS_RESP.md AUX-RESP-L2-MINI-NOK (v9 Table 26) | 8 |
| +0.24, 0.24 | +0.2364 | NUMBERS_RESP.md AUX-RESP-L2-MINI-NOK expiry (v9 Table 26) | 8 |
| -0.17, 0.17 | -0.1719 | NUMBERS_RESP.md AUX-RESP-L2-MINI-NOK supersession (v9 Table 26) | 8 |
| +0.10, 0.10 | +0.0964 | NUMBERS_RESP.md AUX-RESP-L2-MINI-NOK hybrid (v9 Table 26) | 8 |
| +0.17, 0.17 | +0.1747 | NUMBERS_RESP.md AUX-RESP-L2-MINI-NOK hybrid expiry (v9 Table 26) | 8 |
| +0.17, 0.17 | +0.1704 | NUMBERS_RESP.md AUX-RESP-L2-MINI-NOK hybrid retraction (v9 Table 26) | 8 |
| 0.86 | 0.8572 | NUMBERS_RESP.md AUX-RESP-L1-MINI supersession truthful (v9 Table 25) | 8 |
| 0.53 | 0.5310 | NUMBERS_RESP.md AUX-RESP-L1-MINI supersession removed (v9 Table 25) | 8 |
| -0.33, 0.33 | -0.3262 | NUMBERS_RESP.md AUX-RESP-L1-MINI supersession delta (v9 Table 25) | 8 |
| -0.14, 0.14 | -0.1404 | NUMBERS_RESP.md AUX-RESP-L1-MINI retraction delta (v9 Table 25) | 8 |
| 0.79 | 0.7885 | NUMBERS_DS.md AUX-DS-FLAGCENSUS oracle ceiling (v9 F.10 L2310) | 8 |
| 0.035 | 0.0348, 0.0357 | NUMBERS_SIDE.md AUX-SIDE-S2-CAP-RECALL (also NUMBERS_R97.md) | 7 |
| 0.92 | 0.9223 | NUMBERS_CF2.md AUX-CF2-NB6-V2 per-state supersession (v9 Table 9) | 1, 5 (targeted pass) |
| 0.83 | 0.8308 | NUMBERS_CF2.md AUX-CF2-MINI-V2 per-state supersession (v9 Table 9) | 5 (targeted pass) |
| 0.93 | 0.9325 | NUMBERS_CF2.md AUX-CF2-OP5-V2 per-state supersession (v9 Table 9) | 5 (targeted pass) |
| 0.62 | 0.6150 | NUMBERS_CF2.md AUX-CF2-OP5-V2 per-state expiry (v9 Table 9) | 5 (targeted pass) |
| 0.86 | 0.8649 | NUMBERS_CF2.md AUX-CF2-COUNTED Haiku 4.5 all-states on the counted states (v9 Table 9) | 5 (targeted pass) |
| 0.60 | 0.5959 | NUMBERS_E1R.md AUX-E1R-BELIEVED-NOK monitor (v9 Table 20) | 5 (targeted pass) |
| 0.59 | 0.5858 | NUMBERS_E1R.md AUX-E1R-NB6 BELIEVED lookup (v9 Table 20) | 5 (targeted pass) |

Tokens the rewrite prints that already print in v9 in the same form and need no row here: 42.3%, 101.4%, 65.5%, 49.4, 12.7%, 60%, 5%, 0.375, 0.20, 0.00, 0.04 (Graphiti precision), 0.50 (blind by construction), every count.
