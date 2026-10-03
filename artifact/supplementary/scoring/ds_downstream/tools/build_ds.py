"""build_ds.py -- DS Phase B step 2: the policies, the assembled views and Stage 1 (ADDENDUM_DS.md
sections D.1-D.3, P), scored under section T. NO API CALLS. Deterministic.

  policies.json   per item and policy: gate, fetch set name, abstention, fetched ids (section D.2)
  views.json      per item and policy: the view text (the five L2 lines byte-identical, then the fetched
                  records not among the five, ranks continuing), its ids and sha256 (section D.1)
  stage1.json     per item and policy: PN reach (by id), tagged reach, successor-in-view, PRESENT coverage
                  (gold in view and not abstained), gold-in-view, abstention, view size; the rates per
                  policy and per state; the paired differences with both intervals; DS-P1..DS-P4 verdicts
                  and DS-P5, each under its frozen text
  ledger          AUX-DS-LINELOCK, -POLICIES, -REACH, -PRESENT, -ABSTAIN, -VIEWSIZE
"""
from __future__ import annotations

import collections
import datetime as dt
import io
import math
import sys

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import ds_common as DC                                                       # noqa: E402
from ds_common import ROOT, DS, LEDGER, J, jdump, POLICIES                   # noqa: E402
from common_e1r import N_BOOT, SEED                                          # noqa: E402

TOL = 0.05
P_STATES = (("sup", "supersession"), ("ret", "retraction"), ("exp", "expiry"))


# ------------------------------------------------------------------ estimators (section T)
def wilson(k, n, z=1.959964):
    if n == 0:
        return [float("nan"), float("nan")]
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [c - h, c + h]


def _draws(n, g, rng):
    if g is None:
        return rng.integers(0, n, n)
    groups = np.unique(g); idx_by = {u: np.flatnonzero(g == u) for u in groups}
    return np.concatenate([idx_by[groups[j]] for j in rng.integers(0, len(groups), len(groups))])


def boot_prop_diff(a, b, g=None, n=N_BOOT, seed=SEED):
    """The committed draw scheme (boot_item / boot_cluster: default_rng(seed), 1,000 draws) with the
    statistic mean(a) - mean(b) on the resampled items; no single-class discard applies to a proportion."""
    rng = np.random.default_rng(seed); a, b = np.asarray(a, float), np.asarray(b, float)
    g = None if g is None else np.asarray(g)
    d = []
    for _ in range(n):
        k = _draws(len(a), g, rng)
        d.append(float(a[k].mean() - b[k].mean()))
    d = np.asarray(d)
    lo, hi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    return {"n_draws": int(len(d)), "mean": float(d.mean()), "ci_lo": lo, "ci_hi": hi, "excludes_zero": bool(lo > 0 or hi < 0)}


def boot_ratio(a, m, o, g=None, n=N_BOOT, seed=SEED):
    """run_side.boot_ratio's rule on proportions: (mean m - mean a) / (mean o - mean a); draws with a
    non-positive oracle gain are discarded and counted."""
    rng = np.random.default_rng(seed); a, m, o = (np.asarray(v, float) for v in (a, m, o))
    g = None if g is None else np.asarray(g)
    d, n_nonpos = [], 0
    for _ in range(n):
        k = _draws(len(a), g, rng)
        den = o[k].mean() - a[k].mean()
        if den <= 0:
            n_nonpos += 1; continue
        d.append(float((m[k].mean() - a[k].mean()) / den))
    d = np.asarray(d)
    if not len(d):
        return {"n_draws": 0, "n_nonpositive_oracle_gain_discarded": n_nonpos, "note": "every draw discarded"}
    return {"n_draws": int(len(d)), "n_nonpositive_oracle_gain_discarded": n_nonpos, "mean": float(d.mean()),
            "ci_lo": float(np.percentile(d, 2.5)), "ci_hi": float(np.percentile(d, 97.5))}


def pdiff(a, b, g):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return {"a": float(a.mean()), "b": float(b.mean()), "D": float(a.mean() - b.mean()), "n": int(len(a)),
            "item": boot_prop_diff(a, b), "cluster": boot_prop_diff(a, b, g)}


def fmt_i(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]" if "ci_lo" in d else "[—]"


