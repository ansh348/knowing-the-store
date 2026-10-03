# ADDENDUM_R122_ENCODERS: the name lookup under two further sentence encoders, and a random-token control (T1)

Registration of program R122 (the no-human batch; the author's brief of 2026-09-19), written BEFORE any scoring. Offline, 0 USD, no model call of any kind. Carries one prediction (P-E1) with a failure text and one descriptive row (the random-token control); held texts for both branches. Frozen by the sha256 of the bytes above the marker line, recorded in `reviews/r122/FREEZE_R122.md`; the scorer asserts it at start. This file lives under `reviews/r122/registrations/` because the brief fences this session to `reviews/r122/`; the main session copies it to `registrations/` at landing if the author so rules.

## §1: Why

The name lookup, the no-model baseline every model is measured against, scores a question by its maximum cosine similarity to the summary's superseded-names list under one sentence encoder, `all-MiniLM-L6-v2` (Section 5; Appendix C.2). Whether the baseline's level is a property of that encoder or of the list is untested. Two further encoders of different families and sizes, run through the same lookup code on the same items, say how much of the lookup's 0.7663 (444, v2), 0.8756 (444, v3) and 0.7484 (661) is the list. A control that replaces every attribute name by a stable random token, keeping the list's length and the question fixed, says what the lookup reads when the names carry nothing.

## §2: Populations and the recorded rows (read, never re-run)

- The counterfactual set: 444 store versions in 148 triples (`r82_counterfactual/cf2/cf_cell.json`), label `y_nok`, persona, state; the superseded-names list of the v2 summary and the all-states list (superseded ∪ retracted ∪ expired sections) of the v3 summary, read from the emitted texts by `index_v3.named_sections` as `cf2_score.py` reads them. Recorded MiniLM rows: AUX-CF2-NB6-V2 **0.7663** (supersession 0.9223, retraction 0.5000, expiry 0.5000); AUX-CF2-ALLSTATES-V3 **0.8756** (0.8995 / 0.7975 / 0.8711).
- The 661 obligation questions (R-NOK-FRB, TRUE summary), joined as `run_nb6.build` joins them, 104 positives, 40 personas; the superseded section of the committed TRUE index. Recorded MiniLM row: AUX-E1R-NB6 **0.7484** (the committed form, in which an empty section's marker `(none)` is encoded as the list's one name); the marker-free form 0.7442 (AUX-NB6SWEEP-DECOMP-661) printed beside.

Gate, asserted before any other encoder is loaded: the MiniLM rows reproduce at four decimals (0.7663, 0.8756, 0.7484, 0.7442), else STOP.

## §3: The lookup, unchanged; the encoders; the control

The lookup code is the committed one: `score_cf.matcher` on the 444 (max cosine of the question against each name, underscores replaced by spaces, embeddings normalized) and `run_nb6.emb_scores` on the 661 (the same estimator through `run_baselines.encoder`). Only the encoder object behind those functions is swapped (`score_cf._ENC["m"]`, `run_baselines._ENC["m"]`); **no query instruction or prefix is added for any encoder**, so an encoder trained with one is scored as the lookup scores MiniLM. Encoders, in the brief's order: `sentence-transformers/all-mpnet-base-v2` (768-d) and `BAAI/bge-small-en-v1.5` (384-d); if one cannot be loaded, the next of the fixed list `intfloat/e5-small-v2`, `sentence-transformers/all-MiniLM-L12-v2` takes its place and the substitution is recorded in the results file and the ledger. Both were downloaded before this registration (a model download, not a model call) and load offline; the scorer records what loaded.

The random-token control: every distinct attribute name across the three list families is mapped once to a pseudo-word of eight lowercase letters drawn from a generator seeded by sha256 of the name with seed 42 (`enc_lookup.random_token`), the same token for the same name everywhere, no two names sharing a token (asserted); each list keeps its length and order with names replaced by their tokens; the lookup runs on the token lists under each encoder. Descriptive.

Scorer `reviews/r122/tools/enc_lookup.py` (`check` gates; `run` everything), hashed in the freeze record.

## §4: Estimands

Per encoder and population: the lookup's AUROC on the whole set, the item-level 95% percentile interval (1,000 item draws, seed 42, single-class draws discarded) and the persona-grouped interval (`common_e1r.boot_cluster_single`); the paired difference encoder minus MiniLM with both intervals (`cf2_score.paired`: item-level `boot_item`, persona-grouped `boot_cluster`, 1,000 draws, seed 42); on the 444 the per-state AUROCs and paired differences; the count of distinct score values. The random-token rows in the same shape, and their difference from the same encoder's name row at the point.

## §5: Prediction

- **P-E1.** Both encoders are within 0.05 of MiniLM on the whole counterfactual set under the default summary v2: |AUROC(encoder, v2) − 0.7663| ≤ 0.05 at the point estimate for each of the two encoders scored (the substitutes count if a substitution was recorded); both intervals of the difference are printed and do not decide. HOLDS iff both encoders satisfy it. The v3 and 661 rows and the random-token rows are descriptive.

Failure text, frozen: "P-E1 FAILS: `<encoder>` reads $A$ on the whole counterfactual set against MiniLM's 0.7663, difference $D$ with intervals $I_{item}$ and $I_{persona}$; the lookup's level depends on the encoder."

## §6: Held texts, both branches (land only by the author's ruling)

- P-E1 holds: Appendix C.2, after the sentence naming `all-MiniLM-L6-v2`: "Two further encoders, `all-mpnet-base-v2` and `bge-small-en-v1.5`, score the same lookup at $A_1$ and $A_2$ on the counterfactual set, within $0.05$ of MiniLM; replacing every name by a random token scores $A_r$ (Table~\ref{tab:enc-lookup})." One table `tab:enc-lookup` in Appendix C.2: rows MiniLM (recorded), the two encoders, the random-token control; columns the 444 under v2 and v3 and the 661, each with the persona-grouped interval and the difference from MiniLM with both intervals. No body sentence changes; Section 5's "under the sentence encoder `all-MiniLM-L6-v2`" stands.
- P-E1 fails: the same appendix sentence states the encoder and the number ("`<encoder>` scores the lookup at $A$, $D$ from MiniLM"); Limitations gains one clause on the sentence naming the lookup, "and the lookup's level moves by $D$ under a second encoder"; the table prints in every branch.

## §7: Order, ledger

No call. Order: freeze → `enc_lookup.py check` (gates) → `enc_lookup.py run` → `reviews/r122/results/enc_lookup.json` → ledger `reviews/r122/NUMBERS_R122.md` section T1 (`AUX-R122-ENC-LOCK`, `-ENC-ROWS`, `-ENC-RANDOM`, `-ENC-P-E1`). STOP on a gate mismatch. Nothing lands in the paper by this registration.

## Registration mechanics

Frozen by sha256 before the first scoring, in one commit with the other R122 registrations (`FREEZE_R122.md`). Amendments, if any, are appended as dated sections below the marker line and never edit the text above.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->
