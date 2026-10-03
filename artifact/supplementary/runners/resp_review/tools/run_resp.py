"""run_resp.py -- RESP Phase B steps 5-6: the mini lanes of ADDENDUM_RESP.md (frozen 17e6328), sections
L1 (V2-OWN, TRUE-REDRAW), L2 (RETRIEVED, HYBRID), L3 (BLIND-NOGATE), and the scorer of section T.

MODEL CALLS: gpt-4.1-mini only, synchronous chat completions, temperature 0, seed 42, k = 1,
max_tokens 200, JSON mode, the E1 clamp, one retry on a parse failure; plus one served-identifier
probe per arm (E1.7). No Haiku, no Opus, no embedding call (the vectors are step 4's). Responses
cached under resp_review/cache/. The committed BLIND / INDEXED-TRUE rows are read, never re-elicited.

Subcommands, in order:  build | probe | project | run | score
  build    the five cells, asserted (102 / 102 / 661 / 661 / 302); every text present; verify_resp passes
  probe    one call per arm through the raw client: served identifier, tokens -> run/probes_resp.json
  project  probe tokens x calls against the $4 rule (section B), net of what is already billed
  run      the calls; stops submitting at $4 -> run/rows_resp.jsonl
  score    section T: common_e1r.auroc / boot_item / boot_cluster; the registered verdicts under their
           frozen texts; the descriptive rows; the spend -> run/scores_resp.json and NUMBERS_RESP.md
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import datetime as dt
import io
import json
import subprocess
import sys
import threading

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import resp_common as RC                                                     # noqa: E402
from resp_common import ROOT, RESP, L1, L2, RUN, CACHE, LEDGER, J, jdump      # noqa: E402
import prompts_resp as PR                                                    # noqa: E402
import prompts_e1 as P                                                       # noqa: E402
from common_e1r import auroc, boot_item, boot_cluster, N_BOOT, SEED          # noqa: E402

api = RC.e1_api()
LANE, PRICE = "gpt-4.1-mini", (0.40, 1.60)
BUDGET = 4.00
TOL = 0.05
ROWS_P = RUN / "rows_resp.jsonl"
ARMS = ("V2-OWN", "TRUE-REDRAW", "RETRIEVED", "HYBRID", "BLIND-NOGATE")
STATES = (("sup", "supersession"), ("exp", "expiry"), ("ret", "retraction"))
LEDGER_KEYS = ["AUX-RESP-L1-CENSUS", "AUX-RESP-L1-TAU", "AUX-RESP-L1-LOCK", "AUX-RESP-L1-NB6-GATE", "AUX-RESP-L1-NB6",
               "AUX-RESP-L1-MINI", "AUX-RESP-L1-REDRAW", "AUX-RESP-L2-RETRIEVER", "AUX-RESP-L2-REACH", "AUX-RESP-L2-PROMPTS",
               "AUX-RESP-L2-MINI-NOK", "AUX-RESP-L2-MINI-FOK", "AUX-RESP-L3-PROMPT", "AUX-RESP-L3-MINI", "AUX-RESP-PAPER-Q4",
               "AUX-RESP-SPEND", "AUX-RESP-BUDGETRULE"]


def clamp(v):
    """elicit_e1.clamp, verbatim: 0-100 -> [0, 1]."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return min(100.0, max(0.0, f)) / 100.0


def assert_lineage():
    assert P.file_sha256() == RC.PIN_PROMPTS["file"] and P.texts_sha256() == RC.PIN_PROMPTS["texts"], "prompts_e1 digest drift -- STOP"
    assert (P.MODEL, P.TEMPERATURE, P.SEED, P.MAX_TOKENS) == (LANE, 0, 42, 200), "lane drift -- STOP"


def redirect_cache():
    CACHE.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                             # noqa: SLF001
    e0.CACHE_PATH = CACHE / "responses.json"; e0.LEDGER_PATH = CACHE / "cost_ledger.json"
    e0._cache = None; e0._load_cache()                                       # noqa: SLF001
    return e0


# ------------------------------------------------------------------ build
def build_cell():
    sub = RC.load_cell()
    own = J(L1 / "indexes_own.json")["items"]
    ret = J(L2 / "retrieval.json")["items"]
    idx = RC.indexes()
    base = lambda it: {"item_id": it["item_id"], "persona": it["persona"], "question": it["question"], "label": it["label"],
                       "state": it["state"], "y_nok": it["y_nok"], "y_fok": it["y_fok"], "tier": it["tier"], "index_key": it["index_key"]}
    cell = {a: [] for a in ARMS}
    for it in sub:
        if own[it["item_id"]]["changed"]:
            cell["V2-OWN"].append({**base(it), "arm": "V2-OWN"})
            cell["TRUE-REDRAW"].append({**base(it), "arm": "TRUE-REDRAW"})
        cell["RETRIEVED"].append({**base(it), "arm": "RETRIEVED"})
        cell["HYBRID"].append({**base(it), "arm": "HYBRID"})
    seen = set()
    for it in sub:
        if it["question"] not in seen:
            seen.add(it["question"])
            cell["BLIND-NOGATE"].append({"item_id": "blind", "question": it["question"], "arm": "BLIND-NOGATE", "persona": it["persona"],
                                         "label": "-", "state": "-", "y_nok": None, "y_fok": None, "tier": "-", "index_key": "-"})
    assert tuple(len(cell[a]) for a in ARMS) == (102, 102, 661, 661, 302), tuple(len(cell[a]) for a in ARMS)
    texts = {"own": {k: v["text"] for k, v in own.items()}, "true": {it["item_id"]: idx[it["index_key"]] for it in sub},
             "block": {k: v["block"] for k, v in ret.items()}}
    return sub, cell, texts


