"""E1-R sub-step (a), continued: persona clustering on the 84-item matched cell.

Covers the capability-ladder and cross-vendor rows (Table 4). Personas come from item_id.
A reproduction gate runs first against the published Table 4 values.
"""
from __future__ import annotations

import collections
import io
import json
import sys

import numpy as np

from common_e1r import (E1, OUT, XV, auroc, boot_cluster, boot_cluster_single, boot_item,
                        jdump, load_e1, lopo, persona_of)

PUBLISHED = {
    ("mini", "FOK"):      (0.4488, 0.7090, +0.2602),
    ("mini", "NOK"):      (0.5000, 0.7139, +0.2139),
    ("luna", "FOK"):      (0.5735, 0.7417, +0.1682),
    ("luna", "NOK"):      (0.5585, 0.8526, +0.2940),
    ("sol", "FOK"):       (0.7099, 0.7463, +0.0364),
    ("sol", "NOK"):       (0.5290, 0.8588, +0.3298),
    ("Opus 5", "FOK"):    (0.5855, 0.7068, +0.1213),
    ("Opus 5", "NOK"):    (0.6994, 0.8523, +0.1528),
    ("Haiku 4.5", "FOK"): (0.3136, 0.7287, +0.4151),
    ("Haiku 4.5", "NOK"): (0.3688, 0.8199, +0.4511),
    ("K3", "FOK"):        (0.6651, 0.7222, +0.0571),
    ("K3", "NOK"):        (0.5983, 0.8588, +0.2605),
}
XV_MODELS = {
    "Opus 5": "claude-opus-5",
    "Haiku 4.5": "claude-haiku-4-5-20251001",
    "K3": "kimi-k3",
}


def cell84():
    m = json.load(io.open(XV / "manifests" / "cell_84.json", encoding="utf-8"))
    return {it["item_id"]: it for it in m["items"]}


def arms_from_prescored(path, cell):
    """luna / sol: rows already averaged over k draws, one per (item_id, arm)."""
    rows = json.load(io.open(path, encoding="utf-8"))["rows"]
    out = collections.defaultdict(dict)
    for r in rows:
        if r["item_id"] in cell:
            out[r["item_id"]][r["arm"]] = r
    return out


def arms_from_jsonl(model_id, cell):
    """cross-vendor lanes: reuse the COMMITTED scorer's own load/collapse.

    Reimplementing the aggregation drifted in the 3rd-4th decimal, because the frozen
    protocol dedups by (item_id, arm, draw, prompt_hash) with first-wins and averages the
    nok draws independently of the fok draws. Importing the committed functions removes
    that whole class of error.
    """
    sys.path.insert(0, str(XV / "tools"))
    import score_e1xv  # noqa: E402  -- committed frozen scorer

    rows = score_e1xv.load(model_id)
    coll, meta, _ = score_e1xv.collapse(rows)
    out = collections.defaultdict(dict)
    for (tag, arm), v in coll.items():
        if tag in cell:
            out[tag][arm] = v
    return dict(out)


def arms_from_mini(cell):
    """mini: the original E1 elicitation restricted to the matched cell."""
    items, blind, idxT, _ = load_e1()
    qmap = {it["item_id"]: it["question"] for it in items}
    out = {}
    for iid in cell:
        q = qmap.get(iid)
        if q in blind and iid in idxT:
            out[iid] = {"BLIND": blind[q], "INDEXED-TRUE": idxT[iid]}
    return out


def score(arm_map, cell, judgment):
    key = "y_fok" if judgment == "fok" else "y_nok"
    b, i, y, g = [], [], [], []
    for iid, arms in sorted(arm_map.items()):
        if "BLIND" not in arms or "INDEXED-TRUE" not in arms:
            continue
        bv = arms["BLIND"].get(judgment)
        iv = arms["INDEXED-TRUE"].get(judgment)
        if bv is None or iv is None:
            continue
        b.append(bv); i.append(iv)
        y.append(int(cell[iid][key]))
        g.append(persona_of(iid))
    return (np.array(b, float), np.array(i, float), np.array(y, int), np.array(g))


