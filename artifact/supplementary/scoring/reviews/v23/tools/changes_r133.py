# -*- coding: utf-8 -*-
"""changes_r133.py -- reviews/v23/OLD_BESIDE_NEW_V23.md, the sign-off file of the R133 pass (the brief, section 11): every changed sentence of the
main text (the abstract through the builders box), old beside new, grouped by section, with the swap or rule that caused it. Read from
reviews/v23/results/port_r133_log.json (every edit port_r133.py made, with its unit, section and note): each edit's old and new texts are split into
sentences (q_scan's splitter, a bold run-in lead being its own sentence) and aligned with difflib; unchanged sentences are dropped, a replaced run is one
row (its old sentences beside its new ones), an insertion or deletion a row with one side empty. Appendix edits are listed in a last section.
Usage: python reviews/v23/tools/changes_r133.py
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

LOG = V23 / "results" / "port_r133_log.json"
OUT = V23 / "OLD_BESIDE_NEW_V23.md"
CAUSE = {"homes": "section 4 (the coverage homes)", "swaps": "section 5 (the author's swaps)", "s4": "section 6 (Section 4 rewritten; 4.2)", "s51": "sections 6 and 7 (Section 5.1 rewritten)",
         "s52": "sections 6 and 7 (Section 5.2 rewritten)", "s53": "section 6 (Section 5.3 rewritten; S10)", "s6": "section 6 (Section 6 rewritten)", "s7": "section 6 (Section 7 rewritten)",
         "s8": "section 6 (Section 8 rewritten)", "s12": "section 5, S12"}


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
    order = ["abstract / Abstract", "body / 1", "body / 4", "body / 5.1", "body / 5.1 (Table 1)", "body / 5.2", "body / 5.3", "body / 6", "body / 6 (Table 2)", "body / 7", "body / 8", "body / 9", "body / 10"]
    keys = [k for k in order if k in rows] + [k for k in rows if k not in order and k.startswith("body")] + [k for k in rows if k.startswith("appendix")]
    L = ["# OLD_BESIDE_NEW_V23.md: every changed sentence of the main text, old beside new (R133, 2026-09-21)", "",
         "Written by `reviews/v23/tools/changes_r133.py` from `reviews/v23/results/port_r133_log.json` (every edit of `port_r133.py`, in the units' order). A row is a replaced run of "
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
