"""E1-R sub-step (d): reliability diagrams + the monotonicity test behind A4/B5.

The frozen branch for A4/B5 turns on whether the curves are monotone but poorly scaled
(a ranker) or non-monotone (neither). Monotonicity is tested on bins with n >= 10, using
Spearman rank correlation between mean predicted probability and observed frequency.
"""
from __future__ import annotations

import numpy as np

import matplotlib
matplotlib.use("Agg")
# R86 Phase 4: embed TrueType rather than matplotlib's default Type 3. hygiene_scan
# fails on any Type 3 font, and this figure was the manuscript's only one.
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
import matplotlib.pyplot as plt          # noqa: E402
from scipy.stats import spearmanr        # noqa: E402

from common_e1r import OUT, jdump, jload  # noqa: E402

ARMS = ["blind", "intact", "names only"]
MIN_BIN = 10


def main():
    d = jload(OUT / "ece.json")
    base_rate = d["n_pos"] / d["n"]
    stats = {"base_rate": base_rate, "n": d["n"], "n_pos": d["n_pos"], "arms": {}}

    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.9), sharey=True)
    for ax, arm in zip(axes, ARMS):
        rel = d["arms"][arm]["reliability"]
        big = [b for b in rel if b["n"] >= MIN_BIN]
        pred = np.array([b["mean_pred"] for b in big])
        obs = np.array([b["obs_freq"] for b in big])
        ns = np.array([b["n"] for b in big])
        rho, p = (spearmanr(pred, obs) if len(big) > 2 else (float("nan"),) * 2)
        mono = bool(np.all(np.diff(obs) >= -1e-12))
        stats["arms"][arm] = {
            "ece": d["arms"][arm]["ece"], "auroc": d["arms"][arm]["auroc"],
            "n_bins_ge_10": len(big),
            "spearman_rho": float(rho), "spearman_p": float(p),
            "strictly_monotone_nondecreasing": mono,
            "max_overconfidence_gap": float(np.min(obs - pred)),
            "mean_pred_overall": float(np.average(pred, weights=ns)),
            "obs_freq_overall": float(np.average(obs, weights=ns)),
        }

        ax.plot([0, 1], [0, 1], ls="--", lw=1, color="0.6", label="perfect calibration")
        ax.axhline(base_rate, ls=":", lw=1, color="0.4", label="base rate")
        ax.plot(pred, obs, "-o", color="#1f4e79", lw=1.6, ms=4.5, label="observed")
        for b in big:
            ax.annotate(f"{b['n']}", (b["mean_pred"], b["obs_freq"]),
                        textcoords="offset points", xytext=(4, 5), fontsize=7,
                        color="0.35")
        ax.set_title(f"{arm}\nECE {d['arms'][arm]['ece']:.4f} · "
                     f"AUROC {d['arms'][arm]['auroc']:.4f}", fontsize=9)
        ax.set_xlabel("mean predicted FOK", fontsize=8.5)
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.02, 1.02)
        ax.tick_params(labelsize=7.5)
        ax.grid(alpha=0.18)
    axes[0].set_ylabel("observed frequency", fontsize=8.5)
    axes[0].legend(fontsize=7, loc="upper left", framealpha=0.9)
    fig.suptitle("Reliability on the pooled hard tier (n=588, base rate "
                 f"{base_rate:.3f}); bin counts annotated", fontsize=9.5)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"reliability.{ext}", dpi=200)
    plt.close(fig)

    ranker = all(stats["arms"][a]["spearman_rho"] > 0.8 for a in ARMS) and \
        all(stats["arms"][a]["max_overconfidence_gap"] < -0.15 for a in ARMS)
    stats["frozen_branch"] = (
        "MONOTONE BUT POORLY SCALED -- the monitor outputs a ranking signal rather than a "
        "calibrated probability. A4 and B5 are CONCEDED, and the manuscript's use of the "
        "word 'probability' is narrowed wherever it describes an elicited output rather "
        "than a defined target."
        if ranker else
        "NOT the monotone-but-misscaled pattern; see per-arm statistics before reading.")
    jdump(stats, OUT / "reliability.json")

    print("=" * 92)
    print("E1-R (d)  RELIABILITY AND THE 'RANKER, NOT A PROBABILITY' TEST")
    print("=" * 92)
    print(f"population base rate: {base_rate:.4f}  ({d['n_pos']}/{d['n']})\n")
    hdr = (f"{'arm':14s} {'bins>=10':>9s} {'spearman':>9s} {'p':>8s} {'monotone':>9s} "
           f"{'worst gap':>10s} {'mean pred':>10s} {'obs':>7s}")
    print(hdr); print("-" * len(hdr))
    for a in ARMS:
        s = stats["arms"][a]
        print(f"{a:14s} {s['n_bins_ge_10']:9d} {s['spearman_rho']:9.4f} "
              f"{s['spearman_p']:8.4f} {str(s['strictly_monotone_nondecreasing']):>9s} "
              f"{s['max_overconfidence_gap']:+10.3f} {s['mean_pred_overall']:10.3f} "
              f"{s['obs_freq_overall']:7.3f}")
    print()
    print("FROZEN BRANCH SELECTED:"); print(" ", stats["frozen_branch"])
    print(f"\nwrote {OUT / 'reliability.pdf'}, .png and reliability.json")


if __name__ == "__main__":
    main()