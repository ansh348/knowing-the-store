# NUMBERS_R139.md: the R139 pass (mock review 14, W1 and W2: equivalence within 0.05 and the length-only reader; 2026-09-22)

Written by `reviews/r139/tools/ledger_r139.py` from `reviews/r139/results/equiv_r139.json` (`equiv_r139.py`) and `reviews/r139/results/length_r139.json` (`length_r139.py`). Both analyses are post hoc (the R139 POSTHOC block of CLAIMS.md). The branch texts were committed before either script ran (`reviews/r139/BRANCHES_R139.md`, 6616e57). No model call; no API call; every input is a stored score, a stored vector or a stored prompt text.

## AUX-R139-EQUIV: equivalence within 0.05 (two one-sided tests at 5%), every printed model-minus-lookup row of the five Phase 0.3 conditions, plus the B6 row

Rule: equivalent within 0.05: both 90% intervals inside [-0.05, +0.05] (two one-sided tests at 5%); reliable: both 95% intervals exclude zero; neither: 'neither shown nor excluded'. The 90% intervals are the 5th and 95th percentiles of the SAME 1000 draws (seed 42) whose 2.5th and 97.5th percentiles are the printed 95% intervals: the shared summaries `common_e1r._summarise` and `r125_common._summarise` are wrapped at run time (the modules are not edited). Every recomputed 95% interval equals its stored source to 5e-5: 105 of 105 (the three B6 rows are new and have no stored source). Pooled rows: item-level and persona-grouped intervals; matched rows: triple-level and persona-grouped. Both verdicts can be false at once ('neither shown nor excluded').

