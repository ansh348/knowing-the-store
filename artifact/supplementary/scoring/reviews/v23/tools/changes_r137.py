# -*- coding: utf-8 -*-
"""changes_r137.py -- reviews/v23/OLD_BESIDE_NEW_R137.md, the sign-off file of the R137 pass (the brief, section 8; the R135 tool retargeted): every changed sentence of the
main text (the abstract through the builders box), old beside new, grouped by section, with the swap or rule that caused it. Read from
reviews/v23/results/port_r137_log.json (every edit port_r137.py made, with its unit, section and note): each edit's old and new texts are split into
sentences (q_scan's splitter, a bold run-in lead being its own sentence) and aligned with difflib; unchanged sentences are dropped, a replaced run is one
row (its old sentences beside its new ones), an insertion or deletion a row with one side empty. Appendix edits are listed in a last section.
Usage: python reviews/v23/tools/changes_r137.py
"""
from __future__ import annotations

import difflib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
V23 = ROOT / "reviews" / "v23"
sys.path.insert(0, str(V23 / "tools"))
import q_scan as Q  # noqa: E402

LOG = V23 / "results" / "port_r137_log.json"
OUT = V23 / "OLD_BESIDE_NEW_R137.md"
CAUSE = {"numbers": "sections 2 and 3.1 (the pipeline, tab:robust row 9, the recount)", "appendix": "section 4 (the appendix homes)", "main": "sections 3.2, 3.4, 3.5, 3.6 (the main text)",
         "abstract": "section 3.3 (the abstract, verbatim)", "partb": "section 5 (Part B: Figure 1, the thesis sentences, Table 1)", "p1": "section 6, payer P1", "p2": "section 6, payer P2", "p3": "section 6, payer P3 (nothing cut)", "p4": "section 6, payer P4 (nothing cut)"}


def sentences(text):
    text = "\n".join(l for l in text.replace("\r\n", "\n").split("\n") if not l.lstrip().startswith("%"))
    text = re.sub(r"\s+", " ", text).strip()
    return [s.strip() for s in re.split(r"(?:(?<=[.!?])|(?<=[.!?]\}))\s+(?=[A-Z\\$(`])", text) if s.strip()]


def cell(s):
    return s.replace("|", "\\|").replace("\n", " ")


def main():
    log = json.loads(LOG.read_text(encoding="utf-8"))
    rows = {}
    n_rows = 0
    for e in log["edits"]:
        old, new = sentences(e["old"]), sentences(e["new"])
        sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
        pairs = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            pairs.append((" ".join(old[i1:i2]), " ".join(new[j1:j2])))
        if not pairs:
            continue
        key = e["file"] + " / " + e["section"]
        cause = f"{e['note']} [{CAUSE.get(e['unit'], e['unit'])}]"
        for o, n in pairs:
            rows.setdefault(key, []).append((o, n, cause))
            n_rows += 1
    order = ["abstract / the abstract", "body / 3, the evidence box", "body / 4, the readers paragraph", "body / 5.1, the second paragraph", "body / 5.1, the third paragraph", "body / 5.2, the opening paragraph", "body / 5.2, the two absorbed paragraphs", "body / 5.2, the rewording paragraph", "body / 7, the propagation paragraph", "body / the builders box", "body / 5.1", "body / 5.1 (Table 1)", "body / 5.2", "body / 5.3", "body / 6", "body / 6 (Table 2)", "body / 7", "body / 8", "body / 9", "body / 10"]
    keys = [k for k in order if k in rows] + [k for k in rows if k not in order and k.startswith("body")] + [k for k in rows if k.startswith("appendix")]
    L = ["# OLD_BESIDE_NEW_R137.md: every changed sentence of the main text, old beside new (R137, 2026-09-22)", "",
         "Written by `reviews/v23/tools/changes_r137.py` from `reviews/v23/results/port_r137_log.json` (every edit of `port_r137.py`, in the units' order; Figure 1 appears as its whole old and new source; the robust_table caption edit of P1 is listed under its own file). A row is a replaced run of "
         "sentences (old beside new), an inserted sentence (old empty) or a deleted one (new empty); unchanged sentences are not shown. The third column is the edit's note and the brief's "
         "section that caused it. Comments and paragraph breaks are dropped; LaTeX is left as written. This file is what gets signed off. The appendix edits are the last section.", ""]
    for k in keys:
        L.append(f"## {k.replace('body / ', 'Section ').replace('abstract / ', '').replace('appendix / ', 'Appendix ')}")
        L.append("")
        L.append("| old | new | cause |")
        L.append("|---|---|---|")
        for o, n, c in rows[k]:
            L.append(f"| {cell(o)} | {cell(n)} | {cell(c)} |")
        L.append("")
    L.append(f"Rows: {n_rows}.")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"-> {OUT} ({n_rows} rows over {len(keys)} sections)")


if __name__ == "__main__":
    main()
