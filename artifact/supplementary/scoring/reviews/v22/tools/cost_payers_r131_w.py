# -*- coding: utf-8 -*-
"""cost_payers_r131_w.py -- the cumulative costed table of the page 8-9 payers W1 to W7 (2026-09-20; 'R131 CLOSE: PAGE 8-9 PAYERS'), the R131
instrument (slack by bisection; the deficit probed before the Conclusion heading). One variant per foreground call (--only=N applies W1 to WN
cumulatively on top of port_r131_close.py --payers=5,5b,6,7,8,B2); the driver stops applying as soon as slack reads +2 or better. Resumable: each
variant's row goes to reviews/v22/results/cost_payers_r131_w.jsonl. After W1a's k = 0 build the tool reads the PDF and reports whether the
'(Appendix A)' pointer still sits alone on its line (W1's condition for W1b); --w1b adds it. At the end the body is regenerated with --final.
Usage: python reviews/v22/tools/cost_payers_r131_w.py --only=N [--w1b] [--final=N[,w1b]]
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "reviews" / "v22" / "tools"
SUB = ROOT / "iclr2027_monitoring_submission"
BODY = ROOT / "reviews" / "v22" / "src" / "body_v22.tex"
OUT = ROOT / "reviews" / "v22" / "results" / "cost_payers_r131_w.md"
LOG = ROOT / "reviews" / "v22" / "results" / "cost_payers_r131_w.jsonl"
sys.path.insert(0, str(TOOLS))
from cost_payers_r131 import slack  # noqa: E402
from run_gates import margin_lines  # noqa: E402

LABELS = {1: "W1 (Section 8: 'On the shared', the pointer joins the line above)", 2: "+ W2 (Limitations 1: the small-groups sentence)", 3: "+ W3 (Limitations 3: the alignment sentence)",
          4: "+ W4 (Section 7: the tested-rule paragraph's third sentence folded)", 5: "+ W5 (Limitations 2: two trims)", 6: "+ W6 (Conclusion: the all-states clause deleted)",
          7: "+ W7 (Section 8: the coverage-intervals sentence to E.8)"}


SKIP = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--skip=")), "")


def regen(n, w1b):
    subprocess.run([sys.executable, str(TOOLS / "port_v22.py")], check=True, capture_output=True)
    subprocess.run([sys.executable, str(TOOLS / "port_r131.py"), "--payers=1,2,3,4"], check=True, capture_output=True)
    subprocess.run([sys.executable, str(TOOLS / "port_r131_close.py"), "--payers=5,5b,6,7,8,B2"], check=True, capture_output=True)
    if n:
        subprocess.run([sys.executable, str(TOOLS / "port_r131_w.py"), f"--w={n}"] + (["--w1b"] if w1b else []) + ([f"--skip={SKIP}"] if SKIP else []), check=True, capture_output=True)
    return BODY.read_text(encoding="utf-8")


def pointer_alone():
    """After a build: does a Section 8 line hold only '(Appendix A)'?"""
    pdf = SUB / "paper_v22.pdf"
    for p in (8, 9, 10):
        try:
            for n, y, txt in margin_lines(pdf, p):
                if re.fullmatch(r"\(Appendix A\)", txt.strip()):
                    return True
        except Exception:
            pass
    return False


def main():
    only = int(next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--only=")), "0"))
    w1b = "--w1b" in sys.argv
    final = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--final=")), None)
    done = {}
    if LOG.exists():
        for ln in LOG.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                r = json.loads(ln); done[r["key"]] = r
    t0 = time.time()
    try:
        if only:
            key = f"W1-{only}" + ("+w1b" if w1b else "") + (f"-skip{SKIP}" if SKIP else "")
            if key in done:
                print(f"| {LABELS[only]}{' with W1b' if w1b else ''} | {done[key]['slack']:+d} | {done[key]['log'][0]} |  (recorded)")
            else:
                text = regen(only, w1b)
                log = []
                s = slack(text, log)
                alone = pointer_alone() if only == 1 else None
                r = {"key": key, "label": LABELS[only] + (" with W1b" if w1b else "") + (f" without W{SKIP} (the Q-A trip)" if SKIP else ""), "slack": s, "log": log, "pointer_alone_after_last_probe": alone}
                with LOG.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(r) + "\n")
                done[key] = r
                print(f"| {r['label']} | {s:+d} | {log[0]} |  ({time.time() - t0:.0f}s){'; the (Appendix A) pointer alone on its line: ' + str(alone) if alone is not None else ''}", flush=True)
    finally:
        if final:
            n, _, flag = final.partition(",")
            regen(int(n), flag == "w1b")
            subprocess.run([sys.executable, str(TOOLS / "build_v22.py")], check=True, capture_output=True)
    rows = [done[k] for k in sorted(done, key=lambda k: (int(k.split("-")[1].split("+")[0]), "+w1b" in k, "skip" in k))]
    md = ["# The cumulative costed table of the page 8-9 payers W1 to W7 (cost_payers_r131_w.py, 2026-09-20), on the R131 close checkpoint fc94d06 (-5)\n\n",
          "Slack = the largest k such that k baselines added before the builders box still leave it on page 9; a negative value is the smallest k of baselines that must be removed from page 9's text "
          "(the probe puts `\\vspace{-k\\baselineskip}` before the Conclusion heading) for the box to return; the reading at k = 0 beside each row. Variants are cumulative in the ruled order; "
          "the driver stops applying at +2 or better.\n\n| variant (cumulative) | slack in lines | the build at k = 0 |\n|---|---:|---|\n"]
    md += [f"| {r['label']} | {r['slack']:+d} | {r['log'][0]} |\n" for r in rows]
    md.append("\n## The probes\n\n")
    md += [f"- {r['label']}: " + "; ".join(r["log"]) + (f" (the (Appendix A) pointer alone on its line after the last probe build: {r['pointer_alone_after_last_probe']})" if r.get("pointer_alone_after_last_probe") is not None else "") + "\n" for r in rows]
    OUT.write_text("".join(md), encoding="utf-8", newline="\n")
    print("->", OUT)


if __name__ == "__main__":
    main()
