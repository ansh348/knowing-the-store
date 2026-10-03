"""E1-R sub-step (d): ECE bootstrap intervals and reliability diagrams.

Reviewers A4 and B5: flat calibration means "a ranker, not a probability", and the paper
reports ECE point values with no intervals and no reliability diagrams.

Five arms on the pooled hard tier (n=588): blind, intact index, counts jittered, counts
coarsened, names only. Reproduction gate against the published values runs first.
"""
from __future__ import annotations

import sys

import numpy as np

from common_e1r import (E1, OUT, SEED, auroc, ece, jdump, jload, load_e1, persona_of,
                        reliability)

N_BOOT = 1000
PUBLISHED_ECE = {
    "blind": 0.1596, "intact": 0.1741, "counts jittered": 0.1720,
    "counts coarsened": 0.1668, "names only": 0.0583,
}
PUBLISHED_AUROC = {
    "blind": 0.5258, "intact": 0.7530, "counts jittered": 0.7697,
    "counts coarsened": 0.7625, "names only": 0.8516,
}
MECH_ARM = {"counts jittered": "A1-counts-jittered",
            "counts coarsened": "A2-counts-coarsened",
            "names only": "A3-names-only"}


def boot_ece(p, y, g, clustered, n=N_BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    p, y = np.asarray(p, float), np.asarray(y, int)
    vals = []
    if clustered:
        groups = np.unique(g)
        by = {u: np.flatnonzero(g == u) for u in groups}
        for _ in range(n):
            drawn = rng.integers(0, len(groups), len(groups))
            k = np.concatenate([by[groups[t]] for t in drawn])
            vals.append(ece(p[k], y[k]))
    else:
        for _ in range(n):
            k = rng.integers(0, len(y), len(y))
            vals.append(ece(p[k], y[k]))
    v = np.asarray(vals, float)
    return {"ci_lo": float(np.percentile(v, 2.5)),
            "ci_hi": float(np.percentile(v, 97.5)), "mean": float(v.mean())}


def boot_ece_diff(p1, p2, y, g, clustered, n=N_BOOT, seed=SEED):
    """Paired bootstrap of ECE(arm) - ECE(blind); both arms move on the same draw."""
    rng = np.random.default_rng(seed)
    p1, p2, y = np.asarray(p1, float), np.asarray(p2, float), np.asarray(y, int)
    vals = []
    if clustered:
        groups = np.unique(g)
        by = {u: np.flatnonzero(g == u) for u in groups}
        for _ in range(n):
            drawn = rng.integers(0, len(groups), len(groups))
            k = np.concatenate([by[groups[t]] for t in drawn])
            vals.append(ece(p1[k], y[k]) - ece(p2[k], y[k]))
    else:
        for _ in range(n):
            k = rng.integers(0, len(y), len(y))
            vals.append(ece(p1[k], y[k]) - ece(p2[k], y[k]))
    v = np.asarray(vals, float)
    lo, hi = float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))
    return {"ci_lo": lo, "ci_hi": hi, "mean": float(v.mean()),
            "excludes_zero": bool(lo > 0 or hi < 0)}


