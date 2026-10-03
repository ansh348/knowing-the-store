"""cf3_score.py -- ADDENDUM_CF3 §5: score the 42-item expiry cell and the pooled expiry row (CF-2's 30 expiry pairs + these 14).

NO API CALLS. Estimators are cf2_score's (common_e1r): Mann-Whitney AUROC with ties at 0.5; the item-level paired
bootstrap (1,000 draws, seed 42, single-class draws discarded) with the persona-clustered interval beside it; the
weaker reading stated where they disagree. Blind is one call per question reused across its three versions, so blind
AUROC is 0.5 by identity on both cells and on the pool. Lookups: score_cf.matcher (embedding) and run_nb6.lex_scores
(lexical) on the v2 superseded-names list and the v3 all-states list, exactly as cf2_score builds them. Draw collapse:
score_cf.load_lane (X4: MIN_DRAWS 3, arithmetic mean; k = 1 rows pass as single draws).

The pooled row: CF-2's expiry items (90; the recorded rows cf2/rows/rows_{MINI,H45,OP5}.jsonl, never re-run) plus the
CF-3 items (42) = 132 items, 44 positives; the pooling is disclosed in every printed form (two cells, two dates, two
registrations; Opus 5 k = 5 on CF-2's rows and k = 1 here).

Usage: python r82_counterfactual/cf3/cf3_score.py     -> cf3/results/cf_scores_cf3.json
"""
from __future__ import annotations

import io
import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from common_e1r import auroc, boot_cluster, boot_cluster_single, boot_item  # noqa: E402
from index_v3 import named_sections  # noqa: E402
from run_nb6 import lex_scores  # noqa: E402
import score_cf as S  # noqa: E402

CF2 = ROOT / "r82_counterfactual" / "cf2"
CF3 = ROOT / "r82_counterfactual" / "cf3"
OUT = CF3 / "results" / "cf_scores_cf3.json"
LANES = {"MINI": "gpt-4.1-mini", "H45": "claude-haiku-4-5-20251001", "OP5": "claude-opus-5"}
ARMS = (("INDEXED-V2", "v2"), ("INDEXED-V3", "v3"), ("INDEXED-V2R", "v2r"))
LOOKUP_ARM = {"v2": "superseded-names lookup (v2)", "v3": "all-states lookup (v3)", "v2r": "superseded-names lookup (v2; v2r shares v2's lists)"}
REG_SHA = "2f555c1ac4c3018e66a0fc453be7c4c4d3ffd4e3a2f7ac63c5c7b3590ca4f910"


def J(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    p.parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=1, sort_keys=True, default=float)
        f.write("\n")


def paired(b, i, y, g):
    it, cl = boot_item(b, i, y), boot_cluster(b, i, y, g)
    wide = it if (it.get("ci_hi", 0) - it.get("ci_lo", 0)) >= (cl.get("ci_hi", 0) - cl.get("ci_lo", 0)) else cl
    return {"delta": round(float(auroc(i, y) - auroc(b, y)), 4), "item_ci": it, "persona_ci": cl,
            "both_exclude_zero": bool(it.get("excludes_zero") and cl.get("excludes_zero")), "agree": bool(it.get("excludes_zero") == cl.get("excludes_zero")),
            "weaker": {"which": "item" if wide is it else "persona", "ci_lo": wide.get("ci_lo"), "ci_hi": wide.get("ci_hi"), "excludes_zero": wide.get("excludes_zero")}}


def load_cell(d, tag):
    cell = J(d / "cf_cell.json"); items = cell["items"]
    idx = J(d / "cf_indexes.json")["indexes"]
    qmap = {q: f"q{n:03d}" for n, q in enumerate(sorted({it["question"] for it in items}))}
    for it in items:
        it["_cell"], it["_q"] = tag, qmap[it["question"]]
    return items, idx


def lookups(items, idx):
    qs = [it["question"] for it in items]
    sup2 = [named_sections(idx[it["_cell"]][it["item_id"]]["v2"])["superseded"] for it in items]
    s3 = [named_sections(idx[it["_cell"]][it["item_id"]]["v3"]) for it in items]
    all3 = [s["superseded"] + s["retracted"] + s["expired"] for s in s3]
    out = {"emb_v2": S.matcher(qs, sup2), "emb_v3": S.matcher(qs, all3),
           "lex_v2": np.array(lex_scores([{"question": q, "names": l} for q, l in zip(qs, sup2)], "names"), float),
           "lex_v3": np.array(lex_scores([{"question": q, "names": l} for q, l in zip(qs, all3)], "names"), float)}
    return out


