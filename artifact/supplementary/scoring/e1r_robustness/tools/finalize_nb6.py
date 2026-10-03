"""Merge NB-6 into the E1-R baseline table of record. R81 Phase 1.

Reads the committed results/baselines_final.json and results/nb6.json and writes
results/baselines_final_r81.json, the table of record for Table 18 from R81 onward.

TWO RULES, both from ADDENDUM_R81 section 3 (rider 1 of 2026-08-29):

  1. NB-1..NB-5 are READ, never recomputed. The published suite cannot drift underneath
     this addition.
  2. NB-6 enters the OBLIGATION rows only. On the coverage rows FOK-6 is definitionally
     NB-4 and NB-5, so printing it would repeat a number already in the table under two
     other names. Those cells carry a dash, `best` and the monitor delta are left exactly
     as committed, and the footnote gives the reason.

Usage: python e1r_robustness/tools/finalize_nb6.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_e1r import OUT, jdump, jload          # noqa: E402

TOL = 0.05
NB6_NAME = "NB-6 superseded-names match"


def main():
    base = jload(OUT / "baselines_final.json")
    nb6 = jload(OUT / "nb6.json")

    rows, notes = {}, []
    for key, row in base["rows"].items():
        out = dict(row)
        n6 = nb6["rows"].get(key)

        if n6 is None or row["judgment"] != "nok":
            # coverage rows and every external-backend row: no NB-6 cell
            out["nb6"] = None
            out["nb6_status"] = (
                "coverage row: FOK-6 is definitionally NB-4/NB-5, so no cell is printed"
                if row["judgment"] == "fok" and n6 is not None else
                "not scored: the superseded-names section is the inexpressibility marker"
                if row["row"] in ("R-FOK-MEM0", "R-FOK-AMEM") else
                "not in the NB-6 population")
            # best and delta are carried through UNCHANGED
            rows[key] = out
            continue

        legit = dict(row["legitimate_baselines"])
        legit[NB6_NAME] = n6["nb6_best"]
        best_name = max(legit, key=lambda k: legit[k])
        best = legit[best_name]
        mon = row["monitor_indexed"]

        out.update({
            "legitimate_baselines": legit,
            "nb6": {
                "lexical": n6["nb6_lexical"],
                "embedding": n6["nb6_embedding"],
                "best": n6["nb6_best"],
                "best_variant": n6["nb6_best_variant"],
                "mean_names_per_item": n6["mean_names_per_item"],
                "monitor_minus_nb6": n6["monitor_minus_nb6_best"],
                "nb6_exceeds_monitor": bool(n6["nb6_best"] > mon),
                "nb6_beats_monitor_beyond_tol": bool(n6["nb6_best"] > mon + TOL),
            },
            "nb6_status": "scored",
            "best_legit_baseline": best_name,
            "best_legit_auroc": best,
            "monitor_minus_best": mon - best,
            "baseline_matches": bool(abs(mon - best) < TOL),
            "baseline_wins_beyond_tol": bool(best > mon + TOL),
            "best_changed_by_nb6": bool(best_name == NB6_NAME),
            "best_before_nb6": row["best_legit_baseline"],
            "best_before_nb6_auroc": row["best_legit_auroc"],
            "monitor_minus_best_before_nb6": row["monitor_minus_best"],
        })
        rows[key] = out

        if out["best_changed_by_nb6"]:
            notes.append(
                f"{key}: best baseline moves from {row['best_legit_baseline']} "
                f"({row['best_legit_auroc']:.4f}) to {NB6_NAME} ({best:.4f}); "
                f"monitor delta {row['monitor_minus_best']:+.4f} -> {mon - best:+.4f}")

    jdump({
        "rows": rows,
        "matched_84_descriptive": nb6["matched_84_descriptive"],
        "verdicts": nb6["verdicts"],
        "tolerance": TOL,
        "nb6_column_scope": ("obligation rows only; coverage rows print a dash because "
                             "FOK-6 is definitionally NB-4/NB-5 (ADDENDUM_R81 section 3)"),
        "disqualification": base["disqualification"],
        "backend_indicator_pooled_hard": base["backend_indicator_pooled_hard"],
        "provenance": ("baselines_final.json (NB-1..NB-5, read not recomputed) "
                       "+ nb6.json (NB-6, R81)"),
        "registration": nb6["registration"],
        "best_changed_by_nb6": notes,
    }, OUT / "baselines_final_r81.json")

    w = max(len(k) for k in rows)
    print(f"{'row':{w}s}  {'judg':4s} {'monitor':>8s} {'NB-6':>8s} {'best':>8s} "
          f"{'mon-best':>9s}  status")
    for k, r in rows.items():
        n6 = r["nb6"]
        cell = f"{n6['best']:8.4f}" if n6 else "       -"
        flag = ""
        if n6 and n6["nb6_exceeds_monitor"]:
            flag = "  <-- NB-6 above the monitor"
        if r.get("best_changed_by_nb6"):
            flag += " [best changed]"
        print(f"{k:{w}s}  {r['judgment']:4s} {r['monitor_indexed']:8.4f} {cell} "
              f"{r['best_legit_auroc']:8.4f} {r['monitor_minus_best']:+9.4f}  "
              f"{r['nb6_status'][:38]}{flag}")
    if notes:
        print()
        for n in notes:
            print("  NOTE:", n)
    print(f"\nwrote {OUT / 'baselines_final_r81.json'}")


if __name__ == "__main__":
    main()
