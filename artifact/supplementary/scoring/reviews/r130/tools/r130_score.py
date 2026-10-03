# -*- coding: utf-8 -*-
"""r130_score.py -- program R130, Task C: the predictions and the per-policy label tables from the judge's rows. Offline, $0.

    python r130_score.py             reads build/build_r130.json, build/judge_units_r130.json, run/rows_ds_r130_judge.jsonl, run/rows_ds_r130_luna.jsonl,
                                     the recorded detector flags (scores_amend4 / scores_amend5 per_row); writes results/r130_scores.json and
                                     results/R130_TABLES.md; appends section 16 of ds_downstream/NUMBERS_DS.md once (refuses a second write).
    --dry-run <dir>                  reads the judge / Luna rows from <dir> (synthetic), writes there, touches no ledger.

Conventions (registration section 5): a judged answer is ASSERTS iff the judge's label is ASSERTS, MENTIONS iff MENTIONS (UNSURE is neither in the
primary reading; the sensitivity row drops UNSURE units from every pairing). Paired differences: exact McNemar (two-sided binomial on the discordant pairs) and the
item-level and persona-grouped percentile bootstraps (10,000 draws, seed 42). Reliable = McNemar p < 0.05 AND the persona-grouped interval
excludes zero. Two-group differences (P-L3): Fisher's exact test in place of McNemar, both bootstraps over the two groups.
"""
from __future__ import annotations

import collections
import io
import json
import pathlib
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r130_common as C  # noqa: E402

RUN = C.RUN


def units_path():
    return pathlib.Path(sys.argv[sys.argv.index("--units") + 1]) if "--units" in sys.argv else C.BUILD / "judge_units_r130.json"


def load(indir=None):
    b = C.J(C.BUILD / "build_r130.json")
    units = {u["unit_id"]: u for u in C.J(units_path())["units"]}
    rj = (pathlib.Path(indir) / "rows_ds_r130_judge.jsonl") if indir else RUN / "rows_ds_r130_judge_assembled.jsonl"
    rl = (pathlib.Path(indir) / "rows_ds_r130_luna.jsonl") if indir else RUN / "rows_ds_r130_luna.jsonl"
    judge = {json.loads(l)["unit_id"]: json.loads(l) for l in io.open(rj, encoding="utf-8") if l.strip()}
    luna = C.read_rows(rl)
    # the recorded detector flags at 0.50 for mini / Haiku (scores_amend4 for a4 keys, scores_amend5 for a5 keys, keyed by the a4 key)
    s4 = C.J(RUN / "scores_amend4.json")["per_row"]; s5 = C.J(RUN / "scores_amend5.json")["per_row"]
    return b, units, judge, luna, s4, s5


class Labels:
    """label(answerer, source, view key) -> the judge's label or None (no row / not OK); pos() -> is the label the positive one (ASSERTS or MENTIONS).
    unsure = 'primary': UNSURE is not ASSERTS and not MENTIONS; 'drop': a UNSURE unit returns None and leaves every pairing it enters (the sensitivity row)."""

    def __init__(self, units, judge, positive="ASSERTS", unsure="primary"):
        assert positive in C.LABELS and unsure in C.UNSURE_MODES
        self.units, self.judge, self.positive, self.unsure = units, judge, positive, unsure
        self.by = {}
        for uid, r in judge.items():
            if r["status"] == "OK":
                u = units[uid]; self.by[(u["answerer"], u["source"], u["key"])] = r["label"]

    def label(self, a, src, key):
        return self.by.get((a, src, key))

    def pos(self, a, src, key):
        l = self.label(a, src, key)
        if l is None or (self.unsure == "drop" and l == "UNSURE"):
            return None
        return l == self.positive

    asserts = pos


def detector_flag(units, s4, s5, luna_det, a, src, key):
    if a == "LUNA":
        return luna_det.get(key)
    if src == "a4":
        return s4[a].get(key, {}).get("stale_use_tau_gold")
    u = next((x for x in units.values() if x["answerer"] == a and x["source"] == "a5" and x["key"] == key), None)
    return s5[a].get(u["key_a4"], {}).get("stale_use_tau_gold") if u else None


def luna_detector(b, luna):
    """The committed detector at 0.50 on Luna's answers (descriptive only: its length bias makes cross-answerer comparison invalid)."""
    D = C.load_ds(); out = {}
    for j in b["jobs"]:
        r = luna.get(j["key"])
        if not r or r["status"] != "OK" or D["rec"].get(j["item_id"]) is None:
            continue
        out[j["key"]] = bool(D["RD"].score_answer(D["byid"][j["item_id"]], D["rec"][j["item_id"]], r["answer"])["stale_use_tau_gold"])
    return out


