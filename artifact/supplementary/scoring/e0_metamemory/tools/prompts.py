"""
prompts.py -- FROZEN elicitation prompt texts for E0.

This module is the single source of truth. PREREG_E0.md quotes it verbatim and
records its sha256; the elicitation harness imports it. Editing this file after
the pre-registration is committed changes that hash and is therefore a detectable
protocol violation, not a silent one.

The BLIND and INDEXED arms are byte-identical except that INDEXED appends the
fenced index block for the item's store variant. Nothing else differs -- same
system text, same FOK/NOK definitions, same output contract, same ordering.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

MODEL = "gpt-4.1-mini"
TEMPERATURE = 0
SEED = 42
MAX_TOKENS = 120

# --------------------------------------------------------------------------- #
# System prompt. Shared by both arms, verbatim.
# --------------------------------------------------------------------------- #
SYSTEM = """\
You are assessing a personal long-term memory store that belongs to one user.

The store is a structured collection of atomic facts extracted from that user's \
past conversations with an assistant. Each fact carries a behavioral category, an \
ingest timestamp, and lifecycle metadata.

You will be shown a question that the user has just asked. Before any retrieval \
is performed, give two probability judgments about what the store contains.

FOK (feeling of knowing): the probability, from 0 to 100, that the store contains \
content relevant to this question -- anything that should shape the answer.

NOK (negative-obligation knowledge): the probability, from 0 to 100, that the \
store contains superseded, retracted, or expired content bearing on this question \
-- content whose correct influence on the answer is suppression rather than use.

FOK and NOK are independent judgments. NOK is not a subset of FOK and the two need \
not sum to anything in particular.

Do not attempt to answer the question. Do not speculate about what the answer \
would be. Judge only what the store is likely to contain.

Respond with a single JSON object and nothing else:
{"fok": <0-100>, "nok": <0-100>, "would_search": <true|false>}\
"""

# --------------------------------------------------------------------------- #
# User message. BLIND gives the question alone; INDEXED prepends the index block.
# --------------------------------------------------------------------------- #
USER_BLIND = """\
Question: {question}\
"""

USER_INDEXED = """\
Metadata index of this user's memory store (counts and structure only -- no fact \
content):

```
{index}
```

Question: {question}\
"""

# --------------------------------------------------------------------------- #
# Index-leakage control (Step 3). Shown the index ONLY, and asked to answer.
# A control fire means the index carries answer content and must be tightened.
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


def prompt_sha256() -> str:
    """sha256 of this file, recorded in the pre-registration."""
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def texts_sha256() -> str:
    """sha256 of just the frozen strings, stable across comment edits."""
    blob = "\x1f".join([SYSTEM, USER_BLIND, USER_INDEXED, LEAKAGE_SYSTEM, LEAKAGE_USER,
                        MODEL, str(TEMPERATURE), str(SEED), str(MAX_TOKENS)])
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    print("file   sha256:", prompt_sha256())
    print("texts  sha256:", texts_sha256())
