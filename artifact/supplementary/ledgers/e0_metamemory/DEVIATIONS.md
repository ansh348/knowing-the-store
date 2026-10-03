# DEVIATIONS — E0 metamemory feasibility probe

Every departure from the E0 prompt, in the order encountered. Entries marked **STOP** were
load-bearing for a pre-registered gate and were escalated rather than resolved unilaterally,
per Hard Rule 5.

---

### D1 — Step 0 ordering: feasibility measurement ran before pre-registration
**Prompt:** "No API call that produces a scoreable observation may run before the prereg file
is committed."
**What happened:** `tools/feasibility.py` and `tools/yaml_join.py` were written and run before
any prereg existed.
**Why this is not a violation:** both are read-only over committed artifacts and make **zero
API calls**. They produce no scoreable observation — they measure whether the design the prereg
would commit to is constructible. Writing a prereg first would have committed item counts that
turn out to be unachievable.
**Status:** logged, no action needed.

---

### D2 — **STOP** — no per-question gold-edge annotation exists in LifecycleBench
**Prompt:** Hard Rule 6, "Every (query, store-variant) label must be computable by provenance
join against YAML ground truth."
**What is actually true:** the YAML carries supersession chains, expiry dates and retraction
events as claimed, but nothing links a YAML fact to the bank entry ids expressing it. The banks
were built by an LLM extractor that never saw the YAML. The project documents this itself
(`pkwc_q2_common.py:26-30`; `MEMAUDIT_EVIDENCE_REPORT.md:252-255`).
**Conservative reading available?** No. The choice of gold-edge resolver changes what the
primary gate metric (FOK AUROC on ABSENT) measures, and changes the UNRESOLVED count from 3.5%
to 57%. There is no defensible default.
**Status:** STOPPED. See `FINDINGS_E0_STEP0.md` §1, §3, §6.

---

### D3 — **STOP** — the ≥60-per-cell floor is unachievable at 10 personas
**Prompt:** "Select 10 personas … no cell below 60 items."
**Measured:** min cell = 45 (YAML-native), 53 (LEX), 49 (JUDGE), 50 (UNION). `ABSENT` binds in
all four. Relaxing the ablation to 5 categories does not fix it (45 → 44); the binding
parameter is persona count, not ablation size. 20 personas clears every cell (min 85) with
composition 37/31/32 against the 40/35/25 target and n=270 against the ~300 target, at ≈$0.52.
**Status:** STOPPED — this is the prompt's own stop condition, stated verbatim.

---

### D4 — **STOP** — "≥8 questions per persona fully inside the ablated categories" is unachievable
**Prompt:** Step 1, "Choose ablation categories per persona such that at least 8 existing
LifecycleBench questions for that persona have ALL of their gold supporting edges inside the
ablated categories."
**Measured:** with 2–3 ablated categories, **zero** of the 40 personas reach 8 under the
YAML-native, LEX, JUDGE or UNION gold rules. Best single persona reaches 7 (LEX) / 6 (UNION).
Under the coarser `relevant_categories` proxy exactly one persona (dariush) reaches 8. Reaching
8 for ten personas requires ablating 4–5 categories, which the prompt excludes.
**Status:** STOPPED alongside D3 — it is the same binding constraint seen per-persona.

---

### D5 — `is_active == False` rejected as the superseded-content signal
**Prompt:** PRESENT-NEGATIVE is content that is "superseded, retracted, or expired … per YAML
supersession chains, retraction events, expiry dates."
**Why deviated:** of the 121 YAML supersession events, 109 have a well-defined old/new token
discriminator, and for **78/109 (72%)** the bank still holds an `is_active == True` entry
asserting the superseded old value (43/109 at coverage ≥0.75; 11/109 at coverage 1.00). The
ingest pipeline did not supersede in a large fraction of YAML-declared cases. Using `is_active`
would have missed most negative obligations *and* would have measured the pipeline's behaviour
rather than the YAML ground truth.
**Resolution taken:** negative obligation is detected by discriminative-token matching against
the YAML **old** value across the whole persona bank, independent of `is_active`.
**Caveat, not resolved:** at τ=0.50 this detector has false positives (e.g. `amara` lb_00218
matches `old_fact: "Practises at 4 Brick Court Chambers"` on the token *chambers* alone). So
72% is an upper bound and the PRESENT-NEGATIVE cell is the least trustworthy of the three. τ is
therefore a fourth pre-registration decision, trading cell size against precision, and the
Step 1 hand-audit of PRESENT-NEGATIVE items should gate the run rather than merely appear in
the appendix.
**Status:** resolved conservatively; residual precision risk escalated. See
`FINDINGS_E0_STEP0.md` §4 and §5 hazard 11.

