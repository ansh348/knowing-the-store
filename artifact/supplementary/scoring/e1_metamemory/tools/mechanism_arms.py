"""
mechanism_arms.py -- E1.8 STEP 2: build the A1/A2/A3 mechanism-probe indexes.

NO API CALLS. Deterministic. Writes e1_metamemory/mechanism_indexes.json.

Base = the intact TRUE index from indexes_v2.json, unchanged. Each arm applies
exactly ONE manipulation, to COUNTS ONLY:

  A1  counts-jittered   count -> round(count * m[slot]), m ~ U[0.5, 2.0] drawn
                        once per slot with random.Random(42), the SAME multiplier
                        for that slot on every item ("same jitter across items").
  A2  counts-coarsened  count -> "0" | "few" | "many", bucketed at T (below).
  A3  names-only        every count removed and replaced by "-"; category names,
                        lifecycle-state names and attribute names all retained.

WHAT COUNTS AS A COUNT (the whole rule, no discretion left):

    entries in this store: N
    LIFECYCLE TOTALS        active / superseded / retracted / expired /
                            supersession events
    PER-CATEGORY BREAKDOWN  ENTRIES, ACTIVE, SUPRSD, RETRACT, EXPIRED
    AGE DISTRIBUTION        the five band counts
    attribute-name blocks   the "(+N more)" overflow

Everything else is left byte-identical. In particular AGES ARE NOT COUNTS and are
untouched in all three arms -- the per-category NEWEST / OLDEST columns and the
RECENCY block (newest / oldest / median entry age) carry through unchanged, so
recency is held constant and the manipulation stays single-channel. The
"not expressible by this backend" marker is not a count and is never altered.

A1 and A2 preserve zero-ness exactly (0 stays 0, and "0" is its own bucket);
A3 destroys it. The ladder therefore destroys strictly more count information at
each rung: magnitude corrupted -> magnitude coarsened -> magnitude and zero-ness
both gone.

Usage:  python e1_metamemory/tools/mechanism_arms.py
"""

from __future__ import annotations

import collections
import hashlib
import io
import json
import random
import re
import statistics as st
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
OUT = E1 / "mechanism_indexes.json"

SEED = 42
JITTER_LO, JITTER_HI = 0.5, 2.0
MARKER = "not expressible by this backend"
LIFECYCLE_LABELS = ("active", "superseded", "retracted", "expired",
                    "supersession events")
COUNT_COLS = ("ENTRIES", "ACTIVE", "SUPRSD", "RETRACT", "EXPIRED")
AGE_COLS = ("NEWEST", "OLDEST")
AGE_BAND_LABELS = ("0-30", "31-90", "91-180", "181-365", "over 365")
OVERFLOW_RE = re.compile(r"\(\+(\S+) more\)")


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


# --------------------------------------------------------------------------- #
# Parse the rendered index into (line, kind, slot, value) count sites.
# The renderer's grammar is fixed (tools/index_v2.py render()), so this is a
# parse, not a heuristic. Anything that does not match a named site is not a
# count and is never touched.
# --------------------------------------------------------------------------- #
def count_sites(text):
    """Return [(line_index, kind, slot, token, extra)] for every count SITE.

    `token` is the raw string occupying the site. It is an integer literal in the
    intact index and may be "few"/"many"/"-" in a manipulated one -- the parse is
    tolerant on purpose, so the same function can locate the sites in all four
    texts and the "nothing but counts moved" assertion can compare them.
    """
    lines = text.split("\n")
    sites = []
    block = None
    cols = None
    for i, ln in enumerate(lines):
        if ln.startswith("entries in this store: "):
            sites.append((i, "kv", "total_entries", ln.split(": ", 1)[1], None))
            continue
        if ln.startswith("LIFECYCLE TOTALS"):
            block = "life"; continue
        if ln.startswith("PER-CATEGORY BREAKDOWN"):
            block = "percat"; cols = None; continue
        if ln.startswith("RECENCY"):
            block = "recency"; continue
        if ln.startswith("AGE DISTRIBUTION"):
            block = "age"; continue
        if ln.startswith("ATTRIBUTE NAMES"):
            block = "names"; continue
        if not ln.strip():
            continue

        if block == "life":
            lab = ln[2:24].strip()
            val = ln[24:].strip()
            if lab in LIFECYCLE_LABELS and val != MARKER:
                sites.append((i, "kv", f"lifecycle.{lab}", val, None))
        elif block == "percat":
            if ln.startswith("CATEGORY"):
                cols = ln.split()[1:]
                continue
            if cols is None or ln.strip() == MARKER:
                continue
            parts = ln.split()
            cat, nums = parts[0], parts[1:]
            assert len(nums) == len(cols), f"percat arity {len(nums)} vs {len(cols)}"
            for c, v in zip(cols, nums):
                if c in COUNT_COLS:
                    sites.append((i, "percat", f"percat.{cat}.{c}", v, (cat, cols)))
        elif block == "age":
            lab = ln[2:24].strip()
            val = ln[24:].strip()
            if lab in AGE_BAND_LABELS:
                sites.append((i, "kv", f"agedist.{lab}", val, None))
        elif block == "names":
            for m in OVERFLOW_RE.finditer(ln):
                sites.append((i, "overflow", "name_overflow", m.group(1), None))
    return lines, sites


