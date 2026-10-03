# NUMBERS_PAD — ledger for the padding probe (ADDENDUM_PAD) and its Amendment 1

Registration: `registrations/ADDENDUM_PAD.md`, registered text sha256 `93e330225eba5168bd129df565c2c7594883ec830dd1a4ab0f23123520ee32fe` (the bytes above the marker line; Amendment 1 appended below it), frozen at `dab8956` on 2026-09-14 by the author's instruction. Descriptive: no prediction, no bar, no verdict; the §5 branches print as they come out. Every number for this probe enters the manuscript through a key in this file and no other way. Deviations and settled readings: `pad_probe/DEVIATIONS_PAD.md` (D-PAD-1 to D-PAD-5).

## 1. AUX-PAD-LOCK — the build (`tools/pad_common.py`, `tools/run_pad.py build`; `build/build_pad.json`, `build/padded_lists.json`, `build/padded_texts.json`)

| Key | Value |
|---|---|
| **AUX-PAD-LOCK** | Registration sha256 holds; `prompts_e1` digests hold. **661 items, 242 keys.** Renderer lock: the superseded section re-rendered over the committed names alone under the lifted cap reproduces the committed text byte for byte on **242 of 242** keys. Longest committed list 5 names (marker-cleaned; D-PAD-5); committed mean 1.7474 names per item as committed (1.4523 marker-free). Pools: pool A (the key's own printed map names after exclusions i–iii) min 50, median 103, max 128; pool B (other personas' FULL:TRUE map names) min 2894, median 2912, max 2943. Names drawn from pool A / pool B: L=15: 3261 / 0 (0 keys reach pool B); L=30: 6891 / 0 (0 keys reach pool B); L=60: 14135 / 16 (3 keys reach pool B). Every padded list asserted: exactly L names, no excluded name in the padding, no `:`, no duplicate, the committed names kept, the three lengths nested (D-PAD-1). Exclusion (ii) applied as the rule states it (D-PAD-2): the padding names a negative's own attribute on 22 negatives at every L, exactly the 22 the committed list already names, and a positive's own on 74 positives, the committed 74. Padded texts sha256 `ae472fb1cedef1c2…`. |
| **AUX-PAD-GATE** | The committed lists through `run_nb6.lex_scores` / `emb_scores` (as committed, marker included): embedding **0.7484**, lexical **0.5738** — `AUX-E1R-NB6` at four decimals, **PASS**. Mini's recorded `INDEXED-TRUE` row 0.7339 (registered 0.7339). Marker-stripped base, descriptive (D-E1R-11): embedding 0.7442, lexical 0.5738. |
| **AUX-PAD-PROBE** | Three direct calls (one item at each L): served `gpt-4.1-mini-2025-04-14` on all three (E1.7 rule, PASS); prompt tokens 1732, 1591, 1942; completion tokens 24, 24, 24; probe $0.0022. |
| **AUX-PAD-PROJECTION** | 1983 calls; o200k token count over every prompt calibrated by the probe (ratio 1.0064): mean prompt tokens 1604 / 1664 / 1785 at L = 15 / 30 / 60; **$1.41** (×1.3 $1.84) against the $2.50 line and the combined $15 headroom (first lane: $15.00) — under both. |
| **AUX-PAD-MINI-RUN** | 1983 calls (0 cached), 3,341,109 in / 47,110 out tokens, **$1.4118** metered at list price; retried after a parse failure: 0; elicitation failures {'15': 0, '30': 0, '60': 0}; 266 s; JSON mode, temperature 0, seed 42, max_tokens 200, served `gpt-4.1-mini-2025-04-14`. |

## 2. AUX-PAD-LOOKUP-EMB, AUX-PAD-LOOKUP-LEX, AUX-PAD-MINI — AUROC by length, whole and per state, paired against the 1.75-name row (`tools/run_pad.py score`; `results/pad_scores.json`)

