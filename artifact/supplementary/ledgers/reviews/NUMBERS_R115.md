# NUMBERS_R115.md — program R115 (2026-09-18): the author's "Knowing the Store" patch to paper_v19

No new measurement enters through this pass. Every numeral the patch brings into the main text is a two-decimal form of a value already ledgered elsewhere, and the registered texts printed in Appendix G.4 fill their placeholders from ledgered values; this file records each printed form beside its source key (the R102 / R111 precedent) and the pass's own bookkeeping. Ledger keys `AUX-R115-*`.

## AUX-R115-SPEC-FREEZE

`reviews/r115/PATCH_KTS.md` (the patch document as received on 2026-09-18, verbatim): sha256 `0283b8e05f576c5908a75c66a51aef1696c74a75a2f9ed405d8f1939e36692b3`, recorded before any edit. The rulings applied are listed at the head of `reviews/r115/tools/kts_patch.py` and in the CLAIMS.md R115 block.

## AUX-R115-PRINTED — printed forms new to the main text, with their sources

| printed (where) | value | source key (file) |
|---|---|---|
| $0.07$ (abstract, P1: Opus 5 minus the name lookup on the counterfactual set) | 0.8405 − 0.7663 = +0.0742; Table 1 prints 0.84 and 0.77 | AUX-CF2-OP5-V2 and AUX-CF2-NB6-V2 (r82_counterfactual/cf2/NUMBERS_CF2.md; reviews/NUMBERS_WP.md section 3 reproduces both); the two-decimal rows AUX-WP-PRINTED (reviews/NUMBERS_WP.md) |
| $-0.01$ (Section 6, P7: native tags minus untagged on Graphiti's five edges) | −0.0141, item [−0.0786, +0.0554], persona [−0.0613, +0.0325] | AUX-R85-G10-P4 (r85_graphiti/NUMBERS_R85.md) |
| $0.58$ (Section 7, P9: GPT-4.1 mini under the capped store-written Graphiti summary) | 0.5765 | AUX-R85-G10-P2 (r85_graphiti/NUMBERS_R85.md) |
| $0.74$ (Section 7, P9: GPT-4.1 mini under the ground-truth summary on the 323) | 0.7424 | AUX-R113-Z3-ROWS (reviews/NUMBERS_R113.md); INDEXED-TRUE on the 323 in AUX-R85-G10-P2's table |
| $0.68$ (Section 7, P9: the lookup over Graphiti's own superseded names) | 0.6780 | AUX-R85-G10-P3, AUX-R85-G10-GR (r85_graphiti/NUMBERS_R85.md) |
| $+0.10$ (Section 7, P9: the lookup minus the capped monitor) | +0.1014, item [+0.0102, +0.2086], persona [+0.0094, +0.1988] | AUX-R85-G10-GR, GR-3 (r85_graphiti/NUMBERS_R85.md) |
| $323$ (Section 7, P9: the full-store questions) | 323 (47 positive obligations) | AUX-R113-Z2 (reviews/NUMBERS_R113.md); r85_graphiti/g10/results/summary_g10.json population/n |
| "a gain over blind that includes zero" (Section 7, P9; ruling 3) | +0.0801, item [−0.0031, +0.1604], persona [+0.0027, +0.1624]; the weaker interval includes zero (GR-1 FAILS) | AUX-R85-G10-GR (r85_graphiti/NUMBERS_R85.md) |
| $13$ of $34$ (Section 7, unchanged wording) | 13 / 34 = 0.3824 on the FULL-variant obligations | AUX-R85-G10-CENSUS-FORBIDDING-FULL (r85_graphiti/NUMBERS_R85.md) |
| "Opus 5's first draw alone keeps that margin" (Section 5, P4) | first draw 0.8400, +0.0736 above the lookup, item [+0.0298, +0.1223], persona [+0.0388, +0.1129] | AUX-R110-A3 (reviews/NUMBERS_R110.md, the draw table and the printed-forms row 0.84 / +0.07) |
| "both intervals excluding zero" (Section 5, P5: Opus 5 on the moved-count control) | retraction 0.5872 → 0.4861 (−0.1011), expiry 0.6150 → 0.4914 (−0.1236); each interval excluding zero, reaching the band | AUX-V2RCAT-OP5 (r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md) |

## AUX-R115-TEXTS — the registered texts printed in Appendix G.4 with their placeholders filled

| text | placeholders filled | source key |
|---|---|---|
| GR-1 FAILS (registrations/ADDENDUM_R85_GRAPHITI.md section 7; tagged [MAIN], printed in G.4 under D-R115-1) | $D$ = +0.0801 | AUX-R85-G10-GR |
| GR-3 HOLDS (the same section) | $Y$ = 0.6780, $X$ = 0.5765 | AUX-R85-G10-GR |
| P2 HOLDS (registrations/ADDENDUM_R85_GRAPHITI_AMENDMENT_1.md section 5) | $G$ = 0.5765, $T$ = 0.7424, $D$ = −0.1659 (the ledger's fill), $I$ = [−0.2593, −0.0764] (the item-level paired interval P2's criterion names), $Y$ = 0.6780 | AUX-R85-G10-P2 |
| P3 FAILS (the same section) | $Y$ = 0.6780, $D$ = +0.1780 from chance (0.6780 − 0.5000; the one token new to the manuscript, dispositioned in NUMBER_MOVES_V19.md) | AUX-R85-G10-P3 |
| P4 HOLDS (the same section) | $T$ = 0.6854, $U$ = 0.6995 | AUX-R85-G10-P4 |

Numerals that leave the main text: $44$ and $14$ (P6; they stay in Limitations and Appendix C.2), one `1.0.5` (P9; Section 4 and Table 2 keep it). number_moves_wp after the pass: ADDED 302 (one new token, `+0.1780`, dispositioned), VANISHED 17, missing 0.

## AUX-R115-BIB — the bibliography

The carried block `%%V11:677-871%%` inlined into `reviews/v19/src/body_v19.tex`; the build before the deletion byte-identical to the marker build (paper_v19.tex sha256 `9c576608e812cd5d…` before and after the inlining). Nine `\bibitem`s no citation reaches removed (knowbutnotact, dunlosky2009, knowact, metcalfe1994, naeini2015, nosek2018, pineau2021, openaimemory, memgate); 63 → 54 bibitems; refcheck_v11 with the nine keys retired: PASS, 19/19 full-metadata records verified, 35 declared out of scope, 0 uncovered of 54.

## AUX-R115-PAGE — the page budget

| build | label page | page-census reading (485 = the boundary) | raggedbottom fine number | pages |
|---|---|---|---|---|
| before (gates_ckpt_pre_r115.txt, 2026-09-18) | 9 | 485 (+0) | 482 (+3); the AI-use statement on the next page | 57 |
| after (gates_r115.txt) | 9 | 482 (+3) | 480 (+5); the AI-use statement's heading on page 9 | 58 |

Word deltas (kts_patch.py --words; `\ref`, `\cite`, math as one word each): main text −2 words, appendix +272 words (the definitions and the five registered texts). The 58th page is Appendix G.4's growth; the first build of the day read 59 because the shorter bibliography had left page 16 mostly blank (deviation D6, Table tab:crossvendor-predictions placed [H] by `build_v19.py` REPAIRS_R115_BLOCK, returned the 17 September pagination of Appendices A to F).