# ------------------------------------------------------------------ build
def build(sub):
    nb6, nb5, gate = DC.lookup_scores(sub)
    assert gate["pass"], gate
    th = DC.thresholds(sub, nb6, nb5)
    pol = DC.build_policies(sub, nb6, nb5, th)
    art = J(ROOT / "resp_review/l2/retrieval.json")["items"]
    views, n_lines_locked, gold_in_fetch = {}, 0, []
    l2_lines = {}
    for k, a in art.items():
        for ln in a["block"].split("\n"):
            body = ln.split("] ", 1)[1]
            eid = None
            l2_lines.setdefault(a["persona"], {}).setdefault(body, True)
    for it in sub:
        views[it["item_id"]] = {}
        fl = DC.true_flags()[it["persona"]]
        for p in POLICIES:
            fetched = pol[it["item_id"]]["policies"][p]["fetched"]
            assert all(DC.flagged(it, e) for e in fetched), "active entry fetched"
            if it["label"] == "PRESENT" and set(fetched) & set(it["gold"]):
                gold_in_fetch.append((it["item_id"], p))
            text, ids = DC.assemble_view(it, art[it["item_id"]]["block"], art[it["item_id"]]["top5_ids"], fetched)
            for ln in text.split("\n")[5:]:
                body = ln.split("] ", 1)[1]
                if body in l2_lines.get(it["persona"], {}):
                    n_lines_locked += 1
            views[it["item_id"]][p] = {"text": text, "ids": ids, "sha": DC.view_sha(text), "n_lines": len(ids)}
    meta = {"registration": "registrations/ADDENDUM_DS.md", "frozen": DC.FREEZE, "thresholds": th, "lookup_gate": gate,
            "retrieval": "resp_review/l2/retrieval.json (RESP Phase B step 4, b08757c)", "no_api_calls": True, "built": dt.date.today().isoformat(),
            "policies": {"ALWAYS": "top-5 only", "ORACLE": "gold labels: PN fetch F(P), ABSENT abstain", "MODEL": "nok >= theta_NOK fetch F(N2); fok < theta_FOK abstain",
                         "LOOKUP": "nb6 >= lambda_NOK fetch F(N2); nb5 < lambda_FOK abstain", "MODEL-ALL": "as MODEL with F(N3)", "LOOKUP-ALL": "as LOOKUP with F(N3)",
                         "LOOKUP-LIT": "descriptive: nb6 >= theta_NOK fetch F(N2); nb5 < theta_FOK abstain (never)"}}
    jdump({"meta": meta, "items": pol}, DS / "policies.json")
    jdump({"meta": {**meta, "line_rule": "the five L2 lines byte-identical, then F \\ top5 in ascending (slot, entry id) order, ranks continuing; no header"},
           "items": views}, DS / "views.json")
    return pol, views, n_lines_locked, gold_in_fetch


