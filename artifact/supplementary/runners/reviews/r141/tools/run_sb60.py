# -*- coding: utf-8 -*-
"""run_sb60.py -- R141 Phase 1 (ADDENDUM_R141_SB60, frozen at f224177, registered text sha256 4fc25a8b...): the leak screen and the three OpenAI lanes on the
SB-60 texts. R125's call path is reused, not copied: reviews/r125/tools/r125_run.py's call_openai (R136's settings through the same Chat Completions shapes),
served_ok, the leak screen's rule (cf2_leakscreen: N 30, seed 42, threshold 3, gpt-4.1-mini at temperature 0, max_tokens 200) and its price function.

Subcommands:
  leak                 the leak screen on the 88 SB-60 texts (STOP if more than 3 of 30 correct)
  probe <lane>         one probe call on the first unit; the served identifier checked (a mismatch is a STOP for the lane)
  project              the per-lane projection from the probes against the remaining cap (Sol dropped first if it would exceed)
  sync <lane>          the lane, draw-major, draws 1..5, eight workers; rows reviews/r141/rows/rows_<lane>.jsonl; halts at the cap
  spend                the metered spend (rows + leak + probes)
Every call first asserts the frozen registration's sha256 and the SB-60 texts' sha256.
"""
from __future__ import annotations

import concurrent.futures as cf
import datetime as dt
import hashlib
import io
import json
import os
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "r125" / "tools"))
import r125_run as R  # noqa: E402  (imports r125_common, cf2_run -> run_cf, cf2_openai; asserts the prompts_e1 digests)

C, RC, OAI = R.C, R.RC, R.OAI
REG = ROOT / "reviews" / "r141" / "registrations" / "ADDENDUM_R141_SB60.md"
REG_SHA = "4fc25a8b01c2606be4feaaf0092cc16daecf0f2e5087384fa0eda34953f1339b"
BUILD = ROOT / "reviews" / "r141" / "build" / "build_sb60.json"
TEXTS_SHA = "9346d52dbf677c127f78b6aabfa630282b771151146cfb61af84bd69f925fa74"
ROWS = ROOT / "reviews" / "r141" / "rows"
CAP = 12.00
ARM = "SB60"
LANES = {
    "SB60-LUNA": dict(vendor="openai", model="gpt-5.6-luna", kind="raw", k=5, max_completion_tokens=2048, arms=(ARM,)),
    "SB60-MINI": dict(vendor="openai", model="gpt-4.1-mini", kind="chat", k=5, temperature=None, max_tokens=200, arms=(ARM,)),
    "SB60-SOL": dict(vendor="openai", model="gpt-5.6-sol", kind="raw", k=5, max_completion_tokens=2048, arms=(ARM,)),
}
R.LANES.update(LANES)   # r125_run.call_openai reads its LANES table; extended in memory only
_B = {}


def setup():
    t = REG.read_bytes()
    assert hashlib.sha256(t[:t.index(b"<!-- REGISTERED TEXT ENDS")]).hexdigest() == REG_SHA, "REGISTRATION SHA MISMATCH -- STOP"
    assert RC.P.file_sha256() == RC.E1_FILE_SHA and RC.P.texts_sha256() == RC.E1_TEXTS_SHA
    RC.load_env()
    assert os.environ.get("OPENAI_API_KEY")
    ROWS.mkdir(parents=True, exist_ok=True)


def build():
    if not _B:
        b = json.load(open(BUILD, encoding="utf-8"))
        assert b["meta"]["texts_sha256"] == TEXTS_SHA
        assert hashlib.sha256("\x1f".join(b["texts"][k] for k in sorted(b["texts"])).encode("utf-8")).hexdigest() == TEXTS_SHA, "SB-60 TEXTS SHA MISMATCH -- STOP"
        _B.update(b)
    return _B


def units(arm=ARM):
    b = build()
    return [{"unit_id": f"{r['pair_id']}|SB60", "question": r["question"], "index": b["texts"][f"{r['pair_id']}|SB60"]} for r in b["rows"]]


def rows_path(lane):
    return ROWS / f"rows_{lane}.jsonl"


R.units = units            # r125_run.call_openai -> prompts_for(u) uses u["index"] and u["question"] only
R.rows_path = rows_path


