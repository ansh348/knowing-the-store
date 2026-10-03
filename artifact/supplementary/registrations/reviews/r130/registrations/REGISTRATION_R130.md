# REGISTRATION_R130 — Knowing the Store: a stronger answerer on the recorded answer-stage views, and a semantic judge the human labels can validate

Program **R130**, written 2026-09-20 on the author's brief of the same day ("KtS R130: a stronger answerer, and a judge the human labels can validate (new session, exploratory)") and the author's twelve rulings of the same day on the Phase 0 report (`reviews/r130/PHASE0_REPORT.md`), all applied before any answer exists. **Exploratory throughout**: every number this program produces is labelled exploratory wherever it is reported, and no paper text lands from it. Fenced to `reviews/r130/`, with the rows, probes, lock, projection and batch records under `ds_downstream/run/` carrying an `r130` prefix, and one appended section (16) of `ds_downstream/NUMBERS_DS.md`; nothing in `reviews/v22/`, `reviews/r125/` or `human_validation/` is touched. Every commit uses a private git index and an explicit pathspec. This file is frozen by the sha256 of the bytes above the marker line, recorded in `reviews/r130/FREEZE_R130.md` before any call; every tool that calls an API or scores asserts it at start.

Caps, enforced in `reviews/r130/tools/r130_run.py` from the rows at the page prices: **OpenAI $4.00, Anthropic $8.00**. Generation and judging are to be finished before the experiment freeze on the night of 21 September; validation against the human labels is scoring only and may follow.

Three tasks. **A**: GPT-5.6 Luna answers the views the E.10 answer stage recorded for GPT-4.1 mini and Claude Haiku 4.5. **B**: one semantic judge (Claude Opus 5) labels every recorded answer of the three answerers with the human validation sheet's five labels, and is validated against annotator A1's labels on the same 198 rows that validate the token detector. **C**: six predictions about Luna (four primary: P-L1, P-L4, P-L2, P-L3; two secondary: P-L1b, P-L3b), frozen here with the judge prompt before any Luna answer exists.

---

## §1. Why

The answer-stage experiments in Appendix E.10 used GPT-4.1 mini and Haiku 4.5 as answerers, the two models that also fail to follow a stated intent rule and a moved count. Among the 89 scorable obligation views, 35 hold an untagged active copy of the stale value (34 once one inverted ground-truth tag is corrected), and the flagged stale answers trace to those copies even when the forbidding record is present and tagged. Two readings are open: the untagged copies bind any answerer, or a stronger answerer acts on the tags and reconciles the copy. This program separates them by adding a third answerer on the same views. The token detector cannot score the comparison: its length bias makes comparisons across answerers invalid and it cannot score expiry. So the program needs a second instrument, a semantic judge, validated on the same human labels that are validating the detector.

---

## §2. Corrections and disclosures, recorded before anything runs

**2a. Two of the brief's seven policies have no recorded answer under the E.10 harness and are NOT EVALUABLE here.** The brief names "similarity at the matched budget" and "the always-on fetch at the matched budget". Those are Table 3's reach-only rows (R122 T5, `reviews/r122/registrations/ADDENDUM_R122_GATE_REACH.md`): each is a linear interpolation between two integer truncations (TAGGED-5 / TAGGED-6; AF-4 / AF-5), no answer was ever called on them, and the brief's own rule ("same views ... do not regenerate any mini or Haiku answer") leaves no comparator for them. They are reported as **NOT EVALUABLE** under this registration (ruling 1 of 2026-09-20: reach-only rows, no comparator). No Luna-only call is made on those views.

**2b. The policies with recorded answers are the seven DS policies and the retag variant.** Top-five retrieval (ALWAYS), the model rule (MODEL), the lookup rule (LOOKUP), the model and lookup rules with all states named (MODEL-ALL, LOOKUP-ALL), the literal lookup rule (LOOKUP-LIT, descriptive) and the oracle (ORACLE), all under the Amendment 4 header; and the reference-assisted retag variant (Amendment 5, diagnostic). The brief's named policies (top-five, lookup, model, oracle, retag) are the primary rows; the other three print beside because they cost nothing extra (an answer is one call per distinct view, and the seven policies share views).

