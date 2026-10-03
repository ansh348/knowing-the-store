# -*- coding: utf-8 -*-
"""ledger_hybrid_r124.py -- E10 (the hybrid reader; program R124, ruling E1): from r82_counterfactual/cf2/results/cf_scores_hybrid.json write
(1) section 14e of r82_counterfactual/cf2/NUMBERS_CF2.md (AUX-CF2-HYB-LOCK, -WHOLE, -PERSTATE, -VS-LOOKUP, -VS-NB1, -VS-MODELS, -COEF, -P-H1, -P-H2),
appended once (idempotent on the section heading), and (2) the C.2 table tab:cf-hybrid as a block in reviews/v21/src/r124_tables_v21.tex.
No number is typed by hand. Usage: python reviews/v21/tools/ledger_hybrid_r124.py
"""
from __future__ import annotations

import io
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
RES = ROOT / "r82_counterfactual" / "cf2" / "results" / "cf_scores_hybrid.json"
LEDGER = ROOT / "r82_counterfactual" / "cf2" / "NUMBERS_CF2.md"
OUT = ROOT / "reviews" / "v21" / "src" / "r124_tables_v21.tex"
STATES = ("SUPERSESSION", "RETRACTION", "EXPIRY")
ORDER = ("MINI", "H45", "OP5", "SOL", "LUNA")   # the study's order (cf2_hybrid.LANES); the JSON is key-sorted
HEAD = "### 14e. E10, the hybrid reader"


def fp(p):
    return f"{p['delta']:+.4f} ([{p['item_ci']['ci_lo']:+.4f}, {p['item_ci']['ci_hi']:+.4f}]; [{p['persona_ci']['ci_lo']:+.4f}, {p['persona_ci']['ci_hi']:+.4f}])"


def ci(d):
    return f"$[{d['ci_lo']:+.4f},{d['ci_hi']:+.4f}]$"


def cia(d):
    return f"$[{d['ci_lo']:.4f},{d['ci_hi']:.4f}]$"


