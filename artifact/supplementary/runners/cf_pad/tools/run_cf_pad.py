"""run_cf_pad.py -- ADDENDUM_CF_PAD (R136): the long-list check on the counterfactual set.

Phase 0 (read-only, $0):
  dryrun     build the 444 padded summaries (cf_pad_common), renderer lock, leak scan, list lengths, the target's
             position, one rendered triple in full; run the three lookups on the padded lists and DISCARD the scores
             (nothing printed, nothing stored); measure the prompt sizes (o200k) -> cf_pad/build/dryrun_*.json
  project    the cost projection per lane from the measured prompt sizes and the recorded lanes' output means,
             at the page prices below, x1.3 -> cf_pad/build/projection.json

After the GO (section 3 of the brief; each asserts the frozen registration's sha256 first):
  lock | lookups | probe <lane> | sync gpt-4.1-mini | run <openai model> | submit <anthropic lane> | poll <lane> | score | report

Prices (USD per million tokens). OpenAI: the model pages as ADDENDUM_CF2_OPENAI.md (2026-09-18) and ADDENDUM_R122_MINI_K5.md
(2026-09-19) record them. Anthropic: the model table read 2026-09-22 (Opus 5 $5 / $25, Haiku 4.5 $1 / $5), Batch at 50%.
"""
from __future__ import annotations

import collections
import io
import json
import statistics as st
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cf_pad_common as C  # noqa: E402
from cf_pad_common import BUILD, L, VERSIONS, jdump, jload  # noqa: E402

PRICES = {
    "gpt-4.1-mini": dict(vendor="openai", code="MINI", inp=0.40, cached=0.10, out=1.60, write_mult=1.0, k=5),
    "gpt-5.6-luna": dict(vendor="openai", code="LUNA", inp=0.20, cached=0.02, out=1.20, write_mult=1.25, k=5),
    "gpt-5.6-sol": dict(vendor="openai", code="SOL", inp=4.00, cached=0.40, out=20.00, write_mult=1.25, k=5),
    "claude-haiku-4-5-20251001": dict(vendor="anthropic", code="H45", inp=1.00, out=5.00, batch=0.5, k=5),
    "claude-opus-5": dict(vendor="anthropic", code="OP5", inp=5.00, out=25.00, batch=0.5, k=1),
}
RECORDED_ROWS = {"MINI": C.ROOT / "reviews" / "r122" / "rows" / "rows_MINI5.jsonl", "LUNA": C.CF2 / "rows" / "rows_LUNA.jsonl",
                 "SOL": C.CF2 / "rows" / "rows_SOL.jsonl", "H45": C.CF2 / "rows" / "rows_H45.jsonl", "OP5": C.CF2 / "rows" / "rows_OP5.jsonl"}
CAPS = {"anthropic": 12.00, "openai": 20.00}     # the author's ruling of 2026-09-22 (point 1): OpenAI $20, Sol at five draws
MARGIN = 1.3


def _messages(text, question):
    import prompts_e1 as P
    return P.SYSTEM, P.USER_INDEXED.format(index=text, question=question)


