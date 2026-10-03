"""
run_judge_e3.py -- FR's pinned confabulation judge, unmodified. Counts only on stdout.

  judge   claude-sonnet-4-6 via `claude -p`, temperature 0, subscription lane
  rubric  LifeMemEval/evaluate_e2e.py JUDGE_SYSTEM_PROMPT + JUDGE_USER_TEMPLATE,
          IMPORTED BY AST from that file rather than copied, so drift is
          impossible. Byte-identical to audit/judge_panel/PANEL_PACKET.txt, which
          is what makes E3's confabulation numbers comparable to E2's and to FR's
          12.0% / 24.2%.

WHAT IS FED IN. The rubric needs a `correct_answer` and `wrong_indicators`. For
PRESENT and PRESENT-NEGATIVE cells they come from LifeMemEval's own question file
-- and the KEY-VALID-ONLY cell policy (PREREG_E3 section 2) guarantees the
authored key describes a state the rung has reached, which is exactly what D48
required and what the ladder placement bought. For ABSENT cells the correct
behaviour is abstention, so the slot is filled with the frozen sentence below and
the question's own wrong-answer indicators are kept where they exist, so stating
a stale value still flags. THE RUBRIC BYTES ARE UNCHANGED; only the data differs.

D43-E2 IS FIXED HERE, not merely noted: a FAILED verdict is NOT written to the
cache, so a retry actually retries. E1's ledger recorded that a cache which
stores failures makes retry a no-op; this runner refuses to store them.

EVAL HYGIENE: prints counts and costs. Never prints an answer, a verdict, or a
score. Computes no metric.

Usage:  python e3_metamemory/tools/run_judge_e3.py --split calibration
"""

from __future__ import annotations

import concurrent.futures as cf
import io
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e3_common import E3, jdump, jload, load_cells, sha            # noqa: E402

CLAUDE = shutil.which("claude") or "claude"
JUDGE_MODEL = "claude-sonnet-4-6"
WORKERS = 5
TIMEOUT = 180

ABSENT_CORRECT = ("The store contains no information on this topic; the assistant "
                  "should say it does not know.")


def load_rubric():
    """Lift FR's judge prompts out of evaluate_e2e.py by AST, without running it."""
    import ast
    p = ROOT / "LifeMemEval" / "evaluate_e2e.py"
    src = io.open(p, encoding="utf-8").read()
    want = ("JUDGE_SYSTEM_PROMPT", "JUDGE_USER_TEMPLATE")
    found, segs = {}, []
    for node in ast.parse(src).body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id in want):
            found[node.targets[0].id] = ast.literal_eval(node.value)
            segs.append(ast.get_source_segment(src, node))
    missing = set(want) - set(found)
    assert not missing, f"rubric constants not found in evaluate_e2e.py: {missing}"
    return found[want[0]], found[want[1]], sha(*segs)


def last_json(s):
    d, st, esc, start = 0, False, False, -1
    for i, c in enumerate(s):
        if esc:
            esc = False; continue
        if c == "\\":
            esc = True; continue
        if c == '"':
            st = not st; continue
        if st:
            continue
        if c == "{":
            if d == 0:
                start = i
            d += 1
        elif c == "}":
            d -= 1
            if d == 0 and start >= 0:
                try:
                    return json.loads(s[start:i + 1])
                except Exception:                                 # noqa: BLE001
                    pass
    return None


