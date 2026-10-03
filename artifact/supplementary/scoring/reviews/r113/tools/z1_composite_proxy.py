# -*- coding: utf-8 -*-
"""z1_composite_proxy.py -- SPEC_R113 section Z1: the composite's five-line proxy (DS Amendment 7, AUX-DS-A7-COMPOSITE-ANSWERED).
NO MODEL CALL. $0. For every ABSENT item and gated policy whose coverage rule let the item through onto a view longer than
five lines, finds whether any recorded row (any prompt variant, either answerer) or any cache entry carries an answer on
that exact (item, view sha). Writes reviews/r113/results/z1_composite_proxy.json and appends AUX-R113-Z1-* to NUMBERS_R113.md.
Reading rule (spec): full coverage -> recompute; none -> the proxy stands and the required generation is listed; partial -> counted.
"""
from __future__ import annotations

import collections
import datetime as dt
import glob
import io
import json

from r113_common import ROOT, RESULTS, J, jdump, assert_spec, ledger_append

DS = ROOT / "ds_downstream"
POLS = ("MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT")
EXPECTED = {"MODEL": 10, "LOOKUP": 17, "LOOKUP-LIT": 72}


def main():
    assert_spec()
    st1 = J(DS / "stage1.json")["per_item"]
    views = J(DS / "views.json")["items"]
    pol = J(DS / "policies.json")["items"]
    assert len(st1) == len(views) == len(pol) == 661
    absent = [i for i in st1 if pol[i]["label"] == "ABSENT"]; assert len(absent) == 383
    # every (item, view sha) with a recorded answer, by file; and every cache entry's (item_id|view_sha) key
    have = collections.defaultdict(set)
    row_files = sorted(glob.glob(str(DS / "run" / "rows_*.jsonl")))
    for f in row_files:
        for l in io.open(f, encoding="utf-8"):
            r = json.loads(l)
            have[(r["item_id"], r["view_sha"])].add(f.split("run")[-1].strip("\\/"))
    cache_keys = set()
    cache_files = sorted(glob.glob(str(DS / "cache*" / "responses.json")))
    for c in cache_files:
        for v in J(c).values():
            cache_keys.add(v.get("item_id"))       # e0's cache stores item_id as "<item>|<view sha>"
    need, per_policy = [], {}
    for p in POLS:
        ids = [i for i in absent if not st1[i][p]["abstain"] and st1[i][p]["view_size"] > 5]
        per_policy[p] = {"items": len(ids), "answered_on_exact_view": 0, "in_cache_on_exact_view": 0}
        for i in ids:
            v = views[i][p]; key = (i, v["sha"])
            ans = sorted(have.get(key, ())); inc = f"{i}|{v['sha']}" in cache_keys
            per_policy[p]["answered_on_exact_view"] += int(bool(ans)); per_policy[p]["in_cache_on_exact_view"] += int(inc)
            need.append({"item_id": i, "persona": pol[i]["persona"], "policy": p, "view_sha": v["sha"], "n_lines": v["n_lines"],
                         "fetch_set": pol[i]["policies"][p]["fetch_set"], "fetched": len(pol[i]["policies"][p]["fetched"]),
                         "gate": bool(pol[i]["policies"][p]["gate"]), "answered_in": ans, "in_cache": inc})
    for p, k in EXPECTED.items():
        assert per_policy[p]["items"] == k, (p, per_policy[p]["items"], k)
    distinct = {(d["item_id"], d["view_sha"]) for d in need}
    same_items = {"MODEL==MODEL-ALL": sorted({d["item_id"] for d in need if d["policy"] == "MODEL"}) == sorted({d["item_id"] for d in need if d["policy"] == "MODEL-ALL"}),
                  "LOOKUP==LOOKUP-ALL": sorted({d["item_id"] for d in need if d["policy"] == "LOOKUP"}) == sorted({d["item_id"] for d in need if d["policy"] == "LOOKUP-ALL"})}
    shared_view = {"MODEL_vs_MODEL-ALL_same_sha": sum(1 for i in absent if not st1[i]["MODEL"]["abstain"] and st1[i]["MODEL"]["view_size"] > 5 and views[i]["MODEL"]["sha"] == views[i]["MODEL-ALL"]["sha"]),
                   "LOOKUP_vs_LOOKUP-ALL_same_sha": sum(1 for i in absent if not st1[i]["LOOKUP"]["abstain"] and st1[i]["LOOKUP"]["view_size"] > 5 and views[i]["LOOKUP"]["sha"] == views[i]["LOOKUP-ALL"]["sha"]),
                   "LOOKUP_vs_LOOKUP-LIT_same_sha": sum(1 for i in absent if not st1[i]["LOOKUP"]["abstain"] and st1[i]["LOOKUP"]["view_size"] > 5 and views[i]["LOOKUP"]["sha"] == views[i]["LOOKUP-LIT"]["sha"])}
    # do any of these expanded views coincide with an Amendment 6 flat or gated view of the same item? (covered by `have`, stated explicitly)
    amend6_hits = sum(1 for d in need if any("amend6" in f for f in d["answered_in"]))
    n_answered = sum(1 for d in need if d["answered_in"] or d["in_cache"])
    lines_total = sum(d["n_lines"] for d in need)
    items_union = sorted({d["item_id"] for d in need})
    res = {"meta": {"script": "reviews/r113/tools/z1_composite_proxy.py", "spec": "reviews/r113/SPEC_R113.md section Z1", "model_calls": 0,
                    "row_files_scanned": [f.split("ds_downstream")[-1].strip("\\/") for f in row_files], "cache_files_scanned": [c.split("ds_downstream")[-1].strip("\\/") for c in cache_files],
                    "recorded_answer_keys": len(have), "cache_entries": len(cache_keys), "when": dt.datetime.now().isoformat(timespec="seconds")},
           "per_policy": per_policy, "same_item_sets": same_items, "same_view_sha_across_policies": shared_view,
           "distinct_inputs_needing_an_answer": len(distinct), "distinct_absent_items": len(items_union),
           "inputs_with_any_recorded_answer": n_answered, "inputs_answered_on_an_amendment6_view": amend6_hits,
           "generation_required": {"per_answerer_calls": len(distinct), "answerers": ["gpt-4.1-mini", "claude-haiku-4-5-20251001"],
                                   "prompt": "USER_ANSWER_A4 (the Amendment 4 header) with SYSTEM_ANSWER; one call per distinct (item, view), the answer shared by every policy whose view is byte-identical",
                                   "view_lines_total_per_answerer": lines_total},
           "reading": None, "inputs": need}
    if n_answered == 0:
        res["reading"] = ("none of the inputs has a recorded answer: the five-line proxy stands as AUX-DS-A7-COMPOSITE-ANSWERED and the tab:ds-a7 caption state it; "
                          "no composite number changes; the generation required is listed under generation_required and inputs")
    elif n_answered == len(need):
        res["reading"] = "every input has a recorded answer: recompute the answered reading on the actual views (not done here; see the spec)"
    else:
        res["reading"] = f"partial: {n_answered} of {len(need)} inputs have a recorded answer; nothing changes"
    jdump(res, RESULTS / "z1_composite_proxy.json")
    pp = per_policy
    L = ["\n## 1. AUX-R113-Z1: the composite's five-line proxy, the answers that would be needed (SPEC_R113 Z1; DS Amendment 7; no call)\n\n",
         f"Inputs: `ds_downstream/stage1.json`, `views.json`, `policies.json`; every `ds_downstream/run/rows_*.jsonl` ({len(row_files)} files, {len(have)} distinct recorded (item, view) answers) and every `ds_downstream/cache*/responses.json` ({len(cache_files)} files, {len(cache_keys)} entries). ",
         f"ABSENT items whose coverage rule let them through onto a view longer than five lines: MODEL **{pp['MODEL']['items']}**, LOOKUP **{pp['LOOKUP']['items']}**, LOOKUP-LIT **{pp['LOOKUP-LIT']['items']}** (the counts the ledger and the caption state), MODEL-ALL {pp['MODEL-ALL']['items']} and LOOKUP-ALL {pp['LOOKUP-ALL']['items']} (the same items as MODEL and LOOKUP: {same_items}; their F(N3) views share the F(N2) view's sha on {shared_view['MODEL_vs_MODEL-ALL_same_sha']} and {shared_view['LOOKUP_vs_LOOKUP-ALL_same_sha']} items; LOOKUP and LOOKUP-LIT share a sha on {shared_view['LOOKUP_vs_LOOKUP-LIT_same_sha']}). ",
         f"Distinct absent items {len(items_union)}; distinct (item, view) inputs **{len(distinct)}**; inputs with a recorded answer on the exact view under any prompt variant or answerer **{n_answered}** (on an Amendment 6 flat or gated view: {amend6_hits}); in any cache {sum(1 for d in need if d['in_cache'])}.\n\n",
         f"**Reading (the spec's rule):** {res['reading']}.\n\n",
         f"### AUX-R113-Z1-GENERATION: what the answered reading on the actual views would cost in calls (not made)\n\n{len(distinct)} calls per answerer (GPT-4.1 mini; Claude Haiku 4.5), `SYSTEM_ANSWER` + `USER_ANSWER_A4` (the Amendment 4 header), one call per distinct (item, view) with the answer shared by every policy whose view is byte-identical; {lines_total} view lines per answerer in all. The list of inputs (item, policy, view sha, line count, fetch set) is `reviews/r113/results/z1_composite_proxy.json` `inputs`.\n"]
    ledger_append("".join(L))


if __name__ == "__main__":
    main()
