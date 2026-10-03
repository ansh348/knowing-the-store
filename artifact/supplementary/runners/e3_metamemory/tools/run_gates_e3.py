"""
run_gates_e3.py -- the L1W0D0 gate signal for one split. Counts only on stdout.

SIGNALS, NOT DECISIONS. Thresholds are applied later, by the derivation and by
the scorer. This script never compares a signal to a threshold.

THE GATE (PREREG_E3 section 4.5):
  L1  E1's intact index, rendered per rung by build_indexes.py. RENDERER LOCK
      honoured -- L is an index factor and L1 is the unmodified renderer.
  W0  the two worked-example paragraphs deleted from prompts_e1.SYSTEM.
  D0  the two-step decomposition collapsed into a single `nok` judgment.
  W0 and D0 are `m1_factorial.system_variant(W=False, D=False)` REUSED VERBATIM,
  not re-implemented, so the E3 gate is byte-comparable to M1's winning cell.

Lane: gpt-4.1-mini, temperature 0, seed 42, k=1 -- E1's frozen decoding, unchanged.
k=1 rests on lane precedent: E2 ran k=1 on its eval split under the same lane, and
M1's 5,288-call factorial ran k=1 licensed by the lane's 46/50 k=3 stability.

ARM (E3_AMENDMENT_1 section 2.3). The index is consumed by the gate, so arm (a')
CONTENT-LOBOTOMY needs its OWN elicitation over the scrambled index. --arm true
is arms (a)/(a'')/(d); --arm lobotomy is arm (a').

Output: e3_metamemory/gates_<split>[_lobotomy].json -- signals only.

Usage:  python e3_metamemory/tools/run_gates_e3.py --split calibration --arm true
"""

from __future__ import annotations

import collections
import concurrent.futures as cf
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e2_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import e3_api as api                                               # noqa: E402
import prompts_e1 as P1                                            # noqa: E402
from m1_factorial import system_variant                            # noqa: E402
from e3_common import E3, jdump, jload, load_cells, sha            # noqa: E402

WORKERS = 12
E1_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"
CELL = "L1W0D0"


def clamp(v):
    try:
        return min(100.0, max(0.0, float(v))) / 100.0
    except (TypeError, ValueError):
        return None


def main():
    split = sys.argv[sys.argv.index("--split") + 1]
    arm = sys.argv[sys.argv.index("--arm") + 1] if "--arm" in sys.argv else "true"
    assert split in ("calibration", "eval")
    assert arm in ("true", "lobotomy")
    IXKEY = "indexes" if arm == "true" else "indexes_lobotomy"
    SUFFIX = "" if arm == "true" else "_lobotomy"

    got = P1.texts_sha256()
    assert got == E1_TEXTS_SHA, f"E1 frozen prompts changed: {got}"
    SYSTEM = system_variant(W=False, D=False)
    print(f"E1 prompt texts sha verified {got[:16]}...")
    print(f"gate cell {CELL}: system {len(SYSTEM)} chars, sha {sha(SYSTEM)[:16]}...")

    IX = jload(E3 / "indexes_e3.json")
    ash = IX["artifact_sha256"] if arm == "true" else IX["artifact_sha256_lobotomy"]
    print(f"arm={arm}  index family `{IXKEY}`  artifact sha {ash[:16]}...  "
          f"{IX['n_indexes']} indexes")

    cells = [c for c in load_cells()["cells"] if c["split"] == split]
    print(f"split={split}  cells={len(cells)}  k=1")

    def run(c):
        key = f"frbank:{c['persona']}:R{c['rung']}:BELIEVED"
        msgs = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": P1.USER_INDEXED.format(
                    index=IX[IXKEY][key], question=c["question"])}]
        r = api.call(c["cell_id"], f"e3gate-{CELL}{SUFFIX}", msgs)
        o = api.parse_json(r["content"]) or {}
        api.check_cap()
        return {"cell_id": c["cell_id"], "persona": c["persona"],
                "rung": c["rung"], "question_id": c["question_id"],
                "label": c["label"], "split": split, "kind": c["kind"],
                "fok": clamp(o.get("fok")), "nok": clamp(o.get("nok")),
                "arm": arm,
                "index_sha": IX["meta"][key][
                    "sha256" if arm == "true" else "sha256_lobotomy"],
                "cached": r["cached"],
                "prompt_tokens": r.get("prompt_tokens"),
                "completion_tokens": r.get("completion_tokens")}

    out = []
    try:
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
            for n, rec in enumerate(ex.map(run, cells), 1):
                out.append(rec)
                if n % 200 == 0:
                    api.flush()
                    print(f"  {n}/{len(cells)}  ${api.spend()[0]:.4f}", flush=True)
    finally:
        api.flush()

    miss = sum(1 for r in out if r["fok"] is None)
    jdump({"split": split, "arm": arm, "gate_cell": CELL, "k": 1,
           "system_sha256": sha(SYSTEM), "e1_texts_sha256": got,
           "index_artifact_sha256": ash,
           "n": len(out), "n_parse_fail": miss, "rows": out},
          E3 / f"gates_{split}{SUFFIX}.json")

    per_rung = collections.Counter(r["rung"] for r in out)
    total, ncalls = api.spend()
    print(f"  per rung: {dict(sorted(per_rung.items()))}")
    print(f"  parse failures: {miss}")
    print(f"  cumulative metered ${total:.4f} over {ncalls} cached calls")
    print(f"wrote gates_{split}{SUFFIX}.json -- signals only, no decision, no score")


if __name__ == "__main__":
    main()
