# ADDENDUM_R77 — registration freeze for the R77 review-fix pass

Frozen against baseline HEAD `93b7c45` (post-R76-2), 2026-08-24, BEFORE any R77 monitor
call. Spec: the R77 program instruction. Rules inherited from R74/R75/R76: nothing
unregistered may be reported; no committed value is recomputed; registered verdicts are
never re-adjudicated; **publish-regardless** — every result prints under its frozen text.

Ledger: `r74/NUMBERS_R74.md`, new keys `AUX-R77-*`. Verifier: `r74/tools/verify_r74.py`
extended. Deviations: `iclr2027_monitoring_submission/DEVIATIONS_R74.md`, continued
numbering. Bootstrap: committed estimators, 1,000 draws, seed 42, paired, single-class
draws discarded.

Metered budget: **$5 ceiling, part S only**; everything else $0. Projection reported before
launch; the run stops at the ceiling.

---

## §C — E1-NS counterfactual verification (D2a, $0)

**Question.** Does the balanced E1-NS cell's construction constitute a within-slot store-state
counterfactual — near-identical queries scored against stores differing only in the target's
lifecycle state?

**PRE-FREEZE DISCLOSURE (D-R74-17).** The structural check was run **before this freeze**,
during STOP-risk triage of the R77 order, exactly as the AV-CENSUS quantity was at R76
(D-R74-13). It is a deterministic fact about committed data — which personas appear under
which slot in `r74/x5/x5_render.json` — with no model, no sampling, and no seed, so its value
is invariant to when it is computed. Both branch wordings below are frozen here, before
either enters the manuscript, and the branch that fired is the one **against** the paper's
interest. The ordering is disclosed rather than left to be inferred.

**Frozen branch YES** (verified: near-identical queries, same persona, store differs only in
the target's lifecycle state) → one paragraph in Appendix D.1 stating the matched cell
doubles as a small same-query store counterfactual at $n=36$, plus one pointer clause in
§7.1.

**Frozen branch NO / PARTIAL** (anything else varies alongside lifecycle state) → state
exactly what varies, claim no counterfactual, and record the full powered
PRESENT/ABSENT/PN cross as resubmission scope in the disposition.

## §S — registered wrong-index control (D2b; the only metered part)

**Populations, from the committed E1 universe, asserted by the runner.** FOK: FR-Bank hard
tier, $n=307$ (the intersection of the FR-Bank hard tier with the committed `cell_661.json`
population; 35 non-\absent{} positives). NOK: the committed FR-Bank NOK population,
$n=661$ (104 PN). Union of items = **700**; each monitor call returns both judgments, so
each arm costs 700 calls.

**Lane.** mini (`gpt-4.1-mini` pinned), temperature 0, seed 42, E1 protocol, frozen
`prompts_e1` with both digests asserted, $k=1$. Served identifier checked before launch
(E1.7 rule); mismatch = do not launch.

**Arms.** Two manipulated arms, each replacing only the index text:
- **(i) WRONG-PERSON** — each item is scored against the committed `TRUE` index of a
  *different* persona, under a fixed seed-42 derangement of the 40 personas present in the
  cell (a permutation with no fixed point, verified by assertion).
- **(ii) SHUFFLED** — each item's *own* `TRUE` index with the category count rows permuted
  and the per-category attribute-name lists permuted, under a fixed seed 42. Permutation of
  whole lines preserves byte length exactly; the assertion records the achieved length
  delta.

**Blind and intact arms are the committed E1 rows — read, never re-elicited.**

**Registered items, all branch text frozen pre-run.**
- **SW-1**: the paired intact-minus-WRONG-PERSON NOK and FOK deltas are positive with
  intervals excluding zero. Reading if held: *"The index benefit is specific to the store
  being monitored: replacing the index with another persona's costs the monitor its
  advantage on both judgments."*
- **SW-2**: the same for intact-minus-SHUFFLED. Reading if held: *"The benefit depends on
  the index's internal correspondence, not merely on the presence of index-shaped text."*
- **SW-3 (frozen adverse branch)**: if either manipulated arm is statistically
  indistinguishable from intact on a judgment — its paired delta interval including zero —
  that prints as-is with this sentence: *"On this judgment the manipulated index is
  statistically indistinguishable from the store's own, so the measured benefit is not
  shown to be store-specific."* **No existing claim is weakened or strengthened on that
  basis without a ruling; the result is flagged for [AUTHOR-1] before integration.**

**Output cap.** An appendix table beside the count-destruction probe, and at most two
sentences in §4.4.

**Projection (reported before launch).** 1,400 calls at the committed mini telemetry means
(1,552.7 input, 24.4 output tokens per indexed call; $0.40 / $1.60 per 1M): **≈$0.93**.
Ceiling $5; STOP above it.


### §S POST-RESULT RULING ([AUTHOR-1], 2026-08-24) — SW-3 held, then adjudicated

The measured pattern (SW-1 holds on both judgments, SW-2 fails on both) matched neither the
confirming reading nor the frozen SW-3 adverse sentence, so integration was **held** per the
registration and reported. [AUTHOR-1]'s ruling resolves it. **The frozen SW-3 sentence
("...the measured benefit is not shown to be store-specific") is retained here verbatim and
marked NOT-APPLICABLE-TO-THIS-PATTERN**: it presumes a manipulated-arm null implies the
benefit is not store-specific, and SW-1 refutes that premise directly. D-R74-19 records why.
Same convention as D-R74-11 — the unfired frozen text stays on the record and does not print.

**Frozen integration text, written before any paper edit.**

- **(a) SW-1 — store specificity, statable at full strength.** Registered confirming branch.
  Another persona's index does not merely erase the benefit: it inverts FOK below chance
  (0.7003 → 0.3631). The monitor reads *this* store's description, not index-shaped text.
- **(b) SW-2 — a mechanism bound, never a failure of store specificity.** Per-category
  correspondence is not necessary for the effect on FR-Bank. The result is consistent with a
  flat lookup — whether a question-matching attribute name appears anywhere in the index and
  whether it is flagged superseded. **Mandatory scope-limit sentence, travels with the result
  verbatim wherever it appears:** *SHUFFLED preserves the global multiset of names and counts
  and leaves the flat superseded-names section untouched, so it bounds per-category
  correspondence and nothing more.*
- **(c) One linking clause, no more.** It may cohere with §T1's redefined index (the name map,
  not the count structure, is load-bearing) and with count non-necessity (§4.4). **The
  BELIEVED-retention link is NOT drawn** — plausible but unregistered; a `%` comment may flag
  it for resubmission and nothing else.
