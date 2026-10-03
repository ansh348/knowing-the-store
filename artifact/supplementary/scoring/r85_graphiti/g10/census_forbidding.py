"""census_forbidding.py -- R85 Amendment 1, Step 3, section 4 A(ii): the forbidding-record census over the forty g10 graphs. NO API CALL.

Population: the 104 obligations (PRESENT-NEGATIVE items of e1_metamemory/build/items_final.json), each with its pn_members, FR-Bank
record identifiers whose ground-truth state is read from the join (index_v2.true_lifecycle over the persona's own entries), never from
the attack vector. An obligation is RETRACTED if a member is join-retracted, else SUPERSEDED-OR-EXPIRED if a member is join-superseded or
join-expired, else UNFLAGGED (the join marks no member non-active). The amendment expects 78 superseded-or-expired and 26 retracted from
the attack vectors; D-R85-12 records the join's split if it differs, and the join's split is the one used.

Detector: for each superseded-or-expired obligation, the manifest events that mark its members (the supersession event whose old_fact the
record asserts at tau 0.80, cross-guarded; the expiring fact the record anchors at TAU_GOLD, the join's own rule) are transposed onto the
persona's Graphiti edges exactly as census.py does (detector_over at tau 0.80; expiry by coverage of the fact's tokens at tau 0.80).
RECOVERED if any firing edge is non-active under RULE 1 (graphiti_index.derive_state: superseded or expired), STALE_ACTIVE if edges fire
and all are active, EXTRACTION_MISS if none fires. Recall = RECOVERED / the superseded-or-expired count. Precision = the share of
Graphiti's non-active edges, over all forty graphs, that fire on a record the join marks non-active (any join event of the persona:
supersession and contradiction old facts, retraction original facts, expired expiring facts). Both denominators print; the 26
retraction obligations print the marker.

Writes r85_graphiti/g10/census_forbidding_g10.json. Runs under the repository interpreter from the repo root:
  python r85_graphiti/g10/census_forbidding.py
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R85 = HERE.parent
ROOT = R85.parent
sys.path.insert(0, str(R85))
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import census as C  # noqa: E402
from e0_common import MIN_DISCR, MIN_SHARED, TAU_GOLD, cov, load_joins, toks  # noqa: E402
from index_v2 import TAU_HI, detect, true_lifecycle  # noqa: E402

ARM, TAG = "stock", "g10"
ITEMS = ROOT / "e1_metamemory" / "build" / "items_final.json"
OUT = HERE / "census_forbidding_g10.json"
EXPECTED = {"superseded_or_expired": 78, "retracted": 26}   # the attack-vector split, amendment section 3
AV_RETRACTION = {"AV7_selective_forgetting"}


def join_events(J):
    """The join's (kind, old, new) triples for the persona, the facts true_lifecycle marks records by."""
    ev = []
    for sec in ("supersession_events", "contradictions"):
        for rec in (J.y.get(sec) or []):
            if isinstance(rec, dict) and rec.get("old_fact") and rec.get("new_fact"):
                ev.append(("supersession", rec["old_fact"], rec["new_fact"]))
    for rec in (J.y.get("retractions") or []):
        if isinstance(rec, dict) and rec.get("original_fact") and rec.get("retraction"):
            ev.append(("retraction", rec["original_fact"], rec["retraction"]))
    for rec in (J.y.get("expiring_logistics") or []):
        if isinstance(rec, dict) and str(rec.get("status") or "").strip().lower() == "expired" and rec.get("fact"):
            ev.append(("expiry", rec["fact"], None))
    return ev


def marks_record(kind, old, new, J, eid):
    """Does this join event mark record eid non-active, by true_lifecycle's own rule?"""
    if kind in ("supersession", "retraction"):
        d = detect(old, new, {eid: J.etoks[eid]}, J.drop)
        return bool(d) and d.get(eid, 0.0) >= TAU_HI
    ft = toks(old, J.drop)
    t = J.etoks[eid]
    return len(ft) >= MIN_DISCR and len(ft & t) >= MIN_SHARED and cov(ft, t) >= TAU_GOLD


def fires_on_edges(kind, old, new, J, edges):
    """{edge uuid: signal} at tau 0.80, the detector transposed onto edge facts as census.py does."""
    if kind in ("supersession", "retraction"):
        d = C.detector_over(edges, old, new, J.drop)
        return {u: s for u, s in (d or {}).items() if s >= C.TAU_HI}
    ft = toks(old, J.drop)
    if len(ft) < MIN_DISCR:
        return {}
    out = {}
    for e in edges:
        t = toks(e["fact"], J.drop)
        if len(ft & t) >= MIN_SHARED and cov(ft, t) >= C.TAU_HI:
            out[e["uuid"]] = cov(ft, t)
    return out


