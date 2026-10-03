"""
pn_verdicts.py -- verdicts for the full PRESENT-NEGATIVE verification (Amendment 1,
change 3). Detector proposes, YAML disposes.

All 166 (persona, question_id, entry_id) pairs behind the 69 admitted PN items were
read individually against the YAML record that nominated them, using the same
instrument as the committed 30-fire tau audit:

    TRUE   the entry asserts the value the YAML record marks as superseded /
           retracted / expired, so its correct influence on an answer to THIS
           question is SUPPRESSION.
    FALSE  it does not.

FALSE patterns. (a)-(d) carry over from the 30-fire audit; (e) and (f) are new,
and both are cases where the DETECTOR fired correctly but the YAML DISPOSES against
it -- which is exactly what this verification exists to catch.

  (a) the entry states the transition or its outcome, i.e. carries the CURRENT value
      e.g. chenoa lb_00233 "attempted to create ... but it was rejected by the
      tribal council" -- that is the retraction, not the retracted plan.
  (b) the entry is explicitly past-tense marked, so nothing needs suppressing
      e.g. ingrid lb_00219 "User's PREVIOUS primary research focus was Arctic cod";
      mirri lb_00252 "PLANNED to write"; tom lb_00216 "HAD grand plans".
  (c) the supersession changed only part of the record and the entry asserts the
      unchanged part
      e.g. aisha lb_00413 "lives in Manchester, sharing a 2-bedroom flat in Ancoats"
      -- the flat did not change, the flatmate did.
  (d) pure token collision across unrelated facts.
  (e) NEW -- the YAML record's own `status` is `upcoming`. The 14-day cutoff derived
      from the pinned t_now marks the event expired, but the authored ground truth
      says it has not happened, and in every such case the question's GOLD ANSWER IS
      THAT EVENT. Six records, 38 pairs: elena_q11, leila_q06, leila_q11, rosa_q05,
      samuel_q05, tom_q05, zara_q06. This is the 9-record YAML-status-vs-derived
      disagreement logged as D6, which the prereg did not carry forward into the
      expiry rule; per-item verification catches it.
  (f) NEW -- the question explicitly asks the store to surface PAST events, so the
      expired content is the gold answer and its correct influence is USE, not
      suppression. Three questions, 21 pairs: lily_q11 "Does Lily have past
      events?", pan_q13 "When does Pan's brother finish his conscription?" (gold:
      "He already finished"), valentina_q13 "Does Valentina have any past events or
      deadlines?".

Expiry sub-rule, applied uniformly: an expiry-nominated entry is TRUE iff the YAML
record's status is `expired` AND the question seeks current/upcoming state. Expiry
evidence is past-tense by nature, so pattern (b) does NOT apply to it -- the issue
is stale dated content being surfaced as current, not the entry's grammar.
"""

from __future__ import annotations


def _t(note):
    return ("TRUE", note)


def _f(note):
    return ("FALSE", note)


_ASSERTS = "asserts the superseded value"
_RETRACTED = "asserts the retracted plan as live"
_EXPIRED = "carries the expired dated event; question seeks current state"
_UPCOMING = "(e) YAML status is 'upcoming' and the gold answer IS this event"
_PASTQ = "(f) the question asks for past events; correct influence is use, not suppression"

VERDICTS = {}


def _add(persona, qid, entries, verdict):
    for e in entries:
        VERDICTS[(persona, qid, e)] = verdict


# ---------------------------------------------------------------- supersession
_add("aisha", "aisha_q01", ["lb_00004", "lb_00008"], _t("asserts audit at PwC Manchester"))
_add("aisha", "aisha_q02", ["lb_00131", "lb_00139"], _t("asserts PureGym near Piccadilly"))
_add("aisha", "aisha_q03", ["lb_00157", "lb_00161"], _t("asserts living with flatmate Zara"))
_add("aisha", "aisha_q03", ["lb_00413"], _f("(c) the Ancoats flat is unchanged; Zara moving out is the supersession"))

