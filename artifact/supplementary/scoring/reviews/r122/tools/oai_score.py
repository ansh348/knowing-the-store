# -*- coding: utf-8 -*-
"""oai_score.py -- R122 T3 and T4: score the OpenAI lanes with the CF-2 conventions, unchanged (cf2_reader_score: the X4 collapse, whole-set
and per-state AUROC against y_nok, the paired difference with item-level and persona-grouped bootstraps, PN versus PRESENT and W/T/L),
against the recorded rows read and never re-run. No model call.

  T3  rows_MINI5.jsonl (INDEXED-V2, INDEXED-V3; k = 5) beside the recorded one-draw rows rows_MINI.jsonl (same arms). Lookup comparators:
      v2 the superseded-names lookup (0.7663), v3 the all-states lookup (0.8756). Distinct score values and tied triples for both rows.
      P-K1 per summary: |AUROC(k5) - AUROC(k1)| <= 0.05 at the point and tied triples(k5) < tied triples(k1); HOLDS iff on both summaries.
  T4  rows_P1LUNA.jsonl (INDEXED-V2, k = 5) beside the recorded rows_LUNA.jsonl; rows_P1MINI.jsonl (k = 1) beside the recorded rows_MINI.jsonl
      INDEXED-V2. P-R1: each reader's whole-set AUROC under P1 within 0.05 of its recorded P0 value (point). P-R2: the ordering of the three
      per-state AUROCs under P1 equals the recorded ordering under P0, for each reader. P-R3: Luna under P1 minus the lookup is positive
      with both intervals excluding zero.

Usage: python oai_score.py [T3|T4|all]   -> results/scores_r122_oai.json and the ledger sections
"""
from __future__ import annotations

import collections
import io
import json
import sys

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r122_common as C  # noqa: E402
import cf2_reader_score as RS  # noqa: E402
import score_cf as S  # noqa: E402
from index_v3 import named_sections  # noqa: E402
from common_e1r import auroc  # noqa: E402
from cf2_score import paired  # noqa: E402

REG_T3, REG_T4 = "ADDENDUM_R122_MINI_K5.md", "ADDENDUM_R122_CF2_P1.md"
STATES = RS.STATES
RECORDED = {"MINI": C.CF2 / "rows" / "rows_MINI.jsonl", "LUNA": C.CF2 / "rows" / "rows_LUNA.jsonl"}


def lookup_v3(items, idx):
    s3 = [named_sections(idx[it["item_id"]]["v3"]) for it in items]
    look = np.asarray(S.matcher([it["question"] for it in items], [s["superseded"] + s["retracted"] + s["expired"] for s in s3]), float)
    y = np.array([it["y_nok"] for it in items], int)
    assert C.r4(auroc(look, y)) == C.LOOKUP_V3_GATE, ("GATE: the recorded all-states lookup", C.r4(auroc(look, y)))
    return look


def vector(path, arm, items):
    col, census = RS.collapse(path, arm)
    v = np.array([col.get(it["item_id"], np.nan) for it in items], float)
    return v, census


def tied_triples(v, items):
    pos = {(it["pair_id"], it["version"]): k for k, it in enumerate(items)}
    pairs = sorted({it["pair_id"] for it in items}); n = 0
    for p in pairs:
        a, b, c = (v[pos[(p, ver)]] for ver in ("PN", "PRESENT", "ABSENT"))
        n += int(a == b == c)
    return n


def per_state_order(block):
    return sorted(STATES, key=lambda s: -block["per_state"][s]["auroc"])


def score_pair(new_path, new_arm, rec_path, rec_arm, items, look, label_new, label_rec):
    """The new row scored with score_lane (its census, lookup contrast and post-hoc block), the recorded row the same way, and the paired
    difference new minus recorded on the covered items (both intervals)."""
    new = RS.score_lane(new_path, new_arm, items, look); rec = RS.score_lane(rec_path, rec_arm, items, look)
    vn, _ = vector(new_path, new_arm, items); vr, _ = vector(rec_path, rec_arm, items)
    m = ~np.isnan(vn) & ~np.isnan(vr)
    y = np.array([it["y_nok"] for it in items], int)[m]; g = np.array([it["persona"] for it in items])[m]; st = np.array([it["state"] for it in items])[m]
    d = {"covered": int(m.sum()), "whole": paired(vr[m], vn[m], y, g),
         "per_state": {s: paired(vr[m][st == s], vn[m][st == s], y[st == s], g[st == s]) for s in STATES}}
    for r, v_ in ((new, vn), (rec, vr)):
        r["tied_triples"] = tied_triples(v_, items) if not np.isnan(v_).any() else None
    return {"new": {"label": label_new, **new}, "recorded": {"label": label_rec, **rec}, "new_minus_recorded": d}