def policy_tables(b, units, L, det):
    """Per answerer x policy over the answered views (a4 units whose policy list holds the policy; RETAG = the 74 a5 views pooled)."""
    jobs = {j["key"]: j for j in b["jobs"]}
    out = {}
    for a in C.ANSWERERS:
        out[a] = {}
        for p in list(C.POLICIES) + ["RETAG"]:
            keys = [k for k, j in jobs.items() if (j["source"] == "a5" if p == "RETAG" else (j["source"] == "a4" and p in j["policies"]))]
            src = "a5" if p == "RETAG" else "a4"
            labs = {k: L.label(a, src, k) for k in keys}
            judged = [k for k in keys if labs[k] is not None]
            cnt = collections.Counter(labs[k] for k in judged)
            n = len(judged); n_ans = n - cnt["ABSTAINS"]
            ass = sum(1 for k in judged if L.asserts(a, src, k))
            by_state = {}
            for st in ("sup", "ret", "exp"):
                ks = [k for k in judged if jobs[k]["state"] == st]
                by_state[st] = {"n": len(ks), "asserts": sum(1 for k in ks if L.asserts(a, src, k))}
            dflags = [det(a, src, k) for k in judged]; dk = [x for x in dflags if x is not None]
            out[a][p] = {"views": len(keys), "judged": n, "labels": {l: cnt.get(l, 0) for l in C.LABELS}, "asserts": ass, "asserts_rate": (round(ass / n, 4) if n else None),
                         "asserts_wilson": C.wilson(ass, n), "abstains": cnt["ABSTAINS"], "abstains_rate": (round(cnt["ABSTAINS"] / n, 4) if n else None),
                         "safe": cnt["MENTIONS"] + cnt["CLEAN"], "safe_of_answered": (round((cnt["MENTIONS"] + cnt["CLEAN"]) / n_ans, 4) if n_ans else None),
                         "safe_of_judged": (round((cnt["MENTIONS"] + cnt["CLEAN"]) / n, 4) if n else None), "answered_non_abstaining": n_ans, "by_state": by_state,
                         "detector_flag_0_50": {"flagged": sum(dk), "scored": len(dk)}}
    return out


def paired(L, a1, s1, a2, s2, keys1, keys2, personas, direction):
    """Paired comparison of L's positive label between (a1, s1, keys1[i]) and (a2, s2, keys2[i]); direction: 'second_below_first' or 'second_above_first'."""
    x, y, pers, rows = [], [], [], []
    for k1, k2, p in zip(keys1, keys2, personas):
        u, v = L.asserts(a1, s1, k1), L.asserts(a2, s2, k2)
        if u is None or v is None:
            continue
        x.append(int(u)); y.append(int(v)); pers.append(p); rows.append((k1, k2, int(u), int(v)))
    n = len(x); b = sum(1 for u, v in zip(x, y) if u and not v); c = sum(1 for u, v in zip(x, y) if v and not u)
    p_mc = C.mcnemar_exact(b, c); boot = C.boot_paired(x, y, pers)
    d = boot["delta"]
    if n == 0 or d is None:
        return {"n": 0, "verdict": "NOT EVALUABLE"}
    excl = (boot["cluster"][1] < 0) if direction == "second_below_first" else (boot["cluster"][0] > 0)
    excl_item = (boot["item"][1] < 0) if direction == "second_below_first" else (boot["item"][0] > 0)
    right = (d < 0) if direction == "second_below_first" else (d > 0)
    reliable = bool(p_mc < 0.05 and excl)
    return {"n": n, "label": L.positive, "unsure": L.unsure, "first": {"asserts": sum(x), "rate": round(sum(x) / n, 4)}, "second": {"asserts": sum(y), "rate": round(sum(y) / n, 4)},
            "delta_second_minus_first": d, "discordant": {"first_only": b, "second_only": c}, "mcnemar_p": round(p_mc, 4), "ci_item": boot["item"], "ci_persona": boot["cluster"],
            "n_personas": boot["n_clusters"], "direction_as_predicted": bool(right), "reliable": reliable, "persona_interval_excludes_zero": bool(excl), "item_interval_excludes_zero": bool(excl_item),
            "verdict": "HELD" if (right and reliable) else ("FAILED (direction as predicted, not reliable)" if right else ("FAILED (no difference)" if d == 0 else "FAILED (direction against)")),
            "rows": rows}


