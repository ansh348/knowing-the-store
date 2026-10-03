# NUMBERS_V2RCAT.md: ADDENDUM_V2R_CAT, the increment moved within the triple

Registration `registrations/ADDENDUM_V2R_CAT.md`, registered text sha256 `de2dd0baaf33ccb3dcf1c2b0c10b01cc6f76f851e4057946dc03f477a584b18f` (the bytes above the marker line), frozen at `257a090` on 2026-09-14. Descriptive: no prediction, no bar, no verdict. Every number for this addendum enters the manuscript through a key in this file and no other way. Written by `r82_counterfactual/v2rcat/tools/v2rcat.py`; sections 1 to 3 before the first model call on the arm.

## 1. AUX-V2RCAT-LOCK: the construction

Locks: registration True; `cf_indexes.json` meta sha256 (v2 + v3) and sha256_v2r recomputed and equal (True, True). Start text: the recorded v2r of every store version (totals permuted). For each of the 60 counted-state pairs the state's column of the pair's category row reads b, b, b+k across PRESENT, ABSENT and PN on the recorded v2 texts (asserted; k census: retraction {"1": 27, "2": 2, "3": 1}, expiry {"1": 14, "2": 8, "3": 5, "4": 2, "6": 1}); under seed 42 one non-PN sibling takes b+k and the PN version takes b (the sibling per pair is recorded in `build/build_v2rcat.json` moves). RENDERER LOCK asserted on every version: 120 texts differ from their v2r on exactly one line, the category row, and on that line only in the state's column; every supersession text is byte-identical to its v2r; every name section equals its v2's. Texts sha256 `093f1d5839485e23...`; the superseded-names lookup on the texts reproduces the recorded 0.7663 (got 0.7663).

## 2. AUX-V2RCAT-REF: the reference readers ($0; within the state's own items, the CF-2 convention)

| reader | whole | retraction | item 95% | persona 95% | expiry | item 95% | persona 95% |
|---|---:|---:|---|---|---:|---|---|
| CR-oracle-state-cell under V2R-CAT | 0.4335 | 0.3028 | [0.2101, 0.4027] | [0.2575, 0.3517] | 0.3611 | [0.2448, 0.4864] | [0.3160, 0.3923] |
| CR-oracle-state-cell under v2 | 0.6330 | 0.8944 | [0.8179, 0.9601] | [0.7966, 0.9849] | 0.7778 | [0.6793, 0.8625] | [0.7153, 0.8680] |
| CR-totals under V2R-CAT (= v2r) | 0.4472 | 0.4044 | [0.2737, 0.5291] | [0.2754, 0.5167] | 0.3894 | [0.2799, 0.5190] | [0.2444, 0.5256] |

## 3. AUX-V2RCAT-LEAK: the CF-2 leakage screen on the V2R-CAT texts

0 of 30 PRESENT items score correct (leaks iff more than 3): **PASS**; non-UNKNOWN 5, parse failures 0; served ['gpt-4.1-mini-2025-04-14']; $0.0150. The same 30-item sample as CF-2's screen (asserted).

## 4. AUX-V2RCAT-PROBE and AUX-V2RCAT-PROJECTION (E1.7 rule; printed before submission)

| lane | served | identifier ok | probe in / out | calls | projected $ | x1.3 | billed before | headroom | fits |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| claude-haiku-4-5-20251001 | `claude-haiku-4-5-20251001` | True | 1782 / 200 | 2220 | 3.0273 | 3.9355 | 0.0185 | 3.9815 | True |
| gpt-4.1-mini | `gpt-4.1-mini-2025-04-14` | True | 1684 / 26 | 444 | 0.3084 | 0.4009 | 3.0465 | 0.9535 | True |

## 5. AUX-V2RCAT-SUBMISSION

