# NUMBERS_CF_PAD — the long-list check on the counterfactual set (ADDENDUM_CF_PAD, registered text sha256 `a84dac1abc2f604b171b4ab838daba4bbdb440d124ef9f050387bd0a716eba21`, frozen at `06c611f`)

Written 2026-09-22 by `cf_pad/tools/report_cf_pad.py` from `cf_pad/results/cf_pad_scores.json` (scored once, after every lane completed). Every number here is read from the JSON. Pooled AUROC (item; persona intervals) and the matched score (W + T/2) / n, PN against PRESENT (triple; persona intervals); 1,000 draws, seed 42; `*` = both intervals exclude zero. The unpadded values are the recorded Table 1 rows restricted to the same items and triples.

## AUX-CFP-LOCK

Registration sha256 holds; frozen commit `06c611f`; prompts_e1 digests `337d37d3…` / `35d9b968…`; indexes sha256 `b423c34ed6b16c3d…` (= `cf_indexes.json` meta and `cf_cell.json` meta); padded texts sha256 `ce0df620d3f8baec…`; renderer lock 444 of 444; leak scan 0 fails (descriptive {"pad name appearing verbatim in a PN-added entry's text (descriptive)": 20, 'pad name equal to a slot-path suffix of another entry (a qualifier that is also an attribute name; descriptive)': 118}); lookup gate on the committed lists {'emb': 0.7663, 'lex': 0.6698, 'randtok': 0.5954}; recorded gates {'H45_v2': 0.7566, 'LOOKUP_v2': 0.7663, 'LUNA_v2': 0.8417, 'MINI5_v2': 0.7648, 'OP5_v2': 0.8405, 'RANDTOK_v2': 0.5954, 'SOL_v2': 0.85}; pool A min/median/max 71/102.0/121, pairs drawing on pool B 0; list lengths {'57': 2, '58': 12, '59': 162, '60': 268}; pad sizes {'54': 1, '55': 5, '56': 23, '57': 31, '58': 37, '59': 35, '60': 16}; target rank (PN, supersession) min 2, median 41.5, max 60, first 0, last 4.

### Unpadded recorded values (the section-2 rows on the supersession slice and the whole set)

| recorded row | pooled whole | pooled supersession | matched whole | matched supersession |
|---|---:|---:|---:|---:|
| H45_v2 | 0.7566 | 0.8876 | 0.777 | 0.9148 |
| LEX_v2 | 0.6698 | 0.7829 | 0.6689 | 0.7841 |
| LOOKUP_v2 | 0.7663 | 0.9223 | 0.777 | 0.9659 |
| LUNA_v2 | 0.8417 | 0.9426 | 0.8784 | 0.9602 |
| MINI5_v2 | 0.7648 | 0.8793 | 0.7264 | 0.892 |
| OP5_v2 | 0.8405 | 0.9325 | 0.875 | 0.9773 |
| RANDTOK_v2 | 0.5954 | 0.6651 | 0.6453 | 0.7443 |
| SOL_v2 | 0.85 | 0.9383 | 0.8581 | 0.9602 |

## AUX-CFP-PROBES

| lane | served | identifier | tok in / out | usd | status |
|---|---|---|---|---:|---|
| claude-haiku-4-5-20251001 | `claude-haiku-4-5-20251001` | OK | 2075 / 200 | 0.003075 | OK |
| claude-opus-5 | `claude-opus-5` | OK | 2877 / 156 | 0.018285 | OK |
| gpt-4.1-mini | `gpt-4.1-mini-2025-04-14` | OK | 1928 / 24 | 0.000810 | OK |
| gpt-5.6-luna | `gpt-5.6-luna` | OK | 1927 / 132 | 0.000640 | OK |
| gpt-5.6-sol | `gpt-5.6-sol` | OK | 1927 / 131 | 0.012252 | OK |

## AUX-CFP-LANES (rows, served identifiers, collapse census)

| lane | k | rows | not OK | served | units collapsed | complete draws | distinct values | tied triples padded / unpadded | usd |
|---|---:|---:|---:|---|---:|---|---:|---|---:|
| MINI | 5 | 2220 | 0 (0.00%) | {'gpt-4.1-mini-2025-04-14': 2220} | 444 | [1, 2, 3, 4, 5] | 77 | 0 / 6 | 1.5307 |
| H45 | 5 | 2220 | 0 (0.00%) | {'claude-haiku-4-5-20251001': 2220} | 444 | [1, 2, 3, 4, 5] | 73 | 18 / 38 | 3.3115 |
| LUNA | 5 | 2220 | 0 (0.00%) | {'gpt-5.6-luna': 2220} | 444 | [1, 2, 3, 4, 5] | 276 | 0 / 0 | 0.8730 |
| SOL | 5 | 2220 | 0 (0.00%) | {'gpt-5.6-sol': 2220} | 444 | [1, 2, 3, 4, 5] | 264 | 0 / 1 | 13.1196 |
| OP5 | 1 | 444 | 0 (0.00%) | {'claude-opus-5': 444} | 444 | [1] | 43 | 1 / 0 | 4.7777 |

