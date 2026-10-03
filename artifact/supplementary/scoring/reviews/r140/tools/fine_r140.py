# -*- coding: utf-8 -*-
"""fine_r140.py -- one build and the fine number for a unit set of reviews/r139/tools/port_r139.py (the slack probe's k = 0 reading, without the bisection): regenerates the sources
through port_r139.py --units=<list>, builds, and prints the main text's last page and fine number (run_gates.raggedbottom_reading). One build in the foreground.
Usage: python reviews/r139/tools/fine_r140.py --units=<list>
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "reviews" / "v23" / "tools"
SUB = ROOT / "iclr2027_monitoring_submission"
sys.path.insert(0, str(TOOLS))
from run_gates import pdflatex, raggedbottom_reading  # noqa: E402


def main():
    units = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--units=")), "")
    subprocess.run([sys.executable, str(ROOT / "reviews" / "r140" / "tools" / "port_r140.py"), f"--units={units}"], check=True, capture_output=True)
    r = subprocess.run([sys.executable, str(TOOLS / "build_v23.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-600:] + r.stderr[-600:]
    pdflatex("paper_v23", SUB)
    aux = (SUB / "paper_v23.aux").read_text(encoding="utf-8", errors="replace")
    page = int(re.search(r"\\newlabel\{main-text-end\}\{\{[^}]*\}\{([^}]*)\}", aux).group(1))
    f, _, _ = raggedbottom_reading()
    print(f"units={units}: page {page}, fine {f} ({485 - f:+d} against 485)")


if __name__ == "__main__":
    main()
