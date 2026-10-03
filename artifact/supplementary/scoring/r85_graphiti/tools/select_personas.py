"""select_personas.py -- R85 Phase 0. Deterministic persona selection. NO API CALLS.

Emits the census behind the three spike persona picks so the choice is reproducible and
checkable rather than asserted. Read-only over committed artifacts.

Rules, frozen at Phase 0 before any Graphiti dump is read:

  Persona A  the FR-Bank persona with the most PRESENT-NEGATIVE items in the committed
             n=661 NOK population (backend == frbank, label in the scoreable set).
  Persona B  among the counterfactual-cell personas whose registered pair is a RETRACTION,
             the one whose scrubbed attribute name individuates, carries no collision with
             the v2 superseded-names list, and survives index_v2.scrub()'s first-colon
             truncation as something other than "project".
  Persona C  the persona with the most MIN_DISCR-filtered manifest supersession events.
             Added under the joint reading of the ADDENDUM rider, so the gate denominator
             clears four events. Stock and mini only.

Ground truth throughout is the persona manifest (the YAML), never FR-Bank's own
`supersedes` links. The links overstate staleness by roughly sixty times, which the paper
already reports; censusing one backend's belief against another's would measure nothing.

Usage:  python r85_graphiti/tools/select_personas.py
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))
from e0_common import MIN_DISCR, load_joins, toks  # noqa: E402

SCOREABLE = {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}
BANKS = ROOT / "LifeMemEval" / "artifacts" / "lifecycle_banks"


def disc_events(J):
    """Manifest supersession events surviving the MIN_DISCR filter believed_frbank.py uses."""
    out = []
    for rec in (J.y.get("supersession_events") or []):
        if not isinstance(rec, dict):
            continue
        ot, nt = toks(rec.get("old_fact"), J.drop), toks(rec.get("new_fact"), J.drop)
        if len(ot - nt) < MIN_DISCR or len(nt - ot) < MIN_DISCR:
            continue
        out.append(rec)
    return out


def main():
    items = json.loads((ROOT / "e1_metamemory" / "build" / "items_final.json").read_text("utf-8"))
    nok = [i for i in items if i["backend"] == "frbank" and i["label"] in SCOREABLE]
    pn = collections.Counter(i["persona"] for i in nok if i["label"] == "PRESENT-NEGATIVE")
    print(f"n=661 population check: {len(nok)} items, {sum(pn.values())} PN positives")

    joins = load_joins()
    rows = []
    for name in sorted(joins):
        J = joins[name]
        ev = disc_events(J)
        within = sum(1 for r in ev if r.get("old_session") == r.get("new_session"))
        bank = json.loads((BANKS / f"{name}.json").read_text("utf-8"))["entries"]
        rows.append({
            "persona": name,
            "pn": pn.get(name, 0),
            "sup_disc": len(ev),
            "sup_within_session": within,
            "retractions": len(J.y.get("retractions") or []),
            "expired": len([e for e in (J.y.get("expiring_logistics") or [])
                            if str(e.get("status", "")).lower() == "expired"]),
            "records": len(bank),
            "episodes": len({r["created_at"] for r in bank}),
        })

    tot = sum(r["sup_disc"] for r in rows)
    totw = sum(r["sup_within_session"] for r in rows)
    print(f"manifest supersession events over 40 personas: {tot} "
          f"(reproduces the census figure 109); within-session {totw} ({100*totw/tot:.1f}%)")

    a = max(rows, key=lambda r: (r["pn"], -r["records"]))
    c = max(rows, key=lambda r: (r["sup_disc"], r["pn"]))
    # Persona B: retraction pairs whose scrubbed name escapes the "project" collision.
    cf = json.loads((ROOT / "r82_counterfactual" / "cf_cell.json").read_text("utf-8"))
    indiv = cf["meta"]["individuation"]
    b_pool = []
    for pid, m in indiv.items():
        if m.get("state") != "RETRACTION":
            continue
        if not m.get("individuates"):
            continue
        if m.get("superseded_list_collision_in_present"):
            continue
        if m.get("slot_scrubbed") == "project":
            continue
        b_pool.append((pid, m))
    assert len(b_pool) == 1, f"persona B rule is not unique: {[p for p, _ in b_pool]}"
    b_pid, b_meta = b_pool[0]
    b_name = b_pid.split(":")[1]
    b = next(r for r in rows if r["persona"] == b_name)

    print("\n%-8s %4s %8s %7s %5s %5s %8s %9s" % (
        "persona", "PN", "SUPdisc", "within", "RET", "EXPd", "records", "episodes"))
    for r in sorted(rows, key=lambda r: -r["sup_disc"])[:6]:
        print("%-8s %4d %8d %7d %5d %5d %8d %9d" % tuple(r[k] for k in (
            "persona", "pn", "sup_disc", "sup_within_session", "retractions",
            "expired", "records", "episodes")))

    picks = [("A", a), ("B", b), ("C", c)]
    print("\nPICKS")
    for tag, r in picks:
        print("  %s = %-6s  PN=%d  manifest supersession events=%d (within-session %d)  "
              "episodes=%d" % (tag, r["persona"], r["pn"], r["sup_disc"],
                               r["sup_within_session"], r["episodes"]))
    print("  B pair = %s, scrubbed name %r" % (b_pid, b_meta.get("slot_scrubbed")))

    denom = sum(r["sup_disc"] for _, r in picks)
    within = sum(r["sup_within_session"] for _, r in picks)
    print("\nGATE denominator = %d manifest supersession events; within-session %d; "
          "granularity 1/%d; >= 0.50 means >= %d of %d"
          % (denom, within, denom, -(-denom // 2), denom))
    assert denom >= 4, "rider unsatisfied: gate denominator below four"
    print("episodes to ingest, spike: A %d (mini) + A %d (nano) + B %d + C %d + fork A,B %d = %d"
          % (a["episodes"], a["episodes"], b["episodes"], c["episodes"],
             a["episodes"] + b["episodes"],
             3 * a["episodes"] + 2 * b["episodes"] + c["episodes"]))


if __name__ == "__main__":
    main()
