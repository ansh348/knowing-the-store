# -*- coding: utf-8 -*-
"""r125_matched.py -- Task 1: the matched metric on every reader of the counterfactual set (offline, post hoc, labelled so everywhere).
NO MODEL CALL. $0. Reads reviews/r125/results/r125_vectors.json (r125_readers.py); writes reviews/r125/results/r125_matched.json.

Sanity check first (a STOP if it fails): the W/T/L computed from the rows must equal every W/T/L printed in Table 1 (tab:cf-main of
v22, sha f0549e2a), so that the matched AUROC is (W + T/2) / 148 from the printed counts. Then, per reader:
  1. within-triple PN vs PRESENT: W/T/L and the matched AUROC (W + T/2) / n, whole set and per state;
  2. the same for PN vs ABSENT;
  3. the triple-level and the persona-grouped bootstrap interval of each (1,000 draws, seed 42);
  4. paired differences with both intervals: each reader minus its summary's name lookup (whole set; supersession only; every state
     beside), each reader minus each count reader on retraction and on expiry, Opus 5 under the all-states summary minus the all-states
     lookup on the whole set and per state;
  5. the pooled AUROC decomposed into its three pair classes (within-triple, same-state across questions, across states) with pair counts;
  6. the state-balanced pooled AUROC (the mean of the three per-state values).
Usage: python reviews/r125/tools/r125_matched.py
"""
from __future__ import annotations

import sys
import time

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r125_common as C  # noqa: E402
from r125_common import STATES, r4  # noqa: E402

VEC = C.RESULTS / "r125_vectors.json"
OUT = C.RESULTS / "r125_matched.json"

# Table 1 of v22 (tab:cf-main, iclr2027_monitoring_submission/paper_v22.tex lines 340-354; tex sha256 f0549e2a): the printed W/T/L, PN vs PRESENT.
TABLE1_WTL = {
    "MINI5_v2": (100, 15, 33), "MINI5_v3": (130, 5, 13), "H45_v2": (89, 52, 7), "H45_v3": (125, 18, 5), "LUNA_v2": (129, 2, 17), "SOL_v2": (126, 2, 20),
    "OP5_v2": (128, 3, 17), "OP5_v3": (139, 0, 9), "LOOKUP_v2": (82, 66, 0), "ALLSTATES_v3": (121, 27, 0), "CR-nb1_v2": (65, 83, 0), "CR-oracle-a_v2": (60, 88, 0),
}
# the appendix's post-hoc table (tab:pnpresent) and tab:cf-p1 / tab:mini-k5: further printed W/T/L, asserted too
APPENDIX_WTL = {"MINI1_v2": (81, 57, 10), "MINI1_v3": (105, 32, 11), "LUNA5_P1_v2": (125, 1, 22), "MINI1_P1_v2": (80, 52, 16)}
# the moved-count reference readers' recorded per-state pooled values (AUX-V2RCAT-REF)
V2RCAT_REF = {"CR-oracle-state_v2rcat": {"RETRACTION": 0.3028, "EXPIRY": 0.3611}, "CR-totals-a_v2rcat": {"RETRACTION": 0.4044, "EXPIRY": 0.3894}}

COUNT_READERS = ("CR-nb1", "CR-oracle-a", "CR-oracle-state", "CR-totals-a", "CR-oracle-share")
# the count readers each summary family compares against (the count table of v3 equals v2's; the E2 and P1 arms are the v2 texts)
COUNT_FAMILY = {"v2": "v2", "v3": "v2", "v2-counts": "v2", "v2-names": "v2", "v2r": "v2r", "v2rcat": "v2rcat"}
# the lookup each summary family compares against (v2r and the moved-count texts keep v2's name sections; E2's names-only arm keeps them too)
LOOKUP_FAMILY = {"v2": "LOOKUP_v2", "v3": "ALLSTATES_v3", "v2-counts": "LOOKUP_v2", "v2-names": "LOOKUP_v2", "v2r": "LOOKUP_v2", "v2rcat": "LOOKUP_v2"}


