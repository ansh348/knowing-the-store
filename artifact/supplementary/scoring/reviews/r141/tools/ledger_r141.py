# -*- coding: utf-8 -*-
"""ledger_r141.py -- appends (idempotently: replaces its own section) the Phase 2 results to reviews/NUMBERS_R141.md from reviews/r141/results/scores_sb60.json
and writes reviews/r141/results/r141_printed.json (the two-decimal printed forms the landing uses). Usage: python reviews/r141/tools/ledger_r141.py
"""
import json
import re
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LED = ROOT / "reviews" / "NUMBERS_R141.md"
S = json.load(open(ROOT / "reviews" / "r141" / "results" / "scores_sb60.json", encoding="utf-8"))
HEAD = "## AUX-R141-RESULTS"


def r2(x):
    return str(Decimal(str(round(abs(x), 4))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def iv(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"


def main():
    R, ML, P = S["readers"], S["minus_lookup"], S["predictions"]
    o = [HEAD + ": SB-60 scored (reviews/r141/tools/score_sb60.py → reviews/r141/results/scores_sb60.json; run 2588717 under f224177)\n"]
    o.append("Census (the rows): " + "; ".join(f"{n} {c['ok']}/{c['rows']} OK, served {list(c['served'])}, ${c['usd']:.4f}" for n, c in S["meta"]["census"].items())
             + ". The leak screen 0 of 30 correct (PASS, $0.0179); probes and leak included, OpenAI $2.9372 of the $12 cap (token-metered from the rows, not an invoice).\n")
    o.append("| reader | PN-60 vs SB-60 W/T/L | matched | triple interval | persona interval | pooled AUROC | SB-60 vs padded PRESENT (matched) |")
    o.append("|---|---|---:|---|---|---:|---:|")
    for n, r in R.items():
        m = r["pn60_vs_sb60"]
        o.append(f"| {n} | {m['W']}/{m['T']}/{m['L']} | {m['matched']:.4f} | [{m['ci_triple']['ci_lo']:.4f}, {m['ci_triple']['ci_hi']:.4f}] | [{m['ci_persona']['ci_lo']:.4f}, {m['ci_persona']['ci_hi']:.4f}] | "
                 f"{r['pooled_pn60_vs_sb60']['auroc']:.4f} | {r['sb60_vs_present']['matched']:.4f} |")
    NM = json.load(open(ROOT / "reviews" / "r141" / "results" / "nomodel_sb60.json", encoding="utf-8"))["readers"]
    o.append("\nThe no-model readers as tab:sb60 prints them (reviews/r141/results/nomodel_sb60.json, recorded before the freeze):\n")
    o.append("| reader | PN-60 vs SB-60 W/T/L | matched | triple interval | persona interval | pooled AUROC | SB-60 vs padded PRESENT (matched) |")
    o.append("|---|---|---:|---|---|---:|---:|")
    for n, r in NM.items():
        m = r["pn60_vs_sb60"]
        o.append(f"| {n} | {m['W']}/{m['T']}/{m['L']} | {m['matched']:.4f} | [{m['ci_triple']['ci_lo']:.4f}, {m['ci_triple']['ci_hi']:.4f}] | [{m['ci_persona']['ci_lo']:.4f}, {m['ci_persona']['ci_hi']:.4f}] | "
                 f"{r['pooled_pn60_vs_sb60']:.4f} | {r['sb60_vs_present']['matched']:.4f} |")
    o.append("\nEach model minus the name lookup (paired on the same pairs; reliable: both 95% intervals exclude zero; equivalent: both 90% intervals inside [-0.05, +0.05]):\n")
    o.append("| model | metric | difference | 95% triple/item | 95% persona | 90% triple/item | 90% persona | reliable | equivalent |")
    o.append("|---|---|---:|---|---|---|---|---|---|")
    for n, d in ML.items():
        for met in ("matched", "pooled"):
            x = d[met]; a = x["ci_triple"] if met == "matched" else x["ci_item"]; b = x["ci_persona"]
            o.append(f"| {n} | {met} | {x['delta']:+.4f} | {iv(a)} | {iv(b)} | [{a['ci90_lo']:+.4f}, {a['ci90_hi']:+.4f}] | [{b['ci90_lo']:+.4f}, {b['ci90_hi']:+.4f}] | "
                     f"{'yes' if x['reliable'] else 'no'} | {'yes' if x['equivalent'] else 'no'} |")
    o.append("\nThe predictions (matched endpoint; the pooled reading beside it):\n")
    for k, v in P.items():
        o.append(f"- {k} ({v['text']}): **{'HOLDS' if v['holds'] else 'FAILS'}**" + (f"; pooled reading {'holds' if v['pooled_reading'] else 'does not'}" if "pooled_reading" in v else "")
                 + (f"; {json.dumps(v['per_model'])}" if "per_model" in v else ""))
    o.append(f"\n**Branch fired: {S['branch']}** (P-S1 {'holds' if P['P-S1']['holds'] else 'fails'}, P-S2 {'holds' if P['P-S2']['holds'] else 'fails'}); the named reader Sol.")
    o.append(f"Seeds 43 to 46 on every registered difference (both metrics, the reliable and equivalent flags): reading changes {S['seed_reading_changes'] or 'none'}.\n")
    o.append("Scoring note: the name lookup is computed for all three versions in one process (emb_cached), as the recorded values of the registration's §6 were; mixing the stored R136 floats with fresh ones breaks exact ties at the last digit (62/21/5 against the recorded 57/31/0). The stored vectors are asserted equal at 1e-6 and the recorded W/T/L is asserted reproduced. Departure recorded: the lanes called R125's Chat Completions call shape (r125_run.call_openai) with R136's settings, not cf2_openai.call_once.\n")
    printed = {"lookup_sb60_matched": r2(R["Name lookup"]["pn60_vs_sb60"]["matched"]), "sol_lead_matched": r2(ML["GPT-5.6 Sol"]["matched"]["delta"]),
               "luna_lead_matched": r2(ML["GPT-5.6 Luna"]["matched"]["delta"]), "sol_lead_pooled": r2(ML["GPT-5.6 Sol"]["pooled"]["delta"]),
               "luna_lead_pooled": r2(ML["GPT-5.6 Luna"]["pooled"]["delta"]),
               "branch": S["branch"], "predictions": {k: v["holds"] for k, v in P.items()}}
    o.append("Printed forms (two decimals, half-up): the lookup's matched score on PN-60 vs SB-60 " + printed["lookup_sb60_matched"] + "; Sol's matched lead " + printed["sol_lead_matched"]
             + " (reliable); Luna's matched lead " + printed["luna_lead_matched"] + " (not reliable).\n")
    json.dump(printed, open(ROOT / "reviews" / "r141" / "results" / "r141_printed.json", "w", encoding="utf-8"), indent=1)
    t = LED.read_text(encoding="utf-8")
    m = re.search(r"\n" + re.escape(HEAD) + r".*?(?=\n## |\Z)", t, flags=re.S)
    t = (t[:m.start()] + t[m.end():]) if m else t
    LED.write_text(t.rstrip("\n") + "\n\n" + "\n".join(o) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(printed))


if __name__ == "__main__":
    main()
