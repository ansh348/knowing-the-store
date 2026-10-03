"""
ladder_e1.py -- E1 index-leakage ladder, the pre-registered control.

PREREG_E1.md section 5, verbatim: "Leakage ladder runs per backend per
provenance, levels 0 -> 1 -> 2 as in E0. Threshold: more than 3 of 30 sampled
PRESENT items answered correctly from the index alone. D18 inspection rule
(codified): a nominal pass within 2 items of threshold triggers manual
inspection of the index, and descent if inspection shows the scorer masked
leakage. Ladder exhausted without a pass is a stop condition."

What runs here: level 0 only -- the value-scrubbed renderer already built into
`indexes_v2.json` -- across all six cells (frbank/mem0/amem x TRUE/BELIEVED) on
the FULL variant. No FOK/NOK elicitation of any kind is issued; the only prompt
sent is the frozen LEAKAGE pair. **This script never descends a level on its own
initiative.** A descent changes the instrument every downstream number is read
through, so it is a human decision, logged in DEVIATIONS.md.

Sampling. 30 PRESENT items per backend, `random.Random(42)`, drawn from the
backend's own FULL-variant PRESENT pool (`label_pre == "PRESENT"`), the pool
sorted by item_id first so the draw does not depend on file order. The SAME 30
items are shown under both provenances, so TRUE-vs-BELIEVED is paired: a
difference in n_correct is then a property of the index text, not of the sample.

Scoring is deterministic and needs no judge: a response counts as correct iff
`exp4_witnesses.supports_correct(response, correct_answer)` -- the repo's own
declared lexical instrument, >=2 shared content tokens AND >=50% coverage of the
gold answer's content tokens. A literal UNKNOWN never counts. The rule is
deliberately GENEROUS toward detecting leakage: a lexical near-miss still counts
as a leak, because the question is whether the index carries answer content at
all, not whether the model phrased it well.

D18 inspection, mechanised. For any cell whose nominal PASS lands within 2 items
of the threshold (n_correct in {2, 3}), every item that scored correct AND every
item whose response was not UNKNOWN gets its index lines dumped -- the lines
sharing a content token with the gold answer or with the model's own answer --
so a human can read whether the scorer masked leakage. Cells that trip the
trigger are named in the summary table and in the JSON.

Usage:  python e1_metamemory/tools/ladder_e1.py [level]      (default 0)
"""

from __future__ import annotations

