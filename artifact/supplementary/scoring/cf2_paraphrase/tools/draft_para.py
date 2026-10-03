"""draft_para.py -- ADDENDUM_PARA §4-§5: draft the 148 paraphrases, screen them, write the sheet.

Registration: registrations/ADDENDUM_PARA.md (sha256 45cad63d…), frozen before the first call.
Construction only: gpt-4.1-mini, temperature 0, max_tokens 400, three candidates per draft, seed
42; on failure a second draft at seed 4242 and a third at 424242, each with the surface tokens that
failed the screen appended to the forbidden list. Selection per draft: the start index is
random.Random(f"42:{pair_id}").randrange(3) (the CF-1 rule), then in order the first candidate
that passes (1) the §3 screen and (2) the CF-1 intent gate (draft_questions.intent_ok). A pair with
no passing candidate after three drafts is EXCLUDED, listed with its nine candidates and the
token each failed on. Fewer than 120 of 148 passing is a STOP before any sheet is written.

Every draft, candidate, screen result and intent-gate trail goes to cf2_paraphrase/para_questions.json;
the accepted paraphrases go to reviews/v12/PARAPHRASE_SHEET.md for the author's read (§5). No
score of any kind is computed or written here.

Usage:
  python cf2_paraphrase/tools/draft_para.py --dry-run     locks, gate, forbidden-set census; NO call
  python cf2_paraphrase/tools/draft_para.py               the drafting run (needs the freeze)
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from para_common import (PARA, REG_SHA, ROOT, SHEET, forbidden, jdump, jload, locks, lookup_gate,  # noqa: E402
                         pairs, screen)
from draft_questions import intent_ok, last_json, load_env  # noqa: E402

MODEL = "gpt-4.1-mini"
TEMPERATURE = 0
MAX_TOKENS = 400
N = 3
SEEDS = (42, 4242, 424242)
MIN_ACCEPTED = 120
OUT = PARA / "para_questions.json"

# FROZEN prompt, ADDENDUM_PARA §4, verbatim.
SYSTEM = """You rewrite questions a person might ask their own AI assistant about themselves.

You are given the person's name, one question they asked, the time-sense the question carries,
and a list of forbidden words. Write three different questions that ask for exactly the same
thing as the given question, for that person, without using any forbidden word or any singular,
plural or hyphenated form of a forbidden word.

Rules.
Ask for the same specific detail the given question asks for; do not broaden or narrow it.
Write the question the way that person would actually type it to an assistant.
Do not invent or state any value or fact. You do not know what the assistant remembers.
Do not mention memory, stores, records, metadata, or the assistant's knowledge.
Each of the three must be a genuinely different wording, not a light edit of another.
Never use a forbidden word, even as part of a longer word.

Time-sense.
CURRENT-STATE: ask about how things stand now, in the present tense. Do not use words like
upcoming, coming up, scheduled, planning, plans to, going to, will, next, or future, and do not
ask about the past.
UPCOMING: ask about something ahead of the person. Use a forward-looking word such as upcoming,
coming up, scheduled, planning, or next. Do not ask about the past and do not use past-tense
phrasing such as did, was, already, used to, or finished.

