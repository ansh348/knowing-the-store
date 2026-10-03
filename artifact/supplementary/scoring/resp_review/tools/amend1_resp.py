"""amend1_resp.py -- ADDENDUM_RESP Amendment 1 (registrations/ADDENDUM_RESP_AMENDMENT_1.md, frozen by sha256 before the
first call; program R108, 2026-09-14). Section A: the retrieved view under FR-Bank's own lifecycle marks (RETRIEVED-BELIEVED,
gpt-4.1-mini, 661, k = 1). Section B: Haiku 4.5 at k = 5 on HYBRID, then RETRIEVED, then V2-OWN, Batch API, cap $12 in that
order. Descriptive: no bar, no prediction, no verdict.

MODEL CALLS: section A -- gpt-4.1-mini synchronous (temperature 0, seed 42, max_tokens 200, JSON mode, one retry), 661 calls,
cache resp_review/cache_amend1/. Section B -- claude-haiku-4-5-20251001 through the Anthropic Batch API (temperature 0,
max_tokens 200, five draws), one synchronous probe per lane. Nothing registered is written; the recorded rows
(run/rows_resp.jsonl, r74/x4/rows_H45.jsonl) are read, never re-elicited.

Subcommands, in order:
  lock                registration sha256, prompt digests, the believed blocks, the tag census -> run/lock_amend1.json, l2/retrieval_believed.json
  probe-mini          one gpt-4.1-mini call on a RETRIEVED-BELIEVED prompt                     -> run/probes_amend1.json
  run-mini            the 661 calls                                                            -> run/rows_amend1_mini.jsonl
  probe-h45 <lane>    one Haiku 4.5 call (served identifier, tokens); lane in HYBRID | RETRIEVED | OWN
  submit-h45 <lane>   project against the cap net of earlier lanes; submit the Batch if it fits -> run/batch_amend1_<lane>.json
  poll-h45 <lane>     poll; collect rows when ended                                              -> run/rows_amend1_H45_<lane>.jsonl
  score               everything present; NUMBERS_RESP.md section 7 (AUX-RESP-A1-*)            -> run/scores_amend1.json
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import datetime as dt
import hashlib
import io
import json
import os
import sys
import threading

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import resp_common as RC                                                     # noqa: E402
from resp_common import ROOT, RESP, L1, L2, RUN, J, jdump                    # noqa: E402
import run_resp as RR                                                        # noqa: E402
import prompts_resp as PR                                                    # noqa: E402
import prompts_e1 as P                                                       # noqa: E402
from index_v2 import parse_dt                                                # noqa: E402
from backends import load_backend                                            # noqa: E402
from common_e1r import auroc                                                 # noqa: E402

sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
from run_cf import last_json, load_env, make_row                             # noqa: E402

api = RC.e1_api()
REG = ROOT / "registrations" / "ADDENDUM_RESP_AMENDMENT_1.md"
REG_SHA = "40b4c4084f89e41d38ff1b558c1db033bdcec88a5787a3feada9fe94ad321c9d"
CACHE1 = RESP / "cache_amend1"
LEDGER = RESP / "NUMBERS_RESP.md"
LANE_MINI, PRICE_MINI = "gpt-4.1-mini", (0.40, 1.60)
LANE_H45, PRICE_H45, MULT_H45, K = "claude-haiku-4-5-20251001", (1.00, 5.00), 0.5, 5
CAP_H45 = 12.00
ORDER = ("HYBRID", "RETRIEVED", "OWN")
ARM_OF = {"HYBRID": "HYBRID", "RETRIEVED": "RETRIEVED", "OWN": "V2-OWN"}
ROWS_MINI = RUN / "rows_amend1_mini.jsonl"
STATES = RR.STATES


def rows_h45(lane):
    return RUN / f"rows_amend1_H45_{lane}.jsonl"


def assert_lineage():
    h = hashlib.sha256(REG.read_bytes()).hexdigest()
    assert h == REG_SHA, f"ADDENDUM_RESP_AMENDMENT_1.md sha256 {h} != frozen -- STOP"
    RR.assert_lineage()
    d = PR.digests()
    assert d["SYSTEM_RETRIEVED"].startswith("602b9431") and d["USER_RETRIEVED"].startswith("d9031f6f") and d["USER_HYBRID"].startswith("b29d1e47"), "prompts_resp digest drift -- STOP"


def redirect():
    CACHE1.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                             # noqa: SLF001
    e0.CACHE_PATH = CACHE1 / "responses.json"; e0.LEDGER_PATH = CACHE1 / "cost_ledger.json"
    e0._cache = None; e0._load_cache()                                       # noqa: SLF001
    e0.HARD_CAP_USD = 4.00
    return e0


# ------------------------------------------------------------------ section A: the believed blocks
def believed_flags():
    """Per persona: the TRUE flag record of each entry with the lifecycle booleans replaced by the store's own marks
    (index_v2.believed_lifecycle's rule: believed_superseded, believed_retracted, event_time before the persona's cutoff)."""
    joins = RC.load_joins(); true = RC.true_flags()
    raw = collections.defaultdict(dict)
    for r in load_backend("frbank"):
        raw[r["persona"]][r["entry_id"]] = r
    out = {}
    for name, fl in true.items():
        cutoff = joins[name].cutoff; d = {}
        for eid, f in fl.items():
            r = raw[name][eid]; ev = parse_dt(r["event_time"])
            d[eid] = {**f, "superseded": bool(r["believed_superseded"]), "retracted": bool(r["believed_retracted"]),
                      "expired": bool(ev is not None and cutoff is not None and ev < cutoff)}
        out[name] = d
    return out


def build_believed():
    sub = RC.load_cell(); ret = J(L2 / "retrieval.json")["items"]; bf = believed_flags(); tf = RC.true_flags()
    items, census = {}, collections.Counter()
    tag_lines = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}; tag_pn = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    for it in sub:
        rec = ret[it["item_id"]]; ids = rec["top5_ids"]; per = it["persona"]
        lines = []
        for r, eid in enumerate(ids):
            lines.append(RC.render_line(r + 1, bf[per][eid]))
            t_tag, b_tag = RC.lifecycle_tag(tf[per][eid]), RC.lifecycle_tag(bf[per][eid])
            census["changed" if t_tag != b_tag else "same"] += 1
            t_na, b_na = t_tag != "active", b_tag != "active"
            key = "tp" if (t_na and b_na) else "fp" if (b_na and not t_na) else "fn" if (t_na and not b_na) else "tn"
            tag_lines[key] += 1
            if it["y_nok"] and eid in set(it.get("pn_members") or []):
                tag_pn[key] += 1
        block = "\n".join(lines)
        assert block.count("\n") == rec["block"].count("\n")
        items[it["item_id"]] = {"top5_ids": ids, "block": block, "changed_lines": sum(1 for r, eid in enumerate(ids) if RC.lifecycle_tag(tf[per][eid]) != RC.lifecycle_tag(bf[per][eid]))}
    def prf(c):
        p = c["tp"] / (c["tp"] + c["fp"]) if c["tp"] + c["fp"] else None; r = c["tp"] / (c["tp"] + c["fn"]) if c["tp"] + c["fn"] else None
        return {**c, "precision": p, "recall": r}
    meta = {"lines": sum(census.values()), "lines_changed": census["changed"], "items_with_a_changed_line": sum(1 for v in items.values() if v["changed_lines"]),
            "non_active_lines": prf(tag_lines), "forbidding_records_in_view": prf(tag_pn)}
    return sub, items, meta


def cmd_lock():
    assert_lineage()
    sub, items, meta = build_believed()
    jdump({"meta": {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "rule": "index_v2.believed_lifecycle on the same top5_ids; render_line unchanged",
                    "built": dt.datetime.now().isoformat(timespec="seconds")}, "items": items}, L2 / "retrieval_believed.json")
    out = {"registration_sha256": REG_SHA, "prompts_resp": PR.digests(), "prompts_e1": {"file": P.file_sha256(), "texts": P.texts_sha256()},
           "n_items": len(items), "tags": meta, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RUN / "lock_amend1.json"); print(json.dumps(out, indent=1))


def msgs_mini(it, block):
    return [{"role": "system", "content": PR.SYSTEM_RETRIEVED}, {"role": "user", "content": PR.USER_RETRIEVED.format(retrieved=block, question=it["question"])}]


def probes():
    p = RUN / "probes_amend1.json"
    return J(p) if p.exists() else {}


def cmd_probe_mini():
    assert_lineage(); e0 = redirect(); sub = RC.load_cell(); bl = J(L2 / "retrieval_believed.json")["items"]
    first = next(it for it in sub if bl[it["item_id"]]["changed_lines"])
    r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,   # noqa: SLF001
                                             messages=msgs_mini(first, bl[first["item_id"]]["block"]), response_format={"type": "json_object"})
    o = api.parse_json(r.choices[0].message.content) or {}
    rec = {"item_id": first["item_id"], "served": r.model, "identifier_ok": LANE_MINI in r.model, "tok_in": r.usage.prompt_tokens, "tok_out": r.usage.completion_tokens,
           "usd": r.usage.prompt_tokens / 1e6 * PRICE_MINI[0] + r.usage.completion_tokens / 1e6 * PRICE_MINI[1],
           "status": "OK" if RR.clamp(o.get("fok")) is not None and RR.clamp(o.get("nok")) is not None else "PARSE_FAIL",
           "sample": (r.choices[0].message.content or "")[:200], "when": dt.datetime.now().isoformat(timespec="seconds")}
    out = probes(); out["MINI"] = rec; jdump(out, RUN / "probes_amend1.json"); print(json.dumps(rec, indent=1))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def cmd_run_mini():
    assert_lineage(); redirect(); sub = RC.load_cell(); bl = J(L2 / "retrieval_believed.json")["items"]
    have = {json.loads(l)["item_id"] for l in io.open(ROWS_MINI, encoding="utf-8")} if ROWS_MINI.exists() else set()
    todo = [it for it in sub if it["item_id"] not in have]
    print(f"{len(todo)} calls to go (resumed past {len(have)})", flush=True)
    lock = threading.Lock()

    def work(it):
        row = {"item_id": it["item_id"], "arm": "RETRIEVED-BELIEVED", "persona": it["persona"], "question": it["question"], "label": it["label"],
               "state": it["state"], "y_nok": it["y_nok"], "y_fok": it["y_fok"], "tier": it["tier"], "index_key": it["index_key"]}
        texts = {"block": {it["item_id"]: bl[it["item_id"]]["block"]}}
        RR_row = dict(row); RR_row["arm"] = "RETRIEVED"          # run_resp.elicit builds the RETRIEVED messages from texts["block"]
        r = RR.elicit(RR_row, texts); r["arm"] = "RETRIEVED-BELIEVED"
        with lock:
            with io.open(ROWS_MINI, "a", encoding="utf-8") as f:
                f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
        return r
    try:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            out = list(ex.map(work, todo))
    finally:
        api.flush()
    c = collections.Counter(r["status"] for r in out)
    print(f"DONE {len(out)} rows; status {dict(c)}; billed ${sum(r['usd'] for r in out):.4f}")


# ------------------------------------------------------------------ section B: Haiku 4.5 lanes
def h45_units(lane):
    """The prompts of one lane: (unit_id, system, user)."""
    sub, cell, texts = RR.build_cell()
    arm = ARM_OF[lane]
    rows = cell[arm]
    units = []
    for r in rows:
        m = RR.messages(r, texts)
        units.append({"unit_id": r["item_id"], "persona": r["persona"], "state": r["state"], "y_nok": r["y_nok"], "y_fok": r["y_fok"], "tier": r["tier"],
                      "system": m[0]["content"], "user": m[1]["content"]})
    return units


def anthropic_client():
    load_env()
    import anthropic
    return anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def cmd_probe_h45(lane):
    assert_lineage(); units = h45_units(lane); u = units[0]
    cl = anthropic_client()
    r = cl.messages.create(model=LANE_H45, max_tokens=200, temperature=0.0, system=u["system"], messages=[{"role": "user", "content": u["user"]}])
    text = "".join(b.text for b in r.content if b.type == "text"); j = last_json(text) or {}
    rec = {"lane": lane, "unit_id": u["unit_id"], "served": r.model, "identifier_ok": r.model == LANE_H45, "tok_in": r.usage.input_tokens, "tok_out": r.usage.output_tokens,
           "usd": r.usage.input_tokens / 1e6 * PRICE_H45[0] + r.usage.output_tokens / 1e6 * PRICE_H45[1],
           "status": "OK" if RR.clamp(j.get("fok")) is not None and RR.clamp(j.get("nok")) is not None else "PARSE_FAIL",
           "n_requests": len(units) * K, "sample": text[:200], "when": dt.datetime.now().isoformat(timespec="seconds")}
    out = probes(); out[f"H45-{lane}"] = rec; jdump(out, RUN / "probes_amend1.json"); print(json.dumps(rec, indent=1))
    if not rec["identifier_ok"]:
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if rec["status"] != "OK":
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def billed_h45():
    tot = {}
    for lane in ORDER:
        p = rows_h45(lane)
        tot[lane] = sum(json.loads(l).get("usd", 0.0) for l in io.open(p, encoding="utf-8")) if p.exists() else None
    pr = probes(); tot["probes"] = sum(v["usd"] for k, v in pr.items() if k.startswith("H45-"))
    return tot


def projection_h45(lane):
    pr = probes()[f"H45-{lane}"]; units = h45_units(lane)
    # every request of a lane shares its shell; input tokens scale with the prompt length, calibrated on the probe's unit
    ratio = pr["tok_in"] / max(1, len(units[0]["system"]) + len(units[0]["user"]))
    tin = sum(ratio * (len(u["system"]) + len(u["user"])) for u in units) * K
    tout = pr["tok_out"] * len(units) * K
    return {"requests": len(units) * K, "tok_in": int(tin), "tok_out": int(tout), "usd": (tin / 1e6 * PRICE_H45[0] + tout / 1e6 * PRICE_H45[1]) * MULT_H45}


def cmd_submit_h45(lane):
    assert_lineage()
    b = billed_h45(); earlier = [l for l in ORDER[:ORDER.index(lane)]]
    for l in earlier:
        assert b[l] is not None, f"lane {l} has not returned; the order is {ORDER} -- STOP"
    spent = sum(b[l] for l in earlier) + b["probes"]
    proj = projection_h45(lane); fits = spent + 1.3 * proj["usd"] <= CAP_H45
    rec = {"lane": lane, "projection": proj, "x1_3": 1.3 * proj["usd"], "billed_earlier": spent, "cap": CAP_H45, "fits": fits, "when": dt.datetime.now().isoformat(timespec="seconds")}
    pj = J(RUN / "projection_amend1.json") if (RUN / "projection_amend1.json").exists() else {}
    pj[lane] = rec; jdump(pj, RUN / "projection_amend1.json"); print(json.dumps(rec, indent=1))
    if not fits:
        print(f"LANE {lane} NOT SUBMITTED: x1.3 projection ${1.3 * proj['usd']:.4f} + billed ${spent:.4f} exceeds the ${CAP_H45:.2f} cap (registration section B)")
        rec["submitted"] = False; pj[lane] = rec; jdump(pj, RUN / "projection_amend1.json"); sys.exit(1)
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    units = h45_units(lane); reqs = []
    for i, u in enumerate(units):
        for d in range(1, K + 1):
            reqs.append(Request(custom_id=f"A1-{lane}-{i:04d}-d{d}",
                                params=MessageCreateParamsNonStreaming(model=LANE_H45, max_tokens=200, temperature=0.0, system=u["system"],
                                                                       messages=[{"role": "user", "content": u["user"]}])))
    bt = anthropic_client().messages.batches.create(requests=reqs)
    jdump({"id": bt.id, "lane": lane, "arm": ARM_OF[lane], "n": len(reqs), "submitted": dt.datetime.now().isoformat(timespec="seconds")}, RUN / f"batch_amend1_{lane}.json")
    print("submitted", bt.id, len(reqs), "requests")


def cmd_poll_h45(lane):
    meta = J(RUN / f"batch_amend1_{lane}.json"); cl = anthropic_client()
    bt = cl.messages.batches.retrieve(meta["id"]); print(meta["id"], bt.processing_status, bt.request_counts)
    if bt.processing_status != "ended":
        return
    units = h45_units(lane); n_ok = 0
    with io.open(rows_h45(lane), "w", encoding="utf-8", newline="\n") as f:
        for res in cl.messages.batches.results(meta["id"]):
            _, ln, i, d = res.custom_id.split("-"); u = units[int(i)]
            if res.result.type == "succeeded":
                m = res.result.message; text = "".join(bl.text for bl in m.content if bl.type == "text")
                row = make_row(u, ARM_OF[lane], LANE_H45, int(d[1:]), text, m.usage.input_tokens, m.usage.output_tokens, PRICE_H45, MULT_H45, m.model)
                n_ok += 1
            else:
                row = {"unit_id": u["unit_id"], "arm": ARM_OF[lane], "model": LANE_H45, "draw": int(d[1:]), "status": "BATCH_" + res.result.type.upper()}
            row.update({"persona": u["persona"], "state": u["state"], "y_nok": u["y_nok"], "y_fok": u["y_fok"], "tier": u["tier"]})
            f.write(json.dumps(row, sort_keys=True) + "\n")
    print("collected; ok:", n_ok, "of", meta["n"])


# ------------------------------------------------------------------ scoring
def collapse(path):
    """X4's collapse: dedup on draw, at least three OK draws, arithmetic mean of nok and fok per unit."""
    G = collections.defaultdict(dict)
    for l in io.open(path, encoding="utf-8"):
        r = json.loads(l)
        if r.get("status") == "OK":
            G[r["unit_id"]][r["draw"]] = r
    out = {}
    for uid, draws in G.items():
        if len(draws) >= 3:
            out[uid] = {"nok": float(np.mean([r["nok"] for r in draws.values()])), "fok": float(np.mean([r["fok"] for r in draws.values()])), "draws": len(draws)}
    return out


