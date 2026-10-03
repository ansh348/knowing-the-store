# -*- coding: utf-8 -*-
"""r125_t45_score.py -- the scorer for Task 4 (ADDENDUM_R125_SIBLING) and Task 5 (ADDENDUM_R125_E2_AMENDMENT_1). NO MODEL CALL. Written and hashed
before the freeze; the registrations fix every estimand and reading below.

Task 4. Per reader, the scores of the 88 kept pairs' PN and PRESENT versions (recorded rows; draw 1 of the recorded five for Opus 5 and Sol,
the five-draw means for GPT-4.1 mini (Table 1's row), Haiku 4.5 and Luna) and of the SIBLING version (the new rows). Primary estimand: the
matched AUROC of PN against SIBLING within the pair, (W + T/2) / n, with the triple-level and the persona-grouped bootstrap (1,000 draws, seed 42).
  P-SB1  the name lookup reads 0.90 or higher.
  P-SB2  every model reads 0.80 or higher with the persona interval excluding 0.50.
  P-SB3  the random-token lookup and the category-guessing count reader are within 0.05 of 0.50.
  P-SB4  no model reliably exceeds the name lookup (the paired matched difference model minus lookup with both intervals above zero would be a failure).
Descriptive, no bar: SIBLING minus PRESENT per reader (the mean score difference with both intervals; the matched AUROC of SIBLING against PRESENT).
Beside: the pooled AUROC of the 88 PN against the 88 SIBLING items, and the matched PN-vs-PRESENT on the same 88 pairs.

Task 5. Per model (Opus 5 draw 1, Sol draw 1, Luna five draws with its draw-1 column beside): names-only and counts-only on the 444, pooled AUROC
whole and per state with the persona interval, the paired difference against the recorded intact row (draw 1 for the one-draw comparisons; the
five-draw and the draw-1 rows for Luna) and counts-only minus names-only (cf2_score.paired), and the matched PN-vs-PRESENT AUROC whole and per state.
  P-N3  names-only within 0.05 of intact on the whole set at the point (E2's P-N1 rule), for each of the three.
  P-N4  counts-only reliably below names-only on the whole set, both intervals excluding zero, for each of the three.
  P-N5  counts-only above 0.50 on retraction and on expiry under the matched metric with the persona interval excluding 0.50, for each of the three.
A lane not run (NC-SOL under the budget rule) prints NOT EVALUABLE.
Writes reviews/r125/results/r125_t4_sibling.json and r125_t5_nc.json. Usage: python r125_t45_score.py t4 | t5
"""
from __future__ import annotations

import io
import sys

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r125_common as C  # noqa: E402
from r125_common import STATES, auroc, r4  # noqa: E402
from index_v3 import named_sections  # noqa: E402
import score_cf as S  # noqa: E402
import cf2_score  # noqa: E402,F401
from cf2_score import paired  # noqa: E402
from a1_count_readers import reader_scores  # noqa: E402
import enc_lookup as E  # noqa: E402

ROWS = C.CF2 / "rows"
TOL = 0.05
FREEZE = C.R125 / "FREEZE_R125.md"
REGS = ("ADDENDUM_R125_SIBLING.md", "ADDENDUM_R125_E2_AMENDMENT_1.md")


def assert_frozen():
    """Both registrations' registered-text sha256 against FREEZE_R125.md (a mismatch is a STOP)."""
    tab = {}
    for ln in io.open(FREEZE, encoding="utf-8"):
        if ln.startswith("| ") and "`ADDENDUM_R125" in ln:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            tab[cells[1].strip("`")] = cells[2].strip("`")
    for name in REGS:
        got = C.reg_sha(C.REGS / name)
        assert name in tab and got == tab[name], f"REGISTRATION SHA MISMATCH for {name} -- STOP"
    return tab


def load_vec(cell, key):
    v = C.jload(C.RESULTS / "r125_vectors.json")["readers"][key]["vector"]
    return cell.vector({i: (np.nan if x is None else x) for i, x in v.items()})


def outcomes_pairs(a, b):
    out = np.where(a > b, 1.0, np.where(a == b, 0.5, 0.0)); out[np.isnan(a) | np.isnan(b)] = np.nan
    return out


