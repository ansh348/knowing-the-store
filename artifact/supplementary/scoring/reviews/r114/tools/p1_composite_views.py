# -*- coding: utf-8 -*-
"""p1_composite_views.py -- SPEC_R114 section 2: the composite's answered reading on the ACTUAL expanded views (DS Amendment 7,
AUX-DS-A7-COMPOSITE-ANSWERED replaced the 99 unanswered (item, view) inputs by the FLAT-5 proxy; R113 Z1 listed them).

MODEL CALLS (billed): 99 GPT-4.1 mini + 99 Claude Haiku 4.5, one per distinct (item, view sha), SYSTEM_ANSWER + USER_ANSWER_A4
(the Amendment 4 header), the DS decoding (mini: temperature 0, seed 42, max_tokens 200, JSON mode, one retry; Haiku: synchronous,
temperature 0, max_tokens 200, the last JSON object), plus one probe per lane. Nothing recorded is re-run; every existing rows
file, cache and score file is read only. New files: ds_downstream/cache_r114/, run/rows_ds_r114_{mini,h45}.jsonl, run/probes_r114.json,
reviews/r114/results/p1_composite_actual.json; NUMBERS_DS.md section 14 appended.

Subcommands, in order:  build | probe-mini | probe-h45 | project | run-mini | run-h45 | score
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

from r114_common import ROOT, RESULTS, J, jdump, assert_spec, ledger_append_to, LEDGER as LEDGER_R114

sys.path.insert(0, str(ROOT / "ds_downstream" / "tools"))
import ds_common as DC                                                       # noqa: E402
from ds_common import DS, RUN                                                # noqa: E402
import run_ds as RD                                                          # noqa: E402
import prompts_ds as PD                                                      # noqa: E402
import prompts_e1 as P                                                       # noqa: E402
import amend2_lit as A2                                                      # noqa: E402
import amend4_header as A4                                                   # noqa: E402
import amend7_reported as A7                                                 # noqa: E402
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
from run_cf import last_json                                                 # noqa: E402

import numpy as np                                                           # noqa: E402

api = A4.api
CACHE = DS / "cache_r114"
ROWS_MINI = RUN / "rows_ds_r114_mini.jsonl"
ROWS_H45 = RUN / "rows_ds_r114_h45.jsonl"
PROBES = RUN / "probes_r114.json"
LEDGER_DS = DS / "NUMBERS_DS.md"
ARM = "ANSWER-R114"
LANE_MINI, PRICE_MINI = A4.LANE_MINI, A4.PRICE_MINI
LANE_H45, PRICE_H45 = A4.LANE_H45, A4.PRICE_H45
LINE = 0.40            # this phase's line: the manifest's conservative $0.20 doubled; a projection above it is a STOP
Z1 = ROOT / "reviews" / "r113" / "results" / "z1_composite_proxy.json"
EXPECT = {"MODEL": 10, "LOOKUP": 17, "MODEL-ALL": 10, "LOOKUP-ALL": 17, "LOOKUP-LIT": 72}
N_BOOT, SEED = 10000, 42


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def assert_lineage():
    assert_spec()
    lk4 = J(RUN / "lock_amend4.json")
    assert sha(A4.USER_ANSWER_A4) == lk4["user_answer_a4_sha256"] and sha(A4.HEADER) == lk4["header_sha256"], "the Amendment 4 header differs from AUX-DS-A4-LOCK -- STOP"
    assert PD.digests() == lk4["prompts_ds"] and P.file_sha256() == lk4["prompts_e1"]["file"] and P.texts_sha256() == lk4["prompts_e1"]["texts"], "prompt digests differ -- STOP"
    assert A7.registration_ok() and J(RUN / "lock_amend7.json")["gates_ok"], "Amendment 7 lock -- STOP"
    RD.assert_lineage()


def redirect():
    CACHE.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                             # noqa: SLF001
    e0.CACHE_PATH = CACHE / "responses.json"; e0.LEDGER_PATH = CACHE / "cost_ledger.json"
    e0._cache = None; e0._load_cache()                                       # noqa: SLF001
    e0.HARD_CAP_USD = LINE
    return e0


# ------------------------------------------------------------------ build
def build_jobs():
    """The 99 distinct (item, view) inputs, rebuilt from the DS artifacts and asserted against R113's list; the view text from views.json."""
    z1 = J(Z1)
    st1 = J(DS / "stage1.json")["per_item"]; views = J(DS / "views.json")["items"]; pol = J(DS / "policies.json")["items"]
    sub = DC.load_cell(); byid = {it["item_id"]: it for it in sub}
    absent = [i for i in st1 if pol[i]["label"] == "ABSENT"]; assert len(absent) == 383
    need = []
    for p in EXPECT:
        ids = [i for i in absent if not st1[i][p]["abstain"] and st1[i][p]["view_size"] > 5]
        assert len(ids) == EXPECT[p], (p, len(ids))
        for i in ids:
            need.append((i, p, views[i][p]["sha"]))
    z1set = {(d["item_id"], d["policy"], d["view_sha"]) for d in z1["inputs"]}
    assert set(need) == z1set and len(need) == 126, "the R113 Z1 list does not reproduce -- STOP"
    assert z1["inputs_with_any_recorded_answer"] == 0
    # the same recorded-answer scan as R113, re-run now so a row written since would be found
    have = set()
    for f in sorted((RUN).glob("rows_*.jsonl")):
        if f.name.startswith("rows_ds_r114"):
            continue
        for l in io.open(f, encoding="utf-8"):
            r = json.loads(l); have.add((r["item_id"], r["view_sha"]))
    jobs = {}
    for i, p, vs in need:
        v = views[i][p]; assert sha(v["text"])[:16] == vs, (i, p)
        assert (i, vs) not in have, ("a recorded answer exists on this view now", i, vs)
        key = f"{i}|{vs}"
        it = byid[i]
        j = jobs.setdefault(key, {"key": key, "item_id": i, "persona": it["persona"], "question": it["question"], "label": it["label"], "state": it["state"],
                                  "view": v["text"], "view_sha": vs, "n_lines": v["n_lines"], "policies": []})
        assert j["view"] == v["text"]
        j["policies"].append(p)
    jobs = list(jobs.values())
    assert len(jobs) == 99 and sum(len(j["policies"]) for j in jobs) == 126
    assert all(j["label"] == "ABSENT" for j in jobs)
    return sub, jobs


