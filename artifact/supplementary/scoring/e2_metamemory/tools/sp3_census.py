"""
sp3_census.py -- SP3 completeness census. COVERAGE COUNTS ONLY.

Counts how many items HAVE a gate signal, an answer, a verdict -- never what any
of them said. No verdict value is tallied, no rate, no mean, no metric. A count of
`CORRECT` verdicts would be an aggregate of an eval outcome and is deliberately
not computed here.

Usage:  python e2_metamemory/tools/sp3_census.py
"""

from __future__ import annotations

import collections
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e2_common import E2, S0, S1, S2, jdump, jload, load_items    # noqa: E402


def main():
    items = load_items()
    cal = [i for i in items if i["split"] == "calibration"]
    ev = [i for i in items if i["split"] == "eval"]
    cen = {"registered_denominators": {}, "coverage": {}, "gaps": []}

    cen["registered_denominators"] = {
        "frbank_scoreable_total": len(items),
        "calibration_items": len(cal), "eval_items": len(ev),
        "eval_by_label": dict(collections.Counter(i["label_final"] for i in ev)),
        "eval_by_variant": dict(collections.Counter(i["variant"] for i in ev)),
        "context_states": 3, "policies": 7,
    }

    # ---- retrieval artifact
    fr = jload(E2 / "retrieval_frozen.json")
    frids = {r["item_id"] for r in fr["rows"]}
    cen["coverage"]["retrieval_artifact"] = {
        "rows": len(fr["rows"]), "distinct_items": len(frids),
        "covers_all_items": len(frids) == len(items),
        "sha256": fr["artifact_sha256"],
        "zero_fact_items": sum(1 for r in fr["rows"] if r["n_facts"] == 0),
        "v1_zero_leak": fr["validation"]["v1_zero_leak"],
        "v2_pass": fr["validation"]["v2_pass"],
    }

    # ---- gates
    for split, pool in (("calibration", cal), ("eval", ev)):
        g = jload(E2 / f"gates_{split}.json")
        rows = g["rows"]
        have_v = sum(1 for r in rows if (r["verbal"].get("1") or {})
                     .get("p_store_has_relevant") is not None)
        have_i = sum(1 for r in rows if (r["indexed"].get("1") or {})
                     .get("fok") is not None)
        have_s = sum(1 for r in rows if r.get("sim_max_blended") is not None)
        draws = sorted({int(d) for r in rows for d in r["verbal"]})
        cen["coverage"][f"gates_{split}"] = {
            "rows": len(rows), "denominator": len(pool), "k": g["k"],
            "draws_present": draws,
            "have_similarity_signal": have_s,
            "have_verbal_signal_draw1": have_v,
            "have_indexed_signal_draw1": have_i,
            "reused_from_e1": g.get("reused_from_e1"),
            "complete": (len(rows) == len(pool) and have_v == len(pool)
                         and have_i == len(pool) and have_s == len(pool)),
        }
        if not cen["coverage"][f"gates_{split}"]["complete"]:
            cen["gaps"].append(f"gates_{split}: incomplete signal coverage")

    # ---- answers + verdicts
    for split, pool in (("calibration", cal), ("eval", ev)):
        a = jload(E2 / f"answers_{split}.json")
        rows = a["rows"]
        by_state = collections.Counter(r["state"] for r in rows)
        distinct = {(r["item_id"], r["response_sha"]) for r in rows}
        empty = sum(1 for r in rows if not r["response"])
        j = jload(E2 / "cache" / f"judgments_{split}.json")
        keys = {f"{i}|{s[:24]}" for i, s in distinct}
        judged = sum(1 for k in keys if k in j)
        ok = sum(1 for k in keys if j.get(k, {}).get("status") == "OK")
        exp_s2 = len(pool) if a["s2_all"] else None
        cen["coverage"][f"answers_{split}"] = {
            "answerer": a["answerer_model"], "k": a["k"],
            "rows": len(rows), "by_state": dict(by_state),
            "denominator_per_state": len(pool),
            "s2_all": a["s2_all"], "expected_S2": exp_s2,
            "empty_responses": empty,
            "distinct_item_response_pairs": len(distinct),
            "verdicts_present": judged, "verdicts_OK": ok,
            "complete": (by_state[S0] == len(pool) * a["k"]
                         and by_state[S1] == len(pool) * a["k"]
                         and empty == 0 and ok == len(keys)),
        }
        if not cen["coverage"][f"answers_{split}"]["complete"]:
            cen["gaps"].append(f"answers_{split}: incomplete")

    # ---- modules
    for name, path, key in (("M1", "m1_factorial_raw.json", "cell"),
                            ("M2", "m2_renderer_raw.json", "cell")):
        p = E2 / path
        if not p.exists():
            cen["gaps"].append(f"{name}: not run")
            continue
        d = jload(p)
        c = collections.Counter((r[key], r["status"]) for r in d["rows"])
        cells = sorted({r[key] for r in d["rows"]})
        cen["coverage"][name] = {
            "rows": d["n"], "cells": cells,
            "per_cell_OK": {cl: c[(cl, "OK")] for cl in cells},
            "per_cell_FAIL": {cl: c[(cl, "PARSE_FAIL")] for cl in cells},
            "complete": all(c[(cl, "PARSE_FAIL")] == 0 for cl in cells),
        }
        if not cen["coverage"][name]["complete"]:
            cen["gaps"].append(f"{name}: parse failures present")

    # ---- P5
    p5 = sorted(E2.glob("p5_spotcheck_*.json"))
    if not p5:
        cen["coverage"]["P5"] = {"status": "not run"}
        cen["gaps"].append("P5: not run")
    else:
        d = jload(p5[0])
        if d.get("severed"):
            cen["coverage"]["P5"] = {"status": "SEVERED", "reason": d.get("reason"),
                                     "model": d.get("model")}
            cen["gaps"].append(f"P5: severed ({d.get('reason')}) — spot-check is "
                               f"severable by design and does not block SP3")
        else:
            c = collections.Counter((r["arm"], r["status"]) for r in d["rows"])
            arms = sorted({r["arm"] for r in d["rows"]})
            cen["coverage"]["P5"] = {
                "model": d["model"], "k": d["k"], "items": d["n_items"],
                "calls": d["n_calls"], "index_provenance": d["index_provenance"],
                "per_arm_OK": {a: c[(a, "OK")] for a in arms},
                "per_arm_FAIL": {a: sum(v for (aa, s), v in c.items()
                                        if aa == a and s != "OK") for a in arms},
                "cells_identical_across_k": d["cells_identical_across_k"],
                "n_cells": d["n_cells"], "bands_evaluated": d["bands_evaluated"],
                "complete": all(c[(a, "OK")] == d["k"] * d["n_items"] for a in arms),
            }
            if not cen["coverage"]["P5"]["complete"]:
                cen["gaps"].append("P5: incomplete draws")

    jdump(cen, E2 / "sp3_census.json")

    print("=" * 92)
    print("SP3 CENSUS — coverage counts only; no verdict value tallied")
    print("=" * 92)
    d = cen["registered_denominators"]
    print(f"  registered: {d['frbank_scoreable_total']} FR-Bank scoreable "
          f"= {d['calibration_items']} calibration + {d['eval_items']} eval")
    print(f"  eval by label: {d['eval_by_label']}")
    print(f"  eval by variant: {d['eval_by_variant']}")
    for k, v in cen["coverage"].items():
        mark = "OK " if v.get("complete") or v.get("covers_all_items") else "-- "
        print(f"\n  [{mark}] {k}")
        for kk, vv in v.items():
            if kk in ("complete", "covers_all_items"):
                continue
            print(f"        {kk}: {vv}")
    print("\n" + "=" * 92)
    print(f"GAPS: {len(cen['gaps'])}")
    for g in cen["gaps"]:
        print(f"  - {g}")
    print(f"\nwrote sp3_census.json")


if __name__ == "__main__":
    main()
