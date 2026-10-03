# -*- coding: utf-8 -*-
"""amend8_propagate.py -- ADDENDUM_DS Amendment 8 (E4, program R117): label propagation inside the view.

The rule (the registration's section 3, the author's ruling of 2026-09-19): within one assembled view, a tagged line s (superseded /
retracted / expired) propagates its tag to an untagged line u of the same attribute when the census function fires -- index_v2.detect
(old_fact = s.text, new_fact = m.text, MIN_SHARED 2, CROSS_GUARD 0.34, TAU_HI 0.80, MIN_DISCR 3), m being the newest active line of the
attribute whose text does not repeat s's at the census threshold; where no m exists, D_old = toks(s), D_new = empty, the cross guard vacuous
-- and the ordering holds on the age field: where m exists u must be older than m (age_u > age_m); where none, u must be no newer than s
(age_u >= age_s). The tag propagated is s's; two tagged lines matching u: the younger s wins. One pass, no chaining. The secondary arm is the
same rule without the ordering condition (offline only). Two tag sources: the recorded ground-truth tags (views.json) and FR-Bank's own
tags (each line's lifecycle field re-rendered from the store's own marks, resp_review amend1_resp.believed_flags). Three policies of
Table 4: ALWAYS (top-five retrieval), MODEL (the model rule), ORACLE. Re-answers: every view the primary rule changed, GPT-4.1 mini and
Haiku 4.5 once, under the Amendment 4 header and prompt texts; under own tags the unpropagated own-tag view is answered too (the before).
Registration registrations/ADDENDUM_DS_AMENDMENT_8.md, registered-text sha256 c57cda87..., frozen at 177697a. Cap 5 USD.

Subcommands:  lock | probe_mini | probe_h45 | project | run_mini | run_h45 | score
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
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ds_common as DC                                                       # noqa: E402
from ds_common import ROOT, DS, RUN, J, jdump                                # noqa: E402
import run_ds as RD                                                          # noqa: E402
import prompts_ds as PD                                                      # noqa: E402
import prompts_e1 as P                                                       # noqa: E402
import amend2_lit as A2                                                      # noqa: E402
import amend4_header as A4                                                   # noqa: E402
from resp_common import lifecycle_tag, true_flags                            # noqa: E402
from e0_common import toks, cov, MIN_SHARED, CROSS_GUARD, MIN_DISCR         # noqa: E402
from index_v2 import detect, TAU_HI                                          # noqa: E402
sys.path.insert(0, str(ROOT / "resp_review" / "tools"))
import amend1_resp as AR                                                     # noqa: E402
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
from run_cf import last_json                                                 # noqa: E402

api = A4.api
REG = ROOT / "registrations" / "ADDENDUM_DS_AMENDMENT_8.md"
REG_SHA = "c57cda878aa80df7902e4ae35fc49504483a27a3032497a76e1c3b2e8050502c"
FROZEN_AT = "177697a"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
CACHE8 = DS / "cache_amend8"
CAP = 5.00
LANE_MINI, PRICE_MINI = A4.LANE_MINI, A4.PRICE_MINI
LANE_H45, PRICE_H45 = A4.LANE_H45, A4.PRICE_H45
ROWS_MINI = RUN / "rows_ds_amend8_mini.jsonl"
ROWS_H45 = RUN / "rows_ds_amend8_h45.jsonl"
VIEWS8 = RUN / "views_amend8.json"
LOCK8 = RUN / "lock_amend8.json"
LEDGER = DS / "NUMBERS_DS.md"
ARM = "ANSWER-A8"
POLS = ("ALWAYS", "MODEL", "ORACLE")
SOURCES = ("gt", "own")
AUDIT = ROOT / "reviews" / "downstream_audit" / "step4b_view_lines.json"
TAGGED = ("superseded", "retracted", "expired")


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def registration_ok():
    b = REG.read_bytes(); i = b.find(FROZEN_END)
    return i > 0 and hashlib.sha256(b[:i]).hexdigest() == REG_SHA


def assert_lineage():
    assert registration_ok(), "ADDENDUM_DS_AMENDMENT_8.md frozen bytes sha256 != c57cda87 -- STOP"
    lk4 = J(RUN / "lock_amend4.json")
    assert sha(A4.USER_ANSWER_A4) == lk4["user_answer_a4_sha256"] and sha(A4.HEADER) == lk4["header_sha256"], "the Amendment 4 header differs -- STOP"
    assert PD.digests() == lk4["prompts_ds"] and P.file_sha256() == lk4["prompts_e1"]["file"] and P.texts_sha256() == lk4["prompts_e1"]["texts"], "prompt digests differ -- STOP"
    A4.RD.assert_lineage()


def redirect():
    CACHE8.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                             # noqa: SLF001
    e0.CACHE_PATH = CACHE8 / "responses.json"; e0.LEDGER_PATH = CACHE8 / "cost_ledger.json"
    e0._cache = None; e0._load_cache()                                       # noqa: SLF001
    e0.HARD_CAP_USD = CAP
    return e0


# ------------------------------------------------------------------ the view lines
def parse(view_text):
    out = []
    for ln in view_text.split("\n"):
        m = A4.LINE_RE.match(ln); assert m, ("unparsed view line", ln[:80])
        age = m.group(5)
        out.append({"rank": int(m.group(1)), "tag": m.group(2), "category": m.group(3), "attribute": m.group(4), "age_s": age,
                    "age": (int(age.split()[0]) if age != "unknown" else None), "text": m.group(6)})
    return out


def render(lines):
    return "\n".join(f"[{l['rank']}] lifecycle: {l['tag']} | category: {l['category']} | attribute: {l['attribute']} | age: {l['age_s']} | text: {l['text']}" for l in lines)


def propagate(view_text, drop, ordered=True):
    """-> (new view text, {rank: (tag, from_rank)}, diagnostics). The registered rule; ordered=False is the secondary arm."""
    L = parse(view_text)
    tagged = [l for l in L if l["tag"] != "active"]
    active = [l for l in L if l["tag"] == "active"]
    tk = {l["rank"]: toks(l["text"], drop) for l in L}
    prop = {}                                                        # rank -> (tag, source rank, source age)
    diag = {"unresolvable_pairs": 0, "unknown_age": 0}
    for s in tagged:
        same = [u for u in active if u["attribute"] == s["attribute"]]
        if not same:
            continue
        cand = [u for u in same if cov(tk[s["rank"]], tk[u["rank"]]) < TAU_HI]
        cand = [u for u in cand if u["age"] is not None] if ordered else cand
        m = min(cand, key=lambda u: u["age"] if u["age"] is not None else 10 ** 9) if cand else None
        etoks = {u["rank"]: tk[u["rank"]] for u in same}
        if m is not None:
            d = detect(s["text"], m["text"], etoks, drop)
            if d is None:
                diag["unresolvable_pairs"] += 1; continue
            fires = {r for r, c in d.items() if c >= TAU_HI}
        else:
            do = tk[s["rank"]]
            if len(do) < MIN_DISCR:
                diag["unresolvable_pairs"] += 1; continue
            fires = {u["rank"] for u in same if len(do & tk[u["rank"]]) >= MIN_SHARED and cov(do, tk[u["rank"]]) >= TAU_HI}
        for u in same:
            if u["rank"] not in fires:
                continue
            if ordered:
                if u["age"] is None:
                    diag["unknown_age"] += 1; continue
                if m is not None and not (u["age"] > m["age"]):
                    continue
                if m is None and s["age"] is not None and not (u["age"] >= s["age"]):
                    continue
            prev = prop.get(u["rank"])
            s_age = s["age"] if s["age"] is not None else 10 ** 9
            if prev is None or s_age < prev[2]:
                prop[u["rank"]] = (s["tag"], s["rank"], s_age)
    new = [dict(l, tag=prop[l["rank"]][0]) if l["rank"] in prop else l for l in L]
    text = render(new)
    # RENDERER LOCK: same line count, only the lifecycle field of the propagated lines differs; a second pass changes nothing
    a, c = view_text.split("\n"), text.split("\n"); assert len(a) == len(c)
    for x, y_ in zip(a, c):
        if x != y_:
            mx, my = A4.LINE_RE.match(x), A4.LINE_RE.match(y_)
            assert mx.group(2) == "active" and all(mx.group(k) == my.group(k) for k in (1, 3, 4, 5, 6)), "lock: a field outside the lifecycle tag differs"
    return text, {r: (t, fr) for r, (t, fr, _) in prop.items()}, diag


def idempotent(text, drop, ordered):
    t2, p2, _ = propagate(text, drop, ordered)
    return t2 == text and not p2


# ------------------------------------------------------------------ the own-tag views
def own_view(job, ids, bf):
    L = parse(job["view"]); assert len(L) == len(ids), (job["key"], len(L), len(ids))
    out = []
    for l, eid in zip(L, ids):
        f = bf[job["persona"]][eid]
        out.append(dict(l, tag=lifecycle_tag(f)))
    return render(out)


def build_views():
    """Every job (452 views) under both tag sources and both arms; measures (i) and (ii); the re-answer jobs."""
    sub, hj = A4.jobs(); rec = RD.records(sub); byid = {it["item_id"]: it for it in sub}
    views = J(DS / "views.json")["items"]; audit = J(AUDIT)["view_lines"]
    tf = true_flags(); bf = AR.believed_flags(); pf = A4.persona_fields()
    out = {}; census = {s: {a: collections.Counter() for a in ("primary", "secondary")} for s in SOURCES}
    n_gt_lock = 0
    for j in hj:
        per = j["persona"]; drop = toks(pf[per][0])
        ids = views[j["item_id"]][j["policies"][0]]["ids"]
        for pol in j["policies"]:
            assert views[j["item_id"]][pol]["ids"] == ids and views[j["item_id"]][pol]["sha"] == j["view_sha"]
        # lock: the recorded ground-truth view's tags reproduce from the true flags
        for l, eid in zip(parse(j["view"]), ids):
            assert l["tag"] == lifecycle_tag(tf[per][eid]), ("gt lock", j["key"], l["rank"]); n_gt_lock += 1
        src_views = {"gt": j["view"], "own": own_view(j, ids, bf)}
        entry = {"item_id": j["item_id"], "persona": per, "question": j["question"], "label": j["label"], "state": j["state"], "policies": j["policies"],
                 "policies_t4": [p for p in j["policies"] if p in POLS], "n_lines": j["n_lines"], "key_a4": j["key"], "view_sha_a4": j["view_sha"], "ids": ids, "sources": {}}
        for s in SOURCES:
            base = src_views[s]
            arms = {}
            for arm, ordered in (("primary", True), ("secondary", False)):
                new, prop, diag = propagate(base, drop, ordered)
                # D-DS-A8-1: the registration's "reproduces itself on a second pass" lock contradicts its own one-pass rule (a second pass is
                # chaining from newly tagged lines, which section 3 forbids); the one-pass definition governs, and the views a second pass
                # would change are counted here as a diagnostic, never applied.
                diag["second_pass_would_change"] = not idempotent(new, drop, ordered)
                arms[arm] = {"changed": bool(prop), "n_lines_propagated": len(prop), "propagated": {str(r): list(v) for r, v in prop.items()}, "view_sha": sha(new)[:16], "diag": diag}
                if arm == "primary":
                    arms[arm]["view"] = new
                c = census[s][arm]; c["views"] += 1; c["changed"] += int(bool(prop)); c["lines"] += len(prop)
                c["second_pass_would_change"] += int(diag["second_pass_would_change"]); c["unresolvable_pairs"] += diag["unresolvable_pairs"]; c["unknown_age"] += diag["unknown_age"]
                for pol in entry["policies_t4"]:
                    c[f"changed_{pol}"] += int(bool(prop))
            entry["sources"][s] = {"before_view": base, "before_sha": sha(base)[:16], "arms": arms,
                                   "tags_before": collections.Counter(l["tag"] for l in parse(base))}
        out[j["key"]] = entry
    # (i) the 35 audited duplicate views
    dup = {}
    for s in SOURCES:
        for arm in ("primary", "secondary"):
            per_item = collections.defaultdict(list); per_item_t4 = collections.defaultdict(list); n_views = n_full = n_views_t4 = n_full_t4 = 0
            for e in out.values():                                   # job -> audit, as Amendment 5 mapped it (35 items, 74 view instances)
                text = e["sources"][s]["arms"][arm]["view"] if arm == "primary" else propagate(e["sources"][s]["before_view"], toks(pf[e["persona"]][0]), ordered=False)[0]
                tags = {l["rank"]: l["tag"] for l in parse(text)}
                for pol in e["policies"]:
                    ref = audit.get(f"{e['item_id']}|{pol}")
                    if not ref or not ref["active_stale"]:
                        continue
                    full = all(tags[r] != "active" for r in ref["active_stale"])
                    n_views += 1; n_full += int(full); per_item[e["item_id"]].append(full)
                    if pol in POLS:
                        n_views_t4 += 1; n_full_t4 += int(full); per_item_t4[e["item_id"]].append(full)
            dup[f"{s}/{arm}"] = {"views": n_views, "views_fully_tagged": n_full, "items": len(per_item), "items_fully_tagged": sum(1 for v in per_item.values() if all(v)),
                                 "t4_views": n_views_t4, "t4_views_fully_tagged": n_full_t4, "t4_items": len(per_item_t4), "t4_items_fully_tagged": sum(1 for v in per_item_t4.values() if all(v))}
    # (ii) false propagation on the licensed items' views: lines active in the ground-truth view that the rule tags
    fp = {}
    for s in SOURCES:
        for arm in ("primary", "secondary"):
            n_act = n_fp = 0; inst = 0
            for e in out.values():
                if e["label"] != "PRESENT":
                    continue
                gt_tags = {l["rank"]: l["tag"] for l in parse(e["sources"]["gt"]["before_view"])}
                prop = e["sources"][s]["arms"][arm]["propagated"]
                for pol in e["policies_t4"]:
                    inst += 1
                    act = [r for r, t in gt_tags.items() if t == "active"]
                    n_act += len(act); n_fp += sum(1 for r in act if str(r) in prop)
            fp[f"{s}/{arm}"] = {"view_instances": inst, "active_lines_gt": n_act, "false_propagations": n_fp, "share": round(n_fp / n_act, 4) if n_act else None}
    # the re-answer jobs (primary arm): gt after; own before and after; only views serving a Table 4 policy
    jobs = []
    for k, e in out.items():
        if not e["policies_t4"]:
            continue
        for s in SOURCES:
            a = e["sources"][s]["arms"]["primary"]
            if not a["changed"]:
                continue
            if s == "own":
                jobs.append({"key": f"{e['item_id']}|{e['sources']['own']['before_sha']}", "key_a4": k, "source": "own", "stage": "before", "view": e["sources"]["own"]["before_view"], "view_sha": e["sources"]["own"]["before_sha"],
                             **{f: e[f] for f in ("item_id", "persona", "question", "label", "state", "policies", "policies_t4", "n_lines")}})
            jobs.append({"key": f"{e['item_id']}|{a['view_sha']}", "key_a4": k, "source": s, "stage": "after", "view": a["view"], "view_sha": a["view_sha"],
                         **{f: e[f] for f in ("item_id", "persona", "question", "label", "state", "policies", "policies_t4", "n_lines")}})
    seen = set(); uniq = []
    for jb in jobs:
        if (jb["key"], jb["source"], jb["stage"]) in seen:
            continue
        seen.add((jb["key"], jb["source"], jb["stage"])); uniq.append(jb)
    return sub, out, {s: {a: dict(c) for a, c in d.items()} for s, d in census.items()}, dup, fp, uniq, n_gt_lock


def cmd_lock():
    assert_lineage()
    sub, out, census, dup, fp, jobs, n_gt_lock = build_views()
    jdump({"registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "views": out, "census": census, "dup35": dup, "false_propagation": fp, "jobs": jobs}, VIEWS8)
    rec = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "header_sha256": sha(A4.HEADER), "user_answer_a4_sha256": sha(A4.USER_ANSWER_A4),
           "prompts_ds": PD.digests(), "prompts_e1": {"file": P.file_sha256(), "texts": P.texts_sha256()}, "rule": "amend8_propagate.propagate (the registration's section 3; secondary arm ordered=False)",
           "constants": {"MIN_SHARED": MIN_SHARED, "CROSS_GUARD": CROSS_GUARD, "TAU_HI": TAU_HI, "MIN_DISCR": MIN_DISCR}, "gt_tag_lock_lines": n_gt_lock, "census": census, "dup35": dup, "false_propagation": fp,
           "reanswer_jobs": {"n": len(jobs), "by_source_stage": dict(collections.Counter(f"{j['source']}/{j['stage']}" for j in jobs))}, "cap_usd": CAP, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(rec, LOCK8)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"\n## 15. DS Amendment 8: label propagation inside the view (registrations/ADDENDUM_DS_AMENDMENT_8.md; E4, program R117)\n\n"
                f"### AUX-DS-A8-REG, AUX-DS-A8-LOCK (written {dt.date.today().isoformat()}, before the first call)\n\n"
                f"Registered text sha256 `{REG_SHA}`, frozen at `{FROZEN_AT}`; the Amendment 4 header and prompt digests reproduce AUX-DS-A4-LOCK; the rule is `tools/amend8_propagate.py propagate` with the census constants unchanged "
                f"(MIN_SHARED {MIN_SHARED}, CROSS_GUARD {CROSS_GUARD}, TAU_HI {TAU_HI}, MIN_DISCR {MIN_DISCR}); the ground-truth views' tags reproduce from the true flags on {n_gt_lock} lines; the own-tag views re-render each line's lifecycle field from FR-Bank's own marks (resp_review amend1 believed_flags).\n\n"
                f"### AUX-DS-A8-RULE-CENSUS\n\n`{json.dumps(census)}`\n\n### AUX-DS-A8-DUP35\n\n`{json.dumps(dup)}`\n\n### AUX-DS-A8-FALSEPROP\n\n`{json.dumps(fp)}`\n\n"
                f"Re-answer jobs (the primary arm; views serving ALWAYS, MODEL or ORACLE): {len(jobs)} = {dict(collections.Counter(f'{j['source']}/{j['stage']}' for j in jobs))}.\n")
    print(json.dumps({"census": census, "dup35": dup, "false_propagation": fp, "jobs": rec["reanswer_jobs"]}, indent=1))


def jobs8():
    return J(VIEWS8)["jobs"]


def spent(path):
    return sum(json.loads(l).get("usd", 0.0) for l in io.open(path, encoding="utf-8")) if path.exists() else 0.0


def cmd_probe_mini():
    assert_lineage(); redirect(); j = jobs8()[0]
    r = api.call(j["key"], ARM + "#probe", A4.messages(j)); o = api.parse_json(r["content"]) or {}
    rec = {"lane": LANE_MINI, "served": r.get("model"), "identifier_ok": str(r.get("model", "")).startswith("gpt-4.1-mini"), "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"),
           "usd": r.get("prompt_tokens", 0) / 1e6 * PRICE_MINI[0] + r.get("completion_tokens", 0) / 1e6 * PRICE_MINI[1], "parsed": isinstance(o.get("answer"), str), "when": dt.datetime.now().isoformat(timespec="seconds")}
    api.flush()
    d = J(RUN / "probes_amend8.json") if (RUN / "probes_amend8.json").exists() else {}
    d["MINI"] = rec; jdump(d, RUN / "probes_amend8.json"); print(json.dumps(rec, indent=1))
    assert rec["identifier_ok"], "IDENTIFIER MISMATCH -- STOP"


def cmd_probe_h45():
    assert_lineage(); j = jobs8()[0]; cl = A2.anthropic_client()
    text, tin, tout, served = A4.h45_once(cl, j); o = last_json(text) or {}
    rec = {"lane": LANE_H45, "served": served, "identifier_ok": LANE_H45 in served, "tok_in": tin, "tok_out": tout, "usd": tin / 1e6 * PRICE_H45[0] + tout / 1e6 * PRICE_H45[1],
           "parsed": isinstance(o.get("answer"), str), "when": dt.datetime.now().isoformat(timespec="seconds")}
    d = J(RUN / "probes_amend8.json") if (RUN / "probes_amend8.json").exists() else {}
    d["H45"] = rec; jdump(d, RUN / "probes_amend8.json"); print(json.dumps(rec, indent=1))
    assert rec["identifier_ok"], "IDENTIFIER MISMATCH -- STOP"


def cmd_project():
    pr = J(RUN / "probes_amend8.json"); n = len(jobs8())
    mini = n * pr["MINI"]["usd"]; h45 = n * pr["H45"]["usd"]; tot = mini + h45 + pr["MINI"]["usd"] + pr["H45"]["usd"]
    rec = {"jobs": n, "mini_usd": round(mini, 4), "h45_usd": round(h45, 4), "total_usd": round(tot, 4), "x1_3": round(tot * 1.3, 4), "cap": CAP, "runs": tot * 1.3 <= CAP}
    jdump(rec, RUN / "projection_amend8.json"); print(json.dumps(rec, indent=1))
    assert rec["runs"], "PROJECTION OVER THE CAP -- STOP"


def row_fields(job):
    return {k: job[k] for k in ("key", "key_a4", "source", "stage", "item_id", "persona", "question", "label", "state", "view_sha", "n_lines", "policies", "policies_t4")}


def cmd_run_mini():
    assert_lineage(); redirect(); assert J(RUN / "projection_amend8.json")["runs"]
    have = {(json.loads(l)["key"], json.loads(l)["source"], json.loads(l)["stage"]) for l in io.open(ROWS_MINI, encoding="utf-8")} if ROWS_MINI.exists() else set()
    todo = [j for j in jobs8() if (j["key"], j["source"], j["stage"]) not in have]
    print(f"{len(todo)} mini calls to go", flush=True)
    lock = threading.Lock(); spend = [spent(ROWS_MINI) + spent(ROWS_H45)]

    def work(job):
        msgs = A4.messages(job)
        ok = lambda o: o is not None and isinstance(o.get("answer"), str)     # noqa: E731
        r = api.call(job["key"], ARM, msgs); o = api.parse_json(r["content"]); n_calls, failed = 1, False
        usd = 0.0 if r["cached"] else r["prompt_tokens"] / 1e6 * PRICE_MINI[0] + r["completion_tokens"] / 1e6 * PRICE_MINI[1]
        if not ok(o):
            r2 = api.call(job["key"], ARM + "#retry", msgs); o = api.parse_json(r2["content"]); n_calls = 2
            usd += 0.0 if r2["cached"] else r2["prompt_tokens"] / 1e6 * PRICE_MINI[0] + r2["completion_tokens"] / 1e6 * PRICE_MINI[1]; r = r2
            if not ok(o):
                failed, o = True, {}
        rec = {**row_fields(job), "answer": (o.get("answer") if not failed else None), "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls, "model": LANE_MINI,
               "cached": r["cached"], "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "usd": usd, "raw": (r["content"] or "")[:400]}
        with lock:
            spend[0] += usd; assert spend[0] <= CAP, "CAP"
            with io.open(ROWS_MINI, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, sort_keys=True, ensure_ascii=False) + "\n")
        return rec
    try:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            out = list(ex.map(work, todo))
    finally:
        api.flush()
    print(f"DONE {len(out)} rows; status {dict(collections.Counter(r['status'] for r in out))}; spend ${spend[0]:.4f}", flush=True)


def cmd_run_h45():
    assert_lineage(); assert J(RUN / "projection_amend8.json")["runs"]
    have = {(json.loads(l)["key"], json.loads(l)["source"], json.loads(l)["stage"]) for l in io.open(ROWS_H45, encoding="utf-8")} if ROWS_H45.exists() else set()
    todo = [j for j in jobs8() if (j["key"], j["source"], j["stage"]) not in have]
    print(f"{len(todo)} Haiku calls to go", flush=True)
    cl = A2.anthropic_client(); lock = threading.Lock(); spend = [spent(ROWS_MINI) + spent(ROWS_H45)]

    def work(job):
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
        rec = {**row_fields(job), "answer": (o.get("answer") if not failed else None), "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls, "model": LANE_H45,
               "served_model": served, "cached": False, "tok_in": tin, "tok_out": tout, "usd": usd, "raw": (text or "")[:400]}
        with lock:
            spend[0] += usd; assert spend[0] <= CAP, "CAP"
            with io.open(ROWS_H45, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, sort_keys=True, ensure_ascii=False) + "\n")
        return rec
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        out = list(ex.map(work, todo))
    print(f"DONE {len(out)} rows; status {dict(collections.Counter(r['status'] for r in out))}; spend ${spend[0]:.4f}", flush=True)


# ------------------------------------------------------------------ scoring
def boot_dd(before_a, after_a, pers_a, before_b, after_b, pers_b, n_boot=A4.N_BOOT, seed=A4.SEED):
    """Difference of two rate reductions (a minus b), persona-grouped percentile bootstrap: personas resampled, each rate recomputed."""
    rng = np.random.default_rng(seed)
    A = collections.defaultdict(lambda: [0, 0, 0]); B = collections.defaultdict(lambda: [0, 0, 0])
    for b_, a_, p in zip(before_a, after_a, pers_a):
        A[p][0] += b_; A[p][1] += a_; A[p][2] += 1
    for b_, a_, p in zip(before_b, after_b, pers_b):
        B[p][0] += b_; B[p][1] += a_; B[p][2] += 1
    keys = sorted(set(A) | set(B)); G = len(keys)

    def red(D, pick):
        b = sum(D[keys[g]][0] for g in pick if keys[g] in D); a = sum(D[keys[g]][1] for g in pick if keys[g] in D); n = sum(D[keys[g]][2] for g in pick if keys[g] in D)
        return (b - a) / n if n else 0.0
    point = red(A, range(G)) - red(B, range(G))
    draws = np.empty(n_boot)
    for t in range(n_boot):
        pick = rng.integers(0, G, size=G); draws[t] = red(A, pick) - red(B, pick)
    return {"delta": round(float(point), 4), "cluster": [round(float(np.percentile(draws, 2.5)), 4), round(float(np.percentile(draws, 97.5)), 4)], "n_clusters": G, "n_boot": n_boot, "seed": seed}


def cmd_score():
    sys.stdout.reconfigure(encoding="utf-8"); assert registration_ok()
    sub = DC.load_cell(); rec = RD.records(sub); byid = {it["item_id"]: it for it in sub}
    V = J(VIEWS8); lk = J(LOCK8); s4 = J(RUN / "scores_amend4.json")
    S = {"registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "lock": {k: lk[k] for k in ("census", "dup35", "false_propagation", "gt_tag_lock_lines", "reanswer_jobs")}, "answerers": {}}
    # P-L1, P-L2, P-L5 from the lock (offline)
    d = lk["dup35"]["gt/primary"]; f_gt = lk["false_propagation"]["gt/primary"]; f_own = lk["false_propagation"]["own/primary"]
    S["P-L1"] = {"items_fully_tagged": d["items_fully_tagged"], "of": d["items"], "holds": d["items_fully_tagged"] >= 18,
                 "text": (f"P-L1 HOLDS: {d['items_fully_tagged']} of 35 duplicate views are fully tagged by propagation under ground-truth tags." if d["items_fully_tagged"] >= 18 else f"P-L1 FAILS: {d['items_fully_tagged']} of 35 duplicate views are fully tagged by propagation.")}
    S["P-L2"] = {"share": f_gt["share"], "holds": f_gt["share"] is not None and f_gt["share"] <= 0.05,
                 "text": (f"P-L2 HOLDS: propagation tags {100*f_gt['share']:.2f}% of the licensed items' active lines under ground-truth tags." if f_gt["share"] <= 0.05 else f"P-L2 FAILS: propagation tags {100*f_gt['share']:.2f}% of the licensed items' active lines under ground-truth tags.")}
    S["P-L5"] = {"share": f_own["share"], "holds": f_own["share"] is not None and f_own["share"] > 0.05,
                 "text": (f"P-L5 HOLDS: under the store's own tags false propagation is {100*f_own['share']:.2f}%, over 5%." if f_own["share"] > 0.05 else f"P-L5 FAILS: under the store's own tags false propagation is {100*f_own['share']:.2f}%, at or under 5%.")}
    for code, path, name in (("MINI", ROWS_MINI, "GPT-4.1 mini"), ("H45", ROWS_H45, "Claude Haiku 4.5")):
        if not path.exists():
            continue
        rows = {}
        for l in io.open(path, encoding="utf-8"):
            r = json.loads(l); rows[(r["key_a4"], r["source"], r["stage"])] = r
        per = {}
        for k, r in rows.items():
            it = byid[r["item_id"]]
            per[k] = ({"status": r["status"], "scored": False} if r["status"] != "OK" or rec.get(r["item_id"]) is None else {"status": "OK", "scored": True, **RD.score_answer(it, rec[r["item_id"]], r["answer"])})
        p4 = s4["per_row"][code]; a4rows = {}
        for l in io.open(RUN / f"rows_ds_amend4_{code.lower()}.jsonl", encoding="utf-8"):
            r = json.loads(l); a4rows[r["key"]] = r
        R = {"rows": len(rows), "failed": sum(1 for r in rows.values() if r["status"] != "OK"), "served": sorted({str(r.get("served_model") or r.get("model")) for r in rows.values()}), "by_source_policy": {}}
        for src in SOURCES:
            for pol in POLS + ("all",):
                keys = [k for (k, s_, st) in rows if s_ == src and st == "after" and (pol == "all" or pol in V["views"][k]["policies_t4"])]
                keys = sorted(set(keys))
                obl = [k for k in keys if V["views"][k]["label"] == "PRESENT-NEGATIVE"]; lic = [k for k in keys if V["views"][k]["label"] == "PRESENT"]
                def before(k):
                    return p4[k] if src == "gt" else per.get((k, "own", "before"), {})
                b_st = [int(bool(before(k).get("stale_use_tau_gold"))) for k in obl]; a_st = [int(bool(per[(k, src, "after")].get("stale_use_tau_gold"))) for k in obl]
                b_hi = sum(int(bool(before(k).get("stale_use"))) for k in obl); a_hi = sum(int(bool(per[(k, src, "after")].get("stale_use"))) for k in obl)
                b_c = sum(int(bool(before(k).get("correct"))) for k in lic); a_c = sum(int(bool(per[(k, src, "after")].get("correct"))) for k in lic)
                ans_b = [k for k in obl if not A4.is_abst((a4rows.get(k) if src == "gt" else rows.get((k, "own", "before"), {})).get("answer") if (a4rows.get(k) if src == "gt" else rows.get((k, "own", "before"))) else None)]
                ans_a = [k for k in obl if not A4.is_abst(rows[(k, src, "after")].get("answer"))]
                bp = A4.boot_paired(b_st, a_st, [V["views"][k]["persona"] for k in obl]) if obl else None
                R["by_source_policy"][f"{src}/{pol}"] = {"views": len(keys), "obligation_views": len(obl), "licensed_views": len(lic), "stale_gold_before": sum(b_st), "stale_gold_after": sum(a_st),
                                                         "answered_before": len(ans_b), "answered_after": len(ans_a),
                                                         "stale_rate_before": round(sum(b_st) / len(ans_b), 4) if ans_b else None, "stale_rate_after": round(sum(a_st) / len(ans_a), 4) if ans_a else None,
                                                         "stale_hi_before": b_hi, "stale_hi_after": a_hi, "correct_before": b_c, "correct_after": a_c, "paired_stale_gold": bp}
        S["answerers"][code] = R
    # P-L3 and P-L4 on GPT-4.1 mini, ground-truth tags
    M = S["answerers"].get("MINI", {}).get("by_source_policy", {})
    if "gt/MODEL" in M and M["gt/MODEL"]["stale_rate_before"]:
        m = M["gt/MODEL"]; r0, r1 = m["stale_rate_before"], m["stale_rate_after"]
        S["P-L3"] = {"rate_before": r0, "rate_after": r1, "holds": r1 <= 0.5 * r0, "text": (f"P-L3 HOLDS: under the model rule the flagged stale rate moves from {r0:.4f} to {r1:.4f}." if r1 <= 0.5 * r0 else f"P-L3 FAILS: under the model rule the flagged stale rate moves from {r0:.4f} to {r1:.4f}.")}
        rows_m = {}
        for l in io.open(ROWS_MINI, encoding="utf-8"):
            r = json.loads(l); rows_m[(r["key_a4"], r["source"], r["stage"])] = r
        p4 = s4["per_row"]["MINI"]
        def series(pol):
            keys = sorted({k for (k, s_, st) in rows_m if s_ == "gt" and st == "after" and pol in V["views"][k]["policies_t4"] and V["views"][k]["label"] == "PRESENT-NEGATIVE"})
            per = {k: RD.score_answer(byid[V["views"][k]["item_id"]], rec[V["views"][k]["item_id"]], rows_m[(k, "gt", "after")]["answer"]) if rows_m[(k, "gt", "after")]["status"] == "OK" else {} for k in keys}
            return [int(bool(p4[k].get("stale_use_tau_gold"))) for k in keys], [int(bool(per[k].get("stale_use_tau_gold"))) for k in keys], [V["views"][k]["persona"] for k in keys]
        bm, am, pm = series("MODEL"); ba, aa, pa = series("ALWAYS")
        dd = boot_dd(bm, am, pm, ba, aa, pa)
        S["P-L4"] = {**dd, "reduction_model": round((sum(bm) - sum(am)) / len(bm), 4) if bm else None, "reduction_always": round((sum(ba) - sum(aa)) / len(ba), 4) if ba else None,
                     "descriptive": not (dd["cluster"][0] > 0 or dd["cluster"][1] < 0), "holds": dd["delta"] > 0 and dd["cluster"][0] > 0,
                     "text": f"P-L4: the reduction under the model rule minus the reduction under top-five retrieval is {dd['delta']:+.4f}, persona-grouped interval [{dd['cluster'][0]:+.4f}, {dd['cluster'][1]:+.4f}]" + (" (includes zero: descriptive)." if not (dd["cluster"][0] > 0 or dd["cluster"][1] < 0) else (" HOLDS." if dd["delta"] > 0 and dd["cluster"][0] > 0 else " FAILS."))}
    S["spend"] = {"mini": round(spent(ROWS_MINI), 4), "h45": round(spent(ROWS_H45), 4), "probes": J(RUN / "probes_amend8.json"), "cap": CAP}
    S["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(S, RUN / "scores_amend8.json")
    txt = [f"\n### AUX-DS-A8-STAGE2 (scored {dt.date.today().isoformat()}; `run/scores_amend8.json`)\n"]
    for code, R in S["answerers"].items():
        txt.append(f"\n**{code}** ({R['rows']} rows, {R['failed']} failed, served {R['served']}):\n\n| source / policy | views | obligation views | stale at 0.50 before -> after | answered before -> after | stale rate before -> after | stale at 0.80 before -> after | correct licensed before -> after | paired (item; persona) |\n|---|---:|---:|---|---|---|---|---|---|")
        for k, v in R["by_source_policy"].items():
            bp = v["paired_stale_gold"]
            txt.append(f"| {k} | {v['views']} | {v['obligation_views']} | {v['stale_gold_before']} -> {v['stale_gold_after']} | {v['answered_before']} -> {v['answered_after']} | {v['stale_rate_before']} -> {v['stale_rate_after']} | {v['stale_hi_before']} -> {v['stale_hi_after']} | {v['correct_before']} -> {v['correct_after']} (of {v['licensed_views']}) | " + (f"{bp['delta']:+.4f} [{bp['item'][0]:+.4f}, {bp['item'][1]:+.4f}]; [{bp['cluster'][0]:+.4f}, {bp['cluster'][1]:+.4f}]" if bp else "-") + " |")
    for k in ("P-L1", "P-L2", "P-L3", "P-L4", "P-L5"):
        if k in S:
            txt.append(f"\n### AUX-DS-A8-{k}\n\n**{S[k]['text']}**")
    txt.append(f"\n### AUX-DS-A8-SPEND\n\nmini ${S['spend']['mini']:.4f}, Haiku 4.5 ${S['spend']['h45']:.4f}, probes ${S['spend']['probes']['MINI']['usd'] + S['spend']['probes']['H45']['usd']:.4f}, against the cap ${CAP:.0f}.\n")
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(txt) + "\n")
    print("\n".join(txt))


if __name__ == "__main__":
    globals()["cmd_" + sys.argv[1]]()
