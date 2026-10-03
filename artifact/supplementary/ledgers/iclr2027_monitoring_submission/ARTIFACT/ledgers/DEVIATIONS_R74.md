# Deviations and instrument failures — R74

Spec: the R74 program instructions plus `registrations/ADDENDUM_R74.md`, frozen against
baseline HEAD `67ded01b057770ffcc5fd0bb192d769c928e820c` before any monitor call. Every
departure from them, and every instrument failure found while executing them, is recorded
here. The direction-of-interest rule inherited from `DEVIATIONS_E1R.md` governs: a
departure is admissible only when it moves against the paper's interest or is a pure
correction of the spec's factual premises, with the frozen branches controlling every
interpretation.

## D-R74-1 — the addendum completes two underspecified branch sets before computation

**What changed.** (a) §X1's program spec defined only LOW (CI upper bound ≤ 0.65) and
HIGH (lower bound ≥ 0.65) branches; an interval straddling 0.65 satisfies neither. An
INDETERMINATE branch (report the row; no §7.1 change) was registered before computation.
(b) §X4's program spec did not say what happens if the budget cap stops the program with
some lanes incomplete; a cap-stop branch (completed lanes to the appendix table, no
Table-4 swap, one §5.2 sentence) and a frozen cheapest-first lane order were registered
before any projection or call.

**Why this is admissible.** Both completions were written before any number existed and
both default to the weaker claim: INDETERMINATE changes no main-text sentence, and the
cap-stop branch leaves the original registered cell primary. The D-E1R-5 precedent
("unanticipated cells are reported as such, not force-fit") is followed in advance rather
than after the fact.

**Disposition.** Registered in ADDENDUM_R74 §X1 and §X4 at the freeze commit.

## D-R74-2 — the X1 probe target is label-identical to the committed PN probe on its registered populations

**What happened.** X1 registered the FOK target (non-ABSENT vs ABSENT) on the pooled hard
tier (588) and FR-Bank hard (307). The hard tier contains no PRESENT items, so on both
populations y_fok equals y_nok item-for-item (0 differing items, verified in
`r74/x1/x1_results.json`). The FR-Bank-hard "FOK probe" is therefore the same label
vector as the committed PN probe, and its point estimate reproduces the committed 0.9199
exactly; only the pooled-588 row is a new measurement.

**Why this is admissible.** The registration is executed as frozen and the identity is
disclosed rather than presented as independent confirmation — the App D row's reading
column says "label-identical to PN on this tier" and the §7.1 sentence states the
coincidence before citing the pooled number. Nothing about the identity weakens the
branch verdict; it strengthens the caveat (coverage and obligation priors cannot be
separated by question text on this tier).

**Disposition.** HIGH branch applied within its output cap (two table rows, one
sentence). Table 15 X1 outcome updated.

## D-R74-3 — the X2 names arm has no ablation site on the external stores

**What happened.** X2's registered arm (b), "category names removed," has nothing to
remove: all 77 external index keys expose zero category names — every name-bearing
section's body is exactly the "not expressible by this backend" marker line (verified in
`r74/x2/x2_indexes.json` meta and by build-time assertion). X2b is byte-identical to the
intact index and was scored as the committed intact rows rather than re-elicited.

**Why this is admissible.** Eliciting a byte-identical prompt at temperature 0 would
re-measure the intact arm at added cost and no information; the equality is recorded on
the row (`by_construction_equals_intact`) and stated in the manuscript's table prose. The
emptiness is itself evidence about the names hypothesis: it cannot be tested by removal on
stores that render no names, which is disclosed rather than silently skipped.

## D-R74-4 — branch classifier corrected before integration; one §6 consistency edit

**What happened.** (a) The scorer's first branch classifier counted recovering arms and
returned "i-single-channel" for a recovery that is compound (count+markers), one-store
(A-MEM only), and marginal. The frozen wording reserves branch (i) for "exactly one
channel"; the compound arm is not a channel and a one-store recovery is partial. The
classifier was corrected to require a single SINGLE-channel arm recovering on both stores
for branch (i); the verdict is **branch (ii) multiple/partial**. No number changed — only
the branch label. (b) Branch (ii) authorizes the appendix table and the §5.3 citation but
says nothing about §6, whose sentence "The candidate mechanisms in Section 5.3 remain
untested" becomes false once the probe is reported. It was edited to "remain unresolved
after the registered single-channel probe."

**Why this is admissible.** Both moves go against the paper's interest: branch (ii) is
strictly weaker than (i) (no mechanism attribution, hypothesis framing kept, conclusion
untouched), and the §6 replacement claims less than the original while restoring factual
accuracy. The §7.2 "below-chance mechanism remains unresolved" sentence is untouched and
remains true.

**Disposition.** Branch (ii) integrated: `tab:x2-ablation` in App F.6, two §5.3 sentences
under kept hypothesis framing, revised Scope line preserving the bound, §6 consistency
edit, Table 15 outcome "branch ii".

## D-R74-5 — the X5 label-transfer checker failed silently before it failed honestly

