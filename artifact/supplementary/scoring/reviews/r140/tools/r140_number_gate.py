# -*- coding: utf-8 -*-
"""r140_number_gate.py -- the number gate of R140 (2026-09-23): R139's gate (R134, R135, R137 underneath) with the abstract's E-clause fragment as item 1 words it,
plus the verdicts R140's new words state, re-derived from the raw bounds of reviews/r139/results/equiv_r139.json: under the sibling-name control no reader is
reliably above the lookup and none is shown equivalent (the abstract, 5.2 and the Conclusion); the three stronger readers are not equivalent there ('though not under
the control that fixes list length'). No new number is printed by R140. With --built, R139's numeral-set checks.
Usage: python reviews/r140/tools/r140_number_gate.py [--built]
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "r139" / "tools"))
import r139_number_gate as R  # noqa: E402

R.FRAGS139 = ["Within $0.05$, Luna, Sol and Opus are equivalent to the lookup on the short list; mini sits reliably below it on the matched metric only; for Haiku neither holds",
              "and the three stronger ones are equivalent to it within $0.05$. Under a control that fixes counts and list length, none is reliably above it and none is shown equivalent.",
              "the three stronger readers are equivalent to it within $0.05$, though not under the control that fixes list length."]
_orig = R.checks139


def checks140():
    _orig()
    G = R.G
    E = R.J("reviews/r139/results/equiv_r139.json")
    sb = [r for r in E["rows"] if r["condition"] == "sibling-name control"]
    v = {r["reader"]: R.verdict(r) for r in sb}
    G.chk("abstract / 5.2 / Conclusion (R140 items 1, 3, 7): under the sibling-name control none is reliably above the lookup and none is shown equivalent",
          "5 neither", f"{sum(1 for x in v.values() if x == 'neither')} neither", f"equiv_r139.json sibling-name control rows {v}")
    stronger = {k: x for k, x in v.items() if k.startswith(("GPT-5.6", "Opus"))}
    G.chk("Conclusion (item 7): the three stronger readers not equivalent under the control", "not equivalent", "not equivalent" if all(x != "equivalent" for x in stronger.values()) else "equivalent", str(stronger))
    mt = R.main_text()
    for frag in ("and none shown equivalent", "A list-length cue is uncontrolled there.", "whether the judgment pays for itself is unresolved"):
        G.chk(f"main text carries (R140): {frag}", "present", "present" if frag in mt else "absent", "the built main text")


R.checks139 = checks140

if __name__ == "__main__":
    R.main()
