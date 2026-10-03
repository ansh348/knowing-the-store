"""
calibrate.py -- SP2: fit every policy's parameters on the CALIBRATION SPLIT ONLY.

Calibration personas are the 8 frozen in CALIBRATION_SPLIT.json. No eval-split
item is loaded, scored, or even opened by this file.

Per PREREG_E2 section 6:
  * uniform grid {0.00, 0.05, ..., 1.00} for every thresholded policy
  * objective = behaviour-typed credit / expected serving cost per turn,
    ties to lower cost
  * tau_NOK against confabulation / cost on calibration PN items only
  * each rival also records the threshold reproducing (v)'s calibration
    retrieval rate, for H-C1b's matched row
Also produces, per PREREG_E2 sections 2 and 2.1:
  * the measured answer variance sigma_a and the k-draw trigger decision
  * the power recomputation at measured variance (reported; bands untouched)
  * the index maintenance cost, measured rather than asserted

Writes THRESHOLDS_FROZEN.json and calibration_report.json.

Usage:  python e2_metamemory/tools/calibrate.py
"""

from __future__ import annotations

import collections
import io
import statistics as st
import sys
import time
from pathlib import Path

import numpy as np
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e2_common import E2, S0, S1, S2, jdump, jload, load_items, usd  # noqa: E402

GRID = [round(x * 0.05, 2) for x in range(21)]
SIGMA_TRIGGER = 0.065                       # frozen at SP1
SD_SIGNAL_ASSUMED = 0.20
DESIGN_EFFECT = 1.5
N_EVAL = 529
CPU_USD_PER_HOUR = 0.05                     # stated rate for index maintenance
QUERY_EMBED_USD = 15 / 1e6 * 0.02           # ~15 tokens on text-embedding-3-small


def credit_of(label, correctness):
    if correctness is None:
        return None
    if label == "ABSENT":
        return 1.0 if correctness == "ABSTAIN" else 0.0
    return {"CORRECT": 1.0, "PARTIAL": 0.5, "WRONG": 0.0, "ABSTAIN": 0.0}.get(
        correctness, 0.0)


