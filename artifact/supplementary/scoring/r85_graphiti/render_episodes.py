"""render_episodes.py -- R85 Phase 0. Deterministic episode rendering. NO API CALLS.

Turns a committed FR-Bank persona bank into the episode stream Graphiti ingests. The rule
is frozen here and is not revised after any Graphiti dump is read.

RULE (frozen, R85 Phase 0, amending the ADDENDUM's event-time wording as D-R85-1)

  1. One episode per (persona, created_at). `created_at` is the session date and is the
     only populated timestamp: 17,024 of 18,936 records carry `event_time = null`.
  2. The episode reference timestamp is `created_at`, for EVERY episode, including the
     1,912 records that do carry an `event_time`. An event time is the date of the event,
     not the date the user stated it. The extractor is supposed to infer validity and
     expiry from content and reference time on its own, so the event date is never handed
     to it as a reference timestamp.
  3. No absolute date is injected into the text. The records already carry the user's own
     relative wording ("this weekend", "Saturday night"), which resolves against the
     reference timestamp. Injecting the stored `event_time` would state something the user
     never said and would hand the backend its expiry anchor.
  4. Episodes are ordered by `created_at`; records inside an episode by `id`.
  5. Status fields, lifecycle markers and supersedes pointers NEVER appear. Supersession is
     expressed only by the later record's content. Retraction is expressed only by the
     cancellation wording the record itself carries. Expiry is expressed by nothing, since
     time passes.
  6. The record is rendered as the user would have stated it: `User's X` becomes `My X`,
     `User <verb>` becomes `I <verb>` with the third-person singular inflection removed.
     Interior pronouns are left untouched, and the count of sentences still carrying a
     third-person possessive after conversion is reported rather than silently repaired.

Usage:
  python r85_graphiti/render_episodes.py --persona elena [--dry-run] [--audit]
  python r85_graphiti/render_episodes.py --all
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANKS = ROOT / "LifeMemEval" / "artifacts" / "lifecycle_banks"
OUT = Path(__file__).resolve().parent / "episodes"

# Signatures that must never reach the rendered text. These are bank field names, record
# identifiers, and the lifecycle state vocabulary as standalone uppercase tokens. Ordinary
# English words that happen to name a field ("confidence") are not leak signatures, so the
# guard matches the snake_case field name and the id pattern rather than the bare word.
FORBIDDEN_LITERAL = (
    "is_active", "is_retracted", "supersedes", "slot_key", "source_session",
    "numeric_value", "category_weights", "emotional_loading", "next_id", "event_time",
)
FORBIDDEN_PATTERN = re.compile(r"lb_\d{4,6}|(?:ACTIVE|SUPERSEDED|RETRACTED|EXPIRED)")

IRREGULAR = {
    "has": "have", "is": "am", "does": "do", "goes": "go", "hasn't": "haven't",
    "isn't": "am not", "doesn't": "don't",
}


def deinflect(verb: str) -> str:
    """Third-person singular present -> first person. Past tense and modals pass through."""
    low = verb.lower()
    if low in IRREGULAR:
        return IRREGULAR[low]
    if low.endswith("ies") and len(low) > 4:
        return low[:-3] + "y"
    if low.endswith(("ches", "shes", "sses", "xes", "zes", "oes")):
        return low[:-2]
    if low.endswith("s") and not low.endswith("ss"):
        return low[:-1]
    return low


def render_text(text: str, audit: collections.Counter) -> str:
    t = text.strip()
    if t.startswith("User's "):
        audit["possessive"] += 1
        return "My " + t[len("User's "):]
    if t.startswith("User "):
        rest = t[len("User "):]
        m = re.match(r"(\w+)(.*)$", rest, re.S)
        if not m:
            audit["fallthrough"] += 1
            return "I " + rest
        head, tail = m.group(1), m.group(2)
        if head.lower() == "and":
            audit["conjunction"] += 1
            return "I and" + tail
        audit["verb"] += 1
        return "I " + deinflect(head) + tail
    audit["no_user_prefix"] += 1
    return t


def build(persona: str):
    bank = json.loads((BANKS / f"{persona}.json").read_text("utf-8"))["entries"]
    audit = collections.Counter()
    sessions: dict[str, list] = collections.defaultdict(list)
    for rec in bank:
        sessions[rec["created_at"]].append(rec)

    episodes = []
    for created_at in sorted(sessions):
        recs = sorted(sessions[created_at], key=lambda r: r["id"])
        lines = []
        for r in recs:
            s = render_text(r["text"], audit)
            if s and s[-1] not in ".!?":
                s += "."
                audit["terminal_period_added"] += 1
            lines.append(s)
        body = " ".join(lines)
        episodes.append({
            "name": f"{persona}-{created_at[:10]}",
            "reference_time": created_at,
            "episode_body": body,
            "source_description": "user message",
            "n_records": len(recs),
        })
    audit["third_person_possessive_remaining"] = sum(
        1 for e in episodes for s in [e["episode_body"]]
        if re.search(r"\b(their|his|her)\b", s))
    return episodes, audit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--persona")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--audit", action="store_true")
    a = ap.parse_args()

    names = ([p.stem for p in sorted(BANKS.glob("*.json"))] if a.all else [a.persona])
    grand = collections.Counter()
    for persona in names:
        episodes, audit = build(persona)
        blob = json.dumps(episodes, ensure_ascii=False, sort_keys=True, indent=2)
        digest = hashlib.sha256(blob.encode("utf-8")).hexdigest()
        chars = sum(len(e["episode_body"]) for e in episodes)
        print(f"{persona:10s} episodes={len(episodes):3d} records={sum(e['n_records'] for e in episodes):4d} "
              f"chars={chars:6d} mean_body={chars//max(len(episodes),1):5d} sha256={digest[:16]}")
        leaks = [f for f in FORBIDDEN_LITERAL
                 if any(f in e["episode_body"] for e in episodes)]
        leaks += sorted({m.group(0) for e in episodes
                         for m in FORBIDDEN_PATTERN.finditer(e["episode_body"])})
        assert not leaks, f"LABEL LEAK in {persona}: {leaks}"
        grand.update(audit)
        if not a.dry_run:
            OUT.mkdir(exist_ok=True)
            (OUT / f"{persona}.json").write_text(blob, encoding="utf-8")
    if a.audit or a.all:
        print("\nrendering audit (rule applications over all rendered records):")
        for k, v in sorted(grand.items()):
            print(f"  {k:38s} {v}")


if __name__ == "__main__":
    main()
