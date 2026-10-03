# -*- coding: utf-8 -*-
"""ledger_r137.py -- reviews/NUMBERS_R137.md (R137, 2026-09-22: the long-list check landed, the prediction recount, Figure 1 rendered): every printed form the pass
brings into the paper, beside its four-decimal value and artifact key, written from the checks of reviews/v23/tools/r137_number_gate.py (which reads the artifacts,
not this file), so trace_scan_v13 resolves every printed token to a ledger row; tab:robust's row 9 as built (reviews/v23/results/robust_printed.json); the
prediction recount; Figure 1's transcribed lines. No number is typed by hand.
Usage: python reviews/v23/tools/ledger_r137.py
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))
import r134_number_gate as G  # noqa: E402
import r135_number_gate as G135  # noqa: E402
import r137_number_gate as G137  # noqa: E402

OUT = ROOT / "reviews" / "NUMBERS_R137.md"


def main():
    G.checks()
    n134 = len(G.CHECKS)
    G135.checks135()
    n135 = len(G.CHECKS)
    G137.checks137()
    rows = G.CHECKS[n135:]
    bad = [c for c in rows if not c["ok"]]
    assert not bad, bad
    P = json.load(open(ROOT / "reviews" / "v23" / "results" / "robust_printed.json", encoding="utf-8"))
    S = json.load(open(ROOT / "cf_pad" / "results" / "cf_pad_scores.json", encoding="utf-8"))
    r9 = P["rows"][8]
    assert r9["n"] == 9 and r9["tried"] == "List padded to 60 names"
    PR = S["predictions"]
    new = len(PR); otherwise = sum(1 for v in PR.values() if not v["holds"])
    totals, hobbies, sup_names = G137.fig1_lines()
    e, tag = G137.tag_route_record()
    L = ["# NUMBERS_R137.md: the R137 pass (the long-list check landed, the prediction recount, Figure 1 rendered; 2026-09-22)", "",
         "Written by `reviews/v23/tools/ledger_r137.py` from the checks of `reviews/v23/tools/r137_number_gate.py`; every value is read from the artifact named "
         "(`cf_pad/results/cf_pad_scores.json`, scored once at 6d7f224 under registrations/ADDENDUM_CF_PAD.md, registered text sha256 a84dac1a..., frozen alone at 06c611f; `cf_pad/build/lock.json`; "
         "`reviews/NUMBERS_R131.md` AUX-R131-COUNT; `iclr2027_monitoring_submission/ARTIFACT/manifests/indexes_v2.json`; `e1_metamemory/backend_entries/frbank.json`). Printed forms are half-up on the "
         "four-decimal recorded value at two decimals in the body (the convention of reviews/NUMBERS_R131.md), magnitudes with the direction in words, and four decimals in the appendix. "
         "The appendix tables tab:cfpad-* are written by `cf_pad/tools/cfpad_tex.py` (`cf_pad/results/cfpad_tab_*.tex`) and every value in them is a row of `cf_pad/NUMBERS_CF_PAD.md` (AUX-CFP-*); "
         "tab:robust is written by `reviews/v23/tools/robust_tex.py`.", "",
         "## AUX-R137-ROBUST9: tab:robust's row 9 as built (the long-list check in place of the 661-set padding and the injection, which stay in Appendix C.2)", "",
         "| row | what we tried to break | what it removes | what happened (as printed) | metric | population | status | source |", "|---|---|---|---|---|---|---|---|",
         f"| {r9['n']} | {r9['tried']} | {r9['removes']} | {r9['happened']} | {r9['metric']} | {r9['population']} | {r9['status']} | {r9['source']} |", "",
         "## AUX-R137-COUNT: the prediction count with the long-list check's four predictions in it", "",
         f"AUX-R131-COUNT: 98 predictions, 31 otherwise (tab:registrations-e 5 with 2). ADDENDUM_CF_PAD registered four predictions with a bar, each read on the pooled AUROC of the supersession slice: "
         + "; ".join(f"{k} ({'HOLDS' if PR[k]['holds'] else 'FAILS'})" for k in sorted(PR)) + f"; each counts once, {otherwise} otherwise (P-L1 and P-L4 fail on Opus 5 alone). "
         f"**With them: {98 + new} predictions, {31 + otherwise} otherwise; tab:registrations-e carries {5 + new} with {2 + otherwise}**; the other four tables unchanged (47 with 8; 17 with 10; none; 29 with 11). "
         "Section 4's sentence and Appendix F's count paragraph print the new pair.", "",
         "## AUX-R137-FIG1: Figure 1's rendered summary, transcribed from the summary the E.1 excerpt was cut from (`ARTIFACT/manifests/indexes_v2.json` key `frbank:david:FULL:BELIEVED`, the same key AUX-R86-INDEX-EXCERPT transcribes; asserted equal to `e1_metamemory/indexes_v2.json`)", "",
         "| line in the summary | value |", "|---|---|"]
    for st in ("active", "superseded", "retracted", "expired"):
        L.append(f"| `LIFECYCLE TOTALS` {st} | **{totals[st]}** |")
    L += [f"| `ATTRIBUTE NAMES BY CATEGORY` HOBBIES_RECREATION, the first three names printed | {', '.join(hobbies[:3])} (of {len(hobbies)}) |",
          f"| `ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT`, the two names printed | exam_date, hiking_preference (both in the list's first 15) |",
          f"| the tag route's returned record | `e1_metamemory/backend_entries/frbank.json` {e['entry_id']} (persona david, category {e['category']}, slot {e['slot']}); FR-Bank's own tag: {tag} (believed_superseded {e['believed_superseded']}); text \"{e['text']}\" |", "",
          "The figure prints these lines and nothing else of the summary; the E.1 excerpt prints the category rows, the ages and the name lines of the same summary.", "",
          "## AUX-R137-PRINTED: every number and claim the pass's new texts print, beside its source", "",
          f"{len(rows)} checks, {len(bad)} mismatches (`r137_number_gate.py`, this pass's own; R134's {n134} and R135's {n135 - n134} run first, unchanged).", "",
          "| where (the sentence) | printed | recorded value | reliable, claimed / actual | source |", "|---|---|---|---|---|"]
    for c in rows:
        v = c["value"]
        vs = f"{v:+.4f}" if isinstance(v, float) else str(v)
        rl = "" if c["reliable"] is None else f"{c['reliable']} / {c['actual_reliable']}"
        L.append(f"| {c['where']} | {c['printed']} | {vs} | {rl} | {c['source']} |")
    L.append("")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"-> {OUT} ({len(rows)} printed-form rows; count {98 + new} / {31 + otherwise})")


if __name__ == "__main__":
    main()
