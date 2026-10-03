# ADDENDUM_DS — Amendment 1 (D-DS-3 repair): the fetch gate elicited under the all-states summary, a descriptive policy

Written 2026-09-13 (program R103), BEFORE any call, as a separate file because `verify_ds.py`
check A pins `registrations/ADDENDUM_DS.md` byte-identical to `a5a2036`. **Descriptive: no bar,
no prediction, no verdict; DS-P4's FAILS verdict is never re-adjudicated** (D-DS-3 (b), the
author's disposition of 2026-09-13: "The repair is DS Amendment 1: a v3-elicited gate — mini's
obligation score elicited under the all-three-named summary (index_v3) on the 661, thresholded at
the same base rate — driving the MODEL-ALL fetch, registered as a descriptive lane (no bar)").
Every number prints whichever way it comes out. Frozen by sha256 before the first call (CLAIMS.md
R103 block; `ds_downstream/NUMBERS_DS.md` section 6).

## §A1.1 — What is added, and what is not

ADDENDUM_DS §C.4 records that no v3 monitor row exists for the 661 and that the -ALL policies
therefore drive the fetch from the gate elicited under the superseded-only (v2) summary; §C.7
disclosed that DS-P4 could exceed 0.20 only if that gate fired on 9 of the 17 newly fetchable
records, and Phase B found it fired on 0 (AUX-DS-REACH; D-DS-3 (b)). This amendment elicits the
missing row and defines one further policy that reads it. Nothing in ADDENDUM_DS changes: the six
registered policies, their views, Stage 1 and Stage 2 rows, the five verdicts and the frozen
Section 7 paragraph stand as printed.

## §A1.2 — Elicitation (the 661 obligation calls)

**Population.** The 661 obligation items of the committed cell (`ds_common.load_cell`: 661 / 104
PN = 63 supersession / 26 retraction / 15 expiry; 174 PRESENT; 383 ABSENT), asserted as in
verify_ds check B.

**Summary.** For each item, `index_v3.render_v3` on `index_v2.view` of the item's store variant,
the CF-2 renderer that ADDENDUM_DS §C.4 already locks: its v2 prefix is byte-identical to the
committed TRUE text (asserted 661 / 661), and it appends the two sections `ATTRIBUTE NAMES CARRYING
RETRACTED CONTENT` and `ATTRIBUTE NAMES CARRYING EXPIRED CONTENT` in v2's own name-block grammar
(`ds_common.names_for(it)[1]`). The names those sections print are exactly the N3 fetch set the
MODEL-ALL policy already uses.

**Protocol.** `gpt-4.1-mini` pinned (`prompts_e1.MODEL`), `prompts_e1.SYSTEM` and
`prompts_e1.USER_INDEXED` verbatim (digests `337d37d3…` / `35d9b968…` asserted at import),
temperature 0, seed 42, max_tokens 200, JSON mode, k = 1, one retry on a parse failure (the E1
clamp), the main-study protocol the CF-2 INDEXED-V3 arm used; through `e1_metamemory/tools/api.py`
with the cache redirected to `ds_downstream/cache_amend1/` (arm name `INDEXED-V3`). Served
identifier probed before launch (E1.7 rule). One call returns both judgments; `nok` is the gate
score (`nok3_i`), `fok` is recorded and not used by any gate.

## §A1.3 — The added policy

**MODEL-ALL-V3** (paper name: *Model rule, all states named, gate elicited under that summary*):
fetch gate `nok3_i ≥ θ_NOK` with θ_NOK = 104 / 661 = 0.157337, the base rate on the probability
scale exactly as ADDENDUM_DS §C.5 reads it (ruling R1); fetch set `N3_i` (the v3 names, as
MODEL-ALL); abstention `fok_i < θ_FOK` on the committed v2 coverage score, as MODEL and MODEL-ALL,
so that the fetch gate is the only thing that changes. Views are assembled by
`ds_common.assemble_view` (the five L2 lines byte-identical, then the fetched non-active records in
ascending (slot, entry id) order, ranks continuing); where the v2 gate also fires the view is
byte-identical to MODEL-ALL's, and the Stage 2 answer is shared through the cache key.

