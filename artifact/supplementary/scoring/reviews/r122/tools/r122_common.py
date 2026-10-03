# -*- coding: utf-8 -*-
"""r122_common.py -- program R122 (the no-human batch): paths, the registration-hash assertion, the recorded gates and the shared
estimators. NO API CALL in this module. Every R122 file lives under reviews/r122/ (the fence of the brief): registrations in
reviews/r122/registrations/, rows in reviews/r122/rows/, results in reviews/r122/results/, the ledger reviews/r122/NUMBERS_R122.md.

Registered text = the bytes of a registration file above its marker line; the sha256 over those bytes is recorded in FREEZE_R122.md and
asserted by every runner and scorer at start (R117's mechanics).
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
R122 = ROOT / "reviews" / "r122"
REGS, ROWS, RESULTS, TOOLS = R122 / "registrations", R122 / "rows", R122 / "results", R122 / "tools"
LEDGER = R122 / "NUMBERS_R122.md"
FREEZE = R122 / "FREEZE_R122.md"
CF2 = ROOT / "r82_counterfactual" / "cf2"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."

for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "reviews/v19/tools", "reviews/v18/tools", "e1_metamemory/tools"):
    sys.path.insert(0, str(ROOT / p))

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

# the recorded rows every task reads (never re-run)
LOOKUP_V2_GATE = 0.7663          # AUX-CF2-NB6-V2, the superseded-names embedding lookup on the 444, v2
LOOKUP_V3_GATE = 0.8756          # AUX-CF2-ALLSTATES-V3, the all-states embedding lookup on the 444, v3
LOOKUP_661_GATE = 0.7484         # AUX-E1R-NB6, the superseded-section embedding lookup on the 661, TRUE (committed form)
LOOKUP_661_CLEAN = 0.7442        # AUX-NB6SWEEP-DECOMP-661, the same list with the empty-section marker removed
MODEL_REACH_104 = 85             # AUX-DS-REACH, MODEL: 85 of 104
MODEL_MEAN_661 = 5.4341906202723145   # AUX-DS-VIEWSIZE, MODEL mean view size over the 661
MODEL_GOLD_IN_VIEW_174 = 65      # AUX-DS-PRESENT, MODEL gold in view
TOL = 0.05


def sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def reg_sha(p: Path) -> str:
    b = Path(p).read_bytes(); i = b.find(FROZEN_END); assert i > 0, f"no marker in {p}"
    return hashlib.sha256(b[:i]).hexdigest()


def reg_bytes(p: Path) -> int:
    b = Path(p).read_bytes(); i = b.find(FROZEN_END); return i


def freeze_table() -> dict:
    """{registration file name: registered-text sha256} as FREEZE_R122.md records it."""
    out = {}
    if not FREEZE.exists():
        return out
    for ln in io.open(FREEZE, encoding="utf-8"):
        if ln.startswith("| ") and "`ADDENDUM_R122" in ln:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            name = cells[1].strip("`"); sha = cells[2].strip("`")
            out[name] = sha
    return out


def assert_frozen(name: str, expected: str | None = None) -> str:
    """Assert the registration's registered-text sha256 equals the freeze record (and `expected` if given). STOP on mismatch."""
    p = REGS / name
    got = reg_sha(p)
    tab = freeze_table()
    assert name in tab, f"{name} not in FREEZE_R122.md -- not frozen, STOP"
    assert got == tab[name], f"REGISTRATION SHA MISMATCH for {name}: {got} != {tab[name]} -- STOP"
    if expected is not None:
        assert got == expected, f"REGISTRATION SHA MISMATCH for {name}: {got} != {expected} -- STOP"
    return got


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=1, sort_keys=True, default=_default)
        f.write("\n")


def _default(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, set):
        return sorted(o)
    raise TypeError(type(o))


def r4(x):
    return round(float(x), 4)


def ci(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"


def load_env():
    for line in io.open(ROOT / ".env", encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def cf2_cell():
    items = jload(CF2 / "cf_cell.json")["items"]
    idx = jload(CF2 / "cf_indexes.json")["indexes"]
    assert len(items) == 444 and sum(it["y_nok"] for it in items) == 148
    return items, idx


def append_ledger(text: str):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(text if text.endswith("\n") else text + "\n")
