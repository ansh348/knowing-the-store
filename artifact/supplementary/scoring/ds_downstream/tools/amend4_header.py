"""amend4_header.py -- ADDENDUM_DS Amendment 4 (registrations/ADDENDUM_DS_AMENDMENT_4.md, frozen by sha256 before the first
call; program R109, 2026-09-14): the answer stage once more with a header in the user message that binds "User" to the persona's
name and pins the current date, GPT-4.1 mini and Claude Haiku 4.5 on the same 452 distinct views as Amendments 2 and 3, the D.4
system prompt unchanged. Two predictions (A4-P1, A4-P2) on the 65 licensed items whose gold record is in the retrieval view;
everything else descriptive.

MODEL CALLS: Lane 1 -- gpt-4.1-mini (temperature 0, seed 42, max_tokens 200, JSON mode, one retry), 452 calls, cache
ds_downstream/cache_amend4/. Lane 2 -- claude-haiku-4-5-20251001, temperature 0, max_tokens 200, k = 1, synchronous, the answer
read from the last JSON object of the reply with one retry. Both lanes together under the author's $8.00 cap.

Subcommands, in order:
  lock          registration sha256, prompt digests (SYSTEM_ANSWER D.4, USER_ANSWER_A4), population 452, the 65 -> run/lock_amend4.json
  probe-mini    one gpt-4.1-mini call (served identifier, tokens)                                        -> run/probes_amend4.json
  probe-h45     one Haiku 4.5 call (served identifier, tokens)                                           -> run/probes_amend4.json
  project       both lanes against the $8 cap (x1.3)                                                     -> run/projection_amend4.json
  run-mini      Lane 1 -> run/rows_ds_amend4_mini.jsonl
  run-h45       Lane 2 -> run/rows_ds_amend4_h45.jsonl
  score         the committed detector; A4-P1 / A4-P2 with both bootstrap conventions; first-sentence and source columns;
                NUMBERS_DS.md section 10 (AUX-DS-A4-*)                                                   -> run/scores_amend4.json
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import datetime as dt
import hashlib
import io
import json
import math
import re
import sys
import threading
import time

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import ds_common as DC                                                       # noqa: E402
from ds_common import ROOT, DS, RUN, J, jdump, POLICIES                     # noqa: E402
import run_ds as RD                                                          # noqa: E402
import prompts_ds as PD                                                      # noqa: E402
import prompts_e1 as P                                                       # noqa: E402
import amend2_lit as A2                                                      # noqa: E402
from e0_common import load_joins, toks, cov, MIN_SHARED, CROSS_GUARD, TAU_GOLD   # noqa: E402

sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
from run_cf import last_json                                                 # noqa: E402

api = DC.RC.e1_api()
REG = ROOT / "registrations" / "ADDENDUM_DS_AMENDMENT_4.md"
REG_SHA = "fb4b2ca8c8e280cbe6815c9782145abd93082e67b311fa1aeca60804f7dd6d8d"
CACHE4 = DS / "cache_amend4"
LINE = 8.00
LANE_MINI, PRICE_MINI = RD.LANE, RD.PRICE
LANE_H45, PRICE_H45 = A2.LANE_H45, A2.PRICE_H45
ROWS_MINI = RUN / "rows_ds_amend4_mini.jsonl"
ROWS_H45 = RUN / "rows_ds_amend4_h45.jsonl"
LEDGER = DS / "NUMBERS_DS.md"
ARM = "ANSWER-A4"
N_VIEWS = 452
N_INVIEW = 65
ABST = "store does not currently contain"
BAR_P1 = 0.10
BAR_P2 = {"MINI": 7, "H45": 19}                 # section A4.4: 15 -> 7 or fewer; 38 -> 19 or fewer
N_BOOT, SEED = 10000, 42

HEADER = ("The user is {name}. Every entry below that says \"User\" is about {name}. Today's date is {date}; each entry's age is counted back from today.\n"
          "\n")
USER_ANSWER_A4 = HEADER + PD.USER_ANSWER
LINE_RE = re.compile(r"^\[(\d+)\] lifecycle: (.*?) \| category: (.*?) \| attribute: (.*?) \| age: (.*?) \| text: (.*)$")
SENT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def registered_user_template():
    """USER_ANSWER_A4 as the frozen registration prints it (the fenced block of section A4.2, inner fences included)."""
    s = REG.read_text(encoding="utf-8")
    i = s.index("verbatim:\n\n```\n") + len("verbatim:\n\n```\n"); j = s.index("\n```\n\n`{name}` is the persona's name", i)
    return s[i:j]


def assert_lineage():
    h = hashlib.sha256(REG.read_bytes()).hexdigest()
    assert h == REG_SHA, f"ADDENDUM_DS_AMENDMENT_4.md sha256 {h} != frozen -- STOP"
    assert registered_user_template() == USER_ANSWER_A4, "USER_ANSWER_A4 differs from the frozen section A4.2 -- STOP"
    assert "AUX-DS-A4-REG" in LEDGER.read_text(encoding="utf-8"), "AUX-DS-A4-REG absent from NUMBERS_DS.md -- STOP (no call before the freeze is recorded)"
    RD.assert_lineage()


def redirect():
    CACHE4.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                             # noqa: SLF001
    e0.CACHE_PATH = CACHE4 / "responses.json"; e0.LEDGER_PATH = CACHE4 / "cost_ledger.json"
    e0._cache = None; e0._load_cache()                                       # noqa: SLF001
    e0.HARD_CAP_USD = LINE
    return e0


_PERSONA = {}


def persona_fields():
    """{persona: (name, iso date)} from the persona YAML (persona.name) and the join's pinned present (t_now)."""
    if not _PERSONA:
        joins = load_joins()
        for k, Jp in joins.items():
            name = (Jp.y.get("persona") or {}).get("name"); tn = getattr(Jp, "t_now", None)
            assert name and tn is not None, f"persona {k}: name or t_now missing -- STOP"
            _PERSONA[k] = (str(name), tn.date().isoformat())
    return _PERSONA


