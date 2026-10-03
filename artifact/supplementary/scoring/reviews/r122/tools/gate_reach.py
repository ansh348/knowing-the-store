# -*- coding: utf-8 -*-
"""gate_reach.py -- R122 T5: what the gate buys, reach only. OFFLINE, no API call, no answer-stage call, no stale-answer detector.
Registration reviews/r122/registrations/ADDENDUM_R122_GATE_REACH.md (sha asserted at start).

Reuses the downstream pipeline's own functions unchanged: ds_common.load_cell / names_for / fetch / assemble_view / true_flags /
lookup_scores (gate 0.7484 / 0.6186), resp_common.render_line, build_l2.bank_for + LifecycleBank.cosine_search_all (the recorded L2
retriever over the pinned question vectors l2/question_emb.npz; no embedding call), the recorded views.json / policies.json / stage1.json
(the MODEL rule's per-item reach and view sizes) and l2/retrieval.json (the ten-deep ranking and the five-line blocks).

Policies on the 661 (section 3 of the registration):
  AF-k      ALWAYS-FETCH: the lifecycle fetch (ds_common.fetch) with its gate always open, keyed on the ONE attribute of the item's v2
            superseded-names list that the name lookup matches best (max cosine, MiniLM-L6-v2, the NB-6 estimator; ties -> the first
            name in sorted order; an empty list fetches nothing); the similarity fill truncated to the first k of the five recorded lines
            (k = 0..5; k = 5 is the unmatched policy), the fetched records appended by assemble_view with ranks continuing.
  TAGGED-k  similarity retrieval at k lines from the recorded ten-deep ranking, the lifecycle mask off, tags printed (Amendment 6's FLAT-k
            rendering; k = 5..10; TAGGED-7 is the policy named). Lock: TAGGED-5 reproduces the recorded ALWAYS view byte for byte.
  RECENCY-k the same ranking re-derived over the full store variant (lock: its first ten ids equal the recorded top10_ids on all 661),
            keeping only the newest record per attribute (smallest age among the variant's entries sharing the scrubbed slot; entries
            with no slot kept; ties at the smallest age kept), the first k eligible (k = 5..10; RECENCY-7 the policy named).
Budget matching (section 4): the MODEL rule's recorded mean view over the 661 (5.4342) is matched by linear interpolation between the two
integer truncations whose means bracket it (Amendment 6's rule), the weight fixed from the full-population means; the matched rate of
each measure is the same interpolation of the two integer rows, and its intervals resample items (item-level; persona-grouped) once per
draw, computing both integer rows and MODEL's on the resample.

Subcommands:  check   locks and gates only (nothing scored, nothing written)
              run     everything -> results/gate_reach.json, the ledger section
"""
from __future__ import annotations

import io
import json
import sys
import time

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r122_common as C  # noqa: E402
sys.path.insert(0, str(C.ROOT / "ds_downstream" / "tools")); sys.path.insert(0, str(C.ROOT / "resp_review" / "tools"))
import ds_common as DC  # noqa: E402
import build_l2 as BL  # noqa: E402
from build_ds import wilson, boot_prop_diff  # noqa: E402
from resp_common import render_line  # noqa: E402
from run_baselines import encoder  # noqa: E402

REG = "ADDENDUM_R122_GATE_REACH.md"
DS = C.ROOT / "ds_downstream"
TARGET = C.MODEL_MEAN_661
TARGET_104 = 7.076923076923077          # AUX-DS-VIEWSIZE, MODEL mean view size over the 104 obligations (the paper's Section 8 basis; beside)
RECORDED_REACH_BY_DEPTH = {5: 54, 6: 60, 7: 62, 8: 69, 9: 70, 10: 74}   # AUX-R104-REACH, reach of the forbidding record by ranking depth (reused, asserted)
N_BOOT, SEED = 1000, 42
AF_KS = (0, 1, 2, 3, 4, 5)
DEPTHS = (5, 6, 7, 8, 9, 10)


