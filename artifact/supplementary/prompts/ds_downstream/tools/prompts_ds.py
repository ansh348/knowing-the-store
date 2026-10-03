"""prompts_ds.py -- the Stage 2 answer prompt of ADDENDUM_DS.md section D.4 (frozen a5a2036).

NEW, HASHED, DISCLOSED AS NEW; not the frozen monitor lineage (prompts_e1.py is untouched and its
digests are asserted by verify_ds.py). The two strings below are the section D.4 texts verbatim;
verify_ds.py check E extracts the same texts from the frozen registration file and asserts equality,
and asserts the sha256 of each against AUX-DS-PROMPT. The prompt is identical under every policy; only
the view changes. Decoding parameters are prompts_e1's (gpt-4.1-mini, temperature 0, seed 42,
max_tokens 200, JSON mode).
"""
from __future__ import annotations

import hashlib

SYSTEM_ANSWER = (
    "You answer a question about a user from a view of the user's memory store. The view lists entries; each entry "
    "carries the lifecycle metadata the store records for it. An entry marked active is what the store currently holds "
    "as true. An entry marked superseded has been replaced by a later entry; one marked retracted was withdrawn by the "
    "user; one marked expired describes an arrangement whose date has passed. Superseded, retracted and expired entries "
    "do not state the user's current situation and must not be given as the answer.\n"
    "\n"
    "Answer in at most two sentences, from the view alone. If no entry in the view answers the question as it stands, "
    "say that the store does not currently contain the answer. Do not guess and do not use knowledge from outside the view.\n"
    "\n"
    "Return JSON only: {\"answer\": \"<your answer>\"}"
)

USER_ANSWER = (
    "Entries from this user's memory store, each with the lifecycle metadata the store records for it:\n"
    "\n"
    "```\n"
    "{view}\n"
    "```\n"
    "\n"
    "Question: {question}"
)

TEXTS = {"SYSTEM_ANSWER": SYSTEM_ANSWER, "USER_ANSWER": USER_ANSWER}


def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def digests():
    return {k: sha256(v) for k, v in TEXTS.items()}


def from_registration(path):
    """The two texts as the frozen registration prints them (section D.4's fenced blocks)."""
    s = open(path, encoding="utf-8").read()
    i = s.index("`SYSTEM_ANSWER`:\n```\n") + len("`SYSTEM_ANSWER`:\n```\n"); j = s.index("\n```\n\n`USER_ANSWER`:", i)
    k = s.index("`USER_ANSWER`:\n```\n") + len("`USER_ANSWER`:\n```\n"); l = s.index("\n```\n\n**Scoring, no LLM judge", k)
    return {"SYSTEM_ANSWER": s[i:j], "USER_ANSWER": s[k:l]}


if __name__ == "__main__":
    for k, v in digests().items():
        print(f"{k:14s} {v}")
