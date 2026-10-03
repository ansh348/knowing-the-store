# -*- coding: utf-8 -*-
"""amend6_depth.py -- ADDENDUM_DS Amendment 6 (registrations/ADDENDUM_DS_AMENDMENT_6.md, frozen at 12c63f9; registered text sha256
52effd8d... over the bytes above the marker; the author's cap ruling of 2026-09-15 below the marker: $6.00): coverage-gated depth
expansion of the retrieval view. Descriptive: no prediction, no bar, no verdict. Written from amend5_tagdup.py; amend4_header is
imported for the header, the prompt, the lanes' call helpers and the detector-side helpers; nothing there is edited.

Views: the recorded ten-deep ranking (resp_review/l2/retrieval.json top10_ids) rendered by the recorded renderer
(resp_common.render_line over the join's flags); FLAT-k = the first k lines, k = 5..10; GATED = 5, or 10 where the smallest
model's recorded indexed coverage score (the cell's true.fok, the field policy_actions reads) is at or above theta_fok = 35/307. RENDERER LOCK:
the k = 5 rendering reproduces views.json ALWAYS.text byte for byte on all 661 items.

Subcommands, in order:
  lock          registration sha256 (frozen bytes), the cap ruling, the Amendment 4 header sha256 against AUX-DS-A4-LOCK, the prompt
                digests; the views, the lock, the population counts (557; 366 expanded; 8.29; 9.45 / 7.75; 65 / 72 / 77 / 82 / 88 / 89 / 87;
                3,168 calls per answerer, the registered 2,994 corrected under D-DS-A6-1)                                              -> run/lock_amend6.json, run/views_amend6.json;
                NUMBERS_DS.md section 12 opened with AUX-DS-A6-REG
  probe-mini | probe-h45   one call on a ten-line view (served identifier, tokens)     -> run/probes_amend6.json
  project       both lanes over the 2,994 views against the $6 cap (x1.3), printed    -> run/projection_amend6.json
  run-mini | run-h45       the lanes                                                   -> run/rows_ds_amend6_{mini,h45}.jsonl
  score         reach, correct at 0.50 (and 0.80), abstention on absent, per policy with intervals; the budget-matched comparison
                (GATED against the flat curve interpolated at its mean depth between the bracketing k), both bootstraps; the
                targeting figure; NUMBERS_DS.md section 12 (AUX-DS-A6-*)              -> run/scores_amend6.json
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import datetime as dt
import hashlib
import io
import json
import re
import sys
import threading
import time

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import ds_common as DC                                                       # noqa: E402
from ds_common import ROOT, DS, RUN, J, jdump, THETA_FOK                    # noqa: E402
import run_ds as RD                                                          # noqa: E402
import prompts_ds as PD                                                      # noqa: E402
import prompts_e1 as P                                                       # noqa: E402
import amend2_lit as A2                                                      # noqa: E402
import amend4_header as A4                                                   # noqa: E402
from resp_common import true_flags, render_line                              # noqa: E402
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
from run_cf import last_json                                                 # noqa: E402

api = A4.api
REG = ROOT / "registrations" / "ADDENDUM_DS_AMENDMENT_6.md"
REG_SHA = "52effd8d7911a62505f2ee0a7d97fc42ca600a595dbffb46463ec05598fec65a"
FROZEN_AT = "12c63f9"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
CAP_RULING = "Cap raised from $4.00 to $6.00"
LINE = 6.00
CACHE6 = DS / "cache_amend6"
LANE_MINI, PRICE_MINI = A4.LANE_MINI, A4.PRICE_MINI
LANE_H45, PRICE_H45 = A4.LANE_H45, A4.PRICE_H45
ROWS_MINI = RUN / "rows_ds_amend6_mini.jsonl"
ROWS_H45 = RUN / "rows_ds_amend6_h45.jsonl"
LEDGER = DS / "NUMBERS_DS.md"
ARM = "ANSWER-A6"
DEPTHS = (5, 6, 7, 8, 9, 10)
POLS = tuple(f"FLAT-{k}" for k in DEPTHS) + ("GATED",)
EXPECT = {"items": 557, "licensed": 174, "absent": 383, "expanded": 366, "expanded_licensed": 155, "expanded_absent": 211, "mean_view": 8.29, "per_licensed": 9.45, "per_absent": 7.75,
          "inview": {"5": 65, "6": 72, "7": 77, "8": 82, "9": 88, "10": 89, "GATED": 87}, "calls_per_answerer": 3168}   # 3,168 = 174 x 5 + 383 x 6, not the registered 2,994 (D-DS-A6-1: 696 was an arithmetic slip for 870)
N_BOOT, SEED = 10000, 42


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def registration_ok():
    b = REG.read_bytes(); i = b.find(FROZEN_END)
    return i > 0 and hashlib.sha256(b[:i]).hexdigest() == REG_SHA


def assert_lineage(before_call=True):
    assert registration_ok(), "ADDENDUM_DS_AMENDMENT_6.md frozen bytes sha256 != 52effd8d -- STOP"
    assert CAP_RULING in REG.read_text(encoding="utf-8").split("REGISTERED TEXT ENDS ABOVE THIS LINE", 1)[1], "the author's cap ruling ($6.00) is not below the marker -- STOP"
    lk4 = J(RUN / "lock_amend4.json")
    assert sha(A4.USER_ANSWER_A4) == lk4["user_answer_a4_sha256"] and sha(A4.HEADER) == lk4["header_sha256"], "the Amendment 4 header differs from AUX-DS-A4-LOCK -- STOP"
    assert PD.digests() == lk4["prompts_ds"] and P.file_sha256() == lk4["prompts_e1"]["file"] and P.texts_sha256() == lk4["prompts_e1"]["texts"], "prompt digests differ -- STOP"
    if before_call:
        assert "AUX-DS-A6-REG" in LEDGER.read_text(encoding="utf-8"), "AUX-DS-A6-REG absent from NUMBERS_DS.md -- STOP (no call before the freeze is recorded)"
    RD.assert_lineage()


def redirect():
    CACHE6.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                             # noqa: SLF001
    e0.CACHE_PATH = CACHE6 / "responses.json"; e0.LEDGER_PATH = CACHE6 / "cost_ledger.json"
    e0._cache = None; e0._load_cache()                                       # noqa: SLF001
    e0.HARD_CAP_USD = LINE
    return e0


# ------------------------------------------------------------------ views
def build_views():
    """The 557 items x depths, rendered from the recorded ranking; the lock; the gate; the counts."""
    sub = DC.load_cell(); fl = true_flags()
    retr = J(ROOT / "resp_review" / "l2" / "retrieval.json")["items"]
    views = J(DS / "views.json")["items"]
    pop = [it for it in sub if it["label"] in ("PRESENT", "ABSENT")]
    out, n_lock = {}, 0
    for it in pop:
        i = it["item_id"]; ids = retr[i]["top10_ids"]; assert len(ids) == 10
        assert ids[:5] == views[i]["ALWAYS"]["ids"], ("lock: the ALWAYS ids are not the ranking's first five", i)
        texts = {}
        for k in DEPTHS:
            lines = [render_line(r + 1, fl[it["persona"]][e]) for r, e in enumerate(ids[:k])]
            texts[k] = "\n".join(lines)
        assert texts[5] == views[i]["ALWAYS"]["text"], ("lock: the k = 5 rendering differs from the recorded ALWAYS view", i)
        n_lock += 1
        fok = it["true"]["fok"]; gated_k = 10 if fok >= THETA_FOK else 5     # the field policy_actions reads for MODEL's abstention gate
        gold = set(it.get("gold") or [])
        out[i] = {"item_id": i, "persona": it["persona"], "question": it["question"], "label": it["label"], "state": it.get("state"), "fok": fok, "gated_k": gated_k,
                  "always_sha": views[i]["ALWAYS"]["sha"], "views": {str(k): {"text": texts[k], "sha": sha(texts[k])[:16], "n_lines": k, "gold_in_view": bool(gold & set(ids[:k]))} for k in DEPTHS}}
    return out, n_lock


def counts_of(V):
    lic = [v for v in V.values() if v["label"] == "PRESENT"]; ab = [v for v in V.values() if v["label"] == "ABSENT"]
    c = {"items": len(V), "licensed": len(lic), "absent": len(ab), "expanded": sum(1 for v in V.values() if v["gated_k"] == 10),
         "expanded_licensed": sum(1 for v in lic if v["gated_k"] == 10), "expanded_absent": sum(1 for v in ab if v["gated_k"] == 10),
         "mean_view": round(sum(v["gated_k"] for v in V.values()) / len(V), 2), "per_licensed": round(sum(v["gated_k"] for v in lic) / len(lic), 2), "per_absent": round(sum(v["gated_k"] for v in ab) / len(ab), 2),
         "inview": {**{str(k): sum(1 for v in lic if v["views"][str(k)]["gold_in_view"]) for k in DEPTHS}, "GATED": sum(1 for v in lic if v["views"][str(v["gated_k"])]["gold_in_view"])},
         "calls_per_answerer": sum(1 for v in lic) * (len(DEPTHS) - 1) + sum(1 for v in ab) * len(DEPTHS)}
    return c


def jobs_new():
    """The views to answer: every (item, depth) except the licensed k = 5 (Amendment 4's row)."""
    V = J(RUN / "views_amend6.json")["views"]
    out = []
    for i, v in V.items():
        for k in DEPTHS:
            if v["label"] == "PRESENT" and k == 5:
                continue
            w = v["views"][str(k)]
            out.append({"key": f"{i}|{w['sha']}|k{k}", "item_id": i, "persona": v["persona"], "question": v["question"], "label": v["label"], "state": v["state"],
                        "view": w["text"], "view_sha": w["sha"], "n_lines": k, "depth": k, "policies": [f"FLAT-{k}"] + (["GATED"] if v["gated_k"] == k else [])})
    return out


def cmd_lock():
    assert_lineage(before_call=False)
    V, n_lock = build_views(); c = counts_of(V)
    ok = all(c[k] == v for k, v in EXPECT.items())
    out = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "cap_ruling": CAP_RULING + " (dated 2026-09-15, below the marker)", "line_usd": LINE,
           "header_sha256": sha(A4.HEADER), "user_answer_a4_sha256": sha(A4.USER_ANSWER_A4), "prompts_ds": PD.digests(), "theta_fok": THETA_FOK,
           "renderer_lock": f"{n_lock} of {len(V)} k = 5 renderings byte-identical to views.json ALWAYS; the ALWAYS ids the ranking's first five on all", "counts": c, "expected": EXPECT, "counts_ok": ok, "deviation": "D-DS-A6-1: the registered 696 licensed views / 2,994 calls per answerer is an arithmetic slip for 870 / 3,168; every other count reproduces",
           "ranking": "resp_review/l2/retrieval.json top10_ids (ADDENDUM_RESP, frozen 17e6328)", "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RUN / "lock_amend6.json"); jdump({"views": V}, RUN / "views_amend6.json")
    print(json.dumps({k: v for k, v in out.items() if k not in ("prompts_ds",)}, indent=1))
    if not ok:
        sys.exit("POPULATION COUNTS DO NOT REPRODUCE -- STOP")
    txt = LEDGER.read_text(encoding="utf-8")
    if "AUX-DS-A6-REG" not in txt:
        with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
            f.write(f"\n## 12. DS Amendment 6: coverage-gated depth expansion of the retrieval view (registrations/ADDENDUM_DS_AMENDMENT_6.md; descriptive)\n\n"
                    f"### AUX-DS-A6-REG\n\nRegistered text sha256 **`{REG_SHA}`** (the bytes above the marker line), frozen at `{FROZEN_AT}` on 2026-09-15, recorded here before the first call; the author's cap ruling of 2026-09-15 below the marker ($4.00 to $6.00 for the k = 6, 8, 9 flat policies added at the freeze). Descriptive: no prediction, no bar, no verdict. Runner `tools/amend6_depth.py`. The registered call count (2,994 per answerer) is an arithmetic slip for 3,168 (D-DS-A6-1, `DEVIATIONS_DS.md`); every other count reproduces at the lock.\n")
    print("section 12 opened with AUX-DS-A6-REG")


# ------------------------------------------------------------------ probe / project
def probes():
    p = RUN / "probes_amend6.json"
    return J(p) if p.exists() else {}


def probe_job():
    return next(j for j in jobs_new() if j["depth"] == 10 and j["label"] == "PRESENT")


def cmd_probe_mini():
    assert_lineage(); e0 = redirect(); first = probe_job()
    r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,   # noqa: SLF001
                                             messages=A4.messages(first), response_format={"type": "json_object"})
    o = api.parse_json(r.choices[0].message.content) or {}
    rec = {"item_id": first["item_id"], "view_lines": first["n_lines"], "served": r.model, "identifier_ok": LANE_MINI in r.model, "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens,
           "usd": r.usage.prompt_tokens / 1e6 * PRICE_MINI[0] + r.usage.completion_tokens / 1e6 * PRICE_MINI[1], "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL",
           "sample": (r.choices[0].message.content or "")[:300], "when": dt.datetime.now().isoformat(timespec="seconds")}
    out = probes(); out["MINI"] = rec; jdump(out, RUN / "probes_amend6.json"); print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def cmd_probe_h45():
    assert_lineage(); first = probe_job(); cl = A2.anthropic_client()
    text, tin, tout, served = A4.h45_once(cl, first); o = last_json(text) or {}
    rec = {"item_id": first["item_id"], "view_lines": first["n_lines"], "served": served, "identifier_ok": served == LANE_H45, "tok_in": tin, "tok_out": tout,
           "usd": tin / 1e6 * PRICE_H45[0] + tout / 1e6 * PRICE_H45[1], "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL", "sample": text[:300],
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    out = probes(); out["H45"] = rec; jdump(out, RUN / "probes_amend6.json"); print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def cmd_project():
    pr = probes(); hj = jobs_new(); per_line = 45.0
    out = {"views": len(hj), "line": LINE}
    for code, price in (("MINI", PRICE_MINI), ("H45", PRICE_H45)):
        x = pr[code]; shell = max(50.0, x["tok_in"] - per_line * x["view_lines"])
        tin = sum(shell + per_line * j["n_lines"] for j in hj); tout = x["tok_out"] * len(hj)
        out[code] = {"projected_usd": tin / 1e6 * price[0] + tout / 1e6 * price[1], "probe_usd": x["usd"]}
    out["sum"] = out["MINI"]["projected_usd"] + out["H45"]["projected_usd"] + out["MINI"]["probe_usd"] + out["H45"]["probe_usd"]
    out["sum_x1_3"] = 1.3 * out["sum"]; out["runs"] = out["sum_x1_3"] < LINE; out["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(out, RUN / "projection_amend6.json"); print(json.dumps(out, indent=1))
    if not out["runs"]:
        sys.exit("PROJECTION x1.3 AT OR ABOVE THE $6 CAP -- STOP")


def spent(path):
    return sum(json.loads(l).get("usd", 0.0) for l in io.open(path, encoding="utf-8")) if path.exists() else 0.0


def row_fields(job):
    return {k: job[k] for k in ("key", "item_id", "persona", "question", "label", "state", "view_sha", "n_lines", "depth", "policies")}


# ------------------------------------------------------------------ run
def cmd_run_mini():
    assert_lineage(); redirect(); hj = jobs_new()
    assert J(RUN / "projection_amend6.json")["runs"]
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
               "model": LANE_MINI, "cached": r["cached"], "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "usd": usd, "raw": (r["content"] or "")[:400], "source": "amend6 call"}
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
    assert_lineage(); hj = jobs_new()
    assert J(RUN / "projection_amend6.json")["runs"]
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
               "model": LANE_H45, "served_model": served, "cached": False, "tok_in": tin, "tok_out": tout, "usd": usd, "raw": (text or "")[:400], "source": "amend6 call"}
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
def wilson(k, n):
    return A4.wilson(k, n)


def cmd_score():
    sys.stdout.reconfigure(encoding="utf-8")
    assert registration_ok()
    sub = DC.load_cell(); rec = RD.records(sub); byid = {it["item_id"]: it for it in sub}
    V = J(RUN / "views_amend6.json")["views"]; lk = J(RUN / "lock_amend6.json")
    lic = [i for i, v in V.items() if v["label"] == "PRESENT"]; ab = [i for i, v in V.items() if v["label"] == "ABSENT"]
    pers = {i: V[i]["persona"] for i in V}
    S = {"registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "lock": lk, "answerers": {}, "spend": {}}
    for code, path, a4path, name in (("MINI", ROWS_MINI, RUN / "rows_ds_amend4_mini.jsonl", "GPT-4.1 mini"), ("H45", ROWS_H45, RUN / "rows_ds_amend4_h45.jsonl", "Claude Haiku 4.5")):
        rows = {json.loads(l)["key"]: json.loads(l) for l in io.open(path, encoding="utf-8")}
        a4 = {json.loads(l)["key"]: json.loads(l) for l in io.open(a4path, encoding="utf-8")}
        # answer per (item, depth): the licensed k = 5 from Amendment 4 (ALWAYS view), everything else from this amendment
        def answer(i, k):
            if V[i]["label"] == "PRESENT" and k == 5:
                r = a4[f"{i}|{V[i]['always_sha']}"]
            else:
                r = rows[f"{i}|{V[i]['views'][str(k)]['sha']}|k{k}"]
            return r
        def depth_of(i, pol):
            return V[i]["gated_k"] if pol == "GATED" else int(pol.split("-")[1])
        per = {}
        for pol in POLS:
            corr, corr_hi, inview, inview_corr, abst_lic, abst_abs, claim_abs, fails = [], [], [], [], [], [], [], 0
            for i in lic:
                k = depth_of(i, pol); r = answer(i, k)
                if r["status"] != "OK":
                    fails += 1; corr.append(0); corr_hi.append(0); inview.append(int(V[i]["views"][str(k)]["gold_in_view"])); abst_lic.append(0); continue
                sc = RD.score_answer(byid[i], rec[i], r["answer"])
                corr.append(int(bool(sc.get("correct")))); corr_hi.append(int(bool(sc.get("correct_tau_hi")))); gi = V[i]["views"][str(k)]["gold_in_view"]; inview.append(int(gi))
                if gi:
                    inview_corr.append(int(bool(sc.get("correct"))))
                abst_lic.append(int(A4.is_abst(r["answer"])))
            for i in ab:
                k = depth_of(i, pol); r = answer(i, k)
                if r["status"] != "OK":
                    fails += 1; abst_abs.append(0); claim_abs.append(0); continue
                a_ = A4.is_abst(r["answer"]); abst_abs.append(int(a_)); claim_abs.append(int(not a_))
            per[pol] = {"depth_mean": round(sum(depth_of(i, pol) for i in lic + ab) / len(lic + ab), 2), "depth_licensed": round(sum(depth_of(i, pol) for i in lic) / len(lic), 2),
                        "inview": {"k": sum(inview), "n": len(lic), "wilson": wilson(sum(inview), len(lic))}, "correct": {"k": sum(corr), "n": len(lic), "wilson": wilson(sum(corr), len(lic))},
                        "correct_tau_hi": {"k": sum(corr_hi), "n": len(lic)}, "correct_among_inview": {"k": sum(inview_corr), "n": len(inview_corr)},
                        "abstain_licensed": {"k": sum(abst_lic), "n": len(lic)}, "abstain_absent": {"k": sum(abst_abs), "n": len(ab), "wilson": wilson(sum(abst_abs), len(ab))},
                        "claim_absent": {"k": sum(claim_abs), "n": len(ab)}, "failed": fails, "_corr": corr, "_abs": abst_abs, "_inview": inview}
        # the budget-matched comparison: GATED against the flat curve interpolated at d between the bracketing k
        d = per["GATED"]["depth_mean"]; k0 = int(np.floor(d)); k1 = k0 + 1; w = d - k0
        matched = {}
        rng = np.random.default_rng(SEED)
        for metric, field, ids in (("correct", "_corr", lic), ("inview", "_inview", lic), ("abstain_absent", "_abs", ab)):
            g = np.array(per["GATED"][field]); f0 = np.array(per[f"FLAT-{k0}"][field]); f1 = np.array(per[f"FLAT-{k1}"][field]); pp = np.array([pers[i] for i in ids])
            v_d = (1 - w) * f0.mean() + w * f1.mean(); delta = g.mean() - v_d
            n = len(g); groups = np.unique(pp); by = {u: np.flatnonzero(pp == u) for u in groups}
            di, dc = [], []
            for _ in range(N_BOOT):
                s = rng.integers(0, n, n); di.append(g[s].mean() - ((1 - w) * f0[s].mean() + w * f1[s].mean()))
                s = np.concatenate([by[groups[t]] for t in rng.integers(0, len(groups), len(groups))]); dc.append(g[s].mean() - ((1 - w) * f0[s].mean() + w * f1[s].mean()))
            matched[metric] = {"d": d, "bracket": [k0, k1], "flat_interpolated": round(float(v_d), 4), "gated": round(float(g.mean()), 4), "delta": round(float(delta), 4),
                               "ci_item": [round(float(np.percentile(di, 2.5)), 4), round(float(np.percentile(di, 97.5)), 4)], "ci_persona": [round(float(np.percentile(dc, 2.5)), 4), round(float(np.percentile(dc, 97.5)), 4)],
                               "n_boot": N_BOOT, "seed": SEED, "n_clusters": int(len(groups))}
        for pol in per:
            for f_ in ("_corr", "_abs", "_inview"):
                per[pol].pop(f_, None)
        S["answerers"][code] = {"name": name, "per_policy": per, "matched": matched, "rows": len(rows), "failed": sum(1 for r in rows.values() if r["status"] != "OK"), "served": sorted({r.get("served_model") or r.get("model") for r in rows.values()})}
        S["spend"][code] = round(spent(path), 4)
    pr = probes(); S["spend"]["probes"] = round(sum(v["usd"] for v in pr.values()), 4); S["spend"]["total"] = round(sum(v for v in S["spend"].values()), 4); S["spend"]["line"] = LINE
    S["targeting"] = {"per_licensed_item_gated": lk["counts"]["per_licensed"], "per_absent_item_gated": lk["counts"]["per_absent"], "flat_at_equal_total_cost": lk["counts"]["mean_view"]}
    S["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(S, RUN / "scores_amend6.json")
    txt = ledger_text(S)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


def ledger_text(S):
    lk = S["lock"]; c = lk["counts"]; pr = probes(); pj = J(RUN / "projection_amend6.json")
    L = [f"\n### AUX-DS-A6-LOCK, AUX-DS-A6-POP, AUX-DS-A6-PROBE-MINI, AUX-DS-A6-PROBE-H45, AUX-DS-A6-PROJECTION (appended by `tools/amend6_depth.py score`)\n\n",
         f"Registration sha256 holds (frozen at `{FROZEN_AT}`); the cap ruling below the marker read ($6.00); the Amendment 4 header reproduces AUX-DS-A4-LOCK; prompt digests as pinned. {lk['renderer_lock']}. Population {c['items']} items ({c['licensed']} licensed, {c['absent']} absent); the recorded coverage score at or above theta_fok = {lk['theta_fok']:.6f} on {c['expanded']} ({c['expanded_licensed']} licensed, {c['expanded_absent']} absent), so GATED renders ten lines there and five elsewhere: mean view **{c['mean_view']}** lines; the targeting figure **{c['per_licensed']} lines per licensed item and {c['per_absent']} per absent item** at the flat policy's {c['mean_view']} everywhere. The licensed record in view along the flat curve k = 5 to 10: {', '.join(str(c['inview'][str(k)]) for k in DEPTHS)} of 174; under GATED {c['inview']['GATED']}. {c['calls_per_answerer']} calls per answerer. Probes: mini served `{pr['MINI']['served']}` ({pr['MINI']['tok_in']} in / {pr['MINI']['tok_out']} out on a ten-line view); Haiku 4.5 served `{pr['H45']['served']}` ({pr['H45']['tok_in']} in / {pr['H45']['tok_out']} out). Projection printed before submission: mini ${pj['MINI']['projected_usd']:.4f}, Haiku ${pj['H45']['projected_usd']:.4f}, sum with probes ${pj['sum']:.4f} (x1.3 ${pj['sum_x1_3']:.4f}) against the $6.00 line; runs: {pj['runs']}.\n"]
    for code, A in S["answerers"].items():
        L.append(f"\n### AUX-DS-A6-INVIEW, AUX-DS-A6-CORRECT-{code}, AUX-DS-A6-ABSENT-{code}: the flat curve and GATED under {A['name']} (rows {A['rows']}, failed {A['failed']}, served {A['served']}; the licensed k = 5 rows are Amendment 4's)\n\n")
        L.append("| policy | mean depth (all; licensed) | licensed record in view (Wilson) | correct at 0.50 (Wilson) | correct at 0.80 | correct among in view | abstain, licensed | abstain, absent (Wilson) | claims on absent |\n|---|---|---|---|---:|---|---|---|---:|\n")
        for pol, d in A["per_policy"].items():
            L.append(f"| {pol} | {d['depth_mean']}; {d['depth_licensed']} | {d['inview']['k']} / {d['inview']['n']} = {d['inview']['k'] / d['inview']['n']:.4f} {[round(x, 4) for x in d['inview']['wilson']]} | {d['correct']['k']} / {d['correct']['n']} = {d['correct']['k'] / d['correct']['n']:.4f} {[round(x, 4) for x in d['correct']['wilson']]} | {d['correct_tau_hi']['k']} | {d['correct_among_inview']['k']} / {d['correct_among_inview']['n']} | {d['abstain_licensed']['k']} / {d['abstain_licensed']['n']} | {d['abstain_absent']['k']} / {d['abstain_absent']['n']} = {d['abstain_absent']['k'] / d['abstain_absent']['n']:.4f} {[round(x, 4) for x in d['abstain_absent']['wilson']]} | {d['claim_absent']['k']} |\n")
        M = A["matched"]
        L.append(f"\n### AUX-DS-A6-MATCHED-{code}: GATED against the flat curve interpolated at its mean depth d = {M['correct']['d']} (between FLAT-{M['correct']['bracket'][0]} and FLAT-{M['correct']['bracket'][1]}); the matched difference GATED minus flat(d), both bootstraps ({M['correct']['n_boot']} draws, seed {M['correct']['seed']}, {M['correct']['n_clusters']} personas; the three policies resampled together; descriptive, no bar)\n\n")
        for metric, m in M.items():
            L.append(f"- {metric}: GATED {m['gated']:.4f}, flat at d {m['flat_interpolated']:.4f}, **difference {m['delta']:+.4f}**, item [{m['ci_item'][0]:+.4f}, {m['ci_item'][1]:+.4f}], persona [{m['ci_persona'][0]:+.4f}, {m['ci_persona'][1]:+.4f}]\n")
    L.append(f"\n### AUX-DS-A6-SPEND: {json.dumps(S['spend'])}\n")
    return "".join(L)


if __name__ == "__main__":
    {"lock": cmd_lock, "probe-mini": cmd_probe_mini, "probe-h45": cmd_probe_h45, "project": cmd_project,
     "run-mini": cmd_run_mini, "run-h45": cmd_run_h45, "score": cmd_score}[sys.argv[1]]()
