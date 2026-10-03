"""
judge_spotcheck_e3.py -- 20-item independent-judge validity spot-check.

PREREG_E3 section 8: "20 rung-context items on E2's protocol -- blinded, selected
using only the pinned judge's own output. REPORTED, NO BAR", gating nothing.

E2's protocol, carried:
  selection   seeded sample stratified over the pinned judge's OWN verdict cells,
              so the slice is chosen without reference to any arm, any rung
              outcome or any hypothesis;
  blinding    the second judge sees the same rubric and the same four fields the
              pinned judge saw, and nothing that identifies the arm, the state,
              the rung or the first judge's verdict;
  model       gpt-5.6-sol via the Codex CLI if it is reachable, else the pinned
              rubric on a second Anthropic lane. The lane actually used is
              RECORDED with the result.

Reports agreement on the confabulation flag and four-way agreement on
correctness, against E2's reference (FR's slice: 88% confab, 85% four-way;
panel Fleiss kappa 0.834 across six models). NO BAR, NO GATE.

Usage:  python e3_metamemory/tools/judge_spotcheck_e3.py
"""

from __future__ import annotations

import collections
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

from e3_common import E3, jdump, jload, load_cells                 # noqa: E402
from run_judge_e3 import ABSENT_CORRECT, last_json, load_rubric    # noqa: E402

N = 20
SEED = 42
CLAUDE = shutil.which("claude") or "claude"
SECOND_MODEL = "claude-opus-4-1"       # a DIFFERENT model from the pinned judge
TIMEOUT = 180


def main():
    SYS_P, USER_T, rubric_sha = load_rubric()
    cells = {c["cell_id"]: c for c in load_cells()["cells"]}
    gold = {}
    for q in jload(ROOT / "LifeMemEval" / "lifemembench_questions.json"):
        gold[q["id"]] = (q.get("correct_answer") or "",
                         q.get("wrong_answer_indicators") or [])
    ans = jload(E3 / "answers_eval.json")["rows"]
    judg = jload(E3 / "cache" / "judgments_eval.json")

    # selection uses ONLY the pinned judge's own output: stratify over its verdict
    pool = collections.defaultdict(list)
    for a in ans:
        key = f"{a['cell_id']}|{a['response_sha'][:24]}"
        v = judg.get(key)
        if not v or v.get("status") != "OK":
            continue
        pool[(v["correctness"], bool(v["confabulation"]))].append((key, a))
    rng = random.Random(SEED)
    strata = sorted(pool)
    sample, i = [], 0
    while len(sample) < N and any(pool.values()):
        s = strata[i % len(strata)]
        i += 1
        if pool[s]:
            sample.append(pool[s].pop(rng.randrange(len(pool[s]))))
    print(f"selected {len(sample)} items over {len(strata)} pinned-judge verdict "
          f"strata, seed {SEED}; selection used no arm, rung or hypothesis")

    env = {k: v for k, v in os.environ.items()
           if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")}
    rows = []
    for key, a in sample:
        c = cells[a["cell_id"]]
        if c["label"] == "ABSENT":
            ca, wi = ABSENT_CORRECT, gold.get(c["question_id"], ("", []))[1]
        else:
            ca, wi = gold.get(c["question_id"], (ABSENT_CORRECT, []))
        user = USER_T.format(question=c["question"], correct_answer=ca,
                             wrong_indicators=", ".join(wi) if wi else "(none)",
                             response=a["response"])
        v2 = None
        for attempt in range(3):
            try:
                r = subprocess.run(
                    [CLAUDE, "-p", user, "--model", SECOND_MODEL,
                     "--output-format", "json", "--system-prompt", SYS_P,
                     "--exclude-dynamic-system-prompt-sections",
                     "--disallowedTools",
                     "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch,Task,"
                     "NotebookEdit,TodoWrite", "--setting-sources", ""],
                    capture_output=True, text=True, encoding="utf-8",
                    errors="replace", timeout=TIMEOUT, env=env)
                o = json.loads(r.stdout) if r.stdout.strip() else {}
                v2 = last_json(o.get("result", "") or "")
                if v2 and v2.get("correctness"):
                    break
            except Exception:                                     # noqa: BLE001
                pass
            time.sleep(1 + attempt)
        v1 = judg[key]
        rows.append({"key": key, "pinned_correctness": v1["correctness"],
                     "pinned_confab": bool(v1["confabulation"]),
                     "second_correctness": (v2 or {}).get("correctness"),
                     "second_confab": bool((v2 or {}).get("confabulation"))
                     if v2 else None,
                     "second_ok": bool(v2 and v2.get("correctness"))})
        print(f"  {len(rows)}/{len(sample)}", flush=True)

    ok = [r for r in rows if r["second_ok"]]
    confab_agree = sum(1 for r in ok if r["pinned_confab"] == r["second_confab"])
    four_agree = sum(1 for r in ok
                     if r["pinned_correctness"] == r["second_correctness"])
    out = {"protocol": "E2 judge-validity protocol, carried",
           "n_selected": len(rows), "n_second_judge_ok": len(ok),
           "second_judge_model": SECOND_MODEL,
           "pinned_judge_model": "claude-sonnet-4-6",
           "rubric_sha256": rubric_sha, "seed": SEED,
           "confab_agreement": confab_agree / len(ok) if ok else None,
           "four_way_agreement": four_agree / len(ok) if ok else None,
           "e2_reference": {"confab": 0.88, "four_way": 0.85,
                            "panel_fleiss_kappa": 0.834},
           "bar": None, "gates": "nothing", "rows": rows}
    jdump(out, E3 / "judge_spotcheck_e3.json")
    print("\n" + "=" * 88)
    print(f"JUDGE VALIDITY SPOT-CHECK -- {len(ok)}/{len(rows)} second verdicts parsed")
    print("=" * 88)
    print(f"  confabulation-flag agreement : {confab_agree}/{len(ok)} "
          f"({confab_agree/len(ok):.0%})   FR reference 88%")
    print(f"  four-way correctness agreement: {four_agree}/{len(ok)} "
          f"({four_agree/len(ok):.0%})   FR reference 85%")
    print("  REPORTED, NO BAR. This spot-check gates nothing.")
    print("wrote judge_spotcheck_e3.json")


if __name__ == "__main__":
    main()