Whole population n = 661 (104 positives); per state = that state's positives against the same 557 negatives (`nb6_composition`'s construction). Paired difference = padded − recorded, item by item; item-level paired bootstrap (1,000 draws, seed 42, single-class draws discarded) and persona-clustered paired bootstrap; `*` marks an interval excluding zero; where the two disagree the weaker reading governs. Tolerance ±0.05 on the point estimate.

**AUX-PAD-LOOKUP-EMB** — embedding lookup (BELIEVED row 0.5858).

| length | whole | Δ vs 1.75 (item CI, persona CI) | superseded | Δ | retracted | Δ | expired | Δ |
|---|---:|---|---:|---|---:|---|---:|---|
| 1.75 (recorded) | **0.7484** | — | 0.9534 | — | 0.4053 | — | 0.4823 | — |
| 15 | **0.7298** | -0.0186; item [-0.0777, +0.0400], persona [-0.0917, +0.0522] | 0.8213 | -0.1321, weaker [-0.1976, -0.0756]* | 0.5508 | +0.1455, weaker [-0.0564, +0.3301] | 0.6560 | +0.1737, weaker [-0.1888, +0.4610] |
| 30 | **0.7191** | -0.0293; item [-0.0968, +0.0392], persona [-0.1156, +0.0525] | 0.7935 | -0.1599, weaker [-0.2335, -0.0943]* | 0.5438 | +0.1386, weaker [-0.1042, +0.3291] | 0.7105 | +0.2282, weaker [-0.0508, +0.4832] |
| 60 | **0.6696** | -0.0788; item [-0.1541, -0.0096]*, persona [-0.1794, +0.0284] — disagree, the weaker governs | 0.7466 | -0.2068, weaker [-0.2923, -0.1276]* | 0.4822 | +0.0769, weaker [-0.2387, +0.3365] | 0.6710 | +0.1887, weaker [-0.0962, +0.4948] |

**AUX-PAD-LOOKUP-LEX** — lexical lookup (BELIEVED row 0.4718).

| length | whole | Δ vs 1.75 (item CI, persona CI) | superseded | Δ | retracted | Δ | expired | Δ |
|---|---:|---|---:|---|---:|---|---:|---|
| 1.75 (recorded) | **0.5738** | — | 0.6241 | — | 0.4964 | — | 0.4964 | — |
| 15 | **0.5772** | +0.0034; item [-0.0296, +0.0398], persona [-0.0367, +0.0501] | 0.6404 | +0.0162, weaker [-0.0415, +0.0835] | 0.4891 | -0.0073, weaker [-0.0684, +0.0740] | 0.4646 | -0.0318, weaker [-0.0733, +0.0516] |
| 30 | **0.5817** | +0.0079; item [-0.0302, +0.0546], persona [-0.0425, +0.0672] | 0.6414 | +0.0173, weaker [-0.0503, +0.0997] | 0.5277 | +0.0313, weaker [-0.0758, +0.1493] | 0.4247 | -0.0718, weaker [-0.1233, +0.0018] |
| 60 | **0.5825** | +0.0087; item [-0.0434, +0.0592], persona [-0.0662, +0.0865] | 0.6438 | +0.0197, weaker [-0.0793, +0.1301] | 0.5127 | +0.0163, weaker [-0.1247, +0.1564] | 0.4459 | -0.0505, weaker [-0.1645, +0.1167] |

**AUX-PAD-MINI** — GPT-4.1 mini (BELIEVED row 0.5959).

