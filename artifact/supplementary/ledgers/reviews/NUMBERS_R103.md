# NUMBERS_R103.md — printed forms and deterministic values of the v10-to-v11 pass (R103, 2026-09-13)

Purpose. Two kinds of entry, on the R86/R87/R97/R102 precedent (`tools/trace_scan_v13.py` LEDGERS). (A) Rounded forms: the pass rounds body prose to two decimals (rule 2.3 of the author's pass) and its abstract prints an integer percent; each printed form is recorded against the four-decimal (or one-decimal percent) key it rounds (Decimal, ROUND_HALF_UP). (B) Deterministic values computed in this pass with no model call, from recorded rows only, each labelled exploratory in the manuscript: the attribute-naming split of the counterfactual set (W3), the census of the 22 unflagged forbidding records (W6/Q1), precision and recall of the rescaled coverage score at the base rate (Q5), and the persona span of the counterfactual questions (W11). The two model-call runs of this pass have their own ledgers: `q4_inversion_probe/NUMBERS_Q4.md` and `ds_downstream/NUMBERS_DS.md` section 6; their rounded forms are in (A) with those keys.

## A. Rounded forms (printed | source | key or table | v11 site)

| printed | source | key / table | v11 site |
|---|---|---|---|
| 42% | 42.3% | NUMBERS_E1R.md / NUMBERS_SIDE.md, the frozen S2 sentence (v10 Section 7) | abstract, 7, 10 |
| 0.75 | 0.7484 | NUMBERS_E1R.md AUX-E1R-NB6 (Table 3 header, v11) | 10 (the box) |
| 0.73 | 0.7339 | NUMBERS.md NOK FR-Bank indexed (Table 4, v11) | 10 (the box) |
| 0.59 | 0.5858 | NUMBERS_E1R.md AUX-E1R-NB6 BELIEVED lookup (Table 22, appendix) | 10 (the box) |
| 0.60 | 0.5959 | NUMBERS_E1R.md AUX-E1R-BELIEVED-NOK monitor (Table 22, appendix) | 10 (the box) |
| 0.88 | 0.8756 | NUMBERS_CF2.md AUX-CF2-ALLSTATES-V3 (Table 1, v11) | 10 (the box) |
| +0.08, 0.08 | +0.0817 | NUMBERS_E1R.md AUX-E1R-BASELINES (Table 22, appendix) | 10 (the box) |
| 0.03 | 0.0348 | NUMBERS_SIDE.md AUX-SIDE-S2-CAP-RECALL precision, capped | 7 |
| 0.04 | 0.0357 | NUMBERS_SIDE.md AUX-SIDE-S2-CAP-RECALL precision, lifted | 7 |
| +0.06, 0.06 | +0.0554 | NUMBERS_SIDE.md AUX-SIDE-S2-MINI lifted minus capped (Appendix F.9) | 7 |
| +0.00, 0.00 | +0.0015 | NUMBERS_R74.md counts jittered, FR-Bank FOK (Table 17, appendix) | 6 |
| 0.78 | 0.7805 | NUMBERS_DS.md AUX-DS-REACH MODEL on the 41 (the frozen DS paragraph) | 8 (the lead-in; the DS result sentence) |
| 0.85 | 0.8537 | NUMBERS_DS.md AUX-DS-A1-P4DESC MODEL-ALL-V3 on the 41 | 8 |
| +0.07, 0.07 | +0.0732 | NUMBERS_DS.md AUX-DS-A1-P4DESC difference | 8 |
| 0.54 | 0.5353 and 0.5355 | NUMBERS_Q4.md AUX-Q4-M0, AUX-Q4-AM (Table 21, appendix) | 7 |
| +0.08, 0.08 | +0.0829 | NUMBERS_Q4.md AUX-Q4-AM D1 | 7 |
| +0.06, 0.06 | +0.0577 | NUMBERS_Q4.md AUX-Q4-M0 D1 | 7 |
| 0.18 | 0.1791 | this file, AUX-R103-PR precision | 10 (the box) |
| 0.69 | 0.6857 | this file, AUX-R103-PR recall | 10 (the box) |
| 0.87 | 0.8668 | this file, AUX-R103-FLAGSPLIT superseded-names lookup, unflagged whole | 5 |
| 0.84 | 0.8355 | this file, AUX-R103-FLAGSPLIT GPT-4.1 mini sup. only, unflagged whole | 5 |

Tokens the pass prints that already print in v10 in the same form and need no row here: 0.92, 0.88 (abstract; NUMBERS_R102.md), 0.50, 0.72, 0.77, 444, 0.83, 661, 54, 104, 5%, 60x, 42.3%, 101.4%, every count.

## B. Deterministic values (no model call; recorded rows only; exploratory)

### AUX-R103-FLAGSPLIT — the counterfactual set split by the author's question flag (W3)

Source `reviews/v11/flag_split.json` (`reviews/v11/tools/flag_split.py`; flags `r82_counterfactual/cf2/question_read_flags.json`, keyed by `pair_id`, 148 of 148 matched; lanes `cf2/rows/rows_{MINI,H45,OP5}.jsonl` through `score_cf.load_lane`; lookups through `score_cf.matcher`). Flagged (YES) 89 questions, n = 267, 89 positives; unflagged (NO) 59 questions, n = 177, 59 positives. Positives by state and flag: supersession 45 / 43, retraction 22 / 8, expiry 22 / 8. Mann-Whitney AUROC, ties 0.5; no interval.

| reader, summary | flagged whole | flagged sup / ret / exp | unflagged whole | unflagged sup / ret / exp |
|---|---:|---|---:|---|
| Superseded-names lookup (sup. only) | 0.7142 | 0.9047 / 0.5000 / 0.5000 | 0.8668 | 0.9789 / 0.5000 / 0.5000 |
| All-states lookup (all three) | 0.8232 | 0.8675 / 0.7583 / 0.8450 | 0.9718 | 0.9751 / 0.9102 / 1.0000 |
| GPT-4.1 mini, sup. only | 0.6539 | 0.7640 / 0.5000 / 0.5455 | 0.8355 | 0.9244 / 0.5859 / 0.5625 |
| GPT-4.1 mini, all three | 0.7315 | 0.7859 / 0.8605 / 0.5150 | 0.9125 | 0.9145 / 0.9492 / 0.8594 |
| Haiku 4.5, sup. only | 0.6887 | 0.8288 / 0.5527 / 0.5713 | 0.8532 | 0.9417 / 0.5273 / 0.6094 |
| Haiku 4.5, all three | 0.8091 | 0.8037 / 0.8673 / 0.7608 | 0.9631 | 0.9571 / 0.9922 / 0.9922 |
| Opus 5, sup. only | 0.7997 | 0.9217 / 0.5863 / 0.6245 | 0.9060 | 0.9593 / 0.5781 / 0.6055 |
| Opus 5, all three | 0.8690 | 0.9216 / 0.7686 / 0.8926 | 0.9619 | 0.9580 / 0.9688 / 1.0000 |

Reading, whichever way: every reader scores higher on the unflagged half; the naming boundary (named state high, counted states near chance under the superseded-only summary) holds on both halves.

### AUX-R103-UNFLAGGED — the 22 forbidding records the truthful metadata does not flag, by FR-Bank's own write-path fault (W6, Q1)

Source: `AUX-DS-FLAGCENSUS` (the 22 item ids) joined to the raw FR-Bank rows' `believed_superseded`, `believed_retracted`, `believed_supersedes` fields (`e1_metamemory/backend_entries/frbank.json` through `backends.load_backend`; the census script is recorded in `reviews/v11/REPORT.md`). For **17 of 22** at least one `pn_members` entry carries `believed_superseded = true` and none carries `believed_retracted` (14 retraction-derived, 3 expiry-derived): the retraction or expiry was recorded through the supersession mechanism, the Conflate row of `tab:believed`. For **5 of 22** no `pn_members` entry carries any believed flag (4 retraction-derived: `ingrid_q04` FULL / CAT-ABLATED / SLOT-ABLATED, `mirri_q04` CAT-ABLATED; 1 expiry-derived: `marcus_q10` CAT-ABLATED). No entry among the 22 carries `believed_retracted`. Ten distinct questions; the 5 no-mark items come from four of them.

### AUX-R103-PR — precision and recall of the rescaled coverage score at the base-rate threshold (Q5)

Source: the isotonic leave-one-persona-out map of `AUX-R82-CAL` (`r82_counterfactual/tools/calibrate_r82.py` `fit_isotonic` / `lopo_calibrate`) recomputed on the recorded `P-FOK-HARD/intact` rows (n = 588, 35 positives, base rate 0.0595); the recomputation reproduces the ledgered ECE 0.0146, maximum calibrated probability 0.375 and base-rate crossing 0.3. Predicted positive when the out-of-fold probability is at or above the base rate: **TP 24, FP 110, FN 11, TN 443**; flagged 134 of 588; **precision 24 / 134 = 0.1791; recall 24 / 35 = 0.6857**. (Platt map beside, not printed: TP 23, FP 110, precision 0.1729, recall 0.6571.)

### AUX-R103-MARGIN — model minus lookup on the same summary, whole populations, with intervals (the author's point 3, 2026-09-13)

Source `reviews/v11/margin_intervals.json` (`reviews/v11/tools/margin_intervals.py`): paired percentile bootstrap, 1,000 draws, seed 42, single-class draws discarded, item-level primary and persona-clustered beside (`common_e1r.boot_item` / `boot_cluster`); on the 661 mini's committed INDEXED-TRUE `nok` against NB-6's embedding score through `ds_common.lookup_scores` (reproduction gate 0.7484 / 0.6186 asserted); on the 444 each recorded arm against `score_cf.matcher` on the same summary. Computed after the fact on recorded rows; no model call; exploratory. Single-arm intervals on the 661 are persona-clustered (`boot_cluster_single`).

| population | model, summary | model | lookup | model − lookup | item-level CI | persona-clustered CI | point inside ±0.05 |
|---|---|---:|---:|---:|---|---|---|
| 661 | GPT-4.1 mini (committed), sup. only vs superseded-names lookup | 0.7339 [0.6502, 0.8186] | 0.7484 [0.6636, 0.8298] | −0.0145 | [−0.0769, +0.0549] | [−0.1080, +0.0765] | yes |
| 444 | GPT-4.1 mini, sup. only vs superseded-names lookup | 0.7167 | 0.7663 | −0.0496 | [−0.1012, +0.0013] | [−0.0933, −0.0054] | yes |
| 444 | GPT-4.1 mini, all three vs all-states lookup | 0.7967 | 0.8756 | −0.0789 | [−0.1229, −0.0344] | [−0.1283, −0.0334] | no |
| 444 | Haiku 4.5, sup. only vs superseded-names lookup | 0.7566 | 0.7663 | −0.0098 | [−0.0640, +0.0398] | [−0.0494, +0.0336] | yes |
| 444 | Haiku 4.5, all three vs all-states lookup | 0.8773 | 0.8756 | +0.0017 | [−0.0326, +0.0361] | [−0.0312, +0.0320] | yes |
| 444 | Opus 5, sup. only vs superseded-names lookup | 0.8405 | 0.7663 | +0.0742 | [+0.0315, +0.1203] | [+0.0414, +0.1126] | no |
| 444 | Opus 5, all three vs all-states lookup | 0.9079 | 0.8756 | +0.0323 | [+0.0060, +0.0617] | [+0.0077, +0.0608] | yes |

Rounded forms printed in the body (Section 5): −0.05 ← −0.0496; [−0.10, +0.00] ← [−0.1012, +0.0013]; [−0.09, −0.01] ← [−0.0933, −0.0054]; −0.01 ← −0.0145; [−0.08, +0.05] ← [−0.0769, +0.0549]; +0.00 ← +0.0017; +0.03 ← +0.0323. Further rounded forms of this pass: 0.82 ← 0.8199 and 0.86 ← 0.8588 (indexed NOK band, Table 5 / Appendix B); +0.15 ← +0.1528 and +0.45 ← +0.4511 (cross-model NOK gains, Appendix B); 0.83 ← 0.8308, 0.53 ← 0.5283, 0.55 ← 0.5489 (GPT-4.1 mini per state, Appendix D.2).

### AUX-R103-PERSONAS — the persona span of the counterfactual questions (W11)

Source `r82_counterfactual/cf2/cf_cell.json`: the 148 questions span **40 of the 40** personas (every persona contributes at least one pair; cap of four per persona per state, ADDENDUM_CF2 §3).
