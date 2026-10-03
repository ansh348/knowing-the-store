# -*- coding: utf-8 -*-
"""v2rcat_op5.py -- ADDENDUM_V2R_CAT section 4's optional Opus 5 lane, run under the author's instruction of 2026-09-17 (program R114;
D-V2RCAT-2). k = 1 (the registered default; temperature unset, max_tokens 1024, Message Batches, the CF-3 protocol), 444 requests on
the V2R-CAT texts; the comparator is the recorded CF-2 Opus v2 row at k = 5 (AUX-CF2-OP5-V2 0.8405, disclosed beside the row).
v2rcat.py, run_cf.py, score_cf.py and cf2_score.py are imported, not edited; the lane's cap is this pass's ceiling (the addendum
places the lane "outside the $4"), asserted against the R114 running total before submission. New files only: rows/batch_OP5.json,
rows/rows_OP5.jsonl, results/scores_v2rcat_op5.json; NUMBERS_V2RCAT.md gains section 8 (appended; sections 1 to 7 untouched).

Subcommands:  probe | submit | poll | score
"""
from __future__ import annotations

import datetime as dt
import io
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "r114" / "tools"))
from r114_common import assert_spec, J, jdump, r4, CEILING  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
import v2rcat as V                                                           # noqa: E402
import run_cf as RC                                                          # noqa: E402
import score_cf as S                                                         # noqa: E402
from common_e1r import auroc                                                 # noqa: E402
from cf2_score import paired                                                 # noqa: E402

LANE = "claude-opus-5"
CODE = "OP5"
LEDGER = V.V2C / "NUMBERS_V2RCAT.md"
OP5_V2_GATE = 0.8405            # AUX-CF2-OP5-V2, the recorded k = 5 row on the 444
CF3_ANCHOR_PER_CALL = 0.00872   # AUX-CF3-SPEND: $1.2208 / 140 rows
TOL = 0.05


def setup():
    assert_spec(); assert V.registration_ok(); V.point()
    RC.LANES[LANE]["k"] = 1                                     # section 4: k = 1 by default
    RC.load_env()
    dev = (V.V2C / "DEVIATIONS_V2RCAT.md").read_text(encoding="utf-8")
    assert "D-V2RCAT-2" in dev, "D-V2RCAT-2 not recorded -- STOP"
    lk = J(V.RES / "leakscreen_v2rcat.json"); assert not lk["leaked"]


def r114_billed_so_far():
    """The pass's running total from the rows files of every phase (the spend keys of NUMBERS_R114 are written from the same files)."""
    tot = 0.0
    for p in (ROOT / "ds_downstream/run/rows_ds_r114_mini.jsonl", ROOT / "ds_downstream/run/rows_ds_r114_h45.jsonl", ROOT / "r85_graphiti/g10/rows_summary.jsonl",
              ROOT / "r85_graphiti/g10/rows_view.jsonl", ROOT / "r85_graphiti/a2/rows_a2_mini.jsonl"):
        if p.exists():
            tot += sum(json.loads(l).get("usd", 0.0) for l in io.open(p, encoding="utf-8"))
    for p in (ROOT / "ds_downstream/run/probes_r114.json", ROOT / "r85_graphiti/g10/probes_summary.json", ROOT / "r85_graphiti/g10/probes_view.json", ROOT / "r85_graphiti/a2/probes_a2.json"):
        if p.exists():
            tot += sum(v["usd"] for v in J(p).values())
    tot += J(ROOT / "r85_graphiti/g10/leak30_g10.json")["usd"] + J(ROOT / "r85_graphiti/g10/retrieval_raw_g10.json")["meta"]["usd"]
    return tot