## AUX-CFP-READERS-SUPERSEDED (registered): every reader, supersession (264 items / 88 triples), padded (60-name list) beside unpadded (recorded)

| reader | pooled unpadded | pooled padded | Δ pooled (item; persona) | matched unpadded (W/T/L) | matched padded (W/T/L) | Δ matched (triple; persona) |
|---|---:|---:|---|---|---|---|
| Embedding name lookup | 0.9223 | **0.7416** | -0.1807 * [-0.2420, -0.1272]; [-0.2335, -0.1311] | 0.9659 (82/6/0) | **0.8295** (58/30/0) | -0.1364 * [-0.1875, -0.0909]; [-0.1883, -0.0823] |
| Word-matching lookup | 0.7829 | **0.6892** | -0.0937 * [-0.1435, -0.0501]; [-0.1320, -0.0599] | 0.7841 (50/38/0) | **0.7443** (43/45/0) | -0.0398 * [-0.0739, -0.0170]; [-0.0745, -0.0120] |
| Random-token lookup | 0.6651 | **0.5008** | -0.1643 * [-0.2325, -0.0957]; [-0.2302, -0.1106] | 0.7443 (45/41/2) | **0.5057** (1/87/0) | -0.2386 * [-0.2955, -0.1818]; [-0.3056, -0.1772] |
| GPT-4.1 mini (5 draws) | 0.8793 | **0.6891** | -0.1902 * [-0.2451, -0.1369]; [-0.2407, -0.1354] | 0.8920 (76/5/7) | **0.7841** (67/4/17) | -0.1080 * [-0.2159, -0.0055]; [-0.2143, -0.0055] |
| Haiku 4.5 (5 draws) | 0.8876 | **0.7354** | -0.1522 * [-0.2106, -0.1001]; [-0.2017, -0.0997] | 0.9148 (76/9/3) | **0.8011** (59/23/6) | -0.1136 * [-0.1706, -0.0511]; [-0.1786, -0.0455] |
| GPT-5.6 Luna (5 draws) | 0.9426 | **0.8791** | -0.0636 * [-0.0978, -0.0293]; [-0.0989, -0.0307] | 0.9602 (84/1/3) | **0.9318** (82/0/6) | -0.0284 [-0.0795, +0.0170]; [-0.0787, +0.0188] |
| GPT-5.6 Sol (5 draws) | 0.9383 | **0.8690** | -0.0693 * [-0.1058, -0.0352]; [-0.1175, -0.0221] | 0.9602 (84/1/3) | **0.9205** (81/0/7) | -0.0398 [-0.1193, +0.0284]; [-0.1222, +0.0319] |
| Opus 5 (1 draw; recorded row 5 draws) | 0.9325 | **0.7080** | -0.2245 * [-0.2792, -0.1705]; [-0.3449, -0.1294] | 0.9773 (86/0/2) | **0.7841** (67/4/17) | -0.1932 * [-0.2841, -0.1136]; [-0.3148, -0.0841] |

## AUX-CFP-MINUS-LOOKUP-SUPERSEDED (registered): each model minus the embedding lookup, supersession (264 items / 88 triples)

| model | padded: pooled Δ (item; persona) | padded: matched Δ (triple; persona) | unpadded: pooled Δ (item; persona) | unpadded: matched Δ (triple; persona) |
|---|---|---|---|---|
| GPT-4.1 mini (5 draws) | -0.0525 [-0.1065, +0.0041]; [-0.1092, +0.0058] | -0.0455 [-0.1307, +0.0455]; [-0.1461, +0.0450] | -0.0429 [-0.0898, +0.0006]; [-0.1001, +0.0035] | -0.0739 * [-0.1307, -0.0227]; [-0.1393, -0.0214] |
| Haiku 4.5 (5 draws) | -0.0062 [-0.0652, +0.0515]; [-0.0558, +0.0464] | -0.0284 [-0.0852, +0.0341]; [-0.0805, +0.0294] | -0.0347 [-0.0813, +0.0086]; [-0.0809, +0.0066] | -0.0511 [-0.1136, +0.0000]; [-0.1084, +0.0000] |
| GPT-5.6 Luna (5 draws) | +0.1375 * [+0.0883, +0.1934]; [+0.0971, +0.1777] | +0.1023 * [+0.0398, +0.1648]; [+0.0482, +0.1552] | +0.0204 [-0.0053, +0.0473]; [-0.0056, +0.0451] | -0.0057 [-0.0341, +0.0227]; [-0.0321, +0.0174] |
| GPT-5.6 Sol (5 draws) | +0.1274 * [+0.0726, +0.1837]; [+0.0802, +0.1726] | +0.0909 * [+0.0227, +0.1477]; [+0.0341, +0.1519] | +0.0161 [-0.0130, +0.0473]; [-0.0202, +0.0478] | -0.0057 [-0.0511, +0.0341]; [-0.0417, +0.0287] |
| Opus 5 (1 draw; recorded row 5 draws) | -0.0336 [-0.1070, +0.0448]; [-0.1597, +0.0748] | -0.0455 [-0.1420, +0.0398]; [-0.1845, +0.0756] | +0.0102 [-0.0183, +0.0392]; [-0.0259, +0.0432] | +0.0114 [-0.0227, +0.0455]; [-0.0284, +0.0579] |

