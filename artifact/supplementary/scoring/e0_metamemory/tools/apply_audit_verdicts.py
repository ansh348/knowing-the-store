"""
apply_audit_verdicts.py -- write the hand-audit verdicts into tau_audit_sample.json.

The 30 sampled detector fires were read one by one against the YAML record that
produced them. The criterion, fixed before reading:

    TRUE  the entry text ASSERTS the yaml_superseded_value, so its correct
          influence on an answer would be suppression.
    FALSE it does not -- including incidental token overlap, entries that are
          already tense-marked as past, entries that assert the CURRENT value,
          and entries that assert a part of the record which was not the thing
          superseded.

This is a deterministic reading recorded as a committed table, not an LLM judge
inside the labelling pipeline: no model call happens here or downstream, and the
table can be checked line by line against the persona YAMLs.

Recurring FALSE patterns worth naming, because they are what the cross-guard
(CROSS_GUARD = 0.34) fails to catch:
  (a) the entry states the transition itself ("shifted from cod to kelp"), which
      is the current value, not the superseded one;
  (b) the entry is explicitly past-tense ("previously owned", "worked with X for
      4 years"), so nothing needs suppressing;
  (c) the supersession changed only PART of the record (which gym, which
      roommate) and the entry asserts the unchanged part ("lives in Ancoats",
      "climbs twice a week");
  (d) pure token collision across unrelated facts ("family time is sacred" vs
      "sacred family culinary heritage").
"""

from __future__ import annotations

from e0_common import E0, jdump, jload

AUDIT_PATH = E0 / "tau_audit_sample.json"

# entry_id -> (verdict, note).  Keyed by (persona, entry_id) to avoid the
# per-persona lb_ id collision documented in FINDINGS_E0_STEP0.md hazard 1.
VERDICTS = {
    ("aisha", "lb_00161"):     ("TRUE",  "asserts living with Zara; supersession is Zara moving out"),
    ("jerome", "lb_00005"):    ("TRUE",  "asserts driving the 2019 Cascadia verbatim"),
    ("raj", "lb_00113"):       ("TRUE",  "asserts watching PL on Sky Sports; Sky was cancelled"),
    ("ingrid", "lb_00007"):    ("TRUE",  "asserts Arctic cod as the research programme"),
    ("nadia", "lb_00084"):     ("TRUE",  "asserts living in the Plateau apartment"),
    ("bruna", "lb_00129"):     ("TRUE",  "asserts the JLT 1-bedroom"),
    ("callum", "lb_00010"):    ("TRUE",  "asserts NHS Highland employment"),
    ("tom", "lb_00302"):       ("FALSE", "(b) 'previously owned' is already past-marked; nothing to suppress"),
    ("alex", "lb_00028"):      ("TRUE",  "asserts Kotlin as the backend language, in present tense"),
    ("aisha", "lb_00155"):     ("FALSE", "(c) 'lives in Ancoats' is unchanged; the roommate was superseded"),
    ("valentina", "lb_00098"): ("TRUE",  "asserts current half-a-pack smoking; she has since quit"),
    ("jake", "lb_00020"):      ("TRUE",  "asserts Juul/mango-pod vaping; he quit"),
    ("kofi", "lb_00414"):      ("FALSE", "(a) states the return to school, i.e. carries the current value"),
    ("callum", "lb_00145"):    ("FALSE", "(d) rural TB testing; does not assert NHS employment"),
    ("callum", "lb_00438"):    ("FALSE", "(a) asserts the CURRENT private practice"),
    ("nadia", "lb_00134"):     ("TRUE",  "asserts the superseded 'never open a restaurant' stance"),
    ("saga", "lb_00311"):      ("FALSE", "(a) recommendation systems is the current team, not podcast analytics"),
    ("alex", "lb_00197"):      ("FALSE", "(b) 'worked with Kotlin for 4 years' is past-marked background"),
    ("fatima", "lb_00269"):    ("FALSE", "(a) asserts the cancellation, i.e. the retraction itself"),
    ("ingrid", "lb_00237"):    ("FALSE", "(a) asserts the shift to kelp, i.e. the current value"),
    ("dariush", "lb_00453"):   ("FALSE", "(a) 'joined a new golf club' is the current value"),
    ("fatima", "lb_00446"):    ("FALSE", "(a) asserts the residential->commercial transition"),
    ("raj", "lb_00487"):       ("FALSE", "(d) collision on 'sacred'/'family'; unrelated fact"),
    ("saga", "lb_00245"):      ("FALSE", "(c) 'climbs twice a week' unchanged; the gym was superseded"),
    ("samuel", "lb_00206"):    ("FALSE", "(d) Ghana mission vs YMCA swimming; unrelated fact"),
    ("kofi", "lb_00408"):      ("FALSE", "(c) asserts only that Kwabena exists, not the dropout"),
    ("valentina", "lb_00067"): ("FALSE", "(c) asserts employment, not the 'would never leave' stance"),
    ("valentina", "lb_00071"): ("FALSE", "(c) asserts tenure, not the stance that was contradicted"),
    ("valentina", "lb_00072"): ("FALSE", "(c) values the job; compatible with quietly considering a move"),
    ("mirri", "lb_00229"):     ("TRUE",  "asserts patrolling East Alligator; she was reassigned"),
}


def main():
    a = jload(AUDIT_PATH)
    n = 0
    for r in a["sample"]:
        key = (r["persona"], r["entry_id"])
        if key not in VERDICTS:
            raise SystemExit(f"no verdict recorded for {key}")
        r["verdict"], r["audit_note"] = VERDICTS[key]
        n += 1
    a["meta"]["audited_by"] = (
        "read individually against the persona YAML record; deterministic reading "
        "recorded as a committed table, no model call in the labelling pipeline"
    )
    a["meta"]["false_positive_patterns"] = {
        "a": "entry states the transition itself, i.e. carries the current value",
        "b": "entry is explicitly past-tense, so nothing needs suppressing",
        "c": "supersession changed only part of the record; entry asserts the unchanged part",
        "d": "pure token collision across unrelated facts",
    }
    jdump(a, AUDIT_PATH)
    print(f"wrote {n} verdicts to {AUDIT_PATH}")
    tp = sum(1 for r in a["sample"] if r["verdict"] == "TRUE")
    print(f"  TRUE {tp} / {n}  ({tp/n:.0%} raw precision over the whole sample)")


if __name__ == "__main__":
    main()
