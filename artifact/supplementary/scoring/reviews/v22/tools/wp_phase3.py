# -*- coding: utf-8 -*-
"""wp_phase3.py -- Phase 3 of the writing pass on paper_v18 (paper_v18_writing_prompt.md section 16: the new elements; items 5 with its
addendum, 17 with its addendum, 20 (with item 94's CHANGE row), 22, 30 with its addendum, 56, 57/91, 84, plus 4 and 21 by the author's
ruling of 2026-09-15, and the "reads X" replacements item 61 deferred until the box defines the word), applied to
reviews/v18/src/body_v18.tex after Phase 2 (commit 6dbabdf).

Every edit is an asserted string replacement on the body source (each old string occurs exactly once); no number changes: the per-state
figure and the cross-model table print values that already stand in Tables 2 and 9 (four decimals) and Appendix A, and the two-decimal forms
the cross-model table prints are written to reviews/NUMBERS_WP.md section 3 for trace_scan. Usage: python reviews/v18/tools/wp_phase3.py [--check]
"""
from __future__ import annotations

import io
import pathlib
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v18" / "src"
BODY = SRC / "body_v18.tex"
LEDGER = ROOT / "reviews" / "NUMBERS_WP.md"
PRINTED = []


def r2(s, key):
    q = Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    out = f"{q:+.2f}" if s[0] in "+-" else f"{q:.2f}"
    if out.replace("+", "") != s.replace("+", ""):
        PRINTED.append((out, s, key))
    return out


def iv2(s, key):
    m = re.fullmatch(r"\[([+-]?\d\.\d{4}),([+-]?\d\.\d{4})\]", s)
    assert m, s
    return f"[{r2(m.group(1), key)},{r2(m.group(2), key)}]"


EDITS = []   # (old, new)


def rep(old, new):
    EDITS.append((old, new))


# ----------------------------------------------------------------------------------------------------------------------------------
# Section 1: Figure 1 referred to from the first paragraph (item 4); the contributions list (item 5 with its addendum; "forbidding records"
# by the ruling); the route sentence with routes A and B (items 12 and 56); the preregistration sentence to Section 4 (item 10)
# ----------------------------------------------------------------------------------------------------------------------------------
rep("The input to the judgment is a lifecycle summary, a list of what the store holds with the values removed, beside a count of its records in each state.\n",
    "The input to the judgment is a lifecycle summary, a list of what the store holds with the values removed, beside a count of its records in each state (Figure~\\ref{fig:framework}).\n")
rep("Every score in this paper is an AUROC, the chance that a positive scores above a negative.\n"
    "\n"
    "%% Writing pass Phase 1 (2026-09-15), item 7: the four-finding paragraph deleted; every number in it reappears in Sections 5 to 9 with its population; the contributions list (item 5) lands in Phase 3.\n"
    "\n"
    "The two routes are the design (Figure~\\ref{fig:framework}).\n"
    "A summary the store maintains outside query time is read by a lookup or by a model, and retrieval that does not mask returns non-active records with their tags.\n"
    "Of the $58$ predictions preregistered before data collection, $16$ came out otherwise (Appendix~\\ref{app:registration}).\n",
    "Every score in this paper is an AUROC, the chance that a positive scores above a negative.\n"
    "\n"
    "%% Writing pass Phase 3 (2026-09-15), item 5 with its addendum: the contributions list in the author's words (\"forbidding records\" in the fifth by the ruling of the same day);\n"
    "%% item 4: Figure 1 referred to from the first paragraph and the route sentence names routes A and B (item 56); item 10: the preregistration sentence moved to Section 4.\n"
    "This paper makes five contributions.\n"
    "\\begin{itemize}\\setlength{\\itemsep}{1pt}\n"
    "\\item We define two pre-retrieval judgments about an external memory store, FOK (coverage) and NOK (obligation), with an intent-conditional coverage label (Definition~\\ref{def:coverage}) and a value-free lifecycle summary as the monitor's input (Definition~\\ref{def:index}).\n"
    "\\item We build a counterfactual test in which one question is asked of three store versions differing in a single attribute ($n=444$), so the summary is the only input that varies and question wording cannot carry the label.\n"
    "\\item We show that LLM monitors read the summary's \\emph{names}, not its counts. On the counterfactual set (three models), a similarity lookup matches all but the largest model on the state the summary names; on the states it only counts, no model reads them, and naming them lifts every model.\n"
    "\\item We show that unmasked retrieval returning non-active records \\emph{with their tags} is a second route that carries what the list misses, and that no tested backend (FR-Bank, Mem0, A-MEM) writes a list a monitor can use.\n"
    "\\item We show downstream that gating retrieval on the judgment reaches more forbidding records but does not reduce stale answers; tagging the untagged duplicates the store keeps does. The fix is in the write path.\n"
    "\\end{itemize}\n"
    "Figure~\\ref{fig:framework} shows the two routes: route A is a summary the store maintains outside query time, read by a lookup or by a model, and route B is retrieval that does not mask, returning non-active records with their tags.\n")
