"""run_pad.py -- ADDENDUM_PAD §3-§6: build, gate, probe, the mini lane, scoring.

Registration: registrations/ADDENDUM_PAD.md (registered text sha256 93e33022…, frozen at dab8956).
Descriptive: no prediction, no bar, no verdict; the §5 branches print as they come out.

Subcommands, in order:
  build    pools, padded lists (nested, D-PAD-1), padded texts, renderer lock (242 / 242 or STOP),
           the lookup gate on the committed lists (0.7484 / 0.5738 at four decimals or STOP), the
           mini recorded-row gate (0.7339), both lookups on the padded lists -> pad_probe/build/*.json.
           No model call.
  probe    three direct gpt-4.1-mini calls (one item at each L; served identifier asserted, E1.7 rule)
           and the projection from o200k token counts over every prompt, against the $2.50 line and
           the combined $15 headroom -> pad_probe/build/probe.json. Refuses to launch if over.
  run      the mini lane: 3 x 661 calls through e1_metamemory/tools/api.py (JSON mode, temperature 0,
           seed 42, max_tokens 200; one retry on a parse failure), cache under pad_probe/cache/,
           arms PAD-15 / PAD-30 / PAD-60 -> pad_probe/rows/mini_pad.json. Hard cap $2.50.
  score    AUROC whole and per state at 1.75 / 15 / 30 / 60 for the three readers; paired differences
           against the recorded row with both bootstraps; distinct nok values; the §5 branches
           -> pad_probe/results/pad_scores.json.
"""
from __future__ import annotations

import concurrent.futures as cf
import hashlib
import io
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pad_common as PC  # noqa: E402
from pad_common import (BELIEVED, GATE, LENGTHS, PAD, RECORDED, REG_SHA, jdump, jload)  # noqa: E402
from sweep_common import auroc, boot_cluster, boot_item, committed_scores, state_mask  # noqa: E402

BUILD, ROWS, RES = PAD / "build", PAD / "rows", PAD / "results"
LINE_USD = 2.50
COMBINED_CAP = 15.00
PRICE_IN, PRICE_OUT = 0.40, 1.60
STATES = ("superseded", "retracted", "expired")
TOL = 0.05


def lists_json(lists):
    return {f"{k}|{L}": v for (k, L), v in lists.items()}


def lists_from_json(d):
    out = {}
    for kk, v in d.items():
        k, L = kk.rsplit("|", 1)
        out[(k, int(L))] = v
    return out


