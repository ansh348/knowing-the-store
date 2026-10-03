# -*- coding: utf-8 -*-
"""appendix_r126.py -- program R126, Phase 4 (2026-09-20): attach and repair the appendix for the readable body. Every edit is an asserted
replacement on reviews/v22/src/appendix_v22.tex (OLD occurs exactly once; idempotent through marker checks; --check reports without writing).
The carried v11 blocks are repaired in reviews/v22/tools/build_v22.py (REPAIRS_R126_BLOCK), keyed to their line ranges.

  4.1  pointers: every \\ref to a body label resolves to the item that now carries the content (Section 5's sub-labels for the own-name ablation,
       the moved-count control and the model-versus-lookup comparison); no hardcoded number exists in the appendix (checked, none)
  4.2  vocabulary bridge: (a) the reader's guide (six to eight sentences) at the top of the appendix; (b) seven rows in E.1's terms table;
       (c) the captions of C.2's, E.7's, E.9's, E.10's reach tables and G.4's tables use the body's terms where they used the old ones
  E.1  the notation box and Definition 2 (def:index) move here from the body, verbatim from reviews/v21/src/body_v21.tex, so no symbol is orphaned
  4.3  the R124 leftovers are checked (they landed in v21); the tab:ds-a8 rows with an extra brace (21 inherited LaTeX errors) are repaired
  4.4  anonymity: registration calendar dates become day indices (day 0 = the first freeze) beside the hashes; nothing is marked as redacted
  4.5  Table 3's 5.46 and 5.33 (and 6.88, 7.07, 5.00) get their appendix home: three recorded rows in tab:gatereach's licensed panel
  4.6  E.3's coincidence sentence corrected to what reviews/v22/results/e3_intent_table.json shows, with the table (tab:e3-intent)
Usage: python reviews/v22/tools/appendix_r126.py [--check]
"""
from __future__ import annotations

import io
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
APPX = ROOT / "reviews" / "v22" / "src" / "appendix_v22.tex"
V21B = ROOT / "reviews" / "v21" / "src" / "body_v21.tex"
E3 = ROOT / "reviews" / "v22" / "results" / "e3_intent_table.json"
REACH = ROOT / "reviews" / "v21" / "results" / "reach_rows_r123.json"

DAY0 = "2026-08-10"
DAYS = {"2026-08-10": 0, "2026-08-11": 1, "2026-08-14": 4, "2026-08-24": 14, "2026-08-29": 19, "2026-08-30": 20, "2026-09-12": 33, "2026-09-13": 34,
        "2026-09-14": 35, "2026-09-15": 36, "2026-09-17": 38, "2026-09-18": 39, "2026-09-19": 40}
POINTERS = []   # (site, old pointer, new pointer)


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def rep(t, old, new, n=1, where=""):
    assert t.count(old) == n, (where, t.count(old), n, old[:100])
    return t.replace(old, new)


def cut(text, start, end):
    i = text.index(start)
    j = text.index(end, i) + len(end)
    return text[i:j]


GUIDE = r"""%% R126 (2026-09-20), Phase 4.2(a): the reader's guide (six to eight sentences): for each of the three findings the tables that carry it, the
%% provenance table, and the term bridge in one sentence. Replaces the R124 D1 guide.
\noindent\textbf{A reader's guide to the appendices.}
The appendices keep the vocabulary of the registered texts, which are quoted verbatim; in the main text, blind is \emph{question only}, indexed is \emph{with the summary}, route A is \emph{the summary route}, route B is \emph{the tag route}, NOK is \emph{the obligation judgment}, FOK is \emph{the coverage judgment}, the monitor is \emph{the reader}, and the structureless stores are \emph{Mem0 and A-MEM} (the rows of Appendix~\ref{app:glossary}'s terms table).
The first finding, that the summary's names carry the judgment and its counts do not, rests on Table~\ref{tab:cf-main} (every reader on the counterfactual set), Table~\ref{tab:cf-names-counts} (the summary with its counts or its names removed) and Table~\ref{tab:v2rcat} (the moved-count control).
The second, that on a named state no model reliably exceeds a name lookup and three models pull ahead only where the summary counts, rests on Table~\ref{tab:sup-margins} (each model's supersession-only margin), Table~\ref{tab:counterfactual} (every margin over the lookup with both intervals) and Table~\ref{tab:cf-intent} (the intent crossover).
The third, that the backends write the summary poorly, rests on Table~\ref{tab:census} (the census), Table~\ref{tab:levels} (the store-written summary's levels) and Table~\ref{tab:graphiti-completed} (the fourth backend).
The reach of a lifecycle fetch at retrieval is Tables~\ref{tab:reach} and~\ref{tab:gatereach}.
Every headline number's population, label source, tag source and evaluator are in Table~\ref{tab:provenance} (Appendix~\ref{app:provenance}).
The registration record, with each freeze's hash and its day in the registration order, is Appendix~\ref{app:registration}.
"""

