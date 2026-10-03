# -*- coding: utf-8 -*-
"""q_scan.py -- the author's Pass 2 rules of 2026-09-15 (registered in reviews/v18/OUTLINE.md section G), checked on the built manuscript.

Body (Sections 1 to 10): (Q-A) every paragraph opens with one plain sentence carrying no numeral (no digit outside a \\ref, \\cite or
\\label; spelled-out numbers are words); (Q-B) at most one interval quoted in prose per paragraph (an interval is a bracketed pair
[a,b]; "both intervals excluding zero" quotes none); (Q-C) the plain-words definitions of the two named terms appear before the terms'
first numeric use ("a lifecycle summary" ... "with the values removed"; "AUROC" ... "the chance that a positive scores above a negative").
Appendix: (Q-D) every \\subsection and \\section opens with a plain sentence carrying no numeral. Tables, figures, listings (Phase 4b), boxes and definitions
are skipped; captions are not paragraphs. Exit 1 on any failure. Usage: python reviews/v18/tools/q_scan.py [paper_v18.tex]
R111 (2026-09-15, the writing pass): Q-A no longer reads a model name (GPT-4.1 mini, GPT-5.6 Luna / Sol, Haiku 4.5, Opus 5, Kimi K3,
mem0ai 1.0.5) as a numeral. Reason: item 61 of the pass replaces "the smallest model" / "the larger model" by the model's name
everywhere, openers included; the rule is about quantities, and a name carries none."""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"


def strip_refs(s):
    s = re.sub(r"\\(ref|cite[pt]?|label|eqref)\{[^}]*\}", " ", s)
    s = re.sub(r"Section~?\\ref\{[^}]*\}|Table~?\\ref\{[^}]*\}|Figure~?\\ref\{[^}]*\}|Appendix~?\\ref\{[^}]*\}|Definition~?\\ref\{[^}]*\}", " ", s)
    return s


def paragraphs(lines, start, end):
    """Prose paragraphs between two line indices, skipping floats, environments, boxes and comments; returns (first_line_no, text)."""
    out, buf, first, depth, in_box = [], [], None, 0, False
    for i in range(start, end):
        raw = lines[i]
        l = re.sub(r"(?<!\\)%.*$", "", raw).rstrip()
        if re.search(r"\\begin\{(table|figure|tikzpicture|tabular|definition|center|itemize|enumerate|listing)", l):   # listing: Phase 4b, a float is not a paragraph
            depth += 1
        if "\\fbox{" in l:
            in_box = True
        skip = depth > 0 or in_box
        if in_box and "\\end{minipage}}" in l:
            in_box = False
        if re.search(r"\\end\{(table|figure|tikzpicture|tabular|definition|center|itemize|enumerate|listing)", l):
            depth = max(0, depth - 1)
        if skip or l.startswith("\\section") or l.startswith("\\subsection") or l.startswith("\\paragraph") or l.startswith("\\label") or l.startswith("\\FloatBarrier") or l.startswith("\\noindent"):
            if buf:
                out.append((first, " ".join(buf))); buf, first = [], None
            continue
        if not raw.strip():
            if buf:
                out.append((first, " ".join(buf))); buf, first = [], None
            continue
        if not l.strip():
            continue                                  # a comment-only line is not a paragraph break in LaTeX
        if first is None:
            first = i + 1
        buf.append(l.strip())
    if buf:
        out.append((first, " ".join(buf)))
    return out


def first_sentence(text):
    # R126 (2026-09-19): a sentence also ends at '.}' so a bold run-in claim sentence (\claim{...}) is read as the paragraph's opener; the rule's
    # text is unchanged (every paragraph opens with one plain sentence carrying no numeral). Recorded in reviews/v22/REPORT_R126.md, Phase 5.3.
    return re.split(r"(?:(?<=[.!?])|(?<=[.!?]\}))\s+(?=[A-Z\\$(`])", text)[0]


MODEL_NAMES = r"GPT-4\.1 mini|GPT-5\.6 (Luna|Sol)|Haiku[ ~]4\.5|Opus[ ~]5|Kimi K3|mem0ai 1\.0\.5|Mem0"   # Mem0 the backend, Phase 4


