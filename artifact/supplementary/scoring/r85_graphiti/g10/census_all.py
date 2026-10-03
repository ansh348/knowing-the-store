"""census_all.py -- R85 Amendment 1, Step 3, section 4 A(i): the R85 census as frozen, over the forty g10 graphs. NO API CALL.

Runs the frozen r85_graphiti/census.py per persona with `--group-tag g10` (group r85stock_<persona>_g10, D-R85-15), unchanged;
moves each record from census_runs/stock_gpt-4.1-mini-2025-04-14_<persona>.{json,index.txt} (census.py's fixed naming, which would
overwrite the spike's committed records for elena, tom and yoli) to census_runs/g10_<persona>.{json,index.txt}, restoring the three
spike records from HEAD afterwards; then pools the forty records: the buckets over the manifest supersession events, recall at the
frozen tau 0.80 with the 0.75 and 0.50 bands, precision as explained-invalidated over all invalidated edges, entity fragmentation and
undated edges, plus the future-dated-edge count per persona (edges whose valid_at or invalid_at lies after the persona clock t_now,
amendment section 3) and the repeatability rows for the three spike personas (their g10 rows beside their trial rows).
Writes r85_graphiti/g10/census_g10.json and prints the pooled table.

Runs under the repository interpreter (census.py needs yaml and neo4j; no Graphiti import), from the repo root:
  python r85_graphiti/g10/census_all.py
"""
from __future__ import annotations

import collections
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R85 = HERE.parent
ROOT = R85.parent
sys.path.insert(0, str(R85))
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import census as C  # noqa: E402  (the frozen tool, imported for read_edges; run as a subprocess for the records)
import render_episodes as R  # noqa: E402
from e0_common import load_joins, parse_dt  # noqa: E402

MODEL = "gpt-4.1-mini-2025-04-14"
ARM, TAG = "stock", "g10"
RUNS = R85 / "census_runs"
SPIKE = ("elena", "tom", "yoli")
OUT = HERE / "census_g10.json"


