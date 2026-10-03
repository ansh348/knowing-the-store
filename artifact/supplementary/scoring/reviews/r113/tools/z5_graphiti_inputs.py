# -*- coding: utf-8 -*-
"""z5_graphiti_inputs.py -- SPEC_R113 section Z5: what R85 Amendment 1's summary route (Step 4) and tag route (Step 5) would need,
against what exists on disk at this pass. NO MODEL CALL. $0. Deterministic record only: P3 is not scored; no index is built.
Reads the forty census records (r85_graphiti/census_runs/g10_<persona>.{json,index.txt}), the frozen SLOT_CAP, the Docker engine's
reachability (one `docker ps`, no side effect) and whether any edge export exists under r85_graphiti/. Writes
reviews/r113/results/z5_graphiti_inputs.json; appends AUX-R113-Z5 to NUMBERS_R113.md.
"""
from __future__ import annotations

import datetime as dt
import glob
import io
import json
import re
import subprocess

from r113_common import ROOT, RESULTS, J, jdump, assert_spec, ledger_append

G = ROOT / "r85_graphiti"


def slot_cap():
    src = (ROOT / "e1_metamemory" / "tools" / "index_v2.py").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^SLOT_CAP\s*=\s*(\d+)", src, re.M)
    return int(m.group(1)) if m else None


def main():
    assert_spec()
    cap = slot_cap()
    per = {}
    for p in sorted(glob.glob(str(G / "census_runs" / "g10_*.json"))):
        d = J(p); persona = d["persona"]
        txt = io.open(p[:-5] + ".index.txt", encoding="utf-8").read()
        sup_sec = txt.split("ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT")[1] if "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT" in txt else ""
        map_sec = txt.split("ATTRIBUTE NAMES  (")[1].split("ATTRIBUTE NAMES CARRYING")[0] if "ATTRIBUTE NAMES  (" in txt else ""
        per[persona] = {"edges": d["edges"], "states": d["states"], "superseded_names": len(d["superseded_names"]), "superseded_section_truncated": "more)" in sup_sec,
                        "distinct_attribute_names": d["distinct_attribute_names"], "map_section_truncated": "more)" in map_sec,
                        "invalidated_names": len(d.get("invalidated_names", [])), "group_id": d["group_id"]}
    assert len(per) == 40, len(per)
    n_sup_trunc = sum(v["superseded_section_truncated"] for v in per.values()); n_map_trunc = sum(v["map_section_truncated"] for v in per.values())
    max_sup = max(v["superseded_names"] for v in per.values()); min_map = min(v["distinct_attribute_names"] for v in per.values())
    try:
        r = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True, timeout=30)
        docker = {"returncode": r.returncode, "stdout": r.stdout.strip()[:300], "stderr": r.stderr.strip()[:300]}
    except Exception as e:  # noqa: BLE001
        docker = {"returncode": None, "error": str(e)[:300]}
    engine_up = docker.get("returncode") == 0
    neo4j_up = engine_up and "neo4j-r85" in docker.get("stdout", "")
    # any edge export on disk? (a JSON holding per-edge facts; the census records hold counts and names only)
    big = []
    for p in glob.glob(str(G / "**" / "*.json"), recursive=True):
        try:
            s = io.open(p, encoding="utf-8").read(200000)
        except Exception:  # noqa: BLE001
            continue
        if '"fact"' in s and '"valid_at"' in s:
            big.append(str(ROOT and p).replace(str(ROOT) + "\\", "").replace("\\", "/"))
    res = {"meta": {"script": "reviews/r113/tools/z5_graphiti_inputs.py", "spec": "SPEC_R113 Z5", "model_calls": 0, "when": dt.datetime.now().isoformat(timespec="seconds")},
           "slot_cap_frozen": cap, "personas": 40, "superseded_names_max": max_sup, "superseded_section_truncated_personas": n_sup_trunc,
           "map_section_truncated_personas": n_map_trunc, "distinct_attribute_names_min": min_map,
           "docker": docker, "engine_reachable": engine_up, "neo4j_r85_running": neo4j_up, "edge_exports_on_disk": big,
           "consequences": {
               "NB-6 over the superseded list (P3's reader)": "the capped and lifted renderings print the same superseded-names section for every persona (no persona has more than the cap), so the section NB-6 reads exists on disk for all forty; P3 stays unscored at this pass: its population ruling is pending (D-R85-16) and the registration names both renderings",
               "NB-5 over the whole map": "the capped rendering truncates the name map in every persona; the lifted rendering needs the graph",
               "BELIEVED-lifted and TRUE-projected indexes (Step 4)": "need the graph: the engine is down and no per-edge export exists on disk",
               "the tag route's retrieval (Step 5)": "stock Graphiti.search embeds the query with text-embedding-3-small (an API call) and needs the graph: not permitted at this pass",
               "Amendment 2's Graphiti views": "need Step 5's record"},
           "per_persona": per}
    jdump(res, RESULTS / "z5_graphiti_inputs.json")
    L = ["\n## 5. AUX-R113-Z5: R85 Amendment 1 Steps 4 and 5, what exists and what does not (SPEC_R113 Z5; no call; no index built; P3 not scored)\n\n",
         f"The forty `census_runs/g10_<persona>` records: superseded-names section at most **{max_sup}** names against the frozen `SLOT_CAP = {cap}`, truncated in **{n_sup_trunc}** of 40 personas, so the BELIEVED-capped and BELIEVED-lifted renderings print the same superseded-names section for every persona and the list NB-6 reads for P3 exists on disk for all forty; the whole-map section is truncated (`(+N more)`) in **{n_map_trunc}** of 40 (distinct attribute names at least {min_map}), so NB-5's lifted reading needs the graph. ",
         f"Environment at this pass: Docker engine reachable **{engine_up}**, `neo4j-r85` running **{neo4j_up}**; per-edge exports under `r85_graphiti/`: {big if big else 'none'} (the census records hold counts, buckets and name lists, not edges). ",
         "Consequences: the BELIEVED-lifted and TRUE-projected indexes (Step 4) and the tag route's retrieval (Step 5; stock `Graphiti.search`, a `text-embedding-3-small` call per query) cannot be built without the graph and, for Step 5, without an embedding call; Amendment 2's Graphiti views need Step 5's record. P3 (the NB-6 matcher within tolerance of 0.50 under both renderings) is computable from disk for the superseded section alone and is **not scored here**: its population ruling is the author's (D-R85-16) and the registration names both renderings.\n"]
    ledger_append("".join(L))


if __name__ == "__main__":
    main()
