# -*- coding: utf-8 -*-
"""z2_z3_full_population.py -- SPEC_R113 sections Z2 and Z3.
NO MODEL CALL. $0.
Z2  the FULL-store population of the Graphiti comparison recounted from resp_common.load_cell() and asserted against the
    figures Amendment 2 section 0 / section 3 state (323 = 145 / 131 / 47; 178; 99 equal / 230 contradicting / 9 without a
    sibling; 58 / 42 over the 100 ablated non-ABSENT); the FULL-variant census record read, not recomputed.
Z3  the FR-Bank comparators on the 323 FULL items (positives 47) from the recorded per-item rows: GPT-4.1 mini INDEXED-TRUE,
    BLIND, RETRIEVED, HYBRID, RETRIEVED-BELIEVED; Haiku 4.5 INDEXED-TRUE, RETRIEVED, HYBRID; the two lookups; the recorded
    pairings on the 323 with both intervals; reach of the forbidding record among the 47. The 661 figure beside each,
    asserted equal to the ledgered value (reproduction gates). No Graphiti number is computed or read.
Writes reviews/r113/results/z2_full_population.json and z3_frbank_comparators_full.json; appends AUX-R113-Z2-*, AUX-R113-Z3-*.
"""
from __future__ import annotations

import collections
import datetime as dt
import io
import json

import numpy as np

from r113_common import ROOT, RESULTS, J, jdump, assert_spec, ledger_append, r4

import resp_common as RC          # noqa: E402
import run_resp as RR             # noqa: E402
import amend1_resp as A1          # noqa: E402
from run_nb6 import build as nb6_build, emb_scores, lex_scores   # noqa: E402
from common_e1r import load_e1, auroc                            # noqa: E402

GATES_661 = {"mini_true": 0.7339, "mini_blind": 0.4946, "mini_retrieved": 0.6851, "mini_hybrid": 0.8303, "mini_believed": 0.8144,
             "lookup_emb": 0.7484, "lookup_lex": 0.5738, "reach_k5": 54, "reach_k10": 74}
EXPECT = {"full": 323, "full_absent": 145, "full_present": 131, "full_pn": 47, "full_non_absent": 178, "sibling_equal": 99,
          "sibling_contradicts": 230, "no_sibling": 9, "ablated_non_absent": 100, "ablated_dup": 58, "ablated_contra": 42,
          "pn_with_replacement": 38, "pn_without_replacement": 9, "pn_personas": 28,
          "av": {"AV1": 16, "AV4": 11, "AV7": 11, "AV2": 9}, "licensed_intent": {"CURRENT-STATE": 65, "UPCOMING": 26, "CHANGE-AWARE": 35, "PAST-EVENT": 5}}
STATES = RR.STATES


