"""
backends.py -- normalized read-only access to the three memory stores.

NO API CALLS. Frozen artifacts are NEVER opened in place when the reader can
write: Mem0 is copied to the scratchpad before QdrantClient touches it, and A-MEM
is read through sqlite in `mode=ro&immutable=1` because chromadb writes to
chroma.sqlite3 merely by opening it.

Normalized entry shape, common to all three backends:

    {backend, persona, entry_id, text, session_id, ingest_time, recency_time,
     category, slot, believed_superseded, believed_retracted, believed_supersedes,
     event_time}

Fields a backend cannot express are None -- never 0 and never False. A zero is the
claim "there are none of these", which is false for A-MEM supersession and
unknowable for Mem0. Downstream renderers must distinguish None from 0.

Two fields carry the same meaning across stores and are therefore normalized here
rather than in any renderer:

  recency_time  the store's OWN claim about when an entry's content is from, i.e.
                the field each store uses to date its content, ISO-8601 UTC:
                  FR-Bank  created_at   (the LifecycleBench session date)
                  Mem0     payload.date (the session date; rewritten to the
                                         update-time session on the 12.7% of
                                         points that carry updated_at)
                  A-MEM    timestamp    (the LifecycleBench session date,
                                         35 distinct values per persona)
                `ingest_time` is NOT this: on Mem0 and A-MEM it is the ingest
                wall-clock (a single afternoon in 2026-05 for the whole corpus),
                so an age taken against a session-date t_now would be an
                instrument error rather than a believed-state finding.

  believed_supersedes  whether the store itself records this entry as superseding
                an earlier one (FR-Bank `supersedes` pointer). Mem0's updated_at
                is already carried as believed_superseded and points at nothing;
                A-MEM's `links` resolve to 0 note ids and are never used.

Usage:
    python e1_metamemory/tools/backends.py            # build the cache, print census
    from backends import load_backend                 # -> list[dict]
"""

from __future__ import annotations

import collections
import json
import io
import os
import shutil
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
LME = PROJECT_ROOT / "LifeMemEval"
FR_BANKS = LME / "artifacts" / "lifecycle_banks"
MEM0_DIR = LME / "artifacts" / "mem0_41mini_banks"
AMEM_DIR = LME / "artifacts" / "amem_banks"
CACHE = E1 / "backend_entries"

SCRATCH = Path(os.environ.get(
    "E1_SCRATCH",
    r"[HOME]]\AppData\Local\Temp\claude"
    r"\C--Users-[AUTHOR-1]-[PROJECTS-DIR]-[REPO-DIR]"
    r"\fac3a932-65ae-4ad7-8afd-a574792e1fff\scratchpad"))

# priya.canary is a broken A-MEM bank: sidecar claims 293 notes, store holds 101.
AMEM_EXCLUDE = {"priya.canary"}

BACKENDS = ("frbank", "mem0", "amem")


def _n(backend, persona, eid, text, **kw):
    d = {"backend": backend, "persona": persona, "entry_id": eid, "text": text,
         "session_id": None, "ingest_time": None, "recency_time": None,
         "category": None, "slot": None,
         "believed_superseded": None, "believed_retracted": None,
         "believed_supersedes": None, "event_time": None}
    d.update(kw)
    return d


def _iso_compact(v):
    """A-MEM stores 'YYYYMMDDHHMM' with no separators; normalize to ISO-8601 UTC."""
    s = str(v or "")
    if len(s) != 12 or not s.isdigit():
        return None
    return f"{s[0:4]}-{s[4:6]}-{s[6:8]}T{s[8:10]}:{s[10:12]}:00+00:00"


# ------------------------------------------------------------------- FR-Bank
def read_frbank():
    out = []
    for p in sorted(FR_BANKS.glob("*.json")):
        persona = p.stem
        for e in json.load(io.open(p, encoding="utf-8"))["entries"]:
            sk = e.get("slot_key")
            out.append(_n("frbank", persona, e["id"], e.get("text", ""),
                          session_id=e.get("source_session"),
                          ingest_time=e.get("created_at"),
                          recency_time=e.get("created_at"),
                          category=e.get("category"),
                          slot=(str(sk[1]) if isinstance(sk, list) and len(sk) >= 2 else None),
                          believed_superseded=(not e.get("is_active")),
                          believed_retracted=bool(e.get("is_retracted")),
                          believed_supersedes=bool(e.get("supersedes")),
                          event_time=e.get("event_time")))
    return out


