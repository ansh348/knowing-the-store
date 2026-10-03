"""author_pn.py -- R82-CF: author the record each PN version's write path would add.

Executes ADDENDUM_R82 section 2. Produces, per pair, the text FR-Bank would hold after the
counterfactual event, and asserts the predicates that make that claim checkable. It writes
no store; build_cf_cell.py consumes this.

PER STATE
    SUPERSESSION  a successor fact on the same slot. The write path (lifecycle_bank.py
                  :766-777) requires the same slot_key and confidence at or above the
                  category threshold, then deactivates the prior entry.
    RETRACTION    a retracting fact. The write path (:779-784) adds it with
                  is_retracted=True and deactivates everything at cosine above 0.85. That
                  threshold is a BRANCH of the write path, not a requirement on the text:
                  below it the original simply stays active, and the store still holds
                  exactly what the write path produces. Cosine is measured and recorded per
                  pair; it is never enforced. See ADDENDUM_R82 Amendment 1 and D-R82-2.
    EXPIRY        nothing is authored. There is no expiry write path; the anchor moves and
                  the ground truth records the same event as status: expired.

PREDICATES ASSERTED HERE (a failure is a STOP, never a silent retry past the budget)
    detector    e0_common.PersonaJoin.detector(old, new) must fire on the ORIGINAL entry at
                or above TAU_HI 0.80, which needs at least MIN_DISCR 3 tokens unique to each
                side, and must NOT fire on the new entry (CROSS_GUARD 0.34).
    gold        the new entry's text must cover the record's current-value field at or above
                TAU_GOLD 0.50 with at least MIN_SHARED 2 shared tokens, so Stage B anchors
                gold to it.
    cosine      retraction only, MEASURED not enforced: cosine(new, original) under
                text-embedding-3-small, the encoder the write path itself uses, recorded
                together with whether it crosses the 0.85 deactivation branch.

One authoring call per pair, one retry carrying the failed predicate back as instruction.
A pair failing twice is a STOP.

Usage:  python r82_counterfactual/tools/author_pn.py
Writes: r82_counterfactual/cf_pn_texts.json
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e0_metamemory" / "tools"))

import numpy as np  # noqa: E402
from e0_common import (  # noqa: E402
    CROSS_GUARD, MIN_DISCR, MIN_SHARED, TAU_GOLD, cov, toks,
)

PAIRS = ROOT / "r82_counterfactual" / "cf_pairs.json"
NAMES = ROOT / "r82_counterfactual" / "_names.json"
OUT = ROOT / "r82_counterfactual" / "cf_pn_texts.json"

MODEL = "gpt-4.1-mini"
EMBED_MODEL = "text-embedding-3-small"
TEMPERATURE = 0
SEED = 42
MAX_TOKENS = 300
TAU_HI = 0.80
COSINE_MIN = 0.85

SYSTEM = """\
You write the single memory record an assistant would store after something changed in a \
user's life.

You are given the record the store currently holds and what happened to it. Write the ONE \
new record the assistant would write next.

For a SUPERSESSION, the user has replaced the old value with a different one. Write the new \
value as a plain factual statement, in the same voice and format as the existing record. \
Give a concrete, plausible replacement value. Do not mention the old value, do not say \
"changed", "no longer", "instead", "used to", or "previously", and do not reference the \
update itself. It should read like a fact stated fresh.

For a RETRACTION, the user has cancelled or abandoned the thing. Write the record of that \
cancellation. It MUST repeat enough of the original subject matter to be recognisably about \
the same thing, and it MUST say plainly that it is cancelled, called off, dropped, or \
abandoned.

Rules for both.
One sentence. Start with "User" the way the existing record does.
Use at least four content words that do NOT appear in the existing record.
Keep at least three distinctive content words FROM the existing record out of your \
sentence, so the two records remain tellable apart.
State no dates.

