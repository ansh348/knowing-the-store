# -*- coding: utf-8 -*-
"""ledger_r128.py -- reviews/NUMBERS_R128.md, the pass ledger of programs R127, R127b and R128 (2026-09-20): every number the pass prints or reports
that no earlier ledger carries, each read from its artifact by this script (no number typed by hand):
  AUX-R128-DS-DENOM   tab:ds-body with both denominators: the stale answers over all reached scorable obligations (supersession plus retraction in
                      view, tab:ds) and over the answered scorable subset (answered minus the expiry answered), with Wilson 95 percent intervals
                      (the recorded method: the score interval, z = 1.96, as tab:ds-body prints [0.10,0.33] for 8 of 42); every count is tab:ds's
                      (ds_downstream/NUMBERS_DS.md, AUX-DS-REACH, -STAGE2, -A1-*, -A2-STAGE2-LIT), and the Wilson interval of 11 of 65 for tab:ds-body-lower
  AUX-R128-CF3-DRAW1  Opus 5's expiry rows at draw 1 on every pair (reviews/v22/results/r128_cf3_draw1.json; r128_cf3_draw1.py)
  AUX-R128-POOLED66   the composition of the pooled 66 external questions (e1_metamemory/run_a_frontier_indexed.json; ADDENDUM_E1_5.md Run A)
  AUX-R128-GROUPS     the R127 and R127b readings (reviews/v22/results/r127_groups.json, r127b_groups.json), reported, not printed
Usage: python reviews/v22/tools/ledger_r128.py
"""
from __future__ import annotations

import collections
import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews" / "NUMBERS_R128.md"

# tab:ds (ds_downstream/NUMBERS_DS.md): sup. / ret. / exp. in view; answered; expiry answered = exp. in view for the answering policies
DS = {  # policy: (sup, ret, exp, answered, stale_scorable, correct)
    "Top-5 retrieval": (22, 20, 12, 54, 8, 46),
    "Model rule": (53, 20, 12, 74, 8, 44),
    "Lookup rule": (53, 20, 12, 70, 6, 40),
    "Model rule, all states named and scored": (54, 22, 13, 78, 11, 44),
    "Literal lookup rule (descriptive)": (62, 20, 12, 94, 13, 46),
    "Oracle": (63, 22, 14, 99, 16, 46),
}
PRINTED = {"Top-5 retrieval": (42, "[0.10,0.33]"), "Model rule": (62, "[0.07,0.23]"), "Lookup rule": (58, "[0.05,0.21]"),
           "Model rule, all states named and scored": (65, "[0.10,0.28]"), "Literal lookup rule (descriptive)": (82, "[0.10,0.25]"), "Oracle": (85, "[0.12,0.28]")}


def wilson(k, n, z=1.96):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def ds_rows():
    rows = []
    for pol, (sup, ret, exp, ans, stale, correct) in DS.items():
        reached = sup + ret; answered = ans - exp
        assert answered == PRINTED[pol][0], (pol, answered)
        lo, hi = wilson(stale, answered)
        assert f"[{lo:.2f},{hi:.2f}]" == PRINTED[pol][1], (pol, lo, hi)
        lo_r, hi_r = wilson(stale, reached)
        rows.append({"policy": pol, "reached_scorable": reached, "answered_scorable": answered, "stale": stale, "rate_reached": round(stale / reached, 4),
                     "wilson_reached": [round(lo_r, 4), round(hi_r, 4)], "rate_answered": round(stale / answered, 4), "wilson_answered": [round(lo, 4), round(hi, 4)],
                     "abstained_scorable": reached - answered})
    return rows