def main():
    items, blind, idxT, _ = load_e1()
    hard = [it for it in items if it["tier"] == "hard"]
    mech = jload(E1 / "mechanism_elicitation.json")
    mech_by = {}
    for r in mech:
        if r["status"] == "OK" and r.get("fok") is not None:
            mech_by.setdefault(r["arm"], {})[r["item_id"]] = r["fok"]

    # aligned population: hard-tier items joinable in every arm
    base = []
    for it in hard:
        q, tag = it["question"], it["item_id"]
        if q not in blind or tag not in idxT:
            continue
        if blind[q].get("fok") is None or idxT[tag].get("fok") is None:
            continue
        if not all(tag in mech_by.get(a, {}) for a in MECH_ARM.values()):
            continue
        lab = it.get("label", it["label_pre"])
        base.append({"tag": tag, "y": 0 if lab == "ABSENT" else 1,
                     "persona": it["persona"],
                     "blind": blind[q]["fok"], "intact": idxT[tag]["fok"],
                     **{k: mech_by[a][tag] for k, a in MECH_ARM.items()}})

    y = np.array([r["y"] for r in base], int)
    g = np.array([r["persona"] for r in base])
    arms = {k: np.array([r[k] for r in base], float) for k in PUBLISHED_ECE}

    fails = []
    res = {"n": len(base), "n_pos": int(y.sum()), "arms": {}}
    for name, p in arms.items():
        e, a = ece(p, y), auroc(p, y)
        ok_e = abs(e - PUBLISHED_ECE[name]) < 5e-5
        ok_a = abs(a - PUBLISHED_AUROC[name]) < 5e-5
        if not (ok_e and ok_a):
            fails.append((name, round(e, 4), PUBLISHED_ECE[name],
                          round(a, 4), PUBLISHED_AUROC[name]))
        res["arms"][name] = {
            "ece": float(e), "ece_published": PUBLISHED_ECE[name], "ece_reproduces": ok_e,
            "auroc": float(a), "auroc_published": PUBLISHED_AUROC[name],
            "auroc_reproduces": ok_a,
            "ece_ci_item": boot_ece(p, y, g, False),
            "ece_ci_cluster": boot_ece(p, y, g, True),
            "reliability": reliability(p, y),
        }
    if fails:
        print("REPRODUCTION GATE FAILED"); [print("  ", f) for f in fails]
        jdump({"gate": "FAILED", "detail": fails}, OUT / "ece.json")
        sys.exit(1)

    res["diff_vs_blind"] = {}
    for name, p in arms.items():
        if name == "blind":
            continue
        res["diff_vs_blind"][name] = {
            "delta_ece": float(ece(p, y) - ece(arms["blind"], y)),
            "ci_item": boot_ece_diff(p, arms["blind"], y, g, False),
            "ci_cluster": boot_ece_diff(p, arms["blind"], y, g, True),
        }

    d = res["diff_vs_blind"]["intact"]["ci_item"]
    if not d["excludes_zero"]:
        branch = ("BLIND-INTACT ECE DIFFERENCE CI INCLUDES ZERO -- the intact index leaves "
                  "calibration statistically unchanged. The manuscript's existing word "
                  "'unimproved' is exactly right and stays; it may not be upgraded to 'worse'.")
    else:
        branch = ("BLIND-INTACT ECE DIFFERENCE CI EXCLUDES ZERO -- the index measurably "
                  "degrades calibration while improving discrimination; report as a genuine "
                  "cost of the method, not a neutral negative result.")
    res["frozen_branch"] = branch
    res["spec"] = "e1r_robustness/SPEC_E1R.md @ 9ac91a2"
    jdump(res, OUT / "ece.json")

    print("=" * 104)
    print("E1-R (d)  ECE INTERVALS AND RELIABILITY  (pooled hard tier)")
    print("=" * 104)
    print(f"reproduction gate: PASSED on all 5 arms (ECE and AUROC to 4 dp), n={len(base)}\n")
    hdr = (f"{'arm':18s} {'AUROC':>7s} {'ECE':>7s} {'ECE CI (item)':>20s} "
           f"{'ECE CI (cluster)':>20s}")
    print(hdr); print("-" * len(hdr))
    for name in PUBLISHED_ECE:
        a = res["arms"][name]
        ci, cl = a["ece_ci_item"], a["ece_ci_cluster"]
        print(f"{name:18s} {a['auroc']:7.4f} {a['ece']:7.4f} "
              f"[{ci['ci_lo']:.4f},{ci['ci_hi']:.4f}] [{cl['ci_lo']:.4f},{cl['ci_hi']:.4f}]")
    print()
    print(f"{'arm vs blind':18s} {'dECE':>8s} {'CI (item)':>21s} {'excl 0':>7s}")
    for name, v in res["diff_vs_blind"].items():
        c = v["ci_item"]
        print(f"{name:18s} {v['delta_ece']:+8.4f} [{c['ci_lo']:+.4f},{c['ci_hi']:+.4f}] "
              f"{str(c['excludes_zero']):>7s}")
    print()
    print("FROZEN BRANCH SELECTED:"); print(" ", branch)
    print(f"\nwrote {OUT / 'ece.json'}")


if __name__ == "__main__":
    main()