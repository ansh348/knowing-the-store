"""E1-R sub-step (b): non-LLM baselines over the SAME committed serialized indexes.

Reviewer B1: can the paper distinguish "LLM metamemory" from "metadata makes
classification easier"? Answerable only by running non-LLM readers over the identical
index strings the monitor saw.

NB-1 deterministic lifecycle rule       unsupervised
NB-2 logistic over index features       supervised, persona-grouped 5-fold OOF
NB-3 TF-IDF over index text + question  supervised, persona-grouped 5-fold OOF
NB-4 lexical query-index match          unsupervised
NB-5 embedding query-index match        unsupervised, local encoder, offline

Every baseline is run on the TRUE and the BELIEVED index for every population.
"""
from __future__ import annotations

import os
import sys

import numpy as np

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from sklearn.feature_extraction.text import TfidfVectorizer          # noqa: E402
from sklearn.linear_model import LogisticRegression                  # noqa: E402
from sklearn.model_selection import GroupKFold                       # noqa: E402
from sklearn.pipeline import make_pipeline                           # noqa: E402
from sklearn.preprocessing import StandardScaler                     # noqa: E402

from common_e1r import (OUT, POPULATIONS, assemble, auroc, boot_item, jdump,  # noqa: E402
                        load_e1)
from index_features import features, indexes, index_key, parse, toks  # noqa: E402

TOL = 0.05          # inherited from the count-destruction probe; "matches" tolerance
FOLDS = 5
SEED = 42
_ENC = {}


def encoder():
    if "m" not in _ENC:
        from sentence_transformers import SentenceTransformer
        _ENC["m"] = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2",
                                        device="cpu")
    return _ENC["m"]


def jac(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0.0


def build(items, blind, indexed, judgment, provenance):
    """Assemble labels, monitor scores, and every baseline score for one population."""
    rows = []
    for it in items:
        q, tag = it["question"], it["item_id"]
        if q not in blind or tag not in indexed:
            continue
        bv, iv = blind[q].get(judgment), indexed[tag].get(judgment)
        if bv is None or iv is None:
            continue
        lab = it.get("label", it["label_pre"])
        y = (0 if lab == "ABSENT" else 1) if judgment == "fok" \
            else (1 if lab == "PRESENT-NEGATIVE" else 0)
        f, fok_rule, nok_rule, p, txt = features(it, provenance, q)
        attrs = [a for v in p["attr_by_cat"].values() for a in v]
        qt = toks(q)
        lex = max((jac(qt, toks(a.replace("_", " "))) for a in attrs), default=0.0)
        rows.append({
            "y": y, "persona": it["persona"], "item_id": tag,
            "monitor": iv, "monitor_blind": bv,
            "nb1": fok_rule if judgment == "fok" else nok_rule,
            "nb4": lex,
            "feat": f, "text": (txt or "") + "\n\nQUESTION: " + q,
            "question": q, "attrs": attrs,
        })
    return rows


def supervised(X, y, g, name):
    """Persona-grouped 5-fold out-of-fold predictions, pooled, then one AUROC."""
    y = np.asarray(y, int)
    g = np.asarray(g)
    oof = np.zeros(len(y), float)
    n_groups = len(set(g.tolist()))
    folds = min(FOLDS, n_groups)
    gkf = GroupKFold(n_splits=folds)
    for tr, te in gkf.split(X, y, groups=g):
        if len(set(y[tr].tolist())) < 2:
            oof[te] = 0.5
            continue
        if name == "nb3":
            mdl = make_pipeline(
                TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True),
                LogisticRegression(C=1.0, max_iter=2000, random_state=SEED))
            mdl.fit([X[i] for i in tr], y[tr])
            oof[te] = mdl.predict_proba([X[i] for i in te])[:, 1]
        else:
            mdl = make_pipeline(
                StandardScaler(),
                LogisticRegression(C=1.0, max_iter=2000, random_state=SEED))
            mdl.fit(X[tr], y[tr])
            oof[te] = mdl.predict_proba(X[te])[:, 1]
    return oof


