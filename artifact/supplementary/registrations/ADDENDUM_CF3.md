# ADDENDUM_CF3 — descriptive extension of the store-counterfactual set on the expiry state: the 14 eligible, undrawn expiry pairs the CF-2 predicates admit

Written 2026-09-14, BEFORE any call, on the author's ruling of that date, quoted: "CF-3 ruling: expiry only. Register a
descriptive addendum for the 14 eligible undrawn expiry pairs that fit the cap and the name rule (42 items, three
versions each, same construction, same summaries, no reads required). Score both lookups, then mini once, Haiku five
calls, Opus once. Report the cell beside the 444, and a pooled expiry row (CF-2 plus CF-3, 44 pairs) with the pooling
disclosed in the caption. Retraction stays at 30." Descriptive: this addendum carries **no prediction, no bar and no
verdict**; every number prints whichever way it comes out. It is frozen by its sha256, recorded in
`r82_counterfactual/cf3/NUMBERS_CF3.md` before the first call. Nothing here re-adjudicates any CF-2 verdict, predicate
or row; the CF-2 rows are read and never re-run.

## §1 — Population: the 14 pairs, and why no read is needed

The census of 2026-09-14 (`r82_counterfactual/cf3/CF3_CENSUS.md`, `census_cf3.json` sha256 `b1c9cf1e292dfbb7…`,
commit `ba922af`) replayed the CF-2 draw's predicates (ADDENDUM_CF2 §§2–3) one at a time over the 40 banks. On the
expiry class every admitted candidate had been read: 49 ELIGIBLE, 30 drawn into the 444, 19 ELIGIBLE and undrawn. Of
the 19, **14 fit the cap of four pairs per persona per state and the one-pair-per-(persona, scrubbed name) rule with
the 444's usage counted** (`C_sizing.EXPIRY.no_relaxation.eligible_undrawn_fitting_list`). They are the population,
fixed here by (persona, entry id):

| # | persona | entry | slot key | category | anchor (event time) | verdict source | CF-2 queue position | overlap tag |
|---:|---|---|---|---|---|---|---:|---|
| 1 | patrick | `lb_00343` | `travel_arrival_date:battalion_chiefs_conference` | LOGISTICAL_CONTEXT | 2026-09-14 | CF-1 reused | 46 | — |
| 2 | patrick | `lb_00344` | `travel:flight_inbound` | LOGISTICAL_CONTEXT | 2026-09-14 | CF-1 reused | 47 | — |
| 3 | patrick | `lb_00349` | `event:battalion_chiefs_conference_2026` | OBLIGATIONS | 2026-09-15 | CF-1 reused | 49 | — |
| 4 | patrick | `lb_00350` | `hotel_for_conference_2026` | LOGISTICAL_CONTEXT | 2026-09-15 | CF-1 reused | 50 | — |
| 5 | priya | `lb_00324` | `project_deadline:NeurIPS_paper` | OBLIGATIONS | 2026-06-01 | CF-1 reused | 53 | O1 (a CF-1 pair) |
| 6 | raj | `lb_00437` | `training_course:boiler_refresher` | OBLIGATIONS | 2026-06-15 | CF-1 reused | 57 | O2 (the 84) |
| 7 | raj | `lb_00443` | `course:regulatory_update` | OBLIGATIONS | 2026-06-15 | CF-1 reused | 58 | O2 (the 84) |
| 8 | raj | `lb_00515` | `upcoming_job` | PROJECTS_ENDEAVORS | 2026-05-22 | author 2026-09-12 | 61 | — |
| 9 | rosa | `lb_00528` | `family_event_date` | OBLIGATIONS | 2026-07-28 | CF-1 reused | 63 | — |
| 10 | thanh | `lb_00468` | `event_guest_count:duc_wedding` | OBLIGATIONS | 2026-07-12 | CF-1 reused | 65 | O1 (a CF-1 pair; also in the 84) |
| 11 | thanh | `lb_00476` | `wedding_menu` | OBLIGATIONS | 2026-07-12 | CF-1 reused | 66 | O2 (the 84) |
| 12 | valentina | `lb_00362` | `trip_plan_rioclaro` | PROJECTS_ENDEAVORS | 2026-05-26 | author 2026-09-12 | 68 | — |
| 13 | valentina | `lb_00364` | `trip_destination` | LOGISTICAL_CONTEXT | 2026-05-01 | CF-1 reused | 69 | — |
| 14 | yoli | `lb_00418` | `event:Afrofest_attendance` | RELATIONAL_BONDS | 2026-07-31 | author 2026-09-12 | 70 | — |

