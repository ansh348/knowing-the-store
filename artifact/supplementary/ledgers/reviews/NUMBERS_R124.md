# NUMBERS_R124.md — program R124 (2026-09-19): the author's rulings on REPORT_R123

No model call is made by this pass. Two readings from recorded rows (`reviews/v21/tools/margins_r124.py`, `reviews/v21/results/margins_r124.json`) and the two-decimal forms the rulings print. Ledger keys `AUX-R124-*`.

## AUX-R124-OP5-V3-MARGINS — Opus 5 under the all-states summary minus the all-states lookup (ruling B2; the recorded INDEXED-V3 rows of rows_OP5.jsonl through cf2_reader_score.score_lane with the v3 lookup of reviews/r122/tools/oai_score.py; 1,000 paired draws, seed 42)

| scope | Opus 5 | lookup | margin | item interval | persona interval | reliable |
|---|---:|---:|---:|---|---|---|
| whole set (n 444) | 0.9079 | 0.8756 | +0.0323 | [+0.0060, +0.0617] | [+0.0077, +0.0608] | yes (the recorded AUX-R103-MARGIN row of tab:counterfactual) |
| supersession (264) | 0.9319 | 0.8995 | +0.0324 | [−0.0010, +0.0687] | [−0.0030, +0.0699] | no |
| retraction (90) | 0.8100 | 0.7975 | +0.0125 | [−0.0726, +0.0890] | [−0.0535, +0.0803] | no |
| expiry (90) | 0.9267 | 0.8711 | +0.0556 | [−0.0236, +0.1380] | [+0.0015, +0.1169] | no |

Printed: $0.03$ (abstract, Section 5, Conclusion: "only Opus 5 does, by 0.03"), the per-state values at four decimals in Appendix C.2.

## AUX-R124-MINI-K5-PERSTATE — GPT-4.1 mini at five draws, per-state gain over blind with both intervals (ruling B5's check; reviews/r122/rows/rows_MINI5.jsonl, the X4 collapse; the item-level and persona-grouped bootstrap of the AUROC minus 0.50, 1,000 draws, seed 42)

| summary | state | AUROC | gain | item interval | persona interval | separates (both exclude zero) |
|---|---|---:|---:|---|---|---|
| default | supersession | 0.8793 | +0.3793 | [+0.3259, +0.4247] | [+0.3135, +0.4351] | yes |
| default | retraction | 0.5761 | +0.0761 | [−0.0517, +0.2052] | [+0.0242, +0.1341] | no |
| default | expiry | 0.5594 | +0.0594 | [−0.0720, +0.1797] | [+0.0048, +0.1162] | no |
| all-states | supersession | 0.8829 | +0.3829 | [+0.3305, +0.4277] | [+0.3318, +0.4348] | yes |
| all-states | retraction | 0.8433 | +0.3433 | [+0.2527, +0.4296] | [+0.2725, +0.4097] | yes |
| all-states | expiry | 0.6719 | +0.1719 | [+0.0347, +0.3055] | [+0.0723, +0.2934] | yes |

At five draws GPT-4.1 mini separates the expired versions under the all-states summary (the recorded one-draw row, 0.5869, did not: item interval [−0.0524, +0.2230], AUX-CF2-PERSTATE), so Section 5's "all but GPT-4.1 mini the expired ones" cannot stand once Figure 3 is redrawn from the five-draw rows; held with B5 for the author's wording.

## AUX-R124-PRINTED — the other printed forms of the pass

| printed (where) | value | source |
|---|---|---|
| $72\%$ of the $109$ events, $78$ of them (Appendix E.9, ruling D2) | 78 / 109 = 0.7156 supersession events retain an active obsolete assertion | AUX-BELIEVED-FR (e1_metamemory/NUMBERS.md) |
| \texttt{agentic-memory} 0.0.1 (Section 7, Table 2; the R124 addition on interface-specific claims) | the installed package version under which the A-MEM banks were built | reviews/NUMBERS_R86.md AUX-R86-AMEM-LINKS ("agentic-memory 0.0.1, github.com/agiresearch/A-mem") |
| the two reproduction scripts named in Table 2's caption | e1_metamemory/tools/repro_mem0_erase.py (10,074 points; 1,276 = 12.7% carry updated_at) and repro_amem_links.py (11,319 notes; 23,186 references; 0 resolving), both run on 2026-09-19 and matching the printed rows | AUX-BELIEVED-MEM0; AUX-R86-AMEM-LINKS |

## AUX-R124-TALLY — the prediction count after E10 (Section 4; Appendix F's count paragraph; the rule of AUX-R123-TALLY unchanged)

E10 (registrations/ADDENDUM_CF2_HYBRID_READER.md, frozen at fe6ff84 before its run; r82_counterfactual/cf2/NUMBERS_CF2.md section 14e) registered two predictions with a bar: P-H1 (the hybrid exceeds the name lookup reliably) failed, +0.0201 with the item-level interval [−0.0016, +0.0410] including zero; P-H2 (GPT-5.6 Sol stays reliably above the hybrid) held, +0.0635 with both intervals excluding zero. They join tab:registrations-d.

| table | predictions | otherwise |
|---|---:|---:|
| tab:registrations | 47 | 8 |
| tab:registrations-b | 17 | 10 |
| tab:registrations-c | 0 | 0 |
| tab:registrations-d (AUX-R123-TALLY's 26 with 9, plus P-H1, P-H2) | 28 | 10 |
| **total** | **92** | **28** |

Printed: "Of the $92$ predictions preregistered with a bar, each before the run that tests it, $28$ came out otherwise" (Section 4); "Table~\ref{tab:registrations-d} $28$ with $10$: $92$ predictions, $28$ of which came out otherwise" (Appendix F). Before this block the sentence read 90 / 27 (AUX-R123-TALLY).

## AUX-R124-HYB-PRINTED — the hybrid reader's printed forms (Appendix C.2, tab:cf-hybrid and its paragraph; Appendix F)

Every value from r82_counterfactual/cf2/results/cf_scores_hybrid.json through reviews/v21/tools/ledger_hybrid_r124.py (section 14e, AUX-CF2-HYB-*): whole set 0.7865 [0.7488, 0.8234]; minus the lookup +0.0201 ([−0.0016, +0.0410]; [+0.0039, +0.0409]); per state 0.9070 / 0.5889 / 0.5942, minus the lookup −0.0153 / +0.0889 / +0.0942 (the lookup 0.9223 / 0.5000 / 0.5000); minus CR-nb1 +0.1242; the five models minus the hybrid −0.0698, −0.0299, +0.0540, +0.0635, +0.0553; the coefficient ranges +1.13 to +1.29 (lookup), +0.39 to +0.53 (share). The stop rule of ruling E1 (stop and show if the hybrid closes most of the model margin): it closes 0.0201 of GPT-5.6 Sol's 0.0836 margin over the lookup (AUX-CF2-OAI-P-S1), about a quarter, so the rule did not fire.
