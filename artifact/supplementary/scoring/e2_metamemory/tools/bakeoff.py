"""
bakeoff.py -- E2 Amendment 3 STEP 2: answerer bake-off on the CALIBRATION SPLIT.

Each candidate answers the 132 calibration items across the three frozen context
states, from the frozen retrieval artifact. Scored with the UNCHANGED judge. The
frozen selection rule is then applied mechanically.

  RULE (E2_AMENDMENT_3 section 3): on calibration, state S1, PRESENT items whose
  retrieved context contains the gold (gold_coverage >= 0.5) -- mean behaviour-
  typed credit >= 0.55. Among clearers: gpt-5.4 first (FR-comparability), else
  the cheapest by measured cost per answer. If NONE clears, STOP.

The answerer model string is the ONLY thing that varies. Prompt, judge, judge
prompts, context states, retrieval artifact, credit rule: all unchanged.

Usage:  python e2_metamemory/tools/bakeoff.py [--only MODEL]
"""

from __future__ import annotations

import collections
import concurrent.futures as cf
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import e2_api as api                                              # noqa: E402
from e2_common import (E2, S0, S1, S2, answer_messages, jdump,    # noqa: E402
                       jload, load_items, sha)

CANDIDATES = [
    ("gpt-4.1-mini", 0.40, 1.60, "study constant"),
    ("gpt-4.1", 2.00, 8.00, "list price, NOT re-verified"),
    ("gpt-5.4-mini", None, None, "measured"),
    ("gpt-5.4", None, None, "measured"),
]
BAR = 0.55
WORKERS = 12
MAX_TOK = 220


def credit_of(label, correctness):
    if correctness is None:
        return None
    if label == "ABSENT":
        return 1.0 if correctness == "ABSTAIN" else 0.0
    return {"CORRECT": 1.0, "PARTIAL": 0.5, "WRONG": 0.0, "ABSTAIN": 0.0}.get(
        correctness, 0.0)