def z2(sub):
    by_pq = collections.defaultdict(dict)
    for it in sub:
        by_pq[(it["persona"], it["question_id"])][it["variant"]] = it
    full = [it for it in sub if it["variant"] == "FULL"]
    lab = collections.Counter(it["label"] for it in full)
    pn = [it for it in full if it["label"] == "PRESENT-NEGATIVE"]; lic = [it for it in full if it["label"] == "PRESENT"]
    av = collections.Counter(it["attack_vector"].split("_")[0] for it in pn)
    out = {"variant_x_label": {f"{v}|{l}": n for (v, l), n in sorted(collections.Counter((it["variant"], it["label"]) for it in sub).items())},
           "full": len(full), "full_absent": lab["ABSENT"], "full_present": lab["PRESENT"], "full_pn": lab["PRESENT-NEGATIVE"], "full_non_absent": len(pn) + len(lic),
           "pn_subtype": dict(collections.Counter(it["subtype"] for it in pn)), "pn_intent": dict(collections.Counter(it["intent"] for it in pn)),
           "pn_state": dict(collections.Counter(it["state"] for it in pn)), "pn_attack_vector": dict(av), "pn_personas": len({it["persona"] for it in pn}),
           "licensed_intent": dict(collections.Counter(it["intent"] for it in lic)), "licensed_personas": len({it["persona"] for it in lic})}
    eq = contra = none = 0; contra_detail = collections.Counter(); contra_ids = []
    dup = con = 0
    for it in sub:
        if it["variant"] == "FULL":
            continue
        sib = by_pq[(it["persona"], it["question_id"])].get("FULL")
        if sib is None:
            none += 1; continue
        if sib["label"] == it["label"]:
            eq += 1
        else:
            contra += 1; contra_detail[f"{it['label']} (FULL sibling {sib['label']})"] += 1; contra_ids.append(it["item_id"])
        if it["label"] != "ABSENT":
            if sib["label"] == it["label"] and sib.get("subtype") == it.get("subtype"):
                dup += 1
            else:
                con += 1
    out.update({"sibling_equal": eq, "sibling_contradicts": contra, "sibling_contradicts_detail": dict(contra_detail), "no_sibling": none,
                "ablated_non_absent": sum(1 for it in sub if it["variant"] != "FULL" and it["label"] != "ABSENT"), "ablated_dup": dup, "ablated_contra": con,
                "aisha_q03_cat_ablated_in_contradictions": "frbank:aisha:aisha_q03:CAT-ABLATED" in contra_ids})
    cf = J(ROOT / "r85_graphiti" / "g10" / "census_full_variant_g10.json")
    fv = cf["full_variant_47"]
    out["census_full_variant_record"] = {k: fv[k] for k in fv if not isinstance(fv[k], (list, dict))} if isinstance(fv, dict) else fv
    out["census_full_variant_record_raw_keys"] = list(fv.keys()) if isinstance(fv, dict) else None
    checks = {}
    for k, v in EXPECT.items():
        if k == "av":
            checks[k] = {a: (out["pn_attack_vector"].get(a), v[a], out["pn_attack_vector"].get(a) == v[a]) for a in v}
        elif k == "licensed_intent":
            checks[k] = {a: (out["licensed_intent"].get(a), v[a], out["licensed_intent"].get(a) == v[a]) for a in v}
        elif k == "pn_with_replacement":
            checks[k] = (out["pn_subtype"].get("with-replacement"), v, out["pn_subtype"].get("with-replacement") == v)
        elif k == "pn_without_replacement":
            checks[k] = (out["pn_subtype"].get("without-replacement"), v, out["pn_subtype"].get("without-replacement") == v)
        else:
            checks[k] = (out[k], v, out[k] == v)
    out["checks_against_amendment_2_sections_0_and_3"] = checks
    flat = [c[2] for c in checks.values() if isinstance(c, tuple)] + [t[2] for c in checks.values() if isinstance(c, dict) for t in c.values()]
    out["all_checks_pass"] = all(flat)
    return out


