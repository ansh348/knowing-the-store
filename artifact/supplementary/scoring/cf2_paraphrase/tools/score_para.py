"""score_para.py -- ADDENDUM_PARA §5-§7: the author's sheet, the lanes, the scoring.

Registration: registrations/ADDENDUM_PARA.md (registered text sha256 45cad63d…, frozen at dab8956);
the author's rulings of 2026-09-14 (evening): section 3(a) narrowed to the scrubbed slot name (3(b) unchanged),
cap (ii) $21 with Opus 5 once, the PAD Amendment 1 Haiku lane regardless of the x1.3 rule, overall $28.
Descriptive: no prediction, no bar, no verdict; the §7 branches print as they come out.
Amendment of 2026-09-21 (dated line below the marker; whole file 968f9e13…): the author's read excluded 9 of the 124
screen-passing pairs, the floor is amended to the 115 accepted pairs, and one sensitivity analysis is added, labelled
not registered: the same scoring on all 124 screen-passing pairs, reported beside the 115. PARA_POP=all124 in the
environment selects that population (the lanes are submitted once on the 124 pairs' items; the registered scoring
reads the 115's items from those rows; results for the 124 go to *_all124.json).

Subcommands, in order (nothing here runs before `sheet` has ledgered the author's read):
  sheet                  read reviews/v12/PARAPHRASE_READ.md, parse the two verdict columns, ledger its
                         sha256 and the accepted count (AUX-PARA-SHEET), re-run the §3 screen on every
                         accepted paraphrase (STOP on overlap), the locks and the lookup gate on the
                         original questions (AUX-PARA-LOCK) -> cf2_paraphrase/sheet.json
  lookups                both lookups on the paraphrases under v2 and v3, paired against the originals
                         -> cf2_paraphrase/results/lookups.json  ($0)
  probe <lane>           one call per arm on the first accepted pair (served identifier, E1.7) and the
                         projection against the combined headroom -> cf2_paraphrase/probes.json
  sync gpt-4.1-mini      the mini lane (k = 1, synchronous, jsonl resume) -> rows/rows_MINI.jsonl
  submit | poll <lane>   Haiku 4.5 (k = 5) and Opus 5 (k = 1) as Batches -> rows/rows_H45.jsonl, rows_OP5.jsonl
  score                  every reader × summary: AUROC whole and per state, paired paraphrase − original,
                         model − lookup, the §7 branches, AUX-PARA-FLAGS, the author's extra descriptives
                         -> cf2_paraphrase/results/para_scores.json
"""
from __future__ import annotations

import collections
import hashlib
import io
import json
import os
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from para_common import (CF2, PARA, REG_SHA, SHEET, content, forbidden, jdump, jload, locks, lookup_gate,  # noqa: E402
                         pairs, screen, sha256_file)
from index_v3 import named_sections  # noqa: E402
from sweep_common import auroc, boot_cluster, boot_item, emb_cached, lex_cached, state_mask  # noqa: E402

import run_cf as RC  # noqa: E402  (asserts the prompts_e1 digests at import)
import score_cf as S  # noqa: E402

ROWS, RES = PARA / "rows", PARA / "results"
ARMS = ("INDEXED-V2", "INDEXED-V3")
ARM_KEY = {"INDEXED-V2": "v2", "INDEXED-V3": "v3"}
STATES = ("superseded", "retracted", "expired")
TOL = 0.05
FLOOR = 115                           # amended 2026-09-21 from the registered 120 (the dated amendment below the marker)
POP = os.environ.get("PARA_POP", "accepted")   # "accepted" = the 115 (registered); "all124" = the sensitivity, not registered
ADDON_KEYS = ("PAD Amendment 1 H45 lane",)      # the ruling of 2026-09-14 (evening): runs regardless of the x1.3 rule under the $28 overall cap; never displaces a registered lane
ADDED = {"LUNA": {"k": 5, "label": "GPT-5.6 Luna, added 2026-09-21, not registered (v2 only; raw API, Table 1 settings)", "arms": ["INDEXED-V2"]},
         "SOL": {"k": 5, "label": "GPT-5.6 Sol, added 2026-09-21, not registered (v2 only; raw API, Table 1 settings)", "arms": ["INDEXED-V2"]}}
COMBINED_CAP = 15.00
CAP_RAISED = 21.00                    # the author's ruling (ii) of 2026-09-14 (evening): the combined cap is $21 and Opus 5 runs once
OVERALL_CAP = 28.00                   # everything in this pass, the PAD Amendment 1 Haiku lane included (runs regardless of the x1.3 rule)

