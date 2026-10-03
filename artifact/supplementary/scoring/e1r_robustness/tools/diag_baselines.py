"""Diagnostic for E1-R sub-step (b): is NB-3 reading the index, or the question?

NB-3 scored 0.9625 on Mem0 and 0.9512 on A-MEM -- backends whose indexes declare almost
every field "not expressible by this backend". A text classifier cannot read structure that
is not there, so either the index text leaks backend identity or the concatenated QUESTION
is carrying the signal. E1-QP already established that these questions carry
generator-specific template signal (supervised TF-IDF 0.9199 on the hard row).

Ablation: NB-3 is refit three ways -- index+question (as run), index only, question only.
Also reports whether the unsupervised matchers are separating backends rather than stores.
"""
from __future__ import annotations

import os

import numpy as np

os.environ.setdefault("HF_HUB_OFFLINE", "1")

from sklearn.feature_extraction.text import TfidfVectorizer      # noqa: E402
from sklearn.linear_model import LogisticRegression              # noqa: E402
from sklearn.model_selection import GroupKFold                   # noqa: E402
from sklearn.pipeline import make_pipeline                       # noqa: E402

from common_e1r import OUT, POPULATIONS, auroc, jdump, load_e1   # noqa: E402
from index_features import features                              # noqa: E402

SEED, FOLDS = 42, 5


def oof_text(texts, y, g):
    y = np.asarray(y, int)
    g = np.asarray(g)
    out = np.zeros(len(y), float)
    folds = min(FOLDS, len(set(g.tolist())))
    for tr, te in GroupKFold(n_splits=folds).split(texts, y, groups=g):
        if len(set(y[tr].tolist())) < 2:
            out[te] = 0.5
            continue
        m = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True),
                          LogisticRegression(C=1.0, max_iter=2000, random_state=SEED))
        m.fit([texts[i] for i in tr], y[tr])
        out[te] = m.predict_proba([texts[i] for i in te])[:, 1]
    return out


def main():
    items, blind, idxT, idxB = load_e1()
    res = {}
    for rid, spec in POPULATIONS.items():
        if rid == "R-FOK-EASY":
            continue
        sub = [it for it in items if spec["filt"](it)]
        for prov, idx in (("TRUE", idxT), ("BELIEVED", idxB)):
            ys, gs, qs, xs, bks = [], [], [], [], []
            for it in sub:
                q, tag = it["question"], it["item_id"]
                if q not in blind or tag not in idx:
                    continue
                if blind[q].get(spec["judgment"]) is None or \
                        idx[tag].get(spec["judgment"]) is None:
                    continue
                lab = it.get("label", it["label_pre"])
                ys.append((0 if lab == "ABSENT" else 1) if spec["judgment"] == "fok"
                          else (1 if lab == "PRESENT-NEGATIVE" else 0))
                gs.append(it["persona"])
                qs.append(q)
                _, _, _, _, txt = features(it, prov, q)
                xs.append(txt or "")
                bks.append(it["backend"])
            if len(set(ys)) < 2:
                continue
            y = np.array(ys, int)
            both = [x + "\n\nQUESTION: " + q for x, q in zip(xs, qs)]
            a_both = auroc(oof_text(both, y, gs), y)
            a_idx = auroc(oof_text(xs, y, gs), y)
            a_q = auroc(oof_text(qs, y, gs), y)
            # does backend identity alone separate this population?
            bmap = {b: k for k, b in enumerate(sorted(set(bks)))}
            a_backend = (auroc([bmap[b] for b in bks], y)
                         if len(bmap) > 1 else float("nan"))
            res[f"{rid}|{prov}"] = {
                "n": len(y), "n_pos": int(y.sum()),
                "nb3_index_plus_question": float(a_both),
                "nb3_index_only": float(a_idx),
                "nb3_question_only": float(a_q),
                "backend_identity_auroc": float(a_backend),
                "n_backends": len(bmap),
                "question_carries_it": bool(a_q >= a_both - 0.02),
            }
            print(f"{rid:12s} {prov:9s} n={len(y):4d}  both={a_both:.4f}  "
                  f"index-only={a_idx:.4f}  question-only={a_q:.4f}  "
                  f"backend-id={a_backend:.4f}")
    jdump(res, OUT / "baselines_diagnostic.json")
    print(f"\nwrote {OUT / 'baselines_diagnostic.json'}")


if __name__ == "__main__":
    main()