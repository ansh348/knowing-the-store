"""retrieve.py -- R85 Amendment 1 Step 5, the tag-route retrieval (section 4 C). BILLED: one text-embedding-3-small call per query
(Graphiti's own query embedding). NO LLM CALL. NO WRITE TO THE GRAPH. Runs in the STOCK venv (unmodified graphiti-core 0.28.1).

Per item of g10/retrieve_jobs.json (the 323 FULL-variant items, D-R85-17): stock Graphiti.search(question, group_ids=[group_id],
num_results=10) -- EDGE_HYBRID_SEARCH_RRF (BM25 + cosine, reciprocal-rank fusion, no reranker), default SearchFilters(), so
invalidated and expired edges are returned; the ten EntityEdges recorded in rank order with every temporal field, the search
configuration, the served embedding model and the metered usage. The RULE 1 states, RULE 2 names and the rendered lines are
derived afterwards by g10/build_views_g10.py in the repository venv from the same edges.

Usage (stock arm):
  /c/Users/[AUTHOR-1]/AppData/Local/r85_stock_venv/Scripts/python.exe r85_graphiti/g10/retrieve.py
"""
from __future__ import annotations

import asyncio
import datetime as dt
import hashlib
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
R85 = HERE.parent
ROOT = R85.parent
sys.path.insert(0, str(R85))
import ingest as I  # noqa: E402  (load_env, Meter, the pinned constants; nothing else)

JOBS = HERE / "retrieve_jobs.json"
OUT = HERE / "retrieval_raw_g10.json"
K_TAKE = 10
SPEC_SHA = "f13b7df47a9e58ebcd345e1d6d2c5b8fcc3a214ceec3da946cff9ca09722555b"


def edge_dict(e):
    def iso(v):
        return v.isoformat() if isinstance(v, dt.datetime) else v
    return {"uuid": e.uuid, "group_id": e.group_id, "name": e.name, "fact": e.fact, "source_node_uuid": e.source_node_uuid, "target_node_uuid": e.target_node_uuid,
            "created_at": iso(e.created_at), "valid_at": iso(e.valid_at), "invalid_at": iso(e.invalid_at), "expired_at": iso(e.expired_at),
            "episodes": list(e.episodes or []), "attributes": dict(e.attributes or {})}


async def run():
    import logging
    logging.getLogger("neo4j").setLevel(logging.ERROR); logging.getLogger("neo4j.notifications").setLevel(logging.ERROR)
    spec = ROOT / "reviews" / "r114" / "SPEC_R114.md"
    assert hashlib.sha256(spec.read_bytes()).hexdigest() == SPEC_SHA, "SPEC_R114 hash -- STOP"
    env = I.load_env(); os.environ["OPENAI_API_KEY"] = env["OPENAI_API_KEY"]
    from openai import AsyncOpenAI
    from graphiti_core import Graphiti
    from graphiti_core.llm_client import LLMConfig, OpenAIClient
    from graphiti_core.embedder import OpenAIEmbedder, OpenAIEmbedderConfig
    from graphiti_core.search.search_config_recipes import EDGE_HYBRID_SEARCH_RRF
    from graphiti_core.search.search_filters import SearchFilters
    import graphiti_core
    resolved = graphiti_core.__file__
    assert "site-packages" in resolved, f"not the stock package: {resolved}"
    meter = I.Meter()
    client = meter.wrap(AsyncOpenAI(api_key=env["OPENAI_API_KEY"]))
    cfg = LLMConfig(api_key=env["OPENAI_API_KEY"], model=I.PRICES and "gpt-4.1-mini-2025-04-14", small_model="gpt-4.1-mini-2025-04-14")
    g = Graphiti(I.NEO4J_URI, I.NEO4J_USER, I.NEO4J_PASSWORD, llm_client=OpenAIClient(config=cfg, client=client),
                 embedder=OpenAIEmbedder(config=OpenAIEmbedderConfig(api_key=env["OPENAI_API_KEY"], embedding_model=I.EMBED_MODEL), client=client))
    jobs = json.loads(JOBS.read_text(encoding="utf-8"))["jobs"]
    assert len(jobs) == 323
    done = {}
    if OUT.exists():
        done = {r["item_id"]: r for r in json.loads(OUT.read_text(encoding="utf-8"))["items"].values()}
    out = dict(done); t0 = time.time()
    for n, j in enumerate(jobs, 1):
        if j["item_id"] in out:
            continue
        before = (meter.embed_in, meter.embed_calls, meter.calls)
        t = time.time()
        edges = await g.search(j["question"], group_ids=[j["group_id"]], num_results=K_TAKE)
        assert meter.calls == before[2], "an LLM call was made during search -- STOP"
        out[j["item_id"]] = {**j, "edges": [edge_dict(e) for e in edges], "n": len(edges), "embed_tokens": meter.embed_in - before[0], "embed_calls": meter.embed_calls - before[1],
                            "seconds": round(time.time() - t, 2), "when": dt.datetime.now().isoformat(timespec="seconds")}
        if n % 40 == 0 or n == len(jobs):
            OUT.write_text(json.dumps({"meta": meta(resolved, EDGE_HYBRID_SEARCH_RRF, SearchFilters(), meter, t0), "items": out}, indent=1), encoding="utf-8")
            print(f"  [{n:3d}/{len(jobs)}] edges={len(edges)} embed_calls={meter.embed_calls} embed_tokens={meter.embed_in} cum=${meter.embed_in * I.EMBED_PRICE / 1e6:.5f}", flush=True)
    OUT.write_text(json.dumps({"meta": meta(resolved, EDGE_HYBRID_SEARCH_RRF, SearchFilters(), meter, t0), "items": out}, indent=1), encoding="utf-8")
    print(f"DONE {len(out)} items; embed calls {meter.embed_calls}, tokens {meter.embed_in}, ${meter.embed_in * I.EMBED_PRICE / 1e6:.5f}; LLM calls {meter.calls}")
    await g.close()


def meta(resolved, cfgobj, filt, meter, t0):
    return {"script": "r85_graphiti/g10/retrieve.py", "graphiti_core": resolved, "search": "Graphiti.search(query, group_ids=[group_id], num_results=10)",
            "config": "EDGE_HYBRID_SEARCH_RRF", "config_repr": repr(cfgobj)[:600], "search_filter": repr(filt)[:300], "embedder": I.EMBED_MODEL, "embed_price_per_mtok": I.EMBED_PRICE,
            "embed_calls": meter.embed_calls, "embed_tokens": meter.embed_in, "usd": round(meter.embed_in * I.EMBED_PRICE / 1e6, 6), "llm_calls": meter.calls,
            "k_take": K_TAKE, "population": "the 323 FULL-variant items (D-R85-17)", "wall_seconds": round(time.time() - t0, 1), "when": dt.datetime.now().isoformat(timespec="seconds")}


if __name__ == "__main__":
    asyncio.run(run())