RC.ROWS = ROWS
RC.PROBES = PARA / "probes.json"
RC.ARMS = ARMS
RC.LANES["claude-opus-5"]["k"] = 1    # §6: Opus 5 k = 1 by the author's instruction (disclosed beside its row)
S.R82 = CF2                           # load_lane reads the RECORDED CF-2 rows


# ------------------------------------------------------------------ the sheet (§5)
ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*([A-Z-]+)\s*\|\s*([A-Z-]+)\s*\|\s*(.*?)\s*\|\s*\*\*(.*?)\*\*\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")


def parse_sheet():
    rows = []
    for ln in io.open(SHEET, encoding="utf-8"):
        m = ROW.match(ln.rstrip("\n"))
        if m:
            n, pid, state, intent, orig, para, c1, c2 = m.groups()
            rows.append({"num": int(n), "pair_id": pid, "state": state, "intent": intent, "question": orig, "paraphrase": para,
                         "same_intent": c1.strip().upper(), "names_value": c2.strip().upper()})
    return rows


def accepted_pairs():
    sh = jload(PARA / "sheet.json")
    keep = {r["pair_id"] for r in sh["rows"] if r["same_intent"] == "YES" or POP == "all124"}
    para = {r["pair_id"]: r["paraphrase"] for r in sh["rows"]}
    out = []
    for pr in pairs():
        if pr["pair_id"] in keep:
            pr = dict(pr)
            pr["paraphrase"] = para[pr["pair_id"]]
            out.append(pr)
    return out


def cmd_sheet():
    L = locks()
    assert L["all_ok"], f"STOP: lock failure {L}"
    rows = parse_sheet()
    assert rows, "no rows parsed from the sheet"
    bad = [r for r in rows if r["same_intent"] not in ("YES", "NO") or r["names_value"] not in ("YES", "NO")]
    if bad:
        raise SystemExit(f"STOP: {len(bad)} rows without a YES / NO in both columns, e.g. {bad[0]['pair_id']}: {bad[0]['same_intent']!r} / {bad[0]['names_value']!r}")
    Q = jload(PARA / "para_questions.json")
    drafted = {r["pair_id"]: r["paraphrase"] for r in Q["rows"] if r["accepted"]}
    assert all(drafted.get(r["pair_id"]) == r["paraphrase"] for r in rows), "STOP: a paraphrase on the sheet differs from the drafted one"
    acc = [r for r in rows if r["same_intent"] == "YES"]
    # the screen re-run on every accepted paraphrase
    P = {pr["pair_id"]: pr for pr in pairs()}
    fails, n_reg = [], 0
    for r in acc:
        F, _ = forbidden(P[r["pair_id"]], "narrowed")          # the ruling of 2026-09-14: §3(a) = the scrubbed slot name; §3(b) unchanged
        ok, hit, same = screen(r["paraphrase"], r["question"], F)
        if not ok:
            fails.append((r["pair_id"], hit, same))
        n_reg += screen(r["paraphrase"], r["question"], forbidden(P[r["pair_id"]], "registered")[0])[0]
    if fails:
        raise SystemExit(f"STOP: {len(fails)} accepted paraphrases fail the screen at scoring time: {fails[:3]}")
    if len(acc) < FLOOR:
        raise SystemExit(f"STOP: {len(acc)} < {FLOOR} accepted after the author's read")
    gate, gate_ok = lookup_gate(pairs())
    if not gate_ok:
        raise SystemExit("STOP: lookup gate on the original questions failed")
    by_state = collections.Counter(r["state"] for r in acc)
    rec = {"sheet_sha256": sha256_file(SHEET), "n_rows": len(rows), "n_accepted": len(acc), "n_excluded_by_author": len(rows) - len(acc),
           "excluded_by_author": [r["pair_id"] for r in rows if r["same_intent"] != "YES"],
           "names_value_yes": sum(1 for r in acc if r["names_value"] == "YES"), "by_state": dict(by_state),
           "floor": FLOOR, "floor_registered": 120, "floor_amended": "2026-09-21 (the dated amendment below the marker; whole file 968f9e13…)",
           "screen_rerun_ok": True, "screen_scope": "narrowed (§3(a) = scrubbed slot name; §3(b) unchanged)", "n_accepted_passing_registered_screen": n_reg, "locks": L, "lookup_gate": gate, "rows": rows}
    jdump(rec, PARA / "sheet.json")
    print(json.dumps({k: v for k, v in rec.items() if k not in ("rows", "locks")}, indent=1))


