"""probes.py -- E1-QP (a)(i) TF-IDF probe and (a)(ii) LLM text-only classifier.

Per PREREG_E1QP.md (f4dafdd…) sections 2-3. QUESTION STRINGS ONLY: no store, no
index, no persona feature, no metadata. Persona is used ONLY as the CV grouping
key, never as an input feature -- that is what makes this a prior probe rather
than a memorisation probe.

    python probes.py tfidf
    python probes.py llm [--limit N]
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "e1_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "e1xv_crossvendor" / "tools"))

from qp_common import QP, population, matched_slice, strict_slice  # noqa: E402
from score_e1 import auroc  # noqa: E402  committed estimator
from score_ladder import auroc_ci  # noqa: E402

RES = QP / "results"

# ---- frozen probe configuration, PREREG section 2 --------------------------- #
TFIDF = dict(lowercase=True, ngram_range=(1, 2), min_df=1, sublinear_tf=True)
LOGREG = dict(C=1.0, max_iter=2000, class_weight="balanced", solver="lbfgs")
NSPLITS, SEED = 5, 42

# ---- frozen prompt, PREREG section 3, verbatim ------------------------------ #
LLM_MODEL = "gpt-4.1-mini"
LLM_SYSTEM = """\
You are shown a single question that a user asked their assistant. You are shown \
nothing else -- no memory store, no index, no context.

Judge only this: how likely is it that, if an assistant had a memory store for this \
user, that store would contain content on this topic that is now STALE -- superseded \
by a later value, retracted, or past its date -- so that surfacing it would mislead?

Respond with a single JSON object and nothing else:
{"pn_likelihood": <0-100>}\
"""
LLM_USER = "Question: {question}"


def oof_tfidf(rows, target):
    """Pooled out-of-fold predictions, persona-grouped CV. Returns (pred, y)."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedGroupKFold

    X = [r["question"] for r in rows]
    y = np.array([r[target] for r in rows])
    g = np.array([r["persona"] for r in rows])
    pred = np.full(len(y), np.nan)
    n = min(NSPLITS, len(set(g)), int(y.sum()), int((1 - y).sum()))
    if n < 2:
        return None, y, 0
    cv = StratifiedGroupKFold(n_splits=n, shuffle=True, random_state=SEED)
    for tr, te in cv.split(X, y, groups=g):
        if len(set(y[tr])) < 2:
            continue
        v = TfidfVectorizer(**TFIDF)
        Xtr = v.fit_transform([X[i] for i in tr])
        clf = LogisticRegression(**LOGREG).fit(Xtr, y[tr])
        pred[te] = clf.predict_proba(v.transform([X[i] for i in te]))[:, 1]
    keep = ~np.isnan(pred)
    return pred[keep], y[keep], n


def cmd_tfidf():
    out = {"config": {"tfidf": TFIDF, "logreg": LOGREG, "n_splits": NSPLITS,
                      "seed": SEED, "grouped_by": "persona"}, "probes": {}}
    jobs = []
    for pn, pop in (("P1", population("P1")), ("P2", population("P2"))):
        jobs.append((f"{pn}:full:PN-vs-rest", pop, "y_nok"))
        jobs.append((f"{pn}:full:nonABSENT-vs-ABSENT", pop, "y_fok"))
        jobs.append((f"{pn}:matched:PN-vs-slotablated", matched_slice(pop), "y_nok"))
        jobs.append((f"{pn}:strict-slotablated:PN-vs-rest", strict_slice(pop), "y_nok"))

    print(f"{'probe':44s} {'n':>4s} {'pos':>4s} {'AUROC':>8s}  95% CI          includes 0.50")
    for name, rows, target in jobs:
        pred, y, nsp = oof_tfidf(rows, target)
        if pred is None or len(set(y)) < 2:
            out["probes"][name] = {"n": len(rows), "note": "not computable"}
            print(f"{name:44s} {len(rows):4d}    -        -   not computable")
            continue
        a = auroc(pred, y)
        ci = auroc_ci(pred, y)
        out["probes"][name] = {"n": int(len(y)), "n_pos": int(y.sum()), "auroc": a,
                               "ci": [ci["ci_lo"], ci["ci_hi"]],
                               "includes_0.50": ci["includes_0.50"], "n_splits": nsp}
        print(f"{name:44s} {len(y):4d} {int(y.sum()):4d} {a:8.4f}  "
              f"[{ci['ci_lo']:.4f}, {ci['ci_hi']:.4f}]  {ci['includes_0.50']}")

    RES.mkdir(parents=True, exist_ok=True)
    io.open(RES / "probe_tfidf.json", "w", encoding="utf-8").write(
        json.dumps(out, indent=2))
    print(f"\nwritten: results/probe_tfidf.json")


