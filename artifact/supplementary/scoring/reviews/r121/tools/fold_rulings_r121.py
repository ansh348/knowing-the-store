# -*- coding: utf-8 -*-
"""fold_rulings_r121.py -- fold the author's nine rulings of 2026-09-19 on PHASE0_REPORT.md into the registration draft.
Run once; every replacement is asserted to match exactly once. No call."""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
P = ROOT / "reviews" / "r121" / "registrations_draft" / "ADDENDUM_CF2_INTENT_CROSSOVER.md"
s = io.open(P, encoding="utf-8").read()

EDITS = [
    ("Registration for the author's freeze (program R121; drafted 2026-09-19 BEFORE any call; Phase 0 draft, to be frozen at Phase 2 after the author's rulings and the author's check of the crossed questions).",
     "Registration for the author's freeze (program R121; drafted 2026-09-19 BEFORE any call; the author's nine rulings on `reviews/r121/PHASE0_REPORT.md` folded in on 2026-09-19 before Phase 1; to be frozen at Phase 2 after the author's check of the crossed questions)."),
    ("Seed 42 is the primary draft and seed 4242 the one fallback; both are drafted for every pair up front (236 calls) so that the author's check reads one workbook.",
     "Seed 42 is the primary draft and seed 4242 the one fallback; both are drafted for every pair up front (236 calls) so that the author's check reads one workbook (ruling 5)."),
    ("**Author check (disclosed as such), all 118 pairs, before any monitor call.** A workbook (`reviews/r121/build/AUTHOR_CHECK_R121.xlsx`, sha256 recorded at build and again as returned) lists, per pair, the original question and the seed-42 crossed question, with four YES/NO columns:",
     "**Author check (disclosed as such), all 118 pairs, before any monitor call.** One workbook, two tabs (`reviews/r121/build/AUTHOR_CHECK_R121.xlsx`, sha256 recorded at build and again as returned): tab `seed42` lists, per pair, the original question and the seed-42 crossed question; tab `seed4242` the seed-4242 question for the same pairs, consulted only for the rows the author failed on the first tab, and the workbook says so at its top. The author judges all 118 seed-42 questions first and never chooses between two passing candidates; the rows that used the second seed are recorded (AUX-CF2-IX-CHECK). Each tab carries four YES/NO columns:"),
    ("(iii) it names no stored value (the value of the attribute as the pair's entry text or its PN successor records it; naming the slot's topic as the attribute path names it is allowed, the CF renderer's own rule);",
     "(iii) it names no stored value (the value of the attribute as the pair's entry text or its PN successor records it; naming the slot's topic as the attribute path names it is allowed, the CF renderer's own rule; ruling 3);"),
    ("A question passes only on four YES. The seed-4242 question is checked, by the same four columns, only where the seed-42 question fails; a pair whose fallback also fails, or whose fallback is byte-identical to the primary, is **dropped**.",
     "A question passes only on four YES. A pair whose fallback also fails, or whose fallback is byte-identical to the primary, is **dropped**."),
    ("is run on the crossed questions: population A, 30 PRESENT versions drawn by `random.Random(42).sample` from the passing pairs sorted by item_id, under v2; population B, all its passing PRESENT versions under v3. A leak is a STOP.",
     "is run on the crossed questions in Phase 1, before the author's check (ruling 6): population A, 30 PRESENT versions drawn by `random.Random(42).sample` from the 88 sorted by item_id, under v2; population B, all 30 PRESENT versions under v3. The registered cells screen the seed-42 questions; the seed-4242 questions of the same items are screened beside them so that a row that later uses the second seed is covered. A leak in any cell is a STOP (`reviews/r121/tools/ix_leakscreen.py`, `cf2/results/leakscreen_ix.json`)."),
    ("\"Two worked examples.\" becomes \"Three worked examples.\" No other wording changes; `USER_INDEXED` is P0's.",
     "\"Two worked examples.\" becomes \"Three worked examples.\" (ruling 2). No other wording changes; `USER_INDEXED` is P0's."),
    ("| Opus 5 | 3 (the multi-draw rule's minimum) | temperature unset, max_tokens 1024, Message Batches | `rows_OP5.jsonl` V2 (A), V3 (B), k = 5 | the same |",
     "| Opus 5 | **1** (ruling 1, design O2; the V2R-CAT draw-1 precedent, AUX-V2RCAT-A1-DRAW-EFFECT +0.0026 with both intervals including zero) | temperature unset, max_tokens 1024, Message Batches | `rows_OP5.jsonl` V2 (A), V3 (B), k = 5, **draw 1 used for the primary P0 reading** | the same |"),
    ("Draw collapse: the X4 rule (mean over ≥ 3 OK draws; a k = 1 lane its single draw). Where a recorded cell has five draws and its new partner three (Opus, P0 on A and B), the primary reading uses each cell's own collapse and a sensitivity row collapses the recorded cell over its draws 1 to 3 only.",
     "Draw collapse: the X4 rule (mean over ≥ 3 OK draws; a k = 1 lane its single draw). For Opus 5 under P0 the primary reading uses **draw 1** of the recorded five for cells 1 and 2, so that every Opus cell is one draw; the recorded five-draw means for cells 1 and 2 are the registered sensitivity row (ruling 1). Under P1 all four Opus cells are new and one draw each."),
    ("Thirty regular expressions, case-insensitive after NFKD folding, proposed from the instruction texts only:",
     "Thirty regular expressions, case-insensitive after NFKD folding, proposed from the instruction texts only and kept untuned (ruling 4):"),
    ("Failure text: \"P-I3 FAILS: the name lookup reads $A$ on population $X$; the crossed wording moves its cosine.\"",
     "Failure text: \"P-I3 FAILS: the name lookup reads $A$ on population $X$; the crossed questions are $\\Delta$ content tokens longer than the originals on average, and dilution of the cosine by the longer wording, not intent, is the likely reason.\" (ruling 8: the question-length difference, in `e0_common.toks` content tokens and in characters, prints beside the lookup's row in every branch, AUX-CF2-IX-LOOKUPS)."),
    ("Caps: **Anthropic 16 USD, OpenAI 4 USD** (the balance table of ADDENDUM_V2R_CAT_AMENDMENT_2 §7), token-metered from the rows",
     "Caps: **Anthropic 15 USD, OpenAI 4 USD** (ruling 1), token-metered from the rows"),
    ("[The design as run is fixed by the author's ruling on the Phase 0 report; the projection table is there.] Order:",
     "Design O2 as ruled: 708 new units per reader (Luna 768), Opus one draw, Haiku and Luna five, mini one; projection **Anthropic $11.45 expected, $14.88 at ×1.3, $13.20 at the p95 outputs; OpenAI $1.90 with the cache, $3.06 without, $3.98 at ×1.3 of the no-cache reading** (`results/projection_r121.json`, design O2). Order:"),
    ("## §11: Ledger and paper site\n\n`cf2/NUMBERS_CF2.md` section 14:",
     "## §11: Ledger and paper site\n\nRuling 7: the ledger and the rows live with the counterfactual set. `cf2/NUMBERS_CF2.md` section 14:"),
    ("Paper: Section 5, Limitations, Appendix C.2 (`tab:cf-intent`), Appendix E.3, the abstract in the P-I2-fails branch.",
     "Paper: Section 5, Limitations, Appendix C.2 (`tab:cf-intent`), Appendix E.3, the abstract in the P-I2-fails branch. Ruling 9: this session never edits `reviews/v21/` or `reviews/r120/`; the held texts with their numbers filled are delivered as `reviews/r121/HELD_TEXTS_R121.md`, and the main session lands them on the author's ruling; every commit uses a private index and explicit pathspecs."),
]
for old, new in EDITS:
    assert s.count(old) == 1, old[:70]
    s = s.replace(old, new)
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("folded", len(EDITS), "edits")