gpt-4.1-mini: 444 synchronous rows in `rows_MINI.jsonl`; claude-haiku-4-5-20251001: Batch `msgbatch_01CUGoifgYtzd8fdFA8mCYzT`, 2220 requests. Cap $4.00; committed so far $3.2341. AUX-V2RCAT-MINI, -H45, -BRANCH and -SPEND fill at `score`.

## 6. AUX-V2RCAT-MINI, AUX-V2RCAT-H45, AUX-V2RCAT-OP5: the readers under V2R-CAT against their recorded v2 rows (paired; both intervals; band 0.05)

| reader | k | v2 (recorded) | V2R-CAT | whole minus v2 (item; persona) | SUP v2 -> V2R-CAT, delta | RET v2 -> V2R-CAT, delta (item; persona), inside band | EXP v2 -> V2R-CAT, delta (item; persona), inside band | bad rows | $ |
|---|---:|---:|---:|---|---|---|---|---:|---:|
| claude-haiku-4-5-20251001 | 5 | 0.7566 | **0.7525** | -0.0041 ([-0.0220, +0.0133]; [-0.0233, +0.0146]) | 0.8876 -> 0.8873, -0.0002 | 0.5433 -> 0.5361, -0.0072 ([-0.0925, +0.0781]; [-0.0981, +0.0795]), neither | 0.5794 -> 0.5342, -0.0453 ([-0.0958, +0.0014]; [-0.0781, -0.0169]), neither | 0 | 2.9112 |
| claude-opus-5 | | | dash: optional lane not run | | | | | | |
| gpt-4.1-mini | 1 | 0.7167 | **0.7410** | +0.0242 ([-0.0047, +0.0523]; [-0.0032, +0.0530]) | 0.8308 -> 0.8388, +0.0080 | 0.5283 -> 0.5553, +0.0269 ([-0.0491, +0.1080]; [-0.0692, +0.1331]), neither | 0.5489 -> 0.6100, +0.0611 ([-0.0404, +0.1641]; [-0.0217, +0.1417]), neither | 0 | 0.3044 |

The reference readers under the same text (AUX-V2RCAT-REF): the state-cell reader retraction 0.3028 / expiry 0.3611; CR-totals 0.4044 / 0.3894.

### AUX-V2RCAT-BRANCH: **mixed: printed per model**. claude-haiku-4-5-20251001: neither inside the band on both states nor beyond it with both intervals: printed as it came out; gpt-4.1-mini: neither inside the band on both states nor beyond it with both intervals: printed as it came out. Section 5: Section 5 says which model reads the per-category tally and on which state, with the number; the reader claim narrows to the models that did not move.

### AUX-V2RCAT-POSTHOC: the direction reading (POST HOC; the author's ruling of 2026-09-15; not a registered branch)

A reader that follows the moved tally falls below 0.50 on that state (the state-cell reader: retraction 0.3028, expiry 0.3611). Every model's move is read against that direction: claude-haiku-4-5-20251001 on retraction -0.0072 (down; item [-0.0925, +0.0781], persona [-0.0981, +0.0795]; the reader of the moved cell 0.3028); claude-haiku-4-5-20251001 on expiry -0.0453 (down; item [-0.0958, +0.0014], persona [-0.0781, -0.0169]; the reader of the moved cell 0.3611); gpt-4.1-mini on retraction +0.0269 (up; item [-0.0491, +0.1080], persona [-0.0692, +0.1331]; the reader of the moved cell 0.3028); gpt-4.1-mini on expiry +0.0611 (up; item [-0.0404, +0.1641], persona [-0.0217, +0.1417]; the reader of the moved cell 0.3611). GPT-4.1 mini's +0.0611 on expiry is upward with both intervals including zero, so no model followed the tally. Section 5 reports the registered branch as it fired (AUX-V2RCAT-BRANCH) and then this reading, labelled post hoc; the thesis sentence says 'no model follows the tallies', carrying the totals run (AUX-CF2-EQUIV-V2R) and this run with their numbers.

