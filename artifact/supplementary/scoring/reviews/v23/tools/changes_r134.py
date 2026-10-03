# -*- coding: utf-8 -*-
"""changes_r134.py -- reviews/v23/OLD_BESIDE_NEW_R134.md, the sign-off file of the R134 pass (the brief, section 9; the R133 tool retargeted): every changed sentence of the
main text (the abstract through the builders box), old beside new, grouped by section, with the swap or rule that caused it. Read from
reviews/v23/results/port_r134_log.json (every edit port_r134.py made, with its unit, section and note): each edit's old and new texts are split into
sentences (q_scan's splitter, a bold run-in lead being its own sentence) and aligned with difflib; unchanged sentences are dropped, a replaced run is one
row (its old sentences beside its new ones), an insertion or deletion a row with one side empty. Appendix edits are listed in a last section.
Usage: python reviews/v23/tools/changes_r134.py
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

LOG = V23 / "results" / "port_r134_log.json"
OUT = V23 / "OLD_BESIDE_NEW_R134.md"
CAUSE = {"appendix": "section 5 (the appendix)", "main": "section 4 (the main text)", "main_short": "section 4.2 (the shorter paragraph)", "abstract": "the author's abstract (the ruling superseding 4.3)",
         "partb": "section 6 (Part B) and the author's addition (the crossover sentence)", "payers": "RULING 3 (the payers P1 to P5; the 5.1 range)"}


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
    order = ["abstract / the abstract", "body / 1", "body / 1, the second contribution", "body / 2, Related work", "body / 4", "body / 4, the models paragraph", "body / 4, Labels and summaries", "body / 5.1", "body / 5.1 (Table 1)", "body / 5.2", "body / 5.3", "body / 6", "body / 6 (Table 2)", "body / 7", "body / 8", "body / 9", "body / 10"]
    keys = [k for k in order if k in rows] + [k for k in rows if k not in order and k.startswith("body")] + [k for k in rows if k.startswith("appendix")]
    L = ["# OLD_BESIDE_NEW_R134.md: every changed sentence of the main text, old beside new (R134, 2026-09-21)", "",
         "Written by `reviews/v23/tools/changes_r134.py` from `reviews/v23/results/port_r134_log.json` (every edit of `port_r134.py`, in the units' order; the 4.1 paragraph appears as inserted by unit main and replaced by unit main_short, and RULING 2's Conclusion sentence as inserted by unit main and replaced by RULING 3's P4). A row is a replaced run of "
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
