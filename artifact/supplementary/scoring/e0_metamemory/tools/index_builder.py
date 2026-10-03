"""
index_builder.py -- E0 Step 2: the metadata index M(S).

NO API CALLS. Deterministic. One renderer for every store variant.

Allowed contents (PREREG_E0.md §8): per-category entry counts (active and inactive
separately), per-category supersession counts, retraction counts, expiry counts,
ingest-time recency statistics (newest and oldest entry age per category), and
slot-key NAMES per category capped at 15, alphabetically.

Forbidden: fact values, entry text, numeric values from facts, event dates drawn
from fact content, anything from which an answer could be read off.

Note on what is deliberately NOT emitted: `event_time` values are never printed,
only COUNTS of entries whose event_time precedes the pinned cutoff. Ages are
computed from `created_at`, which is the session date -- ingest time, not fact
content. Slot-key names are the only free text that reaches the index, which is
why they are the subject of the tightening ladder.

Tightening ladder, pre-registered:
  0  full slot-key names, capped at 15 per category, alphabetical
  1  strip everything after the first ':', keeping the generic attribute type
  2  drop slot-key names entirely; counts and recency only

Usage:  python e0_metamemory/tools/index_builder.py [level]
"""

from __future__ import annotations

import collections
import datetime as dt
import sys
import textwrap

from e0_common import E0, jdump, jload, parse_dt, EXPIRY_WINDOW

STORES = E0 / "stores"
OUT = E0 / "indexes.json"
SLOT_CAP = 15


def slot_name(entry, level):
    sk = entry.get("slot_key")
    if not (isinstance(sk, list) and len(sk) >= 2):
        return None
    name = str(sk[1])
    if level >= 2:
        return None
    if level == 1:
        return name.split(":", 1)[0]
    return name


def render(entries, t_now_iso, level):
    """The one renderer. Same code path for FULL and ABLATED."""
    t_now = parse_dt(t_now_iso)
    cutoff = t_now - EXPIRY_WINDOW
    by_cat = collections.defaultdict(list)
    for e in entries:
        by_cat[e["category"]].append(e)

    n_act = sum(1 for e in entries if e["is_active"])
    L = ["MEMORY STORE INDEX  (metadata only; no fact content)",
         f"entries: {len(entries)}   active: {n_act}   inactive: {len(entries) - n_act}"
         f"   categories: {len(by_cat)}",
         "",
         f"{'CATEGORY':24s} {'ACT':>4s} {'INACT':>6s} {'SUPRSD':>7s} {'RETR':>5s}"
         f" {'EXPIRED':>8s} {'NEWEST':>7s} {'OLDEST':>7s}"]
    for cat in sorted(by_cat):
        es = by_cat[cat]
        act = sum(1 for e in es if e["is_active"])
        sup = sum(1 for e in es if e.get("supersedes"))
        ret = sum(1 for e in es if e.get("is_retracted"))
        exp = sum(1 for e in es
                  if (d := parse_dt(e.get("event_time"))) is not None and d < cutoff)
        ages = [(t_now - parse_dt(e["created_at"])).days for e in es if parse_dt(e["created_at"])]
        newest = f"{min(ages)}d" if ages else "-"
        oldest = f"{max(ages)}d" if ages else "-"
        L.append(f"{cat:24s} {act:4d} {len(es)-act:6d} {sup:7d} {ret:5d} {exp:8d}"
                 f" {newest:>7s} {oldest:>7s}")

    if level < 2:
        L.append("")
        L.append(f"SLOT KEYS BY CATEGORY  (names only, max {SLOT_CAP} per category, alphabetical)")
        for cat in sorted(by_cat):
            names = sorted({n for e in by_cat[cat] if (n := slot_name(e, level))})
            shown, extra = names[:SLOT_CAP], max(0, len(names) - SLOT_CAP)
            body = ", ".join(shown) + (f", (+{extra} more)" if extra else "")
            wrapped = textwrap.wrap(body, width=96,
                                    initial_indent=f"{cat}: ", subsequent_indent="    ")
            L.extend(wrapped or [f"{cat}: (none)"])
    return "\n".join(L)


def main():
    level = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    plan = jload(E0 / "plan.json")["personas"]
    out, lens = {}, []
    for name in sorted(plan):
        t_now = plan[name]["t_now"]
        for variant, stem in (("FULL", f"{name}_full"), ("ABLATED", f"{name}_ablated")):
            entries = jload(STORES / f"{stem}.json")["entries"]
            txt = render(entries, t_now, level)
            out[f"{name}:{variant}"] = txt
            lens.append(txt.count("\n") + 1)
    jdump({"meta": {"tightening_level": level, "slot_cap": SLOT_CAP,
                    "n_indexes": len(out), "no_api_calls": True,
                    "line_count": {"min": min(lens), "max": max(lens),
                                   "mean": round(sum(lens) / len(lens), 1)}},
           "indexes": out}, OUT)
    print(f"level {level}: {len(out)} indexes, lines min {min(lens)} / mean "
          f"{sum(lens)/len(lens):.1f} / max {max(lens)}  (target 40-60)")
    print(f"wrote {OUT}\n")
    k = "elena:FULL"
    print("=" * 100)
    print(f"SAMPLE — {k}")
    print("=" * 100)
    print(out[k])


if __name__ == "__main__":
    main()