### AUX-V2RCAT-SPEND: {"cap": 4.0, "claude-haiku-4-5-20251001": 2.9112, "gpt-4.1-mini": 0.3044, "leakage_screen": 0.014961, "probes": 0.0035, "total": 3.2341}


## 8. AUX-V2RCAT-OP5 — the optional Opus 5 lane, run 2026-09-17 under the author's instruction (program R114; D-V2RCAT-2; `tools/v2rcat_op5.py`; `rows/rows_OP5.jsonl`, `rows/batch_OP5.json`; `results/scores_v2rcat_op5.json`; sections 1 to 7 above unchanged, the section 6 dash superseded by this row)

`claude-opus-5`, served ['claude-opus-5'], k = **1** (the registered default; temperature unset, `max_tokens` 1024, Message Batches at the 0.5 multiplier), 444 requests over three delivery paths (D-V2RCAT-3, D-V2RCAT-4): `msgbatch_01WVXiaiBoC6JHFXEyiM1y2m` canceled at the author's instruction after 388 had succeeded, `msgbatch_01Cb4ZG9J1qyUCZC7VQuh65j` (the 56 resubmitted) canceled after 5 had succeeded, the remaining 51 synchronous at list price; OK rows per path {'msgbatch_01Cb4ZG9J1qyUCZC7VQuh65j': 5, 'sync-2026-09-17': 51, 'msgbatch_01WVXiaiBoC6JHFXEyiM1y2m': 388}, 0 not OK, $4.5022 (probe $0.0158). The comparator is the recorded CF-2 Opus v2 row at **k = 5** (AUX-CF2-OP5-V2 0.8405, X4 collapse), disclosed here as section 4 requires; the recorded totals-randomized row (v2r, k = 5) prints beside as a distinct construction.

| reader | k | v2 (recorded, k = 5) | v2r totals-randomized (recorded, k = 5) | V2R-CAT (k = 1) | whole minus v2 (item; persona) | whole minus v2r (item; persona) | SUP v2 -> V2R-CAT | RET v2 -> V2R-CAT, delta (item; persona), band | EXP v2 -> V2R-CAT, delta (item; persona), band | bad rows | $ |
|---|---:|---:|---:|---:|---|---|---|---|---|---:|---:|
| claude-opus-5 | 1 | 0.8405 | 0.8353 | **0.8049** | -0.0357 ([-0.0543, -0.0206]; [-0.0617, -0.0169]) | -0.0305 ([-0.0497, -0.0157]; [-0.0572, -0.0110]) | 0.9325 -> 0.9303, -0.0022 | 0.5872 -> 0.4861, -0.1011 ([-0.1700, -0.0435]; [-0.2145, -0.0211]), neither | 0.6150 -> 0.4914, -0.1236 ([-0.2165, -0.0374]; [-0.2598, -0.0118]), neither | 0 | 4.5022 |

The reference readers under the same text (AUX-V2RCAT-REF): the state-cell reader retraction 0.3028 / expiry 0.3611; CR-totals 0.4044 / 0.3894. Section 5 branch for this model: **neither inside the band on both states nor beyond it with both intervals: printed as it came out** (point estimates within 0.05 on both counted states: False). The k = 1 against k = 5 comparison carries draw-count noise the two registered lanes did not; the row is disclosed as such and the section 5 reading for the three models is re-stated in the paper only with that disclosure. The author's ruling of 2026-09-15 on the word 'totals' / 'tallies' (below the marker of the addendum) is not re-opened here.

### AUX-V2RCAT-SPEND (continued) — Opus 5 lane $4.5022 + probe $0.0158 = $4.5180, outside the $4 cap (D-V2RCAT-2), under the R114 ceiling; the addendum's registered lanes' total $3.2341 is unchanged.

## 9. AUX-V2RCAT-A1: Amendment 1 (E1, program R117) -- Opus 5 at five draws on the moved-count texts (registrations/ADDENDUM_V2R_CAT_AMENDMENT_1.md, registered text sha256 `30d102eddbb9166d...`, frozen at `177697a`; `tools/v2rcat_op5_k5.py`; `rows/rows_OP5.jsonl` draws 2 to 5, `rows/batch_OP5_k5.json`, `rows/lock_op5_k5.json`; `results/scores_v2rcat_op5_k5.json`)

