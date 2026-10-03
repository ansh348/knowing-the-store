# -*- coding: utf-8 -*-
"""a3_single_draw.py -- CC_PASS_v18 A3: single-draw scores for the five-call models, and the resolution confound.
NO MODEL CALL. $0.

For Opus 5 and Haiku 4.5 on the counterfactual set (444; cf2/rows, INDEXED-V2) and for Opus 5, Haiku 4.5 and Luna on the
full obligation set (661; r74/x4/rows, INDEXED-TRUE): the AUROC of draw 1 alone; the AUROC of each draw and the range
across draws; the number of distinct score values per draw and after averaging; the paired difference of draw 1 against
the superseded-names lookup with both intervals (cf2_score.paired; model minus lookup); and the same for the five-draw
mean. The model-minus-lookup gap is the abstract's numeral under the reader claim, so it prints for every model at draw 1
and at the mean. GPT-4.1 mini (k=1) prints beside them with its distinct-value count. For Section 4, mini's redraw
stability from the recorded artifacts: the 50-question k=3 blind redraw (scores_e1.json k3_noise) and the 102-prompt
TRUE redraw (scores_resp.json L1.redraw).

Gates: the five-draw means reproduce Opus v2 0.8405 and its +0.0742 over the lookup (cf_scores_cf2.json), Haiku v2 0.7566,
Haiku 661 TRUE 0.8210, Opus 661 0.8327, Luna 661 0.8182; the lookups 0.7663 (444) and 0.7484 (661).
Branch: B1 if Opus draw 1 keeps its margin over the lookup on the 444 with both intervals excluding zero; else B2.

Usage: python reviews/v18/tools/a3_single_draw.py
Writes: reviews/v18/results/a3_single_draw.json
"""
from __future__ import annotations

import collections
import io
import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "resp_review/tools", "ds_downstream/tools", "r74/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from common_e1r import N_BOOT, SEED, auroc  # noqa: E402
from index_v3 import named_sections  # noqa: E402
import score_cf as S  # noqa: E402
from cf2_score import paired  # noqa: E402
sys.path.insert(0, str(ROOT / "reviews" / "v18" / "tools"))
from a1_count_readers import r4  # noqa: E402

CF2 = ROOT / "r82_counterfactual" / "cf2"
X4 = ROOT / "r74" / "x4"
OUT = ROOT / "reviews" / "v18" / "results" / "a3_single_draw.json"
GATES = {"444": {"lookup": 0.7663, "claude-opus-5": (0.8405, 0.0742), "claude-haiku-4-5-20251001": (0.7566, None), "gpt-4.1-mini": (0.7167, None)},
         "661": {"lookup": 0.7484, "claude-opus-5": (0.8327, None), "claude-haiku-4-5-20251001": (0.8210, None), "gpt-5.6-luna": (0.8182, None), "gpt-4.1-mini": (0.7339, None)}}
MIN_DRAWS = 3


def draws(path, arm, key):
    """-> {unit: {draw: nok}} for one arm, OK rows only."""
    per = collections.defaultdict(dict)
    for ln in io.open(path, encoding="utf-8"):
        r = json.loads(ln)
        if r["arm"] == arm and r.get("status") == "OK" and r.get("nok") is not None:
            per[r[key]][int(r["draw"])] = float(r["nok"])
    return per


