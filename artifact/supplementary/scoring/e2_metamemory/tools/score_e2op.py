"""score_e2op.py -- E2-OP scoring. Produces PREREG_E2OP.md §3 and nothing else.

ASSEMBLY route: every arm is built by re-indexing committed answer rows and their
committed judge verdicts. NO API CALLS. NO ELICITATION. NO RE-JUDGING.

The estimator is IMPORTED from score_e2, not reimplemented, so H-OP1 is computed
by byte-identical code to the one that produced H-C2: covariate-adjusted paired
comparison (OLS on persona + coverage-label fixed effects, sum-to-zero, intercept
is the estimate), persona-clustered bootstrap, 1,000 resamples, seed 42.

Gates read mechanically. No recommendation is produced anywhere in this file.

Usage:  python e2_metamemory/tools/score_e2op.py
"""
from __future__ import annotations

import collections
import io
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e2_common import E2, S0, S1, S2, jload, load_items          # noqa: E402
from score_e2 import adjusted, boot_ci, credit_of, state5        # noqa: E402
from score_e2 import NBOOT, SEED                                 # noqa: E402

TAU_FOK = 0.20            # frozen, THRESHOLDS_FROZEN.json
TAU_OP = 0.20             # frozen, PREREG_E2OP.md §1
N_SEEDS = 1000            # frozen, PREREG_E2OP.md §2
# Committed reference values from RESULTS_E2.md §3.1 — the assembly must reproduce
# these exactly or the route is invalid and the run stops.
REF = {"v_confab_n": 149, "vi_confab_n": 120, "n_eval": 529,
       "v_rate": 0.684, "blanket_unadj": -0.0548}