# ------------------------------------------------------------------ items
def items(P):
    """One row per accepted pair × version (n = 3 × accepted), in the CF-2 cell's item order."""
    rows = []
    for pr in P:
        for it in pr["items"]:
            rows.append({"pop": "cf2", "item_id": it["item_id"], "key": it["item_id"], "pair_id": pr["pair_id"], "persona": pr["persona"],
                         "question": pr["question"], "paraphrase": pr["paraphrase"], "y": int(it["y_nok"]), "version": it["version"],
                         "state": pr["state"].lower().replace("supersession", "superseded").replace("retraction", "retracted").replace("expiry", "expired"),
                         "slot": pr["slot"], "v2": it["v2"], "v3": it["v3"]})
    return rows


def name_lists(rows):
    v2, v3 = {}, {}
    for r in rows:
        s = named_sections(r["v3"])
        v2[r["key"]] = list(named_sections(r["v2"])["superseded"])
        v3[r["key"]] = list(s["superseded"] + s["retracted"] + s["expired"])
    return v2, v3


def paired(base, new, y, g):
    it, cl = boot_item(base, new, y), boot_cluster(base, new, y, g)
    d = float(auroc(new, y) - auroc(base, y))
    wide = it if (it.get("ci_hi", 0) - it.get("ci_lo", 0)) >= (cl.get("ci_hi", 0) - cl.get("ci_lo", 0)) else cl
    return {"delta": d, "ci_item": it, "ci_persona": cl, "both_exclude_zero": bool(it.get("excludes_zero") and cl.get("excludes_zero")),
            "agree": bool(it.get("excludes_zero") == cl.get("excludes_zero")),
            "weaker": {"which": "item" if wide is it else "persona", "ci_lo": wide.get("ci_lo"), "ci_hi": wide.get("ci_hi"), "excludes_zero": wide.get("excludes_zero")}}


def per_state(rows, arr, y):
    return {st: float(auroc(arr[state_mask(rows, st)], y[state_mask(rows, st)])) for st in STATES}


def res_path(base):
    """Result file for the population: lookups.json / para_scores.json for the 115; *_all124.json for the sensitivity."""
    return RES / (base if POP == "accepted" else base.replace(".json", "_all124.json"))


def cmd_lookups():
    assert (PARA / "sheet.json").exists(), "STOP: the author's read is not ledgered"
    P = accepted_pairs()
    rows = items(P)
    y = np.array([r["y"] for r in rows], int); g = np.array([r["persona"] for r in rows])
    v2, v3 = name_lists(rows)
    orig = [dict(r, question=r["question"]) for r in rows]
    para = [dict(r, question=r["paraphrase"]) for r in rows]
    out = {"n": len(rows), "n_pairs": len(P), "n_pos": int(y.sum()), "rows": {}}
    scores = {}
    for lk, fn in (("emb", emb_cached), ("lex", lex_cached)):
        for sv, lists in (("v2", v2), ("v3", v3)):
            o, p = fn(orig, lists), fn(para, lists)
            scores[f"{lk}_{sv}"] = {"orig": o.tolist(), "para": p.tolist()}
            out["rows"][f"{lk}_{sv}"] = {"original": float(auroc(o, y)), "original_per_state": per_state(rows, o, y),
                                         "paraphrase": float(auroc(p, y)), "paraphrase_per_state": per_state(rows, p, y),
                                         "paired": paired(o, p, y, g),
                                         "paired_per_state": {st: paired(o[state_mask(rows, st)], p[state_mask(rows, st)], y[state_mask(rows, st)], g[state_mask(rows, st)]) for st in STATES}}
            r = out["rows"][f"{lk}_{sv}"]
            print(f"{lk} {sv}: original {r['original']:.4f} -> paraphrase {r['paraphrase']:.4f}  d {r['paired']['delta']:+.4f} "
                  f"item [{r['paired']['ci_item']['ci_lo']:+.4f},{r['paired']['ci_item']['ci_hi']:+.4f}] persona [{r['paired']['ci_persona']['ci_lo']:+.4f},{r['paired']['ci_persona']['ci_hi']:+.4f}]")
    out["scores"] = scores
    out["items"] = [{k: r[k] for k in ("item_id", "pair_id", "persona", "y", "state", "version", "question", "paraphrase", "slot")} for r in rows]
    out["population"] = POP
    jdump(out, res_path("lookups.json"))
    print(f"wrote {res_path('lookups.json')} (population {POP}, {len(P)} pairs)")


# ------------------------------------------------------------------ the lanes (run_cf, called)
def units(arm):
    P = accepted_pairs()
    return [{"unit_id": it["item_id"], "question": pr["paraphrase"], "index": it[ARM_KEY[arm]]} for pr in P for it in pr["items"]]


