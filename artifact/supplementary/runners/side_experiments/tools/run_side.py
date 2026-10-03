"""run_side.py -- SIDE-BUILD-1 step 5: the S1 and S2-U mini lanes (ADDENDUM_SIDE.md, frozen e8b2630;
sections S1, S2, T, B). MODEL CALLS: gpt-4.1-mini only -- S1 INDEXED-GT on A-MEM (284) and Mem0
(238), S2-U on the 661 -- plus one served-identifier probe per arm. No Haiku, no Opus. The blind,
INDEXED-TRUE and INDEXED-BELIEVED arms are the committed rows of e1_metamemory/elicitation_main.json,
read and never re-elicited.

Protocol: the E1 protocol of elicit_e1.py -- api.call (gpt-4.1-mini, temperature 0, seed 42,
max_tokens 200, JSON mode), prompts_e1.SYSTEM + USER_INDEXED with both digests asserted, the E1
clamp (0-100 -> [0,1]), one retry on a parse failure, status ELICITATION_FAILED otherwise; k = 1;
synchronous chat completions, 8 workers; responses cached under side_experiments/cache/.
Only the index text differs from the committed INDEXED-TRUE / INDEXED-BELIEVED calls:
  INDEXED-GT   side_experiments/s1/indexes_gt.json  (Mem0 lexical-required; A-MEM two-channel)
  INDEXED-S2U  side_experiments/s2/indexes_s2u.json (BELIEVED with SLOT_CAP lifted)

Subcommands, in order:  build | probe | project | run | score
  build    the populations, asserted (238 / 94; 284 / 126; 661 / 104), every index key present
  probe    one call per arm through the same client: served identifier (E1.7 rule), tokens
  project  probe tokens x calls against the $2 line (section B), net of what is already billed
  run      the calls; stops submitting at the $2 line
  score    section T: common_e1r.auroc / boot_item / boot_cluster; the registered verdicts on
           A-MEM (S1-P1, S1-P2), the Mem0 descriptive row, the S2-U descriptive row and retention,
           the spend; frozen texts printed with their numbers; scores_side.json
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import hashlib
import io
import json
import subprocess
import sys
import threading

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import side_common as SC                                         # noqa: E402
from side_common import ROOT, E1, J, jdump                       # noqa: E402
import api                                                       # noqa: E402
import prompts_e1 as P                                           # noqa: E402
from common_e1r import POPULATIONS, auroc, boot_item, boot_cluster, load_e1, N_BOOT, SEED   # noqa: E402

RUN = SC.SIDE / "run"
CACHE = SC.SIDE / "cache"
FREEZE = "e8b2630"
LANE, PRICE = "gpt-4.1-mini", (0.40, 1.60)
BUDGET = 2.00
PIN_PROMPTS = {"file": "337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84",
               "texts": "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"}
ARMS = {"INDEXED-GT": ("s1", "mem0", "amem"), "INDEXED-S2U": ("s2u",)}
ROWS_P = RUN / "rows_side.jsonl"
TOL = 0.05


def clamp(v):
    """elicit_e1.clamp, verbatim: 0-100 -> [0, 1]."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return min(100.0, max(0.0, f)) / 100.0


def assert_lineage():
    assert P.file_sha256() == PIN_PROMPTS["file"], "prompts_e1 file digest drift -- STOP"
    assert P.texts_sha256() == PIN_PROMPTS["texts"], "prompts_e1 texts digest drift -- STOP"
    assert (P.MODEL, P.TEMPERATURE, P.SEED, P.MAX_TOKENS) == (LANE, 0, 42, 200), "lane drift -- STOP"
    assert api.__file__.replace("\\", "/").endswith("e1_metamemory/tools/api.py")


def redirect_cache():
    CACHE.mkdir(parents=True, exist_ok=True)
    e0 = api._e0                                                 # noqa: SLF001
    e0.CACHE_PATH = CACHE / "responses.json"; e0.LEDGER_PATH = CACHE / "cost_ledger.json"
    e0._cache = None; e0._load_cache()                           # noqa: SLF001
    return e0


