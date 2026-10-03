# -*- coding: utf-8 -*-
"""v2rcat_openai.py -- ADDENDUM_V2R_CAT Amendment 2 (E9, program R118): GPT-5.6 Luna and GPT-5.6 Sol on the 444 moved-count (V2R-CAT)
texts, five draws, raw OpenAI Chat Completions with the frozen prompts_e1 texts and no other system text, settings exactly E5's
(reasoning effort and temperature unset, max_completion_tokens 2048), the X4 collapse against each model's own recorded E5 v2 row
(AUX-CF2-OAI-SOL-V2 0.8500, -LUNA-V2 0.8417); P-M2. The runner is E5's cf2_openai.py retargeted at the V2R-CAT cell (v2rcat.point()).

Registered order: Luna first, all five draws, draw-major; then Sol draw-major. Registered stopping rule: a hard cap of 14 USD for both
models together, metered from the rows at the page prices of 2026-09-18. Registered cost rule: after Sol's second draw starts, the
metered cache share and mean cost of its first 25 calls project the five-draw total; over the cap, Sol stops at three whole draws,
otherwise it runs all five; the branch is a registered outcome (rows/costrule_openai.json, AUX-V2RCAT-A2-COSTRULE).
Registration registrations/ADDENDUM_V2R_CAT_AMENDMENT_2.md, registered-text sha256 f70e4779..., frozen at the freeze commit.

Subcommands:  lock | probe <model> | run <model> [--draws 1,2,3,4,5] | score
Rows: v2rcat/rows/rows_LUNA.jsonl, rows_SOL.jsonl (arm INDEXED-V2R-CAT; resume key unit_id, arm, draw), the usage details kept.
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

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
import v2rcat as V                                                           # noqa: E402  (asserts the prompts_e1 digests; V.point() re-points run_cf)
import run_cf as RC                                                          # noqa: E402
import score_cf as S                                                         # noqa: E402
from common_e1r import auroc                                                 # noqa: E402
from cf2_score import paired                                                 # noqa: E402

REG = ROOT / "registrations" / "ADDENDUM_V2R_CAT_AMENDMENT_2.md"
REG_SHA = "f70e4779f7b892df704fe3890917da25031c2f746aa67eaec64cfbe76b4462e9"
FROZEN_AT_FILE = ROOT / "reviews" / "v21" / "E9_FREEZE_COMMIT.txt"          # written at the freeze commit; read into the lock
ARM = V.ARM                                                                  # INDEXED-V2R-CAT
K = 5
CAP = 14.00
WORKERS = 8
COSTRULE_N = 25
MODELS = {
    "gpt-5.6-luna": dict(code="LUNA", inp=0.20, cached=0.02, out=1.20, write_mult=1.25, probe_line=0.0008, v2_gate=0.8417),
    "gpt-5.6-sol":  dict(code="SOL",  inp=4.00, cached=0.40, out=20.00, write_mult=1.25, probe_line=0.0135, v2_gate=0.8500),
}
ORDER = ("gpt-5.6-luna", "gpt-5.6-sol")
ROWS_DIR = V.ROWS
LOCK = ROWS_DIR / "lock_openai.json"
PROBES = ROWS_DIR / "probes_openai.json"
COSTRULE = ROWS_DIR / "costrule_openai.json"
OUT = V.RES / "scores_v2rcat_openai.json"
LEDGER = V.V2C / "NUMBERS_V2RCAT.md"
CF2_ROWS = V.CF2 / "rows"
TOL = 0.05


def reg_sha():
    b = REG.read_bytes(); i = b.find(V.FROZEN_END); assert i > 0
    return hashlib.sha256(b[:i]).hexdigest()


def frozen_at():
    return FROZEN_AT_FILE.read_text(encoding="utf-8").strip() if FROZEN_AT_FILE.exists() else "UNCOMMITTED"


def setup():
    assert reg_sha() == REG_SHA, "REGISTRATION SHA MISMATCH -- STOP"
    assert V.registration_ok(), "PARENT REGISTRATION MISMATCH -- STOP"
    assert V.locks_ok()["indexes_v2r"], "V2R INDEX LOCK MISMATCH -- STOP"
    V.point()
    assert frozen_at() != "UNCOMMITTED", "the freeze commit is not recorded (reviews/v21/E9_FREEZE_COMMIT.txt) -- STOP"
    RC.load_env()
    assert os.environ.get("OPENAI_API_KEY"), "no OPENAI_API_KEY"


def rows_path(model):
    return ROWS_DIR / f"rows_{MODELS[model]['code']}.jsonl"


def price(model, usage):
    """USD from the usage object at the page prices: cache writes at 1.25x input, cached reads at the cached rate, the rest at input."""
    m = MODELS[model]
    pt = usage.get("prompt_tokens", 0); ct = usage.get("completion_tokens", 0)
    det = usage.get("prompt_tokens_details") or {}
    cached = det.get("cached_tokens", 0) or 0
    write = det.get("cache_write_tokens", 0) or 0
    plain = max(0, pt - cached - write)
    usd = (plain * m["inp"] + write * m["inp"] * m["write_mult"] + cached * m["cached"] + ct * m["out"]) / 1e6
    return usd, cached, write, ((usage.get("completion_tokens_details") or {}).get("reasoning_tokens", 0) or 0)


def call_once(model, u, draw):
    from openai import OpenAI
    sysm, user = RC.prompts_for(u, ARM)
    cl = OpenAI(max_retries=2, timeout=120)
    r = cl.chat.completions.create(model=model, max_completion_tokens=2048,
                                   messages=[{"role": "system", "content": sysm}, {"role": "user", "content": user}])
    raw = r.model_dump(mode="json")
    usage = raw.get("usage") or {}
    text = r.choices[0].message.content
    usd, cached, write, reasoning = price(model, usage)
    row = RC.make_row(u, ARM, model, draw, text, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0), (MODELS[model]["inp"], MODELS[model]["out"]), 1.0, r.model)
    row.update({"usd": usd, "tok_cached": cached, "tok_cache_write": write, "tok_reasoning": reasoning, "finish_reason": r.choices[0].finish_reason,
                "usage": usage, "when": dt.datetime.now().isoformat(timespec="seconds")})
    return row


def spent(path):
    if not path.exists():
        return 0.0
    return sum(json.loads(l).get("usd", 0.0) for l in io.open(path, encoding="utf-8") if l.strip())


def probes_spent():
    if not PROBES.exists():
        return 0.0
    return sum(p.get("usd", 0.0) for p in json.load(io.open(PROBES, encoding="utf-8")).values())


def cmd_lock():
    setup()
    texts_sha = hashlib.sha256((V.BUILD / "texts_v2rcat.json").read_bytes()).hexdigest()
    rec = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "frozen_at": frozen_at(), "parent_registration_sha256": V.REG_SHA,
           "texts_v2rcat_sha256": texts_sha, "prompts_file_sha256": RC.P.file_sha256(), "prompts_texts_sha256": RC.P.texts_sha256(),
           "cell": 444, "arm": ARM, "k": K, "order": "Luna first, all five draws, draw-major; then Sol draw-major; 8 workers", "cap_usd_both_models": CAP,
           "cost_rule": {"after": "Sol draw 2 starts", "calls_read": COSTRULE_N, "branch_if_projection_over_cap": "Sol stops at three whole draws", "otherwise": "all five"},
           "settings": {"reasoning_effort": None, "temperature": None, "max_completion_tokens": 2048},
           "prices_per_million": {m: {k: v for k, v in d.items() if k in ("inp", "cached", "out", "write_mult")} for m, d in MODELS.items()},
           "v2_gates": {m: d["v2_gate"] for m, d in MODELS.items()}, "when": dt.datetime.now().isoformat(timespec="seconds")}
    assert len(V.CELL) == 444 and len(V.units(ARM)) == 444
    ROWS_DIR.mkdir(parents=True, exist_ok=True)
    io.open(LOCK, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    print(json.dumps(rec, indent=1))


def cmd_probe(model):
    setup(); assert LOCK.exists()
    u = V.units(ARM)[0]
    row = call_once(model, u, 0)
    ok = model in row["served_model"]
    rec = {"model": model, "served": row["served_model"], "identifier_ok": ok, "tok_in": row["tok_in"], "tok_out": row["tok_out"], "tok_cached": row["tok_cached"], "tok_cache_write": row["tok_cache_write"],
           "tok_reasoning": row["tok_reasoning"], "usd": round(row["usd"], 6), "probe_line": MODELS[model]["probe_line"], "under_line": row["usd"] <= MODELS[model]["probe_line"], "parsed": row["status"],
           "cache_fields_present": ("prompt_tokens_details" in (row.get("usage") or {})), "sample": row["text"][:200], "when": row["when"]}
    d = json.load(io.open(PROBES, encoding="utf-8")) if PROBES.exists() else {}
    d[model] = rec
    io.open(PROBES, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")
    if not rec["under_line"]:
        raise SystemExit("probe per-call cost over the p95 line -- STOP")
    if not rec["cache_fields_present"]:
        raise SystemExit("the usage object carries no prompt_tokens_details -- STOP (the cost rule cannot read the cache share)")


def cmd_run(model, draws):
    setup()
    pr = json.load(io.open(PROBES, encoding="utf-8"))[model]; assert pr["identifier_ok"] and pr["under_line"] and pr["cache_fields_present"]
    if model == "gpt-5.6-sol":   # registered order: Luna's five draws are whole before Sol starts
        luna = rows_path("gpt-5.6-luna")
        n_luna_ok = sum(1 for l in io.open(luna, encoding="utf-8") if l.strip() and json.loads(l).get("status") == "OK") if luna.exists() else 0
        assert n_luna_ok >= 444 * K - 5, f"Luna is not whole ({n_luna_ok} OK rows) -- the registered order runs Luna first"
    units = V.units(ARM)
    path = rows_path(model); other = [rows_path(m) for m in MODELS if m != model][0]
    done = set()
    if path.exists():
        for l in io.open(path, encoding="utf-8"):
            if l.strip():
                r = json.loads(l); done.add((r["unit_id"], int(r["draw"])))
    lock = threading.Lock()
    state = {"mine": spent(path), "other": spent(other), "other_read": time.time(), "n": 0, "halted": False, "d2": [], "plan": list(draws)}
    print(f"{model}: spent so far mine ${state['mine']:.4f}, other lane ${state['other']:.4f}, probes ${probes_spent():.4f}; cap ${CAP} both", flush=True)

    def total():
        if time.time() - state["other_read"] > 60:
            state["other"] = spent(other); state["other_read"] = time.time()
        return state["mine"] + state["other"] + probes_spent()

    def cost_rule(rows25):
        """The registered projection on Sol's first 25 calls of draw 2; writes the record and fixes the plan. Called once, under the lock."""
        pt = sum(r["tok_in"] for r in rows25); cached = sum(r.get("tok_cached", 0) for r in rows25)
        mean_usd = sum(r["usd"] for r in rows25) / len(rows25)
        sol_d1 = sum(json.loads(l).get("usd", 0.0) for l in io.open(path, encoding="utf-8") if l.strip() and int(json.loads(l)["draw"]) == 1)
        projected = spent(other) + probes_spent() + sol_d1 + 4 * 444 * mean_usd
        branch = "stop_at_three" if projected > CAP else "all_five"
        rec = {"model": model, "draw": 2, "calls_read": len(rows25), "cached_share": round(cached / max(1, pt), 4), "mean_usd_per_call": round(mean_usd, 6),
               "luna_spend": round(spent(other), 4), "probes": round(probes_spent(), 4), "sol_draw1": round(sol_d1, 4), "projected_total_five_draws": round(projected, 4), "cap": CAP,
               "branch": branch, "draws_to_run": [1, 2, 3] if branch == "stop_at_three" else [1, 2, 3, 4, 5], "when": dt.datetime.now().isoformat(timespec="seconds")}
        io.open(COSTRULE, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1, sort_keys=True) + "\n")
        state["plan"] = [d for d in state["plan"] if d in rec["draws_to_run"]]
        print(f"  COST RULE: cached share {rec['cached_share']}, mean ${mean_usd:.5f}/call, projected five-draw total ${projected:.2f} against ${CAP} -> {branch}; plan {state['plan']}", flush=True)

    def work(job):
        u, d = job
        if state["halted"]:
            return None
        with lock:
            if total() >= CAP:
                state["halted"] = True
                return None
        row = None
        for attempt in (1, 2, 3):
            try:
                row = call_once(model, u, d); break
            except Exception as e:  # noqa: BLE001
                if attempt == 3:
                    row = {"unit_id": u["unit_id"], "arm": ARM, "model": model, "draw": d, "status": f"ERROR:{type(e).__name__}", "when": dt.datetime.now().isoformat(timespec="seconds")}
                else:
                    time.sleep(5 * attempt)
        with lock:
            state["mine"] += row.get("usd", 0.0); state["n"] += 1
            with io.open(path, "a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(row, sort_keys=True) + "\n")
            if model == "gpt-5.6-sol" and d == 2 and row.get("status") == "OK" and not COSTRULE.exists():
                state["d2"].append(row)
                if len(state["d2"]) == COSTRULE_N:
                    cost_rule(state["d2"])
            if state["n"] % 50 == 0:
                print(f"  {model} draw {d}: {state['n']} calls this run, lane ${state['mine']:.4f}, both ${total():.4f}", flush=True)
        return row

    if model == "gpt-5.6-sol" and COSTRULE.exists():   # a resumed run keeps the recorded branch
        rec = json.load(io.open(COSTRULE, encoding="utf-8")); state["plan"] = [d for d in draws if d in rec["draws_to_run"]]
        print(f"cost rule already recorded: {rec['branch']}; plan {state['plan']}", flush=True)
    d_i = 0
    while d_i < len(state["plan"]):
        d = state["plan"][d_i]; d_i += 1
        jobs = [(u, d) for u in units if (u["unit_id"], d) not in done]
        if not jobs:
            print(f"{model} draw {d}: complete already", flush=True); continue
        t0 = time.time()
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
            list(ex.map(work, jobs))
        n_ok = sum(1 for l in io.open(path, encoding="utf-8") if l.strip() and json.loads(l).get("status") == "OK" and int(json.loads(l)["draw"]) == d)
        print(f"{model} draw {d} pass done in {time.time() - t0:.0f}s: OK rows {n_ok}/444; lane ${state['mine']:.4f}, both ${total():.4f}", flush=True)
        if state["halted"]:
            print(f"{model}: CAP REACHED at draw {d}; stopping (the registered rule: whole draws scored, partial draws discarded)", flush=True)
            break
    print(f"{model} DONE; lane spend ${state['mine']:.4f}; both lanes ${total():.4f}", flush=True)


# ------------------------------------------------------------------ scoring (no model call)
def r4(x):
    return round(float(x), 4)


def collapse_rows(path, arm):
    """{unit: mean nok over >= MIN_DRAWS OK draws}; the census beside (E5's conventions, cf2_reader_score.collapse)."""
    import cf2_reader_score as R
    return R.collapse(path, arm)


def cmd_score():
    import statistics as st
    setup(); sys.stdout.reconfigure(encoding="utf-8")
    y = np.array([it["y_nok"] for it in V.CELL], int); g = np.array([it["persona"] for it in V.CELL]); stt = np.array([it["state"] for it in V.CELL])
    lock = json.load(io.open(LOCK, encoding="utf-8")); probes = json.load(io.open(PROBES, encoding="utf-8"))
    costrule = json.load(io.open(COSTRULE, encoding="utf-8")) if COSTRULE.exists() else None
    res = {"registration_sha256": REG_SHA, "frozen_at": frozen_at(), "lock": lock, "probes": probes, "cost_rule": costrule, "tol": TOL, "models": {}, "when": dt.datetime.now().isoformat(timespec="seconds")}
    for model in ORDER:
        m = MODELS[model]
        v2c, _ = collapse_rows(CF2_ROWS / f"rows_{m['code']}.jsonl", "INDEXED-V2")
        v2 = np.array([v2c.get(it["item_id"], np.nan) for it in V.CELL], float)
        assert not np.isnan(v2).any(); a2 = r4(auroc(v2, y)); assert a2 == m["v2_gate"], ("GATE: the recorded E5 v2 row", model, a2)
        col, census = collapse_rows(rows_path(model), ARM)
        nv = np.array([col.get(it["item_id"], np.nan) for it in V.CELL], float)
        rows = [json.loads(l) for l in io.open(rows_path(model), encoding="utf-8") if l.strip()]
        ok = [x for x in rows if x.get("status") == "OK"]
        draws_whole = sorted(d for d in range(1, K + 1) if sum(1 for x in ok if int(x["draw"]) == d) == 444)
        M = {"census": census, "draws_whole": draws_whole, "scorable": bool(len(draws_whole) >= S.MIN_DRAWS and not np.isnan(nv).any()), "served": sorted({x.get("served_model") for x in ok}),
             "usd": round(sum(x.get("usd", 0.0) for x in rows), 4), "v2_recorded_k5": a2,
             "tokens": {"prompt_mean": r4(st.mean(x["tok_in"] for x in ok)), "completion_mean": r4(st.mean(x["tok_out"] for x in ok)), "reasoning_mean": r4(st.mean(x.get("tok_reasoning", 0) for x in ok)),
                        "cached_mean": r4(st.mean(x.get("tok_cached", 0) for x in ok)), "cache_write_mean": r4(st.mean(x.get("tok_cache_write", 0) for x in ok)),
                        "per_draw_usd": {d: round(sum(x["usd"] for x in ok if int(x["draw"]) == d), 4) for d in range(1, K + 1)},
                        "per_draw_cached_share": {d: r4(sum(x.get("tok_cached", 0) for x in ok if int(x["draw"]) == d) / max(1, sum(x["tok_in"] for x in ok if int(x["draw"]) == d))) for d in range(1, K + 1)}} if ok else {}}
        if M["scorable"]:
            M.update({"v2rcat": r4(auroc(nv, y)), "minus_v2": paired(v2, nv, y, g), "per_state": {}})
            for s_ in V.STATES:
                mk = stt == s_
                pd = paired(v2[mk], nv[mk], y[mk], g[mk])
                inside = bool(-TOL <= pd["item_ci"]["ci_lo"] and pd["item_ci"]["ci_hi"] <= TOL and -TOL <= pd["persona_ci"]["ci_lo"] and pd["persona_ci"]["ci_hi"] <= TOL)
                beyond = bool(abs(pd["delta"]) > TOL and ((pd["item_ci"]["ci_hi"] < -TOL and pd["persona_ci"]["ci_hi"] < -TOL) or (pd["item_ci"]["ci_lo"] > TOL and pd["persona_ci"]["ci_lo"] > TOL)))
                reliable_neg = bool(pd["delta"] < 0 and pd["item_ci"]["ci_hi"] < 0 and pd["persona_ci"]["ci_hi"] < 0)
                M["per_state"][s_] = {"n": int(mk.sum()), "pos": int(y[mk].sum()), "v2": r4(auroc(v2[mk], y[mk])), "v2rcat": r4(auroc(nv[mk], y[mk])), **pd,
                                      "inside_band_both": inside, "beyond_band_both": beyond, "reliable_negative": reliable_neg}
        res["models"][model] = M
    def fmt(M, s_):
        d = M["per_state"][s_]
        return f"{d['delta']:+.4f} with intervals [{d['item_ci']['ci_lo']:+.4f}, {d['item_ci']['ci_hi']:+.4f}] and [{d['persona_ci']['ci_lo']:+.4f}, {d['persona_ci']['ci_hi']:+.4f}]"
    NAMES = {"gpt-5.6-sol": "GPT-5.6 Sol", "gpt-5.6-luna": "GPT-5.6 Luna"}
    failing = []
    for model in ORDER:
        M = res["models"][model]
        if not M["scorable"]:
            failing.append((model, "not scorable")); continue
        for s_ in ("RETRACTION", "EXPIRY"):
            if not M["per_state"][s_]["reliable_negative"]:
                failing.append((model, s_))
    holds = not failing
    if holds:
        verdict = "P-M2 HOLDS: " + "; ".join(f"{NAMES[m]} falls on retraction ({fmt(res['models'][m], 'RETRACTION')}) and on expiry ({fmt(res['models'][m], 'EXPIRY')})" for m in ORDER) + ", every difference negative with both intervals excluding zero."
    else:
        parts = []
        for m, s_ in failing:
            parts.append(f"{NAMES[m]} {s_.lower()}: {'not scorable under the cap' if s_ == 'not scorable' else fmt(res['models'][m], s_)}")
        verdict = "P-M2 FAILS for " + ", ".join(sorted({NAMES[m] for m, _ in failing})) + ": " + "; ".join(parts) + "."
    res["P-M2"] = {"holds": holds, "text": verdict}
    res["spend"] = {m: res["models"][m]["usd"] for m in ORDER}; res["spend"]["both"] = round(sum(res["spend"].values()), 4); res["spend"]["probes"] = round(probes_spent(), 4); res["spend"]["cap"] = CAP
    V.jdump(res, OUT)
    def cell(M, s_):
        if not M["scorable"]:
            return "not scorable"
        d = M["per_state"][s_]
        return f"{d['v2']:.4f} -> {d['v2rcat']:.4f}, {d['delta']:+.4f} ([{d['item_ci']['ci_lo']:+.4f}, {d['item_ci']['ci_hi']:+.4f}]; [{d['persona_ci']['ci_lo']:+.4f}, {d['persona_ci']['ci_hi']:+.4f}]), {'inside' if d['inside_band_both'] else ('beyond' if d['beyond_band_both'] else 'neither')}"
    L = [f"\n## 10. AUX-V2RCAT-A2: Amendment 2 (E9, program R118) -- GPT-5.6 Luna and GPT-5.6 Sol at five draws on the moved-count texts through the raw API (registrations/ADDENDUM_V2R_CAT_AMENDMENT_2.md, registered text sha256 `{REG_SHA[:16]}...`, frozen at `{frozen_at()}`; `tools/v2rcat_openai.py`; `rows/rows_LUNA.jsonl`, `rows/rows_SOL.jsonl`, `rows/lock_openai.json`, `rows/probes_openai.json`, `rows/costrule_openai.json`; `results/scores_v2rcat_openai.json`; scored {dt.date.today().isoformat()})\n",
         "### AUX-V2RCAT-A2-LOCK, AUX-V2RCAT-A2-PROBES\n",
         "Registration sha256 holds; the parent registration and the V2R index lock re-asserted; raw Chat Completions with the frozen `prompts_e1` texts and no other system text; reasoning effort and temperature unset, `max_completion_tokens` 2048 (E5's settings); Luna first then Sol, draw-major, eight workers; the cap of $14 for both models. Probes (E1.7 rule): " + "; ".join(f"`{m}` served `{p['served']}`, {p['tok_in']} in / {p['tok_out']} out ({p['tok_reasoning']} reasoning, {p['tok_cache_write']} cache-write), ${p['usd']:.6f}" for m, p in probes.items()) + ".\n",
         "### AUX-V2RCAT-A2-COSTRULE\n",
         (f"After Sol's second draw started, its first {costrule['calls_read']} calls read a cached share of {costrule['cached_share']} and a mean cost of ${costrule['mean_usd_per_call']:.5f} per call; the projected five-draw total (Luna ${costrule['luna_spend']:.4f} + probes ${costrule['probes']:.4f} + Sol draw 1 ${costrule['sol_draw1']:.4f} + 4 x 444 x the mean) was ${costrule['projected_total_five_draws']:.2f} against the cap of ${CAP:.0f}: **branch `{costrule['branch']}`**, draws {costrule['draws_to_run']} (a registered outcome, not a deviation).\n" if costrule else "The cost rule did not fire (Sol's second draw never started).\n"),
         "### AUX-V2RCAT-A2-LUNA-K5, AUX-V2RCAT-A2-SOL-K5\n",
         "| reader | whole draws | rows (not OK) | v2 (recorded E5, k = 5) | V2R-CAT | whole minus v2 (item; persona) | SUP v2 -> V2R-CAT | RET v2 -> V2R-CAT, delta (item; persona), band | EXP v2 -> V2R-CAT, delta (item; persona), band |", "|---|---|---|---:|---:|---|---|---|---|"]
    for m in ORDER:
        M = res["models"][m]; c = M["census"]
        if M["scorable"]:
            mv = M["minus_v2"]
            L.append(f"| {m} | {M['draws_whole']} | {c['rows']} ({c['not_ok']}) | {M['v2_recorded_k5']:.4f} | **{M['v2rcat']:.4f}** | {mv['delta']:+.4f} ([{mv['item_ci']['ci_lo']:+.4f}, {mv['item_ci']['ci_hi']:+.4f}]; [{mv['persona_ci']['ci_lo']:+.4f}, {mv['persona_ci']['ci_hi']:+.4f}]) | {M['per_state']['SUPERSESSION']['v2']:.4f} -> {M['per_state']['SUPERSESSION']['v2rcat']:.4f}, {M['per_state']['SUPERSESSION']['delta']:+.4f} | {cell(M, 'RETRACTION')} | {cell(M, 'EXPIRY')} |")
        else:
            L.append(f"| {m} | {M['draws_whole']} | {c['rows']} ({c['not_ok']}) | {M['v2_recorded_k5']:.4f} | not scorable (fewer than three whole draws) | | | | |")
    L += ["\n### AUX-V2RCAT-A2-DRAWS (tokens per call, means over OK rows)\n", "| reader | prompt | completion | reasoning | cached | cache-write | usd per draw | cached share per draw |", "|---|---:|---:|---:|---:|---:|---|---|"]
    for m in ORDER:
        t = res["models"][m]["tokens"]
        if t:
            L.append(f"| {m} | {t['prompt_mean']} | {t['completion_mean']} | {t['reasoning_mean']} | {t['cached_mean']} | {t['cache_write_mean']} | {t['per_draw_usd']} | {t['per_draw_cached_share']} |")
    L += [f"\n### AUX-V2RCAT-A2-P-M2\n\n**{verdict}**\n",
          f"### AUX-V2RCAT-A2-SPEND\n\nToken-metered from the rows at OpenAI's page prices of 2026-09-18 (input, cache-write at 1.25x, cached at the cached rate, output): Luna ${res['spend']['gpt-5.6-luna']:.4f}, Sol ${res['spend']['gpt-5.6-sol']:.4f}, both ${res['spend']['both']:.4f}, probes ${res['spend']['probes']:.4f}, against the cap of ${CAP:.0f}; not an invoice.\n"]
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "lock":
        cmd_lock()
    elif cmd == "probe":
        cmd_probe(sys.argv[2])
    elif cmd == "run":
        draws = [int(x) for x in sys.argv[sys.argv.index("--draws") + 1].split(",")] if "--draws" in sys.argv else list(range(1, K + 1))
        cmd_run(sys.argv[2], draws)
    elif cmd == "score":
        cmd_score()