def two_group(L, a, src, keys1, pers1, keys0, pers0, direction):
    y1 = [(k, p, L.asserts(a, src, k)) for k, p in zip(keys1, pers1)]; y0 = [(k, p, L.asserts(a, src, k)) for k, p in zip(keys0, pers0)]
    y1 = [t for t in y1 if t[2] is not None]; y0 = [t for t in y0 if t[2] is not None]
    if not y1 or not y0:
        return {"n1": len(y1), "n0": len(y0), "verdict": "NOT EVALUABLE"}
    k1, k0 = sum(int(t[2]) for t in y1), sum(int(t[2]) for t in y0)
    p_f = C.fisher(k1, len(y1) - k1, k0, len(y0) - k0)
    boot = C.boot_two_group([int(t[2]) for t in y1], [t[1] for t in y1], [int(t[2]) for t in y0], [t[1] for t in y0])
    d = boot["delta"]; excl = (boot["cluster"][0] > 0) if direction == "first_above_second" else (boot["cluster"][1] < 0)
    right = (d > 0) if direction == "first_above_second" else (d < 0); reliable = bool(p_f < 0.05 and excl)
    return {"n1": len(y1), "n0": len(y0), "label": L.positive, "unsure": L.unsure, "group1": {"asserts": k1, "rate": round(k1 / len(y1), 4), "wilson": C.wilson(k1, len(y1))}, "group0": {"asserts": k0, "rate": round(k0 / len(y0), 4), "wilson": C.wilson(k0, len(y0))},
            "delta_group1_minus_group0": d, "fisher_p": round(p_f, 4), "ci_item": boot["item"], "ci_persona": boot["cluster"], "n_personas": boot["n_clusters"],
            "direction_as_predicted": bool(right), "reliable": reliable, "persona_interval_excludes_zero": bool(excl),
            "verdict": "HELD" if (right and reliable) else ("FAILED (direction as predicted, not reliable)" if right else ("FAILED (no difference)" if d == 0 else "FAILED (direction against)"))}


