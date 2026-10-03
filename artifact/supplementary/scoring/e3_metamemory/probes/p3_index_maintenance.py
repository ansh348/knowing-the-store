"""p3_index_maintenance.py -- E3 feasibility probe 3: what does the index cost to keep?

READ-ONLY with respect to every store, index and E1/E2 artifact. NO API CALLS.
Replays ONE persona's writes in memory and times the index update. Nothing is
written except this probe's own JSON report.

The question the ledger left open is "what does the counting index cost to
MAINTAIN, per write, in a running agent". E2 charged it at 1.3 ms/store from a
single rebuild timing and called it negligible. That figure is a REBUILD, and a
rebuild is not a maintenance cost -- it is the cost of not having one.

This probe separates three quantities that E2's single number conflated:

  REBUILD    index_v2.render over the whole surviving store. What E1/E2 do.
  MAINTAIN   the incremental state update a single write forces.
  SERVE      rendering the index text once, when a gate call needs it.

and reports the one structural finding that decides whether MAINTAIN is O(1):
the recency block is computed against a MOVING t_now, so it is not a function of
the writes alone.

Usage:  python e3_metamemory/probes/p3_index_maintenance.py [persona]
"""

from __future__ import annotations

import bisect
import collections
import datetime as dt
import io
import json
import statistics
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LME = PROJECT_ROOT / "LifeMemEval"
BANKS = LME / "artifacts" / "lifecycle_banks"
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(PROJECT_ROOT / "e1_metamemory" / "tools"))

from e0_common import EXPIRY_WINDOW, parse_dt  # noqa: E402
from index_v2 import AGE_BANDS, AVAIL, SLOT_CAP, render, scrub  # noqa: E402

OUT = Path(__file__).resolve().parent / "p3_index_maintenance.json"
REPEATS = 5          # timing repeats; report the median to damp scheduler noise
DEFAULT = "priya"


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def session_dates(persona):
    for ypath in sorted(LME.glob("*/persona_*.yaml")):
        if ypath.name.replace(".yaml", "").split("_")[-1] != persona:
            continue
        out = {}
        for f in sorted((ypath.parent / "sessions").glob("session_*.json")):
            j = jload(f)
            out[int(j["session_id"])] = str(j["date"])
        return out
    raise SystemExit(f"no persona {persona}")


def rows_for(entries, t_now, cutoff):
    """The BELIEVED FR-Bank projection index_v2.view produces, for these entries."""
    out = []
    for e in entries:
        d = parse_dt(e.get("created_at"))
        age = max(0, (t_now - d).days) if d else None
        et = parse_dt(e.get("event_time"))
        out.append({
            "id": e["id"], "category": e["category"], "slot": scrub(
                (e.get("slot_key") or [None, None])[1]
                if isinstance(e.get("slot_key"), list) and len(e["slot_key"]) >= 2
                else None),
            "age": age,
            "superseded": not e["is_active"],
            "retracted": bool(e["is_retracted"]),
            "expired": bool(et is not None and cutoff is not None and et < cutoff),
            "active": bool(e["is_active"] and not e["is_retracted"]),
            "_sup_ptr": bool(e.get("supersedes")),
        })
    return out


class Incremental:
    """The same counting index, maintained rather than rebuilt.

    Every field index_v2 renders is an aggregate over the surviving rows:
      - lifecycle totals            -> five counters
      - per-category breakdown      -> counters keyed (category, field)
      - attribute names by category -> a set per category, plus one for superseded
      - recency + age distribution  -> order statistics over the entry DATES

    The first three are exactly O(1) per write. The fourth is the one that is not,
    and the reason is recorded in the report rather than smoothed over.
    """

    def __init__(self):
        self.n = 0
        self.tot = collections.Counter()
        self.cat = collections.defaultdict(collections.Counter)
        self.names = collections.defaultdict(set)
        self.sup_names = set()
        self.dates = []                       # sorted; the only non-O(1) structure
        self.events = 0

    def add(self, r, created):
        """One write. Returns nothing; times as MAINTAIN."""
        self.n += 1
        for f in ("active", "superseded", "retracted", "expired"):
            if r[f]:
                self.tot[f] += 1
                self.cat[r["category"]][f] += 1
        self.cat[r["category"]]["entries"] += 1
        if r["_sup_ptr"]:
            self.events += 1
        if r["slot"]:
            self.names[r["category"]].add(r["slot"])
            if r["superseded"]:
                self.sup_names.add(r["slot"])
        bisect.insort(self.dates, created)