_add("elena", "elena_q01", ["lb_00008", "lb_00015"], _t("asserts working at Lurie Children's"))
_add("elena", "elena_q02", ["lb_00135"], _t("asserts doing keto"))

_add("fatima", "fatima_q02", ["lb_00088"], _t("asserts exclusively high-end residential design"))

_add("ingrid", "ingrid_q01", ["lb_00005", "lb_00007", "lb_00018", "lb_00019", "lb_00024",
                              "lb_00026"], _t("asserts Arctic cod as a live research focus"))
_add("ingrid", "ingrid_q01", ["lb_00219"], _f("(b) 'User's PREVIOUS primary research focus was' is past-marked"))

_add("jerome", "jerome_q02", ["lb_00001", "lb_00011"], _t("asserts driving for Southeastern Freight Lines"))
_add("jerome", "jerome_q03", ["lb_00005", "lb_00008", "lb_00012", "lb_00014"],
     _t("asserts driving the 2019 Freightliner Cascadia"))

_add("kenji", "kenji_q03", ["lb_00088", "lb_00090", "lb_00094"], _t("asserts the Shinsaibashi shared studio"))

_add("lily", "lily_q01", ["lb_00128"], _t("asserts the microplastics thesis"))

_add("mehmet", "mehmet_q02", ["lb_00079", "lb_00081"], _t("asserts Erkek brand pomade"))

_add("mirri", "mirri_q01", ["lb_00004", "lb_00006"], _t("asserts the East Alligator patrol route"))

_add("pan", "pan_q01", ["lb_00012", "lb_00017"], _t("asserts buying rice from Auntie Somjit at Khlong Toei"))

_add("raj", "raj_q02", ["lb_00113", "lb_00115", "lb_00119"], _t("asserts having Sky Sports"))
_add("raj", "raj_q03", ["lb_00033"], _t("asserts Simran as a Year 3 teacher, pre-promotion"))

_add("samuel", "samuel_q02", ["lb_00086", "lb_00090", "lb_00093", "lb_00096", "lb_00099"],
     _t("asserts swimming laps at the YMCA"))

_add("valentina", "valentina_q03", ["lb_00087", "lb_00101"], _t("asserts smoking half a pack a day"))

_add("zara", "zara_q02", ["lb_00079", "lb_00085", "lb_00090", "lb_00096"],
     _t("asserts reformer pilates on Al Reem Island"))

# ------------------------------------------------------------------ retraction
_add("bruna", "bruna_q06", ["lb_00174", "lb_00185"], _t(_RETRACTED + " (dry needling course)"))

_add("chenoa", "chenoa_q04", ["lb_00233"],
     _f("(a) 'attempted ... but it was rejected by the tribal council' is the retraction itself"))

_add("fatima", "fatima_q06", ["lb_00176", "lb_00180", "lb_00182", "lb_00183", "lb_00186",
                              "lb_00189"], _t(_RETRACTED + " (Oud & Geometry fragrance line)"))
_add("fatima", "fatima_q06", ["lb_00263"], _f("(a) 'decided not to launch' is the cancellation"))

_add("ingrid", "ingrid_q04", ["lb_00076", "lb_00078", "lb_00085", "lb_00086"],
     _t(_RETRACTED + " (Woods Hole sabbatical)"))

_add("lily", "lily_q06", ["lb_00166"], _t(_RETRACTED + " (applying for the UBC exchange)"))
_add("lily", "lily_q06", ["lb_00163"],
     _f("(c) interest in the UBC marine ecology programme is not the exchange plan"))

_add("mirri", "mirri_q04", ["lb_00155", "lb_00157", "lb_00159", "lb_00160", "lb_00162",
                            "lb_00164"], _t(_RETRACTED + " (bilingual children's book)"))
