# DEVIATIONS_CF2 — deviations from ADDENDUM_CF2.md (frozen f016f03)

Own numbering from D-CF2-1. Entries follow the R82 form: what happened, what changed, why it
is admissible, disposition. CF-2 writes into no other deviation file.

---

## D-CF2-1 — the retraction eligibility rate on the CF-2 walk is 0.095, not the 0.177 the registration assumed; the retraction quota falls from 60 to 30 before any acceptance

**What happened.** ADDENDUM_CF2 §3.2 estimated the retraction reads at "≈ 339 at 0.177", CF-1's
measured eligibility rate on its 62-candidate walk. The CF-2 walk (`reviews/CF2_ADJUDICATION_READ.md`,
seed-42 round-robin) returned, over 440 rows walked, **35 ELIGIBLE verdicts in 369 verdict
reads (439 including rank-skips), a rate of 0.0949**; 35 are usable under the
one-pair-per-(persona, scrubbed name) rule together with the one CF-1 verdict reused. The
figures relayed while the read was in progress (30 over 323, 0.093; then 35 over about 367,
0.095) are superseded by the count from the deposited `cf2/adjudication_cf2.json`. Filling 60
would have needed roughly 330 further human reads at that rate. The rate is a fact about the
corpus under the CF-2 admission predicate — a wider, individuating pool than CF-1 walked — and
is recorded as `AUX-CF2-ADJUDICATION-RETRACTION`.

**What changed.** By amendment dated 2026-09-12, entered **before any acceptance, store version,
index, label or score exists** (ADDENDUM_CF2 §14): the retraction quota is **30**, the
composition **100 supersession / 30 retraction / 30 expiry**, **160 pairs, n = 480**. Nothing
else in the registration moves: the predicates, the renderer, the arms, the readers, the
estimators, the five predictions and their frozen texts stand. Consequences carried by the
amendment: P1's whole cell is 480 items, above the 450 at which the Phase 3 grid first clears
0.80 on the smallest reader; the script re-run at 100/30/30 gives P1 0.997, P2 (Haiku 4.5)
1.000, P3 (Haiku 4.5) 1.000, ledgered under `AUX-CF2-POWER`; P3's pooled counted states hold 30 retraction and 30 expiry positives (60
pairs); the retraction per-state rows were descriptive already; the §10 lines shrink to mini $2,
Haiku 4.5 $13, Opus 5 $89 — Anthropic $102 of $130 (expected $77.72, ×1.3 $101.03); the R7 drop
rule stands.

**Why this is admissible.** The change is made on a measured rate before any pair is accepted
and before any store version exists, in the direction of fewer items, and it touches no
prediction's statement. The registration's §13 admits "a dated amendment appended in the R82
form, entered before the numbers it touches exist", and §3 already recorded one composition
ruling on the same grounds (100/100/30 → 100/60/30). The alternative — 330 further reads to hold
a quota chosen on an assumed rate — would have spent the author's time on a per-state row the
registration itself marks descriptive.

**Disposition.** `select_pairs.py --cf2` carries `CF2_QUOTA["RETRACTION"] = 30`; `verify_cf2.py`
asserts the 480-item cell and the 100/30/30 composition; the queue and reading document are
re-emitted with the new estimate (the walk order is unchanged). The per-candidate verdicts
are the author's and are deposited in `cf2/adjudication_cf2.json` (expiry complete, retraction
complete under the amended quota, supersession not started) before any question is drafted
(ADDENDUM_CF2 §3.1); every row was checked against the queue's persona and entry id.

---

## D-CF2-2 — a pair whose original record cannot satisfy the authoring predicate after the frozen retry is replaced by the next eligible candidate in walk order

**What happened.** CF2-BUILD-2 Step 2 (`author_pn.py` through `cf2_author_pn.py`, seed 42, one
retry) stopped on its own predicate at the 21st of 130 authored pairs:

```
STOP: cf2:zara:project:AA_application fails its write-path predicates twice
old:   User is preparing a portfolio for an application to the AA SED program.
new:   User has decided to cancel the submission process for the AA SED program application.
report: n_discr_old = 2, n_discr_new = 4   (MIN_DISCR = 3 on each side)
fails: keep at least 3 distinctive words from the existing record OUT of your sentence (only 2 were left out)
```

The record is short enough that any cancellation which names the plan — "AA SED program
application" — re-uses most of its distinctive words, leaving two on the old side against the
required three. The failure is about the record's length, not about the eligibility criterion:
the author's ELIGIBLE verdict on the candidate stands.

