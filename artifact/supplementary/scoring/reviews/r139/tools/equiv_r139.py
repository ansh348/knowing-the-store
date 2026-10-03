# -*- coding: utf-8 -*-
"""equiv_r139.py -- R139 Phase 1.1 (post hoc; 2026-09-22; $0, no model call): equivalence within 0.05 for every model-minus-lookup row the paper prints
for the five conditions of Phase 0.3, plus the B6 row, by two one-sided tests at 5%.

Rule (reviews/r139/BRANCHES_R139.md, committed before this script ran): equivalent := both 90% intervals (item-level or triple-level, and
persona-grouped) lie inside [-0.05, +0.05]; reliable (unchanged) := both 95% intervals exclude zero. The 90% interval is taken from the SAME 1,000
draws (seed 42) that give the printed 95% interval: the two shared estimators' summaries (e1r_robustness/tools/common_e1r.py:_summarise, pooled;
reviews/r125/tools/r125_common.py:_summarise, matched) are wrapped here at run time so that they return the 5th and 95th percentiles beside the
2.5th and 97.5th; the modules on disk are not edited. Every 95% interval this script computes is asserted equal (to 5e-5) to the stored result the
paper prints it from, so the 90% interval is read off the printed draws.

Rows (the printed tables, Appendix C.2):
  default summary   pooled, supersession: tab:sup-margins (six rows) = tab:cfpad-minus-lookup's unpadded panel; pooled, whole: tab:cfpad-whole's unpadded panel;
                    matched, whole and supersession: tab:cf-matched-vs (the model rows)
  sibling control   matched, PN vs sibling: tab:cf-sibling's 'minus the name lookup' panel
  all-states        matched, whole and supersession: tab:cf-matched-vs' all-states rows; pooled, whole: Table 1's Opus row
  paraphrase set    pooled, whole: tab:para-minus-lookup (paraphrases and originals); pooled and matched, supersession: tab:para-sup
  padded set        pooled and matched, supersession: tab:cfpad-minus-lookup's padded panel; whole: tab:cfpad-whole's padded panel
  B6                the lookup with one count feature minus each of Luna, Sol and Opus, matched, 148 triples (Table 1 footnote b; tab:cf-hybrid)
Writes reviews/r139/results/equiv_r139.json. Usage: python reviews/r139/tools/equiv_r139.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews" / "r139" / "results" / "equiv_r139.json"
for p in ("e1r_robustness/tools", "reviews/r125/tools", "r82_counterfactual/tools", "r82_counterfactual", "cf_pad/tools", "cf2_paraphrase/tools"):
    sys.path.insert(0, str(ROOT / p))

import numpy as np  # noqa: E402
import common_e1r  # noqa: E402
import r125_common  # noqa: E402

TOL = 0.05


def _summarise_both(d):
    """The shared estimators' summary with the 90% (5th, 95th) percentiles beside the printed 95% ones, from the same draws."""
    d = np.asarray(d, float)
    if not len(d):
        return {"n_draws": 0, "note": "no draw"}
    lo, hi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    lo90, hi90 = float(np.percentile(d, 5.0)), float(np.percentile(d, 95.0))
    return {"n_draws": int(len(d)), "mean": float(d.mean()), "ci_lo": lo, "ci_hi": hi, "excludes_zero": bool(lo > 0 or hi < 0), "ci90_lo": lo90, "ci90_hi": hi90}


common_e1r._summarise = _summarise_both
r125_common._summarise = _summarise_both

ROWS = []
CHECKS = []


def J(rel):
    return json.load(open(ROOT / rel, encoding="utf-8"))