| condition | table | reader | scope | metric | difference | 95% item/triple | 95% persona | 90% item/triple | 90% persona | reliable | equivalent | reading |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|
| default summary | tab:cf-matched-vs | GPT-4.1 mini, one draw | whole | matched | -0.0372 | [-0.0811, +0.0068] | [-0.0877, +0.0146] | [-0.0743, -0.0034] | [-0.0800, +0.0070] | no | no | neither shown nor excluded |
| default summary | tab:cf-matched-vs | GPT-4.1 mini, one draw | supersession | matched | -0.0852 | [-0.1307, -0.0398] | [-0.1420, -0.0294] | [-0.1250, -0.0509] | [-0.1330, -0.0372] | yes | no | reliable |
| default summary | tab:cf-matched-vs | GPT-4.1 mini, five draws | whole | matched | -0.0507 | [-0.1115, +0.0101] | [-0.1069, +0.0000] | [-0.1014, -0.0034] | [-0.0992, -0.0063] | no | no | neither shown nor excluded |
| default summary | tab:cf-matched-vs | GPT-4.1 mini, five draws | supersession | matched | -0.0739 | [-0.1307, -0.0227] | [-0.1393, -0.0214] | [-0.1193, -0.0284] | [-0.1304, -0.0294] | yes | no | reliable |
| default summary | tab:cf-matched-vs | Haiku 4.5 | whole | matched | +0.0000 | [-0.0439, +0.0372] | [-0.0528, +0.0483] | [-0.0372, +0.0338] | [-0.0437, +0.0420] | no | yes | equivalent within 0.05 |
| default summary | tab:cf-matched-vs | Haiku 4.5 | supersession | matched | -0.0511 | [-0.1136, +0.0000] | [-0.1084, +0.0000] | [-0.0966, -0.0114] | [-0.0988, -0.0066] | no | no | neither shown nor excluded |
| default summary | tab:cf-matched-vs | GPT-5.6 Luna | whole | matched | +0.1014 | [+0.0473, +0.1554] | [+0.0442, +0.1533] | [+0.0574, +0.1453] | [+0.0530, +0.1449] | yes | no | reliable |
| default summary | tab:cf-matched-vs | GPT-5.6 Luna | supersession | matched | -0.0057 | [-0.0341, +0.0227] | [-0.0321, +0.0174] | [-0.0284, +0.0227] | [-0.0291, +0.0150] | no | yes | equivalent within 0.05 |
| default summary | tab:cf-matched-vs | GPT-5.6 Sol | whole | matched | +0.0811 | [+0.0270, +0.1351] | [+0.0283, +0.1319] | [+0.0372, +0.1284] | [+0.0362, +0.1218] | yes | no | reliable |
| default summary | tab:cf-matched-vs | GPT-5.6 Sol | supersession | matched | -0.0057 | [-0.0511, +0.0341] | [-0.0417, +0.0287] | [-0.0455, +0.0284] | [-0.0372, +0.0230] | no | yes | equivalent within 0.05 |
| default summary | tab:cf-matched-vs | Opus 5 | whole | matched | +0.0980 | [+0.0472, +0.1454] | [+0.0435, +0.1503] | [+0.0541, +0.1387] | [+0.0526, +0.1444] | yes | no | reliable |
| default summary | tab:cf-matched-vs | Opus 5 | supersession | matched | +0.0114 | [-0.0227, +0.0455] | [-0.0284, +0.0579] | [-0.0170, +0.0398] | [-0.0222, +0.0495] | no | yes | equivalent within 0.05 |
| all-states summary | tab:cf-matched-vs | GPT-4.1 mini, five draws | whole | matched | -0.0135 | [-0.0642, +0.0338] | [-0.0698, +0.0375] | [-0.0541, +0.0270] | [-0.0577, +0.0289] | no | no | neither shown nor excluded |
| all-states summary | tab:cf-matched-vs | GPT-4.1 mini, five draws | supersession | matched | -0.0227 | [-0.0795, +0.0342] | [-0.0886, +0.0337] | [-0.0685, +0.0284] | [-0.0778, +0.0266] | no | no | neither shown nor excluded |
| all-states summary | tab:cf-matched-vs | Haiku 4.5 | whole | matched | -0.0034 | [-0.0439, +0.0372] | [-0.0476, +0.0333] | [-0.0372, +0.0304] | [-0.0402, +0.0283] | no | yes | equivalent within 0.05 |
| all-states summary | tab:cf-matched-vs | Haiku 4.5 | supersession | matched | -0.0511 | [-0.1080, +0.0000] | [-0.1123, +0.0054] | [-0.0966, -0.0057] | [-0.1001, -0.0057] | no | no | neither shown nor excluded |
| all-states summary | tab:cf-matched-vs | Opus 5 | whole | matched | +0.0304 | [-0.0068, +0.0643] | [-0.0038, +0.0648] | [+0.0000, +0.0608] | [+0.0000, +0.0599] | no | no | neither shown nor excluded |
| all-states summary | tab:cf-matched-vs | Opus 5 | supersession | matched | +0.0227 | [-0.0114, +0.0568] | [-0.0105, +0.0550] | [-0.0057, +0.0511] | [-0.0056, +0.0500] | no | no | neither shown nor excluded |
| all-states summary | tab:cf-matched-vs | Opus 5, draw 1 | whole | matched | +0.0372 | [+0.0033, +0.0709] | [+0.0076, +0.0662] | [+0.0068, +0.0642] | [+0.0133, +0.0621] | yes | no | reliable |
| all-states summary | tab:cf-matched-vs | Opus 5, draw 1 | supersession | matched | +0.0398 | [+0.0170, +0.0682] | [+0.0118, +0.0714] | [+0.0170, +0.0625] | [+0.0167, +0.0650] | yes | no | reliable |
| B6: lookup with one count feature | tab:cf-hybrid (new row) | count-feature lookup minus GPT-5.6 Luna | whole | matched | +0.0068 | [-0.0507, +0.0642] | [-0.0536, +0.0659] | [-0.0405, +0.0541] | [-0.0431, +0.0568] | no | no | neither shown nor excluded |
| B6: lookup with one count feature | tab:cf-hybrid (new row) | count-feature lookup minus GPT-5.6 Sol | whole | matched | +0.0270 | [-0.0203, +0.0812] | [-0.0175, +0.0737] | [-0.0169, +0.0709] | [-0.0104, +0.0658] | no | no | neither shown nor excluded |
| B6: lookup with one count feature | tab:cf-hybrid (new row) | count-feature lookup minus Opus 5 | whole | matched | +0.0101 | [-0.0439, +0.0676] | [-0.0563, +0.0733] | [-0.0338, +0.0608] | [-0.0438, +0.0642] | no | no | neither shown nor excluded |
| default summary | tab:sup-margins | GPT-4.1 mini, one draw | supersession | pooled | -0.0915 | [-0.1399, -0.0478] | [-0.1436, -0.0425] | [-0.1310, -0.0550] | [-0.1381, -0.0487] | yes | no | reliable |
| all-states summary | Table 1 (tab:cf-main) | Opus 5 | whole | pooled | +0.0323 | [+0.0060, +0.0617] | [+0.0077, +0.0608] | [+0.0087, +0.0569] | [+0.0118, +0.0554] | yes | no | reliable |
| padded set | tab:cfpad-minus-lookup (padded panel) | GPT-4.1 mini, five draws | supersession | pooled | -0.0525 | [-0.1065, +0.0041] | [-0.1092, +0.0058] | [-0.0981, -0.0031] | [-0.1000, -0.0064] | no | no | neither shown nor excluded |
| padded set | tab:cfpad-minus-lookup (padded panel) | GPT-4.1 mini, five draws | supersession | matched | -0.0455 | [-0.1307, +0.0455] | [-0.1461, +0.0450] | [-0.1193, +0.0284] | [-0.1329, +0.0345] | no | no | neither shown nor excluded |
| padded set | tab:cfpad-whole (padded panel) | GPT-4.1 mini, five draws | whole | pooled | -0.0165 | [-0.0699, +0.0359] | [-0.0541, +0.0207] | [-0.0615, +0.0295] | [-0.0486, +0.0136] | no | no | neither shown nor excluded |
| padded set | tab:cfpad-whole (padded panel) | GPT-4.1 mini, five draws | whole | matched | +0.0169 | [-0.0541, +0.0878] | [-0.0578, +0.0743] | [-0.0439, +0.0745] | [-0.0455, +0.0684] | no | no | neither shown nor excluded |
| default summary | tab:cfpad-minus-lookup (unpadded panel) | GPT-4.1 mini, five draws | supersession | pooled | -0.0429 | [-0.0898, +0.0006] | [-0.1001, +0.0035] | [-0.0818, -0.0074] | [-0.0896, -0.0038] | no | no | neither shown nor excluded |
| default summary | tab:cfpad-whole (unpadded panel) | GPT-4.1 mini, five draws | whole | pooled | -0.0016 | [-0.0426, +0.0393] | [-0.0415, +0.0328] | [-0.0371, +0.0316] | [-0.0343, +0.0278] | no | yes | equivalent within 0.05 |
| padded set | tab:cfpad-minus-lookup (padded panel) | Haiku 4.5 | supersession | pooled | -0.0062 | [-0.0652, +0.0515] | [-0.0558, +0.0464] | [-0.0550, +0.0437] | [-0.0497, +0.0378] | no | no | neither shown nor excluded |
| padded set | tab:cfpad-minus-lookup (padded panel) | Haiku 4.5 | supersession | matched | -0.0284 | [-0.0852, +0.0341] | [-0.0805, +0.0294] | [-0.0795, +0.0227] | [-0.0722, +0.0195] | no | no | neither shown nor excluded |
| padded set | tab:cfpad-whole (padded panel) | Haiku 4.5 | whole | pooled | +0.0055 | [-0.0462, +0.0538] | [-0.0278, +0.0447] | [-0.0395, +0.0453] | [-0.0232, +0.0390] | no | yes | equivalent within 0.05 |
| padded set | tab:cfpad-whole (padded panel) | Haiku 4.5 | whole | matched | -0.0439 | [-0.0981, +0.0068] | [-0.0896, +0.0031] | [-0.0880, +0.0000] | [-0.0820, -0.0068] | no | no | neither shown nor excluded |
| default summary | tab:cfpad-minus-lookup (unpadded panel) | Haiku 4.5 | supersession | pooled | -0.0347 | [-0.0813, +0.0086] | [-0.0809, +0.0066] | [-0.0727, +0.0014] | [-0.0706, -0.0017] | no | no | neither shown nor excluded |
| default summary | tab:cfpad-whole (unpadded panel) | Haiku 4.5 | whole | pooled | -0.0098 | [-0.0640, +0.0398] | [-0.0494, +0.0336] | [-0.0527, +0.0320] | [-0.0448, +0.0262] | no | no | neither shown nor excluded |
| padded set | tab:cfpad-minus-lookup (padded panel) | GPT-5.6 Luna | supersession | pooled | +0.1375 | [+0.0883, +0.1934] | [+0.0971, +0.1777] | [+0.0980, +0.1838] | [+0.1016, +0.1722] | yes | no | reliable |
| padded set | tab:cfpad-minus-lookup (padded panel) | GPT-5.6 Luna | supersession | matched | +0.1023 | [+0.0398, +0.1648] | [+0.0482, +0.1552] | [+0.0511, +0.1534] | [+0.0561, +0.1468] | yes | no | reliable |
| padded set | tab:cfpad-whole (padded panel) | GPT-5.6 Luna | whole | pooled | +0.0921 | [+0.0450, +0.1438] | [+0.0572, +0.1277] | [+0.0510, +0.1348] | [+0.0640, +0.1237] | yes | no | reliable |
| padded set | tab:cfpad-whole (padded panel) | GPT-5.6 Luna | whole | matched | +0.1689 | [+0.1115, +0.2297] | [+0.1102, +0.2245] | [+0.1182, +0.2196] | [+0.1172, +0.2177] | yes | no | reliable |
| default summary | tab:cfpad-minus-lookup (unpadded panel) | GPT-5.6 Luna | supersession | pooled | +0.0204 | [-0.0053, +0.0473] | [-0.0056, +0.0451] | [-0.0003, +0.0429] | [-0.0021, +0.0403] | no | yes | equivalent within 0.05 |
| default summary | tab:cfpad-whole (unpadded panel) | GPT-5.6 Luna | whole | pooled | +0.0754 | [+0.0339, +0.1216] | [+0.0450, +0.1090] | [+0.0407, +0.1127] | [+0.0505, +0.1038] | yes | no | reliable |
| padded set | tab:cfpad-minus-lookup (padded panel) | GPT-5.6 Sol | supersession | pooled | +0.1274 | [+0.0726, +0.1837] | [+0.0802, +0.1726] | [+0.0821, +0.1763] | [+0.0883, +0.1653] | yes | no | reliable |
| padded set | tab:cfpad-minus-lookup (padded panel) | GPT-5.6 Sol | supersession | matched | +0.0909 | [+0.0227, +0.1477] | [+0.0341, +0.1519] | [+0.0398, +0.1420] | [+0.0426, +0.1453] | yes | no | reliable |
| padded set | tab:cfpad-whole (padded panel) | GPT-5.6 Sol | whole | pooled | +0.1007 | [+0.0516, +0.1531] | [+0.0629, +0.1413] | [+0.0583, +0.1443] | [+0.0696, +0.1338] | yes | no | reliable |
| padded set | tab:cfpad-whole (padded panel) | GPT-5.6 Sol | whole | matched | +0.0676 | [+0.0000, +0.1318] | [+0.0096, +0.1241] | [+0.0135, +0.1184] | [+0.0170, +0.1151] | no | no | neither shown nor excluded |
| default summary | tab:cfpad-minus-lookup (unpadded panel) | GPT-5.6 Sol | supersession | pooled | +0.0161 | [-0.0130, +0.0473] | [-0.0202, +0.0478] | [-0.0082, +0.0424] | [-0.0109, +0.0411] | no | yes | equivalent within 0.05 |
| default summary | tab:cfpad-whole (unpadded panel) | GPT-5.6 Sol | whole | pooled | +0.0836 | [+0.0401, +0.1315] | [+0.0544, +0.1163] | [+0.0487, +0.1243] | [+0.0578, +0.1110] | yes | no | reliable |
| padded set | tab:cfpad-minus-lookup (padded panel) | Opus 5 | supersession | pooled | -0.0336 | [-0.1070, +0.0448] | [-0.1597, +0.0748] | [-0.0930, +0.0315] | [-0.1444, +0.0614] | no | no | neither shown nor excluded |
| padded set | tab:cfpad-minus-lookup (padded panel) | Opus 5 | supersession | matched | -0.0455 | [-0.1420, +0.0398] | [-0.1845, +0.0756] | [-0.1253, +0.0227] | [-0.1596, +0.0585] | no | no | neither shown nor excluded |
| padded set | tab:cfpad-whole (padded panel) | Opus 5 | whole | pooled | +0.0057 | [-0.0538, +0.0711] | [-0.0780, +0.0847] | [-0.0455, +0.0582] | [-0.0624, +0.0717] | no | no | neither shown nor excluded |
| padded set | tab:cfpad-whole (padded panel) | Opus 5 | whole | matched | +0.0135 | [-0.0574, +0.0845] | [-0.0868, +0.1084] | [-0.0439, +0.0743] | [-0.0684, +0.0946] | no | no | neither shown nor excluded |
| default summary | tab:cfpad-minus-lookup (unpadded panel) | Opus 5 | supersession | pooled | +0.0102 | [-0.0183, +0.0392] | [-0.0259, +0.0432] | [-0.0143, +0.0352] | [-0.0190, +0.0382] | no | yes | equivalent within 0.05 |
| default summary | tab:cfpad-whole (unpadded panel) | Opus 5 | whole | pooled | +0.0742 | [+0.0315, +0.1203] | [+0.0414, +0.1126] | [+0.0378, +0.1139] | [+0.0461, +0.1063] | yes | no | reliable |
| sibling-name control | tab:cf-sibling | GPT-4.1 mini (five draws) | supersession (PN vs sibling) | matched | -0.0455 | [-0.1136, +0.0170] | [-0.1112, +0.0115] | [-0.1023, +0.0057] | [-0.1001, +0.0051] | no | no | neither shown nor excluded |
| sibling-name control | tab:cf-sibling | Haiku 4.5 (five draws) | supersession (PN vs sibling) | matched | -0.0682 | [-0.1364, +0.0000] | [-0.1266, +0.0000] | [-0.1250, -0.0114] | [-0.1176, -0.0118] | no | no | neither shown nor excluded |
| sibling-name control | tab:cf-sibling | GPT-5.6 Luna (five draws) | supersession (PN vs sibling) | matched | -0.0341 | [-0.0854, +0.0227] | [-0.1075, +0.0294] | [-0.0795, +0.0114] | [-0.0958, +0.0215] | no | no | neither shown nor excluded |
| sibling-name control | tab:cf-sibling | GPT-5.6 Sol (draw 1) | supersession (PN vs sibling) | matched | -0.0341 | [-0.0966, +0.0286] | [-0.0905, +0.0253] | [-0.0909, +0.0170] | [-0.0825, +0.0163] | no | no | neither shown nor excluded |
| sibling-name control | tab:cf-sibling | Opus 5 (draw 1) | supersession (PN vs sibling) | matched | +0.0227 | [-0.0170, +0.0682] | [-0.0114, +0.0632] | [-0.0114, +0.0625] | [-0.0059, +0.0568] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-minus-lookup | GPT-4.1 mini, paraphrases | whole | pooled | -0.0904 | [-0.1453, -0.0352] | [-0.1517, -0.0337] | [-0.1387, -0.0438] | [-0.1405, -0.0424] | yes | no | reliable |
| paraphrase set | tab:para-minus-lookup | GPT-4.1 mini, originals | whole | pooled | -0.0794 | [-0.1303, -0.0290] | [-0.1236, -0.0348] | [-0.1238, -0.0375] | [-0.1179, -0.0404] | yes | no | reliable |
| paraphrase set | tab:para-sup | GPT-4.1 mini, paraphrases | supersession | pooled | -0.1195 | [-0.1842, -0.0572] | [-0.1959, -0.0512] | [-0.1687, -0.0666] | [-0.1833, -0.0598] | yes | no | reliable |
| paraphrase set | tab:para-sup | GPT-4.1 mini, originals | supersession | pooled | -0.1044 | [-0.1593, -0.0532] | [-0.1665, -0.0456] | [-0.1475, -0.0594] | [-0.1558, -0.0550] | yes | no | reliable |
| paraphrase set | tab:para-sup | GPT-4.1 mini, paraphrases | supersession | matched | -0.1513 | [-0.2171, -0.0789] | [-0.2501, -0.0548] | [-0.2105, -0.0855] | [-0.2344, -0.0730] | yes | no | reliable |
| paraphrase set | tab:para-sup | GPT-4.1 mini, originals | supersession | matched | -0.1053 | [-0.1581, -0.0526] | [-0.1667, -0.0417] | [-0.1513, -0.0592] | [-0.1594, -0.0533] | yes | no | reliable |
| paraphrase set | tab:para-minus-lookup | GPT-4.1 mini, all states, paraphrases | whole | pooled | -0.1040 | [-0.1775, -0.0351] | [-0.1649, -0.0512] | [-0.1645, -0.0499] | [-0.1557, -0.0612] | yes | no | reliable |
| paraphrase set | tab:para-minus-lookup | GPT-4.1 mini, all states, originals | whole | pooled | -0.0828 | [-0.1323, -0.0357] | [-0.1319, -0.0356] | [-0.1255, -0.0416] | [-0.1235, -0.0438] | yes | no | reliable |
| paraphrase set | tab:para-sup | GPT-4.1 mini, all states, paraphrases | supersession | pooled | -0.0868 | [-0.1583, -0.0115] | [-0.1572, -0.0143] | [-0.1471, -0.0229] | [-0.1448, -0.0308] | yes | no | reliable |
| paraphrase set | tab:para-sup | GPT-4.1 mini, all states, originals | supersession | pooled | -0.0703 | [-0.1177, -0.0197] | [-0.1320, -0.0099] | [-0.1122, -0.0271] | [-0.1187, -0.0196] | yes | no | reliable |
| paraphrase set | tab:para-sup | GPT-4.1 mini, all states, paraphrases | supersession | matched | -0.1118 | [-0.1908, -0.0395] | [-0.1875, -0.0384] | [-0.1776, -0.0461] | [-0.1757, -0.0493] | yes | no | reliable |
| paraphrase set | tab:para-sup | GPT-4.1 mini, all states, originals | supersession | matched | -0.0724 | [-0.1316, -0.0132] | [-0.1583, +0.0000] | [-0.1250, -0.0197] | [-0.1439, -0.0128] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-minus-lookup | Haiku 4.5, paraphrases | whole | pooled | -0.0568 | [-0.1170, +0.0040] | [-0.1066, -0.0074] | [-0.1030, -0.0080] | [-0.0960, -0.0158] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-minus-lookup | Haiku 4.5, originals | whole | pooled | -0.0142 | [-0.0675, +0.0365] | [-0.0557, +0.0346] | [-0.0593, +0.0307] | [-0.0504, +0.0253] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-sup | Haiku 4.5, paraphrases | supersession | pooled | -0.0743 | [-0.1371, -0.0202] | [-0.1355, -0.0116] | [-0.1256, -0.0274] | [-0.1285, -0.0206] | yes | no | reliable |
| paraphrase set | tab:para-sup | Haiku 4.5, originals | supersession | pooled | -0.0304 | [-0.0746, +0.0152] | [-0.0833, +0.0222] | [-0.0660, +0.0066] | [-0.0730, +0.0119] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-sup | Haiku 4.5, paraphrases | supersession | matched | -0.0526 | [-0.1250, +0.0197] | [-0.1205, +0.0236] | [-0.1118, +0.0066] | [-0.1111, +0.0070] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-sup | Haiku 4.5, originals | supersession | matched | -0.0592 | [-0.1250, +0.0000] | [-0.1181, -0.0068] | [-0.1118, -0.0132] | [-0.1053, -0.0130] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-minus-lookup | Haiku 4.5, all states, paraphrases | whole | pooled | -0.0704 | [-0.1300, -0.0130] | [-0.1230, -0.0149] | [-0.1204, -0.0217] | [-0.1150, -0.0241] | yes | no | reliable |
| paraphrase set | tab:para-minus-lookup | Haiku 4.5, all states, originals | whole | pooled | -0.0006 | [-0.0363, +0.0378] | [-0.0426, +0.0385] | [-0.0317, +0.0320] | [-0.0342, +0.0310] | no | yes | equivalent within 0.05 |
| paraphrase set | tab:para-sup | Haiku 4.5, all states, paraphrases | supersession | pooled | -0.0879 | [-0.1577, -0.0148] | [-0.1488, -0.0241] | [-0.1449, -0.0284] | [-0.1390, -0.0338] | yes | no | reliable |
| paraphrase set | tab:para-sup | Haiku 4.5, all states, originals | supersession | pooled | -0.0187 | [-0.0572, +0.0290] | [-0.0678, +0.0265] | [-0.0508, +0.0205] | [-0.0593, +0.0185] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-sup | Haiku 4.5, all states, paraphrases | supersession | matched | -0.0921 | [-0.1645, -0.0132] | [-0.1603, -0.0241] | [-0.1513, -0.0197] | [-0.1500, -0.0337] | yes | no | reliable |
| paraphrase set | tab:para-sup | Haiku 4.5, all states, originals | supersession | matched | -0.0395 | [-0.1053, +0.0263] | [-0.1081, +0.0260] | [-0.0921, +0.0197] | [-0.0987, +0.0143] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-minus-lookup | Opus 5, draw 1, paraphrases | whole | pooled | +0.0630 | [+0.0078, +0.1134] | [+0.0101, +0.1139] | [+0.0162, +0.1052] | [+0.0188, +0.1066] | yes | no | reliable |
| paraphrase set | tab:para-minus-lookup | Opus 5, draw 1, originals | whole | pooled | +0.0745 | [+0.0230, +0.1252] | [+0.0357, +0.1147] | [+0.0288, +0.1160] | [+0.0414, +0.1075] | yes | no | reliable |
| paraphrase set | tab:para-sup | Opus 5, draw 1, paraphrases | supersession | pooled | +0.0226 | [-0.0241, +0.0698] | [-0.0357, +0.0806] | [-0.0164, +0.0603] | [-0.0239, +0.0722] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-sup | Opus 5, draw 1, originals | supersession | pooled | +0.0136 | [-0.0218, +0.0464] | [-0.0249, +0.0513] | [-0.0148, +0.0411] | [-0.0190, +0.0438] | no | yes | equivalent within 0.05 |
| paraphrase set | tab:para-sup | Opus 5, draw 1, paraphrases | supersession | matched | +0.0263 | [-0.0329, +0.0855] | [-0.0375, +0.1000] | [-0.0263, +0.0789] | [-0.0286, +0.0833] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-sup | Opus 5, draw 1, originals | supersession | matched | +0.0132 | [-0.0066, +0.0395] | [-0.0141, +0.0435] | [-0.0066, +0.0329] | [-0.0081, +0.0398] | no | yes | equivalent within 0.05 |
| paraphrase set | tab:para-minus-lookup | Opus 5, draw 1, all states, paraphrases | whole | pooled | +0.0544 | [+0.0013, +0.0983] | [+0.0060, +0.1003] | [+0.0129, +0.0919] | [+0.0148, +0.0921] | yes | no | reliable |
| paraphrase set | tab:para-minus-lookup | Opus 5, draw 1, all states, originals | whole | pooled | +0.0387 | [+0.0053, +0.0718] | [+0.0071, +0.0705] | [+0.0104, +0.0665] | [+0.0123, +0.0661] | yes | no | reliable |
| paraphrase set | tab:para-sup | Opus 5, draw 1, all states, paraphrases | supersession | pooled | +0.0607 | [+0.0114, +0.1156] | [+0.0009, +0.1256] | [+0.0192, +0.1049] | [+0.0102, +0.1159] | yes | no | reliable |
| paraphrase set | tab:para-sup | Opus 5, draw 1, all states, originals | supersession | pooled | +0.0309 | [-0.0027, +0.0662] | [-0.0090, +0.0723] | [+0.0022, +0.0606] | [-0.0023, +0.0641] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-sup | Opus 5, draw 1, all states, paraphrases | supersession | matched | +0.0526 | [+0.0000, +0.1118] | [-0.0068, +0.1071] | [+0.0066, +0.0987] | [+0.0000, +0.0964] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-sup | Opus 5, draw 1, all states, originals | supersession | matched | +0.0461 | [+0.0000, +0.0987] | [+0.0061, +0.0890] | [+0.0132, +0.0921] | [+0.0071, +0.0833] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-minus-lookup | GPT-5.6 Luna, paraphrases | whole | pooled | +0.0945 | [+0.0485, +0.1401] | [+0.0465, +0.1431] | [+0.0556, +0.1330] | [+0.0544, +0.1336] | yes | no | reliable |
| paraphrase set | tab:para-minus-lookup | GPT-5.6 Luna, originals | whole | pooled | +0.0763 | [+0.0305, +0.1192] | [+0.0400, +0.1123] | [+0.0381, +0.1141] | [+0.0467, +0.1072] | yes | no | reliable |
| paraphrase set | tab:para-sup | GPT-5.6 Luna, paraphrases | supersession | pooled | +0.0445 | [+0.0093, +0.0845] | [+0.0042, +0.0895] | [+0.0152, +0.0785] | [+0.0096, +0.0804] | yes | no | reliable |
| paraphrase set | tab:para-sup | GPT-5.6 Luna, originals | supersession | pooled | +0.0255 | [-0.0003, +0.0520] | [-0.0040, +0.0514] | [+0.0044, +0.0483] | [+0.0004, +0.0466] | no | yes | equivalent within 0.05 |
| paraphrase set | tab:para-sup | GPT-5.6 Luna, paraphrases | supersession | matched | +0.0395 | [-0.0066, +0.0921] | [-0.0071, +0.1053] | [+0.0000, +0.0789] | [-0.0061, +0.0903] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-sup | GPT-5.6 Luna, originals | supersession | matched | -0.0197 | [-0.0658, +0.0132] | [-0.0556, +0.0072] | [-0.0526, +0.0066] | [-0.0507, +0.0063] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-minus-lookup | GPT-5.6 Sol, paraphrases | whole | pooled | +0.0891 | [+0.0370, +0.1384] | [+0.0374, +0.1380] | [+0.0458, +0.1312] | [+0.0458, +0.1290] | yes | no | reliable |
| paraphrase set | tab:para-minus-lookup | GPT-5.6 Sol, originals | whole | pooled | +0.0824 | [+0.0379, +0.1300] | [+0.0443, +0.1234] | [+0.0442, +0.1219] | [+0.0493, +0.1147] | yes | no | reliable |
| paraphrase set | tab:para-sup | GPT-5.6 Sol, paraphrases | supersession | pooled | +0.0396 | [-0.0063, +0.0845] | [-0.0176, +0.0929] | [+0.0002, +0.0774] | [-0.0075, +0.0850] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-sup | GPT-5.6 Sol, originals | supersession | pooled | +0.0172 | [-0.0169, +0.0501] | [-0.0228, +0.0517] | [-0.0103, +0.0457] | [-0.0160, +0.0470] | no | yes | equivalent within 0.05 |
| paraphrase set | tab:para-sup | GPT-5.6 Sol, paraphrases | supersession | matched | +0.0263 | [-0.0395, +0.0855] | [-0.0390, +0.0974] | [-0.0263, +0.0789] | [-0.0308, +0.0833] | no | no | neither shown nor excluded |
| paraphrase set | tab:para-sup | GPT-5.6 Sol, originals | supersession | matched | -0.0197 | [-0.0658, +0.0197] | [-0.0596, +0.0130] | [-0.0592, +0.0132] | [-0.0530, +0.0074] | no | no | neither shown nor excluded |

