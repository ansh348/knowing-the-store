"""slogan_scan -- sentence-repeat and style-rule gate for the paper_v2 lineage (R78-2b).

Checks, in order:
  1. S7  no sentence (>= 40 chars, comment-stripped, bib/tikz excised) appears twice;
  2. the pinned untouchable blocks (U1-U7 markers) each appear EXACTLY once;
  3. S8  no em dash (---) in main text (\\begin{document}..\\appendix), after removing
         the declared exemptions: the intro [AUTHOR-1]-DRAFT skeleton region, byte-identical
         untouchable blocks, and structural table placeholders ("& --- \\\\");
  4. S9  no contrastive ", not " / not..but / but..not / "does not merely" in main
         text outside the declared exemptions (byte-identical blocks, content-intact
         limitations, the [AUTHOR-1]-approved abstract sentence);
  5. S10 no internal program vocabulary (lanes/branches/cap-stop/ships/freeze/frozen/
         gate/cells-as-shorthand/registration codes) in main text outside the declared
         exemptions (frozen-registered wording; intact limitations; the carried AI-use
         and reproducibility statements; float labels).

Exemption classes (each string below carries its class):
  BYTE-IDENTICAL      U-blocks carried byte-identical from the frozen lineage;
  INTACT-LIMITATION   Section 7.2 sentences carried verbatim in content;
  CARRIED-STATEMENT   the AI-use and reproducibility statements, carried by order;
  FROZEN-REGISTERED   frozen registered branch wording ships verbatim; style yields
                      (R78-2c ruling: byte-identity outranks style wherever a U-block
                      or frozen registered wording appears, main text included);
  [AUTHOR-1]-APPROVED      landed hand-pass text, integrated verbatim;
  STRUCTURAL          table placeholders and float labels, not prose.
Exit 0 only if all five checks pass.

Usage: python tools/slogan_scan.py paper_v2.tex
"""
import re, pathlib, sys

tex = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")

# comment-strip first so the preamble comment mentioning \begin{document} cannot
# confuse the region anchors
stripped = "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in tex.split("\n"))
doc = stripped[stripped.index("\n\\begin{document}"):]
main = doc[:doc.index("\\appendix")]

fails = []

