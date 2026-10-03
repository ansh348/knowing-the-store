# -*- coding: utf-8 -*-
"""cross_questions.py -- program R121 (the intent crossover): the crossed-question renderer. Phase 1; no call in Phase 0.

One new question per pair of the counterfactual set, from the pair's manifest slot, under a fixed instruction:
population A (the 88 supersession pairs) the CHANGE time-sense (how has the attribute changed over time);
population B (the 30 expiry pairs) the PAST time-sense (what the event was or when it took place, in the past tense).
The prompt sees what the frozen CF renderer saw (draft_questions.py: entity, slot attribute path, time-sense) and nothing
else: no entry text, no value, no category, no store content, no label, and not the original question either, so the
crossed question cannot inherit the original's wording or its value tokens.

INSTRUCTION VERSION 2 (deviation D-IX-1, 2026-09-19). The author's check found, before any verdict and before any
monitor call, that version 1's questions were about half in the second person or addressed the persona by name (the
recorded originals are the user's own voice, so the intent manipulation was confounded with a voice change), that every
population-B question asked how the event went (which the store never records), and that several population-A questions
invented a time window. Version 2 requires the first person, forbids "your", names and invented windows, and asks
population B what the event was or when it took place. Version 1 is kept below as SYSTEM_V1 so its hash can be re-checked;
its questions are kept in build/superseded/.

Model gpt-4.1-mini, max_tokens 200. The primary is seed 42 at temperature 0 (`draft`). The one fallback is the
registered second lineage (the author's Phase 1 ruling 2): the same instruction, temperature 0.7, seed 4242 (`draft2`).
Both are drafted for every pair up front so that the author's check reads one workbook: the seed-42 question first, the
lineage-2 question only where the first fails; a pair whose both questions fail is dropped and reported with its
reasons. A fallback byte-identical to the primary is a drop.

Automatic gate before the author's check (a construction rule, as the CF renderer's intent gate was), applied to
each drafted question; a rejection is a failure of that draft, reported by count:
  G1  no frozen FUTURE marker of e1_metamemory/tools/intent.py fires (a crossed question reading UPCOMING would break
      the licensed label);
  G2  the question is not byte-identical to the pair's original question;
  G3  the JSON parses and the question is non-empty;
  G4  no second person ("you", "your", "yours", "yourself");                       (D-IX-1)
  G5  no token of the persona's display name;                                        (D-IX-1)
  G6  no time-window phrase (TIME_WINDOW below).                                     (D-IX-1)
The gate does NOT use the cue list of cue_list.py: the keyword-intent lookup must stay an empirical reader of the
crossed questions, not their construction. The positive criteria (i)-(iv) of the brief are the author's.

Usage:  python cross_questions.py draft        -> reviews/r121/build/cross_questions.json (the primary, seed 42, t = 0)
        python cross_questions.py draft2       -> the registered second lineage (t = 0.7, seed 4242) into the same file
        python cross_questions.py sha          -> the instruction hashes (v2 primary, v2 lineage 2, v1 for the record)
        (the workbook: build_workbook_r121.py)
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("e1_metamemory/tools", "r82_counterfactual/tools"):
    sys.path.insert(0, str(ROOT / p))
from intent import FUT_RE, fired, norm  # noqa: E402
import draft_questions as D  # noqa: E402  (load_env, last_json, jdump; the frozen renderer's constants)

CF2 = ROOT / "r82_counterfactual" / "cf2"
BUILD = ROOT / "reviews" / "r121" / "build"
OUT = BUILD / "cross_questions.json"

MODEL = "gpt-4.1-mini"
TEMPERATURE = 0
SEED = 42
ALT_SEED = 4242
MAX_TOKENS = 200
CROSSED = {"SUPERSESSION": "CHANGE", "EXPIRY": "PAST"}          # retraction: out of scope (no licensed intent)
LINEAGE2_TEMPERATURE = 0.7
LINEAGE2_SEED = ALT_SEED

# --------------------------------------------------------------------------- #
# FROZEN crossed-question instruction, VERSION 2 (D-IX-1). Its sha256 is recorded
# in the registration. The cue list of cue_list.py is proposed from THIS text
# (the words it offers as examples), before any question is generated.
# --------------------------------------------------------------------------- #
SYSTEM = """\
You write questions a person might ask their own AI assistant about themselves.

You are given the person's name, one attribute path from their memory store, and the \
time-sense the question must carry. Write one question that asks about that attribute \
for that person.

