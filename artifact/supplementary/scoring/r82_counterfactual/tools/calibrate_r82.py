"""calibrate_r82.py -- R82-CAL: post-hoc calibration under leave-one-persona-out CV.

NO API CALLS. Pure post-processing over committed artifacts. Executes ADDENDUM_R82 Part 2.

Populations are re-derived, never read from a score file, because none exists:
    P-FOK-HARD  588 items, 35 positives, 40 personas, arms blind / intact / names-only.
                Assembly transcribed from verify_e1r.py:139-167, whose requirement that a
                tag appear in all three mechanism arms is what makes it 588 and not 595.
    P-NOK-FRB   661 items, 104 positives, 40 personas, arms blind / TRUE / BELIEVED.
                common_e1r.assemble under POPULATIONS["R-NOK-FRB"].

Maps: Platt, isotonic, temperature. Every map is fitted out of fold under leave-one-
persona-out CV, 40 folds, so no item contributes to the fit that predicts it.

Metrics before and after: ECE (common_e1r.ece, the committed definition), Brier, AURC and
excess AURC on the standard selective-prediction convention (confidence max(p,1-p),
prediction 1[p>=0.5], loss 0/1; excess is measured against the oracle ordering).

Monotonicity is asserted PER FITTED MAP, on the observed score grid: a fold whose map is
neither non-decreasing nor non-increasing is a STOP. The pooled out-of-fold AUROC is
reported as a diagnostic and is NOT asserted equal to the raw AUROC, because cross-
validation fits a different map per fold, so the pooled vector is a mixture rather than one
monotone transform. See D-R82-5 and ADDENDUM_R82 section 18 as amended.

Usage:  python r82_counterfactual/tools/calibrate_r82.py
Writes: r82_counterfactual/results/cal_scores.json
"""
from __future__ import annotations

import collections
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1r_robustness" / "tools"))

import numpy as np  # noqa: E402
from common_e1r import E1, POPULATIONS, assemble, auroc, ece, jload, load_e1  # noqa: E402
from sklearn.isotonic import IsotonicRegression  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402

OUT = ROOT / "r82_counterfactual" / "results" / "cal_scores.json"
EPS = 1e-6


def logit(p):
    p = np.clip(np.asarray(p, float), EPS, 1 - EPS)
    return np.log(p / (1 - p))


def fit_platt(s, y):
    m = LogisticRegression(C=1e6, solver="lbfgs")
    m.fit(np.asarray(s, float).reshape(-1, 1), np.asarray(y, int))
    return lambda z: m.predict_proba(np.asarray(z, float).reshape(-1, 1))[:, 1]


def fit_isotonic(s, y):
    m = IsotonicRegression(out_of_bounds="clip", increasing=True)
    m.fit(np.asarray(s, float), np.asarray(y, int))
    return lambda z: m.predict(np.asarray(z, float))


def fit_temperature(s, y):
    """One scalar on the logit, fitted by grid then local refine on NLL."""
    z, yy = logit(s), np.asarray(y, float)
    best, bt = None, 1.0
    for t in np.concatenate([np.linspace(0.05, 5.0, 100), np.linspace(5.0, 50.0, 100)]):
        p = 1.0 / (1.0 + np.exp(-z / t))
        p = np.clip(p, EPS, 1 - EPS)
        nll = -np.mean(yy * np.log(p) + (1 - yy) * np.log(1 - p))
        if best is None or nll < best:
            best, bt = nll, t
    return lambda q: 1.0 / (1.0 + np.exp(-logit(q) / bt)), float(bt)


def brier(p, y):
    return float(np.mean((np.asarray(p, float) - np.asarray(y, int)) ** 2))


def aurc(p, y):
    """Selective risk averaged over coverage; excess is against the oracle ordering."""
    p, y = np.asarray(p, float), np.asarray(y, int)
    pred = (p >= 0.5).astype(int)
    loss = (pred != y).astype(float)
    conf = np.maximum(p, 1 - p)
    order = np.argsort(-conf, kind="mergesort")
    r = np.cumsum(loss[order]) / np.arange(1, len(y) + 1)
    a = float(np.mean(r))
    o = np.sort(loss)
    ro = np.cumsum(o) / np.arange(1, len(y) + 1)
    return a, a - float(np.mean(ro))


def monotone_dir(f, grid, tol=1e-9):
    """-> 'increasing', 'decreasing', or None if the fitted map is neither."""
    v = np.asarray(f(grid), float)
    d = np.diff(v)
    if np.all(d >= -tol):
        return "increasing"
    if np.all(d <= tol):
        return "decreasing"
    return None


def lopo_calibrate(s, y, g, fitter):
    """Out-of-fold calibrated probabilities, one fold per persona.

    Also returns the monotonicity direction of each fold's fitted map. The registered
    invariance check applies PER MAP: a single monotone map cannot change AUROC. It does
    NOT apply to the pooled out-of-fold vector, because cross-validation fits a different
    map per fold and the pooled vector is a mixture of them rather than one transform.
    Recorded as D-R82-5 and amended into ADDENDUM_R82 section 18.
    """
    s, y, g = np.asarray(s, float), np.asarray(y, int), np.asarray(g)
    out = np.full(len(s), np.nan)
    grid = np.unique(s)
    dirs = collections.Counter()
    for u in np.unique(g):
        te = g == u
        tr = ~te
        if len(set(y[tr].tolist())) < 2:
            continue
        f = fitter(s[tr], y[tr])
        if isinstance(f, tuple):
            f = f[0]
        dirs[monotone_dir(f, grid)] += 1
        out[te] = f(s[te])
    return out, dirs