## AUX-R139-E-GROUPS: the E-iv sentence's groups (matched metric, default summary, supersession slice, the five readers at their Table 1 settings; the pooled verdict beside)

| reader | matched verdict | pooled verdict | matched row | pooled row |
|---|---|---|---|---|
| mini | reliably below | neither | -0.0739 90% [-0.1193, -0.0284] [-0.1304, -0.0294] | -0.0429 90% [-0.0818, -0.0074] [-0.0896, -0.0038] |
| Haiku | neither | neither | -0.0511 90% [-0.0966, -0.0114] [-0.0988, -0.0066] | -0.0347 90% [-0.0727, +0.0014] [-0.0706, -0.0017] |
| Luna | equivalent | equivalent | -0.0057 90% [-0.0284, +0.0227] [-0.0291, +0.0150] | +0.0204 90% [-0.0003, +0.0429] [-0.0021, +0.0403] |
| Sol | equivalent | equivalent | -0.0057 90% [-0.0455, +0.0284] [-0.0372, +0.0230] | +0.0161 90% [-0.0082, +0.0424] [-0.0109, +0.0411] |
| Opus | equivalent | equivalent | +0.0114 90% [-0.0170, +0.0398] [-0.0222, +0.0495] | +0.0102 90% [-0.0143, +0.0352] [-0.0190, +0.0382] |