RC.units = units


def billed_so_far():
    """Every lane already billed on the combined cap (metered from the rows / ledgers)."""
    total, parts = 0.0, {}
    pad = PARA.parent / "pad_probe"
    for p, key in ((pad / "cache" / "cost_ledger.json", "PAD mini lane"),):
        if p.exists():
            v = jload(p)["usd"]; parts[key] = v; total += v
    for p, key in ((pad / "build" / "probe.json", "PAD probe"),):
        if p.exists():
            v = jload(p)["probe_usd"]; parts[key] = v; total += v
    if (pad / "build" / "contam_probes.json").exists():
        for lane, rec in jload(pad / "build" / "contam_probes.json").items():
            parts[f"PAD Amendment 1 probe {lane}"] = rec["probe_usd"]; total += rec["probe_usd"]
    for d, tag in ((pad / "rows", "PAD Amendment 1"), (ROWS, "PARA")):
        for code in ("MINI", "H45", "OP5"):
            p = d / f"rows_{code}.jsonl"
            if p.exists():
                v = sum(json.loads(l).get("usd", 0.0) for l in io.open(p, encoding="utf-8")); parts[f"{tag} {code} lane"] = v; total += v
    if (PARA / "para_questions.json").exists():
        v = jload(PARA / "para_questions.json")["meta"]["usd_list_est"]; parts["PARA drafting"] = v; total += v
    if (PARA / "probes.json").exists():
        for lane, rec in jload(PARA / "probes.json").items():
            parts[f"PARA probe {lane}"] = rec["probe_usd"]; total += rec["probe_usd"]
    return total, parts


def headrooms():
    """The ruling of 2026-09-14 (evening): the combined $21 cap covers the registered lanes; the PAD Amendment 1 Haiku add-on sits under
    the $28 overall cap and never displaces a registered lane. A lane fits when its x1.3 projection is within both headrooms."""
    total, parts = billed_so_far()
    # §8: "the cap less every lane already billed and every earlier lane's projection" -- a lane submitted as a Batch but not yet
    # collected (batch_<code>.json present, rows_<code>.jsonl absent) counts at its probe projection until its rows are billed
    if RC.PROBES.exists():
        pr = jload(RC.PROBES)
        for lane, cfg in RC.LANES.items():
            code = cfg["code"]
            if (ROWS / f"batch_{code}.json").exists() and not (ROWS / f"rows_{code}.jsonl").exists() and lane in pr:
                v = pr[lane]["projection"]["usd"]; parts[f"PARA {code} lane (submitted, projection)"] = v; total += v
    combined = sum(v for k, v in parts.items() if k not in ADDON_KEYS)
    return {"billed_overall": round(total, 4), "billed_combined": round(combined, 4), "billed_parts": parts,
            "headroom_combined": round(CAP_RAISED - combined, 4), "headroom_overall": round(OVERALL_CAP - total, 4),
            "headroom": round(min(CAP_RAISED - combined, OVERALL_CAP - total), 4),
            "headroom_if_addon_counted_on_combined": round(CAP_RAISED - total, 4)}


def cmd_probe(lane):
    assert (PARA / "sheet.json").exists(), "STOP: the author's read is not ledgered (§8: no scoring call before AUX-PARA-SHEET)"
    RC.load_env()
    cfg = RC.LANES[lane]
    rows = [RC.call_once(lane, units(arm)[0], arm, 0) for arm in ARMS]
    ok = all(lane.split("-2025")[0] in r["served_model"] or lane in r["served_model"] for r in rows)
    n_units = len(units(ARMS[0]))
    n = cfg["k"] * len(ARMS) * n_units
    tin = cfg["k"] * n_units * sum(r["tok_in"] for r in rows)
    tout = n * max(1, sum(r["tok_out"] for r in rows) / len(rows))
    usd = (tin / 1e6 * cfg["price"][0] + tout / 1e6 * cfg["price"][1]) * cfg["mult"]
    cap = CAP_RAISED or COMBINED_CAP
    H = headrooms(); billed, parts, headroom = H["billed_combined"], H["billed_parts"], H["headroom"]
    rec = {"lane": lane, "served": [r["served_model"] for r in rows], "identifier_ok": ok, "in": [r["tok_in"] for r in rows], "out": [r["tok_out"] for r in rows],
           "parsed": [r["status"] for r in rows], "probe_usd": sum(r["usd"] for r in rows), "k": cfg["k"],
           "projection": {"calls": n, "input_tokens": tin, "output_tokens": tout, "usd": round(usd, 4), "usd_x1.3": round(usd * 1.3, 4)},
           "cap": cap, "overall_cap": OVERALL_CAP, "billed_so_far": round(billed, 4), "billed_parts": parts, "headroom": round(headroom, 4),
           "headroom_combined": H["headroom_combined"], "headroom_overall": H["headroom_overall"], "billed_overall": H["billed_overall"],
           "headroom_if_addon_counted_on_combined": H["headroom_if_addon_counted_on_combined"], "fits": usd * 1.3 <= headroom,
           "fits_if_addon_counted_on_combined": usd * 1.3 <= H["headroom_if_addon_counted_on_combined"], "population": POP, "n_units": n_units,
           "sample": rows[0]["text"][:200]}
    d = jload(RC.PROBES) if RC.PROBES.exists() else {}
    d[lane] = rec
    jdump(d, RC.PROBES)
    print(json.dumps({k: v for k, v in rec.items() if k not in ("sample", "billed_parts")}, indent=1))
    if not ok:
        raise SystemExit("IDENTIFIER MISMATCH -- E1.7 rule: do not launch this lane")
    if not rec["fits"]:
        print(f"DASH: the x1.3 projection ${usd * 1.3:.2f} exceeds the remaining headroom ${headroom:.2f} at the ${cap:.2f} cap -- the lane is not submitted")


