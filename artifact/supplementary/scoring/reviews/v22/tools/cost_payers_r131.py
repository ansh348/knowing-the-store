# -*- coding: utf-8 -*-
"""cost_payers_r131.py -- the costed table of R131 (2026-09-20) in lines of slack, the instrument of cost_payers_r129d.py: the fine number is not linear
under flushbottom (the builders box is one unbreakable minipage), so each variant is measured by the largest k such that \\vspace{k\\baselineskip}
inserted before the box still leaves it on page 9 (positive slack), or the smallest k such that \\vspace{-k\\baselineskip} brings it back (a deficit,
printed negative), found by bisection over k in [1, 24]. Variants: the landing with no payer, each payer of the brief's section H alone, and the
payers cumulatively in the brief's order. Scratch builds only; the body is regenerated (port_v22.py + port_r131.py --payers=<final>) at the end.
Usage: python reviews/v22/tools/cost_payers_r131.py [--final=1,2,3,4] [--only=<payers of one variant>]   (one variant per call fits the harness's ten-minute cap; merge_cost_r131.py joins the parts)
"""
from __future__ import annotations

import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "reviews" / "v22" / "tools"
BODY = ROOT / "reviews" / "v22" / "src" / "body_v22.tex"
OUT = ROOT / "reviews" / "v22" / "results" / "cost_payers_r131.md"
sys.path.insert(0, str(TOOLS))
from cost_payers_r129 import fine  # noqa: E402

ANCHOR = "%% R126: the box as in the inbox (the R124-F wording)"
MAXK = 24


def regen(payers):
    subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
    subprocess.run([sys.executable, str(TOOLS / "port_r131.py"), f"--payers={payers}"], check=True, capture_output=True)
    return BODY.read_text(encoding="utf-8")


ANCHOR_NEG = "\\section{Conclusion}\\label{sec:conclusion}"


def fits(text, k):
    """k > 0: k baselines added before the box (does the box stay on page 9?); k < 0: k baselines removed before the Conclusion heading, which sits on
    page 9 (a negative space before the box would sit on page 10 once the box has moved there and be discarded at the page top; R129's case differed,
    its box alone spilled). Emulates deleting k lines of page 9's text."""
    assert text.count(ANCHOR) == 1 and text.count(ANCHOR_NEG) == 1
    if k > 0:
        t = text.replace(ANCHOR, f"\\vspace{{{k}\\baselineskip}}\n" + ANCHOR)
    elif k < 0:
        t = text.replace(ANCHOR_NEG, f"\\vspace{{{k}\\baselineskip}}\n" + ANCHOR_NEG)
    else:
        t = text
    BODY.write_text(t, encoding="utf-8", newline="\n")
    p, f = fine()
    return p == 9 and f <= 485, p, f


def slack(text, log):
    ok, p, f = fits(text, 0)
    log.append(f"k=0: page {p}, fine {f}")
    if ok:
        lo, hi = 0, MAXK + 1          # the largest k that fits, in [lo, hi)
        while hi - lo > 1:
            mid = (lo + hi) // 2
            ok, p, f = fits(text, mid); log.append(f"k=+{mid}: page {p}, fine {f}")
            lo, hi = (mid, hi) if ok else (lo, mid)
        return lo
    lo, hi = 0, MAXK                  # the smallest k that fits, in (lo, hi]
    ok, p, f = fits(text, -MAXK); log.append(f"k=-{MAXK}: page {p}, fine {f}")
    if not ok:
        return -MAXK - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        ok, p, f = fits(text, -mid); log.append(f"k=-{mid}: page {p}, fine {f}")
        lo, hi = (lo, mid) if ok else (mid, hi)
    return -hi


def main():
    final = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--final=")), "1,2,3,4")
    plan = [("the landing, no payer", ""), ("payer 1 alone (Section 7, the gating paragraph)", "1"), ("payer 2 alone (Section 7, the FR-Bank tags paragraph)", "2"),
            ("payer 3 alone (Related work, the last paragraph)", "3"), ("payer 4 alone (Section 3, the masking sentence)", "4"),
            ("payers 1 and 2", "1,2"), ("payers 1, 2 and 3", "1,2,3"), ("payers 1 to 4 (the landing as committed)", "1,2,3,4")]
    only = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--only=")), None)   # one variant per call (the harness caps a call at ten minutes)
    if only is not None:
        plan = [(l, p_) for l, p_ in plan if p_ == only]
        OUT_ = OUT.with_name(OUT.stem + f"_{only or 'none'}.md")
    else:
        OUT_ = OUT
    rows, logs = [], []
    t0 = time.time()
    try:
        for label, payers in plan:
            text = regen(payers)
            log = []
            s = slack(text, log)
            rows.append((label, s, log[0]))
            logs.append((label, log))
            print(f"| {label} | {s:+d} | {log[0]} |  ({time.time() - t0:.0f}s)", flush=True)
    finally:
        regen(final)
        subprocess.run([sys.executable, str(TOOLS / "build_v22.py")], check=True, capture_output=True)
    md = ["# The costed table of R131 (cost_payers_r131.py, 2026-09-20)\n\n",
          "Slack = the largest k such that k baselines added before the builders box still leave it on page 9; a negative value is the smallest k of baselines that must be removed before the box for it to return. "
          "The fine number itself is not linear (the box is one unbreakable minipage), so this is the instrument; the reading at k = 0 is beside each row.\n\n",
          "| variant (on the R129 close with the R131 landing) | slack in lines | the build at k = 0 |\n|---|---:|---|\n"]
    md += [f"| {label} | {s:+d} | {r0} |\n" for label, s, r0 in rows]
    md.append("\n## The probes\n\n")
    for label, log in logs:
        md.append(f"- {label}: " + "; ".join(log) + "\n")
    OUT_.write_text("".join(md), encoding="utf-8", newline="\n")
    print("->", OUT_)


if __name__ == "__main__":
    main()
