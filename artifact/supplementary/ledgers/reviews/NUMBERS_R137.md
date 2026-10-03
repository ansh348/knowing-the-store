# NUMBERS_R137.md: the R137 pass (the long-list check landed, the prediction recount, Figure 1 rendered; 2026-09-22)

Written by `reviews/v23/tools/ledger_r137.py` from the checks of `reviews/v23/tools/r137_number_gate.py`; every value is read from the artifact named (`cf_pad/results/cf_pad_scores.json`, scored once at 6d7f224 under registrations/ADDENDUM_CF_PAD.md, registered text sha256 a84dac1a..., frozen alone at 06c611f; `cf_pad/build/lock.json`; `reviews/NUMBERS_R131.md` AUX-R131-COUNT; `iclr2027_monitoring_submission/ARTIFACT/manifests/indexes_v2.json`; `e1_metamemory/backend_entries/frbank.json`). Printed forms are half-up on the four-decimal recorded value at two decimals in the body (the convention of reviews/NUMBERS_R131.md), magnitudes with the direction in words, and four decimals in the appendix. The appendix tables tab:cfpad-* are written by `cf_pad/tools/cfpad_tex.py` (`cf_pad/results/cfpad_tab_*.tex`) and every value in them is a row of `cf_pad/NUMBERS_CF_PAD.md` (AUX-CFP-*); tab:robust is written by `reviews/v23/tools/robust_tex.py`.

## AUX-R137-ROBUST9: tab:robust's row 9 as built (the long-list check in place of the 661-set padding and the injection, which stay in Appendix C.2)

| row | what we tried to break | what it removes | what happened (as printed) | metric | population | status | source |
|---|---|---|---|---|---|---|---|
| 9 | List padded to 60 names | Short, clean lists | Lookup $0.92$ to $0.74$; mini, Haiku, Opus fall with it; Luna, Sol lose $0.06$ to $0.07$, lead it by $0.13$ to $0.14$ | pooled | the counterfactual set, supersession (88 triples); Opus one draw against its recorded five-draw row | registered | cf_pad_scores.json readers/LOOKUP/superseded/pooled {unpadded 0.9223, padded 0.7416} (AUX-CFP-READERS-SUPERSEDED); readers/{LUNA,SOL}/superseded/pooled/padded_minus_unpadded (-0.0636, -0.0693, both reliable); minus_lookup/{LUNA,SOL}/LOOKUP/superseded/padded/pooled (+0.1375, +0.1274, both reliable on both metrics; AUX-CFP-MINUS-LOOKUP-SUPERSEDED); mini -0.0525, Haiku -0.0062, Opus -0.0336 minus the lookup, intervals including zero (P-L2 holds, P-L1 fails on Opus) |

## AUX-R137-COUNT: the prediction count with the long-list check's four predictions in it

AUX-R131-COUNT: 98 predictions, 31 otherwise (tab:registrations-e 5 with 2). ADDENDUM_CF_PAD registered four predictions with a bar, each read on the pooled AUROC of the supersession slice: P-L1 (FAILS); P-L2 (HOLDS); P-L3 (HOLDS); P-L4 (FAILS); each counts once, 2 otherwise (P-L1 and P-L4 fail on Opus 5 alone). **With them: 102 predictions, 33 otherwise; tab:registrations-e carries 9 with 4**; the other four tables unchanged (47 with 8; 17 with 10; none; 29 with 11). Section 4's sentence and Appendix F's count paragraph print the new pair.

## AUX-R137-FIG1: Figure 1's rendered summary, transcribed from the summary the E.1 excerpt was cut from (`ARTIFACT/manifests/indexes_v2.json` key `frbank:david:FULL:BELIEVED`, the same key AUX-R86-INDEX-EXCERPT transcribes; asserted equal to `e1_metamemory/indexes_v2.json`)