_add("mirri", "mirri_q04", ["lb_00252"], _f("(b) 'PLANNED to write' is past-marked"))

_add("rosa", "rosa_q06", ["lb_00231", "lb_00233", "lb_00236", "lb_00240", "lb_00242"],
     _t(_RETRACTED + " (two-week Peru trip)"))

_add("tom", "tom_q06", ["lb_00143", "lb_00148", "lb_00151", "lb_00160", "lb_00163"],
     _t(_RETRACTED + " (barn conversion)"))
_add("tom", "tom_q06", ["lb_00216"], _f("(b) 'HAD grand plans' is past-marked"))

_add("valentina", "valentina_q04", ["lb_00115", "lb_00117", "lb_00120"],
     _t(_RETRACTED + " (book on Colombian journalists)"))

# ---------------------------------------------------------------------- expiry
_add("bruna", "bruna_q11", ["lb_00103", "lb_00104", "lb_00108", "lb_00109", "lb_00119"],
     _t(_EXPIRED + " (Dubai Marathon, 2025-01-10)"))
_add("david", "david_q06", ["lb_00171", "lb_00172", "lb_00173", "lb_00175"],
     _t(_EXPIRED + " (AP Euro exam, 2025-05-08)"))
_add("david", "david_q11", ["lb_00148", "lb_00150"],
     _t(_EXPIRED + " (parent-teacher conferences, 2025-03-12)"))
_add("elena", "elena_q05", ["lb_00213", "lb_00214", "lb_00219"],
     _t(_EXPIRED + " (NCLEX recertification, 2025-03-20)"))
_add("elena", "elena_q10", ["lb_00187"],
     _t(_EXPIRED + " (lease renewal deadline, 2025-02-28)"))
_add("zara", "zara_q13", ["lb_00114"],
     _t(_EXPIRED + " ('is preparing for' an exam held 2025-02-08)"))

# (e) YAML status is 'upcoming' -- the record is not a negative obligation
_add("elena", "elena_q11", ["lb_00503", "lb_00504", "lb_00505", "lb_00506", "lb_00507",
                            "lb_00508", "lb_00509", "lb_00513", "lb_00515"], _f(_UPCOMING))
_add("leila", "leila_q06", ["lb_00414", "lb_00416", "lb_00419", "lb_00424", "lb_00426"], _f(_UPCOMING))
_add("leila", "leila_q11", ["lb_00414", "lb_00416", "lb_00419", "lb_00424", "lb_00426"], _f(_UPCOMING))
_add("rosa", "rosa_q05", ["lb_00417", "lb_00421", "lb_00422", "lb_00423", "lb_00425",
                          "lb_00426", "lb_00427", "lb_00428", "lb_00429", "lb_00430",
                          "lb_00431", "lb_00434", "lb_00435", "lb_00438", "lb_00439"], _f(_UPCOMING))
_add("samuel", "samuel_q05", ["lb_00476"], _f(_UPCOMING + "; the entry is also mis-dated 2025 vs 2026"))
_add("tom", "tom_q05", ["lb_00371"], _f(_UPCOMING))
_add("zara", "zara_q06", ["lb_00353", "lb_00354", "lb_00355", "lb_00357", "lb_00359",
                          "lb_00361", "lb_00362"], _f(_UPCOMING))

# (f) the question asks the store to surface PAST events
_add("lily", "lily_q11", ["lb_00145", "lb_00146", "lb_00147", "lb_00148", "lb_00149",
                          "lb_00151", "lb_00152", "lb_00153", "lb_00154", "lb_00155",
                          "lb_00156"], _f(_PASTQ))
_add("pan", "pan_q13", ["lb_00198", "lb_00199", "lb_00202", "lb_00206", "lb_00209",
                        "lb_00212", "lb_00214"], _f(_PASTQ))
_add("valentina", "valentina_q13", ["lb_00167", "lb_00168", "lb_00172"], _f(_PASTQ))
