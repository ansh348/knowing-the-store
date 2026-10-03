# ADDENDUM_DS Amendment 8: label propagation inside the view (E4)

Registration for the author's freeze (program R117; drafted 2026-09-18 BEFORE any call, the author's rulings of 2026-09-19 folded in: matching by the census function unchanged, the age-field ordering, one secondary offline arm without the ordering condition). Carries five predictions (P-L1 to P-L5) with failure texts; P-L4 turns descriptive if its interval includes zero. Frozen by its sha256, recorded in `ds_downstream/NUMBERS_DS.md` before the first call; the runner writes `run/lock_amend8.json` with that hash at start. Nothing here re-adjudicates DS, its Amendments 1 to 7, or the audit; the recorded views and answers are read and never re-run. All stale and correct counts are the token detector's, and every held text says so.

## §1: Why

Section 9 traces the flagged stale answers to active duplicates that carry no tag, and Amendment 5 showed that tagging them from the manifest removes most flags. That repair used reference information. This amendment tests a repair that reads only the assembled view.

## §2: Population and the recorded rows

The recorded views of `ds_downstream/views.json` (452 distinct views over 661 items and seven policies; each line `[rank] lifecycle: <active|superseded|retracted|expired> | category: <C> | attribute: <slot key> | age: <N> days | text: <sentence>`; no ingest timestamp and no event time are on the line, so the age in days before the store's pinned current time orders the writes: a larger age is an earlier write). Three policies of Table 4: **ALWAYS** (top-five retrieval), **MODEL** (the model rule), **ORACLE**. Two tag sources: the recorded ground-truth tags of `views.json`, and **FR-Bank's own tags**, the same views re-rendered line by line with the store's own lifecycle field by the recipe of RESP Amendment 1 (`resp_review/l2/retrieval_believed.json`, `resp_review/tools/amend1_resp.py` section A, `believed_flags`), a pure function of the recorded ids, committed before the run as `ds_downstream/tools/amend8_propagate.py --own-tags`. Populations: the 89 scorable obligations (the obligations whose stale string the detector scores at both thresholds, NUMBERS_DS.md section 9) and their views under the three policies; the 174 items whose licensed record the store holds, and their views. The 35 audited duplicate views: `reviews/downstream_audit/step4b_view_lines.json` (`view_lines`, keyed `<item_id>|<policy>`, field `active_stale` = the ranks of the active lines asserting the stale value), the population Amendment 5 tagged (35 items, 74 changed views, 132 lines).

## §3: The rule (exact; reads only the view)

For a view V with lines $\ell_1 \ldots \ell_n$, each with tag $t$, attribute $a$, age $g$ (days) and text $x$; tokens by `e0_common.toks` with the persona's name tokens dropped (the name is read from the view's own header, Amendment 4's form; nothing is read from the manifest, the alignment or the detector's labels):

1. A **tagged line** is one with $t \in \{$superseded, retracted, expired$\}$; an **untagged line** has $t =$ active.
2. **Matching (the ruling: same attribute, the census function unchanged).** For a tagged line $s$, its **successor candidate** $m$ is the newest active line (smallest age) with $a_m = a_s$ whose text does not repeat $s$'s at the census threshold ($\mathrm{cov}(\mathrm{toks}(x_s), \mathrm{toks}(x_m)) < 0.80$). Where $m$ exists, the untagged lines of attribute $a_s$ are scored by `index_v2.detect(old_fact = x_s, new_fact = x_m, etoks, drop)` exactly as the census scores an entry against a manifest pair: $u$ matches iff $|D_{old} \cap \mathrm{toks}(x_u)| \ge 2$ (`MIN_SHARED`), $\mathrm{cov}(D_{new}, \mathrm{toks}(x_u)) < 0.34$ (`CROSS_GUARD`) and $\mathrm{cov}(D_{old}, \mathrm{toks}(x_u)) \ge 0.80$ (`TAU_HI`), with $D_{old} = \mathrm{toks}(x_s) \setminus \mathrm{toks}(x_m)$, $D_{new} = \mathrm{toks}(x_m) \setminus \mathrm{toks}(x_s)$ and `MIN_DISCR` 3 on both sides (a pair the function declares unresolvable propagates nothing and is counted). Where no $m$ exists there is no new value: $D_{old} = \mathrm{toks}(x_s)$, $D_{new} = \emptyset$, the cross guard vacuous, the same two thresholds.
3. **Ordering (the ruling, on the age field).** Where $m$ exists, $u$ propagates only if it is older than the newest such line: $g_u > g_m$. Where no $m$ exists, $u$ propagates only if it is no newer than its tagged line: $g_u \ge g_s$. A line failing the condition is a return to the old value and stays active.
4. The tag propagated is $s$'s tag; where two tagged lines of different tags match $u$, the one with the smaller age wins. The rule runs once over the view (no chaining from newly tagged lines). Every other character of the view is unchanged; the line rule and the header are Amendment 4's.

**Secondary arm (registered, offline only; the ruling):** the same rule with no ordering condition (step 3 dropped), scored for measures (i) and (ii) only, never re-answered; it prints beside the primary as the catch and false-propagation ceiling of the matching step.

