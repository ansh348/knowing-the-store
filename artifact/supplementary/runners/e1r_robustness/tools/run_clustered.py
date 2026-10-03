"""E1-R sub-step (a): persona-clustered bootstrap + leave-one-persona-out.

Frozen by SPEC_E1R.md. Reproduction gate runs first: if any published point estimate
fails to re-derive to 4 decimals, this script aborts before computing any sensitivity.
"""
from __future__ import annotations

import sys

import numpy as np

from common_e1r import (POPULATIONS, OUT, assemble, auroc, boot_cluster, boot_item,
                        jdump, load_e1, lopo)

# Published values from the manuscript / central ledger, used only as a reproduction gate.
PUBLISHED = {
    "R-FOK-HARD": dict(n=588, blind=0.5258, indexed=0.7530, delta=+0.2272,
                       ci=(+0.1177, +0.3504)),
    "R-FOK-FRB":  dict(n=307, blind=0.4966, indexed=0.7003, delta=+0.2037,
                       ci=(+0.0935, +0.3191)),
    "R-FOK-EASY": dict(n=595, blind=0.4422, indexed=0.6336, delta=+0.1914, ci=None),
    "R-NOK-FRB":  dict(n=661, blind=0.4946, indexed=0.7339, delta=+0.2393,
                       ci=(+0.1801, +0.2949)),
    "R-FOK-MEM0": dict(n=238, blind=0.5746, indexed=0.4777, delta=-0.0969,
                       ci=(-0.169, -0.025)),
    "R-FOK-AMEM": dict(n=284, blind=0.5591, indexed=0.4526, delta=-0.1065,
                       ci=(-0.173, -0.040)),
}


def main():
    items, blind, idxT, idxB = load_e1()
    res, gate_fail = {}, []

    for rid, spec in POPULATIONS.items():
        sub = [it for it in items if spec["filt"](it)]
        b, i, y, g, ids = assemble(sub, blind, idxT, judgment=spec["judgment"])
        pub = PUBLISHED[rid]

        ab, ai = auroc(b, y), auroc(i, y)
        d = ai - ab
        repro = {
            "n": int(len(y)), "n_pub": pub["n"], "n_ok": int(len(y)) == pub["n"],
            "blind": round(ab, 4), "blind_pub": pub["blind"],
            "blind_ok": abs(ab - pub["blind"]) < 5e-5,
            "indexed": round(ai, 4), "indexed_pub": pub["indexed"],
            "indexed_ok": abs(ai - pub["indexed"]) < 5e-5,
            "delta": round(d, 4), "delta_pub": pub["delta"],
            "delta_ok": abs(d - pub["delta"]) < 5e-5,
        }
        if not all(repro[k] for k in ("n_ok", "blind_ok", "indexed_ok", "delta_ok")):
            gate_fail.append((rid, repro))

        n_clusters = int(len(set(g.tolist())))
        pos_clusters = int(len(set(g[y == 1].tolist())))
        res[rid] = {
            "reproduction": repro,
            "n": int(len(y)), "n_pos": int(y.sum()),
            "n_personas": n_clusters, "n_personas_with_positive": pos_clusters,
            "mean_items_per_persona": float(len(y) / n_clusters),
            "point_delta": float(d),
            "ci_item_published": list(pub["ci"]) if pub["ci"] else None,
            "ci_item_rederived": boot_item(b, i, y),
            "ci_cluster": boot_cluster(b, i, y, g),
            "lopo": lopo(b, i, y, g),
        }

    if gate_fail:
        print("REPRODUCTION GATE FAILED -- no sensitivity computed.")
        for rid, r in gate_fail:
            print(" ", rid, r)
        jdump({"gate": "FAILED", "rows": res}, OUT / "clustered.json")
        sys.exit(1)

    # ---- STOP condition evaluation
    stop = []
    for rid, r in res.items():
        pub_ci = r["ci_item_published"]
        if not pub_ci:
            continue
        item_excl = pub_ci[0] > 0 or pub_ci[1] < 0
        cl = r["ci_cluster"]
        clu_excl = cl.get("excludes_zero", False)
        r["stop_condition_triggered"] = bool(item_excl and not clu_excl)
        if r["stop_condition_triggered"]:
            stop.append(rid)

    out = {"gate": "PASSED", "rows": res, "stop_rows": stop,
           "spec": "e1r_robustness/SPEC_E1R.md @ 9ac91a2"}
    jdump(out, OUT / "clustered.json")

    print("=" * 100)
    print("E1-R (a)  PERSONA-CLUSTERED BOOTSTRAP AND LEAVE-ONE-PERSONA-OUT")
    print("=" * 100)
    print("reproduction gate: PASSED on all rows (n, blind, indexed, delta to 4 dp)\n")
    hdr = (f"{'row':13s} {'n':>4s} {'pers':>5s} {'+pers':>6s} {'delta':>8s} "
           f"{'item CI':>22s} {'cluster CI':>22s} {'width x':>8s}")
    print(hdr)
    print("-" * len(hdr))
    for rid, r in res.items():
        it_ci = r["ci_item_rederived"]
        cl = r["ci_cluster"]
        w_it = it_ci["ci_hi"] - it_ci["ci_lo"]
        w_cl = cl["ci_hi"] - cl["ci_lo"]
        flag = "  <-- STOP" if r.get("stop_condition_triggered") else ""
        print(f"{rid:13s} {r['n']:4d} {r['n_personas']:5d} {r['n_personas_with_positive']:6d} "
              f"{r['point_delta']:+8.4f} "
              f"[{it_ci['ci_lo']:+.4f},{it_ci['ci_hi']:+.4f}] "
              f"[{cl['ci_lo']:+.4f},{cl['ci_hi']:+.4f}] "
              f"{w_cl / w_it:7.2f}x{flag}")
    print()
    print("leave-one-persona-out")
    for rid, r in res.items():
        L = r["lopo"]
        print(f"  {rid:13s} folds={L['n_folds']:3d}  delta range "
              f"[{L['min_delta']:+.4f}, {L['max_delta']:+.4f}]  "
              f"sign changes={L['n_sign_changes']}")
    print()
    if stop:
        print(f"*** STOP CONDITION TRIGGERED on {len(stop)} row(s): {', '.join(stop)}")
        print("*** Report to PI before any manuscript sentence is edited.")
    else:
        print("STOP condition not triggered: every published-significant row stays significant.")
    print(f"\nwrote {OUT / 'clustered.json'}")


if __name__ == "__main__":
    main()