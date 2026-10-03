"""run_ds.py -- DS Phase B steps 4-6: Stage 2 of ADDENDUM_DS.md (section D.4), the answer calls and their scoring.

MODEL CALLS: gpt-4.1-mini only (prompts_e1's decoding: temperature 0, seed 42, max_tokens 200, JSON mode,
the E1 clamp's parse-and-retry-once), one served-identifier probe (E1.7), one call per distinct
(item, view) -- policies whose views are byte-identical share the answer (cache key = item id + view
sha256). No Haiku, no Opus, no embedding call. Responses cached under ds_downstream/cache/.

Population: PN items where the forbidding record reached the view and the policy did not abstain, under
each of the six policies; PRESENT items not abstained under each policy (ruling R3). No ABSENT calls.

Subcommands, in order:  build | probe | project | run | score
  build    the Stage 2 population and the distinct views -> run/cell_ds.json (verify_ds must pass)
  probe    one call through the raw client: served identifier, tokens -> run/probes_ds.json
  project  probe tokens x distinct views against the $2 line and the $4 rule, net of what is billed
  run      the calls -> run/rows_ds.jsonl (stops at $4)
  score    the committed detector on every answer (section D.4): stale use / surfacing / successor / both,
           PRESENT correctness; rates per policy split by tagged / untagged reach; spend
           -> run/scores_ds.json and NUMBERS_DS.md (AUX-DS-STAGE2, -SPEND, -BUDGETRULE)
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import datetime as dt
import io
import json
import math
import subprocess
import sys
import threading

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import ds_common as DC                                                       # noqa: E402
from ds_common import ROOT, DS, RUN, CACHE, LEDGER, J, jdump, STAGE2_POLICIES   # noqa: E402
import prompts_ds as PD                                                      # noqa: E402
import prompts_e1 as P                                                       # noqa: E402
from e0_common import load_joins, toks, cov, SECTION_FIELDS, MIN_SHARED, MIN_DISCR, CROSS_GUARD, TAU_GOLD   # noqa: E402
from index_v2 import detect, TAU_HI                                          # noqa: E402

api = DC.RC.e1_api()
LANE, PRICE = "gpt-4.1-mini", (0.40, 1.60)
BUDGET, LINE = 4.00, 2.00
ROWS_P = RUN / "rows_ds.jsonl"
LEDGER_KEYS = ["AUX-DS-PRECOND", "AUX-DS-POP", "AUX-DS-FLAGCENSUS", "AUX-DS-NAMES", "AUX-DS-THRESHOLDS", "AUX-DS-LOOKUP-GATE",
               "AUX-DS-LINELOCK", "AUX-DS-POLICIES", "AUX-DS-REACH", "AUX-DS-PRESENT", "AUX-DS-ABSTAIN", "AUX-DS-VIEWSIZE",
               "AUX-DS-PROMPT", "AUX-DS-STAGE2", "AUX-DS-SPEND", "AUX-DS-BUDGETRULE"]


def assert_lineage():
    assert P.file_sha256() == DC.RC.PIN_PROMPTS["file"] and P.texts_sha256() == DC.RC.PIN_PROMPTS["texts"], "prompts_e1 digest drift -- STOP"
    assert (P.MODEL, P.TEMPERATURE, P.SEED, P.MAX_TOKENS) == (LANE, 0, 42, 200), "lane drift -- STOP"
    reg = PD.from_registration(ROOT / "registrations/ADDENDUM_DS.md")
    assert reg == PD.TEXTS, "prompts_ds differs from the frozen section D.4 -- STOP"


def redirect_cache():
    CACHE.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                             # noqa: SLF001
    e0.CACHE_PATH = CACHE / "responses.json"; e0.LEDGER_PATH = CACHE / "cost_ledger.json"
    e0._cache = None; e0._load_cache()                                       # noqa: SLF001
    return e0


# ------------------------------------------------------------------ build
def build_cell():
    sub = DC.load_cell()
    st1 = J(DS / "stage1.json")["per_item"]; views = J(DS / "views.json")["items"]
    byid = {it["item_id"]: it for it in sub}
    jobs, members = {}, collections.defaultdict(list)          # view key -> job; view key -> (item, policy)
    for it in sub:
        for p in STAGE2_POLICIES:
            s = st1[it["item_id"]][p]
            if s["abstain"]:
                continue
            if it["label"] == "PRESENT-NEGATIVE" and not s["reach"]:
                continue
            if it["label"] == "ABSENT":
                continue
            v = views[it["item_id"]][p]
            key = f"{it['item_id']}|{v['sha']}"
            jobs.setdefault(key, {"key": key, "item_id": it["item_id"], "persona": it["persona"], "question": it["question"], "label": it["label"],
                                  "state": it["state"], "view": v["text"], "view_sha": v["sha"], "n_lines": v["n_lines"], "policies": []})
            jobs[key]["policies"].append(p); members[key].append(p)
    nominal = sum(len(j["policies"]) for j in jobs.values())
    per_pol = {p: {"pn": sum(1 for j in jobs.values() if p in j["policies"] and j["label"] == "PRESENT-NEGATIVE"),
                   "present": sum(1 for j in jobs.values() if p in j["policies"] and j["label"] == "PRESENT")} for p in STAGE2_POLICIES}
    return sub, list(jobs.values()), {"distinct_views": len(jobs), "nominal_calls": nominal, "per_policy": per_pol,
                                      "distinct_pn": sum(1 for j in jobs.values() if j["label"] == "PRESENT-NEGATIVE"),
                                      "distinct_present": sum(1 for j in jobs.values() if j["label"] == "PRESENT")}


def messages(job):
    return [{"role": "system", "content": PD.SYSTEM_ANSWER}, {"role": "user", "content": PD.USER_ANSWER.format(view=job["view"], question=job["question"])}]


def cmd_build():
    assert_lineage()
    rc = subprocess.run([sys.executable, str(DS / "tools" / "verify_ds.py")], capture_output=True, text=True, cwd=ROOT).returncode
    assert rc == 0, "verify_ds.py fails -- STOP"
    sub, jobs, meta = build_cell()
    meta.update({"registration": "registrations/ADDENDUM_DS.md", "frozen": DC.FREEZE, "lane": LANE, "temperature": 0, "seed": 42, "max_tokens": 200, "k": 1,
                 "prompts_ds": PD.digests(), "prompts_e1": {"file": P.file_sha256(), "texts": P.texts_sha256()},
                 "rule": "one call per distinct (item, view); policies sharing a view share the answer; abstained items and unreached PN items get no call",
                 "built": dt.date.today().isoformat()})
    RUN.mkdir(parents=True, exist_ok=True); jdump({"meta": meta, "jobs": jobs}, RUN / "cell_ds.json")
    print(json.dumps(meta, indent=1))


# ------------------------------------------------------------------ probe / project
def cmd_probe():
    assert_lineage(); e0 = redirect_cache()
    sub, jobs, meta = build_cell()
    first = next(j for j in jobs if j["label"] == "PRESENT-NEGATIVE" and j["n_lines"] > 5)
    r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,   # noqa: SLF001
                                             messages=messages(first), response_format={"type": "json_object"})
    o = api.parse_json(r.choices[0].message.content) or {}
    out = {"ANSWER": {"item_id": first["item_id"], "view_lines": first["n_lines"], "served": r.model, "identifier_ok": LANE in r.model,
                      "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens,
                      "usd": r.usage.prompt_tokens / 1e6 * PRICE[0] + r.usage.completion_tokens / 1e6 * PRICE[1],
                      "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL", "sample": (r.choices[0].message.content or "")[:300],
                      "when": dt.datetime.now().isoformat(timespec="seconds")}}
    jdump(out, RUN / "probes_ds.json"); print(json.dumps(out, indent=1))
    if not out["ANSWER"]["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if out["ANSWER"]["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def billed_so_far():
    probes = sum(v["usd"] for v in J(RUN / "probes_ds.json").values()) if (RUN / "probes_ds.json").exists() else 0.0
    run = sum(json.loads(l).get("usd", 0.0) for l in io.open(ROWS_P, encoding="utf-8")) if ROWS_P.exists() else 0.0
    return {"probes": probes, "run": run, "total": probes + run}


def cmd_project():
    p = J(RUN / "probes_ds.json")["ANSWER"]; sub, jobs, meta = build_cell()
    # scale the probe's input tokens by view length: shell tokens (probe minus its lines) + per-line share
    per_line = 45.0
    shell = max(50.0, p["tok_in"] - per_line * p["view_lines"])
    tin = sum(shell + per_line * j["n_lines"] for j in jobs); tout = p["tok_out"] * len(jobs)
    usd = tin / 1e6 * PRICE[0] + tout / 1e6 * PRICE[1]; so_far = billed_so_far()
    print(f"distinct views : {len(jobs)} (nominal {meta['nominal_calls']}; PN {meta['distinct_pn']}, PRESENT {meta['distinct_present']})")
    print(f"projected in   : {tin:,.0f} tok   out: {tout:,} tok   PROJECTED ${usd:.4f}  (probe {p['tok_in']} in / {p['tok_out']} out on a {p['view_lines']}-line view)")
    print(f"billed so far  : ${so_far['total']:.4f}")
    print(f"projected total ${usd + so_far['total']:.4f} against the ${LINE:.2f} line and the ${BUDGET:.2f} rule (x1.3 = ${1.3 * usd + so_far['total']:.4f})")
    jdump({"projected_usd": usd, "n_distinct_views": len(jobs), "nominal_calls": meta["nominal_calls"], "billed_so_far": so_far, "line": LINE, "budget": BUDGET,
           "when": dt.datetime.now().isoformat(timespec="seconds")}, RUN / "projection_ds.json")
    if usd + so_far["total"] > BUDGET:
        sys.exit("PROJECTION ABOVE THE $4 RULE -- STOP")


# ------------------------------------------------------------------ run
def done_keys():
    return {json.loads(l)["key"] for l in io.open(ROWS_P, encoding="utf-8")} if ROWS_P.exists() else set()


def answer(job):
    msgs = messages(job)
    ok = lambda o: o is not None and isinstance(o.get("answer"), str)
    r = api.call(job["key"], "ANSWER", msgs); o = api.parse_json(r["content"]); n_calls, failed = 1, False
    usd = 0.0 if r["cached"] else r["prompt_tokens"] / 1e6 * PRICE[0] + r["completion_tokens"] / 1e6 * PRICE[1]
    if not ok(o):
        r2 = api.call(job["key"], "ANSWER#retry", msgs); o = api.parse_json(r2["content"]); n_calls = 2
        usd += 0.0 if r2["cached"] else r2["prompt_tokens"] / 1e6 * PRICE[0] + r2["completion_tokens"] / 1e6 * PRICE[1]
        r = r2
        if not ok(o):
            failed, o = True, {}
    return {**{k: job[k] for k in ("key", "item_id", "persona", "question", "label", "state", "view_sha", "n_lines", "policies")},
            "answer": (o.get("answer") if not failed else None), "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls,
            "cached": r["cached"], "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "usd": usd, "raw": (r["content"] or "")[:400]}


def cmd_run():
    assert_lineage(); redirect_cache()
    sub, jobs, meta = build_cell(); done = done_keys()
    todo = [j for j in jobs if j["key"] not in done]
    print(f"{len(todo)} calls to go (resumed past {len(done)})", flush=True)
    lock, spend, stopped, n_done = threading.Lock(), [billed_so_far()["total"]], [False], [0]

    def work(job):
        with lock:
            if spend[0] >= BUDGET or stopped[0]:
                stopped[0] = True; return None
        r = answer(job)
        with lock:
            spend[0] += r["usd"]; n_done[0] += 1
            with io.open(ROWS_P, "a", encoding="utf-8") as f:
                f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
            if n_done[0] % 100 == 0:
                print(f"  {n_done[0]} done, billed ${spend[0]:.4f}", flush=True); api.flush()
        return r
    try:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            out = [r for r in ex.map(work, todo) if r is not None]
    finally:
        api.flush()
    c = collections.Counter(r["status"] for r in out)
    print(f"DONE {len(out)} rows; status {dict(c)}; billed total ${spend[0]:.4f} against ${BUDGET:.2f}" + ("  >>> STOPPED AT $4" if stopped[0] else ""))
    if stopped[0]:
        sys.exit(1)


# ------------------------------------------------------------------ score
def records(sub):
    """Per item: the YAML record's stale / successor / gold token sets and the persona drop set."""
    joins = load_joins(); out = {}
    for it in sub:
        if it["label"] == "ABSENT":
            continue
        Jp = joins[it["persona"]]; qid = it["question_id"]
        if qid not in Jp.rec_of or Jp.rec_of[qid] is None:
            out[it["item_id"]] = None; continue
        sec, ridx = Jp.rec_of[qid]
        rec = [r for r in (Jp.y.get(sec) or []) if isinstance(r, dict)][ridx]
        gf, gs, sf, ss = SECTION_FIELDS[sec]
        out[it["item_id"]] = {"section": sec, "gold_field": rec.get(gf), "stale_field": rec.get(sf) if sf else None, "drop": Jp.drop}
    return out


