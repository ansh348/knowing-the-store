"""
score_e2.py -- E2 scoring. Produces SCORING_MANIFEST.md sections 3.1-3.11, nothing else.

Gates read mechanically. No recommendation is produced anywhere in this file.

Usage:  python e2_metamemory/tools/score_e2.py
"""

from __future__ import annotations

import collections
import hashlib
import itertools
import statistics as st
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"
sys.path.insert(0, str(E1 / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e2_common import E2, S0, S1, S2, jdump, jload, load_items, usd   # noqa: E402
from score_e1 import auroc                                            # noqa: E402

NBOOT, SEED = 1000, 42
GRID = [round(x * 0.05, 2) for x in range(21)]
POLICIES = ("i", "ii", "iii", "iv", "v", "vi", "vii")


def credit_of(label, c):
    if c is None:
        return None
    if label == "ABSENT":
        return 1.0 if c == "ABSTAIN" else 0.0
    return {"CORRECT": 1.0, "PARTIAL": 0.5, "WRONG": 0.0, "ABSTAIN": 0.0}.get(c, 0.0)


def state5(c, confab):
    if c in ("ABSTAIN", None):
        return "abstain" if c == "ABSTAIN" else "judge_error"
    if confab:
        return "confab"
    return {"CORRECT": "correct", "PARTIAL": "partial",
            "WRONG": "wrong_nonconfab"}[c]


# ----------------------------------------------------------------- estimator
def adjusted(d, personas, labels):
    """OLS of the paired difference on persona + coverage-label FE, sum-to-zero.
    The intercept is the estimate."""
    if not d:
        return 0.0
    tt = sorted({p for p, _l, _v in d})
    ll = sorted({l for _p, l, _v in d})
    if len(tt) < 2 or len(ll) < 2:
        return float(np.mean([v for _p, _l, v in d]))
    X, y = [], []
    for p, l, v in d:
        row = [1.0]
        for q in tt[:-1]:
            row.append(1.0 if p == q else (-1.0 if p == tt[-1] else 0.0))
        for m in ll[:-1]:
            row.append(1.0 if l == m else (-1.0 if l == ll[-1] else 0.0))
        X.append(row); y.append(v)
    beta, *_ = np.linalg.lstsq(np.asarray(X), np.asarray(y), rcond=None)
    return float(beta[0])


def boot_ci(d, one_sided=False):
    """Persona-clustered bootstrap over the whole adjustment."""
    rng = np.random.default_rng(SEED)
    by_p = collections.defaultdict(list)
    for p, l, v in d:
        by_p[p].append((p, l, v))
    ps = sorted(by_p)
    est = []
    for _ in range(NBOOT):
        pick = rng.choice(ps, size=len(ps), replace=True)
        sub = [x for q in pick for x in by_p[q]]
        est.append(adjusted(sub, None, None))
    est = np.asarray(est)
    if one_sided:
        return float(np.percentile(est, 5)), None
    return float(np.percentile(est, 2.5)), float(np.percentile(est, 97.5))


def main():
    items = {i["item_id"]: i for i in load_items()}
    ev = [i for i in load_items() if i["split"] == "eval"]
    tags = sorted(i["item_id"] for i in ev)
    thr = jload(E2 / "THRESHOLDS_FROZEN.json")
    g = {r["item_id"]: r for r in jload(E2 / "gates_eval.json")["rows"]}
    ans = jload(E2 / "answers_eval.json")["rows"]
    judg = jload(E2 / "cache" / "judgments_eval.json")
    fr = {r["item_id"]: r for r in jload(E2 / "retrieval_frozen.json")["rows"]}

    cell = {}
    tok = collections.defaultdict(list)
    for a in ans:
        v = judg.get(f"{a['item_id']}|{a['response_sha'][:24]}", {})
        lab = items[a["item_id"]]["label_final"]
        cell[(a["item_id"], a["state"])] = (
            credit_of(lab, v.get("correctness")), bool(v.get("confabulation")),
            state5(v.get("correctness"), bool(v.get("confabulation"))))
        tok[a["state"]].append((a["prompt_tokens"] or 0, a["completion_tokens"] or 0))

    gate_tok = collections.defaultdict(list)
    for r in jload(E2 / "cache" / "responses.json").values():
        a = str(r.get("arm", ""))
        if a.startswith("gate-"):
            gate_tok[a.split("-d")[0]].append((r["prompt_tokens"], r["completion_tokens"]))
    c_gate = {k: usd(sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v))
              for k, v in gate_tok.items()}
    c_ans = {s: usd(sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v))
             for s, v in tok.items()}
    # cached-input variant: E1.8 asymptotic -- indexed gate prefix at 10% of list
    c_gate_cached = dict(c_gate)
    c_gate_cached["gate-indexed"] = c_gate.get("gate-indexed", 0) * 0.399

    def sig(pol, t, draw=1):
        r = g[t]
        ix = r["indexed"].get(str(draw)) or r["indexed"].get(draw) or {}
        vb = r["verbal"].get(str(draw)) or r["verbal"].get(draw) or {}
        if pol == "iii":
            return r["sim_max_blended"]
        if pol == "iv":
            return vb.get("p_store_has_relevant")
        return ix.get("fok")

    TAU = {"iii": thr["tau_sim"], "iv": thr["tau_verb"], "v": thr["tau_FOK"],
           "vi": thr["tau_FOK"]}

    def retrieves(pol, t, tau_override=None, rate_v=None):
        if pol == "i":
            return True
        if pol == "ii":
            return False
        if pol == "vii":
            h = int(hashlib.sha256(f"42|{t}".encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
            return h < rate_v
        tau = tau_override if tau_override is not None else TAU[pol]
        if tau is None:
            return False
        s = sig("v" if pol == "vi" else pol, t)
        return s is not None and s >= tau

    def state_of(pol, t, tau_override=None, rate_v=None):
        if not retrieves(pol, t, tau_override, rate_v):
            return S0
        if pol == "vi":
            nk = (g[t]["indexed"].get("1") or {}).get("nok")
            if thr["tau_NOK"] is not None and nk is not None and nk >= thr["tau_NOK"]:
                return S2
        return S1

    rate_v = sum(1 for t in tags if retrieves("v", t)) / len(tags)

    # ------------------------------------------------------ 3.1 policy table
    def profile(pol, subset=None, tau_override=None, weights=None):
        sub = subset if subset is not None else tags
        cr, cf, cost, cost_c, nret = [], [], [], [], 0
        five = collections.Counter()
        w = []
        for t in sub:
            s = state_of(pol, t, tau_override, rate_v)
            c, f, st5 = cell[(t, s)]
            if c is None:
                continue
            wt = 1.0 if weights is None else weights.get(items[t]["label_final"], 1.0)
            cr.append(c * wt); cf.append((1.0 if f else 0.0) * wt); w.append(wt)
            five[st5] += 1
            gc = (c_gate.get("gate-verbal", 0) if pol == "iv"
                  else c_gate.get("gate-indexed", 0) if pol in ("v", "vi") else 0.0)
            gcc = (c_gate_cached.get("gate-verbal", 0) if pol == "iv"
                   else c_gate_cached.get("gate-indexed", 0) if pol in ("v", "vi") else 0.0)
            cost.append(gc + c_ans.get(s, 0))
            cost_c.append(gcc + c_ans.get(s, 0))
            nret += 1 if s != S0 else 0
        W = sum(w)
        return {"n": len(cr), "retrieval_rate": nret / len(sub),
                "credit": sum(cr) / W, "confab": sum(cf) / W,
                "cost": float(np.mean(cost)), "cost_cached": float(np.mean(cost_c)),
                "five_state": dict(five)}

    table = {p: profile(p) for p in POLICIES}

    # ---------------------------------------------------------- contrasts
    def paired(pa, pb, ta=None, tb=None, subset=None, field="credit"):
        sub = subset if subset is not None else tags
        d = []
        for t in sub:
            sa, sb = state_of(pa, t, ta, rate_v), state_of(pb, t, tb, rate_v)
            ca, cb = cell[(t, sa)], cell[(t, sb)]
            if ca[0] is None or cb[0] is None:
                continue
            va = ca[0] if field == "credit" else (1.0 if ca[1] else 0.0)
            vb = cb[0] if field == "credit" else (1.0 if cb[1] else 0.0)
            d.append((items[t]["persona"], items[t]["label_final"], va - vb))
        return d

    def contrast(pa, pb, ta=None, tb=None, field="credit", one_sided=False):
        d = paired(pa, pb, ta, tb, field=field)
        adj = adjusted(d, None, None)
        unadj = float(np.mean([v for _p, _l, v in d])) if d else 0.0
        lo, hi = boot_ci(d, one_sided)
        return {"adjusted": adj, "unadjusted": unadj, "ci_lo": lo, "ci_hi": hi,
                "n": len(d), "excludes_zero": (None if hi is None
                                               else bool(lo > 0 or hi < 0))}

    res = {"n_eval": len(tags), "rate_v": rate_v, "thresholds": TAU,
           "tau_NOK": thr["tau_NOK"], "policy_table": table}

    # ----------------------------------------- 3.2 gates, frozen sequence
    seq, broken = [], None

    # --- H-C2
    hc2_cf = contrast("vi", "v", field="confab")
    hc2_cr = contrast("vi", "v", field="credit", one_sided=True)
    red = -hc2_cf["adjusted"]
    hc2_hold = (red >= 0.03 and hc2_cf["excludes_zero"] and hc2_cr["ci_lo"] > -0.03)
    hc2_fail = ((red <= 0 and hc2_cf["excludes_zero"])
                or (hc2_cr["adjusted"] < -0.03 and hc2_cr["ci_lo"] < -0.03
                    and hc2_cr["ci_hi"] is not None))
    hc2 = {"step": 1, "name": "H-C2", "contrast": "(vi) vs (v)",
           "confab_reduction_pp": red * 100, "confab": hc2_cf,
           "credit_noninferiority": hc2_cr,
           "verdict": "HOLDS" if hc2_hold else ("FAILS" if hc2_fail else "INDETERMINATE")}
    seq.append(hc2)
    if hc2["verdict"] != "HOLDS":
        broken = "H-C2"

    # --- H-C1a
    hc1a_cr = contrast("v", "i", field="credit", one_sided=True)
    hc1a_hold = (table["v"]["retrieval_rate"] <= 0.80 and hc1a_cr["ci_lo"] > -0.03)
    hc1a_fail = (table["v"]["retrieval_rate"] > 0.95 or hc1a_cr["ci_lo"] <= -0.03)
    hc1a = {"step": 2, "name": "H-C1a", "contrast": "(v) vs (i)",
            "retrieval_rate": table["v"]["retrieval_rate"], "credit": hc1a_cr,
            "verdict": "HOLDS" if hc1a_hold else ("FAILS" if hc1a_fail else "INDETERMINATE"),
            "exploratory": broken is not None,
            "label": f"EXPLORATORY (sequence broken at {broken})" if broken else None}
    seq.append(hc1a)
    if broken is None and hc1a["verdict"] != "HOLDS":
        broken = "H-C1a"

    # --- H-C1b, matched rows
    cal = jload(E2 / "calibration_report_v4.json")
    matched_tau = {"iii": 0.40, "iv": 0.75}
    hc1b_rows = {}
    for riv, tv in matched_tau.items():
        r_rate = sum(1 for t in tags if retrieves(riv, t, tau_override=tv)) / len(tags)
        gap = abs(r_rate - table["v"]["retrieval_rate"])
        c = contrast("v", riv, None, tv, field="credit")
        hc1b_rows[riv] = {"matched_tau": tv, "realised_rate": r_rate,
                          "rate_gap": gap, "matched_within_0.02": gap <= 0.02,
                          **c,
                          "row_status": "VOID (unmatched)" if gap > 0.02 else "matched"}
    valid = [r for r in hc1b_rows.values() if r["matched_within_0.02"]]
    if not valid:
        hc1b_verdict = "VOID — no rival row met the ±0.02 matching tolerance"
    else:
        hold = all(r["adjusted"] >= 0.03 and r["excludes_zero"] for r in valid)
        fail = any(r["adjusted"] <= 0 and r["excludes_zero"] for r in valid)
        hc1b_verdict = "HOLDS" if hold else ("FAILS" if fail else "INDETERMINATE")
    hc1b = {"step": 3, "name": "H-C1b", "rows": hc1b_rows, "verdict": hc1b_verdict,
            "exploratory": broken is not None,
            "label": f"EXPLORATORY (sequence broken at {broken})" if broken else None}
    seq.append(hc1b)
    res["gates"] = seq
    res["sequence_broken_at"] = broken

    # ------------------------------------------- 3.3 attribution control
    res["attribution_vii"] = {
        "credit": contrast("v", "vii", field="credit"),
        "confab": contrast("v", "vii", field="confab"),
        "rate_v": table["v"]["retrieval_rate"],
        "rate_vii": table["vii"]["retrieval_rate"]}

    # --------------------------------- 3.4 risk-coverage / operating points
    curve = []
    for tau in GRID:
        p = profile("v", tau_override=tau)
        curve.append({"tau": tau, "rate": p["retrieval_rate"], "credit": p["credit"],
                      "confab": p["confab"], "cost": p["cost"],
                      "cost_cached": p["cost_cached"]})
    res["risk_coverage_v"] = curve

    # ------------------------------------------------ 3.5 secondaries
    full = [t for t in tags if items[t]["variant"] == "FULL"]
    res["secondary_full_only"] = {p: profile(p, subset=full) for p in POLICIES}
    base = collections.Counter(items[t]["label_final"] for t in tags)
    for share in (0.10, 0.25, 0.40):
        n_abs = base["ABSENT"]
        w_abs = (share / (1 - share)) * ((len(tags) - n_abs) / n_abs)
        w = {"ABSENT": w_abs, "PRESENT": 1.0, "PRESENT-NEGATIVE": 1.0}
        res[f"reweighted_absence_{int(share*100)}"] = {
            p: profile(p, weights=w) for p in POLICIES}
    res["natural_absence_share"] = base["ABSENT"] / len(tags)

    # oracle ceiling: TRUE index gate (E1 INDEXED-TRUE signal) at the same tau
    e1t = {r["tag"]: r for r in jload(E1 / "elicitation_main.json")
           if r["arm"] == "INDEXED-TRUE" and r["status"] == "OK"}
    cr_o, n_o = [], 0
    for t in tags:
        f = (e1t.get(t) or {}).get("fok")
        s = S1 if (f is not None and f >= TAU["v"]) else S0
        c = cell[(t, s)][0]
        if c is not None:
            cr_o.append(c); n_o += 1 if s == S1 else 0
    res["oracle_ceiling_TRUE_index"] = {"credit": float(np.mean(cr_o)),
                                        "retrieval_rate": n_o / len(tags),
                                        "label": "oracle ceiling; gates nothing"}

    # ------------------------------------- 3.6 registered descriptives
    def med(vals):
        return float(st.median(vals)) if vals else None
    probe = [t for t in tags if str(items[t]["question_id"]).startswith("probe")]
    abl = [t for t in tags if items[t]["label_final"] == "ABSENT" and t not in probe]
    pres = [t for t in tags if items[t]["label_final"] == "PRESENT"]
    res["descriptive_1_retrieval_confidence"] = {
        "median_max_blended_probe": med([fr[t]["max_blended"] for t in probe]),
        "median_max_blended_PRESENT": med([fr[t]["max_blended"] for t in pres]),
        "median_max_blended_ablation_ABSENT": med([fr[t]["max_blended"] for t in abl]),
        "calibration_reference": {"probe": 0.771, "PRESENT": 0.394}}
    res["descriptive_2_near_miss"] = {
        "S1_confab_ablation": float(np.mean([1.0 if cell[(t, S1)][1] else 0.0 for t in abl])),
        "S1_confab_probe": float(np.mean([1.0 if cell[(t, S1)][1] else 0.0 for t in probe])),
        "S0_credit_ablation": float(np.mean([cell[(t, S0)][0] for t in abl])),
        "S1_credit_ablation": float(np.mean([cell[(t, S1)][0] for t in abl])),
        "S0_credit_probe": float(np.mean([cell[(t, S0)][0] for t in probe])),
        "S1_credit_probe": float(np.mean([cell[(t, S1)][0] for t in probe]))}
    wP = len(pres) / len(tags)
    wN = sum(1 for t in tags if items[t]["label_final"] == "PRESENT-NEGATIVE") / len(tags)
    wA = len(probe + abl) / len(tags)
    s1p = float(np.mean([cell[(t, S1)][0] for t in pres]))
    s1n = float(np.mean([cell[(t, S1)][0] for t in tags
                         if items[t]["label_final"] == "PRESENT-NEGATIVE"]))
    s0a = float(np.mean([cell[(t, S0)][0] for t in probe + abl]))
    s1a = float(np.mean([cell[(t, S1)][0] for t in probe + abl]))
    res["descriptive_3_headroom"] = {
        "never": wA * s0a, "always": wP * s1p + wN * s1n + wA * s1a,
        "oracle": wA * max(s0a, s1a) + wP * max(0, s1p) + wN * max(0, s1n),
        "headroom": (wA * max(s0a, s1a) + wP * max(0, s1p) + wN * max(0, s1n)) - wA * s0a,
        "captured_by_v": table["v"]["credit"] - wA * s0a}
    res["descriptive_4_capability"] = {
        "note": "calibration-only; eval has one answerer by design",
        "calibration": {"near_miss_confab_mini": 0.471, "near_miss_confab_gpt54": 0.706,
                        "always_credit_mini": 0.4583, "always_credit_gpt54": 0.4356,
                        "oracle_mini": 0.6553, "oracle_gpt54": 0.7538}}

    # ------------------------------------------------- 3.7 H-C3 flip rate
    def flip(pol, tau):
        n_flip = 0
        for t in tags:
            dec = set()
            for d in (1, 2, 3):
                s = sig(pol, t, d)
                dec.add(bool(s is not None and s >= tau))
            n_flip += 1 if len(dec) > 1 else 0
        return n_flip / len(tags)
    res["H_C3"] = {"flip_indexed_v": flip("v", TAU["v"]),
                   "flip_verbal_iv": flip("iv", 0.20),
                   "note": "verbal evaluated at the same 0.20 cut since its derived "
                           "point is undefined; exploratory, no gate",
                   "prediction": "flip(v) < flip(iv)"}
    res["H_C3"]["prediction_holds"] = (res["H_C3"]["flip_indexed_v"]
                                       < res["H_C3"]["flip_verbal_iv"])

    # ------------------------------------------------------- 3.8 P5
    p5 = jload(E2 / "p5_spotcheck_gpt-5.6-sol.json")
    fro = collections.defaultdict(list)
    for r in p5["rows"]:
        if r["status"] == "OK":
            v = r["p_store_has_relevant"] if r["arm"] == "gate-verbal" else r["fok"]
            if v is not None:
                fro[(r["item_id"], r["arm"])].append(v)
    cellset = [t for t in {k[0] for k in fro} if t in set(tags)]
    def payoff(gate_fn, sub):
        cr_g, cr_i = [], []
        for t in sub:
            s = S1 if gate_fn(t) else S0
            if cell[(t, s)][0] is None:
                continue
            cr_g.append(cell[(t, s)][0]); cr_i.append(cell[(t, S1)][0])
        return float(np.mean(cr_g) - np.mean(cr_i)) if cr_g else None
    fro_mean = {k: float(np.mean(v)) for k, v in fro.items()}
    p_mini = payoff(lambda t: retrieves("v", t), cellset)
    p_fro = payoff(lambda t: fro_mean.get((t, "gate-indexed-believed"), 0) >= TAU["v"],
                   cellset)
    cf_v, cf_vi = [], []
    for t in cellset:
        ret = fro_mean.get((t, "gate-indexed-believed"), 0) >= TAU["v"]
        sv = S1 if ret else S0
        nk = (g[t]["indexed"].get("1") or {}).get("nok")
        svi = (S2 if (ret and nk is not None and nk >= thr["tau_NOK"]) else sv)
        cf_v.append(1.0 if cell[(t, sv)][1] else 0.0)
        cf_vi.append(1.0 if cell[(t, svi)][1] else 0.0)
    res["P5"] = {"model": p5["model"], "k": p5["k"], "n_cell_items": len(cellset),
                 "n_registered_cell": p5["n_items"],
                 "payoff_mini": p_mini, "payoff_frontier": p_fro,
                 "P5a_band": "payoff_frontier <= 0.5 * payoff_mini",
                 "P5a": ("HOLDS" if (p_fro is not None and p_mini is not None
                                     and p_fro <= 0.5 * p_mini) else "FAILS"),
                 "confab_vi_minus_v": float(np.mean(cf_vi) - np.mean(cf_v)),
                 "P5b_band": "point estimate negative (direction preserved)",
                 "P5b": ("HOLDS" if float(np.mean(cf_vi) - np.mean(cf_v)) < 0 else "FAILS"),
                 "P5b_note": "direction only; explicitly under-powered; a sign check, "
                             "not a test"}

    # ------------------------------------------------------- 3.9 M1
    m1 = jload(E2 / "m1_factorial_raw.json")["rows"]
    blind = {r["question"]: r for r in jload(E1 / "elicitation_main.json")
             if r["arm"] == "BLIND" and r["status"] == "OK"}
    qmap = {r["tag"]: r["question"] for r in jload(E1 / "elicitation_main.json")
            if r["arm"] != "BLIND"}
    frb = [i for i in load_items()]
    y_all = {i["item_id"]: (1 if i["label_final"] == "PRESENT-NEGATIVE" else 0)
             for i in frb}
    bl_nok, bl_y = [], []
    for i in frb:
        q = qmap.get(i["item_id"])
        if q in blind and blind[q].get("nok") is not None:
            bl_nok.append(blind[q]["nok"]); bl_y.append(y_all[i["item_id"]])
    blind_auroc = auroc(bl_nok, bl_y)
    cells8 = {}
    for c in sorted({r["cell"] for r in m1}):
        rows = [r for r in m1 if r["cell"] == c and r["nok"] is not None]
        cells8[c] = {"auroc": auroc([r["nok"] for r in rows],
                                    [y_all[r["item_id"]] for r in rows]),
                     "n": len(rows)}
        cells8[c]["delta_over_blind"] = cells8[c]["auroc"] - blind_auroc
    def eff(mask):
        pos = [v["auroc"] for k, v in cells8.items() if mask(k) > 0]
        neg = [v["auroc"] for k, v in cells8.items() if mask(k) < 0]
        return float(np.mean(pos) - np.mean(neg))
    L = lambda k: 1 if k[1] == "1" else -1          # noqa: E731
    W = lambda k: 1 if k[3] == "1" else -1          # noqa: E731
    D = lambda k: 1 if k[5] == "1" else -1          # noqa: E731
    res["M1"] = {
        "blind_nok_auroc": blind_auroc, "cells": cells8,
        "main_effects": {"L": eff(L), "W": eff(W), "D": eff(D)},
        "interactions": {
            "LxW": eff(lambda k: L(k) * W(k)), "LxD": eff(lambda k: L(k) * D(k)),
            "WxD": eff(lambda k: W(k) * D(k)),
            "LxWxD": eff(lambda k: L(k) * W(k) * D(k))},
        "E1_reference_delta": 0.2393, "E0_reference_delta": 0.0411}
    alloff = cells8["L0W0D0"]["delta_over_blind"]
    res["M1"]["P_M1c_validity"] = {
        "all_off_delta": alloff, "E0_target": 0.0411, "band": 0.06,
        "holds": abs(alloff - 0.0411) <= 0.06}
    me = res["M1"]["main_effects"]
    res["M1"]["P_M1a"] = {"L_largest": abs(me["L"]) >= max(abs(me["W"]), abs(me["D"])),
                          "effects": me}
    res["M1"]["P_M1b"] = {"LxD_positive": res["M1"]["interactions"]["LxD"] > 0,
                          "value": res["M1"]["interactions"]["LxD"]}

    # ------------------------------------------------------- 3.10 M2
    m2 = jload(E2 / "m2_renderer_raw.json")["rows"]
    ext = [i for i in load_items()] + []
    allit = {i["item_id"]: i for i in jload(E1 / "build" / "items_final.json")
             if i["backend"] in ("amem", "mem0")
             and i.get("label", i["label_pre"]) in
             {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}}
    y_ext = {k: (0 if v.get("label", v["label_pre"]) == "ABSENT" else 1)
             for k, v in allit.items()}
    e1_true = {r["tag"]: r for r in jload(E1 / "elicitation_main.json")
               if r["arm"] == "INDEXED-TRUE" and r["status"] == "OK"}
    runb = {r["item_id"]: r for r in jload(E1 / "run_b_nomarker.json")["rows"]}
    m2cells = collections.defaultdict(dict)
    for r in m2:
        m2cells[r["cell"]][r["item_id"]] = r["fok"]
    m2cells["marked"] = {k: v["fok"] for k, v in e1_true.items() if k in allit}
    m2cells["marker-omitted"] = {k: v["fok"] for k, v in runb.items() if k in allit}
    m2res = {}
    for be in ("amem", "mem0"):
        ids = [k for k, v in allit.items() if v["backend"] == be]
        bl = []
        for k in ids:
            q = qmap.get(k)
            bl.append(blind[q]["fok"] if q in blind else None)
        ok = [i for i, x in enumerate(bl) if x is not None]
        b_auroc = auroc([bl[i] for i in ok], [y_ext[ids[i]] for i in ok])
        m2res[be] = {"blind_auroc": b_auroc, "cells": {}}
        for cname in ("marked", "marker-omitted", "a3-style", "minimal"):
            vv = [(k, m2cells[cname][k]) for k in ids
                  if k in m2cells[cname] and m2cells[cname][k] is not None]
            if not vv:
                continue
            a = auroc([x for _k, x in vv], [y_ext[k] for k, _x in vv])
            m2res[be]["cells"][cname] = {"auroc": a, "delta": a - b_auroc, "n": len(vv)}
    order_ok = all(
        m2res[b]["cells"]["minimal"]["delta"] > m2res[b]["cells"]["marker-omitted"]["delta"]
        > m2res[b]["cells"]["marked"]["delta"] for b in ("amem", "mem0"))
    res["M2"] = {"by_backend": m2res,
                 "P_M2a_ordering_minimal_gt_omitted_gt_marked": order_ok,
                 "P_M2b_minimal_delta_ge_0": all(
                     m2res[b]["cells"]["minimal"]["delta"] >= 0 for b in ("amem", "mem0"))}

    # ------------------------------------------------------- 3.11 economics
    res["economics"] = {"c_gate": c_gate, "c_gate_cached": c_gate_cached,
                        "c_answer": c_ans,
                        "index_maintenance_per_write": thr["cost_model"].get(
                            "c_index_maintenance_per_write"),
                        "per_1M_calls": {p: table[p]["cost"] * 1e6 for p in POLICIES},
                        "per_1M_calls_cached": {p: table[p]["cost_cached"] * 1e6
                                                for p in POLICIES}}

    jdump(res, E2 / "results" / "e2_scores.json")
    print("wrote results/e2_scores.json")
    return res


if __name__ == "__main__":
    main()
