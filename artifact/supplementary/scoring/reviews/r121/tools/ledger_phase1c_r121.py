# -*- coding: utf-8 -*-
"""ledger_phase1c_r121.py -- program R121 Phase 1c (deviation D-IX-1): append the version-2 rows to cf2/NUMBERS_CF2.md section 14.
Every number read from the artifacts (cross_questions.json v2, workbook_lock_r121.json, leakscreen_ix.json, cue_list.py v2). Idempotent. NO MODEL CALL."""
from __future__ import annotations

import io
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "r121" / "tools"))
import cue_list as C  # noqa: E402
import cross_questions as X  # noqa: E402

CF2 = ROOT / "r82_counterfactual" / "cf2"
LEDGER = CF2 / "NUMBERS_CF2.md"
BUILD = ROOT / "reviews" / "r121" / "build"
MARK = "### 14c. Phase 1c"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    text = io.open(LEDGER, encoding="utf-8").read()
    assert MARK not in text, "14c already written"
    q = json.load(io.open(BUILD / "cross_questions.json", encoding="utf-8")); m = q["meta"]; rows = q["questions"]; pm = m["primary"]; l2 = m["lineage2"]
    assert m["instruction_version"] == 2 and pm["prompt_sha256"] == X.prompt_sha256() and l2["lineage_sha256"] == X.lineage2_sha256()
    assert m["superseded_v1"]["prompt_sha256"] == X.prompt_sha256(X.SYSTEM_V1)
    wl = json.load(io.open(BUILD / "workbook_lock_r121.json", encoding="utf-8")); dz = wl["design"]
    lk = json.load(io.open(CF2 / "results" / "leakscreen_ix.json", encoding="utf-8")); cells = lk["cells"]
    n_a = sum(r["population"] == "A" for r in rows); n_b = len(rows) - n_a
    cov = {lab: {pop: sum(C.matches(r[lab]["question"]) for r in rows if r["population"] == pop) for pop in "AB"} for lab in ("primary", "fallback")}
    fp = {lab: sum(bool(re.search(r"\b(my|i|me|mine)\b", r[lab]["question"], re.I)) for r in rows) for lab in ("primary", "fallback")}
    second = {lab: sum(bool(re.search(r"\b(you|your|yours|yourself)\b", r[lab]["question"], re.I)) for r in rows) for lab in ("primary", "fallback")}
    cell = json.load(io.open(CF2 / "cf_cell.json", encoding="utf-8"))["items"]
    originals = sorted({(it["pair_id"], it["question"]) for it in cell})
    orig_hits = [(pid, C.cues_fired(qq), qq) for pid, qq in originals if C.cues_fired(qq)]
    gate_fmt = lambda g: f"rejected {g['rejected']} (G1 {g['G1']}, G2 {g['G2']}, G3 {g['G3']}, G4 {g['G4']}, G5 {g['G5']}, G6 {g['G6']})"
    L = [f"\n{MARK} — deviation **D-IX-1** (`reviews/r121/DEVIATIONS_R121.md`, 2026-09-19): the crossed-question instruction amended after the author's check of the version-1 workbook found, before any verdict and before any monitor call, that about half the questions were second-person or addressed the persona by name (A 41 of 88 \"your\"; B 26 of 30 not first person), every population-B question asked how the event went, and several population-A questions invented a time window. Version 2 requires the first person, forbids \"your\", names and invented windows, and asks B what the event was or when it took place; the gate gained G4–G6; the cue list was re-derived from the amended text before any generation; both lineages regenerated; the superseded material kept in `reviews/r121/build/superseded/` and `results/leakscreen_ix_v1_superseded.json`. Sections 14 and 14b stand as the version-1 record.\n",
         "| Key | Value |", "|---|---|",
         f"| **AUX-CF2-IX-INSTRUCTION** (v2) | Instruction version 2 (`cross_questions.py` `SYSTEM`): **prompt sha256 `{pm['prompt_sha256']}`; lineage-2 sha256 `{l2['lineage_sha256']}`**; version 1 (`SYSTEM_V1`, kept) `{m['superseded_v1']['prompt_sha256']}` / `{m['superseded_v1']['lineage2_sha256']}`, reproduced from the kept text. Gate G4 (second person), G5 (persona-name token), G6 (time-window phrase; `TIME_WINDOW`, {len(X.TIME_WINDOW)} patterns) added to G1–G3. |",
         f"| **AUX-CF2-IX-CUES** (v2) | `cue_list.py` version 2, **sha256 `{C.cue_sha256()}`**, {len(C.CUES)} cues ({len(C.PAST_FROZEN)} frozen PAST markers, {len(C.CHANGE_CUES)} CHANGE, {len(C.PAST_CUES)} PAST: {', '.join('`' + p + '`' for p in C.PAST_CUES)}), re-derived from the version-2 instruction before any version-2 question existed; version 1 (`{C.V1_SHA[:16]}…`) reproduces from the module. "
         f"On the 148 recorded original questions {len(orig_hits)} fire: " + "; ".join(f"`{pid}` ({', '.join('`' + c + '`' for c in cues)})" for pid, cues, qq in orig_hits) + f" (rosa's is a retraction pair, outside the populations). Coverage of the version-2 crossed questions: primary A {cov['primary']['A']} of {n_a}, B {cov['primary']['B']} of {n_b}; lineage 2 A {cov['fallback']['A']} of {n_a}, B {cov['fallback']['B']} of {n_b}. |",
         f"| **AUX-CF2-IX-QUESTIONS** (v2) | `reviews/r121/build/cross_questions.json` (instruction version 2): **primary** seed {pm['seed']}, temperature {pm['temperature']}, served `{', '.join(pm['served'])}`, fingerprints {', '.join('`' + f + '`' for f in pm['system_fingerprints'])}, questions sha256 `{pm['questions_sha256']}`, gate {gate_fmt(pm['gate'])}, tokens {pm['tokens_in']} in / {pm['tokens_out']} out, ${pm['usd']:.4f}; "
         f"**lineage 2** seed {l2['seed']}, temperature {l2['temperature']}, fingerprints {', '.join('`' + f + '`' for f in l2['system_fingerprints'])}, questions sha256 `{l2['questions_sha256']}`, gate {gate_fmt(l2['gate'])}, **byte-identical to the primary on {l2['identical_to_primary']} of {len(rows)}**, ${l2['usd']:.4f}. "
         f"Rejections: primary `{', '.join(wl['gate_rejected']['primary'])}`; lineage 2 `{', '.join(wl['gate_rejected']['fallback'])}` (both G1, \"scheduled\"). First person {fp['primary']} of {len(rows)} (primary) and {fp['fallback']} of {len(rows)} (lineage 2); second person {second['primary']} and {second['fallback']}. |",
         f"| **AUX-CF2-IX-CHECK** (v2, as built; the reduced design) | `reviews/r121/build/AUTHOR_CHECK_R121.xlsx` **sha256 as built `{wl['sha256_as_built']}`** ({wl['built']}); the version-1 builds (`e2e6de67…`, `b21445f6…`) superseded, never judged, kept in `build/superseded/`. Reduced design: modal template of A `{dz['modal_template']}` ({dz['template_forms'][dz['modal_template']]} of {n_a}); checked set {dz['n_checked']} = B {n_b} + off-template A {len(dz['off_template_A'])} (`{'`, `'.join(dz['off_template_A'])}`) + a seeded {dz['sample_n']} of the conforming A (seed {dz['sample_seed']}); reserve {dz['n_reserve']} conforming A rows, checked in full only if a sampled row fails. Tabs `seed42`, `seed4242`, `reserve_seed42`, `reserve_seed4242`, `CRITERIA`; the AI-assisted line at the top of every tab (\"{wl['ai_assisted_line']}\"); {len(wl['locked_cells'])} locked cells hashed in `build/workbook_lock_r121.json`. The returned workbook's sha256, verdict counts, second-seed rows and drops fill this row at Phase 2. |",
         f"| **AUX-CF2-IX-LEAK** (v2) | `results/leakscreen_ix.json` (served `{', '.join(lk['meta']['served_models'])}`): " + "; ".join(f"**{k}** {c['n_correct']} of {c['n']} correct, {c['n_non_unknown']} non-UNKNOWN, {c['n_parse_failures']} parse failures, **{c['verdict']}**" for k, c in cells.items()) + f". Registered cells A (v2 summary) and B (v3 summary) both PASS. ${lk['meta']['usd_total']:.4f}. The version-1 screen kept as `results/leakscreen_ix_v1_superseded.json`. |",
         f"| **AUX-CF2-IX-SPEND** (Phase 1, cumulative) | OpenAI, token-metered at list price: version 1 (drafting $0.0435 + lineage 2 $0.0218 + screens $0.0491) $0.1144 + version 2 (primary ${pm['usd']:.4f} + lineage 2 ${l2['usd']:.4f} + screen ${lk['meta']['usd_total']:.4f}) ${pm['usd'] + l2['usd'] + lk['meta']['usd_total']:.4f} = **${0.1144 + pm['usd'] + l2['usd'] + lk['meta']['usd_total']:.4f}** of the 4 USD cap; Anthropic $0. Not an invoice. |",
         ]
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
