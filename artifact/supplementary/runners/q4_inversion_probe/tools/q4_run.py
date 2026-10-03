"""q4_run.py -- ADDENDUM_Q4 (frozen sha256 8b6ee9e3f7e2181edcab06e35d9a9efc0a0c21421ab841664a8f6e22da7ca608,
2026-09-13): the inexpressibility marker read as absence, one descriptive arm on the recorded
structureless coverage items (Mem0 238, A-MEM 284).

MODEL CALLS: gpt-4.1-mini only, frozen prompts_e1 (digests asserted), temperature 0, seed 42, k=1,
max_tokens 200, JSON mode, one retry on a parse failure (the E1 clamp), cache namespace
q4_inversion_probe/cache/. The blind and intact rows are the recorded main-study rows, never re-run.

Condition Q4-MARKER-ABSENT: the committed TRUE summary text (indexes_v2.json, the key the intact row
used) plus a blank line and the instruction line, inside the frozen USER_INDEXED template.

Subcommands, in order:  lock | probe | project | run | score
  lock     assert the population (238 / 284), the intact and blind reproductions, and that every
           rendered summary equals the committed text + "\n\n" + LINE      -> run/lock_q4.json
  probe    one raw call: served identifier, tokens                           -> run/probes_q4.json
  project  522 calls at the probe's tokens against the combined $3 cap       -> run/projection_q4.json
  run      the calls (8 workers; cached; stops at the client's $3 hard cap)  -> run/q4_elicitation.json
  score    D1 (Q4 - intact) and D2 (Q4 - blind) per store, both intervals   -> results/q4_scores.json,
           NUMBERS_Q4.md
"""
from __future__ import annotations

import concurrent.futures as cf
import datetime as dt
import hashlib
import io
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e1r_robustness" / "tools"))
import api                                                                   # noqa: E402  E1 shim -> E0 client under _e0_api
import prompts_e1 as P                                                       # noqa: E402
from common_e1r import auroc, boot_item, boot_cluster                        # noqa: E402

E1_FILE_SHA = "337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84"
E1_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"
assert P.file_sha256() == E1_FILE_SHA, "prompts_e1.py has changed since E1 froze it -- STOP"
assert P.texts_sha256() == E1_TEXTS_SHA, "prompts_e1 frozen texts have changed -- STOP"
assert (P.MODEL, P.TEMPERATURE, P.SEED, P.MAX_TOKENS) == ("gpt-4.1-mini", 0, 42, 200), "lane drift -- STOP"

Q4 = ROOT / "q4_inversion_probe"
RUN, RES, CACHE, LEDGER = Q4 / "run", Q4 / "results", Q4 / "cache", Q4 / "NUMBERS_Q4.md"
REG = ROOT / "registrations" / "ADDENDUM_Q4.md"
REG_SHA = "8b6ee9e3f7e2181edcab06e35d9a9efc0a0c21421ab841664a8f6e22da7ca608"
ARM = "Q4-MARKER-ABSENT"
LINE = "Treat any field marked 'not expressible by this backend' as absent; the backend does not record it."
MARK = "not expressible by this backend"
PRICE = (0.40, 1.60)
CAP = 3.00
SC = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}
E1 = ROOT / "e1_metamemory"

_e0 = sys.modules["_e0_api"]
for d in (RUN, RES, CACHE):
    d.mkdir(parents=True, exist_ok=True)
_e0.CACHE_PATH = CACHE / "responses.json"
_e0.LEDGER_PATH = CACHE / "cost_ledger.json"
_e0._cache = None                                                            # noqa: SLF001
_e0._load_cache()                                                            # noqa: SLF001
_e0.HARD_CAP_USD = CAP
api.load_env()


def J(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    pathlib.Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=1, sort_keys=True, default=float)
        f.write("\n")


def assert_registration():
    sha = hashlib.sha256(REG.read_bytes()).hexdigest()
    assert sha == REG_SHA, f"ADDENDUM_Q4.md sha256 {sha} != frozen {REG_SHA} -- STOP"