Locks asserted before any call: the rule reproduces itself on a second pass (idempotent); no line changes except its lifecycle field; the count of changed views and lines per policy, tag source and arm is recorded before answering.

## §4: Measures

(i) Of the 35 audited duplicate views (74 view instances), how many have **every** active-stale line of the audit tagged after propagation, per tag source (ground truth: the audit's `active_stale` ranks; own tags: the same ranks). (ii) **False propagation:** of the licensed items' lines that are active in the ground-truth view, the share that receives a non-active tag under the rule, per tag source, scored against the ground-truth tags (a line the ground truth marks active that the rule tags is a false propagation). (iii) Every view the rule changed is re-answered once by GPT-4.1 mini (temperature 0, seed 42, max_tokens 200, JSON mode) and by Haiku 4.5 (temperature 0, max_tokens 200), under the Amendment 4 persona-and-date header and prompt texts (`prompts_ds`, digests asserted), the same detector (`index_v2.detect` at 0.50 and 0.80 as Amendment 5 reports them): detector-flagged stale answers at 0.50 and correct licensed answers, per policy and tag source, beside the recorded Amendment 4 rows on the same views; unchanged views keep their recorded answers.

## §5: Predictions

- **P-L1.** Under ground-truth tags, at least 18 of the 35 audited duplicate views (counted by item, every policy instance of the item fully tagged) are fully tagged after propagation.
- **P-L2.** Under ground-truth tags, false propagation is at most 5% of the licensed items' active lines.
- **P-L3.** Under the model rule with ground-truth tags, the flagged stale rate at 0.50 (stale answers over answered obligations, GPT-4.1 mini) falls by at least half against the recorded Amendment 4 row on the same views.
- **P-L4.** That reduction is larger under the model rule than under top-five retrieval: the difference of the two reductions, with its persona-grouped interval (10,000 draws, seed 42, over the 40 personas); descriptive if the interval includes zero.
- **P-L5.** Under FR-Bank's own tags, false propagation exceeds 5% of the licensed items' active lines.

Failure texts, frozen: "P-L1 FAILS: $k$ of 35 duplicate views are fully tagged by propagation." / "P-L2 FAILS: propagation tags $p\%$ of the licensed items' active lines under ground-truth tags." / "P-L3 FAILS: under the model rule the flagged stale rate moves from $r_0$ to $r_1$." / "P-L5 FAILS: under the store's own tags false propagation is $p\%$, at or under 5%."

## §6: Held texts, both branches (Phase 3, by ruling)

Up to two Section 9 sentences after the retagging sentence, e.g. holds: "A rule that reads only the view, propagating a line's lifecycle tag to the untagged lines of the same slot that repeat its value, tags $k$ of the 35 duplicate views and halves the flagged stale rate under the model rule, with false propagation at $p\%$ under ground-truth tags and $q\%$ under the store's own (Appendix E.10; detector counts)." Fails: the sentence states the count and the rate that did not move, with the numbers. Appendix E.10 gains `tab:ds-a8` (measures i to iii per policy and tag source). Candidate rewording of the builders' box, third sentence, for the ruling: "Compare a name lookup with the model on the actual store before paying for the model call, and propagate a record's lifecycle tag to its untagged duplicates before answering (Sections 5, 7 and 9)."

## §7: Budget, order, STOP

Propagation, the censuses and measures (i) and (ii): $0. Re-answers: at most 3 policies × 2 tag sources × 263 items = 1,578 changed views (an upper bound; Amendment 5 changed 74 of 452), each once per answerer: GPT-4.1 mini at the recorded answer-stage figure $0.00028 per call, Haiku 4.5 at $0.00078 (Amendment 5's probes: 528 / 547 input, 19 / 29 output; list prices), **upper bound $1.67, expected under $0.60**, probes $0.01; **against the $5 cap (×1.3 of the upper bound: $2.2)**. Order: own-tag re-render (no call) → rule and locks → measures (i), (ii) → probes → mini → Haiku 4.5 → measure (iii). STOP: registration sha256 mismatch; a lock failure; served-identifier mismatch; more than 2% of a lane's rows not OK after the retry; a projection over the cap.

## §8: Ledger and paper site

`ds_downstream/NUMBERS_DS.md` section 15: `AUX-DS-A8-LOCK`, `-A8-RULE-CENSUS` (changed views and lines per policy, tag source and arm), `-A8-DUP35`, `-A8-FALSEPROP` (both arms), `-A8-STAGE2-MINI`, `-A8-STAGE2-H45`, `-A8-P-L1` to `-P-L5`, `-A8-SPEND`. Paper: up to two sentences in Section 9, `tab:ds-a8` in Appendix E.10, the box sentence by ruling.

## Registration mechanics

Frozen by sha256 before the first call. Copied to `iclr2027_monitoring_submission/ARTIFACT/registrations/`. Amendments, if any, are appended as dated sections below the marker line and never edit the text above. The run proceeds on the author's freeze commit; nothing runs before it exists.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
