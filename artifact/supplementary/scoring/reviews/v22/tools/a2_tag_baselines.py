# -*- coding: utf-8 -*-
"""a2_tag_baselines.py -- CC_PASS_v18 A2: mechanical baselines on the tagged retrieved view (the 661), both tag sources.
NO MODEL CALL. $0.

The view is the recorded five-line block each monitor saw: resp_review/l2/retrieval.json (tags from the ground-truth
join) and resp_review/l2/retrieval_believed.json (the same five records, tags from FR-Bank's own marks). Each line reads
"[r] lifecycle: <state> | category: <cat> | attribute: <scrubbed name> | age: <n> days | text: ...", so the tag and the
name are parsed from the block itself, byte for byte what the model read.

Baselines, per tag source:
  TD      tag density: the fraction of the five lines tagged non-active;
  TL      tagged-name lookup: max cosine (all-MiniLM-L6-v2, score_cf.matcher) between the question and the scrubbed
          names of the lines tagged non-active; 0 when no line is tagged;
  TL-all  the same over all five lines regardless of tag;
  HL      mechanical hybrid: max of the superseded-names lookup (the TRUE summary's section, ds_common.lookup_scores,
          gated at 0.7484) and TL.
Scored whole set and per state (positives of one state against all 557 negatives, Table 34's convention), item-level and
persona-clustered intervals; paired against the monitor that saw the same input (cf2_score.paired; model minus baseline):
join tags -> GPT-4.1 mini RETRIEVED (0.6851); own marks -> RETRIEVED-BELIEVED (0.8144); HL under join -> HYBRID (0.8303).
No hybrid monitor under own marks was run, so HL-own is paired against RETRIEVED-BELIEVED and HYBRID with that stated.

Gates: 1,273 of 3,305 lines change tag between the sources (lock_amend1.json); the three monitor scores above; the lookup;
the forbidding-record census (99 forbidding records in view; 70 tagged non-active under own marks, 60 under the join).
Branches, all printed: B1 TD under own marks at or above 0.8144 - 0.05; B2 TL or HL at or above its monitor - 0.05; B3 neither.

The author's follow-up of 2026-09-14 (after the Phase 1 report): TL under join tags printed beside TL under own marks, and
the indicator FR, "the item's forbidding record is in view and tagged non-active" (1 for an obligation item when one of
its pn_members is among the five lines and that line's tag is non-active under the source; 0 for every other item), under
both sources, AUROC with both intervals; own-minus-join paired differences for TD, TL and FR. If TL and FR are both higher
under own marks, Section 6 explains the rise from 0.69 to 0.81 as the marks' reach of the forbidding records (70 of 99
against 60), not their density; if not, the rise is stated as unexplained.

Usage: python reviews/v18/tools/a2_tag_baselines.py
Writes: reviews/v18/results/a2_tag_baselines.json
"""
from __future__ import annotations

import io
import json
import os
import pathlib
import re
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "resp_review/tools", "ds_downstream/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from common_e1r import N_BOOT, SEED, auroc, boot_cluster_single  # noqa: E402
import score_cf as S  # noqa: E402
from cf2_score import paired  # noqa: E402
sys.path.insert(0, str(ROOT / "reviews" / "v18" / "tools"))
from a1_count_readers import boot_item_single, r4  # noqa: E402

RESP = ROOT / "resp_review"
OUT = ROOT / "reviews" / "v18" / "results" / "a2_tag_baselines.json"
STATES = ("SUPERSESSION", "RETRACTION", "EXPIRY")
SMAP = {"sup": "SUPERSESSION", "ret": "RETRACTION", "exp": "EXPIRY"}
GATES = {"lines": 3305, "lines_changed": 1273, "RETRIEVED": 0.6851, "RETRIEVED-BELIEVED": 0.8144, "HYBRID": 0.8303, "lookup": 0.7484}
TOL = 0.05
LINE = re.compile(r"^\[(\d)\] lifecycle: ([a-z, ]+?) \| category: (\S+) \| attribute: (\S+) \| age: ")


def parse_block(block):
    out = []
    for ln in block.split("\n"):
        m = LINE.match(ln)
        if m:
            out.append({"rank": int(m.group(1)), "tag": m.group(2).strip(), "category": m.group(3), "name": m.group(4)})
    assert len(out) == 5, f"block did not parse to five lines: {block[:120]!r}"
    return out


def mini_arm(path, arm):
    d = {}
    for ln in io.open(path, encoding="utf-8"):
        r = json.loads(ln)
        if r["arm"] == arm and r.get("status") == "OK" and r.get("nok") is not None:
            d[r["item_id"]] = float(r["nok"])
    return d