def embed_scores(rows):
    """NB-5: max cosine(question, attribute-name) using a local offline encoder."""
    enc = encoder()
    uniq_q = sorted({r["question"] for r in rows})
    uniq_a = sorted({a for r in rows for a in r["attrs"]})
    if not uniq_a:
        return [0.0] * len(rows)
    qv = enc.encode(uniq_q, normalize_embeddings=True, batch_size=128,
                    show_progress_bar=False)
    av = enc.encode([a.replace("_", " ") for a in uniq_a], normalize_embeddings=True,
                    batch_size=256, show_progress_bar=False)
    qi = {q: k for k, q in enumerate(uniq_q)}
    ai = {a: k for k, a in enumerate(uniq_a)}
    out = []
    for r in rows:
        if not r["attrs"]:
            out.append(0.0)
            continue
        idx = [ai[a] for a in r["attrs"]]
        out.append(float(np.max(av[idx] @ qv[qi[r["question"]]])))
    return out


def main():
    items, blind, idxT, idxB = load_e1()
    results = {}

    for rid, spec in POPULATIONS.items():
        if rid == "R-FOK-EASY":
            continue
        sub = [it for it in items if spec["filt"](it)]
        for prov, idx in (("TRUE", idxT), ("BELIEVED", idxB)):
            rows = build(sub, blind, idx, spec["judgment"], prov)
            if not rows or len(set(r["y"] for r in rows)) < 2:
                continue
            y = np.array([r["y"] for r in rows], int)
            g = np.array([r["persona"] for r in rows])
            keys = sorted(rows[0]["feat"].keys())
            Xn = np.array([[r["feat"][k] for k in keys] for r in rows], float)
            Xt = [r["text"] for r in rows]

            mon = auroc([r["monitor"] for r in rows], y)
            blind_a = auroc([r["monitor_blind"] for r in rows], y)
            scores = {
                "NB-1 deterministic rule": auroc([r["nb1"] for r in rows], y),
                "NB-2 logistic/index feats": auroc(supervised(Xn, y, g, "nb2"), y),
                "NB-3 TF-IDF/index text": auroc(supervised(Xt, y, g, "nb3"), y),
                "NB-4 lexical match": auroc([r["nb4"] for r in rows], y),
                "NB-5 embedding match": auroc(embed_scores(rows), y),
            }
            best_name = max(scores, key=lambda k: scores[k])
            results[f"{rid}|{prov}"] = {
                "row": rid, "provenance": prov, "judgment": spec["judgment"],
                "n": len(rows), "n_pos": int(y.sum()),
                "monitor_indexed_auroc": float(mon),
                "monitor_blind_auroc": float(blind_a),
                "baselines": {k: float(v) for k, v in scores.items()},
                "best_baseline": best_name,
                "best_baseline_auroc": float(scores[best_name]),
                "monitor_minus_best": float(mon - scores[best_name]),
                "baseline_matches_monitor": bool(abs(mon - scores[best_name]) < TOL),
                "baseline_beats_monitor": bool(scores[best_name] > mon + TOL),
            }
            print(f"  scored {rid:12s} {prov:9s} n={len(rows):4d} "
                  f"monitor={mon:.4f} best={best_name.split()[0]}={scores[best_name]:.4f}")

    jdump({"rows": results, "tolerance": TOL,
           "encoder": "sentence-transformers/all-MiniLM-L6-v2 (local, offline)",
           "spec": "e1r_robustness/SPEC_E1R.md @ 9ac91a2"}, OUT / "baselines.json")

    print()
    print("=" * 112)
    print("E1-R (b)  NON-LLM BASELINES OVER THE SAME COMMITTED SERIALIZED INDEXES")
    print("=" * 112)
    hdr = (f"{'population':13s} {'prov':9s} {'n':>4s} {'monitor':>8s} {'NB-1':>7s} "
           f"{'NB-2':>7s} {'NB-3':>7s} {'NB-4':>7s} {'NB-5':>7s} {'best':>7s} {'mon-best':>9s}")
    print(hdr)
    print("-" * len(hdr))
    for k, r in results.items():
        b = r["baselines"]
        v = [b["NB-1 deterministic rule"], b["NB-2 logistic/index feats"],
             b["NB-3 TF-IDF/index text"], b["NB-4 lexical match"],
             b["NB-5 embedding match"]]
        mark = ""
        if r["baseline_beats_monitor"]:
            mark = "  <-- BASELINE WINS"
        elif r["baseline_matches_monitor"]:
            mark = "  <-- matches"
        print(f"{r['row']:13s} {r['provenance']:9s} {r['n']:4d} "
              f"{r['monitor_indexed_auroc']:8.4f} " + " ".join(f"{x:7.4f}" for x in v) +
              f" {r['best_baseline_auroc']:7.4f} {r['monitor_minus_best']:+9.4f}{mark}")
    print(f"\nwrote {OUT / 'baselines.json'}")


if __name__ == "__main__":
    main()