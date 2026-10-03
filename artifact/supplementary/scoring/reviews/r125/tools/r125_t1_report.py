# -*- coding: utf-8 -*-
"""r125_t1_report.py -- Task 1's tables, ledger section and Figure 3 data file, all from reviews/r125/results/r125_matched.json. No computation
beyond formatting; nothing typed by hand. NO MODEL CALL.

Writes  reviews/r125/T1_TABLES.md                      one table per summary (superseded-only, all-states, totals-randomized, moved-count; the E2 arms
                                                     and the other v2-text readers under the superseded-only table), the pair-class decomposition,
                                                     the paired blocks and the named contrasts
        reviews/r125/results/fig3_data_matched.tex   the per-state matched values in the schema of reviews/v22/src/fig3_data.tex (the main session swaps it in)
        r82_counterfactual/cf2/NUMBERS_CF2.md          section 15 (AUX-CF2-R125-*), written between the markers R125-T1 BEGIN / END (idempotent)
"""
from __future__ import annotations

import io
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r125_common as C  # noqa: E402
from r125_common import STATES  # noqa: E402

RES = C.RESULTS / "r125_matched.json"
TABLES = C.R125 / "T1_TABLES.md"
FIG3 = C.RESULTS / "fig3_data_matched.tex"
BEGIN, END = "<!-- R125-T1 BEGIN (written by reviews/r125/tools/r125_t1_report.py; do not edit by hand) -->", "<!-- R125-T1 END -->"
SHORT = {"SUPERSESSION": "sup", "RETRACTION": "ret", "EXPIRY": "exp"}

# the rows of each table, in print order (reader key -> the label printed)
TABLE_V2 = [("LOOKUP_v2", "Name lookup"), ("MINI1_v2", "GPT-4.1 mini, one draw (t = 0)"), ("MINI5_v2", "GPT-4.1 mini, five draws (Table 1's row)"), ("H45_v2", "Haiku 4.5"),
            ("LUNA_v2", "GPT-5.6 Luna"), ("SOL_v2", "GPT-5.6 Sol"), ("OP5_v2", "Opus 5"),
            ("H45_v2_d1", "Haiku 4.5, draw 1"), ("LUNA_v2_d1", "GPT-5.6 Luna, draw 1"), ("SOL_v2_d1", "GPT-5.6 Sol, draw 1"), ("OP5_v2_d1", "Opus 5, draw 1"), ("MINI5_v2_d1", "GPT-4.1 mini, draw 1 of five"),
            ("CR-nb1_v2", "Count reader, guessed category"), ("CR-oracle-a_v2", "Count reader, given category"), ("CR-oracle-state_v2", "State-aware count reader"),
            ("CR-totals-a_v2", "Totals reader"), ("CR-oracle-share_v2", "Category-given share reader (privileged)"), ("WHOLEMAP_v2", "Whole name-map lookup"),
            ("HYBRID_v2", "Hybrid reader (E10)"), ("RANDTOK_v2", "Random-token lookup"), ("MPNET_v2", "Name lookup, all-mpnet-base-v2"), ("BGE_v2", "Name lookup, bge-small-en-v1.5"),
            ("LUNA5_P1_v2", "GPT-5.6 Luna, intent-explicit rubric"), ("MINI1_P1_v2", "GPT-4.1 mini, intent-explicit rubric"),
            ("H45_NAMES", "Haiku 4.5, names only (E2)"), ("H45_COUNTS", "Haiku 4.5, counts only (E2)"), ("MINI1_NAMES", "GPT-4.1 mini, names only (E2)"),
            ("MINI1_NAMES_DASH", "GPT-4.1 mini, names only, dash rule (E2)"), ("MINI1_COUNTS", "GPT-4.1 mini, counts only (E2)")]
TABLE_V3 = [("ALLSTATES_v3", "All-states lookup"), ("MINI1_v3", "GPT-4.1 mini, one draw (t = 0)"), ("MINI5_v3", "GPT-4.1 mini, five draws (Table 1's row)"), ("H45_v3", "Haiku 4.5"),
            ("OP5_v3", "Opus 5"), ("OP5_v3_d1", "Opus 5, draw 1"), ("MINI5_v3_d1", "GPT-4.1 mini, draw 1 of five"), ("RANDTOK_v3", "Random-token lookup"),
            ("MPNET_v3", "All-states lookup, all-mpnet-base-v2"), ("BGE_v3", "All-states lookup, bge-small-en-v1.5")]
