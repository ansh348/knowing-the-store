# -*- coding: utf-8 -*-
"""probe_draft_r141.py -- the slack probe (reviews/r140/tools/slack_r140.py's bisection) on a drafted branch (draft_branches_r141.py), then the R140 close
restored (port_r140.py --units=close) and rebuilt, so no draft is left in the sources. Appends a row to reviews/r141/results/slack_r141_draft.md.
Usage: python reviews/r141/tools/probe_draft_r141.py --branch=bi|biii
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "r140" / "tools"))
import slack_r140 as S  # noqa: E402

OUT = ROOT / "reviews" / "r141" / "results" / "slack_r141_draft.md"


def main():
    br = next(a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--branch="))
    subprocess.run([sys.executable, str(ROOT / "reviews" / "r141" / "tools" / "draft_branches_r141.py"), f"--branch={br}"], check=True)
    text = S.BODY.read_text(encoding="utf-8")
    log = []
    s = S.slack(text, log)
    subprocess.run([sys.executable, str(ROOT / "reviews" / "r140" / "tools" / "port_r140.py"), "--units=close"], check=True, capture_output=True)
    S.fine()
    row = f"| draft {br} (placeholder numbers) | {s:+d} | {log[0]} | {'; '.join(log[1:])} |\n"
    if not OUT.exists():
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text("# R141 page estimates by branch (the slack probe on drafted landings; placeholders)\n\n| variant | slack | k = 0 | probes |\n|---|---:|---|---|\n", encoding="utf-8", newline="\n")
    OUT.write_text(OUT.read_text(encoding="utf-8") + row, encoding="utf-8", newline="\n")
    print(row)


if __name__ == "__main__":
    main()
