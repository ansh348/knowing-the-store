# -*- coding: utf-8 -*-
"""r130_run.py -- program R130: the two lanes that CALL THE APIs, under the caps the brief sets (OpenAI 4.00 USD, Anthropic 8.00 USD),
metered from the rows at the page prices and checked before every synchronous call and before the Batch submission (at x1.3).

Lane LUNA (Task A): gpt-5.6-luna through raw Chat Completions as E5, with mini's answer-stage settings wherever Luna accepts the parameter
  (ruling 4 of 2026-09-20): seed 42, JSON mode; temperature 0 rejected by the model (unset); max_completion_tokens 2048 (E5) and reasoning
  effort unset; on the 305 views of build_r130.json with the
  E.10 answer stage's prompt exactly (prompts_ds.SYSTEM_ANSWER; amend4_header.USER_ANSWER_A4 with the persona's name and pinned date);
  the answer read from the last JSON object of the reply, one retry on a parse failure (the Haiku lane's rule); one draw; 8 workers.
  Rows: ds_downstream/run/rows_ds_r130_luna.jsonl (key = item id | view sha256, as every answer-stage rows file).
Lane JUDGE (Task B): claude-opus-5 through Message Batches, temperature unset (the registration's 0 is refused by the API, D-R130-1), max_tokens 300, the frozen judge prompt (r130_common
  JUDGE_SYSTEM / JUDGE_USER, asserted against the registration's fenced blocks before any judge call), one request per unit of
  build/judge_units_r130.json (the 610 recorded answers + the Luna rows); the label read from the last JSON object; a unit whose
  label is not one of the five is re-asked once synchronously (retry-judge). Rows: ds_downstream/run/rows_ds_r130_judge.jsonl.

Subcommands, in order:
  lock | probe-luna | probe-judge | project | run-luna | build-judge | submit-judge | poll-judge | retry-judge | spend
  run-judge-sync (D-R130-2: the judge through the synchronous API after the Batch was cancelled for turnaround) | settle-batch (record what the cancelled Batch delivered)
Records: run/lock_r130.json, run/probes_r130.json, run/projection_r130.json, run/batch_r130_judge.json.
"""
from __future__ import annotations

import concurrent.futures as cf
import io
import json
import os
import sys
import threading
import time

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r130_common as C  # noqa: E402

RUN = C.RUN
LOCK, PROBES, PROJ = RUN / "lock_r130.json", RUN / "probes_r130.json", RUN / "projection_r130.json"
ROWS_LUNA, ROWS_JUDGE = RUN / "rows_ds_r130_luna.jsonl", RUN / "rows_ds_r130_judge.jsonl"
BATCH_JUDGE = RUN / "batch_r130_judge.json"
UNITS = C.BUILD / "judge_units_r130.json"
LUNA = {"model": "gpt-5.6-luna", "max_completion_tokens": 2048, "seed": 42, "response_format": {"type": "json_object"}, "temperature": None,
        "reasoning_effort": None, "price": {"inp": 0.20, "cached": 0.02, "out": 1.20, "write_mult": 1.25},
        "note": "mini's answer-stage settings wherever the parameter exists for Luna (ruling 4): seed 42 and JSON mode as mini; temperature 0 REJECTED by the model "
                "(400 unsupported_value, build/luna_settings_check.json) so unset; max_completion_tokens 2048 as E5 (Luna's limit counts reasoning tokens, mini's max_tokens 200 "
                "counts output only); reasoning effort unset as E5; one retry on a parse failure as mini"}   # page prices: E5 / R125's
JUDGE = {"model": "claude-opus-5", "temperature": None, "max_tokens": 300, "price": (5.00, 25.00), "batch_mult": 0.5,
         "note": "D-R130-1: the registration's temperature 0 is REFUSED by the API for claude-opus-5 ('temperature is deprecated for this model', 400 at the probe, "
                 "2026-09-20); the judge runs with temperature unset (the model's default), as every recorded Opus 5 lane (R114, R125) did"}   # R125's page prices, Batch at 0.5
WORKERS = 8
REASK = {"max_tokens": 1024, "cap_anthropic": 10.00, "seed": 130, "insurance": {"MINI": 7, "H45": 7, "LUNA": 6}}   # D-R130-4 / D-R130-5 (the author's ruling of 2026-09-20)
ROWS_REASK, ROWS_FINAL, INSURANCE = RUN / "rows_ds_r130_judge_reask.jsonl", RUN / "rows_ds_r130_judge_assembled.jsonl", RUN / "insurance_r130.json"
BATCH_RESULTS = RUN / "batch_r130_judge_results.jsonl"


