"""leakage.py -- R85 Phase 1. Leakage screen over the serialized Graphiti indexes. BILLED.

Asks the monitor model to answer a PRESENT item's question from the index ALONE. A correct
answer means the index carries content it should not, because the index is metadata only.
Prompts, scorer and threshold are the study's own, imported rather than restated.

UNDER-POWERED BY CONSTRUCTION, AND SAID SO. The frozen threshold is "more than 3 of 30
sampled PRESENT items answered correctly from the index alone". The three spike personas
supply only 10 PRESENT FULL items between them, so a 30-item draw does not exist here. The
raw count is reported against 10 and the frozen threshold is NOT rescaled to fit. The proper
30-item screen belongs to the 40-persona run, where the population supports it.

Usage:
  python r85_graphiti/leakage.py --model gpt-4.1-mini-2025-04-14
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "analysis" / "ontology_validation"))

import prompts_e1  # noqa: E402
from exp4_witnesses import supports_correct  # noqa: E402

THRESHOLD_N, THRESHOLD_K = 30, 3  # frozen; reported, never rescaled
PERSONAS = ("elena", "tom", "yoli")


def load_env():
    env = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--arm", default="stock")
    a = ap.parse_args()

    items = json.loads((ROOT / "e1_metamemory" / "build" / "items_final.json").read_text("utf-8"))
    qs = {q["id"]: q for q in json.loads(
        (ROOT / "LifeMemEval" / "lifemembench_questions.json").read_text("utf-8"))}
    sel = sorted(
        [i for i in items if i["backend"] == "frbank" and i["persona"] in PERSONAS
         and i["label"] == "PRESENT" and i["variant"] == "FULL"],
        key=lambda i: i["item_id"])

    indexes = {}
    for p in PERSONAS:
        f = HERE / "census_runs" / f"{a.arm}_{a.model}_{p}.index.txt"
        if f.exists():
            indexes[p] = f.read_text(encoding="utf-8")
    sel = [i for i in sel if i["persona"] in indexes]
    print(f"screening {len(sel)} PRESENT items over {len(indexes)} personas "
          f"(frozen threshold is >{THRESHOLD_K}/{THRESHOLD_N}; this draw is under-powered)")

    env = load_env()
    from openai import OpenAI
    c = OpenAI(api_key=env["OPENAI_API_KEY"])

    rows, n_correct = [], 0
    for it in sel:
        q = qs[it["question_id"]]
        r = c.chat.completions.create(
            model=a.model, temperature=0,
            messages=[{"role": "system", "content": prompts_e1.LEAKAGE_SYSTEM},
                      {"role": "user", "content": prompts_e1.LEAKAGE_USER.format(
                          index=indexes[it["persona"]], question=q["question"])}])
        txt = r.choices[0].message.content or ""
        try:
            ans = json.loads(txt).get("answer", "")
        except Exception:
            ans = txt
        ok = bool(ans) and ans.strip().upper() != "UNKNOWN" and \
            supports_correct(ans, q["correct_answer"])
        n_correct += int(ok)
        rows.append({"item_id": it["item_id"], "persona": it["persona"],
                     "question": q["question"], "answer": ans, "correct": ok})
        print(f"  {'LEAK' if ok else 'ok  '} {it['item_id']:38s} {ans[:70]}")

    out = {"model": a.model, "arm": a.arm, "n": len(sel), "n_correct": n_correct,
           "frozen_threshold": f">{THRESHOLD_K}/{THRESHOLD_N}",
           "underpowered": True, "rows": rows}
    (HERE / "census_runs" / f"leakage_{a.arm}_{a.model}.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nLEAKAGE: {n_correct}/{len(sel)} answered correctly from the index alone.")
    print(f"Frozen threshold >{THRESHOLD_K}/{THRESHOLD_N} is not rescaled; this draw is "
          f"{len(sel)} items and the 30-item screen belongs to the full run.")


if __name__ == "__main__":
    main()
