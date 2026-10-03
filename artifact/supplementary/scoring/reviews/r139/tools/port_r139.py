# -*- coding: utf-8 -*-
"""port_r139.py -- R139 (2026-09-22; the brief 'KtS R139: answer mock review 14 (W1, W2) in the paper, then the pre-upload sweep', the author's GO with
rulings, the Unit G addendum and G9) applied to the v23 sources on top of the R137 close (port_r137.py --units=close, which regenerates the R135, R134 and
R133 closes underneath). Every edit is an asserted replacement; every number the new texts print is read from reviews/r139/results/r139_printed.json,
equiv_r139.json and length_r139.json (ledger reviews/NUMBERS_R139.md), and reviews/r139/tools/r139_number_gate.py checks each against its artifact.

Units, in the order of work:
  c2    Appendix C.2: 'Equivalence within the tolerance, post hoc' (tab:equiv, tab:equiv-para) and 'The length-only reader, post hoc' (tab:length)
  a     Section 4: A1 the tolerance definition; A2 the comparison count; A3 the reader tiers and 'stronger readers' in the nine sentences
  g     Unit G (monitoring scope): G1, G2 the abstract; G3 Section 1; G4 Section 3 (only if it fits: measured, see G4_ON); G5 Section 7; G6 Limitations
        (with S3's wording); G7 the Conclusion; G9 Limitations (read-side scope)
  b     Section 5.2 and 5.3: B1 to B8 (B9, the Table 2 cell, is 'b9', applied only if it costs no line)
  c     the abstract C1, the Conclusion C3, Section 1 C4
  d     Table 3's A-MEM note
  e     Related Work: StateMemBench moved to the benchmark sentence with its clause
  f     Figure 3's persona-grouped 95% intervals (error bars; AUX-CF2-R125-PERSTATE)
  s2..s7  the sweep: s2 the five orphaned bibitems (and refcheck_v11's RETIRED); s3 the HV-1 wording in E.10; s4 Table 73 to the text width;
        s5 the em dashes in appendix prose; s6 \\mbox guards on GPT-4.1 / GPT-5.6 in the main text; s7 page 4 (only if it costs no line)
  p1..p10  the payers, each only as far as needed
Logged to reviews/r139/results/port_r139_log.json. Usage: python reviews/r139/tools/port_r139.py --units=c2,a,...  [--no-refresh]
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
V23 = ROOT / "reviews" / "v23"
SRC = V23 / "src"
R139 = ROOT / "reviews" / "r139"
RES = R139 / "results"
BODY, ABS, APPX = SRC / "body_v23.tex", SRC / "abstract_v23.tex", SRC / "appendix_v23.tex"
ROBUST, FIG3 = SRC / "robust_table.tex", SRC / "fig3_data_matched.tex"
REFCHECK = ROOT / "iclr2027_monitoring_submission" / "tools" / "refcheck_v11.py"
BASE_COMMIT = "eb37054"      # the R137 close: files outside the regenerated sources are restored from it before the units run
LOG = RES / "port_r139_log.json"
BUILD_REPAIRS = RES / "build_repairs_r139.json"
CLOSE_UNITS = RES / "r139_close_units.txt"
ORDER = ["c2", "a", "g", "b", "b9", "c", "d", "e", "f", "s2", "s3", "s4", "s5", "s6", "s7",
         "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10"]
PR = json.load(open(RES / "r139_printed.json", encoding="utf-8"))
EQ = json.load(open(RES / "equiv_r139.json", encoding="utf-8"))
LN = json.load(open(RES / "length_r139.json", encoding="utf-8"))
NL = json.load(open(RES / "n_list_r139.json", encoding="utf-8")) if (RES / "n_list_r139.json").exists() else None
G4_ON = (RES / "g4_fits.txt").exists() and (RES / "g4_fits.txt").read_text().strip() == "yes"
AC2 = "(Appendix~\\ref{app:counterfactual})"

TEXT = {}
LOGGED = []
BREP = []


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def wr(p, t):
    p.write_text(t, encoding="utf-8", newline="\n")


def rep(which, old, new, n=1, unit="", section="", note=""):
    t = TEXT[which]
    c = t.count(old)
    assert c == n, f"[{unit}] {which}: expected {n} occurrence(s), found {c} of: {old[:100]!r}"
    TEXT[which] = t.replace(old, new)
    LOGGED.append(dict(unit=unit, file=which, section=section, old=old, new=new, note=note))


def ins_after(which, anchor, new, unit="", section="", note=""):
    t = TEXT[which]
    assert t.count(anchor) == 1, f"[{unit}] {which}: anchor not unique ({t.count(anchor)}): {anchor[:90]!r}"
    TEXT[which] = t.replace(anchor, anchor + new)
    LOGGED.append(dict(unit=unit, file=which, section=section, old="", new=new, note=note))


def names(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def f4(x):
    return f"{x:+.4f}"


def iv(a):
    return f"$[{a[0]:+.4f},{a[1]:+.4f}]$"


# ====================================================================================================================== c2
def eq_table(rows, label, caption):
    out = ["\\begin{table}[H]", f"\\caption{{{caption}}}", f"\\label{{{label}}}", "\\centering\\tiny\\setlength{\\tabcolsep}{1.5pt}",
           "\\resizebox{\\textwidth}{!}{\\begin{tabular}{@{}llrllllll@{}}", "\\toprule",
           "Reader & scope, metric & difference & 95\\% item/triple & 95\\% persona & 90\\% item/triple & 90\\% persona & reliable & equivalent \\\\", "\\midrule"]
    cond = None
    for r in rows:
        if r["condition"] != cond:
            cond = r["condition"]
            out.append(f"\\multicolumn{{9}}{{@{{}}l}}{{\\textit{{{cond}}}}}\\\\")
        rd_ = r["reader"].replace("count-feature lookup minus ", "count-feature lookup $-$ ")
        out.append(f"{rd_} & {r['scope']}, {r['metric']} & ${f4(r['delta'])}$ & {iv(r['ci95_a'])} & {iv(r['ci95_persona'])} & {iv(r['ci90_a'])} & {iv(r['ci90_persona'])} & "
                   f"{'yes' if r['reliable'] else 'no'} & {'yes' if r['equivalent'] else 'no'} \\\\")
    out += ["\\bottomrule", "\\end{tabular}}", "\\end{table}"]
    return "\n".join(out) + "\n"


def length_table():
    out = ["\\begin{table}[H]",
           "\\caption{The length-only reader (post hoc): its score is the number of names in the superseded-names section of the summary it is given, and nothing else, scored as the count readers are. "
           "Pooled AUROC with the persona-grouped interval; matched W/T/L and score with the triple-level and persona-grouped intervals. The sibling-name control compares the \\pn{} version with its sibling version. "
           "\\pn{} list length minus each sibling's, per triple and sibling: " + "; ".join(
               f"{k.split('|')[0]} lists, {k.split('|')[1]}: " + ", ".join(f"${d}$ on ${n}$" for d, n in h.items()) for k, h in LN["hist_pn_minus_sibling"].items()) + ".}",
           "\\label{tab:length}", "\\centering\\tiny\\setlength{\\tabcolsep}{2pt}", "\\begin{tabular}{@{}llrrrlrrll@{}}", "\\toprule",
           "Summary & scope & items & triples & pooled & persona interval & W/T/L & matched & triple interval & persona interval \\\\", "\\midrule"]
    lab = {"padded": "padded to $60$", "unpadded": "default (short list)", "sibling": "sibling-name control"}
    for summ in ("padded", "unpadded", "sibling"):
        for scope, v in LN[summ].items():
            out.append(f"{lab[summ]} & {scope} & ${v['n_items']}$ & ${v['n_triples']}$ & ${v['pooled']:.4f}$ & $[{v['pooled_persona_ci'][0]:.4f},{v['pooled_persona_ci'][1]:.4f}]$ & "
                       f"${v['W']}/{v['T']}/{v['L']}$ & ${v['matched']:.4f}$ & $[{v['matched_triple_ci'][0]:.4f},{v['matched_triple_ci'][1]:.4f}]$ & $[{v['matched_persona_ci'][0]:.4f},{v['matched_persona_ci'][1]:.4f}]$ \\\\")
    out += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
    return "\n".join(out) + "\n"


def e_groups():
    order = ["mini", "Haiku", "Luna", "Sol", "Opus"]
    G = PR["e_groups"]
    grp = {k: [r for r in order if G[r]["matched"] == k] for k in ("equivalent", "reliably below", "reliably above", "neither")}
    return G, grp


def unit_c2():
    u = "c2"
    rows = EQ["rows"]
    main = [r for r in rows if r["condition"] != "paraphrase set"]
    order = {"default summary": 0, "sibling-name control": 1, "all-states summary": 2, "padded set": 3, "B6: lookup with one count feature": 4}
    main.sort(key=lambda r: (order[r["condition"]], r["scope"] != "supersession", r["metric"]))
    para = [r for r in rows if r["condition"] == "paraphrase set"]
    G, grp = e_groups()
    sb_eq = [r["reader"] for r in rows if r["condition"] == "sibling-name control" and r["equivalent"]]
    b6 = PR["b6"]
    h = LN["hist_pn_minus_sibling"]["unpadded|supersession"]
    per_triple = {d: n // 2 for d, n in h.items()}          # two siblings per triple, equal lengths (asserted by the histogram's even counts)
    assert all(n % 2 == 0 for n in h.values()) and h == LN["hist_pn_minus_sibling"]["padded|supersession"]
    pooled_note = "; pooled, " + names([k for k in G if G[k]["pooled"] != G[k]["matched"]]) + " " + ("is" if len([k for k in G if G[k]["pooled"] != G[k]["matched"]]) == 1 else "are") + " neither" \
        if all(G[k]["pooled"] == "neither" for k in G if G[k]["pooled"] != G[k]["matched"]) and any(G[k]["pooled"] != G[k]["matched"] for k in G) else ""
    text = (
        "%% R139 (2026-09-22): Phase 1 of the brief 'KtS R139' (mock review 14, W2 and W1), post hoc: the equivalence test (reviews/r139/tools/equiv_r139.py) and the length-only reader\n"
        "%% (length_r139.py), written by reviews/r139/tools/port_r139.py; ledger reviews/NUMBERS_R139.md (AUX-R139-EQUIV, -E-GROUPS, -B6, -LENGTH); every number through r139_number_gate.py.\n"
        "\\paragraph{Equivalence within the tolerance, post hoc.}\\label{app:equiv}\n"
        "A reliable difference is one shown to differ from zero; a difference that is not reliable is not thereby shown to be small. "
        "The mirror test is two one-sided tests at $5\\%$: a difference is equivalent within $0.05$ when both of its $90\\%$ intervals, the item-level (triple-level on the matched metric) and the persona-grouped one, "
        "lie inside $[-0.05,+0.05]$. The $90\\%$ intervals come from the same $1{,}000$ draws that give the printed $95\\%$ ones. "
        "Tables~\\ref{tab:equiv} and~\\ref{tab:equiv-para} apply the test to every model-minus-lookup row printed for the default summary, the sibling-name control, the all-states summary, the padded set and the paraphrase set, "
        "and to the lookup with one count feature against the three stronger readers. A row can be neither reliable nor equivalent; its difference is then neither shown nor excluded. "
        "The test is post hoc and changes no reliable verdict.\n"
        f"On the short list's supersession triples, on the matched metric, {names(grp['equivalent'])} {'is' if len(grp['equivalent']) == 1 else 'are'} equivalent to the lookup, "
        f"{names(grp['reliably below'])} {'is' if len(grp['reliably below']) == 1 else 'are'} reliably below it and {names(grp['neither'])} {'is' if len(grp['neither']) == 1 else 'are'} neither{pooled_note}. "
        f"Under the sibling-name control {('no reader is equivalent to the lookup' if not sb_eq else names(sb_eq) + ' are equivalent to the lookup')}, "
        f"and the lookup with one count feature is {'neither reliably different from nor equivalent to any of' if set(b6.values()) == {'neither'} else 'compared with'} the three stronger readers.\n"
        "\n"
        + eq_table(main, "tab:equiv", "Equivalence within $0.05$ (post hoc): each model minus the name lookup under the same summary, every row printed for the default summary (Tables~\\ref{tab:sup-margins}, \\ref{tab:cfpad-whole} and~\\ref{tab:cf-matched-vs}), "
                   "the sibling-name control (Table~\\ref{tab:cf-sibling}), the all-states summary (Tables~\\ref{tab:cf-main} and~\\ref{tab:cf-matched-vs}) and the padded set (Tables~\\ref{tab:cfpad-minus-lookup} and~\\ref{tab:cfpad-whole}), "
                   "and the lookup with one count feature minus each stronger reader (matched, $148$ triples). Pooled rows: item-level and persona-grouped intervals; matched rows: triple-level and persona-grouped. "
                   "Equivalent: both $90\\%$ intervals inside $[-0.05,+0.05]$, the two one-sided tests at $5\\%$; reliable: both $95\\%$ intervals exclude zero; a row that is neither is neither shown nor excluded.")
        + eq_table(para, "tab:equiv-para", "Equivalence within $0.05$ on the paraphrase set (post hoc): every row of Tables~\\ref{tab:para-minus-lookup} and~\\ref{tab:para-sup}, on the paraphrases and on the original questions of the same pairs; "
                   "Luna and Sol were added after the registration. Columns and rule as in Table~\\ref{tab:equiv}.")
        + "\n"
        "\\paragraph{The length-only reader, post hoc.}\\label{app:length}\n"
        "A reader whose score is the number of names in the superseded-names section of the summary it is given, and nothing else, is scored as the count readers are (Table~\\ref{tab:length}). "
        f"On the supersession triples the \\pn{{}} version's list is longer than each sibling's in every triple, on the default and the padded lists alike (by one name on ${per_triple['1']}$ triples, two on ${per_triple['2']}$ and three on ${per_triple['3']}$), "
        f"so the reader wins all ${LN['padded']['supersession']['n_triples']}$ triples on both; on the padded lists, where every \\pn{{}} list holds ${PR['length'] and LN['padded_lengths']['pn_max']}$ names and every sibling's fewer, it is also perfect pooled. "
        "On the sibling-name control the lists have equal length by construction and the reader ties every triple. "
        "The pad is identical across a triple, so the padded set carries the length difference the default lists already carry; no sibling padded to equal length was run.\n"
        "\n" + length_table() + "\n")
    anchor = "Every served model identifier was checked on a probe call before its run and on every row at scoring; no run reached its cap.\n\n"
    ins_after("appendix", anchor, text, unit=u, section="C.2, after the long-list check", note="Phase 1.1 and 1.2: the two post hoc subsections with their tables")


# ====================================================================================================================== a
STRONGER = [  # (file, old, new): 'stronger models' -> 'stronger readers' in the paper's own grouping, the nine sentences of Phase 0.2 (A3)
    ("abstract", "the lookup loses $0.02$ and one stronger model edges $0.04$ ahead.", "the lookup loses $0.02$ and one stronger reader edges $0.04$ ahead."),
    ("abstract", "The three stronger models lead only where", "The three stronger readers lead only where"),
    ("body", "The stronger models' lead comes from the counts, which the two smaller models do not use.", "The stronger readers' lead comes from the counts, which the two smaller models do not use."),
    ("body", "\\claim{The three stronger models also read the counts.}", "\\claim{The three stronger readers also read the counts.}"),
    ("body", "\\claim{The stronger models' lead comes from counts, and a count feature closes it within a question.}", "\\claim{The stronger readers' lead comes from counts, and a count feature closes it within a question.}"),
    ("body", "among the stronger models only Opus ran the all-states summary", "among the stronger readers only Opus ran the all-states summary"),
    ("body", "when the questions are reworded only one stronger model edges past it.", "when the questions are reworded only one stronger reader edges past it."),
    ("body", "The stronger models' lead comes from counts the smaller models do not use.", "The stronger readers' lead comes from counts the smaller models do not use."),
    ("body", "Told the intent rule, only the stronger models apply it,", "Told the intent rule, only the stronger readers apply it,"),
]


def unit_a():
    u = "a"
    rep("body", "\\emph{Within tolerance} means an absolute difference no greater than $0.05$.",
        f"\\emph{{Within tolerance}} means a point difference no greater than $0.05$; it does not establish equivalence, which we test separately at $0.05$ {AC2}.",
        unit=u, section="4, Tests and comparisons", note="A1 verbatim (the pointer as the brief's 'Appendix C.2')")
    rep("body", "We apply no multiplicity correction, so reliable describes each comparison on its own.",
        f"We apply no multiplicity correction; reliable describes each of the $@@N@@$ comparisons the main text makes on its own, and each registered family holds five readers (three under the all-states summary).",
        unit=u, section="4, Tests and comparisons", note="A2 as ruled (N = AUX-R139-N, the distinct comparisons of the final main text; filled at the end of the run)")
    rep("body", "abbreviated mini, Haiku, Luna, Sol and Opus in that order, and Kimi K3 (open weights) joins the cross-vendor comparison.",
        "abbreviated mini, Haiku, Luna, Sol and Opus in that order. We call the last three the stronger readers and the first two the smaller, by vendor tier. Kimi K3 (open weights) joins the cross-vendor comparison.",
        unit=u, section="4, Stores and readers", note="A3 as ruled: by vendor tier, no E.11 pointer")
    for f, o, n in STRONGER:
        rep(f, o, n, unit=u, section="the nine sentences", note="A3: 'stronger models' -> 'stronger readers'")


# ====================================================================================================================== g
S3 = "registered, with its workbooks built and no label collected at submission"
S3_MAIN = "specified in Appendix~\\ref{app:registration}, with its workbooks built and no label collected at submission"   # the main text's form (rule V bars 'registered'; the ruling of 22 Sep, 23:54)


def unit_g():
    u = "g"
    import os
    skip = set(os.environ.get("R139_GSKIP", "").split(","))   # costing only (the leave-one-piece-out table); never set for a committed build
    _rep = globals()["rep"]

    def rep(which, old, new, n=1, unit="", section="", note=""):
        if note.split(" ")[0] in skip:
            return
        _rep(which, old, new, n, unit, section, note)
    rep("abstract", "We ask what a memory store must expose for an agent to know this before retrieving anything.\n",
        "We ask what a memory store must expose for an agent to know this before retrieving anything, and we score that judgment on its own, as metamemory monitoring.\n", unit=u, section="the abstract", note="G1")
    rep("abstract", "All stores are synthetic, and we do not show that better judgments yield better answers.\n",
        "All stores are synthetic; control, whether a better judgment yields a better answer, is left to a later study.\n", unit=u, section="the abstract", note="G2")
    rep("body", "here judged about an external store.\n",
        "here judged about an external store. We study the monitoring side of that distinction only: how accurately a reader judges the store from what it exposes. "
        "Whether the judgment then changes what is retrieved or answered is control, and we leave it to a later study.\n", unit=u, section="1, paragraph 2", note="G3 (after the Nelson and Narens sentence; unit c rewrites that sentence)")
    if G4_ON:
        rep("body", "the coverage judgment estimates the probability of either \\present{} or \\pn{}.\n",
            "the coverage judgment estimates the probability of either \\present{} or \\pn{}; these two judgments are what the paper monitors.\n", unit=u, section="3, Labels and judgments", note="G4 (measured: fits on the existing line)")
    rep("body", "\\section{At retrieval}", "\\section{What retrieval puts in view}", unit=u, section="7", note="G5 title")
    rep("body", "\\claim{The tagged view complements the summary for mini.}\n",
        "This section scores what each policy brings into a reader's view, the reach of the forbidding record, not what an answerer does with it; the exploratory answer stage is in Appendix~\\ref{app:resp}.\n"
        "\\claim{The tagged view complements the summary for mini.}\n", unit=u, section="7, first paragraph", note="G5 opening sentence")
    rep("body", "Answer outcomes remain exploratory: the token detector can flag mentions rather than use, and its independent human validation is unfinished. The reach results establish neither better answers nor a validated answer-stage detector.",
        f"Control is outside this paper's scope. The answer stage in Appendix~\\ref{{app:resp}} is exploratory: its token detector can flag mentions rather than use, and its human validation is {S3_MAIN}; nothing here shows that a better judgment changes an answer.",
        unit=u, section="9, Limitations", note="G6 with S3's wording")
    rep("body", "In these tests, no reader we tried made up for what the store had failed to write down.",
        "In these monitoring tests, no reader we tried made up for what the store had failed to write down.", unit=u, section="10", note="G7")
    rep("body", "The counterfactual test bypasses backend writing, and no backend tested here is shown maintaining the summary.",
        "We change no backend's write path: the counterfactual test bypasses writing, every intervention is on the read side, and no backend tested here is shown maintaining the summary. "
        "The reach and answer results therefore describe what a store as shipped affords a reader, not what a repaired one would; a write-path intervention is a separate study.",
        unit=u, section="9, Limitations", note="G9")


# ====================================================================================================================== b
def unit_b():
    u = "b"
    G, grp = e_groups()
    b1 = PR["b1"]
    # B1 + the E-iv sentence
    old1 = "The default summary names only supersession; on its triples the lookup scores $0.97$, Opus is $0.01$ above it, Luna and Sol $0.01$ below, and only mini reliably below."
    parts = []
    if grp["equivalent"]:
        parts.append(f"{names(grp['equivalent'])} {'is' if len(grp['equivalent']) == 1 else 'are'} equivalent to the lookup on the short list")
    if grp["reliably below"]:
        only = [k for k in grp["reliably below"] if G[k]["pooled"] == "neither"]
        parts.append(f"{names(grp['reliably below'])} {'sits' if len(grp['reliably below']) == 1 else 'sit'} reliably below it" + (" on the matched metric only" if only == grp["reliably below"] else ""))
    if grp["neither"]:
        parts.append(f"for {names(grp['neither'])} neither holds")   # the author's wording (rulings of 22 Sep, 23:54)
    assert not grp["reliably above"]
    e_sent = f"Within $0.05$, {'; '.join(parts)} {AC2}."
    rep("body", old1, old1 + f" Pooled, the lookup scores ${b1['lookup']}$ and the three ${b1['lo']}$ to ${b1['hi']}$, none reliably above it. " + e_sent,
        unit=u, section="5.2, paragraph 1", note="B1 (the pooled comparison, its own sentence: rule L) and the E-iv sentence after it (ruling B6)")
    # B2
    s = PR["sb_opus"]
    rep("body", "at $0.88$ or higher, none reliably above the lookup, while meaningless tokens",
        f"at $0.88$ or higher, none reliably above the lookup (Opus, the closest, ${s['sign']}{s['delta']}$ $[{s['item_lo_sign']}{s['item_lo']},{s['item_hi_sign']}{s['item_hi']}]$), while meaningless tokens",
        unit=u, section="5.2, paragraph 1", note="B2: the wider (item-level) interval, as ruled")
    # B3, before the padded-list sentence
    L = PR["lists"]
    rep("body", "With the superseded-name list padded to $60$ names (Table~\\ref{tab:robust}),",
        f"At these lengths, ${L['pn_mean_printed']}$ names on average and at most ${L['pn_max']}$, the lookup is close to a string match against one or two candidates (Table~\\ref{{tab:cf-emptiness}}; FR-Bank's own lists in Appendix~\\ref{{app:census}}). "
        "With the superseded-name list padded to $60$ names (Table~\\ref{tab:robust}),", unit=u, section="5.2, paragraph 1", note="B3 as ruled (one line)")
    # B4
    rep("body", "mini, Haiku and Opus fall with it, ending level with it or below.", "mini, Haiku and Opus fall with it, ending at or below it with no reliable difference.", unit=u, section="5.2, paragraph 1", note="B4")
    # B5: replaces the paragraph's closing pointer (the text carries its own)
    rep("body", "and $0.09$ to $0.10$ within triples. (Appendix~\\ref{app:counterfactual})\n",
        "and $0.09$ to $0.10$ within triples. The pad is identical across a triple. The \\pn{} list is one to three names longer than its siblings' in every supersession triple, on the short list and the padded one alike; "
        "a reader that outputs only the list length separates them in every such triple. The sibling-name control removed that cue on the short list, where readers still picked the \\pn{} version at $0.88$ or higher; "
        f"the padded set has no such control {AC2}.\n", unit=u, section="5.2, paragraph 1", note="B5 as ruled, verbatim")
    # B6
    verdicts = set(PR["b6"].values())
    assert len(verdicts) == 1, PR["b6"]
    v = verdicts.pop()
    clause = {"neither": "equivalence within $0.05$ is neither shown nor excluded", "equivalent": "they are equivalent within $0.05$"}[v]
    rep("body", "scores $0.89$ beside the three models' $0.86$ to $0.88$; we ran no equivalence test.",
        f"scores $0.89$ beside the three models' $0.86$ to $0.88$; {clause} {AC2}.", unit=u, section="5.2, paragraph 4",
        note="B6: all three verdicts 'neither'; the pass's wording rule ('neither shown nor excluded') over the ruling's binary 'not equivalent within 0.05'")
    # B7
    b7 = PR["b7"]
    rep("body", "A fixed cue list matches the best model, so the test shows",
        f"A fixed cue list is not reliably below the best model (${b7['delta']}$ $[{b7['lo']},{b7['hi']}]$), so the test shows", unit=u, section="5.3", note="B7: the crossover's own pair (the wider, pair-clustered)")
    # B8
    rep("body", "Under the all-states summary the lookup loses $0.06$ pooled and $0.02$ within triples. (Appendix~\\ref{app:counterfactual})",
        "Under the all-states summary the lookup loses $0.06$ pooled and $0.02$ within triples.", unit=u, section="5.2, paragraph 2", note="B8: the pointer dropped")


def unit_b9():
    rep("robust", "lead it by $0.13$ to $0.14$ \\\\", f"lead it by $0.13$ to $0.14$; length-only reader ${LN['padded']['supersession']['pooled']:.2f}$ \\\\", unit="b9", section="Table 2 row 9", note="B9 (applied only if it costs no line)")


# ====================================================================================================================== c
def unit_c():
    u = "c"
    G, grp = e_groups()
    stronger = ["Luna", "Sol", "Opus"]
    if grp["equivalent"] == stronger:
        eq_abs, eq_con = ". The three stronger ones are equivalent to it within $0.05$", "; the three stronger readers are equivalent to it within $0.05$"   # the abstract split at the ruled point (rule L)
    elif grp["equivalent"]:
        eq_abs = eq_con = f", and {names(grp['equivalent'])} {'is' if len(grp['equivalent']) == 1 else 'are'} equivalent to it within $0.05$"
    else:
        eq_abs = eq_con = ", and none is shown equivalent to it"
    old = ("Where the summary names the affected attribute and the list is short, none of five language models reliably beats a cosine-similarity lookup over the names, including under a control that fixes counts and list length.\n"
           "Padded to $60$ names, the lookup loses $0.18$; GPT-5.6 Luna and Sol lose $0.06$ to $0.07$ and lead it by $0.13$ to $0.14$, while the other three fall with it.\n")
    ctrl = "including with counts and list length fixed" if "--abs-trim" in sys.argv or (RES / "abs_trim.txt").exists() else "including under a control that fixes counts and list length"
    new = ("What a model adds depends on the length of that list.\n"
           f"On the short lists the benchmark's ground truth produces (${PR['lists']['pn_mean_printed']}$ names on average), none of five language models reliably beats a cosine-similarity lookup over the names, {ctrl}{eq_abs}.\n"
           "On lists as long as real stores write, padded to $60$ names, the lookup loses $0.18$; GPT-5.6 Luna and Sol lose $0.06$ to $0.07$ and lead it by $0.13$ to $0.14$, while the other three fall with it.\n")
    rep("abstract", old, new, unit=u, section="the abstract", note="C1 (E-clause from AUX-R139-E-GROUPS)" + ("; G2's trim applied (the +1 cap)" if "fixed" in ctrl else ""))
    rep("body", "On a named state no model reliably exceeds the name lookup on the short list, with list length kept fixed or not, and when the questions are reworded only one stronger reader edges past it.",
        f"On a named state no model reliably exceeds the name lookup on the short list, with list length kept fixed or not{eq_con}. When the questions are reworded only one stronger reader edges past it.",
        unit=u, section="10", note="C3: the E-clause (the sentence split: rule L)")
    rep("body", "and a fixed cue list matches the best of them.", "and a fixed cue list is not reliably below the best of them.", unit=u, section="10", note="C3")
    rep("body", "In metamemory terms these are negative-obligation knowledge (NOK) and the feeling of knowing (FOK) \\citep{hart1965,nelson1990,koriat1993}, here judged about an external store.",
        "The second is the feeling of knowing (FOK) of the metamemory literature \\citep{hart1965,nelson1990,koriat1993}; the first we call negative-obligation knowledge (NOK), a term this paper introduces.",
        unit=u, section="1, paragraph 2", note="C4 as drafted")


# ====================================================================================================================== d, e
def unit_d():
    rep("body", "resolve to $0$ note identifiers, on the $40$ scored personas. \\\\",
        "resolve to $0$ note identifiers, on the $40$ scored personas (not checked against the reference implementation). \\\\", unit="d", section="Table 3, A-MEM", note="D1 (the measurement cell's end)")


def unit_e():
    u = "e"
    rep("body", "conflict resolution after retrieval \\citep{longmemeval,locomo,memora,memoryagentbench}.",
        "conflict resolution after retrieval \\citep{longmemeval,locomo,memora,memoryagentbench}, and StateMemBench scores whether an answer reflects the current or a superseded state \\citep{statemembench}.",
        unit=u, section="2", note="E: the author's clause")
    rep("body", "pmbench,hushbench,statemembench,xu2024conflicts", "pmbench,hushbench,xu2024conflicts", unit=u, section="2", note="E: out of the lifecycle-information list")


# ====================================================================================================================== f
FIGKEYS = {"mini": "MINI5_v2", "haiku": "H45_v2", "luna": "LUNA_v2", "sol": "SOL_v2", "opus": "OP5_v2", "lookup": "LOOKUP_v2", "count": "CR-nb1_v2"}
FIGKEYS_ALL = {"mini": "MINI5_v3", "haiku": "H45_v3", "opus": "OP5_v3", "lookup": "ALLSTATES_v3"}


def unit_f():
    u = "f"
    R = json.load(open(ROOT / "reviews" / "r125" / "results" / "r125_matched.json", encoding="utf-8"))["readers"]
    t = rd(FIG3)

    def table(keys, macro):
        hdr = "x,state," + ",".join(f"{k},{k}P,{k}M" for k in keys)
        lines = [hdr]
        for x, st in enumerate(("SUPERSESSION", "RETRACTION", "EXPIRY")):
            cells = []
            for k, rk in keys.items():
                b = R[rk]["pn_vs_present"]["per_state"][st]
                mval, lo, hi = b["matched"], b["ci_persona"]["ci_lo"], b["ci_persona"]["ci_hi"]
                cells.append(f"{mval:.4f},{hi - mval:.4f},{mval - lo:.4f}")
            lines.append(f"{x},{st.capitalize()}," + ",".join(cells))
        return "\\pgfplotstableread[col sep=comma]{\n" + "\n".join(lines) + "\n}" + macro

    old_sup = t[t.index("\\pgfplotstableread[col sep=comma]{\nx,state,mini,haiku,luna,sol,opus,lookup,count"):t.index("}\\figthreeSup") + len("}\\figthreeSup")]
    old_all = t[t.index("\\pgfplotstableread[col sep=comma]{\nx,state,mini,haiku,opus,lookup"):t.index("}\\figthreeAll") + len("}\\figthreeAll")]
    # the points are unchanged: asserted against the file's values
    for blk, keys in ((old_sup, FIGKEYS), (old_all, FIGKEYS_ALL)):
        rows = [r.split(",") for r in blk.splitlines()[2:5]]
        for i, st in enumerate(("SUPERSESSION", "RETRACTION", "EXPIRY")):
            for j, (k, rk) in enumerate(keys.items()):
                assert abs(float(rows[i][2 + j]) - R[rk]["pn_vs_present"]["per_state"][st]["matched"]) < 5e-5, (k, st)
    t = t.replace(old_sup, table(FIGKEYS, "\\figthreeSup")).replace(old_all, table(FIGKEYS_ALL, "\\figthreeAll"))
    t = ("%% R139 (2026-09-22), Unit F: the persona-grouped 95% interval of each point (reviews/r125/results/r125_matched.json readers.*.pn_vs_present.per_state.*.ci_persona;\n"
         "%% AUX-CF2-R125-PERSTATE), as offsets <reader>P (up) and <reader>M (down) for pgfplots' explicit error bars; the points unchanged (asserted).\n") + t
    wr(FIG3, t)
    LOGGED.append(dict(unit=u, file="fig3_data_matched", section="Figure 3 data", old="", new="the P/M columns", note="F: the persona-grouped intervals"))
    for k in ("mini", "haiku", "luna", "sol", "opus", "lookup", "count"):
        for macro in ("\\figthreeSup", "\\figthreeAll"):
            old = f"table[x=x, y={k}] {{{macro}}};"
            if TEXT["body"].count(old) == 1:
                rep("body", old, f"table[x=x, y={k}, y error plus={k}P, y error minus={k}M] {{{macro}}};", unit=u, section="Figure 3", note="F: the error-bar columns")
    rep("body", "    ymajorgrids, grid style={black!12}, axis line style={black!60}, clip=false,\n",
        "    ymajorgrids, grid style={black!12}, axis line style={black!60}, clip=false,\n    error bars/y dir=both, error bars/y explicit, error bars/error mark options={mark size=0.8pt, rotate=90}, error bars/error bar style={line width=0.35pt},\n",
        unit=u, section="Figure 3", note="F: the bars' style (same footprint)")
    rep("body", "Every value is in the tables of Appendix~\\ref{app:counterfactual}.}", "Every value is in the tables of Appendix~\\ref{app:counterfactual}; bars: persona-grouped 95\\% intervals.}",
        unit=u, section="Figure 3 caption", note="F: the caption")


# ====================================================================================================================== sweep
ORPHANS = ["ren2025", "verbrouting", "wang2023", "metamem", "seakr"]


def unit_s2():
    import re
    for k in ORPHANS:
        m = re.search(r"\\bibitem\[[^\]]*\]\{" + re.escape(k) + r"\}\n.*?\n\n", TEXT["body"], flags=re.S)
        assert m, k
        rep("body", m.group(0), "", unit="s2", section="References", note=f"S2: the orphaned bibitem {k} (never cited)")
    t = TEXT["refcheck"]
    old = "RETIRED = {'knowbutnotact', 'dunlosky2009', 'knowact', 'metcalfe1994', 'naeini2015', 'nosek2018', 'pineau2021', 'openaimemory', 'memgate'}"
    assert t.count(old) == 1
    new = ("# R139 (2026-09-22), sweep S2: the five bibitems no citation reached (Ren 2025, Sah 2026, Wang 2023, Xin 2026, Yao 2024) removed from the bibliography; their records stay above.\n"
           "RETIRED = {'knowbutnotact', 'dunlosky2009', 'knowact', 'metcalfe1994', 'naeini2015', 'nosek2018', 'pineau2021', 'openaimemory', 'memgate',\n"
           "           'ren2025', 'verbrouting', 'wang2023', 'metamem', 'seakr'}")
    TEXT["refcheck"] = t.replace(old, new)
    LOGGED.append(dict(unit="s2", file="refcheck_v11.py", section="RETIRED", old=old, new=new, note="S2"))


def unit_s3():
    u = "s3"
    rep("appendix", "Agreement with the second annotator's fourth question is reported once the sheet is labeled.",
        f"Agreement with the second annotator's fourth question is not reported: the validation is {S3}.", unit=u, section="E.10", note="S3 site 2")
    rep("appendix", "and the detector's human validation is in progress (the validation sample", f"and the detector's human validation is {S3} (the validation sample", unit=u, section="E.10", note="S3 site 3")
    rep("appendix", "with its limits in Appendix~\\ref{app:resp}; its human validation is pending.", f"with its limits in Appendix~\\ref{{app:resp}}; its human validation is {S3}.", unit=u, section="E.10 table note", note="S3 site 4")
    rep("appendix", "and with the detector at both thresholds on the first three, is reported here once labeled.",
        f"and with the detector at both thresholds on the first three, is not reported: the validation is {S3}.", unit=u, section="E.10", note="S3 site 5 (site 1, Limitations, is in unit g)")


def unit_s4():
    BREP.append(["\\label{tab:resp-l1}\\centering\\scriptsize\\setlength{\\tabcolsep}{3pt}\n\\begin{tabular}{@{}lrrrrllrr@{}}\\toprule",
                 "\\label{tab:resp-l1}\\centering\\scriptsize\\setlength{\\tabcolsep}{3pt}\n\\resizebox{\\textwidth}{!}{\\begin{tabular}{@{}lrrrrllrr@{}}\\toprule", 1])
    BREP.append(["& $0.4053$ & $0.4455$ \\\\\n\\bottomrule\\end{tabular}\\end{table}", "& $0.4053$ & $0.4455$ \\\\\n\\bottomrule\\end{tabular}}\\end{table}", 1])
    # the margin scan of the R139 close (x1 > 541.5 pt) found one more: tab:resp-l2, the retrieved-view monitors (48 pt overfull since v22)
    BREP.append(["\\label{tab:resp-l2}\\centering\\scriptsize\\setlength{\\tabcolsep}{3pt}\n\\begin{tabular}{@{}llrrrrll@{}}\\toprule",
                 "\\label{tab:resp-l2}\\centering\\scriptsize\\setlength{\\tabcolsep}{3pt}\n\\resizebox{\\textwidth}{!}{\\begin{tabular}{@{}llrrrrll@{}}\\toprule", 1])
    BREP.append(["expiry $12$ of $15$.} \\\\\n\\bottomrule\\end{tabular}\\end{table}", "expiry $12$ of $15$.} \\\\\n\\bottomrule\\end{tabular}}\\end{table}", 1])
    LOGGED.append(dict(unit="s4", file="build", section="E.10, Table 73 and tab:resp-l2", old="", new="resizebox to the text width", note="S4 (and the margin scan's second table)"))


EMDASH = [
    ("excludes zero on Opus 5 only---the resolution an $n=36$ set affords.", "excludes zero on Opus 5 only, the resolution an $n=36$ set affords."),
    ("This is a deterministic census on recorded labels---no model is fit and nothing is resampled---so no interval", "This is a deterministic census on recorded labels (no model is fit and nothing is resampled), so no interval"),
    ("which bounds the mechanism rather than that specificity---per-category correspondence", "which bounds the mechanism rather than that specificity: per-category correspondence"),
    ("The names condition has no ablation site --- these summaries expose no category names, every name section's body being exactly the inexpressibility marker --- and therefore equals",
     "The names condition has no ablation site (these summaries expose no category names, every name section's body being exactly the inexpressibility marker) and therefore equals"),
]


def unit_s5():
    for o, n in EMDASH:
        BREP.append([o, n, 1])
    LOGGED.append(dict(unit="s5", file="build", section="appendix prose", old="", new="", note="S5: five em-dash sites (eight dashes) in appendix prose"))


def main_text_span(t):
    a = t.index("\\section{Introduction}")
    b = t.index("\\label{main-text-end}")
    return a, b


def unit_s6():
    u = "s6"
    for which in ("abstract", "body"):
        t = TEXT[which]
        a, b = (0, len(t)) if which == "abstract" else main_text_span(t)
        seg = t[a:b]
        lines = seg.split("\n")
        out = []
        n = 0
        for ln in lines:
            if ln.lstrip().startswith("%"):
                out.append(ln); continue
            for s in ("GPT-4.1", "GPT-5.6"):
                k = ln.count(s) - ln.count("\\mbox{" + s + "}")
                if k:
                    ln = ln.replace("\\mbox{" + s + "}", "\x00").replace(s, "\\mbox{" + s + "}").replace("\x00", "\\mbox{" + s + "}")
                    n += k
            out.append(ln)
        TEXT[which] = t[:a] + "\n".join(out) + t[b:]
        LOGGED.append(dict(unit=u, file=which, section="main text", old="", new="", note=f"S6: {n} \\mbox guards"))


def unit_s7():
    """S7: Figure 2's float source moved from the head of Section 5 to the end of Section 3, so the figure floats to the top of page 4 (applied only if it costs no line)."""
    t = TEXT["body"]
    a = t.index("\\begin{figure}[t]\n\\centering\n%% Writing pass Phase 4b (2026-09-15): Figure 2's source at the head of Section 5")
    b = t.index("\\label{fig:example}\n\\end{figure}\n", a) + len("\\label{fig:example}\n\\end{figure}\n")
    blk = t[a:b]
    assert blk.count("\\begin{figure}") == 1
    t = t[:a] + t[b:]
    anchor = "\\section{Setup}\\label{sec:setup}\n"
    assert t.count(anchor) == 1
    # after the heading, not before it: placed before \section{Setup}, placeins' section barrier flushed the float there and left page 3 nine lines short (measured 23 Sep)
    t = t.replace(anchor, anchor + "%% R139 S7 (2026-09-23): Figure 2's source moved here from the head of Section 5 (page 4's stretched gaps; the float lands at the top of page 4).\n" + blk)
    TEXT["body"] = t
    LOGGED.append(dict(unit="s7", file="body", section="Figure 2", old="", new="", note="S7: Figure 2's source moved to the end of Section 3"))