rep("Every preregistered text, prediction and outcome is in Appendix~\\ref{app:registration}.\n",
    "Of the $58$ predictions preregistered before data collection, $16$ came out otherwise, and every preregistered text, prediction and outcome is in Appendix~\\ref{app:registration}.\n")

# ----------------------------------------------------------------------------------------------------------------------------------
# Figure 1 (item 56): full text width, left to right, routes A and B, masked retrieval as a crossed-out arrow
# ----------------------------------------------------------------------------------------------------------------------------------
FIG1_OLD_START = "\\begin{figure}[t]\n\\centering\n%% R110: Figure 1, the framework"
FIG1_OLD_END = "\\label{fig:framework}\n\\end{figure}\n"
FIG1_NEW = r"""\begin{figure}[t]
\centering
%% Writing pass Phase 3 (2026-09-15), item 56: Figure 1 at the text width, left to right (store, the two routes, the monitor, the judgments), routes A and B
%% labelled and used in the text, masked retrieval a crossed-out arrow rather than a third box; every label \footnotesize; no meaning carried by colour alone.
\begin{tikzpicture}[font=\footnotesize, >=Stealth,
  rec/.style={draw, rounded corners=1pt, text width=3.3cm, minimum height=0.34cm, inner sep=1.5pt, align=left, font=\scriptsize\ttfamily},
  box/.style={draw, thick, rounded corners=2pt, inner sep=3.5pt, align=left, font=\footnotesize},
  route/.style={->, thick},
  grey/.style={->, thick, draw=black!50, dashed}]
  \node[rec, fill=white] (r1) {trip\_plan~~active};
  \node[rec, below=1pt of r1, fill=black!10] (r2) {trip\_plan~~superseded};
  \node[rec, below=1pt of r2, fill=black!10] (r3) {hike\_sat~~~retracted};
  \node[rec, below=1pt of r3, fill=black!10] (r4) {exam\_date~~expired};
  \node[rec, below=1pt of r4, fill=white] (r5) {work\_style~active};
  \node[draw, thick, rounded corners=2pt, fit=(r1)(r5), inner sep=3pt, label={[font=\footnotesize\bfseries]above:the store, every record tagged}] (store) {};
  \node[box, right=0.45cm of store.east, anchor=west, yshift=1.0cm, text width=4.0cm] (summ)
    {\textbf{route A: the summary}, maintained outside query time\\ count table, per category and state\\ name map, values removed:\\ \texttt{superseded: trip\_plan}};
  \node[box, below=0.22cm of summ, text width=4.0cm] (tags)
    {\textbf{route B: the tags}, top-$k$ retrieval with no mask, lines keep their tags:\\ \texttt{[2] superseded trip\_plan}\\ \texttt{[3] retracted hike\_sat}};
  \node[box, right=0.45cm of tags.east, anchor=west, yshift=0.6cm, text width=2.2cm, align=center] (mon)
    {\textbf{monitor}\\ a lookup or a model\\ emits FOK and NOK before any content is retrieved};
  \node[right=0.25cm of mon.east, anchor=west, font=\footnotesize, align=left, text width=2.05cm] (jud) {FOK: is the question covered?\\[3pt] NOK: does the store hold anything not to use?};
  \draw[route] (store.east |- summ.west) -- (summ.west) node[midway, above, font=\scriptsize] {A};
  \draw[route] (store.east |- tags.west) -- (tags.west) node[midway, above, font=\scriptsize] {B};
  \draw[route] (summ.east) -- ++(2.8mm,0mm) |- (mon.north west);
  \draw[route] (tags.east) -- ++(2.8mm,0mm) |- (mon.south west);
  \draw[route] (mon.east) -- (jud.west);
  \coordinate (m0) at ($(store.east)+(0mm,-7.2mm)$);
  \coordinate (my) at ($(tags.south)+(0mm,-4.2mm)$);
  \coordinate (m1) at (tags.west |- my);
  \coordinate (m2) at ($(mon.south |- my)$);
  \draw[grey] (m0) -- (m1) -- (m2) node[pos=0.5, inner sep=0pt] (x) {};
  \node[right=0.15cm of m2, anchor=west, font=\footnotesize, text=black!60, align=left, text width=3.1cm] {masked retrieval: non-active records dropped, no route};
  \draw[thick, draw=black!60] ($(x)+(-1.6mm,-1.6mm)$) -- ($(x)+(1.6mm,1.6mm)$) ($(x)+(-1.6mm,1.6mm)$) -- ($(x)+(1.6mm,-1.6mm)$);
\end{tikzpicture}
\caption{The framework. A store tags every record with a lifecycle state (grey rows are non-active). Route A is a summary the store maintains outside query time, a count table and a name map with every value removed; route B is top-$k$ retrieval without a mask, which returns non-active records with their tags. Either carries the obligation to a monitor that emits FOK and NOK before any content is retrieved; masked retrieval drops the tagged records and carries nothing.}
\label{fig:framework}
\end{figure}
"""