## AUX-CFP-READERS-WHOLE (descriptive): every reader, whole set (444 items / 148 triples), padded (60-name list) beside unpadded (recorded)

| reader | pooled unpadded | pooled padded | Δ pooled (item; persona) | matched unpadded (W/T/L) | matched padded (W/T/L) | Δ matched (triple; persona) |
|---|---:|---:|---|---|---|---|
| Embedding name lookup | 0.7663 | **0.6470** | -0.1194 * [-0.1805, -0.0571]; [-0.1551, -0.0857] | 0.7770 (82/66/0) | **0.6959** (58/90/0) | -0.0811 * [-0.1115, -0.0541]; [-0.1157, -0.0521] |
| Word-matching lookup | 0.6698 | **0.6153** | -0.0544 * [-0.0960, -0.0109]; [-0.0791, -0.0298] | 0.6689 (50/98/0) | **0.6453** (43/105/0) | -0.0236 * [-0.0405, -0.0101]; [-0.0426, -0.0074] |
| Random-token lookup | 0.5954 | **0.5004** | -0.0951 * [-0.1567, -0.0316]; [-0.1377, -0.0601] | 0.6453 (45/101/2) | **0.5034** (1/147/0) | -0.1419 * [-0.1824, -0.1047]; [-0.1871, -0.1007] |
| GPT-4.1 mini (5 draws) | 0.7648 | **0.6304** | -0.1344 * [-0.1794, -0.0936]; [-0.1702, -0.0992] | 0.7264 (100/15/33) | **0.7128** (102/7/39) | -0.0135 [-0.1115, +0.0845]; [-0.0988, +0.0621] |
| Haiku 4.5 (5 draws) | 0.7566 | **0.6525** | -0.1041 * [-0.1475, -0.0636]; [-0.1453, -0.0631] | 0.7770 (89/52/7) | **0.6520** (74/45/29) | -0.1250 * [-0.1858, -0.0642]; [-0.1948, -0.0508] |
| GPT-5.6 Luna (5 draws) | 0.8417 | **0.7390** | -0.1027 * [-0.1388, -0.0677]; [-0.1327, -0.0762] | 0.8784 (129/2/17) | **0.8649** (128/0/20) | -0.0135 [-0.0811, +0.0574]; [-0.0966, +0.0669] |
| GPT-5.6 Sol (5 draws) | 0.8500 | **0.7477** | -0.1023 * [-0.1367, -0.0707]; [-0.1390, -0.0627] | 0.8581 (126/2/20) | **0.7635** (113/0/35) | -0.0946 * [-0.1655, -0.0236]; [-0.1633, -0.0280] |
| Opus 5 (1 draw; recorded row 5 draws) | 0.8405 | **0.6527** | -0.1879 * [-0.2268, -0.1480]; [-0.2595, -0.1289] | 0.8750 (128/3/17) | **0.7095** (98/14/36) | -0.1655 * [-0.2433, -0.0811]; [-0.2568, -0.0810] |

## AUX-CFP-MINUS-LOOKUP-WHOLE (descriptive): each model minus the embedding lookup, whole set (444 items / 148 triples)

| model | padded: pooled Δ (item; persona) | padded: matched Δ (triple; persona) | unpadded: pooled Δ (item; persona) | unpadded: matched Δ (triple; persona) |
|---|---|---|---|---|
| GPT-4.1 mini (5 draws) | -0.0165 [-0.0699, +0.0359]; [-0.0541, +0.0207] | +0.0169 [-0.0541, +0.0878]; [-0.0578, +0.0743] | -0.0016 [-0.0426, +0.0393]; [-0.0415, +0.0328] | -0.0507 [-0.1115, +0.0101]; [-0.1069, +0.0000] |
| Haiku 4.5 (5 draws) | +0.0055 [-0.0462, +0.0538]; [-0.0278, +0.0447] | -0.0439 [-0.0981, +0.0068]; [-0.0896, +0.0031] | -0.0098 [-0.0640, +0.0398]; [-0.0494, +0.0336] | +0.0000 [-0.0439, +0.0372]; [-0.0528, +0.0483] |
| GPT-5.6 Luna (5 draws) | +0.0921 * [+0.0450, +0.1438]; [+0.0572, +0.1277] | +0.1689 * [+0.1115, +0.2297]; [+0.1102, +0.2245] | +0.0754 * [+0.0339, +0.1216]; [+0.0450, +0.1090] | +0.1014 * [+0.0473, +0.1554]; [+0.0442, +0.1533] |
| GPT-5.6 Sol (5 draws) | +0.1007 * [+0.0516, +0.1531]; [+0.0629, +0.1413] | +0.0676 [+0.0000, +0.1318]; [+0.0096, +0.1241] | +0.0836 * [+0.0401, +0.1315]; [+0.0544, +0.1163] | +0.0811 * [+0.0270, +0.1351]; [+0.0283, +0.1319] |
| Opus 5 (1 draw; recorded row 5 draws) | +0.0057 [-0.0538, +0.0711]; [-0.0780, +0.0847] | +0.0135 [-0.0574, +0.0845]; [-0.0868, +0.1084] | +0.0742 * [+0.0315, +0.1203]; [+0.0414, +0.1126] | +0.0980 * [+0.0472, +0.1454]; [+0.0435, +0.1503] |

