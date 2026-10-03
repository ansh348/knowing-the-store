"""graphiti_index.py -- R85. The frozen rules for reading Graphiti's self-description.

NO API CALLS. NO DUMP IS READ HERE. This file is the rule, written before any Graphiti
graph exists, and it is not revised after a dump is read. If a dump shows a field means
something other than what is written below, that is a Phase 1 finding and a D-R85-n entry,
never a rule edit.

Every schema fact below was verified against UNMODIFIED graphiti-core 0.28.1 installed from
the public package index, not against the locally modified copy. edges.py is byte identical
between the two, so the model is upstream's.

--------------------------------------------------------------------------------
RULE 1. LIFECYCLE DERIVATION from the edge's temporal fields
--------------------------------------------------------------------------------
EntityEdge carries exactly created_at, valid_at, invalid_at, expired_at, episodes,
attributes, name and fact (upstream edges.py:263-282).

  ACTIVE      invalid_at is null and expired_at is null.
  SUPERSEDED  invalid_at is set AND a later edge exists on the same
              (subject, predicate) slot.
  EXPIRED     expired_at is set, or the valid_at window has closed, with no
              successor edge on the slot.
  RETRACTED   INEXPRESSIBLE. Emits the marker.

The ADDENDUM's draft wording offered a second route to SUPERSEDED, "or Graphiti's own
contradiction pointer targets this edge". THAT CLAUSE IS STRUCK. Graphiti stores no such
pointer. resolve_edge_contradictions (upstream edge_operations.py:425) writes
edge.invalid_at = resolved_edge.valid_at and edge.expired_at = utc_now(), and then discards
the superseding edge's uuid. A grep of the whole upstream package for superseded_by,
invalidated_by and contradicted_by returns nothing. Graphiti records THAT an edge stopped
being true and WHEN, and never BY WHAT.

RETRACTED is inexpressible because Graphiti has exactly one mechanism. Edge.delete() is a
hard Cypher DELETE carrying no temporal semantics, so a deletion leaves no trace to read.
Retraction is therefore reported the way Mem0's and A-MEM's missing fields are reported,
with the marker. Retraction is NEVER folded into supersession silently: the paper already
reports FR-Bank conflating the two, and this row must be able to say the same or the
opposite.

Note for the census, not a rule: invalidation fires only when both edges carry a valid_at
and the earlier is STRICTLY less than the later (upstream edge_operations.py, the
edge_valid_at_utc < resolved_edge_valid_at_utc branch). A same-session event is therefore
unexpressible on this backend. None of the manifest's 109 supersession events is
same-session, so this limit does not reach the ground truth, and the 0.0 percent share
prints beside the recall.

--------------------------------------------------------------------------------
RULE 2. ATTRIBUTE NAMING
--------------------------------------------------------------------------------
An attribute name is edge.name (the relation type) joined with the TARGET NODE'S LABEL.

  NEVER the node name   -- it is a value ("Lurie Children's").
  NEVER the fact string -- it is a value, and it is the whole assertion.

Both would put content into a metadata-only index, and the leakage screen exists to catch
exactly that. The join uses "_" and never ":", so index_v2.scrub(), which truncates at the
first colon, is a no-op on these names and the type qualifier survives. This is asserted,
not assumed.

Naming granularity is itself a reported quantity. FR-Bank names an attribute path; Graphiti
names a relation type. If the stock extractor assigns every node the default label, the
qualifier is constant and the name reduces to the bare relation type. That is a finding
about how finely this backend can describe itself, and the spike report states it beside
FR-Bank's slot keys, because a self-description can only name what its naming rule
individuates.

--------------------------------------------------------------------------------
RULE 3. STOCK DEFAULTS
--------------------------------------------------------------------------------
The unmodified arm runs Graphiti's own defaults: no custom entity types, no custom edge
types, no custom prompts. Passing this paper's category ontology in as custom types would
be co-design of the second backend and would forfeit the independence the program exists to
establish. The consequence is stated in advance: the category axis prints as whatever the
default extractor yields, possibly a single default label, and that is the honest index for
a stock deployment.

Usage:  python r85_graphiti/graphiti_index.py        # prints the frozen rules, self-tests
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
from index_v2 import MARKER, render, scrub  # noqa: E402

ACTIVE, SUPERSEDED, EXPIRED, RETRACTED = "active", "superseded", "expired", "retracted"

# Availability is settled by the SCHEMA, which is read from source, never from a dump.
AVAIL_GRAPHITI = {
    "category": False,    # stock defaults declare no entity types
    "slot": True,         # relation types are carried on every edge
    "active": True,
    "superseded": True,
    "retracted": False,   # no mechanism exists
    "expired": True,
    "sup_events": True,
    "recency": True,
}

AVAIL_WHY_GRAPHITI = {
    "category": "stock defaults declare no entity types, so nodes carry the default "
                "label and the axis names no regions",
    "retracted": "no retraction mechanism exists; invalidation is the single mechanism "
                 "and a delete is a hard delete leaving no trace",
}


def attribute_name(edge_name, target_label):
    """RULE 2. Relation type joined with the target node's label. Never a value."""
    base = (edge_name or "").strip().lower().replace(" ", "_")
    lab = (target_label or "").strip().lower().replace(" ", "_")
    name = f"{base}_{lab}" if lab else base
    assert ":" not in name, "RULE 2: an attribute name must survive scrub() unchanged"
    assert scrub(name) == name, "RULE 2: scrub() must be a no-op on Graphiti names"
    return name


def derive_state(edge, has_later_edge_on_slot):
    """RULE 1. Edge temporal fields -> lifecycle state. RETRACTED is never returned."""
    invalid_at = edge.get("invalid_at")
    expired_at = edge.get("expired_at")
    if invalid_at is None and expired_at is None:
        return ACTIVE
    if invalid_at is not None and has_later_edge_on_slot:
        return SUPERSEDED
    return EXPIRED


def build_index(rows, events):
    """Emit in exactly index_v2's serialization, using index_v2's own renderer."""
    text, blocks, names = render(rows, events, AVAIL_GRAPHITI)
    lines = text.split("\n")
    for field in ("category", "retracted"):
        for i in blocks[field]:
            line = lines[i]
            assert MARKER in line or not any(c.isdigit() for c in line), (
                f"inexpressible field {field!r} emitted a digit on line {i}: {line!r}")
    return text, blocks, names


def _selftest():
    assert attribute_name("WORKS_AT", "Entity") == "works_at_entity"
    assert attribute_name("LIVES_IN", None) == "lives_in"
    assert derive_state({"invalid_at": None, "expired_at": None}, False) == ACTIVE
    assert derive_state({"invalid_at": "2025-01-01", "expired_at": "2025-01-02"}, True) == SUPERSEDED
    assert derive_state({"invalid_at": "2025-01-01", "expired_at": "2025-01-02"}, False) == EXPIRED
    assert derive_state({"invalid_at": None, "expired_at": "2025-01-02"}, False) == EXPIRED
    assert AVAIL_GRAPHITI["retracted"] is False
    print("self-test: rules 1 and 2 hold on synthetic edges; no dump was read")
    print(f"marker in force: {MARKER!r}")
    print("inexpressible on this backend: " +
          ", ".join(k for k, v in AVAIL_GRAPHITI.items() if not v))


if __name__ == "__main__":
    print(__doc__.split("Usage:")[0])
    _selftest()
