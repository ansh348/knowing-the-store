# -*- coding: utf-8 -*-
"""ledger_r117_tables.py -- program R118: the appendix tables of the R117 results, written from the result JSONs (never typed by hand):
  tab:cf-names-counts  E2, from r82_counterfactual/cf2/results/cf_scores_nc.json (AUX-CF2-NC-*)
  tab:marker           E3, from e1_metamemory/marker/scores_marker.json (AUX-MARKER-*)
  tab:ds-a8            E4, from ds_downstream/run/scores_amend8.json and lock_amend8.json (AUX-DS-A8-*)
  Table 1 rows and tab:pnpresent rows for GPT-5.6 Sol and Luna, from r82_counterfactual/cf2/results/cf_scores_openai.json (AUX-CF2-OAI-*)
Writes reviews/v21/src/r117_tables_v21.tex (the record; r118_apply.py splices its blocks at the anchors). No model call.
"""
from __future__ import annotations

import io
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews" / "v21" / "src" / "r117_tables_v21.tex"


def J(p):
    return json.load(io.open(ROOT / p, encoding="utf-8"))


def ci(p, key="persona_ci"):
    return f"$[{p[key]['ci_lo']:+.4f},{p[key]['ci_hi']:+.4f}]$"


def ci_abs(c):
    return f"$[{c['ci_lo']:.4f},{c['ci_hi']:.4f}]$"


def d2(x):
    return f"{x:.2f}"


