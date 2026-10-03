# -*- coding: utf-8 -*-
"""cf2_openai.py -- ADDENDUM_CF2_OPENAI (E5, program R117): GPT-5.6 Luna and GPT-5.6 Sol on the 444 items of the counterfactual set,
INDEXED-V2 (the superseded-only ground-truth summary), five draws, raw OpenAI Chat Completions with the frozen prompts_e1 texts and no
other system text; settings exactly the R74 X4 raw-API rows' (reasoning effort and temperature unset, max_completion_tokens 2048).
Registered sending order: draw-major per model (draw d for all 444 before draw d+1), eight workers, so repeats fall inside the 30-minute
cache window. Registered stopping rule: a hard cap of 30 USD for both models together, metered from the rows at OpenAI's page prices of
2026-09-18 (Sol $4 / $0.40 cached / $20 out, cache writes 1.25x; Luna $0.20 / $0.02 / $1.20, writes 1.25x); nothing else stops the run.
Registration registrations/ADDENDUM_CF2_OPENAI.md, registered-text sha256 230df444..., frozen at 177697a.

Subcommands:  lock | probe <model> | run <model> [--draws 1,2,3,4,5]   (each model in its own process; both read both rows files for the cap)
Rows: cf2/rows/rows_LUNA.jsonl, rows_SOL.jsonl (resume key unit_id, arm, draw), with prompt_tokens_details / completion_tokens_details kept.
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

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
import cf2_run as C2  # noqa: E402  (re-points run_cf to the CF-2 cell; asserts the prompts_e1 digests)
RC = C2.RC

REG = ROOT / "registrations" / "ADDENDUM_CF2_OPENAI.md"
REG_SHA = "230df444e3d5f028102426508e0d883824eb1258576515fadab49fbb84483149"
FROZEN_AT = "177697a"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
ARM = "INDEXED-V2"
K = 5
CAP = 30.00
WORKERS = 8
MODELS = {
    "gpt-5.6-luna": dict(code="LUNA", inp=0.20, cached=0.02, out=1.20, write_mult=1.25, probe_line=0.0008),
    "gpt-5.6-sol":  dict(code="SOL",  inp=4.00, cached=0.40, out=20.00, write_mult=1.25, probe_line=0.0135),
}
ROWS_DIR = C2.CF2 / "rows"
LOCK = ROWS_DIR / "lock_openai.json"
PROBES = ROWS_DIR / "probes_openai.json"


def reg_sha():
    b = REG.read_bytes(); i = b.find(FROZEN_END); assert i > 0
    return hashlib.sha256(b[:i]).hexdigest()


def setup():
    assert reg_sha() == REG_SHA, "REGISTRATION SHA MISMATCH -- STOP"
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


def cmd_lock():
    setup()
    rec = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "prompts_file_sha256": C2.RC.P.file_sha256(), "prompts_texts_sha256": C2.RC.P.texts_sha256(),
           "cell": 444, "arm": ARM, "k": K, "order": "draw-major per model, 8 workers", "cap_usd_both_models": CAP, "settings": {"reasoning_effort": None, "temperature": None, "max_completion_tokens": 2048},
           "prices_per_million": {m: {k: v for k, v in d.items() if k in ("inp", "cached", "out", "write_mult")} for m, d in MODELS.items()}, "when": dt.datetime.now().isoformat(timespec="seconds")}
    assert len(C2.RC.CELL) == 444
    C2.RC.PROBES.parent.mkdir(parents=True, exist_ok=True)
    io.open(LOCK, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    print(json.dumps(rec, indent=1))


def cmd_probe(model):
    setup(); assert LOCK.exists()
    u = C2.units(ARM)[0]
    row = call_once(model, u, 0)
    ok = model in row["served_model"]
    rec = {"model": model, "served": row["served_model"], "identifier_ok": ok, "tok_in": row["tok_in"], "tok_out": row["tok_out"], "tok_cached": row["tok_cached"], "tok_cache_write": row["tok_cache_write"],
           "tok_reasoning": row["tok_reasoning"], "usd": round(row["usd"], 6), "probe_line": MODELS[model]["probe_line"], "under_line": row["usd"] <= MODELS[model]["probe_line"], "parsed": row["status"],
           "sample": row["text"][:200], "when": row["when"]}
    d = json.load(io.open(PROBES, encoding="utf-8")) if PROBES.exists() else {}
    d[model] = rec
    io.open(PROBES, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")
    if not rec["under_line"]:
        raise SystemExit("probe per-call cost over the p95 line -- STOP")


def cmd_run(model, draws):
    setup()
    pr = json.load(io.open(PROBES, encoding="utf-8"))[model]; assert pr["identifier_ok"] and pr["under_line"]
    units = C2.units(ARM)
    path = rows_path(model); other = [rows_path(m) for m in MODELS if m != model][0]
    done = set()
    if path.exists():
        for l in io.open(path, encoding="utf-8"):
            if l.strip():
                r = json.loads(l); done.add((r["unit_id"], int(r["draw"])))
    lock = threading.Lock()
    state = {"mine": spent(path), "other": spent(other), "other_read": time.time(), "n": 0, "halted": False}
    print(f"{model}: spent so far mine ${state['mine']:.4f}, other lane ${state['other']:.4f}; cap ${CAP} both", flush=True)

    def total():
        if time.time() - state["other_read"] > 60:
            state["other"] = spent(other); state["other_read"] = time.time()
        return state["mine"] + state["other"]

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
            if state["n"] % 50 == 0:
                print(f"  {model} draw {d}: {state['n']} calls this run, lane ${state['mine']:.4f}, both ${total():.4f}", flush=True)
        return row

    for d in draws:
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


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "lock":
        cmd_lock()
    elif cmd == "probe":
        cmd_probe(sys.argv[2])
    elif cmd == "run":
        draws = [int(x) for x in sys.argv[sys.argv.index("--draws") + 1].split(",")] if "--draws" in sys.argv else list(range(1, K + 1))
        cmd_run(sys.argv[2], draws)


# ------------------------------------------------------------------ scoring (appended after the runs; no model call)
def cmd_score():
    import statistics as st
    import cf2_reader_score as R
    sys.stdout.reconfigure(encoding="utf-8")
    setup()
    items, idx = R.cell(); look = R.lookup_v2(items, idx)
    lock = json.load(io.open(LOCK, encoding="utf-8")); probes = json.load(io.open(PROBES, encoding="utf-8"))
    res = {"registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "lock": lock, "probes": probes, "lookup_v2": R.LOOKUP_GATE, "models": {}, "spend": {}, "when": dt.datetime.now().isoformat(timespec="seconds")}
    for model in MODELS:
        path = rows_path(model)
        r = R.score_lane(path, ARM, items, look)
        rows = [json.loads(l) for l in io.open(path, encoding="utf-8") if l.strip()]
        ok = [x for x in rows if x.get("status") == "OK"]
        served = sorted({x.get("served_model") for x in ok})
        tok = {"prompt_mean": r4(st.mean(x["tok_in"] for x in ok)), "completion_mean": r4(st.mean(x["tok_out"] for x in ok)), "reasoning_mean": r4(st.mean(x.get("tok_reasoning", 0) for x in ok)),
               "cached_mean": r4(st.mean(x.get("tok_cached", 0) for x in ok)), "cache_write_mean": r4(st.mean(x.get("tok_cache_write", 0) for x in ok)),
               "per_draw_usd": {d: round(sum(x["usd"] for x in ok if int(x["draw"]) == d), 4) for d in range(1, K + 1)},
               "per_draw_cached_share": {d: r4(sum(x.get("tok_cached", 0) for x in ok if int(x["draw"]) == d) / max(1, sum(x["tok_in"] for x in ok if int(x["draw"]) == d))) for d in range(1, K + 1)}}
        r.update({"served": served, "tokens": tok, "usd": round(sum(x.get("usd", 0.0) for x in rows), 4)})
        res["models"][model] = r
    res["spend"] = {m: res["models"][m]["usd"] for m in MODELS}; res["spend"]["both"] = round(sum(res["spend"].values()), 4); res["spend"]["probes"] = round(sum(p["usd"] for p in probes.values()), 4); res["spend"]["cap"] = CAP
    sol, luna = res["models"]["gpt-5.6-sol"]["vs_lookup"], res["models"]["gpt-5.6-luna"]["vs_lookup"]
    ps1 = bool(sol["delta"] > 0 and sol["both_exclude_zero"])
    ps2 = bool(not (luna["delta"] > 0 and luna["both_exclude_zero"]))
    res["P-S1"] = {"holds": ps1, "text": (f"P-S1 HOLDS: GPT-5.6 Sol reads {res['models']['gpt-5.6-sol']['whole']:.4f} against the lookup's {R.LOOKUP_GATE}, difference {R.fmt_paired(sol)}, both intervals excluding zero." if ps1 else
                                        f"P-S1 FAILS: GPT-5.6 Sol reads {res['models']['gpt-5.6-sol']['whole']:.4f} against the lookup's {R.LOOKUP_GATE}, difference {R.fmt_paired(sol)}.")}
    res["P-S2"] = {"holds": ps2, "text": (f"P-S2 HOLDS: GPT-5.6 Luna reads {res['models']['gpt-5.6-luna']['whole']:.4f} against the lookup's {R.LOOKUP_GATE}, difference {R.fmt_paired(luna)}, not reliably above it." if ps2 else
                                        f"P-S2 FAILS: GPT-5.6 Luna exceeds the lookup reliably, {R.fmt_paired(luna)}.")}
    out = C2.CF2 / "results" / "cf_scores_openai.json"
    io.open(out, "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1, sort_keys=True, default=float) + "\n")
    L = [f"\n## 13. ADDENDUM_CF2_OPENAI (E5, program R117): GPT-5.6 Luna and GPT-5.6 Sol on the 444 under the superseded-only summary (registered text sha256 `{REG_SHA[:16]}...`, frozen at `{FROZEN_AT}`; `tools/cf2_openai.py`; `rows/rows_LUNA.jsonl`, `rows/rows_SOL.jsonl`, `rows/lock_openai.json`, `rows/probes_openai.json`; `results/cf_scores_openai.json`; scored {dt.date.today().isoformat()})\n",
         "### AUX-CF2-OAI-LOCK, AUX-CF2-OAI-PROBES\n",
         f"Registration sha256 holds; raw Chat Completions with the frozen `prompts_e1` texts and no other system text; reasoning effort and temperature unset, `max_completion_tokens` 2048 (the R74 X4 settings); draw-major per model, eight workers; the cap of $30 for both models. Probes (E1.7 rule): " + "; ".join(f"`{m}` served `{p['served']}`, {p['tok_in']} in / {p['tok_out']} out ({p['tok_reasoning']} reasoning, {p['tok_cache_write']} cache-write), ${p['usd']:.6f}" for m, p in probes.items()) + ".\n",
         "### AUX-CF2-OAI-LUNA-V2, AUX-CF2-OAI-SOL-V2\n",
         "| reader | k | rows (not OK) | whole AUROC [persona CI] | minus lookup (item; persona) | SUP | RET | EXP | counted pooled | distinct values | identical across draws / median range |", "|---|---:|---|---|---|---|---|---|---|---:|---|"]
    for m, r in res["models"].items():
        c = r["census"]; ps = r["per_state"]
        L.append(f"| {m} | {K} | {c['rows']} ({c['not_ok']}) | **{r['whole']:.4f}** [{r['whole_ci_persona']['ci_lo']:.4f}, {r['whole_ci_persona']['ci_hi']:.4f}] | {R.fmt_paired(r['vs_lookup'])} | {ps['SUPERSESSION']['auroc']:.4f} | {ps['RETRACTION']['auroc']:.4f} | {ps['EXPIRY']['auroc']:.4f} | {r['counted_pooled']:.4f} | {r['distinct_values']} | {c['identical_across_draws']} of {c['units']} / {c['median_range']} |")
    L += ["\n### AUX-CF2-OAI-PNPRESENT (the post-hoc block of POSTHOC_SPEC_R112, the same definitions)\n", "| reader | scope | PN vs PRESENT [persona CI] | PN vs ABSENT | W/T/L | strict-win fraction [persona CI] |", "|---|---|---|---|---|---|"]
    for m, r in res["models"].items():
        for scope, b in (("whole", r["posthoc"]["whole"]),) + tuple((s_, r["posthoc"]["per_state"][s_]) for s_ in R.STATES):
            o = b["ordering"]; c = b["pn_vs_present_ci_persona"]
            L.append(f"| {m} | {scope} | {b['pn_vs_present']:.4f} [{c['ci_lo']:.4f}, {c['ci_hi']:.4f}] | {b['pn_vs_absent']:.4f} | {o['wins']}/{o['ties']}/{o['losses']} | {o['strict_win_fraction']:.4f} [{o['ci_persona']['ci_lo']:.4f}, {o['ci_persona']['ci_hi']:.4f}] |")
    L += ["\n### AUX-CF2-OAI-DRAWS (tokens per call, means over OK rows; the cache and reasoning columns X4 did not record)\n", "| reader | prompt | completion | reasoning | cached | cache-write | usd per draw | cached share per draw |", "|---|---:|---:|---:|---:|---:|---|---|"]
    for m, r in res["models"].items():
        t = r["tokens"]
        L.append(f"| {m} | {t['prompt_mean']} | {t['completion_mean']} | {t['reasoning_mean']} | {t['cached_mean']} | {t['cache_write_mean']} | {t['per_draw_usd']} | {t['per_draw_cached_share']} |")
    L += [f"\n### AUX-CF2-OAI-P-S1\n\n**{res['P-S1']['text']}**\n", f"### AUX-CF2-OAI-P-S2\n\n**{res['P-S2']['text']}**\n",
          f"### AUX-CF2-OAI-SPEND\n\nToken-metered from the rows at OpenAI's page prices of 2026-09-18 (input, cache-write at 1.25x, cached at the cached rate, output): Luna ${res['spend']['gpt-5.6-luna']:.4f}, Sol ${res['spend']['gpt-5.6-sol']:.4f}, both ${res['spend']['both']:.4f}, probes ${res['spend']['probes']:.4f}, against the cap of ${CAP:.0f}; not an invoice.\n"]
    with io.open(C2.CF2 / "NUMBERS_CF2.md", "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


def r4(x):
    return round(float(x), 4)


if __name__ == "__main__" and sys.argv[1] == "score":
    cmd_score()