# ------------------------------------------------------------------ Phase 0
def cmd_dryrun():
    assert C.REG_SHA is None or C.registration_ok()
    pop = C.Pop()
    ok, bad = C.renderer_lock(pop)
    print(f"renderer lock on the committed v2 texts: {ok} of 444" + (f"  BAD {bad[:3]}" if bad else ""))
    if bad:
        raise SystemExit("STOP: renderer lock failed")
    pools = C.build_pools(pop)
    pads = C.build_pads(pop, pools)
    texts = C.render_all(pop, pads)
    lists = C.rendered_lists(texts, pop)
    fails, notes = C.leak_scan(pop, pools, pads, texts)
    # ---- the three lookups, run and discarded (no score printed or stored)
    sc = C.lookup_scores(pop, lists)
    for k, v in sc.items():
        assert v.shape == (444,) and np.isfinite(v).all(), k
    del sc
    # ---- census
    lens = [len(lists[r["key"]]) for r in pop.rows]
    by_vs = collections.defaultdict(list)
    for r in pop.rows:
        by_vs[(r["state"], r["version"])].append(len(lists[r["key"]]))
    pos = C.target_positions(pop, pads)
    pc = collections.Counter(pos.values())
    ex = C.persona_targets(pop)
    census = {
        "n_rows": 444, "n_pairs": 148, "renderer_lock": ok,
        "list_length": {"min": min(lens), "median": st.median(lens), "max": max(lens), "mean": st.mean(lens),
                        "by_state_version": {f"{s}|{v}": {"min": min(x), "median": st.median(x), "max": max(x), "n": len(x)} for (s, v), x in sorted(by_vs.items())},
                        "histogram": dict(sorted(collections.Counter(lens).items()))},
        "n_pad": dict(sorted(collections.Counter(R["n_pad"] for R in pads.values()).items())),
        "from_pool_b_pairs": sum(1 for R in pads.values() if R["from_pool_b"] > 0),
        "pool_a": {"min": min(P["census"]["pool_a"] for P in pools.values()), "median": st.median([P["census"]["pool_a"] for P in pools.values()]),
                   "max": max(P["census"]["pool_a"] for P in pools.values())},
        "pool_b": {"min": min(P["census"]["pool_b"] for P in pools.values()), "median": st.median([P["census"]["pool_b"] for P in pools.values()]),
                   "max": max(P["census"]["pool_b"] for P in pools.values())},
        "map_symdiff": dict(sorted(collections.Counter(P["census"]["map_symdiff"] for P in pools.values()).items())),
        "change_set": dict(sorted(collections.Counter(P["census"]["change_set"] for P in pools.values()).items())),
        "excluded_by_ii": {"from_intersection_total": sum(P["census"]["excluded_by_ii_from_intersection"] for P in pools.values()),
                           "cf2_only_total": sum(P["census"]["excluded_by_ii_cf2_only"] for P in pools.values()),
                           "e1_only_total": sum(P["census"]["excluded_by_ii_e1_only"] for P in pools.values())},
        "persona_targets": {p: {"cf2_targets": len(d["cf2_targets"]), "cf2_pn_slots": len(d["cf2_pn_slots"]), "e1_wide": len(d["e1_wide"]), "all": len(d["all"])} for p, d in sorted(ex.items())},
        "target_position_pn_supersession": {"n": len(pos), "histogram": {str(k): pc[k] for k in sorted(pc)},
                                            "min": min(pos.values()), "median": st.median(pos.values()), "max": max(pos.values()), "mean": st.mean(pos.values()),
                                            "first": pc.get(1, 0), "last": pc.get(L, 0),
                                            "deciles": {str(d): sum(1 for v in pos.values() if (d - 1) * 6 < v <= d * 6) for d in range(1, 11)}},
        "leak_scan": {"fails": fails, "n_fails": len(fails), "descriptive": notes},
        "texts_sha256": C.texts_sha256(texts), "indexes_sha256": pop.idx_sha,
    }
    # ---- prompt sizes (o200k), padded and committed, per item
    import tiktoken
    enc = tiktoken.get_encoding("o200k_base")
    sizes = {}
    for r in pop.rows:
        s0, u0 = _messages(pop.text[r["key"]], r["question"])
        s1, u1 = _messages(texts[r["key"]], r["question"])
        sizes[r["key"]] = {"committed": len(enc.encode(s0)) + len(enc.encode(u0)), "padded": len(enc.encode(s1)) + len(enc.encode(u1))}
    a = np.array([v["committed"] for v in sizes.values()]); b = np.array([v["padded"] for v in sizes.values()])
    census["prompt_tokens_o200k"] = {"committed_mean": float(a.mean()), "padded_mean": float(b.mean()), "padded_max": int(b.max()),
                                     "ratio_mean": float((b / a).mean()), "extra_mean": float((b - a).mean())}
    jdump({"census": census, "pools": {pid: {k: v for k, v in P.items()} for pid, P in pools.items()},
           "pads": {pid: {"pad": R["pad"], "n_pad": R["n_pad"], "from_pool_a": R["from_pool_a"], "from_pool_b": R["from_pool_b"], "len": R["len"]} for pid, R in pads.items()},
           "lists": lists, "target_position": pos, "prompt_sizes": sizes}, BUILD / "dryrun_build.json")
    jdump(texts, BUILD / "dryrun_texts.json")
    # ---- print
    print(json.dumps({k: census[k] for k in ("list_length", "n_pad", "from_pool_b_pairs", "pool_a", "pool_b", "map_symdiff", "change_set", "excluded_by_ii",
                                              "target_position_pn_supersession", "leak_scan", "prompt_tokens_o200k", "texts_sha256")}, indent=1))
    # one rendered triple in full: the first supersession pair in sorted order
    pid = next(p for p in pop.pairs if pop.state(p) == "superseded")
    print(f"\n===== one rendered triple: {pid}  target {pop.target(pid)}  pad {pads[pid]['n_pad']} names (draw order below; the section prints them sorted)")
    print("pad (draw order):", pads[pid]["pad"])
    for v in VERSIONS:
        key = pop.by_pair[pid][v]["key"]
        print("=" * 110); print(f"{key}   y_nok {pop.by_pair[pid][v]['y']}   list length {len(lists[key])}"); print("-" * 110)
        print(texts[key])
    print(f"\nwrote {BUILD / 'dryrun_build.json'}, {BUILD / 'dryrun_texts.json'}  (no score stored)")
    if fails:
        raise SystemExit(f"LEAK SCAN FAILED: {len(fails)} findings")


