# -*- coding: utf-8 -*-
"""ledger_r135.py -- reviews/NUMBERS_R135.md (R135, 2026-09-21: the robustness table, the abstract, the 5.1 trims, the small fixes, ADDENDUM 2): every
printed form the pass brings into the main text, beside its four-decimal value and artifact key, written from the checks of reviews/v23/tools/r135_number_gate.py
(which reads the artifacts, not this file), so trace_scan_v13 resolves every printed token to a ledger row; and the rows of tab:robust as built, each with its
metric, population and status (reviews/v23/results/robust_printed.json). No number is typed by hand.
Usage: python reviews/v23/tools/ledger_r135.py
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))
import r134_number_gate as G  # noqa: E402
import r135_number_gate as G135  # noqa: E402

OUT = ROOT / "reviews" / "NUMBERS_R135.md"


def main():
    G.checks()
    n134 = len(G.CHECKS)
    G135.checks135()
    rows = G.CHECKS[n134:]
    bad = [c for c in rows if not c["ok"]]
    assert not bad, bad
    P = json.load(open(ROOT / "reviews" / "v23" / "results" / "robust_printed.json", encoding="utf-8"))
    L = ["# NUMBERS_R135.md: the R135 pass (the last content pass on v23; 2026-09-21)", "",
         "Written by `reviews/v23/tools/ledger_r135.py` from the checks of `reviews/v23/tools/r135_number_gate.py`; every value is read from the artifact named "
         "(`reviews/r125/results/r125_matched.json`, `r125_t4_sibling.json`, `r125_t5_nc.json`; `r82_counterfactual/cf2/results/cf_scores_cf2.json`, `cf_scores_nc.json`; "
         "`cf2_paraphrase/results/para_scores.json`, `para_minus_lookup_posthoc.json`; `reviews/r122/results/enc_lookup.json`; `pad_probe/results/pad_scores.json`, `contam_scores.json`; "
         "`ds_downstream/run/lock_amend8.json`; the E1R, R74 and BELIEVED_H ledgers). Printed forms are half-up on the four-decimal recorded value at two decimals "
         "(the convention of reviews/NUMBERS_R131.md), magnitudes with the direction in words. The table tab:robust is written by `reviews/v23/tools/robust_tex.py` "
         "(`reviews/v23/src/robust_table.tex`; `reviews/v23/results/robust_printed.json`).", "",
         "## AUX-R135-ROBUST: the rows of tab:robust as built, each with its metric, population, status and source", "",
         "| row | what we tried to break | what it removes | what happened (as printed) | metric | population | status | source |", "|---|---|---|---|---|---|---|---|"]
    for r in P["rows"]:
        L.append(f"| {r['n']} | {r['tried']} | {r['removes']} | {r['happened']} | {r['metric']} | {r['population']} | {r['status']} | {r['source']} |")
    L += ["", "## AUX-R135-PRINTED: every number and claim the pass's new texts print, beside its source", "",
          f"{len(rows)} checks, {len(bad)} mismatches (`r135_number_gate.py`, this pass's own; R134's {n134} run first, unchanged).", "",
          "| where (the sentence) | printed | recorded value | reliable, claimed / actual | source |", "|---|---|---|---|---|"]
    for c in rows:
        v = c["value"]
        vs = f"{v:+.4f}" if isinstance(v, float) else str(v)
        rl = "" if c["reliable"] is None else f"{c['reliable']} / {c['actual_reliable']}"
        L.append(f"| {c['where']} | {c['printed']} | {vs} | {rl} | {c['source']} |")
    L.append("")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"-> {OUT} ({len(P['rows'])} table rows, {len(rows)} printed-form rows)")


if __name__ == "__main__":
    main()
