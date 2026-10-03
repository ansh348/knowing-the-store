# NUMBERS_R104.md — printed forms and deterministic values of the v11-to-v12 pass (R104, 2026-09-13)

Purpose. On the R103 precedent (`tools/trace_scan_v13.py` LEDGERS): (A) rounded forms the body prints against their four-decimal keys; (B) deterministic values computed in this pass with no model call, from recorded rows only, each labelled exploratory in the manuscript. The two new registered runs of this pass (`registrations/ADDENDUM_PAD.md`, `registrations/ADDENDUM_PARA.md`) have their own ledgers once they run.

## A. Rounded forms (printed | source | key | v12 site)

| printed | source | key / table | v12 site |
|---|---|---|---|
| 0.89 | 0.8876 | NUMBERS_CF2.md AUX-CF2-PERSTATE, Haiku 4.5 supersession under v2 (Table 13) | 5 |
| 0.01 | -0.0098 | reviews/NUMBERS_R103.md AUX-R103-MARGIN, Haiku 4.5 sup.-only minus the lookup (Table 1) | 5 |
| +0.07, [+0.03,+0.12], [+0.04,+0.11] | +0.0742, [+0.0315,+0.1203], [+0.0414,+0.1126] | AUX-R103-MARGIN, Opus 5 sup.-only minus the lookup (Table 1) | 5 |
| 0.64, 0.62, 0.69 | 0.6357, 0.6168, 0.6922 | this file, AUX-R104-CF-FOK, the three models under v2 | 5 |
| 0.54, 0.62 | 0.5433 (Haiku 4.5 retraction, v2), 0.6150 (Opus 5 expiry, v2) | NUMBERS_CF2.md AUX-CF2-PERSTATE / AUX-CF2-OP5 per state (Table 13); the range 'between 0.54 and 0.62' spans 0.5433, 0.5794, 0.5872, 0.6150 | 5 |
| 0.80, 0.87 | 0.7975, 0.8711 | NUMBERS_CF2.md AUX-CF2-ALLSTATES-V3 per state (Table 13) | 5 |
| 0.59 | 0.5869 | NUMBERS_CF2.md, GPT-4.1 mini expiry under v3 (Table 13); this file AUX-R104-EXPIRY | 5 |
| 26 of 30; 4 pairs | counts | this file, AUX-R104-EXPIRY (PN version at or below 0.05 on 26 pairs) | 5, D.2 |
| +0.24, -0.17 | +0.2364, -0.1719 | resp_review/NUMBERS_RESP.md AUX-RESP-L2-MINI-NOK (Table 34) | 6 |
| [+0.04,+0.16], [+0.02,+0.16] | [+0.0415,+0.1554], [+0.0227,+0.1635] | AUX-RESP-L2-MINI-NOK, HYBRID whole (Table 2) | 6 |
| 0.86, 0.53, -0.33, [-0.40,-0.25], [-0.43,-0.22] | 0.8572, 0.5310, -0.3262, [-0.3991,-0.2548], [-0.4327,-0.2167] | AUX-RESP-L1-MINI, supersession-derived (Table 33) | 6 |
| -0.14 | -0.1404 | AUX-RESP-L1-MINI, retraction-derived (Table 33) | 6 |
| 66% | 65.5% | side_experiments/NUMBERS_SIDE.md AUX-SIDE-S2-MINI (the frozen S2-U sentence, 7) | 7 |
| 0.025, 0.006, 0.22, 0.17 | 0.02451, 0.00603, 0.2183, 0.1660 | this file, AUX-R104-DIST, Mem0 blind / indexed variance and mean | 7 |
| 0.0245, 0.0242, 0.0060, 0.0052 | 0.02451, 0.02418, 0.00603, 0.00516 | this file, AUX-R104-DIST, five-decimal variances (Table 26 prints four) | F.7 |
| +0.22 | +0.2167 = 0.7167 - 0.5000 | NUMBERS_CF2.md AUX-CF2-MINI-V2 (Table 1); blind 0.5000 by identity | 8 |
| +0.07, +0.08 | +0.0698, +0.0726, +0.0843 | this file, AUX-R104-MARGIN, the 661 rows (Table 31) | 8 |
| 0.79, 0.70, -0.09 | 0.7864, 0.7003, -0.0861 | this file, AUX-R104-COV-LOOKUP, hard tier (Table 4, Table 32) | 8 |
| 0.78, 0.61, +0.18, [+0.09,+0.25], [+0.10,+0.26] | 0.7835, 0.6083, +0.1752, [+0.0938,+0.2515], [+0.0959,+0.2579] | this file, AUX-R104-COV-LOOKUP, FR-Bank easy tier (Table 4, Table 32) | 8 |
| 62, 0.5962 | 62 of 104 at k = 7 | this file, AUX-R104-REACH (Table 5, Table 36) | 8 |
| 9, 9, 7, 12, 17; 44, 40, 46 | counts over all 104 and all 174 | this file, AUX-R104-REACH, policies over the whole populations (Table 5) | 8 |
| -0.03, [-0.05,-0.01], [-0.07,-0.01] | -0.0287, [-0.0519,-0.0057], [-0.0680,-0.0050] | ds_downstream/NUMBERS_DS.md AUX-DS-PRESENT, DS-P5 (Table 35) | 8 |
| 0.03 | +0.0323 | AUX-R103-MARGIN, Opus 5 all-three minus the lookup (Table 1) | 10 (the box) |
| 40, 104 | counts | side_experiments/NUMBERS_SIDE.md AUX-SIDE-S2-CENSUS (104 TRUE-superseded entries, 40 still active) | 7 |
| 0.56 | 0.5625 | NUMBERS_DS.md DS-P2, the persona-clustered lower bound of the retained share of the oracle gain on the 63 supersession-derived items (the frozen paragraph prints 0.562) | 8 |

