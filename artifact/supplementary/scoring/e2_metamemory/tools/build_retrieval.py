"""
build_retrieval.py -- E2 Amendment 2 STEP 2: the frozen retrieval artifact + its gate.

Runs FR's `lifecycle_search` ONCE per (item, variant) over all 661 FR-Bank items
and writes an immutable, hashed data artifact that all seven policies read.
Retrieval nondeterminism is thereby removed from every policy contrast BY
CONSTRUCTION, not by averaging (E2_AMENDMENT_2 section 1).

Ablated variants are handled by removing the variant's entry ids from a COPY of
the bank and rebuilding its indices BEFORE search, so the removal is invisible to
cosine, BM25, category-forcing and multi-hop alike.

Validation, computed here and written to ABLATION_VALIDATION.md:
  v1  ZERO removal-set entries appear in any ablated retrieval. One appearance is
      contamination and STOPS the run; multi-hop expansion and category-forcing
      are the named suspects.
  v2  FULL-variant gold coverage within 2pp of the r3 probe's 35.6%.
  v3  probe-item retrievals, reported descriptively, no bar.

t_now = max(active.created_at) + 24h. Defaults otherwise. HARD CAP $3.

Usage:  python e2_metamemory/tools/build_retrieval.py
"""

from __future__ import annotations

import asyncio
import collections
import copy
import io
import os
import re
import sys
from datetime import timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e2_common import E1, E2, jdump, jload, load_items, sha        # noqa: E402

BANKS = ROOT / "LifeMemEval" / "artifacts" / "lifecycle_banks"
OUT = E2 / "retrieval_frozen.json"
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


def removal_set(it, cat_plan, slot_abl, catmap, by_persona):
    v = it["variant"]
    if v == "FULL":
        return set()
    if v == "SLOT-ABLATED":
        return set(slot_abl[f"{it['persona']}:{it['question_id']}"])
    cats = set(cat_plan[it["persona"]]["categories"])
    return {e for e in by_persona[it["persona"]] if catmap.get(e) in cats}