def has_numeral(s):
    s = strip_refs(s)
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)          # macro names
    # Writing pass Phase 1 (2026-09-15, R111): a model name is not a numeral. Item 61 of paper_v18_writing_prompt.md replaces
    # "the smallest model" / "the larger model" by the model's name everywhere, openers included; the rule is about quantities.
    s = re.sub(MODEL_NAMES, " ", s)
    return re.search(r"\d", s) is not None


def n_intervals(s):
    return len(re.findall(r"\[[+\-]?\d+\.\d+\s*,\s*[+\-]?\d+\.\d+\]", s))   # a bracketed pair of decimals; [0,1] is a range


def main():
    tex = SUB / (sys.argv[1] if len(sys.argv) > 1 else "paper_v22.tex")   # v19 (R112)
    lines = tex.read_text(encoding="utf-8").split("\n")
    intro = next(i for i, l in enumerate(lines) if l.startswith("\\section{Introduction}"))
    end = next(i for i, l in enumerate(lines) if "main-text-end" in l)
    appx = next(i for i, l in enumerate(lines) if l.strip() == "\\appendix")
    fails = []
    body = paragraphs(lines, intro, end)
    for ln, text in body:
        fs = first_sentence(text)
        if has_numeral(fs):
            fails.append(f"Q-A L{ln}: paragraph opens with a numeral :: {fs[:110]}")
        k = n_intervals(text)
        if k > 1:
            fails.append(f"Q-B L{ln}: {k} intervals in one paragraph :: {text[:110]}")
    flat = " ".join(l for l in lines[intro:end] if not l.lstrip().startswith("%"))
    for term, definition in (("lifecycle summary", "with the values removed"), ("AUROC", "the chance that a positive scores above a negative")):
        i_def = flat.find(definition); i_num = None
        for m in re.finditer(r"\$[+\-]?\d", flat):
            if flat.rfind(term, 0, m.start()) != -1:
                i_num = m.start(); break
        if i_def == -1 or (i_num is not None and i_def > i_num):
            fails.append(f"Q-C: the plain definition of '{term}' does not precede its first numeric use")
    # appendix: the first paragraph after each \section / \subsection heading
    heads = [i for i in range(appx, len(lines)) if re.match(r"\\(sub)?section\{", lines[i])]
    for h in heads:
        nxt = next((j for j in heads if j > h), len(lines))
        paras = paragraphs(lines, h + 1, nxt)
        if not paras:
            continue
        ln, text = paras[0]
        fs = first_sentence(text)
        if has_numeral(fs):
            fails.append(f"Q-D L{ln} ({re.search(r'section\{([^}]*)', lines[h]).group(1)[:40]}): appendix section opens with a numeral :: {fs[:100]}")
    print(f"q_scan: {len(body)} body paragraphs, {len(heads)} appendix headings")
    for f in fails:
        print("  " + f)
    print("q_scan: " + ("PASS" if not fails else f"{len(fails)} FAILURES"))
    sys.exit(1 if fails else 0)


def selftest():
    """R127 (2026-09-20): the '.}' splitter (R126) hides nothing. One line each: (1) a plain \\claim lead followed by a numeral sentence is not a
    Q-A hit; (2) a \\claim lead that itself carries a numeral is; (3) a 40-word sentence after a \\claim lead is still its own sentence (the 35-word
    rule of readability_wp.py and prose_scan's 40-word rule see it), not merged into the lead."""
    lead, nums = "\\claim{Models read the names more than the counts.}", "On the counterfactual set, removing counts leaves mini within $0.01$ of its score."
    assert not has_numeral(first_sentence(lead + " " + nums)), "Q-A must not fire on a plain claim lead"
    assert has_numeral(first_sentence("\\claim{Mini loses $0.12$ on counts alone.} " + nums)), "Q-A must fire on a claim lead carrying a numeral"
    long = "The " + "very " * 37 + "long sentence."
    parts = re.split(r"(?:(?<=[.!?])|(?<=[.!?]\}))\s+(?=[A-Z\\$(`])", lead + " " + long)
    assert len(parts) == 2 and len(parts[1].split()) == 40, "a long sentence after a claim lead must stay its own sentence"
    print("q_scan selftest: PASS (a plain claim lead is the opener; a numeral in the lead fires Q-A; a 40-word sentence after the lead is still one 40-word sentence)")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest(); sys.exit(0)
    main()