Equivalent group (matched): Luna, Sol, Opus; reliably below: mini; neither: Haiku. The pooled verdict differs for: mini (neither).

## AUX-R139-B6: the lookup with one count feature minus each of Luna, Sol and Opus (matched, 148 triples)

Luna: neither, Sol: neither, Opus: neither. All three: equivalence within 0.05 is not shown, and no difference is reliable.

## AUX-R139-B2: the sibling-name control's closest reader (the largest model-minus-lookup difference, PN against sibling, matched)

Opus 5 (draw 1): +0.0227, 95% item [-0.0170, +0.0682], persona [-0.0114, +0.0632]; the wider is the item-level one (the ruling prints it): printed +0.02 [-0.02, +0.07].

## AUX-R139-LENGTH: the length-only reader (post hoc)

Score = the number of names in the superseded-names section of the text the reader saw. Pooled AUROC with the persona-grouped interval; matched over the triples with the triple-level and persona-grouped intervals.

| summary | scope | items | triples | pooled | persona interval | W/T/L | matched | triple interval | persona interval |
|---|---|---:|---:|---:|---|---|---:|---|---|
| padded | whole | 444 | 148 | 0.7973 | [0.7552, 0.8404] | 88/60/0 | 0.7973 | [0.7568, 0.8378] | [0.7552, 0.8404] |
| padded | supersession | 264 | 88 | 1.0000 | [1.0000, 1.0000] | 88/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] |
| padded | retraction | 90 | 30 | 0.5000 | [0.5000, 0.5000] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] |
| padded | expiry | 90 | 30 | 0.5000 | [0.5000, 0.5000] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] |
| unpadded | whole | 444 | 148 | 0.6295 | [0.6078, 0.6654] | 88/60/0 | 0.7973 | [0.7568, 0.8378] | [0.7552, 0.8404] |
| unpadded | supersession | 264 | 88 | 0.7199 | [0.6949, 0.7716] | 88/0/0 | 1.0000 | [1.0000, 1.0000] | [1.0000, 1.0000] |
| unpadded | retraction | 90 | 30 | 0.5000 | [0.5000, 0.5000] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] |
| unpadded | expiry | 90 | 30 | 0.5000 | [0.5000, 0.5000] | 0/30/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] |
| sibling | supersession | 176 | 88 | 0.5000 | [0.5000, 0.5000] | 0/88/0 | 0.5000 | [0.5000, 0.5000] | [0.5000, 0.5000] |

