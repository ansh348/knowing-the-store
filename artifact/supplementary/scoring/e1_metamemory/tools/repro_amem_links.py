# -*- coding: utf-8 -*-
"""repro_amem_links.py -- minimal reproduction of the A-MEM census row of Table 2 (the 'invent' finding), from the frozen A-MEM banks.

Finding: in our integration of A-MEM (the `agentic-memory` package, version 0.0.1, github.com/agiresearch/A-mem), every link reference the
notes carry resolves to no note identifier: the distinct link values are the empty string, "0" to "5" and "memory index:0" to "memory
index:5", positional indices into an ephemeral neighbour list. Over the 40 scored personas: 11,319 notes, 23,186 link references, 0
resolving to a note id (the broken `priya.canary` bank is excluded everywhere in the study).

Reads each bank's chroma.sqlite3 read-only and immutable (chromadb writes on open; sqlite does not), the `embedding_metadata` rows whose
key is `id` or `links`, parses each `links` value as JSON, and checks every reference against the note ids of the persona and of the whole
corpus. No API call. Expected (reviews/NUMBERS_R86.md AUX-R86-AMEM-LINKS): 11,319 notes, 23,186 references, 0 resolving.
Usage: python e1_metamemory/tools/repro_amem_links.py
"""
from __future__ import annotations

import collections
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AMEM_DIR = ROOT / "LifeMemEval" / "artifacts" / "amem_banks"
EXCLUDE = {"priya.canary"}


def main():
    notes = 0; refs = 0; resolved_local = 0; values = collections.Counter(); per_persona = {}
    all_ids = set(); all_refs = []
    for d in sorted(AMEM_DIR.iterdir()):
        if not d.is_dir() or d.name in EXCLUDE or not (d / "chroma.sqlite3").exists():
            continue
        con = sqlite3.connect(f"file:{d / 'chroma.sqlite3'}?mode=ro&immutable=1", uri=True)
        rows = con.execute("select id, key, string_value from embedding_metadata where key in ('id','links')").fetchall()
        con.close()
        by = collections.defaultdict(dict)
        for rid, k, v in rows:
            by[rid][k] = v
        ids = {m.get("id") or str(rid) for rid, m in by.items()}
        all_ids |= ids
        n_here = 0
        for rid, m in by.items():
            notes += 1
            links = m.get("links")
            if not links:
                continue
            try:
                lst = json.loads(links)
            except json.JSONDecodeError:
                lst = [links]
            for x in lst:
                refs += 1; n_here += 1; values[str(x)] += 1; all_refs.append(str(x))
                if str(x) in ids:
                    resolved_local += 1
        per_persona[d.name] = (len(by), n_here)
    resolved_global = sum(1 for x in all_refs if x in all_ids)
    print(f"banks (personas): {len(per_persona)}; notes: {notes:,}; link references: {refs:,}")
    print(f"references resolving to a note id: within the persona {resolved_local}, anywhere in the corpus {resolved_global}")
    print("distinct link values:", ", ".join(repr(v) for v in sorted(values)))
    ok = notes == 11319 and refs == 23186 and resolved_local == 0 and resolved_global == 0
    print("matches the printed row (11,319 notes; 23,186 references; 0 resolving):", ok)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