# ------------------------------------------------------------------ scoring
def load_new(code):
    path = ROWS / f"rows_{code}.jsonl"
    if not path.exists():
        return None
    per = collections.defaultdict(dict); n_bad = 0
    for line in io.open(path, encoding="utf-8"):
        r = json.loads(line)
        if r.get("status") != "OK":
            n_bad += 1; continue
        per[(r["unit_id"], r["arm"])][r["draw"]] = r
    out = {}
    for k, draws in per.items():
        rs = list(draws.values())
        if len(rs) < S.MIN_DRAWS and len(rs) != 1:
            continue
        noks = [x["nok"] for x in rs if x["nok"] is not None]
        if noks:
            out[k] = float(np.mean(noks))
    return out, n_bad


def cmd_score():
    LK = jload(res_path("lookups.json"))
    assert LK.get("population", "accepted") == POP
    P = accepted_pairs(); rows = items(P)
    y = np.array([r["y"] for r in rows], int); g = np.array([r["persona"] for r in rows])
    sh = jload(PARA / "sheet.json")
    res = {"registration_sha256": REG_SHA, "sheet_sha256": sh["sheet_sha256"], "population": POP,
           "label": "registered (the 115 accepted pairs; floor amended 2026-09-21)" if POP == "accepted" else "sensitivity, not registered (all 124 screen-passing pairs)",
           "n": len(rows), "n_pairs": len(P), "n_pos": int(y.sum()), "tol": TOL,
           "lookups": LK["rows"], "models": {}, "branches": {}, "flags": {}, "extras": {}}
    lk_scores = {k: {"orig": np.array(v["orig"], float), "para": np.array(v["para"], float)} for k, v in LK["scores"].items()}
    # ---- models
    for code, lane in (("MINI", "gpt-4.1-mini"), ("H45", "claude-haiku-4-5-20251001"), ("OP5", "claude-opus-5"), ("LUNA", "gpt-5.6-luna"), ("SOL", "gpt-5.6-sol")):
        rec = S.load_lane(code); new = load_new(code)
        if new is None and code in ADDED:
            res["models"][code] = {"status": "added reader, not registered: lane not run", "added_not_registered": True}
            continue
        if new is None:
            pr = jload(PARA / "probes.json").get(lane) if (PARA / "probes.json").exists() else None
            res["models"][code] = {"status": "dash: " + (f"the ×1.3 projection ${pr['projection']['usd_x1.3']:.2f} exceeded the headroom ${pr['headroom']:.2f} at the ${pr['cap']:.2f} cap" if pr and not pr["fits"] else "lane not run")}
            continue
        newd, n_bad = new
        M = {"n_bad_rows": n_bad, "k_new": ADDED[code]["k"] if code in ADDED else RC.LANES[lane]["k"], "k_recorded": 5 if code != "MINI" else 1}
        if code in ADDED:
            M.update({"added_not_registered": True, "label": ADDED[code]["label"], "arms": ADDED[code]["arms"]})
        for arm in ARMS:
            sv = ARM_KEY[arm]
            o = np.array([rec.get((r["item_id"], arm), np.nan) for r in rows], float)
            p = np.array([newd.get((r["item_id"], arm), np.nan) for r in rows], float)
            ok = ~np.isnan(o) & ~np.isnan(p)
            if ok.sum() == 0:
                continue                      # the added readers ran under v2 only (their Table 1 arm; the only one with recorded originals)
            R = {"n_scored": int(ok.sum()), "original": float(auroc(o[ok], y[ok])), "original_per_state": per_state([r for r, k in zip(rows, ok) if k], o[ok], y[ok]),
                 "paraphrase": float(auroc(p[ok], y[ok])), "paraphrase_per_state": per_state([r for r, k in zip(rows, ok) if k], p[ok], y[ok]),
                 "paired": paired(o[ok], p[ok], y[ok], g[ok]),
                 "paired_per_state": {st: paired(o[state_mask(rows, st) & ok], p[state_mask(rows, st) & ok], y[state_mask(rows, st) & ok], g[state_mask(rows, st) & ok]) for st in STATES},
                 "model_minus_emb": paired(lk_scores[f"emb_{sv}"]["para"][ok], p[ok], y[ok], g[ok]),
                 "model_minus_lex": paired(lk_scores[f"lex_{sv}"]["para"][ok], p[ok], y[ok], g[ok])}
            M[sv] = R
            print(f"{code} {sv}: original {R['original']:.4f} -> paraphrase {R['paraphrase']:.4f}  d {R['paired']['delta']:+.4f} weaker [{R['paired']['weaker']['ci_lo']:+.4f},{R['paired']['weaker']['ci_hi']:+.4f}]; "
                  f"model-emb {R['model_minus_emb']['delta']:+.4f} model-lex {R['model_minus_lex']['delta']:+.4f}")
        res["models"][code] = M
    # ---- §7 branches per summary
    def status(pd):
        if abs(pd["delta"]) <= TOL:
            return "holds"
        if pd["delta"] < -TOL and pd["both_exclude_zero"]:
            return "collapses"
        return "neither (beyond tolerance, intervals not both excluding zero, or a rise)"
    for sv in ("v2", "v3"):
        st = {"emb": status(LK["rows"][f"emb_{sv}"]["paired"]), "lex": status(LK["rows"][f"lex_{sv}"]["paired"])}
        for code, M in res["models"].items():
            if sv in M:
                st[code] = status(M[sv]["paired"])
        heads = []
        if st["lex"] == "collapses" and st["emb"] == "holds":
            heads.append("A")
        if st["lex"] == "holds" and st["emb"] == "holds":
            heads.append("B")
        if st["lex"] == "collapses" and st["emb"] == "collapses":
            heads.append("C")
        # §7 D reads the registered models only; the added readers (not registered) print their status beside
        D = {code: [lk for lk in ("emb", "lex") if st[lk] == "collapses"] for code in res["models"] if code not in ADDED and st.get(code) == "holds"}
        D = {k: v for k, v in D.items() if v}
        if D:
            heads.append("D")
        added_status = {code: st[code] for code in ADDED if code in st}
        res["branches"][sv] = {"status": {k: v for k, v in st.items() if k not in ADDED}, "headings": heads, "D": D, "added_readers_status_not_registered": added_status}
        print(f"branches {sv}: {st} -> {heads} {D}")
    # ---- AUX-PARA-FLAGS: the H.2 split on the paraphrase set (the author's column 2), and under the original flags
    col2 = {r["pair_id"]: r["names_value"] for r in sh["rows"]}
    orig_flags = {f["pair_id"]: f["flag"] for f in jload(CF2 / "question_read_flags.json")["flags"]}
    tok_flags = {r["pair_id"]: ("YES" if r.get("value_tokens_in_paraphrase") else "NO") for r in jload(PARA / "para_questions.json")["rows"] if r["accepted"]}
    # the amendment of 2026-09-21: the split is reported both ways -- the author's column 2 (H.2's sentence) and the token rule on the paraphrases
    for label, flags in (("author_column2_on_paraphrases", col2), ("original_question_flags", orig_flags), ("token_rule_on_paraphrases", tok_flags)):
        fl = np.array([flags.get(r["pair_id"]) == "YES" for r in rows])
        out = {"n_flagged_pairs": int(sum(1 for pr in P if flags.get(pr["pair_id"]) == "YES")), "n_unflagged_pairs": int(sum(1 for pr in P if flags.get(pr["pair_id"]) != "YES")),
               "positives_by_state_flagged": {st: int(((np.array([r["state"] for r in rows]) == st) & (y == 1) & fl).sum()) for st in STATES},
               "positives_by_state_unflagged": {st: int(((np.array([r["state"] for r in rows]) == st) & (y == 1) & ~fl).sum()) for st in STATES}}

        def split(arr):
            def a(mask):
                m = mask & ~np.isnan(arr)
                return float(auroc(arr[m], y[m])) if m.sum() and y[m].sum() and (m.sum() - y[m].sum()) else None
            return {"whole": a(np.ones(len(y), bool)), "flagged": a(fl), "unflagged": a(~fl),
                    "flagged_per_state": {st: a(fl & state_mask(rows, st)) for st in STATES}, "unflagged_per_state": {st: a(~fl & state_mask(rows, st)) for st in STATES}}
        for k, v in lk_scores.items():
            out[k] = {"paraphrase": split(v["para"]), "original": split(v["orig"])}
        for code, M in res["models"].items():
            for sv in ("v2", "v3"):
                if sv in M:
                    rec = S.load_lane(code); newd, _ = load_new(code)
                    arm = "INDEXED-V2" if sv == "v2" else "INDEXED-V3"
                    o = np.array([rec.get((r["item_id"], arm), np.nan) for r in rows], float)
                    pnew = np.array([newd.get((r["item_id"], arm), np.nan) for r in rows], float)
                    if np.isnan(pnew).all():
                        continue
                    out[f"{code}_{sv}"] = {"paraphrase": split(pnew), "original": split(o)}
        res["flags"][label] = out
    # ---- the author's extra descriptives (2026-09-14, NUMBERS_PARA.md): cosine and overlap to the target name before / after
    from sweep_common import _vecs
    targets = {}
    ind = jload(CF2 / "cf_cell.json")["meta"]["individuation"]
    for pr in P:
        targets[pr["pair_id"]] = ind[pr["pair_id"]]["slot_scrubbed"]
    qs = sorted({r["question"] for r in rows} | {r["paraphrase"] for r in rows}); names = sorted(set(targets.values()))
    qv = _vecs(qs, "q"); nv = _vecs(names, "n")
    cos_o, cos_p, ov_o, ov_p = [], [], [], []
    for pr in P:
        t = targets[pr["pair_id"]]
        cos_o.append(float(qv[pr["question"]] @ nv[t])); cos_p.append(float(qv[pr["paraphrase"]] @ nv[t]))
        tt = content(t.replace("_", " "))
        ov_o.append(len(content(pr["question"]) & tt) / max(1, len(tt))); ov_p.append(len(content(pr["paraphrase"]) & tt) / max(1, len(tt)))
    res["extras"]["target_name_similarity"] = {"cosine_original_mean": float(np.mean(cos_o)), "cosine_paraphrase_mean": float(np.mean(cos_p)),
                                               "cosine_paraphrase_minus_original_mean": float(np.mean(np.array(cos_p) - np.array(cos_o))),
                                               "token_overlap_original_mean": float(np.mean(ov_o)), "token_overlap_paraphrase_mean": float(np.mean(ov_p)),
                                               "pairs_with_zero_overlap_original": int(sum(1 for v in ov_o if v == 0)), "pairs_with_zero_overlap_paraphrase": int(sum(1 for v in ov_p if v == 0)),
                                               "per_pair": [{"pair_id": pr["pair_id"], "cos_orig": a, "cos_para": b, "ov_orig": c, "ov_para": d} for pr, a, b, c, d in zip(P, cos_o, cos_p, ov_o, ov_p)]}
    # ---- seed spot-check 43-46 on the whole-set paired differences that carry a conclusion (every reader × summary)
    spot = {}
    for k, v in lk_scores.items():
        spot[k] = {str(sd): {"item": boot_item(v["orig"], v["para"], y, seed=sd), "persona": boot_cluster(v["orig"], v["para"], y, g, seed=sd)} for sd in (43, 44, 45, 46)}
    res["extras"]["seed_spot_check_lookups"] = spot
    res["matched"] = matched_metric(rows, lk_scores, res["models"])
    jdump(res, res_path("para_scores.json"))
    print(f"wrote {res_path('para_scores.json')} (population {POP})")



