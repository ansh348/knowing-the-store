# -*- coding: utf-8 -*-
"""prompts_p1.py -- program R121 (the intent crossover): the P1 monitor prompt.

P1 is the frozen E1 prompt (prompts_e1.SYSTEM, file sha 337d37d3..., texts sha 35d9b968...) with exactly three edits,
all inside the negative-obligation passage, and nothing else:

  (1) the NEGATIVE OBLIGATION block (definition, Step 1, Step 2) replaced by the intent-conditional block of the
      registration brief, verbatim;
  (2) one worked example appended after the existing two, drawn from the same excluded construction category
      (AV8_numeric_preservation, the cultural-tour rate), verbatim from the brief;
  (3) the count word "Two worked examples." -> "Three worked examples." (the one edit outside the block the brief
      names; without it the sentence would be false).

The module asserts at import that SYSTEM_P1 equals P0 with those three substitutions applied, so "no other wording
changes" is machine-checked, and that the P0 digests are the ones E1 committed. USER_INDEXED is P0's, unchanged.
sha256 of the P1 system text is printed by `python prompts_p1.py` and recorded in the registration.
"""
from __future__ import annotations

import hashlib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import prompts_e1 as P0  # noqa: E402

E1_FILE_SHA = "337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84"
E1_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"
assert P0.file_sha256() == E1_FILE_SHA, "prompts_e1.py has changed since E1 froze it"
assert P0.texts_sha256() == E1_TEXTS_SHA, "prompts_e1 frozen texts have changed"

OLD_BLOCK = (
    "NEGATIVE OBLIGATION: content the store still holds whose correct influence on the answer is SUPPRESSION "
    "rather than use, because it has been superseded, retracted, or has expired. Judge this in two steps.\n\n"
    "  Step 1, nok_candidates_found: is there content on this topic in the store that has been superseded by a "
    "later value, retracted by the user, or has passed its date? true or false.\n\n"
    "  Step 2, nok: the probability, 0 to 100, that such content is present.\n\n"
)

NEW_BLOCK = (
    "NEGATIVE OBLIGATION: content the store still holds that must NOT be used to answer THIS question, because it "
    "has been superseded, retracted, or has expired. Whether it must be withheld depends on what the question asks. "
    "A question about the present, or about what is coming, must not use such content. A question about the past, "
    "or about how something has changed, may properly use it, and then it is not a negative obligation.\n\n"
    "  Step 1, nok_candidates_found: is there content on this topic that has been superseded, retracted, or has "
    "passed its date, and that must not be used for this question? true or false.\n\n"
    "  Step 2, nok: the probability, 0 to 100, that such content is present and must not be used for this "
    "question.\n\n"
)

OLD_COUNT = "Two worked examples.\n\n"
NEW_COUNT = "Three worked examples.\n\n"

EXAMPLE_2_END = (
    "The rate is still in the store and would mislead if surfaced as current. nok_candidates_found = true, "
    "nok = 85.\n\n"
)
EXAMPLE_3 = (
    "  Question: \"How has the user's rate per cultural tour changed?\"\n"
    "  The store holds an old rate and a newer one. The old rate is part of the answer to this question, so it is "
    "not a negative obligation. nok_candidates_found = false, nok = 10.\n\n"
)

for needle in (OLD_BLOCK, OLD_COUNT, EXAMPLE_2_END):
    assert P0.SYSTEM.count(needle) == 1, needle[:40]

SYSTEM_P1 = (P0.SYSTEM.replace(OLD_BLOCK, NEW_BLOCK)
             .replace(OLD_COUNT, NEW_COUNT)
             .replace(EXAMPLE_2_END, EXAMPLE_2_END + EXAMPLE_3))

# the same text, written out in full so the registration can quote it and a reader can diff it against P0
SYSTEM_P1_LITERAL = """\
You are assessing a personal long-term memory store that belongs to one user.

The store is a collection of short factual statements extracted from that user's \
past conversations with an assistant. Different memory systems record different \
amounts of structure alongside those statements, and some record almost none.

You will be shown a question the user has just asked. BEFORE any retrieval is \
performed, give two judgments about what the store contains.

FOK (feeling of knowing): the probability, 0 to 100, that the store contains \
content relevant to this question -- anything that should shape the answer.

NEGATIVE OBLIGATION: content the store still holds that must NOT be used to answer \
THIS question, because it has been superseded, retracted, or has expired. Whether \
it must be withheld depends on what the question asks. A question about the \
present, or about what is coming, must not use such content. A question about the \
past, or about how something has changed, may properly use it, and then it is not \
a negative obligation.

  Step 1, nok_candidates_found: is there content on this topic that has been \
superseded, retracted, or has passed its date, and that must not be used for this \
question? true or false.

  Step 2, nok: the probability, 0 to 100, that such content is present and must \
not be used for this question.

Three worked examples.

  Question: "How much did the user pay for their gaming PC?"
  The store holds one price, stated once, never revised. Nothing has been \
superseded or retracted and no date has passed. nok_candidates_found = false, \
nok = 5.

  Question: "How much does the user earn per cultural tour?"
  The store holds a per-tour rate, but the user later said they no longer run \
those tours. The rate is still in the store and would mislead if surfaced as \
current. nok_candidates_found = true, nok = 85.

  Question: "How has the user's rate per cultural tour changed?"
  The store holds an old rate and a newer one. The old rate is part of the answer \
to this question, so it is not a negative obligation. nok_candidates_found = false, \
nok = 10.

Note that FOK and the negative-obligation judgment are independent. A store can \
hold plenty of relevant content with nothing stale in it, and it can hold stale \
content on a topic it otherwise covers poorly.

Do not attempt to answer the question. Do not speculate about what the answer \
would be. Judge only what the store is likely to contain.

Respond with a single JSON object and nothing else:
{"fok": <0-100>, "nok_candidates_found": <true|false>, "nok": <0-100>, \
"would_search": <true|false>}\
"""

assert SYSTEM_P1 == SYSTEM_P1_LITERAL, "the literal and the constructed P1 differ"
USER_INDEXED = P0.USER_INDEXED          # unchanged


def p1_sha256() -> str:
    return hashlib.sha256(SYSTEM_P1.encode("utf-8")).hexdigest()


def p0_sha256() -> str:
    return hashlib.sha256(P0.SYSTEM.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    print("P0 system sha256:", p0_sha256())
    print("P1 system sha256:", p1_sha256())
    print("P1 chars:", len(SYSTEM_P1), " P0 chars:", len(P0.SYSTEM))
    try:
        import tiktoken
        enc = tiktoken.get_encoding("o200k_base")
        print("tokens (o200k_base): P0", len(enc.encode(P0.SYSTEM)), " P1", len(enc.encode(SYSTEM_P1)))
    except Exception as e:  # noqa: BLE001
        print("tiktoken unavailable:", e)