Rules.
Write the question in the first person, as the person asking their assistant about \
themselves: use "my" and "I". Never use "your" for the person. Never address anyone by \
name, and do not use the person's name at all. Never ask what someone thinks.
Ask for a specific detail, the way a real user would, not a yes or no question.
Do not invent or state any value for the attribute. You do not know what the store holds.
Do not invent a time window: say "over time", never "over the past year" or "in the last \
few weeks".
Do not mention memory, stores, records, metadata, or the assistant's knowledge.

Time-sense.
CHANGE: ask how this attribute has changed over time, so that a full answer must give \
both what it was before and what it is now. Use a wording that asks about change or \
history, such as "how has my ... changed over time", "what did my ... use to be", \
"before", "previously", or "earlier". Do not use words like upcoming, coming up, \
scheduled, planning, plans to, going to, will, next, or future, and do not ask only \
about the present.
PAST: ask, in the past tense, what the event named by the attribute was or when it took \
place, as something that has already happened, such as "What did I have planned for \
...?", "When was my ...?", or "What was my ...?". Never ask how it went, how it turned \
out, or what happened at it. Do not use words like upcoming, coming up, scheduled, \
planning, plans to, going to, will, next, or future, and do not ask about what is still \
to come.

Respond with a single JSON object and nothing else:
{"question": "..."}\
"""

USER = """\
Person: {entity}
Attribute path: {slot}
Time-sense: {intent}\
"""

# VERSION 1, superseded by D-IX-1 (kept for the record; prompt sha 5c15f5ba..., lineage-2 sha 3fd41897...)
SYSTEM_V1 = """\
You write questions a person might ask their own AI assistant about themselves.

You are given the person's name, one attribute path from their memory store, and the \
time-sense the question must carry. Write one question that asks about that attribute \
for that person.

Rules.
Write the question the way that person would actually type it to an assistant.
Ask for a specific detail, the way a real user would, not a yes or no question.
Do not invent or state any value for the attribute. You do not know what the store holds.
Do not mention memory, stores, records, metadata, or the assistant's knowledge.

Time-sense.
CHANGE: ask how this attribute has changed over time, so that a full answer must give \
both what it was before and what it is now. Use a wording that asks about change or \
history, such as "how has ... changed", "what did ... use to be", "before", \
"previously", "over time", or "earlier". Do not use words like upcoming, coming up, \
scheduled, planning, plans to, going to, will, next, or future, and do not ask only \
about the present.
PAST: ask about the event named by the attribute as something that has already \
happened, so that a full answer must describe the event after the fact. Use a \
past-tense wording that asks what happened, such as "how did ... go", "what happened \
at", "what was ... like", "how did ... turn out", or "after". Do not use words like \
upcoming, coming up, scheduled, planning, plans to, going to, will, next, or future, \
and do not ask about what is still to come.

Respond with a single JSON object and nothing else:
{"question": "..."}\
"""

# G6: time-window phrases the instruction forbids (an invented window). Fixed before any version-2 question was drafted.
TIME_WINDOW = [
    r"\b(over|in|during|within|for|across) the (past|last|previous|recent) ((few|couple of|several|many|\d+) )?(year|years|month|months|week|weeks|day|days|decade|decades)\b",
    r"\b(over|in|during|within|for) (the )?recent (years|months|weeks|days)\b",
    r"\b(last|this|next|past) (year|month|week|season|summer|winter|spring|autumn|fall)\b",
    r"\b(yesterday|today|tonight|tomorrow)\b",
    r"\b(recently|lately|nowadays)\b",
    r"\b(a|one|two|three|four|five|six|seven|eight|nine|ten|\d+|few|several) (years|months|weeks|days|year|month|week|day) ago\b",
    r"\bsince (last|this|\d{4})\b",
    r"\bin \d{4}\b",
]
TIME_WINDOW_RE = [re.compile(p, re.I) for p in TIME_WINDOW]
SECOND_PERSON_RE = re.compile(r"\b(you|your|yours|yourself)\b", re.I)


def prompt_sha256(system=SYSTEM) -> str:
    blob = "\x1f".join([system, USER, MODEL, str(TEMPERATURE), str(SEED), str(ALT_SEED), str(MAX_TOKENS)])
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def lineage2_sha256(system=SYSTEM) -> str:
    blob = "\x1f".join([system, USER, MODEL, str(LINEAGE2_TEMPERATURE), str(LINEAGE2_SEED), str(MAX_TOKENS)])
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def name_tokens(entity):
    """The persona's display-name tokens (letters only, length >= 2), matched as whole words."""
    return [t for t in re.findall(r"[A-Za-z][A-Za-z'\-]+", norm(entity)) if len(t) >= 2]