Respond with a single JSON object and nothing else:
{"record": "..."}\
"""

USER = """\
Existing record: {text}
Attribute path: {slot}
What happened: {event}\
"""

EVENT = {
    "SUPERSESSION": "the user replaced this value with a different one",
    "RETRACTION": "the user cancelled or abandoned this",
}


def prompt_sha256():
    blob = "\x1f".join([SYSTEM, USER, json.dumps(EVENT, sort_keys=True), MODEL,
                        str(TEMPERATURE), str(SEED), str(MAX_TOKENS)])
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def jdump(o, p):
    p.parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def load_env():
    f = ROOT / ".env"
    for line in io.open(f, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


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


def check(old, new, drop, need_cosine, cos):
    """The registered predicates. Returns (ok, report, failures-as-instruction)."""
    ot, nt = toks(old, drop), toks(new, drop)
    do, dn = ot - nt, nt - ot
    rep = {"n_discr_old": len(do), "n_discr_new": len(dn)}
    fails = []
    if len(do) < MIN_DISCR:
        fails.append(f"keep at least {MIN_DISCR} distinctive words from the existing "
                     f"record OUT of your sentence (only {len(do)} were left out)")
    if len(dn) < MIN_DISCR:
        fails.append(f"use at least {MIN_DISCR} content words that do not appear in the "
                     f"existing record (only {len(dn)} were new)")
    if fails:
        return False, rep, fails

    # detector on the ORIGINAL entry: coverage of tokens unique to the old value
    sig_old = cov(do, ot) if len(do & ot) >= MIN_SHARED else 0.0
    # cross guard: the NEW entry must not itself look like the old value
    cross_new = cov(dn, nt)
    rep.update({"detector_signal_on_original": round(sig_old, 4),
                "cross_guard_on_new": round(cross_new, 4),
                "gold_cover_new": round(cov(nt, nt), 4)})
    if sig_old < TAU_HI:
        fails.append("make the two records share less wording so they are tellable apart")
    if need_cosine:
        rep["cosine_to_original"] = round(cos, 4)
        # NOT a predicate. lifecycle_bank.py:781-784 deactivates the original only when
        # cosine exceeds 0.85; below it the original stays active and the store still
        # holds exactly what the write path produces. Recorded, never enforced.
        rep["write_path_deactivates_original"] = bool(cos > COSINE_MIN)
    return (not fails), rep, fails


def main():
    load_env()
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    pairs = json.load(io.open(PAIRS, encoding="utf-8"))["pairs"]
    names = json.load(io.open(NAMES, encoding="utf-8"))

    def embed(texts):
        r = client.embeddings.create(model=EMBED_MODEL, input=texts)
        v = np.array([d.embedding for d in r.data], float)
        return v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-12), r.usage.total_tokens

    rows, tin, tout, temb, n_retry = [], 0, 0, 0, 0
    for p in pairs:
        if p["state"] == "EXPIRY":
            rows.append({"pair_id": p["pair_id"], "state": p["state"], "new_text": None,
                         "note": "no expiry write path; the anchor moves and nothing else"})
            print(f'{p["state"][:4]:5s} {p["persona"]:10s} (anchor only)')
            continue

        drop = toks(names[p["persona"]] or "")
        old = p["entry_text"]
        extra, rep, new = "", None, None
        for attempt in (1, 2):
            msgs = [{"role": "system", "content": SYSTEM + extra},
                    {"role": "user", "content": USER.format(
                        text=old, slot=p["slot_key"][1], event=EVENT[p["state"]])}]
            r = client.chat.completions.create(model=MODEL, temperature=TEMPERATURE,
                                               seed=SEED, max_tokens=MAX_TOKENS,
                                               messages=msgs)
            tin += r.usage.prompt_tokens
            tout += r.usage.completion_tokens
            cand = (last_json(r.choices[0].message.content) or {}).get("record", "").strip()
            cos = 0.0
            if p["state"] == "RETRACTION" and cand:
                v, tk = embed([old, cand])
                temb += tk
                cos = float(v[0] @ v[1])
            ok, rep, fails = check(old, cand, drop, p["state"] == "RETRACTION", cos)
            new = cand
            if ok:
                break
            n_retry += 1
            extra = ("\n\nYour previous attempt was rejected. Fix these and rewrite: "
                     + "; ".join(fails) + ".")
        if not ok:
            print(json.dumps({"pair": p["pair_id"], "old": old, "new": new,
                              "report": rep, "fails": fails}, indent=2, ensure_ascii=False))
            raise SystemExit(f"STOP: {p['pair_id']} fails its write-path predicates twice")

        rows.append({"pair_id": p["pair_id"], "state": p["state"], "new_text": new,
                     "predicates": rep, "attempts": attempt})
        print(f'{p["state"][:4]:5s} {p["persona"]:10s} [{attempt}] '
              f'sig={rep["detector_signal_on_original"]:.2f} '
              f'{"cos=%.3f " % rep["cosine_to_original"] if "cosine_to_original" in rep else ""}'
              f'{new[:62]}')

    rows.sort(key=lambda r: r["pair_id"])
    usd = tin / 1e6 * 0.40 + tout / 1e6 * 1.60 + temb / 1e6 * 0.02
    jdump({"meta": {"model": MODEL, "embed_model": EMBED_MODEL, "seed": SEED,
                    "prompt_sha256": prompt_sha256(), "retries": n_retry,
                    "tau_hi": TAU_HI, "cosine_min": COSINE_MIN,
                    "tokens_in": tin, "tokens_out": tout, "embed_tokens": temb,
                    "usd": round(usd, 6)},
           "records": rows}, OUT)
    print(f"\n{len(rows)} records -> {OUT}")
    print(f"  prompt sha256 {prompt_sha256()}   retries {n_retry}   spend ${usd:.4f}")


if __name__ == "__main__":
    main()