## AUX-CFP-READERS-RETRACTED (descriptive): every reader, retraction (90 items / 30 triples), padded (60-name list) beside unpadded (recorded)

| reader | pooled unpadded | pooled padded | Δ pooled (item; persona) | matched unpadded (W/T/L) | matched padded (W/T/L) | Δ matched (triple; persona) |
|---|---:|---:|---|---|---|---|
| Embedding name lookup | 0.5000 | **0.5000** | +0.0000 [-0.1966, +0.1834]; [+0.0000, +0.0000] | 0.5000 (0/30/0) | **0.5000** (0/30/0) | +0.0000 [+0.0000, +0.0000]; [+0.0000, +0.0000] |
| Word-matching lookup | 0.5000 | **0.5000** | +0.0000 [-0.1321, +0.1145]; [+0.0000, +0.0000] | 0.5000 (0/30/0) | **0.5000** (0/30/0) | +0.0000 [+0.0000, +0.0000]; [+0.0000, +0.0000] |
| Random-token lookup | 0.5000 | **0.5000** | +0.0000 [-0.1429, +0.1357]; [+0.0000, +0.0000] | 0.5000 (0/30/0) | **0.5000** (0/30/0) | +0.0000 [+0.0000, +0.0000]; [+0.0000, +0.0000] |
| GPT-4.1 mini (5 draws) | 0.5761 | **0.5597** | -0.0164 [-0.1150, +0.0763]; [-0.0898, +0.0490] | 0.5667 (15/4/11) | **0.6667** (20/0/10) | +0.1000 [-0.1833, +0.3500]; [-0.1482, +0.3550] |
| Haiku 4.5 (5 draws) | 0.5433 | **0.5014** | -0.0419 [-0.1473, +0.0548]; [-0.1072, +0.0165] | 0.5667 (6/22/2) | **0.3833** (6/11/13) | -0.1833 * [-0.3667, -0.0167]; [-0.3549, -0.0156] |
| GPT-5.6 Luna (5 draws) | 0.5458 | **0.4956** | -0.0503 [-0.1573, +0.0510]; [-0.1101, +0.0206] | 0.6500 (19/1/10) | **0.7333** (22/0/8) | +0.0833 [-0.1333, +0.3000]; [-0.1609, +0.3201] |
| GPT-5.6 Sol (5 draws) | 0.5322 | **0.4636** | -0.0686 [-0.1411, +0.0024]; [-0.1200, -0.0157] | 0.5833 (17/1/12) | **0.4000** (12/0/18) | -0.1833 [-0.3833, +0.0167]; [-0.3971, +0.0179] |
| Opus 5 (1 draw; recorded row 5 draws) | 0.5872 | **0.5206** | -0.0667 * [-0.1376, -0.0049]; [-0.1584, -0.0087] | 0.7667 (22/2/6) | **0.5667** (14/6/10) | -0.2000 [-0.4171, +0.0500]; [-0.4500, +0.0470] |

## AUX-CFP-MINUS-LOOKUP-RETRACTED (descriptive): each model minus the embedding lookup, retraction (90 items / 30 triples)

