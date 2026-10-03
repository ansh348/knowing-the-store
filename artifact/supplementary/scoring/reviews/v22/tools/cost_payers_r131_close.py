# -*- coding: utf-8 -*-
"""cost_payers_r131_close.py -- the cumulative costed table of the R131 close (2026-09-20; MERGED RULINGS 1C: 'costed CUMULATIVELY only'), the instrument
of cost_payers_r131.py (slack in lines by bisection over a \\vspace before the builders box, or the deficit by a negative \\vspace before the Conclusion
heading; the fine number is not linear). Variants, cumulative in the ruled order: the close with no payer beyond section H's four, then + payer 5, +
5b, + 6, + 7, + 8, + B2. Resumable: each variant's line is appended to reviews/v22/results/cost_payers_r131_close.jsonl as it completes and a re-run
skips the recorded ones. At the end the body is regenerated with --final (default: every payer) and the paper rebuilt.
Regeneration per variant: port_v22.py -> port_r131.py --payers=1,2,3,4 -> port_r131_close.py --payers=<cumulative>. The appendix (appendix_r131_close.py)
must already be in place; it is not touched here.
Usage: python reviews/v22/tools/cost_payers_r131_close.py [--final=5,5b,6,7,8,B2] [--only=<one cumulative variant>]
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "reviews" / "v22" / "tools"
BODY = ROOT / "reviews" / "v22" / "src" / "body_v22.tex"
OUT = ROOT / "reviews" / "v22" / "results" / "cost_payers_r131_close.md"
LOG = ROOT / "reviews" / "v22" / "results" / "cost_payers_r131_close.jsonl"
sys.path.insert(0, str(TOOLS))
from cost_payers_r131 import slack  # noqa: E402  (fits/slack: the R131 instrument, the deficit probed before the Conclusion heading)

PLAN = [("the close, no payer beyond section H's four (payers 1 to 4 and every non-payer ruling)", ""),
        ("+ payer 5 (Section 5.1's target-name paragraph out)", "5"),
        ("+ payer 5b (the Conclusion's intent sentence)", "5,5b"),
        ("+ payer 6 (the Section 5.3 cuts P6a to P6d)", "5,5b,6"),
        ("+ payer 7 (Figure 3's height 5.0cm to 4.5cm)", "5,5b,6,7"),
        ("+ payer 8 (Section 5.2's list-length paragraph to two sentences)", "5,5b,6,7,8"),
        ("+ payer B2 (Section 1's findings paragraph cut)", "5,5b,6,7,8,B2")]


def regen(payers):
    subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
    subprocess.run([sys.executable, str(TOOLS / "port_r131.py"), "--payers=1,2,3,4"], check=True, capture_output=True)
    subprocess.run([sys.executable, str(TOOLS / "port_r131_close.py"), f"--payers={payers}"], check=True, capture_output=True)
    return BODY.read_text(encoding="utf-8")


def main():
    final = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--final=")), "5,5b,6,7,8,B2")
    only = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--only=")), None)
    plan = [(l, p) for l, p in PLAN if only is None or p == only]
    done = {}
    if LOG.exists():
        for ln in LOG.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                r = json.loads(ln); done[r["payers"]] = r
    t0 = time.time()
    try:
        for label, payers in plan:
            if payers in done:
                print(f"| {label} | {done[payers]['slack']:+d} | {done[payers]['log'][0]} |  (recorded)", flush=True)
                continue
            text = regen(payers)
            log = []
            s = slack(text, log)
            r = {"label": label, "payers": payers, "slack": s, "log": log}
            with LOG.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(r) + "\n")
            done[payers] = r
            print(f"| {label} | {s:+d} | {log[0]} |  ({time.time() - t0:.0f}s)", flush=True)
    finally:
        regen(final)
        subprocess.run([sys.executable, str(TOOLS / "build_v22.py")], check=True, capture_output=True)
    rows = [done[p] for _, p in PLAN if p in done]
    md = ["# The cumulative costed table of the R131 close (cost_payers_r131_close.py, 2026-09-20)\n\n",
          "Slack = the largest k such that k baselines added before the builders box still leave it on page 9; a negative value is the smallest k of baselines that must be removed from page 9's text "
          "(the probe puts `\\vspace{-k\\baselineskip}` before the Conclusion heading) for the box to return. The fine number is not linear (the box is one unbreakable minipage), so this is the instrument; "
          "the reading at k = 0 is beside each row. Variants are cumulative in the ruled order (MERGED RULINGS 1C); every row carries payers 1 to 4 of section H and every non-payer ruling of the close "
          "(L1 to L4, A1', A2', B1 the abstract, 1A, 1B, the appendix edits).\n\n",
          "| variant (cumulative) | slack in lines | the build at k = 0 |\n|---|---:|---|\n"]
    md += [f"| {r['label']} | {r['slack']:+d} | {r['log'][0]} |\n" for r in rows]
    md.append("\n## The probes\n\n")
    md += [f"- {r['label']}: " + "; ".join(r["log"]) + "\n" for r in rows]
    OUT.write_text("".join(md), encoding="utf-8", newline="\n")
    print("->", OUT)


if __name__ == "__main__":
    main()
