"""
build_indexes.py -- the per-rung BELIEVED index, TRUE and LOBOTOMISED. NO API CALLS.

RENDERER LOCK. `index_v2.render` is imported and called; there is no other code
path to an index in E3, and the renderer is not edited. What changes is only WHICH
ROWS it sees and WHAT CLOCK they are aged against -- the rung's own alive set and
the rung's own t_now.

D51-E3, the reason this file exists rather than reusing indexes_v2.json: the
committed indexes are rendered at a single pinned t_now over the whole bank, and
their BELIEVED lifecycle state comes from `is_active`, which records the store's
FINAL state. An entry superseded at session 30 carries is_active=False in the
committed bank; reusing that at rung 14 would leak future information backwards
into a past store. The rung-correct rule uses the `supersedes` POINTER, which
lives on the newer entry and therefore carries a source_session.

E3_AMENDMENT_1, the reason it now emits TWO index families and a digest:

  TRUE       arm (a)'s index and digest.
  LOBOTOMY   arm (a')'s. ONE frozen permutation of the per-entry `superseded`
             flag within each (persona, rung), applied to the renderer's INPUT
             ROWS. One permutation destroys both objects the amendment names --
             the per-category SUPRSD column and the superseded-names block are
             both projections of that flag -- and it is exactly
             marginal-preserving: the LIFECYCLE TOTALS `active`, `superseded` and
             `supersession events` lines come out BYTE-IDENTICAL, so the
             lobotomised store reports the same aggregate supersession load and
             differs only in WHICH categories and WHICH attributes carry it.

  DIGEST     the application-step object, rendered from the same rows in both
             families: the supersession totals, the per-category counts, and the
             superseded-attribute-name list. Frozen text in E3_AMENDMENT_1 2.4.

Also records, per (persona, rung), BOTH maintenance-cost columns p3 separated and
PREREG_E3 section 1 requires reported separately:
  write-driven   1.11 us/write x writes since the previous rung
  clock-driven   the measured cost of one recency/expiry pass at this rung

Usage:  python e3_metamemory/tools/build_indexes.py
"""

from __future__ import annotations

import collections
import statistics
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e0_common import parse_dt                                     # noqa: E402
from index_v2 import AVAIL, SLOT_CAP, render, scrub                # noqa: E402
from e3_common import (E3, RUNGS, Snapshot, jdump, load_cells,     # noqa: E402
                       session_dates, sha)

MAINTAIN_US_PER_WRITE = 1.11        # p3, measured; probes/p3_index_maintenance.json
REPEATS = 3
DIGEST_HDR = "STORE SUPERSESSION RECORD  (metadata only; no fact content)"


def digest(rows, events):
    """E3_AMENDMENT_1 section 2.4, frozen. Same code for TRUE and LOBOTOMY."""
    sup = [r for r in rows if r["superseded"]]
    by_cat = collections.Counter(r["category"] for r in sup)
    names = sorted({r["slot"] for r in sup if r["slot"]})
    shown, extra = names[:SLOT_CAP], max(0, len(names) - SLOT_CAP)
    cat_line = ", ".join(f"{c} {n}" for c, n in sorted(by_cat.items())) or "(none)"
    name_line = (", ".join(shown) + (f", (+{extra} more)" if extra else "")) or "(none)"
    return "\n".join([
        DIGEST_HDR,
        f"  superseded entries        {len(sup)}",
        f"  supersession events       {len(events)}",
        f"  by category               {cat_line}",
        f"  attribute names carrying superseded content: {name_line}",
    ])


