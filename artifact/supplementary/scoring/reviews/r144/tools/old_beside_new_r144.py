# -*- coding: utf-8 -*-
"""old_beside_new_r144.py -- R144: every page of the R144 close whose text changed, plus pages 1, 6 and 9 always, beside the matching page of the R143 close with
unit xd (reviews/r143/paper_v23_r143.pdf, committed at 99ee69b). The paragraphs below are the R142 tool's docstring.
The old side is the fallback PDF itself (reviews/fallback/paper_v23_fallback_42b6951.pdf, the R140 close, sha256 asserted against reviews/fallback/SHA256SUMS); it is
read, never written. The new side is the built paper_v23.pdf, whose tex sha256 is asserted equal to the one given. A new page 'changed' when any of its text lines is
absent from the old PDF's text; it is paired with the old page whose words overlap it most (pages 1 to 10 pair by number). Writes
reviews/r141/old_beside_new/p<NN>_old<MM>.png and reviews/r141/old_beside_new/INDEX.md; copies the new PDF to reviews/r141/paper_v23_r141.pdf.
Usage: python reviews/r141/tools/old_beside_new_r141.py --close-tex-sha=<16 hex>
"""
from __future__ import annotations

import hashlib
import pathlib
import shutil
import sys

import fitz

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
R141 = ROOT / "reviews" / "r144"
OUT = R141 / "old_beside_new"
OLD = ROOT / "reviews" / "r143" / "paper_v23_r143.pdf"   # the R143 close with unit xd


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def lines(page):
    return [" ".join(l.split()) for l in page.get_text().splitlines() if len(l.split()) >= 3 and not l.strip().isdigit() and "Under review as a conference paper" not in l]


def main():
    close_sha = next(a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--close-tex-sha="))
    assert sha(OLD).startswith("b210cc49e5e1edcf"), "the R143 close PDF is not the one committed at 99ee69b"
    assert sha(SUB / "paper_v23.tex")[:16] == close_sha, f"the built tex is {sha(SUB / 'paper_v23.tex')[:16]}, not {close_sha}"
    old, new = fitz.open(OLD), fitz.open(SUB / "paper_v23.pdf")
    shutil.copy2(SUB / "paper_v23.pdf", R141 / "paper_v23_r144.pdf")
    old_all = set(l for i in range(old.page_count) for l in lines(old[i]))
    old_words = [set(" ".join(lines(old[i])).split()) for i in range(old.page_count)]
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.png"):
        f.unlink()
    rows = []
    for i in range(new.page_count):
        nl = lines(new[i])
        changed = [l for l in nl if l not in old_all]
        if not changed and i + 1 not in (1, 6, 9):
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
        rows.append((i + 1, j + 1, len(changed), (changed[0][:90] if changed else "(none; shown as required)")))
    idx = [f"# R144 old beside new (left: the R143 close with xd, {OLD.name}; right: the R144 close)\n",
           f"New PDF: reviews/r144/paper_v23_r144.pdf ({new.page_count} pages, tex sha256 {close_sha}); old: {old.page_count} pages. A page is listed when any of its text lines is absent from the old PDF's text; pages 1, 6 and 9 are always listed.\n",
           "| new page | old page shown | changed lines | first changed line |", "|---:|---:|---:|---|"]
    idx += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows]
    (OUT / "INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(rows)} changed pages of {new.page_count}; images in {OUT}")


if __name__ == "__main__":
    main()