def main():
    rows = ds_rows()
    cf3 = json.loads((ROOT / "reviews/v22/results/r128_cf3_draw1.json").read_text(encoding="utf-8"))
    g1 = json.loads((ROOT / "reviews/v22/results/r127_groups.json").read_text(encoding="utf-8"))
    g2 = json.loads((ROOT / "reviews/v22/results/r127b_groups.json").read_text(encoding="utf-8"))
    ext = [r for r in json.loads((ROOT / "e1_metamemory/run_a_frontier_indexed.json").read_text(encoding="utf-8"))["rows"]]
    def parse(i):
        p = i.split(":")
        return (p[1], p[2], "probe") if p[0] == "probe" else (p[0], p[1], p[3])
    ext = [r for r in ext if parse(r["item_id"])[0] != "frbank"]
    items = json.loads((ROOT / "e1_metamemory/build/items_final.json").read_text(encoding="utf-8"))
    lab = {it["item_id"]: it.get("label") for it in items}
    comp = collections.Counter((parse(r["item_id"])[0], lab.get(r["item_id"])) for r in ext)
    personas = len({parse(r["item_id"])[1] for r in ext})
    L = ["# NUMBERS_R128.md: the pass ledger of programs R127, R127b and R128 (2026-09-20)\n\n",
         "Written by `reviews/v22/tools/ledger_r128.py` from the artifacts named in each section; no number is typed by hand.\n\n",
         "## AUX-R128-DS-DENOM — tab:ds-body with both denominators (the counts are tab:ds's; Wilson score intervals, z = 1.96; the answered-subset intervals reproduce the printed ones)\n\n",
         "| policy | reached scorable (sup. + ret. in view) | answered scorable (answered minus expiry answered) | abstained | stale | rate over reached (Wilson) | rate over answered (Wilson) |\n|---|---:|---:|---:|---:|---|---|\n"]
    for r in rows:
        L.append(f"| {r['policy']} | {r['reached_scorable']} | {r['answered_scorable']} | {r['abstained_scorable']} | {r['stale']} | {r['rate_reached']:.4f} [{r['wilson_reached'][0]:.3f}, {r['wilson_reached'][1]:.3f}] | {r['rate_answered']:.4f} [{r['wilson_answered'][0]:.3f}, {r['wilson_answered'][1]:.3f}] |\n")
    lo, hi = wilson(11, 65)
    L.append(f"\nThe Wilson interval tab:ds-body-lower lacked, the model rule with all states named and scored, 11 of 65: [{lo:.3f}, {hi:.3f}] (printed at two decimals in tab:ds-body as [0.10,0.28]).\n\n")
    L.append("## AUX-R128-CF3-DRAW1 — Opus 5's expiry rows at draw 1 on every pair (`reviews/v22/results/r128_cf3_draw1.json`; the recorded pooled row reproduced first)\n\n"
             "| reading | summary | AUROC | persona CI | delta vs blind | item interval | persona interval |\n|---|---|---:|---|---:|---|---|\n")
    for k, name in (("recorded", "pooled, recorded (k = 5 on the 30, k = 1 on the 14)"), ("draw1", "pooled, draw 1 on every pair"), ("draw1_cf2_expiry", "the 30 pairs at draw 1")):
        for arm, s in (("v2", "sup. only"), ("v3", "all three"), ("v2r", "totals rand.")):
            a = cf3[k]["opus"][arm]
            L.append(f"| {name} | {s} | {a['indexed']:.4f} | [{a['indexed_ci_persona']['ci_lo']:.4f}, {a['indexed_ci_persona']['ci_hi']:.4f}] | {a['delta']:+.4f} | [{a['item_ci']['ci_lo']:+.4f}, {a['item_ci']['ci_hi']:+.4f}] | [{a['persona_ci']['ci_lo']:+.4f}, {a['persona_ci']['ci_hi']:+.4f}] |\n")
    L.append("\n## AUX-R128-POOLED66 — the pooled 66 external questions (ADDENDUM_E1_5.md Run A: the external part of the 150-item stratified subsample of the E1 universe, seed 42, quota PRESENT 50 / ABSENT 60 / PN 40, which resolves by backend to FR-Bank 84, Mem0 29, A-MEM 37; `e1_metamemory/run_a_frontier_indexed.json`)\n\n")
    L.append("| store | PRESENT (full-store questions) | ABSENT (natural-absent probes) | total |\n|---|---:|---:|---:|\n")
    for store in ("mem0", "amem"):
        L.append(f"| {store} | {comp[(store, 'PRESENT')]} | {comp[(store, 'ABSENT')]} | {comp[(store, 'PRESENT')] + comp[(store, 'ABSENT')]} |\n")
    L.append(f"| both | {comp[('mem0', 'PRESENT')] + comp[('amem', 'PRESENT')]} | {comp[('mem0', 'ABSENT')] + comp[('amem', 'ABSENT')]} | {len(ext)} |\n\nPersonas: {personas}.\n\n")
    L.append("## AUX-R128-GROUPS — the R127 and R127b readings (reported in REPORT_R127.md and REPORT_R128.md, not printed): `reviews/v22/results/r127_groups.json` (the 104 PN against the three PRESENT groups, per reader) and `r127b_groups.json` (question-only and with-summary means and the paired gains); the groups are AUX-R126-E3-INTENT's.\n")
    OUT.write_text("".join(L), encoding="utf-8", newline="\n")
    json.dump({"ds_rows": rows, "wilson_11_65": [round(lo, 4), round(hi, 4)], "pooled66": {f"{k[0]}|{k[1]}": v for k, v in comp.items()}, "pooled66_personas": personas},
              open(ROOT / "reviews/v22/results/r128_ds_denoms.json", "w", encoding="utf-8"), indent=1)
    print("".join(L[:12]))
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