# ====================================================================================================================== payers
def unit_p1():
    rep("body", "against Opus's $0.90$. Those models score the change question higher. The main-study rubric's scored step asks whether stale content is present, which is not the intent-conditional target of Definition~\\ref{def:coverage}; the explicit-intent rubric asks the defined question. Opus's behaviour under this underspecified prompt differs from compliance with the explicit rule.",
        "against Opus's $0.90$, scoring the change question higher. The main-study rubric's scored step asks whether stale content is present, which is not the intent-conditional target of Definition~\\ref{def:coverage}; the explicit-intent rubric asks the defined question.",
        unit="p1", section="5.3, paragraph 2", note="P1")


def unit_p2():
    rep("body", "The summary's obligation benefit replicates across vendors. On the shared cross-vendor questions, every model whose question-only score varies gains $0.15$ to $0.45$ with the summary, Kimi included. (Appendix~\\ref{app:laddertable})",
        "The summary's obligation benefit replicates across vendors. On the shared questions every model whose question-only score varies gains $0.15$ to $0.45$ with it, Kimi included (Appendix~\\ref{app:laddertable}).",
        unit="p2", section="8, paragraph 1", note="P2 verbatim")


def unit_p3():
    t = TEXT["body"]
    a = t.index("and the name-lookup rule reaches the same level (Table~\\ref{tab:reach}).\n")
    gate = "\\claim{Gating trades budget against licensed-record reach.}\nUnmatched, the always-on fetch spends $1.20$ times the lines per question; truncated to the gated budget it loses licensed records, a reliable $0.04$.\n\n"
    assert t.count(gate) == 1
    rep("body", gate, "", unit="p3", section="7", note="P3: the gating paragraph merged into the fetch paragraph (both numbers kept)")
    rep("body", "and the name-lookup rule reaches the same level (Table~\\ref{tab:reach}).\n",
        "and the name-lookup rule reaches the same level (Table~\\ref{tab:reach}). Unmatched, the always-on fetch spends $1.20$ times the lines per question; truncated to the gated budget it loses licensed records, a reliable $0.04$.\n",
        unit="p3", section="7", note="P3")


