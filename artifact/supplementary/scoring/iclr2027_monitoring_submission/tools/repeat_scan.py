r"""repeat_scan -- no phrase is told to the reader three times.

R86 item 2.6. Two results are stated in near-identical words all over the paper: the
superseded-names lookup matching the smallest model, and the 42.3% retention. Saying a thing
twice is emphasis; saying it a third time in the same words is a paper repeating itself.

WHAT IT DECIDES. Any 9-gram that occurs in THREE OR MORE distinct places in the gated region
is a VIOLATION. Two occurrences pass, which is what the rule intends: one exact frozen
statement plus one paraphrase elsewhere.

WHY 9. Shorter windows fire on ordinary connective English ("of the store's own
self-description"); longer ones miss a restatement that varies one word. Nine is the length
the R86 order fixed, and it is recorded here rather than tuned.

NORMALIZATION. LaTeX comments are stripped, then math, macros and cross-references are
reduced to single placeholders, then case and punctuation are dropped. So a repetition that
differs only in whether a number is typeset in math mode is still caught.

Usage: python tools/repeat_scan.py paper_v2.tex
Exit 0 when nothing repeats three times, 1 otherwise.
"""
import re
import sys
import pathlib
import collections

N = 9
# R133 RULINGS 1 (2026-09-21): the thesis sentence no longer repeats (Section 1 and the Conclusion in the author's words), so the exemption R133 added is removed;
# the rule runs unexempted (EXEMPT is empty).
EXEMPT = []


def gated_region(tex):
    t = tex[tex.index(r"\begin{document}"):]
    end = t.index(r"\begin{thebibliography}") if r"\begin{thebibliography}" in t else len(t)
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in t[:end].split("\n"))


def normalize(t):
    # Figure source is not prose. A pgfplots options block repeats by construction and no
    # reader ever sees it; stripping it is what keeps this gate about the writing.
    t = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", " FIGURE ", t, flags=re.S)
    t = re.sub(r"\\(?:ref|label|cite[tp]?|eqref)\{[^}]*\}", " XREF ", t)
    t = re.sub(r"\$[^$]*\$", " NUM ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?(?:\{[^}]*\})?", " ", t)
    t = re.sub(r"[^A-Za-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip().lower()


def main(path):
    tex = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    words = normalize(gated_region(tex)).split()
    grams = collections.defaultdict(list)
    for i in range(len(words) - N + 1):
        grams[" ".join(words[i:i + N])].append(i)

    # a repeat is three or more occurrences that are not merely a sliding overlap
    bad = {}
    for g, pos in grams.items():
        spread = [p for k, p in enumerate(pos) if k == 0 or p - pos[k - 1] > N]
        if len(spread) >= 3 and not any(g in e or e in g for e in EXEMPT):   # R133: the one exempt phrase
            bad[g] = spread

    print(f"repeat_scan: {path}")
    print(f"  gated region: begin{{document}} .. bibliography; window {N}; {len(words)} words")
    if not bad:
        print(f"\nPASS -- no {N}-gram occurs in three or more places.")
        return 0
    for g, pos in sorted(bad.items(), key=lambda kv: -len(kv[1])):
        print(f"  x{len(pos)}  {g!r}")
    print(f"\nFAIL -- {len(bad)} {N}-gram(s) in three or more places.")
    return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    raise SystemExit(main(sys.argv[1]))
