"""leak_side.py -- SIDE-BUILD-1 step 3: the leakage screens (ADDENDUM_SIDE.md, frozen e8b2630;
section S1 step 3 and section S2 "before any monitor call"). MODEL CALLS: 90 on gpt-4.1-mini
(30 per cell) plus one served-identifier probe. ladder_e1.py is not modified; this script runs
its level-0 procedure -- the same sampler, the same frozen LEAKAGE prompt pair, the same cached
client (api.call: temperature 0, seed 42, max_tokens 200, json_object), the same scorer
(exp4_witnesses.supports_correct; a literal UNKNOWN never counts) and the same D18 dump -- with
only the index text swapped:

  mem0:GT     the ladder's own 30 Mem0 PRESENT FULL items against the persona's GT index
              (lexical-required map; side_experiments/s1/indexes_gt.json)
  amem:GT     the ladder's own 30 A-MEM PRESENT FULL items against the persona's GT index
              (two-channel map)
  frbank:S2U  the ladder's own 30 FR-Bank PRESENT FULL items against the persona's FULL S2-U
              index (side_experiments/s2/indexes_s2u.json, frbank:<p>:FULL:S2U) -- the committed
              frbank:BELIEVED cell with the cap lifted, paired item for item.

The sample is asserted equal to the committed screen's (e1_metamemory/ladder_L0.json rows), so
each cell is paired with its committed counterpart. More than 3 of 30 correct in any cell is a
STOP (section STOP); a nominal pass at 2 or 3 of 30 trips the D18 inspection dump (a human
reads it; nothing descends here). The cache for the side experiments lives under
side_experiments/cache/ (own write scope; E1's cache is not touched).

Usage, from the repository root:  python side_experiments/tools/leak_side.py
"""
from __future__ import annotations

import concurrent.futures as cf
import hashlib
import io
import json
import random
import subprocess
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import side_common as SC                                         # noqa: E402
from side_common import ROOT, E1, J, jdump                       # noqa: E402
import api                                                       # noqa: E402
import prompts_e1                                                # noqa: E402
import ladder_e1 as LAD                                          # noqa: E402  (imported, never modified, never run)
from e0_common import LME                                        # noqa: E402
from exp4_witnesses import supports_correct                      # noqa: E402

LEAK = SC.SIDE / "leak"
CACHE = SC.SIDE / "cache"
FREEZE = "e8b2630"
PIN_PROMPTS = {"file": "337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84",
               "texts": "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"}
CELLS = (("mem0", "GT"), ("amem", "GT"), ("frbank", "S2U"))
FAILS: list[str] = []


