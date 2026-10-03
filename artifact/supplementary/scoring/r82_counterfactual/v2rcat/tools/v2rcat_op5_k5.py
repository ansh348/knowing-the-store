# -*- coding: utf-8 -*-
"""v2rcat_op5_k5.py -- ADDENDUM_V2R_CAT Amendment 1 (E1, program R117): Opus 5 draws 2 to 5 on the moved-count texts, through Message
Batches exactly like the recorded draw 1 (claude-opus-5, temperature unset, max_tokens 1024, Batch x0.5), appended to rows/rows_OP5.jsonl;
the five-draw collapse (mean over >= 3 OK draws, the X4 rule) against the recorded five-draw v2 row (AUX-CF2-OP5-V2 0.8405); P-M1.
Registration registrations/ADDENDUM_V2R_CAT_AMENDMENT_1.md, registered-text sha256 30d102ed..., frozen at 177697a. Cap 22 USD.

Subcommands, in the registered order:  lock | submit | poll | score
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import v2rcat as V                                                           # noqa: E402  (re-points run_cf to the V2R-CAT cell)
import run_cf as RC                                                          # noqa: E402
import score_cf as S                                                         # noqa: E402
from common_e1r import auroc                                                 # noqa: E402
from cf2_score import paired                                                 # noqa: E402

LANE, CODE = "claude-opus-5", "OP5"
REG = ROOT / "registrations" / "ADDENDUM_V2R_CAT_AMENDMENT_1.md"
REG_SHA = "30d102eddbb9166d3c505871818ab255807ec68f0a9c3962438aeba1ac850d0e"
FROZEN_AT = "177697a"
CAP = 22.00
DRAWS = (2, 3, 4, 5)
OP5_V2_GATE = 0.8405
PER_CALL_EXPECTED = 0.00909      # the recorded draw-1 Batch rows (388), AUX-V2RCAT-OP5
LOCK = V.ROWS / "lock_op5_k5.json"
BATCH = V.ROWS / "batch_OP5_k5.json"
ROWS = V.ROWS / f"rows_{CODE}.jsonl"
OUT = V.RES / "scores_v2rcat_op5_k5.json"
LEDGER = V.V2C / "NUMBERS_V2RCAT.md"
TOL = 0.05


def reg_sha():
    b = REG.read_bytes(); i = b.find(V.FROZEN_END); assert i > 0
    return hashlib.sha256(b[:i]).hexdigest()


def setup():
    assert reg_sha() == REG_SHA, "REGISTRATION SHA MISMATCH -- STOP"
    assert V.registration_ok(); V.point()                       # the parent registration and the texts lock
    RC.LANES[LANE]["k"] = 5
    RC.load_env()
    rows = [json.loads(l) for l in io.open(ROWS, encoding="utf-8")]
    d1 = [r for r in rows if int(r["draw"]) == 1 and r["arm"] == V.ARM]
    assert len(d1) == 444 and all(r["status"] == "OK" for r in d1), "the recorded draw 1 is not the 444 OK rows"
    return rows


def cmd_lock():
    rows = setup()
    texts_sha = hashlib.sha256((V.BUILD / "texts_v2rcat.json").read_bytes()).hexdigest()
    rec = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "parent_registration_sha256": V.REG_SHA,
           "texts_v2rcat_sha256": texts_sha, "recorded_draw1_rows": 444, "lane": LANE, "k": 5, "draws_to_run": list(DRAWS), "max_tokens": RC.LANES[LANE]["max_tokens"],
           "temperature": RC.LANES[LANE]["temp"], "batch_mult": RC.LANES[LANE]["mult"], "cap_usd": CAP, "when": dt.datetime.now().isoformat(timespec="seconds")}
    V.jdump(rec, LOCK); print(json.dumps(rec, indent=1))


def cmd_submit():
    setup()
    assert LOCK.exists(), "lock first"
    assert not BATCH.exists(), "a k5 batch record exists -- STOP (nothing is overwritten)"
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    cfg = RC.LANES[LANE]
    units = V.units(V.ARM)
    n = len(units) * len(DRAWS)
    exp = n * PER_CALL_EXPECTED
    print(f"projection: {n} calls x ${PER_CALL_EXPECTED} = ${exp:.2f}; x1.3 ${exp * 1.3:.2f} against the cap ${CAP}")
    assert exp * 1.3 <= CAP, "projection over the cap -- STOP"
    reqs = []
    for i, u in enumerate(units):
        sysm, user = RC.prompts_for(u, V.ARM)
        for d in DRAWS:
            kw = dict(model=LANE, max_tokens=cfg["max_tokens"], system=sysm, messages=[{"role": "user", "content": user}])
            if cfg["temp"] is not None:
                kw["temperature"] = cfg["temp"]
            reqs.append(Request(custom_id=f"{CODE}-0-{i:04d}-d{d}", params=MessageCreateParamsNonStreaming(**kw)))
    assert len(reqs) == 1776
    b = RC.anthropic_client().messages.batches.create(requests=reqs)
    V.jdump({"id": b.id, "lane": LANE, "n": len(reqs), "draws": list(DRAWS), "submitted": dt.datetime.now().isoformat(timespec="seconds")}, BATCH)
    print("submitted", b.id, len(reqs), "requests")


def cmd_poll():
    setup()
    meta = V.jload(BATCH)
    cl = RC.anthropic_client()
    b = cl.messages.batches.retrieve(meta["id"])
    print(meta["id"], b.processing_status, b.request_counts)
    if b.processing_status != "ended":
        return
    if meta.get("collected"):
        print("already collected"); return
    cfg = RC.LANES[LANE]
    units = V.units(V.ARM)
    done = {(json.loads(l)["unit_id"], int(json.loads(l)["draw"])) for l in io.open(ROWS, encoding="utf-8")}
    n_ok = n_bad = n_skip = 0
    spend = 0.0
    with io.open(ROWS, "a", encoding="utf-8", newline="\n") as f:
        for res in cl.messages.batches.results(meta["id"]):
            code, ai, i, d = res.custom_id.split("-")
            u = units[int(i)]; draw = int(d[1:])
            if (u["unit_id"], draw) in done:
                n_skip += 1; continue
            if res.result.type == "succeeded":
                m = res.result.message
                text = "".join(bl.text for bl in m.content if bl.type == "text")
                row = RC.make_row(u, V.ARM, LANE, draw, text, m.usage.input_tokens, m.usage.output_tokens, cfg["price"], cfg["mult"], m.model)
                assert LANE in row["served_model"], "SERVED IDENTIFIER MISMATCH -- STOP"
                n_ok += 1; spend += row["usd"]
            else:
                row = {"unit_id": u["unit_id"], "arm": V.ARM, "model": LANE, "draw": draw, "status": "BATCH_" + res.result.type.upper()}
                n_bad += 1
            row["batch_id"] = meta["id"]
            f.write(json.dumps(row, sort_keys=True) + "\n")
    meta.update({"collected": dt.datetime.now().isoformat(timespec="seconds"), "ok": n_ok, "not_ok": n_bad, "skipped_duplicates": n_skip, "usd": round(spend, 4)})
    V.jdump(meta, BATCH)
    print(f"collected: ok {n_ok}, not ok {n_bad}, skipped {n_skip}, ${spend:.4f}")


def cmd_score():
    setup(); sys.stdout.reconfigure(encoding="utf-8")
    b = V.jload(V.BUILD / "build_v2rcat.json"); ref = b["reference_readers"]
    y = np.array([it["y_nok"] for it in V.CELL], int); g = np.array([it["persona"] for it in V.CELL]); st = np.array([it["state"] for it in V.CELL])
    rec = S.load_lane(CODE)
    v2 = np.array([rec[(it["item_id"], "INDEXED-V2")] for it in V.CELL], float)
    a2 = round(float(auroc(v2, y)), 4); assert a2 == OP5_V2_GATE, ("GATE: the recorded Opus v2 row", a2)
    # the rows of this arm: per unit, draws -> nok
    per = defaultdict(dict); usd = 0.0; n_bad = 0; batches = Counter()
    for line in io.open(ROWS, encoding="utf-8"):
        r = json.loads(line)
        if r["arm"] != V.ARM:
            continue
        usd += r.get("usd", 0.0); batches[r.get("batch_id", "?")] += 1
        if r.get("status") == "OK" and r.get("nok") is not None:
            per[r["unit_id"]][int(r["draw"])] = float(r["nok"])
        else:
            n_bad += 1
    draws_per = Counter(len(d) for d in per.values())
    excluded = [u for u, d in per.items() if len(d) < S.MIN_DRAWS]
    mean5 = {u: float(np.mean(list(d.values()))) for u, d in per.items() if len(d) >= S.MIN_DRAWS}
    d1 = {u: d[1] for u, d in per.items() if 1 in d}
    nv = np.array([mean5.get(it["item_id"], np.nan) for it in V.CELL], float)
    n1 = np.array([d1.get(it["item_id"], np.nan) for it in V.CELL], float)
    ok = ~np.isnan(nv)
    assert ok.all(), ("items without >= 3 draws", int((~ok).sum()))
    M = {"k": 5, "draws_per_item": dict(draws_per), "excluded_lt_min_draws": len(excluded), "n_rows_bad": n_bad, "rows_per_batch": dict(batches), "usd_all_rows": round(usd, 4),
         "v2_recorded_k5": a2, "v2rcat_k5": round(float(auroc(nv, y)), 4), "v2rcat_k1_recorded": round(float(auroc(n1, y)), 4),
         "minus_v2": paired(v2, nv, y, g), "draw_effect_k5_minus_k1": paired(n1, nv, y, g), "per_state": {}}
    for s_ in V.STATES:
        m = st == s_
        pd = paired(v2[m], nv[m], y[m], g[m])
        inside = bool(-TOL <= pd["item_ci"]["ci_lo"] and pd["item_ci"]["ci_hi"] <= TOL and -TOL <= pd["persona_ci"]["ci_lo"] and pd["persona_ci"]["ci_hi"] <= TOL)
        beyond = bool(abs(pd["delta"]) > TOL and ((pd["item_ci"]["ci_hi"] < -TOL and pd["persona_ci"]["ci_hi"] < -TOL) or (pd["item_ci"]["ci_lo"] > TOL and pd["persona_ci"]["ci_lo"] > TOL)))
        reliable_neg = bool(pd["delta"] < 0 and pd["item_ci"]["ci_hi"] < 0 and pd["persona_ci"]["ci_hi"] < 0)
        M["per_state"][s_] = {"n": int(m.sum()), "pos": int(y[m].sum()), "v2": round(float(auroc(v2[m], y[m])), 4), "v2rcat_k1": round(float(auroc(n1[m], y[m])), 4),
                              "v2rcat_k5": round(float(auroc(nv[m], y[m])), 4), **pd, "inside_band_both": inside, "beyond_band_both": beyond, "reliable_negative": reliable_neg}
    pm1 = all(M["per_state"][s_]["reliable_negative"] for s_ in ("RETRACTION", "EXPIRY"))
    failing = [s_ for s_ in ("RETRACTION", "EXPIRY") if not M["per_state"][s_]["reliable_negative"]]
    def fmt(s_):
        d = M["per_state"][s_]
        return f"{d['delta']:+.4f} with intervals [{d['item_ci']['ci_lo']:+.4f}, {d['item_ci']['ci_hi']:+.4f}] and [{d['persona_ci']['ci_lo']:+.4f}, {d['persona_ci']['ci_hi']:+.4f}]"
    verdict = ("P-M1 HOLDS: at five draws the moved-count movement of Opus 5 replicates on retraction (" + fmt("RETRACTION") + ") and on expiry (" + fmt("EXPIRY") + "), both differences negative with both intervals excluding zero."
               if pm1 else
               "P-M1 FAILS. At five draws the moved-count movement of Opus 5 does not replicate on " + (" / ".join(s.lower() for s in failing) if len(failing) == 1 else "both") + ": the difference is " + "; ".join(f"{s.lower()} {fmt(s)}" for s in failing) + ".")
    spend_new = sum(json.loads(l).get("usd", 0.0) for l in io.open(ROWS, encoding="utf-8") if int(json.loads(l)["draw"]) in DRAWS)
    res = {"registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "lock": V.jload(LOCK), "batch": V.jload(BATCH), "model": LANE, "n": 444, "pos": 148, "tol": TOL,
           "opus_k5": M, "P-M1": {"holds": pm1, "text": verdict}, "spend_draws_2_to_5_usd": round(spend_new, 4), "cap_usd": CAP, "when": dt.datetime.now().isoformat(timespec="seconds")}
    V.jdump(res, OUT)
    def cell(s_):
        d = M["per_state"][s_]
        return f"{d['v2']:.4f} -> {d['v2rcat_k5']:.4f} (k = 1: {d['v2rcat_k1']:.4f}), {d['delta']:+.4f} ([{d['item_ci']['ci_lo']:+.4f}, {d['item_ci']['ci_hi']:+.4f}]; [{d['persona_ci']['ci_lo']:+.4f}, {d['persona_ci']['ci_hi']:+.4f}]), {'inside' if d['inside_band_both'] else ('beyond' if d['beyond_band_both'] else 'neither')}"
    mv, de = M["minus_v2"], M["draw_effect_k5_minus_k1"]
    txt = (f"\n## 9. AUX-V2RCAT-A1: Amendment 1 (E1, program R117) -- Opus 5 at five draws on the moved-count texts (registrations/ADDENDUM_V2R_CAT_AMENDMENT_1.md, registered text sha256 `{REG_SHA[:16]}...`, frozen at `{FROZEN_AT}`; `tools/v2rcat_op5_k5.py`; `rows/rows_OP5.jsonl` draws 2 to 5, `rows/batch_OP5_k5.json`, `rows/lock_op5_k5.json`; `results/scores_v2rcat_op5_k5.json`)\n\n"
           f"### AUX-V2RCAT-A1-LOCK\n\nRegistration sha256 holds; the parent registration and the texts lock re-asserted; draws 2 to 5 through Message Batches like the recorded draw 1 (`claude-opus-5`, temperature unset, `max_tokens` 1024, x0.5). Rows per batch: {dict(batches)}; draws per item {dict(draws_per)}; rows not OK {n_bad}; items excluded (< 3 draws) {len(excluded)}.\n\n"
           f"### AUX-V2RCAT-A1-OP5-K5\n\n| reader | k | v2 (recorded, k = 5) | V2R-CAT (k = 5) | V2R-CAT (k = 1, recorded) | whole minus v2 (item; persona) | SUP v2 -> V2R-CAT | RET v2 -> V2R-CAT, delta (item; persona), band | EXP v2 -> V2R-CAT, delta (item; persona), band |\n|---|---:|---:|---:|---:|---|---|---|---|\n"
           f"| claude-opus-5 | 5 | {a2:.4f} | **{M['v2rcat_k5']:.4f}** | {M['v2rcat_k1_recorded']:.4f} | {mv['delta']:+.4f} ([{mv['item_ci']['ci_lo']:+.4f}, {mv['item_ci']['ci_hi']:+.4f}]; [{mv['persona_ci']['ci_lo']:+.4f}, {mv['persona_ci']['ci_hi']:+.4f}]) | {M['per_state']['SUPERSESSION']['v2']:.4f} -> {M['per_state']['SUPERSESSION']['v2rcat_k5']:.4f}, {M['per_state']['SUPERSESSION']['delta']:+.4f} | {cell('RETRACTION')} | {cell('EXPIRY')} |\n\n"
           f"### AUX-V2RCAT-A1-DRAW-EFFECT\n\nThe five-draw row minus the recorded draw-1 row, whole set: {de['delta']:+.4f} ([{de['item_ci']['ci_lo']:+.4f}, {de['item_ci']['ci_hi']:+.4f}]; [{de['persona_ci']['ci_lo']:+.4f}, {de['persona_ci']['ci_hi']:+.4f}]).\n\n"
           f"### AUX-V2RCAT-A1-P-M1\n\n**{verdict}**\n\n"
           f"### AUX-V2RCAT-A1-SPEND\n\nDraws 2 to 5: ${spend_new:.4f} (Batch-priced from the returned tokens at $5 / $25 per million x 0.5) against the cap of ${CAP:.0f}; the recorded draw 1 stays at $4.5022.\n")
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    {"lock": cmd_lock, "submit": cmd_submit, "poll": cmd_poll, "score": cmd_score}[sys.argv[1]]()