def score_t3(items, idx, look2):
    C.assert_frozen(REG_T3)
    look3 = lookup_v3(items, idx); new = C.ROWS / "rows_MINI5.jsonl"; out = {}
    for arm, look in (("INDEXED-V2", look2), ("INDEXED-V3", look3)):
        out[arm] = score_pair(new, arm, RECORDED["MINI"], arm, items, look, "gpt-4.1-mini k=5 (temperature unset)", "gpt-4.1-mini k=1 temperature 0 (recorded)")
    ver = {}
    for arm in out:
        a, b = out[arm]["new"], out[arm]["recorded"]
        within = abs(a["whole"] - b["whole"]) <= C.TOL; falls = (a["tied_triples"] is not None and b["tied_triples"] is not None and a["tied_triples"] < b["tied_triples"])
        ver[arm] = {"within_tol_point": bool(within), "tied_triples_fall": bool(falls), "k5": a["whole"], "k1": b["whole"], "delta": out[arm]["new_minus_recorded"]["whole"]["delta"],
                    "tied_k5": a["tied_triples"], "tied_k1": b["tied_triples"], "holds": bool(within and falls)}
    out["predictions"] = {"P-K1": {"verdict": "HOLDS" if all(v["holds"] for v in ver.values()) else "FAILS", "per_summary": ver}}
    return out


def score_t4(items, look2):
    C.assert_frozen(REG_T4)
    out = {"LUNA": score_pair(C.ROWS / "rows_P1LUNA.jsonl", "INDEXED-V2", RECORDED["LUNA"], "INDEXED-V2", items, look2, "GPT-5.6 Luna P1 k=5", "GPT-5.6 Luna P0 k=5 (recorded, E5)"),
           "MINI": score_pair(C.ROWS / "rows_P1MINI.jsonl", "INDEXED-V2", RECORDED["MINI"], "INDEXED-V2", items, look2, "GPT-4.1 mini P1 k=1", "GPT-4.1 mini P0 k=1 (recorded)")}
    r1 = {c: {"p1": out[c]["new"]["whole"], "p0": out[c]["recorded"]["whole"], "delta": out[c]["new_minus_recorded"]["whole"]["delta"],
              "within": bool(abs(out[c]["new"]["whole"] - out[c]["recorded"]["whole"]) <= C.TOL)} for c in out}
    r2 = {c: {"order_p1": per_state_order(out[c]["new"]), "order_p0": per_state_order(out[c]["recorded"]),
              "same": per_state_order(out[c]["new"]) == per_state_order(out[c]["recorded"])} for c in out}
    vl = out["LUNA"]["new"]["vs_lookup"]
    r3 = {"delta": vl["delta"], "item_ci": vl["item_ci"], "persona_ci": vl["persona_ci"], "both_exclude_zero": vl["both_exclude_zero"],
          "recorded_delta": out["LUNA"]["recorded"]["vs_lookup"]["delta"], "holds": bool(vl["delta"] > 0 and vl["both_exclude_zero"])}
    out["predictions"] = {"P-R1": {"verdict": "HOLDS" if all(v["within"] for v in r1.values()) else "FAILS", "per_reader": r1},
                          "P-R2": {"verdict": "HOLDS" if all(v["same"] for v in r2.values()) else "FAILS", "per_reader": r2},
                          "P-R3": {"verdict": "HOLDS" if r3["holds"] else "FAILS", **r3}}
    return out


def row_line(name, r):
    ps = " / ".join(f"{r['per_state'][s]['auroc']:.4f}" for s in STATES)
    ph = r["posthoc"]["whole"]; o = ph["ordering"]
    return (f"| {name} | {r['whole']:.4f} [{r['whole_ci_persona']['ci_lo']:.4f}, {r['whole_ci_persona']['ci_hi']:.4f}] | {RS.fmt_paired(r['vs_lookup'])} | {ps} | "
            f"{ph['pn_vs_present']:.4f} | {o['wins']}/{o['ties']}/{o['losses']} | {r['distinct_values']} | {r['tied_triples']} | "
            f"{r['census']['identical_across_draws']} / {r['census']['median_range']} | {r['census']['rows']} rows, {r['census']['not_ok']} not OK, ${r['census']['usd']:.4f} |")


HEAD = ["| row | whole [persona CI] | minus the lookup (item; persona) | SUP / RET / EXP | PN vs PRESENT | W/T/L | distinct values | tied triples | identical draws / median range | census |",
        "|---|---|---|---|---|---|---:|---:|---|---|"]


def ledger_t3(t3):
    L = ["", "## T3. GPT-4.1 mini at five draws on the counterfactual set (ADDENDUM_R122_MINI_K5.md)", "", "### AUX-R122-K5-ROWS", ""] + HEAD
    for arm in ("INDEXED-V2", "INDEXED-V3"):
        L.append(row_line(f"{arm}: {t3[arm]['new']['label']}", t3[arm]["new"])); L.append(row_line(f"{arm}: {t3[arm]['recorded']['label']}", t3[arm]["recorded"]))
    L += ["", "### AUX-R122-K5-DELTA — five-draw minus one-draw (item-level; persona-grouped), whole and per state", ""]
    for arm in ("INDEXED-V2", "INDEXED-V3"):
        d = t3[arm]["new_minus_recorded"]
        L.append(f"- {arm}: whole {RS.fmt_paired(d['whole'])}; " + "; ".join(f"{s} {RS.fmt_paired(d['per_state'][s])}" for s in STATES) + f" (covered {d['covered']})")
    P = t3["predictions"]["P-K1"]
    L += ["", f"### AUX-R122-K5-P-K1 — **{P['verdict']}** (per summary: within 0.05 at the point and the tied-triple count falls; HOLDS iff both summaries)", ""]
    for arm, v in P["per_summary"].items():
        L.append(f"- {arm}: k5 {v['k5']:.4f} vs k1 {v['k1']:.4f} (delta {v['delta']:+.4f}; within {v['within_tol_point']}); tied triples {v['tied_k1']} -> {v['tied_k5']} (falls {v['tied_triples_fall']}) -> {'holds' if v['holds'] else 'fails'}")
    C.append_ledger("\n".join(L) + "\n")


