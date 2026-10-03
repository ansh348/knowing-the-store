"""draft_questions.py -- R82-CF: the 30 frozen questions of the counterfactual cell.

Drafts three paraphrases per (persona, slot) pair and selects one by seed, BEFORE any
store version, index, label or score exists. The question is generated from the entity,
the slot name and the intent ONLY. It never sees the entry's value, its category, the
other candidates, or anything about the store's contents.

WHY THIS ORDER MATTERS. The cell exists to break the coupling between question text and
label that the main population carries (question text alone predicts labels at AUROC 0.92
to 0.97 there). Here the question is fixed and the store varies, so the label cannot be a
property of the question. Drafting the questions before any store version exists is what
makes that true by construction rather than by assertion.

WHAT THE PROMPT SEES
    entity  the persona's display name from the persona YAML
    slot    the slot_key attribute path, verbatim, e.g. "software_preference:excel"
            This is store METADATA, an attribute path. It is not the entry's value; the
            value lives in the entry text, which never enters the prompt. Where a slot
            qualifier happens to coincide with a value token, that is disclosed in the
            registration. It cannot leak the label, because the same question is asked of
            all three store versions of that pair.
    intent  CURRENT-STATE or UPCOMING, fixed per state class before drafting

INTENT GATE (rider 2 of the GO of 2026-08-29; a construction rule, not a deviation)
    Every selected paraphrase is typed by the frozen e1_metamemory/tools/intent.py
    type_question, driven through its text-only Rule 2 path by presenting the question
    under AV2, and must agree with the pair's registered intent:

        UPCOMING pair       -> Rule 2.2, future markers only
        CURRENT-STATE pair  -> Rule 2.3 "no marker fired", i.e. neither past nor future
                               markers fire, which is the signature of a present-tense
                               coverage question

    A past marker firing fails the check in both cases. A paraphrase that reads as past or
    change-aware would break the PN label under Definition 1 regardless of what the store
    contains, because build_e1.label gates the negative obligation on intent: PAST-EVENT
    and CHANGE-AWARE are structurally exempt.

    On failure the next of the three is taken in order and the substitution recorded. If
    all three fail, the pair is redrafted once under the same frozen prompt at a recorded
    alternate seed. A pair still failing after that is a STOP.

Model gpt-4.1-mini, temperature 0, seed 42, as in E1. Construction, not elicitation: no
FOK or NOK judgment is requested and no store is described.

Usage:  python r82_counterfactual/tools/draft_questions.py [--redraft]
Writes: r82_counterfactual/cf_questions.json
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))

from intent import CURRENT, UPCOMING, type_question  # noqa: E402


def load_env():
    """Parse the repo-root .env. Deliberately does NOT import the E1 api shim, which
    warms E1's committed response cache on import; E1 is closed at tag e1-complete and
    this pass reads nothing from it."""
    f = ROOT / ".env"
    if not f.exists():
        return
    for line in io.open(f, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

PAIRS = ROOT / "r82_counterfactual" / "cf_pairs.json"
NAMES = ROOT / "r82_counterfactual" / "_names.json"
OUT = ROOT / "r82_counterfactual" / "cf_questions.json"

MODEL = "gpt-4.1-mini"
TEMPERATURE = 0
SEED = 42
ALT_SEED = 4242
MAX_TOKENS = 400
N_PARAPHRASES = 3

# --------------------------------------------------------------------------- #
# FROZEN drafting prompt. Its sha256 is recorded in ADDENDUM_R82 beside the
# questions. Editing it after the freeze changes the hash and is detectable.
# --------------------------------------------------------------------------- #
SYSTEM = """\
You write questions a person might ask their own AI assistant about themselves.

You are given the person's name, one attribute path from their memory store, and the \
time-sense the question must carry. Write three different questions that ask about that \
attribute for that person.

Rules.
Write the question the way that person would actually type it to an assistant.
Ask for a specific detail, the way a real user would, not a yes or no question.
Do not invent or state any value for the attribute. You do not know what the store holds.
Do not mention memory, stores, records, metadata, or the assistant's knowledge.
Each of the three must be a genuinely different wording, not a light edit of another.

Time-sense.
CURRENT-STATE: ask about how things stand now, in the present tense. Do not use words \
like upcoming, coming up, scheduled, planning, plans to, going to, will, next, or future, \
and do not ask about the past.
UPCOMING: ask about something ahead of the person. Use a forward-looking word such as \
upcoming, coming up, scheduled, planning, or next. Do not ask about the past and do not \
use past-tense phrasing such as did, was, already, used to, or finished.

