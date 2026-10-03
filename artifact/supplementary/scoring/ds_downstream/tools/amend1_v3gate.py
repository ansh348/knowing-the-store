"""amend1_v3gate.py -- ADDENDUM_DS Amendment 1 (registrations/ADDENDUM_DS_AMENDMENT_1.md, frozen sha256
72ab84dae2c7e464b1488570d4098aebf59b1de0d442ddc7b6f79a57bfcbbcf5, 2026-09-13; D-DS-3 (b) repair, descriptive).

MODEL CALLS: gpt-4.1-mini only. (1) The 661 obligation calls under the all-states (v3) summary: frozen
prompts_e1 (digests asserted), temperature 0, seed 42, k=1, max_tokens 200, JSON mode, one retry on a parse
failure, cache namespace ds_downstream/cache_amend1/ (arm INDEXED-V3). (2) Stage 2 answer calls for the added
policy MODEL-ALL-V3 on views no registered policy assembled (prompts_ds verbatim; the DS cache is read first
so byte-identical views share the recorded answer). No Haiku, no Opus, no embedding call.

Nothing registered changes: ADDENDUM_DS.md, policies.json, views.json, stage1.json, rows_ds.jsonl, scores_ds.json
are read and never written. The amendment's artifacts are run/*_amend1.json and run/rows_ds_amend1.jsonl.

Subcommands, in order:  lock | probe | project | elicit | stage1 | stage2-project | stage2 | score
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import datetime as dt
import hashlib
import io
import json
import pathlib
import sys
import threading

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ds_common as DC                                                       # noqa: E402
from ds_common import ROOT, DS, RUN, J, jdump, THETA_NOK                     # noqa: E402
import prompts_e1 as P                                                       # noqa: E402
import prompts_ds as PD                                                      # noqa: E402
from build_ds import wilson, pdiff, fmt_i, P_STATES                          # noqa: E402
from common_e1r import auroc, boot_item, boot_cluster                        # noqa: E402
import run_ds as RD                                                          # noqa: E402  (score_answer, records, messages, PRICE)

api = DC.RC.e1_api()
E1_FILE_SHA = "337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84"
E1_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"
REG = ROOT / "registrations" / "ADDENDUM_DS_AMENDMENT_1.md"
REG_SHA = "72ab84dae2c7e464b1488570d4098aebf59b1de0d442ddc7b6f79a57bfcbbcf5"
CACHE1 = DS / "cache_amend1"
POLICY = "MODEL-ALL-V3"
ARM = "INDEXED-V3"
PRICE, LANE, CAP = RD.PRICE, RD.LANE, 3.00
ROWS1 = RUN / "rows_ds_amend1.jsonl"
LEDGER = DS / "NUMBERS_DS.md"


def assert_lineage():
    assert P.file_sha256() == E1_FILE_SHA and P.texts_sha256() == E1_TEXTS_SHA, "prompts_e1 digest drift -- STOP"
    assert (P.MODEL, P.TEMPERATURE, P.SEED, P.MAX_TOKENS) == (LANE, 0, 42, 200), "lane drift -- STOP"
    sha = hashlib.sha256(REG.read_bytes()).hexdigest()
    assert sha == REG_SHA, f"ADDENDUM_DS_AMENDMENT_1.md sha256 {sha} != frozen -- STOP"
    assert PD.from_registration(ROOT / "registrations/ADDENDUM_DS.md") == PD.TEXTS, "prompts_ds differs from the frozen section D.4 -- STOP"


def redirect(seed_from_ds=False):
    CACHE1.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                             # noqa: SLF001
    e0.CACHE_PATH = CACHE1 / "responses.json"; e0.LEDGER_PATH = CACHE1 / "cost_ledger.json"
    e0._cache = None; c = e0._load_cache()                                   # noqa: SLF001
    if seed_from_ds:
        ds_cache = DS / "cache" / "responses.json"
        if ds_cache.exists():
            n0 = len(c)
            for k, v in J(ds_cache).items():
                c.setdefault(k, v)
            print(f"cache seeded with {len(c) - n0} recorded DS answers (read-only copy; ds_downstream/cache is not written)")
    e0.HARD_CAP_USD = CAP
    return e0


# ------------------------------------------------------------------ the v3 summaries and the messages
def v3_text(it):
    v2txt, v3txt, N2, N3, ret_n, exp_n = DC.names_for(it)
    assert v3txt.startswith(v2txt), "v3 must extend v2 byte-identically"
    assert v2txt == it["true_index_text"] if "true_index_text" in it else True
    return v3txt, N2, N3


def messages(it, v3txt):
    return [{"role": "system", "content": P.SYSTEM}, {"role": "user", "content": P.USER_INDEXED.format(index=v3txt, question=it["question"])}]


def committed_v2_text(it):
    """The committed TRUE text of the item's summary, from indexes_v2.json, for the renderer lock."""
    idx = J(ROOT / "e1_metamemory" / "indexes_v2.json")["indexes"]
    return idx[it["index_key"]]


