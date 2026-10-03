# -*- coding: utf-8 -*-
"""port_r131_close.py -- the R131 close (2026-09-20; the author's blocks 'R131 CONSOLIDATED ADDITIONS' (L, A, P, O), 'ABSTRACT SWAP + ITS PAYER'
(B1 to B5), 'R131 MERGED RULINGS' (1A, 1B, 1C, 2, 3, 4, 5) and 'R131 FINAL RULINGS' (1 to 8)): the body and abstract landings, applied to
reviews/v22/src/body_v22.tex and abstract_v22.tex after port_v22.py and port_r131.py --payers=1,2,3,4 (regeneration order: cp v21 -> appendix_r126.py
-> appendix_r128.py -> appendix_r129.py -> appendix_r131.py -> appendix_r131_close.py -> fig3_data.py -> fig3_data_r131.py -> port_v22.py ->
port_r131.py --payers=1,2,3,4 -> port_r131_close.py [--payers=5,5b,6,7,8,B2] [--o1]). Every edit is an asserted replacement (rep); the author's
texts are verbatim with the LaTeX conversions of port_v22.py (numerals in math mode, \\pn{} / \\present{}, citations as \\citep, Appendix pointers as
\\ref); every number the texts print passed reviews/v22/tools/r131_close_gate.py first (37 checks, 0 mismatches); every gate-driven wording change is
named with its rule in GATES and printed at the end (the report and CLAIMS.md list old beside new). The abstract is hand-tuned (B4): no gate changes a
word of it; a trip is reported and the author rules.
Landings without a payer flag: L1 to L4 (Limitations, Section 4), A1' (Section 4's provenance sentences), A2' and the tex-658 word drop (the AI-use
statement), B1 (the abstract, verbatim), 1A (Table 1's caption note), 1B (the builders box's clause), 4 (L2's 'completed only').
Payers, cumulative in the ruled order: 5 (Section 5.1's target-name paragraph out; the pointer), 5b (the Conclusion's intent sentence), 6 (the 5.3
cuts P6a to P6d), 7 (Figure 3's height 5.0cm -> 4.5cm), 8 (Section 5.2's list-length paragraph to two sentences), B2 (Section 1's findings paragraph
cut to two sentences). --o1 lands O1 (the Conclusion's two closing sentences; only at slack +5 or better).
Usage: python reviews/v22/tools/port_r131_close.py [--payers=5,5b,6,7,8,B2] [--o1] [--check]
"""
from __future__ import annotations

import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT_B = ROOT / "reviews" / "v22" / "src" / "body_v22.tex"
OUT_A = ROOT / "reviews" / "v22" / "src" / "abstract_v22.tex"
sys.path.insert(0, str(ROOT / "reviews" / "v22" / "tools"))

GATE_CHANGES = []  # (rule, section, before, after)
CHANGES = []       # (item, section, before, after, reason): every ruled change, old beside new, for the report and CLAIMS.md


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def rep(t, old, new, n=1, where=""):
    assert t.count(old) == n, (where, t.count(old), n, old[:120])
    return t.replace(old, new)


def change(item, section, t, old, new, reason):
    CHANGES.append((item, section, old, new, reason))
    return rep(t, old, new, 1, item + " " + section)


def gate(rule, section, t, old, new):
    GATE_CHANGES.append((rule, section, old, new))
    return rep(t, old, new, 1, rule + " " + section)


AP = "(Appendix~\\ref{app:counterfactual})"

