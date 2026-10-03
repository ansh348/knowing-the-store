# ADDENDUM_V2R_CAT Amendment 1: Opus 5 on the moved-count texts at five draws (E1)

Registration for the author's freeze (program R117; drafted 2026-09-18 BEFORE any call, the author's rulings of 2026-09-19 folded in: cap 22 USD, draws 2 to 5 through Batch exactly like the recorded draw, max_tokens 1024, temperature unset). Carries one prediction (P-M1) with its failure text. Frozen by its sha256, recorded in `r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md` before the first call; the runner writes `rows/lock_op5_k5.json` with that hash at start. Nothing here re-adjudicates ADDENDUM_V2R_CAT, its rulings, or any CF-2 row; the recorded draw 1 and the recorded v2 rows are read and never re-run.

## §1: Why

Section 5 prints Opus 5's moved-count movement, $-0.10$ on retraction and $-0.12$ on expiry with both intervals excluding zero (AUX-V2RCAT-OP5), qualified as one draw against the recorded five-draw v2 row (D-V2RCAT-2, "draw-count noise the two registered lanes did not carry"). Drawing the four missing draws on the identical texts removes the qualifier or retracts the claim.

## §2: Population and the recorded rows

The 444 store versions of the counterfactual set (`r82_counterfactual/cf2/cf_cell.json`; 148 pairs: 88 supersession, 30 retraction, 30 expiry) under the V2R-CAT texts of `r82_counterfactual/v2rcat/build/texts_v2rcat.json` (texts sha256 `093f1d5839485e23…`, RENDERER LOCK asserted at build and re-asserted before any call). Recorded rows read, never re-run: draw 1 of this arm, `v2rcat/rows/rows_OP5.jsonl` (444 rows, arm `INDEXED-V2R-CAT`, `draw` 1, served `claude-opus-5`, 0 not OK); the comparator, the CF-2 Opus v2 row at k = 5, `cf2/rows/rows_OP5.jsonl` arm `INDEXED-V2` (2,220 rows; AUX-CF2-OP5-V2 0.8405, the X4 collapse, gate re-asserted before scoring); the recorded totals-randomized row (v2r, k = 5) prints beside.

## §3: The run

Draws 2, 3, 4 and 5 on the byte-identical prompts of draw 1: `prompts_e1.SYSTEM` and `USER_INDEXED` with the V2R-CAT text as `{index}` (digests asserted at import by `run_cf.py`), `claude-opus-5`, temperature unset, `max_tokens` 1024, Anthropic Message Batches at the 0.5 multiplier, one Batch of 1,776 requests (`custom_id` `OP5-0-<unit index>-d<draw>`, the `run_cf.cmd_submit` form with draw 1 omitted), rows appended to `rows_OP5.jsonl` with `draw` 2 to 5 and `batch_id`; the resume key is (`unit_id`, arm, draw). Served identifier asserted on every row (E1.7 rule); a mismatch stops the lane. If the Batch is cancelled or expires, the missing draws are resubmitted once; rows never delivered are left absent and disclosed.

## §4: Estimands

The X4 collapse: per item the mean over its draws, MIN_DRAWS 3 (an item with fewer than three OK draws is excluded and counted). The registered V2R-CAT contrasts, unchanged: V2R-CAT (five-draw mean) minus the recorded v2 row (five-draw mean) on the whole set and per state, item-level and persona-grouped paired bootstrap intervals (1,000 draws, seed 42; `cf2_score.paired`), the weaker reading stated where they disagree; the band reading of ADDENDUM_V2R_CAT §5 re-stated at five draws; the reference readers unchanged (AUX-V2RCAT-REF). The five-draw row minus the draw-1 row prints beside as the draw effect.

## §5: Prediction

**P-M1.** On retraction and on expiry the five-draw V2R-CAT row is below the recorded five-draw v2 row, and both differences are reliable: both the item-level and the persona-grouped interval exclude zero, on both states.

Failure text, frozen: "P-M1 FAILS. At five draws the moved-count movement of Opus 5 does not replicate on [retraction / expiry / both]: the difference is $D$ with intervals $I_{item}$ and $I_{persona}$."

## §6: Held texts, both branches (land only by ruling; Phase 3)

- P-M1 HOLDS: Section 5's Opus sentence loses "run once per item against its five-draw row" and reads "Opus 5, at five draws against its five-draw row, moves $D_{ret}$ on retraction and $D_{exp}$ on expiry, both intervals excluding zero."; Section 1 L111 and L122 keep their content; the Conclusion's "Only Opus 5 responds to a moved count." stands.
- P-M1 FAILS: Section 5's Opus sentence reads "Opus 5's single-draw movement on the moved count did not replicate at five draws ($D_{ret}$ on retraction, $D_{exp}$ on expiry; Appendix C.2)."; Section 1 L111 and L122 lose the count-response clause; the Conclusion sentence "Only Opus 5 responds to a moved count." is deleted. In both branches Appendix C.2's `tab:v2rcat` row for Opus 5 reads k = 5 with the draw-1 row kept beside it.

## §7: Budget, order, STOP

Projection from the recorded draw-1 Batch rows (388 rows at $0.00909 per call, mean input 2,414 tokens, mean output 244; Anthropic list $5 / $25 per million, Batch 0.5): 1,776 calls, **expected $16.16**; at the p95 output of 417 tokens $19.98; the repo's ×1.3 launch margin gives $21.0 against the **cap of $22** (the author's ruling of 2026-09-19). Hard stop in the runner at the cap. Order: lock → the texts' sha256 re-asserted → the v2 gate (0.8405) → submit → poll → score. STOP: registration sha256 mismatch; texts sha256 mismatch; served-identifier mismatch; more than 2% of rows not OK after one resubmission; a projection over the cap.

## §8: Ledger and paper site

`r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md` section 9: `AUX-V2RCAT-A1-LOCK`, `-A1-OP5-K5` (the five-draw row, both contrasts, both intervals, per state), `-A1-DRAW-EFFECT`, `-A1-P-M1` (HOLDS / FAILS with the filled text), `-A1-SPEND`. Paper: Section 5's Opus sentence, Section 1 L111 / L122, the Conclusion (Phase 3 landing map), `tab:v2rcat`.

## Registration mechanics

Frozen by sha256 before the first call. Copied to `iclr2027_monitoring_submission/ARTIFACT/registrations/`. Amendments, if any, are appended as dated sections below the marker line and never edit the text above. The run proceeds on the author's freeze commit; nothing runs before it exists.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
