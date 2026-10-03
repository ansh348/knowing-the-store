"""index_v3.py -- R82-CF: the index arm that names all three non-active states.

NO API CALLS. Deterministic.

v2 names attribute paths in exactly one state-conditioned place, the flat section
ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT. Retracted and expired content reaches the
index only as counts. v3 adds the two missing sections so the question of whether naming
recovers the counted states becomes measurable.

RENDERER LOCK. index_v2.render is CALLED, never edited and never copied. v3 is exactly
v2 plus two appended sections, so the v2 prefix of every v3 index is byte-identical to the
v2 index for the same store version, and that identity is asserted rather than assumed.
This follows e3_metamemory/tools/build_indexes.py, which states the same rule.

The two appended sections reuse v2's own name-block grammar verbatim: alphabetical,
deduplicated, capped at SLOT_CAP with a "(+N more)" overflow, wrapped at WRAP with the same
indents. Value scrubbing is v2's scrub(), already applied upstream in view().
"""
from __future__ import annotations

import pathlib
import sys
import textwrap

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))

from index_v2 import MARKER, SLOT_CAP, WRAP, render  # noqa: E402

HDR_RETRACTED = "ATTRIBUTE NAMES CARRYING RETRACTED CONTENT  (value-scrubbed)"
HDR_EXPIRED = "ATTRIBUTE NAMES CARRYING EXPIRED CONTENT  (value-scrubbed)"


def _name_block(names, header):
    """v2's name_block for the flat, single-bucket case (indent_cat False)."""
    out = [header]
    names = sorted(set(names))
    if not names:
        out.append("  (none)")
        return out
    shown, extra = names[:SLOT_CAP], max(0, len(names) - SLOT_CAP)
    body = ", ".join(shown) + (f", (+{extra} more)" if extra else "")
    out.extend(textwrap.wrap(body, width=WRAP, initial_indent="  ",
                            subsequent_indent="    "))
    return out


def render_v3(rows, events, avail):
    """-> (text_v3, text_v2). text_v3 starts with text_v2 byte for byte."""
    v2, blocks, names = render(rows, events, avail)
    lines = [v2, ""]
    for field, hdr in (("retracted", HDR_RETRACTED), ("expired", HDR_EXPIRED)):
        if not (avail["slot"] and avail[field]):
            lines.extend([hdr, f"  {MARKER}"])
        else:
            lines.extend(_name_block([r["slot"] for r in rows if r[field] and r["slot"]],
                                     hdr))
        lines.append("")
    text = "\n".join(lines).rstrip("\n")
    assert text.startswith(v2), "v3 must extend v2 byte-identically"
    return text, v2


def named_sections(text):
    """Parse the three state-conditioned name sections out of a v2 or v3 index.

    Returns {"superseded": [...], "retracted": [...], "expired": [...]}, each a list of
    attribute names, empty where the section is absent or carries the marker. Used by the
    build's assertions, so it reads the emitted text rather than any internal state.
    """
    heads = {
        "superseded": "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT",
        "retracted": "ATTRIBUTE NAMES CARRYING RETRACTED CONTENT",
        "expired": "ATTRIBUTE NAMES CARRYING EXPIRED CONTENT",
    }
    out = {k: [] for k in heads}
    lines = text.split("\n")
    cur = None
    for ln in lines:
        hit = next((k for k, h in heads.items() if ln.startswith(h)), None)
        if hit:
            cur = hit
            continue
        if cur is None:
            continue
        if not ln.strip() or ln.strip() == "(none)":
            if not ln.strip():
                cur = None
            continue
        if ln[:1] not in (" ",) or MARKER in ln or ln.strip().startswith("("):
            if MARKER in ln:
                cur = None
                continue
            if ln[:1] not in (" ",):
                cur = None
                continue
        for part in ln.split(","):
            p = part.strip()
            if p and not p.startswith("(+") and p != "(none)":
                out[cur].append(p)
    return {k: sorted(set(v)) for k, v in out.items()}