# ------------------------------------------------------------------ setup
def load_env():
    for line in io.open(C.ROOT / ".env", encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def setup(judge=False):
    sha = C.assert_frozen(); C.assert_inputs()
    if judge:
        C.assert_judge_prompt()
    load_env()
    assert os.environ.get("OPENAI_API_KEY") and os.environ.get("ANTHROPIC_API_KEY"), "keys missing"
    return sha


def build():
    b = C.J(C.BUILD / "build_r130.json")
    jobs = b["jobs"]
    got = C.sha_text("".join(j["view_sha"] + j["view"] for j in sorted(jobs, key=lambda j: j["key"])))
    assert got == b["meta"]["views_sha256"], "VIEWS SHA MISMATCH against build_r130.json -- STOP"
    return b


def luna_messages(job):
    import amend4_header as A4  # noqa: E402  (asserts nothing at import; the header and prompt texts are asserted at lock)
    return A4.messages(job)


def last_json(text):
    from run_cf import last_json as lj  # noqa: E402
    return lj(text)


# ------------------------------------------------------------------ spend
def price_openai(usage):
    p = LUNA["price"]; pt = usage.get("prompt_tokens", 0); ct = usage.get("completion_tokens", 0)
    det = usage.get("prompt_tokens_details") or {}; cached = det.get("cached_tokens", 0) or 0; write = det.get("cache_write_tokens", 0) or 0
    plain = max(0, pt - cached - write)
    usd = (plain * p["inp"] + write * p["inp"] * p["write_mult"] + cached * p["cached"] + ct * p["out"]) / 1e6
    return usd, cached, write, ((usage.get("completion_tokens_details") or {}).get("reasoning_tokens", 0) or 0)


def spent(vendor):
    usd = 0.0
    if PROBES.exists():
        for k, v in C.J(PROBES).items():
            if v["vendor"] == vendor:
                usd += v.get("usd", 0.0)
    if vendor == "openai" and ROWS_LUNA.exists():
        usd += sum(json.loads(l).get("usd", 0.0) for l in io.open(ROWS_LUNA, encoding="utf-8") if l.strip())
    if vendor == "anthropic":
        for pth in (ROWS_JUDGE, ROWS_REASK):
            if pth.exists():
                usd += sum(json.loads(l).get("usd", 0.0) for l in io.open(pth, encoding="utf-8") if l.strip())
        if INSURANCE.exists():
            usd += C.J(INSURANCE).get("usd", 0.0)
        if BATCH_JUDGE.exists():
            m = C.J(BATCH_JUDGE)
            if m.get("final_status") != "ended":
                usd += m.get("projection_usd", 0.0)      # a submitted or cancelling Batch counts at its projection (the worst case) until it ends
            else:
                usd += m.get("billed_usd", 0.0)          # what the ended Batch actually delivered (settle-batch)
    return usd


def cmd_spend():
    for v in C.CAP:
        print(f"{v}: metered ${spent(v):.4f} of the ${C.CAP[v]:.2f} cap")


# ------------------------------------------------------------------ lock / probes / projection
def cmd_lock():
    sha = setup(judge=True); b = build()
    import amend4_header as A4  # noqa: E402
    import prompts_ds as PD  # noqa: E402
    lk4 = C.J(RUN / "lock_amend4.json")
    assert C.sha_text(A4.USER_ANSWER_A4) == lk4["user_answer_a4_sha256"] and C.sha_text(A4.HEADER) == lk4["header_sha256"], "the Amendment 4 header differs from AUX-DS-A4-LOCK -- STOP"
    assert PD.digests() == lk4["prompts_ds"], "prompts_ds digests differ from Amendment 4's lock -- STOP"
    A4.RD.assert_lineage()
    rec = {"program": C.PROGRAM, "registration_sha256": sha, "freeze_file": str(C.FREEZE.relative_to(C.ROOT)), "build_views_sha256": b["meta"]["views_sha256"],
           "build_units_sha256": b["meta"]["units_sha256"], "n_views": b["meta"]["n_views"], "n_units_recorded": b["meta"]["n_units_recorded"],
           "answer_prompt": {"system_answer_sha256": PD.digests()["SYSTEM_ANSWER"], "user_answer_a4_sha256": lk4["user_answer_a4_sha256"], "header_sha256": lk4["header_sha256"]},
           "judge_prompt": C.judge_digests(), "luna": {k: v for k, v in LUNA.items()}, "judge": {k: v for k, v in JUDGE.items() if k != "note"}, "caps": C.CAP,
           "inputs_sha256": b["meta"]["inputs_sha256"], "runner_sha256": C.sha_file(__file__), "common_sha256": C.sha_file(C.R130 / "tools" / "r130_common.py"), "when": C.now()}
    C.jdump(rec, LOCK); print(json.dumps(rec, indent=1))


def call_luna(job):
    from openai import OpenAI
    msgs = luna_messages(job)
    cl = OpenAI(max_retries=2, timeout=180)
    r = cl.chat.completions.create(model=LUNA["model"], max_completion_tokens=LUNA["max_completion_tokens"], seed=LUNA["seed"], response_format=LUNA["response_format"], messages=msgs)
    raw = r.model_dump(mode="json"); usage = raw.get("usage") or {}
    text = r.choices[0].message.content or ""
    usd, cached, write, reasoning = price_openai(usage)
    o = last_json(text) or {}
    return {"text": text, "answer": o.get("answer") if isinstance(o.get("answer"), str) else None, "served_model": r.model, "usd": usd, "tok_in": usage.get("prompt_tokens", 0),
            "tok_out": usage.get("completion_tokens", 0), "tok_cached": cached, "tok_cache_write": write, "tok_reasoning": reasoning, "finish_reason": r.choices[0].finish_reason,
            "usage": usage, "system_fingerprint": raw.get("system_fingerprint")}


def call_judge_sync(u, max_tokens=None):
    import anthropic
    sysm, user = C.judge_messages(u)
    cl = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    kw = dict(model=JUDGE["model"], max_tokens=max_tokens or JUDGE["max_tokens"], system=sysm, messages=[{"role": "user", "content": user}])
    if JUDGE["temperature"] is not None:
        kw["temperature"] = JUDGE["temperature"]
    r = cl.messages.create(**kw)
    text = "".join(b.text for b in r.content if b.type == "text")
    o = last_json(text) or {}
    usd = (r.usage.input_tokens * JUDGE["price"][0] + r.usage.output_tokens * JUDGE["price"][1]) / 1e6
    return {"text": text, "label": o.get("label") if o.get("label") in C.LABELS else None, "reason": o.get("reason"), "served_model": r.model, "usd": usd,
            "tok_in": r.usage.input_tokens, "tok_out": r.usage.output_tokens, "mult": 1.0, "stop_reason": r.stop_reason, "max_tokens": kw["max_tokens"]}


def probes():
    return C.J(PROBES) if PROBES.exists() else {}


def cmd_probe_luna():
    setup(); b = build(); assert LOCK.exists()
    job = next(j for j in b["jobs"] if j["source"] == "a4" and j["n_lines"] >= 8)
    r = call_luna(job)
    ok = LUNA["model"] in r["served_model"]
    rec = {"vendor": "openai", "model": LUNA["model"], "served": r["served_model"], "identifier_ok": ok, "key": job["key"], "view_lines": job["n_lines"], "view_chars": len(job["view"]),
           "tok_in": r["tok_in"], "tok_out": r["tok_out"], "tok_reasoning": r["tok_reasoning"], "tok_cached": r["tok_cached"], "tok_cache_write": r["tok_cache_write"], "usd": round(r["usd"], 6),
           "status": "OK" if r["answer"] else "PARSE_FAIL", "finish_reason": r["finish_reason"], "sample": r["text"][:300], "when": C.now()}
    d = probes(); d["LUNA"] = rec; C.jdump(d, PROBES); print(json.dumps(rec, indent=1, ensure_ascii=False))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        raise SystemExit("PROBE PARSE FAILURE -- do not launch")


def cmd_probe_judge():
    setup(judge=True); b = build(); assert LOCK.exists()
    u = next(x for x in b["units"] if x["answerer"] == "MINI" and x["source"] == "a4")
    r = call_judge_sync(u)
    ok = JUDGE["model"] in r["served_model"]
    rec = {"vendor": "anthropic", "model": JUDGE["model"], "served": r["served_model"], "identifier_ok": ok, "unit_id": u["unit_id"], "tok_in": r["tok_in"], "tok_out": r["tok_out"],
           "usd": round(r["usd"], 6), "usd_at_batch": round(r["usd"] * JUDGE["batch_mult"], 6), "status": "OK" if r["label"] else "PARSE_FAIL", "label": r["label"], "sample": r["text"][:300],
           "answer_chars": len(u["answer"]), "when": C.now()}
    d = probes(); d["JUDGE"] = rec; C.jdump(d, PROBES); print(json.dumps(rec, indent=1, ensure_ascii=False))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        raise SystemExit("PROBE PARSE FAILURE -- do not launch")


def project_luna(b, pr):
    """Input tokens scaled by each view's characters against the probe's (the header and system text are part of the probe's count);
    output at the probe's completion tokens (reasoning included) per call."""
    p = LUNA["price"]; ratio = pr["tok_in"] / max(1, pr["view_chars"]); tout = max(1, pr["tok_out"])
    tin = [int(len(j["view"]) * ratio) for j in b["jobs"]]
    usd = sum(t * p["inp"] * p["write_mult"] + tout * p["out"] for t in tin) / 1e6
    return usd, len(tin)


def project_judge(pr, units):
    """Per unit: the probe's input tokens scaled by the unit's answer + reference characters against the probe's, output at the probe's, Batch at 0.5."""
    chars0 = pr["answer_chars"]; ratio = pr["tok_in"] / max(1, chars0 + 300)    # ~300 characters of reference text in the probe's unit
    tout = max(1, pr["tok_out"]); pi, po = JUDGE["price"]
    tin = [int((len(u["answer"] or "") + 300) * ratio) for u in units]
    usd = sum(t * pi + tout * po for t in tin) / 1e6 * JUDGE["batch_mult"]
    return usd, len(units)


def cmd_project():
    setup(); b = build(); pr = probes()
    out = {"caps": C.CAP, "when": C.now()}
    if "LUNA" in pr:
        usd, n = project_luna(b, pr["LUNA"]); sp = spent("openai")
        out["LUNA"] = {"calls": n, "usd": round(usd, 4), "x1.3": round(usd * 1.3, 4), "spent": round(sp, 4), "fits": bool(sp + usd * 1.3 <= C.CAP["openai"])}
        print(f"LUNA : {n} calls, projected ${usd:.4f} (x1.3 ${usd * 1.3:.4f}) + metered ${sp:.4f} against the ${C.CAP['openai']:.2f} OpenAI cap -> {'fits' if out['LUNA']['fits'] else 'EXCEEDS'}")
    if "JUDGE" in pr:
        n_units = b["meta"]["n_units_recorded"] + b["meta"]["n_views"]     # the 610 recorded + one per Luna view
        units = b["units"] + [{"answer": "x" * 400} for _ in range(b["meta"]["n_views"])]    # Luna answers projected at 400 characters each until they exist
        if UNITS.exists():
            units = C.J(UNITS)["units"]; n_units = len(units)
        usd, n = project_judge(pr["JUDGE"], units); sp = spent("anthropic")
        out["JUDGE"] = {"units": n, "usd": round(usd, 4), "x1.3": round(usd * 1.3, 4), "spent": round(sp, 4), "fits": bool(sp + usd * 1.3 <= C.CAP["anthropic"])}
        print(f"JUDGE: {n} units, projected ${usd:.4f} at Batch (x1.3 ${usd * 1.3:.4f}) + metered ${sp:.4f} against the ${C.CAP['anthropic']:.2f} Anthropic cap -> {'fits' if out['JUDGE']['fits'] else 'EXCEEDS'}")
    C.jdump(out, PROJ)
    if any(not out[k]["fits"] for k in ("LUNA", "JUDGE") if k in out):
        raise SystemExit("PROJECTION x1.3 EXCEEDS A CAP -- STOP")


# ------------------------------------------------------------------ Lane LUNA
def cmd_run_luna():
    setup(); b = build(); pr = probes()["LUNA"]; assert pr["identifier_ok"] and C.J(PROJ)["LUNA"]["fits"]
    have = C.read_rows(ROWS_LUNA) if ROWS_LUNA.exists() else {}
    todo = [j for j in b["jobs"] if j["key"] not in have]
    print(f"LUNA: {len(todo)} calls to go (resumed past {len(have)}); OpenAI metered ${spent('openai'):.4f} of ${C.CAP['openai']:.2f}", flush=True)
    lock = threading.Lock(); state = {"spent": spent("openai"), "halted": False, "n": 0}

    def work(job):
        if state["halted"]:
            return None
        with lock:
            if state["spent"] >= C.CAP["openai"]:
                state["halted"] = True; return None
        n_calls, usd, r, err = 0, 0.0, None, None
        for attempt in (1, 2):
            try:
                x = call_luna(job); n_calls += 1; usd += x["usd"]; r = x
                if r["answer"] is not None:
                    break
            except Exception as e:  # noqa: BLE001
                err = f"{type(e).__name__}: {e}"[:200]; time.sleep(5 * attempt)
        rec = {**{k: job[k] for k in ("key", "item_id", "persona", "question", "label", "state", "view_sha", "n_lines", "policies", "source", "key_a4")},
               "model": LUNA["model"], "answer": (r["answer"] if r else None), "status": ("OK" if r and r["answer"] is not None else ("ELICITATION_FAILED" if r else "ERROR")),
               "n_calls": n_calls, "usd": usd, "error": err, "when": C.now(), "seed": LUNA["seed"], "max_completion_tokens": LUNA["max_completion_tokens"],
               "response_format": "json_object", "temperature": None}
        if r:
            rec.update({k: r[k] for k in ("served_model", "tok_in", "tok_out", "tok_cached", "tok_cache_write", "tok_reasoning", "finish_reason", "system_fingerprint")})
            rec["raw"] = r["text"][:600]
            if LUNA["model"] not in r["served_model"]:
                rec["status"] = "IDENTIFIER_MISMATCH"
        with lock:
            state["spent"] += usd; state["n"] += 1
            C.append_rows(ROWS_LUNA, [rec])
            if state["n"] % 50 == 0:
                print(f"  {state['n']} calls, OpenAI ${state['spent']:.4f}", flush=True)
        return rec

    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        out = [r for r in ex.map(work, todo) if r is not None]
    import collections
    print(f"LUNA done in {time.time() - t0:.0f}s: {len(out)} rows, status {dict(collections.Counter(r['status'] for r in out))}; OpenAI metered ${state['spent']:.4f} of ${C.CAP['openai']:.2f}"
          + ("  >>> CAP REACHED" if state["halted"] else ""), flush=True)
    if state["halted"]:
        raise SystemExit(1)


# ------------------------------------------------------------------ Lane JUDGE
def cmd_build_judge():
    setup(judge=True); b = build()
    luna = C.read_rows(ROWS_LUNA)
    assert len(luna) == b["meta"]["n_views"], f"Luna rows {len(luna)} != {b['meta']['n_views']} -- run-luna first"
    D = C.load_ds()
    units = C.judge_units(D, luna_rows=luna)
    assert len(units) == b["meta"]["n_units_recorded"] + b["meta"]["n_views"]
    ok = [u for u in units if u["status"] == "OK" and isinstance(u["answer"], str)]
    skipped = [u["unit_id"] for u in units if u not in ok]
    rec = {"meta": {"n_units": len(ok), "n_skipped_no_answer": len(skipped), "skipped": skipped, "judge_prompt": C.judge_digests(),
                    "units_sha256": C.sha_text("".join(u["unit_id"] + u["question"] + u["stale"] + u["gold"] + u["answer"] for u in sorted(ok, key=lambda u: u["unit_id"]))),
                    "by_answerer": {a: sum(1 for u in ok if u["answerer"] == a) for a in C.ANSWERERS}, "when": C.now()}, "units": ok}
    C.jdump(rec, UNITS); print(json.dumps(rec["meta"], indent=1))


def cmd_submit_judge():
    setup(judge=True); pr = probes()["JUDGE"]; assert pr["identifier_ok"]
    assert not BATCH_JUDGE.exists(), "a judge Batch record exists already -- poll it, do not resubmit"
    units = C.J(UNITS)["units"]
    usd, n = project_judge(pr, units); sp = spent("anthropic")
    assert sp + usd * 1.3 <= C.CAP["anthropic"], f"Anthropic: metered ${sp:.4f} + projection x1.3 ${usd * 1.3:.4f} exceeds the ${C.CAP['anthropic']:.2f} cap -- not submitted"
    import anthropic
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    reqs = []
    for i, u in enumerate(units):
        sysm, user = C.judge_messages(u)
        kw = dict(model=JUDGE["model"], max_tokens=JUDGE["max_tokens"], system=sysm, messages=[{"role": "user", "content": user}])
        if JUDGE["temperature"] is not None:
            kw["temperature"] = JUDGE["temperature"]
        reqs.append(Request(custom_id=f"r130-{i:04d}", params=MessageCreateParamsNonStreaming(**kw)))
    cl = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    bt = cl.messages.batches.create(requests=reqs)
    C.jdump({"id": bt.id, "n": len(reqs), "projection_usd": round(usd, 4), "units_sha256": C.J(UNITS)["meta"]["units_sha256"], "when": C.now()}, BATCH_JUDGE)
    print("submitted", bt.id, len(reqs), "requests; projection at Batch", round(usd, 4))


def cmd_poll_judge():
    setup(judge=True); meta = C.J(BATCH_JUDGE); units = C.J(UNITS)["units"]
    import anthropic
    cl = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"]); bt = cl.messages.batches.retrieve(meta["id"])
    print(meta["id"], bt.processing_status, bt.request_counts)
    if bt.processing_status != "ended":
        return
    assert not ROWS_JUDGE.exists(), "judge rows exist already -- STOP (never re-collect over a rows file)"
    rows, n_ok = [], 0
    for res in cl.messages.batches.results(meta["id"]):
        i = int(res.custom_id.split("-")[1]); u = units[i]
        base = {"key": u["unit_id"], "unit_id": u["unit_id"], "answerer": u["answerer"], "source": u["source"], "view_key": u["key"], "key_a4": u["key_a4"], "item_id": u["item_id"],
                "persona": u["persona"], "state": u["state"], "policies": u["policies"], "batch_id": meta["id"], "model": JUDGE["model"], "temperature": JUDGE["temperature"]}
        if res.result.type == "succeeded":
            m = res.result.message; text = "".join(b.text for b in m.content if b.type == "text"); o = last_json(text) or {}
            lab = o.get("label") if o.get("label") in C.LABELS else None
            usd = (m.usage.input_tokens * JUDGE["price"][0] + m.usage.output_tokens * JUDGE["price"][1]) / 1e6 * JUDGE["batch_mult"]
            row = {**base, "label": lab, "reason": o.get("reason"), "status": "OK" if lab else "PARSE_FAIL", "served_model": m.model, "tok_in": m.usage.input_tokens,
                   "tok_out": m.usage.output_tokens, "usd": usd, "mult": JUDGE["batch_mult"], "raw": text[:600], "n_calls": 1, "stop_reason": m.stop_reason}
            if JUDGE["model"] not in m.model:
                row["status"] = "IDENTIFIER_MISMATCH"
            n_ok += row["status"] == "OK"
        else:
            row = {**base, "label": None, "reason": None, "status": "BATCH_" + res.result.type.upper(), "usd": 0.0, "n_calls": 1}
        rows.append(row)
    rows.sort(key=lambda r: r["unit_id"])
    C.append_rows(ROWS_JUDGE, rows)
    print("collected", len(rows), "rows; OK", n_ok, "; Anthropic metered", f"${spent('anthropic'):.4f}")


def cmd_run_judge_sync():
    """D-R130-2: the judge through the synchronous Messages API (list price), same model, prompt and settings; modest concurrency; up to three
    attempts on a transport error with backoff, then one re-ask on a parse failure (the registered retry); the cap checked before every call
    with the cancelling Batch's projection carried as a worst-case liability until it ends."""
    setup(judge=True); pr = probes()["JUDGE"]; assert pr["identifier_ok"]
    units = C.J(UNITS)["units"]
    have = {json.loads(l)["unit_id"] for l in io.open(ROWS_JUDGE, encoding="utf-8") if l.strip()} if ROWS_JUDGE.exists() else set()
    todo = [(i, u) for i, u in enumerate(units) if u["unit_id"] not in have]
    usd_proj, n = project_judge(pr, [u for _, u in todo]); usd_proj /= JUDGE["batch_mult"]     # synchronous = list price
    sp = spent("anthropic")
    print(f"JUDGE sync: {len(todo)} units to go (resumed past {len(have)}); projected ${usd_proj:.4f} (x1.3 ${usd_proj * 1.3:.4f}) + metered / liable ${sp:.4f} against ${C.CAP['anthropic']:.2f}", flush=True)
    assert sp + usd_proj * 1.3 <= C.CAP["anthropic"], "PROJECTION x1.3 EXCEEDS THE ANTHROPIC CAP -- STOP"
    lock = threading.Lock(); state = {"spent": sp, "halted": False, "n": 0}
    stamp = "sync-" + C.now()[:10]

    def work(job):
        i, u = job
        if state["halted"]:
            return None
        with lock:
            if state["spent"] >= C.CAP["anthropic"]:
                state["halted"] = True; return None
        n_calls, usd, r, err = 0, 0.0, None, None
        for parse_try in (1, 2):                              # the registered one re-ask on a parse failure
            for attempt in (1, 2, 3):                         # transport errors: three attempts with backoff
                try:
                    x = call_judge_sync(u); n_calls += 1; usd += x["usd"]; r = x; err = None; break
                except Exception as e:  # noqa: BLE001
                    err = f"{type(e).__name__}: {e}"[:200]; time.sleep(5 * attempt)
            if r is not None and r["label"] is not None:
                break
        base = {"key": u["unit_id"], "unit_id": u["unit_id"], "answerer": u["answerer"], "source": u["source"], "view_key": u["key"], "key_a4": u["key_a4"], "item_id": u["item_id"],
                "persona": u["persona"], "state": u["state"], "policies": u["policies"], "batch_id": stamp, "model": JUDGE["model"], "temperature": JUDGE["temperature"], "n_calls": n_calls, "usd": usd,
                "mult": 1.0, "transport": "synchronous (D-R130-2)", "error": err, "when": C.now()}
        if r is None:
            row = {**base, "label": None, "reason": None, "status": "ERROR"}
        else:
            row = {**base, "label": r["label"], "reason": r["reason"], "status": "OK" if r["label"] else "PARSE_FAIL", "served_model": r["served_model"], "tok_in": r["tok_in"], "tok_out": r["tok_out"], "raw": r["text"][:600]}
            if JUDGE["model"] not in r["served_model"]:
                row["status"] = "IDENTIFIER_MISMATCH"
        with lock:
            state["spent"] += usd; state["n"] += 1
            C.append_rows(ROWS_JUDGE, [row])
            if state["n"] % 100 == 0:
                print(f"  {state['n']} units, Anthropic ${state['spent']:.4f}", flush=True)
        return row

    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        out = [r for r in ex.map(work, todo) if r is not None]
    import collections
    print(f"JUDGE sync done in {time.time() - t0:.0f}s: {len(out)} rows, status {dict(collections.Counter(r['status'] for r in out))}; Anthropic metered / liable ${state['spent']:.4f} of ${C.CAP['anthropic']:.2f}"
          + ("  >>> CAP REACHED" if state["halted"] else ""), flush=True)
    if state["halted"]:
        raise SystemExit(1)


def cmd_settle_batch():
    """Poll the cancelled Batch; once ended, record what it delivered (succeeded requests are billed) into run/batch_r130_judge_results.jsonl
    (spend record only; the synchronous rows are the scored lane) and billed_usd into the batch record."""
    setup(judge=True); meta = C.J(BATCH_JUDGE)
    import anthropic
    cl = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"]); bt = cl.messages.batches.retrieve(meta["id"]); c = bt.request_counts
    print(meta["id"], bt.processing_status, c)
    meta["final_status"] = bt.processing_status
    meta["final_counts"] = {"processing": c.processing, "succeeded": c.succeeded, "errored": c.errored, "canceled": c.canceled, "expired": c.expired}
    if bt.processing_status == "ended":
        billed, rows = 0.0, []
        if c.succeeded:
            for res in cl.messages.batches.results(meta["id"]):
                if res.result.type == "succeeded":
                    m = res.result.message
                    usd = (m.usage.input_tokens * JUDGE["price"][0] + m.usage.output_tokens * JUDGE["price"][1]) / 1e6 * JUDGE["batch_mult"]; billed += usd
                    rows.append({"custom_id": res.custom_id, "usd": usd, "tok_in": m.usage.input_tokens, "tok_out": m.usage.output_tokens, "served_model": m.model,
                                 "text": "".join(b.text for b in m.content if b.type == "text")[:600]})
            C.append_rows(RUN / "batch_r130_judge_results.jsonl", rows)
        meta["billed_usd"] = round(billed, 4); meta["settled"] = C.now()
        print(f"ended: succeeded {c.succeeded} (billed ${billed:.4f} at Batch), canceled {c.canceled}")
    C.jdump(meta, BATCH_JUDGE)


def batch_labels():
    """{unit index: (label, reason, row)} for the Batch's succeeded results (max_tokens 300; a truncated reply parses to None)."""
    out = {}
    if not BATCH_RESULTS.exists():
        return out
    for l in io.open(BATCH_RESULTS, encoding="utf-8"):
        if l.strip():
            r = json.loads(l); i = int(r["custom_id"].split("-")[1]); o = last_json(r["text"]) or {}
            out[i] = (o.get("label") if o.get("label") in C.LABELS else None, o.get("reason"), r)
    return out


def sync_rows(path):
    return {json.loads(l)["unit_id"]: json.loads(l) for l in io.open(path, encoding="utf-8") if l.strip()} if path.exists() else {}


def recorded_label(i, u, bl, sy):
    """(label, transport) already on record for unit i: the Batch's parsed label, else the synchronous run's OK label, else None."""
    if i in bl and bl[i][0]:
        return bl[i][0], "batch"
    r = sy.get(u["unit_id"])
    if r and r["status"] == "OK":
        return r["label"], "sync"
    return None, None


def reask_one(u, max_tokens):
    n_calls, usd, r, err = 0, 0.0, None, None
    for parse_try in (1, 2):
        for attempt in (1, 2, 3):
            try:
                x = call_judge_sync(u, max_tokens=max_tokens); n_calls += 1; usd += x["usd"]; r = x; err = None; break
            except Exception as e:  # noqa: BLE001
                err = f"{type(e).__name__}: {e}"[:200]; time.sleep(5 * attempt)
        if r is not None and r["label"] is not None:
            break
    return n_calls, usd, r, err


def cmd_reask_judge():
    """D-R130-4: the units without a parsed label under max_tokens 300 (the Batch's truncated replies and the cancelled requests the synchronous run
    did not reach or also truncated) re-asked once more at max_tokens 1024, same prompt and model, synchronous; D-R130-5: the Anthropic cap for
    this lane is $10.00. A unit that still fails stays PARSE_FAIL and is counted."""
    setup(judge=True); units = C.J(UNITS)["units"]; bl = batch_labels(); sy = sync_rows(ROWS_JUDGE); done = sync_rows(ROWS_REASK)
    todo = [(i, u) for i, u in enumerate(units) if recorded_label(i, u, bl, sy)[0] is None and u["unit_id"] not in done]
    sp = spent("anthropic"); worst = len(todo) * (600 * JUDGE["price"][0] + REASK["max_tokens"] * JUDGE["price"][1]) / 1e6
    print(f"re-ask: {len(todo)} units (resumed past {len(done)}); metered ${sp:.4f}; worst case ${worst:.4f} -> ${sp + worst:.4f} against the ${REASK['cap_anthropic']:.2f} lane cap", flush=True)
    assert sp + worst <= REASK["cap_anthropic"], "WORST CASE EXCEEDS THE LANE CAP -- STOP"
    lock = threading.Lock(); state = {"spent": sp, "halted": False, "n": 0}

    def work(job):
        i, u = job
        if state["halted"]:
            return None
        with lock:
            if state["spent"] >= REASK["cap_anthropic"]:
                state["halted"] = True; return None
        n_calls, usd, r, err = reask_one(u, REASK["max_tokens"])
        base = {"key": u["unit_id"], "unit_id": u["unit_id"], "unit_index": i, "answerer": u["answerer"], "source": u["source"], "view_key": u["key"], "key_a4": u["key_a4"], "item_id": u["item_id"],
                "persona": u["persona"], "state": u["state"], "policies": u["policies"], "batch_id": "reask-" + C.now()[:10], "model": JUDGE["model"], "temperature": JUDGE["temperature"],
                "max_tokens": REASK["max_tokens"], "n_calls": n_calls, "usd": usd, "mult": 1.0, "transport": "synchronous re-ask at max_tokens 1024 (D-R130-4)", "error": err, "when": C.now()}
        if r is None:
            row = {**base, "label": None, "reason": None, "status": "ERROR"}
        else:
            row = {**base, "label": r["label"], "reason": r["reason"], "status": "OK" if r["label"] else "PARSE_FAIL", "served_model": r["served_model"], "tok_in": r["tok_in"], "tok_out": r["tok_out"],
                   "stop_reason": r["stop_reason"], "raw": r["text"][:600]}
            if JUDGE["model"] not in r["served_model"]:
                row["status"] = "IDENTIFIER_MISMATCH"
        with lock:
            state["spent"] += usd; state["n"] += 1
            C.append_rows(ROWS_REASK, [row])
        return row

    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        out = [r for r in ex.map(work, todo) if r is not None]
    import collections
    print(f"re-ask done: {len(out)} rows, status {dict(collections.Counter(r['status'] for r in out))}; tok_out max {max((r.get('tok_out', 0) for r in out), default=0)}; "
          f"Anthropic metered ${state['spent']:.4f} of the ${REASK['cap_anthropic']:.2f} lane cap" + ("  >>> CAP REACHED" if state["halted"] else ""), flush=True)
    if state["halted"]:
        raise SystemExit(1)


def cmd_insurance_judge():
    """The author's insurance check: 20 already-parsed units (seeded draw, stratified 7 mini / 7 Haiku / 6 Luna) re-asked at max_tokens 1024; every label must
    equal its recorded label, else STOP."""
    import random
    setup(judge=True); units = C.J(UNITS)["units"]; bl = batch_labels(); sy = sync_rows(ROWS_JUDGE)
    assert not INSURANCE.exists(), "insurance record exists -- STOP (run once)"
    rng = random.Random(REASK["seed"]); picks = []
    for a, k in REASK["insurance"].items():
        pool = sorted(i for i, u in enumerate(units) if u["answerer"] == a and recorded_label(i, u, bl, sy)[0])
        picks += rng.sample(pool, k)
    rows = []
    for i in picks:
        u = units[i]; lab, tr = recorded_label(i, u, bl, sy)
        n_calls, usd, r, err = reask_one(u, REASK["max_tokens"])
        rows.append({"unit_index": i, "answerer": u["answerer"], "recorded_label": lab, "recorded_transport": tr, "reask_label": r["label"] if r else None, "match": bool(r and r["label"] == lab),
                     "n_calls": n_calls, "usd": usd, "tok_out": r["tok_out"] if r else None, "stop_reason": r["stop_reason"] if r else None, "error": err})
    import collections
    rec = {"seed": REASK["seed"], "strata": REASK["insurance"], "n": len(rows), "matches": sum(r["match"] for r in rows), "mismatches": sum(not r["match"] for r in rows),
           "by_answerer": {a: {"n": sum(1 for r in rows if r["answerer"] == a), "matches": sum(1 for r in rows if r["answerer"] == a and r["match"])} for a in C.ANSWERERS},
           "mismatch_pairs": dict(collections.Counter(f"{r['recorded_label']}->{r['reask_label']}" for r in rows if not r["match"])),
           "usd": round(sum(r["usd"] for r in rows), 4), "max_tokens": REASK["max_tokens"], "when": C.now(), "rows": rows}
    C.jdump(rec, INSURANCE)
    print(json.dumps({k: v for k, v in rec.items() if k != "rows"}, indent=1))
    if rec["mismatches"]:
        raise SystemExit("INSURANCE CHECK: a re-asked label differs from its recorded label -- STOP")


def cmd_assemble_judge():
    """One label per unit: the Batch's parsed label, else the synchronous run's OK label, else the re-ask's; the transport recorded per row; a unit with no
    parsed label anywhere is PARSE_FAIL. Writes rows_ds_r130_judge_assembled.jsonl, the file the scorer reads."""
    setup(judge=True); units = C.J(UNITS)["units"]; bl = batch_labels(); sy = sync_rows(ROWS_JUDGE); rk = sync_rows(ROWS_REASK)
    assert not ROWS_FINAL.exists(), "assembled rows exist -- STOP (never re-assemble over a rows file)"
    rows, src = [], []
    for i, u in enumerate(units):
        base = {"key": u["unit_id"], "unit_id": u["unit_id"], "unit_index": i, "answerer": u["answerer"], "source": u["source"], "view_key": u["key"], "key_a4": u["key_a4"], "item_id": u["item_id"],
                "persona": u["persona"], "state": u["state"], "policies": u["policies"], "model": JUDGE["model"], "temperature": JUDGE["temperature"]}
        if i in bl and bl[i][0]:
            lab, reason, r = bl[i]
            row = {**base, "label": lab, "reason": reason, "status": "OK", "transport": "batch", "batch_id": C.J(BATCH_JUDGE)["id"], "max_tokens": JUDGE["max_tokens"], "served_model": r["served_model"],
                   "tok_in": r["tok_in"], "tok_out": r["tok_out"], "usd": 0.0, "usd_note": "billed in the Batch's total (batch_r130_judge.json billed_usd)", "n_calls": 1}
        elif u["unit_id"] in sy and sy[u["unit_id"]]["status"] == "OK":
            r = sy[u["unit_id"]]; row = {**base, **{k: r[k] for k in ("label", "reason", "status", "transport", "batch_id", "served_model", "tok_in", "tok_out", "n_calls")}, "max_tokens": JUDGE["max_tokens"], "usd": 0.0,
                                         "usd_note": "billed in rows_ds_r130_judge.jsonl"}
        elif u["unit_id"] in rk:
            r = rk[u["unit_id"]]; row = {**base, **{k: r.get(k) for k in ("label", "reason", "status", "transport", "batch_id", "served_model", "tok_in", "tok_out", "n_calls", "stop_reason")}, "max_tokens": REASK["max_tokens"],
                                         "usd": 0.0, "usd_note": "billed in rows_ds_r130_judge_reask.jsonl"}
        else:
            row = {**base, "label": None, "reason": None, "status": "PARSE_FAIL", "transport": "none", "usd": 0.0, "n_calls": 0}
        rows.append(row); src.append(row["transport"] if row["status"] == "OK" else "PARSE_FAIL")
    C.append_rows(ROWS_FINAL, rows)
    import collections
    print("assembled", len(rows), "rows;", dict(collections.Counter(src)), "; labels", dict(collections.Counter(r["label"] for r in rows)))


def cmd_retry_judge():
    """One synchronous retry (full price) for every unit whose Batch row is not OK; the row is rewritten in place."""
    setup(judge=True); units = {u["unit_id"]: u for u in C.J(UNITS)["units"]}
    rows = [json.loads(l) for l in io.open(ROWS_JUDGE, encoding="utf-8") if l.strip()]
    bad = [r for r in rows if r["status"] != "OK" and r.get("n_calls", 1) < 2]
    print(f"{len(bad)} units to retry; Anthropic metered ${spent('anthropic'):.4f}")
    for r in bad:
        if spent("anthropic") + sum(x.get("usd", 0.0) for x in rows if x.get("n_calls", 1) >= 2) >= C.CAP["anthropic"]:
            print("cap reached; stopping"); break
        x = call_judge_sync(units[r["unit_id"]])
        r.update({"label": x["label"], "reason": x["reason"], "status": "OK" if x["label"] else "PARSE_FAIL", "served_model": x["served_model"], "tok_in": x["tok_in"], "tok_out": x["tok_out"],
                  "usd": r.get("usd", 0.0) + x["usd"], "mult_retry": 1.0, "raw": x["text"][:600], "n_calls": 2, "retried": C.now()})
    with io.open(ROWS_JUDGE, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
    import collections
    print("status", dict(collections.Counter(r["status"] for r in rows)))


if __name__ == "__main__":
    cmd = sys.argv[1]
    {"lock": cmd_lock, "probe-luna": cmd_probe_luna, "probe-judge": cmd_probe_judge, "project": cmd_project, "run-luna": cmd_run_luna, "build-judge": cmd_build_judge,
     "submit-judge": cmd_submit_judge, "poll-judge": cmd_poll_judge, "run-judge-sync": cmd_run_judge_sync, "settle-batch": cmd_settle_batch, "retry-judge": cmd_retry_judge,
     "reask-judge": cmd_reask_judge, "insurance-judge": cmd_insurance_judge, "assemble-judge": cmd_assemble_judge, "spend": cmd_spend}[cmd]()