# ------------------------------------------------------------------ recorded artifacts
def load_recorded():
    sub = DC.load_cell()
    views = C.jload(DS / "views.json")["items"]; pol = C.jload(DS / "policies.json")["items"]; st1 = C.jload(DS / "stage1.json")
    art = C.jload(C.ROOT / "resp_review" / "l2" / "retrieval.json")["items"]
    assert len(sub) == 661 and all(it["item_id"] in views and it["item_id"] in art for it in sub)
    return sub, views, pol, st1, art


def model_rows(sub, views, st1):
    """The MODEL rule's per-item reach (104), gold-in-view (174) and view size (661), recomputed from views.json ids and asserted against stage1.json."""
    per = st1["per_item"]; reach, gold, size = {}, {}, {}
    for it in sub:
        ids = set(views[it["item_id"]]["MODEL"]["ids"]); size[it["item_id"]] = len(ids)
        assert len(ids) == views[it["item_id"]]["MODEL"]["n_lines"] == per[it["item_id"]]["MODEL"]["view_size"]
        if it["y_nok"]:
            reach[it["item_id"]] = bool(set(it["pn_members"]) & ids); assert reach[it["item_id"]] == per[it["item_id"]]["MODEL"]["reach"]
        if it["label"] == "PRESENT":
            gold[it["item_id"]] = bool(set(it["gold"]) & ids); assert gold[it["item_id"]] == per[it["item_id"]]["MODEL"]["gold_in_view"]
    assert sum(reach.values()) == C.MODEL_REACH_104 and sum(gold.values()) == C.MODEL_GOLD_IN_VIEW_174
    assert abs(np.mean(list(size.values())) - TARGET) < 1e-9
    return reach, gold, size


# ------------------------------------------------------------------ the best-matched attribute (the name lookup's argmax)
def best_names(sub):
    enc = encoder()
    uq = sorted({it["question"] for it in sub}); qv = dict(zip(uq, enc.encode(uq, normalize_embeddings=True, batch_size=128, show_progress_bar=False)))
    n2 = {it["item_id"]: sorted(DC.names_for(it)[2]) for it in sub}
    un = sorted({n for v in n2.values() for n in v}); nv = dict(zip(un, enc.encode([n.replace("_", " ") for n in un], normalize_embeddings=True, batch_size=256, show_progress_bar=False)))
    best, sims = {}, {}
    for it in sub:
        names = n2[it["item_id"]]
        if not names:
            best[it["item_id"]] = None; sims[it["item_id"]] = None; continue
        s = [float(qv[it["question"]] @ nv[n]) for n in names]; m = max(s)
        best[it["item_id"]] = names[s.index(m)]; sims[it["item_id"]] = m         # names sorted, so index() takes the first at a tie
    return best, sims, n2


# ------------------------------------------------------------------ the policies' views (ids only are needed for the measures; texts kept for the lock)
def af_view(it, art_it, fetched, k):
    lines = art_it["block"].split("\n")[:k]; top = art_it["top5_ids"][:k]
    text, ids = DC.assemble_view(it, "\n".join(lines), top, fetched)
    return text, ids


def tagged_view(it, art_it, k):
    fl = DC.true_flags()[it["persona"]]; ids = art_it["top10_ids"][:k]
    return "\n".join(render_line(r + 1, fl[e]) for r, e in enumerate(ids)), ids


def full_ranking(it, qv):
    vb = BL.bank_for(it)
    return [e.id for e, _ in vb.cosine_search_all(np.asarray(qv, np.float32), k=len(vb.entries))]


def newest_per_slot(it):
    """The entries of the store variant that are the newest of their scrubbed slot (smallest age; ties kept; no slot -> kept)."""
    fl = DC.true_flags()[it["persona"]]; ids = DC.variant_ids(it)
    by = {}
    for e in ids:
        s = fl[e]["slot"]
        if s is None:
            continue
        by.setdefault(s, []).append(e)
    keep = set(e for e in ids if fl[e]["slot"] is None)
    for s, es in by.items():
        known = [e for e in es if fl[e]["age"] is not None]
        if not known:
            keep.update(es); continue
        m = min(fl[e]["age"] for e in known)
        keep.update(e for e in known if fl[e]["age"] == m)
    return keep


