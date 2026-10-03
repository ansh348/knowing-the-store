# -*- coding: utf-8 -*-
"""cost_pointer.py -- R116 ruling 4: the page cost of the proposed Section 4 body pointer, read on a scratch build that never touches
iclr2027_monitoring_submission/paper_v19.tex. Builds the paper from a copy of body_v19.tex carrying the pointer (r116b_apply.py --pointer)
with build_v19.py's own repair tables, runs pdflatex three times in a temp dir, and prints the page census, the raggedbottom fine number
and the page count. Usage: python reviews/r116/tools/cost_pointer.py <body copy with the pointer>
"""
import importlib.util
import io
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOLS = ROOT / "reviews" / "v19" / "tools"
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location("build_v19", TOOLS / "build_v19.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)
import run_gates as G  # noqa: E402  (margin_lines)


def build(body_path):
    body = io.open(body_path, encoding="utf-8").read().replace("\r\n", "\n")
    abstract = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}\n", B.read(B.SRC / "abstract_v19.tex"), flags=re.S).group(0)
    assert body.count("%%ABSTRACT%%\n") == 1
    text = body.replace("%%ABSTRACT%%\n", abstract) + B.read(B.SRC / "appendix_v19.tex")
    v11 = B.read(B.V11).split("\n")

    def repl(m):
        a, b = int(m.group(1)), int(m.group(2))
        out = []
        for ln in v11[a - 1:b]:
            for o, n_ in B.REPAIRS:
                ln = ln.replace(o, n_)
            for o, n_ in B.REPAIRS_V18:
                ln = ln.replace(o, n_)
            if not any(h in ln for h in B.FROZEN_V11_HEADS):
                for o, n_, _ in B.REPAIRS_R111:
                    ln = ln.replace(o, n_)
                for o, n_, _ in B.REPAIRS_R112:
                    ln = ln.replace(o, n_)
            for o, n_, _ in B.REPAIRS_R115_BLOCK.get((a, b), []):
                ln = ln.replace(o, n_)
            for o, n_, _ in B.REPAIRS_R116_BLOCK.get((a, b), []):
                ln = ln.replace(o, n_)
            if "\textit{Monitors}" in ln:
                ln = ln.replace("\textit{Monitors}", "\\textit{Monitors}")
            out.append(ln)
        return "\n".join(out)

    out = re.sub(r"%%V11:(\d+)-(\d+)%%", repl, text)
    assert "%%V11:" not in out
    return out


def main():
    out = build(sys.argv[1])
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="v19_ptr_"))
    shutil.copytree(SUB / "official_style", tmp / "official_style")
    (tmp / "paper_v19.tex").write_text(out, encoding="utf-8", newline="\n")
    G.pdflatex("paper_v19", tmp)
    r = subprocess.run([sys.executable, str(SUB / "tools" / "page_census_v2.py"), str(tmp / "paper_v19.pdf")], cwd=SUB, capture_output=True, text=True).stdout
    print("page_census:", [l for l in r.split("\n") if "paper_v19.pdf" in l])
    (tmp / "paper_rb.tex").write_text(out.replace("\\begin{document}", "\\begin{document}\\raggedbottom", 1), encoding="utf-8", newline="\n")
    G.pdflatex("paper_rb", tmp)
    aux = (tmp / "paper_rb.aux").read_text(encoding="utf-8", errors="replace")
    page_no = int(re.search(r"\\newlabel\{main-text-end\}\{\{[^}]*\}\{([^}]*)\}", aux).group(1))
    rows = G.margin_lines(tmp / "paper_rb.pdf", page_no)
    head = next((i for i, (_, _, txt) in enumerate(rows) if "AI USE STATEMENT" in txt.upper().replace("  ", " ")), None)
    nums = [n for n, _, _ in (rows[:head] if head is not None else rows) if n is not None]
    print("fine number", max(nums), "label page", page_no, "AI-use statement", "on the same page" if head is not None else "on the next page")
    import fitz
    print("pages", fitz.open(tmp / "paper_v19.pdf").page_count)
    assert tmp.name.startswith("v19_ptr_")
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
