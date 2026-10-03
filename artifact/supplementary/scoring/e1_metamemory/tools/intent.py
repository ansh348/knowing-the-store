"""
intent.py -- E1 Phase 0 item 1: intent typing.

NO API CALLS. Implements INTENT_RULES.md exactly. Typing uses question text and
attack-vector structure only -- never the gold answer, never any label.

Usage:
    python e1_metamemory/tools/intent.py           # type all, write intents.json + spotcheck
"""

from __future__ import annotations

import collections
import io
import json
import random
import re
import unicodedata
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
QUESTIONS = PROJECT_ROOT / "LifeMemEval" / "lifemembench_questions.json"
SEED = 42

CURRENT, UPCOMING, PAST, CHANGE = "CURRENT-STATE", "UPCOMING", "PAST-EVENT", "CHANGE-AWARE"
OUT_OF_SCOPE = "OUT-OF-SCOPE"
UNRESOLVED = "UNRESOLVED"

# Rule 1 -- structural default from attack vector
AV_INTENT = {
    "AV1_superseded_preference": CURRENT,
    "AV4_multi_version_fact": CURRENT,
    "AV3_stable_identity": CURRENT,
    "AV7_selective_forgetting": CURRENT,
    "AV6_cross_session_contradiction": CHANGE,
    "AV9_soft_supersession": CHANGE,
    "AV2_expired_logistics": None,          # Rule 2
    "AV5_broad_query": OUT_OF_SCOPE,
    "AV8_numeric_preservation": OUT_OF_SCOPE,
}

# Rule 2 -- AV2 text split
PAST_MARKERS = [
    r"\bpast\b", r"\balready\b", r"\bwhen did\b", r"\bhow long (has|have|did)\b",
    r"\bhow much\b[^?]*\bdid\b", r"\bwhat did\b", r"\bever been\b", r"\bused to\b",
    r"\bwhen does\b[^?]*\bfinish\b", r"\bfinished\b",
    r"\bwas\b(?=[^?]*\b(exam|event|deadline|ceremony|trip|meeting|conference)\b)",
    # Revision 3 (pre-freeze): "expired" is an unambiguous past marker and was simply
    # absent. Six AV2 questions of the form "Does X have any EXPIRED events?" fell to
    # UNRESOLVED for want of it.
    r"\bexpired\b",
]
# Revision 2 (pre-freeze). Revision 1 also listed the topic patterns
#   \bdeadlines?\b and \bany\b[^?]*\b(events?|appointments?|...)\b
# as FUTURE markers. Those are TOPIC words, not TENSE words: "Does Tom have any
# PAST events?" fired both classes and all 14 such questions fell to UNRESOLVED
# when every one of them is plainly PAST-EVENT. Only strictly temporal markers
# decide the split now; topic words decide nothing. Fixed before the rule table
# was committed, using question text only.
FUTURE_MARKERS = [
    r"\bupcoming\b", r"\bcoming up\b", r"\bcoming\b", r"\bscheduled\b",
    r"\bneed to prepare\b", r"\bplanning\b", r"\bplans? to\b", r"\bgoing to\b",
    r"\bwill\b", r"\bnext\b", r"\bfuture\b",
    # Revision 3 (pre-freeze): broaden "need to prepare" to "need to", and add
    # "registered for". Both are forward-looking in every AV2 occurrence.
    r"\bneed to\b", r"\bregistered for\b",
]
PAST_RE = [re.compile(p, re.I) for p in PAST_MARKERS]
FUT_RE = [re.compile(p, re.I) for p in FUTURE_MARKERS]


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    return "".join(c for c in s if not unicodedata.combining(c))


def fired(res, text):
    return [r.pattern for r in res if r.search(text)]


def type_question(q):
    """-> (intent, rule, evidence). Question text + AV only."""
    av = q["attack_vector"]
    default = AV_INTENT.get(av, UNRESOLVED)
    if default == OUT_OF_SCOPE:
        return OUT_OF_SCOPE, "Rule 1: vector out of scope", []
    if default is not None:
        return default, f"Rule 1: {av} -> {default}", []
    t = norm(q["question"])
    p, f = fired(PAST_RE, t), fired(FUT_RE, t)
    if p and not f:
        return PAST, "Rule 2.1: past markers only", p
    if f and not p:
        return UPCOMING, "Rule 2.2: future markers only", f
    if p and f:
        return UNRESOLVED, "Rule 2.3: both marker classes fired", p + f
    return UNRESOLVED, "Rule 2.3: no marker fired", []


