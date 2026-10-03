"""
believed_frbank.py -- E1 Phase 0 item 3, FR-Bank half: believed-state sanity.

NO API CALLS. Read-only over committed artifacts.

Two questions:

  (a) The supersession-leak rate on the E1 persona set. E1 uses all 40 personas,
      which is the same population E0 measured (78/109 = 72% at coverage >= 0.50),
      so this is a re-derivation on the same set rather than a new sample. Reported
      with the threshold bands so the number is not read as a point estimate.

  (b) The believed-vs-true divergence that defines the FR-Bank BELIEVED index.
      TRUE superseded  = an entry the YAML says asserts a superseded value
                         (detector fire against the YAML old value).
      BELIEVED superseded = an entry the BANK ITSELF marks stale, i.e.
                         is_active == False (E0 established this coincides exactly
                         with being the target of a `supersedes` pointer).
      The gap between these two sets is what a believed-state index gets wrong,
      and it is the FR-Bank arm of the H-BELIEVED hypothesis.

Usage:  python e1_metamemory/tools/believed_frbank.py
"""

from __future__ import annotations

import collections
import json
import io
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))

from e0_common import (  # noqa: E402
    CROSS_GUARD, MIN_DISCR, MIN_SHARED, TAU_GOLD, cov, load_joins, toks,
)

BANDS = (0.50, 0.75, 1.00)


def main():
    joins = load_joins()
    print(f"personas loaded: {len(joins)}")

    # ---------------- (a) supersession-leak rate, with bands
    events, best = 0, []
    per_persona = collections.Counter()
    for name, J in sorted(joins.items()):
        for rec in (J.y.get("supersession_events") or []):
            if not isinstance(rec, dict):
                continue
            ot, nt = toks(rec.get("old_fact"), J.drop), toks(rec.get("new_fact"), J.drop)
            do, dn = ot - nt, nt - ot
            if len(do) < MIN_DISCR or len(dn) < MIN_DISCR:
                continue
            events += 1
            b = 0.0
            for i, t in J.etoks.items():
                if len(do & t) >= MIN_SHARED and cov(dn, t) < CROSS_GUARD and J.by_id[i]["is_active"]:
                    b = max(b, cov(do, t))
            best.append(b)
            if b >= 0.50:
                per_persona[name] += 1

    print("\n" + "=" * 84)
    print("(a) SUPERSESSION LEAK — YAML-declared supersessions the bank did not apply")
    print("=" * 84)
    print(f"  resolvable supersession events (discriminator well-defined): {events}")
    for t in BANDS:
        n = sum(1 for b in best if b >= t)
        print(f"    >=1 STILL-ACTIVE entry asserting the old value at coverage >={t:.2f}: "
              f"{n}/{events} = {n/events:.0%}")
    print(f"  personas affected at >=0.50: {len(per_persona)}/40; "
          f"max per persona {max(per_persona.values())}")
    print("  NOTE: same 40-persona population as E0, so this re-derives the E0 figure rather")
    print("        than sampling a new set. The 0.50 band is an upper bound (E0's hand audit")
    print("        put precision at 0.647 there); the 1.00 band is unambiguous.")

    # ---------------- (b) believed vs true superseded sets
    print("\n" + "=" * 84)
    print("(b) BELIEVED vs TRUE superseded sets — the FR-Bank believed-index divergence")
    print("=" * 84)
    tot_true = tot_bel = tot_both = 0
    rows = []
    for name, J in sorted(joins.items()):
        true_sup = set()
        for rec in (J.y.get("supersession_events") or []):
            if not isinstance(rec, dict):
                continue
            d = J.detector(rec.get("old_fact"), rec.get("new_fact"))
            if d:
                true_sup |= {i for i, s in d.items() if s >= 0.80}   # E0 tau_hi
        bel_sup = {e["id"] for e in J.entries if not e["is_active"]}
        both = true_sup & bel_sup
        tot_true += len(true_sup); tot_bel += len(bel_sup); tot_both += len(both)
        rows.append((name, len(true_sup), len(bel_sup), len(both)))

    print(f"{'persona':12s} {'TRUE sup':>9s} {'BELIEVED sup':>13s} {'both':>6s} "
          f"{'recall':>7s} {'precision':>10s}")
    for name, t, b, x in rows[:8]:
        print(f"{name:12s} {t:9d} {b:13d} {x:6d} "
              f"{(x/t if t else 0):7.2f} {(x/b if b else 0):10.3f}")
    print(f"{'...':12s}")
    rec = tot_both / tot_true if tot_true else 0
    pre = tot_both / tot_bel if tot_bel else 0
    print(f"{'TOTAL':12s} {tot_true:9d} {tot_bel:13d} {tot_both:6d} {rec:7.2f} {pre:10.3f}")
    print(f"\n  The bank's own is_active flag RECALLS {rec:.0%} of the entries the YAML says")
    print(f"  assert a superseded value, and only {pre:.1%} of what it marks inactive")
    print("  corresponds to a YAML-declared supersession. Both directions are wrong, and in")
    print("  opposite ways: is_active misses most true staleness AND flags a large volume of")
    print("  entries that no YAML supersession explains (slot-key churn from the extractor).")

    # ---------------- believed index field availability
    e = next(iter(joins.values())).entries[0]
    fields = sorted(e.keys())
    print("\n" + "=" * 84)
    print("(c) FR-Bank BELIEVED index — field availability from the bank's own metadata")
    print("=" * 84)
    spec = [
        ("per-category active count", "YES", "count of is_active == True"),
        ("per-category superseded count", "YES (unreliable)", f"is_active == False; recall {rec:.0%}, precision {pre:.1%} vs YAML"),
        ("per-category retracted count", "YES (near-empty)", "is_retracted; 31 of 18,936 entries corpus-wide"),
        ("per-category expired count", "YES", "event_time < pinned t_now - 14d"),
        ("supersession-event count", "YES (unreliable)", "count of non-null `supersedes` pointers"),
        ("scrubbed superseded slot names", "YES", "slot_key[1] of inactive entries, value-scrubbed"),
        ("recency stats", "YES", "created_at = session date"),
    ]
    for k, avail, src in spec:
        print(f"  {k:32s} {avail:18s} {src}")
    print(f"\n  entry fields present: {', '.join(fields)}")

    out = {
        "leak": {"events": events,
                 "bands": {f"{t:.2f}": sum(1 for b in best if b >= t) for t in BANDS},
                 "personas_affected_at_0.50": len(per_persona),
                 "note": "same 40-persona population as E0; re-derivation, not a new sample"},
        "believed_vs_true": {"true_superseded": tot_true, "believed_superseded": tot_bel,
                             "intersection": tot_both, "recall": rec, "precision": pre,
                             "per_persona": [{"persona": n, "true": t, "believed": b, "both": x}
                                             for n, t, b, x in rows]},
        "believed_index_fields": [{"field": k, "available": a, "source": s} for k, a, s in spec],
        "no_api_calls": True,
    }
    E1.mkdir(parents=True, exist_ok=True)
    with io.open(E1 / "believed_frbank.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"\nwrote {E1/'believed_frbank.json'}")


if __name__ == "__main__":
    main()