PN list length minus sibling list length, per (triple, sibling):

| summary | scope | histogram (difference: count) |
|---|---|---|
| padded | supersession | 1: 162, 2: 12, 3: 2 |
| padded | whole | 0: 120, 1: 162, 2: 12, 3: 2 |
| unpadded | supersession | 1: 162, 2: 12, 3: 2 |
| unpadded | whole | 0: 120, 1: 162, 2: 12, 3: 2 |
| sibling | supersession | 0: 88 |

The default summary's supersession lists: PN mean 2.625 names (printed at one decimal, half-up: 2.6; the abstract and 5.2), maximum 6, 24 of 88 PRESENT lists empty (AUX-CF2-R125-T2-CENSUS agrees). Padded: PN 60 to 60, siblings 57 to 60.

Reading (no softening): on the supersession triples the PN list is one to three names longer than both siblings' in every triple, padded or not; the length-only reader wins all 88 triples (matched 1.0000) on both lists and, on the padded lists, where every PN list has exactly 60 names and every sibling list fewer, it is also perfect pooled (1.0000). On the sibling-name control the lengths are equal by construction and the reader ties every triple (0.5000). 5.2's text (fixed in BRANCHES_R139.md, no number) and the Limitations sentence carry this.

## AUX-R139-B7: the fixed cue list minus the best model (the intent crossover, supersession crossover A, explicit-intent rubric, same-store pairs)

