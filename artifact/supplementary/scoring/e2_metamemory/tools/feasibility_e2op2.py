"""feasibility_e2op2.py -- E2-OP2 STEP (a) feasibility + (b) the tau grid.

Two things, in this order, and NOTHING else:

  (a) FEASIBILITY. Is the UNGATED policy assembly-constructible? For every one of
      the 529 eval items, does an S1-facts row, an S2-facts-caution row, and a NOK
      monitoring score all resolve? Coverage only -- no control outcome is
      aggregated here.

  (b) TAU GRID, MONITORING DATA ONLY. D40-E2's rule family applied to the UNGATED
      population: the lowest grid tau whose PN precision clears that population's
      base rate. PN labels and NOK scores only; no answer, no judge verdict, no
      confabulation rate is read.

The confabulation endpoint is deliberately NOT computed in this file. It is not
touched until PREREG_E2OP2 is frozen.
"""
from __future__ import annotations

import collections
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E2 = ROOT / "e2_metamemory"

GRID = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def main():
    gates = [g for g in jload(E2 / "gates_eval.json")["rows"] if g.get("split") == "eval"]
    tags = sorted(g["item_id"] for g in gates)
    by = {g["item_id"]: g for g in gates}
    ans = jload(E2 / "answers_eval.json")["rows"]
    J = jload(E2 / "cache" / "judgments_eval.json")

    # ---------------- (a) feasibility: coverage only
    have = collections.defaultdict(set)
    sha = {}
    for a in ans:
        have[a["item_id"]].add(a["state"])
        sha[(a["item_id"], a["state"])] = a["response_sha"]

    need = ("S1-facts", "S2-facts-caution")
    miss_rows = [t for t in tags if not set(need) <= have[t]]
    miss_verdict = [(t, s) for t in tags for s in need
                    if (t, s) not in sha or f"{t}|{sha[(t, s)][:24]}" not in J]
    nok_missing = [t for t in tags
                   if by[t].get("indexed", {}).get("1", {}).get("nok") is None]

    print("(a) FEASIBILITY -- ungated policy, caution iff nok >= tau over ALL eval items")
    print(f"  eval items                              : {len(tags)}")
    print(f"  items with BOTH S1 and S2 answer rows   : {len(tags) - len(miss_rows)} / {len(tags)}")
    print(f"  judge verdicts resolving for those rows : "
          f"{len(tags) * 2 - len(miss_verdict)} / {len(tags) * 2}")
    print(f"  items with a NOK monitoring score       : {len(tags) - len(nok_missing)} / {len(tags)}")
    gaps = {"items_missing_answer_row": miss_rows,
            "rows_missing_verdict": miss_verdict,
            "items_missing_nok": nok_missing}
    ok = not (miss_rows or miss_verdict or nok_missing)
    print(f"  GAPS: {'none -- assembly-constructible' if ok else gaps}")

    # the ungated policy uses no S0 at all; record that explicitly
    print(f"\n  note: the ungated policy assigns S2 (selected) or S1 (not selected) to")
    print(f"        every item and never uses S0-nofacts, because there is no FOK gate.")

    # ---------------- (b) tau grid, monitoring only
    nok = {t: (by[t]["indexed"]["1"]["nok"] or 0.0) for t in tags}
    pn = {t: 1 if by[t]["label"] == "PRESENT-NEGATIVE" else 0 for t in tags}
    base = sum(pn.values()) / len(tags)
    print(f"\n(b) TAU GRID -- monitoring data only, UNGATED population")
    print(f"  n = {len(tags)}   PN = {sum(pn.values())}   base rate = {base:.4f}")
    print(f"\n  {'tau':>5s} {'selected':>9s} {'precision':>10s} {'recall':>8s} "
          f"{'youden J':>9s}  strict subset")
    grid = []
    npos, nneg = sum(pn.values()), len(tags) - sum(pn.values())
    for t in GRID:
        sel = [x for x in tags if nok[x] >= t]
        if not sel:
            grid.append({"tau": t, "selected": 0, "note": "empty"})
            print(f"  {t:5.2f} {0:9d} {'-':>10s} {'-':>8s} {'-':>9s}  no")
            continue
        tp = sum(pn[x] for x in sel)
        prec = tp / len(sel)
        rec = tp / npos
        fpr = (len(sel) - tp) / nneg
        strict = 0 < len(sel) < len(tags)
        grid.append({"tau": t, "selected": len(sel), "precision": prec, "recall": rec,
                     "youden_j": rec - fpr, "strict_subset": bool(strict),
                     "clears_base": bool(prec >= base)})
        print(f"  {t:5.2f} {len(sel):9d} {prec:10.4f} {rec:8.4f} {rec - fpr:9.4f}"
              f"  {'yes' if strict else 'NO'}"
              + ("   <- clears base" if prec >= base else ""))

    elig = [g for g in grid if g.get("strict_subset") and g.get("clears_base")]
    tau = elig[0]["tau"] if elig else None
    print(f"\n  D40-E2 rule: lowest grid tau, strict subset, precision >= base rate "
          f"{base:.4f}")
    if tau is None:
        print("  -> NO ELIGIBLE TAU. Degenerate. STOP.")
    else:
        e = elig[0]
        print(f"  -> tau_OP2 = {tau}   selected {e['selected']} / {len(tags)} "
              f"({e['selected'] / len(tags):.4f})   precision {e['precision']:.4f} "
              f"vs base {base:.4f}   Youden {e['youden_j']:.4f}")

    out = {"feasibility": {"n_eval": len(tags), "gaps": gaps,
                           "assembly_constructible": bool(ok),
                           "uses_S0": False},
           "base_rate_ungated": base, "n_pn": sum(pn.values()),
           "grid": grid, "tau_op2": tau,
           "max_youden": max((g.get("youden_j", -9) for g in grid))}
    io.open(E2 / "results" / "e2op2_tau.json", "w", encoding="utf-8").write(
        json.dumps(out, indent=2))
    print(f"\n  written: results/e2op2_tau.json")
    print("  NO control outcome was aggregated in this file.")


if __name__ == "__main__":
    main()