def recency_ids(ranking, keep, k):
    return [e for e in ranking if e in keep][:k]


# ------------------------------------------------------------------ measures
def measures(sub, ids_by_item):
    reach = {it["item_id"]: bool(set(it["pn_members"]) & set(ids_by_item[it["item_id"]])) for it in sub if it["y_nok"]}
    gold = {it["item_id"]: bool(set(it["gold"]) & set(ids_by_item[it["item_id"]])) for it in sub if it["label"] == "PRESENT"}
    size = {it["item_id"]: len(ids_by_item[it["item_id"]]) for it in sub}
    return reach, gold, size


def rate_block(sub, reach, gold, size, m_reach, m_gold):
    pn = [it for it in sub if it["y_nok"]]; pres = [it for it in sub if it["label"] == "PRESENT"]
    r = np.array([reach[it["item_id"]] for it in pn], float); mr = np.array([m_reach[it["item_id"]] for it in pn], float); gp = [it["persona"] for it in pn]
    g = np.array([gold[it["item_id"]] for it in pres], float); mg = np.array([m_gold[it["item_id"]] for it in pres], float); gq = [it["persona"] for it in pres]
    k = int(r.sum()); kg = int(g.sum())
    per_state = {s: {"reached": int(sum(reach[it["item_id"]] for it in pn if it["state"] == s)), "n": sum(1 for it in pn if it["state"] == s)} for s, _ in DC.STATES}
    return {"reach": {"reached": k, "n": len(pn), "rate": k / len(pn), "wilson": wilson(k, len(pn)), "per_state": per_state,
                      "minus_model": {"D": float(r.mean() - mr.mean()), "item": boot_prop_diff(r, mr), "persona": boot_prop_diff(r, mr, gp)}},
            "licensed_in_view": {"in_view": kg, "n": len(pres), "rate": kg / len(pres), "wilson": wilson(kg, len(pres)),
                                 "minus_model": {"D": float(g.mean() - mg.mean()), "item": boot_prop_diff(g, mg), "persona": boot_prop_diff(g, mg, gq)}},
            "lines": {"mean_661": float(np.mean([size[it["item_id"]] for it in sub])), "max_661": int(max(size.values())),
                      "mean_104": float(np.mean([size[it["item_id"]] for it in pn])), "ratio_to_model": float(np.mean([size[it["item_id"]] for it in sub]) / TARGET)}}


def _draws(n, g, rng):
    if g is None:
        return rng.integers(0, n, n)
    groups = np.unique(g); idx_by = {u: np.flatnonzero(g == u) for u in groups}
    return np.concatenate([idx_by[groups[j]] for j in rng.integers(0, len(groups), len(groups))])


def boot_matched(a_lo, a_hi, w, m, g=None, n=N_BOOT, seed=SEED):
    """Percentile bootstrap of ((1-w) mean a_lo + w mean a_hi) - mean m on the same resample (the A6 rule with the weight fixed)."""
    rng = np.random.default_rng(seed); a_lo, a_hi, m = (np.asarray(v, float) for v in (a_lo, a_hi, m)); g = None if g is None else np.asarray(g); d = []
    for _ in range(n):
        k = _draws(len(m), g, rng)
        d.append(float((1 - w) * a_lo[k].mean() + w * a_hi[k].mean() - m[k].mean()))
    d = np.asarray(d); lo, hi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    return {"n_draws": n, "mean": float(d.mean()), "ci_lo": lo, "ci_hi": hi, "excludes_zero": bool(lo > 0 or hi < 0)}


