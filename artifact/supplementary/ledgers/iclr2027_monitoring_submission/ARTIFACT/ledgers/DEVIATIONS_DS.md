# DEVIATIONS_DS — deviations ledger for the downstream experiment DS

Registration: `registrations/ADDENDUM_DS.md` (frozen at `a5a2036`, R100; baseline `43a094c`). Own
numbering from **D-DS-1**. Entries are dated; nothing here re-adjudicates a registered verdict. Entries: D-DS-1, D-DS-2, D-DS-3.

## D-DS-1 — the truthful metadata does not flag 22 of the 104 forbidding records; ORACLE's ceiling is 0.788 by construction

**What was found (Phase A, 2026-09-13, $0).** For each of the 104 PN items of the committed
obligation population, the `pn_members` entries — the records the label rule (`PersonaJoin.label`,
`e0_common.py:296`) calls forbidding — were checked against the TRUE lifecycle flags of
`index_v2.true_lifecycle` (`index_v2.py:206-252`), the join the committed TRUE index is rendered
from and the flags the retrieved lines of `ADDENDUM_RESP` §L2 print. Keyed by (persona, entry id),
at least one `pn_members` entry is flagged superseded, retracted or expired for **82 of 104**: 63 of
63 supersession-derived, **8 of 26 retraction-derived, 11 of 15 expiry-derived**. For the other
**22** (18 retraction-derived, 4 expiry-derived) no `pn_members` entry carries any TRUE flag.

**Why.** Two committed rules disagree on these states. `PersonaJoin._resolve` (`e0_common.py:256-294`)
admits a retraction fire at signal 1.0 for entries anchored to the original fact's session at
`TAU_GOLD` 0.50 (`_b2_session`) and for `is_retracted` bank entries covering the original fact at
0.50 (L284–290); `true_lifecycle` flags retracted only through `detect(original_fact, retraction)`
at `TAU_HI` 0.80. For expiry the label's `expired_neg` is the gold entries whose `event_time`
precedes the pinned cutoff (L276–277), while `true_lifecycle` flags expired through YAML
`status == expired` records at 0.50 token coverage. The label rule was frozen in E0, the index join
in E1; neither is changed.

**The 22 items** (10 distinct questions across variants; `AUX-DS-FLAGCENSUS` lists the ids):
retraction — `bruna_q06` (FULL, CAT-ABLATED, SLOT-ABLATED), `dariush_q04` (FULL, SLOT-ABLATED),
`fatima_q06` (FULL, SLOT-ABLATED), `ingrid_q04` (FULL, CAT-ABLATED, SLOT-ABLATED), `joonho_q04`
(FULL, SLOT-ABLATED), `mirri_q04` (CAT-ABLATED), `rosa_q06` (FULL, CAT-ABLATED, SLOT-ABLATED),
`valentina_q04` (FULL, SLOT-ABLATED); expiry — `david_q06` (FULL, CAT-ABLATED), `marcus_q10` (FULL,
CAT-ABLATED). Every one survives in its store variant; their slots are `project` (7 questions),
`trip`, `obligation`, `exam_date`.

**Ruling (the author, 2026-09-13): disclose, do not repair.** ORACLE is the oracle over the
store's truthful metadata, so its ceiling is **0.788 by construction**. The 22 forbidding records
the truthful summary cannot name are a store-side fact, consistent with the Conflate row of the
believed-state table (Table 24 in the v8 lineage, `tab:believed`, `paper_v8.tex:2177`: FR-Bank's
write path records retraction through the supersession mechanism, so its metadata cannot separate
retracted from superseded content), and they print as such; they retrieve as `lifecycle: active`,
and the paper says so.

**What this changes in DS.** Nothing in the registered items: DS-P1 to DS-P5 stand as written.
Reach by id stays the registered quantity; **tagged reach** (the record in view *and* printed
non-active) prints beside it; the fetch sets under the v2 names reach 65 of 104 and under the
all-three names 82 of 104, and the draft §C.7 states the structural maxima this implies (ORACLE −
ALWAYS ≤ 0.788; MODEL-ALL − MODEL on the 41 counted-state items ≤ 0.415). Stage 2 rates print split
by tagged / untagged reach so that an answer given with an `active`-tagged forbidding record in
view is never pooled with one given under a non-active tag.

**What this touches outside DS (reported, not repaired here).** The TRUE index's LIFECYCLE TOTALS
and per-category RETRACT / EXPIRED counts do not count these 22 records; Table 21's per-state rows
(`tab:nb6-composition`) read the monitor on retraction / expiry items whose truthful summary does
not count their obligation; L2's retrieved lines will print these records as `active`. Whether a
line is added at those sites is the author's, outside this registration.

**What is NOT claimed.** That the label is wrong or the join is wrong: the two rules answer
different questions (is this record forbidden to use; does the store's own ground-truth join mark
it non-active), and the 22 are where the answers differ.

**Disposition.** Disclosed in `ADDENDUM_DS` §C.3 and §PAPER (the Section 7 paragraph's second
sentence and the `tab:ds` note); pinned by `verify_ds.py`; ledgered under `AUX-DS-FLAGCENSUS`.

