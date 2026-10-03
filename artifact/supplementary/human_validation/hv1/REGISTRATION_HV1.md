# REGISTRATION_HV1 — Knowing the Store: human validation of the stale-answer detector (HV-A) and audit of the counterfactual gold (HV-B)

Program **R119**. Written 2026-09-19 on the author's Phase 0 rulings of the same day (recorded in this session; the Phase 0 report is reproduced in `human_validation/hv1/PHASE0_REPORT.md` at Phase 2). Zero API spend: no model call is made anywhere in this program. Fenced to `human_validation/hv1/`; nothing in `reviews/v19/src/`, `reviews/v21/`, `reviews/r117/`, `CLAIMS.md` or any gate tool is touched. Every commit of this program uses a private git index (`GIT_INDEX_FILE`) and an explicit pathspec. This file is committed alone, before any workbook exists; its registered-text sha256 (the bytes above the marker line) is `AUX-HV1-REG` in `human_validation/hv1/NUMBERS_HV1.md`, and every script of the program asserts it at start.

Two studies share one workbook per annotator.

- **HV-A, detector validation.** Does the token detector that flags stale answers at the ground-truth join's threshold (0.50; `stale_use_tau_gold` of `ds_downstream/tools/run_ds.py::score_answer`) agree with a human?
- **HV-B, gold audit.** Do the constructed labels of the counterfactual set (CF-2, `r82_counterfactual/cf2/cf_cell.json`) agree with an independent human reading the stored records?

Annotators: **A1**, one non-author, primary for both studies. **A2**, an author, HV-A only, a reliability check. A1's identity appears only on the ATTESTATION tab of the returned workbook, which is never committed; the committed record carries the workbook's sha256 and the label columns only.

**Paper wording for the arrangement, fixed now:** "A non-author annotator labelled all items blind to policy, model and condition. An author labelled the same answers under the same blinding; we report the non-author's labels and their agreement."

---

## §1. Two corrections to the brief, recorded before anything is built

**1a. "The 89 scorable obligation views under the gated fetch" (review-2 part C, `review2_cc_prompt.md` §C1) does not exist in the data.** The paper's 89 is the count of scorable obligations, 63 supersession-derived plus 26 retraction-derived of the 104 (the 15 expiry-derived obligations are unscorable for the detector, the audit's first disclosed limit). Only **85** of the 89 are reached by any answered view under any policy; four retraction obligations reach none (`frbank:bruna:bruna_q06:CAT-ABLATED`, `frbank:fatima:fatima_q06:SLOT-ABLATED`, `frbank:joonho:joonho_q04:FULL`, `frbank:mirri:mirri_q04:CAT-ABLATED`). Under the gated fetch alone (the model rule) GPT-4.1 mini answers **62** scorable obligation views, of which the retag re-answered 20 and left 45 byte-identical. The population registered in §3 is therefore the retag's own: the 74 views the reference-assisted retag changed (`AUX-DS-A5-CHANGED-MINI`: 37 flagged before, 8 after, of 74), which contain every answer the detector flags before or after.

**1b. The Phase 0 count of "8 pairs with more than ten slot records" was wrong; the count is 29.** The Phase 0 distribution was truncated when printed. Over CF-2's 148 pairs, the records the base bank holds on the target slot (same scrubbed slot key, `e1_metamemory/tools/index_v2.py::scrub`) number more than ten for **29** pairs: 9 supersession, **15 retraction** (14 of them on the slot `project`, 1 on `family_member`; 24 to 210 records) and 5 expiry. A second exclusion (§6.1, the 14-day window) removes 7 expiry pairs. The eligible pairs are therefore **79 supersession, 15 retraction, 18 expiry**, and 20 per state is not attainable for retraction or expiry under the ruled exclusion. This registration draws **15 per state (45 triples, 135 store versions)**, the size the brief pre-declared as its fallback, so that every version is shown whole and no display rule differs between pairs. Retraction is then a census of its 15 eligible pairs, not a sample, and is described as such. The author may rule for another composition before any workbook leaves the repo; such a ruling is appended below the marker line as Amendment 1 and governs the draw, and `AUX-HV1-POP-B` records which text governed.