def main():
    cells = load_cells()["cells"]
    personas = sorted({c["persona"] for c in cells})
    dates = session_dates()
    snaps = {p: Snapshot(p, dates[p]) for p in personas}

    true_ix, lob_ix, true_dg, lob_dg, meta, lens = {}, {}, {}, {}, {}, []
    identical_totals = 0
    for p in personas:
        S = snaps[p]
        prev_alive = 0
        for r in RUNGS:
            alive = sorted(S.alive(r))
            t_now = S.t_now(r)
            rows = []
            for eid in alive:
                e = S.by_id[eid]
                age = max(0, (t_now - parse_dt(e["created_at"])).days)
                sk = e.get("slot_key")
                rows.append({
                    "id": eid, "category": e["category"],
                    "slot": scrub(sk[1] if isinstance(sk, list) and len(sk) >= 2
                                  else None),
                    "age": age,
                    "superseded": S.is_superseded_at(eid, r),
                    "retracted": bool(e["is_retracted"]),
                    "expired": S.is_expired_at(eid, r)})
            for x in rows:
                x["active"] = not (x["superseded"] or x["retracted"])
            events = [{eid} for eid in alive if S.by_id[eid].get("supersedes")]

            # ---------- the lobotomy: one frozen permutation of `superseded`,
            # taken WITHIN THE NON-RETRACTED SUBSET. Permuting across the whole
            # row set would move the `active` total, because active is
            # not(superseded or retracted) and the two flags co-occur: a
            # retracted row that gains `superseded` frees an active slot that a
            # non-retracted row does not give back. Restricting the permutation
            # to non-retracted rows preserves `superseded` and `active` exactly.
            # 31 of 18,936 entries in the corpus are retracted.
            seed = int(sha("E3-LOBOTOMY-INDEX", p, r)[:16], 16)
            idx = [i for i, x in enumerate(rows) if not x["retracted"]]
            perm = np.random.default_rng(seed).permutation(len(idx))
            lrows = [dict(x) for x in rows]
            for slot, src in zip(idx, perm):
                lrows[slot]["superseded"] = bool(rows[idx[int(src)]]["superseded"])
            for y in lrows:
                y["active"] = not (y["superseded"] or y["retracted"])

            ts = []
            for _ in range(REPEATS):
                t0 = time.perf_counter()
                txt, _b, _n = render(rows, events, AVAIL[("frbank", "BELIEVED")])
                ts.append((time.perf_counter() - t0) * 1000)
            serve_ms = statistics.median(ts)
            ltxt, _b, _n = render(lrows, events, AVAIL[("frbank", "BELIEVED")])

            # marginal preservation: the LIFECYCLE TOTALS block must be identical
            def totals(t):
                a = t.split("LIFECYCLE TOTALS", 1)[1]
                return a.split("PER-CATEGORY", 1)[0]
            assert totals(txt) == totals(ltxt), f"{p}:R{r}: totals block moved"
            identical_totals += 1

            ts = []
            for _ in range(REPEATS):
                t0 = time.perf_counter()
                for eid in alive:
                    _ = max(0, (t_now - parse_dt(S.by_id[eid]["created_at"])).days)
                    _ = S.is_expired_at(eid, r)
                ts.append((time.perf_counter() - t0) * 1000)
            clock_ms = statistics.median(ts)

            writes = len(alive) - prev_alive
            prev_alive = len(alive)
            key = f"frbank:{p}:R{r}:BELIEVED"
            true_ix[key], lob_ix[key] = txt, ltxt
            true_dg[key] = digest(rows, events)
            lob_dg[key] = digest(lrows, events)
            lens.append(txt.count("\n") + 1)
            meta[key] = {
                "persona": p, "rung": r, "n_entries": len(alive),
                "t_now": t_now.isoformat(),
                "n_superseded": sum(1 for x in rows if x["superseded"]),
                "n_expired": sum(1 for x in rows if x["expired"]),
                "n_sup_events": len(events),
                "writes_since_prev_rung": writes,
                "maintain_us_write_driven": round(writes * MAINTAIN_US_PER_WRITE, 2),
                "serve_ms_render": round(serve_ms, 4),
                "clock_pass_ms": round(clock_ms, 4),
                "index_bytes": len(txt),
                "index_differs": txt != ltxt,
                "digest_differs": true_dg[key] != lob_dg[key],
                "sha256": sha(txt), "sha256_lobotomy": sha(ltxt)}

    n = len(meta)
    ix_diff = sum(1 for v in meta.values() if v["index_differs"])
    dg_diff = sum(1 for v in meta.values() if v["digest_differs"])
    art = sha(*[meta[k]["sha256"] for k in sorted(meta)])
    lart = sha(*[meta[k]["sha256_lobotomy"] for k in sorted(meta)])

    jdump({"renderer": "e1_metamemory/tools/index_v2.render, imported unmodified",
           "provenance": "BELIEVED", "rungs": list(RUNGS),
           "believed_superseded_rule":
               "exists e' with source_session(e') <= rung and e'.supersedes == e.id "
               "(D51-E3; is_active is NOT used)",
           "lobotomy": {
               "spec": "E3_AMENDMENT_1 section 2.2 -- one frozen permutation of the "
                       "per-entry `superseded` flag within each (persona, rung), "
                       "applied to the renderer's input rows",
               "seed": "int(sha256('E3-LOBOTOMY-INDEX|persona|rung')[:16], 16)",
               "marginal_preserving_totals_block_identical": identical_totals,
               "indexes_that_differ": ix_diff, "digests_that_differ": dg_diff},
           "n_indexes": n,
           "artifact_sha256": art, "artifact_sha256_lobotomy": lart,
           "digest_header": DIGEST_HDR,
           "maintain_us_per_write_source":
               "p3, measured 1.11 us/write on a 390-entry persona replay",
           "line_count": {"min": min(lens), "max": max(lens),
                          "mean": round(sum(lens) / len(lens), 1)},
           "meta": meta,
           "indexes": true_ix, "indexes_lobotomy": lob_ix,
           "digests": true_dg, "digests_lobotomy": lob_dg},
          E3 / "indexes_e3.json")

    print("=" * 96)
    print(f"E3 INDEXES -- {n} = {len(personas)} personas x {len(RUNGS)} rungs, "
          f"TRUE + LOBOTOMY")
    print("=" * 96)
    print(f"  TRUE     artifact sha256 {art[:32]}...")
    print(f"  LOBOTOMY artifact sha256 {lart[:32]}...")
    print(f"  lines: min {min(lens)} mean {sum(lens)/len(lens):.1f} max {max(lens)}")
    print(f"\n  MARGINAL PRESERVATION: LIFECYCLE TOTALS block byte-identical between "
          f"TRUE and LOBOTOMY on {identical_totals}/{n}   PASS")
    print(f"  NON-VACUITY (index level): TRUE != LOBOTOMY on {ix_diff}/{n} "
          f"({ix_diff/n:.1%})")
    print(f"  NON-VACUITY (digest level): TRUE != LOBOTOMY on {dg_diff}/{n} "
          f"({dg_diff/n:.1%})")
    print(f"\n  {'rung':>5s} {'entries':>9s} {'superseded':>11s} {'expired':>8s} "
          f"{'events':>7s} {'writes':>8s} {'maintain us':>12s} {'serve ms':>9s} "
          f"{'clock ms':>9s}")
    for r in RUNGS:
        m = [v for v in meta.values() if v["rung"] == r]
        print(f"  {r:>5d} {sum(x['n_entries'] for x in m)/len(m):>9.0f} "
              f"{sum(x['n_superseded'] for x in m):>11d} "
              f"{sum(x['n_expired'] for x in m):>8d} "
              f"{sum(x['n_sup_events'] for x in m):>7d} "
              f"{sum(x['writes_since_prev_rung'] for x in m):>8d} "
              f"{sum(x['maintain_us_write_driven'] for x in m):>12.0f} "
              f"{statistics.median([x['serve_ms_render'] for x in m]):>9.3f} "
              f"{statistics.median([x['clock_pass_ms'] for x in m]):>9.3f}")
    print("\n  The two maintenance columns are reported separately and never averaged:")
    print("  write-driven cost is incurred once per write; the clock pass is incurred")
    print("  once per SERVE, because ages and expiry move with t_now and no write.")
    k = sorted(true_dg)[0]
    print("\n  SAMPLE DIGEST (application-step object) --", k)
    print("  " + "\n  ".join(true_dg[k].split("\n")))
    print("\n  SAME CELL, LOBOTOMISED")
    print("  " + "\n  ".join(lob_dg[k].split("\n")))
    print("\nwrote indexes_e3.json")


if __name__ == "__main__":
    main()