*Landed 2026-09-13 at Phase B step 1, verbatim from `reviews/DS_REG_REPORT.md` Appendix B (ruling of
2026-09-13).*

---

## D-DS-2 — the frozen §C.4 table prints 22 in the zero column of F(P); the recomputation gives 10

**What happened (2026-09-13, Phase B step 1, $0).** `ADDENDUM_DS.md` §C.4, the fetch-set table, row
`F(P) (ORACLE, pn slots) | 104 PN | 22 (§C.3) | 2 | 2.64 | 7 | 8`: the "zero" cell says 22, with a
pointer to §C.3. Re-deriving the fetch sets at build (`ds_common.fetch` over the pn slots of each PN
item) gives **10** items whose F(P) is empty; the median (2), mean (2.64), p90 (7) and max (8) of the
same row reproduce exactly, as do every other cell of the table and the reach rows (F(P) reaches the
forbidding record for 82 of 104, as §C.3 states).

**Why.** The 22 is the number of PN items whose forbidding record carries no TRUE flag (§C.3, D-DS-1),
transcribed into the zero column as if an unflagged record implied an empty fetch set. It does not:
twelve of those 22 items have *other* flagged entries under the same slot (for example a superseded
`project` entry beside an unflagged retracted one), so their F(P) is non-empty while still not
containing the forbidding record. The Phase A census printed the F(P) distribution without its zero
count, and the draft filled the cell by inference.

**What this changes.** Nothing registered: no prediction, verdict, threshold or fetch rule reads the
zero count of F(P); ORACLE's reach and view sizes are computed from the fetch sets themselves.
`verify_ds.py` check C pins the recomputed row (mean 2.64, max 8) and prints the zero count as 10 with
a pointer here. The frozen text is not edited.

---

## D-DS-3 — two bars rest on the premise the study corrected at L2; one prediction was unfulfillable by its own gate (recorded 2026-09-13; nothing re-adjudicated)

Two parts, one entry. Neither moves a bar, a threshold, a verdict or a frozen text; both are
disclosures the paper carries, on the D93 precedent (`CLAIMS.md` CL-T-crossvendor: a defective
attachment struck, the registered gate and the failed verdict unchanged).

### (a) DS-P1 and DS-P2 were set under the inherited 5% premise, and RESP L2 measured the unmasked reach at 0.5192 before DS was scored