**2c. The population is the E.10 harness's own.** The harness calls an obligation under a policy only where the forbidding record reached the view and the policy did not abstain (`registrations/ADDENDUM_DS.md`, section D.4; ruling R3). So under top-five retrieval only the **54** obligations it reaches have an answer, under the lookup rule **70** (85 reached, 22 abstained by the coverage gate, some of them unreached), under the oracle **99**; five obligations have no answered view under any policy (`frbank:bruna:bruna_q06:CAT-ABLATED`, `frbank:fatima:fatima_q06:SLOT-ABLATED`, `frbank:joonho:joonho_q04:FULL`, `frbank:marcus:marcus_q10:CAT-ABLATED`, `frbank:mirri:mirri_q04:CAT-ABLATED`). The 104 obligations are 63 supersession, 26 retraction and 15 expiry, over 28 personas. **231** distinct (obligation, view) pairs carry a recorded mini and a recorded Haiku answer across the seven policies; the retag changed **74** views (45 supersession, 29 retraction; 35 obligations). Luna answers those **305** views, once each, and nothing else.

**2d. P-L2's pairing is thin by construction.** The obligations answered under both top-five retrieval and the lookup rule number **40**; on **24** of them the lookup rule fetched nothing and its view is byte-identical to the top-five view, so the answer is the same by construction (one call per distinct view) and the pair is concordant. **16** pairs can differ. The prediction is registered as the brief words it, on the 40, with the 16 stated (ruling 2); a descriptive "of 104" reading (every obligation, an unanswered policy counting as not ASSERTS, Table tab:ds-body's convention) prints beside. **With 16 informative pairs P-L2 is expected to be underpowered**: it cannot be reliable unless at least six of the sixteen move one way and none the other (§5, the size note), and its outcome is read as a direction, not a finding.

**2e. The judge shares a vendor with one answerer.** The judge is Claude Opus 5 (Anthropic); Claude Haiku 4.5 is one of the three answerers. Disclosed here and wherever the judge's numbers are reported.

**2f. The validation sample holds mini answers only.** The 198 primary rows of HV-A are GPT-4.1 mini answers (148 on the 74 retag-changed views before and after, 50 controls); the optional block is 50 flagged Haiku answers. No Luna answer is in the human sample. The judge's validated accuracy therefore transfers to Luna's answers, which are longer and reasoned, only by assumption; the report says so beside every Luna number.

**2g. Luna's settings (ruling 4): mini's answer-stage settings wherever the parameter exists for Luna, raw API as in E5.** The mini lane ran at temperature 0, seed 42, `max_tokens` 200, JSON mode, one retry on a parse failure. A settings check on `gpt-5.6-luna` before the freeze (one-line prompt, no item text; `reviews/r130/build/luna_settings_check.json`) found: **temperature 0 rejected** by the model (`400 unsupported_value: 'temperature' does not support 0 with this model. Only the default (1) value is supported`); **seed 42 and JSON mode (`response_format` `json_object`) accepted**. So every Luna call carries `seed=42` (best-effort on the API; the system fingerprint is recorded per row) and `response_format={"type": "json_object"}`; temperature is unset (recorded as rejected); `max_completion_tokens` is E5's 2048, because Luna's limit counts its reasoning tokens where mini's `max_tokens` 200 counted output only, so 200 would truncate the reasoning; reasoning effort is unset, as E5 set it; one retry on a parse failure, as mini. Every setting is recorded in `FREEZE_R130.md` and in `run/lock_r130.json`.