def gate(question, original, entity):
    """-> (ok, reasons). G1 future markers, G2 identity with the original, G3 non-empty, G4 second person, G5 persona name, G6 time window."""
    reasons = []
    if not question:
        return False, ["G3: empty or unparsed"]
    t = norm(question)
    f = fired(FUT_RE, t)
    if f:
        reasons.append("G1: future marker " + ", ".join(f))
    if question.strip() == original.strip():
        reasons.append("G2: identical to the original question")
    m = SECOND_PERSON_RE.search(t)
    if m:
        reasons.append(f"G4: second person '{m.group(0)}'")
    hits = [n for n in name_tokens(entity) if re.search(r"\b" + re.escape(n) + r"\b", t, re.I)]
    if hits:
        reasons.append("G5: persona name " + ", ".join(hits))
    tw = [r.pattern for r in TIME_WINDOW_RE if r.search(t)]
    if tw:
        reasons.append("G6: time window " + "; ".join(tw))
    return not reasons, reasons


def pairs_in_scope():
    pairs = json.load(io.open(CF2 / "cf_pairs_cf2.json", encoding="utf-8"))["pairs"]
    qs = {r["pair_id"]: r for r in json.load(io.open(CF2 / "cf_questions_cf2.json", encoding="utf-8"))["questions"]}
    names = json.load(io.open(CF2 / "_names_cf2.json", encoding="utf-8"))
    out = []
    for p in sorted(pairs, key=lambda p: p["pair_id"]):
        if p["state"] not in CROSSED:
            continue
        q = qs[p["pair_id"]]
        out.append({"pair_id": p["pair_id"], "persona": p["persona"], "state": p["state"], "population": "A" if p["state"] == "SUPERSESSION" else "B",
                    "entity": names[p["persona"]], "slot": p["slot_key"][1], "original_intent": p["intent"], "crossed_intent": CROSSED[p["state"]],
                    "original_question": q["question"]})
    assert len(out) == 118 and sum(r["population"] == "A" for r in out) == 88, len(out)
    return out


def draft_one(client, entity, slot, intent, seed, temperature=TEMPERATURE):
    r = client.chat.completions.create(model=MODEL, temperature=temperature, seed=seed, max_tokens=MAX_TOKENS,
                                       messages=[{"role": "system", "content": SYSTEM},
                                                 {"role": "user", "content": USER.format(entity=entity, slot=slot, intent=intent)}])
    text = r.choices[0].message.content
    j = D.last_json(text) or {}
    q = str(j.get("question") or "").strip()
    return q, r.usage.prompt_tokens, r.usage.completion_tokens, text, r.model, getattr(r, "system_fingerprint", None)


def gate_census(rows, label):
    c = {"rejected": 0, "G1": 0, "G2": 0, "G3": 0, "G4": 0, "G5": 0, "G6": 0}
    for r in rows:
        if not r[label]["gate_ok"]:
            c["rejected"] += 1
            for reason in r[label]["gate_reasons"]:
                c[reason[:2]] += 1
    return c


