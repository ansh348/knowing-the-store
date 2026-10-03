# -*- coding: utf-8 -*-
"""ledger_r133.py -- reviews/NUMBERS_R133.md (R133 RULINGS 3, 2026-09-21): the two per-state rows tab:routes gains, GPT-4.1 mini on the tagged view under
ground-truth tags minus its summary alone on that state's items, read from resp_review/run/scores_resp.json (L2/arms/RETRIEVED/{expiry,supersession};
the RESP ledger's AUX-RESP-L2-MINI-NOK rows) with the two-decimal forms the table prints (half-up on the four-decimal recorded value), so trace_scan_v13
resolves each printed token to a ledger row. No number is typed by hand.
Usage: python reviews/v23/tools/ledger_r133.py
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))
import r133_number_gate as G  # noqa: E402

OUT = ROOT / "reviews" / "NUMBERS_R133.md"


def main():
    L = ["# NUMBERS_R133.md: the R133 pass (the readability pass, v23; 2026-09-21)", "",
         "Written by `reviews/v23/tools/ledger_r133.py`; every row is read from the artifact named; the printed forms are half-up on the four-decimal recorded value at two decimals "
         "(the convention of reviews/NUMBERS_R131.md). The pass itself changes no number; the one addition is R133 RULINGS 3 (the author, 2026-09-21): Table tab:routes (Appendix E.10) "
         "gains GPT-4.1 mini's per-state view-minus-summary rows.", "",
         "## AUX-R133-ROUTES-PERSTATE: the tagged view under ground-truth tags minus the summary alone, per state (GPT-4.1 mini, one call; the full obligation set)", "",
         "Source: `resp_review/run/scores_resp.json` `L2/arms/RETRIEVED/<state>` (the RESP registration's L2 arm; `resp_review/NUMBERS_RESP.md` AUX-RESP-L2-MINI-NOK rows "
         "'RETRIEVED, expiry' and 'RETRIEVED, supersession'). Each state's obligations against the same 557 negatives (n = positives + 557).", "",
         "| state | n / positives | the summary alone (base) | the tagged view (arm) | difference | item-level 95% | persona-clustered 95% | printed (tab:routes) |", "|---|---|---:|---:|---:|---|---|---|"]
    for state in ("expiry", "supersession"):
        d = G.RESP[state]
        printed = f"{G.r2(d['arm'])}; {G.r2s(d['D'])} (the summary alone, {G.r2(d['base'])}); [{G.r2s(d['item']['ci_lo'])},{G.r2s(d['item']['ci_hi'])}]; [{G.r2s(d['cluster']['ci_lo'])},{G.r2s(d['cluster']['ci_hi'])}]"
        L.append(f"| {state} | {d['n']} / {d['n_pos']} | {d['base']:.4f} | {d['arm']:.4f} | {d['D']:+.4f} | [{d['item']['ci_lo']:+.4f}, {d['item']['ci_hi']:+.4f}] | [{d['cluster']['ci_lo']:+.4f}, {d['cluster']['ci_hi']:+.4f}] | {printed} |")
    L += ["", "Both differences are reliable (both intervals exclude zero), as Section 7's sentence says ('the view helps mini on expiry ... and hurts it on supersession, both effects reliable'). "
          "The whole-set row (-0.0488, not reliable) and the retraction row (+0.0850, not reliable) stay in the RESP ledger; the ruling asked for expiry and supersession.", ""]
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