# ------------------------------------------------------------------ the matched metric (R125's construction, beside the pooled AUROC)
def matched_metric(rows, lk_scores, models):
    """Within-triple PN vs PRESENT (primary) and PN vs ABSENT for every reader x summary, original and paraphrase, whole and per
    state, with the triple-level and the persona-grouped bootstrap (reviews/r125/tools/r125_common: wtl, boot_triple, boot_persona;
    1,000 draws, seed 42), and the paired difference paraphrase - original as the mean over triples of (outcome_para - outcome_orig)
    with both intervals. Post hoc beside the registered pooled AUROC; labelled so."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "reviews" / "r125" / "tools"))
    from r125_common import boot_persona, boot_triple, wtl  # noqa: E402
    pos = {(r["pair_id"], r["version"]): k for k, r in enumerate(rows)}
    pids = sorted({r["pair_id"] for r in rows})
    pstate = {r["pair_id"]: r["state"] for r in rows}
    gp_all = {r["pair_id"]: r["persona"] for r in rows}

    def outcomes(v, neg, ps):
        a = np.array([v[pos[(q, "PN")]] for q in ps], float); b = np.array([v[pos[(q, neg)]] for q in ps], float)
        out = np.where(a > b, 1.0, np.where(a == b, 0.5, 0.0)); out[np.isnan(a) | np.isnan(b)] = np.nan
        return out

    def block(v, neg, ps):
        out = outcomes(v, neg, ps); gp = np.array([gp_all[q] for q in ps])
        r = wtl(out); r["ci_triple"] = boot_triple(out); r["ci_persona"] = boot_persona(out, gp)
        return r

    def pair(vo, vp, neg, ps):
        d = outcomes(vp, neg, ps) - outcomes(vo, neg, ps); gp = np.array([gp_all[q] for q in ps]); keep = ~np.isnan(d)
        it, cl = boot_triple(d), boot_persona(d, gp)
        return {"delta": float(d[keep].mean()) if keep.any() else None, "n": int(keep.sum()), "ci_triple": it, "ci_persona": cl,
                "both_exclude_zero": bool(it.get("excludes_zero") and cl.get("excludes_zero")), "agree": bool(it.get("excludes_zero") == cl.get("excludes_zero"))}

    def reader(vo, vp):
        out = {}
        for neg in ("PRESENT", "ABSENT"):
            key = f"pn_vs_{neg.lower()}"
            out[key] = {"original": {"whole": block(vo, neg, pids), "per_state": {st: block(vo, neg, [q for q in pids if pstate[q] == st]) for st in STATES}},
                        "paraphrase": {"whole": block(vp, neg, pids), "per_state": {st: block(vp, neg, [q for q in pids if pstate[q] == st]) for st in STATES}},
                        "paired": {"whole": pair(vo, vp, neg, pids), "per_state": {st: pair(vo, vp, neg, [q for q in pids if pstate[q] == st]) for st in STATES}}}
        return out

    res = {"n_pairs": len(pids), "construction": "R125 matched metric, (W + T/2) / n over the population's triples; primary PN vs PRESENT; intervals triple-level and persona-grouped, 1,000 draws, seed 42"}
    for k, v in lk_scores.items():
        res[k] = reader(v["orig"], v["para"])
    for code in ("MINI", "H45", "OP5", "LUNA", "SOL"):
        if code not in models or "v2" not in models[code]:
            continue
        rec = S.load_lane(code); newd, _ = load_new(code)
        for arm in ARMS:
            o = np.array([rec.get((r["item_id"], arm), np.nan) for r in rows], float)
            pn = np.array([newd.get((r["item_id"], arm), np.nan) for r in rows], float)
            if np.isnan(pn).all():
                continue
            res[f"{code}_{ARM_KEY[arm]}"] = reader(o, pn)
    for k, v in res.items():
        if isinstance(v, dict) and "pn_vs_present" in v:
            w = v["pn_vs_present"]
            print(f"matched {k}: original {w['original']['whole']['matched']} -> paraphrase {w['paraphrase']['whole']['matched']}  d {w['paired']['whole']['delta']:+.4f} "
                  f"triple [{w['paired']['whole']['ci_triple'].get('ci_lo', float('nan')):+.4f},{w['paired']['whole']['ci_triple'].get('ci_hi', float('nan')):+.4f}] "
                  f"persona [{w['paired']['whole']['ci_persona'].get('ci_lo', float('nan')):+.4f},{w['paired']['whole']['ci_persona'].get('ci_hi', float('nan')):+.4f}]")
    return res


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("sheet", "lookups", "score"):
        globals()["cmd_" + cmd]()
    elif cmd == "probe":
        cmd_probe(sys.argv[2])
    else:
        assert (PARA / "sheet.json").exists(), "STOP: the author's read is not ledgered"
        lane = sys.argv[2]
        pr = jload(PARA / "probes.json").get(lane) if (PARA / "probes.json").exists() else None
        assert pr and pr["identifier_ok"], "STOP: probe this lane first"
        if cmd == "submit" or cmd == "sync":
            assert pr["fits"], "STOP: the lane's x1.3 projection exceeds the headroom; it prints a dash"
        getattr(RC, "cmd_" + cmd)(lane)
