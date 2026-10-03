# -*- coding: utf-8 -*-
"""build_indexes.py -- R85 Amendment 1 Step 4, the three indexes per persona (section 4 B). NO API CALL. NO WRITE TO THE GRAPH.

Per persona (the forty r85stock_<persona>_g10 groups on neo4j-r85, read only):
  BELIEVED-capped   Graphiti's own fields under RULES 1 and 2, census.py's rows verbatim (D-R85-10 ages), rendered through
                    graphiti_index.build_index at SLOT_CAP = 15; asserted byte-identical to census_runs/g10_<persona>.index.txt
                    (the renderer lock).
  BELIEVED-lifted   the same rows with the cap lifted (build_s2u.py's mechanism: the module constant SLOT_CAP set to the smallest
                    power of ten that never binds on the forty stores, 100 as the amendment names it or the next if 100 binds,
                    recorded); asserted to print no "(+N more)".
  TRUE-projected    the ground-truth join's rows for the persona's FR-Bank FULL bank (index_v2.main's own construction: load_backend,
                    pinned-t_now ages, true_lifecycle) rendered under AVAIL_GRAPHITI; the FR-Bank render of the same rows under
                    AVAIL[("frbank", "TRUE")] asserted byte-identical to the committed index frbank:<persona>:FULL:TRUE (the
                    renderer lock); if the cap binds on the projection, TRUE-projected-lifted is added as section 4 B provides.
Name lists for the readers (NB-6 over the superseded-names section, NB-5 over the whole map) are read from each rendered text by
a section reader over the headers index_v2.render emits (index_features.parse cannot read a no-category index, D-R85-19) and
asserted against the rows they were rendered from.

Writes r85_graphiti/g10/indexes_g10.json and appends AUX-R85-G10-INDEXES to r85_graphiti/NUMBERS_R85.md.
"""
from __future__ import annotations

import collections
import datetime as dt
import hashlib
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R85 = HERE.parent
ROOT = R85.parent
sys.path.insert(0, str(ROOT / "reviews" / "r114" / "tools"))
from r114_common import assert_spec, J, jdump  # noqa: E402
sys.path.insert(0, str(R85))
import graphiti_index as G                                                   # noqa: E402
import census as C                                                           # noqa: E402
import index_v2 as IX                                                        # noqa: E402
from backends import load_backend                                            # noqa: E402
from e0_common import load_joins, parse_dt, toks                             # noqa: E402

LEDGER = R85 / "NUMBERS_R85.md"
OUT = HERE / "indexes_g10.json"
CAP = 15
LIFT_CANDIDATES = (100, 1000)


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def graphiti_rows(persona, group_id):
    """census.py's rows, verbatim."""
    edges = C.read_edges(group_id)
    Jp = load_joins()[persona]
    states = C.derive(edges)
    t_now = Jp.t_now
    rows = []
    for e in edges:
        st = states[e["uuid"]]
        d = parse_dt(e["valid_at"]) or parse_dt(e["created_at"])
        age = max((t_now - d).days, 0) if (d and t_now) else None
        rows.append({"id": e["uuid"], "category": None, "slot": G.attribute_name(e["name"], C.label_of(e)), "age": age,
                     "active": st == "active", "superseded": st == "superseded", "retracted": None, "expired": st == "expired"})
    ev = [{e["uuid"]} for e in edges if e["invalid_at"]]
    return edges, states, rows, ev


def render_capped(rows, ev, cap, avail):
    old = IX.SLOT_CAP
    IX.SLOT_CAP = cap
    try:
        if avail is G.AVAIL_GRAPHITI:
            return G.build_index(rows, ev)[0]
        return IX.render(rows, ev, avail)[0]
    finally:
        IX.SLOT_CAP = old


def frbank_true(persona):
    """index_v2.main's TRUE branch for the persona's FULL FR-Bank bank: rows with pinned-t_now ages, the TRUE states and events."""
    Jp = load_joins()[persona]
    rows = sorted([r for r in load_backend("frbank") if r["persona"] == persona], key=lambda r: r["entry_id"])
    assert rows
    for r in rows:
        d = parse_dt(r["recency_time"])
        r["age"] = None if d is None else max(0, (Jp.t_now - d).days)
    etoks = {r["entry_id"]: toks(r["text"], Jp.drop) for r in rows}
    t_sup, t_ret, t_exp, t_ev = IX.true_lifecycle(Jp, etoks)
    return rows, (t_sup, t_ret, t_exp), t_ev


HDR_ALL = "ATTRIBUTE NAMES  (value-scrubbed"
HDR_SUP = "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT  (value-scrubbed)"
HDR_STOP = ("LIFECYCLE TOTALS", "PER-CATEGORY BREAKDOWN", "RECENCY", "AGE DISTRIBUTION")


