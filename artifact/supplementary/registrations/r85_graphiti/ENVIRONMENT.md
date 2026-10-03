# R85-GRAPHITI — environment of record

Frozen at Phase 0. Any change after the R85-0 commit is a deviation with its own entry.

## Two environments, deliberately separate

The repository's own `.venv` installs `graphiti-core 0.28.1` as an **editable** install
pointing at `graphiti/`, so in that environment `import graphiti_core` resolves to the
locally modified copy. The unmodified arm therefore cannot run there. It runs in a venv
created outside the repository root so that neither `_graphiti_core.pth` nor a relative
`sys.path` entry can shadow it.

| | Unmodified arm (primary) | Modified arm (comparison only) |
|---|---|---|
| Interpreter | `[HOME]]\AppData\Local\r85_stock_venv\Scripts\python.exe` | `<repo>\.venv\Scripts\python.exe` |
| `graphiti_core.__file__` | `...\r85_stock_venv\Lib\site-packages\graphiti_core\__init__.py` | `<repo>\graphiti\graphiti_core\__init__.py` |
| Source | PyPI `graphiti-core==0.28.1` | vendored tree |
| Editable | no | yes |

Verified by running `import graphiti_core; print(graphiti_core.__file__)` in each.

## Pinned stack, unmodified arm

```
graphiti-core==0.28.1
openai==2.24.0
httpx==0.28.1
httpcore==1.0.9
neo4j==6.1.0
pydantic==2.13.5
numpy==2.5.2
tenacity==9.1.4
posthog==7.44.2
python-dotenv==1.2.3
```

**Two pins are deliberate and recorded as `D-R85-3`.** `graphiti-core 0.28.1` declares
`openai>=1.91.0` with no upper bound. A fresh resolve takes `openai 3.6.0`, which has
dropped `httpx` in favour of a different client stack, and `graphiti_core/llm_client/client.py`
imports `httpx` at module scope, so the fresh resolve cannot import at all. `openai` is
pinned to `2.24.0`, the version the modified arm already runs, and `neo4j` to `6.1.0` for
the same reason. Both arms therefore differ only in Graphiti's own code, which is the
comparison the program is for.

## Models

| Role | Identifier | Note |
|---|---|---|
| Extractor, primary | `gpt-4.1-mini-2025-04-14` | Graphiti's documented default tier; the model the study's own extractor uses |
| Extractor, priced comparison | `gpt-4.1-nano-2025-04-14` | persona A only |
| Embedder | `text-embedding-3-small` | Graphiti default |

Both identifiers are confirmed served by the account's model listing. The exact-model
identifier check runs again immediately before the first billed call, and the served
identifier is recorded beside every cost line. Ingestion is routed to OpenAI, never to
Anthropic, following Graphiti's own guidance that its structured-output pipeline is
reliable on OpenAI and Gemini.

## Graph store

A second container, so nothing touches the database the earlier work wrote to.

```
docker run -d --name neo4j-r85 -p 7475:7474 -p 7688:7687 \
  -e NEO4J_AUTH=neo4j/r85graphiti2026 -e NEO4J_server_memory_pagecache_size=512M \
  neo4j:5.26.0
```

Bolt endpoint `bolt://localhost:7688`. The pre-existing `neo4j-graphiti` container on
7474/7687 is left running and untouched.

**Why a second instance rather than a second database.** The image is Neo4j Community
edition, which serves exactly one user database, named `neo4j`. A database name the earlier
work never used is therefore unavailable by `CREATE DATABASE`, and the requirement is met
instead by a fresh instance with a fresh volume. The earlier work wrote everything into the
default `neo4j` database of the other container under group identifiers `full_234` and
`lifemembench_*`, and also wrote `fr_*` property overlays across it. A vendored third-party
benchmark in this repository additionally issues unscoped `MATCH (n) SET ...` statements
against that same default database. None of that can reach the new instance.

Isolation inside the new instance is one group identifier per persona per arm:
`r85stock_<persona>` and `r85fork_<persona>`. These collide with nothing in the historical
set.