| model | padded: pooled Δ (item; persona) | padded: matched Δ (triple; persona) | unpadded: pooled Δ (item; persona) | unpadded: matched Δ (triple; persona) |
|---|---|---|---|---|
| GPT-4.1 mini (5 draws) | +0.0597 [-0.1150, +0.2283]; [+0.0169, +0.1049] | +0.1667 [-0.0333, +0.3333]; [+0.0000, +0.3276] | +0.0761 [-0.0733, +0.2074]; [+0.0242, +0.1341] | +0.0667 [-0.1000, +0.2333]; [-0.1094, +0.2414] |
| Haiku 4.5 (5 draws) | +0.0014 [-0.1317, +0.1328]; [-0.0559, +0.0549] | -0.1167 [-0.2500, +0.0167]; [-0.2258, +0.0179] | +0.0433 [-0.1084, +0.1886]; [-0.0057, +0.0963] | +0.0667 [-0.0167, +0.1500]; [-0.0175, +0.1607] |
| GPT-5.6 Luna (5 draws) | -0.0044 [-0.1584, +0.1312]; [-0.0633, +0.0772] | +0.2333 * [+0.0667, +0.4000]; [+0.0806, +0.3667] | +0.0458 [-0.1317, +0.2113]; [-0.0229, +0.1293] | +0.1500 [-0.0167, +0.3167]; [-0.0485, +0.3214] |
| GPT-5.6 Sol (5 draws) | -0.0364 [-0.1970, +0.1175]; [-0.0909, +0.0223] | -0.1000 [-0.2667, +0.0667]; [-0.2813, +0.0938] | +0.0322 [-0.1325, +0.1983]; [-0.0216, +0.0887] | +0.0833 [-0.0833, +0.2500]; [-0.0893, +0.2500] |
| Opus 5 (1 draw; recorded row 5 draws) | +0.0206 [-0.1271, +0.1683]; [-0.0403, +0.0862] | +0.0667 [-0.0833, +0.2167]; [-0.0969, +0.2037] | +0.0872 [-0.0984, +0.2628]; [+0.0427, +0.1581] | +0.2667 * [+0.1167, +0.4000]; [+0.1111, +0.4118] |

## AUX-CFP-READERS-EXPIRED (descriptive): every reader, expiry (90 items / 30 triples), padded (60-name list) beside unpadded (recorded)

| reader | pooled unpadded | pooled padded | Δ pooled (item; persona) | matched unpadded (W/T/L) | matched padded (W/T/L) | Δ matched (triple; persona) |
|---|---:|---:|---|---|---|---|
| Embedding name lookup | 0.5000 | **0.5000** | +0.0000 [-0.1847, +0.1795]; [+0.0000, +0.0000] | 0.5000 (0/30/0) | **0.5000** (0/30/0) | +0.0000 [+0.0000, +0.0000]; [+0.0000, +0.0000] |
| Word-matching lookup | 0.5000 | **0.5000** | +0.0000 [-0.1031, +0.1034]; [+0.0000, +0.0000] | 0.5000 (0/30/0) | **0.5000** (0/30/0) | +0.0000 [+0.0000, +0.0000]; [+0.0000, +0.0000] |
| Random-token lookup | 0.5000 | **0.5000** | +0.0000 [-0.1500, +0.1483]; [+0.0000, +0.0000] | 0.5000 (0/30/0) | **0.5000** (0/30/0) | +0.0000 [+0.0000, +0.0000]; [+0.0000, +0.0000] |
| GPT-4.1 mini (5 draws) | 0.5594 | **0.5147** | -0.0447 [-0.1626, +0.0726]; [-0.1221, +0.0493] | 0.4000 (9/6/15) | **0.5500** (15/3/12) | +0.1500 [-0.0837, +0.4000]; [-0.0938, +0.4076] |
| Haiku 4.5 (5 draws) | 0.5794 | **0.5606** | -0.0189 [-0.1367, +0.1025]; [-0.0775, +0.0502] | 0.5833 (7/21/2) | **0.4833** (9/11/10) | -0.1000 [-0.2333, +0.0500]; [-0.2308, +0.0385] |
| GPT-5.6 Luna (5 draws) | 0.6167 | **0.5700** | -0.0467 [-0.1475, +0.0487]; [-0.1495, +0.0477] | 0.8667 (26/0/4) | **0.8000** (24/0/6) | -0.0667 [-0.2667, +0.1333]; [-0.2963, +0.1200] |
| GPT-5.6 Sol (5 draws) | 0.6403 | **0.5728** | -0.0675 [-0.1528, +0.0056]; [-0.1383, +0.0280] | 0.8333 (25/0/5) | **0.6667** (20/0/10) | -0.1667 [-0.3667, +0.0000]; [-0.3572, +0.0345] |
| Opus 5 (1 draw; recorded row 5 draws) | 0.6150 | **0.6031** | -0.0119 [-0.0944, +0.0752]; [-0.0770, +0.0443] | 0.6833 (20/1/9) | **0.6333** (17/4/9) | -0.0500 [-0.2333, +0.1333]; [-0.2069, +0.0968] |

## AUX-CFP-MINUS-LOOKUP-EXPIRED (descriptive): each model minus the embedding lookup, expiry (90 items / 30 triples)