def row(condition, table, reader, scope, metric, res, a_key, b_key, stored=None, note=""):
    a, b = res[a_key], res[b_key]
    for k in ("ci90_lo", "ci90_hi"):
        assert k in a and k in b, (condition, reader, scope, metric, "the wrapped summary was not used")
    rel = bool(a["excludes_zero"] and b["excludes_zero"])
    eq = bool(a["ci90_lo"] >= -TOL and a["ci90_hi"] <= TOL and b["ci90_lo"] >= -TOL and b["ci90_hi"] <= TOL)
    r = dict(condition=condition, table=table, reader=reader, scope=scope, metric=metric, delta=float(res["delta"]),
             ci95_a=[a["ci_lo"], a["ci_hi"]], ci95_persona=[b["ci_lo"], b["ci_hi"]], ci90_a=[a["ci90_lo"], a["ci90_hi"]], ci90_persona=[b["ci90_lo"], b["ci90_hi"]],
             a_kind="item" if metric == "pooled" else "triple", reliable=rel, equivalent=eq,
             reading="reliable" if rel else ("equivalent within 0.05" if eq else "neither shown nor excluded"), note=note)
    if stored is not None:
        sd, sa, sb = stored
        ok = abs(sd - r["delta"]) < 5e-5 and all(abs(x - y) < 5e-5 for x, y in zip(sa + sb, r["ci95_a"] + r["ci95_persona"]))
        CHECKS.append(dict(row=f"{condition} | {reader} | {scope} | {metric}", ok=ok, stored=[sd, sa, sb], computed=[r["delta"], r["ci95_a"], r["ci95_persona"]]))
        assert ok, CHECKS[-1]
    ROWS.append(r)


def ci(d):
    return [d["ci_lo"], d["ci_hi"]]


# ------------------------------------------------------------------------------------------------ matched: default, all-states, B6 (r125 vectors)
def matched_family():
    C = r125_common
    cell = C.Cell()
    doc = C.jload(C.RESULTS / "r125_vectors.json")["readers"]
    V = {k: cell.vector({i: (np.nan if x is None else x) for i, x in r["vector"].items()}) for k, r in doc.items()}
    S = J("reviews/r125/results/r125_matched.json")["paired"]["vs_lookup"]
    names = {"MINI1_v2": "GPT-4.1 mini, one draw", "MINI5_v2": "GPT-4.1 mini, five draws", "H45_v2": "Haiku 4.5", "LUNA_v2": "GPT-5.6 Luna", "SOL_v2": "GPT-5.6 Sol", "OP5_v2": "Opus 5",
             "MINI5_v3": "GPT-4.1 mini, five draws", "H45_v3": "Haiku 4.5", "OP5_v3": "Opus 5", "OP5_v3_d1": "Opus 5, draw 1"}
    for k in ("MINI1_v2", "MINI5_v2", "H45_v2", "LUNA_v2", "SOL_v2", "OP5_v2", "MINI5_v3", "H45_v3", "OP5_v3", "OP5_v3_d1"):
        lk = "LOOKUP_v2" if k.endswith("_v2") else "ALLSTATES_v3"
        cond = "default summary" if lk == "LOOKUP_v2" else "all-states summary"
        for scope, st in (("whole", None), ("supersession", "SUPERSESSION")):
            res = C.paired_matched(cell, V[k], V[lk], "PRESENT", st)
            sv = None
            if k in S:
                s = S[k]["pn_vs_present"]["whole"] if st is None else S[k]["pn_vs_present"]["per_state"][st]
                assert S[k]["lookup"] == lk
                sv = (s["delta"], ci(s["ci_triple"]), ci(s["ci_persona"]))
            row(cond, "tab:cf-matched-vs", names[k], scope, "matched", res, "ci_triple", "ci_persona", stored=sv,
                note="" if sv else "no stored r125 block; the printed tab:cf-matched-vs value is checked by the number gate")
    # B6: the lookup with one count feature minus each of Luna, Sol and Opus (matched, 148 triples; the sign is the hybrid's)
    for k, nm in (("LUNA_v2", "GPT-5.6 Luna"), ("SOL_v2", "GPT-5.6 Sol"), ("OP5_v2", "Opus 5")):
        res = C.paired_matched(cell, V["HYBRID_v2"], V[k], "PRESENT", None)
        row("B6: lookup with one count feature", "tab:cf-hybrid (new row)", f"count-feature lookup minus {nm}", "whole", "matched", res, "ci_triple", "ci_persona")


