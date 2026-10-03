# -*- coding: utf-8 -*-
"""r129_hybrid_mini5.py -- R129 (2026-09-20), the author's B2: GPT-4.1 mini's five-draw row (R122 T3, rows_MINI5.jsonl, the INDEXED-V2 arm;
AUX-R122-K5, whole set 0.7648) minus the E10 hybrid reader, paired, beside the recorded one-draw row's difference (-0.0698, AUX-CF2-HYB-VS-MODELS).

The hybrid's out-of-fold vector is not stored in cf_scores_hybrid.json, so it is recomputed here exactly as r82_counterfactual/tools/cf2_hybrid.py
computes it (the same features, the same folds, the same sklearn call; deterministic), and gated on the recorded values: the hybrid's whole-set
AUROC 0.7865 and the one-draw mini row's difference -0.0698 must reproduce before the five-draw difference is written. The five-draw rows are read
from the committed blob (git HEAD: reviews/r122/rows/rows_MINI5.jsonl; the working-tree copy is unstaged by another session), their whole-set AUROC
gated on 0.7648. No model call. Writes reviews/v22/results/r129_hybrid_mini5.json.
Usage: python reviews/v22/tools/r129_hybrid_mini5.py
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[3]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "reviews/v19/tools", "reviews/v18/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402
import cf2_reader_score as R  # noqa: E402
from cf2_hybrid import nb1_share, GATE_NB1, GATE_LOOKUP, CF2  # noqa: E402
from common_e1r import auroc  # noqa: E402
from cf2_score import paired  # noqa: E402

OUT = ROOT / "reviews" / "v22" / "results" / "r129_hybrid_mini5.json"
HYB = json.load(io.open(CF2 / "results" / "cf_scores_hybrid.json", encoding="utf-8"))
GATE_HYBRID = HYB["hybrid"]["whole"]                                   # 0.7865
GATE_MINI1 = HYB["models_minus_hybrid"]["MINI"]["minus_hybrid"]        # delta -0.0698 with its intervals
GATE_MINI5 = 0.7648                                                    # AUX-R122-K5 (mini k = 5, v2, whole set)
BLOB = "reviews/r122/rows/rows_MINI5.jsonl"


def r4(x):
    return round(float(x), 4)


def hybrid_vector(items, idx):
    y = np.array([it["y_nok"] for it in items], int); g = np.array([it["persona"] for it in items])
    f1 = R.lookup_v2(items, idx)
    f2 = np.zeros(len(items)); f3 = np.zeros(len(items))
    for k, it in enumerate(items):
        f2[k], f3[k] = nb1_share(idx[it["item_id"]]["v2"], it["question"])
    assert r4(auroc(f2, y)) == GATE_NB1 and r4(auroc(f1, y)) == GATE_LOOKUP
    v = np.full(len(items), np.nan)
    for persona in sorted(set(g)):
        tr, te = g != persona, g == persona
        mu = np.array([f1[tr].mean(), f2[tr].mean()]); sd = np.array([f1[tr].std(), f2[tr].std()]); sd[sd == 0] = 1.0
        X = np.column_stack([(f1 - mu[0]) / sd[0], (f2 - mu[1]) / sd[1], f3])
        clf = LogisticRegression(C=1.0, penalty="l2", solver="lbfgs", max_iter=1000).fit(X[tr], y[tr])
        v[te] = clf.predict_proba(X[te])[:, 1]
    assert not np.isnan(v).any()
    got = r4(auroc(v, y)); assert got == GATE_HYBRID, ("GATE: hybrid whole", got, GATE_HYBRID)
    return v, y, g


def rows_mini5():
    p = ROOT / BLOB
    if p.exists():
        return p, "working tree"
    sha = subprocess.run(["git", "rev-parse", f"HEAD:{BLOB}"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    data = subprocess.run(["git", "show", f"HEAD:{BLOB}"], cwd=ROOT, capture_output=True, check=True).stdout
    tmp = Path(tempfile.gettempdir()) / "rows_MINI5_r129.jsonl"
    tmp.write_bytes(data)
    return tmp, f"git HEAD blob {sha}"


def main():
    items, idx = R.cell()
    v, y, g = hybrid_vector(items, idx)
    # the recorded one-draw row reproduces the recorded difference
    col1, _ = R.collapse(CF2 / "rows" / "rows_MINI.jsonl", "INDEXED-V2")
    m1 = np.array([col1[it["item_id"]] for it in items], float)
    d1 = paired(v, m1, y, g)
    assert d1["delta"] == GATE_MINI1["delta"], ("GATE: mini k=1 minus hybrid", d1["delta"], GATE_MINI1["delta"])
    assert d1["item_ci"]["ci_lo"] == GATE_MINI1["item_ci"]["ci_lo"] and d1["persona_ci"]["ci_hi"] == GATE_MINI1["persona_ci"]["ci_hi"]
    # the five-draw row
    path, source = rows_mini5()
    col5, census = R.collapse(path, "INDEXED-V2")
    m5 = np.array([col5[it["item_id"]] for it in items], float)
    got5 = r4(auroc(m5, y)); assert got5 == GATE_MINI5, ("GATE: mini k=5 whole", got5, GATE_MINI5)
    d5 = paired(v, m5, y, g)
    res = {"source_rows": {"path": BLOB, "read_from": source, "census": census},
           "gates": {"hybrid_whole": GATE_HYBRID, "mini_k1_minus_hybrid": GATE_MINI1["delta"], "mini_k5_whole": GATE_MINI5},
           "mini_k1": {"model": r4(auroc(m1, y)), "minus_hybrid": d1},
           "mini_k5": {"model": got5, "minus_hybrid": d5},
           "reliable_either_direction": bool(d5["item_ci"]["excludes_zero"] and d5["persona_ci"]["excludes_zero"])}
    OUT.write_text(json.dumps(res, indent=1, sort_keys=True, default=float), encoding="utf-8")
    print(f"mini k=1 {res['mini_k1']['model']:.4f} minus hybrid {R.fmt_paired(d1)}")
    print(f"mini k=5 {got5:.4f} minus hybrid {R.fmt_paired(d5)}  reliable in either direction: {res['reliable_either_direction']}")
    print("->", OUT)


if __name__ == "__main__":
    main()