| length | whole | Δ vs 1.75 (item CI, persona CI) | superseded | Δ | retracted | Δ | expired | Δ | distinct nok | mean nok |
|---|---:|---|---:|---|---:|---|---:|---|---:|---:|
| 1.75 (recorded) | **0.7339** | — | 0.8572 | — | 0.5638 | — | 0.5110 | — | 9 | 0.0617 |
| 15 | **0.6675** | -0.0664; item [-0.1132, -0.0219]*, persona [-0.1291, -0.0128]* | 0.7722 | -0.0850, weaker [-0.1517, -0.0380]* | 0.4481 | -0.1156, weaker [-0.2829, +0.0157] | 0.6078 | +0.0968, weaker [-0.0204, +0.2514] | 8 | 0.1042 |
| 30 | **0.6595** | -0.0744; item [-0.1112, -0.0388]*, persona [-0.1231, -0.0301]* | 0.7519 | -0.1053, weaker [-0.1562, -0.0696]* | 0.4705 | -0.0933, weaker [-0.1883, -0.0197]* | 0.5990 | +0.0880, weaker [-0.0139, +0.2055] | 9 | 0.1163 |
| 60 | **0.6944** | -0.0395; item [-0.0840, +0.0043], persona [-0.1021, +0.0274] | 0.8034 | -0.0538, weaker [-0.1269, +0.0250] | 0.5285 | -0.0353, weaker [-0.1283, +0.0648] | 0.5244 | +0.0133, weaker [-0.1120, +0.1392] | 9 | 0.1315 |

## 3. AUX-PAD-BRANCH — the §5 headings, per reader, whole population

| Key | Value |
|---|---|
| **AUX-PAD-BRANCH (embedding lookup)** | a difference beyond tolerance whose intervals do not both exclude zero, or a rise, at L = 60 (printed as described in §2). |
| **AUX-PAD-BRANCH (lexical lookup)** | **Flat** (every paired difference inside ±0.05). |
| **AUX-PAD-BRANCH (GPT-4.1 mini)** | **Degrades**, first at L = 15 (below −0.05 with both intervals excluding zero at L = 15, 30). |

## 4. Amendment 1 — the contaminated lists on the 444 (`tools/contam.py`; `build/contam_build.json`, `build/contam_texts.json`, `rows/rows_MINI.jsonl`, `rows/rows_H45.jsonl`, `results/contam_scores.json`)

