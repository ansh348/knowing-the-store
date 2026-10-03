"""index_v2.py -- E1 Phase B: index v2, the value-scrubbed metadata index.

NO API CALLS. Deterministic. ONE renderer for every (backend, variant, provenance).

Executes PREREG_E1.md section 5 and E1_DESIGN.md section 5. Makes no design decisions
beyond the three reading choices recorded under "SETTLED READINGS" below, each of which
is the conservative branch.

Writes e1_metamemory/indexes_v2.json:

    {"meta": {...},
     "indexes": {"<backend>:<persona>:<variant>:<provenance>": "<text>", ...}}

with SLOT-ABLATED keyed per question as "<backend>:<persona>:SLOT:<qid>:<prov>".

--------------------------------------------------------------------------------
FROZEN RENDERER RULES (pre-registered; not improvised here)
--------------------------------------------------------------------------------
1. VALUE SCRUBBER. Attribute paths are kept, values NEVER. FR-Bank's slot_key is
   [subject, attr]; only `attr` is emitted, with everything after the first ':'
   STRIPPED ("health_condition:atrial_fibrillation" -> "health_condition").
   E0 leaked "medication:warfarin" and "partner_hobby:Lucia" at ladder level 0;
   E1 starts scrubbed. Cap SLOT_CAP names per category, alphabetical, deduplicated.
2. LIFECYCLE FIELDS. Per-category active / superseded / retracted / expired counts,
   supersession-event count, scrubbed superseded attribute names, and recency stats
   (newest and oldest entry age in days against the persona's PINNED t_now).
3. AN INEXPRESSIBLE FIELD EMITS THE LITERAL STRING "not expressible by this backend"
   AND NEVER 0. A zero asserts "there are none of these", which is a different and
   false claim. Enforced by assertion: for every field a backend/provenance cannot
   express, the rendered block carries the marker and contains no digit anywhere.
4. ONE renderer for every (backend, variant, provenance). The only thing that varies
   is which fields are expressible, carried in AVAIL.

--------------------------------------------------------------------------------
SETTLED READINGS (each conservative; reported, not silently absorbed)
--------------------------------------------------------------------------------
R1  PROVENANCE CHANGES EXACTLY ONE THING: where an entry's lifecycle state comes
    from. TRUE reads it from the LifecycleBench persona YAML through the same
    lexical join PersonaJoin uses; BELIEVED reads it from the store's own fields.
    Everything else in the index -- how many entries there are, whether the store
    has named regions to break them down by, whether entries carry attribute names,
    when the store dates its content -- is STRUCTURE, not lifecycle, and is
    identical under both provenances. So per-category and attribute-name blocks are
    marked inexpressible on Mem0 and A-MEM under BOTH provenances: BELIEVED_STATE.md
    ("Region structure") establishes that as a fact about the STORES ("FR-Bank has
    it ... Mem0 and A-MEM do not"), not about their metadata quality, and ground
    truth cannot hand a Mem0 point a category without putting a classifier in the
    path, which E1_DESIGN.md section 4 forbids. Every LIFECYCLE field is expressible
    under TRUE on all three backends, as the prereg requires.

R2  THE INDEX TEXT NAMES NEITHER BACKEND, VARIANT, NOR PROVENANCE. Printing
    "variant: SLOT-ABLATED" would tell the model the store had been ablated, which
    is the manipulation the hard tier measures; printing "Mem0" or "A-MEM" would
    invite a pretrained brand prior; printing "provenance: BELIEVED" would tell the
    model the numbers may be the store's own wrong beliefs, which is the axis
    H-BELIEVED measures. All three live in the index KEY, never in the text. The
    frozen USER_INDEXED prompt already supplies the marker's semantics, so the text
    needs no provenance note of its own.

R3  RECENCY IS TAKEN FROM THE FIELD EACH STORE USES TO DATE ITS CONTENT --
    FR-Bank created_at, Mem0 payload `date`, A-MEM `timestamp`, all the
    LifecycleBench session date -- normalized as `recency_time` in backends.py.
    NOT from ingest wall-clock: on Mem0 and A-MEM that is one afternoon in 2026-05
    for the entire corpus, so an age taken against a session-date t_now would be an
    instrument error rather than a believed-state finding, and A-MEM's believed
    index would lose the recency half of the count-and-recency structure the
    pre-registered lifecycle-ablation decomposition reads. BELIEVED_STATE.md lists
    A-MEM's believed index as built from "timestamp and last_accessed" and Mem0's
    recency as expressible; both are honoured. Mem0's `date` is rewritten to the
    update-time session on the 12.7% of points carrying updated_at -- that
    corruption is a believed-state property and is left in.

t_now is PINNED per persona from the FULL FR-Bank bank (e0_common PersonaJoin.t_now,
= newest ACTIVE created_at + 24h) and is used byte-identically for every backend,
variant and provenance of that persona. Ages are days before it, floored at 0.

Usage:  python e1_metamemory/tools/index_v2.py
"""

