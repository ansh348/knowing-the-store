"""
verify_numbers_e3.py -- the two-direction verifier, extended over the E2/E3 additions.

Same device as `e1_metamemory/tools/verify_numbers.py`, which is imported and RUN
FIRST so the E1 sections keep their guarantee. For every added figure this checks
BOTH directions:

  1. the value in the results artifact rounds to what NUMBERS.md prints, and
  2. that printed string actually appears in NUMBERS.md.

A transcription slip fails (2); a rescore that moves a number fails (1).

It additionally enforces the annotation rule for the four figures that carry a
warning: a figure whose annotation is part of its value fails if the annotation's
own key phrase is missing from the file.

Usage:  python e3_metamemory/tools/verify_numbers_e3.py
"""

from __future__ import annotations

import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"
E2 = ROOT / "e2_metamemory"
E3 = ROOT / "e3_metamemory"


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


E2S = jload(E2 / "results" / "e2_scores.json")
E3S = jload(E3 / "results" / "e3_scores.json")
FOR = jload(E3 / "results" / "forensic_e3.json")
FIG = jload(E3 / "results" / "q1_figure_data.json")
I2 = jload(E3 / "results" / "i2_precondition.json")
THR = jload(E3 / "THRESHOLDS_E3_FROZEN.json")
P4 = jload(E3 / "probes" / "p4_d44_price_fix.json")
P3 = jload(E3 / "probes" / "p3_index_maintenance.json")
BR = jload(E2 / "believed_recall.json")
JS = jload(E3 / "judge_spotcheck_e3.json")
CELLS = jload(E3 / "CELLS_E3.json")

g2 = {g["name"]: g for g in E2S["gates"]}
seq = {g["name"]: g for g in E3S["sequence"]}
strat = {s["stratum"]: s for s in FIG["strata"]}
q4 = FOR["Q4"]
q6 = {r["rung"]: r for r in FOR["Q6"]["rows"]}

CHECKS = [
    # ---- 15. E2 verdicts
    ("E2 n_eval", E2S["n_eval"], "529"),
    ("E2 H-C2 adjusted", g2["H-C2"]["confab"]["adjusted"], "-0.0579"),
    ("E2 H-C2 CI lo", g2["H-C2"]["confab"]["ci_lo"], "-0.0874"),
    ("E2 H-C2 CI hi", g2["H-C2"]["confab"]["ci_hi"], "-0.0307"),
    ("E2 H-C2 credit", g2["H-C2"]["credit_noninferiority"]["adjusted"], "+0.0303"),
    ("E2 H-C1a rate", g2["H-C1a"]["retrieval_rate"], "0.684"),
    ("E2 never credit", E2S["policy_table"]["ii"]["credit"], "0.5822"),
    ("E2 attribution credit", E2S["attribution_vii"]["credit"]["adjusted"], "+0.0522"),
    ("E2 attribution confab", E2S["attribution_vii"]["confab"]["adjusted"], "+0.0073"),
    ("E2 M1 best cell", E2S["M1"]["cells"]["L1W0D0"]["auroc"], "0.7958"),
    ("E2 believed entry recall", BR["entry_level"]["recall"], "0.615"),
    ("E2 believed event recall", BR["event_level"]["recall"], "0.783"),
    # ---- 16. economics
    ("E2 (v) corrected uncached", P4["new"]["v"]["cost"] * 1e6, "1466"),
    ("E2 (v) corrected cached", P4["new"]["v"]["cost_cached"] * 1e6, "1060"),
    ("E2 (i) corrected", P4["new"]["i"]["cost"] * 1e6, "959"),
    ("E2 (ii) corrected", P4["new"]["ii"]["cost"] * 1e6, "421"),
    # ---- 17. E3 verdicts
    ("E3 n_eval", E3S["n_eval"], "834"),
    ("E3 tau_FOK", THR["tau_FOK"], "0.00"),
    ("E3 p_star", THR["derivation"]["p_star"], "0.2011"),
    ("E3 L", THR["derivation"]["loss_ABSENT"], "0.1042"),
    ("E3 H-E3a adjusted", seq["H-E3a"]["adjusted"], "-0.0091"),
    ("E3 H-E3a CI lo", seq["H-E3a"]["ci_lo"], "-0.0299"),
    ("E3 H-E3a CI hi", seq["H-E3a"]["ci_hi"], "+0.0143"),
    ("E3 H-E3b credit", seq["H-E3b"]["adjusted"], "+0.0135"),
    ("E3 H-E3d adjusted", seq["H-E3d"]["adjusted"], "+0.0094"),
    ("E3 (b) confab", E3S["arm_table"]["(b) always-retrieve"]["confab"], "0.0971"),
    ("E3 (a) confab", E3S["arm_table"]["(a) FULL"]["confab"], "0.0851"),
    ("E3 (a') confab", E3S["arm_table"]["(a') CONTENT-LOBOTOMY"]["confab"], "0.0827"),
    ("E3 (a'') confab", E3S["arm_table"]["(a'') CAUTION-ONLY"]["confab"], "0.0767"),
    ("E3 (c) credit", E3S["arm_table"]["(c) no-memory floor"]["credit"], "0.5815"),
    ("E3 maintain us/write MEAN", P3["maintain_us_total"] / 390, "1.11"),
    ("E3 maintain us/write MEDIAN", P3["maintain_us_per_write_median"], "1.00"),
    ("E3 judge confab weighted",
     JS["population_weighted"]["confab_agreement"], "0.880"),
    ("E3 judge four-way weighted",
     JS["population_weighted"]["four_way_agreement"], "0.715"),
    ("E3 cells", CELLS["n_cells"], "1021"),
    # ---- 18. forensic
    ("Q1 predicted", FIG["predicted_at_E3_mix"]["est"] * 100, "-3.09"),
    ("Q1 predicted lo", FIG["predicted_at_E3_mix"]["lo"] * 100, "-5.56"),
    ("Q1 predicted hi", FIG["predicted_at_E3_mix"]["hi"] * 100, "-0.79"),
    ("Q1 observed a''", FIG["observed_E3"][
        "(a'') vs (b) -- pure-caution analogue"]["est"] * 100, "-2.31"),
    ("Q1 residual vs a", FIG["residuals"]["vs_a"] * 100, "+2.18"),
    ("Q1 stratum ablation", strat["ablation/unwritten-absent"]["effect"] * 100, "-10.16"),
    ("Q1 stratum natural", strat["natural-absent"]["effect"] * 100, "-0.83"),
    ("Q1 stratum PN", strat["PN"]["effect"] * 100, "-10.98"),
    ("Q1 share ablation E2", strat["ablation/unwritten-absent"]["share_E2"], "0.353"),
    ("Q1 share natural E3", strat["natural-absent"]["share_E3"], "0.580"),
    ("Q3 habitat n", FOR["Q3"]["habitat_n"], "18"),
    ("Q4 PN delta", q4["PN"]["delta"]["est"], "+0.0909"),
    ("Q4 PN CI lo", q4["PN"]["delta"]["lo"], "+0.0392"),
    ("Q4 PRESENT delta", q4["PRESENT"]["delta"]["est"], "-0.0400"),
    ("Q6 contamination r32", q6[32]["contamination"], "0.0064"),
    ("Q6 store ratio", q6[32]["store_size"] / q6[14]["store_size"], "2.22"),
    ("Q6 raw ratio", FOR["Q6"]["raw_ratio_32_over_14"], "2.78"),
    ("Q6 standardised ratio", FOR["Q6"]["standardised_ratio_32_over_14"], "2.06"),
    ("I2 AUROC", I2["precondition"]["auroc"], "0.7775"),
    ("I2 q_star", I2["derivation"]["q_star"], "0.3796"),
    ("I2 max precision", I2["derivation"]["max_calibration_pn_precision"], "0.2660"),
    ("I2 calibration B", I2["derivation"]["B_ci"]["est"], "-0.0345"),
    ("I2 calibration B lo", I2["derivation"]["B_ci"]["lo"], "-0.0707"),
    ("I2 calibration B hi", I2["derivation"]["B_ci"]["hi"], "-0.0048"),
]