# ----------------------------------------------------------------------------------------------------------------------------------
# Section 3: Definition 1's cases as the PN grid (items 20 and 94); Definition 2's section names (item 21); the notation box (item 17 with its
# addendum, item 23); the example as a listing (item 22); Figure 2's caption (item 91) and the name lookup's score rows
# ----------------------------------------------------------------------------------------------------------------------------------
rep("The label is \\pn{} when $S$ contains content that must be suppressed for the answer to be right under $i(q)$. That happens for a superseded value under current intent, a retracted plan under current or upcoming intent, and an expired event under current or upcoming intent.\n"
    "% C030\n"
    "Expired content under past intent is \\present{} rather than \\pn{}. Otherwise \\present{} denotes licensed answering content with no obligation that matters for the answer, and \\absent{} denotes neither.\n"
    "\\end{definition}\n"
    "The \\textsc{change} intent asks what changed, so such queries are never \\pn{}, because both the old and the new value are licensed.\n",
    "The label is \\pn{} when $S$ contains content that must be suppressed for the answer to be right under $i(q)$; \\present{} denotes licensed answering content with no obligation that matters for the answer, and \\absent{} denotes neither. The grid below gives the label by the state of the relevant record and the intent.\n"
    "% C030: the cases of Definition 1 as the grid of Table tab:pn-grid (items 20 and 94)\n"
    "\\end{definition}\n"
    "\n"
    "%% Writing pass Phase 3 (2026-09-15), items 20 and 94: Definition 1's cases as a grid (unnumbered, so the result tables keep their numbers); the CHANGE intent is never PN\n"
    "%% because both the old and the new value are licensed; n.a. is a combination the definition does not assign because the question construction never produces it (Appendix E.3).\n"
    "\\begin{center}\n"
    "\\scriptsize\n"
    "\\setlength{\\tabcolsep}{5pt}\n"
    "\\begin{tabular}{@{}lcccc@{}}\n"
    "\\toprule\n"
    "Relevant record & \\textsc{current} & \\textsc{upcoming} & \\textsc{past} & \\textsc{change} \\\\\n"
    "\\midrule\n"
    "active, licensed & \\present{} & \\present{} & \\present{} & \\present{} \\\\\n"
    "superseded value & \\pn{} & n.a. & n.a. & \\present{} \\\\\n"
    "retracted plan & \\pn{} & \\pn{} & n.a. & n.a. \\\\\n"
    "expired event & \\pn{} & \\pn{} & \\present{} & n.a. \\\\\n"
    "none & \\absent{} & \\absent{} & \\absent{} & \\absent{} \\\\\n"
    "\\bottomrule\n"
    "\\end{tabular}\n"
    "\\par\\vspace{1pt}{\\scriptsize The \\textsc{change} intent is never \\pn{}, because both the old and the new value are licensed; n.a.\\ is a combination the question construction does not produce.}\n"
    "\\end{center}\n")
rep("We elicit $\\mathrm{FOK}(q,S)\\in[0,1]$ as a probability that coverage is not \\absent{} and $\\mathrm{NOK}(q,S)\\in[0,1]$ as a probability that coverage is \\pn{}.\nWe score both by AUROC \\citep{hanley1982}.\n",
    "Both judgments are probabilities, scored by AUROC \\citep{hanley1982}.\nWe elicit $\\mathrm{FOK}(q,S)\\in[0,1]$ as a probability that coverage is not \\absent{} and $\\mathrm{NOK}(q,S)\\in[0,1]$ as a probability that coverage is \\pn{}.\n")
rep("The name map records which names each category exposes and which carry superseded content. The size",
    "The name map records which names each category exposes and which carry superseded content; the names that carry superseded content form the superseded-names list. The size")