**What changed (ruling of 2026-09-12).** A pair whose original record cannot satisfy
`author_pn.py`'s write-path predicates after the frozen retry is **replaced, before any store
version exists, by the next ELIGIBLE candidate of the same state in walk order under the cap and
the one-per-name rule across states**. The rule applies to any further failure in this run; if a
state's spare list is exhausted, that state's quota drops by one under a further deviation. The
excluded pair keeps its ELIGIBLE verdict and is marked "excluded: authoring predicate" with the
failing report quoted, in `cf2/cf_pairs_cf2.json` (`meta.excluded`). The replacement's question
is drafted under Step 1's frozen renderer and appended to `cf2/cf_questions_cf2.json` with its
own gate trail; the questions sha256 is recomputed over the 160. `verify_cf2.py` check I accepts
excluded-and-replaced pairs; `AUX-CF2-OVERLAP` is updated if a replacement carries a tag. Step 2
re-runs in full at seed 42.

**Why this is admissible.** No store version, index, label or score exists; the replacement
follows the registered walk order under the registered constraints; the composition is
unchanged; the eligibility verdict is not re-adjudicated; the failing report is quoted so the
exclusion is auditable. CF-1 recorded zero retries and so left no precedent; this entry is the
precedent.

**Disposition.** Replacements made under this rule are listed here as they occur and in
`NUMBERS_CF2.md` `AUX-CF2-CONSTRUCTION`:

- 12 Sep 2026: `cf2:zara:project:AA_application` (RETRACTION, position 225) excluded; replaced by `cf2:pan:family_member:beam_role_in_business` (position 414, zero-overlap, not O3); the replacement's question drafted under the frozen renderer (first pick, index 1); Step 2 re-run in full at seed 42 completed with one frozen retry and no further failure.

- 13 Sep 2026 (ruling): the 31 records that fail the D-CF2-3 re-read fall here — **excluded: PN read**, verdicts standing, the failing read quoted in `cf2/cf_pairs_cf2.json` `meta.excluded`; replaced in walk order under the cap and the one-per-name rule across states (`select_pairs.py --cf2 --exclude-batch`). Retraction: `cf2:alex:project_release_strategy` (position 158) → `cf2:nadia:project_pitch:spring_menu` (position 419). Supersession: 30 excluded, **6 replaced** — the six ELIGIBLE spares at positions 154, 157, 161, 162, 164, 165 (callum `communication_style`, jake `habit:juul_use_intensity`, david `reading_preferences_narrative_nonfiction`, aroha `personal_time_value`, tom `vehicle_use`, mirri `learning_source:aunties_and_elders`) — leaving **24 pending**. Instead of the quota dropping by the shortfall (the fallback this entry and §15 name), the author ruled that the supersession queue is **extended from position 166 in walk order** by a further adjudication read: `reviews/CF2_ADJUDICATION_READ_EXT.md` prints about 55 candidates (the shortfall 24 at the observed eligibility 0.667 and authoring pass 0.75, with margin) in the original read file's format, criteria at the top; replacements are accepted from the author's verdicts in walk order, then drafted, authored and read like the others. `meta.pending_replacements` and `meta.pending_draft` record the state; `verify_cf2.py` check I asserts accepted + pending = quota in every state, and J/K accept only D-CF2-2 replacements as awaiting drafting. No store version until the 24 are filled and read.

- 13 Sep 2026: the 7 replacements drafted (frozen renderer, first pick, 0 substitutions, $0.0014) and authored (`author_pn.py` unchanged, seed 42, 0 retries, $0.0012); their read is `reviews/CF2_PN_READ_EXT.md`. The supersession queue extended from position 166 to 228: 55 readable candidates in `reviews/CF2_ADJUDICATION_READ_EXT.md`, 8 skipped (cap or name), sized at the observed eligibility 0.667 and the author's pass 0.75 (expected reads 48.0). Waiting on the author's verdicts.