def main():
    qs = json.load(io.open(QUESTIONS, encoding="utf-8"))
    out = []
    for q in qs:
        intent, rule, ev = type_question(q)
        out.append({"id": q["id"], "persona": q["persona"],
                    "attack_vector": q["attack_vector"], "question": q["question"],
                    "intent": intent, "rule": rule, "markers": ev})
    E1.mkdir(parents=True, exist_ok=True)
    with io.open(E1 / "intents.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")

    c = collections.Counter(r["intent"] for r in out)
    print("=" * 78)
    print("INTENT TYPING — all 516 questions")
    print("=" * 78)
    for k in (CURRENT, UPCOMING, PAST, CHANGE, OUT_OF_SCOPE, UNRESOLVED):
        print(f"  {k:14s} {c[k]:4d}")
    inscope = sum(c[k] for k in (CURRENT, UPCOMING, PAST, CHANGE))
    print(f"  {'in scope':14s} {inscope:4d}   (negative obligation possible on "
          f"{c[CURRENT]+c[UPCOMING]} of them; CHANGE-AWARE and PAST-EVENT are exempt)")

    print("\n  by attack vector:")
    per = collections.defaultdict(collections.Counter)
    for r in out:
        per[r["attack_vector"]][r["intent"]] += 1
    for av in sorted(per):
        print(f"    {av:34s} " + "  ".join(f"{k}:{v}" for k, v in sorted(per[av].items())))

    av2 = [r for r in out if r["attack_vector"] == "AV2_expired_logistics"]
    unres = [r for r in av2 if r["intent"] == UNRESOLVED]
    print(f"\n  AV2 split: UPCOMING {sum(1 for r in av2 if r['intent']==UPCOMING)}, "
          f"PAST-EVENT {sum(1 for r in av2 if r['intent']==PAST)}, "
          f"UNRESOLVED {len(unres)}")
    if unres:
        print("  AV2 intent-ambiguous questions (excluded, never imputed):")
        for r in unres:
            print(f"    {r['id']:16s} {r['rule']:38s} {r['question'][:64]}")

    # ---- 30-item stratified spot-check workbook, seed 42
    rng = random.Random(SEED)
    strata = collections.defaultdict(list)
    for r in out:
        strata[r["intent"]].append(r)
    sample = []
    order = [CURRENT, UPCOMING, PAST, CHANGE, OUT_OF_SCOPE, UNRESOLVED]
    # Quotas sum to 30 over the strata that are non-empty after Revision 3
    # (UNRESOLVED is empty; any residual is added to the sample in full).
    quota = {CURRENT: 10, UPCOMING: 7, PAST: 5, CHANGE: 6, OUT_OF_SCOPE: 2, UNRESOLVED: 99}
    for k in order:
        pool = sorted(strata.get(k, []), key=lambda r: r["id"])
        sample += rng.sample(pool, min(quota[k], len(pool)))
    L = ["# INTENT TYPING — 30-item spot-check workbook", "",
         "Stratified sample, seed 42. Rules in `INTENT_RULES.md`. Typing used question text and "
         "attack-vector structure only — no gold answer, no label, no store contents.",
         "Non-blocking: E1 Phase 0 does not wait on this review.", "",
         "Mark the `agree?` column. A disagreement is a rule-table bug, not an item bug — "
         "the rule table is what would change.", "",
         "| # | id | attack vector | question | assigned intent | rule fired | agree? |",
         "|---|---|---|---|---|---|---|"]
    for n, r in enumerate(sample, 1):
        qt = r["question"].replace("|", "\\|")
        L.append(f"| {n} | `{r['id']}` | {r['attack_vector'].split('_')[0]} | {qt} | "
                 f"**{r['intent']}** | {r['rule']} |  |")
    L += ["", f"Sampled {len(sample)} of {len(out)} questions across "
              f"{len([k for k in order if strata.get(k)])} strata."]
    with io.open(E1 / "intent_spotcheck.md", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"\nwrote {E1/'intents.json'} and {E1/'intent_spotcheck.md'} ({len(sample)} items)")


if __name__ == "__main__":
    main()
