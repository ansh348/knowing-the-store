"""cf2_leakscreen.py -- CF-2: the index-leakage screen on the v3 and V2R arms (ADDENDUM_CF2 section 5).

The screen is ladder_e1.py's, reproduced on the CF-2 cell rather than imported, because ladder_e1
reads E1's own items and indexes from fixed paths and writes into E1's cache:

  sample     the 30 PRESENT items of the cell, sorted by item_id, random.Random(42).sample(pool, 30)
             (ladder_e1.py:121), shared across the two arms screened
  call       gpt-4.1-mini, temperature 0, seed 42, max_tokens 200 (prompts_e1.MODEL/TEMPERATURE/
             SEED/MAX_TOKENS), messages = prompts_e1.LEAKAGE_SYSTEM + LEAKAGE_USER.format(index,
             question); digests of the frozen module asserted before any call
  score      exp4_witnesses.supports_correct(answer, gold): >= 2 shared content tokens and >= 50%
             coverage of the gold's content tokens; UNKNOWN never scores
  gold       the pair's entry_text (the CF questions carry no correct_answer field; the same choice
             R96's leakscreen_v3.py made and recorded)
  rule       a cell LEAKS iff more than THRESHOLD = 3 of N = 30 score correct; a leak is a STOP
  D18        a nominal pass within 2 of the threshold lists the index lines sharing a token with
             the gold, for inspection

Arms screened: v3 and v2r (the registration's two); v2 is screened beside them because it costs
30 calls and v3's prefix is v2. Writes cf2/results/leakscreen_cf2.json. Exit 1 iff v3 or V2R leaks.
OpenAI only; nothing on the Anthropic key.
"""
from __future__ import annotations

import concurrent.futures as cf
import hashlib
import io
import json
import os
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in ("e1_metamemory/tools", "e0_metamemory/tools", "analysis/ontology_validation", "r82_counterfactual/tools"):
    sys.path.insert(0, str(ROOT / p))
import prompts_e1 as P  # noqa: E402
from exp4_witnesses import supports_correct, toks as etoks  # noqa: E402
import run_cf as RC  # noqa: E402  (digest assertions run at import; last_json, load_env)

CF2 = ROOT / "r82_counterfactual" / "cf2"
OUT = CF2 / "results" / "leakscreen_cf2.json"
N, THRESHOLD, D18_BAND, SEED = 30, 3, 2, P.SEED
ARMS = ("v3", "v2r", "v2")
PRICE_IN, PRICE_OUT = 0.40, 1.60          # gpt-4.1-mini list, as run_cf.LANES
assert (P.MODEL, P.TEMPERATURE, P.SEED, P.MAX_TOKENS) == ("gpt-4.1-mini", 0, 42, 200)


def plausible_lines(index_text, gold, response, max_lines=14):
    g, r = etoks(gold), etoks(response); out = []
    for n, line in enumerate(index_text.splitlines(), 1):
        lt = etoks(line); hg, hr = sorted(g & lt), sorted(r & lt)
        if hg or hr:
            out.append({"line_no": n, "line": line.rstrip(), "gold_tokens_on_line": hg, "answer_tokens_on_line": hr})
    out.sort(key=lambda d: (-len(d["gold_tokens_on_line"]), -len(d["answer_tokens_on_line"]), d["line_no"]))
    return out[:max_lines]


