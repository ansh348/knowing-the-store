# -*- coding: utf-8 -*-
"""r130_build.py -- program R130, Phase 0 (offline, $0): the population census and the build file.

    python r130_build.py            writes reviews/r130/build/build_r130.json: the 305 views (the Luna jobs, with view text and sha),
                                    the 610 recorded judge units (mini / Haiku answers with the reference strings), the per-policy
                                    census, the P-L1 / P-L1b / P-L2 / P-L3 / P-L3b / P-L4 populations, the HV1-key lock map, the input digests. Asserts
                                    every EXPECT count; a mismatch is a STOP.

No model call. Reads the recorded rows only; nothing in ds_downstream/ is written.
"""
from __future__ import annotations

import collections
import json
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r130_common as C  # noqa: E402


def census(D, jobs):
    st1, views, byid = D["st1"], D["views"], D["byid"]
    pn = [it for it in D["sub"] if it["label"] == "PRESENT-NEGATIVE"]
    assert len(pn) == C.EXPECT["obligations"]
    per_policy = {}
    for p in C.POLICIES:
        ans = [it for it in pn if st1[it["item_id"]][p]["reach"] and not st1[it["item_id"]][p]["abstain"]]
        per_policy[p] = {"reach": sum(1 for it in pn if st1[it["item_id"]][p]["reach"]), "tagged_reach": sum(1 for it in pn if st1[it["item_id"]][p]["tagged_reach"]),
                         "abstain": sum(1 for it in pn if st1[it["item_id"]][p]["abstain"]), "answered": len(ans),
                         "answered_by_state": dict(collections.Counter(it["state"] for it in ans)),
                         "answered_scorable": sum(1 for it in ans if it["state"] != "exp"),
                         "answered_keys": sorted(f"{it['item_id']}|{views[it['item_id']][p]['sha']}" for it in ans)}
    reached_any = {it["item_id"] for it in pn if any(st1[it["item_id"]][p]["reach"] and not st1[it["item_id"]][p]["abstain"] for p in C.POLICIES)}
    assert len(reached_any) == C.EXPECT["obligations_reached"], len(reached_any)
    # P-L1 / P-L4: ORACLE answered with the tagged forbidding record in view (all states); P-L1b: the LOOKUP version;
    # P-L2: answered under ALWAYS and LOOKUP; P-L3: ORACLE answered, sup/ret (the audited scorable views), split by the active copy; P-L3b: the LOOKUP version
    def answered(p):
        return [it for it in pn if st1[it["item_id"]][p]["reach"] and not st1[it["item_id"]][p]["abstain"]]

    def split_active(p, its):
        src = {}
        for it in its:
            rc = D["rec"].get(it["item_id"])
            src[it["item_id"]] = D["A4"].view_source(views[it["item_id"]][p]["text"], rc) if rc else None
        active = [i for i, s in src.items() if s == "active"]; without = [i for i, s in src.items() if s in ("tagged_only", "none")]
        corr = "frbank:fatima:fatima_q06:FULL"      # R129 A2: the inverted retraction tag corrected on paper; the view as answered is unchanged
        return {"active": sorted(active), "without": sorted(without), "n_active": len(active), "n_without": len(without),
                "source_counts": {str(k): v for k, v in collections.Counter(src.values()).items()}, "expiry_excluded": sum(1 for s in src.values() if s is None),
                "by_state_active": dict(collections.Counter(byid[i]["state"] for i in active)), "by_state_without": dict(collections.Counter(byid[i]["state"] for i in without)),
                "corrected": {"active": sorted(i for i in active if i != corr), "without": sorted(without + ([corr] if corr in active else [])), "n_active": len(active) - (corr in active),
                              "n_without": len(without) + (corr in active), "item": corr, "note": "R129 A2: the inverted retraction tag on fatima_q06 corrected on paper; the view as answered is unchanged"}}
    orc, lk, al = answered("ORACLE"), answered("LOOKUP"), answered("ALWAYS")
    pl1 = [it["item_id"] for it in orc if st1[it["item_id"]]["ORACLE"]["tagged_reach"]]
    pl1b = [it["item_id"] for it in lk if st1[it["item_id"]]["LOOKUP"]["tagged_reach"]]
    pl2 = [it["item_id"] for it in lk if it in al]
    same = [i for i in pl2 if views[i]["ALWAYS"]["sha"] == views[i]["LOOKUP"]["sha"]]
    aud = C.J(C.ROOT / "reviews" / "downstream_audit" / "step4b_view_lines.json")["view_lines"]
    audited = sorted(k.split("|")[0] for k in aud if k.endswith("|ORACLE"))
    pl3 = split_active("ORACLE", [it for it in orc if it["state"] != "exp"]); pl3b = split_active("LOOKUP", lk)
    for i in pl3["active"]:
        assert aud[f"{i}|ORACLE"]["any_active_stale"], i
    for i in pl3["without"]:
        assert not aud[f"{i}|ORACLE"]["any_active_stale"], i
    pops = {"P-L1": {"policy": "ORACLE", "obligations": sorted(pl1), "n": len(pl1), "by_state": dict(collections.Counter(byid[i]["state"] for i in pl1)),
                     "personas": len({byid[i]["persona"] for i in pl1}), "same_view_as_lookup": sum(1 for i in pl1 if views[i]["ORACLE"]["sha"] == views[i]["LOOKUP"]["sha"])},
            "P-L1b": {"policy": "LOOKUP", "obligations": sorted(pl1b), "n": len(pl1b), "by_state": dict(collections.Counter(byid[i]["state"] for i in pl1b)),
                      "personas": len({byid[i]["persona"] for i in pl1b})},
            "P-L2": {"obligations": sorted(pl2), "n": len(pl2), "same_view_under_both": sorted(same), "n_same_view": len(same), "n_informative": len(pl2) - len(same),
                     "always_answered": len(al), "lookup_answered": len(lk), "personas": len({byid[i]["persona"] for i in pl2})},
            "P-L3": {"policy": "ORACLE", "audited_scorable_views": len(audited), "answered_of_audited": len(pl3["active"]) + len(pl3["without"]),
                     "unanswered_audited": sorted(set(audited) - set(pl3["active"]) - set(pl3["without"])), "personas": len({byid[i]["persona"] for i in pl3["active"] + pl3["without"]}), **pl3},
            "P-L3b": {"policy": "LOOKUP", "personas": len({byid[i]["persona"] for i in pl3b["active"] + pl3b["without"]}), **pl3b},
            "P-L4": {"policy": "ORACLE", "note": "the P-L1 pairs; MENTIONS in place of ASSERTS", "n": len(pl1)}}
    E = C.EXPECT
    assert pops["P-L1"]["n"] == E["pl1_pairs"] and pops["P-L1b"]["n"] == E["pl1b_pairs"] and pops["P-L2"]["n"] == E["pl2_pairs"] and pops["P-L2"]["n_same_view"] == E["pl2_same_view"]
    assert pops["P-L3"]["n_active"] == E["pl3_active"] and pops["P-L3"]["n_without"] == E["pl3_without"] and pops["P-L3"]["audited_scorable_views"] == 89
    assert pops["P-L3b"]["n_active"] == E["pl3b_active"] and pops["P-L3b"]["n_without"] == E["pl3b_without"]
    assert per_policy["LOOKUP"]["answered"] == E["lookup_answered"] and per_policy["ORACLE"]["answered"] == E["oracle_answered"]
    retag = collections.Counter(p for j in jobs if j["source"] == "a5" for p in j["policies"])
    return {"per_policy": per_policy, "obligations": len(pn), "obligations_by_state": dict(collections.Counter(it["state"] for it in pn)),
            "obligations_reached_any": len(reached_any), "unreached": sorted(set(it["item_id"] for it in pn) - reached_any),
            "personas_over_obligations": len({it["persona"] for it in pn}), "populations": pops,
            "retag_views_by_policy": dict(retag), "retag_views_by_state": dict(collections.Counter(j["state"] for j in jobs if j["source"] == "a5"))}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    pins = C.assert_inputs()
    D = C.load_ds(); jobs = C.luna_jobs(D)
    units = C.judge_units(D)
    assert len(units) == C.EXPECT["units_recorded"], len(units)
    assert all(u["status"] == "OK" and isinstance(u["answer"], str) for u in units), "a recorded answer is missing -- STOP"
    lockmap = C.lock_against_hv1_key(units)
    cen = census(D, jobs)
    import statistics
    chars = [len(j["view"]) for j in jobs]
    out = {"meta": {"program": C.PROGRAM, "built": C.now(), "inputs_sha256": pins, "judge_prompt_sha256": C.judge_digests(),
                    "views_sha256": C.sha_text("".join(j["view_sha"] + j["view"] for j in sorted(jobs, key=lambda j: j["key"]))),
                    "units_sha256": C.sha_text("".join(u["unit_id"] + u["question"] + u["stale"] + u["gold"] + u["answer"] for u in sorted(units, key=lambda u: u["unit_id"]))),
                    "n_views": len(jobs), "n_views_a4": sum(1 for j in jobs if j["source"] == "a4"), "n_views_a5": sum(1 for j in jobs if j["source"] == "a5"),
                    "n_units_recorded": len(units), "view_chars": {"mean": round(statistics.mean(chars), 1), "max": max(chars), "sum": sum(chars)},
                    "view_lines": {"mean": round(statistics.mean(j["n_lines"] for j in jobs), 2), "max": max(j["n_lines"] for j in jobs)},
                    "hv1_key_lock": {"items": len(lockmap), "blocks": dict(collections.Counter(C.J(C.HV1 / "key" / "key_hv1.json")["hva"]["items"][u]["block"] for u in lockmap))}},
           "census": cen, "jobs": jobs, "units": units, "hv1_lock": lockmap}
    C.jdump(out, C.BUILD / "build_r130.json")
    print(json.dumps({k: v for k, v in out["meta"].items()}, indent=1))
    print(json.dumps({k: v for k, v in cen.items() if k != "per_policy"}, indent=1)[:3000])
    for p, d in cen["per_policy"].items():
        print(f"{p:10s} reach {d['reach']:3d} tagged {d['tagged_reach']:3d} abstain {d['abstain']:3d} answered {d['answered']:3d} scorable {d['answered_scorable']:3d} {d['answered_by_state']}")
    print("retag views by policy", cen["retag_views_by_policy"], "by state", cen["retag_views_by_state"])


if __name__ == "__main__":
    main()