def _draft_label(label, seed, temperature, prog_name):
    """Draft one label (primary or the lineage) for every pair, progressively, returning the row dicts and the token totals."""
    D.load_env()
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    BUILD.mkdir(parents=True, exist_ok=True)
    prog = BUILD / prog_name
    done = {}
    if prog.exists():
        for line in io.open(prog, encoding="utf-8"):
            if line.strip():
                r = json.loads(line); done[r["pair_id"]] = r
    out, tin, tout, served, fps = {}, 0, 0, set(), set()
    for p in pairs_in_scope():
        if p["pair_id"] in done:
            r = done[p["pair_id"]]
        else:
            q, a, b, raw, mdl, fp = draft_one(client, p["entity"], p["slot"], p["crossed_intent"], seed, temperature)
            ok, reasons = gate(q, p["original_question"], p["entity"])
            r = {"pair_id": p["pair_id"], "label": label, "seed": seed, "temperature": temperature, "question": q, "gate_ok": ok, "gate_reasons": reasons,
                 "raw": raw[:300], "tok_in": a, "tok_out": b, "served_model": mdl, "system_fingerprint": fp}
            with io.open(prog, "a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
        tin, tout = tin + r["tok_in"], tout + r["tok_out"]; served.add(r["served_model"]); fps.add(r.get("system_fingerprint"))
        out[p["pair_id"]] = r
        print(f'{p["population"]} {p["persona"]:10s} [{"ok " if r["gate_ok"] else "GATE"}] {r["question"]}' + ("" if r["gate_ok"] else "   <- " + "; ".join(r["gate_reasons"])))
    return out, tin, tout, sorted(served), sorted(x for x in fps if x)


def cmd_draft():
    assert not OUT.exists(), f"{OUT} exists; the superseded file belongs in build/superseded/"
    drafted, tin, tout, served, fps = _draft_label("primary", SEED, TEMPERATURE, "cross_questions_rows.jsonl")
    rows = []
    for p in pairs_in_scope():
        rec = dict(p); r = drafted[p["pair_id"]]
        rec["primary"] = {k: r[k] for k in ("seed", "temperature", "question", "gate_ok", "gate_reasons", "raw", "system_fingerprint")}
        rows.append(rec)
    usd = tin / 1e6 * 0.40 + tout / 1e6 * 1.60
    doc = {"meta": {"instruction_version": 2, "deviation": "D-IX-1", "n": len(rows), "model": MODEL, "max_tokens": MAX_TOKENS,
                    "primary": {"seed": SEED, "temperature": TEMPERATURE, "prompt_sha256": prompt_sha256(), "served": served, "system_fingerprints": fps,
                                "questions_sha256": hashlib.sha256("\x1f".join(r["primary"]["question"] for r in rows).encode("utf-8")).hexdigest(),
                                "gate": gate_census(rows, "primary"), "tokens_in": tin, "tokens_out": tout, "usd": round(usd, 6)},
                    "superseded_v1": {"prompt_sha256": prompt_sha256(SYSTEM_V1), "lineage2_sha256": lineage2_sha256(SYSTEM_V1), "file": "reviews/r121/build/superseded/cross_questions_v1.json"},
                    "prompt_sees": ["entity", "slot attribute path", "crossed time-sense"],
                    "prompt_never_sees": ["entry text or value", "category", "the original question", "any store content", "any label"],
                    "gate": "G1 no frozen future marker; G2 not identical to the original; G3 non-empty; G4 no second person; G5 no persona-name token; G6 no time-window phrase (cross_questions.gate)"},
           "questions": rows}
    D.jdump(doc, OUT)
    m = doc["meta"]["primary"]
    print(f"\n{len(rows)} pairs -> {OUT}\n  prompt sha256 {m['prompt_sha256']}\n  questions sha256 {m['questions_sha256']}\n  served {served}  fingerprints {fps}\n  gate {m['gate']}\n  tokens in {tin} out {tout}  spend ${usd:.4f}")


def cmd_draft2():
    doc = json.load(io.open(OUT, encoding="utf-8")); rows = doc["questions"]; meta = doc["meta"]
    assert "fallback" not in rows[0], "lineage 2 already drafted"
    drafted, tin, tout, served, fps = _draft_label("lineage2", LINEAGE2_SEED, LINEAGE2_TEMPERATURE, "cross_questions_rows_lineage2.jsonl")
    for rec in rows:
        r = drafted[rec["pair_id"]]
        rec["fallback"] = {k: r[k] for k in ("seed", "temperature", "question", "gate_ok", "gate_reasons", "raw", "system_fingerprint")}
        rec["fallback_identical"] = rec["primary"]["question"] == rec["fallback"]["question"]
    usd = tin / 1e6 * 0.40 + tout / 1e6 * 1.60
    meta["lineage2"] = {"seed": LINEAGE2_SEED, "temperature": LINEAGE2_TEMPERATURE, "lineage_sha256": lineage2_sha256(), "served": served, "system_fingerprints": fps,
                        "questions_sha256": hashlib.sha256("\x1f".join(r["fallback"]["question"] for r in rows).encode("utf-8")).hexdigest(),
                        "gate": gate_census(rows, "fallback"), "identical_to_primary": sum(r["fallback_identical"] for r in rows),
                        "tokens_in": tin, "tokens_out": tout, "usd": round(usd, 6)}
    meta["fallback_lineage"] = "lineage2"
    D.jdump(doc, OUT)
    m = meta["lineage2"]
    print(f"\nlineage 2 -> {OUT}\n  lineage sha256 {m['lineage_sha256']}\n  questions sha256 {m['questions_sha256']}\n  served {served}  fingerprints {fps}"
          f"\n  gate {m['gate']}  identical to primary {m['identical_to_primary']}\n  tokens in {tin} out {tout}  spend ${usd:.4f}")


if __name__ == "__main__":
    if sys.argv[1] == "draft":
        cmd_draft()
    elif sys.argv[1] == "draft2":
        cmd_draft2()
    elif sys.argv[1] == "sha":
        print("v2 primary :", prompt_sha256()); print("v2 lineage2:", lineage2_sha256())
        print("v1 primary :", prompt_sha256(SYSTEM_V1)); print("v1 lineage2:", lineage2_sha256(SYSTEM_V1))