Source: r82_counterfactual/cf2/results/cf_scores_ix.json (AUX-CF2-IX-P-I4; reviews/r121/tools/ix_score.py), the crossover's own intervals (pair-clustered and persona-clustered, 1,000 draws; no item-level interval exists and none is computed, by ruling). The best model under that rubric is OP5 (same-store AUROC 0.9885; the cue list 0.9943). Cue list minus OP5 = the sign flip of the stored OP5 minus the keyword lookup (-0.0057): +0.0057, pair [-0.0172, +0.0345], persona [-0.0167, +0.0341]; not reliable (both include zero). The wider (pair) is printed: +0.01 [-0.02, +0.03].

## AUX-R139-B1: the pooled comparison beside the matched one (default summary, supersession, 264 items)

cf_pad/results/cf_pad_scores.json readers/*/superseded/pooled/unpadded (the recorded rows; tab:sup-margins): lookup 0.9223, Luna 0.9426, Sol 0.9383, Opus 0.9325; each minus the lookup not reliable (AUX-R139-EQUIV). Printed: the lookup's 0.92 against 0.93 to 0.94 for the three, none reliably above it.

## AUX-R139-FIG3-BARS: Figure 3's points and persona-grouped 95% bars (Unit F; AUX-CF2-R125-PERSTATE)

Source: reviews/r125/results/r125_matched.json readers/*/pn_vs_present/per_state/*: the matched point, the persona interval, and the offsets up (hi minus point) and down (point minus lo) that fig3_data_matched.tex carries.

| reader | state | point | persona interval | up | down |
|---|---|---:|---|---:|---:|
| MINI5_v2 | supersession | 0.8920 | [0.8228, 0.9487] | 0.0567 | 0.0692 |
| MINI5_v2 | retraction | 0.5667 | [0.3906, 0.7414] | 0.1747 | 0.1761 |
| MINI5_v2 | expiry | 0.4000 | [0.2857, 0.5143] | 0.1143 | 0.1143 |
| H45_v2 | supersession | 0.9148 | [0.8631, 0.9615] | 0.0467 | 0.0517 |
| H45_v2 | retraction | 0.5667 | [0.4825, 0.6607] | 0.0940 | 0.0842 |
| H45_v2 | expiry | 0.5833 | [0.4688, 0.7116] | 0.1283 | 0.1146 |
| LUNA_v2 | supersession | 0.9602 | [0.9175, 0.9937] | 0.0335 | 0.0427 |
| LUNA_v2 | retraction | 0.6500 | [0.4515, 0.8214] | 0.1714 | 0.1985 |
| LUNA_v2 | expiry | 0.8667 | [0.7586, 0.9677] | 0.1010 | 0.1081 |
| SOL_v2 | supersession | 0.9602 | [0.9231, 0.9895] | 0.0293 | 0.0371 |
| SOL_v2 | retraction | 0.5833 | [0.4107, 0.7500] | 0.1667 | 0.1726 |
| SOL_v2 | expiry | 0.8333 | [0.7000, 0.9394] | 0.1061 | 0.1333 |
| OP5_v2 | supersession | 0.9773 | [0.9432, 1.0000] | 0.0227 | 0.0341 |
| OP5_v2 | retraction | 0.7667 | [0.6111, 0.9118] | 0.1451 | 0.1556 |
| OP5_v2 | expiry | 0.6833 | [0.5000, 0.8750] | 0.1917 | 0.1833 |
| LOOKUP_v2 | supersession | 0.9659 | [0.9286, 0.9944] | 0.0285 | 0.0373 |
| LOOKUP_v2 | retraction | 0.5000 | [0.5000, 0.5000] | 0.0000 | 0.0000 |
| LOOKUP_v2 | expiry | 0.5000 | [0.5000, 0.5000] | 0.0000 | 0.0000 |
| CR-nb1_v2 | supersession | 0.6932 | [0.6288, 0.7566] | 0.0634 | 0.0644 |
| CR-nb1_v2 | retraction | 0.7667 | [0.6897, 0.8519] | 0.0852 | 0.0770 |
| CR-nb1_v2 | expiry | 0.7500 | [0.6613, 0.8261] | 0.0761 | 0.0887 |
| MINI5_v3 | supersession | 0.9205 | [0.8636, 0.9670] | 0.0465 | 0.0569 |
| MINI5_v3 | retraction | 0.9333 | [0.8214, 1.0000] | 0.0667 | 0.1119 |
| MINI5_v3 | expiry | 0.7833 | [0.6429, 0.9107] | 0.1274 | 0.1404 |
| H45_v3 | supersession | 0.8920 | [0.8367, 0.9412] | 0.0492 | 0.0553 |
| H45_v3 | retraction | 0.9333 | [0.8676, 1.0000] | 0.0667 | 0.0657 |
| H45_v3 | expiry | 0.9167 | [0.8387, 0.9828] | 0.0661 | 0.0780 |
| OP5_v3 | supersession | 0.9659 | [0.9140, 1.0000] | 0.0341 | 0.0519 |
| OP5_v3 | retraction | 0.8333 | [0.7000, 0.9432] | 0.1099 | 0.1333 |
| OP5_v3 | expiry | 0.9667 | [0.8929, 1.0000] | 0.0333 | 0.0738 |
| ALLSTATES_v3 | supersession | 0.9432 | [0.9022, 0.9810] | 0.0378 | 0.0410 |
| ALLSTATES_v3 | retraction | 0.8167 | [0.7321, 0.8940] | 0.0773 | 0.0846 |
| ALLSTATES_v3 | expiry | 0.9000 | [0.8333, 0.9545] | 0.0545 | 0.0667 |

## AUX-R139-N: the comparisons the main text calls reliable or not reliable (A2)

A comparison is one difference (one reader minus another, or one reader's score under one condition minus under another) on one population. It is counted once for each metric a sentence distinguishes (the pooled AUROC and the matched score); where a sentence names no metric, or names none apart, the difference counts once. A reader named in a group counts once per reader; states named separately count separately. A comparison named in several sentences counts once. Only sentences that apply 'reliable' or 'reliably' (or deny it) to a comparison enter; the two definition sentences of Section 4 do not. The list is keyed to sentence fragments; port_r139.py counts only the entries whose fragment is in the final main text and asserts that every main-text sentence carrying 'reliab' is covered, so a payer that deletes a sentence deletes its comparisons.

| # | sentence (fragment asserted present in the built main text) | comparisons named | count |
|---|---|---|---:|
| 1 | none of five language models reliably beats a cosine-similarity lookup over the names | short list, supersession, model minus lookup, matched: mini; short list, supersession, model minus lookup, matched: Haiku; short list, supersession, model minus lookup, matched: Luna; short list, supersession, model minus lookup, matched: Sol; short list, supersession, model minus lookup, matched: Opus; sibling-name control, model minus lookup: mini; sibling-name control, model minus lookup: Haiku; sibling-name control, model minus lookup: Luna; sibling-name control, model minus lookup: Sol; sibling-name control, model minus lookup: Opus | 10 |
| 2 | On the named state no model reliably exceeds a name lookup when the list is short | short list, supersession, model minus lookup, matched: mini; short list, supersession, model minus lookup, matched: Haiku; short list, supersession, model minus lookup, matched: Luna; short list, supersession, model minus lookup, matched: Sol; short list, supersession, model minus lookup, matched: Opus; sibling-name control, model minus lookup: mini; sibling-name control, model minus lookup: Haiku; sibling-name control, model minus lookup: Luna; sibling-name control, model minus lookup: Sol; sibling-name control, model minus lookup: Opus; padded set, supersession, model minus lookup, pooled: mini; padded set, supersession, model minus lookup, pooled: Haiku; padded set, supersession, model minus lookup, pooled: Luna; padded set, supersession, model minus lookup, pooled: Sol; padded set, supersession, model minus lookup, pooled: Opus | 15 |
| 3 | on retraction and expiry both stay reliably below a count reader that merely guesses the category | retraction, mini minus the guessing count reader; expiry, mini minus the guessing count reader; retraction, Haiku minus the guessing count reader; expiry, Haiku minus the guessing count reader | 4 |
| 4 | none of Luna, Sol and Opus sits reliably below the guessing count reader | retraction, Luna minus the guessing count reader; expiry, Luna minus the guessing count reader; retraction, Sol minus the guessing count reader; expiry, Sol minus the guessing count reader; retraction, Opus minus the guessing count reader; expiry, Opus minus the guessing count reader | 6 |
| 5 | while mini and Haiku show no reliable change | count moved to a sibling version minus default, counted states: mini; count moved to a sibling version minus default, counted states: Haiku | 2 |
| 6 | The falls are reliable on the matched metric and, pooled, on expiry for all three and on retraction for Opus alone. | count moved to a sibling version minus default, counted states, matched: Luna; count moved to a sibling version minus default, counted states, matched: Sol; count moved to a sibling version minus default, counted states, matched: Opus; count moved, expiry, pooled: Luna; count moved, expiry, pooled: Sol; count moved, expiry, pooled: Opus; count moved, retraction, pooled: Luna; count moved, retraction, pooled: Sol; count moved, retraction, pooled: Opus | 9 |
| 7 | Removing every count costs Luna and Opus reliably | every count deleted minus default: Luna; every count deleted minus default: Opus | 2 |
| 8 | no model reliably beats the lookup on the short list; on a long one, two do. | short list, supersession, model minus lookup, matched: mini; short list, supersession, model minus lookup, matched: Haiku; short list, supersession, model minus lookup, matched: Luna; short list, supersession, model minus lookup, matched: Sol; short list, supersession, model minus lookup, matched: Opus; padded set, supersession, model minus lookup, pooled: mini; padded set, supersession, model minus lookup, pooled: Haiku; padded set, supersession, model minus lookup, pooled: Luna; padded set, supersession, model minus lookup, pooled: Sol; padded set, supersession, model minus lookup, pooled: Opus | 10 |
| 9 | Luna and Sol $0.01$ below, and only mini reliably below. | short list, supersession, model minus lookup, matched: mini; short list, supersession, model minus lookup, matched: Haiku; short list, supersession, model minus lookup, matched: Luna; short list, supersession, model minus lookup, matched: Sol; short list, supersession, model minus lookup, matched: Opus | 5 |
| 10 | Pooled, the lookup scores $0.92$ and the three $0.93$ to $0.94$, none reliably above it. | short list, supersession, model minus lookup, pooled: Luna; short list, supersession, model minus lookup, pooled: Sol; short list, supersession, model minus lookup, pooled: Opus | 3 |
| 11 | sits reliably below it on the matched metric only | short list, supersession, model minus lookup, matched: mini; short list, supersession, model minus lookup, pooled: mini; short list, supersession, model minus lookup, matched: Haiku | 3 |
| 12 | none reliably above the lookup (Opus, the closest, | sibling-name control, model minus lookup: mini; sibling-name control, model minus lookup: Haiku; sibling-name control, model minus lookup: Luna; sibling-name control, model minus lookup: Sol; sibling-name control, model minus lookup: Opus | 5 |
| 13 | none reliably above the lookup, while meaningless tokens | sibling-name control, model minus lookup: mini; sibling-name control, model minus lookup: Haiku; sibling-name control, model minus lookup: Luna; sibling-name control, model minus lookup: Sol; sibling-name control, model minus lookup: Opus | 5 |
| 14 | ending at or below it with no reliable difference | padded set, supersession, model minus lookup, pooled: mini; padded set, supersession, model minus lookup, pooled: Haiku; padded set, supersession, model minus lookup, pooled: Opus | 3 |
| 15 | lead the lookup by a reliable $0.13$ to $0.14$ pooled and $0.09$ to $0.10$ within triples | padded set, supersession, model minus lookup, pooled: Luna; padded set, supersession, model minus lookup, pooled: Sol; padded set, supersession, model minus lookup, matched: Luna; padded set, supersession, model minus lookup, matched: Sol | 4 |
| 16 | Across all $148$ triples Luna, Sol and Opus score a reliable $0.08$ to $0.10$ above the lookup. | whole set, model minus lookup, matched: Luna; whole set, model minus lookup, matched: Sol; whole set, model minus lookup, matched: Opus | 3 |
| 17 | the models stay a reliable $0.05$ to $0.06$ above it | whole set, model minus the lookup with one count feature, pooled: Luna; whole set, model minus the lookup with one count feature, pooled: Sol; whole set, model minus the lookup with one count feature, pooled: Opus | 3 |
| 18 | Haiku by a reliable $0.35$ on the two states that were only counted | Haiku, all-states summary minus default, counted states | 1 |
| 19 | lead over the all-states lookup is reliable on the pooled metric and not on the matched one, so with every state named no model is reliably ahead on both. | all-states summary, Opus minus the all-states lookup, pooled; all-states summary, Opus minus the all-states lookup, matched; all-states summary, mini minus the all-states lookup; all-states summary, Haiku minus the all-states lookup | 4 |
| 20 | A fixed cue list is not reliably below the best model | intent crossover, explicit rubric, fixed cue list minus Opus | 1 |
| 21 | the capped summary still costs each reader a reliable $0.13$ to $0.20$ | FR-Bank capped store-written minus ground truth, marked obligations: mini; FR-Bank capped store-written minus ground truth, marked obligations: Haiku; FR-Bank capped store-written minus ground truth, marked obligations: the lookup | 3 |
| 22 | against $0.84$ under ground truth is still a reliable loss. | Graphiti, mini, capped store-written minus ground truth, retained obligations | 1 |
| 23 | and $0.83$ with both, a reliable gain over the summary alone. | mini, summary and tagged view minus summary alone | 1 |
| 24 | both effects reliable (Table~\ref{tab:routes}) | mini, tagged view effect, expiry; mini, tagged view effect, supersession | 2 |
| 25 | mini's view-only score rises reliably to $0.81$ | mini, view only, FR-Bank's own tags minus ground-truth tags | 1 |
| 26 | native tags on the same retrieved edges bring no reliable improvement | Graphiti, native tags minus ground-truth tags, view | 1 |
| 27 | truncated to the gated budget it loses licensed records, a reliable $0.04$ | truncated always-on fetch minus gated fetch, licensed-record reach | 1 |
| 28 | On the full obligation set, no completed model reliably beats the lookup. | full obligation set, model minus lookup: mini; full obligation set, model minus lookup: Haiku; full obligation set, model minus lookup: Luna; full obligation set, model minus lookup: Opus | 4 |
| 29 | On a named state no model reliably exceeds the name lookup on the short list, with list length kept fixed or not | short list, supersession, model minus lookup, matched: mini; short list, supersession, model minus lookup, matched: Haiku; short list, supersession, model minus lookup, matched: Luna; short list, supersession, model minus lookup, matched: Sol; short list, supersession, model minus lookup, matched: Opus; sibling-name control, model minus lookup: mini; sibling-name control, model minus lookup: Haiku; sibling-name control, model minus lookup: Luna; sibling-name control, model minus lookup: Sol; sibling-name control, model minus lookup: Opus | 10 |
| 30 | and only mini reliably below (pooled: $0.92$ against $0.93$ to $0.94$, none reliable; | short list, supersession, model minus lookup, matched: mini; short list, supersession, model minus lookup, matched: Haiku; short list, supersession, model minus lookup, matched: Luna; short list, supersession, model minus lookup, matched: Sol; short list, supersession, model minus lookup, matched: Opus; short list, supersession, model minus lookup, pooled: Luna; short list, supersession, model minus lookup, pooled: Sol; short list, supersession, model minus lookup, pooled: Opus | 8 |
| 31 | On a named state no model reliably exceeds the name lookup on the short list; | short list, supersession, model minus lookup, matched: mini; short list, supersession, model minus lookup, matched: Haiku; short list, supersession, model minus lookup, matched: Luna; short list, supersession, model minus lookup, matched: Sol; short list, supersession, model minus lookup, matched: Opus | 5 |
| 32 | and a fixed cue list is not reliably below the best of them. | intent crossover, explicit rubric, fixed cue list minus Opus | 1 |

**Distinct comparisons in the main text as last built by port_r139.py: 68** over the 28 entries present (a comparison named in several sentences counts once; an entry whose sentence a payer removed does not count); families: the registered model-minus-lookup families hold five readers each (default summary, sibling-name control, padded set, paraphrase set) and three under the all-states summary (mini, Haiku, Opus).

The distinct comparisons: FR-Bank capped store-written minus ground truth, marked obligations: Haiku; FR-Bank capped store-written minus ground truth, marked obligations: mini; FR-Bank capped store-written minus ground truth, marked obligations: the lookup; Graphiti, mini, capped store-written minus ground truth, retained obligations; Graphiti, native tags minus ground-truth tags, view; Haiku, all-states summary minus default, counted states; all-states summary, Haiku minus the all-states lookup; all-states summary, Opus minus the all-states lookup, matched; all-states summary, Opus minus the all-states lookup, pooled; all-states summary, mini minus the all-states lookup; count moved to a sibling version minus default, counted states, matched: Luna; count moved to a sibling version minus default, counted states, matched: Opus; count moved to a sibling version minus default, counted states, matched: Sol; count moved to a sibling version minus default, counted states: Haiku; count moved to a sibling version minus default, counted states: mini; count moved, expiry, pooled: Luna; count moved, expiry, pooled: Opus; count moved, expiry, pooled: Sol; count moved, retraction, pooled: Luna; count moved, retraction, pooled: Opus; count moved, retraction, pooled: Sol; expiry, Haiku minus the guessing count reader; expiry, Luna minus the guessing count reader; expiry, Opus minus the guessing count reader; expiry, Sol minus the guessing count reader; expiry, mini minus the guessing count reader; full obligation set, model minus lookup: Haiku; full obligation set, model minus lookup: Luna; full obligation set, model minus lookup: Opus; full obligation set, model minus lookup: mini; intent crossover, explicit rubric, fixed cue list minus Opus; mini, summary and tagged view minus summary alone; mini, tagged view effect, expiry; mini, tagged view effect, supersession; mini, view only, FR-Bank's own tags minus ground-truth tags; padded set, supersession, model minus lookup, matched: Luna; padded set, supersession, model minus lookup, matched: Sol; padded set, supersession, model minus lookup, pooled: Haiku; padded set, supersession, model minus lookup, pooled: Luna; padded set, supersession, model minus lookup, pooled: Opus; padded set, supersession, model minus lookup, pooled: Sol; padded set, supersession, model minus lookup, pooled: mini; retraction, Haiku minus the guessing count reader; retraction, Luna minus the guessing count reader; retraction, Opus minus the guessing count reader; retraction, Sol minus the guessing count reader; retraction, mini minus the guessing count reader; short list, supersession, model minus lookup, matched: Haiku; short list, supersession, model minus lookup, matched: Luna; short list, supersession, model minus lookup, matched: Opus; short list, supersession, model minus lookup, matched: Sol; short list, supersession, model minus lookup, matched: mini; short list, supersession, model minus lookup, pooled: Luna; short list, supersession, model minus lookup, pooled: Opus; short list, supersession, model minus lookup, pooled: Sol; short list, supersession, model minus lookup, pooled: mini; sibling-name control, model minus lookup: Haiku; sibling-name control, model minus lookup: Luna; sibling-name control, model minus lookup: Opus; sibling-name control, model minus lookup: Sol; sibling-name control, model minus lookup: mini; truncated always-on fetch minus gated fetch, licensed-record reach; whole set, model minus lookup, matched: Luna; whole set, model minus lookup, matched: Opus; whole set, model minus lookup, matched: Sol; whole set, model minus the lookup with one count feature, pooled: Luna; whole set, model minus the lookup with one count feature, pooled: Opus; whole set, model minus the lookup with one count feature, pooled: Sol.