def unit_p4():
    rep("body", " Check active duplicates as well as the record originally tagged. The tested view-side rule leaves those copies largely untouched.", "", unit="p4", section="the builders box", note="P4")


def unit_p5():
    rep("body", " Removing every count costs Luna and Opus reliably, and the counts alone still score below the names alone for both.", "", unit="p5", section="5.1, paragraph 3", note="P5")


def unit_p6():
    rep("body", "With the questions rewritten to share no content word with any name in the summary ($115$ pairs), the embedding lookup loses $0.02$ and the two smaller models lose more (Table~\\ref{tab:robust}). On the named state, reworded, mini and Haiku sit below the lookup and Luna, a reader we added later, edges $0.04$ above it on the pooled metric only.",
        "With the questions rewritten to share no content word with any name ($115$ pairs), the embedding lookup loses $0.02$ and the two smaller models lose more and sit below it (Table~\\ref{tab:robust}). Luna, added later, edges $0.04$ above it on the pooled metric only.",
        unit="p6", section="5.2, the rewording paragraph", note="P6: both numbers and the Luna clause kept")


def unit_p7():
    rep("body", " It cannot tell the cancelled hike from the planned one.", "", unit="p7", section="5.2, paragraph 3", note="P7")
    rep("body", " Their scores stay comparable from one question to the next and the fitted reader's do not.", "", unit="p7", section="5.2, paragraph 3", note="P7")


