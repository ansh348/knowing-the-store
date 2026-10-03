# -*- coding: utf-8 -*-
"""port_v22.py -- program R126 (2026-09-19, the author's brief "KtS R126: build v22 from the readable body"), Phases 1 to 3: port the readable body
of reviews/v22/inbox/v22_readable_main.tex into reviews/v22/src/body_v22.tex and abstract_v22.tex. The repository is the source of truth: the
inbox text is a draft to port; every number, pointer and citation it carries is checked by the gates on the built manuscript.

What this script takes from where:
  the preamble, the AI-use and reproducibility statements, the bibliography and \\appendix   reviews/v21/src/body_v21.tex, verbatim (the preamble
                                                                                             gains tabularx, the Y column and the \\claim macro)
  Figures 1 and 2                                                                            our v21 TikZ / table, simplified to the inbox's labels
  Definition 1 with its grid (def:coverage)                                                  body_v21.tex, verbatim (not retyped)
  Table 2's upper part (the census)                                                          body_v21.tex tab:census, verbatim (the R124-F wording)
  Figure 3                                                                                   pgfplots over reviews/v22/src/fig3_data.tex (fig3_data.py)
  everything else in the main text                                                           the inbox, converted: \\N{x}{prov} to x (math mode for
                                                                                             numerals), \\ap{X} to Appendix~\\ref{}, \\PN etc. to our
                                                                                             macros, the inbox's labels to ours, hardcoded table numbers
                                                                                             to \\ref, the dropped citation keys restored at their sentences
Phase 2 (the author's text fixes) and the gate-driven wording changes (Phase 5.3; each named with its rule in GATE_CHANGES, printed at the end)
are asserted replacements on the converted text. The notation box and Definition 2 leave the body for Appendix E.1 (appendix_r126.py reads them
from body_v21.tex). Usage: python reviews/v22/tools/port_v22.py [--check]   (idempotent: regenerates both files from the inbox and body_v21.tex)
"""
from __future__ import annotations

import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
V21B = ROOT / "reviews" / "v21" / "src" / "body_v21.tex"
INBOX = ROOT / "reviews" / "v22" / "inbox" / "v22_readable_main.tex"
OUT_B = ROOT / "reviews" / "v22" / "src" / "body_v22.tex"
OUT_A = ROOT / "reviews" / "v22" / "src" / "abstract_v22.tex"
OUT_NUMS = ROOT / "reviews" / "v22" / "INBOX_NUMBERS_R126.md"

R126_HEADER = ("% R126 (2026-09-19): paper_v22.tex, the v22 lineage opened from the R124 close (ee6b735; paper_v21.tex as gates_r124_f.txt records it):\n"
               "% the v21 sources copied by reviews/v22/tools/bump_v22.py. The main text is the readable body of reviews/v22/inbox/ ported section by\n"
               "% section (reviews/v22/tools/port_v22.py); the statements, the references and the appendix are ours. v21 stays as committed, the\n"
               "% fallback build (tag fallback/v22-pre-restructure). Built by reviews/v22/tools/build_v22.py; CLAIMS.md R126 block; reviews/v22/.\n")

NUMS = []          # (printed value, the inbox's provenance tag, section)
GATE_CHANGES = []  # (rule, section, before, after)


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def rep(t, old, new, n=1, where=""):
    assert t.count(old) == n, (where, t.count(old), n, old[:90])
    return t.replace(old, new)


def gate(rule, section, t, old, new):
    GATE_CHANGES.append((rule, section, old, new))
    return rep(t, old, new, 1, rule + " " + section)


# ----------------------------------------------------------------------------------------------------------------------- conversions
AP = {"A": "app:laddertable", "C.2": "app:counterfactual", "E.1": "app:glossary", "E.3": "app:construction", "E.7": "app:inversion",
      "E.8": "app:baselines", "E.9": "app:census", "E.10": "app:resp", "E.12": "app:provenance", "F": "app:registration", "G.4": "app:posthoc-graphiti"}
LABELS = {"sec:introduction": "sec:intro", "sec:related_work": "sec:related", "sec:readers": "sec:counterfactual", "sec:retrieval": "sec:downstream",
          "sec:replication": "sec:populations", "tab:readers": "tab:cf-main", "fig:triple": "fig:example", "fig:states": "fig:perstate",
          "def:state_intent": "def:coverage"}
WORDS = {"three", "zero", "one", "fifteen", "five", "quarter", "Two", "two", "Three"}


def conv_N(t, section):
    def r(m):
        val, prov = m.group(1), m.group(2)
        NUMS.append((val, prov, section))
        if val in WORDS:
            return val
        if val == "1.0.5":
            return val
        if re.fullmatch(r"[0-9][0-9,]*(\.[0-9]+)?(\\%)?", val):
            return "$" + val.replace(",", "{,}") + "$"
        raise AssertionError(("unclassified \\N", val, prov))
    return re.sub(r"\\N\{([^{}]*)\}\{([^{}]*)\}", r, t)


def conv(t, section):
    t = conv_N(t, section)
    t = re.sub(r"\(\\ap\{([^}]*)\}\)", lambda m: "(Appendix~\\ref{" + AP[m.group(1)] + "})", t)
    t = re.sub(r"\\ap\{([^}]*)\}", lambda m: "Appendix~\\ref{" + AP[m.group(1)] + "}", t)   # 'in \ap{E.3}', 'from \ap{E.12}'
    assert "\\ap{" not in t, section
    for a, b in (("\\PRESENT\\ ", "\\present{} "), ("\\PRESENT", "\\present{}"), ("\\ABSENT\\ ", "\\absent{} "), ("\\ABSENT", "\\absent{}"),
                 ("\\PN\\ ", "\\pn{} "), ("\\PN", "\\pn{}")):
        t = t.replace(a, b)
    for a, b in LABELS.items():
        t = t.replace("{" + a + "}", "{" + b + "}")
    return t


def sections(inbox):
    parts = re.split(r"^% SECTION (\S+)\n", inbox, flags=re.M)
    assert parts[0].strip() == "", parts[0][:80]
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def cut(text, start, end, include_end=True):
    i = text.index(start)
    j = text.index(end, i) + (len(end) if include_end else 0)
    return text[i:j]


# ----------------------------------------------------------------------------------------------------------------------- the pieces from v21
def v21_pieces(b):
    pre = b[:b.index("%%ABSTRACT%%\n") + len("%%ABSTRACT%%\n")]
    fig1 = cut(b, "\\begin{figure}[t]\n\\centering\n%% Writing pass Phase 3 (2026-09-15), item 56: Figure 1", "\\label{fig:framework}\n\\end{figure}\n")
    def1 = cut(b, "\\begin{definition}[Intent-conditional coverage]\\label{def:coverage}", "\\end{definition}\n")
    grid = cut(b, "%% Writing pass Phase 3 (2026-09-15), items 20 and 94: Definition 1's cases as a grid", "n.a.\\ means a combination the question construction never produces.}\n\\end{center}\n")
    fig2 = cut(b, "\\begin{figure}[t]\n\\centering\n%% Writing pass Phase 4b (2026-09-15): Figure 2's source", "\\label{fig:example}\n\\end{figure}\n")
    census = cut(b, "\\begin{table}[h]\n%% Writing pass Phase 1 (2026-09-15), items 52 and 90: three rows", "\\end{tabular}\n\\end{table}\n")
    tail = b[b.index("\\subsection*{AI use statement}"):]
    return pre, fig1, def1, grid, fig2, census, tail