def main():
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    items = {i["item_id"]: i for i in load_items() if i["split"] == "calibration"}
    fr = {r["item_id"]: r for r in jload(E2 / "retrieval_frozen.json")["rows"]}
    tags = sorted(items)
    print(f"bake-off on {len(tags)} calibration items x 3 context states")

    allrows = {}
    for model, pin, pout, prov in CANDIDATES:
        if only and model != only:
            continue
        jobs = []
        for t in tags:
            facts = fr[t]["facts"]
            for state, f in ((S0, []), (S1, facts), (S2, facts)):
                jobs.append((t, items[t]["question"], state, tuple(f)))

        def run(job):
            t, q, state, facts = job
            msgs = answer_messages(list(facts), q, state)
            ctx = sha(state, *facts)
            r = api.call_text_model(f"{t}|{ctx[:16]}|d1", f"bake-{state}", msgs,
                                    model=model, max_tokens=MAX_TOK)
            api.check_cap()
            txt = (r["content"] or "").strip()
            return {"item_id": t, "state": state, "response": txt,
                    "response_sha": sha(t, txt), "cached": r["cached"],
                    "prompt_tokens": r.get("prompt_tokens"),
                    "completion_tokens": r.get("completion_tokens"),
                    "reasoning_tokens": r.get("reasoning_tokens", 0),
                    "params": r.get("params")}

        out = []
        try:
            with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
                for n, rec in enumerate(ex.map(run, jobs), 1):
                    out.append(rec)
                    if n % 150 == 0:
                        api.flush()
                        print(f"    {model} {n}/{len(jobs)}  "
                              f"${api.spend()[0]:.4f}", flush=True)
        finally:
            api.flush()
        allrows[model] = out
        empty = sum(1 for r in out if not r["response"])
        print(f"  {model:16s} {len(out)} answers, {empty} empty, "
              f"params={out[0]['params']}", flush=True)
        jdump({"model": model, "n": len(out), "rows": out},
              E2 / f"bakeoff_answers_{model}.json")

    # ------------------------------------------------------------- judge them
    for model in allrows:
        jdump({"split": f"bakeoff-{model}", "k": 1, "s2_all": True,
               "n": len(allrows[model]), "answerer_model": model,
               "rows": allrows[model]}, E2 / f"answers_bakeoff-{model}.json")
        print(f"  judging {model}...", flush=True)
        subprocess.run([sys.executable,
                        str(Path(__file__).parent / "run_judge.py"),
                        "--split", f"bakeoff-{model}"], check=True)

    # ------------------------------------------------------------ competence
    table = {}
    for model, rows in allrows.items():
        judg = jload(E2 / "cache" / f"judgments_bakeoff-{model}.json")
        cell = {}
        for r in rows:
            v = judg.get(f"{r['item_id']}|{r['response_sha'][:24]}", {})
            cell[(r["item_id"], r["state"])] = (
                credit_of(items[r["item_id"]]["label_final"], v.get("correctness")),
                bool(v.get("confabulation")), v.get("correctness"))

        def m(pred, state, idx=0):
            v = [cell[(t, state)][idx] for t in tags
                 if pred(t) and cell.get((t, state)) and cell[(t, state)][0] is not None]
            return (sum(v) / len(v)) if v else None, len(v)

        gold = lambda t: (items[t]["label_final"] == "PRESENT"                 # noqa: E731
                          and (fr[t]["gold_coverage"] or 0) >= 0.5)
        bar_val, bar_n = m(gold, S1)
        tin = sum(r["prompt_tokens"] or 0 for r in rows)
        tout = sum(r["completion_tokens"] or 0 for r in rows)
        rtok = sum(r.get("reasoning_tokens") or 0 for r in rows)
        pin, pout = next((a, b) for (mm, a, b, _p) in CANDIDATES if mm == model)[:2] \
            if False else (None, None)
        for (mm, a, b, _p) in CANDIDATES:
            if mm == model:
                pin, pout = a, b
        usd = (tin / 1e6 * pin + tout / 1e6 * pout) if pin else None
        table[model] = {
            "BAR_credit_S1_PRESENT_gold": bar_val, "BAR_n": bar_n,
            "clears": (bar_val is not None and bar_val >= BAR),
            "credit_S1_PRESENT": m(lambda t: items[t]["label_final"] == "PRESENT", S1)[0],
            "credit_S1_PN": m(lambda t: items[t]["label_final"] == "PRESENT-NEGATIVE", S1)[0],
            "credit_S1_ABSENT": m(lambda t: items[t]["label_final"] == "ABSENT", S1)[0],
            "credit_S0_ABSENT": m(lambda t: items[t]["label_final"] == "ABSENT", S0)[0],
            "confab_S1_ablation": m(
                lambda t: items[t]["label_final"] == "ABSENT"
                and not str(items[t]["question_id"]).startswith("probe"), S1, 1)[0],
            "confab_S1_probe": m(
                lambda t: str(items[t]["question_id"]).startswith("probe"), S1, 1)[0],
            "tokens_in": tin, "tokens_out": tout, "reasoning_tokens": rtok,
            "usd_total": usd,
            "usd_per_answer": (usd / len(rows)) if usd else None,
            "price_provenance": next(p for (mm, _a, _b, p) in CANDIDATES if mm == model),
            "params_used": rows[0]["params"],
            "temperature0_comparable": "temperature" in (rows[0]["params"] or []),
        }

    clearing = [m2 for m2, v in table.items() if v["clears"]]
    if not clearing:
        winner, why = None, ("NO CANDIDATE CLEARS 0.55 -- per the frozen rule this is "
                             "a finding about the task, not a selection failure. STOP.")
    elif "gpt-5.4" in clearing:
        winner, why = "gpt-5.4", ("clears the bar and is FR's own answerer, so "
                                  "absolute FR-comparability conceded under D31-E2 is "
                                  "RESTORED for H-C2")
    else:
        priced = [(table[m2]["usd_per_answer"], m2) for m2 in clearing
                  if table[m2]["usd_per_answer"] is not None]
        winner = min(priced)[1] if priced else sorted(clearing)[0]
        why = "cheapest clearing candidate by measured cost per answer"

    jdump({"bar": BAR, "rule": "E2_AMENDMENT_3 section 3, frozen before any "
                               "candidate answered",
           "table": table, "clearing": clearing, "winner": winner, "why": why},
          E2 / "bakeoff_report.json")
    if winner:
        jdump({"answerer_model": winner, "selected_by": why, "bar": BAR,
               "bar_value": table[winner]["BAR_credit_S1_PRESENT_gold"]},
              E2 / "ANSWERER_FROZEN.json")

    print("\n" + "=" * 100)
    print(f"BAKE-OFF — bar: mean credit >= {BAR} on S1, PRESENT items with gold retrieved")
    print("=" * 100)
    print(f"{'model':16s}{'BAR':>8s}{'n':>4s}{'clears':>8s}{'S1 PRES':>9s}"
          f"{'S1 PN':>8s}{'S1 ABS':>8s}{'cf abl':>8s}{'cf prb':>8s}{'$/ans':>10s}")
    for m2, v in table.items():
        b = v["BAR_credit_S1_PRESENT_gold"]
        print(f"{m2:16s}{(b if b is not None else float('nan')):8.3f}{v['BAR_n']:4d}"
              f"{('YES' if v['clears'] else 'no'):>8s}"
              f"{v['credit_S1_PRESENT']:9.3f}{v['credit_S1_PN']:8.3f}"
              f"{v['credit_S1_ABSENT']:8.3f}{v['confab_S1_ablation']:8.3f}"
              f"{v['confab_S1_probe']:8.3f}"
              f"{(v['usd_per_answer'] or float('nan')):10.6f}")
    for m2, v in table.items():
        print(f"  {m2:16s} params={v['params_used']} temp0-comparable="
              f"{v['temperature0_comparable']} reasoning_tokens={v['reasoning_tokens']}")
    print(f"\nWINNER: {winner}\n  because {why}")
    print(f"E2 cumulative ${api.spend()[0]:.4f} of ${api.E2_CAP_USD}")


if __name__ == "__main__":
    main()