def predictions(b, L, M):
    """L: the ASSERTS reader, M: the MENTIONS reader (the same unsure mode)."""
    D_views = C.J(C.DS / "views.json")["items"]
    byid = {j["item_id"]: j for j in b["jobs"]}
    pops = b["census"]["populations"]
    key_of = lambda i, p: f"{i}|{D_views[i][p]['sha']}"     # noqa: E731
    pers = lambda ids: [byid[i]["persona"] for i in ids]   # noqa: E731
    out = {}
    # P-L1 (oracle view, tagged reach, all states) and P-L1b (the lookup version): mini (first) against Luna (second), Luna below mini
    for name, pol in (("P-L1", "ORACLE"), ("P-L1b", "LOOKUP")):
        ids = pops[name]["obligations"]; ks = [key_of(i, pol) for i in ids]
        which = "oracle fetch" if pol == "ORACLE" else "lookup rule"
        out[name] = {"registered": f"among obligations whose tagged forbidding record is in view under the {which}, Luna's ASSERTS rate is below GPT-4.1 mini's; paired by obligation" + ("" if pol == "ORACLE" else " (secondary)"),
                     "population": f"the {len(ids)} obligations answered under the {pol} policy whose forbidding record is in view and tagged (stage 1 tagged_reach); by state {pops[name]['by_state']}",
                     **paired(L, "MINI", "a4", "LUNA", "a4", ks, ks, pers(ids), "second_below_first")}
        out[name]["haiku_to_luna_beside"] = paired(L, "H45", "a4", "LUNA", "a4", ks, ks, pers(ids), "second_below_first")
        out[name]["mini_to_haiku_beside"] = paired(L, "MINI", "a4", "H45", "a4", ks, ks, pers(ids), "second_below_first")
    # P-L4: the P-L1 pairs, MENTIONS, Luna above mini
    ids = pops["P-L1"]["obligations"]; ks = [key_of(i, "ORACLE") for i in ids]
    out["P-L4"] = {"registered": "on the P-L1 pairs (oracle view, tagged reach), Luna's MENTIONS rate is above GPT-4.1 mini's; paired by obligation",
                   "population": out["P-L1"]["population"], **paired(M, "MINI", "a4", "LUNA", "a4", ks, ks, pers(ids), "second_above_first")}
    out["P-L4"]["haiku_to_luna_beside"] = paired(M, "H45", "a4", "LUNA", "a4", ks, ks, pers(ids), "second_above_first")
    out["P-L4"]["mini_to_haiku_beside"] = paired(M, "MINI", "a4", "H45", "a4", ks, ks, pers(ids), "second_above_first")
    # P-L2: within Luna, ALWAYS (first) against LOOKUP (second) over the 40 obligations answered under both
    ids = pops["P-L2"]["obligations"]; ka = [key_of(i, "ALWAYS") for i in ids]; kl = [key_of(i, "LOOKUP") for i in ids]
    out["P-L2"] = {"registered": "within Luna, the ASSERTS rate under the lookup rule is below its rate under top-five retrieval, over all judged obligations; paired",
                   "population": f"the {len(ids)} obligations answered under both policies ({pops['P-L2']['n_same_view']} with the same view under both, so concordant by construction; {pops['P-L2']['n_informative']} informative pairs)",
                   **paired(L, "LUNA", "a4", "LUNA", "a4", ka, kl, pers(ids), "second_below_first")}
    for a in ("MINI", "H45"):
        out["P-L2"][f"{a.lower()}_beside"] = paired(L, a, "a4", a, "a4", ka, kl, pers(ids), "second_below_first")
    # the 'of 104' reading: every obligation, an unanswered policy counting as not ASSERTS (descriptive)
    obl = sorted({j["item_id"] for j in b["jobs"]} | set(b["census"]["unreached"]))
    assert len(obl) == 104, len(obl)
    st1 = C.J(C.DS / "stage1.json")["per_item"]

    def of104(a, p):
        v = []
        for i in obl:
            s_ = st1[i][p]
            if s_["reach"] and not s_["abstain"]:
                x = L.pos(a, "a4", key_of(i, p)); v.append(None if x is None else int(x))
            else:
                v.append(0)
        return v
    o104 = {}
    for a in C.ANSWERERS:
        x, y = of104(a, "ALWAYS"), of104(a, "LOOKUP"); keep = [i for i in range(104) if x[i] is not None and y[i] is not None]
        xs, ys = [x[i] for i in keep], [y[i] for i in keep]; ps = [obl[i].split(":")[1] for i in keep]
        bb = sum(1 for u, v in zip(xs, ys) if u and not v); cc = sum(1 for u, v in zip(xs, ys) if v and not u); boot = C.boot_paired(xs, ys, ps)
        o104[a] = {"n": len(keep), "always_asserts": sum(xs), "lookup_asserts": sum(ys), "delta": boot["delta"], "discordant": {"always_only": bb, "lookup_only": cc},
                   "mcnemar_p": round(C.mcnemar_exact(bb, cc), 4), "ci_item": boot["item"], "ci_persona": boot["cluster"]}
    out["P-L2"]["of_104_reading"] = {"rule": "every obligation; a policy that did not answer it (unreached or abstained) counts as not ASSERTS (Table tab:ds-body's convention); descriptive", **o104}
    # P-L3 (oracle, the audited scorable views) and P-L3b (lookup): Luna, an untagged active copy in view (group 1) against without (group 0): above
    for name, pol in (("P-L3", "ORACLE"), ("P-L3b", "LOOKUP")):
        p3 = pops[name]; k1 = [key_of(i, pol) for i in p3["active"]]; k0 = [key_of(i, pol) for i in p3["without"]]
        which = "oracle fetch" if pol == "ORACLE" else "lookup rule"
        tail = f"; {p3['answered_of_audited']} of the {p3['audited_scorable_views']} audited scorable views" if pol == "ORACLE" else f"; expiry ({p3['expiry_excluded']}) excluded"
        out[name] = {"registered": f"under the {which}, Luna's ASSERTS rate on views holding an untagged active copy of the stale value is above its rate on views without one" + ("" if pol == "ORACLE" else " (secondary)"),
                     "population": f"the {p3['n_active'] + p3['n_without']} supersession and retraction obligations answered under {pol}: {p3['n_active']} whose view holds an active line asserting the stale value (amend4_header.view_source), {p3['n_without']} without" + tail,
                     **two_group(L, "LUNA", "a4", k1, pers(p3["active"]), k0, pers(p3["without"]), "first_above_second")}
        for a in ("MINI", "H45"):
            out[name][f"{a.lower()}_beside"] = two_group(L, a, "a4", k1, pers(p3["active"]), k0, pers(p3["without"]), "first_above_second")
        pc = p3["corrected"]; k1c = [key_of(i, pol) for i in pc["active"]]; k0c = [key_of(i, pol) for i in pc["without"]]
        out[name]["corrected_tag_beside"] = {"note": pc["note"], **{a: two_group(L, a, "a4", k1c, pers(pc["active"]), k0c, pers(pc["without"]), "first_above_second") for a in C.ANSWERERS}}
    # the retag variant, all three answerers: before (a4 key) against after (a5 key) over the 74 changed views, paired by view
    a5 = [j for j in b["jobs"] if j["source"] == "a5"]
    out["RETAG"] = {"population": "the 74 views the reference-assisted retag changed (45 supersession, 29 retraction), before (Amendment 4 view) against after (the retagged view), paired by view; descriptive",
                    **{a: paired(L, a, "a4", a, "a5", [j["key_a4"] for j in a5], [j["key"] for j in a5], [j["persona"] for j in a5], "second_below_first") for a in C.ANSWERERS}}
    out["RETAG"]["mentions"] = {a: paired(M, a, "a4", a, "a5", [j["key_a4"] for j in a5], [j["key"] for j in a5], [j["persona"] for j in a5], "second_above_first") for a in C.ANSWERERS}
    return out


PRED_ORDER = ("P-L1", "P-L1b", "P-L4", "P-L2", "P-L3", "P-L3b")
PRED_TITLE = {"P-L1": "P-L1 (mini -> Luna, oracle view, tagged reach, all states; ASSERTS below)", "P-L1b": "P-L1b (mini -> Luna, lookup view, tagged reach; ASSERTS below; secondary)",
              "P-L4": "P-L4 (mini -> Luna, the P-L1 pairs; MENTIONS above)", "P-L2": "P-L2 (Luna: top-five -> lookup, the 40 answered under both; ASSERTS below)",
              "P-L3": "P-L3 (Luna, oracle view: active copy vs without; ASSERTS above)", "P-L3b": "P-L3b (Luna, lookup view: active copy vs without; ASSERTS above; secondary)"}


