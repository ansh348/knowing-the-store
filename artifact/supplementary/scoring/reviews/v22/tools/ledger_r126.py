# -*- coding: utf-8 -*-
"""ledger_r126.py -- reviews/NUMBERS_R126.md, the pass ledger of program R126 (2026-09-20): every number the pass prints that no earlier ledger
carries in its printed form, each read from its artifact by this script (no number typed by hand):
  AUX-R126-E3-INTENT   the cells of tab:e3-intent (reviews/v22/results/e3_intent_table.json; reviews/v22/tools/e3_intent_table.py)
  AUX-R126-GATEREACH   the three recorded rows added to tab:gatereach's licensed panel (reviews/v21/results/reach_rows_r123.json, AUX-R123-REACH-ROWS)
  AUX-R126-DAYS        the day index of the registration order that replaces each calendar date in the PDF (Phase 4.4; the map, not a measurement)
  AUX-R126-FIG3        Figure 3's plotted values (reviews/v22/src/fig3_data.tex, written by fig3_data.py from the artifacts named there)
Usage: python reviews/v22/tools/ledger_r126.py
"""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews" / "NUMBERS_R126.md"
DAYS = {"2026-08-10": 0, "2026-08-11": 1, "2026-08-14": 4, "2026-08-24": 14, "2026-08-29": 19, "2026-08-30": 20, "2026-09-12": 33, "2026-09-13": 34,
        "2026-09-14": 35, "2026-09-15": 36, "2026-09-17": 38, "2026-09-18": 39, "2026-09-19": 40}


def main():
    e3 = json.loads((ROOT / "reviews/v22/results/e3_intent_table.json").read_text(encoding="utf-8"))
    reach = json.loads((ROOT / "reviews/v21/results/reach_rows_r123.json").read_text(encoding="utf-8"))["policies"]
    fig3 = (ROOT / "reviews/v22/src/fig3_data.tex").read_text(encoding="utf-8")
    L = ["# NUMBERS_R126.md: the pass ledger of program R126 (the readable body, v22; 2026-09-20)\n\n",
         "Written by `reviews/v22/tools/ledger_r126.py` from the artifacts named in each section; no number is typed by hand. The readable body's own numbers are the v21 body's "
         "(every printed form resolves to an earlier ledger; `reviews/v22/INBOX_NUMBERS_R126.md` lists the 130 values with the inbox's provenance tags); this file carries what the pass adds.\n\n",
         "## AUX-R126-E3-INTENT — the 661 by intent, label and the state of the question's own attribute (tab:e3-intent; `reviews/v22/results/e3_intent_table.json`, `reviews/v22/tools/e3_intent_table.py`)\n\n",
         f"Method: {e3['method']}\n\n| intent | label | " + " | ".join(e3["states"]) + " | total |\n|---|---|" + "---:|" * (len(e3["states"]) + 1) + "\n"]
    for i in e3["intents"]:
        for l in e3["labels"]:
            vals = [e3["counts"].get(f"{i}|{l}|{s}", 0) for s in e3["states"]]
            if sum(vals):
                L.append(f"| {i} | {l} | " + " | ".join(str(v) for v in vals) + f" | {sum(vals)} |\n")
    pn = e3["pn_by_intent"]; pres = e3["present_with_a_non_active_own_slot_by_intent"]
    L.append(f"\nPN by intent: {pn} (every PN question has current or upcoming intent). PRESENT questions whose own attribute also holds a non-active record, by intent: {pres}; "
             f"total {sum(pres.values())} of {sum(v for k, v in e3['counts'].items() if '|PRESENT|' in k)} PRESENT questions ({pres['CURRENT-STATE'] + pres['UPCOMING']} under current or upcoming intent, "
             f"{pres['CHANGE-AWARE']} under change intent). Non-exclusive marks on PRESENT questions: {e3['present_own_slot_marks_non_exclusive']} "
             f"(CHANGE-AWARE|superseded = {e3['present_own_slot_marks_non_exclusive'].get('CHANGE-AWARE|superseded')}, the 4 of the 45 that reviews/NUMBERS_WP.md section 9 B4b counts).\n\n")
    L.append("## AUX-R126-GATEREACH — the recorded policies' rows added to tab:gatereach's licensed panel (`reviews/v21/results/reach_rows_r123.json`, AUX-R123-REACH-ROWS; printed at two decimals)\n\n"
             "| policy | licensed in view (of 174) | rate | mean lines, 661 (printed) | mean lines, 104 (printed) |\n|---|---:|---:|---:|---:|\n")
    for name, k in (("top-five retrieval", "ALWAYS"), ("lookup rule", "LOOKUP"), ("oracle", "ORACLE")):
        r = reach[k]
        L.append(f"| {name} ({k}) | {r['licensed_in_view']} | {r['licensed_rate']:.4f} | {r['mean_lines_661']:.4f} -> {r['mean_lines_661']:.2f} | {r['mean_lines_104']:.4f} -> {r['mean_lines_104']:.2f} |\n")
    L.append("\n## AUX-R126-DAYS — the day index of the registration order (Phase 4.4, anonymity): the calendar date each index replaces in the PDF; day 0 is the first freeze (the E0 preregistration)\n\n"
             "| date | day |\n|---|---:|\n" + "".join(f"| {d} | {n} |\n" for d, n in DAYS.items()))
    L.append("\nThe artifact files that still carry these dates (for the 24 September sweep) are listed in `reviews/v22/REPORT_R126.md`, Phase 4.4; git history is not rewritten.\n\n")
    L.append("## AUX-R126-FIG3 — Figure 3's plotted values (`reviews/v22/src/fig3_data.tex`; the sources per reader in the file's header)\n\n```\n" + "\n".join(l for l in fig3.split("\n") if not l.startswith("%%")) + "\n```\n")
    OUT.write_text("".join(L), encoding="utf-8", newline="\n")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
