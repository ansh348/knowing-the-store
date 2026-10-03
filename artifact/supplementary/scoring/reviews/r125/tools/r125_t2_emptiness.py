# -*- coding: utf-8 -*-
"""r125_t2_emptiness.py -- Task 2: how much of the name lookup is list emptiness (offline, post hoc). NO MODEL CALL. $0.

1. Of the 88 supersession pairs of the counterfactual set, how many carry an empty superseded-names list in the PRESENT version and in the
   ABSENT version; the distribution of list length per version (PN, PRESENT, ABSENT); the same census on the counted-state pairs and, under
   the all-states summary, on the retracted and expired lists.
2. The random-token control (every name replaced by its stable token, enc_lookup.random_token, seed 42; MiniLM) per state and under the
   matched metric on the 444 (v2 and v3; the vectors of r125_vectors.json), and per state on the 661 (positives of one state against the
   557 negatives, the committed form with the '(none)' marker as a name and the marker-free form). The 661 has no triples, so the matched
   metric is not defined there; the pooled rows are given.
3. The name lookup minus the random-token control, paired, both intervals, under both metrics, on both populations: pooled (cf2_score.paired:
   the item-level and the persona-grouped bootstrap, 1,000 draws, seed 42) whole and per state; matched (r125_common.paired_matched: the
   triple-level and the persona-grouped bootstrap) whole and per state on the 444.
Gates: the recorded MiniLM rows 0.7663 (444 v2), 0.8756 (444 v3), 0.7484 (661), 0.7442 (661 marker-free), the random-token rows 0.5954 / 0.5479
(444) and 0.6654 (661 committed form) of AUX-R122-ENC-RANDOM.
Writes reviews/r125/results/r125_t2_emptiness.json.
"""
from __future__ import annotations

import collections
import sys

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r125_common as C  # noqa: E402
from r125_common import STATES, auroc, r4  # noqa: E402
from index_v3 import named_sections  # noqa: E402
from cf2_score import paired  # noqa: E402

OUT = C.RESULTS / "r125_t2_emptiness.json"
VEC = C.RESULTS / "r125_vectors.json"
MARKER = "(none)"
STATE661 = {"sup": "SUPERSESSION", "ret": "RETRACTION", "exp": "EXPIRY"}


def hist(xs):
    c = collections.Counter(int(x) for x in xs)
    return {str(k): c[k] for k in sorted(c)}


def census_444(cell):
    res = {}
    v2 = {i: named_sections(cell.idx[i]["v2"])["superseded"] for i in cell.ids}
    v3 = {i: named_sections(cell.idx[i]["v3"]) for i in cell.ids}
    for state in (None,) + STATES:
        pids = cell.pids(state)
        block = {"n_pairs": len(pids)}
        for ver in C.VERSIONS:
            L = [len(v2[cell.ids[cell.pos_of[(p, ver)]]]) for p in pids]
            block[f"v2_superseded_list/{ver}"] = {"empty": int(sum(1 for x in L if x == 0)), "length_hist": hist(L), "mean_length": r4(np.mean(L))}
        d = [len(v2[cell.ids[cell.pos_of[(p, "PN")]]]) - len(v2[cell.ids[cell.pos_of[(p, "PRESENT")]]]) for p in pids]
        block["v2_superseded_list/PN_minus_PRESENT_length"] = hist(d)
        d = [len(v2[cell.ids[cell.pos_of[(p, "PN")]]]) - len(v2[cell.ids[cell.pos_of[(p, "ABSENT")]]]) for p in pids]
        block["v2_superseded_list/PN_minus_ABSENT_length"] = hist(d)
        block["v2_pairs_where_PRESENT_empty_and_PN_nonempty"] = int(sum(1 for p in pids if len(v2[cell.ids[cell.pos_of[(p, "PRESENT")]]]) == 0 and len(v2[cell.ids[cell.pos_of[(p, "PN")]]]) > 0))
        for sec in ("superseded", "retracted", "expired"):
            for ver in C.VERSIONS:
                L = [len(v3[cell.ids[cell.pos_of[(p, ver)]]][sec]) for p in pids]
                block[f"v3_{sec}_list/{ver}"] = {"empty": int(sum(1 for x in L if x == 0)), "length_hist": hist(L), "mean_length": r4(np.mean(L))}
        res[state or "ALL"] = block
    return res


def per_state_pooled_661(v, y, st):
    """The 661 convention: positives of one state against all negatives."""
    out = {"whole": r4(auroc(v, y))}
    neg = y == 0
    for s in ("sup", "ret", "exp"):
        keep = neg | ((y == 1) & (st == s))
        out[STATE661[s]] = {"n": int(keep.sum()), "pos": int(((y == 1) & (st == s)).sum()), "auroc": r4(auroc(v[keep], y[keep]))}
    return out