## B. Deterministic values (no model call; recorded rows only; exploratory)

Tokens the body prints that already print in v11 in the same form need no row here (reviews/NUMBERS_R102.md and NUMBERS_R103.md carry them).

<!-- GENERATED BELOW: reviews/v12/tools/ledger_r104.py -->

### AUX-R104-COV-LOOKUP — the superseded-section lookup on the coverage tiers, beside GPT-4.1 mini's recorded indexed FOK (Phase 1 item 1; no model call)

Source `reviews/v12/phase1.json` item1 (`reviews/v12/tools/phase1.py`). Populations: `common_e1r.POPULATIONS` R-FOK-FRB (hard tier, FR-Bank), the FR-Bank easy tier (`tier == easy and backend == frbank`), and the pooled easy tier of Table 1 (all backends). The lookup reads the superseded-names section of the committed TRUE summary (`run_nb6.lex_scores` / `emb_scores` on the `sup` field of `run_nb6.build`'s rows; the coverage rows were never scored this way in E1-R, whose FOK-6 read the whole map). Positives are non-ABSENT items. Intervals: persona-clustered single-arm (`boot_cluster_single`) and the paired model-minus-lookup bootstrap (`boot_item` / `boot_cluster`, 1,000 draws, seed 42). Exploratory.

| population | n / pos | monitor blind | monitor indexed (persona CI) | lookup lexical (persona CI) | lookup embedding (persona CI) | sup names / item | model − embedding: Δ, item CI, persona CI | model − lexical: Δ, item CI, persona CI |
|---|---|---:|---|---|---|---:|---|---|
| FR-Bank hard tier (307) | 307 / 35 | 0.4966 | 0.7003 [+0.6361, +0.7598] | 0.5970 [+0.5395, +0.6643] | 0.7864 [+0.6925, +0.8825] | 1.837 | -0.0861 [-0.1879, +0.0305] [-0.1793, +0.0166] | +0.1034 [+0.0162, +0.2022] [+0.0233, +0.1782] |
| FR-Bank easy tier | 354 / 243 | 0.4660 | 0.7835 [+0.7316, +0.8300] | 0.5162 [+0.5037, +0.5307] | 0.6083 [+0.5442, +0.6718] | 1.669 | +0.1752 [+0.0938, +0.2515] [+0.0959, +0.2579] | +0.2673 [+0.2129, +0.3182] [+0.2101, +0.3164] |
| easy tier, all backends | 595 / 463 | 0.4422 | 0.6336 [+0.5834, +0.6756] | 0.5071 [+0.4984, +0.5155] | 0.4021 [+0.3588, +0.4443] | 0.993 | +0.2315 [+0.1628, +0.2979] [+0.1680, +0.2970] | +0.1265 [+0.0694, +0.1771] [+0.0734, +0.1705] |

Reading: on the hard tier the embedding lookup on the superseded section (0.7864) sits above the model (0.7003); the difference of -0.0861 has intervals that include zero, so the model reads no more than that lookup on the tier where every coverage positive is an obligation. The pass's branch rule (lookup within 0.05 of the model on the hard tier) reads **Branch B** on the letter: the point estimate is not within 0.05, in the lookup's favour. On the FR-Bank easy tier the model leads both lookups with intervals excluding zero.

### AUX-R104-CF-FOK — coverage on the counterfactual set from the recorded fok values (Phase 1 item 2; no model call)

Source phase1.json item2_fok_444; the X4 collapse of `cf2/rows/rows_{MINI,H45,OP5}.jsonl` on the `fok` field. Positives are the PRESENT and PN versions (296), negatives the ABSENT version (148). Blind FOK is 0.5000 by the same identity as blind NOK (one blind score per question, reused across its three versions), so each AUROC is also its gain. Persona-clustered single-arm interval. Descriptive.

| reader | summary | AUROC (persona CI) | supersession / retraction / expiry pairs | mean FOK: PRESENT / ABSENT / PN version | distinct values |
|---|---|---|---|---|---:|
| GPT-4.1 mini | v2 | 0.6357 [+0.5972, +0.6770] | 0.6251 / 0.6397 / 0.6675 | 0.4517 / 0.3530 / 0.4966 | 13 |
| GPT-4.1 mini | v3 | 0.6436 [+0.6120, +0.6802] | 0.6357 / 0.6586 / 0.6567 | 0.4926 / 0.3875 / 0.5439 | 12 |
| GPT-4.1 mini | v2r | 0.6371 [+0.6071, +0.6709] | 0.6253 / 0.6389 / 0.6772 | 0.4551 / 0.3503 / 0.4882 | 13 |
| Haiku 4.5 | v2 | 0.6168 [+0.5828, +0.6537] | 0.6157 / 0.6381 / 0.6036 | 0.5130 / 0.4178 / 0.5263 | 44 |
| Haiku 4.5 | v3 | 0.6133 [+0.5816, +0.6522] | 0.6337 / 0.5675 / 0.6103 | 0.5055 / 0.4163 / 0.5180 | 42 |
| Haiku 4.5 | v2r | 0.6050 [+0.5713, +0.6416] | 0.5951 / 0.6481 / 0.5950 | 0.5072 / 0.4231 / 0.5180 | 38 |
| Opus 5 | v2 | 0.6922 [+0.6576, +0.7353] | 0.7084 / 0.6539 / 0.6772 | 0.7746 / 0.6604 / 0.8369 | 200 |
| Opus 5 | v3 | 0.7098 [+0.6763, +0.7535] | 0.7103 / 0.7031 / 0.7156 | 0.7818 / 0.6637 / 0.8567 | 196 |
| Opus 5 | v2r | 0.6894 [+0.6572, +0.7299] | 0.6959 / 0.6883 / 0.6842 | 0.7741 / 0.6633 / 0.8386 | 197 |

### AUX-R104-MARGIN — model minus lookup, both lookup variants, whole populations, with both intervals (Phase 1 item 3; no model call)

Source phase1.json item3_444_margins, item3_444_lookups, item3_661. On the 444 the lookups are `score_cf.matcher` (embedding, `sentence-transformers/all-MiniLM-L6-v2`) and the Jaccard lexical lookup (`run_nb6.lex_scores`) on the superseded section of v2 and on the three sections of v3 (`index_v3.named_sections`); each model's recorded arm against the lookup on the same summary. On the 661 the models are GPT-4.1 mini's committed INDEXED-TRUE `nok` and the X4 expansion rows of GPT-5.6 Luna, Opus 5 and Haiku 4.5 (`r74/x4/rows_*.jsonl` through `x4_score.load_lane`), against the two lookups on the committed TRUE section (gate 0.7484 / 0.5738 reproduced). Item-level paired bootstrap primary, persona-clustered beside. Exploratory.

| population | lookup, summary | AUROC (persona CI) | supersession / retraction / expiry |
|---|---|---|---|
| 444 | embedding-v2 | 0.7663 [+0.7226, +0.8051] | 0.9223 / 0.5000 / 0.5000 |
| 444 | embedding-v3 | 0.8756 [+0.8391, +0.9111] | 0.8995 / 0.7975 / 0.8711 |
| 444 | lexical-v2 | 0.6698 [+0.6226, +0.7145] | 0.7829 / 0.5000 / 0.5000 |
| 444 | lexical-v3 | 0.8085 [+0.7619, +0.8486] | 0.7829 / 0.8617 / 0.8244 |
| 661 | lexical, superseded section | 0.5738 [+0.5273, +0.6282] | 0.6241 / 0.4964 / 0.4964 |
| 661 | embedding, superseded section | 0.7484 [+0.6636, +0.8298] | 0.9534 / 0.4053 / 0.4823 |

| population | model, summary minus lookup | model | lookup | model − lookup | item CI | persona CI | both exclude zero | point inside ±0.05 |
|---|---|---:|---:|---:|---|---|---|---|
| 444 | GPT-4.1 mini (v2) minus embedding lookup (v2) | 0.7167 | 0.7663 | -0.0496 | [-0.1012, +0.0013] | [-0.0933, -0.0054] | no | yes |
| 444 | GPT-4.1 mini (v2) minus lexical lookup (v2) | 0.7167 | 0.6698 | +0.0469 | [+0.0037, +0.0925] | [+0.0037, +0.0895] | yes | yes |
| 444 | GPT-4.1 mini (v3) minus embedding lookup (v3) | 0.7967 | 0.8756 | -0.0789 | [-0.1229, -0.0344] | [-0.1283, -0.0334] | yes | no |
| 444 | GPT-4.1 mini (v3) minus lexical lookup (v3) | 0.7967 | 0.8085 | -0.0117 | [-0.0591, +0.0360] | [-0.0566, +0.0294] | no | yes |
| 444 | Haiku 4.5 (v2) minus embedding lookup (v2) | 0.7566 | 0.7663 | -0.0098 | [-0.0640, +0.0398] | [-0.0494, +0.0336] | no | yes |
| 444 | Haiku 4.5 (v2) minus lexical lookup (v2) | 0.7566 | 0.6698 | +0.0868 | [+0.0405, +0.1299] | [+0.0476, +0.1274] | yes | no |
| 444 | Haiku 4.5 (v3) minus embedding lookup (v3) | 0.8773 | 0.8756 | +0.0017 | [-0.0326, +0.0361] | [-0.0312, +0.0320] | no | yes |
| 444 | Haiku 4.5 (v3) minus lexical lookup (v3) | 0.8773 | 0.8085 | +0.0689 | [+0.0283, +0.1087] | [+0.0321, +0.1046] | yes | no |
| 444 | Opus 5 (v2) minus embedding lookup (v2) | 0.8405 | 0.7663 | +0.0742 | [+0.0315, +0.1203] | [+0.0414, +0.1126] | yes | no |
| 444 | Opus 5 (v2) minus lexical lookup (v2) | 0.8405 | 0.6698 | +0.1707 | [+0.1314, +0.2102] | [+0.1317, +0.2118] | yes | no |
| 444 | Opus 5 (v3) minus embedding lookup (v3) | 0.9079 | 0.8756 | +0.0323 | [+0.0060, +0.0617] | [+0.0077, +0.0608] | yes | yes |
| 444 | Opus 5 (v3) minus lexical lookup (v3) | 0.9079 | 0.8085 | +0.0994 | [+0.0602, +0.1409] | [+0.0545, +0.1451] | yes | no |
| 661 | GPT-4.1 mini (committed) minus embedding lookup | 0.7339 | 0.7484 | -0.0145 | [-0.0769, +0.0549] | [-0.1080, +0.0765] | no | yes |
| 661 | GPT-4.1 mini (committed) minus lexical lookup | 0.7339 | 0.5738 | +0.1601 | [+0.1086, +0.2153] | [+0.0676, +0.2585] | yes | no |
| 661 | GPT-5.6 Luna minus embedding lookup | 0.8182 | 0.7484 | +0.0698 | [+0.0123, +0.1264] | [-0.0180, +0.1520] | no | no |
| 661 | GPT-5.6 Luna minus lexical lookup | 0.8182 | 0.5738 | +0.2444 | [+0.1977, +0.2888] | [+0.1655, +0.3197] | yes | no |
| 661 | Haiku 4.5 minus embedding lookup | 0.8210 | 0.7484 | +0.0726 | [+0.0052, +0.1393] | [-0.0143, +0.1634] | no | no |
| 661 | Haiku 4.5 minus lexical lookup | 0.8210 | 0.5738 | +0.2473 | [+0.1993, +0.2933] | [+0.1747, +0.3178] | yes | no |
| 661 | Opus 5 minus embedding lookup | 0.8327 | 0.7484 | +0.0843 | [+0.0182, +0.1448] | [-0.0091, +0.1759] | no | no |
| 661 | Opus 5 minus lexical lookup | 0.8327 | 0.5738 | +0.2589 | [+0.2195, +0.2987] | [+0.1935, +0.3199] | yes | no |

### AUX-R104-REACH — reach of the forbidding record by ranking depth, and the downstream rates over all 104 and all 174 (Phase 1 item 4; no model call)

Source phase1.json item4: `resp_review/l2/retrieval.json` `best_rank` over the 104 obligation items (a census; the recorded ranking is ten deep, so k > 10 is not defined); `ds_downstream/stage1.json` view sizes on the 104; `ds_downstream/run/scores_ds.json` and `scores_amend1.json` per policy, with the stale-use and correctness counts divided by the whole population (104 obligations; 174 PRESENT items) rather than by the answered subset. The 0.80 detector endpoint reads zero under every policy and is uninformative (NUMBERS_DS.md reading note).

| k | reach (of 104) | rate | supersession (of 63) | retraction (of 26) | expiry (of 15) |
|---:|---:|---:|---:|---:|---:|
| 5 | 54 | 0.5192 | 22 | 20 | 12 |
| 6 | 60 | 0.5769 | 25 | 23 | 12 |
| 7 | 62 | 0.5962 | 27 | 23 | 12 |
| 8 | 69 | 0.6635 | 32 | 25 | 12 |
| 9 | 70 | 0.6731 | 33 | 25 | 12 |
| 10 | 74 | 0.7115 | 37 | 25 | 12 |

| policy | mean view size on the 104 | median | max |
|---|---:|---:|---:|
| ALWAYS | 5.00 | 5 | 5 |
| LOOKUP | 6.88 | 5 | 13 |
| LOOKUP-ALL | 10.36 | 8.5 | 27 |
| LOOKUP-LIT | 7.42 | 7 | 13 |
| MODEL | 7.08 | 6 | 13 |
| MODEL-ALL | 10.74 | 10 | 27 |
| ORACLE | 7.07 | 7 | 13 |

Matched budget: gated mean view size 7.08 (model) / 6.88 (lookup) on the 104 -> k = 7; MODEL-ALL 10.74 and MODEL-ALL-V3 11.42 exceed the recorded ranking depth of 10, so k = 10 is the nearest matched row.

| policy | obligations answered | stale at 0.50 (count) | stale at 0.50 over all 104 | stale at 0.80 over all 104 | PRESENT answered | correct at 0.50 (count) | correct over all 174 | stale at 0.50 tagged / untagged (of answered) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| ALWAYS | 54 | 9 | 0.0865 | 0.0000 | 174 | 46 | 0.2644 | 2 of 35 / 7 of 19 |
| LOOKUP | 70 | 7 | 0.0673 | 0.0000 | 146 | 40 | 0.2299 | 5 of 61 / 2 of 9 |
| LOOKUP-ALL | 70 | 6 | 0.0577 | 0.0000 | 146 | 39 | 0.2241 | 4 of 61 / 2 of 9 |
| MODEL | 74 | 9 | 0.0865 | 0.0000 | 155 | 44 | 0.2529 | 5 of 61 / 4 of 13 |
| MODEL-ALL | 74 | 9 | 0.0865 | 0.0000 | 155 | 44 | 0.2529 | 5 of 61 / 4 of 13 |
| ORACLE | 99 | 17 | 0.1635 | 0.0000 | 174 | 46 | 0.2644 | 11 of 82 / 6 of 17 |

### AUX-R104-DIST — score distribution of GPT-4.1 mini's coverage score on the two structureless stores, blind against indexed (Phase 1 item 5; no model call)

Source phase1.json item5; the recorded rows of `e1_metamemory/elicitation_main.json` (arms BLIND, INDEXED-TRUE, INDEXED-BELIEVED) on the scoreable Mem0 (238) and A-MEM (284) items. Descriptive.

| store | arm | distinct values | values (count) | mean | variance | share at the mode | AUROC | mean on positives / negatives |
|---|---|---:|---|---:|---:|---:|---:|---|
| Mem0 | blind | 6 | 0.0: 8, 0.05: 1, 0.1: 100, 0.2: 62, 0.4: 58, 0.7: 9 | 0.2183 | 0.02451 | 0.4202 | 0.5746 | 0.2202 / 0.2170 |
| Mem0 | indexed_TRUE | 5 | 0.05: 2, 0.1: 105, 0.15: 6, 0.2: 110, 0.4: 15 | 0.1660 | 0.00603 | 0.4622 | 0.4777 | 0.1617 / 0.1688 |
| Mem0 | indexed_BELIEVED | 7 | 0.0: 1, 0.05: 2, 0.1: 123, 0.15: 7, 0.2: 97, 0.4: 7, 0.7: 1 | 0.1527 | 0.00559 | 0.5168 | 0.5741 | — |
| Mem0 | items indexed < blind / = / > | 86 / 106 / 46 | | | | | | |
| A-MEM | blind | 6 | 0.0: 9, 0.05: 1, 0.1: 114, 0.2: 75, 0.4: 75, 0.7: 10 | 0.2234 | 0.02418 | 0.4014 | 0.5591 | 0.2230 / 0.2237 |
| A-MEM | indexed_TRUE | 5 | 0.05: 3, 0.1: 130, 0.15: 6, 0.2: 132, 0.4: 13 | 0.1607 | 0.00516 | 0.4648 | 0.4526 | 0.1544 / 0.1658 |
| A-MEM | indexed_BELIEVED | 5 | 0.05: 13, 0.1: 183, 0.15: 1, 0.2: 85, 0.4: 2 | 0.1299 | 0.00285 | 0.6444 | 0.5278 | — |
| A-MEM | items indexed < blind / = / > | 110 / 126 / 48 | | | | | | |

### AUX-R104-EXPIRY — GPT-4.1 mini's 30 expiry pairs under the all-states summary on the counterfactual set (Phase 1 item 6; no model call)

Source phase1.json item6_mini_expiry_v3 (`cf2/rows/rows_MINI.jsonl`, arm INDEXED-V3, beside INDEXED-V2). Every expiry question carries the UPCOMING intent. Mean `nok` by version under v3: PN 0.1367, PRESENT 0.0667, ABSENT 0.0483; the PN version scores above its PRESENT version in 7 of 30 pairs, equal in 18, below in 5; above ABSENT in 10, equal in 19, below in 1. Distinct PN values under v3: 0, 0.05, 0.4, 0.6, 0.7. Expiry AUROC on the 90 items: v2 0.5489, v3 0.5869.

| pair | v3: PN / PRESENT / ABSENT | v2: PN / PRESENT / ABSENT | expired names printed, PN / PRESENT version | question |
|---|---|---|---|---|
| cf2:aisha:preparation_for_meeting | 0.05 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 6 / 5 | What materials do I need to prepare for my upcoming meeting? |
| cf2:aisha:upcoming_meeting | 0.70 / 0.05 / 0.05 | 0.05 / 0.05 / 0.05 | 6 / 5 | Who am I meeting with in my next scheduled meeting? |
| cf2:billy:project_aircraft:aerial_wildlife_survey | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 6 / 4 | What preparations are planned for the coming aerial wildlife survey in the project aircraft? |
| cf2:callum:accommodation_option:conference | 0.40 / 0.00 / 0.05 | 0.00 / 0.00 / 0.00 | 4 / 2 | Can you tell me about the accommodation arrangements for my next conference? |
| cf2:callum:accommodation_plan | 0.40 / 0.10 / 0.05 | 0.05 / 0.05 / 0.05 | 4 / 2 | What details are in my upcoming accommodation plan, Callum? |
| cf2:dariush:annual_event:Nowruz_dinner_guest_count | 0.00 / 0.00 / 0.00 | 0.05 / 0.00 / 0.05 | 4 / 3 | How many guests are coming to the Nowruz dinner this year? |
| cf2:dariush:trip:Isfahan | 0.00 / 0.00 / 0.00 | 0.05 / 0.00 / 0.05 | 4 / 3 | Can you tell me the schedule for my next trip to Isfahan? |
| cf2:dariush:trip_duration:Isfahan | 0.00 / 0.00 / 0.00 | 0.05 / 0.00 / 0.00 | 5 / 3 | What is the duration of my next trip to Isfahan? |
| cf2:david:coaching_event_date | 0.00 / 0.00 / 0.00 | 0.00 / 0.05 / 0.00 | 10 / 8 | What day is my next coaching event coming up, David Park? |
| cf2:david:project:debate_coaching_teams_qualified | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 9 / 8 | What are the names of the debate coaching teams scheduled to be qualified soon? |
| cf2:diane:emotional_state:nervous_about_greg_show | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 8 / 6 | How nervous am I feeling about the upcoming Greg show? |
| cf2:diane:relationship:greg_project_folk_art_center | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 8 / 6 | What are the upcoming plans for my collaboration with Greg on the project at the Folk Art Center? |
| cf2:elena:event:wedding_timeline | 0.05 / 0.05 / 0.05 | 0.05 / 0.10 / 0.10 | 8 / 6 | What are the key events on my upcoming wedding timeline? |
| cf2:elena:health_aid:light_therapy_lamp | 0.00 / 0.05 / 0.00 | 0.00 / 0.00 / 0.00 | 7 / 6 | When is the light therapy lamp scheduled for me next? |
| cf2:elena:wedding_date | 0.05 / 0.05 / 0.00 | 0.05 / 0.05 / 0.00 | 7 / 6 | Can you tell me the date scheduled for my wedding? |
| cf2:fatima:personal_day_activity | 0.05 / 0.05 / 0.05 | 0.05 / 0.05 / 0.05 | 4 / 3 | What personal activities do I have coming up today, Fatima? |
| cf2:fatima:trip:Milan April 2026 | 0.05 / 0.05 / 0.00 | 0.00 / 0.00 / 0.00 | 6 / 3 | Can you tell me the itinerary for my Milan trip scheduled for April 2026? |
| cf2:fatima:trip_schedule:salone_del_mobile_2026 | 0.40 / 0.40 / 0.40 | 0.05 / 0.05 / 0.00 | 4 / 3 | Can you tell me the itinerary details for my upcoming Salone del Mobile 2026 visit? |
| cf2:jake:project:lake_trip_presidents_day_weekend | 0.05 / 0.05 / 0.05 | 0.00 / 0.05 / 0.00 | 7 / 5 | What details do I have for the upcoming lake trip over Presidents Day weekend? |
| cf2:jake:project_role:lake_trip | 0.00 / 0.05 / 0.00 | 0.00 / 0.00 / 0.00 | 7 / 5 | What part am I playing in the scheduled lake trip? |
| cf2:jerome:project:Disney trip with Naomi | 0.05 / 0.00 / 0.05 | 0.05 / 0.05 / 0.05 | 7 / 6 | Can you tell me the schedule for the Disney trip with Naomi that's coming up? |
| cf2:kofi:preparation_for_meeting | 0.05 / 0.05 / 0.05 | 0.05 / 0.05 / 0.05 | 2 / 1 | What tasks are scheduled for me to complete before the coming meeting? |
| cf2:marcus:budget:kayla_graduation_celebration | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 4 / 3 | How much have I allocated for Kayla's graduation party that's coming up? |
| cf2:marcus:event:Kayla_graduation_party | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 8 / 3 | What time is Kayla's graduation party coming up? |
| cf2:marcus:event_space_capacity | 0.70 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 4 / 3 | What is the capacity of the event space for my upcoming event? |
| cf2:marley:event_transportation | 0.60 / 0.05 / 0.05 | 0.05 / 0.00 / 0.00 | 5 / 4 | What transportation is arranged for my upcoming events? |
| cf2:marley:graduation_guest_tickets | 0.05 / 0.05 / 0.00 | 0.05 / 0.05 / 0.00 | 5 / 4 | How many graduation guest tickets do I have for the upcoming ceremony? |
| cf2:mehmet:preparation:barber_trade_guild_annual_meeting | 0.00 / 0.05 / 0.00 | 0.00 / 0.00 / 0.00 | 4 / 2 | What items or documents should I bring to the coming barber trade guild annual meeting? |
| cf2:mehmet:project:air_conditioning_installation | 0.05 / 0.30 / 0.00 | 0.00 / 0.00 / 0.00 | 3 / 2 | What are the details of my upcoming air conditioning installation project? |
| cf2:pan:product_plan_songkran | 0.40 / 0.60 / 0.60 | 0.40 / 0.40 / 0.60 | 3 / 2 | What is planned next for my Songkran product project? |

### AUX-R104-DETSAMPLE — the detector-validation sample (Phase 1 item 9; no model call)

Source phase1.json item9; `reviews/v12/detector_sample.json` (the 100 rows), `detector_sample_key.json` (the detector's flags, withheld from the sheet), `DETECTOR_LABELING_SHEET.md`, `tools/detector_agreement.py`. 655 recorded answer rows collapse to 443 distinct (item, view) pairs; strata (label | tag status | policy group) and quota: PRESENT-NEGATIVE|tagged|always: 35 available, 14 drawn; PRESENT-NEGATIVE|tagged|gated: 119 available, 13 drawn; PRESENT-NEGATIVE|tagged|oracle: 43 available, 13 drawn; PRESENT-NEGATIVE|untagged|always: 19 available, 14 drawn; PRESENT-NEGATIVE|untagged|gated: 8 available, 8 drawn; PRESENT-NEGATIVE|untagged|oracle: 8 available, 8 drawn; PRESENT|present|always: 174 available, 15 drawn; PRESENT|present|gated: 37 available, 15 drawn. Drawn under seed 42: PRESENT-NEGATIVE|tagged 40, PRESENT-NEGATIVE|untagged 30, PRESENT|present 30.