def matched(sub, fam, m_reach, m_gold, target=TARGET, pop="661"):
    """fam: {k: (reach, gold, size)} over integer truncations. The matched row at `target` (the mean over the 661, or over the 104 when pop == "104"),
    or a note if the target is outside the family's range."""
    ks = sorted(fam); pn_ids = {it["item_id"] for it in sub if it["y_nok"]}
    means = {k: float(np.mean([v for i, v in fam[k][2].items() if pop == "661" or i in pn_ids])) for k in ks}
    lo = [k for k in ks if means[k] <= target]; hi = [k for k in ks if means[k] > target]
    if not lo or not hi:
        return {"means": means, "target": target, "pop": pop, "note": "target outside the family's range; no matched row"}
    k_lo, k_hi = max(lo, key=lambda k: means[k]), min(hi, key=lambda k: means[k])
    w = (target - means[k_lo]) / (means[k_hi] - means[k_lo])
    pn = [it for it in sub if it["y_nok"]]; pres = [it for it in sub if it["label"] == "PRESENT"]
    R = lambda k, items, which: np.array([fam[k][which][it["item_id"]] for it in items], float)   # noqa: E731
    r_lo, r_hi, mr = R(k_lo, pn, 0), R(k_hi, pn, 0), np.array([m_reach[it["item_id"]] for it in pn], float)
    g_lo, g_hi, mg = R(k_lo, pres, 1), R(k_hi, pres, 1), np.array([m_gold[it["item_id"]] for it in pres], float)
    reach = (1 - w) * r_lo.mean() + w * r_hi.mean(); gold = (1 - w) * g_lo.mean() + w * g_hi.mean()
    return {"means": means, "target": target, "pop": pop, "k_lo": k_lo, "k_hi": k_hi, "weight_hi": w, "achieved_mean": (1 - w) * means[k_lo] + w * means[k_hi],
            "reach": {"rate": float(reach), "lo": float(r_lo.mean()), "hi": float(r_hi.mean()), "minus_model": {"D": float(reach - mr.mean()),
                      "item": boot_matched(r_lo, r_hi, w, mr), "persona": boot_matched(r_lo, r_hi, w, mr, [it["persona"] for it in pn])}},
            "licensed_in_view": {"rate": float(gold), "lo": float(g_lo.mean()), "hi": float(g_hi.mean()), "minus_model": {"D": float(gold - mg.mean()),
                                 "item": boot_matched(g_lo, g_hi, w, mg), "persona": boot_matched(g_lo, g_hi, w, mg, [it["persona"] for it in pres])}}}


# ------------------------------------------------------------------ locks
def locks(sub, views, art):
    """TAGGED-5 reproduces the ALWAYS view byte for byte; the re-derived ranking's first ten equal the recorded top10_ids; the DS lookup gate."""
    qemb = BL.load_question_vectors(); n_view = n_rank = 0
    for it in sub:
        text, ids = tagged_view(it, art[it["item_id"]], 5)
        assert text == views[it["item_id"]]["ALWAYS"]["text"] and ids == views[it["item_id"]]["ALWAYS"]["ids"], it["item_id"]; n_view += 1
        rk = full_ranking(it, qemb[it["question"]])
        assert rk[:10] == art[it["item_id"]]["top10_ids"], it["item_id"]; n_rank += 1
    nb6, nb5, gate = DC.lookup_scores(sub); assert gate["pass"], gate
    print(f"locks: TAGGED-5 == ALWAYS on {n_view}; ranking top-10 reproduced on {n_rank}; lookup gate {gate}")
    return {"tagged5_equals_always": n_view, "ranking_top10_reproduced": n_rank, "lookup_gate": gate}


