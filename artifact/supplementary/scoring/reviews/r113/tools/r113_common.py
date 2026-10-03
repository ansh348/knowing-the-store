# -*- coding: utf-8 -*-
"""r113_common.py -- shared paths, the spec assertion and the ledger append for program R113 (2026-09-16).
NO MODEL CALL. $0. Every script asserts the spec hash before it reads an input."""
from __future__ import annotations

import hashlib
import io
import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[3]
R113 = ROOT / "reviews" / "r113"
RESULTS = R113 / "results"
SPEC = R113 / "SPEC_R113.md"
SPEC_SHA = "a315511d5291074ba172c4aa3c4e12c70ba600747280cfac0fe05ba82699acb6"
LEDGER = ROOT / "reviews" / "NUMBERS_R113.md"
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "resp_review/tools", "ds_downstream/tools",
          "r74/tools", "e0_metamemory/tools", "e1_metamemory/tools"):
    sys.path.insert(0, str(ROOT / p))


def assert_spec():
    h = hashlib.sha256(SPEC.read_bytes()).hexdigest()
    assert h == SPEC_SHA, f"SPEC_R113.md sha256 {h} != {SPEC_SHA} -- the spec changed after its hash was ledgered; STOP"
    assert "AUX-R113-SPEC-FREEZE" in LEDGER.read_text(encoding="utf-8"), "the spec freeze is not ledgered -- STOP"


def J(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(obj, p):
    p = pathlib.Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=False))


def sha16(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:16]


def ledger_append(text):
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(text)
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


def r4(x):
    return None if x is None else round(float(x), 4)
