# -*- coding: utf-8 -*-
"""repro_mem0_erase.py -- minimal reproduction of the Mem0 census row of Table 2 (the 'erase' finding), from the frozen Mem0 banks.

Finding: at the retrieval surface we evaluated (mem0ai 1.0.5; the `search` and `get_all` surface, read here through the same Qdrant
collection those calls return from), 12.7% of the 10,074 stored points carry `updated_at` and nothing else records a revision: an UPDATE
rewrites the payload in place, keeping `created_at` and stamping `updated_at`, so the prior value is not in the store. The per-memory
history call was not consulted (it reads a separate, shared history database that is not part of the frozen artifact).

Reads LifeMemEval/artifacts/mem0_41mini_banks (copied first: the frozen directory carries a Qdrant lock file). Prints the payload keys, the
point count, the count and share of points carrying `updated_at`, and checks every such point has updated_at > created_at. No API call.
Expected (e1_metamemory/NUMBERS.md AUX-BELIEVED-MEM0; BELIEVED_STATE.md): 10,074 points; 1,276 (12.7%) carry updated_at.
Usage: python e1_metamemory/tools/repro_mem0_erase.py
"""
from __future__ import annotations

import collections
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEM0_DIR = ROOT / "LifeMemEval" / "artifacts" / "mem0_41mini_banks"
COLLECTION = "mem0_41mini"


def main():
    from qdrant_client import QdrantClient
    dst = Path(tempfile.mkdtemp(prefix="repro_mem0_")) / "banks"
    shutil.copytree(MEM0_DIR, dst)
    c = QdrantClient(path=str(dst))
    n = 0; with_updated = 0; bad_order = 0; keys = collections.Counter(); off = None
    while True:
        batch, off = c.scroll(COLLECTION, limit=2000, offset=off, with_payload=True, with_vectors=False)
        for pt in batch:
            pl = pt.payload or {}
            n += 1
            for k in pl:
                keys[k] += 1
            if pl.get("updated_at") is not None:
                with_updated += 1
                if not (str(pl["updated_at"]) > str(pl.get("created_at", ""))):
                    bad_order += 1
        if off is None:
            break
    del c
    shutil.rmtree(dst.parent, ignore_errors=True)
    print(f"points: {n:,}")
    print("payload keys:", ", ".join(sorted(keys)))
    print(f"points carrying updated_at: {with_updated:,} ({100 * with_updated / n:.1f}%); updated_at <= created_at on {bad_order} of them")
    print("lifecycle fields (category, slot, event time, retraction, supersedes):", "none" if not any(k in keys for k in ("category", "slot", "event_time", "retracted", "supersedes")) else "present")
    ok = n == 10074 and with_updated == 1276
    print("matches the printed row (10,074; 1,276 = 12.7%):", ok)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
