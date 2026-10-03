# NUMBERS_HV1.md -- the R119 ledger (human validation, HV-A and HV-B)

Every number this program prints resolves to a key here. Registration of record: `human_validation/hv1/REGISTRATION_HV1.md`, registered-text sha256 `34d6fa098661f1ee991639dc532e89731116f1bd688fcb4db362098c7b06e0d5`, frozen at `4f10aa2`. Zero model calls.

## AUX-HV1-REG, AUX-HV1-INPUTS (Phase 2, build)

Registered-text sha256 `34d6fa098661f1ee991639dc532e89731116f1bd688fcb4db362098c7b06e0d5`, frozen at `4f10aa2` (2026-09-19), asserted by `build_hv1.py` at start. Records commit of the three Amendment 4 files: `bf1dafb`. Inputs as pinned in registration section 12, digests found (working bytes; LF-normalised where they differ):

- `ds_downstream/run/rows_ds_amend4_mini.jsonl`: `9ddc9f2638b6a297` (LF `36e80b0fd6975c64`)
- `ds_downstream/run/rows_ds_amend5_merged_mini.jsonl`: `b96ddcb2c52256e6`
- `ds_downstream/run/rows_ds_amend4_h45.jsonl`: `2f26e9332c7594cd` (LF `330abc63433dfb67`)
- `ds_downstream/run/rows_ds_amend5_merged_h45.jsonl`: `4d34ad8f53c51a1e`
- `ds_downstream/run/scores_amend4.json`: `a28a58595d8de7f4`
- `ds_downstream/run/scores_amend5.json`: `64cfb720d5a8dee1`
- `ds_downstream/run/views_amend5.json`: `db120fef3cb452d1`
- `r82_counterfactual/cf2/cf_cell.json`: `b0a42c1e0b996019`
- `r82_counterfactual/cf2/cf_pairs_cf2.json`: `460eb05f19b229f5`
- `r82_counterfactual/cf2/cf_pn_texts_cf2.json`: `b605ec6b62ee26f7`
- `r82_counterfactual/cf2/cf_questions_cf2.json`: `d81d59ab1e927bdf`
- `r82_counterfactual/cf2/cf_indexes.json`: `09c897b8703dd5ff`
- `r82_counterfactual/cf_cell.json`: `496b66ca149b7816`
- `r82_counterfactual/cf_pairs.json`: `576a43c1e2fbbee8`
- `r82_counterfactual/cf_pn_texts.json`: `e135d62d1918455a`
- `r82_counterfactual/cf_questions.json`: `c4c2f249be657403`
- `registrations/ADDENDUM_RESP.md`: `ad4a90ebfe36d943`
- `registrations/ADDENDUM_DS_AMENDMENT_7.md`: `6fa6155ae965af15`
- `LifeMemEval/artifacts/lifecycle_banks/*.json`: `319dd64a018cabf0`

Frozen extract `human_validation/hv1/inputs/hva_rows.json` sha256 `f0ba8ec949b14b08a8077d5317711670ab65d3d24f45f73e9271b71e1dbbfb1d` (904 rows).

## AUX-HV1-POP-A, AUX-HV1-CONTROLS, AUX-HV1-POP-A2 (Phase 2, build)

**POP-A**: the 74 changed scorable views (registration 3.1): by state {'sup': 45, 'ret': 29}, 35 obligations, 14 personas; 148 answers; detector flags at 0.50: 37 before, 8 after, 45 flagged answers; identical-text twins 20. The keys are in `key/key_hv1.json` (`hva.population.changed_keys`).

**CONTROLS**: 50 unflagged answers from the 138 unchanged scorable views, seed 11901, round robin in Table 4 order; turns {'ALWAYS': 9, 'MODEL': 9, 'LOOKUP': 8, 'MODEL-ALL': 8, 'LOOKUP-LIT': 8, 'ORACLE': 8}; views drawn serving each policy {'ALWAYS': 12, 'MODEL': 27, 'LOOKUP': 26, 'MODEL-ALL': 12, 'LOOKUP-LIT': 31, 'ORACLE': 17}; abstentions among them 15. Primary rows 198.