def z3(sub):
    by = RR.load_rows(); bel = {json.loads(l)["item_id"]: json.loads(l) for l in io.open(ROOT / "resp_review/run/rows_amend1_mini.jsonl", encoding="utf-8")}
    T45 = A1.h45_true(); R45 = A1.collapse(A1.rows_h45("RETRIEVED")); H45 = A1.collapse(A1.rows_h45("HYBRID"))
    e1_items, blind, idxT, _ = load_e1(); by_id = {it["item_id"]: it for it in sub}
    rows = nb6_build([it for it in e1_items if it["item_id"] in by_id], blind, idxT, "nok", "TRUE"); assert len(rows) == 661
    emb = dict(zip([r["item_id"] for r in rows], map(float, emb_scores(rows, "sup")))); lex = dict(zip([r["item_id"] for r in rows], map(float, lex_scores(rows, "sup"))))
    readers = {"mini_true": lambda it: it["true"]["nok"], "mini_blind": lambda it: it["blind"]["nok"],
               "mini_retrieved": lambda it: by["RETRIEVED"][it["item_id"]]["nok"], "mini_hybrid": lambda it: by["HYBRID"][it["item_id"]]["nok"],
               "mini_believed": lambda it: bel[it["item_id"]]["nok"], "lookup_emb": lambda it: emb[it["item_id"]], "lookup_lex": lambda it: lex[it["item_id"]],
               "h45_true": lambda it: T45[it["item_id"]]["nok"], "h45_retrieved": lambda it: R45[it["item_id"]]["nok"], "h45_hybrid": lambda it: H45[it["item_id"]]["nok"]}
    avail = {"mini_true": lambda it: True, "mini_blind": lambda it: True, "mini_retrieved": lambda it: by["RETRIEVED"].get(it["item_id"], {}).get("status") == "OK",
             "mini_hybrid": lambda it: by["HYBRID"].get(it["item_id"], {}).get("status") == "OK", "mini_believed": lambda it: bel.get(it["item_id"], {}).get("status") == "OK",
             "lookup_emb": lambda it: True, "lookup_lex": lambda it: True, "h45_true": lambda it: it["item_id"] in T45, "h45_retrieved": lambda it: it["item_id"] in R45,
             "h45_hybrid": lambda it: it["item_id"] in H45}
    full = [it for it in sub if it["variant"] == "FULL"]
    out = {"gates_661": {}, "single_arm": {}, "paired": {}, "reach_47": {}}
    for name, f in readers.items():
        pop = [it for it in sub if avail[name](it)]
        a661 = r4(auroc([f(it) for it in pop], [it["y_nok"] for it in pop]))
        out["gates_661"][name] = {"auroc": a661, "n": len(pop), "n_pos": sum(it["y_nok"] for it in pop)}
        if name in GATES_661:
            assert a661 == GATES_661[name], f"GATE {name}: {a661} != {GATES_661[name]}"
        out["single_arm"][name] = {}
        for st, sname in [(None, "all")] + [(s, n) for s, n in STATES]:
            pop = [it for it in RR.subpop(full, st) if avail[name](it)]
            s = [f(it) for it in pop]; y = [it["y_nok"] for it in pop]; g = [it["persona"] for it in pop]
            ci = RR.auroc_ci(s, y)
            from common_e1r import boot_cluster_single
            cl = boot_cluster_single(np.asarray(s, float), np.asarray(y, int), np.asarray(g))
            out["single_arm"][name][sname] = {"auroc": r4(ci["point"]), "n": len(pop), "n_pos": int(sum(y)), "item_ci": [r4(ci["ci_lo"]), r4(ci["ci_hi"])],
                                              "persona_ci": [r4(cl.get("ci_lo")), r4(cl.get("ci_hi"))] if isinstance(cl, dict) else None}
    pairs = {"mini_retrieved_minus_true": ("mini_true", "mini_retrieved"), "mini_hybrid_minus_true": ("mini_true", "mini_hybrid"),
             "mini_believed_minus_retrieved": ("mini_retrieved", "mini_believed"), "mini_believed_minus_true": ("mini_true", "mini_believed"),
             "h45_retrieved_minus_true": ("h45_true", "h45_retrieved"), "h45_hybrid_minus_true": ("h45_true", "h45_hybrid"),
             "lookup_emb_minus_mini_true": ("mini_true", "lookup_emb")}
    for pname, (b, a) in pairs.items():
        out["paired"][pname] = {}
        for pop_name, base_pop in (("full_323", full), ("all_661", sub)):
            out["paired"][pname][pop_name] = {}
            for st, sname in [(None, "all")] + [(s, n) for s, n in STATES]:
                pop = [it for it in RR.subpop(base_pop, st) if avail[b](it) and avail[a](it)]
                d = RR.paired([readers[b](it) for it in pop], [readers[a](it) for it in pop], [it["y_nok"] for it in pop], [it["persona"] for it in pop])
                out["paired"][pname][pop_name][sname] = {"base": r4(d["base"]), "arm": r4(d["arm"]), "D": r4(d["D"]), "n": d["n"], "n_pos": d["n_pos"],
                                                          "item_ci": [r4(d["item"].get("ci_lo")), r4(d["item"].get("ci_hi"))], "persona_ci": [r4(d["cluster"].get("ci_lo")), r4(d["cluster"].get("ci_hi"))],
                                                          "item_excludes_zero": bool(d["item"].get("excludes_zero")), "persona_excludes_zero": bool(d["cluster"].get("excludes_zero"))}
    # reach of the forbidding record (by identifier) among the 47 FULL obligations, and the 104
    ret = J(ROOT / "resp_review/l2/retrieval.json")["items"]
    for pop_name, pop in (("full_47", [it for it in full if it["y_nok"]]), ("all_104", [it for it in sub if it["y_nok"]])):
        k5 = k10 = 0; per_state = collections.defaultdict(lambda: [0, 0, 0])
        for it in pop:
            pm = set(it.get("pn_members") or []); ids = ret[it["item_id"]]["top10_ids"]
            r5 = bool(pm & set(ids[:5])); r10 = bool(pm & set(ids[:10]))
            k5 += r5; k10 += r10; per_state[it["state"]][0] += 1; per_state[it["state"]][1] += r5; per_state[it["state"]][2] += r10
        out["reach_47" if pop_name == "full_47" else "reach_104"] = {"n": len(pop), "k5": k5, "k10": k10, "per_state (n, k5, k10)": dict(per_state)}
    assert out["reach_104"]["k5"] == GATES_661["reach_k5"] and out["reach_104"]["k10"] == GATES_661["reach_k10"]
    return out