# ------------------------------------------------------------------ stage 1
def stage1(sub, pol, views, write=True):
    per = {}
    for it in sub:
        per[it["item_id"]] = {}
        for p in POLICIES:
            v = views[it["item_id"]][p]; a = pol[it["item_id"]]["policies"][p]["abstain"]
            ids = set(v["ids"]); pm = set(it.get("pn_members") or []); gold = set(it["gold"])
            per[it["item_id"]][p] = {"reach": bool(pm & ids) if it["y_nok"] else None,
                                     "tagged_reach": bool(any(DC.flagged(it, e) for e in pm & ids)) if it["y_nok"] else None,
                                     "successor_in_view": bool(gold & ids) if it["y_nok"] else None,
                                     "gold_in_view": bool(gold & ids) if it["label"] == "PRESENT" else None,
                                     "coverage": (bool(gold & ids) and not a) if it["label"] == "PRESENT" else None,
                                     "abstain": bool(a), "view_size": v["n_lines"], "gate": pol[it["item_id"]]["policies"][p]["gate"]}
    pn = [it for it in sub if it["y_nok"]]; pres = [it for it in sub if it["label"] == "PRESENT"]; absn = [it for it in sub if it["label"] == "ABSENT"]
    R = lambda p, items, key: np.array([per[it["item_id"]][p][key] for it in items], float)
    G = lambda items: [it["persona"] for it in items]
    rates = {}
    for p in POLICIES:
        r = {"gate_fires": sum(1 for it in sub if per[it["item_id"]][p]["gate"]), "abstentions": sum(1 for it in sub if per[it["item_id"]][p]["abstain"]),
             "pn_reach": {}, "pn_tagged": {}, "pn_successor": {}, "pn_abstain": sum(1 for it in pn if per[it["item_id"]][p]["abstain"])}
        for st, name in [(None, "all")] + [(s, n) for s, n in P_STATES]:
            sel = [it for it in pn if st is None or it["state"] == st]
            k = int(R(p, sel, "reach").sum()); r["pn_reach"][name] = {"reached": k, "n": len(sel), "rate": k / len(sel), "wilson": wilson(k, len(sel))}
            r["pn_tagged"][name] = int(R(p, sel, "tagged_reach").sum()); r["pn_successor"][name] = int(R(p, sel, "successor_in_view").sum())
        c = int(R(p, pres, "coverage").sum()); gv = int(R(p, pres, "gold_in_view").sum()); ab = int(R(p, pres, "abstain").sum())
        r["present"] = {"coverage": c, "n": 174, "rate": c / 174, "wilson": wilson(c, 174), "gold_in_view": gv, "abstained": ab,
                        "abstained_with_gold_in_view": int(sum(1 for it in pres if per[it["item_id"]][p]["abstain"] and per[it["item_id"]][p]["gold_in_view"]))}
        a383 = int(R(p, absn, "abstain").sum()); a272 = int(sum(1 for it in absn if it["tier"] == "hard" and per[it["item_id"]][p]["abstain"]))
        r["absent"] = {"abstain_383": a383, "rate_383": a383 / 383, "abstain_272": a272, "rate_272": a272 / 272}
        vs = [per[it["item_id"]][p]["view_size"] for it in sub]; vp = [per[it["item_id"]][p]["view_size"] for it in pn]
        r["view_size"] = {"mean_661": float(np.mean(vs)), "max_661": int(max(vs)), "mean_104": float(np.mean(vp)), "max_104": int(max(vp))}
        rates[p] = r

    # ---- registered items
    sup = [it for it in pn if it["state"] == "sup"]; ce = [it for it in pn if it["state"] in ("ret", "exp")]
    A, O, M, L, MA = (R("ALWAYS", pn, "reach"), R("ORACLE", pn, "reach"), R("MODEL", pn, "reach"), R("LOOKUP", pn, "reach"), R("MODEL-ALL", pn, "reach"))
    p1 = pdiff(O, A, G(pn))
    As, Os, Ms, Ls = (R("ALWAYS", sup, "reach"), R("ORACLE", sup, "reach"), R("MODEL", sup, "reach"), R("LOOKUP", sup, "reach"))
    rho = float((Ms.mean() - As.mean()) / (Os.mean() - As.mean())) if Os.mean() > As.mean() else float("nan")
    rho_i, rho_c = boot_ratio(As, Ms, Os), boot_ratio(As, Ms, Os, G(sup))
    missed = [it for it in sup if not per[it["item_id"]]["ALWAYS"]["reach"]]
    g_on_missed = sum(1 for it in missed if per[it["item_id"]]["MODEL"]["gate"])
    p3 = pdiff(Ls, Ms, G(sup)); p3_all = pdiff(L, M, G(pn))
    Mce, MAce = R("MODEL", ce, "reach"), R("MODEL-ALL", ce, "reach")
    p4 = pdiff(MAce, Mce, G(ce))
    newly = [it for it in ce if set(DC.fetch(it, DC.names_for(it)[3])) & set(it["pn_members"]) and not (set(DC.fetch(it, DC.names_for(it)[2])) & set(it["pn_members"]))]
    g_newly = sum(1 for it in newly if per[it["item_id"]]["MODEL"]["gate"] and not per[it["item_id"]]["ALWAYS"]["reach"])
    CA, CM = R("ALWAYS", pres, "coverage"), R("MODEL", pres, "coverage")
    p5 = pdiff(CM, CA, G(pres))
    a_pres = rates["MODEL"]["present"]["abstained"]; c_pres = rates["MODEL"]["present"]["abstained_with_gold_in_view"]

    V = {}
    v1 = p1["D"] > 0.50
    V["DS-P1"] = {"holds": bool(v1), "O": p1["a"], "A": p1["b"], "D": p1["D"], "item": p1["item"], "cluster": p1["cluster"]}
    if v1:
        V["DS-P1"]["text"] = (f"Fetching the store's lifecycle records for the obligation's own attribute raises the forbidding record's presence in the view from "
                              f"{p1['b']:.4f} to {p1['a']:.4f} on the 104 obligations (difference {p1['D']:+.4f}, interval {fmt_i(p1['item'])}; persona-clustered {fmt_i(p1['cluster'])}): "
                              f"the record is within reach of a policy that acts on the judgment, and out of reach of the retriever.")
    else:
        V["DS-P1"]["text"] = (f"Fetching the store's lifecycle records for the obligation's own attribute, on gold labels, puts the forbidding record in the view for "
                              f"{int(O.sum())} of the 104 obligations against {int(A.sum())} for the five-entry similarity view alone, a difference of {p1['D']:+.4f} "
                              f"(interval {fmt_i(p1['item'])}; persona-clustered {fmt_i(p1['cluster'])}) that does not exceed 0.50. Either the retrieved view already carries the "
                              f"record for most obligations, or the store's metadata does not flag it: the truthful join marks the forbidding record non-active for 82 of 104 "
                              f"(8 of 26 retraction-derived, 11 of 15 expiry-derived), and no fetch by lifecycle state reaches the other 22. Acting on a perfect obligation "
                              f"judgment reaches {p1['a']:.4f} on this store, not one.")
    i_ok = "ci_lo" in rho_i and rho_i["ci_lo"] > 0.60 and rho >= 0.60
    c_ok = "ci_lo" in rho_c and rho_c["ci_lo"] > 0.60 and rho >= 0.60
    V["DS-P2"] = {"holds": bool(i_ok and c_ok), "item_reading": bool(i_ok), "cluster_reading": bool(c_ok), "disagree": bool(i_ok != c_ok), "rho": rho,
                  "item": rho_i, "cluster": rho_c, "M": float(Ms.mean()), "A": float(As.mean()), "O": float(Os.mean()), "gate_on_missed": g_on_missed, "missed": len(missed)}
    Ii = f"[{rho_i['ci_lo']:.4f}, {rho_i['ci_hi']:.4f}]" if "ci_lo" in rho_i else "[—]"
    Ic = f"[{rho_c['ci_lo']:.4f}, {rho_c['ci_hi']:.4f}]" if "ci_lo" in rho_c else "[—]"
    if V["DS-P2"]["holds"]:
        V["DS-P2"]["text"] = (f"Gated on the smallest model's committed obligation score at its base rate, the fetch retains {rho:.4f} of the oracle gain on the "
                              f"supersession-derived obligations (interval {Ii}; persona-clustered {Ic}): the judgment the summary supports is acted on.")
    else:
        V["DS-P2"]["text"] = (f"On the 63 supersession-derived obligations, where every forbidding record is flagged and named, gating the fetch on the smallest model's "
                              f"committed obligation score at its base rate puts the record in view for {Ms.mean():.4f}, against {As.mean():.4f} under retrieval alone and "
                              f"{Os.mean():.4f} under gold labels, retaining {rho:.4f} of the oracle gain with interval {Ii} (persona-clustered {Ic}) that does not exclude 0.60 "
                              f"from below. The gate fires on {g_on_missed} of the {len(missed)} supersession-derived obligations the retriever misses; the summary supports the "
                              f"judgment, and the judgment at this threshold does not carry it into the view.")
        if V["DS-P2"]["disagree"]:
            V["DS-P2"]["text"] += " The item-level and the persona-clustered intervals disagree on this prediction; the weaker reading governs."
    v3 = abs(p3["D"]) <= TOL
    V["DS-P3"] = {"holds": bool(v3), "L": p3["a"], "M": p3["b"], "D": p3["D"], "item": p3["item"], "cluster": p3["cluster"], "on_104": {"L": p3_all["a"], "M": p3_all["b"], "D": p3_all["D"], "item": p3_all["item"], "cluster": p3_all["cluster"]}}
    if v3:
        V["DS-P3"]["text"] = (f"The superseded-names lookup, at the same fetch budget, puts the record in view within tolerance of the model's gate ({p3['a']:.4f} against "
                              f"{p3['b']:.4f} on the 63, {p3['D']:+.4f}, interval {fmt_i(p3['item'])}; persona-clustered {fmt_i(p3['cluster'])}): on the state the summary names, the gate can be a lookup.")
    else:
        V["DS-P3"]["text"] = (f"Driving the same fetch rule from the superseded-names lookup, at the model's fetch budget, puts the record in view for {p3['a']:.4f} against "
                              f"the model's {p3['b']:.4f} on the same 63 items, a difference of {p3['D']:+.4f} (interval {fmt_i(p3['item'])}; persona-clustered {fmt_i(p3['cluster'])}) outside the tolerance. "
                              + ("The lookup fetches what the model does not; on the state the summary names, the model's judgment is not the better gate."
                                 if p3["D"] > 0 else "The model's judgment fetches what the lookup does not; the lookup is not a substitute for it."))
    v4 = p4["D"] > 0.20
    V["DS-P4"] = {"holds": bool(v4), "MA": p4["a"], "M": p4["b"], "D": p4["D"], "item": p4["item"], "cluster": p4["cluster"], "n": 41, "newly_fetchable": len(newly), "gate_on_newly_unretrieved": g_newly}
    if v4:
        V["DS-P4"]["text"] = (f"Naming the retracted and expired attributes makes their records fetchable: the same gate reaches {p4['a']:.4f} of those obligations under the "
                              f"all-three-named summary against {p4['b']:.4f} under the superseded-only names (difference {p4['D']:+.4f}, interval {fmt_i(p4['item'])}; persona-clustered {fmt_i(p4['cluster'])}).")
    else:
        V["DS-P4"]["text"] = (f"Naming the retracted and expired attributes in the summary makes their records fetchable, and the gate elicited under the counting summary "
                              f"reaches them for {p4['a']:.4f} against {p4['b']:.4f} under the superseded-only names, a difference of {p4['D']:+.4f} (interval {fmt_i(p4['item'])}; "
                              f"persona-clustered {fmt_i(p4['cluster'])}) that does not exceed 0.20 on the 41 retraction- and expiry-derived obligations. Of the 41, 19 carry a flagged "
                              f"record; naming makes {len(newly)} of them fetchable that the superseded-only names do not, and the gate fires on {g_newly} of those. The bound on these "
                              f"states is the judgment, not the naming.")
    v5 = abs(p5["D"]) <= TOL
    V["DS-P5"] = {"holds": bool(v5), "C_M": p5["a"], "C_A": p5["b"], "D": p5["D"], "item": p5["item"], "cluster": p5["cluster"], "abstained": a_pres, "abstained_with_gold_in_view": c_pres}
    if v5:
        V["DS-P5"]["text"] = (f"The gate does not cost coverage: on the 174 items whose licensed record the store holds, coverage under the gated policy is within tolerance "
                              f"of retrieval alone ({p5['a']:.4f} against {p5['b']:.4f}, {p5['D']:+.4f}, interval {fmt_i(p5['item'])}; persona-clustered {fmt_i(p5['cluster'])}).")
    else:
        V["DS-P5"]["text"] = (f"Gating on the smallest model's coverage score at the coverage base rate abstains on {a_pres} of the 174 items whose licensed record the store "
                              f"holds, and the licensed record was in the retrieved view for {c_pres} of those; coverage falls from {p5['b']:.4f} to {p5['a']:.4f}, a difference of "
                              f"{p5['D']:+.4f} (interval {fmt_i(p5['item'])}; persona-clustered {fmt_i(p5['cluster'])}) beyond the tolerance. The obligation gate is free; the coverage "
                              f"gate at this threshold is not.")
    S = {"per_item": per, "rates": rates, "verdicts": V, "when": dt.datetime.now().isoformat(timespec="seconds")}
    if write:
        jdump(S, DS / "stage1.json")
    return S


