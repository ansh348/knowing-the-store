# NUMBERS_R129.md: the pass ledger of program R129 (2026-09-20)

Written by `reviews/v22/tools/ledger_r129.py` from the artifacts named in each section; no number is typed by hand.

## AUX-R129-GROUPS — the 104 obligations against the three PRESENT groups of tab:e3-intent, per reader (Appendix E.3, tab:e3-groups; `reviews/v22/results/r127_groups.json` for the with-summary AUROC and its intervals, `r127b_groups.json` for the means, the question-only AUROC and the paired gain; item-level and persona-grouped bootstrap, 1,000 draws, seed 42)

Groups (AUX-R126-E3-INTENT): (a) 33 PRESENT questions whose own attribute holds a non-active record under current or upcoming intent; (b) 11 under change intent; (c) the remaining 130. Readers: GPT-4.1 mini one call (question only and INDEXED-TRUE); Haiku 4.5, Opus 5 and GPT-5.6 Luna the five-call collapse (BLIND and INDEXED-TRUE); the name lookup has no question-only form. The gain is the with-summary AUROC minus the question-only AUROC on the same items.

| reader | group | n | mean, question only | mean, with summary | AUROC with summary | item interval | persona interval | AUROC question only | gain | item interval | persona interval |
|---|---|---:|---:|---:|---:|---|---|---:|---:|---|---|
| GPT-4.1 mini | the 104 obligations | 104 | 0.0000 | 0.2591 | | | | | | | |
| | (a) | 33 | 0.0000 | 0.0773 | 0.6801 | [0.5924, 0.7619] | [0.5649, 0.7791] | 0.5000 | +0.1801 | [+0.0924, +0.2619] | [+0.0649, +0.2791] |
| | (b) | 11 | 0.0000 | 0.0455 | 0.6875 | [0.5809, 0.7815] | [0.5574, 0.7973] | 0.5000 | +0.1875 | [+0.0809, +0.2815] | [+0.0574, +0.2973] |
| | (c) | 130 | 0.0015 | 0.0296 | 0.6947 | [0.6261, 0.7659] | [0.6051, 0.7868] | 0.4923 | +0.2024 | [+0.1362, +0.2742] | [+0.1100, +0.2943] |
| Haiku 4.5 | the 104 obligations | 104 | 0.1201 | 0.3399 | | | | | | | |
| | (a) | 33 | 0.3559 | 0.2177 | 0.6716 | [0.5738, 0.7598] | [0.5623, 0.7620] | 0.2902 | +0.3814 | [+0.2577, +0.5018] | [+0.2671, +0.5158] |
| | (b) | 11 | 0.1340 | 0.1800 | 0.7019 | [0.5759, 0.8049] | [0.5549, 0.8349] | 0.4637 | +0.2382 | [-0.0092, +0.4692] | [-0.0743, +0.5068] |
| | (c) | 130 | 0.1787 | 0.1216 | 0.7889 | [0.7238, 0.8436] | [0.7237, 0.8564] | 0.4315 | +0.3574 | [+0.2704, +0.4448] | [+0.2450, +0.4719] |
| GPT-5.6 Luna | the 104 obligations | 104 | 0.0651 | 0.4720 | | | | | | | |
| | (a) | 33 | 0.1175 | 0.3322 | 0.6173 | [0.5177, 0.7166] | [0.4752, 0.7310] | 0.3550 | +0.2622 | [+0.1315, +0.3839] | [+0.1341, +0.3717] |
| | (b) | 11 | 0.0880 | 0.1589 | 0.7906 | [0.6609, 0.9077] | [0.6210, 0.9202] | 0.3951 | +0.3955 | [+0.1343, +0.6512] | [+0.0888, +0.6503] |
| | (c) | 130 | 0.0858 | 0.1308 | 0.8311 | [0.7735, 0.8833] | [0.7507, 0.8990] | 0.4098 | +0.4213 | [+0.3389, +0.5097] | [+0.3135, +0.5207] |
| Opus 5 | the 104 obligations | 104 | 0.3906 | 0.5171 | | | | | | | |
| | (a) | 33 | 0.4587 | 0.4495 | 0.5747 | [0.4462, 0.6920] | [0.4189, 0.7047] | 0.3977 | +0.1770 | [+0.0924, +0.2693] | [+0.0616, +0.2906] |
| | (b) | 11 | 0.3905 | 0.2667 | 0.7841 | [0.6529, 0.9110] | [0.6360, 0.9074] | 0.5109 | +0.2732 | [+0.0395, +0.4901] | [+0.0076, +0.5129] |
| | (c) | 130 | 0.3394 | 0.2336 | 0.8160 | [0.7606, 0.8681] | [0.7552, 0.8797] | 0.6139 | +0.2021 | [+0.1392, +0.2671] | [+0.1300, +0.2810] |
| name lookup | the 104 obligations | 104 | | 0.2636 | | | | | | | |
| | (a) | 33 | | 0.1279 | 0.7395 | [0.6484, 0.8213] | [0.6299, 0.8277] | | | | |
| | (b) | 11 | | 0.1583 | 0.6932 | [0.5518, 0.8165] | [0.5451, 0.8092] | | | | |
| | (c) | 130 | | 0.1226 | 0.7428 | [0.6692, 0.8112] | [0.6548, 0.8276] | | | | |