def _recorded_stats(code):
    rows = [json.loads(l) for l in io.open(RECORDED_ROWS[code], encoding="utf-8") if l.strip()]
    rows = [r for r in rows if r.get("arm") == "INDEXED-V2" and r.get("status") == "OK"]
    tin = {}
    for r in rows:
        tin.setdefault(r["unit_id"], []).append(r["tok_in"])
    return {"n_rows": len(rows), "tok_in_mean": st.mean(r["tok_in"] for r in rows), "tok_out_mean": st.mean(r["tok_out"] for r in rows),
            "tok_out_p95": sorted(r["tok_out"] for r in rows)[int(0.95 * len(rows))], "usd": sum(r.get("usd", 0.0) for r in rows),
            "tok_in_by_unit": {u: st.mean(v) for u, v in tin.items()}}


def _anchored(code, P, sizes, k_new):
    """The recorded lane's own rows (arm INDEXED-V2), each row's prompt-side tokens scaled by its item's padded/committed o200k
    ratio, its completion tokens kept, priced at the page prices (OpenAI: plain input, cache writes at write_mult, cached reads
    at the cached rate, output; Anthropic: input and output at Batch); the per-draw mean times k_new."""
    rows = [json.loads(l) for l in io.open(RECORDED_ROWS[code], encoding="utf-8") if l.strip()]
    rows = [r for r in rows if r.get("arm") == "INDEXED-V2" and r.get("status") == "OK"]
    by_draw = collections.defaultdict(float)
    for r in rows:
        ratio = sizes[r["unit_id"]]["padded"] / sizes[r["unit_id"]]["committed"]
        if P["vendor"] == "openai":
            u = r.get("usage") or {}
            pt = u.get("prompt_tokens", r["tok_in"]) * ratio; ct = u.get("completion_tokens", r["tok_out"])
            det = u.get("prompt_tokens_details") or {}
            cached = (det.get("cached_tokens", 0) or 0) * ratio; write = (det.get("cache_write_tokens", 0) or 0) * ratio
            plain = max(0.0, pt - cached - write)
            usd = (plain * P["inp"] + write * P["inp"] * P["write_mult"] + cached * P["cached"] + ct * P["out"]) / 1e6
        else:
            usd = (r["tok_in"] * ratio * P["inp"] + r["tok_out"] * P["out"]) / 1e6 * P["batch"]
        by_draw[int(r["draw"])] += usd
    draws = sorted(by_draw)
    per_draw = {d: round(by_draw[d], 4) for d in draws}
    if P["vendor"] == "openai":
        # draw 1 uncached, later draws cached: keep the recorded draw structure (draw 1 as recorded draw 1, draws 2..k as the mean of the recorded later draws)
        first = by_draw[draws[0]]; later = st.mean(by_draw[d] for d in draws[1:]) if len(draws) > 1 else first
        usd = first + (k_new - 1) * later
        usd3 = first + 2 * later
    else:
        mean = st.mean(by_draw.values()); usd = k_new * mean; usd3 = 3 * mean
    return {"per_draw_recorded_scaled": per_draw, "usd_anchored": usd, "usd_anchored_x1.3": usd * MARGIN, "usd_anchored_3_draws": usd3 if k_new > 1 else None}