# ------------------------------------------------------------------ build
def cmd_build():
    assert PC.registration_ok(), "STOP: registration sha256 mismatch"
    assert PC.prompts_digests_ok(), "STOP: prompts_e1 digests differ from E1's"
    rows = PC.rows_661()
    pools = PC.build_pools(rows)
    ok, bad = PC.renderer_lock(pools)
    print(f"renderer lock: {ok} of {len(pools)}" + (f"  BAD {bad}" if bad else ""))
    if bad:
        raise SystemExit("STOP: renderer lock failed")
    lists, meta = PC.padded_lists(rows, pools)
    texts = PC.padded_texts(pools, lists)
    y = np.array([r["y"] for r in rows], int)
    # the lookup gate: the committed lists (as committed, marker included) through run_nb6's functions
    lex_b, emb_b = committed_scores(rows, {r["key"]: r["base_marker"] for r in rows})
    gate = {"emb": float(auroc(emb_b, y)), "lex": float(auroc(lex_b, y))}
    gate_ok = all(round(gate[k], 4) == GATE[k] for k in GATE)
    print(f"lookup gate on the committed lists: emb {gate['emb']:.4f} lex {gate['lex']:.4f}  {'PASS' if gate_ok else 'FAIL'}")
    if not gate_ok:
        raise SystemExit("STOP: lookup gate failed at four decimals")
    mon = np.array([r["monitor"] for r in rows], float)
    mini_rec = float(auroc(mon, y))
    print(f"mini recorded row (INDEXED-TRUE nok): {mini_rec:.4f} (registered 0.7339)")
    assert round(mini_rec, 4) == RECORDED["mini"], mini_rec
    # marker-stripped base, descriptive (D-E1R-11)
    lex_c, emb_c = committed_scores(rows, {r["key"]: r["base"] for r in rows})
    # the padded lists, both lookups
    padded = {}
    for L in LENGTHS:
        lst = {r["key"]: lists[(r["key"], L)] for r in rows}
        assert all(len(v) == L for v in lst.values())
        lx, em = committed_scores(rows, lst)
        padded[L] = {"lex": lx.tolist(), "emb": em.tolist()}
        print(f"L={L}: emb {auroc(em, y):.4f} lex {auroc(lx, y):.4f}")
    ex = PC.targeted_slots()
    census = {k: {**P["census"], "persona": P["persona"], "committed_names": P["committed"],
                  **{f"from_pool_a_L{L}": meta[(k, L)]["from_pool_a"] for L in LENGTHS},
                  **{f"from_pool_b_L{L}": meta[(k, L)]["from_pool_b"] for L in LENGTHS}} for k, P in pools.items()}
    excl = {p: {"literal": sorted(d["literal"]), "wide_only": sorted(d["wide_only"]), "n_items": d["n_items"], "n_pn": d["n_pn"],
                "n_present": d["n_present"], "n_absent": d["n_absent"]} for p, d in ex.items()}
    tsha = hashlib.sha256("\x1f".join(texts[(k, L)] for k in sorted(pools) for L in LENGTHS).encode("utf-8")).hexdigest()
    jdump({"registration_sha256": REG_SHA, "n_rows": len(rows), "n_keys": len(pools), "renderer_lock": {"ok": ok, "bad": bad},
           "lookup_gate": {"got": gate, "expected": GATE, "ok": gate_ok}, "mini_recorded_auroc": mini_rec,
           "base_marker_stripped": {"emb": float(auroc(emb_c, y)), "lex": float(auroc(lex_c, y))},
           "longest_committed_list": max(len(P["committed"]) for P in pools.values()),
           "mean_names_per_item_committed": float(np.mean([len(r["base_marker"]) for r in rows])),
           "mean_names_per_item_committed_marker_stripped": float(np.mean([len(r["base"]) for r in rows])),
           "pool_census": census, "exclusion_ii": excl, "texts_sha256": tsha,
           "contamination_check": {f"L{L}": {"neg_own_named": int(sum(1 for r in rows if r["y"] == 0 and set(r["own"]) & set(lists[(r["key"], L)]))),
                                             "pos_own_named": int(sum(1 for r in rows if r["y"] == 1 and set(r["own"]) & set(lists[(r["key"], L)])))}
                                   for L in ("base",) + LENGTHS if L != "base"} | {"base": {"neg_own_named": int(sum(1 for r in rows if r["y"] == 0 and set(r["own"]) & set(r["base"]))),
                                                                                     "pos_own_named": int(sum(1 for r in rows if r["y"] == 1 and set(r["own"]) & set(r["base"])))}}},
          BUILD / "build_pad.json")
    jdump(lists_json(lists), BUILD / "padded_lists.json")
    jdump(lists_json(texts), BUILD / "padded_texts.json")
    jdump({"rows": [{k: r[k] for k in ("item_id", "persona", "question", "y", "state", "label", "variant", "key", "base", "base_marker", "own", "monitor")} for r in rows],
           "scores": {"base_marker": {"lex": lex_b.tolist(), "emb": emb_b.tolist()}, "base_clean": {"lex": lex_c.tolist(), "emb": emb_c.tolist()},
                      **{f"L{L}": padded[L] for L in LENGTHS}}}, BUILD / "lookup_scores.json")
    print(f"wrote {BUILD}; texts sha256 {tsha[:16]}")


# ------------------------------------------------------------------ probe and projection
def _messages(text, question):
    import prompts_e1 as P
    return [{"role": "system", "content": P.SYSTEM},
            {"role": "user", "content": P.USER_INDEXED.format(index=text, question=question)}]