def fmt_pred(x):
    if "n1" in x:
        if not x.get("n1") or not x.get("n0"):
            return "| | | | | | | | NOT EVALUABLE |"
        return (f"| {x['n1']} + {x['n0']} | with {x['group1']['asserts']} ({x['group1']['rate']}) | without {x['group0']['asserts']} ({x['group0']['rate']}) | {x['delta_group1_minus_group0']:+.4f} | Fisher | {x['fisher_p']} | "
                f"{x['ci_item']} | {x['ci_persona']} | {x['verdict']} |")
    if not x.get("n"):
        return "| 0 | | | | | | | | NOT EVALUABLE |"
    return (f"| {x['n']} | {x['first']['asserts']} ({x['first']['rate']}) | {x['second']['asserts']} ({x['second']['rate']}) | {x['delta_second_minus_first']:+.4f} | "
            f"{x['discordant']['first_only']} / {x['discordant']['second_only']} | {x['mcnemar_p']} | {x['ci_item']} | {x['ci_persona']} | {x['verdict']} |")


def beside_line(name, x):
    if "n1" in x:
        return f"- {name}: with {x['group1']['asserts']}/{x['n1']} vs without {x['group0']['asserts']}/{x['n0']}, delta {x['delta_group1_minus_group0']:+.4f}, Fisher p {x['fisher_p']}, item {x['ci_item']}, persona {x['ci_persona']}" if x.get("n1") and x.get("n0") else f"- {name}: NOT EVALUABLE"
    return f"- {name}: n {x['n']}, {x['first']['asserts']} -> {x['second']['asserts']}, delta {x['delta_second_minus_first']:+.4f}, discordant {x['discordant']['first_only']} / {x['discordant']['second_only']}, p {x['mcnemar_p']}, item {x['ci_item']}, persona {x['ci_persona']}" if x.get("n") else f"- {name}: NOT EVALUABLE"