def unit_p8():
    rep("body", "rather than supplying a deployable repair.\n\n\\claim{The tested rule cannot repair copies under different attribute keys.}\nPropagating a lifecycle tag",
        "rather than supplying a deployable repair. Propagating a lifecycle tag", unit="p8", section="7", note="P8: the two copies paragraphs merged; every number kept; 'which leaves the write path' kept (G9)")


def unit_p9():
    t = TEXT["robust"]
    old = ("Pooled AUROC on the counterfactual set unless noted: rows 2 and 5 matched and post hoc ($^{p}$), row 5 on the $60$ counted-state pairs; row 3 the \\pn{} version against its sibling, matched, on the $88$ supersession pairs; "
           "row 7 the $115$ reworded pairs; row 9 the $88$ supersession triples, the lists padded to $60$ names, Opus at one draw against its five-draw row; row 10 the full obligation set. ")
    assert t.count(old) == 1
    TEXT["robust"] = t.replace(old, "")
    LOGGED.append(dict(unit="p9", file="robust_table", section="Table 2 caption", old=old, new="", note="P9: the per-row descriptions to C.2"))
    ins_after("appendix", "it is reported after the paraphrase check.\n",
              "%% R139 payer P9 (2026-09-22): Table 2's per-row notes, moved from its caption.\n"
              "Table~\\ref{tab:robust} reads the pooled AUROC on the counterfactual set unless noted: rows 2 and 5 matched and post hoc (marked $^{p}$), row 5 on the $60$ counted-state pairs; row 3 the \\pn{} version against its sibling, matched, on the $88$ supersession pairs; "
              "row 7 the $115$ reworded pairs; row 9 the $88$ supersession triples, the lists padded to $60$ names, Opus at one draw against its five-draw row; row 10 the full obligation set.\n",
              unit="p9", section="C.2, the registered checks paragraph", note="P9: the notes' home")