def run(check_only=False):
    sha = None if check_only else C.assert_frozen(REG)
    sub, views, pol, st1, art = load_recorded()
    lk = locks(sub, views, art)
    m_reach, m_gold, m_size = model_rows(sub, views, st1)
    if check_only:
        print("check OK (nothing scored)"); return
    t0 = time.time()
    best, sims, n2 = best_names(sub)
    qemb = BL.load_question_vectors()
    fetched = {it["item_id"]: (DC.fetch(it, {best[it["item_id"]]}) if best[it["item_id"]] else []) for it in sub}
    for it in sub:
        assert all(DC.flagged(it, e) for e in fetched[it["item_id"]]), "active entry fetched"
    fam = {"AF": {}, "TAGGED": {}, "RECENCY": {}}
    rank = {it["item_id"]: full_ranking(it, qemb[it["question"]]) for it in sub}
    keep = {it["item_id"]: newest_per_slot(it) for it in sub}
    for k in AF_KS:
        ids = {it["item_id"]: af_view(it, art[it["item_id"]], fetched[it["item_id"]], k)[1] for it in sub}; fam["AF"][k] = measures(sub, ids)
    for k in DEPTHS:
        ids = {it["item_id"]: tagged_view(it, art[it["item_id"]], k)[1] for it in sub}; fam["TAGGED"][k] = measures(sub, ids)
        ids = {it["item_id"]: recency_ids(rank[it["item_id"]], keep[it["item_id"]], k) for it in sub}; fam["RECENCY"][k] = measures(sub, ids)
    rows = {f: {k: rate_block(sub, *fam[f][k], m_reach, m_gold) for k in fam[f]} for f in fam}
    match = {f: matched(sub, fam[f], m_reach, m_gold) for f in fam}
    match_104 = {f: matched(sub, fam[f], m_reach, m_gold, TARGET_104, "104") for f in fam}
    for k, n in RECORDED_REACH_BY_DEPTH.items():   # the recorded reach-by-depth row (AUX-R104-REACH) is reused: TAGGED-k must reproduce it
        assert rows["TAGGED"][k]["reach"]["reached"] == n, ("AUX-R104-REACH mismatch", k, rows["TAGGED"][k]["reach"]["reached"], n)
    # the recorded A6 FLAT-7 licensed row (77 of 174) beside TAGGED-7's, asserted equal
    a6 = C.jload(DS / "run" / "scores_amend6.json") if (DS / "run" / "scores_amend6.json").exists() else None
    model_rate = C.MODEL_REACH_104 / 104
    if a6:   # the recorded Amendment 6 flat curve on the 174 (lock.counts.inview) is reused: TAGGED-k's licensed-in-view counts must equal it
        rec = a6["lock"]["counts"]["inview"]
        for k in DEPTHS:
            assert rows["TAGGED"][k]["licensed_in_view"]["in_view"] == rec[str(k)], ("A6 FLAT row mismatch", k, rows["TAGGED"][k]["licensed_in_view"]["in_view"], rec[str(k)])
    # censuses
    n_best = sum(1 for v in best.values() if v); n_fetch = sum(1 for v in fetched.values() if v)
    pn = [it for it in sub if it["y_nok"]]
    best_is_pn_slot = sum(1 for it in pn if best[it["item_id"]] and best[it["item_id"]] in DC.pn_slots(it))
    keep_census = {"mean_kept_per_variant": float(np.mean([len(keep[it["item_id"]]) for it in sub])), "mean_variant_size": float(np.mean([len(DC.variant_ids(it)) for it in sub])),
                   "pn_member_kept_items": sum(1 for it in pn if set(it["pn_members"]) & keep[it["item_id"]])}
    # predictions
    af_m, rc_m = match["AF"], match["RECENCY"]
    g1 = abs(af_m["reach"]["rate"] - model_rate) <= C.TOL if "reach" in af_m else None
    g2 = rows["AF"][5]["lines"]["mean_661"] > TARGET
    g3 = (model_rate - rc_m["reach"]["rate"]) > C.TOL if "reach" in rc_m else None
    res = {"meta": {"registration": REG, "registration_sha256": sha, "locks": lk, "target_mean_661": TARGET, "target_mean_104": TARGET_104, "recorded_reach_by_depth": RECORDED_REACH_BY_DEPTH,
                    "model_reach": C.MODEL_REACH_104, "model_gold_in_view": C.MODEL_GOLD_IN_VIEW_174,
                    "n_boot": N_BOOT, "seed": SEED, "seconds": round(time.time() - t0, 1), "when": time.strftime("%Y-%m-%dT%H:%M:%S")},
           "census": {"items_with_a_best_name": n_best, "items_fetching_at_least_one_record": n_fetch, "mean_fetched_661": float(np.mean([len(v) for v in fetched.values()])),
                      "obligations_whose_best_name_is_a_forbidding_slot": best_is_pn_slot, "n_obligations": len(pn), "recency": keep_census,
                      "a6_recorded_inview": (a6 or {}).get("lock", {}).get("counts", {}).get("inview")},
           "rows": rows, "matched": match, "matched_104": match_104, "best_name": best, "fetched": fetched,
           "predictions": {"P-G1": {"verdict": "HOLDS" if g1 else "FAILS", "af_matched_reach": af_m.get("reach", {}).get("rate"), "model": model_rate,
                                    "D": (af_m["reach"]["minus_model"]["D"] if "reach" in af_m else None), "item": af_m.get("reach", {}).get("minus_model", {}).get("item"),
                                    "persona": af_m.get("reach", {}).get("minus_model", {}).get("persona"), "unmatched_af5_reach": rows["AF"][5]["reach"]["rate"]},
                           "P-G2": {"verdict": "HOLDS" if g2 else "FAILS", "af5_mean_661": rows["AF"][5]["lines"]["mean_661"], "model_mean_661": TARGET, "ratio": rows["AF"][5]["lines"]["ratio_to_model"]},
                           "P-G3": {"verdict": "HOLDS" if g3 else "FAILS", "recency_matched_reach": rc_m.get("reach", {}).get("rate"), "model": model_rate,
                                    "D": (rc_m["reach"]["minus_model"]["D"] if "reach" in rc_m else None), "item": rc_m.get("reach", {}).get("minus_model", {}).get("item"),
                                    "persona": rc_m.get("reach", {}).get("minus_model", {}).get("persona"), "unmatched_recency7_reach": rows["RECENCY"][7]["reach"]["rate"]}}}
    C.jdump(res, C.RESULTS / "gate_reach.json")
    write_ledger(res)
    for k, v in res["predictions"].items():
        print(k, v["verdict"], {kk: vv for kk, vv in v.items() if kk not in ("item", "persona")})