Respond with a single JSON object and nothing else:
{"questions": ["...", "...", "..."]}"""

USER = """Person: {entity}
Question: {question}
Time-sense: {intent}
Forbidden words: {forbidden}"""


def prompt_sha256():
    """§4: sha256 over SYSTEM ⊕ USER ⊕ model ⊕ temperature ⊕ max_tokens ⊕ N."""
    blob = "\x1f".join([SYSTEM, USER, MODEL, str(TEMPERATURE), str(MAX_TOKENS), str(N)])
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def draft(client, pair, forb, seed):
    r = client.chat.completions.create(
        model=MODEL, temperature=TEMPERATURE, seed=seed, max_tokens=MAX_TOKENS,
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": USER.format(entity=pair["entity"], question=pair["question"],
                                                          intent=pair["intent"], forbidden=" ".join(sorted(forb)))}])
    text = r.choices[0].message.content
    j = last_json(text) or {}
    qs = [str(q).strip() for q in (j.get("questions") or []) if str(q).strip()]
    return qs, r.usage.prompt_tokens, r.usage.completion_tokens, text, getattr(r, "model", None), getattr(r, "system_fingerprint", None)


def select(pair, qs, F):
    """§4 selection: seeded start, then in order the first candidate passing the screen and the intent gate."""
    rng = random.Random(f"42:{pair['pair_id']}")
    start = rng.randrange(N)
    trail, failed_surface = [], []
    for k in range(N):
        idx = (start + k) % N
        if idx >= len(qs):
            trail.append({"index": idx, "question": None, "screen_ok": False, "reason": "missing candidate"})
            continue
        cand = qs[idx]
        ok_s, hit, same = screen(cand, pair["question"], F)
        rec = {"index": idx, "question": cand, "screen_ok": ok_s, "screen_hits": hit, "same_as_original": same}
        if hit:
            # the surface forms the model used, for the redraft's appended forbidden list
            failed_surface += [w for w in cand.replace("-", " ").split() if any(h in w.lower() for h in hit)]
        if ok_s:
            ok_i, got, rule, markers = intent_ok(cand, pair["intent"])
            rec.update({"intent_ok": ok_i, "typed": got, "rule": rule, "markers": markers})
            if ok_i:
                trail.append(rec)
                return idx, trail, failed_surface
        trail.append(rec)
    return None, trail, failed_surface


def main():
    dry = "--dry-run" in sys.argv
    L = locks()
    print("locks:", json.dumps({k: v for k, v in L.items() if k.endswith("_ok") or k == "n_questions"}))
    if not L["all_ok"]:
        raise SystemExit(f"STOP: lock failure {L}")
    P = pairs()
    assert len(P) == 148
    gate, gate_ok = lookup_gate(P)
    print("lookup gate on the original questions:", {k: round(v, 4) for k, v in gate.items()}, "PASS" if gate_ok else "FAIL")
    if not gate_ok:
        raise SystemExit("STOP: lookup gate on the original questions failed at four decimals")
    F_all, census = {}, []
    for pr in P:
        F, c = forbidden(pr)
        F_all[pr["pair_id"]] = F
        q_toks = set(t for t in (_s(t) for t in _toks(pr["question"])))
        c.update({"pair_id": pr["pair_id"], "original_tokens": len(q_toks),
                  "original_tokens_in_F": len(q_toks & F), "original_passes_screen": not (q_toks & F)})
        census.append(c)
    n_orig_pass = sum(1 for c in census if c["original_passes_screen"])
    print(f"forbidden sets built for 148 pairs: |F| min {min(c['F_size'] for c in census)}, median "
          f"{sorted(c['F_size'] for c in census)[74]}, max {max(c['F_size'] for c in census)}; names per pair median "
          f"{sorted(c['names'] for c in census)[74]}; original questions that would already pass the screen: {n_orig_pass} of 148; "
          f"original tokens in F, mean {sum(c['original_tokens_in_F'] for c in census) / 148:.2f} of {sum(c['original_tokens'] for c in census) / 148:.2f}")
    print(f"prompt sha256 {prompt_sha256()}")
    if dry:
        jdump({"locks": L, "lookup_gate": gate, "forbidden_census": census, "prompt_sha256": prompt_sha256(),
               "status": "DRY RUN: no call made"}, PARA / "para_dryrun.json")
        print(f"dry run: wrote {PARA / 'para_dryrun.json'}; no call made")
        return

    # ---------------------------------------------------------------- the drafting run
    load_env()
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    rows, excluded, tin, tout, n_calls = [], [], 0, 0, 0
    served_ids, projection = [], None
    t0 = time.time()
    for pr in P:
        F = F_all[pr["pair_id"]]
        forb = set(F)
        drafts, chosen = [], None
        for d_i, seed in enumerate(SEEDS):
            qs, a, b, raw, served, fp = draft(client, pr, forb, seed)
            n_calls += 1; tin += a; tout += b
            served_ids.append(served)
            if n_calls == 3:
                # §8: the lane's own three-call probe -- served identifier (E1.7) and the projection, before the lane continues
                ok_id = all(x and "gpt-4.1-mini" in x for x in served_ids)
                est_calls = 2 * 148                                   # the registration's ~2 drafts per pair
                usd = est_calls * ((tin / 3) * 0.40 / 1e6 + (tout / 3) * 1.60 / 1e6)
                projection = {"probe_calls": 3, "served": served_ids[:], "identifier_ok": ok_id, "mean_in": tin / 3, "mean_out": tout / 3,
                              "est_calls": est_calls, "usd": round(usd, 4), "usd_x1.3": round(usd * 1.3, 4)}
                print("probe / projection:", json.dumps(projection))
                if not ok_id:
                    raise SystemExit("STOP: served-identifier mismatch (E1.7)")
            idx, trail, failed_surface = select(pr, qs, F)
            drafts.append({"draft": d_i + 1, "seed": seed, "forbidden_size": len(forb), "candidates": qs, "raw": raw,
                           "served_model": served, "system_fingerprint": fp, "trail": trail, "selected_index": idx})
            if idx is not None:
                chosen = qs[idx]
                break
            forb |= {w.lower() for w in failed_surface}
        rec = {"pair_id": pr["pair_id"], "persona": pr["persona"], "entity": pr["entity"], "slot": pr["slot"],
               "intent": pr["intent"], "state": pr["state"], "question": pr["question"], "F_size": len(F),
               "drafts": drafts, "attempts": len(drafts), "paraphrase": chosen, "accepted": chosen is not None}
        if chosen is None:
            excluded.append(rec)
            print(f"  EXCLUDED {pr['pair_id']}: no passing candidate after {len(drafts)} drafts")
        else:
            # the screen re-run on the accepted paraphrase, as the registration requires at scoring time too
            ok_s, hit, same = screen(chosen, pr["question"], F)
            assert ok_s, (pr["pair_id"], hit, same)
            print(f"  {pr['state'][:4]:5s} {pr['persona']:10s} [draft {len(drafts)} #{drafts[-1]['selected_index']}] {chosen}")
        rows.append(rec)
    accepted = [r for r in rows if r["accepted"]]
    para_sha = hashlib.sha256("\x1f".join(r["paraphrase"] for r in accepted).encode("utf-8")).hexdigest()
    usd = tin * 0.40 / 1e6 + tout * 1.60 / 1e6            # gpt-4.1-mini list, as the CF-2 ledger priced it
    meta = {"registration_sha256": REG_SHA, "prompt_sha256": prompt_sha256(), "model": MODEL, "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS, "n_candidates": N, "seeds": SEEDS, "n_pairs": len(rows), "n_accepted": len(accepted),
            "n_excluded": len(excluded), "attempts_histogram": {str(k): sum(1 for r in rows if r["attempts"] == k) for k in (1, 2, 3)},
            "calls": n_calls, "prompt_tokens": tin, "completion_tokens": tout, "usd_list_est": round(usd, 4),
            "seconds": round(time.time() - t0, 1), "paraphrases_sha256": para_sha, "locks": L, "lookup_gate": gate,
            "probe_projection": projection, "served_models": sorted(set(x for x in served_ids if x))}
    jdump({"meta": meta, "rows": rows}, OUT)
    print(f"\naccepted {len(accepted)} / 148; excluded {len(excluded)}; attempts {meta['attempts_histogram']}; "
          f"calls {n_calls}; tokens {tin}+{tout}; ~${usd:.4f}; paraphrases sha256 {para_sha}")
    if len(accepted) < MIN_ACCEPTED:
        raise SystemExit(f"STOP: {len(accepted)} < {MIN_ACCEPTED} accepted; the author's ruling is required before any sheet is written")
    write_sheet(accepted, excluded, meta)


def write_sheet(accepted, excluded, meta):
    """§5: one row per accepted pair; the author fills the two verdict columns."""
    L = ["# PARAPHRASE_READ — the author's read of the CF-2 paraphrases (ADDENDUM_PARA §5)\n",
         f"Registration sha256 `{REG_SHA}`; prompt sha256 `{meta['prompt_sha256']}`; paraphrase set sha256 "
         f"`{meta['paraphrases_sha256']}`; {meta['n_accepted']} of 148 pairs accepted by the screen and the intent gate "
         f"({meta['n_excluded']} excluded, listed at the end). No score of any kind has been computed on these paraphrases.\n",
         "Fill the two verdict columns. **Column 1** (asks the same thing under the same intent? YES / NO): a NO excludes the "
         "pair, no re-draft. **Column 2** (names the value or plan? YES / NO): a disclosure only, for the Appendix H.2 split "
         "recomputed on this set; it excludes nothing. Every accepted paraphrase shares no content token with the scrubbed slot name "
         "or any attribute name its three v3 summaries print (stopwords excluded), and typed to its registered intent under "
         "the CF-1 gate. Under the author's ruling of 2026-09-14 the slot-path half of the screen covers the scrubbed slot name "
         "(the part a summary prints), so a paraphrase may name the value or plan -- that is what column 2 records.\n",
         "| # | pair_id | state | intent | original question | paraphrase | asks the same thing under the same intent? (YES / NO) | names the value or plan? (YES / NO) |",
         "|---:|---|---|---|---|---|---|---|"]
    for i, r in enumerate(accepted, 1):
        L.append(f"| {i} | `{r['pair_id']}` | {r['state']} | {r['intent']} | {r['question']} | **{r['paraphrase']}** |  |  |")
    L.append("")
    L.append(f"Rows drafted under the registered screen (run 1): {sum(1 for r in accepted if r.get('run', 1) == 1)}; redrafted under the narrowed §3(a) "
             f"(the author's ruling of 2026-09-14): {sum(1 for r in accepted if r.get('run') == 2)}. Which rows are which is recorded in `para_questions.json` "
             f"and not marked here, so the read is blind to it.")
    if excluded:
        L.append("\n## Excluded by the screen after three drafts (no author action)\n")
        L.append("| pair_id | state | intent | original question | candidates (draft, index, offending tokens) |")
        L.append("|---|---|---|---|---|")
        for r in excluded:
            cands = "; ".join(f"d{d['draft']}#{t['index']} \"{t.get('question')}\" [{', '.join(t.get('screen_hits', []) or (['intent'] if t.get('intent_ok') is False else ['?']))}]"
                              for d in r["drafts"] for t in d["trail"])
            L.append(f"| `{r['pair_id']}` | {r['state']} | {r['intent']} | {r['question']} | {cands} |")
    SHEET.parent.mkdir(parents=True, exist_ok=True)
    io.open(SHEET, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(f"wrote {SHEET}")


# ---------------------------------------------------------------- the redraft of the 61 (the author's ruling of 2026-09-14, evening)
RUN1 = PARA / "para_questions_run1.json"


def redraft():
    """Option (2): the 87 accepted paraphrases of run 1 stand; only the excluded pairs are redrafted under the
    same prompt, model, seeds, candidates, selection rule and intent gate, with §3(a) narrowed to the scrubbed
    slot name (para_common.forbidden scope 'narrowed'); §3(b) unchanged. The floor of 120 applies to the
    resulting set. Every accepted paraphrase also records whether it passes the registered (unnarrowed)
    screen and which value tokens it carries -- a disclosure, not a criterion."""
    L = locks()
    if not L["all_ok"]:
        raise SystemExit(f"STOP: lock failure {L}")
    if not RUN1.exists():
        io.open(RUN1, "w", encoding="utf-8", newline="\n").write(io.open(OUT, encoding="utf-8").read())
    Q1 = jload(RUN1)
    assert Q1["meta"]["prompt_sha256"] == prompt_sha256(), "STOP: prompt sha256 differs from run 1"
    assert Q1["meta"]["registration_sha256"] == REG_SHA
    P = {pr["pair_id"]: pr for pr in pairs()}
    assert len(Q1["rows"]) == 148
    gate, gate_ok = lookup_gate(list(P.values()))
    if not gate_ok:
        raise SystemExit("STOP: lookup gate on the original questions failed at four decimals")
    load_env()
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    rows, tin, tout, n_calls, served_ids = [], 0, 0, 0, []
    t0 = time.time()
    for r1 in Q1["rows"]:
        pr = P[r1["pair_id"]]
        F_reg, c_reg = forbidden(pr, "registered")
        F_nar, c_nar = forbidden(pr, "narrowed")
        assert F_nar <= F_reg
        if r1["accepted"]:
            rec = dict(r1)
            rec.update({"run": 1, "screen_scope": "registered", "F_size_registered": len(F_reg), "F_size_narrowed": len(F_nar)})
            ok_n, hit_n, _ = screen(rec["paraphrase"], pr["question"], F_nar)
            assert ok_n, (pr["pair_id"], hit_n)
            rows.append(rec)
            continue
        forb = set(F_nar)
        drafts, chosen = [], None
        for d_i, seed in enumerate(SEEDS):
            qs, a, b, raw, served, fp = draft(client, pr, forb, seed)
            n_calls += 1; tin += a; tout += b; served_ids.append(served)
            idx, trail, failed_surface = select(pr, qs, F_nar)
            drafts.append({"draft": d_i + 1, "seed": seed, "forbidden_size": len(forb), "candidates": qs, "raw": raw,
                           "served_model": served, "system_fingerprint": fp, "trail": trail, "selected_index": idx})
            if idx is not None:
                chosen = qs[idx]
                break
            forb |= {w.lower() for w in failed_surface}
        rec = {"pair_id": pr["pair_id"], "persona": pr["persona"], "entity": pr["entity"], "slot": pr["slot"], "intent": pr["intent"],
               "state": pr["state"], "question": pr["question"], "F_size": len(F_nar), "F_size_registered": len(F_reg), "F_size_narrowed": len(F_nar),
               "run": 2, "screen_scope": "narrowed", "run1_drafts": r1["drafts"], "drafts": drafts, "attempts": len(drafts),
               "paraphrase": chosen, "accepted": chosen is not None}
        if chosen is None:
            print(f"  EXCLUDED (run 2) {pr['pair_id']}: no passing candidate after {len(drafts)} drafts")
        else:
            ok_n, hit_n, same = screen(chosen, pr["question"], F_nar)
            assert ok_n, (pr["pair_id"], hit_n, same)
            print(f"  {pr['state'][:4]:5s} {pr['persona']:10s} [run 2, draft {len(drafts)} #{drafts[-1]['selected_index']}] {chosen}")
        rows.append(rec)
    # the disclosure on every accepted paraphrase: the registered screen and the value tokens it carries
    for rec in rows:
        if not rec["accepted"]:
            continue
        pr = P[rec["pair_id"]]
        F_reg, _ = forbidden(pr, "registered"); F_nar, _ = forbidden(pr, "narrowed")
        ok_r, hit_r, _ = screen(rec["paraphrase"], pr["question"], F_reg)
        rec["passes_registered_screen"] = ok_r
        rec["value_tokens_in_paraphrase"] = sorted(set(hit_r) & (F_reg - F_nar))
    accepted = [r for r in rows if r["accepted"]]
    excluded = [r for r in rows if not r["accepted"]]
    para_sha = hashlib.sha256("\x1f".join(r["paraphrase"] for r in accepted).encode("utf-8")).hexdigest()
    usd = tin * 0.40 / 1e6 + tout * 1.60 / 1e6
    m1 = Q1["meta"]
    meta = {"registration_sha256": REG_SHA, "prompt_sha256": prompt_sha256(), "model": MODEL, "temperature": TEMPERATURE, "max_tokens": MAX_TOKENS,
            "n_candidates": N, "seeds": SEEDS, "n_pairs": len(rows), "n_accepted": len(accepted), "n_excluded": len(excluded),
            "run1": {k: m1.get(k) for k in ("n_accepted", "n_excluded", "attempts_histogram", "calls", "prompt_tokens", "completion_tokens", "usd_list_est", "paraphrases_sha256", "served_models", "probe_projection")},
            "run2": {"scope": "narrowed (the author's ruling of 2026-09-14, evening)", "n_redrafted": sum(1 for r in rows if r.get("run") == 2),
                     "n_accepted": sum(1 for r in accepted if r.get("run") == 2), "n_excluded": len(excluded),
                     "attempts_histogram": {str(k): sum(1 for r in rows if r.get("run") == 2 and r["attempts"] == k) for k in (1, 2, 3)},
                     "calls": n_calls, "prompt_tokens": tin, "completion_tokens": tout, "usd_list_est": round(usd, 4),
                     "served_models": sorted(set(x for x in served_ids if x)), "seconds": round(time.time() - t0, 1)},
            "calls": m1["calls"] + n_calls, "prompt_tokens": m1["prompt_tokens"] + tin, "completion_tokens": m1["completion_tokens"] + tout,
            "usd_list_est": round(m1["usd_list_est"] + usd, 4), "attempts_histogram": {str(k): sum(1 for r in rows if r["attempts"] == k) for k in (1, 2, 3)},
            "n_accepted_passing_registered_screen": sum(1 for r in accepted if r["passes_registered_screen"]),
            "paraphrases_sha256": para_sha, "locks": L, "lookup_gate": gate, "served_models": sorted(set(list(m1.get("served_models") or []) + [x for x in served_ids if x]))}
    jdump({"meta": meta, "rows": rows}, OUT)
    print(f"\nrun 2: redrafted {meta['run2']['n_redrafted']}, accepted {meta['run2']['n_accepted']}, still excluded {len(excluded)}; calls {n_calls}; ~${usd:.4f}")
    print(f"set: accepted {len(accepted)} / 148 (of which {meta['n_accepted_passing_registered_screen']} also pass the registered screen); paraphrases sha256 {para_sha}")
    if len(accepted) < MIN_ACCEPTED:
        raise SystemExit(f"STOP: {len(accepted)} < {MIN_ACCEPTED} accepted after the redraft; the author's ruling is required before any sheet is written")
    write_sheet(accepted, excluded, meta)


def _toks(s):
    from index_features import toks
    return toks(s)


def _s(t):
    from index_features import _sing
    return _sing(t)


if __name__ == "__main__":
    if "--redraft" in sys.argv:
        redraft()
    else:
        main()