def unit_p10():
    u = "p10"
    rep("body", "Count reader, given category$^{c}$ & superseded", "Count reader, given category & superseded", unit=u, section="Table 1", note="P10: the marker with its note")
    rep("body", "Lookup with one count feature$^{b}$ & superseded", "Lookup with one count feature & superseded", unit=u, section="Table 1", note="P10")
    old = (" $^{b}$A logistic reader over the name lookup's similarity and the guessed category's non-active share, fit with personas left out (Table~\\ref{tab:cf-hybrid}). "
           "$^{c}$The two read different quantities: the given-category reader ties every supersession triple and is perfect on the counted states by construction. A dash marks a condition the model did not run.")
    rep("body", old, " A dash marks a condition the model did not run.", unit=u, section="Table 1 notes", note="P10: notes b and c to C.2; note a and the dash sentence stay")
    ins_after("appendix", "it is reported after the paraphrase check.\n",
              "%% R139 payer P10 (2026-09-22): Table 1's notes b and c, moved from its notes.\n"
              "In Table~\\ref{tab:cf-main}, the lookup with one count feature is a logistic reader over the name lookup's similarity and the guessed category's non-active share, fit with personas left out (Table~\\ref{tab:cf-hybrid}); "
              "the two count readers read different quantities: the given-category reader ties every supersession triple and is perfect on the counted states by construction.\n",
              unit=u, section="C.2", note="P10: the notes' home")


