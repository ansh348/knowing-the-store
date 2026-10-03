# ADDENDUM_R122_GATE_REACH: what the gate buys, reach only (T5)

Registration of program R122 (the no-human batch; the author's brief of 2026-09-19), written BEFORE any scoring. Offline, 0 USD: no model call, no embedding call, no answer-stage call, and none of its measures uses the stale-answer detector. Carries three predictions (P-G1, P-G2, P-G3) with failure texts; held texts for both branches. Frozen by the sha256 of the bytes above the marker line, recorded in `reviews/r122/FREEZE_R122.md`; the scorer asserts it at start. Lives under `reviews/r122/registrations/` by the brief's fence.

## §1: Why

Section 8 reads the gated fetch against retrieval alone at a matched budget: the MODEL rule reaches 0.82 of the 104 obligations at a mean view of about seven records on the 104, where a seven-record retrieval view reaches 0.60. Two things that comparison does not separate are the gate and the fetch: a fetch keyed on the name the lookup matches best, with no gate at all, may reach as much at more lines; and a retrieval that keeps only the newest record per attribute, the store a recency-only memory would hold, may reach far less at the same lines. Three policies, each matched to the MODEL rule's mean view over the full population, put those on the same scale, with reach and cost only.

## §2: Population and the recorded artifacts (read, never re-run)

The 661 obligation items (`ds_common.load_cell`: 104 obligations with `pn_members`, 174 licensed items with `gold`, 383 absent; 40 personas), the recorded L2 ranking (`resp_review/l2/retrieval.json`: per item the ten ids and cosines of `LifecycleBank.cosine_search_all` over the item's store variant with no lifecycle mask, and the five-line block), the pinned question vectors (`l2/question_emb.npz`), the recorded DS views and rates (`ds_downstream/views.json`, `policies.json`, `stage1.json`). The MODEL rule's recorded rows: reach **85 of 104** (0.8173; AUX-DS-REACH), licensed record in view **65 of 174** (AUX-DS-PRESENT), mean view **5.4342** lines over the 661 and 7.0769 over the 104 (AUX-DS-VIEWSIZE), each recomputed from `views.json` ids and asserted. Reused recorded rows: reach of the forbidding record by ranking depth, k = 5 … 10 = 54, 60, 62, 69, 70, 74 of 104 (AUX-R104-REACH), and the licensed record in view by depth, 65, 72, 77, 82, 88, 89 of 174 (Amendment 6, `scores_amend6.json` `lock.counts.inview`): TAGGED-k reproduces both, asserted, so **TAGGED-7's rows are the recorded 62 / 104 and 77 / 174**.

Locks, asserted before scoring: TAGGED-5's rendering equals the recorded ALWAYS view byte for byte on all 661 (Amendment 6's renderer lock); the ranking re-derived from the pinned vectors through the recorded retriever function has the recorded ten ids first on all 661; the DS lookup gate (NB-6 0.7484 on the 661, NB-5 0.6186 on the 307) passes.

## §3: The policies (every choice fixed here; the pipeline's functions unchanged)

- **ALWAYS-FETCH (AF).** The lifecycle fetch `ds_common.fetch` with its gate always open on every one of the 661, keyed on **one** attribute: of the names in the item's v2 superseded-names list (`ds_common.names_for`, the set N2 the MODEL rule fetches over), the one the name lookup matches best, the maximum cosine of the question to the name under `all-MiniLM-L6-v2` (the NB-6 estimator, `run_baselines.encoder`, underscores replaced by spaces); ties go to the first name in sorted order; an item whose list is empty fetches nothing. The fetched records are every non-active entry of the store variant under that slot, appended to the similarity fill by `ds_common.assemble_view` with ranks continuing (the recorded view rule). The similarity fill is the first k of the item's five recorded lines, k = 0 … 5; **AF-5 is the unmatched policy** (five lines plus the fetch).
- **TAGGED-k.** Similarity retrieval at k lines from the recorded ten-deep ranking with the lifecycle mask off and the tags printed (`resp_common.render_line`), k = 5 … 10 (Amendment 6's FLAT-k); **TAGGED-7 is the policy named**, its rows reused as §2 states.
- **RECENCY-k.** The same ranking, re-derived over the full store variant (`build_l2.bank_for` and `cosine_search_all` with k = the variant's size, the pinned question vector), keeping only the newest record per attribute: an entry is eligible iff it has the smallest age among the variant's entries sharing its scrubbed slot (`true_flags` `slot` and `age`, the days before the persona's pinned now); ties at the smallest age are all kept; entries with no slot are kept; a slot whose entries all lack an age keeps them all. The first k eligible in cosine order, k = 5 … 10; **RECENCY-7 is the policy named**.

Scorer `reviews/r122/tools/gate_reach.py` (`check` locks; `run` everything), hashed in the freeze record.

## §4: Measures, the budget match, the estimands

Per policy and truncation: **reach** on the 104 (a `pn_members` entry among the view's ids; the stage-1 rule), with Wilson 95% and per state; **lines per question** over the 661 (mean, max; and the mean over the 104 beside); **the licensed record in view** on the 174 (a `gold` entry among the ids). Paired differences against the MODEL rule's recorded per-item rows, item-level and persona-grouped percentile bootstraps (`build_ds.boot_prop_diff`, 1,000 draws, seed 42).

**The budget match (the rule; decision D-R122-2, recorded here).** The brief matches each policy to the MODEL rule's mean view by truncating the similarity fill, and integer truncations cannot hit 5.4342. The nearest recorded precedent is Amendment 6's rule (§A6.4): the value at a non-integer depth is the linear interpolation of the integer curve between the bracketing depths. So per policy family the two integer truncations whose mean lines over the 661 bracket **5.4342** are found, the weight on the upper one is fixed from those full-population means, and the matched rate of each measure is the same interpolation of the two integer rows; its intervals resample the items once per draw, compute both integer rows and the MODEL row on the resample, interpolate with the fixed weight and difference (item-level; persona-grouped). The achieved mean is 5.4342 by construction; the bracketing integer means are reported. Beside, descriptive: the same match at the MODEL rule's mean over the 104 obligations, 7.0769 (Section 8's basis). A family whose curve does not bracket a target prints its curve and no matched row.

## §5: Predictions (read on the matched rows at 5.4342)

- **P-G1.** ALWAYS-FETCH's matched reach is within 0.05 of the MODEL rule's 0.8173 at the point estimate; both intervals of the difference are printed and do not decide.
- **P-G2.** ALWAYS-FETCH before matching (AF-5) spends more lines per question over the 661 than the MODEL rule: mean(AF-5) > 5.4342; the ratio mean(AF-5) / 5.4342 is reported.
- **P-G3.** RECENCY's matched reach is below the MODEL rule's by more than 0.05: 0.8173 − reach(RECENCY, matched) > 0.05 at the point estimate; both intervals printed. The unmatched RECENCY-7 row prints beside.

Failure texts, frozen: "P-G1 FAILS: the ungated fetch keyed on the best-matched name reaches $R$ at the MODEL rule's mean view against its $0.8173$, a difference of $D$ with intervals $I_{item}$ and $I_{persona}$." / "P-G2 FAILS: the ungated fetch spends $L$ lines per question against the MODEL rule's $5.43$, ratio $r$." / "P-G3 FAILS: a retrieval over the newest record per attribute reaches $R$ at the MODEL rule's mean view, within $0.05$ of its $0.8173$ (difference $D$, intervals $I_{item}$ and $I_{persona}$)."

## §6: Held texts, both branches (land only by the author's ruling)

- All three hold: Section 8, one sentence after "The lookup rule reaches the same $0.82$ and the oracle $0.95$": "The gate itself buys little reach: a fetch keyed on the best-matched name with no gate reaches $R_{AF}$ at the same mean view, spending $r$ times the lines before matching, while a retrieval over the newest record per attribute reaches $R_{REC}$ (Appendix E.10)." One table `tab:gate-reach` in Appendix E.10: MODEL (recorded), ALWAYS-FETCH (unmatched and matched), TAGGED-7 (recorded) and its matched row, RECENCY-7 and its matched row; columns reach with Wilson and per state, minus MODEL with both intervals, licensed record in view, mean lines over the 661 and over the 104.
- P-G1 fails (the ungated fetch reaches less at the matched view): the sentence reads "The gate buys reach at the matched view: a fetch keyed on the best-matched name with no gate reaches $R_{AF}$ against the rule's $0.82$ at the same mean view (Appendix E.10)."; P-G2 fails: the sentence drops the cost clause and the appendix states the ratio; P-G3 fails: the recency clause reads "and a retrieval over the newest record per attribute reaches $R_{REC}$, within $0.05$ of the rule", and Section 8's reading that the fetch reaches records retrieval does not is re-read by ruling. The table prints in every branch; nothing lands by this registration.

## §7: Order, ledger

No call. Order: freeze → `gate_reach.py check` (locks) → `gate_reach.py run` → `reviews/r122/results/gate_reach.json` → ledger `reviews/r122/NUMBERS_R122.md` section T5 (`AUX-R122-GATE-LOCK`, `-GATE-ROWS`, `-GATE-MATCHED`, `-GATE-MATCHED-104`, `-GATE-PREDICTIONS`). STOP on a lock or gate mismatch or on a reused recorded row that does not reproduce.

## Registration mechanics

Frozen by sha256 before the first scoring, in one commit with the other R122 registrations (`FREEZE_R122.md`). Amendments, if any, are appended as dated sections below the marker line and never edit the text above.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
