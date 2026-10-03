# NUMBERS_R113.md: the zero-cost audit pass (program R113, 2026-09-16; no model call; no embedding call; no ingestion; no human annotation; $0)

Sections are appended by the scripts under `reviews/r113/tools/` from the result files under `reviews/r113/results/`; every input is a recorded row or a recorded artifact named by path; frozen lane code is imported, never edited. Estimators: `common_e1r.auroc` (Mann-Whitney, ties at 0.5); `run_resp.paired` and `run_resp.auroc_ci` (item-level and persona-clustered bootstraps, 1,000 draws, seed 42; the weaker governs). No registration: these are descriptive analyses on recorded rows, specified in `reviews/r113/SPEC_R113.md` before computation and ordered by the author's instruction of 2026-09-16. Every number the manuscript prints from them enters through a key here and no other way.

## 0. AUX-R113-SPEC-FREEZE

`reviews/r113/SPEC_R113.md` sha256 **`a315511d5291074ba172c4aa3c4e12c70ba600747280cfac0fe05ba82699acb6`**, recorded at HEAD `5e1a031` (the integration pass) on 2026-09-16 before any script under `reviews/r113/tools/` ran. The scripts assert this hash at start.

## 1. AUX-R113-Z1: the composite's five-line proxy, the answers that would be needed (SPEC_R113 Z1; DS Amendment 7; no call)