def cmd_lock():
    assert_lineage()
    sub = DC.load_cell()
    idx = J(ROOT / "e1_metamemory" / "indexes_v2.json")["indexes"]
    n_ok, ce_newly = 0, 0
    for it in sub:
        v2txt, v3txt, N2, N3, _, _ = DC.names_for(it)
        assert v3txt.startswith(v2txt) and v2txt == idx[it["index_key"]], it["item_id"]
        n_ok += 1
    pn = [it for it in sub if it["y_nok"]]
    ce = [it for it in pn if it["state"] in ("ret", "exp")]
    newly = [it for it in ce if set(DC.fetch(it, DC.names_for(it)[3])) & set(it["pn_members"]) and not (set(DC.fetch(it, DC.names_for(it)[2])) & set(it["pn_members"]))]
    out = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "renderer_lock": f"{n_ok} / 661 v2 prefixes byte-identical to the committed TRUE text",
           "population": {"n": len(sub), "pn": len(pn), "sup": sum(1 for it in pn if it["state"] == "sup"), "ret": sum(1 for it in pn if it["state"] == "ret"),
                          "exp": sum(1 for it in pn if it["state"] == "exp"), "present": sum(1 for it in sub if it["label"] == "PRESENT"), "absent": sum(1 for it in sub if it["label"] == "ABSENT")},
           "counted_state_items": len(ce), "newly_fetchable_under_v3": len(newly), "theta_nok": THETA_NOK,
           "prompts_e1": {"file": P.file_sha256(), "texts": P.texts_sha256()}, "when": dt.datetime.now().isoformat(timespec="seconds")}
    assert out["population"] == {"n": 661, "pn": 104, "sup": 63, "ret": 26, "exp": 15, "present": 174, "absent": 383}, out["population"]
    assert len(newly) == 17, len(newly)
    jdump(out, RUN / "lock_amend1.json"); print(json.dumps(out, indent=1))