---

## §2. Blinding, common to both studies

Hidden from both annotators, in every tab: the policy, the model, the before/after condition, the detector's score and flag, the version name (PRESENT / ABSENT / PN), the constructed label, the persona key, the view, the item key, and every internal identifier. Rows carry only a running number. Names inside the question, answer and record texts are the synthetic personas' names and are the material being judged; they are not scrubbed. The hidden key (row number per workbook → item key, condition, policies, model, detector flag and score, constructed label) stays in `human_validation/hv1/key/` in the repo and is never sent.

Order: a seeded shuffle, a different seed for A1 (11902) and for A2 (11903). Constraint: the two answers of one view (before and after) sit at least ten rows apart. If a shuffle violates it, the shuffle is redrawn with seed + 1000·k for k = 1, 2, … until it holds; k is recorded. The optional block (§3.3) is shuffled separately (seeds 11907 for A1, 11908 for A2) under the same constraint.

---

## §3. HV-A population (GPT-4.1 mini; the six policies of Table 4 are Top-5 retrieval, Model rule, Lookup rule, Model rule all states, Literal lookup rule, Oracle)

Rows and scores: before = `ds_downstream/run/rows_ds_amend4_mini.jsonl` (the Amendment 4 header prompt) with `ds_downstream/run/scores_amend4.json` `per_row.MINI`; after = `ds_downstream/run/rows_ds_amend5_merged_mini.jsonl` with `scores_amend5.json` `per_row.MINI`. A view is a row key `item_id|view_sha`. Scorable = label PRESENT-NEGATIVE, state `sup` or `ret`. Flagged = `stale_use_tau_gold` true. Sha256s of every input are in §12.

**3.1 Primary block, 148 answers.** The **74** scorable views whose `source` in the Amendment 5 merged file reads "amend5 call (changed view)" (45 supersession, 29 retraction; 35 obligations; 14 personas), each with its before answer and its after answer. Twenty of the 74 pairs have byte-identical text before and after (the re-answer returned the same string); they stay in as an intra-rater check and are subject to the ten-row spacing like every pair. Detector flags inside the block: 37 before, 8 after, **45 flagged answers**; the 138 unchanged scorable views carry no flag before or after, so the block holds every flagged GPT-4.1 mini answer of the retag comparison.

**3.2 Controls, 50 answers.** Fifty unflagged answers from the 138 unchanged scorable views (before = after on these; the before row is shown), drawn with seed **11901** by round robin over the six Table 4 policies in the order Top-5 (ALWAYS), Model rule (MODEL), Lookup rule (LOOKUP), Model rule all states (MODEL-ALL), Literal lookup rule (LOOKUP-LIT), Oracle (ORACLE): the views serving each policy are sorted by key and shuffled under the seed; the policies are visited in turn and each turn takes one view not yet drawn that serves that policy, until 50 are drawn. A view serving several policies counts for each it serves; the five views serving only the lookup rule with all states (not a Table 4 row) cannot be drawn. The draw, the per-policy coverage and the abstention count are `AUX-HV1-CONTROLS`.

Primary total: **198 rows**, about two hours.

**3.3 Secondary block, optional, placed last: Haiku 4.5's flagged answers on the same 74 views.** Before (`rows_ds_amend4_h45.jsonl`, `scores_amend4.json` `per_row.H45`): 38 flagged; after (`rows_ds_amend5_merged_h45.jsonl`, `scores_amend5.json` `per_row.H45`): 12 flagged; **50 answers**, all flagged. This block serves detector precision on the second answerer only. It may be left unlabelled, in whole or in part, without affecting the primary analysis; whatever is labelled is scored, and the count labelled is reported.

