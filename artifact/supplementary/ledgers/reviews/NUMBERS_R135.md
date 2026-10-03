# NUMBERS_R135.md: the R135 pass (the last content pass on v23; 2026-09-21)

Written by `reviews/v23/tools/ledger_r135.py` from the checks of `reviews/v23/tools/r135_number_gate.py`; every value is read from the artifact named (`reviews/r125/results/r125_matched.json`, `r125_t4_sibling.json`, `r125_t5_nc.json`; `r82_counterfactual/cf2/results/cf_scores_cf2.json`, `cf_scores_nc.json`; `cf2_paraphrase/results/para_scores.json`, `para_minus_lookup_posthoc.json`; `reviews/r122/results/enc_lookup.json`; `pad_probe/results/pad_scores.json`, `contam_scores.json`; `ds_downstream/run/lock_amend8.json`; the E1R, R74 and BELIEVED_H ledgers). Printed forms are half-up on the four-decimal recorded value at two decimals (the convention of reviews/NUMBERS_R131.md), magnitudes with the direction in words. The table tab:robust is written by `reviews/v23/tools/robust_tex.py` (`reviews/v23/src/robust_table.tex`; `reviews/v23/results/robust_printed.json`).

## AUX-R135-ROBUST: the rows of tab:robust as built, each with its metric, population, status and source

