"""
score_mechanism.py -- E1.8 STEP 2 scoring, per E1_8_ADDENDUM.md (281c410).

E1's scoring procedure unchanged, imported from score_e1 rather than re-typed:
rank-based AUROC with ties at 0.5, positive class = NON-ABSENT, ECE (10 bins),
Brier, and the paired bootstrap (1,000 resamples, seed 42, items resampled,
both arms moving together).

Rows: PRIMARY pooled hard tier n=588 (reference intact 0.7530 / blind 0.5258),
SECONDARY FR-Bank hard tier n=307 (0.7003 / 0.4966), and the slot-ablated
slice descriptively.

The frozen interpretation rules are read mechanically. NO recommendation is
produced anywhere in this file.

Usage:  python e1_metamemory/tools/score_mechanism.py
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from score_e1 import auroc, boot, brier, ece  # noqa: E402

OUT = E1 / "results" / "mechanism_scores.json"
ARMS = ("A1-counts-jittered", "A2-counts-coarsened", "A3-names-only")
SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}

REF = {"pooled": {"n": 588, "intact": 0.7530353913717386, "blind": 0.5258331180573496},
       "frbank": {"n": 307, "intact": 0.7003151260504201, "blind": 0.4965861344537815}}
WITHIN = 0.05


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True, default=float)
        f.write("\n")


def main():
    items = [i for i in jload(E1 / "build" / "items_final.json")
             if i["tier"] == "hard" and i.get("label", i["label_pre"]) in SCOREABLE]
    main_rows = jload(E1 / "elicitation_main.json")
    blind = {r["question"]: r for r in main_rows
             if r["arm"] == "BLIND" and r["status"] == "OK"}
    intact = {r["tag"]: r for r in main_rows
              if r["arm"] == "INDEXED-TRUE" and r["status"] == "OK"}
    qmap = {r["tag"]: r["question"] for r in main_rows if r["arm"] != "BLIND"}
    mech = {}
    for r in jload(E1 / "mechanism_elicitation.json"):
        if r["status"] == "OK" and r["fok"] is not None:
            mech[(r["item_id"], r["arm"])] = r

    def slice_rows(pred, name):
        """Assemble a paired matrix over the items passing `pred`."""
        keys, y, b, i0, arms = [], [], [], [], {a: [] for a in ARMS}
        for it in items:
            if not pred(it):
                continue
            tag = it["item_id"]
            q = qmap.get(tag)
            if q not in blind or tag not in intact:
                continue
            if any((tag, a) not in mech for a in ARMS):
                continue
            bv, iv = blind[q].get("fok"), intact[tag].get("fok")
            if bv is None or iv is None:
                continue
            keys.append(tag)
            y.append(0 if it.get("label", it["label_pre"]) == "ABSENT" else 1)
            b.append(bv)
            i0.append(iv)
            for a in ARMS:
                arms[a].append(mech[(tag, a)]["fok"])
        if len(set(y)) < 2:
            # Expected on the external backends: their whole hard tier is ABSENT
            # (every hard-tier positive in the study is an FR-Bank PN item), so
            # AUROC is undefined there. Mean FOK is reported instead.
            return {"row": name, "n": len(y), "n_pos": int(sum(y)),
                    "note": "single-class; AUROC undefined",
                    "mean_fok": {"blind": sum(b) / max(len(b), 1),
                                 "intact": sum(i0) / max(len(i0), 1),
                                 **{a: sum(arms[a]) / max(len(arms[a]), 1)
                                    for a in ARMS}}}
        res = {"row": name, "n": len(y), "n_pos": int(sum(y)),
               "blind_auroc": auroc(b, y), "intact_auroc": auroc(i0, y),
               "arms": {}}
        for a in ARMS:
            s = arms[a]
            res["arms"][a] = {
                "auroc": auroc(s, y),
                "ece": ece(s, y), "brier": brier(s, y),
                "delta_vs_intact": auroc(s, y) - auroc(i0, y),
                "delta_vs_blind": auroc(s, y) - auroc(b, y),
                "bootstrap_vs_intact": boot(i0, s, y),
                "bootstrap_vs_blind": boot(b, s, y),
            }
        return res

    res = {"n_items_hard": len(items),
           "n_mech_responses": len(mech),
           "frozen_reference": REF, "within_threshold": WITHIN}
    res["PRIMARY_pooled"] = slice_rows(lambda it: True, "PRIMARY pooled hard tier")
    res["SECONDARY_frbank"] = slice_rows(lambda it: it["backend"] == "frbank",
                                         "SECONDARY FR-Bank hard tier")
    res["slot_ablated"] = slice_rows(lambda it: it["variant"] == "SLOT-ABLATED",
                                     "slot-ablated slice (descriptive)")
    # Decomposition of the FR-Bank hard tier into its two contrasts. Its 35
    # positives are all slot-ablated PN items; its negatives are 127 slot-ablated
    # ABSENT plus 145 FR-Bank natural-absent probes. Those are different tests
    # and the pooled row does not separate them.
    res["frbank_pn_vs_natural"] = slice_rows(
        lambda it: it["backend"] == "frbank" and (
            it.get("label", it["label_pre"]) == "PRESENT-NEGATIVE"
            or it["variant"] == "FULL"),
        "FR-Bank: PN vs natural-absent (decomposition)")
    for b in ("frbank", "mem0", "amem"):
        res[f"backend_{b}"] = slice_rows(lambda it, b=b: it["backend"] == b,
                                         f"{b} hard tier (descriptive)")

    # ------------------------------------------------- frozen rules, mechanical
    def verdict(row, ref):
        a = {k: v["auroc"] for k, v in row["arms"].items()}
        within = {k: abs(v - ref["intact"]) <= WITHIN for k, v in a.items()}
        ordered = (a["A1-counts-jittered"] > a["A2-counts-coarsened"]
                   > a["A3-names-only"])
        a3 = row["arms"]["A3-names-only"]["bootstrap_vs_blind"]
        a3_indistinct_from_blind = not a3["excludes_zero"]
        if all(within.values()):
            v = ("ALL WITHIN 0.05 OF REFERENCE -- the signal is the "
                 "category-coverage map x question-specificity, counts not "
                 "load-bearing; this ANSWERS the 'reading a table you built' "
                 "objection with a mechanism")
        elif ordered and a3_indistinct_from_blind:
            v = ("COLLAPSE TOWARD BLIND with A1 > A2 > A3 ordering -- counts are "
                 "load-bearing and the leakage question REOPENS")
        else:
            v = ("MIXED / NON-MONOTONE -- mechanism partially resolved; the "
                 "pattern is reported, no forced story")
        return {"auroc": a, "within_0.05_of_intact": within,
                "ordering_A1_gt_A2_gt_A3": ordered,
                "A3_indistinguishable_from_blind": a3_indistinct_from_blind,
                "A3_vs_blind_ci": [a3["ci_lo"], a3["ci_hi"]],
                "verdict": v}

    res["VERDICT_primary"] = verdict(res["PRIMARY_pooled"], REF["pooled"])
    res["VERDICT_secondary_frbank"] = verdict(res["SECONDARY_frbank"], REF["frbank"])
    res["rows_agree"] = (res["VERDICT_primary"]["verdict"]
                         == res["VERDICT_secondary_frbank"]["verdict"])
    jdump(res, OUT)

    # ------------------------------------------------------------------ report
    for key, ref in (("PRIMARY_pooled", REF["pooled"]),
                     ("SECONDARY_frbank", REF["frbank"]),
                     ("slot_ablated", None), ("frbank_pn_vs_natural", None),
                     ("backend_amem", None), ("backend_mem0", None)):
        r = res[key]
        print("=" * 98)
        print(f"{r['row']}   n={r['n']}  n_pos={r['n_pos']}")
        print("=" * 98)
        if "note" in r:
            print(f"  {r['note']} -- mean FOK instead:")
            for a, v in r["mean_fok"].items():
                print(f"    {a:24s}{v:8.4f}")
            print()
            continue
        print(f"  {'blind':24s}{r['blind_auroc']:8.4f}")
        print(f"  {'intact index':24s}{r['intact_auroc']:8.4f}")
        for a in ARMS:
            v = r["arms"][a]
            ci = v["bootstrap_vs_intact"]
            print(f"  {a:24s}{v['auroc']:8.4f}   vs intact {v['delta_vs_intact']:+7.4f} "
                  f"CI [{ci['ci_lo']:+.4f}, {ci['ci_hi']:+.4f}]"
                  f"{'  *' if ci['excludes_zero'] else '   '}"
                  f"   vs blind {v['delta_vs_blind']:+7.4f}")
        if ref:
            print(f"  reference: intact {ref['intact']:.4f} / blind {ref['blind']:.4f}"
                  f"  (|arm - intact| <= {WITHIN})")
        print()

    for k in ("VERDICT_primary", "VERDICT_secondary_frbank"):
        v = res[k]
        print("=" * 98)
        print(k)
        print("=" * 98)
        print(f"  within 0.05 of intact: "
              + ", ".join(f"{a.split('-')[0]}={v['within_0.05_of_intact'][a]}"
                          for a in ARMS))
        print(f"  A1 > A2 > A3 ordering: {v['ordering_A1_gt_A2_gt_A3']}")
        print(f"  A3 indistinguishable from blind: "
              f"{v['A3_indistinguishable_from_blind']}  "
              f"CI [{v['A3_vs_blind_ci'][0]:+.4f}, {v['A3_vs_blind_ci'][1]:+.4f}]")
        print(f"  VERDICT: {v['verdict']}")
        print()
    print(f"rows agree: {res['rows_agree']}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