from __future__ import annotations

import collections
import io
import json
import statistics
import sys
import textwrap
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e0_common import (  # noqa: E402
    CROSS_GUARD, EXPIRY_WINDOW, MIN_DISCR, MIN_SHARED, TAU_GOLD,
    cov, load_joins, parse_dt, toks,
)
from backends import BACKENDS, load_backend  # noqa: E402

OUT = E1 / "indexes_v2.json"
BUILD = E1 / "build"

MARKER = "not expressible by this backend"
SLOT_CAP = 15
# Wrap width for the attribute-name blocks. Cosmetic only -- it moves line counts,
# never content. Set so FR-Bank lands near the 40-60 line target with the rule-1 cap
# of 15 names per category intact; the cap is pre-registered and is NOT tuned here.
WRAP = 150
TAU_HI = 0.80                     # E0 tau_hi, carried unchanged (PREREG_E1.md section 3)
MEM0_EXCLUDE = {"alex", "thanh", "aisha"}
PROVENANCES = ("TRUE", "BELIEVED")

LIFECYCLE = ("active", "superseded", "retracted", "expired", "sup_events")
FIELDS = ("category", "slot", "recency") + LIFECYCLE

# ---------------------------------------------------------------------------
# Field availability. TRUE rows: every lifecycle field is expressible on every
# backend, because the YAML join settles it (PREREG_E1.md section 5). Structure
# rows (category / slot) follow the store, per R1 and BELIEVED_STATE.md
# "Region structure". BELIEVED rows are BELIEVED_STATE.md's measured table.
# ---------------------------------------------------------------------------
def _av(category, slot, active, superseded, retracted, expired, sup_events, recency):
    return {"category": category, "slot": slot, "active": active,
            "superseded": superseded, "retracted": retracted, "expired": expired,
            "sup_events": sup_events, "recency": recency}


AVAIL = {
    #                        cat   slot   act   sup    ret    exp    sev    rec
    ("frbank", "TRUE"):     _av(True,  True,  True,  True,  True,  True,  True,  True),
    ("frbank", "BELIEVED"): _av(True,  True,  True,  True,  True,  True,  True,  True),
    ("mem0",   "TRUE"):     _av(False, False, True,  True,  True,  True,  True,  True),
    ("mem0",   "BELIEVED"): _av(False, False, False, True,  False, False, False, True),
    ("amem",   "TRUE"):     _av(False, False, True,  True,  True,  True,  True,  True),
    ("amem",   "BELIEVED"): _av(False, False, False, False, False, False, False, True),
}

AVAIL_WHY = {
    ("mem0", "BELIEVED"): {
        "category": "no category field in the payload",
        "slot": "no slot field in the payload",
        "active": "no active/inactive state; _update_memory rewrites the payload in place",
        "superseded": "EXPRESSIBLE as a bare boolean only: presence of updated_at "
                      "(1,276 / 10,074 points); the prior value is destroyed",
        "retracted": "_delete_memory hard-deletes, leaving no trace in the store",
        "expired": "no event-time field",
        "sup_events": "updated_at points at nothing; no event record survives",
    },
    ("amem", "BELIEVED"): {
        "category": "constant 'Uncategorized' on all 11,319 notes",
        "slot": "no slot field; tags share zero names with the FR ontology",
        "active": "no lifecycle field of any kind",
        "superseded": "no lifecycle field of any kind",
        "retracted": "no lifecycle field of any kind",
        "expired": "no lifecycle field of any kind",
        "sup_events": "the 23,403 `links` references resolve to 0 note ids and are "
                      "NEVER used to synthesise a supersession graph",
    },
    ("mem0", "TRUE"): {"category": "store has no named regions (R1)",
                       "slot": "store carries no attribute names (R1)"},
    ("amem", "TRUE"): {"category": "store has no named regions (R1)",
                       "slot": "store carries no attribute names (R1)"},
}

