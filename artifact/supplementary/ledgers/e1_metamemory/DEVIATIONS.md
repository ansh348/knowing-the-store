# DEVIATIONS — E1 full calibration study

Every departure from `E1_DESIGN.md` v0.2 and `PREREG_E1.md`, in the order encountered.
Entries marked **STOP** were escalated rather than resolved unilaterally.

**Consolidated at E1.8.** This file was appended to by each of E1, E1.5, E1.6 and E1.7, and every
append carried a trailing chunk of the previous one, so D16, D17 and D18-E1 each appeared four
times. All duplicate copies were verified byte-identical before removal. **No entry text has been
edited** — the entries below are as written, deduplicated and put in numeric order, with a summary
table added. The pre-consolidation file is in git history.

---

## Summary — every deviation, one line each

| # | what | disposition |
|---|---|---|
| **D1** | design doc absent when Phase A began | **Resolved** — v0.2 supplied verbatim in the instruction, committed unaltered, sha256 `c9ca79e8…` recorded in the prereg. |
| **D2** | E0's frozen prompt module not reused | **Resolved** — E0's system text asserts structure Mem0 and A-MEM lack; new frozen `prompts_e1.py`. E1 is therefore **not** prompt-level comparable to E0. |
| **D3** | NOK worked examples drawn from out-of-scope material | **Resolved** — both from AV8, out of scope by rule, paraphrased, no persona named. |
| **D4** | SLOT-ABLATED stored as removal sets, not materialised banks | **Resolved** — equivalent by construction; removal ids asserted against the bank. |
| **D5** | **STOP** — the lexical presence sweep is only 70% recall | **Escalated, then resolved by D6** — `ABSENT-by-ingestion-loss` asserted a cause the instrument could not establish; 207 labels renamed `sweep-negative` pending the decision, then re-routed by the two-channel instrument. |
| **D6** | two-channel control gives epsilon = 0.5% | **Resolved** — lexical .697 / embedding .965 / combined .995; external ABSENT collapses to Mem0 8 and A-MEM 13, 186 items to UNRESOLVED. Makes the probe corpus load-bearing for H-BELIEVED on the external backends. |
| **D7** | natural-absent probe survival is 52%, not 83% | **Resolved, imbalance reported not corrected** — 145/279 survived; 19 personas below target and one produced none. No re-draft: re-drafting only the shortfall personas would sample conditional on the screen having rejected their predecessors. |
| **D8** | verification burden 393 reads, not the 341 budgeted | **Logged** — all 393 performed. |
| **D9** | 6 membership exclusions outside the three named patterns | **Resolved** — tagged and reported as subtype counts, never folded into the frozen criterion. |
| **D10** | **STOP** — the conditional-GO checklist was not fully evaluable | **Escalated, then cleared** — re-evaluated after the two outstanding passes; all four items PASS (`2085330`); proceeded under the standing conditional go. |
| **D11** | index v2 line counts 31–71 against a ~40–60 target | **Logged** — wrap width is cosmetic; the pre-registered slot cap was not tuned. |
| **D12** | category/slot inexpressible on external backends under TRUE too | **Logged, reversible** — settled reading R1: provenance sets the lifecycle source only; region structure follows the store under both provenances. |
| **D13** | `recency_time` build-instrument correction | **Resolved** — recency taken from each store's own content date, not the ingest wall-clock, which is one afternoon in 2026-05 for the entire external corpus. |
| **D14** | E1 gained its own `api.py`; a thread-safety bug found in E0's | **Logged** — `_load_cache()` ran outside the lock (180 calls, 179 records). Closed in E1's adapter; E0 left alone, its runs already spent and published. |
| **D15** | probe sweep instrument tightened twice before use | **Resolved** — corpus-measured document-frequency filter, then the house ≥2-distinct-token rule: 127 → 114 → 3 probes needing a human read. |
| **D16** | elicitation run on scoreable items only | **Logged** — UNRESOLVED items are excluded from every metric by pre-elicitation rule, so eliciting them would have bought nothing and roughly doubled cost. |
| **D17** | a test run collided with the in-flight full elicitation | **Logged, no correctness impact** — the full run rewrote every output on completion; 2,698/2,698 parsed. |
| **D18** | the strong-model lane needed a Windows path fix | **Resolved** — `shutil.which` for the npm `.CMD` shim; 150/150 after. |
| **D19** | `run_a.py` imported `strong_model.py`, which has no `__main__` guard | **Resolved, and became a finding** — deduplicated keeping post-fix rows; the accidental duplicate pairs measured codex nondeterminism directly (98/129 disagreed), which is why every frontier figure is a k=5 mean. |
| **D20** | Run B killed twice by parent-shell timeouts | **Logged** — resumed from cache; no prompt or item changed. |
| **D21** | the k=5 redraw supersedes every single-draw frontier figure | **Resolved** — supersession chain resolved in `NUMBERS.md`; the single-draw run stays committed as the nondeterminism measurement. |
| **D22** | Luna emits far more tokens per turn than Sol | **Logged, corrected by D24** — 11,712 against 3,157 on a trivial probe, n=1 each. |
| **D23** | mini's blind NOK is constant, so its 0.5000 is degenerate | **Logged** — 0.0 on all 84 matched items, so every pair ties and the AUROC is 0.5 by arithmetic. Annotated wherever that cell appears. |
| **D24** | D22-E1 was wrong on both of its numbers | **Corrected in place** — measured luna 43.2 min vs sol 44.7 min (luna marginally *faster*, not ~80 min slower), and codex's "tokens used" is a turn total, not a reasoning-token count. No result depends on either. |
| **D25** | E1's Phase-C usage records were written into E0's cache | **Logged, not repaired** — `elicit_e1.py` puts E0's tools dir first on `sys.path`, so `import api` resolves to E0's. Split is exact and mechanical; repairing it would rewrite a frozen E0 artifact to fix a filing error that changed no result. |
| **D26** | the E1.8 mechanism probe runs on the pooled hard tier | **Resolved before any call** — "272" is the FR-Bank ABSENT count, the evaluable FR-Bank slice is 307, and the quoted 0.7530/0.5258 reference is the pooled n=588 row. Ran the superset so the reference applies exactly and nothing was narrowed. |
| **D27** | a DNS drop killed the first A1–A3 run at 1,111 of 1,764 calls | **Resolved** — resumed from cache at $0 for the completed calls; the $5 step cap check was made cumulative rather than per-process. The cap was never at risk. |
| **D28** | two arms were mis-filed in the economics table | **Corrected** — `draft` (40 records = one per E1 persona; E0 ran 20 and had no drafting step) and the E1.8 A1/A2/A3 arms were filed under E0. No headline figure moved. Adds a result: **A3 names-only is the cheapest index arm, $501/1M against the intact index's $519.** |
| **D29** | E1's Phase-C usage records were never committed | **Resolved** — the 3,037 records D25-E1 located in E0's cache sat uncommitted through the `e1-complete` tag, and every measured figure in `ECONOMICS.md` reads from them. Committed unmodified; no record moved or rewritten. Found while checking the tree was clean before starting E2. |
| **D31** | the answerer model was unspecified by the prereg | **Resolved** — pinned at `gpt-4.1-mini`, temp 0, seed 42, metered, before any answer existed; the instrument that must match FR is the JUDGE and it does exactly. Carry: absolute confab rates are not comparable to FR's 12.0%/24.2%; the (vi)-vs-(v) contrast is. Also added `e2_api.call_text`, since E0's client forces JSON mode. |
| **D32** | **STOP** — the retriever is not fit for purpose; calibration degenerate | **STOPPED at SP2.** Every threshold collapsed to never-retrieve. Cause is retrieval, not gating: a retrieved fact covers ≥50% of the gold on **1/57** PRESENT/PN items against FR's own **23.8%**. The gate signal is intact (FOK medians 0.700/0.400/0.200). Options and costs in `e2_metamemory/SP2_STOP.md`. |
| **D33** | the paired-difference SD was under-assumed; power collapses | **Reported, bands untouched** — measured 0.3395 against an assumed 0.200, so power at the frozen bands falls to 38.6% (H-C1a) and 27.3% (H-C1b). The SP1 freeze rule forbids re-tuning; recorded so any re-freeze starts from a measured SD. |
| **D34** | P5's registered spot-check subset is not computable as written | **Flagged before any call** — P5 needs credit and confabulation, but 66 of the 150 registered items are external and get no E2 answers by construction. Resolution offered, not taken; folds into the D32 decision. |
| **D35** | `consolidate_deviations.py` silently deleted four deviations | **Fixed.** Its heading regex hard-coded `-E1`, so `-E2` blocks parsed as nothing and were dropped on rewrite — D31-E2..D34-E2 were lost and restored from the session record. Regex now accepts any phase, and the tool **asserts that every `### D` heading present was parsed**, so an unrecognised block is a hard failure rather than a silent deletion. The tool built to protect the record damaged it once. |
| **D36** | **BRANCH B** — FR's retrieval runs, but its published run is not reproducible | **STOPPED.** r1 pass (FULL only), r2 marginal (9/10 repeats), **r3 fail**: vs the fed context, gold coverage 35.6% fresh against 30.5% cached (5.1pp, outside the band) with item-level agreement of Jaccard 0.319 / top-1 37.3%; vs `fr_bank_results` Jaccard 0.035. Fresh retrieval BEATS the cache on coverage — what fails is comparability. Cache not adopted; surviving terrain would be 178 items with ZERO ABSENT, on which H-C1a is near-vacuous. See `e2_metamemory/SUBSTRATE_FINDINGS.md`. |
| **D37** | **STOP** at SP2 round 2 — gates collapse for a substantive reason | **STOPPED.** Substrate validated (0/338 leaks, coverage 35.4%), yet fitted rates are 0.000/0.000/0.008. Retrieval gains +0.319 on PRESENT and loses −0.383 on ABSENT at 57% ABSENT, so always (0.4444) < never (0.5606) and the sweep is monotone. Oracle headroom +0.101; the FOK gate captures +0.0076 (7.5%). Damage is the hard tier: ablation-ABSENT 1.000→0.510 with 45% confabulation vs probes 0.958→0.806 at 3%. Hierarchy rule fired (100% ≥ 60%) on a degenerate contrast and is flagged uninformative. See `e2_metamemory/SP2_STOP_2.md`. |
| **D38** | **STOP** at SP2 round 3 — the calibration split cannot resolve the credit surface | **STOPPED at the decision point.** gpt-5.4 pinned by the frozen bake-off rule; item 1 fails a third time (rates 0.000/0.000/0.008). The gate clears break-even precision (0.582–0.635 vs a required 0.566, base rate 0.432) but the credit surface is only ~0.040 wide against a 132-item split where one item is worth 0.0076 — the argmax beats never-retrieve by exactly one item. At τ=0.50 the gate DOMINATES always-retrieve on both axes (0.5694 vs 0.4369 credit, 0.154 vs 0.386 confabulation). The hypotheses are alive; the selection rule is degenerate. See `e2_metamemory/SP2_STOP_3.md`. |
| **D39** | variable shadowing in `run_answers.py` — invisible on calibration, fatal on eval | **Resolved.** `frozen` named both the retrieval artifact and the thresholds dict; the collision only fires when `s2_all` is False, i.e. never on calibration. Failed loudly with a KeyError before any API call, so no eval answer was written. Also logs a cost projection error: eval gates $0.964 against a $0.38 projection. |
| **D40** | the eval judge task was stopped by the harness mid-run | **Resolved.** Stopped externally at ~150/1,179; `run_judge.py` checkpoints every 50 verdicts and skips cached keys, so the resume lost nothing and re-judged nothing. |
| **D41** | five eval judgments failed on first pass, all on one question | **Resolved.** 1,174/1,179 OK; the five failures were all `callum_q04` across two variants. The runner skips cached keys including failed ones, so the five were evicted by key and re-judged: **1,179/1,179 OK**, with `cached=1174, to judge=5` confirming no other verdict was touched. |
| **D42** | eleven P5 frontier draws failed to parse; retried to full completeness | **Resolved.** 829/840 OK on first pass (1.3%); no cell fell below E1.7's MIN_DRAWS floor of 3, checked before acting, so the retry was for completeness not necessity. Failed rows evicted by status from the resumable partial, resumed 829 done / 11 to go -> **840/840 OK**. Lane reproducibility 8/168 cells identical across 5 draws vs E1.7's sol 3/300 — same order, and why k=5 is by construction. |
| **D43** | **ledger-class** — a cached failure is indistinguishable from a cached success | **Logged as an instrument note.** The judge cache skips any present key including a `JUDGE_FAILED` one, so a failure becomes a permanent hole that no re-run fills. Same class as Incident 8 and D35. Standing lesson: **a cache that stores failures makes retry a no-op** — memoisation over a fallible call must refuse to store failures, or expose them as a state resumption re-attempts. E2's data is complete. |
| **D44** | the answer component of the cost table is priced at the wrong model's rates | **Logged, not corrected.** `usd()` prices at gpt-4.1-mini rates; the answerer is gpt-5.4, whose list price was never verified. Understates answer cost for every policy equally and therefore **overstates the gate's relative cost disadvantage**. Tokens are exact, dollars are not; `RESULTS_E2.md` §3.11 carries the caveat inline. |

