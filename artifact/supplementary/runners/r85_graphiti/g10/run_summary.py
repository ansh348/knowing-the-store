# -*- coding: utf-8 -*-
"""run_summary.py -- R85 Amendment 1 Step 4 on the 323 FULL-variant items (D-R85-17): the leakage screen, the summary-route lanes, the
readers, and the readings P2, P3, GR-1 to GR-5. Program R114 (2026-09-17).

MODEL CALLS (billed, OpenAI metered key, gpt-4.1-mini): the 30-item leakage screen (prompts_e1.LEAKAGE_*), one probe, and one call per
(item, index) for the four indexes of build_indexes.py (BELIEVED-capped, BELIEVED-lifted, TRUE-projected, TRUE-projected-lifted):
4 x 323. The main-study protocol: prompts_e1.SYSTEM / USER_INDEXED, temperature 0, seed 42, max_tokens 200, JSON mode, the E1 clamp,
one retry on a parse failure (run_resp.elicit's mechanics). The blind and INDEXED-TRUE rows are read from the record, never re-run.
Readers NB-5 / NB-6 (local encoder, $0). Cache r85_graphiti/g10/cache_mini/; rows g10/rows_summary.jsonl; leak g10/leak30_g10.json.

Subcommands, in order:  leak30 | probe | project | run | score
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import datetime as dt
import hashlib
import io
import json
import random
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
import prompts_e1 as P                                                       # noqa: E402
from common_e1r import auroc                                                 # noqa: E402
from run_nb6 import emb_scores, lex_scores                                   # noqa: E402
sys.path.insert(0, str(ROOT / "analysis" / "ontology_validation"))
from exp4_witnesses import supports_correct                                  # noqa: E402

api = RC.e1_api()
LANE, PRICE = "gpt-4.1-mini", (0.40, 1.60)
LINE = 2.00                     # this step's line (manifest: expected 0.70, conservative 0.95)
CACHE = HERE / "cache_mini"
ROWS_P = HERE / "rows_summary.jsonl"
PROBES_P = HERE / "probes_summary.json"
LEAK_P = HERE / "leak30_g10.json"
RES = HERE / "results"
LEDGER = R85 / "NUMBERS_R85.md"
IDX = HERE / "indexes_g10.json"
ARMS = {"G10-BELIEVED": "believed_capped", "G10-LIFTED": "believed_lifted", "G10-TRUEPROJ": "true_projected", "G10-TRUEPROJ-LIFTED": "true_projected_lifted"}
TOL = 0.05
LEAK_N, LEAK_K, SEED = 30, 3, 42
TRUE_GAIN_661 = 0.2393          # GR-4's registered denominator (the 661: 0.7339 - 0.4946)


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def assert_lineage():
    assert_spec(); RR.assert_lineage()
    assert "D-R85-17" in (R85 / "DEVIATIONS_R85.md").read_text(encoding="utf-8"), "D-R85-17 not recorded -- STOP"
    assert "AUX-R85-G10-INDEXES" in LEDGER.read_text(encoding="utf-8"), "the indexes are not ledgered -- STOP"


def redirect():
    CACHE.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                             # noqa: SLF001
    e0.CACHE_PATH = CACHE / "responses.json"; e0.LEDGER_PATH = CACHE / "cost_ledger.json"
    e0._cache = None; e0._load_cache()                                       # noqa: SLF001
    e0.HARD_CAP_USD = LINE
    return e0


def population():
    sub = RC.load_cell()
    full = [it for it in sub if it["variant"] == "FULL"]
    assert (len(full), sum(i["y_nok"] for i in full), sum(1 for i in full if i["label"] == "PRESENT")) == (323, 47, 131)
    return full


def indexes():
    return J(IDX)["personas"]


def messages(it, text):
    return [{"role": "system", "content": P.SYSTEM}, {"role": "user", "content": P.USER_INDEXED.format(index=text, question=it["question"])}]


# ------------------------------------------------------------------ leakage screen
def cmd_leak30():
    assert_lineage(); e0 = redirect()
    full = population(); ix = indexes()
    present = sorted([it for it in full if it["label"] == "PRESENT"], key=lambda i: i["item_id"]); assert len(present) == 131
    sample = sorted(random.Random(SEED).sample(present, LEAK_N), key=lambda i: i["item_id"])
    qs = {q["id"]: q for q in json.loads((ROOT / "LifeMemEval" / "lifemembench_questions.json").read_text("utf-8"))}
    rows, n_correct, usd = [], 0, 0.0
    for it in sample:
        q = qs[it["question_id"]]; assert q["question"] == it["question"]
        text = ix[it["persona"]]["believed_capped"]["text"]
        msgs = [{"role": "system", "content": P.LEAKAGE_SYSTEM}, {"role": "user", "content": P.LEAKAGE_USER.format(index=text, question=q["question"])}]
        r = api.call(it["item_id"], "G10-LEAK30", msgs); o = api.parse_json(r["content"]) or {}
        ans = o.get("answer", "") if isinstance(o, dict) else ""
        ans = ans if isinstance(ans, str) else json.dumps(ans)
        ok = bool(ans) and ans.strip().upper() != "UNKNOWN" and supports_correct(ans, q["correct_answer"])
        n_correct += int(ok)
        usd += 0.0 if r["cached"] else r["prompt_tokens"] / 1e6 * PRICE[0] + r["completion_tokens"] / 1e6 * PRICE[1]
        rows.append({"item_id": it["item_id"], "persona": it["persona"], "question": q["question"], "answer": ans, "correct": ok, "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "served": r.get("model"), "raw": (r["content"] or "")[:300]})
        print(f"  {'LEAK' if ok else 'ok  '} {it['item_id']:40s} {ans[:70]}")
    api.flush()
    out = {"model": LANE, "index": "BELIEVED-capped (g10/indexes_g10.json)", "n": len(sample), "n_correct": n_correct, "frozen_threshold": f">{LEAK_K}/{LEAK_N}", "seed": SEED, "draw": "random.Random(42).sample over the 131 PRESENT FULL items sorted by item_id, as e0's run_leakage_control",
           "leaked": n_correct > LEAK_K, "usd": round(usd, 4), "rows": rows, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, LEAK_P)
    txt = (f"\n### AUX-R85-G10-LEAK30 — Step 4, the leakage screen at forty personas (2026-09-17; `g10/run_summary.py leak30`; `g10/leak30_g10.json`; billed)\n\n"
           f"30 PRESENT FULL-variant items drawn by the frozen rule (seed 42 over the 131, as `run_leakage_control.py`), GPT-4.1 mini asked to answer from the BELIEVED-capped index alone (`prompts_e1.LEAKAGE_*`, `supports_correct`, UNKNOWN never correct): "
           f"**{n_correct} of 30** answered correctly against the frozen threshold of more than 3 of 30 — {'**LEAK: the summary lanes stop**' if out['leaked'] else 'no leak; the summary lanes proceed'}. ${usd:.4f}.\n")
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)
    if out["leaked"]:
        sys.exit("LEAK -- STOP")


# ------------------------------------------------------------------ probe / project
def cmd_probe():
    assert_lineage(); e0 = redirect(); full = population(); ix = indexes()
    it = next(i for i in full if i["y_nok"])
    out = {}
    for arm, key in ARMS.items():
        text = ix[it["persona"]][key]["text"]
        r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,   # noqa: SLF001
                                                 messages=messages(it, text), response_format={"type": "json_object"})
        o = api.parse_json(r.choices[0].message.content) or {}
        out[arm] = {"item_id": it["item_id"], "served": r.model, "identifier_ok": LANE in r.model, "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens,
                    "usd": r.usage.prompt_tokens / 1e6 * PRICE[0] + r.usage.completion_tokens / 1e6 * PRICE[1], "index_chars": len(text),
                    "status": "OK" if (RR.clamp(o.get("nok")) is not None and RR.clamp(o.get("fok")) is not None) else "PARSE_FAIL", "sample": (r.choices[0].message.content or "")[:200],
                    "when": dt.datetime.now().isoformat(timespec="seconds")}
        print(json.dumps({k: v for k, v in out[arm].items() if k != "sample"}))
        if not out[arm]["identifier_ok"]:
            sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
        if out[arm]["status"] != "OK":
            sys.exit("PROBE PARSE FAILURE -- do not launch")
    jdump(out, PROBES_P)


def billed():
    usd = sum(json.loads(l).get("usd", 0.0) for l in io.open(ROWS_P, encoding="utf-8")) if ROWS_P.exists() else 0.0
    usd += sum(v["usd"] for v in J(PROBES_P).values()) if PROBES_P.exists() else 0.0
    usd += J(LEAK_P)["usd"] if LEAK_P.exists() else 0.0
    return usd


def cmd_project():
    pr = J(PROBES_P); full = population(); ix = indexes()
    tot = 0.0; out = {}
    for arm, key in ARMS.items():
        x = pr[arm]; ratio = x["tok_in"] / max(1, x["index_chars"])
        tin = sum(int(len(ix[it["persona"]][key]["text"]) * ratio) for it in full); tout = x["tok_out"] * len(full)
        usd = tin / 1e6 * PRICE[0] + tout / 1e6 * PRICE[1]; tot += usd
        out[arm] = {"calls": len(full), "tin": tin, "tout": tout, "usd": round(usd, 4)}
    out["sum"] = round(tot, 4); out["sum_x1_3"] = round(1.3 * tot, 4); out["billed_before"] = round(billed(), 4); out["line"] = LINE
    out["runs"] = out["sum_x1_3"] + out["billed_before"] < LINE; out["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(out, HERE / "projection_summary.json"); print(json.dumps(out, indent=1))
    if not out["runs"]:
        sys.exit("PROJECTION OVER THE LINE -- STOP")


# ------------------------------------------------------------------ run
def rowkey(r):
    return (r["item_id"], r["arm"])


def cmd_run():
    assert_lineage(); redirect(); full = population(); ix = indexes()
    assert J(HERE / "projection_summary.json")["runs"]
    done = {rowkey(json.loads(l)) for l in io.open(ROWS_P, encoding="utf-8")} if ROWS_P.exists() else set()
    jobs = [(it, arm) for arm in ARMS for it in full if (it["item_id"], arm) not in done]
    print(f"{len(jobs)} calls to go (resumed past {len(done)})", flush=True)
    lock, spend, stopped, n_done = threading.Lock(), [billed()], [False], [0]

    def work(job):
        it, arm = job
        with lock:
            if spend[0] >= LINE or stopped[0]:
                stopped[0] = True; return None
        text = ix[it["persona"]][ARMS[arm]]["text"]; msgs = messages(it, text)
        ok = lambda o: o is not None and RR.clamp(o.get("fok")) is not None and RR.clamp(o.get("nok")) is not None     # noqa: E731
        r = api.call(it["item_id"], arm, msgs); o = api.parse_json(r["content"]); n_calls, failed = 1, False
        usd = 0.0 if r["cached"] else r["prompt_tokens"] / 1e6 * PRICE[0] + r["completion_tokens"] / 1e6 * PRICE[1]
        if not ok(o):
            r2 = api.call(it["item_id"], arm + "#retry", msgs); o = api.parse_json(r2["content"]); n_calls = 2
            usd += 0.0 if r2["cached"] else r2["prompt_tokens"] / 1e6 * PRICE[0] + r2["completion_tokens"] / 1e6 * PRICE[1]
            r = r2
            if not ok(o):
                failed, o = True, {}
        rec = {**{k: it[k] for k in ("item_id", "persona", "question", "label", "state", "y_nok", "y_fok", "tier", "variant", "index_key")}, "arm": arm, "draw": 1,
               "index_sha256": ix[it["persona"]][ARMS[arm]]["sha256"], "fok": RR.clamp(o.get("fok")), "nok": RR.clamp(o.get("nok")),
               "nok_candidates_found": (bool(o.get("nok_candidates_found")) if not failed else None), "would_search": (bool(o.get("would_search")) if not failed else None),
               "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls, "cached": r["cached"], "served_model": r.get("model"),
               "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "usd": usd, "text": (r["content"] or "")[:300], "when": dt.datetime.now().isoformat(timespec="seconds")}
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


# ------------------------------------------------------------------ score
def load_rows():
    by = {a: {} for a in ARMS}
    for l in io.open(ROWS_P, encoding="utf-8"):
        r = json.loads(l); by[r["arm"]][r["item_id"]] = r
    return by


def fmt(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"


def cmd_score():
    assert_lineage(); sys.stdout.reconfigure(encoding="utf-8")
    full = population(); ix = indexes(); by = load_rows()
    ids = [it["item_id"] for it in full]; y = np.array([it["y_nok"] for it in full], int); g = np.array([it["persona"] for it in full])
    yf = np.array([it["y_fok"] for it in full], int)
    blind = np.array([it["blind"]["nok"] for it in full], float); true_ = np.array([it["true"]["nok"] for it in full], float)
    blind_f = np.array([it["blind"]["fok"] for it in full], float); true_f = np.array([it["true"]["fok"] for it in full], float)
    # reproduction gates on the recorded rows (AUX-R113-Z3-ROWS)
    a_true, a_blind = round(float(auroc(true_, y)), 4), round(float(auroc(blind, y)), 4)
    assert (a_true, a_blind) == (0.7424, 0.4964), (a_true, a_blind)
    res = {"population": {"n": 323, "positives": 47, "rule": "D-R85-17"}, "gates": {"true_323": a_true, "blind_323": a_blind}, "arms": {}, "readers": {}, "readings": {}, "spend": {}}
    for arm in ARMS:
        rows = by[arm]; fails = sum(1 for i in ids if rows.get(i, {}).get("status") != "OK")
        assert fails == 0, (arm, fails)
        s = np.array([rows[i]["nok"] for i in ids], float); sf = np.array([rows[i]["fok"] for i in ids], float)
        A = {"nok": RR.auroc_ci(s, y), "fok_323": RR.auroc_ci(sf, yf), "n_fail": fails, "cached": sum(1 for i in ids if rows[i]["cached"]),
             "usd": round(sum(rows[i]["usd"] for i in ids), 4), "tok_in": sum(rows[i]["tok_in"] or 0 for i in ids), "served": sorted({rows[i]["served_model"] for i in ids}),
             "vs_true": RR.paired(true_, s, y, g), "vs_blind": RR.paired(blind, s, y, g), "fok_vs_blind_323": RR.paired(blind_f, sf, yf, g),
             "per_state": {}}
        for st, name in RR.STATES:
            sub_ = [k for k, it in enumerate(full) if it["y_nok"] == 0 or it["state"] == st]
            A["per_state"][st] = {"n": len(sub_), "pos": int(y[sub_].sum()), "auroc": r4(auroc(s[sub_], y[sub_])), "true": r4(auroc(true_[sub_], y[sub_]))}
        res["arms"][arm] = A
    # readers: NB-6 (superseded section) and NB-5 (whole map), embedding and lexical, under each rendering
    for arm, key in ARMS.items():
        rows_r = [{"question": it["question"], "sup": ix[it["persona"]][key]["names_sup"], "all": ix[it["persona"]][key]["names_all"]} for it in full]
        R = {}
        for field, nb in (("sup", "NB-6"), ("all", "NB-5")):
            for var, fn in (("emb", emb_scores), ("lex", lex_scores)):
                sc = np.array(fn(rows_r, field), float)
                R[f"{nb}-{var}"] = {**RR.auroc_ci(sc, y), "vs_monitor": RR.paired(np.array([by[arm][i]["nok"] for i in ids], float), sc, y, g),
                                   "vs_true": RR.paired(true_, sc, y, g), "n_empty": sum(1 for r in rows_r if not r[field])}
        res["readers"][arm] = R
    # readings
    B = res["arms"]["G10-BELIEVED"]; nb6 = res["readers"]["G10-BELIEVED"]["NB-6-emb"]; nb6l = res["readers"]["G10-LIFTED"]["NB-6-emb"]
    D = B["vs_true"]["D"]; I_item, I_pers = B["vs_true"]["item"], B["vs_true"]["cluster"]
    p2_holds = D < -TOL and (I_item["ci_hi"] < 0)
    res["readings"]["P2"] = {"G": r4(B["nok"]["point"]), "T": a_true, "D": r4(D), "item": I_item, "persona": I_pers, "criterion": "Graphiti BELIEVED-capped below INDEXED-TRUE by more than 0.05 with the item-level paired interval excluding zero",
                             "verdict": "HOLDS" if p2_holds else "FAILS", "blind_beside": a_blind, "Y": r4(nb6["point"]),
                             "lifted": r4(res["arms"]["G10-LIFTED"]["nok"]["point"]), "true_projected": r4(res["arms"]["G10-TRUEPROJ"]["nok"]["point"]), "true_projected_lifted": r4(res["arms"]["G10-TRUEPROJ-LIFTED"]["nok"]["point"])}
    p3 = {"capped": r4(nb6["point"]), "lifted": r4(nb6l["point"]), "capped_ci": [r4(nb6["ci_lo"]), r4(nb6["ci_hi"])], "lifted_ci": [r4(nb6l["ci_lo"]), r4(nb6l["ci_hi"])]}
    p3["verdict"] = "HOLDS" if (abs(p3["capped"] - 0.5) <= TOL and abs(p3["lifted"] - 0.5) <= TOL) else "FAILS"
    p3["D_from_chance"] = {"capped": r4(p3["capped"] - 0.5), "lifted": r4(p3["lifted"] - 0.5)}
    res["readings"]["P3"] = p3
    gr1 = B["vs_blind"]; res["readings"]["GR-1"] = {"D": r4(gr1["D"]), "item": gr1["item"], "cluster": gr1["cluster"], "verdict": "HOLDS" if (gr1["item"]["ci_lo"] > 0 and gr1["cluster"]["ci_lo"] > 0) else ("FAILS" if not (gr1["item"]["ci_lo"] > 0) else "item interval excludes zero, persona interval does not")}
    res["readings"]["GR-2"] = {"registered": "the paired FOK gain on the hard tier (307 items, 35 positives)", "status": "dash: the FULL variant holds 145 hard-tier items with 0 positives (the hard tier's 35 positives are all ablated-variant rows), so the registered row is not computable on the 323",
                               "fok_323_descriptive": {"blind": r4(auroc(blind_f, yf)), "true": r4(auroc(true_f, yf)), "believed": r4(B["fok_323"]["point"]), "D_vs_blind": r4(B["fok_vs_blind_323"]["D"]), "item": B["fok_vs_blind_323"]["item"], "cluster": B["fok_vs_blind_323"]["cluster"], "n": 323, "positives": int(yf.sum())}}
    m = nb6["vs_monitor"]; res["readings"]["GR-3"] = {"Y": r4(nb6["point"]), "X": r4(B["nok"]["point"]), "D": r4(m["D"]), "item": m["item"], "cluster": m["cluster"],
                                                    "verdict": "HOLDS" if (abs(m["D"]) <= TOL or m["D"] > 0) else "FAILS in the monitor's favour"}
    true_gain_323 = round(a_true - a_blind, 4)
    res["readings"]["GR-4"] = {"believed_gain_323": r4(gr1["D"]), "true_gain_323": true_gain_323, "fraction_of_true_gain_323": r4(gr1["D"] / true_gain_323), "fraction_of_registered_0.2393": r4(gr1["D"] / TRUE_GAIN_661), "frbank_believed_retention_registered": "42.3%"}
    res["readings"]["GR-5"] = {"named_at_step_3": "extraction (AUX-R85-G10-CENSUS: EXTRACTION_MISS 77 of 109; erase with overstatement in what survives)", "unchanged": True}
    res["spend"] = {"leak30": J(LEAK_P)["usd"], "probes": round(sum(v["usd"] for v in J(PROBES_P).values()), 4), "lanes": {a: res["arms"][a]["usd"] for a in ARMS}}
    res["spend"]["total"] = round(res["spend"]["leak30"] + res["spend"]["probes"] + sum(res["spend"]["lanes"].values()), 4)
    res["when"] = dt.datetime.now().isoformat(timespec="seconds")
    RES.mkdir(exist_ok=True); jdump(res, RES / "summary_g10.json")
    # ---------------------------------------------------------------- ledger
    L = [f"\n### AUX-R85-G10-SUMMARY — Step 4, the summary route on the 323 (2026-09-17, program R114, D-R85-17; `g10/run_summary.py`; `g10/rows_summary.jsonl`; `g10/results/summary_g10.json`; billed)\n\n",
         f"GPT-4.1 mini, one call per (item, index), the main-study protocol, on the 323 FULL-variant items (positives 47); the blind and INDEXED-TRUE rows from the record (gates on the 323: INDEXED-TRUE {a_true}, BLIND {a_blind}, equal to AUX-R113-Z3-ROWS). Item-level and persona-clustered paired bootstraps, 1,000 draws, seed 42; the weaker governs. Per state: that state's positives against every FULL negative (276).\n\n",
         "| index | NOK AUROC (item 95%) | minus INDEXED-TRUE (item; persona) | minus BLIND (item; persona) | supersession (27) | expiry (9) | retraction (11) | FOK on the 323 (178 pos.) | failures | served | $ |\n|---|---|---|---|---:|---:|---:|---:|---:|---|---:|\n"]
    for arm in ARMS:
        A = res["arms"][arm]
        L.append(f"| {arm} | **{A['nok']['point']:.4f}** [{A['nok']['ci_lo']:.4f}, {A['nok']['ci_hi']:.4f}] | {A['vs_true']['D']:+.4f} ({fmt(A['vs_true']['item'])}; {fmt(A['vs_true']['cluster'])}) | {A['vs_blind']['D']:+.4f} ({fmt(A['vs_blind']['item'])}; {fmt(A['vs_blind']['cluster'])}) | {A['per_state']['sup']['auroc']:.4f} | {A['per_state']['exp']['auroc']:.4f} | {A['per_state']['ret']['auroc']:.4f} | {A['fok_323']['point']:.4f} | {A['n_fail']} | {', '.join(A['served'])} | {A['usd']:.4f} |\n")
    L.append("\n### AUX-R85-G10-NB — the readers on the same renderings ($0; `run_nb6.emb_scores` / `lex_scores` on the name lists of AUX-R85-G10-INDEXES, D-R85-19): NB-6 over the superseded-names section, NB-5 over the whole map\n\n| index | NB-6 emb (item 95%) | NB-6 lex | NB-5 emb | NB-5 lex | NB-6 emb minus the monitor (item; persona) | items with an empty superseded list |\n|---|---|---|---|---|---|---:|\n")
    for arm in ARMS:
        R = res["readers"][arm]
        L.append(f"| {arm} | **{R['NB-6-emb']['point']:.4f}** [{R['NB-6-emb']['ci_lo']:.4f}, {R['NB-6-emb']['ci_hi']:.4f}] | {R['NB-6-lex']['point']:.4f} | {R['NB-5-emb']['point']:.4f} | {R['NB-5-lex']['point']:.4f} | {R['NB-6-emb']['vs_monitor']['D']:+.4f} ({fmt(R['NB-6-emb']['vs_monitor']['item'])}; {fmt(R['NB-6-emb']['vs_monitor']['cluster'])}) | {R['NB-6-emb']['n_empty']} |\n")
    P2, P3, G1, G2, G3, G4 = (res["readings"][k] for k in ("P2", "P3", "GR-1", "GR-2", "GR-3", "GR-4"))
    L.append(f"\n### AUX-R85-G10-P2 — **{P2['verdict']}**. Under Graphiti's store-written summary GPT-4.1 mini reads {P2['G']:.4f} against {P2['T']:.4f} under the ground-truth summary on the same 323 questions, {P2['D']:+.4f} {'below' if P2['D'] < 0 else 'above or within tolerance of it'} with interval {fmt(P2['item'])} (persona {fmt(P2['persona'])}); a matcher reading Graphiti's own list of superseded names reads {P2['Y']:.4f}. The blind row prints beside, not inside, the criterion: {P2['blind_beside']:.4f} (one value on most questions; Section 4's caveat). BELIEVED-lifted {P2['lifted']:.4f}, TRUE-projected {P2['true_projected']:.4f}, TRUE-projected-lifted {P2['true_projected_lifted']:.4f}, no bar.\n")
    L.append(f"\n### AUX-R85-G10-P3 — **{P3['verdict']}**. A matcher reading Graphiti's own list of superseded names reaches {P3['capped']:.4f} under the capped rendering and {P3['lifted']:.4f} under the lifted (the superseded section is identical under both, the cap never binding on it), {P3['D_from_chance']['capped']:+.4f} from chance, item intervals {P3['capped_ci']} / {P3['lifted_ci']}.\n")
    L.append(f"\n### AUX-R85-G10-GR — GR-1 **{G1['verdict']}**: on Graphiti BELIEVED the paired NOK gain on GPT-4.1 mini is {G1['D']:+.4f}, item {fmt(G1['item'])}, persona {fmt(G1['cluster'])}. GR-2: {G2['status']}; descriptive on the 323 (FOK, {G2['fok_323_descriptive']['positives']} positives): blind {G2['fok_323_descriptive']['blind']:.4f}, TRUE {G2['fok_323_descriptive']['true']:.4f}, BELIEVED {G2['fok_323_descriptive']['believed']:.4f}, gain {G2['fok_323_descriptive']['D_vs_blind']:+.4f} item {fmt(G2['fok_323_descriptive']['item'])} persona {fmt(G2['fok_323_descriptive']['cluster'])}. GR-3 **{G3['verdict']}**: the matcher {G3['Y']:.4f} against the monitor {G3['X']:.4f}, margin {G3['D']:+.4f} ({fmt(G3['item'])}; {fmt(G3['cluster'])}). GR-4 (descriptive): Graphiti BELIEVED's NOK gain over blind {G4['believed_gain_323']:+.4f} is {G4['fraction_of_true_gain_323']:.4f} of FR-Bank's TRUE gain on the same 323 ({G4['true_gain_323']:+.4f}) and {G4['fraction_of_registered_0.2393']:.4f} of the registered 661 gain (+0.2393), beside FR-Bank's own BELIEVED retention of 42.3%. GR-5: {res['readings']['GR-5']['named_at_step_3']}, unchanged by this step.\n")
    L.append(f"\n### AUX-R85-G10-SUMMARY-SPEND — leakage screen ${res['spend']['leak30']:.4f}, probes ${res['spend']['probes']:.4f}, lanes " + ", ".join(f"{a} ${v:.4f}" for a, v in res["spend"]["lanes"].items()) + f"; **Step 4 total ${res['spend']['total']:.4f}**.\n")
    txt = "".join(L)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    {"leak30": cmd_leak30, "probe": cmd_probe, "project": cmd_project, "run": cmd_run, "score": cmd_score}[sys.argv[1]]()