| line in the summary | value |
|---|---|
| `LIFECYCLE TOTALS` active | **377** |
| `LIFECYCLE TOTALS` superseded | **197** |
| `LIFECYCLE TOTALS` retracted | **1** |
| `LIFECYCLE TOTALS` expired | **49** |
| `ATTRIBUTE NAMES BY CATEGORY` HOBBIES_RECREATION, the first three names printed | current_reading_list, hiking_experience, hiking_preference (of 11) |
| `ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT`, the two names printed | exam_date, hiking_preference (both in the list's first 15) |
| the tag route's returned record | `e1_metamemory/backend_entries/frbank.json` lb_00163 (persona david, category HOBBIES_RECREATION, slot hiking_preference); FR-Bank's own tag: superseded (believed_superseded True); text "User prefers moderate difficulty hikes in the six to ten mile range." |

The figure prints these lines and nothing else of the summary; the E.1 excerpt prints the category rows, the ages and the name lines of the same summary.

## AUX-R137-PRINTED: every number and claim the pass's new texts print, beside its source

77 checks, 0 mismatches (`r137_number_gate.py`, this pass's own; R134's 62 and R135's 37 run first, unchanged).

| where (the sentence) | printed | recorded value | reliable, claimed / actual | source |
|---|---|---|---|---|
| tab:robust row 9: 'Lookup 0.92' (supersession, pooled, unpadded) | 0.92 | +0.9223 |  | cf_pad_scores.json readers/LOOKUP/superseded/pooled/unpadded (AUX-CFP-READERS-SUPERSEDED; the recorded Table 1 row on the slice) |
| tab:robust row 9: 'to 0.74' (padded) | 0.74 | +0.7416 |  | readers/LOOKUP/superseded/pooled/padded |
| 5.2 / abstract: 'the lookup loses 0.18' (padded minus unpadded, pooled, supersession; reliable; P-L3) | 0.18 | -0.1807 | True / True | readers/LOOKUP/superseded/pooled/padded_minus_unpadded -0.1807 [-0.2420,-0.1272]; [-0.2335,-0.1311] (AUX-CFP-P-L3 HOLDS) |
| 5.2: P-L3 holds | HOLDS | HOLDS |  | predictions/P-L3 |
| tab:robust row 9 / 5.2 / abstract: 'mini falls with it' (padded minus unpadded reliable and below zero; not reliably above the lookup) | falls | falls |  | readers/MINI/superseded/pooled/padded_minus_unpadded -0.1902; minus_lookup/MINI/LOOKUP/superseded/padded/pooled -0.0525 (intervals including zero) |
| 5.2: 'mini ends level with the lookup or below' (padded minus lookup at or below zero at the point) | at or below | at or below |  | minus_lookup/MINI/LOOKUP/superseded/padded/pooled -0.0525 |
| tab:robust row 9 / 5.2 / abstract: 'Haiku falls with it' (padded minus unpadded reliable and below zero; not reliably above the lookup) | falls | falls |  | readers/H45/superseded/pooled/padded_minus_unpadded -0.1522; minus_lookup/H45/LOOKUP/superseded/padded/pooled -0.0062 (intervals including zero) |
| 5.2: 'Haiku ends level with the lookup or below' (padded minus lookup at or below zero at the point) | at or below | at or below |  | minus_lookup/H45/LOOKUP/superseded/padded/pooled -0.0062 |
| tab:robust row 9 / 5.2 / abstract: 'Opus falls with it' (padded minus unpadded reliable and below zero; not reliably above the lookup) | falls | falls |  | readers/OP5/superseded/pooled/padded_minus_unpadded -0.2245; minus_lookup/OP5/LOOKUP/superseded/padded/pooled -0.0336 (intervals including zero) |
| 5.2: 'Opus ends level with the lookup or below' (padded minus lookup at or below zero at the point) | at or below | at or below |  | minus_lookup/OP5/LOOKUP/superseded/padded/pooled -0.0336 |
| 5.2: 'mini and Opus lose more than the lookup' (the brief's 'as much or more' corrected: Haiku loses less at the point) | more | more |  | mini -0.1902, Opus -0.2245 against the lookup's -0.1807 |
| 5.2: Haiku loses less than the lookup at the point (why the brief's 'as much or more' is not printed; 'fall with it' is) | less | less |  | Haiku -0.1522 against the lookup's -0.1807 |
| tab:robust row 9 / 5.2 / abstract: 'Luna and Sol lose 0.06' (the smaller of the two falls; both reliable) | 0.06 | +0.0636 | True / True | readers/LUNA/superseded/pooled/padded_minus_unpadded -0.0636, SOL -0.0693 |
| tab:robust row 9 / 5.2 / abstract: 'to 0.07' (the larger) | 0.07 | +0.0693 |  | as above |
| 5.2 / P-L4: 'Luna and Sol lose less than the lookup' (point estimates) | less | less |  | Luna -0.0636, Sol -0.0693 against the lookup's -0.1807 |
| Limitations / P-L4: Opus loses more than the lookup (P-L4 fails on Opus alone) | FAILS on Opus | FAILS on Opus |  | predictions/P-L4 per_model: Luna loses_less True, Sol True, Opus False (Opus -0.2245) |
| tab:robust row 9 / 5.2 / abstract / Conclusion: 'lead the lookup by 0.13' (the smaller pooled lead; both reliable) | 0.13 | +0.1274 | True / True | minus_lookup/LUNA/LOOKUP/superseded/padded/pooled +0.1375, SOL +0.1274 (AUX-CFP-MINUS-LOOKUP-SUPERSEDED; P-L1 fails on Opus alone) |
| tab:robust row 9 / 5.2 / abstract / Conclusion: 'to 0.14' (the larger pooled lead) | 0.14 | +0.1375 |  | as above |
| 5.2: 'and 0.09 within triples' (the smaller matched lead; both reliable; the brief's 'on both metrics' made explicit) | 0.09 | +0.0909 | True / True | minus_lookup/LUNA/LOOKUP/superseded/padded/matched +0.1023, SOL +0.0909 |
| 5.2: 'to 0.10 within triples' (the larger matched lead) | 0.10 | +0.1023 |  | as above |
| 5.2 / 1 / Conclusion: 'two of five' reliably above the lookup on the padded list (pooled; P-L1 fails on Opus, P-L2 holds) | 2 | 2 |  | minus_lookup/*/LOOKUP/superseded/padded/pooled, both intervals above zero |
| 5.2 / 1: the two are Luna and Sol | LUNA,SOL | LUNA,SOL |  | as above |
| 5.2 / 1: the same two on the matched metric | LUNA,SOL | LUNA,SOL |  | minus_lookup/*/LOOKUP/superseded/padded/matched |
| 5.2: P-L1 fails and P-L2 holds | FAILS,HOLDS | FAILS,HOLDS |  | predictions/P-L1, P-L2 |
| 5.2 / C.2: 'Retraction and expiry do not move' (the reliable changes there: Haiku matched and Opus pooled on retraction only) | H45 retracted matched; OP5 retracted pooled | H45 retracted matched; OP5 retracted pooled |  | readers/*/{retracted,expired}/{pooled,matched}/padded_minus_unpadded both_exclude_zero |
| C.2: the LOOKUP lookup at chance on retracted, padded and unpadded | 0.50/0.50 | 0.50/0.50 |  | readers/LOOKUP/retracted/pooled |
| C.2: the LOOKUP lookup at chance on expired, padded and unpadded | 0.50/0.50 | 0.50/0.50 |  | readers/LOOKUP/expired/pooled |
| C.2: the LEX lookup at chance on retracted, padded and unpadded | 0.50/0.50 | 0.50/0.50 |  | readers/LEX/retracted/pooled |
| C.2: the LEX lookup at chance on expired, padded and unpadded | 0.50/0.50 | 0.50/0.50 |  | readers/LEX/expired/pooled |
| C.2: the RANDTOK lookup at chance on retracted, padded and unpadded | 0.50/0.50 | 0.50/0.50 |  | readers/RANDTOK/retracted/pooled |
| C.2: the RANDTOK lookup at chance on expired, padded and unpadded | 0.50/0.50 | 0.50/0.50 |  | readers/RANDTOK/expired/pooled |
| Limitations / tab:robust caption / C.2: 'Opus 5 ran one draw against its five-draw row' | 1 / 5 | 1 / 5 |  | census/OP5 k_new, k_recorded |
| Limitations: 'the two readers that keep their lead there are from one model family' | one family | one family |  | GPT-5.6 Luna and GPT-5.6 Sol: OpenAI |
| abstract / 1 / 5.2 / tab:robust: 'padded to 60 names' (every PN list exactly 60) | 60/60 | 60/60 |  | build/lock.json list_length by_state_version superseded|PN |
| 4 / F: the prediction count, M (98 + the four P-L predictions) | 102 | 102 |  | NUMBERS_R131.md AUX-R131-COUNT 98 + cf_pad_scores.json predictions 4 |
| 4 / F: the prediction count, N (31 + the two that came out otherwise) | 33 | 33 |  | NUMBERS_R131.md AUX-R131-COUNT 31 + 2 (P-L1, P-L4) |
| F: tab:registrations-e carries 9 with 4 | 9 with 4 | 9 with 4 |  | AUX-R131-COUNT 5 with 2, plus 4 with 2 |
| F: the registration's four predictions, P-L1 to P-L4 | P-L1,P-L2,P-L3,P-L4 | P-L1,P-L2,P-L3,P-L4 |  | predictions |
| F: outcomes | FAILS,HOLDS,HOLDS,FAILS | FAILS,HOLDS,HOLDS,FAILS |  | predictions/*/holds |
| F: the frozen commit | 06c611f | 06c611f |  | cf_pad_scores.json lock/frozen_commit (registrations/ADDENDUM_CF_PAD.md frozen alone before the first paid call) |
| F: the freeze day (2026-09-22 against day 0 = 2026-08-10) | 43 | 43 |  | reviews/NUMBERS_R126.md AUX-R126-DAYS; cf_pad/build/lock.json 'when' 2026-09-22 |
| F: the registered text's sha256 prefix | a84dac1a | a84dac1a |  | cf_pad_scores.json registration_sha256 |
| C.2: the population (items / triples / supersession items / supersession triples) | 444/148/264/88 | 444/148/264/88 |  | lock.json n_rows, n_pairs; readers/LOOKUP/superseded n |
| C.2: the counted states (items / triples each) | 90/30 | 90/30 |  | readers/LOOKUP/retracted n |
| C.2: lists 57 to 60 names long | 57-60 | 57-60 |  | lock.json list_length min, max |
| C.2: pool A 71 to 121 names, median 102; no pad on pool B | 71/102/121/0 | 71/102/121/0 |  | lock.json pools |
| C.2: the target's rank: min 2, median 41.5, max 60, never first, last on 4 of 88 (the brief's 'median 41' corrected to the ledger's 41.5) | 2/41.5/60/0/4/88 | 2/41.5/60/0/4/88 |  | lock.json target_position |
| C.2: the rank by tenths of the list | 5/3/2/5/8/12/12/9/9/23 | 5/3/2/5/8/12/12/9/9/23 |  | lock.json target_position deciles |
| C.2: renderer lock 444 of 444; leak scan 0 fails | 444/0 | 444/0 |  | lock.json renderer_lock, leak_scan |
| C.2 / tab:setup: draws (mini, Haiku, Luna, Sol, Opus) | 5/5/5/5/1 | 5/5/5/5/1 |  | census/*/k_new |
| C.2: rows per five-draw lane / Opus; not-OK rows | 2220/444/0 | 2220/444/0 |  | census/*/rows, not_ok |
| C.2 / E.11: Anthropic spend of the cap | 8.11 of 12 | 8.11 of 12 |  | spend/anthropic (token-metered, not an invoice) |
| C.2 / E.11: OpenAI spend of the cap | 15.54 of 20 | 15.54 of 20 |  | spend/openai |
| C.2: no cap reached, no draw dropped, no STOP fired, no deviation | clean | clean |  | cf_pad_scores.json stops, census/*/complete_draws; cf_pad/DEVIATIONS_CF_PAD.md |
| C.2: the tolerance | 0.05 | +0.0500 |  | cf_pad_scores.json tol |
| C.2 P-L1: LUNA minus the lookup +0.1375 (reliably above: True) | +0.1375 | +0.1375 |  | predictions/P-L1 per_model against minus_lookup |
| C.2 P-L1: SOL minus the lookup +0.1274 (reliably above: True) | +0.1274 | +0.1274 |  | predictions/P-L1 per_model against minus_lookup |
| C.2 P-L1: OP5 minus the lookup -0.0336 (reliably above: False) | -0.0336 | -0.0336 |  | predictions/P-L1 per_model against minus_lookup |
| C.2 P-L2: MINI minus the lookup -0.0525 (reliably above: False) | -0.0525 | -0.0525 |  | predictions/P-L2 per_model against minus_lookup |
| C.2 P-L2: H45 minus the lookup -0.0062 (reliably above: False) | -0.0062 | -0.0062 |  | predictions/P-L2 per_model against minus_lookup |
| C.2: Opus's recorded draw 1 alone, superseded, pooled | 0.9317 | 0.9317 |  | descriptive/opus_recorded_draw1/superseded |
| C.2: Opus padded minus its recorded draw 1, superseded (reliable) | -0.2236 | -0.2236 | True / True | the same block: a_auroc - b_auroc |
| C.2: Opus's recorded draw 1 alone, whole, pooled | 0.8400 | 0.8400 |  | descriptive/opus_recorded_draw1/whole |
| C.2: Opus padded minus its recorded draw 1, whole (reliable) | -0.1873 | -0.1873 | True / True | the same block: a_auroc - b_auroc |
| C.2: 'the fall is not the draw count' (the one-draw padded row minus the recorded draw 1 is reliable and as large as minus the five-draw row, within 0.01) | not the draw count | not the draw count |  | padded minus draw 1 -0.2236 against padded minus the five-draw row -0.2245 |
| C.2: seeds 43 to 46 change no registered reading | 0 | 0 |  | descriptive/seed_spot_check: [] |
| C.2: one interval of one difference moves (mini minus the lookup, seed 45, persona) | MINI_minus_LOOKUP/45/persona | MINI_minus_LOOKUP/45/persona |  | descriptive/seed_spot_check |
| C.2: the seeds | 43-46 | 43-46 |  | descriptive/seed_spot_check keys |
| C.2: every lane served one identifier and every row was OK | one each, 0 not OK | one each, 0 not OK |  | census/*/served {'H45': ['claude-haiku-4-5-20251001'], 'LUNA': ['gpt-5.6-luna'], 'MINI': ['gpt-4.1-mini-2025-04-14'], 'OP5': ['claude-opus-5'], 'SOL': ['gpt-5.6-sol']} |
| Figure 1: LIFECYCLE TOTALS active | 377 | 377 |  | ARTIFACT/manifests/indexes_v2.json frbank:david:FULL:BELIEVED, LIFECYCLE TOTALS (transcribed, as AUX-R86-INDEX-EXCERPT transcribes the same summary's category rows) |
| Figure 1: LIFECYCLE TOTALS superseded | 197 | 197 |  | ARTIFACT/manifests/indexes_v2.json frbank:david:FULL:BELIEVED, LIFECYCLE TOTALS (transcribed, as AUX-R86-INDEX-EXCERPT transcribes the same summary's category rows) |
| Figure 1: LIFECYCLE TOTALS retracted | 1 | 1 |  | ARTIFACT/manifests/indexes_v2.json frbank:david:FULL:BELIEVED, LIFECYCLE TOTALS (transcribed, as AUX-R86-INDEX-EXCERPT transcribes the same summary's category rows) |
| Figure 1: LIFECYCLE TOTALS expired | 49 | 49 |  | ARTIFACT/manifests/indexes_v2.json frbank:david:FULL:BELIEVED, LIFECYCLE TOTALS (transcribed, as AUX-R86-INDEX-EXCERPT transcribes the same summary's category rows) |
| Figure 1: HOBBIES_RECREATION's first names | current_reading_list, hiking_experience, hiking_preference, hiking_preference_scenery | current_reading_list, hiking_experience, hiking_preference, hiking_preference_scenery |  | the same summary, ATTRIBUTE NAMES BY CATEGORY |
| Figure 1: the superseded-names line carries hiking_preference and exam_date | yes | yes |  | the same summary, ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT |
| Figure 1: the tag route's returned record (David's HOBBIES_RECREATION hiking_preference) carries FR-Bank's own superseded tag | superseded | superseded |  | e1_metamemory/backend_entries/frbank.json lb_00163 believed_superseded True |
| Figure 1: the record's text | User prefers moderate difficulty hikes in the six to ten mile range. | User prefers moderate difficulty hikes in the six to ten mile range. |  | frbank.json lb_00163 text |

