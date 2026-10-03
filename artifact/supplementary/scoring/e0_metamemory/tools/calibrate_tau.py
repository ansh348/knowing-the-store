"""
calibrate_tau.py -- fix the asymmetric detector threshold pair (TAU_LO, TAU_HI).

NO API CALLS. Runs before pre-registration because both constants must appear IN
the pre-registration; it touches ground truth only and produces no elicitation
observation.

TAU_LO (high recall). Any detector signal at or above TAU_LO disqualifies an item
from ABSENT, protecting the gate-critical cell. Rule, declared in advance:

    TAU_LO = the LARGEST value on the grid {0.00,0.10,0.20,0.25,0.34,0.40,0.50}
             at which the set of ABSENT-disqualified items is IDENTICAL to the
             set at the structural floor (0.00, i.e. >=MIN_SHARED tokens only).

That is the plateau point: maximum recall, expressed by the largest threshold
that gives up nothing relative to firing on every structurally valid match.

TAU_HI (high precision). Admits an item to PRESENT-NEGATIVE. Rule, declared in
advance: the smallest threshold on the same grid whose hand-audited precision is
>=95%. The audit is 30 detector fires sampled uniformly at random (seed 42) from
every fire attached to a resolved question across all 40 personas, each read
directly against the YAML record that produced it. No LLM judging: the audit is a
committed table of (entry text, YAML old value, YAML new value, verdict) that can
be checked line by line.

Usage:
    python e0_metamemory/tools/calibrate_tau.py emit      # writes tau_audit_sample.json
    python e0_metamemory/tools/calibrate_tau.py finalize  # reads verdicts, writes thresholds.json
"""

from __future__ import annotations

import collections
import random
import sys

from e0_common import (
    E0, SEED, jdump, jload, load_joins, CATEGORIES, MIN_SHARED,
)

# One uniform grid, spanning the whole signal range, used for BOTH rules.
# The first draft of this file stopped the grid at 0.50, which is where the
# TAU_LO plateau lives but is below the TAU_HI precision cliff -- see DEVIATIONS
# D10. The audit table is published verbatim, so precision at any threshold can
# be recomputed independently of this choice.
GRID = [round(0.05 * i, 2) for i in range(21)]
AUDIT_N = 30
AUDIT_PATH = E0 / "tau_audit_sample.json"
THRESH_PATH = E0 / "thresholds.json"


def all_fires(joins):
    """Every detector fire attached to a resolved question, across all 40 personas."""
    out = []
    for name, J in sorted(joins.items()):
        for q in J.questions:
            qid = q["id"]
            for eid, sig in (J.fires.get(qid) or {}).items():
                sec_ridx = J.rec_of[qid]
                sec, ridx = sec_ridx
                rec = [r for r in (J.y.get(sec) or []) if isinstance(r, dict)][ridx]
                from e0_common import SECTION_FIELDS
                gf, _, sf, _ = SECTION_FIELDS[sec]
                out.append({
                    "persona": name, "question_id": qid, "entry_id": eid,
                    "signal": round(sig, 4), "section": sec,
                    "attack_vector": q["attack_vector"],
                    "entry_text": J.by_id[eid]["text"],
                    "entry_category": J.by_id[eid]["category"],
                    "entry_is_active": bool(J.by_id[eid]["is_active"]),
                    "yaml_superseded_value": str(rec.get(sf)) if sf else None,
                    "yaml_current_value": str(rec.get(gf)),
                })
    out.sort(key=lambda r: (r["persona"], r["question_id"], r["entry_id"]))
    return out


def tau_lo_plateau(joins):
    """Largest grid value whose ABSENT-disqualification set equals the floor's."""
    # An item is (question, variant); disqualification is a property of the fire
    # set surviving the ablation, so evaluate on the FULL variant -- the ABLATED
    # variant can only remove fires, never add them, so the floor set is a superset.
    def disq(tau):
        s = set()
        for name, J in sorted(joins.items()):
            for q in J.questions:
                f = J.fires.get(q["id"]) or {}
                if any(sig >= tau for sig in f.values()):
                    s.add((name, q["id"]))
        return s

    floor = disq(0.0)
    best = 0.0
    for t in GRID:
        if disq(t) == floor:
            best = t
    return best, len(floor)


