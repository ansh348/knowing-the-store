# -*- coding: utf-8 -*-
"""ix_leakscreen.py -- program R121: the CF-2 summary-leakage screen on the crossed questions (registration §3; ruling 6).

cf2_leakscreen.py's protocol, reproduced: gpt-4.1-mini, temperature 0, seed 42, max_tokens 200 (prompts_e1.MODEL / TEMPERATURE /
SEED / MAX_TOKENS), messages = prompts_e1.LEAKAGE_SYSTEM + LEAKAGE_USER.format(index, question), digests asserted at import;
scorer exp4_witnesses.supports_correct(answer, gold) with gold = the pair's entry_text; a cell LEAKS iff more than THRESHOLD = 3
of N = 30 score correct; a leak is a STOP.

Cells (registered): A  the 30 PRESENT versions drawn by random.Random(42).sample from population A's 88, sorted by item_id, under
                       the v2 summary, with the seed-42 crossed question;
                    B  all 30 PRESENT versions of population B under the v3 summary, the seed-42 crossed question.
Beside them (cover, not a registered cell): the second lineage's question (temperature 0.7, seed 4242) of every sampled item whose
fallback differs from its primary. Writes r82_counterfactual/cf2/results/leakscreen_ix.json (ruling 7). OpenAI only.
Version 2 of the questions (D-IX-1): the version-1 screen is kept as results/leakscreen_ix_v1_superseded.json.
"""
from __future__ import annotations

import concurrent.futures as cf
import io
import json
import os
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("e1_metamemory/tools", "e0_metamemory/tools", "analysis/ontology_validation", "r82_counterfactual/tools"):
    sys.path.insert(0, str(ROOT / p))
import prompts_e1 as P  # noqa: E402
from exp4_witnesses import supports_correct  # noqa: E402
import run_cf as RC  # noqa: E402  (digest assertions at import; last_json, load_env)

CF2 = ROOT / "r82_counterfactual" / "cf2"
QF = ROOT / "reviews" / "r121" / "build" / "cross_questions.json"
OUT = CF2 / "results" / "leakscreen_ix.json"
N, THRESHOLD, SEED = 30, 3, P.SEED
SUMMARY = {"A": "v2", "B": "v3"}
PRICE_IN, PRICE_OUT = 0.40, 1.60
assert (P.MODEL, P.TEMPERATURE, P.SEED, P.MAX_TOKENS) == ("gpt-4.1-mini", 0, 42, 200)


