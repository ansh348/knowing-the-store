# -*- coding: utf-8 -*-
"""ledger_r134.py -- reviews/NUMBERS_R134.md (R134, 2026-09-21: the paraphrase check landed in v23): the printed forms the pass brings into the main text,
the abstract and the appendix prose, each beside the four-decimal value and the artifact key it comes from, written from the checks of
reviews/v23/tools/r134_number_gate.py (which reads the artifacts, not this file), so trace_scan_v13 resolves every printed token to a ledger row and a
reader can audit each rounding. The four-decimal table values print from cf2_paraphrase/results/para_tables.tex (para_tex.py) and are ledgered in
cf2_paraphrase/NUMBERS_PARA.md (AUX-PARA-*). No number is typed by hand.
Usage: python reviews/v23/tools/ledger_r134.py
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))
import r134_number_gate as G  # noqa: E402

OUT = ROOT / "reviews" / "NUMBERS_R134.md"


def main():
    rows = G.checks()
    bad = [c for c in rows if not c["ok"]]
    assert not bad, bad
    L = ["# NUMBERS_R134.md: the R134 pass (the paraphrase check landed in v23; 2026-09-21)", "",
         "Written by `reviews/v23/tools/ledger_r134.py` from the checks of `reviews/v23/tools/r134_number_gate.py`; every value is read from the artifact named "
         "(`cf2_paraphrase/results/para_scores.json`, `para_scores_all124.json`, `lookups.json`, `para_minus_lookup_posthoc.json`, `cf2_paraphrase/sheet.json`, "
         "`para_questions.json`; the abstract's inherited numbers from `reviews/r125/results/r125_matched.json`, `r82_counterfactual/cf2/NUMBERS_CF2.md`, "
         "`e1r_robustness/NUMBERS_E1R.md`, `r74/NUMBERS_R74.md`, `believed_h/NUMBERS_BELIEVED_H.md`). Printed forms are half-up on the four-decimal recorded value at two decimals "
         "(the convention of reviews/NUMBERS_R131.md), magnitudes with the direction in words; the appendix prose prints the two genericity descriptives at three decimals and Luna's two lower "
         "bounds at three (the author's ruling). The four-decimal values of the six appendix tables (tab:para-pooled, -matched, -minus-lookup, -sup, -sens, -flags) are written by "
         "`cf2_paraphrase/tools/para_tex.py` and ledgered in `cf2_paraphrase/NUMBERS_PARA.md` (AUX-PARA-LOOKUP-*, AUX-PARA-{MINI,H45,OP5,LUNA,SOL}-V2/V3, AUX-PARA-MATCHED-*, "
         "AUX-PARA-POSTHOC-MINUS-LOOKUP-*, AUX-PARA-FLAGS, AUX-PARA-SENS-*, AUX-PARA-GENERIC).", "",
         "## AUX-R134-PRINTED: every number and claim the pass's new texts print, beside its source", "",
         f"{len(rows)} checks, {len(bad)} mismatches (`r134_number_gate.py`).", "",
         "| where (the sentence) | printed | recorded value | reliable, claimed / actual | source |", "|---|---|---|---|---|"]
    for c in rows:
        v = c["value"]
        vs = f"{v:+.4f}" if isinstance(v, float) else str(v)
        rel = "" if c["reliable"] is None else f"{c['reliable']} / {c['actual_reliable']}"
        L.append(f"| {c['where']} | {c['printed']} | {vs} | {rel} | {c['source']} |")
    L += ["", "## AUX-R134-BRANCH: the branch of the brief's section 3 and the author's ruling", "",
          "Supersession only, paraphrase set, superseded-names summary, pooled AUROC, model minus the embedding lookup (`para_minus_lookup_posthoc.json` `models/*/v2/superseded/pooled/paraphrase`; "
          "AUX-PARA-POSTHOC-MINUS-LOOKUP-*-V2): " + "; ".join(f"{c} {G.SUP[c]['pooled']['paraphrase']['delta']:+.4f} [{G.SUP[c]['pooled']['paraphrase']['ci_item']['ci_lo']:+.4f},{G.SUP[c]['pooled']['paraphrase']['ci_item']['ci_hi']:+.4f}] "
                                                            f"[{G.SUP[c]['pooled']['paraphrase']['ci_persona']['ci_lo']:+.4f},{G.SUP[c]['pooled']['paraphrase']['ci_persona']['ci_hi']:+.4f}]{' *' if G.SUP[c]['pooled']['paraphrase']['both_exclude_zero'] else ''}" for c in G.SUP)
          + ". Branch B (at least one model with both intervals excluding zero above the lookup): GPT-5.6 Luna, the reader added after the registration; the author's ruling of 2026-09-21 keeps Branch B "
          "by the pre-stated rule and words it in both directions. Pooled against matched on reliability: " + "; ".join(f"{c} {'agree' if G.SUP[c]['pooled']['paraphrase']['both_exclude_zero'] == G.SUP[c]['matched']['paraphrase']['both_exclude_zero'] else 'DISAGREE'}" for c in G.SUP) + ".", ""]
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"-> {OUT} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