def read_names(text):
    """The names printed under the whole-map header and under the superseded header of one rendered index (no category);
    the wrapped body of each section is joined before it is split on commas, so a '(+N more)' broken across a wrap is read whole;
    '(none)' yields []."""
    out = {"all": [], "sup": [], "all_more": 0, "sup_more": 0, "all_marker": False, "sup_marker": False}
    body = {"all": [], "sup": []}
    sec = None
    for ln in text.split("\n"):
        s = ln.strip()
        if s.startswith(HDR_SUP):
            sec = "sup"; continue
        if s.startswith(HDR_ALL) or s.startswith("ATTRIBUTE NAMES BY CATEGORY"):
            sec = "all"; continue
        if any(s.startswith(h) for h in HDR_STOP):
            sec = None; continue
        if sec is None or not s:
            continue
        body[sec].append(s)
    for sec in ("all", "sup"):
        joined = " ".join(body[sec])
        if joined == "(none)" or not joined:
            continue
        if IX.MARKER in joined:
            out[sec + "_marker"] = True; continue
        m = re.search(r"\(\+(\d+) more\)", joined)
        if m:
            out[sec + "_more"] = int(m.group(1)); joined = joined[:m.start()] + joined[m.end():]
        out[sec] = [t.strip() for t in joined.split(",") if t.strip()]
    return out


