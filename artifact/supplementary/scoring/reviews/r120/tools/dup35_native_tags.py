# -*- coding: utf-8 -*-
"""dup35_native_tags.py -- program R120, item k (read-only, no model call): for the 35 audited duplicate items of the downstream
experiment and their active-stale line instances, FR-Bank's native lifecycle tag (the store's own marks, amend1_resp.believed_flags)
beside the alignment-derived tag (the ground-truth flags of resp_common.true_flags, the tag the recorded ground-truth views carry).
An "untagged-by-alignment duplicate" is a view line the audit (reviews/downstream_audit/step4b_view_lines.json, step 4b) marks
active_stale: its ground-truth tag is active while its text asserts the item's stale value under the committed detector
(shared tokens >= MIN_SHARED, cross guard, coverage >= TAU_GOLD). The views are rebuilt by amend8_propagate.build_views() (the E4
lock's enumeration, 452 views), so the instance count reproduces AUX-DS-A8-DIAGNOSIS's 272.
Writes reviews/r120/results/dup35_native_tags.json and the 35-row sheet reviews/r120/DUP35_NATIVE_TAGS.md."""
from __future__ import annotations

import collections
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "ds_downstream" / "tools"))
import amend8_propagate as M                                                 # noqa: E402  (imports the DS stack; no call is made)
from resp_common import lifecycle_tag, true_flags                            # noqa: E402
import amend1_resp as AR                                                     # noqa: E402
from e0_common import toks, cov, MIN_SHARED, CROSS_GUARD, TAU_GOLD           # noqa: E402  (the committed detector's constants)

