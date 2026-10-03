"""
believed_recall.py -- how much of the genuine supersession structure does FR-Bank's
OWN metadata actually see? NO API CALLS.

PREREG_E2 section 4 asserts a number in the prereg's own voice, so the number has
to be auditable rather than quoted. This computes it from E1's committed
artifacts, using E1's own machinery unmodified:

  TRUE superseded   index_v2.true_lifecycle(J, etoks) -- the YAML-native join,
                    discriminative-token detector at TAU_HI, cross-guarded
  BELIEVED superseded  backends.py's `believed_superseded`, which on FR-Bank is
                    exactly `not is_active`

  recall = |TRUE and BELIEVED| / |TRUE|

Reported at two granularities, because they answer different questions: entry
level (what fraction of genuinely superseded ENTRIES does the store flag?) and
event level (what fraction of supersession EVENTS leave at least one flagged
side?). Policy (vi) reads the entry level, so that is the one the prereg quotes.

Usage:  python e2_metamemory/tools/believed_recall.py
"""

from __future__ import annotations

import collections
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "e2_metamemory" / "believed_recall.json"

sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))

from e0_common import load_joins, toks          # noqa: E402
import index_v2 as IX                            # noqa: E402
from backends import load_backend                # noqa: E402


def main():
    joins = load_joins()
    raw = collections.defaultdict(list)
    for r in load_backend("frbank"):
        raw[r["persona"]].append(r)

    per, tot_true, tot_hit, ev_tot, ev_hit = [], 0, 0, 0, 0
    for name in sorted(joins):
        J = joins[name]
        rows = sorted(raw[name], key=lambda r: r["entry_id"])
        etoks = {r["entry_id"]: toks(r["text"], J.drop) for r in rows}
        t_sup, _t_ret, _t_exp, t_ev = IX.true_lifecycle(J, etoks)
        believed = {r["entry_id"] for r in rows if r["believed_superseded"]}
        hit = len(t_sup & believed)
        tot_true += len(t_sup)
        tot_hit += hit
        e_t = e_h = 0
        for ev in t_ev:
            e_t += 1
            e_h += 1 if (ev & believed) else 0
        ev_tot += e_t
        ev_hit += e_h
        per.append({"persona": name, "true_superseded": len(t_sup),
                    "believed_flagged": hit, "events": e_t, "events_flagged": e_h,
                    "recall": (hit / len(t_sup)) if t_sup else None})

    res = {
        "no_api_calls": True,
        "backend": "frbank",
        "true_source": "index_v2.true_lifecycle -- the YAML-native join, unmodified",
        "believed_source": "backends.believed_superseded, i.e. `not is_active`",
        "entry_level": {"true_superseded": tot_true, "believed_flagged": tot_hit,
                        "recall": tot_hit / tot_true,
                        "missed": tot_true - tot_hit},
        "event_level": {"events": ev_tot, "at_least_one_side_flagged": ev_hit,
                        "recall": ev_hit / ev_tot},
        "reading": (
            "Policy (vi) reads entry-level flags, so entry-level recall is the "
            "figure the prereg quotes. Roughly two in five genuinely superseded "
            "entries are invisible to the deployable obligation map, which is why "
            "H-C2 under the BELIEVED index is the strictest deployable form of the "
            "FR bridge rather than a weakened one."),
        "personas_with_no_true_supersession": sum(1 for p in per
                                                  if p["true_superseded"] == 0),
        "per_persona": per,
    }
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    e, v = res["entry_level"], res["event_level"]
    print(f"ENTRY LEVEL  {e['believed_flagged']}/{e['true_superseded']} genuinely "
          f"superseded entries flagged -> recall {e['recall']:.4f} "
          f"({e['missed']} invisible)")
    print(f"EVENT LEVEL  {v['at_least_one_side_flagged']}/{v['events']} events with "
          f"a flagged side -> recall {v['recall']:.4f}")
    print(f"personas with no resolvable supersession: "
          f"{res['personas_with_no_true_supersession']}/40")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
