"""
r3_probe.py -- E2 Amendment 1 STEP 1: is FR's retrieval runnable AND comparable?

Runs FR's own `lifecycle_search` FRESH on the FULL-slice overlap and measures it
against the two cached retrieval artifacts, plus a determinism repeat. Answers
r1/r2/r3 with numbers rather than inspection.

  r1 runnable   does it import, load an E2 store snapshot, and return facts
  r2 determinism  same query twice -> same fact set? (the pipeline contains an
                  LLM distillation step at temperature 0, so this is measured)
  r3 comparability  fresh vs cached item-level agreement, and gold coverage
                  within 5pp of the cached 23.8%

TWO cached artifacts are compared, not one, because they are already known to
disagree with each other: `analysis/abstention_pricing/common.py` records that
`fr_bank_results.json` top5_facts does NOT correspond to the context actually fed
to the answerer (`e2e_responses.json[gpt54_nr][qid]['fr_bank_facts']`), median
overlap 0 facts. Whichever one fresh retrieval matches, if either, is the finding.

t_now follows the canonical LCB driver exactly: max(active.created_at) + 24h,
which is also E1's pinned t_now. Defaults otherwise (multihop=True,
skip_distill=False, temporal_query=False, include_inactive=False).

HARD CAP $0.50. Zero Anthropic calls. Zero eval-item ANSWERS -- this touches
retrieval only, and reports no credit, confabulation or policy score.

Usage:  python e2_metamemory/tools/r3_probe.py [--n 60]
"""

from __future__ import annotations

import asyncio
import collections
import io
import json
import os
import random
import re
import sys
from datetime import timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e2_common import E2, jdump, jload, load_items                # noqa: E402

BANKS = ROOT / "LifeMemEval" / "artifacts" / "lifecycle_banks"
QUESTIONS = ROOT / "LifeMemEval" / "lifemembench_questions.json"
STORED_A = ROOT / "LifeMemEval" / "artifacts" / "fr_bank_results.json"
STORED_B = ROOT / "LifeMemEval" / "artifacts" / "e2e_responses.json"
CAP_USD = 0.50
SEED = 42
STOP = set("the a an of and or to in for is are was were with on at by my i you user "
           "their they them this that it its".split())


def toks(s):
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower())
            if w not in STOP and len(w) > 2}


def coverage(gold, facts):
    g = toks(gold)
    if not g or not facts:
        return 0.0
    return max(len(g & toks(str(f))) / len(g) for f in facts)


class Metered:
    """Wraps AsyncOpenAI, meters spend, raises past the cap."""

    def __init__(self, inner):
        self._i = inner
        self.usd = 0.0
        self.emb = 0
        self._chat_n = 0

    def __getattr__(self, k):
        return getattr(self._i, k)

    @property
    def embeddings(self):
        outer = self

        class E:
            async def create(self, **kw):
                r = await outer._i.embeddings.create(**kw)
                outer.emb += 1
                outer.usd += r.usage.total_tokens / 1e6 * 0.02
                outer._guard()
                return r
        return E()

    @property
    def chat(self):
        outer = self

        class C:
            class completions:
                @staticmethod
                async def create(**kw):
                    r = await outer._i.chat.completions.create(**kw)
                    outer._chat_n += 1
                    outer.usd += (r.usage.prompt_tokens / 1e6 * 0.40
                                  + r.usage.completion_tokens / 1e6 * 1.60)
                    outer._guard()
                    return r
        return C()

    def _guard(self):
        if self.usd > CAP_USD:
            raise RuntimeError(f"r3 probe cap ${CAP_USD} exceeded (${self.usd:.4f})")