AGE_BANDS = ((0, 30, "0-30"), (31, 90, "31-90"), (91, 180, "91-180"),
             (181, 365, "181-365"), (366, 10 ** 9, "over 365"))


# --------------------------------------------------------------------- helpers
def jdump(obj, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def scrub(slot):
    """RULE 1. Attribute path in, value out. Never returns a name containing ':'."""
    if not slot:
        return None
    name = str(slot).split(":", 1)[0].strip()
    return name or None


def detect(old_fact, new_fact, etoks, drop):
    """PersonaJoin.detector, parameterised over an arbitrary entry-token map.

    Byte-identical computation to e0_common.PersonaJoin.detector (asserted at run
    time against it on FR-Bank), so the SAME ground-truth join runs on all three
    backends rather than a per-backend variant of it.
    """
    ot, nt = toks(old_fact, drop), toks(new_fact, drop)
    do, dn = ot - nt, nt - ot
    if len(do) < MIN_DISCR or len(dn) < MIN_DISCR:
        return None
    return {i: cov(do, t) for i, t in etoks.items()
            if len(do & t) >= MIN_SHARED and cov(dn, t) < CROSS_GUARD}


# ------------------------------------------------------------- lifecycle states
def true_lifecycle(J, etoks):
    """TRUE provenance: lifecycle state from the persona YAML, for ANY backend.

    superseded : asserts the old_fact of a supersession_events / contradictions
                 record at discriminative coverage >= TAU_HI, cross-guarded.
    retracted  : asserts the original_fact of a retractions record, same rule.
    expired    : anchors an expiring_logistics fact whose YAML `status` is
                 'expired'. YAML status fields override derived cutoffs
                 (PREREG_E1.md section 3), so no date arithmetic enters here.
    sup_events : one entry-id set per resolvable YAML supersession event, holding
                 the entries asserting EITHER side of it; an event counts in a
                 variant when at least one of them survives in that variant.
    """
    superseded, retracted, expired, events = set(), set(), set(), []
    for sec in ("supersession_events", "contradictions"):
        for rec in (J.y.get(sec) or []):
            if not isinstance(rec, dict):
                continue
            old, new = rec.get("old_fact"), rec.get("new_fact")
            d_old = detect(old, new, etoks, J.drop)
            if d_old is None:                     # discriminator undefined: unresolvable
                continue
            hit_old = {i for i, s in d_old.items() if s >= TAU_HI}
            d_new = detect(new, old, etoks, J.drop) or {}
            hit_new = {i for i, s in d_new.items() if s >= TAU_HI}
            superseded |= hit_old
            if hit_old or hit_new:
                events.append(hit_old | hit_new)
    for rec in (J.y.get("retractions") or []):
        if not isinstance(rec, dict):
            continue
        d = detect(rec.get("original_fact"), rec.get("retraction"), etoks, J.drop)
        if d:
            retracted |= {i for i, s in d.items() if s >= TAU_HI}
    for rec in (J.y.get("expiring_logistics") or []):
        if not isinstance(rec, dict):
            continue
        if str(rec.get("status") or "").strip().lower() != "expired":
            continue
        ft = toks(rec.get("fact"), J.drop)
        if len(ft) < MIN_DISCR:
            continue
        expired |= {i for i, t in etoks.items()
                    if len(ft & t) >= MIN_SHARED and cov(ft, t) >= TAU_GOLD}
    return superseded, retracted, expired, events


def believed_lifecycle(backend, rows, cutoff):
    """BELIEVED provenance: lifecycle state from the store's OWN fields only.

    Every value is None wherever the store cannot express it -- never False, which
    would be the claim "the store says no". AVAIL is asserted against this.
    """
    superseded, retracted, expired, events = set(), set(), set(), []
    for r in rows:
        eid = r["entry_id"]
        if r["believed_superseded"]:              # FR-Bank !is_active; Mem0 updated_at
            superseded.add(eid)
        if r["believed_retracted"]:
            retracted.add(eid)
        if r["believed_supersedes"]:              # FR-Bank `supersedes` pointer
            events.append({eid})
        d = parse_dt(r["event_time"])
        if d is not None and cutoff is not None and d < cutoff:
            expired.add(eid)
    if backend != "frbank":
        retracted, expired, events = None, None, None
    if backend == "amem":
        superseded = None
    return superseded, retracted, expired, events


# ------------------------------------------------------------------- THE RENDERER
def render(rows, events, avail):
    """The one renderer. Same code path for every backend, variant and provenance.

    rows   : [{id, category, slot, age, active, superseded, retracted, expired}]
             where each lifecycle value is a bool, or None where inexpressible.
    events : list of entry-id sets (one per supersession event), or None.
    avail  : the AVAIL row for this (backend, provenance).

    Returns (text, blocks, emitted_slot_names) where blocks maps each field to the
    line indices that field owns, so the marker/no-digit rule can be asserted on
    exactly the lines the field is responsible for.
    """
    L, blocks = [], collections.defaultdict(list)
    surv = {r["id"] for r in rows}

    def add(line, *fields):
        L.append(line)
        for f in fields:
            blocks[f].append(len(L) - 1)

    def count(field):
        if not avail[field]:
            return MARKER
        if field == "sup_events":
            return str(sum(1 for ev in events if ev & surv))
        return str(sum(1 for r in rows if r[field]))

    ages = [r["age"] for r in rows if r["age"] is not None] if avail["recency"] else []

    # ---------------------------------------------------------------- header
    add("MEMORY STORE INDEX  (metadata only; no fact content)")
    add(f"entries in this store: {len(rows)}")
    add("Ages below are in days before the store's pinned current time.")
    add("")

    # ------------------------------------------------------- lifecycle totals
    add("LIFECYCLE TOTALS")
    for f, label in (("active", "active"), ("superseded", "superseded"),
                     ("retracted", "retracted"), ("expired", "expired"),
                     ("sup_events", "supersession events")):
        add(f"  {label:<22s}{count(f)}", f)
    add("")

    # ------------------------------------------------------- per-category table
    add("PER-CATEGORY BREAKDOWN", "category")
    if not avail["category"]:
        add(f"  {MARKER}", "category")
    else:
        cols = [f for f in ("active", "superseded", "retracted", "expired") if avail[f]]
        head = {"active": "ACTIVE", "superseded": "SUPRSD",
                "retracted": "RETRACT", "expired": "EXPIRED"}
        hdr = f"{'CATEGORY':<24s}{'ENTRIES':>8s}" + "".join(f"{head[c]:>9s}" for c in cols)
        if avail["recency"]:
            hdr += f"{'NEWEST':>8s}{'OLDEST':>8s}"
        add(hdr, "category", *cols)
        by_cat = collections.defaultdict(list)
        for r in rows:
            by_cat[r["category"]].append(r)
        for cat in sorted(by_cat):
            es = by_cat[cat]
            line = f"{str(cat):<24s}{len(es):>8d}"
            line += "".join(f"{sum(1 for e in es if e[c]):>9d}" for c in cols)
            if avail["recency"]:
                a = [e["age"] for e in es if e["age"] is not None]
                line += f"{(min(a) if a else 0):>8d}{(max(a) if a else 0):>8d}"
            add(line, "category", *cols)
    add("")

    # -------------------------------------------------------------- recency
    add("RECENCY", "recency")
    if not avail["recency"] or not ages:
        add(f"  {MARKER}" if not avail["recency"] else "  (none)", "recency")
    else:
        for label, v in (("newest entry", min(ages)), ("oldest entry", max(ages)),
                         ("median entry age", int(round(statistics.median(ages))))):
            add(f"  {label:<22s}{v}", "recency")
    add("")
    add("AGE DISTRIBUTION  (entries by age band)", "recency")
    if not avail["recency"]:
        add(f"  {MARKER}", "recency")
    else:
        for lo, hi, label in AGE_BANDS:
            add(f"  {label:<22s}{sum(1 for a in ages if lo <= a <= hi)}", "recency")
    add("")

    # ------------------------------------------------- attribute names (scrubbed)
    names_emitted = []

    def name_block(pairs, header, indent_cat):
        """pairs: [(bucket_label, [names])]. RULE 1 cap applied here, once."""
        add(header, "slot")
        if not pairs:
            add("  (none)", "slot")
            return
        for bucket, names in pairs:
            names = sorted(set(names))
            names_emitted.extend(names)
            shown, extra = names[:SLOT_CAP], max(0, len(names) - SLOT_CAP)
            body = ", ".join(shown) + (f", (+{extra} more)" if extra else "")
            if not shown:
                add(f"{bucket}: (none)" if indent_cat else "  (none)", "slot")
                continue
            wrapped = textwrap.wrap(
                body, width=WRAP,
                initial_indent=(f"{bucket}: " if indent_cat else "  "),
                subsequent_indent="    ")
            for w in wrapped:
                add(w, "slot")

    cap_note = f"; names only, max {SLOT_CAP} per category, alphabetical" if avail["slot"] else ""
    if not avail["slot"]:
        add("ATTRIBUTE NAMES BY CATEGORY  (value-scrubbed)", "slot")
        add(f"  {MARKER}", "slot")
    elif not avail["category"]:
        name_block([("", [r["slot"] for r in rows if r["slot"]])],
                   f"ATTRIBUTE NAMES  (value-scrubbed{cap_note})", False)
    else:
        by_cat = collections.defaultdict(list)
        for r in rows:
            if r["slot"]:
                by_cat[r["category"]].append(r["slot"])
        name_block(sorted(by_cat.items()),
                   f"ATTRIBUTE NAMES BY CATEGORY  (value-scrubbed{cap_note})", True)
    add("")

    hdr2 = "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT  (value-scrubbed)"
    if not (avail["slot"] and avail["superseded"]):
        add(hdr2, "slot", "superseded")
        add(f"  {MARKER}", "slot", "superseded")
    else:
        name_block([("", [r["slot"] for r in rows if r["superseded"] and r["slot"]])],
                   hdr2, False)

    return "\n".join(L), dict(blocks), names_emitted


# ------------------------------------------------------------------------ build
def view(rows, states, ids=None):
    """Project normalized entries + a lifecycle state triple into renderer rows."""
    superseded, retracted, expired = states
    out = []
    for r in rows:
        if ids is not None and r["entry_id"] in ids:
            continue
        eid = r["entry_id"]
        out.append({
            "id": eid,
            "category": r["category"],
            "slot": scrub(r["slot"]),
            "age": r["age"],
            "superseded": (eid in superseded) if superseded is not None else None,
            "retracted": (eid in retracted) if retracted is not None else None,
            "expired": (eid in expired) if expired is not None else None,
            "active": (None if (superseded is None or retracted is None)
                       else (eid not in superseded and eid not in retracted)),
        })
    return out


def main():
    joins = load_joins()
    personas = sorted(joins)
    cat_plan = jload(BUILD / "variant_plan.json")["cat_ablation"]
    slot_abl = jload(BUILD / "slot_ablations.json")

    raw = {b: collections.defaultdict(list) for b in BACKENDS}
    for b in BACKENDS:
        for r in load_backend(b):
            raw[b][r["persona"]].append(r)

    indexes, lens, clamped = {}, collections.defaultdict(list), collections.Counter()
    detector_checks = 0
    slot_names_seen = set()
    assert_b_checked = collections.Counter()

    for name in personas:
        J = joins[name]
        t_now, cutoff = J.t_now, J.cutoff
        assert t_now is not None, f"{name}: t_now not pinned"

        for b in BACKENDS:
            if b == "mem0" and name in MEM0_EXCLUDE:
                continue
            rows = sorted(raw[b].get(name, []), key=lambda r: r["entry_id"])
            assert rows, f"{b}:{name}: no entries"

            # pinned-t_now ages, floored at 0 (a store may date content after t_now)
            for r in rows:
                d = parse_dt(r["recency_time"])
                if d is None:
                    r["age"] = None
                    continue
                days = (t_now - d).days
                if days < 0:
                    clamped[b] += 1
                r["age"] = max(0, days)

            etoks = {r["entry_id"]: toks(r["text"], J.drop) for r in rows}
            if b == "frbank":                     # the join is PersonaJoin's, verbatim
                for rec in (J.y.get("supersession_events") or []):
                    if not isinstance(rec, dict):
                        continue
                    assert detect(rec.get("old_fact"), rec.get("new_fact"),
                                  etoks, J.drop) == J.detector(rec.get("old_fact"),
                                                               rec.get("new_fact")), name
                    detector_checks += 1

            t_sup, t_ret, t_exp, t_ev = true_lifecycle(J, etoks)
            b_sup, b_ret, b_exp, b_ev = believed_lifecycle(b, rows, cutoff)
            states = {"TRUE": ((t_sup, t_ret, t_exp), t_ev),
                      "BELIEVED": ((b_sup, b_ret, b_exp), b_ev)}

            plan = [("FULL", None)]
            if b == "frbank":
                cats = set(cat_plan[name]["categories"])
                plan.append(("CAT-ABLATED",
                             {r["entry_id"] for r in rows if r["category"] in cats}))
                for qid_key in sorted(k for k in slot_abl if k.startswith(name + ":")):
                    qid = qid_key.split(":", 1)[1]
                    rm = set(slot_abl[qid_key])
                    assert rm <= set(etoks), f"{qid_key}: removal ids not in bank"
                    plan.append((f"SLOT:{qid}", rm))

            for vname, removed in plan:
                for prov in PROVENANCES:
                    st, ev = states[prov]
                    v = view(rows, st, removed)
                    txt, blocks, names = render(v, ev, AVAIL[(b, prov)])
                    indexes[f"{b}:{name}:{vname}:{prov}"] = txt
                    lens[(b, prov)].append(txt.count("\n") + 1)
                    slot_names_seen.update(names)

                    # -------- ASSERTION (b), enforced on every index as it is built
                    lines = txt.split("\n")
                    for f in FIELDS:
                        if AVAIL[(b, prov)][f]:
                            continue
                        blk = [lines[i] for i in blocks.get(f, [])]
                        assert blk, f"{b}:{name}:{vname}:{prov}: field {f} renders nothing"
                        assert any(MARKER in ln for ln in blk), \
                            f"{b}:{name}:{vname}:{prov}: {f} lacks the marker"
                        bad = [ln for ln in blk if any(c.isdigit() for c in ln)]
                        assert not bad, \
                            f"{b}:{name}:{vname}:{prov}: {f} emits a digit: {bad!r}"
                        assert_b_checked[(b, prov, f)] += 1

    # ------------------------------------------------------------- assertion (a)
    bad_names = sorted(n for n in slot_names_seen if ":" in n)
    assert not bad_names, f"scrubber leaked {len(bad_names)} names with ':': {bad_names[:5]}"

    # ------------------------------------------------------------- assertion (c)
    expected = (len(personas) * 2                              # frbank FULL
                + len(personas) * 2                            # frbank CAT-ABLATED
                + len(slot_abl) * 2                            # frbank SLOT (per question)
                + (len(personas) - len(MEM0_EXCLUDE)) * 2      # mem0 FULL
                + len(personas) * 2)                           # amem FULL
    assert len(indexes) == expected, f"{len(indexes)} indexes, expected {expected}"

    # ------------------------------------------------------------------- output
    all_lens = [n for v in lens.values() for n in v]
    meta = {
        "no_api_calls": True,
        "n_indexes": len(indexes),
        "expected_indexes": expected,
        "marker": MARKER,
        "slot_cap": SLOT_CAP,
        "thresholds": {"tau_hi": TAU_HI, "tau_gold": TAU_GOLD,
                       "expiry_window_days": EXPIRY_WINDOW.days},
        "key_format": {
            "standard": "<backend>:<persona>:<variant>:<provenance>",
            "slot_ablated": "<backend>:<persona>:SLOT:<question_id>:<provenance>",
        },
        "variants": {"frbank": ["FULL", "CAT-ABLATED", "SLOT (per question)"],
                     "mem0": ["FULL"], "amem": ["FULL"]},
        "mem0_excluded_personas": sorted(MEM0_EXCLUDE),
        "availability": {f"{b}:{p}": AVAIL[(b, p)] for b, p in sorted(AVAIL)},
        "availability_reasons": {f"{b}:{p}": v for (b, p), v in sorted(AVAIL_WHY.items())},
        "settled_readings": {
            "R1": "provenance sets lifecycle source only; category/slot follow the store "
                  "under BOTH provenances (BELIEVED_STATE.md 'Region structure')",
            "R2": "index text names neither backend, variant nor provenance; all three "
                  "live in the key, so the ablation is not announced to the model",
            "R3": "recency from each store's own content date (backends.recency_time), "
                  "not the ingest wall-clock",
        },
        "t_now": "pinned per persona from the FULL FR-Bank bank "
                 "(e0_common PersonaJoin.t_now); byte-identical across every "
                 "backend, variant and provenance of that persona",
        "ages_clamped_at_zero": dict(clamped),
        "detector_equivalence_checks": detector_checks,
        "distinct_scrubbed_attribute_names": len(slot_names_seen),
        "line_count": {"min": min(all_lens), "max": max(all_lens),
                       "mean": round(sum(all_lens) / len(all_lens), 1)},
        "line_count_by_cell": {
            f"{b}:{p}": {"n": len(v), "min": min(v), "max": max(v),
                         "mean": round(sum(v) / len(v), 1)}
            for (b, p), v in sorted(lens.items())},
        "assertions": {
            "a_no_colon_in_emitted_slot_names": True,
            "b_inexpressible_fields_marker_only": {
                f"{b}:{p}:{f}": n for (b, p, f), n in sorted(assert_b_checked.items())},
            "c_index_count_matches_expected": True,
        },
    }
    jdump({"meta": meta, "indexes": indexes}, OUT)

    # -------------------------------------------------------------------- report
    print("=" * 96)
    print(f"INDEX v2 — {len(indexes)} indexes written to {OUT}")
    print("=" * 96)
    print(f"{'cell':22s} {'n':>5s} {'min':>5s} {'mean':>7s} {'max':>5s}   target 40-60")
    for (b, p), v in sorted(lens.items()):
        print(f"{b + ':' + p:22s} {len(v):5d} {min(v):5d} {sum(v)/len(v):7.1f} {max(v):5d}")
    print(f"{'ALL':22s} {len(all_lens):5d} {min(all_lens):5d} "
          f"{sum(all_lens)/len(all_lens):7.1f} {max(all_lens):5d}")
    hist = collections.Counter(min(n // 10 * 10, 90) for n in all_lens)
    print("\n  line-count histogram (10-line bins): " +
          "  ".join(f"{k}-{k+9}:{hist[k]}" for k in sorted(hist)))
    print(f"  distinct scrubbed attribute names emitted: {len(slot_names_seen)}")
    print(f"  ages clamped at 0 (content dated after pinned t_now): {dict(clamped) or 'none'}")

    print("\n" + "=" * 96)
    print("ASSERTIONS")
    print("=" * 96)
    print(f"  (a) no ':' inside any emitted attribute name        PASS  "
          f"({len(slot_names_seen)} distinct names, 0 containing ':')")
    ncells = len({(b, p) for (b, p, f) in assert_b_checked})
    print(f"  (b) inexpressible field => marker, never a digit    PASS  "
          f"({sum(assert_b_checked.values())} field-checks over "
          f"{len(assert_b_checked)} (cell, field) pairs in {ncells} cells)")
    for (b, p, f) in sorted(assert_b_checked):
        why = AVAIL_WHY.get((b, p), {}).get(f, "")
        print(f"        {b}:{p}:{f:11s} {assert_b_checked[(b, p, f)]:4d} indexes   {why}")
    print(f"  (c) index count == expected combinations           PASS  "
          f"({len(indexes)} == {expected} = 40x2 FULL + 40x2 CAT + "
          f"{len(slot_abl)}x2 SLOT + 37x2 mem0 + 40x2 amem)")
    print(f"  (+) FR-Bank TRUE join == PersonaJoin.detector       PASS  "
          f"({detector_checks} record-level equality checks)")

    for k in ("frbank:elena:FULL:TRUE", "amem:elena:FULL:BELIEVED"):
        print("\n" + "=" * 96)
        print(f"SAMPLE — {k}   ({indexes[k].count(chr(10)) + 1} lines)")
        print("=" * 96)
        print(indexes[k])


if __name__ == "__main__":
    main()