def analyse(per, units, look, y, g, name, gate):
    """per-draw and mean rows for one model on one set."""
    ks = sorted({d for u in units for d in per.get(u, {})})
    rows = {"draws_present": ks, "per_draw": {}, "units": len(units)}
    vec = {}
    for d in ks:
        v = np.array([per.get(u, {}).get(d, np.nan) for u in units], float)
        cov = int((~np.isnan(v)).sum())
        rows["per_draw"][d] = {"covered": cov, "auroc": r4(auroc(v[~np.isnan(v)], y[~np.isnan(v)])) if cov else None,
                               "distinct_values": int(len(np.unique(np.round(v[~np.isnan(v)], 6))))}
        vec[d] = v
    aur = [rows["per_draw"][d]["auroc"] for d in ks if rows["per_draw"][d]["auroc"] is not None]
    rows["range_across_draws"] = {"min": min(aur), "max": max(aur), "spread": r4(max(aur) - min(aur))} if aur else None
    # the recorded collapse: mean over >= MIN_DRAWS draws (k=1 lanes: the single draw)
    mean = np.full(len(units), np.nan)
    for k, u in enumerate(units):
        vs = [x for x in per.get(u, {}).values()]
        if len(vs) >= MIN_DRAWS or len(vs) == 1:
            mean[k] = float(np.mean(vs))
    m = ~np.isnan(mean)
    rows["mean"] = {"covered": int(m.sum()), "auroc": r4(auroc(mean[m], y[m])), "distinct_values": int(len(np.unique(np.round(mean[m], 6)))),
                    "vs_lookup": paired(look[m], mean[m], y[m], g[m]), "lookup_auroc": r4(auroc(look[m], y[m]))}
    if gate:
        a, dlt = gate
        assert rows["mean"]["auroc"] == a, f"GATE: {name} mean {rows['mean']['auroc']} != {a}"
        if dlt is not None:
            assert rows["mean"]["vs_lookup"]["delta"] == dlt, f"GATE: {name} mean minus lookup {rows['mean']['vs_lookup']['delta']} != {dlt}"
    if 1 in vec:
        v = vec[1]; m1 = ~np.isnan(v)
        rows["draw1"] = {"covered": int(m1.sum()), "auroc": r4(auroc(v[m1], y[m1])), "distinct_values": rows["per_draw"][1]["distinct_values"],
                         "vs_lookup": paired(look[m1], v[m1], y[m1], g[m1]), "lookup_auroc": r4(auroc(look[m1], y[m1]))}
    rows["gap_model_minus_lookup"] = {"draw1": rows.get("draw1", {}).get("vs_lookup", {}).get("delta"), "mean": rows["mean"]["vs_lookup"]["delta"]}
    return rows