def score_set(items, idx, lanes_by_cell, label):
    y = np.array([it["y_nok"] for it in items], int); g = np.array([it["persona"] for it in items])
    b = np.full(len(items), 0.5)                     # the blind identity; each lane's own blind is loaded below and checked
    L = lookups(items, idx)
    res = {"label": label, "n": len(items), "pairs": len(items) // 3, "pos": int(y.sum()), "personas": int(len(set(g))), "lookups": {}, "models": {}}
    for k, s_ in L.items():
        res["lookups"][k] = {"auroc": round(float(auroc(s_, y)), 4), "persona_ci": boot_cluster_single(s_, y, g)}
    for code, model in LANES.items():
        lane = {}
        ok = True
        for it in items:
            ln = lanes_by_cell[it["_cell"]].get(code)
            if ln is None:
                ok = False; break
            for arm, tag in ARMS:
                v = ln.get((it["item_id"], arm))
                if v is None:
                    ok = False
                lane[(it["item_id"], arm)] = v
            bv = ln.get((it["_q"], "BLIND"))
            if bv is None:
                ok = False
            lane[(it["item_id"], "BLIND")] = bv
        if not ok:
            res["models"][model] = {"status": "lane not complete on this set"}; continue
        bl = np.array([lane[(it["item_id"], "BLIND")] for it in items], float)
        row = {"blind_auroc": round(float(auroc(bl, y)), 4), "blind_identity_0.5": bool(abs(auroc(bl, y) - 0.5) < 1e-9)}
        for arm, tag in ARMS:
            i = np.array([lane[(it["item_id"], arm)] for it in items], float)
            r = paired(bl, i, y, g)
            r.update({"indexed": round(float(auroc(i, y)), 4), "indexed_ci_persona": boot_cluster_single(i, y, g)})
            lk = "v3" if tag == "v3" else "v2"
            r["model_minus_emb_lookup"] = paired(L[f"emb_{lk}"], i, y, g); r["model_minus_emb_lookup"]["lookup"] = LOOKUP_ARM[tag]
            r["model_minus_lex_lookup"] = paired(L[f"lex_{lk}"], i, y, g)
            row[tag] = r
        if "v2" in row and "v2r" in row:
            i2 = np.array([lane[(it["item_id"], "INDEXED-V2")] for it in items], float); ir = np.array([lane[(it["item_id"], "INDEXED-V2R")] for it in items], float)
            row["v2r_minus_v2"] = paired(i2, ir, y, g)
        res["models"][model] = row
    return res


def main():
    it2, idx2 = load_cell(CF2, "cf2"); it3, idx3 = load_cell(CF3, "cf3")
    idx = {"cf2": idx2, "cf3": idx3}
    S.R82 = CF2; lanes2 = {code: S.load_lane(code) for code in LANES}
    S.R82 = CF3; lanes3 = {code: S.load_lane(code) for code in LANES}
    lanes_by_cell = {"cf2": lanes2, "cf3": lanes3}
    exp2 = [it for it in it2 if it["state"] == "EXPIRY"]
    assert len(exp2) == 90 and len(it3) == 42
    res = {"registration_sha256": REG_SHA, "cells": {}}
    res["cells"]["cf3"] = score_set(it3, idx, lanes_by_cell, "CF-3 expiry cell: 14 pairs, 42 items")
    res["cells"]["cf2_expiry"] = score_set(exp2, idx, lanes_by_cell, "CF-2 expiry slice: 30 pairs, 90 items (recorded rows)")
    res["cells"]["pooled"] = score_set(exp2 + it3, idx, lanes_by_cell, "pooled expiry: CF-2's 30 pairs + CF-3's 14 = 44 pairs, 132 items (two cells, two dates, two registrations; Opus 5 k = 5 on CF-2's rows, k = 1 on CF-3's)")
    # the CF-2 expiry slice must reproduce the ledgered lookup values (AUX-CF2-NB6-V2 / ALLSTATES-V3 per state: 0.5000 / 0.8711)
    c2 = res["cells"]["cf2_expiry"]["lookups"]
    res["gate"] = {"cf2_expiry_emb_v2": c2["emb_v2"]["auroc"], "cf2_expiry_emb_v3": c2["emb_v3"]["auroc"],
                   "expected": {"emb_v2": 0.5, "emb_v3": 0.8711}, "ok": c2["emb_v2"]["auroc"] == 0.5 and c2["emb_v3"]["auroc"] == 0.8711}
    jdump(res, OUT)
    for name, c in res["cells"].items():
        print(f"\n== {c['label']}")
        print("   lookups: " + "  ".join(f"{k} {v['auroc']:.4f}" for k, v in c["lookups"].items()))
        for model, row in c["models"].items():
            if "status" in row:
                print(f"   {model}: {row['status']}"); continue
            print(f"   {model}: blind {row['blind_auroc']:.4f}  " + "  ".join(f"{tag} {row[tag]['indexed']:.4f} [{row[tag]['weaker']['ci_lo']:+.3f},{row[tag]['weaker']['ci_hi']:+.3f}]" for _, tag in ARMS if tag in row)
                  + f"  | v2−emb {row['v2']['model_minus_emb_lookup']['delta']:+.4f} v3−emb {row['v3']['model_minus_emb_lookup']['delta']:+.4f}")
    print("\ngate (CF-2 expiry slice lookups reproduce):", res["gate"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