# ------------------------------------------------------------------ build
def build_cell():
    """The populations, joined exactly as common_e1r.assemble joins them; only committed rows enter."""
    items, blind, idxT, idxB = load_e1()
    gt = J(SC.S1 / "indexes_gt.json")["indexes"]; s2 = J(SC.SIDE / "s2" / "indexes_s2u.json")
    s2u, s2map = s2["indexes"], {r["item_id"]: r["index_key_s2u"] for r in s2["items"]}
    cell = {"s1": {}, "s2u": []}
    for b, (rid, n, npos) in (("mem0", ("R-FOK-MEM0", 238, 94)), ("amem", ("R-FOK-AMEM", 284, 126))):
        rows = []
        for it in items:
            if not POPULATIONS[rid]["filt"](it) or it["question"] not in blind or it["item_id"] not in idxT:
                continue
            if blind[it["question"]].get("fok") is None or idxT[it["item_id"]].get("fok") is None:
                continue
            lab = it.get("label", it["label_pre"])
            rows.append({"item_id": it["item_id"], "persona": it["persona"], "question": it["question"], "label": lab,
                         "y_fok": 0 if lab == "ABSENT" else 1, "index_key": SC.gt_key(b, it["persona"]), "arm": "INDEXED-GT"})
        assert (len(rows), sum(r["y_fok"] for r in rows)) == (n, npos), f"{b}: {len(rows)} / {sum(r['y_fok'] for r in rows)}"
        assert all(r["index_key"] in gt for r in rows), f"{b}: GT index missing"
        cell["s1"][b] = rows
    frb = [it for it in items if it["backend"] == "frbank"]
    c661 = {i["item_id"]: i for i in J(ROOT / "r74/x4/cell_661.json")["items"]}
    for it in frb:
        q, tag = it["question"], it["item_id"]
        if q not in blind or tag not in idxT or tag not in idxB:
            continue
        if any(d.get("nok") is None for d in (blind[q], idxT[tag], idxB[tag])):
            continue
        lab = it.get("label", it["label_pre"])
        cell["s2u"].append({"item_id": tag, "persona": it["persona"], "question": q, "label": lab, "y_nok": 1 if lab == "PRESENT-NEGATIVE" else 0,
                            "index_key": s2map[tag], "arm": "INDEXED-S2U"})
    assert (len(cell["s2u"]), sum(r["y_nok"] for r in cell["s2u"])) == (661, 104)
    assert {r["item_id"] for r in cell["s2u"]} == set(c661) and all(c661[r["item_id"]]["y_nok"] == r["y_nok"] for r in cell["s2u"])
    assert all(r["index_key"] in s2u for r in cell["s2u"])
    texts = {**gt, **s2u}
    return cell, texts


def messages(row, texts):
    return [{"role": "system", "content": P.SYSTEM},
            {"role": "user", "content": P.USER_INDEXED.format(index=texts[row["index_key"]], question=row["question"])}]


def cmd_build():
    assert_lineage()
    rc = subprocess.run([sys.executable, str(SC.SIDE / "tools" / "verify_side.py")], capture_output=True, text=True).returncode
    assert rc == 0, "verify_side.py fails -- STOP"
    cell, texts = build_cell()
    meta = {"registration": "registrations/ADDENDUM_SIDE.md", "frozen": FREEZE, "lane": LANE, "temperature": 0, "seed": 42, "max_tokens": 200, "k": 1,
            "prompts_file_sha256": P.file_sha256(), "prompts_texts_sha256": P.texts_sha256(),
            "gt_indexes_sha256": hashlib.sha256((SC.S1 / "indexes_gt.json").read_bytes()).hexdigest(),
            "s2u_indexes_sha256": hashlib.sha256((SC.SIDE / "s2" / "indexes_s2u.json").read_bytes()).hexdigest(),
            "populations": {"mem0": {"n": len(cell["s1"]["mem0"]), "pos": sum(r["y_fok"] for r in cell["s1"]["mem0"])},
                            "amem": {"n": len(cell["s1"]["amem"]), "pos": sum(r["y_fok"] for r in cell["s1"]["amem"])},
                            "s2u": {"n": len(cell["s2u"]), "pn": sum(r["y_nok"] for r in cell["s2u"])}},
            "calls": len(cell["s1"]["mem0"]) + len(cell["s1"]["amem"]) + len(cell["s2u"]),
            "blind_intact_source": "e1_metamemory/elicitation_main.json (BLIND by question; INDEXED-TRUE / INDEXED-BELIEVED by tag); read, never re-elicited"}
    RUN.mkdir(parents=True, exist_ok=True); jdump({"meta": meta, "cell": cell}, RUN / "cell_side.json")
    print(json.dumps(meta, indent=1))