| model | padded: pooled Δ (item; persona) | padded: matched Δ (triple; persona) | unpadded: pooled Δ (item; persona) | unpadded: matched Δ (triple; persona) |
|---|---|---|---|---|
| GPT-4.1 mini (5 draws) | +0.0147 [-0.1576, +0.1852]; [-0.0650, +0.1008] | +0.0500 [-0.1000, +0.2167]; [-0.1207, +0.2500] | +0.0594 [-0.0511, +0.1691]; [+0.0048, +0.1162] | -0.1000 [-0.2500, +0.0500]; [-0.2143, +0.0143] |
| Haiku 4.5 (5 draws) | +0.0606 [-0.0938, +0.2044]; [+0.0028, +0.1222] | -0.0167 [-0.1500, +0.1333]; [-0.1522, +0.1207] | +0.0794 [-0.0776, +0.2488]; [+0.0234, +0.1457] | +0.0833 [-0.0004, +0.1833]; [-0.0312, +0.2116] |
| GPT-5.6 Luna (5 draws) | +0.0700 [-0.0754, +0.2243]; [+0.0078, +0.1390] | +0.3000 * [+0.1333, +0.4333]; [+0.1250, +0.4310] | +0.1167 [-0.0278, +0.2642]; [+0.0432, +0.2213] | +0.3667 * [+0.2333, +0.4667]; [+0.2586, +0.4677] |
| GPT-5.6 Sol (5 draws) | +0.0728 [-0.0680, +0.2253]; [+0.0255, +0.1262] | +0.1667 [+0.0000, +0.3333]; [-0.0203, +0.3387] | +0.1403 [-0.0055, +0.3087]; [+0.0497, +0.2432] | +0.3333 * [+0.2000, +0.4667]; [+0.2000, +0.4394] |
| Opus 5 (1 draw; recorded row 5 draws) | +0.1031 [-0.0423, +0.2504]; [+0.0241, +0.1932] | +0.1333 [-0.0333, +0.3000]; [-0.0601, +0.3002] | +0.1150 [-0.0242, +0.2573]; [+0.0443, +0.2008] | +0.1833 [+0.0167, +0.3333]; [+0.0000, +0.3750] |

## AUX-CFP-MINUS-LEX-SUPERSEDED (descriptive): each model minus the word-matching lookup, supersession

| model | padded: pooled Δ (item; persona) | padded: matched Δ (triple; persona) | unpadded: pooled Δ (item; persona) | unpadded: matched Δ (triple; persona) |
|---|---|---|---|---|
| GPT-4.1 mini (5 draws) | -0.0001 [-0.0583, +0.0618]; [-0.0432, +0.0470] | +0.0398 [-0.0456, +0.1193]; [-0.0523, +0.1209] | +0.0964 * [+0.0457, +0.1457]; [+0.0394, +0.1500] | +0.1080 * [+0.0455, +0.1648]; [+0.0460, +0.1701] |
| Haiku 4.5 (5 draws) | +0.0461 [-0.0224, +0.1203]; [-0.0068, +0.1058] | +0.0568 [-0.0057, +0.1193]; [-0.0102, +0.1236] | +0.1046 * [+0.0519, +0.1607]; [+0.0544, +0.1550] | +0.1307 * [+0.0625, +0.1932]; [+0.0671, +0.1848] |
| GPT-5.6 Luna (5 draws) | +0.1898 * [+0.1284, +0.2596]; [+0.1478, +0.2345] | +0.1875 * [+0.1250, +0.2500]; [+0.1321, +0.2408] | +0.1597 * [+0.1170, +0.2069]; [+0.1173, +0.2031] | +0.1761 * [+0.1193, +0.2330]; [+0.1123, +0.2371] |
| GPT-5.6 Sol (5 draws) | +0.1798 * [+0.1162, +0.2491]; [+0.1307, +0.2347] | +0.1761 * [+0.1078, +0.2330]; [+0.1131, +0.2384] | +0.1554 * [+0.1052, +0.2065]; [+0.1082, +0.2033] | +0.1761 * [+0.1193, +0.2273]; [+0.1169, +0.2338] |
| Opus 5 (1 draw; recorded row 5 draws) | +0.0188 [-0.0578, +0.0985]; [-0.1126, +0.1371] | +0.0398 [-0.0682, +0.1307]; [-0.1044, +0.1685] | +0.1496 * [+0.1033, +0.1975]; [+0.1025, +0.2040] | +0.1932 * [+0.1364, +0.2443]; [+0.1319, +0.2581] |

## AUX-CFP-MINUS-RANDTOK-SUPERSEDED (descriptive): each model minus the random-token lookup, supersession