def cmd_project():
    B = jload(BUILD / "dryrun_build.json")
    sizes = B["prompt_sizes"]
    out, totals = {}, collections.Counter()
    for lane, P in PRICES.items():
        rec = _recorded_stats(P["code"])
        # the padded prompt per item: the recorded lane's own input tokens (that vendor's tokenizer) scaled by the item's o200k ratio
        per_item = [rec["tok_in_by_unit"].get(k, rec["tok_in_mean"]) * sizes[k]["padded"] / sizes[k]["committed"] for k in sizes]
        tin_draw = float(sum(per_item)); n_units = len(per_item)
        out_tok = rec["tok_out_mean"]; k = P["k"]
        if P["vendor"] == "openai":
            first = tin_draw * P["inp"] / 1e6
            cached = tin_draw * P["cached"] / 1e6
            outc = n_units * out_tok * P["out"] / 1e6
            usd_cache = first + (k - 1) * cached + k * outc          # draws 2..k at the cached input rate (the recorded lanes' pattern, 99.8% cached)
            usd_nocache = k * first + k * outc
            rec_row = {"usd_expected": usd_cache, "usd_no_cache": usd_nocache, "usd_x1.3": usd_cache * MARGIN, "usd_no_cache_x1.3": usd_nocache * MARGIN,
                       "usd_expected_3_draws": first + 2 * cached + 3 * outc, "usd_expected_3_draws_x1.3": (first + 2 * cached + 3 * outc) * MARGIN}
        else:
            usd = k * (tin_draw * P["inp"] + n_units * out_tok * P["out"]) / 1e6 * P["batch"]
            rec_row = {"usd_expected": usd, "usd_x1.3": usd * MARGIN,
                       "usd_expected_3_draws": 3 * (tin_draw * P["inp"] + n_units * out_tok * P["out"]) / 1e6 * P["batch"] if k > 1 else None}
        anc = _anchored(P["code"], P, sizes, k)
        planning = max(rec_row["usd_expected"], anc["usd_anchored"])
        out[lane] = {"vendor": P["vendor"], "k": k, "calls": k * n_units, "prompt_tokens_per_draw": tin_draw, "prompt_tokens_mean": tin_draw / n_units,
                     "recorded": {kk: v for kk, v in rec.items() if kk != "tok_in_by_unit"}, "prices": {kk: v for kk, v in P.items() if kk not in ("vendor", "code", "k")},
                     **rec_row, **anc, "usd_planning": planning, "usd_planning_x1.3": planning * MARGIN}
        totals[P["vendor"]] += planning; totals[P["vendor"] + "_x1.3"] += planning * MARGIN
        totals[P["vendor"] + "_formula"] += rec_row["usd_expected"]; totals[P["vendor"] + "_anchored"] += anc["usd_anchored"]
    res = {"lanes": out, "totals": dict(totals), "caps": CAPS, "margin": MARGIN,
           "planning_rule": "per lane the larger of the formula projection and the recorded-rows-scaled (anchored) projection; the vendor total of those, x1.3, against the cap",
           "fits_x1.3": {v: totals[v + "_x1.3"] <= CAPS[v] for v in CAPS}, "fits_planning": {v: totals[v] <= CAPS[v] for v in CAPS}}
    jdump(res, BUILD / "projection.json")
    print(f"{'lane':28s} {'k':>2s} {'calls':>6s} {'prompt/call':>11s} {'out/call':>8s} {'formula':>8s} {'anchored':>9s} {'planning':>9s} {'x1.3':>8s} {'no-cache':>9s} {'3 draws':>8s}")
    for lane, r in out.items():
        print(f"{lane:28s} {r['k']:2d} {r['calls']:6d} {r['prompt_tokens_mean']:11.0f} {r['recorded']['tok_out_mean']:8.1f} {r['usd_expected']:8.2f} {r['usd_anchored']:9.2f} "
              f"{r['usd_planning']:9.2f} {r['usd_planning_x1.3']:8.2f} {r.get('usd_no_cache', float('nan')):9.2f} {(r.get('usd_anchored_3_draws') or float('nan')):8.2f}")
    for v in CAPS:
        print(f"{v:10s} formula ${totals[v + '_formula']:.2f}  anchored ${totals[v + '_anchored']:.2f}  planning ${totals[v]:.2f}  x1.3 ${totals[v + '_x1.3']:.2f}  "
              f"cap ${CAPS[v]:.2f}  fits (x1.3) {res['fits_x1.3'][v]}  fits (planning) {res['fits_planning'][v]}")
    print(f"wrote {BUILD / 'projection.json'}")




