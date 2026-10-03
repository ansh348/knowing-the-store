"""
membership.py -- B4 membership spot-check under the (question, YAML-record) factorization.

NO API CALLS.

The factorization splits PN verification into two steps:

  SEMANTIC  "does YAML record R constitute a negative obligation for question Q,
            under Q's intent type?"  -- backend-INDEPENDENT, read once per
            (question, record) pair by a human.
  MEMBERSHIP "does backend B's store contain an entry asserting R's superseded
            value?" -- mechanical, decided by the detector.

Only the second step is per-backend, and only it is being spot-checked here. This
tool samples ~40 (entry, record) membership decisions stratified across the three
backends, emits them for direct reading, and measures precision per backend.

Pre-registered consequence: **membership precision < 90% on any backend escalates
that backend to full (question, entry) verification.**

Ordering note: this runs before PREREG_E1.md exists because its outcome -- which
backends escalate -- is a parameter the pre-registration must state. Same
structure as E0's tau calibration, which also necessarily preceded its prereg.

Usage:
    python e1_metamemory/tools/membership.py emit
    python e1_metamemory/tools/membership.py apply
"""

from __future__ import annotations

import collections
import io
import json
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e0_common import (  # noqa: E402
    CROSS_GUARD, MIN_DISCR, MIN_SHARED, cov, load_joins, toks,
)
from backends import BACKENDS, load_backend  # noqa: E402

SEED = 42
TAU_HI = 0.80            # E0's admission threshold, carried
N_SAMPLE = 40
WORKSHEET = E1 / "membership_worksheet.md"
OUT = E1 / "membership_spotcheck.json"

# B3: Mem0 personas below 20/35 sessions are excluded from the study entirely.
MEM0_EXCLUDE = {"alex", "thanh", "aisha"}


def records_for(J):
    """(kind, superseded_value, current_value) triples from the persona YAML."""
    out = []
    for r in (J.y.get("supersession_events") or []):
        if isinstance(r, dict) and r.get("old_fact") and r.get("new_fact"):
            out.append(("supersession", r["old_fact"], r["new_fact"]))
    for r in (J.y.get("retractions") or []):
        if isinstance(r, dict) and r.get("original_fact") and r.get("retraction"):
            out.append(("retraction", r["original_fact"], r["retraction"]))
    return out


def fires(old, new, entries, drop):
    """Detector over an arbitrary backend's entries. Same rule as E0."""
    ot, nt = toks(old, drop), toks(new, drop)
    do, dn = ot - nt, nt - ot
    if len(do) < MIN_DISCR or len(dn) < MIN_DISCR:
        return []
    hits = []
    for e in entries:
        t = toks(e["text"], drop)
        if len(do & t) >= MIN_SHARED and cov(dn, t) < CROSS_GUARD:
            s = cov(do, t)
            if s >= TAU_HI:
                hits.append((e, round(s, 4)))
    return hits


def build_pool():
    joins = load_joins()
    per_backend = {b: collections.defaultdict(list) for b in BACKENDS}
    for b in BACKENDS:
        for r in load_backend(b):
            per_backend[b][r["persona"]].append(r)
    pool = []
    for name, J in sorted(joins.items()):
        recs = records_for(J)
        if not recs:
            continue
        for b in BACKENDS:
            if b == "mem0" and name in MEM0_EXCLUDE:
                continue
            entries = per_backend[b].get(name, [])
            if not entries:
                continue
            for kind, old, new in recs:
                for e, s in fires(old, new, entries, J.drop):
                    pool.append({"backend": b, "persona": name, "kind": kind,
                                 "entry_id": e["entry_id"], "signal": s,
                                 "entry_text": e["text"],
                                 "yaml_superseded": old, "yaml_current": new})
    return pool


