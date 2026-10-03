"""
score_ladder.py -- E1.7 scoring: Luna cells, frozen predictions, three-point ladder.

NO new calls. Same bootstrap procedure as E1.6 (1,000 resamples, seed 42, items
resampled) plus a ONE-SAMPLE bootstrap CI on a single-arm AUROC, which P1 needs
and E1.6 did not.
"""

from __future__ import annotations

import collections
import io
import json
import statistics as st
import sys
from pathlib import Path

import numpy as np

E1 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from score_e1 import auroc, boot  # noqa: E402

N_BOOT, SEED = 1000, 42


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def auroc_ci(scores, y, n=N_BOOT, seed=SEED):
    """One-sample bootstrap CI on a single-arm AUROC (P1 needs this)."""
    rng = np.random.default_rng(seed)
    s, yy = np.asarray(scores, float), np.asarray(y, int)
    vals = []
    for _ in range(n):
        k = rng.integers(0, len(yy), len(yy))
        if yy[k].sum() in (0, len(k)):
            continue
        vals.append(auroc(s[k], yy[k]))
    v = np.asarray(vals)
    return {"point": auroc(s, yy), "ci_lo": float(np.percentile(v, 2.5)),
            "ci_hi": float(np.percentile(v, 97.5)),
            "includes_0.50": bool(np.percentile(v, 2.5) <= 0.50 <= np.percentile(v, 97.5))}


def cellset(keys, blind, indexed, items, judgment, positive):
    lab = lambda k: items[k].get("label", items[k]["label_pre"])
    ks = [k for k in keys if blind.get(k, {}).get(judgment) is not None
          and indexed.get(k, {}).get(judgment) is not None]
    y = [((0 if lab(k) == "ABSENT" else 1) if positive == "non-ABSENT"
          else (1 if lab(k) == "PRESENT-NEGATIVE" else 0)) for k in ks]
    if len(set(y)) < 2:
        return {"n": len(ks), "note": "single-class"}
    b = [blind[k][judgment] for k in ks]
    i = [indexed[k][judgment] for k in ks]
    return {"n": len(ks), "n_pos": int(sum(y)),
            "blind": auroc(b, y), "indexed": auroc(i, y),
            "delta": auroc(i, y) - auroc(b, y), "bootstrap": boot(b, i, y),
            "blind_ci": auroc_ci(b, y), "indexed_ci": auroc_ci(i, y),
            "mean_blind": st.mean(b), "mean_indexed": st.mean(i)}


def load_k5(path):
    d = jload(path)
    return ({r["item_id"]: r for r in d["rows"] if r["arm"] == "BLIND"},
            {r["item_id"]: r for r in d["rows"] if r["arm"] == "INDEXED-TRUE"}, d)