# ---------------------------------------------------------------------- Mem0
def read_mem0():
    """Qdrant on-disk. MUST be opened on a copy -- the frozen dir carries a .lock."""
    dst = SCRATCH / "e1_mem0_copy"
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(MEM0_DIR, dst)
    from qdrant_client import QdrantClient
    c = QdrantClient(path=str(dst))
    out, off = [], None
    while True:
        batch, off = c.scroll("mem0_41mini", limit=2000, offset=off,
                              with_payload=True, with_vectors=False)
        for pt in batch:
            pl = pt.payload or {}
            out.append(_n("mem0", pl.get("user_id"), str(pt.id), pl.get("data", ""),
                          session_id=pl.get("session_id"),
                          ingest_time=pl.get("created_at"),
                          # `date` is the session date the store attaches to the
                          # content; created_at is the ingest wall-clock and is
                          # the same afternoon for all 10,074 points.
                          recency_time=pl.get("date"),
                          # category / slot / event_time: NOT EXPRESSIBLE -> stay None
                          # updated_at is the ONLY supersession signal Mem0 retains, and it
                          # is a bare boolean: the prior value is destroyed in place.
                          believed_superseded=(pl.get("updated_at") is not None)))
        if off is None:
            break
    del c
    return out


# ---------------------------------------------------------------------- A-MEM
def read_amem():
    """Chroma sqlite, read-only + immutable. chromadb WRITES on open; sqlite does not."""
    out = []
    for d in sorted(AMEM_DIR.iterdir()):
        if not d.is_dir() or d.name in AMEM_EXCLUDE:
            continue
        db = d / "chroma.sqlite3"
        if not db.exists():
            continue
        con = sqlite3.connect(f"file:{db}?mode=ro&immutable=1", uri=True)
        rows = con.execute(
            "select id, key, string_value from embedding_metadata "
            "where key in ('content','timestamp','last_accessed','id')").fetchall()
        con.close()
        by = collections.defaultdict(dict)
        for rid, k, v in rows:
            by[rid][k] = v
        for rid, m in by.items():
            out.append(_n("amem", d.name, m.get("id") or str(rid), m.get("content", ""),
                          session_id=None,          # timestamp is the session DATE, not an id
                          ingest_time=_iso_compact(m.get("last_accessed")),
                          recency_time=_iso_compact(m.get("timestamp"))))
            # category: stored but constant 'Uncategorized' -> NOT EXPRESSIBLE, stays None
            # supersession/retraction/expiry: no field exists; `links` resolve to 0 note ids
    return out


READERS = {"frbank": read_frbank, "mem0": read_mem0, "amem": read_amem}


def load_backend(name, rebuild=False):
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"{name}.json"
    if p.exists() and not rebuild:
        return json.load(io.open(p, encoding="utf-8"))
    rows = READERS[name]()
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rows, f, ensure_ascii=False)
        f.write("\n")
    return rows


def main():
    census = {}
    for b in BACKENDS:
        rows = load_backend(b, rebuild="--rebuild" in sys.argv)
        per = collections.Counter(r["persona"] for r in rows)
        expressible = {k: sum(1 for r in rows if r[k] is not None)
                       for k in ("session_id", "ingest_time", "recency_time",
                                 "category", "slot", "believed_superseded",
                                 "believed_retracted", "believed_supersedes",
                                 "event_time")}
        census[b] = {"entries": len(rows), "personas": len(per),
                     "min_per_persona": min(per.values()), "max_per_persona": max(per.values()),
                     "field_non_null": expressible}
        print("=" * 84)
        print(f"{b.upper()}  entries {len(rows)}  personas {len(per)}  "
              f"per-persona {min(per.values())}-{max(per.values())}")
        for k, v in expressible.items():
            mark = "NOT EXPRESSIBLE" if v == 0 else f"{v} ({v/len(rows):.0%})"
            print(f"    {k:22s} {mark}")
    with io.open(E1 / "backend_census.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump({"census": census, "amem_excluded": sorted(AMEM_EXCLUDE),
                   "no_api_calls": True}, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(f"\nwrote {E1/'backend_census.json'} and {CACHE}/*.json")


if __name__ == "__main__":
    main()