def main():
    res = {"meta": {"script": "reviews/v18/tools/a3_single_draw.py", "model_calls": 0, "n_boot": N_BOOT, "seed": SEED, "paired_sign": "model minus lookup",
                    "collapse": "mean over at least three draws (X4); k=1 lanes are their single draw"}, "gates": {}, "cf444": {}, "obl661": {}}

    # ---- the 444
    cell = json.load(io.open(CF2 / "cf_cell.json", encoding="utf-8")); items = cell["items"]
    idx = json.load(io.open(CF2 / "cf_indexes.json", encoding="utf-8"))["indexes"]
    y = np.array([it["y_nok"] for it in items], int); g = np.array([it["persona"] for it in items]); units = [it["item_id"] for it in items]
    look = S.matcher([it["question"] for it in items], [named_sections(idx[u]["v2"])["superseded"] for u in units])
    lk = r4(auroc(look, y)); assert lk == GATES["444"]["lookup"]; res["gates"]["lookup_444"] = lk
    for code, name in (("OP5", "claude-opus-5"), ("H45", "claude-haiku-4-5-20251001"), ("MINI", "gpt-4.1-mini")):
        per = draws(CF2 / "rows" / f"rows_{code}.jsonl", "INDEXED-V2", "unit_id")
        res["cf444"][name] = analyse(per, units, look, y, g, name, GATES["444"][name])

    # ---- the 661
    from ds_common import load_cell, lookup_scores  # noqa: E402
    from common_e1r import load_e1  # noqa: E402
    sub = load_cell(); units = [it["item_id"] for it in sub]
    y = np.array([it["y_nok"] for it in sub], int); g = np.array([it["persona"] for it in sub])
    nb6, _, gate = lookup_scores(sub); assert gate["pass"]; res["gates"]["lookup_661"] = r4(gate["nb6_661"])
    look = np.array([nb6[u] for u in units], float)
    for code, name in (("OP5", "claude-opus-5"), ("H45", "claude-haiku-4-5-20251001"), ("LUNA", "gpt-5.6-luna")):
        per = draws(X4 / f"rows_{code}.jsonl", "INDEXED-TRUE", "item_id")
        res["obl661"][name] = analyse(per, units, look, y, g, name, GATES["661"][name])
    _, _, idxT, _ = load_e1()
    per = {u: {1: float(idxT[u]["nok"])} for u in units}
    res["obl661"]["gpt-4.1-mini"] = analyse(per, units, look, y, g, "gpt-4.1-mini", GATES["661"]["gpt-4.1-mini"])

    # ---- mini's redraw stability (recorded)
    e1 = json.load(io.open(ROOT / "e1_metamemory" / "results" / "scores_e1.json", encoding="utf-8"))
    rs = json.load(io.open(ROOT / "resp_review" / "run" / "scores_resp.json", encoding="utf-8"))
    res["mini_redraw"] = {"k3_blind_50": e1.get("k3_noise"), "true_redraw_102": rs["L1"]["redraw"]["all"]["redraw_minus_true"],
                          "sources": ["e1_metamemory/results/scores_e1.json k3_noise (NUMBERS.md AUX 46 of 50)", "resp_review/run/scores_resp.json L1.redraw (AUX-RESP-L1-REDRAW)"]}

    # ---- branch
    op = res["cf444"]["claude-opus-5"]["draw1"]["vs_lookup"]
    b1 = op["delta"] > 0 and op["both_exclude_zero"]
    res["branch"] = {"fires": "B1" if b1 else "B2", "opus_draw1_minus_lookup_444": op["delta"], "item_ci": [op["item_ci"]["ci_lo"], op["item_ci"]["ci_hi"]],
                     "persona_ci": [op["persona_ci"]["ci_lo"], op["persona_ci"]["ci_hi"]],
                     "wording": ("Section 4 states the resolution confound and dismisses it with this number; the abstract keeps 'the largest model reads slightly more'." if b1 else
                                 "Section 5: the largest model's five-call average exceeds the lookup by 0.07; a single call does not separate from it. Abstract: 'and the largest model's averaged score slightly more'.")}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=1, sort_keys=True, default=float); f.write("\n")

    print("A3 single draw -- gates:", res["gates"])
    for setname in ("cf444", "obl661"):
        print(f"\n== {setname} ==")
        for name, r in res[setname].items():
            pd = r["per_draw"]
            print(f"  {name}: draws {r['draws_present']}; per-draw AUROC " + ", ".join(f"d{d} {pd[d]['auroc']} ({pd[d]['distinct_values']} values, {pd[d]['covered']} covered)" for d in r["draws_present"])
                  + (f"; range {r['range_across_draws']['min']}..{r['range_across_draws']['max']} (spread {r['range_across_draws']['spread']})" if r["range_across_draws"] else ""))
            mn = r["mean"]; print(f"      mean: {mn['auroc']} ({mn['distinct_values']} values); minus lookup {mn['vs_lookup']['delta']:+.4f} item [{mn['vs_lookup']['item_ci']['ci_lo']:+.4f},{mn['vs_lookup']['item_ci']['ci_hi']:+.4f}] persona [{mn['vs_lookup']['persona_ci']['ci_lo']:+.4f},{mn['vs_lookup']['persona_ci']['ci_hi']:+.4f}] both_exclude_zero={mn['vs_lookup']['both_exclude_zero']}")
            if "draw1" in r and len(r["draws_present"]) > 1:
                d1 = r["draw1"]; print(f"      draw 1: {d1['auroc']} ({d1['distinct_values']} values); minus lookup {d1['vs_lookup']['delta']:+.4f} item [{d1['vs_lookup']['item_ci']['ci_lo']:+.4f},{d1['vs_lookup']['item_ci']['ci_hi']:+.4f}] persona [{d1['vs_lookup']['persona_ci']['ci_lo']:+.4f},{d1['vs_lookup']['persona_ci']['ci_hi']:+.4f}] both_exclude_zero={d1['vs_lookup']['both_exclude_zero']}")
    print("\nmini redraw:", json.dumps(res["mini_redraw"]["k3_blind_50"]), "|", json.dumps(res["mini_redraw"]["true_redraw_102"]))
    print("\nbranch:", json.dumps(res["branch"], indent=1))
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
