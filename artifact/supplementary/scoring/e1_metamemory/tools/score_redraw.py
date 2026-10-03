"""
score_redraw.py -- E1.6 scoring: redrawn frontier AUROCs beside the single-draw values,
with the frozen Run-A interpretation rule re-applied to the redrawn FOK delta.

NO new calls. Reads redraw_frontier.json, strong_model.json (single-draw blind) and
run_a_frontier_indexed.json (single-draw indexed).
"""

from __future__ import annotations

import collections
import io
import json
import statistics as st
import sys
from pathlib import Path

E1 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from score_e1 import auroc, boot, ece  # noqa: E402


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def cell(keys, blind, indexed, items, judgment="fok", positive="non-ABSENT"):
    lab = lambda k: items[k].get("label", items[k]["label_pre"])
    ks = [k for k in keys
          if blind.get(k, {}).get(judgment) is not None
          and indexed.get(k, {}).get(judgment) is not None]
    y = [((0 if lab(k) == "ABSENT" else 1) if positive == "non-ABSENT"
          else (1 if lab(k) == "PRESENT-NEGATIVE" else 0)) for k in ks]
    if len(set(y)) < 2:
        return {"n": len(ks), "note": "single-class"}
    b = [blind[k][judgment] for k in ks]
    i = [indexed[k][judgment] for k in ks]
    ab, ai = auroc(b, y), auroc(i, y)
    return {"n": len(ks), "n_pos": int(sum(y)), "blind": ab, "indexed": ai,
            "delta": ai - ab, "bootstrap": boot(b, i, y),
            "mean_blind": st.mean(b), "mean_indexed": st.mean(i),
            "blind_ece": ece(b, y), "indexed_ece": ece(i, y)}


def main():
    rd = jload(E1 / "redraw_frontier.json")
    items = {i["item_id"]: i
             for i in jload(E1 / "build" / "items_final.json")}
    rblind = {r["item_id"]: r for r in rd["rows"] if r["arm"] == "BLIND"}
    rind = {r["item_id"]: r for r in rd["rows"] if r["arm"] == "INDEXED-TRUE"}
    sblind = {r["item_id"]: r for r in jload(E1 / "strong_model.json")["rows"]}
    sind = {r["item_id"]: r for r in jload(E1 / "run_a_frontier_indexed.json")["rows"]}

    frb = sorted(k for k in rind if items[k]["backend"] == "frbank")
    ext = sorted(k for k in rind if items[k]["backend"] != "frbank")
    allk = sorted(rind)

    res = {"k": rd["k"], "n_calls": rd["n_calls"],
           "n_excluded_lt_min_draws": rd["n_excluded_lt_min_draws"]}

    print("=" * 104)
    print(f"E1.6 FRONTIER REDRAW  k={rd['k']}, per-item mean  ({rd['n_calls']} calls)")
    print("=" * 104)

    # ---- realised draw-to-draw spread
    ident = sum(1 for r in rd["rows"] if r["fok_all_identical"])
    sds = [r["fok_sd"] for r in rd["rows"]]
    res["spread"] = {"n_cells": len(rd["rows"]),
                     "all_identical": ident,
                     "frac_all_identical": ident / max(len(rd["rows"]), 1),
                     "mean_sd": st.mean(sds), "median_sd": st.median(sds),
                     "max_sd": max(sds)}
    print(f"  draw-to-draw spread: {ident}/{len(rd['rows'])} cells identical across all "
          f"{rd['k']} draws ({ident/max(len(rd['rows']),1):.0%});")
    print(f"    per-item SD  mean {st.mean(sds):.4f}  median {st.median(sds):.4f}  "
          f"max {max(sds):.4f}")

    # ---- FOK, redrawn beside single-draw
    print(f"\n{'cell':30s} {'n':>4s} {'blind':>17s} {'indexed':>17s} {'delta':>19s}")
    print(f"{'':30s} {'':>4s} {'1-draw   k=5':>17s} {'1-draw   k=5':>17s} "
          f"{'1-draw    k=5':>19s}")
    for name, keys in (("FR-Bank (PRIMARY)", frb), ("external", ext), ("all 150", allk)):
        r5 = cell(keys, rblind, rind, items)
        r1 = cell(keys, sblind, sind, items)
        if "delta" not in r5:
            continue
        res[name] = {"redraw": r5, "single_draw": r1}
        print(f"  {name:28s} {r5['n']:4d} "
              f"{r1['blind']:8.4f} {r5['blind']:8.4f} "
              f"{r1['indexed']:8.4f} {r5['indexed']:8.4f} "
              f"{r1['delta']:+9.4f} {r5['delta']:+9.4f}")
        c = r5["bootstrap"]
        print(f"  {'':28s}      k=5 CI [{c['ci_lo']:+.4f}, {c['ci_hi']:+.4f}]  "
              f"excludes0={c['excludes_zero']}")

    # ---- frozen Run-A rule, re-applied to the redrawn FR-Bank FOK delta
    p = res["FR-Bank (PRIMARY)"]["redraw"]
    rule = "a" if (p["delta"] >= 0.10 and p["bootstrap"]["excludes_zero"]) else "b"
    prev = res["FR-Bank (PRIMARY)"]["single_draw"]
    prev_rule = "a" if (prev["delta"] >= 0.10
                        and prev["bootstrap"]["excludes_zero"]) else "b"
    res["rule"] = {"redraw": rule, "single_draw": prev_rule, "reversed": rule != prev_rule,
                   "text": ("mechanism generalizes up the capability ladder" if rule == "a"
                            else "cheap-model equalizer")}
    print(f"\n  FROZEN RUN-A RULE on the REDRAWN FR-Bank delta: ({rule}) {res['rule']['text']}")
    print(f"    single-draw fired ({prev_rule}); "
          f"{'REVERSED by re-estimation' if rule != prev_rule else 'unchanged'}")

    # ---- NOK, redrawn (exploratory, ungated)
    n5 = cell(frb, rblind, rind, items, judgment="nok", positive="PRESENT-NEGATIVE")
    n1 = cell(frb, sblind, sind, items, judgment="nok", positive="PRESENT-NEGATIVE")
    res["NOK_frbank"] = {"redraw": n5, "single_draw": n1}
    if "delta" in n5:
        print(f"\n  frontier NOK, FR-Bank (exploratory, ungated) n={n5['n']}, "
              f"{n5['n_pos']} PN:")
        print(f"    blind   1-draw {n1['blind']:.4f}  k=5 {n5['blind']:.4f}")
        print(f"    indexed 1-draw {n1['indexed']:.4f}  k=5 {n5['indexed']:.4f}")
        print(f"    delta   1-draw {n1['delta']:+.4f}  k=5 {n5['delta']:+.4f}  "
              f"CI [{n5['bootstrap']['ci_lo']:+.4f}, {n5['bootstrap']['ci_hi']:+.4f}]")

    with io.open(E1 / "results" / "redraw_scores.json", "w",
                 encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=2, sort_keys=True, default=float)
        f.write("\n")
    print(f"\nwrote {E1/'results'/'redraw_scores.json'}")


if __name__ == "__main__":
    main()