rep("%% R110: the abridged example summary directly after Definition 2 (CC_PASS_v18 section 3.3); the lines are those of the E.1 excerpt (AUX-R86-INDEX-EXCERPT).\n"
    "\n"
    "\\begin{center}\n"
    "\\fbox{\\begin{minipage}{0.97\\linewidth}\n"
    "\\ttfamily\\scriptsize\n",
    "%% Writing pass Phase 3 (2026-09-15), item 17 with its addendum and item 23: the notation box directly after Definition 2, twelve rows; every term is used verbatim\n"
    "%% from here on (ground rule 3). The vocabulary of names / counts / reads leaves the prose of Section 3 for the box (its E.1 copy stands until item 69).\n"
    "\\begin{center}\n"
    "\\fbox{\\begin{minipage}{0.97\\linewidth}\n"
    "\\scriptsize\n"
    "\\setlength{\\tabcolsep}{3pt}\n"
    "\\begin{tabular}{@{}p{0.22\\linewidth}p{0.76\\linewidth}@{}}\n"
    "\\multicolumn{2}{@{}l}{\\textbf{Notation.} The terms below are used verbatim throughout.}\\\\\n"
    "\\midrule\n"
    "lifecycle state; non-active & the tag a record carries, \\textsc{active}, \\textsc{superseded}, \\textsc{retracted} or \\textsc{expired}; the last three are the non-active states \\\\\n"
    "forbidding record & the non-active record that would make an answer wrong if used \\\\\n"
    "intent; \\pn{} & the time frame a question asks about (\\textsc{current}, \\textsc{upcoming}, \\textsc{past}, \\textsc{change}); present-negative: the store holds relevant content and using it would make the answer wrong. An \\emph{obligation} is a question whose label is \\pn{} \\\\\n"
    "FOK; NOK & the coverage judgment, is the question covered; the obligation judgment, does the store hold anything not to use \\\\\n"
    "summary & the count table (records per category and lifecycle state) and the name map (the attribute names each category exposes, values removed); the superseded-names list is the part of the name map that carries superseded content \\\\\n"
    "named state; counted state & a state whose attribute names the summary lists (superseded, by default); a state the summary only counts (retracted, expired) \\\\\n"
    "names, counts, reads & a summary \\emph{names} a state when it lists the attribute names in that state and \\emph{counts} it when it gives only a count of it; a reader \\emph{reads} a state when its score separates that state's items from the rest \\\\\n"
    "blind; indexed & the monitor sees the question alone; the monitor sees the question and the summary \\\\\n"
    "gain ($\\Delta$) & the indexed score minus the blind score on the same questions; on the counterfactual set the blind score is $0.50$ by construction, so there the AUROC and the gain carry the same information \\\\\n"
    "ground-truth summary; store-written summary & the summary built from ground truth; the summary built from the fields the backend itself exposes \\\\\n"
    "name lookup; all-states lookup & the similarity lookup over the summary's superseded-names list, the no-model baseline every model is measured against; the same over a list that names all three non-active states \\\\\n"
    "route A; route B & the summary route; the tag route, retrieval without a mask that returns non-active records with their tags (Figure~\\ref{fig:framework}) \\\\\n"
    "\\end{tabular}\n"
    "\\end{minipage}}\n"
    "\\end{center}\n"
    "\n"
    "%% R110: the abridged example summary directly after Definition 2 (CC_PASS_v18 section 3.3); the lines are those of the E.1 excerpt (AUX-R86-INDEX-EXCERPT).\n"
    "%% Writing pass Phase 3 (2026-09-15), item 22: the example as a listing with a one-line caption, referenced by number; item 21's section names in the caption.\n"
    "\\begin{listing}[h]\n"
    "\\caption{An abridged real summary: the count table (lines two and three), the name map (line four) and the superseded-names list (line five).}\n"
    "\\label{lst:summary}\n"
    "\\centering\n"
    "\\fbox{\\begin{minipage}{0.97\\linewidth}\n"
    "\\ttfamily\\scriptsize\n")
rep("ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT (abridged): hiking\\_preference, ...\n"
    "\\end{minipage}}\n"
    "\\end{center}\n"
    "This abridged real summary is what the indexed monitor reads: counts per category and state, and names with no values.\n",
    "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT (abridged): hiking\\_preference, ...\n"
    "\\end{minipage}}\n"
    "\\end{listing}\n"
    "Listing~\\ref{lst:summary} is what the indexed monitor sees: counts per category and state, and names with no values.\n")
rep("Section~\\ref{sec:counterfactual} also tests an all-states summary that names all three non-active states; Figure~\\ref{fig:example} shows both cases on real store versions.\n"
    "A summary names a state when it lists the attribute names in that state, and counts it when it gives only a count of it.\n"
    "A reader reads a state when its score separates that state's items from the rest (Appendix~\\ref{app:glossary}).\n",
    "Section~\\ref{sec:counterfactual} also tests an all-states summary that names all three non-active states; Figure~\\ref{fig:example} shows both cases on real store versions.\n")
rep("A monitor reads a summary of the store with every value removed and returns two probabilities before any content is retrieved.",
    "A monitor sees a summary of the store with every value removed and returns two probabilities before any content is retrieved.")
