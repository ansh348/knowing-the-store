# E1 DESIGN: FULL CALIBRATION STUDY ("Feeling of Knowing")

**v0.2, 10 Aug 2026. Supersedes v0.1. Commit as e1_metamemory/E1_DESIGN.md.**
Changelog from v0.1: folds in the Phase-0 census and the B2/B3/B4 resolutions (CC commits 0f48a69, 426efb4, 783b1bc); adds the PN membership criterion, the A-MEM lifecycle-ablation decomposition, and the believed-state deliverable; retires the five open decisions (all resolved).
Predecessor: E0 (GO at 77a4dfd; blind FOK 0.5087 / indexed 0.8176, dedup delta +0.2747 CI [+0.1712, +0.3787]; NOK null; $0.342).

## 1. What E1 must license

E0 proved the mechanism on easy terrain. E1 answers the three questions E0 could not: does the FOK effect survive honest ABSENT (terrain where the index cannot just read a zero); can NOK, the differentiating judgment, be made to work at all; and does the effect hold across backends and, critically, when the index is built from the store's own corrupted beliefs rather than from ground truth. E1's numbers are the flag-plant numbers. Every design choice optimizes for a result that survives a hostile reviewer, not for a large delta.

## 2. Lessons carried from E0, each with its number

L1 (20% expiry-route precision): negative obligation is query-intent-conditional. The taxonomy is built on (item, intent) pairs, never on items alone.
L2 (warfarin/Lucia in the Level-0 index): slot keys embed fact values in this corpus. The index renderer gets a value scrubber and the leakage ladder is a permanent fixture.
L3 (90/255 byte-identical blind pairs disagreeing, 14.6% of blind variance): the blind arm caches on prompt hash, one draw per unique prompt, with a k=3 multi-draw subsample to quantify residual noise.
L4 (indexed 0.8176 partly measuring "can the model read a zero"): ABSENT gets difficulty tiers; the headline gate reads the hard tier.
L5 (blind NOK 0.00 on 316/510, four distinct values): NOK elicitation is redesigned, with worked examples, decomposition, and an index that carries lifecycle signal.
L6 (E1 Phase 0, membership spot-check 69-86% across backends): there is no mechanical half of PN labeling. Membership is semantic and gets full human verification (section 3).

## 3. Label taxonomy v2 (intent-conditional) and PN verification

Every question receives an intent type before any label is assigned: CURRENT-STATE, UPCOMING, PAST-EVENT, or CHANGE-AWARE, typed under the committed rule table (Phase 0: 516/516 typed, 0 unresolved; 110/413 in-scope questions are structurally barred from PN by rule). Labels are functions of (store variant, question, intent):

- PRESENT: variant contains licensed content answering the question under its intent, no negative obligation load-bearing. On external backends, PRESENT additionally requires sweep-verified presence in the actual store (see section 4 on ingestion loss).
- PRESENT-NEGATIVE: variant contains content that, under this intent, must be suppressed (superseded value for CURRENT-STATE; retracted plan for CURRENT-STATE or UPCOMING; expired event for CURRENT-STATE or UPCOMING). Expired content under PAST-EVENT intent is PRESENT, not PN. YAML status fields override derived cutoffs.
- ABSENT: no licensed content and no obligation bears, under the tau_lo screen carried from E0.
- UNRESOLVED: everything the joins cannot settle. Standard.

PN verification uses the factorized design with full verification of both halves, registered from the outset (the E1 Phase-0 spot-check escalated all three backends at 85.7 / 76.9 / 69.2% membership precision, and the measured total burden of ~341 judgments sits well under the 500-pair stop threshold; the escalation rule is therefore retired and replaced by full coverage):

- Semantic half, once per (question, YAML-record) pair (~166): does this record constitute a negative obligation for this question under its intent. Backend-independent.
- Membership half, per (entry, record) pair at tau_hi (~175): does this entry assert the superseded value AS CURRENT. Exclusions, written here verbatim for the prereg: entries stating the decision-against ("considered X but decided against it") are NOT members; entries with explicit historical framing ("the previous focus was X", "used to") are NOT members; token collisions are NOT members. The first two exclusion classes are recorded as tagged subtype counts (decision-against; historically-framed) during the pass, since they are cheap to tag and scientifically interesting as weak-generator hazards.

All verification tables committed. Detector-proposes, YAML-disposes remains the house method.

## 4. Store variants, difficulty tiers, and backend scope

Backends: FR-Bank, Mem0, A-MEM. Mem0 excludes personas alex (5/35 sessions), thanh (8), aisha (18) for ingestion incompleteness; 37 personas and 9,736 of 10,074 entries retained; session coverage reported as a covariate. Gold content silently lost to ingestion on external backends labels as ABSENT-by-ingestion-loss, a named subtype in the ABSENT mechanism split, reported, never pooled into the hard tier.

Variants:

