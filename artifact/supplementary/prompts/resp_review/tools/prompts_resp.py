"""prompts_resp.py -- the prompt variants of ADDENDUM_RESP.md sections L2 and L3 (frozen 17e6328).

NEW, HASHED, NOT THE FROZEN LINEAGE. prompts_e1.py is imported and never edited; its two digests are
asserted by verify_resp.py. Every variant is a minimal extension of the frozen texts, constructed
here FROM prompts_e1.SYSTEM / USER_INDEXED by exactly the edits the registration lists, so that the
diff is a property of this file rather than a claim about it. The sha256 of each string is ledgered
at build (AUX-RESP-L2-PROMPTS, AUX-RESP-L3-PROMPT) and asserted by verify_resp.py check D.

Decoding parameters are prompts_e1's (gpt-4.1-mini, temperature 0, seed 42, max_tokens 200) and are
not restated here.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
import prompts_e1 as P  # noqa: E402

# --------------------------------------------------------------------------- #
# L2: SYSTEM_RETRIEVED = prompts_e1.SYSTEM with exactly one passage replaced.
# --------------------------------------------------------------------------- #
FROZEN_PASSAGE = ("You will be shown a question the user has just asked. BEFORE any retrieval is "
                  "performed, give two judgments about what the store contains.")
VARIANT_PASSAGE = ("You will be shown a question the user has just asked, together with the five entries "
                   "a similarity retriever returned for it from the store, each with the lifecycle "
                   "metadata the store records. Give two judgments about what the store as a whole contains.")
assert P.SYSTEM.count(FROZEN_PASSAGE) == 1
SYSTEM_RETRIEVED = P.SYSTEM.replace(FROZEN_PASSAGE, VARIANT_PASSAGE)

USER_RETRIEVED_TEXT = """\
Five entries a similarity retriever returned from this user's memory store for the question below \
(top 5 by cosine similarity over every entry the store holds, active or not), each with the lifecycle \
metadata the store records for it. No other part of the store is shown.

```
{retrieved}
```

Question: {question}\
"""
USER_RETRIEVED = USER_RETRIEVED_TEXT

_INDEXED_HEAD = P.USER_INDEXED[:P.USER_INDEXED.index("Question: {question}")]   # paragraph + fenced index, unchanged
USER_HYBRID_TEXT = _INDEXED_HEAD + """\
Five entries a similarity retriever returned from this store for the question below (top 5 by cosine \
similarity over every entry the store holds, active or not), each with the lifecycle metadata the \
store records for it.

```
{retrieved}
```

Question: {question}\
"""
USER_HYBRID = USER_HYBRID_TEXT

# --------------------------------------------------------------------------- #
# L3: SYSTEM_NOGATE = prompts_e1.SYSTEM with the two-step decomposition removed and nothing else.
# --------------------------------------------------------------------------- #
GATE_SENTENCE = " Judge this in two steps."
STEP1_PARAGRAPH = ("\n\n  Step 1, nok_candidates_found: is there content on this topic in the store that has "
                   "been superseded by a later value, retracted by the user, or has passed its date? true or false.")
STEP2_LINE = "  Step 2, nok: the probability, 0 to 100, that such content is present."
NOGATE_LINE = ("  nok: the probability, 0 to 100, that there is content on this topic in the store that has "
               "been superseded by a later value, retracted by the user, or has passed its date.")
EXAMPLE_FALSE, EXAMPLE_TRUE = "nok_candidates_found = false, ", "nok_candidates_found = true, "
GATED_SCHEMA = '{"fok": <0-100>, "nok_candidates_found": <true|false>, "nok": <0-100>, "would_search": <true|false>}'
NOGATE_SCHEMA = '{"fok": <0-100>, "nok": <0-100>, "would_search": <true|false>}'


def nogate_from_frozen(system):
    for needle in (GATE_SENTENCE, STEP1_PARAGRAPH, STEP2_LINE, EXAMPLE_FALSE, EXAMPLE_TRUE, GATED_SCHEMA):
        assert system.count(needle) == 1, needle[:40]
    s = system.replace(GATE_SENTENCE, "")
    s = s.replace(STEP1_PARAGRAPH, "")
    s = s.replace(STEP2_LINE, NOGATE_LINE)
    s = s.replace(EXAMPLE_FALSE, "").replace(EXAMPLE_TRUE, "")
    s = s.replace(GATED_SCHEMA, NOGATE_SCHEMA)
    return s


SYSTEM_NOGATE = nogate_from_frozen(P.SYSTEM)

TEXTS = {"SYSTEM_RETRIEVED": SYSTEM_RETRIEVED, "USER_RETRIEVED": USER_RETRIEVED, "USER_HYBRID": USER_HYBRID,
         "SYSTEM_NOGATE": SYSTEM_NOGATE}


def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def digests():
    return {k: sha256(v) for k, v in TEXTS.items()}


if __name__ == "__main__":
    for k, v in digests().items():
        print(f"{k:18s} {v}")
    print("prompts_e1 file :", P.file_sha256())
    print("prompts_e1 texts:", P.texts_sha256())
