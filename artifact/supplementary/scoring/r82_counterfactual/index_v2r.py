"""index_v2r.py -- CF-2: the count-randomized index arm (ADDENDUM_CF2.md section 5, V2R).

NO API CALLS. Deterministic.

V2R is v2 with exactly two fields rewritten: the retracted-content count and the
expired-content count on the LIFECYCLE TOTALS block. The replacement values are the cell's own
(retracted, expired) pairs PERMUTED ACROSS THE STORE VERSIONS under a recorded seed-42
derangement, so every count value that appears in the cell appears the same number of times
and no version keeps its own pair. Outside those two lines V2R is asserted byte-identical to
the v2 index of the same store version (the RENDERER LOCK, as index_v3.py states it):
index_v2.render is CALLED upstream, never edited and never copied; this module only edits two
lines of its output and asserts the rest.

FIELD OFFSETS. The two lines are the ones index_v2.render emits as
    add(f"  {label:<22s}{count(f)}", f)   for f in ("retracted", "expired")
inside LIFECYCLE TOTALS: line index 6 ("  retracted") and 7 ("  expired") of every v2 index,
located here by their labels rather than by position and asserted to be exactly two.

DISCLOSED. The PER-CATEGORY BREAKDOWN keeps its RETRACT and EXPIRED columns unchanged: a reader
that sums a column recovers the true total. The registration names exactly two fields
(section 5), so that is what moves; the disclosure is ledgered under AUX-CF2-V2R-DEF.
"""
from __future__ import annotations

import numpy as np

LABELS = ("retracted", "expired")
SEED = 42


def _count_lines(v2_text):
    """-> {label: line index} for the two LIFECYCLE TOTALS lines; asserts exactly one each."""
    lines = v2_text.split("\n")
    try:
        start = lines.index("LIFECYCLE TOTALS")
    except ValueError as e:
        raise AssertionError("v2 index without a LIFECYCLE TOTALS block") from e
    found = {}
    for i in range(start + 1, min(start + 7, len(lines))):
        for lab in LABELS:
            if lines[i].startswith(f"  {lab:<22s}"):
                assert lab not in found, f"two {lab} lines"
                found[lab] = i
    assert set(found) == set(LABELS), f"count lines not found: {found}"
    return found


def counts_of(v2_text):
    """The (retracted, expired) totals a v2 index carries, as integers."""
    lines = v2_text.split("\n"); at = _count_lines(v2_text)
    return tuple(int(lines[at[lab]][24:].strip()) for lab in LABELS)


def render_v2r(v2_text, retracted, expired):
    """v2 with the two totals replaced; asserts the RENDERER LOCK before returning."""
    lines = v2_text.split("\n"); at = _count_lines(v2_text)
    out = list(lines)
    out[at["retracted"]] = f"  {'retracted':<22s}{retracted}"
    out[at["expired"]] = f"  {'expired':<22s}{expired}"
    text = "\n".join(out)
    assert_lock(v2_text, text)
    return text


def assert_lock(v2_text, v2r_text):
    """RENDERER LOCK: same line count; every differing line is one of the two count lines."""
    a, b = v2_text.split("\n"), v2r_text.split("\n")
    assert len(a) == len(b), "V2R changed the line count"
    at = _count_lines(v2_text)
    allowed = {at["retracted"], at["expired"]}
    diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    assert set(diff) <= allowed, f"V2R differs from v2 outside the two count fields at lines {sorted(set(diff) - allowed)[:5]}"
    for i in allowed:
        assert b[i][:24] == a[i][:24], "V2R changed a count label"


def derangement(values, seed=SEED):
    """A permutation p of range(len(values)) with values[p[i]] != values[i] for every i.

    Value-level, so a version never keeps its own (retracted, expired) pair even when many
    versions carry the same pair (the three versions of one persona's pairs mostly do).
    Construction: group the positions by value, shuffle within each group and shuffle the
    group order under the seed, lay the groups out in a line, and rotate by k drawn uniformly
    from [largest group, n - largest group]; a rotation in that band moves every position out
    of its own group, so no position receives its own value. Exists iff the largest group is
    at most half the cell. Returns (p, k). Every count value keeps its multiplicity."""
    from collections import defaultdict
    n = len(values); rng = np.random.default_rng(seed)
    groups = defaultdict(list)
    for i, v in enumerate(values):
        groups[v].append(i)
    top = max(len(g) for g in groups.values())
    assert top * 2 <= n, f"a value appears {top} times in {n}; no value-level derangement"
    keys = sorted(groups); rng.shuffle(keys)
    line = []
    for kx in keys:
        g = list(groups[kx]); rng.shuffle(g); line.extend(g)
    k = int(rng.integers(top, n - top + 1))
    p = [0] * n
    for j, i in enumerate(line):
        p[i] = line[(j + k) % n]          # position i receives the value at position p[i]
    assert all(values[p[i]] != values[i] for i in range(n))
    assert sorted(p) == list(range(n))
    return p, k