**What happened.** DS was frozen at `a5a2036` (R100, 2026-09-13) **before RESP Phase B ran, by
design**: the registration's header sequences DS Phase B after RESP step 4 and says so, and freezing
first kept the DS bars fixed before any L2 reach number existed. The bars for DS-P1 (ORACLE − ALWAYS
> 0.50) and DS-P2 (retention of the oracle gain ≥ 0.60 with the interval excluding the bar) were set
by the instruction under the inherited premise that the forbidding record enters a similarity view at
5% (`paper_v8.tex:137`, the FR paper's AV7 pass rate; `ADDENDUM_DS.md` §C.7 names it "L2-P3's
premise"). RESP L2 then measured the unmasked reach at k = 5 as **0.5192 (54 of 104)**
(`resp_review/NUMBERS_RESP.md` `AUX-RESP-L2-REACH`, step 4, commit `b08757c`, 2026-09-13), L2-P3
failed under its frozen text, and DS was scored after that (`ds_downstream/NUMBERS_DS.md` §2,
`AUX-DS-REACH`): DS-P1 = +0.4327 [+0.337, +0.529] (FAILS, under 0.50); DS-P2 ρ = 0.7561, item-level
[0.610, 0.872], persona-clustered [0.563, 0.939] (FAILS by the weaker reading). Both are the adverse
branch the registration wrote in advance (§C.7: "under L2's adverse branch it narrows exactly as the
instruction anticipates"; the retrieved view already carries the record for half the items).

**Disposition (the author, 2026-09-13).** The bars stand; the verdicts stand as printed. The paper
states the premise the bars were set under, following the D93 precedent: the attachment (the 5%
premise, since corrected by L2) is named as defective in the sentence that prints beside the DS
paragraph, and the gate is unchanged. The sentence, authorized in `CLAIMS.md` (R101 block): "The two
failed bars were fixed before the study measured the retrieval premise they rest on; the mechanism
numbers stand and the bars are printed as set." Table 25 carries the DS row with outcome "held /
failed" and the clause "two bars set under the 5% premise the study corrected at L2".

### (b) DS-P4 was structurally unfulfillable: the MODEL gate was elicited under a summary that names no counted-state attribute

**What happened.** DS-P4 (MODEL-ALL − MODEL > 0.20 on the 41 retraction- and expiry-derived items)
compares two policies that share one gate, mini's committed obligation score elicited under the
TRUE v2 summary — the summary that names superseded attributes and only counts the other two states
(`ADDENDUM_DS.md` §C.4: "the -ALL policies keep the committed v2-elicited gate and change only the
fetch set"; §C.7: the difference "exceeds 0.20 only if the committed gate fires on at least 9 of the
17 newly fetchable records"). The gate fired on **0 of the 17** (`AUX-DS-REACH`: MODEL-ALL 0.7805,
MODEL 0.7805, D = +0.0000 with both intervals [+0.0000, +0.0000]). The gate could not fire on those
items by construction: the score it thresholds was produced with no name for the counted states in
front of the model, and the committed post-hoc per-state monitor AUROC on those states is 0.5638 /
0.5110 (`AUX-E1R-NB6-COMPOSITION`). The registration disclosed the mechanism (§C.7, F5/F6 of the
Phase A report) and registered the bar as instructed; the frozen failure text names it ("The bound on
these states is the judgment, not the naming").

**Disposition (the author, 2026-09-13).** The verdict stands as printed (FAILS). **The repair is DS
Amendment 1: a v3-elicited gate — mini's obligation score elicited under the all-three-named summary
(`index_v3`) on the 661, thresholded at the same base rate — driving the MODEL-ALL fetch, registered as
a descriptive lane** (no bar; the DS-P4 verdict is never re-adjudicated). The amendment is to be
drafted, frozen by the author's commit and given GO before any elicitation; it is not written here.
Table 25's DS row carries "one prediction unfulfillable by its own gate (D-DS-3)".

**What this touches.** `paper_v9.tex` (R101): the Section 7 DS paragraph's authorized sentence, the
failures paragraph, Table 25's DS row, the deviation index. No ledger value, no threshold, no frozen
text of `ADDENDUM_DS.md` changes; `verify_ds.py` is unaffected.

**Amendment 1 executed (2026-09-13, R103; descriptive).** Drafted as `registrations/ADDENDUM_DS_AMENDMENT_1.md`
from the disposition above, in a separate file because check A pins `ADDENDUM_DS.md` byte-identical to
`a5a2036`; frozen by sha256 `72ab84dae2c7e464b1488570d4098aebf59b1de0d442ddc7b6f79a57bfcbbcf5` and copied
to `ARTIFACT/registrations/` before the first call (no registration file for it existed in the tree at the
start of the pass, so the pass wrote one from this disposition; recorded in `reviews/v11/CONFLICTS.md`
C-R103-1). The 661 obligation calls under `index_v3` ran under the main-study protocol (served
`gpt-4.1-mini-2025-04-14`, 0 failures, $0.4489); the v3-elicited gate at the same base rate fires on 110 items
(63 PN / 22 PRESENT / 25 ABSENT) against the committed gate's 75, and the policy MODEL-ALL-V3 that reads it
reaches 89 / 104 = 0.8558 (54 / 63, 22 / 26, 13 / 15; tagged 72). On the 41 counted-state items it reaches
0.8537 against MODEL's 0.7805, +0.0732 with both intervals reaching zero ([+0.0000, +0.1707]; [+0.0000, +0.1875]);
the gate fires on 5 of the 17 newly fetchable records (3 of them ones the retriever misses). The v3 monitor row
reads 0.7354 against 0.7339 committed (+0.0015, [-0.0385, +0.0494]; [-0.0473, +0.0503]). Stage 2 on the 21 views
no registered policy assembled billed $0.0083; total $0.4579. Ledgered in `NUMBERS_DS.md` section 6
(`AUX-DS-A1-*`); every value prints as descriptive; **the DS-P4 verdict is unchanged**. Nothing registered was
written; `verify_ds.py` A–G still pass.


## D-DS-4 — the DS-P4 failed-form sentence states a zero change as "raises ... only from $0.7805$ to $0.7805$" (recorded 2026-09-13)

**What happened.** The frozen failed form of DS-P4 (`ADDENDUM_DS.md` §PAPER) reads "Naming the retracted and expired attributes raises the gated reach on those obligations only from $M_{ce}$ to $MA_{ce}$", and both placeholders resolved to $0.7805$ (`AUX-DS-REACH`; D-DS-3 (b)). The printed sentence therefore says "raises ... from $0.7805$ to $0.7805$", a phrasing that reads as a change where the measurement is a zero change. No number is wrong.

**Disposition (the author, 2026-09-13, ruling on the v10 rewrite brief, defect 1).** A wording correction, no number changed: the plain form is "leaves the gated reach on those obligations unchanged at $0.7805$". The freeze forbids rewording the frozen sentence in place (R78-2c: frozen registered wording ships verbatim; the D93 form: the frozen text ships unedited and the correction prints beside it, never in place of it). The sentence therefore ships verbatim in `paper_v10.tex` and the lead-in sentence that precedes the frozen paragraph states the zero change plainly. The verdict (FAILS), the bar, `AUX-DS-REACH` and `AUX-DS-PARAGRAPH` are unchanged; the printed form `AUX-DS-PARAGRAPH-PRINTED` is unchanged.

**What this touches.** `paper_v10.tex` (R102): the lead-in sentence before the frozen Section 8 paragraph; the deviation index of Appendix G gains this line. No ledger value, no threshold, no frozen text of `ADDENDUM_DS.md` changes; `verify_ds.py` is unaffected.
