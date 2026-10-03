r"""_phase4_audit.py -- R81 Phase 4 items 13 and 14: caveat density and figure integrity."""
import io
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SUB = ROOT / "iclr2027_monitoring_submission"
TEX = SUB / "paper_v2.tex"

CAV = re.compile(
    r"\b(does not|do not|cannot|remains open|remains unresolved|not measured|we ran no|"
    r"no claim|not identify|not attribute|bounds the|confined to|within what sampling|"
    r"descriptive comparison|indeterminate|is not necessary|no equivalence test)\b", re.I)


def main():
    d = io.open(TEX, encoding="utf-8").read()
    d = re.sub(r"(?m)^\s*%.*$", "", d)
    main_text = d[d.index(r"\begin{document}"):d.index(r"\appendix")]

    print("=== item 13: caveat density in main-text prose paragraphs ===")
    paras = [p for p in main_text.split("\n\n") if p.strip()]
    rows = []
    for p in paras:
        flat = " ".join(p.split())
        if flat.startswith("\\") and "\\item" not in flat:
            continue          # float or command block, not prose
        sents = [s for s in re.split(r"(?<=[.!?])\s+", flat) if len(s.split()) > 4]
        cav = [s for s in sents if CAV.search(s)]
        if len(cav) >= 3:
            rows.append((len(cav), len(sents), sents[0][:66]))
    for n, tot, head in sorted(rows, reverse=True):
        print(f"  {n} caveat sentences of {tot} :: {head}")
    print(f"  paragraphs carrying 3 or more caveat sentences: {len(rows)}")

    print()
    print("=== item 14: figure environments ===")
    for i, m in enumerate(re.finditer(r"\\begin\{figure\}(.*?)\\end\{figure\}", d, re.S), 1):
        b = m.group(1)
        kind = ("tikz/pgfplots" if "tikzpicture" in b or "\\begin{axis}" in b
                else "includegraphics" if "includegraphics" in b else "unknown")
        lab = re.search(r"\\label\{(.*?)\}", b)
        print(f"  figure {i}: {kind:16s} label={lab.group(1) if lab else 'NONE'}")

    print()
    print("=== item 14: rasterize the pages carrying figures 1 and 2 ===")
    pdf = SUB / "paper_v2.pdf"
    out = ROOT / "scratchpad" / "figcheck"
    out.mkdir(parents=True, exist_ok=True)
    for pg in (1, 2, 7, 8):
        r = subprocess.run(["pdftoppm", "-f", str(pg), "-l", str(pg), "-r", "60", "-png",
                            str(pdf), str(out / f"p{pg}")], capture_output=True)
        made = sorted(out.glob(f"p{pg}*.png"))
        size = made[0].stat().st_size if made else 0
        print(f"  page {pg}: rc={r.returncode} png={'yes' if made else 'NO'} bytes={size}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