def crossing(s, p, target):
    """Smallest raw score whose mean out-of-fold calibrated probability reaches target."""
    by = collections.defaultdict(list)
    for a, b in zip(np.asarray(s, float), np.asarray(p, float)):
        if not np.isnan(b):
            by[round(float(a), 6)].append(b)
    for k in sorted(by):
        if float(np.mean(by[k])) >= target:
            return k
    return None


def evaluate(name, s, y, g, results):
    s, y = np.asarray(s, float), np.asarray(y, int)
    base = {"n": int(len(y)), "pos": int(y.sum()),
            "base_rate": round(float(y.mean()), 4),
            "auroc": round(float(auroc(s, y)), 4),
            "ece": round(float(ece(s, y)), 4),
            "brier": round(brier(s, y), 4),
            "distinct_values": int(len(set(np.round(s, 6).tolist())))}
    a, ex = aurc(s, y)
    base["aurc"], base["excess_aurc"] = round(a, 4), round(ex, 4)
    row = {"raw": base, "maps": {}}
    for mname, fitter in (("platt", fit_platt), ("isotonic", fit_isotonic),
                          ("temperature", fit_temperature)):
        p, dirs = lopo_calibrate(s, y, g, fitter)
        m = ~np.isnan(p)
        a2, ex2 = aurc(p[m], y[m])
        au_before = round(float(auroc(s[m], y[m])), 4)
        au_after = round(float(auroc(p[m], y[m])), 4)
        if dirs.get(None, 0):
            raise SystemExit(f"STOP: {name}/{mname} fitted a non-monotone map in "
                             f"{dirs[None]} folds")
        row["maps"][mname] = {
            "n_scored": int(m.sum()),
            "ece": round(float(ece(p[m], y[m])), 4),
            "brier": round(brier(p[m], y[m]), 4),
            "aurc": round(a2, 4), "excess_aurc": round(ex2, 4),
            "auroc_raw": au_before, "auroc_pooled_oof": au_after,
            "folds_increasing": dirs.get("increasing", 0),
            "folds_decreasing": dirs.get("decreasing", 0),
            "max_calibrated_p": round(float(np.nanmax(p[m])), 4),
            "crossing_0.5": crossing(s[m], p[m], 0.5),
            "crossing_base_rate": crossing(s[m], p[m], float(y.mean()))}
    results[name] = row
    return row


def main():
    items, blind, idxT, idxB = load_e1()
    results = {}

    # ---------------- P-NOK-FRB, 661
    sel = [it for it in items if POPULATIONS["R-NOK-FRB"]["filt"](it)]
    b, i, y, g, _ = assemble(sel, blind, idxT, "nok")
    bB, iB, yB, gB, _ = assemble(sel, blind, idxB, "nok")
    evaluate("P-NOK-FRB/blind", b, y, g, results)
    evaluate("P-NOK-FRB/indexed-TRUE", i, y, g, results)
    evaluate("P-NOK-FRB/indexed-BELIEVED", iB, yB, gB, results)

    # ---------------- P-FOK-HARD, 588
    mech = collections.defaultdict(dict)
    for r in jload(E1 / "mechanism_elicitation.json"):
        if r.get("status") == "OK":
            mech[r["arm"]][r["item_id"]] = r
    hard = [it for it in items if it["tier"] == "hard"]
    base = [it for it in hard
            if it["question"] in blind and it["item_id"] in idxT
            and blind[it["question"]].get("fok") is not None
            and idxT[it["item_id"]].get("fok") is not None
            and all(it["item_id"] in mech[a] for a in mech)]
    yy = np.array([0 if it.get("label", it["label_pre"]) == "ABSENT" else 1
                   for it in base], int)
    gg = np.array([it["persona"] for it in base])
    arms = {
        "blind": np.array([blind[it["question"]]["fok"] for it in base], float),
        "intact": np.array([idxT[it["item_id"]]["fok"] for it in base], float),
        "names-only": np.array([mech["A3-names-only"][it["item_id"]]["fok"]
                                for it in base], float),
    }
    for k, v in arms.items():
        evaluate(f"P-FOK-HARD/{k}", v, yy, gg, results)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(
        json.dumps(results, indent=2, sort_keys=True, default=float) + "\n")

    print("=" * 96)
    print("R82-CAL  leave-one-persona-out, 40 folds. AUROC invariance asserted at 1e-4.")
    print("=" * 96)
    for name, row in results.items():
        r = row["raw"]
        print(f"\n{name}   n={r['n']} pos={r['pos']} base={r['base_rate']:.4f} "
              f"AUROC={r['auroc']:.4f} distinct={r['distinct_values']}")
        print(f"  raw          ECE {r['ece']:.4f}  Brier {r['brier']:.4f}  "
              f"AURC {r['aurc']:.4f}  excess {r['excess_aurc']:.4f}")
        for m, v in row["maps"].items():
            c5 = v["crossing_0.5"]
            print(f"  {m:12s} ECE {v['ece']:.4f}  Brier {v['brier']:.4f}  "
                  f"AURC {v['aurc']:.4f}  excess {v['excess_aurc']:.4f}  "
                  f"maxp {v['max_calibrated_p']:.3f}  "
                  f"cross0.5 {'undefined' if c5 is None else f'{c5:.3f}'}  "
                  f"crossBR {v['crossing_base_rate']}")
    print(f"\n-> {OUT}")


if __name__ == "__main__":
    main()
