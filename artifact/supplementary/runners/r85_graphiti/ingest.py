"""ingest.py -- R85 Phase 1. Ingest a rendered persona into Graphiti. BILLED.

Runs the frozen episode stream from render_episodes.py through Graphiti and records what it
cost and how long it took, per episode, so the 40-persona projection rests on measurement.

RULE 3 is enforced here and is visible in the add_episode call: entity_types, edge_types and
custom_extraction_instructions are all left None, so the run is Graphiti's own defaults. Both
ends of the model config are pinned, because Graphiti routes some subtasks to a `small_model`
and an arm that mixed mini with nano would not be a clean arm.

Arms:
  stock  -- unmodified graphiti-core 0.28.1, run with the r85_stock_venv interpreter
  fork   -- the locally modified vendored tree, run with the repo .venv interpreter

Usage (stock arm):
  /c/Users/[AUTHOR-1]/AppData/Local/r85_stock_venv/Scripts/python.exe \
      r85_graphiti/ingest.py --persona elena --arm stock --model gpt-4.1-mini-2025-04-14
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import render_episodes as R  # noqa: E402

# USD per million tokens.
PRICES = {
    "gpt-4.1-mini-2025-04-14": (0.40, 1.60),
    "gpt-4.1-nano-2025-04-14": (0.10, 0.40),
}
EMBED_PRICE = 0.02
EMBED_MODEL = "text-embedding-3-small"
NEO4J_URI = "bolt://localhost:7688"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "r85graphiti2026"


def load_env():
    env = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


class Meter:
    """Accumulates token usage by wrapping the injected OpenAI client's call sites."""

    def __init__(self):
        self.llm_in = self.llm_out = self.llm_cached = self.embed_in = 0
        self.calls = 0
        self.embed_calls = 0

    def wrap(self, client):
        meter = self

        def instrument(owner, attr, kind):
            original = getattr(owner, attr)

            async def wrapped(*a, **kw):
                resp = await original(*a, **kw)
                u = getattr(resp, "usage", None)
                if u is not None:
                    if kind == "llm":
                        meter.calls += 1
                        meter.llm_in += getattr(u, "input_tokens", 0) or getattr(u, "prompt_tokens", 0) or 0
                        meter.llm_out += getattr(u, "output_tokens", 0) or getattr(u, "completion_tokens", 0) or 0
                        det = getattr(u, "input_tokens_details", None) or getattr(u, "prompt_tokens_details", None)
                        meter.llm_cached += getattr(det, "cached_tokens", 0) or 0
                    else:
                        meter.embed_calls += 1
                        meter.embed_in += getattr(u, "prompt_tokens", 0) or getattr(u, "total_tokens", 0) or 0
                return resp

            setattr(owner, attr, wrapped)

        instrument(client.responses, "parse", "llm")
        instrument(client.chat.completions, "create", "llm")
        instrument(client.embeddings, "create", "embed")
        return client

    def cost(self, model):
        pin, pout = PRICES[model]
        billed_in = self.llm_in - self.llm_cached
        return (billed_in * pin + self.llm_cached * pin * 0.25 + self.llm_out * pout) / 1e6 \
            + self.embed_in * EMBED_PRICE / 1e6


