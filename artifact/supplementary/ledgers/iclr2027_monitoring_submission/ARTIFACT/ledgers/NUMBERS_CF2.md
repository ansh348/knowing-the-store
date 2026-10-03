# NUMBERS_CF2 — ledger for the CF-2 cell (ADDENDUM_CF2.md, frozen f016f03; Amendment 1 at §14)

Every number CF-2 prints enters the manuscript through a key in this file and no other way.
Keys are reserved in the registration's §9 and written as the build proceeds; a key that cannot
be computed carries a dash and its reason. No store version, index, label, monitor score or
baseline score exists at the time of the entries below. Verifier: `tools/verify_cf2.py`.

---

## 1. AUX-CF2-CENSUS — the census under the CF-2 predicate (2026-09-12, `select_pairs.py --cf2 --census`, `cf2/census_cf2.json`)

Stages: raw → individuates in PRESENT → not on the v2 superseded list → zero overlap with the
90 / the 84 / the 36, or re-admitted (O1, O2). Beside each, `reviews/CF2_SCOPE.md` Phase 2.

| Class | CF-2 | Scope | Admitted | Verdicts before the CF-2 read | Admissible | Personas | Distinct (persona, scrubbed name) |
|---|---|---|---:|---|---:|---:|---:|
| EXPIRY, frozen two-category predicate | 46 → 41 → 41 → 41 → 38 → 38 | 46 → 41 → 41 → 32 → 25 → 25 | 38 (25 zero-overlap, 9 O1, 4 O2) | 29 ELIGIBLE, 9 INELIGIBLE | 29 | — | — |
| EXPIRY, O3 widened | 87 → 59 → 53 → 45 → 41 → 41 | 87 → 41 | 41 | 41 unadjudicated | 41 | — | — |
| EXPIRY, all | | | **79** | 29 / 9 / 41 | **70** | 25 | 62 |
| RETRACTION | 1,590 → 1,379 → 1,173 → 1,053 → 1,048 → 1,043 | identical | 1,043 | 1 ELIGIBLE, 25 INELIGIBLE, 1,017 unadjudicated | **1,018** | 40 | 509 |
| SUPERSESSION | 3,347 → 3,230 → 3,230 → 3,187 → 3,170 → 3,133 | identical | 3,133 | 3 INELIGIBLE, 3,130 unadjudicated | **3,130** | 40 | 2,399 |

Scarcity order: EXPIRY > RETRACTION > SUPERSESSION (unchanged from CF-1). The only movement
against the scope is the two registered re-admissions (+9 at the 90 stage, +4 at the 84 stage);
`rosa lb_00522` falls at individuation and is not admitted.

## 2. AUX-CF2-ADJUDICATION — the CF-2 read, complete (12 Sep 2026; `cf2/verdicts_12sep.json`, sha256 `48112523bded3ffe…`, merged into `cf2/adjudication_queue.json` by (state, entry_id) and regenerated as `cf2/adjudication_cf2.json`; every row checked against the queue)

