"""
prompts_e1.py -- FROZEN elicitation prompt texts for E1.

PREREG_E1.md quotes this module verbatim and records its sha256; the harness
imports it. Editing after the freeze changes the hash and is therefore a
detectable protocol violation.

Why E0's prompts.py could not be reused: its system text asserts "Each fact
carries a behavioral category, an ingest timestamp, and lifecycle metadata."
That is FALSE for Mem0 (no category, no lifecycle fields) and A-MEM (category is
the constant 'Uncategorized', no lifecycle fields at all). A prompt that tells the
model the store has structure it does not have would confound the believed-state
axis, which is precisely the axis E1 exists to measure. The E1 system text
describes only what is true of every backend.

NOK redesign (design doc section 6), addressing the E0 null (blind NOK 0.00 on
316/510 items, four distinct values across the whole arm):
  cause 1  the index carried no lifecycle signal          -> fixed in index v2
  cause 2  "negative obligation" was defined but never shown -> two worked examples
  cause 3  a single probability judgment collapsed detection and quantification
           -> decomposed: nok_candidates_found first, then nok

Worked examples are drawn from AV8_numeric_preservation questions, which are
OUT OF SCOPE for E1 by rule (design doc section 3 / INTENT_RULES.md) and appear
in no cell of any tier. They therefore cannot leak scoreable material.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

MODEL = "gpt-4.1-mini"
TEMPERATURE = 0
SEED = 42
MAX_TOKENS = 200

STRONG_MODEL = "gpt-5.6-sol"          # via codex exec, blind arm only

# --------------------------------------------------------------------------- #
# System prompt. Shared by BLIND and both INDEXED provenances, verbatim.
# --------------------------------------------------------------------------- #
SYSTEM = """\
You are assessing a personal long-term memory store that belongs to one user.

The store is a collection of short factual statements extracted from that user's \
past conversations with an assistant. Different memory systems record different \
amounts of structure alongside those statements, and some record almost none.

You will be shown a question the user has just asked. BEFORE any retrieval is \
performed, give two judgments about what the store contains.

FOK (feeling of knowing): the probability, 0 to 100, that the store contains \
content relevant to this question -- anything that should shape the answer.

NEGATIVE OBLIGATION: content the store still holds whose correct influence on the \
answer is SUPPRESSION rather than use, because it has been superseded, retracted, \
or has expired. Judge this in two steps.

  Step 1, nok_candidates_found: is there content on this topic in the store that \
has been superseded by a later value, retracted by the user, or has passed its \
date? true or false.

  Step 2, nok: the probability, 0 to 100, that such content is present.

Two worked examples.

  Question: "How much did the user pay for their gaming PC?"
  The store holds one price, stated once, never revised. Nothing has been \
superseded or retracted and no date has passed. nok_candidates_found = false, \
nok = 5.

  Question: "How much does the user earn per cultural tour?"
  The store holds a per-tour rate, but the user later said they no longer run \
those tours. The rate is still in the store and would mislead if surfaced as \
current. nok_candidates_found = true, nok = 85.

Note that FOK and the negative-obligation judgment are independent. A store can \
hold plenty of relevant content with nothing stale in it, and it can hold stale \
content on a topic it otherwise covers poorly.

Do not attempt to answer the question. Do not speculate about what the answer \
would be. Judge only what the store is likely to contain.

Respond with a single JSON object and nothing else:
{"fok": <0-100>, "nok_candidates_found": <true|false>, "nok": <0-100>, \
"would_search": <true|false>}\
"""

USER_BLIND = """\
Question: {question}\
"""

USER_INDEXED = """\
Metadata index of this user's memory store (structure and counts only -- no fact \
content). Fields this memory system cannot record are marked as such; a field \
marked "not expressible by this backend" means the system does not track it, \
which is different from tracking it and finding none.

```
{index}
```