def main_text(t_abs, t_body):
    a, b = main_text_span(t_body)
    txt = t_abs + "\n" + t_body[a:b]
    return "\n".join(l for l in txt.split("\n") if not l.lstrip().startswith("%"))


def count_n():
    """AUX-R139-N: the distinct comparisons named by the entries of n_list_r139.json whose fragment is in the final main text; every main-text sentence
    carrying 'reliab' must be covered by an entry (asserted), so a payer that removes a sentence removes its comparisons."""
    assert NL is not None, "reviews/r139/results/n_list_r139.json is missing"
    import re
    mt = " ".join(main_text(TEXT["abstract"], TEXT["body"]).split())
    present = [e for e in NL["entries"] if " ".join(e["fragment"].split()) in mt]
    sents = [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\\])", mt) if re.search(r"\breliab", s) and "\\emph{reliable}" not in s and "multiplicity correction" not in s]
    unc = [s for s in sents if not any(" ".join(e["fragment"].split()) in s for e in NL["entries"])]
    assert not unc, "main-text sentences with 'reliab' not in the comparison list: " + " || ".join(x[:140] for x in unc)
    comps = sorted({c for e in present for c in e["comparisons"]})
    (RES / "n_count_r139.json").write_text(json.dumps(dict(n_distinct=len(comps), entries_present=[e["fragment"] for e in present], comparisons=comps), indent=1), encoding="utf-8", newline="\n")
    return len(comps)