def messages(row, texts):
    a, q = row["arm"], row["question"]
    if a == "V2-OWN":
        return [{"role": "system", "content": P.SYSTEM}, {"role": "user", "content": P.USER_INDEXED.format(index=texts["own"][row["item_id"]], question=q)}]
    if a == "TRUE-REDRAW":
        return [{"role": "system", "content": P.SYSTEM}, {"role": "user", "content": P.USER_INDEXED.format(index=texts["true"][row["item_id"]], question=q)}]
    if a == "RETRIEVED":
        return [{"role": "system", "content": PR.SYSTEM_RETRIEVED}, {"role": "user", "content": PR.USER_RETRIEVED.format(retrieved=texts["block"][row["item_id"]], question=q)}]
    if a == "HYBRID":
        return [{"role": "system", "content": PR.SYSTEM_RETRIEVED},
                {"role": "user", "content": PR.USER_HYBRID.format(index=texts["true"][row["item_id"]], retrieved=texts["block"][row["item_id"]], question=q)}]
    if a == "BLIND-NOGATE":
        return [{"role": "system", "content": PR.SYSTEM_NOGATE}, {"role": "user", "content": P.USER_BLIND.format(question=q)}]
    raise ValueError(a)


def cmd_build():
    assert_lineage()
    rc = subprocess.run([sys.executable, str(RESP / "tools" / "verify_resp.py")], capture_output=True, text=True, cwd=ROOT).returncode
    assert rc == 0, "verify_resp.py fails -- STOP"
    sub, cell, texts = build_cell()
    meta = {"registration": "registrations/ADDENDUM_RESP.md", "frozen": RC.FREEZE, "lane": LANE, "temperature": 0, "seed": 42, "max_tokens": 200, "k": 1,
            "prompts_e1": {"file": P.file_sha256(), "texts": P.texts_sha256()}, "prompts_resp": PR.digests(),
            "cells": {a: len(cell[a]) for a in ARMS}, "calls": sum(len(cell[a]) for a in ARMS),
            "committed_rows": "e1_metamemory/elicitation_main.json (BLIND by question; INDEXED-TRUE by tag); read, never re-elicited",
            "built": dt.date.today().isoformat()}
    RUN.mkdir(parents=True, exist_ok=True); jdump({"meta": meta, "cell": cell}, RUN / "cell_resp.json")
    print(json.dumps(meta, indent=1))


