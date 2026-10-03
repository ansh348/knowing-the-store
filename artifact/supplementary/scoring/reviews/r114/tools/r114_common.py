# -*- coding: utf-8 -*-
"""r114_common.py -- shared paths, the spec assertion and the ledger append for program R114 (2026-09-17).
Every script asserts the spec hash before it reads an input or makes a call."""
from __future__ import annotations

import hashlib
import io
import json
import os
import pathlib
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = pathlib.Path(__file__).resolve().parents[3]
R114 = ROOT / "reviews" / "r114"
RESULTS = R114 / "results"
SPEC = R114 / "SPEC_R114.md"
SPEC_SHA = "f13b7df47a9e58ebcd345e1d6d2c5b8fcc3a214ceec3da946cff9ca09722555b"
LEDGER = ROOT / "reviews" / "NUMBERS_R114.md"
CEILING = 40.00
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "resp_review/tools", "ds_downstream/tools",
          "r74/tools", "e0_metamemory/tools", "e1_metamemory/tools", "r85_graphiti", "r85_graphiti/g10", "side_experiments/tools"):
    sys.path.insert(0, str(ROOT / p))


def assert_spec():
    h = hashlib.sha256(SPEC.read_bytes()).hexdigest()
    assert h == SPEC_SHA, f"SPEC_R114.md sha256 {h} != {SPEC_SHA} -- the spec changed after its hash was ledgered; STOP"
    assert "AUX-R114-SPEC-FREEZE" in LEDGER.read_text(encoding="utf-8"), "the spec freeze is not ledgered -- STOP"


def J(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(obj, p):
    p = pathlib.Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=False))


def sha16(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:16]


def sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def ledger_append_to(path, text):
    with io.open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(text)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    print(text)


def ledger_append(text):
    ledger_append_to(LEDGER, text)


def r4(x):
    return None if x is None else round(float(x), 4)
