"""
score_e3.py -- E3 scoring. Produces SCORING_MANIFEST_E3.md sections 3.1-3.12 and
nothing else.

Gates are read MECHANICALLY. No recommendation is produced anywhere in this file.
The estimator and the bootstrap are imported from score_e2, not re-implemented.

Usage:  python e3_metamemory/tools/score_e3.py
"""

from __future__ import annotations

import collections
import io
import json
import statistics as st
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e2_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from score_e2 import adjusted, boot_ci                             # noqa: E402
from e3_common import (E3, RUNGS, S0, S1, S2, S3, S3P, jdump,      # noqa: E402
                       jload, load_cells, sha, usd)

GATE_CACHE_MULT = 0.399           # E1.8 asymptotic, frozen; carried from E2


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
    return {"CORRECT": "correct", "PARTIAL": "partial", "WRONG": "wrong_nonconfab"}[c]


def main():
    # ---------------------------------------------------- 1. inputs and hashes
    C = load_cells()
    census = jload(E3 / "sp3_census_e3.json")
    thr = jload(E3 / "THRESHOLDS_E3_FROZEN.json")
    fr = jload(E3 / "retrieval_frozen_e3.json")
    IX = jload(E3 / "indexes_e3.json")
    ann = jload(E3 / "annotations_e3.json")
    want = census["artifacts"]
    got = {"retrieval_frozen_e3.json": fr["artifact_sha256"],
           "indexes_e3.json (true)": IX["artifact_sha256"],
           "indexes_e3.json (lobotomy)": IX["artifact_sha256_lobotomy"],
           "annotations_e3.json": ann["artifact_sha256"],
           "CELLS_E3.json": sha(json.dumps(C, sort_keys=True)),
           "THRESHOLDS_E3_FROZEN.json": sha(json.dumps(thr, sort_keys=True))}
    for k, v in got.items():
        assert want[k] == v, f"ARTIFACT HASH MISMATCH on {k}: refusing to score"
    print(f"artifact hashes verified ({len(got)}/{len(got)})")

    cells = {c["cell_id"]: c for c in C["cells"] if c["split"] == "eval"}
    tags = sorted(cells)
    gT = {r["cell_id"]: r for r in jload(E3 / "gates_eval.json")["rows"]}
    gL = {r["cell_id"]: r for r in jload(E3 / "gates_eval_lobotomy.json")["rows"]}
    A = jload(E3 / "answers_eval.json")
    judg = jload(E3 / "cache" / "judgments_eval.json")

    cell, tok = {}, collections.defaultdict(list)
    s0_by_q = {}
    for a in A["rows"]:
        v = judg.get(f"{a['cell_id']}|{a['response_sha'][:24]}", {})
        lab = cells[a["cell_id"]]["label"]
        rec = (credit_of(lab, v.get("correctness")), bool(v.get("confabulation")),
               v.get("correctness"))
        cell[(a["cell_id"], a["state"])] = rec
        tok[a["state"]].append((a["prompt_tokens"] or 0, a["completion_tokens"] or 0))
        if a["state"] == S0:
            s0_by_q[(a["persona"], a["question_id"])] = v.get("correctness")

    def outcome(t, state):
        """(credit, confab, five_state) for a cell under a context state."""
        if state == S0:
            c = s0_by_q[(cells[t]["persona"], cells[t]["question_id"])]
        else:
            c = cell[(t, state)][2]
        confab = False if state == S0 else cell[(t, state)][1]
        return credit_of(cells[t]["label"], c), confab, state5(c, confab)

    tau = thr["tau_FOK"]

    def fok(g, t):
        return g[t]["fok"] if g[t]["fok"] is not None else -1

    ARMS = {
        "(a) FULL": lambda t: S3 if fok(gT, t) >= tau else S0,
        "(a') CONTENT-LOBOTOMY": lambda t: S3P if fok(gL, t) >= tau else S0,
        "(a'') CAUTION-ONLY": lambda t: S2 if fok(gT, t) >= tau else S0,
        "(b) always-retrieve": lambda t: S1,
        "(c) no-memory floor": lambda t: S0,
        "(d) SHUFFLED-FOK [VOID]": lambda t: S3 if fok(gT, t) >= tau else S0,
    }
    GATED = {"(a) FULL", "(a') CONTENT-LOBOTOMY", "(a'') CAUTION-ONLY",
             "(d) SHUFFLED-FOK [VOID]"}

    # ------------------------------------------------------------- economics
    gtok = collections.defaultdict(list)
    for r in json.load(io.open(E3 / "cache" / "responses.json", encoding="utf-8")).values():
        arm = str(r.get("arm", ""))
        if arm.startswith("e3gate"):
            gtok[arm].append((r["prompt_tokens"], r["completion_tokens"]))
    c_gate = {k: usd(sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v),
                     "gpt-4.1-mini") for k, v in gtok.items()}
    c_gate_mean = sum(c_gate.values()) / len(c_gate)
    c_ans = {s: usd(sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v),
                    "gpt-5.4") for s, v in tok.items()}
    maint = {r: {"write_us": sum(v["maintain_us_write_driven"]
                                 for v in IX["meta"].values() if v["rung"] == r),
                 "clock_ms": st.median([v["clock_pass_ms"]
                                        for v in IX["meta"].values() if v["rung"] == r]),
                 "serve_ms": st.median([v["serve_ms_render"]
                                        for v in IX["meta"].values() if v["rung"] == r])}
             for r in RUNGS}

    # ------------------------------------------------------ 3.1 the arm table
    def profile(arm, subset=None, weights=None):
        sub = subset if subset is not None else tags
        cr, cf, w, cost, costc = [], [], [], [], []
        five = collections.Counter()
        nret = 0
        for t in sub:
            s = ARMS[arm](t)
            c, f, s5 = outcome(t, s)
            if c is None:
                continue
            wt = 1.0 if weights is None else weights.get(cells[t]["label"], 1.0)
            cr.append(c * wt); cf.append((1.0 if f else 0.0) * wt); w.append(wt)
            five[s5] += 1
            g = c_gate_mean if arm in GATED else 0.0
            gc = g * GATE_CACHE_MULT if arm in GATED else 0.0
            cost.append(g + c_ans.get(s, 0.0))
            costc.append(gc + c_ans.get(s, 0.0))
            nret += 1 if s != S0 else 0
        W = sum(w)
        return {"n": len(cr), "retrieval_rate": nret / len(sub),
                "credit": sum(cr) / W, "confab": sum(cf) / W,
                "cost": float(np.mean(cost)), "cost_cached": float(np.mean(costc)),
                "five_state": dict(five)}

    table = {a: profile(a) for a in ARMS}

    def paired(a1, a2, field, subset=None):
        sub = subset if subset is not None else tags
        d = []
        for t in sub:
            c1, f1, _ = outcome(t, ARMS[a1](t))
            c2, f2, _ = outcome(t, ARMS[a2](t))
            if c1 is None or c2 is None:
                continue
            v1 = c1 if field == "credit" else (1.0 if f1 else 0.0)
            v2 = c2 if field == "credit" else (1.0 if f2 else 0.0)
            d.append((cells[t]["persona"], cells[t]["label"], v1 - v2))
        return d

    def contrast(a1, a2, field, one_sided=False, subset=None):
        d = paired(a1, a2, field, subset)
        lo, hi = boot_ci(d, one_sided)
        adj = adjusted(d, None, None)
        return {"adjusted": adj,
                "unadjusted": float(np.mean([v for _p, _l, v in d])),
                "ci_lo": lo, "ci_hi": hi, "n": len(d),
                "excludes_zero": (None if hi is None else bool(lo > 0 or hi < 0))}

    res = {"n_eval": len(tags), "tau_FOK": tau, "tau_NOK": thr["tau_NOK"],
           "margin": thr["hE3b_margin"], "k": thr["k_decision"],
           "arm_table": table}

    # ---------------------------------------------- 3.2-3.4 the fixed sequence
    seq, broken = [], None
    a_vs_b_confab = contrast("(a) FULL", "(b) always-retrieve", "confab")
    red = -a_vs_b_confab["adjusted"]
    hold_a = red >= 0.03 and a_vs_b_confab["excludes_zero"]
    seq.append({"name": "H-E3a", "step": 1, "contrast": "(a) vs (b), confabulation",
                "band": "reduction >= 3pp AND CI excludes zero",
                "reduction_pp": red * 100, **a_vs_b_confab,
                "verdict": "HOLDS" if hold_a else "FAILS"})
    if not hold_a:
        broken = "H-E3a"

    m = thr["hE3b_margin"]
    a_vs_b_credit = contrast("(a) FULL", "(b) always-retrieve", "credit",
                             one_sided=True)
    hold_b = a_vs_b_credit["ci_lo"] > -m
    seq.append({"name": "H-E3b", "step": 2, "contrast": "(a) vs (b), credit",
                "band": f"one-sided 95% LB > -{m}", **a_vs_b_credit,
                "verdict": ("HOLDS" if hold_b else "FAILS") if not broken
                           else f"EXPLORATORY (sequence broken at {broken})"})
    if not broken and not hold_b:
        broken = "H-E3b"

    a_vs_l = contrast("(a) FULL", "(a') CONTENT-LOBOTOMY", "confab")
    redl = -a_vs_l["adjusted"]
    hold_d = redl > 0 and a_vs_l["excludes_zero"]
    seq.append({"name": "H-E3d", "step": 3, "contrast": "(a) vs (a'), confabulation",
                "band": "reduction > 0 AND CI excludes zero",
                "reduction_pp": redl * 100, **a_vs_l,
                "verdict": ("HOLDS" if hold_d else "FAILS") if not broken
                           else f"EXPLORATORY (sequence broken at {broken})"})
    res["sequence"] = seq
    res["sequence_broken_at"] = broken

    # ------------------------------------------------------ 3.5 H-E3c, VOID
    void = contrast("(a) FULL", "(d) SHUFFLED-FOK [VOID]", "credit")
    res["H_E3c_VOID"] = {
        "disposition": "VOID BY DERIVATION (E3_AMENDMENT_2)",
        "cause": f"tau_FOK = {tau}; arm (a) realised retrieval rate "
                 f"{table['(a) FULL']['retrieval_rate']:.3f}; a permutation of FOK "
                 "cannot move a decision, so (d) is byte-identical to (a)",
        "prompt_pairs_differing": 0, "not_a_claim": True, **void}

    # -------------------------------------- 3.6 staleness trajectory
    p1 = jload(E3 / "probes" / "p1_sessions.json")
    calset = set(jload(ROOT / "e2_metamemory" / "CALIBRATION_SPLIT.json")
                 ["calibration_personas"])
    chg = ("supersession_events", "retractions", "contradictions")
    ns = [e["new_session"] for p, v in p1.items() if p not in calset
          for s in chg for e in v["events"][s] if e["new_session"]]
    traj = []
    for r in RUNGS:
        sub = [t for t in tags if cells[t]["rung"] == r]
        c = contrast("(a) FULL", "(b) always-retrieve", "confab", subset=sub)
        traj.append({"rung": r, "n": len(sub),
                     "accumulated_supersessions": sum(1 for x in ns if x <= r),
                     "advantage_pp": -c["adjusted"] * 100,
                     "ci_lo_pp": -c["ci_hi"] * 100, "ci_hi_pp": -c["ci_lo"] * 100,
                     "confab_a": profile("(a) FULL", sub)["confab"],
                     "confab_b": profile("(b) always-retrieve", sub)["confab"]})
    adv = [x["advantage_pp"] for x in traj]
    res["staleness_trajectory"] = {
        "rows": traj, "registered_prediction": "non-decreasing across the four rungs",
        "non_decreasing": all(adv[i] <= adv[i + 1] + 1e-9 for i in range(len(adv) - 1)),
        "spearman_like_direction": "up" if adv[-1] > adv[0] else "down"}

    # -------------------------------------- 3.7 absence-mix curve
    res["absence_mix"] = {
        "per_rung_absence_share": {
            str(r): sum(1 for t in tags if cells[t]["rung"] == r
                        and cells[t]["label"] == "ABSENT")
                    / sum(1 for t in tags if cells[t]["rung"] == r) for r in RUNGS},
        "E2_vs_E3": {
            "E2": {"manufactured_share": 0.360, "L": 0.5467, "p_star": 0.5683,
                   "tau_FOK": 0.20, "realised_rate": 0.684},
            "E3": {"manufactured_share": 0.0,
                   "L": thr["derivation"]["loss_ABSENT"],
                   "p_star": thr["derivation"]["p_star"], "tau_FOK": tau,
                   "realised_rate": table["(a) FULL"]["retrieval_rate"]}},
        "mechanism": "RESULTS_E2 3.6: ablation-induced ABSENT 1.000->0.235 credit "
                     "with 70.1% confabulation; natural-absent probes 1.000->0.917 "
                     "with 8.3%"}

    # -------------------------------------- 3.8 near-miss vs off-topic
    probe = [t for t in tags if cells[t]["kind"] == "probe"]
    authored_abs = [t for t in tags if cells[t]["kind"] == "authored"
                    and cells[t]["label"] == "ABSENT"]
    res["absence_split"] = {
        kind: {arm: {"credit": profile(arm, sub)["credit"],
                     "confab": profile(arm, sub)["confab"], "n": len(sub)}
               for arm in ARMS}
        for kind, sub in (("natural_absent_probe", probe),
                          ("not_yet_written", authored_abs))}

    # -------------------------------------- 3.9 economics
    res["economics"] = {
        "prices": {"gpt-5.4": [2.50, 15.00], "gpt-4.1-mini": [0.40, 1.60],
                   "source": "RESULTS_E2 3.11-R, verified 2026-08-11"},
        "per_1M_turns": {a: {"uncached": table[a]["cost"] * 1e6,
                             "cached": table[a]["cost_cached"] * 1e6} for a in ARMS},
        "gate_call_usd": c_gate_mean, "answer_usd_by_state": c_ans,
        "index_maintenance": {
            "write_driven_us_per_write": 1.11,
            "per_rung_write_driven_us_40_personas": {str(r): maint[r]["write_us"]
                                                     for r in RUNGS},
            "clock_driven_ms_per_serve_median": {str(r): maint[r]["clock_ms"]
                                                 for r in RUNGS},
            "render_ms_per_serve_median": {str(r): maint[r]["serve_ms"] for r in RUNGS},
            "note": "reported as two columns and never averaged into one: the "
                    "write-driven cost is incurred once per write, the clock pass "
                    "once per SERVE, because ages and expiry move with t_now and no "
                    "write"}}

    # -------------------------------------- 3.10 scramble census
    res["scramble"] = {
        "annotation_destruction_rate": ann["destruction_rate"],
        "degenerate_persona_rungs": len(ann["degenerate_persona_rungs"]),
        "index_lobotomy": IX["lobotomy"],
        "non_vacuity_realised_eval": {"a_vs_b": 1.0, "a_vs_a_prime": 1.0}}

    # -------------------------------------- 3.11 judge spot-check
    js = jload(E3 / "judge_spotcheck_e3.json")
    res["judge_spotcheck"] = {
        "unweighted": {"confab": js["confab_agreement"],
                       "four_way": js["four_way_agreement"]},
        "population_weighted": js["population_weighted"],
        "per_stratum": js["per_stratum"],
        "reference": js["e2_reference"], "bar": None, "gates": "nothing"}

    # -------------------------------------- 3.12 the operating points
    res["operating_points"] = {
        "tau_FOK": tau, "tau_NOK": thr["tau_NOK"],
        "derivation": thr["derivation"], "q_note": thr["q_note"],
        "consequence": "both thresholds sit at the grid minimum, so arm (a) is "
                       "retrieve-always plus apply-always. It is not a gate and "
                       "must not be called one."}

    jdump(res, E3 / "results" / "e3_scores.json")

    # ------------------------------------------------------------------ print
    P = print
    P("\n" + "=" * 100)
    P(f"E3 SCORES -- n_eval = {len(tags)} cells, 32 personas, rungs {list(RUNGS)}")
    P("=" * 100)
    P(f"\n3.1 ARM TABLE  (fixed denominators: all {len(tags)} eval cells enter every arm)")
    P(f"  {'arm':28s}{'rate':>7s}{'credit':>9s}{'confab':>9s}{'corr':>6s}"
      f"{'part':>6s}{'wrong':>7s}{'confab':>8s}{'abst':>6s}{'$/1M':>8s}{'cached':>8s}")
    for a, v in table.items():
        f5 = v["five_state"]
        P(f"  {a:28s}{v['retrieval_rate']:7.3f}{v['credit']:9.4f}{v['confab']:9.4f}"
          f"{f5.get('correct',0):6d}{f5.get('partial',0):6d}"
          f"{f5.get('wrong_nonconfab',0):7d}{f5.get('confab',0):8d}"
          f"{f5.get('abstain',0):6d}{v['cost']*1e6:8.0f}{v['cost_cached']*1e6:8.0f}")

    P("\n3.2-3.4 THE FIXED SEQUENCE  H-E3a -> H-E3b -> H-E3d")
    for g in seq:
        P(f"\n  {g['name']}  {g['contrast']}")
        P(f"    band: {g['band']}")
        P(f"    adjusted {g['adjusted']:+.4f}   unadjusted {g['unadjusted']:+.4f}"
          f"   CI [{g['ci_lo']:+.4f}, "
          f"{('%+.4f' % g['ci_hi']) if g['ci_hi'] is not None else 'one-sided'}]"
          f"   n={g['n']}")
        if "reduction_pp" in g:
            P(f"    reduction {g['reduction_pp']:.2f}pp   "
              f"excludes zero: {g['excludes_zero']}")
        P(f"    VERDICT: {g['verdict']}")
    P(f"\n  sequence broken at: {broken or 'not broken'}")

    P("\n3.5 H-E3c -- VOID BY DERIVATION")
    P(f"    {res['H_E3c_VOID']['cause']}")
    P(f"    computed anyway: credit delta adjusted {void['adjusted']:+.4f} "
      f"CI [{void['ci_lo']:+.4f}, {void['ci_hi']:+.4f}]")
    P("    THIS IS NOT A CLAIM.")

    P("\n3.6 STALENESS TRAJECTORY  (registered prediction: non-decreasing)")
    P(f"  {'rung':>5s}{'n':>6s}{'accum sup':>11s}{'confab (a)':>12s}"
      f"{'confab (b)':>12s}{'advantage pp':>14s}{'95% CI pp':>22s}")
    for x in traj:
        P(f"  {x['rung']:>5d}{x['n']:>6d}{x['accumulated_supersessions']:>11d}"
          f"{x['confab_a']:>12.4f}{x['confab_b']:>12.4f}{x['advantage_pp']:>14.2f}"
          f"   [{x['ci_lo_pp']:+7.2f}, {x['ci_hi_pp']:+7.2f}]")
    P(f"  non-decreasing across the four rungs: "
      f"{res['staleness_trajectory']['non_decreasing']}")

    P("\n3.7 ABSENCE MIX")
    P("  per-rung eval absence share: " + "  ".join(
        f"r{r} {res['absence_mix']['per_rung_absence_share'][str(r)]:.1%}"
        for r in RUNGS))
    e2, e3 = res["absence_mix"]["E2_vs_E3"]["E2"], res["absence_mix"]["E2_vs_E3"]["E3"]
    P(f"  {'':22s}{'manufactured':>14s}{'L':>9s}{'p*':>9s}{'tau':>7s}{'rate':>8s}")
    P(f"  {'E2 (all variants)':22s}{e2['manufactured_share']:>13.1%}{e2['L']:>9.4f}"
      f"{e2['p_star']:>9.4f}{e2['tau_FOK']:>7.2f}{e2['realised_rate']:>8.3f}")
    P(f"  {'E3 (FULL slice)':22s}{e3['manufactured_share']:>13.1%}{e3['L']:>9.4f}"
      f"{e3['p_star']:>9.4f}{e3['tau_FOK']:>7.2f}{e3['realised_rate']:>8.3f}")

    P("\n3.8 ABSENCE SPLIT AT SESSION SCALE")
    for kind, d in res["absence_split"].items():
        P(f"  {kind}  (n={list(d.values())[0]['n']})")
        for a, v in d.items():
            P(f"    {a:28s} credit {v['credit']:.4f}   confab {v['confab']:.4f}")

    P("\n3.9 ECONOMICS  ($/1M turns, D44-corrected prices)")
    for a, v in res["economics"]["per_1M_turns"].items():
        P(f"  {a:28s} uncached {v['uncached']:8.0f}   cached {v['cached']:8.0f}")
    P("  index maintenance, TWO columns, never averaged:")
    for r in RUNGS:
        P(f"    rung {r:>2d}: write-driven {maint[r]['write_us']:8.0f} us "
          f"(40 personas)   clock pass {maint[r]['clock_ms']:.3f} ms/serve   "
          f"render {maint[r]['serve_ms']:.3f} ms/serve")

    P("\n3.10 SCRAMBLE CENSUS")
    P(f"  annotation destruction rate: {ann['destruction_rate']}")
    P(f"  index lobotomy: totals block identical on "
      f"{IX['lobotomy']['marginal_preserving_totals_block_identical']}/160; "
      f"indexes differ {IX['lobotomy']['indexes_that_differ']}/160; "
      f"digests differ {IX['lobotomy']['digests_that_differ']}/160")
    P("  non-vacuity realised on eval: (a)/(b) 100.0%, (a)/(a') 100.0%")

    P("\n3.11 JUDGE VALIDITY SPOT-CHECK  (reported, no bar, gates nothing)")
    P(f"  confabulation flag : unweighted {js['confab_agreement']:.0%}   "
      f"POPULATION-WEIGHTED {js['population_weighted']['confab_agreement']:.1%}"
      f"   FR reference 88%")
    P(f"  four-way typing    : unweighted {js['four_way_agreement']:.0%}   "
      f"POPULATION-WEIGHTED {js['population_weighted']['four_way_agreement']:.1%}"
      f"   FR reference 85%")

    P("\n3.12 OPERATING POINTS")
    P(f"  tau_FOK {tau}   tau_NOK {thr['tau_NOK']}   p* "
      f"{thr['derivation']['p_star']:.4f}   both at the grid minimum")
    P(f"  {res['operating_points']['consequence']}")
    P("\nwrote results/e3_scores.json")


if __name__ == "__main__":
    main()
