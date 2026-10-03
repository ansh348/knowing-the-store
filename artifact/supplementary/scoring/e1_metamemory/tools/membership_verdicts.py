"""
membership_verdicts.py -- verdicts for the B4 membership spot-check.

All 40 sampled (entry, record) membership decisions were read individually against
the YAML record that nominated them. Criterion, fixed before reading:

    TRUE   the entry ASSERTS the value the YAML marks as superseded.
    FALSE  it does not.

The failure modes are the same four E0 named: (a) the entry states the transition
or the decision-against, so it carries the CURRENT value; (b) the entry is
explicitly past-tense marked; (c) it asserts an unchanged part of the record;
(d) pure token collision across unrelated facts.

Keyed on (backend, persona, entry_id[:12]) -- the composite key. FR-Bank ids are
lb_NNNNN (already short and persona-scoped); Mem0 and A-MEM ids are uuids, keyed by
their 12-char prefix, which membership.py resolves. Verified collision-free.
"""

from __future__ import annotations

T, F = "TRUE", "FALSE"

VERDICTS = {
    # ---------------------------------------------------------------- frbank
    ("frbank", "nadia", "lb_00180"): (T, "asserts the Noma stage application"),
    ("frbank", "amara", "lb_00099"): (T, "asserts considering the UCL LLM"),
    ("frbank", "aisha", "lb_00139"): (T, "asserts PureGym near Piccadilly"),
    ("frbank", "rosa", "lb_00105"): (T, "asserts yoga 3 mornings in Coral Gables"),
    ("frbank", "chenoa", "lb_00088"): (T, "asserts the 2015 Ford F-150"),
    ("frbank", "callum", "lb_00109"): (T, "asserts winger for Inverness Highland RFC"),
    ("frbank", "aroha", "lb_00310"): (F, "(a) 'decided NOT to pursue' is the decision-against"),
    ("frbank", "amara", "lb_00222"): (F, "(b)+(a) 'used to run ... but has given it up'"),
    ("frbank", "amara", "lb_00044"): (T, "asserts the 5K in Victoria Park"),
    ("frbank", "patrick", "lb_00092"): (T, "asserts the Wildwood shore house with Kevin"),
    ("frbank", "tom", "lb_00163"): (T, "asserts the barn conversion plan as live"),
    ("frbank", "lily", "lb_00128"): (T, "asserts the microplastics thesis"),
    ("frbank", "amara", "lb_00038"): (T, "asserts the 5K in Victoria Park"),
    ("frbank", "mirri", "lb_00004"): (T, "asserts the East Alligator patrol route"),

    # ------------------------------------------------------------------ mem0
    ("mem0", "valentina", "8350f0a3-6ab"):
        (T, "asserts the La Candelaria third-floor flat"),
    ("mem0", "amara", "f68f3eb6-200"):
        (F, "(a) 'considered ... but decided against it' is the decision-against"),
    ("mem0", "amara", "743dcfc5-b1c"):
        (T, "asserts the 5K in Victoria Park"),
    ("mem0", "yoli", "40a696c8-38c"):
        (T, "asserts the Drake Hotel Friday residency"),
    ("mem0", "aroha", "e66ac07d-d38"):
        (T, "asserts Thursday netball as wing defence"),
    ("mem0", "tom", "c5800a63-281"):
        (F, "(b)+(a) 'used to attend ... can no longer manage'"),
    ("mem0", "mirri", "170ae98c-d9a"):
        (F, "(b) 'had an idea to write' is past-marked"),
    ("mem0", "nadia", "abfd39c1-a2f"):
        (F, "(b) 'previously had a very small kitchen' is past-marked"),
    ("mem0", "yoli", "0417cc3f-f76"):
        (T, "asserts the Ableton-to-Logic switch, which is the superseded value here"),
    ("mem0", "samuel", "50987b52-1cf"):
        (T, "asserts YMCA lap swimming 3 mornings a week"),
    ("mem0", "fatima", "3da889b0-9d8"):
        (T, "asserts exclusively high-end residential design"),
    ("mem0", "ingrid", "71b65911-e06"):
        (T, "asserts the Kvaloeya ridge ski route"),
    ("mem0", "callum", "56dc6c6c-1b6"):
        (T, "asserts winger for Inverness Highland RFC"),

    # ------------------------------------------------------------------ amem
    ("amem", "rosa", "43df2dd4-b0c"):
        (T, "asserts yoga 3 mornings in Coral Gables"),
    ("amem", "kenji", "639ccc8c-b91"):
        (F, "(d) about Figma tooling; asserts nothing about Tanaka Foods as main client"),
    ("amem", "yoli", "f59ba28d-724"):
        (T, "asserts the Drake Hotel Friday residency"),
    ("amem", "lily", "72a8ca25-178"):
        (T, "asserts the microplastics thesis"),
    ("amem", "elena", "4838c96b-48c"):
        (T, "asserts doing keto, 15 pounds lost"),
    ("amem", "raj", "bcb71737-3df"):
        (T, "asserts Simran as a Year 3 teacher at Ladywood Primary"),
    ("amem", "amara", "59b7df8f-af5"):
        (T, "asserts the 5K in Victoria Park"),
    ("amem", "raj", "2a577010-1cf"):
        (T, "asserts Sky Sports and watching every Premier League match"),
    ("amem", "callum", "1e66ff4d-cf6"):
        (T, "asserts winger for Inverness Highland RFC"),
    ("amem", "pan", "7d6701fa-1b8"):
        (T, "asserts the Soi Rangnam cart location, same spot 4 years"),
    ("amem", "joonho", "610f85cd-914"):
        (F, "(d) about solitude after marriage; unrelated to the Baduk Club teaching"),
    ("amem", "ingrid", "5ea8c95a-9c2"):
        (F, "(b) 'The PREVIOUS focus was Arctic cod' is explicitly past-marked"),
    ("amem", "tom", "6d446b99-438"):
        (T, "asserts the Thursday pub quiz at The Fox with Gerald"),
}