def main():
    cell = cell84()
    sources = {
        "mini": arms_from_mini(cell),
        "luna": arms_from_prescored(E1 / "ladder_gpt-5.6-luna.json", cell),
        "sol": arms_from_prescored(E1 / "redraw_frontier.json", cell),
    }
    for name, mid in XV_MODELS.items():
        sources[name] = arms_from_jsonl(mid, cell)

    res, fails = {}, []
    for model, arm_map in sources.items():
        for judgment, J in (("fok", "FOK"), ("nok", "NOK")):
            b, i, y, g = score(arm_map, cell, judgment)
            ab, ai = auroc(b, y), auroc(i, y)
            d = ai - ab
            pb, pi, pd = PUBLISHED[(model, J)]
            ok = (abs(ab - pb) < 5e-5 and abs(ai - pi) < 5e-5 and abs(d - pd) < 5e-5)
            if not ok:
                fails.append((model, J, round(ab, 4), pb, round(ai, 4), pi, round(d, 4), pd))
            tie = bool(len(set(b.tolist())) == 1)
            res[f"{model}|{J}"] = {
                "model": model, "judgment": J, "n": int(len(y)), "n_pos": int(y.sum()),
                "n_personas": int(len(set(g.tolist()))),
                "blind": float(ab), "indexed": float(ai), "delta": float(d),
                "reproduces_published": bool(ok),
                "blind_tie_degenerate": tie,
                "ci_item": boot_item(b, i, y),
                "ci_cluster": boot_cluster(b, i, y, g),
                "lopo": {k: v for k, v in lopo(b, i, y, g).items() if k != "folds"},
            }

    if fails:
        print("REPRODUCTION GATE FAILED")
        for f in fails:
            print("  ", f)
        jdump({"gate": "FAILED", "detail": fails}, OUT / "clustered_ladder.json")
        sys.exit(1)

    stop = [k for k, r in res.items()
            if r["ci_item"].get("excludes_zero") and not r["ci_cluster"].get("excludes_zero")]
    jdump({"gate": "PASSED", "rows": res, "stop_rows": stop,
           "spec": "e1r_robustness/SPEC_E1R.md @ 9ac91a2"}, OUT / "clustered_ladder.json")

    print("=" * 104)
    print("E1-R (a)  PERSONA-CLUSTERED BOOTSTRAP -- 84-item matched cell (Table 4 rows)")
    print("=" * 104)
    print("reproduction gate: PASSED on all 12 rows\n")
    hdr = (f"{'model':11s} {'J':4s} {'n':>3s} {'pers':>5s} {'delta':>8s} "
           f"{'item CI':>21s} {'cluster CI':>21s} {'w x':>6s} {'LOPO sign':>10s}")
    print(hdr)
    print("-" * len(hdr))
    for k, r in res.items():
        ci, cl = r["ci_item"], r["ci_cluster"]
        w = ((cl["ci_hi"] - cl["ci_lo"]) / (ci["ci_hi"] - ci["ci_lo"]))
        note = " TIE" if r["blind_tie_degenerate"] else ""
        flag = "  <-- STOP" if k in stop else ""
        print(f"{r['model']:11s} {r['judgment']:4s} {r['n']:3d} {r['n_personas']:5d} "
              f"{r['delta']:+8.4f} [{ci['ci_lo']:+.4f},{ci['ci_hi']:+.4f}] "
              f"[{cl['ci_lo']:+.4f},{cl['ci_hi']:+.4f}] {w:5.2f}x "
              f"{r['lopo']['n_sign_changes']:10d}{note}{flag}")
    print()
    if stop:
        print(f"*** STOP CONDITION TRIGGERED on {len(stop)} row(s): {', '.join(stop)}")
    else:
        print("STOP condition not triggered on the matched cell.")
    print(f"\nwrote {OUT / 'clustered_ladder.json'}")


if __name__ == "__main__":
    main()