# ====================================================================== after the GO (the registration frozen at 06c611f)
import datetime as dt  # noqa: E402
import threading  # noqa: E402
import time  # noqa: E402
import concurrent.futures as cf  # noqa: E402

import run_cf as RC  # noqa: E402  (asserts the prompts_e1 digests at import)
import cf2_openai as OAI  # noqa: E402  (E5's price() and call_once: raw Chat Completions, max_completion_tokens 2048, nothing else set)

ARM = C.ARM
LOCK = BUILD / "lock.json"
PROBES = BUILD / "probes.json"
TEXTS = BUILD / "texts.json"
ROWS = C.ROWS
WORKERS = 8
LANE_CODE = {"gpt-4.1-mini": "MINI", "gpt-5.6-luna": "LUNA", "gpt-5.6-sol": "SOL", "claude-haiku-4-5-20251001": "H45", "claude-opus-5": "OP5"}
VENDOR = {"gpt-4.1-mini": "openai", "gpt-5.6-luna": "openai", "gpt-5.6-sol": "openai", "claude-haiku-4-5-20251001": "anthropic", "claude-opus-5": "anthropic"}
OAI.MODELS.update({"gpt-4.1-mini": dict(code="MINI", inp=0.40, cached=0.10, out=1.60, write_mult=1.0)})   # E5's price() reads MODELS[model]; extended in memory only

# re-point run_cf (the recorded Anthropic lanes' code path) at this run: rows here, one arm, Opus at one draw
RC.ROWS = ROWS
RC.PROBES = PROBES
RC.ARMS = (ARM,)
RC.LANES["claude-opus-5"]["k"] = 1


def require_frozen():
    assert C.registration_ok(), "STOP: registration sha256 mismatch"
    assert C.REG_SHA == "a84dac1abc2f604b171b4ab838daba4bbdb440d124ef9f050387bd0a716eba21"


def identifier_ok(lane, served):
    if VENDOR[lane] == "openai" and lane != "gpt-4.1-mini":
        return lane in (served or "")
    return (lane.split("-2025")[0] in (served or "")) or (lane in (served or ""))


_UNITS = {}


def units(arm=ARM):
    """One unit per item, in the cell's order: the padded v2 text in place of the summary, the recorded question."""
    if "u" not in _UNITS:
        T = jload(TEXTS)
        pop = C.Pop()
        _UNITS["u"] = [{"unit_id": r["key"], "question": r["question"], "index": T[r["key"]]} for r in pop.rows]
    return _UNITS["u"]


RC.units = units


