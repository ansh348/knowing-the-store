"""amend2_lit.py -- ADDENDUM_DS Amendment 2 (registrations/ADDENDUM_DS_AMENDMENT_2.md, frozen by sha256 before the
first call; program R106, 2026-09-14): the answer stage of the literal-threshold lookup rule (LOOKUP-LIT) under the
section D.4 protocol (Lane 1, gpt-4.1-mini), and Claude Haiku 4.5 as a second answerer on every distinct (item, view)
pair of Stage 2 across the seven policies (Lane 2). Descriptive: no bar, no prediction, no verdict.

MODEL CALLS: Lane 1 -- gpt-4.1-mini through run_ds.answer (temperature 0, seed 42, max_tokens 200, JSON mode, one retry),
one call per LOOKUP-LIT view not already answered under a registered policy (the DS cache is read first; ds_downstream/cache
is never written). Lane 2 -- claude-haiku-4-5-20251001, temperature 0, max_tokens 200, k = 1, the same two prompt texts,
synchronous Messages API, the answer read from the last JSON object of the reply with one retry. No monitor elicited, no
summary rendered, no lookup re-scored, no embedding call. The registered artifacts (stage1.json, views.json, rows_ds.jsonl,
scores_ds.json) are read and never written. Artifacts: run/*_amend2*.json, run/rows_ds_amend2.jsonl, run/rows_ds_amend2_h45.jsonl.

Subcommands, in order:
  lock            registration sha256, prompts, population counts (268 / 238 / 30; 452) -> run/lock_amend2.json
  probe-mini      one gpt-4.1-mini call on a new LOOKUP-LIT view (served identifier)  -> run/probes_amend2.json
  probe-h45       three Haiku 4.5 calls on recorded views (served identifier, tokens)  -> run/probes_amend2.json
  project         both lanes' projections against the DS $4 rule and the author's $5 line -> run/projection_amend2.json
  stage2-mini     Lane 1: the 268 LOOKUP-LIT rows (238 copied from rows_ds.jsonl, 30 new calls) -> run/rows_ds_amend2.jsonl
  stage2-h45      Lane 2: 452 Haiku 4.5 rows -> run/rows_ds_amend2_h45.jsonl (stops at the $5 hard cap)
  score           the committed detector on every answer; NUMBERS_DS.md section 7 (AUX-DS-A2-*) -> run/scores_amend2.json
"""
from __future__ import annotations

import collections
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
import ds_common as DC                                                       # noqa: E402
from ds_common import ROOT, DS, RUN, J, jdump, POLICIES, STAGE2_POLICIES     # noqa: E402
import run_ds as RD                                                          # noqa: E402
import prompts_ds as PD                                                      # noqa: E402
import prompts_e1 as P                                                       # noqa: E402

sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
from run_cf import last_json, load_env                                       # noqa: E402

api = DC.RC.e1_api()
REG = ROOT / "registrations" / "ADDENDUM_DS_AMENDMENT_2.md"
REG_SHA = "a3ff9d89c7b330d1243bc50d9b619b8497239f7f3757cb59816cf2e17fe3bdec"
CACHE2 = DS / "cache_amend2"
POLICY = "LOOKUP-LIT"
LANE_MINI, PRICE_MINI = RD.LANE, RD.PRICE
LANE_H45, PRICE_H45 = "claude-haiku-4-5-20251001", (1.00, 5.00)
LINE_H45, RULE_MINI = 5.00, RD.BUDGET
ROWS_MINI = RUN / "rows_ds_amend2.jsonl"
ROWS_H45 = RUN / "rows_ds_amend2_h45.jsonl"
LEDGER = DS / "NUMBERS_DS.md"
EXPECT = {"nominal": 268, "reused": 238, "new": 30, "new_pn": 6, "new_present": 24, "h45_views": 452}


def assert_lineage():
    sha = hashlib.sha256(REG.read_bytes()).hexdigest()
    assert sha == REG_SHA, f"ADDENDUM_DS_AMENDMENT_2.md sha256 {sha} != frozen -- STOP"
    RD.assert_lineage()