def cmd_probe():
    setup()
    u = V.units(V.ARM)[0]
    r = RC.call_once(LANE, u, V.ARM, 0)
    ok = LANE in r["served_model"] or LANE.split("-2025")[0] in r["served_model"]
    cfg = RC.LANES[LANE]; n = cfg["k"] * len(V.CELL)
    ratio = r["tok_in"] / max(1, len(u["index"]))
    tin = sum(int(len(x["index"]) * ratio) for x in V.units(V.ARM)) * cfg["k"]; tout = n * max(1, r["tok_out"])
    usd = (tin / 1e6 * cfg["price"][0] + tout / 1e6 * cfg["price"][1]) * cfg["mult"]
    billed = r114_billed_so_far() + r["usd"]; headroom = CEILING - billed
    rec = {"lane": LANE, "k": cfg["k"], "served": r["served_model"], "identifier_ok": ok, "in": r["tok_in"], "out": r["tok_out"], "parsed": r["status"], "probe_usd": r["usd"],
           "projection": {"calls": n, "input_tokens": tin, "output_tokens": tout, "usd": round(usd, 4), "usd_x1.3": round(usd * 1.3, 4), "cf3_anchor_usd": round(n * CF3_ANCHOR_PER_CALL, 4)},
           "r114_billed_before": round(billed, 4), "r114_ceiling": CEILING, "headroom": round(headroom, 4), "fits": bool(ok and usd * 1.3 <= headroom), "sample": r["text"][:200], "when": dt.datetime.now().isoformat(timespec="seconds")}
    d = J(RC.PROBES) if RC.PROBES.exists() else {}
    d[LANE] = rec; jdump(d, RC.PROBES)
    print(json.dumps({k: v for k, v in rec.items() if k != "sample"}, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")
    if not rec["fits"]:
        raise SystemExit("the x1.3 projection exceeds the R114 headroom -- do not launch")


def cmd_submit():
    setup(); pr = J(RC.PROBES)[LANE]; assert pr["identifier_ok"] and pr["fits"] and pr["k"] == 1
    assert not (V.ROWS / f"batch_{CODE}.json").exists() and not (V.ROWS / f"rows_{CODE}.jsonl").exists(), "an Opus batch or rows file already exists -- STOP (nothing is overwritten)"
    RC.cmd_submit(LANE)
    b = J(V.ROWS / f"batch_{CODE}.json"); assert b["n"] == 444, b


def cmd_poll():
    setup()
    if (V.ROWS / f"rows_{CODE}.jsonl").exists():
        print("rows already collected"); return
    RC.cmd_poll(LANE)


def cmd_score():
    setup(); sys.stdout.reconfigure(encoding="utf-8")
    assert (V.ROWS / f"rows_{CODE}.jsonl").exists(), "no Opus rows -- poll first"
    b = J(V.BUILD / "build_v2rcat.json"); ref = b["reference_readers"]
    y = np.array([it["y_nok"] for it in V.CELL], int); g = np.array([it["persona"] for it in V.CELL]); st = np.array([it["state"] for it in V.CELL])
    rec = S.load_lane(CODE)
    v2 = np.array([rec[(it["item_id"], "INDEXED-V2")] for it in V.CELL], float)
    a2 = round(float(auroc(v2, y)), 4); assert a2 == OP5_V2_GATE, ("GATE: the recorded Opus v2 row", a2)
    v2r_rec = np.array([rec[(it["item_id"], "INDEXED-V2R")] for it in V.CELL], float)
    newd, n_bad, usd = V.load_new(CODE)
    nv = np.array([newd.get(it["item_id"], np.nan) for it in V.CELL], float)
    missing = int(np.isnan(nv).sum()); assert missing == 0, ("items without a score", missing)
    M = {"n_rows_bad": n_bad, "usd": round(usd, 4), "k": 1, "k_of_recorded_v2": 5, "v2_recorded": a2, "v2r_recorded_totals_randomized": round(float(auroc(v2r_rec, y)), 4), "v2rcat": round(float(auroc(nv, y)), 4),
         "minus_v2": paired(v2, nv, y, g), "minus_v2r": paired(v2r_rec, nv, y, g), "per_state": {}, "vs_reference": {}}
    for s_ in V.STATES:
        m = st == s_
        pd = paired(v2[m], nv[m], y[m], g[m])
        inside = bool(-TOL <= pd["item_ci"]["ci_lo"] and pd["item_ci"]["ci_hi"] <= TOL and -TOL <= pd["persona_ci"]["ci_lo"] and pd["persona_ci"]["ci_hi"] <= TOL)
        beyond = bool(abs(pd["delta"]) > TOL and ((pd["item_ci"]["ci_hi"] < -TOL and pd["persona_ci"]["ci_hi"] < -TOL) or (pd["item_ci"]["ci_lo"] > TOL and pd["persona_ci"]["ci_lo"] > TOL)))
        M["per_state"][s_] = {"n": int(m.sum()), "pos": int(y[m].sum()), "v2": round(float(auroc(v2[m], y[m])), 4), "v2r": round(float(auroc(v2r_rec[m], y[m])), 4), "v2rcat": round(float(auroc(nv[m], y[m])), 4),
                              **pd, "inside_band_both": inside, "beyond_band_both": beyond, "point_within_band": bool(abs(pd["delta"]) <= TOL)}
    cr = ref["CR-oracle-state-cell under V2R-CAT"]
    for s_ in ("RETRACTION", "EXPIRY"):
        M["vs_reference"][s_] = {"model": M["per_state"][s_]["v2rcat"], "CR-oracle-state-cell": cr["per_state"][s_]["auroc"], "CR-totals": ref["CR-totals under V2R-CAT (= v2r)"]["per_state"][s_]["auroc"]}
    moved = [s_ for s_ in ("RETRACTION", "EXPIRY") if M["per_state"][s_]["beyond_band_both"]]
    within = all(M["per_state"][s_]["inside_band_both"] for s_ in ("RETRACTION", "EXPIRY"))
    point_within = all(M["per_state"][s_]["point_within_band"] for s_ in ("RETRACTION", "EXPIRY"))
    M["branch"] = {"within_band_both_states": within, "moved_beyond_band": moved, "point_within_band_both_states": point_within,
                   "reading": ("stays within 0.05 of its v2 row on both counted states (both intervals inside the band)" if within else
                               ("reads the per-category tally on " + ", ".join(moved) if moved else "neither inside the band on both states nor beyond it with both intervals: printed as it came out"))}
    pr = J(RC.PROBES)[LANE]
    b2 = V.ROWS / f"batch_{CODE}_2.json"
    rows_all = [json.loads(l) for l in io.open(V.ROWS / f"rows_{CODE}.jsonl", encoding="utf-8")]
    from collections import Counter
    by_batch = Counter(r.get("batch_id", "?") for r in rows_all if r["status"] == "OK")
    batches = (f" over three delivery paths (D-V2RCAT-3, D-V2RCAT-4): `{J(V.ROWS / f'batch_{CODE}.json')['id']}` canceled at the author's instruction after 388 had succeeded, `{J(b2)['id']}` (the 56 resubmitted) canceled after 5 had succeeded, the remaining 51 synchronous at list price; OK rows per path {dict(by_batch)}" if b2.exists() else f" (`{J(V.ROWS / f'batch_{CODE}.json')['id']}`)")
    res = {"registration_sha256": V.REG_SHA, "batches": batches, "deviation": "D-V2RCAT-2", "model": LANE, "served": sorted({json.loads(l).get("served_model") for l in io.open(V.ROWS / f"rows_{CODE}.jsonl", encoding="utf-8") if json.loads(l).get("status") == "OK"}),
           "n": 444, "pos": 148, "tol": TOL, "opus": M, "spend": {"probe": pr["probe_usd"], "lane": round(usd, 4), "total": round(usd + pr["probe_usd"], 4)}, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(res, V.RES / "scores_v2rcat_op5.json")
    def cell(s_):
        d = M["per_state"][s_]
        return f"{d['v2']:.4f} -> {d['v2rcat']:.4f}, {d['delta']:+.4f} ([{d['item_ci']['ci_lo']:+.4f}, {d['item_ci']['ci_hi']:+.4f}]; [{d['persona_ci']['ci_lo']:+.4f}, {d['persona_ci']['ci_hi']:+.4f}]), {'inside' if d['inside_band_both'] else ('beyond' if d['beyond_band_both'] else 'neither')}"
    mv = M["minus_v2"]; mr = M["minus_v2r"]
    txt = (f"\n## 8. AUX-V2RCAT-OP5 — the optional Opus 5 lane, run 2026-09-17 under the author's instruction (program R114; D-V2RCAT-2; `tools/v2rcat_op5.py`; `rows/rows_OP5.jsonl`, `rows/batch_OP5.json`; `results/scores_v2rcat_op5.json`; sections 1 to 7 above unchanged, the section 6 dash superseded by this row)\n\n"
           f"`claude-opus-5`, served {res['served']}, k = **1** (the registered default; temperature unset, `max_tokens` 1024, Message Batches at the 0.5 multiplier), 444 requests{batches}, {n_bad} not OK, ${usd:.4f} (probe ${pr['probe_usd']:.4f}). The comparator is the recorded CF-2 Opus v2 row at **k = 5** (AUX-CF2-OP5-V2 {a2}, X4 collapse), disclosed here as section 4 requires; the recorded totals-randomized row (v2r, k = 5) prints beside as a distinct construction.\n\n"
           f"| reader | k | v2 (recorded, k = 5) | v2r totals-randomized (recorded, k = 5) | V2R-CAT (k = 1) | whole minus v2 (item; persona) | whole minus v2r (item; persona) | SUP v2 -> V2R-CAT | RET v2 -> V2R-CAT, delta (item; persona), band | EXP v2 -> V2R-CAT, delta (item; persona), band | bad rows | $ |\n|---|---:|---:|---:|---:|---|---|---|---|---|---:|---:|\n"
           f"| claude-opus-5 | 1 | {a2:.4f} | {M['v2r_recorded_totals_randomized']:.4f} | **{M['v2rcat']:.4f}** | {mv['delta']:+.4f} ([{mv['item_ci']['ci_lo']:+.4f}, {mv['item_ci']['ci_hi']:+.4f}]; [{mv['persona_ci']['ci_lo']:+.4f}, {mv['persona_ci']['ci_hi']:+.4f}]) | {mr['delta']:+.4f} ([{mr['item_ci']['ci_lo']:+.4f}, {mr['item_ci']['ci_hi']:+.4f}]; [{mr['persona_ci']['ci_lo']:+.4f}, {mr['persona_ci']['ci_hi']:+.4f}]) | {M['per_state']['SUPERSESSION']['v2']:.4f} -> {M['per_state']['SUPERSESSION']['v2rcat']:.4f}, {M['per_state']['SUPERSESSION']['delta']:+.4f} | {cell('RETRACTION')} | {cell('EXPIRY')} | {n_bad} | {usd:.4f} |\n\n"
           f"The reference readers under the same text (AUX-V2RCAT-REF): the state-cell reader retraction {cr['per_state']['RETRACTION']['auroc']} / expiry {cr['per_state']['EXPIRY']['auroc']}; CR-totals {ref['CR-totals under V2R-CAT (= v2r)']['per_state']['RETRACTION']['auroc']} / {ref['CR-totals under V2R-CAT (= v2r)']['per_state']['EXPIRY']['auroc']}. "
           f"Section 5 branch for this model: **{M['branch']['reading']}** (point estimates within 0.05 on both counted states: {point_within}). The k = 1 against k = 5 comparison carries draw-count noise the two registered lanes did not; the row is disclosed as such and the section 5 reading for the three models is re-stated in the paper only with that disclosure. The author's ruling of 2026-09-15 on the word 'totals' / 'tallies' (below the marker of the addendum) is not re-opened here.\n\n"
           f"### AUX-V2RCAT-SPEND (continued) — Opus 5 lane ${usd:.4f} + probe ${pr['probe_usd']:.4f} = ${usd + pr['probe_usd']:.4f}, outside the $4 cap (D-V2RCAT-2), under the R114 ceiling; the addendum's registered lanes' total $3.2341 is unchanged.\n")
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    {"probe": cmd_probe, "submit": cmd_submit, "poll": cmd_poll, "score": cmd_score}[sys.argv[1]]()