---

## Full entries

### D1 — the design doc was not in the repository when Phase A began
**Reported:** "E1_DESIGN.md v0.2 is now committed."
**Observed:** no such file, tracked or untracked, and `HEAD` was still `783b1bc` (my Phase-0
resolutions commit). The same discrepancy had occurred once before, at the first Phase-A gate.
**Resolution taken:** the v0.2 text was supplied verbatim in the instructing message. I committed
it to `e1_metamemory/E1_DESIGN.md` **without alteration** and froze the pre-registration from that
file, recording its sha256 (`c9ca79e8…`) in `PREREG_E1.md` so the frozen text is identifiable.
**Why not blocking this time:** the content existed and was explicit; only the file did not. The
first gate blocked because no text existed at all, so writing the prereg would have meant
inventing the label rules. Here the label rules are quoted verbatim from the supplied text.
**Status:** resolved, logged. If the file that lands in the repository from another source differs
from sha256 `c9ca79e8…`, this pre-registration must be re-frozen against it.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D2 — E0's frozen prompt module is not reused
**E0:** `e0_metamemory/tools/prompts.py`, sha256-frozen in `PREREG_E0.md`.
**Why not carried:** its system text asserts *"Each fact carries a behavioral category, an ingest
timestamp, and lifecycle metadata."* That is false for Mem0 (no category, no lifecycle fields) and
for A-MEM (category is the constant `'Uncategorized'`, no lifecycle fields at all). Telling the
model the store has structure it does not have would confound the believed-state axis, which is
the axis E1 exists to measure.
**Resolution:** new frozen module `tools/prompts_e1.py` describing only what is true of every
backend, with its own hashes recorded in the prereg. E1 numbers are therefore **not** prompt-level
comparable to E0's; the CAT-ABLATED tier carries the E0 comparison instead, at the design level.
**Status:** resolved, logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D3 — NOK worked examples drawn from out-of-scope material
**Design doc §6:** worked examples "drawn from non-scoreable material only".
**Resolution taken:** both examples are built from `AV8_numeric_preservation` questions, which are
out of scope by rule and appear in no cell of any tier, so they cannot leak scoreable material.
The example texts are paraphrased rather than quoted, and name no persona.
**Status:** resolved, logged.