def main():
    d = json.load(io.open(RES, encoding="utf-8"))
    h = d["hybrid"]; o = h["posthoc"]["whole"]["ordering"]
    L = [f"{HEAD} (registrations/ADDENDUM_CF2_HYBRID_READER.md, frozen 2026-09-19 at fe6ff84, sha256 `{d['registration_sha256'][:16]}…`; scorer r82_counterfactual/tools/cf2_hybrid.py, sha256 `{d['scorer_sha256'][:16]}…`; results/cf_scores_hybrid.json; no model call)", "",
         "### AUX-CF2-HYB-LOCK", "",
         f"Gates before fitting: the name lookup on v2 {d['gates']['lookup_v2']} (AUX-CF2-NB6-V2), CR-nb1 {d['gates']['nb1_v2']} (AUX-R110-A1-CR); a category assigned on {d['features']['f3_assigned_items']} of 444 items. Model: {d['model']}.", "",
         "### AUX-CF2-HYB-WHOLE, AUX-CF2-HYB-PERSTATE", "",
         f"Whole set **{h['whole']:.4f}**, persona interval [{h['whole_ci_persona']['ci_lo']:.4f}, {h['whole_ci_persona']['ci_hi']:.4f}]; per state " + ", ".join(f"{s} **{h['per_state'][s]['auroc']:.4f}** (lookup {h['per_state'][s]['lookup']:.4f}, minus the lookup {fp(h['per_state'][s]['vs_lookup'])})" for s in STATES) + f"; counted states pooled {h['counted_pooled']:.4f}; PN vs PRESENT {h['posthoc']['whole']['pn_vs_present']:.4f}, W/T/L {o['wins']}/{o['ties']}/{o['losses']}; distinct values {h['distinct_values']}.", "",
         "### AUX-CF2-HYB-VS-LOOKUP, AUX-CF2-HYB-VS-NB1, AUX-CF2-HYB-VS-MODELS (paired, item-level; persona-grouped)", "",
         f"Hybrid minus the name lookup {fp(h['vs_lookup'])}; hybrid minus CR-nb1 {fp(d['vs_nb1'])}.", ""]
    for code in ORDER:
        m = d["models_minus_hybrid"][code]
        L.append(f"- {m['name']} ({m['model']:.4f}) minus the hybrid: {fp(m['minus_hybrid'])}")
    L += ["", "### AUX-CF2-HYB-COEF (the leave-persona-out fits: 40 folds; the range over folds)", "",
          "| coefficient | min | max |", "|---|---:|---:|"]
    for k, (lo, hi) in d["coefficient_range"].items():
        L.append(f"| {k} | {lo:+.4f} | {hi:+.4f} |")
    L += ["", "### AUX-CF2-HYB-P-H1, AUX-CF2-HYB-P-H2", "", f"**{d['predictions']['P-H1']['text']}**", "", f"**{d['predictions']['P-H2']['text']}**", ""]
    text = "\n".join(L) + "\n"
    led = io.open(LEDGER, encoding="utf-8").read()
    if HEAD in led:   # the last section of the file: regenerated whole from the same artifact
        led = led[:led.index(HEAD)].rstrip("\n") + "\n"
    io.open(LEDGER, "w", encoding="utf-8", newline="\n").write(led + "\n" + text)
    print("ledger section 14e written")
    # the C.2 table
    T = ["%% R124 E1: tab:cf-hybrid, written by reviews/v21/tools/ledger_hybrid_r124.py from r82_counterfactual/cf2/results/cf_scores_hybrid.json (NUMBERS_CF2.md section 14e, AUX-CF2-HYB-*); do not edit by hand.",
         "\\begin{table}[H]",
         "\\caption{A hybrid reader with no generative-model call on the counterfactual set (registered; ADDENDUM\\_CF2\\_HYBRID\\_READER): a logistic regression of the label on the name lookup's cosine, the category-guessing reader's share and an indicator that a category was assigned, fitted under leave-persona-out over the $40$ personas and scored out of fold, under the superseded-only summary. Upper panel: whole set and per state with the persona interval, and the paired differences against the name lookup and the category-guessing reader with both intervals. Lower panel: each model's recorded row minus the hybrid. Predicted before the run: that the hybrid exceeds the name lookup reliably (it does not: the item-level interval includes zero, a failed prediction) and that GPT-5.6 Sol stays reliably above it (as predicted). The fitted coefficients on the standardized features range over the folds from " + f"${d['coefficient_range']['f1_lookup'][0]:+.2f}$ to ${d['coefficient_range']['f1_lookup'][1]:+.2f}$ on the lookup and ${d['coefficient_range']['f2_share'][0]:+.2f}$ to ${d['coefficient_range']['f2_share'][1]:+.2f}$ on the share." + "}",
         "\\label{tab:cf-hybrid}",
         "\\centering\\tiny\\setlength{\\tabcolsep}{2pt}",
         "\\begin{tabular}{@{}lrlrll@{}}", "\\toprule",
         "Scope & hybrid & persona interval & minus the lookup & item interval & persona interval \\\\", "\\midrule",
         f"whole set & ${h['whole']:.4f}$ & {cia(h['whole_ci_persona'])} & ${h['vs_lookup']['delta']:+.4f}$ & {ci(h['vs_lookup']['item_ci'])} & {ci(h['vs_lookup']['persona_ci'])} \\\\"]
    for s in STATES:
        ps = h["per_state"][s]
        T.append(f"{s.lower()} & ${ps['auroc']:.4f}$ & -- & ${ps['vs_lookup']['delta']:+.4f}$ & {ci(ps['vs_lookup']['item_ci'])} & {ci(ps['vs_lookup']['persona_ci'])} \\\\")
    T.append(f"whole set, minus the category-guessing reader & & & ${d['vs_nb1']['delta']:+.4f}$ & {ci(d['vs_nb1']['item_ci'])} & {ci(d['vs_nb1']['persona_ci'])} \\\\")
    T += ["\\bottomrule", "\\end{tabular}\\\\[4pt]",
          "\\begin{tabular}{@{}lrrll@{}}", "\\toprule", "Model (recorded row) & model & minus the hybrid & item interval & persona interval \\\\", "\\midrule"]
    for code in ORDER:
        m = d["models_minus_hybrid"][code]
        T.append(f"{m['name']} & ${m['model']:.4f}$ & ${m['minus_hybrid']['delta']:+.4f}$ & {ci(m['minus_hybrid']['item_ci'])} & {ci(m['minus_hybrid']['persona_ci'])} \\\\")
    T += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
    io.open(OUT, "w", encoding="utf-8", newline="\n").write("%%BLOCK cf_hybrid%%\n" + "\n".join(T) + "\n%%END cf_hybrid%%\n")
    print("->", OUT)


if __name__ == "__main__":
    main()