Every verdict is one CF-2 recorded (eleven CF-1 verdicts reused as CF-2 reused them, three of the author's
2026-09-12 read); none is re-adjudicated. Five pairs carry the overlap tags CF-2 admitted for the expiry class (O1: a
CF-1 expiry pair; O2: an entry the 84-question filter had removed); they are disclosed as CF-2 disclosed them. Four
pairs of one persona (patrick) are four records of one conference under four scrubbed names, which the one-per-name
rule permits; the cap of four binds there. **Zero overlap with the 444 by (persona, entry id) is asserted at build.**
Retraction stays at 30 (the census: one candidate in ten passes the author's eligibility read, 36 of 370; no draw).

## §2 — Construction (CF-2's, called; frozen)

The three store versions of each pair are built by `cf2_build_cell.build()` with its path constant re-pointed to
`r82_counterfactual/cf3/` and nothing else changed: the expiry PN version moves the original's `event_time` to
`cutoff − 30 d` and appends the `expiring_logistics` record with `status: expired`, so the label path and the index path
record the same event and are asserted to agree; PRESENT is the store as it stands; ABSENT removes the slot through
scrubbed-slot closure with the category left populated (ADDENDUM_CF2 §2). Assertion families A–E, the draw-time
predicates re-asserted at build and assertion C on the emitted text are carried unchanged; any failure is a STOP. The v2
(superseded-names) and v3 (all-states) summaries come from the locked renderer through `build_cf_cell.build_index`. The
count-randomized arm is built by `cf2_build_cell.add_v2r()` over the **42 versions of this cell** (a seed-42 derangement
of the (retracted, expired) totals within the cell, renderer lock asserted per version); the permutation is within the
cell and not across the 444, which is disclosed wherever the arm prints. The input files are written under the CF-2
file names inside `cf3/` (`cf_pairs_cf2.json`, `cf_questions_cf2.json`, `cf_pn_texts_cf2.json`, `_names_cf2.json`) so
that the CF-2 modules read them unmodified; `cf3/README.md` says so.

## §3 — Questions (the frozen renderer) and the leakage screen

Each pair's question is drafted **before any store version exists** through the frozen CF-1 renderer
(`draft_questions.py`, prompt sha256 `b748247b…`; `gpt-4.1-mini`, temperature 0, seed 42 with 4242 as the retry, three
paraphrases, the CF-1 intent gate under UPCOMING), exactly as `cf2_draft_questions.py` drafted the 148: the module's
three path constants are re-pointed and nothing else. The questions sha256 is ledgered (`AUX-CF3-QUESTIONS`). The
index-leakage screen of ADDENDUM_CF2 §5 (`cf2_leakscreen.py`, `prompts_e1.LEAKAGE_*`, `gpt-4.1-mini`) runs on the v3
and v2r arms (v2 beside them) over **all 14 PRESENT items** of the cell; the CF-2 rule "leaks iff more than 3 of 30
score correct" scales to **leaks iff more than 1 of 14 scores correct**, and a leak is a STOP. The author's question-read
flag (names the value or plan) is a disclosure that Appendix H.2's split reads; a one-column sheet is offered at
`reviews/v13/CF3_QUESTION_FLAGS.md`, and an unread flag excludes nothing.

## §4 — Arms and readers

Arms: BLIND (one call per question, reused across the question's three versions, so blind AUROC is 0.5 by the CF-2
identity), INDEXED-V2, INDEXED-V3, INDEXED-V2R. Prompts `prompts_e1.SYSTEM` / `USER_BLIND` / `USER_INDEXED` verbatim
(digests asserted at import through `run_cf.py`). **Lookups ($0):** the superseded-names lookup on v2 and the all-states
lookup on v3, embedding (`score_cf.matcher`) and lexical (`run_nb6.lex_scores`), exactly as `cf2_score.py` builds the
lists. **Models:** `gpt-4.1-mini` k = 1, temperature 0, max_tokens 200, synchronous, list price; Haiku 4.5
(`claude-haiku-4-5-20251001`) k = 5, temperature 0, max_tokens 200, Batch, X4 collapse (MIN_DRAWS 3, arithmetic mean);
Opus 5 (`claude-opus-5`) **k = 1**, temperature unset, max_tokens 1024, Batch — one call by the author's instruction,
against k = 5 on the CF-2 rows, a draw-count difference disclosed beside every pooled Opus row. Served identifiers are
probed before each lane (E1.7 rule). Rows under `r82_counterfactual/cf3/rows/`.

## §5 — Estimands (descriptive)

On the 42 items (14 positives, one PN version per pair): for every reader × arm, AUROC (Mann-Whitney, ties at 0.5;
blind 0.5 by identity so every AUROC is also its gain), the item-level paired bootstrap interval (1,000 draws, seed 42,
single-class draws discarded) and the persona-clustered interval (group = persona; nine personas), both printed, the
weaker reading stated where they disagree; the model-minus-lookup difference on the same summary (v2 against the
superseded-names lookup, v3 against the all-states lookup) with both intervals. **The pooled expiry row:** the 444's 30
expiry pairs (90 items, the recorded CF-2 rows `cf2/rows/rows_{MINI,H45,OP5}.jsonl` through `score_cf.load_lane`) plus
these 14 (42 items) = **44 pairs, 132 items**, per reader per summary, with the same estimands; the pooling is
disclosed wherever the row prints: the two cells were scored on different dates under two registrations with the same
prompts, models and construction, and Opus 5's CF-2 rows are k = 5 against k = 1 here. No branch is enumerated; nothing
holds or fails.

## §6 — Budget, lane order, STOP

Projected from the CF-2 rows' per-call actuals (`AUX-CF2-SPEND`): drafting ≈ 14–42 calls $0.01; the leakage screen 42
calls ≈ $0.06; mini 140 calls ≈ $0.10; Haiku 4.5 700 calls ≈ $0.93; Opus 5 140 calls ≈ $1.20 — **≈ $2.30, line $5**,
inside the author's overall cap of $28 for the pass ($7.89 billed before this addendum; the PARA lanes pending). Lane
order: drafting → build (no call) → leakage screen → lookups → mini → Haiku 4.5 → Opus 5; each lane probed and projected
before submission against its line. STOP: registration sha256 mismatch; the census file's sha256 differing from §1; any
of the 14 not ELIGIBLE in `cf2/adjudication_cf2.json`, or present in the 444 by (persona, entry id); any assertion of
§2 failing; a leak under §3; a served-identifier mismatch; elicitation failures after the retry on more than 2% of a
lane's rows; a projection over the line.

## §7 — Ledger and paper site

`r82_counterfactual/cf3/NUMBERS_CF3.md`: `AUX-CF3-LOCK`, `AUX-CF3-QUESTIONS`, `AUX-CF3-LEAK`, `AUX-CF3-PROBE-*`,
`AUX-CF3-LOOKUP-{EMB,LEX}-{V2,V3}`, `AUX-CF3-MINI-*`, `AUX-CF3-H45-*`, `AUX-CF3-OP5-*`, `AUX-CF3-POOLED-*`,
`AUX-CF3-SPEND`. Paper: the CF-3 cell beside the 444 in the per-state table of Appendix D.2 and the pooled expiry row
with the pooling in the caption; one sentence in Section 5 or Section 9 that one retraction candidate in ten passes the
author's eligibility read, citing the census; Table 3's conflate row gains the manifest count (40 retraction events, 9
resolving to a retracted entry under the truthful join) if the paper does not state it. No frozen number and no frozen
text changes.

## Registration mechanics

Frozen by sha256 before the first call (recorded in `NUMBERS_CF3.md`). Copied to
`iclr2027_monitoring_submission/ARTIFACT/registrations/ADDENDUM_CF3.md`. Amendments, if any, are appended as dated
sections below the marker line and never edit the text above. The run proceeds on the author's instruction of
2026-09-14 quoted at the head; the author's ratification line is drafted below the marker alongside the placement
amendment's, for the author's signature.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->

## Author's ratification (dated; drafted 2026-09-14 alongside AMENDMENT_MAIN_PLACEMENT.md)

**Dated line for the author to ratify (2026-09-14):** _The author ratifies ADDENDUM_CF3.md (registered text sha256 `2f555c1ac4c3018e66a0fc453be7c4c4d3ffd4e3a2f7ac63c5c7b3590ca4f910`): the 14 expiry pairs of §1, CF-2's construction, questions and arms, the readers of §4 and the pooled expiry row of §5, run on the author's instruction of 2026-09-14 ahead of this line._ — signed: ______

The run was ordered by the author's message of 2026-09-14 quoted at the head of this file; it proceeds ahead of the ratification line, as the placement amendment did, and every artifact it writes carries the sha256 above.