**What happened.** The first X5 pass reported transfer accuracy 0.0: every extraction
returned empty while every render succeeded. Diagnosis: `subprocess` with `shell=True` on
Windows mangles arguments containing double quotes, and only the extraction prompt
contained JSON quoting — the checker never reached the model. The renders (quote-free
prompts) were valid and were kept byte-verbatim; the extraction re-ran after the spawn fix
(`x5_check.py`, direct executable, no shell). The fixed checker reports **0.9444
(34/36)**, under the registered 0.95 bar → **HARD-STOP S1**, X5 monitor calls do not
launch.

**Why this is admissible.** A checker that cannot reach the model reports an instrument
failure, not a result; declaring S1 on the broken pass would have been as wrong as
declaring PASS. The renders were never regenerated (no second draw was taken), so the
0.9444 is the first and only measurement of the registered check, and it fires the
registered stop. The two failing items are reported with their extraction evidence rather
than patched.

**Disposition.** X5 halted at S1 per its frozen protocol; exhibits staged for [AUTHOR-1]; the
ledger and Table 15 record the halt. This is the ledger-class lesson again: a seemingly
mechanical operation (shell quoting) embedded a semantic assumption (prompts survive the
spawn).

## D-R74-6 — mid-program PI budget directive: metered spend cut, subscription transports where they exist