SCOPES = (("whole", None), ("sup", "SUPERSESSION"), ("ret", "RETRACTION"), ("exp", "EXPIRY"), ("counted", ("RETRACTION", "EXPIRY")))
CONTRASTS = [  # (name, A, B): A minus B
    # E2 names against counts (the recorded intact row is the comparator: mini at one draw, Haiku at five)
    ("E2 mini names-only minus intact", "MINI1_NAMES", "MINI1_v2"), ("E2 mini counts-only minus intact", "MINI1_COUNTS", "MINI1_v2"),
    ("E2 mini counts-only minus names-only", "MINI1_COUNTS", "MINI1_NAMES"), ("E2 mini names-only dash minus intact", "MINI1_NAMES_DASH", "MINI1_v2"),
    ("E2 Haiku names-only minus intact", "H45_NAMES", "H45_v2"), ("E2 Haiku counts-only minus intact", "H45_COUNTS", "H45_v2"),
    ("E2 Haiku counts-only minus names-only", "H45_COUNTS", "H45_NAMES"),
    # the moved-count control against the recorded superseded-only row (E1 Amendment 1: Opus at five draws; E9: Luna and Sol at five draws)
    ("moved count mini minus sup-only", "MINI1_v2rcat", "MINI1_v2"), ("moved count Haiku minus sup-only", "H45_v2rcat", "H45_v2"),
    ("moved count Opus k5 minus sup-only k5", "OP5_v2rcat", "OP5_v2"), ("moved count Opus draw 1 minus sup-only k5 (registered)", "OP5_v2rcat_d1", "OP5_v2"),
    ("moved count Opus draw 1 minus sup-only draw 1", "OP5_v2rcat_d1", "OP5_v2_d1"),
    ("moved count Luna k5 minus sup-only k5 (E9)", "LUNA_v2rcat", "LUNA_v2"), ("moved count Sol k5 minus sup-only k5 (E9)", "SOL_v2rcat", "SOL_v2"),
    ("moved count Luna draw 1 minus sup-only draw 1", "LUNA_v2rcat_d1", "LUNA_v2_d1"), ("moved count Sol draw 1 minus sup-only draw 1", "SOL_v2rcat_d1", "SOL_v2_d1"),
    # the totals-randomized summary against the superseded-only one
    ("totals rand. mini minus sup-only", "MINI1_v2r", "MINI1_v2"), ("totals rand. Haiku minus sup-only", "H45_v2r", "H45_v2"), ("totals rand. Opus minus sup-only", "OP5_v2r", "OP5_v2"),
    # the all-states summary against the superseded-only one (the counted states are where the names are added)
    ("all-states mini k1 minus sup-only", "MINI1_v3", "MINI1_v2"), ("all-states mini k5 minus sup-only", "MINI5_v3", "MINI5_v2"),
    ("all-states Haiku minus sup-only", "H45_v3", "H45_v2"), ("all-states Opus minus sup-only", "OP5_v3", "OP5_v2"), ("all-states lookup minus name lookup", "ALLSTATES_v3", "LOOKUP_v2"),
    # the intent-explicit rubric against the main-study rubric (R122 T4)
    ("intent-explicit Luna minus main-study", "LUNA5_P1_v2", "LUNA_v2"), ("intent-explicit mini minus main-study", "MINI1_P1_v2", "MINI1_v2"),
    # five draws against one (R122 T3; the draw-1 rows of the five-draw lanes)
    ("mini five draws minus one draw (v2)", "MINI5_v2", "MINI1_v2"), ("mini five draws minus one draw (v3)", "MINI5_v3", "MINI1_v3"),
    ("Opus draw 1 minus five draws (v2)", "OP5_v2_d1", "OP5_v2"), ("Haiku draw 1 minus five draws (v2)", "H45_v2_d1", "H45_v2"),
    ("Luna draw 1 minus five draws (v2)", "LUNA_v2_d1", "LUNA_v2"), ("Sol draw 1 minus five draws (v2)", "SOL_v2_d1", "SOL_v2"),
    # E10 the hybrid reader against the lookup, the guessing count reader and each model
    ("hybrid minus name lookup (P-H1)", "HYBRID_v2", "LOOKUP_v2"), ("hybrid minus guessed-category count reader", "HYBRID_v2", "CR-nb1_v2"),
    ("Sol minus hybrid (P-H2)", "SOL_v2", "HYBRID_v2"), ("Luna minus hybrid", "LUNA_v2", "HYBRID_v2"), ("Opus minus hybrid", "OP5_v2", "HYBRID_v2"),
    ("Haiku minus hybrid", "H45_v2", "HYBRID_v2"), ("mini k5 minus hybrid", "MINI5_v2", "HYBRID_v2"), ("mini k1 minus hybrid", "MINI1_v2", "HYBRID_v2"),
    # the random-token control and the encoders against the name lookup
    ("random-token minus name lookup (v2)", "RANDTOK_v2", "LOOKUP_v2"), ("random-token minus all-states lookup (v3)", "RANDTOK_v3", "ALLSTATES_v3"),
    ("mpnet minus MiniLM (v2)", "MPNET_v2", "LOOKUP_v2"), ("bge-small minus MiniLM (v2)", "BGE_v2", "LOOKUP_v2"),
    # every model against the category-guessing and the category-aware count reader on the whole set (the body's count-reader sentences)
    ("Opus minus guessed-category count reader", "OP5_v2", "CR-nb1_v2"), ("Luna minus guessed-category count reader", "LUNA_v2", "CR-nb1_v2"),
    ("Sol minus guessed-category count reader", "SOL_v2", "CR-nb1_v2"), ("Haiku minus guessed-category count reader", "H45_v2", "CR-nb1_v2"),
    ("mini k5 minus guessed-category count reader", "MINI5_v2", "CR-nb1_v2"), ("mini k1 minus guessed-category count reader", "MINI1_v2", "CR-nb1_v2"),
    ("name lookup minus guessed-category count reader", "LOOKUP_v2", "CR-nb1_v2"),
]