# ------------------------------------------------------------------ probe / project
def cmd_probe():
    assert_lineage(); e0 = redirect_cache()
    cell, texts = build_cell()
    out = {}
    for arm, first in (("INDEXED-GT", cell["s1"]["amem"][0]), ("INDEXED-S2U", cell["s2u"][0])):
        r = e0._client().chat.completions.create(model=P.MODEL, temperature=P.TEMPERATURE, seed=P.SEED, max_tokens=P.MAX_TOKENS,  # noqa: SLF001
                                                 messages=messages(first, texts), response_format={"type": "json_object"})
        o = api.parse_json(r.choices[0].message.content) or {}
        out[arm] = {"item_id": first["item_id"], "served": r.model, "identifier_ok": LANE in r.model, "tok_in": r.usage.prompt_tokens,
                    "tok_out": r.usage.completion_tokens, "usd": r.usage.prompt_tokens / 1e6 * PRICE[0] + r.usage.completion_tokens / 1e6 * PRICE[1],
                    "status": "OK" if clamp(o.get("fok")) is not None else "PARSE_FAIL", "sample": (r.choices[0].message.content or "")[:160]}
    jdump(out, RUN / "probes_side.json"); print(json.dumps(out, indent=1))
    if not all(v["identifier_ok"] for v in out.values()):
        sys.exit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch")
    if any(v["status"] != "OK" for v in out.values()):
        sys.exit("PROBE PARSE FAILURE -- do not launch")


def billed_so_far():
    leak = J(SC.SIDE / "leak" / "leak_side.json")["cost"]["usd_with_probe"]
    probes = sum(v["usd"] for v in J(RUN / "probes_side.json").values()) if (RUN / "probes_side.json").exists() else 0.0
    run = sum(json.loads(l).get("usd", 0.0) for l in io.open(ROWS_P, encoding="utf-8")) if ROWS_P.exists() else 0.0
    return {"leakage_screens": leak, "probes": probes, "run": run, "total": leak + probes + run}


def cmd_project():
    p = J(RUN / "probes_side.json"); cell, _ = build_cell()
    n = {"INDEXED-GT": len(cell["s1"]["mem0"]) + len(cell["s1"]["amem"]), "INDEXED-S2U": len(cell["s2u"])}
    tin = sum(p[a]["tok_in"] * n[a] for a in n); tout = sum(p[a]["tok_out"] * n[a] for a in n)
    usd = tin / 1e6 * PRICE[0] + tout / 1e6 * PRICE[1]; so_far = billed_so_far()
    print(f"calls        : {sum(n.values())}  (INDEXED-GT {n['INDEXED-GT']}, INDEXED-S2U {n['INDEXED-S2U']}; k=1)")
    print(f"projected in : {tin:,} tok   out: {tout:,} tok   PROJECTED ${usd:.4f}")
    print(f"billed so far: ${so_far['total']:.4f} (leakage ${so_far['leakage_screens']:.4f}, probes ${so_far['probes']:.4f}, run ${so_far['run']:.4f})")
    print(f"projected total ${usd + so_far['total']:.4f} against the ${BUDGET:.2f} line (section B; x1.3 = ${1.3 * usd + so_far['total']:.4f})")
    jdump({"projected_usd": usd, "billed_so_far": so_far, "n": n, "budget": BUDGET}, RUN / "projection_side.json")
    if usd + so_far["total"] > BUDGET:
        sys.exit("PROJECTION ABOVE THE $2 LINE -- STOP per section B")


# ------------------------------------------------------------------ run
def done_keys():
    ks = set()
    if ROWS_P.exists():
        for l in io.open(ROWS_P, encoding="utf-8"):
            r = json.loads(l); ks.add((r["item_id"], r["arm"]))
    return ks