def cmd_build():
    assert_lineage()
    sub, jobs = build_jobs()
    out = {"spec": "reviews/r114/SPEC_R114.md section 2", "n_jobs": len(jobs), "policy_rows": sum(len(j["policies"]) for j in jobs),
           "lines": sum(j["n_lines"] for j in jobs), "per_policy": dict(collections.Counter(p for j in jobs for p in j["policies"])),
           "header_sha256": sha(A4.HEADER), "user_answer_a4_sha256": sha(A4.USER_ANSWER_A4), "system_answer_sha256": sha(PD.SYSTEM_ANSWER),
           "lanes": {"MINI": {"model": LANE_MINI, "temperature": 0, "seed": 42, "max_tokens": 200, "json_mode": True, "retry": 1},
                     "H45": {"model": LANE_H45, "temperature": 0, "max_tokens": 200, "synchronous": True, "parse": "last JSON object", "retry": 1}},
           "jobs": [{k: j[k] for k in ("key", "item_id", "persona", "policies", "view_sha", "n_lines")} for j in jobs],
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RESULTS / "p1_jobs.json")
    print(json.dumps({k: v for k, v in out.items() if k != "jobs"}, indent=1))


# ------------------------------------------------------------------ probe / project
def probes():
    return J(PROBES) if PROBES.exists() else {}


def probe_job(jobs):
    return max(jobs, key=lambda j: j["n_lines"])