# ------------------------------------------------------------------ lock
def cmd_lock():
    require_frozen()
    pop = C.Pop()
    ok, bad = C.renderer_lock(pop)
    if bad:
        raise SystemExit(f"STOP: renderer lock failed on {len(bad)} items")
    L0 = jload(C.CF2 / "cf_indexes.json")
    import hashlib
    ih = hashlib.sha256("\x1f".join(L0["indexes"][k]["v2"] + "\x1e" + L0["indexes"][k]["v3"] for k in sorted(L0["indexes"])).encode()).hexdigest()
    cell_meta = jload(C.CF2 / "cf_cell.json")["meta"]["indexes_sha256"]
    if not (ih == L0["meta"]["sha256"] == cell_meta):
        raise SystemExit("STOP: the indexes' content hash differs from cf_indexes.json meta.sha256 / cf_cell.json meta.indexes_sha256")
    pools = C.build_pools(pop); pads = C.build_pads(pop, pools); texts = C.render_all(pop, pads)
    lists = C.rendered_lists(texts, pop)
    fails, notes = C.leak_scan(pop, pools, pads, texts)
    if fails:
        raise SystemExit(f"STOP: leak scan failed: {fails[:5]}")
    tsha = C.texts_sha256(texts)
    D = jload(BUILD / "dryrun_build.json")["census"]
    assert tsha == D["texts_sha256"], "the padded texts differ from the dry run's"
    # gates: the three lookups on the COMMITTED lists, and the recorded vectors
    committed = {r["key"]: C.committed_names(pop.text[r["key"]]) for r in pop.rows}
    sc = C.lookup_scores(pop, committed)
    got = {k: round(float(C.auroc(v, pop.y)), 4) for k, v in sc.items()}
    want = {"emb": C.RECORDED["LOOKUP_v2"], "lex": C.LEX_V2, "randtok": C.RECORDED["RANDTOK_v2"]}
    if any(got[k] != want[k] for k in want):
        raise SystemExit(f"STOP: lookup gate failed: {got} vs {want}")
    rv = C.recorded_vectors()
    gates = {}
    for k, g in C.RECORDED.items():
        v = np.array([rv[k][r["key"]] for r in pop.rows], float)
        gates[k] = round(float(C.auroc(v, pop.y)), 4)
        if gates[k] != g:
            raise SystemExit(f"STOP: recorded gate {k}: {gates[k]} vs {g}")
    # the unpadded supersession-slice pooled and matched values of every recorded reader (section 2)
    import score_cf_pad as SCP
    cell = SCP.cell_for(pop)
    unpadded = {}
    for k in list(C.RECORDED) + ["LEX_v2"]:
        v = sc["lex"] if k == "LEX_v2" else np.array([rv[k][r["key"]] for r in pop.rows], float)
        m = C.state_mask(pop.rows, "superseded")
        unpadded[k] = {"pooled_whole": round(float(C.auroc(v, pop.y)), 4), "pooled_superseded": round(float(C.auroc(v[m], pop.y[m])), 4),
                       "matched_whole": SCP.matched(cell, v, "PRESENT", None)["matched"], "matched_superseded": SCP.matched(cell, v, "PRESENT", "SUPERSESSION")["matched"]}
    ex = C.persona_targets(pop)
    lock = {"registration": str(C.REG.relative_to(C.ROOT)), "registration_sha256": C.REG_SHA, "frozen_commit": "06c611f", "when": dt.datetime.now().isoformat(timespec="seconds"),
            "prompts_file_sha256": RC.P.file_sha256(), "prompts_texts_sha256": RC.P.texts_sha256(), "indexes_sha256": ih, "texts_sha256": tsha,
            "renderer_lock": ok, "leak_scan": {"fails": 0, "descriptive": notes}, "lookup_gate": {"got": got, "want": want},
            "recorded_gates": gates, "unpadded_recorded": unpadded, "n_pairs": 148, "n_rows": 444,
            "pools": {"a_min": min(P["census"]["pool_a"] for P in pools.values()), "a_median": float(np.median([P["census"]["pool_a"] for P in pools.values()])),
                      "a_max": max(P["census"]["pool_a"] for P in pools.values()), "from_pool_b_pairs": sum(1 for R in pads.values() if R["from_pool_b"] > 0)},
            "list_length": D["list_length"], "n_pad": D["n_pad"], "target_position": D["target_position_pn_supersession"],
            "persona_targets": {p: {k: len(v) for k, v in d.items()} for p, d in sorted(ex.items())},
            "arm": ARM, "lanes": {lane: {"code": LANE_CODE[lane], "k": (1 if lane == "claude-opus-5" else 5), "vendor": VENDOR[lane]} for lane in LANE_CODE},
            "caps": CAPS, "prices": {k: {kk: v for kk, v in p.items() if kk not in ("vendor", "code", "k")} for k, p in PRICES.items()}}
    jdump(lock, LOCK)
    jdump(texts, TEXTS)
    jdump(lists, BUILD / "lists.json")
    jdump({"pads": {pid: {"pad": R["pad"], "n_pad": R["n_pad"], "len": R["len"]} for pid, R in pads.items()},
           "pools": {pid: {k: v for k, v in P.items() if k != "pool_b"} | {"pool_b_size": len(P["pool_b"])} for pid, P in pools.items()},
           "target_position": C.target_positions(pop, pads)}, BUILD / "pads.json")
    print(json.dumps({k: lock[k] for k in ("registration_sha256", "indexes_sha256", "texts_sha256", "renderer_lock", "lookup_gate", "recorded_gates", "unpadded_recorded", "pools")}, indent=1))
    print(f"wrote {LOCK}")


# ------------------------------------------------------------------ the lookups on the padded lists ($0; vectors only, no AUROC until score)
def cmd_lookups():
    require_frozen(); assert LOCK.exists(), "STOP: lock first"
    pop = C.Pop()
    lists = jload(BUILD / "lists.json")
    sc = C.lookup_scores(pop, lists)
    committed = {r["key"]: C.committed_names(pop.text[r["key"]]) for r in pop.rows}
    sc0 = C.lookup_scores(pop, committed)
    jdump({"registration_sha256": C.REG_SHA, "arm": ARM, "keys": [r["key"] for r in pop.rows],
           "padded": {k: v.tolist() for k, v in sc.items()}, "committed": {k: v.tolist() for k, v in sc0.items()}}, C.RES / "lookup_vectors.json")
    print(f"wrote {C.RES / 'lookup_vectors.json'} (vectors only; no AUROC computed)")