**POP-A2** (optional block): Haiku 4.5 flagged answers on the 74 views, 38 before + 12 after = 50 rows.

Spacing redraws k (registration 2): {'A1': {'primary': 550, 'haiku': 371}, 'A2': {'primary': 767, 'haiku': 96}}.

## AUX-HV1-POP-B, AUX-HV1-DISTRACTORS (Phase 2, build)

Governing text: the registration as frozen (no Amendment 1). Eligible pairs by state {'SUPERSESSION': 79, 'RETRACTION': 15, 'EXPIRY': 18}; excluded: more than ten slot records {'EXPIRY': 5, 'RETRACTION': 15, 'SUPERSESSION': 9}, expiry event inside the 14-day window {'EXPIRY': 7}. Drawn 15 per state, seed 11904: 45 triples, 135 versions; every version re-derived with cf2_build_cell's construction and asserted equal to `cf_cell.json`'s label and pn_members and to `cf_indexes.json`'s v2 text. Presentation order and the within-triple orders are in `key/key_hv1.json` (`hvb.triples`).

**DISTRACTORS**: six per pair from the same category under other slot keys, present in all three versions, outside the own-name neighbourhood (tau 0.503637); records dropped as neighbours over the 45 pools: 134; pools under six: [('cf2:fatima:health_care:physiotherapy', 5)].

## AUX-HV1-PRACTICE (Phase 2, build)

Ten answers (8 GPT-4.1 mini expiry, 2 Haiku 4.5) with key labels {'CLEAN': 4, 'ABSTAINS': 4, 'MENTIONS': 1, 'ASSERTS': 1}; replacements under the missing-label rule: [('H45|frbank:fatima:fatima_q02:SLOT-ABLATED|340491d8ab96d14d', 'MINI|frbank:marcus:marcus_q10:FULL|7b437d1259c5ea12', 'ASSERTS')]. Five CF-1 store versions (['PRESENT', 'PN', 'ABSENT', 'PRESENT', 'PN']) from the 12 of the 23 CF-1 pairs free of CF-2 that pass the slot rule. Key labels are the builder's read; the practice set is discarded and never scored.

## AUX-HV1-WORKBOOK-A1, AUX-HV1-WORKBOOK-A2, AUX-HV1-KEY (Phase 2, build; recorded before anything is sent)

- `human_validation/hv1/workbooks/blank/HV1_A1.xlsx` sha256 `7a1fc974eecb3cbf05561784a62edaa80d48c9de7c6bba7ab4774c1eb8bb6843` (README sha256 `1df7437a9aef2e69`)
- `human_validation/hv1/workbooks/blank/HV1_A2.xlsx` sha256 `50f1aa50876adacb827c8243c686ac9ca57b6dc3662c7976426419b99759e8e1` (README sha256 `18192591dff41c45`)
- `human_validation/hv1/key/key_hv1.json` sha256 `e8ea5bc1e38365a8b433ac801f0b1aafe7c809a78236b5d7a6aeb3602fd0f1c8` (never sent).

## AUX-HV1-LEAKSCAN (Phase 2)

`tools/leakscan_hv1.py` over every cell of both blank workbooks ({'A1': 2070, 'A2': 1345}): **PASS**; hard fails 0; content-column occurrences listed for review 48 (by word: meta:after x25, meta:before x17, version:PRESENT x2, version:PN x2, plain:literal x2, decimal:0.67 x2, version:ABSENT x1, decimal:0.45 x1). Output `human_validation/hv1/results/leakscan_hv1.txt`.

First pass (same tool, before its 'literal' rule was narrowed) reported two hard hits: the plain English word "literal" inside two memory-note texts of A1's TRIPLES tab (E21, E22), not the policy's name. The rule now matches the policy's name ("literal lookup", "literal rule") and lists the plain word for review; no cell changed between the passes (the workbook digests above are the same bytes).