def unit_b3m():
    """The ruling's fallback after P10: B3's clause moves to C.2 (the length-only reader's paragraph) with a pointer in 5.2."""
    L = PR["lists"]
    b3 = (f"At these lengths, ${L['pn_mean_printed']}$ names on average and at most ${L['pn_max']}$, the lookup is close to a string match against one or two candidates (Table~\\ref{{tab:cf-emptiness}}; FR-Bank's own lists in Appendix~\\ref{{app:census}}). ")
    rep("body", b3 + "With the superseded-name list padded to $60$ names (Table~\\ref{tab:robust}),",
        "With the superseded-name list padded to $60$ names (Table~\\ref{tab:robust}; the default lengths in Appendix~\\ref{app:length}),", unit="b3m", section="5.2", note="B3 moved to C.2 (the ruling's fallback), a pointer left")
    rep("appendix", "\\paragraph{The length-only reader, post hoc.}\\label{app:length}\n",
        "\\paragraph{The length-only reader, post hoc.}\\label{app:length}\n"
        f"The default lists are short: the \\pn{{}} version's superseded list holds ${L['pn_mean_printed']}$ names on average and at most ${L['pn_max']}$ on the supersession triples, and ${L['present_empty']}$ of the ${L['n']}$ \\present{{}} lists are empty; "
        "at these lengths the lookup is close to a string match against one or two candidates (Table~\\ref{tab:cf-emptiness}; FR-Bank's own lists in Appendix~\\ref{app:census}).\n",
        unit="b3m", section="C.2", note="B3's clause, moved")


def unit_g8():
    """G8 (the rulings of 22 Sep, 23:54): Section 7's two answer-outcome sentences become exploratory pointers."""
    rep("body", "The flagged stale answers trace to these untagged copies even when the forbidding record is present and tagged.",
        "The answers the exploratory detector flags trace to these untagged copies even when the forbidding record is present and tagged (Appendix~\\ref{app:resp}).", unit="g8", section="7", note="G8")
    rep("body", "so it diagnoses a source of stale use rather than supplying a deployable repair.", "so it diagnoses where the copies sit rather than supplying a deployable repair.", unit="g8", section="7", note="G8")


def unit_q1():
    rep("body", "on explicit intent questions and, on the pooled metric only, in the all-states comparison and under FR-Bank's store-written summary, where Haiku sits $0.12$ above the lookup, and in the scenario we priced, a model call before every query cost more than the retrieval it saved (Appendix~\\ref{app:utility-completion}).",
        "on explicit intent questions and, pooled only, in two further conditions (Sections~\\ref{sec:lookup} and~\\ref{sec:backends}), and a model call before every query cost more than the retrieval it saved (Appendix~\\ref{app:utility-completion}).",
        unit="q1", section="the builders box", note="Q1 (0.12 stays in E.9, the priced scenario in G.5)")


def unit_q2():
    rep("body", " Scores collapse onto a few low values, with positives slightly below negatives, and the trigger remains unresolved.", "", unit="q2", section="6", note="Q2 (E.7 has it)")
    rep("appendix", "What the summary does to the score is a collapse onto a few low values, with the positives averaging slightly below the negatives (Table~\\ref{tab:dist}).\n",
        "What the summary does to the score is a collapse onto a few low values, with the positives averaging slightly below the negatives (Table~\\ref{tab:dist}).\n"
        "%% R139 Q2 (2026-09-23, the author's approval): the pinned claim U5, moved verbatim from Section 6.\n"
        "Scores collapse onto a few low values, with positives slightly below negatives, and the trigger remains unresolved.\n",
        unit="q2", section="E.7", note="Q2: U5 verbatim in E.7 (approved 23 Sep morning)")


def unit_q3():
    rep("body", "and two of five do when it is padded to $60$ names; the lookup loses $0.02$ when the questions are reworded to share no word with the names.",
        "and two of five do when it is padded to $60$ names.", unit="q3", section="1, bullet 2", note="Q3 (the abstract and 5.2 carry it)")


def unit_q4():
    rep("body", " A reader that merely counts tagged lines scores $0.62$ under either tag source.", "", unit="q4", section="7", note="Q4 (E.10 and G.4 have it)")


def unit_q5():
    rep("body", "We change no backend's write path: the counterfactual test bypasses writing, every intervention is on the read side, and no backend tested here is shown maintaining the summary. "
                "The reach and answer results therefore describe what a store as shipped affords a reader, not what a repaired one would; a write-path intervention is a separate study.",
        "We change no backend's write path: the counterfactual test bypasses writing, every intervention is read-side, and no backend tested here is shown maintaining the summary, "
        "so the reach results describe what a store as shipped affords a reader; a write-path intervention is a separate study.", unit="q5", section="9", note="Q5: G9 tightened")