def messages(job):
    name, date = persona_fields()[job["persona"]]
    return [{"role": "system", "content": PD.SYSTEM_ANSWER},
            {"role": "user", "content": USER_ANSWER_A4.format(name=name, date=date, view=job["view"], question=job["question"])}]


def jobs():
    sub, hj = A2.h45_jobs()
    assert len(hj) == N_VIEWS, len(hj)
    return sub, hj


def inview_items(sub):
    st1 = J(DS / "stage1.json")["per_item"]; views = J(DS / "views.json")["items"]
    out = [(it, f"{it['item_id']}|{views[it['item_id']]['ALWAYS']['sha']}") for it in sub if it["label"] == "PRESENT" and st1[it["item_id"]]["ALWAYS"]["gold_in_view"]]
    assert len(out) == N_INVIEW, len(out)
    return out


# ------------------------------------------------------------------ lock / probe / project
def cmd_lock():
    assert_lineage()
    sub, hj = jobs(); inv = inview_items(sub); pf = persona_fields()
    out = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "user_answer_a4_sha256": sha(USER_ANSWER_A4), "header_sha256": sha(HEADER),
           "prompts_ds": PD.digests(), "prompts_e1": {"file": P.file_sha256(), "texts": P.texts_sha256()},
           "population": len(hj), "expected": N_VIEWS, "pn": sum(1 for j in hj if j["label"] == "PRESENT-NEGATIVE"), "present": sum(1 for j in hj if j["label"] == "PRESENT"),
           "inview_present": len(inv), "inview_personas": len({it["persona"] for it, _ in inv}), "personas_with_name_and_date": len(pf),
           "header_example": USER_ANSWER_A4.split("\n")[0].format(name=pf["aisha"][0], date=pf["aisha"][1]), "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RUN / "lock_amend4.json"); print(json.dumps(out, indent=1, ensure_ascii=False))


def probes():
    p = RUN / "probes_amend4.json"
    return J(p) if p.exists() else {}