def main():
    split = sys.argv[sys.argv.index("--split") + 1]
    SYS_P, USER_T, rubric_sha = load_rubric()
    print(f"rubric imported from LifeMemEval/evaluate_e2e.py, sha {rubric_sha[:16]}...")

    gold = {}
    for q in jload(ROOT / "LifeMemEval" / "lifemembench_questions.json"):
        gold[q["id"]] = (q.get("correct_answer") or "",
                         q.get("wrong_answer_indicators") or [])

    cells = {c["cell_id"]: c for c in load_cells()["cells"]}
    answers = jload(E3 / f"answers_{split}.json")["rows"]
    cache_path = E3 / "cache" / f"judgments_{split}.json"
    cache = jload(cache_path) if cache_path.exists() else {}

    todo, seen = [], set()
    for a in answers:
        key = f"{a['cell_id']}|{a['response_sha'][:24]}"
        if key in seen:
            continue
        seen.add(key)
        if cache.get(key, {}).get("status") == "OK":
            continue
        c = cells[a["cell_id"]]
        if c["label"] == "ABSENT":
            ca, wi = ABSENT_CORRECT, gold.get(c["question_id"], ("", []))[1]
        else:
            ca, wi = gold.get(c["question_id"], (ABSENT_CORRECT, []))
        todo.append((key, c["question"], ca, wi, a["response"]))

    print(f"split={split}  answers={len(answers)}  distinct={len(seen)}  "
          f"cached_OK={len(seen)-len(todo)}  to judge={len(todo)}")

    env = {k: v for k, v in os.environ.items()
           if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")}

    def run(job):
        key, q, ca, wi, resp = job
        user = USER_T.format(question=q, correct_answer=ca,
                             wrong_indicators=", ".join(wi) if wi else "(none)",
                             response=resp)
        for attempt in range(3):
            try:
                t0 = time.perf_counter()
                r = subprocess.run(
                    [CLAUDE, "-p", user, "--model", JUDGE_MODEL,
                     "--output-format", "json", "--system-prompt", SYS_P,
                     "--exclude-dynamic-system-prompt-sections",
                     "--disallowedTools",
                     "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch,Task,"
                     "NotebookEdit,TodoWrite", "--setting-sources", ""],
                    capture_output=True, text=True, encoding="utf-8",
                    errors="replace", timeout=TIMEOUT, env=env)
                dt = time.perf_counter() - t0
                o = json.loads(r.stdout) if r.stdout.strip() else {}
                v = last_json(o.get("result", "") or "")
                if v and v.get("correctness"):
                    return key, {"correctness": v.get("correctness"),
                                 "confabulation": bool(v.get("confabulation")),
                                 "reasoning": str(v.get("reasoning", ""))[:300],
                                 "seconds": round(dt, 2),
                                 "metered_equiv_usd": o.get("total_cost_usd"),
                                 "status": "OK"}
            except Exception:                                     # noqa: BLE001
                pass
            time.sleep(1 + attempt)
        # D43-E2: a failure is NOT cached, so a re-run actually re-attempts it.
        return key, None

    done = 0
    if todo:
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
            for key, verdict in ex.map(run, todo):
                if verdict is not None:
                    cache[key] = verdict
                done += 1
                if done % 50 == 0:
                    jdump(cache, cache_path)
                    print(f"  {done}/{len(todo)}", flush=True)
    jdump(cache, cache_path)

    ok = sum(1 for k in seen if cache.get(k, {}).get("status") == "OK")
    fail = len(seen) - ok
    lat = [cache[k]["seconds"] for k in seen if cache.get(k, {}).get("seconds")]
    eq = sum(cache[k].get("metered_equiv_usd") or 0 for k in seen if k in cache)
    jdump({"split": split, "judge_model": JUDGE_MODEL, "rubric_sha256": rubric_sha,
           "n_distinct": len(seen), "n_ok": ok, "n_failed": fail,
           "failures_not_cached": True,
           "metered_equivalent_usd_computed_not_paid": eq,
           "mean_seconds": (sum(lat) / len(lat)) if lat else None},
          E3 / f"judge_census_{split}.json")
    print(f"  judged OK {ok}, missing {fail}")
    if lat:
        print(f"  latency mean {sum(lat)/len(lat):.2f}s over {len(lat)} live calls")
    print(f"  metered-equivalent ${eq:.2f} (computed-not-paid; subscription lane)")
    print(f"wrote judgments_{split}.json -- no verdict printed, no metric computed")


if __name__ == "__main__":
    main()