def elicit(row, texts):
    """elicit_e1.run for an indexed arm, verbatim in effect: one retry on a parse failure."""
    msgs = messages(row, texts); arm = row["arm"]
    r = api.call(row["item_id"], arm, msgs); o = api.parse_json(r["content"]); n_calls, failed = 1, False
    if o is None or clamp(o.get("fok")) is None:
        r2 = api.call(row["item_id"], arm + "#retry", msgs); o = api.parse_json(r2["content"]); n_calls = 2
        usd = sum(x["prompt_tokens"] / 1e6 * PRICE[0] + x["completion_tokens"] / 1e6 * PRICE[1] for x in (r, r2) if not x["cached"])
        r = r2
        if o is None or clamp(o.get("fok")) is None:
            failed, o = True, {}
    else:
        usd = 0.0 if r["cached"] else r["prompt_tokens"] / 1e6 * PRICE[0] + r["completion_tokens"] / 1e6 * PRICE[1]
    return {"item_id": row["item_id"], "arm": arm, "draw": 1, "persona": row["persona"], "label": row["label"],
            "y_fok": row.get("y_fok"), "y_nok": row.get("y_nok"), "index_key": row["index_key"],
            "fok": clamp(o.get("fok")), "nok": clamp(o.get("nok")),
            "nok_candidates_found": (bool(o.get("nok_candidates_found")) if not failed else None),
            "would_search": (bool(o.get("would_search")) if not failed else None),
            "status": "ELICITATION_FAILED" if failed else "OK", "n_calls": n_calls, "cached": r["cached"],
            "tok_in": r.get("prompt_tokens"), "tok_out": r.get("completion_tokens"), "usd": usd, "text": (r["content"] or "")[:400]}


def cmd_run():
    assert_lineage(); redirect_cache()
    cell, texts = build_cell(); done = done_keys()
    jobs = [r for r in cell["s1"]["amem"] + cell["s1"]["mem0"] + cell["s2u"] if (r["item_id"], r["arm"]) not in done]
    print(f"{len(jobs)} calls to go (resumed past {len(done)})")
    lock, spend, stopped = threading.Lock(), [billed_so_far()["total"]], [False]

    def work(row):
        with lock:
            if spend[0] >= BUDGET or stopped[0]:
                stopped[0] = True; return None
        r = elicit(row, texts)
        with lock:
            spend[0] += r["usd"]
            with io.open(ROWS_P, "a", encoding="utf-8") as f:
                f.write(json.dumps(r, sort_keys=True) + "\n")
        return r
    try:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            out = [r for r in ex.map(work, jobs) if r is not None]
    finally:
        api.flush()
    c = collections.Counter((r["arm"], r["status"]) for r in out)
    print(f"DONE {len(out)} rows; status {dict(c)}; billed total ${spend[0]:.4f} against ${BUDGET:.2f}"
          + ("  >>> STOPPED AT THE $2 LINE with cells unscored" if stopped[0] else ""))
    if stopped[0]:
        sys.exit(1)


# ------------------------------------------------------------------ score
def boot_ratio(b, t, s, y, g=None, n=N_BOOT, seed=SEED):
    """Paired bootstrap of the retention ratio (s - b) / (t - b) under the committed draw scheme
    (common_e1r.boot_item / boot_cluster: default_rng(seed), 1,000 draws, single-class draws discarded;
    a draw with a non-positive TRUE gain is discarded too and counted)."""
    rng = np.random.default_rng(seed); b, t, s, y = (np.asarray(v, float) for v in (b, t, s, y)); y = y.astype(int)
    if g is not None:
        g = np.asarray(g); groups = np.unique(g); idx_by = {u: np.flatnonzero(g == u) for u in groups}
    d, n_nonpos = [], 0
    for _ in range(n):
        k = rng.integers(0, len(y), len(y)) if g is None else np.concatenate([idx_by[groups[j]] for j in rng.integers(0, len(groups), len(groups))])
        if y[k].sum() in (0, len(k)):
            continue
        ab = auroc(b[k], y[k]); dt = auroc(t[k], y[k]) - ab
        if dt <= 0:
            n_nonpos += 1; continue
        d.append((auroc(s[k], y[k]) - ab) / dt)
    d = np.asarray(d)
    return {"n_draws": int(len(d)), "n_nonpositive_true_gain_discarded": n_nonpos, "mean": float(d.mean()),
            "ci_lo": float(np.percentile(d, 2.5)), "ci_hi": float(np.percentile(d, 97.5))}