def cmd_probe():
    import tiktoken
    import prompts_e1 as P
    from openai import OpenAI
    sys.path.insert(0, str(PC.ROOT / "r82_counterfactual" / "tools"))
    from run_cf import load_env
    load_env()
    rows = jload(BUILD / "lookup_scores.json")["rows"]
    texts = lists_from_json(jload(BUILD / "padded_texts.json"))
    enc = tiktoken.get_encoding("o200k_base")
    counts = {L: [] for L in LENGTHS}
    for r in rows:
        for L in LENGTHS:
            m = _messages(texts[(r["key"], L)], r["question"])
            counts[L].append(sum(len(enc.encode(x["content"])) for x in m))
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    probes = []
    for i, L in enumerate(LENGTHS):
        r = rows[i]
        m = _messages(texts[(r["key"], L)], r["question"])
        resp = client.chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,
                                              messages=m, response_format={"type": "json_object"})
        probes.append({"L": L, "item_id": r["item_id"], "served_model": resp.model, "prompt_tokens": resp.usage.prompt_tokens,
                       "completion_tokens": resp.usage.completion_tokens, "o200k_estimate": counts[L][i],
                       "content": resp.choices[0].message.content[:300], "system_fingerprint": getattr(resp, "system_fingerprint", None)})
    ok_id = all("gpt-4.1-mini" in p["served_model"] for p in probes)
    ratio = float(np.mean([p["prompt_tokens"] / p["o200k_estimate"] for p in probes]))
    out_mean = float(np.mean([p["completion_tokens"] for p in probes]))
    tin = sum(sum(counts[L]) for L in LENGTHS) * ratio
    n = 3 * len(rows)
    usd = tin / 1e6 * PRICE_IN + n * out_mean / 1e6 * PRICE_OUT
    proj = {"calls": n, "input_tokens_est": int(tin), "output_tokens_est": int(n * out_mean), "usd": round(usd, 4), "usd_x1.3": round(usd * 1.3, 4),
            "line_usd": LINE_USD, "combined_cap": COMBINED_CAP, "billed_so_far_combined": 0.0,
            "headroom_rule": "the cap less every lane already billed and every earlier lane's projection; this is the first lane",
            "headroom": COMBINED_CAP, "within_line": usd * 1.3 <= LINE_USD, "within_headroom": usd * 1.3 <= COMBINED_CAP,
            "mean_prompt_tokens_by_L": {str(L): float(np.mean(counts[L]) * ratio) for L in LENGTHS},
            "calibration_ratio_served_over_o200k": ratio, "mean_completion_tokens_probe": out_mean}
    probe_usd = sum(p["prompt_tokens"] for p in probes) / 1e6 * PRICE_IN + sum(p["completion_tokens"] for p in probes) / 1e6 * PRICE_OUT
    jdump({"probes": probes, "identifier_ok": ok_id, "projection": proj, "probe_usd": probe_usd}, BUILD / "probe.json")
    print(json.dumps({"identifier_ok": ok_id, "served": [p["served_model"] for p in probes], "projection": proj, "probe_usd": round(probe_usd, 5)}, indent=1))
    if not ok_id:
        raise SystemExit("STOP: served-identifier mismatch (E1.7)")
    if not (proj["within_line"] and proj["within_headroom"]):
        raise SystemExit("STOP: projection over the line or the combined headroom")


# ------------------------------------------------------------------ the mini lane
def _api():
    from resp_common import e1_api
    m = e1_api()
    m._e0.CACHE_PATH = PAD / "cache" / "responses.json"
    m._e0.LEDGER_PATH = PAD / "cache" / "cost_ledger.json"
    m._e0.HARD_CAP_USD = LINE_USD
    m._e0.ESCALATE_USD = 2.0
    m._e0._cache = None
    m._e0._load_cache()
    return m