def h45_true():
    """Haiku 4.5's recorded INDEXED-TRUE row on the 661 (r74/x4/rows_H45.jsonl), collapsed as X4 does."""
    G = collections.defaultdict(dict)
    for l in io.open(ROOT / "r74" / "x4" / "rows_H45.jsonl", encoding="utf-8"):
        r = json.loads(l)
        if r.get("status") == "OK" and r["arm"] == "INDEXED-TRUE":
            G[r["item_id"]][r["draw"]] = r
    return {k: {"nok": float(np.mean([r["nok"] for r in v.values()])), "fok": float(np.mean([r["fok"] for r in v.values()]))} for k, v in G.items() if len(v) >= 3}


def paired_rows(sub, base_of, arm_of, keep):
    out = {}
    for st, name in [(None, "all")] + [(s, n) for s, n in STATES]:
        pop = [it for it in RR.subpop(sub, st) if keep(it)]
        out[name] = RR.paired([base_of(it) for it in pop], [arm_of(it) for it in pop], [it["y_nok"] for it in pop], [it["persona"] for it in pop])
    return out


def cmd_score():
    sys.stdout.reconfigure(encoding="utf-8")
    sub = RC.load_cell(); by = RR.load_rows()
    S = {"registration_sha256": REG_SHA, "lock": J(RUN / "lock_amend1.json")}
    # section A
    if ROWS_MINI.exists():
        rows = {json.loads(l)["item_id"]: json.loads(l) for l in io.open(ROWS_MINI, encoding="utf-8")}
        ok = lambda it: rows.get(it["item_id"], {}).get("status") == "OK" and by["RETRIEVED"].get(it["item_id"], {}).get("status") == "OK"
        A = {"n_rows": len(rows), "failures": sum(1 for r in rows.values() if r["status"] != "OK")}
        A["vs_retrieved_true_tags"] = paired_rows(sub, lambda it: by["RETRIEVED"][it["item_id"]]["nok"], lambda it: rows[it["item_id"]]["nok"], ok)
        A["vs_true_summary"] = paired_rows(sub, lambda it: it["true"]["nok"], lambda it: rows[it["item_id"]]["nok"], ok)
        hard = [it for it in sub if it["tier"] == "hard" and ok(it)]
        A["fok_307"] = {"believed": RR.auroc_ci([rows[it["item_id"]]["fok"] for it in hard], [it["y_fok"] for it in hard]),
                        "retrieved_true_tags": RR.auroc_ci([by["RETRIEVED"][it["item_id"]]["fok"] for it in hard], [it["y_fok"] for it in hard])}
        d = A["vs_retrieved_true_tags"]["all"]
        A["collapse"] = {"rule": "below the recorded RETRIEVED row by more than 0.05 with both intervals excluding zero",
                         "D": d["D"], "item_excludes": bool(d["item"].get("excludes_zero")), "cluster_excludes": bool(d["cluster"].get("excludes_zero")),
                         "collapsed": bool(d["D"] < -0.05 and d["item"].get("excludes_zero") and d["cluster"].get("excludes_zero"))}
        A["spend"] = sum(r.get("usd", 0.0) for r in rows.values()) + probes().get("MINI", {}).get("usd", 0.0)
        S["A"] = A
    # section B
    T = h45_true(); own = J(L1 / "indexes_own.json")["items"]
    B = {}
    for lane in ORDER:
        p = rows_h45(lane)
        if not p.exists():
            B[lane] = {"status": "not run"}; continue
        C = collapse(p); arm = ARM_OF[lane]
        if lane == "OWN":
            score = lambda it: (C[it["item_id"]]["nok"] if own[it["item_id"]]["changed"] else T[it["item_id"]]["nok"])
            keep = lambda it: it["item_id"] in T and ((not own[it["item_id"]]["changed"]) or it["item_id"] in C)
        else:
            score = lambda it: C[it["item_id"]]["nok"]
            keep = lambda it: it["item_id"] in T and it["item_id"] in C
        n_rows = sum(1 for _ in io.open(p, encoding="utf-8")); n_ok = sum(1 for l in io.open(p, encoding="utf-8") if json.loads(l).get("status") == "OK")
        L = {"arm": arm, "rows": n_rows, "ok": n_ok, "units_scored": len(C), "spend": sum(json.loads(l).get("usd", 0.0) for l in io.open(p, encoding="utf-8"))}
        L["vs_h45_true"] = paired_rows(sub, lambda it: T[it["item_id"]]["nok"], score, keep)
        if lane != "OWN":
            hard = [it for it in sub if it["tier"] == "hard" and keep(it)]
            L["fok_307"] = {"lane": RR.auroc_ci([C[it["item_id"]]["fok"] for it in hard], [it["y_fok"] for it in hard]),
                            "h45_true": RR.auroc_ci([T[it["item_id"]]["fok"] for it in hard], [it["y_fok"] for it in hard])}
        B[lane] = L
    S["B"] = B; S["billed_h45"] = billed_h45(); S["projection"] = J(RUN / "projection_amend1.json") if (RUN / "projection_amend1.json").exists() else {}
    S["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(S, RUN / "scores_amend1.json")
    txt = ledger_text(S)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


def fmt(d):
    return f"| {d['n']} / {d['n_pos']} | {d['base']:.4f} | {d['arm']:.4f} | {d['D']:+.4f} | {RR.fmt_i(d['item'])} | {RR.fmt_i(d['cluster'])} |"


def ledger_text(S):
    lk = S["lock"]; t = lk["tags"]; L = []
    L.append("\n### AUX-RESP-A1-LOCK, AUX-RESP-A1-TAGS — the believed blocks and the tag census (no call)\n\n")
    L.append(f"Registration sha256 holds; prompts_resp digests as AUX-RESP-L2-PROMPTS; prompts_e1 as pinned. The same `top5_ids` as `l2/retrieval.json`, re-rendered with FR-Bank's own marks "
             f"(`l2/retrieval_believed.json`). Of the {t['lines']} rendered lines, {t['lines_changed']} change tag between the join and the store's marks ({t['items_with_a_changed_line']} of 661 views change at least one line). "
             f"The store's non-active mark against the join's, over lines: tp {t['non_active_lines']['tp']}, fp {t['non_active_lines']['fp']}, fn {t['non_active_lines']['fn']}, tn {t['non_active_lines']['tn']}; "
             f"precision {t['non_active_lines']['precision']:.4f}, recall {t['non_active_lines']['recall']:.4f}. Over the forbidding records in view (the 104 obligations' pn_members among the five): "
             f"tp {t['forbidding_records_in_view']['tp']}, fp {t['forbidding_records_in_view']['fp']}, fn {t['forbidding_records_in_view']['fn']}, tn {t['forbidding_records_in_view']['tn']}"
             + (f"; precision {t['forbidding_records_in_view']['precision']:.4f}, recall {t['forbidding_records_in_view']['recall']:.4f}" if t['forbidding_records_in_view']['precision'] is not None else "") + ".\n")
    pr = probes()
    if "A" in S:
        A = S["A"]; m = pr["MINI"]
        L.append(f"\n### AUX-RESP-A1-PROBE, AUX-RESP-A1-BELIEVED — RETRIEVED-BELIEVED (gpt-4.1-mini, 661, k = 1)\n\n")
        L.append(f"Probe served `{m['served']}` ({m['tok_in']} in / {m['tok_out']} out). Rows {A['n_rows']}, failures {A['failures']}; billed ${A['spend']:.4f}. "
                 "Paired against the recorded RETRIEVED row (ground-truth tags) and against the committed INDEXED-TRUE row; item-level and persona-clustered paired bootstrap (1,000 draws, seed 42).\n\n")
        L.append("| row | n / positives | base | RETRIEVED-BELIEVED | D | item-level 95% | persona-clustered 95% |\n|---|---|---:|---:|---:|---|---|\n")
        for name in ("all", "supersession", "expiry", "retraction"):
            L.append(f"| vs RETRIEVED (join tags), {name} " + fmt(A["vs_retrieved_true_tags"][name]) + "\n")
        for name in ("all", "supersession", "expiry", "retraction"):
            L.append(f"| vs INDEXED-TRUE (summary), {name} " + fmt(A["vs_true_summary"][name]) + "\n")
        f1, f2 = A["fok_307"]["believed"], A["fok_307"]["retrieved_true_tags"]
        L.append(f"\nFOK on the 307 (descriptive): RETRIEVED-BELIEVED {f1['point']:.4f} [{f1['ci_lo']:.4f}, {f1['ci_hi']:.4f}] against RETRIEVED (join tags) {f2['point']:.4f}.\n")
        c = A["collapse"]
        L.append(f"\n**Collapse rule (section A):** D vs RETRIEVED {c['D']:+.4f}; item interval excludes zero: {c['item_excludes']}; persona interval excludes zero: {c['cluster_excludes']} → "
                 f"**{'COLLAPSED: the box\'s tag clause becomes conditional on tag accuracy' if c['collapsed'] else 'not collapsed: the tag clause stays unconditional'}**.\n")
    L.append("\n### AUX-RESP-A1-H45-HYBRID, -H45-RETRIEVED, -H45-OWN — Haiku 4.5 at k = 5 (Batch), against its recorded INDEXED-TRUE row on the 661\n\n")
    for lane in ORDER:
        Lx = S["B"][lane]; key = f"AUX-RESP-A1-H45-{lane}"
        if Lx.get("status") == "not run":
            pj = S["projection"].get(lane)
            L.append(f"**{key}**: — (not run" + (f": projection x1.3 ${pj['x1_3']:.4f} with ${pj['billed_earlier']:.4f} billed exceeds the $12 cap" if pj and not pj.get("fits", True) else "") + ").\n\n"); continue
        p = pr.get(f"H45-{lane}", {})
        L.append(f"**{key}** — arm {Lx['arm']}: probe served `{p.get('served')}` ({p.get('tok_in')} in / {p.get('tok_out')} out); Batch rows {Lx['rows']}, OK {Lx['ok']}, units scored {Lx['units_scored']} (at least three draws, mean); billed ${Lx['spend']:.4f}.\n\n")
        L.append("| row | n / positives | Haiku 4.5 INDEXED-TRUE (recorded) | arm | D | item-level 95% | persona-clustered 95% |\n|---|---|---:|---:|---:|---|---|\n")
        for name in ("all", "supersession", "expiry", "retraction"):
            L.append(f"| {name} " + fmt(Lx["vs_h45_true"][name]) + "\n")
        if "fok_307" in Lx:
            f1, f2 = Lx["fok_307"]["lane"], Lx["fok_307"]["h45_true"]
            L.append(f"\nFOK on the 307 (descriptive): {Lx['arm']} {f1['point']:.4f} [{f1['ci_lo']:.4f}, {f1['ci_hi']:.4f}] against the recorded TRUE row {f2['point']:.4f}.\n")
        L.append("\n")
    b = S["billed_h45"]
    L.append(f"### AUX-RESP-A1-SPEND\n\nHaiku 4.5 (Batch prices): " + "; ".join(f"{lane} ${b[lane]:.4f}" if b[lane] is not None else f"{lane} —" for lane in ORDER)
             + f"; probes ${b['probes']:.4f}; **total ${sum(v for v in b.values() if v is not None):.4f}** against the $12.00 cap. "
             + (f"GPT-4.1 mini (section A): ${S['A']['spend']:.4f}.\n" if "A" in S else "\n"))
    return "".join(L)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("probe-h45", "submit-h45", "poll-h45"):
        {"probe-h45": cmd_probe_h45, "submit-h45": cmd_submit_h45, "poll-h45": cmd_poll_h45}[cmd](sys.argv[2])
    else:
        {"lock": cmd_lock, "probe-mini": cmd_probe_mini, "run-mini": cmd_run_mini, "score": cmd_score}[cmd]()
