"""claims_diff -- mechanical re-execution of the CLAIMS_DIFF gate.

WHY THIS EXISTS. `CLAIMS_DIFF.md` has been hand-authored at every pass, and its own headline
("all 62 entries") drifted out of date without anything catching it. This tool re-executes
the parts of that audit a machine can decide, so the hand-written narrative is checked rather
than trusted.

WHAT IT DECIDES, and what it deliberately does not.
  1. ENTRY COUNT      every `## CL-*` heading is counted, and any prose in CLAIMS.md or
                      CLAIMS_DIFF.md claiming a different total is a VIOLATION.
  2. COVERAGE         every CL id in CLAIMS.md appears somewhere in CLAIMS_DIFF.md, so no
                      claim is silently unmapped.
  3. U-BLOCKS         each untouchable block appears in paper_v2.tex EXACTLY ONCE and
                      byte-identically. Relocation is allowed; disappearance and duplication
                      are not.
  4. BANNED CLAIM     the Reframe 5 words are absent from main text outside the held region
     WORDS            (main text = \begin{document} to the bibliography; R93 note at the check).
  5. STRENGTH         NOT decided here. Whether a reworded sentence still carries its
                      registered strength is a reading, and readings stay with the human
                      audit in CLAIMS_DIFF.md. This tool reports the count of entries whose
                      TEXT is no longer verbatim so that audit has a denominator.

Line endings are normalized to LF before any comparison.

Usage: python tools/claims_diff.py            (exit 0 only when there are zero VIOLATIONs)
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
SUB = HERE.parent
CLAIMS = SUB / "CLAIMS.md"
DIFF = SUB / "CLAIMS_DIFF.md"
# R90 (2026-09-11): the working lineage is paper_v3.tex; paper_v2.tex is frozen at f4c5b2c.
# R92 (2026-09-11): the working lineage is paper_v4.tex; paper_v3.tex is frozen at abac307 (R91-6).
# R93 (2026-09-11): the working lineage is paper_v5.tex; paper_v4.tex is frozen at fdd34c8 (R92-6).
# R96 (2026-09-12): the working lineage is paper_v6.tex; paper_v5.tex is the R93 close.
# R97 (2026-09-13): the working lineage is paper_v7.tex; paper_v6.tex is the R96 close.
# R98 (2026-09-13): the working lineage is paper_v8.tex (the CF-2 landing); paper_v7.tex is the R97 close.
# An optional first argument names another manuscript.
TEX = SUB / (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "paper_v8.tex")

U_BLOCKS = {
    "U1": "This is an inversion at every scale, not a below-chance score at every scale.",
    "U2": ("Scope: the negative index effect is measured; the single-channel ablations do "
           "not identify its cause."),
    "U3": "The association does not identify which rendered feature causes the inversion.",
    "U4": "This law is directional but not mechanistic",
    # R126 (2026-09-19, the brief's Phase 2.3): U5 re-pinned to the Section 6 sentence of the paragraph that carries the four U5 conditions (the readable
    # body); was "What triggers the loss under the constrained rendering is unresolved" (R124 A2, the Limitations pointer), before that "below-chance
    # mechanism remains unresolved" (C090). CLAIMS.md R126 block shows old and new.
    # R128 (2026-09-20, the author's A2): the sentence in its corrected form (tab:dist: positives slightly below negatives); was "Scores compress toward a low value, but the trigger remains unresolved." (R126).
    "U5": "Scores collapse onto a few low values, with positives slightly below negatives, and the trigger remains unresolved.",
    "U6": "which we record as a failed prediction",
    "U7": "so bounds correspondence alone",
}

BANNED = [r"\bdesign law\b", r"\blaws?\b", r"\bprecondition\b"]


def norm(s):
    return re.sub(r"\s+", " ", s.replace("\r\n", "\n"))


def main():
    claims = CLAIMS.read_text(encoding="utf-8", errors="replace")
    diff = DIFF.read_text(encoding="utf-8", errors="replace")
    tex = TEX.read_text(encoding="utf-8", errors="replace")
    # R105 (2026-09-14): --extra-tex=<file> adds the supplement to the U-block count, so a U-block the author moved to the
    # supplement (U6, Section S.9) is still checked exactly once across the paper and the supplement together.
    extra = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--extra-tex=")]
    flat = norm(tex + "".join((SUB / e).read_text(encoding="utf-8", errors="replace") for e in extra))
    viol = []

    ids = re.findall(r"(?m)^## (CL-[A-Za-z0-9-]+)", claims)
    n = len(ids)
    print(f"claims_diff: {n} CL entries in CLAIMS.md")

    # 1. entry count claimed anywhere in prose
    for name, blob in (("CLAIMS.md", claims), ("CLAIMS_DIFF.md", diff)):
        for m in re.finditer(r"(?:all |Entry count: )(\d+) entries", blob):
            if int(m.group(1)) != n:
                viol.append(f"{name} states {m.group(1)} entries; the real count is {n}")

    # 2. coverage
    unmapped = [i for i in ids if i not in diff]
    if unmapped:
        viol.append(f"{len(unmapped)} CL ids absent from CLAIMS_DIFF.md: "
                    f"{', '.join(unmapped[:6])}")
    print(f"  coverage: {n - len(unmapped)}/{n} ids mapped in CLAIMS_DIFF.md")

    # 3. U-blocks exactly once, byte-identical
    for tag, s in U_BLOCKS.items():
        c = flat.count(norm(s))
        mark = "ok" if c == 1 else "VIOLATION"
        print(f"  {tag}: {c} occurrence(s) {mark}")
        if c != 1:
            viol.append(f"{tag} appears {c} times in paper_v2.tex; must be exactly once")

    # 4. banned claim words in main text outside the held region
    # R93 (2026-09-11): the region ends at the bibliography, not at \appendix. Reframe 5 bars the
    # words from CLAIM prose; a journal title in a \bibitem ("Washington Law Review", nissenbaum2004)
    # is not a claim, and code_scan/repeat_scan already gate "begin{document} .. bibliography".
    # Before this the bibliography sat inside the region only because no entry carried a banned word.
    body_end = tex.index(r"\begin{thebibliography}") if r"\begin{thebibliography}" in tex else tex.index(r"\appendix")
    body = tex[tex.index(r"\begin{document}"):body_end]
    body = re.sub(r"(?m)^\s*%.*$", "", body)
    held_start = body.index(r"\begin{abstract}") if r"\begin{abstract}" in body else 0
    held_end = body.index(r"\section{Related work}") if r"\section{Related work}" in body \
        else held_start
    gated = body[:held_start] + body[held_end:]
    for pat in BANNED:
        hits = re.findall(pat, gated, re.I)
        if hits:
            viol.append(f"banned claim word {pat} in gated main text: {hits[:4]}")
    print(f"  banned claim words outside the held region: "
          f"{sum(len(re.findall(p, gated, re.I)) for p in BANNED)}")

    # 5. denominator for the human audit
    texts = re.findall(r'(?m)^TEXT\s+\| "(.*?)"\s*$', claims)
    verbatim = sum(1 for t in texts if norm(t) in flat)
    print(f"  entries whose TEXT is still verbatim in paper_v2: {verbatim}/{len(texts)} "
          f"(the rest are the reworded set the human audit dispositions)")

    print()
    if viol:
        print(f"VIOLATIONS ({len(viol)}):")
        for v in viol:
            print("  ", v)
        return 1
    print("PASS -- 0 VIOLATIONs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
