

---

## D-R82-3 — D-R82-2 read one branch of the write path and missed the one that runs before it

**What happened.** D-R82-2 concluded that nine of ten retraction pairs leave the cancelled
plan active, reasoning from the cosine branch at `lifecycle_bank.py:781-784`. It did not
account for `:766-777`, which runs first: an entry sharing an active entry's `slot_key` at
sufficient confidence sets `supersedes` and deactivates that entry, whatever the cosine.

**What changed.** The claim is withdrawn. Measured on the committed banks, all 31
`is_retracted` entries carry a `slot_key`, 22 share it with another entry, and 16 of those
carry a `supersedes` pointer, so the slot branch is what deactivates in practice. The
construction gives the retracting entry the same `slot_key`, matching both the observed
corpus and the extraction rule stated at `:604`. Registered as Amendment 2.

**Why this is admissible.** It is a correction of my own error, made before any store
version, label or score existed, and it moves against the more striking claim rather than
toward it. The replacement finding is weaker and better supported.

**Disposition.** What survives: at the store level a retraction is recorded through the same
mechanism as a supersession, so the two are not distinguishable in the store's own metadata,
and the retraction-specific cosine rule is largely redundant. That belongs to the BELIEVED
account rather than to this cell, which runs TRUE only. The withdrawn claim is not repeated
anywhere.

---

## D-R82-4 — the second clause of the frozen CF-1 failure text does not describe the outcome, and is struck

**What happened.** CF-1 failed as registered. The smallest model's v2 obligation judgment
reached 0.5939 against a blind 0.5000, and the preregistered item-level interval
[-0.0345,+0.2315] includes chance while the question-clustered interval [+0.0325,+0.1625]
excludes it. Mixed, so the weaker reading governs and the verdict is FAILS.

The frozen failure text has two clauses. The first describes the outcome. The second asserts
that the gain measured on the larger population is therefore not free of what the question
alone gives away. **A positive point estimate whose primary interval includes chance at n=90
is an underpowered null.** It cannot establish contamination on another population, and the
clustered interval excluding chance points the other way.

**What changed.** The verdict stands and prints as FAILS. The first clause prints. The second
clause is **struck as defective** and does not print. The landed text adds one sentence
recording that at this size the cell can neither establish the aggregate effect nor establish
contamination, with the point estimate and both intervals printed.

**Why this is admissible.** This follows **D93** (`e1xv_crossvendor/DEVIATIONS_E1XV.md:238`),
which records two clauses of a frozen FAILS text that did not describe the outcome, and
states the handling: not a departure from the protocol, a defect in the registered prose,
reported rather than reworded. The gate and its verdict are untouched and only the
explanation attached to them is corrected. No third reading is written, because the
registered verdict is unchanged.

**The design error is recorded against the prompt rather than the build.** CF-1 was registered
on aggregate v2 NOK over a cell where twenty of the thirty obligations are states the v2 index
only counts. The paper's own mechanism predicts those twenty sit near chance under v2, so only
a third of the positives could move the aggregate, and the test was low-powered by
construction. The per-state block confirms it: under v2 supersession runs 0.6550 to 0.8275
across the three lanes while the counted states run 0.5225 to 0.6225. What CF-1 was built to
find is in those rows, and they print as the registered descriptive block.

**Disposition.** Opus 5, descriptive and carrying no prediction, reaches 0.7122 under v2 with
an item-level interval [+0.0683,+0.3567] excluding chance, so the aggregate effect is
establishable on this cell at this size by a stronger lane. That is recorded beside the CF-1
block and alters no verdict.

---

## D-R82-5 — the registered AUROC-invariance assertion tested the wrong object under cross-validation

**What happened.** `ADDENDUM_R82` §18 registered that AUROC is unchanged by a monotone map,
required agreement to four decimals, and made a disagreement a STOP. Run as written it stopped
on its first arm: the pooled out-of-fold AUROC on the blind arm of `P-NOK-FRB` moved from
0.4946 to 0.2572 under Platt.

**Diagnosis.** The assertion is true of a single monotone map applied to every item. Under
leave-one-persona-out cross-validation each of the 40 folds fits its **own** map, so the
pooled out-of-fold vector is a mixture of 40 maps rather than one transform of the score, and
its AUROC has no reason to match. The blind arm makes this visible because its raw AUROC is
0.4946, close enough to chance that a logistic fit can take a negative slope in some folds
and invert the ordering there.