def unit_q6():
    rep("body", "This section scores what each policy brings into a reader's view, the reach of the forbidding record, not what an answerer does with it; the exploratory answer stage is in Appendix~\\ref{app:resp}.\n", "",
        unit="q6", section="7", note="Q6: G5's opening sentence dropped; the title stays")
    rep("body", "Haiku's score with both stays within tolerance of its summary alone.", "Haiku's score with both stays within tolerance of its summary alone; answers are not scored here (Appendix~\\ref{app:resp}).",
        unit="q6", section="7, first paragraph", note="Q6")


def unit_q7():
    rep("body", "The counterfactual comparison covers closed models from two vendors; the one open-weights model, Kimi K3, completed only the cross-vendor replication.",
        "Kimi K3, the one open-weights model, completed only the cross-vendor replication.", unit="q7", section="9", note="Q7")


def unit_q8():
    rep("body", " comparisons the main text makes on its own, and each registered family holds five readers (three under the all-states summary).", " comparisons the main text makes on its own.",
        unit="q8", section="4", note="Q8: A2's second clause to E.4 (clears rule V)")
    rep("appendix", "Items are nested within the $40$ personas.\n",
        "Items are nested within the $40$ personas.\n%% R139 Q8 (2026-09-23): A2's second clause, moved from Section 4.\nEach registered family of model-minus-lookup comparisons holds five readers (three under the all-states summary).\n",
        unit="q8", section="E.4", note="Q8: the clause's home")


def unit_q9():
    rep("body", "We study the monitoring side of that distinction only: how accurately a reader judges the store from what it exposes. Whether the judgment then changes what is retrieved or answered is control, and we leave it to a later study.",
        "Metamemory separates monitoring a state from controlling its use \\citep{nelson1990}; we study monitoring only, how accurately a reader judges the store from what it exposes. Whether the judgment then changes what is retrieved or answered is control, which we leave to a later study.",
        unit="q9", section="1", note="Q9: G3 with its own antecedent")
    rep("body", "Metamemory separates monitoring a memory state from controlling its use \\citep{nelson1990,koriat1996}. We apply that distinction to an external store:",
        "We apply that distinction to an external store \\citep{koriat1996}:", unit="q9", section="2", note="Q9: the duplicate first sentence dropped; Koriat and Goldsmith moved onto the next")


ORDER[ORDER.index("g") + 1:ORDER.index("g") + 1] = ["g8"]
ORDER.append("b3m")
ORDER += ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9"]


# ====================================================================================================================== the last three lines (rulings of 23 Sep, morning)
def unit_r1():
    rep("body", "Models differ further when the rubric states the intent rule.\n", "", unit="r1", section="1", note="R1 (5.3 has it)")


def unit_r2():
    rep("body", " The default name lookup reads the superseded list, so it ties the versions.", "", unit="r2", section="Figure 2 caption", note="R2 (5.2 states it)")


def unit_r3():
    rep("body", "{\\scriptsize The \\textsc{change} intent is never \\pn{}, because both the old and the new value are licensed; n.a.\\ means a combination the question construction never produces.}",
        "{\\scriptsize \\textsc{change} is never \\pn{}, since both values are licensed; n.a.: a combination the question construction never produces.}", unit="r3", section="3, Definition 1's note", note="R3")


def unit_r4():
    b1 = PR["b1"]
    old = f"and only mini reliably below. Pooled, the lookup scores ${b1['lookup']}$ and the three ${b1['lo']}$ to ${b1['hi']}$, none reliably above it."
    rep("body", old, f"and only mini reliably below (pooled: ${b1['lookup']}$ against ${b1['lo']}$ to ${b1['hi']}$, none reliable; Appendix~\\ref{{app:counterfactual}}).", unit="r4", section="5.2", note="R4: B1 as a clause")


def unit_r5():
    rep("body", "For Mem0 and A-MEM we also render the manifest under each backend's constraints; this constrained rendering is ours and differs from a summary built from their own fields.",
        "For Mem0 and A-MEM we also render the manifest under each backend's constraints; that rendering is ours, not theirs.", unit="r5", section="4", note="R5")


def unit_r6():
    rep("body", " What differs across readers is which of the two they use.", "", unit="r6", section="5.1", note="R6")


def unit_r7():
    rep("body", "Cancelling the hike can therefore move a retraction count from zero to one without placing the hike's name in a retracted-name list. Naming that state exposes which attribute the count concerns.",
        "Cancelling the hike therefore moves a retraction count without naming the hike; naming the state exposes which attribute the count concerns.", unit="r7", section="3", note="R7")


def unit_r8():
    """R8: S6's guards removed except the Limitations one that fixed the 'GPT-' / '4.1 mini' break."""
    keep = "from one model family. \\mbox{GPT-4.1} mini drafted the questions"
    for which in ("abstract", "body"):
        t = TEXT[which]
        if which == "body":
            assert t.count(keep) == 1
            t = t.replace(keep, "@@KEEP@@")
        n = t.count("\\mbox{GPT-4.1}") + t.count("\\mbox{GPT-5.6}")
        t = t.replace("\\mbox{GPT-4.1}", "GPT-4.1").replace("\\mbox{GPT-5.6}", "GPT-5.6")
        if which == "body":
            t = t.replace("@@KEEP@@", keep)
        TEXT[which] = t
        LOGGED.append(dict(unit="r8", file=which, section="main text", old="", new="", note=f"R8: {n} \\mbox guards removed (the Limitations one kept)"))


def unit_r9():
    rep("body", "On a named state no model reliably exceeds the name lookup on the short list, with list length kept fixed or not;",
        "On a named state no model reliably exceeds the name lookup on the short list;", unit="r9", section="10", note="R9")


def unit_rm():
    rep("body", "The pad is identical across a triple. The \\pn{} list is one to three names longer", "The pad is identical across a triple, and the \\pn{} list is one to three names longer",
        unit="rm", section="5.2", note="the ruled merge (never dropped)")


ORDER += ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "rm"]
UNITS = {k: globals()[f"unit_{k}"] for k in ORDER}


def main():
    arg = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--units=")), "")
    if arg == "close":
        units = CLOSE_UNITS.read_text(encoding="utf-8").split()
    else:
        units = [u for u in arg.split(",") if u]
    assert all(u in UNITS for u in units), f"unknown unit in {units}"
    assert units == [u for u in ORDER if u in units], f"units must be in the order {ORDER}"
    if "--no-refresh" not in sys.argv:
        r = subprocess.run([sys.executable, str(V23 / "tools" / "port_r137.py"), "--units=close"], capture_output=True, text=True)
        assert r.returncode == 0, r.stdout[-800:] + r.stderr[-800:]
    # files outside the regenerated sources: restored from the R137 close before the units run
    REFCHECK.write_bytes(subprocess.run(["git", "show", f"{BASE_COMMIT}:iclr2027_monitoring_submission/tools/refcheck_v11.py"], cwd=ROOT, capture_output=True, check=True).stdout)
    TEXT.update(body=rd(BODY), abstract=rd(ABS), appendix=rd(APPX), robust=rd(ROBUST), refcheck=rd(REFCHECK))
    for u in units:
        UNITS[u]()
        print(f"unit {u}: applied ({sum(1 for r in LOGGED if r['unit'] == u)} edits)")
    if "@@N@@" in TEXT["body"]:
        TEXT["body"] = TEXT["body"].replace("@@N@@", str(count_n()))   # --no-n: drafting only, never built for a gate
    wr(BODY, TEXT["body"]); wr(ABS, TEXT["abstract"]); wr(APPX, TEXT["appendix"]); wr(ROBUST, TEXT["robust"])
    if "s2" in units:
        wr(REFCHECK, TEXT["refcheck"])
    RES.mkdir(parents=True, exist_ok=True)
    BUILD_REPAIRS.write_text(json.dumps(BREP, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    LOG.write_text(json.dumps(dict(units=units, edits=LOGGED), indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"-> {len(LOGGED)} edits logged")


if __name__ == "__main__":
    main()
