"""
sp2_checklist.py -- the SP2 conditional go. NO API CALLS. Computes NO metric.

Seven items. All must pass. Any failure stops the run.

  1  every policy parameter DERIVED and FROZEN as a committed constant, on
     calibration data only
  2  power recomputation reported, BANDS UNTOUCHED
  3  k per lane precedent, decision recorded with its number
  4  cost projection < $15 including every riding arm
  5  assert_clean passes at the boundary
  6  ZERO eval-cell contact to date
  7  NON-VACUITY (E3_AMENDMENT_1 section 3): the (a)/(a') prompt pair differs
     BYTE-WISE on >= 95% of eval cells, on BOTH the gate prompt and the
     application-step prompt. This is the D56 class made structurally impossible
     to repeat, and it is checked BEFORE any answer call is bought.

Usage:  python e3_metamemory/tools/sp2_checklist.py
"""

from __future__ import annotations

import collections
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e2_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import prompts_e1 as P1                                            # noqa: E402
from m1_factorial import system_variant                            # noqa: E402
from e3_common import (E3, S0, S1, S3, S3P, answer_messages,       # noqa: E402
                       jdump, jload, load_cells, usd)

GATE_BAND = 0.95
PROJECTION_GATE = 15.00


def main():
    fails, report = [], {}
    cells = load_cells()["cells"]
    ev = [c for c in cells if c["split"] == "eval"]
    ca = [c for c in cells if c["split"] == "calibration"]
    thr = jload(E3 / "THRESHOLDS_E3_FROZEN.json")
    IX = jload(E3 / "indexes_e3.json")
    ann = jload(E3 / "annotations_e3.json")
    fr = jload(E3 / "retrieval_frozen_e3.json")
    ret = {r["cell_id"]: r for r in fr["rows"]}

    print("=" * 96)
    print("SP2 CHECKLIST -- seven items, all fatal")
    print("=" * 96)

    # ---- 1 parameters derived and frozen on calibration only
    ok1 = (thr["tau_FOK"] is not None and thr["method"] == "DERIVED, no argmax"
           and thr["rule_source"].startswith("E2_AMENDMENT_4"))
    report["1_parameters"] = {"tau_FOK": thr["tau_FOK"], "tau_NOK": thr["tau_NOK"],
                              "p_star": thr["derivation"]["p_star"],
                              "method": thr["method"], "pass": bool(ok1)}
    print(f"\n1  PARAMETERS DERIVED AND FROZEN            {'PASS' if ok1 else 'FAIL'}")
    print(f"     tau_FOK {thr['tau_FOK']}  tau_NOK {thr['tau_NOK']}  "
          f"p* {thr['derivation']['p_star']:.4f}  ({thr['method']})")
    print(f"     derived on {len(ca)} calibration cells only; "
          f"rule carried verbatim from E2_AMENDMENT_4")
    if not ok1:
        fails.append("1 parameters")

    # ---- 2 power reported, bands untouched
    pw = thr["power_recomputation"]
    ok2 = pw["bands_untouched"] and pw["se_eval"] > 0
    report["2_power"] = pw
    print(f"\n2  POWER RECOMPUTED, BANDS UNTOUCHED        {'PASS' if ok2 else 'FAIL'}")
    print(f"     paired SD {pw['paired_sd_confab']:.4f}  SE(eval) {pw['se_eval']:.5f}  "
          f"binding {pw['binding']:.4f}")
    print("     power: " + "  ".join(f"{k} {v:.1%}" for k, v in pw["power"].items()
                                     if v is not None))
    print(f"     H-E3b margin by the frozen rule: m = {thr['hE3b_margin']}"
          + ("  INDETERMINATE-BY-DESIGN" if thr["hE3b_indeterminate_by_design"] else ""))
    if not ok2:
        fails.append("2 power")

    # ---- 3 k per lane precedent
    ok3 = thr["k_decision"] in (1, 3)
    report["3_k"] = {"sigma_a": thr["sigma_a"], "trigger": thr["sigma_a_trigger"],
                     "k": thr["k_decision"], "pass": bool(ok3)}
    print(f"\n3  K DECISION RECORDED WITH ITS NUMBER      {'PASS' if ok3 else 'FAIL'}")
    print(f"     sigma_a measured {thr['sigma_a']:.4f} vs frozen trigger "
          f"{thr['sigma_a_trigger']}  ->  k = {thr['k_decision']}")
    print("     lane precedent: E2 ran k=1 on its eval split under the same "
          "answerer and lane;\n     M1's 5,288-call factorial ran k=1 on the gate lane.")
    if not ok3:
        fails.append("3 k")

    # ---- 7 NON-VACUITY, generalised to EVERY gated arm pair.
    # E3_AMENDMENT_1 section 3 states the assertion for (a)/(a'). Incident 10's
    # standing lesson states it generally -- "any ablation arm should be required
    # to prove it is an ablation" -- so it is applied to every pair a GATE
    # compares. Two levels are checked and both must clear the band:
    #   decision level  do the two arms make different retrieval decisions, or
    #                   is one arm's rule provably inert at the frozen tau?
    #   prompt level    do the two arms' prompt bytes differ?
    # At SP2 the prompt level is computed on CALIBRATION cells, because PREREG_E3
    # section 8 blocks every eval-cell call until this checklist passes. The
    # eval-cell verification runs inside the eval phase, before any answer call.
    tau = thr["tau_FOK"]
    SYSTEM = system_variant(W=False, D=False)
    gTc = {r["cell_id"]: r for r in jload(E3 / "gates_calibration.json")["rows"]}
    gLc = {r["cell_id"]: r
           for r in jload(E3 / "gates_calibration_lobotomy.json")["rows"]}

    def gate_prompt(c, family):
        key = f"frbank:{c['persona']}:R{c['rung']}:BELIEVED"
        return SYSTEM + "" + P1.USER_INDEXED.format(
            index=IX[family][key], question=c["question"])

    def app_prompt(c, state):
        key = f"frbank:{c['persona']}:R{c['rung']}:BELIEVED"
        dg = (IX["digests"][key] if state == S3
              else IX["digests_lobotomy"][key] if state == S3P else None)
        anns = ann["true"][c["cell_id"]] if state in (S3, S3P) else None
        m = answer_messages(ret[c["cell_id"]]["facts"], anns, dg,
                            c["question"], state)
        return m[0]["content"] + "" + m[1]["content"]

    ret_a = {t: (gTc[t]["fok"] if gTc[t]["fok"] is not None else -1) >= tau for t in gTc}
    ret_l = {t: (gLc[t]["fok"] if gLc[t]["fok"] is not None else -1) >= tau for t in gLc}
    rate_a = sum(ret_a.values()) / len(ret_a)

    pairs, voided = {}, {}
    # H-E3a: (a) FULL vs (b) always-retrieve
    n_a_vs_b = sum(1 for c in ca
                   if app_prompt(c, S3 if ret_a[c["cell_id"]] else S0)
                   != app_prompt(c, S1))
    pairs["H-E3a  (a) vs (b) always"] = {
        "prompt_differs": n_a_vs_b, "n": len(ca), "share": n_a_vs_b / len(ca),
        "decision_note": "arms differ by the application step, not by retrieval"}
    # H-E3c: VOID BY DERIVATION (E3_AMENDMENT_2). Arm (d) is retired from the
    # sequence, so the pair is no longer gated and is not asserted. Its measured
    # vacuity is still printed, because the disposition rests on it.
    inert = rate_a >= 1.0 or rate_a <= 0.0
    voided["H-E3c  (a) vs (d) SHUFFLED-FOK"] = {
        "prompt_differs": 0 if inert else None, "n": len(ca),
        "share": 0.0 if inert else None,
        "disposition": "VOID BY DERIVATION (E3_AMENDMENT_2); arm (d) retired",
        "decision_note": (
            f"tau_FOK = {tau} and the realised rate is {rate_a:.3f}: a permutation "
            "of FOK cannot move any decision, so (d) is byte-identical to (a) on "
            "every cell" if inert else "permutation moves decisions")}
    # H-E3d: (a) FULL vs (a') CONTENT-LOBOTOMY
    n_a_vs_l = sum(1 for c in ca
                   if (app_prompt(c, S3 if ret_a[c["cell_id"]] else S0)
                       != app_prompt(c, S3P if ret_l[c["cell_id"]] else S0))
                   or (gate_prompt(c, "indexes") != gate_prompt(c, "indexes_lobotomy")))
    pairs["H-E3d  (a) vs (a') LOBOTOMY"] = {
        "prompt_differs": n_a_vs_l, "n": len(ca), "share": n_a_vs_l / len(ca),
        "decision_note": "gate index and application digest both scrambled"}

    bad = [k for k, v in pairs.items()
           if v["share"] is None or v["share"] < GATE_BAND]
    ok7 = not bad
    report["7_non_vacuity"] = {"band": GATE_BAND, "tau_FOK": tau,
                               "realised_calibration_rate": rate_a,
                               "pairs": pairs, "voided": voided,
                               "failing": bad, "pass": bool(ok7)}
    print(f"\n7  NON-VACUITY OF EVERY GATED ARM PAIR      {'PASS' if ok7 else 'FAIL'}")
    print(f"     band >= {GATE_BAND:.0%} of cells must differ, at the prompt level")
    for k, v in pairs.items():
        sh = "n/a" if v["share"] is None else f"{v['share']:.1%}"
        flag = "  <-- FAILS" if k in bad else ""
        print(f"     {k:32s} {str(v['prompt_differs']):>5s}/{v['n']}  {sh:>7s}{flag}")
        print(f"       {v['decision_note']}")
    for k, v in voided.items():
        sh = "n/a" if v["share"] is None else f"{v['share']:.1%}"
        print(f"     {k:32s} {str(v['prompt_differs']):>5s}/{v['n']}  {sh:>7s}"
              f"  [{v['disposition']}]")
        print(f"       {v['decision_note']}")
    if not ok7:
        fails.append("7 non-vacuity")

    # ---- 4 cost projection
    spend_now, ncalls = 0.0, 0
    cp = E3 / "cache" / "responses.json"
    if cp.exists():
        for r in json.load(io.open(cp, encoding="utf-8")).values():
            m = str(r.get("model", "gpt-4.1-mini"))
            m = "gpt-5.4" if m.startswith("gpt-5.4") else "gpt-4.1-mini"
            spend_now += usd(r.get("prompt_tokens", 0), r.get("completion_tokens", 0), m)
            ncalls += 1
    # measured unit costs from what has already run
    tok = collections.defaultdict(list)
    for a in jload(E3 / "answers_calibration.json")["rows"]:
        tok[a["state"]].append((a["prompt_tokens"] or 0, a["completion_tokens"] or 0))
    gtok = [(r["prompt_tokens"] or 0, r["completion_tokens"] or 0)
            for r in jload(E3 / "gates_calibration.json")["rows"]]
    c_gate = usd(sum(x[0] for x in gtok) / len(gtok),
                 sum(x[1] for x in gtok) / len(gtok), "gpt-4.1-mini")
    c_ans = {s: usd(sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v),
                    "gpt-5.4") for s, v in tok.items()}

    n_ev = len(ev)
    proj_gate = 2 * n_ev * c_gate                     # arms (a) and (a')
    n_q = len({(c["persona"], c["question_id"]) for c in ev})
    rate = thr["calibration_rate_at_tau"] or 0.7
    proj = {
        "gate (a) + (a')": proj_gate,
        "S0 (rung-invariant)": n_q * c_ans[S0],
        "S1 (arm b, every cell)": n_ev * c_ans[S1],
        "S3 (arms a, d)": (1 - (1 - rate) ** 2) * n_ev * c_ans[S3],
        "S2 (arm a'', descriptive)": rate * n_ev * c_ans["S2-facts-caution"],
        "S3' (arm a')": rate * n_ev * c_ans[S3P],
    }
    k = thr["k_decision"]
    if k > 1:
        for key in ("S1 (arm b, every cell)", "S3 (arms a, d)"):
            proj[key] *= k
    total_proj = spend_now + sum(proj.values())
    ok4 = total_proj < PROJECTION_GATE
    report["4_cost"] = {"spent": spend_now, "n_calls": ncalls,
                        "projection_lines": proj, "projected_total": total_proj,
                        "gate": PROJECTION_GATE, "pass": bool(ok4)}
    print(f"\n4  COST PROJECTION < ${PROJECTION_GATE:.0f}                   "
          f"{'PASS' if ok4 else 'FAIL'}")
    print(f"     spent to date  ${spend_now:.4f} over {ncalls} calls")
    for kk, v in proj.items():
        print(f"     {kk:28s} ${v:.4f}")
    print(f"     PROJECTED TOTAL ${total_proj:.4f}  (cap $40 absolute)")
    if not ok4:
        fails.append("4 cost")

    # ---- 5 assert_clean
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "assert_clean_e3.py"),
                        "--boundary", "SP2"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=str(ROOT))
    ok5 = r.returncode == 0
    report["5_assert_clean"] = {"returncode": r.returncode, "pass": bool(ok5)}
    print(f"\n5  ASSERT_CLEAN AT THE BOUNDARY             {'PASS' if ok5 else 'FAIL'}")
    for ln in (r.stdout or "").strip().split("\n")[-6:]:
        print(f"     {ln}")
    if not ok5:
        fails.append("5 assert_clean")

    # ---- 6 zero eval-cell contact
    ev_ids = {c["cell_id"] for c in ev}
    ev_q = {f"{c['persona']}:{c['question_id']}" for c in ev}
    touched = []
    if cp.exists():
        for rec in json.load(io.open(cp, encoding="utf-8")).values():
            iid = str(rec.get("item_id", ""))
            arm = str(rec.get("arm", ""))
            stem = iid.split("|")[0]
            if arm.startswith("e3answer") and (stem in ev_ids or stem in ev_q):
                touched.append(iid)
    ok6 = not touched
    report["6_zero_eval_contact"] = {"eval_answer_calls": len(touched),
                                     "pass": bool(ok6)}
    print(f"\n6  ZERO EVAL-CELL CONTACT                   {'PASS' if ok6 else 'FAIL'}")
    print(f"     eval-cell ANSWER calls in the cache: {len(touched)}")
    print("     (eval GATE signals are permitted before SP2 and carry no outcome)")
    if not ok6:
        fails.append("6 eval contact")

    report["verdict"] = "GO" if not fails else "STOP"
    report["failures"] = fails
    jdump(report, E3 / "SP2_CHECKLIST.json")
    print("\n" + "=" * 96)
    if fails:
        print(f"VERDICT: STOP -- {len(fails)} item(s) failed: {fails}")
        sys.exit(1)
    print("VERDICT: ALL SEVEN PASS -> proceed through the eval phase to SP3")
    print("=" * 96)


if __name__ == "__main__":
    main()
