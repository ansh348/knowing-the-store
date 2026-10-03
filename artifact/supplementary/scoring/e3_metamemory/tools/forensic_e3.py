"""
forensic_e3.py -- EXPLORATORY decomposition. Q1-Q6 of FORENSIC_E3.md, and nothing
outside them. NO API CALLS. $0.

EVERY OUTPUT OF THIS FILE IS EXPLORATORY. No gate is re-evaluated, no band appears,
and no result here may be described as confirming or refuting a registered
hypothesis. RESULTS_E3.md is immutable.

Estimator and bootstrap imported from score_e2, not re-implemented. Strata with
n < 20 report their interval and their point estimate is not interpreted.

Usage:  python e3_metamemory/tools/forensic_e3.py
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e2_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from score_e2 import adjusted, boot_ci                             # noqa: E402
from e3_common import (E3, RUNGS, S0, S1, S2, S3, S3P, INTENTS,    # noqa: E402
                       NEG_ELIGIBLE, Snapshot, jdump, jload,
                       load_cells, session_dates)
from score_e3 import credit_of                                     # noqa: E402

MIN_N = 20
GRID = [round(x * 0.05, 2) for x in range(21)]
OUT = E3 / "results" / "forensic_e3.json"


def ci(d, one_sided=False):
    if not d:
        return {"n": 0}
    lo, hi = boot_ci(d, one_sided)
    personas = len({p for p, _l, _v in d})
    labels = len({l for _p, l, _v in d})
    est = adjusted(d, None, None) if (personas >= 2 and labels >= 2) else \
        float(np.mean([v for _p, _l, v in d]))
    return {"est": est, "unadj": float(np.mean([v for _p, _l, v in d])),
            "lo": lo, "hi": hi, "n": len(d),
            "adjusted": personas >= 2 and labels >= 2,
            "interpret": len(d) >= MIN_N}


# ===========================================================================
# E3 outcome layer
# ===========================================================================
def e3_layer():
    C = load_cells()
    cells = {c["cell_id"]: c for c in C["cells"] if c["split"] == "eval"}
    tags = sorted(cells)
    thr = jload(E3 / "THRESHOLDS_E3_FROZEN.json")
    gT = {r["cell_id"]: r for r in jload(E3 / "gates_eval.json")["rows"]}
    gL = {r["cell_id"]: r for r in jload(E3 / "gates_eval_lobotomy.json")["rows"]}
    A = jload(E3 / "answers_eval.json")["rows"]
    J = jload(E3 / "cache" / "judgments_eval.json")
    corr, conf, s0q = {}, {}, {}
    for a in A:
        v = J.get(f"{a['cell_id']}|{a['response_sha'][:24]}", {})
        corr[(a["cell_id"], a["state"])] = v.get("correctness")
        conf[(a["cell_id"], a["state"])] = bool(v.get("confabulation"))
        if a["state"] == S0:
            s0q[(a["persona"], a["question_id"])] = v.get("correctness")
    tau = thr["tau_FOK"]

    def fok(g, t):
        return g[t]["fok"] if g[t]["fok"] is not None else -1

    ARMS = {"(a)": lambda t: S3 if fok(gT, t) >= tau else S0,
            "(a')": lambda t: S3P if fok(gL, t) >= tau else S0,
            "(a'')": lambda t: S2 if fok(gT, t) >= tau else S0,
            "(b)": lambda t: S1,
            "(c)": lambda t: S0}

    def out(t, state):
        c = (s0q[(cells[t]["persona"], cells[t]["question_id"])] if state == S0
             else corr[(t, state)])
        f = False if state == S0 else conf[(t, state)]
        return credit_of(cells[t]["label"], c), (1.0 if f else 0.0)

    return cells, tags, ARMS, out, gT, gL, thr


def stratum_of(c):
    if c["label"] == "PRESENT-NEGATIVE":
        return "PN"
    if c["label"] == "PRESENT":
        return "PRESENT"
    return "natural-absent" if c["kind"] == "probe" else "ablation/unwritten-absent"


# ===========================================================================
def main():
    R = {"EXPLORATORY": True, "results_e3_immutable": True,
         "no_gate_re_evaluated": True, "questions": "FORENSIC_E3.md Q1-Q6"}
    cells, tags, ARMS, out, gT, gL, thr = e3_layer()
    P = print
    P("=" * 100)
    P("FORENSIC E3 -- EXPLORATORY. No gate is re-evaluated. No band appears below.")
    P("=" * 100)

    def contrast(a1, a2, field, sub):
        d = []
        for t in sub:
            c1, f1 = out(t, ARMS[a1](t))
            c2, f2 = out(t, ARMS[a2](t))
            if c1 is None or c2 is None:
                continue
            v1, v2 = (c1, c2) if field == "credit" else (f1, f2)
            d.append((cells[t]["persona"], cells[t]["label"], v1 - v2))
        return ci(d)

    def rate(arm, field, sub):
        v = []
        for t in sub:
            c, f = out(t, ARMS[arm](t))
            if c is None:
                continue
            v.append(c if field == "credit" else f)
        return float(np.mean(v)) if v else None

    strata = collections.defaultdict(list)
    for t in tags:
        strata[stratum_of(cells[t])].append(t)
    e3_mix = {k: len(v) / len(tags) for k, v in strata.items()}

    # =======================================================================
    # Q1 RECONCILIATION
    # =======================================================================
    P("\n" + "=" * 100)
    P("Q1  RECONCILIATION -- E2's caution effect by stratum, re-weighted to E3's mix")
    P("=" * 100)
    from e2_common import E2, load_items                            # noqa: PLC0415
    e2items = {i["item_id"]: i for i in load_items() if i["split"] == "eval"}
    e2A = jload(E2 / "answers_eval.json")["rows"]
    e2J = jload(E2 / "cache" / "judgments_eval.json")
    e2c = {}
    for a in e2A:
        v = e2J.get(f"{a['item_id']}|{a['response_sha'][:24]}", {})
        e2c[(a["item_id"], a["state"])] = (v.get("correctness"),
                                           bool(v.get("confabulation")))

    def e2_stratum(i):
        if i["label_final"] == "PRESENT-NEGATIVE":
            return "PN"
        if i["label_final"] == "PRESENT":
            return "PRESENT"
        return ("natural-absent" if str(i.get("absent_mechanism")) == "natural"
                else "ablation/unwritten-absent")

    e2s = collections.defaultdict(list)
    for k, i in e2items.items():
        e2s[e2_stratum(i)].append(k)
    e2_mix = {k: len(v) / len(e2items) for k, v in e2s.items()}

    def e2_caution(sub, field="confab"):
        d = []
        for t in sub:
            c2, f2 = e2c[(t, S2)]
            c1, f1 = e2c[(t, S1)]
            if c2 is None or c1 is None:
                continue
            lab = e2items[t]["label_final"]
            v = ((credit_of(lab, c2) - credit_of(lab, c1)) if field == "credit"
                 else ((1.0 if f2 else 0.0) - (1.0 if f1 else 0.0)))
            d.append((e2items[t]["persona"], lab, v))
        return ci(d)

    per_stratum = {k: e2_caution(v) for k, v in e2s.items()}
    P(f"\n  E2's PURE CAUTION EFFECT (S2 minus S1, confabulation, all "
      f"{len(e2items)} eval items -- unselected)")
    P(f"  {'stratum':30s}{'n':>5s}{'E2 share':>10s}{'E3 share':>10s}"
      f"{'effect pp':>11s}{'95% CI pp':>22s}")
    for k in sorted(per_stratum):
        v = per_stratum[k]
        P(f"  {k:30s}{v['n']:>5d}{e2_mix.get(k,0):>10.1%}{e3_mix.get(k,0):>10.1%}"
          f"{v['est']*100:>11.2f}   [{v['lo']*100:+7.2f}, {v['hi']*100:+7.2f}]"
          + ("" if v["interpret"] else "   n<20"))
    pooled_e2 = e2_caution(sorted(e2items))
    P(f"  {'POOLED at E2 mix':30s}{pooled_e2['n']:>5d}{1.0:>10.1%}{'':>10s}"
      f"{pooled_e2['est']*100:>11.2f}   [{pooled_e2['lo']*100:+7.2f}, "
      f"{pooled_e2['hi']*100:+7.2f}]")

    # re-weight, with a persona-clustered bootstrap over E2 personas
    def reweight(mix, boot=1000, seed=42):
        rng = np.random.default_rng(seed)
        keys = [k for k in mix if k in e2s and e2s[k]]
        point = sum(mix[k] * per_stratum[k]["est"] for k in keys)
        byp = collections.defaultdict(list)
        for k in keys:
            for t in e2s[k]:
                byp[e2items[t]["persona"]].append((k, t))
        ps = sorted(byp)
        draws = []
        for _ in range(boot):
            pick = rng.choice(ps, size=len(ps), replace=True)
            acc = collections.defaultdict(list)
            for q in pick:
                for k, t in byp[q]:
                    c2, f2 = e2c[(t, S2)]
                    c1, f1 = e2c[(t, S1)]
                    if c2 is None or c1 is None:
                        continue
                    acc[k].append((1.0 if f2 else 0.0) - (1.0 if f1 else 0.0))
            tot, wsum = 0.0, 0.0
            for k in keys:
                if acc[k]:
                    tot += mix[k] * float(np.mean(acc[k]))
                    wsum += mix[k]
            draws.append(tot / wsum if wsum else 0.0)
        return point, float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))

    # ---- the SAME decomposition on E2's PUBLISHED H-C2 contrast, (vi) minus (v),
    # for the record. E3's (a)/(b) pair both retrieve on 100% of cells, so the
    # unselected S2-S1 above is the correct analogue; (vi)-(v) additionally carries
    # E2's 68% gating decision and is NOT the same quantity. Both are reported so
    # the choice is visible rather than assumed.
    e2thr = jload(E2 / "THRESHOLDS_FROZEN.json")
    e2g = {r["item_id"]: r for r in jload(E2 / "gates_eval.json")["rows"]}

    def e2_retrieves(t):
        f = (e2g[t]["indexed"].get("1") or {}).get("fok")
        return f is not None and f >= e2thr["tau_FOK"]

    def e2_hc2(sub):
        d = []
        for t in sub:
            s_vi = S2 if e2_retrieves(t) else S0
            s_v = S1 if e2_retrieves(t) else S0
            _c2, f2 = e2c[(t, s_vi)]
            _c1, f1 = e2c[(t, s_v)]
            if _c2 is None or _c1 is None:
                continue
            d.append((e2items[t]["persona"], e2items[t]["label_final"],
                      (1.0 if f2 else 0.0) - (1.0 if f1 else 0.0)))
        return ci(d)

    hc2 = {k: e2_hc2(v) for k, v in e2s.items()}
    hc2_all = e2_hc2(sorted(e2items))
    P("\n  E2's PUBLISHED H-C2 contrast, (vi) minus (v), same strata "
      "-- carries E2's 68% gating decision, NOT the same quantity")
    P(f"  {'stratum':30s}{'n':>5s}{'effect pp':>11s}{'95% CI pp':>22s}")
    for k in sorted(hc2):
        v = hc2[k]
        P(f"  {k:30s}{v['n']:>5d}{v['est']*100:>11.2f}   "
          f"[{v['lo']*100:+7.2f}, {v['hi']*100:+7.2f}]")
    P(f"  {'POOLED (published -5.79pp)':30s}{hc2_all['n']:>5d}"
      f"{hc2_all['est']*100:>11.2f}   [{hc2_all['lo']*100:+7.2f}, "
      f"{hc2_all['hi']*100:+7.2f}]")

    pred, plo, phi = reweight(e3_mix)
    obs_a = contrast("(a)", "(b)", "confab", tags)
    obs_ac = contrast("(a'')", "(b)", "confab", tags)
    P(f"\n  PREDICTED for E3's mix (E2 per-stratum effects re-weighted): "
      f"{pred*100:+.2f}pp   95% CI [{plo*100:+.2f}, {phi*100:+.2f}]")
    P(f"  OBSERVED E3 (a'') vs (b)  -- the pure-caution analogue : "
      f"{obs_ac['est']*100:+.2f}pp   95% CI [{obs_ac['lo']*100:+.2f}, "
      f"{obs_ac['hi']*100:+.2f}]")
    P(f"  OBSERVED E3 (a)   vs (b)  -- the registered H-E3a arm  : "
      f"{obs_a['est']*100:+.2f}pp   95% CI [{obs_a['lo']*100:+.2f}, "
      f"{obs_a['hi']*100:+.2f}]")
    resid_c = obs_ac["est"] - pred
    resid_a = obs_a["est"] - pred
    P(f"\n  RESIDUAL vs (a''): {resid_c*100:+.2f}pp     "
      f"RESIDUAL vs (a): {resid_a*100:+.2f}pp")
    agree_c = plo <= obs_ac["est"] <= phi and obs_ac["lo"] <= pred <= obs_ac["hi"]
    agree_a = plo <= obs_a["est"] <= phi and obs_a["lo"] <= pred <= obs_a["hi"]
    P(f"  intervals mutually contain the other's point estimate: "
      f"(a'') {agree_c}   (a) {agree_a}")
    R["Q1"] = {"e2_per_stratum": per_stratum,
               "e2_published_hc2_per_stratum": hc2, "e2_published_hc2_pooled": hc2_all,
               "analogue_note": "E3's (a)/(b) pair both retrieve on 100% of cells, "
                                "so the unselected S2-S1 is the correct analogue; "
                                "(vi)-(v) additionally carries E2's 68% gating "
                                "decision and is not the same quantity", "e2_mix": e2_mix, "e3_mix": e3_mix,
               "e2_pooled": pooled_e2,
               "predicted_at_e3_mix": {"est": pred, "lo": plo, "hi": phi},
               "observed_a_vs_b": obs_a, "observed_ac_vs_b": obs_ac,
               "residual_vs_ac": resid_c, "residual_vs_a": resid_a,
               "mutual_containment": {"a''": bool(agree_c), "a": bool(agree_a)}}

    # =======================================================================
    # Q2 STRATUM MAP
    # =======================================================================
    P("\n" + "=" * 100)
    P("Q2  STRATUM MAP -- deltas by coverage label and by rung. No narrative.")
    P("=" * 100)
    q2 = {}
    for pair in (("(a)", "(b)"), ("(a)", "(a'')")):
        for field in ("confab", "credit"):
            P(f"\n  {pair[0]} minus {pair[1]}, {field}")
            P(f"  {'slice':30s}{'n':>5s}{'delta':>10s}{'95% CI':>24s}")
            rows = {}
            for k in sorted(strata):
                v = contrast(pair[0], pair[1], field, strata[k])
                rows[f"label:{k}"] = v
                P(f"  {k:30s}{v['n']:>5d}{v['est']:>10.4f}   "
                  f"[{v['lo']:+8.4f}, {v['hi']:+8.4f}]"
                  + ("" if v["interpret"] else "   n<20, not interpreted"))
            for r in RUNGS:
                sub = [t for t in tags if cells[t]["rung"] == r]
                v = contrast(pair[0], pair[1], field, sub)
                rows[f"rung:{r}"] = v
                P(f"  {'rung ' + str(r):30s}{v['n']:>5d}{v['est']:>10.4f}   "
                  f"[{v['lo']:+8.4f}, {v['hi']:+8.4f}]")
            q2[f"{pair[0]}_minus_{pair[1]}|{field}"] = rows
    R["Q2"] = q2

    # =======================================================================
    # Q3 PN ZOOM
    # =======================================================================
    P("\n" + "=" * 100)
    P("Q3  PN ZOOM -- cells where a truly-superseded, BELIEVED-ACTIVE entry was")
    P("    actually retrieved, under CURRENT-STATE / UPCOMING intent")
    P("=" * 100)
    from e0_common import load_joins, toks                          # noqa: PLC0415
    from index_v2 import detect                                     # noqa: PLC0415
    joins = load_joins()
    dates = session_dates()
    personas = sorted({c["persona"] for c in cells.values()})
    snaps = {p: Snapshot(p, dates[p]) for p in personas}
    fr = {r["cell_id"]: r for r in jload(E3 / "retrieval_frozen_e3.json")["rows"]}

    truly = {}                       # (persona, rung) -> set of truly-stale ids
    for p in personas:
        J = joins[p]
        et = {e["id"]: toks(e.get("text", ""), J.drop) for e in J.entries}
        for r in RUNGS:
            alive = snaps[p].alive(r)
            s = set()
            for sec, nf in (("supersession_events", "new_session"),
                            ("contradictions", "new_session")):
                for rec in (J.y.get(sec) or []):
                    if not isinstance(rec, dict):
                        continue
                    ns = rec.get(nf)
                    if not isinstance(ns, int) or ns > r:
                        continue
                    d = detect(rec.get("old_fact"), rec.get("new_fact"), et, J.drop)
                    if d:
                        s |= {i for i, v in d.items() if v >= 0.80 and i in alive}
            truly[(p, r)] = s

    hab, contam_rows = [], []
    for t in tags:
        c = cells[t]
        p, r = c["persona"], c["rung"]
        got = fr[t]["entry_ids"]
        stale_ret = [e for e in got if e in truly[(p, r)]
                     and not snaps[p].is_superseded_at(e, r)]
        contam_rows.append((t, r, len(got), len(stale_ret)))
        intent = INTENTS.get(c["question_id"])
        if stale_ret and intent in NEG_ELIGIBLE:
            hab.append(t)
    P(f"\n  eval cells whose retrieved context contains at least one "
      f"truly-superseded, believed-active fact")
    P(f"  AND whose question intent is CURRENT-STATE or UPCOMING:  **{len(hab)}** "
      f"of {len(tags)}")
    P(f"  by rung: {dict(collections.Counter(cells[t]['rung'] for t in hab))}")
    P(f"  by label: {dict(collections.Counter(cells[t]['label'] for t in hab))}")
    if hab:
        P(f"\n  {'arm':8s}{'confab':>10s}{'credit':>10s}   on exactly that stratum "
          f"(n={len(hab)})")
        for a in ("(a)", "(a')", "(a'')", "(b)", "(c)"):
            P(f"  {a:8s}{rate(a,'confab',hab):>10.4f}{rate(a,'credit',hab):>10.4f}")
        d1 = contrast("(a)", "(a'')", "confab", hab)
        d2 = contrast("(a)", "(b)", "confab", hab)
        P(f"\n  (a) minus (a'') confab on the habitat: {d1['est']:+.4f}  "
          f"[{d1['lo']:+.4f}, {d1['hi']:+.4f}]  n={d1['n']}"
          + ("" if d1["interpret"] else "   n<20, NOT INTERPRETED"))
        P(f"  (a) minus (b)   confab on the habitat: {d2['est']:+.4f}  "
          f"[{d2['lo']:+.4f}, {d2['hi']:+.4f}]  n={d2['n']}"
          + ("" if d2["interpret"] else "   n<20, NOT INTERPRETED"))
        R["Q3"] = {"habitat_n": len(hab), "by_rung": dict(collections.Counter(
            cells[t]["rung"] for t in hab)),
            "by_label": dict(collections.Counter(cells[t]["label"] for t in hab)),
            "per_arm": {a: {"confab": rate(a, "confab", hab),
                            "credit": rate(a, "credit", hab)}
                        for a in ("(a)", "(a')", "(a'')", "(b)", "(c)")
                        if a in ARMS},
            "a_minus_ac": d1, "a_minus_b": d2, "cells": hab}
    else:
        R["Q3"] = {"habitat_n": 0}

    # =======================================================================
    # Q4 CAUTION TAX
    # =======================================================================
    P("\n" + "=" * 100)
    P("Q4  CAUTION TAX -- (a'') minus (b) CREDIT by label")
    P("=" * 100)
    P(f"  {'stratum':30s}{'n':>5s}{'credit a2':>14s}{'credit (b)':>12s}"
      f"{'delta':>10s}{'95% CI':>24s}")
    q4 = {}
    for k in sorted(strata) + ["ALL"]:
        sub = tags if k == "ALL" else strata[k]
        v = contrast("(a'')", "(b)", "credit", sub)
        q4[k] = {"delta": v, "credit_ac": rate("(a'')", "credit", sub),
                 "credit_b": rate("(b)", "credit", sub)}
        P(f"  {k:30s}{v['n']:>5d}{q4[k]['credit_ac']:>14.4f}"
          f"{q4[k]['credit_b']:>12.4f}{v['est']:>10.4f}   "
          f"[{v['lo']:+8.4f}, {v['hi']:+8.4f}]"
          + ("" if v["interpret"] else "   n<20"))
    R["Q4"] = q4

    # =======================================================================
    # Q5 OFFLINE SELECTIVE-CAUTION FRONTIER
    # =======================================================================
    P("\n" + "=" * 100)
    P("Q5  OFFLINE SELECTIVE-CAUTION FRONTIER")
    P("    *** FITTED ON EVAL DATA. HYPOTHESIS-GENERATING ONLY. NO CLAIM. ***")
    P("=" * 100)
    nok = {t: (gT[t]["nok"] if gT[t]["nok"] is not None else 0.0) for t in tags}
    P(f"\n  {'t':>6s}{'fires':>8s}{'rate':>8s}{'confab':>10s}{'credit':>10s}")
    q5 = []
    for tt in GRID:
        cr, cf, n = [], [], 0
        for t in tags:
            arm = "(a'')" if nok[t] >= tt else "(b)"
            c, f = out(t, ARMS[arm](t))
            if c is None:
                continue
            cr.append(c); cf.append(f)
            n += 1 if nok[t] >= tt else 0
        q5.append({"t": tt, "fires": n, "rate": n / len(tags),
                   "confab": float(np.mean(cf)), "credit": float(np.mean(cr))})
        P(f"  {tt:>6.2f}{n:>8d}{n/len(tags):>8.3f}"
          f"{q5[-1]['confab']:>10.4f}{q5[-1]['credit']:>10.4f}")
    ref = {a: {"confab": rate(a, "confab", tags), "credit": rate(a, "credit", tags)}
           for a in ("(a)", "(a'')", "(b)")}
    P(f"\n  reference points:")
    for a, v in ref.items():
        P(f"    {a:8s} confab {v['confab']:.4f}   credit {v['credit']:.4f}")
    dom = [x for x in q5
           if x["confab"] <= ref["(a'')"]["confab"] + 1e-12
           and x["credit"] >= ref["(a'')"]["credit"] - 1e-12
           and (x["confab"] < ref["(a'')"]["confab"] - 1e-12
                or x["credit"] > ref["(a'')"]["credit"] + 1e-12)]
    P(f"\n  thresholds weakly dominating (a'') on BOTH endpoints: "
      f"{[x['t'] for x in dom] or 'none'}")
    R["Q5"] = {"WARNING": "FITTED ON EVAL DATA; HYPOTHESIS-GENERATING ONLY; NO CLAIM",
               "sweep": q5, "reference": ref,
               "dominating_thresholds": [x["t"] for x in dom]}

    # =======================================================================
    # Q6 AGING DECOMPOSITION
    # =======================================================================
    P("\n" + "=" * 100)
    P("Q6  AGING DECOMPOSITION -- what carries the tripling")
    P("=" * 100)
    P(f"\n  {'rung':>5s}{'cells':>7s}{'facts':>8s}{'stale facts':>12s}"
      f"{'contamination':>14s}{'cells w/ any':>13s}{'store':>7s}"
      f"{'non-ABSENT':>12s}{'confab (b)':>12s}")
    q6 = []
    for r in RUNGS:
        rows = [x for x in contam_rows if x[1] == r]
        nf = sum(x[2] for x in rows)
        ns = sum(x[3] for x in rows)
        anyc = sum(1 for x in rows if x[3] > 0)
        sub = [t for t in tags if cells[t]["rung"] == r]
        nonabs = sum(1 for t in sub if cells[t]["label"] != "ABSENT") / len(sub)
        store = float(np.mean([fr[t]["n_alive"] for t in sub]))
        row = {"rung": r, "cells": len(sub), "facts": nf, "stale_facts": ns,
               "contamination": ns / nf if nf else 0.0,
               "cells_with_any_stale": anyc / len(sub), "store_size": store,
               "non_absent_share": nonabs,
               "confab_b": rate("(b)", "confab", sub),
               "confab_a": rate("(a)", "confab", sub)}
        q6.append(row)
        P(f"  {r:>5d}{len(sub):>7d}{nf:>8d}{ns:>12d}{row['contamination']:>14.4f}"
          f"{row['cells_with_any_stale']:>13.3f}{store:>7.0f}{nonabs:>12.3f}"
          f"{row['confab_b']:>12.4f}")

    # mix-standardised: hold the label mix at the pooled mix, vary only rung
    pooled_w = {k: len(v) / len(tags) for k, v in
                collections.defaultdict(list, {
                    lab: [t for t in tags if cells[t]["label"] == lab]
                    for lab in ("PRESENT", "PRESENT-NEGATIVE", "ABSENT")}).items()}
    P(f"\n  MIX-STANDARDISED confab for (b): each rung's within-label rates "
      f"re-weighted to the pooled label mix")
    P(f"  {'rung':>5s}{'raw':>10s}{'standardised':>14s}   within-label rates")
    std = []
    for r in RUNGS:
        sub = [t for t in tags if cells[t]["rung"] == r]
        parts, s = {}, 0.0
        for lab, w in pooled_w.items():
            ss = [t for t in sub if cells[t]["label"] == lab]
            v = rate("(b)", "confab", ss) if ss else None
            parts[lab] = v
            if v is not None:
                s += w * v
        std.append({"rung": r, "raw": rate("(b)", "confab", sub),
                    "standardised": s, "within_label": parts})
        P(f"  {r:>5d}{std[-1]['raw']:>10.4f}{s:>14.4f}   " +
          "  ".join(f"{k[:4]} {('%.3f' % v) if v is not None else 'n/a'}"
                    for k, v in parts.items()))
    raw_ratio = q6[-1]["confab_b"] / q6[0]["confab_b"] if q6[0]["confab_b"] else None
    std_ratio = std[-1]["standardised"] / std[0]["standardised"] \
        if std[0]["standardised"] else None
    P(f"\n  rung 32 / rung 14 confabulation ratio, (b):  RAW {raw_ratio:.2f}x   "
      f"MIX-STANDARDISED {std_ratio:.2f}x")
    P(f"  contamination rung 14 -> 32: {q6[0]['contamination']:.4f} -> "
      f"{q6[-1]['contamination']:.4f}   "
      f"({q6[-1]['contamination']/max(q6[0]['contamination'],1e-9):.2f}x)")
    P(f"  store size    rung 14 -> 32: {q6[0]['store_size']:.0f} -> "
      f"{q6[-1]['store_size']:.0f}   "
      f"({q6[-1]['store_size']/q6[0]['store_size']:.2f}x)")
    P(f"  non-ABSENT share rung 14 -> 32: {q6[0]['non_absent_share']:.3f} -> "
      f"{q6[-1]['non_absent_share']:.3f}   "
      f"({q6[-1]['non_absent_share']/q6[0]['non_absent_share']:.2f}x)")
    R["Q6"] = {"rows": q6, "mix_standardised": std,
               "raw_ratio_32_over_14": raw_ratio,
               "standardised_ratio_32_over_14": std_ratio}

    jdump(R, OUT)
    P(f"\nwrote {OUT.name}   -- EVERY TABLE ABOVE IS EXPLORATORY")


if __name__ == "__main__":
    main()