**2i. Limits (ruling 11).** The judge is validated on GPT-4.1 mini's answers only (the human sample, §6), so its use on Luna's and Haiku's answers assumes the labels transfer across answerers; Luna's answers are longer and reasoned, and the report says so beside every Luna and Haiku number. The judge (Claude Opus 5) shares a vendor with one answerer (Claude Haiku 4.5). The token detector's own limits (length bias, no expiry) are the reason the judge exists and are not repaired here. Nothing from this program is offered for the body unless its label's validation bar passes (§6), and even then only by the author's decision with the numbers in hand.

**2h. Expiry is judged.** The detector cannot score the 15 expiry obligations; the judge can, because its reference for an expiry obligation is the event as the old value and "date passed" as what is true now, the rule `build_hv1.practice_candidates` used for the practice set. Expiry rows enter the per-policy tables and P-L1, P-L1b, P-L4 and P-L2; they are excluded from P-L3 and P-L3b, whose split (an untagged active copy of the stale value in view) is defined by `amend4_header.view_source` for supersession and retraction only.

---

## §3. Task A: GPT-5.6 Luna as the answerer

- **Views**: the 305 of §2c, byte-identical to the recorded ones (`ds_downstream/run/cell_ds.json` and Amendment 2's LOOKUP-LIT additions through `amend4_header.jobs`, and `views_amend5.json`'s 74 changed views); their sha256 over (view sha, view text) is `AUX-R130-LOCK`'s `build_views_sha256` and is asserted before every call.
- **Prompt**: the E.10 answer stage's, unchanged: `prompts_ds.SYSTEM_ANSWER` (section D.4, digest as `AUX-DS-PROMPT`) and `amend4_header.USER_ANSWER_A4` (the D.4 user text with the Amendment 4 header binding "User" to the persona's name and pinning the date; sha256 asserted equal to `AUX-DS-A4-LOCK`). Persona name and date from `amend4_header.persona_fields`.
- **Lane**: `gpt-5.6-luna` through raw Chat Completions as E5 (`r82_counterfactual/tools/cf2_openai.py`): `seed` 42, `response_format` `json_object`, temperature unset (rejected by the model), `max_completion_tokens` 2048, reasoning effort unset (§2g); one draw; eight workers; the served identifier asserted on every row (E1.7 rule); the answer read from the last JSON object of the reply (`run_cf.last_json`, the Haiku lane's rule) with one retry on a parse failure; a row whose retry also fails is `ELICITATION_FAILED` and gets no judge unit. Rows `ds_downstream/run/rows_ds_r130_luna.jsonl`, keyed `item id | view sha256` as every answer-stage rows file, each carrying the view sha, the policies the view serves, the source (`a4` or `a5`), tokens, reasoning tokens, cost and the raw reply.
- **Not done**: no mini or Haiku answer is regenerated; no PRESENT or ABSENT item is answered; no other policy's view is built.

---

## §4. Task B: the semantic judge

- **Model and settings**: `claude-opus-5` through Message Batches, **temperature 0**, `max_tokens` 300, one request per unit, the label read from the last JSON object of the reply; a unit whose reply carries no label from the five is re-asked once synchronously (full price) and, failing that, is `PARSE_FAIL` and counted, never guessed.
- **Units**: one per recorded answer of GPT-4.1 mini and Claude Haiku 4.5 on the 305 views (**610**) and one per Luna row with an answer (up to **305**): up to **915**. The 20 retag pairs whose re-answer returned byte-identical text are two units each, as they are two rows for the human (an intra-judge consistency reading, descriptive).
- **What the judge sees**: the question, the old value (no longer true), what is true now, the answer, in the HV-A workbook's four columns and wording (`build_hv1.py`: `stale_field` / `gold_field` of `run_ds.records` for supersession and retraction; the event and "date passed" for expiry). **It never sees** the policy, the answerer, the view, the detector's score or flag, the before / after condition, or any identifier. The build asserts, for all 248 HV-A key items, that the strings the judge is given equal the strings the human saw (`r130_common.lock_against_hv1_key`; a mismatch is a STOP).
- **Labels**: exactly the human sheet's: ASSERTS, MENTIONS, CLEAN, ABSTAINS, UNSURE, with the README's definitions verbatim. **UNSURE counts as not ASSERTS and not MENTIONS in every primary reading; the sensitivity row drops every unit labelled UNSURE from every pairing it enters** (ruling 5). The README's MENTIONS definition, on which P-L4 rests, reads verbatim: "MENTIONS: the old value appears, but the answer says it is in the past, changed or cancelled, or explains why it no longer holds." — the answer refers to the old value as cancelled, replaced or past (ruling 8's sense; "explains why it no longer holds" is that same reading, not a broader one).
- **The prompt, frozen here** (the tool `r130_common.py` holds the same two strings and asserts them against these fenced blocks before any judge call; `{question}`, `{stale}`, `{gold}`, `{answer}` are the four fields):