def compare(a, b, path="", out=None):
    out = [] if out is None else out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a:
            if k == "when":
                continue
            if k not in b:
                out.append(path + "/" + k + " missing"); continue
            compare(a[k], b[k], path + "/" + k, out)
    elif isinstance(a, list) and isinstance(b, list):
        for i, (x, y) in enumerate(zip(a, b)):
            compare(x, y, f"{path}[{i}]", out)
        if len(a) != len(b):
            out.append(f"{path}: length {len(a)} != {len(b)}")
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        if not (math.isnan(float(a)) and math.isnan(float(b))) and abs(float(a) - float(b)) > 1e-9:
            out.append(f"{path}: {a} != {b}")
    elif a != b:
        out.append(f"{path}: {str(a)[:40]} != {str(b)[:40]}")
    return out


# ------------------------------------------------------------------ ledger
def ledger(S, n_lines_locked, gold_in_fetch):
    r, V = S["rates"], S["verdicts"]
    today = dt.date.today().isoformat()
    hdr = "| policy | gate fires | abstentions | PN reach all (Wilson) | sup | ret | exp | tagged all | successor in view (all) | PN abstained |\n|---|---:|---:|---|---:|---:|---:|---:|---:|---:|"
    row = lambda p: (f"| {p} | {r[p]['gate_fires']} | {r[p]['abstentions']} | **{r[p]['pn_reach']['all']['reached']} / 104 = {r[p]['pn_reach']['all']['rate']:.4f}** "
                     f"[{r[p]['pn_reach']['all']['wilson'][0]:.3f}, {r[p]['pn_reach']['all']['wilson'][1]:.3f}] | {r[p]['pn_reach']['supersession']['reached']} / 63 | "
                     f"{r[p]['pn_reach']['retraction']['reached']} / 26 | {r[p]['pn_reach']['expiry']['reached']} / 15 | {r[p]['pn_tagged']['all']} | {r[p]['pn_successor']['all']} | {r[p]['pn_abstain']} |")
    vt = lambda k: f"**{'HOLDS' if V[k]['holds'] else 'FAILS'}**"
    txt = f"""
---

## 2. Step 2 — policies, views, Stage 1 (written {today}; no model call)

### AUX-DS-LINELOCK

The five retrieved lines of every view are L2's rendered block byte for byte (`resp_review/l2/retrieval.json`); fetched
lines are rendered by the same function (`resp_common.render_line`) — {n_lines_locked} fetched lines whose entry also
appears in some L2 block match that block's line byte for byte after the rank label; no active entry in any fetch set;
gold entries of PRESENT items in a fetch set: {len(gold_in_fetch)} {('(' + ', '.join(f'{i} under {p}' for i, p in gold_in_fetch[:10]) + ')') if gold_in_fetch else ''}.
`verify_ds.py` check F re-derives every policy, view and Stage 1 flag.

### AUX-DS-POLICIES and AUX-DS-VIEWSIZE

| policy | gate fires (661) | abstentions (661) | mean view size, 661 | max | mean view size, 104 PN | max |
|---|---:|---:|---:|---:|---:|---:|
""" + "\n".join(f"| {p} | {r[p]['gate_fires']} | {r[p]['abstentions']} | {r[p]['view_size']['mean_661']:.2f} | {r[p]['view_size']['max_661']} | {r[p]['view_size']['mean_104']:.2f} | {r[p]['view_size']['max_104']} |" for p in POLICIES) + f"""

### AUX-DS-REACH — Stage 1 PN reach per policy (by id; tagged reach and successor-in-view beside)

{hdr}
""" + "\n".join(row(p) for p in POLICIES) + f"""

ORACLE's flagged ceiling: 82 / 104 (D-DS-1). Tagged reach = the record in view *and* printed non-active.

**DS-P1** (ORACLE − ALWAYS on the 104 > 0.50): {V['DS-P1']['O']:.4f} − {V['DS-P1']['A']:.4f} = **{V['DS-P1']['D']:+.4f}** (item-level {fmt_i(V['DS-P1']['item'])}; persona-clustered {fmt_i(V['DS-P1']['cluster'])}) → {vt('DS-P1')}. Frozen text with its numbers:
> {V['DS-P1']['text']}

**DS-P2** (ρ = (MODEL − ALWAYS) / (ORACLE − ALWAYS) on the 63 supersession-derived items ≥ 0.60 with the item-level interval's lower bound > 0.60; clustered beside, weaker governs): ALWAYS {V['DS-P2']['A']:.4f}, MODEL {V['DS-P2']['M']:.4f}, ORACLE {V['DS-P2']['O']:.4f}; **ρ = {V['DS-P2']['rho']:.4f}**, item-level [{V['DS-P2']['item'].get('ci_lo', float('nan')):.4f}, {V['DS-P2']['item'].get('ci_hi', float('nan')):.4f}] ({V['DS-P2']['item'].get('n_draws')} draws, {V['DS-P2']['item'].get('n_nonpositive_oracle_gain_discarded')} discarded), persona-clustered [{V['DS-P2']['cluster'].get('ci_lo', float('nan')):.4f}, {V['DS-P2']['cluster'].get('ci_hi', float('nan')):.4f}] ({V['DS-P2']['cluster'].get('n_draws')} draws, {V['DS-P2']['cluster'].get('n_nonpositive_oracle_gain_discarded')} discarded); the gate fires on {V['DS-P2']['gate_on_missed']} of the {V['DS-P2']['missed']} supersession items the retriever misses; item-level reading {'holds' if V['DS-P2']['item_reading'] else 'fails'}, clustered reading {'holds' if V['DS-P2']['cluster_reading'] else 'fails'} → {vt('DS-P2')}. Frozen text with its numbers:
> {V['DS-P2']['text']}

**DS-P3** (|LOOKUP − MODEL| on the same 63 ≤ 0.05): LOOKUP {V['DS-P3']['L']:.4f}, MODEL {V['DS-P3']['M']:.4f}, **D = {V['DS-P3']['D']:+.4f}** ({fmt_i(V['DS-P3']['item'])}; {fmt_i(V['DS-P3']['cluster'])}); on the 104: {V['DS-P3']['on_104']['L']:.4f} vs {V['DS-P3']['on_104']['M']:.4f}, {V['DS-P3']['on_104']['D']:+.4f} ({fmt_i(V['DS-P3']['on_104']['item'])}; {fmt_i(V['DS-P3']['on_104']['cluster'])}) → {vt('DS-P3')}. Frozen text with its numbers:
> {V['DS-P3']['text']}

**DS-P4** (MODEL-ALL − MODEL on the 41 retraction- and expiry-derived items > 0.20): MODEL-ALL {V['DS-P4']['MA']:.4f}, MODEL {V['DS-P4']['M']:.4f}, **D = {V['DS-P4']['D']:+.4f}** ({fmt_i(V['DS-P4']['item'])}; {fmt_i(V['DS-P4']['cluster'])}); newly fetchable under v3: {V['DS-P4']['newly_fetchable']}, of which the gate fires on {V['DS-P4']['gate_on_newly_unretrieved']} that the retriever misses → {vt('DS-P4')}. Frozen text with its numbers:
> {V['DS-P4']['text']}

### AUX-DS-PRESENT — coverage on the 174 PRESENT items

| policy | coverage (gold in view ∧ not abstained) | rate (Wilson) | gold in view | abstained | abstained with gold in view |
|---|---:|---|---:|---:|---:|
""" + "\n".join(f"| {p} | {r[p]['present']['coverage']} / 174 | {r[p]['present']['rate']:.4f} [{r[p]['present']['wilson'][0]:.3f}, {r[p]['present']['wilson'][1]:.3f}] | {r[p]['present']['gold_in_view']} | {r[p]['present']['abstained']} | {r[p]['present']['abstained_with_gold_in_view']} |" for p in POLICIES) + f"""

The fetch adds no active record, so gold-in-view is the same under every policy; coverage differs only through abstention (§C.7).

**DS-P5** (|MODEL − ALWAYS| coverage ≤ 0.05): ALWAYS {V['DS-P5']['C_A']:.4f}, MODEL {V['DS-P5']['C_M']:.4f}, **D = {V['DS-P5']['D']:+.4f}** ({fmt_i(V['DS-P5']['item'])}; {fmt_i(V['DS-P5']['cluster'])}); MODEL abstains on {V['DS-P5']['abstained']} PRESENT items, {V['DS-P5']['abstained_with_gold_in_view']} with the licensed record in the five → {vt('DS-P5')}. Frozen text with its numbers:
> {V['DS-P5']['text']}

### AUX-DS-ABSTAIN — abstention on ABSENT items (descriptive)

| policy | abstain on the 383 ABSENT | rate | on the 272 ABSENT of the coverage population | rate | PN abstained (104) |
|---|---:|---:|---:|---:|---:|
""" + "\n".join(f"| {p} | {r[p]['absent']['abstain_383']} | {r[p]['absent']['rate_383']:.4f} | {r[p]['absent']['abstain_272']} | {r[p]['absent']['rate_272']:.4f} | {r[p]['pn_abstain']} |" for p in POLICIES) + "\n"
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    return txt


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sub = DC.load_cell()
    pol, views, n_locked, gold_in_fetch = build(sub)
    S = stage1(sub, pol, views, write=True)
    txt = ledger(S, n_locked, gold_in_fetch)
    print(txt)


if __name__ == "__main__":
    main()