### AUX-R129-GROUPS-PRINTED — the two-decimal forms Appendix E.3's sentences print
With the summary, the obligations against group (a): 0.68, 0.67, 0.62, 0.57 (range 0.57 to 0.68); against group (c): 0.69, 0.79, 0.83, 0.82 (0.69 to 0.83). Question only against group (a), the three models that score anything without a summary (Haiku 4.5, GPT-5.6 Luna, Opus 5): 0.29, 0.35, 0.40 (0.29 to 0.40). The name lookup against (a), (b), (c): 0.74, 0.69, 0.74.

## AUX-R129-HYB-MINI5 — GPT-4.1 mini at five draws minus the hybrid reader (`reviews/v22/results/r129_hybrid_mini5.json`; the hybrid recomputed by the frozen recipe and gated on 0.7865, the one-draw difference gated on -0.0698, the five-draw row read from working tree and gated on 0.7648)

| row | model | minus the hybrid | item interval | persona interval | both exclude zero |
|---|---:|---:|---|---|---|
| GPT-4.1 mini, one draw (recorded) | 0.7167 | -0.0698 | [-0.1187, -0.0192] | [-0.1094, -0.0316] | True |
| GPT-4.1 mini, five draws (AUX-R122-K5) | 0.7648 | -0.0217 | [-0.0621, +0.0186] | [-0.0587, +0.0067] | False |

**The five-draw difference is not reliable in either direction** (-0.0217; both intervals include zero).

### AUX-R129-HYB-PRINTED — the two-decimal forms Section 5.2's hybrid paragraph prints
The hybrid's whole-set AUROC 0.7865 prints as 0.79; hybrid minus the lookup +0.0201 with the item interval including zero (not reliable); Opus 5, GPT-5.6 Luna and GPT-5.6 Sol minus the hybrid +0.0540, +0.0553, +0.0635, each with both intervals excluding zero, print as 0.05 to 0.06.

## AUX-R129-B9 — the inverted tag (`frbank:fatima:fatima_q06`; AUX-DS-AUDIT-SOURCE) corrected on paper: E.10's counts both ways (`reviews/v22/results/r129_b9.json`; no answer re-scored)

Scorable obligations 89 (63 supersession, 26 retraction). Views with an active line asserting the stale value: as joined **35** (21 supersession, 14 retraction); with the tag corrected **34** (21, 13). The FULL view of the question holds active stale lines [2, 3] and the tagged retraction statement at line [8]; the SLOT-ABLATED view holds neither, so it is outside the 35 either way.

