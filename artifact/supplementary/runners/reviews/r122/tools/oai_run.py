# -*- coding: utf-8 -*-
"""oai_run.py -- R122 T3 and T4: the OpenAI lanes on the 444-item counterfactual set. Registrations reviews/r122/registrations/
ADDENDUM_R122_MINI_K5.md (T3) and ADDENDUM_R122_CF2_P1.md (T4); their registered-text sha256 asserted at start against FREEZE_R122.md.

Lanes
  MINI5    T3  gpt-4.1-mini, the frozen P0 texts (prompts_e1, digests asserted by run_cf at import), arms INDEXED-V2 and INDEXED-V3,
               k = 5, temperature UNSET (the provider default; D-R122-1), max_tokens 200; draw-major over the 888 (item, arm) units.
  P1LUNA   T4  gpt-5.6-luna, the frozen P1 system text (reviews/r121/tools/prompts_p1.SYSTEM_P1, sha c3c9a8e2... asserted) with P0's
               USER_INDEXED, arm INDEXED-V2, k = 5, E5's settings (reasoning effort and temperature unset, max_completion_tokens 2048),
               raw Chat Completions, draw-major over the 444.
  P1MINI   T4  gpt-4.1-mini, the P1 system text, INDEXED-V2, k = 1, temperature 0, max_tokens 200 (the recorded mini lane's settings).

One hard cap for the whole batch: 5.00 USD, metered from every R122 rows file at the page prices below, checked before every call;
eight workers; resume key (unit_id, arm, draw). Served identifier asserted on every row (E1.7 rule). No Anthropic call anywhere.

Subcommands:  lock | probe <lane> | project | run <lane> [--draws 1,2,3,4,5]
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

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r122_common as C  # noqa: E402
sys.path.insert(0, str(C.ROOT / "reviews" / "r121" / "tools"))
import cf2_run as C2  # noqa: E402  (re-points run_cf to the CF-2 cell; asserts the prompts_e1 digests at import)
import prompts_p1 as P1  # noqa: E402  (asserts P1's construction and the P0 digests at import)
import cf2_openai as OAI  # noqa: E402  (E5's price function)

RC = C2.RC
REG_T3, REG_T4 = "ADDENDUM_R122_MINI_K5.md", "ADDENDUM_R122_CF2_P1.md"
P1_SHA = "c3c9a8e2b9798b50aa5a8f091f382b550e296f973f0c9af09d7fa38442cc7ce4"
CAP = 5.00
WORKERS = 8
PRICES = {  # USD per million, OpenAI's model pages as read on 2026-09-18 (E5) and 2026-09-19 (mini's cached rate)
    "gpt-4.1-mini": dict(inp=0.40, cached=0.10, out=1.60, write_mult=1.0),
    "gpt-5.6-luna": dict(inp=0.20, cached=0.02, out=1.20, write_mult=1.25),
}
LANES = {
    "MINI5": dict(task="T3", reg=REG_T3, model="gpt-4.1-mini", prompt="P0", arms=("INDEXED-V2", "INDEXED-V3"), k=5, temperature=None, max_tokens=200, kind="chat",
                  probe_line=0.0015),
    "P1LUNA": dict(task="T4", reg=REG_T4, model="gpt-5.6-luna", prompt="P1", arms=("INDEXED-V2",), k=5, temperature=None, max_completion_tokens=2048, kind="raw",
                   probe_line=0.0010),
    "P1MINI": dict(task="T4", reg=REG_T4, model="gpt-4.1-mini", prompt="P1", arms=("INDEXED-V2",), k=1, temperature=0.0, max_tokens=200, kind="chat",
                   probe_line=0.0015),
}
LOCK = C.ROWS / "lock_r122_oai.json"
PROBES = C.ROWS / "probes_r122_oai.json"
OAI.MODELS.update({m: dict(code=m, **p) for m, p in PRICES.items()})     # E5's price() reads MODELS[model]; extended in memory only


def rows_path(lane):
    return C.ROWS / f"rows_{lane}.jsonl"


def setup():
    shas = {REG_T3: C.assert_frozen(REG_T3), REG_T4: C.assert_frozen(REG_T4)}
    assert P1.p1_sha256() == P1_SHA, "P1 SYSTEM TEXT SHA MISMATCH -- STOP"
    assert RC.P.file_sha256() == RC.E1_FILE_SHA and RC.P.texts_sha256() == RC.E1_TEXTS_SHA
    assert len(RC.CELL) == 444
    C.load_env()
    assert os.environ.get("OPENAI_API_KEY"), "no OPENAI_API_KEY"
    os.environ.pop("ANTHROPIC_API_KEY", None)          # no Anthropic call in this batch, by construction
    return shas


def prompts_for(u, arm, prompt):
    sysm, user = RC.prompts_for(u, arm)
    if prompt == "P1":
        sysm = P1.SYSTEM_P1
    return sysm, user


def call_once(lane, u, arm, draw):
    from openai import OpenAI
    cfg = LANES[lane]
    sysm, user = prompts_for(u, arm, cfg["prompt"])
    cl = OpenAI(max_retries=2, timeout=120)
    kw = dict(model=cfg["model"], messages=[{"role": "system", "content": sysm}, {"role": "user", "content": user}])
    if cfg["kind"] == "chat":
        kw["max_tokens"] = cfg["max_tokens"]
        if cfg["temperature"] is not None:
            kw["temperature"] = cfg["temperature"]
    else:
        kw["max_completion_tokens"] = cfg["max_completion_tokens"]
    r = cl.chat.completions.create(**kw)
    raw = r.model_dump(mode="json"); usage = raw.get("usage") or {}
    text = r.choices[0].message.content
    usd, cached, write, reasoning = OAI.price(cfg["model"], usage)
    row = RC.make_row(u, arm, cfg["model"], draw, text, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0), (PRICES[cfg["model"]]["inp"], PRICES[cfg["model"]]["out"]), 1.0, r.model)
    row.update({"lane": lane, "prompt": cfg["prompt"], "temperature": cfg["temperature"], "usd": usd, "tok_cached": cached, "tok_cache_write": write, "tok_reasoning": reasoning,
                "finish_reason": r.choices[0].finish_reason, "usage": usage, "when": dt.datetime.now().isoformat(timespec="seconds")})
    return row


def spent_all():
    tot = 0.0
    for lane in LANES:
        p = rows_path(lane)
        if p.exists():
            tot += sum(json.loads(l).get("usd", 0.0) for l in io.open(p, encoding="utf-8") if l.strip())
    if PROBES.exists():
        tot += sum(v.get("usd", 0.0) for v in C.jload(PROBES).values())
    return tot


def cmd_lock():
    shas = setup()
    rec = {"registrations": shas, "p1_system_sha256": P1_SHA, "p0_file_sha256": RC.E1_FILE_SHA, "p0_texts_sha256": RC.E1_TEXTS_SHA, "cell": 444, "cap_usd_batch": CAP,
           "lanes": {k: {kk: vv for kk, vv in v.items()} for k, v in LANES.items()}, "prices_per_million": PRICES, "order": "draw-major per lane, 8 workers; lane order P1MINI, P1LUNA, MINI5",
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    C.jdump(rec, LOCK); print(json.dumps(rec, indent=1))


def cmd_probe(lane):
    setup(); assert LOCK.exists(), "lock first"
    cfg = LANES[lane]; u = C2.units(cfg["arms"][0])[0]
    row = call_once(lane, u, cfg["arms"][0], 0)
    ok = cfg["model"] in row["served_model"]
    rec = {"lane": lane, "model": cfg["model"], "served": row["served_model"], "identifier_ok": ok, "tok_in": row["tok_in"], "tok_out": row["tok_out"], "tok_cached": row["tok_cached"],
           "tok_reasoning": row["tok_reasoning"], "usd": round(row["usd"], 6), "probe_line": cfg["probe_line"], "under_line": row["usd"] <= cfg["probe_line"], "parsed": row["status"],
           "sample": row["text"][:200], "when": row["when"]}
    d = C.jload(PROBES) if PROBES.exists() else {}
    d[lane] = rec; C.jdump(d, PROBES)
    print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")
    if not rec["under_line"]:
        raise SystemExit("probe per-call cost over the line -- STOP")


def projection(pr):
    """Expected spend per lane from the probes: draw 1 at the input rate, draws 2..k at the cached rate on the prompt (the draw-major order), output at the probe's tokens;
    the no-cache figure beside (every draw at the input rate)."""
    out = {}
    for lane, cfg in LANES.items():
        if lane not in pr:
            continue
        p = PRICES[cfg["model"]]; n_units = len(cfg["arms"]) * 444; tin = pr[lane]["tok_in"]; tout = max(pr[lane]["tok_out"], 1)
        d1 = n_units * (tin * p["inp"] * (p["write_mult"] if cfg["k"] > 1 else 1.0) + tout * p["out"]) / 1e6
        dk = (cfg["k"] - 1) * n_units * (tin * p["cached"] + tout * p["out"]) / 1e6
        nocache = cfg["k"] * n_units * (tin * p["inp"] + tout * p["out"]) / 1e6
        out[lane] = {"calls": cfg["k"] * n_units, "expected_usd": round(d1 + dk, 4), "no_cache_usd": round(nocache, 4), "tok_in": tin, "tok_out": tout}
    out["total_expected"] = round(sum(v["expected_usd"] for k, v in out.items() if k in LANES), 4)
    out["total_no_cache"] = round(sum(v["no_cache_usd"] for k, v in out.items() if k in LANES), 4)
    out["spent_so_far"] = round(spent_all(), 4); out["cap"] = CAP
    return out


def cmd_project():
    setup(); pr = C.jload(PROBES)
    out = projection(pr); print(json.dumps(out, indent=1))
    C.jdump(out, C.RESULTS / "projection_r122_oai.json")
    if out["total_expected"] + out["spent_so_far"] > CAP:
        raise SystemExit("PROJECTION ABOVE THE CAP -- STOP")


def cmd_run(lane, draws):
    setup(); cfg = LANES[lane]
    pr = C.jload(PROBES)[lane]; assert pr["identifier_ok"] and pr["under_line"]
    units = [(u, arm) for arm in cfg["arms"] for u in C2.units(arm)]
    path = rows_path(lane); done = set()
    if path.exists():
        for l in io.open(path, encoding="utf-8"):
            if l.strip():
                r = json.loads(l); done.add((r["unit_id"], r["arm"], int(r["draw"])))
    lock = threading.Lock(); state = {"spent": spent_all(), "n": 0, "halted": False}
    print(f"{lane}: batch spent so far ${state['spent']:.4f} of the ${CAP} cap; {len(units)} units x draws {draws}", flush=True)

    def work(job):
        (u, arm), d = job
        if state["halted"]:
            return None
        with lock:
            if state["spent"] >= CAP:
                state["halted"] = True; return None
        try:
            row = call_once(lane, u, arm, d)
        except Exception as e:  # noqa: BLE001
            row = {"unit_id": u["unit_id"], "arm": arm, "model": cfg["model"], "draw": d, "fok": None, "nok": None, "status": f"ERROR: {type(e).__name__}: {str(e)[:200]}",
                   "served_model": None, "tok_in": 0, "tok_out": 0, "usd": 0.0, "text": "", "lane": lane, "prompt": cfg["prompt"], "when": dt.datetime.now().isoformat(timespec="seconds")}
        with lock:
            with io.open(path, "a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
            state["spent"] += row.get("usd", 0.0); state["n"] += 1
            if state["n"] % 100 == 0:
                print(f"  {lane} draw {d}: {state['n']} rows this session, batch spent ${state['spent']:.4f}", flush=True)
        return row

    for d in draws:
        jobs = [((u, arm), d) for (u, arm) in units if (u["unit_id"], arm, d) not in done]
        if not jobs:
            print(f"{lane} draw {d}: nothing to do"); continue
        t0 = time.time()
        with cf.ThreadPoolExecutor(WORKERS) as ex:
            list(ex.map(work, jobs))
        print(f"{lane} draw {d}: {len(jobs)} calls in {time.time() - t0:.0f}s; batch spent ${state['spent']:.4f}", flush=True)
        if state["halted"]:
            print("CAP REACHED -- halted; the partial draw is discarded at scoring and disclosed"); break


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "lock":
        cmd_lock()
    elif cmd == "probe":
        cmd_probe(sys.argv[2])
    elif cmd == "project":
        cmd_project()
    elif cmd == "run":
        lane = sys.argv[2]; draws = [int(x) for x in (sys.argv[4].split(",") if len(sys.argv) > 4 and sys.argv[3] == "--draws" else range(1, LANES[lane]["k"] + 1))]
        cmd_run(lane, draws)
    else:
        raise SystemExit("usage: oai_run.py lock | probe <lane> | project | run <lane> [--draws 1,2]")
