# NUMBERS_R134.md: the R134 pass (the paraphrase check landed in v23; 2026-09-21)

Written by `reviews/v23/tools/ledger_r134.py` from the checks of `reviews/v23/tools/r134_number_gate.py`; every value is read from the artifact named (`cf2_paraphrase/results/para_scores.json`, `para_scores_all124.json`, `lookups.json`, `para_minus_lookup_posthoc.json`, `cf2_paraphrase/sheet.json`, `para_questions.json`; the abstract's inherited numbers from `reviews/r125/results/r125_matched.json`, `r82_counterfactual/cf2/NUMBERS_CF2.md`, `e1r_robustness/NUMBERS_E1R.md`, `r74/NUMBERS_R74.md`, `believed_h/NUMBERS_BELIEVED_H.md`). Printed forms are half-up on the four-decimal recorded value at two decimals (the convention of reviews/NUMBERS_R131.md), magnitudes with the direction in words; the appendix prose prints the two genericity descriptives at three decimals and Luna's two lower bounds at three (the author's ruling). The four-decimal values of the six appendix tables (tab:para-pooled, -matched, -minus-lookup, -sup, -sens, -flags) are written by `cf2_paraphrase/tools/para_tex.py` and ledgered in `cf2_paraphrase/NUMBERS_PARA.md` (AUX-PARA-LOOKUP-*, AUX-PARA-{MINI,H45,OP5,LUNA,SOL}-V2/V3, AUX-PARA-MATCHED-*, AUX-PARA-POSTHOC-MINUS-LOOKUP-*, AUX-PARA-FLAGS, AUX-PARA-SENS-*, AUX-PARA-GENERIC).

## AUX-R134-PRINTED: every number and claim the pass's new texts print, beside its source

62 checks, 0 mismatches (`r134_number_gate.py`).

| where (the sentence) | printed | recorded value | reliable, claimed / actual | source |
|---|---|---|---|---|
| 5.2: '115 rewrites passed a word screen and an author's read' | 115 | 115 |  | para_scores.json n_pairs (sheet.json n_accepted 115 of 124 screen-passing; para_questions.json 124 accepted of 148) |
| 5.2 / abstract / Section 1: 'the embedding lookup loses 0.02, within tolerance' (whole set, superseded-names summary) | 0.02 | -0.0216 | False / False | lookups.json emb_v2 paired delta -0.0216 (AUX-PARA-LOOKUP-EMB-V2); within tolerance = |d| <= 0.05 |
| 5.2: the lookup's loss is within the registered tolerance | within | within |  | as above; the registered reading 'holds' |
| 5.2: 'A word-matching lookup falls to chance by construction' | 0.5000 | 0.5000 |  | lookups.json lex_v2 paraphrase (AUX-PARA-LOOKUP-LEX-V2) |
| 5.2: 'Rewording costs mini 0.03' (not reliable) | 0.03 | -0.0326 | False / False | para_scores.json MINI v2 paired delta -0.0326 (AUX-PARA-MINI-V2) |
| 5.2: 'Haiku a reliable 0.06' | 0.06 | -0.0642 | True / True | para_scores.json H45 v2 paired delta -0.0642 (AUX-PARA-H45-V2) |
| 5.2: 'Opus a reliable 0.03' | 0.03 | -0.0331 | True / True | para_scores.json OP5 v2 paired delta -0.0331 (AUX-PARA-OP5-V2; one draw against the recorded five) |
| 5.2: 'Luna ... do not move' (within tolerance, intervals include zero) | holds | holds |  | para_scores.json LUNA v2 paired delta -0.0034 (AUX-PARA-LUNA-V2; added, not registered) |
| 5.2: 'Sol ... do not move' (within tolerance, intervals include zero) | holds | holds |  | para_scores.json SOL v2 paired delta -0.0149 (AUX-PARA-SOL-V2; added, not registered) |
| 5.2: 'the lookup now sits a reliable 0.09 above mini' | 0.09 | -0.0904 | True / True | para_scores.json MINI v2 model_minus_emb -0.0904 (AUX-PARA-MINI-V2) |
| 5.2: 'the stronger models keep the lead they had' (Opus, Luna, Sol reliably above the lookup on the paraphrase set and on the original questions, whole set, pooled) | holds | holds |  | para_minus_lookup_posthoc.json models/{OP5,LUNA,SOL}/v2/whole/pooled: paraphrase +0.0630, +0.0945, +0.0891; original +0.0745, +0.0763, +0.0824 (AUX-PARA-POSTHOC-MINUS-LOOKUP-*) |
| 5.2 (Branch B): 'mini ... reliably below the lookup on the pooled metric (by 0.12' | 0.12 | -0.1195 | True / True | para_minus_lookup_posthoc.json MINI v2 superseded pooled paraphrase -0.1195 (AUX-PARA-POSTHOC-MINUS-LOOKUP-MINI-V2) |
| 5.2 (Branch B): 'Haiku ... reliably below ... and 0.07)' | 0.07 | -0.0743 | True / True | para_minus_lookup_posthoc.json H45 v2 superseded pooled paraphrase -0.0743 (AUX-PARA-POSTHOC-MINUS-LOOKUP-H45-V2) |
| 5.2 (Branch B): 'Opus ... do not differ from it' (intervals include zero) | not reliable | not reliable |  | para_minus_lookup_posthoc.json OP5 v2 superseded pooled paraphrase +0.0226 item [-0.0241,+0.0698] persona [-0.0357,+0.0806] |
| 5.2 (Branch B): 'Sol ... do not differ from it' (intervals include zero) | not reliable | not reliable |  | para_minus_lookup_posthoc.json SOL v2 superseded pooled paraphrase +0.0396 item [-0.0063,+0.0845] persona [-0.0176,+0.0929] |
| 5.2 (Branch B) / abstract / Conclusion: 'Luna ... edges above it by 0.04, reliable on the pooled metric' | 0.04 | +0.0445 | True / True | para_minus_lookup_posthoc.json LUNA v2 superseded pooled paraphrase +0.0445 item [+0.0093,+0.0845] persona [+0.0042,+0.0895] (AUX-PARA-POSTHOC-MINUS-LOOKUP-LUNA-V2) |
| ruling check: Luna's pooled intervals are [+0.009, +0.084] and [+0.004, +0.089] | [+0.009,+0.084] [+0.004,+0.089] | [+0.009,+0.084] [+0.004,+0.089] |  | as above |
| 5.2 (Branch B): Luna '... and not within triples' (matched interval includes zero) | not reliable | not reliable |  | para_minus_lookup_posthoc.json LUNA v2 superseded matched paraphrase +0.0395 triple [-0.0066,+0.0921] persona [-0.0071,+0.1053] |
| appendix (the ruling): Luna's matched difference prints 0.04 | 0.04 | +0.0395 |  | as above |
| appendix (the ruling): Luna's pooled lower bounds print 0.009 and 0.004 | 0.009 / 0.004 | 0.009 / 0.004 |  | as above |
| 5.2 (Branch B): 'On the original questions no model exceeded it' (supersession only, original questions, pooled: none reliably above) | holds | holds |  | para_minus_lookup_posthoc.json */v2/superseded/pooled/original: MINI -0.1044*, H45 -0.0304, OP5 +0.0136, LUNA +0.0255, SOL +0.0172 |
| appendix (the ruling): Luna is the only reader above the lookup on the named state, reworded (pooled) | holds | holds |  | as above, the paraphrase column |
| appendix (the ruling): Haiku's pooled and matched readings disagree on supersession | disagree | disagree |  | H45 v2 superseded pooled paraphrase -0.0743 reliable=True; matched -0.0526 reliable=False |
| appendix (the ruling): 'one of five comparisons' (five models on the named state) | 5 | 5 |  | para_minus_lookup_posthoc.json models with a v2 row |
| 5.2: 'Under the all-states summary the lookup loses 0.06 pooled, beyond tolerance' | 0.06 | -0.0559 | True / True | lookups.json emb_v3 paired delta -0.0559 (AUX-PARA-LOOKUP-EMB-V3) |
| 5.2: the all-states lookup's pooled loss is beyond the tolerance | beyond | beyond |  | as above; the registered reading 'collapses' |
| 5.2: '... and 0.02 within triples' (matched, not reliable) | 0.02 | -0.0174 | False / False | para_scores.json matched emb_v3 pn_vs_present paired whole -0.0174 triple [-0.0522,+0.0217] persona [-0.0572,+0.0192] (AUX-PARA-MATCHED-EMB_V3) |
| abstract: 'Each of 148 questions' | 148 | 148 |  | r125_matched.json readers/LOOKUP_v2/pn_vs_present/whole/n (the triples); para_questions.json 148 rows |
| abstract / Conclusion: 'the two smaller models fall below it' (mini and Haiku reliably below the lookup on the named state, reworded, pooled) | holds | holds |  | MINI and H45 v2 superseded pooled paraphrase, as above |
| abstract / Conclusion: 'one stronger model edges ahead by 0.04' | 0.04 | +0.0445 | True / True | LUNA v2 superseded pooled paraphrase, as above |
| abstract: 'lead over the lookup of 0.08 to 0.10' (lower end; matched, whole set) | 0.08 | +0.0811 | True / True | r125_matched.json paired/vs_lookup/{LUNA_v2 +0.1014, SOL_v2 +0.0811, OP5_v2 +0.0980}/pn_vs_present/whole (AUX-CF2-R125-VS-LOOKUP) |
| abstract: 'lead over the lookup of 0.08 to 0.10' (upper end) | 0.10 | +0.1014 |  | as above |
| abstract: '(0.05 to 0.06 remains)' (pooled; lower end) | 0.05 | +0.0540 | True / True | r82_counterfactual/cf2/NUMBERS_CF2.md AUX-CF2-HYB-VS-MODELS (Opus +0.0540, Luna +0.0553, Sol +0.0635) |
| abstract: '(0.05 to 0.06 remains)' (upper end) | 0.06 | +0.0635 |  | as above |
| abstract: 'one count feature added to the lookup closes it within a question's three store versions' (no stronger model reliably above the count-feature lookup, matched) | holds | holds |  | r125_matched.json paired/contrasts 'Luna minus hybrid', 'Sol minus hybrid (P-H2)', 'Opus minus hybrid' |
| abstract: mini 0.73 under the ground-truth summary | 0.73 | +0.7339 |  | e1r_robustness/NUMBERS_E1R.md section 11 R-NOK-FRB TRUE, monitor (AUX-E1R-TRUE-NOK) |
| abstract: mini 0.60 under FR-Bank's capped store-written summary | 0.60 | +0.5959 |  | e1r_robustness/NUMBERS_E1R.md section 11 R-NOK-FRB BELIEVED, monitor (AUX-E1R-BELIEVED-NOK) |
| abstract: the lookup 0.75 under the ground-truth summary | 0.75 | +0.7484 |  | e1r_robustness/NUMBERS_E1R.md section 11 R-NOK-FRB TRUE, NB-6 (AUX-E1R-NB6) |
| abstract: the lookup 0.59 under the capped store-written summary | 0.59 | +0.5858 |  | e1r_robustness/NUMBERS_E1R.md section 11 R-NOK-FRB BELIEVED, NB-6 (AUX-E1R-NB6) |
| abstract: Haiku 0.82 under the ground-truth summary (n = 661) | 0.82 | +0.8210 |  | r74/NUMBERS_R74.md AUX-R74-X4-H45-NOK (n = 661) |
| abstract: Haiku 0.71 under FR-Bank's capped store-written summary | 0.71 | +0.7069 |  | believed_h/NUMBERS_BELIEVED_H.md section 5 AUX-BH-H45-15 |
| Limitations: 'covers 115 of the 148 questions' | 115 / 148 | 115 / 148 |  | para_scores.json n_pairs; para_questions.json rows |
| Limitations: 'Opus ran it with one draw' | 1 | 1 |  | para_scores.json OP5 k_new (k_recorded 5) |
| appendix: 148 questions; 24 failed the screen at drafting; 124 read; 9 excluded; 115 accepted | 148 / 24 / 124 / 9 / 115 | 148 / 24 / 124 / 9 / 115 |  | para_questions.json rows and accepted; sheet.json n_rows, n_excluded_by_author, n_accepted (AUX-PARA-DRAFT, AUX-PARA-SHEET) |
| appendix / tab:setup: supersession 76, retraction 17, expiry 22 | 76 / 17 / 22 | 76 / 17 / 22 |  | sheet.json by_state (AUX-PARA-SHEET) |
| appendix / tab:setup: 345 items | 345 | 345 |  | para_scores.json n |
| appendix: the registered floor was 120 | 120 | 120 |  | sheet.json floor_registered (the registration's STOP list); floor amended to 115 before any scoring call |
| appendix: the assistant's flags against the read: A 5 of 5, B 3 of 4, C 1 of 12, unflagged 0 of 103 | 5/5 3/4 1/12 0/103 | 5/5 3/4 1/12 0/103 |  | sheet.json rows (column 1) against the flag levels of reviews/para/PARA_AI_FLAGS.md (report_para.py FLAGS_A/B/C) |
| appendix: the attribute-naming split, 61 of 115 by the appendix's sentence and 32 of 115 by the token rule | 61 / 32 | 61 / 32 |  | para_scores.json flags (AUX-PARA-FLAGS both rules; AUX-PARA-SHEET column 2) |
| appendix: mean cosine to the target name 0.486 to 0.317 | 0.486 / 0.317 | 0.486 / 0.317 |  | para_scores.json extras.target_name_similarity (AUX-PARA-GENERIC) |
| appendix: content-token overlap 0.484 to 0.000 | 0.484 / 0.000 | 0.484 / 0.000 |  | as above |
| appendix / tab:setup: draws mini 1, Haiku 5, Opus 1 (recorded 5), Luna 5, Sol 5 | 1 5 1/5 5 5 | 1 5 1/5 5 5 |  | para_scores.json models/*/k_new, k_recorded |
| appendix: the branch readings under the v2 summary | A D | A D |  | para_scores.json branches/v2/headings (AUX-PARA-BRANCH-V2); status {'H45': 'collapses', 'MINI': 'holds', 'OP5': 'holds', 'emb': 'holds', 'lex': 'collapses'} |
| appendix: the branch readings under the v3 summary | C D | C D |  | para_scores.json branches/v3/headings (AUX-PARA-BRANCH-V3); status {'H45': 'collapses', 'MINI': 'collapses', 'OP5': 'holds', 'emb': 'collapses', 'lex': 'collapses'} |
| appendix: 'the picture is the same with the nine excluded pairs put back, slightly lower for every reader' (every paraphrase-set AUROC on the 124 at or below the 115's) | holds | holds |  | para_scores_all124.json against para_scores.json, every reader's paraphrase AUROC |
| appendix: the same headings on the 124 | A D | C D | A D | C D |  | para_scores_all124.json branches (sensitivity, not registered) |
| tab:registrations-c: the registered text's sha256 45cad63d and the whole file 2848f1ad | 45cad63d 2848f1ad | 45cad63d 2848f1ad |  | para_scores.json registration_sha256; sha256 of registrations/ADDENDUM_PARA.md (REPORT_PARA.md section 8) |
| 5.1: Opus 5's matched moved-count fall on the counted states (five against five draws) | 0.28 | -0.2833 | True / True | r125_matched.json paired/contrasts/.../pn_vs_present/counted -0.2833 (AUX-CF2-R125-CONTRASTS; tab:cf-matched-ablations) |
| 5.1: GPT-5.6 Luna's matched moved-count fall on the counted states (five against five draws) | 0.29 | -0.2917 | True / True | r125_matched.json paired/contrasts/.../pn_vs_present/counted -0.2917 (AUX-CF2-R125-CONTRASTS; tab:cf-matched-ablations) |
| 5.1: GPT-5.6 Sol's matched moved-count fall on the counted states (five against five draws) | 0.33 | -0.3250 | True / True | r125_matched.json paired/contrasts/.../pn_vs_present/counted -0.3250 (AUX-CF2-R125-CONTRASTS; tab:cf-matched-ablations) |
| 5.1: 'falling by 0.28 to 0.33 on the counted states' (lower end) | 0.28 | +0.2833 |  | the smallest of the three counted-states falls (Opus -0.2833); the R133 text's 0.27 was Luna's expiry value -0.2667, a per-state row |
| 5.1: 'falling by 0.28 to 0.33 on the counted states' (upper end) | 0.33 | +0.3250 |  | the largest of the three (Sol -0.3250) |

## AUX-R134-BRANCH: the branch of the brief's section 3 and the author's ruling

Supersession only, paraphrase set, superseded-names summary, pooled AUROC, model minus the embedding lookup (`para_minus_lookup_posthoc.json` `models/*/v2/superseded/pooled/paraphrase`; AUX-PARA-POSTHOC-MINUS-LOOKUP-*-V2): MINI -0.1195 [-0.1842,-0.0572] [-0.1959,-0.0512] *; H45 -0.0743 [-0.1371,-0.0202] [-0.1355,-0.0116] *; OP5 +0.0226 [-0.0241,+0.0698] [-0.0357,+0.0806]; LUNA +0.0445 [+0.0093,+0.0845] [+0.0042,+0.0895] *; SOL +0.0396 [-0.0063,+0.0845] [-0.0176,+0.0929]. Branch B (at least one model with both intervals excluding zero above the lookup): GPT-5.6 Luna, the reader added after the registration; the author's ruling of 2026-09-21 keeps Branch B by the pre-stated rule and words it in both directions. Pooled against matched on reliability: MINI agree; H45 DISAGREE; OP5 agree; LUNA DISAGREE; SOL agree.