def spent():
    usd = 0.0
    for p in ROWS.glob("rows_*.jsonl"):
        for l in io.open(p, encoding="utf-8"):
            if l.strip():
                usd += float(json.loads(l).get("usd") or 0.0)
    for name in ("leak_r141.json", "probes_r141.json"):
        p = ROWS / name
        if p.exists():
            d = json.load(open(p, encoding="utf-8"))
            usd += d.get("usd", 0.0) if name.startswith("leak") else sum(v.get("usd", 0.0) for v in d.values())
    return usd


def cmd_leak():
    setup()
    import random
    import cf2_leakscreen as LS
    from openai import OpenAI
    b = build()
    gold = {pid: pp["entry_text"] for pid, pp in C.Cell().pairs.items()}
    pool = sorted(b["rows"], key=lambda r: f"{r['pair_id']}|SB60")
    sample = sorted(random.Random(LS.SEED).sample(pool, LS.N), key=lambda r: r["pair_id"])
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def one(r):
        text_idx = b["texts"][f"{r['pair_id']}|SB60"]
        msgs = [{"role": "system", "content": LS.P.LEAKAGE_SYSTEM}, {"role": "user", "content": LS.P.LEAKAGE_USER.format(index=text_idx, question=r["question"])}]
        resp = client.chat.completions.create(model=LS.P.MODEL, temperature=LS.P.TEMPERATURE, seed=LS.P.SEED, max_tokens=LS.P.MAX_TOKENS, messages=msgs)
        text = resp.choices[0].message.content or ""
        obj = RC.last_json(text)
        ans = "" if obj is None else str(obj.get("answer", "")).strip()
        non_unknown = bool(ans) and ans.upper() != "UNKNOWN"
        g = gold[r["pair_id"]]
        return {"item_id": f"{r['pair_id']}|SB60", "pair_id": r["pair_id"], "question": r["question"], "gold_entry_text": g, "response": ans, "raw_response": text[:600],
                "parse_ok": obj is not None, "non_unknown": non_unknown, "correct": bool(non_unknown and LS.supports_correct(ans, g)), "served_model": resp.model,
                "tok_in": resp.usage.prompt_tokens, "tok_out": resp.usage.completion_tokens}

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        rows = sorted(ex.map(one, sample), key=lambda r: r["item_id"])
    n_correct = sum(r["correct"] for r in rows)
    leaked = n_correct > LS.THRESHOLD
    res = {"arm": ARM, "n": LS.N, "n_correct": n_correct, "threshold": LS.THRESHOLD, "leaked": leaked, "verdict": "LEAKS -- STOP" if leaked else "PASS",
           "n_non_unknown": sum(r["non_unknown"] for r in rows), "n_parse_failures": sum(not r["parse_ok"] for r in rows),
           "usd": round(sum(r["tok_in"] for r in rows) / 1e6 * LS.PRICE_IN + sum(r["tok_out"] for r in rows) / 1e6 * LS.PRICE_OUT, 6),
           "sample": [r["item_id"] for r in rows], "served_models": sorted({r["served_model"] for r in rows}), "when": dt.datetime.now().isoformat(timespec="seconds"),
           "rule": "cf2_leakscreen.py's rule, as R125 reproduced it, on the 88 SB-60 texts", "rows": rows}
    C.jdump(res, ROWS / "leak_r141.json")
    print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
    if leaked:
        raise SystemExit("STOP: the SB-60 texts leak")


