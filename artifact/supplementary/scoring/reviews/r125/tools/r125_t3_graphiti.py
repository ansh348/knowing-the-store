# -*- coding: utf-8 -*-
"""r125_t3_graphiti.py -- Task 3, Graphiti: the obligation labels relative to what the graph retains (offline; the graph read from the local
neo4j-r85 container once, exported to reviews/r125/build/graphiti_edges_g10.json, then everything from the export). NO MODEL CALL. $0.

The store S in the scored condition is one Graphiti graph per persona (graphiti-core 0.28.1, stock), built by Graphiti's own extraction from
the 1,365 episodes rendered from FR-Bank's persona banks with every lifecycle field removed; it is the FULL store of every persona, so the
scored population is the 323 FULL-variant items (47 obligations; D-R85-17). The PN labels come from the manifest; the forbidding records are
FR-Bank entry identifiers (pn_members), which the graph does not hold: whether the graph retains the forbidding CONTENT is the census join's
question (the manifest event that marks a member under `index_v2.true_lifecycle`, transposed onto the persona's edges at the overlap bar;
`r85_graphiti/g10/census_forbidding.py`). The recorded buckets at the 0.80 bar (RECOVERED 13 / STALE_ACTIVE 10 / EXTRACTION_MISS 11 on the
34 join-marked superseded-or-expired obligations; 4 join-retracted, inexpressible; 9 unflagged) are reproduced from the export, then the
two bands the census already uses (0.75, 0.50) are computed per obligation:
  retained at a band   = some edge asserts the forbidding content at that overlap (fires), whatever its state;
  recovered at a band  = a firing edge carries a non-active state under RULE 1 (graphiti_index.derive_state);
  stale-active         = fires, every firing edge active;  extraction miss = no edge fires.
For the 4 join-retracted obligations the retraction event's original fact is transposed the same way (retention of the content; the state is
inexpressible on this backend). For the 9 unflagged obligations the join names no marking event, so no census stratum exists; they are printed
as their own stratum.
Re-scoring: every monitor row of tab:graphiti-completed on the 323 (the four summary renderings, the four view lanes, the store's superseded-name
lookup, the whole-map lookup, the recorded FR-Bank ground-truth summary and question-only rows) with the positives restricted to each stratum
and the 276 negatives unchanged: AUROC with both single-arm intervals, the store-written-minus-ground-truth paired difference, n printed.
Gates: G10-BELIEVED 0.5765, G10-LIFTED 0.6511, G10-TRUEPROJ 0.7556, G10-TRUEPROJ-LIFTED 0.6958, TRUE 0.7424, blind 0.4964, NB-6 0.6780, NB-5 0.6994 / 0.7959,
VIEW-UNTAGGED 0.6995, VIEW-TAGGED 0.6854, HYBRID 0.7741, FRB-VIEW-UNTAGGED 0.6991.
Writes reviews/r125/results/r125_t3_graphiti.json (and the edge export under build/).
"""
from __future__ import annotations

import collections
import json
import sys

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r125_common as C  # noqa: E402
from r125_common import auroc, r4  # noqa: E402
for p in ("resp_review/tools", "e0_metamemory/tools", "e1_metamemory/tools", "r85_graphiti", "r85_graphiti/g10"):
    sys.path.insert(0, str(C.ROOT / p))
import resp_common as RC  # noqa: E402
import census as CE  # noqa: E402
from e0_common import MIN_DISCR, MIN_SHARED, cov, load_joins, toks  # noqa: E402
from index_v2 import true_lifecycle  # noqa: E402
from common_e1r import boot_cluster_single  # noqa: E402
from run_nb6 import emb_scores  # noqa: E402
from cf2_score import paired  # noqa: E402
from a1_count_readers import boot_item_single  # noqa: E402
import census_forbidding as CF  # noqa: E402

