"""
prompts_e2.py -- FROZEN prompt text added by E2. Frozen at the calibration boundary.

E2 adds exactly ONE new elicitation prompt: policy (iv), the verbalized-confidence
gate with no index. Everything else reuses E1's frozen `prompts_e1`:

  policy (v)/(vi) gate   prompts_e1.SYSTEM + USER_INDEXED, BELIEVED index -- which
                         is E1's INDEXED-BELIEVED arm exactly, so those signals are
                         already committed and cost nothing to obtain
  answerer               FR's GENERATION_SYSTEM_PROMPT, verbatim (e2_common)
  judge                  FR's pinned rubric, unmodified (LifeMemEval/evaluate_e2e.py)

WHY (iv) IS NOT JUST E1'S BLIND ARM. E1's blind arm asks for FOK directly. The
literature's version of this baseline (arXiv 2607.25600) does better: it elicits a
structured PROVISIONAL ANSWER first, then a confidence, then thresholds the
confidence on held-out data. Making the model commit to an attempt before rating
itself is what gives that baseline its strength, and the pre-registration says the
baseline gets the literature's own best version of itself rather than a strawman.
E1's blind FOK remains available as a weaker secondary reference.

The model, decoding parameters and cache discipline are prompts_e1's, unchanged.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

VERBAL_SYSTEM = """\
You are the gate in front of a personal long-term memory store belonging to one \
user. The store holds short factual statements drawn from that user's past \
conversations with an assistant.

You are shown a question the user has just asked. You cannot see the store. Decide \
whether it is worth retrieving from it.

Work in three steps.

  1. provisional_answer: attempt the question from what you already know, in one \
short sentence. If you have no basis for an answer, write "none".

  2. confidence_without_store: the probability, 0 to 100, that your provisional \
answer is correct and complete as it stands.

  3. p_store_has_relevant: the probability, 0 to 100, that this user's memory \
store contains content relevant to this question -- anything that should shape \
the answer.

Judge the store, not your own knowledge, in step 3. A question you cannot answer \
yourself is not automatically one the store covers, and a question you can answer \
yourself may still have a personal detail recorded that would change the answer.

Respond with a single JSON object and nothing else:
{"provisional_answer": "<one sentence, or none>", \
"confidence_without_store": <0-100>, "p_store_has_relevant": <0-100>}\
"""

VERBAL_USER = """\
Question: {question}\
"""


def texts_sha256() -> str:
    blob = "\x1f".join([VERBAL_SYSTEM, VERBAL_USER])
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def file_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


if __name__ == "__main__":
    print("texts sha256:", texts_sha256())
    print("file  sha256:", file_sha256())