| Key | Value |
|---|---|
| **AUX-PAD-C-LOCK** | 444 items (148 PN), v2 summaries; renderer lock on the committed names alone **444 of 444**; every rendered list re-parses to the injected list, no `:`, no duplicate. |
| **AUX-PAD-C-GATE (c = 0.232)** | Regenerated by `sweep_common.inject`, seed 42: 69 names injected, achieved rate 0.2331 of 296 negatives (target 0.232); mean 1.9189 names per item; negatives naming their own attribute 69, positives 88. Lookups on the regenerated lists: embedding whole **0.6740** (sweep 0.6740), supersession slice 0.8317 (sweep 0.8317); lexical whole 0.5961 (sweep 0.5961), slice 0.7099 (sweep 0.7099) — **PASS** at four decimals (D-PAD-4 on the amendment's label). |
| **AUX-PAD-C-GATE (c = 0.4)** | Regenerated by `sweep_common.inject`, seed 42: 118 names injected, achieved rate 0.3986 of 296 negatives (target 0.4); mean 2.0293 names per item; negatives naming their own attribute 118, positives 88. Lookups on the regenerated lists: embedding whole **0.6001** (sweep 0.6001), supersession slice 0.7567 (sweep 0.7567); lexical whole 0.5497 (sweep 0.5497), slice 0.6630 (sweep 0.6630) — **PASS** at four decimals (D-PAD-4 on the amendment's label). |
| **AUX-PAD-C-PROBE (claude-haiku-4-5-20251001)** | served `claude-haiku-4-5-20251001` on both arms (E1.7, PASS); prompt tokens [1782, 1782], completion [200, 200]; projection 4440 calls **$6.18** (×1.3 $8.03). |
| **AUX-PAD-C-PROBE (gpt-4.1-mini)** | served `gpt-4.1-mini-2025-04-14` on both arms (E1.7, PASS); prompt tokens [1684, 1684], completion [26, 26]; projection 888 calls **$0.64** (×1.3 $0.83). |

Per state on the 444 = the items of that state, positives and negatives alike (the CF-2 convention, `AUX-CF2-NB6-V2`). Paired difference = contaminated − recorded on the same items; model − lookup on the same lists under the same summary (the `AUX-R103-MARGIN` construction). Intervals as in section 2.

**AUX-PAD-C-LOOKUP-EMB** — embedding lookup.

| list | whole | Δ vs recorded (item CI, persona CI) | supersession | Δ | retraction | Δ | expiry | Δ |
|---|---:|---|---:|---|---:|---|---:|---|
| recorded (c = 0) | **0.7663** | — | 0.9222 | — | 0.5000 | — | 0.5000 | — |
| c = 0.232 | **0.6740** | -0.0923; item [-0.1157, -0.0696]*, persona [-0.1177, -0.0695]* | 0.8317 | -0.0905, weaker [-0.1270, -0.0589]* | 0.4025 | -0.0975, weaker [-0.1660, -0.0420]* | 0.4256 | -0.0744, weaker [-0.1268, -0.0279]* |
| c = 0.4 | **0.6001** | -0.1662; item [-0.1995, -0.1351]*, persona [-0.2020, -0.1314]* | 0.7567 | -0.1655, weaker [-0.2141, -0.1234]* | 0.3531 | -0.1469, weaker [-0.2350, -0.0787]* | 0.3353 | -0.1647, weaker [-0.2307, -0.0939]* |

**AUX-PAD-C-LOOKUP-LEX** — lexical lookup.

| list | whole | Δ vs recorded (item CI, persona CI) | supersession | Δ | retraction | Δ | expiry | Δ |
|---|---:|---|---:|---|---:|---|---:|---|
| recorded (c = 0) | **0.6698** | — | 0.7829 | — | 0.5000 | — | 0.5000 | — |
| c = 0.232 | **0.5961** | -0.0737; item [-0.0941, -0.0549]*, persona [-0.0960, -0.0521]* | 0.7099 | -0.0730, weaker [-0.1050, -0.0448]* | 0.3944 | -0.1056, weaker [-0.1649, -0.0542]* | 0.4333 | -0.0667, weaker [-0.1181, -0.0217]* |
| c = 0.4 | **0.5497** | -0.1201; item [-0.1458, -0.0962]*, persona [-0.1493, -0.0918]* | 0.6630 | -0.1199, weaker [-0.1584, -0.0809]* | 0.3411 | -0.1589, weaker [-0.2224, -0.0970]* | 0.3825 | -0.1175, weaker [-0.1835, -0.0600]* |

**AUX-PAD-C-MINI** — GPT-4.1 mini (k = 1).

| list | whole | Δ vs recorded (item CI, persona CI) | supersession | Δ | retraction | Δ | expiry | Δ | model − emb | model − lex |
|---|---:|---|---:|---|---:|---|---:|---|---|---|
| recorded (c = 0) | **0.7167** | — | 0.8308 | — | 0.5283 | — | 0.5489 | — | — | — |
| c = 0.232 | **0.6809** | -0.0358; item [-0.0712, -0.0029]*, persona [-0.0771, -0.0006]* | 0.8096 | -0.0212, weaker [-0.0615, +0.0157] | 0.4639 | -0.0644, weaker [-0.1716, +0.0428] | 0.4861 | -0.0628, weaker [-0.1612, +0.0235] | +0.0069, weaker [-0.0362, +0.0498] | +0.0848, weaker [+0.0411, +0.1271]* |
| c = 0.4 | **0.6123** | -0.1045; item [-0.1365, -0.0708]*, persona [-0.1473, -0.0638]* | 0.7277 | -0.1031, weaker [-0.1456, -0.0657]* | 0.3936 | -0.1347, weaker [-0.2309, -0.0352]* | 0.4469 | -0.1019, weaker [-0.2230, +0.0259] | +0.0122, weaker [-0.0291, +0.0528] | +0.0626, weaker [+0.0218, +0.1002]* |

**AUX-PAD-C-H45** — Haiku 4.5 (k = 5, X4 mean).

| list | whole | Δ vs recorded (item CI, persona CI) | supersession | Δ | retraction | Δ | expiry | Δ | model − emb | model − lex |
|---|---:|---|---:|---|---:|---|---:|---|---|---|
| recorded (c = 0) | **0.7566** | — | 0.8876 | — | 0.5433 | — | 0.5794 | — | — | — |
| c = 0.232 | **0.6823** | -0.0742; item [-0.0983, -0.0495]*, persona [-0.1027, -0.0476]* | 0.8205 | -0.0671, weaker [-0.0999, -0.0393]* | 0.4581 | -0.0853, weaker [-0.1548, -0.0213]* | 0.4958 | -0.0836, weaker [-0.1548, -0.0293]* | +0.0083, weaker [-0.0405, +0.0527] | +0.0862, weaker [+0.0424, +0.1258]* |
| c = 0.4 | **0.6192** | -0.1373; item [-0.1660, -0.1078]*, persona [-0.1709, -0.1044]* | 0.7566 | -0.1310, weaker [-0.1722, -0.0950]* | 0.4286 | -0.1147, weaker [-0.1872, -0.0541]* | 0.4147 | -0.1647, weaker [-0.2574, -0.0870]* | +0.0192, weaker [-0.0227, +0.0602] | +0.0695, weaker [+0.0271, +0.1098]* |

## 5. AUX-PAD-SPEND

| Key | Value |
|---|---|
| **AUX-PAD-SPEND** | PAD mini lane $1.4118 (1983 calls); PAD probe $0.0022; Amendment 1 probe claude-haiku-4-5-20251001 $0.0056; Amendment 1 probe gpt-4.1-mini $0.0014; Amendment 1 gpt-4.1-mini lane $0.6090 (888 rows); Amendment 1 claude-haiku-4-5-20251001 lane $5.8600 (4440 rows); **total $7.8900** metered from the rows at list / Batch prices, against the caps of the author's rulings of 2026-09-14 (evening): $21 combined for the registered lanes, $28 overall with this amendment's Haiku lane, which ran regardless of the ×1.3 rule in its reordered turn (the dated lines of `ADDENDUM_PAD.md`). |

## Author's adoption of the freeze (dated)

**2026-09-14 (evening).** The author reviewed freeze `dab8956` and adopted it as the author's registration; the rulings of that date are the dated lines appended below the marker of the registration file.
<!-- AUX-PAD-PRINTED BEGIN (pad_table.py) -->

## 6. AUX-PAD-PRINTED — the two-decimal forms Section 5 prints, against their four-decimal sources (the R97/R102 printed-forms convention; written by `tools/pad_table.py`, R107)

| printed | source |
|---|---|
| $0.75$ to $0.73$, $0.72$ and $0.67$ at $15$, $30$ and $60$ names | AUX-PAD-LOOKUP-EMB whole: 0.7484 → 0.7298 / 0.7191 / 0.6696 |
| the lexical lookup flat ($0.57$ to $0.58$) | AUX-PAD-LOOKUP-LEX whole: 0.5738 → 0.5772 / 0.5817 / 0.5825; AUX-PAD-BRANCH flat |
| $0.73$ to $0.67$, $0.66$ and $0.69$ | AUX-PAD-MINI whole: 0.7339 → 0.6675 / 0.6595 / 0.6944; AUX-PAD-BRANCH degrades, first at 15 |
| $-0.08$ at $60$ names, item interval excluding zero and profile interval including it | AUX-PAD-LOOKUP-EMB 60: -0.0788, item $[-0.1541,-0.0096]$, persona $[-0.1794,+0.0284]$ |
| $0.77$ to $0.67$ and $0.60$ | AUX-PAD-C-LOOKUP-EMB whole: 0.7663 → 0.6740 / 0.6001 |
| $0.72$ to $0.68$ and $0.61$ | AUX-PAD-C-MINI whole: 0.7167 → 0.6809 / 0.6123 |
| $0.76$ to $0.68$ and $0.62$ | AUX-PAD-C-H45 whole: 0.7566 → 0.6823 / 0.6192 |
| each model within $0.02$ of the lookup on the same lists, intervals including zero | AUX-PAD-C-MINI minus emb +0.0069 / +0.0122; AUX-PAD-C-H45 +0.0083 / +0.0192; every weaker interval includes zero |

<!-- AUX-PAD-PRINTED END -->