def main():
    items = {i["item_id"]: i for i in load_items() if i["split"] == "calibration"}
    gates = {g["item_id"]: g for g in jload(E2 / "gates_calibration.json")["rows"]}
    answers = jload(E2 / "answers_calibration.json")["rows"]
    judg = jload(E2 / "cache" / "judgments_calibration.json")

    # ---------------- per (item, state, draw): credit, confab, cost ----------
    cell = collections.defaultdict(list)
    tok = collections.defaultdict(list)
    for a in answers:
        key = f"{a['item_id']}|{a['response_sha'][:24]}"
        v = judg.get(key, {})
        c = credit_of(items[a["item_id"]]["label_final"], v.get("correctness"))
        if c is None:
            continue
        cell[(a["item_id"], a["state"])].append((c, bool(v.get("confabulation")),
                                                 a["draw"]))
        tok[a["state"]].append((a["prompt_tokens"] or 0, a["completion_tokens"] or 0))

    def agg(tag, state):
        v = cell.get((tag, state))
        if not v:
            return None, None, 0
        return (sum(x[0] for x in v) / len(v),
                sum(1 for x in v if x[1]) / len(v), len(v))

    # ---------------- sigma_a: answer variance, and the k trigger ------------
    sds = [st.stdev([x[0] for x in v]) for v in cell.values() if len(v) > 1]
    sigma_a = sum(sds) / len(sds) if sds else 0.0
    identical = sum(1 for v in cell.values() if len({x[0] for x in v}) == 1)
    k_decision = 3 if sigma_a > SIGMA_TRIGGER else 1

    # ---------------- costs, measured ---------------------------------------
    gate_tok = collections.defaultdict(list)
    for r in jload(E2 / "cache" / "responses.json").values():
        a = str(r.get("arm", ""))
        if a.startswith("gate-"):
            gate_tok[a.split("-d")[0]].append((r["prompt_tokens"],
                                               r["completion_tokens"]))
    c_gate = {k: usd(sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v))
              for k, v in gate_tok.items()}
    c_ans = {s: usd(sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v))
             for s, v in tok.items()}

    # index maintenance: measured, not asserted. Time index_v2's renderer over
    # the FR-Bank BELIEVED path per persona. No artifact is written.
    import index_v2 as IX
    from backends import load_backend
    from e0_common import load_joins, toks
    joins = load_joins()
    raw = collections.defaultdict(list)
    for r in load_backend("frbank"):
        raw[r["persona"]].append(r)
    t0 = time.perf_counter()
    n_stores = 0
    for name in sorted(joins):
        rows = sorted(raw[name], key=lambda r: r["entry_id"])
        for r in rows:
            r.setdefault("age", 0)
        b_sup, b_ret, b_exp, b_ev = IX.believed_lifecycle("frbank", rows,
                                                          joins[name].cutoff)
        IX.render(IX.view(rows, (b_sup, b_ret, b_exp)), b_ev,
                  IX.AVAIL[("frbank", "BELIEVED")])
        n_stores += 1
    build_s = (time.perf_counter() - t0) / n_stores
    c_index = build_s / 3600 * CPU_USD_PER_HOUR      # per rebuild == per write, worst case

    c_ret = QUERY_EMBED_USD

    # ---------------- policy simulation -------------------------------------
    tags = sorted(items)

    def simulate(policy, tau, tau_nok=None):
        cr, cf, cost, nret = [], [], [], 0
        for t in tags:
            g = gates[t]
            ix = g["indexed"].get("1") or g["indexed"].get(1) or {}
            vb = g["verbal"].get("1") or g["verbal"].get(1) or {}
            if policy == "i":
                ret, gc = True, 0.0
            elif policy == "ii":
                ret, gc = False, 0.0
            elif policy == "iii":
                ret, gc = g["sim_max_blended"] >= tau, 0.0
            elif policy == "iv":
                p = vb.get("p_store_has_relevant")
                ret, gc = (p is not None and p >= tau), c_gate.get("gate-verbal", 0)
            else:                                    # v, vi
                f = ix.get("fok")
                ret, gc = (f is not None and f >= tau), c_gate.get("gate-indexed", 0)
            state = S0
            if ret:
                state = S1
                if policy == "vi" and tau_nok is not None:
                    nk = ix.get("nok")
                    if nk is not None and nk >= tau_nok:
                        state = S2
            c, f_, n = agg(t, state)
            if c is None:
                continue
            cr.append(c); cf.append(f_)
            cost.append(gc + c_ans.get(state, 0) + (c_ret if ret else 0)
                        + (c_index if policy in ("v", "vi") else 0))
            nret += 1 if ret else 0
        return {"credit": float(np.mean(cr)), "confab": float(np.mean(cf)),
                "cost": float(np.mean(cost)), "retrieval_rate": nret / len(tags),
                "n": len(cr)}

    def sweep(policy, tau_nok=None):
        best, rows = None, []
        for tau in GRID:
            r = simulate(policy, tau, tau_nok)
            r["tau"] = tau
            r["objective"] = r["credit"] / max(r["cost"], 1e-12)
            rows.append(r)
            if best is None or (r["objective"], -r["cost"]) > (best["objective"],
                                                               -best["cost"]):
                best = r
        return best, rows

    fixed = {p: simulate(p, None) for p in ("i", "ii")}
    best_iii, sweep_iii = sweep("iii")
    best_iv, sweep_iv = sweep("iv")
    best_v, sweep_v = sweep("v")

    # tau_NOK: confabulation per dollar on calibration PN items only
    pn = [t for t in tags if items[t]["label_final"] == "PRESENT-NEGATIVE"]
    nok_rows = []
    for tn in GRID:
        cf_, cost_ = [], []
        for t in pn:
            g = gates[t]
            ix = g["indexed"].get("1") or g["indexed"].get(1) or {}
            f = ix.get("fok")
            ret = f is not None and f >= best_v["tau"]
            state = S0
            if ret:
                state = S1
                nk = ix.get("nok")
                if nk is not None and nk >= tn:
                    state = S2
            c, f_, n = agg(t, state)
            if c is None:
                continue
            cf_.append(f_)
            cost_.append(c_gate.get("gate-indexed", 0) + c_ans.get(state, 0)
                         + (c_ret if ret else 0) + c_index)
        nok_rows.append({"tau_NOK": tn, "confab": float(np.mean(cf_)),
                         "cost": float(np.mean(cost_)),
                         "objective": float(np.mean(cf_)) / max(float(np.mean(cost_)), 1e-12),
                         "n_pn": len(cf_)})
    best_nok = min(nok_rows, key=lambda r: (r["objective"], r["cost"]))

    # matched-rate thresholds for the rivals at (v)'s calibration retrieval rate
    target = best_v["retrieval_rate"]

    def matched(policy, rows):
        return min(rows, key=lambda r: (abs(r["retrieval_rate"] - target), r["cost"]))

    m_iii, m_iv = matched("iii", sweep_iii), matched("iv", sweep_iv)

    def simulate_item(policy, tau, t):
        """One item's credit under one policy. Used only to form paired differences."""
        g = gates[t]
        ix = g["indexed"].get("1") or g["indexed"].get(1) or {}
        vb = g["verbal"].get("1") or g["verbal"].get(1) or {}
        if policy == "i":
            ret = True
        elif policy == "ii":
            ret = False
        elif policy == "iii":
            ret = g["sim_max_blended"] >= tau
        elif policy == "iv":
            p_ = vb.get("p_store_has_relevant")
            ret = p_ is not None and p_ >= tau
        else:
            f_ = ix.get("fok")
            ret = f_ is not None and f_ >= tau
        c, _f, _n = agg(t, S1 if ret else S0)
        return c

    # ------- ADJUSTED ESTIMATOR + the frozen hierarchy rule (Amendment 2) -----
    # OLS of the paired difference on persona + coverage-label fixed effects,
    # sum-to-zero coding; the INTERCEPT is the estimate -- the adjusted mean
    # difference at the average persona and average coverage label. Covariates are
    # pre-treatment ONLY: persona and label are fixed by the store and the question
    # before any policy acts. Nothing downstream of the policy may enter.
    personas = sorted({items[t]["persona"] for t in tags})
    labels = sorted({items[t]["label_final"] for t in tags})

    def design(tt):
        X = [[1.0] for _ in tt]
        for j, p_ in enumerate(personas[:-1]):
            for r_, t in zip(X, tt):
                r_.append(1.0 if items[t]["persona"] == p_ else
                          (-1.0 if items[t]["persona"] == personas[-1] else 0.0))
        for j, l_ in enumerate(labels[:-1]):
            for r_, t in zip(X, tt):
                r_.append(1.0 if items[t]["label_final"] == l_ else
                          (-1.0 if items[t]["label_final"] == labels[-1] else 0.0))
        return np.asarray(X)

    def adjusted(pa, ta, pb, tb, subset=None):
        tt, d = [], []
        for t in (subset if subset is not None else tags):
            ra, rb = simulate_item(pa, ta, t), simulate_item(pb, tb, t)
            if ra is not None and rb is not None:
                tt.append(t); d.append(ra - rb)
        if len(tt) < len(personas) + len(labels):
            return float(np.mean(d)) if d else 0.0, tt, d
        X, y = design(tt), np.asarray(d)
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        return float(beta[0]), tt, d

    def boot_se(pa, ta, pb, tb, n=1000, seed=42):
        rng = np.random.default_rng(seed)
        by_p = collections.defaultdict(list)
        for t in tags:
            by_p[items[t]["persona"]].append(t)
        ests = []
        for _ in range(n):
            pick = rng.choice(personas, size=len(personas), replace=True)
            sub = [t for p_ in pick for t in by_p[p_]]
            try:
                e, _tt, dd = adjusted(pa, ta, pb, tb, subset=sub)
                if dd:
                    ests.append(e)
            except Exception:                                     # noqa: BLE001
                continue
        return (float(np.std(ests, ddof=1)) if len(ests) > 1 else 0.0), len(ests)

    contrasts = {
        "H-C1a (v vs i)": ("v", best_v["tau"], "i", None),
        "H-C1b (v vs iv-matched)": ("v", best_v["tau"], "iv", m_iv["tau"]),
        "H-C1b (v vs iii-matched)": ("v", best_v["tau"], "iii", m_iii["tau"]),
    }
    est = {}
    for nm, (pa, ta, pb, tb) in contrasts.items():
        adj, tt, d = adjusted(pa, ta, pb, tb)
        se_cal, nb = boot_se(pa, ta, pb, tb)
        se_eval = se_cal * ((len(tt) / N_EVAL) ** 0.5)
        est[nm] = {"adjusted": adj, "unadjusted": float(np.mean(d)) if d else 0.0,
                   "sd_paired": float(np.std(d, ddof=1)) if len(d) > 1 else 0.0,
                   "n": len(tt), "se_calibration": se_cal,
                   "se_eval_scaled": se_eval, "n_boot": nb}

    N = NormalDist()

    def sup_power(se):
        return 1 - N.cdf((1.96 * se - 0.03) / se) if se > 0 else 1.0

    def ni_power(se, margin=0.03):
        return 1 - N.cdf((1.645 * se - margin) / se) if se > 0 else 1.0

    # H-C1b power = the WEAKER of the two rival contrasts, since H-C1b requires
    # beating BOTH. Using the easier one would overstate the hierarchy's case.
    hc1b_se = max(est["H-C1b (v vs iv-matched)"]["se_eval_scaled"],
                  est["H-C1b (v vs iii-matched)"]["se_eval_scaled"])
    hc1b_power = sup_power(hc1b_se)
    order = (["H-C1a", "H-C1b", "H-C2"] if hc1b_power >= 0.60
             else ["H-C2", "H-C1a", "H-C1b"])
    hierarchy = {
        "rule": "Amendment 2 section 2, frozen before this refit: H-C1b power on "
                "calibration under the adjusted estimator; >=60% keeps the e2-sp1 "
                "ordering, <60% puts H-C2 first. No other ordering available.",
        "hc1b_power": hc1b_power, "threshold": 0.60,
        "se_used": hc1b_se, "se_source": "weaker of the two rival contrasts",
        "verdict": "e2-sp1 ordering stands" if hc1b_power >= 0.60
                   else "H-C2 leads",
        "sequence": order,
    }
    power = {"estimator": "covariate-adjusted paired (persona + coverage-label FE, "
                          "sum-to-zero), persona-clustered bootstrap, 1000, seed 42",
             "contrasts": est,
             "H_C1a_ni_power_margin_0.03":
                 ni_power(est["H-C1a (v vs i)"]["se_eval_scaled"]),
             "H_C1b_power_gate_0.03": hc1b_power,
             "bands_touched": False}

    frozen = {
        "frozen_at": "SP2",
        "split": "calibration only (8 personas, 132 items)",
        "grid": GRID,
        "objective": "behaviour-typed credit / expected serving cost per turn, "
                     "ties to lower cost",
        "tau_sim": best_iii["tau"], "tau_verb": best_iv["tau"],
        "tau_FOK": best_v["tau"], "tau_NOK": best_nok["tau_NOK"],
        "matched_rate_target": target,
        "tau_sim_matched": m_iii["tau"], "tau_verb_matched": m_iv["tau"],
        "k_answer_draws": k_decision,
        "sigma_a_measured": sigma_a, "sigma_a_trigger": SIGMA_TRIGGER,
        "hierarchy": hierarchy,
        "policy_retrieval_rates": {
            "i": fixed["i"]["retrieval_rate"], "ii": fixed["ii"]["retrieval_rate"],
            "iii": best_iii["retrieval_rate"], "iv": best_iv["retrieval_rate"],
            "v": best_v["retrieval_rate"]},
        "retrieval_artifact_sha256": jload(E2 / "retrieval_frozen.json")["artifact_sha256"],
        "cost_model": {"c_gate": c_gate, "c_answer": c_ans,
                       "c_retrieval_query_embed": c_ret,
                       "c_index_maintenance_per_write": c_index,
                       "index_rebuild_seconds_per_store": build_s,
                       "cpu_usd_per_hour": CPU_USD_PER_HOUR},
    }
    jdump(frozen, E2 / "THRESHOLDS_FROZEN.json")
    jdump({"calibration_only": True, "n_items": len(tags),
           "fixed": fixed, "best": {"iii": best_iii, "iv": best_iv, "v": best_v},
           "sweeps": {"iii": sweep_iii, "iv": sweep_iv, "v": sweep_v,
                      "nok": nok_rows},
           "matched": {"iii": m_iii, "iv": m_iv},
           "answer_variance": {"sigma_a": sigma_a, "n_cells": len(cell),
                               "cells_identical_across_draws": identical,
                               "trigger": SIGMA_TRIGGER, "k": k_decision},
           "power": power, "thresholds": frozen},
          E2 / "calibration_report.json")

    print("=" * 92)
    print("CALIBRATION (8 personas, 132 items) -- fitted values")
    print("=" * 92)
    for p, r in fixed.items():
        print(f"  ({p}) {'always' if p=='i' else 'never':7s} credit {r['credit']:.4f} "
              f"confab {r['confab']:.4f} cost ${r['cost']:.6f} rate {r['retrieval_rate']:.2f}")
    for nm, b in (("iii sim", best_iii), ("iv verbal", best_iv), ("v FOK", best_v)):
        print(f"  ({nm:9s}) tau {b['tau']:.2f}  credit {b['credit']:.4f}  "
              f"confab {b['confab']:.4f}  cost ${b['cost']:.6f}  "
              f"rate {b['retrieval_rate']:.2f}")
    print(f"  tau_NOK {best_nok['tau_NOK']:.2f} (confab {best_nok['confab']:.4f} "
          f"on {best_nok['n_pn']} calibration PN items)")
    print(f"  matched-rate target {target:.3f} -> tau_sim {m_iii['tau']:.2f} "
          f"(rate {m_iii['retrieval_rate']:.3f}), tau_verb {m_iv['tau']:.2f} "
          f"(rate {m_iv['retrieval_rate']:.3f})")
    print("\n" + "=" * 92)
    print("ANSWER VARIANCE AND THE k TRIGGER")
    print("=" * 92)
    print(f"  sigma_a measured {sigma_a:.5f}  trigger {SIGMA_TRIGGER}  -> k = {k_decision}")
    print(f"  {identical}/{len(cell)} (item,state) cells identical across 3 draws")
    print("\n" + "=" * 92)
    print("POWER RECOMPUTATION (reported; BANDS UNTOUCHED)")
    print("=" * 92)
    for nm, e in est.items():
        print(f"  {nm:26s} adj {e['adjusted']:+.4f} | unadj {e['unadjusted']:+.4f} | "
              f"paired SD {e['sd_paired']:.4f} | SE_eval {e['se_eval_scaled']:.5f}")
    print(f"  H-C1a non-inferiority power (margin 0.03): "
          f"{power['H_C1a_ni_power_margin_0.03']:.1%}")
    print(f"  H-C1b power at +0.03 (weaker rival): {hc1b_power:.1%}")
    print()
    print("=" * 92)
    print("HIERARCHY RULE — applied, not chosen")
    print("=" * 92)
    print(f"  H-C1b power {hc1b_power:.1%} vs threshold 60.0%  ->  {hierarchy['verdict']}")
    print(f"  SEQUENCE: {' -> '.join(order)}")
    print("\n" + "=" * 92)
    print("COST MODEL (measured)")
    print("=" * 92)
    for k2, v in sorted(c_gate.items()):
        print(f"  {k2:16s} ${v:.6f}/call")
    for k2, v in sorted(c_ans.items()):
        print(f"  answer {k2:12s} ${v:.6f}/call")
    print(f"  index rebuild {build_s*1000:.1f} ms/store -> "
          f"${c_index:.9f}/write at ${CPU_USD_PER_HOUR}/vCPU-hour")
    print(f"\nwrote THRESHOLDS_FROZEN.json and calibration_report.json")


if __name__ == "__main__":
    main()
