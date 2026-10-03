# -*- coding: utf-8 -*-
"""r129_b9.py -- R129 (2026-09-20), the author's ruling A2 on R128's B9 (the inverted tag from the join's missing negation handling):
what changes in Appendix E.10's counts if the tag on `frbank:fatima:fatima_q06` is corrected, read from the downstream audit's artifacts
(reviews/downstream_audit/step4b_view_lines.json, rows_master.jsonl; AUX-DS-AUDIT-SOURCE) without re-answering anything.

As joined: of the 89 scorable obligations the ORACLE view holds an active line asserting the stale value for 35 (21 supersession, 14 retraction);
the stale answers under ORACLE split by that line 16 / 0 (GPT-4.1 mini, D.4: stale with such a line / stale without) and 14 / 5 (Haiku 4.5, D.4).
Corrected: the retraction statement becomes the active record and the plan records retracted, so the FULL view of that question holds no active
line asserting the stale value (its SLOT-ABLATED view already holds none); the 35 read 34, the retraction count 13, and each answerer's stale
answer on that view (both answered from the plan lines the view showed as active) moves to the 'without' cell. The scored tables are unchanged.
Writes reviews/v22/results/r129_b9.json. Usage: python reviews/v22/tools/r129_b9.py
"""
from __future__ import annotations

import collections
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
for p in ("reviews/v22/tools", "e1_metamemory/tools", "e3_metamemory/tools", "ds_downstream/tools", "r82_counterfactual/tools", "reviews/v19/tools", "reviews/v21/tools"):
    sys.path.insert(0, str(ROOT / p))
from ds_common import load_cell  # noqa: E402

AUD = ROOT / "reviews" / "downstream_audit"
OUT = ROOT / "reviews" / "v22" / "results" / "r129_b9.json"
ITEM = "frbank:fatima:fatima_q06"
LANES = {"mini-D4": "GPT-4.1 mini", "h45-D4": "Haiku 4.5"}


def main():
    items = {it["item_id"]: it for it in load_cell()}
    vl = json.load(io.open(AUD / "step4b_view_lines.json", encoding="utf-8"))
    orc = {k.split("|")[0]: v for k, v in vl["view_lines"].items() if k.endswith("|ORACLE")}
    assert len(orc) == 89 and vl["oracle_summary"]["n_scorable"] == 89
    state = {i: items[i]["state"] for i in orc}
    by_state = collections.Counter(state.values()); assert by_state == {"sup": 63, "ret": 26}, by_state
    active = {i: v["any_active_stale"] for i, v in orc.items()}
    assert sum(active.values()) == 35
    joined = collections.Counter(state[i] for i in orc if active[i]); assert joined == {"sup": 21, "ret": 14}, joined
    variants = {i: orc[i] for i in orc if i.startswith(ITEM)}
    assert set(variants) == {f"{ITEM}:FULL", f"{ITEM}:SLOT-ABLATED"}, set(variants)
    assert variants[f"{ITEM}:FULL"]["any_active_stale"] and not variants[f"{ITEM}:SLOT-ABLATED"]["any_active_stale"]
    corrected_active = dict(active); corrected_active[f"{ITEM}:FULL"] = False
    corrected = collections.Counter(state[i] for i in orc if corrected_active[i])
    rows = [json.loads(l) for l in io.open(AUD / "rows_master.jsonl", encoding="utf-8")]
    split = {}
    for lane, name in LANES.items():
        rs = [r for r in rows if r["lane"] == lane and "ORACLE" in r["policies"] and r["item_id"] in orc]
        assert len(rs) == 85, (lane, len(rs))                      # the oracle's reached scorable obligations (tab:ds-body)
        def cells(act):
            c = collections.Counter((r["registered"]["stale_use_tau_gold"], act[r["item_id"]]) for r in rs)
            return {"stale_with_active_stale_line": c[(True, True)], "stale_without": c[(True, False)],
                    "not_stale_with": c[(False, True)], "not_stale_without": c[(False, False)]}
        f = [r for r in rs if r["item_id"] == f"{ITEM}:FULL"]; assert len(f) == 1
        split[name] = {"lane": lane, "as_joined": cells(active), "corrected": cells(corrected_active),
                       "stale_on_the_corrected_view": bool(f[0]["registered"]["stale_use_tau_gold"]), "answer_head": f[0]["answer"][:160]}
    assert split["GPT-4.1 mini"]["as_joined"] == {"stale_with_active_stale_line": 16, "stale_without": 0, "not_stale_with": 19, "not_stale_without": 50}
    assert split["Haiku 4.5"]["as_joined"] == {"stale_with_active_stale_line": 14, "stale_without": 5, "not_stale_with": 21, "not_stale_without": 45}
    res = {"item": ITEM, "scorable": 89, "by_state": dict(by_state),
           "views_with_active_stale_line": {"as_joined": {"total": 35, **dict(joined)}, "corrected": {"total": sum(corrected.values()), **dict(corrected)}},
           "variants": {k: {"active_stale_lines": v["active_stale"], "tagged_stale_lines": v["tagged_stale"], "in_the_35": v["any_active_stale"]} for k, v in variants.items()},
           "oracle_split": split, "scored_tables": "unchanged: every answer-stage table was scored with the tag as joined"}
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(res["views_with_active_stale_line"]))
    for name, s in split.items():
        print(name, "as joined", s["as_joined"], "corrected", s["corrected"], "stale on that view:", s["stale_on_the_corrected_view"])
    print("->", OUT)


if __name__ == "__main__":
    main()