rep("the lookup's score & $0.00$ & $0.73$ & $0.00$\\\\", "the name lookup's score & $0.00$ & $0.73$ & $0.00$\\\\")
rep("the lookup's score & $0.00$ & $0.00$ & $0.00$\\\\", "the name lookup's score & $0.00$ & $0.00$ & $0.00$\\\\")
FIG2_CAP_START = "\\caption{Two real triples of the counterfactual set: the question is fixed and the three store versions differ in one attribute."
FIG2_CAP_NEW = "\\caption{Two triples of the counterfactual set. The question is fixed; the three store versions differ in one attribute. Only the summary lines that differ are shown, with the name lookup's score under each. In row one the obligation is named and the lookup separates the versions; in row two only the count row differs and no reader over names can.}"

# ----------------------------------------------------------------------------------------------------------------------------------
# Section 5: the per-state figure (item 30 with its addendum); Table 2 to the whole-set column (item 50); names / counts in italics on first
# use (item 23); "reads" as a score -> separates / scores on first use (item 61, deferred until the box)
# ----------------------------------------------------------------------------------------------------------------------------------
STATES = ["Whole", "Sup.", "Retr.", "Exp."]
SUP_ONLY = [  # AUX-CF2-NB6-V2; AUX-R110-A1-CR (CR-nb1); AUX-CF2-MINI-V2, -H45-V2, -OP5-V2 (per state AUX-CF2-PERSTATE)
    ("name lookup", ["0.7663", "0.9223", "0.5000", "0.5000"]),
    ("category-guessing count reader", ["0.6623", "0.6573", "0.6669", "0.6872"]),
    ("GPT-4.1 mini", ["0.7167", "0.8308", "0.5283", "0.5489"]),
    ("Haiku 4.5", ["0.7566", "0.8876", "0.5433", "0.5794"]),
    ("Opus 5", ["0.8405", "0.9325", "0.5872", "0.6150"]),
]
ALL_STATES = [  # AUX-CF2-ALLSTATES-V3; AUX-CF2-MINI-V3, -H45-V3, -OP5-V3
    ("all-states lookup", ["0.8756", "0.8995", "0.7975", "0.8711"]),
    ("GPT-4.1 mini", ["0.7967", "0.8444", "0.8725", "0.5869"]),
    ("Haiku 4.5", ["0.8773", "0.8852", "0.9042", "0.8269"]),
    ("Opus 5", ["0.9079", "0.9319", "0.8100", "0.9267"]),
]
FILLS = {"name lookup": "black!15", "all-states lookup": "black!15", "category-guessing count reader": "black!45", "GPT-4.1 mini": "white",
         "Haiku 4.5": "black!70", "Opus 5": "black"}
PATTERNS = {"GPT-4.1 mini": "north east lines", "category-guessing count reader": "crosshatch dots"}


def plots(rows):
    out = []
    for name, vals in rows:
        style = f"fill={FILLS[name]}"
        if name in PATTERNS:
            style += f", pattern={PATTERNS[name]}, pattern color=black"
        coords = " ".join(f"({s},{v})" for s, v in zip(STATES, vals))
        out.append(f"      \\addplot[draw=black, {style}] coordinates {{{coords}}};")
    return "\n".join(out)


FIG_STATES = (
    "\n"
    "\\begin{figure}[t]\n"
    "\\centering\n"
    "%% Writing pass Phase 3 (2026-09-15), item 30 with its addendum: per-state AUROC on the counterfactual set as two panels sharing the y-axis (left the superseded-only\n"
    "%% summary, right the all-states summary), four states, one bar per reader within each state, a dashed line at 0.50, y from 0.4 to 1.0; the count reader has no\n"
    "%% all-states variant. Values as in Table tab:cf-main and Appendix C.2 (AUX-CF2-NB6-V2, -ALLSTATES-V3, -MINI/-H45/-OP5-V2/-V3, AUX-CF2-PERSTATE, AUX-R110-A1-CR).\n"
    "\\begin{tikzpicture}\n"
    "\\begin{groupplot}[group style={group size=2 by 1, horizontal sep=0.35cm, ylabels at=edge left, yticklabels at=edge left},\n"
    "    ybar, /pgf/bar width=3.6pt, width=0.5\\linewidth, height=4.1cm, ymin=0.4, ymax=1.0,\n"
    "    ylabel={obligation AUROC}, ylabel style={font=\\scriptsize}, symbolic x coords={Whole,Sup.,Retr.,Exp.}, xtick=data, enlarge x limits=0.18,\n"
    "    tick label style={font=\\scriptsize}, title style={font=\\scriptsize, yshift=-2pt}, ymajorgrids, grid style={black!12},\n"
    "    legend style={at={(-0.05,-0.3)}, anchor=north, legend columns=5, font=\\scriptsize, draw=none, fill=none, column sep=5pt}]\n"
    "  \\nextgroupplot[title={superseded-only summary}]\n"
    "      \\draw[dashed, black!60] (axis cs:Whole,0.5) -- (axis cs:Exp.,0.5);\n"
    + plots(SUP_ONLY) + "\n"
    "  \\nextgroupplot[title={all-states summary}]\n"
    "      \\draw[dashed, black!60] (axis cs:Whole,0.5) -- (axis cs:Exp.,0.5);\n"
    + plots(ALL_STATES) + "\n"
    "      \\addlegendimage{draw=black, fill=black!45, pattern=crosshatch dots, pattern color=black}\n"
    "      \\legend{lookup (name; all-states), GPT-4.1 mini, Haiku 4.5, Opus 5, count reader (left panel)}\n"
    "\\end{groupplot}\n"
    "\\end{tikzpicture}\n"
    "\\caption{Obligation AUROC on the counterfactual set per state, under the superseded-only summary (left) and the all-states summary (right); the dashed line is chance. On the state the summary names the lookup and the models are high together; on the states it only counts, the count reader separates the versions and no model does, and naming those states lifts every reader.}\n"
    "\\label{fig:perstate}\n"
    "\\end{figure}\n")