def cmd_score():
    assert_lineage()
    cell, _ = build_cell(); meta = J(RUN / "cell_side.json")["meta"]
    items, blind, idxT, idxB = load_e1()
    new = collections.defaultdict(dict); fails = collections.Counter(); tot = collections.Counter()
    for l in io.open(ROWS_P, encoding="utf-8"):
        r = json.loads(l); tot[r["arm"]] += 1
        if r["status"] != "OK":
            fails[r["arm"]] += 1; continue
        new[r["arm"]][r["item_id"]] = r
    spend = billed_so_far()
    out = {"registration": "registrations/ADDENDUM_SIDE.md", "frozen": FREEZE, "lane": LANE, "meta": meta,
           "rows": {a: {"elicited": tot[a], "failed": fails[a]} for a in sorted(tot)}, "spend": spend, "budget_line": BUDGET,
           "estimators": "common_e1r.auroc (Mann-Whitney, ties 0.5); boot_item (item-level paired, 1,000 draws, seed 42, single-class draws discarded); boot_cluster (persona-clustered paired) beside; tolerance 0.05",
           "S1": {}, "S2U": {}}

    # ---- S1: FOK on Mem0 (descriptive) and A-MEM (registered)
    for b in ("amem", "mem0"):
        rows = [r for r in cell["s1"][b] if r["item_id"] in new["INDEXED-GT"] and new["INDEXED-GT"][r["item_id"]]["fok"] is not None]
        y = [r["y_fok"] for r in rows]; g = [r["persona"] for r in rows]
        bl = [blind[r["question"]]["fok"] for r in rows]; tr = [idxT[r["item_id"]]["fok"] for r in rows]; gtv = [new["INDEXED-GT"][r["item_id"]]["fok"] for r in rows]
        A = {"blind": auroc(bl, y), "true": auroc(tr, y), "gt": auroc(gtv, y)}
        X, Y = A["true"] - A["blind"], A["gt"] - A["blind"]; D = Y - X
        d_item, d_cl = boot_item(tr, gtv, y), boot_cluster(tr, gtv, y, g)            # GT - TRUE per item
        y_item, y_cl = boot_item(bl, gtv, y), boot_cluster(bl, gtv, y, g)            # GT - blind
        x_item = boot_item(bl, tr, y)
        res = {"n": len(rows), "n_pos": int(sum(y)), "n_personas": len(set(g)), "n_population": len(cell["s1"][b]),
               "coverage": f"{len(rows)} of {len(cell['s1'][b])} items scored under INDEXED-GT (paired on those)",
               "auroc": A, "gain_true_X": X, "gain_gt_Y": Y, "difference_D": D,
               "D_interval_item": d_item, "D_interval_clustered": d_cl, "Y_interval_item": y_item, "Y_interval_clustered": y_cl, "X_interval_item": x_item}
        if b == "amem":
            p1_item, p1_cl = D > TOL and d_item["ci_lo"] > 0, D > TOL and d_cl["ci_lo"] > 0
            p2_item, p2_cl = y_item["ci_hi"] >= 0, y_cl["ci_hi"] >= 0
            res["S1-P1"] = {"holds": bool(p1_item and p1_cl), "item_level": bool(p1_item), "clustered": bool(p1_cl), "disagree": bool(p1_item != p1_cl),
                            "criterion": "D > 0.05 and the paired interval of GT - TRUE excludes zero; the weaker reading governs where the two intervals disagree"}
            res["S1-P2"] = {"holds": bool(p2_item and p2_cl), "item_level": bool(p2_item), "clustered": bool(p2_cl), "disagree": bool(p2_item != p2_cl),
                            "criterion": "the GT gain's interval does not lie entirely below zero; the weaker reading governs"}
            res["arm_status"] = "registered test (two-channel map, spot-check 0.800, rule (c) 0.970)"
        else:
            res["arm_status"] = "DESCRIPTIVE ROW: spot-check precision 0.567 under the two-channel map; lexical-required coverage 0.494 < 0.50 (rule (c)); no verdict"
        out["S1"][b] = res
    out["S1"]["H45"] = "-- (no committed Haiku blind or TRUE rows on the external items; the S1 Haiku lane moves to October)"

    # ---- S2-U: NOK on the 661
    rows = [r for r in cell["s2u"] if r["item_id"] in new["INDEXED-S2U"] and new["INDEXED-S2U"][r["item_id"]]["nok"] is not None]
    y = [r["y_nok"] for r in rows]; g = [r["persona"] for r in rows]
    bl = [blind[r["question"]]["nok"] for r in rows]; tr = [idxT[r["item_id"]]["nok"] for r in rows]
    be = [idxB[r["item_id"]]["nok"] for r in rows]; su = [new["INDEXED-S2U"][r["item_id"]]["nok"] for r in rows]
    A = {"blind": auroc(bl, y), "true": auroc(tr, y), "believed": auroc(be, y), "s2u": auroc(su, y)}
    gains = {"true": A["true"] - A["blind"], "believed": A["believed"] - A["blind"], "s2u": A["s2u"] - A["blind"]}
    out["S2U"] = {"n": len(rows), "n_pn": int(sum(y)), "n_personas": len(set(g)), "n_population": len(cell["s2u"]),
                  "coverage": f"{len(rows)} of {len(cell['s2u'])} items scored under S2-U (all four arms paired on those)",
                  "auroc": A, "gains": gains,
                  "s2u_gain_interval_item": boot_item(bl, su, y), "s2u_gain_interval_clustered": boot_cluster(bl, su, y, g),
                  "true_gain_interval_item": boot_item(bl, tr, y), "believed_gain_interval_item": boot_item(bl, be, y),
                  "retention_s2u": gains["s2u"] / gains["true"], "retention_believed_committed_recomputed": gains["believed"] / gains["true"],
                  "retention_s2u_interval_item": boot_ratio(bl, tr, su, y), "retention_s2u_interval_clustered": boot_ratio(bl, tr, su, y, g),
                  "s2u_minus_believed_item": boot_item(be, su, y), "s2u_minus_believed_clustered": boot_cluster(be, su, y, g),
                  "expected_direction": "retention short of 60%", "line_60pct": 0.60, "committed_retention_42_3": 0.423}
    out["S2U"]["branch"] = "retention reaches 60% (not expected)" if out["S2U"]["retention_s2u"] >= 0.60 else "retention stays short of 60% (expected)"
    jdump(out, RUN / "scores_side.json")
    print_report(out)