- 13 Sep 2026 (extension read merged; `AUX-CF2-ADJUDICATION` §2h): positions 166–228 gave 27 ELIGIBLE / 27 INELIGIBLE / 1 rank-skip (the author's note says 26/28; the per-row file governs). Three replacement records whose NO stood by identity (aroha `personal_time_value`, callum `communication_style`, mirri `learning_source:aunties_and_elders`) excluded here, pending 27; the walk resumed at 166 accepted **26 replacements (positions 166–226)**, passing over 0215 elena at the cap; **pending 1**. The chain rule: a replacement that is itself excluded stays in `meta.excluded` with `replaces` and `replaced_by`, and `verify_cf2.py` check I follows the chain one step at a time.

- 13 Sep 2026: the 26 replacements drafted (frozen renderer, all first pick, $0.0050) and authored (`author_pn.py` unchanged, seed 42, 0 retries, $0.0043); the supersession queue extended a second time, positions 229–272 (30 readable, 14 skipped — the cap binds on 12 personas), sized on pending 1 + expected read failures 7.0 of the 28 records awaiting the read. Read file `reviews/CF2_PN_READ_EXT2.md` (Parts A–C). Waiting on the author.

- 13 Sep 2026 (third read merged; `AUX-CF2-ADJUDICATION` §2k): positions 229–272 gave 13 ELIGIBLE / 17 INELIGIBLE. Ten pairs excluded here — 8 whose NO stood by identity and the 2 failed re-reads — pending 11; the walk resumed at 229 accepted **11 replacements (positions 230–263)**: aisha:skill_development:soft_skills (230), omar:clothing_habit (232), bruna:marital_status (233), chenoa:health_belief:traditional healing (240), david:reading_volume (241), aroha:health_metric:fasting_blood_sugar (242), diane:favorite_scents_combination (243), mirri:health_condition:back_discomfort (245), pan:business_preference (252), leila:work_style_preference (261), valentina:job_attitude (263). **Supersession back at 100; pending 0.** Two ELIGIBLE rows lie beyond the fill point: 0264 patrick `communication_preference:trauma` (admissible) and 0272 omar `income_pattern` (omar at the cap). This is the last D-CF2-2 walk: **D-CF2-4** closes the replacement rule.

---

## D-CF2-3 — a PN record the author reads as a paraphrase or as implausible is re-authored once at seed 4242 and re-read; a second failure falls to D-CF2-2

**What happened.** The author's three-way read of the 130 authored records
(`reviews/CF2_PN_READ.md`; `AUX-CF2-PNREAD`) returned supersession 69 YES / 21 NO-paraphrase /
10 NO-implausible and retraction 29 YES / 1 NO-implausible: **32 records fail the read**. All 130
had passed `author_pn.py`'s lexical predicates; the predicates do not see whether a successor
restates the fact (a paraphrase leaves the PN label semantically hollow under Definition 1) or
contradicts the persona.

**What changed (ruling of 2026-09-12).** A record judged NO is **re-authored once with
`author_pn.py` unchanged (prompt sha `b6f53b1a…`) at seed 4242** — the same convention as the
question redraft — and **re-read by the author under the same three-way question**
(`reviews/CF2_PN_REREAD.md`). A record that fails the second read is handled by **D-CF2-2**: the
pair is replaced by the next ELIGIBLE candidate of its state in walk order under the cap and the
one-per-name rule, its question drafted, its record authored and read. When a state's spares are
exhausted, that state's quota drops by the shortfall under a further deviation. The registration
text is the amendment at `ADDENDUM_CF2.md` §15.

**Why this is admissible.** No store version, index, label or score exists; the authoring tool,
prompt, thresholds and retry are unchanged; the alternate seed is the one the registration
already uses for the question redraft; the read is a human check on the truth of the PN label,
which the value-scrubbed monitor input never sees, so it cannot tune the measurement. The
failure pattern is ledgered as observed: **paraphrases concentrate on attitude, feeling and
philosophy slots; implausible successors on identity-adjacent slots** (career, family history,
trauma).

**Disposition.** `cf2/cf_pn_texts_cf2_reauthor_4242.json` holds the 32 re-authored records
beside the first attempts; the re-read verdicts go to `cf2/pn_reread_verdicts.json`; a record
that passes the re-read replaces its first attempt in `cf2/cf_pn_texts_cf2.json` with
`reauthored_under: D-CF2-3`; a record that fails goes to D-CF2-2. No store version until the
re-read closes.

- 12 Sep 2026: the 32 re-authored at seed 4242 (retries 0, $0.0055); `author_pn.prompt_sha256()` binds the seed, so the file records `3b5c9c236b6783e2…` for the unchanged prompt at 4242; **15 of 32 came back identical to the first attempt** (9 paraphrase + 5 implausible supersession, 1 retraction) and fall to D-CF2-2 unless the re-read differs. Re-read pending: `reviews/CF2_PN_REREAD.md`.

- 13 Sep 2026: re-read closed (`AUX-CF2-PNREREAD`): 1 YES (omar `budget_allocation`, applied — `reauthored_under: D-CF2-3`), 31 fail (16 re-read, 15 by identity) → D-CF2-2. Instrument note: the alternate seed changed 17 of 32 outputs at temperature 0 and fixed 1; the frozen retry is nearly a no-op for this tool.

- 13 Sep 2026 (second round, ruling): the 5 NO replacement records (131, 132, 133, 135, 136 of `reviews/CF2_PN_READ_EXT.md`) re-authored once at seed 4242; **a byte-identical re-author lets the NO stand by identity without a re-read** and the pair falls to D-CF2-2 (3: aroha, callum, mirri); **a changed re-author joins the next read file** (2: david `reading_preferences_narrative_nonfiction`, tom `vehicle_use` → `reviews/CF2_PN_READ_EXT2.md` Part A). The author's disclosure is ledgered: the paraphrase/implausible letters on 131–137 were assigned by a language model from the author's bare NO.

- 13 Sep 2026 (third round): the 13 first-read NOs of `reviews/CF2_PN_READ_EXT2.md` (140–143, 146–148, 150, 151, 153, 156, 160, 162) re-authored once at seed 4242 (retries 0, $0.0021): **8 byte-identical** → NO stands by identity → D-CF2-2 (callum `privacy_preference:health_condition`, dmitri `client_facing_name_usage`, kofi `health_condition:tiredness`, lily `health_management:eczema_cotton_gloves`, mehmet `barbering_method_preference`, mehmet `shop_equipment_preference`, tom `preference:routine`, valentina `therapy_method`); **5 changed** → one last read in `reviews/CF2_PN_READ_EXT3.md` (chenoa `perspective:chronic_condition_management`, elena `work_stress_carryover`, jerome `health_condition:trauma_flashbacks`, omar `value_system`, priya `cognitive_style`). The two re-reads of that file (35 david `reading_preferences_narrative_nonfiction`, 37 tom `vehicle_use`) failed and fall to D-CF2-2 directly — the frozen retry is one. Identity across the run: 26 of 50 re-authors returned the first attempt byte-for-byte; a last read that fails now falls to **D-CF2-4**, not to a further replacement.

---

## D-CF2-4 — the supersession queue is not extended again; the quota is fixed at what the last walk reached and drops by one for every record that fails its read from here on, with no replacement

**What happened.** Three reads and two queue extensions (positions 166–228, 229–272) have not
closed the supersession draw. Of 100 first-drawn supersession records, 30 failed the author's
read; of 33 replacements read so far, 18 failed (7 → 5 of 7; 26 → 13 of 26); the seed-4242
retry restored 1 record in 50 and returned the first attempt byte-for-byte 26 times. The
failures concentrate on attitude, feeling and philosophy slots (paraphrase) and on
identity-adjacent slots (implausible successor), as `AUX-CF2-PNREAD` records. Meanwhile the
queue is thinning: eligibility on the walk fell from 0.667 (positions 1–165) to 0.500
(166–228) to 0.433 (229–272), and **the persona cap of 4 binds on 12 of 40 personas**, so 14 of the
44 positions in the second extension were unreadable. At the third read the author counted 16
replacements needed against 13 ELIGIBLE in reserve.

**What changed (the author's ruling, 13 Sep 2026; ADDENDUM_CF2 §16).** After the D-CF2-3 retry
and the D-CF2-2 walk over positions 229–272, **no further extension of the supersession queue is
made.** The quota is fixed at what that walk reached — **100**, because 5 of the 15 NOs changed at
re-author and await a last read, so only 11 replacements were needed and the 13 ELIGIBLE covered
them under the cap and the name rule — and from here on **a record that fails its read
(a new replacement's first read, or a changed re-author's last read) is excluded under this
deviation with no replacement; the supersession quota drops by one for each, and the
composition is (N_sup) / 30 / 30**. The 16 records awaiting a read at the time of this ruling
are the 11 new replacements and the 5 changed re-authors of `reviews/CF2_PN_READ_EXT3.md`.

**Why this is admissible.** No store version, index, label or score exists. The drop is in
the direction of fewer items, touches no prediction's statement, and stops a replacement
process whose marginal yield is falling (eligibility 0.433, read pass 0.50 on the last
batch) while its cost — the author's reads — is not. §13 admits a dated amendment entered
before the numbers it touches exist; §14 and §15 record the same kind of ruling.
**Consequence for power, flagged:** the §14 power figures (P1 0.997, P2 1.000, P3 1.000) were
simulated at 100/30/30, n = 480. The Phase 3 grid first cleared 0.80 on the smallest reader at
n = 450, i.e. 150 pairs, i.e. N_sup ≥ 90; if more than 10 of the 16 records awaiting a read fail,
n falls below 450 and the power claim must be re-run at the final composition before any store
version is built. The author's note ("n remains above 470") assumed a shortfall of 3; the
actual range is 432–480.

**Disposition.** `cf_pairs_cf2.json` `meta.quota` carries the effective quota (`--record-d4`),
`meta.quota_history` every change; `--exclude-d4 <spec>` excludes without refill and decrements
the quota; `verify_cf2.py` check I asserts effective quota = recorded quota − D-CF2-4
exclusions, `no_further_extension`, and no `replaced_by` on a D-CF2-4 exclusion; check D
counts items as 3 × the accepted pairs. Exclusions under this rule are listed here as they occur.

- 13 Sep 2026: recorded with quota 100/30/30, residual shortfall 0; 16 records awaiting a read.
- 13 Sep 2026: the 11 replacements of the last walk drafted (all first pick, $0.0021) and authored (0 retries, $0.0018); `reviews/CF2_PN_READ_EXT3.md` carries them and the 5 changed re-authors for the last read. Waiting on the author; the first NO in that file is the first exclusion under this rule.
- 13 Sep 2026 (final read merged, `AUX-CF2-PNREAD` §2n): **12 of the 16 failed** (7 first reads, 5 last re-reads) → excluded here with no replacement (`--exclude-d4`); **quota 88 / 30 / 30, n = 444**. The conditional power re-run fired (12 > 10): at 89/30/30 P1 0.994, P2 1.000, P3 1.000 (§3a). The author's ruling "patrick 0264 is the one spare" was made on a report of one admissible spare; the exclusions freed 0215 elena (which precedes 0264 in walk order) and 0272 omar. **Held for the author's ruling** — walk order gives 0215 elena; the ruling names patrick; all three give N_sup = 91 — nothing drafted meanwhile.
- 13 Sep 2026 (ruling): **no spare.** D-CF2-4 as written: **88 / 30 / 30, 148 pairs, n = 444**; 0215 elena, 0264 patrick, 0272 omar stay undrawn and are listed (`NUMBERS_CF2.md` §2p). The 89/30/30 power run covers the cell within three items; no re-run. §16 carries the applied line. The draw is closed; the build proceeds.

---

## D-CF2-5 — the §11 drop rule is evaluated on 2026-09-13, not on 2026-09-19

**What happened.** §11 fixes the evaluation of the Opus 5 drop rule to a date, 2026-09-19, chosen at
freeze so that the mini and Haiku 4.5 lanes would be scored and ledgered first. Both lanes were
scored and ledgered on 2026-09-13 (`AUX-CF2-MINI-*`, `AUX-CF2-H45-*`, `AUX-CF2-SPEND`); the
precondition the date stood for is met six days early.

**What changed (the author's ruling, 13 Sep 2026).** The three checks of §11 are evaluated on
2026-09-13, once, and ledgered under `AUX-CF2-DROPRULE` before any Opus 5 batch is created. Nothing
in the checks themselves moves: (i) metered spend after the two lanes against their combined lines;
(ii) a three-call Opus 5 probe projecting the lane against its own line; (iii) a registered
prediction naming Opus 5. The once-only property is kept — the row is not re-evaluated on the 19th.

**Why this is admissible.** The date was a proxy for an ordering (Opus last, after the other lanes
are scored), and the ordering is honoured; the evaluation is written before the Opus batch exists;
no score of the Opus lane exists; nothing about the predictions or estimators moves.

**Disposition.** `cf2/results/droprule_cf2.json`; `NUMBERS_CF2.md` §5h. Result: (i) $10.02 of $18 — pass;
(ii) $56.01 (×1.3 $72.81) of $105 — pass; (iii) P2 and P5 name Opus 5 — pass. **The lane runs at
k = 5; the batch is not created until the author's GO.**

- 13 Sep 2026: GO given; batch `msgbatch_014ADrDKGmyQuxCdzzrJjg6c` submitted and collected the same day (7,400 / 7,400; 2 parse failures in one cell, which collapses on 3 draws); actual $63.38 against the $105 line (probe projected $56.01; output tokens ran 1.70 M against 1.02 M projected). P2 (Opus) HELD, P5 (Opus) inside the band (`NUMBERS_CF2.md` §5j).