# --------------------------------------------------------------------------------------------------------------- B1. the abstract, verbatim (ABSTRACT SWAP)
ABS_NEW = ("\\begin{abstract}\n"
           "%% R131 close, B1 (2026-09-20): the author's abstract, verbatim (ABSTRACT SWAP + ITS PAYER; hand-tuned, B4: no gate changes a word of it). Numbers: r131_close_gate.py\n"
           "%% (148 = the triples; 0.88 = the sibling floor, Haiku 0.8807, AUX-CF2-R125-SB-*; 0.08 to 0.10 = AUX-CF2-R125-VS-LOOKUP +0.0811 to +0.1014; 0.73 / 0.75 -> 0.60 / 0.59 = AUX-E1R-TRUE-NOK 0.7339,\n"
           "%% AUX-E1R-NB6 0.7484 / 0.5858, AUX-E1R-BELIEVED-NOK 0.5959; chance 0.50). The last clause is a placeholder (B5): it is replaced when the HV-1 numbers exist.\n"
           "An agent with long-term memory can answer from a record it should no longer use, such as a plan the user later cancelled.\n"
           "We test whether an agent can tell, before retrieving anything, that its store holds such a record, from a summary alone: the number of records in each lifecycle state, and a list of attribute names with the values removed.\n"
           "Each of $148$ questions is asked against three versions of one store that differ in one attribute, so a question's wording cannot give the answer away.\n"
           "First, ablations show that the two smaller of five models rely on the attribute names alone, while the three stronger ones also use the state counts.\n"
           "Second, for superseded records, the one state whose names the summary lists, no model reliably beats a cosine-similarity lookup over those names.\n"
           "Under a control that holds counts and list length fixed, the lookup and every model pick the correct name over a similar one at an AUROC of $0.88$ or higher (chance $0.50$).\n"
           "The stronger models lead the lookup by $0.08$ to $0.10$ overall, a lead that comes from retracted and expired records, which the summary only counts; adding one count feature to the lookup closes it.\n"
           "Third, the memory backends we tested omit or misstate this information.\n"
           "Given only what FR-Bank, a backend that tags every entry with a lifecycle state, actually writes, GPT-4.1 mini and the lookup drop from $0.73$ and $0.75$ to $0.60$ and $0.59$ on our larger question set.\n"
           "In these tests, what the store wrote down mattered more than which model read it.\n"
           "All stores are synthetic, and whether better judgments yield better answers is not established; human validation is pending.\n"
           "\\end{abstract}\n")

# --------------------------------------------------------------------------------------------------------------- L. Limitations; L4 Section 4
L1_OLD = "The counterfactual test bypasses backend writing; FR-Bank and Graphiti use the same personas."
L1_NEW = "All tests use one bank of $40$ synthetic personas; transfer to a second benchmark is untested. The counterfactual test bypasses backend writing, and no backend tested here is shown maintaining the summary."
L2_OLD = "The capability comparison on the counterfactual set covers closed models from two vendors, with no open-weights model."
L2_NEW = "The counterfactual comparison covers closed models from two vendors; the one open-weights model, Kimi K3, completed only the cross-vendor replication."
L3_OLD = "Under the explicit-intent rubric, only mini and Luna were rerun on the original counterfactual task: both stay within $0.02$ of their main-study scores, and Luna retains a reliable lookup margin. " + AP
L3_NEW = "Under the explicit-intent rubric only mini and Luna were rerun. " + AP
L4_OLD = "Kimi K3 joins the smaller comparison shared across vendors."
L4_NEW = "Kimi K3 (open weights) joins the smaller comparison shared across vendors."

# --------------------------------------------------------------------------------------------------------------- A. provenance (A1', A2', the tex-658 word drop)
A1_OLD = "Language models generate the questions and synthetic persona stores from human-written manifests."
A1_NEW = ("%% R131 close, A1' (2026-09-20): the author's provenance sentences (FINAL RULINGS 1); the counts and the Graphiti construction verified in r131_close_gate.py; the paragraph in Appendix E.3 (A1'').\n"
          "The personas, their human-written manifests and sessions, the FR-Bank, Mem0 and A-MEM stores and part of the main question set come from the FR-Bank release \\citep{fr}. "
          "Language models drafted our other questions, and we built the Graphiti graphs from the released FR-Bank records, with lifecycle fields removed. (Appendix~\\ref{app:construction})")
A2_OLD = ("We used generative AI tools for synthetic data generation and for implementation.\n"
          "The synthetic persona bank, the stores built from it, and every question set were generated with large language models from human-written manifests and specifications, and those manifests are the ground truth against which every label is scored.\n")
A2_NEW = ("%% R131 close, A2' (2026-09-20): the author's statement (MERGED RULINGS 2; the Graphiti clause as verified against r85_graphiti/render_episodes.py, FINAL RULINGS 1).\n"
          "We used generative AI tools to draft questions and for implementation.\n"
          "The persona bank, its sessions and the FR-Bank, Mem0 and A-MEM stores are a released synthetic benchmark \\citep{fr}.\n"
          "Language models drafted the question sets we added, and Graphiti's language-model pipeline built our graphs from the released FR-Bank store's records, rendered one episode per session without its lifecycle fields; the benchmark's human-written manifests are the ground truth against which every label is scored.\n")
