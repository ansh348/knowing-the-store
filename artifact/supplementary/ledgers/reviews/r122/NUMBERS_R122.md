# NUMBERS_R122 — the ledger of program R122, the no-human batch (2026-09-19)

Every number a report of this program cites is here or in `reviews/r122/results/*.json`; nothing is typed from memory. Readings use the paper's vocabulary: **reliable** = both the item-level and the persona-grouped interval exclude zero; **within tolerance** = |Δ| ≤ 0.05 at the point estimate.

## 0. AUX-R122-FREEZE

The four registrations frozen at commit **`77bc0d9`** (`FREEZE_R122.md`: T1 `eb0553ba…`, T3 `953e94a2…`, T4 `f8a42bf5…`, T5 `1176a8af…`), before any call and before any scoring; T2 skipped (R120's draft). Tools hashed in the same record. Caps: OpenAI 5.00 USD for the batch, Anthropic 0 (no call).

## T1. The name lookup under further sentence encoders (ADDENDUM_R122_ENCODERS.md)

### AUX-R122-ENC-LOCK

Registered text sha256 `eb0553ba2720fa1c2cffa0be062ba892d1f174d1381cf13db104adb2ad9f7da1`; gates (MiniLM-L6-v2, the recorded encoder) {'v2': 0.7663, 'v3': 0.8756, '661': 0.7484, '661_clean': 0.7442} PASS; lookup code score_cf.matcher (444) / run_nb6.emb_scores (661), the encoder object swapped, no prefix; loaded ['sentence-transformers/all-mpnet-base-v2', 'BAAI/bge-small-en-v1.5']; not loaded none; 218 distinct names; token seed 42.

### AUX-R122-ENC-ROWS — the lookup per encoder (AUROC; item-level and persona-grouped 95% intervals; the paired difference against MiniLM with both intervals)

| encoder | population | whole | item CI | persona CI | minus MiniLM (item; persona) | SUP / RET / EXP |
|---|---|---:|---|---|---|---|
| MINILM `sentence-transformers/all-MiniLM-L6-v2` | v2 | 0.7663 | [0.7174, 0.8151] | [0.7226, 0.8051] | (recorded row) | 0.9223 / 0.5000 / 0.5000 |
| MINILM `sentence-transformers/all-MiniLM-L6-v2` | v3 | 0.8756 | [0.8387, 0.9082] | [0.8391, 0.9111] | (recorded row) | 0.8995 / 0.7975 / 0.8711 |
| MINILM `sentence-transformers/all-MiniLM-L6-v2` | 661 | 0.7484 | [0.6842, 0.8108] | [0.6636, 0.8298] | (recorded row) | — |
| MINILM `sentence-transformers/all-MiniLM-L6-v2` | 661_clean | 0.7442 | [0.6832, 0.8117] | [0.6513, 0.8336] | (recorded row) | — |
| MPNET `sentence-transformers/all-mpnet-base-v2` | v2 | 0.7605 | [0.7104, 0.8086] | [0.7140, 0.8024] | -0.0059 ([-0.0240, +0.0126]; [-0.0224, +0.0093]) | 0.9156 / 0.5000 / 0.5000 |
| MPNET `sentence-transformers/all-mpnet-base-v2` | v3 | 0.8646 | [0.8244, 0.9002] | [0.8296, 0.9018] | -0.0110 ([-0.0296, +0.0063]; [-0.0257, +0.0034]) | 0.8814 / 0.8019 / 0.8717 |
| MPNET `sentence-transformers/all-mpnet-base-v2` | 661 | 0.7642 | [0.6983, 0.8248] | [0.6705, 0.8573] | +0.0158 ([-0.0275, +0.0585]; [-0.0469, +0.0686]) | — |
| MPNET `sentence-transformers/all-mpnet-base-v2` | 661_clean | 0.7642 | [0.7015, 0.8290] | [0.6574, 0.8619] | +0.0200 ([-0.0037, +0.0426]; [-0.0095, +0.0507]) | — |
| BGE `BAAI/bge-small-en-v1.5` | v2 | 0.7584 | [0.7039, 0.8067] | [0.7166, 0.7989] | -0.0080 ([-0.0298, +0.0143]; [-0.0244, +0.0098]) | 0.9203 / 0.5000 / 0.5000 |
| BGE `BAAI/bge-small-en-v1.5` | v3 | 0.8690 | [0.8293, 0.9047] | [0.8326, 0.9076] | -0.0066 ([-0.0254, +0.0101]; [-0.0259, +0.0134]) | 0.8802 / 0.8172 / 0.8878 |
| BGE `BAAI/bge-small-en-v1.5` | 661 | 0.8133 | [0.7595, 0.8588] | [0.7452, 0.8856] | +0.0649 ([+0.0292, +0.1026]; [+0.0101, +0.1297]) | — |
| BGE `BAAI/bge-small-en-v1.5` | 661_clean | 0.7620 | [0.6995, 0.8245] | [0.6595, 0.8519] | +0.0178 ([-0.0014, +0.0392]; [-0.0170, +0.0530]) | — |

### AUX-R122-ENC-RANDOM — the random-token control (every attribute name replaced by a stable random token; descriptive)

| encoder | population | whole | item CI | persona CI | minus the same encoder's name row | SUP / RET / EXP |
|---|---|---:|---|---|---|---|
| MINILM | v2 | 0.5954 | [0.5392, 0.6501] | [0.5601, 0.6383] | -0.1709 | 0.6651 / 0.5000 / 0.5000 |
| MINILM | v3 | 0.5479 | [0.4921, 0.6078] | [0.5260, 0.5740] | -0.3277 | 0.5385 / 0.5697 / 0.5694 |
| MINILM | 661 | 0.6654 | [0.6080, 0.7226] | [0.5874, 0.7417] | -0.0830 | — |
| MINILM | 661_clean | 0.6627 | [0.6040, 0.7231] | [0.5798, 0.7393] | -0.0815 | — |
| MPNET | v2 | 0.5977 | [0.5475, 0.6552] | [0.5620, 0.6365] | -0.1628 | 0.6618 / 0.5000 / 0.5000 |
| MPNET | v3 | 0.5363 | [0.4771, 0.5939] | [0.5203, 0.5555] | -0.3283 | 0.5400 / 0.5361 / 0.5261 |
| MPNET | 661 | 0.7150 | [0.6616, 0.7714] | [0.6475, 0.7854] | -0.0492 | — |
| MPNET | 661_clean | 0.7003 | [0.6406, 0.7613] | [0.6225, 0.7763] | -0.0639 | — |
| BGE | v2 | 0.5948 | [0.5421, 0.6473] | [0.5580, 0.6396] | -0.1636 | 0.6704 / 0.5000 / 0.5000 |
| BGE | v3 | 0.5452 | [0.4876, 0.6046] | [0.5262, 0.5701] | -0.3238 | 0.5517 / 0.5275 / 0.5478 |
| BGE | 661 | 0.6989 | [0.6461, 0.7426] | [0.6228, 0.7666] | -0.1144 | — |
| BGE | 661_clean | 0.6437 | [0.5886, 0.6992] | [0.5681, 0.7174] | -0.1183 | — |

### AUX-R122-ENC-P-E1 — **HOLDS** (both encoders within 0.05 of MiniLM's 0.7663 on the whole counterfactual set under v2, at the point estimate)

- MPNET: 0.7605, minus MiniLM -0.0059 (item [-0.0240, +0.0126]; persona [-0.0224, +0.0093]); within tolerance: True
- BGE: 0.7584, minus MiniLM -0.0080 (item [-0.0298, +0.0143]; persona [-0.0244, +0.0098]); within tolerance: True

## T5. What the gate buys, reach only (ADDENDUM_R122_GATE_REACH.md)

### AUX-R122-GATE-LOCK

Registered text sha256 `1176a8af2158fc7fa1c0517d7003b55e0542bae440411ea1a6291e383e710b4e`; locks {'tagged5_equals_always': 661, 'ranking_top10_reproduced': 661, 'lookup_gate': {'nb6_661': 0.7484204529761083, 'nb5_307': 0.6185924369747899, 'pass': True}}; the MODEL rule's recorded rows reproduced (reach 85 of 104, licensed in view 65 of 174, mean view 5.4342 over the 661). Census: {'items_with_a_best_name': 466, 'items_fetching_at_least_one_record': 466, 'mean_fetched_661': 1.583963691376702, 'obligations_whose_best_name_is_a_forbidding_slot': 58, 'n_obligations': 104, 'recency': {'mean_kept_per_variant': 219.29954614220878, 'mean_variant_size': 427.93494704992435, 'pn_member_kept_items': 38}, 'a6_recorded_inview': {'10': 89, '5': 65, '6': 72, '7': 77, '8': 82, '9': 88, 'GATED': 87}}.

### AUX-R122-GATE-ROWS — every truncation (reach on the 104 with Wilson; the paired difference against the MODEL rule, item-level and persona-grouped; licensed record in view on the 174; lines per question over the 661)

| policy | reach | Wilson | minus MODEL (item; persona) | sup / ret / exp | licensed in view | minus MODEL | mean lines 661 (max) | mean 104 | ratio to MODEL |
|---|---|---|---|---|---|---|---|---|---|
| ALWAYS-FETCH, fill k=0 | 56/104 = 0.5385 | [0.443, 0.631] | -0.2788 ([-0.3942, -0.1635]; [-0.4467, -0.1199]) | 54/63 / 2/26 / 0/15 | 1/174 = 0.0057 | -0.3678 ([-0.4425, -0.2989]; [-0.4596, -0.2874]) | 1.5840 (8) | 1.7212 | 0.2915 |
| ALWAYS-FETCH, fill k=1 | 69/104 = 0.6635 | [0.568, 0.747] | -0.1538 ([-0.2596, -0.0577]; [-0.2881, -0.0300]) | 54/63 / 8/26 / 7/15 | 21/174 = 0.1207 | -0.2529 ([-0.3161, -0.1897]; [-0.3438, -0.1716]) | 2.5719 (9) | 2.6538 | 0.4733 |
| ALWAYS-FETCH, fill k=2 | 76/104 = 0.7308 | [0.638, 0.807] | -0.0865 ([-0.1731, +0.0000]; [-0.2016, +0.0200]) | 54/63 / 11/26 / 11/15 | 35/174 = 0.2011 | -0.1724 ([-0.2299, -0.1205]; [-0.2446, -0.1029]) | 3.5522 (10) | 3.5673 | 0.6537 |
| ALWAYS-FETCH, fill k=3 | 84/104 = 0.8077 | [0.722, 0.872] | -0.0096 ([-0.0772, +0.0577]; [-0.0949, +0.0700]) | 54/63 / 18/26 / 12/15 | 44/174 = 0.2529 | -0.1207 ([-0.1724, -0.0747]; [-0.1790, -0.0678]) | 4.5401 (11) | 4.5096 | 0.8355 |
| ALWAYS-FETCH, fill k=4 | 85/104 = 0.8173 | [0.732, 0.880] | +0.0000 ([-0.0673, +0.0673]; [-0.0893, +0.0909]) | 54/63 / 19/26 / 12/15 | 60/174 = 0.3448 | -0.0287 ([-0.0575, -0.0057]; [-0.0578, -0.0057]) | 5.5280 (12) | 5.4519 | 1.0173 |
| ALWAYS-FETCH, fill k=5 | 86/104 = 0.8269 | [0.743, 0.888] | +0.0096 ([-0.0577, +0.0673]; [-0.0804, +0.0980]) | 54/63 / 20/26 / 12/15 | 65/174 = 0.3736 | +0.0000 ([+0.0000, +0.0000]; [+0.0000, +0.0000]) | 6.5129 (13) | 6.3942 | 1.1985 |
| TAGGED-k=5 | 54/104 = 0.5192 | [0.424, 0.613] | -0.2981 ([-0.3942, -0.2115]; [-0.4228, -0.1665]) | 22/63 / 20/26 / 12/15 | 65/174 = 0.3736 | +0.0000 ([+0.0000, +0.0000]; [+0.0000, +0.0000]) | 5.0000 (5) | 5.0000 | 0.9201 |
| TAGGED-k=6 | 60/104 = 0.5769 | [0.481, 0.667] | -0.2404 ([-0.3365, -0.1538]; [-0.3704, -0.0968]) | 25/63 / 23/26 / 12/15 | 72/174 = 0.4138 | +0.0402 ([+0.0172, +0.0690]; [+0.0126, +0.0719]) | 6.0000 (6) | 6.0000 | 1.1041 |
| TAGGED-k=7 | 62/104 = 0.5962 | [0.500, 0.685] | -0.2212 ([-0.3077, -0.1346]; [-0.3530, -0.0850]) | 27/63 / 23/26 / 12/15 | 77/174 = 0.4425 | +0.0690 ([+0.0345, +0.1092]; [+0.0363, +0.1037]) | 7.0000 (7) | 7.0000 | 1.2881 |
| TAGGED-k=8 | 69/104 = 0.6635 | [0.568, 0.747] | -0.1538 ([-0.2500, -0.0577]; [-0.2936, -0.0206]) | 32/63 / 25/26 / 12/15 | 82/174 = 0.4713 | +0.0977 ([+0.0517, +0.1437]; [+0.0588, +0.1377]) | 8.0000 (8) | 8.0000 | 1.4722 |
| TAGGED-k=9 | 70/104 = 0.6731 | [0.578, 0.756] | -0.1442 ([-0.2406, -0.0481]; [-0.2822, -0.0189]) | 33/63 / 25/26 / 12/15 | 88/174 = 0.5057 | +0.1322 ([+0.0805, +0.1897]; [+0.0838, +0.1794]) | 9.0000 (9) | 9.0000 | 1.6562 |
| TAGGED-k=10 | 74/104 = 0.7115 | [0.618, 0.790] | -0.1058 ([-0.2019, -0.0190]; [-0.2407, +0.0294]) | 37/63 / 25/26 / 12/15 | 89/174 = 0.5115 | +0.1379 ([+0.0862, +0.1897]; [+0.0890, +0.1862]) | 10.0000 (10) | 10.0000 | 1.8402 |
| RECENCY-k=5 | 23/104 = 0.2212 | [0.152, 0.310] | -0.5962 ([-0.7019, -0.4904]; [-0.7374, -0.4495]) | 12/63 / 0/26 / 11/15 | 49/174 = 0.2816 | -0.0920 ([-0.1494, -0.0401]; [-0.1585, -0.0259]) | 5.0000 (5) | 5.0000 | 0.9201 |
| RECENCY-k=6 | 26/104 = 0.2500 | [0.177, 0.341] | -0.5673 ([-0.6827, -0.4613]; [-0.7130, -0.4190]) | 15/63 / 0/26 / 11/15 | 53/174 = 0.3046 | -0.0690 ([-0.1322, -0.0115]; [-0.1447, +0.0048]) | 6.0000 (6) | 6.0000 | 1.1041 |
| RECENCY-k=7 | 28/104 = 0.2692 | [0.193, 0.362] | -0.5481 ([-0.6635, -0.4423]; [-0.6970, -0.3924]) | 17/63 / 0/26 / 11/15 | 55/174 = 0.3161 | -0.0575 ([-0.1207, +0.0057]; [-0.1350, +0.0121]) | 7.0000 (7) | 7.0000 | 1.2881 |
| RECENCY-k=8 | 32/104 = 0.3077 | [0.227, 0.402] | -0.5096 ([-0.6156, -0.4038]; [-0.6733, -0.3303]) | 21/63 / 0/26 / 11/15 | 58/174 = 0.3333 | -0.0402 ([-0.1034, +0.0230]; [-0.1183, +0.0328]) | 8.0000 (8) | 8.0000 | 1.4722 |
| RECENCY-k=9 | 33/104 = 0.3173 | [0.236, 0.412] | -0.5000 ([-0.6058, -0.3942]; [-0.6668, -0.3214]) | 22/63 / 0/26 / 11/15 | 61/174 = 0.3506 | -0.0230 ([-0.0862, +0.0402]; [-0.1021, +0.0537]) | 9.0000 (9) | 9.0000 | 1.6562 |
| RECENCY-k=10 | 34/104 = 0.3269 | [0.244, 0.422] | -0.4904 ([-0.5962, -0.3846]; [-0.6596, -0.3119]) | 23/63 / 0/26 / 11/15 | 62/174 = 0.3563 | -0.0172 ([-0.0862, +0.0460]; [-0.0958, +0.0616]) | 10.0000 (10) | 10.0000 | 1.8402 |

### AUX-R122-GATE-MATCHED — the budget-matched rows at the MODEL rule's mean view over the 661, 5.4342 (the registered primary); linear interpolation between the bracketing truncations (Amendment 6's rule), the weight fixed from the population means

| policy | bracketing k (means) | weight on k_hi | achieved mean | reach (matched) | minus MODEL (item; persona) | licensed in view (matched) | minus MODEL (item; persona) |
|---|---|---:|---:|---:|---|---:|---|
| AF | 3 (4.5401), 4 (5.5280) | 0.9051 | 5.4342 | 0.8164 | -0.0009 ([-0.0700, +0.0664]; [-0.0893, +0.0890]) | 0.3361 | -0.0375 ([-0.0657, -0.0159]; [-0.0667, -0.0142]) |
| TAGGED | 5 (5.0000), 6 (6.0000) | 0.4342 | 5.4342 | 0.5443 | -0.2730 ([-0.3621, -0.1865]; [-0.3976, -0.1378]) | 0.3910 | +0.0175 ([+0.0075, +0.0299]; [+0.0055, +0.0312]) |
| RECENCY | 5 (5.0000), 6 (6.0000) | 0.4342 | 5.4342 | 0.2337 | -0.5836 ([-0.6936, -0.4749]; [-0.7300, -0.4370]) | 0.2916 | -0.0820 ([-0.1394, -0.0270]; [-0.1519, -0.0156]) |

### AUX-R122-GATE-MATCHED-104 — the same at the MODEL rule's mean view over the 104 obligations, 7.0769 (Section 8's basis; beside); linear interpolation between the bracketing truncations (Amendment 6's rule), the weight fixed from the population means

| policy | bracketing k (means) | weight on k_hi | achieved mean | reach (matched) | minus MODEL (item; persona) | licensed in view (matched) | minus MODEL (item; persona) |
|---|---|---:|---:|---:|---|---:|---|
| AF | {0: 1.7212, 1: 2.6538, 2: 3.5673, 3: 4.5096, 4: 5.4519, 5: 6.3942} | — | — | target outside the family's range; no matched row | | | |
| TAGGED | 7 (7.0000), 8 (8.0000) | 0.0769 | 7.0769 | 0.6013 | -0.2160 ([-0.3040, -0.1294]; [-0.3475, -0.0785]) | 0.4447 | +0.0712 ([+0.0358, +0.1114]; [+0.0382, +0.1073]) |
| RECENCY | 7 (7.0000), 8 (8.0000) | 0.0769 | 7.0769 | 0.2722 | -0.5451 ([-0.6598, -0.4408]; [-0.6967, -0.3868]) | 0.3174 | -0.0561 ([-0.1172, +0.0062]; [-0.1340, +0.0131]) |

### AUX-R122-GATE-PREDICTIONS

- **P-G1 HOLDS**: ALWAYS-FETCH budget-matched reach 0.8164 against the MODEL rule's 0.8173, D -0.0009 ([-0.0700, +0.0664]; [-0.0893, +0.0890]); unmatched (five lines plus the fetch) 0.8269.
- **P-G2 HOLDS**: ALWAYS-FETCH before matching spends 6.5129 lines per question over the 661 against the MODEL rule's 5.4342; ratio 1.1985.
- **P-G3 HOLDS**: RECENCY budget-matched reach 0.2337 against the MODEL rule's 0.8173, D -0.5836 ([-0.6936, -0.4749]; [-0.7300, -0.4370]); unmatched RECENCY-7 0.2692.

## T4. The counterfactual set under the intent-explicit rubric P1 (ADDENDUM_R122_CF2_P1.md)

### AUX-R122-P1-ROWS

| row | whole [persona CI] | minus the lookup (item; persona) | SUP / RET / EXP | PN vs PRESENT | W/T/L | distinct values | tied triples | identical draws / median range | census |
|---|---|---|---|---|---|---:|---:|---|---|
| GPT-5.6 Luna P1 k=5 | 0.8531 [0.8108, 0.8950] | +0.0867 ([+0.0447, +0.1302]; [+0.0562, +0.1219]) | 0.9470 / 0.5997 / 0.6347 | 0.8566 | 125/1/22 | 228 | 0 | 6 / 0.1 | 2220 rows, 0 not OK, $0.7745 |
| GPT-5.6 Luna P0 k=5 (recorded, E5) | 0.8417 [0.7999, 0.8835] | +0.0754 ([+0.0339, +0.1216]; [+0.0450, +0.1090]) | 0.9426 / 0.5458 / 0.6167 | 0.8544 | 129/2/17 | 239 | 0 | 9 / 0.12 | 2220 rows, 1 not OK, $0.7478 |
| GPT-4.1 mini P1 k=1 | 0.7253 [0.6738, 0.7731] | -0.0411 ([-0.0878, +0.0034]; [-0.0817, -0.0036]) | 0.8591 / 0.5456 / 0.4758 | 0.7120 | 80/52/16 | 10 | 45 | 0 / None | 444 rows, 0 not OK, $0.2976 |
| GPT-4.1 mini P0 k=1 (recorded) | 0.7167 [0.6663, 0.7649] | -0.0496 ([-0.1012, +0.0013]; [-0.0933, -0.0054]) | 0.8308 / 0.5283 / 0.5489 | 0.7056 | 81/57/10 | 12 | 51 | 0 / None | 444 rows, 0 not OK, $0.3045 |

### AUX-R122-P1-DELTA — P1 minus P0 (item-level; persona-grouped), whole and per state

- LUNA: whole +0.0113 ([-0.0052, +0.0277]; [-0.0010, +0.0227]); SUPERSESSION +0.0043 ([-0.0051, +0.0140]; [-0.0056, +0.0141]); RETRACTION +0.0539 ([-0.0133, +0.1247]; [-0.0055, +0.1164]); EXPIRY +0.0181 ([-0.0905, +0.1197]; [-0.0354, +0.0700]) (covered 444)
- MINI: whole +0.0085 ([-0.0260, +0.0430]; [-0.0290, +0.0417]); SUPERSESSION +0.0282 ([-0.0047, +0.0645]; [-0.0046, +0.0583]); RETRACTION +0.0172 ([-0.0803, +0.1089]; [-0.0927, +0.1145]); EXPIRY -0.0731 ([-0.1795, +0.0319]; [-0.1615, +0.0269]) (covered 444)

### AUX-R122-P1-P-R1 — **HOLDS** (each reader within 0.05 of its recorded P0 whole-set value, at the point)

- LUNA: P1 0.8531 vs P0 0.8417, delta +0.0113, within True
- MINI: P1 0.7253 vs P0 0.7167, delta +0.0085, within True

### AUX-R122-P1-P-R2 — **FAILS** (the per-state ordering unchanged)

- LUNA: P0 SUPERSESSION > EXPIRY > RETRACTION; P1 SUPERSESSION > EXPIRY > RETRACTION; same True
- MINI: P0 SUPERSESSION > EXPIRY > RETRACTION; P1 SUPERSESSION > RETRACTION > EXPIRY; same False

### AUX-R122-P1-P-R3 — **HOLDS** (Luna under P1 minus the lookup keeps its sign with both intervals excluding zero)

- Luna P1 minus the lookup 0.7663: +0.0867 ([+0.0447, +0.1302]; [+0.0562, +0.1219]); recorded P0 margin +0.0754; both exclude zero True

### AUX-R122-OAI-SPEND — token-metered from the rows at the page prices (not an invoice): {"MINI5": {"rows": 91, "usd": 0.0545, "not_ok": 0, "cached_share": 0.1881, "served": ["gpt-4.1-mini-2025-04-14"]}, "P1LUNA": {"rows": 2220, "usd": 0.7745, "not_ok": 0, "cached_share": 0.7991, "served": ["gpt-5.6-luna"]}, "P1MINI": {"rows": 444, "usd": 0.2976, "not_ok": 0, "cached_share": 0.1171, "served": ["gpt-4.1-mini-2025-04-14"]}, "probes_usd": 0.0022, "total_usd": 1.1288}; cap 5.00 USD for the batch.

## T3. GPT-4.1 mini at five draws on the counterfactual set (ADDENDUM_R122_MINI_K5.md)

### AUX-R122-K5-ROWS

| row | whole [persona CI] | minus the lookup (item; persona) | SUP / RET / EXP | PN vs PRESENT | W/T/L | distinct values | tied triples | identical draws / median range | census |
|---|---|---|---|---|---|---:|---:|---|---|
| INDEXED-V2: gpt-4.1-mini k=5 (temperature unset) | 0.7648 [0.7218, 0.8047] | -0.0016 ([-0.0426, +0.0393]; [-0.0415, +0.0328]) | 0.8793 / 0.5761 / 0.5594 | 0.7394 | 100/15/33 | 74 | 6 | 58 / 0.05 | 2220 rows, 0 not OK, $1.1066 |
| INDEXED-V2: gpt-4.1-mini k=1 temperature 0 (recorded) | 0.7167 [0.6663, 0.7649] | -0.0496 ([-0.1012, +0.0013]; [-0.0933, -0.0054]) | 0.8308 / 0.5283 / 0.5489 | 0.7056 | 81/57/10 | 12 | 51 | 0 / None | 444 rows, 0 not OK, $0.3045 |
| INDEXED-V3: gpt-4.1-mini k=5 (temperature unset) | 0.8323 [0.7889, 0.8725] | -0.0433 ([-0.0879, -0.0035]; [-0.0838, -0.0042]) | 0.8829 / 0.8433 / 0.6719 | 0.8307 | 130/5/13 | 78 | 1 | 49 / 0.1 | 2220 rows, 0 not OK, $1.0368 |
| INDEXED-V3: gpt-4.1-mini k=1 temperature 0 (recorded) | 0.7967 [0.7438, 0.8478] | -0.0789 ([-0.1229, -0.0344]; [-0.1283, -0.0334]) | 0.8444 / 0.8725 / 0.5869 | 0.7840 | 105/32/11 | 12 | 26 | 0 / None | 444 rows, 0 not OK, $0.3132 |

### AUX-R122-K5-DELTA — five-draw minus one-draw (item-level; persona-grouped), whole and per state

- INDEXED-V2: whole +0.0481 ([+0.0119, +0.0857]; [+0.0171, +0.0827]); SUPERSESSION +0.0485 ([+0.0129, +0.0886]; [+0.0144, +0.0857]); RETRACTION +0.0478 ([-0.0506, +0.1669]; [-0.0377, +0.1481]); EXPIRY +0.0106 ([-0.1000, +0.1224]; [-0.0752, +0.0774]) (covered 444)
- INDEXED-V3: whole +0.0356 ([+0.0094, +0.0619]; [+0.0092, +0.0688]); SUPERSESSION +0.0385 ([+0.0069, +0.0770]; [+0.0041, +0.0801]); RETRACTION -0.0292 ([-0.0745, +0.0111]; [-0.0699, +0.0147]); EXPIRY +0.0850 ([+0.0072, +0.1704]; [+0.0146, +0.1783]) (covered 444)

### AUX-R122-K5-P-K1 — **HOLDS** (per summary: within 0.05 at the point and the tied-triple count falls; HOLDS iff both summaries)

- INDEXED-V2: k5 0.7648 vs k1 0.7167 (delta +0.0481; within True); tied triples 51 -> 6 (falls True) -> holds
- INDEXED-V3: k5 0.8323 vs k1 0.7967 (delta +0.0356; within True); tied triples 26 -> 1 (falls True) -> holds

### AUX-R122-OAI-SPEND — token-metered from the rows at the page prices (not an invoice): {"MINI5": {"rows": 4440, "usd": 2.1434, "not_ok": 0, "cached_share": 0.4299, "served": ["gpt-4.1-mini-2025-04-14"]}, "P1LUNA": {"rows": 2220, "usd": 0.7745, "not_ok": 0, "cached_share": 0.7991, "served": ["gpt-5.6-luna"]}, "P1MINI": {"rows": 444, "usd": 0.2976, "not_ok": 0, "cached_share": 0.1171, "served": ["gpt-4.1-mini-2025-04-14"]}, "probes_usd": 0.0022, "total_usd": 3.2177}; cap 5.00 USD for the batch.