def run_one(p):
    r = subprocess.run([sys.executable, str(R85 / "census.py"), "--persona", p, "--arm", ARM, "--model", MODEL, "--group-tag", TAG],
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise SystemExit(f"census.py failed on {p}:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
    src = RUNS / f"{ARM}_{MODEL}_{p}.json"
    rec = json.loads(src.read_text(encoding="utf-8"))
    assert rec["group_id"] == f"r85{ARM}_{p}_{TAG}", rec["group_id"]
    (RUNS / f"g10_{p}.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")
    (RUNS / f"g10_{p}.index.txt").write_text((RUNS / f"{ARM}_{MODEL}_{p}.index.txt").read_text(encoding="utf-8"), encoding="utf-8")
    src.unlink()
    (RUNS / f"{ARM}_{MODEL}_{p}.index.txt").unlink()
    if p in SPIKE:
        for ext in ("json", "index.txt"):
            rel = f"r85_graphiti/census_runs/{ARM}_{MODEL}_{p}.{ext}"
            subprocess.run(["git", "checkout", "--", rel], cwd=ROOT, capture_output=True)
    return rec


def future_dated(p, J):
    edges = C.read_edges(f"r85{ARM}_{p}_{TAG}")
    t_now = J.t_now
    n = sum(1 for e in edges if any(parse_dt(e[k]) and parse_dt(e[k]) > t_now for k in ("valid_at", "invalid_at")))
    return n, len(edges)


def main():
    personas = [p.stem for p in sorted(R.BANKS.glob("*.json"))]
    assert len(personas) == 40
    joins = load_joins()
    recs, fut = {}, {}
    for p in personas:
        recs[p] = run_one(p)
        fut[p] = future_dated(p, joins[p])
        r = recs[p]
        print(f"{p:10s} edges={r['edges']:4d} states={r['states']}  events={r['manifest_supersession_events']} buckets={r['buckets']}  "
              f"recall={r['supersession_recall']} precision={r['supersession_precision']}  future-dated={fut[p][0]}", flush=True)

    # ---- pooled, the R85 census as frozen
    buckets = collections.Counter()
    bands = collections.Counter()
    denom = explained_num = 0
    invalidated = 0
    states = collections.Counter()
    frag = collections.Counter()
    undated = incoherent = edges = 0
    facts = collections.Counter()
    by_kind = collections.defaultdict(lambda: [0, 0])
    for p, r in recs.items():
        buckets.update(r["buckets"])
        denom += r["manifest_supersession_events"]
        for k, (v, d) in r["recall_by_band"].items():
            bands[k] += v
        # precision as frozen: explained-invalidated / invalidated edges, both summed over the forty graphs
        if r["supersession_precision"] is not None:
            explained_num += round(r["supersession_precision"] * r["believed_superseded_edges"])
        invalidated += r["believed_superseded_edges"]
        states.update(r["states"])
        frag[len(r["user_entity_nodes"])] += 1
        undated += r["valid_at_null_edges"]
        incoherent += r["edges_invalid_before_valid"]
        edges += r["edges"]
        facts["extracted"] += r["manifest_facts_extracted"]
        facts["total"] += r["manifest_facts"]
        for k, (v, d) in r["manifest_fact_recall_by_kind"].items():
            by_kind[k][0] += v; by_kind[k][1] += d
    pooled = {
        "personas": 40, "edges": edges, "states": dict(states),
        "manifest_supersession_events": denom, "buckets": dict(buckets),
        "recall_tau_0.80": round(buckets["RECOVERED"] / denom, 4) if denom else None,
        "recall_by_band": {k: [v, denom] for k, v in sorted(bands.items())},
        "invalidated_edges": invalidated, "explained_invalidated_edges": explained_num,
        "precision": round(explained_num / invalidated, 4) if invalidated else None,
        "user_entity_nodes_per_persona": {str(k): v for k, v in sorted(frag.items())},
        "valid_at_null_edges": undated, "edges_invalid_before_valid": incoherent,
        "manifest_facts": facts["total"], "manifest_facts_extracted": facts["extracted"],
        "manifest_fact_recall": round(facts["extracted"] / facts["total"], 4) if facts["total"] else None,
        "manifest_fact_recall_by_kind": {k: v for k, v in sorted(by_kind.items())},
        "future_dated_edges": {p: {"future_dated": n, "edges": m} for p, (n, m) in fut.items()},
        "future_dated_edges_total": sum(n for n, _ in fut.values()),
    }
    # ---- repeatability rows: the three spike personas, trial (r85stock_<p>) beside g10 (r85stock_<p>_g10)
    rep = {}
    for p in SPIKE:
        t = json.loads((RUNS / f"{ARM}_{MODEL}_{p}.json").read_text(encoding="utf-8"))
        g = recs[p]
        rep[p] = {k: {"trial": t[k], "g10": g[k]} for k in
                  ("edges", "states", "manifest_supersession_events", "buckets", "supersession_recall", "supersession_precision",
                   "believed_superseded_edges", "manifest_fact_recall", "distinct_attribute_names", "valid_at_null_edges",
                   "edges_invalid_before_valid", "user_entity_nodes")}
    out = {"pooled": pooled, "repeatability": rep, "per_persona": {p: {k: v for k, v in r.items() if k != "detail"} for p, r in recs.items()}}
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("\n=== pooled (the R85 census as frozen, forty personas) ===")
    for k in ("edges", "states", "manifest_supersession_events", "buckets", "recall_tau_0.80", "recall_by_band", "invalidated_edges",
              "explained_invalidated_edges", "precision", "user_entity_nodes_per_persona", "valid_at_null_edges", "edges_invalid_before_valid",
              "manifest_facts", "manifest_facts_extracted", "manifest_fact_recall", "manifest_fact_recall_by_kind", "future_dated_edges_total"):
        print(f"  {k}: {pooled[k]}")
    print("=== repeatability (trial | g10) ===")
    for p, d in rep.items():
        print(f"  {p}: edges {d['edges']['trial']} | {d['edges']['g10']}; events {d['manifest_supersession_events']['trial']} | "
              f"{d['manifest_supersession_events']['g10']}; buckets {d['buckets']['trial']} | {d['buckets']['g10']}; "
              f"recall {d['supersession_recall']['trial']} | {d['supersession_recall']['g10']}; precision {d['supersession_precision']['trial']} | "
              f"{d['supersession_precision']['g10']}; fact recall {d['manifest_fact_recall']['trial']} | {d['manifest_fact_recall']['g10']}")
    print(f"-> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
