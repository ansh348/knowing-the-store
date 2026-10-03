# v23 (program R133): the lineage from the R131 close

Opened 2026-09-21 by `reviews/v23/tools/bump_v23.py` from `b3cc631` (paper_v22.tex as `reviews/v22/gates_r131_close_f.txt` records it: tex sha256
cb888cd665d0dc77, pdf sha256 ed94f96a82426be5, 83 pages, the main text ending on page 9). The base for frozen_diff, numeric_diff and appendix_identity is
`reviews/v23/base_tree.txt` (paper_v22.tex, paper_v22.pdf, SUPPLEMENT.tex; sha256 in `base_files_sha256.txt`); the program is R133 (CLAIMS.md R133 block);
the inherited number dispositions are `NUMBER_MOVES_V22_inherited.md` and the v23 ledger is `NUMBER_MOVES_V23.md`. The pass is the author's brief
'R133: V23 READABILITY PASS' (hedges to the appendix, claims narrowed, Sections 4 to 8 rewritten; no number changes, no new experiments, no API calls);
its edits are `reviews/v23/tools/port_r133.py` on the copied v22 sources. reviews/v22/ is never edited in place and is the fallback build.