### AUX-V2RCAT-A1-LOCK

Registration sha256 holds; the parent registration and the texts lock re-asserted; draws 2 to 5 through Message Batches like the recorded draw 1 (`claude-opus-5`, temperature unset, `max_tokens` 1024, x0.5). Rows per batch: {'msgbatch_01Cb4ZG9J1qyUCZC7VQuh65j': 5, 'sync-2026-09-17': 51, 'msgbatch_01WVXiaiBoC6JHFXEyiM1y2m': 388, 'msgbatch_018zhTXQp7tEQjp7Sb2MfdEc': 1776}; draws per item {5: 444}; rows not OK 0; items excluded (< 3 draws) 0.

### AUX-V2RCAT-A1-OP5-K5

| reader | k | v2 (recorded, k = 5) | V2R-CAT (k = 5) | V2R-CAT (k = 1, recorded) | whole minus v2 (item; persona) | SUP v2 -> V2R-CAT | RET v2 -> V2R-CAT, delta (item; persona), band | EXP v2 -> V2R-CAT, delta (item; persona), band |
|---|---:|---:|---:|---:|---|---|---|---|
| claude-opus-5 | 5 | 0.8405 | **0.8075** | 0.8049 | -0.0330 ([-0.0496, -0.0196]; [-0.0592, -0.0142]) | 0.9325 -> 0.9312, -0.0013 | 0.5872 -> 0.4869 (k = 1: 0.4861), -0.1003 ([-0.1612, -0.0472]; [-0.2079, -0.0317]), neither | 0.6150 -> 0.4869 (k = 1: 0.4914), -0.1281 ([-0.2127, -0.0517]; [-0.2651, -0.0095]), neither |

### AUX-V2RCAT-A1-DRAW-EFFECT

The five-draw row minus the recorded draw-1 row, whole set: +0.0026 ([-0.0069, +0.0122]; [-0.0088, +0.0138]).

### AUX-V2RCAT-A1-P-M1

**P-M1 HOLDS: at five draws the moved-count movement of Opus 5 replicates on retraction (-0.1003 with intervals [-0.1612, -0.0472] and [-0.2079, -0.0317]) and on expiry (-0.1281 with intervals [-0.2127, -0.0517] and [-0.2651, -0.0095]), both differences negative with both intervals excluding zero.**

### AUX-V2RCAT-A1-SPEND

Draws 2 to 5: $16.1825 (Batch-priced from the returned tokens at $5 / $25 per million x 0.5) against the cap of $22; the recorded draw 1 stays at $4.5022.

## 10. AUX-V2RCAT-A2: Amendment 2 (E9, program R118) -- GPT-5.6 Luna and GPT-5.6 Sol at five draws on the moved-count texts through the raw API (registrations/ADDENDUM_V2R_CAT_AMENDMENT_2.md, registered text sha256 `f70e4779f7b892df...`, frozen at `b0bee93`; `tools/v2rcat_openai.py`; `rows/rows_LUNA.jsonl`, `rows/rows_SOL.jsonl`, `rows/lock_openai.json`, `rows/probes_openai.json`, `rows/costrule_openai.json`; `results/scores_v2rcat_openai.json`; scored 2026-09-19)

### AUX-V2RCAT-A2-LOCK, AUX-V2RCAT-A2-PROBES

