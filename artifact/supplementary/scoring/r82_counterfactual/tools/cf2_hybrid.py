# -*- coding: utf-8 -*-
"""cf2_hybrid.py -- E10 (registrations/ADDENDUM_CF2_HYBRID_READER.md; program R124, the author's ruling E1 of 2026-09-19): a no-model
hybrid reader on the 444-item counterfactual set, scored with the CF-2 conventions. Written before the freeze and hashed in it.

The reader (the registration's section 3, every choice fixed there): features per item f1 = the name lookup's score (the cosine of the
question to the superseded-names list of the superseded-only summary, cf2_reader_score.lookup_v2), f2 = the category-guessing share
(CR-nb1's quantity: assign_category on the question text, then the category's (superseded + retracted + expired) / entries, 0 when no
category is assigned), f3 = an indicator that a category was assigned. Model: sklearn LogisticRegression(C=1.0, penalty="l2",
solver="lbfgs", max_iter=1000) of y_nok on (1, f1, f2, f3) with f1 and f2 standardized by the training fold's mean and standard
deviation. Leave-persona-out over the 40 personas; the out-of-fold scores of all 444 items form the reader's vector. No other
hyperparameter, no other feature, no second fit.

Estimands (section 4): the whole-set and per-state AUROC with the persona-grouped interval; the paired difference against the name lookup,
against the category-guessing reader and against each of the five models (item-level and persona-grouped bootstrap, 1,000 draws, seed 42,
cf2_score.paired); PN versus PRESENT and W/T/L (the post-hoc block); the fold coefficients with their range. Gates before fitting: the
lookup 0.7663, CR-nb1 0.6623 (STOP on a mismatch). Predictions: P-H1 (hybrid minus lookup reliable, both intervals excluding zero),
P-H2 (GPT-5.6 Sol minus hybrid reliably positive). No model call; the embedding matcher runs locally.
Writes r82_counterfactual/cf2/results/cf_scores_hybrid.json. Usage: python r82_counterfactual/tools/cf2_hybrid.py
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[2]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "reviews/v19/tools", "reviews/v18/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402
import cf2_reader_score as R  # noqa: E402
from index_features import assign_category, parse  # noqa: E402
from common_e1r import auroc  # noqa: E402
from cf2_score import paired  # noqa: E402
import score_cf as S  # noqa: E402

CF2 = ROOT / "r82_counterfactual" / "cf2"
OUT = CF2 / "results" / "cf_scores_hybrid.json"
REG = ROOT / "registrations" / "ADDENDUM_CF2_HYBRID_READER.md"
GATE_LOOKUP, GATE_NB1 = 0.7663, 0.6623
LANES = [("MINI", "GPT-4.1 mini", "rows_MINI.jsonl", 0.7167), ("H45", "Haiku 4.5", "rows_H45.jsonl", 0.7566), ("OP5", "Opus 5", "rows_OP5.jsonl", 0.8405),
         ("SOL", "GPT-5.6 Sol", "rows_SOL.jsonl", 0.8500), ("LUNA", "GPT-5.6 Luna", "rows_LUNA.jsonl", 0.8417)]


def r4(x):
    return round(float(x), 4)


def nb1_share(text, question):
    p = parse(text)
    a_cat, _, _, _ = assign_category(p, question)
    c = p["categories"].get(a_cat) if a_cat else None
    if not c:
        return 0.0, 0.0
    cc = {k: int(c.get(k, 0) or 0) for k in ("entries", "suprsd", "retract", "expired")}
    return float(cc["suprsd"] + cc["retract"] + cc["expired"]) / max(1, cc["entries"]), 1.0


def main():
    items, idx = R.cell()
    y = np.array([it["y_nok"] for it in items], int); g = np.array([it["persona"] for it in items])
    f1 = R.lookup_v2(items, idx)                                                     # gate 0.7663 asserted inside
    f2 = np.zeros(len(items)); f3 = np.zeros(len(items))
    for k, it in enumerate(items):
        f2[k], f3[k] = nb1_share(idx[it["item_id"]]["v2"], it["question"])
    nb1 = r4(auroc(f2, y)); assert nb1 == GATE_NB1, ("GATE: CR-nb1", nb1, GATE_NB1)
    # leave-persona-out logistic regression
    v = np.full(len(items), np.nan); coefs = []
    for persona in sorted(set(g)):
        tr, te = g != persona, g == persona
        mu = np.array([f1[tr].mean(), f2[tr].mean()]); sd = np.array([f1[tr].std(), f2[tr].std()]); sd[sd == 0] = 1.0
        X = np.column_stack([(f1 - mu[0]) / sd[0], (f2 - mu[1]) / sd[1], f3])
        clf = LogisticRegression(C=1.0, penalty="l2", solver="lbfgs", max_iter=1000).fit(X[tr], y[tr])
        v[te] = clf.predict_proba(X[te])[:, 1]
        coefs.append({"persona": persona, "n_train": int(tr.sum()), "intercept": r4(clf.intercept_[0]), "f1_lookup": r4(clf.coef_[0][0]), "f2_share": r4(clf.coef_[0][1]), "f3_assigned": r4(clf.coef_[0][2])})
    assert not np.isnan(v).any()
    res = {"registration": REG.name, "registration_sha256": hashlib.sha256(REG.read_bytes()).hexdigest() if REG.exists() else None,
           "scorer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "gates": {"lookup_v2": GATE_LOOKUP, "nb1_v2": nb1},
           "features": {"f1": "name lookup cosine (lookup_v2)", "f2": "CR-nb1 share at the assigned category", "f3": "category assigned indicator", "f3_assigned_items": int(f3.sum())},
           "model": "LogisticRegression(C=1.0, penalty=l2, solver=lbfgs, max_iter=1000) on standardized f1, f2 and f3; leave-persona-out over 40 personas",
           "hybrid": R.score_vector(v, items, f1), "vs_nb1": paired(f2, v, y, g), "coefficients": coefs,
           "coefficient_range": {k: [r4(min(c[k] for c in coefs)), r4(max(c[k] for c in coefs))] for k in ("intercept", "f1_lookup", "f2_share", "f3_assigned")}}
    # the five models minus the hybrid (each model's recorded collapsed vector; the gates on their whole-set AUROC)
    res["models_minus_hybrid"] = {}
    for code, name, fn, gate in LANES:
        col, census = R.collapse(CF2 / "rows" / fn, "INDEXED-V2")
        m = np.array([col[it["item_id"]] for it in items], float)
        got = r4(auroc(m, y)); assert got == gate, ("GATE", name, got, gate)
        res["models_minus_hybrid"][code] = {"name": name, "model": got, "minus_hybrid": paired(v, m, y, g)}
    h = res["hybrid"]; vl = h["vs_lookup"]; sol = res["models_minus_hybrid"]["SOL"]["minus_hybrid"]
    p1 = bool(vl["delta"] > 0 and vl["item_ci"]["excludes_zero"] and vl["persona_ci"]["excludes_zero"])
    p2 = bool(sol["delta"] > 0 and sol["item_ci"]["excludes_zero"] and sol["persona_ci"]["excludes_zero"])
    res["predictions"] = {
        "P-H1": {"verdict": "HOLDS" if p1 else "FAILS", "hybrid": h["whole"], "lookup": GATE_LOOKUP, "delta": vl["delta"], "item_ci": vl["item_ci"], "persona_ci": vl["persona_ci"],
                 "text": ("P-H1 HOLDS: the hybrid reads {A} against the lookup's 0.7663, difference {D} with intervals {Ii} and {Ip}." if p1 else
                          "P-H1 FAILS: the hybrid reads {A} against the lookup's 0.7663, difference {D} with intervals {Ii} and {Ip}.").format(
                     A=f"{h['whole']:.4f}", D=f"{vl['delta']:+.4f}", Ii=f"[{vl['item_ci']['ci_lo']:+.4f}, {vl['item_ci']['ci_hi']:+.4f}]", Ip=f"[{vl['persona_ci']['ci_lo']:+.4f}, {vl['persona_ci']['ci_hi']:+.4f}]")},
        "P-H2": {"verdict": "HOLDS" if p2 else "FAILS", "sol_minus_hybrid": sol["delta"], "item_ci": sol["item_ci"], "persona_ci": sol["persona_ci"],
                 "text": ("P-H2 HOLDS: GPT-5.6 Sol minus the hybrid is {D} with intervals {Ii} and {Ip}, reliably positive." if p2 else
                          "P-H2 FAILS: GPT-5.6 Sol minus the hybrid is {D} with intervals {Ii} and {Ip}, not reliably positive.").format(
                     D=f"{sol['delta']:+.4f}", Ii=f"[{sol['item_ci']['ci_lo']:+.4f}, {sol['item_ci']['ci_hi']:+.4f}]", Ip=f"[{sol['persona_ci']['ci_lo']:+.4f}, {sol['persona_ci']['ci_hi']:+.4f}]")}}
    OUT.parent.mkdir(exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(res, indent=1, sort_keys=True, default=float))
    print(f"hybrid: whole {h['whole']:.4f} [{h['whole_ci_persona']['ci_lo']:.4f}, {h['whole_ci_persona']['ci_hi']:.4f}]; per state " + ", ".join(f"{s} {h['per_state'][s]['auroc']:.4f}" for s in R.STATES))
    print(f"  minus lookup {R.fmt_paired(vl)}   minus CR-nb1 {R.fmt_paired(res['vs_nb1'])}")
    for code, d in res["models_minus_hybrid"].items():
        print(f"  {d['name']:14s} {d['model']:.4f} minus hybrid {R.fmt_paired(d['minus_hybrid'])}")
    print("  coefficient ranges:", res["coefficient_range"])
    print(" ", res["predictions"]["P-H1"]["text"]); print(" ", res["predictions"]["P-H2"]["text"])
    print("->", OUT)


if __name__ == "__main__":
    main()