# ------------------------------------------------------------------ spend
def spent(vendor):
    total, parts = 0.0, {}
    for lane, code in LANE_CODE.items():
        if VENDOR[lane] != vendor:
            continue
        p = ROWS / f"rows_{code}.jsonl"
        if p.exists():
            v = sum(json.loads(l).get("usd", 0.0) for l in io.open(p, encoding="utf-8") if l.strip()); parts[f"{code} rows"] = round(v, 4); total += v
    if PROBES.exists():
        for lane, rec in jload(PROBES).items():
            if VENDOR.get(lane) == vendor:
                parts[f"{LANE_CODE[lane]} probe"] = round(rec["usd"], 6); total += rec["usd"]
    return total, parts


# ------------------------------------------------------------------ calls
def call_mini(u, draw):
    """The five-draw row's call shape (reviews/r122/tools/oai_run.py MINI5): max_tokens 200, temperature unset, Chat Completions."""
    from openai import OpenAI
    sysm, user = RC.prompts_for(u, ARM)
    cl = OpenAI(max_retries=2, timeout=120)
    r = cl.chat.completions.create(model="gpt-4.1-mini", max_tokens=200, messages=[{"role": "system", "content": sysm}, {"role": "user", "content": user}])
    raw = r.model_dump(mode="json"); usage = raw.get("usage") or {}
    usd, cached, write, reasoning = OAI.price("gpt-4.1-mini", usage)
    row = RC.make_row(u, ARM, "gpt-4.1-mini", draw, r.choices[0].message.content, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0), (0.40, 1.60), 1.0, r.model)
    row.update({"usd": usd, "tok_cached": cached, "tok_cache_write": write, "tok_reasoning": reasoning, "finish_reason": r.choices[0].finish_reason,
                "usage": usage, "temperature": None, "when": dt.datetime.now().isoformat(timespec="seconds")})
    return row


def call_raw(model, u, draw):
    """Luna / Sol: cf2_openai.call_once (E5's settings), the arm relabelled."""
    row = OAI.call_once(model, u, draw)
    row["arm"] = ARM
    return row


def call_anthropic_once(lane, u, draw):
    return RC.call_once(lane, u, ARM, draw)      # synchronous, list price (probes only)


def cmd_probe(lane):
    require_frozen(); assert LOCK.exists()
    RC.load_env()
    u = units()[0]
    if lane == "gpt-4.1-mini":
        row = call_mini(u, 0)
    elif VENDOR[lane] == "openai":
        row = call_raw(lane, u, 0)
    else:
        row = call_anthropic_once(lane, u, 0)
    ok = identifier_ok(lane, row.get("served_model"))
    rec = {"lane": lane, "served": row.get("served_model"), "identifier_ok": ok, "tok_in": row.get("tok_in"), "tok_out": row.get("tok_out"),
           "tok_reasoning": row.get("tok_reasoning", 0), "usd": row.get("usd", 0.0), "status": row.get("status"), "nok": row.get("nok"), "fok": row.get("fok"),
           "sample": (row.get("text") or "")[:200], "when": dt.datetime.now().isoformat(timespec="seconds")}
    d = jload(PROBES) if PROBES.exists() else {}
    d[lane] = rec
    jdump(d, PROBES)
    print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: this lane does not launch")


def anthropic_projection():
    """At submission: k x 444 x the probe's tokens at Batch prices, both Anthropic lanes, plus the probes' spend, against the cap."""
    pr = jload(PROBES); total = 0.0; parts = {}
    for lane in ("claude-haiku-4-5-20251001", "claude-opus-5"):
        cfg = RC.LANES[lane]; p = pr[lane]
        v = cfg["k"] * 444 * (p["tok_in"] * cfg["price"][0] + p["tok_out"] * cfg["price"][1]) / 1e6 * cfg["mult"]
        parts[lane] = round(v, 4); total += v
    s, sp = spent("anthropic")
    return {"projection": parts, "projection_total": round(total, 4), "spent": round(s, 4), "spent_parts": sp, "cap": CAPS["anthropic"], "fits": total + s <= CAPS["anthropic"]}