---

## Not yet reached

Phase B (build) not started. No index built, no leakage control run, **no elicitation call made**.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D4 — SLOT-ABLATED stored as removal sets, not materialised banks
201 per-question slot ablations would mean 201 near-identical 400-entry bank copies per backend.
Stored instead as `build/slot_ablations.json` mapping `persona:question_id` to the removed entry
ids; FULL and CAT-ABLATED are written out as files. The index builder applies removals on the fly.
Equivalent by construction and checkable by assertion. **Status:** resolved, logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D5 — **STOP** — the presence sweep is 70% recall, so `ABSENT-by-ingestion-loss` is not a clean label
**Prereg §3 / design §4:** "On external backends, PRESENT additionally requires sweep-verified
presence in the actual store", and gold lost to ingestion "labels as ABSENT-by-ingestion-loss".
Both presuppose the sweep is reliable.

**Measured:** applying the same lexical presence sweep to **FR-Bank FULL**, restricted to the 201
in-scope questions the YAML join says *are* answerable there, it detects presence on only
**140/201 (70%)** — a **30% false-negative rate** against known-present content.

**Consequence:** every external-backend ABSENT label inherits that rate. Mem0 is sweep-negative on
111/205 in-scope resolvable questions (54%), A-MEM on 96/222 (43%). Roughly 30% of those are
sweep failures rather than ingestion loss, and **the two cannot be separated by the current
instrument**. The label as specified asserts a cause the measurement does not establish.

**Conservative action taken, pending a decision:** the 207 affected labels are renamed from
`ingestion-loss` to **`sweep-negative`** — what the measurement actually shows — with the
false-negative rate recorded on each item. No item was relabelled to PRESENT or UNRESOLVED, and
no new rule was invented.

**Why this is escalated rather than absorbed:** it is load-bearing for two of E1's three stated
purposes — H-BELIEVED per backend, and the cross-backend replication claim — because it determines
the PRESENT/ABSENT split on two of three backends. It does **not** touch the headline H2-hard
(FR-Bank SLOT-ABLATED + NATURAL-ABSENT) and does **not** touch PN verification, which is
FR-Bank-only.

**Proposed fix (not adopted):** add an embedding channel to the sweep using the instrument already
calibrated for natural-absent probes — embed external-backend entries with
`text-embedding-3-small` (~21k entries, ~$0.01) and treat lexical-negative-but-embedding-positive
items as **UNRESOLVED** rather than ABSENT. Conservative, reuses a calibrated instrument, and
separates "not found by a weak matcher" from "not there".
**Status:** STOPPED for a decision.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D6 — the two-channel control returns epsilon = 0.5%, and external ABSENT collapses
**Amendment 1 §3** required the two-channel instrument to run the FR-Bank known-present control.
**Measured** over the 201 in-scope questions the YAML join establishes are answerable in FR-Bank
FULL: lexical recall 0.697, **embedding recall 0.965**, combined (either) **0.995**.

> **epsilon = 0.005 — a 0.5% residual false-negative rate**, down from the lexical-only 30.3%.

Routing consequence, under Amendment 1 §4: external ABSENT collapses from ~100 per backend to
**Mem0 8** (7 `ingestion-loss-attributed` + 1 `sweep-negative`) and **A-MEM 13** (12 + 1), with
**186 items moved to UNRESOLVED** as lexical-negative-but-embedding-positive. Most of what the
lexical sweep called absent was topically present content it could not confirm.

**Consequence to carry:** the external backends now have almost no ABSENT from the FULL variant,
so their ABSENT cell rests **entirely** on NATURAL-ABSENT probes. That was already the design
(both subtypes are excluded from the hard tier), but it makes the probe corpus load-bearing for
H-BELIEVED on Mem0 and A-MEM rather than merely supplementary. **Status:** resolved, logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D7 — natural-absent probe survival is 52%, not the 83% the pilot suggested
**Phase 0 sizing:** 7 drafts per persona, expected yield 5.8, from a pilot survival of 5/6.
**Measured over all 40 personas:** 279 drafted, **145 survived the screen (52%)**.

The pilot was a single persona at n=6; 83% was not a reliable estimate and the sizing rule built
on it was optimistic. Distribution of survivors per persona: 6→2, 5→7, 4→12, 3→14, 2→4, **0→1**.
**19 personas fall below the 4–6 target**, one produced none.

