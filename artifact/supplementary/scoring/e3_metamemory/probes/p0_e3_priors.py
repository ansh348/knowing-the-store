"""p0_e3_priors.py -- E3 band derivation: the contrasts E3's gates need, measured on E2.

READ-ONLY over E2 artifacts. NO API CALLS. Computes nothing new about E2's own
hypotheses; it recomputes, with E2's own estimator and bootstrap, the two paired
contrasts E3's bands must be derived from and which RESULTS_E2 did not report:

    (vi) vs (i)    the FULL policy against always-retrieve -- E3's H-E3a prior
    (vi) vs (vii)  the FULL policy against a rate-matched RANDOM gate -- the
                   closest thing E2 has to E3's SHUFFLED monitor, and therefore
                   the only empirical basis for H-E3c's fraction

The estimator, the fixed effects, the seed, the resample count and the clustering
are score_e2's, imported rather than re-implemented.

Usage:  python e3_metamemory/probes/p0_e3_priors.py
"""

from __future__ import annotations

import collections
import hashlib
import io
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
E2D = ROOT / "e2_metamemory"
sys.path.insert(0, str(E2D / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))

from e2_common import S0, S1, S2, jload, load_items          # noqa: E402
from score_e2 import adjusted, boot_ci, credit_of, state5    # noqa: E402

OUT = Path(__file__).resolve().parent / "p0_e3_priors.json"