## §A1.4 — What is computed ($0 after the elicitation, deterministic)

- **The v3 monitor row (descriptive).** AUROC of `nok3` on the 661 and per state (positives of one
  state against the same 557 negatives); the paired difference v3 minus the committed v2 `nok`
  (item-level and persona-clustered paired bootstrap, 1,000 draws, seed 42); the number of distinct
  values `nok3` takes; flag counts of `nok3 ≥ θ_NOK` by label (PN / PRESENT / ABSENT) beside the
  committed gate's 75 = 56 / 9 / 10.
- **Stage 1 for MODEL-ALL-V3**, in the row format of AUX-DS-REACH, AUX-DS-PRESENT, AUX-DS-ABSTAIN
  and AUX-DS-VIEWSIZE: gate fires, abstentions, PN reach whole and per state with the Wilson
  interval, tagged reach, successor in view, PN abstained, PRESENT coverage of 174, ABSENT
  abstention of 383 and 272, view sizes.
- **The DS-P4 quantity, descriptive:** MODEL-ALL-V3 reach minus MODEL reach on the 41 retraction-
  and expiry-derived items, with both intervals (`build_ds.pdiff`); the number of the 17 newly
  fetchable records the v3 gate fires on; MODEL-ALL-V3 minus MODEL on the 104. No bar is applied.
- **Stage 2 for MODEL-ALL-V3**: one `gpt-4.1-mini` answer call per distinct (item, view) not already
  answered in `ds_downstream/run/rows_ds.jsonl` (the DS cache is read first; only views no
  registered policy assembled are new calls), `prompts_ds.SYSTEM_ANSWER` / `USER_ANSWER` verbatim,
  scored by the committed detector exactly as `run_ds.score_answer`: stale use at TAU_HI and
  TAU_GOLD split by tagged / untagged reach, stale surfacing, successor use, both, PRESENT
  correctness. Rows in `ds_downstream/run/rows_ds_amend1.jsonl`.

## §A1.5 — Budget and STOP

Cost line: this amendment and the Q4 probe together are capped at **$3.00** by the author. The
runner projects the 661 elicitation calls from the probe's token counts (the v3 summary is the
longest input in the program) and the Stage 2 calls from the DS probe's figure, prints both beside
the cap, and refuses to launch if the two runs' projections together exceed it; the client's hard
cap is set to $3.00 on the namespace. STOP: served-identifier mismatch; elicitation failures after
the retry on more than 2% of items; projection over the cap; any assertion of §A1.2 failing.

## §A1.6 — Ledger and paper site

`ds_downstream/NUMBERS_DS.md` gains section 6 with keys `AUX-DS-A1-PROBE`, `-PROJECTION`, `-LOCK`,
`-V3ROW`, `-GATE`, `-REACH`, `-PRESENT`, `-ABSTAIN`, `-VIEWSIZE`, `-P4DESC`, `-STAGE2`, `-SPEND`;
`ds_downstream/DEVIATIONS_DS.md` D-DS-3 (b) gains a dated paragraph recording that the amendment
ran and what it found. Paper: one row in the downstream block of Table 4 (`tab:routes`) and in both
blocks of `tab:ds`, one sentence in Section 8 in place of "the repair is under way", and the
account in Appendix F.10. `verify_ds.py` is unaffected (it checks the registered artifacts and
does not read the amendment's files).

## Registration mechanics

Frozen by sha256 before the first call (recorded in CLAIMS.md R103 and NUMBERS_DS.md section 6).
Copied to `iclr2027_monitoring_submission/ARTIFACT/registrations/ADDENDUM_DS_AMENDMENT_1.md`.
Further amendments append dated sections and never edit the text above.