def main():
    RC.load_env()
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    cell = json.load(io.open(CF2 / "cf_cell.json", encoding="utf-8"))["items"]
    idx = json.load(io.open(CF2 / "cf_indexes.json", encoding="utf-8"))["indexes"]
    gold = {p["pair_id"]: p["entry_text"] for p in json.load(io.open(CF2 / "cf_pairs_cf2.json", encoding="utf-8"))["pairs"]}
    pool = sorted((it for it in cell if it["version"] == "PRESENT"), key=lambda i: i["item_id"])
    assert len(pool) >= N
    sample = sorted(random.Random(SEED).sample(pool, N), key=lambda i: i["item_id"])
    jobs = [(arm, it) for arm in ARMS for it in sample]

    def one(job):
        arm, it = job
        index_text = idx[it["item_id"]][arm]
        msgs = [{"role": "system", "content": P.LEAKAGE_SYSTEM}, {"role": "user", "content": P.LEAKAGE_USER.format(index=index_text, question=it["question"])}]
        r = client.chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS, messages=msgs)
        text = r.choices[0].message.content or ""
        obj = RC.last_json(text); ans = "" if obj is None else str(obj.get("answer", "")).strip()
        non_unknown = bool(ans) and ans.upper() != "UNKNOWN"
        g = gold[it["pair_id"]]
        correct = non_unknown and supports_correct(ans, g)
        return arm, {"item_id": it["item_id"], "pair_id": it["pair_id"], "persona": it["persona"], "state": it["state"], "question": it["question"],
                     "gold_entry_text": g, "response": ans, "raw_response": text[:600], "parse_ok": obj is not None, "non_unknown": non_unknown,
                     "correct": bool(correct), "served_model": r.model, "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens}

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(one, jobs))
    cells = {}
    for arm in ARMS:
        rows = sorted((r for a, r in results if a == arm), key=lambda r: r["item_id"])
        n_correct = sum(r["correct"] for r in rows); leaked = n_correct > THRESHOLD
        d18 = (not leaked) and n_correct >= THRESHOLD - D18_BAND + 1
        if d18:
            for r in rows:
                if r["correct"] or r["non_unknown"]:
                    r["d18_index_lines"] = plausible_lines(idx[r["item_id"]][arm], r["gold_entry_text"], r["response"])
        cells[arm] = {"arm": arm, "n": N, "n_correct": n_correct, "threshold": THRESHOLD, "leaked": leaked,
                      "verdict": "LEAKS -- STOP" if leaked else "PASS", "d18_triggered": bool(d18),
                      "n_non_unknown": sum(r["non_unknown"] for r in rows), "n_parse_failures": sum(not r["parse_ok"] for r in rows),
                      "usd": round(sum(r["tok_in"] for r in rows) / 1e6 * PRICE_IN + sum(r["tok_out"] for r in rows) / 1e6 * PRICE_OUT, 6),
                      "rows": rows}
    out = {"meta": {"screen": "ladder_e1.py's, reproduced on the CF-2 cell", "model": P.MODEL, "temperature": P.TEMPERATURE, "seed": P.SEED,
                    "max_tokens": P.MAX_TOKENS, "prompts_e1_file_sha256": P.file_sha256(), "prompts_e1_texts_sha256": P.texts_sha256(),
                    "n": N, "threshold": THRESHOLD, "leak_rule": f"a cell leaks iff MORE than {THRESHOLD} of {N} PRESENT items score correct",
                    "sample_rule": f"PRESENT items sorted by item_id, random.Random({SEED}).sample(pool, {N})", "sample": [it["item_id"] for it in sample],
                    "gold": "the pair's entry_text (cf_pairs_cf2.json)", "scorer": "exp4_witnesses.supports_correct (>=2 shared content tokens, >=50% gold coverage)",
                    "arms": list(ARMS), "usd_total": round(sum(c["usd"] for c in cells.values()), 6), "date": "2026-09-13",
                    "served_models": sorted({r["served_model"] for _, r in results})},
           "cells": cells}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True); f.write("\n")
    for arm in ARMS:
        c = cells[arm]
        print(f"{arm:4s} {c['n_correct']:2d}/{N} correct  non-UNKNOWN {c['n_non_unknown']:2d}  parse-fail {c['n_parse_failures']}  {c['verdict']}"
              f"{'  (D18 inspection dumped)' if c['d18_triggered'] else ''}  ${c['usd']:.4f}")
    print(f"served {out['meta']['served_models']}  total ${out['meta']['usd_total']:.4f}  -> {OUT}")
    if cells["v3"]["leaked"] or cells["v2r"]["leaked"]:
        raise SystemExit("STOP: a registered arm leaks (ADDENDUM_CF2 section 13)")


if __name__ == "__main__":
    main()