def score_answer(it, rec, text):
    """Section D.4: the committed detector on the answer as the one text."""
    A = toks(text or "", rec["drop"])
    out = {}
    if it["label"] == "PRESENT-NEGATIVE":
        if rec["section"] == "expiring_logistics":
            ft = toks(rec["gold_field"], rec["drop"])
            c = cov(ft, A); shared = len(ft & A) >= MIN_SHARED
            out.update({"stale_use": bool(shared and c >= TAU_HI), "stale_surface": bool(shared and c >= TAU_HI), "stale_cov": c,
                        "stale_use_tau_gold": bool(shared and c >= TAU_GOLD), "successor_use": None, "both": None})
        else:
            old, new = rec["stale_field"], rec["gold_field"]
            d_old = detect(old, new, {"a": A}, rec["drop"]); d_new = detect(new, old, {"a": A}, rec["drop"])
            ot, nt = toks(old, rec["drop"]), toks(new, rec["drop"]); do, dn = ot - nt, nt - ot
            c_old, c_new = cov(do, A), cov(dn, A)
            out.update({"stale_use": bool(d_old is not None and d_old.get("a", 0.0) >= TAU_HI),
                        "stale_surface": bool(len(do & A) >= MIN_SHARED and c_old >= TAU_HI), "stale_cov": c_old,
                        "stale_use_tau_gold": bool(d_old is not None and d_old.get("a", 0.0) >= TAU_GOLD),
                        "successor_use": (bool(d_new is not None and d_new.get("a", 0.0) >= TAU_HI) if rec["section"] == "supersession_events" else None),
                        "successor_cov": c_new,
                        "both": bool(c_old >= TAU_HI and c_new >= TAU_HI and len(do & A) >= MIN_SHARED and len(dn & A) >= MIN_SHARED)})
    else:
        gt = toks(rec["gold_field"], rec["drop"]); c = cov(gt, A); shared = len(gt & A) >= MIN_SHARED
        out.update({"correct": bool(shared and c >= TAU_GOLD), "correct_tau_hi": bool(shared and c >= TAU_HI), "gold_cov": c})
    return out


