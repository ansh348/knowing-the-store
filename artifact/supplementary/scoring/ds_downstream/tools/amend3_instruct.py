"""amend3_instruct.py -- ADDENDUM_DS Amendment 3 (registrations/ADDENDUM_DS_AMENDMENT_3.md, frozen by sha256 before the
first call; program R107, 2026-09-14): the answer stage once more, with one added instruction to treat records tagged
superseded, retracted or expired as not to be used, GPT-4.1 mini and Claude Haiku 4.5 on the same 452 distinct views as
Amendment 2's Haiku lane. Descriptive: no bar, no prediction, no verdict.

MODEL CALLS: Lane 1 -- gpt-4.1-mini (temperature 0, seed 42, max_tokens 200, JSON mode, one retry), 452 calls, cache
ds_downstream/cache_amend3/ (a new prompt; nothing recorded is reused). Lane 2 -- claude-haiku-4-5-20251001, temperature 0,
max_tokens 200, k = 1, synchronous, the answer read from the last JSON object of the reply with one retry. Both lanes
together under the author's $2.00 line. Nothing registered is written.

Subcommands, in order:
  lock          registration sha256, prompt digests (SYSTEM_ANSWER_A3, USER_ANSWER), population 452 -> run/lock_amend3.json
  probe-mini    one gpt-4.1-mini call (served identifier, tokens)                            -> run/probes_amend3.json
  probe-h45     one Haiku 4.5 call (served identifier, tokens)                               -> run/probes_amend3.json
  project       both lanes against the $2 line (x1.3)                                        -> run/projection_amend3.json
  run-mini      Lane 1 -> run/rows_ds_amend3_mini.jsonl
  run-h45       Lane 2 -> run/rows_ds_amend3_h45.jsonl
  score         the committed detector; NUMBERS_DS.md section 8 (AUX-DS-A3-*)                -> run/scores_amend3.json
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import datetime as dt
import hashlib
import io
import json
import sys
import threading
import time

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import ds_common as DC                                                       # noqa: E402
from ds_common import ROOT, DS, RUN, J, jdump, POLICIES                     # noqa: E402
import run_ds as RD                                                          # noqa: E402
import prompts_ds as PD                                                      # noqa: E402
import prompts_e1 as P                                                       # noqa: E402
import amend2_lit as A2                                                      # noqa: E402

sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
from run_cf import last_json                                                 # noqa: E402

api = DC.RC.e1_api()
REG = ROOT / "registrations" / "ADDENDUM_DS_AMENDMENT_3.md"
REG_SHA = "eca19607629c03d122f0e0ac66c50c3068978dcecd3be35296191aa3e2f3bce1"
CACHE3 = DS / "cache_amend3"
LINE = 2.00
LANE_MINI, PRICE_MINI = RD.LANE, RD.PRICE
LANE_H45, PRICE_H45 = A2.LANE_H45, A2.PRICE_H45
ROWS_MINI = RUN / "rows_ds_amend3_mini.jsonl"
ROWS_H45 = RUN / "rows_ds_amend3_h45.jsonl"
LEDGER = DS / "NUMBERS_DS.md"
ARM = "ANSWER-A3"
N_VIEWS = 452

ADDED = ("Treat every entry tagged superseded, retracted or expired as not to be used: do not draw on it for the answer and do not "
         "report it as the user's current situation. If the only entries that bear on the question carry one of those tags, say that "
         "the store does not currently contain the answer.")
TAIL = "Return JSON only: {\"answer\": \"<your answer>\"}"
assert PD.SYSTEM_ANSWER.endswith(TAIL)
SYSTEM_ANSWER_A3 = PD.SYSTEM_ANSWER[:-len(TAIL)] + ADDED + "\n\n" + TAIL


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def registered_added():
    """The added paragraph as the frozen registration prints it (the fenced block of section A3.2)."""
    s = REG.read_text(encoding="utf-8")
    i = s.index("verbatim:\n\n```\n") + len("verbatim:\n\n```\n"); j = s.index("\n```\n", i)
    return s[i:j]


def assert_lineage():
    h = hashlib.sha256(REG.read_bytes()).hexdigest()
    assert h == REG_SHA, f"ADDENDUM_DS_AMENDMENT_3.md sha256 {h} != frozen -- STOP"
    assert registered_added() == ADDED, "the added instruction differs from the frozen section A3.2 -- STOP"
    RD.assert_lineage()


def redirect():
    CACHE3.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                             # noqa: SLF001
    e0.CACHE_PATH = CACHE3 / "responses.json"; e0.LEDGER_PATH = CACHE3 / "cost_ledger.json"
    e0._cache = None; e0._load_cache()                                       # noqa: SLF001
    e0.HARD_CAP_USD = LINE
    return e0


def messages(job):
    return [{"role": "system", "content": SYSTEM_ANSWER_A3}, {"role": "user", "content": PD.USER_ANSWER.format(view=job["view"], question=job["question"])}]


def jobs():
    sub, hj = A2.h45_jobs()
    assert len(hj) == N_VIEWS, len(hj)
    return sub, hj


def cmd_lock():
    assert_lineage()
    sub, hj = jobs()
    out = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "system_answer_a3_sha256": sha(SYSTEM_ANSWER_A3),
           "added_paragraph_sha256": sha(ADDED), "prompts_ds": PD.digests(), "prompts_e1": {"file": P.file_sha256(), "texts": P.texts_sha256()},
           "population": len(hj), "expected": N_VIEWS, "pn": sum(1 for j in hj if j["label"] == "PRESENT-NEGATIVE"),
           "present": sum(1 for j in hj if j["label"] == "PRESENT"), "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RUN / "lock_amend3.json"); print(json.dumps(out, indent=1))


def probes():
    p = RUN / "probes_amend3.json"
    return J(p) if p.exists() else {}


def cmd_probe_mini():
    assert_lineage(); e0 = redirect(); sub, hj = jobs()
    first = next(j for j in hj if j["label"] == "PRESENT-NEGATIVE" and j["n_lines"] > 5)
    r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,   # noqa: SLF001
                                             messages=messages(first), response_format={"type": "json_object"})
    o = api.parse_json(r.choices[0].message.content) or {}
    rec = {"item_id": first["item_id"], "view_lines": first["n_lines"], "served": r.model, "identifier_ok": LANE_MINI in r.model,
           "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens,
           "usd": r.usage.prompt_tokens / 1e6 * PRICE_MINI[0] + r.usage.completion_tokens / 1e6 * PRICE_MINI[1],
           "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL", "sample": (r.choices[0].message.content or "")[:300],
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    out = probes(); out["MINI"] = rec; jdump(out, RUN / "probes_amend3.json"); print(json.dumps(rec, indent=1))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def h45_once(client, job):
    msgs = messages(job)
    r = client.messages.create(model=LANE_H45, max_tokens=200, temperature=0.0, system=msgs[0]["content"],
                               messages=[{"role": "user", "content": msgs[1]["content"]}])
    text = "".join(b.text for b in r.content if b.type == "text")
    return text, r.usage.input_tokens, r.usage.output_tokens, r.model


def cmd_probe_h45():
    assert_lineage(); sub, hj = jobs()
    first = next(j for j in hj if j["label"] == "PRESENT-NEGATIVE" and j["n_lines"] > 5)
    cl = A2.anthropic_client()
    text, tin, tout, served = h45_once(cl, first); o = last_json(text) or {}
    rec = {"item_id": first["item_id"], "view_lines": first["n_lines"], "served": served, "identifier_ok": served == LANE_H45, "tok_in": tin, "tok_out": tout,
           "usd": tin / 1e6 * PRICE_H45[0] + tout / 1e6 * PRICE_H45[1], "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL",
           "sample": text[:300], "when": dt.datetime.now().isoformat(timespec="seconds")}
    out = probes(); out["H45"] = rec; jdump(out, RUN / "probes_amend3.json"); print(json.dumps(rec, indent=1))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def cmd_project():
    pr = probes(); sub, hj = jobs(); per_line = 45.0
    out = {"views": len(hj), "line": LINE}
    for code, price in (("MINI", PRICE_MINI), ("H45", PRICE_H45)):
        x = pr[code]; shell = max(50.0, x["tok_in"] - per_line * x["view_lines"])
        tin = sum(shell + per_line * j["n_lines"] for j in hj); tout = x["tok_out"] * len(hj)
        out[code] = {"projected_usd": tin / 1e6 * price[0] + tout / 1e6 * price[1], "probe_usd": x["usd"]}
    out["sum"] = out["MINI"]["projected_usd"] + out["H45"]["projected_usd"] + out["MINI"]["probe_usd"] + out["H45"]["probe_usd"]
    out["sum_x1_3"] = 1.3 * out["sum"]; out["runs"] = out["sum_x1_3"] < LINE; out["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(out, RUN / "projection_amend3.json"); print(json.dumps(out, indent=1))
    if not out["runs"]:
        sys.exit("PROJECTION x1.3 AT OR ABOVE THE $2 LINE -- STOP")


def spent(path):
    return sum(json.loads(l).get("usd", 0.0) for l in io.open(path, encoding="utf-8")) if path.exists() else 0.0


def cmd_run_mini():
    assert_lineage(); redirect(); sub, hj = jobs()
    assert J(RUN / "projection_amend3.json")["runs"]
    have = {json.loads(l)["key"] for l in io.open(ROWS_MINI, encoding="utf-8")} if ROWS_MINI.exists() else set()
    todo = [j for j in hj if j["key"] not in have]
    print(f"{len(todo)} mini calls to go (resumed past {len(have)})", flush=True)
    lock = threading.Lock(); spend = [spent(ROWS_MINI) + spent(ROWS_H45)]; stopped = [False]

    def work(job):
        with lock:
            if spend[0] >= LINE or stopped[0]:
                stopped[0] = True; return None
        msgs = messages(job)
        ok = lambda o: o is not None and isinstance(o.get("answer"), str)
        r = api.call(job["key"], ARM, msgs); o = api.parse_json(r["content"]); n_calls, failed = 1, False
        usd = 0.0 if r["cached"] else r["prompt_tokens"] / 1e6 * PRICE_MINI[0] + r["completion_tokens"] / 1e6 * PRICE_MINI[1]
        if not ok(o):
            r2 = api.call(job["key"], ARM + "#retry", msgs); o = api.parse_json(r2["content"]); n_calls = 2
            usd += 0.0 if r2["cached"] else r2["prompt_tokens"] / 1e6 * PRICE_MINI[0] + r2["completion_tokens"] / 1e6 * PRICE_MINI[1]
            r = r2
            if not ok(o):
                failed, o = True, {}
        rec = {**{k: job[k] for k in ("key", "item_id", "persona", "question", "label", "state", "view_sha", "n_lines", "policies")},
               "answer": (o.get("answer") if not failed else None), "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls,
               "model": LANE_MINI, "cached": r["cached"], "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "usd": usd,
               "raw": (r["content"] or "")[:400], "source": "amend3 call"}
        with lock:
            spend[0] += usd
            with io.open(ROWS_MINI, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, sort_keys=True, ensure_ascii=False) + "\n")
        return rec
    try:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            out = [r for r in ex.map(work, todo) if r is not None]
    finally:
        api.flush()
    c = collections.Counter(r["status"] for r in out)
    print(f"DONE {len(out)} rows; status {dict(c)}; billed this step ${sum(r['usd'] for r in out):.4f}; amendment total ${spend[0]:.4f} against ${LINE:.2f}" + ("  >>> STOPPED AT THE LINE" if stopped[0] else ""))
    if stopped[0]:
        sys.exit(1)


def cmd_run_h45():
    assert_lineage(); sub, hj = jobs()
    assert J(RUN / "projection_amend3.json")["runs"]
    have = {json.loads(l)["key"] for l in io.open(ROWS_H45, encoding="utf-8")} if ROWS_H45.exists() else set()
    todo = [j for j in hj if j["key"] not in have]
    print(f"{len(todo)} Haiku calls to go (resumed past {len(have)})", flush=True)
    cl = A2.anthropic_client(); lock = threading.Lock(); spend = [spent(ROWS_MINI) + spent(ROWS_H45)]; stopped = [False]

    def work(job):
        with lock:
            if spend[0] >= LINE or stopped[0]:
                stopped[0] = True; return None
        n_calls, failed, usd, text, served, tin, tout, o = 0, False, 0.0, "", None, 0, 0, {}
        for attempt in range(2):
            for backoff in range(4):
                try:
                    text, tin_, tout_, served = h45_once(cl, job); break
                except Exception:                                      # noqa: BLE001
                    if backoff == 3:
                        raise
                    time.sleep(2 ** backoff)
            n_calls += 1; usd += tin_ / 1e6 * PRICE_H45[0] + tout_ / 1e6 * PRICE_H45[1]; tin, tout = tin_, tout_
            o = last_json(text) or {}
            if isinstance(o.get("answer"), str):
                break
        else:
            failed = True
        rec = {**{k: job[k] for k in ("key", "item_id", "persona", "question", "label", "state", "view_sha", "n_lines", "policies")},
               "answer": (o.get("answer") if not failed else None), "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls,
               "model": LANE_H45, "served_model": served, "cached": False, "tok_in": tin, "tok_out": tout, "usd": usd, "raw": (text or "")[:400], "source": "amend3 call"}
        with lock:
            spend[0] += usd
            with io.open(ROWS_H45, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, sort_keys=True, ensure_ascii=False) + "\n")
        return rec
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        out = [r for r in ex.map(work, todo) if r is not None]
    c = collections.Counter(r["status"] for r in out)
    print(f"DONE {len(out)} rows; status {dict(c)}; billed this step ${sum(r['usd'] for r in out):.4f}; amendment total ${spend[0]:.4f} against ${LINE:.2f}" + ("  >>> STOPPED AT THE LINE" if stopped[0] else ""))
    if stopped[0]:
        sys.exit(1)


def cmd_score():
    sys.stdout.reconfigure(encoding="utf-8")
    sub = DC.load_cell(); rec = RD.records(sub)
    S = {"registration_sha256": REG_SHA, "lock": J(RUN / "lock_amend3.json"), "stage2": {}, "per_row": {}}
    for code, path in (("MINI", ROWS_MINI), ("H45", ROWS_H45)):
        rows, per, byid = A2.score_rows(path, sub, rec)
        S["stage2"][code] = {p: A2.summarize(rows, per, byid, None, p) for p in POLICIES}
        S["per_row"][code] = per
        S["stage2"][code]["_rows"] = {"n": len(rows), "failed": sum(1 for r in rows.values() if r["status"] != "OK"), "served": sorted({r.get("served_model") or r.get("model") for r in rows.values()})}
    pr = probes()
    spend = {"probe_mini": pr["MINI"]["usd"], "probe_h45": pr["H45"]["usd"], "mini": spent(ROWS_MINI), "h45": spent(ROWS_H45)}
    spend["total"] = sum(spend.values()); S["spend"] = spend; S["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(S, RUN / "scores_amend3.json")
    txt = ledger_text(S)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


def ledger_text(S):
    lk = S["lock"]; sp = S["spend"]; pr = probes(); pj = J(RUN / "projection_amend3.json")
    L = ["\n### AUX-DS-A3-LOCK, AUX-DS-A3-PROMPT, AUX-DS-A3-POP, AUX-DS-A3-PROBE-MINI, AUX-DS-A3-PROBE-H45, AUX-DS-A3-PROJECTION\n",
         f"\nRegistration sha256 holds; `SYSTEM_ANSWER_A3` sha256 `{lk['system_answer_a3_sha256']}` (the D.4 system text with the added paragraph, sha256 `{lk['added_paragraph_sha256']}`, "
         f"verbatim from section A3.2); `USER_ANSWER` as AUX-DS-PROMPT; prompts_e1 digests as pinned. Population {lk['population']} distinct (item, view) pairs "
         f"({lk['pn']} PN, {lk['present']} PRESENT), the 452 of Amendment 2's Haiku lane. Probe mini: served `{pr['MINI']['served']}` ({pr['MINI']['tok_in']} in / {pr['MINI']['tok_out']} out); "
         f"probe Haiku 4.5: served `{pr['H45']['served']}` ({pr['H45']['tok_in']} in / {pr['H45']['tok_out']} out). Projection: mini ${pj['MINI']['projected_usd']:.4f}, "
         f"Haiku ${pj['H45']['projected_usd']:.4f}, sum with probes ${pj['sum']:.4f} (x1.3 ${pj['sum_x1_3']:.4f}) against the $2.00 line; runs: {pj['runs']}.\n"]
    for code, name, key in (("MINI", "GPT-4.1 mini", "AUX-DS-A3-STAGE2-MINI"), ("H45", "Claude Haiku 4.5", "AUX-DS-A3-STAGE2-H45")):
        h = S["stage2"][code]; rr = h["_rows"]
        L.append(f"\n### {key} — Stage 2 under {name} with the added instruction, every policy (rows {rr['n']}, failed {rr['failed']}, served {rr['served']}; temperature 0, k = 1)\n\n")
        L.append(A2.HEAD + "\n".join(A2.fmt_row(f"{name} + instruction, {p}", h[p]) for p in POLICIES) + "\n")
        L.append(f"\nPer state under {name} + instruction (stale use at TAU_HI / at TAU_GOLD / answered): " + " · ".join(
            f"{p}: " + ", ".join(f"{st} {h[p][f'pn_state_{st}']['stale_use']} / {h[p][f'pn_state_{st}']['stale_use_tau_gold']} / {h[p][f'pn_state_{st}']['n']}" for st in ("sup", "ret", "exp")) for p in POLICIES) + ".\n")
    L.append(f"\n### AUX-DS-A3-SPEND\n\nProbe mini ${sp['probe_mini']:.4f}; probe Haiku ${sp['probe_h45']:.4f}; mini lane ${sp['mini']:.4f}; Haiku lane ${sp['h45']:.4f}; "
             f"**total ${sp['total']:.4f}** against the author's $2.00 line.\n")
    return "".join(L)


if __name__ == "__main__":
    {"lock": cmd_lock, "probe-mini": cmd_probe_mini, "probe-h45": cmd_probe_h45, "project": cmd_project,
     "run-mini": cmd_run_mini, "run-h45": cmd_run_h45, "score": cmd_score}[sys.argv[1]]()
