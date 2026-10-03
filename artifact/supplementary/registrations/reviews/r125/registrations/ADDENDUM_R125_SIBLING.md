# ADDENDUM_R125_SIBLING: the sibling-name control on the counterfactual set (Task 4 of R125)

Registration of program R125 (the brief "KtS R125: matched metric, sibling-name control, store-relative labels, strong-model ablations", 2026-09-20), written BEFORE any call on these items and frozen by the sha256 of the bytes above the marker line, recorded in `reviews/r125/FREEZE_R125.md`; the runner and the scorer assert it at start. This file lives under `reviews/r125/registrations/` (the brief's fence); the main session copies it to `registrations/` at landing if the author so rules. Four predictions (P-SB1 to P-SB4) with the outcome vocabulary HELD / FAILED / NOT EVALUABLE, and one descriptive reading. Nothing here re-adjudicates a CF-2 row; every recorded row is read and never re-run.

## §1: Why

On the counterfactual set the PN version of a supersession pair differs from its PRESENT sibling in the superseded-names section (the target's name appears) and in the count cells (the category's superseded column and the lifecycle total rise by one). Task 1 showed that the design-matched comparison, PN against PRESENT within the pair, still rewards a reader that scores the longer list higher without reading any name: the random-token lookup reads 0.7443 on the supersession pairs (AUX-CF2-R125-MATCHED-V2), and Task 2 showed that 24 of the 88 PRESENT versions carry an empty list. The reviewers' request is a control that separates name binding from list emptiness. The SIBLING version keeps every count and the list's length and changes only WHICH name the list carries, so a count reader and the random-token control are at chance by construction (the count reader exactly; the token control up to the token drawn for the sibling), and what is left is the binding of a name to the question.

## §2: Population and the recorded rows (read, never re-run)

The 88 supersession pairs of the counterfactual set (`r82_counterfactual/cf2/cf_cell.json`, `cf_indexes.json` key `v2`, `cf_pairs_cf2.json`), their PN and PRESENT versions under the superseded-only summary. Recorded rows read: GPT-4.1 mini at five draws (`reviews/r122/rows/rows_MINI5.jsonl`, `INDEXED-V2`; Table 1's row, AUX-R122-K5), Haiku 4.5 (`cf2/rows/rows_H45.jsonl`, k = 5), GPT-5.6 Luna (`cf2/rows/rows_LUNA.jsonl`, k = 5), Opus 5 (`cf2/rows/rows_OP5.jsonl`, draw 1 of the recorded five), GPT-5.6 Sol (`cf2/rows/rows_SOL.jsonl`, draw 1 of the recorded five); the name lookup on the v2 lists (AUX-CF2-NB6-V2 0.7663), the random-token control (AUX-R122-ENC-RANDOM 0.5954; `enc_lookup.random_token`, seed 42) and the category-guessing count reader (AUX-R110-A1-CR, CR-nb1 0.6623), all reproduced at four decimals by `reviews/r125/tools/r125_readers.py` (`results/r125_vectors.json`). The 88 pairs' PN-vs-PRESENT matched values of Task 1 print beside.

## §3: The construction (`reviews/r125/tools/r125_t4_build.py`; built before this registration; no model call)

For each of the 88 pairs a fourth summary, SIBLING, is rendered from the PN version's v2 text by replacing the target's name in the ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT section with a sibling attribute name from the same category; every other line, the count table and the name map included, is byte-identical to the PN text (asserted), so the category counts are exactly the PN version's. The section is re-rendered by the renderer's own rule (`index_v2.render`'s name block: sorted names, comma-joined, wrapped at 150 columns with the two-space and four-space indents); the lock asserts that the PN section re-renders byte-identically under the same rule, that `index_v3.named_sections` reads the intended list, that `index_features.parse` agrees with PN on every field but `superseded_attrs`, and that the list's length is unchanged.

**Sibling rule** (seed 12501; `numpy.random.default_rng(12501)`, one integer draw per kept pair in pair-id order, uniform over the sorted eligible names). The persona's name map is the ATTRIBUTE NAMES BY CATEGORY section as printed (`index_features.parse`, `attr_by_cat`); the pool is the names printed under the target's category (`cf_pairs_cf2.json` `pairs[].category`) in all three versions of the pair (PN, PRESENT, ABSENT: present in every version, HV-B's rule 6.4 (a), `human_validation/hv1/REGISTRATION_HV1.md`). Excluded: the target slot (HV-B 6.4 (c)); any name already in the PN version's superseded-names list (so the list changes in exactly one name); any name in the target's encoder neighbourhood (HV-B 6.4 (d): cosine under `sentence-transformers/all-MiniLM-L6-v2`, `run_baselines.encoder`, on the two names with underscores as spaces, at or above tau 0.503637, `registrations/ADDENDUM_RESP.md` C.2); any name sharing a content token (`e0_common.toks`, the persona's name dropped) with the question or with the target name. A pair with no eligible sibling drops, with the count reported. **Built: 88 of 88 pairs kept, 0 dropped; eligible names per pair min 2, median 11, max 16; the texts' sha256 `f54a7527d37d1a55…` (`reviews/r125/build/build_t4_sibling.json`).** Label: PRESENT under Definition 1 (the stale record the list names is not relevant to the question), `y_nok` 0.

**Leak screen**, as for CF-2 (`cf2_leakscreen.py`'s rule, reproduced in `r125_run.py leak`): the 88 SIBLING items sorted by item id, `random.Random(42).sample(pool, 30)`; gpt-4.1-mini at temperature 0, seed 42, max_tokens 200 with `prompts_e1.LEAKAGE_SYSTEM` / `LEAKAGE_USER`; gold = the pair's `entry_text`; `exp4_witnesses.supports_correct`; the cell LEAKS iff more than 3 of 30 score correct, and a leak is a STOP.

## §4: Lanes (`reviews/r125/tools/r125_run.py`; only the SIBLING items are new calls)

Prompts `prompts_e1.SYSTEM` / `USER_INDEXED` verbatim (digests asserted at import); the served identifier asserted on every row (E1.7); rows under `r82_counterfactual/cf2/rows/rows_r125_<LANE>.jsonl`.

| lane | model | settings (the analogue copied) |
|---|---|---|
| SB-MINI5 | gpt-4.1-mini | k = 5, temperature unset (the provider default), max_tokens 200, synchronous, draw-major, eight workers (Table 1's row: R122 T3, D-R122-1) |
| SB-H45 | claude-haiku-4-5-20251001 | k = 5, temperature 0, max_tokens 200, Message Batches, X4 collapse (E1 / CF-2) |
| SB-LUNA | gpt-5.6-luna | k = 5, raw Chat Completions, reasoning effort and temperature unset, max_completion_tokens 2048, draw-major, eight workers (E5) |
| SB-OP5 | claude-opus-5 | k = 1, temperature unset, max_tokens 1024, Message Batches (E1's settings, one draw) |
| SB-SOL | gpt-5.6-sol | k = 1, raw Chat Completions, E5's settings |

The no-model readers on the SIBLING texts, $0: the name lookup (`score_cf.matcher` on the SIBLING list), the random-token lookup (the same token map extended to the sibling names, `enc_lookup.random_token`, seed 42; the map reproduces the recorded 0.5954 on the 444, asserted), the category-guessing count reader (`a1_count_readers.reader_scores`, CR-nb1, on the SIBLING text; asserted equal to its PN score on every pair).

## §5: Estimands and predictions (`reviews/r125/tools/r125_t45_score.py t4`)

Primary estimand, per reader: the matched AUROC of PN against SIBLING within the pair, (W + T/2) / n over the kept pairs, ties exact equality of the collapsed scores; W/T/L; the triple-level bootstrap (pairs resampled) and the persona-grouped bootstrap (personas resampled, pairs intact), 1,000 draws, seed 42, 2.5 / 97.5 percentiles. Readers: GPT-4.1 mini (five-draw means on all three versions), Haiku 4.5 (five-draw means), GPT-5.6 Luna (five-draw means), Opus 5 (draw 1 on all three versions), GPT-5.6 Sol (draw 1), the name lookup, the random-token lookup, the count reader. Beside: the pooled AUROC of the 88 PN against the 88 SIBLING items; the matched PN-vs-PRESENT on the same pairs (Task 1's values); the paired matched difference of each model against the name lookup (model's PN-vs-SIBLING outcome minus the lookup's, per pair, both bootstraps).

- **P-SB1.** The name lookup reads 0.90 or higher. HELD iff matched ≥ 0.90.
- **P-SB2.** Every model reads 0.80 or higher with the persona interval excluding 0.50. HELD iff, for each of the five models, matched ≥ 0.80 and the persona interval's lower bound is above 0.50; a model whose lane did not run is NOT EVALUABLE and the verdict is stated on the models run.
- **P-SB3.** The random-token lookup and the count reader are within tolerance of 0.50: |matched − 0.50| ≤ 0.05 for both. HELD iff both.
- **P-SB4.** No model reliably exceeds the name lookup: HELD iff no model's paired matched difference against the lookup is positive with both intervals above zero.
- **Descriptive, no bar.** SIBLING minus PRESENT for each reader: the mean score difference over the pairs with both bootstraps, and the matched AUROC of SIBLING against PRESENT with W/T/L (how far an unrelated name in the list raises the score: the list-emptiness component).

Failure texts are the numbers: "P-SBk FAILS: [reader] reads [value] with intervals [triple] and [persona]." No paper text is written by this session; the main session writes from the ledger.

## §6: Budget, order, STOP

Neither API exposes a credit balance to the keys in use (OpenAI `organization/costs` needs `api.usage.read`; Anthropic's cost report needs an Admin key; probed 2026-09-20, both refused), so the month's token-metered spend from the rows in the tree is printed in the freeze record in its place (September 2026, files deduplicated by content: Anthropic $143.76, OpenAI $43.78) and the projection is read against the brief's caps: **Anthropic $10.00, OpenAI $10.00, enforced in the runner** (metered from the rows at the recorded page prices, checked before every synchronous call; a Batch is submitted only if the vendor's metered spend plus the Batch's projection at ×1.3 stays under the cap). Projection from one probe per lane on the first SIBLING item (`r125_run.py probe`, then `project`): input tokens scaled by each unit's characters, OpenAI draws 2 to 5 at the cached rate (E5's cost rule), Anthropic Batch at 0.5. Order: freeze commit → leak screen → probes → projection → SB-MINI5, SB-LUNA, SB-SOL synchronous; SB-H45, SB-OP5 submitted as Batches → poll → score. STOP: a registration sha256 mismatch; a lock failure; a served-identifier mismatch; a leak; a projection over a cap; more than 2 percent of a lane's rows not OK after the retry.

## §7: Ledger and paper site

`r82_counterfactual/cf2/NUMBERS_CF2.md` section 15d: `AUX-CF2-R125-SB-LOCK`, `-SB-CENSUS`, `-SB-LEAK`, `-SB-PROBES`, `-SB-PROJECTION`, `-SB-<READER>` (one row per reader), `-SB-P-SB1` to `-SB-P-SB4`, `-SB-DESCRIPTIVE`, `-SB-SPEND`. Paper site: the main session's; nothing lands from here.

## §8: Disclosures

This registration follows every earlier result on the same items (CF-2, E2, E5, E9, E10, R121, R122, Task 1's matched rows and Task 2's list census), so no confirmatory design is claimed. The scorer was dry-run once before this freeze to check its code path; the dry run computed the three no-model readers' values on the SIBLING texts (the name lookup 0.9489, 82/3/3; the random-token lookup 0.4716, 25/33/30; the count reader 0.5000, 0/88/0), so **P-SB1 and P-SB3 are recorded values rather than predictions** and print as such; no model row existed at the dry run, so P-SB2 and P-SB4 are untouched by it. The predictions' wording is the brief's.

<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
