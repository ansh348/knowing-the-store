"""
judge_spotcheck.py -- E2 Amendment 3 section 4: judge validity, 20 items per candidate.

Re-judges 20 already-judged responses per candidate with the SAME pinned judge and
reports the agreement rate. NO BAR -- this is a disclosure that the judge behaves
consistently on each candidate's output distribution, not a gate.

Deterministic sample: seed 42 over the sorted judged keys.

Usage:  python e2_metamemory/tools/judge_spotcheck.py
"""

from __future__ import annotations

import concurrent.futures as cf
import json
import os
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e2_common import E2, jdump, jload, load_items                # noqa: E402
from run_judge import ABSENT_CORRECT, last_json, load_gold, load_rubric  # noqa: E402

CLAUDE = shutil.which("claude") or "claude"
JUDGE_MODEL = "claude-sonnet-4-6"
N = 20


def main():
    SYS_P, USER_T, rubric_sha = load_rubric()
    gold = load_gold()
    items = {i["item_id"]: i for i in load_items() if i["split"] == "calibration"}
    env = {k: v for k, v in os.environ.items()
           if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")}

    def judge(q, ca, wi, resp):
        user = USER_T.format(question=q, correct_answer=ca,
                             wrong_indicators=", ".join(wi) if wi else "(none)",
                             response=resp)
        for _ in range(3):
            try:
                r = subprocess.run(
                    [CLAUDE, "-p", user, "--model", JUDGE_MODEL,
                     "--output-format", "json", "--system-prompt", SYS_P,
                     "--exclude-dynamic-system-prompt-sections",
                     "--disallowedTools",
                     "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch,Task,"
                     "NotebookEdit,TodoWrite", "--setting-sources", ""],
                    capture_output=True, text=True, encoding="utf-8",
                    errors="replace", timeout=180, env=env)
                o = json.loads(r.stdout) if r.stdout.strip() else {}
                v = last_json(o.get("result", "") or "")
                if v and v.get("correctness"):
                    return v
            except Exception:                                     # noqa: BLE001
                pass
            time.sleep(1)
        return None

    out = {}
    for f in sorted(E2.glob("answers_bakeoff-*.json")):
        model = f.stem.replace("answers_bakeoff-", "")
        rows = jload(f)["rows"]
        cache = jload(E2 / "cache" / f"judgments_bakeoff-{model}.json")
        byk = {}
        for r in rows:
            byk.setdefault(f"{r['item_id']}|{r['response_sha'][:24]}", r)
        keys = sorted(k for k in byk if cache.get(k, {}).get("status") == "OK")
        pick = random.Random(42).sample(keys, min(N, len(keys)))

        def one(k):
            r = byk[k]
            it = items[r["item_id"]]
            if it["label_final"] == "ABSENT":
                ca, wi = ABSENT_CORRECT, gold.get(it["question_id"], ("", []))[1]
            else:
                ca, wi = gold.get(it["question_id"], (ABSENT_CORRECT, []))
            v = judge(it["question"], ca, wi, r["response"])
            a = cache[k]
            return (v is not None
                    and v.get("correctness") == a.get("correctness"),
                    v is not None
                    and bool(v.get("confabulation")) == bool(a.get("confabulation")))

        with cf.ThreadPoolExecutor(max_workers=5) as ex:
            res = list(ex.map(one, pick))
        out[model] = {
            "n": len(res),
            "correctness_agreement": sum(1 for a, _b in res if a) / max(len(res), 1),
            "confabulation_agreement": sum(1 for _a, b in res if b) / max(len(res), 1),
        }
        print(f"  {model:16s} n={out[model]['n']:3d}  correctness "
              f"{out[model]['correctness_agreement']:.2f}  confab "
              f"{out[model]['confabulation_agreement']:.2f}", flush=True)

    jdump({"note": "same pinned judge, re-judged; NO BAR -- disclosure only",
           "judge": JUDGE_MODEL, "rubric_sha256": rubric_sha, "per_candidate": out},
          E2 / "judge_spotcheck.json")
    print("wrote judge_spotcheck.json")


if __name__ == "__main__":
    main()