OUT_JSON = ROOT / "reviews" / "r120" / "results" / "dup35_native_tags.json"
OUT_MD = ROOT / "reviews" / "r120" / "DUP35_NATIVE_TAGS.md"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sub, out, census, dup, fp, jobs, n_gt_lock = M.build_views()
    audit = M.J(M.AUDIT)["view_lines"]
    tf = true_flags(); bf = AR.believed_flags(); rec = M.RD.records(sub); byid = {it["item_id"]: it for it in sub}
    inst = []                                    # one row per active-stale line instance (view x policy x rank)
    for key, e in out.items():
        per = e["persona"]; ids = e["ids"]
        lines = M.parse(e["sources"]["gt"]["before_view"]); own_lines = M.parse(e["sources"]["own"]["before_view"])
        for pol in e["policies"]:
            ref = audit.get(f"{e['item_id']}|{pol}")
            if not ref or not ref["active_stale"]:
                continue
            for r in ref["active_stale"]:
                l = lines[r - 1]; assert l["rank"] == r
                eid = ids[r - 1]
                gt_tag = lifecycle_tag(tf[per][eid]); own_tag = lifecycle_tag(bf[per][eid])
                assert l["tag"] == gt_tag == "active", (key, pol, r, l["tag"], gt_tag)
                assert own_lines[r - 1]["tag"] == own_tag
                rc = rec.get(e["item_id"]) or {}; drop = rc.get("drop", frozenset())
                ot, nt = toks(rc.get("stale_field") or "", drop), toks(rc.get("gold_field") or "", drop); do, dn = ot - nt, nt - ot; A = toks(l["text"], drop)
                det = {"shared_stale_only": len(do & A), "cov_stale_only": round(cov(do, A), 2), "cov_successor_only": round(cov(dn, A), 2),
                       "fires": bool(len(do & A) >= MIN_SHARED and cov(dn, A) < CROSS_GUARD and cov(do, A) >= TAU_GOLD)}
                assert det["fires"], (key, pol, r, det)
                inst.append({"item_id": e["item_id"], "persona": per, "policy": pol, "job_key": key, "rank": r, "entry_id": eid, "attribute": l["attribute"], "category": l["category"],
                             "age": l["age_s"], "text": l["text"], "alignment_tag": gt_tag, "native_tag": own_tag, "asserts_stale_value_detector": det,
                             "native_flags": {k: bool(bf[per][eid][k]) for k in ("superseded", "retracted", "expired")}})
    n_inst = len(inst); items = sorted({x["item_id"] for x in inst})
    assert len(items) == 35, len(items)
    # unique lines (item, entry) and their native state
    uniq = {}
    for x in inst:
        uniq.setdefault((x["item_id"], x["entry_id"]), x)
    by_native_inst = collections.Counter(x["native_tag"] for x in inst)
    by_native_uniq = collections.Counter(x["native_tag"] for x in uniq.values())
    items_all_active = sum(1 for it in items if all(u["native_tag"] == "active" for (i, _), u in uniq.items() if i == it))
    items_any_nonactive = sum(1 for it in items if any(u["native_tag"] != "active" for (i, _), u in uniq.items() if i == it))
    res = {"instances": n_inst, "unique_lines": len(uniq), "items": len(items), "gt_lock_lines": n_gt_lock,
           "native_state_by_instance": dict(by_native_inst), "native_state_by_unique_line": dict(by_native_uniq),
           "items_every_duplicate_active_natively": items_all_active, "items_with_a_duplicate_non_active_natively": items_any_nonactive,
           "rows": inst}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT_JSON, "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    # the 35-row sheet
    L = ["# DUP35_NATIVE_TAGS — the 35 audited duplicate items: FR-Bank's native tag beside the alignment-derived tag (R120 item k; read-only, no call)\n",
         f"Source: `reviews/r120/tools/dup35_native_tags.py` on the recorded views (amend8_propagate.build_views, {len(out)} views, ground-truth tag lock {n_gt_lock} lines), the audit `step4b_view_lines.json` (active_stale ranks: lines whose text asserts the item's stale value under the committed detector while the ground-truth tag is active), the store's own marks (`amend1_resp.believed_flags`: believed_superseded, believed_retracted, event time before the cutoff) and the ground-truth flags (`resp_common.true_flags`). Instances = view × policy × line; unique lines = distinct (item, entry).\n",
         f"**Counts.** {n_inst} active-stale line instances (AUX-DS-A8-DIAGNOSIS: 272) over {len(uniq)} unique lines in {len(items)} items. Native state of the untagged-by-alignment duplicates: by instance {dict(by_native_inst)}; by unique line {dict(by_native_uniq)}. Items whose every duplicate is active natively: {items_all_active}; items with at least one duplicate already non-active natively: {items_any_nonactive}.\n",
         "| # | item | persona | state | stale field (record) | gold field (record) | duplicate line(s): rank@policies · attribute · text | native state | alignment state | asserts the stale value (the detector's verdict; the author reads the text) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for n, it in enumerate(items, 1):
        item = byid[it]; rc = rec.get(it) or {}
        rows = [u for (i, _), u in uniq.items() if i == it]
        pol_of = collections.defaultdict(set)
        for x in inst:
            if x["item_id"] == it:
                pol_of[x["entry_id"]].add(f"{x['rank']}@{x['policy']}")
        cells = "<br>".join(f"{', '.join(sorted(pol_of[u['entry_id']]))} · {u['attribute']} · {u['text']}" for u in rows)
        nat = "<br>".join(u["native_tag"] for u in rows); ali = "<br>".join(u["alignment_tag"] for u in rows); ass = "<br>".join(f"detector fires: {u['asserts_stale_value_detector']['shared_stale_only']} shared stale-only tokens, coverage {u['asserts_stale_value_detector']['cov_stale_only']:.2f} (successor {u['asserts_stale_value_detector']['cov_successor_only']:.2f})" for u in rows)
        L.append(f"| {n} | `{it}` | {item['persona']} | {item['state']} | {str(rc.get('stale_field'))[:160]} | {str(rc.get('gold_field'))[:160]} | {cells} | {nat} | {ali} | {ass} |")
    io.open(OUT_MD, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
    print("->", OUT_MD)


if __name__ == "__main__":
    main()