- **(d) Placement.** Full table in the appendix beside the count-destruction probe; **at most
  two main-text sentences in §4.4**, one for SW-1 and one for SW-2 carrying its bound.

## §T2 — the presence-control posterior (D6, $0, deterministic)

`AUX-R77-POSTERIOR` is arithmetic on the committed `two_channel_control.json`: combined
recall 0.9950248756, so $\varepsilon = 0.0049751244$; routing verdicts ABSENT 21 / PRESENT
220 / UNRESOLVED 554. Inverting the check at specificity 1 (a truly absent target cannot be
found) gives implied truly-present $220/0.995 = 221.10$ among the 241 resolved, base rate
**0.9174**, of which $1.10$ are missed into the 21 ABSENT verdicts, so
$P(\text{present}\mid\text{claimed ABSENT}) = 1.10/21 = $ **0.0524**. No sampling, no seed;
census class, reported without an interval. The honest value prints although it is ~10×
the $\varepsilon$ the manuscript previously quoted.

## §B, §T1, §H — transcription and correction (all $0, no new measurement)

No registered predictions: these transcribe or correct, and every value is committed.
Recorded here because two of them correct a premise of the R77 order itself:

1. **§B ledger provenance.** The order cites "NUMBERS.md §13C / commit a9d9d17". §13C is
   **not committed** — it exists only in the concurrent session's uncommitted working copy of
   `e1_metamemory/NUMBERS.md`, which this pass must not touch, and `a9d9d17`'s NUMBERS.md has
   no §13C. The transcription therefore cites the committed ledger of record,
   `e1r_robustness/NUMBERS_E1R.md` §6 `AUX-E1R-BASELINES`, verified by `verify_e1r.py`
   (346 checks, 0 failures) against the committed artifact `results/baselines_final.json`.
2. **§B scope.** The order's main-text sentence says the monitor "outranks every mechanical
   reader of the same metadata." That is **false as stated**: the committed table shows a
   baseline outranking the monitor on A-MEM FOK-TRUE ($-0.0700$) and on pooled hard FOK-TRUE
   ($-0.0594$). The claim is true **on the FR-Bank populations**, and the main-text sentence
   is scoped accordingly, with the two adverse rows printed in the appendix table.
3. **§T1 tie-in.** The order says the count-destruction probe "shows where the effect
   lives." §4.4 explicitly disclaims that: it establishes count **non-necessity** and states
   it "does not isolate the map from those preserved channels." The tie sentence claims only
   non-necessity, with the name map named as a remaining candidate.

## §A — report-vs-repo sweep ($0)

Every checkable claim in DESCOPE_REPORT's DESCOPE/R74/R75/R76 sections is re-executed where a
pinned tool exists and recorded in `REPORT_AUDIT.md` as REPRODUCED / CORRECTED /
UNVERIFIABLE-annotated. New D-entries only for claims found false.

---

## Registration mechanics

One Table-15 row, added with this file's freeze-commit hash after the freeze commit exists.
Outcome cells start "pending" and update only per the frozen text above.