G10 = C.ROOT / "r85_graphiti" / "g10"
EXPORT = C.BUILD / "graphiti_edges_g10.json"
OUT = C.RESULTS / "r125_t3_graphiti.json"
BANDS = (0.80, 0.75, 0.50)
RECORDED = {"RECOVERED": 13, "STALE_ACTIVE": 10, "EXTRACTION_MISS": 11, "retracted": 4, "unflagged": 9}
GATES = {"G10-BELIEVED": 0.5765, "G10-LIFTED": 0.6511, "G10-TRUEPROJ": 0.7556, "G10-TRUEPROJ-LIFTED": 0.6958, "TRUE": 0.7424, "BLIND": 0.4964,
         "NB6-emb-capped": 0.6780, "NB5-emb-capped": 0.6994, "NB5-emb-lifted": 0.7959, "G10-VIEW-UNTAGGED": 0.6995, "G10-VIEW-TAGGED": 0.6854, "G10-HYBRID": 0.7741, "FRB-VIEW-UNTAGGED": 0.6991}


def export_edges(personas):
    if EXPORT.exists():
        return C.jload(EXPORT)
    out = {}
    for p in personas:
        edges = CE.read_edges(f"r85stock_{p}_g10")
        states = CE.derive(edges)                      # RULE 1 on the live objects; the export carries the states, so nothing is re-derived from strings
        plain = [{k: (v if isinstance(v, (str, int, float, bool, list, dict)) or v is None else str(v)) for k, v in e.items()} for e in edges]
        out[p] = {"group_id": f"r85stock_{p}_g10", "edges": plain, "states": states}
        print(f"  exported {p}: {len(edges)} edges")
    C.jdump({"meta": {"source": "neo4j-r85 (bolt://localhost:7688), census.read_edges / census.derive (RULE 1)", "when": __import__("time").strftime("%Y-%m-%dT%H:%M:%S")}, "personas": out}, EXPORT)
    return C.jload(EXPORT)


def fires(kind, old, new, J, edges, band):
    if kind in ("supersession", "retraction"):
        d = CE.detector_over(edges, old, new, J.drop) or {}
        return {u: s for u, s in d.items() if s >= band}
    ft = toks(old, J.drop)
    if len(ft) < MIN_DISCR:
        return {}
    return {e["uuid"]: cov(ft, toks(e["fact"], J.drop)) for e in edges if len(ft & toks(e["fact"], J.drop)) >= MIN_SHARED and cov(ft, toks(e["fact"], J.drop)) >= band}