# ----------------------------------------------------------------------------------------------------------------------- Figure 1 (our TikZ, the inbox's labels)
def fig1_v22(fig1):
    f = fig1
    f = rep(f, "%% Writing pass Phase 3 (2026-09-15), item 56: Figure 1 at the text width, left to right (store, the two routes, the monitor, the judgments), routes A and B\n"
               "%% labelled and used in the text, masked retrieval a crossed-out arrow rather than a third box; every label \\footnotesize; no meaning carried by colour alone.\n",
            "%% Writing pass Phase 3 (2026-09-15), item 56: Figure 1 at the text width, left to right (store, the two routes, the reader); masked retrieval a crossed-out\n"
            "%% arrow rather than a third box; every label \\footnotesize; no meaning carried by colour alone. R126 (2026-09-19): the same drawing with the inbox's labels\n"
            "%% (the summary route, the tag route, the reader; the judgments folded into the reader's box) and the inbox's caption; nothing else changes.\n")
    f = rep(f, "{\\textbf{route A: the summary}, maintained outside query time\\\\ count table, per category and state\\\\ name map, values removed:\\\\ \\texttt{superseded: trip\\_plan}};",
            "{\\textbf{the summary route}, before retrieval, maintained outside query time\\\\ count table, per category and state\\\\ name map, values removed:\\\\ \\texttt{superseded: trip\\_plan}};")
    f = rep(f, "{\\textbf{route B: the tags}, at retrieval: top-$k$ with no mask, returned lines keep their tags:\\\\ \\texttt{[2] superseded trip\\_plan}\\\\ \\texttt{[3] retracted hike\\_sat}};",
            "{\\textbf{the tag route}, at retrieval: top-$k$ with no mask, returned lines keep their tags:\\\\ \\texttt{[2] superseded trip\\_plan}\\\\ \\texttt{[3] retracted hike\\_sat}};")
    f = rep(f, "  \\node[box, right=0.45cm of tags.east, anchor=west, yshift=0.6cm, text width=2.2cm, align=center] (mon)\n"
               "    {\\textbf{monitor}\\\\ a lookup or a model\\\\ emits FOK and NOK: route A before any retrieval, route B on the returned records};\n"
               "  \\node[right=0.25cm of mon.east, anchor=west, font=\\footnotesize, align=left, text width=2.05cm] (jud) {FOK: is the question covered?\\\\[3pt] NOK: does the store hold anything not to use?};\n",
            "  \\node[box, right=0.45cm of tags.east, anchor=west, yshift=0.6cm, text width=3.45cm, align=left] (mon)\n"
            "    {\\textbf{the reader}: a name lookup or a model, judging before any retrieval (the summary route) or on the returned records (the tag route)\\\\[2pt]"
            " \\textbf{coverage} (FOK): is the question covered?\\\\ \\textbf{obligation} (NOK): anything not to use?};\n")
    f = rep(f, "  \\draw[route] (mon.east) -- (jud.west);\n", "")
    f = rep(f, "  \\draw[route] (store.east |- summ.west) -- (summ.west) node[midway, above, font=\\scriptsize] {A};\n"
               "  \\draw[route] (store.east |- tags.west) -- (tags.west) node[midway, above, font=\\scriptsize] {B};\n",
            "  \\draw[route] (store.east |- summ.west) -- (summ.west);\n"
            "  \\draw[route] (store.east |- tags.west) -- (tags.west);\n")
    f = rep(f, "{masked retrieval: non-active records dropped, no route};", "{masked retrieval: non-active records dropped, the tag route blocked};")
    f = rep(f, "\\caption{The framework: a tagged store (grey rows non-active), route A (the summary, read before any retrieval) and route B (the tags on returned records, read at retrieval time) to a monitor emitting FOK and NOK; masked retrieval has no route.}",
            "\\caption{A tagged store (grey rows non-active) and its two routes to a reader. The summary route exposes names and counts before retrieval. The tag route exposes lifecycle states on returned records. A retrieval mask that drops non-active records blocks the tag route.}")
    return f


# ----------------------------------------------------------------------------------------------------------------------- Figure 2 (our table, the inbox's labels and caption)
def fig2_v22(fig2):
    f = fig2
    f = rep(f, "%% R110: Figure 2, the worked example (CC_PASS_v18 section 3.4)", "%% R126 (2026-09-19): the inbox's row labels and caption; the cells are unchanged.\n%% R110: Figure 2, the worked example (CC_PASS_v18 section 3.4)")
    f = rep(f, "summary line & version 1: \\present{} & version 2: \\pn{} & version 3: \\absent{}\\\\", "summary line & \\present{} version & \\pn{} version & \\absent{} version\\\\")
    f = rep(f, "lifecycle total, retracted & \\texttt{0}", "retraction total & \\texttt{0}")
    f = rep(f, "\\texttt{PROJECTS\\_ENDEAVORS}: entries, active, retracted &", "category: entries, active, retracted &")   # the inbox's label (the category's name wrapped the row to three lines)
    f = rep(f, "names in the category & \\texttt{..., trip\\_plan}", "category names & \\texttt{..., trip\\_plan}")
    f = rep(f, "names carrying superseded content & \\texttt{(none)}", "superseded names & \\texttt{(none)}")
    f = rep(f, "the name lookup's score & $0.00$", "name lookup score & $0.00$")
    f = rep(f, "the label & the trip is on & the trip was cancelled & no such record\\\\", "what changes & the trip is on & the trip is cancelled & no such record\\\\")
    f = rep(f, "\\caption{A retraction triple of the counterfactual set: one question, three store versions differing in one attribute; only the differing summary lines are shown, with the name lookup's score. Only the count row differs between the \\present{} and \\pn{} versions, and the \\absent{} version also loses the name, so the name lookup separates none of the three (supersession triple: Appendix~\\ref{app:counterfactual}).}",
            "\\caption{The Carnival retraction triple: one question, three store versions differing in one attribute. Only the count distinguishes \\present{} from \\pn{}; \\absent{} also loses the category name. The default name lookup reads the superseded list, so it ties the versions. Only changed summary lines are shown (the supersession triple is in Appendix~\\ref{app:counterfactual}).}")
    return f


# ----------------------------------------------------------------------------------------------------------------------- Figure 3 (pgfplots over fig3_data.tex)
FIG3 = r"""\begin{figure}[t]
\centering
%% R126 (2026-09-19), Phase 3: Figure 3 redrawn in pgfplots from reviews/v22/src/fig3_data.tex (written by reviews/v22/tools/fig3_data.py from the
%% recorded artifacts; the marker spliced by build_v22.py), not from the inbox figure: two panels, states on the x axis, markers only, readers dodged
%% within each state, one marker shape per reader, one legend column at the right, the chance line dashed. Provisional: redrawn on the matched
%% metric when R125 reports, by regenerating the data file. GPT-4.1 mini is its five-draw per-state rows (AUX-R122-K5-ROWS).
%%FIG3-DATA%%
\begin{tikzpicture}
\begin{groupplot}[group style={group size=2 by 1, horizontal sep=0.9cm, ylabels at=edge left, yticklabels at=edge left},
    width=0.41\linewidth, height=5.0cm, xmin=-0.5, xmax=2.5, ymin=0.45, ymax=1.0,
    xtick={0,1,2}, xticklabels={Supersession,Retraction,Expiry}, ytick={0.5,0.6,0.7,0.8,0.9,1.0},
    ylabel={obligation AUROC}, ylabel style={font=\scriptsize}, tick label style={font=\scriptsize}, title style={font=\scriptsize, yshift=-3pt},
    ymajorgrids, grid style={black!12}, axis line style={black!60}, clip=false,
    legend style={at={(1.04,0.5)}, anchor=west, font=\scriptsize, draw=none, fill=none, row sep=-1pt, nodes={anchor=west}}]
  \nextgroupplot[title={only supersession named}]
      \draw[dashed, black!60] (axis cs:-0.5,0.5) -- (axis cs:2.5,0.5);
      \addplot[only marks, mark=*, mark size=2.0pt, black, xshift=-9pt] table[x=x, y=mini] {\figthreeSup};
      \addplot[only marks, mark=square*, mark size=1.9pt, black, xshift=-6pt] table[x=x, y=haiku] {\figthreeSup};
      \addplot[only marks, mark=triangle*, mark size=2.3pt, black, mark options={fill=white}, xshift=-3pt] table[x=x, y=luna] {\figthreeSup};
      \addplot[only marks, mark=diamond*, mark size=2.3pt, black, mark options={fill=white}, xshift=0pt] table[x=x, y=sol] {\figthreeSup};
      \addplot[only marks, mark=pentagon*, mark size=2.2pt, black, xshift=3pt] table[x=x, y=opus] {\figthreeSup};
      \addplot[only marks, mark=x, mark size=2.6pt, black, thick, xshift=6pt] table[x=x, y=lookup] {\figthreeSup};
      \addplot[only marks, mark=+, mark size=2.6pt, black!60, thick, xshift=9pt] table[x=x, y=count] {\figthreeSup};
  \nextgroupplot[title={all states named}]
      \draw[dashed, black!60] (axis cs:-0.5,0.5) -- (axis cs:2.5,0.5);
      \addplot[only marks, mark=*, mark size=2.0pt, black, xshift=-9pt] table[x=x, y=mini] {\figthreeAll};
      \addplot[only marks, mark=square*, mark size=1.9pt, black, xshift=-6pt] table[x=x, y=haiku] {\figthreeAll};
      \addlegendimage{only marks, mark=triangle*, mark size=2.3pt, black, mark options={fill=white}}
      \addlegendimage{only marks, mark=diamond*, mark size=2.3pt, black, mark options={fill=white}}
      \addplot[only marks, mark=pentagon*, mark size=2.2pt, black, xshift=3pt] table[x=x, y=opus] {\figthreeAll};
      \addplot[only marks, mark=x, mark size=2.6pt, black, thick, xshift=6pt] table[x=x, y=lookup] {\figthreeAll};
      \addlegendimage{only marks, mark=+, mark size=2.6pt, black!60, thick}
      \addlegendimage{dashed, black!60}
      \legend{mini (five draws), Haiku, Luna (left only), Sol (left only), Opus, name lookup, count reader (left only), chance}
\end{groupplot}
\end{tikzpicture}
\caption{Per-state obligation AUROC on the counterfactual set under the summary naming supersession only (left) and the summary naming all states (right); the dashed line is chance. Mini uses five draws, matching Table~\ref{tab:cf-main}. The count reader guesses the category. Luna and Sol ran only the default summary. Every value is in the tables of Appendix~\ref{app:counterfactual}.}
\label{fig:perstate}
\end{figure}
"""