| answerer (D.4, ORACLE) | stale with such a line / stale without, as joined | not stale with / without | stale with / without, corrected | answered stale on that view |
|---|---|---|---|---|
| GPT-4.1 mini | 16 / 0 | 19 / 50 | 15 / 1 | True |
| Haiku 4.5 | 14 / 5 | 21 / 45 | 13 / 6 | True |

Printed forms: 'of 16' and 'of 19' stale answers under the oracle, 16 of 16 and 14 of 19 on such a view as joined, 15 of 16 and 13 of 19 with the tag corrected. Every answer-stage table was scored with the tag as joined (the captions say so).

## AUX-R129-COUNT — the prediction count with E9 in it

The moved-count control's second amendment (registrations/ADDENDUM_V2R_CAT_AMENDMENT_2.md, frozen at b0bee93, day 40) registered one prediction with a bar, P-M2 (both models fall reliably on retraction and on expiry); it failed for both models on retraction (AUX-V2RCAT-A2-P-M2). AUX-R124-TALLY: 92 predictions, 28 otherwise, of which tab:registrations-d carries 28 with 10. With P-M2: **93 predictions, 29 otherwise; tab:registrations-d 29 with 11**; the other three tables unchanged (47 with 8; 17 with 10; none).

## AUX-R129-E9-PRINTED — the two-decimal forms Section 5.1 prints (each the rounding of a ledgered value; the whole-set rows for tab:v2rcat's E9 rows)

| reader | state | recorded sup.-only row | moved-count row | delta | item interval | persona interval | both exclude zero | printed | source |
|---|---|---:|---:|---:|---|---|---|---:|---|
| Opus 5 (five draws) | retraction | 0.5872 | 0.4869 | -0.1003 | [-0.1612, -0.0472] | [-0.2079, -0.0317] | True | 0.10 | AUX-V2RCAT-A1-OP5-K5 |
| Opus 5 (five draws) | expiry | 0.6150 | 0.4869 | -0.1281 | [-0.2127, -0.0517] | [-0.2651, -0.0095] | True | 0.13 | AUX-V2RCAT-A1-OP5-K5 |
| GPT-5.6 Luna | whole set | 0.8417 | 0.8121 | -0.0297 | [-0.0499, -0.0089] | [-0.0583, -0.0081] | True | 0.03 | AUX-V2RCAT-A2-LUNA-K5 |
| GPT-5.6 Luna | retraction | 0.5458 | 0.4794 | -0.0664 | [-0.1505, +0.0156] | [-0.1903, +0.0294] | False | 0.07 | AUX-V2RCAT-A2-LUNA-K5 |
| GPT-5.6 Luna | expiry | 0.6167 | 0.5008 | -0.1158 | [-0.2162, -0.0210] | [-0.2551, -0.0121] | True | 0.12 | AUX-V2RCAT-A2-LUNA-K5 |
| GPT-5.6 Sol | whole set | 0.8500 | 0.8172 | -0.0327 | [-0.0521, -0.0151] | [-0.0621, -0.0102] | True | 0.03 | AUX-V2RCAT-A2-SOL-K5 |
| GPT-5.6 Sol | retraction | 0.5322 | 0.5000 | -0.0322 | [-0.1121, +0.0440] | [-0.1228, +0.0636] | False | 0.03 | AUX-V2RCAT-A2-SOL-K5 |
| GPT-5.6 Sol | expiry | 0.6403 | 0.4489 | -0.1914 | [-0.2862, -0.1074] | [-0.3232, -0.0816] | True | 0.19 | AUX-V2RCAT-A2-SOL-K5 |

Section 5.1 prints Opus 0.10 and 0.13, Luna and Sol 0.12 and 0.19 on expiry (both intervals excluding zero) and 0.07 and 0.03 on retraction (intervals including zero); GPT-4.1 mini and Haiku 4.5 show no change reliable under both intervals (AUX-V2RCAT-MINI, -H45: +0.0269 / +0.0611 and -0.0072 / -0.0453, each with at least one interval including zero).