def reader_block(cell, v):
    out = {"pooled": C.per_state_pooled(cell, v), "pair_classes": {"whole": C.pair_classes(cell, v)}}
    for s in STATES:
        out["pair_classes"][s] = C.pair_classes(cell, v, cell.st == s)
    for neg in ("PRESENT", "ABSENT"):
        key = f"pn_vs_{neg.lower()}"
        out[key] = {"whole": C.matched_block(cell, v, neg), "per_state": {s: C.matched_block(cell, v, neg, s) for s in STATES}}
        out[key]["state_balanced"] = r4(np.mean([out[key]["per_state"][s]["matched"] for s in STATES]))
    return out


def main():
    t0 = time.time()
    cell = C.Cell()
    doc = C.jload(VEC); readers = doc["readers"]
    V = {k: cell.vector({i: (np.nan if x is None else x) for i, x in r["vector"].items()}) for k, r in readers.items()}
    res = {"meta": {"script": "reviews/r125/tools/r125_matched.py", "model_calls": 0, "status": "post hoc, offline; the matched metric labelled so everywhere",
                    "n_boot": C.N_BOOT, "seed": C.SEED, "vectors": str(VEC.relative_to(C.ROOT)), "tie_rule": "exact equality of the collapsed scores (posthoc_b_pnpresent.py)",
                    "matched_auroc": "(W + T/2) / n over the triples scored; PN against PRESENT (primary) and PN against ABSENT",
                    "intervals": "triple-level bootstrap (triples resampled) and persona-grouped bootstrap (personas resampled, triples intact); 2.5 / 97.5 percentiles"},
           "sanity": {}, "readers": {}, "paired": {"vs_lookup": {}, "vs_count_readers": {}, "opus_v3_vs_allstates": {}}}

    # ---- the sanity check: Table 1's printed W/T/L reproduce from the rows
    print("sanity check: Table 1's W/T/L from the rows")
    ok_all = True
    for key, (w, t, l) in list(TABLE1_WTL.items()) + list(APPENDIX_WTL.items()):
        got = C.wtl(C.outcomes(cell, V[key], "PRESENT"))
        ok = (got["W"], got["T"], got["L"]) == (w, t, l)
        ok_all &= ok
        res["sanity"][key] = {"printed": [w, t, l], "computed": [got["W"], got["T"], got["L"]], "matched_from_printed": r4((w + t / 2.0) / 148), "matched_computed": got["matched"], "ok": ok,
                              "where": "Table 1" if key in TABLE1_WTL else "appendix (tab:pnpresent / tab:cf-p1)"}
        print(f"  {key:16s} printed {w:3d}/{t:3d}/{l:3d}  computed {got['W']:3d}/{got['T']:3d}/{got['L']:3d}  matched {got['matched']}  {'ok' if ok else 'MISMATCH'}")
    for key, ref in V2RCAT_REF.items():
        ps = C.per_state_pooled(cell, V[key])["per_state"]
        for s, want in ref.items():
            ok = ps[s] == want; ok_all &= ok
            res["sanity"][f"{key}/{s}"] = {"recorded_pooled": want, "computed": ps[s], "ok": ok, "where": "AUX-V2RCAT-REF"}
            print(f"  {key:24s} {s:10s} recorded {want}  computed {ps[s]}  {'ok' if ok else 'MISMATCH'}")
    res["sanity"]["all_ok"] = ok_all
    if not ok_all:
        C.jdump(res, OUT)
        raise SystemExit("SANITY CHECK FAILED -- STOP (Task 1's stop rule)")

    # ---- per reader
    print("per reader: pooled, pair classes, matched PN vs PRESENT / PN vs ABSENT with both intervals")
    for key, r in readers.items():
        b = reader_block(cell, V[key])
        b.update({"label": r["label"], "summary": r["summary"], "source": r["source"], "gate": r["gate"], "covered": r["covered"], "distinct_values": r["distinct_values"]})
        res["readers"][key] = b
        pp, pa = b["pn_vs_present"]["whole"], b["pn_vs_absent"]["whole"]; pc = b["pair_classes"]["whole"]
        print(f"  {key:22s} pooled {b['pooled']['whole']:.4f} bal {b['pooled']['state_balanced']:.4f} | PNvPR {pp['W']:3d}/{pp['T']:3d}/{pp['L']:3d} {pp['matched']:.4f} "
              f"[{pp['ci_triple']['ci_lo']:.4f},{pp['ci_triple']['ci_hi']:.4f}] [{pp['ci_persona']['ci_lo']:.4f},{pp['ci_persona']['ci_hi']:.4f}] | PNvAB {pa['W']:3d}/{pa['T']:3d}/{pa['L']:3d} {pa['matched']:.4f} "
              f"| classes wt {pc['within_triple']['auroc']:.4f} ss {pc['same_state_across_questions']['auroc']:.4f} xs {pc['across_states']['auroc']:.4f}")

    # ---- paired differences
    print("paired: each reader minus its summary's lookup (whole; supersession; every state)")
    for key, r in readers.items():
        lk = LOOKUP_FAMILY[r["summary"]]
        if key == lk:
            continue
        d = {"lookup": lk}
        for neg in ("PRESENT", "ABSENT"):
            d[f"pn_vs_{neg.lower()}"] = {"whole": C.paired_matched(cell, V[key], V[lk], neg), "per_state": {s: C.paired_matched(cell, V[key], V[lk], neg, s) for s in STATES}}
        res["paired"]["vs_lookup"][key] = d
        w, s_ = d["pn_vs_present"]["whole"], d["pn_vs_present"]["per_state"]["SUPERSESSION"]
        print(f"  {key:22s} minus {lk:12s} whole {w['delta']:+.4f} {C.ci(w['ci_triple'])} {C.ci(w['ci_persona'])} {'reliable' if w['both_exclude_zero'] else ''} | sup {s_['delta']:+.4f} {C.ci(s_['ci_triple'])} {C.ci(s_['ci_persona'])} {'reliable' if s_['both_exclude_zero'] else ''}")
    print("paired: each reader minus each count reader on retraction and on expiry")
    for key, r in readers.items():
        if key.startswith("CR-"):
            continue
        fam = COUNT_FAMILY[r["summary"]]
        res["paired"]["vs_count_readers"][key] = {}
        for cr in COUNT_READERS:
            ck = f"{cr}_{fam}"
            d = {"count_reader": ck}
            for neg in ("PRESENT", "ABSENT"):
                d[f"pn_vs_{neg.lower()}"] = {s: C.paired_matched(cell, V[key], V[ck], neg, s) for s in ("RETRACTION", "EXPIRY")}
            res["paired"]["vs_count_readers"][key][cr] = d
        d1 = res["paired"]["vs_count_readers"][key]["CR-nb1"]["pn_vs_present"]; d2 = res["paired"]["vs_count_readers"][key]["CR-oracle-a"]["pn_vs_present"]
        print(f"  {key:22s} minus guessed: ret {d1['RETRACTION']['delta']:+.4f} {'rel' if d1['RETRACTION']['both_exclude_zero'] else '   '} exp {d1['EXPIRY']['delta']:+.4f} {'rel' if d1['EXPIRY']['both_exclude_zero'] else '   '}"
              f" | minus given: ret {d2['RETRACTION']['delta']:+.4f} {'rel' if d2['RETRACTION']['both_exclude_zero'] else '   '} exp {d2['EXPIRY']['delta']:+.4f} {'rel' if d2['EXPIRY']['both_exclude_zero'] else '   '}")
    print("paired: Opus 5 (all-states summary) minus the all-states lookup, whole and per state")
    for key in ("OP5_v3", "OP5_v3_d1"):
        d = {}
        for neg in ("PRESENT", "ABSENT"):
            d[f"pn_vs_{neg.lower()}"] = {"whole": C.paired_matched(cell, V[key], V["ALLSTATES_v3"], neg), "per_state": {s: C.paired_matched(cell, V[key], V["ALLSTATES_v3"], neg, s) for s in STATES}}
        res["paired"]["opus_v3_vs_allstates"][key] = d
        w = d["pn_vs_present"]["whole"]
        print(f"  {key:12s} whole {w['delta']:+.4f} {C.ci(w['ci_triple'])} {C.ci(w['ci_persona'])} {'reliable' if w['both_exclude_zero'] else ''}; per state " +
              "; ".join(f"{s[:3]} {d['pn_vs_present']['per_state'][s]['delta']:+.4f}{'*' if d['pn_vs_present']['per_state'][s]['both_exclude_zero'] else ''}" for s in STATES))

    # ---- the named contrasts the body's Section 5 sentences rest on (A minus B; whole, per state, the counted states pooled)
    print("named contrasts (A minus B) under the matched metric")
    res["paired"]["contrasts"] = {}
    for name, a, b in CONTRASTS:
        d = {"a": a, "b": b}
        for neg in ("PRESENT", "ABSENT"):
            d[f"pn_vs_{neg.lower()}"] = {sc: C.paired_matched(cell, V[a], V[b], neg, st) for sc, st in SCOPES}
        res["paired"]["contrasts"][name] = d
        p = d["pn_vs_present"]
        print(f"  {name:44s} " + "; ".join(f"{sc} {p[sc]['delta']:+.4f}{'*' if p[sc]['both_exclude_zero'] else ' '}" for sc, _ in SCOPES))

    # ---- the coverage-only reference (B3 of posthoc_b): 1 on PN and PRESENT, 0 on ABSENT
    cov = np.where(cell.ver == "ABSENT", 0.0, 1.0)
    res["coverage_only"] = {"pooled": C.per_state_pooled(cell, cov), "pn_vs_present": C.wtl(C.outcomes(cell, cov, "PRESENT")), "pn_vs_absent": C.wtl(C.outcomes(cell, cov, "ABSENT")),
                            "pair_classes": C.pair_classes(cell, cov)}
    res["meta"]["seconds"] = round(time.time() - t0, 1)
    C.jdump(res, OUT)
    print(f"-> {OUT.relative_to(C.ROOT)} ({time.time() - t0:.0f} s)")


if __name__ == "__main__":
    main()
