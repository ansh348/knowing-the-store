"""
build_annotations.py -- the S3 lifecycle annotation and its S3' scramble. NO API CALLS.

Executes PREREG_E3.md sections 4.3-4.4. Written once, committed, and read by the
answer runner; the scramble is never recomputed at run time.

ANNOTATION (D49-E3), per retrieved fact, from the BELIEVED store state at the rung:
    [expired]     event_time < t_now(rung) - 14d
    [superseded]  exists e' with source_session(e') <= rung and e'.supersedes == e.id
    [active]      otherwise
`[retracted]` is deliberately absent from the vocabulary: the store's is_retracted
flag carries no date, so a rung-correct believed retraction is not derivable from
store-own fields. 31 of 18,936 entries carry it; they fall through to the rules
above. Taking the date from the persona YAML would put TRUE provenance into a
BELIEVED arm and is barred.

SCRAMBLE, marginal-preserving and frozen:
  1. per (persona, rung), collect every retrieved fact occurrence's annotation in
     ascending (cell_id, fact_position);
  2. seed default_rng(int(sha256("E3-LOBOTOMY|persona|rung")[:16], 16));
  3. permute the annotation vector and reassign it to the same positions.
The multiset within each (persona, rung) is exactly preserved, so S3' prompts are
statistically identical to S3 prompts in annotation composition; only the
fact-to-annotation association is destroyed.

Usage:  python e3_metamemory/tools/build_annotations.py
"""

from __future__ import annotations

import collections
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e3_common import (E3, RUNGS, Snapshot, jdump, jload,          # noqa: E402
                       load_cells, scramble_map, session_dates, sha)


def main():
    cells = {c["cell_id"]: c for c in load_cells()["cells"]}
    fr = jload(E3 / "retrieval_frozen_e3.json")
    print(f"retrieval artifact {fr['artifact_sha256'][:16]}...  {fr['n_cells']} cells")
    rows = {r["cell_id"]: r for r in fr["rows"]}
    dates = session_dates()
    personas = sorted({c["persona"] for c in cells.values()})
    snaps = {p: Snapshot(p, dates[p]) for p in personas}

    # ---- true annotations
    true_ann = {}
    for cid, r in rows.items():
        S = snaps[r["persona"]]
        true_ann[cid] = [S.annotate(e, r["rung"]) for e in r["entry_ids"]]

    # ---- the scramble, per (persona, rung)
    scram = {cid: list(v) for cid, v in true_ann.items()}
    dest, degenerate = {}, []
    for p in personas:
        for rung in RUNGS:
            pairs = [(cid, i, a)
                     for cid, r in rows.items() if r["persona"] == p and r["rung"] == rung
                     for i, a in enumerate(true_ann[cid])]
            m, rate = scramble_map(pairs, p, rung)
            for (cid, i), a in m.items():
                scram[cid][i] = a
            dest[f"{p}|{rung}"] = round(rate, 4)
            if len({a for _c, _i, a in pairs}) < 2 and pairs:
                degenerate.append(f"{p}|{rung}")

    vocab = collections.Counter(a for v in true_ann.values() for a in v)
    rates = [v for v in dest.values()]
    jdump({"prereg": "PREREG_E3.md sections 4.3-4.4",
           "retrieval_artifact_sha256": fr["artifact_sha256"],
           "vocabulary": sorted(vocab),
           "annotation_counts": dict(vocab),
           "n_cells": len(true_ann),
           "destruction_rate_by_persona_rung": dest,
           "destruction_rate": {"mean": round(statistics.mean(rates), 4),
                                "median": round(statistics.median(rates), 4),
                                "min": min(rates), "max": max(rates)},
           "degenerate_persona_rungs": degenerate,
           "artifact_sha256": sha(*[f"{c}:{'|'.join(true_ann[c])}:{'|'.join(scram[c])}"
                                    for c in sorted(true_ann)]),
           "true": true_ann, "scrambled": scram},
          E3 / "annotations_e3.json")

    print("=" * 92)
    print("S3 ANNOTATION AND S3' SCRAMBLE")
    print("=" * 92)
    print(f"  fact occurrences annotated: {sum(len(v) for v in true_ann.values())}")
    print(f"  vocabulary: {dict(vocab)}")
    for rung in RUNGS:
        cc = collections.Counter(a for cid, v in true_ann.items()
                                 for a in v if rows[cid]["rung"] == rung)
        tot = sum(cc.values())
        print(f"  rung {rung:>2d}: " + "  ".join(
            f"{k} {v} ({v/tot:.1%})" for k, v in sorted(cc.items())))
    print(f"\n  scramble destruction rate: mean {statistics.mean(rates):.3f}  "
          f"median {statistics.median(rates):.3f}  min {min(rates):.3f}  "
          f"max {max(rates):.3f}")
    print(f"  degenerate (persona, rung) cells -- annotation vector constant: "
          f"{len(degenerate)}")
    print("\nwrote annotations_e3.json")


if __name__ == "__main__":
    main()