BRIDGE_ROWS = r"""%% R126 (2026-09-20), Phase 4.2(b): the appendix prose's terms beside the main text's (the reader's guide gives the same bridge in one sentence).
blind & question only (the reader sees the question alone) \\
indexed & with the summary (the reader sees the question and the summary) \\
route A & the summary route \\
route B & the tag route \\
NOK & the obligation judgment \\
FOK & the coverage judgment \\
the monitor & the reader (a name lookup or a model) \\
the structureless stores & Mem0 and A-MEM, the two backends that record no lifecycle state \\
"""


def e3_table():
    d = json.loads(E3.read_text(encoding="utf-8"))
    c = d["counts"]
    intents = [("CURRENT-STATE", "\\textsc{current}"), ("UPCOMING", "\\textsc{upcoming}"), ("PAST-EVENT", "\\textsc{past}"), ("CHANGE-AWARE", "\\textsc{change}")]
    labels = [("PRESENT-NEGATIVE", "\\pn{}"), ("PRESENT", "\\present{}"), ("ABSENT", "\\absent{}")]
    states = d["states"]
    rows = []
    for ik, iname in intents:
        for lk, lname in labels:
            vals = [c.get(f"{ik}|{lk}|{s}", 0) for s in states]
            if sum(vals):
                rows.append(f"{iname} & {lname} & " + " & ".join(f"${v}$" for v in vals) + f" & ${sum(vals)}$ \\\\")
    return ("%% R126 (2026-09-20), Phase 4.6: the state-by-intent-by-label counts of the 661, written from reviews/v22/results/e3_intent_table.json\n"
            "%% (reviews/v22/tools/e3_intent_table.py; reviews/NUMBERS_R126.md AUX-R126-E3-INTENT); do not edit by hand.\n"
            "\\begin{table}[H]\n"
            "\\caption{The $661$ questions of the full obligation set by intent, label and the state of the question's own attribute. For a \\pn{} question the state is the forbidding record's, from the manifest; for a \\present{} question it is the first of retracted, superseded and expired that the ground-truth join puts on any record of the question's own attribute in its store version, else active only (unaligned: no gold record is aligned, the ten past-event questions); an \\absent{} question has no such record. Every \\pn{} question has current or upcoming intent, and $44$ \\present{} questions hold a non-active record of their own attribute: $33$ under current or upcoming intent, where the label follows the record the question targets, and $11$ under change intent, where intent licenses the old content (the $4$ with a superseded record are the items Appendix~\\ref{app:counterfactual} counts).}\n"
            "\\label{tab:e3-intent}\n"
            "\\centering\\scriptsize\\setlength{\\tabcolsep}{4pt}\n"
            "\\begin{tabular}{@{}llrrrrrrr@{}}\n\\toprule\n"
            "Intent & Label & superseded & retracted & expired & active only & unaligned & none & total \\\\\n\\midrule\n"
            + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def gatereach_rows():
    p = json.loads(REACH.read_text(encoding="utf-8"))["policies"]
    def row(name, k):
        r = p[k]
        return (f"{name} & ${r['licensed_in_view']}$ = ${r['licensed_rate']:.4f}$ & -- & -- & -- & ${r['mean_lines_661']:.2f}$ & ${r['mean_lines_104']:.2f}$ \\\\")
    return "\n".join([row("Top-five retrieval (recorded)", "ALWAYS"), row("Lookup rule (recorded)", "LOOKUP"), row("Oracle (recorded)", "ORACLE")]) + "\n"


def main():
    check = "--check" in sys.argv
    t = rd(APPX)
    b21 = rd(V21B)
    if "%% R126 (2026-09-20), Phase 4.2(a)" in t:
        print("appendix_r126.py: already applied"); return

    # ---- 4.2(a) the reader's guide
    old_guide = cut(t, "%% R124 D1 (2026-09-19): a reader's guide to the seventy-odd tables, one line per finding, then the provenance table.\n",
                    "the registration record is Appendix~\\ref{app:registration}.\n")
    t = rep(t, old_guide, GUIDE)

    # ---- 4.1 pointers to Section 5's sub-labels
    t = rep(t, "so the model-versus-lookup comparison of Section~\\ref{sec:counterfactual} is the same on the harder comparison",
            "so the model-versus-lookup comparison of Section~\\ref{sec:lookup} is the same on the harder comparison")
    POINTERS.append(("C.2, the PN-versus-PRESENT paragraph", "Section~\\ref{sec:counterfactual} (v21 Section 5)", "Section~\\ref{sec:lookup} (5.2)"))
    t = rep(t, "Own-name ablation, $0.86$ to $0.53$ (Section~\\ref{sec:counterfactual})", "Own-name ablation, $0.86$ to $0.53$ (Section~\\ref{sec:names_counts})")
    POINTERS.append(("E.12, tab:provenance, the own-name ablation row", "Section~\\ref{sec:counterfactual}", "Section~\\ref{sec:names_counts} (5.1)"))
    t = rep(t, "Moved-count control (Section~\\ref{sec:counterfactual})", "Moved-count control (Section~\\ref{sec:names_counts})")
    POINTERS.append(("E.12, tab:provenance, the moved-count row", "Section~\\ref{sec:counterfactual}", "Section~\\ref{sec:names_counts} (5.1)"))

    # ---- E.1: the notation box and Definition 2 from the body (verbatim), and the bridge rows in the terms table
    def2 = cut(b21, "\\begin{definition}[Lifecycle summary]\\label{def:index}", "\\end{definition}\n")
    box = cut(b21, "\\begin{center}\n\\setlength{\\fboxsep}{1.5pt}", "\\end{minipage}}\n\\end{center}\n")
    t = rep(t, "The two blocks below define every term the main text uses, and a third block in the supplement (Section~S.5) maps the internal names a reader meets in the registrations, ledgers and row files onto the paper's term.\n",
            "The two blocks below define every term the main text uses, and a third block in the supplement (Section~S.5) maps the internal names a reader meets in the registrations, ledgers and row files onto the paper's term.\n"
            "The notation box and the definition of the lifecycle summary, which the main text stated in full until this version, follow the two blocks, so that every symbol the appendices use is defined here.\n")
    t = rep(t, "%% R110: Definition 3 of v17 returns to vocabulary here (rule G3; READER_CLAIM.md section 2).\n",
            "%% R126 (2026-09-20): the notation box and Definition 2 (def:index), verbatim from reviews/v21/src/body_v21.tex (the readable body states the summary in\n"
            "%% prose, Section 3); Appendix E.6's carried U7 sentence refers to Definition~\\ref{def:index}, which resolves here.\n"
            + box + def2 +
            "%% R110: Definition 3 of v17 returns to vocabulary here (rule G3; READER_CLAIM.md section 2).\n")
    t = rep(t, "\\paragraph{The artifact's names in the registered texts.}\n", "\\paragraph{The artifact's names in the registered texts, and the appendix prose's terms in the main text.}\n")
    t = rep(t, "Six of those names differ from this paper's terms.\n", "Six of those names differ from this paper's terms, and eight terms of the appendix prose differ from the main text's; the table gives both.\n")
    t = rep(t, "In the registered texts & In this paper \\\\\n\\midrule\n", "In the registered texts or the appendix prose & In this paper's main text \\\\\n\\midrule\n")
    t = rep(t, "user profile & persona \\\\\n\\bottomrule\n", "user profile & persona \\\\\n\\midrule\n" + BRIDGE_ROWS + "\\bottomrule\n")

    # ---- 4.6 E.3's sentence and the table
    t = rep(t, "In the main populations every \\pn{} question has current or upcoming intent by construction, so there a staleness judgment and an obligation judgment coincide; they come apart only in the crossover of Appendix~\\ref{app:counterfactual}.\n",
            "%% R126 (2026-09-20), Phase 4.6: the sentence corrected to what tab:e3-intent shows (reviews/v22/results/e3_intent_table.json); flagged for the author's check in REPORT_R126.md.\n"
            "In the main populations every \\pn{} question has current or upcoming intent by construction (Table~\\ref{tab:e3-intent}), but a staleness judgment and an obligation judgment do not coincide even there: $44$ of the $174$ \\present{} questions hold a non-active record of their own attribute, $33$ under current or upcoming intent, where the label follows the record the question targets, and $11$ under change intent, where intent licenses the old content; the crossover of Appendix~\\ref{app:counterfactual} is where the two judgments are separated on one store.\n"
            + e3_table())

    # ---- the addendum (2026-09-20): A2, Table 2's caption notes to E.9; A5, Section 3's summary-size sentences to E.3; A7, the Haiku paragraph to E.9
    t = rep(t, "The manifests record $40$ retraction events, one per persona, and the ground-truth join resolves $9$ of them to a retracted entry ($23$ entries).\n",
            "The manifests record $40$ retraction events, one per persona, and the ground-truth join resolves $9$ of them to a retracted entry ($23$ entries).\n"
            "%% R126 addendum A2 (2026-09-20): Table 2's caption notes moved here (the matching threshold; the two reproduction scripts; the conflation note is the sentence above).\n"
            "The count of retained active assertions in Table~\\ref{tab:census} depends on the stored-versus-obsolete matching threshold of the census, and the artifact's \\texttt{repro\\_mem0\\_erase.py} and \\texttt{repro\\_amem\\_links.py} reproduce the table's Mem0 and A-MEM rows from the frozen banks.\n")
    t = rep(t, "Listing~\\ref{lst:summary} is the abridged summary the indexed monitor sees, rendered from the store of one persona.\n",
            "Listing~\\ref{lst:summary} is the abridged summary the indexed monitor sees, rendered from the store of one persona.\n"
            "%% R126 addendum A5 (2026-09-20): Section 3's two summary-size sentences moved here.\n"
            "Summary size grows with categories, states and distinct names; at a fixed vocabulary, it does not grow with record count. Counts remain because the design fixed them before the study.\n")
    t = rep(t, "\\paragraph{Haiku 4.5 under the store's own metadata.}\n",
            "%% R126 addendum A7 (2026-09-20): Section 6's 'Haiku fares better' paragraph moved here in the readable body's words (AUX-BH-SPLIT: 0.8658 / 0.8855 on 53; 0.6839 on 10).\n"
            "Haiku 4.5 fares better where FR-Bank keeps the target's name: with the uncapped store-written summary it scores $0.87$ on the supersession obligations whose name survives, against $0.89$ under ground truth, and $0.68$ where the name is missing (Table~\\ref{tab:bh-split}). This descriptive split resembles the target-name ablation, but the missing-name subgroup is small and its paired decline is not reliable.\n\n"
            "\\paragraph{Haiku 4.5 under the store's own metadata.}\n")

    # ---- 4.5 the recorded rules' rows in tab:gatereach's licensed panel (5.46 and 5.33 of Table 3)
    t = rep(t, "Model rule (recorded) & $65$ = $0.3736$ & -- & -- & -- & $5.43$ & $7.08$ \\\\\n",
            "%% R126 (2026-09-20), Phase 4.5: the recorded policies of Table 3 beside the model rule, from reviews/v21/results/reach_rows_r123.json (AUX-R123-REACH-ROWS; reviews/NUMBERS_R126.md AUX-R126-GATEREACH), so Table 3's $5.46$ and $5.33$ have an appendix home.\n"
            "Model rule (recorded) & $65$ = $0.3736$ & -- & -- & -- & $5.43$ & $7.08$ \\\\\n" + gatereach_rows())
    t = rep(t, "Upper panel: the forbidding record in view over the $104$ obligations with the Wilson int", "Upper panel: the forbidding record in view over the $104$ obligations with the Wilson int")

    # ---- 4.2(c) captions in the body's terms (prose tables; the carried blocks' captions are build repairs)
    t = rep(t, "Obligation AUROC per reader and summary; blind is $0.5000$ by construction on every set, so each value is also a gain.",
            "Obligation AUROC per reader and summary; question only (blind) is $0.5000$ by construction on every set, so each value is also a gain.")
    t = rep(t, "on the two structureless stores, blind against indexed under the constrained rendering, from the recorded rows:",
            "on the two structureless stores, question only (blind) against with the summary (indexed) under the constrained rendering, from the recorded rows:")
    t = rep(t, "and with the marker's three lines reworded to say the store does not record the field (neutral), against blind.",
            "and with the marker's three lines reworded to say the store does not record the field (neutral), against question only (blind).")
    t = rep(t, "Differences against blind carry the item-level and the persona-grouped interval.", "Differences against question only carry the item-level and the persona-grouped interval.")
    t = rep(t, "assembled from the recorded ranking and the store's records with no monitor call and no answer call, against the recorded model rule.",
            "assembled from the recorded ranking and the store's records with no reader (monitor) call and no answer call, against the recorded model rule.")

    # ---- 4.3 the inherited LaTeX errors: tab:ds-a8's two rows close one brace too many
    t = rep(t, "oracle: $6$/$17$ $\\to$ $1$/$8$; correct $11 \\to 7$}} \\\\", "oracle: $6$/$17$ $\\to$ $1$/$8$; correct $11 \\to 7$} \\\\")
    t = rep(t, "oracle: $4$/$15$ $\\to$ $2$/$5$; correct $11 \\to 7$}} \\\\", "oracle: $4$/$15$ $\\to$ $2$/$5$; correct $11 \\to 7$} \\\\")

    # ---- 4.4 anonymity: day indices in the registration record, nothing marked as redacted
    t = rep(t, "This appendix is the registration record: each frozen artifact, its commit, freeze date, scope and outcome.\n",
            "This appendix is the registration record: each frozen artifact, its commit or file hash, its freeze day, scope and outcome.\n"
            "%% R126 (2026-09-20), Phase 4.4: calendar dates replaced by the day index of the registration order (day $0$ is the first freeze; reviews/NUMBERS_R126.md AUX-R126-DAYS), so no date precedes the FR-Bank preprint's public date in the PDF.\n"
            "Freeze days count from the first freeze, day $0$; the rows of each table follow the registration order, and the hashes identify the frozen files.\n")
    for tab in ("tab:registrations-b", "tab:registrations-c", "tab:registrations-d"):
        i = t.index("\\label{" + tab + "}"); j = t.index("\\end{table}", i)
        blk = t[i:j]
        new = blk.replace("Artifact & Commit hash & Freeze date & What it froze & Outcome \\\\", "Artifact & Commit hash & Freeze day & What it froze & Outcome \\\\")
        new = new.replace("Artifact & sha256 (first bytes) & Freeze date & What it froze & Outcome \\\\", "Artifact & sha256 (first bytes) & Freeze day & What it froze & Outcome \\\\")
        new = re.sub(r"& (2026-\d\d-\d\d) &", lambda m: f"& day {DAYS[m.group(1)]} &", new)
        assert "Freeze day" in new and not re.search(r"2026-\d\d-\d\d", re.sub(r"%.*", "", new)), tab
        t = t[:i] + new + t[j:]
    t = rep(t, "each hashed by the runner before its first call (the commits of 18 September do not date them)", "each hashed by the runner before its first call (the commits of day 39 do not date them)")
    t = rep(t, "in the main study's preregistration (2026-08-10) for coverage retention", "in the main study's preregistration (day $0$ of the registration record, Appendix~\\ref{app:registration}) for coverage retention")
    t = rep(t, "A fourth amendment, registered on 2026-09-14 with two predictions,", "A fourth amendment, registered on day $35$ of the registration record with two predictions,")
    t = rep(t, "first committed on 18 September 2026, the evidence that the text predates the run is the runner's lock record and the file times.",
            "first committed on day $39$, the evidence that the text predates the run is the runner's lock record and the file times.")
    t = rep(t, "(the cross-vendor addendum, Table~\\ref{tab:registrations}; 2026-08-14), carrying three of its predictions. That freeze came after the main-study freeze of 2026-08-10 and before the counterfactual freeze of 2026-08-29.",
            "(the cross-vendor addendum, Table~\\ref{tab:registrations}; day $4$), carrying three of its predictions. That freeze came after the main-study freeze of day $0$ and before the counterfactual freeze of day $19$.")
    t = rep(t, "does not reproduce where the lifecycle record is thinner.'' (The quotation is redacted for anonymity.)",
            "does not reproduce where the lifecycle record is thinner.'' (The bracketed words stand in for the store's name as the registered text gives it.)")
    body_dates = re.findall(r"2026-0[89]-\d\d", "\n".join(l for l in t.split("\n") if not l.lstrip().startswith("%")))
    assert not body_dates, body_dates

    if check:
        print("appendix_r126.py --check: every OLD found; nothing written"); return
    io.open(APPX, "w", encoding="utf-8", newline="\n").write(t)
    print(f"-> {APPX}")
    print("pointers retargeted:")
    for site, old, new in POINTERS:
        print(f"  {site}: {old} -> {new}")


if __name__ == "__main__":
    main()
