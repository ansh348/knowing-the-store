"""p1_sessions.py -- E3 feasibility probe 1: is the corpus replayable?

READ-ONLY. NO API CALLS. NO WRITES to any store or artifact.

Answers three questions the E3 design cannot be written without:

  (1) Do all 40 personas carry a session/time structure that can be replayed
      step by step -- ordered sessions, dated, with the bank's entries
      attributable to the session that produced them?
  (2) How many lifecycle events (supersession, retraction, expiry,
      contradiction, soft/ambiguous supersession) does each persona's timeline
      carry, and are BOTH SIDES of each event dated by session?
  (3) WHERE in the timeline do the lifecycle events land? A snapshot ladder is
      only informative if the resolving side of an event lands late enough that
      a pre-event snapshot and a post-event snapshot both exist.

Usage:  python e3_metamemory/probes/p1_sessions.py
"""

from __future__ import annotations

import collections
import io
import json
import re
import statistics
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LME = PROJECT_ROOT / "LifeMemEval"
BANKS = LME / "artifacts" / "lifecycle_banks"
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))

# The YAML loader with the one known quoting fix, reused verbatim from E0.
from e0_common import load_yaml  # noqa: E402

OUT = Path(__file__).resolve().parent / "p1_sessions.json"

# section -> (old-side session field, new/resolving-side session field)
# None on the old side = the section has one side only (a fact, not a change).
EVENT_SECTIONS = {
    "supersession_events": ("old_session", "new_session"),
    "retractions":         ("original_session", "retraction_session"),
    "contradictions":      ("old_session", "new_session"),
    "ambiguous":           ("existing_session", "new_session"),
    "expiring_logistics":  (None, "session"),
    "stable_identity":     (None, "session"),
}


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def as_int(v):
    """Session fields are ints in most files and strings like 'session 22' in a few."""
    if v is None:
        return None
    if isinstance(v, int):
        return v
    m = re.search(r"\d+", str(v))
    return int(m.group()) if m else None