# Table 2 to the whole-set column (item 50: the per-state columns go once the figure exists)
TAB2_OLD_HEAD = "\\begin{tabular}{@{}lrrrrl@{}}\n\\toprule\nReader, summary & Whole & Sup. & Retr. & Exp. & persona interval \\\\\n\\midrule\n"
TAB2_NEW_HEAD = "\\begin{tabular}{@{}lrl@{}}\n\\toprule\nReader, summary & AUROC & persona interval \\\\\n\\midrule\n"


def shrink_table2(text):
    i = text.index(TAB2_OLD_HEAD)
    j = text.index("\\end{tabular}", i)
    block = text[i:j]
    lines = block.split("\n")
    out = []
    for l in lines:
        m = re.fullmatch(r"(.+?) & (\$[0-9.]+\$) & \$[0-9.]+\$ & \$[0-9.]+\$ & \$[0-9.]+\$ & (\$\[[0-9.,]+\]\$) \\\\", l)
        if m:
            out.append(f"{m.group(1)} & {m.group(2)} & {m.group(3)} \\\\")
        elif l.startswith("\\multicolumn{6}"):
            out.append(l.replace("\\multicolumn{6}", "\\multicolumn{3}"))
        else:
            out.append(l)
    new_block = "\n".join(out).replace(TAB2_OLD_HEAD, TAB2_NEW_HEAD)
    assert new_block.count("\\multicolumn{3}") == 1 and "Sup." not in new_block
    return text[:i] + new_block + text[j:]


rep("\\caption{Obligation AUROC on the counterfactual set ($n=444$; positives $88$ supersession, $30$ retraction, $30$ expiry), whole set and per state. Blind NOK is $0.50$ by construction, so each AUROC is also a gain; the interval is the persona-grouped interval of the whole-set AUROC; the item-level paired gain intervals are in Appendix~\\ref{app:counterfactual}.}",
    "\\caption{Obligation AUROC on the counterfactual set ($n=444$; positives $88$ supersession, $30$ retraction, $30$ expiry), whole set; the per-state values are Figure~\\ref{fig:perstate}. Blind NOK is $0.50$ by construction, so each AUROC is also a gain; the interval is the persona-grouped interval of the AUROC; the item-level paired gain intervals are in Appendix~\\ref{app:counterfactual}.}")
rep("Table~\\ref{tab:cf-main} gives every reader on the whole set and per state, with two readers that have no model in them.\n"
    "One is the name lookup, a similarity lookup over the superseded-names list; the other is a count reader that knows the question's category and reads that category's retracted and expired counts.\n",
    "Table~\\ref{tab:cf-main} gives every reader on the whole set and Figure~\\ref{fig:perstate} per state, with two readers that have no model in them.\n"
    "One is the name lookup, a similarity lookup over the superseded-names list; the other is a count reader that knows the question's category and reads that category's retracted and expired \\emph{counts}.\n")
rep("Supersession is the one state the summary names.\n", "Supersession is the one state the summary \\emph{names}.\n")
rep("That reader reads the retracted versions at $0.73$ and the expired versions at $0.78$ on the counterfactual set",
    "That reader separates the retracted versions at $0.73$ and the expired versions at $0.78$ on the counterfactual set")