def main():
    items = [i for i in json.loads(ITEMS.read_text(encoding="utf-8")) if i.get("label", i["label_pre"]) == "PRESENT-NEGATIVE"]
    assert len(items) == 104, len(items)
    joins = load_joins()
    per_persona = {}
    split = collections.Counter()
    av_split = collections.Counter()
    obligations = []
    buckets = collections.Counter()
    bands = collections.Counter()
    prec_num = prec_den = 0
    edge_cache = {}
    for it in items:
        p = it["persona"]
        J = joins[p]
        if p not in per_persona:
            sup, ret, exp, _ = true_lifecycle(J, J.etoks)
            per_persona[p] = {"superseded": sup, "retracted": ret, "expired": exp, "events": join_events(J)}
        st = per_persona[p]
        members = it["pn_members"]
        if any(m in st["retracted"] for m in members):
            state = "retracted"
        elif any(m in st["superseded"] or m in st["expired"] for m in members):
            state = "superseded_or_expired"
        else:
            state = "unflagged"
        split[state] += 1
        av_split["retracted" if it["attack_vector"] in AV_RETRACTION else "superseded_or_expired"] += 1
        row = {"item_id": it["item_id"], "persona": p, "attack_vector": it["attack_vector"], "members": members, "join_state": state}
        if state == "superseded_or_expired":
            if p not in edge_cache:
                edge_cache[p] = C.read_edges(f"r85{ARM}_{p}_{TAG}")
            edges = edge_cache[p]
            states = C.derive(edges)
            marked = [m for m in members if m in st["superseded"] or m in st["expired"]]
            evs = [(k, o, n) for (k, o, n) in st["events"] if k != "retraction" and any(marks_record(k, o, n, J, m) for m in marked)]
            fired = {}
            for k, o, n in evs:
                fired.update(fires_on_edges(k, o, n, J, edges))
            if not fired:
                b = "EXTRACTION_MISS"
            elif any(states[u] != "active" for u in fired):
                b = "RECOVERED"
            else:
                b = "STALE_ACTIVE"
            buckets[b] += 1
            for band in (0.50, 0.75, 0.80):
                f = {}
                for k, o, n in evs:
                    if k == "expiry":
                        ft = toks(o, J.drop)
                        f.update({e["uuid"]: 1 for e in edges if len(ft & toks(e["fact"], J.drop)) >= MIN_SHARED and cov(ft, toks(e["fact"], J.drop)) >= band})
                    else:
                        d = C.detector_over(edges, o, n, J.drop) or {}
                        f.update({u: 1 for u, s in d.items() if s >= band})
                if f and any(states[u] != "active" for u in f):
                    bands[band] += 1
            row.update({"bucket": b, "marking_events": len(evs), "firing_edges": len(fired),
                        "firing_non_active": sum(1 for u in fired if states[u] != "active")})
        elif state == "retracted":
            row["bucket"] = "INEXPRESSIBLE (marker)"
        else:
            row["bucket"] = "UNFLAGGED (no member marked by the join)"
        obligations.append(row)

    # ---- precision over all forty graphs: non-active edges (RULE 1) that fire on a record the join marks non-active
    prec_detail = {}
    for p, J in joins.items():
        if p not in edge_cache:
            edge_cache[p] = C.read_edges(f"r85{ARM}_{p}_{TAG}")
        edges = edge_cache[p]
        states = C.derive(edges)
        st = per_persona.get(p) or {"events": join_events(J)}
        fired = set()
        for k, o, n in st["events"]:
            fired |= set(fires_on_edges(k, o, n, J, edges))
        non_active = {e["uuid"] for e in edges if states[e["uuid"]] != "active"}
        prec_detail[p] = {"non_active_edges": len(non_active), "firing_non_active": len(non_active & fired), "join_events": len(st["events"])}
        prec_num += len(non_active & fired)
        prec_den += len(non_active)

    n_soe = split["superseded_or_expired"]
    out = {
        "population": 104,
        "join_split": dict(split), "attack_vector_split": dict(av_split), "expected_split": EXPECTED,
        "D-R85-12": "join split equals the attack-vector split" if dict(split) == EXPECTED else
                    "join split differs from the attack-vector split; the join's split is used (D-R85-12)",
        "buckets": dict(buckets),
        "recall": round(buckets["RECOVERED"] / n_soe, 4) if n_soe else None,
        "recall_denominator": n_soe,
        "recall_denominator_attack_vector": EXPECTED["superseded_or_expired"],
        "recall_over_attack_vector_78": round(buckets["RECOVERED"] / EXPECTED["superseded_or_expired"], 4),
        "recall_by_band": {str(k): [v, n_soe] for k, v in sorted(bands.items())},
        "precision": round(prec_num / prec_den, 4) if prec_den else None,
        "precision_numerator": prec_num, "precision_denominator": prec_den,
        "retraction": "INEXPRESSIBLE (marker) on every Graphiti row",
        "per_persona_precision": prec_detail,
        "obligations": obligations,
    }
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"population 104; join split {dict(split)}; attack-vector split {dict(av_split)}; expected {EXPECTED}")
    print(f"  {out['D-R85-12']}")
    print(f"buckets over the {n_soe} join superseded-or-expired obligations: {dict(buckets)}")
    print(f"recall = {buckets['RECOVERED']}/{n_soe} = {out['recall']}   (over the attack-vector 78: {out['recall_over_attack_vector_78']})")
    print(f"recall by band: {out['recall_by_band']}")
    print(f"precision = {prec_num}/{prec_den} = {out['precision']}   (non-active edges under RULE 1 that fire on a join-marked record, forty graphs)")
    print(f"-> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