def cmd_submit(lane):
    require_frozen(); assert PROBES.exists() and jload(PROBES)[lane]["identifier_ok"], "STOP: probe this lane first"
    proj = anthropic_projection()
    print(json.dumps(proj, indent=1))
    if not proj["fits"]:
        raise SystemExit("STOP: the Anthropic projection at submission exceeds the cap")
    RC.cmd_submit(lane)


def cmd_poll(lane):
    require_frozen()
    RC.cmd_poll(lane)


def run_openai(lane, draws):
    """Draw-major over the 444 units, eight workers, the OpenAI cap metered across the three lanes before every call; resume on (unit_id, draw)."""
    require_frozen(); RC.load_env()
    pr = jload(PROBES)[lane]; assert pr["identifier_ok"], "STOP: identifier"
    code = LANE_CODE[lane]; path = ROWS / f"rows_{code}.jsonl"; ROWS.mkdir(parents=True, exist_ok=True)
    done = set()
    if path.exists():
        for l in io.open(path, encoding="utf-8"):
            if l.strip():
                r = json.loads(l); done.add((r["unit_id"], int(r["draw"])))
    U = units()
    lock = threading.Lock()
    state = {"spent": spent("openai")[0], "n": 0, "halted": False}
    print(f"{lane}: OpenAI spent so far ${state['spent']:.4f} of ${CAPS['openai']:.2f}; {len(done)} rows already", flush=True)

    def work(job):
        u, d = job
        if state["halted"]:
            return None
        with lock:
            if state["spent"] >= CAPS["openai"]:
                state["halted"] = True; return None
        row = None
        for attempt in (1, 2, 3):
            try:
                row = call_mini(u, d) if lane == "gpt-4.1-mini" else call_raw(lane, u, d); break
            except Exception as e:  # noqa: BLE001
                if attempt == 3:
                    row = {"unit_id": u["unit_id"], "arm": ARM, "model": lane, "draw": d, "status": f"ERROR:{type(e).__name__}", "when": dt.datetime.now().isoformat(timespec="seconds")}
                else:
                    time.sleep(5 * attempt)
        with lock:
            state["spent"] += row.get("usd", 0.0); state["n"] += 1
            with io.open(path, "a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(row, sort_keys=True) + "\n")
            if state["n"] % 111 == 0:
                print(f"  {lane} draw {d}: {state['n']} calls this run; OpenAI ${state['spent']:.4f}", flush=True)
        return row

    for d in draws:
        jobs = [(u, d) for u in U if (u["unit_id"], d) not in done]
        if not jobs:
            print(f"{lane} draw {d}: complete already", flush=True); continue
        t0 = time.time()
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
            list(ex.map(work, jobs))
        n_ok = sum(1 for l in io.open(path, encoding="utf-8") if l.strip() and json.loads(l).get("status") == "OK" and int(json.loads(l)["draw"]) == d)
        print(f"{lane} draw {d} done in {time.time() - t0:.0f}s: OK rows {n_ok}/444; OpenAI ${state['spent']:.4f}", flush=True)
        if state["halted"]:
            print(f"{lane}: CAP REACHED during draw {d}; stopping (whole draws scored, the partial draw discarded and disclosed)", flush=True)
            break
    print(f"{lane} DONE; OpenAI spend ${spent('openai')[0]:.4f} of ${CAPS['openai']:.2f}", flush=True)


def cmd_spend():
    for v in ("anthropic", "openai"):
        s, parts = spent(v)
        print(f"{v}: ${s:.4f} of ${CAPS[v]:.2f}  {parts}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1]
    if cmd == "dryrun":
        cmd_dryrun()
    elif cmd == "project":
        cmd_project()
    elif cmd == "lock":
        cmd_lock()
    elif cmd == "lookups":
        cmd_lookups()
    elif cmd == "probe":
        cmd_probe(sys.argv[2])
    elif cmd == "submit":
        cmd_submit(sys.argv[2])
    elif cmd == "poll":
        cmd_poll(sys.argv[2])
    elif cmd in ("sync", "run"):
        draws = [int(x) for x in sys.argv[sys.argv.index("--draws") + 1].split(",")] if "--draws" in sys.argv else list(range(1, 6))
        run_openai(sys.argv[2], draws)
    elif cmd == "spend":
        cmd_spend()
    else:
        raise SystemExit(f"unknown subcommand {cmd}")
