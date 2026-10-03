# ADDENDUM_BELIEVED_H: descriptive: Haiku 4.5 under the lifecycle store's own metadata (the BELIEVED summary), capped and lifted renderings

DRAFT for the author's freeze (CC_PASS_v18 section 2, R-A; drafted 2026-09-14 in Phase 1, BEFORE any call; not frozen, not run). Descriptive: this addendum carries **no prediction, no bar and no verdict**; every number prints whichever way it comes out, and the three branches of §4 name the abstract wording each forces. It is frozen by its sha256, recorded in `believed_h/NUMBERS_BELIEVED_H.md` before the first call. Nothing here re-adjudicates a recorded row: the GPT-4.1 mini rows under both renderings, the lookup's capped row and Haiku 4.5's blind and truthful rows are read and never re-run.

## §1: Why, and what is already recorded

Review ten (W7, W8, Q7): the retention figures the paper prints under the store's own metadata (42.3% capped, 65.5% lifted; `e1r_robustness/NUMBERS_E1R.md` AUX-E1R-BELIEVED-NOK, `side_experiments/NUMBERS_SIDE.md` AUX-SIDE-S2-MINI) have GPT-4.1 mini's indexed-minus-blind difference as their denominator, and that difference is not a gain (its blind score is one value on 604 of the 661 questions). The abstract's "every reader falls to near chance" rests on one model and the lookup. Haiku 4.5 has a blind row that varies (0.4150) and a truthful row (0.8210; `r74/NUMBERS_R74.md` AUX-R74-X4-H45-NOK, k = 5, temperature 0), so its retention is a ratio of two gains. This addendum runs Haiku 4.5 under the BELIEVED summary in both recorded renderings and reports its retention; the paper's levels table (Section 3.5 of the pass) carries its percentage, and mini's two figures move to Appendix E.9 with the caveat that their denominator is not a gain.

Recorded and read, never re-run: mini BELIEVED capped 0.5959, lifted 0.6513 (`AUX-E1R-BELIEVED-NOK`, `AUX-SIDE-S2-MINI`); the embedding lookup on the capped list 0.5858 (`AUX-E1R-NB6`); Haiku 4.5 blind 0.4150 and truthful 0.8210 (`r74/x4/rows_H45.jsonl`, arms BLIND and INDEXED-TRUE).

## §2: Population and texts

The full obligation set: the 661 obligation questions (104 PRESENT-NEGATIVE) of `r74/x4/cell_661.json`, the population every Haiku 4.5 row above was scored on. Two summary texts per item, both recorded:

- **BELIEVED-15 (capped):** the committed BELIEVED summary, `e1_metamemory/indexes_v2.json` `indexes[key]` with `key = item.index_key` and its `:TRUE` suffix replaced by `:BELIEVED` (rule 1's cap of fifteen names per category, the header note printed; `index_v2.render`, SLOT_CAP = 15; 281 frbank BELIEVED keys, of which the 661 items use 242).
- **BELIEVED-LIFTED (cap lifted):** the S2-U rendering, `side_experiments/s2/indexes_s2u.json` `indexes[items[i].index_key_s2u]` (the same renderer with SLOT_CAP lifted to 100; largest bucket 86, largest superseded set 50; renderer lock: the cap-15 render reproduces the committed BELIEVED text on 661 of 661; `registrations/ADDENDUM_SIDE.md` arm S2-U, settled reading in `NUMBERS_SIDE.md`).

Both texts are asserted at build to be byte-identical to the recorded files (sha256 of each file recorded under `AUX-BH-LOCK`), and the item-to-key map is asserted against `indexes_s2u.json` `items`. No text is rendered anew.

## §3: Arms, reader, prompts

Arms: INDEXED-BELIEVED-15 and INDEXED-BELIEVED-LIFTED, 661 items each. Reader: Haiku 4.5 (`claude-haiku-4-5-20251001`), **k = 5, temperature 0, max_tokens 200, Message Batches**, the X4 collapse (dedup on draw, at least three draws, arithmetic mean), exactly its recorded protocol on the 661. Prompts `prompts_e1.SYSTEM` / `USER_INDEXED` verbatim, digests asserted at import through `run_cf.py` (the recipe of `pad_probe/tools/contam.py` and `r82_counterfactual/cf3/cf3_run.py`: `run_cf`'s module globals re-pointed, nothing else). Blind is the recorded BLIND arm of `r74/x4/rows_H45.jsonl`; no blind call is made. The served identifier is probed before each lane (E1.7 rule; a mismatch is a STOP). Rows under `believed_h/rows/rows_H45.jsonl`, arms named as above. **The lookup ($0):** the superseded-names embedding lookup (`score_cf.matcher`, all-MiniLM-L6-v2) on the lifted list, the list parsed from the S2-U text by `index_v3.named_sections`; the capped value is recorded (0.5858) and reproduced as a gate.

## §4: Estimands and the three branches (descriptive)

Per rendering: Haiku 4.5's indexed AUROC (Mann-Whitney, ties at 0.5) with the item-level and persona-clustered intervals (1,000 draws, seed 42, single-class draws discarded; the persona is the cluster); the paired difference against its recorded truthful row (BELIEVED minus TRUE) and against its recorded blind row (BELIEVED minus blind), both intervals; **retention = (BELIEVED minus blind) / (TRUE minus blind)** with blind 0.4150 and TRUE 0.8210 fixed at their recorded values, the item and persona intervals of the ratio from the same bootstrap draws (the ratio of the paired resampled differences; a draw with a non-positive denominator is discarded and counted). Per state (positives of one state against all negatives) beside the whole set. The lookup on the lifted list with both intervals, and Haiku minus lookup under each rendering.

The sixty-percent line is read as the main-study preregistration fixed it for coverage on 2026-08-10 (`e1_metamemory/PREREG_E1.md`, H-BELIEVED, report-only) and as `e1r_robustness/SPEC_E1R.md` inherited it for the obligation judgment; no reason for the value was recorded and none is supplied here. Three branches, one of which prints; each names the abstract wording it forces (CC_PASS_v18 R-A):

- **Retention below 60% under both renderings.** The abstract keeps "under the lifecycle store's own metadata the readers we test fall near chance" only if Haiku 4.5's BELIEVED level is at or below 0.60 under both renderings; otherwise it says "fall by X", X the larger of the two drops from 0.8210.
- **At or above 60% under the lifted rendering only.** The abstract says "the smallest model and the lookup fall near chance under the store's own metadata; a larger model keeps more of its gain once the renderer's cap is lifted."
- **At or above 60% under both.** The abstract says "the smallest model and the lookup fall near chance; the larger model keeps X of its gain", X the capped retention.

Nothing holds or fails. The paper's levels table (TRUE, BELIEVED capped, BELIEVED lifted for mini, Haiku 4.5 and the lookup) carries Haiku's retention percentage only; mini's 42.3% and 65.5% stay in E.9 with their frozen texts and the denominator caveat. Opus 5 and Luna under BELIEVED are listed in Section 6 as discussion-period runs.

## §5: Budget, lane order, STOP

Projected from the recorded Haiku 4.5 per-call actual on the counterfactual set (`AUX-CF2-SPEND`: $9.0623 over 7,400 Batch calls, $0.001225 per call at about 4,300 characters of summary): the capped lane 3,305 calls ≈ $4.05; the lifted lane 3,305 calls at about 1.35 times the input (5,939 against 4,384 characters mean) ≈ $5.30; probes ≈ $0.01; **≈ $9.4 against the cap of $12 (×1.3: $12.2)**. Each lane is probed and its projection printed before submission; the lifted lane runs first (the body reports the lifted rendering as the store's full self-description); the capped lane runs if the remaining headroom under $12 covers its projection at ×1.3, and otherwise prints a dash with the projection beside it, the author's call. Total new spend under the pass stays under $40 on Anthropic. STOP: registration sha256 mismatch; either text file's sha256 differing from `AUX-BH-LOCK`; the item-to-key map failing; a served-identifier mismatch; elicitation failures after the retry on more than 2% of a lane's rows; the lookup's capped value not reproducing 0.5858 at four decimals; a projection over the cap.

## §6: Ledger and paper site

`believed_h/NUMBERS_BELIEVED_H.md`: `AUX-BH-LOCK`, `AUX-BH-PROBE`, `AUX-BH-PROJECTION`, `AUX-BH-H45-15`, `AUX-BH-H45-LIFTED` (levels, paired differences, per state), `AUX-BH-RETENTION-15`, `AUX-BH-RETENTION-LIFTED` (with both intervals and the discarded-draw count), `AUX-BH-LOOKUP-LIFTED`, `AUX-BH-BRANCH`, `AUX-BH-SPEND`; the file enters `trace_scan_v13`'s LEDGERS. Paper: the levels table of Section 7 (Section 3.5 of the pass: Table 4 after the split), the abstract clause the branch forces, one sentence in Section 4 on the cap and the sixty-percent line. No frozen number and no frozen text changes.

## Registration mechanics

Frozen by sha256 before the first call (recorded in `NUMBERS_BELIEVED_H.md`). Copied to `iclr2027_monitoring_submission/ARTIFACT/registrations/ADDENDUM_BELIEVED_H.md`. Amendments, if any, are appended as dated sections below the marker line and never edit the text above. The run proceeds on the author's freeze commit; nothing runs before it exists.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