def cmd_probe_mini():
    assert_lineage(); e0 = redirect(); sub, jobs = build_jobs(); first = probe_job(jobs)
    r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,   # noqa: SLF001
                                             messages=A4.messages(first), response_format={"type": "json_object"})
    o = api.parse_json(r.choices[0].message.content) or {}
    rec = {"item_id": first["item_id"], "view_lines": first["n_lines"], "served": r.model, "identifier_ok": LANE_MINI in r.model, "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens,
           "usd": r.usage.prompt_tokens / 1e6 * PRICE_MINI[0] + r.usage.completion_tokens / 1e6 * PRICE_MINI[1], "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL",
           "sample": (r.choices[0].message.content or "")[:300], "when": dt.datetime.now().isoformat(timespec="seconds")}
    out = probes(); out["MINI"] = rec; jdump(out, PROBES); print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def cmd_probe_h45():
    assert_lineage(); sub, jobs = build_jobs(); first = probe_job(jobs); cl = A2.anthropic_client()
    text, tin, tout, served = A4.h45_once(cl, first); o = last_json(text) or {}
    rec = {"item_id": first["item_id"], "view_lines": first["n_lines"], "served": served, "identifier_ok": served == LANE_H45, "tok_in": tin, "tok_out": tout,
           "usd": tin / 1e6 * PRICE_H45[0] + tout / 1e6 * PRICE_H45[1], "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL", "sample": text[:300],
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    out = probes(); out["H45"] = rec; jdump(out, PROBES); print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def cmd_project():
    pr = probes(); sub, jobs = build_jobs(); per_line = 45.0
    out = {"views": len(jobs), "line": LINE}
    for code, price in (("MINI", PRICE_MINI), ("H45", PRICE_H45)):
        x = pr[code]; shell = max(50.0, x["tok_in"] - per_line * x["view_lines"])
        tin = sum(shell + per_line * j["n_lines"] for j in jobs); tout = x["tok_out"] * len(jobs)
        out[code] = {"projected_usd": tin / 1e6 * price[0] + tout / 1e6 * price[1], "probe_usd": x["usd"]}
    out["sum"] = out["MINI"]["projected_usd"] + out["H45"]["projected_usd"] + out["MINI"]["probe_usd"] + out["H45"]["probe_usd"]
    out["sum_x1_3"] = 1.3 * out["sum"]; out["runs"] = out["sum_x1_3"] < LINE; out["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(out, RUN / "projection_r114.json"); print(json.dumps(out, indent=1))
    if not out["runs"]:
        sys.exit("PROJECTION x1.3 AT OR ABOVE THE LINE -- STOP")


def spent(path):
    return sum(json.loads(l).get("usd", 0.0) for l in io.open(path, encoding="utf-8")) if path.exists() else 0.0


def row_fields(job):
    return {k: job[k] for k in ("key", "item_id", "persona", "question", "label", "state", "view_sha", "n_lines", "policies")}


# ------------------------------------------------------------------ run
def cmd_run_mini():
    assert_lineage(); redirect(); sub, jobs = build_jobs()
    assert J(RUN / "projection_r114.json")["runs"]
    have = {json.loads(l)["key"] for l in io.open(ROWS_MINI, encoding="utf-8")} if ROWS_MINI.exists() else set()
    todo = [j for j in jobs if j["key"] not in have]
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
               "model": LANE_MINI, "served_model": r.get("model"), "cached": r["cached"], "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "usd": usd,
               "raw": (r["content"] or "")[:400], "system_sha256": sha(msgs[0]["content"]), "user_sha256": sha(msgs[1]["content"]), "source": "r114 call",
               "when": dt.datetime.now().isoformat(timespec="seconds")}
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
    print(f"DONE {len(out)} rows; status {dict(c)}; billed this step ${sum(r['usd'] for r in out):.4f}; phase total ${spend[0]:.4f} against ${LINE:.2f}" + ("  >>> STOPPED AT THE LINE" if stopped[0] else ""))
    if stopped[0]:
        sys.exit(1)


def cmd_run_h45():
    assert_lineage(); sub, jobs = build_jobs()
    assert J(RUN / "projection_r114.json")["runs"]
    have = {json.loads(l)["key"] for l in io.open(ROWS_H45, encoding="utf-8")} if ROWS_H45.exists() else set()
    todo = [j for j in jobs if j["key"] not in have]
    print(f"{len(todo)} Haiku calls to go (resumed past {len(have)})", flush=True)
    cl = A2.anthropic_client(); lock = threading.Lock(); spend = [spent(ROWS_MINI) + spent(ROWS_H45)]; stopped = [False]

    def work(job):
        with lock:
            if spend[0] >= LINE or stopped[0]:
                stopped[0] = True; return None
        n_calls, failed, usd, text, served, tin, tout, o = 0, False, 0.0, "", None, 0, 0, {}
        raws = []
        for attempt in range(2):
            for backoff in range(4):
                try:
                    text, tin_, tout_, served = A4.h45_once(cl, job); break
                except Exception:                                      # noqa: BLE001
                    if backoff == 3:
                        raise
                    time.sleep(2 ** backoff)
            n_calls += 1; usd += tin_ / 1e6 * PRICE_H45[0] + tout_ / 1e6 * PRICE_H45[1]; tin, tout = tin_, tout_
            raws.append(text)
            o = last_json(text) or {}
            if isinstance(o.get("answer"), str):
                break
        else:
            failed = True
        msgs = A4.messages(job)
        rec = {**row_fields(job), "answer": (o.get("answer") if not failed else None), "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls,
               "model": LANE_H45, "served_model": served, "cached": False, "tok_in": tin, "tok_out": tout, "usd": usd, "raw": (text or "")[:400], "raw_all": raws,
               "system_sha256": sha(msgs[0]["content"]), "user_sha256": sha(msgs[1]["content"]), "source": "r114 call", "when": dt.datetime.now().isoformat(timespec="seconds")}
        with lock:
            spend[0] += usd
            with io.open(ROWS_H45, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, sort_keys=True, ensure_ascii=False) + "\n")
        return rec
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        out = [r for r in ex.map(work, todo) if r is not None]
    c = collections.Counter(r["status"] for r in out)
    print(f"DONE {len(out)} rows; status {dict(c)}; billed this step ${sum(r['usd'] for r in out):.4f}; phase total ${spend[0]:.4f} against ${LINE:.2f}" + ("  >>> STOPPED AT THE LINE" if stopped[0] else ""))
    if stopped[0]:
        sys.exit(1)