Respond with a single JSON object and nothing else:
{"questions": ["...", "...", "..."]}\
"""

USER = """\
Person: {entity}
Attribute path: {slot}
Time-sense: {intent}\
"""


def prompt_sha256() -> str:
    blob = "\x1f".join([SYSTEM, USER, MODEL, str(TEMPERATURE), str(SEED),
                        str(MAX_TOKENS), str(N_PARAPHRASES)])
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def jdump(obj, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def last_json(text):
    depth, start, best, ins, esc = 0, None, None, False, False
    for i, ch in enumerate(text or ""):
        if ins:
            ins = not (ch == '"' and not esc)
            esc = (ch == "\\" and not esc)
            continue
        if ch == '"':
            ins, esc = True, False
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None:
                best = text[start:i + 1]
    try:
        return json.loads(best) if best else None
    except Exception:
        return None


def intent_ok(question, want):
    """Rule-2 (text-only) typing of a candidate question against its registered intent.

    The question is presented under AV2 so type_question takes its text-only path; no
    real attack vector is claimed for it and none is stored.
    """
    got, rule, markers = type_question({"attack_vector": "AV2_expired_logistics",
                                        "question": question})
    if want == UPCOMING:
        ok = (got == UPCOMING)
    elif want == CURRENT:
        ok = (got == "UNRESOLVED" and rule == "Rule 2.3: no marker fired")
    else:
        raise SystemExit(f"unregistered intent {want!r}")
    return ok, got, rule, markers


def draft(client, entity, slot, intent, seed):
    r = client.chat.completions.create(
        model=MODEL, temperature=TEMPERATURE, seed=seed, max_tokens=MAX_TOKENS,
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": USER.format(entity=entity, slot=slot,
                                                          intent=intent)}])
    text = r.choices[0].message.content
    j = last_json(text) or {}
    qs = [str(q).strip() for q in (j.get("questions") or []) if str(q).strip()]
    return qs, r.usage.prompt_tokens, r.usage.completion_tokens, text


def main():
    load_env()
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    pairs = json.load(io.open(PAIRS, encoding="utf-8"))["pairs"]
    names = json.load(io.open(NAMES, encoding="utf-8"))

    rows, tin, tout, n_sub, n_redraft = [], 0, 0, 0, 0
    for p in pairs:
        entity = names[p["persona"]]
        slot = p["slot_key"][1]
        want = p["intent"]

        used_seed, attempt = SEED, "first"
        qs, a, b, raw = draft(client, entity, slot, want, used_seed)
        tin, tout = tin + a, tout + b

        def pick(qs):
            """Seeded choice, then the next of the three in order on failure."""
            if len(qs) < N_PARAPHRASES:
                return None, []
            rng = random.Random(f"{SEED}:{p['pair_id']}")
            start = rng.randrange(N_PARAPHRASES)
            trail = []
            for k in range(N_PARAPHRASES):
                idx = (start + k) % N_PARAPHRASES
                ok, got, rule, markers = intent_ok(qs[idx], want)
                trail.append({"index": idx, "question": qs[idx], "ok": ok,
                              "typed": got, "rule": rule, "markers": markers})
                if ok:
                    return idx, trail
            return None, trail

        idx, trail = pick(qs)
        if idx is None:
            n_redraft += 1
            used_seed, attempt = ALT_SEED, "redraft"
            qs2, a, b, raw = draft(client, entity, slot, want, used_seed)
            tin, tout = tin + a, tout + b
            idx2, trail2 = pick(qs2)
            if idx2 is None:
                print(json.dumps({"pair": p["pair_id"], "first": trail,
                                  "redraft": trail2}, indent=2, ensure_ascii=False))
                raise SystemExit(f"STOP: {p['pair_id']} fails the intent gate on all "
                                 f"six paraphrases; a registered amendment is required")
            qs, idx, trail = qs2, idx2, trail + trail2
        if len(trail) > 1 and trail[0]["ok"] is False:
            n_sub += 1

        rows.append({
            "pair_id": p["pair_id"], "persona": p["persona"], "state": p["state"],
            "intent": want, "entity": entity, "slot": slot,
            "question": qs[idx], "selected_index": idx, "attempt": attempt,
            "seed_used": used_seed, "paraphrases": qs, "intent_trail": trail,
        })
        print(f'{p["state"][:4]:5s} {p["persona"]:10s} [{attempt:8s} #{idx}] {qs[idx]}')

    rows.sort(key=lambda r: r["pair_id"])
    qhash = hashlib.sha256("\x1f".join(r["question"] for r in rows).encode("utf-8")).hexdigest()
    usd = tin / 1e6 * 0.40 + tout / 1e6 * 1.60

    jdump({"meta": {
        "n": len(rows), "model": MODEL, "temperature": TEMPERATURE, "seed": SEED,
        "alt_seed": ALT_SEED, "n_paraphrases": N_PARAPHRASES,
        "prompt_sha256": prompt_sha256(),
        "questions_sha256": qhash,
        "substitutions": n_sub, "redrafts": n_redraft,
        "tokens_in": tin, "tokens_out": tout, "usd": round(usd, 6),
        "prompt_sees": ["entity", "slot attribute path", "intent"],
        "prompt_never_sees": ["entry text or value", "category", "other candidates",
                              "any store content", "any label"],
        "intent_gate": "e1_metamemory/tools/intent.py type_question, text-only Rule 2 path",
    }, "questions": rows}, OUT)

    print(f"\n{len(rows)} questions -> {OUT}")
    print(f"  prompt    sha256 {prompt_sha256()}")
    print(f"  questions sha256 {qhash}")
    print(f"  substitutions {n_sub}   redrafts {n_redraft}")
    print(f"  tokens in {tin} out {tout}   spend ${usd:.4f}")


if __name__ == "__main__":
    main()