def gate(name, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'} {name}" + (f": {detail}" if detail and not ok else ""))
    if not ok:
        FAILS.append(f"{name}: {detail}")


def redirect_cache():
    """Side-experiment responses land under side_experiments/cache/, the same client otherwise."""
    CACHE.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                 # noqa: SLF001
    e0.CACHE_PATH = CACHE / "responses.json"; e0.LEDGER_PATH = CACHE / "cost_ledger.json"
    e0._cache = None; e0._load_cache()                           # noqa: SLF001
    return e0


def sample(items):
    """ladder_e1.main's sampler, verbatim: FULL PRESENT items per backend, sorted by item_id,
    random.Random(SEED).sample(pool, N), sorted by item_id."""
    out = {}
    for b in LAD.BACKENDS:
        pool = sorted((i for i in items if i["backend"] == b and i["variant"] == LAD.VARIANT and i["label_pre"] == "PRESENT"),
                      key=lambda i: i["item_id"])
        out[b] = sorted(random.Random(LAD.SEED).sample(pool, LAD.N), key=lambda i: i["item_id"])
    return out


def main():
    print(f"leak_side -- SIDE-BUILD-1 step 3, ADDENDUM_SIDE.md (frozen {FREEZE}); ladder_e1 level 0 on the side indexes")
    print("0. gates before any call")
    rc = subprocess.run([sys.executable, str(SC.SIDE / "tools" / "verify_side.py")], capture_output=True, text=True).returncode
    gate("verify_side.py passes", rc == 0, f"exit {rc}")
    gate("prompts_e1 digests as frozen", prompts_e1.file_sha256() == PIN_PROMPTS["file"] and prompts_e1.texts_sha256() == PIN_PROMPTS["texts"])
    lad_blob = subprocess.run(["git", "hash-object", str(E1 / "tools" / "ladder_e1.py")], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    lad_head = subprocess.run(["git", "rev-parse", "HEAD:e1_metamemory/tools/ladder_e1.py"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    gate("ladder_e1.py unchanged (working tree blob == HEAD blob)", lad_blob == lad_head and len(lad_blob) == 40, f"{lad_blob[:8]} vs {lad_head[:8]}")
    gate("api is E1's cached client (e1_metamemory/tools/api.py)", api.__file__.replace("\\", "/").endswith("e1_metamemory/tools/api.py"), api.__file__)
    gate("lane pinned: gpt-4.1-mini, temperature 0, seed 42, max_tokens 200",
         prompts_e1.MODEL == "gpt-4.1-mini" and prompts_e1.TEMPERATURE == 0 and prompts_e1.SEED == 42 and prompts_e1.MAX_TOKENS == 200)
    gt = J(SC.S1 / "indexes_gt.json")["indexes"]; s2u = J(SC.SIDE / "s2" / "indexes_s2u.json")["indexes"]
    items = J(E1 / "build" / "items_pre.json"); questions = {q["id"]: q for q in J(LME / "lifemembench_questions.json")}
    samples = sample(items)
    committed = J(E1 / "ladder_L0.json")["cells"]
    for b in LAD.BACKENDS:
        want = [r["item_id"] for r in committed[f"{b}:TRUE"]["rows"]]
        gate(f"{b}: the 30 sampled items are the committed screen's (ladder_L0.json)", [i["item_id"] for i in samples[b]] == want)
    jobs = []
    for b, tag in CELLS:
        for it in samples[b]:
            key = SC.gt_key(b, it["persona"]) if tag == "GT" else f"frbank:{it['persona']}:FULL:S2U"
            text = (gt if tag == "GT" else s2u).get(key)
            if text is None:
                gate(f"index {key} exists", False, "missing")
            jobs.append((b, tag, it, key, text))
    gate("90 jobs, 30 per cell", len(jobs) == 90)
    if FAILS:
        print("leak_side: STOP -- a pre-call gate failed; no call made"); return 1

    e0 = redirect_cache()
    print("1. served-identifier probe (E1.7 rule), one call through the same client")
    b, tag, it, key, text = jobs[0]
    q = questions[it["question_id"]]
    msgs = [{"role": "system", "content": prompts_e1.LEAKAGE_SYSTEM},
            {"role": "user", "content": prompts_e1.LEAKAGE_USER.format(index=text, question=q["question"])}]
    r = e0._client().chat.completions.create(model=prompts_e1.MODEL, temperature=prompts_e1.TEMPERATURE, seed=prompts_e1.SEED,  # noqa: SLF001
                                             max_tokens=prompts_e1.MAX_TOKENS, messages=msgs, response_format={"type": "json_object"})
    probe = {"served_model": r.model, "prompt_tokens": r.usage.prompt_tokens, "completion_tokens": r.usage.completion_tokens,
             "usd": r.usage.prompt_tokens / 1e6 * api.PRICE_IN + r.usage.completion_tokens / 1e6 * api.PRICE_OUT,
             "content": r.choices[0].message.content}
    gate(f"served identifier carries gpt-4.1-mini ({r.model})", "gpt-4.1-mini" in r.model)
    if FAILS:
        print("leak_side: STOP -- identifier mismatch; do not launch"); return 1

    print("2. the screens (90 calls, 8 workers, api.call)")

    def one(job):
        b, tag, it, key, text = job
        q = questions[it["question_id"]]
        msgs = [{"role": "system", "content": prompts_e1.LEAKAGE_SYSTEM},
                {"role": "user", "content": prompts_e1.LEAKAGE_USER.format(index=text, question=q["question"])}]
        r = api.call(it["item_id"], f"leakage_L0:side:{b}:{tag}", msgs, max_tokens=prompts_e1.MAX_TOKENS)
        obj = api.parse_json(r["content"])
        ans = "" if obj is None else str(obj.get("answer", "")).strip()
        non_unknown = bool(ans) and ans.upper() != "UNKNOWN"
        correct = non_unknown and supports_correct(ans, q.get("correct_answer", ""))
        return (b, tag, {"item_id": it["item_id"], "persona": it["persona"], "question_id": it["question_id"], "index_key": key,
                         "attack_vector": q.get("attack_vector"), "question": q["question"], "correct_answer": q.get("correct_answer", ""),
                         "response": ans, "raw_response": r["content"], "parse_ok": obj is not None, "non_unknown": non_unknown,
                         "correct": bool(correct), "cached": r["cached"], "prompt_tokens": r.get("prompt_tokens"),
                         "completion_tokens": r.get("completion_tokens")})

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(one, jobs))
    api.flush()

    cells = {}
    for b, tag in CELLS:
        rows = sorted((r for bb, tt, r in results if bb == b and tt == tag), key=lambda r: r["item_id"])
        n_correct = sum(r["correct"] for r in rows); leaked = n_correct > LAD.THRESHOLD
        d18 = (not leaked) and n_correct >= LAD.THRESHOLD - LAD.D18_BAND + 1
        idx = gt if tag == "GT" else s2u
        if d18:
            for r in rows:
                if r["correct"] or r["non_unknown"]:
                    r["d18_index_lines"] = LAD.plausible_lines(idx[r["index_key"]], r["correct_answer"], r["response"])
        paired = committed[f"{b}:{'TRUE' if tag == 'GT' else 'BELIEVED'}"]
        cells[f"{b}:{tag}"] = {"backend": b, "arm": tag, "n": LAD.N, "n_correct": n_correct, "threshold": LAD.THRESHOLD,
                               "leaked": leaked, "verdict": "LEAKS -- STOP" if leaked else "PASS", "d18_triggered": bool(d18),
                               "n_non_unknown": sum(r["non_unknown"] for r in rows), "n_parse_failures": sum(not r["parse_ok"] for r in rows),
                               "n_cached": sum(r["cached"] for r in rows),
                               "committed_counterpart": {"cell": f"{b}:{'TRUE' if tag == 'GT' else 'BELIEVED'}", "n_correct": paired["n_correct"],
                                                         "n_non_unknown": paired["n_non_unknown"]},
                               "rows": rows}
    cache = J(e0.CACHE_PATH)
    lv = [r for r in cache.values() if str(r.get("arm", "")).startswith("leakage_L0:side:")]
    cost = {"n_calls": len(lv), "prompt_tokens": sum(r["prompt_tokens"] for r in lv), "completion_tokens": sum(r["completion_tokens"] for r in lv)}
    cost["usd"] = round(cost["prompt_tokens"] / 1e6 * api.PRICE_IN + cost["completion_tokens"] / 1e6 * api.PRICE_OUT, 6)
    cost["probe_usd"] = round(probe["usd"], 6); cost["usd_with_probe"] = round(cost["usd"] + probe["usd"], 6)
    cost["source"] = "summed over every cached response whose arm is leakage_L0:side:*, invariant to re-runs; the probe added"
    out = {"registration": "registrations/ADDENDUM_SIDE.md", "frozen": FREEZE, "level": 0, "model": prompts_e1.MODEL, "temperature": prompts_e1.TEMPERATURE,
           "seed": prompts_e1.SEED, "max_tokens": prompts_e1.MAX_TOKENS, "n": LAD.N, "threshold": LAD.THRESHOLD, "d18_band": LAD.D18_BAND,
           "ladder_e1_blob": lad_blob, "prompts_file_sha256": prompts_e1.file_sha256(), "prompts_texts_sha256": prompts_e1.texts_sha256(),
           "gt_indexes_sha256": hashlib.sha256((SC.S1 / "indexes_gt.json").read_bytes()).hexdigest(),
           "s2u_indexes_sha256": hashlib.sha256((SC.SIDE / "s2" / "indexes_s2u.json").read_bytes()).hexdigest(),
           "sampling": "ladder_e1.main's sampler verbatim; the 30 items per backend equal ladder_L0.json's",
           "scoring": "exp4_witnesses.supports_correct(response, correct_answer); a literal UNKNOWN never counts",
           "probe": probe, "cost": cost, "meter": api.meter(), "cells": cells,
           "d18_triggered_cells": [k for k, c in cells.items() if c["d18_triggered"]], "n_cells_leaking": sum(c["leaked"] for c in cells.values())}
    LEAK.mkdir(parents=True, exist_ok=True); jdump(out, LEAK / "leak_side.json")

    W = 100
    print("=" * W)
    for k, c in cells.items():
        print(f"---- {k} ----   correct {c['n_correct']}/{LAD.N}   non-UNKNOWN {c['n_non_unknown']}/{LAD.N}   parse failures {c['n_parse_failures']}   "
              f"{c['verdict']}   (committed {c['committed_counterpart']['cell']}: {c['committed_counterpart']['n_correct']}/30)")
        for r in c["rows"]:
            if r["correct"] or r["non_unknown"]:
                print(f"  {'LEAK' if r['correct'] else ' ans'} {r['item_id']:38s} {r['response'][:40]:40s} | gold: {r['correct_answer'][:34]}")
    trig = out["d18_triggered_cells"]
    print("D18:", "no cell within 2 of the threshold" if not trig else f"TRIGGERED in {trig} -- inspection dump in leak_side.json")
    for k in trig:
        for r in cells[k]["rows"]:
            if r["correct"] or r["non_unknown"]:
                print(f"    [{'CORRECT' if r['correct'] else 'non-UNKNOWN'}] {r['item_id']}\n      Q: {r['question']}\n      gold: {r['correct_answer']}\n      model: {r['response']}")
                for d in r.get("d18_index_lines") or []:
                    print(f"      L{d['line_no']:<3d} gold={d['gold_tokens_on_line']} ans={d['answer_tokens_on_line']}\n           | {d['line'][:150]}")
    print(f"cost: {cost['n_calls']} calls, {cost['prompt_tokens']:,} in / {cost['completion_tokens']:,} out, ${cost['usd']:.4f} (+ probe ${probe['usd']:.4f})")
    print(f"wrote {LEAK / 'leak_side.json'}")
    if out["n_cells_leaking"]:
        print(f"leak_side: STOP -- {out['n_cells_leaking']} cell(s) above 3 of 30"); return 1
    print("leak_side: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