**Floor impact: none.** 145 probes clear the ≥50 hard-tier floor on every backend (FR-Bank hard
tier = 127 slot-ABSENT + 145 natural = 272; external hard tier = 145 each). No re-draft is
performed, because re-drafting only the shortfall personas would sample probes conditional on the
screen having already rejected their predecessors — a selection effect on the one cell that is
supposed to be honest. The per-persona imbalance is reported instead.
**Status:** resolved, logged; imbalance reported rather than corrected.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D8 — verification burden is 393 reads, not the 341 the prereg budgeted
The prereg's ~341 covered PN only (56 semantic + 192 membership = 248 measured). Natural-absent
survivors also require direct-YAML verification: **+145**. Total **393**, above the ~341 budget
and below the 500 stop threshold. Reported, not silently absorbed. **Status:** logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D9 — PN verification complete; 6 membership exclusions fall outside the three named patterns
56 semantic + 192 membership = 248 judgments, all read individually. 104 PN, 18 to UNRESOLVED.
13 membership exclusions: 5 `historically-framed`, 2 `decision-against`, and **6 outside the three
named patterns** — 3 `other:generic-not-the-dated-event`, 1 `other:unchanged-part-of-record`,
1 `other:asserts-completion-not-plan`, 1 `other:adjacent-topic-not-the-value`. All tagged, none
folded into the frozen criterion; each was excluded on the criterion as written (the entry does
not assert the superseded value as current) and only then given a descriptive name.
Table: `MEMBERSHIP_EDGE_CASES.md`. **Status:** resolved, logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D10 — **STOP** — the conditional-GO checklist cannot be fully evaluated
Items 3 and 4 pass. Items 1 and 2 are **not evaluable**: the 145 natural-absent probes are
unverified, and they constitute the entire hard tier on Mem0 and A-MEM, so no external hard-tier
cell count exists; and the leakage ladder has not finished, so no (backend, provenance) can be
asserted clean. An item that cannot be evaluated is not a pass, and the instruction is explicit —
any failure means stop, do not partially proceed. **No elicitation call made.**
This is a sequencing shortfall on my side: the 248-judgment PN pass consumed the verification
budget this round. Neither outstanding item is blocked on a decision. **Status:** STOPPED.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D11 -- index v2 line counts fall outside the ~40-60 target
Measured 31-71, mean 55.7. FR-Bank overshoots (mean ~62) because the lifecycle blocks are additive
to E0's layout; bringing it under 60 would mean cutting the pre-registered cap of 15 attribute
names per category, so the cap was kept and the cosmetic wrap widened instead. The externals
undershoot (31) because most rows are the inexpressibility marker; padding them would be
fabrication. Reported, not corrected. **Status:** logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

### D12 -- category/slot marked inexpressible on the external backends under TRUE as well as BELIEVED
Provenance sets the *lifecycle* source; region structure is a property of the store. Ground truth
cannot hand a Mem0 point a category without a classifier, which the design forbids. Conservative
branch taken. **Status:** logged; reversible if TRUE was intended to synthesise regions.

---

---

---

---

---

---

---

---

---

---

---

---

---

### D13 -- recency_time build-instrument correction
`ingest_time` on Mem0 and A-MEM is the ingest wall-clock (one afternoon for the whole corpus), so
ages against a session-date `t_now` would have collapsed to a constant, making A-MEM's believed
index -- counts and recency only -- degenerate, and publishing an instrument error as a lifecycle
finding. Fixed with an additive normalized `recency_time` taken from each store's own content
date. Documented in `STOP_POINT_2.md`. **Status:** resolved, logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

### D14 -- E1 gained its own api.py; a thread-safety bug was found in E0's
E1's Phase-0 scripts imported E0's `api` across `sys.path`, so E1 construction spend landed in
E0's ledger. E1's adapter re-points cache and decoding parameters only; the request path is
untouched. While running the ladder, 180 calls produced 179 cache records:
`e0_metamemory/tools/api.py:69` calls `_load_cache()` outside the lock, so concurrent workers
build competing dicts and the losers write to an orphan. It cannot corrupt results -- every
response is in `ladder_L0.json` -- but it silently defeats the cache. Closed in E1's adapter;
**E0's file left alone**, since E0 is published and its cache is complete. **Status:** logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

### D15 -- probe sweep instrument tightened twice before use
The first pass swept every content word and produced up to 58 hits per probe on generic
vocabulary (`type` matches every `session_plan` line). Fixed with (a) a corpus-measured
document-frequency filter dropping terms present in >50% of persona YAMLs, and (b) the house
>=2-distinct-token rule, so a hit counts only where one line or entry matches two or more probe
terms. Probes needing individual reading fell 127 -> 114 -> 3. Both fixes are measured or carried,
not hand-tuned. **Status:** resolved, logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D16 -- elicitation run on scoreable items only
The pre-registration lists the arms but does not require eliciting UNRESOLVED items, and section 8
computes every metric on the scoreable subset. Eliciting the 1,184 UNRESOLVED (question, variant)
pairs would have bought nothing and roughly doubled cost. 1,183 scoreable items elicited.
**Status:** logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D17 -- a test run collided with the in-flight full elicitation
While the full Phase-C run was in the background I launched `elicit_e1.py --limit 40` to diagnose
what looked like a stall. Both wrote the same output files and the same cache. The full run
rewrote every output on completion and its parse counts are intact (2,698/2,698; arms 332 blind /
1,183 INDEXED-TRUE / 1,183 INDEXED-BELIEVED), so the only cost was a small number of re-called
cache entries. The apparent stall was not one -- the run was progressing with buffered output, and
my own test run then satisfied the file-based wait condition I had set, which is what made it look
finished. **Status:** logged; no correctness impact.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D18-E1 -- the strong-model lane needed a Windows path fix
`subprocess` cannot resolve the bare name `codex` to the npm `.CMD` shim without a shell, so the
first strong-model attempt returned `FileNotFoundError` on all 150 items. Resolved with
`shutil.which`. Re-ran: **150/150 parsed**. The cost-routing guard (stripping `ANTHROPIC_API_KEY`
and `OPENAI_API_KEY` from the subprocess environment) is in place, closing the hazard the Phase-0
inventory flagged in the FR re-judge harness, which strips only the Anthropic key.
**Status:** resolved, logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D19-E1 -- run_a.py imported strong_model.py, which has no __main__ guard
`from strong_model import last_json, CODEX` re-executed the entire 150-item strong-model blind arm
before Run A began, and an interrupted first launch left duplicate rows in `run_a_partial.jsonl`
(279 rows, 150 distinct ids). Fixed by duplicating the two helpers into `run_a.py` rather than
editing `strong_model.py`, whose output is already committed. Rows were deduplicated keeping the
post-fix occurrence, declared before scoring; `strong_model.json` verified intact at 150/150.

**The fault produced a real measurement.** 129 items were called twice with byte-identical prompts
and **98 of those pairs disagree on FOK** -- `codex exec` at these settings is substantially
nondeterministic, well beyond E0's blind arm (90/255). Reported in the E1.5 addendum as a caveat on
Run A's interval width. **Status:** resolved, logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D20-E1 -- Run B killed twice by parent-shell timeouts
The H-b arm died at ~300/522 and again when the foreground command that launched it hit the
10-minute limit. No correctness impact: every completed call was cached, so the relaunch resumed
and reached 522/522 for $0.0216 of new spend. **Status:** logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D21-E1 -- the k=5 redraw supersedes every single-draw frontier figure
`ADDENDUM_E1_6_REDRAW.md` (`c92deef`) was committed before any redraw call. 1,500 calls, 0
exclusions, $0 (subscription-billed). Measured directly what D19-E1 inferred: **3 of 300 cells
reproduce across 5 draws (1%)**, per-item SD mean 0.0946.