# ---- exemption registry (audit trail: why each string is allowed) -------------------
EXEMPT_S8 = [
    # U7 (D-R74-19 byte-identical SW-2 bound sentence)
    "that specificity---per-category correspondence is not necessary",
    # structural empty-CI placeholder in tab:e1 (committed table convention)
    "& --- \\\\",
]
EXEMPT_S9 = [
    # U1 (byte-identical inversion disclosure)
    "This is an inversion at every scale, not a below-chance score at every scale.",
    # C091 (content-intact limitation)
    "is a measured resolution limit, not evidence that the label is absent",
    # U4 (byte-identical hedge)
    "This law is directional but not mechanistic",
    # L652 (content-intact limitation carrying the frozen NS-2 failure wording)
    "excludes zero on the Opus 5 lane but not on the mini lane",
    # [AUTHOR-1]-approved abstract sentence (landed verbatim, R78-2b)
    "ranks items well but cannot yet be trusted as a probability",
    # R107 (2026-09-14): the author's replacement abstract, verbatim by instruction; its closing sentence
    "Backends should return tags, not masks, and maintain the list",
    # R110 (2026-09-15): the author's abstract v7, the downstream sentence in the author's words (reviews/v18/src/abstract_v18.tex; CLAIMS.md R110 block)
    "reaches more forbidding records but does not reduce stale answers",
    # Phase 0 of the writing pass (2026-09-15): the author's abstract v8 (paper_v18_writing_prompt.md item 6, addendum), verbatim;
    # the thesis phrase is ordered kept ("because it is the paper's claim"); reviews/v18/src/abstract_v18.tex
    "read the summary by its names, not by its counts",
    # R111 Phase 2 (2026-09-15): the author's own sentence of paper_v18_writing_prompt.md section 15 for Section 6's own-tags paragraph, verbatim
    "the store's tags reach more of the forbidding records, not that there are more tags",
    # R111 Phase 3 (2026-09-15): the author's contributions list (paper_v18_writing_prompt.md item 5, its third bullet), verbatim
    "read the summary's \\emph{names}, not its counts",
    # R111 Phase 4 (2026-09-15): the author's sentence of paper_v18_writing_prompt.md item 63 (its addendum) for Section 5's opener, verbatim
    "tracks the attribute names in the summary, not the counts beside them",
    # R111 Phase 4c (2026-09-15): the author's cold-read ruling, items 6 and 4, verbatim: the third contribution and Section 8's FOK sentence
    "We show monitors read names, not counts",
    "but not a single deleted record",
    # R133 (2026-09-21): the author's abstract swap S2 carried 'but not when all items are pooled, where the models stay'; R134 (2026-09-21): that sentence left with the
    # author's abstract (reviews/v23/tools/port_r134.py, unit abstract; RULING 2), so the entry is retired (gate_edits_r134.py); the new abstract carries no S9 pattern.
]
# R133 RULINGS 1 (2026-09-21): the thesis sentence no longer repeats (Section 1 and the Conclusion in the author's words), so the S7 exemption R133 added is removed;
# S7 runs unexempted. The S9 entry above for S2's abstract sentence stays (the ruling kept the abstract).
EXEMPT_S7 = []
# FROZEN-REGISTERED (R78-2c ruling, CONFIRMED): frozen branch text ships verbatim;
# S8-S10 yield to it, the same logic as S8's appendix exemption. Applied to every check.
EXEMPT_FROZEN_REGISTERED = [
    # the cap-stop branch sentence (AUX-R74-X4)
    # R97 (2026-09-13): the SIDE registration's frozen S1-P1 held reading and the frozen Mem0
    # descriptive text print in Section 5.3 under ADDENDUM_SIDE.md Amendment 1 (R78-2c: frozen
    # registered wording ships verbatim; style yields). S1-P1 carries ", not of the store alone"
    # (S9); the Mem0 text carries "registered" and "verdict" (S10/prose V) and runs over 40 words.
    "Given the manifest's names for what it holds, the store no longer inverts the benefit by the margin it did; the inversion was a property of the index the store was handed, not of the store alone.",
    "On Mem0 the name-bearing index could be built for $49.4$ percent of the store's entries under the lexical-required mapping the spot-check forced (two-channel precision $0.567$); below the registered coverage floor of one half, its coverage gain of $+0.3006$ (interval $[+0.2208,+0.3728]$; \\trueidx{} $-0.0969$) is reported and carries no verdict.",
    # R98 (2026-09-13): the CF-2 registration's frozen P1 HOLDS [MAIN] sentence (Section 7) and P3 HOLDS
    # [MAIN] sentence (Section 6), registrations/ADDENDUM_CF2.md section 8, placeholders filled from
    # NUMBERS_CF2.md; R78-2c. P1 runs to 46 words.
    "On $148$ questions written before any version of the store existed, and asked of three versions of the same store that differ in one attribute each, the smallest model's obligation judgment reaches $0.7167$ against the $0.5$ a question-only reader attains here, with an interval of $[+0.1494,+0.2846]$.",
    "Naming retracted and expired content lifts Haiku 4.5's judgment on those states from $0.5638$ to $0.8649$ on the store-counterfactual set ($60$ questions), a paired gain of $+0.3010$ with interval $[+0.2268,+0.3721]$.",
    # R101 (2026-09-13): the DS registration's frozen Section 7 paragraph and the RESP L1-P1 held reading
    # (R78-2c; NUMBERS_DS.md AUX-DS-PARAGRAPH-PRINTED, NUMBERS_RESP.md AUX-RESP-PRINTED).
    "Acting on the obligation judgment changes what a bounded view carries. The store's truthful metadata flags $82$ of the $104$ forbidding records; the other $22$ ($18$ retraction-derived, $4$ expiry-derived) are a store-side fact of the kind Table~\\ref{tab:believed} records, retrieve as active, and are out of reach of any policy that acts on the metadata. On the $104$ obligation items, the five-entry similarity view contains the forbidding record for $0.5192$; a gold-label fetch of the store's lifecycle records for the obligation's own attribute reaches $0.9519$, $0.4327$ above retrieval alone and short of the $0.50$ bar; gated on the smallest model's committed obligation score at its base rate, the fetch reaches $0.8173$, retaining $0.7561$ of that gain on the supersession-derived items (interval $[0.610, 0.872]$; $[0.562, 0.939]$ with questions grouped by user profile), short of the $60\\%$ bar under the weaker reading. The superseded-names lookup reaches $0.8173$ at the same fetch budget, within tolerance of the model. Naming the retracted and expired attributes raises the gated reach on those obligations only from $0.7805$ to $0.7805$: the gate elicited under the counting summary does not fire on them. The coverage gate at its base rate costs $0.0287$ of coverage on the items whose licensed record the store holds, within tolerance. With the forbidding record in view and tagged, the smallest model gives the stale value as the answer in $0$ of $82$ cases at the registered detector threshold ($11$ of $82$ at the join's gold threshold; $6$ of $17$ where the record printed as active) (Appendix~\\ref{app:resp}).",
    "Removing the target's own name and its nearest neighbours from the superseded-names section costs the smallest model $0.3262$ of its supersession discrimination ($0.8572$ to $0.5310$; interval $[-0.3991,-0.2548]$, and $[-0.4327,-0.2167]$ with questions grouped by user profile): the obligation is read off the name, as the manuscript says.",
]
EXEMPT_S10 = [
    # INTACT-LIMITATION (L650, L652)
    "all rows reuse the same authored cell",
    "excludes zero on the Opus 5 lane but not on the mini lane",
    "which we record as a failed prediction",
    "has now been measured on three lanes",
    "at chance on the mini and Opus 5 lanes",
    # CARRIED-STATEMENT (AI use / reproducibility, verbatim by order); the phrase
    # "frozen decision rules" also covers the landed introduction's [AUTHOR-1]-APPROVED use
    "frozen decision rules",
    "frozen registrations",
    # STRUCTURAL float label, not prose
    "tab:matched-cell",
]