def single(s, y, g):
    return {"auroc": r4(auroc(s, y)), "item_ci": boot_item_single(s, y), "persona_ci": boot_cluster_single(s, y, g)}


def per_state(s, y, g, st):
    d = {}
    for s_ in STATES:
        m = (st == s_) | (y == 0)
        d[s_] = {"n": int(m.sum()), "pos": int(y[m].sum()), **single(s[m], y[m], g[m])}
    return d


def main():
    from ds_common import load_cell, lookup_scores  # noqa: E402
    sub = load_cell()
    rj = json.load(io.open(RESP / "l2" / "retrieval.json", encoding="utf-8"))["items"]
    rb = json.load(io.open(RESP / "l2" / "retrieval_believed.json", encoding="utf-8"))["items"]
    ids = [it["item_id"] for it in sub]; assert len(ids) == 661
    y = np.array([it["y_nok"] for it in sub], int); g = np.array([it["persona"] for it in sub])
    st = np.array([SMAP.get(rj[i]["state"], "-") for i in ids]); qs = [it["question"] for it in sub]
    res = {"meta": {"script": "reviews/v18/tools/a2_tag_baselines.py", "model_calls": 0, "n_boot": N_BOOT, "seed": SEED, "tol": TOL,
                    "per_state_convention": "positives of one state against all negatives (Table 34)", "paired_sign": "monitor minus baseline"},
           "gates": {}, "tag_census": {}, "baselines": {}, "branches": {}}

    # the two views, parsed from the blocks the monitors saw
    views = {"join": [parse_block(rj[i]["block"]) for i in ids], "own": [parse_block(rb[i]["block"]) for i in ids]}
    for src in views:
        for k, i in enumerate(ids):
            assert [l["name"] for l in views[src][k]] == [l["name"] for l in views["join"][k]], "the two views differ in their records"
    lines = sum(len(v) for v in views["join"]); changed = sum(1 for k in range(661) for a, b in zip(views["join"][k], views["own"][k]) if a["tag"] != b["tag"])
    assert lines == GATES["lines"] and changed == GATES["lines_changed"], f"GATE: tag census {changed}/{lines}"
    res["gates"]["tag_census"] = {"lines": lines, "lines_changed": changed}
    # the forbidding-record census (record level), gated against lock_amend1.json forbidding_records_in_view
    fr_rec = {"in_view": 0, "tagged_join": 0, "tagged_own": 0}
    for k, i in enumerate(ids):
        if rj[i]["label"] != "PRESENT-NEGATIVE":
            continue
        for rank, rid in enumerate(rj[i]["top5_ids"]):
            if rid in rj[i]["pn_members"]:
                fr_rec["in_view"] += 1
                fr_rec["tagged_join"] += 1 if views["join"][k][rank]["tag"] != "active" else 0
                fr_rec["tagged_own"] += 1 if views["own"][k][rank]["tag"] != "active" else 0
    lock = json.load(io.open(RESP / "run" / "lock_amend1.json", encoding="utf-8"))["tags"]["forbidding_records_in_view"]
    assert fr_rec == {"in_view": lock["tp"] + lock["fp"] + lock["fn"] + lock["tn"], "tagged_join": lock["tp"] + lock["fn"], "tagged_own": lock["tp"] + lock["fp"]}, ("GATE: forbidding-record census", fr_rec, lock)
    res["gates"]["forbidding_records_in_view"] = fr_rec
    for src in views:
        tags = [l["tag"] for v in views[src] for l in v]
        res["tag_census"][src] = {"non_active_lines": sum(1 for t in tags if t != "active"), "lines": len(tags),
                                  "items_with_no_tagged_line": sum(1 for v in views[src] if all(l["tag"] == "active" for l in v)),
                                  "tag_vocabulary": sorted({t for t in tags})}

    # monitors
    mon = {"RETRIEVED": mini_arm(RESP / "run" / "rows_resp.jsonl", "RETRIEVED"), "HYBRID": mini_arm(RESP / "run" / "rows_resp.jsonl", "HYBRID"),
           "RETRIEVED-BELIEVED": mini_arm(RESP / "run" / "rows_amend1_mini.jsonl", "RETRIEVED-BELIEVED")}
    M = {}
    for name, d in mon.items():
        v = np.array([d[i] for i in ids], float); a = r4(auroc(v, y))
        assert a == GATES[name], f"GATE: {name} {a} != {GATES[name]}"; res["gates"][name] = a; M[name] = v

    # the superseded-names lookup on the 661 (gated inside lookup_scores)
    nb6, _, gate = lookup_scores(sub)
    assert gate["pass"], f"GATE: lookup {gate}"; res["gates"]["lookup_nb6_661"] = r4(gate["nb6_661"])
    look = np.array([nb6[i] for i in ids], float)

    # baselines per tag source
    def tl(view, tagged_only):
        lists = [[l["name"] for l in v if (l["tag"] != "active" or not tagged_only)] for v in view]
        return S.matcher(qs, lists)
    B = {}
    for src, view in views.items():
        td = np.array([sum(1 for l in v if l["tag"] != "active") / 5.0 for v in view], float)
        t_l = tl(view, True); t_all = tl(view, False); hl = np.maximum(look, t_l)
        B[src] = {"TD": td, "TL": t_l, "TL-all": t_all, "HL": hl}
    # the indicator FR: the item's forbidding record is in view and tagged non-active under the source (0 for non-obligation items)
    for src, view in views.items():
        fr = np.zeros(661)
        for k, i in enumerate(ids):
            if rj[i]["label"] == "PRESENT-NEGATIVE":
                fr[k] = 1.0 if any(rid in rj[i]["pn_members"] and view[k][rank]["tag"] != "active" for rank, rid in enumerate(rj[i]["top5_ids"])) else 0.0
        B[src]["FR"] = fr
    B["lookup"] = {"superseded-names lookup": look}

    pair_with = {("join", "TD"): ["RETRIEVED"], ("join", "TL"): ["RETRIEVED"], ("join", "TL-all"): ["RETRIEVED"], ("join", "HL"): ["HYBRID"],
                 ("own", "TD"): ["RETRIEVED-BELIEVED"], ("own", "TL"): ["RETRIEVED-BELIEVED"], ("own", "TL-all"): ["RETRIEVED-BELIEVED"],
                 ("own", "HL"): ["RETRIEVED-BELIEVED", "HYBRID"], ("lookup", "superseded-names lookup"): ["RETRIEVED", "HYBRID"],
                 ("join", "FR"): ["RETRIEVED"], ("own", "FR"): ["RETRIEVED-BELIEVED"]}
    for src, d in B.items():
        res["baselines"][src] = {}
        for name, s in d.items():
            row = {"distinct_values": int(len(np.unique(np.round(s, 6)))), "whole": single(s, y, g), "per_state": per_state(s, y, g, st), "vs_monitor": {}}
            for mname in pair_with[(src, name)]:
                v = M[mname]
                row["vs_monitor"][mname] = {"monitor": r4(auroc(v, y)), "baseline": r4(auroc(s, y)), "whole": paired(s, v, y, g),
                                            "per_state": {s_: {"monitor": r4(auroc(v[(st == s_) | (y == 0)], y[(st == s_) | (y == 0)])),
                                                               "baseline": r4(auroc(s[(st == s_) | (y == 0)], y[(st == s_) | (y == 0)])),
                                                               **paired(s[(st == s_) | (y == 0)], v[(st == s_) | (y == 0)], y[(st == s_) | (y == 0)], g[(st == s_) | (y == 0)])}
                                                          for s_ in STATES},
                                            "note": ("no hybrid monitor under own marks was run; paired against the nearest monitors" if (src, name) == ("own", "HL") else "")}
            res["baselines"][src][name] = row
    # own minus join, paired, for the readers that exist under both sources; FR item counts
    res["own_minus_join"] = {name: {"join": r4(auroc(B["join"][name], y)), "own": r4(auroc(B["own"][name], y)), **paired(B["join"][name], B["own"][name], y, g)}
                             for name in ("TD", "TL", "FR")}
    pn = np.array([rj[i]["label"] == "PRESENT-NEGATIVE" for i in ids])
    res["fr_items"] = {"obligation_items": int(pn.sum()), "with_a_forbidding_record_in_view": int(sum(1 for i in ids if rj[i]["label"] == "PRESENT-NEGATIVE" and rj[i]["reach_k5"])),
                       "in_view_and_tagged_join": int(B["join"]["FR"].sum()), "in_view_and_tagged_own": int(B["own"]["FR"].sum())}
    # monitors' own per-state rows, for the table
    res["monitors"] = {name: {"whole": r4(auroc(v, y)), "per_state": {s_: r4(auroc(v[(st == s_) | (y == 0)], y[(st == s_) | (y == 0)])) for s_ in STATES}} for name, v in M.items()}

    # branches
    td_own = res["baselines"]["own"]["TD"]["whole"]["auroc"]
    b1 = td_own >= GATES["RETRIEVED-BELIEVED"] - TOL
    b2_hits = []
    for src in ("join", "own"):
        for name in ("TL", "HL"):
            for mname, vm in res["baselines"][src][name]["vs_monitor"].items():
                if vm["baseline"] >= vm["monitor"] - TOL:
                    b2_hits.append(f"{name} under {src} ({vm['baseline']}) within 0.05 of {mname} ({vm['monitor']})")
    omj = res["own_minus_join"]
    reach = omj["TL"]["own"] > omj["TL"]["join"] and omj["FR"]["own"] > omj["FR"]["join"]
    res["branches"] = {"B1_density_explains_own_marks": {"fires": bool(b1), "TD_own": td_own, "threshold": round(GATES["RETRIEVED-BELIEVED"] - TOL, 4)},
                       "B2_lookup_reads_tag_route": {"fires": bool(b2_hits), "hits": b2_hits},
                       "B3_monitor_reads_more": {"fires": not b1 and not b2_hits},
                       "reach_explains_the_rise": {"fires": bool(reach), "TL_join": omj["TL"]["join"], "TL_own": omj["TL"]["own"], "FR_join": omj["FR"]["join"], "FR_own": omj["FR"]["own"],
                                                   "forbidding_records_in_view_tagged": {"own": res["gates"]["forbidding_records_in_view"]["tagged_own"], "join": res["gates"]["forbidding_records_in_view"]["tagged_join"], "of": res["gates"]["forbidding_records_in_view"]["in_view"]},
                                                   "wording": ("Section 6 explains the rise from 0.69 to 0.81 under the store's own marks as the marks' reach of the forbidding records (70 of the 99 in view tagged non-active, against 60 under the join), not their density."
                                                               if reach else "Section 6 states the rise from 0.69 to 0.81 under the store's own marks as unexplained: neither the tagged-name lookup nor the forbidding-record indicator is higher under the marks.")}}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=1, sort_keys=True, default=float); f.write("\n")

    print("A2 tag baselines -- gates:", res["gates"])
    print("tag census:", json.dumps(res["tag_census"]))
    print("\nmonitors (whole; SUP / RET / EXP):")
    for name, m in res["monitors"].items():
        print(f"  {name:20s} {m['whole']:.4f}  {m['per_state']['SUPERSESSION']:.4f} / {m['per_state']['RETRACTION']:.4f} / {m['per_state']['EXPIRY']:.4f}")
    for src in ("join", "own", "lookup"):
        print(f"\n[{src}] baseline: whole  SUP / RET / EXP   item CI   persona CI   distinct")
        for name, row in res["baselines"][src].items():
            w = row["whole"]; ps = row["per_state"]
            print(f"  {name:24s} {w['auroc']:.4f}  {ps['SUPERSESSION']['auroc']:.4f} / {ps['RETRACTION']['auroc']:.4f} / {ps['EXPIRY']['auroc']:.4f}"
                  f"   [{w['item_ci']['ci_lo']:.4f},{w['item_ci']['ci_hi']:.4f}] [{w['persona_ci']['ci_lo']:.4f},{w['persona_ci']['ci_hi']:.4f}]   {row['distinct_values']}")
            for mname, vm in row["vs_monitor"].items():
                p = vm["whole"]
                print(f"      {mname} ({vm['monitor']}) minus {name} ({vm['baseline']}): {p['delta']:+.4f} item [{p['item_ci']['ci_lo']:+.4f},{p['item_ci']['ci_hi']:+.4f}]"
                      f" persona [{p['persona_ci']['ci_lo']:+.4f},{p['persona_ci']['ci_hi']:+.4f}] both_exclude_zero={p['both_exclude_zero']}"
                      + (f"  ({vm['note']})" if vm["note"] else ""))
    print("\nown minus join (paired):")
    for name, d in res["own_minus_join"].items():
        print(f"  {name}: join {d['join']:.4f} own {d['own']:.4f} delta {d['delta']:+.4f} item [{d['item_ci']['ci_lo']:+.4f},{d['item_ci']['ci_hi']:+.4f}] persona [{d['persona_ci']['ci_lo']:+.4f},{d['persona_ci']['ci_hi']:+.4f}] both_exclude_zero={d['both_exclude_zero']}")
    print("FR item counts:", json.dumps(res["fr_items"]), "| record census:", json.dumps(res["gates"]["forbidding_records_in_view"]))
    print("\nbranches:", json.dumps(res["branches"], indent=1))
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