Registration sha256 holds; the parent registration and the V2R index lock re-asserted; raw Chat Completions with the frozen `prompts_e1` texts and no other system text; reasoning effort and temperature unset, `max_completion_tokens` 2048 (E5's settings); Luna first then Sol, draw-major, eight workers; the cap of $14 for both models. Probes (E1.7 rule): `gpt-5.6-luna` served `gpt-5.6-luna`, 1683 in / 162 out (132 reasoning, 1680 cache-write), $0.000615; `gpt-5.6-sol` served `gpt-5.6-sol`, 1683 in / 97 out (67 reasoning, 1680 cache-write), $0.010352.

### AUX-V2RCAT-A2-COSTRULE

After Sol's second draw started, its first 25 calls read a cached share of 0.9982 and a mean cost of $0.00354 per call; the projected five-draw total (Luna $0.7570 + probes $0.0110 + Sol draw 1 $4.9982 + 4 x 444 x the mean) was $12.06 against the cap of $14: **branch `all_five`**, draws [1, 2, 3, 4, 5] (a registered outcome, not a deviation).

### AUX-V2RCAT-A2-LUNA-K5, AUX-V2RCAT-A2-SOL-K5

| reader | whole draws | rows (not OK) | v2 (recorded E5, k = 5) | V2R-CAT | whole minus v2 (item; persona) | SUP v2 -> V2R-CAT | RET v2 -> V2R-CAT, delta (item; persona), band | EXP v2 -> V2R-CAT, delta (item; persona), band |
|---|---|---|---:|---:|---|---|---|---|
| gpt-5.6-luna | [1, 2, 3, 4, 5] | 2220 (0) | 0.8417 | **0.8121** | -0.0297 ([-0.0499, -0.0089]; [-0.0583, -0.0081]) | 0.9426 -> 0.9416, -0.0011 | 0.5458 -> 0.4794, -0.0664 ([-0.1505, +0.0156]; [-0.1903, +0.0294]), neither | 0.6167 -> 0.5008, -0.1158 ([-0.2162, -0.0210]; [-0.2551, -0.0121]), neither |
| gpt-5.6-sol | [1, 2, 3, 4, 5] | 2220 (0) | 0.8500 | **0.8172** | -0.0327 ([-0.0521, -0.0151]; [-0.0621, -0.0102]) | 0.9383 -> 0.9373, -0.0010 | 0.5322 -> 0.5000, -0.0322 ([-0.1121, +0.0440]; [-0.1228, +0.0636]), neither | 0.6403 -> 0.4489, -0.1914 ([-0.2862, -0.1074]; [-0.3232, -0.0816]), beyond |

### AUX-V2RCAT-A2-DRAWS (tokens per call, means over OK rows)

| reader | prompt | completion | reasoning | cached | cache-write | usd per draw | cached share per draw |
|---|---:|---:|---:|---:|---:|---|---|
| gpt-5.6-luna | 1614.6104 | 195.9905 | 165.9905 | 1294.4095 | 317.2009 | {1: 0.2792, 2: 0.1197, 3: 0.1193, 4: 0.1199, 5: 0.1188} | {1: 0.0159, 2: 0.9981, 3: 0.9981, 4: 0.9981, 5: 0.9981} |
| gpt-5.6-sol | 1614.6104 | 158.9369 | 128.6892 | 1290.045 | 321.5653 | {1: 4.9982, 2: 1.6994, 3: 1.6859, 4: 1.6872, 5: 1.7276} | {1: 0.0023, 2: 0.9981, 3: 0.9981, 4: 0.9981, 5: 0.9981} |

### AUX-V2RCAT-A2-P-M2

**P-M2 FAILS for GPT-5.6 Luna, GPT-5.6 Sol: GPT-5.6 Luna retraction: -0.0664 with intervals [-0.1505, +0.0156] and [-0.1903, +0.0294]; GPT-5.6 Sol retraction: -0.0322 with intervals [-0.1121, +0.0440] and [-0.1228, +0.0636].**

### AUX-V2RCAT-A2-SPEND

Token-metered from the rows at OpenAI's page prices of 2026-09-18 (input, cache-write at 1.25x, cached at the cached rate, output): Luna $0.7570, Sol $11.7984, both $12.5554, probes $0.0110, against the cap of $14; not an invoice.

