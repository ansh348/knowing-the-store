# -*- coding: utf-8 -*-
"""cue_list.py -- program R121 (the intent crossover): the keyword-intent lookup's cue list. NO MODEL CALL.

The keyword-intent lookup is the recorded name lookup (score_cf.matcher: max cosine of the question against the
summary's named attributes) with the score set to ZERO when the question matches any cue below. The list is fixed
here, before any crossed question exists, and is proposed from the instruction texts only:

  PAST_FROZEN   the twelve PAST markers of e1_metamemory/tools/intent.py (the paper's own text rule for the PAST
                intent, Rule 2.1), imported and not retyped;
  CHANGE_CUES   the wordings the CHANGE time-sense instruction of cross_questions.SYSTEM offers as examples
                ("how has my ... changed over time", "what did my ... use to be", "before", "previously", "earlier",
                and "change or history");
  PAST_CUES     the wordings the PAST time-sense instruction offers ("What did I have planned for ...?", "When was
                my ...?", "What was my ...?", "already happened").

VERSION 2 (deviation D-IX-1, 2026-09-19): re-derived from the amended instruction BEFORE any version-2 question was
generated, as the version-1 list was from its instruction. Version 1 (sha256 bf063a8e...) offered "what happened at",
"how did ... go", "how did ... turn out", "what was ... like" and "after"; the amended PAST paragraph offers none of
those, so the cues `happened?` (kept: "already happened" remains in the text), `how did`, `how was`, `turn(ed) out`,
`after` and `went` leave, and `when was`, `(have|had) planned` enter. The CHANGE cues are unchanged (the paragraph's
examples are the same words with "my" added). Nothing here was tuned on any generated question. The crossed-question
renderer's automatic gate does not use this list (cross_questions.py), so the lookup's coverage of the crossed questions
is measured, not built in.

`python cue_list.py` prints the list with its sha256 and, as a disclosure only, the cues that fire on the 148
recorded original questions of the counterfactual set (cells 1 and 2 of every pair): those are the keyword lookup's
false zeros on the recorded cells, reported and not edited away.
"""
from __future__ import annotations

import hashlib
import io
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
from intent import PAST_MARKERS, norm  # noqa: E402

VERSION = 2
PAST_FROZEN = list(PAST_MARKERS)
assert len(PAST_FROZEN) == 12, len(PAST_FROZEN)

CHANGE_CUES = [
    r"\bhow (has|have)\b",
    r"\bchanged?\b",
    r"\bchanges\b",
    r"\bchanging\b",
    r"\bhistory\b",
    r"\buse(d)? to\b",
    r"\bbefore\b",
    r"\bpreviously\b",
    r"\bover time\b",
    r"\bearlier\b",
]

PAST_CUES = [
    r"\bhappened?\b",
    r"\bwhen was\b",
    r"\bwhat was\b",
    r"\b(have|had) planned\b",
]

CUES = PAST_FROZEN + CHANGE_CUES + PAST_CUES
CUE_RE = [re.compile(p, re.I) for p in CUES]

# version 1, superseded by D-IX-1 (for the record; its sha256 must reproduce)
PAST_CUES_V1 = [r"\bhappened?\b", r"\bhow did\b", r"\bwhat did\b", r"\bwhat was\b", r"\bhow was\b", r"\bturn(ed)? out\b", r"\bafter\b", r"\bwent\b"]
CUES_V1 = PAST_FROZEN + CHANGE_CUES + PAST_CUES_V1
V1_SHA = "bf063a8eb9830a78b9a0d061714aa1736e287fe63a8d6805336396735cf39d4f"
assert hashlib.sha256("\n".join(CUES_V1).encode("utf-8")).hexdigest() == V1_SHA, "the version-1 cue list does not reproduce"


def cues_fired(question):
    t = norm(question)
    return [r.pattern for r in CUE_RE if r.search(t)]


def matches(question):
    return bool(cues_fired(question))


def cue_sha256():
    return hashlib.sha256("\n".join(CUES).encode("utf-8")).hexdigest()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"version {VERSION}: {len(CUES)} cues (PAST_FROZEN {len(PAST_FROZEN)}, CHANGE {len(CHANGE_CUES)}, PAST {len(PAST_CUES)}); sha256 {cue_sha256()}   (v1 {V1_SHA[:16]}... reproduces)")
    for p in CUES:
        print("  ", p)
    cell = json.load(io.open(ROOT / "r82_counterfactual" / "cf2" / "cf_cell.json", encoding="utf-8"))["items"]
    qs = sorted({(it["pair_id"], it["state"], it["intent"], it["question"]) for it in cell})
    hits = [(pid, st, intent, q, cues_fired(q)) for pid, st, intent, q in qs if cues_fired(q)]
    print(f"\nDisclosure: cues firing on the {len(qs)} recorded original questions: {len(hits)}")
    for pid, st, intent, q, f in hits:
        print(f"  {st[:3]} {intent:13s} {pid:50s} {f}  {q}")