def cut_regions(text):
    # intro [AUTHOR-1]-DRAFT skeleton region is exempt from S8-S10 until its hand-pass
    m = re.search(r"\\skelhead\{Introduction.*?\\skelfoot", text, re.S)
    return text.replace(m.group(0), " ") if m else text

# ---- 1. sentence dedup over the whole document --------------------------------------
body = doc
b0, b1 = body.index("\\begin{thebibliography}"), body.index("\\end{thebibliography}")
body = body[:b0] + body[b1:]
body = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", " ", body, flags=re.S)
sentences = {}
for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", body)):
    s = s.strip()
    if len(s) >= 40:
        sentences[s] = sentences.get(s, 0) + 1
dups = {s: c for s, c in sentences.items() if c > 1 and s not in EXEMPT_S7}   # R133: the one exempt sentence (EXEMPT_S7)
for s, c in dups.items():
    fails.append(f"S7 duplicate sentence x{c}: {s[:90]!r}")

# ---- 2. pinned exactly-once blocks --------------------------------------------------
PINNED = [
    "This is an inversion at every scale, not a below-chance score at every scale.",
    "Scope: the negative index effect is measured; the single-channel ablations do not identify its cause.",
    "The association does not identify which rendered feature causes the inversion.",
    "This law is directional but not mechanistic",
    "Scores collapse onto a few low values, with positives slightly below negatives, and the trigger remains unresolved.",   # R128 (2026-09-20): U5 in the author's corrected form (A2); R126: "Scores compress toward a low value, but the trigger remains unresolved."; R124 A2: "What triggers the loss under the constrained rendering is unresolved"; before that "below-chance mechanism remains unresolved"
    "which we record as a failed prediction",
    "so bounds correspondence alone",
]
flat = re.sub(r"\s+", " ", doc)
# R105 (2026-09-14): --extra-tex=<file> adds the supplement to the pinned-block count (U6 moved to Section S.9 on the
# author's order; it must still occur exactly once across the paper and the supplement together; claims_diff does the same).
_extra = "".join(pathlib.Path(a.split("=", 1)[1]).read_text(encoding="utf-8") for a in sys.argv[2:] if a.startswith("--extra-tex="))
_extra_stripped = "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in _extra.split("\n"))
flat_all = flat + " " + re.sub(r"\s+", " ", _extra_stripped)
for p in PINNED:
    c = flat_all.count(p)
    if c != 1:
        fails.append(f"PINNED block count {c} != 1: {p[:70]!r}")