rep("every model reads the retracted attributes and all but the smallest the expired ones", "every model separates the retracted attributes and all but GPT-4.1 mini the expired ones")
rep("while Haiku 4.5 reads $0.71$ capped", "while Haiku 4.5 scores $0.71$ capped")
rep("The all-states lookup reads $0.88$ on the whole set", "The all-states lookup scores $0.88$ on the whole set")
rep("the view reads the obligation at $0.81$ against $0.69$ for GPT-4.1 mini", "the view scores the obligation at $0.81$ against $0.69$ for GPT-4.1 mini")
rep("A count of tagged lines reads the obligation at $0.62$", "A count of tagged lines scores the obligation at $0.62$")
rep("is in view and tagged reads $0.72$ under the store's own tags", "is in view and tagged scores $0.72$ under the store's own tags")
rep("GPT-4.1 mini and the lookup read $0.60$ and $0.59$ capped", "GPT-4.1 mini and the lookup score $0.60$ and $0.59$ capped")
rep("Haiku 4.5 reads it at its ground-truth level", "Haiku 4.5 scores it at its ground-truth level")
rep("Haiku 4.5 reads $0.87$ against $0.89$ under the ground-truth summary", "Haiku 4.5 scores $0.87$ against $0.89$ under the ground-truth summary")
rep("The lookup on the same halves reads $0.76$ where the name is present", "The lookup on the same halves scores $0.76$ where the name is present")

# ----------------------------------------------------------------------------------------------------------------------------------
# Section 8: the cross-model table (item 84 (a)); values as in Appendix A's exact table (AUX-E1R-CLUSTER-CELL; two decimals in the body)
# ----------------------------------------------------------------------------------------------------------------------------------
XM = [  # model, blind, indexed, delta, item CI, clustered CI  (the cross-model set, n = 84, 40 obligations)
    ("GPT-4.1 mini", "0.5000", "0.7139", None, None, None),
    ("Haiku 4.5", "0.3688", "0.8199", "+0.4511", "[+0.3265,+0.5741]", "[+0.2925,+0.5981]"),
    ("Opus 5", "0.6994", "0.8523", "+0.1528", "[+0.0659,+0.2509]", "[+0.0923,+0.2392]"),
    ("GPT-5.6 Luna", "0.5585", "0.8526", "+0.2940", "[+0.1696,+0.4172]", "[+0.1984,+0.4051]"),
    ("GPT-5.6 Sol", "0.5290", "0.8588", "+0.3298", "[+0.1994,+0.4470]", "[+0.2117,+0.4500]"),
    ("Kimi K3", "0.5983", "0.8588", "+0.2605", "[+0.1456,+0.3866]", "[+0.1653,+0.3933]"),
]


def xm_table():
    K = "AUX-E1R-CLUSTER-CELL (the cross-model set; Table tab:ladder-exact)"
    rows = []
    for m, b, i, d, ci, cc in XM:
        if d is None:
            rows.append(f"{m} & ${r2(b, K)}$$^{{a}}$ & ${r2(i, K)}$ & -- & -- & -- \\\\")
        else:
            rows.append(f"{m} & ${r2(b, K)}$ & ${r2(i, K)}$ & ${r2(d, K)}$ & ${iv2(ci, K)}$ & ${iv2(cc, K)}$ \\\\")
    return (
        "\\begin{table}[h]\n"
        "%% Writing pass Phase 3 (2026-09-15), item 84 (a): the replication claim as a six-row table on the cross-model set ($n=84$, $40$ obligations), values from\n"
        "%% Appendix A's exact table (tab:ladder-exact; AUX-E1R-CLUSTER-CELL), two decimals; GPT-4.1 mini's blind is an all-tie artifact, so its difference is not a gain.\n"
        "\\caption{The obligation judgment on the cross-model set ($84$ questions, $40$ obligations) for six models from three vendors: blind and indexed AUROC and the paired gain with both intervals. Every gain excludes zero where the blind score varies.}\n"
        "\\label{tab:crossmodel}\n"
        "\\centering\n"
        "\\scriptsize\n"
        "\\setlength{\\tabcolsep}{3pt}\n"
        "\\begin{tabular}{@{}lrrrll@{}}\n"
        "\\toprule\n"
        "Model & Blind & Indexed & $\\Delta$ & item interval & persona interval \\\\\n"
        "\\midrule\n" + "\n".join(rows) + "\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "\\par\\smallskip\n"
        "\\begin{minipage}{0.97\\linewidth}\\scriptsize\n"
        "$^{a}$GPT-4.1 mini's blind obligation score takes one value on every question of this set, so its indexed-minus-blind difference is not a gain and is not shown; its gain is defined on the counterfactual set (Table~\\ref{tab:cf-main}).\n"
        "\\end{minipage}\n"
        "\\end{table}\n")


