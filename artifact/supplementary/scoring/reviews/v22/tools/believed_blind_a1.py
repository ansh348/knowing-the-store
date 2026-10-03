"""believed_blind_a1.py -- the store-written (BELIEVED) coverage summary against blind on Mem0 and A-MEM (R112, review-2 A1).

A $0 computation on the recorded E1 rows: the paired delta BELIEVED-indexed minus blind, with the item-level paired
bootstrap and the persona-clustered paired bootstrap, both exactly as e1r_robustness/tools/common_e1r.py defines them
(N_BOOT 1000, seed 42; the estimators transcribed from the preregistered scorer). The point values must reproduce
e1_metamemory/NUMBERS.md section 7 (Mem0 blind 0.5746, BELIEVED 0.5741, delta -0.0005; A-MEM 0.5591, 0.5278, -0.0313)
before any interval is written; otherwise the script exits 1 and writes nothing.

The ruling's phrasing rule is evaluated here and printed: "within tolerance of blind" iff |delta| <= 0.05 and both
intervals include zero; otherwise the delta with its intervals and no adjective.

Writes reviews/v19/results/believed_blind_a1.json. No model call.
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "e1r_robustness" / "tools"))
from common_e1r import POPULATIONS, assemble, auroc, boot_cluster, boot_item, load_e1  # noqa: E402

OUT = ROOT / "reviews" / "v19" / "results" / "believed_blind_a1.json"
TOL = 0.05

# e1_metamemory/NUMBERS.md section 7 (E1 believed-state axis), the ledgered point values.
LEDGER = {
    "R-FOK-MEM0": dict(n=238, blind=0.5746, believed=0.5741, delta=-0.0005),
    "R-FOK-AMEM": dict(n=284, blind=0.5591, believed=0.5278, delta=-0.0313),
}


def main():
    items, blind, idxT, idxB = load_e1()
    out, fail = {}, []
    for rid, led in LEDGER.items():
        spec = POPULATIONS[rid]
        sub = [it for it in items if spec["filt"](it)]
        b, i, y, g, ids = assemble(sub, blind, idxB, judgment=spec["judgment"])
        ab, ai = auroc(b, y), auroc(i, y)
        d = ai - ab
        repro = {
            "n": int(len(y)), "n_ledger": led["n"],
            "blind": round(ab, 4), "blind_ledger": led["blind"],
            "believed": round(ai, 4), "believed_ledger": led["believed"],
            "delta": round(d, 4), "delta_ledger": led["delta"],
        }
        ok = (len(y) == led["n"] and abs(ab - led["blind"]) < 5e-5 and abs(ai - led["believed"]) < 5e-5
              and abs(round(d, 4) - led["delta"]) < 5e-5)
        if not ok:
            fail.append((rid, repro))
            continue
        ci_item = boot_item(b, i, y)
        ci_cl = boot_cluster(b, i, y, g)
        within = (abs(d) <= TOL) and (not ci_item["excludes_zero"]) and (not ci_cl["excludes_zero"])
        out[rid] = {
            "reproduction": repro, "n": int(len(y)), "n_pos": int(y.sum()),
            "n_personas": int(len(set(g.tolist()))),
            "point_delta": float(d),
            "ci_item": ci_item, "ci_cluster": ci_cl,
            "tolerance": TOL,
            "phrase": "within tolerance of blind" if within else "delta with its intervals, no adjective",
        }
    if fail:
        print("REPRODUCTION GATE FAILED -- nothing written.")
        for rid, r in fail:
            print(" ", rid, r)
        sys.exit(1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True, default=float) + "\n", encoding="utf-8")
    for rid, r in out.items():
        ci, cc = r["ci_item"], r["ci_cluster"]
        print(f"{rid}: n={r['n']} pos={r['n_pos']} personas={r['n_personas']}  blind={r['reproduction']['blind']:.4f} "
              f"believed={r['reproduction']['believed']:.4f}  delta={r['point_delta']:+.4f}  "
              f"item [{ci['ci_lo']:+.4f},{ci['ci_hi']:+.4f}] (draws {ci['n_draws']})  "
              f"persona [{cc['ci_lo']:+.4f},{cc['ci_hi']:+.4f}] (draws {cc['n_draws']})  -> {r['phrase']}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