def main():
    joins = load_joins()
    full = [it for it in RC.load_cell() if it["variant"] == "FULL"]
    assert (len(full), sum(i["y_nok"] for i in full)) == (323, 47)
    ids = [it["item_id"] for it in full]; y = np.array([it["y_nok"] for it in full], int); g = np.array([it["persona"] for it in full]); st = np.array([it["state"] for it in full])
    pos = [k for k in range(323) if y[k] == 1]; neg = [k for k in range(323) if y[k] == 0]; assert len(neg) == 276
    ex = export_edges(sorted(joins))["personas"]
    recorded = {o["item_id"]: o for o in C.jload(G10 / "census_forbidding_g10.json")["obligations"]}
    # ---- per obligation: the join's state and marking events (at 0.80, as recorded), then the buckets per band
    per_persona = {}
    obl = []
    for k in pos:
        it = full[k]; p = it["persona"]; J = joins[p]; members = list(it["pn_members"])
        if p not in per_persona:
            sup, ret, exp_, _ = true_lifecycle(J, J.etoks)
            per_persona[p] = {"superseded": sup, "retracted": ret, "expired": exp_, "events": CF.join_events(J)}
        S = per_persona[p]
        state = "retracted" if any(m in S["retracted"] for m in members) else "superseded_or_expired" if any(m in S["superseded"] or m in S["expired"] for m in members) else "unflagged"
        rec = recorded[it["item_id"]]; assert rec["join_state"] == state, (it["item_id"], rec["join_state"], state)
        edges = ex[p]["edges"]; states = ex[p]["states"]
        row = {"item_id": it["item_id"], "persona": p, "state_frbank": it["state"], "attack_vector": it["attack_vector"], "members": members, "join_state": state, "recorded_bucket": rec["bucket"], "bands": {}}
        if state == "superseded_or_expired":
            marked = [m for m in members if m in S["superseded"] or m in S["expired"]]
            evs = [(kd, o, n) for (kd, o, n) in S["events"] if kd != "retraction" and any(CF.marks_record(kd, o, n, J, m) for m in marked)]
        elif state == "retracted":
            marked = [m for m in members if m in S["retracted"]]
            evs = [(kd, o, n) for (kd, o, n) in S["events"] if kd == "retraction" and any(CF.marks_record(kd, o, n, J, m) for m in marked)]
        else:
            evs = []
        row["marking_events"] = len(evs)
        for band in BANDS:
            f = {}
            for kd, o, n in evs:
                f.update(fires(kd, o, n, J, edges, band))
            if not evs:
                b = "NO_JOIN_EVENT"
            elif not f:
                b = "EXTRACTION_MISS"
            elif any(states[u] != "active" for u in f):
                b = "RECOVERED"
            else:
                b = "STALE_ACTIVE"
            row["bands"][f"{band:.2f}"] = {"bucket": b, "retained": bool(f), "firing_edges": len(f), "firing_non_active": sum(1 for u in f if states[u] != "active"),
                                          "best_overlap": r4(max(f.values())) if f else None}
        if state == "superseded_or_expired":
            assert row["bands"]["0.80"]["bucket"] == rec["bucket"], (it["item_id"], row["bands"]["0.80"], rec["bucket"])
        obl.append(row)
    cnt = collections.Counter(r["bands"]["0.80"]["bucket"] for r in obl if r["join_state"] == "superseded_or_expired")
    n_ret = sum(1 for r in obl if r["join_state"] == "retracted"); n_unf = sum(1 for r in obl if r["join_state"] == "unflagged")
    got = {**dict(cnt), "retracted": n_ret, "unflagged": n_unf}
    assert got == RECORDED, (got, RECORDED)
    print("recorded buckets at 0.80 reproduce:", got)
    for band in BANDS:
        c = collections.Counter(r["bands"][f"{band:.2f}"]["bucket"] for r in obl if r["join_state"] == "superseded_or_expired")
        cr = collections.Counter(r["bands"][f"{band:.2f}"]["retained"] for r in obl if r["join_state"] == "retracted")
        print(f"  band {band:.2f}: the 34 sup-or-exp {dict(c)} (retained = recovered + stale-active = {c['RECOVERED'] + c['STALE_ACTIVE']}); the 4 join-retracted: content retained {cr[True]} of 4")

    # ---- the readers on the 323
    ix = C.jload(G10 / "indexes_g10.json")["personas"]
    V = {"TRUE": np.array([it["true"]["nok"] for it in full], float), "BLIND": np.array([it["blind"]["nok"] for it in full], float)}
    for fn in ("rows_summary.jsonl", "rows_view.jsonl"):
        by = collections.defaultdict(dict)
        for line in open(G10 / fn, encoding="utf-8"):
            r = json.loads(line)
            if r.get("status") == "OK":
                by[r["arm"]][r["item_id"]] = float(r["nok"])
        for arm, d in by.items():
            V[arm] = np.array([d[i] for i in ids], float)
    V["NB6-emb-capped"] = np.array(emb_scores([{"question": it["question"], "sup": ix[it["persona"]]["believed_capped"]["names_sup"]} for it in full], "sup"), float)
    V["NB5-emb-capped"] = np.array(emb_scores([{"question": it["question"], "all": ix[it["persona"]]["believed_capped"]["names_all"]} for it in full], "all"), float)
    V["NB5-emb-lifted"] = np.array(emb_scores([{"question": it["question"], "all": ix[it["persona"]]["believed_lifted"]["names_all"]} for it in full], "all"), float)
    gates = {k: r4(auroc(V[k], y)) for k in GATES}
    for k, want in GATES.items():
        assert gates[k] == want, (k, gates[k], want)
    print("gates", gates, "PASS")
    # ---- strata
    kp = {r["item_id"]: k for k, r in zip(pos, obl)}
    strata = {"all_47 (manifest-relative, the printed rows)": list(pos)}
    for band in BANDS:
        tag = f"{band:.2f}"
        strata[f"retained_{tag} (recovered + stale-active, of the 34)"] = [kp[r["item_id"]] for r in obl if r["join_state"] == "superseded_or_expired" and r["bands"][tag]["retained"]]
        strata[f"recovered_{tag} (non-active mark on a firing edge)"] = [kp[r["item_id"]] for r in obl if r["join_state"] == "superseded_or_expired" and r["bands"][tag]["bucket"] == "RECOVERED"]
        strata[f"stale_active_{tag}"] = [kp[r["item_id"]] for r in obl if r["join_state"] == "superseded_or_expired" and r["bands"][tag]["bucket"] == "STALE_ACTIVE"]
        strata[f"extraction_miss_{tag}"] = [kp[r["item_id"]] for r in obl if r["join_state"] == "superseded_or_expired" and r["bands"][tag]["bucket"] == "EXTRACTION_MISS"]
    strata["join_retracted_4 (inexpressible)"] = [kp[r["item_id"]] for r in obl if r["join_state"] == "retracted"]
    strata["join_unflagged_9"] = [kp[r["item_id"]] for r in obl if r["join_state"] == "unflagged"]
    strata["not_retained_0.80 (extraction miss + retracted + unflagged)"] = [kp[r["item_id"]] for r in obl if not (r["join_state"] == "superseded_or_expired" and r["bands"]["0.80"]["retained"])]
    READERS = ["G10-BELIEVED", "G10-LIFTED", "G10-TRUEPROJ", "G10-TRUEPROJ-LIFTED", "NB6-emb-capped", "NB5-emb-capped", "NB5-emb-lifted", "G10-VIEW-UNTAGGED", "G10-VIEW-TAGGED", "G10-HYBRID", "FRB-VIEW-UNTAGGED", "TRUE", "BLIND"]
    rescored = {}
    for name, kk in strata.items():
        if not kk:
            rescored[name] = {"n_pos": 0, "note": "empty stratum"}
            continue
        keep = sorted(kk + neg); yy = y[keep]; gg = g[keep]
        blk = {"n_pos": len(kk), "n": len(keep), "by_state": dict(collections.Counter(st[k] for k in kk)), "readers": {}}
        for key in READERS:
            v = V[key][keep]
            d = {"auroc": r4(auroc(v, yy)), "ci_item": boot_item_single(v, yy), "ci_persona": boot_cluster_single(v, yy, gg)}
            if key not in ("TRUE", "BLIND"):
                d["minus_true"] = paired(V["TRUE"][keep], v, yy, gg)
            blk["readers"][key] = d
        rescored[name] = blk
        print(f"  {name:58s} n_pos {len(kk):2d} " + " ".join(f"{key[:10]} {blk['readers'][key]['auroc']:.4f}" for key in ("G10-BELIEVED", "G10-LIFTED", "NB6-emb-capped", "G10-VIEW-TAGGED", "G10-HYBRID", "TRUE")))
    res = {"meta": {"script": "reviews/r125/tools/r125_t3_graphiti.py", "model_calls": 0, "status": "post hoc, offline; the graph read once from the local container and exported", "bands": list(BANDS),
                    "export": str(EXPORT.relative_to(C.ROOT)), "n_boot": C.N_BOOT, "seed": C.SEED, "population": "the 323 FULL-variant items, 47 obligations (D-R85-17)"},
           "gates": gates, "recorded_buckets_080": got,
           "counts": {f"{b:.2f}": {"sup_or_exp_34": dict(collections.Counter(r["bands"][f"{b:.2f}"]["bucket"] for r in obl if r["join_state"] == "superseded_or_expired")),
                                   "retained": sum(1 for r in obl if r["join_state"] == "superseded_or_expired" and r["bands"][f"{b:.2f}"]["retained"]),
                                   "retracted_content_retained": sum(1 for r in obl if r["join_state"] == "retracted" and r["bands"][f"{b:.2f}"]["retained"])} for b in BANDS},
           "obligations": obl, "strata": {k: len(v) for k, v in strata.items()}, "rescored": rescored}
    C.jdump(res, OUT)
    print(f"-> {OUT.relative_to(C.ROOT)}")


if __name__ == "__main__":
    main()