Consequences, all reported in the E1.6 addendum rather than absorbed: the FR-Bank frontier delta
falls +0.1022 -> +0.0364 (the frozen rule still fires (b), now firmly rather than marginally); the
external delta moves +0.0236 -> **-0.1046 with a CI excluding zero**, confirming the below-chance
finding at frontier scale; frontier NOK strengthens to +0.3298 with a CI excluding zero; and
frontier blind FOK AUROC rises 0.7154 -> **0.8131**, which is **above the 0.75 H1 threshold**, so
`RESULTS_E1.md` section 5's conclusion that H1 "would still formally hold" for the frontier model
is **corrected: it does not hold**. The superseded tables are annotated in place and the
single-draw run remains committed. **Status:** resolved, logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D22-E1 -- Luna emits far more tokens per turn than Sol  *(CORRECTED by D24-E1)*
`gpt-5.6-luna` reported **11,712** tokens used on a trivial probe against Sol's **3,157**. No design
impact. Recorded because it is a capability-axis observation in its own right and it sets the budget
for any future rung.

**As first written this entry said two wrong things**, both corrected in **D24-E1** from E1.8
telemetry: it called the probe figures "reasoning tokens" (they are `codex` turn totals — harness
prompt + user prompt + reasoning + output), and it claimed the 1,500-call run "took ~80 minutes
rather than ~45" (measured: **luna 43.2 min, sol 44.7 min** — luna was marginally faster).
**Status:** logged, corrected.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D23-E1 -- mini's blind NOK is constant on the matched subset, so its 0.5000 is degenerate
On the 84 FR-Bank ladder items `gpt-4.1-mini`'s blind NOK is **0.0 on every item**, so every pair
is a tie and the AUROC is exactly 0.5 by arithmetic rather than by measurement. Luna's blind NOK
spans 48 distinct values and Sol's likewise, and both still fail to discriminate. Reported in place
wherever that cell appears, so the ladder's flat NOK-blind row is not read as three comparable
measurements. It strengthens rather than weakens the claim: the frontier models form varied
obligation judgments that carry no signal, which is a different failure from mini declining to
answer. **Status:** logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D24-E1 -- D22-E1 was wrong on both of its numbers; corrected from E1.8 telemetry
E1.8 Step 1 read the session transcript's tool-use and completion timestamps for every background
run. The luna ladder ran **18:43:34 -> 19:26:46 = 43.2 min**; the sol redraw ran
**17:42:49 -> 18:27:31 = 44.7 min**. Same harness, same 5 workers, same 1,500 calls, 16 minutes
apart. **Luna was marginally faster, not ~80 minutes slower.** Separately, the "~11,700 reasoning
tokens" phrasing was wrong: `codex`'s "tokens used" line is a turn total including its own system
prompt and tool schemas, and both figures are single observations on a trivial probe (n=1 per
model). The surviving observation -- luna emits ~3.7x sol's tokens per turn in the same wall clock
-- is stated correctly in `ECONOMICS.md` section 4. **No result anywhere in the study depends on
either number.** **Status:** corrected in place in D22-E1, `RESULTS_E1_7.md` and `ECONOMICS.md`.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D25-E1 -- E1's Phase-C usage records were written into E0's cache
`tools/api.py` exists precisely to keep E1's responses inside E1's write scope, but
`elicit_e1.py:37-38` inserts E1's tools dir at `sys.path[0]` and then inserts E0's at `sys.path[0]`
again, so E0's directory ends up FIRST and `import api` resolves to E0's module. Every Phase-C
record (INDEXED-TRUE 1,178 / INDEXED-BELIEVED 1,179 / BLIND 330 / BLIND-K 156 / STAIRCASE 154) and
the Phase-C meter therefore live in `e0_metamemory/cache/`. **Discovered in E1.8, after all E1
elicitation was complete.** The records are intact and carry `arm` and `item_id`, so the E0/E1 split
is exact and mechanical (E1's blind arm keys on the constant `item_id == "blind"`, E0's on the real
item id, so the two never collide); `ECONOMICS.md` reports the split. **Not repaired**: moving
records now would rewrite a frozen, committed E0 artifact to fix a filing error that changed no
result. Both caches are committed and the code path is documented here. **Status:** logged,
not repaired.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D26-E1 -- the E1.8 mechanism probe runs on the pooled hard tier, not the FR-Bank slice
The instruction names "the FR-Bank hard tier (272 items)" and gives the reference as intact 0.7530
against blind 0.5258. Those are not the same slice. **272 is the count of ABSENT items in the
FR-Bank hard tier** (127 slot-ABSENT + 145 natural-absent); a FOK AUROC needs both classes, so the
smallest evaluable FR-Bank slice is **307** (272 ABSENT + 35 PN), whose figures are **0.4966 /
0.7003**. **0.5258 / 0.7530 are the POOLED hard tier, n=588** -- the study's headline row. Since
the frozen interpretation rule is a distance from that reference, the mismatch is load-bearing.
**Resolved before any call by running all three arms on the pooled tier (n=588)**, a superset of
both readings: the instruction's reference numbers then apply exactly, the FR-Bank row is reported
against its own arm-matched reference, and no choice is forced. Cost of the superset: 1,764 calls
instead of 921, about $0.45. Recorded in `E1_8_ADDENDUM.md` before elicitation.
**Status:** resolved, logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

---

### D27-E1 -- a DNS drop killed the first A1-A3 run at 1,111 of 1,764 calls
`getaddrinfo failed` on the local network exhausted `api.py`'s four-attempt retry ladder and the
process exited. Routine transient fault, handled as the continuation instruction provides: the
1,111 completed responses were already flushed to the cache, so the resumed run re-served them for
$0 and made only the 653 remaining live calls. **No prompt, item, arm or threshold changed between
the two attempts**, and the cache key `(item_id, arm, model, prompt_hash)` guarantees the resumed
run cannot silently substitute a different prompt.

One code change was made at the resume point and is disclosed here rather than absorbed: the step's
$5 cap was being checked against `api.meter()`, which counts only the CURRENT process, so a resumed
run would have started its cap at zero. It now checks `prior + current`, where `prior` is summed
over the cached responses of the three arms -- re-run invariant, and the same device
`ladder_L0.json` already uses for `ladder_cost`. **The cap was never at risk** (step total well
under $1 against a $5 cap); the fix is for correctness of the guard, not because it bound.
**Status:** resolved, logged.

---

---

---

---

---

---

---

---

---

---

---

---

---