def ledger_t4(t4):
    L = ["", "## T4. The counterfactual set under the intent-explicit rubric P1 (ADDENDUM_R122_CF2_P1.md)", "", "### AUX-R122-P1-ROWS", ""] + HEAD
    for c in ("LUNA", "MINI"):
        L.append(row_line(t4[c]["new"]["label"], t4[c]["new"])); L.append(row_line(t4[c]["recorded"]["label"], t4[c]["recorded"]))
    L += ["", "### AUX-R122-P1-DELTA — P1 minus P0 (item-level; persona-grouped), whole and per state", ""]
    for c in ("LUNA", "MINI"):
        d = t4[c]["new_minus_recorded"]
        L.append(f"- {c}: whole {RS.fmt_paired(d['whole'])}; " + "; ".join(f"{s} {RS.fmt_paired(d['per_state'][s])}" for s in STATES) + f" (covered {d['covered']})")
    P = t4["predictions"]
    L += ["", f"### AUX-R122-P1-P-R1 — **{P['P-R1']['verdict']}** (each reader within 0.05 of its recorded P0 whole-set value, at the point)", ""]
    for c, v in P["P-R1"]["per_reader"].items():
        L.append(f"- {c}: P1 {v['p1']:.4f} vs P0 {v['p0']:.4f}, delta {v['delta']:+.4f}, within {v['within']}")
    L += ["", f"### AUX-R122-P1-P-R2 — **{P['P-R2']['verdict']}** (the per-state ordering unchanged)", ""]
    for c, v in P["P-R2"]["per_reader"].items():
        L.append(f"- {c}: P0 {' > '.join(v['order_p0'])}; P1 {' > '.join(v['order_p1'])}; same {v['same']}")
    r3 = P["P-R3"]
    L += ["", f"### AUX-R122-P1-P-R3 — **{r3['verdict']}** (Luna under P1 minus the lookup keeps its sign with both intervals excluding zero)", "",
          f"- Luna P1 minus the lookup 0.7663: {r3['delta']:+.4f} ({C.ci(r3['item_ci'])}; {C.ci(r3['persona_ci'])}); recorded P0 margin {r3['recorded_delta']:+.4f}; both exclude zero {r3['both_exclude_zero']}"]
    C.append_ledger("\n".join(L) + "\n")


def spend():
    tot = {}
    for lane in ("MINI5", "P1LUNA", "P1MINI"):
        p = C.ROWS / f"rows_{lane}.jsonl"
        if p.exists():
            rows = [json.loads(l) for l in io.open(p, encoding="utf-8") if l.strip()]
            tot[lane] = {"rows": len(rows), "usd": round(sum(r.get("usd", 0) for r in rows), 4), "not_ok": sum(1 for r in rows if r.get("status") != "OK"),
                         "cached_share": round(sum(r.get("tok_cached", 0) for r in rows) / max(1, sum(r.get("tok_in", 0) for r in rows)), 4),
                         "served": sorted({r.get("served_model") for r in rows if r.get("served_model")})}
    pr = C.jload(C.ROWS / "probes_r122_oai.json") if (C.ROWS / "probes_r122_oai.json").exists() else {}
    tot["probes_usd"] = round(sum(v.get("usd", 0) for v in pr.values()), 4)
    tot["total_usd"] = round(sum(v["usd"] for k, v in tot.items() if isinstance(v, dict)) + tot["probes_usd"], 4)
    return tot


def main(which):
    items, idx = C.cf2_cell(); look2 = RS.lookup_v2(items, idx)
    out = {"spend": spend()}
    if which in ("T3", "all"):
        out["T3"] = score_t3(items, idx, look2); ledger_t3(out["T3"])
    if which in ("T4", "all"):
        out["T4"] = score_t4(items, look2); ledger_t4(out["T4"])
    C.append_ledger(f"\n### AUX-R122-OAI-SPEND — token-metered from the rows at the page prices (not an invoice): {json.dumps(out['spend'])}; cap 5.00 USD for the batch.\n")
    prev = C.jload(C.RESULTS / "scores_r122_oai.json") if (C.RESULTS / "scores_r122_oai.json").exists() else {}
    prev.update(out); C.jdump(prev, C.RESULTS / "scores_r122_oai.json")
    for t in ("T3", "T4"):
        if t in out:
            for k, v in out[t]["predictions"].items():
                print(t, k, v["verdict"])
    print("spend", out["spend"])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