A5_OLD = "executed the experimental protocols under preregistered, human-directed designs with frozen decision rules,"
A5_NEW = "executed the experimental protocols under human-directed designs with frozen decision rules,"

# --------------------------------------------------------------------------------------------------------------- 1A, 1B (MERGED RULINGS)
TAB1_CAP_OLD = "Question-only AUROC is $0.50$. (Appendix~\\ref{app:counterfactual})}"
TAB1_CAP_NEW = "Question-only AUROC is $0.50$. Differences at four decimals. (Appendix~\\ref{app:counterfactual})}"
BOX_OLD = "in our tests a model added something only on counted states, explicit intent questions, and the reported all-states comparison, and in the scenario we priced,"
BOX_NEW = "in our tests a model added something only on counted states, on explicit intent questions and, on the pooled metric only, in the all-states comparison, and in the scenario we priced,"

# --------------------------------------------------------------------------------------------------------------- the payers (1C), cumulative
P5_PAR = ("\\claim{Removing the target name leaves mini near chance.}\n"
          "On supersession questions in the full obligation set, removing the target name and its nearest neighbours lowers mini from $0.86$ to $0.53$ and Haiku from $0.89$ to $0.68$, both reliably. (Appendix~\\ref{app:resp})\n\n")
P5_PTR_OLD = "that only guesses the question's category ($0.77$ and $0.75$). (Appendix~\\ref{app:counterfactual})\n"
P5_PTR_NEW = "that only guesses the question's category ($0.77$ and $0.75$). (Appendix~\\ref{app:counterfactual}; target-name ablation: Appendix~\\ref{app:resp})\n"
P5B_OLD = "The explicit intent test shows a further distinction among readers, bounded by the fixed cue list's performance."
P5B_NEW = "Told the intent rule, only the three stronger models apply it, and a fixed cue list matches the best of them."
P6A_OLD = "These comparisons use the first draw for every reader.\n"
P6B_OLD = ("When the rubric states that rule, Luna scores $0.96$, Sol $0.88$ and Opus $0.99$.\n"
           "When Sol fails, it often scores both questions high, leaving the rule unapplied. " + AP + "\n")
P6B_NEW = "When the rubric states that rule, Luna scores $0.96$, Sol $0.88$ and Opus $0.99$. " + AP + "\n"
P6C_OLD = ("Those models score the change question higher, consistent with the scored step asking whether stale content exists.\n"
           "The content remains in the store.\n")
P6C_NEW = "Those models score the change question higher, consistent with a scored step that asks whether stale content exists.\n"
P6D_OLD = ("Sol also separates expiry intents under the main-study rubric, scoring $0.64$.\n"
           "Across these tests, stating the rule lowers no model's score on its original questions beyond tolerance. " + AP + "\n")
P6D_NEW = "Sol also separates expiry intents under the main-study rubric, scoring $0.64$. " + AP + "\n"
P7_OLD = "width=0.41\\linewidth, height=5.0cm, xmin=-0.5, xmax=2.5, ymin=0.35, ymax=1.0,"
P7_NEW = "width=0.41\\linewidth, height=4.5cm, xmin=-0.5, xmax=2.5, ymin=0.35, ymax=1.0,"
P8_OLD = ("\\claim{List length and coverage inflate both metrics.}\n"
          "A reader that only knows whether the store covers the question scores $0.75$ pooled and $0.50$ matched.\n"
          "A lookup over meaningless tokens scores $0.60$ pooled and $0.65$ matched, because the \\pn{} version's list is one name longer and $24$ of the $88$ \\present{} lists are empty; the name lookup is a reliable $0.13$ above it on the matched metric.\n"
          "The sibling-name control is the comparison that removes both. " + AP + "\n")