TABLE_V2R = [("MINI1_v2r", "GPT-4.1 mini, one draw (t = 0)"), ("H45_v2r", "Haiku 4.5"), ("OP5_v2r", "Opus 5"), ("CR-totals-a_v2r", "Totals reader (the permuted lines)"),
             ("CR-oracle-a_v2r", "Count reader, given category (unchanged)"), ("CR-nb1_v2r", "Count reader, guessed category (unchanged)")]
TABLE_CAT = [("MINI1_v2rcat", "GPT-4.1 mini, one draw"), ("H45_v2rcat", "Haiku 4.5, five draws"), ("OP5_v2rcat", "Opus 5, five draws (E1 Amendment 1)"), ("OP5_v2rcat_d1", "Opus 5, draw 1"),
             ("LUNA_v2rcat", "GPT-5.6 Luna, five draws (E9)"), ("LUNA_v2rcat_d1", "GPT-5.6 Luna, draw 1"), ("SOL_v2rcat", "GPT-5.6 Sol, five draws (E9)"), ("SOL_v2rcat_d1", "GPT-5.6 Sol, draw 1"),
             ("CR-oracle-state_v2rcat", "State-aware count reader"), ("CR-totals-a_v2rcat", "Totals reader"), ("CR-oracle-a_v2rcat", "Count reader, given category"),
             ("CR-nb1_v2rcat", "Count reader, guessed category"), ("CR-oracle-share_v2rcat", "Category-given share reader")]


def f4(x):
    return "—" if x is None else f"{x:.4f}"


def sci(d):
    return f"[{d['ci_lo']:.4f}, {d['ci_hi']:.4f}]"


