# -*- coding: utf-8 -*-
"""old_beside_new_r140.py -- the page images for the author's cold read: every page of the R139 build whose text changed, beside the matching page of the R137 close.
The R137 close PDF is not tracked, so it is rebuilt: port_r137.py --units=close, an empty R139 build-repair list, build_v23.py (the tex asserted equal to the R137 close's
sha256 893da7ec5e2c9fcf), pdflatex three times in a scratch directory WITHOUT the bundled fancyhdr.sty (as the R137 build ran). Then the R139 close is regenerated
(port_r139.py --units=close, build, three pdflatex passes in the submission directory) and its tex sha asserted equal to the one given. A new page 'changed' when any of
its text lines is absent from the old PDF's text; it is paired with the old page whose words overlap it most (pages 1 to 10 pair by number). Writes
reviews/r140/old_beside_new/p<NN>_old<MM>.png and reviews/r140/old_beside_new/INDEX.md; copies the new PDF to reviews/r139/paper_v23_r140.pdf.
Usage: python reviews/r139/tools/old_beside_new_r140.py --close-tex-sha=<16 hex>
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

import fitz

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
V23T = ROOT / "reviews" / "v23" / "tools"
R139 = ROOT / "reviews" / "r140"
OUT = R139 / "old_beside_new"
PY = sys.executable
R137_TEX = "5fa47883e5e5d498"   # R140: the old side is the R139 close


def sha16(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def run(cmd, cwd=ROOT):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    assert r.returncode == 0, (cmd, r.stdout[-600:], r.stderr[-600:])


def pdflatex(cwd, stem):
    for _ in range(3):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", f"{stem}.tex"], cwd=cwd, capture_output=True)


def lines(page):
    return [" ".join(l.split()) for l in page.get_text().splitlines() if len(l.split()) >= 3 and not l.strip().isdigit() and "Under review as a conference paper" not in l]


def main():
    close_sha = next(a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--close-tex-sha="))
    brep = ROOT / "reviews" / "r139" / "results" / "build_repairs_r139.json"
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="r139_old_"))
    try:
        # the R137 close, rebuilt
        run([PY, str(ROOT / "reviews" / "r139" / "tools" / "port_r139.py"), "--units=close"])
        saved = brep.read_text(encoding="utf-8")
        pass  # R140: the R139 build repairs stay (the old side is the R139 close)
        run([PY, str(V23T / "build_v23.py")])
        brep.write_text(saved, encoding="utf-8", newline="\n")
        assert sha16(SUB / "paper_v23.tex") == R137_TEX, f"the rebuilt R137 tex is {sha16(SUB / 'paper_v23.tex')}, not {R137_TEX}"
        shutil.copytree(SUB / "official_style", tmp / "official_style"); shutil.copy2(SUB / "fancyhdr.sty", tmp / "fancyhdr.sty")
        shutil.copy2(SUB / "paper_v23.tex", tmp / "old.tex")
        pdflatex(tmp, "old")
        old = fitz.open(tmp / "old.pdf")
        # the R139 close, regenerated
        run([PY, str(ROOT / "reviews" / "r140" / "tools" / "port_r140.py"), "--units=close"])
        run([PY, str(V23T / "build_v23.py")])
        assert sha16(SUB / "paper_v23.tex") == close_sha, f"the regenerated R139 tex is {sha16(SUB / 'paper_v23.tex')}, not {close_sha}"
        pdflatex(SUB, "paper_v23")
        new = fitz.open(SUB / "paper_v23.pdf")
        shutil.copy2(SUB / "paper_v23.pdf", R139 / "paper_v23_r140.pdf")
        old_all = set(l for i in range(old.page_count) for l in lines(old[i]))
        old_words = [set(" ".join(lines(old[i])).split()) for i in range(old.page_count)]
        OUT.mkdir(parents=True, exist_ok=True)
        for f in OUT.glob("*.png"):
            f.unlink()
        rows = []
        for i in range(new.page_count):
            nl = lines(new[i])
            changed = [l for l in nl if l not in old_all]
            if not changed:
                continue
            if i < 10:
                j = i
            else:
                w = set(" ".join(nl).split())
                j = max(range(old.page_count), key=lambda k: len(w & old_words[k]) / (len(w | old_words[k]) or 1))
            a = old[j].get_pixmap(dpi=80); b = new[i].get_pixmap(dpi=80)
            img = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, a.width + b.width + 20, max(a.height, b.height)), False)
            img.clear_with(255)
            a.set_origin(0, 0); img.copy(a, a.irect)
            b.set_origin(a.width + 20, 0); img.copy(b, b.irect)
            name = f"p{i + 1:02d}_old{j + 1:02d}.png"
            img.save(OUT / name)
            rows.append((i + 1, j + 1, len(changed), changed[0][:90]))
        idx = ["# R140 old beside new (left: the R139 close, rebuilt, tex sha256 5fa47883e5e5d498; right: the R140 close)\n",
               f"New PDF: reviews/r139/paper_v23_r140.pdf ({new.page_count} pages, tex sha256 {close_sha}); old: {old.page_count} pages. A page is listed when any of its text lines is absent from the old PDF's text.\n",
               "| new page | old page shown | changed lines | first changed line |", "|---:|---:|---:|---|"]
        idx += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows]
        (OUT / "INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8", newline="\n")
        print(f"{len(rows)} changed pages of {new.page_count}; images in {OUT}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