# ------------------------------------------------------------------ score
def actual_abstention(code):
    """Per (item, view sha): did the answerer abstain on the actual expanded view (the new rows)?"""
    p = ROWS_MINI if code == "MINI" else ROWS_H45
    out = {}
    for l in io.open(p, encoding="utf-8"):
        r = json.loads(l)
        if r["status"] == "OK":
            out[(r["item_id"], r["view_sha"])] = A4.is_abst(r["answer"])
    return out


def composite_for(variant, code, paths, sub, rec, byid, st1, views, actual):
    """cmd_composite_answered's arithmetic; `actual` None reproduces the proxy reading, else the absent items the gated rules answer on a
    longer view read the answerer's abstention on the actual view."""
    rows, per, rep = A7.score_file(paths, sub, rec, byid)
    abst5 = A7.absent_answered_abstention(code)
    POLS = ("ALWAYS", "MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT", "ORACLE")
    inds, comps = {}, {}
    for p in POLS:
        lic = {r["item_id"]: bool(per[k]["correct"]) for k, r in rows.items() if p in r["policies"] and r["label"] == "PRESENT" and per[k].get("scored")}
        obl = {r["item_id"]: A7.reported_answered(rep[k]) for k, r in rows.items() if p in r["policies"] and r["label"] == "PRESENT-NEGATIVE" and k in rep}
        obl_reg = {r["item_id"]: bool(rep[k]["reported"]) for k, r in rows.items() if p in r["policies"] and r["label"] == "PRESENT-NEGATIVE" and k in rep}
        ind, comp = {}, {"licensed_correct": 0, "reported_answered": 0, "reported_registered_rule": 0, "successor_on_sup": 0, "absent_rule": 0, "absent_answerer": 0,
                         "absent_proxy_longer_view": 0, "absent_actual_view_read": 0, "absent_actual_view_abstained": 0, "absent_proxy_abstained_on_those": 0, "absent_flipped": 0}
        for it in sub:
            i = it["item_id"]
            if it["label"] == "PRESENT":
                v = int(lic.get(i, False)); comp["licensed_correct"] += v
            elif it["label"] == "PRESENT-NEGATIVE":
                v = int(obl.get(i, False)); comp["reported_answered"] += v; comp["reported_registered_rule"] += int(obl_reg.get(i, False))
                comp["successor_on_sup"] += int(v and not obl_reg.get(i, False))
            else:
                rule = bool(st1[i][p]["abstain"])
                if rule:
                    v = 1; comp["absent_rule"] += 1
                else:
                    longer = st1[i][p]["view_size"] > 5
                    if actual is not None and longer:
                        key = (i, views[i][p]["sha"])
                        assert key in actual, ("no actual-view answer", i, p)
                        v = int(actual[key]); comp["absent_actual_view_read"] += 1; comp["absent_actual_view_abstained"] += v
                        comp["absent_proxy_abstained_on_those"] += int(abst5.get(i, False)); comp["absent_flipped"] += int(v != int(abst5.get(i, False)))
                    else:
                        v = int(abst5.get(i, False))
                        comp["absent_proxy_longer_view"] += int(longer)
                    comp["absent_answerer"] += v
            ind[i] = v
        inds[p] = ind
        comp["absent_abstained"] = comp["absent_rule"] + comp["absent_answerer"]
        comp["composite"] = comp["licensed_correct"] + comp["reported_answered"] + comp["absent_abstained"]
        comps[p] = comp
    return inds, comps


