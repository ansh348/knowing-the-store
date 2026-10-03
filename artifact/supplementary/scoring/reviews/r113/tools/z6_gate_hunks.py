# -*- coding: utf-8 -*-
"""z6_gate_hunks.py -- the two gate-tool hunks of program R113 (2026-09-16), each with a dated header note, applied as asserted byte
edits that keep each file's line endings: (1) iclr2027_monitoring_submission/tools/trace_scan_v13.py LEDGERS gains reviews/NUMBERS_R113.md;
(2) reviews/v19/tools/number_moves_wp.py ADDED / VANISHED gain the R113 dispositions (the lexical rows' paired intervals in tab:pad, and
the single-arm interval bounds those rows no longer print). Idempotent. Run from the repository root.
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
TS = ROOT / "iclr2027_monitoring_submission" / "tools" / "trace_scan_v13.py"
NM = ROOT / "reviews" / "v19" / "tools" / "number_moves_wp.py"


def edit(path, old, new, tag):
    b = path.read_bytes(); nl = b"\r\n" if b"\r\n" in b else b"\n"
    if tag.encode() in b:
        print(f"{path.name}: already applied"); return
    o = old.replace("\n", nl.decode()).encode(); n = new.replace("\n", nl.decode()).encode()
    assert b.count(o) == 1, (path.name, b.count(o))
    path.write_bytes(b.replace(o, n))
    print(f"{path.name}: applied")


edit(TS,
     '    pathlib.Path("../r85_graphiti/NUMBERS_R85.md"),\n]\n',
     '    pathlib.Path("../r85_graphiti/NUMBERS_R85.md"),\n'
     '    # R113 (2026-09-16, the zero-cost audit pass): the lexical lookup\'s paired rows at 100 and 200 padded names (tab:pad) are read from\n'
     '    # R110\'s A4 artifact and ledgered in reviews/NUMBERS_R113.md (AUX-R113-PAD-LEX-PAIRED); the pass\'s other sections (AUX-R113-Z1 to -Z5)\n'
     '    # print nothing in the manuscript.\n'
     '    pathlib.Path("../reviews/NUMBERS_R113.md"),\n]\n',
     "R113 (2026-09-16, the zero-cost audit pass)")

edit(NM,
     '    "0.0230": "Appendix C.2, the largest move from the pooled AUROC to PN-vs-PRESENT over the whole set, any reader (reviews/NUMBERS_WP.md section 8, the printed-forms table)",\n}\n',
     '    "0.0230": "Appendix C.2, the largest move from the pooled AUROC to PN-vs-PRESENT over the whole set, any reader (reviews/NUMBERS_WP.md section 8, the printed-forms table)",\n'
     '    # R113 (2026-09-16, the zero-cost audit pass): tab:pad\'s lexical rows at 100 and 200 names print the paired difference against the committed\n'
     '    # list and both intervals, read from reviews/v18/results/a4_pad_extend.json and ledgered in reviews/NUMBERS_R113.md AUX-R113-PAD-LEX-PAIRED\n'
     '    "-0.0137": "tab:pad, the lexical lookup at 100 names minus the committed list (AUX-R113-PAD-LEX-PAIRED)",\n'
     '    "-0.0672": "tab:pad, the lexical lookup at 100 names, item-level interval, lower bound (AUX-R113-PAD-LEX-PAIRED)",\n'
     '    "+0.0369": "tab:pad, the lexical lookup at 100 names, item-level interval, upper bound (AUX-R113-PAD-LEX-PAIRED)",\n'
     '    "-0.0926": "tab:pad, the lexical lookup at 100 names, persona-clustered interval, lower bound (AUX-R113-PAD-LEX-PAIRED)",\n'
     '    "+0.0716": "tab:pad, the lexical lookup at 100 names, persona-clustered interval, upper bound (AUX-R113-PAD-LEX-PAIRED)",\n'
     '    "-0.0355": "tab:pad, the lexical lookup at 200 names minus the committed list (AUX-R113-PAD-LEX-PAIRED)",\n'
     '    "-0.0903": "tab:pad, the lexical lookup at 200 names, item-level interval, lower bound (AUX-R113-PAD-LEX-PAIRED)",\n'
     '    "+0.0189": "tab:pad, the lexical lookup at 200 names, item-level interval, upper bound (AUX-R113-PAD-LEX-PAIRED)",\n'
     '    "-0.1125": "tab:pad, the lexical lookup at 200 names, persona-clustered interval, lower bound (AUX-R113-PAD-LEX-PAIRED)",\n'
     '    "+0.0455": "tab:pad, the lexical lookup at 200 names, persona-clustered interval, upper bound (AUX-R113-PAD-LEX-PAIRED)",\n'
     '    "79": "tab:pad\'s caption, the summaries whose 100-name list draws on other personas\' names (79 of 242 keys; reviews/NUMBERS_R110.md AUX-R110-A4, AUX-R113-PAD-LEX-PAIRED)",\n'
     '    "242": "tab:pad\'s caption, the 242 summaries (index keys) of the 661 (AUX-R110-A4)",\n'
     '}\n',
     "R113 (2026-09-16, the zero-cost audit pass): tab:pad's lexical rows")

edit(NM,
     '    "0.90": "Section 7\'s lookup-halves interval [0.67,0.90] moved to Table tab:bh-split\'s pointer; AUX-BH-SPLIT",\n}\n',
     '    "0.90": "Section 7\'s lookup-halves interval [0.67,0.90] moved to Table tab:bh-split\'s pointer; AUX-BH-SPLIT",\n'
     '    # R113 (2026-09-16): the single-arm interval bounds tab:pad\'s lexical rows at 100 and 200 printed in the item-interval column, replaced by the\n'
     '    # paired difference and its intervals; the single-arm intervals stand in reviews/NUMBERS_R110.md AUX-R110-A4 (lex item 95%)\n'
     '    "0.5001": "tab:pad, the lexical lookup at 100 names, single-arm item interval lower bound, no longer printed (AUX-R110-A4 keeps it)",\n'
     '    "0.6162": "tab:pad, the lexical lookup at 100 names, single-arm item interval upper bound, no longer printed (AUX-R110-A4 keeps it)",\n'
     '    "0.4737": "tab:pad, the lexical lookup at 200 names, single-arm item interval lower bound, no longer printed (AUX-R110-A4 keeps it)",\n'
     '    "0.6006": "tab:pad, the lexical lookup at 200 names, single-arm item interval upper bound, no longer printed (AUX-R110-A4 keeps it)",\n'
     '}\n',
     "R113 (2026-09-16): the single-arm interval bounds")
print("done")
