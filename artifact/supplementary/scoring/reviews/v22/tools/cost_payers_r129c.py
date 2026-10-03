# -*- coding: utf-8 -*-
"""cost_payers_r129c.py -- each R129 body change applied alone on the R128 close (2026-09-20). The builders box moves whole once the main text spills,
so a change reverted inside the spill reads +0 lines (cost_payers_r129.py); on the R128 close (page 9, +2) the fine number is linear in lines, so each
change's own cost or gain is read there. Nothing it writes survives: port_v22.py regenerates the body at the end.
Usage: python reviews/v22/tools/cost_payers_r129c.py
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "reviews" / "v22" / "tools"
BODY = ROOT / "reviews" / "v22" / "src" / "body_v22.tex"
OUT = ROOT / "reviews" / "v22" / "results" / "cost_payers_r129.md"
sys.path.insert(0, str(TOOLS))
from cost_payers_r129 import VARIANTS, fine  # noqa: E402

POOLED = "\\claim{The pooled metric rewards readers that miss the obligation.}\n"


def main():
    subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
    base = BODY.read_text(encoding="utf-8")
    close = base
    for name, new, old in VARIANTS:
        assert close.count(new) == 1, name
        close = close.replace(new, old)
    rows = []
    try:
        BODY.write_text(close, encoding="utf-8", newline="\n")
        pc, fc = fine()
        rows.append(f"| the R128 close rebuilt (reference) | {pc} | {fc} | {485 - fc:+d} | |")
        print(rows[-1], flush=True)
        for name, new, old in VARIANTS:
            if old:
                assert close.count(old) == 1, name
                v = close.replace(old, new)
            else:
                v = close.replace(POOLED, new + POOLED, 1)
            BODY.write_text(v, encoding="utf-8", newline="\n")
            p, f = fine()
            rows.append(f"| {name} applied alone on the R128 close | {p} | {f} | {485 - f:+d} | {f - fc:+d} lines |")
            print(rows[-1], flush=True)
        # the payers together, and each landing with both payers
        v = close
        for name, new, old in VARIANTS:
            if name.startswith("C"):
                v = v.replace(old, new)
        BODY.write_text(v, encoding="utf-8", newline="\n")
        p, f = fine()
        rows.append(f"| C1 and C2 applied together on the R128 close | {p} | {f} | {485 - f:+d} | {f - fc:+d} lines |")
        print(rows[-1], flush=True)
        for which in ("B1", "B2"):
            w = v
            for name, new, old in VARIANTS:
                if name.startswith(which) or name[:2] in ("A1", "A2", "S4"):
                    w = w.replace(old, new) if old else w.replace(POOLED, new + POOLED, 1)
            BODY.write_text(w, encoding="utf-8", newline="\n")
            p, f = fine()
            rows.append(f"| A1, A2, S4, C1, C2 and {which} (the landing without {'B2' if which == 'B1' else 'B1'}) | {p} | {f} | {485 - f:+d} | {f - fc:+d} lines |")
            print(rows[-1], flush=True)
    finally:
        subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
        subprocess.run([sys.executable, str(TOOLS / "build_v22.py")], check=True, capture_output=True)
    md = OUT.read_text(encoding="utf-8")
    md += "\n## Each change alone on the R128 close (cost_payers_r129c.py; the fine number is linear there)\n\n| variant | page | fine number | against 485 | lines against the close |\n|---|---:|---:|---:|---:|\n" + "\n".join(rows) + "\n"
    OUT.write_text(md, encoding="utf-8", newline="\n")
    print("->", OUT)


if __name__ == "__main__":
    main()