def main():
    items = {i["item_id"]: i for i in load_items()}
    tags = sorted(i["item_id"] for i in load_items() if i["split"] == "eval")
    g = {r["item_id"]: r for r in jload(E2 / "gates_eval.json")["rows"]}
    ans = jload(E2 / "answers_eval.json")["rows"]
    judg = jload(E2 / "cache" / "judgments_eval.json")

    # ---- committed per-(item,state) outcomes, built exactly as score_e2 builds them
    cell = {}
    for a in ans:
        v = judg.get(f"{a['item_id']}|{a['response_sha'][:24]}", {})
        lab = items[a["item_id"]]["label_final"]
        cell[(a["item_id"], a["state"])] = (
            credit_of(lab, v.get("correctness")), bool(v.get("confabulation")),
            state5(v.get("correctness"), bool(v.get("confabulation"))))
    missing = [(t, s) for t in tags for s in (S0, S1, S2) if (t, s) not in cell]
    if missing:
        raise SystemExit(f"ASSEMBLY INVALID: {len(missing)} (item,state) cells missing")

    def fok(t):
        return ((g[t]["indexed"].get("1") or {}).get("fok"))

    def nok(t):
        return ((g[t]["indexed"].get("1") or {}).get("nok"))

    retrieved = [t for t in tags if (fok(t) is not None and fok(t) >= TAU_FOK)]
    selected = [t for t in retrieved if (nok(t) is not None and nok(t) >= TAU_OP)]
    n_sel = len(selected)
    sel_set = set(selected)

    def confab(t, state):
        return cell[(t, state)][1]

    def credit(t, state):
        return cell[(t, state)][0]

    ret_set = set(retrieved)

    def state_v(t):
        return S1 if t in ret_set else S0

    def state_vi(t):
        return S2 if t in ret_set else S0

    def state_op(t):
        return (S2 if t in sel_set else S1) if t in ret_set else S0

    # ---- FIDELITY: the assembly must reproduce the committed policy table
    v_confab_n = sum(confab(t, state_v(t)) for t in tags)
    vi_confab_n = sum(confab(t, state_vi(t)) for t in tags)
    fidelity = {"n_eval": len(tags), "v_confab_n": v_confab_n,
                "vi_confab_n": vi_confab_n,
                "v_rate": round(len(retrieved) / len(tags), 4)}
    fid_ok = (len(tags) == REF["n_eval"] and v_confab_n == REF["v_confab_n"]
              and vi_confab_n == REF["vi_confab_n"]
              and abs(fidelity["v_rate"] - REF["v_rate"]) < 5e-4)
    fidelity["PASS"] = bool(fid_ok)
    if not fid_ok:
        raise SystemExit(f"ASSEMBLY FIDELITY FAILED: {fidelity} vs {REF}")

    # ---- (vii-NOK): 1,000 uniform random subsets of size n_sel from `retrieved`
    rng = np.random.default_rng(SEED)
    ridx = np.asarray(retrieved)
    per_item_hits = collections.Counter()
    seed_rates = []
    for _ in range(N_SEEDS):
        pick = set(rng.choice(ridx, size=n_sel, replace=False).tolist())
        for t in pick:
            per_item_hits[t] += 1
        r = sum(confab(t, (S2 if t in pick else S1) if t in ret_set else S0)
                for t in tags) / len(tags)
        seed_rates.append(r)
    seed_rates = np.asarray(seed_rates)

    # expected per-item confabulation under random assignment, as frozen:
    # the MEAN over the 1,000 seeds
    def rand_expected(t):
        if t not in ret_set:
            return float(confab(t, S0))
        p = per_item_hits[t] / N_SEEDS
        return p * float(confab(t, S2)) + (1 - p) * float(confab(t, S1))

    # analytic check: uniform fixed-size draw => marginal inclusion = n_sel/|retrieved|
    p_analytic = n_sel / len(retrieved)

    def rand_analytic(t):
        if t not in ret_set:
            return float(confab(t, S0))
        return p_analytic * float(confab(t, S2)) + (1 - p_analytic) * float(confab(t, S1))

    # ---- H-OP1: targeted vs rate-matched random, H-C2's exact endpoint
    d1 = [(items[t]["persona"], items[t]["label_final"],
           float(confab(t, state_op(t))) - rand_expected(t)) for t in tags]
    adj1 = adjusted(d1, None, None)
    un1 = float(np.mean([v for _p, _l, v in d1]))
    lo1, hi1 = boot_ci(d1)
    hopn1 = (hi1 < 0)

    d1a = [(items[t]["persona"], items[t]["label_final"],
            float(confab(t, state_op(t))) - rand_analytic(t)) for t in tags]
    adj1_analytic = adjusted(d1a, None, None)

    # permutation reference: where does the targeted arm sit among the 1,000 draws?
    op_rate = sum(confab(t, state_op(t)) for t in tags) / len(tags)
    n_le = int((seed_rates <= op_rate).sum())
    perm_p = (n_le + 1) / (N_SEEDS + 1)

    # ---- H-OP2: does targeted retain >= half of blanket's benefit?
    d2 = [(items[t]["persona"], items[t]["label_final"],
           float(confab(t, state_op(t))) - float(confab(t, state_v(t)))) for t in tags]
    adj2 = adjusted(d2, None, None)
    un2 = float(np.mean([v for _p, _l, v in d2]))
    lo2, hi2 = boot_ci(d2)
    blanket_un = (vi_confab_n - v_confab_n) / len(tags)
    half = 0.5 * blanket_un
    hopn2 = (un2 <= half)

    # ---- reproduce PREREG_E2OP §1's frozen tau-derivation table, so the prereg's
    # own monitoring-side numbers are verifiable rather than quoted from prose.
    # Monitoring rows and construction labels only; no control outcome enters.
    def is_pn(t):
        return items[t]["label_final"] == "PRESENT-NEGATIVE"
    base_all = sum(is_pn(t) for t in tags) / len(tags)
    base_ret = sum(is_pn(t) for t in retrieved) / len(retrieved)
    ladder = []
    P = sum(is_pn(t) for t in retrieved)
    N = len(retrieved) - P
    for t_ in sorted({nok(t) for t in retrieved if nok(t) is not None}):
        s = [t for t in retrieved if (nok(t) or 0) >= t_]
        tp = sum(is_pn(t) for t in s)
        ladder.append({"tau": t_, "selected": len(s),
                       "precision": round(tp / len(s), 4) if s else None,
                       "recall": round(tp / P, 4),
                       "youden": round(tp / P - (len(s) - tp) / N, 4)})
    v_rate_c = v_confab_n / len(tags)
    out = {
        "run": "E2-OP", "route": "assembly", "api_calls": 0, "usd": 0.0,
        "estimator": "imported from score_e2.adjusted/boot_ci — byte-identical to H-C2",
        "nboot": NBOOT, "seed": SEED, "n_seeds_random": N_SEEDS,
        "tau_FOK": TAU_FOK, "tau_OP": TAU_OP,
        "n_eval": len(tags), "n_retrieved": len(retrieved), "n_selected": n_sel,
        "selected_fraction_of_retrieved": round(n_sel / len(retrieved), 4),
        "fidelity": fidelity,
        "tau_derivation": {
            "note": "reproduces PREREG_E2OP.md §1; monitoring rows + construction "
                    "labels only, no control outcome",
            "pn_base_all_items": round(base_all, 4),
            "pn_base_retrieved": round(base_ret, 4),
            "ladder_on_retrieved": ladder,
            "max_youden": round(max(r["youden"] for r in ladder), 4),
            "precision_min": round(min(r["precision"] for r in ladder), 4),
            "precision_max": round(max(r["precision"] for r in ladder), 4),
        },
        "confab_rates": {
            "(v) gate only": round(v_rate_c, 4),
            "(vi) blanket": round(vi_confab_n / len(tags), 4),
            "(vi-OP) targeted": round(op_rate, 4),
            "(vii-NOK) random, mean of seeds": round(float(seed_rates.mean()), 4),
            "(vii-NOK) random, sd": round(float(seed_rates.std(ddof=1)), 5),
            "(vii-NOK) random, min": round(float(seed_rates.min()), 4),
            "(vii-NOK) random, max": round(float(seed_rates.max()), 4),
        },
        "H_OP1": {
            "contrast": "confab(vi-OP) - confab(vii-NOK, mean of 1000 seeds)",
            "adjusted": round(adj1, 5), "unadjusted": round(un1, 5),
            "ci95": [round(lo1, 5), round(hi1, 5)],
            "adjusted_analytic_check": round(adj1_analytic, 5),
            "permutation_p_one_sided": round(perm_p, 4),
            "n_seeds_at_or_below_targeted": n_le,
            "HOLDS": bool(hopn1),
        },
        "H_OP2": {
            "contrast": "confab(vi-OP) - confab(v)",
            "adjusted": round(adj2, 5), "unadjusted": round(un2, 5),
            "ci95": [round(lo2, 5), round(hi2, 5)],
            "blanket_unadjusted": round(blanket_un, 5),
            "half_of_blanket": round(half, 5),
            "HOLDS": bool(hopn2),
            # the retention ratio IS the quantity H-OP2 tests; the random row is the
            # same ratio for the rate-matched comparator, for reading only.
            "retention_fraction_targeted": round(un2 / blanket_un, 4),
            "retention_fraction_random": round(
                (float(seed_rates.mean()) - v_rate_c) / blanket_un, 4),
            "instructed_fraction_of_blanket": round(n_sel / len(retrieved), 4),
        },
    }
    with io.open(E2 / "results" / "e2op_scores.json", "w",
                 encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    W = 78
    print("=" * W)
    print("E2-OP — assembly, scored per PREREG_E2OP.md §3 and nothing else")
    print("=" * W)
    print(f"  fidelity vs committed policy table: {fidelity}")
    print(f"  tau_OP {TAU_OP}   retrieved {len(retrieved)}   selected {n_sel} "
          f"({n_sel/len(retrieved):.1%} of retrieved)")
    print()
    for k, v in out["confab_rates"].items():
        print(f"  {k:38s} {v}")
    print()
    print("-" * W)
    print("H-OP1  targeted vs rate-matched random, H-C2's endpoint")
    print("-" * W)
    h = out["H_OP1"]
    print(f"  adjusted {h['adjusted']:+.5f}   unadjusted {h['unadjusted']:+.5f}   "
          f"95% CI [{h['ci95'][0]:+.5f}, {h['ci95'][1]:+.5f}]")
    print(f"  analytic cross-check of the random arm: {h['adjusted_analytic_check']:+.5f}")
    print(f"  permutation: targeted rate {op_rate:.4f}; "
          f"{h['n_seeds_at_or_below_targeted']}/{N_SEEDS} random draws at or below; "
          f"p = {h['permutation_p_one_sided']:.4f}")
    print(f"  ==> H-OP1 {'HOLDS' if h['HOLDS'] else 'FAILS'}")
    print()
    print("-" * W)
    print("H-OP2  does targeted retain >= half of blanket's benefit?")
    print("-" * W)
    h2 = out["H_OP2"]
    print(f"  targeted - (v): adjusted {h2['adjusted']:+.5f}  "
          f"unadjusted {h2['unadjusted']:+.5f}  CI [{h2['ci95'][0]:+.5f}, {h2['ci95'][1]:+.5f}]")
    print(f"  blanket - (v) unadjusted {h2['blanket_unadjusted']:+.5f}; "
          f"half = {h2['half_of_blanket']:+.5f}")
    print(f"  ==> H-OP2 {'HOLDS' if h2['HOLDS'] else 'FAILS'}")
    print()
    print(f"wrote {E2 / 'results' / 'e2op_scores.json'}   spend $0.00, 0 API calls")


if __name__ == "__main__":
    main()
