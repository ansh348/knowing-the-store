# -*- coding: utf-8 -*-
"""appendix_r131.py -- program R131 (2026-09-20; the author's brief 'KtS R131: land R125 in the body', section H): the appendix edits, applied to
reviews/v22/src/appendix_v22.tex after appendix_r129.py (regeneration order: cp v21 -> appendix_r126.py -> appendix_r128.py -> appendix_r129.py ->
appendix_r131.py -> fig3_data.py -> fig3_data_r131.py -> port_v22.py -> port_r131.py). Every edit is asserted (rep); every number is read from its
artifact under reviews/r125/results/ (r125_matched.json, r125_t2_emptiness.json, r125_t3_frbank.json, r125_t3_graphiti.json, r125_t4_sibling.json,
r125_t5_nc.json; the ledger is r82_counterfactual/cf2/NUMBERS_CF2.md section 15; the printed two-decimal forms reviews/NUMBERS_R131.md).
  C.2  E2 Amendment 1's table (tab:cf-nc-strong; P-N3, P-N4, P-N5; Sol's lane not run) after tab:cf-names-counts
  C.2  the matched metric: tab:cf-matched (Table 1's readers, both metrics, both intervals, per state), tab:cf-classes (the pooled AUROC by pair
       class), tab:cf-matched-vs (each reader minus its lookup; minus the count readers), tab:cf-matched-ablations (the E2 and moved-count rows under
       the matched metric), the pooled Figure 3 (fig:perstate-pooled), the list-emptiness census and random-token rows (tab:cf-emptiness)
  C.2  tab:cf-hybrid gains a matched panel; the sibling-name control (tab:cf-sibling; P-SB1 to P-SB4 with the pre-freeze disclosure)
  E.9  what the store is in each scored condition; tab:levels-strata (the FR-Bank rows re-scored per stratum)
  G.4  tab:graphiti-strata (the Graphiti rows re-scored per stratum)
  F    the two registrations in tab:registrations-d; the count paragraph (98 predictions, 31 otherwise; P-SB1 and P-SB3 not counted)
  the reader's guide pointers
Usage: python reviews/v22/tools/appendix_r131.py [--check]
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
APPX = ROOT / "reviews" / "v22" / "src" / "appendix_v22.tex"
R125 = ROOT / "reviews" / "r125" / "results"
M = json.load(open(R125 / "r125_matched.json", encoding="utf-8"))
T2 = json.load(open(R125 / "r125_t2_emptiness.json", encoding="utf-8"))
T3F = json.load(open(R125 / "r125_t3_frbank.json", encoding="utf-8"))
T3G = json.load(open(R125 / "r125_t3_graphiti.json", encoding="utf-8"))
T4 = json.load(open(R125 / "r125_t4_sibling.json", encoding="utf-8"))
T5 = json.load(open(R125 / "r125_t5_nc.json", encoding="utf-8"))
RD, PD = M["readers"], M["paired"]
ST = ("SUPERSESSION", "RETRACTION", "EXPIRY")
HDR = "%% R131 (2026-09-20): written by reviews/v22/tools/appendix_r131.py from reviews/r125/results/{}; r82_counterfactual/cf2/NUMBERS_CF2.md section {}; do not edit by hand.\n"


def rep(t, old, new, n=1, where=""):
    assert t.count(old) == n, (where, t.count(old), n, old[:100])
    return t.replace(old, new)


def f4(x):
    return f"${x:.4f}$"


def s4(x):
    return f"${x:+.4f}$"


def iv(d, signed=True):
    lo, hi = d["ci_lo"], d["ci_hi"]
    return f"$[{lo:+.4f},{hi:+.4f}]$" if signed else f"$[{lo:.4f},{hi:.4f}]$"


def ivp(d):   # a paired difference: delta with its two intervals
    return f"{s4(d['delta'])} {iv(d['ci_triple'])}; {iv(d['ci_persona'])}"


def ivq(d):   # a pooled paired difference (item_ci / persona_ci)
    return f"{s4(d['delta'])} {iv(d['item_ci'])}; {iv(d['persona_ci'])}"


def wtl(x):
    return f"${x['W']}/{x['T']}/{x['L']}$"


def star(d):
    return "$^{*}$" if d["both_exclude_zero"] else ""


# ------------------------------------------------------------------------------------------------------------------------------ C.2: E2 Amendment 1
def nc_strong_table():
    rows = []
    for key, name in (("GPT-5.6 Luna (draw 1)", "GPT-5.6 Luna, draw 1"), ("GPT-5.6 Luna (five draws)", "GPT-5.6 Luna, five draws"), ("GPT-5.6 Sol (draw 1)", "GPT-5.6 Sol, draw 1"), ("Opus 5 (draw 1)", "Opus 5, draw 1")):
        r = T5["readers"][key]
        if "status" in r:
            rows.append(f"{name} & not run & \\multicolumn{{7}}{{l}}{{dropped by the registration's budget rule (the caption); its moved-count response is in Table~\\ref{{tab:v2rcat}}}} \\\\\n")
            continue
        no, co = r["names_only"], r["counts_only"]
        rows.append(f"{name} & intact (recorded) & {f4(r['intact_pooled'])} & & & & & & \\\\\n")
        for lab, x in (("names only", no), ("counts only", co)):
            d = x["minus_intact"]; cm = x["matched"]["per_state"]
            rows.append(f" & {lab} & {f4(x['pooled']['whole'])} & {s4(d['delta'])}{star(d)} & {iv(d['item_ci'])} & {iv(d['persona_ci'])} & {f4(x['matched']['whole']['matched'])} & "
                        f"{f4(cm['RETRACTION']['matched'])} & {f4(cm['EXPIRY']['matched'])} \\\\\n")
        d = r["counts_minus_names"]
        rows.append(f" & counts minus names & & {s4(d['delta'])}{star(d)} & {iv(d['item_ci'])} & {iv(d['persona_ci'])} & & & \\\\\n\\addlinespace[1pt]\n")
    P = T5["predictions"]
    return (HDR.format("r125_t5_nc.json", "15e (AUX-CF2-R125-NC-*)") +
            "\\begin{table}[H]\n"
            "\\caption{Names against counts on the three stronger models (E2, Amendment 1; registered, ADDENDUM\\_R125\\_E2\\_AMENDMENT\\_1). E2's two renderings, byte-identical to Table~\\ref{tab:cf-names-counts}'s, on Opus 5 (one draw, Batch), GPT-5.6 Luna (five draws through the raw API; its one-draw reading beside) and GPT-5.6 Sol (one draw; not run, see below): the pooled AUROC (its persona interval is in the ledger), the paired difference from the recorded intact row with both intervals ($^{*}$ both exclude zero), counts only minus names only, and the renderings under the matched metric, the whole set and the two counted states (ret., exp.; their persona intervals are in the ledger, P-N5's two failing lower bounds below). "
            f"Three predictions: P-N3, names only within tolerance of the intact row at the point, {P['P-N3']['verdict'].lower()} (GPT-5.6 Luna ${P['P-N3']['per_model']['GPT-5.6 Luna (five draws)']['delta']:+.4f}$; Opus 5 ${P['P-N3']['per_model']['Opus 5 (draw 1)']['delta']:+.4f}$, within the band); "
            f"P-N4, counts only reliably below names only, {P['P-N4']['verdict'].lower()}; P-N5, counts only above $0.50$ on both counted states under the matched metric with the persona interval excluding $0.50$, {P['P-N5']['verdict'].lower()} (Opus 5 reads ${P['P-N5']['per_model']['Opus 5 (draw 1)']['RETRACTION']['matched']:.4f}$ on retraction; GPT-5.6 Luna's expiry lower bound is ${P['P-N5']['per_model']['GPT-5.6 Luna (five draws)']['EXPIRY']['persona_lo']:.4f}$). "
            "GPT-5.6 Sol's lane was dropped by the registration's own rule when the vendor's projection for this task and the sibling-name control together exceeded the cap, so its rows print as not run.}\n"
            "\\label{tab:cf-nc-strong}\n"
            "\\centering\\tiny\\setlength{\\tabcolsep}{1.5pt}\n"
            "\\begin{tabular}{@{}llrrllrll@{}}\n\\toprule\n"
            "Reader & summary & AUROC & minus intact & item interval & persona interval & matched & ret. & exp. \\\\\n\\midrule\n"
            + "".join(rows) + "\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def nc_strong_prose():
    L5 = T5["readers"]["GPT-5.6 Luna (five draws)"]; O = T5["readers"]["Opus 5 (draw 1)"]
    return ("\\paragraph{Names against counts on the three stronger models.}\n"
            "%% R131 (2026-09-20): E2 Amendment 1 (R125 Task 5; AUX-CF2-R125-NC-*).\n"
            "The same two renderings were run on the three stronger models after the matched metric had been read (Table~\\ref{tab:cf-nc-strong}).\n"
            f"Removing every count costs GPT-5.6 Luna {s4(L5['names_only']['minus_intact']['delta'])} and Opus 5 {s4(O['names_only']['minus_intact']['delta'])} on the pooled metric, each with both intervals clear of zero, so the prediction that names alone would sit within tolerance of the intact row came out otherwise for Luna and held for Opus 5 at the point.\n"
            f"Counts alone still score reliably below names alone for both, by {s4(L5['counts_minus_names']['delta'])} and {s4(O['counts_minus_names']['delta'])}, as predicted.\n"
            f"Under the matched metric counts alone read {f4(O['counts_only']['matched']['per_state']['RETRACTION']['matched'])} on retraction for Opus 5 and {f4(L5['counts_only']['matched']['per_state']['EXPIRY']['matched'])} on expiry for Luna with the persona interval reaching below $0.50$, so the third prediction came out otherwise for both.\n"
            "GPT-5.6 Sol was not run: after the sibling-name control's lanes the re-projected cost of its names-and-counts lane would have taken the vendor's total over the cap, and the registration drops the lane in that case.\n\n")


# ------------------------------------------------------------------------------------------------------------------------------ C.2: the matched metric
V2 = [("LOOKUP_v2", "Name lookup"), ("MINI1_v2", "GPT-4.1 mini, one draw"), ("MINI5_v2", "GPT-4.1 mini, five draws"), ("H45_v2", "Haiku 4.5"), ("LUNA_v2", "GPT-5.6 Luna"),
      ("SOL_v2", "GPT-5.6 Sol"), ("OP5_v2", "Opus 5"), ("CR-nb1_v2", "Count reader, guessed category"), ("CR-oracle-a_v2", "Count reader, given category"),
      ("CR-oracle-state_v2", "State-aware count reader"), ("CR-oracle-share_v2", "Category-given share reader"), ("HYBRID_v2", "Lookup with one count feature"),
      ("RANDTOK_v2", "Random-token lookup"), ("WHOLEMAP_v2", "Whole name-map lookup")]
V3 = [("ALLSTATES_v3", "Name lookup, all states"), ("MINI1_v3", "GPT-4.1 mini, one draw"), ("MINI5_v3", "GPT-4.1 mini, five draws"), ("H45_v3", "Haiku 4.5"),
      ("OP5_v3", "Opus 5"), ("OP5_v3_d1", "Opus 5, draw 1"), ("RANDTOK_v3", "Random-token lookup")]


def matched_row(key, name):
    r = RD[key]; p = r["pn_vs_present"]; w = p["whole"]; a = r["pn_vs_absent"]["whole"]
    per = " / ".join(f4(p["per_state"][s]["matched"]) for s in ST)
    return f"{name} & {f4(r['pooled']['whole'])} & {f4(r['pooled']['state_balanced'])} & {wtl(w)} & {f4(w['matched'])} & {iv(w['ci_triple'], False)} & {iv(w['ci_persona'], False)} & {per} & {f4(a['matched'])} \\\\\n"


def matched_table():
    cov = M["coverage_only"]
    rows = [matched_row(k, n) for k, n in V2]
    rows.append(f"Coverage-only reader & {f4(cov['pooled']['whole'])} & {f4(cov['pooled']['state_balanced'])} & {wtl(cov['pn_vs_present'])} & {f4(cov['pn_vs_present']['matched'])} & -- & -- & -- & {f4(cov['pn_vs_absent']['matched'])} \\\\\n")
    rows3 = [matched_row(k, n) for k, n in V3]
    return (HDR.format("r125_matched.json", "15 (AUX-CF2-R125-MATCHED-V2, -V3, -PERSTATE)") +
            "\\begin{table}[H]\n"
            "\\caption{Every reader of Table~\\ref{tab:cf-main} under both metrics (post hoc; the matched metric was defined after the pooled rows were known). Pooled: the recorded AUROC over the $444$ items, and the mean of the three per-state pooled values (state-balanced). Matched: W/T/L counts the triples in which the reader scores the \\pn{} version above, equal to, or below the \\present{} version (ties exact equality of the collapsed scores), and the matched AUROC is $(W+T/2)/148$, with the triple-level and the persona-grouped bootstrap interval ($1{,}000$ draws) and the per-state values over each state's own triples ($88$ / $30$ / $30$); the last column is the same comparison against the \\absent{} version. The lookups and the count readers never lose a triple, so their matched values are half their tie counts plus their wins; GPT-4.1 mini's five-draw row loses $33$ triples where its one-draw row loses $10$, so it sits lower on this metric and higher on the pooled one.}\n"
            "\\label{tab:cf-matched}\n"
            "\\centering\\tiny\\setlength{\\tabcolsep}{1pt}\n"
            "\\begin{tabular}{@{}lrrrrllcr@{}}\n\\toprule\n"
            "Reader & pooled & state-balanced & W/T/L & matched & triple interval & persona interval & matched sup.\\ / ret.\\ / exp. & vs \\absent{} \\\\\n\\midrule\n"
            "\\multicolumn{9}{@{}l}{\\textit{The default summary (superseded content named)}}\\\\\n" + "".join(rows) +
            "\\addlinespace[2pt]\\multicolumn{9}{@{}l}{\\textit{The summary naming all states}}\\\\\n" + "".join(rows3) +
            "\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def classes_table():
    def row(key, name):
        pc = RD[key]["pair_classes"]["whole"]
        return f"{name} & {f4(pc['pooled'])} & {f4(pc['within_triple']['auroc'])} & {f4(pc['same_state_across_questions']['auroc'])} & {f4(pc['across_states']['auroc'])} \\\\\n"
    pc = RD["LOOKUP_v2"]["pair_classes"]["whole"]
    n1, n2, n3, nt = pc["within_triple"]["pairs"], pc["same_state_across_questions"]["pairs"], pc["across_states"]["pairs"], pc["pairs_total"]
    return (HDR.format("r125_matched.json", "15 (AUX-CF2-R125-CLASSES)") +
            "\\begin{table}[H]\n"
            f"\\caption{{The pooled AUROC decomposed by pair class (post hoc). Of the ${nt:,}$ positive-negative pairs the pooled AUROC averages over, ${n1}$ are within a triple, ${n2:,}$ pair a positive with a negative of the same state from another question, and ${n3:,}$ cross states; the pooled value is the pair-count-weighted mean of the three class AUROCs (asserted for every reader). The within-triple class is the matched metric's two comparisons pooled. Readers as in Table~\\ref{{tab:cf-matched}}.}}\n"
            "\\label{tab:cf-classes}\n"
            "\\centering\\scriptsize\\setlength{\\tabcolsep}{3pt}\n"
            "\\begin{tabular}{@{}lrrrr@{}}\n\\toprule\n"
            f"Reader & pooled & within a triple (${n1}$) & same state, across questions (${n2:,}$) & across states (${n3:,}$) \\\\\n\\midrule\n"
            "\\multicolumn{5}{@{}l}{\\textit{The default summary}}\\\\\n" + "".join(row(k, n) for k, n in V2) +
            "\\addlinespace[2pt]\\multicolumn{5}{@{}l}{\\textit{The summary naming all states}}\\\\\n" + "".join(row(k, n) for k, n in V3) +
            "\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def vs_table():
    MODELS = (("MINI1_v2", "GPT-4.1 mini, one draw"), ("MINI5_v2", "GPT-4.1 mini, five draws"), ("H45_v2", "Haiku 4.5"), ("LUNA_v2", "GPT-5.6 Luna"), ("SOL_v2", "GPT-5.6 Sol"), ("OP5_v2", "Opus 5"),
              ("HYBRID_v2", "Lookup with one count feature"), ("CR-nb1_v2", "Count reader, guessed category"), ("RANDTOK_v2", "Random-token lookup"),
              ("MINI5_v3", "GPT-4.1 mini, five draws, all states"), ("H45_v3", "Haiku 4.5, all states"), ("OP5_v3", "Opus 5, all states"), ("OP5_v3_d1", "Opus 5, draw 1, all states"))
    a, b = [], []
    for key, name in MODELS:
        v = PD["vs_lookup"][key]["pn_vs_present"]; w = v["whole"]; s_ = v["per_state"]["SUPERSESSION"]
        a.append(f"{name} & {s4(w['delta'])}{star(w)} & {iv(w['ci_triple'])} & {iv(w['ci_persona'])} & {s4(v['per_state']['RETRACTION']['delta'])} & {s4(v['per_state']['EXPIRY']['delta'])} \\\\\n")
        b.append(f"{name} & {s4(s_['delta'])}{star(s_)} & {iv(s_['ci_triple'])} & {iv(s_['ci_persona'])} \\\\\n")
    c, d = [], []
    for key, name in (("LOOKUP_v2", "Name lookup"), ("MINI1_v2", "GPT-4.1 mini, one draw"), ("MINI5_v2", "GPT-4.1 mini, five draws"), ("H45_v2", "Haiku 4.5"), ("LUNA_v2", "GPT-5.6 Luna"), ("SOL_v2", "GPT-5.6 Sol"), ("OP5_v2", "Opus 5"), ("HYBRID_v2", "Lookup with one count feature")):
        g = PD["vs_count_readers"][key]["CR-nb1"]["pn_vs_present"]; o = PD["vs_count_readers"][key]["CR-oracle-a"]["pn_vs_present"]
        for st, lab in (("RETRACTION", "retraction"), ("EXPIRY", "expiry")):
            nm = name if st == "RETRACTION" else ""
            c.append(f"{nm} & {lab} & {s4(g[st]['delta'])}{star(g[st])} & {iv(g[st]['ci_triple'])} & {iv(g[st]['ci_persona'])} \\\\\n")
            d.append(f"{nm} & {lab} & {s4(o[st]['delta'])}{star(o[st])} & {iv(o[st]['ci_triple'])} & {iv(o[st]['ci_persona'])} \\\\\n")
    return (HDR.format("r125_matched.json", "15 (AUX-CF2-R125-VS-LOOKUP, -VS-COUNT, -OP5-V3)") +
            "\\begin{table}[H]\n"
            "\\caption{Paired differences under the matched metric (post hoc): the mean over triples of the two readers' per-triple outcomes (a win $1$, a tie $\\tfrac12$, a loss $0$), with the triple-level and the persona-grouped interval; $^{*}$ marks a difference with both intervals clear of zero. First panel: each reader minus its summary's lookup on the whole set, with the point differences on the two counted states (the lookup ties every counted-state triple under the default summary); second panel: the same on supersession. Under the all-states summary Opus 5's lead over its lookup is not reliable at five draws and is at its first draw alone. Third and fourth panels: each reader minus the guessed-category and the given-category count reader on the counted states; a difference of $-0.5000$ against the given-category reader means that reader won every triple the other tied.}\n"
            "\\label{tab:cf-matched-vs}\n"
            "\\centering\\tiny\\setlength{\\tabcolsep}{2pt}\n"
            "\\begin{tabular}{@{}lrllrr@{}}\n\\toprule\n"
            "Reader minus its lookup, whole set & difference & triple interval & persona interval & retraction & expiry \\\\\n\\midrule\n" + "".join(a) +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}lrll@{}}\n\\toprule\n"
            "Reader minus its lookup, supersession & difference & triple interval & persona interval \\\\\n\\midrule\n" + "".join(b) +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}llrll@{}}\n\\toprule\n"
            "Reader minus the guessed-category count reader & state & difference & triple interval & persona interval \\\\\n\\midrule\n" + "".join(c) +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}llrll@{}}\n\\toprule\n"
            "Reader minus the given-category count reader & state & difference & triple interval & persona interval \\\\\n\\midrule\n" + "".join(d) +
            "\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def ablations_table():
    def level(key, name):
        p = RD[key]["pn_vs_present"]
        return f"{name} & {wtl(p['whole'])} & {f4(p['whole']['matched'])} & " + " & ".join(f4(p["per_state"][s]["matched"]) for s in ST) + " \\\\\n"

    SC = {"whole": "whole set", "sup": "supersession", "ret": "retraction", "exp": "expiry", "counted": "counted states"}

    def con(name, label, scopes):
        c = PD["contrasts"][name]["pn_vs_present"]
        return "".join(f"{label if i == 0 else ''} & {SC[sc]} & {s4(c[sc]['delta'])}{star(c[sc])} & {iv(c[sc]['ci_triple'])} & {iv(c[sc]['ci_persona'])} \\\\\n" for i, sc in enumerate(scopes))
    lev = [level(k, n) for k, n in (("MINI1_NAMES", "GPT-4.1 mini, names only"), ("MINI1_NAMES_DASH", "GPT-4.1 mini, names only, dash rule"), ("MINI1_COUNTS", "GPT-4.1 mini, counts only"),
                                    ("H45_NAMES", "Haiku 4.5, names only"), ("H45_COUNTS", "Haiku 4.5, counts only"),
                                    ("MINI1_v2r", "GPT-4.1 mini, totals randomized"), ("H45_v2r", "Haiku 4.5, totals randomized"), ("OP5_v2r", "Opus 5, totals randomized"),
                                    ("MINI1_v2rcat", "GPT-4.1 mini, moved count"), ("H45_v2rcat", "Haiku 4.5, moved count"), ("OP5_v2rcat", "Opus 5, moved count (five draws)"),
                                    ("LUNA_v2rcat", "GPT-5.6 Luna, moved count (five draws)"), ("SOL_v2rcat", "GPT-5.6 Sol, moved count (five draws)"), ("CR-oracle-state_v2rcat", "State-aware count reader, moved count"))]
    c1 = "".join(con(n, l, ("whole", "sup", "counted")) for n, l in (("E2 mini names-only minus intact", "GPT-4.1 mini, names only minus intact"), ("E2 mini counts-only minus names-only", "GPT-4.1 mini, counts only minus names only"),
                                                                    ("E2 Haiku names-only minus intact", "Haiku 4.5, names only minus intact"), ("E2 Haiku counts-only minus names-only", "Haiku 4.5, counts only minus names only")))
    c1 += "".join(con(n, l, ("whole",)) for n, l in (("totals rand. mini minus sup-only", "GPT-4.1 mini, totals randomized minus intact"), ("totals rand. Haiku minus sup-only", "Haiku 4.5, totals randomized minus intact"), ("totals rand. Opus minus sup-only", "Opus 5, totals randomized minus intact")))
    c2 = "".join(con(n, l, ("whole", "ret", "exp", "counted")) for n, l in (("moved count mini minus sup-only", "GPT-4.1 mini, moved count minus intact"), ("moved count Haiku minus sup-only", "Haiku 4.5, moved count minus intact"),
                                                                            ("moved count Opus k5 minus sup-only k5", "Opus 5, moved count minus intact (five against five draws)"),
                                                                            ("moved count Luna k5 minus sup-only k5 (E9)", "GPT-5.6 Luna, moved count minus intact (five against five)"),
                                                                            ("moved count Sol k5 minus sup-only k5 (E9)", "GPT-5.6 Sol, moved count minus intact (five against five)")))
    c2 += "".join(con(n, l, ("whole", "counted")) for n, l in (("all-states mini k5 minus sup-only", "GPT-4.1 mini, five draws, all states minus default"), ("all-states Haiku minus sup-only", "Haiku 4.5, all states minus default"),
                                                               ("all-states Opus minus sup-only", "Opus 5, all states minus default"), ("all-states lookup minus name lookup", "Name lookup, all states minus default")))
    o = PD["opus_v3_vs_allstates"]
    c3 = []
    for key, label in (("OP5_v3", "Opus 5, five draws"), ("OP5_v3_d1", "Opus 5, draw 1")):
        p = o[key]["pn_vs_present"]
        for i, (sc, x) in enumerate((("whole set", p["whole"]), ("supersession", p["per_state"]["SUPERSESSION"]), ("retraction", p["per_state"]["RETRACTION"]), ("expiry", p["per_state"]["EXPIRY"]))):
            c3.append(f"{label if i == 0 else ''} & {sc} & {s4(x['delta'])}{star(x)} & {iv(x['ci_triple'])} & {iv(x['ci_persona'])} \\\\\n")
    return (HDR.format("r125_matched.json", "15 (AUX-CF2-R125-MATCHED-V2, -V2R, -V2RCAT, -PERSTATE, -CONTRASTS, -OP5-V3)") +
            "\\begin{table}[H]\n"
            "\\caption{The ablations under the matched metric (post hoc). Upper panel: the names-only, counts-only, totals-randomized and moved-count rows, W/T/L against the \\present{} version and the matched AUROC, whole set and per state (Tables~\\ref{tab:cf-names-counts} and~\\ref{tab:v2rcat} carry the pooled rows). Middle panels: the paired contrasts, one row per scope, with both intervals, $^{*}$ where both exclude zero; the counted states are the $60$ retraction and expiry triples. Names alone leave both smaller models where the intact summary left them and counts alone cost each about $0.14$, all of it on supersession; the moved count moves the three stronger models reliably on the counted states and neither smaller model. Lower panel: Opus 5 under the all-states summary minus the all-states lookup, five draws and its first draw alone.}\n"
            "\\label{tab:cf-matched-ablations}\n"
            "\\centering\\tiny\\setlength{\\tabcolsep}{2pt}\n"
            "\\begin{tabular}{@{}lrrrrr@{}}\n\\toprule\n"
            "Reader, summary & W/T/L & matched & supersession & retraction & expiry \\\\\n\\midrule\n" + "".join(lev) +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}llrll@{}}\n\\toprule\n"
            "Contrast (names, counts, totals) & scope & difference & triple interval & persona interval \\\\\n\\midrule\n" + c1 +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}llrll@{}}\n\\toprule\n"
            "Contrast (the moved count; all states named) & scope & difference & triple interval & persona interval \\\\\n\\midrule\n" + c2 +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}llrll@{}}\n\\toprule\n"
            "Opus 5 minus the all-states lookup & scope & difference & triple interval & persona interval \\\\\n\\midrule\n" + "".join(c3) +
            "\\bottomrule\n\\end{tabular}\n\\end{table}\n")


FIG3_POOLED = r"""%% R131 D (2026-09-20): the pooled version of Figure 3 (the R126 drawing; fig3_data.py's file spliced by build_v22.py at the pooled-data marker below with its macros renamed); the body's Figure 3 is on the matched metric.
%%FIG3-DATA-POOLED%%
\begin{figure}[H]
\centering
\begin{tikzpicture}
\begin{groupplot}[group style={group size=2 by 1, horizontal sep=0.9cm, ylabels at=edge left, yticklabels at=edge left},
    width=0.41\linewidth, height=5.0cm, xmin=-0.5, xmax=2.5, ymin=0.45, ymax=1.0,
    xtick={0,1,2}, xticklabels={Supersession,Retraction,Expiry}, ytick={0.5,0.6,0.7,0.8,0.9,1.0},
    ylabel={pooled obligation AUROC}, ylabel style={font=\scriptsize}, tick label style={font=\scriptsize}, title style={font=\scriptsize, yshift=-3pt},
    ymajorgrids, grid style={black!12}, axis line style={black!60}, clip=false,
    legend style={at={(1.04,0.5)}, anchor=west, font=\scriptsize, draw=none, fill=none, row sep=-1pt, nodes={anchor=west}}]
  \nextgroupplot[title={only supersession named}]
      \draw[dashed, black!60] (axis cs:-0.5,0.5) -- (axis cs:2.5,0.5);
      \addplot[only marks, mark=*, mark size=2.0pt, black, xshift=-9pt] table[x=x, y=mini] {\figthreeSupPooled};
      \addplot[only marks, mark=square*, mark size=1.9pt, black, xshift=-6pt] table[x=x, y=haiku] {\figthreeSupPooled};
      \addplot[only marks, mark=triangle*, mark size=2.3pt, black, mark options={fill=white}, xshift=-3pt] table[x=x, y=luna] {\figthreeSupPooled};
      \addplot[only marks, mark=diamond*, mark size=2.3pt, black, mark options={fill=white}, xshift=0pt] table[x=x, y=sol] {\figthreeSupPooled};
      \addplot[only marks, mark=pentagon*, mark size=2.2pt, black, xshift=3pt] table[x=x, y=opus] {\figthreeSupPooled};
      \addplot[only marks, mark=x, mark size=2.6pt, black, thick, xshift=6pt] table[x=x, y=lookup] {\figthreeSupPooled};
      \addplot[only marks, mark=+, mark size=2.6pt, black!60, thick, xshift=9pt] table[x=x, y=count] {\figthreeSupPooled};
  \nextgroupplot[title={all states named}]
      \draw[dashed, black!60] (axis cs:-0.5,0.5) -- (axis cs:2.5,0.5);
      \addplot[only marks, mark=*, mark size=2.0pt, black, xshift=-9pt] table[x=x, y=mini] {\figthreeAllPooled};
      \addplot[only marks, mark=square*, mark size=1.9pt, black, xshift=-6pt] table[x=x, y=haiku] {\figthreeAllPooled};
      \addlegendimage{only marks, mark=triangle*, mark size=2.3pt, black, mark options={fill=white}}
      \addlegendimage{only marks, mark=diamond*, mark size=2.3pt, black, mark options={fill=white}}
      \addplot[only marks, mark=pentagon*, mark size=2.2pt, black, xshift=3pt] table[x=x, y=opus] {\figthreeAllPooled};
      \addplot[only marks, mark=x, mark size=2.6pt, black, thick, xshift=6pt] table[x=x, y=lookup] {\figthreeAllPooled};
      \addlegendimage{only marks, mark=+, mark size=2.6pt, black!60, thick}
      \addlegendimage{dashed, black!60}
      \legend{mini (five draws), Haiku, Luna (left only), Sol (left only), Opus, name lookup, count reader (left only), chance}
\end{groupplot}
\end{tikzpicture}
\caption{The pooled version of Figure~\ref{fig:perstate}: per-state pooled obligation AUROC on the counterfactual set, each state's positives against all of its items' negatives, under the summary naming supersession only (left) and the summary naming all states (right); the dashed line is chance. Mini uses five draws, matching Table~\ref{tab:cf-main}; the count reader guesses the category; Luna and Sol have rows under the default summary only. Every value is in Table~\ref{tab:cf-matched}.}
\label{fig:perstate-pooled}
\end{figure}
"""


def emptiness_table():
    c = T2["census_444"]["SUPERSESSION"]
    def hist(h):
        return ", ".join(f"{k}: {v}" for k, v in sorted(h.items(), key=lambda kv: int(kv[0])))
    rows = []
    for ver in ("PN", "PRESENT", "ABSENT"):
        x = c[f"v2_superseded_list/{ver}"]
        rows.append(f"\\{ver.lower()}{{}} & ${x['empty']}$ & ${x['mean_length']:.4f}$ & {hist(x['length_hist'])} \\\\\n")
    d = c["v2_superseded_list/PN_minus_PRESENT_length"]
    v2, v3 = T2["cf444"]["v2"], T2["cf444"]["v3"]
    lev, dif = [], []
    for v, lab in ((v2, "$444$, default summary"), (v3, "$444$, all states named")):
        r = v["random_token"]; pm = r["matched_pn_vs_present"]; lp = v["lookup_minus_random_pooled"]["whole"]; lm = v["lookup_minus_random_matched"]["pn_vs_present"]["whole"]
        per = " / ".join(f4(r["pooled"]["per_state"][s]) for s in ST)
        lev.append(f"{lab} & {f4(r['pooled']['whole'])} & {per} & {wtl(pm['whole'])} & {f4(pm['whole']['matched'])} & {f4(pm['per_state']['SUPERSESSION']['matched'])} \\\\\n")
        dif.append(f"{lab}, pooled & {s4(lp['delta'])}{star(lp)} & {iv(lp['item_ci'])} & {iv(lp['persona_ci'])} \\\\\n")
        dif.append(f"{lab}, matched & {s4(lm['delta'])}{star(lm)} & {iv(lm['ci_triple'])} & {iv(lm['ci_persona'])} \\\\\n")
    for form, lab in (("committed", "$661$, as committed"), ("marker_free", "$661$, marker-free")):
        o = T2["obl661"][form]; r = o["random_token"]; lp = o["lookup_minus_random_pooled"]["whole"]
        lev.append(f"{lab} & {f4(r['whole'])} & " + " / ".join(f4(r[s]["auroc"]) for s in ST) + " & -- & -- & -- \\\\\n")
        dif.append(f"{lab}, pooled & {s4(lp['delta'])}{star(lp)} & {iv(lp['item_ci'])} & {iv(lp['persona_ci'])} \\\\\n")
    return (HDR.format("r125_t2_emptiness.json", "15b (AUX-CF2-R125-T2-CENSUS, -T2-RANDOM, -T2-DIFF)") +
            "\\begin{table}[H]\n"
            f"\\caption{{How much of the lookup is list length and emptiness (post hoc). Upper panel: the superseded-names list of the $88$ supersession pairs per store version under the default summary, the count of empty lists, the mean length and the length distribution; the \\pn{{}} version's list is longer than the \\present{{}} version's by one name on ${d['1']}$ pairs, two on ${d['2']}$ and three on ${d['3']}$, and on the ${c['v2_pairs_where_PRESENT_empty_and_PN_nonempty']}$ pairs whose \\present{{}} list is empty emptiness alone identifies the \\pn{{}} version. Middle panel: the random-token control (every name replaced by a random token, the list's length and emptiness kept) on the counterfactual set under both summaries, pooled and matched, and on the full obligation set (no triples, so no matched row; each state's positives against all $557$ negatives). Lower panel: the name lookup minus the random-token control, pooled with the item-level and persona-grouped intervals and matched with the triple-level and persona-grouped intervals ($^{{*}}$ both exclude zero). Under the default summary $0.60$ of the lookup's $0.77$ pooled and $0.65$ of its $0.78$ matched is reachable with no name meaning anything; the sibling-name control (Table~\\ref{{tab:cf-sibling}}) removes that component.}}\n"
            "\\label{tab:cf-emptiness}\n"
            "\\centering\\tiny\\setlength{\\tabcolsep}{2pt}\n"
            "\\begin{tabular}{@{}lrrl@{}}\n\\toprule\n"
            "Store version & empty lists & mean length & length: pairs \\\\\n\\midrule\n" + "".join(rows) +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}lrlrrr@{}}\n\\toprule\n"
            "Random-token lookup & pooled & sup.\\ / ret.\\ / exp. & W/T/L & matched & matched, supersession \\\\\n\\midrule\n" + "".join(lev) +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}lrll@{}}\n\\toprule\n"
            "Name lookup minus random token & difference & item or triple interval & persona interval \\\\\n\\midrule\n" + "".join(dif) +
            "\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def matched_prose():
    l = RD["LOOKUP_v2"]["pn_vs_present"]["whole"]; g = RD["CR-nb1_v2"]["pn_vs_present"]["whole"]; m5 = RD["MINI5_v2"]["pn_vs_present"]["whole"]; m1 = RD["MINI1_v2"]["pn_vs_present"]["whole"]
    o = PD["opus_v3_vs_allstates"]["OP5_v3"]["pn_vs_present"]["whole"]; o1 = PD["opus_v3_vs_allstates"]["OP5_v3_d1"]["pn_vs_present"]["whole"]
    rt = RD["RANDTOK_v2"]["pn_vs_present"]
    return ("\\paragraph{The matched metric.}\n"
            "%% R131 (2026-09-20): R125 Task 1 (AUX-CF2-R125-*) and Task 2 (AUX-CF2-R125-T2-*); the pooled Figure 3 moves here.\n"
            "The counterfactual set fixes the question and varies the store, so the comparison the design supports is within a triple; the pooled AUROC of Table~\\ref{tab:cf-main} also orders each positive against the negatives of every other question.\n"
            "The matched AUROC of Section~\\ref{sec:setup} is $(W+T/2)/n$ over the triples, the \\pn{} version against the \\present{} version, with a tie counting half; it was defined after every pooled row was known, and every value here is post hoc.\n"
            f"Table~\\ref{{tab:cf-matched}} gives it for every reader of Table~\\ref{{tab:cf-main}} with the triple-level and the persona-grouped interval, whole set and per state; Table~\\ref{{tab:cf-classes}} decomposes the pooled AUROC by pair class; Table~\\ref{{tab:cf-matched-vs}} gives the paired differences against the lookups and the count readers; Table~\\ref{{tab:cf-matched-ablations}} the ablations; Figure~\\ref{{fig:perstate-pooled}} is the pooled version of Figure~\\ref{{fig:perstate}}.\n"
            f"Under this metric a tie is half a win, so the readers that never lose a triple sit on their tie counts: the name lookup ties ${l['T']}$ of ${l['n']}$ triples and reads {f4(l['matched'])}, and the guessing count reader ties ${g['T']}$ and reads {f4(g['matched'])}, while a model with fine-grained scores rarely ties and pays for every loss (GPT-4.1 mini's five-draw row loses ${m5['L']}$ triples against its one-draw row's ${m1['L']}$, so it reads {f4(m5['matched'])} against {f4(m1['matched'])}).\n"
            f"The three claims of Section~\\ref{{sec:counterfactual}} whose reading changes under it are the count readers on the counted states, where GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 are no longer reliably below the guessing reader (Table~\\ref{{tab:cf-matched-vs}}); the moved count, which Luna and Sol follow reliably as well as Opus 5 (Table~\\ref{{tab:cf-matched-ablations}}); and the hybrid reader (Table~\\ref{{tab:cf-hybrid}}).\n"
            f"One reliability changes: Opus 5 under the all-states summary exceeds the all-states lookup by {s4(o['delta'])} with intervals {iv(o['ci_triple'])} and {iv(o['ci_persona'])}, not reliable, where the pooled difference of Table~\\ref{{tab:cf-main}} is; its first draw alone reads {s4(o1['delta'])} with both intervals clear of zero.\n"
            f"What the matched comparison does not remove is list length: the random-token lookup reads {f4(rt['whole']['matched'])} on it ({f4(rt['per_state']['SUPERSESSION']['matched'])} on supersession) because the \\pn{{}} version's list is one name longer than the \\present{{}} version's, and Table~\\ref{{tab:cf-emptiness}} measures that component; the sibling-name control below is built to remove it.\n\n")


# ------------------------------------------------------------------------------------------------------------------------------ C.2: the hybrid's matched panel and the sibling-name control
def hybrid_matched_panel():
    h = RD["HYBRID_v2"]["pn_vs_present"]; hl = PD["vs_lookup"]["HYBRID_v2"]["pn_vs_present"]
    rows, rowsl = [], []
    for s_, lab in (("whole", "whole set"), ("SUPERSESSION", "supersession"), ("RETRACTION", "retraction"), ("EXPIRY", "expiry")):
        p = h["whole"] if s_ == "whole" else h["per_state"][s_]; q = hl["whole"] if s_ == "whole" else hl["per_state"][s_]
        rows.append(f"{lab} & {wtl(p)} & {f4(p['matched'])} & {iv(p['ci_triple'], False)} & {iv(p['ci_persona'], False)} \\\\\n")
        rowsl.append(f"{lab} & {s4(q['delta'])}{star(q)} & {iv(q['ci_triple'])} & {iv(q['ci_persona'])} \\\\\n")
    rows2 = []
    for name, lab, key in (("mini k1 minus hybrid", "GPT-4.1 mini, one draw", "MINI1_v2"), ("mini k5 minus hybrid", "GPT-4.1 mini, five draws", "MINI5_v2"), ("Haiku minus hybrid", "Haiku 4.5", "H45_v2"),
                           ("Opus minus hybrid", "Opus 5", "OP5_v2"), ("Sol minus hybrid (P-H2)", "GPT-5.6 Sol", "SOL_v2"), ("Luna minus hybrid", "GPT-5.6 Luna", "LUNA_v2")):
        c = PD["contrasts"][name]["pn_vs_present"]["whole"]
        rows2.append(f"{lab} & {f4(RD[key]['pn_vs_present']['whole']['matched'])} & {s4(c['delta'])}{star(c)} & {iv(c['ci_triple'])} & {iv(c['ci_persona'])} \\\\\n")
    return ("%% R131 (2026-09-20): the hybrid reader under the matched metric (R125 Task 1; AUX-CF2-R125-MATCHED-V2 HYBRID_v2, -VS-LOOKUP, -CONTRASTS), written by appendix_r131.py.\n"
            "\\\\[4pt]\n\\begin{tabular}{@{}lrrll@{}}\n\\toprule\n"
            "Under the matched metric (post hoc) & W/T/L & matched & triple interval & persona interval \\\\\n\\midrule\n" + "".join(rows) +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}lrll@{}}\n\\toprule\n"
            "Hybrid minus the lookup, matched & difference & triple interval & persona interval \\\\\n\\midrule\n" + "".join(rowsl) +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}lrrll@{}}\n\\toprule\n"
            "Model minus the hybrid, matched & model & difference & triple interval & persona interval \\\\\n\\midrule\n" + "".join(rows2) +
            "\\bottomrule\n\\end{tabular}\n")


def hybrid_prose():
    h = RD["HYBRID_v2"]["pn_vs_present"]["whole"]; hl = PD["vs_lookup"]["HYBRID_v2"]["pn_vs_present"]["whole"]
    s = PD["contrasts"]["Sol minus hybrid (P-H2)"]["pn_vs_present"]["whole"]; lu = PD["contrasts"]["Luna minus hybrid"]["pn_vs_present"]["whole"]; op = PD["contrasts"]["Opus minus hybrid"]["pn_vs_present"]["whole"]
    ha = PD["contrasts"]["Haiku minus hybrid"]["pn_vs_present"]["whole"]; m5 = PD["contrasts"]["mini k5 minus hybrid"]["pn_vs_present"]["whole"]
    return ("%% R131 (2026-09-20): the hybrid under the matched metric (AUX-CF2-R125-MATCHED-V2 HYBRID_v2; -CONTRASTS 'hybrid minus name lookup (P-H1)', 'Sol minus hybrid (P-H2)').\n"
            f"Under the matched metric the same reader reads {f4(h['matched'])} (${h['W']}/{h['T']}/{h['L']}$), {s4(hl['delta'])} above the name lookup with intervals {iv(hl['ci_triple'])} and {iv(hl['ci_persona'])}, and the three stronger models are level with it at the point: GPT-5.6 Sol {s4(s['delta'])}, GPT-5.6 Luna {s4(lu['delta'])} and Opus 5 {s4(op['delta'])}, each with both intervals including zero, while Haiku 4.5 ({s4(ha['delta'])}) and GPT-4.1 mini at five draws ({s4(m5['delta'])}) are reliably below it.\n"
            "So the two registered predictions, read under the pooled metric, reverse under the matched one, which was defined afterwards: the combination is reliably above the lookup within triples, and Sol is not reliably above the combination.\n"
            "Table~\\ref{tab:cf-classes} shows where the pooled metric's ordering comes from: the hybrid's within-triple and same-state values are close to the three models', and its across-state value is not.\n")


def sibling_table():
    order = ["Name lookup", "GPT-4.1 mini (five draws)", "Haiku 4.5 (five draws)", "GPT-5.6 Luna (five draws)", "GPT-5.6 Sol (draw 1)", "Opus 5 (draw 1)", "Random-token lookup", "Count reader, guessed category"]
    rows, rows2, rows3 = [], [], []
    for k in order:
        r = T4["readers"][k]; s_ = r["pn_vs_sibling"]; ml = r.get("minus_lookup_matched"); sp = r["sibling_minus_present_mean"]
        rows.append(f"{k} & {wtl(s_)} & {f4(s_['matched'])} & {iv(s_['ci_triple'], False)} & {iv(s_['ci_persona'], False)} & {f4(r['pn_vs_present_same_pairs']['matched'])} & {f4(r['sibling_vs_present']['matched'])} \\\\\n")
        rows2.append(f"{k} & {s4(sp['delta'])}{star(sp)} & {iv(sp['ci_triple'])} & {iv(sp['ci_persona'])} \\\\\n")
        if ml:
            rows3.append(f"{k} & {s4(ml['delta'])}{star(ml)} & {iv(ml['ci_triple'])} & {iv(ml['ci_persona'])} \\\\\n")
    P = T4["predictions"]
    sb2 = P["P-SB2"]["per_model"]
    lows = ", ".join(f"${v['persona_lo']:.4f}$" for v in sb2.values())
    return (HDR.format("r125_t4_sibling.json", "15d (AUX-CF2-R125-SB-*)") +
            "\\begin{table}[H]\n"
            f"\\caption{{The sibling-name control (registered; ADDENDUM\\_R125\\_SIBLING): a fourth version of each of the $88$ supersession pairs, rendered from the \\pn{{}} version's text with the target's name in the superseded-names list replaced by a same-category sibling under HV-B's pool and neighbourhood rule (no content token shared with the question or the target; ${T4['meta']['n_pairs'] - T4['meta']['dropped']}$ of $88$ pairs kept; the leak screen $0$ of $30$), so counts, list length and every other line are identical to the \\pn{{}} version's. Upper panel: W/T/L and the matched AUROC of the \\pn{{}} version against the sibling version with both intervals; the \\pn{{}}-against-\\present{{}} value on the same pairs; and the sibling version against the \\present{{}} version (how far an unrelated name in the list raises the score, the list-length component; descriptive). Lower panels: the sibling-minus-\\present{{}} mean score with both intervals, and each reader minus the name lookup on the primary comparison, $^{{*}}$ where both intervals exclude zero. "
            f"Four predictions, all as written: P-SB1, the lookup at or above $0.90$ (${P['P-SB1']['lookup']:.4f}$); P-SB2, every model at or above $0.80$ with the persona interval above $0.50$ (lower bounds {lows}); P-SB3, the random-token lookup and the count reader within $0.05$ of $0.50$ (${P['P-SB3']['random_token']:.4f}$, ${P['P-SB3']['count_reader']:.4f}$); P-SB4, no model reliably above the lookup. "
            "Disclosure: the scorer was dry-run once before the freeze to check its code path and computed the three no-model readers on the sibling texts, so P-SB1 and P-SB3 are recorded values rather than predictions and are not counted in Appendix~\\ref{app:registration}; no model row existed at the dry run. GPT-4.1 mini, Haiku 4.5 and GPT-5.6 Luna are five-draw means as in Table~\\ref{tab:cf-main}; Opus 5 and GPT-5.6 Sol one draw.}\n"
            "\\label{tab:cf-sibling}\n"
            "\\centering\\tiny\\setlength{\\tabcolsep}{2pt}\n"
            "\\begin{tabular}{@{}lrrllrr@{}}\n\\toprule\n"
            "Reader & W/T/L & \\pn{} vs sibling & triple interval & persona interval & \\pn{} vs \\present{} & sibling vs \\present{} \\\\\n\\midrule\n" + "".join(rows) +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}lrll@{}}\n\\toprule\n"
            "Reader: sibling minus \\present{} mean score & difference & triple interval & persona interval \\\\\n\\midrule\n" + "".join(rows2) +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}lrll@{}}\n\\toprule\n"
            "Reader minus the name lookup, \\pn{} vs sibling & difference & triple interval & persona interval \\\\\n\\midrule\n" + "".join(rows3) +
            "\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def sibling_prose():
    R = T4["readers"]; lk = R["Name lookup"]["pn_vs_sibling"]; op = R["Opus 5 (draw 1)"]; ha = R["Haiku 4.5 (five draws)"]
    vals = {k: R[k]["pn_vs_sibling"]["matched"] for k in ("GPT-4.1 mini (five draws)", "Haiku 4.5 (five draws)", "GPT-5.6 Luna (five draws)", "GPT-5.6 Sol (draw 1)", "Opus 5 (draw 1)")}
    return ("\\paragraph{The sibling-name control.}\n"
            "%% R131 (2026-09-20): R125 Task 4 (AUX-CF2-R125-SB-*).\n"
            "The matched comparison still lets a reader profit from list length, since the \\pn{} version's superseded-names list is one name longer than its siblings' and $24$ of the $88$ \\present{} lists are empty (Table~\\ref{tab:cf-emptiness}).\n"
            "The sibling-name control removes that: a fourth store version per supersession pair carries the \\pn{} version's text with the target's name in the superseded-names list replaced by another attribute of the same category, so the two versions differ only in which name is listed (Table~\\ref{tab:cf-sibling}).\n"
            f"The name lookup separates the \\pn{{}} version from it at {f4(lk['matched'])} (${lk['W']}/{lk['T']}/{lk['L']}$), and the five models at {f4(min(vals.values()))} to {f4(max(vals.values()))}, none reliably above the lookup (Opus 5 {s4(op['minus_lookup_matched']['delta'])} with intervals {iv(op['minus_lookup_matched']['ci_triple'])} and {iv(op['minus_lookup_matched']['ci_persona'])}); the random-token lookup falls to {f4(R['Random-token lookup']['pn_vs_sibling']['matched'])} and the count reader ties every pair.\n"
            f"An unrelated name in the list does raise the scores: the sibling version scores above the \\present{{}} version for every reader but Opus 5 (the sibling-minus-\\present{{}} mean for Haiku 4.5 {s4(ha['sibling_minus_present_mean']['delta'])}, both intervals clear of zero; Opus 5 {s4(op['sibling_minus_present_mean']['delta'])}, intervals including zero), which is the list-length component the primary comparison removes.\n\n")


# ------------------------------------------------------------------------------------------------------------------------------ E.9 and G.4: the strata
FR_READERS = [("mini_true", "GPT-4.1 mini, ground truth"), ("mini_capped", "GPT-4.1 mini, store-written capped"), ("mini_lifted", "GPT-4.1 mini, store-written lifted"),
              ("haiku_true", "Haiku 4.5, ground truth"), ("haiku_capped", "Haiku 4.5, store-written capped"), ("haiku_lifted", "Haiku 4.5, store-written lifted"),
              ("lookup_true", "Name lookup, ground truth"), ("lookup_capped", "Name lookup, store-written capped"), ("lookup_lifted", "Name lookup, store-written lifted")]
FR_STRATA = [("all_104 (manifest-relative, the printed rows)", "all $104$ (the printed rows)"), ("join_marked_0.80", "alignment marks the forbidding record ($0.80$ bar)"), ("join_marked_0.75", "the same at the $0.75$ bar"),
             ("join_marked_0.50", "the same at the $0.50$ bar"), ("join_unmarked_0.80 (the 22)", "not marked at $0.80$ (the $22$)"), ("own_marked", "the store's own mark on a member"),
             ("own_active (no store mark on any member)", "no store mark on any member"), ("join_marked_0.80_and_own_marked", "marked by both"), ("join_marked_0.80_and_own_active", "marked by the alignment only")]


def frbank_strata_table():
    rows = []
    for key, lab in FR_STRATA:
        s = T3F["rescored"][key]
        rows.append(f"{lab} & ${s['n_pos']}$ & " + " & ".join(f4(s["readers"][r]["auroc"]) for r, _ in FR_READERS) + " \\\\\n")
    s82 = T3F["rescored"]["join_marked_0.80"]
    low = []
    for r, lab in (("mini_capped", "GPT-4.1 mini, capped"), ("mini_lifted", "GPT-4.1 mini, lifted"), ("haiku_capped", "Haiku 4.5, capped"), ("haiku_lifted", "Haiku 4.5, lifted"), ("lookup_capped", "Name lookup, capped"), ("lookup_lifted", "Name lookup, lifted")):
        d = s82["readers"][r]["minus_ground_truth"]
        low.append(f"{lab} & {ivq(d)}{star(d)} \\\\\n")
    c = T3F["counts"]
    return (HDR.format("r125_t3_frbank.json", "15c (AUX-CF2-R125-T3-FRBANK)") +
            "\\begin{table}[H]\n"
            f"\\caption{{The rows of Table~\\ref{{tab:levels}} re-scored on strata of the $104$ obligations, the $557$ negatives unchanged (post hoc). The alignment of manifest events to stored records marks a forbidding record for ${c['join_marked']['0.80']['n']}$ obligations at the $0.80$ overlap bar (${c['join_marked']['0.80']['by_state']['sup']}$ supersession, ${c['join_marked']['0.80']['by_state']['ret']}$ retraction, ${c['join_marked']['0.80']['by_state']['exp']}$ expiry), ${c['join_marked']['0.75']['n']}$ at $0.75$ and ${c['join_marked']['0.50']['n']}$ at $0.50$; the store's own fields mark a member of ${c['own_marked']['n']}$; ${c['cross_join080_own']['join=True,own=True']}$ are marked by both, ${c['cross_join080_own']['join=True,own=False']}$ by the alignment alone, ${c['cross_join080_own']['join=False,own=True']}$ by the store alone and ${c['cross_join080_own']['join=False,own=False']}$ by neither. Upper panel: the AUROC per stratum. Lower panel: on the ${s82['n_pos']}$ the alignment marks, each store-written row minus its ground-truth row with both intervals, $^{{*}}$ where both exclude zero. On the ${T3F['rescored']['join_unmarked_0.80 (the 22)']['n_pos']}$ it does not mark every reader is at or below $0.71$ under every summary, the ground-truth summary included, because the ground-truth name list is built from the same alignment.}}\n"
            "\\label{tab:levels-strata}\n"
            "\\centering\\tiny\\setlength{\\tabcolsep}{1.5pt}\n"
            "\\begin{tabular}{@{}lrrrrrrrrrr@{}}\n\\toprule\n"
            "Obligations & $n$ & \\multicolumn{3}{c}{GPT-4.1 mini} & \\multicolumn{3}{c}{Haiku 4.5} & \\multicolumn{3}{c}{Name lookup} \\\\\n"
            " & & truth & capped & lifted & truth & capped & lifted & truth & capped & lifted \\\\\n\\midrule\n" + "".join(rows) +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}ll@{}}\n\\toprule\n"
            f"On the ${s82['n_pos']}$ the alignment marks: store-written minus ground truth & difference, item interval; persona interval \\\\\n\\midrule\n" + "".join(low) +
            "\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def frbank_prose():
    c = T3F["counts"]; s82 = T3F["rescored"]["join_marked_0.80"]; u = T3F["rescored"]["join_unmarked_0.80 (the 22)"]
    return ("\\paragraph{What the store is in each scored condition, and where the labels come from.}\n"
            "%% R131 (2026-09-20): R125 Task 3 (AUX-CF2-R125-T3-FRBANK); the paragraph on what the store is in each condition.\n"
            "On FR-Bank the store is its own persona bank, read through the store's own fields (\\texttt{is\\_active}, \\texttt{is\\_retracted}, \\texttt{supersedes}) by the one renderer into the store-written summary, capped at fifteen names per category or with the cap lifted.\n"
            "The \\pn{} labels come from the manifest, checked by hand, and each obligation's forbidding records are entries of that same bank, so the forbidding content is stored by construction for all $104$ obligations.\n"
            f"What the label does not say is whether the alignment of manifest events to stored records marks one of those records, which is what the ground-truth summary's superseded-names list and the ground-truth tags are built from: it marks ${c['join_marked']['0.80']['n']}$ at the $0.80$ bar, and the ${u['n_pos']}$ it does not mark are all retraction- or expiry-derived.\n"
            "So on FR-Bank the label is manifest-relative, the ground-truth summary is alignment-relative and the store-written summary is store-relative; the three coincide on the $63$ supersession obligations and diverge on the counted states.\n"
            f"Table~\\ref{{tab:levels-strata}} re-scores the rows of Table~\\ref{{tab:levels}} on each stratum: on the ${s82['n_pos']}$ the alignment marks, the capped store-written summary still costs GPT-4.1 mini {s4(s82['readers']['mini_capped']['minus_ground_truth']['delta'])}, Haiku 4.5 {s4(s82['readers']['haiku_capped']['minus_ground_truth']['delta'])} and the lookup {s4(s82['readers']['lookup_capped']['minus_ground_truth']['delta'])} against the ground-truth summary, each with both intervals clear of zero, so the loss the body reports is not an artifact of the obligations the alignment misses; on the ${u['n_pos']}$ it does not mark, the ground-truth summary itself reads {f4(u['readers']['mini_true']['auroc'])} for mini, {f4(u['readers']['haiku_true']['auroc'])} for Haiku 4.5 and {f4(u['readers']['lookup_true']['auroc'])} for the lookup, because its list is built from the same alignment.\n"
            "On Graphiti the store is one graph per persona built by the backend's own extraction from the same conversations with every lifecycle field removed, so whether it retains the forbidding content is a question of extraction (Appendix~\\ref{app:posthoc-graphiti}, Table~\\ref{tab:graphiti-strata}).\n"
            "On Mem0 and A-MEM no obligation is scored: their scored populations hold \\present{} and \\absent{} items only, so their evaluation is the coverage judgment and the census, and there is no \\pn{} label to state relative to what they retain.\n\n")


G_READERS = [("G10-BELIEVED", ("store-written", "capped")), ("G10-LIFTED", ("store-written", "lifted")), ("NB6-emb-capped", ("store's name", "lookup")), ("NB5-emb-capped", ("whole-map", "lookup")), ("G10-VIEW-UNTAGGED", ("five edges", "untagged")),
             ("G10-VIEW-TAGGED", ("native", "tags")), ("G10-HYBRID", ("tagged +", "summary")), ("FRB-VIEW-UNTAGGED", ("FR-Bank", "top-five")), ("TRUE", ("FR-Bank", "ground truth"))]
G_STRATA = [("all_47 (manifest-relative, the printed rows)", "all $47$ (the printed rows)"), ("retained_0.80 (recovered + stale-active, of the 34)", "retained at $0.80$ (recovered or stale-active)"),
            ("recovered_0.80 (non-active mark on a firing edge)", "recovered (a non-active mark on the edge)"), ("stale_active_0.80", "stale-active"), ("extraction_miss_0.80", "extraction miss"),
            ("retained_0.75 (recovered + stale-active, of the 34)", "retained at $0.75$"), ("retained_0.50 (recovered + stale-active, of the 34)", "retained at $0.50$"),
            ("join_retracted_4 (inexpressible)", "retraction-derived (inexpressible)"), ("join_unflagged_9", "not marked by the alignment"), ("not_retained_0.80 (extraction miss + retracted + unflagged)", "not retained (the three above)")]


def graphiti_strata_table():
    rows = []
    for key, lab in G_STRATA:
        s = T3G["rescored"][key]
        rows.append(f"{lab} & ${s['n_pos']}$ & " + " & ".join(f4(s["readers"][r]["auroc"]) for r, _ in G_READERS) + " \\\\\n")
    r23 = T3G["rescored"]["retained_0.80 (recovered + stale-active, of the 34)"]; r13 = T3G["rescored"]["recovered_0.80 (non-active mark on a firing edge)"]
    d23 = r23["readers"]["G10-BELIEVED"]["minus_true"]; l23 = r23["readers"]["NB6-emb-capped"]["minus_true"]; d13 = r13["readers"]["G10-BELIEVED"]["minus_true"]
    b = T3G["recorded_buckets_080"]; c = T3G["counts"]
    return (HDR.format("r125_t3_graphiti.json", "15c (AUX-CF2-R125-T3-GRAPHITI)") +
            "\\begin{table}[H]\n"
            f"\\caption{{The rows of Table~\\ref{{tab:graphiti-completed}} re-scored on strata of the $47$ full-store obligations, the $276$ negatives unchanged (post hoc; the edges read once from the forty graphs). Of the $34$ superseded-or-expired obligations the alignment marks, the graph retains the forbidding content for ${c['0.80']['retained']}$ at the $0.80$ overlap bar (${b['RECOVERED']}$ recovered, a non-active mark on a firing edge, and ${b['STALE_ACTIVE']}$ stale-active) and never extracted it for ${b['EXTRACTION_MISS']}$; ${c['0.75']['retained']}$ and ${c['0.50']['retained']}$ are retained at the $0.75$ and $0.50$ bars; the ${b['retracted']}$ retraction-derived obligations are inexpressible under the mapping and the ${b['unflagged']}$ the alignment does not mark have no stratum. "
            f"On the ${r23['n_pos']}$ retained, the capped store-written summary reads {s4(d23['delta'])} against the FR-Bank ground-truth summary on the same items with intervals {iv(d23['item_ci'])} and {iv(d23['persona_ci'])}, still a reliable loss, and the store's own name lookup {s4(l23['delta'])} ({iv(l23['item_ci'])}; {iv(l23['persona_ci'])}); on the ${r13['n_pos']}$ recovered the capped summary reads {s4(d13['delta'])} ({iv(d13['item_ci'])}; {iv(d13['persona_ci'])}), not reliable at that size.}}\n"
            "\\label{tab:graphiti-strata}\n"
            "\\centering\\tiny\\setlength{\\tabcolsep}{1pt}\n"
            "\\begin{tabular}{@{}lrrrrrrrrrr@{}}\n\\toprule\n"
            "Obligations & $n$ & " + " & ".join(f"\\hd{{{a}}}{{{b}}}" for _, (a, b) in G_READERS) + " \\\\\n\\midrule\n" + "".join(rows) +
            "\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def graphiti_prose():
    b = T3G["recorded_buckets_080"]; r23 = T3G["rescored"]["retained_0.80 (recovered + stale-active, of the 34)"]
    return ("%% R131 (2026-09-20): R125 Task 3 (AUX-CF2-R125-T3-GRAPHITI); the strata behind Section 6's Graphiti paragraph.\n"
            f"Read relative to what the graph retains rather than to the manifest, ${b['RECOVERED'] + b['STALE_ACTIVE']}$ of the $34$ obligations it could express hold the forbidding content (${b['RECOVERED']}$ with a non-active mark on it, ${b['STALE_ACTIVE']}$ with every such edge active) and ${b['EXTRACTION_MISS']}$ were never extracted; Table~\\ref{{tab:graphiti-strata}} re-scores every monitor row of Table~\\ref{{tab:graphiti-completed}} on those strata.\n"
            f"On the ${r23['n_pos']}$ retained, GPT-4.1 mini under the capped store-written summary reads {f4(r23['readers']['G10-BELIEVED']['auroc'])} against {f4(r23['readers']['TRUE']['auroc'])} under the FR-Bank ground-truth summary on the same items, a loss that stays reliable, so part of the store-written loss is the summary's and part is extraction.\n\n")


# ------------------------------------------------------------------------------------------------------------------------------ F
def registration_table_e():
    """The fifth registration table: tab:registrations-d is placed [H] and already fills its page (R129 shortened E9's row until it fit), so the two R125 rows get a table of their own."""
    return ("%% R131 (2026-09-20): the registration record's fifth table, the two R125 registrations (reviews/r125/registrations/, frozen together at 5cd8f809f2 = day 41); tab:registrations-d is a [H] table at its page's height, so the rows have their own table.\n"
            "\\begin{table}[H]\n"
            "\\caption{The registration record, continued: the sibling-name control and the names-against-counts amendment on the three stronger models, both registered after the matched metric had been read; the Outcome column lists each prediction's outcome. Both rows were committed before their first call.}\n"
            "\\label{tab:registrations-e}\n"
            "\\centering\n\\scriptsize\n\\setlength{\\tabcolsep}{1.5pt}\n"
            "\\begin{tabular}{@{}p{0.15\\linewidth}p{0.11\\linewidth}p{0.11\\linewidth}p{0.42\\linewidth}p{0.15\\linewidth}@{}}\n\\toprule\n"
            "Artifact & Commit hash & Freeze day & What it froze & Outcome \\\\\n\\midrule\n"
            + registration_rows() + "\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def registration_rows():
    P4 = T4["predictions"]; P5 = T5["predictions"]
    return ("%% R131 (2026-09-20): the two R125 registrations (reviews/r125/registrations/, frozen together at 5cd8f809f2 = day 41; AUX-CF2-R125-SB-P-SB1 to -P-SB4, AUX-CF2-R125-NC-P-N3 to -P-N5).\n"
            "The sibling-name control & \\texttt{5cd8f809f2} & day 41 & a fourth store version per supersession pair with a same-category sibling in place of the target's name, the name lookup, five models, the random-token lookup and the count reader on the matched \\pn{}-against-sibling comparison (Table~\\ref{tab:cf-sibling}); four readings with a bar, two of them (P-SB1, P-SB3) disclosed at the freeze as recorded values from the scorer's dry run and not counted as predictions & "
            f"P-SB2 (every model at or above $0.80$) and P-SB4 (no model reliably above the lookup) {P4['P-SB2']['verdict'].lower()}; P-SB1 and P-SB3 as recorded \\\\\n"
            "Names against counts, Amendment 1: the three stronger models & \\texttt{5cd8f809f2} & day 41 & E2's names-only and counts-only renderings on Opus 5, GPT-5.6 Luna and GPT-5.6 Sol (Table~\\ref{tab:cf-nc-strong}); three predictions: names only within tolerance of the intact row, counts only reliably below names only, counts only above $0.50$ on both counted states under the matched metric; Sol's lane dropped by the registration's own budget rule & "
            f"the first {P5['P-N3']['verdict'].split(' ')[0].lower()} on GPT-5.6 Luna and held on Opus 5; the second held on both; the third {P5['P-N5']['verdict'].split(' ')[0].lower()} on both; not evaluable on Sol \\\\\n")


COUNT_OLD = ("%% R129 B1 (2026-09-20): E9's one prediction (P-M2, failed) in the count (AUX-R129-COUNT): 92 / 28 -> 93 / 29; tab:registrations-d 28 with 10 -> 29 with 11.\n"
             "Table~\\ref{tab:registrations-d} $29$ with $11$: $93$ predictions, $29$ of which came out otherwise, the count Section~\\ref{sec:setup} states.\\\\\n")
COUNT_NEW = ("%% R129 B1 (2026-09-20): E9's one prediction (P-M2, failed) in the count (AUX-R129-COUNT): 92 / 28 -> 93 / 29; tab:registrations-d 28 with 10 -> 29 with 11.\n"
             "%% R131 (2026-09-20): the two R125 registrations (AUX-R131-COUNT): P-SB2 and P-SB4 (held) and P-N3 (failed), P-N4 (held), P-N5 (failed) join the count; P-SB1 and P-SB3 are recorded values, not counted: 93 / 29 -> 98 / 31; the new table -e 5 with 2.\n"
             "Table~\\ref{tab:registrations-d} $29$ with $11$ and Table~\\ref{tab:registrations-e} $5$ with $2$: $98$ predictions, $31$ of which came out otherwise, the count Section~\\ref{sec:setup} states. "
             "The sibling-name control's P-SB1 and P-SB3 were disclosed at its freeze as recorded values (the scorer's pre-freeze dry run had computed the no-model readers) and are not counted as predictions.\\\\\n")

GUIDE_OLD = ("The first finding, that the summary's names carry the judgment and its counts do not, rests on Table~\\ref{tab:cf-main} (every reader on the counterfactual set), Table~\\ref{tab:cf-names-counts} (the summary with its counts or its names removed) and Table~\\ref{tab:v2rcat} (the moved-count control).\n"
             "The second, that on a named state no model reliably exceeds a name lookup and three models pull ahead only where the summary counts, rests on Table~\\ref{tab:sup-margins} (each model's supersession-only margin), Table~\\ref{tab:counterfactual} (every margin over the lookup with both intervals) and Table~\\ref{tab:cf-intent} (the intent crossover).\n"
             "The third, that the backends write the summary poorly, rests on Table~\\ref{tab:census} (the census), Table~\\ref{tab:levels} (the store-written summary's levels) and Table~\\ref{tab:graphiti-completed} (the fourth backend).\n")
GUIDE_NEW = ("%% R131 (2026-09-20): the pointers to the R125 tables.\n"
             "The first finding, that the two smaller models read only the summary's names and the three stronger ones also read its counts, rests on Table~\\ref{tab:cf-main} (every reader on the counterfactual set, both metrics), Table~\\ref{tab:cf-names-counts} with Table~\\ref{tab:cf-nc-strong} (the summary with its counts or its names removed), Table~\\ref{tab:v2rcat} (the moved-count control) and Table~\\ref{tab:cf-matched-ablations} (the same under the matched metric).\n"
             "The second, that on a named state no model reliably exceeds a name lookup and three models pull ahead only where the summary counts, rests on Table~\\ref{tab:sup-margins} (each model's supersession-only margin), Table~\\ref{tab:counterfactual} and Table~\\ref{tab:cf-matched} (every margin over the lookup under both metrics), Table~\\ref{tab:cf-sibling} (the sibling-name control), Table~\\ref{tab:cf-hybrid} (the lookup with one count feature) and Table~\\ref{tab:cf-intent} (the intent crossover).\n"
             "The third, that the backends write the summary poorly, rests on Table~\\ref{tab:census} (the census), Table~\\ref{tab:levels} with Table~\\ref{tab:levels-strata} (the store-written summary's levels, and by what the store retains) and Table~\\ref{tab:graphiti-completed} with Table~\\ref{tab:graphiti-strata} (the fourth backend).\n")


def main():
    check = "--check" in sys.argv
    t = APPX.read_text(encoding="utf-8").replace("\r\n", "\n")
    assert "%% R129 B1" in t, "run appendix_r129.py first"
    if "%% R131" in t:
        print("appendix_r131.py: already applied"); return

    # the reader's guide
    t = rep(t, GUIDE_OLD, GUIDE_NEW, where="reader's guide")
    # C.2: E2 Amendment 1 after tab:cf-names-counts
    anchor = "%% R112 (2026-09-16), post hoc B1 to B4, specified before recomputation"
    t = rep(t, anchor, nc_strong_prose() + nc_strong_table() + "\n" + anchor, where="C.2 E2 Amendment 1")
    # C.2: the matched metric after tab:pnpresent
    anchor = "\\paragraph{The intent crossover.}"
    t = rep(t, anchor, matched_prose() + matched_table() + "\n" + classes_table() + "\n" + vs_table() + "\n" + ablations_table() + "\n" + FIG3_POOLED + "\n" + emptiness_table() + "\n" + anchor, where="C.2 matched")
    # C.2: the hybrid's matched sentences and panel
    t = rep(t, "The combination gains on the two counted states ($+0.0889$ on retraction and $+0.0942$ on expiry over the lookup's $0.5000$) and reads $-0.0153$ against the lookup on supersession, where the lookup alone scores $0.9223$.\n",
            "The combination gains on the two counted states ($+0.0889$ on retraction and $+0.0942$ on expiry over the lookup's $0.5000$) and reads $-0.0153$ against the lookup on supersession, where the lookup alone scores $0.9223$.\n" + hybrid_prose(), where="C.2 hybrid prose")
    t = rep(t, "GPT-5.6 Luna & $0.8417$ & $+0.0553$ & $[+0.0169,+0.0987]$ & $[+0.0245,+0.0864]$ \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n",
            "GPT-5.6 Luna & $0.8417$ & $+0.0553$ & $[+0.0169,+0.0987]$ & $[+0.0245,+0.0864]$ \\\\\n\\bottomrule\n\\end{tabular}" + hybrid_matched_panel() + "\\end{table}\n", where="C.2 hybrid panel")
    t = rep(t, "Lower panel: each model's recorded row minus the hybrid, and GPT-4.1 mini's five-draw row (Table~\\ref{tab:cf-main}) beside its one-draw row.",
            "Lower panels: each model's recorded row minus the hybrid, and GPT-4.1 mini's five-draw row (Table~\\ref{tab:cf-main}) beside its one-draw row; then the same reader under the matched metric (post hoc), whole set and per state, minus the lookup and against each model.", where="C.2 hybrid caption")
    # C.2: the sibling-name control after tab:cf-hybrid
    anchor = "\\paragraph{GPT-4.1 mini on the expiry pairs under the all-states summary.}"
    t = rep(t, anchor, sibling_prose() + sibling_table() + "\n" + anchor, where="C.2 sibling")
    # E.9: the strata, before the three-persona trial
    anchor = "\\paragraph{A fourth backend, measured on three personas.}"
    t = rep(t, anchor, frbank_prose() + frbank_strata_table() + "\n" + anchor, where="E.9 strata")
    # G.4: the strata after tab:graphiti-completed
    anchor = "%% R115 (2026-09-18): the amendment's predictions and readings defined here"
    t = rep(t, anchor, graphiti_prose() + graphiti_strata_table() + "\n" + anchor, where="G.4 strata")
    # F: the two rows and the count
    t = rep(t, "the first failed ($+0.0201$, the item-level interval including zero); the second held \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n",
            "the first failed ($+0.0201$, the item-level interval including zero); the second held \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\n" + registration_table_e(), where="F table e")
    t = rep(t, COUNT_OLD, COUNT_NEW, where="F count")

    if check:
        print("appendix_r131.py --check: would write", APPX); return
    APPX.write_text(t, encoding="utf-8", newline="\n")
    print("->", APPX)


if __name__ == "__main__":
    main()