`JUDGE_SYSTEM`:
```
You label an answer that an assistant wrote to a question a user asked about themselves. Each item has the question, an old value that is no longer true, the value that is true now, and the answer. Pick exactly one label:
- ASSERTS: the answer treats the old value as true now. Example: the user cancelled a trip, and the answer tells them what to pack for it.
- MENTIONS: the old value appears, but the answer says it is in the past, changed or cancelled, or explains why it no longer holds. Example: "You used to prefer tea, and now you prefer coffee."
- CLEAN: the old value does not appear at all, and the answer does answer the question.
- ABSTAINS: the answer refuses, says it does not know, or gives nothing usable. Example: "I don't have enough information about that."
- UNSURE: you really cannot decide. Use this rarely and say why in the reason.
Judge only what the answer says. Do not judge whether the answer is polite, complete or well written.

Return JSON only, the reason first: {"reason": "<one sentence>", "label": "<ASSERTS or MENTIONS or CLEAN or ABSTAINS or UNSURE>"}
```

`JUDGE_USER`:
```
Question: {question}
Old value (no longer true): {stale}
True now: {gold}
Answer: {answer}
```

- **Order**: the judge prompt is frozen with this file; the judge's probe (one synchronous call on a recorded mini answer) and its Batch run only after `FREEZE_R130.md` records this file's sha256 and after the Luna rows exist, so that one Batch judges all three answerers' answers under one prompt at one time. No Luna answer is judged before the freeze.

---

## §5. Task C: predictions, populations, statistics

A judged answer is **ASSERTS** iff the judge's label is ASSERTS, **MENTIONS** iff MENTIONS (primary reading; UNSURE is neither). Rates are over judged answers. Paired differences: the exact McNemar test (two-sided binomial on the discordant pairs) and the item-level and persona-grouped percentile bootstraps of the paired difference (10,000 draws, seed 42, the paper's convention; `amend4_header.boot_paired`'s construction). **A difference is reliable only if the exact McNemar p is below 0.05 and the persona-grouped interval excludes zero.** Direction and both intervals are reported whatever they are. A prediction is **HELD** iff the difference is in the predicted direction and reliable; **FAILED** otherwise, printed with the qualifier "direction as predicted, not reliable", "no difference" or "direction against"; **NOT EVALUABLE** if its population is empty or unjudged. Primary predictions: P-L1, P-L4, P-L2, P-L3. Secondary: P-L1b, P-L3b. Sensitivity row for all six: UNSURE units dropped.