- FR-Bank: FULL, CAT-ABLATED (easy tier, E0 comparability), SLOT-ABLATED (hard tier; removes gold-supporting entries AND sibling slot-key copies; Phase-0 closure factor 2.59x gold, median 1.50x, max 20.3x), plus NATURAL-ABSENT probes.
- Mem0 and A-MEM: FULL plus NATURAL-ABSENT only. CAT-ABLATED is inexpressible on both (Mem0 has no category field; A-MEM's is a constant), and no classifier enters the label path under any circumstances. The inexpressibility is a reported finding: a category ablation is a regional probe and presupposes region structure the store can name; a store without region structure cannot be probed regionally. Session-ablation may exist as an unpooled exploratory cell only.
- NATURAL-ABSENT probes: 7 drafted per persona (Phase-0 survival 5/6), machine pre-screened at the fixed 0.295 embedding threshold, survivors verified by direct YAML reading with committed per-probe tables including the search transcript.

t_now pinned per persona, byte-identical across variants. Construction-stage lexical contamination sweep runs before label freeze; flagged items route to UNRESOLVED by build rule (Phase 0: 59/201, 29%). Hard tier = SLOT-ABLATED + NATURAL-ABSENT pooled; the pre-registered headline reads it.

## 5. Index v2 and the provenance axis

Value-scrubbed renderer (attribute paths kept, values never), leakage ladder per backend per provenance, D18 inspection rule on marginal passes. Lifecycle fields included: per-category active / superseded / retracted / expired counts, supersession-event counts, scrubbed superseded slot names, recency statistics. Renderer rule: an inexpressible field emits "not expressible by this backend", never 0.

Two provenances per variant, both primary:

- TRUE-state index: built from YAML ground truth.
- BELIEVED-state index: built from the backend's own metadata, only from fields that actually resolve. Per the Phase-0 characterization (BELIEVED_STATE.md, all numbers preserved): FR-Bank overstates staleness ~60x while recalling 61% of genuine supersessions; Mem0 erases history (12.7% of entries carry updated_at and nothing else); A-MEM can express no lifecycle signal at all and its believed index builds from timestamp and last_accessed only, with the 23,403 unresolvable links reported, never repaired.

The lifecycle-ablation decomposition (new in v0.2): because A-MEM's believed index is structurally limited to counts and recency, the three-way comparison A-MEM-believed vs FR-Bank-believed vs TRUE decomposes the indexed benefit into bare count-and-recency structure versus lifecycle signal without a dedicated ablation arm. Pre-register this comparison as a named analysis. The believed-state failure taxonomy (overstate / erase / invent) is a named deliverable and a candidate Figure 1.

## 6. NOK redesign (the E1 priority)

Index carries lifecycle fields (cause 1 of the E0 null); elicitation gets a definition plus two worked examples drawn from non-scoreable material only, and a decomposed two-step form: first "does the store hold content on this topic that has been superseded, retracted, or expired?", then the NOK probability (causes 2 and 3). One arm uses a binary staircase to break the D20 quantisation.

H-NOK gate: on the intent-conditional taxonomy with the lifecycle-bearing index, indexed-TRUE NOK AUROC >= 0.65 AND indexed minus blind >= +0.10 with CI excluding 0. Believed-state NOK reports but does not gate (the corruption taxonomy may legitimately cap it; on A-MEM it is expected to fail by construction, which is itself the decomposition datapoint). Pre-committed failure consequence: NOK demotes to a reported negative result and the paper re-scopes to coverage-FOK plus control.

## 7. Elicitation, models, caching

Primary gpt-4.1-mini, temperature 0, JSON {"fok": 0-100, "nok_candidates_found": bool, "nok": 0-100, "would_search": bool}. Blind arm: one draw per unique prompt hash, shared across variants; k=3 noise subsample (~50 questions). Indexed-TRUE and indexed-BELIEVED per backend. Staircase subsample (~150 items, FR-Bank TRUE only). Strong-model integrity check: GPT-5.6 via codex exec, blind arm, ~150 stratified items; OpenRouter fallback (currently ~$4.46, thin but non-blocking). Either outcome of the integrity check is reportable; the E0 pessimistic-prior finding (mean blind FOK 0.26 vs 0.67 base rate) either generalizes to the frontier class or is bounded to small models.

## 8. Hypotheses and gates

- H1-hard: blind FOK AUROC < 0.75 on the hard tier.
- H2-hard (headline): indexed-TRUE minus blind FOK AUROC >= +0.10 on the hard tier, paired bootstrap 95% CI excluding 0. Publishability bands frozen in the prereg: < +0.10 re-scope; +0.10 to +0.15 modest, carried by NOK and control; > +0.15 stands alone.
- H-NOK: section 6.
- H-BELIEVED (report-only): believed-state indexed FOK retains >= 60% of the TRUE-state delta, per backend; the A-MEM cell is the decomposition read.
- Secondary: ECE / Brier / reliability diagrams per tier, arm, backend, provenance; pessimistic-prior re-measurement; descriptive skip-rate curves from FOK thresholds (control proper remains E2).

## 9. Analysis and integrity standards (house rules, carried)

Fixed declared universe; UNRESOLVED excluded by pre-elicitation rule with published census; sensitivity rows for every construction-stage exclusion plus the dedup row as standard; the ABSENT mechanism split (ablation / expiry / natural / ingestion-loss); matched counterfactual replay for any mechanism claim; deviations table in the main report; per-item records, cached raw responses, manifest with hashes; all amendments dated and pre-observation.

## 10. Scale, cost, stop conditions

Phase-0 projections: hard tier ~342 items against a floor of 50; whole study ~$2.50 against the $50 cap (projection-gated at $35). Stop conditions: any gate-relevant cell under 50 on the hard tier after construction; leakage ladder exhausted; verification burden materially exceeding the measured ~341; anything touching a frozen artifact; any label rule this document does not settle (conservative reading plus DEVIATIONS.md if minor, stop if load-bearing).

## 11. Resolved decisions (log)

NOK gate 0.65 (adopted). Believed-state axis primary (adopted). Strong model GPT-5.6 via codex (adopted). Natural-absent LLM-drafted with direct-YAML verification (adopted; survival 5/6, draft 7 per persona). CAT-ABLATED dropped on externals; Mem0 persona exclusions; PN full verification with the membership criterion; escalation rule retired. Timing vs FSE: decided by when Phase A starts; E1 is a multi-day build.
