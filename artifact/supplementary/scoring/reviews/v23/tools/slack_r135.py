# -*- coding: utf-8 -*-
"""slack_r135.py -- the slack probe of the R131 instrument on the v23 build under R135 (regenerating through port_r135.py, which regenerates the R134 close underneath): the largest k such that k baselines added before the
builders box still leave it on page 9 (a \\vspace{k\\baselineskip} before the box), or, when the box has already moved, the smallest k of baselines that
must be removed from page 9's text (the probe puts \\vspace{-k\\baselineskip} before the Conclusion heading) for it to return; bisection, one build per
probe, all in the foreground. The body is regenerated from the sources through port_r134.py with the units named, and left regenerated (no probe residue)
at the end. Appends a row to reviews/v23/results/slack_r134.md.
Usage: python reviews/v23/tools/slack_r135.py --units=<list> [--label="..."]   (the units of port_r135.py; the R134 close is regenerated underneath)
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "reviews" / "v23" / "tools"
SUB = ROOT / "iclr2027_monitoring_submission"
BODY = ROOT / "reviews" / "v23" / "src" / "body_v23.tex"
OUT = ROOT / "reviews" / "v23" / "results" / "slack_r135.md"
sys.path.insert(0, str(TOOLS))
from run_gates import pdflatex, raggedbottom_reading  # noqa: E402

ANCHOR = "%% R126: the box as in the inbox (the R124-F wording)"
ANCHOR_NEG = "\\section{Conclusion}\\label{sec:conclusion}"
MAXK = 24


def fine():
    r = subprocess.run([sys.executable, str(TOOLS / "build_v23.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-600:] + r.stderr[-600:]
    pdflatex("paper_v23", SUB)
    aux = (SUB / "paper_v23.aux").read_text(encoding="utf-8", errors="replace")
    page = int(re.search(r"\\newlabel\{main-text-end\}\{\{[^}]*\}\{([^}]*)\}", aux).group(1))
    f, _, _ = raggedbottom_reading()
    return page, f


def fits(text, k):
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
        lo, hi = 0, MAXK + 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            ok, p, f = fits(text, mid); log.append(f"k=+{mid}: page {p}, fine {f}")
            lo, hi = (mid, hi) if ok else (lo, mid)
        return lo
    lo, hi = 0, MAXK
    ok, p, f = fits(text, -MAXK); log.append(f"k=-{MAXK}: page {p}, fine {f}")
    if not ok:
        return -MAXK - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        ok, p, f = fits(text, -mid); log.append(f"k=-{mid}: page {p}, fine {f}")
        lo, hi = (lo, mid) if ok else (mid, hi)
    return -hi


def main():
    units = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--units=")), "")
    label = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--label=")), units)
    subprocess.run([sys.executable, str(TOOLS / "port_r135.py"), f"--units={units}"], check=True, capture_output=True)
    text = BODY.read_text(encoding="utf-8")
    log = []
    s = slack(text, log)
    subprocess.run([sys.executable, str(TOOLS / "port_r135.py"), f"--units={units}"], check=True, capture_output=True)   # no probe residue
    assert BODY.read_text(encoding="utf-8").count("vspace{-") == 0 and BODY.read_text(encoding="utf-8") == text
    fine()   # the build left as the sources say
    row = f"| {label} | {s:+d} | {log[0]} | {'; '.join(log[1:])} |\n"
    if not OUT.exists():
        OUT.write_text("# The slack probe on the v23 build (slack_r133.py; the R131 instrument)\n\nSlack = the largest k such that k baselines added before the builders box still leave it on page 9; "
                       "a negative value is the smallest k of baselines that must be removed from page 9's text for the box to return.\n\n| variant | slack | k = 0 | the probes |\n|---|---:|---|---|\n", encoding="utf-8", newline="\n")
    OUT.write_text(OUT.read_text(encoding="utf-8") + row, encoding="utf-8", newline="\n")
    print(row)


if __name__ == "__main__":
    main()