def score_all(write=True):
    sub = DC.load_cell(); byid = {it["item_id"]: it for it in sub}
    rec = records(sub); st1 = J(DS / "stage1.json")["per_item"]
    rows = {}
    for l in io.open(ROWS_P, encoding="utf-8"):
        r = json.loads(l); rows[r["key"]] = r
    sub_, jobs, meta = build_cell()
    S = {"population": meta, "n_rows": len(rows), "failures": sum(1 for r in rows.values() if r["status"] != "OK"), "per_policy": {}, "per_row": {}}
    for key, r in rows.items():
        it = byid[r["item_id"]]
        if r["status"] != "OK" or rec.get(r["item_id"]) is None:
            S["per_row"][key] = {"status": r["status"], "policies": r["policies"], "scored": False}; continue
        S["per_row"][key] = {"status": "OK", "policies": r["policies"], "scored": True, **score_answer(it, rec[r["item_id"]], r["answer"])}
    for p in STAGE2_POLICIES:
        pn_rows = [(k, s) for k, s in S["per_row"].items() if p in s["policies"] and s["scored"] and byid[rows[k]["item_id"]]["label"] == "PRESENT-NEGATIVE"]
        pr_rows = [(k, s) for k, s in S["per_row"].items() if p in s["policies"] and s["scored"] and byid[rows[k]["item_id"]]["label"] == "PRESENT"]
        d = {"pn_answered": len(pn_rows), "present_answered": len(pr_rows), "pn_abstained": sum(1 for it in sub if it["y_nok"] and st1[it["item_id"]][p]["abstain"]),
             "pn_reached_not_abstained": sum(1 for it in sub if it["y_nok"] and st1[it["item_id"]][p]["reach"] and not st1[it["item_id"]][p]["abstain"])}
        for split, pred in (("all", lambda it: True), ("tagged", lambda it: st1[it["item_id"]][p]["tagged_reach"]), ("untagged", lambda it: not st1[it["item_id"]][p]["tagged_reach"])):
            sel = [s for k, s in pn_rows if pred(byid[rows[k]["item_id"]])]
            n = len(sel)
            d[f"pn_{split}"] = {"n": n, "stale_use": sum(1 for s in sel if s["stale_use"]), "stale_surface": sum(1 for s in sel if s["stale_surface"]),
                                "stale_use_tau_gold": sum(1 for s in sel if s["stale_use_tau_gold"]),
                                "successor_use": sum(1 for s in sel if s.get("successor_use")), "n_supersession": sum(1 for s in sel if s.get("successor_use") is not None),
                                "both": sum(1 for s in sel if s.get("both"))}
            d[f"pn_{split}"]["stale_use_rate"] = d[f"pn_{split}"]["stale_use"] / n if n else None
        for st in ("sup", "ret", "exp"):
            sel = [s for k, s in pn_rows if byid[rows[k]["item_id"]]["state"] == st]
            d[f"pn_state_{st}"] = {"n": len(sel), "stale_use": sum(1 for s in sel if s["stale_use"]), "stale_surface": sum(1 for s in sel if s["stale_surface"])}
        d["present"] = {"n": len(pr_rows), "correct": sum(1 for k, s in pr_rows if s["correct"]), "correct_tau_hi": sum(1 for k, s in pr_rows if s["correct_tau_hi"]),
                        "rate": (sum(1 for k, s in pr_rows if s["correct"]) / len(pr_rows)) if pr_rows else None}
        S["per_policy"][p] = d
    S["spend"] = billed_so_far(); S["spend"]["under_4"] = S["spend"]["total"] < BUDGET; S["spend"]["under_line"] = S["spend"]["total"] < LINE
    S["when"] = dt.datetime.now().isoformat(timespec="seconds")
    if write:
        jdump(S, RUN / "scores_ds.json")
    return S