def main():
    RC.load_env()
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    cell = json.load(io.open(CF2 / "cf_cell.json", encoding="utf-8"))["items"]
    idx = json.load(io.open(CF2 / "cf_indexes.json", encoding="utf-8"))["indexes"]
    gold = {p["pair_id"]: p["entry_text"] for p in json.load(io.open(CF2 / "cf_pairs_cf2.json", encoding="utf-8"))["pairs"]}
    qdoc = json.load(io.open(QF, encoding="utf-8")); qs = {r["pair_id"]: r for r in qdoc["questions"]}
    present = {it["pair_id"]: it for it in cell if it["version"] == "PRESENT"}
    pool_a = sorted((present[pid] for pid, r in qs.items() if r["population"] == "A"), key=lambda i: i["item_id"])
    pool_b = sorted((present[pid] for pid, r in qs.items() if r["population"] == "B"), key=lambda i: i["item_id"])
    assert len(pool_a) == 88 and len(pool_b) == 30
    sample = {"A": sorted(random.Random(SEED).sample(pool_a, N), key=lambda i: i["item_id"]), "B": pool_b}
    assert qdoc["meta"].get("instruction_version") == 2 and qdoc["meta"].get("fallback_lineage") == "lineage2", "cross_questions.json is not version 2 with lineage 2"
    assert not OUT.exists(), f"{OUT} exists; a superseded screen belongs beside it as *_superseded.json"
    prev = None
    jobs = []
    for pop, items in sample.items():
        for it in items:
            jobs.append((pop, "primary", it))
            if not qs[it["pair_id"]]["fallback_identical"]:
                jobs.append((pop, "fallback", it))

    def one(job):
        pop, label, it = job
        arm = SUMMARY[pop]; q = qs[it["pair_id"]][label]["question"]; index_text = idx[it["item_id"]][arm]
        msgs = [{"role": "system", "content": P.LEAKAGE_SYSTEM}, {"role": "user", "content": P.LEAKAGE_USER.format(index=index_text, question=q)}]
        r = client.chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS, messages=msgs)
        text = r.choices[0].message.content or ""
        obj = RC.last_json(text); ans = "" if obj is None else str(obj.get("answer", "")).strip()
        non_unknown = bool(ans) and ans.upper() != "UNKNOWN"
        g = gold[it["pair_id"]]; correct = non_unknown and supports_correct(ans, g)
        return pop, label, {"item_id": it["item_id"], "pair_id": it["pair_id"], "persona": it["persona"], "state": it["state"], "summary": arm, "question": q,
                            "gold_entry_text": g, "response": ans, "raw_response": text[:600], "parse_ok": obj is not None, "non_unknown": non_unknown,
                            "correct": bool(correct), "served_model": r.model, "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens}

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(one, jobs))
    cells = {}
    for pop in ("A", "B"):
        for label in ("primary", "fallback"):
            rows = sorted((r for p_, l_, r in results if p_ == pop and l_ == label), key=lambda r: r["item_id"])
            if not rows:
                continue
            n_correct = sum(r["correct"] for r in rows)
            registered = label == "primary"
            leaked = n_correct > THRESHOLD if registered else None
            cells[f"{pop}_{label}"] = {"population": pop, "summary": SUMMARY[pop], "questions": "seed 42" if registered else "lineage 2, temperature 0.7, seed 4242 (differing fallbacks only)",
                                       "registered_cell": registered, "n": len(rows), "n_correct": n_correct, "threshold": THRESHOLD if registered else None, "leaked": leaked,
                                       "verdict": ("LEAKS -- STOP" if leaked else "PASS") if registered else f"{n_correct} of {len(rows)} correct (cover)",
                                       "n_non_unknown": sum(r["non_unknown"] for r in rows), "n_parse_failures": sum(not r["parse_ok"] for r in rows),
                                       "usd": round(sum(r["tok_in"] for r in rows) / 1e6 * PRICE_IN + sum(r["tok_out"] for r in rows) / 1e6 * PRICE_OUT, 6), "rows": rows}
    out = {"meta": {"screen": "cf2_leakscreen.py's protocol on the crossed questions (program R121, registration section 3, ruling 6)", "model": P.MODEL, "temperature": P.TEMPERATURE,
                    "seed": P.SEED, "max_tokens": P.MAX_TOKENS, "prompts_e1_file_sha256": P.file_sha256(), "prompts_e1_texts_sha256": P.texts_sha256(),
                    "questions_file": str(QF.relative_to(ROOT)).replace("\\", "/"), "instruction_version": 2, "deviation": "D-IX-1",
                    "prompt_sha256": qdoc["meta"]["primary"]["prompt_sha256"], "questions_sha256_seed42": qdoc["meta"]["primary"]["questions_sha256"],
                    "lineage2_sha256": qdoc["meta"]["lineage2"]["lineage_sha256"], "questions_sha256_lineage2": qdoc["meta"]["lineage2"]["questions_sha256"],
                    "fallback_lineage": "lineage2", "n": N, "threshold": THRESHOLD,
                    "leak_rule": f"a registered cell leaks iff MORE than {THRESHOLD} of {N} PRESENT items score correct",
                    "sample_rule": "A: PRESENT versions of population A sorted by item_id, random.Random(42).sample(pool, 30), under v2; B: all 30 PRESENT versions under v3",
                    "sample": {pop: [it["item_id"] for it in items] for pop, items in sample.items()},
                    "gold": "the pair's entry_text (cf_pairs_cf2.json)", "scorer": "exp4_witnesses.supports_correct (>=2 shared content tokens, >=50% gold coverage)",
                    "usd_total": round(sum(c["usd"] for c in cells.values()), 6), "date": "2026-09-19", "served_models": sorted({r["served_model"] for _, _, r in results})},
           "cells": cells}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True); f.write("\n")
    for k, c in cells.items():
        print(f"{k:11s} {c['n_correct']:2d}/{c['n']:2d} correct  non-UNKNOWN {c['n_non_unknown']:2d}  parse-fail {c['n_parse_failures']}  {c['verdict']}  ${c['usd']:.4f}")
    print(f"served {out['meta']['served_models']}  total ${out['meta']['usd_total']:.4f}  -> {OUT.relative_to(ROOT)}")
    if any(c["leaked"] for c in cells.values() if c["registered_cell"]):
        raise SystemExit("STOP: a registered cell leaks (registration section 3)")


if __name__ == "__main__":
    main()
