"""Independent corroboration of the clustered-bootstrap widths.

The clustered intervals came out NARROWER than the item-level intervals on four of six
rows. That is the opposite of the direction reviewer B2 assumed, so it is checked here by
two methods that do not share the bootstrap's machinery:

  1. Cluster jackknife (delete-one-persona) standard error -- the standard design-based
     variance estimator for clustered data, computed from the LOPO deltas.
  2. Intracluster correlation of the per-item pair contribution, which explains the
     direction if it is negative (a within-persona balanced design).

If the jackknife agrees with the clustered bootstrap, the narrowing is a property of the
design, not a bug in the resampler.
"""
from __future__ import annotations

import numpy as np

from common_e1r import (POPULATIONS, OUT, assemble, auroc, boot_cluster, boot_item,
                        jdump, load_e1)


def cluster_jackknife(b, i, y, g):
    """Delete-one-cluster jackknife SE for the paired AUROC delta."""
    groups = np.unique(g)
    K = len(groups)
    ds = []
    for u in groups:
        k = g != u
        if len(set(y[k].tolist())) < 2:
            continue
        ds.append(auroc(i[k], y[k]) - auroc(b[k], y[k]))
    ds = np.asarray(ds, float)
    K = len(ds)
    var = (K - 1) / K * float(((ds - ds.mean()) ** 2).sum())
    return float(np.sqrt(var)), K


def icc_of_contribution(b, i, y, g):
    """One-way ANOVA intracluster correlation of the per-item arm difference.

    Contribution proxy: indexed minus blind score for that item. A negative ICC means
    items within a persona vary in compensating directions -- a balanced design -- which
    makes whole-persona resampling LESS variable than independent item resampling.
    """
    x = np.asarray(i, float) - np.asarray(b, float)
    groups = np.unique(g)
    k = len(groups)
    n = len(x)
    grand = x.mean()
    ns = np.array([int((g == u).sum()) for u in groups], float)
    means = np.array([x[g == u].mean() for u in groups], float)
    ssb = float((ns * (means - grand) ** 2).sum())
    ssw = float(sum(((x[g == u] - means[j]) ** 2).sum() for j, u in enumerate(groups)))
    msb = ssb / (k - 1)
    msw = ssw / (n - k)
    n0 = (n - (ns ** 2).sum() / n) / (k - 1)
    icc = (msb - msw) / (msb + (n0 - 1) * msw)
    return float(icc), float(n0)


def main():
    items, blind, idxT, idxB = load_e1()
    out = {}
    print("=" * 104)
    print("E1-R (a) VALIDATION -- is the clustered narrowing real?")
    print("=" * 104)
    hdr = (f"{'row':13s} {'boot item w':>12s} {'boot clus w':>12s} {'jack SE':>9s} "
           f"{'jack w(1.96)':>13s} {'clus/jack':>10s} {'ICC':>8s}")
    print(hdr)
    print("-" * len(hdr))
    for rid, spec in POPULATIONS.items():
        sub = [it for it in items if spec["filt"](it)]
        b, i, y, g, _ = assemble(sub, blind, idxT, judgment=spec["judgment"])
        bi, bc = boot_item(b, i, y), boot_cluster(b, i, y, g)
        w_it = bi["ci_hi"] - bi["ci_lo"]
        w_cl = bc["ci_hi"] - bc["ci_lo"]
        se, K = cluster_jackknife(b, i, y, g)
        w_jk = 2 * 1.96 * se
        icc, n0 = icc_of_contribution(b, i, y, g)
        out[rid] = {"width_item_boot": w_it, "width_cluster_boot": w_cl,
                    "cluster_jackknife_se": se, "cluster_jackknife_width_1p96": w_jk,
                    "cluster_boot_over_jackknife": w_cl / w_jk,
                    "icc_contribution": icc, "icc_n0": n0, "jackknife_folds": K}
        print(f"{rid:13s} {w_it:12.4f} {w_cl:12.4f} {se:9.4f} {w_jk:13.4f} "
              f"{w_cl / w_jk:10.2f} {icc:8.4f}")
    jdump(out, OUT / "clustered_validation.json")
    print()
    print("Reading: cluster_boot / jackknife near 1.0 means the two independent cluster-level")
    print("variance estimators agree, so the narrowing is a design property, not a resampler bug.")
    print("A negative ICC means items within a persona compensate -- the balanced-by-persona")
    print("construction -- which is exactly what makes whole-persona resampling less variable.")
    print(f"\nwrote {OUT / 'clustered_validation.json'}")


if __name__ == "__main__":
    main()