- **P-L1 (the answerer link), primary.** Population: the **82** obligations answered under the oracle fetch whose forbidding record is in view and tagged (`stage1.json` `ORACLE.tagged_reach`; all three states: 63 supersession, 8 retraction, 11 expiry; 26 personas). On the oracle view of each, Luna's answer against GPT-4.1 mini's, paired by obligation. Prediction: Luna's ASSERTS rate is below mini's. Reason recorded (ruling 7): the answerer link is about what an answerer does with the record in view, so the largest population with the tagged record in view is the right one. Beside, descriptive: Haiku against Luna, and mini against Haiku, on the same 82.
- **P-L1b, secondary.** The lookup-rule version: the **61** obligations answered under the lookup rule with the tagged forbidding record in view (50 supersession, 2 retraction, 9 expiry; 24 personas), on the lookup view; 34 of the 61 share their view with the oracle view. Same prediction, same readings beside.
- **P-L4 (the safe form), primary.** On the P-L1 pairs (the 82 oracle views), Luna's MENTIONS rate is above mini's, paired by obligation. Beside, descriptive: Haiku against Luna, and mini against Haiku.
- **P-L2 (reach helps a strong answerer), primary.** Population: the **40** obligations answered under both top-five retrieval and the lookup rule (§2d; 24 concordant by construction, 16 informative; expected to be underpowered). Within Luna, the lookup-rule answer against the top-five answer, paired by obligation. Prediction: the ASSERTS rate under the lookup rule is below the rate under top-five retrieval. Beside, descriptive: the same for mini and Haiku; and the "of 104" reading for all three answerers.
- **P-L3 (the copies still bind), primary.** Population: the audited scorable oracle views (`reviews/downstream_audit/step4b_view_lines.json`, 89 supersession and retraction obligations) that the oracle fetch answered, **85**, split by whether the view holds an active line asserting the stale value (`amend4_header.view_source` = `active`, asserted equal to the audit's `any_active_stale`): **35** with (21 supersession, 14 retraction), **50** without (42, 8); 24 personas. Two groups, not pairs: Fisher's exact test in place of McNemar, the item-level and persona-grouped bootstraps of the rate difference (both groups resampled; personas resampled over the union). Prediction: Luna's ASSERTS rate with an active copy is above its rate without. Beside, descriptive: the same for mini and Haiku; and the reading with the fatima_q06 tag corrected on paper (R129 A2: that view moves to the "without" group; 34 with, 51 without).
- **P-L3b, secondary.** The lookup-rule version: the **58** supersession and retraction obligations answered under the lookup rule, **17** with an active copy in the lookup view, **41** without (the 12 expiry obligations excluded; 21 personas); the corrected reading is unchanged (fatima_q06 FULL is not answered under the lookup rule). Same prediction, same readings beside.
- **Descriptive, no bar**: the per-policy label table for the three answerers (ASSERTS, MENTIONS, CLEAN, ABSTAINS, UNSURE counts; the ASSERTS rate with its Wilson interval; MENTIONS plus CLEAN as the share of the non-abstaining answers, and of all judged answers; ABSTAINS per policy; the split by state); the retag variant for all three answerers (the 74 changed views, before against after, paired by view, McNemar and both bootstraps, ASSERTS and MENTIONS); the committed detector's flag at 0.50 beside each row (recorded for mini and Haiku, computed on Luna's answers here; descriptive only, the length bias stands); the judge's label on the 20 byte-identical retag pairs (same label on both or not).

**Size, settled here.** Five points of rate on 89 obligations is 4.45 answers; on P-L1's 82 it is 4.1. Under the exact McNemar test the smallest two-sided p with d discordant pairs all in one direction is 2 × 0.5^d: 0.125 at d = 4, 0.0625 at d = 5, 0.0312 at d = 6. So a net difference of four answers cannot be reliable even if every discordant pair points the same way; the smallest reliable difference is six discordant pairs against none (7.3 points on 82, about seven on 89, ten on P-L1b's 61), and any opposing pair raises it (7 against 1 gives p = 0.070; 8 against 1 gives 0.039; 10 against 2 gives 0.039). The same floor governs P-L4 on the 82. On P-L2's 16 informative pairs the floor is six of the sixteen one way and none the other. For P-L3 (Fisher, 35 against 50): 10/35 against 4/50 gives p = 0.017, 9/35 against 4/50 gives 0.034, 9/35 against 5/50 gives 0.076, 8/35 against 4/50 gives 0.065; for P-L3b (17 against 41): 6/17 against 4/41 gives 0.050, 6/17 against 3/41 gives 0.014, 5/17 against 4/41 gives 0.106. **A five-point difference will not be reliable at any of these sizes; direction and interval are reported whatever they are, and an unreliable difference is not a finding.**