def rewrite(text, fn):
    """Rebuild `text` with every count site replaced by fn(slot, token) -> str."""
    lines, sites = count_sites(text)
    out = list(lines)
    percat = collections.defaultdict(list)
    for i, kind, slot, tok, extra in sites:
        if kind == "kv":
            if out[i].startswith("entries in this store: "):
                out[i] = f"entries in this store: {fn(slot, tok)}"
            else:
                out[i] = out[i][:24] + fn(slot, tok)
        elif kind == "percat":
            percat[i].append((slot, tok, extra))
        elif kind == "overflow":
            out[i] = OVERFLOW_RE.sub(
                lambda m: "(+" + fn("name_overflow", m.group(1)) + " more)",
                out[i], count=1)
    for i, entries in percat.items():
        _cat, cols = entries[0][2]
        cat = lines[i].split()[0]
        orig = dict(zip(cols, lines[i].split()[1:]))
        rep = {slot.rsplit(".", 1)[1]: fn(slot, tok) for slot, tok, _ in entries}
        line = f"{cat:<24s}"
        for n, c in enumerate(cols):
            w = 8 if (n == 0 or c in AGE_COLS) else 9
            line += f"{rep.get(c, orig[c]):>{w}s}"
        out[i] = line
    return "\n".join(out)


def strip_counts(text):
    """Canonical form with every count masked -- used to assert nothing else moved."""
    return rewrite(text, lambda _slot, _tok: "\x00")


