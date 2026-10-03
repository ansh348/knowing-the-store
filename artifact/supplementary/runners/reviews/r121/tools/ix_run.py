# -*- coding: utf-8 -*-
"""ix_run.py -- ADDENDUM_CF2_INTENT_CROSSOVER (program R121): the runner. Registration registrations/ADDENDUM_CF2_INTENT_CROSSOVER.md,
registered-text sha256 9480d6bb..., frozen at 648d671. Asserts at start: the registration's sha256, the P0 digests (run_cf's import),
the P1 system-text sha256 (prompts_p1), the cue list's sha256 (cue_list v2), the questions' sha256 at both lineages, the verdicts file
against the returned workbook's sha256. Writes cf2/rows/lock_ix.json at `lock`.

Units (the 113 pairs the author's check left in scope; verdicts_r121.json): per pair the recorded question (cells 1, 2) and the passing
crossed question (cells 3, 4), each of the PN version (cells 1, 3) and the PRESENT version (cells 2, 4), under the population's summary
(A: v2; B: v3). New calls: P0 cells 3 and 4 for every lane, plus P0 cells 1 and 2 on population B for Luna (no recorded V3 rows);
P1 cells 1 to 4 for every lane. The recorded P0 cells 1 and 2 (rows_MINI/H45/OP5 INDEXED-V2 / -V3; rows_LUNA INDEXED-V2) are read
at scoring and never re-run. unit_id = "<pair_id>|c<cell>|<P0|P1>"; resume key (unit_id, draw).

Lanes (registration section 5): MINI gpt-4.1-mini k=1 temperature 0 max_tokens 200, synchronous, 8 workers; LUNA gpt-5.6-luna k=5,
raw Chat Completions, effort and temperature unset, max_completion_tokens 2048, draw-major, 8 workers, the E5 cache pricing;
H45 claude-haiku-4-5-20251001 k=5 temperature 0 max_tokens 200, one Message Batch; OP5 claude-opus-5 k=1 temperature unset
max_tokens 1024, one Message Batch (design O2). Caps: Anthropic 15 USD, OpenAI 4 USD (Phase 1's 0.2044 counted), metered from the rows.

Subcommands:  lock | probe <lane> | project | run <lane> (MINI, LUNA, SOL) | submit <lane> | poll <lane> (H45, OP5) | lock_amend1

Amendment 1 (2026-09-19; approved, cap 12 USD; text sha256 2a21bcce...): GPT-5.6 Sol as a fifth reader, one draw on every cell it needs
(P0 cells 3-4, P1 cells 1-4, and P0 cells 1-2 on population B; 730 calls), raw API with E5's settings, its own 12 USD cap; cells 1-2
under P0 on population A from its recorded E5 rows at draw 1. Added after the interim read of three lanes (disclosed in the amendment).
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
for p in ("r82_counterfactual/tools", "reviews/r121/tools", "e1_metamemory/tools"):
    sys.path.insert(0, str(ROOT / p))
import run_cf as RC  # noqa: E402  (asserts the prompts_e1 digests at import)
import prompts_p1 as P1  # noqa: E402  (asserts P1's construction at import)
import cue_list as CUES  # noqa: E402  (asserts the v1 list reproduces)
import cross_questions as X  # noqa: E402
import cf2_openai as OAI  # noqa: E402  (E5's price function and Luna's page prices)

CF2 = ROOT / "r82_counterfactual" / "cf2"
ROWS = CF2 / "rows"
BUILD = ROOT / "reviews" / "r121" / "build"
REG = ROOT / "registrations" / "ADDENDUM_CF2_INTENT_CROSSOVER.md"
REG_SHA = "9480d6bbcfef47d25c2711d0c42f9c05d7dc2239fdddb371205a07923675711a"
FROZEN_AT = "648d671"
P1_SHA = "c3c9a8e2b9798b50aa5a8f091f382b550e296f973f0c9af09d7fa38442cc7ce4"
CUES_SHA = "a63461d09d5c60c44009c05b004657394a854ab10d468f80bf9377625f8fb9a8"
Q_SHA = {"primary": "efa8eeee63db25674d68a1e1067cdc5d3e9ea837d2ce2c8f68d063ba5dee195e", "lineage2": "c488db0c316d8bd7f5f8deeb1f459cf3ef65fd6aa4c8ad7357cdadaf6bf1128b"}
RETURNED_SHA = "be79963e0a328761aec0ca0d0300de78efc8ef1d114254a0540fcbf1ae585c49"
AMEND1_SHA = "2a21bcce8257c551450896bcb17668cefbfd5573f89bc318256bc8f80057c1e6"
AMEND1_HEAD = "## Amendment 1 (2026-09-19)"
LANE_CAP = {"SOL": 12.00}                      # Amendment 1: the Sol lane's own cap, separate from the design's OpenAI cap
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
CAP = {"anthropic": 15.00, "openai": 4.00}
PHASE1_OPENAI = 0.2044
WORKERS = 8
SUMMARY = {"A": "v2", "B": "v3"}
LANES = {
    "MINI": dict(vendor="openai", model="gpt-4.1-mini", temp=0.0, max_tokens=200, price=(0.40, 1.60), mult=1.0, k=1, transport="sync"),
    "LUNA": dict(vendor="openai", model="gpt-5.6-luna", temp=None, max_tokens=2048, price=(0.20, 1.20), mult=1.0, k=5, transport="raw"),
    "H45": dict(vendor="anthropic", model="claude-haiku-4-5-20251001", temp=0.0, max_tokens=200, price=(1.00, 5.00), mult=0.5, k=5, transport="batch"),
    "OP5": dict(vendor="anthropic", model="claude-opus-5", temp=None, max_tokens=1024, price=(5.00, 25.00), mult=0.5, k=1, transport="batch"),
    "SOL": dict(vendor="openai", model="gpt-5.6-sol", temp=None, max_tokens=2048, price=(4.00, 20.00), mult=1.0, k=1, transport="raw"),   # Amendment 1
}
LOCK = ROWS / "lock_ix.json"
PROBES = ROWS / "probes_ix.json"


def reg_sha():
    b = REG.read_bytes(); i = b.find(FROZEN_END); assert i > 0
    return hashlib.sha256(b[:i]).hexdigest()


def amend1_sha():
    t = REG.read_text(encoding="utf-8"); i = t.find(AMEND1_HEAD); assert i > 0, "Amendment 1 not appended"
    return hashlib.sha256(t[i:].encode("utf-8")).hexdigest()


def setup():
    assert reg_sha() == REG_SHA, "REGISTRATION SHA MISMATCH -- STOP"
    assert P1.p1_sha256() == P1_SHA, "P1 SHA MISMATCH -- STOP"
    assert CUES.cue_sha256() == CUES_SHA, "CUE LIST SHA MISMATCH -- STOP"
    q = json.load(io.open(BUILD / "cross_questions.json", encoding="utf-8"))
    assert q["meta"]["primary"]["questions_sha256"] == Q_SHA["primary"] and q["meta"]["lineage2"]["questions_sha256"] == Q_SHA["lineage2"], "QUESTIONS SHA MISMATCH -- STOP"
    assert hashlib.sha256((BUILD / "AUTHOR_CHECK_R121_returned.xlsx").read_bytes()).hexdigest() == RETURNED_SHA, "RETURNED WORKBOOK SHA MISMATCH -- STOP"
    v = json.load(io.open(BUILD / "verdicts_r121.json", encoding="utf-8"))
    assert v["returned_sha256"] == RETURNED_SHA and v["counts_match_expected"]
    RC.load_env()
    return q, v


_UNITS = None


def units_all():
    """Every unit of the design in a fixed order: arm, pair, version, cell (so cells sharing a prompt prefix are adjacent)."""
    global _UNITS
    if _UNITS is not None:
        return _UNITS
    q, v = setup()
    qs = {r["pair_id"]: r for r in q["questions"]}
    cell = {it["item_id"]: it for it in json.load(io.open(CF2 / "cf_cell.json", encoding="utf-8"))["items"]}
    idx = json.load(io.open(CF2 / "cf_indexes.json", encoding="utf-8"))["indexes"]
    pairs = sorted(pid for pid, rec in v["pairs"].items() if rec["status"] != "DROP")
    assert len(pairs) == 113
    out = []
    for arm in ("P0", "P1"):
        for pid in pairs:
            rec = v["pairs"][pid]; pop = rec["population"]; key = SUMMARY[pop]
            orig = cell[pid + "|PN"]["question"]; crossed = rec["question"]
            assert cell[pid + "|PRESENT"]["question"] == orig
            for version, cells in (("PN", (1, 3)), ("PRESENT", (2, 4))):
                for c in cells:
                    question = orig if c in (1, 2) else crossed
                    label = "PN" if c == 1 else "PRESENT"
                    out.append({"unit_id": f"{pid}|c{c}|{arm}", "pair_id": pid, "cell": c, "arm": arm, "version": version, "population": pop, "summary": key,
                                "persona": cell[pid + "|PN"]["persona"], "label": label, "y": 1 if c == 1 else 0, "question": question,
                                "index": idx[f"{pid}|{version}"][key], "lineage": rec["lineage"] if c in (3, 4) else "recorded"})
    _UNITS = out
    return out


def units_for(lane):
    """The new calls of a lane: P0 cells 3-4 (and cells 1-2 on B for LUNA), P1 cells 1-4."""
    out = []
    for u in units_all():
        if u["arm"] == "P1" or u["cell"] in (3, 4) or (lane in ("LUNA", "SOL") and u["population"] == "B"):
            out.append(u)
    return out


def prompts_for(u):
    sysm = RC.P.SYSTEM if u["arm"] == "P0" else P1.SYSTEM_P1
    return sysm, RC.P.USER_INDEXED.format(index=u["index"], question=u["question"])


def rows_path(lane):
    return ROWS / f"rows_IX_{lane}.jsonl"


def base_row(u, lane, draw):
    return {k: u[k] for k in ("unit_id", "pair_id", "cell", "arm", "version", "population", "summary", "persona", "label", "y", "question", "lineage")} | {"model": LANES[lane]["model"], "lane": lane, "draw": draw}


def call_openai(lane, u, draw):
    from openai import OpenAI
    cfg = LANES[lane]; sysm, user = prompts_for(u)
    cl = OpenAI(max_retries=2, timeout=120)
    if cfg["transport"] == "sync":
        r = cl.chat.completions.create(model=cfg["model"], temperature=cfg["temp"], max_tokens=cfg["max_tokens"],
                                       messages=[{"role": "system", "content": sysm}, {"role": "user", "content": user}])
        row = RC.make_row(u, u["arm"], cfg["model"], draw, r.choices[0].message.content, r.usage.prompt_tokens, r.usage.completion_tokens, cfg["price"], 1.0, r.model)
        row.update(base_row(u, lane, draw)); row["when"] = dt.datetime.now().isoformat(timespec="seconds")
        return row
    r = cl.chat.completions.create(model=cfg["model"], max_completion_tokens=cfg["max_tokens"],
                                   messages=[{"role": "system", "content": sysm}, {"role": "user", "content": user}])
    usage = (r.model_dump(mode="json").get("usage") or {})
    usd, cached, write, reasoning = OAI.price(cfg["model"], usage)
    row = RC.make_row(u, u["arm"], cfg["model"], draw, r.choices[0].message.content, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0), cfg["price"], 1.0, r.model)
    row.update(base_row(u, lane, draw))
    row.update({"usd": usd, "tok_cached": cached, "tok_cache_write": write, "tok_reasoning": reasoning, "finish_reason": r.choices[0].finish_reason, "usage": usage,
                "when": dt.datetime.now().isoformat(timespec="seconds")})
    return row


def call_anthropic_sync(lane, u, draw):
    cfg = LANES[lane]; sysm, user = prompts_for(u)
    kw = dict(model=cfg["model"], max_tokens=cfg["max_tokens"], system=sysm, messages=[{"role": "user", "content": user}])
    if cfg["temp"] is not None:
        kw["temperature"] = cfg["temp"]
    r = RC.anthropic_client().messages.create(**kw)
    text = "".join(b.text for b in r.content if b.type == "text")
    row = RC.make_row(u, u["arm"], cfg["model"], draw, text, r.usage.input_tokens, r.usage.output_tokens, cfg["price"], 1.0, r.model)   # list price (a probe)
    row.update(base_row(u, lane, draw)); row["when"] = dt.datetime.now().isoformat(timespec="seconds")
    return row


def spent(lane):
    p = rows_path(lane)
    if not p.exists():
        return 0.0
    return sum(json.loads(l).get("usd", 0.0) for l in io.open(p, encoding="utf-8") if l.strip())


def spent_vendor(vendor):
    tot = sum(spent(l) for l, c in LANES.items() if c["vendor"] == vendor and l not in LANE_CAP)
    if PROBES.exists():
        for lane, rec in json.load(io.open(PROBES, encoding="utf-8")).items():
            if LANES[lane]["vendor"] == vendor and lane not in LANE_CAP:
                tot += rec["usd"]
    if vendor == "openai":
        tot += PHASE1_OPENAI
    return tot


# ------------------------------------------------------------------------------------------------ lock / probe / project
def cmd_lock():
    q, v = setup()
    U = units_all()
    rec = {"registration": str(REG.relative_to(ROOT)).replace("\\", "/"), "registration_sha256": REG_SHA, "frozen_at": FROZEN_AT,
           "prompts_file_sha256": RC.P.file_sha256(), "prompts_texts_sha256": RC.P.texts_sha256(), "p0_system_sha256": P1.p0_sha256(), "p1_system_sha256": P1_SHA,
           "cue_list_sha256": CUES_SHA, "questions_sha256": Q_SHA, "instruction_prompt_sha256": q["meta"]["primary"]["prompt_sha256"], "lineage2_sha256": q["meta"]["lineage2"]["lineage_sha256"],
           "workbook_returned_sha256": RETURNED_SHA, "counts": v["counts"], "pairs_in_scope": 113, "units_total": len(U),
           "units_per_lane": {l: len(units_for(l)) for l in LANES}, "lanes": {l: {k: v_ for k, v_ in c.items()} for l, c in LANES.items()},
           "caps_usd": CAP, "phase1_openai_usd": PHASE1_OPENAI, "order": "MINI sync -> LUNA draw-major (8 workers) -> H45 Batch -> OP5 Batch -> score",
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    ROWS.mkdir(parents=True, exist_ok=True)
    io.open(LOCK, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: rec[k] for k in ("registration_sha256", "frozen_at", "p1_system_sha256", "cue_list_sha256", "units_total", "units_per_lane", "counts")}, indent=1))


def cmd_lock_amend1():
    """Amendment 1: the Sol lane's lock (the amendment sha, the freeze commit, the cap, the units)."""
    q, v = setup(); assert amend1_sha() == AMEND1_SHA, "AMENDMENT 1 SHA MISMATCH -- STOP"
    rec = {"amendment": "Amendment 1 (GPT-5.6 Sol)", "amendment_sha256": AMEND1_SHA, "registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "amendment_frozen_at": sys.argv[2] if len(sys.argv) > 2 else None,
           "lane": "SOL", "settings": LANES["SOL"], "cap_usd": LANE_CAP["SOL"], "units": len(units_for("SOL")), "recorded_cells12_A": "rows_SOL.jsonl INDEXED-V2 draw 1 (sensitivity: the five-draw mean)",
           "disclosure": "added after the interim read of three lanes (cf_scores_ix_interim_3lanes.json) while the Opus 5 batch was running and unread; P-I2b labelled as made after that read",
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    io.open(ROWS / "lock_ix_amend1.json", "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    print(json.dumps(rec, indent=1))


def cmd_probe(lane):
    setup(); assert LOCK.exists(), "lock first"
    if lane in LANE_CAP:
        assert amend1_sha() == AMEND1_SHA, "AMENDMENT 1 SHA MISMATCH -- STOP"
    cfg = LANES[lane]; U = units_for(lane)
    u0 = next(u for u in U if u["arm"] == "P0"); u1 = next(u for u in U if u["arm"] == "P1")
    rows = [(call_openai if cfg["vendor"] == "openai" else call_anthropic_sync)(lane, u, 0) for u in (u0, u1)]
    ok = all(cfg["model"].split("-2025")[0] in r["served_model"] for r in rows)
    rec = {"lane": lane, "model": cfg["model"], "served": sorted({r["served_model"] for r in rows}), "identifier_ok": ok,
           "p0_in": rows[0]["tok_in"], "p1_in": rows[1]["tok_in"], "out": [r["tok_out"] for r in rows], "parsed": [r["status"] for r in rows],
           "usd": round(sum(r["usd"] for r in rows), 6), "sample": rows[1]["text"][:200], "when": rows[0]["when"]}
    if cfg["transport"] == "raw":
        rec.update({"tok_cached": [r["tok_cached"] for r in rows], "tok_cache_write": [r["tok_cache_write"] for r in rows], "tok_reasoning": [r["tok_reasoning"] for r in rows]})
    d = json.load(io.open(PROBES, encoding="utf-8")) if PROBES.exists() else {}
    d[lane] = rec
    io.open(PROBES, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")
    if any(s != "OK" for s in rec["parsed"]):
        raise SystemExit("probe did not parse -- STOP")


def projection(lane):
    """Expected usd of the lane from its probe (input tokens per arm, output at the recorded lane mean), at the lane's multiplier."""
    pr = json.load(io.open(PROBES, encoding="utf-8"))[lane]; cfg = LANES[lane]; U = units_for(lane)
    out_mean = {"MINI": 24.8, "H45": 182.7, "OP5": 245.1, "LUNA": 191.7}[lane]       # the recorded CF-2 means (projection_r121.json bases)
    n = len(U) * cfg["k"]
    tin = sum((pr["p0_in"] if u["arm"] == "P0" else pr["p1_in"]) for u in U) * cfg["k"]
    if lane == "LUNA":
        # draw 1 at the input rate (a cache write on the prefix, 1.25x on the written part), draws 2-5 mostly cached reads: E5's per-draw bases scaled by the input tokens
        per_unit_in = tin / n
        d1 = (per_unit_in * 1.25 * 0.20 + out_mean * 1.20) / 1e6
        dn = (per_unit_in * (0.02 * 0.998 + 0.20 * 0.002) + out_mean * 1.20) / 1e6
        exp = len(U) * (d1 + (cfg["k"] - 1) * dn); nocache = n * d1
        return {"calls": n, "expected": round(exp, 3), "no_cache": round(nocache, 3), "x1.3_no_cache": round(1.3 * nocache, 3)}
    usd = (tin / 1e6 * cfg["price"][0] + n * out_mean / 1e6 * cfg["price"][1]) * cfg["mult"]
    return {"calls": n, "expected": round(usd, 3), "x1.3": round(1.3 * usd, 3)}


def cmd_project():
    setup()
    tot = {"anthropic": spent_vendor("anthropic"), "openai": spent_vendor("openai")}
    print(f"spent so far: anthropic ${tot['anthropic']:.4f}  openai ${tot['openai']:.4f} (Phase 1's ${PHASE1_OPENAI} included)")
    over = []
    for lane, cfg in LANES.items():
        if not PROBES.exists() or lane not in json.load(io.open(PROBES, encoding="utf-8")):
            print(f"{lane:5s} no probe yet"); continue
        pj = projection(lane); v = cfg["vendor"]
        high = pj.get("x1.3", pj.get("x1.3_no_cache"))
        fits = tot[v] + high <= CAP[v]
        print(f"{lane:5s} {json.dumps(pj)}  -> {v} {tot[v]:.2f} + {high:.2f} = {tot[v] + high:.2f} against {CAP[v]:.2f}  {'fits' if fits else 'OVER'}")
        if not fits:
            over.append(lane)
    if over:
        sys.exit(f"PROJECTION EXCEEDS A CAP AT 1.3x: {over} -- do not launch")


# ------------------------------------------------------------------------------------------------ synchronous lanes
def lane_spent_with_probe(lane):
    pr = json.load(io.open(PROBES, encoding="utf-8")).get(lane, {"usd": 0.0}) if PROBES.exists() else {"usd": 0.0}
    return spent(lane) + pr["usd"]


def cmd_run(lane):
    setup(); cfg = LANES[lane]; assert cfg["vendor"] == "openai"
    if lane in LANE_CAP:
        assert amend1_sha() == AMEND1_SHA, "AMENDMENT 1 SHA MISMATCH -- STOP"; assert (ROWS / "lock_ix_amend1.json").exists(), "lock_amend1 first"
    pr = json.load(io.open(PROBES, encoding="utf-8"))[lane]; assert pr["identifier_ok"]
    U = units_for(lane); path = rows_path(lane); vendor = cfg["vendor"]
    cap_now = (lambda: lane_spent_with_probe(lane) >= LANE_CAP[lane]) if lane in LANE_CAP else (lambda: spent_vendor(vendor) >= CAP[vendor])
    cap_str = f"${LANE_CAP[lane]} (the lane's own cap, Amendment 1)" if lane in LANE_CAP else f"${CAP[vendor]}"
    done = set()
    if path.exists():
        for l in io.open(path, encoding="utf-8"):
            if l.strip():
                r = json.loads(l); done.add((r["unit_id"], int(r["draw"])))
    lock = threading.Lock(); state = {"n": 0, "halted": False}
    print(f"{lane}: {len(U)} units x {cfg['k']} draws; done {len(done)}; lane ${lane_spent_with_probe(lane):.4f}; {vendor} design spend ${spent_vendor(vendor):.4f}; cap {cap_str}", flush=True)

    def work(job):
        u, d = job
        if state["halted"]:
            return None
        with lock:
            if cap_now():
                state["halted"] = True; return None
        row = None
        for attempt in (1, 2, 3):
            try:
                row = call_openai(lane, u, d); break
            except Exception as e:  # noqa: BLE001
                if attempt == 3:
                    row = base_row(u, lane, d) | {"status": f"ERROR:{type(e).__name__}", "when": dt.datetime.now().isoformat(timespec="seconds")}
                else:
                    time.sleep(5 * attempt)
        with lock:
            state["n"] += 1
            with io.open(path, "a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
            if state["n"] % 100 == 0:
                print(f"  {lane} draw {d}: {state['n']} calls this run; {vendor} ${spent_vendor(vendor):.4f}", flush=True)
        return row

    for d in range(1, cfg["k"] + 1):
        jobs = [(u, d) for u in U if (u["unit_id"], d) not in done]
        if not jobs:
            print(f"{lane} draw {d}: complete already", flush=True); continue
        t0 = time.time()
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
            list(ex.map(work, jobs))
        n_ok = sum(1 for l in io.open(path, encoding="utf-8") if l.strip() and (lambda r: r.get("status") == "OK" and int(r["draw"]) == d)(json.loads(l)))
        print(f"{lane} draw {d} done in {time.time() - t0:.0f}s: OK rows {n_ok}/{len(U)}; {vendor} ${spent_vendor(vendor):.4f}", flush=True)
        if state["halted"]:
            print(f"{lane}: CAP REACHED at draw {d}; stopping (whole draws scored, partial draws discarded)", flush=True); break
    print(f"{lane} DONE; lane ${spent(lane):.4f}; {vendor} ${spent_vendor(vendor):.4f}", flush=True)


# ------------------------------------------------------------------------------------------------ Anthropic batches
def cmd_submit(lane):
    setup(); cfg = LANES[lane]; assert cfg["transport"] == "batch"
    pr = json.load(io.open(PROBES, encoding="utf-8"))[lane]; assert pr["identifier_ok"]
    pj = projection(lane); tot = spent_vendor("anthropic")
    assert tot + pj["x1.3"] <= CAP["anthropic"], ("projection over the cap", tot, pj)
    meta_p = ROWS / f"batch_IX_{lane}.json"
    assert not meta_p.exists() and not rows_path(lane).exists(), "a batch or rows file exists for this lane"
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    U = units_for(lane); reqs = []
    for i, u in enumerate(U):
        sysm, user = prompts_for(u)
        for d in range(1, cfg["k"] + 1):
            kw = dict(model=cfg["model"], max_tokens=cfg["max_tokens"], system=sysm, messages=[{"role": "user", "content": user}])
            if cfg["temp"] is not None:
                kw["temperature"] = cfg["temp"]
            reqs.append(Request(custom_id=f"IX-{lane}-{i:04d}-d{d}", params=MessageCreateParamsNonStreaming(**kw)))
    b = RC.anthropic_client().messages.batches.create(requests=reqs)
    meta_p.write_text(json.dumps({"id": b.id, "lane": lane, "n": len(reqs), "units": [u["unit_id"] for u in U], "projection": pj, "submitted": dt.datetime.now().isoformat(timespec="seconds")}, indent=1))
    print("submitted", b.id, len(reqs), "requests; projection", pj)


def cmd_poll(lane):
    setup(); cfg = LANES[lane]
    meta = json.loads((ROWS / f"batch_IX_{lane}.json").read_text())
    cl = RC.anthropic_client(); b = cl.messages.batches.retrieve(meta["id"])
    print(meta["id"], b.processing_status, b.request_counts)
    if b.processing_status != "ended":
        return
    by = {u["unit_id"]: u for u in units_for(lane)}; order = meta["units"]
    n_ok = 0; rows = []
    for res in cl.messages.batches.results(meta["id"]):
        _, _, i, d = res.custom_id.split("-")
        u = by[order[int(i)]]; draw = int(d[1:])
        if res.result.type == "succeeded":
            m = res.result.message
            text = "".join(bl.text for bl in m.content if bl.type == "text")
            row = RC.make_row(u, u["arm"], cfg["model"], draw, text, m.usage.input_tokens, m.usage.output_tokens, cfg["price"], cfg["mult"], m.model)
            row.update(base_row(u, lane, draw)); row["batch_id"] = meta["id"]; n_ok += 1
        else:
            row = base_row(u, lane, draw) | {"status": "BATCH_" + res.result.type.upper(), "batch_id": meta["id"]}
        rows.append(row)
    rows.sort(key=lambda r: (r["unit_id"], r["draw"]))
    with io.open(rows_path(lane), "w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
    print(f"collected {len(rows)} rows; ok {n_ok}; lane ${spent(lane):.4f}; anthropic ${spent_vendor('anthropic'):.4f}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "lock":
        cmd_lock()
    elif cmd == "lock_amend1":
        cmd_lock_amend1()
    elif cmd == "project":
        cmd_project()
    else:
        globals()["cmd_" + cmd](sys.argv[2])
