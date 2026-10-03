# NUMBERS_R123.md — program R123 (2026-09-19): the v21 update and writing pass (the author's brief with its amendments from R122's report)

No model call is made by this pass. It lands results ledgered elsewhere (the intent crossover, `r82_counterfactual/cf2/NUMBERS_CF2.md` §14d, AUX-CF2-IX-*; the no-human batch, `reviews/r122/NUMBERS_R122.md`, AUX-R122-*) and records here, beside their sources, (i) the two-decimal forms those landings print in the body, (ii) the supersession-only margins over the name lookup that the amendment's recomputation reads from the recorded rows (a table the paper had not printed), (iii) the recorded downstream policies' mean view over the 661 questions (a denominator the paper had not printed) and (iv) the prediction tally behind Section 4's sentence. Ledger keys `AUX-R123-*`. Tools: `reviews/v21/tools/ledger_r123_tables.py` (every table from its artifact), `reach_rows_r123.py`, `r123_apply.py` (every edit asserted).

## AUX-R123-SPEC-FREEZE

The author's brief (pasted 2026-09-19, "Knowing the Store: v21 update and writing pass") and its amendments ("Amendments to the update-and-writing-pass brief, from R122's final report"), applied as received; the fallback build tagged `fallback/v21-pre-pass` at `61b0bd8` before any edit.

## AUX-R123-PRINTED — two-decimal forms new to the body, with their sources