### D28-E1 -- two arms were mis-filed in the economics table; corrected
`tools/economics.py` classified cache records into E0's study and E1's by arm name. Two arms were
filed under E0 that are E1's: the **`draft` arm (40 records)** is the natural-absent PROBE drafting
run -- probes were an E1 addition, `PROBE_SYSTEM` lives in `prompts_e1.py`, and there are exactly 40
records, one per E1 persona, where E0 ran 20 personas and had no drafting step; and the **E1.8
A1/A2/A3 arms (588 each)**, which post-dated the classifier. Corrected in `economics.py`, and the
three mechanism arms are now reported as measured rows in `ECONOMICS.md` -- they add a result rather
than just a correction: **A3 names-only is the cheapest index arm at $501/1M against the intact
index's $519**, because deleting every count shortens the prompt. **No headline figure moved**: the
$234 blind / $519 indexed pair and every cache-adjusted number were already computed from correctly
filed arms. **Status:** corrected.

---

---

---

---

---

---

---

---

---

---

---

---

---

### D29-E1 -- E1's Phase-C usage records were never committed
D25-E1 recorded that `elicit_e1.py` writes E1's responses into `e0_metamemory/cache/` through a
`sys.path` ordering bug. What it did not catch is that those 3,037 records -- INDEXED-BELIEVED
1,179 / INDEXED-TRUE 1,178 / BLIND 330 / BLIND-K 156 / STAIRCASE 154 / draft 40 -- **sat uncommitted
in the working tree**, including through the E1.8 closeout and the `e1-complete` tag. Every measured
figure in `ECONOMICS.md` is read from them, so on a fresh clone that file could not be regenerated.
Found while checking the tree was clean before starting E2.

**Committed now, unmodified.** This is not the "repair" D25-E1 declined: no record is moved or
rewritten, and E0's own 1,071 records are untouched. It records what actually happened, which is
what a frozen artifact is for. The `e1-complete` tag now points at a commit whose economics inputs
are one commit behind; **`ECONOMICS.md` regenerates byte-identically from the committed state**, and
that is asserted by re-running `tools/economics.py` at this commit. **Status:** resolved, logged.

---

---

---

---

---

---

---

---

---

---

