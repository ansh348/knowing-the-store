# NUMBERS_R131.md: the pass ledger of program R131 (2026-09-20; the author's brief 'KtS R131: land R125 in the body')

Written by `reviews/v22/tools/ledger_r131.py`; every row is read from the R125 artifacts under `reviews/r125/results/` (the ledger rows are `r82_counterfactual/cf2/NUMBERS_CF2.md` section 15) or from the recorded values the body already printed; no number is typed by hand. Rounding is half-up on the four-decimal value at two decimals (the one exact tie, GPT-5.6 Sol's counted-state fall of $-0.3250$, prints 0.33).

## AUX-R131-PRINTED — the two-decimal forms the body prints, each beside its artifact value and source key (the number gate, `r131_number_gate.py`: 135 checks, 0 mismatches)

| where | printed | artifact value | reliability, claimed / artifact | source |
|---|---|---|---|---|
| 5.1 p1: category-given count reader wins every retraction triple | 30/0/0 | 30/0/0 |  | AUX-CF2-R125-PERSTATE CR-oracle-a_v2 RETRACTION |
| 5.1 p1: ... and every expiry triple | 30/0/0 | 30/0/0 |  | AUX-CF2-R125-PERSTATE CR-oracle-a_v2 EXPIRY |
| 5.1 p1: the name lookup wins 82 of the 88 supersession triples and loses none | 82/6/0 | 82/6/0 |  | AUX-CF2-R125-PERSTATE LOOKUP_v2 SUPERSESSION |
| 5.1 p2: removing counts leaves mini within 0.01 (matched; mini one draw) | 0.00 | 0.0000 |  | AUX-CF2-R125-CONTRASTS 'E2 mini names-only minus intact' whole |
| 5.1 p2: ... Haiku within 0.01 (matched) | 0.00 | 0.0034 |  | AUX-CF2-R125-CONTRASTS 'E2 Haiku names-only minus intact' whole |
| 5.1 p2: counts alone below names alone by 0.14, mini (matched) | 0.14 | 0.1351 | reliable / reliable | AUX-CF2-R125-CONTRASTS 'E2 mini counts-only minus names-only' whole |
| 5.1 p2: ... 0.14, Haiku (matched) | 0.14 | 0.1385 | reliable / reliable | AUX-CF2-R125-CONTRASTS 'E2 Haiku counts-only minus names-only' whole |
| 5.1 p2: (0.12 pooled, mini) carried: AUX-CF2-NC-MINI counts only minus names only -0.1242 | 0.12 | 0.1242 |  | tab:cf-names-counts (AUX-CF2-NC-*), the body's recorded value |
| 5.1 p2: (0.16 pooled, Haiku) carried: AUX-CF2-NC-H45 -0.1562 | 0.16 | 0.1562 |  | tab:cf-names-counts (AUX-CF2-NC-*), the body's recorded value |
| 5.1 p2: the whole loss falls on supersession: mini counted-state difference not reliable | not reliable | not reliable |  | AUX-CF2-R125-CONTRASTS mini counts-only minus names-only, counted |
| 5.1 p2: ... Haiku counted-state difference not reliable | not reliable | not reliable |  | AUX-CF2-R125-CONTRASTS Haiku counts-only minus names-only, counted |
| 5.1 p2: guessing count reader 0.77 on retraction (matched) | 0.77 | 0.7667 |  | AUX-CF2-R125-PERSTATE CR-nb1_v2 RETRACTION |
| 5.1 p2: ... 0.75 on expiry | 0.75 | 0.7500 |  | AUX-CF2-R125-PERSTATE CR-nb1_v2 EXPIRY |
| 5.1 p2: mini five draws reliably below the guessing reader on retraction | reliable | reliable |  | AUX-CF2-R125-VS-COUNT MINI5_v2 minus CR-nb1 RETRACTION |
| 5.1 p2: mini five draws reliably below the guessing reader on expiry | reliable | reliable |  | AUX-CF2-R125-VS-COUNT MINI5_v2 minus CR-nb1 EXPIRY |
| 5.1 p2: mini one draw reliably below the guessing reader on retraction | reliable | reliable |  | AUX-CF2-R125-VS-COUNT MINI1_v2 minus CR-nb1 RETRACTION |
| 5.1 p2: mini one draw reliably below the guessing reader on expiry | reliable | reliable |  | AUX-CF2-R125-VS-COUNT MINI1_v2 minus CR-nb1 EXPIRY |
| 5.1 p2: Haiku reliably below the guessing reader on retraction | reliable | reliable |  | AUX-CF2-R125-VS-COUNT H45_v2 minus CR-nb1 RETRACTION |
| 5.1 p2: Haiku reliably below the guessing reader on expiry | reliable | reliable |  | AUX-CF2-R125-VS-COUNT H45_v2 minus CR-nb1 EXPIRY |
| 5.1 p3: mini 0.86 to 0.53 (carried, Appendix E.10) | 0.86 / 0.53 | 0.86 / 0.53 |  | the body's recorded values (Appendix E.10, the own-name ablation) |
| 5.1 p3: Haiku 0.89 to 0.68 (carried) | 0.89 / 0.68 | 0.89 / 0.68 |  | the body's recorded values (Appendix E.10) |
| 5.1 p4: Luna, Sol, Opus on retraction and expiry, matched, low end 0.58 | 0.58 | 0.5833 |  | AUX-CF2-R125-PERSTATE SOL_v2 RETRACTION 0.5833 |
| 5.1 p4: ... high end 0.87 | 0.87 | 0.8667 |  | AUX-CF2-R125-PERSTATE LUNA_v2 EXPIRY 0.8667 |
| 5.1 p4: LUNA_v2 not reliably below the guessing reader on retraction | not reliably below | not reliably below |  | AUX-CF2-R125-VS-COUNT LUNA_v2 minus CR-nb1 RETRACTION (-0.1167) |
| 5.1 p4: LUNA_v2 not reliably below the guessing reader on expiry | not reliably below | not reliably below |  | AUX-CF2-R125-VS-COUNT LUNA_v2 minus CR-nb1 EXPIRY (+0.1167) |
| 5.1 p4: SOL_v2 not reliably below the guessing reader on retraction | not reliably below | not reliably below |  | AUX-CF2-R125-VS-COUNT SOL_v2 minus CR-nb1 RETRACTION (-0.1833) |
| 5.1 p4: SOL_v2 not reliably below the guessing reader on expiry | not reliably below | not reliably below |  | AUX-CF2-R125-VS-COUNT SOL_v2 minus CR-nb1 EXPIRY (+0.0833) |
| 5.1 p4: OP5_v2 not reliably below the guessing reader on retraction | not reliably below | not reliably below |  | AUX-CF2-R125-VS-COUNT OP5_v2 minus CR-nb1 RETRACTION (+0.0000) |
| 5.1 p4: OP5_v2 not reliably below the guessing reader on expiry | not reliably below | not reliably below |  | AUX-CF2-R125-VS-COUNT OP5_v2 minus CR-nb1 EXPIRY (-0.0667) |
| 5.1 p4: Opus falls by 0.28 across the two counted states (matched) | 0.28 | 0.2833 | reliable / reliable | AUX-CF2-R125-CONTRASTS 'moved count Opus k5 minus sup-only k5' counted |
| 5.1 p4: Sol by 0.33 (matched, counted) | 0.33 | 0.3250 | reliable / reliable | AUX-CF2-R125-CONTRASTS 'moved count Sol k5 minus sup-only k5 (E9)' counted |
| 5.1 p4: Luna falls by 0.32 on retraction (matched) | 0.32 | 0.3167 | reliable / reliable | AUX-CF2-R125-CONTRASTS 'moved count Luna k5 minus sup-only k5 (E9)' ret |
| 5.1 p4: ... 0.27 on expiry | 0.27 | 0.2667 | reliable / reliable | AUX-CF2-R125-CONTRASTS 'moved count Luna k5 minus sup-only k5 (E9)' exp |
| 5.1 p4: 'moved count mini minus sup-only' whole not reliable | not reliable | not reliable |  | AUX-CF2-R125-CONTRASTS 'moved count mini minus sup-only' whole |
| 5.1 p4: 'moved count mini minus sup-only' ret not reliable | not reliable | not reliable |  | AUX-CF2-R125-CONTRASTS 'moved count mini minus sup-only' ret |
| 5.1 p4: 'moved count mini minus sup-only' exp not reliable | not reliable | not reliable |  | AUX-CF2-R125-CONTRASTS 'moved count mini minus sup-only' exp |
| 5.1 p4: 'moved count mini minus sup-only' counted not reliable | not reliable | not reliable |  | AUX-CF2-R125-CONTRASTS 'moved count mini minus sup-only' counted |
| 5.1 p4: 'moved count Haiku minus sup-only' whole not reliable | not reliable | not reliable |  | AUX-CF2-R125-CONTRASTS 'moved count Haiku minus sup-only' whole |
| 5.1 p4: 'moved count Haiku minus sup-only' ret not reliable | not reliable | not reliable |  | AUX-CF2-R125-CONTRASTS 'moved count Haiku minus sup-only' ret |
| 5.1 p4: 'moved count Haiku minus sup-only' exp not reliable | not reliable | not reliable |  | AUX-CF2-R125-CONTRASTS 'moved count Haiku minus sup-only' exp |
| 5.1 p4: 'moved count Haiku minus sup-only' counted not reliable | not reliable | not reliable |  | AUX-CF2-R125-CONTRASTS 'moved count Haiku minus sup-only' counted |
| 5.1 p4: pooled moved count, expiry falls reliable for all three, retraction for Opus alone (carried: AUX-R129-E9-PRINTED) | as printed in the R129 body | as printed in the R129 body |  | reviews/NUMBERS_R129.md AUX-R129-E9-PRINTED (Opus -0.1003 / -0.1281 both reliable; Luna -0.0664 no / -0.1158 yes; Sol -0.0322 no / -0.1914 yes) |
| 5.1 p4: removing every count costs Luna a reliable 0.06 (pooled) | 0.06 | 0.0598 | reliable / reliable | AUX-CF2-R125-NC-LUNA-NAMES minus intact |
| 5.1 p4: ... Opus 0.04 (pooled) | 0.04 | 0.0426 | reliable / reliable | AUX-CF2-R125-NC-OP5-NAMES minus intact |
| 5.1 p4: counts alone reliably below names alone, Luna (pooled) | reliable | reliable |  | AUX-CF2-R125-NC-P-N4 Luna |
| 5.1 p4: ... Opus | reliable | reliable |  | AUX-CF2-R125-NC-P-N4 Opus |
| 5.1 p4: Sol was not run | NOT RUN | NOT RUN |  | AUX-CF2-R125-NC (D-R125-1) |
| 5.2 p1: the lookup scores 0.97 on supersession (matched) | 0.97 | 0.9659 |  | AUX-CF2-R125-PERSTATE LOOKUP_v2 SUPERSESSION |
| 5.2 p1: Opus 0.01 above it (not reliable) | 0.01 | 0.0114 | not reliable / not reliable | AUX-CF2-R125-VS-LOOKUP OP5_v2 sup |
| 5.2 p1: Luna 0.01 below | 0.01 | 0.0057 | not reliable / not reliable | AUX-CF2-R125-VS-LOOKUP LUNA_v2 sup |
| 5.2 p1: Sol 0.01 below | 0.01 | 0.0057 | not reliable / not reliable | AUX-CF2-R125-VS-LOOKUP SOL_v2 sup |
| 5.2 p1: mini reliably below by 0.07 | 0.07 | 0.0739 | reliable / reliable | AUX-CF2-R125-VS-LOOKUP MINI5_v2 sup |
| 5.2 p1: sibling control, lookup and every model 0.88 to 0.97, low end | 0.88 | 0.8807 |  | AUX-CF2-R125-SB-H45 0.8807 |
| 5.2 p1: ... high end | 0.97 | 0.9716 |  | AUX-CF2-R125-SB-OP5 0.9716 |
| 5.2 p1: none reliably above the lookup (P-SB4) | HELD | HELD |  | AUX-CF2-R125-SB-P-SB4 |
| 5.2 p1: random-token lookup 0.47 | 0.47 | 0.4716 |  | AUX-CF2-R125-SB-RANDTOK |
| 5.2 p1: count reader 0.50 | 0.50 | 0.5000 |  | AUX-CF2-R125-SB-CR-NB1 |
| 5.2 p2: the lookup 0.78 (matched, whole) | 0.78 | 0.7770 |  | AUX-CF2-R125-MATCHED-V2 LOOKUP_v2 |
| 5.2 p2: Haiku 0.78 | 0.78 | 0.7770 |  | AUX-CF2-R125-MATCHED-V2 H45_v2 |
| 5.2 p2: mini 0.73 | 0.73 | 0.7264 |  | AUX-CF2-R125-MATCHED-V2 MINI5_v2 |
| 5.2 p2: Luna, Sol, Opus 0.86 to 0.88, low end | 0.86 | 0.8581 |  | AUX-CF2-R125-MATCHED-V2 SOL_v2 0.8581 |
| 5.2 p2: ... high end | 0.88 | 0.8784 |  | AUX-CF2-R125-MATCHED-V2 LUNA_v2 0.8784 |
| 5.2 p2: a reliable 0.08 to 0.10 above the lookup, low end | 0.08 | 0.0811 | reliable / reliable | AUX-CF2-R125-VS-LOOKUP SOL_v2 whole +0.0811 |
| 5.2 p2: ... high end | 0.10 | 0.1014 | reliable / reliable | AUX-CF2-R125-VS-LOOKUP LUNA_v2 whole +0.1014 |
| 5.2 p2: (0.07 to 0.08 pooled) carried | 0.07 / 0.08 | 0.07 / 0.08 |  | AUX-CF2-OAI-P-S2 +0.0754, -P-S1 +0.0836, AUX-CF2-OP5 margin; the body's recorded values |
| 5.2 p2: the lookup ties every retraction triple | 0/30/0 | 0/30/0 |  | AUX-CF2-R125-PERSTATE LOOKUP_v2 RETRACTION |
| 5.2 p2: ... every expiry triple | 0/30/0 | 0/30/0 |  | AUX-CF2-R125-PERSTATE LOOKUP_v2 EXPIRY |
| 5.2 p2: the hybrid reader scores 0.89 (matched) | 0.89 | 0.8851 |  | AUX-CF2-R125-MATCHED-V2 HYBRID_v2 |
| 5.2 p2: hybrid reliably above the lookup (matched) | reliable | reliable |  | AUX-CF2-R125-CONTRASTS 'hybrid minus name lookup (P-H1)' whole +0.1081 |
| 5.2 p2: level with the three models: 'Luna minus hybrid' not reliable | not reliable | not reliable |  | AUX-CF2-R125-CONTRASTS 'Luna minus hybrid' whole -0.0068 |
| 5.2 p2: level with the three models: 'Sol minus hybrid (P-H2)' not reliable | not reliable | not reliable |  | AUX-CF2-R125-CONTRASTS 'Sol minus hybrid (P-H2)' whole -0.0270 |
| 5.2 p2: level with the three models: 'Opus minus hybrid' not reliable | not reliable | not reliable |  | AUX-CF2-R125-CONTRASTS 'Opus minus hybrid' whole -0.0101 |
| 5.2 p2: the hybrid 0.79 pooled (carried) | 0.79 | 0.7865 |  | AUX-CF2-HYB-WHOLE 0.7865 |
| 5.2 p2: the three a reliable 0.05 to 0.06 above it, pooled (carried) | 0.05 / 0.06 | 0.05 / 0.06 |  | AUX-CF2-HYB-VS-MODELS +0.0540 (Opus), +0.0553 (Luna), +0.0635 (Sol), each with both intervals excluding zero |
| 5.2 p3: the all-states lookup 0.91 (matched) | 0.91 | 0.9088 |  | AUX-CF2-R125-MATCHED-V3 ALLSTATES_v3 |
| 5.2 p3: Haiku gains a reliable 0.35 on the counted states (matched) | 0.35 | 0.3500 | reliable / reliable | AUX-CF2-R125-CONTRASTS 'all-states Haiku minus sup-only' counted |
| 5.2 p3: Opus reaches 0.94 | 0.94 | 0.9392 |  | AUX-CF2-R125-MATCHED-V3 OP5_v3 |
| 5.2 p3: Opus's 0.03 lead over that lookup, matched, not reliable | 0.03 | 0.0304 | not reliable / not reliable | AUX-CF2-R125-OP5-V3 whole +0.0304 |
| 5.2 p3: ... pooled 0.03 reliable (carried) | 0.03 | 0.0323 | reliable / reliable | AUX-R103-MARGIN +0.0323 [+0.0060,+0.0617]; [+0.0077,+0.0608] |
| 5.2 p4: coverage-only reader 0.75 pooled | 0.75 | 0.7500 |  | AUX-CF2-R125 coverage_only pooled |
| 5.2 p4: ... 0.50 matched | 0.50 | 0.5000 |  | AUX-CF2-R125 coverage_only matched |
| 5.2 p4: random-token lookup 0.60 pooled | 0.60 | 0.5954 |  | AUX-CF2-R125-MATCHED-V2 RANDTOK_v2 pooled 0.5954 |
| 5.2 p4: ... 0.65 matched | 0.65 | 0.6453 |  | AUX-CF2-R125-MATCHED-V2 RANDTOK_v2 matched 0.6453 |
| 5.2 p4: 24 of the 88 PRESENT lists are empty | 24 | 24 |  | AUX-CF2-R125-T2-CENSUS SUPERSESSION PRESENT empty |
| 5.2 p4: the name lookup a reliable 0.13 above it (matched) | 0.13 | 0.1318 | reliable / reliable | AUX-CF2-R125-CONTRASTS 'random-token minus name lookup (v2)' whole -0.1318 |
| 5.2 p4: 'the PN version's list is one name longer' (81 of 88 by one; 6 by two; 1 by three) | 81/6/1 | 81/6/1 |  | AUX-CF2-R125-T2-CENSUS PN minus PRESENT length; the author's sentence says 'one name longer' (a simplification, noted) |
| Table 1 matched column: MINI5_v2 | 0.73 | 0.7264 |  | AUX-CF2-R125-MATCHED-V2/-V3 MINI5_v2 ((W + T/2) / 148 = 100/15/33) |
| Table 1 matched column: MINI5_v3 | 0.90 | 0.8953 |  | AUX-CF2-R125-MATCHED-V2/-V3 MINI5_v3 ((W + T/2) / 148 = 130/5/13) |
| Table 1 matched column: H45_v2 | 0.78 | 0.7770 |  | AUX-CF2-R125-MATCHED-V2/-V3 H45_v2 ((W + T/2) / 148 = 89/52/7) |
| Table 1 matched column: H45_v3 | 0.91 | 0.9054 |  | AUX-CF2-R125-MATCHED-V2/-V3 H45_v3 ((W + T/2) / 148 = 125/18/5) |
| Table 1 matched column: LUNA_v2 | 0.88 | 0.8784 |  | AUX-CF2-R125-MATCHED-V2/-V3 LUNA_v2 ((W + T/2) / 148 = 129/2/17) |
| Table 1 matched column: SOL_v2 | 0.86 | 0.8581 |  | AUX-CF2-R125-MATCHED-V2/-V3 SOL_v2 ((W + T/2) / 148 = 126/2/20) |
| Table 1 matched column: OP5_v2 | 0.88 | 0.8750 |  | AUX-CF2-R125-MATCHED-V2/-V3 OP5_v2 ((W + T/2) / 148 = 128/3/17) |
| Table 1 matched column: OP5_v3 | 0.94 | 0.9392 |  | AUX-CF2-R125-MATCHED-V2/-V3 OP5_v3 ((W + T/2) / 148 = 139/0/9) |
| Table 1 matched column: LOOKUP_v2 | 0.78 | 0.7770 |  | AUX-CF2-R125-MATCHED-V2/-V3 LOOKUP_v2 ((W + T/2) / 148 = 82/66/0) |
| Table 1 matched column: ALLSTATES_v3 | 0.91 | 0.9088 |  | AUX-CF2-R125-MATCHED-V2/-V3 ALLSTATES_v3 ((W + T/2) / 148 = 121/27/0) |
| Table 1 matched column: CR-nb1_v2 | 0.72 | 0.7196 |  | AUX-CF2-R125-MATCHED-V2/-V3 CR-nb1_v2 ((W + T/2) / 148 = 65/83/0) |
| Table 1 matched column: CR-oracle-a_v2 | 0.70 | 0.7027 |  | AUX-CF2-R125-MATCHED-V2/-V3 CR-oracle-a_v2 ((W + T/2) / 148 = 60/88/0) |
| Table 1 matched column: HYBRID_v2 | 0.89 | 0.8851 |  | AUX-CF2-R125-MATCHED-V2/-V3 HYBRID_v2 ((W + T/2) / 148 = 114/34/0) |
| Table 1 hybrid row: W/T/L 114/34/0 | 114/34/0 | 114/34/0 |  | AUX-CF2-R125-MATCHED-V2 HYBRID_v2 |
| Table 1 hybrid row: pooled 0.79 (carried) | 0.79 | 0.7865 |  | AUX-CF2-HYB-WHOLE 0.7865, persona interval [0.7488, 0.8234] |
| Table 1 difference row: pooled +0.03 (carried) | 0.03 | 0.0323 |  | AUX-R103-MARGIN |
| Table 1 difference row: matched +0.03 | 0.03 | 0.0304 |  | AUX-CF2-R125-OP5-V3 whole |
| Figure 3: mini's expiry value under the default summary 0.40 (the y axis must reach 0.35) | 0.40 | 0.4000 |  | AUX-CF2-R125-FIG3 mini expiry |
| Abstract: 148 questions | 148 | 148 |  | the counterfactual set's triples |
| Abstract: sibling control at 0.88 or higher (the lowest of the lookup and the five models) | 0.88 | 0.8807 |  | AUX-CF2-R125-SB-H45 0.8807 |
| Abstract: lead the lookup by 0.08 to 0.10 within matched triples | 0.08 / 0.10 | 0.08 / 0.10 |  | AUX-CF2-R125-VS-LOOKUP SOL_v2 / LUNA_v2 whole |
| Abstract: 0.60 and 0.59 (carried) | 0.60 / 0.59 | 0.60 / 0.59 |  | AUX-E1R-BELIEVED-NOK 0.5959, AUX-E1R-NB6 0.5858 (the body's recorded values) |
| Conclusion: Opus's 0.03 lead (both metrics) | 0.03 / 0.03 | 0.03 / 0.03 |  | AUX-R103-MARGIN; AUX-CF2-R125-OP5-V3 |
| Section 6 FR-Bank: on the 82 the alignment marks | 82 | 82 |  | AUX-CF2-R125-T3-FRBANK join_marked_0.80 n_pos |
| Section 6 FR-Bank: the capped summary still costs mini 0.13 on the 82, reliable | 0.13 | 0.1274 | reliable / reliable | AUX-CF2-R125-T3-FRBANK join_marked_0.80 mini_capped minus ground truth |
| Section 6 FR-Bank: the capped summary still costs Haiku 0.13 on the 82, reliable | 0.13 | 0.1258 | reliable / reliable | AUX-CF2-R125-T3-FRBANK join_marked_0.80 haiku_capped minus ground truth |
| Section 6 FR-Bank: the capped summary still costs the lookup 0.20 on the 82, reliable | 0.20 | 0.2027 | reliable / reliable | AUX-CF2-R125-T3-FRBANK join_marked_0.80 lookup_capped minus ground truth |
| Section 6 Graphiti: invalidation marks 13 of the 34 | 13 | 13 |  | AUX-CF2-R125-T3-GRAPHITI recorded buckets at 0.80 RECOVERED |
| Section 6 Graphiti: 11 of the 34 never extracted | 11 | 11 |  | AUX-CF2-R125-T3-GRAPHITI EXTRACTION_MISS at 0.80 |
| Section 6 Graphiti: 34 = recovered + stale-active + extraction miss | 34 | 34 |  | AUX-CF2-R125-T3-GRAPHITI |
| Section 6 Graphiti: mini 0.58 with the capped store-written summary over all 47 (carried) | 0.58 | 0.5765 |  | AUX-CF2-R125-T3-GRAPHITI all_47 G10-BELIEVED (the recorded row, AUX-R85-G10) |
| Section 6 Graphiti: 47 obligations | 47 | 47 |  | AUX-CF2-R125-T3-GRAPHITI all_47 n_pos |
| Section 6 Graphiti: 0.74 under ground truth (carried) | 0.74 | 0.7424 |  | AUX-CF2-R125-T3-GRAPHITI all_47 TRUE (the recorded row) |
| Section 6 Graphiti: the store's own name lookup 0.68 (carried) | 0.68 | 0.6780 |  | AUX-CF2-R125-T3-GRAPHITI all_47 NB6-emb-capped (the recorded row) |
| Section 6 Graphiti: a reliable 0.10 above mini (carried: +0.1014 from the unrounded scores, Appendix G.4) | 0.10 | 0.1014 | reliable / reliable | r85_graphiti/NUMBERS_R85.md (G.4's '+0.1014') |
| Section 6 Graphiti: on the 23 obligations whose content the graph retains | 23 | 23 |  | AUX-CF2-R125-T3-GRAPHITI retained_0.80 n_pos |
| Section 6 Graphiti: mini scores 0.69 on the 23 (capped store-written) | 0.69 | 0.6920 |  | AUX-CF2-R125-T3-GRAPHITI retained_0.80 G10-BELIEVED |
| Section 6 Graphiti: against 0.84 under ground truth on the 23 | 0.84 | 0.8433 |  | AUX-CF2-R125-T3-GRAPHITI retained_0.80 TRUE |
| Section 6 Graphiti: still a reliable loss on the 23 | reliable | reliable |  | AUX-CF2-R125-T3-GRAPHITI retained_0.80 G10-BELIEVED minus TRUE -0.1512 |
| Limitations: the 22 obligations the alignment does not mark | 22 | 22 |  | AUX-CF2-R125-T3-FRBANK join_unmarked_0.80 n_pos |
| Limitations: mini scores 0.52 on them under ground truth | 0.52 | 0.5210 |  | AUX-CF2-R125-T3-FRBANK join_unmarked_0.80 mini_true |
| Limitations: 104 - 82 = 22 | 22 | 22 |  | AUX-CF2-R125-T3-FRBANK |
| Appendix F: P-SB1 verdict | HELD | HELD |  | AUX-CF2-R125-SB-P-SB1 (a recorded value) |
| Appendix F: P-SB2 verdict | HELD | HELD |  | AUX-CF2-R125-SB-P-SB2 |
| Appendix F: P-SB3 verdict | HELD | HELD |  | AUX-CF2-R125-SB-P-SB3 (recorded values) |
| Appendix F: P-SB4 verdict | HELD | HELD |  | AUX-CF2-R125-SB-P-SB4 |
| Appendix F: P-N3 verdict | FAILED | FAILED |  | AUX-CF2-R125-NC-P-N3 |
| Appendix F: P-N4 verdict | HELD | HELD |  | AUX-CF2-R125-NC-P-N4 |
| Appendix F: P-N5 verdict | FAILED | FAILED |  | AUX-CF2-R125-NC-P-N5 |

## AUX-R131-TAB1 — Table 1's matched column, (W + T/2) / 148 from the printed W/T/L (AUX-CF2-R125-SANITY: the printed counts reproduce from the rows), the hybrid row and the difference row

| row | W/T/L | (W + T/2) / 148 | printed |
|---|---|---:|---:|
| mini, superseded | 100/15/33 | 0.7264 | 0.73 |
| mini, all | 130/5/13 | 0.8953 | 0.90 |
| Haiku, superseded | 89/52/7 | 0.7770 | 0.78 |
| Haiku, all | 125/18/5 | 0.9054 | 0.91 |
| Luna | 129/2/17 | 0.8784 | 0.88 |
| Sol | 126/2/20 | 0.8581 | 0.86 |
| Opus, superseded | 128/3/17 | 0.8750 | 0.88 |
| Opus, all | 139/0/9 | 0.9392 | 0.94 |
| Name lookup, superseded | 82/66/0 | 0.7770 | 0.78 |
| Name lookup, all | 121/27/0 | 0.9088 | 0.91 |
| Count reader, guessed category | 65/83/0 | 0.7196 | 0.72 |
| Count reader, given category | 60/88/0 | 0.7027 | 0.70 |
| Lookup with one count feature (the hybrid reader, E10) | 114/34/0 | 0.8851 | 0.89 |

The hybrid row's pooled value and persona interval: 0.7865 [0.7488, 0.8234] (AUX-CF2-HYB-WHOLE), printed 0.79 [0.75, 0.82]. The difference row (all states named, Opus 5 minus the all-states lookup) prints four decimals: pooled +0.0323 [+0.0060, +0.0617]; [+0.0077, +0.0608] (AUX-R103-MARGIN, reliable); matched +0.0304 [-0.0068, +0.0643]; [-0.0038, +0.0648] (AUX-CF2-R125-OP5-V3, not reliable); the body prints both as 0.03.

## AUX-R131-COUNT — the prediction count with the two R125 registrations in it

AUX-R129-COUNT: 93 predictions, 29 otherwise (tab:registrations-d 29 with 11). The sibling-name control registered four readings with a bar: P-SB1 (HELD) and P-SB3 (HELD) were disclosed at the freeze as recorded values from the scorer's pre-freeze dry run (ADDENDUM_R125_SIBLING section 8; D-R125-2) and are **not counted as predictions**; P-SB2 (HELD) and P-SB4 (HELD) count, neither otherwise. E2 Amendment 1 registered three: P-N3 (FAILED (on the models run)), P-N4 (HELD (on the models run)), P-N5 (FAILED (on the models run)); each counts once (the verdict is stated on the models run; GPT-5.6 Sol's lane not run), two otherwise. **With them: 98 predictions, 31 otherwise; the new tab:registrations-e carries 5 with 2**; the other four tables unchanged (47 with 8; 17 with 10; none; 29 with 11).

## AUX-R131-FIG3 — Figure 3 on the matched metric (`reviews/v22/src/fig3_data_matched.tex`, copied from `reviews/r125/results/fig3_data_matched.tex` by fig3_data_r131.py after checking every value against r125_matched.json; AUX-CF2-R125-FIG3)

The y axis reaches 0.35 (mini's expiry value under the default summary is 0.4000); the pooled figure (fig3_data.tex, AUX-R126-FIG3) moves to Appendix C.2 as fig:perstate-pooled.

## AUX-R131-APPENDIX — the appendix tables written by `reviews/v22/tools/appendix_r131.py`

tab:cf-nc-strong (r125_t5_nc.json; NUMBERS_CF2.md 15e), tab:cf-matched, tab:cf-classes, tab:cf-matched-vs, tab:cf-matched-ablations and the hybrid panel of tab:cf-hybrid (r125_matched.json; 15), tab:cf-emptiness (r125_t2_emptiness.json; 15b), tab:cf-sibling (r125_t4_sibling.json; 15d), tab:levels-strata (r125_t3_frbank.json; 15c), tab:graphiti-strata (r125_t3_graphiti.json; 15c), tab:registrations-e (the two registrations, frozen 5cd8f809f2 on day 41). Every value prints at four decimals as the artifact records it; the two-decimal forms in their captions (0.14; 0.60 of 0.77; 0.65 of 0.78; 0.71; 0.90; 0.80; 0.50; 0.05) are the rows of AUX-R131-PRINTED or the recorded body values.

## AUX-R131-CLOSE-PRINTED — the R131 close (2026-09-20; CONSOLIDATED ADDITIONS, ABSTRACT SWAP, MERGED RULINGS, FINAL RULINGS): every number the close's new texts print, beside its artifact value and source (`reviews/v22/tools/r131_close_gate.py`: 37 checks, 0 mismatches; rounding half-up on the recorded four-decimal value, as AUX-R131-PRINTED)

| where | printed | artifact value | reliability, claimed / artifact | source |
|---|---|---|---|---|
| Abstract: 148 questions | 148 | 148 |  | r125_matched.json readers/LOOKUP_v2/pn_vs_present/whole/n (the triples of the 444) |
| Abstract: 'at an AUROC of 0.88 or higher' (the lookup and every model, PN against the sibling, matched) | 0.88 | 0.8807 |  | r125_t4_sibling.json readers/*/pn_vs_sibling/matched, minimum over ['GPT-4.1 mini (five draws)', 'GPT-5.6 Luna (five draws)', 'GPT-5.6 Sol (draw 1)', 'Haiku 4.5 (five draws)', 'Name lookup', 'Opus 5 (draw 1)'] = 0.8807 |
| Abstract: chance 0.50 | 0.50 | 0.5000 |  | the definition (a tie scores half) |
| Abstract: 'lead the lookup by 0.08 to 0.10 overall' (lower end) | 0.08 | 0.0811 | reliable / reliable | r125_matched.json paired/vs_lookup/{LUNA_v2,SOL_v2,OP5_v2}/pn_vs_present/whole/delta (+0.1014, +0.0811, +0.0980) |
| Abstract: 'lead the lookup by 0.08 to 0.10 overall' (upper end) | 0.10 | 0.1014 |  | as above |
| Abstract: 'a lead that comes from retracted and expired records' (no stronger model reliably above the lookup on supersession; every retraction and expiry lead positive) | holds | holds |  | r125_matched.json paired/vs_lookup/*/pn_vs_present/per_state |
| Abstract: mini under the ground-truth summary (full obligation set) | 0.73 | 0.7339 |  | e1r_robustness/NUMBERS_E1R.md AUX-E1R-TRUE-NOK / AUX-E1R-NB6 row R-NOK-FRB TRUE, monitor 0.7339 |
| Abstract: the lookup under the ground-truth summary | 0.75 | 0.7484 |  | NUMBERS_E1R.md AUX-E1R-NB6 row R-NOK-FRB TRUE, NB-6 0.7484 |
| Abstract: mini under FR-Bank's capped store-written summary | 0.60 | 0.5959 |  | NUMBERS_E1R.md AUX-E1R-BELIEVED-NOK row R-NOK-FRB BELIEVED, monitor 0.5959 |
| Abstract: the lookup under FR-Bank's capped store-written summary | 0.59 | 0.5858 |  | NUMBERS_E1R.md AUX-E1R-NB6 row R-NOK-FRB BELIEVED, NB-6 0.5858 |
| Abstract: five models, the two smaller (mini, Haiku) and three stronger (Luna, Sol, Opus) | 5 | 5 |  | Section 4's model list (the five readers of Table 1) |
| Section 5.2 (payer 8): the coverage-only reader, pooled | 0.75 | 0.7500 |  | r125_matched.json coverage_only/pair_classes/pooled |
| Section 5.2 (payer 8): the coverage-only reader, matched | 0.50 | 0.5000 |  | r125_matched.json coverage_only/pn_vs_present/matched |
| Section 5.2 (payer 8): the lookup a reliable 0.13 above meaningless tokens on the matched metric | 0.13 | 0.1318 | reliable / reliable | r125_matched.json paired/vs_lookup/RANDTOK_v2/pn_vs_present/whole/delta (-0.1318, both intervals clear of zero) |
| Conclusion (P5b): 'only the three stronger models apply it' (Luna, Sol, Opus each above 0.85 under the explicit rubric; mini and Haiku below 0.60) | holds | holds |  | cf_scores_ix.json readers/*/A/P1 same-store AUROC (draw 1 where five draws ran): {'MINI': 0.4789, 'H45': 0.5464, 'LUNA': 0.964, 'SOL': 0.8815, 'OP5': 0.9885} |
| Conclusion (P5b): 'a fixed cue list matches the best of them' (the cue list and the best model round to the same value) | 0.99 | 0.9943 |  | cf_scores_ix.json lookups/A/keyword/same_store/auroc 0.9943 against the best model 0.9885 |
| Limitations L1 / E.3: 40 personas (numbered persona directories of LifeMemEval/) | 40 | 40 |  | LifeMemEval/<n>_<name>/ directories |
| E.3: 40 human-written manifests (one persona_*.yaml per directory) | 40 | 40 |  | LifeMemEval/<n>_<name>/persona_*.yaml |
| E.3: 1,400 sessions (35 per persona) | 1400 | 1400 |  | LifeMemEval/<n>_<name>/sessions/session_*.json |
| E.3: the three stores (FR-Bank, Mem0, A-MEM banks) are in the release's freeze commit | 3 | 3 |  | git ls-tree 5b097fb LifeMemEval/artifacts/ (the directories e1_metamemory/tools/backends.py:59-61 reads) |
| E.3: the release's question file holds 516 questions | 516 | 516 |  | LifeMemEval/lifemembench_questions.json |
| E.3: the full obligation set is 661 FR-Bank items | 661 | 661 |  | e1_metamemory/build/items_final.json (backend frbank, labels ABSENT / PRESENT / PRESENT-NEGATIVE) |
| E.3: 516 of the 661 ask a released question | 516 | 516 |  | items_final.json question_id in lifemembench_questions.json ids |
| E.3: 187 distinct released questions among them | 187 | 187 |  | as above, distinct question_id |
| E.3: 145 natural-absent probe items | 145 | 145 |  | items_final.json question_id 'probe_*' (the hard tier's natural-absent items) |
| E.3: the released questions used on the full store, the category-removed and the slot-removed variants (178 / 176 / 162) | 178/176/162 | 178/176/162 |  | items_final.json by variant |
| E.3: 148 counterfactual questions drafted by GPT-4.1 mini | 148 | 148 |  | r82_counterfactual/cf2/cf_questions_cf2.json questions |
| E.3: 444 counterfactual items (three versions each) | 444 | 444 |  | 3 x 148 (Table tab:setup; r125_matched.json n=148 triples) |
| E.3: the expiry extension, 14 pairs | 14 | 14 |  | r82_counterfactual/cf3/NUMBERS_CF3.md AUX-CF3 |
| E.3: the expiry extension, 42 items | 42 | 42 |  | r82_counterfactual/cf3/NUMBERS_CF3.md AUX-CF3 |
| E.3: crossed intent questions drafted (88 + 30) | 118 | 118 |  | cf_scores_ix.json lock/counts A_total + B_total |
| E.3: crossed intent questions asked (87 + 26) | 113 | 113 |  | cf_scores_ix.json lock/counts A_pass + B_pass |
| E.3: 148 paraphrases drafted by GPT-4.1 mini | 148 | 148 |  | cf2_paraphrase/para_questions.json rows (meta.model gpt-4.1-mini) |
| E.3: the cross-vendor set, 84 main-study items | 84 | 84 |  | e1xv_crossvendor/manifests/cell_84.json items |
| E.3: of them 76 with a released question and 8 natural-absent probes | 76/8 | 76/8 |  | cell_84.json item ids against lifemembench_questions.json |
| E.3: 40 Graphiti graphs | 40 | 40 |  | r85_graphiti/g10/ingest_all_status.json done |
| E.3: 1,365 episodes rendered from FR-Bank's records | 1365 | 1365 |  | r85_graphiti/NUMBERS_R85.md AUX-R85-G10-INGEST (Personas / episodes / records 40 / 1365 / 18936) |

The abstract's third finding prints the levels (0.73 and 0.75 to 0.60 and 0.59; G2 under its pattern reading, the author's ruling of the FINAL RULINGS 3: G2 concerns the lookup's level on the counterfactual set, where the level depends on the metric; the full-set numbers have one metric). The drops, for the record: mini 0.1380 (0.14), the lookup 0.1626 (0.16); R124 block C states no reason contradicting the ruling, so the level form stands.

Sol's counted-state fall under the moved count, $-0.3250$ exactly (AUX-CF2-R125-CONTRASTS), prints 0.33 in the body: the number gate rounds every body number half-up on the recorded four-decimal value (`Decimal ... ROUND_HALF_UP`), so 0.33 is the convention applied to every other body number (MERGED RULINGS 1A, confirmed); the appendix row prints $-0.3250$.

## AUX-R131-CLOSE-PROV — the provenance counts of Appendix E.3's paragraph (A1''), each counted from the tree by `r131_close_gate.py`; the release is the FR-Bank freeze `5b097fb` (audit/FREEZE_MANIFEST.md; Zenodo 10.5281/zenodo.20067778)

| quantity | value | source |
|---|---:|---|
| personas | 40 | LifeMemEval/<n>_<name>/ numbered directories |
| human-written manifests | 40 | LifeMemEval/<n>_<name>/persona_*.yaml |
| sessions per persona | 35 | session_*.json per directory (every persona 35) |
| sessions, all personas (1,400 = 1400) | 1,400 (1400) | LifeMemEval/<n>_<name>/sessions/session_*.json |
| stores of the release read by the main study | 3 | git ls-tree 5b097fb LifeMemEval/artifacts/: lifecycle_banks, mem0_41mini_banks, amem_banks (e1_metamemory/tools/backends.py:59-61) |
| released questions | 516 | LifeMemEval/lifemembench_questions.json |
| full obligation set, FR-Bank items | 661 | e1_metamemory/build/items_final.json (backend frbank; ABSENT / PRESENT / PRESENT-NEGATIVE) |
| of them asked with a released question | 516 | items_final.json question_id in the released ids |
| distinct released questions among them | 187 | as above, distinct question_id |
| released questions on the full store / category-removed / slot-removed variants | 178 / 176 / 162 | items_final.json by variant |
| natural-absent probe items (distinct texts) | 145 (115) | items_final.json question_id probe_* |
| distinct released questions used across the three backends | 217 | items_final.json, scored labels |
| counterfactual questions / items | 148 / 444 | r82_counterfactual/cf2/cf_questions_cf2.json; 3 versions each |
| expiry extension pairs / items | 14 / 42 | r82_counterfactual/cf3/NUMBERS_CF3.md AUX-CF3 |
| crossed intent questions drafted / asked / dropped | 118 / 113 / 5 | r82_counterfactual/cf2/results/cf_scores_ix.json lock/counts (A 88 -> 87, B 30 -> 26) |
| paraphrases drafted (GPT-4.1 mini) | 148 | cf2_paraphrase/para_questions.json rows |
| cross-vendor set items / with a released question / probes | 84 / 76 / 8 | e1xv_crossvendor/manifests/cell_84.json |
| Graphiti graphs / episodes (1,365 = 1365) | 40 / 1,365 (1365) | r85_graphiti/g10/ingest_all_status.json; r85_graphiti/NUMBERS_R85.md AUX-R85-G10-INGEST |

The question-only probes (e1qp_questionprior/PREREG_E1QP.md) are classifiers over the existing question strings and the cross-vendor set is a subset of the 661, so neither adds a question; the Graphiti graphs were built from FR-Bank's store records rendered one episode per session with every lifecycle field removed (r85_graphiti/render_episodes.py), not from the session transcripts.