def redirect():
    CACHE2.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                             # noqa: SLF001
    e0.CACHE_PATH = CACHE2 / "responses.json"; e0.LEDGER_PATH = CACHE2 / "cost_ledger.json"
    e0._cache = None; c = e0._load_cache()                                   # noqa: SLF001
    ds_cache = DS / "cache" / "responses.json"
    n0 = len(c)
    for k, v in J(ds_cache).items():
        c.setdefault(k, v)
    print(f"cache seeded with {len(c) - n0} recorded DS answers (read-only copy; ds_downstream/cache is not written)")
    e0.HARD_CAP_USD = RULE_MINI
    return e0


# ------------------------------------------------------------------ populations
def recorded_rows():
    return {json.loads(l)["key"]: json.loads(l) for l in io.open(RD.ROWS_P, encoding="utf-8")}


def lit_jobs():
    """The LOOKUP-LIT Stage 2 population under run_ds.build_cell's rule; `recorded` marks a view already answered."""
    sub = DC.load_cell()
    st1 = J(DS / "stage1.json")["per_item"]; views = J(DS / "views.json")["items"]
    done = recorded_rows(); jobs = []
    for it in sub:
        s = st1[it["item_id"]][POLICY]
        if s["abstain"] or it["label"] == "ABSENT" or (it["label"] == "PRESENT-NEGATIVE" and not s["reach"]):
            continue
        v = views[it["item_id"]][POLICY]; key = f"{it['item_id']}|{v['sha']}"
        jobs.append({"key": key, "item_id": it["item_id"], "persona": it["persona"], "question": it["question"], "label": it["label"],
                     "state": it["state"], "view": v["text"], "view_sha": v["sha"], "n_lines": v["n_lines"], "policies": [POLICY], "recorded": key in done})
    return sub, jobs, done


def counts(jobs):
    new = [j for j in jobs if not j["recorded"]]
    return {"nominal": len(jobs), "reused": len(jobs) - len(new), "new": len(new),
            "new_pn": sum(1 for j in new if j["label"] == "PRESENT-NEGATIVE"), "new_present": sum(1 for j in new if j["label"] == "PRESENT")}


def h45_jobs():
    """Every distinct (item, view) of Stage 2 across the seven policies: the 422 recorded pairs plus the new LOOKUP-LIT pairs."""
    sub, jobs, done = lit_jobs()
    cell = J(RUN / "cell_ds.json")["jobs"]
    out = {}
    for j in cell:
        out[j["key"]] = {k: j[k] for k in ("key", "item_id", "persona", "question", "label", "state", "view", "view_sha", "n_lines")}
        out[j["key"]]["policies"] = list(j["policies"])
    for j in jobs:
        if j["key"] in out:
            if POLICY not in out[j["key"]]["policies"]:
                out[j["key"]]["policies"].append(POLICY)
        else:
            out[j["key"]] = {k: j[k] for k in ("key", "item_id", "persona", "question", "label", "state", "view", "view_sha", "n_lines")}
            out[j["key"]]["policies"] = [POLICY]
    return sub, list(out.values())


def cmd_lock():
    assert_lineage()
    sub, jobs, done = lit_jobs(); c = counts(jobs); sub2, hj = h45_jobs()
    c["h45_views"] = len(hj)
    ok = all(c[k] == v for k, v in EXPECT.items())
    out = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "prompts_ds": PD.digests(),
           "prompts_e1": {"file": P.file_sha256(), "texts": P.texts_sha256()}, "recorded_rows": len(done), "population": c, "expected": EXPECT,
           "population_ok": ok, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RUN / "lock_amend2.json"); print(json.dumps(out, indent=1))
    if not ok:
        sys.exit("POPULATION COUNTS DO NOT REPRODUCE THE REGISTRATION -- STOP")


# ------------------------------------------------------------------ probes
def probes():
    p = RUN / "probes_amend2.json"
    return J(p) if p.exists() else {}