---

## §6. Validation of the judge against the human labels (registered before the labels are read)

- **When**: after the hv1 session has validated and committed annotator A1's released label file, `human_validation/hv1/results/labels_A1.json` (written by `validate_hv1.py check A1`). This program reads that file **from git only** (`git show <commit>:path`, default HEAD), never from the working tree and never a workbook, and never before hv1's own commit; `r130_validate.py` refuses otherwise. A2's labels are not used.
- **Rows**: the 198 primary rows of HV-A (148 on the 74 changed views before and after, 50 controls), all GPT-4.1 mini answers, matched to the judge's units through the key lock of §4 (row uid → unit id). Rows A1 left blank are counted and excluded.
- **Report**, judge against A1 (A1 the reference): raw agreement on the five-way label; Cohen's kappa (unweighted) on the four-way label over the rows where neither gave UNSURE, with the number excluded (HV-A's §5.3 rule), and the five-way kappa beside; the 5 × 5 confusion matrix (A1 rows, judge columns); precision and recall of **ASSERTS** and of **MENTIONS** with Wilson intervals (CLEAN and ABSTAINS beside, descriptive). **Beside, the token detector's same numbers**: its flag at 0.50 (`flag_gold` of the HV1 key, `stale_use_tau_gold`) read as a binary ASSERTS label: precision, recall, raw agreement and kappa on the binary against A1. Sensitivity row: the rows where either A1 or the judge gave UNSURE dropped. Split rows: the 148 alone, the 50 controls alone, and the Haiku block where A1 labelled it (descriptive).
- **Bars, per prediction (ruling 10)**: **ASSERTS precision and recall both at or above 0.80** on the labelled primary rows validates P-L1, P-L1b, P-L2, P-L3 and P-L3b; **MENTIONS precision and recall both at or above 0.80** validates P-L4. A prediction whose label misses its bar is reported as **unvalidated**, and nothing resting on that label is offered for the body. If the labels are not released before this program's report, the report says "labels not yet released" and the validation is appended when they are, without any other number changing.

---

## §7. Budget, order, STOP conditions