def paired_661(base, v, y, g, st):
    """lookup (v) minus random-token (base), pooled, whole and per state (the state's positives against all negatives)."""
    out = {"whole": paired(base, v, y, g)}
    neg = y == 0
    for s in ("sup", "ret", "exp"):
        keep = neg | ((y == 1) & (st == s))
        out[STATE661[s]] = paired(base[keep], v[keep], y[keep], g[keep])
    return out


def main():
    cell = C.Cell()
    vec = C.jload(VEC)["readers"]
    V = {k: cell.vector({i: (np.nan if x is None else x) for i, x in vec[k]["vector"].items()}) for k in ("LOOKUP_v2", "RANDTOK_v2", "ALLSTATES_v3", "RANDTOK_v3")}
    for k, gate in (("LOOKUP_v2", 0.7663), ("RANDTOK_v2", 0.5954), ("ALLSTATES_v3", 0.8756), ("RANDTOK_v3", 0.5479)):
        assert r4(auroc(V[k], cell.y)) == gate, (k, r4(auroc(V[k], cell.y)), gate)
    res = {"meta": {"script": "reviews/r125/tools/r125_t2_emptiness.py", "model_calls": 0, "status": "post hoc, offline", "n_boot": C.N_BOOT, "seed": C.SEED,
                    "random_token": "enc_lookup.random_token (sha256 of the name with seed 42; eight lowercase letters; one token per distinct name), MiniLM-L6-v2",
                    "matched_on_661": "not defined: the 661 has no triples; pooled rows only"}}
    # ---- 1. the census
    res["census_444"] = census_444(cell)
    c = res["census_444"]["SUPERSESSION"]
    print("1. the 88 supersession pairs, v2 superseded-names list: empty in PRESENT", c["v2_superseded_list/PRESENT"]["empty"], "empty in ABSENT", c["v2_superseded_list/ABSENT"]["empty"],
          "empty in PN", c["v2_superseded_list/PN"]["empty"])
    for ver in C.VERSIONS:
        print(f"   {ver:8s} length hist {c[f'v2_superseded_list/{ver}']['length_hist']} mean {c[f'v2_superseded_list/{ver}']['mean_length']}")
    print("   PN minus PRESENT length", c["v2_superseded_list/PN_minus_PRESENT_length"], "; PN minus ABSENT", c["v2_superseded_list/PN_minus_ABSENT_length"],
          "; pairs where PRESENT is empty and PN is not", c["v2_pairs_where_PRESENT_empty_and_PN_nonempty"])
    # ---- 2. the random-token control on the 444 (pooled per state; matched per state) -- the vectors of Task 1
    m444 = {}
    for tag, lk, rk in (("v2", "LOOKUP_v2", "RANDTOK_v2"), ("v3", "ALLSTATES_v3", "RANDTOK_v3")):
        blk = {"random_token": {"pooled": C.per_state_pooled(cell, V[rk]), "matched_pn_vs_present": {"whole": C.matched_block(cell, V[rk], "PRESENT"), "per_state": {s: C.matched_block(cell, V[rk], "PRESENT", s) for s in STATES}},
                                "matched_pn_vs_absent": {"whole": C.matched_block(cell, V[rk], "ABSENT"), "per_state": {s: C.matched_block(cell, V[rk], "ABSENT", s) for s in STATES}}},
               "lookup": {"pooled": C.per_state_pooled(cell, V[lk]), "matched_pn_vs_present": {"whole": C.matched_block(cell, V[lk], "PRESENT"), "per_state": {s: C.matched_block(cell, V[lk], "PRESENT", s) for s in STATES}}},
               # 3. lookup minus random token, pooled (item + persona) and matched (triple + persona), whole and per state
               "lookup_minus_random_pooled": {"whole": paired(V[rk], V[lk], cell.y, cell.g), "per_state": {s: paired(V[rk][cell.st == s], V[lk][cell.st == s], cell.y[cell.st == s], cell.g[cell.st == s]) for s in STATES}},
               "lookup_minus_random_matched": {"pn_vs_present": {"whole": C.paired_matched(cell, V[lk], V[rk], "PRESENT"), "per_state": {s: C.paired_matched(cell, V[lk], V[rk], "PRESENT", s) for s in STATES}},
                                               "pn_vs_absent": {"whole": C.paired_matched(cell, V[lk], V[rk], "ABSENT"), "per_state": {s: C.paired_matched(cell, V[lk], V[rk], "ABSENT", s) for s in STATES}}}}
        m444[tag] = blk
        rt, lo = blk["random_token"], blk["lookup"]
        print(f"2. 444 {tag}: random token pooled {rt['pooled']['whole']:.4f} per state {[rt['pooled']['per_state'][s] for s in STATES]}; matched PNvPR {rt['matched_pn_vs_present']['whole']['matched']:.4f} "
              f"per state {[rt['matched_pn_vs_present']['per_state'][s]['matched'] for s in STATES]}; lookup pooled {lo['pooled']['whole']:.4f} matched {lo['matched_pn_vs_present']['whole']['matched']:.4f}")
        pw, mw = blk["lookup_minus_random_pooled"]["whole"], blk["lookup_minus_random_matched"]["pn_vs_present"]["whole"]
        print(f"3. 444 {tag}: lookup minus random token, pooled {pw['delta']:+.4f} {C.ci(pw['item_ci'])} {C.ci(pw['persona_ci'])}{' reliable' if pw['both_exclude_zero'] else ''}; "
              f"matched {mw['delta']:+.4f} {C.ci(mw['ci_triple'])} {C.ci(mw['ci_persona'])}{' reliable' if mw['both_exclude_zero'] else ''}")
        for s in STATES:
            ps, ms = blk["lookup_minus_random_pooled"]["per_state"][s], blk["lookup_minus_random_matched"]["pn_vs_present"]["per_state"][s]
            print(f"      {s:12s} pooled {ps['delta']:+.4f} {C.ci(ps['item_ci'])} {C.ci(ps['persona_ci'])}; matched {ms['delta']:+.4f} {C.ci(ms['ci_triple'])} {C.ci(ms['ci_persona'])}")
    res["cf444"] = m444
    # ---- 2/3 on the 661
    import enc_lookup as E
    sys.path.insert(0, str(C.ROOT / "resp_review" / "tools"))
    import resp_common as RC
    E.set_encoder(E.MINILM)
    R = E.pop_661()
    state_of = {it["item_id"]: it["state"] for it in RC.load_cell()}
    st = np.array([state_of[r["item_id"]] for r in R]); y = np.array([r["y"] for r in R], int); g = np.array([r["persona"] for r in R])
    assert collections.Counter(st[y == 1]) == {"sup": 63, "ret": 26, "exp": 15}
    for r in R:
        r["sup_clean"] = [n for n in r["sup"] if n.strip() != MARKER]
    names = sorted({n for r in R for n in r["sup"]})
    tok = {n: E.random_token(n) for n in names}
    for r in R:
        r["sup_tok"] = [tok[n] for n in r["sup"]]; r["sup_clean_tok"] = [tok[n] for n in r["sup_clean"]]
    b661 = {}
    for form, fld in (("committed", "sup"), ("marker_free", "sup_clean")):
        lk = E.score_661(R, fld); rk = E.score_661(R, fld + "_tok")
        b661[form] = {"lookup": per_state_pooled_661(lk, y, st), "random_token": per_state_pooled_661(rk, y, st), "lookup_minus_random_pooled": paired_661(rk, lk, y, g, st),
                      "census": {"items_with_empty_list": int(sum(1 for r in R if not r[fld])), "positives_with_empty_list": int(sum(1 for r in R if r["y"] == 1 and not r[fld])),
                                 "mean_length": r4(np.mean([len(r[fld]) for r in R])), "length_hist": hist(len(r[fld]) for r in R)}}
        print(f"2. 661 {form}: lookup {b661[form]['lookup']['whole']:.4f} per state {[b661[form]['lookup'][STATE661[s]]['auroc'] for s in ('sup','ret','exp')]}; random token {b661[form]['random_token']['whole']:.4f} "
              f"per state {[b661[form]['random_token'][STATE661[s]]['auroc'] for s in ('sup','ret','exp')]}; empty lists {b661[form]['census']['items_with_empty_list']} of 661 ({b661[form]['census']['positives_with_empty_list']} positives)")
        pw = b661[form]["lookup_minus_random_pooled"]["whole"]
        print(f"3. 661 {form}: lookup minus random token pooled {pw['delta']:+.4f} {C.ci(pw['item_ci'])} {C.ci(pw['persona_ci'])}{' reliable' if pw['both_exclude_zero'] else ''}; per state " +
              "; ".join(f"{s} {b661[form]['lookup_minus_random_pooled'][STATE661[s]]['delta']:+.4f}{'*' if b661[form]['lookup_minus_random_pooled'][STATE661[s]]['both_exclude_zero'] else ''}" for s in ("sup", "ret", "exp")))
    gates = {"661_committed": b661["committed"]["lookup"]["whole"], "661_marker_free": b661["marker_free"]["lookup"]["whole"], "661_random_committed": b661["committed"]["random_token"]["whole"]}
    assert gates == {"661_committed": 0.7484, "661_marker_free": 0.7442, "661_random_committed": 0.6654}, gates
    res["obl661"] = b661; res["gates"] = {"444_v2": 0.7663, "444_v3": 0.8756, "444_random_v2": 0.5954, "444_random_v3": 0.5479, **gates}
    C.jdump(res, OUT)
    print(f"-> {OUT.relative_to(C.ROOT)}")


if __name__ == "__main__":
    main()
