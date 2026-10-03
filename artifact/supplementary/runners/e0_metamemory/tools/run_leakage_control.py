"""
run_leakage_control.py -- E0 Step 3: the index-leakage control.

Pre-registered (PREREG_E0.md §9): sample 30 PRESENT items (seed 42), show the model
ONLY the index and the question, and instruct it to answer. If MORE THAN 3 of 30
are answered correctly, the index leaks answer content -- stop, descend one level
of the tightening ladder, re-run, and log the change in DEVIATIONS.md.

**The control failing twice is a stop condition.**

Scoring is deterministic and needs no judge: a response counts as correct iff
exp4_witnesses.supports_correct(response, correct_answer) -- the repo's own
declared lexical instrument, >=2 shared content tokens and >=50% coverage of the
gold answer's content tokens. A literal UNKNOWN never counts as correct. The rule
is deliberately GENEROUS toward detecting leakage: a lexical near-miss still
counts as a leak, because the question is whether the index carries answer content
at all.

Usage:  python e0_metamemory/tools/run_leakage_control.py <level>
"""

from __future__ import annotations

import concurrent.futures as cf
import random
import sys

import api
import prompts
from e0_common import E0, PROJECT_ROOT, SEED, jdump, jload, load_joins

sys.path.insert(0, str(PROJECT_ROOT / "analysis" / "ontology_validation"))
from exp4_witnesses import supports_correct  # noqa: E402

N = 30
THRESHOLD = 3          # MORE than this many correct => leak


def main():
    level = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    idx = jload(E0 / "indexes.json")
    if idx["meta"]["tightening_level"] != level:
        raise SystemExit(f"indexes.json is level {idx['meta']['tightening_level']}, "
                         f"asked for {level} -- rebuild first")
    indexes = idx["indexes"]

    items = [i for i in jload(E0 / "items.json") if i["label"] == "PRESENT"]
    joins = load_joins()
    qs = {q["id"]: q for J in joins.values() for q in J.questions}
    sample = sorted(random.Random(SEED).sample(items, N), key=lambda i: i["item_id"])

    def one(it):
        q = qs[it["question_id"]]
        msgs = [{"role": "system", "content": prompts.LEAKAGE_SYSTEM},
                {"role": "user", "content": prompts.LEAKAGE_USER.format(
                    index=indexes[f"{it['persona']}:{it['variant']}"], question=q["question"])}]
        r = api.call(it["item_id"], f"leakage_L{level}", msgs, max_tokens=200)
        obj = api.parse_json(r["content"]) or {}
        ans = str(obj.get("answer", "")).strip()
        correct = (ans.upper() != "UNKNOWN"
                   and supports_correct(ans, q.get("correct_answer", "")))
        return {"item_id": it["item_id"], "question": q["question"],
                "correct_answer": q.get("correct_answer", ""), "response": ans,
                "correct": bool(correct), "cached": r["cached"]}

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one, sample))
    api.flush()

    n_correct = sum(1 for r in rows if r["correct"])
    leaked = n_correct > THRESHOLD
    m = api.meter()

    print("=" * 92)
    print(f"INDEX-LEAKAGE CONTROL — tightening level {level}")
    print("=" * 92)
    for r in rows:
        mark = "LEAK " if r["correct"] else "  .  "
        print(f"{mark} {r['item_id']:34s} {r['response'][:44]:44s} | gold: {r['correct_answer'][:34]}")
    print(f"\n  correct: {n_correct}/{N}   threshold: >{THRESHOLD}   "
          f"verdict: {'LEAKS — TIGHTEN' if leaked else 'PASS'}")
    print(f"  spend so far: ${m['usd']:.4f}  ({m['calls']} calls, {m['cached']} cached)")

    jdump({"level": level, "n": N, "n_correct": n_correct, "threshold": THRESHOLD,
           "leaked": leaked, "seed": SEED,
           "scoring": "exp4_witnesses.supports_correct(response, correct_answer); "
                      "UNKNOWN never counts as correct",
           "rows": rows, "meter": m},
          E0 / f"leakage_control_L{level}.json")
    print(f"\nwrote {E0/f'leakage_control_L{level}.json'}")
    return 1 if leaked else 0


if __name__ == "__main__":
    sys.exit(main())
