"""Independent numeric-occurrence re-scan of paper.tex against the central number record.

Direction A: every numeric token printed by the manuscript is either (i) present in the
central ledger family, or (ii) falls in a declared non-research exclusion class.

Exclusion classes frozen by the v0.8/v0.9 closing audits: automatic section/page numbers,
TeX dimensions and plot geometry, package versions, table column specs, claim-comment
identifiers, and bibliographic metadata (years, volumes, pages, arXiv identifiers).
"""
import re, pathlib, sys

SUB = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "paper.tex")
LEDGERS = [
    pathlib.Path("../e1_metamemory/NUMBERS.md"),
    pathlib.Path("../e1xv_crossvendor/NUMBERS_E1XV.md"),
    pathlib.Path("../e1qp_questionprior/NUMBERS_E1QP.md"),
]

NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")


def norm(tok):
    t = tok.replace(",", "")
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return t or "0"


def ledger_numbers():
    s = set()
    for p in LEDGERS:
        if not p.exists():
            print(f"  !! missing ledger {p}")
            continue
        for m in NUM.finditer(p.read_text(encoding="utf-8", errors="replace")):
            s.add(norm(m.group()))
    return s


def main():
    tex = SUB.read_text(encoding="utf-8")
    tex = tex[tex.index("\\begin{document}"):]

    # 1. pull the bibliography out first (metadata exclusion class)
    b0 = tex.index("\\begin{thebibliography}")
    b1 = tex.index("\\end{thebibliography}")
    bib = tex[b0:b1]
    tex = tex[:b0] + tex[b1:]

    # 2. pull tikz/pgfplots blocks out (plot-geometry exclusion class)
    tikz = []
    tex = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}",
                 lambda m: (tikz.append(m.group(0)), "\n")[1], tex, flags=re.S)

    # 3. strip comments (claim identifiers) and layout-only constructs
    tex = "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in tex.split("\n"))
    # LaTeX thin-space thousands separator: 18{,}936 is the single token 18936
    tex = tex.replace("{,}", ",")
    # deviation / registration identifiers (D86, D93, ...) are an identifier class
    tex = re.sub(r"\bD\d{1,3}\b", " ", tex)
    drop = [
        r"p\{[^}]*\}",                       # column specs
        r"\\setlength\{[^}]*\}\{[^}]*\}",    # lengths
        r"\\multicolumn\{\d+\}",             # spans
        r"\\newtheorem[^\n]*",
        r"\\(?:v|h)space\{[^}]*\}",
        r"0\.\d+\\linewidth",
        r"\\hspace\*?\{[^}]*\}",
        r"\\char\d+",                        # literal backtick escapes in the prompt box
        r"\\begin\{minipage\}\[?t?\]?\{[^}]*\}",
        r"\\thebibliography\{\d+\}",
    ]
    for d in drop:
        tex = re.sub(d, " ", tex)

    ledger = ledger_numbers()
    hits = [(m.group(), m.start()) for m in NUM.finditer(tex)]
    counts = {}
    where = {}
    for tok, pos in hits:
        t = norm(tok)
        counts[t] = counts.get(t, 0) + 1
        where.setdefault(t, pos)

    unaccounted = {t: c for t, c in counts.items() if t not in ledger}

    print(f"manuscript: {SUB}")
    print(f"central-ledger distinct tokens: {len(ledger)}")
    print(f"manuscript numeric occurrences (research classes): {len(hits)}")
    print(f"distinct tokens: {len(counts)}   unaccounted: {len(unaccounted)}")
    print()
    print("DIRECTION A -- tokens with no central-ledger match:")
    if not unaccounted:
        print("  (none)")
    for t in sorted(unaccounted, key=lambda x: -unaccounted[x]):
        p = where[t]
        ctx = re.sub(r"\s+", " ", tex[max(0, p - 70):p + 60])
        print(f"  {t:>12s} x{unaccounted[t]:<3d} | ...{ctx}...")
    print()
    bibn = {norm(m.group()) for m in NUM.finditer(bib)}
    tk = {norm(m.group()) for m in NUM.finditer("".join(tikz))}
    print(f"EXCLUSION CLASS bibliographic metadata: {len(bibn)} distinct tokens (not audited as research)")
    print(f"EXCLUSION CLASS tikz/pgfplots: {len(tk)} distinct; not in ledger: "
          f"{sorted(x for x in tk if x not in ledger)}")


main()