Question: {question}\
"""

# --------------------------------------------------------------------------- #
# Staircase variant (FR-Bank, TRUE index only, ~150 items). Breaks the D20
# quantisation by asking for a sequence of binary comparisons instead of a
# number: the model never emits a probability, so it cannot round to 0/10/20.
# --------------------------------------------------------------------------- #
STAIRCASE_SYSTEM = """\
You are assessing a personal long-term memory store that belongs to one user, \
before any retrieval is performed.

You will be shown a metadata index of the store and a question the user asked. \
Answer four independent yes/no questions about how likely it is that the store \
contains content relevant to the question. Each asks about a different threshold. \
Answer each on its own terms; they are not required to agree, but a coherent \
assessment will normally answer yes to the lower thresholds and no to the higher \
ones.

Do not attempt to answer the user's question.

Respond with a single JSON object and nothing else:
{"gt_10": <true|false>, "gt_30": <true|false>, "gt_50": <true|false>, \
"gt_70": <true|false>}\
"""

STAIRCASE_USER = """\
```
{index}
```

Question the user asked: {question}

gt_10: is the chance the store holds relevant content greater than 10%?
gt_30: greater than 30%?
gt_50: greater than 50%?
gt_70: greater than 70%?\
"""

# --------------------------------------------------------------------------- #
# Index-leakage control. Run per backend per provenance per ladder level.
# --------------------------------------------------------------------------- #
LEAKAGE_SYSTEM = """\
You are shown a metadata index of a personal memory store belonging to one user, \
and a question that user has asked. Answer the question as well as you can from \
the index alone. If the index does not let you determine the answer, reply exactly \
UNKNOWN.

Respond with a single JSON object and nothing else:
{"answer": "<your answer, or UNKNOWN>"}\
"""

LEAKAGE_USER = """\
```
{index}
```

Question: {question}\
"""

# --------------------------------------------------------------------------- #
# Natural-absent probe drafting (construction, not elicitation).
# --------------------------------------------------------------------------- #
PROBE_SYSTEM = """\
You draft NATURAL-ABSENT probe questions for a memory-benchmark study.

A natural-absent probe is a question the user could plausibly ask their assistant, \
about their own life, whose answer the assistant's memory store does NOT contain. \
The absence must be natural -- a topic that simply never came up -- not a trick \
question and not about someone else.

You are given a persona sketch and the ATTRIBUTE NAMES the store already covers \
(names only, no values). Draft questions in ordinary life domains that those \
attribute names do NOT cover. Avoid any topic named in the inventory. Avoid \
yes/no questions about whether a thing exists; ask for a specific detail, the way \
a user actually would.

Return a single JSON object: {"probes": [{"question": "...", "domain": "...", \
"why_absent": "..."}]}\
"""



# --------------------------------------------------------------------------- #
# E1.5 Run B, hypothesis H-b: identical to USER_INDEXED except that lines whose
# value is the inexpressibility marker are OMITTED rather than rendered. The
# paragraph explaining the marker goes with them -- it would otherwise refer to
# something no longer in the prompt. That substitution is the ONLY difference.
# --------------------------------------------------------------------------- #
USER_INDEXED_NOMARKER = """Metadata index of this user's memory store (structure and counts only -- no fact content). This index reports the fields this memory system records; it does not list every field a memory system could record.

```
{index}
```

Question: {question}"""


def file_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def texts_sha256() -> str:
    """sha256 over the frozen strings only -- stable across comment edits."""
    blob = "\x1f".join([SYSTEM, USER_BLIND, USER_INDEXED, STAIRCASE_SYSTEM,
                        STAIRCASE_USER, LEAKAGE_SYSTEM, LEAKAGE_USER, PROBE_SYSTEM, USER_INDEXED_NOMARKER,
                        MODEL, STRONG_MODEL, str(TEMPERATURE), str(SEED),
                        str(MAX_TOKENS)])
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    print("file  sha256:", file_sha256())
    print("texts sha256:", texts_sha256())
