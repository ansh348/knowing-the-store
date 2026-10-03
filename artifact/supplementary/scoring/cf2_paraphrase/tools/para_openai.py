"""para_openai.py -- the added readers, not registered (the dated line of 2026-09-21 below the marker of ADDENDUM_PARA.md):
GPT-5.6 Luna and GPT-5.6 Sol on the paraphrases of the 124 screen-passing pairs, raw OpenAI Chat Completions with the frozen
prompts_e1 texts and no other system text, reasoning effort and temperature unset, max_completion_tokens 2048 (the settings of
their Table 1 rows, ADDENDUM_CF2_OPENAI.md), five draws each, draw-major, eight workers, resume on (unit_id, arm, draw).
Arm INDEXED-V2 only: the Table 1 rows and the recorded originals (cf2/rows/rows_LUNA.jsonl, rows_SOL.jsonl) are v2 only, and
both arms project over the $14 cap (see the projection printed by `probe`). Cap $14 for both models together, metered from the
rows at OpenAI's page prices of 2026-09-18 (cf2_openai.MODELS). No prediction is attached; reported beside the registered
readers and labelled not registered. Rows: cf2_paraphrase/rows/rows_LUNA.jsonl, rows_SOL.jsonl.

  python cf2_paraphrase/tools/para_openai.py probe <model>     one call on the first unit; served identifier; projection printed
  python cf2_paraphrase/tools/para_openai.py run <model>       the five draws (PARA_POP=all124 is set by the script)
"""
from __future__ import annotations

import concurrent.futures as cf
import datetime as dt
import io
import json
import os
import sys
import threading
import time
from pathlib import Path

os.environ["PARA_POP"] = "all124"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_para as SP  # noqa: E402  (PARA_POP=all124: units over the 124 pairs; asserts the prompts_e1 digests via run_cf)
from para_common import PARA, jload  # noqa: E402

RC = SP.RC
ARM = "INDEXED-V2"
K = 5
CAP = 14.00
WORKERS = 8
MODELS = {   # OpenAI page prices of 2026-09-18 as ADDENDUM_CF2_OPENAI.md records them (cf2_openai.MODELS)
    "gpt-5.6-luna": dict(code="LUNA", inp=0.20, cached=0.02, out=1.20, write_mult=1.25),
    "gpt-5.6-sol": dict(code="SOL", inp=4.00, cached=0.40, out=20.00, write_mult=1.25),
}
ROWS = PARA / "rows"
PROBES = PARA / "probes_openai.json"
CF2_ROWS = PARA.parent / "r82_counterfactual" / "cf2" / "rows"


def rows_path(model):
    return ROWS / f"rows_{MODELS[model]['code']}.jsonl"


def price(model, usage):
    m = MODELS[model]
    pt = usage.get("prompt_tokens", 0); ct = usage.get("completion_tokens", 0)
    det = usage.get("prompt_tokens_details") or {}
    cached = det.get("cached_tokens", 0) or 0
    write = det.get("cache_write_tokens", 0) or 0
    plain = max(0, pt - cached - write)
    usd = (plain * m["inp"] + write * m["inp"] * m["write_mult"] + cached * m["cached"] + ct * m["out"]) / 1e6
    return usd, cached, write, ((usage.get("completion_tokens_details") or {}).get("reasoning_tokens", 0) or 0)


def call_once(model, u, arm, draw):
    from openai import OpenAI
    sysm, user = RC.prompts_for(u, arm)
    cl = OpenAI(max_retries=2, timeout=120)
    r = cl.chat.completions.create(model=model, max_completion_tokens=2048,
                                   messages=[{"role": "system", "content": sysm}, {"role": "user", "content": user}])
    raw = r.model_dump(mode="json"); usage = raw.get("usage") or {}
    usd, cached, write, reasoning = price(model, usage)
    row = RC.make_row(u, arm, model, draw, r.choices[0].message.content, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0),
                      (MODELS[model]["inp"], MODELS[model]["out"]), 1.0, r.model)
    row.update({"usd": usd, "tok_cached": cached, "tok_cache_write": write, "tok_reasoning": reasoning, "finish_reason": r.choices[0].finish_reason,
                "usage": usage, "when": dt.datetime.now().isoformat(timespec="seconds")})
    return row


def spent(path):
    return sum(json.loads(l).get("usd", 0.0) for l in io.open(path, encoding="utf-8") if l.strip()) if path.exists() else 0.0