async def run(persona, arm, model, limit, wipe, group_tag):
    import logging
    # The driver emits a property-key-does-not-exist warning per search on a sparse graph.
    # It is expected on an empty store and would otherwise bury the per-episode log.
    logging.getLogger("neo4j").setLevel(logging.ERROR)
    logging.getLogger("neo4j.notifications").setLevel(logging.ERROR)
    env = load_env()
    os.environ["OPENAI_API_KEY"] = env["OPENAI_API_KEY"]

    from openai import AsyncOpenAI
    from graphiti_core import Graphiti
    from graphiti_core.nodes import EpisodeType
    from graphiti_core.llm_client import LLMConfig, OpenAIClient
    from graphiti_core.embedder import OpenAIEmbedder, OpenAIEmbedderConfig
    import graphiti_core

    resolved = graphiti_core.__file__
    is_stock = "site-packages" in resolved
    assert (arm == "stock") == is_stock, (
        f"arm={arm} but graphiti_core resolves to {resolved}. Use the matching interpreter.")

    meter = Meter()
    client = meter.wrap(AsyncOpenAI(api_key=env["OPENAI_API_KEY"]))
    # Both ends pinned: Graphiti routes some subtasks to small_model.
    cfg = LLMConfig(api_key=env["OPENAI_API_KEY"], model=model, small_model=model)
    g = Graphiti(
        NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD,
        llm_client=OpenAIClient(config=cfg, client=client),
        embedder=OpenAIEmbedder(
            config=OpenAIEmbedderConfig(api_key=env["OPENAI_API_KEY"], embedding_model=EMBED_MODEL),
            client=client),
    )
    await g.build_indices_and_constraints()

    # The model belongs in the group id: without it a second model on the same persona
    # would wipe the first model's graph.
    group_id = f"r85{arm}_{persona}" + (f"_{group_tag}" if group_tag else "")

    if wipe:
        # A partial group from an aborted run would confound timeline-order invalidation.
        res = await g.driver.execute_query(
            "MATCH (n) WHERE n.group_id = $g DETACH DELETE n RETURN count(n) AS n",
            g=group_id)
        print(f"wiped group {group_id}: {res[0][0]['n'] if res[0] else 0} nodes")

    episodes, _ = R.build(persona)
    if limit:
        episodes = episodes[:limit]
    tag = f"{arm}_{model}_{persona}"
    print(f"[{tag}] group_id={group_id} episodes={len(episodes)} resolves={resolved}")

    rows, t0 = [], time.time()
    for i, ep in enumerate(episodes, 1):
        before = (meter.llm_in, meter.llm_out, meter.embed_in, meter.calls)
        t = time.time()
        res = await g.add_episode(
            name=ep["name"],
            episode_body=ep["episode_body"],
            source_description=ep["source_description"],
            reference_time=datetime.fromisoformat(ep["reference_time"]),
            source=EpisodeType.message,
            group_id=group_id,
            # RULE 3: stock defaults. Nothing custom is passed.
            entity_types=None,
            edge_types=None,
            custom_extraction_instructions=None,
        )
        dt = time.time() - t
        rows.append({
            "i": i, "name": ep["name"], "reference_time": ep["reference_time"],
            "n_records": ep["n_records"], "seconds": round(dt, 2),
            "nodes": len(res.nodes), "edges": len(res.edges),
            "llm_calls": meter.calls - before[3],
            "in": meter.llm_in - before[0], "out": meter.llm_out - before[1],
            "embed": meter.embed_in - before[2],
            "cum_usd": round(meter.cost(model), 4),
        })
        print(f"  [{i:3d}/{len(episodes)}] {ep['name']} {dt:6.1f}s "
              f"nodes={len(res.nodes):3d} edges={len(res.edges):3d} "
              f"calls={rows[-1]['llm_calls']:3d} cum=${rows[-1]['cum_usd']:.4f}", flush=True)
        # Checkpoint the ledger every episode. A run stopped part way still has to be able
        # to say what it spent: the program requires every number to trace to an artifact,
        # and a cost record written only at the end is lost exactly when it is needed.
        ckpt = HERE / "ingest_runs"
        ckpt.mkdir(exist_ok=True)
        (ckpt / f"{tag}.partial.json").write_text(json.dumps({
            "tag": tag, "persona": persona, "arm": arm, "model": model,
            "group_id": group_id, "complete": False,
            "episodes_done": i, "episodes_total": len(episodes),
            "usd": round(meter.cost(model), 4),
            "wall_seconds": round(time.time() - t0, 1),
            "llm_calls": meter.calls, "tokens_in": meter.llm_in,
            "tokens_out": meter.llm_out, "embed_tokens": meter.embed_in,
            "per_episode": rows,
        }, indent=2), encoding="utf-8")

    wall = time.time() - t0
    usd = meter.cost(model)
    out = {
        "tag": tag, "persona": persona, "arm": arm, "model": model, "group_id": group_id,
        "graphiti_core": resolved, "episodes": len(episodes),
        "records": sum(e["n_records"] for e in episodes),
        "wall_seconds": round(wall, 1), "usd": round(usd, 4),
        "usd_per_episode": round(usd / max(len(episodes), 1), 5),
        "seconds_per_episode": round(wall / max(len(episodes), 1), 2),
        "llm_calls": meter.calls, "embed_calls": meter.embed_calls,
        "tokens_in": meter.llm_in, "tokens_cached": meter.llm_cached,
        "tokens_out": meter.llm_out, "embed_tokens": meter.embed_in,
        "per_episode": rows,
    }
    d = HERE / "ingest_runs"
    d.mkdir(exist_ok=True)
    out["complete"] = True
    (d / f"{tag}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    (d / f"{tag}.partial.json").unlink(missing_ok=True)
    print(f"\n[{tag}] DONE episodes={len(episodes)} wall={wall/60:.1f}min "
          f"usd=${usd:.4f} (${usd/max(len(episodes),1):.5f}/episode) "
          f"calls={meter.calls} in={meter.llm_in} cached={meter.llm_cached} out={meter.llm_out}")
    print(f"[{tag}] 40-persona projection at this rate: "
          f"${usd/max(len(episodes),1)*1365:.2f}, "
          f"{wall/max(len(episodes),1)*1365/3600:.1f}h sequential")
    await g.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--persona", required=True)
    ap.add_argument("--arm", required=True, choices=("stock", "fork"))
    ap.add_argument("--model", required=True, choices=tuple(PRICES))
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--wipe", action="store_true")
    ap.add_argument("--group-tag", default="", dest="group_tag")
    a = ap.parse_args()
    asyncio.run(run(a.persona, a.arm, a.model, a.limit, a.wipe, a.group_tag))


if __name__ == "__main__":
    main()