def main():
    items = {i["item_id"]: i for i in jload(E1 / "build" / "items_final.json")}
    lb, li, ld = load_k5(E1 / "ladder_gpt-5.6-luna.json")
    sb, si, sd = load_k5(E1 / "redraw_frontier.json")

    # mini, restricted to the same 150-item subset
    main_rows = jload(E1 / "elicitation_main.json")
    qmap = {r["tag"]: r["question"] for r in main_rows if r["arm"] != "BLIND"}
    mblind_q = {r["question"]: r for r in main_rows
                if r["arm"] == "BLIND" and r["status"] == "OK"}
    mind = {r["tag"]: r for r in main_rows
            if r["arm"] == "INDEXED-TRUE" and r["status"] == "OK"}
    subset = [r["item_id"] for r in jload(E1 / "strong_model.json")["rows"]]
    mblind = {k: mblind_q[qmap[k]] for k in subset if qmap.get(k) in mblind_q}

    frb = sorted(k for k in li if items[k]["backend"] == "frbank")
    ext = sorted(k for k in li if items[k]["backend"] != "frbank")
    allk = sorted(li)
    res = {"model": ld["model"], "k": ld["k"], "n_calls": ld["n_calls"],
           "prompt_texts_sha256": ld["prompt_texts_sha256"],
           "n_excluded": ld["n_excluded_lt_min_draws"]}

    print("=" * 100)
    print(f"E1.7 CAPABILITY LADDER — {ld['model']}, k={ld['k']}, {ld['n_calls']} calls")
    print("=" * 100)

    # ---------------- (a) Luna cells
    print("\n(a) LUNA cells")
    for nm, keys in (("FR-Bank primary", frb), ("external", ext), ("all 150", allk)):
        for j, pos in (("fok", "non-ABSENT"), ("nok", "PRESENT-NEGATIVE")):
            c = cellset(keys, lb, li, items, j, pos)
            if "delta" not in c:
                continue
            res[f"luna:{nm}:{j}"] = c
            print(f"  {nm:16s} {j.upper():4s} n={c['n']:3d} blind {c['blind']:.4f} "
                  f"indexed {c['indexed']:.4f} delta {c['delta']:+.4f} "
                  f"CI [{c['bootstrap']['ci_lo']:+.4f},{c['bootstrap']['ci_hi']:+.4f}]")

    # ---------------- (b) frozen predictions
    print("\n(b) FROZEN PREDICTIONS")
    nb = res.get("luna:FR-Bank primary:nok")
    p1pt, p1ci = nb["blind"], nb["blind_ci"]
    if p1pt < 0.60 and p1ci["includes_0.50"]:
        p1 = "HOLDS"
    elif p1pt >= 0.65 and not p1ci["includes_0.50"]:
        p1 = "FAILS"
    else:
        p1 = "INDETERMINATE"
    res["P1"] = {"verdict": p1, "point": p1pt,
                 "ci": [p1ci["ci_lo"], p1ci["ci_hi"]],
                 "includes_0.50": p1ci["includes_0.50"]}
    print(f"  P1 (LOAD-BEARING) Luna blind NOK at chance: point {p1pt:.4f}, "
          f"CI [{p1ci['ci_lo']:.4f},{p1ci['ci_hi']:.4f}], includes 0.50 "
          f"{p1ci['includes_0.50']}  ->  {p1}")
    if p1 == "FAILS":
        print("     VERBATIM: obligation awareness is partially capability-graded; "
              "the information-property claim is damaged.")

    mini_f = cellset(frb, mblind, mind, items, "fok", "non-ABSENT")
    mini_all = cellset(allk, mblind, mind, items, "fok", "non-ABSENT")
    luna_all = res["luna:all 150:fok"]
    sol_all = cellset(allk, sb, si, items, "fok", "non-ABSENT")
    p2 = mini_all["blind"] < luna_all["blind"] < sol_all["blind"]
    res["P2"] = {"holds": bool(p2), "mini": mini_all["blind"],
                 "luna": luna_all["blind"], "sol": sol_all["blind"]}
    print(f"  P2 blind FOK mini<luna<sol: {mini_all['blind']:.4f} / "
          f"{luna_all['blind']:.4f} / {sol_all['blind']:.4f}  ->  "
          f"{'HOLDS' if p2 else 'VIOLATED'}")

    luna_f = res["luna:FR-Bank primary:fok"]
    sol_f = cellset(frb, sb, si, items, "fok", "non-ABSENT")
    p3 = sol_f["delta"] < luna_f["delta"] < mini_f["delta"]
    res["P3"] = {"holds": bool(p3), "sol": sol_f["delta"],
                 "luna": luna_f["delta"], "mini": mini_f["delta"]}
    print(f"  P3 FOK delta sol<luna<mini: {sol_f['delta']:+.4f} / "
          f"{luna_f['delta']:+.4f} / {mini_f['delta']:+.4f}  ->  "
          f"{'HOLDS' if p3 else 'VIOLATED'}")

    nk = res["luna:FR-Bank primary:nok"]
    p4 = nk["delta"] > 0 and nk["bootstrap"]["excludes_zero"]
    res["P4"] = {"holds": bool(p4), "delta": nk["delta"],
                 "ci": [nk["bootstrap"]["ci_lo"], nk["bootstrap"]["ci_hi"]]}
    print(f"  P4 Luna NOK delta > 0, CI excludes 0: {nk['delta']:+.4f} "
          f"CI [{nk['bootstrap']['ci_lo']:+.4f},{nk['bootstrap']['ci_hi']:+.4f}]  ->  "
          f"{'HOLDS' if p4 else 'FAILS'}")

    supported = (p1 == "HOLDS") and p4
    res["headline"] = {"claim": "scale buys coverage discrimination, not obligation awareness",
                       "supported": bool(supported),
                       "rule": "SUPPORTED iff P1 and P4 both hold"}
    print(f"\n  CAPABILITY HEADLINE ('scale buys coverage discrimination, not obligation "
          f"awareness'): {'SUPPORTED' if supported else 'NOT SUPPORTED'}")

    # ---------------- (c) ladder table
    print("\n(c) LADDER (matched cells)")
    lad = {}
    for j, pos, keys, nm in (("fok", "non-ABSENT", frb, "FR-Bank FOK"),
                             ("nok", "PRESENT-NEGATIVE", frb, "FR-Bank NOK")):
        row = {"mini": cellset(keys, mblind, mind, items, j, pos),
               "luna": cellset(keys, lb, li, items, j, pos),
               "sol": cellset(keys, sb, si, items, j, pos)}
        lad[nm] = row
        print(f"  {nm}")
        for m in ("mini", "luna", "sol"):
            c = row[m]
            if "delta" in c:
                print(f"    {m:5s} n={c['n']:3d} blind {c['blind']:.4f} "
                      f"indexed {c['indexed']:.4f} delta {c['delta']:+.4f}")
    res["ladder"] = lad

    # ---------------- (d) lane reproducibility
    def repro(d):
        rows = d["rows"]
        ident = sum(1 for r in rows if r["fok_all_identical"])
        sds = [r["fok_sd"] for r in rows]
        return {"cells": len(rows), "identical": ident,
                "frac_identical": ident / max(len(rows), 1),
                "mean_sd": st.mean(sds), "median_sd": st.median(sds), "max_sd": max(sds)}
    res["reproducibility"] = {"luna": repro(ld), "sol": repro(sd)}
    print("\n(d) LANE REPRODUCIBILITY (standing disclosure)")
    for m, v in res["reproducibility"].items():
        print(f"  {m:5s} identical {v['identical']}/{v['cells']} "
              f"({v['frac_identical']:.0%}), per-item SD mean {v['mean_sd']:.4f} "
              f"median {v['median_sd']:.4f} max {v['max_sd']:.4f}")

    # ---------------- (e) blind vs indexed dispersion ratio (exploratory)
    print("\n(e) BLIND vs INDEXED dispersion across draws (exploratory)")
    disp = {}
    for m, d in (("luna", ld), ("sol", sd)):
        b = [r["fok_sd"] for r in d["rows"] if r["arm"] == "BLIND"]
        i = [r["fok_sd"] for r in d["rows"] if r["arm"] == "INDEXED-TRUE"]
        disp[m] = {"blind_mean_sd": st.mean(b), "indexed_mean_sd": st.mean(i),
                   "ratio_indexed_over_blind": st.mean(i) / st.mean(b) if st.mean(b) else None}
        print(f"  {m:5s} blind SD {st.mean(b):.4f}  indexed SD {st.mean(i):.4f}  "
              f"ratio {disp[m]['ratio_indexed_over_blind']:.3f}")
    k3 = jload(E1 / "elicitation_k3.json")
    byq = collections.defaultdict(list)
    for r in k3:
        if r["fok"] is not None:
            byq[r["question"]].append(r["fok"])
    msd = [st.stdev(v) for v in byq.values() if len(v) > 1]
    disp["mini"] = {"blind_mean_sd": st.mean(msd) if msd else None,
                    "indexed_mean_sd": None,
                    "note": "mini has k=3 on the BLIND arm only (50 questions); no "
                            "multi-draw indexed arm exists, so no ratio is computable"}
    print(f"  mini  blind SD {st.mean(msd):.4f} (k=3, 50 questions); "
          f"indexed multi-draw not available -> ratio not computable")
    res["dispersion"] = disp

    with io.open(E1 / "results" / "ladder_scores.json", "w",
                 encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=2, sort_keys=True, default=float)
        f.write("\n")
    print(f"\nwrote {E1/'results'/'ladder_scores.json'}")


if __name__ == "__main__":
    main()
