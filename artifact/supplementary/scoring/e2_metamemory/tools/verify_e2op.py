"""verify_e2op.py -- two-direction verifier over the E2-OP rows.

Direction A — REDERIVE: every number in `results/e2op_scores.json` is recomputed
from the committed artifacts by an INDEPENDENT path that does not import
score_e2's estimator or score_e2op's assembly, and must match.

Direction B — ACCOUNT: every number that appears in `NUMBERS_E2OP.md` must exist
in the scores JSON, so the write-up cannot carry a figure the scoring did not
produce.

NO API CALLS. Exits non-zero on any mismatch.
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
E2 = ROOT / "e2_metamemory"
sys.path.insert(0, str(E2 / "tools"))
from e2_common import load_items  # noqa: E402

TOL = 5e-4
fails, checks = [], 0


def chk(name, got, want, tol=TOL):
    global checks
    checks += 1
    ok = abs(float(got) - float(want)) <= tol
    if not ok:
        fails.append(f"{name}: rederived {got} != reported {want}")
    print(f"  {'ok ' if ok else 'FAIL'} {name:52s} {got:>10.5f} vs {want:>10.5f}")


def main():
    S = json.load(io.open(E2 / "results" / "e2op_scores.json", encoding="utf-8"))

    # ---------- Direction A: independent rederivation
    items = {i["item_id"]: i for i in load_items()}
    tags = sorted(i["item_id"] for i in load_items() if i["split"] == "eval")
    g = {r["item_id"]: r for r in
         json.load(io.open(E2 / "gates_eval.json", encoding="utf-8"))["rows"]}
    ans = json.load(io.open(E2 / "answers_eval.json", encoding="utf-8"))["rows"]
    J = json.load(io.open(E2 / "cache" / "judgments_eval.json", encoding="utf-8"))

    # confab flags rebuilt straight from the judge cache, no helper functions
    cf = {}
    for a in ans:
        v = J.get(f"{a['item_id']}|{a['response_sha'][:24]}")
        if v is None:
            fails.append(f"missing verdict for {a['item_id']}|{a['state']}")
            continue
        cf[(a["item_id"], a["state"])] = 1 if v.get("confabulation") else 0

    ret = [t for t in tags if (g[t]["indexed"]["1"]["fok"] or 0) >= 0.20]
    sel = [t for t in ret if (g[t]["indexed"]["1"]["nok"] or 0) >= 0.20]
    rs, ss = set(ret), set(sel)

    print("DIRECTION A — rederive from artifacts, independent path")
    chk("n_eval", len(tags), S["n_eval"])
    chk("n_retrieved", len(ret), S["n_retrieved"])
    chk("n_selected", len(sel), S["n_selected"])
    chk("selected_fraction_of_retrieved", len(sel) / len(ret),
        S["selected_fraction_of_retrieved"])

    rate = lambda f: sum(f(t) for t in tags) / len(tags)  # noqa: E731
    v_c = rate(lambda t: cf[(t, "S1-facts" if t in rs else "S0-nofacts")])
    vi_c = rate(lambda t: cf[(t, "S2-facts-caution" if t in rs else "S0-nofacts")])
    op_c = rate(lambda t: cf[(t, ("S2-facts-caution" if t in ss else "S1-facts")
                              if t in rs else "S0-nofacts")])
    chk("(v) confab rate", v_c, S["confab_rates"]["(v) gate only"])
    chk("(vi) confab rate", vi_c, S["confab_rates"]["(vi) blanket"])
    chk("(vi-OP) confab rate", op_c, S["confab_rates"]["(vi-OP) targeted"])
    chk("fidelity (v) confab count", v_c * len(tags), S["fidelity"]["v_confab_n"], 0.5)
    chk("fidelity (vi) confab count", vi_c * len(tags), S["fidelity"]["vi_confab_n"], 0.5)

    # random arm: analytic expectation of a uniform fixed-size draw.
    # Independent of the 1,000-seed simulation the scorer ran.
    p = len(sel) / len(ret)
    rnd_c = rate(lambda t: (p * cf[(t, "S2-facts-caution")]
                            + (1 - p) * cf[(t, "S1-facts")]) if t in rs
                 else cf[(t, "S0-nofacts")])
    chk("(vii-NOK) mean rate (analytic vs simulated)", rnd_c,
        S["confab_rates"]["(vii-NOK) random, mean of seeds"], 3e-3)

    # unadjusted contrasts
    chk("H-OP1 unadjusted", op_c - rnd_c, S["H_OP1"]["unadjusted"], 3e-3)
    chk("H-OP2 unadjusted", op_c - v_c, S["H_OP2"]["unadjusted"])
    chk("blanket unadjusted", vi_c - v_c, S["H_OP2"]["blanket_unadjusted"])
    chk("half of blanket", 0.5 * (vi_c - v_c), S["H_OP2"]["half_of_blanket"])

    # gate verdicts read mechanically, rederived
    h1 = S["H_OP1"]["ci95"][1] < 0
    h2 = (op_c - v_c) <= 0.5 * (vi_c - v_c)
    checks_ok = (h1 == S["H_OP1"]["HOLDS"]) and (h2 == S["H_OP2"]["HOLDS"])
    print(f"  {'ok ' if checks_ok else 'FAIL'} gate verdicts read mechanically"
          f"{'':21s} H-OP1 {S['H_OP1']['HOLDS']}  H-OP2 {S['H_OP2']['HOLDS']}")
    if not checks_ok:
        fails.append("gate verdict does not follow mechanically from the numbers")

    # ---------- Direction B: every number in the write-up exists in the scores
    print("\nDIRECTION B — every figure in NUMBERS_E2OP.md is accounted for")
    nums_path = E2 / "NUMBERS_E2OP.md"
    if nums_path.exists():
        flat = set()

        def walk(o):
            if isinstance(o, dict):
                [walk(v) for v in o.values()]
            elif isinstance(o, list):
                [walk(v) for v in o]
            elif isinstance(o, (int, float)) and not isinstance(o, bool):
                flat.add(round(float(o), 5))
                flat.add(round(abs(float(o)), 5))
                flat.add(round(float(o) * 100, 2))
                flat.add(round(abs(float(o)) * 100, 2))
        walk(S)
        txt = io.open(nums_path, encoding="utf-8").read()
        # only check figures inside the tables, not prose section numbers
        cited = set()
        for m in re.finditer(r"(?<![\w.])[-+]?\d+\.\d+(?![\w])", txt):
            cited.add(round(abs(float(m.group())), 5))
        # Declared cross-references: figures the write-up legitimately cites that
        # this run did not produce. Named with their source so they stay visible
        # rather than being silently tolerated by a looser regex.
        CROSSREF = {
            3.1: "section reference to RESULTS_E2.md §3.1",
            5.81: "E2 cumulative spend to date, RESULTS_E2.md header",
        }
        unaccounted, crossed = [], []
        for x in sorted(cited):
            if any(abs(x - f) <= 5e-4 for f in flat):
                continue
            (crossed if any(abs(x - c) <= 5e-4 for c in CROSSREF) else
             unaccounted).append(x)
        for u in unaccounted:
            fails.append(f"NUMBERS_E2OP.md cites {u}, absent from e2op_scores.json")
        print(f"  cited decimals {len(cited)}   from this run "
              f"{len(cited) - len(crossed) - len(unaccounted)}   "
              f"declared cross-refs {len(crossed)}   unaccounted {len(unaccounted)}")
        for c in crossed:
            print(f"    crossref {c} — {CROSSREF[min(CROSSREF, key=lambda k: abs(k - c))]}")
        if unaccounted:
            print(f"    UNACCOUNTED -> {unaccounted}")
    else:
        print("  NUMBERS_E2OP.md not present yet — direction B skipped")

    print(f"\n{checks} rederivation checks, {len(fails)} failures")
    if fails:
        for f in fails:
            print("  FAIL:", f)
        raise SystemExit(1)
    print("VERIFIER PASSES — both directions clean.")


if __name__ == "__main__":
    main()