| model | padded: pooled Δ (item; persona) | padded: matched Δ (triple; persona) | unpadded: pooled Δ (item; persona) | unpadded: matched Δ (triple; persona) |
|---|---|---|---|---|
| GPT-4.1 mini (5 draws) | +0.1883 * [+0.0859, +0.2888]; [+0.1308, +0.2541] | +0.2784 * [+0.1875, +0.3636]; [+0.1768, +0.3667] | +0.2142 * [+0.1330, +0.2880]; [+0.1414, +0.2773] | +0.1477 * [+0.0682, +0.2330]; [+0.0517, +0.2283] |
| Haiku 4.5 (5 draws) | +0.2345 * [+0.1292, +0.3352]; [+0.1768, +0.2956] | +0.2955 * [+0.2330, +0.3580]; [+0.2267, +0.3625] | +0.2225 * [+0.1458, +0.3007]; [+0.1563, +0.2868] | +0.1705 * [+0.0966, +0.2443]; [+0.0933, +0.2446] |
| GPT-5.6 Luna (5 draws) | +0.3782 * [+0.2940, +0.4694]; [+0.3330, +0.4216] | +0.4261 * [+0.3693, +0.4773]; [+0.3750, +0.4696] | +0.2775 * [+0.2112, +0.3433]; [+0.2150, +0.3308] | +0.2159 * [+0.1420, +0.2898]; [+0.1333, +0.2895] |
| GPT-5.6 Sol (5 draws) | +0.3682 * [+0.2758, +0.4599]; [+0.3179, +0.4155] | +0.4148 * [+0.3523, +0.4659]; [+0.3500, +0.4695] | +0.2732 * [+0.2084, +0.3406]; [+0.2123, +0.3266] | +0.2159 * [+0.1420, +0.2899]; [+0.1306, +0.2957] |
| Opus 5 (1 draw; recorded row 5 draws) | +0.2072 * [+0.1082, +0.3065]; [+0.0969, +0.3031] | +0.2784 * [+0.1875, +0.3581]; [+0.1511, +0.3896] | +0.2674 * [+0.1977, +0.3366]; [+0.2051, +0.3244] | +0.2330 * [+0.1648, +0.3011]; [+0.1648, +0.3023] |

## AUX-CFP-P-L1 … P-L4

- **P-L1 FAILS.** Model minus the embedding lookup, pooled AUROC, supersession, 60-name list: GPT-5.6 Luna +0.1375 item [+0.0883, +0.1934] persona [+0.0971, +0.1777] (reliably above); Opus 5 -0.0336 item [-0.1070, +0.0448] persona [-0.1597, +0.0748] (not reliably above); GPT-5.6 Sol +0.1274 item [+0.0726, +0.1837] persona [+0.0802, +0.1726] (reliably above).
- **P-L2 HOLDS.** Model minus the embedding lookup, pooled AUROC, supersession, 60-name list: Haiku 4.5 -0.0062 item [-0.0652, +0.0515] persona [-0.0558, +0.0464] (not reliably above); GPT-4.1 mini -0.0525 item [-0.1065, +0.0041] persona [-0.1092, +0.0058] (not reliably above).
- **P-L3 HOLDS.** The embedding lookup's padded minus unpadded pooled AUROC on supersession: -0.1807, item [-0.2420, -0.1272], persona [-0.2335, -0.1311] (holds iff below −0.05 with both intervals below zero).
- **P-L4 FAILS.** Padded minus unpadded pooled AUROC on supersession, point estimates: GPT-5.6 Luna -0.0636 against the lookup's -0.1807 (loses less); Opus 5 -0.2245 against the lookup's -0.1807 (does not lose less); GPT-5.6 Sol -0.0693 against the lookup's -0.1807 (loses less).

## AUX-CFP-POSITION (descriptive): the target's alphabetical rank in the PN list (88 supersession triples) against each reader

Rank histogram (rank: triples): 2: 1, 4: 3, 5: 1, 11: 1, 12: 2, 17: 1, 18: 1, 20: 1, 24: 4, 25: 3, 26: 1, 27: 1, 28: 2, 30: 1, 31: 1, 32: 1, 33: 2, 34: 1, 35: 3, 36: 4, 38: 2, 39: 2, 40: 1, 41: 4, 42: 3, 43: 1, 44: 4, 47: 2, 48: 2, 49: 2, 50: 1, 51: 3, 52: 2, 53: 1, 55: 3, 56: 9, 57: 1, 58: 4, 59: 2, 60: 4.

