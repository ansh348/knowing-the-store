# -*- coding: utf-8 -*-
"""r125_run.py -- the runner for Task 4 (the sibling-name control, ADDENDUM_R125_SIBLING) and Task 5 (E2 Amendment 1, ADDENDUM_R125_E2_AMENDMENT_1).
CALLS the APIs. Two hard caps enforced here, metered from the rows at the recorded page prices: Anthropic 10.00 USD, OpenAI 10.00 USD, checked
before every synchronous call and before every Batch submission (a Batch is submitted only if the lanes' metered spend plus the Batch's projection
at x1.3 stays under the cap). Both registrations' registered-text sha256 are asserted at every start against FREEZE_R125.md; the prompts are
run_cf's frozen prompts_e1 texts (digests asserted at import); the served identifier is asserted on every row (E1.7 rule).

Lanes (recorded settings copied from their analogues):
  Task 4, the 88 SIBLING items (reviews/r125/build/build_t4_sibling.json, texts sha256 asserted):
    SB-MINI5  gpt-4.1-mini            k = 5, temperature unset, max_tokens 200, synchronous, draw-major   (Table 1's row: R122 T3, D-R122-1)
    SB-H45    claude-haiku-4-5        k = 5, temperature 0, max_tokens 200, Message Batches                (E1 / CF-2)
    SB-LUNA   gpt-5.6-luna            k = 5, raw Chat Completions, reasoning / temperature unset, max_completion_tokens 2048, draw-major   (E5)
    SB-OP5    claude-opus-5           k = 1, temperature unset, max_tokens 1024, Message Batches            (E1's settings, one draw)
    SB-SOL    gpt-5.6-sol             k = 1, raw Chat Completions, E5's settings
  Task 5, the 888 (item, arm) units of INDEXED-NAMES and INDEXED-COUNTS (E2's renderer, sha256 asserted against cf2/build_nc.json):
    NC-OP5    claude-opus-5           k = 1, E1's settings, Message Batches
    NC-LUNA   gpt-5.6-luna            k = 5, E5's settings, draw-major over the 888 units
    NC-SOL    gpt-5.6-sol             k = 1, E5's settings -- run only if the OpenAI projection for Tasks 4 and 5 together fits the cap (the brief's rule)
Rows: r82_counterfactual/cf2/rows/rows_r125_<LANE>.jsonl; probes cf2/rows/probes_r125.json; locks cf2/rows/lock_r125.json; batches cf2/rows/batch_r125_<LANE>.json.
Subcommands: lock | leak | probe <lane> | project | sync <lane> [--draws 1,2] | submit <lane> | poll <lane> | spend
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

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r125_common as C  # noqa: E402
import cf2_run as C2  # noqa: E402  (re-points run_cf to the cf2 cell; asserts the prompts_e1 digests)
import cf2_openai as OAI  # noqa: E402  (E5's price function and MODELS)
import cf2_names_counts as NC  # noqa: E402  (E2's renderer)

RC = C2.RC
ROWS = C.CF2 / "rows"
LOCK, PROBES = ROWS / "lock_r125.json", ROWS / "probes_r125.json"
FREEZE = C.R125 / "FREEZE_R125.md"
REG_T4, REG_T5 = "ADDENDUM_R125_SIBLING.md", "ADDENDUM_R125_E2_AMENDMENT_1.md"
CAP = {"anthropic": 10.00, "openai": 10.00}
WORKERS = 8
PRICES = {  # USD per million: OpenAI's page prices as the recorded lanes priced them (E5 2026-09-18; R122 2026-09-19); Anthropic list, Batch at 0.5
    "gpt-4.1-mini": dict(inp=0.40, cached=0.10, out=1.60, write_mult=1.0),
    "gpt-5.6-luna": dict(inp=0.20, cached=0.02, out=1.20, write_mult=1.25),
    "gpt-5.6-sol": dict(inp=4.00, cached=0.40, out=20.00, write_mult=1.25),
}
OAI.MODELS.update({m: dict(code=m, **p) for m, p in PRICES.items() if m not in OAI.MODELS})   # E5's price() reads MODELS; extended in memory only
LANES = {
    "SB-MINI5": dict(task="T4", vendor="openai", model="gpt-4.1-mini", kind="chat", k=5, temperature=None, max_tokens=200, arms=("SIBLING",)),
    "SB-H45": dict(task="T4", vendor="anthropic", model="claude-haiku-4-5-20251001", kind="batch", k=5, temperature=0.0, max_tokens=200, arms=("SIBLING",), price=(1.00, 5.00), code="H45"),
    "SB-LUNA": dict(task="T4", vendor="openai", model="gpt-5.6-luna", kind="raw", k=5, max_completion_tokens=2048, arms=("SIBLING",)),
    "SB-OP5": dict(task="T4", vendor="anthropic", model="claude-opus-5", kind="batch", k=1, temperature=None, max_tokens=1024, arms=("SIBLING",), price=(5.00, 25.00), code="OP5"),
    "SB-SOL": dict(task="T4", vendor="openai", model="gpt-5.6-sol", kind="raw", k=1, max_completion_tokens=2048, arms=("SIBLING",)),
    "NC-OP5": dict(task="T5", vendor="anthropic", model="claude-opus-5", kind="batch", k=1, temperature=None, max_tokens=1024, arms=("INDEXED-NAMES", "INDEXED-COUNTS"), price=(5.00, 25.00), code="OP5"),
    "NC-LUNA": dict(task="T5", vendor="openai", model="gpt-5.6-luna", kind="raw", k=5, max_completion_tokens=2048, arms=("INDEXED-NAMES", "INDEXED-COUNTS")),
    "NC-SOL": dict(task="T5", vendor="openai", model="gpt-5.6-sol", kind="raw", k=1, max_completion_tokens=2048, arms=("INDEXED-NAMES", "INDEXED-COUNTS")),
}


# ------------------------------------------------------------------ freeze, units, prompts
def freeze_table():
    out = {}
    for ln in io.open(FREEZE, encoding="utf-8"):
        if ln.startswith("| ") and "`ADDENDUM_R125" in ln:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            out[cells[1].strip("`")] = cells[2].strip("`")
    return out


def assert_frozen(name):
    got = C.reg_sha(C.REGS / name); tab = freeze_table()
    assert name in tab and got == tab[name], f"REGISTRATION SHA MISMATCH for {name} -- STOP"
    return got


def setup():
    shas = {REG_T4: assert_frozen(REG_T4), REG_T5: assert_frozen(REG_T5)}
    assert RC.P.file_sha256() == RC.E1_FILE_SHA and RC.P.texts_sha256() == RC.E1_TEXTS_SHA
    RC.load_env()
    assert os.environ.get("OPENAI_API_KEY") and os.environ.get("ANTHROPIC_API_KEY")
    return shas


_SIB = {}


def sibling_build():
    if not _SIB:
        b = C.jload(C.BUILD / "build_t4_sibling.json")
        shas = [hashlib.sha256(b["texts"][r["item_id"]].encode("utf-8")).hexdigest() for r in b["rows"]]
        assert hashlib.sha256("".join(shas).encode()).hexdigest() == b["meta"]["texts_sha256"], "SIBLING TEXTS SHA MISMATCH -- STOP"
        _SIB.update(b)
    return _SIB


def units(arm):
    if arm == "SIBLING":
        b = sibling_build()
        return [{"unit_id": r["item_id"], "question": r["question"], "index": b["texts"][r["item_id"]]} for r in b["rows"]]
    rec = C.jload(C.CF2 / "build_nc.json")["arms"][arm]["texts_sha256"]
    U = [{"unit_id": it["item_id"], "question": it["question"], "index": NC.RENDER[arm](RC.IDX[it["item_id"]]["v2"])} for it in RC.CELL]
    got = hashlib.sha256("".join(hashlib.sha256(u["index"].encode("utf-8")).hexdigest() for u in U).encode()).hexdigest()
    assert got == rec, f"{arm} TEXTS SHA MISMATCH against build_nc.json -- STOP"
    return U


def prompts_for(u):
    return RC.P.SYSTEM, RC.P.USER_INDEXED.format(index=u["index"], question=u["question"])


def rows_path(lane):
    return ROWS / f"rows_r125_{lane}.jsonl"


# ------------------------------------------------------------------ spend
def spent_vendor(vendor):
    usd = 0.0
    for lane, cfg in LANES.items():
        if cfg["vendor"] != vendor:
            continue
        p = rows_path(lane)
        if p.exists():
            usd += sum(json.loads(l).get("usd", 0.0) for l in io.open(p, encoding="utf-8") if l.strip())
        bp = ROWS / f"batch_r125_{lane}.json"
        if bp.exists() and not p.exists():
            usd += json.loads(bp.read_text(encoding="utf-8")).get("projection_usd", 0.0)     # a submitted, uncollected Batch counts at its projection
    if PROBES.exists():
        for k, v in C.jload(PROBES).items():
            if LANES[k]["vendor"] == vendor:
                usd += v.get("usd", 0.0)
    if vendor == "openai" and (ROWS / "leak_r125.json").exists():
        usd += C.jload(ROWS / "leak_r125.json").get("usd", 0.0)
    return usd


def cmd_spend():
    for v in CAP:
        print(f"{v}: metered ${spent_vendor(v):.4f} of the ${CAP[v]:.2f} cap")


# ------------------------------------------------------------------ calls
def call_openai(lane, u, arm, draw):
    from openai import OpenAI
    cfg = LANES[lane]; sysm, user = prompts_for(u)
    cl = OpenAI(max_retries=2, timeout=120)
    kw = dict(model=cfg["model"], messages=[{"role": "system", "content": sysm}, {"role": "user", "content": user}])
    if cfg["kind"] == "chat":
        kw["max_tokens"] = cfg["max_tokens"]
        if cfg.get("temperature") is not None:
            kw["temperature"] = cfg["temperature"]
    else:
        kw["max_completion_tokens"] = cfg["max_completion_tokens"]
    r = cl.chat.completions.create(**kw)
    raw = r.model_dump(mode="json"); usage = raw.get("usage") or {}
    usd, cached, write, reasoning = OAI.price(cfg["model"], usage)
    row = RC.make_row(u, arm, cfg["model"], draw, r.choices[0].message.content, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0), (PRICES[cfg["model"]]["inp"], PRICES[cfg["model"]]["out"]), 1.0, r.model)
    row.update({"lane": lane, "usd": usd, "tok_cached": cached, "tok_cache_write": write, "tok_reasoning": reasoning, "finish_reason": r.choices[0].finish_reason, "usage": usage,
                "temperature": cfg.get("temperature"), "when": dt.datetime.now().isoformat(timespec="seconds")})
    return row


def call_anthropic_once(lane, u, arm, draw):
    cfg = LANES[lane]; sysm, user = prompts_for(u)
    kw = dict(model=cfg["model"], max_tokens=cfg["max_tokens"], system=sysm, messages=[{"role": "user", "content": user}])
    if cfg.get("temperature") is not None:
        kw["temperature"] = cfg["temperature"]
    r = RC.anthropic_client().messages.create(**kw)
    text = "".join(b.text for b in r.content if b.type == "text")
    row = RC.make_row(u, arm, cfg["model"], draw, text, r.usage.input_tokens, r.usage.output_tokens, cfg["price"], 1.0, r.model)
    row.update({"lane": lane, "when": dt.datetime.now().isoformat(timespec="seconds")})
    return row


def served_ok(cfg, served):
    return cfg["model"].split("-2025")[0] in served or cfg["model"] in served


# ------------------------------------------------------------------ subcommands
def cmd_lock():
    shas = setup()
    rec = {"registrations": shas, "freeze_file": str(FREEZE.relative_to(C.ROOT)), "prompts_file_sha256": RC.P.file_sha256(), "prompts_texts_sha256": RC.P.texts_sha256(),
           "sibling_texts_sha256": sibling_build()["meta"]["texts_sha256"], "n_sibling": len(sibling_build()["rows"]),
           "nc_texts_sha256": {a: C.jload(C.CF2 / "build_nc.json")["arms"][a]["texts_sha256"] for a in ("INDEXED-NAMES", "INDEXED-COUNTS")},
           "caps": CAP, "prices": PRICES, "anthropic_prices": {"claude-haiku-4-5-20251001": [1.00, 5.00], "claude-opus-5": [5.00, 25.00], "batch_mult": 0.5},
           "lanes": {k: {kk: vv for kk, vv in v.items()} for k, v in LANES.items()}, "runner_sha256": C.sha_file(__file__), "when": dt.datetime.now().isoformat(timespec="seconds")}
    for a in ("INDEXED-NAMES", "INDEXED-COUNTS"):
        units(a)
    ROWS.mkdir(parents=True, exist_ok=True)
    C.jdump(rec, LOCK)
    print(json.dumps({k: v for k, v in rec.items() if k != "lanes"}, indent=1))


def cmd_leak():
    """The CF-2 leakage screen (cf2_leakscreen.py's rule, reproduced) on the SIBLING texts: the 88 SIBLING items sorted by item_id, random.Random(42).sample(pool, 30);
    gpt-4.1-mini at temperature 0, seed 42, max_tokens 200 with prompts_e1.LEAKAGE_SYSTEM / LEAKAGE_USER; gold = the pair's entry_text; exp4_witnesses.supports_correct;
    the cell LEAKS iff more than 3 of 30 score correct (a STOP)."""
    setup(); assert LOCK.exists()
    import random
    import cf2_leakscreen as LS
    from openai import OpenAI
    b = sibling_build(); gold = {pid: pp["entry_text"] for pid, pp in C.Cell().pairs.items()}
    pool = sorted(b["rows"], key=lambda r: r["item_id"]); sample = sorted(random.Random(LS.SEED).sample(pool, LS.N), key=lambda r: r["item_id"])
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def one(r):
        text_idx = b["texts"][r["item_id"]]
        msgs = [{"role": "system", "content": LS.P.LEAKAGE_SYSTEM}, {"role": "user", "content": LS.P.LEAKAGE_USER.format(index=text_idx, question=r["question"])}]
        resp = client.chat.completions.create(model=LS.P.MODEL, temperature=LS.P.TEMPERATURE, seed=LS.P.SEED, max_tokens=LS.P.MAX_TOKENS, messages=msgs)
        text = resp.choices[0].message.content or ""; obj = RC.last_json(text); ans = "" if obj is None else str(obj.get("answer", "")).strip()
        non_unknown = bool(ans) and ans.upper() != "UNKNOWN"; g = gold[r["pair_id"]]
        return {"item_id": r["item_id"], "pair_id": r["pair_id"], "persona": r["persona"], "question": r["question"], "gold_entry_text": g, "response": ans, "raw_response": text[:600],
                "parse_ok": obj is not None, "non_unknown": non_unknown, "correct": bool(non_unknown and LS.supports_correct(ans, g)), "served_model": resp.model,
                "tok_in": resp.usage.prompt_tokens, "tok_out": resp.usage.completion_tokens}

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        rows = sorted(ex.map(one, sample), key=lambda r: r["item_id"])
    n_correct = sum(r["correct"] for r in rows); leaked = n_correct > LS.THRESHOLD
    res = {"arm": "SIBLING", "n": LS.N, "n_correct": n_correct, "threshold": LS.THRESHOLD, "leaked": leaked, "verdict": "LEAKS -- STOP" if leaked else "PASS",
           "n_non_unknown": sum(r["non_unknown"] for r in rows), "n_parse_failures": sum(not r["parse_ok"] for r in rows),
           "usd": round(sum(r["tok_in"] for r in rows) / 1e6 * LS.PRICE_IN + sum(r["tok_out"] for r in rows) / 1e6 * LS.PRICE_OUT, 6),
           "sample": [r["item_id"] for r in sample], "served_models": sorted({r["served_model"] for r in rows}), "when": dt.datetime.now().isoformat(timespec="seconds"),
           "rule": "cf2_leakscreen.py's, reproduced on the SIBLING texts (the 88 items, all PRESENT-labelled, are the pool)", "rows": rows}
    C.jdump(res, ROWS / "leak_r125.json"); print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
    if leaked:
        raise SystemExit("STOP: the SIBLING texts leak")


def cmd_probe(lane):
    setup(); assert LOCK.exists()
    cfg = LANES[lane]; u = units(cfg["arms"][0])[0]
    row = call_openai(lane, u, cfg["arms"][0], 0) if cfg["vendor"] == "openai" else call_anthropic_once(lane, u, cfg["arms"][0], 0)
    ok = served_ok(cfg, row["served_model"])
    rec = {"lane": lane, "model": cfg["model"], "served": row["served_model"], "identifier_ok": ok, "tok_in": row["tok_in"], "tok_out": row["tok_out"], "usd": round(row["usd"], 6),
           "tok_cached": row.get("tok_cached", 0), "tok_cache_write": row.get("tok_cache_write", 0), "tok_reasoning": row.get("tok_reasoning", 0), "parsed": row["status"], "sample": row["text"][:200], "when": row["when"]}
    d = C.jload(PROBES) if PROBES.exists() else {}
    d[lane] = rec; C.jdump(d, PROBES)
    print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")


def projection(lane, pr):
    """USD for the lane from its probe: input tokens scaled by each unit's characters against the probe's; OpenAI draws 2..k at the cached rate (E5's cost rule);
    Anthropic Batch at 0.5."""
    cfg = LANES[lane]; U = [u for a in cfg["arms"] for u in units(a)]
    chars0 = len(units(cfg["arms"][0])[0]["index"]); ratio = pr["tok_in"] / max(1, chars0)
    tin = [int(len(u["index"]) * ratio) for u in U]; tout = max(1, pr["tok_out"])
    if cfg["vendor"] == "openai":
        p = PRICES[cfg["model"]]
        d1 = sum(t * p["inp"] * p["write_mult"] + tout * p["out"] for t in tin) / 1e6
        dk = sum(t * p["cached"] + tout * p["out"] for t in tin) / 1e6 * (cfg["k"] - 1)
        return d1 + dk, len(U) * cfg["k"]
    p = cfg["price"]
    return sum(t * p[0] + tout * p[1] for t in tin) / 1e6 * cfg["k"] * 0.5, len(U) * cfg["k"]


def cmd_project():
    setup(); pr = C.jload(PROBES)
    tot = {"anthropic": 0.0, "openai": 0.0}
    print(f"{'lane':10s} {'calls':>6s} {'usd':>8s} {'x1.3':>8s}")
    out = {}
    for lane in LANES:
        if lane not in pr:
            print(f"{lane:10s} (no probe)"); continue
        usd, n = projection(lane, pr[lane]); tot[LANES[lane]["vendor"]] += usd
        out[lane] = {"calls": n, "usd": round(usd, 4), "x1.3": round(usd * 1.3, 4)}
        print(f"{lane:10s} {n:6d} {usd:8.3f} {usd * 1.3:8.3f}")
    for v in tot:
        sp = spent_vendor(v)
        print(f"{v}: projected ${tot[v]:.3f} (x1.3 ${tot[v] * 1.3:.3f}) + metered so far ${sp:.4f} against the ${CAP[v]:.2f} cap" + ("" if tot[v] + sp <= CAP[v] else "  -- EXCEEDS THE CAP"))
    out["totals"] = {v: {"projected": round(tot[v], 4), "spent": round(spent_vendor(v), 4), "cap": CAP[v], "fits": bool(tot[v] + spent_vendor(v) <= CAP[v])} for v in tot}
    oai_no_sol = sum(out[l]["usd"] for l in out if l in LANES and LANES[l]["vendor"] == "openai" and l != "NC-SOL")
    out["openai_without_NC-SOL"] = {"projected": round(oai_no_sol, 4), "fits": bool(oai_no_sol + spent_vendor("openai") <= CAP["openai"])}
    C.jdump(out, ROWS / "projection_r125.json")
    print(f"OpenAI without NC-SOL: ${oai_no_sol:.3f}")


def cmd_sync(lane, draws):
    setup(); cfg = LANES[lane]; assert cfg["vendor"] == "openai"
    pr = C.jload(PROBES)[lane]; assert pr["identifier_ok"]
    if lane == "NC-SOL":
        proj = C.jload(ROWS / "projection_r125.json"); assert proj["totals"]["openai"]["fits"], "NC-SOL is dropped by the registered rule: the OpenAI projection for Tasks 4 and 5 exceeds the cap"
    U = [(a, u) for a in cfg["arms"] for u in units(a)]
    path = rows_path(lane); done = set()
    if path.exists():
        for l in io.open(path, encoding="utf-8"):
            if l.strip():
                r = json.loads(l); done.add((r["unit_id"], r["arm"], int(r["draw"])))
    lock = threading.Lock(); state = {"halted": False, "n": 0, "spent": spent_vendor("openai")}
    print(f"{lane}: OpenAI metered so far ${state['spent']:.4f} of ${CAP['openai']:.2f}; {len(U)} units x draws {draws}", flush=True)

    def work(job):
        a, u, d = job
        if state["halted"]:
            return None
        with lock:
            if state["spent"] >= CAP["openai"]:
                state["halted"] = True; return None
        row = None
        for attempt in (1, 2, 3):
            try:
                row = call_openai(lane, u, a, d); break
            except Exception as e:  # noqa: BLE001
                if attempt == 3:
                    row = {"unit_id": u["unit_id"], "arm": a, "model": cfg["model"], "draw": d, "lane": lane, "status": f"ERROR:{type(e).__name__}", "when": dt.datetime.now().isoformat(timespec="seconds")}
                else:
                    time.sleep(5 * attempt)
        if row.get("status") == "OK" and not served_ok(cfg, row["served_model"]):
            row["status"] = "IDENTIFIER_MISMATCH"
        with lock:
            state["spent"] += row.get("usd", 0.0); state["n"] += 1
            with io.open(path, "a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(row, sort_keys=True) + "\n")
            if state["n"] % 100 == 0:
                print(f"  {lane} draw {d}: {state['n']} calls, OpenAI ${state['spent']:.4f}", flush=True)
        return row

    for d in draws:
        jobs = [(a, u, d) for a, u in U if (u["unit_id"], a, d) not in done]
        if not jobs:
            print(f"{lane} draw {d}: complete already", flush=True); continue
        t0 = time.time()
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
            list(ex.map(work, jobs))
        n_ok = sum(1 for l in io.open(path, encoding="utf-8") if l.strip() and json.loads(l).get("status") == "OK" and int(json.loads(l)["draw"]) == d)
        print(f"{lane} draw {d} done in {time.time() - t0:.0f}s: OK rows {n_ok}/{len(U)}; OpenAI ${state['spent']:.4f}", flush=True)
        if state["halted"]:
            print(f"{lane}: CAP REACHED at draw {d}; stopping (whole draws scored, partial draws discarded)", flush=True); break


def cmd_submit(lane):
    setup(); cfg = LANES[lane]; assert cfg["vendor"] == "anthropic"
    pr = C.jload(PROBES)[lane]; assert pr["identifier_ok"]
    usd, n = projection(lane, pr); sp = spent_vendor("anthropic")
    assert sp + usd * 1.3 <= CAP["anthropic"], f"Anthropic: metered ${sp:.4f} + projection x1.3 ${usd * 1.3:.4f} exceeds the ${CAP['anthropic']:.2f} cap -- not submitted"
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    reqs = []
    for ai, a in enumerate(cfg["arms"]):
        for i, u in enumerate(units(a)):
            sysm, user = prompts_for(u)
            for d in range(1, cfg["k"] + 1):
                kw = dict(model=cfg["model"], max_tokens=cfg["max_tokens"], system=sysm, messages=[{"role": "user", "content": user}])
                if cfg.get("temperature") is not None:
                    kw["temperature"] = cfg["temperature"]
                reqs.append(Request(custom_id=f"{lane}-{ai}-{i:04d}-d{d}", params=MessageCreateParamsNonStreaming(**kw)))
    b = RC.anthropic_client().messages.batches.create(requests=reqs)
    (ROWS / f"batch_r125_{lane}.json").write_text(json.dumps({"id": b.id, "lane": lane, "n": len(reqs), "projection_usd": round(usd, 4), "when": dt.datetime.now().isoformat(timespec="seconds")}), encoding="utf-8")
    print("submitted", b.id, len(reqs), "requests; projection", round(usd, 4))


def cmd_poll(lane):
    setup(); cfg = LANES[lane]
    meta = json.loads((ROWS / f"batch_r125_{lane}.json").read_text(encoding="utf-8"))
    cl = RC.anthropic_client(); b = cl.messages.batches.retrieve(meta["id"])
    print(meta["id"], b.processing_status, b.request_counts)
    if b.processing_status != "ended":
        return
    by = {ai: units(a) for ai, a in enumerate(cfg["arms"])}
    n_ok = 0
    with io.open(rows_path(lane), "w", encoding="utf-8", newline="\n") as f:
        for res in cl.messages.batches.results(meta["id"]):
            _lane, ai, i, d = res.custom_id.rsplit("-", 3)
            a = cfg["arms"][int(ai)]; u = by[int(ai)][int(i)]
            if res.result.type == "succeeded":
                m = res.result.message
                text = "".join(bl.text for bl in m.content if bl.type == "text")
                row = RC.make_row(u, a, cfg["model"], int(d[1:]), text, m.usage.input_tokens, m.usage.output_tokens, cfg["price"], 0.5, m.model)
                row.update({"lane": lane, "batch_id": meta["id"]})
                if not served_ok(cfg, m.model):
                    row["status"] = "IDENTIFIER_MISMATCH"
                n_ok += row["status"] == "OK"
            else:
                row = {"unit_id": u["unit_id"], "arm": a, "model": cfg["model"], "draw": int(d[1:]), "lane": lane, "status": "BATCH_" + res.result.type.upper()}
            f.write(json.dumps(row, sort_keys=True) + "\n")
    print("collected; ok:", n_ok, "of", meta["n"])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "lock":
        cmd_lock()
    elif cmd == "leak":
        cmd_leak()
    elif cmd == "probe":
        cmd_probe(sys.argv[2])
    elif cmd == "project":
        cmd_project()
    elif cmd == "sync":
        draws = [int(x) for x in sys.argv[sys.argv.index("--draws") + 1].split(",")] if "--draws" in sys.argv else list(range(1, LANES[sys.argv[2]]["k"] + 1))
        cmd_sync(sys.argv[2], draws)
    elif cmd == "submit":
        cmd_submit(sys.argv[2])
    elif cmd == "poll":
        cmd_poll(sys.argv[2])
    elif cmd == "spend":
        cmd_spend()