def cmd_probe_mini():
    assert_lineage(); e0 = redirect()
    sub, jobs, done = lit_jobs()
    first = next(j for j in jobs if not j["recorded"] and j["label"] == "PRESENT-NEGATIVE")
    r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,   # noqa: SLF001
                                             messages=RD.messages(first), response_format={"type": "json_object"})
    o = api.parse_json(r.choices[0].message.content) or {}
    rec = {"item_id": first["item_id"], "view_lines": first["n_lines"], "served": r.model, "identifier_ok": LANE_MINI in r.model,
           "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens,
           "usd": r.usage.prompt_tokens / 1e6 * PRICE_MINI[0] + r.usage.completion_tokens / 1e6 * PRICE_MINI[1],
           "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL", "sample": (r.choices[0].message.content or "")[:300],
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    out = probes(); out["MINI"] = rec; jdump(out, RUN / "probes_amend2.json"); print(json.dumps(rec, indent=1))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def anthropic_client():
    load_env()
    import anthropic
    return anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def h45_once(client, job):
    msgs = RD.messages(job)
    r = client.messages.create(model=LANE_H45, max_tokens=200, temperature=0.0, system=msgs[0]["content"],
                               messages=[{"role": "user", "content": msgs[1]["content"]}])
    text = "".join(b.text for b in r.content if b.type == "text")
    return text, r.usage.input_tokens, r.usage.output_tokens, r.model


def cmd_probe_h45():
    assert_lineage()
    sub, hj = h45_jobs()
    rec = [j for j in hj if j["key"] in recorded_rows()]
    picks = [next(j for j in rec if j["label"] == "PRESENT-NEGATIVE"), next(j for j in rec if j["label"] == "PRESENT"), max(rec, key=lambda j: j["n_lines"])]
    cl = anthropic_client(); out = probes(); out["H45"] = []
    for j in picks:
        text, tin, tout, served = h45_once(cl, j)
        o = last_json(text) or {}
        out["H45"].append({"item_id": j["item_id"], "view_lines": j["n_lines"], "served": served, "identifier_ok": served == LANE_H45, "tok_in": tin, "tok_out": tout,
                           "usd": tin / 1e6 * PRICE_H45[0] + tout / 1e6 * PRICE_H45[1], "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL",
                           "sample": text[:300], "when": dt.datetime.now().isoformat(timespec="seconds")})
    jdump(out, RUN / "probes_amend2.json"); print(json.dumps(out["H45"], indent=1))
    if not all(x["identifier_ok"] for x in out["H45"]):
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if any(x["status"] != "OK" for x in out["H45"]):
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def cmd_project():
    pr = probes(); sub, jobs, done = lit_jobs(); new = [j for j in jobs if not j["recorded"]]; sub2, hj = h45_jobs()
    dsp = J(RUN / "probes_ds.json")["ANSWER"]; per_line = 45.0; shell = max(50.0, dsp["tok_in"] - per_line * dsp["view_lines"])
    tin = sum(shell + per_line * j["n_lines"] for j in new); tout = dsp["tok_out"] * len(new)
    usd_mini = tin / 1e6 * PRICE_MINI[0] + tout / 1e6 * PRICE_MINI[1]
    billed_ds = RD.billed_so_far()["total"]
    a1 = RUN / "scores_amend1.json"; billed_a1 = J(a1)["spend"]["stage2"] if a1.exists() else 0.0
    h = pr["H45"]; per_line_h = 45.0
    shell_h = max(50.0, min(x["tok_in"] - per_line_h * x["view_lines"] for x in h)); tout_h = max(x["tok_out"] for x in h)
    tin_h = sum(shell_h + per_line_h * j["n_lines"] for j in hj); tout_h_all = tout_h * len(hj)
    usd_h45 = tin_h / 1e6 * PRICE_H45[0] + tout_h_all / 1e6 * PRICE_H45[1]
    out = {"mini": {"new_calls": len(new), "projected_usd": usd_mini, "billed_ds_and_probe": billed_ds + pr["MINI"]["usd"], "billed_amend1_stage2": billed_a1,
                    "rule": RULE_MINI, "total_against_rule": billed_ds + pr["MINI"]["usd"] + billed_a1 + usd_mini},
           "h45": {"views": len(hj), "projected_usd": usd_h45, "x1_3": 1.3 * usd_h45, "probe_usd": sum(x["usd"] for x in h), "line": LINE_H45,
                   "runs": 1.3 * usd_h45 + sum(x["usd"] for x in h) < LINE_H45},
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RUN / "projection_amend2.json"); print(json.dumps(out, indent=1))
    if out["mini"]["total_against_rule"] > RULE_MINI:
        sys.exit("MINI PROJECTION ABOVE THE $4 RULE -- STOP")
    if not out["h45"]["runs"]:
        print("HAIKU LANE: projection x1.3 at or above the $5 line -- the lane does not run (registration section A2.6)")


# ------------------------------------------------------------------ lanes
def cmd_stage2_mini():
    assert_lineage(); redirect()
    sub, jobs, done = lit_jobs(); c = counts(jobs)
    assert all(c[k] == v for k, v in EXPECT.items() if k in c), c
    have = {json.loads(l)["key"] for l in io.open(ROWS_MINI, encoding="utf-8")} if ROWS_MINI.exists() else set()
    todo = [j for j in jobs if j["key"] not in have]
    print(f"{len(todo)} rows to write ({sum(1 for j in todo if j['recorded'])} recorded answers copied, {sum(1 for j in todo if not j['recorded'])} new calls)", flush=True)
    lock = threading.Lock()

    def work(job):
        if job["recorded"]:
            r = dict(done[job["key"]]); r["policies"] = [POLICY]; r["source"] = "ds_downstream/run/rows_ds.jsonl"; r["usd"] = 0.0
        else:
            r = RD.answer(job); r["source"] = "amend2 call"
        with lock:
            with io.open(ROWS_MINI, "a", encoding="utf-8") as f:
                f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
        return r
    try:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            out = list(ex.map(work, todo))
    finally:
        api.flush()
    cnt = collections.Counter(r["status"] for r in out)
    print(f"DONE {len(out)} rows; status {dict(cnt)}; billed this step ${sum(r.get('usd', 0.0) for r in out):.4f}")


def cmd_stage2_h45():
    assert_lineage()
    pj = J(RUN / "projection_amend2.json")
    assert pj["h45"]["runs"], "the Haiku lane's projection is at or above the $5 line -- STOP"
    sub, hj = h45_jobs(); assert len(hj) == EXPECT["h45_views"], len(hj)
    have = {json.loads(l)["key"] for l in io.open(ROWS_H45, encoding="utf-8")} if ROWS_H45.exists() else set()
    todo = [j for j in hj if j["key"] not in have]
    print(f"{len(todo)} Haiku calls to go (resumed past {len(have)})", flush=True)
    cl = anthropic_client(); lock = threading.Lock(); spend = [sum(json.loads(l).get("usd", 0.0) for l in io.open(ROWS_H45, encoding="utf-8"))] if ROWS_H45.exists() else [0.0]
    stopped = [False]

    def work(job):
        with lock:
            if spend[0] >= LINE_H45 or stopped[0]:
                stopped[0] = True; return None
        n_calls, failed, usd, text, served, tin, tout = 0, False, 0.0, "", None, 0, 0
        o = {}
        for attempt in range(2):
            for backoff in range(4):
                try:
                    text, tin_, tout_, served = h45_once(cl, job); break
                except Exception as e:                                 # noqa: BLE001
                    if backoff == 3:
                        raise
                    time.sleep(2 ** backoff)
            n_calls += 1; usd += tin_ / 1e6 * PRICE_H45[0] + tout_ / 1e6 * PRICE_H45[1]; tin, tout = tin_, tout_
            o = last_json(text) or {}
            if isinstance(o.get("answer"), str):
                break
        else:
            failed = True
        r = {**{k: job[k] for k in ("key", "item_id", "persona", "question", "label", "state", "view_sha", "n_lines", "policies")},
             "answer": (o.get("answer") if not failed else None), "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls,
             "model": LANE_H45, "served_model": served, "cached": False, "tok_in": tin, "tok_out": tout, "usd": usd, "raw": (text or "")[:400], "source": "amend2 call"}
        with lock:
            spend[0] += usd
            with io.open(ROWS_H45, "a", encoding="utf-8") as f:
                f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
        return r
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        out = [r for r in ex.map(work, todo) if r is not None]
    cnt = collections.Counter(r["status"] for r in out)
    print(f"DONE {len(out)} rows; status {dict(cnt)}; billed this step ${sum(r['usd'] for r in out):.4f}; lane total ${spend[0]:.4f} against ${LINE_H45:.2f}" + ("  >>> STOPPED AT THE LINE" if stopped[0] else ""))
    if stopped[0]:
        sys.exit(1)


# ------------------------------------------------------------------ score
def summarize(rows, per_row, byid, st1, policy):
    """AUX-DS-STAGE2's columns for one policy from rows keyed (item, view) whose `policies` list carries it."""
    per = st1[policy] if isinstance(st1, dict) and policy in st1 else None
    sel = [(k, s) for k, s in per_row.items() if s["scored"] and policy in rows[k]["policies"]]
    pn = [(k, s) for k, s in sel if byid[rows[k]["item_id"]]["label"] == "PRESENT-NEGATIVE"]
    pr = [(k, s) for k, s in sel if byid[rows[k]["item_id"]]["label"] == "PRESENT"]
    d = {"pn_answered": len(pn), "present_answered": len(pr),
         "failed": sum(1 for k, s in per_row.items() if not s["scored"] and policy in rows[k]["policies"] and s["status"] != "OK")}
    for split, pred in (("all", lambda it: True), ("tagged", lambda it: it["tagged"]), ("untagged", lambda it: not it["tagged"])):
        ss = [s for k, s in pn if pred(_tag(byid[rows[k]["item_id"]], policy))]; n = len(ss)
        d[f"pn_{split}"] = {"n": n, "stale_use": sum(1 for s in ss if s["stale_use"]), "stale_surface": sum(1 for s in ss if s["stale_surface"]),
                            "stale_use_tau_gold": sum(1 for s in ss if s["stale_use_tau_gold"]), "successor_use": sum(1 for s in ss if s.get("successor_use")),
                            "n_supersession": sum(1 for s in ss if s.get("successor_use") is not None), "both": sum(1 for s in ss if s.get("both"))}
    for st in ("sup", "ret", "exp"):
        ss = [s for k, s in pn if byid[rows[k]["item_id"]]["state"] == st]
        d[f"pn_state_{st}"] = {"n": len(ss), "stale_use": sum(1 for s in ss if s["stale_use"]), "stale_use_tau_gold": sum(1 for s in ss if s["stale_use_tau_gold"])}
    d["present"] = {"n": len(pr), "correct": sum(1 for k, s in pr if s["correct"]), "correct_tau_hi": sum(1 for k, s in pr if s["correct_tau_hi"])}
    return d


_ST1 = {}


def _tag(it, policy):
    if not _ST1:
        _ST1.update(J(DS / "stage1.json")["per_item"])
    return {"tagged": bool(_ST1[it["item_id"]][policy]["tagged_reach"])}


def score_rows(path, sub, rec):
    byid = {it["item_id"]: it for it in sub}
    rows = {}
    for l in io.open(path, encoding="utf-8"):
        r = json.loads(l); rows[r["key"]] = r
    per_row = {}
    for key, r in rows.items():
        it = byid[r["item_id"]]
        if r["status"] != "OK" or rec.get(r["item_id"]) is None:
            per_row[key] = {"status": r["status"], "scored": False}; continue
        per_row[key] = {"status": "OK", "scored": True, **RD.score_answer(it, rec[r["item_id"]], r["answer"])}
    return rows, per_row, byid


def cmd_score():
    sys.stdout.reconfigure(encoding="utf-8")
    sub = DC.load_cell(); rec = RD.records(sub)
    rows_m, per_m, byid = score_rows(ROWS_MINI, sub, rec)
    lit = summarize(rows_m, per_m, byid, None, POLICY)
    lit["new_calls"] = sum(1 for r in rows_m.values() if r.get("source") == "amend2 call"); lit["recorded_reused"] = len(rows_m) - lit["new_calls"]
    S = {"registration_sha256": REG_SHA, "lock": J(RUN / "lock_amend2.json")["population"], "stage2_lit_mini": lit, "per_row_mini": per_m}
    if ROWS_H45.exists():
        rows_h, per_h, _ = score_rows(ROWS_H45, sub, rec)
        S["stage2_h45"] = {p: summarize(rows_h, per_h, byid, None, p) for p in POLICIES}
        S["per_row_h45"] = per_h
        S["h45_rows"] = {"n": len(rows_h), "failed": sum(1 for r in rows_h.values() if r["status"] != "OK"), "served": sorted({r.get("served_model") for r in rows_h.values()})}
    # the recorded mini rows per policy, reprinted from scores_ds.json for the side-by-side table
    ds = J(RUN / "scores_ds.json")
    S["mini_recorded"] = {p: ds["per_policy"][p] for p in STAGE2_POLICIES if p in ds.get("per_policy", {})}
    pr = probes()
    spend = {"probe_mini": pr.get("MINI", {}).get("usd", 0.0), "probe_h45": sum(x["usd"] for x in pr.get("H45", [])),
             "mini": sum(r.get("usd", 0.0) for r in rows_m.values()), "h45": (sum(r["usd"] for r in rows_h.values()) if ROWS_H45.exists() else 0.0)}
    spend["total"] = sum(spend.values()); S["spend"] = spend; S["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(S, RUN / "scores_amend2.json")
    txt = ledger_text(S)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


def fmt_row(name, d):
    a, t, u = d["pn_all"], d["pn_tagged"], d["pn_untagged"]; pres = d["present"]
    def frac(x, n):
        return f"{x} / {n} = {x / n:.4f}" if n else "—"
    return (f"| {name} | {d['pn_answered']} | {frac(a['stale_use'], a['n'])} | {frac(t['stale_use'], t['n'])} | {frac(u['stale_use'], u['n'])} | {a['stale_surface']} | "
            f"{frac(a['stale_use_tau_gold'], a['n'])} | {frac(t['stale_use_tau_gold'], t['n'])} | {frac(u['stale_use_tau_gold'], u['n'])} | "
            f"{frac(a['successor_use'], a['n_supersession'])} | {a['both']} | {pres['n']} | {frac(pres['correct'], pres['n'])} | {pres['correct_tau_hi']} |")


HEAD = ("| answerer, policy | PN reached ∧ answered | stale use (all) | stale use, tagged reach | stale use, untagged reach | stale surfacing | "
        "stale use at TAU_GOLD (all) | at TAU_GOLD, tagged | at TAU_GOLD, untagged | successor use (of supersession) | both | PRESENT answered | "
        "PRESENT correct (TAU_GOLD) | at TAU_HI |\n|---|---:|---|---|---|---:|---|---|---|---|---:|---:|---|---:|\n")


def ledger_text(S):
    lk = S["lock"]; sp = S["spend"]; lit = S["stage2_lit_mini"]
    L = ["\n### AUX-DS-A2-LOCK, AUX-DS-A2-POP, AUX-DS-A2-PROBE-MINI, AUX-DS-A2-PROBE-H45, AUX-DS-A2-PROJECTION\n",
         f"\nRegistration sha256 holds; prompts_ds digests as AUX-DS-PROMPT; prompts_e1 digests as pinned. Population (section A2.2 / A2.4, reproduced): "
         f"{lk['nominal']} nominal LOOKUP-LIT (item, view) pairs, {lk['reused']} reuse a recorded answer, {lk['new']} new calls ({lk['new_pn']} PN / {lk['new_present']} PRESENT); "
         f"Haiku 4.5 views {lk['h45_views']}.\n"]
    pr = probes(); pj = J(RUN / "projection_amend2.json")
    if "MINI" in pr:
        m = pr["MINI"]; L.append(f"Probe mini: served `{m['served']}` (identifier ok: {m['identifier_ok']}), {m['tok_in']} in / {m['tok_out']} out on a {m['view_lines']}-line view. ")
    if "H45" in pr:
        L.append("Probe Haiku 4.5: " + "; ".join(f"served `{x['served']}` ({x['tok_in']} in / {x['tok_out']} out, {x['view_lines']} lines)" for x in pr["H45"]) + ". ")
    L.append(f"Projection: mini {pj['mini']['new_calls']} calls ${pj['mini']['projected_usd']:.4f} (total against the $4 rule ${pj['mini']['total_against_rule']:.4f}); "
             f"Haiku 4.5 {pj['h45']['views']} calls ${pj['h45']['projected_usd']:.4f} (x1.3 ${pj['h45']['x1_3']:.4f} against the $5 line; runs: {pj['h45']['runs']}).\n")
    L.append("\n### AUX-DS-A2-STAGE2-LIT — Stage 2 for LOOKUP-LIT under GPT-4.1 mini (the §D.4 protocol; the AUX-DS-STAGE2 columns)\n\n")
    L.append(f"{lit['new_calls']} new calls, {lit['recorded_reused']} recorded answers reused; failures {lit['failed']}; PN abstained 0 (the rule never abstains).\n\n")
    L.append(HEAD + fmt_row("GPT-4.1 mini, LOOKUP-LIT", lit) + "\n")
    L.append("\nPer state (stale use at TAU_HI / at TAU_GOLD / answered): " + "; ".join(f"{st} {lit[f'pn_state_{st}']['stale_use']} / {lit[f'pn_state_{st}']['stale_use_tau_gold']} / {lit[f'pn_state_{st}']['n']}" for st in ("sup", "ret", "exp")) + ".\n")
    if "stage2_h45" in S:
        h = S["stage2_h45"]; hr = S["h45_rows"]
        L.append(f"\n### AUX-DS-A2-STAGE2-H45 — Stage 2 under Claude Haiku 4.5, every policy (rows {hr['n']}, failed {hr['failed']}, served {hr['served']}; temperature 0, max_tokens 200, k = 1)\n\n")
        L.append(HEAD + "\n".join(fmt_row(f"Haiku 4.5, {p}", h[p]) for p in POLICIES) + "\n")
        L.append("\nPer state under Haiku 4.5 (stale use at TAU_HI / at TAU_GOLD / answered): " + " · ".join(
            f"{p}: " + ", ".join(f"{st} {h[p][f'pn_state_{st}']['stale_use']} / {h[p][f'pn_state_{st}']['stale_use_tau_gold']} / {h[p][f'pn_state_{st}']['n']}" for st in ("sup", "ret", "exp")) for p in POLICIES) + ".\n")
    L.append(f"\n### AUX-DS-A2-SPEND\n\nProbe mini ${sp['probe_mini']:.4f}; probe Haiku ${sp['probe_h45']:.4f}; mini lane ${sp['mini']:.4f}; Haiku lane ${sp['h45']:.4f}; "
             f"**total ${sp['total']:.4f}** (the Haiku lane against the author's $5 line; the mini lane under the DS $4 rule).\n")
    return "".join(L)


if __name__ == "__main__":
    {"lock": cmd_lock, "probe-mini": cmd_probe_mini, "probe-h45": cmd_probe_h45, "project": cmd_project,
     "stage2-mini": cmd_stage2_mini, "stage2-h45": cmd_stage2_h45, "score": cmd_score}[sys.argv[1]]()