| printed (where) | value | source key (file) |
|---|---|---|
| $0.35$ to $0.44$ (Section 5, the crossover: same-store AUROC on supersession under the main-study rubric, the four models that do not condition on intent) | GPT-5.6 Luna 0.3467, Haiku 4.5 0.3765, GPT-4.1 mini 0.3973, GPT-5.6 Sol 0.4406 | AUX-CF2-IX-LUNA-A-P0, -H45-A-P0, -MINI-A-P0, -SOL-A-P0 (r82_counterfactual/cf2/NUMBERS_CF2.md §14d) |
| $0.90$, $0.85$ (Section 5: Opus 5 same-store, population A and B, main-study rubric) | 0.8966; 0.8484 | AUX-CF2-IX-OP5-A-P0, -OP5-B-P0 |
| $0.64$ (Section 5: GPT-5.6 Sol on expiry, main-study rubric) | 0.6354 | AUX-CF2-IX-SOL-B-P0 |
| $0.99$, $0.96$, $0.88$ (Section 5: Opus 5, GPT-5.6 Luna at draw 1, GPT-5.6 Sol, intent-explicit rubric, population A) | 0.9885; 0.9640 (draw 1; five-draw mean 0.9836); 0.8815 | AUX-CF2-IX-OP5-A-P1, -LUNA-A-P1 (the draw-1 comparable column), -SOL-A-P1 |
| $0.99$ (Section 5: the fixed cue list, population A) | 0.9943 | AUX-CF2-IX-LOOKUPS, keyword A |
| $0.48$, $0.55$ (Section 5: GPT-4.1 mini, Haiku 4.5 under the intent-explicit rubric, population A) | 0.4789; 0.5483 (five-draw mean; draw 1 0.5464) | AUX-CF2-IX-MINI-A-P1, -H45-A-P1 |
| $9$ of $11$, $76/0/11$ (Section 5: GPT-5.6 Sol's losses under the intent-explicit rubric) | within-pair counts 76/0/11; 9 losses with both questions at 0.96 or higher | AUX-CF2-IX-SOL-A-P1 and the losses list of §14d (14d-interim-3, the author's correction) |
| $0.47$, $0.45$ (Section 5: the name lookup, populations A and B) | 0.4739; 0.4527 | AUX-CF2-IX-LOOKUPS, name A / B; AUX-CF2-IX-P-I3 |
| $0.05$, $0.17$ (Section 5: the largest fall and rise on the original questions under the intent-explicit rubric) | Haiku 4.5 A −0.0458; GPT-4.1 mini B +0.1716 | AUX-CF2-IX-P-I5 |
| $0.02$, $+0.09$ (Limitations: GPT-5.6 Luna and GPT-4.1 mini under the intent-explicit rubric on the counterfactual set; Luna's margin over the lookup) | Luna +0.0113 and mini +0.0085 from their recorded rows (0.8531 against 0.8417; 0.7253 against 0.7167); Luna minus the lookup +0.0867 [+0.0447, +0.1302]; [+0.0562, +0.1219] | AUX-R122-P1-DELTA, AUX-R122-P1-P-R1, AUX-R122-P1-P-R3 (reviews/r122/NUMBERS_R122.md) |
| $0.76$, $[0.72,0.80]$, $0.74$, $100/15/33$ and $0.83$, $[0.79,0.87]$, $0.83$, $130/5/13$ (Table 1: GPT-4.1 mini at five draws, default and all-states summary); $0.72$, $0.80$ (the note: the recorded one-draw rows) | 0.7648 [0.7218, 0.8047], PN vs PRESENT 0.7394, W/T/L 100/15/33; 0.8323 [0.7889, 0.8725], 0.8307, 130/5/13; recorded 0.7167, 0.7967 | AUX-R122-K5-ROWS |
| $0.76$, $0.83$, $51$ to $6$ (Appendix C.2: the five-draw sentence) | as above; tied triples 51 → 6 under the default summary | AUX-R122-K5-ROWS, AUX-R122-K5-P-K1 |
| $0.76$, $0.76$, $0.01$, $0.60$ (Appendix C.2: the two further encoders and the random-token control on the counterfactual set, default summary) | all-mpnet-base-v2 0.7605 (−0.0059 from MiniLM), bge-small-en-v1.5 0.7584 (−0.0080); random tokens under MiniLM 0.5954 | AUX-R122-ENC-ROWS, AUX-R122-ENC-RANDOM |
| $5.43$, $7.08$, $6.51$, $1.20$, $26$ (Appendix E.10 and the Section 9 reach table: the model rule's mean view over the 661 and over the 104; the ungated fetch's lines and ratio; the retraction obligations the recency-aware view misses) | 5.4342; 7.0769; 6.5129; 1.1985; 0 of 26 | AUX-R122-GATE-ROWS, AUX-R122-GATE-MATCHED, AUX-R122-GATE-PREDICTIONS; AUX-R123-REACH-ROWS below |
| $0.82$, $0.52$, $0.54$, $0.23$, $0.95$, $0.37$, $0.39$, $0.29$, $0.34$ (the Section 9 reach table's rates) | always-open fetch matched 0.8164; top-five 0.5192; similarity matched 0.5443; recency matched 0.2337; oracle 0.9519; licensed record in view 65 of 174 = 0.3736 (every recorded policy), matched rows 0.3910 / 0.2916 / 0.3361 | AUX-R122-GATE-MATCHED; AUX-R123-REACH-ROWS |
| $5.53$, $6.39$ (Appendix E.10, tab:gatereach: the always-open fetch at four similarity lines, mean lines over the 661; the five-line form's mean lines over the 104) | 5.5280; 6.3942 | AUX-R122-GATE-ROWS (reviews/r122/results/gate_reach.json rows/AF/4/lines/mean_661, rows/AF/5/lines/mean_104) |
| $90$, $27$ (Section 4: the prediction count) | AUX-R123-TALLY below | this file |

## AUX-R123-SUP-MARGINS — each model's supersession-only margin over the name lookup on the counterfactual set (tab:sup-margins; the amendment's recomputation)

Source: `reviews/r117/results/sup_margins.json` (reviews/r117/tools/sup_margins.py: the recorded INDEXED-V2 rows through r82_counterfactual/tools/cf2_reader_score.py, score_lane, 1,000 paired draws, seed 42; the whole-set AUROC of each model asserted against its recorded value) and, for the five-draw row, `reviews/r122/results/scores_r122_oai.json` T3 INDEXED-V2 `new.per_state.SUPERSESSION.vs_lookup` (the same scorer on the five-draw rows). The lookup reads 0.9223 on the 88 supersession pairs (264 items).

| model | whole set | supersession | minus the lookup | item interval | persona interval | both exclude zero |
|---|---:|---:|---:|---|---|---|
| GPT-4.1 mini, one draw (recorded) | 0.7167 | 0.8308 | −0.0915 | [−0.1399, −0.0478] | [−0.1436, −0.0425] | yes |
| GPT-4.1 mini, five draws (provider default; R122 T3) | 0.7648 | 0.8793 | −0.0429 | [−0.0898, +0.0006] | [−0.1001, +0.0035] | no |
| Haiku 4.5 (five draws) | 0.7566 | 0.8876 | −0.0347 | [−0.0813, +0.0086] | [−0.0809, +0.0066] | no |
| Opus 5 (five draws) | 0.8405 | 0.9325 | +0.0102 | [−0.0183, +0.0392] | [−0.0259, +0.0432] | no |
| GPT-5.6 Sol (five draws) | 0.8500 | 0.9383 | +0.0161 | [−0.0130, +0.0473] | [−0.0202, +0.0478] | no |
| GPT-5.6 Luna (five draws) | 0.8417 | 0.9426 | +0.0204 | [−0.0053, +0.0473] | [−0.0056, +0.0451] | no |

**Amendment 2's case: at five draws GPT-4.1 mini is no longer reliably below the lookup on supersession** (both intervals include zero), so the clause "and GPT-4.1 mini falls below it" is not in the abstract, Section 5 reads "no model reliably exceeds the name lookup on supersession", and the per-model margins print in tab:sup-margins only. At five draws the whole-set margin is −0.0016 [−0.0426, +0.0393]; [−0.0415, +0.0328] (AUX-R122-K5-ROWS).

## AUX-R123-REACH-ROWS — the recorded downstream policies' reach rows (the Section 9 reach table; `reviews/v21/results/reach_rows_r123.json`, `reviews/v21/tools/reach_rows_r123.py`)

Source: `ds_downstream/stage1.json` per_item (view_size, reach, gold_in_view), the recorded downstream record; no model call, nothing re-run. The model rule reproduces AUX-DS-REACH (85 of 104), AUX-DS-PRESENT (65 of 174) and R122's target mean over the 661 (5.4342, AUX-R122-GATE-MATCHED); the top-five view reproduces 54 of 104 and 5.00 lines.

| policy | forbidding record in view (of 104) | rate | licensed record in view (of 174) | rate | mean lines, 661 | mean lines, 104 |
|---|---:|---:|---:|---:|---:|---:|
| top-five retrieval (ALWAYS) | 54 | 0.5192 | 65 | 0.3736 | 5.0000 | 5.0000 |
| lookup rule (LOOKUP) | 85 | 0.8173 | 65 | 0.3736 | 5.4569 | 6.8750 |
| model rule (MODEL) | 85 | 0.8173 | 65 | 0.3736 | 5.4342 | 7.0769 |
| oracle (ORACLE) | 99 | 0.9519 | 65 | 0.3736 | 5.3253 | 7.0673 |

**The two denominators reconciled.** The earlier Section 9's "about seven records" was the mean view over the 104 obligations alone (7.08 for the model rule; tab:ds-body-lower's column); R122's 5.43 is the mean over all 661 questions, the budget its matched rows share. The reach table prints the 661 mean and its caption states both.

## AUX-R123-TALLY — the prediction count (Section 4; Appendix F's count paragraph)

A prediction counts when it was registered with a bar, whether it held, failed or could not be evaluated (the R101 precedent: R82-CAL's undefined second prediction and the frontier addendum's descriptive third were in the 47); readings registered as descriptive are not counted (the R121 held text's rule for P-I4 and P-I5); the pending answer-stage predictions of Graphiti Amendment 2 and the moved-count control's second amendment (E9, scored but not landed) are not yet in the count.

| table | registrations and their predictions (came out otherwise in parentheses) | predictions | otherwise |
|---|---|---:|---:|
| tab:registrations (the R101 count) | E0 2; E1 4; frontier 3; ladder 5 (1); NOK-factorial 3 (1); E1-XV 4 (1); E1-QP 2 (1); X4 5; X5 2 (1); R77 2 (1); NB-6 2 (1); R82-CF 4 (1); R82-CAL 2 (one undefined); CF-2 5; SIDE S1 2 | 47 | 8 |
| tab:registrations-b | RESP 6 (5); DS 5 (3); DS Amendment 4 2; Graphiti forty personas 4 (2: P1 on recall, P3) | 17 | 10 |
| tab:registrations-c | twelve descriptive registrations | 0 | 0 |
| tab:registrations-d | Graphiti trial readings GR-1 (1), GR-2 (not computable), GR-3: 3 (1); moved-count Amendment 1 P-M1 1; names against counts P-N1, P-N2 2; marker ablation P-X2 1 (1, on Mem0); DS Amendment 8 P-L1 to P-L5 5 (3; P-L4 not defined); Sol and Luna P-S1, P-S2 2 (1); intent crossover P-I1, P-I2, P-I3 3 (2); Amendment 1 P-I2b 1; encoders P-E1 1; mini at five draws P-K1 1; intent-explicit rubric P-R1, P-R2, P-R3 3 (1); gate reach P-G1 to P-G3 3 | 26 | 9 |
| **total** | | **90** | **27** |

Before this pass the sentence read 58 / 16 (R101, 2026-09-13: 47 + 6 RESP + 5 DS; 8 + 5 + 3).

## AUX-R123-REFS — the three references added to Related Work (Phase D), each verified against its Crossref DOI record on 2026-09-19

| key | reference as printed | verified against |
|---|---|---|
| doyle1979 | J. Doyle. A truth maintenance system. Artificial Intelligence, 12(3):231–272, 1979. | Crossref DOI 10.1016/0004-3702(79)90008-0 (title, author, journal, volume 12, issue 3, pages 231-272, year 1979 as given) |
| snodgrass1986 | R. Snodgrass and I. Ahn. Temporal databases. Computer, 19(9):35–42, 1986. | Crossref DOI 10.1109/MC.1986.1663327 (title "Temporal Databases", authors Snodgrass and Ahn, Computer 19(9):35-42, 1986); the 1985 SIGMOD taxonomy paper (DOI 10.1145/318898.318921) was not used because Crossref records its title as "A taxonomy of time databases" |
| shapiro2011 | M. Shapiro, N. Preguiça, C. Baquero, and M. Zawirski. Conflict-free replicated data types. In SSS 2011, LNCS, pages 386–400. Springer, 2011. | Crossref DOI 10.1007/978-3-642-24550-3_29 (title, four authors, container "Stabilization, Safety, and Security of Distributed Systems", LNCS, pages 386-400, Springer, 2011) |

STALE's write-side component, read from its arXiv abstract (2605.06527) on 2026-09-19: "we further present CUPMem, a prototype that strengthens write-time revision through structured state consolidation and propagation-aware search"; the Related Work sentence engages it in those terms.