def cmd_probe_mini():
    assert_lineage(); e0 = redirect(); sub, hj = jobs()
    first = next(j for j in hj if j["label"] == "PRESENT" and j["n_lines"] >= 5)
    r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,   # noqa: SLF001
                                             messages=messages(first), response_format={"type": "json_object"})
    o = api.parse_json(r.choices[0].message.content) or {}
    rec = {"item_id": first["item_id"], "view_lines": first["n_lines"], "served": r.model, "identifier_ok": LANE_MINI in r.model,
           "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens,
           "usd": r.usage.prompt_tokens / 1e6 * PRICE_MINI[0] + r.usage.completion_tokens / 1e6 * PRICE_MINI[1],
           "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL", "sample": (r.choices[0].message.content or "")[:300],
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    out = probes(); out["MINI"] = rec; jdump(out, RUN / "probes_amend4.json"); print(json.dumps(rec, indent=1, ensure_ascii=False))
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
    first = next(j for j in hj if j["label"] == "PRESENT" and j["n_lines"] >= 5)
    cl = A2.anthropic_client()
    text, tin, tout, served = h45_once(cl, first); o = last_json(text) or {}
    rec = {"item_id": first["item_id"], "view_lines": first["n_lines"], "served": served, "identifier_ok": served == LANE_H45, "tok_in": tin, "tok_out": tout,
           "usd": tin / 1e6 * PRICE_H45[0] + tout / 1e6 * PRICE_H45[1], "status": "OK" if isinstance(o.get("answer"), str) else "PARSE_FAIL",
           "sample": text[:300], "when": dt.datetime.now().isoformat(timespec="seconds")}
    out = probes(); out["H45"] = rec; jdump(out, RUN / "probes_amend4.json"); print(json.dumps(rec, indent=1, ensure_ascii=False))
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
    jdump(out, RUN / "projection_amend4.json"); print(json.dumps(out, indent=1))
    if not out["runs"]:
        sys.exit("PROJECTION x1.3 AT OR ABOVE THE $8 CAP -- STOP")


def spent(path):
    return sum(json.loads(l).get("usd", 0.0) for l in io.open(path, encoding="utf-8")) if path.exists() else 0.0


# ------------------------------------------------------------------ run
def cmd_run_mini():
    assert_lineage(); redirect(); sub, hj = jobs()
    assert J(RUN / "projection_amend4.json")["runs"]
    have = {json.loads(l)["key"] for l in io.open(ROWS_MINI, encoding="utf-8")} if ROWS_MINI.exists() else set()
    todo = [j for j in hj if j["key"] not in have]
    print(f"{len(todo)} mini calls to go (resumed past {len(have)})", flush=True)
    lock = threading.Lock(); spend = [spent(ROWS_MINI) + spent(ROWS_H45)]; stopped = [False]

    def work(job):
        with lock:
            if spend[0] >= LINE or stopped[0]:
                stopped[0] = True; return None
        msgs = messages(job)
        ok = lambda o: o is not None and isinstance(o.get("answer"), str)     # noqa: E731
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
               "raw": (r["content"] or "")[:400], "source": "amend4 call"}
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
    assert_lineage(); sub, hj = jobs()
    assert J(RUN / "projection_amend4.json")["runs"]
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
               "model": LANE_H45, "served_model": served, "cached": False, "tok_in": tin, "tok_out": tout, "usd": usd, "raw": (text or "")[:400], "source": "amend4 call"}
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
def is_abst(a):
    return ABST in re.sub(r"\s+", " ", (a or "")).casefold()


def first_sentence(a):
    parts = [x for x in SENT_RE.split((a or "").strip()) if x]
    return parts[0] if parts else (a or "")


def view_source(view_text, rec):
    """For a sup/ret obligation: does any ACTIVE line of the view assert the stale value (the item's own detector at TAU_GOLD)?
    Returns 'active' if so, 'tagged_only' if only tagged lines do, 'none' if no line does; None for expiry (unscorable)."""
    if rec["section"] == "expiring_logistics" or not rec.get("stale_field"):
        return None
    drop = rec["drop"]; ot, nt = toks(rec["stale_field"], drop), toks(rec["gold_field"], drop); do, dn = ot - nt, nt - ot
    act = tag = False
    for ln in view_text.split("\n"):
        m = LINE_RE.match(ln)
        if not m:
            continue
        A = toks(m.group(6), drop)
        if len(do & A) >= MIN_SHARED and cov(dn, A) < CROSS_GUARD and cov(do, A) >= TAU_GOLD:
            if m.group(2) == "active":
                act = True
            else:
                tag = True
    return "active" if act else ("tagged_only" if tag else "none")


def wilson(k, n, z=1.959964):
    if not n:
        return None
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 4), round(c + h, 4)]


