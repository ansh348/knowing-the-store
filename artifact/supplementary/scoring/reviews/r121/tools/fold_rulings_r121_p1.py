# -*- coding: utf-8 -*-
"""fold_rulings_r121_p1.py -- fold the author's three rulings of 2026-09-19 on PHASE1_REPORT.md into the registration draft.
Run once; every replacement is asserted to match exactly once. No call."""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
P = ROOT / "reviews" / "r121" / "registrations_draft" / "ADDENDUM_CF2_INTENT_CROSSOVER.md"
s = io.open(P, encoding="utf-8").read()

EDITS = [
    # header: the rulings on the Phase 1 report
    ("the author's nine rulings on `reviews/r121/PHASE0_REPORT.md` folded in on 2026-09-19 before Phase 1; to be frozen at Phase 2 after the author's check of the crossed questions). Carries four predictions (P-I1 to P-I4) with failure texts and one descriptive reading (P-I5).",
     "the author's nine rulings on `reviews/r121/PHASE0_REPORT.md` folded in on 2026-09-19 before Phase 1, and the three rulings on `PHASE1_REPORT.md` after it; to be frozen at Phase 2 after the author's check of the crossed questions). Carries three predictions (P-I1, P-I2, P-I3) with failure texts and two descriptive readings (P-I4, demoted by the Phase 1 ruling because its outcome is fixed by the construction, and P-I5)."),
    # §3 renderer: the second lineage
    ("Seed 42 is the primary draft and seed 4242 the one fallback; both are drafted for every pair up front (236 calls) so that the author's check reads one workbook (ruling 5).",
     "Seed 42 at temperature 0 is the primary draft. The one fallback is a **registered second lineage** (Phase 1 ruling 2): the same instruction and model, **temperature 0.7, seed 4242**, one question per pair, through the same automatic gate and the same leak screen (lineage sha256 `LINEAGE2_SHA` over the same seven fields with the temperature 0.7). Both are drafted for every pair up front so that the author's check reads one workbook (ruling 5). An earlier fallback at temperature 0 and seed 4242 was byte-identical to the primary on 98 of 118 pairs (AUX-CF2-IX-QUESTIONS) and is superseded by the lineage; its rows stay in the questions file as a record (`fallback_t0_superseded`). The lineage stays cue-bearing on purpose, so the population remains homogeneous; a cue-free population is an open item, not part of this registration."),
    ("tab `seed4242` the seed-4242 question for the same pairs, consulted only for the rows the author failed on the first tab, and the workbook says so at its top.",
     "tab `seed4242` the second lineage's question (temperature 0.7, seed 4242) for the same pairs, consulted only for the rows the author failed on the first tab, and the workbook says so at its top."),
    ("A pair whose fallback also fails, or whose fallback is byte-identical to the primary, is **dropped**.",
     "A pair whose fallback also fails, or whose fallback is byte-identical to the primary (reported, not greyed), is **dropped**."),
    ("The registered cells screen the seed-42 questions; the seed-4242 questions of the same items are screened beside them so that a row that later uses the second seed is covered.",
     "The registered cells screen the seed-42 questions; the second lineage's questions of the same items are screened beside them, as cover cells with the same rule, so that a row that later uses the fallback is covered."),
    # §7 estimands: the pooled descriptive row
    ("- **Model against a lookup** (P-I4): the paired difference of same-store AUROCs, `cf2_score.paired` (item-level and persona-grouped), the model minus the keyword-intent lookup on the same cells.",
     "- **Model against the keyword-intent lookup** (P-I4, descriptive): the paired difference, `cf2_score.paired` (pair-clustered and persona-grouped), the model under P1 minus the keyword-intent lookup, on the same-store estimand (where the lookup sits at the ceiling by construction, AUX-CF2-IX-CUES) and, as the registered descriptive row of the Phase 1 ruling, **on the pooled estimand** (cell 1 against cells 2 to 4), each model under P1 beside the lookup with both intervals."),
    # §8 predictions: P-I4 demoted
    ("- **P-I4.** Under P1, at least one model exceeds the keyword-intent lookup on population A, both intervals excluding zero. Failure text: \"P-I4 FAILS: the cue list alone matches the models: keyword-intent lookup $L$, the best model $A$, difference $D$ with intervals $I_{pair}$ and $I_{persona}$.\"",
     "- **P-I4** (descriptive, demoted by the Phase 1 ruling; no failure text). The crossed questions were drafted from an instruction that offers cue wordings, so the fixed cue list identifies their intent on every one of them (118 of 118 at both lineages' drafting) and sits at the ceiling on the same-store estimand; on these questions a model can at best match the cue list. The row prints each model under P1 beside the keyword-intent lookup on the same-store and on the pooled estimand, both intervals."),
    # §9 held texts: the P-I4 sentence
    ("  - P-I4 fails, in any branch: \"…a lookup that zeroes questions with past or change wording matches the models ($L$).\"",
     "  - P-I4 (descriptive), in every branch, replaces the lookup clause: \"The crossed questions were drafted from an instruction that offers cue wordings, so a fixed cue list identifies their intent on every one of them and sits at the ceiling on the same-store estimand; on these questions a model can at best match the cue list, and on the pooled estimand the models read $A_{1..4}$ against the lookup's $L$.\""),
    ("The name lookup cannot separate them; a lookup that zeroes questions with past or change wording reads $L$.\"",
     "The name lookup cannot separate them.\""),
    # §10 order: the lineage's cells in the lock
    ("Order: lock (registration sha256, P0 digests, P1 sha256, cue-list sha256, questions sha256, workbook sha256)",
     "Order: lock (registration sha256, P0 digests, P1 sha256, cue-list sha256, the questions' sha256 at both lineages, the workbook's sha256 as built and as returned)"),
]
for old, new in EDITS:
    assert s.count(old) == 1, old[:70]
    s = s.replace(old, new)
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("folded", len(EDITS), "edits (LINEAGE2_SHA placeholder to fill after the drafting)")
