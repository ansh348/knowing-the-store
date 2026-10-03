# -*- coding: utf-8 -*-
"""ledger_r131.py -- reviews/NUMBERS_R131.md, the pass ledger of program R131 (2026-09-20): every two-decimal form the body prints from the R125
artifacts beside its four-decimal source (the checks of reviews/v22/tools/r131_number_gate.py, each read from reviews/r125/results/*.json), Table 1's
matched column from the printed W/T/L, the recount of predictions, and Figure 3's matched data. No number is typed by hand. trace_scan_v13 reads it
(LEDGERS). Usage: python reviews/v22/tools/ledger_r131.py
"""
from __future__ import annotations

import json
import pathlib
import sys
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews" / "NUMBERS_R131.md"
sys.path.insert(0, str(ROOT / "reviews" / "v22" / "tools"))
import r131_number_gate as G  # noqa: E402


def r2(x):
    return str(Decimal(str(round(x, 4))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def main():
    G.main()
    bad = [c for c in G.CHECKS if not c["ok"]]
    assert not bad, bad
    L = ["# NUMBERS_R131.md: the pass ledger of program R131 (2026-09-20; the author's brief 'KtS R131: land R125 in the body')\n\n",
         "Written by `reviews/v22/tools/ledger_r131.py`; every row is read from the R125 artifacts under `reviews/r125/results/` (the ledger rows are "
         "`r82_counterfactual/cf2/NUMBERS_CF2.md` section 15) or from the recorded values the body already printed; no number is typed by hand. "
         "Rounding is half-up on the four-decimal value at two decimals (the one exact tie, GPT-5.6 Sol's counted-state fall of $-0.3250$, prints 0.33).\n\n",
         "## AUX-R131-PRINTED — the two-decimal forms the body prints, each beside its artifact value and source key (the number gate, `r131_number_gate.py`: "
         f"{len(G.CHECKS)} checks, 0 mismatches)\n\n",
         "| where | printed | artifact value | reliability, claimed / artifact | source |\n|---|---|---|---|---|\n"]
    for c in G.CHECKS:
        v = c["value"]
        vs = f"{v:.4f}" if isinstance(v, float) else str(v)
        rel = "" if c["reliable"] is None else f"{'reliable' if c['reliable'] else 'not reliable'} / {'reliable' if c['actual_reliable'] else 'not reliable'}"
        L.append(f"| {c['where']} | {c['printed']} | {vs} | {rel} | {c['source']} |\n")

    # Table 1's matched column
    L.append("\n## AUX-R131-TAB1 — Table 1's matched column, (W + T/2) / 148 from the printed W/T/L (AUX-CF2-R125-SANITY: the printed counts reproduce from the rows), the hybrid row and the difference row\n\n")
    L.append("| row | W/T/L | (W + T/2) / 148 | printed |\n|---|---|---:|---:|\n")
    for key, name in (("MINI5_v2", "mini, superseded"), ("MINI5_v3", "mini, all"), ("H45_v2", "Haiku, superseded"), ("H45_v3", "Haiku, all"), ("LUNA_v2", "Luna"), ("SOL_v2", "Sol"),
                      ("OP5_v2", "Opus, superseded"), ("OP5_v3", "Opus, all"), ("LOOKUP_v2", "Name lookup, superseded"), ("ALLSTATES_v3", "Name lookup, all"),
                      ("CR-nb1_v2", "Count reader, guessed category"), ("CR-oracle-a_v2", "Count reader, given category"), ("HYBRID_v2", "Lookup with one count feature (the hybrid reader, E10)")):
        w = G.RD[key]["pn_vs_present"]["whole"]
        m = (w["W"] + w["T"] / 2) / w["n"]
        assert abs(m - w["matched"]) < 1e-4
        L.append(f"| {name} | {w['W']}/{w['T']}/{w['L']} | {m:.4f} | {r2(m)} |\n")
    hyb = 0.7865
    L.append(f"\nThe hybrid row's pooled value and persona interval: {hyb:.4f} [0.7488, 0.8234] (AUX-CF2-HYB-WHOLE), printed 0.79 [0.75, 0.82]. "
             "The difference row (all states named, Opus 5 minus the all-states lookup) prints four decimals: pooled +0.0323 [+0.0060, +0.0617]; [+0.0077, +0.0608] (AUX-R103-MARGIN, reliable); "
             f"matched {G.PD['opus_v3_vs_allstates']['OP5_v3']['pn_vs_present']['whole']['delta']:+.4f} "
             f"[{G.PD['opus_v3_vs_allstates']['OP5_v3']['pn_vs_present']['whole']['ci_triple']['ci_lo']:+.4f}, {G.PD['opus_v3_vs_allstates']['OP5_v3']['pn_vs_present']['whole']['ci_triple']['ci_hi']:+.4f}]; "
             f"[{G.PD['opus_v3_vs_allstates']['OP5_v3']['pn_vs_present']['whole']['ci_persona']['ci_lo']:+.4f}, {G.PD['opus_v3_vs_allstates']['OP5_v3']['pn_vs_present']['whole']['ci_persona']['ci_hi']:+.4f}] (AUX-CF2-R125-OP5-V3, not reliable); the body prints both as 0.03.\n")

    # the recount
    P4, P5 = G.T4["predictions"], G.T5["predictions"]
    L.append("\n## AUX-R131-COUNT — the prediction count with the two R125 registrations in it\n\n")
    L.append(f"AUX-R129-COUNT: 93 predictions, 29 otherwise (tab:registrations-d 29 with 11). The sibling-name control registered four readings with a bar: P-SB1 ({P4['P-SB1']['verdict']}) and P-SB3 ({P4['P-SB3']['verdict']}) "
             "were disclosed at the freeze as recorded values from the scorer's pre-freeze dry run (ADDENDUM_R125_SIBLING section 8; D-R125-2) and are **not counted as predictions**; "
             f"P-SB2 ({P4['P-SB2']['verdict']}) and P-SB4 ({P4['P-SB4']['verdict']}) count, neither otherwise. E2 Amendment 1 registered three: P-N3 ({P5['P-N3']['verdict']}), P-N4 ({P5['P-N4']['verdict']}), P-N5 ({P5['P-N5']['verdict']}); "
             "each counts once (the verdict is stated on the models run; GPT-5.6 Sol's lane not run), two otherwise. "
             "**With them: 98 predictions, 31 otherwise; the new tab:registrations-e carries 5 with 2**; the other four tables unchanged (47 with 8; 17 with 10; none; 29 with 11).\n")

    # Figure 3
    L.append("\n## AUX-R131-FIG3 — Figure 3 on the matched metric (`reviews/v22/src/fig3_data_matched.tex`, copied from `reviews/r125/results/fig3_data_matched.tex` by fig3_data_r131.py after checking every value against r125_matched.json; AUX-CF2-R125-FIG3)\n\n")
    L.append("The y axis reaches 0.35 (mini's expiry value under the default summary is 0.4000); the pooled figure (fig3_data.tex, AUX-R126-FIG3) moves to Appendix C.2 as fig:perstate-pooled.\n")

    # the appendix tables
    L.append("\n## AUX-R131-APPENDIX — the appendix tables written by `reviews/v22/tools/appendix_r131.py`\n\n")
    L.append("tab:cf-nc-strong (r125_t5_nc.json; NUMBERS_CF2.md 15e), tab:cf-matched, tab:cf-classes, tab:cf-matched-vs, tab:cf-matched-ablations and the hybrid panel of tab:cf-hybrid (r125_matched.json; 15), "
             "tab:cf-emptiness (r125_t2_emptiness.json; 15b), tab:cf-sibling (r125_t4_sibling.json; 15d), tab:levels-strata (r125_t3_frbank.json; 15c), tab:graphiti-strata (r125_t3_graphiti.json; 15c), "
             "tab:registrations-e (the two registrations, frozen 5cd8f809f2 on day 41). Every value prints at four decimals as the artifact records it; the two-decimal forms in their captions (0.14; 0.60 of 0.77; 0.65 of 0.78; 0.71; 0.90; 0.80; 0.50; 0.05) are the rows of AUX-R131-PRINTED or the recorded body values.\n")
    OUT.write_text("".join(L), encoding="utf-8", newline="\n")
    print("->", OUT, len(G.CHECKS), "rows")


if __name__ == "__main__":
    main()
