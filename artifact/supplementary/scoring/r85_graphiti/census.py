"""census.py -- R85 Phase 1. Read Graphiti's graph, build its index, census it. NO API CALLS.

Applies the rules frozen in graphiti_index.py to the graph an ingest run produced, then
censuses that self-description against the persona manifest using the study's OWN detector,
so the Graphiti row is comparable with the FR-Bank, Mem0 and A-MEM rows of Table 21.

The detector is e0_common.PersonaJoin.detector transposed onto Graphiti edge facts:
tokens unique to the superseded value must be shared at MIN_SHARED, the superseding value
must not be asserted at CROSS_GUARD, and a fire is coverage >= 0.80, which is the same
tau_hi the published census uses.

Each manifest supersession event lands in exactly one bucket:

  RECOVERED       an edge asserting the old value exists AND carries invalid_at.
  STALE_ACTIVE    an edge asserting the old value exists and was never invalidated.
                  This is the erase/overstate signal: the backend kept a dead fact live.
  EXTRACTION_MISS no edge asserts the old value at all. The extractor lost it before
                  lifecycle could apply, which is a different failure and is counted apart.

Usage:
  python r85_graphiti/census.py --persona elena --arm stock --model gpt-4.1-mini-2025-04-14
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))

import graphiti_index as G  # noqa: E402
from e0_common import (CROSS_GUARD, MIN_DISCR, MIN_SHARED, cov, load_joins,  # noqa: E402
                       parse_dt, toks)

TAU_HI = 0.80
NEO4J_URI = "bolt://localhost:7688"
NEO4J_AUTH = ("neo4j", "r85graphiti2026")

EDGE_QUERY = """
MATCH (n:Entity)-[e:RELATES_TO]->(m:Entity)
WHERE e.group_id = $g
RETURN e.uuid AS uuid, e.name AS name, e.fact AS fact,
       e.created_at AS created_at, e.valid_at AS valid_at,
       e.invalid_at AS invalid_at, e.expired_at AS expired_at,
       n.uuid AS src_uuid, n.name AS src_name, labels(n) AS src_labels,
       m.uuid AS tgt_uuid, m.name AS tgt_name, labels(m) AS tgt_labels