**3.4 What a row shows.** The question; the old value, marked as no longer true (`stale_field` of `run_ds.py::records`); what is true now (`gold_field`: the successor value for supersession, the manifest's retraction statement for retraction); the answer text. Nothing else.

---

## §4. HV-A rubric (one label per row, from a dropdown)

- **ASSERTS**: the answer presents the old value as true now, or acts on it.
- **MENTIONS**: the old value appears, and the answer marks it as past, changed, cancelled or expired, or explains why it no longer holds.
- **CLEAN**: the old value does not appear, and the answer does answer the question.
- **ABSTAINS**: the answer declines, says it does not know, or gives no usable answer (separated from CLEAN so that a fall in stale answers cannot be an increase in refusals; review-2 W1).
- **UNSURE**: cannot decide; the notes column says why. Primary analysis counts UNSURE as not ASSERTS and not ABSTAINS; sensitivity rows count it as ASSERTS.

The annotator guide is the README tab, pasted from the brief as is (§9.1).

---

## §5. HV-A statistics and predictions (A1's labels are the reference; A2's enter only §5.3 and one sensitivity row)

Every count below is over the primary block unless said otherwise. Rates are per 74 views. Intervals are Wilson 95%.

- **P-C1, precision.** Of the 45 flagged answers, the share A1 labels ASSERTS is **at least 0.50** (≥ 23 of 45). Printed with its interval; also split before (37) / after (8), descriptive.
- **P-C2, the retag effect under human labels.** Let b = the number of the 74 before answers A1 labels ASSERTS and a = the number of the 74 after answers so labelled. P-C2 holds iff **2·a < b**. If b = 0 the prediction is unscorable (there is no rate to halve) and prints so. Beside it, descriptive: the paired difference (a − b)/74 with bootstrap intervals at item level and grouped by persona (10,000 draws, seed 42, the paper's convention).
- **P-C3, recall.** Of the answers A1 labels ASSERTS among the **198 primary rows**, the share the detector flagged is **at least 0.80**. If A1 labels no answer ASSERTS, unscorable, printed as such. Sensitivity: the same over the 148 alone (`AUX-HV1-RECALL-148`).
- **P-C4, abstentions.** Let b' and a' be the ABSTAINS counts among the 74 before and 74 after answers. P-C4 holds iff |a' − b'| ≤ 3 (3/74 = 0.041 ≤ 0.05; 4/74 = 0.054 > 0.05).

**5.1 Sensitivity rows.** (i) UNSURE counted as ASSERTS, P-C1 to P-C4 recomputed. (ii) A2's labels in place of A1's, P-C1 to P-C4 recomputed. Each row prints beside the primary; none changes a verdict.

**5.2 The secondary block.** Haiku 4.5 precision at 0.50: of the labelled flagged answers, the share ASSERTS, with its interval and the count labelled, split before / after (`AUX-HV1-HAIKU-PRECISION`). No prediction.

**5.3 Reliability.** Cohen's kappa (unweighted) between A1 and A2 on the four-way label over the rows where both gave a label other than UNSURE; the number of rows excluded, and the raw agreement, printed beside it. Computed on the 198 primary rows and, if both labelled it, on the secondary block separately. **No adjudication.** Disagreements are counted, not resolved.

**5.4 A descriptive substitute for the Table 50 sentence, not the registered comparison.** HV-A does **not** discharge `AUX-DS-A7-Q4` (the reported-detector's agreement with Q4 of the 100-answer second-annotator sheet, `reviews/v16/SECOND_ANNOTATOR_SHEET.md` Section C; `registrations/ADDENDUM_DS_AMENDMENT_7.md`), and the sentence in the paper that waits for it is not touched by this program; the author rules on its wording in the main session. As a $0 descriptive, on the 198 primary rows (all obligation items): the reported-detector of Amendment 7 (`ds_downstream/tools/amend7_reported.py::reports_obligation`: names a lifecycle state from the closed list and is not flagged at 0.50) against the derived human column "label is MENTIONS or ABSTAINS"; the 2×2 table, raw agreement and kappa, marked **substitute population** (`AUX-HV1-Q4-SUBSTITUTE`). It costs the annotators nothing.

---

## §6. HV-B population (CF-2; 45 triples, 135 store versions)

**6.1 Eligible pairs.** CF-2's 148 pairs (`r82_counterfactual/cf2/cf_pairs_cf2.json`) minus (i) the 29 whose target slot holds more than ten records in the base bank (§1b) and minus (ii) the 7 expiry pairs whose original event date lies inside the fourteen-day window [cutoff, t_now) of the persona join (`e0_metamemory/tools/e0_common.py`: `t_now` = newest active record + 24 h, `cutoff` = `t_now` − 14 days; expired iff event date < cutoff). On those 7 the constructed label reads PRESENT while a reader shown the date t_now would read the date as passed; excluding them keeps "today" unambiguous. Eligible: 79 supersession, 15 retraction, 18 expiry.

**6.2 The draw.** Fifteen pairs per state, seed **11904**: eligible pair ids sorted, shuffled under the seed within state, the first fifteen taken (retraction: all fifteen). Triples are presented in one seeded order (the same seed), the three versions of a triple adjacent, in a seeded order within the triple (seed 11906, fresh per triple), with no version name and no label.

**6.3 What a version shows.** The line "Today: <t_now date>"; the question (identical across the triple); and the records, shuffled together (seed 11906): the target slot's records as they stand in that version, plus **six distractors**. Each record prints as its text, then "recorded <created_at date>" and, where the record has one, "event date <event_time date>". No ids, no lifecycle flags, no confidence, no category name, no summary.

Version contents follow `r82_counterfactual/tools/cf2_build_cell.py` byte for byte: PRESENT = the base bank; ABSENT = the base bank minus every record on the target slot and the question's resolved gold records (`removedABS`); PN = the base bank plus the successor or retraction record (`cf2/cf_pn_texts_cf2.json`, `created_at` = the newest active record's) or, for expiry, the anchor record with its event date moved to cutoff − 30 days. The build recomputes the label of every rendered version with the same code and asserts it equals `cf_cell.json`'s; any mismatch is a STOP.

**6.4 Distractors.** For each pair, the pool is the base bank's records in the target's category that (a) are not in `removedABS`, so they are present in all three versions; (b) have a slot key; (c) have a scrubbed slot different from the target's; (d) are not in the target's encoder neighbourhood, reusing the own-name ablation's rule (`registrations/ADDENDUM_RESP.md` §C.2): cosine under `sentence-transformers/all-MiniLM-L6-v2` (local, offline; `e1r_robustness/tools/run_baselines.py::encoder`) between the two slot names with underscores replaced by spaces is **below τ = 0.503637**. Six are drawn with seed 11905, the same six for the three versions of the pair. If the pool holds fewer than six, all of it is used and the count is recorded (`AUX-HV1-DISTRACTORS`). The registration states the purpose: the annotator must find the records that bear on the question among records that do not, so that agreement measures reading and not counting.

**6.5 Labels.** A1 labels each version PRESENT, PN or ABSENT under the README's rule. A2 does not label HV-B.

---

## §7. HV-B statistic and prediction

Agreement of A1 with the constructed labels: per version (of 135) and per triple (all three right, of 45), each with its Wilson 95% interval; the 3×3 confusion table (constructed × A1); every disagreement printed verbatim (question, the records shown, constructed label, A1's label and note) in the appendix material. **P-B1: per-version agreement is at least 0.90 (≥ 122 of 135).** No label is changed after the fact; a disagreement is a finding about the label, the guide or the reader, and is reported as one.

If A1's time is short, HV-A comes first; HV-B is already at the brief's fallback size and does not shrink further. Any partial return is scored on the versions labelled and the count is reported.

---

## §8. Practice set (15 items; discarded, never scored)

Ten answers and five store versions from outside both populations, each with a key label and a one-line explanation written by the builder of the workbook (this session's read; not a validation). Both annotators do it first; A2 does the ten answers only.

- **Answers (10):** seven GPT-4.1 mini answers on expiry obligations (the 19 expiry PRESENT-NEGATIVE views of `rows_ds_amend4_mini.jsonl`, 17 distinct texts) and three Haiku 4.5 answers on unchanged scorable views not among the 50 control views, drawn with seed 11909; if a label of the four is missing among the ten, the last drawn items are replaced by the first seeded candidates carrying it, until every label appears at least once. Expiry items show the event as the old value and "date passed" as what is true now.
- **Store versions (5):** from the CF-1 pairs (`r82_counterfactual/cf_pairs.json`, 30 pairs) that share neither (persona, entry id) nor (persona, scrubbed slot) with any CF-2 pair — **23** pairs (the brief's "14" counted CF-2's reused adjudications, not pairs) — passing the same ≤ 10-record rule; five distinct pairs, versions assigned so the key reads two PRESENT, two PN, one ABSENT; the same display and distractor rule as §6.

---

## §9. Build, leak scan, hashes, return

**9.1 Workbooks.** One `.xlsx` per annotator, built by `human_validation/hv1/tools/build_hv1.py` from the key: tabs `README` (the brief's guide, pasted as is, plus one sentence in the TRIPLES paragraph, "Some notes will be about neighbouring topics; judge only the ones that bear on the question.", which the distractors of §6.4 require and which the author sees at the Phase 2 STOP), `PRACTICE` (with its key beside it), `ANSWERS`, `TRIPLES` (A1 only), `ATTESTATION` (name, date, time taken, what was confusing). Label cells are dropdowns (ASSERTS / MENTIONS / CLEAN / ABSTAINS / UNSURE; PRESENT / PN / ABSENT); `notes` is free text; every other cell is locked, and the key stores a sha256 of each locked cell's content.

**9.2 Leak scan.** Before anything is sent, `tools/leakscan_hv1.py` reads every cell of both blank workbooks. Hard fail on any occurrence, in any cell outside the four content columns (question, old value, true now, answer; and the records column of TRIPLES), of: a policy name (ALWAYS, MODEL, LOOKUP, MODEL-ALL, LOOKUP-ALL, LOOKUP-LIT, ORACLE, "top-5", "model rule", "lookup rule", "literal"), "retag", "oracle", "gated", "amend", "before", "after", "haiku", "gpt", "mini", "detector", a decimal in [0,1] with two places, a version name (PRESENT, ABSENT, PN, PRESENT-NEGATIVE, v2, v3, V2R), a constructed label, a persona key, an item key or view sha, a record id (`lb_`). Occurrences inside the content columns are listed for review and recorded (`AUX-HV1-LEAKSCAN`); a condition-revealing one there (a policy name, "retag", "oracle", "gated", a model name) is a hard fail. The scan's output is committed.

**9.3 Hashes before sending.** sha256 of each blank workbook and of the key file, recorded in `NUMBERS_HV1.md` (`AUX-HV1-WORKBOOK-A1`, `-A2`, `AUX-HV1-KEY`) and committed before either file leaves the machine. STOP and report.

**9.4 Return.** (1) A2 finishes first or in parallel; the sha256 of A2's returned workbook is committed (`AUX-HV1-RETURN-A2`) **before** A1's workbook is opened on this machine; then A1's (`AUX-HV1-RETURN-A1`). (2) `tools/validate_hv1.py` checks completeness (every label cell filled or explicitly blank, counted) and that no locked cell changed against the stored hashes; a changed locked cell is a STOP. (3) `tools/score_hv1.py` computes everything of §5 and §7 in **one run** and writes `results/scores_hv1.json` and the ledger keys; it is run once on the validated files. Labels are never edited after ingest.

**9.5 Output.** The appendix tables (HV-A: the prediction rows with intervals, the kappa row, the sensitivity rows, the Haiku row, the substitute row; HV-B: agreement rows, the confusion table, the disagreements verbatim) and the held paper sentences in both branches (predictions hold; predictions fail) for Section 9, the Table 4 footnote, the abstract's last clause, the Limitations sentence and the AI-use statement, written to `human_validation/hv1/HELD_TEXTS_HV1.md`. **Nothing lands in `reviews/v19/src/` or `reviews/v21/src/` without a ruling.** A claims block for the author to fold into CLAIMS.md is held at `human_validation/hv1/claims_r119_block.md`.

---

## §10. Deviations pre-declared

Recorded in `human_validation/hv1/DEVIATIONS_HV1.md` with dates: the secondary block unlabelled or partly labelled (§3.3); HV-B partly labelled (§7); A2 not returning (then §5.3 and sensitivity row (ii) print as dashes and the paper wording of the arrangement changes by ruling); a redraw of the shuffle for the spacing constraint (§2, the k); a distractor pool under six (§6.4); an author's ruling on the HV-B composition (§1b, Amendment 1). Anything else is a deviation and is written down before the workbook is sent, or, after sending, before scoring.

---

## §11. Dates

Registration committed 19 Sep 2026; workbooks built, scanned, hashed and sent 19 Sep (evening); labels back 22 Sep; scoring 22 Sep; integration ruling 23 Sep.

---

## §12. Inputs pinned (sha256, first 16 hex; the full digests are recomputed and asserted by every tool at start)

| file | sha256 (16) | tracked at freeze |
|---|---|---|
| `ds_downstream/run/rows_ds_amend4_mini.jsonl` | `9ddc9f2638b6a297` | **untracked** |
| `ds_downstream/run/rows_ds_amend5_merged_mini.jsonl` | `b96ddcb2c52256e6` | yes |
| `ds_downstream/run/rows_ds_amend4_h45.jsonl` | `2f26e9332c7594cd` | **untracked** |
| `ds_downstream/run/rows_ds_amend5_merged_h45.jsonl` | `4d34ad8f53c51a1e` | yes |
| `ds_downstream/run/scores_amend4.json` | `a28a58595d8de7f4` | **untracked** |
| `ds_downstream/run/scores_amend5.json` | `64cfb720d5a8dee1` | yes |
| `ds_downstream/run/views_amend5.json` | `db120fef3cb452d1` | yes |
| `r82_counterfactual/cf2/cf_cell.json` | `b0a42c1e0b996019` | yes |
| `r82_counterfactual/cf2/cf_pairs_cf2.json` | `460eb05f19b229f5` | yes |
| `r82_counterfactual/cf2/cf_pn_texts_cf2.json` | `b605ec6b62ee26f7` | yes |
| `r82_counterfactual/cf2/cf_questions_cf2.json` | `d81d59ab1e927bdf` | yes |
| `r82_counterfactual/cf_cell.json`, `cf_pairs.json`, `cf_pn_texts.json`, `cf_questions.json` (CF-1, practice) | `496b66ca149b7816`, `576a43c1e2fbbee8`, `e135d62d1918455a`, `c4c2f249be657403` | yes |
| `LifeMemEval/artifacts/lifecycle_banks/*.json` (40 files; sha256 over the sorted "name sha256" lines) | `319dd64a018cabf0` | yes |
| `registrations/ADDENDUM_RESP.md` (τ), `registrations/ADDENDUM_DS_AMENDMENT_7.md` (the word list) | `ad4a90ebfe36d943`, `6fa6155ae965af15` | yes |

The three untracked files hold the only copy of GPT-4.1 mini's and Haiku 4.5's **before** answers on the 74 changed views (the merged Amendment 5 files carry the after answers there). Phase 2 writes a frozen extract of the rows and per-row scores this program uses to `human_validation/hv1/inputs/hva_rows.json`, with the source digests above inside it, and commits it within the fence; committing the source files themselves is for the session that owns `ds_downstream/`.

## §13. Ledger keys (`human_validation/hv1/NUMBERS_HV1.md`)

`AUX-HV1-REG`, `-INPUTS`, `-POP-A` (the 74 keys; 148; the 45 flags), `-CONTROLS`, `-POP-A2` (the Haiku 50), `-POP-B` (the 45 triples and the governing text), `-DISTRACTORS`, `-PRACTICE`, `-WORKBOOK-A1`, `-WORKBOOK-A2`, `-KEY`, `-LEAKSCAN`, `-RETURN-A2`, `-RETURN-A1`, `-VALIDATE`, `-PC1`, `-PC2`, `-PC3`, `-PC4`, `-KAPPA`, `-SENS-UNSURE`, `-SENS-A2`, `-RECALL-148`, `-HAIKU-PRECISION`, `-Q4-SUBSTITUTE`, `-PB1`, `-PB-TRIPLE`, `-CONFUSION-B`, `-DISAGREE-B`, `-DEVIATIONS`.

## Registration mechanics

Frozen by sha256 over the bytes above the marker line, recorded as `AUX-HV1-REG` with the freeze commit's hash before any workbook is built. Amendments, if any, are appended as dated sections below the marker and never edit the text above.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
