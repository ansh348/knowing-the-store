# -*- coding: utf-8 -*-
"""fig3_data.py -- Figure 3's data file, reviews/v22/src/fig3_data.tex, written from the recorded artifacts (program R126, Phase 3; 2026-09-19).

The figure (reviews/v22/tools/port_v22.py, FIG3) is drawn in pgfplots from the two pgfplots tables this file defines, \\figthreeSup (the
summary naming supersession only) and \\figthreeAll (the summary naming all states); it is provisional and is redrawn on the matched metric
when R125 reports, by swapping this file alone. Every value is the per-state obligation AUROC within the state's own items (cf2_score), read
by key from its artifact, four decimals, no rounding:

  GPT-4.1 mini      reviews/r122/results/scores_r122_oai.json  T3/INDEXED-V2|V3/new/per_state   (AUX-R122-K5-ROWS: the five-draw rows)
  Haiku 4.5, Opus 5 r82_counterfactual/cf2/results/cf_scores_cf2.json  lanes/<model>/v2|v3/per_state  (AUX-CF2-H45-V2/-V3, AUX-CF2-OP5-V2/-V3, AUX-CF2-PERSTATE)
  GPT-5.6 Luna, Sol r82_counterfactual/cf2/results/cf_scores_openai.json  models/<model>/per_state  (AUX-CF2-OAI-LUNA-V2, -SOL-V2; superseded-only summary only)
  name lookup       cf_scores_cf2.json  baselines/NB6-superseded-names-v2 and all-states-names-v3 /per_state  (AUX-CF2-NB6-V2, AUX-CF2-ALLSTATES-V3)
  count reader      reviews/v18/results/a1_count_readers.json  cf444/summaries/v2/readers/CR-nb1/per_state  (AUX-R110-A1-CR: the category-guessing reader)

Usage: python reviews/v22/tools/fig3_data.py   (writes the file and prints every value with its source path)
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews" / "v22" / "src" / "fig3_data.tex"
STATES = ["SUPERSESSION", "RETRACTION", "EXPIRY"]


def load(rel):
    return json.load(open(ROOT / rel, encoding="utf-8"))


def auroc(x):
    """The per-state AUROC as each artifact records it: a bare number, an 'auroc' field, or the 'indexed' field of a lane row."""
    if isinstance(x, dict):
        return x["auroc"] if "auroc" in x else x["indexed"]
    return x


def main():
    k5 = load("reviews/r122/results/scores_r122_oai.json")["T3"]
    cf2 = load("r82_counterfactual/cf2/results/cf_scores_cf2.json")
    oai = load("r82_counterfactual/cf2/results/cf_scores_openai.json")["models"]
    cr = load("reviews/v18/results/a1_count_readers.json")["cf444"]["summaries"]["v2"]["readers"]["CR-nb1"]["per_state"]
    sup = {
        "mini": ("scores_r122_oai.json T3/INDEXED-V2/new/per_state", {s: auroc(k5["INDEXED-V2"]["new"]["per_state"][s]) for s in STATES}),
        "haiku": ("cf_scores_cf2.json lanes/claude-haiku-4-5-20251001/v2/per_state", {s: auroc(cf2["lanes"]["claude-haiku-4-5-20251001"]["v2"]["per_state"][s]) for s in STATES}),
        "luna": ("cf_scores_openai.json models/gpt-5.6-luna/per_state", {s: auroc(oai["gpt-5.6-luna"]["per_state"][s]) for s in STATES}),
        "sol": ("cf_scores_openai.json models/gpt-5.6-sol/per_state", {s: auroc(oai["gpt-5.6-sol"]["per_state"][s]) for s in STATES}),
        "opus": ("cf_scores_cf2.json lanes/claude-opus-5/v2/per_state", {s: auroc(cf2["lanes"]["claude-opus-5"]["v2"]["per_state"][s]) for s in STATES}),
        "lookup": ("cf_scores_cf2.json baselines/NB6-superseded-names-v2/per_state", {s: auroc(cf2["baselines"]["NB6-superseded-names-v2"]["per_state"][s]) for s in STATES}),
        "count": ("a1_count_readers.json cf444/summaries/v2/readers/CR-nb1/per_state", {s: auroc(cr[s]) for s in STATES}),
    }
    allst = {
        "mini": ("scores_r122_oai.json T3/INDEXED-V3/new/per_state", {s: auroc(k5["INDEXED-V3"]["new"]["per_state"][s]) for s in STATES}),
        "haiku": ("cf_scores_cf2.json lanes/claude-haiku-4-5-20251001/v3/per_state", {s: auroc(cf2["lanes"]["claude-haiku-4-5-20251001"]["v3"]["per_state"][s]) for s in STATES}),
        "opus": ("cf_scores_cf2.json lanes/claude-opus-5/v3/per_state", {s: auroc(cf2["lanes"]["claude-opus-5"]["v3"]["per_state"][s]) for s in STATES}),
        "lookup": ("cf_scores_cf2.json baselines/all-states-names-v3/per_state", {s: auroc(cf2["baselines"]["all-states-names-v3"]["per_state"][s]) for s in STATES}),
    }
    L = ["%% fig3_data.tex -- Figure 3's data, written by reviews/v22/tools/fig3_data.py from the recorded artifacts (R126, Phase 3); do not edit by hand.",
         "%% Provisional: redrawn on the matched metric when R125 reports, by regenerating this file. Per-state obligation AUROC within the state's own items.",
         "%% x: 0 supersession, 1 retraction, 2 expiry. Sources (four decimals, as recorded):"]
    for name, (src, vals) in list(sup.items()) + [(k + " (all states)", v) for k, v in allst.items()]:
        L.append(f"%%   {name:22s} {src}: " + ", ".join(f"{s.lower()} {vals[s]:.4f}" for s in STATES))
    L.append("\\pgfplotstableread[col sep=comma]{")
    L.append("x,state," + ",".join(sup))
    for i, s in enumerate(STATES):
        L.append(f"{i},{s.title()}," + ",".join(f"{sup[r][1][s]:.4f}" for r in sup))
    L.append("}\\figthreeSup")
    L.append("\\pgfplotstableread[col sep=comma]{")
    L.append("x,state," + ",".join(allst))
    for i, s in enumerate(STATES):
        L.append(f"{i},{s.title()}," + ",".join(f"{allst[r][1][s]:.4f}" for r in allst))
    L.append("}\\figthreeAll")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
