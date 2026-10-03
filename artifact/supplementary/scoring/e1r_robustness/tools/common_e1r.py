"""Shared loaders and estimators for the E1-R robustness pass.

Frozen by e1r_robustness/SPEC_E1R.md (commit 9ac91a2). Estimators are transcribed from
e1_metamemory/tools/score_e1.py so that this pass cannot silently use a different AUROC or
ECE definition from the preregistered scorer.
"""
from __future__ import annotations

import io
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"
XV = ROOT / "e1xv_crossvendor"
OUT = ROOT / "e1r_robustness" / "results"

N_BOOT, BINS, SEED = 1000, 10, 42
SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True, default=float)
        f.write("\n")


# ---------------------------------------------------------------- estimators
def auroc(s, y):
    """Mann-Whitney rank AUROC, ties at 0.5. Transcribed from score_e1.py."""
    s, y = np.asarray(s, float), np.asarray(y, int)
    n1, n0 = int(y.sum()), int((1 - y).sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    o = np.argsort(s, kind="mergesort")
    r = np.empty(len(s), float)
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[o[j + 1]] == s[o[i]]:
            j += 1
        r[o[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def ece(p, y, bins=BINS):
    """10 equal-width bins, mass-weighted gap. Transcribed from score_e1.py."""
    p, y = np.asarray(p, float), np.asarray(y, int)
    if not len(p):
        return float("nan")
    e = np.linspace(0, 1, bins + 1)
    t = 0.0
    for b in range(bins):
        m = (p >= e[b]) & ((p < e[b + 1]) if b < bins - 1 else (p <= e[b + 1]))
        if m.sum():
            t += (m.sum() / len(p)) * abs(y[m].mean() - p[m].mean())
    return float(t)


def reliability(p, y, bins=BINS):
    p, y = np.asarray(p, float), np.asarray(y, int)
    e = np.linspace(0, 1, bins + 1)
    out = []
    for b in range(bins):
        m = (p >= e[b]) & ((p < e[b + 1]) if b < bins - 1 else (p <= e[b + 1]))
        out.append({
            "bin_lo": float(e[b]), "bin_hi": float(e[b + 1]),
            "n": int(m.sum()),
            "mean_pred": float(p[m].mean()) if m.sum() else None,
            "obs_freq": float(y[m].mean()) if m.sum() else None,
        })
    return out


# ---------------------------------------------------------------- bootstraps
def boot_item(b, i, y, n=N_BOOT, seed=SEED):
    """Preregistered item-level paired bootstrap (score_e1.py `boot`)."""
    rng = np.random.default_rng(seed)
    b, i, y = np.asarray(b), np.asarray(i), np.asarray(y)
    d = []
    for _ in range(n):
        k = rng.integers(0, len(y), len(y))
        if y[k].sum() in (0, len(k)):
            continue
        d.append(auroc(i[k], y[k]) - auroc(b[k], y[k]))
    return _summarise(d)


def boot_cluster(b, i, y, g, n=N_BOOT, seed=SEED):
    """Persona-clustered paired bootstrap, per SPEC_E1R (a).

    Draw n_clusters clusters with replacement; the resampled item multiset is the
    concatenation of all items in the drawn clusters. Both arms move together.
    """
    rng = np.random.default_rng(seed)
    b, i, y = np.asarray(b), np.asarray(i), np.asarray(y)
    g = np.asarray(g)
    groups = np.unique(g)
    idx_by_group = {u: np.flatnonzero(g == u) for u in groups}
    d = []
    for _ in range(n):
        drawn = rng.integers(0, len(groups), len(groups))
        k = np.concatenate([idx_by_group[groups[t]] for t in drawn])
        if y[k].sum() in (0, len(k)):
            continue
        d.append(auroc(i[k], y[k]) - auroc(b[k], y[k]))
    return _summarise(d)


def boot_cluster_single(s, y, g, n=N_BOOT, seed=SEED):
    """Clustered bootstrap for a single-arm AUROC (no pairing)."""
    rng = np.random.default_rng(seed)
    s, y, g = np.asarray(s, float), np.asarray(y, int), np.asarray(g)
    groups = np.unique(g)
    idx_by_group = {u: np.flatnonzero(g == u) for u in groups}
    d = []
    for _ in range(n):
        drawn = rng.integers(0, len(groups), len(groups))
        k = np.concatenate([idx_by_group[groups[t]] for t in drawn])
        if y[k].sum() in (0, len(k)):
            continue
        d.append(auroc(s[k], y[k]))
    return _summarise(d)


def _summarise(d):
    d = np.asarray(d, float)
    if not len(d):
        return {"n_draws": 0, "note": "all draws discarded as single-class"}
    lo, hi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    return {"n_draws": int(len(d)), "mean": float(d.mean()),
            "ci_lo": lo, "ci_hi": hi,
            "excludes_zero": bool(lo > 0 or hi < 0)}


def lopo(b, i, y, g):
    """Leave-one-persona-out deltas. Fragility diagnostic, not an interval."""
    b, i, y, g = np.asarray(b), np.asarray(i), np.asarray(y), np.asarray(g)
    full = auroc(i, y) - auroc(b, y)
    folds = []
    for u in np.unique(g):
        k = g != u
        if len(set(y[k].tolist())) < 2:
            continue
        folds.append({"persona": str(u), "n": int(k.sum()),
                      "delta": float(auroc(i[k], y[k]) - auroc(b[k], y[k]))})
    ds = [f["delta"] for f in folds]
    return {
        "full_delta": float(full),
        "n_folds": len(folds),
        "min_delta": float(min(ds)) if ds else None,
        "max_delta": float(max(ds)) if ds else None,
        "n_sign_changes": int(sum(1 for d in ds if (d > 0) != (full > 0))),
        "folds": folds,
    }


# ---------------------------------------------------------------- E1 loaders
def persona_of(item_id):
    return item_id.split(":")[1]


def load_e1():
    """Return (items, blind, idxT, idxB) exactly as score_e1.py joins them."""
    rows = jload(E1 / "elicitation_main.json")
    blind = {r["question"]: r for r in rows if r["arm"] == "BLIND" and r["status"] == "OK"}
    idxT = {r["tag"]: r for r in rows if r["arm"] == "INDEXED-TRUE" and r["status"] == "OK"}
    idxB = {r["tag"]: r for r in rows if r["arm"] == "INDEXED-BELIEVED" and r["status"] == "OK"}
    qmap = {r["tag"]: r["question"] for r in rows if r["arm"] != "BLIND"}
    items = [i for i in jload(E1 / "build" / "items_final.json")
             if i.get("label", i["label_pre"]) in SCOREABLE]
    for it in items:
        it["question"] = qmap.get(it["item_id"], "")
    return items, blind, idxT, idxB


def assemble(items, blind, indexed, judgment="fok"):
    """Join one population into aligned arrays. Mirrors score_e1.row()."""
    y, b, i, g, ids = [], [], [], [], []
    for it in items:
        q, tag = it["question"], it["item_id"]
        if q not in blind or tag not in indexed:
            continue
        bv, iv = blind[q].get(judgment), indexed[tag].get(judgment)
        if bv is None or iv is None:
            continue
        lab = it.get("label", it["label_pre"])
        y.append((0 if lab == "ABSENT" else 1) if judgment == "fok"
                 else (1 if lab == "PRESENT-NEGATIVE" else 0))
        b.append(bv)
        i.append(iv)
        g.append(it["persona"])
        ids.append(tag)
    return np.array(b, float), np.array(i, float), np.array(y, int), np.array(g), ids


POPULATIONS = {
    "R-FOK-HARD":  dict(filt=lambda it: it["tier"] == "hard", judgment="fok"),
    "R-FOK-FRB":   dict(filt=lambda it: it["tier"] == "hard" and it["backend"] == "frbank",
                        judgment="fok"),
    "R-FOK-EASY":  dict(filt=lambda it: it["tier"] == "easy", judgment="fok"),
    "R-NOK-FRB":   dict(filt=lambda it: it["backend"] == "frbank", judgment="nok"),
    "R-FOK-MEM0":  dict(filt=lambda it: it["backend"] == "mem0", judgment="fok"),
    "R-FOK-AMEM":  dict(filt=lambda it: it["backend"] == "amem", judgment="fok"),
}
