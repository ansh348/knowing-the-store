# NUMBERS_CF3 — ledger for the CF-3 expiry cell (ADDENDUM_CF3)

Registration: `registrations/ADDENDUM_CF3.md`, registered text sha256
`2f555c1ac4c3018e66a0fc453be7c4c4d3ffd4e3a2f7ac63c5c7b3590ca4f910` (the bytes above the marker line; the author's
ratification line is appended below it), recorded here before the first call on 2026-09-14. Descriptive: no
prediction, no bar, no verdict. The census that fixed the population: `cf3/census_cf3.json` sha256 `b1c9cf1e292dfbb7…`
(commit `ba922af`). Every number for this cell enters the manuscript through a key in this file and no other way.

## 0. Status

| item | state |
|---|---|
| Registration | sha256 recorded above before any call; the run ordered by the author's message of 2026-09-14 (quoted at the head of the registration); the ratification line drafted below its marker, pending |
| Locks (§6) | registration sha256 holds; census sha256 holds; all 14 pairs ELIGIBLE in `cf2/adjudication_cf2.json` (11 CF-1 reused, 3 author 2026-09-12); none in the 444 by (persona, entry id) |
| Calls made | none at this line |

## 1. AUX-CF3-LOCK, AUX-CF3-QUESTIONS, AUX-CF3-CELL, AUX-CF3-LEAK — the build (`cf3_build.py`)