# ------------------------------------------------------------------ population
def load():
    items = {i["item_id"]: i for i in J(E1 / "build" / "items_final.json")}
    main = J(E1 / "elicitation_main.json")
    idx = J(E1 / "indexes_v2.json")["indexes"]
    blind = {r["question"]: r for r in main if r["arm"] == "BLIND" and r["status"] == "OK"}
    intact = {r["tag"]: r for r in main if r["arm"] == "INDEXED-TRUE" and r["status"] == "OK"}
    qmap = {r["tag"]: r["question"] for r in main if r["arm"] != "BLIND"}
    ext = [it for it in items.values() if it.get("label", it["label_pre"]) in SC and it["backend"] in ("mem0", "amem")]
    ext = [it for it in ext if qmap.get(it["item_id"]) in blind and it["item_id"] in intact
           and blind[qmap[it["item_id"]]]["fok"] is not None and intact[it["item_id"]]["fok"] is not None]
    ext.sort(key=lambda it: (it["backend"], it["item_id"]))
    n = {b: sum(1 for it in ext if it["backend"] == b) for b in ("mem0", "amem")}
    assert n == {"mem0": 238, "amem": 284}, n
    return ext, blind, intact, qmap, idx


def ikey(it):
    b, p, v = it["backend"], it["persona"], it["variant"]
    return (f"{b}:{p}:SLOT:{it['question_id']}" if v == "SLOT-ABLATED" else f"{b}:{p}:{v}") + ":TRUE"


def q4_text(committed):
    assert not committed.endswith("\n"), "committed text ends with a newline; the lock assumes it does not"
    return committed + "\n\n" + LINE


def label_y(it):
    return 0 if it.get("label", it["label_pre"]) == "ABSENT" else 1


def arrays(store, ext, blind, intact, qmap, rows=None):
    """(blind, intact, q4 or None, y, personas) on the paired items of one store."""
    b, a, q, y, g = [], [], [], [], []
    for it in ext:
        if it["backend"] != store:
            continue
        t = it["item_id"]
        if rows is not None:
            r = rows.get(t)
            if not r or r["fok"] is None:
                continue
            q.append(r["fok"])
        b.append(blind[qmap[t]]["fok"]); a.append(intact[t]["fok"]); y.append(label_y(it)); g.append(it["persona"])
    return np.array(b, float), np.array(a, float), (np.array(q, float) if rows is not None else None), np.array(y, int), np.array(g)


EXPECT = {"mem0": (238, 0.4777, -0.0969), "amem": (284, 0.4526, -0.1065)}


def cmd_lock():
    assert_registration()
    ext, blind, intact, qmap, idx = load()
    keys = sorted({ikey(it) for it in ext})
    for k in keys:
        base = idx[k]; t = q4_text(base)
        assert t[:len(base)] == base and t[len(base):] == "\n\n" + LINE, k
        assert sum(1 for ln in base.splitlines() if ln.strip() == MARK) == 3, (k, "marker lines")
    rep = {}
    for store, (n, au, d) in EXPECT.items():
        b, a, _, y, g = arrays(store, ext, blind, intact, qmap)
        rep[store] = {"n": int(len(y)), "pos": int(y.sum()), "intact_auroc": round(float(auroc(a, y)), 4), "blind_auroc": round(float(auroc(b, y)), 4),
                      "intact_delta": round(float(auroc(a, y) - auroc(b, y)), 4), "personas": int(len(set(g.tolist())))}
        assert (rep[store]["n"], rep[store]["intact_auroc"], rep[store]["intact_delta"]) == (n, au, d), rep[store]
    out = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "keys": len(keys), "marker_lines_per_key": 3,
           "line": LINE, "sep": "\\n\\n", "reproduction": rep, "prompts_e1": {"file": P.file_sha256(), "texts": P.texts_sha256()},
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RUN / "lock_q4.json"); print(json.dumps(out, indent=1))


