# -*- coding: utf-8 -*-
"""scratch_gates.py -- program R118: cost a landing before it is ruled on. Copies reviews/v21/src to a scratch directory, applies the named
r118_apply groups there, builds paper_v21_scratch.tex with build_v21's repair tables, compiles it three times, and runs the scans that
decide a landing (page census, the raggedbottom fine number, frozen_diff, prose_scan, repeat_scan, slogan_scan, claims_diff, trace_scan,
q_scan, s17_grep, code_scan, u9_scan, and numeric_diff's ADDED list). The v21 sources and paper_v21.tex are untouched; the scratch
build's files are removed at the end. Usage: python reviews/v21/tools/scratch_gates.py <tag> <group,group,...>
"""
from __future__ import annotations

import importlib.util
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
V21 = ROOT / "reviews" / "v21"
TOOLS = V21 / "tools"
PY = sys.executable
BASE = (V21 / "base_tree.txt").read_text().strip()
sys.path.insert(0, str(TOOLS))
import run_gates as G  # noqa: E402  (margin_lines, pdflatex)


def run(cmd, cwd=SUB):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (r.stdout + r.stderr).strip()


def last(out, n=1):
    lines = [l for l in out.split("\n") if l.strip()]
    return " | ".join(lines[-n:]) if lines else "(no output)"


def main():
    tag, groups = sys.argv[1], sys.argv[2]
    scratch = pathlib.Path(tempfile.mkdtemp(prefix="v21_scratch_")) / "src"
    shutil.copytree(V21 / "src", scratch)
    out = run([PY, str(TOOLS / "r118_apply.py"), "--only", groups, "--src", str(scratch)], cwd=ROOT)
    assert "written" in out, out[-600:]
    spec = importlib.util.spec_from_file_location("build_v21", TOOLS / "build_v21.py"); B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
    B.SRC = scratch; B.OUT = SUB / "paper_v21_scratch.tex"
    B.main()
    G.pdflatex("paper_v21_scratch", SUB)
    L = [f"scratch gates on paper_v21_scratch.tex, groups {groups} ({tag}); base tree {BASE}"]
    row = next((l for l in run([PY, "tools/page_census_v2.py", "paper_v21_scratch.pdf"]).split("\n") if l.startswith("paper_v21_scratch.pdf")), "(no census)")
    # raggedbottom fine number
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="v21_rb_")); shutil.copytree(SUB / "official_style", tmp / "official_style")
    t = (SUB / "paper_v21_scratch.tex").read_text(encoding="utf-8")
    (tmp / "paper_v21_scratch.tex").write_text(t.replace("\\begin{document}", "\\begin{document}\\raggedbottom", 1), encoding="utf-8", newline="\n")
    G.pdflatex("paper_v21_scratch", tmp)
    aux = (tmp / "paper_v21_scratch.aux").read_text(encoding="utf-8", errors="replace")
    page_no = int(re.search(r"\\newlabel\{main-text-end\}\{\{[^}]*\}\{([^}]*)\}", aux).group(1))
    rows = G.margin_lines(tmp / "paper_v21_scratch.pdf", page_no)
    head = next((i for i, (_, _, txt) in enumerate(rows) if "AI USE STATEMENT" in txt.upper().replace("  ", " ")), None)
    nums = [n for n, _, _ in (rows[:head] if head is not None else rows) if n is not None]
    shutil.rmtree(tmp, ignore_errors=True)
    if nums:
        L.append(f"page_census_v2: {row}   (raggedbottom: last margin number {max(nums)}, label page {page_no}; fine number {max(nums)} against 485, {485 - max(nums):+d})")
    else:
        L.append(f"page_census_v2: {row}   (raggedbottom: label page {page_no}, no body line with a margin number before the AI-use heading on that page: the main text spills by less than a numbered line)")
    fz = run([PY, "tools/frozen_diff.py", f"--base={BASE}", "--program=R118", "--tex=paper_v21_scratch.tex", "--base-tex=paper_v19.tex"])
    L.append("frozen_diff: " + last(fz, 3))
    L.extend("  " + l for l in fz.splitlines() if "UNAUTHORIZED" in l and not l.startswith("frozen_diff"))   # R118: the unauthorized strings by name
    L.append("trace_scan_v13: " + last(run([PY, "tools/trace_scan_v13.py", "paper_v21_scratch.tex"]), 3))
    L.append("claims_diff: " + last(run([PY, "tools/claims_diff.py", "paper_v21_scratch.tex", "--extra-tex=SUPPLEMENT.tex"])))
    L.append("slogan_scan: " + last(run([PY, "tools/slogan_scan.py", "paper_v21_scratch.tex", "--extra-tex=SUPPLEMENT.tex"]), 3))
    L.append("prose_scan: " + last(run([PY, "tools/prose_scan.py", "paper_v21_scratch.tex"]), 4))
    L.append("q_scan: " + last(run([PY, str(TOOLS / "q_scan.py"), "paper_v21_scratch.tex"], cwd=ROOT)))
    L.append("s17_grep: " + last(run([PY, str(TOOLS / "s17_grep.py"), "paper_v21_scratch.tex"], cwd=ROOT)))
    L.append("repeat_scan: " + last(run([PY, "tools/repeat_scan.py", "paper_v21_scratch.tex"]), 3))
    L.append("code_scan: " + last(run([PY, "tools/code_scan.py", "paper_v21_scratch.tex"]), 2))
    L.append("u9_scan: " + last(run([PY, "tools/u9_scan.py", "paper_v21_scratch.tex"])))
    nd = run([PY, "tools/numeric_diff.py", f"--base={BASE}", "--tex=paper_v21_scratch.tex", "--base-tex=paper_v19.tex", "--round2"])
    added = re.search(r"ADDED \((\d+)\):[ \t]*(.*)", nd); van = re.search(r"VANISHED \((\d+)\):[ \t]*(.*)", nd)
    L.append(f"numeric_diff: ADDED {added.group(1) if added else '?'}: {(added.group(2)[:600] if added else '')}")
    L.append(f"numeric_diff: VANISHED {van.group(1) if van else '?'}: {(van.group(2)[:300] if van else '')}")
    log = (SUB / "paper_v21_scratch.log").read_text(encoding="utf-8", errors="replace")
    L.append(f"overfull boxes: {log.count('Overfull')}; undefined references: {log.count('Reference `')}; undefined citations: {log.count('Citation `')}")
    import fitz
    L.append(f"pages: {fitz.open(SUB / 'paper_v21_scratch.pdf').page_count}")
    text = "\n".join(L) + "\n"
    (V21 / f"scratch_{tag}.txt").write_text(text, encoding="utf-8", newline="\n")
    print(text)
    if "--keep" in sys.argv:            # R118: keep the scratch build (tex, pdf, log) for inspection; the scratch sources too
        print("kept:", SUB / "paper_v21_scratch.pdf", "and", scratch); return
    for ext in (".tex", ".pdf", ".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".bbl", ".blg"):
        p = SUB / f"paper_v21_scratch{ext}"
        if p.exists():
            p.unlink()
    shutil.rmtree(scratch.parent, ignore_errors=True)


if __name__ == "__main__":
    main()