Criteria: `ADDENDUM_R82.md` §3.1 verbatim; the author's dated notes are in `ADDENDUM_CF2.md` §3.1
(amendment text under §14). Walk statuses: ELIGIBLE / INELIGIBLE (author's verdicts, 12 Sep);
REUSED (CF-1 ELIGIBLE carried, not re-read); SKIP-RANK (not read — an earlier same-name candidate
for the persona was ELIGIBLE; recorded as not adjudicated with that reason); UNREAD (past the
state's stop; stays unread).

**Method (author's line, verbatim).** Method: entries presented by a language model in walk order, triaged within each batch (plan-like first, plain records grouped) for retraction, plain tables for expiry and supersession; every entry shown; verdicts typed by the author; the model flagged disagreements only after the author's verdict. Disclosed under the AI-use line.

**Read telemetry (author's line, verbatim).** Read telemetry, 12 Sep 2026, one session: expiry 41 verdicts in about 25 minutes; retraction about 367 reads (verdicts plus rank-skips) in 8 batches, measured eligibility 35/367 = 0.095 (34 usable); supersession 165 reads in 4 batches, 106 ELIGIBLE, 53 INELIGIBLE, 6 rank-skips, rate 106/159 = 0.667.

| Key | Value |
|---|---|
| **AUX-CF2-ADJUDICATION-EXPIRY** | 70 rows in the queue; stop at position **70**. Walk statuses: ELIGIBLE 20, INELIGIBLE 16, REUSED 29, SKIP-RANK 5. **Verdict reads 36** (41 with rank-skips); ELIGIBLE **49** (20 new + 29 reused); new-candidate eligibility **0.5556**. |
| **AUX-CF2-ADJUDICATION-RETRACTION** | 1018 rows in the queue; stop at position **440**. Walk statuses: ELIGIBLE 35, INELIGIBLE 334, REUSED 1, SKIP-RANK 70, UNREAD 578. **Verdict reads 369** (439 with rank-skips); ELIGIBLE **36** (35 new + 1 reused); new-candidate eligibility **0.0949**. |
| **AUX-CF2-ADJUDICATION-SUPERSESSION** | 3130 rows in the queue; stop at position **165**. Walk statuses: ELIGIBLE 106, INELIGIBLE 53, SKIP-RANK 6, UNREAD 2965. **Verdict reads 159** (165 with rank-skips); ELIGIBLE **106** (106 new + 0 reused); new-candidate eligibility **0.6667**. |

Counted against the author's telemetry line: retraction verdict reads are 369 by the file
(the line says "about 367"), and "34 usable" is the author's within-walk count; the acceptance
walk below finds 33 usable under the one-per-name rule applied across states (three retraction
`project` candidates yield to same-name pairs: chenoa `lb_00029`, jake `lb_00110`, jerome
`lb_00184`). Supersession: 106 / 159 = 0.667 against the 0.769 §3.2 assumed. Expiry `patrick
lb_00376` (six-week class), PENDING in the first deposit, is ELIGIBLE by the author's call
("weak E").

## 2a. AUX-CF2-CONSTRUCTION and AUX-CF2-OVERLAP — the acceptance walk (12 Sep 2026; `cf2/cf_pairs_cf2.json`; no question drafted, no store version built)

`select_pairs.py --cf2 --accept`: ELIGIBLE rows only, in queue order, states in scarcity order
EXPIRY > RETRACTION > SUPERSESSION, cap 4 per persona per state, one pair per (persona,
scrubbed name) across the whole draw; stop at the quota. Quotas per §14: 100 / 30 / 30.

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (draw) | **160 pairs accepted: SUPERSESSION 100, RETRACTION 30, EXPIRY 30**, over **40 personas**; cap never binding (max 4 per persona per state, reached by elena, kenji, kofi, marcus, mirri, omar, priya, thanh in supersession). Last accepted queue position: expiry **44** of 70, retraction **404** of 440 read, supersession **152** of 165 read. Sources: expiry 15 CF-1 reused + 15 author; retraction 1 reused + 29 author; supersession 100 author. Expiry by class: 15 under the frozen two-category predicate (OBLIGATIONS 7, LOGISTICAL_CONTEXT 8), **15 O3** (PROJECTS_ENDEAVORS 10, RELATIONAL_BONDS 2, HEALTH_WELLBEING 1, HOBBIES_RECREATION 1, FINANCIAL_MATERIAL 1). Passed over at acceptance, all by the one-per-name rule, none by the cap: EXPIRY 0029 jake `lb_00358` (project); RETRACTION 0077 jake `lb_00110` (project); RETRACTION 0120 chenoa `lb_00029` (project); RETRACTION 0224 jerome `lb_00184` (project). ELIGIBLE but unreached: expiry 18 (positions 45–70, among them patrick's five conference entries, priya's two, raj's four, rosa, thanh's two, valentina's two, yoli), retraction 3, supersession 6. |
| **AUX-CF2-OVERLAP** | Accepted pairs carrying an overlap tag, by (persona, entry_id): **O1 (CF-1's expiry pairs re-admitted): 7** — (billy, lb_00273), (david, lb_00496), (elena, lb_00488), (fatima, lb_00393), (marcus, lb_00235), (marley, lb_00343), (mehmet, lb_00429). **O2 (the four ELIGIBLE entries the 84 filter removed): 0** — none reached: raj `lb_00437`, `lb_00443`, `lb_00447` and thanh `lb_00476` sit at expiry positions 57–59 and 66, past the position (44) at which the quota filled in persona order. No other accepted pair overlaps the 90, the 84 or the 36. |
| accepted per persona (SUP / RET / EXP) | aisha 3/3/2, alex 3/1/0, amara 3/0/0, aroha 1/1/0, billy 1/1/1, bruna 3/1/0, callum 2/1/2, chenoa 1/1/0, dariush 0/0/3, david 1/0/2, diane 1/0/2, dmitri 3/1/0, elena 4/1/3, fatima 3/0/3, ingrid 3/1/0, jake 2/1/2, jerome 3/0/1, joonho 3/0/0, kenji 4/0/0, kofi 4/1/1, leila 2/1/0, lily 2/1/0, marcus 4/1/3, marley 1/2/2, mehmet 2/0/2, mirri 4/0/0, nadia 2/0/0, omar 4/1/0, pan 2/1/1, patrick 1/1/0, priya 4/2/0, raj 3/2/0, rosa 2/1/0, saga 3/1/0, samuel 2/0/0, thanh 4/0/0, tom 2/0/0, valentina 3/0/0, yoli 3/1/0, zara 2/1/0 |

## 2b. AUX-CF2-CONSTRUCTION — questions and PN records (CF2-BUILD-2, 12 Sep 2026; gpt-4.1-mini and text-embedding-3-small only; nothing on the Anthropic key)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (D-CF2-2 replacement) | `cf2:zara:project:AA_application` (RETRACTION, queue position 225, ELIGIBLE by the author) **excluded: authoring predicate** — `author_pn.py` failed twice on MIN_DISCR (n_discr_old 2 < 3; the cancellation must name "AA SED program application"); the verdict stands. Replaced by **`cf2:pan:family_member:beam_role_in_business`** (position 414, zero-overlap, not O3); mehmet `lb_00156` at 410 was passed over by the one-per-name rule (mehmet's `project` is an accepted expiry pair). Composition unchanged 100 / 30 / 30. |
| **AUX-CF2-CONSTRUCTION** (questions) | `cf2/cf_questions_cf2.json`: **160 questions**, frozen renderer sha `b748247b…` (seven fields unchanged), seed 42, three paraphrases, seeded pick, intent gate under AV2. **Substitutions 3** (elena `event:wedding_timeline`, fatima `trip_schedule:salone_del_mobile_2026`, marcus `morning_phone_usage_duration` — the seeded paraphrase failed the gate, the next in order passed), **redrafts 0**; the D-CF2-2 replacement drafted and appended with its own trail (first pick, index 1). **Questions sha256 `871c353762e8065fff141039cd452e73df34cca8cd61cb21712324ff53645b0e`**. First-person voice 141 of 160 (CF-1: 25 of 30). Tokens 50,234 in / 7,374 out; **$0.0319**. |
| **AUX-CF2-CONSTRUCTION** (PN records) | `cf2/cf_pn_texts_cf2.json`: **130 records authored** (100 supersession, 30 retraction) through `author_pn.py` unchanged (prompt sha `b6f53b1a…` = CF-1's), seed 42; 30 expiry pairs anchor-only. Predicates on every record: n_discr ≥ 3 both sides, detector on the original ≥ TAU_HI 0.80 (all 130 at 1.00), cross-guard, gold cover at TAU_GOLD. **Retries 1** (cf2:zara:medication:vitamin D supplement dosage — passed on the frozen second attempt). **Retraction cosine** to the original under text-embedding-3-small, measured not enforced (n = 30): min 0.463, p25 0.623, median 0.675, p75 0.729, max 0.789; **0 of 30 at or above 0.85** (CF-1: 1 of 10; the store's slot branch fires regardless, Amendment 2). Tokens 42,668 in / 3,184 out / 1,177 embed; **$0.0222**. Aborted first run (stopped at the 21st authored pair, no meter reached): ≈ $0.004 **[est]**. |

## 2c. AUX-CF2-PNREAD and AUX-CF2-QUESTIONREAD — the author's two reads (12 Sep 2026; `cf2/cf2_reads_12sep.json`, sha256 `ae207a01f39b7a94…`, merged by (state, persona, entry_id) into `cf2/pn_read_verdicts.json` and `cf2/question_read_flags.json`; every row checked against the read documents' order)

Merge key: (state, persona, entry_id) — (state, entry_id) alone is ambiguous, entry ids repeat
across personas (52 collisions among the 130 authored pairs).

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** | Three-way read of the 130 authored records (`reviews/CF2_PN_READ.md`): **supersession 69 YES / 21 NO-paraphrase / 10 NO-implausible; retraction 29 YES / 1 NO-implausible** (record 104, alex `project_release_strategy`: half-reverses rather than cancels). **32 NO in all**, every one re-authored once at seed 4242 under D-CF2-3 (§2d). **Failure pattern, as observed by the author:** paraphrases concentrate on attitude, feeling and philosophy slots; implausible successors on identity-adjacent slots (career, family history, trauma). **What the read guards:** the monitor's input is value-scrubbed — no authored text reaches any index or prompt — so this read guards **label honesty under Definition 1** (a paraphrase would make the PN label semantically hollow), not the measurement. |
| AUX-CF2-PNREAD, author's notes verbatim | (1) Three-way read: YES (a different value or a real cancellation this person could plausibly come to), NO-paraphrase (same fact reworded; under Definition 1 the old value would not make the answer wrong, so the PN label would be semantically hollow), NO-implausible (contradicts the persona or cancels something other than the plan). (2) Result: supersession 69 YES / 21 NO-paraphrase / 10 NO-implausible; retraction 29 YES / 1 NO-implausible (104: half-reverses rather than cancels). (3) Pattern: paraphrases concentrate on attitude, feeling and philosophy slots; implausible successors on identity-adjacent slots (career, family history, trauma). (4) The monitor's input is value-scrubbed; the read guards label honesty, not the measurement. (5) Method: records presented by a language model with a look-twice flag on some rows; verdicts typed by the author; disclosed under the AI-use line. Author caught 004 (Series A to seed is a rewind, not a successor) unflagged. |
| **AUX-CF2-QUESTIONREAD** | Value-token read of the 160 questions (`reviews/CF2_QUESTION_READ.md`): **90 of 160 flagged** — by the file, supersession 47 of 100, retraction 21 of 30, expiry 22 of 30 (the author's note gives the split as 43 / 19 / 28 "after the four consistency additions"; the per-row file governs and sums to the same 90). CF-1 found 3 of 30. **Construction explains the rise:** CF-2's retraction and expiry slots are named after their events, so the question names the plan. **Disclosure, not a gate:** the question is identical across the three store versions and cannot carry the label. Rendering note: item 119's raw slot name `msc_sports_rehabilitation` appears verbatim in the question. 83 distinct tokens; the most frequent appear twice (vaping, malaria, tea, vitamin D, CIMA, Isfahan, wedding). |
| AUX-CF2-QUESTIONREAD, author's notes verbatim | (1) Rule applied by the author: flag YES when the question names any specific condition, method, item, place, person (other than the persona's own name), date or event; NO when it names only the slot's topic. Persona's own name is not a value. (2) Result: 90 of 160 flagged (supersession 43 of 100 after the four consistency additions, retraction 19 of 30, expiry 28 of 30). CF-1 found 3 of 30. The difference is construction: CF-2's retraction and expiry slots are named after their events, so the question names the plan. The question is identical across the three versions and cannot carry the label; this is a disclosure, not a gate. (3) 119: the raw slot name msc_sports_rehabilitation rendered verbatim in the question; flagged and recorded as a rendering note. |

## 2d. AUX-CF2-PNREAD — the D-CF2-3 re-authoring (12 Sep 2026; `cf2/cf_pn_texts_cf2_reauthor_4242.json`; gpt-4.1-mini + text-embedding-3-small)

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** (re-authoring) | **32 records re-authored once** through `author_pn.py` unchanged at **seed 4242** (`tools/cf2_reauthor_pn.py`; the only patched constant is the seed). The tool's digest binds the seed: the file records prompt sha `3b5c9c236b6783e2f306bd80ace8fb3b67311bd5643cbe8b20cc7eaf6d796c5a` = the frozen prompt `b6f53b1a…` at seed 4242 (asserted before patching). All 32 pass the write-path predicates; **retries 0**. **15 of 32 are byte-identical to the first attempt** — supersession 9 paraphrase + 5 implausible, retraction 1 — so at temperature 0 the alternate seed moved 17 outputs; the identical ones fall to D-CF2-2 unless the author reads them differently. Re-read document `reviews/CF2_PN_REREAD.md`; verdicts pending in `cf2/pn_reread_verdicts.json`. Tokens 10,441 in / 807 out / 51 embed; **$0.0055**. |
| supersession spares, for the D-CF2-2 consequence | 106 ELIGIBLE − 100 accepted = **6 spare** in walk order (positions 153–165); every failure beyond six drops the supersession quota by the shortfall under a further deviation, unless the author extends the supersession read past position 165 (2,965 UNREAD, rate 0.667 so far). Retraction: 3 spare ELIGIBLE; expiry: 18 unreached ELIGIBLE. |

## 2e. AUX-CF2-PNREREAD — the re-read of the 32 re-authored records (13 Sep 2026; `cf2/cf2_pn_reread_13sep.json`, sha256 `07212b1d529a7c84…`, merged by (state, persona, entry_id) into `cf2/pn_reread_verdicts.json`; every row checked against `reviews/CF2_PN_REREAD.md`'s order and identity flags)

| Key | Value |
|---|---|
| **AUX-CF2-PNREREAD** | Of the 32 re-authored at seed 4242: **17 re-read** (the ones the seed changed) → **1 YES** (re-read 20, omar `budget_allocation`, "a real change of value") and 16 the same failure in new words (13 paraphrase, 3 implausible); **15 kept the first verdict by identity** (byte-identical text; 9 paraphrase + 5 implausible supersession, 1 implausible retraction). **Outcome: 30 supersession and 1 retraction records fail after the frozen retry and fall to D-CF2-2**; the YES record replaces its first attempt in `cf2/cf_pn_texts_cf2.json` (`reauthored_under: D-CF2-3`, seed 4242). Supersession spares in walk order 6 (positions 153–165); **shortfall 24 before authoring losses**. |
| **Instrument note** (author's, for the ledger and for CF-3) | At temperature 0 an alternate seed changed 17 of 32 outputs and fixed 1; "one frozen retry" is nearly a no-op for this tool. A retry that varies the sampling temperature or uses a disclosed second prompt lineage should be registered next time. |
| author's notes verbatim | (1) Re-read of the 17 records the seed-4242 re-authoring changed: 1 YES (20, omar budget_allocation: a real change of value), 16 the same failure in new words (13 paraphrase, 3 implausible). The 15 byte-identical records keep the first verdict by identity and were not re-read. (2) Outcome: 30 supersession and 1 retraction records fail after the frozen retry and fall to D-CF2-2 replacement. Supersession spares in walk order: 6 (positions 153-165); shortfall 24 before authoring losses. (3) Instrument note for the ledger and for CF-3: at temperature 0 an alternate seed changed 17 of 32 outputs and fixed 1; 'one frozen retry' is nearly a no-op for this tool. A retry that varies the sampling temperature or uses a disclosed second prompt lineage should be registered next time. (4) Method as before: records presented by a language model, verdicts typed by the author, disclosed under the AI-use line. |

## 2f. AUX-CF2-CONSTRUCTION — D-CF2-2 applied to the 31 records that fail the re-read (13 Sep 2026; `select_pairs.py --cf2 --exclude-batch`; `cf2/cf_pairs_cf2.json`; no store version built)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (D-CF2-2 batch) | **31 pairs excluded: PN read** — 30 supersession (queue positions 3, 10, 18, 28, 30, 32, 39, 40, 45, 46, 52, 56, 63, 66, 68, 73, 81, 85, 87, 103, 105, 110, 112, 116, 125, 127, 128, 135, 146, 150) and 1 retraction (alex:project_release_strategy `cf2:alex:project_release_strategy`, position 158); every one keeps its ELIGIBLE verdict (`eligibility_verdict_stands: true`) and carries the failing read (`AUX-CF2-PNREREAD`) in `meta.excluded`; their question rows and PN records moved to `meta.excluded_questions` / `meta.excluded_records` of their files, the questions sha256 recomputed over the 129 remaining. None of the 31 carried an overlap tag or O3 (`AUX-CF2-OVERLAP` unchanged: O1 7, O2 0, O3 15). |
| **AUX-CF2-CONSTRUCTION** (refill, walk order) | Each short state re-walked from position 1 under the cap and the one-per-name rule across states, using the freed cap slots and names. **Retraction: 1 replacement**, `cf2:nadia:project_pitch:spring_menu` (position 419, `lb_00470`, PROJECTS_ENDEAVORS, zero-overlap) for `cf2:alex:project_release_strategy`. **Supersession: 6 replacements — every ELIGIBLE spare in the 165 rows read** — `cf2:nadia:project_pitch:spring_menu` (pos 419) for `cf2:alex:project_release_strategy`; `cf2:callum:communication_style` (pos 154) for `cf2:aisha:career_progress`; `cf2:jake:habit:juul_use_intensity` (pos 157) for `cf2:aisha:emotional_state:family_expectations`; `cf2:david:reading_preferences_narrative_nonfiction` (pos 161) for `cf2:aisha:medication:ferrous_sulfate`; `cf2:aroha:personal_time_value` (pos 162) for `cf2:alex:company_stage`; `cf2:tom:vehicle_use` (pos 164) for `cf2:bruna:professional_style`; `cf2:mirri:learning_source:aunties_and_elders` (pos 165) for `cf2:chenoa:personal_commitment`; all zero-overlap, not O3. **Shortfall: 24 supersession pairs pending**; the supersession queue is extended from position 166 by a further adjudication read (`reviews/CF2_ADJUDICATION_READ_EXT.md`, §2g) rather than the quota dropping — the author's ruling of 13 Sep 2026. |
| **AUX-CF2-CONSTRUCTION** (state of the draw) | **136 pairs accepted: SUPERSESSION 76, RETRACTION 30, EXPIRY 30; pending {'SUPERSESSION': 24}**; 40 personas; cap 4 reached in supersession by kenji, marcus, thanh only. Last accepted queue position: expiry 44, retraction **419**, supersession **165** (all 106 ELIGIBLE rows of the 165 read are used: 76 accepted, 30 excluded). Supersession eligibility on the 165 read: 106 ELIGIBLE / 159 verdict reads = **0.667** (6 NOT-ADJUDICATED); PN authoring-and-read pass on the 100 first-drawn supersession records: 70 of 100 (69 first read + 1 re-read) = 0.70; the extension is sized at the author's 0.75. `meta.pending_draft` lists the 7 replacements awaiting their question and record. |
| accepted per persona (SUP / RET / EXP), after the batch | aisha 0/3/2, alex 2/0/0, amara 3/0/0, aroha 2/1/0, billy 1/1/1, bruna 2/1/0, callum 3/1/2, chenoa 0/1/0, dariush 0/0/3, david 1/0/2, diane 0/0/2, dmitri 2/1/0, elena 3/1/3, fatima 3/0/3, ingrid 2/1/0, jake 3/1/2, jerome 1/0/1, joonho 3/0/0, kenji 4/0/0, kofi 3/1/1, leila 2/1/0, lily 2/1/0, marcus 4/1/3, marley 1/2/2, mehmet 1/0/2, mirri 2/0/0, nadia 1/1/0, omar 2/1/0, pan 1/2/1, patrick 1/1/0, priya 2/2/0, raj 3/2/0, rosa 1/1/0, saga 1/1/0, samuel 1/0/0, thanh 4/0/0, tom 3/0/0, valentina 1/0/0, yoli 3/1/0, zara 2/0/0 |

## 2g. AUX-CF2-CONSTRUCTION — the 7 replacements drafted and authored; the supersession queue extended (13 Sep 2026; gpt-4.1-mini and text-embedding-3-small only; nothing on the Anthropic key)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (replacement questions) | `cf2_draft_questions.py --only` through the frozen renderer (sha `b748247b…`, seed 42): **7 questions, all first pick, 0 substitutions, 0 redrafts**, every one through the intent gate; **$0.0014**. `cf_questions_cf2.json` now **136 rows**, questions sha256 `27777fbdac37cb0eea323b93728abbb73d0e801654cb8465f6bfdc6c94ae8947`; cumulative drafting spend $0.0333. |
| **AUX-CF2-CONSTRUCTION** (replacement PN records) | `cf2_author_pn.py --only` through `author_pn.py` unchanged (sha `b6f53b1a…`, seed 42): **7 records, 0 retries**, every one clears MIN_DISCR 3 both sides (old side 5–9, new side 7–11) and detector 1.00 on the original; nadia's retraction cosine 0.726 (measured, not enforced); **$0.0012**. `cf_pn_texts_cf2.json` now **136 records** (106 authored, 30 anchor-only); cumulative authoring spend $0.0234. `meta.pending_draft` is empty. The 7 records and 7 questions await the author's read: `reviews/CF2_PN_READ_EXT.md` (Part A three-way, Part B value token). |
| **AUX-CF2-ADJUDICATION** (supersession extension, ruling of 13 Sep) | `select_pairs.py --cf2 --extend SUPERSESSION --n 55`: the seed-42 walk continued from **position 166 to 228** — **55 readable candidates** printed in `reviews/CF2_ADJUDICATION_READ_EXT.md` (criteria verbatim at top), **8 skipped** as unreadable under the current draw (kenji ×2, marcus ×2, thanh ×2 at the cap; kofi `project` and joonho `hobby` names already accepted). Sizing from the observed rates, not assumed: eligibility on positions 1–165 = **106 / 159 = 0.6667**; authoring-and-read pass **0.75** (the author's figure; the observed pass on the first 100 supersession records was 0.70); expected reads to fill 24 = **48.0**, marker printed at 48. Nothing accepted from the extension until the verdicts exist; `adjudication_queue.json` `meta.extensions` records the extension. |
| Spend today (13 Sep) | re-read merge $0; batch exclusion $0; questions $0.0014; PN $0.0012; extension $0 — **$0.0025**, OpenAI only. CF-2 OpenAI construction spend to date: questions $0.0333 + PN $0.0234 + re-authoring $0.0055 = **$0.0621** of the $22 line. |

## 2h. AUX-CF2-PNREAD, AUX-CF2-QUESTIONREAD, AUX-CF2-ADJUDICATION — the author's reads of 13 Sep 2026 (`cf2/cf2_ext_13sep.json`, sha256 `92608882d41fe0e1…`; PN and question rows merged by (state, persona, entry_id), adjudication rows by printed position, every row checked against `reviews/CF2_PN_READ_EXT.md` and `reviews/CF2_ADJUDICATION_READ_EXT.md`)

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** (replacements 131–137) | Three-way read of the 7 replacement records: **2 YES** (134 jake `habit:juul_use_intensity`, 137 nadia `project_pitch:spring_menu`), **3 NO-paraphrase** (131 aroha `personal_time_value`, 133 david `reading_preferences_narrative_nonfiction`, 135 mirri `learning_source:aunties_and_elders`), **2 NO-implausible** (132 callum `communication_style`, 136 tom `vehicle_use`). Disclosed by the author: the paraphrase/implausible letters were assigned by a language model from the author's bare NO; the YES/NO is the author's. The 5 NO go to D-CF2-3 (§2i). Cumulative first reads: 137 records — supersession 70 YES / 24 NO-paraphrase / 12 NO-implausible, retraction 30 YES / 1 NO-implausible (`cf2/pn_read_verdicts.json` `meta.counts`). |
| **AUX-CF2-QUESTIONREAD** (161–167) | Value-token read of the 7 replacement questions: **3 flagged** — 164 jake ("Juul"), 165 mirri ("aunties and elders"), 167 nadia ("spring menu pitch"); 161–163, 166 NO. Cumulative: **93 of 167** flagged. Disclosure, not a gate. |
| **AUX-CF2-ADJUDICATION** (supersession extension, positions 166–228) | The 55 readable candidates read: **27 ELIGIBLE, 27 INELIGIBLE, 1 rank-skip** (0212 pan `medication:antacid_gaviscon` behind 0172 `medication:omeprazole_dose`, ELIGIBLE); the 8 pre-skipped (cap/name) recorded as NOT-ADJUDICATED (`SKIP-CAP` 6, `SKIP-NAME` 2). **The author's note gives 26 ELIGIBLE / 28 INELIGIBLE; the per-row file governs** — both sum to 54 verdict reads; the row-level split is 27/27 and is what the walk uses. Supersession to date: **213 verdict reads, 133 ELIGIBLE, rate 0.6244** (extension alone 27/54 = 0.500, below the 0.667 the sizing assumed); stop at 228. |
| author's notes verbatim | (1) 13 Sep 2026: replacement records 131-137 read under the three-way question; 134 and 137 YES; 131/133/135 NO-paraphrase, 132/136 NO-implausible (letters assigned by the model from the author's NO, disclosed). Questions 161-167 flagged 164, 165, 167. Extension read positions 166-228: 26 ELIGIBLE, 28 INELIGIBLE, 1 rank-skip (0212 behind 0172), 8 pre-skipped by cap or name. Verdicts typed by the author; records presented by a language model; disclosed under the AI-use line. |

## 2i. AUX-CF2-PNREAD and AUX-CF2-CONSTRUCTION — D-CF2-3 on the 5 replacement NOs; the acceptance walk over positions 166–228 (13 Sep 2026; `cf2_reauthor_pn.py --only`, `select_pairs.py --cf2 --exclude-batch`)

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** (D-CF2-3, second round) | The 5 NO replacement records re-authored once at seed 4242 (`author_pn` unchanged, retries 0, $0.0008; `cf_pn_texts_cf2_reauthor_4242.json` now 37 records): **3 byte-identical** to the first attempt — 131 aroha `personal_time_value`, 132 callum `communication_style`, 135 mirri `learning_source:aunties_and_elders` — the NO **stands by identity without a re-read** (ruling of 13 Sep) and the pairs fall to D-CF2-2; **2 changed** — 133 david `reading_preferences_narrative_nonfiction`, 136 tom `vehicle_use` — join the next read (`reviews/CF2_PN_READ_EXT2.md` Part A); their first attempts stay in `cf_pn_texts_cf2.json` until a YES. Identity rate for the tool at temperature 0 across both rounds: **18 of 37**. |
| **AUX-CF2-CONSTRUCTION** (D-CF2-2, third batch) | 3 pairs excluded "PN read: NO stands by identity", verdicts standing (the excluded rows carry both reads); **pending rises to 27**; the supersession walk resumed at position 166 under the cap and the one-per-name rule: **26 replacements accepted, positions 166–226** (mehmet:shop_equipment_preference (166), priya:cognitive_style (167), dmitri:client_facing_name_usage (168), lily:healthcare_provider:gp (171), pan:medication:omeprazole_dose (172), elena:work_stress_carryover (175), fatima:health_care:physiotherapy (179), valentina:therapy_method (183), saga:health_observation:stress_correlation (188), yoli:profession_or_hobby:music_production (191), omar:value_system (192), bruna:breakfast_habit (193), callum:privacy_preference:health_condition (194), jake:preference:juul_flavor (197), chenoa:perspective:chronic_condition_management (200), aroha:health_habit:blood_sugar_monitoring (202), tom:preference:routine (204), mirri:work_vehicle_condition (205), mehmet:barbering_method_preference (206), priya:morning_routine (207), lily:health_management:eczema_cotton_gloves (211), raj:website_hosting_budget (222), valentina:hobby:history_podcasts (223), patrick:mental_health_care (224), kofi:health_condition:tiredness (225), jerome:health_condition:trauma_flashbacks (226)); all zero-overlap, none O3. **One ELIGIBLE row passed over: 0215 elena `mental_transition_routine` — elena reached the cap at 0175.** **Pending: 1 supersession pair** (for mirri `learning_source:aunties_and_elders`). |
| **AUX-CF2-CONSTRUCTION** (state of the draw) | **159 pairs accepted: SUPERSESSION 99, RETRACTION 30, EXPIRY 30; pending {'SUPERSESSION': 1}**; 40 personas; at the cap in supersession: elena, fatima, jake, kenji, kofi, lily, marcus, priya, raj, thanh, tom, yoli. Last accepted position: expiry 44, retraction 419, supersession **226**. 35 excluded in all (1 authoring predicate, 31 PN read after re-read, 3 PN read by identity), 3 of them former replacements (chains followed in `verify_cf2.py` check I). `meta.pending_draft`: the 26 new replacements, awaiting question and record (§2j). |
| accepted per persona (SUP / RET / EXP), after the walk | aisha 0/3/2, alex 2/0/0, amara 3/0/0, aroha 2/1/0, billy 1/1/1, bruna 3/1/0, callum 3/1/2, chenoa 1/1/0, dariush 0/0/3, david 1/0/2, diane 0/0/2, dmitri 3/1/0, elena 4/1/3, fatima 4/0/3, ingrid 2/1/0, jake 4/1/2, jerome 2/0/1, joonho 3/0/0, kenji 4/0/0, kofi 4/1/1, leila 2/1/0, lily 4/1/0, marcus 4/1/3, marley 1/2/2, mehmet 3/0/2, mirri 2/0/0, nadia 1/1/0, omar 3/1/0, pan 2/2/1, patrick 2/1/0, priya 4/2/0, raj 4/2/0, rosa 1/1/0, saga 2/1/0, samuel 1/0/0, thanh 4/0/0, tom 4/0/0, valentina 3/0/0, yoli 4/1/0, zara 2/0/0 |

## 2j. AUX-CF2-CONSTRUCTION and AUX-CF2-ADJUDICATION — the 26 replacements drafted and authored; the supersession queue extended a second time (13 Sep 2026; gpt-4.1-mini and text-embedding-3-small only; nothing on the Anthropic key)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (replacement questions, batch 2) | `cf2_draft_questions.py --only` × 26 through the frozen renderer (sha `b748247b…`, seed 42): **26 questions, all first pick, 0 substitutions, 0 redrafts**, all through the intent gate; **$0.0050**. `cf_questions_cf2.json` now **159 rows**, questions sha256 `afe3747d5f1e0894fa7c3a03941d4c61e12d09b32f0ab52cfa9c1bf9be053e70`; cumulative drafting spend $0.0383. |
| **AUX-CF2-CONSTRUCTION** (replacement PN records, batch 2) | `cf2_author_pn.py --only` × 26 through `author_pn.py` unchanged (sha `b6f53b1a…`, seed 42): **26 records, 0 retries, no predicate STOP**; n_discr old 5–16, new 7–16; detector 1.00 on every original; **$0.0043**. `cf_pn_texts_cf2.json` now **159 records** (129 authored: 99 supersession + 30 retraction; 30 anchor-only); cumulative authoring spend $0.0277. `meta.pending_draft` empty. |
| **AUX-CF2-ADJUDICATION** (supersession extension 2) | `select_pairs.py --cf2 --extend SUPERSESSION --n 30`: the walk continued from **position 229 to 272** — **30 readable candidates**, **14 skipped** (12 personas at the cap — elena, fatima, jake, kenji, kofi, lily, marcus, priya, raj, thanh, tom, yoli — and joonho `hobby` by name). Sizing: pending 1 + expected read failures **7.0** of the 28 records awaiting the author's read (26 first reads + 2 re-reads, at 1 − 0.75) = shortfall 8.0; eligibility observed **133 / 213 = 0.6244** (positions 1–228); expected reads **17.08**; 30 printed. **The cap now binds on 12 of 40 personas**: 14 of the 44 positions walked were unreadable. |
| Read file | `reviews/CF2_PN_READ_EXT2.md`: Part A the 26 records (138–163) + re-reads 35 (david `reading_preferences_narrative_nonfiction`) and 37 (tom `vehicle_use`); Part B the 26 questions (168–193); Part C = `reviews/CF2_ADJUDICATION_READ_EXT2.md` from its criteria heading, verbatim (positions 229–272). |
| Spend today (13 Sep, all steps) | re-read merge $0; batch exclusions $0; questions $0.0064; PN $0.0055; re-authoring $0.0008; extensions $0 — **$0.0128**, OpenAI only. CF-2 OpenAI construction spend to date: questions $0.0383 + PN $0.0277 + re-authoring $0.0063 = **$0.0723** of the $22 line. |

## 2k. AUX-CF2-PNREAD, AUX-CF2-QUESTIONREAD, AUX-CF2-ADJUDICATION — the author's third read (13 Sep 2026; `cf2/cf2_ext2_13sep.json`, sha256 `f6b5dd3d100bb1bf…`; PN and question rows merged by (state, persona, entry_id), adjudication rows by printed position; every row checked against `reviews/CF2_PN_READ_EXT2.md`)

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** (records 138–163) | Three-way read of the 26 batch-2 replacement records: **13 YES** (138, 139, 144, 145, 149, 152, 154, 155, 157, 158, 159, 161, 163), **13 NO** — 3 paraphrase (141 chenoa `perspective:chronic_condition_management`, 147 kofi `health_condition:tiredness`, 148 lily `health_management:eczema_cotton_gloves`), 10 implausible (140 callum, 142 dmitri, 143 elena, 146 jerome, 150 mehmet, 151 mehmet, 153 omar, 156 priya, 160 tom, 162 valentina). Letters model-assigned from the author's bare NO (disclosed). Pass rate on this batch **0.50**, against the 0.75 the sizing assumed and 0.70 / 0.29 on the two earlier batches. Cumulative first reads: 163 records — supersession 83 YES / 27 NO-paraphrase / 22 NO-implausible, retraction 30 YES / 1 NO-implausible. |
| **AUX-CF2-PNREREAD** (re-reads 35, 37) | david `reading_preferences_narrative_nonfiction` NO-paraphrase; tom `vehicle_use` NO-implausible — **both fail the re-read and fall to D-CF2-2**. Re-read tally across the run: 37 re-authored, 1 YES, 36 fail (18 by identity, 18 on re-read). |
| **AUX-CF2-QUESTIONREAD** (168–193) | **14 of 26 flagged** (168, 170, 174–179, 182, 184, 188, 189, 191, 192); cumulative **107 of 193**. Disclosure, not a gate. |
| **AUX-CF2-ADJUDICATION** (supersession extension 2, positions 229–272) | The 30 readable candidates: **13 ELIGIBLE, 17 INELIGIBLE**, no rank-skip; the 14 pre-skipped recorded (`SKIP-CAP` 13, `SKIP-NAME` 1). Note and rows agree. Supersession to date: **243 verdict reads, 146 ELIGIBLE, rate 0.6008** (extension 2 alone 13/30 = 0.433); stop at 272. |
| author's notes verbatim | (1) 13 Sep 2026, third read: records 138-163 and re-reads 35/37: 13 YES, 15 NO (4 paraphrase, 11 implausible; letters model-assigned from the author's bare NO, disclosed). Questions 168-193: 14 flagged. Extension 229-272: 13 ELIGIBLE, 17 INELIGIBLE of 30 readable. (2) Author's ruling: with 16 replacements needed (15 failures plus 1 pending) against 13 eligible in reserve and the persona cap binding on 12 of 40 personas, the supersession quota drops by the residual shortfall after the D-CF2-3 retry and the walk over 229-272, under a deviation stating the reason (authoring failure rate on attitude slots, cap saturation, queue thinning). No further extension. n remains above 470. (3) Method as before: records presented by a language model, verdicts typed by the author, disclosed. |

## 2l. AUX-CF2-PNREAD and AUX-CF2-CONSTRUCTION — D-CF2-3 third round; the last D-CF2-2 walk (positions 229–272); D-CF2-4 recorded (13 Sep 2026)

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** (D-CF2-3, third round) | The 13 first-read NOs of `CF2_PN_READ_EXT2.md` re-authored once at seed 4242 (`author_pn` unchanged, retries 0, $0.0021; `cf_pn_texts_cf2_reauthor_4242.json` now 50 records): **8 byte-identical** → NO stands by identity → excluded; **5 changed** → one last read (`CF2_PN_READ_EXT3.md`). The 2 re-reads (35 david, 37 tom) failed → excluded. Identity across the run: **26 of 50**; the retry has restored **1 record in 50**. |
| **AUX-CF2-CONSTRUCTION** (D-CF2-2, last walk) | 10 excluded (8 identity, 2 re-read), pending 11; the walk over 229–272 accepted **11 replacements, positions 230–263** (aisha:skill_development:soft_skills (230), omar:clothing_habit (232), bruna:marital_status (233), chenoa:health_belief:traditional healing (240), david:reading_volume (241), aroha:health_metric:fasting_blood_sugar (242), diane:favorite_scents_combination (243), mirri:health_condition:back_discomfort (245), pan:business_preference (252), leila:work_style_preference (261), valentina:job_attitude (263)); all zero-overlap, none O3. **Supersession 100, pending 0.** Beyond the fill point: 0264 patrick `communication_preference:trauma` (admissible, unused), 0272 omar `income_pattern` (omar at the cap). |
| **AUX-CF2-CONSTRUCTION** (D-CF2-4) | **Quota fixed at 100 / 30 / 30 (residual 0); no further extension.** From here a record failing its read is excluded with no replacement and N_sup drops by one. **16 records await a read** (11 new + 5 changed re-authors); at the last batch's pass 0.50 the expectation is N_sup ≈ 92, n ≈ 456; **if more than 10 of the 16 fail, n < 450 and the §14 power figures must be re-run** (D-CF2-4, §16). Replacements accepted in the run: **45**; excluded in all: **45** (1 authoring predicate, 33 read failures after the frozen retry, 11 NOs standing by identity), **13 of them former replacements** (chains followed in check I). |
| **AUX-CF2-CONSTRUCTION** (state of the draw) | **160 pairs accepted: SUPERSESSION 100, RETRACTION 30, EXPIRY 30**; 40 personas; at the cap in supersession: bruna, elena, fatima, jake, kenji, marcus, omar, priya, raj, thanh, yoli. Last accepted position: expiry 44, retraction 419, supersession **263**. Supersession queue read to 272: 243 verdict reads, 146 ELIGIBLE (rate 0.6008), of which 100 accepted, 43 excluded, 3 not drawn (0215 elena at the cap, 0264 patrick beyond the fill point, 0272 omar at the cap). `meta.pending_draft`: the 11 new replacements (§2m). |
| accepted per persona (SUP / RET / EXP) | aisha 1/3/2, alex 2/0/0, amara 3/0/0, aroha 3/1/0, billy 1/1/1, bruna 4/1/0, callum 2/1/2, chenoa 2/1/0, dariush 0/0/3, david 1/0/2, diane 1/0/2, dmitri 2/1/0, elena 4/1/3, fatima 4/0/3, ingrid 2/1/0, jake 4/1/2, jerome 2/0/1, joonho 3/0/0, kenji 4/0/0, kofi 3/1/1, leila 3/1/0, lily 3/1/0, marcus 4/1/3, marley 1/2/2, mehmet 1/0/2, mirri 3/0/0, nadia 1/1/0, omar 4/1/0, pan 3/2/1, patrick 2/1/0, priya 4/2/0, raj 4/2/0, rosa 1/1/0, saga 2/1/0, samuel 1/0/0, thanh 4/0/0, tom 2/0/0, valentina 3/0/0, yoli 4/1/0, zara 2/0/0 |

## 2m. AUX-CF2-CONSTRUCTION — the 11 replacements of the last walk drafted and authored; the last read file (13 Sep 2026; gpt-4.1-mini and text-embedding-3-small only; nothing on the Anthropic key)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (replacement questions, batch 3) | `cf2_draft_questions.py --only` × 11 (frozen renderer, seed 42): **11 questions, all first pick, 0 substitutions, 0 redrafts**, all through the intent gate; **$0.0021**. `cf_questions_cf2.json`: **160 rows**, questions sha256 `e20facf6e7fb44b53b2616f8c407c381c7a1b63a76d99f3521fb4c1a76ba0097`; cumulative $0.0404. |
| **AUX-CF2-CONSTRUCTION** (replacement PN records, batch 3) | `cf2_author_pn.py --only` × 11 (`author_pn.py` unchanged, seed 42): **11 records, 0 retries, no predicate STOP**; n_discr old 6–12, new 6–15; detector 1.00 on every original; **$0.0018**. `cf_pn_texts_cf2.json`: **160 records** (130 authored: 100 supersession + 30 retraction; 30 anchor-only); cumulative $0.0295. `meta.pending_draft` empty. |
| Read file | `reviews/CF2_PN_READ_EXT3.md`: Part A the 11 records (164–174) + re-reads 39 chenoa, 41 elena, 42 jerome, 47 omar, 48 priya (last reads); Part B the 11 questions (194–204); **no Part C** (D-CF2-4). A NO anywhere in the file excludes the pair with no replacement; N_sup ∈ [84, 100] after this read. |
| Spend today (13 Sep, all steps) | questions $0.0085; PN $0.0073; re-authoring $0.0029; merges, walks, extensions $0 — **$0.0187**, OpenAI only. CF-2 OpenAI construction spend to date: questions $0.0404 + PN $0.0295 + re-authoring $0.0084 = **$0.0783** of the $22 line. |

## 2n. AUX-CF2-PNREAD, AUX-CF2-PNREREAD, AUX-CF2-QUESTIONREAD — the author's final read (13 Sep 2026; `cf2/cf2_ext3_13sep.json`, sha256 `9bf72390f1793223…`; merged by (state, persona, entry_id), every row checked against `reviews/CF2_PN_READ_EXT3.md`)

| Key | Value |
|---|---|
| **AUX-CF2-PNREAD** (records 164–174) | **4 YES** (165 aroha `health_metric:fasting_blood_sugar`, 166 bruna `marital_status`, 168 david `reading_volume`, 174 valentina `job_attitude`), **7 NO** — 2 paraphrase (164 aisha `skill_development:soft_skills`, 167 chenoa `health_belief:traditional healing`), 5 implausible (169 diane, 170 leila, 171 mirri, 172 omar `clothing_habit`, 173 pan). Letters model-assigned from the author's bare NO (disclosed). Pass on this batch **0.36**. **Cumulative first reads, closed: 174 records — supersession 87 YES / 29 NO-paraphrase / 27 NO-implausible; retraction 30 YES / 1 NO-implausible** (`meta.counts`: {'RETRACTION|NO-implausible': 1, 'RETRACTION|YES': 30, 'SUPERSESSION|NO-implausible': 27, 'SUPERSESSION|NO-paraphrase': 29, 'SUPERSESSION|YES': 87}). |
| **AUX-CF2-PNREREAD** (re-reads 39, 41, 42, 47, 48) | All five NO (RE39 chenoa paraphrase; RE41 elena, RE42 jerome, RE47 omar `value_system`, RE48 priya implausible). **Re-read tally, closed: 50 re-authored at seed 4242 — 1 YES, 49 fail (26 by identity, 23 on re-read).** |
| **AUX-CF2-QUESTIONREAD** (194–204) | **4 of 11 flagged** (195, 197, 201, 202); **cumulative 111 of 204**. Disclosure, not a gate. |
| **Failures under D-CF2-4** | **12 of the 16 records awaiting a read failed** (7 first reads + 5 last re-reads) — above the 10 at which §16's conditional power re-run fires. Disposition in §2o. |
| **Construction telemetry, author's summary** (verbatim, note 3) | Construction telemetry across CF-2: PN read pass rate on supersession records 0.59 (first 100: 0.69; replacements: 0.42 to 0.50); the frozen seed-4242 retry restored 1 of 50; supersession eligibility 0.60 over 273 walked positions with the cap binding on 12 of 40 personas by position 272. |
| author's notes verbatim | (1) 13 Sep 2026, final read: records 164-174: 4 YES (165, 166, 168, 174), 7 NO; re-reads 39, 41, 42, 47, 48: all NO. Letters model-assigned from the author's bare NO (164, 167, RE39 paraphrase; the rest implausible), disclosed. Questions 194-204: 4 flagged. (2) Consequence under D-CF2-4: 12 failures; patrick 0264 fills one as the last spare (author's ruling); the supersession quota drops by the residual 11 to N_sup = 89, composition 89/30/30, n = 447. More than 10 of the 16 failed, so the conditional power re-run at the final composition fires before any store version; P1 below 0.80 is a STOP. (3) Construction telemetry across CF-2: PN read pass rate on supersession records 0.59 (first 100: 0.69; replacements: 0.42 to 0.50); the frozen seed-4242 retry restored 1 of 50; supersession eligibility 0.60 over 273 walked positions with the cap binding on 12 of 40 personas by position 272. (4) Method as before: entries presented by a language model, verdicts typed by the author, disclosed under the AI-use line. |

## 2o. AUX-CF2-CONSTRUCTION — D-CF2-4 applied to the 12 failures of the final read (13 Sep 2026; `select_pairs.py --cf2 --exclude-d4`; `cf_pairs_cf2.json` `meta.quota`, `meta.quota_history`)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (D-CF2-4 exclusions) | **12 pairs excluded with no replacement**, in walk order: priya:cognitive_style (167), elena:work_stress_carryover (175), omar:value_system (192), chenoa:perspective:chronic_condition_management (200), jerome:health_condition:trauma_flashbacks (226), aisha:skill_development:soft_skills (230), omar:clothing_habit (232), chenoa:health_belief:traditional healing (240), diane:favorite_scents_combination (243), mirri:health_condition:back_discomfort (245), pan:business_preference (252), leila:work_style_preference (261) — 7 first-read NOs (no retry: D-CF2-4 forecloses replacement) and 5 last-read NOs after the seed-4242 retry; every one keeps its ELIGIBLE verdict and carries both reads. Question rows and PN records moved to `meta.excluded_*`. **Quota now 88 / 30 / 30; accepted 88 / 30 / 30; n = 444.** |
| **AUX-CF2-CONSTRUCTION** (the spare — awaiting the author's ruling) | The author ruled "patrick 0264 is the one spare" on the report that 0264 was the only admissible ELIGIBLE row beyond the fill point. **The 12 exclusions freed two more:** elena (`work_stress_carryover` excluded → 3 in supersession) makes **0215 elena `mental_transition_routine` admissible — and it precedes 0264 in walk order**; omar (`value_system`, `clothing_habit` excluded → 2) makes **0272 omar `income_pattern`** admissible. Three admissible spares: 0215 elena, 0264 patrick, 0272 omar. Under D-CF2-2's walk-order rule one spare = 0215 elena; the author named patrick; taking all three would give N_sup = 91. **No spare drawn, nothing drafted, until the author rules**; `verify_cf2.py` check I lists 0215 as "admissible but undrawn under no-replacement". |
| **AUX-CF2-CONSTRUCTION** (state of the draw) | **148 pairs accepted: SUPERSESSION 88, RETRACTION 30, EXPIRY 30**; 40 personas; at the cap in supersession: bruna, fatima, jake, kenji, marcus, raj, thanh, yoli. Excluded in all: **57** (1 authoring predicate, 33 read failures after retry, 11 by identity, 12 under D-CF2-4), 25 of them former replacements. Reads closed: 174 first reads, 50 re-reads; `meta.pending_draft` empty; nothing awaits a read. |
| **Power** | §16 conditional fired (12 > 10 failures): the Phase 3 script re-run at 89/30/30 — **P1 0.994, P2 (Haiku) 1.000, P3 (Haiku) 1.000** (§3a). |

## 2p. AUX-CF2-CONSTRUCTION — the draw closed (13 Sep 2026; author's ruling: no spare)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (final) | **148 pairs: SUPERSESSION 88, RETRACTION 30, EXPIRY 30; composition 88 / 30 / 30; n = 444 items.** `meta.quota` 88/30/30, `meta.quota_history` closed with `final: true`. 40 personas; cluster unit persona. Undrawn ELIGIBLE rows, listed as the ruling requires: **0215 elena `mental_transition_routine`, 0264 patrick `communication_preference:trauma`, 0272 omar `income_pattern`** — admissible after the D-CF2-4 exclusions, not drawn (no spare). Supersession queue read to position 272: 243 verdict reads, 146 ELIGIBLE, of which 88 accepted, 55 excluded, 3 undrawn. Retraction: 30 of 35 ELIGIBLE accepted (last position 419); expiry: 30 (last position 44). |
| **AUX-CF2-OVERLAP** (final) | O1 7 (billy, david, elena, fatima, marcus, marley, mehmet expiry pairs), O2 0, O3 15 expiry pairs from the widened class; none of the 45 D-CF2-2 replacements carried a tag. |
| Reads closed | first reads 174 (supersession 87 YES / 29 paraphrase / 27 implausible; retraction 30 / 1), re-reads 50 (1 YES), question flags 111 of 204. PN read pass on supersession records, overall **87 / 143 = 0.61**. |
| Power | 89/30/30 run covers 88/30/30 within three items (§3a): P1 0.994, P2 1.000, P3 1.000. No re-run (ruling). |

## 3. AUX-CF2-POWER — the Phase 3 script at the registered and amended compositions

`reviews/CF2_SCOPE.md` Phase 3 script (md5 `a40d810f…`), per-state draw counts set to the
composition, 1,000 outer draws, seed 42, gate to 1e-9 passed on every run. Share of draws whose
item-level interval lower bound exceeds zero / excludes zero either side. Full grid tables in
`reviews/CF2_REG_REPORT.md` Step A; the 100/30/30 run added 2026-09-12 for D-CF2-1.

| Reading | 100/100/30 (n=690) | 100/100/60 (n=780) | 100/60/30 (n=570, frozen §3) | **100/30/30 (n=480, §14)** |
|---|---:|---:|---:|---:|
| P1 — mini whole cell v2 | 1.000 | 1.000 | 0.999 | **0.997** |
| P2 — Haiku 4.5 named − counted, v2 | 0.999 | 1.000 | 0.998 | **1.000** |
| P2 conditional — Opus 5 named − counted, v2 | 1.000 | 1.000 | 1.000 | 1.000 |
| P3 — Haiku 4.5 counted paired v3 − v2 | 1.000 | 1.000 | 1.000 | **1.000** |
| mini descriptive — supersession v2 | 0.990 | 0.993 | 0.998 | 0.995 |
| mini descriptive — retraction v2 | 0.902 | 0.887 | 0.517 | 0.107 |
| mini descriptive — expiry v2 | 0.055 | 0.241 | 0.047 | 0.044 |
| mini descriptive — named − counted v2 | 0.401 | 0.395 | 0.313 | 0.200 |
| mini descriptive — counted paired v3 − v2 | 1.000 | 1.000 | 0.993 | 0.828 |
| Haiku descriptive — retraction v2 / v3 | 0.858 / 1.000 | 0.848 / 1.000 | 0.378 / 1.000 | 0.044 / 0.885 |
| Opus descriptive — retraction v2 / v3 | 0.319 / 1.000 | 0.322 / 1.000 | 0.034 / 1.000 | 0.003 / 0.841 |

At 100/30/30 all three registered readings clear 0.80 (P1 0.997, P2 1.000, P3 1.000). What the
amendment gives up is confined to descriptive rows: mini's counted paired reading falls to 0.828
and every reader's retraction-v2 row is unpowered. Persona-clustered power is not simulated
(caveat 3 of the scope).

### 3a. AUX-CF2-POWER at 89/30/30 (n = 447) — the §16 conditional re-run, 13 Sep 2026

Fired because 12 of the 16 records awaiting a read failed (> 10). Same script (`cf2/power/power_sim_comp.py`, md5 `55ce5637…`, the Phase 3 script with the composition edit of `CF2_REG_REPORT.md` Step A), outer 1000 × inner 1000, seed 42; all three lanes reproduced the committed CF-1 item intervals to 1e-9 before drawing; outputs deposited in `cf2/power/out_*_89-30-30.jsonl` (elapsed MINI 127.7s, H45 128.1s, OP5 135.1s). Share of draws with the item-level 95% interval above zero:

| Reading | 89/30/30 (n=447) | 100/30/30 (n=480, §14) |
|---|---:|---:|
| P1 — mini whole cell v2 | **0.994** | see §3 |
| P2 — Haiku supersession − counted, v2 | **1.000** | see §3 |
| P3 — Haiku counted paired v3 − v2 | **1.000** | see §3 |
| P2 / P3 — Opus (conditional) | **1.000 / 1.000** | see §3 |
| mini descriptive — supersession v2 | **0.982** | see §3 |
| mini descriptive — retraction v2 | **0.103** | see §3 |
| mini descriptive — expiry v2 | **0.049** | see §3 |
| mini descriptive — named − counted v2 | **0.161** | see §3 |
| mini descriptive — counted paired v3 − v2 | **0.852** | see §3 |
| Haiku descriptive — retraction v2 / v3 | **0.044 / 0.903** | see §3 |
| Opus descriptive — retraction v2 / v3 | **0.000 / 0.847** | see §3 |

**P1 = 0.994 ≥ 0.80: the §16 conditional clears; P2 and P3 on Haiku 1.000.** Composition 89/30/30 assumes the one spare is accepted and passes its read; at 88/30/30 (n = 444) the reading would move by at most the three items and is not separately simulated — if the spare fails, the script is re-run at 88/30/30 before any store version. Persona-clustered power not simulated (scope caveat 3 stands). The 100/30/30 outputs are deposited beside these (`cf2/power/out_*_100-30-30.jsonl`).

## 4. Keys reserved and not yet written

`AUX-CF2-INDIVIDUATION`, `-INDEXSIZE`, `-V2R-DEF`, `-LEAKSCREEN-V3`,
`-LEAKSCREEN-V2R`, `-BLIND`, `-MINI-V2`, `-MINI-V3`, `-MINI-V2R`, `-H45-V2`, `-H45-V3`, `-H45-V2R`,
`-OP5-V2`, `-OP5-V3`, `-OP5-V2R`, `-PERSTATE`, `-COUNTED`, `-NAMEDVSCOUNTED`, `-EQUIV-V2R`,
`-NB6-V2`, `-ALLSTATES-V3`, `-NB5-V2`, `-FOK`, `-SPEND`, `-DROPRULE` (evaluated 2026-09-19).

## 5. CF2-BUILD-3 — the build (13 Sep 2026; `registrations/ADDENDUM_CF2.md` §2, §5; `cf2_build_cell.py`, `index_v2r.py`)

### 5a. AUX-CF2-V2R-DEF — written BEFORE any index exists

| Key | Value |
|---|---|
| **AUX-CF2-V2R-DEF** | `r82_counterfactual/index_v2r.py` (sha256 `ea4a7e4c1b196bf9…`) wraps the OUTPUT of `index_v2.render` (called upstream, never edited or copied) and rewrites **exactly two fields**: the `LIFECYCLE TOTALS` lines `  retracted             N` and `  expired               N`, located by label (asserted exactly one each), the label's 24-character prefix preserved. **Permutation:** the cell's (retracted, expired) pairs — one per store version, 444 — are permuted across versions by a **value-level derangement under seed 42**: positions grouped by value, shuffled within and across groups (`numpy.random.default_rng(42)`), laid out in a line and rotated by k drawn uniformly from [largest group, n − largest group]; a rotation in that band moves every position out of its own value group, so **no version keeps its own pair and every value keeps its multiplicity** (exists iff the largest group ≤ n/2; asserted). The realized k and the version→version map are recorded in `cf2/cf_indexes.json` `meta.v2r` at build. **Assertion (RENDERER LOCK, `index_v2r.assert_lock`):** same line count, every differing line is one of the two count lines, the labels unchanged — asserted per version at render and again by `verify_cf2.py` check E. **Disclosed:** the `PER-CATEGORY BREAKDOWN` keeps its RETRACT / EXPIRED columns, so a reader summing a column recovers the true totals; §5 names exactly two fields and that is what moves. |

### 5b. AUX-CF2-CONSTRUCTION (store versions), AUX-CF2-INDIVIDUATION, AUX-CF2-INDEXSIZE — build step 1 (`cf2_build_cell.py`, sha256 `f99c090196f0bc4f…`; no model call)

| Key | Value |
|---|---|
| **AUX-CF2-CONSTRUCTION** (store versions) | **444 items = 148 pairs × 3 versions (PRESENT / ABSENT / PN), composition 88 / 30 / 30; 148 PN positives**; every version returns its intended label under Definition 1 (assertion A: 444/444). Write path (B): 118 non-expiry PN versions append the successor on the same `slot_key` at confidence 0.9; the supersession branch fires where 0.9 clears the category threshold — 65 non-ACCUMULATE pairs (threshold 0.80, original deactivated, `supersedes` set) and **53 ACCUMULATE-category pairs where 0.9 < 0.95 and the branch does not fire** (both entries stay active, no pointer — a legitimate write-path outcome, recorded not forced, as CF-1); 30 expiry PN versions move the anchor to cutoff − 30 d (all strictly before cutoff) and append `status: expired`. Assertion C on the emitted text: 148/148 (retraction PN names on the v3 retracted list and off the v2 superseded list; expiry PN on the v3 expired list only; supersession PN on the superseded list). D (base leak / category ablation) and E (v3 extends v2 byte-identically): 444/444. `cf2/cf_cell.json`, `cf2/cf_indexes.json` (v2, v3), indexes sha256 `b423c34ed6b16c3d…`. **`meta.fails` = []**. |
| **AUX-CF2-INDIVIDUATION** | Draw-time predicates re-asserted at build: **148 / 148 pairs individuate** (scrubbed name absent from its own state's v3 section in PRESENT, present in PN) and **0 / 148 collide with the v2 superseded list in PRESENT** — no collision row prints; the pooled counted-state population is the full 60 pairs (30 retraction + 30 expiry, 180 items). |
| **AUX-CF2-INDEXSIZE** | v2: 58–69 lines, mean 4257.4 chars; v3: 64–75 lines, mean 4445.4 chars (V2R = v2's size by the lock). Entries per store version 223–623. |

### 5c. AUX-CF2-V2R-DEF (realized) — build step 2 (`cf2_build_cell.py --v2r`; no model call)

| Key | Value |
|---|---|
| **AUX-CF2-V2R-DEF** (realized permutation) | 444 store versions; **42 distinct (retracted, expired) pairs**, largest value group 47 (≤ 222, so a value-level derangement exists); rotation **k = 390** under seed 42; **0 versions keep their own pair; the multiset of pairs is preserved**; **444 of 444 V2R texts differ from their v2** (every version differs on at least one of the two lines by construction). RENDERER LOCK asserted on every version at render (`index_v2r.assert_lock`) and by `verify_cf2.py` check E: **every V2R differs from its v2 only on the two count lines**. `cf2/cf_indexes.json` `meta.arms` = [v2, v3, v2r]; `meta.v2r.permutation` is the version → source-version map; V2R sha256 `c2238bd6b90346d8…`. |

### 5d. AUX-CF2-LEAKSCREEN-V3, AUX-CF2-LEAKSCREEN-V2R — build step 3 (`cf2_leakscreen.py`; gpt-4.1-mini, served `gpt-4.1-mini-2025-04-14`; `cf2/results/leakscreen_cf2.json`)

ladder_e1's screen reproduced on the CF-2 cell: the 30 PRESENT items drawn by `random.Random(42).sample` from the 148 sorted by item_id, `prompts_e1` LEAKAGE prompts (file sha `337d37d3414c…`, texts sha `35d9b968ffc0…`), temperature 0, seed 42, max_tokens 200; scorer `supports_correct` against the pair's `entry_text`; a cell leaks iff more than 3 of 30 score correct.

| Key | Value |
|---|---|
| **AUX-CF2-LEAKSCREEN-V3** | **0 of 30 correct — PASS** (6 non-UNKNOWN answers, none matching the gold at the scorer's threshold; 0 parse failures). $0.0157. |
| **AUX-CF2-LEAKSCREEN-V2R** | **0 of 30 correct — PASS** (5 non-UNKNOWN, 0 parse failures). $0.0150. |
| v2 beside (not a registered screen) | 1 of 30 correct — PASS (cf2:jake:project:lake_trip_presidents_day_weekend|PRESENT: the answer "You have an entry related to a friend group lake trip under the RELATI" shares content tokens with the gold at the threshold; the index carries attribute names, so a name-shaped answer can overlap the stored value). $0.0150. |
| Spend | $0.0456, OpenAI; the 90 calls are the screen's, not a lane's. |

### 5e. The mini lane — build step 4 (`cf2_run.py` through `run_cf.py`; `cf2_score.py`; `cf2/rows/rows_MINI.jsonl`, `cf2/results/cf_scores_cf2.json`)

Probe (E1.7 rule): served `gpt-4.1-mini-2025-04-14`, identifier ok; blind 481 / v2 1684 / v3 1740 input tokens. Projection against §10 before launch: 1,480 calls, $0.99 expected, $1.29 at ×1.3 against the **$2** line — under. Run: BLIND 148 (one per question), INDEXED-V2 / -V3 / -V2R 444 each, k = 1, temperature 0, synchronous, `prompts_e1` digests asserted at import; **1,480 rows, 1,480 OK, 0 parse failures**; served `gpt-4.1-mini-2025-04-14` on every row. Estimators: item-level paired bootstrap primary, persona-clustered beside (cluster unit persona, 40 clusters), D.2 rule; tolerance 0.05.

| Key | Value |
|---|---|
| **AUX-CF2-BLIND** | 0.5000 on every lane and arm, by the §6 identity (one blind call per question, reused across its three versions). Printed, not suppressed. |
| **AUX-CF2-MINI-V2** | **0.7167** (blind 0.5000 by identity; Δ +0.2167); item [+0.1494, +0.2846]*, persona-clustered [+0.1663, +0.2649]* — agree; indexed persona-clustered [+0.6663, +0.7649]; 1000 draws each, seed 42 |
| **AUX-CF2-MINI-V3** | **0.7967** (blind 0.5000 by identity; Δ +0.2967); item [+0.2314, +0.3568]*, persona-clustered [+0.2438, +0.3478]* — agree; indexed persona-clustered [+0.7438, +0.8478]; 1000 draws each, seed 42 |
| **AUX-CF2-MINI-V2R** | **0.7179** (blind 0.5000 by identity; Δ +0.2179); item [+0.1479, +0.2857]*, persona-clustered [+0.1691, +0.2638]* — agree; indexed persona-clustered [+0.6691, +0.7638]; 1000 draws each, seed 42 |
| **AUX-CF2-H45-V2** | — Haiku 4.5 batch submitted (step 5), not yet collected; row fills when the lane is scored |
| **AUX-CF2-H45-V3** | — Haiku 4.5 batch submitted (step 5), not yet collected; row fills when the lane is scored |
| **AUX-CF2-H45-V2R** | — Haiku 4.5 batch submitted (step 5), not yet collected; row fills when the lane is scored |
| **AUX-CF2-OP5-V2** | — lane not run: the drop rule of §11 is evaluated on 2026-09-19, after the Haiku 4.5 lane is scored (AUX-CF2-DROPRULE) |
| **AUX-CF2-OP5-V3** | — lane not run: the drop rule of §11 is evaluated on 2026-09-19, after the Haiku 4.5 lane is scored (AUX-CF2-DROPRULE) |
| **AUX-CF2-OP5-V2R** | — lane not run: the drop rule of §11 is evaluated on 2026-09-19, after the Haiku 4.5 lane is scored (AUX-CF2-DROPRULE) |
| **AUX-CF2-PERSTATE** (mini, descriptive) | v2: EXPIRY (n 90, pos 30) indexed **0.5489**, paired item [-0.1022, +0.1893], persona [-0.0200, +0.1293]; RETRACTION (n 90, pos 30) indexed **0.5283**, paired item [-0.1204, +0.1577], persona [-0.0583, +0.1228]; SUPERSESSION (n 264, pos 88) indexed **0.8308**, paired item [+0.2480, +0.4070]*, persona [+0.2666, +0.3988]*. v3: EXPIRY (n 90, pos 30) indexed **0.5869**, paired item [-0.0524, +0.2230], persona [+0.0127, +0.1684]*; RETRACTION (n 90, pos 30) indexed **0.8725**, paired item [+0.2573, +0.4926]*, persona [+0.2971, +0.4307]*; SUPERSESSION (n 264, pos 88) indexed **0.8444**, paired item [+0.2610, +0.4256]*, persona [+0.2729, +0.4111]*. v2r: EXPIRY (n 90, pos 30) indexed **0.5144**, paired item [-0.1317, +0.1534], persona [-0.0576, +0.0840]; RETRACTION (n 90, pos 30) indexed **0.4950**, paired item [-0.1552, +0.1359], persona [-0.0775, +0.0788]; SUPERSESSION (n 264, pos 88) indexed **0.8500**, paired item [+0.2726, +0.4242]*, persona [+0.2886, +0.4147]*. Haiku / Opus rows: dash, as above. |
| **AUX-CF2-COUNTED** (mini, descriptive; P3's reading on the smallest reader) | Pooled counted states, 60 pairs / 180 items (all individuating by construction): v2 **0.5360** → v3 **0.7214**, paired Δ **+0.1854**, item [+0.1007, +0.2689]*, persona [+0.1000, +0.2734]*. Haiku 4.5 (the registered reader): dash, pending. |
| **AUX-CF2-NAMEDVSCOUNTED** (mini, descriptive; P2's reading on the smallest reader) | v2: named (supersession, 264 items) **0.8308** − counted (180 items) **0.5360** = **+0.2948**, two-subset interval [+0.1875, +0.3905]. v3: 0.8444 − 0.7214 = +0.1230, [+0.0204, +0.2210]. Haiku 4.5 (P2's reader): dash, pending. |
| **AUX-CF2-EQUIV-V2R** (mini; P5) | V2R − v2 on the whole cell: Δ **+0.0011**, item [-0.0282, +0.0297], persona [-0.0210, +0.0230] — **both inside [−0.05, +0.05]**. Haiku 4.5: dash, pending; Opus 5: dash (§11). |
| **AUX-CF2-NB6-V2** | Superseded-names matcher on v2 (all-MiniLM-L6-v2 max cosine, NB-6's estimator): **0.7663**, persona-clustered [+0.7226, +0.8051]; per state {'EXPIRY': 0.5, 'RETRACTION': 0.5, 'SUPERSESSION': 0.9223}. **Exceeds gpt-4.1-mini v2 (0.7167) by +0.0496 — within tolerance (P4), adverse branch prints.** |
| **AUX-CF2-ALLSTATES-V3** | All-states matcher over the three named sections of v3: **0.8756**, persona-clustered [+0.8391, +0.9111]; per state {'EXPIRY': 0.8711, 'RETRACTION': 0.7975, 'SUPERSESSION': 0.8995}. Exceeds gpt-4.1-mini on every arm and whole cell (adverse branch); P4's v3 comparison is against Haiku 4.5 — dash, pending. |
| **AUX-CF2-NB5-V2** | Whole-map matcher on v2: **0.5776**, persona-clustered [+0.5587, +0.5981]; per state {'EXPIRY': 0.5919, 'RETRACTION': 0.5758, 'SUPERSESSION': 0.5728}. Exceeds mini's counted-state rows under v2 / v2r (adverse branch). |
| **AUX-CF2-FOK** (descriptive only) | gpt-4.1-mini FOK AUROC against y_fok: v2 0.6357, v3 0.6436, v2r 0.6371. Not a registered reading. |
| **AUX-CF2-SPEND** (so far) | OpenAI, token-metered at list price from the rows (the dashboard's billed figure is not exposed by the API): mini lane **$0.9568** (2,246,659 in / 36,366 out tokens), probe ≈ $0.002, leakage screens $0.0456, construction $0.0783 → **$1.0828 of the $22 line**. Anthropic: $0 so far (Haiku batch submitted at step 5; its cost is metered at collection). |
| **AUX-CF2-DROPRULE** | — not yet evaluated: §11 fixes the evaluation to 2026-09-19, after the Haiku 4.5 lane is scored and ledgered; the Opus 5 batch is not created before then. |

**Mini verdicts (§8 texts, numbers filled):**

- **P1 — HOLDS.** On 148 questions written before any version of the store existed, and asked of three versions of the same store that differ in one attribute each, the smallest model's obligation judgment reaches 0.717 against the 0.5 a question-only reader attains here, with an interval of [+0.1494, +0.2846] (persona-clustered [+0.1663, +0.2649]). The gain survives where the question cannot carry the label.
- **P2** — Haiku 4.5: dash, pending. `gpt-4.1-mini` descriptive beside it: named − counted +0.295, two-subset [+0.1875, +0.3905] (carries no prediction, §7). Opus 5: dash (§11).
- **P3** — Haiku 4.5: dash, pending. `gpt-4.1-mini` descriptive: 0.536 → 0.721, paired +0.185, item [+0.1007, +0.2689], persona [+0.1000, +0.2734].
- **P4 (v2 half)** — On this cell the superseded-names lookup reaches 0.766 against the smallest reader's 0.717 under the superseded-only summary, within tolerance; the all-states lookup against Haiku 4.5 under the all-three-named summary prints when that lane is scored.
- **P5 (mini)** — Randomizing the retracted and expired counts in the superseded-only summary moves gpt-4.1-mini's whole-cell judgment by +0.001, intervals [-0.0282, +0.0297] (persona-clustered [-0.0210, +0.0230]), inside the tolerance band; on this cell that reader takes nothing from the counts; Haiku 4.5's row prints when that lane is scored.
- **Adverse branch (§8):** the superseded-names lookup exceeds the smallest reader on the whole cell under v2 (0.766 vs 0.717) and on supersession (0.922 vs 0.831); the all-states lookup exceeds it everywhere (0.876 whole cell); the whole-map lookup exceeds it on the counted states under v2 / v2r. Every flag is in `cf_scores_cf2.json` `flags` (22 rows) and prints in the table; no row is dropped.

### 5f. The Haiku 4.5 lane — build step 5, submitted (`cf2_run.py probe / project / submit`; `cf2/rows/batch_H45.json`)

| Key | Value |
|---|---|
| **AUX-CF2-H45-V2 / -V3 / -V2R** (submission record) | Probe (E1.7 rule, 3 calls): served **`claude-haiku-4-5-20251001`**, identifier ok; input tokens blind 525 / v2 1782 / v3 1845; output 39 / 200 / 200 (the indexed answers reach `max_tokens` 200 after the JSON object, which `last_json` parses — as CF-1). **Projection against §10 before submission: 7,400 calls, $8.91 expected, $11.58 at ×1.3 against the $16 line — under**; Anthropic total projected $8.91 of $121. **Batch `msgbatch_01Hu8kYryhnSkB8JqfcxsbhT`, 7400 requests** (BLIND 148 + 3 × 444 items, k = 5, temperature 0, `max_tokens` 200, Batch pricing ×0.5), submitted 2026-09-13; status at submission `in_progress`, 7,400 processing. Rows collect to `cf2/rows/rows_H45.jsonl` on `poll`; the three keys fill when the lane is scored. |
| **AUX-CF2-OP5-V2 / -V3 / -V2R** | Not submitted. The §11 drop rule is evaluated once, on 2026-09-19, after the Haiku 4.5 lane is scored and ledgered (`AUX-CF2-DROPRULE`); the Opus 5 probe is run then. |
| **AUX-CF2-SPEND** (Anthropic, at submission) | Probe 3 calls ≈ $0.006 (metered from tokens at list); batch cost metered at collection (expected $8.91). |

**STOP** at the end of step 5 (CF2-BUILD-3): the Haiku 4.5 batch is in flight; nothing else is submitted.

### 5g. The Haiku 4.5 lane, scored (`cf2_score.py`; `cf2/rows/rows_H45.jsonl`, `cf2/results/cf_scores_cf2.json`; 13 Sep 2026)

Batch `msgbatch_01Hu8kYryhnSkB8JqfcxsbhT` ended: **7,400 / 7,400 succeeded, 0 errored, 0 expired; every row parsed OK; 5 draws in each of the 1,480 (unit, arm) cells**; served `claude-haiku-4-5-20251001` on every row. P2's estimator is the registered two-subset difference bootstrap; the persona-clustered two-subset difference (personas drawn with replacement, both subsets moving together) prints beside it under the D.2 rule — it is not the registered estimator and is labelled so.

| Key | Value |
|---|---|
| **AUX-CF2-H45-V2** | **0.7566** (blind 0.5000 by identity; Δ +0.2566); item [+0.1942, +0.3189]*, persona-clustered [+0.2102, +0.3035]* — agree; indexed persona-clustered [+0.7102, +0.8035]; k = 5 collapsed by the X4 mean, 1000 draws, seed 42 |
| **AUX-CF2-H45-V3** | **0.8773** (blind 0.5000 by identity; Δ +0.3773); item [+0.3174, +0.4395]*, persona-clustered [+0.3362, +0.4124]* — agree; indexed persona-clustered [+0.8362, +0.9124]; k = 5 collapsed by the X4 mean, 1000 draws, seed 42 |
| **AUX-CF2-H45-V2R** | **0.7638** (blind 0.5000 by identity; Δ +0.2638); item [+0.2003, +0.3254]*, persona-clustered [+0.2193, +0.3071]* — agree; indexed persona-clustered [+0.7193, +0.8071]; k = 5 collapsed by the X4 mean, 1000 draws, seed 42 |
| **AUX-CF2-PERSTATE** (Haiku 4.5, descriptive) | v2: EXPIRY (n 90, pos 30) indexed **0.5794**, paired item [-0.0626, +0.2182], persona [+0.0234, +0.1457]*; RETRACTION (n 90, pos 30) indexed **0.5433**, paired item [-0.0799, +0.1701], persona [-0.0057, +0.0963]; SUPERSESSION (n 264, pos 88) indexed **0.8876**, paired item [+0.3072, +0.4676]*, persona [+0.3379, +0.4365]*. v3: EXPIRY (n 90, pos 30) indexed **0.8269**, paired item [+0.1935, +0.4675]*, persona [+0.2388, +0.4156]*; RETRACTION (n 90, pos 30) indexed **0.9042**, paired item [+0.2639, +0.5519]*, persona [+0.3524, +0.4545]*; SUPERSESSION (n 264, pos 88) indexed **0.8852**, paired item [+0.3050, +0.4634]*, persona [+0.3343, +0.4351]*. v2r: EXPIRY (n 90, pos 30) indexed **0.5847**, paired item [-0.0594, +0.2188], persona [+0.0351, +0.1414]*; RETRACTION (n 90, pos 30) indexed **0.5844**, paired item [-0.0564, +0.2279], persona [+0.0193, +0.1453]*; SUPERSESSION (n 264, pos 88) indexed **0.8874**, paired item [+0.3065, +0.4655]*, persona [+0.3382, +0.4339]*. |
| **AUX-CF2-COUNTED** (Haiku 4.5; **P3**) | Pooled counted states, 60 pairs / 180 items: v2 **0.5638** → v3 **0.8649**, paired Δ **+0.3010**, item [+0.2268, +0.3721]*, persona [+0.2247, +0.3591]* — both exclude zero, Δ clears tolerance: **P3 HOLDS**. |
| **AUX-CF2-NAMEDVSCOUNTED** (Haiku 4.5; **P2**) | v2: named (supersession, 264 items) **0.8876** − counted (180 items) **0.5638** = **+0.3237**, two-subset [+0.2319, +0.4011], persona-clustered [+0.2612, +0.3851] — both exclude zero, Δ clears tolerance: **P2 HOLDS**. v3 (descriptive): 0.8852 − 0.8649 = +0.0203, [-0.0570, +0.0907], persona [-0.0547, +0.0925] — naming the counted states closes the boundary. Opus 5: dash (§11). |
| **AUX-CF2-EQUIV-V2R** (Haiku 4.5; **P5**) | V2R − v2 on the whole cell: Δ **+0.0072**, item [-0.0079, +0.0229], persona [-0.0103, +0.0248] — **both inside [−0.05, +0.05]**; with mini's row (+0.0011) **P5: both readers inside the band**. Opus 5: dash (§11). |
| **AUX-CF2-ALLSTATES-V3** (P4's v3 half) | All-states lookup **0.8756** against Haiku 4.5 v3 **0.8773**: D = -0.0017, **within tolerance**, in the reader's favour by 0.0017. |
| **AUX-CF2-FOK** (Haiku 4.5, descriptive only) | v2 0.6168, v3 0.6133, v2r 0.6050. |
| **AUX-CF2-SPEND** (after the mini and Haiku lanes) | **Haiku 4.5 lane $9.0623** (Batch-priced from the returned tokens: 11,929,785 in / 1,238,972 out at $1.00 / $5.00 per M × 0.5) against the $16 line; probe ≈ $0.006. **Mini lane $0.9568** against $2. Lanes combined **$10.0192 of $18**. OpenAI to date $1.0828 of $22 (lane + probe + screens + construction); Anthropic to date $9.0683 of $130. |

**Verdicts with the Haiku lane (§8 texts):**

- **P1 — HOLDS** (mini, above).
- **P2 — HOLDS.** Under the summary that names only superseded content, Haiku 4.5's judgment on the named state exceeds its judgment on the two counted states by +0.324, interval [+0.2319, +0.4011] (persona-clustered [+0.2612, +0.3851]). `gpt-4.1-mini` descriptive beside it: +0.295, two-subset [+0.1875, +0.3905]. Opus 5: dash (§11).
- **P3 — HOLDS.** Naming retracted and expired content lifts Haiku 4.5's judgment on those states from 0.564 to 0.865 on the store-counterfactual set (60 questions), a paired gain of +0.301 with interval [+0.2268, +0.3721] (persona-clustered [+0.2247, +0.3591]). `gpt-4.1-mini` descriptive: 0.536 → 0.721, +0.185, item [+0.1007, +0.2689].
- **P4 — prints either way.** On this cell the superseded-names lookup reaches 0.766 against the smallest reader's 0.717 under the superseded-only summary, within tolerance, and the all-states lookup reaches 0.876 against Haiku 4.5's 0.877 under the all-three-named summary, within tolerance.
- **P5 — both inside the band.** Randomizing the retracted and expired counts in the superseded-only summary moves gpt-4.1-mini's whole-cell judgment by +0.001 and Haiku 4.5's by +0.007, intervals [-0.0282, +0.0297] (persona-clustered [-0.0210, +0.0230]) and [-0.0079, +0.0229] (persona-clustered [-0.0103, +0.0248]), both inside the tolerance band; on this cell neither reader takes anything from the counts. Opus 5: dash (§11).
- **Adverse branch (§8), Haiku rows:** 18 flags — the superseded-names lookup exceeds Haiku on the whole cell under v2 (0.766 vs 0.757) and v2r (0.766 vs 0.764) and on supersession under every arm (0.922 vs 0.885–0.888); the all-states lookup exceeds Haiku's v2 / v2r rows everywhere and its v3 row on supersession (0.900 vs 0.885) and expiry (0.871 vs 0.827); the whole-map lookup exceeds Haiku's counted-state rows under v2 (retraction 0.576 vs 0.543; expiry 0.592 vs 0.579) and v2r expiry. All 40 flags are in `cf_scores_cf2.json` `flags`; no row is dropped.

### 5h. AUX-CF2-DROPRULE — the §11 drop rule, evaluated 2026-09-13 by the author's ruling (D-CF2-5); `cf2/results/droprule_cf2.json`

| Key | Value |
|---|---|
| **AUX-CF2-DROPRULE** | Evaluated **once, on 2026-09-13** (the registration fixed 2026-09-19; the author moved the date forward after the Haiku lane was scored and ledgered — D-CF2-5; the once-only property is kept: this row is not re-evaluated on the 19th). **(i) Metered spend after the mini and Haiku 4.5 lanes: $0.9568 + $9.0623 = $10.0192 against their combined lines $2 + $16 = $18 — PASS.** **(ii) Opus 5 probe, three calls: served `claude-opus-5`, identifier ok; input tokens blind 693 / v2 2483 / v3 2595, output [144, 136, 134]; projection at k = 5, 7,400 calls, 17.298 M in / 1.021 M out, Batch ×0.5: $56.01, ×1.3 $72.81 against the $105 line — PASS**; Anthropic total (Haiku actual + Opus projected) $65.07, ×1.3 $84.59 against $121. **(iii) P2 and P5 name Opus 5 as a conditional branch (§7) — PASS.** **Verdict: the Opus 5 lane RUNS at k = 5** (§11: comparability with Tables 20 and 21). **Not submitted: STOP before submission on the author's instruction; the batch is created only on GO.** |

### 5i. The Opus 5 lane — submitted on the author's GO (13 Sep 2026; `cf2_run.py submit claude-opus-5`; `cf2/rows/batch_OP5.json`)

| Key | Value |
|---|---|
| **AUX-CF2-OP5-V2 / -V3 / -V2R** (submission record) | The §11 rule evaluated and ledgered first (`AUX-CF2-DROPRULE`, §5h: RUN). **Batch `msgbatch_014ADrDKGmyQuxCdzzrJjg6c`, 7,400 requests** (BLIND 148 + 3 × 444 items, **k = 5**, temperature unset, `max_tokens` 1024, Batch pricing ×0.5), submitted 2026-09-13 after the mini and Haiku 4.5 lanes were scored; status at submission `in_progress`, 7,400 processing. Projected $56.01 against the $105 line. The three keys fill when the lane is scored; P2 and P5's Opus branches print HELD / FAILED then. |

### 5j. The Opus 5 lane, scored (`cf2_score.py`; `cf2/rows/rows_OP5.jsonl`, `cf2/results/cf_scores_cf2.json`; 13 Sep 2026)

Batch `msgbatch_014ADrDKGmyQuxCdzzrJjg6c` ended: **7,400 / 7,400 succeeded**, 0 errored, 0 expired; **7,398 parsed OK, 2 PARSE_FAIL** (cf2:kofi:project:cocoa_farm_replanting_schedule|PRESENT INDEXED-V2R draw 1, cf2:kofi:project:cocoa_farm_replanting_schedule|PRESENT INDEXED-V2R draw 4 — one cell collapses on 3 draws, at MIN_DRAWS); served `claude-opus-5` on every row; temperature unset, `max_tokens` 1024, k = 5. Opus 5 carries the conditional branches of P2 and P5 only (§7); its other rows are descriptive.

| Key | Value |
|---|---|
| **AUX-CF2-OP5-V2** | **0.8405** (blind 0.5000 by identity; Δ +0.3405); item [+0.2882, +0.3913]*, persona-clustered [+0.2996, +0.3817]* — agree; indexed persona-clustered [+0.7996, +0.8817]; k = 5 collapsed by the X4 mean, 1000 draws, seed 42 |
| **AUX-CF2-OP5-V3** | **0.9079** (blind 0.5000 by identity; Δ +0.4079); item [+0.3508, +0.4628]*, persona-clustered [+0.3769, +0.4377]* — agree; indexed persona-clustered [+0.8769, +0.9377]; k = 5 collapsed by the X4 mean, 1000 draws, seed 42 |
| **AUX-CF2-OP5-V2R** | **0.8353** (blind 0.5000 by identity; Δ +0.3353); item [+0.2825, +0.3870]*, persona-clustered [+0.2937, +0.3768]* — agree; indexed persona-clustered [+0.7937, +0.8768]; k = 5 collapsed by the X4 mean, 1000 draws, seed 42 |
| **AUX-CF2-PERSTATE** (Opus 5, descriptive) | v2: EXPIRY (n 90, pos 30) indexed **0.6150**, paired item [+0.0077, +0.2282]*, persona [+0.0443, +0.2008]*; RETRACTION (n 90, pos 30) indexed **0.5872**, paired item [-0.0331, +0.2026], persona [+0.0427, +0.1581]*; SUPERSESSION (n 264, pos 88) indexed **0.9325**, paired item [+0.3598, +0.5068]*, persona [+0.3949, +0.4688]*. v3: EXPIRY (n 90, pos 30) indexed **0.9267**, paired item [+0.2974, +0.5637]*, persona [+0.3576, +0.4787]*; RETRACTION (n 90, pos 30) indexed **0.8100**, paired item [+0.1550, +0.4597]*, persona [+0.2245, +0.3922]*; SUPERSESSION (n 264, pos 88) indexed **0.9319**, paired item [+0.3584, +0.5079]*, persona [+0.3939, +0.4687]*. v2r: EXPIRY (n 90, pos 30) indexed **0.6092**, paired item [+0.0008, +0.2140]*, persona [+0.0401, +0.1985]*; RETRACTION (n 90, pos 30) indexed **0.5681**, paired item [-0.0548, +0.1820], persona [+0.0264, +0.1306]*; SUPERSESSION (n 264, pos 88) indexed **0.9322**, paired item [+0.3603, +0.5044]*, persona [+0.3934, +0.4690]*. |
| **AUX-CF2-COUNTED** (Opus 5, descriptive — P3 is Haiku's) | Pooled counted states, 60 pairs / 180 items: v2 **0.6030** → v3 **0.8536**, paired Δ **+0.2506**, item [+0.1784, +0.3349]*, persona [+0.1941, +0.3019]*. |
| **AUX-CF2-NAMEDVSCOUNTED** (Opus 5; **P2's conditional branch**) | v2: named **0.9325** − counted **0.6030** = **+0.3295**, two-subset [+0.2420, +0.4181], persona-clustered [+0.2556, +0.3875] — both exclude zero, Δ clears tolerance: **P2 (Opus 5) HELD**. v3 (descriptive): 0.9319 − 0.8536 = +0.0783, [+0.0140, +0.1443], persona [+0.0147, +0.1385] — a residual boundary survives naming on this reader (Haiku's closed to +0.020). |
| **AUX-CF2-EQUIV-V2R** (Opus 5; **P5's conditional branch**) | V2R − v2 on the whole cell: Δ **-0.0052**, item [-0.0130, +0.0026], persona [-0.0122, +0.0020] — **both inside [−0.05, +0.05]**: **P5 (Opus 5) inside the band**; all three readers inside. |
| **AUX-CF2-FOK** (Opus 5, descriptive only) | v2 0.6922, v3 0.7098, v2r 0.6894. |
| **AUX-CF2-SPEND** (final) | **Opus 5 lane $63.3783** (Batch-priced from the returned tokens: 16,831,465 in / 1,703,969 out at $5 / $25 per M × 0.5) against the **$105** line — under; the probe projected $56.01 (output ran 1.70 M tokens against 1.02 M projected). **Anthropic total: Haiku $9.0623 + Opus $63.3783 + probes ≈ $0.06 = $72.50 of $130** (ceiling line $121). **OpenAI total: $1.0828 of $22** (mini lane $0.9568, probe, screens $0.0456, construction $0.0783). Every figure is metered from the rows at list / Batch prices; the vendors' billed totals are not exposed by the APIs. |
| **AUX-CF2-DROPRULE** (closed) | Evaluated once on 2026-09-13 (D-CF2-5): RUN; lane submitted on the author's GO and scored the same day; actual $63.38 against the $105 line. |

**Opus 5 conditional branches (§8 texts):**

- **P2 (Opus 5) — HELD.** Under the summary that names only superseded content, Opus 5's judgment on the named state exceeds its judgment on the two counted states by +0.330, interval [+0.2420, +0.4181] (persona-clustered [+0.2556, +0.3875]).
- **P5 — all three readers inside the band.** Randomizing the retracted and expired counts in the superseded-only summary moves gpt-4.1-mini's whole-cell judgment by +0.001 and Haiku 4.5's by +0.007, intervals [-0.0282, +0.0297] (persona-clustered [-0.0210, +0.0230]) and [-0.0079, +0.0229] (persona-clustered [-0.0103, +0.0248]), both inside the tolerance band; on this cell neither reader takes anything from the counts. Opus 5, run under the §11 rule: -0.005, intervals [-0.0130, +0.0026] (persona-clustered [-0.0122, +0.0020]), inside the band.
- **Descriptive (no prediction):** Opus 5 whole cell v2 0.841, v3 0.908, v2r 0.835; counted states 0.603 → 0.854 (+0.251).
- **Adverse branch (§8), Opus rows:** 7 flags — the all-states lookup (0.876) exceeds Opus 5's v2 (0.841) and v2r (0.835) rows on the whole cell and on the counted states; the whole-map lookup edges Opus's v2r retraction row (0.576 vs 0.568). No baseline exceeds Opus 5 under v3 on any row, and none exceeds it on supersession. All 47 flags across the three readers are in `cf_scores_cf2.json` `flags`; no row is dropped.

### 5k. Derived margins for the manuscript (R98, 13 Sep 2026; differences of ledgered values, `cf_scores_cf2.json`)

Whole-cell rows where a lookup exceeds a reader (§8 adverse branch), lookup AUROC minus reader AUROC under the reader's summary; the lookups are scored once each on their own summary (superseded-names on v2 `AUX-CF2-NB6-V2` 0.7663, all-states on v3 `AUX-CF2-ALLSTATES-V3` 0.8756, whole-map on v2 `AUX-CF2-NB5-V2` 0.5776):

| Lookup | Reader, summary | lookup − reader (whole cell) | beyond ±0.05 |
|---|---|---:|---|
| superseded-names (v2) | Haiku 4.5, v2 | **+0.0097** | no |
| superseded-names (v2) | Haiku 4.5, v2r | **+0.0025** | no |
| superseded-names (v2) | GPT-4.1 mini, v2 | **+0.0496** | no |
| superseded-names (v2) | GPT-4.1 mini, v2r | **+0.0484** | no |
| all-states (v3) | Haiku 4.5, v2 | **+0.1190** | yes |
| all-states (v3) | Haiku 4.5, v2r | **+0.1118** | yes |
| all-states (v3) | Opus 5, v2 | **+0.0351** | no |
| all-states (v3) | Opus 5, v2r | **+0.0403** | no |
| all-states (v3) | GPT-4.1 mini, v2 | **+0.1589** | yes |
| all-states (v3) | GPT-4.1 mini, v3 | **+0.0789** | yes |
| all-states (v3) | GPT-4.1 mini, v2r | **+0.1577** | yes |

Per-state rows where a lookup exceeds a reader: superseded-names (v2) over Haiku 4.5 v2 supersession **+0.0347**; superseded-names (v2) over Haiku 4.5 v3 supersession **+0.0371**; superseded-names (v2) over Haiku 4.5 v2r supersession **+0.0349**; superseded-names (v2) over GPT-4.1 mini v2 supersession **+0.0915**; superseded-names (v2) over GPT-4.1 mini v3 supersession **+0.0779**; superseded-names (v2) over GPT-4.1 mini v2r supersession **+0.0723**; superseded-names (v2) over GPT-4.1 mini v2r retraction **+0.0050**; all-states (v3) over Haiku 4.5 v2 supersession **+0.0119**; all-states (v3) over Haiku 4.5 v2 retraction **+0.2542**; all-states (v3) over Haiku 4.5 v2 expiry **+0.2917**; all-states (v3) over Haiku 4.5 v3 supersession **+0.0143**; all-states (v3) over Haiku 4.5 v3 expiry **+0.0442**; all-states (v3) over Haiku 4.5 v2r supersession **+0.0121**; all-states (v3) over Haiku 4.5 v2r retraction **+0.2131**; all-states (v3) over Haiku 4.5 v2r expiry **+0.2864**; all-states (v3) over Opus 5 v2 retraction **+0.2103**; all-states (v3) over Opus 5 v2 expiry **+0.2561**; all-states (v3) over Opus 5 v2r retraction **+0.2294**; all-states (v3) over Opus 5 v2r expiry **+0.2619**; all-states (v3) over GPT-4.1 mini v2 supersession **+0.0687**; all-states (v3) over GPT-4.1 mini v2 retraction **+0.2692**; all-states (v3) over GPT-4.1 mini v2 expiry **+0.3222**; all-states (v3) over GPT-4.1 mini v3 supersession **+0.0551**; all-states (v3) over GPT-4.1 mini v3 expiry **+0.2842**; all-states (v3) over GPT-4.1 mini v2r supersession **+0.0495**; all-states (v3) over GPT-4.1 mini v2r retraction **+0.3025**; all-states (v3) over GPT-4.1 mini v2r expiry **+0.3567**; whole-map (v2) over Haiku 4.5 v2 retraction **+0.0325**; whole-map (v2) over Haiku 4.5 v2 expiry **+0.0125**; whole-map (v2) over Haiku 4.5 v2r expiry **+0.0072**; whole-map (v2) over Opus 5 v2r retraction **+0.0077**; whole-map (v2) over GPT-4.1 mini v2 retraction **+0.0475**; whole-map (v2) over GPT-4.1 mini v2 expiry **+0.0430**; whole-map (v2) over GPT-4.1 mini v3 expiry **+0.0050**; whole-map (v2) over GPT-4.1 mini v2r retraction **+0.0808**; whole-map (v2) over GPT-4.1 mini v2r expiry **+0.0775**.

Other derived figures printed: P4 margins **+0.0496** (superseded-names 0.7663 − GPT-4.1 mini v2 0.7167) and **−0.0017** (all-states 0.8756 − Haiku 4.5 v3 0.8773), both within ±0.05; counted-state pooled items **180** (60 pairs × 3), named-state items **264** (88 × 3); preregistered predictions across the registration record **47** (the manuscript's 42 + CF-2's 5), of which **8** did not hold (unchanged: CF-1's aggregate replication remains a failed registered prediction in its own row); questions asked of each summary **148**; PN read passes on the final draw's supersession records **87 of 88** authored first-read YES plus 1 D-CF2-3 YES — all 148 records in the cell passed the author's read (a construction fact, not a result).

Named-minus-counted, persona-clustered two-subset intervals not yet printed above (from `cf_scores_cf2.json` `two_subset_ci_persona`): GPT-4.1 mini v2 **[+0.2099, +0.3838]** (item-level two-subset [+0.1875, +0.3905], difference +0.2948, named 0.8308, counted 0.5360); GPT-4.1 mini v3 +0.1230, [+0.0204, +0.2210], persona [+0.0132, +0.2323]; Opus 5 v2r counted 0.5865, difference +0.3457, [+0.2528, +0.4411], persona [+0.2737, +0.4001]; GPT-4.1 mini v2r counted 0.5025, difference +0.3475, [+0.2496, +0.4425], persona [+0.2741, +0.4152]; Haiku 4.5 v2r counted 0.5847, difference +0.3026, [+0.2055, +0.3910], persona [+0.2453, +0.3669]. Whole-cell gains (AUROC − 0.5000) print at four decimals as the ledger's Δ values above (e.g. GPT-4.1 mini v2 +0.2167, Haiku 4.5 v3 +0.3773, Opus 5 v3 +0.4079).

Printed forms of the frozen §8 texts as they land in the manuscript (R98; placeholders filled at four decimals; the model identifier in the manuscript's name form), each on one line:

- P1 HOLDS [MAIN]: On $148$ questions written before any version of the store existed, and asked of three versions of the same store that differ in one attribute each, the smallest model's obligation judgment reaches $0.7167$ against the $0.5$ a question-only reader attains here, with an interval of $[+0.1494,+0.2846]$. The gain survives where the question cannot carry the label.
- P3 HOLDS [MAIN]: Naming retracted and expired content lifts Haiku 4.5's judgment on those states from $0.5638$ to $0.8649$ on the store-counterfactual set ($60$ questions), a paired gain of $+0.3010$ with interval $[+0.2268,+0.3721]$.