"""


def read_edges(group_id):
    from neo4j import GraphDatabase
    with GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH) as d:
        with d.session() as s:
            return [dict(r) for r in s.run(EDGE_QUERY, g=group_id)]


def slot_of(e):
    """The (subject, predicate) slot an edge occupies."""
    return (e["src_uuid"], e["name"])


def label_of(e):
    labs = [x for x in (e.get("tgt_labels") or []) if x != "Entity"]
    return labs[0] if labs else "entity"


def derive(edges):
    """Apply RULE 1 to every edge, using a later-edge-on-the-slot test."""
    by_slot = collections.defaultdict(list)
    for e in edges:
        by_slot[slot_of(e)].append(e)
    for v in by_slot.values():
        v.sort(key=lambda e: (parse_dt(e["valid_at"]) or parse_dt(e["created_at"])
                              or parse_dt("1970-01-01T00:00:00+00:00")))
    states = {}
    for e in edges:
        peers = by_slot[slot_of(e)]
        mine = parse_dt(e["valid_at"]) or parse_dt(e["created_at"])
        later = any((parse_dt(p["valid_at"]) or parse_dt(p["created_at"])) > mine
                    for p in peers if p["uuid"] != e["uuid"] and mine)
        states[e["uuid"]] = G.derive_state(e, later)
    return states


def detector_over(edges, old_fact, new_fact, drop):
    """e0_common.PersonaJoin.detector, transposed onto Graphiti edge facts."""
    ot, nt = toks(old_fact, drop), toks(new_fact, drop)
    do, dn = ot - nt, nt - ot
    if len(do) < MIN_DISCR or len(dn) < MIN_DISCR:
        return None
    out = {}
    for e in edges:
        t = toks(e["fact"], drop)
        if len(do & t) >= MIN_SHARED and cov(dn, t) < CROSS_GUARD:
            out[e["uuid"]] = cov(do, t)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--persona", required=True)
    ap.add_argument("--arm", default="stock")
    ap.add_argument("--model", required=True)
    ap.add_argument("--group-tag", default="", dest="group_tag")
    a = ap.parse_args()

    group_id = f"r85{a.arm}_{a.persona}" + (f"_{a.group_tag}" if a.group_tag else "")
    edges = read_edges(group_id)
    J = load_joins()[a.persona]
    states = derive(edges)
    by_uuid = {e["uuid"]: e for e in edges}

    # ---------------------------------------------------------------- the index
    t_now = J.t_now
    rows = []
    for e in edges:
        st = states[e["uuid"]]
        # D-R85-10. The recency mapping was not covered by the frozen rules, and the dump
        # shows why it needs one: Graphiti's `created_at` is TRANSACTION time, the wall
        # clock at ingestion, so every edge would read as zero days old and the axis would
        # describe the run rather than the store. `valid_at` is the semantic analogue of
        # FR-Bank's `recency_time`, which is the record's own session date. Age is taken
        # against valid_at, falling back to created_at where the extractor left it null.
        d = parse_dt(e["valid_at"]) or parse_dt(e["created_at"])
        age = max((t_now - d).days, 0) if (d and t_now) else None
        rows.append({
            "id": e["uuid"], "category": None,
            "slot": G.attribute_name(e["name"], label_of(e)),
            "age": age,
            "active": st == "active", "superseded": st == "superseded",
            "retracted": None, "expired": st == "expired",
        })
    sup_events_idx = [{e["uuid"]} for e in edges if e["invalid_at"]]
    text, blocks, names = G.build_index(rows, sup_events_idx)

    # ------------------------------------------------------------- the census
    buckets, detail = collections.Counter(), []
    bands = collections.Counter()
    explained = set()
    for rec in (J.y.get("supersession_events") or []):
        if not isinstance(rec, dict):
            continue
        d = detector_over(edges, rec.get("old_fact"), rec.get("new_fact"), J.drop)
        if d is None:
            continue  # not resolvable; excluded from the denominator, as published
        fires = {u for u, s in d.items() if s >= TAU_HI}
        if not fires:
            bucket = "EXTRACTION_MISS"
        elif any(by_uuid[u]["invalid_at"] for u in fires):
            bucket = "RECOVERED"
            explained |= {u for u in fires if by_uuid[u]["invalid_at"]}
        else:
            bucket = "STALE_ACTIVE"
        buckets[bucket] += 1
        # Coverage BANDS, the convention believed_frbank.py already uses for this census.
        # The frozen bar is TAU_HI and is not moved; the lower bands show how close the
        # verdict sits to it, because a bucket boundary at 0.80 can turn an edge Graphiti
        # did invalidate into an apparent miss.
        for band in (0.50, 0.75, TAU_HI):
            f = {u for u, s in d.items() if s >= band}
            if f and any(by_uuid[u]["invalid_at"] for u in f):
                bands[band] += 1
        detail.append({"slot": rec.get("slot"), "bucket": bucket,
                       "fires": len(fires), "best": round(max(d.values()), 3) if d else 0.0,
                       "old_session": rec.get("old_session"),
                       "new_session": rec.get("new_session")})

    # ---------------------------------------- entity-level extraction audit
    # Against the MANIFEST, not against FR-Bank's records: a manifest fact counts as
    # extracted when some Graphiti edge asserts it at the same tau_hi the census uses.
    # This separates "the extractor lost the fact" from "lifecycle was not applied".
    edge_toks = [(e["uuid"], toks(e["fact"], J.drop)) for e in edges]
    fact_sources = []
    for rec in (J.y.get("stable_identity") or []):
        fact_sources.append(("stable_identity", rec.get("fact")))
    for rec in (J.y.get("supersession_events") or []):
        fact_sources += [("supersession_old", rec.get("old_fact")),
                         ("supersession_new", rec.get("new_fact"))]
    for rec in (J.y.get("retractions") or []):
        fact_sources.append(("retraction_original", rec.get("original_fact")))
    for rec in (J.y.get("expiring_logistics") or []):
        fact_sources.append(("expiring", rec.get("fact")))
    ext = collections.Counter()
    ext_detail = collections.defaultdict(lambda: [0, 0])
    for kind, fact in fact_sources:
        if not isinstance(fact, str) or not fact.strip():
            continue
        ft = toks(fact, J.drop)
        if len(ft) < MIN_DISCR:
            continue
        best = max((cov(ft, et) for _, et in edge_toks if len(ft & et) >= MIN_SHARED),
                   default=0.0)
        hit = best >= TAU_HI
        ext["extracted" if hit else "lost"] += 1
        ext_detail[kind][0] += int(hit)
        ext_detail[kind][1] += 1

    denom = sum(buckets.values())
    recovered = buckets["RECOVERED"]
    believed_sup = [e for e in edges if e["invalid_at"]]
    # Entity fragmentation: how many distinct subject nodes stand for the one user.
    user_like = sorted({e["src_name"] for e in edges
                        if str(e["src_name"]).strip().lower() in
                        ("i", "user", "the user", "speaker", "the speaker", "me")})
    # Temporal incoherence: an edge invalidated before it became valid.
    incoherent = sum(1 for e in edges
                     if e["invalid_at"] and e["valid_at"]
                     and parse_dt(e["invalid_at"]) < parse_dt(e["valid_at"]))
    out = {
        "persona": a.persona, "arm": a.arm, "model": a.model, "group_id": group_id,
        "edges": len(edges),
        "states": dict(collections.Counter(states.values())),
        "manifest_supersession_events": denom,
        "buckets": dict(buckets),
        "supersession_recall": round(recovered / denom, 4) if denom else None,
        "supersession_precision": round(len(explained) / len(believed_sup), 4) if believed_sup else None,
        "believed_superseded_edges": len(believed_sup),
        "retraction": "INEXPRESSIBLE (marker)",
        "recall_by_band": {str(k): [v, denom] for k, v in sorted(bands.items())},
        "user_entity_nodes": user_like,
        "edges_invalid_before_valid": incoherent,
        "manifest_facts": sum(ext.values()),
        "manifest_facts_extracted": ext["extracted"],
        "manifest_fact_recall": round(ext["extracted"] / sum(ext.values()), 4) if ext else None,
        "manifest_fact_recall_by_kind": {k: [v[0], v[1]] for k, v in sorted(ext_detail.items())},
        "distinct_attribute_names": len(set(r["slot"] for r in rows)),
        "distinct_relation_types": len(set(e["name"] for e in edges)),
        "distinct_target_labels": sorted(set(label_of(e) for e in edges))[:12],
        # The index's superseded section follows the DERIVED state (RULE 1), which needs a
        # later edge on the slot as well as invalid_at. The invalid_at-flagged set is
        # reported beside it, because their difference is itself a census quantity: an edge
        # invalidated with no successor on its slot is expiry, not supersession.
        "superseded_names": sorted({rows[i]["slot"] for i, e in enumerate(edges)
                                    if states[e["uuid"]] == "superseded"}),
        "invalidated_names": sorted({rows[i]["slot"] for i, e in enumerate(edges)
                                     if e["invalid_at"]}),
        "valid_at_null_edges": sum(1 for e in edges if not e["valid_at"]),
        "detail": detail,
    }
    d = HERE / "census_runs"
    d.mkdir(exist_ok=True)
    tag = f"{a.arm}_{a.model}_{a.persona}"
    (d / f"{tag}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    (d / f"{tag}.index.txt").write_text(text, encoding="utf-8")

    print(f"=== {tag} ===")
    print(f"edges={len(edges)}  states={out['states']}")
    print(f"manifest supersession events={denom}  buckets={dict(buckets)}")
    print(f"supersession recall={out['supersession_recall']}  "
          f"precision={out['supersession_precision']}")
    print(f"recall by coverage band (frozen bar is {TAU_HI}): {out['recall_by_band']}")
    print(f"user split across entity nodes: {user_like}")
    print(f"edges invalidated before they became valid: {incoherent}")
    print(f"manifest facts extracted={out['manifest_facts_extracted']}/{out['manifest_facts']} "
          f"(recall={out['manifest_fact_recall']}) by kind={out['manifest_fact_recall_by_kind']}")
    print(f"distinct attribute names={out['distinct_attribute_names']} "
          f"(relation types={out['distinct_relation_types']}, "
          f"target labels={out['distinct_target_labels']})")
    print(f"superseded-names list: {out['superseded_names'][:10]}")
    print("\n--- index ---")
    print(text)


if __name__ == "__main__":
    main()
