# -*- coding: utf-8 -*-
"""amend5_tagdup.py -- ADDENDUM_DS Amendment 5 (registrations/ADDENDUM_DS_AMENDMENT_5.md, frozen at 54f4ade; registered text
sha256 a820195f... over the bytes above the marker): the active duplicates tagged from the manifest, the store otherwise untouched,
the answer stage re-run with GPT-4.1 mini and Claude Haiku 4.5 on every view that changes, under the Amendment 4 header.
Descriptive: no prediction, no bar, no verdict.

Written from amend4_header.py, which is imported for the header, the prompt, the persona fields, the lanes' call helpers, the
detector-side helpers (view_source, first_sentence, is_abst) and the paired bootstrap; nothing there is edited.

Subcommands, in order:
  lock          registration sha256 (frozen bytes), the Amendment 4 header sha256 against AUX-DS-A4-LOCK, the prompt digests; the
                rewrite of every view with an active duplicate line (the item's own committed detector at TAU_GOLD on the line's
                text; the tag is the obligation's state, superseded or retracted); the RENDERER LOCK per view; the changed ranks
                against the audit's step4b_view_lines.json; the population counts (452; 74 changed; 35 items; 124 lines in the 70)
                -> run/lock_amend5.json, run/views_amend5.json; NUMBERS_DS.md section 11 opened with AUX-DS-A5-REG
  probe-mini    one gpt-4.1-mini call on the first changed view (served identifier, tokens)               -> run/probes_amend5.json
  probe-h45     one Haiku 4.5 call on the first changed view                                                -> run/probes_amend5.json
  project       both lanes over the 74 changed views against the $2 cap (x1.3)                             -> run/projection_amend5.json
  run-mini      Lane 1 on the 74 changed views -> run/rows_ds_amend5_mini.jsonl (cache ds_downstream/cache_amend5/)
  run-h45       Lane 2 on the 74 changed views -> run/rows_ds_amend5_h45.jsonl
  score         the committed detector on the 452 (74 new answers + 378 Amendment 4 rows carried), per policy beside the
                Amendment 4 rows; the 74 before / after with transitions and both bootstrap intervals; the source split; TAU_HI;
                abstentions; spend; NUMBERS_DS.md section 11 (AUX-DS-A5-*)                                 -> run/scores_amend5.json
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import datetime as dt
import hashlib
import io
import json
import re
import shutil
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
import amend4_header as A4                                                   # noqa: E402
from e0_common import toks, cov, MIN_SHARED, CROSS_GUARD, TAU_GOLD           # noqa: E402
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
from run_cf import last_json                                                 # noqa: E402

api = A4.api
REG = ROOT / "registrations" / "ADDENDUM_DS_AMENDMENT_5.md"
REG_SHA = "a820195f93ffdf5b1d25c336b81bfcc59afaa27d67c5fd28ae1e97d9ae41e7a0"
FROZEN_AT = "54f4ade"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
CACHE5 = DS / "cache_amend5"
LINE = 2.00
LANE_MINI, PRICE_MINI = A4.LANE_MINI, A4.PRICE_MINI
LANE_H45, PRICE_H45 = A4.LANE_H45, A4.PRICE_H45
ROWS_MINI = RUN / "rows_ds_amend5_mini.jsonl"
ROWS_H45 = RUN / "rows_ds_amend5_h45.jsonl"
LEDGER = DS / "NUMBERS_DS.md"
ARM = "ANSWER-A5"
EXPECT = {"views": 452, "changed": 74, "items": 35, "changed_in_422": 70, "lines_in_422": 124, "changed_lit": 4}
TAG = {"sup": "superseded", "ret": "retracted"}
AUDIT = ROOT / "reviews" / "downstream_audit" / "step4b_view_lines.json"


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def registration_ok():
    b = REG.read_bytes(); i = b.find(FROZEN_END)
    return i > 0 and hashlib.sha256(b[:i]).hexdigest() == REG_SHA


def assert_lineage(before_call=True):
    assert registration_ok(), "ADDENDUM_DS_AMENDMENT_5.md frozen bytes sha256 != a820195f -- STOP"
    lk4 = J(RUN / "lock_amend4.json")
    assert sha(A4.USER_ANSWER_A4) == lk4["user_answer_a4_sha256"] and sha(A4.HEADER) == lk4["header_sha256"], "the Amendment 4 header differs from AUX-DS-A4-LOCK -- STOP"
    assert PD.digests() == lk4["prompts_ds"], "prompts_ds digests differ from Amendment 4's lock -- STOP"
    assert P.file_sha256() == lk4["prompts_e1"]["file"] and P.texts_sha256() == lk4["prompts_e1"]["texts"], "prompts_e1 digests differ -- STOP"
    if before_call:
        assert "AUX-DS-A5-REG" in LEDGER.read_text(encoding="utf-8"), "AUX-DS-A5-REG absent from NUMBERS_DS.md -- STOP (no call before the freeze is recorded)"
    A4.RD.assert_lineage()


def redirect():
    CACHE5.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                             # noqa: SLF001
    e0.CACHE_PATH = CACHE5 / "responses.json"; e0.LEDGER_PATH = CACHE5 / "cost_ledger.json"
    e0._cache = None; e0._load_cache()                                       # noqa: SLF001
    e0.HARD_CAP_USD = LINE
    return e0


# ------------------------------------------------------------------ the rewrite
def duplicate_ranks(view_text, rec):
    """Ranks of the ACTIVE lines whose text asserts the stale value by the item's own detector at TAU_GOLD (amend4_header.view_source's test)."""
    if rec is None or rec["section"] == "expiring_logistics" or not rec.get("stale_field"):
        return []
    drop = rec["drop"]; ot, nt = toks(rec["stale_field"], drop), toks(rec["gold_field"], drop); do, dn = ot - nt, nt - ot
    out = []
    for ln in view_text.split("\n"):
        m = A4.LINE_RE.match(ln)
        if not m or m.group(2) != "active":
            continue
        A = toks(m.group(6), drop)
        if len(do & A) >= MIN_SHARED and cov(dn, A) < CROSS_GUARD and cov(do, A) >= TAU_GOLD:
            out.append(int(m.group(1)))
    return out


def rewrite(view_text, ranks, tag):
    lines = view_text.split("\n"); out = []
    for ln in lines:
        m = A4.LINE_RE.match(ln)
        if m and int(m.group(1)) in ranks:
            assert m.group(2) == "active"
            ln = f"[{m.group(1)}] lifecycle: {tag} | category: {m.group(3)} | attribute: {m.group(4)} | age: {m.group(5)} | text: {m.group(6)}"
        out.append(ln)
    new = "\n".join(out)
    # RENDERER LOCK: same line count; every differing line differs only in the lifecycle field, from active to the tag
    a, c = lines, new.split("\n"); assert len(a) == len(c)
    for x, y_ in zip(a, c):
        if x != y_:
            mx, my = A4.LINE_RE.match(x), A4.LINE_RE.match(y_)
            assert mx and my and mx.group(2) == "active" and my.group(2) == tag and all(mx.group(k) == my.group(k) for k in (1, 3, 4, 5, 6)), "lock: a field outside the lifecycle tag differs"
    return new


def changed_views():
    """The 452 jobs; for each that changes, the new view, its sha and key, the ranks, the tag; asserted against the audit."""
    sub, hj = A4.jobs(); rec = RD.records(sub); audit = J(AUDIT)["view_lines"]
    cell_keys = {j["key"] for j in J(RUN / "cell_ds.json")["jobs"]}
    ch = {}
    for j in hj:
        if j["label"] != "PRESENT-NEGATIVE" or j["state"] not in TAG:
            continue
        ranks = duplicate_ranks(j["view"], rec.get(j["item_id"]))
        for pol in j["policies"]:
            ref = audit.get(f"{j['item_id']}|{pol}")
            assert ref is not None and sorted(ref["active_stale"]) == sorted(ranks), ("lock: ranks differ from the audit", j["key"], pol, ranks, ref and ref["active_stale"])
        if not ranks:
            continue
        new = rewrite(j["view"], set(ranks), TAG[j["state"]]); ns = sha(new)[:16]
        ch[j["key"]] = {"item_id": j["item_id"], "persona": j["persona"], "question": j["question"], "label": j["label"], "state": j["state"], "policies": j["policies"],
                        "n_lines": j["n_lines"], "view_sha_a4": j["view_sha"], "key_a4": j["key"], "view": new, "view_sha": ns, "key": f"{j['item_id']}|{ns}",
                        "ranks_tagged": sorted(ranks), "tag": TAG[j["state"]], "in_422": j["key"] in cell_keys}
    return sub, hj, ch


def new_jobs():
    return list(J(RUN / "views_amend5.json")["changed"].values())


# ------------------------------------------------------------------ lock / probe / project
def cmd_lock():
    assert_lineage(before_call=False)
    sub, hj, ch = changed_views()
    got = {"views": len(hj), "changed": len(ch), "items": len({c["item_id"] for c in ch.values()}), "changed_in_422": sum(1 for c in ch.values() if c["in_422"]),
           "lines_in_422": sum(len(c["ranks_tagged"]) for c in ch.values() if c["in_422"]), "changed_lit": sum(1 for c in ch.values() if not c["in_422"])}
    ok = all(got[k] == v for k, v in EXPECT.items())
    by_state = collections.Counter(c["state"] for c in ch.values()); by_pol = collections.Counter(p for c in ch.values() for p in c["policies"])
    out = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "header_sha256": sha(A4.HEADER), "user_answer_a4_sha256": sha(A4.USER_ANSWER_A4),
           "prompts_ds": PD.digests(), "counts": got, "expected": EXPECT, "counts_ok": ok, "changed_by_state": dict(by_state), "changed_by_policy": dict(by_pol),
           "lines_tagged_total": sum(len(c["ranks_tagged"]) for c in ch.values()), "renderer_lock": "asserted on every changed view; unchanged views byte-identical (not re-run)",
           "detector_rule": "an active line whose text asserts the item's stale value by the item's own committed detector at TAU_GOLD (old-only coverage >= 0.50 with >= 2 shared tokens, new-only coverage < 0.34)",
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RUN / "lock_amend5.json"); jdump({"changed": ch}, RUN / "views_amend5.json")
    print(json.dumps({k: v for k, v in out.items()}, indent=1))
    if not ok:
        sys.exit("POPULATION COUNTS DO NOT REPRODUCE -- STOP")
    txt = LEDGER.read_text(encoding="utf-8")
    if "AUX-DS-A5-REG" not in txt:
        with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
            f.write(f"\n## 11. DS Amendment 5: the active duplicates tagged from the manifest (registrations/ADDENDUM_DS_AMENDMENT_5.md; descriptive)\n\n"
                    f"### AUX-DS-A5-REG\n\nRegistered text sha256 **`{REG_SHA}`** (the bytes above the marker line), frozen at `{FROZEN_AT}` on 2026-09-14, recorded here before the first call. "
                    f"Descriptive: no prediction, no bar, no verdict. Runner `tools/amend5_tagdup.py`.\n")
    print("section 11 opened with AUX-DS-A5-REG")


def probes():
    p = RUN / "probes_amend5.json"
    return J(p) if p.exists() else {}


def cmd_probe_mini():
    assert_lineage(); e0 = redirect(); first = new_jobs()[0]
    r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,   # noqa: SLF001
                                             messages=A4.messages(first), response_format={"type": "json_object"})
    o = api.parse_json(r.choices[0].message.content) or {}
    rec = {"item_id": first["item_id"], "view_lines": first["n_lines"], "served": r.model, "identifier_ok": LANE_MINI in r.model, "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens,
           "usd": r.usage.prompt_tokens / 1e6 * PRICE_MINI[0] + r.usage.completion_tokens / 1e6 * PRICE_MINI[1], "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL",
           "sample": (r.choices[0].message.content or "")[:300], "when": dt.datetime.now().isoformat(timespec="seconds")}
    out = probes(); out["MINI"] = rec; jdump(out, RUN / "probes_amend5.json"); print(json.dumps(rec, indent=1, ensure_ascii=False))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def cmd_probe_h45():
    assert_lineage(); first = new_jobs()[0]; cl = A2.anthropic_client()
    text, tin, tout, served = A4.h45_once(cl, first); o = last_json(text) or {}
    rec = {"item_id": first["item_id"], "view_lines": first["n_lines"], "served": served, "identifier_ok": served == LANE_H45, "tok_in": tin, "tok_out": tout,
           "usd": tin / 1e6 * PRICE_H45[0] + tout / 1e6 * PRICE_H45[1], "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL", "sample": text[:300],
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    out = probes(); out["H45"] = rec; jdump(out, RUN / "probes_amend5.json"); print(json.dumps(rec, indent=1, ensure_ascii=False))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def cmd_project():
    pr = probes(); hj = new_jobs(); per_line = 45.0
    out = {"views": len(hj), "line": LINE}
    for code, price in (("MINI", PRICE_MINI), ("H45", PRICE_H45)):
        x = pr[code]; shell = max(50.0, x["tok_in"] - per_line * x["view_lines"])
        tin = sum(shell + per_line * j["n_lines"] for j in hj); tout = x["tok_out"] * len(hj)
        out[code] = {"projected_usd": tin / 1e6 * price[0] + tout / 1e6 * price[1], "probe_usd": x["usd"]}
    out["sum"] = out["MINI"]["projected_usd"] + out["H45"]["projected_usd"] + out["MINI"]["probe_usd"] + out["H45"]["probe_usd"]
    out["sum_x1_3"] = 1.3 * out["sum"]; out["runs"] = out["sum_x1_3"] < LINE; out["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(out, RUN / "projection_amend5.json"); print(json.dumps(out, indent=1))
    if not out["runs"]:
        sys.exit("PROJECTION x1.3 AT OR ABOVE THE $2 CAP -- STOP")


def spent(path):
    return sum(json.loads(l).get("usd", 0.0) for l in io.open(path, encoding="utf-8")) if path.exists() else 0.0


# ------------------------------------------------------------------ run
def row_fields(job):
    return {k: job[k] for k in ("key", "item_id", "persona", "question", "label", "state", "view_sha", "n_lines", "policies", "key_a4", "view_sha_a4", "ranks_tagged", "tag")}


def cmd_run_mini():
    assert_lineage(); redirect(); hj = new_jobs()
    assert J(RUN / "projection_amend5.json")["runs"]
    have = {json.loads(l)["key"] for l in io.open(ROWS_MINI, encoding="utf-8")} if ROWS_MINI.exists() else set()
    todo = [j for j in hj if j["key"] not in have]
    print(f"{len(todo)} mini calls to go (resumed past {len(have)})", flush=True)
    lock = threading.Lock(); spend = [spent(ROWS_MINI) + spent(ROWS_H45)]; stopped = [False]

    def work(job):
        with lock:
            if spend[0] >= LINE or stopped[0]:
                stopped[0] = True; return None
        msgs = A4.messages(job)
        ok = lambda o: o is not None and isinstance(o.get("answer"), str)     # noqa: E731
        r = api.call(job["key"], ARM, msgs); o = api.parse_json(r["content"]); n_calls, failed = 1, False
        usd = 0.0 if r["cached"] else r["prompt_tokens"] / 1e6 * PRICE_MINI[0] + r["completion_tokens"] / 1e6 * PRICE_MINI[1]
        if not ok(o):
            r2 = api.call(job["key"], ARM + "#retry", msgs); o = api.parse_json(r2["content"]); n_calls = 2
            usd += 0.0 if r2["cached"] else r2["prompt_tokens"] / 1e6 * PRICE_MINI[0] + r2["completion_tokens"] / 1e6 * PRICE_MINI[1]
            r = r2
            if not ok(o):
                failed, o = True, {}
        rec = {**row_fields(job), "answer": (o.get("answer") if not failed else None), "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls,
               "model": LANE_MINI, "cached": r["cached"], "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "usd": usd, "raw": (r["content"] or "")[:400], "source": "amend5 call"}
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
    print(f"DONE {len(out)} rows; status {dict(c)}; billed this step ${sum(r['usd'] for r in out):.4f}; amendment total ${spend[0]:.4f} against ${LINE:.2f}" + ("  >>> STOPPED AT THE CAP" if stopped[0] else ""))
    if stopped[0]:
        sys.exit(1)


def cmd_run_h45():
    assert_lineage(); hj = new_jobs()
    assert J(RUN / "projection_amend5.json")["runs"]
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
                    text, tin_, tout_, served = A4.h45_once(cl, job); break
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
        rec = {**row_fields(job), "answer": (o.get("answer") if not failed else None), "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls,
               "model": LANE_H45, "served_model": served, "cached": False, "tok_in": tin, "tok_out": tout, "usd": usd, "raw": (text or "")[:400], "source": "amend5 call"}
        with lock:
            spend[0] += usd
            with io.open(ROWS_H45, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, sort_keys=True, ensure_ascii=False) + "\n")
        return rec
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        out = [r for r in ex.map(work, todo) if r is not None]
    c = collections.Counter(r["status"] for r in out)
    print(f"DONE {len(out)} rows; status {dict(c)}; billed this step ${sum(r['usd'] for r in out):.4f}; amendment total ${spend[0]:.4f} against ${LINE:.2f}" + ("  >>> STOPPED AT THE CAP" if stopped[0] else ""))
    if stopped[0]:
        sys.exit(1)


# ------------------------------------------------------------------ score
def merged_rows(code, new_path):
    """The 452 rows: Amendment 4's recorded row for every unchanged view, the Amendment 5 row for every changed view (under its A4 key,
    so the per-policy summaries add up over the same 452 keys)."""
    a4 = {json.loads(l)["key"]: json.loads(l) for l in io.open(RUN / f"rows_ds_amend4_{'mini' if code == 'MINI' else 'h45'}.jsonl", encoding="utf-8")}
    new = {json.loads(l)["key_a4"]: json.loads(l) for l in io.open(new_path, encoding="utf-8")}
    out = RUN / f"rows_ds_amend5_merged_{'mini' if code == 'MINI' else 'h45'}.jsonl"
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        for k in a4:
            if k in new:
                r = dict(new[k]); r["key"] = k; r["source"] = "amend5 call (changed view)"
            else:
                r = dict(a4[k]); r["source"] = "amend4 recorded (unchanged view)"
            f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
    return out, a4, new


def cmd_score():
    sys.stdout.reconfigure(encoding="utf-8")
    assert registration_ok()
    sub = DC.load_cell(); rec = RD.records(sub); byid = {it["item_id"]: it for it in sub}
    s4 = J(RUN / "scores_amend4.json"); ch = J(RUN / "views_amend5.json")["changed"]
    S = {"registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "lock": J(RUN / "lock_amend5.json"), "stage2": {}, "stage2_a4": {}, "changed": {}, "source": {}, "per_row": {}}
    for code, path, name in (("MINI", ROWS_MINI, "GPT-4.1 mini"), ("H45", ROWS_H45, "Claude Haiku 4.5")):
        merged, a4rows, newrows = merged_rows(code, path)
        rows, per, _ = A2.score_rows(merged, sub, rec)
        assert len(rows) == 452, len(rows)
        S["stage2"][code] = {p: A2.summarize(rows, per, byid, None, p) for p in POLICIES}
        S["stage2"][code]["_rows"] = {"n": len(rows), "new": len(newrows), "failed": sum(1 for r in newrows.values() if r["status"] != "OK"), "served": sorted({r.get("served_model") or r.get("model") for r in newrows.values()})}
        S["stage2_a4"][code] = {p: s4["stage2"][code][p] for p in POLICIES}
        S["per_row"][code] = per
        # the 74 changed views before (A4 rows) and after (A5 rows): stale at TAU_GOLD, stale at TAU_HI, correct, abstention; transitions; bootstrap
        p4 = s4["per_row"][code]
        before, after, pers, trans, hi_b, hi_a, ab_b, ab_a = [], [], [], [], 0, 0, 0, 0
        for k4, c in ch.items():
            sb, sa = p4[k4], per[k4]
            b_, a_ = int(bool(sb.get("stale_use_tau_gold"))), int(bool(sa.get("stale_use_tau_gold")))
            before.append(b_); after.append(a_); pers.append(c["persona"])
            hi_b += int(bool(sb.get("stale_use"))); hi_a += int(bool(sa.get("stale_use")))
            ab_b += int(A4.is_abst(a4rows[k4]["answer"])); ab_a += int(A4.is_abst(rows[k4]["answer"]))
            if b_ != a_:
                trans.append({"key_a4": k4, "item_id": c["item_id"], "state": c["state"], "policies": c["policies"], "before": b_, "after": a_, "answer_before": a4rows[k4]["answer"], "answer_after": rows[k4]["answer"]})
        bp = A4.boot_paired(before, after, pers)
        # per policy on the changed views only
        per_pol = {}
        for p in POLICIES:
            keys = [k4 for k4, c in ch.items() if p in c["policies"]]
            per_pol[p] = {"n": len(keys), "stale_gold_before": sum(int(bool(p4[k].get("stale_use_tau_gold"))) for k in keys), "stale_gold_after": sum(int(bool(per[k].get("stale_use_tau_gold"))) for k in keys)}
        S["changed"][code] = {"n": len(ch), "stale_gold_before": sum(before), "stale_gold_after": sum(after), "delta_rate": bp["delta"], "ci_item": bp["item"], "ci_cluster": bp["cluster"],
                              "n_boot": bp["n_boot"], "seed": bp["seed"], "n_clusters": bp["n_clusters"], "stale_hi_before": hi_b, "stale_hi_after": hi_a, "abstained_before": ab_b, "abstained_after": ab_a,
                              "transitions": trans, "per_policy": per_pol}
        # the source split on the new views (no changed view may carry an active stale line after the rewrite)
        src = collections.Counter()
        for k4, c in ch.items():
            s_ = A4.view_source(c["view"], rec[c["item_id"]]); src[f"src={s_}|stale={bool(per[k4].get('stale_use_tau_gold'))}"] += 1
            assert s_ != "active", ("an active stale line survives the rewrite", k4)
        S["source"][code] = dict(src)
    pr = probes()
    spend = {"probe_mini": pr["MINI"]["usd"], "probe_h45": pr["H45"]["usd"], "mini": spent(ROWS_MINI), "h45": spent(ROWS_H45)}
    spend["total"] = sum(spend.values()); S["spend"] = spend; S["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(S, RUN / "scores_amend5.json")
    txt = ledger_text(S)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


def cmd_firstsent():
    """The author's addition of 2026-09-14 (after reading the Amendment 5 report): the first-sentence stale count beside the recorded
    column per policy and answerer (Amendment 4's AUX-DS-A4-FIRSTSENT reading, on the Amendment 5 rows), and the source of each
    answerer's residual on the 74 changed views (whole answer against first sentence; tagged-line mention). Appends AUX-DS-A5-FIRSTSENT-*."""
    sys.stdout.reconfigure(encoding="utf-8")
    assert registration_ok()
    sub = DC.load_cell(); rec = RD.records(sub); byid = {it["item_id"]: it for it in sub}
    s4 = J(RUN / "scores_amend4.json"); S5 = J(RUN / "scores_amend5.json"); ch = J(RUN / "views_amend5.json")["changed"]
    NL = chr(10)
    out = {}
    for code, name in (("MINI", "GPT-4.1 mini"), ("H45", "Claude Haiku 4.5")):
        merged = RUN / f"rows_ds_amend5_merged_{'mini' if code == 'MINI' else 'h45'}.jsonl"
        rows, per, _ = A2.score_rows(merged, sub, rec)
        cols = {}
        for pol in POLICIES:
            keys = [k for k, r in rows.items() if pol in r["policies"] and r["label"] == "PRESENT-NEGATIVE" and per[k]["scored"]]
            sc = [k for k in keys if byid[rows[k]["item_id"]]["state"] != "exp"]
            reg = sum(1 for k in sc if per[k]["stale_use_tau_gold"])
            fs = sum(1 for k in sc if RD.score_answer(byid[rows[k]["item_id"]], rec[rows[k]["item_id"]], A4.first_sentence(rows[k]["answer"]))["stale_use_tau_gold"])
            a4c = s4["columns"][code][pol]
            cols[pol] = {"n_scorable": len(sc), "registered_scorable": reg, "first_sentence": fs, "wilson_registered": A4.wilson(reg, len(sc)), "wilson_first": A4.wilson(fs, len(sc)),
                         "a4_registered_scorable": a4c["registered_scorable"]["k"], "a4_first_sentence": a4c["first_sentence"]["k"], "a4_n_scorable": a4c["registered_scorable"]["n"]}
        res_whole = [k for k in ch if per[k]["stale_use_tau_gold"]]
        res_first = [k for k in res_whole if RD.score_answer(byid[rows[k]["item_id"]], rec[rows[k]["item_id"]], A4.first_sentence(rows[k]["answer"]))["stale_use_tau_gold"]]
        residual = {"n_changed": len(ch), "stale_whole_answer": len(res_whole), "stale_first_sentence": len(res_first), "stale_beyond_first_sentence": len(res_whole) - len(res_first),
                    "source": "tagged lines only (no active stale line survives the rewrite; AUX-DS-A5-SOURCE)",
                    "answers": {k: rows[k]["answer"] for k in res_whole}}
        out[code] = {"columns": cols, "residual": residual}
    S5["firstsent"] = out; jdump(S5, RUN / "scores_amend5.json")
    L = [NL + "### AUX-DS-A5-FIRSTSENT-MINI, AUX-DS-A5-FIRSTSENT-H45: stale use at TAU_GOLD on the scorable (supersession + retraction) reached obligations, the registered flag on the whole answer beside the flag on the first sentence, Amendment 5 with Amendment 4 beside (the author's addition of 2026-09-14; appended by `tools/amend5_tagdup.py firstsent`)" + NL + NL,
         "| answerer | policy | scorable | A5 registered (Wilson) | A5 first sentence (Wilson) | A4 registered | A4 first sentence |" + NL + "|---|---|---:|---|---|---:|---:|" + NL]
    for code, name in (("MINI", "GPT-4.1 mini"), ("H45", "Claude Haiku 4.5")):
        for pol in POLICIES:
            c = out[code]["columns"][pol]
            L.append(f"| {name} | {pol} | {c['n_scorable']} | {c['registered_scorable']} / {c['n_scorable']} = {c['registered_scorable'] / c['n_scorable']:.4f} {c['wilson_registered']} | "
                     f"{c['first_sentence']} / {c['n_scorable']} = {c['first_sentence'] / c['n_scorable']:.4f} {c['wilson_first']} | {c['a4_registered_scorable']} / {c['a4_n_scorable']} | {c['a4_first_sentence']} / {c['a4_n_scorable']} |" + NL)
        r = out[code]["residual"]
        L.append(NL + f"Residual on the {r['n_changed']} changed views, {name}: {r['stale_whole_answer']} stale on the whole answer, {r['stale_first_sentence']} on the first sentence, {r['stale_beyond_first_sentence']} only beyond it; source {r['source']}." + NL)
        L.extend(f"- `{k}`: {a!s:.220}" + NL for k, a in r["answers"].items())
    with io.open(LEDGER, "a", encoding="utf-8", newline=NL) as f:
        f.write("".join(L))
    print("".join(L))


def ledger_text(S):
    lk = S["lock"]; sp = S["spend"]; pr = probes(); pj = J(RUN / "projection_amend5.json")
    L = [f"\n### AUX-DS-A5-LOCK, AUX-DS-A5-POP, AUX-DS-A5-PROBE-MINI, AUX-DS-A5-PROBE-H45, AUX-DS-A5-PROJECTION (appended by `tools/amend5_tagdup.py score`)\n\n",
         f"Registration sha256 holds (frozen at `{FROZEN_AT}`); the Amendment 4 header and user text reproduce AUX-DS-A4-LOCK (`{lk['user_answer_a4_sha256'][:16]}...`); prompt digests as pinned. "
         f"The duplicate rule: {lk['detector_rule']}; the tag is the obligation's state (superseded, retracted). Population: {lk['counts']['views']} views, of which **{lk['counts']['changed']} change** "
         f"({lk['counts']['changed_in_422']} of the 422 with {lk['counts']['lines_in_422']} lines tagged, {lk['counts']['changed_lit']} of the 30 LOOKUP-LIT views; {lk['lines_tagged_total']} lines in all), covering {lk['counts']['items']} obligations "
         f"(by state {json.dumps(lk['changed_by_state'])}; by the policies the views serve {json.dumps(lk['changed_by_policy'])}); every count as registered. {lk['renderer_lock']}. "
         f"Probe mini: served `{pr['MINI']['served']}` ({pr['MINI']['tok_in']} in / {pr['MINI']['tok_out']} out); probe Haiku 4.5: served `{pr['H45']['served']}` ({pr['H45']['tok_in']} in / {pr['H45']['tok_out']} out). "
         f"Projection: mini ${pj['MINI']['projected_usd']:.4f}, Haiku ${pj['H45']['projected_usd']:.4f}, sum with probes ${pj['sum']:.4f} (x1.3 ${pj['sum_x1_3']:.4f}) against the $2.00 cap; runs: {pj['runs']}.\n"]
    for code, name in (("MINI", "GPT-4.1 mini"), ("H45", "Claude Haiku 4.5")):
        h = S["stage2"][code]; h4 = S["stage2_a4"][code]; rr = h["_rows"]; c = S["changed"][code]
        L.append(f"\n### AUX-DS-A5-STAGE2-{code}: Stage 2 under {name} with the duplicates tagged, every policy, the committed detector, all states (452 rows: {rr['new']} new answers on the changed views, the rest Amendment 4's; new rows failed {rr['failed']}, served {rr['served']}); each row beside its Amendment 4 row\n\n")
        L.append(A2.HEAD + "\n".join(A2.fmt_row(f"{name} + header, duplicates tagged, {p}", h[p]) + "\n" + A2.fmt_row(f"{name} + header (Amendment 4, recorded), {p}", h4[p]) for p in POLICIES) + "\n")
        L.append(f"\n### AUX-DS-A5-CHANGED-{code}: the {c['n']} changed views before (Amendment 4) and after (this amendment), {name}\n\n"
                 f"Stale at TAU_GOLD: **{c['stale_gold_before']} before, {c['stale_gold_after']} after** of {c['n']}; rate difference (after minus before) {c['delta_rate']:+.4f}, item-level [{c['ci_item'][0]:+.4f}, {c['ci_item'][1]:+.4f}], persona-grouped [{c['ci_cluster'][0]:+.4f}, {c['ci_cluster'][1]:+.4f}] ({c['n_boot']} draws, seed {c['seed']}, {c['n_clusters']} personas; no bar). "
                 f"Stale at TAU_HI: {c['stale_hi_before']} before, {c['stale_hi_after']} after. Abstentions: {c['abstained_before']} before, {c['abstained_after']} after. Per policy (changed views only, stale at TAU_GOLD before -> after): "
                 + "; ".join(f"{p} {v['stale_gold_before']} -> {v['stale_gold_after']} of {v['n']}" for p, v in c["per_policy"].items()) + ".\n\n")
        if c["transitions"]:
            L.append("Transitions (stale at TAU_GOLD):\n\n")
            L.extend(f"- `{t['key_a4']}` ({t['state']}; {', '.join(t['policies'])}): {t['before']} -> {t['after']}; before: {t['answer_before']!s:.160}; after: {t['answer_after']!s:.160}\n" for t in c["transitions"])
            L.append("\n")
        else:
            L.append("No transition: every changed view keeps its flag.\n\n")
        L.append(f"### AUX-DS-A5-SOURCE-{code}: the source split on the changed views after the rewrite (no active line asserts the stale value on any of them, asserted): {json.dumps(S['source'][code])}\n")
    L.append(f"\n### AUX-DS-A5-SPEND\n\nProbe mini ${sp['probe_mini']:.4f}; probe Haiku ${sp['probe_h45']:.4f}; mini lane ${sp['mini']:.4f}; Haiku lane ${sp['h45']:.4f}; **total ${sp['total']:.4f}** against the author's $2.00 cap.\n")
    return "".join(L)


if __name__ == "__main__":
    {"lock": cmd_lock, "probe-mini": cmd_probe_mini, "probe-h45": cmd_probe_h45, "project": cmd_project,
     "run-mini": cmd_run_mini, "run-h45": cmd_run_h45, "score": cmd_score, "firstsent": cmd_firstsent}[sys.argv[1]]()