def tables(S):
    L = [f"# R130 tables (written {S['when']}; exploratory; judge validation: {S.get('validation_status', 'labels not yet released')})\n"]
    L.append("\n## Per-policy labels (the judge's; over the views the E.10 answer stage answered under the policy; RETAG = the 74 retagged views pooled)\n")
    L.append("| answerer | policy | views judged | ASSERTS | MENTIONS | CLEAN | ABSTAINS | UNSURE | ASSERTS rate [Wilson] | safe (M+C) of non-abstaining | ABSTAINS rate | sup / ret / exp ASSERTS | detector flag 0.50 |\n|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|")
    for a in C.ANSWERERS:
        for p, d in S["policy_tables"][a].items():
            lb = d["labels"]; bs = d["by_state"]
            L.append(f"| {C.ANSWERER_NAME[a]} | {C.POLICY_NAME[p]} | {d['judged']} | {lb['ASSERTS']} | {lb['MENTIONS']} | {lb['CLEAN']} | {lb['ABSTAINS']} | {lb['UNSURE']} | "
                     f"{d['asserts_rate']} {d['asserts_wilson']} | {d['safe']} / {d['answered_non_abstaining']} = {d['safe_of_answered']} | {d['abstains_rate']} | "
                     f"{bs['sup']['asserts']}/{bs['sup']['n']} / {bs['ret']['asserts']}/{bs['ret']['n']} / {bs['exp']['asserts']}/{bs['exp']['n']} | {d['detector_flag_0_50']['flagged']} / {d['detector_flag_0_50']['scored']} |")
    P = S["predictions"]
    L.append("\n## Predictions (primary reading: UNSURE is not ASSERTS and not MENTIONS; HELD = predicted direction AND exact McNemar / Fisher p < 0.05 AND the persona-grouped interval excluding zero)\n")
    L.append("| prediction | n | first / with | second / without | delta | discordant (first only / second only) | p | item interval | persona interval | verdict |\n|---|---:|---|---|---|---|---|---|---|---|")
    for k in PRED_ORDER:
        L.append(f"| {PRED_TITLE[k]} " + fmt_pred(P[k]))
    L.append("\n## Beside (descriptive, no bar)\n")
    for k in ("P-L1", "P-L1b", "P-L4"):
        L.append(beside_line(f"{k} read Haiku -> Luna", P[k]["haiku_to_luna_beside"])); L.append(beside_line(f"{k} read mini -> Haiku", P[k]["mini_to_haiku_beside"]))
    for a in ("mini", "h45"):
        L.append(beside_line(f"P-L2 read for {a}", P["P-L2"][f"{a}_beside"]))
        for k in ("P-L3", "P-L3b"):
            L.append(beside_line(f"{k} read for {a}", P[k][f"{a}_beside"]))
    o = P["P-L2"]["of_104_reading"]
    L.append("- P-L2, the 'of 104' reading (unanswered = not ASSERTS): " + "; ".join(f"{C.ANSWERER_NAME[a]} top-five {o[a]['always_asserts']} -> lookup {o[a]['lookup_asserts']} of {o[a]['n']} (delta {o[a]['delta']:+.4f}, p {o[a]['mcnemar_p']}, persona {o[a]['ci_persona']})" for a in C.ANSWERERS))
    for k in ("P-L3", "P-L3b"):
        c = P[k]["corrected_tag_beside"]
        L.append(f"- {k} with the fatima_q06 tag corrected on paper: " + "; ".join(f"{C.ANSWERER_NAME[a]} with {c[a]['group1']['asserts']}/{c[a]['n1']} vs without {c[a]['group0']['asserts']}/{c[a]['n0']} (delta {c[a]['delta_group1_minus_group0']:+.4f}, Fisher p {c[a]['fisher_p']}, persona {c[a]['ci_persona']})" for a in C.ANSWERERS if c[a].get("n1")))
    R = P["RETAG"]
    L.append("\n## The retag variant (the 74 changed views, before -> after, paired by view; descriptive)\n")
    L.append("| answerer | n | ASSERTS before | ASSERTS after | delta | discordant (before only / after only) | McNemar p | item interval | persona interval | MENTIONS before -> after (delta, p) |\n|---|---:|---:|---:|---|---|---|---|---|---|")
    for a in C.ANSWERERS:
        x = R[a]; m = R["mentions"][a]
        if x.get("n"):
            L.append(f"| {C.ANSWERER_NAME[a]} | {x['n']} | {x['first']['asserts']} | {x['second']['asserts']} | {x['delta_second_minus_first']:+.4f} | {x['discordant']['first_only']} / {x['discordant']['second_only']} | {x['mcnemar_p']} | {x['ci_item']} | {x['ci_persona']} | "
                     + (f"{m['first']['asserts']} -> {m['second']['asserts']} ({m['delta_second_minus_first']:+.4f}, p {m['mcnemar_p']}) |" if m.get("n") else "|"))
    L.append(f"\nThe 20 byte-identical retag pairs (same text before and after): the judge gave the same label to both on {S['identical_pairs']['same_label']} of {S['identical_pairs']['n']} for mini and {S['identical_pairs']['same_label_h45']} of {S['identical_pairs']['n_h45']} for Haiku (intra-judge consistency, descriptive).\n")
    S2 = S["sensitivity_drop_unsure"]
    L.append("\n## Sensitivity: UNSURE units dropped from every pairing\n")
    L.append("| prediction | n | delta | p | persona interval | verdict |\n|---|---:|---|---|---|---|")
    for k in PRED_ORDER:
        x = S2[k]
        if "n1" in x and x.get("n1"):
            L.append(f"| {k} | {x['n1']} + {x['n0']} | {x['delta_group1_minus_group0']:+.4f} | {x['fisher_p']} | {x['ci_persona']} | {x['verdict']} |")
        elif x.get("n"):
            L.append(f"| {k} | {x['n']} | {x['delta_second_minus_first']:+.4f} | {x['mcnemar_p']} | {x['ci_persona']} | {x['verdict']} |")
        else:
            L.append(f"| {k} | 0 | | | | NOT EVALUABLE |")
    L.append(f"\n## Rows\n\nJudge rows {S['rows']['judge']['n']} (OK {S['rows']['judge']['ok']}, by status {S['rows']['judge']['status']}); Luna rows {S['rows']['luna']['n']} (OK {S['rows']['luna']['ok']}, by status {S['rows']['luna']['status']}); "
             f"judge label distribution over all rows {S['rows']['judge']['labels']}; Luna answers the detector flags at 0.50 (descriptive): {S['rows']['luna']['detector_flagged']} of {S['rows']['luna']['detector_scored']}; Luna's mean answer length {S['rows']['luna']['mean_answer_chars']} characters.\n")
    return "\n".join(L) + "\n"


