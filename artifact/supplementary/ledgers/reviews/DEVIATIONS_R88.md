# DEVIATIONS_R88 — R88-FRAME deviation ledger

Every departure from the R88-FRAME prompt, with a one-line reason. This program assigns only
`D-R88-n` identifiers.

Opened 2026-09-11 at Phase A; Phase B landed the same day in `paper_v3.tex`.

| ID | Phase | Deviation | Reason |
|---|---|---|---|
| **D-R88-1** | B | B3 reads "The lookup has one descriptive value on the 84-question set, none per state on the counterfactual set, and none on the one-voice set, so the comparison between model and lookup is complete only on the 661-question population." in place of the program's sentence, which said the lookup had "no rows on the 84-question set". | `e1r_robustness/results/nb6.json` (`matched_84_descriptive`, commit `40b0e7d`) and `NUMBERS_E1R.md` carry NB-6 = 0.6023 (TRUE) / 0.5563 (BELIEVED) on the 84-question cell; the 36-question cell has none. The program's C3 premise ("the one-voice cell already has 0.6023") was the same mislabel, which Appendix F.8 also carried and which this phase corrects. |
| **D-R88-2** | B | B1's fifth sentence ("On a store without that structure the lexical and embedding matchers sit at 0.5000 and the model's point estimates fall below it under the truthful summary (0.4777, 0.4526).") is not printed. | Page budget. Section 8's existing sentence states the inversion; the Table 19 caption (B2) now carries the point estimates. Measured: with the sentence the label sat on page 10. |
| **D-R88-3** | B | Cuts beyond the R87 Phase B list were needed to reach the slack floor after R87 Phase C landed: the §4.4 factorial effect sizes and matching sentence (R86_HEADROOM 3 and 4; Appendix F.6 keeps them), the contribution list printed inline, Table 2's caption tightened, R87's C16 and C25 paragraph breaks taken back, Figure 2's redundant in-plot note dropped. | The program's rule A2 assumed R87 Phase E items would be the first to go; none had landed. R87 Phase C cost 5 lines the R88 A2 measurement (taken before Phase C) did not include. Each cut is recorded in the CLAIMS.md R88 block; the factorial one is a strength reduction at its site with the values byte-identical in Appendix F.6. |
| **D-R88-4** | B | B4 (the optional §1 extension "and what the model adds beyond that match is the question the study answers") does not land. | The program allowed it only if it cost no line; slack is exactly the floor. |
| **D-R88-5** | C | Phase C did not run. | Optional and time-boxed; C1 is a transcription (the 0.6023 value already in the ledger), C2 and C3 would be new local computations. Nothing reverts because nothing started. |
| **D-R88-6** | B | Figure 2 was measured at 0.17 of the text width and returned to 0.20. | At 0.17 the legend covered the 0.5000 label and the in-plot note overlapped the indexed line. |
