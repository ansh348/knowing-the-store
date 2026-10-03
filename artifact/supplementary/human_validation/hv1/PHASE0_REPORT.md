# PHASE0_REPORT — program R119 (human validation, HV-A and HV-B): the inventory of 2026-09-19

Read-only inventory reported to the author on 2026-09-19 (morning) and accepted with rulings the same day; reproduced here at Phase 2 as the registration (section 0) says. **One correction to the report as delivered is marked below (section 4b): the count "8 pairs with more than ten slot records" was a truncated printout; the count is 29.** The registration carries the corrected figure (its section 1b).

Program number: R117 (experiments) and R118 (the v21 lineage) were taken; **R119** was free in every tracked file and in `reviews/`, `registrations/`. Ledger keys `AUX-HV1-*` in `human_validation/hv1/NUMBERS_HV1.md`; a claims block held at `human_validation/hv1/claims_r119_block.md` (CLAIMS.md is off-limits to this program). `human_validation/hv1/` did not exist. Another session had files staged in the shared index; every commit of this program uses a private `GIT_INDEX_FILE` and an explicit pathspec.

## 1. What already existed

No top-level `human_validation/`. Seven `…/knowing_the_store/human_validation/` directories are release-package copies (under `submission/iclr2027_release/` and `analysis/no_new_annotation_v1/`) whose README says "Packaging provides instruments; it does not provide completed human validation." Canonical originals, every label cell empty (0 of 200 rows in the v16 sheet, 0 of 19 in the addendum):

| artifact | path | note |
|---|---|---|
| Detector sheet (100 answers, Q1–Q4, YES/NO, two annotator columns) | `reviews/v12/DETECTOR_LABELING_SHEET.md`; key `reviews/v12/detector_sample_key.json`; sample `detector_sample.json`; built by `reviews/v12/tools/phase1.py::item9` (seed 42, strata policy × tag) | R104; from the original DS run (`rows_ds.jsonl`, `rows_ds_amend1.jsonl`), pre-header, pre-retag |
| Second-annotator sheet (A: 50 PN checks; B: 50 cancellable-plan reads; C: the same 100 answers) | `reviews/v16/SECOND_ANNOTATOR_SHEET.md`; key `reviews/v16/second_annotator_key.json`; scorer `reviews/v16/tools/second_annotator_agreement.py` | R108 |
| Addendum: the 19 oracle answers the audit read as stale (11 mini, 8 Haiku) | `reviews/v17/SECOND_ANNOTATOR_SHEET_ADDENDUM.md`; key `reviews/v17/second_annotator_addendum_key.json` | R109; Q3/Q4 with a third option |
| Synthetic dry run ("numbers meaningless") | `reviews/v18/results/annotator_dryrun.json` | R110 |
| Completion-v1 leftovers | `analysis/submission_completion_v1/human/`: byte-identical copies of the above plus `PARAPHRASE_READ.md`, `sheet_a2.md` (622 rows), `answer_packets_blank.json`, `source_review_blank.json`, `REVIEW_SPEC.md`, `tasks.json`, `coordinator_manifest.json` | 17 Sep; "No human label was filled" |
| 16 Sep review-response pass, part C | `review2_cc_prompt.md` §C: the brief's ancestor (cells "89 scorable obligation views under the gated fetch … 178 answers", rubric ASSERTS/MENTIONS/CLEAN, P-C1..P-C3); `reviews/integration/COMPLETED_EXPERIMENTS.md:99` "Review-2 C … not started" | mock review `reviews/v19/REVIEW_2_v18.md` W1 + Q1 |

No existing workbook matched the scope (Markdown sheets, a four-question YES/NO rubric, a 100-answer pre-retag sample, no gold audit). Reusable pieces: the agreement code in `second_annotator_agreement.py`, the stale/successor rendering and stratified sampler in `phase1.py::item9`, the leak-screen pattern in `r82_counterfactual/tools/cf2_leakscreen.py`.

## 2. "The second annotator's fourth question" (Table 50)

Table 50 = `\label{tab:ds-a7}` (`paper_v19.aux`, `paper_v21.aux`; `appendix_v19.tex:1405`), the DS Amendment 7 composite. "Agreement with the second annotator's fourth question is reported once the sheet is labeled" refers to Q4 of Section C of `reviews/v16/SECOND_ANNOTATOR_SHEET.md` (verbatim from the v12 sheet): "(Q4, obligation items only) does the answer correctly report the obligation, that is, that the stale content is superseded, retracted or expired and is not to be used, whether by saying so or by declining to answer from it?" Registered comparison: `registrations/ADDENDUM_DS_AMENDMENT_7.md` (the closed-word-list reported-detector against the Q4 column; ledger key `AUX-DS-A7-Q4`, a dash until labeled). HV-A's rubric has no Q4 equivalent; HV-A does not discharge that sentence (registration 5.4).

## 3. Exact paths for the inputs