async def main():
    n_want = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 60
    for line in io.open(ROOT / ".env", encoding="utf-8", errors="replace"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

    sys.path.insert(0, str(ROOT))
    from lifecycle_bank import LifecycleBank, lifecycle_search    # noqa: E402
    from openai import AsyncOpenAI                                # noqa: E402

    client = Metered(AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"]))

    qs = {q["id"]: q for q in jload(QUESTIONS)}
    stored_a = {r["question_id"]: r for r in
                jload(STORED_A)["per_question"]["fr_bank"]}
    stored_b = jload(STORED_B)["gpt54_nr"]

    # FULL-slice overlap: FR-Bank FULL-variant E2 items whose question is canonical
    cand = [i for i in load_items()
            if i["variant"] == "FULL" and i["question_id"] in qs]
    by_av = collections.defaultdict(list)
    for i in cand:
        by_av[qs[i["question_id"]]["attack_vector"]].append(i)
    rng = random.Random(SEED)
    picks = []
    for av in sorted(by_av):
        pool = sorted(by_av[av], key=lambda x: x["item_id"])
        take = max(1, round(n_want * len(pool) / len(cand)))
        picks.extend(rng.sample(pool, min(take, len(pool))))
    picks = sorted(picks, key=lambda x: x["item_id"])[:n_want]
    print(f"FULL-slice overlap {len(cand)} items; probing {len(picks)} "
          f"stratified across {len(by_av)} AVs")

    bankcache, rows = {}, []
    for n, it in enumerate(picks, 1):
        p = it["persona"]
        if p not in bankcache:
            bankcache[p] = LifecycleBank.load(BANKS / p)
        bank = bankcache[p]
        active = bank.active_entries()
        if not active:
            continue
        t_now = max(e.created_at for e in active) + timedelta(hours=24)
        try:
            r1 = await lifecycle_search(it["question"], bank, t_now, client,
                                        multihop=True, skip_distill=False)
        except RuntimeError as e:
            print(f"STOP: {e}")
            break
        f1 = [c[0].fact for c in r1]
        rep = None
        if n <= 10:                                   # r2: determinism repeat
            r2 = await lifecycle_search(it["question"], bank, t_now, client,
                                        multihop=True, skip_distill=False)
            rep = [c[0].fact for c in r2]
        qa = qs[it["question_id"]]
        ca = qa.get("correct_answer") or ""
        sa = [f.get("fact") for f in (stored_a.get(it["question_id"], {})
                                      .get("top5_facts") or [])]
        sb = stored_b.get(it["question_id"], {}).get("fr_bank_facts") or []
        rows.append({
            "item_id": it["item_id"], "question_id": it["question_id"],
            "attack_vector": qa["attack_vector"], "label": it["label_final"],
            "n_fresh": len(f1), "n_stored_a": len(sa), "n_stored_b": len(sb),
            "cov_fresh": coverage(ca, f1), "cov_stored_a": coverage(ca, sa),
            "cov_stored_b": coverage(ca, sb),
            "jaccard_fresh_a": _j(f1, sa), "jaccard_fresh_b": _j(f1, sb),
            "jaccard_a_b": _j(sa, sb),
            "top1_match_a": bool(f1 and sa and f1[0].strip() == str(sa[0]).strip()),
            "top1_match_b": bool(f1 and sb and f1[0].strip() == str(sb[0]).strip()),
            "repeat_identical": (None if rep is None else rep == f1),
        })
        if n % 10 == 0:
            print(f"  {n}/{len(picks)}  ${client.usd:.4f}", flush=True)

    def frac(key, thr=0.5):
        v = [r[key] for r in rows]
        return sum(1 for x in v if x >= thr) / max(len(v), 1)

    reps = [r["repeat_identical"] for r in rows if r["repeat_identical"] is not None]
    res = {
        "n_probed": len(rows), "usd": client.usd,
        "emb_calls": client.emb, "chat_calls": client._chat_n,
        "r1_runnable": len(rows) > 0,
        "r2_determinism": {"n_repeats": len(reps),
                           "identical": sum(1 for x in reps if x),
                           "rate": (sum(1 for x in reps if x) / len(reps)) if reps else None},
        "r3": {
            "gold_coverage_ge50": {"fresh": frac("cov_fresh"),
                                   "stored_a_fr_bank_results": frac("cov_stored_a"),
                                   "stored_b_e2e_fed_context": frac("cov_stored_b")},
            "mean_jaccard": {"fresh_vs_a": _m(rows, "jaccard_fresh_a"),
                             "fresh_vs_b": _m(rows, "jaccard_fresh_b"),
                             "a_vs_b": _m(rows, "jaccard_a_b")},
            "top1_match_rate": {"fresh_vs_a": _m(rows, "top1_match_a"),
                                "fresh_vs_b": _m(rows, "top1_match_b")},
        },
        "rows": rows,
    }
    jdump(res, E2 / "r3_probe.json")
    r = res["r3"]
    print("\n" + "=" * 88)
    print(f"r1 RUNNABLE: {res['r1_runnable']}  ({len(rows)} items returned facts)")
    d = res["r2_determinism"]
    print(f"r2 DETERMINISM: {d['identical']}/{d['n_repeats']} repeats identical")
    print("r3 COMPARABILITY")
    print(f"  gold coverage >=50%:  fresh {r['gold_coverage_ge50']['fresh']:.1%} | "
          f"cached A (fr_bank_results) {r['gold_coverage_ge50']['stored_a_fr_bank_results']:.1%} | "
          f"cached B (fed context) {r['gold_coverage_ge50']['stored_b_e2e_fed_context']:.1%}")
    print(f"  mean fact-set Jaccard: fresh~A {r['mean_jaccard']['fresh_vs_a']:.3f} | "
          f"fresh~B {r['mean_jaccard']['fresh_vs_b']:.3f} | A~B {r['mean_jaccard']['a_vs_b']:.3f}")
    print(f"  top-1 exact match:     fresh~A {r['top1_match_rate']['fresh_vs_a']:.1%} | "
          f"fresh~B {r['top1_match_rate']['fresh_vs_b']:.1%}")
    print(f"  spend ${client.usd:.4f} of ${CAP_USD}")
    print(f"wrote r3_probe.json")


def _j(a, b):
    sa, sb = {str(x).strip() for x in a}, {str(x).strip() for x in b}
    return len(sa & sb) / len(sa | sb) if (sa or sb) else 0.0


def _m(rows, k):
    v = [float(r[k]) for r in rows]
    return sum(v) / max(len(v), 1)


if __name__ == "__main__":
    asyncio.run(main())
