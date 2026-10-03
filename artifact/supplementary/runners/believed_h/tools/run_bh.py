# -*- coding: utf-8 -*-
"""run_bh.py -- ADDENDUM_BELIEVED_H (R-A): Haiku 4.5 under the lifecycle store's own metadata, capped and lifted renderings.
Registration: registrations/ADDENDUM_BELIEVED_H.md, registered text sha256 77de1e37... (the bytes above the marker), frozen
at 257a090 on 2026-09-14. Descriptive: no prediction, no bar, no verdict; the three branches of its section 4 print as they
come out. run_cf's module globals are re-pointed (the recipe of pad_probe/tools/contam.py and cf3/cf3_run.py); nothing in
run_cf, score_cf or prompts_e1 is edited.

Subcommands, in the registered order:
  build            locks (registration sha256; the two recorded text files' sha256; the 661 item-to-key map against
                   indexes_s2u.json items), the texts per arm, the $0 lookup on the lifted list with the capped value
                   reproduced as a gate (0.5858), the ledger's first sections -> believed_h/build/build_bh.json
  probe <arm>      one Haiku 4.5 call on the first item under that arm (served identifier, E1.7) and the projection
                   (661 x 5 calls at Batch pricing, x1.3) against the $12 cap less what this addendum has billed
  submit <arm>     the Batch for that arm (k = 5, temperature 0, max_tokens 200); refuses without a fitting probe
  poll <arm>       collect the Batch into believed_h/rows/<arm>/rows_H45.jsonl
  score            after both arms are collected (a later step)
Arms: INDEXED-BELIEVED-LIFTED first (the S2-U texts), then INDEXED-BELIEVED-15 (the committed BELIEVED texts) if the
remaining headroom covers its projection at x1.3; otherwise it prints a dash with the projection beside it.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[2]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "resp_review/tools", "ds_downstream/tools"):
    sys.path.insert(0, str(ROOT / p))
import numpy as np  # noqa: E402
from common_e1r import auroc, load_e1  # noqa: E402
from index_v3 import named_sections  # noqa: E402
from run_nb6 import build as nb6_build, emb_scores  # noqa: E402
import run_cf as RC  # noqa: E402  (asserts the prompts_e1 digests at import)

BH = ROOT / "believed_h"
BUILD, ROWS = BH / "build", BH / "rows"
REG = ROOT / "registrations" / "ADDENDUM_BELIEVED_H.md"
REG_SHA = "77de1e3786e4e86214f35a2a89c76d1daf4f88bd902f6c0e5f34880982b05d5c"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
LANE = "claude-haiku-4-5-20251001"
ARMS = ("INDEXED-BELIEVED-LIFTED", "INDEXED-BELIEVED-15")
CAP = 12.00
RECORDED = {"blind": 0.4150, "true": 0.8210, "lookup_capped": 0.5858, "mini_capped": 0.5959, "mini_lifted": 0.6513}
CELL = json.load(io.open(ROOT / "r74" / "x4" / "cell_661.json", encoding="utf-8"))["items"]
E1_IDX = ROOT / "e1_metamemory" / "indexes_v2.json"
S2U = ROOT / "side_experiments" / "s2" / "indexes_s2u.json"


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def registration_ok():
    b = REG.read_bytes(); i = b.find(FROZEN_END)
    return i > 0 and hashlib.sha256(b[:i]).hexdigest() == REG_SHA


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=1, sort_keys=True, default=float); f.write("\n")


_T = {}


def texts():
    """item_id -> {arm: text}, from the two recorded files; asserted at build."""
    if _T:
        return _T
    e1 = jload(E1_IDX)["indexes"]; s2 = jload(S2U)
    s2map = {it["item_id"]: it for it in s2["items"]}
    for it in CELL:
        m = s2map[it["item_id"]]
        assert m["index_key_true"] == it["index_key"] and m["index_key_believed"] == it["index_key"].replace(":TRUE", ":BELIEVED")
        _T[it["item_id"]] = {"INDEXED-BELIEVED-15": e1[m["index_key_believed"]], "INDEXED-BELIEVED-LIFTED": s2["indexes"][m["index_key_s2u"]]}
    return _T


def units(arm):
    T = texts()
    return [{"unit_id": it["item_id"], "question": it["question"], "index": T[it["item_id"]][arm]} for it in CELL]


def point(arm):
    RC.CELL = CELL; RC.ARMS = (arm,); RC.units = units
    RC.ROWS = ROWS / arm; RC.PROBES = BUILD / "probes.json"


def billed_so_far():
    """Committed spend under the cap: collected rows at their metered cost, plus the projection of any submitted Batch
    not yet collected, plus the probes."""
    usd = 0.0
    pr = jload(BUILD / "probes.json") if (BUILD / "probes.json").exists() else {}
    for arm in ARMS:
        p = ROWS / arm / "rows_H45.jsonl"
        if p.exists():
            usd += sum(json.loads(l).get("usd", 0.0) for l in io.open(p, encoding="utf-8"))
        elif (ROWS / arm / "batch_H45.json").exists() and arm in pr:
            usd += pr[arm]["projection"]["usd"]
    usd += sum(v.get("probe_usd", 0.0) for v in pr.values())
    return usd


# ------------------------------------------------------------------ build
def cmd_build():
    assert registration_ok(), "STOP: registration sha256 mismatch"
    T = texts(); assert len(T) == 661
    y = np.array([it["y_nok"] for it in CELL], int); assert int(y.sum()) == 104
    # the lookup on the capped list through run_nb6's committed functions (gate 0.5858), then on the lifted list
    items, blind, idxT, idxB = load_e1()
    from common_e1r import POPULATIONS
    src = [it for it in items if POPULATIONS["R-NOK-FRB"]["filt"](it)]
    rows_b = nb6_build(src, blind, idxB, "nok", "BELIEVED")
    by_id = {r["item_id"]: r for r in rows_b}
    assert set(by_id) == {it["item_id"] for it in CELL}, "the BELIEVED rows are not the cell's 661 items"
    rows = [by_id[it["item_id"]] for it in CELL]            # aligned to the cell's order by item_id
    emb_capped = np.array(emb_scores(rows, "sup")); a_capped = round(float(auroc(emb_capped, y)), 4)
    assert a_capped == RECORDED["lookup_capped"], f"GATE: capped lookup {a_capped} != {RECORDED['lookup_capped']}"
    lifted_lists = [named_sections(T[it["item_id"]]["INDEXED-BELIEVED-LIFTED"])["superseded"] for it in CELL]
    rows_l = [{"question": it["question"], "sup": lst} for it, lst in zip(CELL, lifted_lists)]
    emb_lifted = np.array(emb_scores(rows_l, "sup")); a_lifted = float(auroc(emb_lifted, y))
    from common_e1r import boot_cluster_single
    sys.path.insert(0, str(ROOT / "reviews" / "v18" / "tools"))
    from a1_count_readers import boot_item_single  # noqa: E402
    g = np.array([it["persona"] for it in CELL])
    census = {"capped_names_per_item_mean": float(np.mean([len(r["sup"]) for r in rows])), "lifted_names_per_item_mean": float(np.mean([len(l) for l in lifted_lists])),
              "lifted_max": int(max(len(l) for l in lifted_lists)), "capped_chars_mean": float(np.mean([len(T[i]["INDEXED-BELIEVED-15"]) for i in T])),
              "lifted_chars_mean": float(np.mean([len(T[i]["INDEXED-BELIEVED-LIFTED"]) for i in T]))}
    rec = {"registration_sha256": REG_SHA, "frozen_at": "257a090", "locks": {"indexes_v2.json": sha_file(E1_IDX), "indexes_s2u.json": sha_file(S2U), "cell_661.json": sha_file(ROOT / "r74" / "x4" / "cell_661.json"),
                                                                              "item_key_map_asserted": True, "n_items": 661, "n_pos": 104},
           "lookup": {"capped": {"auroc": a_capped, "gate": RECORDED["lookup_capped"], "ok": True},
                      "lifted": {"auroc": round(a_lifted, 4), "item_ci": boot_item_single(emb_lifted, y), "persona_ci": boot_cluster_single(emb_lifted, y, g),
                                 "scores": emb_lifted.tolist()}},
           "census": census, "recorded_rows_read": RECORDED, "arms": list(ARMS), "cap_usd": CAP}
    jdump(rec, BUILD / "build_bh.json")
    print(f"locks ok; capped lookup {a_capped} (gate {RECORDED['lookup_capped']}); lifted lookup {a_lifted:.4f}; census {json.dumps(census)}")
    write_ledger()


# ------------------------------------------------------------------ probe, submit, poll
def cmd_probe(arm):
    assert registration_ok(), "STOP: registration sha256 mismatch"
    point(arm); RC.load_env()
    cfg = RC.LANES[LANE]
    r = RC.call_once(LANE, units(arm)[0], arm, 0)
    ok = LANE.split("-2025")[0] in r["served_model"] or LANE in r["served_model"]
    n = cfg["k"] * len(CELL)
    # every prompt's input tokens estimated from the probe's ratio of tokens to characters over the arm's texts
    chars0 = len(units(arm)[0]["index"]); ratio = r["tok_in"] / max(1, chars0)
    tin = sum(int(len(u["index"]) * ratio) for u in units(arm)) * cfg["k"]
    tout = n * max(1, r["tok_out"])
    usd = (tin / 1e6 * cfg["price"][0] + tout / 1e6 * cfg["price"][1]) * cfg["mult"]
    billed = billed_so_far() + r["usd"]
    headroom = CAP - billed
    rec = {"arm": arm, "served": r["served_model"], "identifier_ok": ok, "in": r["tok_in"], "out": r["tok_out"], "parsed": r["status"], "probe_usd": r["usd"],
           "projection": {"calls": n, "input_tokens": tin, "output_tokens": tout, "usd": round(usd, 4), "usd_x1.3": round(usd * 1.3, 4)},
           "billed_before": round(billed, 4), "headroom": round(headroom, 4), "fits": bool(ok and usd * 1.3 <= headroom), "sample": r["text"][:200]}
    d = jload(RC.PROBES) if RC.PROBES.exists() else {}
    d[arm] = rec; jdump(d, RC.PROBES)
    print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")
    if not rec["fits"]:
        print(f"DASH: the x1.3 projection ${usd * 1.3:.2f} exceeds the headroom ${headroom:.2f} under the ${CAP:.2f} cap; this arm prints a dash")
    write_ledger()


def cmd_submit(arm):
    assert registration_ok(), "STOP: registration sha256 mismatch"
    point(arm)
    pr = jload(RC.PROBES).get(arm)
    assert pr and pr["identifier_ok"], "STOP: probe this arm first"
    assert pr["fits"], "STOP: the arm's x1.3 projection exceeds the headroom; it prints a dash"
    RC.cmd_submit(LANE)
    write_ledger()


def cmd_poll(arm):
    point(arm); RC.cmd_poll(LANE); write_ledger()


# ------------------------------------------------------------------ score
def lane_rows(arm):
    """(item_id -> mean nok over >= 3 draws) for one collected arm, the X4 collapse."""
    import collections
    per = collections.defaultdict(dict)
    p = ROWS / arm / "rows_H45.jsonl"
    for line in io.open(p, encoding="utf-8"):
        r = json.loads(line)
        if r.get("status") == "OK" and r.get("nok") is not None:
            per[r["unit_id"]][int(r["draw"])] = float(r["nok"])
    out = {u: float(np.mean(list(d.values()))) for u, d in per.items() if len(d) >= 3}
    usd = sum(json.loads(l).get("usd", 0.0) for l in io.open(p, encoding="utf-8"))
    n_bad = sum(1 for l in io.open(p, encoding="utf-8") if json.loads(l).get("status") != "OK")
    return out, usd, n_bad


def ratio_boot(blind, true, bel, y, g, n=1000, seed=42):
    """Retention = (bel - blind) / (true - blind) on resampled sets; item-level and persona-clustered; draws with a non-positive
    denominator or a single class discarded and counted."""
    rng = np.random.default_rng(seed); groups = np.unique(g); by = {u: np.flatnonzero(g == u) for u in groups}
    out = {}
    for mode in ("item", "persona"):
        rr, disc = [], 0
        for _ in range(n):
            k = rng.integers(0, len(y), len(y)) if mode == "item" else np.concatenate([by[groups[t]] for t in rng.integers(0, len(groups), len(groups))])
            if y[k].sum() in (0, len(k)):
                disc += 1; continue
            den = auroc(true[k], y[k]) - auroc(blind[k], y[k])
            if den <= 0:
                disc += 1; continue
            rr.append((auroc(bel[k], y[k]) - auroc(blind[k], y[k])) / den)
        rr = np.asarray(rr)
        out[mode] = {"n_draws": int(len(rr)), "discarded": disc, "ci_lo": float(np.percentile(rr, 2.5)), "ci_hi": float(np.percentile(rr, 97.5)), "mean": float(rr.mean())}
    return out


def cmd_score():
    assert registration_ok(), "STOP: registration sha256 mismatch"
    sys.path.insert(0, str(ROOT / "r74" / "tools")); sys.path.insert(0, str(ROOT / "reviews" / "v18" / "tools"))
    import x4_score  # noqa: E402
    from cf2_score import paired  # noqa: E402
    from a1_count_readers import boot_item_single  # noqa: E402
    from common_e1r import boot_cluster_single  # noqa: E402
    coll, _ = x4_score.load_lane("H45")
    y = np.array([it["y_nok"] for it in CELL], int); g = np.array([it["persona"] for it in CELL])
    st = np.array([{"sup": "SUPERSESSION", "ret": "RETRACTION", "exp": "EXPIRY"}.get(v["state"], "-") for v in
                   (json.load(io.open(ROOT / "resp_review" / "l2" / "retrieval.json", encoding="utf-8"))["items"][it["item_id"]] for it in CELL)])
    blind = np.array([coll[(it["item_id"], "BLIND")]["nok"] for it in CELL], float)
    true = np.array([coll[(it["item_id"], "INDEXED-TRUE")]["nok"] for it in CELL], float)
    b_a, t_a = round(float(auroc(blind, y)), 4), round(float(auroc(true, y)), 4)
    assert (b_a, t_a) == (RECORDED["blind"], RECORDED["true"]), ("GATE: recorded Haiku rows", b_a, t_a)
    build = jload(BUILD / "build_bh.json"); look_l = np.array(build["lookup"]["lifted"]["scores"], float)
    items_, blind_e1, idxT, idxB = load_e1()
    from common_e1r import POPULATIONS
    src = [it for it in items_ if POPULATIONS["R-NOK-FRB"]["filt"](it)]
    rows_b = {r["item_id"]: r for r in nb6_build(src, blind_e1, idxB, "nok", "BELIEVED")}
    look_c = np.array(emb_scores([rows_b[it["item_id"]] for it in CELL], "sup"), float)
    res = {"registration_sha256": REG_SHA, "frozen_at": "257a090", "n": 661, "pos": 104, "recorded": {"blind": b_a, "true": t_a}, "arms": {}, "spend": {}}
    for arm, look in (("INDEXED-BELIEVED-LIFTED", look_l), ("INDEXED-BELIEVED-15", look_c)):
        bel_d, usd, n_bad = lane_rows(arm)
        bel = np.array([bel_d.get(it["item_id"], np.nan) for it in CELL], float); ok = ~np.isnan(bel)
        assert ok.all(), (arm, int((~ok).sum()), "items without a collapsed score")
        a = float(auroc(bel, y))
        R = {"n_rows_bad": n_bad, "usd": round(usd, 4), "auroc": round(a, 4), "item_ci": boot_item_single(bel, y), "persona_ci": boot_cluster_single(bel, y, g),
             "minus_true": paired(true, bel, y, g), "minus_blind": paired(blind, bel, y, g),
             "retention": {"point": round((a - b_a) / (t_a - b_a), 4), **ratio_boot(blind, true, bel, y, g)},
             "lookup_auroc": round(float(auroc(look, y)), 4), "haiku_minus_lookup": paired(look, bel, y, g), "per_state": {}}
        for s_ in ("SUPERSESSION", "RETRACTION", "EXPIRY"):
            m = (st == s_) | (y == 0)
            R["per_state"][s_] = {"n": int(m.sum()), "pos": int(y[m].sum()), "believed": round(float(auroc(bel[m], y[m])), 4), "true": round(float(auroc(true[m], y[m])), 4),
                                  "blind": round(float(auroc(blind[m], y[m])), 4), "lookup": round(float(auroc(look[m], y[m])), 4)}
        res["arms"][arm] = R; res["spend"][arm] = round(usd, 4)
    pr = jload(BUILD / "probes.json"); res["spend"]["probes"] = round(sum(v["probe_usd"] for v in pr.values()), 4)
    res["spend"]["total"] = round(sum(res["spend"].values()), 4); res["spend"]["cap"] = CAP
    # the three branches (section 4)
    rl, rc = res["arms"]["INDEXED-BELIEVED-LIFTED"]["retention"]["point"], res["arms"]["INDEXED-BELIEVED-15"]["retention"]["point"]
    al, ac = res["arms"]["INDEXED-BELIEVED-LIFTED"]["auroc"], res["arms"]["INDEXED-BELIEVED-15"]["auroc"]
    if rl < 0.60 and rc < 0.60:
        br = "below 60% under both renderings"; ab = ("the abstract keeps 'under the lifecycle store's own metadata the readers we test fall near chance'" if max(al, ac) <= 0.60
                                                      else f"the abstract says the readers 'fall by {max(t_a - al, t_a - ac):.2f}'")
    elif rl >= 0.60 and rc < 0.60:
        br = "at or above 60% under the lifted rendering only"; ab = "the abstract says 'the smallest model and the lookup fall near chance under the store's own metadata; a larger model keeps more of its gain once the renderer's cap is lifted'"
    elif rl >= 0.60 and rc >= 0.60:
        br = "at or above 60% under both"; ab = f"the abstract says 'the smallest model and the lookup fall near chance; the larger model keeps {rc:.0%} of its gain'"
    else:
        br = "at or above 60% under the capped rendering only (no branch enumerated; printed as it came out)"; ab = "the wording is the author's call"
    res["branch"] = {"retention_lifted": rl, "retention_capped": rc, "fires": br, "abstract": ab}
    jdump(res, BH / "results" / "scores_bh.json")
    for arm, R in res["arms"].items():
        print(f"{arm}: {R['auroc']:.4f} item [{R['item_ci']['ci_lo']:.4f},{R['item_ci']['ci_hi']:.4f}] persona [{R['persona_ci']['ci_lo']:.4f},{R['persona_ci']['ci_hi']:.4f}]; minus TRUE {R['minus_true']['delta']:+.4f} "
              f"item [{R['minus_true']['item_ci']['ci_lo']:+.4f},{R['minus_true']['item_ci']['ci_hi']:+.4f}] persona [{R['minus_true']['persona_ci']['ci_lo']:+.4f},{R['minus_true']['persona_ci']['ci_hi']:+.4f}]; "
              f"minus blind {R['minus_blind']['delta']:+.4f}; retention {R['retention']['point']:.4f} item [{R['retention']['item']['ci_lo']:.4f},{R['retention']['item']['ci_hi']:.4f}] "
              f"persona [{R['retention']['persona']['ci_lo']:.4f},{R['retention']['persona']['ci_hi']:.4f}] (discarded {R['retention']['item']['discarded']}/{R['retention']['persona']['discarded']}); "
              f"lookup {R['lookup_auroc']:.4f}, Haiku minus lookup {R['haiku_minus_lookup']['delta']:+.4f} [{R['haiku_minus_lookup']['item_ci']['ci_lo']:+.4f},{R['haiku_minus_lookup']['item_ci']['ci_hi']:+.4f}]; "
              f"per state believed/true SUP {R['per_state']['SUPERSESSION']['believed']}/{R['per_state']['SUPERSESSION']['true']} RET {R['per_state']['RETRACTION']['believed']}/{R['per_state']['RETRACTION']['true']} "
              f"EXP {R['per_state']['EXPIRY']['believed']}/{R['per_state']['EXPIRY']['true']}; bad rows {R['n_rows_bad']}; ${R['usd']:.4f}")
    print("branch:", json.dumps(res["branch"])); print("spend:", json.dumps(res["spend"]))
    write_ledger()


# ------------------------------------------------------------------ the own-name split (the author's follow-up of 2026-09-14; $0)
def cmd_split():
    """Split the 63 supersession obligations by whether the item's own scrubbed name (any of its forbidding records' slot names)
    survives in the BELIEVED superseded-names list, per rendering; score Haiku 4.5 (BELIEVED and truthful) and the lookup on each
    half against the same 557 negatives, both intervals; paired BELIEVED minus truthful on each half."""
    assert registration_ok()
    sys.path.insert(0, str(ROOT / "r74" / "tools")); sys.path.insert(0, str(ROOT / "reviews" / "v18" / "tools"))
    import x4_score  # noqa: E402
    from cf2_score import paired  # noqa: E402
    from a1_count_readers import boot_item_single  # noqa: E402
    from common_e1r import boot_cluster_single, POPULATIONS  # noqa: E402
    from resp_common import true_flags  # noqa: E402
    T = texts(); fl = true_flags()
    retr = json.load(io.open(ROOT / "resp_review" / "l2" / "retrieval.json", encoding="utf-8"))["items"]
    coll, _ = x4_score.load_lane("H45")
    y = np.array([it["y_nok"] for it in CELL], int); g = np.array([it["persona"] for it in CELL])
    true = np.array([coll[(it["item_id"], "INDEXED-TRUE")]["nok"] for it in CELL], float)
    build = jload(BUILD / "build_bh.json"); look = {"INDEXED-BELIEVED-LIFTED": np.array(build["lookup"]["lifted"]["scores"], float)}
    items_, blind_e1, idxT, idxB = load_e1()
    src = [it for it in items_ if POPULATIONS["R-NOK-FRB"]["filt"](it)]
    rows_b = {r["item_id"]: r for r in nb6_build(src, blind_e1, idxB, "nok", "BELIEVED")}
    look["INDEXED-BELIEVED-15"] = np.array(emb_scores([rows_b[it["item_id"]] for it in CELL], "sup"), float)
    sup = np.array([retr[it["item_id"]]["label"] == "PRESENT-NEGATIVE" and retr[it["item_id"]]["state"] == "sup" for it in CELL])
    neg = y == 0
    out = {"n_supersession_obligations": int(sup.sum()), "n_negatives": int(neg.sum()), "rule": "present iff any forbidding record's scrubbed slot name is in the rendering's superseded-names section", "arms": {}}
    for arm in ARMS:
        bel_d, _, _ = lane_rows(arm); bel = np.array([bel_d[it["item_id"]] for it in CELL], float)
        present = np.zeros(len(CELL), bool)
        for k, it in enumerate(CELL):
            if sup[k]:
                names = set(named_sections(T[it["item_id"]][arm])["superseded"])
                own = {fl[it["persona"]][m]["slot"] for m in retr[it["item_id"]]["pn_members"] if m in fl[it["persona"]]}
                present[k] = bool(own & names)
        R = {"present": int((sup & present).sum()), "absent": int((sup & ~present).sum()), "halves": {}}
        for half, mask in (("present", sup & present), ("absent", sup & ~present)):
            m = mask | neg
            if mask.sum() == 0:
                R["halves"][half] = {"n_pos": 0}; continue
            d = {"n_pos": int(mask.sum()), "n": int(m.sum())}
            for name, v in (("haiku_believed", bel), ("haiku_truthful", true), ("lookup_believed", look[arm])):
                d[name] = {"auroc": round(float(auroc(v[m], y[m])), 4), "item_ci": boot_item_single(v[m], y[m]), "persona_ci": boot_cluster_single(v[m], y[m], g[m])}
            d["believed_minus_truthful"] = paired(true[m], bel[m], y[m], g[m])
            d["haiku_minus_lookup"] = paired(look[arm][m], bel[m], y[m], g[m])
            R["halves"][half] = d
        out["arms"][arm] = R
    jdump(out, BH / "results" / "split_bh.json")
    for arm, R in out["arms"].items():
        print(f"{arm}: own name present {R['present']} / absent {R['absent']} of {out['n_supersession_obligations']}")
        for half, d in R["halves"].items():
            if d["n_pos"] == 0:
                continue
            print(f"   {half:7s} (pos {d['n_pos']}): Haiku BELIEVED {d['haiku_believed']['auroc']:.4f} [{d['haiku_believed']['item_ci']['ci_lo']:.4f},{d['haiku_believed']['item_ci']['ci_hi']:.4f}]/[{d['haiku_believed']['persona_ci']['ci_lo']:.4f},{d['haiku_believed']['persona_ci']['ci_hi']:.4f}]"
                  f" | truthful {d['haiku_truthful']['auroc']:.4f} | lookup {d['lookup_believed']['auroc']:.4f} [{d['lookup_believed']['item_ci']['ci_lo']:.4f},{d['lookup_believed']['item_ci']['ci_hi']:.4f}]"
                  f" | BELIEVED minus truthful {d['believed_minus_truthful']['delta']:+.4f} [{d['believed_minus_truthful']['item_ci']['ci_lo']:+.4f},{d['believed_minus_truthful']['item_ci']['ci_hi']:+.4f}]/[{d['believed_minus_truthful']['persona_ci']['ci_lo']:+.4f},{d['believed_minus_truthful']['persona_ci']['ci_hi']:+.4f}]"
                  f" | Haiku minus lookup {d['haiku_minus_lookup']['delta']:+.4f}")
    write_ledger()


# ------------------------------------------------------------------ ledger
def write_ledger():
    L = []; w = L.append
    b = jload(BUILD / "build_bh.json") if (BUILD / "build_bh.json").exists() else None
    pr = jload(BUILD / "probes.json") if (BUILD / "probes.json").exists() else {}
    w("# NUMBERS_BELIEVED_H.md: ADDENDUM_BELIEVED_H (R-A), Haiku 4.5 under the store's own metadata")
    w("")
    w(f"Registration `registrations/ADDENDUM_BELIEVED_H.md`, registered text sha256 `{REG_SHA}` (the bytes above the marker line), frozen at `257a090` on 2026-09-14. Descriptive: no prediction, no bar, no verdict. Every number for this addendum enters the manuscript through a key in this file and no other way. Written by `believed_h/tools/run_bh.py`; sections 1 to 3 before the first call.")
    w("")
    if b:
        w("## 1. AUX-BH-LOCK: the recorded texts, read and never re-rendered")
        w("")
        w(f"`e1_metamemory/indexes_v2.json` sha256 `{b['locks']['indexes_v2.json'][:16]}...` (the committed BELIEVED texts, cap 15); `side_experiments/s2/indexes_s2u.json` sha256 `{b['locks']['indexes_s2u.json'][:16]}...` (the S2-U texts, cap lifted to 100); `r74/x4/cell_661.json` sha256 `{b['locks']['cell_661.json'][:16]}...`; the 661 item-to-key map asserted against `indexes_s2u.json` items (index_key_true = the cell's key; index_key_believed = its `:BELIEVED` form). 661 items, 104 positives. Capped texts {b['census']['capped_chars_mean']:.0f} characters mean, {b['census']['capped_names_per_item_mean']:.2f} superseded names per item; lifted {b['census']['lifted_chars_mean']:.0f} characters, {b['census']['lifted_names_per_item_mean']:.2f} names (max {b['census']['lifted_max']}). Recorded rows read: Haiku 4.5 blind {RECORDED['blind']}, truthful {RECORDED['true']} (AUX-R74-X4-H45-NOK); mini capped {RECORDED['mini_capped']}, lifted {RECORDED['mini_lifted']} (AUX-E1R-BELIEVED-NOK, AUX-SIDE-S2-MINI).")
        w("")
        w("## 2. AUX-BH-LOOKUP-LIFTED: the superseded-names embedding lookup on the lifted list ($0; computed before any call)")
        w("")
        lf = b["lookup"]["lifted"]
        w(f"Capped list (gate): **{b['lookup']['capped']['auroc']:.4f}** = the recorded {RECORDED['lookup_capped']} (AUX-E1R-NB6) through `run_nb6.build` / `emb_scores`. Lifted list: **{lf['auroc']:.4f}**, item [{lf['item_ci']['ci_lo']:.4f}, {lf['item_ci']['ci_hi']:.4f}], persona [{lf['persona_ci']['ci_lo']:.4f}, {lf['persona_ci']['ci_hi']:.4f}] (the same estimator over `index_v3.named_sections` of the S2-U text).")
        w("")
    if pr:
        w("## 3. AUX-BH-PROBE and AUX-BH-PROJECTION (E1.7 rule; printed before submission)")
        w("")
        w("| arm | served | identifier ok | probe in / out tokens | projected calls | projected $ | x1.3 | billed before | headroom | fits |")
        w("|---|---|---|---|---:|---:|---:|---:|---:|---|")
        for arm in ARMS:
            if arm in pr:
                p = pr[arm]
                w(f"| {arm} | `{p['served']}` | {p['identifier_ok']} | {p['in']} / {p['out']} | {p['projection']['calls']} | {p['projection']['usd']:.4f} | {p['projection']['usd_x1.3']:.4f} | {p['billed_before']:.4f} | {p['headroom']:.4f} | {p['fits']} |")
        w("")
    subs = []
    for arm in ARMS:
        bp = ROWS / arm / "batch_H45.json"
        if bp.exists():
            m = jload(bp); subs.append(f"{arm}: Batch `{m['id']}`, {m['n']} requests")
    if subs:
        w("## 4. AUX-BH-SUBMISSION")
        w("")
        w("; ".join(subs) + f". Cap ${CAP:.2f}; billed so far (probes and collected rows) ${billed_so_far():.4f}. Rows collect to `believed_h/rows/<arm>/rows_H45.jsonl` on `poll`; AUX-BH-H45-*, -RETENTION-*, -BRANCH and -SPEND fill at `score`.")
        w("")
    sc = jload(BH / "results" / "scores_bh.json") if (BH / "results" / "scores_bh.json").exists() else None
    if sc:
        w("## 5. AUX-BH-H45-LIFTED, AUX-BH-H45-15: Haiku 4.5 under the two renderings (k = 5, X4 collapse; recorded blind %.4f and truthful %.4f reproduced)" % (sc["recorded"]["blind"], sc["recorded"]["true"]))
        w("")
        w("| arm | AUROC | item 95% | persona 95% | minus truthful (item; persona) | minus blind | lookup on the same list | Haiku minus lookup (item; persona) | per state believed / truthful: SUP, RET, EXP | bad rows | $ |")
        w("|---|---:|---|---|---|---:|---:|---|---|---:|---:|")
        for arm, R in sc["arms"].items():
            ps = R["per_state"]
            w(f"| {arm} | **{R['auroc']:.4f}** | [{R['item_ci']['ci_lo']:.4f}, {R['item_ci']['ci_hi']:.4f}] | [{R['persona_ci']['ci_lo']:.4f}, {R['persona_ci']['ci_hi']:.4f}] | {R['minus_true']['delta']:+.4f} ([{R['minus_true']['item_ci']['ci_lo']:+.4f}, {R['minus_true']['item_ci']['ci_hi']:+.4f}]; [{R['minus_true']['persona_ci']['ci_lo']:+.4f}, {R['minus_true']['persona_ci']['ci_hi']:+.4f}]) | {R['minus_blind']['delta']:+.4f} | {R['lookup_auroc']:.4f} | {R['haiku_minus_lookup']['delta']:+.4f} ([{R['haiku_minus_lookup']['item_ci']['ci_lo']:+.4f}, {R['haiku_minus_lookup']['item_ci']['ci_hi']:+.4f}]; [{R['haiku_minus_lookup']['persona_ci']['ci_lo']:+.4f}, {R['haiku_minus_lookup']['persona_ci']['ci_hi']:+.4f}]) | {ps['SUPERSESSION']['believed']:.4f} / {ps['SUPERSESSION']['true']:.4f}, {ps['RETRACTION']['believed']:.4f} / {ps['RETRACTION']['true']:.4f}, {ps['EXPIRY']['believed']:.4f} / {ps['EXPIRY']['true']:.4f} | {R['n_rows_bad']} | {R['usd']:.4f} |")
        w("")
        w("## 6. AUX-BH-RETENTION-LIFTED, AUX-BH-RETENTION-15: retention = (BELIEVED minus blind) / (truthful minus blind), the ratio of the paired resampled differences")
        w("")
        w("| arm | retention | item 95% (discarded draws) | persona 95% (discarded draws) |")
        w("|---|---:|---|---|")
        for arm, R in sc["arms"].items():
            r = R["retention"]
            w(f"| {arm} | **{r['point']:.4f}** | [{r['item']['ci_lo']:.4f}, {r['item']['ci_hi']:.4f}] ({r['item']['discarded']}) | [{r['persona']['ci_lo']:.4f}, {r['persona']['ci_hi']:.4f}] ({r['persona']['discarded']}) |")
        w("")
        b_ = sc["branch"]
        w(f"### AUX-BH-BRANCH: retention {b_['retention_lifted']:.4f} lifted, {b_['retention_capped']:.4f} capped: **{b_['fires']}**; {b_['abstract']}. The sixty-percent line is the main-study preregistration's (2026-08-10, report-only), inherited unchanged; no reason for the value was recorded.")
        w("")
        w(f"### AUX-BH-SPEND: {json.dumps(sc['spend'])}")
        w("")
    sp = jload(BH / "results" / "split_bh.json") if (BH / "results" / "split_bh.json").exists() else None
    if sp:
        w(f"## 7. AUX-BH-SPLIT: the {sp['n_supersession_obligations']} supersession obligations split by whether the item's own scrubbed name survives in the BELIEVED list (the author's follow-up of 2026-09-14; $0; each half against the same {sp['n_negatives']} negatives)")
        w("")
        w("| rendering | half | positives | Haiku BELIEVED (item; persona) | Haiku truthful | lookup on the BELIEVED list (item) | BELIEVED minus truthful (item; persona) | Haiku minus lookup (item; persona) |")
        w("|---|---|---:|---|---:|---|---|---|")
        for arm, R in sp["arms"].items():
            for half, d in R["halves"].items():
                if d["n_pos"] == 0:
                    w(f"| {arm} | {half} | 0 | | | | | |"); continue
                hb, ht, lk_ = d["haiku_believed"], d["haiku_truthful"], d["lookup_believed"]; bt, hl = d["believed_minus_truthful"], d["haiku_minus_lookup"]
                w(f"| {arm} | {half} | {d['n_pos']} | **{hb['auroc']:.4f}** ([{hb['item_ci']['ci_lo']:.4f}, {hb['item_ci']['ci_hi']:.4f}]; [{hb['persona_ci']['ci_lo']:.4f}, {hb['persona_ci']['ci_hi']:.4f}]) | {ht['auroc']:.4f} | {lk_['auroc']:.4f} ([{lk_['item_ci']['ci_lo']:.4f}, {lk_['item_ci']['ci_hi']:.4f}]) | {bt['delta']:+.4f} ([{bt['item_ci']['ci_lo']:+.4f}, {bt['item_ci']['ci_hi']:+.4f}]; [{bt['persona_ci']['ci_lo']:+.4f}, {bt['persona_ci']['ci_hi']:+.4f}]) | {hl['delta']:+.4f} ([{hl['item_ci']['ci_lo']:+.4f}, {hl['item_ci']['ci_hi']:+.4f}]; [{hl['persona_ci']['ci_lo']:+.4f}, {hl['persona_ci']['ci_hi']:+.4f}]) |")
        w("")
    io.open(BH / "NUMBERS_BELIEVED_H.md", "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        cmd_build()
    elif cmd in ("probe", "submit", "poll"):
        globals()["cmd_" + cmd](sys.argv[2])
    elif cmd == "score":
        cmd_score()
    elif cmd == "split":
        cmd_split()
    else:
        raise SystemExit("usage: run_bh.py build | probe <arm> | submit <arm> | poll <arm>")