def clamp(v):
    """elicit_e1.clamp, verbatim: 0-100 -> [0, 1]; None when unparseable."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return min(100.0, max(0.0, f)) / 100.0


def cmd_run():
    pr = jload(BUILD / "probe.json")
    assert pr["identifier_ok"] and pr["projection"]["within_line"] and pr["projection"]["within_headroom"], "STOP: probe/projection not clean"
    assert PC.registration_ok() and PC.prompts_digests_ok()
    api = _api()
    rows = jload(BUILD / "lookup_scores.json")["rows"]
    texts = lists_from_json(jload(BUILD / "padded_texts.json"))
    jobs = [(r, L) for L in LENGTHS for r in rows]

    def run(job):
        r, L = job
        arm = f"PAD-{L}"
        msgs = _messages(texts[(r["key"], L)], r["question"])
        resp = api.call(r["item_id"], arm, msgs)
        o = api.parse_json(resp["content"])
        failed, retried = False, False
        if o is None or clamp(o.get("fok")) is None:
            retried = True
            resp = api.call(r["item_id"], arm + "#retry", msgs)
            o = api.parse_json(resp["content"])
            if o is None or clamp(o.get("fok")) is None:
                failed, o = True, {}
        return {"arm": arm, "L": L, "item_id": r["item_id"], "question": r["question"], "fok": clamp(o.get("fok")), "nok": clamp(o.get("nok")),
                "nok_candidates_found": (bool(o.get("nok_candidates_found")) if not failed else None),
                "status": "ELICITATION_FAILED" if failed else "OK", "retried": retried, "cached": resp["cached"],
                "prompt_tokens": resp.get("prompt_tokens"), "completion_tokens": resp.get("completion_tokens")}

    out, t0 = [], time.time()
    try:
        with cf.ThreadPoolExecutor(max_workers=12) as ex:
            for n, rec in enumerate(ex.map(run, jobs), 1):
                out.append(rec)
                if n % 300 == 0:
                    api.flush()
                    print(f"  {n}/{len(jobs)}  ${api.meter()['usd']:.4f}", flush=True)
    finally:
        api.flush()
    m = api.meter()
    by_L = {L: [r for r in out if r["L"] == L] for L in LENGTHS}
    fails = {L: sum(1 for r in by_L[L] if r["status"] != "OK") for L in LENGTHS}
    print(f"done in {time.time() - t0:.0f}s; calls {m['calls']} cached {m['cached']} tokens {m['in']}+{m['out']} ${m['usd']:.4f}; failures {fails}")
    jdump({"meta": {"registration_sha256": REG_SHA, "model": "gpt-4.1-mini", "temperature": 0, "seed": 42, "max_tokens": 200, "json_mode": True,
                    "served_model_probe": jload(BUILD / "probe.json")["probes"][0]["served_model"], "meter": m, "failures": fails,
                    "seconds": round(time.time() - t0, 1), "retried": sum(1 for r in out if r["retried"])},
           "rows": out}, ROWS / "mini_pad.json")
    for L in LENGTHS:
        if fails[L] > 0.02 * len(by_L[L]):
            raise SystemExit(f"STOP: elicitation failures {fails[L]} > 2% at L={L}")


# ------------------------------------------------------------------ scoring
def paired(base, new, y, g):
    it, cl = boot_item(base, new, y), boot_cluster(base, new, y, g)
    d = float(auroc(new, y) - auroc(base, y))
    both = bool(it.get("excludes_zero") and cl.get("excludes_zero"))
    wide = it if (it.get("ci_hi", 0) - it.get("ci_lo", 0)) >= (cl.get("ci_hi", 0) - cl.get("ci_lo", 0)) else cl
    return {"delta": d, "ci_item": it, "ci_persona": cl, "both_exclude_zero": both, "agree": bool(it.get("excludes_zero") == cl.get("excludes_zero")),
            "weaker": {"which": "item" if wide is it else "persona", "ci_lo": wide.get("ci_lo"), "ci_hi": wide.get("ci_hi"), "excludes_zero": wide.get("excludes_zero")}}


def cmd_score():
    B = jload(BUILD / "lookup_scores.json")
    rows = B["rows"]
    for r in rows:
        r["pop"] = "661"                      # state_mask's convention switch
    y = np.array([r["y"] for r in rows], int)
    g = np.array([r["persona"] for r in rows])
    mini = jload(ROWS / "mini_pad.json")["rows"]
    mrows = {(r["item_id"], r["L"]): r for r in mini}
    readers = {"emb": {"base": np.array(B["scores"]["base_marker"]["emb"], float)},
               "lex": {"base": np.array(B["scores"]["base_marker"]["lex"], float)},
               "mini": {"base": np.array([r["monitor"] for r in rows], float)}}
    for L in LENGTHS:
        readers["emb"][L] = np.array(B["scores"][f"L{L}"]["emb"], float)
        readers["lex"][L] = np.array(B["scores"][f"L{L}"]["lex"], float)
        v = []
        for r in rows:
            m = mrows[(r["item_id"], L)]
            v.append(np.nan if m["nok"] is None else m["nok"])
        readers["mini"][L] = np.array(v, float)
    res = {"registration_sha256": REG_SHA, "n": len(rows), "n_pos": int(y.sum()), "tol": TOL, "readers": {}, "branches": {}}
    for name, S in readers.items():
        R = {"believed_row": BELIEVED[name]}
        base = S["base"]
        okm = ~np.isnan(base)
        for lab, arr in (("base", base),) + tuple((str(L), S[L]) for L in LENGTHS):
            ok = okm & ~np.isnan(arr)
            rec = {"n_scored": int(ok.sum()), "auroc": float(auroc(arr[ok], y[ok]))}
            for st in STATES:
                m = state_mask(rows, st) & ok
                rec[f"auroc_{st}"] = float(auroc(arr[m], y[m]))
            if name == "mini":
                rec["distinct_nok"] = int(len(np.unique(arr[ok])))
                rec["mean_nok"] = float(np.mean(arr[ok]))
            if lab != "base":
                rec["paired_vs_base"] = paired(base[ok], arr[ok], y[ok], g[ok])
                for st in STATES:
                    m = state_mask(rows, st) & ok
                    rec[f"paired_vs_base_{st}"] = paired(base[m], arr[m], y[m], g[m])
            R[lab] = rec
        # §5 branches, whole population
        flat = all(abs(R[str(L)]["paired_vs_base"]["delta"]) <= TOL for L in LENGTHS)
        deg = [L for L in LENGTHS if R[str(L)]["paired_vs_base"]["delta"] < -TOL and R[str(L)]["paired_vs_base"]["both_exclude_zero"]]
        past = [L for L in LENGTHS if R[str(L)]["auroc"] <= BELIEVED[name]]
        other = [L for L in LENGTHS if abs(R[str(L)]["paired_vs_base"]["delta"]) > TOL and not (R[str(L)]["paired_vs_base"]["delta"] < -TOL and R[str(L)]["paired_vs_base"]["both_exclude_zero"])]
        R["branches"] = {"flat": flat, "degrades_first_at": (deg[0] if deg else None), "degrades_at": deg,
                         "past_believed_at": past, "beyond_tolerance_without_both_intervals_or_rise": other}
        res["readers"][name] = R
        print(f"\n{name}: base {R['base']['auroc']:.4f}  " + "  ".join(f"L{L} {R[str(L)]['auroc']:.4f} (d {R[str(L)]['paired_vs_base']['delta']:+.4f} "
              f"item [{R[str(L)]['paired_vs_base']['ci_item']['ci_lo']:+.4f},{R[str(L)]['paired_vs_base']['ci_item']['ci_hi']:+.4f}] "
              f"persona [{R[str(L)]['paired_vs_base']['ci_persona']['ci_lo']:+.4f},{R[str(L)]['paired_vs_base']['ci_persona']['ci_hi']:+.4f}])" for L in LENGTHS))
        for st in STATES:
            print(f"   {st:10s} base {R['base'][f'auroc_{st}']:.4f}  " + "  ".join(f"L{L} {R[str(L)][f'auroc_{st}']:.4f} (d {R[str(L)][f'paired_vs_base_{st}']['delta']:+.4f}, weaker "
                  f"[{R[str(L)][f'paired_vs_base_{st}']['weaker']['ci_lo']:+.4f},{R[str(L)][f'paired_vs_base_{st}']['weaker']['ci_hi']:+.4f}])" for L in LENGTHS))
        print(f"   branches: {R['branches']}")
    jdump(res, RES / "pad_scores.json")
    print(f"\nwrote {RES / 'pad_scores.json'}")


if __name__ == "__main__":
    {"build": cmd_build, "probe": cmd_probe, "run": cmd_run, "score": cmd_score}[sys.argv[1]]()