# ----------------------------------------------------------------------------------------------------------------------- Table 1 (the inbox's layout, our style)
TAB1 = r"""\begin{table}[t]
%% R126 (2026-09-19): Table 1 in the inbox's layout (rows by reader, a named-states column, the Opus-minus-lookup difference row), our style; the
%% values are v21's tab:cf-main rows (AUX-R122-K5-* for GPT-4.1 mini at five draws; AUX-CF2-*-V2/-V3; AUX-CF2-OAI-SOL-V2, -LUNA-V2; AUX-WP-B-PNPRESENT,
%% -B-ORDERING; AUX-R110-A1-CR) and the difference row is AUX-R103-MARGIN (+0.0323, [+0.0060,+0.0617]; [+0.0077,+0.0608]).
\caption{Counterfactual obligation AUROC: $88$ supersession, $30$ retraction and $30$ expiry positives. Brackets: persona intervals. \pn{} vs \present{} and wins/ties/losses are post hoc; question-only AUROC is $0.50$. (Appendix~\ref{app:counterfactual})}
\label{tab:cf-main}
\centering
\scriptsize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}llrlrl@{}}
\toprule
Reader & Named states & AUROC & persona interval & \pn{} vs \present{} & W/T/L \\
\midrule
mini$^{a}$ & superseded & $0.76$ & $[0.72,0.80]$ & $0.74$ & $100/15/33$ \\
mini$^{a}$ & all & $0.83$ & $[0.79,0.87]$ & $0.83$ & $130/5/13$ \\
Haiku & superseded & $0.76$ & $[0.71,0.80]$ & $0.75$ & $89/52/7$ \\
Haiku & all & $0.88$ & $[0.84,0.91]$ & $0.87$ & $125/18/5$ \\
Luna & superseded & $0.84$ & $[0.80,0.88]$ & $0.85$ & $129/2/17$ \\
Sol & superseded & $0.85$ & $[0.81,0.88]$ & $0.85$ & $126/2/20$ \\
Opus & superseded & $0.84$ & $[0.80,0.88]$ & $0.84$ & $128/3/17$ \\
Opus & all & $0.91$ & $[0.88,0.94]$ & $0.91$ & $139/0/9$ \\
\midrule
\multicolumn{6}{@{}l}{\textit{Readers with no generative-model call}}\\
Name lookup & superseded & $0.77$ & $[0.72,0.81]$ & $0.77$ & $82/66/0$ \\
Name lookup & all & $0.88$ & $[0.84,0.91]$ & $0.87$ & $121/27/0$ \\
Count reader, guessed category & superseded & $0.66$ & $[0.63,0.70]$ & $0.64$ & $65/83/0$ \\
Count reader, given category & superseded & $0.60$ & $[0.58,0.64]$ & $0.59$ & $60/88/0$ \\
\bottomrule
\end{tabular}
\par\vspace{2pt}
\begin{tabular}{@{}lrll@{}}
\toprule
All-states comparison & difference & item interval & persona interval \\
\midrule
Opus minus name lookup & $+0.03$ & $[+0.01,+0.06]$ & $[+0.01,+0.06]$ \\
\bottomrule
\end{tabular}
\par\smallskip
\begin{minipage}{0.97\linewidth}\scriptsize
$^{a}$Mini uses the provider's default temperature here. Its earlier one-draw rows at temperature $0$ score $0.72$ and $0.80$; both draw count and temperature change (Table~\ref{tab:mini-k5}). The paired comparison is from Table~\ref{tab:counterfactual}.
\end{minipage}
\end{table}
"""

# ----------------------------------------------------------------------------------------------------------------------- Table 2's lower panel
TAB2_LOWER = r"""\par\vspace{4pt}
%% R126 (2026-09-19): the lower panel (the inbox's Table 2), part of Section 6: AUX-WP-A1 / the constrained rendering's losses (Section 7 of v21:
%% 0.10 on Mem0, 0.11 on A-MEM), the rebuilt name-bearing summary (0.88 Mem0, 0.90 A-MEM; AUX-SIDE-S1), the pooled 66 (GPT-5.6 Luna raw API 0.29;
%% GPT-5.6 Sol through the agent harness 0.10, the $^{h}$ rows of Appendix E.7).
\begin{tabular}{@{}p{0.70\linewidth}rr@{}}
\toprule
Coverage judgment, GPT-4.1 mini & Mem0 & A-MEM \\
\midrule
loss under the constrained rendering & $0.10$ & $0.11$ \\
score with the names rebuilt from ground truth & $0.88$ & $0.90$ \\
\midrule
\multicolumn{3}{@{}p{0.98\linewidth}@{}}{On the $66$ questions pooled across both stores, GPT-5.6 Luna (raw API) loses $0.29$ and GPT-5.6 Sol (agent tool) $0.10$.}\\
\bottomrule
\end{tabular}
"""

# ----------------------------------------------------------------------------------------------------------------------- Table 3 (the inbox's rows, our style)
TAB3 = r"""\begin{table}[h]
%% R126 (2026-09-19): Table 3 in the inbox's wording, our style; the rows are v21's tab:reach (reviews/v21/tools/ledger_r123_tables.py from
%% reviews/v21/results/reach_rows_r123.json, AUX-R123-REACH-ROWS, and reviews/r122/results/gate_reach.json, AUX-R122-GATE-*), unchanged.
\caption{Reach on the full obligation set: forbidding records among the $104$ obligations, mean lines over the $661$ questions, and licensed records among the $174$ items. Matched rows interpolate between depths (Table~\ref{tab:gatereach}, Appendix~\ref{app:resp}). No answer is scored here.}
\label{tab:reach}
\centering\scriptsize\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{0.9}
\begin{tabular}{@{}lrrrr@{}}
\toprule
Policy & \hd{Forbidding records}{in view (of $104$)} & rate & \hd{Mean lines}{per question} & \hd{Licensed record}{in view (of $174$)} \\
\midrule
Top-five retrieval & $54$ & $0.52$ & $5.00$ & $0.37$ \\
Similarity, matched budget & -- & $0.54$ & $5.43$ & $0.39$ \\
Newest per attribute, matched & -- & $0.23$ & $5.43$ & $0.29$ \\
Always-on fetch, matched & -- & $0.82$ & $5.43$ & $0.34$ \\
Lookup rule & $85$ & $0.82$ & $5.46$ & $0.37$ \\
Model rule & $85$ & $0.82$ & $5.43$ & $0.37$ \\
Oracle & $99$ & $0.95$ & $5.33$ & $0.37$ \\
\bottomrule
\end{tabular}
\end{table}
"""

# ----------------------------------------------------------------------------------------------------------------------- the evidence table (Section 3)
EVIDENCE = r"""\begin{center}
\small
%% R126 (2026-09-19): the inbox's evidence table; the first column widened (1.26in to 1.62in) so no label hyphenates (the brief, Phase 1.4); a tabular,
%% not a tabularx, because prose_scan and q_scan skip tabular environments only (the cells were read as an 81-word sentence).
\textbf{What kind of evidence supports each result?}\\[4pt]
\begin{tabular}{@{}p{1.62in}p{\dimexpr\linewidth-1.62in-2\tabcolsep\relax}@{}}
\toprule
Evidence & What it supports and what limits it\\
\midrule
Exact counterfactual labels & Constructed store versions isolate summary information; comparison with \present{} alone is post hoc.\\
Alignment-derived tags & Manifest-to-record matches support ablations, tagged views and reach; alignment can miss forbidding records.\\
Backend-native metadata & Censuses and store-written summaries describe the interfaces evaluated; census counts have no sampling interval.\\
Provisional answer judgments & A token detector flags stale or correct answers under retrieval policies and reference-assisted repairs.\\
\bottomrule
\end{tabular}
\par\vspace{2pt}\raggedright Evidence condensed from Appendix~\ref{app:provenance}.
\end{center}
"""