def main():
    ydirs = {p.name.replace(".yaml", "").split("_")[-1]: p.parent
             for p in sorted(LME.glob("*/persona_*.yaml"))}
    ypaths = {p.name.replace(".yaml", "").split("_")[-1]: p
              for p in sorted(LME.glob("*/persona_*.yaml"))}

    rows = {}
    for name in sorted(ypaths):
        sess_dir = ydirs[name] / "sessions"
        files = sorted(sess_dir.glob("session_*.json"))
        sessions = []
        for f in files:
            d = jload(f)
            sessions.append({"id": d.get("session_id"), "date": str(d.get("date") or ""),
                             "type": d.get("type"), "turns": len(d.get("turns") or []),
                             "facts": len(d.get("facts_disclosed") or [])})
        sessions.sort(key=lambda s: (s["id"] or 0))
        ids = [s["id"] for s in sessions]
        dates = [s["date"] for s in sessions]

        y = load_yaml(ypaths[name])
        events = collections.defaultdict(list)
        for sec, (of, nf) in EVENT_SECTIONS.items():
            for rec in (y.get(sec) or []):
                if not isinstance(rec, dict):
                    continue
                events[sec].append({
                    "old_session": as_int(rec.get(of)) if of else None,
                    "new_session": as_int(rec.get(nf)),
                    "event_date": str(rec.get("event_date") or "") or None,
                    "status": str(rec.get("status") or "") or None,
                    "category": rec.get("category"),
                    "av": rec.get("attack_vector"),
                })

        bank = jload(BANKS / f"{name}.json")["entries"]
        by_src = collections.Counter(e.get("source_session") for e in bank)
        created = {e["id"]: str(e.get("created_at") or "")[:10] for e in bank}
        # does created_at agree with the session's own date?
        date_of = {s["id"]: s["date"] for s in sessions}
        agree = sum(1 for e in bank
                    if date_of.get(e.get("source_session")) == created[e["id"]])

        rows[name] = {
            "n_session_files": len(files),
            "session_ids": ids,
            "ids_contiguous": ids == list(range(1, len(ids) + 1)),
            "dates_monotone": all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1)),
            "date_first": dates[0] if dates else None,
            "date_last": dates[-1] if dates else None,
            "span_days": None,
            "turns_total": sum(s["turns"] for s in sessions),
            "type_counts": dict(collections.Counter(s["type"] for s in sessions)),
            "bank_entries": len(bank),
            "bank_src_null": by_src.get(None, 0),
            "bank_src_out_of_range": sum(v for k, v in by_src.items()
                                         if k is not None and (k < 1 or k > len(ids))),
            "writes_per_session": {int(k): v for k, v in sorted(by_src.items())
                                   if k is not None},
            "created_at_matches_session_date": agree,
            "events": {k: v for k, v in events.items()},
        }
        import datetime as dt
        try:
            rows[name]["span_days"] = (dt.date.fromisoformat(dates[-1])
                                       - dt.date.fromisoformat(dates[0])).days
        except Exception:
            pass

    # -------------------------------------------------------------- reporting
    print("=" * 100)
    print("p1 -- SESSION / TIME STRUCTURE, 40 personas")
    print("=" * 100)
    nsess = [r["n_session_files"] for r in rows.values()]
    print(f"  personas                       : {len(rows)}")
    print(f"  session files per persona      : min {min(nsess)}  max {max(nsess)}  "
          f"all-equal {len(set(nsess)) == 1}")
    print(f"  session ids contiguous 1..N    : {sum(r['ids_contiguous'] for r in rows.values())}/40")
    print(f"  session dates non-decreasing   : {sum(r['dates_monotone'] for r in rows.values())}/40")
    spans = [r["span_days"] for r in rows.values() if r["span_days"]]
    print(f"  calendar span (days)           : min {min(spans)}  median "
          f"{int(statistics.median(spans))}  max {max(spans)}")
    turns = [r["turns_total"] for r in rows.values()]
    print(f"  turns per persona              : min {min(turns)}  median "
          f"{int(statistics.median(turns))}  max {max(turns)}")
    ents = [r["bank_entries"] for r in rows.values()]
    print(f"  bank entries per persona       : min {min(ents)}  median "
          f"{int(statistics.median(ents))}  max {max(ents)}  total {sum(ents)}")
    print(f"  entries with NO source_session : "
          f"{sum(r['bank_src_null'] for r in rows.values())}")
    print(f"  source_session out of 1..N     : "
          f"{sum(r['bank_src_out_of_range'] for r in rows.values())}")
    agree = sum(r["created_at_matches_session_date"] for r in rows.values())
    print(f"  created_at == session date     : {agree}/{sum(ents)} "
          f"({agree / sum(ents):.1%})")

    print("\n  writes per session (pooled over 40 personas, by session index):")
    pooled = collections.Counter()
    for r in rows.values():
        for k, v in r["writes_per_session"].items():
            pooled[k] += v
    line = "    "
    for k in sorted(pooled):
        line += f"{k}:{pooled[k]}  "
        if k % 7 == 0:
            print(line); line = "    "
    if line.strip():
        print(line)

    # --------------------------------------------------------- event structure
    print("\n" + "=" * 100)
    print("p1 -- LIFECYCLE EVENTS PER TIMELINE")
    print("=" * 100)
    tot = collections.Counter()
    dated_both = collections.Counter()
    dated_new = collections.Counter()
    per_persona = collections.defaultdict(collections.Counter)
    for name, r in rows.items():
        for sec, evs in r["events"].items():
            tot[sec] += len(evs)
            per_persona[name][sec] = len(evs)
            for e in evs:
                if e["new_session"] is not None:
                    dated_new[sec] += 1
                if e["new_session"] is not None and (
                        e["old_session"] is not None or EVENT_SECTIONS[sec][0] is None):
                    dated_both[sec] += 1
    print(f"  {'section':22s} {'total':>7s} {'resolving side dated':>21s} "
          f"{'both sides dated':>18s}  per persona (min/med/max)")
    for sec in EVENT_SECTIONS:
        counts = [per_persona[n][sec] for n in rows]
        print(f"  {sec:22s} {tot[sec]:7d} {dated_new[sec]:21d} {dated_both[sec]:18d}"
              f"  {min(counts)}/{int(statistics.median(counts))}/{max(counts)}")
    change = ("supersession_events", "retractions", "contradictions", "ambiguous")
    n_change = sum(tot[s] for s in change)
    per_p = [sum(per_persona[n][s] for s in change) for n in rows]
    print(f"\n  CHANGE EVENTS (the four two-sided sections): {n_change} total, "
          f"per persona min {min(per_p)} / median {int(statistics.median(per_p))} / max {max(per_p)}")

    # ------------------------------------------------------------- clustering
    print("\n" + "=" * 100)
    print("p1 -- WHERE THE EVENTS LAND IN THE TIMELINE")
    print("=" * 100)
    print("  Resolving-side session (new_session / retraction_session), pooled.")
    hist = collections.Counter()
    old_hist = collections.Counter()
    gaps = []
    for name, r in rows.items():
        N = r["n_session_files"]
        for sec in change:
            for e in r["events"][sec]:
                ns, os_ = e["new_session"], e["old_session"]
                if ns:
                    hist[min(int((ns - 1) / N * 5), 4)] += 1
                if os_:
                    old_hist[min(int((os_ - 1) / N * 5), 4)] += 1
                if ns and os_:
                    gaps.append(ns - os_)
    band = ["1st fifth", "2nd fifth", "3rd fifth", "4th fifth", "5th fifth"]
    print(f"    {'band':12s} {'OLD side':>10s} {'RESOLVING side':>16s}")
    for i, b in enumerate(band):
        print(f"    {b:12s} {old_hist[i]:10d} {hist[i]:16d}")
    if gaps:
        print(f"\n  session gap old -> resolving: min {min(gaps)}  median "
              f"{int(statistics.median(gaps))}  mean {statistics.mean(gaps):.1f}  max {max(gaps)}")
        print(f"  events resolving at session >= 6 (a pre-event snapshot exists at s=5): "
              f"{sum(1 for n, r in rows.items() for sec in change for e in r['events'][sec] if (e['new_session'] or 0) >= 6)}"
              f" / {n_change}")

    # expiries
    exp = [e for r in rows.values() for e in r["events"]["expiring_logistics"]]
    print(f"\n  expiring_logistics: {len(exp)} records; "
          f"{sum(1 for e in exp if e['event_date'])} carry an event_date; "
          f"status counts {dict(collections.Counter(e['status'] for e in exp))}")

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print(f"\n  written: {OUT}")


if __name__ == "__main__":
    main()