| row | what we tried to break | what it removes | what happened (as printed) | metric | population | status | source |
|---|---|---|---|---|---|---|---|
| 1 | One question, three store versions | Question-wording leakage | A question-only reader scores $0.50$ by construction | pooled | the counterfactual set | by construction | one score per question reused across its three versions (Table 1's caption; AUX-CF2-MINI-V2 'blind 0.5000 by identity') |
| 2 | Random tokens for the names | Name meaning, length kept | $0.65$; the real lookup is $0.13$ higher | matched | the counterfactual set | post hoc | r125_matched.json readers/RANDTOK_v2/pn_vs_present/whole/matched; paired/contrasts 'random-token minus name lookup (v2)' (AUX-CF2-R125-MATCHED-V2, -CONTRASTS) |
| 3 | Sibling-name control | List length and counts | Lookup $0.95$, models $0.88$ to $0.97$, none reliably above the lookup | matched, the PN version against its sibling | the 88 supersession pairs | registered | r125_t4_sibling.json readers/*/pn_vs_sibling/matched; predictions P-SB4 HELD (AUX-CF2-R125-SB-*) |
| 4 | Lifecycle totals permuted | The summary's two totals | No model moves by more than $0.01$, none reliably | pooled | the counterfactual set | registered | cf_scores_cf2.json lanes/*/equiv_v2r_minus_v2 (AUX-CF2-EQUIV-V2R: mini +0.0011, Haiku 4.5 +0.0072, Opus 5 -0.0052; P5 held) |
| 5 | Count moved to a sibling version | Where the count sits | Luna, Sol, Opus fall $0.28$ to $0.33$; mini, Haiku no reliable change | matched | the counterfactual set, the 60 counted-state pairs | post hoc | r125_matched.json paired/contrasts 'moved count {Opus k5, Luna k5, Sol k5} minus sup-only k5' counted (AUX-CF2-R125-CONTRASTS); mini and Haiku counted, intervals include zero |
| 6 | Every count deleted | The counts | Mini and Haiku within $0.01$; Luna loses $0.06$, Opus $0.04$ | pooled | the counterfactual set | registered | cf_scores_nc.json readers/*/arms/INDEXED-NAMES/vs_v2 (AUX-CF2-NC-MINI-NAMES -0.0064, -H45-NAMES -0.0059; P-N1 held); r125_t5_nc.json readers/{Luna five draws, Opus draw 1}/names_only/minus_intact (AUX-CF2-R125-NC-*) |
| 7 | Questions reworded, no shared word | Word overlap with names | Word lookup at $0.50$; embedding lookup loses $0.02$; mini, Haiku lose more | pooled | the 115 reworded pairs | registered | para_scores.json lookups/lex_v2/paraphrase 0.5000, lookups/emb_v2/paired -0.0216, models/MINI/v2/paired -0.0326, models/H45/v2/paired -0.0642 (AUX-PARA-LOOKUP-LEX-V2, -EMB-V2, -MINI-V2, -H45-V2) |
| 8 | Two other sentence encoders | The choice of encoder | Both within $0.01$ of the lookup | pooled | the counterfactual set | registered | enc_lookup.json predictions/P-E1/encoders/{MPNET -0.0059, BGE -0.0080}/delta (AUX-R122-ENC-*; P-E1 held) |
| 9 | Padding to 60; wrong names injected | Short, clean lists | $0.67$ padded; $0.67$/$0.60$ with wrong names, mini and Haiku falling with it, within $0.02$ of the lookup | pooled | the full obligation set (padding); the counterfactual set (injection) | registered | pad_scores.json readers/emb/60/auroc 0.6696 (AUX-PAD-LOOKUP-EMB); contam_scores.json readers/emb/{C0.232 0.6740, C0.40 0.6001}/auroc and readers/{MINI,H45}/*/model_minus_emb (AUX-PAD-C-LOOKUP-EMB, -C-MINI, -C-H45: within 0.02, intervals including zero) |
| 10 | The store's own metadata (FR-Bank) | The ground-truth summary | Mini, Haiku, lookup: $0.73$, $0.82$, $0.75$ to $0.60$, $0.71$, $0.59$ | pooled | the full obligation set | registered | NUMBERS_E1R.md section 11 R-NOK-FRB TRUE / BELIEVED (AUX-E1R-TRUE-NOK, -BELIEVED-NOK, -NB6); NUMBERS_R74.md AUX-R74-X4-H45-NOK; NUMBERS_BELIEVED_H.md AUX-BH-H45-15 |

## AUX-R135-PRINTED: every number and claim the pass's new texts print, beside its source

37 checks, 0 mismatches (`r135_number_gate.py`, this pass's own; R134's 62 run first, unchanged).

| where (the sentence) | printed | recorded value | reliable, claimed / actual | source |
|---|---|---|---|---|
| tab:robust row 1: a question-only reader scores 0.50 by construction | 0.50 | +0.5000 |  | NUMBERS_CF2.md AUX-CF2-MINI-V2 'blind 0.5000 by identity' (one score per question across its three versions) |
| tab:robust row 2: the random-token lookup 0.65 (matched) | 0.65 | +0.6453 |  | r125_matched.json readers/RANDTOK_v2/pn_vs_present/whole/matched (post hoc) |
| tab:robust row 2: 'the real lookup is 0.13 higher' (matched, reliable) | 0.13 | -0.1318 | True / True | r125_matched.json contrasts 'random-token minus name lookup (v2)' whole -0.1318 |
| tab:robust row 3 / abstract: the lookup 0.95 against its sibling (matched; the 88 supersession pairs) | 0.95 | +0.9489 |  | r125_t4_sibling.json readers/Name lookup/pn_vs_sibling/matched (AUX-CF2-R125-SB-*) |
| tab:robust row 3 / abstract: models 0.88 (the floor; Haiku 4.5) | 0.88 | +0.8807 |  | r125_t4_sibling.json readers/*/pn_vs_sibling/matched, the minimum |
| tab:robust row 3: models to 0.97 (Opus 5) | 0.97 | +0.9716 |  | as above, the maximum |
| tab:robust row 3 / abstract: 'none reliably above the lookup' (P-SB4) | HELD | HELD |  | r125_t4_sibling.json predictions/P-SB4 reliably_above [] |
| tab:robust row 3: every reader, the lookup included, at 0.88 or higher against the sibling (the abstract's parenthetical, deleted by the G2 ruling; 0.88 moved to the row) | 0.88 | +0.8807 |  | r125_t4_sibling.json, the minimum over the lookup and the five models |
| tab:robust row 4: 'No model moves by more than 0.01' (totals permuted, pooled; the largest |delta|) | 0.01 | +0.0072 | False / False | cf_scores_cf2.json lanes/*/equiv_v2r_minus_v2 delta: mini +0.0011, Haiku +0.0072, Opus -0.0052 (AUX-CF2-EQUIV-V2R; P5 held) |
| tab:robust row 5: 'fall 0.28 to 0.33 on the counted states' (lower end; matched) | 0.28 | +0.2833 | True / True | r125_matched.json contrasts moved count {Opus -0.2833, Luna -0.2917, Sol -0.3250} counted (AUX-CF2-R125-CONTRASTS) |
| tab:robust row 5: upper end | 0.33 | +0.3250 |  | as above |
| tab:robust row 5 / 5.1: 'mini and Haiku show no reliable change' (counted states, matched) | not reliable | not reliable |  | r125_matched.json contrasts moved count mini +0.0167, Haiku -0.0500 counted |
| tab:robust row 6 / 5.1: 'Mini and Haiku within 0.01' with every count deleted (pooled) | within | within |  | cf_scores_nc.json readers/*/arms/INDEXED-NAMES/vs_v2 delta: mini -0.0064, Haiku -0.0059 (AUX-CF2-NC-*-NAMES; P-N1 held) |
| tab:robust row 6: 'Luna loses 0.06' (pooled, reliable) | 0.06 | -0.0598 | True / True | r125_t5_nc.json readers/GPT-5.6 Luna (five draws)/names_only/minus_intact -0.0598 (AUX-CF2-R125-NC-LUNA-NAMES) |
| tab:robust row 6 / 5.1: 'Opus 0.04' (pooled, reliable) | 0.04 | -0.0426 | True / True | r125_t5_nc.json readers/Opus 5 (draw 1)/names_only/minus_intact -0.0426 (AUX-CF2-R125-NC-OP5-NAMES) |
| tab:robust row 7: 'A word-matching lookup falls to 0.50' | 0.50 | +0.5000 |  | para_scores.json lookups/lex_v2/paraphrase (AUX-PARA-LOOKUP-LEX-V2) |
| tab:robust row 7 / 5.2 / abstract: 'the embedding lookup loses 0.02' | 0.02 | -0.0216 | False / False | para_scores.json lookups/emb_v2/paired -0.0216 (AUX-PARA-LOOKUP-EMB-V2) |
| tab:robust row 7 / 5.2: 'mini and Haiku lose more' (than the embedding lookup) | holds | holds |  | para_scores.json models/MINI/v2/paired -0.0326, models/H45/v2/paired -0.0642 against -0.0216 |
| tab:robust row 8: 'Both within 0.01 of the lookup' (encoders, pooled) | within | within |  | enc_lookup.json predictions/P-E1/encoders MPNET -0.0059, BGE -0.0080 (AUX-R122-ENC-*; P-E1 held) |
| tab:robust row 9: 'Padded, the lookup falls to 0.67' (60 names; the full obligation set) | 0.67 | +0.6696 |  | pad_scores.json readers/emb/60/auroc (AUX-PAD-LOOKUP-EMB) |
| tab:robust row 9: 'with wrong names it falls to 0.67' (c = 0.232; the counterfactual set) | 0.67 | +0.6740 |  | contam_scores.json readers/emb/INDEXED-V2-C0.232/auroc (AUX-PAD-C-LOOKUP-EMB) |
| tab:robust row 9: '... and 0.60' (c = 0.40) | 0.60 | +0.6001 |  | contam_scores.json readers/emb/INDEXED-V2-C0.40/auroc |
| tab:robust row 9: 'mini and Haiku fall with it, within 0.02 of it' (the largest model minus lookup on the injected lists; intervals include zero) | within | within |  | contam_scores.json readers/{MINI,H45}/*/model_minus_emb, largest |delta| 0.0192 (AUX-PAD-C-MINI, -C-H45) |
| tab:robust row 10 / abstract: mini, ground truth | 0.73 | +0.7339 |  | AUX-E1R-TRUE-NOK |
| tab:robust row 10 / abstract: Haiku, ground truth | 0.82 | +0.8210 |  | AUX-R74-X4-H45-NOK |
| tab:robust row 10 / abstract: the lookup, ground truth | 0.75 | +0.7484 |  | AUX-E1R-NB6 |
| tab:robust row 10 / abstract: mini, FR-Bank's metadata | 0.60 | +0.5959 |  | AUX-E1R-BELIEVED-NOK |
| tab:robust row 10 / abstract: Haiku, FR-Bank's metadata | 0.71 | +0.7069 |  | AUX-BH-H45-15 |
| tab:robust row 10 / abstract: the lookup, FR-Bank's metadata | 0.59 | +0.5858 |  | AUX-E1R-NB6 BELIEVED |
| builders box: 'under FR-Bank's store-written summary, where Haiku sits 0.12 above the lookup' | 0.12 | +0.1212 | True / True | NUMBERS_BELIEVED_H.md AUX-BH-H45-15 'Haiku minus lookup' +0.1212 ([+0.0628, +0.1849]; [+0.0317, +0.2107]): reliable, both intervals above zero |
| abstract: 'one stronger model edges 0.04 ahead' (Luna, the named state, reworded, pooled) | 0.04 | +0.0445 | True / True | para_minus_lookup_posthoc.json LUNA v2 superseded pooled paraphrase (AUX-PARA-POSTHOC-MINUS-LOOKUP-LUNA-V2) |
| 5.1: 'given the counts alone, they fall by 0.14' (mini; matched, counts only minus names only) | 0.14 | +0.1351 | True / True | r125_matched.json contrasts 'E2 mini counts-only minus names-only' whole -0.1351 |
| 5.1: 'given the counts alone, they fall by 0.14' (Haiku; matched, counts only minus names only) | 0.14 | +0.1385 | True / True | r125_matched.json contrasts 'E2 Haiku counts-only minus names-only' whole -0.1385 |
| Section 7: 'changes 1 of 452 assembled views under the reference tags' | 1 / 452 | 1 / 452 |  | lock_amend8.json census/gt/primary (AUX-DS-A8-RULE-CENSUS) |
| Section 7: 'the same rule changes 90 views' (own tags, primary) | 90 | 90 |  | lock_amend8.json census/own/primary changed |
| Section 7: 'fully tags 15 of the 35 duplicate views' | 15 / 35 | 15 / 35 |  | lock_amend8.json dup35/own/primary (AUX-DS-A8-DUP35) |
| Section 7: 'propagates falsely (69 of 2,333 licensed active lines)' | 69 / 2333 | 69 / 2333 |  | lock_amend8.json false_propagation/own/primary (AUX-DS-A8-FALSEPROP; share 0.0296) |