- **Projection** from the probes before any lane runs: one Luna call on a recorded view (served identifier, tokens, reasoning tokens) scaled by each view's characters; one synchronous judge call on a recorded mini answer scaled by each unit's characters, at the Batch rate. The runner refuses a lane whose projection times 1.3 plus the metered spend exceeds its cap. Pre-registered estimate from the R125 rows (Luna about $0.0005 a call at 1,600 input tokens; Opus 5 about $0.008 a Batch unit at 2,000 input tokens): Luna 305 calls about $0.20; the judge 915 units about $2.5 at Batch; both far inside the caps.
- **Order**: freeze (this file's sha256 into `FREEZE_R130.md`, committed with the tools and the build) → `r130_run.py lock` → `probe-luna` → `probe-judge` → `project` → `run-luna` → `build-judge` → `project` again on the actual units → `submit-judge` → `poll-judge` (→ `retry-judge` if needed) → `r130_score.py` → `REPORT_R130.md` → STOP. Validation (`r130_validate.py`) after hv1's commit.
- **STOP**: the registration sha256 not matching the freeze; an input digest not matching (§11); the build counts not reproducing (305 / 231 / 74 / 610; P-L1 82, P-L1b 61, P-L2 40 with 24 same-view, P-L3 35 / 50 of 85 answered of 89 audited, P-L3b 17 / 41; the key lock 248); the HV1 key lock failing on any item; the served identifier differing on the probe or on any row; a projection over a cap; failures after the retry on more than 2% of a lane; any call before the freeze commit exists.
- **Credit**. Neither API exposes a balance to the keys in use (probed by R125 on 2026-09-20). The month's token-metered spend is reported at the freeze in place of a balance, with this program's projection beside it; if the author knows the remaining credit cannot cover both lanes, the program stops before the probes.

---

## §8. Outputs and ledger keys

`reviews/r130/build/build_r130.json` (the views, the recorded units, the census, the populations, the key lock), `build/judge_units_r130.json`; `ds_downstream/run/{lock,probes,projection}_r130.json`, `run/rows_ds_r130_luna.jsonl`, `run/batch_r130_judge.json`, `run/rows_ds_r130_judge.jsonl`; `reviews/r130/results/r130_scores.json`, `results/R130_TABLES.md`, `results/r130_validation.json`, `results/R130_VALIDATION.md`; `reviews/r130/REPORT_R130.md`. Ledger: `ds_downstream/NUMBERS_DS.md` section 16 with `AUX-R130-POP`, `-POLICY-TABLE`, `-PL1`, `-PL1B`, `-PL4`, `-PL2`, `-PL3`, `-PL3B`, `-RETAG`, `-SPEND`, `-VALIDATION`. No held text; the author decides with the numbers in hand whether anything earns a sentence.

## §9. Deviations pre-declared

Recorded in `reviews/r130/DEVIATIONS_R130.md` with dates: a Luna row failing after the retry (the unit is dropped from every pairing it enters; the count printed); a judge unit failing after the retry (the same); the labels not released before the report (§6); A1 leaving rows blank (§6); a ruling under §2a. Anything else is a deviation and is written down before scoring.

## §10. Dates

Freeze and probes 20 Sep 2026; Luna and the judge Batch 20–21 Sep; scoring and the report 21 Sep, before the experiment freeze that night; validation when hv1 commits A1's labels (expected 22 Sep).

## §11. Inputs pinned (sha256 of the working bytes; asserted by every tool at start)

| file | sha256 (16) |
|---|---|
| `ds_downstream/run/rows_ds_amend4_mini.jsonl` (untracked; HV1's pin) | `9ddc9f2638b6a297` |
| `ds_downstream/run/rows_ds_amend4_h45.jsonl` (untracked; HV1's pin) | `2f26e9332c7594cd` |
| `ds_downstream/run/rows_ds_amend5_mini.jsonl` | `fdfa2ca33a33df2b` |
| `ds_downstream/run/rows_ds_amend5_h45.jsonl` | `ee05348247656bf5` |
| `ds_downstream/run/rows_ds_amend5_merged_mini.jsonl`, `_h45.jsonl` (HV1's pins) | `b96ddcb2c52256e6`, `4d34ad8f53c51a1e` |
| `ds_downstream/run/scores_amend4.json`, `scores_amend5.json` (HV1's pins) | `a28a58595d8de7f4`, `64cfb720d5a8dee1` |
| `ds_downstream/run/views_amend5.json` (HV1's pin) | `db120fef3cb452d1` |
| `ds_downstream/run/cell_ds.json`, `ds_downstream/stage1.json`, `ds_downstream/views.json` | `e46d7b95da2a4e53`, `6691654d3dfd2359`, `6d3cb6c7b863c481` |
| `human_validation/hv1/key/key_hv1.json` (read for the string lock and the detector's flag only; never sent anywhere) | `e8ea5bc1e38365a8` |
| `human_validation/hv1/inputs/hva_rows.json` | `f0ba8ec949b14b08` |

## Registration mechanics

Frozen by sha256 over the bytes above the marker line, recorded in `reviews/r130/FREEZE_R130.md` with the freeze commit's hash before any call. Amendments and rulings, if any, are appended as dated sections below the marker and never edit the text above.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