- Items (661; 104 obligations = 63 sup / 26 ret / 15 exp): `ds_downstream/tools/ds_common.py::load_cell()`. Stale / current value per item: `ds_downstream/tools/run_ds.py::records()` → `stale_field`, `gold_field`, `section`.
- Before retag (GPT-4.1 mini, header prompt, Amendment 4): `ds_downstream/run/rows_ds_amend4_mini.jsonl` (452 rows; 231 PN views, 212 sup/ret over 85 obligations). After retag (Amendment 5): `ds_downstream/run/rows_ds_amend5_merged_mini.jsonl` (`source` = "amend5 call (changed view)" on 74). Haiku 4.5: the `_h45` files. Detector scores: `scores_amend4.json`, `scores_amend5.json` → `per_row.{MINI,H45}[key]` (`stale_use_tau_gold` = the 0.50 flag, `stale_cov`, `stale_use` = 0.80); code `run_ds.py::score_answer`.
- Counterfactual set (CF-2): `r82_counterfactual/cf2/cf_cell.json` (444 = 148 × 3; 88 sup / 30 ret / 30 exp; `label`, `pn_members`, `question`, `intent`), `cf_pairs_cf2.json` (entry_id, slot_key, `t_now`, `cutoff`), `cf_pn_texts_cf2.json`, `cf_questions_cf2.json`. Per-version stores are not serialized; `cf_indexes.json` holds the v2/v3/v2r summaries only. Records per version are deterministic from `LifeMemEval/artifacts/lifecycle_banks/{persona}.json` via `r82_counterfactual/tools/cf2_build_cell.py`. CF-1 (`r82_counterfactual/cf_cell.json`, 30 pairs) for the practice set.

## 4. Discrepancies raised for the ruling

**4a. "89 scorable obligation views under the gated fetch" does not exist in the data.** GPT-4.1 mini, sup+ret only, flag at 0.50, Amendment 4 → 5:

| candidate population | views | flagged before → after | re-answered by the retag | text identical before/after |
|---|---:|---:|---:|---:|
| Model rule (the gated fetch) | 62 | 10 → 1 | 20 | 45 of 62 |
| Oracle | 85 | 17 → 2 | 35 | 62 of 85 |
| all scorable views, any policy | 212 | 37 → 8 | 74 | 158 of 212 |
| the 74 views the retag changed (AUX-DS-A5-CHANGED-MINI) | 74 | 37 → 8 | 74 | 20 of 74 |

The paper's 89 = 63 + 26 scorable obligations of the 104; 85 are reached by any policy; four retraction obligations reach no answered view (`bruna_q06:CAT-ABLATED`, `fatima_q06:SLOT-ABLATED`, `joonho_q04:FULL`, `mirri_q04:CAT-ABLATED`); one expiry obligation (`marcus_q10:CAT-ABLATED`) also reaches none. Table 4's "89" is MODEL-ALL's reach. MODEL ∪ LOOKUP ∪ LOOKUP-LIT also has 89 distinct views (recorded as unexplained, not as the source). Recommendation, ruled in: the 74 changed views × {before, after} = 148, plus unflagged controls from the 138 unchanged scorable views (ruled 50, not 20).

**4b. HV-B display makes the label countable.** 99 of 148 pairs have exactly one record on the target slot, so the plain display renders as 0 / 1 / 2 records. Ruled: six seeded same-category distractors outside the own-name neighbourhood. **As delivered, this section also said "8 pairs have >10 slot records (max 210)"; the distribution had been truncated at twelve bins when printed. The count is 29 (9 sup, 15 ret, 5 exp).** With that and the 14-day-window exclusion, the eligible pairs are 79 / 15 / 18, and the registration fixes HV-B at 15 per state (its section 1b), which the author accepted on 19 Sep with no Amendment 1.

**4c. Expiry items in HV-A.** Unscorable for the detector (the paper's first disclosed limit). Ruled: excluded from HV-A; used in the practice set; HV-B keeps its expiry triples.

**4d. Q4 / Table 50.** Ruled: HV-A does not discharge `AUX-DS-A7-Q4`; a $0 descriptive substitute (reported-detector against "MENTIONS or ABSTAINS") is reported as a substitute population; the paper's wording of the unrun comparison is ruled in the main session.

## 5. Rulings received (19 Sep) and where they landed

R119 and `AUX-HV1-*` approved. (a) primary 74 × 2 = 148, controls 50 (six Table 4 policies), optional Haiku block of the flagged answers on the 74 → registration §3. (b) six distractors, own-name neighbourhood, slot rule → §6. (c) expiry out of HV-A → §3, §8. (d) no Q4 discharge; substitute → §5.4. Practice: CF-1's free pairs, expiry answers plus a few Haiku answers → §8 (the free-pair count is 23 by the rule, not 14). After Phase 1: HV-B at 15 per state stands; the three Amendment 4 files committed as records (`bf1dafb`); the README additions accepted for showing at the Phase 2 stop.