| Key | Value |
|---|---|
| **AUX-CF3-LOCK** | Registration sha256 holds; census sha256 `b1c9cf1e292dfbb7…` holds; 14 pairs, every one ELIGIBLE in `cf2/adjudication_cf2.json` (11 CF-1 reused, 3 author 2026-09-12); none in the 444 by (persona, entry id); overlap tags as CF-2 admitted them: cf3:priya:project_deadline:NeurIPS_paper O1, cf3:raj:course:regulatory_update O2, cf3:raj:training_course:boiler_refresher O2, cf3:thanh:event_guest_count:duc_wedding O1, cf3:thanh:wedding_menu O2. |
| **AUX-CF3-QUESTIONS** | The frozen CF-1 renderer (prompt sha256 `b748247b3ff380d8…`, `gpt-4.1-mini`, temperature 0, seed 42): 14 questions, 0 redrafts, 1 substitution, questions sha256 **`75fee108042176cd6217228b24b413510884462fcb25fe14cbf07f52ade30e61`**, $0.0028. |
| **AUX-CF3-CELL** | 42 items (0/0/14 = supersession / retraction / expiry pairs), 14 PN positives; assertions A–E, the draw-time predicates and assertion C hold on 14 of 14; indexes sha256 `b2d6441fd1b99a4b…`, v2r sha256 `7e90e43c5b20f48a…` (a derangement within the cell's 42 versions, rotation k = 28, 15 distinct (retracted, expired) values, 0 versions keeping their own pair); summaries 60–66 lines (v2). |
| **AUX-CF3-LEAK** | v2: 0 of 14 correct (leaks iff more than 1) — PASS; v2r: 0 of 14 correct (leaks iff more than 1) — PASS; v3: 0 of 14 correct (leaks iff more than 1) — PASS; served `gpt-4.1-mini-2025-04-14`; $0.0206. |

## 2. AUX-CF3-PROBE-*, AUX-CF3-PROJECTION — the lanes before submission (`cf3_run.py probe / project`)

| Key | Value |
|---|---|
| **AUX-CF3-PROBE-HAIKU** | served `claude-haiku-4-5-20251001` (PASS); prompt tokens blind 525, v2 1745, v3 1798; completion [39, 200, 200]. |
| **AUX-CF3-PROBE-OPUS** | served `claude-opus-5` (PASS); prompt tokens blind 697, v2 2463, v3 2559; completion [132, 185, 144]. |
| **AUX-CF3-PROBE-GPT-4.1** | served `gpt-4.1-mini-2025-04-14` (PASS); prompt tokens blind 482, v2 1640, v3 1688; completion [26, 21, 24]. |
| **AUX-CF3-PROJECTION** | mini 140 calls $0.09, Haiku 4.5 700 calls $0.83, Opus 5 140 calls $1.08 — $2.00 (×1.3 $2.60) against the $5 line (`cf3_run.py project`). |

## 3. AUX-CF3-LOOKUP-*, AUX-CF3-{MINI,H45,OP5}-*, AUX-CF3-POOLED-* — the scores (`cf3_score.py`; `results/cf_scores_cf3.json`)

Blind is one call per question, reused across its three versions, so blind AUROC is 0.5000 by identity on every set and each AUROC is also a gain. Intervals: item-level paired bootstrap (1,000 draws, seed 42) and persona-clustered, `*` excludes zero; the weaker reading governs. Model − lookup: the model's row minus the embedding lookup on the same summary (v2 and v2r against the superseded-names lookup, v3 against the all-states lookup), same construction as `AUX-R103-MARGIN`. Gate: the CF-2 expiry slice's lookups reproduce `AUX-CF2-NB6-V2` / `AUX-CF2-ALLSTATES-V3` per state (embedding v2 0.5000, v3 0.8711: PASS).

**AUX-CF3-CF2SLICE** — CF-2 expiry slice: 30 pairs, 90 items (recorded rows) (90 items, 30 positives, 15 personas).

| reader | summary | AUROC | Δ vs blind (item CI; persona CI) | model − embedding lookup (weaker CI) | model − lexical lookup (weaker CI) |
|---|---|---:|---|---|---|
| embedding lookup, superseded names (v2) | — | **0.5000** | persona CI of the AUROC [0.5000, 0.5000] | — | — |
| lexical lookup, superseded names (v2) | — | **0.5000** | persona CI of the AUROC [0.5000, 0.5000] | — | — |
| embedding lookup, all states (v3) | — | **0.8711** | persona CI of the AUROC [0.7864, 0.9424] | — | — |
| lexical lookup, all states (v3) | — | **0.8244** | persona CI of the AUROC [0.7477, 0.9000] | — | — |
| Haiku 4.5 | v2 | **0.5794** | +0.0794; item [-0.0626, +0.2182]; persona [+0.0234, +0.1457]* | +0.0794 [-0.0776, +0.2488] | +0.0794 [-0.0295, +0.1829] |
| Haiku 4.5 | v3 | **0.8269** | +0.3269; item [+0.1935, +0.4675]*; persona [+0.2388, +0.4156]* | -0.0442 [-0.1387, +0.0449] | +0.0025 [-0.1053, +0.1111] |
| Haiku 4.5 | v2r | **0.5847** | +0.0847; item [-0.0594, +0.2188]; persona [+0.0351, +0.1414]* | +0.0847 [-0.0761, +0.2569] | +0.0847 [-0.0249, +0.1849] |
| Haiku 4.5 | v2r − v2 | — | +0.0053; item [-0.0375, +0.0503]; persona [-0.0370, +0.0504] | — | — |
| Opus 5 | v2 | **0.6150** | +0.1150; item [+0.0077, +0.2282]*; persona [+0.0443, +0.2008]* | +0.1150 [-0.0242, +0.2573] | +0.1150 [-0.0069, +0.2310] |
| Opus 5 | v3 | **0.9267** | +0.4267; item [+0.2974, +0.5637]*; persona [+0.3576, +0.4787]* | +0.0556 [-0.0236, +0.1380] | +0.1022 [+0.0169, +0.1922]* |
| Opus 5 | v2r | **0.6092** | +0.1092; item [+0.0008, +0.2140]*; persona [+0.0401, +0.1985]* | +0.1092 [-0.0325, +0.2447] | +0.1092 [-0.0121, +0.2217] |
| Opus 5 | v2r − v2 | — | -0.0058; item [-0.0556, +0.0392]; persona [-0.0581, +0.0381] | — | — |
| GPT-4.1 mini | v2 | **0.5489** | +0.0489; item [-0.1022, +0.1893]; persona [-0.0200, +0.1293] | +0.0489 [-0.0705, +0.1711] | +0.0489 [-0.0467, +0.1522] |
| GPT-4.1 mini | v3 | **0.5869** | +0.0869; item [-0.0524, +0.2230]; persona [+0.0127, +0.1684]* | -0.2842 [-0.4114, -0.1716]* | -0.2375 [-0.3629, -0.1305]* |
| GPT-4.1 mini | v2r | **0.5144** | +0.0144; item [-0.1317, +0.1534]; persona [-0.0576, +0.0840] | +0.0144 [-0.1214, +0.1481] | +0.0144 [-0.0944, +0.1205] |
| GPT-4.1 mini | v2r − v2 | — | -0.0344; item [-0.1175, +0.0504]; persona [-0.1082, +0.0603] | — | — |

**AUX-CF3** — CF-3 expiry cell: 14 pairs, 42 items (42 items, 14 positives, 7 personas).

| reader | summary | AUROC | Δ vs blind (item CI; persona CI) | model − embedding lookup (weaker CI) | model − lexical lookup (weaker CI) |
|---|---|---:|---|---|---|
| embedding lookup, superseded names (v2) | — | **0.5000** | persona CI of the AUROC [0.5000, 0.5000] | — | — |
| lexical lookup, superseded names (v2) | — | **0.5000** | persona CI of the AUROC [0.5000, 0.5000] | — | — |
| embedding lookup, all states (v3) | — | **0.9694** | persona CI of the AUROC [0.9475, 1.0000] | — | — |
| lexical lookup, all states (v3) | — | **0.8929** | persona CI of the AUROC [0.7781, 1.0000] | — | — |
| Haiku 4.5 | v2 | **0.6059** | +0.1059; item [-0.0441, +0.2595]; persona [+0.0385, +0.1790]* | +0.1059 [-0.1000, +0.3149] | +0.1059 [-0.0821, +0.2766] |
| Haiku 4.5 | v3 | **0.9630** | +0.4630; item [+0.2917, +0.6377]*; persona [+0.4422, +0.5000]* | -0.0064 [-0.0612, +0.0293] | +0.0702 [+0.0000, +0.1817] |
| Haiku 4.5 | v2r | **0.6212** | +0.1212; item [-0.0321, +0.2577]; persona [+0.0312, +0.2840]* | +0.1212 [-0.0802, +0.3126] | +0.1212 [-0.0727, +0.2837] |
| Haiku 4.5 | v2r − v2 | — | +0.0153; item [-0.1212, +0.1422]; persona [-0.0573, +0.1570] | — | — |
| Opus 5 | v2 | **0.5638** | +0.0638; item [-0.1078, +0.2431]; persona [-0.0867, +0.2840] | +0.0638 [-0.0867, +0.2840] | +0.0638 [-0.0867, +0.2840] |
| Opus 5 | v3 | **0.9452** | +0.4452; item [+0.2593, +0.6318]*; persona [+0.3828, +0.4941]* | -0.0242 [-0.0898, +0.0000] | +0.0523 [-0.0525, +0.1813] |
| Opus 5 | v2r | **0.6084** | +0.1084; item [-0.0830, +0.2792]; persona [+0.0210, +0.2480]* | +0.1084 [-0.0539, +0.2716] | +0.1084 [-0.0682, +0.2799] |
| Opus 5 | v2r − v2 | — | +0.0446; item [-0.0397, +0.1306]; persona [-0.0625, +0.1921] | — | — |
| GPT-4.1 mini | v2 | **0.5421** | +0.0421; item [-0.1446, +0.2222]; persona [-0.0334, +0.1467] | +0.0421 [-0.1550, +0.2386] | +0.0421 [-0.1358, +0.2087] |
| GPT-4.1 mini | v3 | **0.6811** | +0.1811; item [-0.0308, +0.3901]; persona [-0.0173, +0.3951] | -0.2883 [-0.4981, -0.1015]* | -0.2117 [-0.3979, -0.0641]* |
| GPT-4.1 mini | v2r | **0.5651** | +0.0651; item [-0.1021, +0.2373]; persona [+0.0222, +0.1049]* | +0.0651 [-0.1181, +0.2569] | +0.0651 [-0.0993, +0.2250] |
| GPT-4.1 mini | v2r − v2 | — | +0.0230; item [-0.1220, +0.1833]; persona [-0.0982, +0.1175] | — | — |

**AUX-CF3-POOLED** — pooled expiry: CF-2's 30 pairs + CF-3's 14 = 44 pairs, 132 items (two cells, two dates, two registrations; Opus 5 k = 5 on CF-2's rows, k = 1 on CF-3's) (132 items, 44 positives, 22 personas).

| reader | summary | AUROC | Δ vs blind (item CI; persona CI) | model − embedding lookup (weaker CI) | model − lexical lookup (weaker CI) |
|---|---|---:|---|---|---|
| embedding lookup, superseded names (v2) | — | **0.5000** | persona CI of the AUROC [0.5000, 0.5000] | — | — |
| lexical lookup, superseded names (v2) | — | **0.5000** | persona CI of the AUROC [0.5000, 0.5000] | — | — |
| embedding lookup, all states (v3) | — | **0.8977** | persona CI of the AUROC [0.8376, 0.9477] | — | — |
| lexical lookup, all states (v3) | — | **0.8453** | persona CI of the AUROC [0.7806, 0.9073] | — | — |
| Haiku 4.5 | v2 | **0.5872** | +0.0872; item [-0.0307, +0.1932]; persona [+0.0470, +0.1366]* | +0.0872 [-0.0490, +0.2188] | +0.0872 [-0.0089, +0.1784] |
| Haiku 4.5 | v3 | **0.8644** | +0.3644; item [+0.2552, +0.4676]*; persona [+0.2924, +0.4326]* | -0.0333 [-0.0981, +0.0306] | +0.0191 [-0.0575, +0.1009] |
| Haiku 4.5 | v2r | **0.5980** | +0.0980; item [-0.0186, +0.2056]; persona [+0.0531, +0.1505]* | +0.0980 [-0.0387, +0.2336] | +0.0980 [+0.0021, +0.1871]* |
| Haiku 4.5 | v2r − v2 | — | +0.0108; item [-0.0341, +0.0587]; persona [-0.0257, +0.0521] | — | — |
| Opus 5 (k = 5 on the CF-2 rows, k = 1 on the CF-3 rows) | v2 | **0.5914** | +0.0914; item [-0.0061, +0.1930]; persona [+0.0303, +0.1593]* | +0.0914 [-0.0320, +0.2124] | +0.0914 [-0.0121, +0.1946] |
| Opus 5 (k = 5 on the CF-2 rows, k = 1 on the CF-3 rows) | v3 | **0.9232** | +0.4232; item [+0.3246, +0.5218]*; persona [+0.3769, +0.4654]* | +0.0254 [-0.0262, +0.0815] | +0.0779 [+0.0109, +0.1486]* |
| Opus 5 (k = 5 on the CF-2 rows, k = 1 on the CF-3 rows) | v2r | **0.6068** | +0.1068; item [+0.0115, +0.1974]*; persona [+0.0587, +0.1779]* | +0.1068 [-0.0116, +0.2231] | +0.1068 [+0.0024, +0.2055]* |
| Opus 5 | v2r − v2 | — | +0.0154; item [-0.0264, +0.0593]; persona [-0.0287, +0.0686] | — | — |
| GPT-4.1 mini | v2 | **0.5461** | +0.0461; item [-0.0628, +0.1585]; persona [-0.0054, +0.1135] | +0.0461 [-0.0508, +0.1473] | +0.0461 [-0.0411, +0.1322] |
| GPT-4.1 mini | v3 | **0.6139** | +0.1139; item [-0.0042, +0.2198]; persona [+0.0349, +0.2030]* | -0.2838 [-0.3762, -0.1819]* | -0.2314 [-0.3323, -0.1367]* |
| GPT-4.1 mini | v2r | **0.5302** | +0.0302; item [-0.0797, +0.1325]; persona [-0.0208, +0.0782] | +0.0302 [-0.0845, +0.1375] | +0.0302 [-0.0562, +0.1157] |
| GPT-4.1 mini | v2r − v2 | — | -0.0159; item [-0.0943, +0.0595]; persona [-0.0838, +0.0544] | — | — |

**AUX-CF3-PRINTED** — the two-decimal forms Appendix D.2's prose prints, against their four-decimal sources in this file (the R97/R102 printed-forms convention):

| printed | source |
|---|---|
| 0.97 | 0.9694 (AUX-CF3, all-states lookup, v3) |
| 0.68 | 0.6811 (AUX-CF3, GPT-4.1 mini, v3) |

## 4. AUX-CF3-CENSUS — the sizing census the population rests on (`census_cf3.py`, `CF3_CENSUS.md`; no call)

| Key | Value |
|---|---|
| **AUX-CF3-CENSUS-MANIFEST** | The 40 manifests record **40 retraction events** (one per persona), **9** of which resolve to a retracted entry under the truthful join (index_v2.true_lifecycle, TAU_HI; 23 entries in all), against 31 entries the store marks retracted; 85 expired logistics records, 79 resolving (276 entries). |
| **AUX-CF3-CENSUS-RETRACTION** | Under the CF-2 predicates 1,018 retraction candidates entered the queue; the author's eligibility read (ADDENDUM_CF2 §3.1) left **36 ELIGIBLE among the 370 candidates carrying a verdict** (35 of the 369 the author read plus one CF-1 verdict reused; rate 0.0949, about one in ten; 578 unread); 30 used; the name rule (`project` on 336 of the 578 unread) bounds any extension more than the predicates do. Retraction stays at 30 by the author's ruling of 2026-09-14. |
| **AUX-CF3-CENSUS-EXPIRY** | 70 expiry candidates entered the queue and every one was read: 49 ELIGIBLE, 30 used, 19 undrawn, **14 fitting the cap and the name rule** — the population of this addendum. |

## 5. AUX-CF3-SPEND

| Key | Value |
|---|---|
| **AUX-CF3-SPEND** | drafting $0.0028; leakage screen $0.0206; probe Haiku 4.5 (3 calls); probe Opus 5 (3 calls); probe GPT-4.1 mini (3 calls); GPT-4.1 mini lane $0.0907 (140 rows, 0 not OK); Haiku 4.5 lane $0.8765 (700 rows, 0 not OK); Opus 5 lane $1.2208 (140 rows, 0 not OK); **total $2.2113** metered from the rows at list / Batch prices against the $5 line (probes metered in the lanes' probe files). |
