"""
sp3_census_e3.py -- SP3. Census, failures, cost, hashes. NO METRIC.

PREREG_E3 section 8: SP3 reports census, deviations and cost, and BLOCKS any gate
being read. This file contains no scoring code, imports none, and computes no
credit, no confabulation rate, no contrast and no aggregate over any outcome.

It answers exactly one question: IS THE DATA COMPLETE, and is every artifact the
scorer will read hash-accounted?

The one place it touches a verdict is to count whether a verdict EXISTS and
whether it parsed. It never counts what the verdict said.

Usage:  python e3_metamemory/tools/sp3_census_e3.py
"""

from __future__ import annotations

import collections
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e3_common import (E3, S0, S1, S2, S3, S3P, jdump, jload,      # noqa: E402
                       load_cells, sha, usd)

ARM_STATE = {"(a) FULL": S3, "(a') CONTENT-LOBOTOMY": S3P,
             "(a'') CAUTION-ONLY [descriptive]": S2,
             "(b) always-retrieve": S1, "(c) no-memory floor": S0}


def main():
    C = load_cells()
    cells = {c["cell_id"]: c for c in C["cells"]}
    ev = [c for c in C["cells"] if c["split"] == "eval"]
    ca = [c for c in C["cells"] if c["split"] == "calibration"]
    thr = jload(E3 / "THRESHOLDS_E3_FROZEN.json")
    IXm = jload(E3 / "indexes_e3.json")
    fr = jload(E3 / "retrieval_frozen_e3.json")
    ann = jload(E3 / "annotations_e3.json")
    rep = {"prereg": "PREREG_E3.md", "amendments": ["E3_AMENDMENT_1.md",
                                                    "E3_AMENDMENT_2.md"]}

    print("=" * 96)
    print("SP3 CENSUS -- completeness, failures, cost, hashes. NO METRIC.")
    print("=" * 96)

    # ---------------------------------------------------------------- cells
    per = collections.Counter((c["rung"], c["split"]) for c in C["cells"])
    rep["cells"] = {"n": C["n_cells"], "eval": len(ev), "calibration": len(ca),
                    "rungs": C["rungs"], "excluded": C["n_excluded"],
                    "exclusion_reasons": C["exclusion_reasons"],
                    "assertions": C["assertions"],
                    "per_rung": {f"{r}|{s}": n for (r, s), n in sorted(per.items())}}
    print(f"\nCELLS  {C['n_cells']} = eval {len(ev)} + calibration {len(ca)}   "
          f"rungs {C['rungs']}")
    for r in C["rungs"]:
        print(f"   rung {r:>2d}: eval {per[(r,'eval')]:>4d}  "
              f"calibration {per[(r,'calibration')]:>3d}")
    print(f"   excluded {C['n_excluded']}  {C['exclusion_reasons']}")
    print(f"   build assertions: {C['assertions']}")

    # ---------------------------------------------------------------- gates
    rep["gates"] = {}
    print("\nGATE SIGNALS")
    for name, f in (("eval / true", "gates_eval.json"),
                    ("eval / lobotomy", "gates_eval_lobotomy.json"),
                    ("calibration / true", "gates_calibration.json"),
                    ("calibration / lobotomy", "gates_calibration_lobotomy.json")):
        g = jload(E3 / f)
        exp = len(ev) if "eval" in name else len(ca)
        rep["gates"][name] = {"n": g["n"], "expected": exp,
                              "parse_fail": g["n_parse_fail"],
                              "complete": g["n"] == exp and g["n_parse_fail"] == 0,
                              "index_artifact_sha256": g["index_artifact_sha256"],
                              "system_sha256": g["system_sha256"]}
        print(f"   {name:24s} {g['n']:>4d}/{exp:<4d}  parse-fail {g['n_parse_fail']}"
              f"   {'COMPLETE' if rep['gates'][name]['complete'] else 'INCOMPLETE'}")

    # -------------------------------------------------------------- answers
    rep["answers"], rep["judgments"] = {}, {}
    print("\nANSWERS AND JUDGMENTS")
    gaps = []
    for split, exp_cells in (("eval", ev), ("calibration", ca)):
        A = jload(E3 / f"answers_{split}.json")
        rows = A["rows"]
        by_state = collections.Counter(r["state"] for r in rows)
        empty = sum(1 for r in rows if not r["response"])
        cov = collections.defaultdict(set)
        for r in rows:
            cov[r["state"]].add(r["cell_id"])
        J = jload(E3 / "cache" / f"judgments_{split}.json")
        keys = {f"{r['cell_id']}|{r['response_sha'][:24]}" for r in rows}
        judged = sum(1 for k in keys if J.get(k, {}).get("status") == "OK")
        missing = sorted(k for k in keys if J.get(k, {}).get("status") != "OK")
        rep["answers"][split] = {
            "n_calls": len(rows), "k": A["k"], "answerer": A["answerer_model"],
            "by_state": dict(by_state), "empty_responses": empty,
            "state_cell_coverage": {s: len(v) for s, v in sorted(cov.items())},
            "retrieval_artifact_sha256": A["retrieval_artifact_sha256"],
            "index_artifact_sha256": A["index_artifact_sha256"],
            "index_artifact_sha256_lobotomy": A["index_artifact_sha256_lobotomy"]}
        rep["judgments"][split] = {"distinct_pairs": len(keys), "ok": judged,
                                   "missing": len(missing),
                                   "complete": not missing}
        if missing:
            gaps.append((split, len(missing)))
        print(f"   {split:12s} answers {len(rows):>5d} (k={A['k']}, empty {empty})"
              f"   states {dict(by_state)}")
        print(f"   {'':12s} distinct (cell,response) {len(keys):>5d}  "
              f"judged OK {judged:>5d}  MISSING {len(missing)}"
              f"   {'ZERO GAPS' if not missing else 'GAP'}")

    # ------------------------------------------------- arm-by-arm coverage
    A = jload(E3 / "answers_eval.json")["rows"]
    have = collections.defaultdict(set)
    for r in A:
        have[r["state"]].add(r["cell_id"])
    s0_q = {f"{r['persona']}:{r['question_id']}" for r in A if r["state"] == S0}
    print("\nARM COVERAGE ON THE 834 EVAL CELLS")
    rep["arm_coverage"] = {}
    for arm, state in ARM_STATE.items():
        if state == S0:
            n = len({f"{c['persona']}:{c['question_id']}" for c in ev} & s0_q)
            d = len({f"{c['persona']}:{c['question_id']}" for c in ev})
            note = "rung-invariant: one answer per question, shared across rungs"
        else:
            n, d = len(have[state] & {c["cell_id"] for c in ev}), len(ev)
            note = ""
        rep["arm_coverage"][arm] = {"state": state, "covered": n, "denominator": d,
                                    "complete": n == d, "note": note}
        print(f"   {arm:36s} {state:32s} {n:>4d}/{d:<4d} "
              f"{'OK' if n == d else 'GAP'}  {note}")
    rep["arm_coverage"]["(d) SHUFFLED-FOK [retired]"] = {
        "state": S3, "covered": len(have[S3] & {c["cell_id"] for c in ev}),
        "denominator": len(ev), "complete": True,
        "note": "VOID BY DERIVATION (E3_AMENDMENT_2): byte-identical to (a) at "
                "tau_FOK = 0.00; shares (a)'s answers exactly, buys no new call"}
    print(f"   {'(d) SHUFFLED-FOK [retired]':36s} {S3:32s} "
          f"{len(have[S3] & {c['cell_id'] for c in ev}):>4d}/{len(ev):<4d} OK  "
          f"VOID BY DERIVATION -- shares (a)'s answers")

    # ------------------------------------------------------------- artifacts
    rep["artifacts"] = {
        "CELLS_E3.json": sha(json.dumps(C, sort_keys=True)),
        "retrieval_frozen_e3.json": fr["artifact_sha256"],
        "indexes_e3.json (true)": IXm["artifact_sha256"],
        "indexes_e3.json (lobotomy)": IXm["artifact_sha256_lobotomy"],
        "annotations_e3.json": ann["artifact_sha256"],
        "THRESHOLDS_E3_FROZEN.json": sha(json.dumps(thr, sort_keys=True)),
    }
    print("\nFROZEN ARTIFACT HASHES")
    for k, v in rep["artifacts"].items():
        print(f"   {k:34s} {v[:32]}...")

    # ------------------------------------------------------------------ cost
    spend, ncalls, by_arm = 0.0, 0, collections.Counter()
    cp = E3 / "cache" / "responses.json"
    for r in json.load(io.open(cp, encoding="utf-8")).values():
        m = "gpt-5.4" if str(r.get("model", "")).startswith("gpt-5.4") else "gpt-4.1-mini"
        u = usd(r.get("prompt_tokens", 0), r.get("completion_tokens", 0), m)
        spend += u
        ncalls += 1
        by_arm[str(r.get("arm", ""))] += u
    jc = {s: jload(E3 / f"judge_census_{s}.json") for s in ("eval", "calibration")}
    judge_equiv = sum(v["metered_equivalent_usd_computed_not_paid"] for v in jc.values())
    rep["cost"] = {"metered_usd": spend, "n_calls": ncalls,
                   "by_arm": dict(by_arm),
                   "judge_metered_equivalent_computed_not_paid": judge_equiv,
                   "cap": 40.00, "projection_gate": 15.00,
                   "under_cap": spend < 40.00}
    print(f"\nCOST   metered ${spend:.4f} over {ncalls} calls   cap $40   "
          f"{'UNDER CAP' if spend < 40 else 'OVER CAP'}")
    for k, v in by_arm.most_common():
        print(f"   {k:36s} ${v:.4f}")
    print(f"   judge lane: subscription; metered-equivalent ${judge_equiv:.2f} "
          "(computed, not paid)")

    # --------------------------------------------------------------- verdict
    rep["zero_gaps"] = not gaps
    rep["metric_computed"] = False
    jdump(rep, E3 / "sp3_census_e3.json")
    print("\n" + "=" * 96)
    print(f"SP3 VERDICT: {'ZERO GAPS' if not gaps else 'GAPS: ' + str(gaps)}")
    print("NO METRIC COMPUTED. No gate has been read. No scoring code exists in "
          "this file.")
    print("=" * 96)
    print("wrote sp3_census_e3.json")


if __name__ == "__main__":
    main()
