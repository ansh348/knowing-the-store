"""
verify_numbers.py -- assert NUMBERS.md still matches the artifacts it cites.

NUMBERS.md is the canonical record: a figure not in it does not go in a draft.
That only works if the file cannot drift from the JSON it was read off. This
checks both directions for every load-bearing figure:

  1. the value in the results artifact rounds to what NUMBERS.md prints, and
  2. that printed string actually appears in NUMBERS.md.

A transcription slip fails (2); a rescore that moves a number fails (1).

Usage:  python e1_metamemory/tools/verify_numbers.py
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

E1 = Path(__file__).resolve().parents[1]


def jload(p):
    return json.load(io.open(E1 / p, encoding="utf-8"))


SCORES = jload("results/scores_e1.json")
LADDER = jload("results/ladder_scores.json")
REDRAW = jload("results/redraw_scores.json")
MECH = jload("results/mechanism_scores.json")
ECON = jload("results/economics.json")

# (label, value from the artifact, how NUMBERS.md prints it)
CHECKS = [
    ("H2-hard blind", SCORES["H2_hard"]["blind_auroc"], "0.5258"),
    ("H2-hard indexed", SCORES["H2_hard"]["indexed_auroc"], "0.7530"),
    ("H2-hard delta", SCORES["H2_hard"]["delta"], "+0.2272"),
    ("H2-hard n", SCORES["H2_hard"]["n"], "588"),
    ("H2-hard frbank indexed", SCORES["H2_hard_frbank"]["indexed_auroc"], "0.7003"),
    ("H2-hard frbank blind", SCORES["H2_hard_frbank"]["blind_auroc"], "0.4966"),
    ("NOK indexed", SCORES["H_NOK"]["row"]["indexed_auroc"], "0.7339"),
    ("NOK delta", SCORES["H_NOK"]["row"]["delta"], "+0.2393"),
    ("frbank TRUE delta", SCORES["by_backend"]["frbank"]["TRUE"]["delta"], "+0.2386"),
    ("frbank BELIEVED delta", SCORES["by_backend"]["frbank"]["BELIEVED"]["delta"], "+0.2420"),
    ("mem0 TRUE delta", SCORES["by_backend"]["mem0"]["TRUE"]["delta"], "−0.0969"),
    ("amem TRUE delta", SCORES["by_backend"]["amem"]["TRUE"]["delta"], "−0.1065"),
    ("staircase auroc", SCORES["staircase"]["auroc"], "0.7516"),
    ("ladder mini FOK delta", LADDER["P3"]["mini"], "+0.2602"),
    ("ladder luna FOK delta", LADDER["P3"]["luna"], "+0.1682"),
    ("ladder sol FOK delta", LADDER["P3"]["sol"], "+0.0364"),
    ("ladder luna blind NOK (P1)", LADDER["P1"]["point"], "0.5585"),
    ("ladder luna NOK delta (P4)", LADDER["P4"]["delta"], "+0.2940"),
    ("ladder sol blind FOK (P2)", LADDER["P2"]["sol"], "0.8131"),
    ("redraw sol external delta", REDRAW["external"]["redraw"]["delta"], "−0.1046"),
    ("redraw sol external blind", REDRAW["external"]["redraw"]["blind"], "0.9130"),
    ("mech A1 frbank", MECH["SECONDARY_frbank"]["arms"]["A1-counts-jittered"]["auroc"], "0.7018"),
    ("mech A2 frbank", MECH["SECONDARY_frbank"]["arms"]["A2-counts-coarsened"]["auroc"], "0.7015"),
    ("mech A3 frbank", MECH["SECONDARY_frbank"]["arms"]["A3-names-only"]["auroc"], "0.7283"),
    ("mech A3 pooled", MECH["PRIMARY_pooled"]["arms"]["A3-names-only"]["auroc"], "0.8516"),
    ("mech A3 pooled ECE", MECH["PRIMARY_pooled"]["arms"]["A3-names-only"]["ece"], "0.0583"),
    ("mech PN-vs-natural intact", MECH["frbank_pn_vs_natural"]["intact_auroc"], "0.8782"),
    ("mech slot-ablated intact", MECH["slot_ablated"]["intact_auroc"], "0.4972"),
    ("econ mini blind $/1M", ECON["metered_lane"]["E1:BLIND"]["usd_per_1M_calls"], "234"),
    ("econ mini indexed $/1M", ECON["metered_lane"]["E1:INDEXED-TRUE"]["usd_per_1M_calls"], "519"),
]


def main():
    txt = io.open(E1 / "NUMBERS.md", encoding="utf-8").read()
    bad = []
    for label, val, printed in CHECKS:
        s = printed.replace("−", "-").lstrip("+")
        try:
            want = float(s)
        except ValueError:
            bad.append((label, f"unparseable printed value {printed!r}"))
            continue
        dp = len(s.split(".")[1]) if "." in s else 0
        got = round(float(val), dp)
        if abs(got - want) > 10 ** -dp / 2:
            bad.append((label, f"artifact {val!r} rounds to {got}, NUMBERS.md prints {printed}"))
        elif printed not in txt:
            bad.append((label, f"value {printed} does not appear in NUMBERS.md"))
    for label, why in bad:
        print(f"  FAIL  {label}: {why}")
    print(f"\n{len(CHECKS) - len(bad)}/{len(CHECKS)} canonical figures verified against artifacts")
    if bad:
        sys.exit(1)
    print("NUMBERS.md agrees with every artifact it cites.")


if __name__ == "__main__":
    main()