def main():
    persona = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    entries = jload(BANKS / f"{persona}.json")["entries"]
    dates = session_dates(persona)
    by_sess = collections.defaultdict(list)
    for e in entries:
        by_sess[e.get("source_session")].append(e)
    sessions = sorted(k for k in by_sess if k is not None)

    print("=" * 100)
    print(f"p3 -- INDEX MAINTENANCE, persona `{persona}`: {len(entries)} entries over "
          f"{len(sessions)} sessions")
    print("=" * 100)
    print("  STATED FINDING FIRST: index_v2.py does NOT update incrementally. `render()`")
    print("  iterates every surviving row on every call, and E1/E2 call it once per")
    print("  (persona, variant, provenance). E2's 1.3 ms/store figure is a REBUILD cost.")
    print()

    # ------------------------------------------------------- REBUILD, per session
    rebuild_ms, serve_ms, n_alive, txt_len = [], [], [], []
    alive = []
    for s in sessions:
        alive.extend(by_sess[s])
        t_now = parse_dt(dates[s]) + dt.timedelta(hours=24)
        cutoff = t_now - EXPIRY_WINDOW
        rows = rows_for(alive, t_now, cutoff)
        ev = [{r["id"]} for r in rows if r["_sup_ptr"]]
        ts = []
        for _ in range(REPEATS):
            t0 = time.perf_counter()
            rows2 = rows_for(alive, t_now, cutoff)
            txt, _, _ = render(rows2, ev, AVAIL[("frbank", "BELIEVED")])
            ts.append((time.perf_counter() - t0) * 1000)
        rebuild_ms.append(statistics.median(ts))
        ts = []
        for _ in range(REPEATS):
            t0 = time.perf_counter()
            render(rows, ev, AVAIL[("frbank", "BELIEVED")])
            ts.append((time.perf_counter() - t0) * 1000)
        serve_ms.append(statistics.median(ts))
        n_alive.append(len(alive))
        txt_len.append(len(txt))

    # ------------------------------------------------------ MAINTAIN, per write
    maint_us = []
    for _ in range(REPEATS):
        inc = Incremental()
        acc, alive = [], []
        for s in sessions:
            t_now = parse_dt(dates[s]) + dt.timedelta(hours=24)
            cutoff = t_now - EXPIRY_WINDOW
            rows = rows_for(by_sess[s], t_now, cutoff)
            for r, e in zip(rows, by_sess[s]):
                d = parse_dt(e["created_at"])
                t0 = time.perf_counter()
                inc.add(r, d)
                acc.append((time.perf_counter() - t0) * 1e6)
            alive.extend(by_sess[s])
        maint_us.append(acc)
    per_write_us = [statistics.median(x) for x in zip(*maint_us)]

    # -------------------------------------- the t_now problem, measured not asserted
    t_first = parse_dt(dates[sessions[0]]) + dt.timedelta(hours=24)
    t_last = parse_dt(dates[sessions[-1]]) + dt.timedelta(hours=24)
    rows_first = rows_for(entries, t_first, t_first - EXPIRY_WINDOW)
    rows_last = rows_for(entries, t_last, t_last - EXPIRY_WINDOW)

    def bands(rs):
        ages = [r["age"] for r in rs if r["age"] is not None]
        return {lab: sum(1 for a in ages if lo <= a <= hi) for lo, hi, lab in AGE_BANDS}

    b1, b2 = bands(rows_first), bands(rows_last)
    moved = sum(1 for r1, r2 in zip(rows_first, rows_last)
                if r1["age"] is not None and r2["age"] is not None
                and _band(r1["age"]) != _band(r2["age"]))
    exp_first = sum(1 for r in rows_first if r["expired"])
    exp_last = sum(1 for r in rows_last if r["expired"])

    # ------------------------------------------------------------------- report
    print(f"  {'session':>8s} {'entries':>9s} {'writes':>8s} {'REBUILD ms':>12s} "
          f"{'SERVE ms':>10s} {'index bytes':>12s}")
    for i, s in enumerate(sessions):
        if s in (sessions[0], sessions[len(sessions) // 2], sessions[-1]) or s % 7 == 0:
            print(f"  {s:>8d} {n_alive[i]:>9d} {len(by_sess[s]):>8d} "
                  f"{rebuild_ms[i]:>12.2f} {serve_ms[i]:>10.2f} {txt_len[i]:>12d}")
    print(f"\n  REBUILD  (project rows + render, whole store): "
          f"first {rebuild_ms[0]:.2f} ms  last {rebuild_ms[-1]:.2f} ms  "
          f"median {statistics.median(rebuild_ms):.2f} ms")
    print(f"  SERVE    (render only, rows already projected): "
          f"first {serve_ms[0]:.2f} ms  last {serve_ms[-1]:.2f} ms  "
          f"median {statistics.median(serve_ms):.2f} ms")
    print(f"  MAINTAIN (one incremental write)              : "
          f"median {statistics.median(per_write_us):.2f} us  "
          f"p95 {sorted(per_write_us)[int(0.95 * len(per_write_us))]:.2f} us  "
          f"max {max(per_write_us):.2f} us")
    tot_writes = sum(len(by_sess[s]) for s in sessions)
    print(f"\n  Whole-timeline totals for this persona ({tot_writes} writes, "
          f"{len(sessions)} sessions):")
    print(f"    rebuild-per-write   : {sum(rebuild_ms) / 1000:.3f} s  "
          f"(index rebuilt once per session)")
    print(f"    maintain-per-write  : {sum(per_write_us) / 1e6:.4f} s "
          f"({sum(per_write_us) / tot_writes:.2f} us/write)")
    ratio = (sum(rebuild_ms) * 1000) / max(1e-9, sum(per_write_us))
    print(f"    ratio               : rebuilding once per session costs {ratio:.0f}x "
          f"the incremental maintenance of the same writes")

    print("\n  THE FIELD THAT IS NOT O(1) PER WRITE -- recency, and why:")
    print("    Ages are days before a MOVING t_now, so every entry's age changes when")
    print("    t_now advances, with no write involved. Between this persona's first and")
    print("    last session t_now:")
    print(f"      entries whose AGE BAND changes with no write : {moved} / {len(entries)}")
    print(f"      age-band histogram at first t_now            : {b1}")
    print(f"      age-band histogram at last  t_now            : {b2}")
    print(f"      entries counted EXPIRED (event_time < t_now-14d): "
          f"{exp_first} -> {exp_last}")
    print("    So `recency`, `expired` and the age distribution are functions of the")
    print("    CLOCK as well as of the writes. They are maintainable in O(log n) per write")
    print("    off a sorted date list plus an O(1) clock read at serve time (the structure")
    print("    this probe uses), but NOT by a counter that only sees writes. Any E3")
    print("    maintenance-cost column must charge a per-SERVE clock pass, not a per-write")
    print("    one, for those three fields.")

    payload = {
        "persona": persona, "n_entries": len(entries), "n_sessions": len(sessions),
        "repeats": REPEATS,
        "rebuild_ms": rebuild_ms, "serve_ms": serve_ms,
        "maintain_us_per_write_median": statistics.median(per_write_us),
        "maintain_us_total": sum(per_write_us),
        "rebuild_ms_total": sum(rebuild_ms),
        "n_alive": n_alive, "index_bytes": txt_len,
        "incremental_implemented_in_index_v2": False,
        "age_band_moves_with_clock": moved,
        "expired_first_tnow": exp_first, "expired_last_tnow": exp_last,
    }
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print(f"\n  written: {OUT}")


def _band(age):
    for lo, hi, lab in AGE_BANDS:
        if lo <= age <= hi:
            return lab
    return None


if __name__ == "__main__":
    main()