---

### D6 — expiry reference date chosen as `t_now(FULL) − 14 days`, pinned per persona
**Prompt:** does not specify a reference date.
**Choice:** `expired ⟺ event_time < (max(created_at over ACTIVE entries of the FULL bank) + 24h)
− 14 days`, i.e. the operational cutoff the system itself applies
(`lifecycle_bank.py:1055`, `evaluate_lifecycle_bank.py:168-174`), computed from the **FULL**
bank and reused unchanged for the ABLATED variant.
**Why:** `t_now` is derived from bank contents, so computing it per-variant would let the
ablation silently move the expiry cutoff. Measured spread across personas 2026-02-07 to
2026-05-29 — it is not a global constant. Today's date (2026-08-10) was rejected: it marks
essentially everything expired. YAML `status:` was rejected as primary because it is relative
to an unstated authoring date; measured agreement with the derived rule is 117/126 (92.9%).
**Status:** resolved conservatively, logged. The 9 disagreements would go to UNRESOLVED rather
than being adjudicated.

---

### D7 — 26/40 persona YAMLs do not parse; repaired rather than skipped
**What happened:** `yaml.safe_load` raises on 26 of 40 persona files (unquoted parentheticals
after `wrong_if_surfaced`). The existing repo helper
(`analysis/ontology_validation/common.py:165-181`) dodges this by truncating each file at
`draft_questions:`, which silently discards them.
**Resolution taken:** reused `convert_draft_questions.py:168-182 fix_yaml_content()`, which
rescues 40/40. No YAML file was modified on disk.
**Status:** resolved, logged.

---

### D8 — AV5 and AV8 questions are structurally unresolvable
**Measured:** `AV5_broad_query` (40 questions) and `AV8_numeric_preservation` (63) have no
source YAML section — AV5 by design ("system must synthesize"), AV8 because all 16 of the
q13/q14 extras were hand-appended with no YAML counterpart and the rest draw numbers from
across sections. Their lexical argmax scatters across every section.
**Resolution taken:** both are assigned UNRESOLVED by construction rather than being forced to
a section. 103 of the 294 YAML-native UNRESOLVED items are these.
**Status:** resolved conservatively, logged.

---