def cmd_emit():
    pool = build_pool()
    byb = collections.Counter(p["backend"] for p in pool)
    print("membership-decision pool (detector fires at tau_hi >= 0.80):")
    for b in BACKENDS:
        print(f"  {b:8s} {byb[b]:5d}")
    rng = random.Random(SEED)
    quota = {"frbank": 14, "mem0": 13, "amem": 13}
    sample = []
    for b in BACKENDS:
        cand = sorted([p for p in pool if p["backend"] == b],
                      key=lambda p: (p["persona"], p["entry_id"]))
        sample += rng.sample(cand, min(quota[b], len(cand)))
    for r in sample:
        r["verdict"] = None
        r["note"] = ""

    L = ["# MEMBERSHIP SPOT-CHECK — B4 (question, YAML-record) factorization", "",
         f"{len(sample)} sampled membership decisions, seed {SEED}, stratified across backends. "
         f"Pool: " + ", ".join(f"{b} {byb[b]}" for b in BACKENDS) + ".", "",
         "**The decision under test is MEMBERSHIP only**: does this entry, in this backend's "
         "store, assert the value the YAML marks as superseded? It is NOT the semantic question "
         "of whether that constitutes a negative obligation for any particular question — that "
         "is verified once per (question, record) and is backend-independent.", "",
         "TRUE = the entry asserts the superseded value. FALSE = it does not.", "",
         "**Escalation rule: precision < 90% on any backend sends that backend to full "
         "(question, entry) verification.**", ""]
    for b in BACKENDS:
        rows = [r for r in sample if r["backend"] == b]
        L += [f"\n## {b} — {len(rows)} decisions\n",
              "| # | persona | entry | sig | entry text | YAML superseded value | verdict |",
              "|---|---|---|---|---|---|---|"]
        for n, r in enumerate(rows, 1):
            et = r["entry_text"].replace("|", "\\|")[:150]
            ys = r["yaml_superseded"].replace("|", "\\|")[:90]
            L.append(f"| {n} | {r['persona']} | `{r['entry_id'][:12]}` | {r['signal']:.2f} | "
                     f"{et} | {ys} |  |")
    with io.open(WORKSHEET, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    with io.open(E1 / "membership_sample.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump({"pool_size_by_backend": dict(byb), "seed": SEED,
                   "tau_hi": TAU_HI, "sample": sample}, f,
                  ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(f"\nwrote {WORKSHEET} ({len(sample)} decisions) and membership_sample.json")


def cmd_apply():
    from membership_verdicts import VERDICTS  # noqa: PLC0415
    d = json.load(io.open(E1 / "membership_sample.json", encoding="utf-8"))
    sample = d["sample"]
    key = lambda r: (r["backend"], r["persona"], r["entry_id"][:12])
    miss = [key(r) for r in sample if key(r) not in VERDICTS]
    if miss:
        raise SystemExit(f"{len(miss)} unverified: {miss[:3]}")
    stats = collections.defaultdict(lambda: [0, 0])
    for r in sample:
        v, note = VERDICTS[key(r)]
        r["verdict"], r["note"] = v, note
        stats[r["backend"]][0] += 1
        stats[r["backend"]][1] += (v == "TRUE")
    print(f"{'backend':10s} {'n':>4s} {'true':>5s} {'precision':>10s}  escalation")
    esc = []
    for b in BACKENDS:
        n, t = stats[b]
        p = t / n if n else 0.0
        if p < 0.90:
            esc.append(b)
        print(f"{b:10s} {n:4d} {t:5d} {p:10.1%}  "
              f"{'ESCALATE to full (question,entry) verification' if p < 0.90 else 'ok'}")
    d["results"] = {b: {"n": stats[b][0], "true": stats[b][1],
                        "precision": (stats[b][1] / stats[b][0]) if stats[b][0] else None}
                    for b in BACKENDS}
    d["escalated_backends"] = esc
    d["rule"] = "precision < 0.90 escalates that backend to full (question, entry) verification"
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(f"\nescalated: {esc or 'none'}\nwrote {OUT}")


if __name__ == "__main__":
    {"emit": cmd_emit, "apply": cmd_apply}[sys.argv[1] if len(sys.argv) > 1 else "emit"]()