def cf2_per_call(model):
    p = CF2_ROWS / f"rows_{MODELS[model]['code']}.jsonl"
    rows = [json.loads(l) for l in io.open(p, encoding="utf-8") if l.strip()]
    return sum(r.get("usd", 0.0) for r in rows) / len(rows), len(rows)


def cmd_probe(model):
    RC.load_env(); assert os.environ.get("OPENAI_API_KEY"), "no OPENAI_API_KEY"
    u = SP.units(ARM)[0]; n_units = len(SP.units(ARM))
    row = call_once(model, u, ARM, 0)
    ok = model in row["served_model"]
    pc, n_cf2 = cf2_per_call(model)
    proj_v2 = pc * n_units * K
    rec = {"model": model, "served": row["served_model"], "identifier_ok": ok, "tok_in": row["tok_in"], "tok_out": row["tok_out"], "tok_cached": row["tok_cached"],
           "tok_cache_write": row["tok_cache_write"], "tok_reasoning": row["tok_reasoning"], "usd": round(row["usd"], 6), "parsed": row["status"], "n_units": n_units, "k": K, "arm": ARM,
           "cf2_per_call_usd": round(pc, 6), "cf2_rows": n_cf2,
           "projection_v2_only_usd": round(proj_v2, 4), "projection_both_arms_usd": round(proj_v2 * 2.03, 4), "cap_both_models": CAP,
           "spent_both_models_so_far": round(sum(spent(rows_path(m)) for m in MODELS), 4), "sample": row["text"][:200], "when": row["when"]}
    d = jload(PROBES) if PROBES.exists() else {}
    d[model] = rec
    io.open(PROBES, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")


def cmd_run(model):
    RC.load_env()
    pr = jload(PROBES)[model]; assert pr["identifier_ok"]
    units = SP.units(ARM); path = rows_path(model); other = [rows_path(m) for m in MODELS if m != model][0]
    done = set()
    if path.exists():
        for l in io.open(path, encoding="utf-8"):
            if l.strip():
                r = json.loads(l); done.add((r["unit_id"], r["arm"], int(r["draw"])))
    lock = threading.Lock()
    state = {"mine": spent(path), "other": spent(other), "n": 0, "halted": False}
    print(f"{model}: spent so far mine ${state['mine']:.4f}, other ${state['other']:.4f}; cap ${CAP} both models; {len(units)} units x {K} draws, arm {ARM}", flush=True)

    def work(job):
        u, d = job
        if state["halted"]:
            return None
        with lock:
            if state["mine"] + state["other"] >= CAP:
                state["halted"] = True; return None
        row = None
        for attempt in (1, 2, 3):
            try:
                row = call_once(model, u, ARM, d); break
            except Exception as e:  # noqa: BLE001
                if attempt == 3:
                    row = {"unit_id": u["unit_id"], "arm": ARM, "model": model, "draw": d, "status": f"ERROR:{type(e).__name__}", "when": dt.datetime.now().isoformat(timespec="seconds")}
                else:
                    time.sleep(5 * attempt)
        with lock:
            state["mine"] += row.get("usd", 0.0); state["n"] += 1
            with io.open(path, "a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(row, sort_keys=True) + "\n")
            if state["n"] % 100 == 0:
                print(f"  {model} draw {d}: {state['n']} calls this run, lane ${state['mine']:.4f}, both ${state['mine'] + state['other']:.4f}", flush=True)
        return row

    for d in range(1, K + 1):
        jobs = [(u, d) for u in units if (u["unit_id"], ARM, d) not in done]
        if not jobs:
            print(f"{model} draw {d}: complete already", flush=True); continue
        t0 = time.time()
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
            list(ex.map(work, jobs))
        n_ok = sum(1 for l in io.open(path, encoding="utf-8") if l.strip() and json.loads(l).get("status") == "OK" and int(json.loads(l)["draw"]) == d)
        print(f"{model} draw {d} done in {time.time() - t0:.0f}s: OK rows {n_ok}/{len(units)}; lane ${state['mine']:.4f}, both ${state['mine'] + state['other']:.4f}", flush=True)
        if state["halted"]:
            print(f"{model}: CAP REACHED at draw {d}; stopping (whole draws scored, partial draws discarded)", flush=True); break
    print(f"{model} DONE; lane ${state['mine']:.4f}; both ${state['mine'] + state['other']:.4f}", flush=True)


if __name__ == "__main__":
    {"probe": cmd_probe, "run": cmd_run}[sys.argv[1]](sys.argv[2])