def fmt(d):
    return f"{d['D']:+.4f} ({C.ci(d['item'])}; {C.ci(d['persona'])})"


def write_ledger(res):
    R = res["rows"]
    L = ["", "## T5. What the gate buys, reach only (ADDENDUM_R122_GATE_REACH.md)", "", "### AUX-R122-GATE-LOCK", "",
         f"Registered text sha256 `{res['meta']['registration_sha256']}`; locks {res['meta']['locks']}; the MODEL rule's recorded rows reproduced (reach {res['meta']['model_reach']} of 104, "
         f"licensed in view {res['meta']['model_gold_in_view']} of 174, mean view {res['meta']['target_mean_661']:.4f} over the 661). Census: {res['census']}.", "",
         "### AUX-R122-GATE-ROWS — every truncation (reach on the 104 with Wilson; the paired difference against the MODEL rule, item-level and persona-grouped; licensed record in view on the 174; lines per question over the 661)", "",
         "| policy | reach | Wilson | minus MODEL (item; persona) | sup / ret / exp | licensed in view | minus MODEL | mean lines 661 (max) | mean 104 | ratio to MODEL |", "|---|---|---|---|---|---|---|---|---|---|"]
    for f, name in (("AF", "ALWAYS-FETCH, fill k"), ("TAGGED", "TAGGED-k"), ("RECENCY", "RECENCY-k")):
        for k, B in R[f].items():
            ps = " / ".join(f"{B['reach']['per_state'][s]['reached']}/{B['reach']['per_state'][s]['n']}" for s, _ in DC.STATES)
            L.append(f"| {name}={k} | {B['reach']['reached']}/104 = {B['reach']['rate']:.4f} | [{B['reach']['wilson'][0]:.3f}, {B['reach']['wilson'][1]:.3f}] | {fmt(B['reach']['minus_model'])} | {ps} | "
                     f"{B['licensed_in_view']['in_view']}/174 = {B['licensed_in_view']['rate']:.4f} | {fmt(B['licensed_in_view']['minus_model'])} | {B['lines']['mean_661']:.4f} ({B['lines']['max_661']}) | {B['lines']['mean_104']:.4f} | {B['lines']['ratio_to_model']:.4f} |")
    for key, title in (("matched", f"the budget-matched rows at the MODEL rule's mean view over the 661, {res['meta']['target_mean_661']:.4f} (the registered primary)"),
                       ("matched_104", f"the same at the MODEL rule's mean view over the 104 obligations, {res['meta']['target_mean_104']:.4f} (Section 8's basis; beside)")):
        M = res[key]
        L += ["", f"### AUX-R122-GATE-{'MATCHED' if key == 'matched' else 'MATCHED-104'} — {title}; linear interpolation between the bracketing truncations (Amendment 6's rule), the weight fixed from the population means", "",
              "| policy | bracketing k (means) | weight on k_hi | achieved mean | reach (matched) | minus MODEL (item; persona) | licensed in view (matched) | minus MODEL (item; persona) |", "|---|---|---:|---:|---:|---|---:|---|"]
        for f in ("AF", "TAGGED", "RECENCY"):
            m = M[f]
            if "reach" not in m:
                L.append(f"| {f} | { {k: round(v, 4) for k, v in m['means'].items()} } | — | — | {m['note']} | | | |"); continue
            L.append(f"| {f} | {m['k_lo']} ({m['means'][m['k_lo']]:.4f}), {m['k_hi']} ({m['means'][m['k_hi']]:.4f}) | {m['weight_hi']:.4f} | {m['achieved_mean']:.4f} | {m['reach']['rate']:.4f} | {fmt(m['reach']['minus_model'])} | "
                     f"{m['licensed_in_view']['rate']:.4f} | {fmt(m['licensed_in_view']['minus_model'])} |")
    P = res["predictions"]
    L += ["", "### AUX-R122-GATE-PREDICTIONS", "",
          f"- **P-G1 {P['P-G1']['verdict']}**: ALWAYS-FETCH budget-matched reach {P['P-G1']['af_matched_reach']:.4f} against the MODEL rule's {P['P-G1']['model']:.4f}, D {P['P-G1']['D']:+.4f} "
          f"({C.ci(P['P-G1']['item'])}; {C.ci(P['P-G1']['persona'])}); unmatched (five lines plus the fetch) {P['P-G1']['unmatched_af5_reach']:.4f}.",
          f"- **P-G2 {P['P-G2']['verdict']}**: ALWAYS-FETCH before matching spends {P['P-G2']['af5_mean_661']:.4f} lines per question over the 661 against the MODEL rule's {P['P-G2']['model_mean_661']:.4f}; ratio {P['P-G2']['ratio']:.4f}.",
          f"- **P-G3 {P['P-G3']['verdict']}**: RECENCY budget-matched reach {P['P-G3']['recency_matched_reach']:.4f} against the MODEL rule's {P['P-G3']['model']:.4f}, D {P['P-G3']['D']:+.4f} "
          f"({C.ci(P['P-G3']['item'])}; {C.ci(P['P-G3']['persona'])}); unmatched RECENCY-7 {P['P-G3']['unmatched_recency7_reach']:.4f}."]
    C.append_ledger("\n".join(L) + "\n")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        run(check_only=True)
    elif cmd == "run":
        run()
    else:
        raise SystemExit("usage: gate_reach.py check|run")