def dci(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"


def wtl(b):
    return f"{b['W']}/{b['T']}/{b['L']}"


def rel(p):
    return "**reliable**" if p["both_exclude_zero"] else ("disagree" if not p["agree"] else "no")


def table_summary(res, rows, title):
    R = res["readers"]
    L = [f"### {title}", "",
         "| reader | pooled (whole) | pooled sup / ret / exp | state-balanced | PN vs PRESENT W/T/L | matched (whole) | triple interval | persona interval | matched sup / ret / exp | PN vs ABSENT W/T/L | matched (whole) | matched sup / ret / exp |",
         "|---|---:|---|---:|---|---:|---|---|---|---|---:|---|"]
    for key, label in rows:
        r = R[key]; po = r["pooled"]; pp = r["pn_vs_present"]; pa = r["pn_vs_absent"]
        L.append(f"| {label} | {f4(po['whole'])} | {' / '.join(f4(po['per_state'][s]) for s in STATES)} | {f4(po['state_balanced'])} | {wtl(pp['whole'])} | {f4(pp['whole']['matched'])} | "
                 f"{sci(pp['whole']['ci_triple'])} | {sci(pp['whole']['ci_persona'])} | {' / '.join(f4(pp['per_state'][s]['matched']) for s in STATES)} | {wtl(pa['whole'])} | {f4(pa['whole']['matched'])} | "
                 f"{' / '.join(f4(pa['per_state'][s]['matched']) for s in STATES)} |")
    return L


def table_perstate_intervals(res, rows, title):
    R = res["readers"]
    L = [f"### {title}: per-state matched PN vs PRESENT with both intervals (W/T/L per state)", "",
         "| reader | sup W/T/L | sup matched | triple | persona | ret W/T/L | ret matched | triple | persona | exp W/T/L | exp matched | triple | persona |", "|---|---|---:|---|---|---|---:|---|---|---|---:|---|---|"]
    for key, label in rows:
        pp = R[key]["pn_vs_present"]["per_state"]
        L.append(f"| {label} | " + " | ".join(f"{wtl(pp[s])} | {f4(pp[s]['matched'])} | {sci(pp[s]['ci_triple'])} | {sci(pp[s]['ci_persona'])}" for s in STATES) + " |")
    return L


def table_classes(res, rows, title):
    R = res["readers"]
    L = [f"### {title}: the pooled AUROC decomposed by pair class (whole set; pair counts within-triple 296, same-state across questions 18,792, across states 24,720 of 43,808)", "",
         "| reader | pooled | within-triple (296) | same state, across questions (18,792) | across states (24,720) | state-balanced pooled |", "|---|---:|---:|---:|---:|---:|"]
    for key, label in rows:
        pc = R[key]["pair_classes"]["whole"]
        L.append(f"| {label} | {f4(pc['pooled'])} | {f4(pc['within_triple']['auroc'])} | {f4(pc['same_state_across_questions']['auroc'])} | {f4(pc['across_states']['auroc'])} | {f4(R[key]['pooled']['state_balanced'])} |")
    return L


def table_vs_lookup(res, rows, title):
    P = res["paired"]["vs_lookup"]
    L = [f"### {title}: each reader minus its summary's lookup under the matched metric, PN vs PRESENT (whole set; supersession only; the counted states beside), triple and persona intervals", "",
         "| reader | lookup | whole Δ | triple | persona | reliable | sup Δ | triple | persona | reliable | ret Δ | exp Δ | PN vs ABSENT whole Δ | triple | persona | reliable |", "|---|---|---:|---|---|---|---:|---|---|---|---:|---:|---:|---|---|---|"]
    for key, label in rows:
        if key not in P:
            continue
        d = P[key]; w = d["pn_vs_present"]["whole"]; s = d["pn_vs_present"]["per_state"]["SUPERSESSION"]; r_ = d["pn_vs_present"]["per_state"]["RETRACTION"]; e = d["pn_vs_present"]["per_state"]["EXPIRY"]
        a = d["pn_vs_absent"]["whole"]
        L.append(f"| {label} | {d['lookup']} | {w['delta']:+.4f} | {dci(w['ci_triple'])} | {dci(w['ci_persona'])} | {rel(w)} | {s['delta']:+.4f} | {dci(s['ci_triple'])} | {dci(s['ci_persona'])} | {rel(s)} | "
                 f"{r_['delta']:+.4f}{'*' if r_['both_exclude_zero'] else ''} | {e['delta']:+.4f}{'*' if e['both_exclude_zero'] else ''} | {a['delta']:+.4f} | {dci(a['ci_triple'])} | {dci(a['ci_persona'])} | {rel(a)} |")
    return L


def table_vs_count(res, rows, title):
    P = res["paired"]["vs_count_readers"]
    crs = ("CR-nb1", "CR-oracle-a", "CR-oracle-state", "CR-totals-a", "CR-oracle-share")
    names = {"CR-nb1": "guessed category", "CR-oracle-a": "given category", "CR-oracle-state": "state-aware", "CR-totals-a": "totals", "CR-oracle-share": "given share"}
    L = [f"### {title}: each reader minus each count reader on retraction and on expiry, matched PN vs PRESENT (Δ; triple interval; persona interval; * = both intervals exclude zero)", "",
         "| reader | " + " | ".join(f"minus {names[c]}: ret | exp" for c in crs) + " |", "|---|" + "---|---|" * len(crs)]
    for key, label in rows:
        if key not in P:
            continue
        cells = []
        for c in crs:
            d = P[key][c]["pn_vs_present"]
            for s in ("RETRACTION", "EXPIRY"):
                x = d[s]
                cells.append(f"{x['delta']:+.4f}{'*' if x['both_exclude_zero'] else ''} {dci(x['ci_triple'])} {dci(x['ci_persona'])}")
        L.append(f"| {label} | " + " | ".join(cells) + " |")
    return L


def table_contrasts(res):
    P = res["paired"]["contrasts"]
    L = ["### The named contrasts (A minus B) under the matched metric, PN vs PRESENT: Δ with the triple and the persona interval per scope; * = both intervals exclude zero", "",
         "| contrast | whole | sup | ret | exp | counted (ret + exp, 60 triples) |", "|---|---|---|---|---|---|"]
    for name, d in P.items():
        p = d["pn_vs_present"]
        L.append(f"| {name} | " + " | ".join(f"{p[sc]['delta']:+.4f}{'*' if p[sc]['both_exclude_zero'] else ''} {dci(p[sc]['ci_triple'])} {dci(p[sc]['ci_persona'])}" for sc in ("whole", "sup", "ret", "exp", "counted")) + " |")
    L += ["", "The same contrasts, PN vs ABSENT:", "", "| contrast | whole | sup | ret | exp | counted |", "|---|---|---|---|---|---|"]
    for name, d in P.items():
        p = d["pn_vs_absent"]
        L.append(f"| {name} | " + " | ".join(f"{p[sc]['delta']:+.4f}{'*' if p[sc]['both_exclude_zero'] else ''} {dci(p[sc]['ci_triple'])} {dci(p[sc]['ci_persona'])}" for sc in ("whole", "sup", "ret", "exp", "counted")) + " |")
    return L


def table_opus_v3(res):
    P = res["paired"]["opus_v3_vs_allstates"]
    L = ["### Opus 5 under the all-states summary minus the all-states lookup, matched PN vs PRESENT (and PN vs ABSENT), whole set and per state", "",
         "| row | comparison | whole Δ | triple | persona | reliable | sup Δ | triple | persona | ret Δ | triple | persona | exp Δ | triple | persona |", "|---|---|---:|---|---|---|---:|---|---|---:|---|---|---:|---|---|"]
    for key, label in (("OP5_v3", "Opus 5, five draws"), ("OP5_v3_d1", "Opus 5, draw 1")):
        for neg in ("pn_vs_present", "pn_vs_absent"):
            d = P[key][neg]; w = d["whole"]
            L.append(f"| {label} | {neg.replace('_', ' ')} | {w['delta']:+.4f} | {dci(w['ci_triple'])} | {dci(w['ci_persona'])} | {rel(w)} | " +
                     " | ".join(f"{d['per_state'][s]['delta']:+.4f}{'*' if d['per_state'][s]['both_exclude_zero'] else ''} | {dci(d['per_state'][s]['ci_triple'])} | {dci(d['per_state'][s]['ci_persona'])}" for s in STATES) + " |")
    return L


def sanity_lines(res):
    S = res["sanity"]
    L = ["| row | where | printed W/T/L | computed W/T/L | (W + T/2) / 148 | ok |", "|---|---|---|---|---:|---|"]
    for k, v in S.items():
        if k == "all_ok" or "/" in k:
            continue
        L.append(f"| {k} | {v['where']} | {'/'.join(map(str, v['printed']))} | {'/'.join(map(str, v['computed']))} | {v['matched_from_printed']:.4f} | {'yes' if v['ok'] else 'NO'} |")
    for k, v in S.items():
        if "/" in k:
            L.append(f"| {k} | {v['where']} | pooled {v['recorded_pooled']:.4f} | computed {v['computed']:.4f} | | {'yes' if v['ok'] else 'NO'} |")
    return L


def write_fig3(res):
    R = res["readers"]
    m = lambda k, s: R[k]["pn_vs_present"]["per_state"][s]["matched"]  # noqa: E731
    sup = {"mini": "MINI5_v2", "haiku": "H45_v2", "luna": "LUNA_v2", "sol": "SOL_v2", "opus": "OP5_v2", "lookup": "LOOKUP_v2", "count": "CR-nb1_v2"}
    allst = {"mini": "MINI5_v3", "haiku": "H45_v3", "opus": "OP5_v3", "lookup": "ALLSTATES_v3"}
    L = ["%% fig3_data_matched.tex -- Figure 3's data ON THE MATCHED METRIC, written by reviews/r125/tools/r125_t1_report.py from reviews/r125/results/r125_matched.json (R125, Task 1); do not edit by hand.",
         "%% The same schema as reviews/v22/src/fig3_data.tex (\\figthreeSup, \\figthreeAll; x: 0 supersession, 1 retraction, 2 expiry). Every value is the within-triple matched AUROC (W + T/2) / n of the",
         "%% PN version against the PRESENT version, over the state's own triples (88 / 30 / 30), four decimals. Post hoc. Sources (reader keys of r125_matched.json 'readers'):"]
    for name, key in list(sup.items()) + [(k + " (all states)", v) for k, v in allst.items()]:
        L.append(f"%%   {name:22s} {key}: " + ", ".join(f"{s.lower()} {m(key, s):.4f} ({R[key]['pn_vs_present']['per_state'][s]['W']}/{R[key]['pn_vs_present']['per_state'][s]['T']}/{R[key]['pn_vs_present']['per_state'][s]['L']})" for s in STATES))
    L.append("\\pgfplotstableread[col sep=comma]{")
    L.append("x,state," + ",".join(sup))
    for i, s in enumerate(STATES):
        L.append(f"{i},{s.title()}," + ",".join(f"{m(sup[r], s):.4f}" for r in sup))
    L.append("}\\figthreeSup")
    L.append("\\pgfplotstableread[col sep=comma]{")
    L.append("x,state," + ",".join(allst))
    for i, s in enumerate(STATES):
        L.append(f"{i},{s.title()}," + ",".join(f"{m(allst[r], s):.4f}" for r in allst))
    L.append("}\\figthreeAll")
    FIG3.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    return L


def main():
    res = C.jload(RES)
    cov = res["coverage_only"]
    head = ["# R125 Task 1 — the matched metric on the counterfactual set (post hoc, offline, $0)", "",
            f"Every number from `reviews/r125/results/r125_matched.json` (`r125_matched.py`, {res['meta']['seconds']} s) on the vectors of `r125_vectors.json` (`r125_readers.py`; every gated reader "
            "reproduces its recorded whole-set pooled AUROC at four decimals). **Matched AUROC** = (W + T/2) / n over the triples, the PN version's score against the PRESENT version's (primary) "
            "or the ABSENT version's, within the triple; ties are exact equality of the collapsed scores, as the printed W/T/L count them. Intervals: the triple-level bootstrap and the persona-grouped "
            "bootstrap (triples intact), 1,000 draws, seed 42; **reliable** = both exclude zero. Pooled = the recorded Mann-Whitney AUROC over the 444 (whole) or within the state's own items (per state); "
            "state-balanced = the mean of the three per-state pooled values. Every row is post hoc and labelled so.", "",
            f"The coverage-only reader (1 on PN and PRESENT, 0 on ABSENT) scores {cov['pooled']['whole']:.4f} pooled, {cov['pn_vs_present']['matched']:.4f} matched PN vs PRESENT "
            f"({cov['pn_vs_present']['W']}/{cov['pn_vs_present']['T']}/{cov['pn_vs_present']['L']}), {cov['pn_vs_absent']['matched']:.4f} matched PN vs ABSENT; its pair classes read "
            f"{cov['pair_classes']['within_triple']['auroc']:.4f} within-triple, {cov['pair_classes']['same_state_across_questions']['auroc']:.4f} same-state, {cov['pair_classes']['across_states']['auroc']:.4f} across states.", "",
            "## 0. The sanity check (Task 1's stop rule): the printed W/T/L reproduce from the rows", ""] + sanity_lines(res) + [""]
    body = []
    body += ["## 1. The superseded-only summary (v2) and the readers of its texts", ""] + table_summary(res, TABLE_V2, "Superseded-only summary: whole set and per state") + [""]
    body += table_perstate_intervals(res, TABLE_V2, "Superseded-only summary") + [""]
    body += table_classes(res, TABLE_V2, "Superseded-only summary") + [""]
    body += ["## 2. The all-states summary (v3)", ""] + table_summary(res, TABLE_V3, "All-states summary: whole set and per state") + [""]
    body += table_perstate_intervals(res, TABLE_V3, "All-states summary") + [""] + table_classes(res, TABLE_V3, "All-states summary") + [""]
    body += ["## 3. The totals-randomized summary (v2r)", ""] + table_summary(res, TABLE_V2R, "Totals-randomized summary: whole set and per state") + [""]
    body += table_perstate_intervals(res, TABLE_V2R, "Totals-randomized summary") + [""] + table_classes(res, TABLE_V2R, "Totals-randomized summary") + [""]
    body += ["## 4. The moved-count control (v2r-cat; E1 Amendment 1, E9)", ""] + table_summary(res, TABLE_CAT, "Moved-count control: whole set and per state") + [""]
    body += table_perstate_intervals(res, TABLE_CAT, "Moved-count control") + [""] + table_classes(res, TABLE_CAT, "Moved-count control") + [""]
    body += ["## 5. Paired differences", ""] + table_vs_lookup(res, TABLE_V2 + TABLE_V3 + TABLE_V2R + TABLE_CAT, "Against the lookup") + [""]
    body += table_vs_count(res, TABLE_V2 + TABLE_V3 + TABLE_V2R + TABLE_CAT, "Against the count readers") + [""]
    body += table_opus_v3(res) + [""] + ["## 6. The named contrasts", ""] + table_contrasts(res) + [""]
    TABLES.write_text("\n".join(head + body) + "\n", encoding="utf-8", newline="\n")
    fig = write_fig3(res)
    # ---- the ledger section (section 15 of NUMBERS_CF2.md), between markers
    sec = [BEGIN, "",
           "## 15. AUX-CF2-R125-T1 — the matched metric (program R125, Task 1; 2026-09-20; post hoc, offline, no model call; `reviews/r125/tools/r125_readers.py`, `r125_matched.py`, `r125_t1_report.py`; `reviews/r125/results/r125_vectors.json`, `r125_matched.json`; tables `reviews/r125/T1_TABLES.md`; Figure 3 data on the matched metric `reviews/r125/results/fig3_data_matched.tex`)", "",
           "Matched AUROC = (W + T/2) / n within the triple (PN against PRESENT, the primary; PN against ABSENT beside), ties exact equality of the collapsed scores; the triple-level and the persona-grouped bootstrap (1,000 draws, seed 42); reliable = both intervals exclude zero. Every gated reader reproduced its recorded pooled row at four decimals before scoring. Every row here is post hoc and labelled so.", "",
           "### AUX-CF2-R125-SANITY — the printed W/T/L of Table 1 (tab:cf-main, v22 sha f0549e2a) and of the appendix reproduce from the rows: " + ("**PASS** (every row)" if res["sanity"]["all_ok"] else "**FAIL**"), ""] + sanity_lines(res) + ["",
           "### AUX-CF2-R125-MATCHED-V2, -V3, -V2R, -V2RCAT — every reader under the matched metric (whole set and per state; the pooled row and the state-balanced pooled row beside)", ""]
    sec += table_summary(res, TABLE_V2, "AUX-CF2-R125-MATCHED-V2 — the superseded-only summary and the readers of its texts") + [""]
    sec += table_summary(res, TABLE_V3, "AUX-CF2-R125-MATCHED-V3 — the all-states summary") + [""]
    sec += table_summary(res, TABLE_V2R, "AUX-CF2-R125-MATCHED-V2R — the totals-randomized summary") + [""]
    sec += table_summary(res, TABLE_CAT, "AUX-CF2-R125-MATCHED-V2RCAT — the moved-count control") + [""]
    sec += ["### AUX-CF2-R125-PERSTATE — per-state matched PN vs PRESENT with both intervals", ""]
    for rows, t in ((TABLE_V2, "v2"), (TABLE_V3, "v3"), (TABLE_V2R, "v2r"), (TABLE_CAT, "v2rcat")):
        sec += table_perstate_intervals(res, rows, t) + [""]
    sec += ["### AUX-CF2-R125-CLASSES — the pooled AUROC by pair class", ""]
    for rows, t in ((TABLE_V2, "v2"), (TABLE_V3, "v3"), (TABLE_V2R, "v2r"), (TABLE_CAT, "v2rcat")):
        sec += table_classes(res, rows, t) + [""]
    sec += ["### AUX-CF2-R125-VS-LOOKUP — each reader minus its summary's lookup", ""] + table_vs_lookup(res, TABLE_V2 + TABLE_V3 + TABLE_V2R + TABLE_CAT, "all summaries") + [""]
    sec += ["### AUX-CF2-R125-VS-COUNT — each reader minus each count reader on the counted states", ""] + table_vs_count(res, TABLE_V2 + TABLE_V3 + TABLE_V2R + TABLE_CAT, "all summaries") + [""]
    sec += ["### AUX-CF2-R125-OP5-V3 — Opus 5 under the all-states summary minus the all-states lookup", ""] + table_opus_v3(res) + [""]
    sec += ["### AUX-CF2-R125-CONTRASTS — the named contrasts", ""] + table_contrasts(res) + [""]
    sec += ["### AUX-CF2-R125-FIG3 — Figure 3's data on the matched metric (`reviews/r125/results/fig3_data_matched.tex`)", "", "```"] + fig + ["```", "", END]
    text = C.LEDGER.read_text(encoding="utf-8")
    block = "\n".join(sec) + "\n"
    if BEGIN in text:
        text = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", lambda m: block, text, flags=re.S)
    else:
        text = text.rstrip("\n") + "\n\n" + block
    C.LEDGER.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {TABLES.relative_to(C.ROOT)}, {FIG3.relative_to(C.ROOT)}, section 15 of {C.LEDGER.relative_to(C.ROOT)}")


if __name__ == "__main__":
    main()