# ------------------------------------------------------------------------------------------------ pooled: mini one draw on supersession, Opus all-states whole
def pooled_cf2():
    import cf2_reader_score as R
    import score_cf as SC
    from index_v3 import named_sections
    items, idx = R.cell()
    look = R.lookup_v2(items, idx)
    rows = ROOT / "r82_counterfactual" / "cf2" / "rows"
    SM = J("reviews/r117/results/sup_margins.json")
    r = R.score_lane(rows / "rows_MINI.jsonl", "INDEXED-V2", items, look)
    p = r["per_state"]["SUPERSESSION"]["vs_lookup"]
    s = SM["GPT-4.1 mini"]["supersession"]["vs_lookup"]
    row("default summary", "tab:sup-margins", "GPT-4.1 mini, one draw", "supersession", "pooled", p, "item_ci", "persona_ci",
        stored=(s["delta"], ci(s["item_ci"]), ci(s["persona_ci"])))
    s3 = [named_sections(idx[it["item_id"]]["v3"]) for it in items]
    look3 = np.asarray(SC.matcher([it["question"] for it in items], [s["superseded"] + s["retracted"] + s["expired"] for s in s3]), float)
    r = R.score_lane(rows / "rows_OP5.jsonl", "INDEXED-V3", items, look3)
    row("all-states summary", "Table 1 (tab:cf-main)", "Opus 5", "whole", "pooled", r["vs_lookup"], "item_ci", "persona_ci",
        stored=(0.0323, [0.0060, 0.0617], [0.0077, 0.0608]), note="stored = Table 1's printed row (AUX-R103-MARGIN), compared at the printed four decimals")


# ------------------------------------------------------------------------------------------------ the padded set and the unpadded panels (cf_pad)
def padded_family():
    import score_cf_pad as SP
    C = SP.C
    pop = C.Pop(); cell = SP.cell_for(pop); y, g = pop.y, pop.g
    LV = C.jload(C.RES / "lookup_vectors.json")
    assert LV["keys"] == [r["key"] for r in pop.rows]
    rv = C.recorded_vectors()
    S = J("cf_pad/results/cf_pad_scores.json")["minus_lookup"]
    names = {"MINI": "GPT-4.1 mini, five draws", "H45": "Haiku 4.5", "LUNA": "GPT-5.6 Luna", "SOL": "GPT-5.6 Sol", "OP5": "Opus 5"}
    look = {"padded": np.array(LV["padded"]["emb"], float), "unpadded": np.array([rv["LOOKUP_v2"][r["key"]] for r in pop.rows], float)}
    for code in SP.MODELS:
        vec = {"padded": SP.lane_vectors(pop, code)[0], "unpadded": np.array([rv[SP.RECORDED_KEY[code]][r["key"]] for r in pop.rows], float)}
        okm = ~np.isnan(vec["padded"]) & ~np.isnan(vec["unpadded"])
        for arm in ("padded", "unpadded"):
            lp, v = look[arm], vec[arm]
            for scope in ("superseded", "whole"):
                st_ = S[code]["LOOKUP"][scope][arm]
                m = SP.scope_mask(pop, scope) & okm; st = SP.scope_state(scope)
                pp = SP.pooled_paired(lp[m], v[m], y[m], g[m])
                mp = SP.matched_paired(cell, v, lp, "PRESENT", st)
                cond = "padded set" if arm == "padded" else "default summary"
                tab = ("tab:cfpad-minus-lookup" if scope == "superseded" else "tab:cfpad-whole") + (" (padded panel)" if arm == "padded" else " (unpadded panel)")
                sc = "supersession" if scope == "superseded" else "whole"
                row(cond, tab, names[code], sc, "pooled", pp, "ci_item", "ci_persona",
                    stored=(st_["pooled"]["delta"], ci(st_["pooled"]["ci_item"]), ci(st_["pooled"]["ci_persona"])))
                if arm == "padded":   # the unpadded matched rows are tab:cf-matched-vs' (matched_family)
                    row(cond, tab, names[code], sc, "matched", mp, "ci_triple", "ci_persona",
                        stored=(st_["matched"]["delta"], ci(st_["matched"]["ci_triple"]), ci(st_["matched"]["ci_persona"])))