# --------------------------------------------------------------------------- #
def main():
    idx = jload(E1 / "indexes_v2.json")["indexes"]
    items = [i for i in jload(E1 / "build" / "items_final.json")
             if i["tier"] == "hard"
             and i.get("label", i["label_pre"]) in
             {"PRESENT", "ABSENT", "PRESENT-NEGATIVE"}]

    def ikey(it):
        b, p, v = it["backend"], it["persona"], it["variant"]
        return (f"{b}:{p}:SLOT:{it['question_id']}:TRUE" if v == "SLOT-ABLATED"
                else f"{b}:{p}:{v}:TRUE")

    keys = sorted({ikey(it) for it in items})
    assert all(k in idx for k in keys), "missing index for a hard-tier item"

    # ---------------------------------------------------------------- slots
    slots, values = set(), []
    for k in keys:
        for _i, _kind, slot, tok, _e in count_sites(idx[k])[1]:
            slots.add(slot)
            values.append(int(tok))
    slots = sorted(slots)

    rng = random.Random(SEED)
    mult = {s: rng.uniform(JITTER_LO, JITTER_HI) for s in slots}

    nonzero = sorted(v for v in values if v > 0)
    T = int(st.median(nonzero))

    def a1(slot, tok):
        return str(int(int(tok) * mult[slot] + 0.5))   # round-half-up; 0 stays 0

    def a2(_slot, tok):
        v = int(tok)
        return "0" if v == 0 else ("few" if v <= T else "many")

    def a3(_slot, _tok):
        return "-"

    arms = {"A1-counts-jittered": a1, "A2-counts-coarsened": a2, "A3-names-only": a3}
    built = {}

    def age_lines(t):
        """The RECENCY block plus every NEWEST/OLDEST column value."""
        keep, block = [], None
        for ln in t.split("\n"):
            if ln.startswith("RECENCY"):
                block = "rec"
            elif ln.startswith("AGE DISTRIBUTION") or ln.startswith("ATTRIBUTE"):
                block = None
            if block == "rec":
                keep.append(ln)
        cols, ages = None, []
        for ln in t.split("\n"):
            if ln.startswith("CATEGORY"):
                cols = ln.split()[1:]
            elif cols and ln and not ln.startswith(" ") and len(ln.split()) == len(cols) + 1:
                d = dict(zip(cols, ln.split()[1:]))
                ages.append(tuple(d.get(c) for c in AGE_COLS))
        return keep, ages

    for k in keys:
        base = idx[k]
        masked = strip_counts(base)
        base_sites = count_sites(base)[1]
        built[k] = {"TRUE": base}
        for name, fn in arms.items():
            t = rewrite(base, fn)
            # (i) nothing but counts moved
            assert strip_counts(t) == masked, f"{k}/{name}: non-count text changed"
            # (ii)/(iii) A1 and A2 preserve zero-ness exactly; (iv) A3 destroys it
            for _i, _kind, slot, tok, _e in base_sites:
                new = fn(slot, tok)
                if name.startswith("A3"):
                    assert new == "-", f"{k}/{name}: count survived"
                else:
                    assert (int(tok) == 0) == (new == "0"), \
                        f"{k}/{name}: zero-ness changed at {slot}"
            # (v) ages byte-identical
            assert age_lines(t) == age_lines(base), f"{k}/{name}: an age field moved"
            built[k][name] = t

    meta = {
        "no_api_calls": True,
        "seed": SEED,
        "jitter_range": [JITTER_LO, JITTER_HI],
        "n_index_keys": len(keys),
        "n_hard_tier_items": len(items),
        "n_count_slots": len(slots),
        "count_slots": slots,
        "jitter_multipliers": {s: round(mult[s], 6) for s in slots},
        "A2_threshold_T": T,
        "A2_threshold_rule": (
            "T = median of every NONZERO count appearing in the intact TRUE "
            "indexes of the hard tier; 0 -> \"0\", 1..T -> \"few\", >T -> \"many\". "
            "Label-blind by construction: computed from index text only, never "
            "from an outcome."),
        "A2_threshold_basis": {"n_nonzero_counts": len(nonzero),
                               "min": nonzero[0], "max": nonzero[-1],
                               "median": T},
        "count_value_census": {"n_count_sites_total": len(values),
                               "n_zero": sum(1 for v in values if v == 0)},
        "assertions": {
            "i_only_counts_changed": True,
            "ii_A1_preserves_zeroness": True,
            "iii_A2_preserves_zeroness": True,
            "iv_A3_has_no_count_digits": True,
            "v_recency_block_byte_identical": True,
        },
        "sha256_by_key": {k: {a: hashlib.sha256(t.encode()).hexdigest()[:16]
                              for a, t in v.items()} for k, v in built.items()},
    }
    jdump({"meta": meta, "indexes": built}, OUT)

    print("=" * 96)
    print(f"MECHANISM ARMS built for {len(keys)} index keys "
          f"({len(items)} hard-tier items)")
    print("=" * 96)
    print(f"  count slots: {len(slots)}   count sites: {len(values)} "
          f"({meta['count_value_census']['n_zero']} of them zero)")
    print(f"  A2 threshold T = {T}  (median of {len(nonzero)} nonzero counts, "
          f"range {nonzero[0]}..{nonzero[-1]})")
    print(f"  jitter multipliers: min {min(mult.values()):.4f} "
          f"max {max(mult.values()):.4f} over {len(slots)} slots")
    print("  assertions (i)-(v): PASS")
    k = "frbank:elena:FULL:TRUE"
    if k in built:
        for a in ("TRUE", "A1-counts-jittered", "A2-counts-coarsened", "A3-names-only"):
            print("\n" + "-" * 96)
            print(f"SAMPLE {k}  /  {a}")
            print("-" * 96)
            print("\n".join(built[k][a].split("\n")[:22]))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
