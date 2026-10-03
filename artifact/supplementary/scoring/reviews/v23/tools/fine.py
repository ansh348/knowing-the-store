# -*- coding: utf-8 -*-
"""fine.py -- build paper_v23.tex, compile it three times and print the page-census reading and the raggedbottom fine number, nothing else
(the quick page-budget instrument of the integration pass; the gate battery is run_gates.py). Usage: python reviews/v19/tools/fine.py"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))
from run_gates import pdflatex, raggedbottom_reading  # noqa: E402


def main():
    r = subprocess.run([sys.executable, str(ROOT / "reviews" / "v23" / "tools" / "build_v23.py")], capture_output=True, text=True)
    if r.returncode:
        print(r.stdout[-800:], r.stderr[-800:]); sys.exit(1)
    pdflatex("paper_v23", SUB)
    aux = (SUB / "paper_v23.aux").read_text(encoding="utf-8", errors="replace")
    page = re.search(r"\\newlabel\{main-text-end\}\{\{[^}]*\}\{([^}]*)\}", aux).group(1)
    log = (SUB / "paper_v23.log").read_text(encoding="utf-8", errors="replace")
    over = log.count("Overfull"); undef = len(re.findall(r"Reference `", log))
    fine, rb_page, where = raggedbottom_reading()
    print(f"main-text-end page {page}; fine number {fine} against 485 ({485 - fine:+d}); raggedbottom label page {rb_page}, AI-use {where}; overfull {over}; undefined refs {undef}")


if __name__ == "__main__":
    main()