def matched(a, b, gp):
    out = outcomes_pairs(a, b); res = C.wtl(out)
    res["ci_triple"] = C.boot_triple(out); res["ci_persona"] = C.boot_persona(out, gp)
    return res


def paired_m(a1, b1, a2, b2, gp):
    """(A: a1 vs b1) minus (B: a2 vs b2) under the matched metric."""
    d = outcomes_pairs(a1, b1) - outcomes_pairs(a2, b2); keep = ~np.isnan(d)
    it, cl = C.boot_triple(d), C.boot_persona(d, gp)
    return {"delta": r4(d[keep].mean()), "n": int(keep.sum()), "ci_triple": it, "ci_persona": cl, "both_exclude_zero": bool(it.get("excludes_zero") and cl.get("excludes_zero"))}


def mean_diff(a, b, gp):
    d = a - b; keep = ~np.isnan(d)
    it, cl = C.boot_triple(d), C.boot_persona(d, gp)
    return {"delta": r4(d[keep].mean()), "n": int(keep.sum()), "ci_triple": it, "ci_persona": cl, "both_exclude_zero": bool(it.get("excludes_zero") and cl.get("excludes_zero"))}


# ------------------------------------------------------------------ Task 4
def score_t4():
    cell = C.Cell(); b = C.jload(C.BUILD / "build_t4_sibling.json"); rows = b["rows"]
    pids = [r["pair_id"] for r in rows]; gp = np.array([cell.pair_persona[p] for p in pids])
    kPN = [cell.pos_of[(p, "PN")] for p in pids]; kPR = [cell.pos_of[(p, "PRESENT")] for p in pids]
    qs = [r["question"] for r in rows]
    V = {}  # reader -> {"PN": vec, "PRESENT": vec, "SIBLING": vec}
    # no-model readers
    look = load_vec(cell, "LOOKUP_v2"); rtok = load_vec(cell, "RANDTOK_v2"); nb1 = load_vec(cell, "CR-nb1_v2")
    sib_lists = [r["sibling_list"] for r in rows]
    V["Name lookup"] = {"PN": look[kPN], "PRESENT": look[kPR], "SIBLING": np.asarray(S.matcher(qs, sib_lists), float)}
    names = sorted({n for i in cell.ids for n in named_sections(cell.idx[i]["v2"])["superseded"]} | {n for lst in sib_lists for n in lst})
    tok = {n: E.random_token(n) for n in names}; assert len(set(tok.values())) == len(tok)
    V["Random-token lookup"] = {"PN": rtok[kPN], "PRESENT": rtok[kPR], "SIBLING": np.asarray(S.matcher(qs, [[tok[n] for n in lst] for lst in sib_lists]), float)}
    gate_tok = np.asarray(S.matcher(cell.qs, [[tok[n] for n in named_sections(cell.idx[i]["v2"])["superseded"]] for i in cell.ids]), float)
    assert r4(auroc(gate_tok, cell.y)) == 0.5954, "the token map does not reproduce the recorded random-token row"
    cr_sib = np.array([reader_scores(b["texts"][r["item_id"]], r["question"], cell.pairs[r["pair_id"]]["category"], "SUPERSESSION")["CR-nb1"] for r in rows], float)
    V["Count reader, guessed category"] = {"PN": nb1[kPN], "PRESENT": nb1[kPR], "SIBLING": cr_sib}
    assert np.array_equal(cr_sib, nb1[kPN]), "the count reader's SIBLING scores differ from PN (counts were meant to be identical)"
    # models
    def sib_vec(lane, draw=None):
        p = ROWS / f"rows_r125_{lane}.jsonl"
        if not p.exists():
            return None
        col = C.collapse(p, "SIBLING")[0] if draw is None else C.draw_k(p, "SIBLING", draw)
        return np.array([col.get(r["item_id"], np.nan) for r in rows], float)
    M = [("GPT-4.1 mini (five draws)", "MINI5_v2", "SB-MINI5", None), ("Haiku 4.5 (five draws)", "H45_v2", "SB-H45", None), ("GPT-5.6 Luna (five draws)", "LUNA_v2", "SB-LUNA", None),
         ("Opus 5 (draw 1)", "OP5_v2_d1", "SB-OP5", 1), ("GPT-5.6 Sol (draw 1)", "SOL_v2_d1", "SB-SOL", 1)]
    for name, key, lane, draw in M:
        rec = load_vec(cell, key); sv = sib_vec(lane, draw)
        V[name] = {"PN": rec[kPN], "PRESENT": rec[kPR], "SIBLING": sv}
    res = {"meta": {"script": "reviews/r125/tools/r125_t45_score.py t4", "model_calls": 0, "n_pairs": len(pids), "dropped": b["meta"]["n_dropped"], "n_boot": C.N_BOOT, "seed": C.SEED,
                    "primary": "matched AUROC of PN against SIBLING within the pair, (W + T/2) / n; triple-level and persona-grouped bootstrap", "sibling_texts_sha256": b["meta"]["texts_sha256"]},
           "readers": {}, "predictions": {}}
    for name, d in V.items():
        if d["SIBLING"] is None:
            res["readers"][name] = {"status": "NOT EVALUABLE: lane not run"}; continue
        ok = ~np.isnan(d["SIBLING"])
        r = {"n_sibling_scored": int(ok.sum()), "pn_vs_sibling": matched(d["PN"], d["SIBLING"], gp), "pn_vs_present_same_pairs": matched(d["PN"], d["PRESENT"], gp),
             "sibling_vs_present": matched(d["SIBLING"], d["PRESENT"], gp), "sibling_minus_present_mean": mean_diff(d["SIBLING"], d["PRESENT"], gp),
             "pn_minus_sibling_mean": mean_diff(d["PN"], d["SIBLING"], gp),
             "pooled_pn_vs_sibling": r4(auroc(np.concatenate([d["PN"][ok], d["SIBLING"][ok]]), np.concatenate([np.ones(ok.sum()), np.zeros(ok.sum())]))),
             "means": {v: r4(np.nanmean(d[v])) for v in ("PN", "PRESENT", "SIBLING")}}
        if name != "Name lookup":
            r["minus_lookup_matched"] = paired_m(d["PN"], d["SIBLING"], V["Name lookup"]["PN"], V["Name lookup"]["SIBLING"], gp)
        res["readers"][name] = r
    R = res["readers"]
    lk = R["Name lookup"]["pn_vs_sibling"]["matched"]
    res["predictions"]["P-SB1"] = {"criterion": "the name lookup's matched PN-vs-SIBLING AUROC at or above 0.90", "lookup": lk, "verdict": "HELD" if lk >= 0.90 else "FAILED"}
    per = {}
    for name, _, _, _ in M:
        r = R[name]
        if "status" in r:
            per[name] = {"verdict": "NOT EVALUABLE"}; continue
        m = r["pn_vs_sibling"]; per[name] = {"matched": m["matched"], "persona_lo": r4(m["ci_persona"]["ci_lo"]), "ok": bool(m["matched"] >= 0.80 and m["ci_persona"]["ci_lo"] > 0.50)}
    ev = [v for v in per.values() if "ok" in v]
    res["predictions"]["P-SB2"] = {"criterion": "every model at or above 0.80 with the persona interval excluding 0.50", "per_model": per,
                                   "verdict": ("NOT EVALUABLE" if not ev else "HELD" if all(v["ok"] for v in ev) else "FAILED") + ("" if len(ev) == len(per) else " (on the models run)")}
    rt = R["Random-token lookup"]["pn_vs_sibling"]["matched"]; cr = R["Count reader, guessed category"]["pn_vs_sibling"]["matched"]
    res["predictions"]["P-SB3"] = {"criterion": "the random-token lookup and the count reader within 0.05 of 0.50", "random_token": rt, "count_reader": cr, "verdict": "HELD" if abs(rt - 0.5) <= TOL and abs(cr - 0.5) <= TOL else "FAILED"}
    ex = {name: R[name]["minus_lookup_matched"] for name, _, _, _ in M if "minus_lookup_matched" in R[name]}
    above = [n for n, d in ex.items() if d["delta"] > 0 and d["both_exclude_zero"]]
    res["predictions"]["P-SB4"] = {"criterion": "no model reliably exceeds the name lookup (matched, paired, both intervals above zero)", "reliably_above": above,
                                   "verdict": ("NOT EVALUABLE" if not ex else "HELD" if not above else "FAILED") + ("" if len(ex) == len(M) else " (on the models run)")}
    C.jdump(res, C.RESULTS / "r125_t4_sibling.json")
    print(f"Task 4: {len(pids)} pairs")
    for name, r in R.items():
        if "status" in r:
            print(f"  {name:32s} {r['status']}"); continue
        m = r["pn_vs_sibling"]; s = r["sibling_vs_present"]
        print(f"  {name:32s} PN vs SIBLING {m['W']:3d}/{m['T']:3d}/{m['L']:3d} matched {m['matched']:.4f} [{m['ci_triple']['ci_lo']:.4f},{m['ci_triple']['ci_hi']:.4f}] [{m['ci_persona']['ci_lo']:.4f},{m['ci_persona']['ci_hi']:.4f}] "
              f"| PN vs PRESENT {r['pn_vs_present_same_pairs']['matched']:.4f} | SIBLING vs PRESENT {s['matched']:.4f} ({s['W']}/{s['T']}/{s['L']}) mean diff {r['sibling_minus_present_mean']['delta']:+.4f} | pooled {r['pooled_pn_vs_sibling']:.4f}"
              + (f" | minus lookup {r['minus_lookup_matched']['delta']:+.4f}{'*' if r['minus_lookup_matched']['both_exclude_zero'] else ''}" if "minus_lookup_matched" in r else ""))
    for k, v in res["predictions"].items():
        print(f"  {k}: {v['verdict']}")