async def main():
    for line in io.open(ROOT / ".env", encoding="utf-8", errors="replace"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    from lifecycle_bank import LifecycleBank, lifecycle_search      # noqa: E402
    from openai import AsyncOpenAI                                  # noqa: E402
    from backends import load_backend                               # noqa: E402

    client = Metered(AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"]))
    items = load_items()
    qs = {q["id"]: q for q in jload(ROOT / "LifeMemEval" / "lifemembench_questions.json")}
    cat_plan = jload(E1 / "build" / "variant_plan.json")["cat_ablation"]
    slot_abl = jload(E1 / "build" / "slot_ablations.json")
    catmap, by_persona = {}, collections.defaultdict(list)
    for r in load_backend("frbank"):
        catmap[r["entry_id"]] = r["category"]
        by_persona[r["persona"]].append(r["entry_id"])

    banks, t_nows = {}, {}
    for p in sorted({i["persona"] for i in items}):
        b = LifecycleBank.load(BANKS / p)
        banks[p] = b
        act = b.active_entries()
        t_nows[p] = max(e.created_at for e in act) + timedelta(hours=24)
    print(f"{len(items)} items over {len(banks)} personas", flush=True)

    sem = asyncio.Semaphore(CONC)
    rows, done = [], [0]

    async def one(it):
        rm = removal_set(it, cat_plan, slot_abl, catmap, by_persona)
        async with sem:
            b = banks[it["persona"]]
            if rm:
                b = copy.copy(b)
                b.entries = {k: v for k, v in banks[it["persona"]].entries.items()
                             if k not in rm}
                b._rebuild()
            res = await lifecycle_search(it["question"], b, t_nows[it["persona"]],
                                         client, multihop=True, skip_distill=False)
        facts = [c[0].fact for c in res]
        eids = [c[0].uuid for c in res]
        blended = [float(c[3]) for c in res]
        leak = sorted(set(eids) & rm)
        ca = (qs.get(it["question_id"], {}) or {}).get("correct_answer") or ""
        done[0] += 1
        if done[0] % 50 == 0:
            print(f"  {done[0]}/{len(items)}  ${client.usd:.4f}", flush=True)
        return {"item_id": it["item_id"], "persona": it["persona"],
                "question_id": it["question_id"], "variant": it["variant"],
                "label": it["label_final"], "split": it["split"],
                "n_removed": len(rm), "n_facts": len(facts),
                "facts": facts, "entry_ids": eids, "blended": blended,
                "max_blended": max(blended) if blended else 0.0,
                "leaked_entry_ids": leak,
                "gold_coverage": coverage(ca, facts) if ca else None,
                "facts_sha256": sha(*facts)}

    try:
        rows = list(await asyncio.gather(*(one(i) for i in items)))
    except RuntimeError as e:
        print(f"STOP: {e}")
        return

    # ------------------------------------------------------------ validation
    ablated = [r for r in rows if r["n_removed"] > 0]
    leaks = [r for r in ablated if r["leaked_entry_ids"]]
    full_canon = [r for r in rows
                  if r["variant"] == "FULL" and r["gold_coverage"] is not None]
    cov_full = sum(1 for r in full_canon if r["gold_coverage"] >= 0.5) / max(len(full_canon), 1)
    probes = [r for r in rows if str(r["question_id"]).startswith("probe")]
    v1 = not leaks
    v2 = abs(cov_full - 0.356) <= 0.02

    jdump({"immutable": True,
           "substrate": "lifecycle_search (lifecycle_bank.py), fresh, defaults, "
                        "t_now = max(active.created_at)+24h",
           "n_items": len(rows), "usd": client.usd,
           "emb_calls": client.emb, "chat_calls": client.chat_n,
           "artifact_sha256": sha(*[r["facts_sha256"] for r in sorted(
               rows, key=lambda x: x["item_id"])]),
           "validation": {"v1_zero_leak": v1, "v1_n_ablated": len(ablated),
                          "v1_n_leaking": len(leaks),
                          "v2_full_coverage": cov_full, "v2_probe_ref": 0.356,
                          "v2_pass": v2, "v3_n_probes": len(probes)},
           "rows": rows}, OUT)

    by_var = collections.Counter(r["variant"] for r in rows)
    zero = sum(1 for r in rows if r["n_facts"] == 0)
    print("\n" + "=" * 88)
    print(f"RETRIEVAL ARTIFACT  {len(rows)} items  {dict(by_var)}  ${client.usd:.4f}")
    print(f"  items returning zero facts: {zero}")
    print(f"v1 ZERO LEAK      {'PASS' if v1 else 'FAIL'} — "
          f"{len(leaks)}/{len(ablated)} ablated retrievals contain a removed entry")
    if leaks:
        for r in leaks[:5]:
            print(f"    {r['item_id']} variant={r['variant']} "
                  f"leaked={r['leaked_entry_ids'][:3]}")
    print(f"v2 FULL COVERAGE  {'PASS' if v2 else 'FAIL'} — {cov_full:.1%} "
          f"vs probe 35.6% (bar: within 2pp)  n={len(full_canon)}")
    print(f"v3 PROBES         {len(probes)} probe items, descriptive:")
    if probes:
        nf = [r["n_facts"] for r in probes]
        mb = [r["max_blended"] for r in probes]
        nonp = [r["max_blended"] for r in rows if r["label"] != "ABSENT"]
        print(f"    facts returned: mean {sum(nf)/len(nf):.2f}, "
              f"zero-fact {sum(1 for x in nf if x == 0)}/{len(nf)}")
        print(f"    max blended on probes: mean {sum(mb)/len(mb):.4f}")
        print(f"    max blended on non-ABSENT: mean {sum(nonp)/len(nonp):.4f}")
    print(f"\nwrote {OUT.name}")


if __name__ == "__main__":
    asyncio.run(main())
