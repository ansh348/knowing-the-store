"""
leakscreen_v3.py -- the deterministic half of the ADDENDUM_R82 section 5 leakage screen,
run retroactively at R96 (2026-09-12) over every one of the 90 v3 indexes (and the 90 v2
indexes beside them). NO MODEL CALL IS MADE.

WHAT WAS REGISTERED. ADDENDUM_R82 section 5: "The existing leakage screen (`ladder_e1.py`, 30
items, threshold 3, seed 42) runs on a sample of the 90 v3 indexes and must return at most 3
of 30 correct." Section 9 reserved `AUX-R82-CF-LEAKSCREEN`. It never ran and was never
ledgered (reviews/CF2_SCOPE.md finding 4).

WHAT ladder_e1 IS. Its SCORING is deterministic: `exp4_witnesses.supports_correct(response,
gold)`, >=2 shared content tokens AND >=50% coverage of the gold's content tokens, no judge.
Its ANSWERS are not: each item is one `api.call` with the frozen LEAKAGE prompt, asking the
model to answer the question from the index alone. R96 runs under a no-model-call rule, so
this script runs the deterministic half and nothing else.

WHAT RUNS HERE. The registered scorer is applied to the index text itself:
`supports_correct(index_text, entry_text)`. That asks, line for line, the question the screen
exists to ask: does the index carry the answer's content tokens at the scorer's own threshold?
A model reading the index alone cannot be scored correct on an item whose index does not
satisfy this, short of guessing from the question, so on the index side this bounds the
registered screen from above. It does NOT replace it: D-R82-6 records that the model-mediated
screen has not run.

GOLD. The CF cell's questions were drafted from the slot path alone and carry no
`correct_answer` field. The gold used is the pair's `entry_text` from cf_pairs.json, the
stored value the question targets (the entry that becomes PRESENT / ABSENT / PN across the
three versions).

SAMPLING, reproduced for the record. ladder_e1 samples 30 PRESENT items per cell with
`random.Random(42).sample(pool_sorted_by_item_id, 30)`. The CF cell has exactly 30 PRESENT
items, so the seeded sample is the whole PRESENT pool; it is drawn anyway and recorded, and
the ABSENT and PN versions are screened as well because it costs nothing.

INSPECTION DUMP (ladder_e1's D18 idea). For every index, the lines sharing a content token
with the gold are listed with the tokens they share, so a reader can see what the scorer saw.

Output: results/leakscreen_v3.json. Exit 1 iff the registered cell (PRESENT x v3) leaks.

Usage:  python r82_counterfactual/tools/leakscreen_v3.py
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R82 = ROOT / "r82_counterfactual"
sys.path.insert(0, str(ROOT / "analysis" / "ontology_validation"))
from exp4_witnesses import supports_correct, toks  # noqa: E402  (the scorer of record)

N = 30
THRESHOLD = 3          # a cell leaks iff MORE than this many of N score correct
SEED = 42
ARMS = ("v2", "v3")
VERSIONS = ("PRESENT", "ABSENT", "PN")
MAX_LINES = 14


def shared_lines(index_text: str, gold: str):
    g = toks(gold)
    out = []
    for n, line in enumerate(index_text.splitlines(), 1):
        hit = sorted(g & toks(line))
        if hit:
            out.append({"line_no": n, "line": line.rstrip()[:160], "gold_tokens_on_line": hit})
    out.sort(key=lambda d: (-len(d["gold_tokens_on_line"]), d["line_no"]))
    return out[:MAX_LINES]


def main() -> int:
    idx_path = R82 / "cf_indexes.json"
    raw = idx_path.read_bytes()
    idx_doc = json.loads(raw.decode("utf-8"))
    indexes = idx_doc["indexes"]
    cell = json.loads((R82 / "cf_cell.json").read_text(encoding="utf-8"))["items"]
    pairs = {p["pair_id"]: p for p in json.loads((R82 / "cf_pairs.json").read_text(encoding="utf-8"))["pairs"]}

    pool = sorted((it for it in cell if it["label"] == "PRESENT"), key=lambda it: it["item_id"])
    if len(pool) != N:
        raise SystemExit(f"expected {N} PRESENT items, found {len(pool)}")
    sample = sorted(random.Random(SEED).sample(pool, N), key=lambda it: it["item_id"])
    sample_ids = [it["item_id"] for it in sample]

    cells = {}
    for version in VERSIONS:
        items = sorted((it for it in cell if it["version"] == version), key=lambda it: it["item_id"])
        for arm in ARMS:
            rows = []
            for it in items:
                gold = pairs[it["pair_id"]]["entry_text"]
                text = indexes[it["item_id"]][arm]
                g = toks(gold)
                hit = sorted(g & toks(text))
                correct = supports_correct(text, gold)
                rows.append({
                    "item_id": it["item_id"], "pair_id": it["pair_id"], "persona": it["persona"],
                    "state": it["state"], "question": it["question"], "gold_entry_text": gold,
                    "gold_content_tokens": len(g), "tokens_shared_with_index": hit,
                    "coverage": round(len(hit) / len(g), 4) if g else None,
                    "correct": bool(correct),
                    "shared_lines": shared_lines(text, gold) if hit else [],
                })
            n_correct = sum(r["correct"] for r in rows)
            cells[f"{version}:{arm}"] = {
                "version": version, "arm": arm, "n": len(rows), "n_correct": n_correct,
                "threshold": THRESHOLD, "leaked": n_correct > THRESHOLD,
                "verdict": "LEAKS -- TIGHTEN" if n_correct > THRESHOLD else "PASS",
                "n_items_sharing_any_token": sum(1 for r in rows if r["tokens_shared_with_index"]),
                "max_coverage": max((r["coverage"] or 0.0) for r in rows),
                "max_shared_tokens": max(len(r["tokens_shared_with_index"]) for r in rows),
                "rows": rows,
            }

    reg = cells["PRESENT:v3"]
    W = 96
    print("=" * W)
    print("R82 v3 INDEX-LEAKAGE SCREEN, deterministic half (no model call), R96 2026-09-12")
    print(f"  scorer: exp4_witnesses.supports_correct(index_text, entry_text); leak iff >{THRESHOLD}/{N} correct")
    print(f"  registered cell: PRESENT x v3, sample = seed-{SEED} draw of the {N} PRESENT items (the whole pool)")
    print("=" * W)
    print(f"{'version':<9}{'arm':<5}{'n':>4}{'correct':>9}{'any-token':>11}{'max-cov':>9}{'max-shared':>12}  verdict")
    for k, c in cells.items():
        print(f"{c['version']:<9}{c['arm']:<5}{c['n']:>4}{c['n_correct']:>9}{c['n_items_sharing_any_token']:>11}"
              f"{c['max_coverage']:>9.3f}{c['max_shared_tokens']:>12}  {c['verdict']}")
    print("-" * W)
    top = sorted(reg["rows"], key=lambda r: (-(r["coverage"] or 0), r["item_id"]))[:5]
    print("PRESENT x v3, the five items with the highest gold coverage in the index text:")
    for r in top:
        print(f"  cov {r['coverage']:.3f}  shared={r['tokens_shared_with_index']}  {r['item_id']}")
        for d in r["shared_lines"][:2]:
            print(f"      L{d['line_no']:<3d} {d['gold_tokens_on_line']} | {d['line'][:110]}")
    print("-" * W)
    print(f"REGISTERED CELL PRESENT x v3: {reg['n_correct']}/{N} correct -> {reg['verdict']}")

    out = {
        "program": "R96 (2026-09-12), retroactive; ADDENDUM_R82 section 5, key AUX-R82-CF-LEAKSCREEN",
        "model_mediated_screen_ran": False,
        "what_ran": "the deterministic half only: the registered scorer applied to the index text "
                    "against the pair's entry_text; no model call (D-R82-6)",
        "registered_form": "ladder_e1.py: 30 PRESENT items, seed 42, threshold 3, gpt-4.1-mini answers "
                           "from the index alone under the frozen LEAKAGE prompt, scored by supports_correct",
        "scoring": "exp4_witnesses.supports_correct(index_text, entry_text): >=2 shared content tokens "
                   "AND >=50% coverage of the gold's content tokens",
        "gold": "cf_pairs.json entry_text of the item's pair (the drafted questions carry no correct_answer)",
        "n": N, "threshold": THRESHOLD, "seed": SEED,
        "sampling": f"random.Random({SEED}).sample over the {N} PRESENT items sorted by item_id "
                    f"(the whole PRESENT pool, so the sample is exhaustive); ABSENT and PN screened beside it",
        "sample_item_ids": sample_ids,
        "indexes_path": str(idx_path.relative_to(ROOT)).replace("\\", "/"),
        "indexes_file_sha256": hashlib.sha256(raw).hexdigest(),
        "indexes_meta_sha256": idx_doc["meta"]["sha256"],   # the content hash cf_cell.json and NUMBERS_R82 section 1 cite
        "registered_cell": "PRESENT:v3",
        "registered_cell_n_correct": reg["n_correct"],
        "registered_cell_verdict": reg["verdict"],
        "cells": cells,
    }
    dst = R82 / "results" / "leakscreen_v3.json"
    dst.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {dst.relative_to(ROOT)}")
    return 1 if reg["leaked"] else 0


if __name__ == "__main__":
    sys.exit(main())
