# -*- coding: utf-8 -*-
"""finalize_registration_r121.py -- fold the author's check outcome (verdicts_r121.json) and the final populations into the
registration draft before the freeze. Asserted whole-line and substring replacements; every number read from the artifacts. No call."""
import io
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
P = ROOT / "reviews" / "r121" / "registrations_draft" / "ADDENDUM_CF2_INTENT_CROSSOVER.md"
V = json.load(io.open(ROOT / "reviews" / "r121" / "build" / "verdicts_r121.json", encoding="utf-8"))
W = json.load(io.open(ROOT / "reviews" / "r121" / "build" / "workbook_lock_r121.json", encoding="utf-8"))
PR = json.load(io.open(ROOT / "reviews" / "r121" / "results" / "projection_r121_final.json", encoding="utf-8"))
Q = json.load(io.open(ROOT / "reviews" / "r121" / "build" / "cross_questions.json", encoding="utf-8"))["meta"]
c = V["counts"]; e = PR["expected"]
s = io.open(P, encoding="utf-8").read()


def rep(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


rep("and the three rulings on `PHASE1_REPORT.md` after it; to be frozen at Phase 2 after the author's check of the crossed questions).",
    "and the three rulings on `PHASE1_REPORT.md` after it; deviation D-IX-1 of `reviews/r121/DEVIATIONS_R121.md` applied; the author's check returned on 2026-09-19; **frozen 2026-09-19 (Phase 2) before any monitor call**).")
rep("**Retraction** (30 pairs) is out of scope: the grid gives it no licensed intent. In scope: 118 pairs, 40 personas.",
    f"**Retraction** (30 pairs) is out of scope: the grid gives it no licensed intent. Drafted: 118 pairs, 40 personas. **In scope after the author's check (§3): {c['A_pass'] + c['B_pass']} pairs, population A {c['A_pass']} of 88 and population B {c['B_pass']} of 30**; the five drops and the two second-lineage rows are listed in §3.")
drops = "; ".join(f"row {d['n']} `{d['pair_id']}` ({d['reason']}; the author's note: \"{d['note']}\")" for d in V["drops"])
second = "; ".join(f"row {x['n']} `{x['pair_id']}` (seed 42 {x['seed42_failure']}, \"{x['note']}\"; the lineage-2 question \"{x['question']}\")" for x in V["second_lineage"])
notes = "; ".join(f"row {n}: \"{t}\"" for n, t in V["notes_on_passing_rows"].items())
rep("A conforming A pair in the reserve that is never checked is taken as passing under the sampled 20 (the reduced design); if any sampled row fails, the reserve is checked in full. The verdicts are the author's; the workbook is the record.",
    "A conforming A pair in the reserve that is never checked is taken as passing under the sampled 20 (the reduced design); if any sampled row fails, the reserve is checked in full. The verdicts are the author's; the workbook is the record.\n\n"
    f"**Outcome (2026-09-19; `build/verdicts_r121.json`).** Workbook as built (the disclosure line amended before any entry) sha256 `{W['sha256_as_built']}`; **returned `{V['returned_sha256']}`** (`build/AUTHOR_CHECK_R121_returned.xlsx`; the verdicts entered from the author's dictated list by `tools/enter_verdicts_r121.py`; all {V['locked_cells_verified']} locked cells verified against the lock). Checked set {c['checked']} rows: {c['pass_primary_checked']} pass on the seed-42 question, {c['second_lineage']} pass on the second lineage, {c['drops']} drop; the seeded 20 conforming A rows all pass, so the reserve ({c['reserve_unjudged']} rows) stays unjudged and passes under the design. "
    f"**Population A {c['A_pass']} of 88; population B {c['B_pass']} of 30; {c['A_pass'] + c['B_pass']} pairs in scope.** Drops (AUX-CF2-IX-DROPS): {drops}. Second lineage (AUX-CF2-IX-CHECK): {second}. Notes on passing rows: {notes}. Questions' sha256: primary `{Q['primary']['questions_sha256']}`, lineage 2 `{Q['lineage2']['questions_sha256']}`.")
rep("Per reader 708 new units (A: 88 × 6; B: 30 × 6), Luna 768.",
    f"Per reader {6 * (c['A_pass'] + c['B_pass'])} new units (A: {c['A_pass']} × 6; B: {c['B_pass']} × 6), Luna {6 * (c['A_pass'] + c['B_pass']) + 2 * c['B_pass']}.")
rep("Design O2 as ruled: 708 new units per reader (Luna 768), Opus one draw, Haiku and Luna five, mini one; projection **Anthropic $11.45 expected, $14.88 at ×1.3, $13.20 at the p95 outputs; OpenAI $1.90 with the cache, $3.06 without, $3.98 at ×1.3 of the no-cache reading** (`results/projection_r121.json`, design O2).",
    f"Design O2 as ruled, at the final populations: {6 * (c['A_pass'] + c['B_pass'])} new units per reader (Luna {6 * (c['A_pass'] + c['B_pass']) + 2 * c['B_pass']}), Opus one draw, Haiku and Luna five, mini one; calls Opus {e['calls']['opus']}, Haiku {e['calls']['haiku']}, mini {e['calls']['mini']}, Luna {e['calls']['luna']}; projection **Anthropic ${e['anthropic']:.2f} expected, ${e['anthropic_x1.3']:.2f} at ×1.3, ${PR['high']['anthropic']:.2f} at the p95 outputs; OpenAI for the run ${e['mini'] + e['luna_cache']:.2f} with the cache and ${e['mini'] + e['luna_nocache']:.2f} without, on top of Phase 1's $0.2044** (`results/projection_r121_final.json`).")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("finalized")