# ---- 3. S8 em dashes ----------------------------------------------------------------
region = cut_regions(main)
for e in EXEMPT_S8 + EXEMPT_FROZEN_REGISTERED:
    region = region.replace(e, " ")
n_em = region.count("---")
if n_em:
    for x in re.finditer(r"[^\n]{0,50}---[^\n]{0,50}", region):
        fails.append(f"S8 em dash: ...{re.sub(r'  +', ' ', x.group(0))[:100]}...")

# ---- 4. S9 contrastives -------------------------------------------------------------
region9 = cut_regions(main)
for e in EXEMPT_S9 + EXEMPT_FROZEN_REGISTERED:
    region9 = region9.replace(e, " ")
flat9 = re.sub(r"\s+", " ", region9)
pats = [r", not ", r"\bnot\b[^.]{0,70}\bbut\b", r"\bbut\b[^.]{0,50}\bnot\b",
        r"does not merely"]
for p in pats:
    for x in re.finditer(r"[^.]{0,50}" + p + r"[^.]{0,40}", flat9):
        fails.append(f"S9 contrastive [{p}]: ...{x.group(0)[:100]}...")

# ---- 5. S10 vocabulary --------------------------------------------------------------
region10 = cut_regions(main)
for e in EXEMPT_S10 + EXEMPT_FROZEN_REGISTERED:
    region10 = region10.replace(e, " ")
flat10 = re.sub(r"\s+", " ", region10)
words = [r"\blanes?\b", r"cap-stop", r"\bships\b", r"\bfreeze\b", r"\bfrozen\b",
         r"\bgate\b", r"\bcells?\b", r"\bXV-\d", r"\bNS-\d", r"\bSW-\d"]
for w in words:
    for x in re.finditer(r"[^.]{0,45}" + w + r"[^.]{0,45}", flat10):
        fails.append(f"S10 vocabulary [{w}]: ...{x.group(0)[:95]}...")

# ---- 6. R79 prose gates (tools/prose_scan.py) ---------------------------------------
# Vocabulary, hedge phrases, the 'preregistered' cap, sentence length, near-duplicate
# pairs, parentheticals, and the appendix registration-code rule. Gate scope is read
# from tools/prose_gate_sections.txt (see prose_scan header); the abstract/Section 1
# HELD region reports without gating until the R79 Phase 4 proposal lands.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import prose_scan
p_fails, p_lines = prose_scan.run(sys.argv[1])
for _l in p_lines:
    print(_l)
fails.extend(p_fails)

print(f"duplicate sentences: {len(dups)}")
print(f"pinned exactly-once: {'ALL PASS' if not any(f.startswith('PINNED') for f in fails) else 'FAIL'}")
print(f"S8 em dashes (after exemptions): {n_em}")
print(f"S9/S10 hits (after exemptions): "
      f"{sum(1 for f in fails if f.startswith(('S9', 'S10')))}")
if fails:
    print(f"FAILURES ({len(fails)}):")
    for f in fails:
        print("  ", f)
else:
    print("PASS -- no duplicates; pinned blocks exactly once; S8-S10 clean outside the declared exemptions.")
sys.exit(1 if fails else 0)
