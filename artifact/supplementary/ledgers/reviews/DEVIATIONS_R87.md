# DEVIATIONS_R87 — R87-READ deviation ledger

Every departure from the R87-READ prompt, with a one-line reason. This program assigns only
`D-R87-n` identifiers.

Opened 2026-09-11 at Phase A.

| ID | Phase | Deviation | Reason |
|---|---|---|---|
| **D-R87-1** | A | The Table 2 counted-states row is not wholly "transcribed from NUMBERS_R82": the GPT-4.1 mini pair (0.5578 / 0.6600) is in no ledger, so it is transcribed from the committed artifact `r82_counterfactual/results/cf_scores.json` (`lanes["gpt-4.1-mini"].cf3_counted`, commit `7e9ac39`) into `reviews/NUMBERS_R87.md`, which is registered in `trace_scan_v13.py`'s `LEDGERS`. | NUMBERS_R82 sections 7 and 9 carry only the Haiku 4.5 and Opus 5 pairs. Without a ledger row the trace gate reports two unaccounted tokens and the row cannot print. The R86 precedent (`reviews/NUMBERS_R86.md`) is a new ledger with the artifact, key, and commit stated; nothing is recomputed. The mini delta includes zero on both interval conventions, recorded there. Ruled by [AUTHOR-1] at planning on 2026-09-11. |
| **D-R87-2** | A | Contribution items (3) and (4) are each split at their comma-and into two sentences; the program gave each as one sentence. | `prose_scan`'s 40-word rule (S-rule L) flagged them at 44 and 43 words. No word changes beyond the period; the split was foreseen in the plan and costs no review line (reading 485 before and after). |
| **D-R87-3** | B | The B3 pilot sentence is split at its semicolon ("…not comparable with the main study. Its lesson was…"); the program gave it as one sentence. | `prose_scan`'s 40-word rule flagged it at 49 words. No word changes. |
| **D-R87-4** | B | Phase B lands in `paper_v3.tex`, not `paper_v2.tex`, and after R89 rather than before R88. | [AUTHOR-1]'s instruction on 2026-09-11: make a v3 by copying v2 and put every pending change (R87, R88, R90) in it. `paper_v2.tex` is frozen at `f4c5b2c`; the tools' default manuscript moved to v3. |
| **D-R87-5** | C | C14's merged mechanical-reader sentence keeps a period where the program's colon would have joined the two clauses. | The one-sentence form is 46 words and `prose_scan`'s 40-word rule fails it. Scope clause and margins are unchanged. |
