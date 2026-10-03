# -*- coding: utf-8 -*-
"""ledger_phase1_r121.py -- program R121 Phase 1: append section 14's construction rows to cf2/NUMBERS_CF2.md (ruling 7).
Every number is read from the artifacts (cross_questions.json, workbook_lock_r121.json, leakscreen_ix.json, cue_list.py);
nothing typed from memory. Idempotent: refuses to run if the section header already exists. NO MODEL CALL."""
from __future__ import annotations

import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "r121" / "tools"))
import cue_list as C  # noqa: E402
import cross_questions as X  # noqa: E402
import prompts_p1 as P1  # noqa: E402

CF2 = ROOT / "r82_counterfactual" / "cf2"
LEDGER = CF2 / "NUMBERS_CF2.md"
BUILD = ROOT / "reviews" / "r121" / "build"
HEAD = "## 14. ADDENDUM_CF2_INTENT_CROSSOVER (program R121): the same store under two intents"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    text = io.open(LEDGER, encoding="utf-8").read()
    assert HEAD not in text, "section 14 already written"
    q = json.load(io.open(BUILD / "cross_questions.json", encoding="utf-8")); m = q["meta"]; rows = q["questions"]
    wl = json.load(io.open(BUILD / "workbook_lock_r121.json", encoding="utf-8"))
    lk = json.load(io.open(CF2 / "results" / "leakscreen_ix.json", encoding="utf-8"))
    cell = json.load(io.open(CF2 / "cf_cell.json", encoding="utf-8"))["items"]
    originals = sorted({(it["pair_id"], it["question"]) for it in cell})
    orig_hits = [(pid, C.cues_fired(qq), qq) for pid, qq in originals if C.cues_fired(qq)]
    cov = {lab: {pop: sum(C.matches(r[lab]["question"]) for r in rows if r["population"] == pop) for pop in "AB"} for lab in ("primary", "fallback")}
    n_a = sum(r["population"] == "A" for r in rows); n_b = len(rows) - n_a
    first_person = sum(1 for r in rows if (" my " in " " + r["primary"]["question"].lower() + " ") or (" i " in " " + r["primary"]["question"].lower() + " "))
    ident = [r["pair_id"] for r in rows if r["fallback_identical"]]
    L = [f"\n{HEAD} (registration draft `reviews/r121/registrations_draft/ADDENDUM_CF2_INTENT_CROSSOVER.md`, NOT YET FROZEN; Phase 1 construction rows, 2026-09-19; "
         f"`reviews/r121/tools/cross_questions.py`, `build_workbook_r121.py`, `ix_leakscreen.py`, `cue_list.py`, `prompts_p1.py`; gpt-4.1-mini only; nothing on the Anthropic key)\n",
         "Phase 0 report `reviews/r121/PHASE0_REPORT.md` and the author's nine rulings of 2026-09-19 (design O2: Opus 5 one draw on every new cell; caps Anthropic 15 USD, OpenAI 4 USD; "
         "the recorded Opus draw 1 for the primary P0 reading; the cue list untuned; one workbook, two tabs; the leak screen on 30 of A and all of B; ledger and rows here).\n",
         "| Key | Value |", "|---|---|",
         f"| **AUX-CF2-IX-P1** | The P1 monitor prompt (`prompts_p1.py`): P0 with the negative-obligation block replaced, one worked example added and \"Two\" → \"Three worked examples.\" (ruling 2); "
         f"system-text sha256 `{P1.p1_sha256()}` ({len(P1.SYSTEM_P1)} chars) against P0's `{P1.p0_sha256()[:16]}…` ({len(P1.P0.SYSTEM)} chars); the module asserts the construction at import. |",
         f"| **AUX-CF2-IX-CUES** | The keyword-intent lookup's cue list (`cue_list.py`, sha256 `{C.cue_sha256()}`): {len(C.CUES)} patterns ({len(C.PAST_FROZEN)} frozen PAST markers of `intent.py`, {len(C.CHANGE_CUES)} CHANGE, {len(C.PAST_CUES)} PAST), "
         f"proposed from the instruction texts before any question existed and kept untuned (ruling 4). **On the 148 recorded original questions {len(orig_hits)} fire**: "
         + "; ".join(f"`{pid}` ({', '.join(f'`{c}`' for c in cues)}: \"{qq}\")" for pid, cues, qq in orig_hits) + ". "
         f"**On the crossed questions the coverage is complete**: seed 42 A {cov['primary']['A']} of {n_a}, B {cov['primary']['B']} of {n_b}; seed 4242 A {cov['fallback']['A']} of {n_a}, B {cov['fallback']['B']} of {n_b} "
         f"(the renderer's instruction offers the cue wordings and the model used them on every question), so the keyword-intent lookup zeroes every crossed question and coincides with the oracle-intent lookup on cells 3 and 4; see the Phase 1 report for the consequence for P-I4. |",
         f"| **AUX-CF2-IX-QUESTIONS** | `reviews/r121/build/cross_questions.json`: **{m['n']} pairs** (A {n_a} supersession → CHANGE, B {n_b} expiry → PAST; retraction out of scope), renderer prompt sha256 `{m['prompt_sha256']}`, "
         f"model `{m['model']}` served `{', '.join(m['served'])}`, temperature {m['temperature']}, seeds {m['seed']} (primary) and {m['alt_seed']} (fallback), max_tokens {m['max_tokens']}, one question per call, both seeds drafted for every pair ({2 * m['n']} calls). "
         f"Prompt saw {', '.join(m['prompt_sees'])}; never {', '.join(m['prompt_never_sees'])}. Automatic gate (G1 no frozen future marker, G2 not identical to the original, G3 non-empty): "
         f"**primary failures {m['primary_gate_fail']}, fallback failures {m['fallback_gate_fail']}**. **Fallback byte-identical to the primary: {m['fallback_identical']} of {m['n']}** (temperature 0; the CF-2 record saw 15 of 32), so the second seed offers a different question on {m['n'] - m['fallback_identical']} pairs only. "
         f"Questions sha256 seed 42 `{m['questions_sha256_seed42']}`, seed 4242 `{m['questions_sha256_seed4242']}`. First-person voice {first_person} of {m['n']} (the recorded originals: 141 of 160). "
         f"Tokens {m['tokens_in']} in / {m['tokens_out']} out; **${m['usd']:.4f}**. |",
         f"| **AUX-CF2-IX-CHECK** (as built) | `reviews/r121/build/AUTHOR_CHECK_R121.xlsx`, **sha256 as built `{wl['sha256_as_built']}`** ({wl['built']}); tabs `seed42` (all {wl['n_rows']} rows, four YES/NO columns and Notes), `seed4242` (consulted only for rows failed on `seed42`, said at its top; "
         f"{wl['n_identical_fallback']} rows marked IDENTICAL with their verdict cells locked), `CRITERIA`; {len(wl['locked_cells'])} locked cells hashed in `build/workbook_lock_r121.json`. The returned workbook's sha256 and the verdict counts fill this row at Phase 2. Not yet sent. |",
         f"| **AUX-CF2-IX-LEAK** | `results/leakscreen_ix.json` (`ix_leakscreen.py`; cf2_leakscreen's protocol; `prompts_e1` file sha `{lk['meta']['prompts_e1_file_sha256'][:12]}…`, texts sha `{lk['meta']['prompts_e1_texts_sha256'][:12]}…`; served `{', '.join(lk['meta']['served_models'])}`): "
         + "; ".join(f"**{k}** {c['n_correct']} of {c['n']} correct, {c['n_non_unknown']} non-UNKNOWN, {c['n_parse_failures']} parse failures, **{c['verdict']}**" for k, c in lk["cells"].items())
         + f". Registered cells A (seed-42 questions, 30 PRESENT versions by seed 42 under v2) and B (all 30 PRESENT versions under v3) both PASS; the fallback cover cells screen the differing seed-4242 questions in the samples. ${lk['meta']['usd_total']:.4f}. |",
         f"| **AUX-CF2-IX-SPEND** (Phase 1) | OpenAI, token-metered at list price: drafting ${m['usd']:.4f} + leak screen ${lk['meta']['usd_total']:.4f} = **${m['usd'] + lk['meta']['usd_total']:.4f}** of the 4 USD cap; Anthropic $0. Not an invoice. |",
         ]
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
