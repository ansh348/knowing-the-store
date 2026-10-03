r"""code_scan -- no internal identifier reaches the page a reviewer reads.

R86 item 2.5. The main text (Section 1 to Section 8), the abstract, and the AI use and
reproducibility statements carry ZERO internal identifiers. The registrations, ledgers and
row files are full of them and that is fine; they are the artifact's vocabulary, not the
paper's. Appendix G is the registration record and keeps its codes, and Appendix F.1 is the
glossary that decodes them, so both are exempt by scope.

WHAT IT DECIDES.
  1. IDENTIFIERS. A deviation number, a program number, or a registered-item code anywhere in
     the gated region is a VIOLATION. These are unambiguous and carry no allowlist.
  2. JARGON. The internal words STYLE_SPEC S10 names -- lane, cell, arm, provenance, lineage
     -- are a VIOLATION in the gated region. "prior", "committed" and "registered" have
     ordinary English senses the paper legitimately uses ("prior work", "a prior store",
     "preregistered"), so they are checked against a small allowlist of collocations and
     flagged only outside it.

SCOPE. `\begin{document}` through `\label{main-text-end}`, plus the two statements that follow
it, with LaTeX comments stripped first. Comments are where this program records its own
reasoning and they never reach the reader.

Usage: python tools/code_scan.py paper_v2.tex
Exit 0 when the gated region is clean, 1 on any hit.
"""
import re
import sys
import pathlib

IDENTIFIERS = [
    (r"\bD-R\d+-\d+\b", "deviation number"),
    (r"\bD\d{1,3}-E1R?\b", "deviation number"),
    (r"\bD-E1R-\d+\b", "deviation number"),
    (r"\bR\d{2}-[A-Z0-9]", "program identifier"),
    (r"\bR\d{2}\b(?!\s*(?:personas|questions|items))", "program identifier"),
    (r"\b(?:NS|XV|CF|SW|CAL|QP|XP|NB)-\d+\b", "registered-item code"),
    (r"\bNB\d\b", "baseline code"),
    (r"\bP-M1[abc]\b", "registered-item code"),
    (r"\bAUX-[A-Z0-9-]+\b", "ledger key"),
    (r"\bE1-[A-Z]{2,}\b", "internal study code"),
    (r"\bE0\b|\bE1\b|\bE2\b", "internal study code"),
]

JARGON = [
    (r"\blanes?\b", "lane"),
    (r"\bcells?\b", "cell"),
    (r"\barms?\b", "arm"),
    (r"\bprovenances?\b", "provenance"),
    (r"\blineages?\b", "lineage"),
]

# "prior", "committed" and "registered" are ordinary English here; these are the senses the
# paper is entitled to use. Anything outside them is reported.
ALLOWED = [
    r"prior work", r"a prior\b", r"prior lifecycle", r"prior system", r"prior store",
    r"prior apparatus", r"in that prior", r"the prior",
    r"preregistered", r"preregistration",
    r"registered prediction", r"registered failure", r"registered predictions",
    r"as registered", r"registered with", r"registered before",
    # R97 (2026-09-13): "the registered coverage floor of one half" is inside the SIDE
    # registration's frozen Mem0 descriptive text, which prints verbatim in Section 5.3 under
    # ADDENDUM_SIDE.md Amendment 1 (R78-2c: frozen registered wording ships verbatim; style
    # yields). The collocation is permitted; the bare word stays gated everywhere else.
    r"registered coverage floor",
    # R101 (2026-09-13): two collocations inside the DS registration's frozen Section 7 paragraph
    # (registrations/ADDENDUM_DS.md section PAPER, frozen a5a2036; R78-2c). The bare words stay gated.
    r"committed obligation score", r"registered detector threshold",
]


def gated_region(tex):
    t = tex[tex.index(r"\begin{document}"):]
    # main text plus the two uncounted statements, which item 2.5 gates as well
    end = t.index(r"\begin{thebibliography}") if r"\begin{thebibliography}" in t else len(t)
    t = t[:end]
    t = "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in t.split("\n"))
    # Cross-reference keys are not prose. `tab:matched-cell` is a label a reader never sees,
    # and reading it as the word "cell" would make the gate unpassable for a correct paper.
    # The argument is blanked rather than deleted so line numbers stay meaningful.
    t = re.sub(r"\\(?:ref|label|cite[tp]?|eqref)\{([^}]*)\}",
               lambda m: "\\ref{" + " " * len(m.group(1)) + "}", t)
    return t


def main(path):
    tex = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    region = gated_region(tex)
    hits = []

    for pat, what in IDENTIFIERS + JARGON:
        for m in re.finditer(pat, region):
            line = region.count("\n", 0, m.start()) + 1
            ctx = region[max(0, m.start() - 45):m.end() + 45].replace("\n", " ")
            hits.append((what, m.group(0), line, ctx))

    for word in ("prior", "committed", "registered"):
        for m in re.finditer(r"\b" + word + r"\w*\b", region):
            span = region[max(0, m.start() - 30):m.end() + 30]
            if any(re.search(a, span, re.I) for a in ALLOWED):
                continue
            line = region.count("\n", 0, m.start()) + 1
            ctx = region[max(0, m.start() - 45):m.end() + 45].replace("\n", " ")
            hits.append(("jargon sense", m.group(0), line, ctx))

    print(f"code_scan: {path}")
    print(f"  gated region: begin{{document}} .. bibliography, comments stripped")
    if not hits:
        print("\nPASS -- no internal identifier or jargon token in the gated region.")
        return 0
    for what, tok, line, ctx in hits:
        print(f"  [{what}] {tok!r} at region line {line}")
        print(f"      ...{ctx.strip()}...")
    print(f"\nFAIL -- {len(hits)} hit(s).")
    return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    raise SystemExit(main(sys.argv[1]))