Inputs: `ds_downstream/stage1.json`, `views.json`, `policies.json`; every `ds_downstream/run/rows_*.jsonl` (14 files, 3715 distinct recorded (item, view) answers) and every `ds_downstream/cache*/responses.json` (7 files, 4376 entries). ABSENT items whose coverage rule let them through onto a view longer than five lines: MODEL **10**, LOOKUP **17**, LOOKUP-LIT **72** (the counts the ledger and the caption state), MODEL-ALL 10 and LOOKUP-ALL 17 (the same items as MODEL and LOOKUP: {'MODEL==MODEL-ALL': True, 'LOOKUP==LOOKUP-ALL': True}; their F(N3) views share the F(N2) view's sha on 0 and 0 items; LOOKUP and LOOKUP-LIT share a sha on 17). Distinct absent items 75; distinct (item, view) inputs **99**; inputs with a recorded answer on the exact view under any prompt variant or answerer **0** (on an Amendment 6 flat or gated view: 0); in any cache 0.

**Reading (the spec's rule):** none of the inputs has a recorded answer: the five-line proxy stands as AUX-DS-A7-COMPOSITE-ANSWERED and the tab:ds-a7 caption state it; no composite number changes; the generation required is listed under generation_required and inputs.

### AUX-R113-Z1-GENERATION: what the answered reading on the actual views would cost in calls (not made)

99 calls per answerer (GPT-4.1 mini; Claude Haiku 4.5), `SYSTEM_ANSWER` + `USER_ANSWER_A4` (the Amendment 4 header), one call per distinct (item, view) with the answer shared by every policy whose view is byte-identical; 1322 view lines per answerer in all. The list of inputs (item, policy, view sha, line count, fetch set) is `reviews/r113/results/z1_composite_proxy.json` `inputs`.

## 2. AUX-R113-Z2: the FULL-store population of the Graphiti comparison, recounted (SPEC_R113 Z2; no call)

From `resp_common.load_cell()` (the 661): FULL **323** (145 ABSENT / 131 PRESENT / 47 PRESENT-NEGATIVE), non-ABSENT FULL **178**; the 47 obligations by subtype {'with-replacement': 38, 'without-replacement': 9}, intent {'CURRENT-STATE': 38, 'UPCOMING': 9}, state {'sup': 27, 'ret': 11, 'exp': 9}, attack vector {'AV4': 11, 'AV1': 16, 'AV7': 11, 'AV2': 9}, over 28 personas; the 131 licensed by intent {'CURRENT-STATE': 65, 'UPCOMING': 26, 'CHANGE-AWARE': 35, 'PAST-EVENT': 5} over 40 personas. Non-FULL items against the FULL sibling of the same question: labels equal **99**, the full store contradicts the label **230** ({'ABSENT (FULL sibling PRESENT-NEGATIVE)': 14, 'PRESENT (FULL sibling PRESENT-NEGATIVE)': 1, 'ABSENT (FULL sibling PRESENT)': 215}; `aisha_q03` CAT-ABLATED among them: True), no FULL sibling in the cell **9**; over the 100 ablated non-ABSENT items, 58 duplicate the sibling's label and subtype and 42 contradict it. The FULL-variant census record (`r85_graphiti/g10/census_full_variant_g10.json`, read): {"obligations": 47, "superseded_or_expired": 34, "RECOVERED": 13, "STALE_ACTIVE": 10, "EXTRACTION_MISS": 11, "recall": 0.3824}. Every count Amendment 2 sections 0 and 3 state reproduces: **True** (`reviews/r113/results/z2_full_population.json` `checks_against_amendment_2_sections_0_and_3`).

## 3. AUX-R113-Z3: the FR-Bank comparators on the FULL-variant population (SPEC_R113 Z3; the section 0 "$0 repair", FR-Bank side; no Graphiti number; no call)

Reproduction gates on the 661, all equal to the ledgered values: {"mini_true": 0.7339, "mini_blind": 0.4946, "mini_retrieved": 0.6851, "mini_hybrid": 0.8303, "mini_believed": 0.8144, "lookup_emb": 0.7484, "lookup_lex": 0.5738, "h45_true": 0.821, "h45_retrieved": 0.7134, "h45_hybrid": 0.7863}; reach 54 / 74 of 104. Population the 323 FULL items, positives the 47 obligations; per state this state's positives against every FULL negative (276). Haiku 4.5 rows are X4's collapse (units with at least three draws).

### AUX-R113-Z3-ROWS: each reader on the 323 (single-arm item and persona intervals), the 661 beside

| reader | 661 | 323, all (47 of 323) | item 95% | persona 95% | supersession | expiry | retraction |
|---|---:|---:|---|---|---:|---:|---:|
| GPT-4.1 mini INDEXED-TRUE | 0.7339 | **0.7424** (n 323, pos 47) | [0.6500, 0.8225] | [0.6517, 0.8353] | 0.8707 (27) | 0.5564 (9) | 0.5795 (11) |
| GPT-4.1 mini BLIND | 0.4946 | **0.4964** (n 323, pos 47) | [0.4907, 0.5000] | [0.4907, 0.5000] | 0.4964 (27) | 0.4964 (9) | 0.4964 (11) |
| GPT-4.1 mini RETRIEVED (join tags) | 0.6851 | **0.6980** (n 323, pos 47) | [0.6133, 0.7719] | [0.6141, 0.7746] | 0.6564 (27) | 0.7909 (9) | 0.7241 (11) |
| GPT-4.1 mini HYBRID | 0.8303 | **0.8855** (n 323, pos 47) | [0.8197, 0.9364] | [0.8076, 0.9426] | 0.9561 (27) | 0.7500 (9) | 0.8233 (11) |
| GPT-4.1 mini RETRIEVED-BELIEVED (own marks) | 0.8144 | **0.8504** (n 323, pos 47) | [0.8125, 0.8889] | [0.8125, 0.8860] | 0.8472 (27) | 0.8321 (9) | 0.8730 (11) |
| embedding lookup (superseded section) | 0.7484 | **0.7434** (n 323, pos 47) | [0.6457, 0.8300] | [0.6588, 0.8268] | 0.9548 (27) | 0.4771 (9) | 0.4424 (11) |
| lexical lookup | 0.5738 | **0.5713** (n 323, pos 47) | [0.5250, 0.6296] | [0.5260, 0.6291] | 0.6268 (27) | 0.4964 (9) | 0.4964 (11) |
| Haiku 4.5 INDEXED-TRUE | 0.8210 | **0.8477** (n 323, pos 47) | [0.7841, 0.9026] | [0.7845, 0.9040] | 0.9020 (27) | 0.6916 (9) | 0.8422 (11) |
| Haiku 4.5 RETRIEVED (join tags) | 0.7134 | **0.7395** (n 323, pos 47) | [0.6551, 0.8101] | [0.6690, 0.8064] | 0.6931 (27) | 0.8198 (9) | 0.7877 (11) |
| Haiku 4.5 HYBRID | 0.7863 | **0.8469** (n 323, pos 47) | [0.7730, 0.9037] | [0.7960, 0.8946] | 0.8268 (27) | 0.8917 (9) | 0.8594 (11) |

### AUX-R113-Z3-PAIRED: the recorded pairings on the 323, the 661 beside (paired difference; item and persona intervals; an asterisk marks both excluding zero)

| pairing | population | all: base -> arm, D | item 95% | persona 95% | supersession D | expiry D | retraction D |
|---|---|---|---|---|---:|---:|---:|
| mini RETRIEVED - INDEXED-TRUE | full_323 | 0.7424 -> 0.6980, **-0.0444** (n 323) | [-0.1636, +0.0722] | [-0.1621, +0.0597] | -0.2143 | +0.2345 | +0.1446 |
| mini RETRIEVED - INDEXED-TRUE | all_661 | 0.7339 -> 0.6851, **-0.0488** (n 661) | [-0.1274, +0.0285] | [-0.1454, +0.0389] | -0.1719 | +0.2364 | +0.0850 |
| mini HYBRID - INDEXED-TRUE | full_323 | 0.7424 -> 0.8855, **+0.1432*** (n 323) | [+0.0649, +0.2269] | [+0.0663, +0.2123] | +0.0853 | +0.1936 | +0.2437 |
| mini HYBRID - INDEXED-TRUE | all_661 | 0.7339 -> 0.8303, **+0.0964*** (n 661) | [+0.0415, +0.1554] | [+0.0227, +0.1635] | +0.0472 | +0.1747 | +0.1704 |
| mini RETRIEVED-BELIEVED - RETRIEVED | full_323 | 0.6980 -> 0.8504, **+0.1524*** (n 323) | [+0.0793, +0.2323] | [+0.0815, +0.2271] | +0.1908 | +0.0413 | +0.1489 |
| mini RETRIEVED-BELIEVED - RETRIEVED | all_661 | 0.6851 -> 0.8144, **+0.1292*** (n 661) | [+0.0666, +0.1826] | [+0.0606, +0.2060] | +0.1336 | +0.0392 | +0.1706 |
| mini RETRIEVED-BELIEVED - INDEXED-TRUE | full_323 | 0.7424 -> 0.8504, **+0.1080*** (n 323) | [+0.0206, +0.1986] | [+0.0110, +0.2031] | -0.0235 | +0.2758 | +0.2935 |
| mini RETRIEVED-BELIEVED - INDEXED-TRUE | all_661 | 0.7339 -> 0.8144, **+0.0805** (n 661) | [+0.0177, +0.1439] | [-0.0081, +0.1660] | -0.0383 | +0.2756 | +0.2556 |
| Haiku RETRIEVED - INDEXED-TRUE | full_323 | 0.8477 -> 0.7395, **-0.1082*** (n 323) | [-0.2088, -0.0123] | [-0.1962, -0.0117] | -0.2089 | +0.1282 | -0.0545 |
| Haiku RETRIEVED - INDEXED-TRUE | all_661 | 0.8210 -> 0.7134, **-0.1077*** (n 661) | [-0.1732, -0.0369] | [-0.1939, -0.0203] | -0.1986 | +0.0870 | +0.0005 |
| Haiku HYBRID - INDEXED-TRUE | full_323 | 0.8477 -> 0.8469, **-0.0009** (n 323) | [-0.0771, +0.0732] | [-0.0688, +0.0774] | -0.0752 | +0.2001 | +0.0171 |
| Haiku HYBRID - INDEXED-TRUE | all_661 | 0.8210 -> 0.7863, **-0.0347** (n 661) | [-0.0930, +0.0248] | [-0.1109, +0.0433] | -0.1020 | +0.1396 | +0.0278 |
| embedding lookup - mini INDEXED-TRUE | full_323 | 0.7424 -> 0.7434, **+0.0010** (n 323) | [-0.0993, +0.0963] | [-0.1111, +0.1067] | +0.0841 | -0.0793 | -0.1372 |
| embedding lookup - mini INDEXED-TRUE | all_661 | 0.7339 -> 0.7484, **+0.0145** (n 661) | [-0.0549, +0.0769] | [-0.0765, +0.1080] | +0.0962 | -0.0287 | -0.1585 |

### AUX-R113-Z3-REACH: the forbidding record among the recorded top-k by identifier

The 47 FULL obligations: in ranks 1 to 5 **26** of 47, in ranks 1 to 10 **34**; per state (n, k5, k10) {'sup': [27, 9, 15], 'ret': [11, 9, 11], 'exp': [9, 8, 8]}. The 104 (the ledgered AUX-RESP-L2-REACH row): 54 / 74 of 104.

## 4. AUX-R113-Z4: R85 Amendment 2's FR-Bank inputs, built from the unfrozen draft (SPEC_R113 Z4; draft sha256 `2e7715d1d41a1692...`; no call; nothing answered)

Views per item from `resp_review/l2/retrieval.json` `top10_ids` rendered with FR-Bank's own marks (`amend1_resp.believed_flags`, `resp_common.render_line`): T ranks 1 to 5 with the store's state; U the same lines with the `lifecycle:` field removed (asserted: exactly that field differs on every line); M the active lines of ranks 1 to 10 in rank order, the first five, renumbered from [1] (every M line reads `active`, asserted; T = M byte-identically where ranks 1 to 5 hold no non-active line, asserted). The views: `reviews/r113/results/z4_a2_frbank_views.json`. The graph side is not built: `neo4j-r85` is down at this pass and the stock retrieval needs Graphiti's embedding call (AUX-R113-Z5).

### AUX-R113-Z4-VIEWS and AUX-R113-Z4-RESOLUTION: the view census and the section 5 quantities on FR-Bank

| population | n (obl. / lic.) | distinct inputs U / T / M | T = M | n_TM (bound n_TM / n) | n_TM obligations (bound) | n_TM licensed (bound) | M short views (lengths) | lines removed T -> M | (a) reached | (b) reached, marked | (c) reached, unmarked | (e) imported | (g) unreached in 10 | (f) evidence removed by intent (licensed with evidence in ranks 1 to 5, by intent) |
|---|---|---|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| primary_178 | 178 (47 / 131) | 178 / 178 / 178 | 15 | **163** (0.9157) | 46 (0.9787) | 117 (0.8931) | 63 ({2: 16, 1: 3, 3: 14, 4: 29, 0: 1}) | 423 | 26 | 23 | 3 | 10 | 13 | {'CHANGE-AWARE': 5, 'CURRENT-STATE': 18, 'UPCOMING': 3, 'PAST-EVENT': 3} (of {'CHANGE-AWARE': 13, 'CURRENT-STATE': 31, 'UPCOMING': 8, 'PAST-EVENT': 3}; licensed {'CURRENT-STATE': 65, 'UPCOMING': 26, 'CHANGE-AWARE': 35, 'PAST-EVENT': 5}) |
| frbank_only_100 | 100 (57 / 43) | 99 / 99 / 96 | 7 | **93** (0.93) | 55 (0.9649) | 38 (0.8837) | 34 ({3: 15, 2: 3, 4: 16}) | 234 | 28 | 23 | 5 | 10 | 17 | {'CURRENT-STATE': 6, 'CHANGE-AWARE': 1, 'PAST-EVENT': 3} (of {'CHANGE-AWARE': 5, 'CURRENT-STATE': 10, 'UPCOMING': 3, 'PAST-EVENT': 3}; licensed {'CURRENT-STATE': 20, 'UPCOMING': 8, 'CHANGE-AWARE': 10, 'PAST-EVENT': 5}) |

The structural bound is the draft's quantity (i): the paired T-versus-M difference in any endpoint cannot exceed n_TM / n because identical complete inputs share one answer. Sets (a) to (g) are the draft's descriptive mechanism sets and bound nothing. Set (f) uses the gold field's token coverage of the line text at TAU_GOLD with MIN_SHARED (`run_ds.records`, `e0_common.toks` / `cov`).

### AUX-R113-Z4-REFERENCE: DS Amendment 4's ALWAYS row (the header prompt; the join's tags; the recorded top-5) restricted to the 178 from `ds_downstream/run/scores_amend4.json` `per_row` (read, never re-run)

| answerer | licensed: n, gold in view, answered / abstained, correct at 0.50 / 0.80 | obligations: n, reached at k = 5 (no row otherwise), answered / abstained, scorable answered, stale at 0.50 / 0.80, successor use (supersession), expiry reached (unscorable) |
|---|---|---|
| MINI | 131, 48, 109 / 22, **43** / 15 | 47, 26 (21 unreached), 17 / 9, 14, **3** / 0, 0, 8 |
| H45 | 131, 48, 99 / 32, **55** / 18 | 47, 26 (21 unreached), 13 / 13, 13, **3** / 0, 0, 8 |

## 5. AUX-R113-Z5: R85 Amendment 1 Steps 4 and 5, what exists and what does not (SPEC_R113 Z5; no call; no index built; P3 not scored)

The forty `census_runs/g10_<persona>` records: superseded-names section at most **6** names against the frozen `SLOT_CAP = 15`, truncated in **0** of 40 personas, so the BELIEVED-capped and BELIEVED-lifted renderings print the same superseded-names section for every persona and the list NB-6 reads for P3 exists on disk for all forty; the whole-map section is truncated (`(+N more)`) in **40** of 40 (distinct attribute names at least 100), so NB-5's lifted reading needs the graph. Environment at this pass: Docker engine reachable **False**, `neo4j-r85` running **False**; per-edge exports under `r85_graphiti/`: none (the census records hold counts, buckets and name lists, not edges). Consequences: the BELIEVED-lifted and TRUE-projected indexes (Step 4) and the tag route's retrieval (Step 5; stock `Graphiti.search`, a `text-embedding-3-small` call per query) cannot be built without the graph and, for Step 5, without an embedding call; Amendment 2's Graphiti views need Step 5's record. P3 (the NB-6 matcher within tolerance of 0.50 under both renderings) is computable from disk for the superseded section alone and is **not scored here**: its population ruling is the author's (D-R85-16) and the registration names both renderings.

## 6. AUX-R113-PAD-LEX-PAIRED: the lexical lookup at 100 and 200 padded names under the registered draw order, paired against the committed list (SPEC_R113 Z6; read from `reviews/v18/results/a4_pad_extend.json`, R110's A4 artifact; no recomputation; no call)

Artifact sha256 `3f963949dc2fc66a...`. The registered draw order continues into pool B (other personas' names) once the store's own pool is exhausted: at 100 names 79 of 242 keys draw 1216 names from pool B, at 200 every key does (23596 names). The embedding rows are AUX-R110-A4's (0.6558, -0.0926 [-0.1718, -0.0221] / [-0.1953, +0.0199]; 0.5960, -0.1525 [-0.2357, -0.0773] / [-0.2595, -0.0399]). The lexical paired rows, padded minus the committed list (base 0.5738), item-level and persona-clustered (1,000 draws, seed 42):

| L | lexical AUROC | delta vs 0.5738 | item 95% | persona 95% |
|---:|---:|---:|---|---|
| 100 | 0.5601 | **-0.0137** | [-0.0672, +0.0369] | [-0.0926, +0.0716] |
| 200 | 0.5383 | **-0.0355** | [-0.0903, +0.0189] | [-0.1125, +0.0455] |

Both intervals include zero at both lengths: the lexical lookup is flat under the registered order as it is at 15, 30 and 60.

### AUX-R113-PRINTED: the forms the v19 manuscript prints from this pass (each from a value above or in the key named)

| printed | source | key |
|---|---|---|
| $100$, $200$; $79$ of $242$ | 100, 200; keys_spilling_into_pool_b 79 of 242 keys (every key at 200) | AUX-R110-A4; this section |
| $0.6558$, $0.5960$ | the embedding lookup at 100 and 200 under the registered order | AUX-R110-A4 |
| $-0.0137$ $[-0.0672,+0.0369]$ $[-0.0926,+0.0716]$; $-0.0355$ $[-0.0903,+0.0189]$ $[-0.1125,+0.0455]$ | the lexical rows at 100 and 200 | this section |
| $99$, $129$, $0.6531$ | the store's own pool exhausted: mean 99.2209 names, at most 129, embedding 0.6531 | AUX-R110-A4 (reading (ii)) |