def ledger_text(S):
    P = S["predictions"]; sp = S["spend"]

    def f(x):
        if "n1" in x:
            return (f"with {x['group1']['asserts']} / {x['n1']} = {x['group1']['rate']} against without {x['group0']['asserts']} / {x['n0']} = {x['group0']['rate']}, delta {x['delta_group1_minus_group0']:+.4f}, "
                    f"Fisher p {x['fisher_p']}, item {x['ci_item']}, persona {x['ci_persona']}: **{x['verdict']}**") if x.get("n1") and x.get("n0") else "NOT EVALUABLE"
        return (f"n {x['n']}, {x['first']['asserts']} -> {x['second']['asserts']}, delta {x['delta_second_minus_first']:+.4f}, discordant {x['discordant']['first_only']} / {x['discordant']['second_only']}, "
                f"McNemar p {x['mcnemar_p']}, item {x['ci_item']}, persona {x['ci_persona']}: **{x['verdict']}**") if x.get("n") else "NOT EVALUABLE"
    rows = [f"| {C.ANSWERER_NAME[a]} | {C.POLICY_NAME[p]} | {d['judged']} | {d['labels']['ASSERTS']} | {d['labels']['MENTIONS']} | {d['labels']['CLEAN']} | {d['labels']['ABSTAINS']} | {d['labels']['UNSURE']} | {d['asserts_rate']} {d['asserts_wilson']} | {d['safe_of_answered']} |"
            for a in C.ANSWERERS for p, d in S["policy_tables"][a].items()]
    return (f"\n## 16. Program R130 (2026-09-{S['when'][8:10]}): GPT-5.6 Luna as a third answerer on the recorded E.10 views, and a semantic judge (Opus 5) over the three answerers' answers "
            f"(reviews/r130/; exploratory; registration reviews/r130/registrations/REGISTRATION_R130.md, sha `{S['registration_sha256'][:16]}`)\n\n"
            f"### AUX-R130-POP\n\n{S['build']['n_views']} views ({S['build']['n_views_a4']} of the Amendment 4 population, label PRESENT-NEGATIVE, over the seven policies; {S['build']['n_views_a5']} retagged); "
            f"judge units {S['rows']['judge']['n']} ({S['rows']['judge']['ok']} OK). Luna rows {S['rows']['luna']['n']} ({S['rows']['luna']['ok']} OK), served `{S['rows']['luna']['served']}`.\n\n"
            f"### AUX-R130-POLICY-TABLE\n\n| answerer | policy | views judged | ASSERTS | MENTIONS | CLEAN | ABSTAINS | UNSURE | ASSERTS rate [Wilson] | safe (M+C) of non-abstaining |\n|---|---|---:|---:|---:|---:|---:|---:|---|---|\n" + "\n".join(rows) + "\n\n"
            f"### AUX-R130-PL1, AUX-R130-PL1B, AUX-R130-PL4, AUX-R130-PL2, AUX-R130-PL3, AUX-R130-PL3B (primary reading; the drop-UNSURE sensitivity in results/R130_TABLES.md)\n\n"
            + "\n\n".join(f"{PRED_TITLE[k]}: {f(P[k])}." for k in PRED_ORDER) + "\n\n"
            f"### AUX-R130-RETAG\n\n" + "; ".join(f"{C.ANSWERER_NAME[a]}: {f(P['RETAG'][a])}" for a in C.ANSWERERS) + "\n\n"
            f"### AUX-R130-SPEND\n\nToken-metered at the page prices: OpenAI ${sp['openai']:.4f} of the $4.00 cap (Luna {sp['luna_rows']:.4f}, probe {sp['probe_luna']:.4f}); "
            f"Anthropic ${sp['anthropic']:.4f} against the registered $8.00 cap, raised to $10.00 for the judge lane by D-R130-5 (the cancelled-then-settled Batch {sp['judge_batch']:.4f} at the 0.5 rate, "
            f"the synchronous run {sp['judge_sync_rows']:.4f}, the re-asks at max_tokens 1024 {sp['judge_reask_rows']:.4f}, the insurance check {sp['judge_insurance']:.4f}, probe {sp['probe_judge']:.4f}). "
            f"Judge transports in the assembled lane: {S['transports']}.\n"
            f"\nValidation against the human labels: {S.get('validation_status', 'labels not yet released (AUX-R130-VALIDATION to follow)')}.\n")


