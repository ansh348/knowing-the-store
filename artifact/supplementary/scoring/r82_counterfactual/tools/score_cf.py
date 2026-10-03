"""score_cf.py -- R82-CF: score the counterfactual cell under the frozen branches.

NO API CALLS. The offline encoder is the one the E1-R baseline suite uses, from the on-disk
cache. Estimators are the committed ones from common_e1r: Mann-Whitney AUROC with ties at
0.5, the preregistered item-level paired bootstrap (1000 draws, seed 42, single-class draws
discarded) as primary, and the clustered paired bootstrap grouped BY QUESTION beside it.
Tolerance 0.05.

Draw collapse follows the X4 protocol: dedup on draw, drop cells below MIN_DRAWS=3, take the
arithmetic mean. mini is k=1.

Blind is one call per question, reused across that question's three versions, so blind AUROC
is 0.5 by the identity registered in ADDENDUM_R82 section 6. It is printed, not suppressed.

Usage:  python r82_counterfactual/tools/score_cf.py
Writes: r82_counterfactual/results/cf_scores.json
"""
from __future__ import annotations

import collections
import io
import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in ("e1r_robustness/tools", "r82_counterfactual"):
    sys.path.insert(0, str(ROOT / p))

import numpy as np  # noqa: E402
from common_e1r import auroc, boot_cluster, boot_cluster_single, boot_item  # noqa: E402
from index_features import parse as parse_index  # noqa: E402
from index_v3 import named_sections  # noqa: E402

R82 = ROOT / "r82_counterfactual"
OUT = R82 / "results" / "cf_scores.json"
TOL = 0.05
MIN_DRAWS = 3
LANES = {"MINI": "gpt-4.1-mini", "H45": "claude-haiku-4-5-20251001",
         "OP5": "claude-opus-5"}

_ENC = {}


def encoder():
    if "m" not in _ENC:
        from sentence_transformers import SentenceTransformer
        _ENC["m"] = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2",
                                        device="cpu")
    return _ENC["m"]


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def load_lane(code):
    """-> {(unit_id, arm): mean score}. X4 collapse, unchanged."""
    path = R82 / "rows" / f"rows_{code}.jsonl"
    if not path.exists():
        return None
    per = collections.defaultdict(dict)
    for line in io.open(path, encoding="utf-8"):
        r = json.loads(line)
        if r.get("status") != "OK":
            continue
        per[(r["unit_id"], r["arm"])][r["draw"]] = r
    out = {}
    for k, draws in per.items():
        rs = list(draws.values())
        if len(rs) < MIN_DRAWS and len(rs) != 1:
            continue
        noks = [x["nok"] for x in rs if x["nok"] is not None]
        if noks:
            out[k] = float(np.mean(noks))
    return out


def matcher(questions, name_lists):
    """Max cosine of the question against a list of attribute names. NB-6's estimator."""
    enc = encoder()
    uq = sorted(set(questions))
    qv = dict(zip(uq, enc.encode(uq, normalize_embeddings=True, batch_size=128,
                                 show_progress_bar=False)))
    un = sorted({n for lst in name_lists for n in lst})
    nv = dict(zip(un, enc.encode([n.replace("_", " ") for n in un],
                                 normalize_embeddings=True, batch_size=256,
                                 show_progress_bar=False))) if un else {}
    out = []
    for q, lst in zip(questions, name_lists):
        out.append(max((float(qv[q] @ nv[n]) for n in lst), default=0.0))
    return np.array(out, float)


def summarise(b, i, y, g, label):
    d = auroc(i, y) - auroc(b, y)
    return {"label": label, "n": int(len(y)), "pos": int(y.sum()),
            "blind": round(float(auroc(b, y)), 4),
            "indexed": round(float(auroc(i, y)), 4),
            "delta": round(float(d), 4),
            "item_ci": boot_item(b, i, y),
            "question_clustered_ci": boot_cluster(b, i, y, g),
            "indexed_ci_clustered": boot_cluster_single(i, y, g)}