def cmd_emit():
    joins = load_joins()
    tau_lo, n_floor = tau_lo_plateau(joins)
    fires = all_fires(joins)
    pool = [f for f in fires if f["signal"] >= tau_lo]
    rng = random.Random(SEED)
    sample = sorted(rng.sample(pool, min(AUDIT_N, len(pool))),
                    key=lambda r: (-r["signal"], r["persona"], r["entry_id"]))
    for r in sample:
        r["verdict"] = None      # "TRUE"  = entry really asserts the superseded value
        r["audit_note"] = ""     # "FALSE" = it does not
    jdump({
        "meta": {
            "purpose": "hand audit of 30 detector fires; sets TAU_HI",
            "sampling": f"uniform without replacement, seed {SEED}, from all fires "
                        f"with signal >= tau_lo across all 40 personas",
            "tau_lo": tau_lo,
            "tau_lo_rule": "largest grid value whose ABSENT-disqualification set "
                           "equals the structural floor's",
            "n_fires_total": len(fires),
            "n_fires_at_tau_lo": len(pool),
            "n_items_disqualified_at_floor": n_floor,
            "grid": GRID,
            "audit_instruction": "TRUE iff the entry text asserts the "
                                 "yaml_superseded_value (so its correct influence on an "
                                 "answer would be suppression). FALSE otherwise, "
                                 "including incidental token overlap.",
        },
        "sample": sample,
    }, AUDIT_PATH)
    print(f"tau_lo = {tau_lo:.2f}  (plateau; {n_floor} items disqualified at the floor)")
    print(f"fires total {len(fires)}, at tau_lo {len(pool)}, sampled {len(sample)}")
    print(f"wrote {AUDIT_PATH} -- fill in 'verdict' for each row, then run finalize")
    print("\n  signal distribution of the pool:")
    band = collections.Counter()
    for f in pool:
        band[f"{min(int(f['signal'] * 10) / 10, 0.9):.1f}-"] += 1
    for k in sorted(band):
        print(f"    {k:6s} {band[k]:4d}")


def cmd_finalize():
    a = jload(AUDIT_PATH)
    sample = a["sample"]
    missing = [r["entry_id"] for r in sample if r.get("verdict") not in ("TRUE", "FALSE")]
    if missing:
        raise SystemExit(f"{len(missing)} rows still unaudited: {missing[:5]} ...")
    tau_lo = float(a["meta"]["tau_lo"])

    rows = []
    tau_hi = None
    for t in GRID:
        at = [r for r in sample if r["signal"] >= t]
        n = len(at)
        tp = sum(1 for r in at if r["verdict"] == "TRUE")
        prec = (tp / n) if n else None
        rows.append({"threshold": t, "n_audited_at_or_above": n,
                     "n_true": tp, "precision": (round(prec, 4) if prec is not None else None)})
        if tau_hi is None and n > 0 and prec >= 0.95:
            tau_hi = t
    if tau_hi is None:
        tau_hi = 1.00
        note = ("no grid threshold reached 95% precision on the audit; "
                "TAU_HI falls back to 1.00 (every discriminative token present)")
    else:
        note = f"smallest grid threshold with audited precision >= 95% is {tau_hi:.2f}"

    print(f"{'thr':>5s} {'n>=thr':>7s} {'true':>5s} {'precision':>10s}")
    for r in rows:
        p = "-" if r["precision"] is None else f"{r['precision']:.3f}"
        print(f"{r['threshold']:5.2f} {r['n_audited_at_or_above']:7d} {r['n_true']:5d} {p:>10s}")
    print(f"\nTAU_LO = {tau_lo:.2f}   TAU_HI = {tau_hi:.2f}\n{note}")

    jdump({
        "tau_gold": 0.50,
        "tau_lo": tau_lo,
        "tau_hi": tau_hi,
        "min_shared_tokens": MIN_SHARED,
        "grid": GRID,
        "tau_lo_rule": a["meta"]["tau_lo_rule"],
        "tau_hi_rule": "smallest grid threshold with hand-audited precision >= 0.95",
        "tau_hi_note": note,
        "audit": {"n": len(sample), "seed": SEED, "table": rows,
                  "source": "e0_metamemory/tau_audit_sample.json"},
        "no_api_calls": True,
    }, THRESH_PATH)
    print(f"wrote {THRESH_PATH}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "emit"
    {"emit": cmd_emit, "finalize": cmd_finalize}[cmd]()