| reader | Spearman rank vs PN score | Spearman rank vs PN-vs-PRESENT outcome | matched by tenth of the list (1 = ranks 1–6 … 10 = ranks 55–60) |
|---|---:|---:|---|
| Embedding name lookup | 0.3264 | 0.2040 | 1: 0.9000 (n 5), 2: 0.8333 (n 3), 3: 0.5000 (n 2), 4: 0.6000 (n 5), 5: 0.6875 (n 8), 6: 0.8333 (n 12), 7: 0.9167 (n 12), 8: 0.8889 (n 9), 9: 0.8333 (n 9), 10: 0.8696 (n 23) |
| Word-matching lookup | 0.3316 | 0.1612 | 1: 0.9000 (n 5), 2: 0.6667 (n 3), 3: 0.5000 (n 2), 4: 0.6000 (n 5), 5: 0.6250 (n 8), 6: 0.6250 (n 12), 7: 0.8750 (n 12), 8: 0.7778 (n 9), 9: 0.7778 (n 9), 10: 0.7826 (n 23) |
| Random-token lookup | -0.0496 | -0.0613 | 1: 0.5000 (n 5), 2: 0.5000 (n 3), 3: 0.5000 (n 2), 4: 0.5000 (n 5), 5: 0.5000 (n 8), 6: 0.5417 (n 12), 7: 0.5000 (n 12), 8: 0.5000 (n 9), 9: 0.5000 (n 9), 10: 0.5000 (n 23) |
| GPT-4.1 mini (5 draws) | 0.1434 | 0.2762 | 1: 1.0000 (n 5), 2: 0.6667 (n 3), 3: 0.7500 (n 2), 4: 0.1000 (n 5), 5: 0.6250 (n 8), 6: 0.6667 (n 12), 7: 0.9167 (n 12), 8: 0.7778 (n 9), 9: 1.0000 (n 9), 10: 0.8696 (n 23) |
| Haiku 4.5 (5 draws) | 0.1647 | 0.2717 | 1: 0.8000 (n 5), 2: 0.8333 (n 3), 3: 0.2500 (n 2), 4: 0.5000 (n 5), 5: 0.5625 (n 8), 6: 0.8750 (n 12), 7: 0.8333 (n 12), 8: 1.0000 (n 9), 9: 0.8889 (n 9), 10: 0.8261 (n 23) |
| GPT-5.6 Luna (5 draws) | 0.2634 | 0.1199 | 1: 1.0000 (n 5), 2: 0.6667 (n 3), 3: 1.0000 (n 2), 4: 0.6000 (n 5), 5: 1.0000 (n 8), 6: 0.9167 (n 12), 7: 1.0000 (n 12), 8: 0.8889 (n 9), 9: 1.0000 (n 9), 10: 0.9565 (n 23) |
| GPT-5.6 Sol (5 draws) | 0.2388 | -0.0546 | 1: 1.0000 (n 5), 2: 1.0000 (n 3), 3: 1.0000 (n 2), 4: 0.8000 (n 5), 5: 0.8750 (n 8), 6: 1.0000 (n 12), 7: 0.9167 (n 12), 8: 0.8889 (n 9), 9: 1.0000 (n 9), 10: 0.8696 (n 23) |
| Opus 5 (1 draw; recorded row 5 draws) | 0.0467 | 0.0172 | 1: 0.6000 (n 5), 2: 1.0000 (n 3), 3: 0.5000 (n 2), 4: 0.8000 (n 5), 5: 0.5000 (n 8), 6: 1.0000 (n 12), 7: 0.9167 (n 12), 8: 0.7778 (n 9), 9: 0.8333 (n 9), 10: 0.7174 (n 23) |

## AUX-CFP-OP5-D1 (descriptive): Opus 5's padded one draw beside its recorded draw 1 alone

- superseded: recorded draw 1 pooled 0.9317, matched 0.9716; padded minus recorded draw 1, pooled -0.2236 * [-0.2776, -0.1690]; [-0.3416, -0.1294]
- whole: recorded draw 1 pooled 0.8400, matched 0.8682; padded minus recorded draw 1, pooled -0.1873 * [-0.2277, -0.1476]; [-0.2569, -0.1278]

## AUX-CFP-SEEDS (descriptive): seeds 43–46 on the registered pooled differences, supersession (both intervals exclude zero?)

| difference | 43 (item; persona) | 44 | 45 | 46 |
|---|---|---|---|---|
| H45_minus_LOOKUP | False; False | False; False | False; False | False; False |
| H45_padded_minus_unpadded | True; True | True; True | True; True | True; True |
| LEX_padded_minus_unpadded | True; True | True; True | True; True | True; True |
| LOOKUP_padded_minus_unpadded | True; True | True; True | True; True | True; True |
| LUNA_minus_LOOKUP | True; True | True; True | True; True | True; True |
| LUNA_padded_minus_unpadded | True; True | True; True | True; True | True; True |
| MINI_minus_LOOKUP | False; False | False; False | False; True | False; False |
| MINI_padded_minus_unpadded | True; True | True; True | True; True | True; True |
| OP5_minus_LOOKUP | False; False | False; False | False; False | False; False |
| OP5_padded_minus_unpadded | True; True | True; True | True; True | True; True |
| RANDTOK_padded_minus_unpadded | True; True | True; True | True; True | True; True |
| SOL_minus_LOOKUP | True; True | True; True | True; True | True; True |
| SOL_padded_minus_unpadded | True; True | True; True | True; True | True; True |

## AUX-CFP-SPEND

- anthropic: **$8.1105** against the $12.00 cap ({'H45 probe': 0.003075, 'H45 rows': 3.3115, 'OP5 probe': 0.018285, 'OP5 rows': 4.7777}); token-metered from the rows at the registration's page prices, Batch at 50%; not an invoice.
- openai: **$15.5370** against the $20.00 cap ({'LUNA probe': 0.00064, 'LUNA rows': 0.873, 'MINI probe': 0.00081, 'MINI rows': 1.5307, 'SOL probe': 0.012252, 'SOL rows': 13.1196}); token-metered from the rows at the registration's page prices, Batch at 50%; not an invoice.

## Deviations

none
