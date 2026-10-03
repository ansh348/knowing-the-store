# -*- coding: utf-8 -*-
"""run_gates.py -- the gate battery on paper_v22.tex (program R126; the v21 runner retargeted by bump_v22.py), in the order and format of reviews/v18/gates_wp_phase*.txt:
build the tex (build_v22.py), three pdflatex passes, then page_census_v2, frozen_diff, numeric_diff via number_moves_wp --check,
trace_scan_v13, appendix_identity, claims_diff, slogan_scan, prose_scan, q_scan, s17_grep, repeat_scan, code_scan, u9_scan, dupkey_scan,
refcheck_v11, hygiene_scan, the overfull count, the page count, readability_wp and frozen_list_wp. Writes reviews/v22/<name>.txt and
prints it; the readability listing goes to reviews/v22/first_sentences_<tag>.txt and the frozen list to reviews/v22/results/frozen_<tag>.json.
A raggedbottom diagnostic build (the paper with \\raggedbottom after \\begin{document}, built in a scratch directory) gives the fine number:
the margin number of the main text's last line when pages are not stretched.
Usage: python reviews/v22/tools/run_gates.py <tag> ["<one-line description>"] [--no-build]
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
V19 = ROOT / "reviews" / "v22"
TOOLS = V19 / "tools"
PY = sys.executable
BASE = (V19 / "base_tree.txt").read_text().strip()


def run(cmd, cwd=SUB):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (r.stdout + r.stderr).strip(), r.returncode


def last(out, n=1):
    lines = [l for l in out.split("\n") if l.strip()]
    return " | ".join(lines[-n:]) if lines else "(no output)"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def pdflatex(stem, cwd):
    for _ in range(3):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", f"{stem}.tex"], cwd=cwd, capture_output=True)


def margin_lines(pdf, page_no):
    """(margin number, baseline y, text) for every line of a page, the way the phase reports read them."""
    import fitz, statistics
    page = fitz.open(pdf)[page_no - 1]
    words = page.get_text("words")
    nums = [w for w in words if re.fullmatch(r"\d{3}", w[4])]
    modal_x = statistics.mode([round(w[0], 1) for w in nums])
    margin = {round(w[3], 0): int(w[4]) for w in nums if abs(w[0] - modal_x) <= 1.5}
    rows = []
    for w in sorted((w for w in words if not (re.fullmatch(r"\d{3}", w[4]) and abs(w[0] - modal_x) <= 1.5)), key=lambda w: (w[3], w[0])):
        if rows and abs(w[3] - rows[-1][0]) < 3.0:
            rows[-1][1].append(w)
        else:
            rows.append([w[3], [w]])
    return [(next((n for yy, n in margin.items() if abs(yy - y) < 4.5), None), y, " ".join(x[4] for x in sorted(ws, key=lambda w: w[0]))) for y, ws in rows]


def raggedbottom_reading():
    """The fine number: the last margin number of the main text under \\raggedbottom, and the page the AI-use statement opens."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="v22_rb_"))
    shutil.copytree(SUB / "official_style", tmp / "official_style")
    t = (SUB / "paper_v22.tex").read_text(encoding="utf-8")
    (tmp / "paper_v22.tex").write_text(t.replace("\\begin{document}", "\\begin{document}\\raggedbottom", 1), encoding="utf-8", newline="\n")
    pdflatex("paper_v22", tmp)
    aux = (tmp / "paper_v22.aux").read_text(encoding="utf-8", errors="replace")
    page_no = int(re.search(r"\\newlabel\{main-text-end\}\{\{[^}]*\}\{([^}]*)\}", aux).group(1))
    rows = margin_lines(tmp / "paper_v22.pdf", page_no)
    head = next((i for i, (_, _, txt) in enumerate(rows) if "AI USE STATEMENT" in txt.upper().replace("  ", " ")), None)
    body = rows[:head] if head is not None else rows
    nums = [n for n, _, _ in body if n is not None]
    # Completion 2026-09-17: verify the diagnostic scratch target before recursive cleanup.
    assert tmp.resolve().parent == pathlib.Path(tempfile.gettempdir()).resolve()
    assert tmp.name.startswith("v22_rb_")
    shutil.rmtree(tmp, ignore_errors=True)
    return max(nums), page_no, ("on the same page" if head is not None else "on the next page")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tag = args[0]
    desc = args[1] if len(args) > 1 else ""
    if "--no-build" not in sys.argv:
        out, rc = run([PY, str(TOOLS / "build_v22.py")], cwd=ROOT)
        assert rc == 0, out[-800:]
        pdflatex("paper_v22", SUB)
    L = [f"gate battery on paper_v22.tex, {desc or tag} (program R126), base tree {BASE} (paper_v21.tex at the R124 close, ee6b735); "
         f"paper_v22.tex sha256 {sha(SUB / 'paper_v22.tex')}; paper_v22.pdf sha256 {sha(SUB / 'paper_v22.pdf')}"]
    out, rc = run([PY, "tools/page_census_v2.py", "paper_v22.pdf"])
    row = next((l for l in out.split("\n") if l.startswith("paper_v22.pdf")), out)
    rb, page_no, where = raggedbottom_reading()
    L.append(f"page_census_v2: {row}   (raggedbottom diagnostic build: the main text's last margin number {rb}, label page {page_no}, the AI-use statement {where}; fine number {rb} against 485, {485 - rb:+d})")
    # without --extra-tex, as R110 ran: the base holds the paper alone, and the supplement on the working side doubles the title and two configuration strings
    out, rc = run([PY, "tools/frozen_diff.py", f"--base={BASE}", "--program=R126", "--tex=paper_v22.tex", "--base-tex=paper_v21.tex"])
    L.append(f"frozen_diff (program R126): {last(out)}")
    out, rc = run([PY, str(TOOLS / "number_moves_wp.py"), "--check"], cwd=ROOT)
    L.append(f"numeric_diff (--round2) via NUMBER_MOVES_V21.md: {last(out)}")
    out, rc = run([PY, "tools/trace_scan_v13.py", "paper_v22.tex"])
    L.append(f"trace_scan_v13: {last(out)}")
    out, rc = run([PY, "tools/appendix_identity.py", BASE, "--tex=paper_v22.tex", "--base=iclr2027_monitoring_submission/paper_v21.tex"])
    L.append(f"appendix_identity: {last(out)}")
    out, rc = run([PY, "tools/claims_diff.py", "paper_v22.tex", "--extra-tex=SUPPLEMENT.tex"])
    L.append(f"claims_diff: {last(out)}")
    out, rc = run([PY, "tools/slogan_scan.py", "paper_v22.tex", "--extra-tex=SUPPLEMENT.tex"])
    L.append(f"slogan_scan: {last(out)}")
    out, rc = run([PY, "tools/prose_scan.py", "paper_v22.tex"])
    L.append(f"prose_scan (rules incl. G): {last(out)}")
    out, rc = run([PY, str(TOOLS / "q_scan.py"), "paper_v22.tex"], cwd=ROOT)
    L.append(f"q_scan: {last(out)}")
    out, rc = run([PY, str(TOOLS / "s17_grep.py"), "paper_v22.tex"], cwd=ROOT)
    L.append(f"s17_grep: {last(out)}")
    out, rc = run([PY, "tools/repeat_scan.py", "paper_v22.tex"])
    L.append(f"repeat_scan: {last(out)}")
    out, rc = run([PY, "tools/code_scan.py", "paper_v22.tex"])
    L.append(f"code_scan: {last(out)}")
    out, rc = run([PY, "tools/u9_scan.py", "paper_v22.tex"])
    L.append(f"u9_scan: {last(out)}")
    out, rc = run([PY, "tools/dupkey_scan.py"])
    L.append(f"dupkey_scan: {last(out)}")
    out, rc = run([PY, "tools/refcheck_v11.py", "paper_v22.tex"])
    L.append(f"refcheck_v11: {last(out, 2).split(' | ')[0]}")
    out, rc = run([PY, "tools/hygiene_scan.py", "paper_v22.pdf"])
    L.append(f"hygiene_scan: {last(out)}")
    log = (SUB / "paper_v22.log").read_text(encoding="utf-8", errors="replace")
    L.append(f"overfull boxes: {log.count('Overfull')}; undefined references: {log.count('Reference `')}; " + ("undefined citations: " + str(log.count("Citation `"))))
    import fitz
    L.append(f"pages: {fitz.open(SUB / 'paper_v22.pdf').page_count} pages")
    out, rc = run([PY, str(TOOLS / "readability_wp.py"), "paper_v22.tex", f"--first=reviews/v22/first_sentences_{tag}.txt"], cwd=ROOT)
    (V19 / "results").mkdir(exist_ok=True)
    fl, rc = run([PY, str(TOOLS / "frozen_list_wp.py"), BASE, "--base-tex=paper_v21.tex", "--tex=paper_v22.tex", "--program=R126", f"--json=reviews/v22/results/frozen_{tag}.json"], cwd=ROOT)
    L.append(f"readability: {' | '.join(l for l in out.split(chr(10)) if l.startswith(('readability', 'contributions')))}; frozen_list_wp {last(fl)}")
    text = "\n".join(L) + "\n"
    (V19 / f"gates_{tag}.txt").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
