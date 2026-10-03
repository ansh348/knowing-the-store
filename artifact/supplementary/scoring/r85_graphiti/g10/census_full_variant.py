"""census_full_variant.py -- the forbidding-record census of Step 3 re-aggregated on the FULL store variant (D-R85-16; 2026-09-16). NO API CALL.

The 104 obligations of census_forbidding.py are 47 questions under up to three FR-Bank store variants (FULL, CAT-ABLATED, SLOT-ABLATED),
while every Graphiti graph is one store per persona ingested from the whole bank, so the variant rows repeat the FULL sibling's forbidding
records on the same graph (48 of the 57 non-FULL rows carry the FULL sibling's pn_members exactly). This script reads the recorded
per-obligation rows of census_forbidding_g10.json (nothing is re-detected) and re-aggregates them (i) on the 47 FULL-variant obligations and
(ii) on the distinct (persona, member-set) pairs, printing the registered 104-row figures beside both. Precision is over edges and does not
change. Writes r85_graphiti/g10/census_full_variant_g10.json. Runs from the repo root: python r85_graphiti/g10/census_full_variant.py
"""
from __future__ import annotations

import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "census_forbidding_g10.json"
OUT = HERE / "census_full_variant_g10.json"


def agg(rows):
    se = [o for o in rows if o["join_state"] == "superseded_or_expired"]
    b = collections.Counter(o["bucket"] for o in se)
    rec = b.get("RECOVERED", 0)
    by_av = {}
    for av in sorted({o["attack_vector"] for o in se}):
        sub = [o for o in se if o["attack_vector"] == av]; bb = collections.Counter(o["bucket"] for o in sub)
        by_av[av] = {"n": len(sub), "RECOVERED": bb.get("RECOVERED", 0), "STALE_ACTIVE": bb.get("STALE_ACTIVE", 0), "EXTRACTION_MISS": bb.get("EXTRACTION_MISS", 0),
                     "recall": round(bb.get("RECOVERED", 0) / len(sub), 4) if sub else None}
    return {"obligations": len(rows), "join_split": dict(collections.Counter(o["join_state"] for o in rows)),
            "superseded_or_expired": len(se), "RECOVERED": rec, "STALE_ACTIVE": b.get("STALE_ACTIVE", 0), "EXTRACTION_MISS": b.get("EXTRACTION_MISS", 0),
            "recall": round(rec / len(se), 4) if se else None, "by_attack_vector": by_av}


def main():
    c = json.loads(SRC.read_text(encoding="utf-8"))
    rows = c["obligations"]
    assert len(rows) == 104
    full = [o for o in rows if o["item_id"].endswith(":FULL")]
    assert len(full) == 47, len(full)
    # distinct (persona, member-set): buckets must agree across the variants that share a member set (asserted)
    seen = collections.OrderedDict()
    disagree = 0
    for o in rows:
        k = (o["persona"], tuple(sorted(o["members"])))
        if k in seen:
            if seen[k]["join_state"] != o["join_state"] or seen[k].get("bucket") != o.get("bucket"):
                disagree += 1
            continue
        seen[k] = o
    non_full = [o for o in rows if not o["item_id"].endswith(":FULL")]
    full_by_q = {(o["persona"], o["item_id"].split(":")[2]): tuple(sorted(o["members"])) for o in full}
    same = sum(1 for o in non_full if full_by_q.get((o["persona"], o["item_id"].split(":")[2])) == tuple(sorted(o["members"])))
    out = {"source": str(SRC.name), "registered_104_rows": agg(rows), "full_variant_47": agg(full), "distinct_member_sets": agg(list(seen.values())),
           "non_full_rows": len(non_full), "non_full_rows_repeating_the_full_siblings_members": same, "member_set_bucket_disagreements": disagree,
           "precision": {"numerator": c["precision_numerator"], "denominator": c["precision_denominator"], "value": c["precision"], "note": "over edges; unchanged by the re-aggregation"},
           "note": "D-R85-16: the graph is the FULL store for every item; the FULL-variant reading is the one the main text prints, the registered 104-row reading and its P1 verdict print beside it"}
    OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k in ("registered_104_rows", "full_variant_47", "distinct_member_sets"):
        a = out[k]
        print(f"{k:24s} obligations {a['obligations']:3d}  split {a['join_split']}  sup/exp {a['superseded_or_expired']:3d}  RECOVERED {a['RECOVERED']:2d}  STALE_ACTIVE {a['STALE_ACTIVE']:2d}  EXTRACTION_MISS {a['EXTRACTION_MISS']:2d}  recall {a['recall']}")
        for av, d in a["by_attack_vector"].items():
            print(f"    {av:28s} n {d['n']:2d}  {d['RECOVERED']}/{d['STALE_ACTIVE']}/{d['EXTRACTION_MISS']}  recall {d['recall']}")
    print(f"non-FULL rows {out['non_full_rows']}, repeating the FULL sibling's members {same}; bucket disagreements across shared member sets {disagree}")
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
