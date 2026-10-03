# -*- coding: utf-8 -*-
"""wp_phase1.py -- Phase 1 of the writing pass on paper_v18 (paper_v18_writing_prompt.md section 16: structure and cuts; items 1, 2, 3, 7,
18, 24, 36, 49-55, 87, 90), 2026-09-15, applied to reviews/v18/src/body_v18.tex and reviews/v18/src/appendix_v18.tex.

Every edit is a line-range replacement on the source as it stood after Phase 0 (commit 78d8f8b), asserted by the first and last line
of the range, applied from the bottom of each file upward so the line numbers of the pass file stay valid. No number changes: every
value that leaves the body stands in a table, an appendix or a ledger named in the comment beside the edit (reviews/v18/NUMBER_MOVES.md
carries the reasons); two-decimal forms in the six body tables are ROUND_HALF_UP of the recorded four-decimal values (the rule
numeric_diff applies), and every (printed, source) pair is written to reviews/NUMBERS_WP.md section 1 for trace_scan.
Usage: python reviews/v18/tools/wp_phase1.py [--check]   (--check applies to copies and prints the diff statistics only)
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
APPX = SRC / "appendix_v18.tex"
LEDGER = ROOT / "reviews" / "NUMBERS_WP.md"

PRINTED: list[tuple[str, str, str]] = []   # (printed, source, key)


def r2(s: str, key: str) -> str:
    """ROUND_HALF_UP of a four-decimal string to two decimals, keeping an explicit sign; records the pair for the ledger."""
    d = Decimal(s)
    q = d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    out = (f"{q:+.2f}" if s[0] in "+-" else f"{q:.2f}")
    if out.replace("+", "") != s.replace("+", ""):
        PRINTED.append((out, s, key))
    return out


def iv2(s: str, key: str) -> str:
    """'[+0.1494,+0.2846]' -> '[+0.15,+0.28]'"""
    m = re.fullmatch(r"\[([+-]?\d\.\d{4}),([+-]?\d\.\d{4})\]", s)
    assert m, s
    return f"[{r2(m.group(1), key)},{r2(m.group(2), key)}]"


def read(p):
    return io.open(p, encoding="utf-8").read().replace("\r\n", "\n").split("\n")


def write(p, lines):
    io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))


class Edits:
    def __init__(self, lines):
        self.lines = lines
        self.ops = []   # (start, end, new_lines, first, last) 1-indexed inclusive

    def replace(self, start, end, new, first, last):
        self.ops.append((start, end, new, first, last))

    def apply(self):
        for start, end, new, first, last in sorted(self.ops, key=lambda o: -o[0]):
            a, b = self.lines[start - 1], self.lines[end - 1]
            assert a.startswith(first), (start, a[:80], first)
            assert b.startswith(last), (end, b[:80], last)
            self.lines[start - 1:end] = new
        return self.lines


# ----------------------------------------------------------------------------------------------------------------------------------
# the six body tables, two decimals (items 50, 51, 53, 54, 55; item 45's table half done here because each table is rewritten once)
# ----------------------------------------------------------------------------------------------------------------------------------

def table1():
    K = "AUX-CF2-*-V2/-V3 (Table 1)"
    rows = [
        ("GPT-4.1 mini, sup.\\ only", "0.7167", "0.8308", "0.5283", "0.5489", "[0.6663,0.7649]", "AUX-CF2-MINI-V2 indexed persona-clustered"),
        ("GPT-4.1 mini, all three", "0.7967", "0.8444", "0.8725", "0.5869", "[0.7438,0.8478]", "AUX-CF2-MINI-V3 indexed persona-clustered"),
        ("Haiku 4.5, sup.\\ only", "0.7566", "0.8876", "0.5433", "0.5794", "[0.7102,0.8035]", "AUX-CF2-H45-V2 indexed persona-clustered"),
        ("Haiku 4.5, all three", "0.8773", "0.8852", "0.9042", "0.8269", "[0.8362,0.9124]", "AUX-CF2-H45-V3 indexed persona-clustered"),
        ("Opus 5, sup.\\ only", "0.8405", "0.9325", "0.5872", "0.6150", "[0.7996,0.8817]", "AUX-CF2-OP5-V2 indexed persona-clustered"),
        ("Opus 5, all three", "0.9079", "0.9319", "0.8100", "0.9267", "[0.8769,0.9377]", "AUX-CF2-OP5-V3 indexed persona-clustered"),
    ]
    nomodel = [
        ("Name lookup, sup.\\ only", "0.7663", "0.9223", "0.5000", "0.5000", "[0.7226,0.8051]", "AUX-CF2-NB6-V2"),
        ("All-states lookup, all three", "0.8756", "0.8995", "0.7975", "0.8711", "[0.8391,0.9111]", "AUX-CF2-ALLSTATES-V3"),
        ("Category-guessing count reader, sup.\\ only", "0.6623", "0.6573", "0.6669", "0.6872", "[0.6273,0.6991]", "AUX-R110-A1-CR (CR-nb1)"),
        ("Category-aware count reader, sup.\\ only", "0.6043", "0.5000", "0.7306", "0.7778", "[0.5753,0.6389]", "AUX-R110-A1-CR (CR-oracle-a)"),
    ]

    def row(r):
        lab, w, s, rt, e, iv, key = r
        iv = iv2(iv, key)
        return f"{lab} & ${r2(w, key)}$ & ${r2(s, key)}$ & ${r2(rt, key)}$ & ${r2(e, key)}$ & ${iv}$ \\\\"

    out = [
        "\\begin{table}[h]",
        "%% Writing pass Phase 1 (2026-09-15), item 50 with its addendum: two decimals; one quantity per column, the profile-grouped interval of the AUROC on every row",
        "%% (the model rows' AUX-CF2-*-V2 / -V3 'indexed persona-clustered' intervals, the gain interval shifted by the blind 0.5000; no item-level AUROC interval is recorded,",
        "%% so the item-level intervals of the gain stay in Appendix C.2, tab:counterfactual); the count readers AUX-R110-A1-CR; the readers with no model under a rule.",
        "%% The per-state columns stay until the per-state figure of item 30 lands (Phase 3). 0.92 lives in this table and in C.2 only (P4).",
        "\\caption{Obligation AUROC on the counterfactual set ($n=444$; positives $88$ supersession, $30$ retraction, $30$ expiry), whole set and per state. Blind NOK is $0.50$ by construction, so each AUROC is also a gain; the interval is the profile-grouped interval of the whole-set AUROC (item-level: Appendix~\\ref{app:counterfactual}).}",
        "\\label{tab:cf-main}",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{3pt}",
        "\\begin{tabular}{@{}lrrrrl@{}}",
        "\\toprule",
        "Reader, summary & Whole & Sup. & Retr. & Exp. & profile interval \\\\",
        "\\midrule",
    ] + [row(r) for r in rows] + [
        "\\midrule",
        "\\multicolumn{6}{@{}l}{\\textit{Readers with no model in them}}\\\\",
    ] + [row(r) for r in nomodel] + [
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
    ]
    return out


def table2():
    K = "AUX-RESP-RETRIEVED / -HYBRID / -A1-BELIEVED (Table 2)"
    return [
        "\\begin{table}[h]",
        "%% Writing pass Phase 1 (2026-09-15), items 51 and 90: the three GPT-4.1 mini rows with the comparison in the row, two decimals; the four readers with no model in",
        "%% them under the store's own tags moved to Appendix E.10 (tab:routes-full) with the sign fix of item 36. AUX-RESP-RETRIEVED (0.6851), AUX-RESP-HYBRID (0.8303),",
        "%% AUX-RESP-A1-BELIEVED (0.8144), AUX-E1R-TRUE-NOK (0.7339).",
        "\\caption{Obligation AUROC of GPT-4.1 mini on the tagged view, on the full obligation set ($661$ questions, $104$ obligations). $\\Delta$ is the monitor minus the comparison named in its row, with both intervals; Haiku 4.5 and the no-model readers are in Appendix~\\ref{app:resp}.}",
        "\\label{tab:routes}",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{3pt}",
        "\\begin{tabular}{@{}lrlll@{}}",
        "\\toprule",
        "Monitor, tag source & AUROC & $\\Delta$ (against) & item interval & profile interval \\\\",
        "\\midrule",
        f"Summary alone & ${r2('0.7339', K)}$ & & & \\\\",
        f"Tagged view, ground-truth tags & ${r2('0.6851', K)}$ & ${r2('-0.0488', K)}$ (the summary alone) & ${iv2('[-0.1274,+0.0285]', K)}$ & ${iv2('[-0.1454,+0.0389]', K)}$ \\\\",
        f"Summary plus tagged view, ground-truth tags & ${r2('0.8303', K)}$ & ${r2('+0.0964', K)}$ (the summary alone) & ${iv2('[+0.0415,+0.1554]', K)}$ & ${iv2('[+0.0227,+0.1635]', K)}$ \\\\",
        f"Tagged view, the store's own tags & ${r2('0.8144', K)}$ & ${r2('+0.1292', K)}$ (the view under ground-truth tags) & ${iv2('[+0.0666,+0.1826]', K)}$ & ${iv2('[+0.0606,+0.2060]', K)}$ \\\\",
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
    ]


def table3():
    return [
        "\\begin{table}[h]",
        "%% Writing pass Phase 1 (2026-09-15), items 52 and 90: three rows, one sentence per cell; the Conflate row's content is in Appendix E.9 as prose. AUX-SIDE-S2-CENSUS, AUX-BELIEVED-MEM0, the R86 census (A-MEM).",
        "\\caption{A census of what each backend writes about itself, scored against the ground-truth manifests: counts with no sampling interval. The store that conflates retraction with supersession is described in Appendix~\\ref{app:believed-census}.}",
        "\\label{tab:believed}",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{2pt}",
        "\\begin{tabular}{@{}p{0.12\\linewidth}p{0.10\\linewidth}p{0.70\\linewidth}@{}}",
        "\\toprule",
        "Backend & Mode & Census measurement \\\\",
        "\\midrule",
        "FR-Bank & Overstate & Of $18{,}936$ entries and $109$ events, marks $5{,}968$ entries stale against ${\\sim}102$ in ground truth (about $58\\times$) and retains an active obsolete assertion after $72\\%$ of supersession events, at the stored-versus-obsolete matching threshold of the census. \\\\",
        "Mem0 & Erase & Of $10{,}074$ entries, $12.7\\%$ expose \\texttt{updated\\_at} and nothing else, because \\texttt{UPDATE} overwrites the record it exposes (version 1.0.5) and ingestion is silently lossy. \\\\",
        "A-MEM & Invent & All $23{,}186$ link references across $11{,}319$ notes resolve to $0$ note identifiers, on the $40$ scored personas. \\\\",
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
    ]


def table4():
    K = "AUX-E1R-*, AUX-BH-* (Table 4)"
    return [
        "\\begin{table}[h]",
        "%% Writing pass Phase 1 (2026-09-15), item 53: the columns renamed (item 34's terms), two decimals, the caption to two lines, the retention intervals in the note.",
        "%% AUX-E1R-TRUE-NOK (0.7339), AUX-E1R-BELIEVED-NOK (0.5959), AUX-SIDE-S2-MINI (0.6513); AUX-R74-X4-H45-NOK (0.8210), AUX-BH-H45-15 (0.7069), AUX-BH-H45-LIFTED (0.7364);",
        "%% AUX-E1R-NB6 (0.7484 truthful; 0.5858 capped), AUX-BH-LOOKUP-LIFTED (0.6588); AUX-BH-RETENTION-15 (0.7190 [0.6214, 0.8497] / [0.5935, 0.8603]), -LIFTED (0.7916 [0.6838, 0.9243] / [0.6342, 0.9425]).",
        "\\caption{Obligation AUROC on the full obligation set ($661$ questions, $104$ obligations) under the ground-truth summary and under FR-Bank's store-written summary, rendered with the fifteen-name cap and with the cap lifted; retention is Haiku 4.5's store-written gain as a fraction of its ground-truth gain.}",
        "\\label{tab:levels}",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{3pt}",
        "\\begin{tabular}{@{}lrrr@{}}",
        "\\toprule",
        "Reader & Ground-truth summary & Store-written, capped & Store-written, cap lifted \\\\",
        "\\midrule",
        f"GPT-4.1 mini & ${r2('0.7339', K)}$ & ${r2('0.5959', K)}$ & ${r2('0.6513', K)}$ \\\\",
        f"Haiku 4.5 & ${r2('0.8210', K)}$ & ${r2('0.7069', K)}$ & ${r2('0.7364', K)}$ \\\\",
        f"\\quad retention$^{{a}}$ & & ${r2('0.7190', K)}$ & ${r2('0.7916', K)}$ \\\\",
        f"Name lookup & ${r2('0.7484', K)}$ & ${r2('0.5858', K)}$ & ${r2('0.6588', K)}$ \\\\",
        "\\bottomrule",
        "\\end{tabular}",
        "\\par\\smallskip",
        "\\begin{minipage}{0.97\\linewidth}\\scriptsize",
        "$^{a}$The ratio of the paired resampled differences, with the item-level and the profile-grouped interval: capped $" + iv2('[0.6214,0.8497]', K) + "$ and $" + iv2('[0.5935,0.8603]', K) + "$, lifted $" + iv2('[0.6838,0.9243]', K) + "$ and $" + iv2('[0.6342,0.9425]', K) + "$. Reported for Haiku 4.5 only, because GPT-4.1 mini's blind score is one value on $604$ of the $661$ questions and the lookup has no blind score (Appendix~\\ref{app:believed-census}).",
        "\\end{minipage}",
        "\\end{table}",
    ]


def table5():
    K = "AUX-E1R-*, AUX-R74-X4-* (Table 5)"
    fok = [
        ("FR-Bank hard tier", "307", "35", "0.4966", "0.7003", "+0.2037", "[+0.0935,+0.3191]", "[+0.1259,+0.2767]"),
        ("Mem0", "238", "94", "0.5746", "0.4777", "-0.0969", "[-0.1686,-0.0250]", "[-0.1638,-0.0286]"),
        ("A-MEM", "284", "126", "0.5591", "0.4526", "-0.1065", "[-0.1726,-0.0403]", "[-0.1654,-0.0446]"),
    ]
    nok = [
        ("Haiku 4.5", "661", "104", "0.4150", "0.8210", "+0.4060", "[+0.3283,+0.4791]", "[+0.3063,+0.5026]"),
        ("Opus 5", "661", "104", "0.6429", "0.8327", "+0.1898", "[+0.1437,+0.2411]", "[+0.1241,+0.2523]"),
        ("GPT-5.6 Luna", "661", "104", "0.4495", "0.8182", "+0.3687", "[+0.2932,+0.4358]", "[+0.2656,+0.4666]"),
    ]

    def row(r):
        lab, n, p, b, i, d, a, c = r
        return f"{lab} & ${n}$ / ${p}$ & ${r2(b, K)}$ & ${r2(i, K)}$ & ${r2(d, K)}$ & ${iv2(a, K)}$ & ${iv2(c, K)}$ \\\\"

    return [
        "\\begin{table}[h]",
        "%% Writing pass Phase 1 (2026-09-15), item 54: two ruled panels (FOK by backend; NOK by model), 'Indexed (ground-truth summary)', two decimals. Values as in v18 (AUX-E1R-*; AUX-R74-X4-*).",
        "\\caption{Blind and indexed judgments with the paired gain and both intervals: coverage by backend for GPT-4.1 mini (positives non-\\absent{}) and the obligation judgment on FR-Bank by model (positives \\pn{}). On the hard tier every coverage positive is an obligation, so that FOK row is the NOK row relabeled.}",
        "\\label{tab:e1}",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{2pt}",
        "\\begin{tabular}{@{}lrrrrll@{}}",
        "\\toprule",
        "\\multicolumn{7}{@{}l}{\\textbf{FOK by backend, GPT-4.1 mini}}\\\\",
        "Backend & $n$ / pos. & Blind & \\hd{Indexed}{(ground-truth summary)} & $\\Delta$ & item interval & profile interval \\\\",
        "\\midrule",
    ] + [row(r) for r in fok] + [
        "\\midrule",
        f"\\multicolumn{{7}}{{@{{}}l}}{{\\textbf{{NOK by model, FR-Bank}}; the name lookup scores ${r2('0.7484', K)}$ on the same $661$ questions}}\\\\",
        "Model & $n$ / pos. & Blind & \\hd{Indexed}{(ground-truth summary)} & $\\Delta$ & item interval & profile interval \\\\",
        "\\midrule",
    ] + [row(r) for r in nok] + [
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
    ]


def table6():
    K = "AUX-DS-AUDIT-RATES, AUX-DS-A7-REPORTED (Table 6)"
    rows = [
        ("Top-5 retrieval", "54", "9", "8", "42", "0.1905", "46"),
        ("Model rule", "85", "9", "8", "62", "0.1290", "44"),
        ("Lookup rule", "85", "7", "6", "58", "0.1034", "40"),
        ("Model rule, all states named and scored", "89", "12", "11", "65", "0.1692", "44"),
        ("Literal lookup rule (descriptive)", "94", "14", "13", "82", "0.1585", "46"),
        ("Oracle", "99", "17", "16", "85", "0.1882", "46"),
    ]
    return [
        "\\begin{table}[h]",
        "%% Writing pass Phase 1 (2026-09-15), item 55: self-explanatory headers, the 0.80-threshold note below the table, two decimals; values as in v18 (AUX-DS-AUDIT-RATES: 8/42, 8/62, 6/58, 13/82, 16/85; AUX-DS-A7-REPORTED 11/65; AUX-R104-REACH; AUX-DS-A4-*).",
        "\\caption{The downstream policies for GPT-4.1 mini on the full obligation set: forbidding records put in view, stale answers at the detector's $0.50$ threshold, and correct answers on the licensed items. The stale rate holds under every gated policy until the store's untagged duplicates are tagged (Table~\\ref{tab:ds-a5}, Appendix~\\ref{app:resp}).}",
        "\\label{tab:ds-body}",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{3pt}",
        "\\begin{tabular}{@{}lrrlr@{}}",
        "\\toprule",
        "Policy & \\hd{Forbidding records}{in view (of $104$)} & \\hd{Stale answers}{(of $104$)} & \\hdl{Stale rate over the}{reached, scorable} & \\hd{Correct}{(of $174$)} \\\\",
        "\\midrule",
    ] + [f"{lab} & ${a}$ & ${b}$ & ${c}$ of ${d}$, ${r2(rate, K)}$ & ${e}$ \\\\" for lab, a, b, c, d, rate, e in rows] + [
        "\\bottomrule",
        "\\end{tabular}",
        "\\par\\smallskip",
        "\\begin{minipage}{0.97\\linewidth}\\scriptsize",
        "The detector's $0.80$ threshold gives zero stale answers under every policy. The items on which each rule fires, the reach as a rate, the Wilson interval of the stale rate, the mean view size, tagged records and coverage are in Table~\\ref{tab:ds-body-lower} (Appendix~\\ref{app:resp}).",
        "\\end{minipage}",
        "\\end{table}",
    ]


def setup_table():
    return [
        "\\begin{table}[h]",
        "%% Writing pass Phase 1 (2026-09-15), item 24: Table tab:populations and Table tab:runs (Appendix A) merged and trimmed to eight rows. Sizes and positives as in tab:populations;",
        "%% the models and calls per question from tab:runs and, for the expiry extension, r82_counterfactual/cf3/NUMBERS_CF3.md (AUX-CF3-PROJECTION: mini 140 calls, Haiku 4.5 700, Opus 5 140),",
        "%% for the authorship-matched set the recorded rows (r74/x5/rows_MINI.jsonl: three draws per arm; rows_OP5.jsonl and r74/x6/rows_H45.jsonl: five; reviews/NUMBERS_WP.md AUX-WP-X5-DRAWS).",
        "%% The note carries the score-resolution paragraph (items 1 and 29; AUX-R110-A3, k3_noise 46 of 50).",
        "\\caption{The populations, with their sizes and positives and the models that ran on each (calls per question in parentheses). Every question set was generated from human-written manifests, which are the ground truth every label is scored against; Appendix~\\ref{app:laddertable} defines each population in full and records the runs.}",
        "\\label{tab:setup}",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{3pt}",
        "\\begin{tabular}{@{}p{0.19\\linewidth}p{0.45\\linewidth}p{0.32\\linewidth}@{}}",
        "\\toprule",
        "Population & $n$ (positives) & Models (calls per question) \\\\",
        "\\midrule",
        "the counterfactual set & $444$ items: $148$ questions asked of three versions of one store that differ in one attribute ($148$ obligations: $88$ supersession, $30$ retraction, $30$ expiry) & GPT-4.1 mini (1), Haiku 4.5 (5), Opus 5 (5) \\\\",
        "the expiry extension & $42$ items: the $14$ eligible expiry pairs the first draw left undrawn, built by the same construction ($44$ expiry pairs pooled with the set's $30$) & GPT-4.1 mini (1), Haiku 4.5 (5), Opus 5 (1) \\\\",
        "the full obligation set & $661$ questions ($104$ obligations: $63$ supersession, $26$ retraction, $15$ expiry): the hard tier's $307$ and the easy tier's $354$ together & GPT-4.1 mini (1); Haiku 4.5, Opus 5 and GPT-5.6 Luna (5); GPT-5.6 Sol and Kimi K3 stopped at the budget \\\\",
        "the coverage set & $307$ questions ($35$ non-\\absent{}): the hard tier, on which every coverage positive is an obligation & the same \\\\",
        "the easy tier & $354$ questions ($243$ non-\\absent{}, $69$ obligations): a whole category removed for absence & the same \\\\",
        "the cross-model set & $84$ questions ($54$ FOK-positive, $40$ obligations): the same questions asked of every model & all six; GPT-4.1 mini (1), the others (5) \\\\",
        "the authorship-matched set & $36$ questions ($12$ obligations): every question rewritten in one voice & GPT-4.1 mini (3), Haiku 4.5 (5), Opus 5 (5) \\\\",
        "the downstream items & $174$ licensed items and $89$ scorable obligations: the items the answer stage can answer and the obligations its detector can score & GPT-4.1 mini and Haiku 4.5 as answerers (1) \\\\",
        "\\bottomrule",
        "\\end{tabular}",
        "\\par\\smallskip",
        "\\begin{minipage}{0.97\\linewidth}\\scriptsize",
        "GPT-4.1 mini is scored from one call in the main study and every other model from five, and the finer resolution of the averaged scores is not their margin: Opus 5's first call alone keeps its margin over the lookup on the counterfactual set, and GPT-4.1 mini's repeated calls return identical scores on $46$ of $50$ questions (Appendix~\\ref{app:counterfactual}).",
        "\\end{minipage}",
        "\\end{table}",
    ]


# ----------------------------------------------------------------------------------------------------------------------------------
# the body edits (line numbers of body_v18.tex at 78d8f8b)
# ----------------------------------------------------------------------------------------------------------------------------------

def body_edits(E: Edits):
    # 1. the box: the write-path sentence points at the downstream section (item 2)
    E.replace(634, 634, [
        "Fix the write path: tag the duplicates the store keeps active, because that removes most of the stale answers and no fetch policy does (Section~\\ref{sec:downstream}).",
    ], "Fix the write path: tag the duplicates", "Fix the write path: tag the duplicates")

    # 2. Limitations to about 130 words (items 47, 83, 85, 90); the pinned U5 sentence stays; the own-tags disclosure kept in one sentence
    E.replace(603, 616, [
        "%% Writing pass Phase 1 (2026-09-15), item 90: Limitations cut to the five the author keeps (synthetic stores, one lifecycle backend, the counted-state cells, one closed family,",
        "%% the untested name pool) plus the pinned U5 sentence and the own-tags disclosure (A5_EDITS.md item 1) in one sentence; item 83's FR-Bank sentence; item 85's link to C.2.",
        "%% Dropped: the sixty-percent line (item 47; its provenance is in Appendix E.9), the FOK-deleted sentence (item 47; the measurement stands in Section 8), the authorship-matched",
        "%% sentence (Appendix C.1 carries the set).",
        "The evidence comes from synthetic stores and one lifecycle backend.",
        "The stores are synthetic because temporal ground truth is unobservable without controlled construction, and NOK is measured on one lifecycle store, FR-Bank, the only tested backend that retains superseded content \\citep{fr}.",
        "% C090 (U5, byte-identical)",
        "The structureless-store inversion is measured across scales, but its below-chance mechanism remains unresolved.",
        "The counted-state groups are small: $30$ retraction and $30$ expiry pairs on the counterfactual set, $44$ expiry with the extension draw of Appendix~\\ref{app:counterfactual}, and $26$ retraction and $15$ expiry obligations on the full obligation set, whose counted-state rows give only a direction.",
        "The lookup is untested beyond the store's own name pool, a mean of $99$ names, and the paraphrase check covers one rewording per question.",
        "One closed model family supplies the primary capability comparison, and two runs stopped at the budget on the full populations.",
        "The tagged route under the store's own tags is descriptive, with no prediction fixed in advance for its rise, which is the tags' reach of the forbidding records rather than their density (Section~\\ref{sec:routes}).",
    ], "The evidence comes from synthetic stores", "FOK's inability to distinguish")

    # 3. the depth and composite paragraphs to the sentences item 42 allows (items 1, 42); the detector sentence stays
    E.replace(586, 598, [
        "%% Writing pass Phase 1 (2026-09-15), items 1 and 42: the depth and composite paragraphs cut; the mean depths per item class (AUX-DS-A6-INVIEW 9.45 / 7.75) and the composite's",
        "%% counts (+18 of 661, +2; AUX-DS-A7-COMPOSITE-ANSWERED-DIFF) stand in Tables tab:ds-a6 and tab:ds-a7.",
        "The coverage judgment sets the depth of the view, and the extra lines land on the licensed items.",
        "For Haiku~4.5 the expanded view matches a ten-line view's correct count at $8.3$ lines, $+0.04$ over a flat view of equal cost with both intervals excluding zero.",
        "For GPT-4.1 mini the difference is $+0.02$ with intervals including zero (Table~\\ref{tab:ds-a6}, Appendix~\\ref{app:resp}).",
        "% AUX-DS-A6-MATCHED-H45 (+0.0369 [+0.0156, +0.0623] / [+0.0136, +0.0639]); AUX-DS-A6-MATCHED-MINI (+0.0197 [-0.0106, +0.0517] / [-0.0161, +0.0575]); AUX-DS-A6-POP (8.29)",
        "",
        "A composite that scores each policy on all three jobs at once rises under the gated fetch for GPT-4.1 mini and stays level for Haiku 4.5.",
        "It counts a licensed item answered correctly, an obligation reached and reported, and an absent item abstained on; under the model rule it rises by $+0.03$ against retrieval alone for GPT-4.1 mini with both intervals excluding zero, and for Haiku 4.5 by a rate whose intervals include zero (Table~\\ref{tab:ds-a7}, Appendix~\\ref{app:resp}).",
        "% AUX-DS-A7-COMPOSITE-ANSWERED-DIFF (MINI +18 of 661, +0.0272 [+0.0121, +0.0439] / [+0.0113, +0.0443]; H45 +2, +0.0030 [-0.0121, +0.0182] / [-0.0132, +0.0191]); the oracle excluded (D-DS-A7-1)",
    ], "%% R110: the depth link", "% AUX-DS-A7-COMPOSITE-ANSWERED (A4-header MODEL")

    # 4. the header paragraph to two sentences (item 42)
    E.replace(576, 578, [
        "Correct answers are bounded by the view, which holds the licensed record for $65$ of the $174$ items, and by whether the prompt binds the entries to the person asking.",
        "A header naming the persona and the date raises in-view correct answers from $37$ to $48$ for GPT-4.1 mini and from $38$ to $59$ for Haiku 4.5, both intervals above zero (Appendix~\\ref{app:resp}).",
    ], "Correct answers are bounded by the view", "A header naming the persona and the date")

    # 5. Section 9 (item 2): the downstream experiment as its own section, with Table 6 (item 55)
    E.replace(541, 562, [
        "\\section{Acting on the judgment}\\label{sec:downstream}",
        "",
        "%% Writing pass Phase 1 (2026-09-15), item 2: the downstream experiment split out of the old Section 8 as Section 9; the opener from the old section's first paragraph.",
        "Acting on the judgment changes the answer stage one link at a time.",
        "The links are reach, the tags, the store's untagged duplicates, their repair, and the depth the coverage judgment buys.",
        "",
    ] + table6(), "\\subsection*{Acting on the judgment}", "\\end{table}")

    # 6-7. Section 8 (item 2): the replication and the coverage judgment; Table 5 in two panels (item 54)
    E.replace(503, 532, [
        "\\section{Replication across models and the coverage judgment}\\label{sec:populations}\\label{sec:calibration}\\label{sec:coverage}\\label{sec:discrimination}\\label{sec:calibration-secondary}\\label{sec:ladder}",
        "",
        "%% Writing pass Phase 1 (2026-09-15), item 2: the old Section 8 split; this section keeps the replication and the coverage result.",
        "The obligation gain replicates across models, and the coverage margin lives on ordinary records.",
        "Every paired obligation gain excludes zero where the blind score varies (Table~\\ref{tab:e1}), and on the cross-model set the five models with a varying blind score gain $+0.15$ to $+0.45$ (Appendix~\\ref{app:laddertable}).",
        "On the full obligation set the lookup scores $0.75$ against the smallest model's $0.73$, inside tolerance, and the three larger models sit $+0.07$ to $+0.08$ above it with item-level intervals excluding zero and profile-grouped intervals including it (Appendix~\\ref{app:baselines}).",
        "",
    ] + table5(), "\\section{Six models, coverage, and acting on the judgment}", "\\end{table}")

    # 8. the inversion paragraph to four sentences with the pointer (item 1; the 35-word rule of section 15 splits the author's third sentence); U1 and the compression reading move to E.7
    E.replace(495, 501, [
        "%% Writing pass Phase 1 (2026-09-15), item 1: the structureless-store paragraph cut; the compression reading and the U1 disclosure stand verbatim in Appendix E.7 (pinned once).",
        "On the two structureless stores a summary that names what they hold restores coverage, and the summary they can write loses it at every scale.",
        "A name-bearing summary rebuilt from ground truth restores coverage from $0.45$ to $0.90$ on A-MEM and from $0.48$ to $0.88$ on Mem0, so the loss belongs to the summary these stores write.",
        "Under that summary GPT-4.1 mini loses $0.10$ on Mem0 and $0.11$ on A-MEM, and on the pooled $66$ questions of both stores GPT-5.6 Luna loses $0.34$ and GPT-5.6 Sol $0.10$, every interval excluding zero.",
        "The loss is compression of the indexed score toward one low value, and what triggers it is unresolved (Appendix~\\ref{app:inversion}).",
    ], "On the two structureless stores a summary", "What triggers the compression is unresolved")

    # 9. the own-name split paragraph to four sentences (item 90): the split, the two Haiku numbers, the floor, the lookup's n = 10 interval
    E.replace(483, 493, [
        "%% Writing pass Phase 1 (2026-09-15), item 90: the own-name split in four sentences (AUX-BH-SPLIT: 0.8658 / 0.8855 on 53; 0.6839 on 10; lookup 0.7593 / 0.7969 [0.6722, 0.8992]; AUX-RESP-A1-H45-OWN 0.6882);",
        "%% the capped halves (24 / 39; 0.6933; lookup 0.7292 / 0.6146), Haiku minus the lookup (+0.1065) and the contamination sentences (AUX-PAD-C-*) stand in Table tab:bh-split and Appendix C.2.",
        "Where the store still writes the item's own name Haiku 4.5 reads it at its ground-truth level, and where it does not the model falls to the floor the own-name ablation found.",
        "Haiku 4.5 reads $0.87$ against $0.89$ under the ground-truth summary on the $53$ of the $63$ supersession obligations whose name survives under the lifted rendering, and $0.68$ on the $10$ whose name is gone.",
        "That floor is the own-name ablation's, $0.69$ on the whole population after the item's own name is removed (Section~\\ref{sec:counterfactual}).",
        "The lookup on the same halves reads $0.76$ where the name is present and $0.80$ where it is absent, on $10$ items with item interval $[0.67,0.90]$ (Table~\\ref{tab:bh-split}, Appendix~\\ref{app:believed-census}).",
    ], "%% R110: the own-name split", "% AUX-PAD-C-LOOKUP-EMB, -LOOKUP-LEX, -MINI, -H45")

    # 10. Table 4 (item 53)
    E.replace(456, 476, table4(), "\\begin{table}[h]", "\\end{table}")

    # 11. Table 3 (items 52, 90)
    E.replace(436, 454, table3(), "\\begin{table}[h]", "\\end{table}")

    # 12. the own-name paragraph leaves Section 6 for Section 5 (item 87)
    E.replace(420, 424, [""], "", "% AUX-RESP-L1-MINI (-0.3262), AUX-RESP-A1-H45-OWN")

    # 13. the pointer to the moved rows (item 90)
    E.replace(415, 415, [
        "A count of tagged lines reads the obligation at $0.62$ under either source, against the monitor's $0.81$ under the marks, and the tagged-name lookup at $0.65$, so the monitor reads more than density or name match (the four readers with no model in them are in Table~\\ref{tab:routes-full}, Appendix~\\ref{app:resp}).",
    ], "A count of tagged lines reads the obligation", "A count of tagged lines reads the obligation")

    # 14. Table 2 (items 36, 51, 90)
    E.replace(381, 401, table2(), "\\begin{table}[h]", "\\end{table}")

    # 15. the list-length paragraph to two sentences (item 90); the padding figures stand in Table tab:pad, the pool sentence moves to C.2
    E.replace(363, 371, [
        "%% Writing pass Phase 1 (2026-09-15), item 90: the list-length paragraph to two sentences; the padding curve (AUX-PAD-*, Table tab:pad), the store's own pool (AUX-R110-A4, moved to C.2) and the contamination figures (AUX-PAD-C-*) stand in Appendix C.2.",
        "The lookup works because the list is short and clean.",
        "As the list grows or fills with wrong names, the lookup and the models fall together (Appendix~\\ref{app:counterfactual}).",
    ], "%% R110: list length and wrong names", "% AUX-PAD-C-LOOKUP-EMB, -MINI, -H45")

    # 16. the 44 expiry pairs linked to C.2 (item 85)
    E.replace(361, 361, [
        "The counted-state evidence rests on $30$ retraction and $44$ expiry pairs, the $30$ plus the $14$ of the descriptive extension draw in Appendix~\\ref{app:counterfactual}, and on the full obligation set ($661$ questions) the counted-state rows give only a direction (Section~\\ref{sec:populations}).",
    ], "The counted-state evidence rests on", "The counted-state evidence rests on")

    # 17. the own-name paragraph enters Section 5 in three sentences (items 87, 90), after the supersession paragraph
    E.replace(347, 347, [
        "",
        "%% Writing pass Phase 1 (2026-09-15), items 87 and 90: the own-name ablation paragraph from Section 6, in three sentences (AUX-RESP-L1-MINI: 0.8572 to 0.5310, -0.3262; AUX-RESP-A1-H45-OWN: 0.8897 to 0.6759, -0.2139; whole 0.6882).",
        "The summary route rests on names, because removing them removes the judgment.",
        "Taking the target's own name and its nearest neighbours out of the superseded-names list drops GPT-4.1 mini's supersession judgment from $0.86$ to $0.53$ on the full obligation set ($63$ supersession obligations), with both intervals excluding zero.",
        "The same edit drops Haiku 4.5's from $0.89$ to $0.68$ with both intervals excluding zero, while Haiku 4.5 keeps $0.69$ on the whole population (Appendix~\\ref{app:resp}).",
        "",
    ], "", "")

    # 18. Table 1 (item 50 with its addendum)
    E.replace(313, 341, table1(), "\\begin{table}[h]", "\\end{table}")

    # 19-20. Section 4: the populations as a table with the score-resolution note (items 1, 18, 24, 29, 90)
    E.replace(269, 286, [
        "%% Writing pass Phase 1 (2026-09-15): the two population paragraphs replaced by Table tab:setup (item 24); the score-resolution paragraph is its note (items 1, 29); the Graphiti",
        "%% aside is Appendix E.9's fourth-backend paragraph and the 5% provenance sentence moved there (item 90); the mask pass rate moved here from Section 3 (item 18).",
        "Three backends, three summaries and models from three vendors, on question sets whose labels are exact.",
        "FR-Bank is the lifecycle-tracking store of \\mbox{\\citet{fr}}, the one evaluated store that records a lifecycle state on every entry; its stock configuration masks non-active records from retrieval, and retraction records pass that mask at $5\\%$ (Appendix~\\ref{app:believed-census}).",
        "Mem0 (\\texttt{mem0ai} 1.0.5) overwrites the record it exposes and A-MEM links notes \\citep{mem0,amem}; neither records lifecycle structure, so this paper calls them the structureless backends.",
        "The models are GPT-4.1 mini, GPT-5.6 Luna and GPT-5.6 Sol from one family in ascending size and price, Anthropic's Opus 5 and Haiku 4.5, and Kimi K3 with open weights.",
        "Table~\\ref{tab:setup} names every population with its size, its positives and the models that ran on it, and every later number is stated on one of them.",
        "",
    ] + setup_table(), "Three backends, three summaries and models", "% AUX-R110-A3 (0.8400; +0.0736")

    # 21. the two results leave Section 3 (items 3, 18): the mask pass rate to Section 4, the reach sentence already in Section 6
    E.replace(228, 229, [], "On the inherited store, FR-Bank as released", "The figure describes the mask rather than the records")

    # 22. the example summary to five lines (item 90; the full excerpt stands in Appendix E.1, AUX-R86-INDEX-EXCERPT)
    E.replace(206, 213, [
        "MEMORY STORE INDEX  (metadata only; no fact content)\\\\",
        "CATEGORY\\hspace{16mm} ENTRIES\\quad ACTIVE\\quad SUPRSD\\quad RETRACT\\quad EXPIRED\\\\",
        "HOBBIES\\_RECREATION\\hspace{8mm}29\\hspace{8mm}18\\hspace{8mm}11\\hspace{10mm}0\\hspace{10mm}2\\\\",
        "ATTRIBUTE NAMES BY CATEGORY (value-scrubbed; abridged)\\quad HOBBIES\\_RECREATION: hiking\\_experience, hiking\\_preference, ...\\\\",
        "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT (abridged): hiking\\_preference, ...",
    ], "MEMORY STORE INDEX", "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT")

    # 23. the finding sentence leaves Related work (item 3)
    E.replace(167, 167, [], "On this store the answer is little on the named state", "On this store the answer is little on the named state")

    # 24. the four-finding paragraph leaves Section 1 (item 7); the contributions list of item 5 lands in Phase 3
    E.replace(100, 116, [
        "%% Writing pass Phase 1 (2026-09-15), item 7: the four-finding paragraph deleted; every number in it reappears in Sections 5 to 9 with its population; the contributions list (item 5) lands in Phase 3.",
        "",
    ], "First, the monitors are name readers.", "")

    # 24b. two-line table headers for Table 6 (item 55)
    E.replace(70, 70, [
        "\\newcommand{\\believed}{\\textsc{believed}}",
        "% Writing pass Phase 1: two-line table headers (item 55), right- and left-aligned.",
        "\\newcommand{\\hd}[2]{\\begin{tabular}[b]{@{}r@{}}#1\\\\#2\\end{tabular}}",
        "\\newcommand{\\hdl}[2]{\\begin{tabular}[b]{@{}l@{}}#1\\\\#2\\end{tabular}}",
    ], "\\newcommand{\\believed}", "\\newcommand{\\believed}")

    # 25. the file's provenance comment
    E.replace(43, 43, [
        "% Built by reviews/v18/tools/build_v18.py; CLAIMS.md R110 block; reviews/v18/.",
        "% Writing pass (2026-09-15, paper_v18_writing_prompt.md; program R111): Phase 0 the abstract v8; Phase 1 the structure and cuts (reviews/v18/tools/wp_phase1.py, every",
        "% edit asserted by line range): Section 8 split into 8 and 9, the population table, the six body tables rewritten to two decimals with short captions, the cuts of items 1 and 90.",
    ], "% Built by reviews/v18/tools/build_v18.py", "% Built by reviews/v18/tools/build_v18.py")


# ----------------------------------------------------------------------------------------------------------------------------------
# the appendix edits (line numbers of appendix_v18.tex at 78d8f8b)
# ----------------------------------------------------------------------------------------------------------------------------------

def routes_full():
    return [
        "%% R110: the rows of Section 6's Table 3 that the author's trim order of 2026-09-15 moved here: Haiku 4.5 on the retrieved-view monitors (AUX-RESP-A1-H45-HYBRID, -H45-RETRIEVED) and the four readers with no model in them under the join's tags (AUX-R110-A2).",
        "%% Writing pass Phase 1 (2026-09-15), items 36 and 90: the four readers under the store's own tags moved here from the body's Table 2 (AUX-R110-A2: TD 0.6209, TL 0.6523, HL 0.6857; AUX-R110-A2-OWNVSJOIN: FR 0.7212;",
        "%% AUX-RESP-A1-BELIEVED 0.8144), and the sign fix: the printed difference on every no-model row is the monitor minus the reader (as the ledger records it), so those rows now name the monitor first. No cell value changes.",
        "\\begin{table}[H]",
        "\\caption{The tagged view, the rows Section~\\ref{sec:routes}'s table leaves out: Haiku 4.5 on the view and on summary plus view under ground-truth tags, and the four readers with no model in them under each tag source, each against the GPT-4.1 mini monitor that saw the same input. The readers are tag density (the fraction of lines tagged non-active), the tagged-name lookup (the question against the names of the tagged lines), the forbidding-record indicator (the item's forbidding record in view and tagged) and the hybrid of the name lookup with the tagged-name lookup. $\\Delta$ is the first-named score minus the second, with both intervals.}",
        "\\label{tab:routes-full}",
        "\\centering",
        "\\tiny",
        "\\setlength{\\tabcolsep}{2pt}",
        "\\begin{tabular}{@{}lrrrll@{}}",
        "\\toprule",
        "Row & first & second & $\\Delta$ & item interval & profile interval \\\\",
        "\\midrule",
        "Haiku 4.5, view (ground-truth tags) minus its summary alone & $0.7134$ & $0.8210$ & $-0.1077$ & $[-0.1732,-0.0369]$ & $[-0.1939,-0.0203]$ \\\\",
        "Haiku 4.5, summary plus view (ground-truth tags) minus its summary alone & $0.7863$ & $0.8210$ & $-0.0347$ & $[-0.0930,+0.0248]$ & $[-0.1109,+0.0433]$ \\\\",
        "\\addlinespace",
        "\\multicolumn{6}{@{}l}{\\textit{Ground-truth tags: the GPT-4.1 mini monitor on the same input minus the reader with no model in it}}\\\\",
        "View monitor minus tag density & $0.6851$ & $0.6157$ & $+0.0694$ & $[+0.0375,+0.1053]$ & $[+0.0257,+0.1103]$ \\\\",
        "View monitor minus tagged-name lookup & $0.6851$ & $0.6313$ & $+0.0538$ & $[+0.0232,+0.0899]$ & $[+0.0110,+0.0951]$ \\\\",
        "View monitor minus forbidding-record indicator & $0.6851$ & $0.6683$ & $+0.0168$ & $[-0.0192,+0.0572]$ & $[-0.0380,+0.0784]$ \\\\",
        "Summary-plus-view monitor minus hybrid lookup & $0.8303$ & $0.7708$ & $+0.0595$ & $[-0.0005,+0.1228]$ & $[-0.0198,+0.1498]$ \\\\",
        "\\addlinespace",
        "\\multicolumn{6}{@{}l}{\\textit{The store's own tags: the same, against the view monitor under those tags}}\\\\",
        "View monitor minus tag density & $0.8144$ & $0.6209$ & $+0.1934$ & $[+0.1446,+0.2462]$ & $[+0.1280,+0.2536]$ \\\\",
        "View monitor minus tagged-name lookup & $0.8144$ & $0.6523$ & $+0.1621$ & $[+0.1123,+0.2164]$ & $[+0.0967,+0.2320]$ \\\\",
        "View monitor minus forbidding-record indicator & $0.8144$ & $0.7212$ & $+0.0932$ & $[+0.0440,+0.1453]$ & $[+0.0273,+0.1552]$ \\\\",
        "View monitor minus hybrid lookup & $0.8144$ & $0.6857$ & $+0.1287$ & $[+0.0771,+0.1878]$ & $[+0.0597,+0.2003]$ \\\\",
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
    ]


def appendix_edits(E: Edits):
    # a. tab:routes-full with the moved rows and the sign fix (items 36, 90)
    E.replace(890, 909, routes_full(), "%% R110: the rows of Section 6's Table 3", "\\end{table}")

    # b. E.9: the 5% provenance, the Conflate row's content (items 52, 90)
    E.replace(745, 745, [
        "This appendix records the believed superseded list, the renderer's cap, and the fourth-backend trial, because each bears on how much of the loss is the store's.",
        "",
        "%% Writing pass Phase 1 (2026-09-15), items 52 and 90: the 5% provenance sentence from Section 4 and the body's Conflate row (AUX-SIDE-S2-CENSUS; the R109 write-path census) as prose.",
        "\\paragraph{Two census facts the body states in brief.}",
        "The pass rate of $5\\%$ that Section~\\ref{sec:setup} cites for FR-Bank's mask is the released store's own figure, measured on its $40$ retraction questions with the mask in place \\citep{fr}.",
        "The store also conflates retraction with supersession: of $31$ entries marked retracted across the $40$ personas, $22$ share a slot key with another entry and $16$ carry a supersedes pointer, so the write path records retraction through the supersession mechanism and the backend's own metadata cannot separate retracted from superseded content.",
        "The manifests record $40$ retraction events, one per persona, and the ground-truth join resolves $9$ of them to a retracted entry ($23$ entries).",
    ], "This appendix records the believed superseded list", "This appendix records the believed superseded list")

    # c. E.7: the compression reading and U1 from Section 7 (item 1), spliced between the carried block's U3 lines and its table paragraph
    E.replace(574, 574, [
        "%%V11:1563-1574%%",
        "%% Writing pass Phase 1 (2026-09-15), item 1: the body's structureless-store paragraph cut to four sentences; its compression reading and the U1 disclosure (C071, byte-identical; pinned once) stand here.",
        "What the summary does to the score is compression, the indexed monitor answering almost every question with the same low value.",
        "% C071 (U1, byte-identical)",
        "This is an inversion at every scale, not a below-chance score at every scale.",
        "What triggers the compression is unresolved, and the ablations that narrowed it follow.",
        "",
        "%%V11:1575-1766%%",
    ], "%%V11:1563-1766%%", "%%V11:1563-1766%%")

    # d. C.2: the lookup at the store's own name pool (AUX-R110-A4), from Section 5 (item 90)
    E.replace(331, 331, [
        "The embedding lookup falls from $0.7484$ to $0.6696$ at $60$ names, a difference whose item interval excludes zero and whose profile interval includes it; the lexical lookup is flat at every length; GPT-4.1 mini degrades first at $15$ names, below $-0.05$ with both intervals excluding zero at $15$ and $30$.",
        "%% Writing pass Phase 1 (2026-09-15), item 90: the store's-own-pool sentence from Section 5 (reviews/NUMBERS_R110.md AUX-R110-A4: 0.6531; 99.2 names; 129).",
        "With every untargeted name the store holds on the list, a mean of $99$ names per summary and at most $129$, the embedding lookup reads $0.6531$; beyond the store's own name pool it is untested.",
    ], "The embedding lookup falls from $0.7484$", "The embedding lookup falls from $0.7484$")

    # e. the file's provenance comment
    E.replace(5, 5, [
        "%% v11 because they carry the U-blocks and the U8 region.",
        "%% Writing pass (2026-09-15, paper_v18_writing_prompt.md; program R111): this file is edited in place by reviews/v18/tools/wp_phase1.py (Phase 1: E.7's carried block split around",
        "%% the U1 sentence, E.9's two census facts, C.2's own-pool sentence, tab:routes-full with the store's-own-tags rows and the sign fix). Do not re-run appendix_v18.py; it would overwrite these edits.",
    ], "%% v11 because they carry the U-blocks", "%% v11 because they carry the U-blocks")


def write_ledger():
    seen = {}
    for p, s, k in PRINTED:
        seen.setdefault((p, s), k)
    lines = [
        "# NUMBERS_WP.md: the writing pass on paper_v18 (program R111, 2026-09-15)",
        "",
        "Written by `reviews/v18/tools/wp_phase1.py`. Section 1 lists every two-decimal form the six body tables print, each from the four-decimal value",
        "under the key named (ROUND_HALF_UP, the rule `numeric_diff.py` applies; ties round away from zero). Section 2 lists the run facts the",
        "population table prints that no earlier ledger states as printed.",
        "",
        "## 1. AUX-WP-PRINTED: two-decimal forms of the body tables (Phase 1)",
        "",
        "| printed | four-decimal source | key |",
        "|---|---|---|",
    ]
    for (p, s), k in sorted(seen.items(), key=lambda x: (x[1], x[0][1])):
        lines.append(f"| {p} | {s} | {k} |")
    lines += [
        "",
        "## 2. AUX-WP-X5-DRAWS: calls per question on the authorship-matched set (Table tab:setup)",
        "",
        "| key | value |",
        "|---|---|",
        "| AUX-WP-X5-DRAWS | GPT-4.1 mini: **3** draws per arm (r74/x5/rows_MINI.jsonl: arms BLIND and INDEXED-TRUE, draws 1 to 3, 36 items; r74/NUMBERS_R74.md X5: 216 calls = 36 x 2 x 3); Opus 5: **5** (r74/x5/rows_OP5.jsonl, 360 calls); Haiku 4.5: **5** (r74/x6/rows_H45.jsonl, 360 calls). The expiry extension: GPT-4.1 mini 1, Haiku 4.5 5, Opus 5 1 (AUX-CF3-PROJECTION: 140 / 700 / 140 calls over 42 items x 3 summaries + 14 blind = 140 prompts). |",
        "",
    ]
    io.open(LEDGER, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(f"-> {LEDGER} ({len(seen)} printed forms)")


# ----------------------------------------------------------------------------------------------------------------------------------
# the polish after the first build: sentences of this script's own writing that prose_scan (cap 40 words; near-duplicate pairs) and
# q_scan (no numeral in an opener) flagged; each replacement asserts one occurrence on the edited body text
# ----------------------------------------------------------------------------------------------------------------------------------

POLISH = [
    # the population table's note, 61 words, in three sentences
    ("GPT-4.1 mini is scored from one call in the main study and every other model from five, and the finer resolution of the averaged scores is not their margin: Opus 5's first call alone keeps its margin over the lookup on the counterfactual set, and GPT-4.1 mini's repeated calls return identical scores on $46$ of $50$ questions (Appendix~\\ref{app:counterfactual}).",
     "GPT-4.1 mini is scored from one call in the main study and every other model from five. The finer resolution of the averaged scores is not their margin: Opus 5's first call alone keeps its margin over the lookup on the counterfactual set. GPT-4.1 mini's repeated calls return identical scores on $46$ of $50$ questions (Appendix~\\ref{app:counterfactual})."),
    # Section 5, the counted-state sentence (item 85), 41 words, in two
    ("The counted-state evidence rests on $30$ retraction and $44$ expiry pairs, the $30$ plus the $14$ of the descriptive extension draw in Appendix~\\ref{app:counterfactual}, and on the full obligation set ($661$ questions) the counted-state rows give only a direction (Section~\\ref{sec:populations}).",
     "The counted-state evidence rests on $30$ retraction and $44$ expiry pairs, the $30$ plus the $14$ of the descriptive extension draw in Appendix~\\ref{app:counterfactual}. On the full obligation set ($661$ questions) the counted-state rows give only a direction (Section~\\ref{sec:populations})."),
    # Section 6, the density sentence with its pointer, 50 words, in two
    ("A count of tagged lines reads the obligation at $0.62$ under either source, against the monitor's $0.81$ under the marks, and the tagged-name lookup at $0.65$, so the monitor reads more than density or name match (the four readers with no model in them are in Table~\\ref{tab:routes-full}, Appendix~\\ref{app:resp}).",
     "A count of tagged lines reads the obligation at $0.62$ under either source, against the monitor's $0.81$ under the marks, and the tagged-name lookup at $0.65$, so the monitor reads more than density or name match. The four readers with no model in them are in Table~\\ref{tab:routes-full} (Appendix~\\ref{app:resp})."),
    # Table 4's caption, 44 tokens with the table's preamble, in two sentences
    ("rendered with the fifteen-name cap and with the cap lifted; retention is Haiku 4.5's store-written gain as a fraction of its ground-truth gain.}",
     "rendered with the fifteen-name cap and with the cap lifted. Retention is Haiku 4.5's store-written gain as a fraction of its ground-truth gain.}"),
    # Section 9, the header paragraph: the opener without a numeral (q_scan Q-A), three sentences
    ("Correct answers are bounded by the view, which holds the licensed record for $65$ of the $174$ items, and by whether the prompt binds the entries to the person asking.\nA header naming",
     "Correct answers are bounded by the view and by whether the prompt binds the entries to the person asking.\nThe licensed record is in the view for $65$ of the $174$ items.\nA header naming"),
    # Section 9, the depth paragraph's last sentence, reworded away from the near-duplicate of Section 6's difference sentence
    ("For GPT-4.1 mini the difference is $+0.02$ with intervals including zero (Table~\\ref{tab:ds-a6}, Appendix~\\ref{app:resp}).",
     "GPT-4.1 mini gains $+0.02$ under the same comparison, with intervals including zero (Table~\\ref{tab:ds-a6}, Appendix~\\ref{app:resp})."),
    # Section 9, the composite's second sentence, 52 words, in two
    ("It counts a licensed item answered correctly, an obligation reached and reported, and an absent item abstained on; under the model rule it rises by $+0.03$ against retrieval alone for GPT-4.1 mini with both intervals excluding zero, and for Haiku 4.5 by a rate whose intervals include zero (Table~\\ref{tab:ds-a7}, Appendix~\\ref{app:resp}).",
     "It counts a licensed item answered correctly, an obligation reached and reported, and an absent item abstained on. Under the model rule it rises by $+0.03$ against retrieval alone for GPT-4.1 mini with both intervals excluding zero, and for Haiku 4.5 by a rate whose intervals include zero (Table~\\ref{tab:ds-a7}, Appendix~\\ref{app:resp})."),
    # Limitations, the counted-state sentence, 43 words, in two
    ("The counted-state groups are small: $30$ retraction and $30$ expiry pairs on the counterfactual set, $44$ expiry with the extension draw of Appendix~\\ref{app:counterfactual}, and $26$ retraction and $15$ expiry obligations on the full obligation set, whose counted-state rows give only a direction.",
     "The counted-state groups are small: $30$ retraction and $30$ expiry pairs on the counterfactual set, and $44$ expiry with the extension draw of Appendix~\\ref{app:counterfactual}. On the full obligation set they are $26$ retraction and $15$ expiry obligations, whose counted-state rows give only a direction."),
]


# ----------------------------------------------------------------------------------------------------------------------------------
# the author's ruling on the Phase 1 report (2026-09-15, evening): D1 (the persona-grouped interval named as such, the item-level gain
# intervals pointed to C.2; one clause in Section 4's reporting paragraph), D3 (a footnote on the matched set's cell), item 33's
# paragraph in the author's words minus its third sentence (AUX-CF2-QUESTIONREAD counts questions naming a value beyond their topic,
# not questions naming their attribute; reported, not landed), replacing Section 5's whole-set paragraph.
# ----------------------------------------------------------------------------------------------------------------------------------

RULING = [
    # D1: the caption and the column header of the counterfactual table
    ("the interval is the profile-grouped interval of the whole-set AUROC (item-level: Appendix~\\ref{app:counterfactual}).}",
     "the interval is the persona-grouped interval of the whole-set AUROC; the item-level paired gain intervals are in Appendix~\\ref{app:counterfactual}.}"),
    ("Reader, summary & Whole & Sup. & Retr. & Exp. & profile interval \\\\",
     "Reader, summary & Whole & Sup. & Retr. & Exp. & persona interval \\\\"),
    # D1: the reporting paragraph of Section 4 (item 26's clause, the author's words)
    ("where they disagree the wider decides, and two scores are within tolerance at $\\pm0.05$.\n",
     "where they disagree the wider decides, and two scores are within tolerance at $\\pm0.05$.\n"
     "On the counterfactual set the persona-grouped interval is the one printed, because resampling whole questions keeps each triple intact.\n"),
    # D3: the footnote on the matched set's cell
    ("every question rewritten in one voice & GPT-4.1 mini (3), Haiku 4.5 (5), Opus 5 (5) \\\\",
     "every question rewritten in one voice & GPT-4.1 mini (3)$^{a}$, Haiku 4.5 (5), Opus 5 (5) \\\\"),
    ("GPT-4.1 mini is scored from one call in the main study and every other model from five. The finer resolution",
     "$^{a}$Three draws per question under each prompt on this set, one call on every other. GPT-4.1 mini is scored from one call in the main study and every other model from five. The finer resolution"),
    # item 33: the author's paragraph (its third sentence held back; see WRITING_PASS.md) in place of the whole-set paragraph
    ("On the whole set two of the three models do not exceed the lookup and the largest exceeds it by a margin one call keeps.\n"
     "The lookup scores $0.77$, GPT-4.1 mini and Haiku 4.5 do not exceed it, and Opus 5 reads $+0.07$ more with both intervals excluding zero, a margin its first call alone keeps (Table~\\ref{tab:cf-main}; Appendix~\\ref{app:counterfactual}).\n"
     "% AUX-CF2-NB6-V2 (0.7663); AUX-R104-MARGIN; AUX-R110-A3\n"
     "On the state the list names, supersession, every model and the lookup read the obligation from the same names, and the lookup reads it as well as any model but the largest (Table~\\ref{tab:cf-main}).\n",
     "%% The author's paragraph of 2026-09-15 (the ruling on the Phase 1 report; items 31 and 33), one number per sentence; its third sentence (\"Most questions name the attribute they ask about (111 of the 204 drafted)\") is held back:\n"
     "%% AUX-CF2-QUESTIONREAD's 111 of 204 counts questions that name a specific value beyond their topic (the G.2 flag), not questions that name their attribute. AUX-E1R-NB6 (1.75); AUX-R104-MARGIN (+0.0742).\n"
     "Supersession is the one state the summary names.\n"
     "The superseded-names list averages $1.75$ names on the full obligation set.\n"
     "The lookup therefore has the target's name in front of it, and the question is what a model adds.\n"
     "On the counterfactual set, GPT-4.1 mini and Haiku 4.5 do not exceed the lookup and Opus 5 exceeds it by $0.07$ (Table~\\ref{tab:cf-main}).\n"
     "What the list does not name, no model reads.\n"),
]


def polish(lines):
    text = "\n".join(lines)
    for old, new in POLISH + RULING:
        assert text.count(old) == 1, (text.count(old), old[:70])
        text = text.replace(old, new)
    return text.split("\n")


def main():
    check = "--check" in sys.argv
    body = Edits(read(BODY)); body_edits(body); nb = polish(body.apply())
    appx = Edits(read(APPX)); appendix_edits(appx); na = appx.apply()
    if check:
        print(f"body: {len(nb)} lines; appendix: {len(na)} lines (check only, nothing written)")
        return
    write(BODY, nb); write(APPX, na)
    write_ledger()
    print(f"body_v18.tex: {len(nb)} lines; appendix_v18.tex: {len(na)} lines; {len(body.ops)} + {len(appx.ops)} edits applied")


if __name__ == "__main__":
    main()
