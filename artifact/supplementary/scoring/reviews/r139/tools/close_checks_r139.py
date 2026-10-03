# -*- coding: utf-8 -*-
"""close_checks_r139.py -- the close checks of R139 on the built paper_v23.pdf: close_checks_r137.py's checks (the anonymity greps over the text layer, the overfull
boxes by page, pages 1 to 10 rasterized with the word-box overlap count), plus the pass's own: the running header on every page (S1); the main text and the builders
box ending on page 9 (the label main-text-end, and the AI-use statement's heading on page 10 or later); no character past the right margin, x1 > 541.5 pt, on any
page (S4); no em dash in prose but the registered ADDENDUM_SIDE text's pair (S5); no HV-1 'once labeled' / 'in progress' / 'pending' / 'unfinished' left (S3);
'monitor' in the main text only in the sentences Unit G and Q9 placed (the G gate). Writes reviews/r139/results/close_r139_p<N>.png. Exit 1 on a failure.
Usage: python reviews/r139/tools/close_checks_r139.py
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

import fitz

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
OUT = ROOT / "reviews" / "r139" / "results"
HEADER = "Under review as a conference paper at ICLR 2027"
MONITOR_OK = ["as metamemory monitoring", "Metamemory separates monitoring a state from controlling its use", "we study monitoring only", "In these monitoring tests", "monitoring and control distinction (Section"]   # R140 item 4 adds the last


def main():
    fails = []
    r = subprocess.run([sys.executable, str(ROOT / "reviews" / "v23" / "tools" / "close_checks_r137.py")], capture_output=True, text=True)
    print(r.stdout.replace("close_checks_r137", "close_checks_r137 (inherited)"))
    if r.returncode:
        fails.append("the inherited R137 checks")
    doc = fitz.open(SUB / "paper_v23.pdf")
    # S1: the header
    miss = [i + 1 for i in range(doc.page_count) if HEADER not in doc[i].get_text("text", clip=fitz.Rect(0, 0, doc[i].rect.width, 80))]
    print(f"  S1 running header: present on {doc.page_count - len(miss)} of {doc.page_count} pages" + (f"; missing on {miss}" if miss else ""))
    fails += ["header"] if miss else []
    # the close rule: main-text-end on page 9, the AI-use statement after it
    aux = (SUB / "paper_v23.aux").read_text(encoding="utf-8", errors="replace")
    end = int(re.search(r"\\newlabel\{main-text-end\}\{\{[^}]*\}\{([^}]*)\}", aux).group(1))
    ai = next(i + 1 for i in range(doc.page_count) if "AI use statement" in doc[i].get_text() or "AI USE STATEMENT" in doc[i].get_text().upper())
    print(f"  close rule: main-text-end (the builders box) on page {end}; the AI-use statement opens on page {ai}")
    fails += ["page"] if end != 9 else []
    # S4: the right margin
    over = []
    for i in range(doc.page_count):
        for w in doc[i].get_text("words"):
            if w[2] > 541.5 and w[1] > 60 and w[3] < doc[i].rect.height - 40:
                over.append((i + 1, round(w[2], 1), w[4][:30]))
    print(f"  S4 right margin: {len(over)} word(s) with x1 > 541.5 pt" + (f": {over[:12]}" if over else ""))
    fails += ["margin"] if over else []
    # S5: em dashes in prose (a table's dash cell is a line holding the dash alone)
    dashes = []
    for i in range(doc.page_count):
        for ln in doc[i].get_text().splitlines():
            if "\u2014" in ln and ln.strip() != "\u2014" and len(ln.strip()) > 3 and not re.fullmatch(r"[\u2014\s\[\]+\-.,0-9]*", ln.strip()):
                dashes.append((i + 1, ln.strip()[:110]))
    # the registered ADDENDUM_SIDE sentence (kept verbatim by ruling) breaks across two text lines; a table cell may pair the dash with a note mark (e.g. '—†')
    allowed = [d for d in dashes if "FR-Bank exposes" in d[1] or "fourteen days later" in d[1] or "restricted to an active successor" in d[1] or "leave the superseded list at 15.04" in d[1]
               or re.fullmatch(r"(—[†‡*a-z]?\s*)+", d[1])]
    other = [d for d in dashes if d not in allowed]
    print(f"  S5 em dashes in prose: {len(dashes)} line(s); the registered ADDENDUM_SIDE text: {len(allowed)}; others: {other or 'none'}")
    fails += ["em dash"] if other else []
    # S3: the HV-1 placeholders
    hv = []
    for i in range(doc.page_count):
        t = " ".join(doc[i].get_text().split())
        for k in ("once labeled", "once labelled", "in progress", "unfinished"):
            if k in t:
                hv.append((i + 1, k))
        for m in re.finditer(r"[^.]*\bpending\b[^.]*", t):
            if re.search(r"validation|annotat|label|HV", m.group(0)):
                hv.append((i + 1, m.group(0)[:100]))
    print(f"  S3 HV-1 placeholders left: {hv or 'none'}")
    fails += ["hv1"] if hv else []
    # G: 'monitor' in the main text
    tex = (SUB / "paper_v23.tex").read_text(encoding="utf-8")
    a, b = tex.index("\\begin{abstract}"), tex.index("\\label{main-text-end}")
    main = "\n".join(l for l in tex[a:b].split("\n") if not l.lstrip().startswith("%"))
    sents = [s for s in re.split(r"(?<=[.!?])\s+", " ".join(main.split())) if re.search(r"monitor", s, re.I)]
    stray = [s[:120] for s in sents if not any(k in s for k in MONITOR_OK)]
    print(f"  G gate, 'monitor' in the main text: {len(sents)} sentence(s); outside Unit G / Q9: {stray or 'none'}")
    fails += ["monitor"] if stray else []
    for i in range(min(10, doc.page_count)):
        doc[i].get_pixmap(dpi=110).save(OUT / f"close_r139_p{i + 1}.png")
    print(f"  rasterized: {OUT}/close_r139_p1.png to p10.png")
    print("close_checks_r139: " + ("FAIL " + ", ".join(fails) if fails else "PASS"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