rep("The obligation gain replicates across models, and the coverage margin lives on ordinary records.\n"
    "Every paired obligation gain excludes zero where the blind score varies (Table~\\ref{tab:e1}), and on the cross-model set the five models with a varying blind score gain $+0.15$ to $+0.45$ (Appendix~\\ref{app:laddertable}).\n",
    "The obligation gain replicates across models, and the coverage margin lives on ordinary records.\n"
    "Every paired obligation gain excludes zero where the blind score varies (Tables~\\ref{tab:crossmodel} and~\\ref{tab:e1}), and on the cross-model set the five models with a varying blind score gain $+0.15$ to $+0.45$ (Appendix~\\ref{app:laddertable}).\n")
rep("Haiku 4.5, Opus 5 and GPT-5.6 Luna sit $+0.07$ to $+0.08$ above it, with item-level intervals excluding zero and persona-grouped intervals including it (Appendix~\\ref{app:baselines}).\n",
    "Haiku 4.5, Opus 5 and GPT-5.6 Luna sit $+0.07$ to $+0.08$ above it, with item-level intervals excluding zero and persona-grouped intervals including it (Appendix~\\ref{app:baselines}).\n"
    "\n" + "%%XMTABLE%%\n")

# the listing float type in the preamble (item 22)
rep("\\newcommand{\\hdl}[2]{\\begin{tabular}[b]{@{}l@{}}#1\\\\#2\\end{tabular}}\n",
    "\\newcommand{\\hdl}[2]{\\begin{tabular}[b]{@{}l@{}}#1\\\\#2\\end{tabular}}\n"
    "% Writing pass Phase 3: the example summary is a listing (item 22), so Figure 2 stays Figure 2 (item 91).\n"
    "\\newfloat{listing}{htbp}{lol}\n"
    "\\floatname{listing}{Listing}\n"
    "\\usetikzlibrary{patterns}\n")


def main():
    check = "--check" in sys.argv
    text = io.open(BODY, encoding="utf-8").read().replace("\r\n", "\n")
    for old, new in EDITS:
        assert text.count(old) == 1, (text.count(old), old[:80])
        text = text.replace(old, new)
    # Figure 1
    i = text.index(FIG1_OLD_START); j = text.index(FIG1_OLD_END, i) + len(FIG1_OLD_END)
    text = text[:i] + FIG1_NEW + text[j:]
    # Figure 2's caption
    i = text.index(FIG2_CAP_START); j = text.index("}\n\\label{fig:example}", i) + 1
    text = text[:i] + FIG2_CAP_NEW + text[j:]
    # the per-state figure after Table 2's \end{table}
    i = text.index("\\label{tab:cf-main}"); j = text.index("\\end{table}\n", i) + len("\\end{table}\n")
    text = text[:j] + FIG_STATES + text[j:]
    text = shrink_table2(text)
    # the cross-model table
    assert text.count("%%XMTABLE%%\n") == 1
    text = text.replace("%%XMTABLE%%\n", xm_table())
    # the provenance comment
    text = text.replace("% edit asserted by line range): Section 8 split into 8 and 9, the population table, the six body tables rewritten to two decimals with short captions, the cuts of items 1 and 90.\n",
                        "% edit asserted by line range): Section 8 split into 8 and 9, the population table, the six body tables rewritten to two decimals with short captions, the cuts of items 1 and 90.\n"
                        "% Phase 2 the renames (wp_phase2.py); Phase 3 the new elements (wp_phase3.py): the contributions list, Figure 1 at the text width with routes A and B, the PN grid,\n"
                        "% the notation box, the example as a listing, Figure 2's two-line caption, the per-state figure with Table 2 at the whole-set column, the cross-model table.\n")
    if check:
        print(f"check: {len(EDITS)} edits apply; nothing written"); return
    io.open(BODY, "w", encoding="utf-8", newline="\n").write(text)
    # the ledger's Phase 3 section
    led = LEDGER.read_text(encoding="utf-8")
    marker = "## 3. AUX-WP-PRINTED-P3"
    if marker in led:
        led = led[:led.index(marker)]
    seen = {}
    for p_, s_, k_ in PRINTED:
        seen.setdefault((p_, s_), k_)
    led = led.rstrip("\n") + "\n\n" + marker + ": two-decimal forms the cross-model table of Section 8 prints (Phase 3; each from the four-decimal value of Appendix A's exact table under the key named)\n\n| printed | four-decimal source | key |\n|---|---|---|\n"
    for (p_, s_), k_ in seen.items():
        led += f"| {p_} | {s_} | {k_} |\n"
    LEDGER.write_text(led, encoding="utf-8", newline="\n")
    print(f"body_v18.tex written; {len(EDITS)} edits, Figure 1, Figure 2's caption, the per-state figure, Table 2, the cross-model table; ledger section 3 with {len(seen)} printed forms")


if __name__ == "__main__":
    main()