def main():
    cell = jload(R82 / "cf_cell.json")
    items = cell["items"]
    ind = cell["meta"]["individuation"]
    idx = jload(R82 / "cf_indexes.json")["indexes"]
    qmap = {}
    for n, q in enumerate(sorted({it["question"] for it in items})):
        qmap[q] = f"q{n:02d}"

    y = np.array([it["y_nok"] for it in items], int)
    g = np.array([it["pair_id"] for it in items])
    qs = [it["question"] for it in items]

    res = {"meta": {"n": len(items), "pos": int(y.sum()), "tol": TOL,
                    "blind_is_half_by_construction": True}, "lanes": {}, "baselines": {},
           "predictions": {}}

    # ---------------------------------------------------------------- monitors
    for code, model in LANES.items():
        lane = load_lane(code)
        if not lane:
            continue
        row = {}
        b = np.array([lane.get((qmap[it["question"]], "BLIND"), np.nan) for it in items])
        if np.isnan(b).any():
            print(f"{code}: blind incomplete, skipping")
            continue
        for arm, tag in (("INDEXED-V2", "v2"), ("INDEXED-V3", "v3")):
            i = np.array([lane.get((it["item_id"], arm), np.nan) for it in items])
            if np.isnan(i).any():
                continue
            row[tag] = summarise(b, i, y, g, f"{model} {tag} NOK, all 90")
            # per-state, descriptive
            row[tag]["per_state"] = {}
            for st in ("SUPERSESSION", "RETRACTION", "EXPIRY"):
                m = np.array([it["state"] == st for it in items])
                row[tag]["per_state"][st] = {
                    "n": int(m.sum()), "pos": int(y[m].sum()),
                    "blind": round(float(auroc(b[m], y[m])), 4),
                    "indexed": round(float(auroc(i[m], y[m])), 4)}
        res["lanes"][model] = row

        # ---- CF-3: pooled counted-state, individuating pairs only, paired v3 - v2
        if "v2" in row and "v3" in row:
            keep = np.array([it["state"] != "SUPERSESSION"
                             and ind[it["pair_id"]]["individuates"] for it in items])
            i2 = np.array([lane[(it["item_id"], "INDEXED-V2")] for it in items])
            i3 = np.array([lane[(it["item_id"], "INDEXED-V3")] for it in items])
            res["lanes"][model]["cf3_counted"] = {
                "n_items": int(keep.sum()), "pos": int(y[keep].sum()),
                "pairs": int(keep.sum() // 3),
                "v2": round(float(auroc(i2[keep], y[keep])), 4),
                "v3": round(float(auroc(i3[keep], y[keep])), 4),
                "delta_v3_minus_v2": round(float(auroc(i3[keep], y[keep])
                                                 - auroc(i2[keep], y[keep])), 4),
                "item_ci": boot_item(i2[keep], i3[keep], y[keep]),
                "question_clustered_ci": boot_cluster(i2[keep], i3[keep], y[keep],
                                                      g[keep])}

    # ---------------------------------------------------------------- baselines
    sup2 = [named_sections(idx[it["item_id"]]["v2"])["superseded"] for it in items]
    s3 = [named_sections(idx[it["item_id"]]["v3"]) for it in items]
    all3 = [s["superseded"] + s["retracted"] + s["expired"] for s in s3]
    whole = [sorted({n for lst in parse_index(idx[it["item_id"]]["v2"])["attr_by_cat"]
                     .values() for n in lst}) for it in items]
    for name, lists in (("NB6-superseded-names-v2", sup2),
                        ("all-states-names-v3", all3),
                        ("NB5-whole-map-v2", whole)):
        s = matcher(qs, lists)
        res["baselines"][name] = {
            "auroc": round(float(auroc(s, y)), 4),
            "clustered_ci": boot_cluster_single(s, y, g)}
    res["baselines"]["_scores_cached"] = False

    jdump = lambda o, p: (pathlib.Path(p).parent.mkdir(parents=True, exist_ok=True),
                          io.open(p, "w", encoding="utf-8", newline="\n").write(
                              json.dumps(o, ensure_ascii=False, indent=2, sort_keys=True,
                                         default=float) + "\n"))
    jdump(res, OUT)

    # ---------------------------------------------------------------- report
    print("=" * 78)
    print(f"R82-CF  n={len(items)}  PN positives={int(y.sum())}  tolerance +/-{TOL}")
    print("=" * 78)
    for model, row in res["lanes"].items():
        print(f"\n{model}")
        for tag in ("v2", "v3"):
            if tag not in row:
                continue
            r = row[tag]
            ci, cc = r["item_ci"], r["question_clustered_ci"]
            print(f"  {tag}: blind {r['blind']:.4f}  indexed {r['indexed']:.4f}  "
                  f"delta {r['delta']:+.4f}  item [{ci['ci_lo']:+.4f},{ci['ci_hi']:+.4f}]"
                  f"{'*' if ci['excludes_zero'] else ''}  "
                  f"qclust [{cc['ci_lo']:+.4f},{cc['ci_hi']:+.4f}]"
                  f"{'*' if cc['excludes_zero'] else ''}")
            ps = r["per_state"]
            print("      per state (descriptive): " + "  ".join(
                f"{k[:4]} {v['indexed']:.4f}" for k, v in ps.items()))
        if "cf3_counted" in row:
            c = row["cf3_counted"]
            ci = c["question_clustered_ci"]
            print(f"  CF-3 counted-state, {c['pairs']} pairs / {c['n_items']} items: "
                  f"v2 {c['v2']:.4f} -> v3 {c['v3']:.4f}  "
                  f"delta {c['delta_v3_minus_v2']:+.4f}  "
                  f"qclust [{ci['ci_lo']:+.4f},{ci['ci_hi']:+.4f}]"
                  f"{'*' if ci['excludes_zero'] else ''}")
    print("\nbaselines (NOK, all 90):")
    for k, v in res["baselines"].items():
        if k.startswith("_"):
            continue
        print(f"  {k:28s} {v['auroc']:.4f}  clustered "
              f"[{v['clustered_ci']['ci_lo']:.4f},{v['clustered_ci']['ci_hi']:.4f}]")
    print(f"\n-> {OUT}")


if __name__ == "__main__":
    main()