def main():
    assert_spec()
    sub = RC.load_cell()
    z2r = z2(sub); z2r["meta"] = {"script": "reviews/r113/tools/z2_z3_full_population.py", "spec": "SPEC_R113 Z2", "model_calls": 0, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(z2r, RESULTS / "z2_full_population.json")
    z3r = z3(sub); z3r["meta"] = {"script": "reviews/r113/tools/z2_z3_full_population.py", "spec": "SPEC_R113 Z3", "model_calls": 0, "n_boot": 1000, "seed": 42, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(z3r, RESULTS / "z3_frbank_comparators_full.json")
    c = z2r["checks_against_amendment_2_sections_0_and_3"]
    L = ["\n## 2. AUX-R113-Z2: the FULL-store population of the Graphiti comparison, recounted (SPEC_R113 Z2; no call)\n\n",
         f"From `resp_common.load_cell()` (the 661): FULL **{z2r['full']}** ({z2r['full_absent']} ABSENT / {z2r['full_present']} PRESENT / {z2r['full_pn']} PRESENT-NEGATIVE), non-ABSENT FULL **{z2r['full_non_absent']}**; the 47 obligations by subtype {z2r['pn_subtype']}, intent {z2r['pn_intent']}, state {z2r['pn_state']}, attack vector {z2r['pn_attack_vector']}, over {z2r['pn_personas']} personas; the 131 licensed by intent {z2r['licensed_intent']} over {z2r['licensed_personas']} personas. ",
         f"Non-FULL items against the FULL sibling of the same question: labels equal **{z2r['sibling_equal']}**, the full store contradicts the label **{z2r['sibling_contradicts']}** ({z2r['sibling_contradicts_detail']}; `aisha_q03` CAT-ABLATED among them: {z2r['aisha_q03_cat_ablated_in_contradictions']}), no FULL sibling in the cell **{z2r['no_sibling']}**; over the {z2r['ablated_non_absent']} ablated non-ABSENT items, {z2r['ablated_dup']} duplicate the sibling's label and subtype and {z2r['ablated_contra']} contradict it. ",
         f"The FULL-variant census record (`r85_graphiti/g10/census_full_variant_g10.json`, read): {json.dumps(z2r['census_full_variant_record'])}. ",
         f"Every count Amendment 2 sections 0 and 3 state reproduces: **{z2r['all_checks_pass']}** (`reviews/r113/results/z2_full_population.json` `checks_against_amendment_2_sections_0_and_3`).\n"]
    L.append("\n## 3. AUX-R113-Z3: the FR-Bank comparators on the FULL-variant population (SPEC_R113 Z3; the section 0 \"$0 repair\", FR-Bank side; no Graphiti number; no call)\n\n")
    L.append(f"Reproduction gates on the 661, all equal to the ledgered values: {json.dumps({k: v['auroc'] for k, v in z3r['gates_661'].items()})}; reach 54 / 74 of 104. Population the 323 FULL items, positives the 47 obligations; per state this state's positives against every FULL negative (276). Haiku 4.5 rows are X4's collapse (units with at least three draws).\n\n")
    L.append("### AUX-R113-Z3-ROWS: each reader on the 323 (single-arm item and persona intervals), the 661 beside\n\n| reader | 661 | 323, all (47 of 323) | item 95% | persona 95% | supersession | expiry | retraction |\n|---|---:|---:|---|---|---:|---:|---:|\n")
    names = {"mini_true": "GPT-4.1 mini INDEXED-TRUE", "mini_blind": "GPT-4.1 mini BLIND", "mini_retrieved": "GPT-4.1 mini RETRIEVED (join tags)", "mini_hybrid": "GPT-4.1 mini HYBRID",
             "mini_believed": "GPT-4.1 mini RETRIEVED-BELIEVED (own marks)", "lookup_emb": "embedding lookup (superseded section)", "lookup_lex": "lexical lookup",
             "h45_true": "Haiku 4.5 INDEXED-TRUE", "h45_retrieved": "Haiku 4.5 RETRIEVED (join tags)", "h45_hybrid": "Haiku 4.5 HYBRID"}
    for k, nm in names.items():
        s = z3r["single_arm"][k]; a = s["all"]
        L.append(f"| {nm} | {z3r['gates_661'][k]['auroc']:.4f} | **{a['auroc']:.4f}** (n {a['n']}, pos {a['n_pos']}) | [{a['item_ci'][0]:.4f}, {a['item_ci'][1]:.4f}] | [{a['persona_ci'][0]:.4f}, {a['persona_ci'][1]:.4f}] | {s['supersession']['auroc']:.4f} ({s['supersession']['n_pos']}) | {s['expiry']['auroc']:.4f} ({s['expiry']['n_pos']}) | {s['retraction']['auroc']:.4f} ({s['retraction']['n_pos']}) |\n")
    L.append("\n### AUX-R113-Z3-PAIRED: the recorded pairings on the 323, the 661 beside (paired difference; item and persona intervals; an asterisk marks both excluding zero)\n\n| pairing | population | all: base -> arm, D | item 95% | persona 95% | supersession D | expiry D | retraction D |\n|---|---|---|---|---|---:|---:|---:|\n")
    pn = {"mini_retrieved_minus_true": "mini RETRIEVED - INDEXED-TRUE", "mini_hybrid_minus_true": "mini HYBRID - INDEXED-TRUE", "mini_believed_minus_retrieved": "mini RETRIEVED-BELIEVED - RETRIEVED",
          "mini_believed_minus_true": "mini RETRIEVED-BELIEVED - INDEXED-TRUE", "h45_retrieved_minus_true": "Haiku RETRIEVED - INDEXED-TRUE", "h45_hybrid_minus_true": "Haiku HYBRID - INDEXED-TRUE",
          "lookup_emb_minus_mini_true": "embedding lookup - mini INDEXED-TRUE"}
    for k, nm in pn.items():
        for pop in ("full_323", "all_661"):
            d = z3r["paired"][k][pop]; a = d["all"]; star = "*" if a["item_excludes_zero"] and a["persona_excludes_zero"] else ""
            L.append(f"| {nm} | {pop} | {a['base']:.4f} -> {a['arm']:.4f}, **{a['D']:+.4f}**{star} (n {a['n']}) | [{a['item_ci'][0]:+.4f}, {a['item_ci'][1]:+.4f}] | [{a['persona_ci'][0]:+.4f}, {a['persona_ci'][1]:+.4f}] | {d['supersession']['D']:+.4f} | {d['expiry']['D']:+.4f} | {d['retraction']['D']:+.4f} |\n")
    r47 = z3r["reach_47"]; r104 = z3r["reach_104"]
    L.append(f"\n### AUX-R113-Z3-REACH: the forbidding record among the recorded top-k by identifier\n\nThe 47 FULL obligations: in ranks 1 to 5 **{r47['k5']}** of 47, in ranks 1 to 10 **{r47['k10']}**; per state (n, k5, k10) {r47['per_state (n, k5, k10)']}. The 104 (the ledgered AUX-RESP-L2-REACH row): {r104['k5']} / {r104['k10']} of 104.\n")
    ledger_append("".join(L))


if __name__ == "__main__":
    main()