**What changed.** Monotonicity is asserted **per fitted map** on the observed score grid: a
fold whose map is neither non-decreasing nor non-increasing is a STOP. The pooled out-of-fold
AUROC prints as a diagnostic beside the raw AUROC and is no longer asserted equal to it.
Amended into §18.

**Why this is admissible.** It corrects a method statement before any registered reading was
evaluated, and it makes the check test the property §18 names rather than a consequence that
does not follow under cross-validation. Neither CAL-1 nor CAL-2 involves the blind arm, and
neither reading changed.

---

## D-R82-6 — the v3 leakage screen was reserved, never run, and never ledgered; the deterministic half ran at R96 without a model call

**What happened.** `ADDENDUM_R82` §5 registered that the existing leakage screen (`ladder_e1.py`,
30 items, threshold 3, seed 42) runs on a sample of the 90 v3 indexes and must return at most 3
of 30 correct, and §9 reserved `AUX-R82-CF-LEAKSCREEN`. No artifact was written under
`results/`, no ledger row was written, and the cell was scored (`be64244`, `7e9ac39`) without
the screen having run. Found by the CF-2 scope pass (reviews/CF2_SCOPE.md finding 4) on
2026-09-12 and acted on under R96-4c.

**What the registered instrument is.** `ladder_e1.py` is deterministic in its SCORING
(`exp4_witnesses.supports_correct`, no judge) and not in its ANSWERS: each item is one
`api.call` under the frozen LEAKAGE prompt, asking `gpt-4.1-mini` to answer the question from
the index alone. The R96 program instruction reads the screen as deterministic and runs under a
no-model-call rule.

**What changed.** The deterministic half ran, retroactively, over every one of the 90 v3
indexes and the 90 v2 indexes beside them: the registered scorer applied to the index text
itself, `supports_correct(index_text, entry_text)`, with the pair's `entry_text` as gold because
the drafted questions carry no `correct_answer` field (`tools/leakscreen_v3.py`;
`results/leakscreen_v3.json`; ledgered as `NUMBERS_R82.md` §12). The registered cell, PRESENT
under v3, scores 1 of 30, inside the threshold; the one hit is on attribute names that carry
the slot's topic words, the same item in all six version-by-arm cells, and the v3 sections add
no hit.

**What this does not close.** The model-mediated screen has not run. What it measures beyond the
deterministic half is whether a model, shown the index, produces the gold's tokens anyway,
which on this cell can only come from the question; the deterministic screen bounds the index
side and says nothing about that. Running it is 30 to 90 `gpt-4.1-mini` calls under the frozen
LEAKAGE prompt (`ladder_e1`'s `one()` with the CF indexes and `entry_text` as gold), under a
separate authorization. Until then this key carries the deterministic result and this entry.

**Why this is admissible.** It is a disclosure of an omission and a partial, deterministic
repair made after every score existed; it changes no score, no verdict and no printed number,
and it moves against the paper if anything, by recording that a registered control did not run.

---

## D-R82-7 — two Opus 5 per-state values under v3 were computed at 7e9ac39 and never ledgered, so Table 9 printed dashes for computable cells

**What happened.** `results/cf_scores.json` has carried
`lanes/claude-opus-5/v3/per_state/SUPERSESSION/indexed` = 0.835 and
`.../RETRACTION/indexed` = 0.73 since `7e9ac39`, computed by the same scorer pass that produced
the expiry value 0.945 which §10 ledgers. §9 and §10 named only the expiry value, so the R86 table
transcription (Table 9, "every value is transcribed from NUMBERS_R82.md sections 6 to 10")
printed a dash for the two cells under the caption's "never scored" wording. The values were
scored; they were unledgered. Found by the CF-2 scope pass (reviews/CF2_SCOPE.md finding 6).

**What changed.** §9 gains the Opus 5 per-state table (v2 and v3), §10's v3 sentence names all
three Opus values, and Table 9's two dashes become $0.8350$ and $0.7300$ under the R96 block
(entry 4d); the caption's dash sentence now describes the dashes that remain (matcher cells).
`verify_r82.py` checks both against the artifact by key name.

**Why this is admissible.** Transcription of two committed values into the ledger and the table
that reads it; nothing is recomputed, no verdict or reading changes, and the per-state boundary
the section states was already stated on the v2 row.