def cmd_llm(limit=None):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "e1xv_crossvendor" / "tools"))
    from lane_probe import load_env
    from openai import OpenAI
    load_env()
    c = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    seen = {}
    p = RES / "probe_llm_raw.jsonl"
    if p.exists():
        for ln in io.open(p, encoding="utf-8"):
            if ln.strip():
                r = json.loads(ln)
                seen[r["item_id"]] = r

    pop = {r["item_id"]: r for r in population("P2")}
    pop.update({r["item_id"]: r for r in population("P1")})   # union, dedup by id
    todo = [r for k, r in sorted(pop.items()) if k not in seen]
    if limit:
        todo = todo[:limit]
    print(f"LLM probe: {len(pop)} items in the union, {len(seen)} cached, "
          f"{len(todo)} to call")

    RES.mkdir(parents=True, exist_ok=True)
    fh = io.open(p, "a", encoding="utf-8", newline="\n")
    usd = 0.0
    for n, r in enumerate(todo, 1):
        try:
            resp = c.chat.completions.create(
                model=LLM_MODEL, temperature=0, max_tokens=16,
                messages=[{"role": "system", "content": LLM_SYSTEM},
                          {"role": "user", "content": LLM_USER.format(question=r["question"])}])
            txt = resp.choices[0].message.content or ""
            u = resp.usage
            usd += (u.prompt_tokens * 0.40 + u.completion_tokens * 1.60) / 1e6
            try:
                v = float(json.loads(txt[txt.find("{"):txt.rfind("}") + 1])["pn_likelihood"])
                v = min(100.0, max(0.0, v)) / 100.0
            except Exception:                                  # noqa: BLE001
                v = None
            row = {"item_id": r["item_id"], "pn_likelihood": v, "text": txt,
                   "served": resp.model, "in": u.prompt_tokens, "out": u.completion_tokens}
        except Exception as e:                                 # noqa: BLE001
            row = {"item_id": r["item_id"], "pn_likelihood": None,
                   "error": f"{type(e).__name__}:{str(e)[:160]}"}
        fh.write(json.dumps(row, ensure_ascii=False) + "\n"); fh.flush()
        if n % 50 == 0:
            print(f"  {n}/{len(todo)}  ${usd:.4f}", flush=True)
        if usd > 2.00:
            fh.close()
            raise SystemExit(f"CAP ABORT at ${usd:.2f}")
    fh.close()
    print(f"  {len(todo)} calls, ${usd:.4f}")

    # score
    vals = {}
    for ln in io.open(p, encoding="utf-8"):
        if ln.strip():
            r = json.loads(ln)
            vals[r["item_id"]] = r.get("pn_likelihood")
    out = {"model": LLM_MODEL, "prompt_system": LLM_SYSTEM, "prompt_user": LLM_USER,
           "n_called": len(vals), "usd_this_run": round(usd, 4),
           "n_unparsed": sum(1 for v in vals.values() if v is None), "probes": {}}
    print(f"\n{'probe':44s} {'n':>4s} {'pos':>4s} {'AUROC':>8s}  95% CI          includes 0.50")
    for pn in ("P1", "P2"):
        base = population(pn)
        for nm, rows in (("full", base), ("matched", matched_slice(base)),
                         ("strict-slotablated", strict_slice(base))):
            for target in ("y_nok", "y_fok"):
                rs = [r for r in rows if vals.get(r["item_id"]) is not None]
                y = np.array([r[target] for r in rs])
                s = np.array([vals[r["item_id"]] for r in rs])
                key = f"{pn}:{nm}:{target}"
                if len(set(y)) < 2:
                    out["probes"][key] = {"n": len(rs), "note": "single-class"}
                    continue
                a, ci = auroc(s, y), auroc_ci(s, y)
                out["probes"][key] = {"n": len(rs), "n_pos": int(y.sum()), "auroc": a,
                                      "ci": [ci["ci_lo"], ci["ci_hi"]],
                                      "includes_0.50": ci["includes_0.50"]}
                print(f"{key:44s} {len(rs):4d} {int(y.sum()):4d} {a:8.4f}  "
                      f"[{ci['ci_lo']:.4f}, {ci['ci_hi']:.4f}]  {ci['includes_0.50']}")
    io.open(RES / "probe_llm.json", "w", encoding="utf-8").write(json.dumps(out, indent=2))
    print(f"\nwritten: results/probe_llm.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["tfidf", "llm"])
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    cmd_tfidf() if a.cmd == "tfidf" else cmd_llm(a.limit)