import concurrent.futures as cf
import hashlib
import io
import json
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(PROJECT_ROOT / "analysis" / "ontology_validation"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import api                                                      # noqa: E402
import prompts_e1                                               # noqa: E402
from e0_common import LME, jdump, jload                          # noqa: E402
from exp4_witnesses import supports_correct, toks as etoks       # noqa: E402

N = 30
THRESHOLD = 3          # MORE than this many correct => the index leaks
D18_BAND = 2           # a nominal PASS this close to the threshold -> inspect
SEED = prompts_e1.SEED

BACKENDS = ["frbank", "mem0", "amem"]
PROVENANCES = ["TRUE", "BELIEVED"]
VARIANT = "FULL"
MAX_D18_LINES = 14     # per item, in the printed inspection dump


# --------------------------------------------------------------------------- #
# D18 inspection: which index lines could plausibly have carried this answer
# --------------------------------------------------------------------------- #
def plausible_lines(index_text: str, gold: str, response: str):
    """
    Index lines that share a content token with the gold answer or with the
    model's own answer, ranked by gold overlap then response overlap.

    Content tokens are exp4_witnesses.toks -- the SAME tokeniser the scorer
    uses -- so this dump is answering the scorer's own question line by line:
    if no line shares a token with the gold answer, the scorer could not have
    been reading leaked content, whatever the model said.
    """
    g, r = etoks(gold), etoks(response)
    out = []
    for n, line in enumerate(index_text.splitlines(), 1):
        lt = etoks(line)
        hg, hr = sorted(g & lt), sorted(r & lt)
        if hg or hr:
            out.append({"line_no": n, "line": line.rstrip(),
                        "gold_tokens_on_line": hg, "answer_tokens_on_line": hr})
    out.sort(key=lambda d: (-len(d["gold_tokens_on_line"]),
                            -len(d["answer_tokens_on_line"]), d["line_no"]))
    return out[:MAX_D18_LINES]


# --------------------------------------------------------------------------- #
def main() -> int:
    level = int(sys.argv[1]) if len(sys.argv) > 1 else 0

    idx_path = E1 / "indexes_v2.json"
    raw = idx_path.read_bytes()
    idx = json.loads(raw.decode("utf-8"))
    indexes = idx["indexes"]

    items = jload(E1 / "build" / "items_pre.json")
    questions = {q["id"]: q for q in jload(LME / "lifemembench_questions.json")}

    # ---- sample: 30 PRESENT FULL items per backend, shared across provenances
    samples = {}
    for b in BACKENDS:
        pool = sorted((i for i in items
                       if i["backend"] == b and i["variant"] == VARIANT
                       and i["label_pre"] == "PRESENT"),
                      key=lambda i: i["item_id"])
        if len(pool) < N:
            raise SystemExit(f"{b}: only {len(pool)} PRESENT {VARIANT} items, need {N}")
        samples[b] = sorted(random.Random(SEED).sample(pool, N),
                            key=lambda i: i["item_id"])

    # ---- one job per (backend, provenance, item)
    jobs = []
    for b in BACKENDS:
        for prov in PROVENANCES:
            for it in samples[b]:
                key = f"{b}:{it['persona']}:{VARIANT}:{prov}"
                if key not in indexes:
                    raise SystemExit(f"missing index {key}")
                jobs.append((b, prov, it, indexes[key]))

    def one(job):
        b, prov, it, index_text = job
        q = questions[it["question_id"]]
        msgs = [{"role": "system", "content": prompts_e1.LEAKAGE_SYSTEM},
                {"role": "user", "content": prompts_e1.LEAKAGE_USER.format(
                    index=index_text, question=q["question"])}]
        r = api.call(it["item_id"], f"leakage_L{level}:{b}:{prov}", msgs,
                     max_tokens=prompts_e1.MAX_TOKENS)
        obj = api.parse_json(r["content"])
        ans = "" if obj is None else str(obj.get("answer", "")).strip()
        non_unknown = bool(ans) and ans.upper() != "UNKNOWN"
        correct = non_unknown and supports_correct(ans, q.get("correct_answer", ""))
        return (b, prov, {
            "item_id": it["item_id"], "persona": it["persona"],
            "question_id": it["question_id"], "attack_vector": q.get("attack_vector"),
            "question": q["question"], "correct_answer": q.get("correct_answer", ""),
            "response": ans, "raw_response": r["content"],
            "parse_ok": obj is not None, "non_unknown": non_unknown,
            "correct": bool(correct), "cached": r["cached"],
        })

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(one, jobs))
    api.flush()

    # ---- true cost of this ladder level, independent of how many processes ran
    # it. api.meter() is per-process, so a cached re-run would report ~$0 and
    # misstate what the result cost; the cache holds the token counts of every
    # call ever made under this level's arms, so sum those instead.
    cache = jload(api.CACHE_PATH) if Path(api.CACHE_PATH).exists() else {}
    lv = [r for r in cache.values()
          if str(r.get("arm", "")).startswith(f"leakage_L{level}:")]
    cost = {"n_calls": len(lv),
            "prompt_tokens": sum(r["prompt_tokens"] for r in lv),
            "completion_tokens": sum(r["completion_tokens"] for r in lv)}
    cost["usd"] = round(cost["prompt_tokens"] / 1e6 * api.PRICE_IN
                        + cost["completion_tokens"] / 1e6 * api.PRICE_OUT, 6)
    cost["source"] = ("summed over every cached response whose arm is "
                      f"leakage_L{level}:*, so it is invariant to re-runs")

    # ---- assemble per-cell results
    cells = {}
    for b in BACKENDS:
        for prov in PROVENANCES:
            rows = sorted((r for bb, pp, r in results if bb == b and pp == prov),
                          key=lambda r: r["item_id"])
            n_correct = sum(r["correct"] for r in rows)
            leaked = n_correct > THRESHOLD
            d18 = (not leaked) and n_correct >= THRESHOLD - D18_BAND + 1
            if d18:
                for r in rows:
                    if r["correct"] or r["non_unknown"]:
                        key = f"{b}:{r['persona']}:{VARIANT}:{prov}"
                        r["d18_index_lines"] = plausible_lines(
                            indexes[key], r["correct_answer"], r["response"])
            cells[f"{b}:{prov}"] = {
                "backend": b, "provenance": prov, "variant": VARIANT,
                "n": N, "n_correct": n_correct, "threshold": THRESHOLD,
                "leaked": leaked, "verdict": "LEAKS -- TIGHTEN" if leaked else "PASS",
                "d18_triggered": bool(d18),
                "n_non_unknown": sum(r["non_unknown"] for r in rows),
                "n_parse_failures": sum(not r["parse_ok"] for r in rows),
                "rows": rows,
            }

    # ---- print
    W = 100
    print("=" * W)
    print(f"E1 INDEX-LEAKAGE LADDER -- level {level} (value-scrubbed renderer), "
          f"{VARIANT} variant")
    print(f"  {N} PRESENT items per backend, seed {SEED}, same items under both "
          f"provenances; leak iff >{THRESHOLD}/{N} correct")
    print("=" * W)

    for b in BACKENDS:
        for prov in PROVENANCES:
            c = cells[f"{b}:{prov}"]
            print(f"\n---- {b}:{prov} ----   correct {c['n_correct']}/{N}   "
                  f"non-UNKNOWN {c['n_non_unknown']}/{N}   {c['verdict']}")
            for r in c["rows"]:
                if r["correct"] or r["non_unknown"]:
                    mark = "LEAK" if r["correct"] else " ans"
                    print(f"  {mark} {r['item_id']:38s} {r['response'][:40]:40s} "
                          f"| gold: {r['correct_answer'][:34]}")

    trig = [k for k, c in cells.items() if c["d18_triggered"]]
    print("\n" + "=" * W)
    print("D18 INSPECTION TRIGGER")
    print("=" * W)
    if not trig:
        print(f"  No cell landed within {D18_BAND} items of the threshold: no cell "
              f"scored {THRESHOLD - D18_BAND + 1}..{THRESHOLD} of {N} correct. "
              f"No manual inspection required.")
    for k in trig:
        c = cells[k]
        print(f"\n  {k}: nominal PASS at {c['n_correct']}/{N}, within {D18_BAND} of "
              f"the threshold -- manual inspection follows.")
        for r in c["rows"]:
            if not (r["correct"] or r["non_unknown"]):
                continue
            print(f"\n    [{'CORRECT' if r['correct'] else 'non-UNKNOWN'}] "
                  f"{r['item_id']}")
            print(f"      Q      : {r['question']}")
            print(f"      gold   : {r['correct_answer']}")
            print(f"      model  : {r['response']}")
            lines = r.get("d18_index_lines") or []
            if not lines:
                print("      index  : NO line of this index shares a content token "
                      "with the gold answer or with the model's answer.")
            for d in lines:
                print(f"      L{d['line_no']:<3d} gold={d['gold_tokens_on_line']} "
                      f"ans={d['answer_tokens_on_line']}")
                print(f"           | {d['line'][:150]}")

    m = api.meter()
    print("\n" + "=" * W)
    print(f"{'backend':<10}{'provenance':<12}{'n_correct':>10}{'  verdict':<20}"
          f"{'d18_triggered':>15}")
    print("-" * W)
    for b in BACKENDS:
        for prov in PROVENANCES:
            c = cells[f"{b}:{prov}"]
            print(f"{b:<10}{prov:<12}{c['n_correct']:>10}  {c['verdict']:<18}"
                  f"{str(c['d18_triggered']):>15}")
    print("-" * W)
    n_leak = sum(c["leaked"] for c in cells.values())
    print(f"  cells leaking: {n_leak}/6      cells tripping D18: {len(trig)}/6")
    print(f"  this process: {m['calls']} calls, {m['cached']} served from cache, "
          f"${m['usd']:.4f}")
    print(f"  LADDER LEVEL {level} TOTAL: {cost['n_calls']} calls, "
          f"{cost['prompt_tokens']} in + {cost['completion_tokens']} out tokens, "
          f"${cost['usd']:.4f}")

    out = {
        "level": level, "n": N, "threshold": THRESHOLD, "d18_band": D18_BAND,
        "seed": SEED, "variant": VARIANT,
        "leak_rule": f"a cell leaks iff MORE than {THRESHOLD} of {N} PRESENT items "
                     f"are answered correctly from the index alone",
        "d18_rule": f"a nominal PASS with n_correct >= {THRESHOLD - D18_BAND + 1} "
                    f"(within {D18_BAND} of the threshold) triggers manual "
                    f"inspection; descent is a human decision, never taken here",
        "sampling": f"per backend: {VARIANT}-variant items with label_pre==PRESENT, "
                    f"sorted by item_id, random.Random({SEED}).sample(pool, {N}); "
                    f"the same 30 items are used under both provenances",
        "scoring": "exp4_witnesses.supports_correct(response, correct_answer); "
                   "a literal UNKNOWN never counts as correct",
        "model": prompts_e1.MODEL, "temperature": prompts_e1.TEMPERATURE,
        "max_tokens": prompts_e1.MAX_TOKENS,
        "prompts_file_sha256": prompts_e1.file_sha256(),
        "prompts_texts_sha256": prompts_e1.texts_sha256(),
        "indexes_path": str(idx_path),
        "indexes_sha256": hashlib.sha256(raw).hexdigest(),
        "pool_sizes": {b: sum(1 for i in items if i["backend"] == b
                              and i["variant"] == VARIANT
                              and i["label_pre"] == "PRESENT") for b in BACKENDS},
        "d18_triggered_cells": trig,
        "n_cells_leaking": n_leak,
        "cells": cells,
        "ladder_cost": cost,
        "meter": m,
    }
    jdump(out, E1 / f"ladder_L{level}.json")
    print(f"\nwrote {E1 / f'ladder_L{level}.json'}")
    return 1 if n_leak else 0


if __name__ == "__main__":
    sys.exit(main())
