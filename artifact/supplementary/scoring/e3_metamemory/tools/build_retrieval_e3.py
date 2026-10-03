"""
build_retrieval_e3.py -- the frozen retrieval-and-store artifact, one state per rung.

Runs FR's `lifecycle_search` ONCE per registered (item, rung) cell and writes an
immutable, hashed data artifact that every arm reads. Retrieval nondeterminism is
removed from every arm contrast BY CONSTRUCTION, exactly as E2_AMENDMENT_2 did it
for E2 -- retrieval-as-data.

THE STORE AT A RUNG IS BUILT TWICE-CORRECTLY (D51-E3):
  membership  entries with source_session <= rung, and no others;
  state       is_active RECOMPUTED at the rung from the `supersedes` pointer.
              The bank's own is_active records the store's FINAL state, so
              reusing it would let a session-30 supersession suppress an entry
              during a rung-14 retrieval -- future information changing a past
              store's behaviour. Entries are rebuilt with dataclasses.replace so
              the committed bank objects are never mutated.

t_now at rung s is session s's own date + 24h.

Validation, computed here:
  v1  NO entry with source_session > rung appears in any rung-s retrieval.
      One appearance is contamination and STOPS the run.
  v2  NESTING of the retrieval pools: the candidate pool at rung s1 is a subset
      of the pool at s2 > s1, per persona.
  v3  gold coverage at the terminal rung, reported against E2's FULL-variant
      0.354 for continuity. Descriptive, no bar -- E3's store is not E2's.

HARD CAP $3 on this phase.

Usage:  python e3_metamemory/tools/build_retrieval_e3.py
"""

from __future__ import annotations

import asyncio
import collections
import dataclasses
import io
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e3_common import E3, RUNGS, Snapshot, jdump, jload, load_cells, session_dates, sha  # noqa: E402

BANKS = ROOT / "LifeMemEval" / "artifacts" / "lifecycle_banks"
OUT = E3 / "retrieval_frozen_e3.json"
CAP_USD = 3.00
CONC = 6
STOP_W = set("the a an of and or to in for is are was were with on at by my i you user "
             "their they them this that it its".split())


def toks(s):
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower())
            if w not in STOP_W and len(w) > 2}


def coverage(gold, facts):
    g = toks(gold)
    if not g or not facts:
        return 0.0
    return max(len(g & toks(str(f))) / len(g) for f in facts)


class Metered:
    def __init__(self, inner):
        self._i, self.usd, self.emb, self.chat_n = inner, 0.0, 0, 0

    def __getattr__(self, k):
        return getattr(self._i, k)

    @property
    def embeddings(self):
        o = self

        class E:
            async def create(self, **kw):
                r = await o._i.embeddings.create(**kw)
                o.emb += 1
                o.usd += r.usage.total_tokens / 1e6 * 0.02
                o._g()
                return r
        return E()

    @property
    def chat(self):
        o = self

        class C:
            class completions:
                @staticmethod
                async def create(**kw):
                    r = await o._i.chat.completions.create(**kw)
                    o.chat_n += 1
                    o.usd += (r.usage.prompt_tokens / 1e6 * 0.40
                              + r.usage.completion_tokens / 1e6 * 1.60)
                    o._g()
                    return r
        return C()

    def _g(self):
        if self.usd > CAP_USD:
            raise RuntimeError(f"retrieval cap ${CAP_USD} exceeded (${self.usd:.4f})")