def fmt_i(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"


def print_report(o):
    W = 104
    print("=" * W); print(f"SIDE-BUILD-1 step 5 -- S1 and S2-U mini lanes (ADDENDUM_SIDE.md, frozen {FREEZE}); lane {o['lane']}"); print("=" * W)
    print(f"rows: {o['rows']}")
    for b in ("amem", "mem0"):
        r = o["S1"][b]; A = r["auroc"]
        print(f"\n---- S1 {b.upper()}  n={r['n']} pos={r['n_pos']} personas={r['n_personas']}  ({r['coverage']})")
        print(f"  {r['arm_status']}")
        print(f"  AUROC  blind {A['blind']:.4f}   INDEXED-TRUE {A['true']:.4f}   INDEXED-GT {A['gt']:.4f}")
        print(f"  gains  X = TRUE - blind {r['gain_true_X']:+.4f} {fmt_i(r['X_interval_item'])}   Y = GT - blind {r['gain_gt_Y']:+.4f} item {fmt_i(r['Y_interval_item'])} clustered {fmt_i(r['Y_interval_clustered'])}")
        print(f"  D = Y - X = GT - TRUE {r['difference_D']:+.4f}   item {fmt_i(r['D_interval_item'])}   clustered {fmt_i(r['D_interval_clustered'])}")
        if b == "amem":
            p1, p2 = r["S1-P1"], r["S1-P2"]
            print(f"\n  S1-P1 {'HOLDS' if p1['holds'] else 'FAILS'}  (item-level {'holds' if p1['item_level'] else 'fails'}, clustered {'holds' if p1['clustered'] else 'fails'}"
                  + ("; the two intervals DISAGREE -- the weaker reading governs)" if p1["disagree"] else ")"))
            print(f"  S1-P2 {'HOLDS' if p2['holds'] else 'FAILS'}  (item-level {'holds' if p2['item_level'] else 'fails'}, clustered {'holds' if p2['clustered'] else 'fails'}"
                  + ("; the two intervals DISAGREE -- the weaker reading governs)" if p2["disagree"] else ")"))
            X, Y, D, I = r["gain_true_X"], r["gain_gt_Y"], r["difference_D"], fmt_i(r["D_interval_item"]); IY = fmt_i(r["Y_interval_item"])
            print("\n  frozen text, S1-P1:")
            if p1["holds"]:
                print(f'    "Given the manifest\'s names for what it holds, the store no longer inverts the benefit by the margin it did; the inversion was a property of the index the store was handed, not of the store alone."  (X={X:+.4f}, Y={Y:+.4f}, D={D:+.4f}, I={I})')
            else:
                print(f'    "On the committed A-MEM items, handing the store a name-bearing index built from the manifest for the entries it holds moves the coverage gain from {X:+.4f} to {Y:+.4f}, a paired difference of {D:+.4f} with interval {I}, which does not clear the tolerance with an interval excluding zero. The inversion is not repaired by naming, and Section 5.3 keeps its wording."')
            print("  frozen text, S1-P2:")
            if p2["holds"]:
                print(f'    "The name-bearing index does not invert."  (Y={Y:+.4f}, I={IY})')
            else:
                print(f'    "Under the name-bearing index the coverage gain on A-MEM is {Y:+.4f} with interval {IY} lying entirely below zero: on this store the index inverts the benefit even when it carries the manifest\'s names."')
        else:
            X, Y, IY = r["gain_true_X"], r["gain_gt_Y"], fmt_i(r["Y_interval_item"])
            print("\n  frozen text, Mem0 descriptive row (prints regardless):")
            print(f'    "On Mem0 the name-bearing index could be built for 49.4 percent of the store\'s entries under the lexical-required mapping the spot-check forced (two-channel precision 0.567); below the registered coverage floor of one half, its coverage gain of {Y:+.4f} (interval {IY}; TRUE {X:+.4f}) is reported and carries no verdict."')
    print(f"\n---- S1 Haiku 4.5: {o['S1']['H45']}")
    s = o["S2U"]; A = s["auroc"]; G = s["gains"]
    print(f"\n---- S2-U  n={s['n']} PN={s['n_pn']} personas={s['n_personas']}  ({s['coverage']})  DESCRIPTIVE, no pass bar")
    print(f"  NOK AUROC  blind {A['blind']:.4f}   TRUE {A['true']:.4f}   BELIEVED {A['believed']:.4f}   S2-U {A['s2u']:.4f}")
    print(f"  gains      TRUE {G['true']:+.4f} {fmt_i(s['true_gain_interval_item'])}   BELIEVED {G['believed']:+.4f} {fmt_i(s['believed_gain_interval_item'])}   "
          f"S2-U {G['s2u']:+.4f} item {fmt_i(s['s2u_gain_interval_item'])} clustered {fmt_i(s['s2u_gain_interval_clustered'])}")
    ri, rc = s["retention_s2u_interval_item"], s["retention_s2u_interval_clustered"]
    print(f"  retention  (S2-U - blind) / (TRUE - blind) = {100 * s['retention_s2u']:.1f}%   item [{100 * ri['ci_lo']:.1f}%, {100 * ri['ci_hi']:.1f}%] "
          f"clustered [{100 * rc['ci_lo']:.1f}%, {100 * rc['ci_hi']:.1f}%]   (committed BELIEVED retention 42.3%, recomputed {100 * s['retention_believed_committed_recomputed']:.1f}%; the 60% line)")
    d1, d2 = s["s2u_minus_believed_item"], s["s2u_minus_believed_clustered"]
    print(f"  S2-U - BELIEVED  {A['s2u'] - A['believed']:+.4f}   item {fmt_i(d1)}   clustered {fmt_i(d2)}")
    F = 100 * s["retention_s2u"]
    print(f"  branch: {s['branch']}\n  frozen text:")
    if s["retention_s2u"] >= 0.60:
        print(f'    "Lifting the cap on the believed list, which raises its recall of ground-truth superseded names from 30.0 to 66.6 percent at unchanged precision, retains {F:.1f} percent of the TRUE gain, at or above the 60 percent threshold. Part of the believed-state loss recorded at 42.3 percent is an effect of the renderer\'s cap of fifteen names rather than of the store\'s metadata."')
    else:
        print(f'    "Lifting the cap on the believed list raises its recall of ground-truth superseded names from 30.0 to 66.6 percent and leaves its precision at 0.035; under that list the obligation gain retains {F:.1f} percent of the TRUE gain, still short of the 60 percent threshold. The believed-state loss is not a cap effect."')
    sp = o["spend"]
    print(f"\n---- SPEND  billed ${sp['total']:.4f} against the ${o['budget_line']:.2f} line: leakage screens ${sp['leakage_screens']:.4f}, probes ${sp['probes']:.4f}, "
          f"S1 + S2-U run ${sp['run']:.4f}   ({'UNDER' if sp['total'] < o['budget_line'] else 'AT OR OVER'} the line)")
    print("=" * W)


if __name__ == "__main__":
    globals()["cmd_" + sys.argv[1]]()