### D9 — two AV3-labelled questions test expiring_logistics, not stable_identity
`omar_q12` ("What's Omar's career plan?") and `patrick_q13` ("How long has Patrick been on the
job?") are labelled `AV3_stable_identity` but their gold answers are dated logistics facts.
This is pre-existing label noise in the question set (~2% of AV3), not introduced here. Any
per-attack-vector breakdown inherits it.
**Status:** logged, no action.

---

### D10 — TAU_HI grid extended after the first grid failed to reach the criterion
**What happened:** `calibrate_tau.py` was first written with the grid
`{0.00, 0.10, 0.20, 0.25, 0.34, 0.40, 0.50}`, chosen around where the TAU_LO plateau was
expected. The hand audit then showed the TAU_HI precision cliff lies **above** 0.50 — audited
precision is 0.647 at 0.50 and only reaches ≥95% at 0.80. Under the original grid the
pre-registered rule would have fallen through to its 1.00 fallback.
**Resolution taken:** the grid was replaced with a uniform `{0.00, 0.05, …, 1.00}` spanning the
whole signal range, used for **both** rules, before `thresholds.json` was written.
**Why this is disclosed rather than buried:** the grid was widened *after* seeing that the
original did not reach the criterion, which is exactly the shape of a post-hoc adjustment. Three
things constrain it: the **rule** ("smallest threshold with audited precision ≥95%") was fixed
before the audit was read and did not change; the widened grid is uniform and not gerrymandered
around the answer; and the full 30-row audit table is committed verbatim in
`tau_audit_sample.json`, so precision at any threshold can be recomputed without trusting this
choice. The alternative — accepting a 1.00 fallback caused by a badly chosen grid — would have
been a worse instrument selected for a worse reason.
**Status:** resolved, disclosed. Recorded in `PREREG_E0.md` §4.

---

### D11 — three distinct thresholds, not one
**Prompt / decision of record:** item 4 replaces "the single threshold" with an asymmetric pair.
**Ambiguity:** in the Step-0 code a single constant `TAU` governed two different things — Stage B
resolution of the **gold** set, and the **negative-obligation detector**. The decision of record
concerns the detector.
**Resolution taken (conservative):** the asymmetric pair applies to the detector only.
Gold resolution keeps its own named constant `TAU_GOLD = 0.50`, unchanged and separately
declared, so that the two roles cannot drift into each other unnoticed.
**Status:** resolved conservatively, logged. Declared in `PREREG_E0.md` §4.

---

### D12 — committed census is 89/69/69, not the 99/85/86 target
**Decision of record:** "Target the 99/85/86 census."
**Measured after setting the thresholds:** PRESENT 89, ABSENT 69, PRESENT-NEGATIVE 69,
UNRESOLVED 283, scoreable 227.
**Why:** 99/85/86 came from the Step-0 measurement at a single τ=0.50. The asymmetric pair sends
mid-strength detector fires to UNRESOLVED, costing ~16 items in each of ABSENT and
PRESENT-NEGATIVE. This is the intended effect of the decision, not a regression.
**Gate applied:** ABSENT = 69 ≥ 60, so the plan stays at 20 personas and the escalation to 30 is
not triggered. PRESENT-NEGATIVE = 69 also clears 60 although it was not required to.
**Status:** logged, no escalation.

---

### D13 — operational: a concurrent session's staged files entered commit `d51f12d`
**What happened:** `git add e0_metamemory/` staged only this probe's files, but a second session
working in the same clone had its own files staged, and `git commit` without a pathspec swept in
all of them. `d51f12d` therefore carries 23 unrelated SESSION 13 files under an E0 message.
**Resolution:** the other session verified nothing was lost and recorded it as Incident 7
(`eff4e6a`) rather than rewriting a commit a live session was building on. Not re-litigated here.
**Change adopted:** every subsequent commit from this probe uses an explicit pathspec
(`git commit -- e0_metamemory/`).
**Status:** logged; design-basis citation `FINDINGS_E0_STEP0.md @ d51f12d` remains correct, since
that is the commit that introduced the file.

---

## Not yet reached

Steps 2–6 (index M(S), leakage control, elicitation, scoring, amber path) not started. No index
built, **no API call made**.

---

### D14 — ABSENT verification statistic non-zero: 3/69, of which 2 are genuine label errors
**Prereg §7:** the independent lexical check on ABSENT items is "a finding to report, not a
relabelling trigger".
**Measured:** 3 of 69 ABSENT items contain a surviving entry that passes the lexical proxy.
Read individually: `david:david_q11` is a proxy false positive (shared phrase, no bearing);
`ingrid:ingrid_q02` and `pan:pan_q10` are genuine — content re-expressed in a later session under
a non-ablated category, which the session-anchored Stage B gold set does not see, so the ablation
did not remove it.
**Action taken:** none. Nothing was relabelled, per the pre-registered rule.
**Escalated because the bias is not neutral:** a mislabelled ABSENT is an item where the store
does hold relevant content, so a well-calibrated high FOK scores as an error and DEFLATES the
measured AUROC — pushing the blind arm toward satisfying H1. 2/69 = 2.9% contamination, biased in
the direction the hypothesis wants. Recorded in `STEP1_REPORT.md` §4.1 and to be repeated in
`RESULTS_E0.md`.
**Status:** logged; a decision for [AUTHOR-1] on whether 2.9% is acceptable or whether the prereg
should be amended to route lexically-flagged ABSENT items to UNRESOLVED.

---

### D15 — "ablation-manufactured ABSENT vs any other ABSENT" is a degenerate breakdown
**Prompt Step 5:** requires that breakdown.
**Measured:** all 69 ABSENT items are ABLATED-variant, so the "other ABSENT" stratum is empty.
**Resolution:** the breakdown will be reported as degenerate rather than silently omitted. A
related distinction that IS informative was found instead and will be reported in its place:
59 ABSENT items arise from gold being ablated away, and 10 from AV2 negative-answer questions
whose expired content was ablated away (`STEP1_REPORT.md` §4.2).
**Status:** logged.

---

### D16 — the pre-registered expiry rule was 20% precise; caught by Amendment 1 verification
**Prereg §3:** "Expiry is date-derived and exact, with no threshold."
**Measured under full per-item verification:** of 80 expiry-admitted (question, entry) pairs,
only **16 (20.0%)** establish a real negative obligation. The description was true about *dates*
and false about *negative obligation*. Two causes: (e) the YAML record's own `status` is
`upcoming` and the question's gold answer IS that event (38 pairs, 7 questions); (f) the question
explicitly asks the store to surface PAST events, so the expired content is the gold answer
(21 pairs, 3 questions).
**Why the 30-fire audit missed it:** that audit sampled only *detector fires* at ≥ τ_lo. Expiry
evidence carries no detector signal and was never in the sampling frame. The route was trusted
because it was called "exact".
**Relation to D6:** D6 recorded that the 9 YAML-status-vs-derived-cutoff disagreements "would go
to UNRESOLVED rather than being adjudicated". The pre-registration did not carry that provision
into its expiry rule. Cause (e) is exactly that gap.
**Resolution:** per-item verification routes all 71 failing pairs' items to UNRESOLVED where no
surviving admitting entry verifies; 17 of 69 PN items moved. The expiry sub-rule is now stated
explicitly in `tools/pn_verdicts.py` and `AMENDMENT_1.md`.
**Status:** resolved by Amendment 1. Belongs in the main deviations table of RESULTS.

---

### D17 — τ_hi demoted from label warrant to candidate filter
**Amendment 1, change 3.** Every admitted PRESENT-NEGATIVE item is now read individually, so the
label set no longer rests on the threshold. τ_hi = 0.80 bounds how much evidence had to be read.
Its measured precision on the full 166-pair set — 91.2% at signal 1.00, 93.1% in 0.80–0.99 —
validates the original 30-fire audit rather than warranting labels. The n=5 and one-item-cliff
caveats pre-registered in `PREREG_E0.md` §4 are superseded.
**Status:** resolved by Amendment 1.

---

### D18 — index tightened to Level 1 despite the leakage control passing at Level 0
**Prereg §9:** "if more than 3 of 30 are answered correctly, the index leaks answer content" —
which implies that at ≤3 the index is kept.
**Measured at Level 0:** **3/30 correct — a PASS by exactly one item.** That is the
pre-registered verdict and it is reported as such.
**Why the ladder was descended anyway:** the pre-registered scorer materially under-detects.
It requires the response to cover ≥50% of the gold answer's content tokens, which penalises
short correct answers. Direct inspection of the Level-0 indexes shows they literally contain
the gold answers as slot-key names:
`health_condition:atrial_fibrillation` + `medication:warfarin` (gold for `tom_q04`),
`health_condition:mild hearing loss` (`david_q05`), `certification_renewal:telehealth`
(`chenoa_q06`), `considering_move_to:Cicero` (`elena_q09`), `partner_hobby:Lucía`
(`valentina_q07`). A looser scorer — response recovers ≥1 distinctive (>4 char) gold token —
gives **9/30**. The model returned "Lucía" and "atrial fibrillation" from the index alone and
was scored incorrect only because it did not also recover the rest of the gold string.
**Action:** descended to **Level 1** of the pre-registered tightening ladder (strip everything
after the first `:`). Re-ran the control: **0/30, 29/30 UNKNOWN**. Level 1 is used for the main
run. Line count also moves from 42–74 (mean 57.8) to 34–57 (mean 44.5), closer to the
pre-registered ~40–60.
**Why this cannot bias toward the hypothesis:** a *less* informative index can only make H2
(indexed − blind ≥ +0.10) **harder** to satisfy, never easier. Tightening on a marginal pass is
conservative in exactly the direction that matters, and it removes a confound that would
otherwise let the index raise FOK by leaking answers rather than by conveying coverage metadata.
**Status:** deviation from the letter of §9, taken deliberately, with both control runs
committed (`leakage_control_L0.json`, `leakage_control_L1.json`). Belongs in the main deviations
table of RESULTS.

---

### D19 — the BLIND arm is not deterministic at temperature 0 with a fixed seed
**Prereg §10:** temperature 0, seed 42, one call per item per arm.
**Observed:** the BLIND prompt is byte-identical for the FULL and ABLATED variants of a
question — the blind arm cannot see the variant — so both calls should return the same FOK. On
**90 of 255 question pairs (35%)** they do not; mean |Δ| when discordant 0.134, max 0.30.
Within-question variance is **14.6% of total blind FOK variance**.
**Cause:** ordinary provider-side nondeterminism. The two calls differ only in `item_id`, which
enters the local cache key and nothing sent to the model. Not a harness defect.
**Why it matters:** every ABSENT item is an ABLATED variant, so this noise sits directly on the
axis the primary gate reads. It is noise, not bias — no preferred direction — but it inflates
the variance of blind FOK AUROC and will widen the paired bootstrap CI.
**Action:** no design change; the prereg specifies one call per item per arm and that was
followed. Reported beside the blind number in RESULTS rather than left to be discovered after.
**Status:** logged.

---

### D20 — responses are coarsely quantised, and NOK is near-degenerate in the blind arm
**Observed:** across 510 items per arm, BLIND FOK takes 6 distinct values and BLIND NOK 4, with
NOK = 0.00 on 316/510. INDEXED FOK takes 12.
**Consequence:** AUROC handles ties correctly, but a large share of pairs are ties, and ECE with
10 equal-width bins concentrates in two or three bins. This bears hardest on NOK, effectively a
three-value variable blind.
**Action:** none — the metric definitions are pre-registered and will not be changed after
seeing the data. NOK ECE/AUROC will be reported as descriptive of a near-degenerate response
distribution rather than as calibration measurements. NOK is exploratory and gates nothing.
**Status:** logged.