# ------------------------------------------------------------------ probe / project
def cmd_probe():
    assert_lineage(); e0 = redirect_cache()
    sub, cell, texts = build_cell()
    out = {}
    for arm in ARMS:
        first = cell[arm][0]
        r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,   # noqa: SLF001
                                                 messages=messages(first, texts), response_format={"type": "json_object"})
        o = api.parse_json(r.choices[0].message.content) or {}
        out[arm] = {"item_id": first["item_id"], "question": first["question"][:80], "served": r.model, "identifier_ok": LANE in r.model,
                    "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens,
                    "usd": r.usage.prompt_tokens / 1e6 * PRICE[0] + r.usage.completion_tokens / 1e6 * PRICE[1],
                    "status": "OK" if clamp(o.get("fok")) is not None and clamp(o.get("nok")) is not None else "PARSE_FAIL",
                    "sample": (r.choices[0].message.content or "")[:200], "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RUN / "probes_resp.json"); print(json.dumps(out, indent=1))
    if not all(v["identifier_ok"] for v in out.values()):
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if any(v["status"] != "OK" for v in out.values()):
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def billed_so_far():
    emb = J(L2 / "embedding_call.json")["usage"]["usd"] if (L2 / "embedding_call.json").exists() else 0.0
    probes = sum(v["usd"] for v in J(RUN / "probes_resp.json").values()) if (RUN / "probes_resp.json").exists() else 0.0
    run = sum(json.loads(l).get("usd", 0.0) for l in io.open(ROWS_P, encoding="utf-8")) if ROWS_P.exists() else 0.0
    return {"embedding": emb, "probes": probes, "run": run, "total": emb + probes + run}


def cmd_project():
    p = J(RUN / "probes_resp.json"); sub, cell, _ = build_cell()
    n = {a: len(cell[a]) for a in ARMS}
    tin = sum(p[a]["tok_in"] * n[a] for a in ARMS); tout = sum(p[a]["tok_out"] * n[a] for a in ARMS)
    usd = tin / 1e6 * PRICE[0] + tout / 1e6 * PRICE[1]; so_far = billed_so_far()
    per_arm = {a: {"calls": n[a], "tok_in": p[a]["tok_in"], "tok_out": p[a]["tok_out"], "usd": n[a] * (p[a]["tok_in"] / 1e6 * PRICE[0] + p[a]["tok_out"] / 1e6 * PRICE[1])} for a in ARMS}
    print(f"calls        : {sum(n.values())}  " + ", ".join(f"{a} {n[a]}" for a in ARMS) + " (k=1)")
    print(f"projected in : {tin:,} tok   out: {tout:,} tok   PROJECTED ${usd:.4f}   " + "; ".join(f"{a} ${per_arm[a]['usd']:.4f}" for a in ARMS))
    print(f"billed so far: ${so_far['total']:.4f} (embedding ${so_far['embedding']:.6f}, probes ${so_far['probes']:.4f}, run ${so_far['run']:.4f})")
    print(f"projected total ${usd + so_far['total']:.4f} against the ${BUDGET:.2f} rule (section B; x1.3 = ${1.3 * usd + so_far['total']:.4f})")
    jdump({"projected_usd": usd, "per_arm": per_arm, "billed_so_far": so_far, "budget": BUDGET, "when": dt.datetime.now().isoformat(timespec="seconds")}, RUN / "projection_resp.json")
    if usd + so_far["total"] > BUDGET:
        sys.exit("PROJECTION ABOVE THE $4 RULE -- STOP per section B")


# ------------------------------------------------------------------ run
def rowkey(r):
    return (r["item_id"] if r["arm"] != "BLIND-NOGATE" else r["question"], r["arm"])


def done_keys():
    ks = set()
    if ROWS_P.exists():
        for l in io.open(ROWS_P, encoding="utf-8"):
            r = json.loads(l); ks.add(rowkey(r))
    return ks


def elicit(row, texts):
    """elicit_e1.run in effect: one retry on a parse failure; the gated arms carry nok_candidates_found."""
    msgs = messages(row, texts); arm = row["arm"]; cid = row["item_id"]
    gated = arm != "BLIND-NOGATE"
    ok = lambda o: o is not None and clamp(o.get("fok")) is not None and clamp(o.get("nok")) is not None
    r = api.call(cid, arm, msgs); o = api.parse_json(r["content"]); n_calls, failed = 1, False
    usd = 0.0 if r["cached"] else r["prompt_tokens"] / 1e6 * PRICE[0] + r["completion_tokens"] / 1e6 * PRICE[1]
    if not ok(o):
        r2 = api.call(cid, arm + "#retry", msgs); o = api.parse_json(r2["content"]); n_calls = 2
        usd += 0.0 if r2["cached"] else r2["prompt_tokens"] / 1e6 * PRICE[0] + r2["completion_tokens"] / 1e6 * PRICE[1]
        r = r2
        if not ok(o):
            failed, o = True, {}
    return {**{k: row[k] for k in ("item_id", "arm", "persona", "question", "label", "state", "y_nok", "y_fok", "tier", "index_key")}, "draw": 1,
            "fok": clamp(o.get("fok")), "nok": clamp(o.get("nok")),
            "nok_candidates_found": (bool(o.get("nok_candidates_found")) if (gated and not failed) else None),
            "would_search": (bool(o.get("would_search")) if not failed else None),
            "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls, "cached": r["cached"],
            "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "usd": usd, "text": (r["content"] or "")[:300]}


def cmd_run():
    assert_lineage(); redirect_cache()
    sub, cell, texts = build_cell(); done = done_keys()
    jobs = [r for a in ARMS for r in cell[a] if rowkey(r) not in done]
    print(f"{len(jobs)} calls to go (resumed past {len(done)})", flush=True)
    lock, spend, stopped, n_done = threading.Lock(), [billed_so_far()["total"]], [False], [0]

    def work(row):
        with lock:
            if spend[0] >= BUDGET or stopped[0]:
                stopped[0] = True; return None
        r = elicit(row, texts)
        with lock:
            spend[0] += r["usd"]; n_done[0] += 1
            with io.open(ROWS_P, "a", encoding="utf-8") as f:
                f.write(json.dumps(r, sort_keys=True) + "\n")
            if n_done[0] % 100 == 0:
                print(f"  {n_done[0]} done, billed ${spend[0]:.4f}", flush=True)
                api.flush()
        return r
    try:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            out = [r for r in ex.map(work, jobs) if r is not None]
    finally:
        api.flush()
    c = collections.Counter((r["arm"], r["status"]) for r in out)
    print(f"DONE {len(out)} rows; status {dict(c)}; billed total ${spend[0]:.4f} against ${BUDGET:.2f}"
          + ("  >>> STOPPED AT THE $4 RULE with cells unscored" if stopped[0] else ""))
    if stopped[0]:
        sys.exit(1)


# ------------------------------------------------------------------ score
def load_rows():
    rows = [json.loads(l) for l in io.open(ROWS_P, encoding="utf-8")]
    by = {a: {} for a in ARMS}
    for r in rows:
        by[r["arm"]][r["item_id"] if r["arm"] != "BLIND-NOGATE" else r["question"]] = r
    return by


def auroc_ci(scores, y, n=N_BOOT, seed=SEED):
    """score_ladder.auroc_ci, verbatim: one-sample item-level bootstrap on a single-arm AUROC."""
    rng = np.random.default_rng(seed)
    s, yy = np.asarray(scores, float), np.asarray(y, int)
    vals = []
    for _ in range(n):
        k = rng.integers(0, len(yy), len(yy))
        if yy[k].sum() in (0, len(k)):
            continue
        vals.append(auroc(s[k], yy[k]))
    v = np.asarray(vals)
    return {"point": float(auroc(s, yy)), "ci_lo": float(np.percentile(v, 2.5)), "ci_hi": float(np.percentile(v, 97.5)),
            "includes_0.50": bool(np.percentile(v, 2.5) <= 0.50 <= np.percentile(v, 97.5)), "n_draws": int(len(v))}


def paired(b, i, y, g):
    b, i, y = np.asarray(b, float), np.asarray(i, float), np.asarray(y, int)
    return {"base": float(auroc(b, y)), "arm": float(auroc(i, y)), "D": float(auroc(i, y) - auroc(b, y)),
            "item": boot_item(b, i, y), "cluster": boot_cluster(b, i, y, np.asarray(g)), "n": int(len(y)), "n_pos": int(y.sum())}


def subpop(sub, st):
    """positives of one state with all 557 negatives (Table 20 construction); st None = whole population."""
    return [it for it in sub if it["y_nok"] == 0 or st is None or it["state"] == st]


def fmt_i(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]" if "ci_lo" in d else "[—]"


def score_all(write=True):
    sub = RC.load_cell(); by = load_rows(); own = J(L1 / "indexes_own.json")["items"]
    fails = {a: sum(1 for r in by[a].values() if r["status"] != "OK") for a in ARMS}
    okrow = lambda a, k: by[a].get(k) if by[a].get(k, {}).get("status") == "OK" else None
    S = {"failures": fails, "n_rows": {a: len(by[a]) for a in ARMS}}

    # ---------- L1
    def own_score(it):
        if own[it["item_id"]]["changed"]:
            r = okrow("V2-OWN", it["item_id"]); return None if r is None else r["nok"]
        return it["true"]["nok"]
    l1 = {}
    for st, name in [(None, "all")] + [(s, n) for s, n in STATES]:
        pop = [it for it in subpop(sub, st) if own_score(it) is not None]
        l1[name] = paired([it["true"]["nok"] for it in pop], [own_score(it) for it in pop], [it["y_nok"] for it in pop], [it["persona"] for it in pop])
    changed = [it for it in sub if own[it["item_id"]]["changed"]]
    redraw = {}
    for st, name in [(None, "all")] + [(s, n) for s, n in STATES]:
        pop = [it for it in changed if (st is None or it["y_nok"] == 0 or it["state"] == st) and okrow("TRUE-REDRAW", it["item_id"]) and own_score(it) is not None]
        y = [it["y_nok"] for it in pop]
        if sum(y) == 0 or sum(y) == len(y):
            redraw[name] = {"note": "no positives of this state among the 102 changed items", "n": len(pop), "n_pos": int(sum(y))}; continue
        redraw[name] = {"redraw_minus_true": paired([it["true"]["nok"] for it in pop], [by["TRUE-REDRAW"][it["item_id"]]["nok"] for it in pop], y, [it["persona"] for it in pop]),
                        "own_minus_true_same_items": paired([it["true"]["nok"] for it in pop], [own_score(it) for it in pop], y, [it["persona"] for it in pop])}
        redraw[name]["inside_draw_noise"] = abs(redraw[name]["own_minus_true_same_items"]["D"]) <= abs(redraw[name]["redraw_minus_true"]["D"])
    d = l1["supersession"]
    p1_item = d["D"] < -TOL and d["item"].get("ci_hi", 1) < 0
    p1_clu = d["D"] < -TOL and d["cluster"].get("ci_hi", 1) < 0
    p2 = all(abs(l1[n]["D"]) <= TOL for n in ("expiry", "retraction"))
    l1_v = {"L1-P1": {"holds": bool(p1_item and p1_clu), "item_reading": bool(p1_item), "cluster_reading": bool(p1_clu), "disagree": bool(p1_item != p1_clu)},
            "L1-P2": {"holds": bool(p2), "expiry_D": l1["expiry"]["D"], "retraction_D": l1["retraction"]["D"]}}
    X, Y, D, I, Ic = d["base"], d["arm"], d["D"], fmt_i(d["item"]), fmt_i(d["cluster"])
    if l1_v["L1-P1"]["holds"]:
        l1_v["L1-P1"]["text"] = (f"Removing the target's own name and its nearest neighbours from the superseded-names section costs the smallest model "
                                 f"{abs(D):.4f} of its supersession discrimination ({X:.4f} to {Y:.4f}, interval {I}; persona-clustered {Ic}): the obligation is read off the name, as the manuscript says.")
    else:
        l1_v["L1-P1"]["text"] = (f"With the target's own attribute name and its nearest neighbours under the matcher's encoder removed from the superseded-names "
                                 f"section — the only place the summary names anything — the smallest model's obligation discrimination on supersession-derived items "
                                 f"moves from {X:.4f} to {Y:.4f}, a paired difference of {D:+.4f} with interval {I} (persona-clustered {Ic}), which does not fall below the "
                                 f"truthful level by more than the tolerance with an interval excluding zero. The reader is recovering the obligation from something other "
                                 f"than the name: the superseded counts survive in the lifecycle totals and the per-category table, and this ablation does not remove them.")
        if l1_v["L1-P1"]["disagree"]:
            l1_v["L1-P1"]["text"] += " The item-level and the persona-clustered intervals disagree on this prediction; the weaker reading governs."
    if p2:
        l1_v["L1-P2"]["text"] = ("On the two states the summary only counts, the ablation changes nothing within tolerance: those obligations were never read from a name. "
                                 f"(expiry {l1['expiry']['D']:+.4f} {fmt_i(l1['expiry']['item'])}; retraction {l1['retraction']['D']:+.4f} {fmt_i(l1['retraction']['item'])}, "
                                 f"11 of 26 retraction-derived obligations named in the section, registration §C.2.)")
    else:
        bad = [(n, l1[n]) for n in ("expiry", "retraction") if abs(l1[n]["D"]) > TOL]
        l1_v["L1-P2"]["text"] = " ".join(
            f"On {n}-derived items, which the summary only counts and never names, the ablation moves the smallest model's discrimination by {v['D']:+.4f} "
            f"with interval {fmt_i(v['item'])} (persona-clustered {fmt_i(v['cluster'])}), outside the tolerance. The change cannot come from a name the positives carried; "
            f"it comes through the negatives whose names were removed, or through the model's response to a section that now reads \"(none)\" against non-zero counts. "
            f"The per-state reading of Table 20 is not clean of the ablation on this state." for n, v in bad) + " (Retraction: 11 of 26 named in the section, §C.2.)"
    S["L1"] = {"per_state": l1, "redraw": redraw, "verdicts": l1_v}

    # ---------- L2
    l2 = {}
    for arm in ("RETRIEVED", "HYBRID"):
        arm_rows = {}
        for st, name in [(None, "all")] + [(s, n) for s, n in STATES]:
            pop = [it for it in subpop(sub, st) if okrow(arm, it["item_id"])]
            arm_rows[name] = paired([it["true"]["nok"] for it in pop], [by[arm][it["item_id"]]["nok"] for it in pop], [it["y_nok"] for it in pop], [it["persona"] for it in pop])
        hard = [it for it in sub if it["tier"] == "hard" and okrow(arm, it["item_id"])]
        arm_rows["fok_307_vs_true"] = paired([it["true"]["fok"] for it in hard], [by[arm][it["item_id"]]["fok"] for it in hard], [it["y_fok"] for it in hard], [it["persona"] for it in hard])
        arm_rows["fok_307_vs_blind"] = paired([it["blind"]["fok"] for it in hard], [by[arm][it["item_id"]]["fok"] for it in hard], [it["y_fok"] for it in hard], [it["persona"] for it in hard])
        arm_rows["blind_nok_all"] = float(auroc([it["blind"]["nok"] for it in sub if okrow(arm, it["item_id"])], [it["y_nok"] for it in sub if okrow(arm, it["item_id"])]))
        l2[arm] = arm_rows
    dR, dH = l2["RETRIEVED"]["all"], l2["HYBRID"]["all"]
    r_item = dR["D"] < -TOL and dR["item"].get("ci_hi", 1) < 0
    r_clu = dR["D"] < -TOL and dR["cluster"].get("ci_hi", 1) < 0
    l2_v = {"L2-P1": {"holds": bool(r_item and r_clu), "item_reading": bool(r_item), "cluster_reading": bool(r_clu), "disagree": bool(r_item != r_clu)},
            "L2-P2": {"holds": bool(abs(dH["D"]) <= TOL)}}
    R, T, D, I, Ic = dR["arm"], dR["base"], dR["D"], fmt_i(dR["item"]), fmt_i(dR["cluster"])
    if l2_v["L2-P1"]["holds"]:
        l2_v["L2-P1"]["text"] = (f"A monitor shown the five most similar entries with their lifecycle metadata, and no summary, falls {abs(D):.4f} short of the summary on "
                                 f"obligation ({R:.4f} against {T:.4f}, interval {I}; persona-clustered {Ic}); the bounded retrieved view does not carry what the summary carries.")
    else:
        l2_v["L2-P1"]["text"] = (f"A monitor shown the five most similar entries with their lifecycle metadata, and no summary, scores {R:.4f} on obligation against {T:.4f} "
                                 f"under the truthful summary, a paired difference of {D:+.4f} with interval {I} (persona-clustered {Ic}) that does not fall below the summary by "
                                 f"more than the tolerance. On this population a five-item view carries the obligation signal the summary carries; the argument that a bounded "
                                 f"retrieved view cannot settle the judgment is not supported at k = 5 here.")
        if l2_v["L2-P1"]["disagree"]:
            l2_v["L2-P1"]["text"] += " The item-level and the persona-clustered intervals disagree on this prediction; the weaker reading governs."
    H, Dh, Ih, Ihc = dH["arm"], dH["D"], fmt_i(dH["item"]), fmt_i(dH["cluster"])
    if l2_v["L2-P2"]["holds"]:
        l2_v["L2-P2"]["text"] = (f"Given the summary, the five retrieved entries add nothing within tolerance ({T:.4f} to {H:.4f}, {Dh:+.4f}, interval {Ih}; persona-clustered {Ihc}): "
                                 f"the summary supplies what retrieval cannot, and retrieval adds nothing to it.")
    else:
        incl = not dH["item"].get("excludes_zero", False)
        if Dh > 0:
            l2_v["L2-P2"]["text"] = (f"Adding the five retrieved entries to the truthful summary raises the smallest model's obligation discrimination from {T:.4f} to {H:.4f}, "
                                     f"a paired difference of {Dh:+.4f} with interval {Ih} (persona-clustered {Ihc}) above the tolerance. Retrieved items carry obligation signal the "
                                     f"summary does not: the summary names superseded content and only counts the other two states, and a retrieved entry flagged retracted or "
                                     f"expired is a name the summary never prints.")
        else:
            l2_v["L2-P2"]["text"] = (f"Adding the five retrieved entries to the truthful summary lowers the smallest model's obligation discrimination from {T:.4f} to {H:.4f}, "
                                     f"a paired difference of {Dh:+.4f} with interval {Ih} (persona-clustered {Ihc}) below the tolerance. The retrieved view does not add to the "
                                     f"summary; it takes from it.")
        if incl:
            l2_v["L2-P2"]["text"] += " — with an interval that includes zero"; l2_v["L2-P2"]["no_verdict"] = True
    reach = J(L2 / "reach.json")
    l2_v["L2-P3"] = {"holds": reach["L2-P3"]["verdict"] == "HOLDS", "rate": reach["k5"]["rate"], "text": reach["L2-P3"]["text"]}
    S["L2"] = {"arms": l2, "verdicts": l2_v, "reach": reach["k5"]}

    # ---------- L3
    ng = {q: r for q, r in by["BLIND-NOGATE"].items() if r["status"] == "OK"}
    pop = [it for it in sub if it["question"] in ng]
    vals = collections.Counter(ng[it["question"]]["nok"] for it in pop)
    scores = [ng[it["question"]]["nok"] for it in pop]; y = [it["y_nok"] for it in pop]
    ci = auroc_ci(scores, y)
    a_ok, b_ok = len(vals) > 2, ci["includes_0.50"]
    modal = vals.most_common(1)[0]
    desc = paired(scores, [it["true"]["nok"] for it in pop], y, [it["persona"] for it in pop])   # INDEXED-TRUE minus NOGATE (descriptive)
    l3_v = {"L3-P1": {"holds": bool(a_ok and b_ok), "a_distinct_gt_2": bool(a_ok), "b_includes_0.5": bool(b_ok)}}
    V, N, A, I = len(vals), modal[1], ci["point"], f"[{ci['ci_lo']:.4f}, {ci['ci_hi']:.4f}]"
    if a_ok and b_ok:
        l3_v["L3-P1"]["text"] = (f"Without the detection step the smallest model's blind obligation score takes {V} distinct values and its discrimination, {A:.4f} with "
                                 f"interval {I}, includes chance: the constant was the gate, and removing it does not give the blind arm a ranking to improve on. The manuscript says so at L477.")
    elif not a_ok:
        l3_v["L3-P1"]["text"] = (f"With the detection step removed and the probability elicited directly, the smallest model's blind obligation score still takes {V} distinct "
                                 f"values across the {len(pop)} questions ({N} at the modal value). The constant was not the gate: the reviewer's explanation is not supported, "
                                 f"and the smallest model's blind obligation judgment is flat under either rubric.")
    else:
        l3_v["L3-P1"]["text"] = (f"With the detection step removed, the smallest model's blind obligation score takes {V} distinct values and reaches {A:.4f} with interval {I} "
                                 f"excluding 0.5. The gate was pinning the score, and without it the blind arm carries a ranking on these questions; the manuscript's reading of the "
                                 f"smallest model's indexed level against the lookup, rather than against a blind gain, is then a consequence of the rubric and says so.")
    S["L3"] = {"n_items": len(pop), "n_questions": len(ng), "values": {str(k): v for k, v in sorted(vals.items())}, "n_distinct": V, "modal": list(modal),
               "auroc_one_sample": ci, "indexed_true_minus_nogate_descriptive": desc, "verdicts": l3_v,
               "fok_values": {str(k): v for k, v in sorted(collections.Counter(ng[it["question"]]["fok"] for it in pop).items())}}

    # ---------- spend
    S["spend"] = billed_so_far()
    S["spend"]["under_4"] = S["spend"]["total"] < BUDGET
    S["when"] = dt.datetime.now().isoformat(timespec="seconds")
    if write:
        jdump(S, RUN / "scores_resp.json")
    return S


def compare_scores(a, b, path="", out=None):
    out = [] if out is None else out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a:
            if k in ("when", "spend"):
                continue
            if k not in b:
                out.append(path + "/" + k + " missing"); continue
            compare_scores(a[k], b[k], path + "/" + k, out)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        if abs(float(a) - float(b)) > 1e-9:
            out.append(f"{path}: {a} != {b}")
    elif a != b:
        out.append(f"{path}: {str(a)[:40]} != {str(b)[:40]}")
    return out


def ledger_text(S):
    l1, l2, l3 = S["L1"], S["L2"], S["L3"]
    today = dt.date.today().isoformat()
    row = lambda name, d: f"| {name} | {d['n']} / {d['n_pos']} | {d['base']:.4f} | {d['arm']:.4f} | {d['D']:+.4f} | {fmt_i(d['item'])} | {fmt_i(d['cluster'])} |"
    hdr = "| row | n / positives | TRUE (committed) | arm | D | item-level 95% | persona-clustered 95% |\n|---|---|---:|---:|---:|---|---|"
    out = f"""
---

## 5. Steps 5–6 — the mini lanes, scored (written {today})

Lane: `gpt-4.1-mini` (served identifier probed per arm, `run/probes_resp.json`), temperature 0, seed 42,
k = 1, max_tokens 200, JSON mode, the E1 clamp, one retry on a parse failure; rows `run/rows_resp.jsonl`
({', '.join(f'{a} {S["n_rows"][a]}' for a in ARMS)}); elicitation failures {S['failures']}. Estimators: `common_e1r.auroc`
(Mann-Whitney, ties 0.5), `boot_item` (1,000 draws, seed 42, single-class draws discarded), `boot_cluster`
beside; the weaker reading governs where they disagree. Tolerance ±0.05. Per-state rows: positives of
one state against the same 557 negatives.

### AUX-RESP-L1-MINI — V2-OWN against the committed TRUE rows (NOK)

{hdr}
{row('whole population', l1['per_state']['all'])}
{row('supersession-derived (63)', l1['per_state']['supersession'])}
{row('expiry-derived (15)', l1['per_state']['expiry'])}
{row('retraction-derived (26)', l1['per_state']['retraction'])}

**L1-P1** (D_sup < −0.05, item-level interval excluding zero; clustered beside, weaker governs): item-level reading {'holds' if l1['verdicts']['L1-P1']['item_reading'] else 'fails'}, persona-clustered reading {'holds' if l1['verdicts']['L1-P1']['cluster_reading'] else 'fails'} → **{'HOLDS' if l1['verdicts']['L1-P1']['holds'] else 'FAILS'}**. Frozen text with its numbers:
> {l1['verdicts']['L1-P1']['text']}

**L1-P2** (|D_exp| ≤ 0.05 and |D_ret| ≤ 0.05): expiry {l1['verdicts']['L1-P2']['expiry_D']:+.4f}, retraction {l1['verdicts']['L1-P2']['retraction_D']:+.4f} → **{'HOLDS' if l1['verdicts']['L1-P2']['holds'] else 'FAILS'}**. Frozen text with its numbers:
> {l1['verdicts']['L1-P2']['text']}

NB-6 on the ablated list is `AUX-RESP-L1-NB6` (§2).

### AUX-RESP-L1-REDRAW — the draw-noise floor on the 102 changed items (descriptive)

REDRAW − TRUE and V2-OWN − TRUE on the same 102 items (per state: positives of the state among the 102 against the 28 changed negatives).

| population | n / positives | REDRAW − TRUE (item-level; clustered) | V2-OWN − TRUE on the same items | inside the draw noise |
|---|---|---|---|---|
""" + "\n".join(
        (f"| {name} | {v['redraw_minus_true']['n']} / {v['redraw_minus_true']['n_pos']} | {v['redraw_minus_true']['D']:+.4f} {fmt_i(v['redraw_minus_true']['item'])}; {fmt_i(v['redraw_minus_true']['cluster'])} "
         f"| {v['own_minus_true_same_items']['D']:+.4f} {fmt_i(v['own_minus_true_same_items']['item'])} | {'yes' if v['inside_draw_noise'] else 'no'} |")
        if "redraw_minus_true" in v else f"| {name} | {v['n']} / {v['n_pos']} | — | — | {v['note']} |"
        for name, v in l1["redraw"].items()) + f"""

**Reading rule (§L1):** where |V2-OWN − TRUE| on a state does not exceed |REDRAW − TRUE| on the same state, the ablation is inside the draw noise there: {', '.join(f"{n} {'inside' if v.get('inside_draw_noise') else 'outside'}" for n, v in l1['redraw'].items() if 'inside_draw_noise' in v)}.

### AUX-RESP-L2-MINI-NOK — RETRIEVED and HYBRID against the committed TRUE rows (NOK, 661)

{hdr}
{row('RETRIEVED, whole', l2['arms']['RETRIEVED']['all'])}
{row('RETRIEVED, supersession', l2['arms']['RETRIEVED']['supersession'])}
{row('RETRIEVED, expiry', l2['arms']['RETRIEVED']['expiry'])}
{row('RETRIEVED, retraction', l2['arms']['RETRIEVED']['retraction'])}
{row('HYBRID, whole', l2['arms']['HYBRID']['all'])}
{row('HYBRID, supersession', l2['arms']['HYBRID']['supersession'])}
{row('HYBRID, expiry', l2['arms']['HYBRID']['expiry'])}
{row('HYBRID, retraction', l2['arms']['HYBRID']['retraction'])}

Committed blind NOK on the 661: {l2['arms']['RETRIEVED']['blind_nok_all']:.4f} (descriptive; anchors no gain, R96).

**L2-P1** (RETRIEVED − TRUE < −0.05, item-level interval excluding zero; clustered beside, weaker governs): item-level reading {'holds' if l2['verdicts']['L2-P1']['item_reading'] else 'fails'}, persona-clustered reading {'holds' if l2['verdicts']['L2-P1']['cluster_reading'] else 'fails'} → **{'HOLDS' if l2['verdicts']['L2-P1']['holds'] else 'FAILS'}**. Frozen text with its numbers:
> {l2['verdicts']['L2-P1']['text']}

**L2-P2** (|HYBRID − TRUE| ≤ 0.05, point estimate): → **{'HOLDS' if l2['verdicts']['L2-P2']['holds'] else ('no verdict (outside tolerance, interval includes zero)' if l2['verdicts']['L2-P2'].get('no_verdict') else 'FAILS')}**. Frozen text with its numbers:
> {l2['verdicts']['L2-P2']['text']}

**L2-P3** (reach at k = 5 < 0.20): {l2['reach']['reached']} of {l2['reach']['n']} = {l2['reach']['rate']:.4f} → **{'HOLDS' if l2['verdicts']['L2-P3']['holds'] else 'FAILS'}** (`AUX-RESP-L2-REACH`, §4, frozen text printed there).

### AUX-RESP-L2-MINI-FOK — the FOK rows on the 307 (descriptive, no bar)

| arm | vs TRUE (0.7003): arm, D, item-level, clustered | vs blind (0.4966): D, item-level, clustered |
|---|---|---|
""" + "\n".join(
        f"| {a} | {v['fok_307_vs_true']['arm']:.4f}, {v['fok_307_vs_true']['D']:+.4f}, {fmt_i(v['fok_307_vs_true']['item'])}, {fmt_i(v['fok_307_vs_true']['cluster'])} "
        f"| {v['fok_307_vs_blind']['D']:+.4f}, {fmt_i(v['fok_307_vs_blind']['item'])}, {fmt_i(v['fok_307_vs_blind']['cluster'])} |"
        for a, v in l2["arms"].items()) + f"""

Expectation stated in advance (§L2): RETRIEVED FOK at or above TRUE's — {'as expected' if l2['arms']['RETRIEVED']['fok_307_vs_true']['D'] >= 0 else 'not as expected'} ({l2['arms']['RETRIEVED']['fok_307_vs_true']['D']:+.4f}).

### AUX-RESP-L3-MINI — BLIND-NOGATE

Scores attached to the 661 items by question text ({l3['n_questions']} questions, {l3['n_items']} items). Value distribution of `nok`: {l3['values']} — **{l3['n_distinct']} distinct values**, modal value {l3['modal'][0]} on {l3['modal'][1]} items. `fok` distribution (stored, not scored): {l3['fok_values']}.
One-sample AUROC (the ladder rule, item-level, 1,000 draws, seed 42): **{l3['auroc_one_sample']['point']:.4f}** [{l3['auroc_one_sample']['ci_lo']:.4f}, {l3['auroc_one_sample']['ci_hi']:.4f}], includes 0.50: {l3['auroc_one_sample']['includes_0.50']}.

**L3-P1** ((a) more than two distinct values: {l3['verdicts']['L3-P1']['a_distinct_gt_2']}; (b) interval includes 0.5: {l3['verdicts']['L3-P1']['b_includes_0.5']}) → **{'HOLDS' if l3['verdicts']['L3-P1']['holds'] else 'FAILS'}**. Frozen text with its numbers:
> {l3['verdicts']['L3-P1']['text']}

Descriptive only (not a rubric-matched gain — the committed indexed arm was elicited under the gated rubric): INDEXED-TRUE − BLIND-NOGATE = {l3['indexed_true_minus_nogate_descriptive']['D']:+.4f} {fmt_i(l3['indexed_true_minus_nogate_descriptive']['item'])}; persona-clustered {fmt_i(l3['indexed_true_minus_nogate_descriptive']['cluster'])} (INDEXED-TRUE {l3['indexed_true_minus_nogate_descriptive']['arm']:.4f}).

### AUX-RESP-SPEND and AUX-RESP-BUDGETRULE

Billed on the OpenAI key, from response usage at $0.40 / $1.60 per 1M (`gpt-4.1-mini`) and $0.02 per 1M (`text-embedding-3-small`): embedding ${S['spend']['embedding']:.6f}, identifier probes ${S['spend']['probes']:.4f}, run ${S['spend']['run']:.4f} — **total ${S['spend']['total']:.4f}**, under the $4 rule ({'yes' if S['spend']['under_4'] else 'NO'}). Nothing on the Anthropic key; no Haiku, no Opus; no monitor call on any model other than `gpt-4.1-mini`. Projection before launch: `run/projection_resp.json`.
"""
    return out


def cmd_score():
    sys.stdout.reconfigure(encoding="utf-8")
    S = score_all(write=True)
    txt = ledger_text(S)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    {"build": cmd_build, "probe": cmd_probe, "project": cmd_project, "run": cmd_run, "score": cmd_score}[sys.argv[1]]()
