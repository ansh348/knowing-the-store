# -*- coding: utf-8 -*-
"""run_view.py -- R85 Amendment 1 Step 6, the tag-route lanes on the 323 (D-R85-17). Program R114 (2026-09-17).

MODEL CALLS (billed, OpenAI metered key, gpt-4.1-mini, one call per (item, lane)): VIEW-UNTAGGED, VIEW-TAGGED, HYBRID (Graphiti; the
BELIEVED-capped summary in HYBRID) and FR-Bank VIEW-UNTAGGED (D-R85-14): 4 x 323, plus one probe per lane. Prompts: the untagged variant
of AUX-R85-G10-PROMPTS for the two untagged lanes, prompts_resp.SYSTEM_RETRIEVED / USER_RETRIEVED for VIEW-TAGGED, SYSTEM_RETRIEVED /
USER_HYBRID for HYBRID. Decoding: prompts_e1's (temperature 0, seed 42, max_tokens 200, JSON mode, the E1 clamp, one retry).
Cache g10/cache_mini/ (shared with run_summary.py; keys differ by arm); rows g10/rows_view.jsonl. P4 reads; HYBRID and the FR-Bank
lane descriptive; the tagged lane paired against the untagged and against the recorded FR-Bank rows on the 323.

Subcommands:  probe | project | run | score
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import datetime as dt
import io
import json
import sys
import threading
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
R85 = HERE.parent
ROOT = R85.parent
sys.path.insert(0, str(ROOT / "reviews" / "r114" / "tools"))
from r114_common import assert_spec, J, jdump, r4  # noqa: E402
import resp_common as RC                                                     # noqa: E402
import run_resp as RR                                                        # noqa: E402
import prompts_resp as PR                                                    # noqa: E402
import prompts_e1 as P                                                       # noqa: E402
from common_e1r import auroc                                                 # noqa: E402
import run_summary as RS                                                     # noqa: E402  (population, indexes, redirect, billed helpers)

api = RC.e1_api()
LANE, PRICE = "gpt-4.1-mini", (0.40, 1.60)
LINE = 2.00
ROWS_P = HERE / "rows_view.jsonl"
PROBES_P = HERE / "probes_view.json"
LEDGER = R85 / "NUMBERS_R85.md"
VIEWS = HERE / "views_g10.json"
ARMS = ("G10-VIEW-UNTAGGED", "G10-VIEW-TAGGED", "G10-HYBRID", "FRB-VIEW-UNTAGGED")
TOL = 0.05


def assert_lineage():
    assert_spec(); RR.assert_lineage()
    assert "AUX-R85-G10-CHECK" in LEDGER.read_text(encoding="utf-8") and "No rendering fault found; Step 6 proceeds" in LEDGER.read_text(encoding="utf-8"), "the checkpoint is not recorded -- STOP"
    assert "D-R85-20" in (R85 / "DEVIATIONS_R85.md").read_text(encoding="utf-8")


def load_views():
    V = J(VIEWS); pr = V["prompts"]
    s_u, u_u = pr["texts"]["SYSTEM_RETRIEVED_UNTAGGED"], pr["texts"]["USER_RETRIEVED_UNTAGGED"]
    assert RS.sha(s_u) == pr["SYSTEM_RETRIEVED_UNTAGGED"] and RS.sha(u_u) == pr["USER_RETRIEVED_UNTAGGED"]
    return V["items"], s_u, u_u


def messages(arm, it, v, texts, ix):
    s_u, u_u = texts; q = it["question"]
    if arm == "G10-VIEW-UNTAGGED":
        return [{"role": "system", "content": s_u}, {"role": "user", "content": u_u.format(retrieved=v["graphiti_untagged"], question=q)}]
    if arm == "G10-VIEW-TAGGED":
        return [{"role": "system", "content": PR.SYSTEM_RETRIEVED}, {"role": "user", "content": PR.USER_RETRIEVED.format(retrieved=v["graphiti_tagged"], question=q)}]
    if arm == "G10-HYBRID":
        return [{"role": "system", "content": PR.SYSTEM_RETRIEVED}, {"role": "user", "content": PR.USER_HYBRID.format(index=ix[it["persona"]]["believed_capped"]["text"], retrieved=v["graphiti_tagged"], question=q)}]
    if arm == "FRB-VIEW-UNTAGGED":
        return [{"role": "system", "content": s_u}, {"role": "user", "content": u_u.format(retrieved=v["frbank_untagged"], question=q)}]
    raise ValueError(arm)


def cmd_probe():
    assert_lineage(); e0 = RS.redirect(); full = RS.population(); ix = RS.indexes(); views, s_u, u_u = load_views()
    it = next(i for i in full if i["y_nok"]); out = {}
    for arm in ARMS:
        msgs = messages(arm, it, views[it["item_id"]], (s_u, u_u), ix)
        r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS, messages=msgs, response_format={"type": "json_object"})   # noqa: SLF001
        o = api.parse_json(r.choices[0].message.content) or {}
        out[arm] = {"item_id": it["item_id"], "served": r.model, "identifier_ok": LANE in r.model, "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens,
                    "usd": r.usage.prompt_tokens / 1e6 * PRICE[0] + r.usage.completion_tokens / 1e6 * PRICE[1], "user_chars": len(msgs[1]["content"]),
                    "status": "OK" if (RR.clamp(o.get("nok")) is not None and RR.clamp(o.get("fok")) is not None) else "PARSE_FAIL", "sample": (r.choices[0].message.content or "")[:200], "when": dt.datetime.now().isoformat(timespec="seconds")}
        print(json.dumps({k: v for k, v in out[arm].items() if k != "sample"}))
        if not out[arm]["identifier_ok"]:
            sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
        if out[arm]["status"] != "OK":
            sys.exit("PROBE PARSE FAILURE -- do not launch")
    jdump(out, PROBES_P)


def billed():
    usd = sum(json.loads(l).get("usd", 0.0) for l in io.open(ROWS_P, encoding="utf-8")) if ROWS_P.exists() else 0.0
    usd += sum(v["usd"] for v in J(PROBES_P).values()) if PROBES_P.exists() else 0.0
    return usd


def cmd_project():
    pr = J(PROBES_P); full = RS.population(); ix = RS.indexes(); views, s_u, u_u = load_views()
    tot, out = 0.0, {}
    for arm in ARMS:
        x = pr[arm]; ratio = x["tok_in"] / max(1, x["user_chars"])
        tin = sum(int(len(messages(arm, it, views[it["item_id"]], (s_u, u_u), ix)[1]["content"]) * ratio) for it in full); tout = x["tok_out"] * len(full)
        usd = tin / 1e6 * PRICE[0] + tout / 1e6 * PRICE[1]; tot += usd
        out[arm] = {"calls": len(full), "tin": tin, "tout": tout, "usd": round(usd, 4)}
    out["sum"] = round(tot, 4); out["sum_x1_3"] = round(1.3 * tot, 4); out["billed_before"] = round(billed(), 4); out["line"] = LINE
    out["runs"] = out["sum_x1_3"] + out["billed_before"] < LINE; out["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(out, HERE / "projection_view.json"); print(json.dumps(out, indent=1))
    if not out["runs"]:
        sys.exit("PROJECTION OVER THE LINE -- STOP")


def cmd_run():
    assert_lineage(); RS.redirect(); full = RS.population(); ix = RS.indexes(); views, s_u, u_u = load_views()
    assert J(HERE / "projection_view.json")["runs"]
    done = {(json.loads(l)["item_id"], json.loads(l)["arm"]) for l in io.open(ROWS_P, encoding="utf-8")} if ROWS_P.exists() else set()
    jobs = [(it, arm) for arm in ARMS for it in full if (it["item_id"], arm) not in done]
    print(f"{len(jobs)} calls to go (resumed past {len(done)})", flush=True)
    lock, spend, stopped, n_done = threading.Lock(), [billed()], [False], [0]

    def work(job):
        it, arm = job
        with lock:
            if spend[0] >= LINE or stopped[0]:
                stopped[0] = True; return None
        v = views[it["item_id"]]; msgs = messages(arm, it, v, (s_u, u_u), ix)
        ok = lambda o: o is not None and RR.clamp(o.get("fok")) is not None and RR.clamp(o.get("nok")) is not None     # noqa: E731
        r = api.call(it["item_id"], arm, msgs); o = api.parse_json(r["content"]); n_calls, failed = 1, False
        usd = 0.0 if r["cached"] else r["prompt_tokens"] / 1e6 * PRICE[0] + r["completion_tokens"] / 1e6 * PRICE[1]
        if not ok(o):
            r2 = api.call(it["item_id"], arm + "#retry", msgs); o = api.parse_json(r2["content"]); n_calls = 2
            usd += 0.0 if r2["cached"] else r2["prompt_tokens"] / 1e6 * PRICE[0] + r2["completion_tokens"] / 1e6 * PRICE[1]
            r = r2
            if not ok(o):
                failed, o = True, {}
        view_text = {"G10-VIEW-UNTAGGED": v["graphiti_untagged"], "G10-VIEW-TAGGED": v["graphiti_tagged"], "G10-HYBRID": v["graphiti_tagged"], "FRB-VIEW-UNTAGGED": v["frbank_untagged"]}[arm]
        rec = {**{k: it[k] for k in ("item_id", "persona", "question", "label", "state", "y_nok", "y_fok", "tier", "variant")}, "arm": arm, "draw": 1,
               "view_sha256": RS.sha(view_text), "view_lines": (view_text.count("\n") + 1) if view_text else 0, "system_sha256": RS.sha(msgs[0]["content"]), "user_sha256": RS.sha(msgs[1]["content"]),
               "fok": RR.clamp(o.get("fok")), "nok": RR.clamp(o.get("nok")), "nok_candidates_found": (bool(o.get("nok_candidates_found")) if not failed else None), "would_search": (bool(o.get("would_search")) if not failed else None),
               "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls, "cached": r["cached"], "served_model": r.get("model"), "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "usd": usd,
               "text": (r["content"] or "")[:300], "when": dt.datetime.now().isoformat(timespec="seconds")}
        with lock:
            spend[0] += usd; n_done[0] += 1
            with io.open(ROWS_P, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, sort_keys=True) + "\n")
            if n_done[0] % 200 == 0:
                print(f"  {n_done[0]} done, billed ${spend[0]:.4f}", flush=True); api.flush()
        return rec
    try:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            out = [r for r in ex.map(work, jobs) if r is not None]
    finally:
        api.flush()
    c = collections.Counter((r["arm"], r["status"]) for r in out)
    print(f"DONE {len(out)} rows; status {dict(c)}; billed total ${spend[0]:.4f} against ${LINE:.2f}" + ("  >>> STOPPED" if stopped[0] else ""))
    if stopped[0]:
        sys.exit(1)


def fmt(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"


def cmd_score():
    assert_lineage(); sys.stdout.reconfigure(encoding="utf-8")
    full = RS.population(); ids = [it["item_id"] for it in full]
    y = np.array([it["y_nok"] for it in full], int); g = np.array([it["persona"] for it in full]); yf = np.array([it["y_fok"] for it in full], int)
    blind = np.array([it["blind"]["nok"] for it in full], float); true_ = np.array([it["true"]["nok"] for it in full], float)
    by = {a: {} for a in ARMS}
    for l in io.open(ROWS_P, encoding="utf-8"):
        r = json.loads(l); by[r["arm"]][r["item_id"]] = r
    # the recorded FR-Bank rows on the 323 (RETRIEVED, HYBRID: run_resp rows; RETRIEVED-BELIEVED: amend1 rows), the R113 Z3 gates
    rr = RR.load_rows(); ret_rec = np.array([rr["RETRIEVED"][i]["nok"] for i in ids], float); hyb_rec = np.array([rr["HYBRID"][i]["nok"] for i in ids], float)
    bel = {}
    for l in io.open(ROOT / "resp_review" / "run" / "rows_amend1_mini.jsonl", encoding="utf-8"):
        r = json.loads(l)
        if r.get("arm") == "RETRIEVED-BELIEVED" and r.get("status") == "OK":
            bel[r["item_id"]] = r["nok"]
    bel_rec = np.array([bel[i] for i in ids], float)
    gates = {"retrieved_323": round(float(auroc(ret_rec, y)), 4), "hybrid_323": round(float(auroc(hyb_rec, y)), 4), "believed_323": round(float(auroc(bel_rec, y)), 4), "true_323": round(float(auroc(true_, y)), 4), "blind_323": round(float(auroc(blind, y)), 4)}
    assert gates == {"retrieved_323": 0.6980, "hybrid_323": 0.8855, "believed_323": 0.8504, "true_323": 0.7424, "blind_323": 0.4964}, gates
    summ = J(HERE / "results" / "summary_g10.json"); g10b = {}
    for l in io.open(HERE / "rows_summary.jsonl", encoding="utf-8"):
        r = json.loads(l)
        if r["arm"] == "G10-BELIEVED":
            g10b[r["item_id"]] = r["nok"]
    g10b = np.array([g10b[i] for i in ids], float)
    res = {"population": {"n": 323, "positives": 47, "rule": "D-R85-17"}, "gates": gates, "arms": {}, "readings": {}, "spend": {}}
    S = {}
    for arm in ARMS:
        rows = by[arm]; fails = sum(1 for i in ids if rows.get(i, {}).get("status") != "OK"); assert fails == 0, (arm, fails)
        s = np.array([rows[i]["nok"] for i in ids], float); S[arm] = s
        A = {"nok": RR.auroc_ci(s, y), "fok_323": r4(auroc(np.array([rows[i]["fok"] for i in ids], float), yf)), "vs_blind": RR.paired(blind, s, y, g), "vs_true": RR.paired(true_, s, y, g),
             "usd": round(sum(rows[i]["usd"] for i in ids), 4), "served": sorted({rows[i]["served_model"] for i in ids}), "cached": sum(1 for i in ids if rows[i]["cached"]), "per_state": {}, "empty_views": sum(1 for i in ids if rows[i]["view_lines"] == 0)}
        for st, name in RR.STATES:
            sub_ = [k for k, it in enumerate(full) if it["y_nok"] == 0 or it["state"] == st]
            A["per_state"][st] = {"n": len(sub_), "pos": int(y[sub_].sum()), "auroc": r4(auroc(s[sub_], y[sub_]))}
        res["arms"][arm] = A
    # P4: tagged against untagged on Graphiti
    p4 = RR.paired(S["G10-VIEW-UNTAGGED"], S["G10-VIEW-TAGGED"], y, g)
    res["readings"]["P4"] = {"U": r4(p4["base"]), "T": r4(p4["arm"]), "D": r4(p4["D"]), "item": p4["item"], "persona": p4["cluster"], "verdict": "HOLDS" if abs(p4["D"]) <= TOL else "FAILS",
                             "criterion": "|VIEW-TAGGED - VIEW-UNTAGGED| within 0.05 on the 323 (the L2-P2 convention on the point estimate; the intervals print beside)"}
    hy = RR.paired(S["G10-VIEW-TAGGED"], S["G10-HYBRID"], y, g); hs = RR.paired(g10b, S["G10-HYBRID"], y, g)
    res["readings"]["HYBRID"] = {"vs_tagged": hy, "vs_believed_summary_alone": hs, "believed_summary_alone": r4(auroc(g10b, y))}
    fu = S["FRB-VIEW-UNTAGGED"]
    res["readings"]["FRB-UNTAGGED"] = {"untagged": r4(auroc(fu, y)), "vs_retrieved_join_tags": RR.paired(fu, ret_rec, y, g), "vs_retrieved_believed_own_marks": RR.paired(fu, bel_rec, y, g),
                                       "retrieved_323": gates["retrieved_323"], "believed_323": gates["believed_323"]}
    res["readings"]["cross_store"] = {"graphiti_tagged_vs_frbank_believed": RR.paired(S["G10-VIEW-TAGGED"], bel_rec, y, g), "graphiti_untagged_vs_frbank_untagged": RR.paired(S["G10-VIEW-UNTAGGED"], fu, y, g)}
    res["spend"] = {"probes": round(sum(v["usd"] for v in J(PROBES_P).values()), 4), "lanes": {a: res["arms"][a]["usd"] for a in ARMS}}
    res["spend"]["total"] = round(res["spend"]["probes"] + sum(res["spend"]["lanes"].values()), 4); res["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(res, HERE / "results" / "view_g10.json")
    P4, H, F, X = res["readings"]["P4"], res["readings"]["HYBRID"], res["readings"]["FRB-UNTAGGED"], res["readings"]["cross_store"]
    L = [f"\n### AUX-R85-G10-VIEW — Step 6, the tag-route lanes on the 323 (2026-09-17, program R114, D-R85-17; `g10/run_view.py`; `g10/rows_view.jsonl`; `g10/results/view_g10.json`; billed)\n\n",
         f"GPT-4.1 mini, one call per (item, lane), the RESP L2 protocol; the recorded FR-Bank rows re-scored on the 323 (gates: RETRIEVED {gates['retrieved_323']}, RETRIEVED-BELIEVED {gates['believed_323']}, HYBRID {gates['hybrid_323']}, INDEXED-TRUE {gates['true_323']}, BLIND {gates['blind_323']}, equal to AUX-R113-Z3-ROWS). Item-level and persona-clustered paired bootstraps, 1,000 draws, seed 42.\n\n",
         "| lane | view | prompt | NOK AUROC (item 95%) | minus BLIND (item; persona) | minus INDEXED-TRUE (item; persona) | supersession (27) | expiry (9) | retraction (11) | FOK (323) | empty views | $ |\n|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|\n"]
    desc = {"G10-VIEW-UNTAGGED": ("Graphiti ranks 1-5, no lifecycle field", "untagged variant"), "G10-VIEW-TAGGED": ("Graphiti ranks 1-5, RULE 1 states", "SYSTEM_RETRIEVED / USER_RETRIEVED"),
            "G10-HYBRID": ("Graphiti ranks 1-5 tagged + BELIEVED-capped summary", "SYSTEM_RETRIEVED / USER_HYBRID"), "FRB-VIEW-UNTAGGED": ("FR-Bank recorded top-5, no lifecycle field", "untagged variant")}
    for arm in ARMS:
        A = res["arms"][arm]
        L.append(f"| {arm} | {desc[arm][0]} | {desc[arm][1]} | **{A['nok']['point']:.4f}** [{A['nok']['ci_lo']:.4f}, {A['nok']['ci_hi']:.4f}] | {A['vs_blind']['D']:+.4f} ({fmt(A['vs_blind']['item'])}; {fmt(A['vs_blind']['cluster'])}) | {A['vs_true']['D']:+.4f} ({fmt(A['vs_true']['item'])}; {fmt(A['vs_true']['cluster'])}) | {A['per_state']['sup']['auroc']:.4f} | {A['per_state']['exp']['auroc']:.4f} | {A['per_state']['ret']['auroc']:.4f} | {A['fok_323']:.4f} | {A['empty_views']} | {A['usd']:.4f} |\n")
    L.append(f"\n### AUX-R85-G10-P4 — **{P4['verdict']}**. Shown the five retrieved edges with Graphiti's own states, GPT-4.1 mini reads {P4['T']:.4f} against {P4['U']:.4f} without them, {P4['D']:+.4f} apart with interval {fmt(P4['item'])} (persona {fmt(P4['persona'])}); {'within tolerance: the states this store writes do not reach the records that forbid use' if P4['verdict'] == 'HOLDS' else 'beyond the registered tolerance'}.\n")
    L.append(f"\n### AUX-R85-G10-HYBRID (descriptive, no bar) — HYBRID {res['arms']['G10-HYBRID']['nok']['point']:.4f} against VIEW-TAGGED {P4['T']:.4f}: {H['vs_tagged']['D']:+.4f} ({fmt(H['vs_tagged']['item'])}; {fmt(H['vs_tagged']['cluster'])}); against the BELIEVED-capped summary alone {H['believed_summary_alone']:.4f}: {H['vs_believed_summary_alone']['D']:+.4f} ({fmt(H['vs_believed_summary_alone']['item'])}; {fmt(H['vs_believed_summary_alone']['cluster'])}).\n")
    L.append(f"\n### AUX-R85-G10-FRB-UNTAGGED (D-R85-14, descriptive, no bar) — FR-Bank's recorded top-5 with the lifecycle field removed: {F['untagged']:.4f}; the recorded RETRIEVED row (the join's tags) {F['retrieved_323']:.4f} is {F['vs_retrieved_join_tags']['D']:+.4f} above it ({fmt(F['vs_retrieved_join_tags']['item'])}; {fmt(F['vs_retrieved_join_tags']['cluster'])}); the recorded RETRIEVED-BELIEVED row (FR-Bank's own marks) {F['believed_323']:.4f} is {F['vs_retrieved_believed_own_marks']['D']:+.4f} above it ({fmt(F['vs_retrieved_believed_own_marks']['item'])}; {fmt(F['vs_retrieved_believed_own_marks']['cluster'])}). Cross-store, the same footing: Graphiti VIEW-TAGGED against FR-Bank RETRIEVED-BELIEVED {X['graphiti_tagged_vs_frbank_believed']['D']:+.4f} ({fmt(X['graphiti_tagged_vs_frbank_believed']['item'])}; {fmt(X['graphiti_tagged_vs_frbank_believed']['cluster'])}); Graphiti VIEW-UNTAGGED against FR-Bank VIEW-UNTAGGED {X['graphiti_untagged_vs_frbank_untagged']['D']:+.4f} ({fmt(X['graphiti_untagged_vs_frbank_untagged']['item'])}; {fmt(X['graphiti_untagged_vs_frbank_untagged']['cluster'])}).\n")
    L.append(f"\n### AUX-R85-G10-VIEW-SPEND — probes ${res['spend']['probes']:.4f}, lanes " + ", ".join(f"{a} ${v:.4f}" for a, v in res["spend"]["lanes"].items()) + f"; **Step 6 total ${res['spend']['total']:.4f}**; query embeddings (Step 5) ${J(HERE / 'retrieval_raw_g10.json')['meta']['usd']:.5f}.\n")
    txt = "".join(L)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    {"probe": cmd_probe, "project": cmd_project, "run": cmd_run, "score": cmd_score}[sys.argv[1]]()