# ------------------------------------------------------------------------------------------------ the sibling-name control (matched)
def sibling_family():
    import r125_t45_score as T
    captured = {}

    def jd(o, p):
        captured[Path(p).name] = o
    T.C.jdump = jd
    r125_common.jdump = jd
    T.score_t4()
    new = captured["r125_t4_sibling.json"]["readers"]
    old = J("reviews/r125/results/r125_t4_sibling.json")["readers"]
    for name in ("GPT-4.1 mini (five draws)", "Haiku 4.5 (five draws)", "GPT-5.6 Luna (five draws)", "GPT-5.6 Sol (draw 1)", "Opus 5 (draw 1)"):
        n, o = new[name]["minus_lookup_matched"], old[name]["minus_lookup_matched"]
        row("sibling-name control", "tab:cf-sibling", name, "supersession (PN vs sibling)", "matched", n, "ci_triple", "ci_persona",
            stored=(o["delta"], ci(o["ci_triple"]), ci(o["ci_persona"])))


# ------------------------------------------------------------------------------------------------ the paraphrase set
def para_family():
    import posthoc_minus_lookup as P
    captured = {}

    def jd(o, p):
        captured["out"] = json.loads(json.dumps(o, default=float))
    P.jdump = jd
    P.main()
    new = captured["out"]["models"]
    old = J("cf2_paraphrase/results/para_minus_lookup_posthoc.json")["models"]
    names = {"MINI": "GPT-4.1 mini", "H45": "Haiku 4.5", "OP5": "Opus 5, draw 1", "LUNA": "GPT-5.6 Luna", "SOL": "GPT-5.6 Sol"}
    for code in ("MINI", "H45", "OP5", "LUNA", "SOL"):
        for summ in ("v2", "v3"):
            if summ not in new[code]:
                continue
            for scope, metrics in (("whole", ("pooled",)), ("superseded", ("pooled", "matched"))):
                for metric in metrics:
                    for qset in ("paraphrase", "original"):
                        n = new[code][summ][scope][metric][qset]; o = old[code][summ][scope][metric][qset]
                        a = "ci_item" if metric == "pooled" else "ci_triple"
                        tab = "tab:para-minus-lookup" if scope == "whole" else "tab:para-sup"
                        rd = f"{names[code]}{'' if summ == 'v2' else ', all states'}, {'paraphrases' if qset == 'paraphrase' else 'originals'}"
                        row("paraphrase set", tab, rd, "whole" if scope == "whole" else "supersession", metric, n, a, "ci_persona",
                            stored=(o["delta"], ci(o[a]), ci(o["ci_persona"])),
                            note="added after the registration, not registered" if code in ("LUNA", "SOL") else ("registered row" if (scope == "whole" and qset == "paraphrase") else "post hoc"))


def main():
    matched_family()
    pooled_cf2()
    padded_family()
    sibling_family()
    para_family()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = dict(rule="equivalent within 0.05: both 90% intervals inside [-0.05, +0.05] (two one-sided tests at 5%); reliable: both 95% intervals exclude zero; neither: 'neither shown nor excluded'",
               draws=1000, seed=42, tol=TOL, n_rows=len(ROWS), checks=dict(n=len(CHECKS), ok=sum(c["ok"] for c in CHECKS)), rows=ROWS, check_rows=CHECKS)
    OUT.write_text(json.dumps(doc, indent=1), encoding="utf-8", newline="\n")
    for r in ROWS:
        print(f"{r['condition']:<34} {r['scope']:<28} {r['metric']:<8} {r['reader']:<44} {r['delta']:+.4f} 90% [{r['ci90_a'][0]:+.4f},{r['ci90_a'][1]:+.4f}] [{r['ci90_persona'][0]:+.4f},{r['ci90_persona'][1]:+.4f}]  {r['reading']}")
    print(f"-> {OUT.relative_to(ROOT).as_posix()}: {len(ROWS)} rows; 95% checks {sum(c['ok'] for c in CHECKS)}/{len(CHECKS)}")


if __name__ == "__main__":
    main()