def main():
    items = {i["item_id"]: i for i in load_items()}
    tags = sorted(i["item_id"] for i in load_items() if i["split"] == "eval")
    thr = jload(E2D / "THRESHOLDS_FROZEN.json")
    g = {r["item_id"]: r for r in jload(E2D / "gates_eval.json")["rows"]}
    ans = jload(E2D / "answers_eval.json")["rows"]
    judg = jload(E2D / "cache" / "judgments_eval.json")

    cell = {}
    for a in ans:
        v = judg.get(f"{a['item_id']}|{a['response_sha'][:24]}", {})
        lab = items[a["item_id"]]["label_final"]
        cell[(a["item_id"], a["state"])] = (
            credit_of(lab, v.get("correctness")), bool(v.get("confabulation")))

    TAU = {"iii": thr["tau_sim"], "iv": thr["tau_verb"], "v": thr["tau_FOK"],
           "vi": thr["tau_FOK"]}

    def sig(pol, t):
        r = g[t]
        if pol == "iii":
            return r["sim_max_blended"]
        if pol == "iv":
            return (r["verbal"].get("1") or {}).get("p_store_has_relevant")
        return (r["indexed"].get("1") or {}).get("fok")

    def retrieves(pol, t, rate_v):
        if pol == "i":
            return True
        if pol == "ii":
            return False
        if pol == "vii":
            h = int(hashlib.sha256(f"42|{t}".encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
            return h < rate_v
        tau = TAU[pol]
        return tau is not None and (sig("v" if pol == "vi" else pol, t) or -1) >= tau

    def state_of(pol, t, rate_v):
        if not retrieves(pol, t, rate_v):
            return S0
        if pol == "vi":
            nk = (g[t]["indexed"].get("1") or {}).get("nok")
            if thr["tau_NOK"] is not None and nk is not None and nk >= thr["tau_NOK"]:
                return S2
        return S1

    rate_v = sum(1 for t in tags if retrieves("v", t, 0)) / len(tags)

    def paired(pa, pb, field):
        d = []
        for t in tags:
            ca = cell[(t, state_of(pa, t, rate_v))]
            cb = cell[(t, state_of(pb, t, rate_v))]
            if ca[0] is None or cb[0] is None:
                continue
            va = ca[0] if field == "credit" else (1.0 if ca[1] else 0.0)
            vb = cb[0] if field == "credit" else (1.0 if cb[1] else 0.0)
            d.append((items[t]["persona"], items[t]["label_final"], va - vb))
        return d

    def contrast(pa, pb, field):
        d = paired(pa, pb, field)
        lo, hi = boot_ci(d, False)
        return {"adjusted": adjusted(d, None, None),
                "unadjusted": float(np.mean([v for _p, _l, v in d])),
                "ci_lo": lo, "ci_hi": hi, "n": len(d),
                "excludes_zero": bool(lo > 0 or hi < 0),
                "se_implied": (hi - lo) / (2 * 1.96)}

    print("=" * 100)
    print("p0 -- E3 BAND PRIORS, recomputed on E2's eval split with E2's own estimator")
    print("=" * 100)
    out = {}
    for name, (pa, pb) in {
        "FULL vs always  (vi)-(i)": ("vi", "i"),
        "FULL vs random  (vi)-(vii)": ("vi", "vii"),
        "gate vs always  (v)-(i)": ("v", "i"),
        "gate vs random  (v)-(vii)": ("v", "vii"),
    }.items():
        row = {f: contrast(pa, pb, f) for f in ("confab", "credit")}
        out[name] = row
        c, k = row["confab"], row["credit"]
        print(f"\n  {name}")
        print(f"    confabulation  adj {c['adjusted']:+.4f}  unadj {c['unadjusted']:+.4f}"
              f"  CI [{c['ci_lo']:+.4f}, {c['ci_hi']:+.4f}]  "
              f"{'excludes 0' if c['excludes_zero'] else 'INCLUDES 0'}  "
              f"SE~{c['se_implied']:.4f}")
        print(f"    credit         adj {k['adjusted']:+.4f}  unadj {k['unadjusted']:+.4f}"
              f"  CI [{k['ci_lo']:+.4f}, {k['ci_hi']:+.4f}]  "
              f"{'excludes 0' if k['excludes_zero'] else 'INCLUDES 0'}  "
              f"SE~{k['se_implied']:.4f}")

    a = -out["FULL vs always  (vi)-(i)"]["confab"]["adjusted"]     # advantage, positive
    b = -out["FULL vs random  (vi)-(vii)"]["confab"]["adjusted"]
    print("\n" + "=" * 100)
    print("THE H-E3c FRACTION, as E2's data implies it")
    print("=" * 100)
    print(f"  FULL's confabulation advantage over always-retrieve      : {a:+.4f}")
    print(f"  FULL's confabulation advantage over a RATE-MATCHED RANDOM: {b:+.4f}")
    print(f"  implied monitor-attributable fraction                    : {b / a:.3f}")
    print("  E2's (vii) is a random GATE with no obligation layer, so it is a WEAKER")
    print("  lobotomy than E3's SHUFFLED (which permutes FOK *and* NOK). The fraction")
    print("  above is therefore a LOWER bound on what SHUFFLED would give -- but it is the")
    print("  only measured anchor that exists, and it sits far below 2/3.")

    # ---------------- power arithmetic for the proposed bands, at E2's measured SE
    se = out["FULL vs always  (vi)-(i)"]["confab"]["se_implied"]
    print("\n" + "=" * 100)
    print("POWER FOR H-E3a AT E2'S MEASURED SE, AND AT E3-DEGRADED SEs")
    print("=" * 100)
    from math import erf, sqrt
    phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))                       # noqa: E731
    print("  A band of '>= 3pp AND CI excludes zero' binds on whichever is larger:")
    print("  the 3pp floor, or 1.96*SE. Power = P(estimate clears the binding one).")
    print(f"\n  {'SE':>8s} {'binding':>10s}  " +
          "".join(f"{'d=' + str(x) + 'pp':>10s}" for x in (3, 5, 7, 10, 14)))
    for mult, lab in ((1.0, "E2 SE"), (1.33, "x1.33"), (1.75, "x1.75"), (2.5, "x2.5")):
        s = se * mult
        binding = max(0.03, 1.96 * s)
        row = "".join(f"{phi((x / 100 - binding) / s):>10.1%}" for x in (3, 5, 7, 10, 14))
        print(f"  {s:>8.4f} {binding:>10.4f}  {row}   ({lab})")
    print("\n  Read: at E2's own precision the band is cleared with near-certainty at the")
    print("  effect E2 measured. The design question is how much precision E3 LOSES, and")
    print("  that is set by the number of independent persona clusters and by how much of")
    print("  a question's variance is shared across rungs -- not by the raw cell count.")

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"contrasts": out, "fraction_implied": b / a,
                   "se_confab_full_vs_always": se}, f,
                  ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print(f"\n  written: {OUT}")


if __name__ == "__main__":
    main()