def main():
    assert_spec()
    sys.stdout.reconfigure(encoding="utf-8")
    committed = J(ROOT / "e1_metamemory" / "indexes_v2.json")["indexes"]
    personas = sorted(load_joins())
    assert len(personas) == 40
    # the lift: the smallest candidate that never binds on the forty Graphiti stores
    per, largest = {}, 0
    for p in personas:
        gid = f"r85stock_{p}_g10"
        edges, states, rows, ev = graphiti_rows(p, gid)
        per[p] = (edges, states, rows, ev)
        largest = max(largest, len({r["slot"] for r in rows if r["slot"]}))
    lift = next(c for c in LIFT_CANDIDATES if c > largest)
    out = {"meta": {"script": "r85_graphiti/g10/build_indexes.py", "cap": CAP, "lift": lift, "largest_whole_map": largest, "lift_note": "the amendment names 100; the next power of ten is used where 100 binds",
                    "avail_graphiti": G.AVAIL_GRAPHITI, "marker": IX.MARKER, "when": dt.datetime.now().isoformat(timespec="seconds")}, "personas": {}}
    n_lock_b, n_lock_t, n_true_cap_binds = 0, 0, 0
    for p in personas:
        edges, states, rows, ev = per[p]
        gid = f"r85stock_{p}_g10"
        rec = J(HERE.parent / "census_runs" / f"g10_{p}.json"); assert rec["group_id"] == gid and rec["edges"] == len(edges)
        cap_txt = render_capped(rows, ev, CAP, G.AVAIL_GRAPHITI)
        committed_capped = (HERE.parent / "census_runs" / f"g10_{p}.index.txt").read_text(encoding="utf-8")
        assert cap_txt == committed_capped, f"{p}: the cap-15 render differs from the census index (renderer lock)"
        n_lock_b += 1
        lift_txt = render_capped(rows, ev, lift, G.AVAIL_GRAPHITI)
        assert "(+" not in lift_txt, f"{p}: the lifted render still truncates"
        nc, nl = read_names(cap_txt), read_names(lift_txt)
        slots_all = sorted({r["slot"] for r in rows if r["slot"]}); slots_sup = sorted({r["slot"] for r in rows if r["superseded"] and r["slot"]})
        assert nl["all"] == slots_all and nl["sup"] == slots_sup and nc["sup"] == slots_sup[:CAP] and nc["all"] == slots_all[:CAP], (p, "name reader")
        assert sorted(nc["sup"]) == sorted(rec["superseded_names"])[:CAP], (p, "superseded names against the census record")
        assert not nc["all_marker"] and not nc["sup_marker"]
        # TRUE-projected
        frows, fst, fev = frbank_true(p)
        v = IX.view(frows, fst, None)
        lock_txt = IX.render(v, fev, IX.AVAIL[("frbank", "TRUE")])[0]
        assert lock_txt == committed[f"frbank:{p}:FULL:TRUE"], f"{p}: the FR-Bank TRUE render differs from the committed index (renderer lock)"
        n_lock_t += 1
        proj_txt = render_capped(v, fev, CAP, G.AVAIL_GRAPHITI)
        binds = "(+" in proj_txt
        n_true_cap_binds += int(binds)
        proj_lift = render_capped(v, fev, lift, G.AVAIL_GRAPHITI) if binds else None
        if proj_lift is not None:
            assert "(+" not in proj_lift
        np_, npl = read_names(proj_txt), (read_names(proj_lift) if proj_lift else None)
        fslots_all = sorted({r["slot"] for r in v if r["slot"]}); fslots_sup = sorted({r["slot"] for r in v if r["superseded"] and r["slot"]})
        assert np_["sup"] == fslots_sup[:CAP] and np_["all"] == fslots_all[:CAP]
        if npl:
            assert npl["all"] == fslots_all and npl["sup"] == fslots_sup
        out["personas"][p] = {
            "group_id": gid, "edges": len(edges), "states": dict(collections.Counter(states.values())), "t_now": load_joins()[p].t_now.isoformat(),
            "believed_capped": {"text": cap_txt, "sha256": sha(cap_txt), "lines": cap_txt.count("\n") + 1, "names_all": nc["all"], "names_sup": nc["sup"], "all_more": nc["all_more"], "sup_more": nc["sup_more"]},
            "believed_lifted": {"text": lift_txt, "sha256": sha(lift_txt), "lines": lift_txt.count("\n") + 1, "names_all": nl["all"], "names_sup": nl["sup"], "cap": lift},
            "true_projected": {"text": proj_txt, "sha256": sha(proj_txt), "lines": proj_txt.count("\n") + 1, "names_all": np_["all"], "names_sup": np_["sup"], "all_more": np_["all_more"], "sup_more": np_["sup_more"], "cap_binds": binds,
                               "frbank_entries": len(frows), "frbank_true_states": {"superseded": len(fst[0]), "retracted": len(fst[1]), "expired": len(fst[2]), "sup_events": len(fev)}},
            "true_projected_lifted": ({"text": proj_lift, "sha256": sha(proj_lift), "lines": proj_lift.count("\n") + 1, "names_all": npl["all"], "names_sup": npl["sup"], "cap": lift} if proj_lift else None),
            "whole_map_names": len(slots_all), "superseded_names": len(slots_sup),
        }
    out["meta"].update({"renderer_lock_believed": n_lock_b, "renderer_lock_true": n_lock_t, "true_projected_cap_binds_on": n_true_cap_binds})
    jdump(out, OUT)
    P = out["personas"]
    wm = [P[p]["whole_map_names"] for p in personas]; sn = [P[p]["superseded_names"] for p in personas]
    lc = [P[p]["believed_capped"]["lines"] for p in personas]; ll = [P[p]["believed_lifted"]["lines"] for p in personas]
    lt = [P[p]["true_projected"]["lines"] for p in personas]; ltl = [P[p]["true_projected_lifted"]["lines"] for p in personas if P[p]["true_projected_lifted"]]
    tsup = [len(P[p]["true_projected"]["names_sup"]) + P[p]["true_projected"]["sup_more"] for p in personas]
    txt = (f"\n### AUX-R85-G10-INDEXES — Step 4, the indexes (2026-09-17, program R114; no call; `g10/build_indexes.py`, `g10/indexes_g10.json`)\n\n"
           f"Forty personas, the `_g10` groups read only. BELIEVED-capped: the cap-15 render reproduces `census_runs/g10_<persona>.index.txt` byte for byte on {n_lock_b} of 40 (renderer lock); "
           f"whole-map names per store {min(wm)} to {max(wm)} (mean {sum(wm)/40:.1f}), superseded names {min(sn)} to {max(sn)} (mean {sum(sn)/40:.2f}; the cap never binds on the superseded section), "
           f"{min(lc)} to {max(lc)} lines. BELIEVED-lifted: `SLOT_CAP` = **{lift}** (the amendment names 100; the largest whole map is {largest}, so 100 binds on the forty stores and the next power of ten is used, D-R85-19), "
           f"no `(+N more)` in any text, {min(ll)} to {max(ll)} lines. TRUE-projected: the persona's FR-Bank FULL rows under the TRUE join rendered under `AVAIL_GRAPHITI` (category and retracted print the marker); "
           f"the same rows under `AVAIL[(frbank, TRUE)]` reproduce the committed `frbank:<persona>:FULL:TRUE` index on {n_lock_t} of 40 (renderer lock); the cap binds on the projection's whole map on **{n_true_cap_binds}** of 40 "
           f"(FR-Bank's slot names in one bucket once the category axis is inexpressible), so TRUE-projected-lifted (cap {lift}) is added as section 4 B provides; {min(lt)} to {max(lt)} lines capped, "
           f"{(str(min(ltl)) + ' to ' + str(max(ltl))) if ltl else '—'} lifted; the projection's superseded-names section holds {min(tsup)} to {max(tsup)} names (the cap of 15 binds on it in {sum(1 for p in personas if P[p]['true_projected']['sup_more'])} personas).\n")
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    main()