def messages(it, qmap, idx):
    return [{"role": "system", "content": P.SYSTEM},
            {"role": "user", "content": P.USER_INDEXED.format(index=q4_text(idx[ikey(it)]), question=qmap[it["item_id"]])}]


def cmd_probe():
    assert_registration()
    ext, blind, intact, qmap, idx = load()
    first = ext[0]
    r = _e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,   # noqa: SLF001
                                             messages=messages(first, qmap, idx), response_format={"type": "json_object"})
    o = api.parse_json(r.choices[0].message.content) or {}
    rec = {"item_id": first["item_id"], "backend": first["backend"], "served": r.model, "identifier_ok": P.MODEL in r.model,
           "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens,
           "usd": r.usage.prompt_tokens / 1e6 * PRICE[0] + r.usage.completion_tokens / 1e6 * PRICE[1],
           "status": "OK" if o.get("fok") is not None else "PARSE_FAIL", "sample": (r.choices[0].message.content or "")[:300],
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump({"PROBE": rec}, RUN / "probes_q4.json"); print(json.dumps(rec, indent=1))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def cmd_project():
    p = J(RUN / "probes_q4.json")["PROBE"]
    n = 522
    tin, tout = p["tok_in"] * n, max(1, p["tok_out"]) * n
    usd = tin / 1e6 * PRICE[0] + tout / 1e6 * PRICE[1]
    other = ROOT / "ds_downstream" / "run" / "projection_amend1.json"
    other_usd = J(other)["projected_total_usd"] if other.exists() else None
    out = {"n_calls": n, "tok_in": tin, "tok_out": tout, "projected_usd": usd, "x1_3": 1.3 * usd, "probe_usd": p["usd"], "cap_combined": CAP,
           "ds_amend1_projection_usd": other_usd, "combined": (usd + other_usd) if other_usd is not None else None,
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RUN / "projection_q4.json"); print(json.dumps(out, indent=1))
    if out["combined"] is not None and out["combined"] > CAP:
        sys.exit("COMBINED PROJECTION ABOVE THE $3 CAP -- STOP")
    if usd > CAP:
        sys.exit("PROJECTION ABOVE THE $3 CAP -- STOP")


def one(it, qmap, idx):
    msgs = messages(it, qmap, idx)
    r = api.call(it["item_id"], ARM, msgs)
    j = api.parse_json(r["content"]) or {}
    fok, nok = _clamp(j.get("fok")), _clamp(j.get("nok"))
    n_calls = 1
    if fok is None:
        r = api.call(it["item_id"], ARM + "#retry", msgs); j = api.parse_json(r["content"]) or {}
        fok, nok = _clamp(j.get("fok")), _clamp(j.get("nok")); n_calls = 2
    usd = 0.0 if r["cached"] else r["prompt_tokens"] / 1e6 * PRICE[0] + r["completion_tokens"] / 1e6 * PRICE[1]
    return {"tag": it["item_id"], "arm": ARM, "backend": it["backend"], "persona": it["persona"], "label": it.get("label", it["label_pre"]),
            "question": qmap[it["item_id"]], "fok": fok, "nok": nok, "cached": r["cached"], "n_calls": n_calls,
            "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "usd": usd,
            "status": "OK" if fok is not None else "ELICITATION_FAILED", "raw": (r["content"] or "")[:300]}


def _clamp(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    if v > 1:
        v = v / 100.0
    return max(0.0, min(1.0, v))


def cmd_run():
    assert_registration()
    ext, blind, intact, qmap, idx = load()
    out = []
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for n, row in enumerate(ex.map(lambda it: one(it, qmap, idx), ext), 1):
            out.append(row)
            if n % 100 == 0:
                api.flush(); print(n, "/", len(ext), api.meter(), flush=True)
    api.flush()
    out.sort(key=lambda r: (r["backend"], r["tag"]))
    jdump({"meta": {"registration_sha256": REG_SHA, "arm": ARM, "line": LINE, "lane": P.MODEL, "temperature": 0, "seed": 42, "max_tokens": 200, "k": 1,
                    "when": dt.datetime.now().isoformat(timespec="seconds")}, "rows": out}, RUN / "q4_elicitation.json")
    failed = sum(1 for r in out if r["status"] != "OK")
    print("DONE", len(out), "rows; failed:", failed, "; meter:", api.meter(), "; billed this run: $%.4f" % sum(r["usd"] for r in out))
    if failed > 0.02 * len(out):
        sys.exit("STOP: elicitation failures above 2%")


def ci(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]" if "ci_lo" in d else "[—]"


def cmd_score():
    sys.stdout.reconfigure(encoding="utf-8")
    ext, blind, intact, qmap, idx = load()
    rows = {r["tag"]: r for r in J(RUN / "q4_elicitation.json")["rows"] if r["status"] == "OK"}
    probe = J(RUN / "probes_q4.json")["PROBE"]; proj = J(RUN / "projection_q4.json"); lock = J(RUN / "lock_q4.json")
    res = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "arm": ARM, "line": LINE, "stores": {}}
    for store in ("mem0", "amem"):
        b, a, q, y, g = arrays(store, ext, blind, intact, qmap, rows)
        d1_i, d1_c = boot_item(a, q, y), boot_cluster(a, q, y, g)
        d2_i, d2_c = boot_item(b, q, y), boot_cluster(b, q, y, g)
        res["stores"][store] = {
            "n": int(len(y)), "pos": int(y.sum()), "personas": int(len(set(g.tolist()))),
            "blind_auroc": round(float(auroc(b, y)), 4), "intact_auroc": round(float(auroc(a, y)), 4), "q4_auroc": round(float(auroc(q, y)), 4),
            "intact_delta_vs_blind": round(float(auroc(a, y) - auroc(b, y)), 4),
            "q4_mean_fok": round(float(q.mean()), 4), "intact_mean_fok": round(float(a.mean()), 4), "q4_distinct_values": int(len(set(np.round(q, 6).tolist()))),
            "D1_q4_minus_intact": {"delta": round(float(auroc(q, y) - auroc(a, y)), 4), "item": d1_i, "persona": d1_c,
                                   "both_exclude_zero": bool(d1_i.get("excludes_zero") and d1_c.get("excludes_zero")),
                                   "agree": bool(d1_i.get("excludes_zero") == d1_c.get("excludes_zero"))},
            "D2_q4_minus_blind": {"delta": round(float(auroc(q, y) - auroc(b, y)), 4), "item": d2_i, "persona": d2_c,
                                  "both_exclude_zero": bool(d2_i.get("excludes_zero") and d2_c.get("excludes_zero")),
                                  "agree": bool(d2_i.get("excludes_zero") == d2_c.get("excludes_zero"))},
            "identical_to_intact": int(sum(1 for x, z in zip(q, a) if x == z)),
        }
    all_rows = J(RUN / "q4_elicitation.json")["rows"]
    spend = {"probe": probe["usd"], "run": sum(r["usd"] for r in all_rows), "n_calls": sum(r["n_calls"] for r in all_rows),
             "cached": sum(1 for r in all_rows if r["cached"]), "failed": sum(1 for r in all_rows if r["status"] != "OK")}
    spend["total"] = spend["probe"] + spend["run"]
    res["spend"] = spend; res["probe"] = probe; res["projection"] = proj; res["lock"] = lock
    res["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(res, RES / "q4_scores.json")
    S = res["stores"]; today = dt.date.today().isoformat()
    txt = f"""# NUMBERS_Q4.md — the marker-as-absence probe (ADDENDUM_Q4, descriptive; R103, {today})

Registration `registrations/ADDENDUM_Q4.md`, frozen sha256 `{REG_SHA}` before the first call (copy in
`iclr2027_monitoring_submission/ARTIFACT/registrations/`). Descriptive: no prediction, no bar, no verdict; every value prints
whichever way it came out. Source `q4_inversion_probe/results/q4_scores.json`; rows `run/q4_elicitation.json`; lock `run/lock_q4.json`.

### AUX-Q4-LOCK

Population {S['mem0']['n']} Mem0 ({S['mem0']['pos']} positive) and {S['amem']['n']} A-MEM ({S['amem']['pos']} positive), {lock['keys']} summary keys, 3 marker lines per key. Each rendered
summary equals the committed TRUE text plus one blank line and the instruction line, byte for byte; the recorded intact rows reproduce
(Mem0 {lock['reproduction']['mem0']['intact_auroc']}, Δ {lock['reproduction']['mem0']['intact_delta']:+.4f}; A-MEM {lock['reproduction']['amem']['intact_auroc']}, Δ {lock['reproduction']['amem']['intact_delta']:+.4f}). prompts_e1 digests {lock['prompts_e1']['file'][:8]}… / {lock['prompts_e1']['texts'][:8]}….

### AUX-Q4-PROBE and AUX-Q4-PROJECTION

Served `{probe['served']}` (identifier ok: {probe['identifier_ok']}), {probe['tok_in']} in / {probe['tok_out']} out on the first item; projection {proj['n_calls']} calls,
${proj['projected_usd']:.4f} (x1.3 ${proj['x1_3']:.4f}) against the combined $3.00 cap.

### AUX-Q4-M0 and AUX-Q4-AM — the condition beside the recorded rows

| Key | Store | n | blind | intact (recorded) | Q4 marker-as-absence | D1 = Q4 − intact | item CI | persona CI | D2 = Q4 − blind | item CI | persona CI |
|---|---|---:|---:|---:|---:|---:|---|---|---:|---|---|
""" + "\n".join(
        f"| AUX-Q4-{k} | {name} | {s['n']} | {s['blind_auroc']:.4f} | {s['intact_auroc']:.4f} | **{s['q4_auroc']:.4f}** | {s['D1_q4_minus_intact']['delta']:+.4f} | {ci(s['D1_q4_minus_intact']['item'])} | {ci(s['D1_q4_minus_intact']['persona'])} | {s['D2_q4_minus_blind']['delta']:+.4f} | {ci(s['D2_q4_minus_blind']['item'])} | {ci(s['D2_q4_minus_blind']['persona'])} |"
        for k, name, s in (("M0", "Mem0", S["mem0"]), ("AM", "A-MEM", S["amem"]))) + f"""

Mean FOK under the condition {S['mem0']['q4_mean_fok']:.4f} (Mem0; intact {S['mem0']['intact_mean_fok']:.4f}) and {S['amem']['q4_mean_fok']:.4f} (A-MEM; intact {S['amem']['intact_mean_fok']:.4f});
distinct FOK values {S['mem0']['q4_distinct_values']} and {S['amem']['q4_distinct_values']}; items whose score equals the intact score exactly {S['mem0']['identical_to_intact']} of {S['mem0']['n']} and {S['amem']['identical_to_intact']} of {S['amem']['n']}.
Reading rule stated, not applied: where the two intervals disagree the weaker reading governs; nothing here is a verdict.

### AUX-Q4-SPEND

Billed from response usage at $0.40 / $1.60 per 1M: probe ${spend['probe']:.4f}, run ${spend['run']:.4f} — **total ${spend['total']:.4f}**; {spend['n_calls']} calls
({spend['cached']} served from cache, {spend['failed']} failures). Nothing on any other key; no embedding call.
"""
    io.open(LEDGER, "w", encoding="utf-8", newline="\n").write(txt)
    print(txt)


if __name__ == "__main__":
    {"lock": cmd_lock, "probe": cmd_probe, "project": cmd_project, "run": cmd_run, "score": cmd_score}[sys.argv[1]]()