P8_NEW = ("%% R131 close, payer 8 (2026-09-20): the paragraph in the author's two sentences (MERGED RULINGS 1C; the lead keeps its run-in form with the author's verb); 0.60 / 0.65 and 24 of 88 stay in tab:cf-emptiness and tab:cf-matched.\n"
          "\\claim{List length and coverage lift both metrics.}\n"
          "A reader that only knows whether the store covers the question scores $0.75$ pooled and $0.50$ matched.\n"
          "The name lookup stays a reliable $0.13$ above a lookup over meaningless tokens on the matched metric. " + AP + "\n")
B2_OLD = ("In these tests, what the store writes down mattered more than which reader read it.\n"
          "The two smaller models read the attribute names alone; Luna, Sol and Opus also read the counts.\n"
          "On the one state the default summary names, no model reliably outscores the lookup, with list length kept fixed or not.\n"
          "The three stronger models pull ahead of it through the counted states, and a lookup given one count feature catches them within triples.\n"
          "Models differ further when the rubric states the intent rule.\n"
          "Backend errors weaken the information supplied to every reader, while the retrieval fetch supplies much of the added reach.\n")
B2_NEW = ("%% R131 close, payer B2 (2026-09-20): the findings paragraph cut to its first sentence and the intent sentence (ABSTRACT SWAP B2); the deleted sentences' claims are in the bullets below and Section 5.\n"
          "In these tests, what the store writes down mattered more than which reader read it.\n"
          "Models differ further when the rubric states the intent rule.\n")
O1_ANCHOR = "At retrieval, the fetch keyed on the names reaches as far ungated as gated, at a budget trade-off.\n"
O1_NEW = (O1_ANCHOR + "%% R131 close, O1 (2026-09-20): landed only at slack +5 or better (CONSOLIDATED ADDITIONS O).\n"
          "None of the four backends we examined writes these names at the interfaces we evaluated. Whether a backend can maintain them at write time, and at what cost, is the open problem these results point to.\n")

PAYER_ORDER = ["5", "5b", "6", "7", "8", "B2"]


def apply_payers(b, payers):
    for k in payers:
        if k == "5":
            b = change("payer 5", "Section 5.1", b, P5_PAR, "", "the target-name paragraph out of the body (1C payer 5); E.10 tab:resp-l1 prints 0.8572 -> 0.5310 and 0.8897 -> 0.6759, both reliable")
            b = change("payer 5", "Section 5.1", b, P5_PTR_OLD, P5_PTR_NEW, "the pointer of at most six words in the adjacent paragraph (1C payer 5)")
        elif k == "5b":
            b = change("payer 5b", "Conclusion", b, P5B_OLD, P5B_NEW, "the author's sentence (CONSOLIDATED ADDITIONS P5b; 1C payer 5b)")
        elif k == "6":
            b = change("payer 6, P6a", "Section 5.3", b, P6A_OLD, "", "deleted; tab:cf-intent's caption already says the body reads the draw-1 column (P6a accepted as proposed, no caption addition)")
            b = change("payer 6, P6b", "Section 5.3", b, P6B_OLD, P6B_NEW, "deleted; tab:cf-intent's caption says 9 of Sol's 11 losses score both questions 0.96 or higher (P6b)")
            b = change("payer 6, P6c", "Section 5.3", b, P6C_OLD, P6C_NEW, "the author's sentence for two (P6c)")
            b = change("payer 6, P6d", "Section 5.3", b, P6D_OLD, P6D_NEW, "deleted; tab:cf-intent's caption prints the largest fall -0.0458 (P6d)")
        elif k == "7":
            b = change("payer 7", "Figure 3", b, P7_OLD, P7_NEW, "height 5.0cm -> 4.5cm (10 percent); width, markers, fonts unchanged; the Luna 0.8667 / Sol 0.8333 expiry markers do not overlap before or after (rendered check in the report)")
        elif k == "8":
            b = change("payer 8", "Section 5.2", b, P8_OLD, P8_NEW, "the list-length paragraph to two sentences after its lead (1C payer 8)")
        elif k == "B2":
            b = change("payer B2", "Section 1", b, B2_OLD, B2_NEW, "the findings paragraph cut (ABSTRACT SWAP B2); every deleted claim is in bullets 2 and 3 or Section 5")
        else:
            raise SystemExit(f"unknown payer {k}")
    return b


