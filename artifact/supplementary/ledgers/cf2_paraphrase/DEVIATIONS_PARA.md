# DEVIATIONS_PARA: settled readings and deviations for the paraphrase check (ADDENDUM_PARA)

Registration `registrations/ADDENDUM_PARA.md`, registered text sha256
`45cad63d...` (the bytes above the marker line; the author's rulings of 2026-09-14 are appended below it), frozen at
`dab8956` on 2026-09-14. Every entry below was written before the first scoring call of the item it concerns, with the
direction it moves stated.

| id | recorded | what | direction |
|---|---|---|---|
| **D-PARA-1** | 2026-09-14, before any scoring call (the author's note on the Phase 1 report of CC_PASS_v18) | Opus 5 runs at k = 1 (the author's ruling (ii) of 2026-09-14, already in `score_para.py`), and its single paraphrase draw is paired against **draw 1 of the recorded CF-2 Opus 5 rows** (`r82_counterfactual/cf2/rows/rows_OP5.jsonl`, `draw == 1`) rather than against the five-draw mean the registration's collapse (`score_cf.load_lane`) would supply, so both sides of the paired paraphrase-minus-original difference are single calls at the same setting. The loader is re-pointed for the OP5 code only in `reviews/v18/paraphrase_score.py` (`load_lane_opus_draw1`); `score_para.py` is not edited; GPT-4.1 mini and Haiku 4.5 are scored as frozen. Basis: A3 of the Phase 1 report (`reviews/NUMBERS_R110.md` AUX-R110-A3): on the counterfactual set Opus 5's draw 1 alone reads 0.8400 (53 distinct values) against the five-draw mean 0.8405, a per-draw spread of 0.0059, and keeps its margin over the superseded-names lookup (+0.0736, item [+0.0298, +0.1223], persona [+0.0388, +0.1129]). The `para_scores.json` row for OP5 carries `original_side` and the deviation id. | Removes the draw-count asymmetry (k = 1 against k = 5) from the Opus row; the original side's AUROC moves from 0.8405 to 0.8400 on the full set and its paired interval widens by the single draw's noise. Neither favours the paraphrase side. |