CONTRIB = r"""\begin{itemize}\setlength{\itemsep}{1pt}
%% R126 (2026-09-19), Phase 2.1: the author's three contributions, replacing the inbox's.
\item A counterfactual test of judgments made before retrieval. One question is asked of three versions of a store that differ in one attribute ($444$ items), so question wording cannot predict the label, and readers that make no generative-model call serve as baselines.
\item Evidence that names carry the judgment. The two models ablated score $0.12$ and $0.16$ lower on counts alone than on names alone; no model reliably exceeds a name lookup on the named state, and Luna, Sol and Opus lead it only through the states the summary merely counts.
\item A census of what four backends write and what it costs a reader. Under FR-Bank's own metadata mini and the lookup fall to $0.60$ and $0.59$, and at retrieval a fetch keyed on the names reaches as far without a model's judgment as with it.
\end{itemize}
"""


def main():
    check = "--check" in sys.argv
    b21 = rd(V21B)
    pre, fig1, def1, grid, fig2, census, tail = v21_pieces(b21)
    S = sections(rd(INBOX))
    assert list(S) == ["abstract", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "builders"], list(S)

    # ------------------------------------------------------------------------------------------------------------ the preamble
    pre = rep(pre, "% R118 (2026-09-19): paper_v21.tex, the v21 lineage opened from the R116 commit (e439141; paper_v19.tex as gates_r116b.txt records it):\n"
                   "% the v19 sources copied by reviews/v21/tools/bump_v21.py. The results of program R117 (E1 to E5) land here by ruling; v19 stays\n"
                   "% as committed, the fallback build on OpenReview. Built by reviews/v21/tools/build_v21.py; CLAIMS.md R118 block; reviews/v21/.\n"
                   "\\documentclass{article}\n",
              "% R118 (2026-09-19): paper_v21.tex, the v21 lineage opened from the R116 commit (e439141; paper_v19.tex as gates_r116b.txt records it):\n"
              "% the v19 sources copied by reviews/v21/tools/bump_v21.py. The results of program R117 (E1 to E5) land here by ruling; v19 stays\n"
              "% as committed, the fallback build on OpenReview. Built by reviews/v21/tools/build_v21.py; CLAIMS.md R118 block; reviews/v21/.\n"
              + R126_HEADER + "\\documentclass{article}\n")
    pre = rep(pre, "\\newtheorem{claim}{Claim}\n", "% R126 (2026-09-19): the bold run-in claim sentences of the readable body (the theorem environment 'claim' was unused).\n\\newcommand{\\claim}[1]{\\textbf{#1}}\n")
    pre = rep(pre, "\\usepackage[section,above]{placeins}", "\\usepackage[section,above]{placeins}")

    # ------------------------------------------------------------------------------------------------------------ the abstract
    a = conv(S["abstract"], "abstract")
    a = rep(a, "Third, backend metadata omit or misstate lifecycle information, weakening readers' judgments.\n",
            "%% R126 (2026-09-19), Phase 2.2: the author's third finding (AUX-E1R-BELIEVED-NOK 0.5959, AUX-E1R-NB6 0.5858, the capped store-written rows of Table tab:levels).\n"
            "Third, the backends we tested omit or misstate this information: under FR-Bank's own metadata, mini and the lookup fall to $0.60$ and $0.59$.\n")
    # R128 A1 (2026-09-20): which whole set; the margin is the counterfactual set's
    a = rep(a, "GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 lead overall by $0.07$ to $0.08$; Opus leads by $0.03$ when all states are named.",
            "%% R128 A1 (2026-09-20): the margin is on the counterfactual set (AUX-CF2-OAI-P-S1/-S2, AUX-R103-MARGIN); on the 661 no margin survives the persona interval.\n"
            "GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 lead it by $0.07$ to $0.08$ on the counterfactual set; Opus leads by $0.03$ when all states are named.")
    abstract = ("%% R126 (2026-09-19): the abstract of the readable body (reviews/v22/inbox/v22_readable_main.tex), ported by reviews/v22/tools/port_v22.py;\n"
                "%% the third finding is the author's (Phase 2.2). Spliced at %%ABSTRACT%% by build_v22.py.\n" + a.strip() + "\n")

    # ------------------------------------------------------------------------------------------------------------ Section 1
    s1 = conv(S["1"], "1")
    s1 = rep(s1, "\\section{Introduction}\\label{sec:intro}\n", "\\section{Introduction}\\label{sec:intro}\n\n%% R126 (2026-09-19): Sections 1 to 10 and the box are the readable body of reviews/v22/inbox/v22_readable_main.tex, ported by\n%% reviews/v22/tools/port_v22.py (the conversions and every wording change are recorded there and in reviews/v22/REPORT_R126.md).\n")
    # the contributions (Phase 2.1)
    s1 = rep(s1, cut(s1, "\\begin{itemize}\n", "\\end{itemize}\n"), CONTRIB)
    # Figure 1: the addendum's A1 (2026-09-20): the inbox's simplified three-box layout (tagged store; the summary route above the tag route; the reader
    # with its two judgments), the masked-retrieval note as a dashed line under the tag route; the caption unchanged (our adapted v21 TikZ, fig1_v22, is retired:
    # its masked-retrieval text collided with the reader box).
    s1 = rep(s1, "\\begin{figure}[t]\n\\centering\n\\begin{tikzpicture}[font=\\small,>=Latex,node distance=4mm,",
             "\\begin{figure}[t]\n\\centering\n%% R126 addendum A1 (2026-09-20): the inbox's three-box layout with the masked-retrieval note under the tag route; caption unchanged.\n"
             "\\begin{tikzpicture}[font=\\small,>=Latex,node distance=4mm,")
    s1 = rep(s1, "\\draw[arr] (tags.east) -- (reader.west);\n\\end{tikzpicture}\n",
             "\\draw[arr] (tags.east) -- (reader.west);\n"
             "\\coordinate (m1) at ($(tags.south west)+(0,-3.5mm)$);\n"
             "\\coordinate (m2) at ($(tags.south east)+(0,-3.5mm)$);\n"
             "\\draw[dashed,draw=black!55,->] (store.east |- m1) -- (m2);\n"
             "\\coordinate (mx) at ($(m1)!0.5!(m2)$);\n"
             "\\draw[thick,draw=black!60] ($(mx)+(-1.5mm,-1.5mm)$) -- ($(mx)+(1.5mm,1.5mm)$) ($(mx)+(-1.5mm,1.5mm)$) -- ($(mx)+(1.5mm,-1.5mm)$);\n"
             "\\node[anchor=north west,font=\\footnotesize,text=black!60,align=left,text width=3.0in] at ($(m1)+(0,-0.5mm)$) {masked retrieval: non-active records and their tags dropped; no tag route};\n"
             "\\end{tikzpicture}\n")
    s1 = rep(s1, "\\node[box,text width=1.62in,right=8mm of store,yshift=10mm] (summary)", "\\node[box,text width=1.62in,right=8mm of store,yshift=9mm] (summary)")
    s1 = rep(s1, "\\node[box,text width=1.62in,right=8mm of store,yshift=-16mm] (tags)", "\\node[box,text width=1.62in,right=8mm of store,yshift=-14mm] (tags)")
    # prose_scan Q-C (q_scan): the plain definition of the lifecycle summary must read 'with the values removed'; rule G4: Section 1's reader-claim anchor
    # ('name list' is one of the rule's anchor forms) must not follow the first mention of tags, which is this paragraph's last sentence.
    s1 = gate("Q-C and G4", "Section 1", s1,
              "A \\emph{lifecycle summary} lists record counts by state and attribute names, with stored values removed.",
              "A \\emph{lifecycle summary} lists record counts by state and, per category, an attribute-name list with the values removed.")
    s1 = gate("G4 (the anchor sentence in the R112 form)", "Section 1", s1,
              "Names carry most of the observed signal.\n", "Attribute names carry most of the observed signal.\n")
    # prose_scan rule D: Section 1's two restatements shared more than 70 percent of their content tokens with the abstract's and Section 5.2's sentences
    # (88 and 83 percent); the addendum's B1 (2026-09-20) gives the author's wording for both, which passes rule D against the abstract (67 percent).
    s1 = rep(s1, "No model reliably exceeds the lookup on the state named by the default summary.\n"
                 "Luna, Sol and Opus lead overall on that summary; Opus also leads when all states are named.\n",
             "%% R126 addendum B1 (2026-09-20): the author's two sentences (the inbox's tripped rule D against the abstract at 88 and 83 percent).\n"
             "On the one state the default summary names, no model reliably outscores the lookup.\n"
             "%% R128 A1 (2026-09-20): 'on the counterfactual set' for 'on the whole set'.\n"
             "Luna, Sol and Opus pull ahead of it on the counterfactual set, and Opus stays ahead by $0.03$ when every state is named.\n")
    GATE_CHANGES.append(("D (88% and 83% with the abstract); the author's B1 wording", "Section 1",
                         "No model reliably exceeds the lookup on the state named by the default summary. Luna, Sol and Opus lead overall on that summary; Opus also leads when all states are named.",
                         "On the one state the default summary names, no model reliably outscores the lookup. Luna, Sol and Opus pull ahead of it on the whole set, and Opus stays ahead by $0.03$ when every state is named."))

    # R129 A1 (2026-09-20): the author's ruling on R127b item 1 (Hu et al., Table 3, column FC-MH: every memory mechanism at most 7.0; the long-context
    # GPT-5-mini (400K) row 28.0, the paper's own 'at most 28%' sentence); the sentence in the author's words.
    s1 = rep(s1, "On MemoryAgentBench's multi-hop conflict-resolution questions, no memory agent exceeds $7\\%$ accuracy \\citep{memoryagentbench}.",
             "On MemoryAgentBench's multi-hop conflict-resolution questions, no memory mechanism exceeds $7\\%$ accuracy and the best long-context model reaches $28\\%$ \\citep{memoryagentbench}.")
    s1 = rep(s1, "Most memory evaluations score what an agent retrieves or answers", "%% R129 A1 (2026-09-20): the MemoryAgentBench sentence in the author's words (R127b item 1's ruling).\nMost memory evaluations score what an agent retrieves or answers")

    # ------------------------------------------------------------------------------------------------------------ Section 2: our citation keys restored at their sentences
    s2 = conv(S["2"], "2")
    for old, new in (("\\citep{lewis2020,flare,mallen2023,selfrag,su2024}", "\\citep{lewis2020,flare,mallen2023,ren2025,wang2023,selfrag,su2024,seakr,verbrouting,metamem}"),
                     ("\\citep{kamath2020,abstentionbench}", "\\citep{rajpurkar2018,kamath2020,yang2024,abstentionbench}"),
                     ("\\citep{kadavath2022,xiong2024}", "\\citep{kadavath2022,lin2022,tian2023,xiong2024}"),
                     ("\\citep{automem,supersede,packer2023,mem0,amem}", "\\citep{automem,supersede,packer2023,zhong2024,zhang2025survey,mem0,amem}"),
                     ("\\citep{cimemories,gatemem,hushbench}", "\\citep{nissenbaum2004,cimemories,maini2024,gatemem,pmbench,hushbench,statemembench}"),
                     ("\\citep{xu2024conflicts,dhingra2022}", "\\citep{xu2024conflicts,longpre2021,dhingra2022}")):
        s2 = rep(s2, old, new)
    # repeat_scan: 'must be suppressed for the answer to be right' in three places (Section 2, Section 3's labels paragraph, Definition 1 verbatim)
    s2 = gate("repeat_scan (a 9-gram in three places; Definition 1 is verbatim)", "Section 2", s2,
              "while obligation concerns content whose use must be suppressed for the answer to be right.",
              "while obligation concerns content whose use would make the answer wrong.")
    s2 = rep(s2, "\\section{Related work}\\label{sec:related}\n",
             "\\section{Related work}\\label{sec:related}\n%% R126 (2026-09-19): the inbox's citation lists are subsets of v21's at the same sentences; the sixteen keys the inbox dropped are restored\n%% at those sentences (no new entry; reviews/v22/REPORT_R126.md lists them), so every entry of the bibliography stays cited.\n")

    # ------------------------------------------------------------------------------------------------------------ Section 3
    s3 = conv(S["3"], "3")
    # Definition 1 is ours, with its grid, verbatim from body_v21.tex (the brief, Phase 1.3)
    inbox_def = cut(s3, "\\begin{center}\n\\small\n\\refstepcounter{definition}", "\\end{center}\n")
    # the addendum's A4 (2026-09-20): 'under $i(q)$' reads 'under the question's intent' (the symbol is never defined in the new body); the hike
    # paragraph loses its last two sentences (the grid's footnote says both)
    def1 = rep(def1, "must be suppressed for the answer to be right under $i(q)$;", "must be suppressed for the answer to be right under the question's intent;")
    s3 = rep(s3, inbox_def, "%% R126 (2026-09-19): Definition 1 and its grid restored from body_v21.tex, not retyped (the brief, Phase 1.3); addendum A4: 'under the question's intent' for 'under $i(q)$'.\n" + def1 + "\n" + grid)
    s3 = rep(s3, " The construction never labels a change question \\pn{}. Definition~\\ref{def:coverage} lists the combinations the construction defines.", "")
    # the addendum's A5: the two summary-size sentences move to Appendix E.3 (appendix_r126.py)
    s3 = rep(s3, "Summary size grows with categories, states and distinct names; at a fixed vocabulary, it does not grow with record count. Counts remain because the design fixed them before the study. The summary route reads",
             "%% R126 addendum A5 (2026-09-20): the two summary-size sentences moved to Appendix E.3.\nThe summary route reads")
    s3 = rep(s3, cut(s3, "\\begin{center}\n\\small\n\\textbf{What kind of evidence supports each result?}", "\\end{center}\n"), EVIDENCE)
    s3 = rep(s3, "\\section{Framework}\\label{sec:framework}\n",
             "\\section{Framework}\\label{sec:framework}\n%% R126 (2026-09-19): the notation box and Definition 2 (def:index) leave the body for Appendix E.1 (appendix_r126.py), so no symbol is orphaned.\n")

    # ------------------------------------------------------------------------------------------------------------ Section 4
    s4 = conv(S["4"], "4")
    s4 = rep(s4, cut(s4, "\\begin{figure}[t]\n", "\\end{figure}\n"), fig2_v22(fig2))
    # prose_scan rule V bars 'elicited', 'registered' and 'registrations' in the main text; q_scan Q-C needs the AUROC definition's exact words
    s4 = gate("V (elicited)", "Section 4", s4,
              "Luna's and Sol's shared cross-vendor rows are elicited through the vendor's agent tool.",
              "Luna's and Sol's shared cross-vendor rows are obtained through the vendor's agent tool.")
    s4 = gate("Q-C (the AUROC definition's words)", "Section 4", s4,
              "We score separation by AUROC, the chance that a positive ranks above a negative \\citep{hanley1982}.",
              "We score separation by AUROC, the chance that a positive scores above a negative \\citep{hanley1982}.")
    # q_scan Q-A: a body paragraph opens with a plain sentence carrying no numeral
    s4 = gate("Q-A (the opener carries numerals)", "Section 4", s4,
              "The \\emph{counterfactual set} contains $444$ items: $148$ questions, each asked of three versions of its store. Versions differ only in the target attribute.",
              "The \\emph{counterfactual set} asks each of its questions of three versions of one store. It contains $444$ items from $148$ questions, and the versions differ only in the target attribute.")
    s4 = gate("Q-A (the opener carries a numeral)", "Section 4", s4,
              "The \\emph{full obligation set} contains $661$ questions about the original stores and their variants, supporting the backend and retrieval comparisons.",
              "The \\emph{full obligation set} supports the backend and retrieval comparisons. It contains $661$ questions about the original stores and their variants.")
    # the prediction count: the repository's 92 / 28 (reviews/NUMBERS_R124.md AUX-R124-TALLY), not the inbox's 27 / 90 (R124 close: the count moved on the R123 rule)
    s4 = rep(s4, "The predictions were registered with a bar, each before the run that tests it: $27$ of $90$ came out otherwise. These registrations include follow-ups rather than a single plan fixed before all data collection. (Appendix~\\ref{app:registration})",
             "The predictions were registered with a bar, each before the run that tests it: $28$ of $92$ came out otherwise. They include follow-ups rather than a single plan fixed before all data collection. (Appendix~\\ref{app:registration})\n"
             "%% R126: the count is the repository's (AUX-R124-TALLY 92 / 28 after E10; the inbox's 27 / 90 predates R124 block E); rule V bars 'registrations' in the main text, and\n"
             "%% 'registered with a bar' is allowed by the addendum's B2 (tools/prose_scan.py, the R126 collocation).")
    GATE_CHANGES.append(("V (registrations); 'registered with a bar' kept by the addendum's B2, the rule gaining that collocation", "Section 4",
                         "These registrations include follow-ups", "They include follow-ups"))
    # R129 B1 (2026-09-20): E9's one prediction (P-M2, failed for both models) joins the count (AUX-R129-COUNT: 93 predictions, 29 otherwise).
    s4 = rep(s4, "each before the run that tests it: $28$ of $92$ came out otherwise.", "each before the run that tests it: $29$ of $93$ came out otherwise.")

    # ------------------------------------------------------------------------------------------------------------ Section 5
    s5 = conv(S["5"], "5")
    s5 = rep(s5, "\\section{What readers read}\\label{sec:counterfactual}\n", "\\section{What readers read}\\label{sec:counterfactual}\\label{sec:readers}\n")
    s5 = rep(s5, cut(s5, "\\begin{table}[t]\n\\caption{Counterfactual obligation AUROC", "\\end{table}\n"), TAB1)
    s5 = rep(s5, cut(s5, "\\begin{figure}[t]\n\\centering\n\\begin{tikzpicture}[x=1cm,y=1cm,font=\\footnotesize]", "\\end{figure}\n"), FIG3)
    # Phase 2.5: the two merges. (i) 'Knowing the category helps a count reader' folded into the paragraph before it, its bold lead dropped
    s5 = rep(s5, "It scores $0.67$ on retraction and $0.69$ on expiry. (Appendix~\\ref{app:counterfactual})\n\n"
                 "\\claim{Knowing the category helps a count reader.}\n"
                 "A reader given the manifest category reads its retracted-plus-expired count, scoring $0.73$ on retraction and $0.78$ on expiry.\n",
             "It scores $0.67$ on retraction and $0.69$ on expiry.\n"
             "%% R126 (2026-09-19), Phase 2.5: 'Knowing the category helps a count reader' folded into this paragraph, its bold lead dropped.\n"
             "A reader given the manifest category reads its retracted-plus-expired count, scoring $0.73$ on retraction and $0.78$ on expiry.\n")
    # (ii) 'Permuting the totals barely changes the models' scores' folded into 'A bare count can give the obligation away' as its closing sentences
    s5 = rep(s5, "Adding the obligation makes an empty count nonempty, so a reader can identify its store version without identifying its attribute. (Appendix~\\ref{app:counterfactual})\n\n"
                 "\\claim{Permuting the totals barely changes the models' scores.}\n"
                 "Permuting only the lifecycle totals moves mini, Haiku and Opus by at most $0.01$.\n"
                 "The category counts remain untouched, so this intervention does not test whether a reader uses those counts. (Appendix~\\ref{app:counterfactual})\n",
             "Adding the obligation makes an empty count nonempty, so a reader can identify its store version without identifying its attribute.\n"
             "%% R126 (2026-09-19), Phase 2.5: 'Permuting the totals barely changes the models' scores' folded in as the closing sentences.\n"
             "Permuting only the lifecycle totals moves mini, Haiku and Opus by at most $0.01$.\n"
             "The category counts remain untouched, so this intervention does not test whether a reader uses those counts. (Appendix~\\ref{app:counterfactual})\n")
    # prose_scan rule D against the abstract's second sentence (86%) and, after the addendum's B1, Section 1's first finding sentence: the claim in the
    # inbox's own words with 'the default named state' as 'supersession' (the paragraph's next sentence says the default summary names only supersession)
    s5 = gate("D (86% with the abstract's second sentence; 88% with the B1 sentence)", "Section 5.2", s5,
              "\\claim{No model reliably beats the lookup on the default named state.}",
              "\\claim{No model reliably beats the lookup on supersession.}")
    # the addendum's A6: the long-or-wrong-lists paragraph in the author's words
    s5 = rep(s5, "\\claim{Long or wrong name lists weaken the readers together.}\n"
                 "On the full obligation set, padding the default list lowers the lookup to $0.67$ at $60$ names; mini also falls.\n"
                 "Not every decline is reliable, and short ground-truth lists do not establish robustness to longer store-written lists.\n"
                 "On the counterfactual set, injecting wrong names also lowers mini, Haiku and the lookup together.\n"
                 "At the larger tested injection rate, neither model exceeds that lookup by more than $0.02$, and neither margin is reliable. (Appendix~\\ref{app:counterfactual})\n",
             "%% R126 addendum A6 (2026-09-20): the author's paragraph.\n"
             "\\claim{Long or wrong name lists weaken the readers together.}\n"
             "On the full obligation set, padding the default list to $60$ names lowers the lookup to $0.67$, and mini falls with it; on the counterfactual set, injecting wrong names lowers mini, Haiku and the lookup together.\n"
             "Not every decline is reliable, and short ground-truth lists do not establish robustness to longer store-written lists. (Appendix~\\ref{app:counterfactual})\n")
    s5 = gate("D (71% with the abstract's third sentence)", "Section 5.2", s5,
              "Luna, Sol and Opus reliably lead the lookup overall by $0.07$ to $0.08$.",
              "Luna, Sol and Opus reliably lead the lookup on the whole set by $0.07$ to $0.08$.")
    # slogan_scan S9 bars ', not ' in the main text
    s5 = gate("S9 (', not ')", "Section 5.1", s5,
              "This ablation uses mini's recorded single-call row, not the repeated-call row in Table~\\ref{tab:cf-main}.",
              "This ablation uses mini's recorded single-call row rather than the repeated-call row in Table~\\ref{tab:cf-main}.")
    # R129 C1 (2026-09-20): the payer in Section 5.1's first paragraph, the author's sentence (the single-call qualification folded in).
    s5 = rep(s5, "Counts alone score reliably below names alone: mini loses $0.12$, and Haiku loses $0.16$.\n"
                 "This ablation uses mini's recorded single-call row rather than the repeated-call row in Table~\\ref{tab:cf-main}. (Appendix~\\ref{app:counterfactual})\n",
             "%% R129 C1 (2026-09-20): the author's sentence.\n"
             "Counts alone score reliably below names alone: mini loses $0.12$ on its single-call row, and Haiku loses $0.16$. (Appendix~\\ref{app:counterfactual})\n")
    # R129 B1 (2026-09-20): Section 5.1's moved-count paragraph in the author's words; E9 (AUX-V2RCAT-A2-LUNA-K5, -SOL-K5: Luna and Sol fall reliably on
    # expiry, -0.1158 and -0.1914; on retraction -0.0664 and -0.0322 with intervals including zero) beside Opus 5 at five draws (AUX-V2RCAT-A1-OP5-K5:
    # -0.1003, -0.1281) and the two registered readers (AUX-V2RCAT-MINI, -H45: no change reliable under both intervals); reviews/NUMBERS_R129.md AUX-R129-E9-PRINTED.
    s5 = rep(s5, "\\claim{Only Opus follows a count when it moves.}\n"
                 "The \\emph{moved-count control} transfers the obligation's increment to a sibling store version while preserving the names.\n"
                 "A reader following that count should rank the wrong version higher.\n"
                 "Mini's expiry score rises by $0.06$, without a reliable difference; Haiku remains within tolerance.\n"
                 "Opus falls reliably by $0.10$ on retraction and $0.13$ on expiry when draw counts are matched. (Appendix~\\ref{app:counterfactual})\n",
             "%% R129 B1 (2026-09-20): the author's paragraph (E9 in the body).\n"
             "\\claim{The three stronger models follow a count when it moves.}\n"
             "The \\emph{moved-count control} transfers the obligation's increment to a sibling store version while preserving the names, so a reader following that count should rank the wrong version higher.\n"
             "Opus falls reliably by $0.10$ on retraction and $0.13$ on expiry when draw counts are matched.\n"
             "Luna and Sol fall reliably on expiry, by $0.12$ and $0.19$; their retraction falls, $0.07$ and $0.03$, do not clear zero.\n"
             "Mini and Haiku show no reliable change. (Appendix~\\ref{app:counterfactual})\n")
    # R129 B2 (2026-09-20): the hybrid reader's paragraph ('A cheap combined reader does not close the gap.', E10 in the body) was built at the
    # checkpoint 659737d and WITHDRAWN by the author's ruling on REPORT_R129.md (close without B2: with B1 and B2 both in, Figure 3 moved to
    # page 7 and the box to page 10; the hybrid returns with the Section 5 rewrite once R125 Task 1 reports). tab:cf-hybrid keeps the five-draw
    # mini row (AUX-R129-HYB-MINI5); the count keeps E9's prediction (93 / 29). The rule-V word ('left out' for 'held out') went with the paragraph.
    # R129 C2 (2026-09-20): the payer in Section 5.2, the long-or-wrong-lists paragraph in the author's words.
    s5 = rep(s5, "\\claim{Long or wrong name lists weaken the readers together.}\n"
                 "On the full obligation set, padding the default list to $60$ names lowers the lookup to $0.67$, and mini falls with it; on the counterfactual set, injecting wrong names lowers mini, Haiku and the lookup together.\n"
                 "Not every decline is reliable, and short ground-truth lists do not establish robustness to longer store-written lists. (Appendix~\\ref{app:counterfactual})\n",
             "%% R129 C2 (2026-09-20): the author's paragraph.\n"
             "\\claim{Long or wrong name lists weaken the readers together.}\n"
             "Padding the default list to $60$ names lowers the lookup to $0.67$ on the full obligation set, and injected wrong names lower mini, Haiku and the lookup together, so short ground-truth lists do not establish robustness to longer store-written ones. (Appendix~\\ref{app:counterfactual})\n")

    # ------------------------------------------------------------------------------------------------------------ Section 6
    s6 = conv(S["6"], "6")
    s6 = rep(s6, "\\section{What backends write}\\label{sec:backends}\n", "\\section{What backends write}\\label{sec:backends}\\label{sec:inversion}\\label{sec:stores}\n")
    # the addendum's A3 (2026-09-20): the first paragraph in the author's words (the interface details stay in the table rows)
    s6 = rep(s6, "\\claim{Backends omit or misstate the lifecycle information readers need.}\n"
                 "FR-Bank's census marks about $58$ times as many entries stale as ground truth, yet retains obsolete assertions as active.\n"
                 "It also conflates retraction with supersession.\n"
                 "Mem0 overwrites at the retrieval surface we evaluated (\\texttt{search} and \\texttt{get\\_all}, version 1.0.5); its per-memory history call was not consulted.\n"
                 "A-MEM's links fail to resolve to note identifiers in our integration.\n"
                 "Table~\\ref{tab:census} gives the census and matching scope. (Appendix~\\ref{app:census})\n",
             "%% R126 addendum A3 (2026-09-20): the author's paragraph.\n"
             "\\claim{Backends omit or misstate the lifecycle information readers need.}\n"
             "FR-Bank marks about $58$ times as many entries stale as ground truth, yet retains obsolete assertions as active and conflates retraction with supersession.\n"
             "Mem0 overwrites at the retrieval surface we evaluated, and A-MEM's links resolve to no note in our integration (Table~\\ref{tab:census}). (Appendix~\\ref{app:census})\n")
    # the addendum's A7: the Haiku paragraph moves to Appendix E.9 (appendix_r126.py); the FR-Bank paragraph's last sentence in the author's words
    s6 = rep(s6, "Haiku retains more of its gain than mini does. (Appendix~\\ref{app:census})\n\n"
                 "\\claim{Haiku fares better when FR-Bank keeps the target name.}\n"
                 "With the uncapped store-written summary, Haiku scores $0.87$ on supersession obligations whose name survives, against $0.89$ under ground truth.\n"
                 "Where the name is missing, its store-written score is $0.68$.\n"
                 "This descriptive split resembles the target-name ablation, but the missing-name subgroup is small and its paired decline is not reliable. (Appendix~\\ref{app:census})\n",
             "%% R126 addendum A7 (2026-09-20): the author's sentence; the 'Haiku fares better' paragraph moved to Appendix E.9 (AUX-BH-SPLIT).\n"
             "Haiku retains more of its gain than mini does, and more where the target's name survives the store's list ($0.87$ against $0.68$ where it does not; descriptive). (Appendix~\\ref{app:census})\n")
    # Table 2: our census (the upper part, verbatim) with the inbox's lower panel; the caption in the author's words (Phase 2.4) with the scripts named
    tab2_inbox = cut(s6, "\\begin{table}[t]\n\\caption{Backend census against the manifests.", "\\end{table}\n")
    c = census
    c = rep(c, "\\caption{A census of what each backend writes about itself, scored against the ground-truth manifests: counts with no sampling interval. FR-Bank's conflation of retraction with supersession is described in Appendix~\\ref{app:census}; the artifact's \\texttt{repro\\_mem0\\_erase.py} and \\texttt{repro\\_amem\\_links.py} reproduce the Mem0 and A-MEM rows.}",
            "%% R126 (2026-09-19): the upper part is v21's census, verbatim (the R124-F wording). The caption is the author's (addendum A2, 2026-09-20; Phase 2.4's sentence in its\n"
            "%% shorter form); the matching-threshold note, the conflation note and the two reproduction script names are in Appendix E.9.\n"
            "\\caption{Backend census: counts of disagreement with the manifest-and-alignment reference, without hand adjudication or sampling intervals. Lower panel: coverage losses and rebuilt-summary scores. (Appendices~\\ref{app:inversion} and~\\ref{app:census})}")
    c = rep(c, "\\end{tabular}\n\\end{table}\n", "\\end{tabular}\n" + TAB2_LOWER + "\\end{table}\n")
    s6 = rep(s6, tab2_inbox, c)
    # Phase 2.3: the Mem0 and A-MEM paragraph carries all four U5 conditions
    s6 = rep(s6, "Omitting or rewording the unavailable-field marker does not remove the Mem0 loss, and Luna loses under every rendering tested through the raw API.",
             "%% R126 (2026-09-19), Phase 2.3: the four U5 conditions in this paragraph (AUX-MARKER-*: the marker omitted or reworded; GPT-5.6 Luna 0.27 to 0.34 under every rendering).\n"
             "Omitting or rewording the unavailable-field marker does not remove the Mem0 loss, and Luna loses $0.27$ to $0.34$ under every rendering tested through the raw API.")
    # U5 is re-pinned to this paragraph's own sentence (the brief, Phase 2.3): claims_diff.U_BLOCKS and slogan_scan.PINNED carry the new string
    # "Scores compress toward a low value, but the trigger remains unresolved." (old: "What triggers the loss under the constrained rendering is
    # unresolved", the v21 Limitations pointer); the inbox sentence itself is unchanged. CLAIMS.md R126 shows old and new.
    assert s6.count("Scores compress toward a low value, but the trigger remains unresolved.") == 1
    # R128 A2 (2026-09-20): the author's sentence, checked against tab:dist (indexed positives 0.1617 against negatives 0.1688 on Mem0, 0.1544 against
    # 0.1658 on A-MEM; five distinct values); U5 re-pinned to it (claims_diff.U_BLOCKS, slogan_scan.PINNED; CLAIMS.md R128).
    s6 = rep(s6, "Scores compress toward a low value, but the trigger remains unresolved.",
             "Scores collapse onto a few low values, with positives slightly below negatives, and the trigger remains unresolved.")
    s6 = gate("S9 ('but ... not')", "Section 6", s6,
              "Removing the rendering cap raises their scores but does not restore their ground-truth results.",
              "Removing the rendering cap raises their scores without restoring their ground-truth results.")

    # ------------------------------------------------------------------------------------------------------------ Section 7
    s7 = conv(S["7"], "7")
    s7 = rep(s7, "\\section{At retrieval}\\label{sec:downstream}\n", "\\section{At retrieval}\\label{sec:downstream}\\label{sec:routes}\\label{sec:retrieval}\n")
    s7 = rep(s7, cut(s7, "\\begin{table}[t]\n\\caption{Reach on the full obligation set:", "\\end{table}\n"), TAB3)
    # the addendum's A8 (2026-09-20): the first two paragraphs merged in the author's words (the 0.79 / 0.82 pair leaves the body: AUX-RESP-A1-H45-HYBRID
    # 0.7863 and Haiku 4.5's ground-truth row 0.8210, verified; 'within tolerance' stands, the difference being -0.0347)
    s7 = rep(s7, "\\claim{The tagged view complements the summary for mini.}\n"
                 "On the full obligation set, FR-Bank's cosine search returns records without a lifecycle mask.\n"
                 "Mini scores $0.73$ with the default summary and $0.69$ with the retrieved records and their ground-truth tags.\n"
                 "Combining them raises its score reliably to $0.83$.\n"
                 "(Appendix~\\ref{app:resp})\n\n"
                 "\\claim{The view helps mini on expiry but hurts on supersession.}\n"
                 "Compared with the summary alone, mini gains $0.24$ on expiry and loses $0.17$ on supersession; both differences are reliable.\n"
                 "For Haiku, combining the view and summary scores $0.79$, below its summary-only $0.82$, though within tolerance.\n"
                 "(Appendix~\\ref{app:resp})\n",
             "%% R126 addendum A8 (2026-09-20): the author's merged paragraph (AUX-RESP-RETRIEVED, -HYBRID, AUX-RESP-A1-H45-HYBRID).\n"
             "\\claim{The tagged view complements the summary for mini.}\n"
             "On the full obligation set, FR-Bank's cosine search returns records without a lifecycle mask.\n"
             "Mini scores $0.73$ with the default summary, $0.69$ with the retrieved records and their ground-truth tags, and a reliable $0.83$ with both.\n"
             "The two routes mirror each other by state: against the summary alone, the view gains mini $0.24$ on expiry and costs it $0.17$ on supersession, both reliable.\n"
             "Haiku's score with both stays within tolerance of its summary alone. (Appendix~\\ref{app:resp})\n")

    # ------------------------------------------------------------------------------------------------------------ Sections 8 to 10 and the box
    s8 = conv(S["8"], "8")
    s8 = rep(s8, "\\section{Replication and the coverage judgment}\\label{sec:populations}\n",
             "\\section{Replication and the coverage judgment}\\label{sec:populations}\\label{sec:replication}\\label{sec:calibration}\\label{sec:coverage}\\label{sec:discrimination}\\label{sec:calibration-secondary}\\label{sec:ladder}\n")
    s9 = conv(S["9"], "9")
    s9 = rep(s9, "\\section{Limitations}\\label{sec:limitations}\n", "\\section{Limitations}\\label{sec:limitations}\\label{sec:discussion}\n")
    # q_scan Q-A: the third and fourth Limitations paragraphs open on a numeral; the third joins the second (whose opener is plain), the fourth's opener is split at its semicolon
    s9 = gate("Q-A (the paragraph opened on a numeral; joined to the paragraph before it)", "Section 9", s9,
              "with no open-weights model.\n\nTwo further encoders leave the default lookup within $0.01$ of its score.",
              "with no open-weights model.\nTwo further encoders leave the default lookup within $0.01$ of its score.")
    s9 = gate("Q-A (the opener carries numerals; split at the semicolon)", "Section 9", s9,
              "The ground-truth tags in retrieved views depend on aligning manifests to stored records; that alignment marks the forbidding record for $82$ of $104$ obligations.",
              "The ground-truth tags in retrieved views depend on aligning manifests to stored records. That alignment marks the forbidding record for $82$ of $104$ obligations.")
    s10 = conv(S["10"], "10")
    # prose_scan rule V bars the noun 'gate' in the main text (R123's precedent: 'always on' / 'gated')
    s10 = gate("V (gate)", "Section 10", s10,
               "reaches as far without a model gate as with one, at a budget trade-off.",
               "reaches as far ungated as gated, at a budget trade-off.")
    # slogan_scan S7 (a sentence twice) and prose_scan D (near-duplicate pairs): the Conclusion repeats Section 1's thesis sentence verbatim
    # slogan_scan S7 and prose_scan D: the inbox's Conclusion opened with Section 1's thesis sentence verbatim. The addendum's B3 (2026-09-20) gives the
    # author's sentence "In these tests, the information a store writes down counted for more than the choice of reader.", which shares 73 percent of its
    # content tokens with Section 1's sentence (rule D's bar is 70); one word changed, 'writes' to 'wrote', brings it to 64 percent. Listed for the author.
    s10 = gate("S7 and D (the sentence repeated Section 1's verbatim); the author's B3 sentence with 'wrote' for 'writes' (rule D, 73% to 64%)", "Section 10", s10,
               "In these tests, what the store writes down mattered more than which reader read it. Removing names",
               "In these tests, the information a store wrote down counted for more than the choice of reader. Removing names")
    s10 = s10.rstrip() + "\n"
    # R128 A3 (2026-09-20): Section 7's last paragraph, the author's sentence
    s7 = rep(s7, "This result limits that rule; it does not rule out other repairs that operate on retrieved content. (Appendix~\\ref{app:resp})",
             "%% R128 A3 (2026-09-20): the author's sentence.\nA reference-free repair for copies under other keys remains open. (Appendix~\\ref{app:resp})")
    # R129 A2 (2026-09-20): the inverted tag's parenthetical (AUX-R129-B9: 35 -> 34 once the tag is corrected).
    s7 = rep(s7, "Among $89$ scorable obligation views, $35$ contain an active line asserting the stale value.",
             "Among $89$ scorable obligation views, $35$ contain an active line asserting the stale value ($34$ once one inverted tag from the join is corrected).")
    s7 = gate("S17 ('the join' is barred in the main text; E.1 maps it to the ground-truth tags); the author's A2 parenthetical", "Section 7", s7,
              "($34$ once one inverted tag from the join is corrected)", "($34$ once one inverted ground-truth tag is corrected)")
    box = conv(S["builders"], "builders")
    # R128 A4 (2026-09-20): the box's lookup sentence gains the priced scenario (Appendix G.5: the historically measured mean monitor cost applied to
    # the cached-depth batch adds $0.289083 against maximum selector allowances of $0.038258 and $0.106836, the retrieval the selection saved)
    box = rep(box, "in our tests a model added something only on counted states, explicit intent questions, and the reported all-states comparison.",
              "in our tests a model added something only on counted states, explicit intent questions, and the reported all-states comparison, and in the scenario we priced, a model call before every query cost more than the retrieval it saved (Appendix~\\ref{app:utility-completion}).")
    box = rep(box, "\\end{minipage}}\n\\end{center}\n\\label{box:builders}\n\\label{mainend}\n", "\\end{minipage}}\\label{main-text-end}\n\\end{center}\n")
    box = rep(box, "\\begin{center}\n\\fbox{\\begin{minipage}{0.95\\linewidth}\n", "%% R126: the box as in the inbox (the R124-F wording); \\label{main-text-end} inside the minipage as in v21 (page_census_v2 keys on it).\n\\begin{center}\n\\fbox{\\begin{minipage}{0.97\\linewidth}\n")

    body = pre + s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9 + s10 + "\n" + box + "\n" + tail
    for bad in ("\\N{", "\\ap{", "\\PN", "\\PRESENT", "\\ABSENT", "tab:readers", "fig:triple", "fig:states", "def:state_intent", "sec:readers}", "sec:related_work", "sec:introduction", "\\label{mainend}"):
        assert bad not in body.replace("\\label{sec:readers}", ""), bad
    assert "\u2014" not in body and "\u2014" not in abstract, "em dash"
    body = re.sub(r"\n{3,}", "\n\n", body)
    if check:
        print("port_v22.py --check: would write", OUT_B, OUT_A)
        return
    io.open(OUT_B, "w", encoding="utf-8", newline="\n").write(body)
    io.open(OUT_A, "w", encoding="utf-8", newline="\n").write(abstract)
    # the inbox's number ledger, for the report (Phase 5.1)
    L = ["# INBOX_NUMBERS_R126.md: every \\N{value}{provenance} of the readable body, in order, as ported\n\n",
         "The provenance tag is the inbox's (a page and table of paper_v21.pdf); the gate that checks the printed form against the ledgers is trace_scan_v13 on the built paper_v22.tex.\n\n",
         "| # | section | value | inbox provenance |\n|---|---|---|---|\n"]
    for i, (v, p, s) in enumerate(NUMS, 1):
        L.append(f"| {i} | {s} | `{v}` | {p} |\n")
    io.open(OUT_NUMS, "w", encoding="utf-8", newline="\n").write("".join(L))
    print(f"-> {OUT_B} ({len(body.splitlines())} lines); {OUT_A}; {OUT_NUMS} ({len(NUMS)} numbers)")
    print("gate-driven wording changes:")
    for rule, sec, old, new in GATE_CHANGES:
        print(f"  [{rule}] {sec}\n     - {old[:150]}\n     + {new[:150]}")


if __name__ == "__main__":
    main()