async def main():
    for line in io.open(ROOT / ".env", encoding="utf-8", errors="replace"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    from lifecycle_bank import LifecycleBank, lifecycle_search       # noqa: E402
    from openai import AsyncOpenAI                                   # noqa: E402

    client = Metered(AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"]))
    cells = load_cells()["cells"]
    qs = {q["id"]: q for q in jload(ROOT / "LifeMemEval" / "lifemembench_questions.json")}
    dates = session_dates()
    personas = sorted({c["persona"] for c in cells})
    snaps = {p: Snapshot(p, dates[p]) for p in personas}

    base = {p: LifecycleBank.load(BANKS / p) for p in personas}
    print(f"{len(cells)} cells over {len(personas)} personas x {len(RUNGS)} rungs",
          flush=True)

    # ---- one rung-correct bank per (persona, rung), built once and shared
    banks, pools = {}, {}
    for p in personas:
        S = snaps[p]
        for r in RUNGS:
            alive = S.alive(r)
            b = LifecycleBank.__new__(LifecycleBank)
            b.__dict__.update(base[p].__dict__)
            b.entries = {}
            for eid in alive:
                e = base[p].entries[eid]
                b.entries[eid] = dataclasses.replace(
                    e, is_active=S.is_active_at(eid, r))
            b._rebuild()
            banks[(p, r)] = b
            pools[(p, r)] = set(alive)

    # ---- v2 nesting of the pools
    v2_bad = []
    for p in personas:
        for a, bq in zip(RUNGS, RUNGS[1:]):
            if not pools[(p, a)] <= pools[(p, bq)]:
                v2_bad.append((p, a, bq))
    assert not v2_bad, f"v2 pool nesting failed: {v2_bad[:3]}"
    print(f"v2 pool nesting over {RUNGS}: PASS ({len(personas)} personas)", flush=True)

    sem = asyncio.Semaphore(CONC)
    done = [0]

    async def one(c):
        p, r = c["persona"], c["rung"]
        async with sem:
            res = await lifecycle_search(c["question"], banks[(p, r)],
                                         snaps[p].t_now(r), client,
                                         multihop=True, skip_distill=False)
        facts = [x[0].fact for x in res]
        eids = [x[0].uuid for x in res]
        blended = [float(x[3]) for x in res]
        leak = sorted(e for e in eids if e not in pools[(p, r)])
        ca = (qs.get(c["question_id"], {}) or {}).get("correct_answer") or ""
        done[0] += 1
        if done[0] % 100 == 0:
            print(f"  {done[0]}/{len(cells)}  ${client.usd:.4f}", flush=True)
        return {"cell_id": c["cell_id"], "persona": p, "rung": r,
                "question_id": c["question_id"], "label": c["label"],
                "split": c["split"], "kind": c["kind"],
                "n_alive": len(pools[(p, r)]), "n_facts": len(facts),
                "facts": facts, "entry_ids": eids, "blended": blended,
                "max_blended": max(blended) if blended else 0.0,
                "leaked_entry_ids": leak,
                "gold_coverage": coverage(ca, facts) if ca else None,
                "facts_sha256": sha(*facts)}

    try:
        rows = list(await asyncio.gather(*(one(c) for c in cells)))
    except RuntimeError as e:
        print(f"STOP: {e}")
        return

    leaks = [r for r in rows if r["leaked_entry_ids"]]
    v1 = not leaks
    term = [r for r in rows if r["rung"] == RUNGS[-1]
            and r["kind"] == "authored" and r["gold_coverage"] is not None]
    cov_term = sum(1 for r in term if r["gold_coverage"] >= 0.5) / max(len(term), 1)

    per_rung_sha = {}
    for r in RUNGS:
        sub = sorted((x for x in rows if x["rung"] == r), key=lambda x: x["cell_id"])
        per_rung_sha[str(r)] = sha(*[x["facts_sha256"] for x in sub])
    art = sha(*[per_rung_sha[str(r)] for r in RUNGS])

    jdump({"immutable": True,
           "substrate": "lifecycle_search (lifecycle_bank.py), fresh, defaults; "
                        "store = {e : source_session(e) <= rung} with is_active "
                        "recomputed at the rung from the supersedes pointer "
                        "(D51-E3); t_now = session(rung).date + 24h",
           "rungs": list(RUNGS), "n_cells": len(rows), "usd": client.usd,
           "emb_calls": client.emb, "chat_calls": client.chat_n,
           "per_rung_sha256": per_rung_sha, "artifact_sha256": art,
           "validation": {"v1_zero_future_leak": v1, "v1_n_leaking": len(leaks),
                          "v2_pool_nesting": True,
                          "v3_terminal_gold_coverage": cov_term,
                          "v3_e2_full_reference": 0.354},
           "rows": rows}, OUT)

    zero = sum(1 for r in rows if r["n_facts"] == 0)
    print("\n" + "=" * 92)
    print(f"E3 RETRIEVAL ARTIFACT  {len(rows)} cells  ${client.usd:.4f}  "
          f"({client.emb} emb, {client.chat_n} chat)")
    print("=" * 92)
    print(f"  artifact sha256 {art[:32]}...")
    for r in RUNGS:
        sub = [x for x in rows if x["rung"] == r]
        print(f"  rung {r:>2d}: {len(sub):4d} cells  mean facts "
              f"{sum(x['n_facts'] for x in sub)/len(sub):.2f}  "
              f"mean pool {sum(x['n_alive'] for x in sub)/len(sub):.0f}  "
              f"sha {per_rung_sha[str(r)][:16]}...")
    print(f"  cells returning zero facts: {zero}")
    print(f"v1 ZERO FUTURE LEAK  {'PASS' if v1 else 'FAIL'} "
          f"({len(leaks)} cells leaked an entry from a later session)")
    print(f"v2 POOL NESTING      PASS")
    print(f"v3 terminal-rung gold coverage {cov_term:.3f} "
          f"(E2 FULL-variant reference 0.354; descriptive, no bar)")
    if not v1:
        raise SystemExit("STOP: future-session contamination in the retrieval artifact")
    print(f"\nwrote {OUT.name}")


if __name__ == "__main__":
    asyncio.run(main())