# a figure whose annotation is part of its value fails if the annotation is absent
ANNOTATIONS = [
    ("H-C2's mix condition",
     "36.0% of E2's primary eval set is absence manufactured by the ablation"),
    ("Q4's split instability",
     "Both intervals exclude zero in opposite directions"),
    ("judge reliability",
     "Credit-based figures inherit the second number"),
    ("forensic exploratory banner",
     "Every figure in this section is EXPLORATORY"),
]


def main():
    print("running the E1 verifier first, unchanged")
    r = subprocess.run([sys.executable, str(E1 / "tools" / "verify_numbers.py")],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", cwd=str(ROOT))
    print("  " + (r.stdout or "").strip().split("\n")[-1])
    if r.returncode != 0:
        print("  E1 VERIFIER FAILED -- refusing to verify the additions")
        sys.exit(1)

    txt = io.open(E1 / "NUMBERS.md", encoding="utf-8").read()
    bad = []
    for label, val, printed in CHECKS:
        s = printed.replace("−", "-").replace(",", "").lstrip("+")
        try:
            want = float(s)
        except ValueError:
            bad.append((label, f"unparseable printed value {printed!r}"))
            continue
        dp = len(s.split(".")[1]) if "." in s else 0
        got = round(float(val), dp)
        if abs(got - want) > 10 ** -dp / 2:
            bad.append((label,
                        f"artifact {val!r} rounds to {got}, NUMBERS.md prints {printed}"))
        elif printed not in txt:
            bad.append((label, f"value {printed} does not appear in NUMBERS.md"))
    for label, phrase in ANNOTATIONS:
        if phrase not in txt:
            bad.append((f"ANNOTATION: {label}",
                        f"the annotation that is part of the value is missing: "
                        f"{phrase!r}"))
    for label, why in bad:
        print(f"  FAIL  {label}: {why}")
    n = len(CHECKS) + len(ANNOTATIONS)
    print(f"\n{n - len(bad)}/{n} E2/E3 canonical figures and annotations verified "
          f"against artifacts, both directions")
    if bad:
        sys.exit(1)
    print("NUMBERS.md agrees with every E2/E3 artifact it cites, and every "
          "mandatory annotation is present.")


if __name__ == "__main__":
    main()