### D31-E2 -- the answerer model was unspecified by the prereg; pinned at the calibration boundary
`PREREG_E2` section 3 pins the answer PROMPT (FR's `GENERATION_SYSTEM_PROMPT`, verbatim) but never
names the answerer MODEL. Pinned here as **`gpt-4.1-mini`, temperature 0, seed 42, metered**, before
any answer was generated. The instrument that must match FR is the JUDGE, and it does exactly
(`claude-sonnet-4-6`, FR's rubric read out of `evaluate_e2e.py` by AST so it cannot drift); the
answerer only has to be identical across policies, which it is. The metered lane is also the only
one that records per-call telemetry (D24-E1). **Carry: absolute confabulation rates are not
comparable to FR's 12.0%/24.2%**; the (vi)-vs-(v) contrast H-C2 tests is internally valid regardless.

Second item, same heading: E0's `api.call` hard-codes `response_format={"type": "json_object"}`,
right for every judgment arm and wrong for a free-text answerer. Rather than bend FR's frozen prompt
to suit the client, `e2_api.call_text` adds a text path reusing E0's cache, lock, meter and retry
ladder directly, so spend accounting cannot drift. **Status:** resolved, logged.

---

---

---

---

---

---

---

---

---

### D32-E2 -- **STOP** -- the retriever is not fit for purpose, and calibration is degenerate
Calibration ran to completion and **every fitted threshold collapsed to "never retrieve"** (tau_sim
0.60, tau_verb 0.95, tau_FOK 0.90, all at retrieval rate 0.00). Never-retrieve scores **0.5606**
against always-retrieve's **0.4242**, so the pre-registered credit-per-dollar objective correctly
walked every gate to the floor.

**Cause: retrieval, not gating.** On PRESENT items -- whose gold IS in the store -- retrieving
produces credit **0.000**, on all 35 PRESENT and all 22 PN calibration items across three draws. The
decisive measurement: **a retrieved fact covers >=50% of the gold answer's tokens on 1 of 57
PRESENT/PN items (1.8%), against 23.8% for FR's own committed retrieval** -- a ~13x gap. Max cosine
barely separates the classes (median 0.319 PRESENT vs 0.286 ABSENT), so no threshold rescues it. I
built the retriever as raw top-5 cosine over `text-embedding-3-small`; FR's real system routes by
category, applies a semantic floor and filters by lifecycle state. **A defect in my substrate, not a
finding about gating.** It also invalidates baseline (iii), which reads the same signal.

**The gate signal is intact**: on the same items, indexed FOK medians are 0.700 PRESENT / 0.400 PN /
0.200 ABSENT -- E1 reproduces on the calibration split. The failure is strictly downstream of the
gate. **Status:** STOPPED at SP2 for a decision; options and costs in `e2_metamemory/SP2_STOP.md`.

---

---

---

---

---

---

---

---

---

### D33-E2 -- the paired-difference SD was under-assumed; power at the frozen bands collapses
`E2_DESIGN` section 2 assumed a paired-difference SD of 0.20. Measured on calibration: **0.3395**,
so SE rises from 0.01304 to **0.02214** and power at the frozen bands falls from **74.4% to 38.6%**
(H-C1a) and **63.3% to 27.3%** (H-C1b). Credit is more nearly bimodal than assumed and the policies
disagree on more items than assumed. **The bands are NOT touched**, per the SP1 freeze rule: power is
recomputed and reported as information for the stop/go call, never as a licence to adjust. Recorded
so that any re-freeze starts from a measured SD. **Status:** reported; bands untouched.

---

---

---

---

---

---

---

---

---

### D34-E2 -- P5's registered spot-check subset is not computable as written
`PREREG_E2` section 7 puts the frontier spot-check on "the 150-item E1.7 subset". Discovered before
any spot-check call: **P5's endpoints are credit and confabulation, which require downstream
answers, and 66 of those 150 items are Mem0/A-MEM items for which E2 generates no answers by
construction.** Of the 84 FR-Bank items, those in calibration personas cannot be scored against an
eval-split comparison. The prereg registered a subset on which its own prediction cannot be
evaluated. No spot-check call has been made, so nothing is contaminated. The conservative resolution
-- the FR-Bank eval split, a strict enlargement -- is **offered, not taken**, and folds into whatever
re-freeze follows D32-E2. **Status:** flagged before any call; awaiting the D32 decision.

---

---

---

---

---

---

---

---

---

### D35-E2 -- `consolidate_deviations.py` silently deleted four deviations
Its heading regex hard-coded the `-E1` suffix, so the four `-E2` blocks appended above parsed as
nothing, were excluded from the parsed set, and **were deleted when the file was rewritten from that
set**. Found immediately, by grepping for the entries just written; restored from the session record.

Two fixes. The regex now accepts any phase suffix. More importantly, the tool now **counts every
`### D` heading in the input and refuses to run if that count differs from the number parsed**, so a
block it cannot recognise is a hard failure instead of a silent deletion.

**The tool built to protect the record is the tool that damaged it**, and it did so in the same class
as ledger Incident 8: a silent omission that every existing check passed over. A rewrite-from-parse
is only as safe as its parser, and it must therefore prove it parsed everything before it writes.
**Status:** fixed, entries restored, guard added.

---

---

---

---

---

---

---

---

### D36-E2 -- BRANCH B: FR's retrieval is runnable but its published run is not reproducible
E2 Amendment 1 STEP 1. FR's retrieval is `lifecycle_search` in `lifecycle_bank.py`: cosine top-60 ->
BM25 -> category-forced -> multi-hop -> **LLM distillation** (gpt-4.1-mini, temp 0) -> lifecycle
filters -> blended scoring with a semantic floor at 0.85 -> top-10. Probed on 59 items stratified
across 7 AVs from the 178-item FULL-slice overlap, `t_now = max(active.created_at)+24h`, defaults.

**r1 PASS (partially)** -- runs on 59/59 items; proven on FULL only, ablated variants untested.
**r2 MARGINAL** -- 9/10 repeat queries identical; the distillation call carries no seed.
**r3 FAIL.** Two cached artifacts exist and disagree. Against `fr_bank_results.top5_facts`: Jaccard
**0.035**, top-1 **6.8%**, and that artifact's own gold coverage is **1.7%** -- it is not a usable
retrieval record. Against the actually-fed context (`e2e_responses[gpt54_nr].fr_bank_facts`): gold
coverage **35.6% fresh vs 30.5% cached = 5.1pp apart, outside the 5pp band**, with item-level
agreement of only **Jaccard 0.319 / top-1 37.3%**. An earlier independent check reaches the same
verdict by a stricter route: `audit/full_history_baseline/dryrun_fr_fidelity_report.json` records
`pass = false`, three stratified questions, all MISMATCH.

**The code is runnable and runs well -- fresh retrieval BEATS the cached context on gold coverage.
What fails is comparability, which was the only reason to want the cache.** Per the amendment that
is treated as not runnable for comparability purposes, so **Branch B**: nothing refit, nothing
re-frozen, the cache not adopted, and the hierarchy decision returned to [AUTHOR-1] with
`e2_metamemory/SUBSTRATE_FINDINGS.md`.

That file records the surviving terrain under cache adoption -- **178 items, 131 PRESENT + 47 PN,
ZERO ABSENT**, 26.4% PN density, re-derived split 34 calibration / 144 eval -- and shows why it is
not usable: with no ABSENT items no skip is ever correct, so H-C1a is near-vacuous, H-C1b's CI
half-width is ~0.083 against a +0.03 band, and H-C2's 80%-power MDE is 6.2-9.7pp against a frozen
3pp band. **Status:** STOPPED at Branch B; awaiting the hierarchy and substrate decision.

---

---

---

---

---

---

---

### D37-E2 -- **STOP** at SP2 round 2: gates still collapse, now for a substantive reason
Substrate repaired and validated (v1 0/338 leaks, v2 35.4% vs 35.6%, ablation biting: gold coverage
FULL 35.4% -> SLOT-ABLATED 11.1%). Retrieval finds the gold about a third of the time, matching FR's
own published performance. **Checklist item 1 still fails**: fitted retrieval rates (iii) 0.000,
(iv) 0.000, (v) 0.008 -- all within 0.02 of each other and of the floor.

**This time it is not an instrument defect.** Retrieval gains **+0.319** credit on PRESENT and loses
**-0.383** on ABSENT, and 57% of items are ABSENT, so always-retrieve (0.4444) sits below
never-retrieve (0.5606). The FOK sweep is **monotone** -- credit rises all the way as the gate
tightens, and best-by-credit agrees with best-by-objective at tau 0.85, so the credit-per-dollar
objective is NOT what forces the floor. A perfect gate would score **0.6615**, so oracle headroom
over never-retrieve is **+0.101**; the FOK gate captures **+0.0076, about 7.5% of it**.

**Where the damage is: the hard tier.** Ablation-induced ABSENT items go S0 1.000 -> S1 **0.510**
with confabulation **0.451**, while natural-absent probes go 0.958 -> 0.806 with confabulation 0.028.
**Near-miss context is far more dangerous than off-topic context** -- measured end-to-end for the
first time. And on PRESENT/PN items credit is 0.296 with the gold retrieved against 0.205 without,
so retrieval helps mostly by giving the model something to say rather than the right thing.

**The frozen hierarchy rule fired and its input is degenerate.** H-C1b power computed to 100.0%
(>= 60%), so the e2-sp1 ordering formally stands -- but that power comes from a paired SD of 0.087
between two policies that both retrieve on almost nothing. The rule was applied faithfully to data
that cannot support it; the verdict is recorded because the rule says to, and flagged as
uninformative because it is.

Options and costs in `e2_metamemory/SP2_STOP_2.md`. Recommendation: pin a stronger answerer -- the
prereg pins the answer PROMPT, not the model (D31-E2), and the diagnostic says the ceiling is the
answer step, not the gate -- then re-run this checklist. **Status:** STOPPED; no band, margin,
split, renderer or hierarchy touched; retrieval artifact immutable.

---

---

---

---

---

---

### D38-E2 -- **STOP** at SP2 round 3: the calibration split cannot resolve the credit surface
Answerer replaced under the Amendment 3 frozen rule (**gpt-5.4**, bar 0.600 >= 0.55, selected as FR's
own answerer so FR-comparability is restored). Substrate validated. Item 1 fails a **third** time:
fitted rates (iii) 0.000, (iv) 0.000, (v) 0.008.

**The diagnosis, with a number.** The gate's discrimination is real: break-even requires precision
>= **0.566** for non-ABSENT against a base rate of **0.432**, and the FOK gate delivers **0.582-0.635**
from tau >= 0.20 onward. But clearing break-even by 1.6-6.9 points is worth almost nothing by
construction, so it converts to no credit. **The entire interesting range of the credit surface is
~0.040 wide; the calibration split is 132 items, so ONE ITEM IS WORTH 0.0076. The whole decision
surface is about five items across, and the argmax at tau 0.85 beats never-retrieve by exactly one
item.** Threshold selection on calibration credit is under-resolved by roughly 4:1. No answerer,
substrate or objective change fixes that -- it is the split size against a flat surface, and it was
invisible until the substrate and the answerer were both healthy enough to rule out.

**The hypotheses are alive; the selection rule is what is degenerate.** At tau = 0.50 the gate
DOMINATES always-retrieve on both axes -- credit **0.5694 vs 0.4369** and confabulation **0.154 vs
0.386** -- while retrieving on a third of turns. H-C1a as pre-registered would pass emphatically
there, by superiority rather than non-inferiority. The confabulation surface spans 0.386 -> 0.000
across the sweep, **ten times** the credit surface's range, and would resolve cleanly on 132 items.

**The answerer swap worked**: headroom +0.1023 -> **+0.1856** (+81%), because gpt-5.4 uses good
context better (S1 PRESENT 0.329 -> 0.457) and is more damaged by near-miss context (ablation-ABSENT
confabulation 0.471 -> **0.706**). It moved the binding constraint from the answer step to the
selection step. Judge validity spot-check (20/candidate, no bar): correctness agreement
1.00/1.00/0.95/1.00, confabulation 1.00/1.00/1.00/0.95 -- the judge is not the problem.

Options in `e2_metamemory/SP2_STOP_3.md`; recommendation B (fix the operating point by decision
theory rather than by argmaxing a surface narrower than its noise) with D (reorder to H-C2 first) as
secondary. **Status:** STOPPED at the decision point; no band, margin, split, renderer, hierarchy or
retrieval artifact touched.

---

---

---

---

---

### D39-E2 -- variable shadowing in `run_answers.py`: invisible on calibration, fatal on eval
The Amendment-2 patch introduced `frozen` for the retrieval artifact; pre-existing code four lines
later reused the same name for the thresholds dict:

    frozen = {r["item_id"]: r for r in fr["rows"]}      # retrieval artifact
    ...
    if not s2_all:
        frozen = jload(".../THRESHOLDS_FROZEN.json")    # clobbers it

On the **calibration** split `s2_all` is True, so the shadowing branch never ran and the collision
was invisible through three rounds. On **eval** it fired and `frozen[tag]` looked up an item id in a
thresholds dict. Renamed to `thr`, with the reason recorded in a comment at the site.

**It failed loudly rather than quietly** -- a `KeyError` during job construction, before any API
call -- so **no eval answer was written**, confirmed on disk before resuming. Nothing discarded,
nothing contaminated. Eval gates had already completed (2,645 calls, all parsed); gate signals are
inputs, not outcomes, so eval hygiene is intact.

**Cost projection error, reported rather than absorbed:** eval gates cost **$0.964** against a $0.38
projection. k=3 on the eval split is 529x3 verbal + 529x2 extra indexed = 2,645 calls, and I priced
them all at the cheaper verbal rate instead of accounting for the ~1,200-token indexed prompts.
Cumulative $1.72 of $25 -- far under the cap and under the $15 gate, but the projection was wrong.
**Status:** resolved, logged.

---

---

---

---

---

### D40-E2 -- the eval judge task was stopped by the harness mid-run; resumed from cache
The background task running eval judging was stopped externally at ~150/1,179 distinct responses.
Not a fault in the run: `run_judge.py` checkpoints its cache every 50 verdicts and skips cached keys
on restart, so the resume picked up at **150 cached, 1,029 to judge** with no re-judging and no lost
work. Relaunched detached. No prompt, item, rubric or answer changed between attempts, and the
judgment cache key `(item_id, response_sha)` guarantees a resumed run cannot substitute a different
response. **Status:** resolved, logged.

---

---

---

---

### D41-E2 -- five eval judgments failed on first pass, all on one question; cleared on retry
The eval judge returned **1,174 OK / 5 failed** over 1,179 distinct responses (0.42%). All five were
the same question, `callum_q04`, across two variants (FULL and SLOT-ABLATED) -- a clustering that
points at the item's content rather than at transport noise, though the cause was not diagnosed
because it did not survive.

`run_judge.py` skips any key already in its cache, **including a failed one**, so a plain re-run
would not have retried them. The five failed entries were evicted by key and the judge re-run:
**1,179/1,179 OK, 0 failed.** No other verdict was touched -- the run reported `cached=1174,
to judge=5`. **Status:** resolved; full completeness on the eval endpoint.

---

---

---

### D42-E2 -- eleven P5 frontier draws failed to parse; retried to full completeness
The codex lane returned **829 OK / 11 PARSE_FAIL** over 840 draws (1.3%) -- 5 on the verbal arm, 6
on the indexed arm. **No cell was left below E1.7's MIN_DRAWS floor of 3**, checked before acting, so
the data were already usable; the retry was for completeness, not necessity. The 11 failed rows were
evicted from the resumable partial file by status and the run resumed (`829 done, 11 to go`):
**840/840 OK, 0 failures.** No prompt, item, model or draw index changed between attempts, and the
`(item, arm, model, draw, prompt_hash)` key makes substitution impossible.

**Lane reproducibility, reported as a standing disclosure:** 8 of 168 cells identical across 5 draws
(4.8%), against E1.7's sol reference of 3/300 (1%). Same order of magnitude, and the reason k=5 is
by construction on this lane. **Status:** resolved; full completeness on P5.


---

---

### D43-E2 -- LEDGER-CLASS INSTRUMENT NOTE: a cached failure is indistinguishable from a cached success
Raised at [AUTHOR-1]'s instruction from D41-E2. `run_judge.py` caches every verdict keyed
`(item_id, response_sha)` and skips any key already present -- **including one whose status is
`JUDGE_FAILED`**. A failure therefore persists as a permanent hole that no re-run will fill, and the
only thing that surfaces it is the run's own OK/failed counter, which a resumed run reports against
the *remaining* work rather than the whole. On the eval split five holes survived that way and were
found only because the completion line was read against the 1,179 denominator.

**Same class as ledger Incident 8 and D35-E2:** a silent omission that every existing check passed
over, because the checks ran on what was present rather than on what should have been.

**Standing lesson, wider than this tool:** *a cache that stores failures makes retry a no-op.* Any
memoisation over a fallible call must either refuse to store a failure, or expose failures as a
distinct state that resumption re-attempts. The fix applied here was manual eviction by status; the
durable fix -- not storing failures at all -- is recorded for whatever the next harness is.
**Status:** logged as an instrument note; E2's own data is complete (1,179/1,179, 840/840).

---

---

### D44-E2 -- the answer component of the cost table is priced at the wrong model's rates
`e2_common.usd()` prices tokens at `gpt-4.1-mini`'s $0.40/$1.60. After Amendment 3 the answerer is
**gpt-5.4**, whose list price was never independently verified -- the amendment recorded it as
"measured", and only TOKENS were measured. The answer component of every serving-cost figure is
therefore mini-priced.

**Direction of the error, stated so the number can be used carefully:** it understates the answer
cost for **every policy equally**, and therefore **overstates the gate's relative cost
disadvantage** -- a larger true answer cost would shrink the gate's share of the total. Token counts
are exact; the dollar level is not. `RESULTS_E2.md` section 3.11 carries the caveat inline and
instructs that the dollar column not be quoted without it. **Status:** logged; not corrected, because
correcting it requires a verified gpt-5.4 price this study does not have.
