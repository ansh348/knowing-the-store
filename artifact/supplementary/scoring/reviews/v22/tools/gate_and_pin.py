# -*- coding: utf-8 -*-
"""gate_and_pin.py -- program R118: run the gate battery on a landed step, pin the appendix sections it changed (pin_appendix_r118.py, which
needs a recorded reason per section), and re-run the gates without rebuilding; print the gate record's decisive lines.
Usage: python reviews/v21/tools/gate_and_pin.py <step> <tag> "<description>" """
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "reviews" / "v21" / "tools"
PY = sys.executable


def run(args):
    r = subprocess.run([PY] + args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (r.stdout + r.stderr)


def main():
    step, tag, desc = sys.argv[1], sys.argv[2], sys.argv[3]
    out = run([str(TOOLS / "run_gates.py"), tag, desc])
    if "appendix_identity: FAIL" in out:
        print(run([str(TOOLS / "pin_appendix_r118.py"), step]).strip().splitlines()[-1])
        out = run([str(TOOLS / "run_gates.py"), tag, desc, "--no-build"])
    rec = (ROOT / "reviews" / "v21" / f"gates_{tag}.txt").read_text(encoding="utf-8")
    import re
    GATES = ("frozen_diff", "numeric_diff", "trace_scan_v13", "appendix_identity", "claims_diff", "slogan_scan", "prose_scan", "q_scan",
             "s17_grep", "repeat_scan", "code_scan", "u9_scan", "dupkey_scan", "refcheck_v11", "hygiene_scan")
    # a gate line passes only when it says PASS (numeric_diff: "missing ... 0"); a failure line often carries neither word, only the finding
    bad = lambda l: (l.startswith(GATES) and "PASS" not in l and not re.search(r"missing from NUMBER_MOVES_V21[.]md 0$", l)) or ("UNAUTHORIZED" in l)
    fails = [l for l in rec.splitlines() if bad(l)]
    for l in rec.splitlines():
        if l.startswith(("page_census", "overfull", "pages")) or bad(l):
            print(l[:230])
    print("GATES:", "ALL PASS" if not fails else f"{len(fails)} FAILING LINE(S)")


if __name__ == "__main__":
    main()