def main():
    B = {}
    # ---- E2
    e2 = J("r82_counterfactual/cf2/results/cf_scores_nc.json")
    L = ["%% R118: tab:cf-names-counts, written by reviews/v21/tools/ledger_r117_tables.py from r82_counterfactual/cf2/results/cf_scores_nc.json (AUX-CF2-NC-MINI-NAMES, -MINI-NAMES-DASH, -MINI-COUNTS, -H45-NAMES, -H45-COUNTS, -PERSTATE); do not edit by hand.",
         "\\begin{table}[H]",
         "\\caption{Names against counts on the counterfactual set (E2; registered, ADDENDUM\\_CF2\\_NAMES\\_COUNTS). The superseded-only summary with every count line removed (names only), with the two name blocks removed (counts only), and, for GPT-4.1 mini, with every count replaced by a dash (the committed names-only rule of the pooled hard tier). The recorded intact row is the comparator; differences carry the item-level and the persona-grouped interval. Both readers stay within tolerance of the intact summary without the counts and fall reliably without the names (P-N1 and P-N2 held).}",
         "\\label{tab:cf-names-counts}", "\\centering\\tiny\\setlength{\\tabcolsep}{1.5pt}",
         "\\begin{tabular}{@{}llrlrrrrr@{}}", "\\toprule",
         "Reader & summary & AUROC & persona interval & minus intact & item interval & persona interval & retraction & expiry \\\\", "\\midrule"]
    NAMES = {"gpt-4.1-mini": "GPT-4.1 mini", "claude-haiku-4-5-20251001": "Haiku 4.5"}
    ARMN = {"INDEXED-NAMES": "names only", "INDEXED-COUNTS": "counts only", "INDEXED-NAMES-DASH": "names only, dash rule"}
    for lane, out in e2["readers"].items():
        L.append(f"{NAMES[lane]} & intact (recorded) & ${out['v2_recorded']:.4f}$ & & & & & & \\\\")
        for arm, r in out["arms"].items():
            v = r["vs_v2"]; ps = r["per_state"]
            L.append(f" & {ARMN[arm]} & ${r['whole']:.4f}$ & {ci_abs(r['whole_ci_persona'])} & ${v['delta']:+.4f}$ & {ci(v, 'item_ci')} & {ci(v)} & ${ps['RETRACTION']['auroc']:.4f}$ & ${ps['EXPIRY']['auroc']:.4f}$ \\\\")
        c = out["counts_minus_names"]
        L.append(f" & counts only minus names only & & & ${c['delta']:+.4f}$ & {ci(c, 'item_ci')} & {ci(c)} & & \\\\")
        L.append("\\addlinespace[1pt]")
    L += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
    B["e2"] = "\n".join(L)
    # ---- E3
    e3 = J("e1_metamemory/marker/scores_marker.json")
    L = ["%% R118: tab:marker, written by reviews/v21/tools/ledger_r117_tables.py from e1_metamemory/marker/scores_marker.json (AUX-MARKER-OMITTED-MINI, -NEUTRAL-MINI, -LUNA-66, -MODAL); do not edit by hand.",
         "\\begin{table}[H]",
         "\\caption{The inexpressibility marker on the two structureless stores (E3; registered, ADDENDUM\\_MARKER\\_ABLATION): coverage AUROC under the constrained rendering (structural), with the three inexpressible sections omitted (the recorded omitted arm of the main study), and with the marker's three lines reworded to say the store does not record the field (neutral), against blind. GPT-4.1 mini on each store's coverage population at one call; GPT-5.6 Luna on the pooled $66$ questions through the raw API at five calls, with its recorded harness rows beside. Differences against blind carry the item-level and the persona-grouped interval. The modal share is the fraction of items at the most common score.}",
         "\\label{tab:marker}", "\\centering\\tiny\\setlength{\\tabcolsep}{2pt}",
         "\\begin{tabular}{@{}lllrlrrrr@{}}", "\\toprule",
         "Reader & store & summary & AUROC & persona interval & minus blind & item interval & persona interval & modal share \\\\", "\\midrule"]
    ARM3 = {"BLIND": "blind", "STRUCTURAL": "structural", "OMITTED": "omitted", "NEUTRAL": "neutral"}
    for be, name in (("mem0", "Mem0"), ("amem", "A-MEM")):
        row = e3["mini"][be]
        for arm in ("BLIND", "STRUCTURAL", "OMITTED", "NEUTRAL"):
            a = row["arms"][arm]; v = a["vs_blind"]
            L.append(f"{'GPT-4.1 mini' if arm == 'BLIND' else ''} & {name if arm == 'BLIND' else ''} & {ARM3[arm]} & ${a['auroc']:.4f}$ & {ci_abs(a['ci_persona'])} & " + (f"${v['delta']:+.4f}$ & {ci(v, 'item_ci')} & {ci(v)}" if v else " & & ") + f" & ${a['modal_share']:.4f}$ \\\\")
        L.append("\\addlinespace[1pt]")
    Lu = e3["luna66"]
    for arm in ("BLIND", "STRUCTURAL", "OMITTED", "NEUTRAL"):
        a = Lu["arms"][arm]; v = a["vs_blind"]
        L.append(f"{'GPT-5.6 Luna, raw API' if arm == 'BLIND' else ''} & {'pooled $66$' if arm == 'BLIND' else ''} & {ARM3[arm]} & ${a['auroc']:.4f}$ & {ci_abs(a['ci_persona'])} & " + (f"${v['delta']:+.4f}$ & {ci(v, 'item_ci')} & {ci(v)}" if v else " & & ") + f" & ${a['modal_share']:.4f}$ \\\\")
    h = Lu["harness_recorded"]
    L.append(f"GPT-5.6 Luna, harness$^{{h}}$ & pooled $66$ & blind & ${h['blind']:.4f}$ & & & & & \\\\")
    L.append(f"(recorded) & & structural & ${h['structural']:.4f}$ & & ${h['delta']:+.4f}$ & & & \\\\")
    L += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
    B["e3"] = "\n".join(L)
    # ---- E4
    e4 = J("ds_downstream/run/scores_amend8.json"); lk = J("ds_downstream/run/lock_amend8.json")
    L = ["%% R118: tab:ds-a8, written by reviews/v21/tools/ledger_r117_tables.py from ds_downstream/run/scores_amend8.json and lock_amend8.json (AUX-DS-A8-RULE-CENSUS, -DUP35, -FALSEPROP, -STAGE2, -DIAGNOSIS); do not edit by hand.",
         "\\begin{table}[H]",
         "\\caption{Label propagation inside the view (E4; registered, DS Amendment 8). A rule that reads only the assembled view propagates a tagged line's lifecycle tag to the untagged lines of the same attribute that repeat it under the census function unchanged (shared tokens $\\ge 2$, cross guard $0.34$, coverage $\\ge 0.80$), with an age-field ordering (primary) or without it (secondary), under the ground-truth tags and under FR-Bank's own tags. Of the $272$ audited stale-line instances, $187$ sit under a different attribute key from their tagged twin, $45$ fall below $0.50$ coverage of any same-attribute tagged line, $40$ between $0.50$ and $0.80$, and none reaches the threshold. Detector counts; the re-answers under own tags are descriptive, no prediction was registered on them.}",
         "\\label{tab:ds-a8}", "\\centering\\tiny\\setlength{\\tabcolsep}{2pt}",
         "\\begin{tabular}{@{}lrrrr@{}}", "\\toprule",
         "Measure & GT tags, primary & GT tags, secondary & own tags, primary & own tags, secondary \\\\", "\\midrule"]
    keys = ["gt/primary", "gt/secondary", "own/primary", "own/secondary"]
    cen = lk["census"]; dup = lk["dup35"]; fp = lk["false_propagation"]
    L.append("Views changed, of $452$ & " + " & ".join(f"${cen[k.split('/')[0]][k.split('/')[1]]['changed']}$" for k in keys) + " \\\\")
    L.append("Lines propagated & " + " & ".join(f"${cen[k.split('/')[0]][k.split('/')[1]]['lines']}$" for k in keys) + " \\\\")
    L.append("Audited duplicate items fully tagged, of $35$ & " + " & ".join(f"${dup[k]['items_fully_tagged']}$" for k in keys) + " \\\\")
    L.append("False propagation on the licensed items' active lines & " + " & ".join(f"${fp[k]['false_propagations']}$ / ${fp[k]['active_lines_gt']}$ ($" + f"{100*fp[k]['share']:.2f}" + "\\%$)" for k in keys) + " \\\\")
    L.append("\\midrule")
    L.append("\\multicolumn{5}{@{}l}{\\textit{Re-answers on the changed views under own tags (before $\\to$ after; stale at $0.50$ over answered obligation views; correct licensed answers)}}\\\\")
    for code, name in (("MINI", "GPT-4.1 mini"), ("H45", "Haiku 4.5")):
        R = e4["answerers"][code]["by_source_policy"]
        cells = []
        for pol in ("ALWAYS", "MODEL", "ORACLE"):
            v = R[f"own/{pol}"]
            cells.append(f"{pol.lower() if pol != 'ALWAYS' else 'top-five'}: ${v['stale_gold_before']}$/${v['answered_before']}$ $\\to$ ${v['stale_gold_after']}$/${v['answered_after']}$; correct ${v['correct_before']} \\to {v['correct_after']}$")
        L.append(f"\\multicolumn{{5}}{{@{{}}l@{{}}}}{{{name}: " + "; ".join(cells) + "}} \\\\")   # one full-width line per answerer (the four-column span overflowed by 19pt)
    L += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
    B["e4"] = "\n".join(L)
    # ---- E5: Table 1 rows and tab:pnpresent rows
    e5 = J("r82_counterfactual/cf2/results/cf_scores_openai.json")["models"]
    rows1 = []
    pn = []
    for m, name in (("gpt-5.6-sol", "GPT-5.6 Sol"), ("gpt-5.6-luna", "GPT-5.6 Luna")):
        r = e5[m]; c = r["whole_ci_persona"]; ph = r["posthoc"]["whole"]; o = ph["ordering"]
        rows1.append(f"{name}, sup.\\ only & ${d2(r['whole'])}$ & $[{d2(c['ci_lo'])},{d2(c['ci_hi'])}]$ & ${d2(ph['pn_vs_present'])}$ & ${o['wins']}/{o['ties']}/{o['losses']}$ \\\\")
        for scope, b, pooled in (("whole", ph, r["whole"]),) + tuple((s_, r["posthoc"]["per_state"][s_], r["per_state"][s_]["auroc"]) for s_ in ("SUPERSESSION", "RETRACTION", "EXPIRY")):
            oo = b["ordering"]; lab = {"whole": "whole", "SUPERSESSION": "sup.", "RETRACTION": "ret.", "EXPIRY": "exp."}[scope]
            pn.append(f"{name + ', sup.\\\\ only' if scope == 'whole' else ''} & {lab} & ${b['pn_vs_present']:.4f}$ & {ci_abs(b['pn_vs_present_ci_persona'])} & ${pooled:.4f}$ & ${oo['wins']}/{oo['ties']}/{oo['losses']}$ & ${oo['strict_win_fraction']:.4f}$ & {ci_abs(oo['ci_persona'])} \\\\")
        pn.append("\\addlinespace[1pt]")
    B["e5_table1_rows"] = "%% R118: the E5 rows (AUX-CF2-OAI-SOL-V2, -LUNA-V2, -PNPRESENT; r82_counterfactual/cf2/results/cf_scores_openai.json).\n" + "\n".join(rows1)
    B["e5_pnpresent_rows"] = "%% R118: the E5 rows, written by reviews/v21/tools/ledger_r117_tables.py from cf_scores_openai.json (AUX-CF2-OAI-PNPRESENT).\n" + "\n".join(pn)
    text = "\n\n".join(f"%%BLOCK {k}%%\n{v}\n%%END {k}%%" for k, v in B.items()) + "\n"
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)} with blocks {list(B)}")


if __name__ == "__main__":
    main()