**What happened.** Mid-X4, the PI directed that metered API spend be minimized and asked
whether `claude -p` (subscription) could carry the work. At that moment: Haiku complete
($5.36), Opus batch already finished server-side (6,609/6,610 succeeded, $40.20 — no
cancellation possible or useful), luna and X3 near-done and cheap (kept: ~$2.7 and ~$4.5
final), sol stopped at 1,422/6,610 rows ($12.39 partial), K3 stopped at 231/6,610
($3.16 partial). Subscription reality: `claude -p` can only serve Claude models (both
Claude lanes already complete); the committed subscription transport for luna/sol is
`codex exec` (the ladder's own lane); K3 has no subscription path at all. A codex
continuation for sol was probed; viability per the probe record (below).

**Why this is admissible.** The registration's cap-stop branch was frozen for exactly
this shape of stop — lanes halted by budget before completion — and it is the weaker
branch: no Table-4 primary swap unless all five new lanes complete; completed lanes print
in the expansion appendix table; partial lanes are disclosed with their row counts, never
scored as complete cells. A PI budget directive is a stricter cap, applied through the
same frozen branch. All partial rows are retained on disk (resume-keyed), never deleted.

**Disposition.** X4 integrates under the cap-stop branch with completed lanes
{mini (committed), luna, Haiku 4.5, Opus 5} unless the sol codex continuation proves
viable in time; sol and K3 report as stopped-incomplete with row counts and spend.
The codex continuation was probed and found non-viable (conversational non-JSON reply,
>10-minute single-call latency); the cap-stop branch stands. Program metered total ≈ $69
against the $700 cap.

## D-R74-8 — the sol codex transport failed both probe gates; sol stops per the PI instruction

**What happened.** The PI authorized completing sol on its committed subscription
transport (`codex exec`, the ladder's own lane) behind a 12-call probe gate. Gate one:
0/12 — sol replied conversationally ("Understood. Share the memory-store contents…") on
every call, on both arms, indicating the flattened SYSTEM+USER body was not delivered as
a completed request. Flags are parity-identical to the committed `ladder_luna.py`
invocation; the CLI drifted (codex-cli 0.147.0 vs the committed Aug-13 lane). The one
authorized fix — an explicit output-format wrapper around the byte-verbatim frozen
prompts — produced diagnostic JSON errors ("Monitoring request details were not
included") on 0/12: the wrapper's head and tail reach the model while the multi-line body
does not. Per the instruction ("still failing → stop sol, report, do not improvise a
third variant"), sol stopped. No probe row entered the lane file; the mixed-transport
guard is moot because no codex row ever joined the cell.

**Disposition.** X4 closes on BRANCH-DEFERRED for both sol and K3 (four completed lanes);
`r74/K3_RESUME_PLAN.md` and `r74/patches/k3_swap_INSTRUCTIONS.md` stage both lanes'
completion and the registered swap.

## D-R74-9 — the cut ladder is exhausted 13 review lines short of the page-9 gate

**What happened.** After the X integrations, main text ends at review line 498 against
the page-9 boundary at 485. Every authorized rung was applied: C1–C5, C6 (count-
destruction compression, numbers retained), style-legal caption/table tightening
(including removing Table 1's resolution footnote, which duplicated the §4.3 prose
verbatim), the clustered-column fallback (main-text sensitivity reduced to a pointer
clause), and blessed collapse-onto-table merges (§4.4 factorial, §7.1 probe values).
Later cuts bind only below the Table-2/Table-3 float walls, and the legally trimmable
mass below those walls is spent; word-level merges above them are absorbed by paragraph
re-fill.

**Disposition.** The residual is reported, not forced. Ranked options for [AUTHOR-1]:
(1) **Table 3 → appendix** (lossless relocation, ~11 lines, directly in the binding
region — same class as the clustered-column fallback but not pre-enumerated, so it needs
a ruling); (2) the §5.3 worked example (~3.5 lines, inside the branch-guarded range;
branch (ii) arguably licenses it but the example is the text's best intuition carrier);
(3) the abstract/intro hand-pass ([AUTHOR-1]'s), whose front-matter savings may be absorbed by
the float walls. No further cut was taken without a ruling.

## D-R74-7 — the X3 non-confirming branch forces one conclusion consistency edit

**What happened.** X3's frozen rule authorizes the Table 2 as-billed rows and the §5.4
discrepancy statement; it says nothing about the conclusion, whose sentence "Under
asymptotic caching arithmetic, it is cheaper than the blind mini monitor" would stand
uncorrected beside a billed table showing $360 against $233. The sentence was edited to
"Under the projected asymptotic caching arithmetic it is cheaper than the blind mini
monitor, an ordering the registered billed micro-run reverses at current cache pricing."
The three [AUTHOR-1]-PASS-REQUIRED abstract-ending candidates were regenerated to match (the
compiled abstract remains untouched per the standing rule; its C006 projection sentence
is flagged for the hand-pass).

**Why this is admissible.** Same pattern as D-R74-4(b): the replacement claims strictly
less than the original, restores internal consistency with a registered result, and moves
against the paper's interest (the flattering cost ordering is demoted to
regime-conditional). The abstract's compiled text was not touched; the contradiction
there is queued for the hand that owns it.
## D-R74-10 — X5 monitor launch approved; transport runs metered against the standing subscription-only directive

**What changed.** The R75 instruction records [AUTHOR-1]'s registered in-session approval: "X5
monitor calls are APPROVED. Transport ruling: run as drafted — mini metered (~$1) and
Opus 5 via Batch (~$2–3)." This is logged, before any call, as the registered one-line
deviation the ruling itself prescribes: the lanes run on metered API against the standing
subscription-transports-only directive (D-R74-6, the PI budget directive; the addendum's
own `claude -p` clause governs only question rendering, which stayed on subscription).
Cause: the codex subscription lane is broken (D-R74-8), and neither lane's model is
reachable by `claude -p` at the frozen E1/E1-XV protocols (mini is an OpenAI model; the
Opus lane is registered on the Batch API with digest-asserted raw prompts).

**Why this is admissible.** The transport is exactly the one the frozen
`PREREG_E1NS_DRAFT.md` §6 projected and priced ($6.14 inside its $10 cap; the definite
n=36 cell costs proportionally less); nothing about the measurement changes — the
deviation is purely that metered spend resumes under an explicit PI approval that
supersedes the earlier directive. Approval and ruling are quoted verbatim above.

**Disposition.** Logged before launch. Every other element of X5 runs per its freeze,
including the ruling-(a) re-rendered 36/36 cell.
## D-R74-11 — the X5 outcome matches neither frozen (i)/(ii) trigger; reported as its own cell

**What happened.** X5 completed on both lanes (NS-1 held on both; NS-2 held on Opus 5
and failed on mini). The R74 branch pair was written as "(i) blind orderings survive →
§7.1 upgrades … (ii) blind orderings collapse → the slogan's priors half demotes …".
The measured pattern is neither: the blind FOK ordering survives descriptively
(0.5788 < 0.6675 under matched authorship), while blind NOK sits at chance on both
lanes — which is NS-1's own registered prediction on a slice constructed so text
carries no label signal, not a collapse of a measured prior. The prereg §5
pre-commitment resolves the delta side independently: its confirming sentence
required NS-2 on both lanes, so the mini failure ships in its frozen words and adds
nothing.

**Why this is admissible.** Following the D-E1R-5 / D-R74-1 precedent, an
unanticipated cell is reported as such rather than force-fit to a branch. The
resolution taken is the weakest available: no §7.1 upgrade (branch (i)'s reward is
foregone), no slogan demotion (branch (ii)'s trigger is factually unmet for the
coverage half), paired-delta claims untouched, and the only paper change is the §7.2
reality update the R75 instruction itself mandates plus the Table 15 outcome cell.
Every number is ledgered in NUMBERS_R74 §X5.

**Disposition.** §7.2's "remains under construction; no monitor call has run" sentence
replaced by the measured statement naming both verdicts without printing new decimals;
Table 15 X5 outcome updated; the frozen mini FAILS text recorded verbatim in the
ledger and report.

## D-R74-12 — the R76 program is rescoped at its freeze gate: the matched-84 premise fails

**What happened.** R76 instructed a powered authorship-matched replication on "the full
matched 84-item FR-Bank cell," reusing the X5 renderer, voice spec, slot-disambiguated
instruction, and label-transfer checker. The pre-freeze premise check found the
instruction's central assumption false. The target cell
(`e1xv_crossvendor/manifests/cell_84.json`, verified {84, 54 FOK-pos, 40 PN} — the
Table 7 `0.7972` population) is a **different item universe** from the X5 cell (`frbank:*`
vs `ns:*`, zero overlap), and it cannot be authorship-matched under the frozen protocol:
`items_final.json` carries no `slot` key on any of its 2,653 items, so the renderer's
`(entity, slot, CURRENT)` input has no counterpart; 22 of 84 items are non-CURRENT intents
while both renderer and checker hardcode CURRENT, capping label transfer at 62/84 = 0.7381
against the 0.95 bar; 8 items are second-person NATURAL_ABSENT with no entity and no slot;
and the checker cannot re-derive an FR-Bank label at all, since those labels depend on a
fact's version history rather than on (intent, slot, store state). Decisively, the label is
content-borne: attack vector alone attains AUROC 0.9736 on that cell — above the supervised
probe it was meant to decompose — with six of eight strata single-class, so NS-3 (blind NOK
at chance on the matched-84) is structurally precluded rather than merely unlikely. Read
instead as powering the E1-NS cell, NS-4 is unreachable: the cell is 3 × (confirmed PN), so
the required n ≥ 87 needs ≥ 29 confirmed PN, while 11 finalized rejections cap the pool at
22 PN / n = 66, where the mini interval still includes zero (h₋ ≈ 0.2326 > Δ = 0.2028).

**Why this is admissible.** No number was invented and no registration was frozen against
an unexecutable protocol. The full arithmetic and the five structural findings are written
verbatim into `registrations/ADDENDUM_R76.md` §A1 as findings, print nowhere in the
manuscript, and cost nothing: the STOP fired before any monitor call or scored probe, at
$0 metered. The rescope is strictly subtractive on the claim side — NS-3 and NS-4 are
struck rather than weakened into something the cell could satisfy, the paraphrase
replication is declined outright (§A2), and NS-2's registered mini failure stands as the
final word on that quantity for this submission.

**Ledger class.** This is the same failure the paper's own §7.1 lesson names: a semantic
assumption ("the matched cell can be re-rendered at scale") embedded inside an instruction
that read as mechanical ("render all 84"). It was caught by the freeze-before-run gate,
which is what that gate is for. D-R74-5 was the same class one instrument down.

**Disposition.** R76 rescoped to the executable subset by [AUTHOR-1]'s in-session ruling
(path (a)): NS-5 stands, NS-6 is replaced by two $0 items, NS-3/NS-4 struck, option 4
declined. Registration `registrations/ADDENDUM_R76.md`.

## D-R74-13 — the AV-CENSUS quantity was computed before its freeze; provenance disclosed

**What happened.** The attack-vector census on the committed matched-84 labels (AUROC
0.9736; the strata table) was computed **before** ADDENDUM_R76 was frozen, as the premise
diagnostic that produced the D-R74-12 STOP. It is now registered as a reported quantity
(ADDENDUM_R76 §A4.1) and enters Appendix D, so the ordering is disclosed rather than left
for a reader to infer from the report's chronology.

**Why this is admissible.** The quantity is a deterministic census on committed labels —
the same family as the committed one-bit is-FR-Bank rule (0.7541) and the Table 16
registration census. It fits no model, holds nothing out, draws no bootstrap samples, and
has no seed; its value is invariant to when it is run, which is why a pre-freeze
computation is admissible here and would not be for a fitted or sampled estimate. It is
reported with **no sampling interval**, exactly as the is-FR-Bank rule is. The registered
script `r74/tools/x6_probes.py` recomputes the quantity after the freeze and returns the
identical value — necessarily so, since it is deterministic — so the reported number is the
pre-freeze one in substance, and the post-freeze run is a reproducibility artifact rather
than a second draw. What is disclosed is the ordering itself: this quantity was first
computed **before** the freeze, as the diagnostic that stopped the pass. What the freeze
fixes is the **interpretation**, written into §A4.1 before the value entered the manuscript,
and that interpretation moves against the paper's interest — it states that the benchmark's
own taxonomy, not a generator's fingerprint, bounds the question-only probe.

**Disposition.** Registered in ADDENDUM_R76 §A4.1 with the provenance clause; keyed
`AUX-R76-AVCENSUS`; the disclosure travels with the value into the DESCOPE report.

## D-R74-14 — NS-5 branch sentences amended before launch on the confirmation/consistency bar

**What happened.** [AUTHOR-1]'s R76-A2 launch note set a three-part bar on every NS-5 branch
sentence: each must carry n=36 explicitly, claim consistency rather than confirmation, and
state in the same sentence that XV-1's registered verdict is unchanged. Branch (ii) already
met all three and was launched unchanged. Branch (i) did not: its frozen text ended
"…survives authorship matching **and is a property of the model** rather than of how the
questions were written," which asserts as established what a single 36-item cell can only
leave standing, and it carried neither the explicit n nor the XV-1 clause. Branch (iii) met
(a) and (b) but omitted (c). Both were amended before the probe call.

**Why this is admissible.** Both amendments are strictly weakening: (i) drops an assertion
of a model property to "consistent with a property of the model" and gains the n and the
XV-1 clause; (iii) gains the XV-1 clause and softens "is a model property or an artifact" to
"reflects a property of the model or of question authorship." Neither touches a measurement,
a population, an estimator, or a gate — only the strength of the claim a branch may make,
and only downward. The amendment was logged before any call and the window closed at Batch
submission, so no measured value could have informed it.

**Disposition.** Recorded in ADDENDUM_R76 §A3 under "PRE-RUN AMENDMENT" with the original
and amended text; committed before the NS-5 launch.

## D-R74-15 — the refcheck coverage claim was false; the audit record was not (outcome (b))

**What happened.** The R75-V report line read "refcheck 26 bibitems ALL VERIFIED." R76-A5
reported "17 full-metadata VERIFIED of 26 keys" and flagged the mismatch. [AUTHOR-1] ruled that
one of the two must be wrong and ordered the reconciliation before anything further froze.
**Both were wrong.** The bibliography holds **26** bibitems; `refcheck_v10.py` carries full
metadata records for **16** of them; **10** have no record and are never checked by the tool
at all. R76-A5's "17" was itself off by one — a `grep -c VERIFIED` counted the tool's own
`ALL VERIFIED` summary line as a seventeenth entry.

**Adjudication: outcome (b) — the R75 claim was false as written**, by the mechanism
outcome (a) describes. `refcheck_v10.py` prints two adjacent, unlabelled lines:
`bibitem count: 26` (whole bibliography) and, forty lines later, `ALL VERIFIED` (scoped
only to the 16 records it holds). The R75-V line joined them. No verdict logic was ever
wrong and no bibliography entry was ever misrepresented in the underlying audit — the
instrument's *reporting* licensed a coverage claim it could not support.

**Outcome (c) is ruled out.** The split is byte-identical at the R75 baseline `b839464`
and at `f151a13`: 26 bibitems, 16 checked, 10 unchecked, with the same unchecked set
{amem, flare, fr, koriat1996, locomo, longmemeval, nelson1990, openaimemory, pricingrecord,
selfrag}. Nothing about the bibliography changed between builds.

**Materially mitigating, and it matters.** `REFCHECK_V10.md` (2026-08-15) was and remains
**correct**: its "Out-of-scope bibliography entries" section enumerates the unchecked
entries with each one's verification basis, added in its own words "so the audit's coverage
is explicit rather than silent." The standing audit record never overstated coverage. The
defect is confined to one summary line in the R75-V report, and to R76-A5's off-by-one
restatement of it. Both are annotated in place with today's date rather than edited away.

**The correct convention had already been used and was then lost.** DESCOPE_REPORT STEP 0
reports the same tool as "28 bibitems; **16 arXiv-bearing references** all 5/5 checks → ALL
VERIFIED", naming both populations and separately flagging `openaimemory` as
VERIFIED-PARTIAL. (28 rather than 26: `programrecord` and `memaudit` were removed at
STEP 2/3.) The program therefore started with the precise formulation and **regressed** to
the imprecise one by R75. This is the strongest argument for pinning the strict definition
inside the instrument rather than relying on report prose: prose conventions decay across
passes, and a summary line that cannot state its own scope will eventually be quoted
without it.

**Why this is the verify_r74 class.** A gate quoted at wider scope than it was run at is the
same failure as a gate declared and never created (the R74 verify_r74 gap, closed at R75-V).
In both cases the record asserted an assurance the instrument did not provide.

**Disposition — the stricter definition is pinned as the gate going forward.**
`iclr2027_monitoring_submission/tools/refcheck_v11.py` (repo convention: versioned
instruments, as `trace_scan_v10/v11/v12`). Verdict logic is unchanged — same 16 records,
same five fields, same MISMATCH rule. It adds (1) an explicit COVERAGE block, (2) an
`OUT_OF_SCOPE` registry transcribed from REFCHECK_V10.md so every unchecked entry names its
basis inside the tool rather than only in prose, (3) **the stricter gate: a bibitem in
neither population is a FAILURE** — under v10 a new citation with no metadata record passed
silently, and (4) a summary line that states its own scope so it cannot be quoted as
coverage it does not have. Negative test run and recorded: on a bibliography with one
fabricated uncovered citation, v10 prints "bibitem count: 27 / ALL VERIFIED" and exits 0,
while v11 reports "silently uncovered: 1" and exits 1. On the real manuscript v11 exits 0:
16/16 verified, 10 declared out of scope, 0 silently uncovered. **No bibliography entry was
edited** — this pass was enumeration and adjudication only, per the ruling.

**Two definitions, recorded so the distinction cannot collapse again.**
*Weak (what R75 quoted):* every record the tool holds passes, therefore "the bibliography
verifies." *Strict (pinned):* every bibitem is either verified against a full metadata
record or carries an explicit out-of-scope declaration naming its basis, and the count of
each is reported beside the verdict. Only the strict form may be quoted as a gate.

## D-R74-16 — the page census had no instrument; the method is pinned at R76

**What happened.** Successive reports quoted absolute review-line counts that no script in
the repo could reproduce: R74-I 498, R75-P "on the boundary at 485", R75-V 490, R76-A5 493.
`PAGE_CENSUS_V09.md` describes the method in prose only. When R76 measured the R75 build at
492 against R75-V's 490, neither number could be checked against the other, because there
was no instrument — only two prose claims.

**Disposition.** `iclr2027_monitoring_submission/tools/page_census.py` implements the R76
method (the one that exists) and is pinned: locate the page carrying the AI use statement,
which ICLR 2027 excludes from the 9-page limit, and take the greatest `lineno` margin number
above it; boundary 485 per PAGE_CENSUS_V09. Its assumptions are stated in the docstring and
one is machine-checked — the recovered numbers must be strictly increasing, so a table cell
beginning with three digits cannot silently masquerade as a line number. Under the pinned
tool: DESCOPE build 486 (+1), R74 501 (+16), R75 492 (+7), R76 493 (+8).

**Note on the discrepancy's shape.** The prior method read consistently 1--3 lines *lower*
than the pinned tool across every build, not randomly — so the earlier figures reflect a
different, now-unrecoverable convention rather than arithmetic error. Prior absolute claims
are annotated as method-unpinned rather than restated; from R76 onward the reported quantity
is the count under the pinned tool, and the +8 residual is accepted and assigned to the
[AUTHOR-1] hand-pass.

## D-R74-17 — the E1-NS counterfactual check ran before its freeze; provenance disclosed

**What happened.** R77-C required both branch wordings frozen before verification. The
structural check — which personas appear under which slot in `r74/x5/x5_render.json` — was
run first, during STOP-risk triage of the R77 order, before ADDENDUM_R77 existed.

**Why this is admissible.** Same class and same disclosure as D-R74-13: a deterministic fact
about committed data, no model, no sampling, no seed, so invariant to when it is computed.
Both branch wordings were frozen in ADDENDUM_R77 §C before either entered the manuscript,
and the branch that fired is **NO** — the answer against the paper's interest. Had the check
been run after the freeze it would have returned the same result.

**Disposition.** Branch NO integrated in Appendix D.1: within a slot the question is
near-identical and the PN rate is one third by construction, but each item is a different
persona, so the label co-varies with the whole store rather than the target's lifecycle state
alone. No counterfactual is claimed. The powered same-store cross is recorded as resubmission
scope in `reviews/REVIEW_DISPOSITION.md`.

## D-R74-18 — the R77 order cited an uncommitted ledger section

**What happened.** The R77-B instruction located the non-LLM baseline suite at
"NUMBERS.md §13C (commit a9d9d17)". Neither holds: `a9d9d17`'s `NUMBERS.md` contains no
§13C, and the §13B/§13C sections in the working tree are **uncommitted**, part of the
concurrent session's +61-line diff that this pass is forbidden to touch. Transcribing from
them would have cited another session's unsaved work as the source of record.

**Why this is admissible.** The suite itself is fully committed one level down:
`e1r_robustness/NUMBERS_E1R.md` §6 `AUX-E1R-BASELINES`, verified by `verify_e1r.py`
(346 checks, 0 failures) against the committed artifact `results/baselines_final.json`. The
transcription cites that chain instead. Per the standing numbers rule, the artifact and its
own project ledger outrank a relayed pointer, and a discrepancy is a STOP rather than a
guess — the STOP fired, the correct source was located, and no value changed.

**Second correction in the same part.** The order's main-text sentence — "the monitor
outranks every mechanical reader of the same metadata" — is false as stated: the committed
table shows a baseline outranking the monitor on A-MEM FOK-\trueidx{} (−0.0700) and on
pooled hard FOK-\trueidx{} (−0.0594). The claim holds **on the FR-Bank populations**, the
main-text sentence is scoped accordingly, and both adverse rows print in `tab:baselines`
rather than being omitted.

## D-R74-19 — SW-3's frozen sentence does not fit the measured pattern

**What happened.** R77-S measured SW-1 holding on both judgments (another persona's index
costs the monitor its whole benefit; on FOK it drives it below chance at 0.3631) and SW-2
failing on both (permuting which counts and name lists belong to which category changes
nothing). The frozen SW-3 sentence reads: "the measured benefit is not shown to be
store-specific." That is **wrong for this pattern** — SW-1 shows store-specificity directly.
What SW-2 refutes is dependence on the index's internal correspondence, which is a different
claim.

**Why this is admissible.** Following D-E1R-5 / D-R74-1 / D-R74-11, an unanticipated cell is
reported as its own cell rather than force-fit to a branch whose premise it does not match.
The frozen text is recorded verbatim in the ledger and is **not** printed, because printing
it would state something the same experiment refutes. No existing claim is weakened or
strengthened: integration is held for [AUTHOR-1] exactly as the registration requires.

**Scope limit recorded with the null so it cannot travel without it.** SHUFFLED permutes the
per-category count rows and per-category name lists only. It leaves the flat
`ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT` section untouched and preserves the global
multiset of names and counts. Its null therefore bounds the **per-category correspondence**
and nothing more; it is consistent with a monitor that checks whether a question-matching
name appears anywhere in the index and whether it is flagged superseded. Any integration
must carry this limit.

**Disposition.** Held, reported, then **ruled** (ADDENDUM_R77 §S post-result ruling,
2026-08-24). SW-1 integrates at full strength as the store-specificity result. SW-2
integrates as a mechanism bound with its scope-limit sentence attached verbatim, and one
linking clause to the redefined index and count non-necessity; the BELIEVED-retention link
was explicitly **not** drawn and survives only as a `%` comment for resubmission. The frozen
SW-3 sentence stays in the registration marked NOT-APPLICABLE-TO-THIS-PATTERN and does not
print — the D-R74-11 convention. Values `AUX-R77-SWAP-*`; `tab:wrongindex` in Appendix F
beside the count-destruction probe; two sentences in §4.4.

## D-R74-20 — the R78 A2 premise was factually wrong; corrected before print (Option 3 ruling)

**What happened.** R78's A2 instruction anticipated that Table 15's printed ∆ values might
"derive from unrounded committed values," and authorized a one-line footnote saying exactly
that. Inspection of the committed producer (`r74/tools/x7_score.py` → `score_e1.boot`) and
artifact (`r74/x7/x7_scores.json`) settled the fact differently: each printed ∆ is the
committed **paired-bootstrap mean** (1,000 item-level draws, seed 42, single-class draws
discarded) — a distinct committed estimator, not the difference of the displayed AUROC
endpoints, rounded or unrounded. The gaps between ∆ and the endpoint difference are
0.000585–0.001864 across the four cells (6–19× a 4-dp rounding step), consistent with the
Monte-Carlo noise of the bootstrap mean. Each ∆ verifies exactly against its committed key
(the standing verify_r74 checks).

**Why this is admissible.** The order's factual premise is corrected before anything prints
— the D-R74-13/D-R74-18 class: a pure correction of a spec's factual premises, moving no
claim in the paper's favor. The authorized footnote wording would have been false; printing
it was refused and the branch was pre-ruled instead.

**Disposition.** Ruled by [AUTHOR-1] at R78 planning (Option 3): the sign flip proceeds; the
footnote states plainly that each printed ∆ is the committed paired-bootstrap estimate of
manipulated minus intact rather than the difference of the two displayed columns, **and**
that the two agree within Monte Carlo error, at most 0.002 on every row — the gap size is
named so a reviewer who does the subtraction finds the discrepancy already accounted for.
The bound is ledgered as `AUX-R78-SWAP-GAP` (deterministic arithmetic on committed fields;
max gap 0.0019 at 4dp) and `verify_r74` re-derives it from the artifact. Committed values,
ledger rows, and `x7_scores.json` are untouched; the flip and footnote exist only on the
paper_v2 lineage.

## D-R81-1 — a §7.2 limitation pointed at a slice that does not exist

**What happened.** §7.2's synthetic-stores limitation ended with "the agent-generated slice
(Appendix~\ref{app:registration}) is a partial response to both concerns". A whole-tree search
finds the agent-generated slice in exactly one place: `e1_metamemory/E2_BACKLOG.md` item 6,
"a store slice written by an agent in ordinary use rather than by the benchmark generator" —
a **backlog** entry, never registered, never run, and absent from the Appendix G registration
table the sentence cited. `CLAIMS.md` (C088) compounds it by calling the slice "registered".

**What changed.** The trailing clause is deleted. **The limitation itself is kept at full
strength**: the stores are synthetic, and the two reasons are unchanged. Deleting the whole
sentence, as a literal reading of the R81 order would have it, would have dropped the
synthetic-stores disclosure, which is a claim and outside the authorization block.

**Why this is admissible.** It removes an unsupported partial-mitigation claim and leaves the
limitation harder, not softer. The direction is against the paper.

**Disposition.** The R81 report carries the finding. The E2 backlog entry stands as future
work; nothing in the manuscript now points at it.

---

## D-R81-2 — the census instrument overstated every reading by one line

**What happened.** `tools/page_census.py` reported **486** for builds whose main text ends at
**485**. Its method takes "the greatest margin line number appearing above the AI USE
STATEMENT on that page". In this build the statement is the **first line of page 10**, and
`pdftotext` emits its margin number on a separate extracted line just above the marker text,
so the tool recovered the statement's own number and returned it as the last main-text line.
The true last main-text line is the conclusion's final sentence, on page 9, at 485.

**Consequence.** Every census figure reported since the tool was written is one line high.
The R81 and R82 reports had recorded "486 against a boundary of 485, +1 over"; the paper was
in fact **at the boundary and compliant**. The frozen lineage corrects the same way, from 501
to 499.

**What changed.** The tool now extracts with `-layout`, so a margin number and the text it
numbers stay on one line; identifies the statement's own number; excludes it; and, when
nothing remains above the marker because the statement leads its page, **falls back to the
preceding page** and takes its greatest margin number. It then asserts the recovered line is
strictly below the statement's own line, and prints which page the figure came from.

**Why this is admissible.** It is a correction of an instrument against its own stated method,
and it moves **against** the paper's interest in the sense that matters: it removes a line of
apparent slack that never existed, and it makes the gate stricter by adding an assertion that
can fail. It was found while measuring Phase 4's yield, reported in the Phase 4 report before
being fixed, and fixed in Phase 5 where the order places the gate instruments. It was not
patched at the moment it was inconvenient.

**Disposition.** Every earlier "486" in `reviews/R81_REPORT.md` is corrected to 485 with a
note. The R82 report carries the same correction for its own censuses.

---

## D-R81-3 — CLAIMS.md had been reporting its own entry count wrong since R78

**What happened.** `CLAIMS.md` closed with "Entry count: 62 entries" and `CLAIMS_DIFF.md`
asserted its gate verdict "across all 62 entries" in four places. The real number of `## CL-*`
headings is **106**.

**What changed.** Both files corrected to 106, with the correction dated in `CLAIMS.md`. The
flag tallies in `CLAIMS_DIFF.md` are left as the R78 and R79 dispositions recorded them, and
are labelled as such, because re-deriving historical flag counts is not this pass's work.

**Why this is admissible.** It is a factual correction to a count, made by an instrument
rather than by eye. `tools/claims_diff.py`, written this phase, recounts the headings at every
gate run and raises a VIOLATION on any prose in either file claiming a different total, so the
figure cannot drift again silently.

**Disposition.** The instrument found this on its first run, together with confirming that all
106 ids are mapped in `CLAIMS_DIFF.md` and that all seven untouchable blocks appear exactly
once.

## D-R83-1 -- a venue upgrade outran the number that depended on it

**What happened.** Section 1 stated that no evaluated system exceeds 6% accuracy on the
multi-hop conflict-resolution slice, citing `memoryagentbench`. Under R75-F13 that bibitem was
upgraded from the 2025 arXiv preprint to `ICLR, 2026` after checking title, venue, year and lead
author. Nobody re-checked the number the sentence attributes to it. The 6% is the arXiv **v1**
figure (2025-07-07). arXiv v4 (2026-06-28) and the ICLR 2026 camera-ready both say **28%**.

The camera-ready was read directly, not inferred: "We observe that all methods fail on the
multi-hop situation (with achieving at most 28% accuracy)." Its FC-MH column agrees, with a
maximum of 28.0 (GPT-5-mini 400K) against 7.0 or lower for every other evaluated system.

**What changed.** The sentence prints 28%. Recorded as an AUTHORIZED-CORRECTION in `CLAIMS.md`,
because the value is strength-bearing: CL-C149's STRENGTH line read "6% ceiling (cited)" and now
reads "28% ceiling (cited)". The claim class does not change; it was always a cited external
ceiling, and it now carries the value the cited record prints.

**Why it was taken despite weakening the premise.** The premise is weaker at 28% than at 6%, and
is taken anyway. A motivating number a reviewer falsifies by opening the citation costs more than
a smaller true one, and the sentence still does its work: better than one system in four fails the
task the paper is about.

**Disposition.** Corrected. A method note is recorded in REFCHECK_V11 section 4: a venue or
version upgrade must re-test every number the manuscript attributes to that citation.
`refcheck_v11.py` matches this record on the literal string `ICLR` and cannot detect the class,
so the check is procedural rather than mechanical.

**Available strengthening, not taken, offered for ruling.** The camera-ready's FC-MH column shows
the 28.0 belongs to a long-context agent holding the whole history, while every dedicated memory
and RAG system tops out at 7.0. That distinction is sharper for this paper than the aggregate,
since the paper's subject is memory stores rather than long context. It is not stated in the
cited paper's own sentence and would be our reading of their table, so it is left out pending a
ruling rather than landed silently.

## D-R83-2 -- the cited table says something sharper than the sentence citing it

**What happened.** D-R83-1 corrected the motivating ceiling from 6% to 28%, which is what the
cited paper's prose states. Reading the table that prose summarises shows the 28.0 is one row:
GPT-5-mini (400K), inside Table 3's **Long-Context Agents** block. Every row outside that block
tops out at 7.0.

**What changed.** The sentence prints both ceilings under the cited table's own groupings: no
evaluated RAG or agentic-memory agent exceeds 7%, and the 28% ceiling belongs to a long-context
agent holding the entire history. Values and category names are both the source's, so this is
citation, not our reading. Table 3 blocks its rows under Long-Context Agents, Simple RAG Agents,
Embedding RAG Agents, Structure-Augmented RAG Agents and Agentic Memory Agents; section 3.2 names
the same three top-level types.

**The wording trap, recorded because it nearly landed.** The clause was first drafted as "no
evaluated memory system exceeds 7%". That is FALSE under the source's own definitions: line 69
says "we refer to agents equipped with memory mechanisms as Memory Agents", and section 3.2 puts
Long-Context Agents inside that set. GPT-5-mini is therefore a memory agent scoring 28.0. Only the
source's category names make the sentence true.

**Why it is worth the words.** This is Proposition 1 in someone else's data. A bounded retrieved
view fails the task where a full view does not, measured by a third party on a benchmark we did
not build. It is better motivating evidence than the 6% it descends from.

**Disposition.** Landed. Table citation with the column name and named row values is recorded in
REFCHECK_V11 section 4 so the next reader verifies rather than re-derives.