def identical_pairs(b, units, judge):
    """The retag pairs whose after answer is byte-identical to the before answer: does the judge give both the same label?"""
    out = {}
    for a, suffix in (("MINI", ""), ("H45", "_h45")):
        by = {(u["source"], u["key"]): u for u in units.values() if u["answerer"] == a}
        n = same = 0
        for j in b["jobs"]:
            if j["source"] != "a5":
                continue
            ub, ua = by.get(("a4", j["key_a4"])), by.get(("a5", j["key"]))
            if ub and ua and ub["answer"] == ua["answer"]:
                rb, ra = judge.get(ub["unit_id"]), judge.get(ua["unit_id"])
                if rb and ra and rb["status"] == "OK" and ra["status"] == "OK":
                    n += 1; same += rb["label"] == ra["label"]
        out["n" + suffix] = n; out["same_label" + suffix] = same
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    dry = "--dry-run" in sys.argv; indir = sys.argv[sys.argv.index("--dry-run") + 1] if dry else None
    if not dry:
        C.assert_frozen(); C.assert_inputs(); C.assert_judge_prompt()
    b, units, judge, luna, s4, s5 = load(indir)
    ld = luna_detector(b, luna)
    det = lambda a, src, k: detector_flag(units, s4, s5, ld, a, src, k)   # noqa: E731
    L, M = Labels(units, judge, "ASSERTS"), Labels(units, judge, "MENTIONS")
    S = {"program": C.PROGRAM, "registration_sha256": C.reg_sha() if C.REG.exists() else None, "when": C.now(), "build": b["meta"],
         "rows": {"judge": {"n": len(judge), "ok": sum(1 for r in judge.values() if r["status"] == "OK"), "status": dict(collections.Counter(r["status"] for r in judge.values())),
                            "labels": dict(collections.Counter(r.get("label") or "NONE" for r in judge.values())), "served": sorted({r.get("served_model") for r in judge.values() if r.get("served_model")})},
                  "luna": {"n": len(luna), "ok": sum(1 for r in luna.values() if r["status"] == "OK"), "status": dict(collections.Counter(r["status"] for r in luna.values())),
                           "served": sorted({r.get("served_model") for r in luna.values() if r.get("served_model")}), "detector_flagged": sum(ld.values()), "detector_scored": len(ld),
                           "mean_answer_chars": (round(sum(len(r["answer"]) for r in luna.values() if r["status"] == "OK") / max(1, sum(1 for r in luna.values() if r["status"] == "OK")), 1))}},
         "policy_tables": policy_tables(b, units, L, det), "predictions": predictions(b, L, M), "identical_pairs": identical_pairs(b, units, judge)}
    Ld, Md = Labels(units, judge, "ASSERTS", "drop"), Labels(units, judge, "MENTIONS", "drop")
    S2 = predictions(b, Ld, Md); S["sensitivity_drop_unsure"] = {k: S2[k] for k in PRED_ORDER}
    pr = C.J(RUN / "probes_r130.json") if (RUN / "probes_r130.json").exists() else {}
    def usd_of(pth):
        return sum(json.loads(l).get("usd", 0.0) for l in io.open(pth, encoding="utf-8") if l.strip()) if pth.exists() else 0.0
    bt = C.J(RUN / "batch_r130_judge.json") if (RUN / "batch_r130_judge.json").exists() else {}
    ins = C.J(RUN / "insurance_r130.json") if (RUN / "insurance_r130.json").exists() else {}
    S["spend"] = {"luna_rows": sum(r.get("usd", 0.0) for r in luna.values()), "probe_luna": pr.get("LUNA", {}).get("usd", 0.0), "probe_judge": pr.get("JUDGE", {}).get("usd", 0.0),
                  "judge_batch": bt.get("billed_usd", 0.0), "judge_sync_rows": usd_of(RUN / "rows_ds_r130_judge.jsonl") if not dry else 0.0,
                  "judge_reask_rows": usd_of(RUN / "rows_ds_r130_judge_reask.jsonl") if not dry else 0.0, "judge_insurance": ins.get("usd", 0.0),
                  "caps": {"openai": C.CAP["openai"], "anthropic_registered": C.CAP["anthropic"], "anthropic_lane_D_R130_5": 10.00}}
    S["spend"]["judge_rows"] = S["spend"]["judge_batch"] + S["spend"]["judge_sync_rows"] + S["spend"]["judge_reask_rows"] + S["spend"]["judge_insurance"]
    S["spend"]["openai"] = S["spend"]["luna_rows"] + S["spend"]["probe_luna"]; S["spend"]["anthropic"] = S["spend"]["judge_rows"] + S["spend"]["probe_judge"]
    S["transports"] = dict(collections.Counter((r.get("transport") if r["status"] == "OK" else "PARSE_FAIL") for r in judge.values()))
    outdir = pathlib.Path(indir) if dry else C.RES
    # the author's constraint of 2026-09-20 (A2's sheet unlabelled): the scores file and everything printed stay aggregate; per-pair rows go to a separate file
    items = {}

    def strip(node, path):
        if isinstance(node, dict):
            if "rows" in node and isinstance(node["rows"], list):
                items[path] = node.pop("rows")
            for k, v in list(node.items()):
                strip(v, f"{path}/{k}")
    strip(S, "")
    C.jdump({"note": "item-level material of r130_scores.json (the per-pair rows: view keys and the two binary readings); not displayed while A2's sheet is unlabelled", "pairs": items}, outdir / "r130_item_level.json")
    C.jdump(S, outdir / "r130_scores.json")
    txt = tables(S)
    io.open(outdir / "R130_TABLES.md", "w", encoding="utf-8", newline="\n").write(txt)
    print(txt)
    if not dry:
        led = C.LEDGER.read_text(encoding="utf-8")
        assert "## 16. Program R130" not in led, "section 16 exists already in NUMBERS_DS.md -- refusing a second write"
        with io.open(C.LEDGER, "a", encoding="utf-8", newline="\n") as f:
            f.write(ledger_text(S))
        print("NUMBERS_DS.md section 16 appended")


if __name__ == "__main__":
    main()