def boot_paired(a, b, personas):
    """Paired difference of proportions mean(b - a) over items; item-level and persona-clustered percentile bootstrap (N_BOOT, SEED)."""
    a = np.asarray(a, float); b = np.asarray(b, float); d = b - a; n = len(d)
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, n, size=(N_BOOT, n)); item = d[idx].mean(axis=1)
    groups = collections.defaultdict(list)
    for i, p in enumerate(personas):
        groups[p].append(i)
    keys = sorted(groups); G = len(keys)
    rng2 = np.random.default_rng(SEED); cl = np.empty(N_BOOT)
    for t in range(N_BOOT):
        pick = rng2.integers(0, G, size=G)
        ids = np.concatenate([groups[keys[g]] for g in pick])
        cl[t] = d[ids].mean()
    return {"delta": round(float(d.mean()), 4), "item": [round(float(np.percentile(item, 2.5)), 4), round(float(np.percentile(item, 97.5)), 4)],
            "cluster": [round(float(np.percentile(cl, 2.5)), 4), round(float(np.percentile(cl, 97.5)), 4)], "n": n, "n_clusters": G, "n_boot": N_BOOT, "seed": SEED}


def cmd_score():
    sys.stdout.reconfigure(encoding="utf-8")
    sub = DC.load_cell(); rec = RD.records(sub); byid = {it["item_id"]: it for it in sub}
    st1 = J(DS / "stage1.json")["per_item"]; views = J(DS / "views.json")["items"]
    inv = inview_items(sub)
    d4 = {"MINI": J(RUN / "scores_ds.json")["per_row"], "H45": J(RUN / "scores_amend2.json")["per_row_h45"]}
    d4rows = {"MINI": {json.loads(l)["key"]: json.loads(l) for l in io.open(RUN / "rows_ds.jsonl", encoding="utf-8")},
              "H45": {json.loads(l)["key"]: json.loads(l) for l in io.open(RUN / "rows_ds_amend2_h45.jsonl", encoding="utf-8")}}
    for l in io.open(RUN / "rows_ds_amend2.jsonl", encoding="utf-8"):
        r = json.loads(l); d4rows["MINI"].setdefault(r["key"], r)
    S = {"registration_sha256": REG_SHA, "lock": J(RUN / "lock_amend4.json"), "stage2": {}, "per_row": {}, "predictions": {}, "columns": {}, "present": {}, "expiry": {}}
    for code, path, name in (("MINI", ROWS_MINI, "GPT-4.1 mini"), ("H45", ROWS_H45, "Claude Haiku 4.5")):
        rows, per, _ = A2.score_rows(path, sub, rec)
        S["stage2"][code] = {p: A2.summarize(rows, per, byid, None, p) for p in POLICIES}
        S["stage2"][code]["_rows"] = {"n": len(rows), "failed": sum(1 for r in rows.values() if r["status"] != "OK"), "served": sorted({r.get("served_model") or r.get("model") for r in rows.values()})}
        S["per_row"][code] = per
        # ---- A4-P1 / A4-P2 on the 65 in-view licensed items (ALWAYS view)
        cA, cB, aA, aB, pers, both = [], [], [], [], [], {"D4": 0, "A4": 0}
        for it, key in inv:
            sd, sa = d4[code][key], per[key]; rd, ra = d4rows[code][key], rows[key]
            cA.append(1 if sd.get("correct") else 0); cB.append(1 if sa.get("correct") else 0)
            aA.append(1 if is_abst(rd["answer"]) else 0); aB.append(1 if is_abst(ra["answer"]) else 0); pers.append(it["persona"])
            both["D4"] += int(sd.get("correct") and is_abst(rd["answer"])); both["A4"] += int(sa.get("correct") and is_abst(ra["answer"]))
        bp = boot_paired(cA, cB, pers)
        p1 = {"k_d4": sum(cA), "k_a4": sum(cB), "n": len(cA), "delta": bp["delta"], "ci_item": bp["item"], "ci_cluster": bp["cluster"], "bar": BAR_P1,
              "holds": bool(bp["delta"] >= BAR_P1 and bp["item"][0] > 0 and bp["cluster"][0] > 0), "n_clusters": bp["n_clusters"], "n_boot": bp["n_boot"], "seed": bp["seed"],
              "correct_and_abstained": both}
        p1["text"] = (f"A4-P1 HOLDS for {name}: the header raises the correct count on the 65 licensed items in view from {p1['k_d4']} to {p1['k_a4']}, Δ₁ = {p1['delta']:+.4f} with intervals [{bp['item'][0]:+.4f}, {bp['item'][1]:+.4f}] (item) and [{bp['cluster'][0]:+.4f}, {bp['cluster'][1]:+.4f}] (persona), both above zero and the point estimate at or above +0.10."
                      if p1["holds"] else
                      f"The header binding the entries to the persona and pinning the date raises the correct count on the 65 licensed items in view by less than 0.10, or by an amount whose interval reaches zero, for {name}: {p1['k_d4']} to {p1['k_a4']} of 65, Δ₁ = {p1['delta']:+.4f} with intervals [{bp['item'][0]:+.4f}, {bp['item'][1]:+.4f}] and [{bp['cluster'][0]:+.4f}, {bp['cluster'][1]:+.4f}].")
        p2 = {"k_d4": sum(aA), "k_a4": sum(aB), "n": len(aA), "bar_k_a4_at_most": BAR_P2[code], "holds": bool(sum(aB) <= BAR_P2[code])}
        p2["text"] = (f"A4-P2 HOLDS for {name}: abstentions on the 65 licensed items in view fall from {p2['k_d4']} to {p2['k_a4']}, at or under the bar of {BAR_P2[code]}."
                      if p2["holds"] else f"The header leaves {name}'s abstentions on the 65 licensed items in view at {p2['k_a4']} against {p2['k_d4']}, not less than half.")
        S["predictions"][code] = {"A4-P1": p1, "A4-P2": p2}
        # ---- descriptive columns: registered flag / first sentence / source, scorable PN per policy; expiry unscorable
        cols = {}
        for p in POLICIES:
            keys = [k for k, r in rows.items() if p in r["policies"] and r["label"] == "PRESENT-NEGATIVE" and per[k]["scored"]]
            sc = [k for k in keys if byid[rows[k]["item_id"]]["state"] != "exp"]
            reg = {k: bool(per[k]["stale_use_tau_gold"]) for k in keys}
            fs = {k: bool(RD.score_answer(byid[rows[k]["item_id"]], rec[rows[k]["item_id"]], first_sentence(rows[k]["answer"]))["stale_use_tau_gold"]) for k in sc}
            src = {k: view_source(views[rows[k]["item_id"]][p]["text"], rec[rows[k]["item_id"]]) for k in sc}
            cnt = collections.Counter()
            for k in sc:
                cnt[f"src={src[k]}|stale={reg[k]}"] += 1
            cols[p] = {"n_reached": len(keys), "n_expiry_unscorable": len(keys) - len(sc), "n_scorable": len(sc),
                       "registered_all": {"k": sum(reg[k] for k in keys), "n": len(keys)},
                       "registered_scorable": {"k": sum(reg[k] for k in sc), "n": len(sc), "wilson": wilson(sum(reg[k] for k in sc), len(sc))},
                       "first_sentence": {"k": sum(fs.values()), "n": len(sc), "wilson": wilson(sum(fs.values()), len(sc))},
                       "source_active": {"views": sum(1 for k in sc if src[k] == "active"), "stale": sum(1 for k in sc if src[k] == "active" and reg[k])},
                       "source_tagged_only": {"views": sum(1 for k in sc if src[k] == "tagged_only"), "stale": sum(1 for k in sc if src[k] == "tagged_only" and reg[k])},
                       "source_none": {"views": sum(1 for k in sc if src[k] == "none"), "stale": sum(1 for k in sc if src[k] == "none" and reg[k])},
                       "crosstab": dict(cnt),
                       "abstention_pn": {"k": sum(1 for k in sc if is_abst(rows[k]["answer"])), "n": len(sc)}}
        S["columns"][code] = cols
        # ---- PRESENT: correct over the 174 (ALWAYS) and the 65; abstentions
        pk = [k for k, r in rows.items() if "ALWAYS" in r["policies"] and r["label"] == "PRESENT" and per[k]["scored"]]
        S["present"][code] = {"always_n": len(pk), "always_correct": sum(1 for k in pk if per[k]["correct"]), "always_abstained": sum(1 for k in pk if is_abst(rows[k]["answer"])),
                              "always_correct_and_abstained": sum(1 for k in pk if per[k]["correct"] and is_abst(rows[k]["answer"])),
                              "inview": {"n": N_INVIEW, "correct_d4": p1["k_d4"], "correct_a4": p1["k_a4"], "abstained_d4": p2["k_d4"], "abstained_a4": p2["k_a4"], "correct_and_abstained": both,
                                         "correct_among_answered_a4": {"k": sum(1 for (it, key) in inv if per[key]["correct"] and not is_abst(rows[key]["answer"])), "n": N_INVIEW - p2["k_a4"]}},
                              "all_rows": {"n": sum(1 for r in rows.values() if r["label"] == "PRESENT"), "abstained": sum(1 for r in rows.values() if r["label"] == "PRESENT" and is_abst(r["answer"]))}}
        # ---- expiry rows under the pinned date, read as a list
        ex = [k for k, r in rows.items() if "ORACLE" in r["policies"] and r["label"] == "PRESENT-NEGATIVE" and byid[r["item_id"]]["state"] == "exp"]
        S["expiry"][code] = {"n_oracle": len(ex), "abstained": sum(1 for k in ex if is_abst(rows[k]["answer"])), "registered_flag": sum(1 for k in ex if per[k]["stale_use_tau_gold"]),
                             "answers": {k: rows[k]["answer"] for k in sorted(ex)}}
    pr = probes()
    spend = {"probe_mini": pr["MINI"]["usd"], "probe_h45": pr["H45"]["usd"], "mini": spent(ROWS_MINI), "h45": spent(ROWS_H45)}
    spend["total"] = sum(spend.values()); S["spend"] = spend; S["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(S, RUN / "scores_amend4.json")
    txt = ledger_text(S)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


def ledger_text(S):
    lk = S["lock"]; sp = S["spend"]; pr = probes(); pj = J(RUN / "projection_amend4.json")
    L = ["\n### AUX-DS-A4-LOCK, AUX-DS-A4-PROMPT, AUX-DS-A4-POP, AUX-DS-A4-PROBE-MINI, AUX-DS-A4-PROBE-H45, AUX-DS-A4-PROJECTION (appended by `tools/amend4_header.py score`)\n",
         f"\nRegistration sha256 holds; `USER_ANSWER_A4` sha256 `{lk['user_answer_a4_sha256']}` (the D.4 user text with the header, sha256 `{lk['header_sha256']}`, verbatim from section A4.2; "
         f"example first line: {lk['header_example']}); `SYSTEM_ANSWER` and `USER_ANSWER` as AUX-DS-PROMPT; prompts_e1 digests as pinned. Population {lk['population']} distinct (item, view) pairs "
         f"({lk['pn']} PN, {lk['present']} PRESENT); the prediction population {lk['inview_present']} licensed items in view over {lk['inview_personas']} personas; {lk['personas_with_name_and_date']} personas with a name and a pinned date. "
         f"Probe mini: served `{pr['MINI']['served']}` ({pr['MINI']['tok_in']} in / {pr['MINI']['tok_out']} out); probe Haiku 4.5: served `{pr['H45']['served']}` ({pr['H45']['tok_in']} in / {pr['H45']['tok_out']} out). "
         f"Projection: mini ${pj['MINI']['projected_usd']:.4f}, Haiku ${pj['H45']['projected_usd']:.4f}, sum with probes ${pj['sum']:.4f} (x1.3 ${pj['sum_x1_3']:.4f}) against the $8.00 cap; runs: {pj['runs']}.\n"]
    for code, name in (("MINI", "GPT-4.1 mini"), ("H45", "Claude Haiku 4.5")):
        P1 = S["predictions"][code]["A4-P1"]; P2 = S["predictions"][code]["A4-P2"]; pres = S["present"][code]
        L.append(f"\n### AUX-DS-A4-P1-{code}, AUX-DS-A4-P2-{code} — the two predictions, {name} (the 65 licensed items in view; item-level and persona-clustered percentile bootstrap, {P1['n_boot']} draws, seed {P1['seed']}, {P1['n_clusters']} personas)\n\n"
                 f"A4-P1: correct {P1['k_d4']} → {P1['k_a4']} of {P1['n']}, Δ₁ = {P1['delta']:+.4f}, item interval [{P1['ci_item'][0]:+.4f}, {P1['ci_item'][1]:+.4f}], persona interval [{P1['ci_cluster'][0]:+.4f}, {P1['ci_cluster'][1]:+.4f}], bar +{P1['bar']:.2f} with both intervals above zero: **{'HOLDS' if P1['holds'] else 'FAILS'}**. {P1['text']}\n\n"
                 f"A4-P2: abstentions {P2['k_d4']} → {P2['k_a4']} of {P2['n']}, bar {P2['bar_k_a4_at_most']} or fewer: **{'HOLDS' if P2['holds'] else 'FAILS'}**. {P2['text']}\n\n"
                 f"Beside: detector-correct answers that are abstentions restating the gold line, D.4 {P1['correct_and_abstained']['D4']} → A4 {P1['correct_and_abstained']['A4']}; correct among the answered under A4 {pres['inview']['correct_among_answered_a4']['k']} / {pres['inview']['correct_among_answered_a4']['n']}.\n")
        L.append(f"\n### AUX-DS-A4-PRESENT-{code} — the licensed items under {name} with the header\n\n"
                 f"Under retrieval alone (ALWAYS view, the ORACLE view on every licensed item): correct {pres['always_correct']} / {pres['always_n']} (D.4: {J(RUN / 'scores_ds.json')['per_policy']['ALWAYS']['present']['correct'] if code == 'MINI' else J(RUN / 'scores_amend2.json')['stage2_h45']['ALWAYS']['present']['correct']}), "
                 f"abstained {pres['always_abstained']} / {pres['always_n']}, of which {pres['always_correct_and_abstained']} counted correct; over all {pres['all_rows']['n']} licensed views abstained {pres['all_rows']['abstained']}.\n")
        h = S["stage2"][code]; rr = h["_rows"]
        L.append(f"\n### AUX-DS-A4-STAGE2-{code} — Stage 2 under {name} with the header, every policy, the committed detector, all states (rows {rr['n']}, failed {rr['failed']}, served {rr['served']}; temperature 0, k = 1)\n\n")
        L.append(A2.HEAD + "\n".join(A2.fmt_row(f"{name} + header, {p}", h[p]) for p in POLICIES) + "\n")
        L.append(f"\n### AUX-DS-A4-FIRSTSENT-{code}, AUX-DS-A4-SOURCE-{code} — stale use at TAU_GOLD on the scorable (supersession + retraction) reached obligations, {name} + header: the registered flag beside the first-sentence flag and the source in the view (expiry unscorable: {S['columns'][code]['ORACLE']['n_expiry_unscorable']} of the oracle's {S['columns'][code]['ORACLE']['n_reached']})\n\n"
                 "| policy | reached | expiry (unscorable) | scorable | registered flag, all states | registered flag, scorable (Wilson) | first sentence (Wilson) | active line asserts the stale value: views / stale | tagged-only: views / stale | no line: views / stale | abstentions |\n|---|---:|---:|---:|---|---|---|---|---|---|---|\n")
        for p in POLICIES:
            c = S["columns"][code][p]; rs = c["registered_scorable"]; fsn = c["first_sentence"]
            L.append(f"| {p} | {c['n_reached']} | {c['n_expiry_unscorable']} | {c['n_scorable']} | {c['registered_all']['k']} / {c['registered_all']['n']} | {rs['k']} / {rs['n']} = {rs['k'] / rs['n']:.4f} {rs['wilson']} | "
                     f"{fsn['k']} / {fsn['n']} = {fsn['k'] / fsn['n']:.4f} {fsn['wilson']} | {c['source_active']['views']} / {c['source_active']['stale']} | {c['source_tagged_only']['views']} / {c['source_tagged_only']['stale']} | "
                     f"{c['source_none']['views']} / {c['source_none']['stale']} | {c['abstention_pn']['k']} / {c['abstention_pn']['n']} |\n")
        ex = S["expiry"][code]
        L.append(f"\n### AUX-DS-A4-EXPIRY-{code} — the {ex['n_oracle']} expiry obligations under the oracle, {name} + header (unscorable; descriptive): abstained {ex['abstained']}, registered flag fires {ex['registered_flag']}. Answers, read as a list:\n\n")
        L.extend(f"- `{k}`: {a}\n" for k, a in ex["answers"].items())
    L.append(f"\n### AUX-DS-A4-SPEND\n\nProbe mini ${sp['probe_mini']:.4f}; probe Haiku ${sp['probe_h45']:.4f}; mini lane ${sp['mini']:.4f}; Haiku lane ${sp['h45']:.4f}; **total ${sp['total']:.4f}** against the author's $8.00 cap.\n")
    return "".join(L)


if __name__ == "__main__":
    {"lock": cmd_lock, "probe-mini": cmd_probe_mini, "probe-h45": cmd_probe_h45, "project": cmd_project,
     "run-mini": cmd_run_mini, "run-h45": cmd_run_h45, "score": cmd_score}[sys.argv[1]]()