# ------------------------------------------------------------------ Task 5
def score_t5():
    cell = C.Cell(); y, g, st = cell.y, cell.g, cell.st
    look = load_vec(cell, "LOOKUP_v2")

    def lane_vec(lane, arm, draw=None):
        p = ROWS / f"rows_r125_{lane}.jsonl"
        if not p.exists():
            return None
        col = C.collapse(p, arm)[0] if draw is None else C.draw_k(p, arm, draw)
        return cell.vector(col)

    M = [("Opus 5 (draw 1)", "NC-OP5", 1, "OP5_v2_d1", "OP5_v2"), ("GPT-5.6 Sol (draw 1)", "NC-SOL", 1, "SOL_v2_d1", "SOL_v2"),
         ("GPT-5.6 Luna (five draws)", "NC-LUNA", None, "LUNA_v2", "LUNA_v2_d1"), ("GPT-5.6 Luna (draw 1)", "NC-LUNA", 1, "LUNA_v2_d1", "LUNA_v2")]
    res = {"meta": {"script": "reviews/r125/tools/r125_t45_score.py t5", "model_calls": 0, "n_boot": C.N_BOOT, "seed": C.SEED, "tolerance": TOL,
                    "comparator": "the recorded intact row: draw 1 for the one-draw comparisons; Luna's five-draw row for its five-draw rows, its draw 1 beside"}, "readers": {}, "predictions": {}}

    from common_e1r import boot_cluster_single
    for name, lane, draw, intact_key, other_key in M:
        intact = load_vec(cell, intact_key); other = load_vec(cell, other_key)
        vn, vc = lane_vec(lane, "INDEXED-NAMES", draw), lane_vec(lane, "INDEXED-COUNTS", draw)
        if vn is None or vc is None:
            res["readers"][name] = {"status": "NOT EVALUABLE: lane not run (NC-SOL is dropped when the OpenAI projection for Tasks 4 and 5 exceeds the cap)"}; continue
        okn, okc = ~np.isnan(vn), ~np.isnan(vc); keep = okn & okc
        r = {"intact_row": intact_key, "intact_pooled": r4(auroc(intact, y)), "other_intact_row": other_key, "covered": {"names": int(okn.sum()), "counts": int(okc.sum())}}
        for arm, v in (("names_only", vn), ("counts_only", vc)):
            ok = ~np.isnan(v)
            r[arm] = {"pooled": C.per_state_pooled(cell, v), "ci_persona_whole": boot_cluster_single(v[ok], y[ok], g[ok]),
                      "minus_intact": paired(intact[ok], v[ok], y[ok], g[ok]), "minus_other_intact": paired(other[ok], v[ok], y[ok], g[ok]),
                      "minus_lookup": paired(look[ok], v[ok], y[ok], g[ok]),
                      "matched": {"whole": C.matched_block(cell, v, "PRESENT"), "per_state": {s: C.matched_block(cell, v, "PRESENT", s) for s in STATES}},
                      "matched_absent": {"whole": C.matched_block(cell, v, "ABSENT")}}
        r["counts_minus_names"] = paired(vn[keep], vc[keep], y[keep], g[keep])
        r["counts_minus_names_matched"] = C.paired_matched(cell, vc, vn, "PRESENT")
        r["names_minus_intact_matched"] = C.paired_matched(cell, vn, intact, "PRESENT")
        res["readers"][name] = r
    # predictions on the three strong models (Luna's five-draw row is its row; the draw-1 row is beside)
    P3, P4, P5 = {}, {}, {}
    for name in ("Opus 5 (draw 1)", "GPT-5.6 Sol (draw 1)", "GPT-5.6 Luna (five draws)"):
        r = res["readers"][name]
        if "status" in r:
            P3[name] = P4[name] = P5[name] = {"verdict": "NOT EVALUABLE"}; continue
        d3 = r["names_only"]["minus_intact"]["delta"]; P3[name] = {"delta": d3, "item_ci": C.ci(r["names_only"]["minus_intact"]["item_ci"]), "persona_ci": C.ci(r["names_only"]["minus_intact"]["persona_ci"]), "verdict": "HELD" if abs(d3) <= TOL else "FAILED"}
        d4 = r["counts_minus_names"]; P4[name] = {"delta": d4["delta"], "item_ci": C.ci(d4["item_ci"]), "persona_ci": C.ci(d4["persona_ci"]), "verdict": "HELD" if (d4["delta"] < 0 and d4["both_exclude_zero"]) else "FAILED"}
        ps = r["counts_only"]["matched"]["per_state"]
        P5[name] = {s: {"matched": ps[s]["matched"], "persona_lo": r4(ps[s]["ci_persona"]["ci_lo"]), "ok": bool(ps[s]["matched"] > 0.5 and ps[s]["ci_persona"]["ci_lo"] > 0.5)} for s in ("RETRACTION", "EXPIRY")}
        P5[name]["verdict"] = "HELD" if all(P5[name][s]["ok"] for s in ("RETRACTION", "EXPIRY")) else "FAILED"
    def overall(P):
        vs = [v["verdict"] for v in P.values()]
        if all(v == "NOT EVALUABLE" for v in vs):
            return "NOT EVALUABLE"
        ev = [v for v in vs if v != "NOT EVALUABLE"]
        return ("HELD" if all(v == "HELD" for v in ev) else "FAILED") + ("" if len(ev) == len(vs) else " (on the models run)")
    res["predictions"] = {"P-N3": {"criterion": "names-only within 0.05 of the intact row at the point, whole set, each of the three", "per_model": P3, "verdict": overall(P3)},
                          "P-N4": {"criterion": "counts-only reliably below names-only, whole set, both intervals excluding zero, each of the three", "per_model": P4, "verdict": overall(P4)},
                          "P-N5": {"criterion": "counts-only above 0.50 on retraction and on expiry under the matched metric with the persona interval excluding 0.50, each of the three", "per_model": P5, "verdict": overall(P5)}}
    C.jdump(res, C.RESULTS / "r125_t5_nc.json")
    for name, r in res["readers"].items():
        if "status" in r:
            print(f"  {name:28s} {r['status']}"); continue
        n, c = r["names_only"], r["counts_only"]
        print(f"  {name:28s} intact {r['intact_pooled']:.4f} | names {n['pooled']['whole']:.4f} ({n['minus_intact']['delta']:+.4f}{'*' if n['minus_intact']['both_exclude_zero'] else ''}) matched {n['matched']['whole']['matched']:.4f} "
              f"| counts {c['pooled']['whole']:.4f} ({c['minus_intact']['delta']:+.4f}{'*' if c['minus_intact']['both_exclude_zero'] else ''}) matched {c['matched']['whole']['matched']:.4f} ret {c['matched']['per_state']['RETRACTION']['matched']:.4f} exp {c['matched']['per_state']['EXPIRY']['matched']:.4f} "
              f"| counts minus names {r['counts_minus_names']['delta']:+.4f}{'*' if r['counts_minus_names']['both_exclude_zero'] else ''}")
    for k, v in res["predictions"].items():
        print(f"  {k}: {v['verdict']}  " + "; ".join(f"{n}: {d['verdict']}" for n, d in v["per_model"].items()))


if __name__ == "__main__":
    assert_frozen()
    {"t4": score_t4, "t5": score_t5}[sys.argv[1]]()