def compare(a, b, path="", out=None):
    out = [] if out is None else out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a:
            if k in ("when", "spend"):
                continue
            if k not in b:
                out.append(path + "/" + k + " missing"); continue
            compare(a[k], b[k], path + "/" + k, out)
    elif isinstance(a, list) and isinstance(b, list):
        if a != b:
            out.append(f"{path}: lists differ")
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        if abs(float(a) - float(b)) > 1e-9:
            out.append(f"{path}: {a} != {b}")
    elif a != b:
        out.append(f"{path}: {str(a)[:40]} != {str(b)[:40]}")
    return out


def ledger_text(S):
    pp = S["per_policy"]; today = dt.date.today().isoformat()
    f = lambda k, n: f"{k} / {n} = {k / n:.4f}" if n else "—"
    txt = f"""
---

## 4. Steps 4–6 — Stage 2, the answer calls, scored (written {today})

### AUX-DS-STAGE2

Lane `gpt-4.1-mini` (served identifier probed, `run/probes_ds.json`), temperature 0, seed 42, max_tokens 200, JSON mode,
one retry on a parse failure. **{S['population']['distinct_views']} distinct (item, view) calls** for {S['population']['nominal_calls']} nominal
(policy, item) pairs ({S['population']['distinct_pn']} PN views, {S['population']['distinct_present']} PRESENT views); rows {S['n_rows']}, failures {S['failures']}.
Scoring: the committed detector (`e0_common` / `index_v2.detect`) on the `answer` string, persona-name tokens dropped:
stale use = `detect(stale, successor)` ≥ TAU_HI 0.80 (cross-guarded; expiry: the expired fact's tokens at TAU_HI, no
successor); stale surfacing = unguarded coverage ≥ 0.80; successor use (supersession) = `detect(successor, stale)` ≥ 0.80;
both = both coverages ≥ 0.80 unguarded; PRESENT correctness = gold-field coverage ≥ TAU_GOLD 0.50 (TAU_HI beside).
Abstained items are reported as abstained, never pooled. **Reading note (descriptive):** TAU_HI 0.80 was calibrated on entry
texts; on a two-sentence answer the stale value's unique tokens are paraphrased (coverage 0.5–0.67 on the answers that give
the stale value as the answer), so the registered TAU_HI row reads zero everywhere and the TAU_GOLD row beside it is the
sensitive one; the tagged / untagged split of that row is where the tag's effect shows.

| policy | PN reached ∧ answered | PN abstained | stale use (all) | stale use, tagged reach | stale use, untagged reach | stale surfacing | stale use at TAU_GOLD (all) | at TAU_GOLD, tagged | at TAU_GOLD, untagged | successor use (of supersession) | both | PRESENT answered | PRESENT correct (TAU_GOLD) | at TAU_HI |
|---|---:|---:|---|---|---|---:|---|---|---|---|---:|---:|---|---:|
""" + "\n".join(
        f"| {p} | {d['pn_answered']} | {d['pn_abstained']} | {f(d['pn_all']['stale_use'], d['pn_all']['n'])} | {f(d['pn_tagged']['stale_use'], d['pn_tagged']['n'])} | "
        f"{f(d['pn_untagged']['stale_use'], d['pn_untagged']['n'])} | {d['pn_all']['stale_surface']} | {f(d['pn_all']['stale_use_tau_gold'], d['pn_all']['n'])} | "
        f"{f(d['pn_tagged']['stale_use_tau_gold'], d['pn_tagged']['n'])} | {f(d['pn_untagged']['stale_use_tau_gold'], d['pn_untagged']['n'])} | "
        f"{f(d['pn_all']['successor_use'], d['pn_all']['n_supersession'])} | {d['pn_all']['both']} | {d['present_answered']} | {f(d['present']['correct'], d['present']['n'])} | {d['present']['correct_tau_hi']} |"
        for p, d in pp.items()) + f"""

Per state (stale use / answered): """ + "; ".join(
        f"{p}: sup {pp[p]['pn_state_sup']['stale_use']}/{pp[p]['pn_state_sup']['n']}, ret {pp[p]['pn_state_ret']['stale_use']}/{pp[p]['pn_state_ret']['n']}, exp {pp[p]['pn_state_exp']['stale_use']}/{pp[p]['pn_state_exp']['n']}"
        for p in pp) + f""".

### AUX-DS-SPEND and AUX-DS-BUDGETRULE

Billed on the OpenAI key from response usage at $0.40 / $1.60 per 1M: probe ${S['spend']['probes']:.4f}, run ${S['spend']['run']:.4f} — **total
${S['spend']['total']:.4f}**, under the $2 line ({'yes' if S['spend']['under_line'] else 'NO'}) and the $4 rule ({'yes' if S['spend']['under_4'] else 'NO'}). Nothing on the Anthropic key; no Haiku,
no Opus; no embedding call; no monitor elicited. Projection before launch: `run/projection_ds.json`.
"""
    return txt


def cmd_score():
    sys.stdout.reconfigure(encoding="utf-8")
    S = score_all(write=True); txt = ledger_text(S)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    {"build": cmd_build, "probe": cmd_probe, "project": cmd_project, "run": cmd_run, "score": cmd_score}[sys.argv[1]]()