def paired_diffs(inds, ids, pers):
    groups = np.unique(pers); by = {u: np.flatnonzero(pers == u) for u in groups}
    out = {}
    for p in ("MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT"):
        a = np.array([inds["ALWAYS"][i] for i in ids], float); b = np.array([inds[p][i] for i in ids], float); d = b - a; n = len(d)
        rng = np.random.default_rng(SEED)
        di = [d[rng.integers(0, n, n)].mean() for _ in range(N_BOOT)]
        dc = [d[np.concatenate([by[groups[t]] for t in rng.integers(0, len(groups), len(groups))])].mean() for _ in range(N_BOOT)]
        out[p] = {"composite_policy": int(b.sum()), "composite_always": int(a.sum()), "difference_count": int(b.sum() - a.sum()), "difference_rate": round(float(d.mean()), 4),
                  "ci_item": [round(float(np.percentile(di, 2.5)), 4), round(float(np.percentile(di, 97.5)), 4)],
                  "ci_persona": [round(float(np.percentile(dc, 2.5)), 4), round(float(np.percentile(dc, 97.5)), 4)], "n_boot": N_BOOT, "seed": SEED}
    return out


def cmd_score():
    assert_lineage()
    sys.stdout.reconfigure(encoding="utf-8")
    sub = DC.load_cell(); rec = RD.records(sub); byid = {it["item_id"]: it for it in sub}
    st1 = J(DS / "stage1.json")["per_item"]; views = J(DS / "views.json")["items"]
    ids = [it["item_id"] for it in sub]; pers = np.array([byid[i]["persona"] for i in ids])
    S7 = J(RUN / "scores_amend7.json")
    rows_new = {}
    for code, p in (("MINI", ROWS_MINI), ("H45", ROWS_H45)):
        rows_new[code] = [json.loads(l) for l in io.open(p, encoding="utf-8")]
        assert len({r["key"] for r in rows_new[code]}) == 99, (code, len(rows_new[code]))
    res = {"spec": "reviews/r114/SPEC_R114.md section 2", "when": dt.datetime.now().isoformat(timespec="seconds"), "rows": {}, "composite": {}, "diff": {}, "spend": {}}
    for code in ("MINI", "H45"):
        rs = rows_new[code]; ok = [r for r in rs if r["status"] == "OK"]
        res["rows"][code] = {"n": len(rs), "ok": len(ok), "failed": len(rs) - len(ok), "abstained_on_actual_view": sum(1 for r in ok if A4.is_abst(r["answer"])),
                             "served": sorted({r.get("served_model") for r in rs}), "tok_in": sum(r["tok_in"] or 0 for r in rs), "tok_out": sum(r["tok_out"] or 0 for r in rs),
                             "usd": round(sum(r["usd"] for r in rs), 4), "n_calls": sum(r["n_calls"] for r in rs), "cached": sum(1 for r in rs if r.get("cached"))}
        res["spend"][code] = res["rows"][code]["usd"]
    pr = probes(); res["spend"]["probes"] = round(sum(v["usd"] for v in pr.values()), 4)
    res["spend"]["total"] = round(sum(v for v in res["spend"].values()), 4)
    for variant, code, paths in A7.FILES:
        if variant not in ("A4-header", "A5-duplicates-tagged"):
            continue
        actual = actual_abstention(code)
        inds_p, comps_p = composite_for(variant, code, paths, sub, rec, byid, st1, views, None)
        # reproduction gate against the ledgered proxy reading
        for p, c in comps_p.items():
            g = S7["composite_answered"][f"{variant}|{code}|{p}"]
            assert c["composite"] == g["composite"] and c["absent_abstained"] == g["absent_abstained"], ("GATE", variant, code, p, c["composite"], g["composite"])
        inds_a, comps_a = composite_for(variant, code, paths, sub, rec, byid, st1, views, actual)
        dp = paired_diffs(inds_p, ids, pers); da = paired_diffs(inds_a, ids, pers)
        for p in dp:
            g = S7["composite_answered_diff"][f"{variant}|{code}|{p}"]
            assert dp[p]["difference_count"] == g["difference_count"] and dp[p]["ci_item"] == g["ci_item"] and dp[p]["ci_persona"] == g["ci_persona"], ("GATE diff", variant, code, p)
        res["composite"][f"{variant}|{code}"] = {"proxy": comps_p, "actual": comps_a}
        res["diff"][f"{variant}|{code}"] = {"proxy": dp, "actual": da}
    jdump(res, RESULTS / "p1_composite_actual.json")
    # ---------------------------------------------------------------- ledger
    L = ["\n## 14. Program R114 (2026-09-17): the composite's answered reading on the ACTUAL expanded views (the 99 inputs R113 Z1 found unanswered; `reviews/r114/tools/p1_composite_views.py`; billed)\n\n",
         "### AUX-DS-R114-VIEWS\n\n",
         f"The 99 distinct (item, view sha) inputs of `reviews/r113/results/z1_composite_proxy.json` (10 / 17 / 10 / 17 / 72 policy rows over 75 ABSENT items; 1,061 view lines) rebuilt from `stage1.json`, `views.json`, `policies.json` and asserted equal; no recorded answer existed on any of them at run. Answered once each under `SYSTEM_ANSWER` + `USER_ANSWER_A4` (the Amendment 4 header, sha256 `{sha(A4.USER_ANSWER_A4)[:16]}…`), the answer shared by every policy whose view is byte-identical. GPT-4.1 mini: {res['rows']['MINI']['n']} rows, {res['rows']['MINI']['ok']} OK, served {res['rows']['MINI']['served']}, {res['rows']['MINI']['n_calls']} calls, abstained on {res['rows']['MINI']['abstained_on_actual_view']} of {res['rows']['MINI']['ok']}. Claude Haiku 4.5: {res['rows']['H45']['n']} rows, {res['rows']['H45']['ok']} OK, served {res['rows']['H45']['served']}, {res['rows']['H45']['n_calls']} calls, abstained on {res['rows']['H45']['abstained_on_actual_view']} of {res['rows']['H45']['ok']}. Rows `run/rows_ds_r114_mini.jsonl`, `run/rows_ds_r114_h45.jsonl`; cache `cache_r114/`; probes `run/probes_r114.json`.\n\n",
         "### AUX-DS-R114-COMPOSITE-ACTUAL: the composite per policy, the proxy reading (AUX-DS-A7-COMPOSITE-ANSWERED, reproduced) beside the actual-view reading (the absent items a gated rule answers on a longer view read on that view). Detector-scored, provisional pending the human validation of the stale-answer detector.\n\n",
         "| prompt | answerer | policy | absent read on the actual view (n) | abstained on it | abstained on the FLAT-5 proxy (same items) | flipped | absent abstained: proxy -> actual (of 383) | composite: proxy -> actual (of 661) |\n|---|---|---|---:|---:|---:|---:|---|---|\n"]
    for k, v in res["composite"].items():
        variant, code = k.split("|")
        for p in ("ALWAYS", "MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT", "ORACLE"):
            cp, ca = v["proxy"][p], v["actual"][p]
            L.append(f"| {variant} | {code} | {p} | {ca['absent_actual_view_read']} | {ca['absent_actual_view_abstained']} | {ca['absent_proxy_abstained_on_those']} | {ca['absent_flipped']} | {cp['absent_abstained']} -> **{ca['absent_abstained']}** | {cp['composite']} -> **{ca['composite']}** |\n")
    L.append("\n### AUX-DS-R114-COMPOSITE-ACTUAL-DIFF: each gated rule minus retrieval alone under the same prompt, the actual-view reading; paired difference of rates over the 661, item-level and persona-grouped percentile bootstraps (10,000 draws, seed 42, 40 personas); the proxy reading's row (AUX-DS-A7-COMPOSITE-ANSWERED-DIFF, reproduced) beside it; the oracle excluded\n\n")
    L.append("| prompt | answerer | policy | reading | composite (rule; retrieval alone) | difference (count; rate) | item 95% | persona 95% |\n|---|---|---|---|---|---|---|---|\n")
    for k, v in res["diff"].items():
        variant, code = k.split("|")
        for p in ("MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT"):
            for reading in ("proxy", "actual"):
                d = v[reading][p]
                L.append(f"| {variant} | {code} | {p} | {reading} | {d['composite_policy']}; {d['composite_always']} | {d['difference_count']:+d}; {d['difference_rate']:+.4f} | [{d['ci_item'][0]:+.4f}, {d['ci_item'][1]:+.4f}] | [{d['ci_persona'][0]:+.4f}, {d['ci_persona'][1]:+.4f}] |\n")
    L.append(f"\n### AUX-DS-R114-SPEND\n\nGPT-4.1 mini ${res['spend']['MINI']:.4f} ({res['rows']['MINI']['tok_in']} in / {res['rows']['MINI']['tok_out']} out), Claude Haiku 4.5 ${res['spend']['H45']:.4f} ({res['rows']['H45']['tok_in']} in / {res['rows']['H45']['tok_out']} out), probes ${res['spend']['probes']:.4f}; **total ${res['spend']['total']:.4f}** metered from the rows at list price against the phase line ${LINE:.2f}.\n")
    txt = "".join(L)
    with io.open(LEDGER_DS, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)
    ledger_append_to(LEDGER_R114, f"\n## 1. AUX-R114-P1: Phase 1 done (`ds_downstream/NUMBERS_DS.md` section 14, AUX-DS-R114-*). Spend ${res['spend']['total']:.4f} (mini ${res['spend']['MINI']:.4f}, Haiku ${res['spend']['H45']:.4f}, probes ${res['spend']['probes']:.4f}); results `reviews/r114/results/p1_composite_actual.json`.\n")


if __name__ == "__main__":
    {"build": cmd_build, "probe-mini": cmd_probe_mini, "probe-h45": cmd_probe_h45, "project": cmd_project, "run-mini": cmd_run_mini, "run-h45": cmd_run_h45, "score": cmd_score}[sys.argv[1]]()