def cmd_probe():
    assert_lineage(); e0 = redirect()
    sub = DC.load_cell()
    first = next(it for it in sub if it["y_nok"] and it["state"] in ("ret", "exp"))
    v3txt, _, _ = v3_text(first)
    r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,   # noqa: SLF001
                                             messages=messages(first, v3txt), response_format={"type": "json_object"})
    o = api.parse_json(r.choices[0].message.content) or {}
    rec = {"item_id": first["item_id"], "state": first["state"], "served": r.model, "identifier_ok": LANE in r.model,
           "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens, "v3_lines": len(v3txt.split("\n")),
           "usd": r.usage.prompt_tokens / 1e6 * PRICE[0] + r.usage.completion_tokens / 1e6 * PRICE[1],
           "status": "OK" if o.get("nok") is not None else "PARSE_FAIL", "sample": (r.choices[0].message.content or "")[:300],
           "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump({"ELICIT": rec}, RUN / "probes_amend1.json"); print(json.dumps(rec, indent=1))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def cmd_project():
    p = J(RUN / "probes_amend1.json")["ELICIT"]
    sub = DC.load_cell()
    lens = [len(DC.names_for(it)[1]) for it in sub]
    # scale the probe's input tokens by summary length (characters), the shell being the prompt without the summary
    probe_len = len(DC.names_for(next(it for it in sub if it["item_id"] == p["item_id"]))[1])
    per_char = p["tok_in"] / max(1, probe_len)
    tin = sum(per_char * L for L in lens); tout = max(1, p["tok_out"]) * len(sub)
    usd = tin / 1e6 * PRICE[0] + tout / 1e6 * PRICE[1]
    # Stage 2: an upper bound of one new call per PN item and per PRESENT item at the DS probe's figure
    dsp = J(RUN / "probes_ds.json")["ANSWER"]
    st2_max = 104 + 174
    usd2 = st2_max * (dsp["tok_in"] / 1e6 * PRICE[0] + dsp["tok_out"] / 1e6 * PRICE[1])
    q4 = ROOT / "q4_inversion_probe" / "run" / "projection_q4.json"
    q4_usd = J(q4)["projected_usd"] if q4.exists() else None
    out = {"elicit_calls": len(sub), "elicit_tok_in": tin, "elicit_tok_out": tout, "elicit_usd": usd, "stage2_upper_bound_calls": st2_max, "stage2_upper_bound_usd": usd2,
           "projected_total_usd": usd + usd2, "x1_3": 1.3 * (usd + usd2), "probe_usd": p["usd"], "q4_projection_usd": q4_usd,
           "combined_with_q4": (usd + usd2 + q4_usd) if q4_usd is not None else None, "cap_combined": CAP, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RUN / "projection_amend1.json"); print(json.dumps(out, indent=1))
    if (out["combined_with_q4"] or out["projected_total_usd"]) > CAP:
        sys.exit("PROJECTION ABOVE THE $3 COMBINED CAP -- STOP")


def _clamp(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    if v > 1:
        v = v / 100.0
    return max(0.0, min(1.0, v))


def one(it):
    v3txt, _, _ = v3_text(it)
    msgs = messages(it, v3txt)
    r = api.call(it["item_id"], ARM, msgs); j = api.parse_json(r["content"]) or {}
    fok, nok = _clamp(j.get("fok")), _clamp(j.get("nok")); n_calls = 1
    if fok is None or nok is None:
        r = api.call(it["item_id"], ARM + "#retry", msgs); j = api.parse_json(r["content"]) or {}
        fok, nok = _clamp(j.get("fok")), _clamp(j.get("nok")); n_calls = 2
    usd = 0.0 if r["cached"] else r["prompt_tokens"] / 1e6 * PRICE[0] + r["completion_tokens"] / 1e6 * PRICE[1]
    return {"item_id": it["item_id"], "arm": ARM, "persona": it["persona"], "label": it["label"], "state": it["state"], "fok": fok, "nok": nok,
            "nok_candidates_found": j.get("nok_candidates_found"), "cached": r["cached"], "n_calls": n_calls, "tok_in": r.get("prompt_tokens"),
            "tok_out": r.get("completion_tokens"), "usd": usd, "status": "OK" if (fok is not None and nok is not None) else "ELICITATION_FAILED",
            "raw": (r["content"] or "")[:300]}


def cmd_elicit():
    assert_lineage(); redirect()
    sub = DC.load_cell()
    out = []
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for n, row in enumerate(ex.map(one, sub), 1):
            out.append(row)
            if n % 100 == 0:
                api.flush(); print(n, "/", len(sub), api.meter(), flush=True)
    api.flush()
    out.sort(key=lambda r: r["item_id"])
    jdump({"meta": {"registration_sha256": REG_SHA, "arm": ARM, "lane": LANE, "temperature": 0, "seed": 42, "max_tokens": 200, "k": 1,
                    "prompts_e1": {"file": P.file_sha256(), "texts": P.texts_sha256()}, "when": dt.datetime.now().isoformat(timespec="seconds")},
           "rows": out}, RUN / "elicitation_v3_amend1.json")
    failed = sum(1 for r in out if r["status"] != "OK")
    print("DONE", len(out), "rows; failed:", failed, "; billed this run: $%.4f" % sum(r["usd"] for r in out), "; meter:", api.meter())
    if failed > 0.02 * len(out):
        sys.exit("STOP: elicitation failures above 2%")


# ------------------------------------------------------------------ stage 1 for MODEL-ALL-V3
def load_v3_rows():
    return {r["item_id"]: r for r in J(RUN / "elicitation_v3_amend1.json")["rows"] if r["status"] == "OK"}


def policy_rows(sub, v3):
    """Per item: gate, abstain, fetched ids, the view (text, ids, sha) under MODEL-ALL-V3."""
    pol = J(DS / "policies.json")["items"]; art = J(ROOT / "resp_review/l2/retrieval.json")["items"]
    out = {}
    for it in sub:
        rec = pol[it["item_id"]]
        gate = v3[it["item_id"]]["nok"] >= THETA_NOK
        abstain = rec["policies"]["MODEL"]["abstain"]
        fetched = DC.fetch(it, set(rec["N3"])) if gate else []
        assert all(DC.flagged(it, e) for e in fetched), "active entry fetched"
        if gate and rec["policies"]["MODEL-ALL"]["gate"]:
            assert fetched == rec["policies"]["MODEL-ALL"]["fetched"], it["item_id"]
        text, ids = DC.assemble_view(it, art[it["item_id"]]["block"], art[it["item_id"]]["top5_ids"], fetched)
        out[it["item_id"]] = {"gate": bool(gate), "abstain": bool(abstain), "fetched": fetched, "view": {"text": text, "ids": ids, "sha": DC.view_sha(text), "n_lines": len(ids)}}
    return out


def cmd_stage1():
    assert_lineage()
    sub = DC.load_cell(); v3 = load_v3_rows(); byid = {it["item_id"]: it for it in sub}
    assert len(v3) == 661, len(v3)
    st1 = J(DS / "stage1.json")["per_item"]
    rows = policy_rows(sub, v3)
    per = {}
    for it in sub:
        r = rows[it["item_id"]]; ids = set(r["view"]["ids"]); pm = set(it.get("pn_members") or []); gold = set(it["gold"])
        per[it["item_id"]] = {"reach": bool(pm & ids) if it["y_nok"] else None,
                              "tagged_reach": bool(any(DC.flagged(it, e) for e in pm & ids)) if it["y_nok"] else None,
                              "successor_in_view": bool(gold & ids) if it["y_nok"] else None,
                              "gold_in_view": bool(gold & ids) if it["label"] == "PRESENT" else None,
                              "coverage": (bool(gold & ids) and not r["abstain"]) if it["label"] == "PRESENT" else None,
                              "abstain": r["abstain"], "view_size": r["view"]["n_lines"], "gate": r["gate"], "view_sha": r["view"]["sha"]}
    pn = [it for it in sub if it["y_nok"]]; pres = [it for it in sub if it["label"] == "PRESENT"]; absn = [it for it in sub if it["label"] == "ABSENT"]
    R = lambda items, key: np.array([per[it["item_id"]][key] for it in items], float)
    R0 = lambda p, items, key: np.array([st1[it["item_id"]][p][key] for it in items], float)
    G = lambda items: [it["persona"] for it in items]
    rate = {"gate_fires": sum(1 for it in sub if per[it["item_id"]]["gate"]), "abstentions": sum(1 for it in sub if per[it["item_id"]]["abstain"]),
            "pn_reach": {}, "pn_tagged": {}, "pn_successor": {}, "pn_abstain": sum(1 for it in pn if per[it["item_id"]]["abstain"])}
    for st, name in [(None, "all")] + [(s, n) for s, n in P_STATES]:
        sel = [it for it in pn if st is None or it["state"] == st]
        k = int(R(sel, "reach").sum()); rate["pn_reach"][name] = {"reached": k, "n": len(sel), "rate": k / len(sel), "wilson": wilson(k, len(sel))}
        rate["pn_tagged"][name] = int(R(sel, "tagged_reach").sum()); rate["pn_successor"][name] = int(R(sel, "successor_in_view").sum())
    c = int(R(pres, "coverage").sum()); gv = int(R(pres, "gold_in_view").sum()); ab = int(R(pres, "abstain").sum())
    rate["present"] = {"coverage": c, "n": 174, "rate": c / 174, "wilson": wilson(c, 174), "gold_in_view": gv, "abstained": ab}
    a383 = int(R(absn, "abstain").sum()); a272 = int(sum(1 for it in absn if it["tier"] == "hard" and per[it["item_id"]]["abstain"]))
    rate["absent"] = {"abstain_383": a383, "rate_383": a383 / 383, "abstain_272": a272, "rate_272": a272 / 272}
    vs = [per[it["item_id"]]["view_size"] for it in sub]; vp = [per[it["item_id"]]["view_size"] for it in pn]
    rate["view_size"] = {"mean_661": float(np.mean(vs)), "max_661": int(max(vs)), "mean_104": float(np.mean(vp)), "max_104": int(max(vp))}
    # gate flag counts by label
    gate_by = collections.Counter(it["label"] for it in sub if per[it["item_id"]]["gate"])
    rate["gate_by_label"] = {"PN": gate_by.get("PRESENT-NEGATIVE", 0), "PRESENT": gate_by.get("PRESENT", 0), "ABSENT": gate_by.get("ABSENT", 0)}
    rate["gate_by_state"] = {s: sum(1 for it in pn if it["state"] == s and per[it["item_id"]]["gate"]) for s, _ in P_STATES}
    v2gate = {it["item_id"]: st1[it["item_id"]]["MODEL"]["gate"] for it in sub}
    rate["gate_agreement_with_v2"] = {"both": sum(1 for it in sub if per[it["item_id"]]["gate"] and v2gate[it["item_id"]]),
                                      "v3_only": sum(1 for it in sub if per[it["item_id"]]["gate"] and not v2gate[it["item_id"]]),
                                      "v2_only": sum(1 for it in sub if not per[it["item_id"]]["gate"] and v2gate[it["item_id"]])}
    # the DS-P4 quantity, descriptive
    ce = [it for it in pn if it["state"] in ("ret", "exp")]
    Mce, MAV3ce = R0("MODEL", ce, "reach"), R(ce, "reach")
    p4 = pdiff(MAV3ce, Mce, G(ce))
    p4_all = pdiff(R(pn, "reach"), R0("MODEL", pn, "reach"), G(pn))
    newly = [it for it in ce if set(DC.fetch(it, DC.names_for(it)[3])) & set(it["pn_members"]) and not (set(DC.fetch(it, DC.names_for(it)[2])) & set(it["pn_members"]))]
    g_newly = sum(1 for it in newly if per[it["item_id"]]["gate"])
    g_newly_missed = sum(1 for it in newly if per[it["item_id"]]["gate"] and not st1[it["item_id"]]["ALWAYS"]["reach"])
    reached_newly = sum(1 for it in newly if per[it["item_id"]]["reach"])
    # MODEL-ALL-V3 against ORACLE on the counted states, descriptive
    Oce = R0("ORACLE", ce, "reach"); Ace = R0("ALWAYS", ce, "reach")
    desc = {"MAV3_minus_M_ce41": {"MAV3": p4["a"], "M": p4["b"], "D": p4["D"], "item": p4["item"], "cluster": p4["cluster"], "n": len(ce)},
            "MAV3_minus_M_104": {"MAV3": p4_all["a"], "M": p4_all["b"], "D": p4_all["D"], "item": p4_all["item"], "cluster": p4_all["cluster"]},
            "newly_fetchable": len(newly), "v3_gate_fires_on_newly": g_newly, "v3_gate_fires_on_newly_the_retriever_misses": g_newly_missed, "newly_reached": reached_newly,
            "ce41_reach": {"ALWAYS": float(Ace.mean()), "MODEL": float(Mce.mean()), "MODEL-ALL-V3": float(MAV3ce.mean()), "ORACLE": float(Oce.mean())}}
    # the v3 monitor row
    y = np.array([it["y_nok"] for it in sub], int); s3 = np.array([v3[it["item_id"]]["nok"] for it in sub], float)
    s2 = np.array([it["true"]["nok"] for it in sub], float); g = np.array([it["persona"] for it in sub])
    row = {"auroc_v3": round(float(auroc(s3, y)), 4), "auroc_v2_committed": round(float(auroc(s2, y)), 4), "distinct_values_v3": int(len(set(np.round(s3, 6).tolist()))),
           "paired_v3_minus_v2": {"delta": round(float(auroc(s3, y) - auroc(s2, y)), 4), "item": boot_item(s2, s3, y), "cluster": boot_cluster(s2, s3, y, g)},
           "per_state": {}}
    neg = y == 0
    for st, name in P_STATES:
        m = neg | np.array([it["state"] == st for it in sub])
        row["per_state"][name] = {"n_pos": int(sum(1 for it in sub if it["state"] == st)), "v3": round(float(auroc(s3[m], y[m])), 4), "v2": round(float(auroc(s2[m], y[m])), 4),
                                  "paired": boot_item(s2[m], s3[m], y[m])}
    row["fok_v3_auroc_307"] = round(float(auroc(np.array([v3[it["item_id"]]["fok"] for it in sub if it["tier"] == "hard"], float),
                                                 np.array([it["y_fok"] for it in sub if it["tier"] == "hard"], int))), 4)
    S = {"registration_sha256": REG_SHA, "policy": POLICY, "per_item": per, "rates": rate, "descriptive": desc, "v3_row": row, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(S, RUN / "stage1_amend1.json")
    print(json.dumps({"rates": {k: v for k, v in rate.items() if k != "pn_successor"}, "descriptive": desc, "v3_row": {k: v for k, v in row.items() if k != "per_state"}}, indent=1, default=float))


# ------------------------------------------------------------------ stage 2 for MODEL-ALL-V3
def stage2_jobs():
    sub = DC.load_cell(); v3 = load_v3_rows(); rows = policy_rows(sub, v3)
    st1a = J(RUN / "stage1_amend1.json")["per_item"]
    done = {json.loads(l)["key"]: json.loads(l) for l in io.open(RD.ROWS_P, encoding="utf-8")}
    jobs = []
    for it in sub:
        r = rows[it["item_id"]]; s = st1a[it["item_id"]]
        if s["abstain"] or it["label"] == "ABSENT" or (it["label"] == "PRESENT-NEGATIVE" and not s["reach"]):
            continue
        key = f"{it['item_id']}|{r['view']['sha']}"
        jobs.append({"key": key, "item_id": it["item_id"], "persona": it["persona"], "question": it["question"], "label": it["label"], "state": it["state"],
                     "view": r["view"]["text"], "view_sha": r["view"]["sha"], "n_lines": r["view"]["n_lines"], "policies": [POLICY], "recorded": key in done})
    return sub, jobs, done


def cmd_stage2_project():
    sub, jobs, done = stage2_jobs()
    new = [j for j in jobs if not j["recorded"]]
    dsp = J(RUN / "probes_ds.json")["ANSWER"]; per_line = 45.0; shell = max(50.0, dsp["tok_in"] - per_line * dsp["view_lines"])
    tin = sum(shell + per_line * j["n_lines"] for j in new); tout = dsp["tok_out"] * len(new)
    usd = tin / 1e6 * PRICE[0] + tout / 1e6 * PRICE[1]
    el = J(RUN / "elicitation_v3_amend1.json")["rows"]; billed = sum(r["usd"] for r in el) + J(RUN / "probes_amend1.json")["ELICIT"]["usd"]
    q4 = ROOT / "q4_inversion_probe" / "results" / "q4_scores.json"
    q4_spend = J(q4)["spend"]["total"] if q4.exists() else J(ROOT / "q4_inversion_probe" / "run" / "projection_q4.json")["projected_usd"]
    out = {"stage2_population": len(jobs), "recorded_in_ds": len(jobs) - len(new), "new_calls": len(new), "pn_new": sum(1 for j in new if j["label"] == "PRESENT-NEGATIVE"),
           "present_new": sum(1 for j in new if j["label"] == "PRESENT"), "projected_usd": usd, "billed_so_far_amend1": billed, "q4_spend_or_projection": q4_spend,
           "combined": billed + usd + q4_spend, "cap_combined": CAP, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RUN / "projection_stage2_amend1.json"); print(json.dumps(out, indent=1))
    if out["combined"] > CAP:
        sys.exit("COMBINED PROJECTION ABOVE THE $3 CAP -- STOP")


def cmd_stage2():
    assert_lineage(); redirect(seed_from_ds=True)
    sub, jobs, done = stage2_jobs()
    have = {json.loads(l)["key"] for l in io.open(ROWS1, encoding="utf-8")} if ROWS1.exists() else set()
    todo = [j for j in jobs if j["key"] not in have]
    print(f"{len(todo)} rows to write ({sum(1 for j in todo if j['recorded'])} recorded answers copied, {sum(1 for j in todo if not j['recorded'])} new calls)", flush=True)
    lock = threading.Lock()

    def work(job):
        if job["recorded"]:
            r = dict(done[job["key"]]); r["policies"] = [POLICY]; r["source"] = "ds_downstream/run/rows_ds.jsonl"; r["usd"] = 0.0
        else:
            r = RD.answer(job); r["source"] = "amend1 call"
        with lock:
            with io.open(ROWS1, "a", encoding="utf-8") as f:
                f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
        return r
    try:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            out = list(ex.map(work, todo))
    finally:
        api.flush()
    c = collections.Counter(r["status"] for r in out)
    print(f"DONE {len(out)} rows; status {dict(c)}; billed this step ${sum(r.get('usd', 0.0) for r in out):.4f}")


def cmd_score():
    sys.stdout.reconfigure(encoding="utf-8")
    sub = DC.load_cell(); byid = {it["item_id"]: it for it in sub}
    rec = RD.records(sub); st1a = J(RUN / "stage1_amend1.json"); per = st1a["per_item"]
    rows = {}
    for l in io.open(ROWS1, encoding="utf-8"):
        r = json.loads(l); rows[r["key"]] = r
    per_row = {}
    for key, r in rows.items():
        it = byid[r["item_id"]]
        if r["status"] != "OK" or rec.get(r["item_id"]) is None:
            per_row[key] = {"status": r["status"], "scored": False}; continue
        per_row[key] = {"status": "OK", "scored": True, **RD.score_answer(it, rec[r["item_id"]], r["answer"])}
    pn_rows = [(k, s) for k, s in per_row.items() if s["scored"] and byid[rows[k]["item_id"]]["label"] == "PRESENT-NEGATIVE"]
    pr_rows = [(k, s) for k, s in per_row.items() if s["scored"] and byid[rows[k]["item_id"]]["label"] == "PRESENT"]
    d = {"pn_answered": len(pn_rows), "present_answered": len(pr_rows), "pn_abstained": sum(1 for it in sub if it["y_nok"] and per[it["item_id"]]["abstain"]),
         "new_calls": sum(1 for r in rows.values() if r.get("source") == "amend1 call"), "recorded_reused": sum(1 for r in rows.values() if r.get("source") != "amend1 call")}
    for split, pred in (("all", lambda it: True), ("tagged", lambda it: per[it["item_id"]]["tagged_reach"]), ("untagged", lambda it: not per[it["item_id"]]["tagged_reach"])):
        sel = [s for k, s in pn_rows if pred(byid[rows[k]["item_id"]])]; n = len(sel)
        d[f"pn_{split}"] = {"n": n, "stale_use": sum(1 for s in sel if s["stale_use"]), "stale_surface": sum(1 for s in sel if s["stale_surface"]),
                            "stale_use_tau_gold": sum(1 for s in sel if s["stale_use_tau_gold"]), "successor_use": sum(1 for s in sel if s.get("successor_use")),
                            "n_supersession": sum(1 for s in sel if s.get("successor_use") is not None), "both": sum(1 for s in sel if s.get("both"))}
    for st in ("sup", "ret", "exp"):
        sel = [s for k, s in pn_rows if byid[rows[k]["item_id"]]["state"] == st]
        d[f"pn_state_{st}"] = {"n": len(sel), "stale_use": sum(1 for s in sel if s["stale_use"]), "stale_use_tau_gold": sum(1 for s in sel if s["stale_use_tau_gold"])}
    d["present"] = {"n": len(pr_rows), "correct": sum(1 for k, s in pr_rows if s["correct"]), "correct_tau_hi": sum(1 for k, s in pr_rows if s["correct_tau_hi"])}
    el = J(RUN / "elicitation_v3_amend1.json")["rows"]
    spend = {"probe": J(RUN / "probes_amend1.json")["ELICIT"]["usd"], "elicit": sum(r["usd"] for r in el), "stage2": sum(r.get("usd", 0.0) for r in rows.values())}
    spend["total"] = spend["probe"] + spend["elicit"] + spend["stage2"]
    S = {"registration_sha256": REG_SHA, "policy": POLICY, "stage2": d, "per_row": per_row, "spend": spend,
         "elicitation": {"rows": len(el), "failed": sum(1 for r in el if r["status"] != "OK"), "cached": sum(1 for r in el if r["cached"])},
         "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(S, RUN / "scores_amend1.json")
    txt = ledger_text(st1a, S)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


def ledger_text(st1a, S):
    r, desc, row, d, sp = st1a["rates"], st1a["descriptive"], st1a["v3_row"], S["stage2"], S["spend"]
    today = dt.date.today().isoformat(); f = lambda k, n: f"{k} / {n} = {k / n:.4f}" if n else "—"
    lock = J(RUN / "lock_amend1.json"); probe = J(RUN / "probes_amend1.json")["ELICIT"]; proj = J(RUN / "projection_amend1.json"); proj2 = J(RUN / "projection_stage2_amend1.json")
    W = lambda w: f"[{w[0]:.3f}, {w[1]:.3f}]" if isinstance(w, (list, tuple)) else str(w)
    pr = r["pn_reach"]
    return f"""
---

## 6. Amendment 1 — the fetch gate elicited under the all-states summary (descriptive; D-DS-3 (b) repair; written {today}, R103)

Registration `registrations/ADDENDUM_DS_AMENDMENT_1.md`, frozen sha256 `{REG_SHA}` before the first call (copy in
`iclr2027_monitoring_submission/ARTIFACT/registrations/`). **Descriptive: no bar, no prediction, no verdict; DS-P4 stands as FAILS.**
Sources: `run/lock_amend1.json`, `run/probes_amend1.json`, `run/projection_amend1.json`, `run/elicitation_v3_amend1.json`,
`run/stage1_amend1.json`, `run/projection_stage2_amend1.json`, `run/rows_ds_amend1.jsonl`, `run/scores_amend1.json`. Nothing
registered was written.

### AUX-DS-A1-LOCK, AUX-DS-A1-PROBE, AUX-DS-A1-PROJECTION

Renderer lock {lock['renderer_lock']}; population 661 / 104 = 63 / 26 / 15; 174 PRESENT; 383 ABSENT; counted-state items {lock['counted_state_items']},
newly fetchable under the v3 names {lock['newly_fetchable_under_v3']}; θ_NOK {THETA_NOK:.6f}. Served `{probe['served']}` (identifier ok: {probe['identifier_ok']}), {probe['tok_in']} in /
{probe['tok_out']} out on a {probe['v3_lines']}-line v3 summary. Projection: {proj['elicit_calls']} elicitation calls ${proj['elicit_usd']:.4f}, Stage 2 upper bound
{proj['stage2_upper_bound_calls']} calls ${proj['stage2_upper_bound_usd']:.4f}, total ${proj['projected_total_usd']:.4f} (x1.3 ${proj['x1_3']:.4f}) against the combined $3.00 cap.

### AUX-DS-A1-V3ROW — mini's obligation score under the all-states summary, the row §C.4 said did not exist

Lane `gpt-4.1-mini`, temperature 0, seed 42, max_tokens 200, JSON mode, k = 1, one retry on a parse failure; {S['elicitation']['rows']} rows,
{S['elicitation']['failed']} failures. NOK AUROC on the 661: **{row['auroc_v3']:.4f}** under the all-states summary against {row['auroc_v2_committed']:.4f} committed under the
superseded-only summary, paired difference {row['paired_v3_minus_v2']['delta']:+.4f} (item-level {fmt_i(row['paired_v3_minus_v2']['item'])}; persona-clustered
{fmt_i(row['paired_v3_minus_v2']['cluster'])}); `nok` takes {row['distinct_values_v3']} distinct values. Per state (positives of one state against the 557 negatives):
""" + "; ".join(f"{name} {v['v3']:.4f} against {v['v2']:.4f} (paired {fmt_i(v['paired'])})" for name, v in row["per_state"].items()) + f""".
FOK under the v3 summary on the 307 (descriptive, unused by any gate): {row['fok_v3_auroc_307']:.4f}.

### AUX-DS-A1-GATE — `nok3 ≥ θ_NOK`, by label and state, beside the committed gate (75 = 56 / 9 / 10)

Fires on **{r['gate_fires']}** of 661: PN {r['gate_by_label']['PN']} / PRESENT {r['gate_by_label']['PRESENT']} / ABSENT {r['gate_by_label']['ABSENT']}; by state sup {r['gate_by_state']['sup']} of 63,
ret {r['gate_by_state']['ret']} of 26, exp {r['gate_by_state']['exp']} of 15. Agreement with the committed v2 gate: both fire {r['gate_agreement_with_v2']['both']}, v3 only
{r['gate_agreement_with_v2']['v3_only']}, v2 only {r['gate_agreement_with_v2']['v2_only']}. Abstention is the committed coverage gate ({r['abstentions']} abstentions, {r['pn_abstain']} on PN), unchanged.

### AUX-DS-A1-REACH, -PRESENT, -ABSTAIN, -VIEWSIZE — Stage 1 for MODEL-ALL-V3 (the AUX-DS-REACH row format)

| policy | gate fires | abstentions | PN reach all (Wilson) | sup | ret | exp | tagged all | successor in view (all) | PN abstained |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|
| MODEL-ALL-V3 | {r['gate_fires']} | {r['abstentions']} | **{pr['all']['reached']} / 104 = {pr['all']['rate']:.4f}** {W(pr['all']['wilson'])} | {pr['supersession']['reached']} / 63 | {pr['retraction']['reached']} / 26 | {pr['expiry']['reached']} / 15 | {r['pn_tagged']['all']} | {r['pn_successor']['all']} | {r['pn_abstain']} |

PRESENT coverage {r['present']['coverage']} / 174 = {r['present']['rate']:.4f} {W(r['present']['wilson'])} (gold in view {r['present']['gold_in_view']}, abstained {r['present']['abstained']}); ABSENT abstention
{r['absent']['abstain_383']} / 383 and {r['absent']['abstain_272']} / 272; view size mean {r['view_size']['mean_661']:.2f} on the 661 (max {r['view_size']['max_661']}), {r['view_size']['mean_104']:.2f} on the 104 (max {r['view_size']['max_104']}).

### AUX-DS-A1-P4DESC — the DS-P4 quantity under the v3-elicited gate (descriptive; the verdict is not re-adjudicated)

On the 41 retraction- and expiry-derived obligations: ALWAYS {desc['ce41_reach']['ALWAYS']:.4f}, MODEL {desc['ce41_reach']['MODEL']:.4f}, **MODEL-ALL-V3 {desc['ce41_reach']['MODEL-ALL-V3']:.4f}**, ORACLE
{desc['ce41_reach']['ORACLE']:.4f}; MODEL-ALL-V3 − MODEL = **{desc['MAV3_minus_M_ce41']['D']:+.4f}** (item-level {fmt_i(desc['MAV3_minus_M_ce41']['item'])}; persona-clustered
{fmt_i(desc['MAV3_minus_M_ce41']['cluster'])}). Of the {desc['newly_fetchable']} records naming makes fetchable, the v3 gate fires on **{desc['v3_gate_fires_on_newly']}** ({desc['v3_gate_fires_on_newly_the_retriever_misses']} of them ones the
retriever misses) and {desc['newly_reached']} are reached. On the 104: MODEL-ALL-V3 {desc['MAV3_minus_M_104']['MAV3']:.4f} against MODEL {desc['MAV3_minus_M_104']['M']:.4f}, {desc['MAV3_minus_M_104']['D']:+.4f}
(item-level {fmt_i(desc['MAV3_minus_M_104']['item'])}; persona-clustered {fmt_i(desc['MAV3_minus_M_104']['cluster'])}).

### AUX-DS-A1-STAGE2 — the answer stage for MODEL-ALL-V3

Stage 2 population {proj2['stage2_population']} distinct (item, view) pairs: {proj2['recorded_in_ds']} answered by a registered policy's byte-identical view (the recorded answer
is read; `ds_downstream/cache` is not written), {proj2['new_calls']} new calls ({proj2['pn_new']} PN, {proj2['present_new']} PRESENT), prompts_ds verbatim, the committed detector as §D.4.

| policy | PN reached ∧ answered | PN abstained | stale use (all) | tagged | untagged | stale surfacing | stale use at TAU_GOLD (all) | tagged | untagged | successor use (of supersession) | both | PRESENT answered | correct (TAU_GOLD) | at TAU_HI |
|---|---:|---:|---|---|---|---:|---|---|---|---|---:|---:|---|---:|
| MODEL-ALL-V3 | {d['pn_answered']} | {d['pn_abstained']} | {f(d['pn_all']['stale_use'], d['pn_all']['n'])} | {f(d['pn_tagged']['stale_use'], d['pn_tagged']['n'])} | {f(d['pn_untagged']['stale_use'], d['pn_untagged']['n'])} | {d['pn_all']['stale_surface']} | {f(d['pn_all']['stale_use_tau_gold'], d['pn_all']['n'])} | {f(d['pn_tagged']['stale_use_tau_gold'], d['pn_tagged']['n'])} | {f(d['pn_untagged']['stale_use_tau_gold'], d['pn_untagged']['n'])} | {f(d['pn_all']['successor_use'], d['pn_all']['n_supersession'])} | {d['pn_all']['both']} | {d['present_answered']} | {f(d['present']['correct'], d['present']['n'])} | {d['present']['correct_tau_hi']} |

Per state (stale use at TAU_HI / at TAU_GOLD / answered): sup {d['pn_state_sup']['stale_use']} / {d['pn_state_sup']['stale_use_tau_gold']} / {d['pn_state_sup']['n']}; ret {d['pn_state_ret']['stale_use']} / {d['pn_state_ret']['stale_use_tau_gold']} / {d['pn_state_ret']['n']};
exp {d['pn_state_exp']['stale_use']} / {d['pn_state_exp']['stale_use_tau_gold']} / {d['pn_state_exp']['n']}.

### AUX-DS-A1-SPEND

Billed from response usage at $0.40 / $1.60 per 1M: probe ${sp['probe']:.4f}, elicitation ${sp['elicit']:.4f} ({S['elicitation']['cached']} served from cache), Stage 2 ${sp['stage2']:.4f}
— **total ${sp['total']:.4f}** against the combined $3.00 cap shared with the Q4 probe. No Haiku, no Opus, no embedding call.
"""


if __name__ == "__main__":
    {"lock": cmd_lock, "probe": cmd_probe, "project": cmd_project, "elicit": cmd_elicit, "stage1": cmd_stage1,
     "stage2-project": cmd_stage2_project, "stage2": cmd_stage2, "score": cmd_score}[sys.argv[1]]()