def main():
    check = "--check" in sys.argv
    payers = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--payers=")), "")
    payers = [x.strip() for x in payers.split(",") if x.strip()]
    payers = [k for k in PAYER_ORDER if k in payers]
    o1 = "--o1" in sys.argv
    b = rd(OUT_B)
    a = rd(OUT_A)
    assert "%% R131 " in b and "%% R131 close" not in b and "%% R131 close" not in a, "port_r131_close.py: run after port_r131.py (and not twice)"

    # B1: the abstract, whole
    i = a.index("\\begin{abstract}\n")
    j = a.index("\\end{abstract}\n") + len("\\end{abstract}\n")
    CHANGES.append(("B1", "Abstract", a[i:j], ABS_NEW, "the author's abstract, verbatim (ABSTRACT SWAP B1)"))
    a = a[:i] + ABS_NEW + a[j:]
    # L, A (Section 4, Limitations, the AI-use statement)
    b = change("L4", "Section 4", b, L4_OLD, L4_NEW, "'(open weights)' at the first mention of Kimi K3 (CONSOLIDATED ADDITIONS L4; the authors' assertion, FINAL RULINGS 4)")
    b = change("A1'", "Section 4", b, A1_OLD, A1_NEW, "the provenance sentences (MERGED RULINGS 2, FINAL RULINGS 1)")
    b = change("L1", "Limitations", b, L1_OLD, L1_NEW, "the author's two sentences (CONSOLIDATED ADDITIONS L1; 40 verified against the bank)")
    b = change("L2", "Limitations", b, L2_OLD, L2_NEW, "the author's sentence with 'completed only' (CONSOLIDATED ADDITIONS L2; FINAL RULINGS 4)")
    b = change("L3", "Limitations", b, L3_OLD, L3_NEW, "the sentence cut; C.2 prints the within-0.02 result and Luna's margin (CONSOLIDATED ADDITIONS L3)")
    b = change("A2'", "AI-use statement", b, A2_OLD, A2_NEW, "the author's statement (MERGED RULINGS 2; FINAL RULINGS 1)")
    b = change("A5", "AI-use statement", b, A5_OLD, A5_NEW, "the word 'preregistered,' dropped (FINAL RULINGS 6)")
    # 1A, 1B
    b = change("1A", "Table 1", b, TAB1_CAP_OLD, TAB1_CAP_NEW, "the caption's four-word note on the four-decimal difference sub-table (MERGED RULINGS 1A)")
    b = change("1B", "the builders box", b, BOX_OLD, BOX_NEW, "the all-states clause in the author's words (FINAL RULINGS 4)")
    # the payers
    b = apply_payers(b, payers)
    if o1:
        b = change("O1", "Conclusion", b, O1_ANCHOR, O1_NEW, "the two closing sentences (CONSOLIDATED ADDITIONS O1; slack +5 or better)")

    b, a = gates(b, a)

    assert "\u2014" not in b and "\u2014" not in a, "em dash"
    if check:
        print("port_r131_close.py --check: would write", OUT_B, OUT_A, "payers", payers, "o1", o1)
        return
    io.open(OUT_B, "w", encoding="utf-8", newline="\n").write(b)
    io.open(OUT_A, "w", encoding="utf-8", newline="\n").write(a)
    print(f"-> {OUT_B} ({len(b.splitlines())} lines); {OUT_A}; payers applied: {payers or 'none'}; O1 {'landed' if o1 else 'not landed'}")
    print("gate-driven wording changes:")
    for rule, sec, old, new in GATE_CHANGES:
        print(f"  [{rule}] {sec}\n     - {old[:160]}\n     + {new[:160]}")


# The gate-driven wording changes on the author's texts, added after the first gate run (reviews/v22/gates_r131_close_a.txt); each the smallest change
# satisfying its rule, listed old beside new in REPORT_R131_CLOSE.md and CLAIMS.md. The abstract ('a') is never a target (B4).
GATES = [
]


def gates(b, a):
    for target, rule, section, old, new in GATES:
        if old not in (b if target == "b" else a):
            continue   # a payer removed the sentence
        if target == "b":
            b = gate(rule, section, b, old, new)
        else:
            raise AssertionError("the abstract is hand-tuned (B4); report the trip instead")
    return b, a


if __name__ == "__main__":
    main()