def cmd_probe(lane):
    setup()
    leak = ROWS / "leak_r141.json"
    assert leak.exists() and json.load(open(leak, encoding="utf-8"))["verdict"] == "PASS", "the leak screen has not passed -- no lane"
    cfg = LANES[lane]
    row = R.call_openai(lane, units()[0], ARM, 0)
    ok = R.served_ok(cfg, row["served_model"])
    rec = {"lane": lane, "model": cfg["model"], "served": row["served_model"], "identifier_ok": ok, "tok_in": row["tok_in"], "tok_out": row["tok_out"], "usd": round(row["usd"], 6),
           "tok_reasoning": row.get("tok_reasoning", 0), "parsed": row["status"], "when": row["when"]}
    p = ROWS / "probes_r141.json"
    d = json.load(open(p, encoding="utf-8")) if p.exists() else {}
    d[lane] = rec
    C.jdump(d, p)
    print(json.dumps(rec, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- do not launch this lane")


def projection(lane, pr):
    cfg = LANES[lane]
    U = units()
    chars0 = len(U[0]["index"])
    ratio = pr["tok_in"] / max(1, chars0)
    tin = [int(len(u["index"]) * ratio) for u in U]
    tout = max(1, pr["tok_out"])
    p = R.PRICES[cfg["model"]]
    d1 = sum(t * p["inp"] * p["write_mult"] + tout * p["out"] for t in tin) / 1e6
    dk = sum(t * p["cached"] + tout * p["out"] for t in tin) / 1e6 * (cfg["k"] - 1)
    return d1 + dk


def cmd_project():
    setup()
    pr = json.load(open(ROWS / "probes_r141.json", encoding="utf-8"))
    rem = CAP - spent()
    out = {"cap": CAP, "spent_before": round(spent(), 4), "lanes": {}}
    for lane in ("SB60-LUNA", "SB60-MINI", "SB60-SOL"):
        if lane not in pr:
            continue
        pj = projection(lane, pr[lane])
        fits = pj <= rem
        out["lanes"][lane] = {"projection": round(pj, 4), "remaining_before": round(rem, 4), "fits": fits}
        if fits:
            rem -= pj
    C.jdump(out, ROWS / "projection_r141.json")
    print(json.dumps(out, indent=1))


def cmd_sync(lane):
    setup()
    cfg = LANES[lane]
    pr = json.load(open(ROWS / "probes_r141.json", encoding="utf-8"))[lane]
    assert pr["identifier_ok"]
    proj = json.load(open(ROWS / "projection_r141.json", encoding="utf-8"))
    assert proj["lanes"][lane]["fits"], f"{lane} is dropped by the registered cap rule"
    U = units()
    path = rows_path(lane)
    done = set()
    if path.exists():
        for l in io.open(path, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                done.add((r["unit_id"], int(r["draw"])))
    lock = threading.Lock()
    state = {"halted": False, "n": 0, "spent": spent()}
    print(f"{lane}: OpenAI metered so far ${state['spent']:.4f} of ${CAP:.2f}; {len(U)} units x 5 draws", flush=True)

    def work(job):
        u, d = job
        if state["halted"]:
            return None
        with lock:
            if state["spent"] >= CAP:
                state["halted"] = True
                return None
        row = None
        for attempt in (1, 2, 3):
            try:
                row = R.call_openai(lane, u, ARM, d)
                break
            except Exception as e:  # noqa: BLE001
                if attempt == 3:
                    row = {"unit_id": u["unit_id"], "arm": ARM, "model": cfg["model"], "draw": d, "lane": lane, "status": f"ERROR:{type(e).__name__}", "when": dt.datetime.now().isoformat(timespec="seconds")}
                else:
                    time.sleep(5 * attempt)
        if row.get("status") == "OK" and not R.served_ok(cfg, row["served_model"]):
            row["status"] = "IDENTIFIER_MISMATCH"
        with lock:
            state["spent"] += row.get("usd", 0.0)
            state["n"] += 1
            with io.open(path, "a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(row, sort_keys=True) + "\n")
            if state["n"] % 100 == 0:
                print(f"  {lane} draw {d}: {state['n']} calls, OpenAI ${state['spent']:.4f}", flush=True)
        return row

    for d in range(1, cfg["k"] + 1):
        jobs = [(u, d) for u in U if (u["unit_id"], d) not in done]
        if not jobs:
            print(f"{lane} draw {d}: complete already", flush=True)
            continue
        t0 = time.time()
        with cf.ThreadPoolExecutor(max_workers=R.WORKERS) as ex:
            list(ex.map(work, jobs))
        n_ok = sum(1 for l in io.open(path, encoding="utf-8") if l.strip() and json.loads(l).get("status") == "OK" and int(json.loads(l)["draw"]) == d)
        print(f"{lane} draw {d} done in {time.time() - t0:.0f}s: OK rows {n_ok}/{len(U)}; OpenAI ${state['spent']:.4f}", flush=True)
        if state["halted"]:
            print(f"{lane}: CAP REACHED at draw {d}; stopping", flush=True)
            break


def cmd_spend():
    print(f"OpenAI metered (rows + leak + probes): ${spent():.4f} of ${CAP:.2f}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    {"leak": cmd_leak, "project": cmd_project, "spend": cmd_spend}.get(cmd, lambda: None)()
    if cmd == "probe":
        cmd_probe(sys.argv[2])
    elif cmd == "sync":
        cmd_sync(sys.argv[2])
