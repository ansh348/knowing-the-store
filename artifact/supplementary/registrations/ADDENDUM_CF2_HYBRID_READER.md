# ADDENDUM_CF2_HYBRID_READER: a no-model hybrid reader on the counterfactual set (E10)

FROZEN 2026-09-19 by the author's ruling E1 on REPORT_R124 (program R124, the main session; drafted by program R120 as item l, 2026-09-19, no call made). The reader makes **no generative-model call**; its only model is the sentence-embedding matcher the name lookup already uses (`score_cf.matcher`, all-MiniLM-L6-v2, local). Carries two predictions (P-H1, P-H2) with failure texts, both branches' held texts, and no budget (0 USD). The scorer `r82_counterfactual/tools/cf2_hybrid.py` was written before this freeze and is hashed in `reviews/v21/FREEZE_E10.md` beside this file's sha256; the ledger section is `cf2/NUMBERS_CF2.md` section 14e (the registration's 'section 14'). The text below this paragraph is the R120 draft unchanged.

## §1: Why

The name lookup reads the superseded-names list (0.7663 on the whole set; supersession 0.9223, retraction and expiry 0.5000). The category-guessing count reader reads the non-active share of the category the question's text names (0.6623; retraction 0.6669, expiry 0.6872). The two carry different states: the list the named state, the share the counted states. Whether a fixed combination of the two, with no generative model, reaches the models on the whole set says how much of the three top models' margin over the lookup (Opus 5, GPT-5.6 Sol and GPT-5.6 Luna, $+0.07$ to $+0.08$, on the counted states; R118-5) a reader of the summary's two parts can reach without them.

## §2: Population and the recorded rows

The 444 store versions in 148 triples (`r82_counterfactual/cf2/cf_cell.json`), the superseded-only summary v2 of each (`cf_indexes.json`, `v2`), the recorded label `y_nok` and persona. Never subset. Recorded rows read, never re-run: the embedding name lookup on the v2 lists (AUX-CF2-NB6-V2, gate 0.7663; `cf2_reader_score.lookup_v2`), the category-guessing count reader (CR-nb1, `reviews/v18/tools/a1_count_readers.py` `reader_scores`, AUX-R110-A1-CR 0.6623; the category from `index_features.assign_category` on the question text, 341 of 444 items assigned), and every model row of Table 1 (mini k = 1, Haiku 4.5, Opus 5, Sol, Luna at k = 5 under the X4 collapse) for the comparisons.

## §3: The reader (registered; every choice fixed here)

Features per item: $f_1$ = the name lookup's score (the cosine similarity of the question to the superseded-names list, as `lookup_v2` computes it); $f_2$ = the category-guessing share (CR-nb1's quantity, 0 when no category is assigned); $f_3$ = an indicator that a category was assigned. Model: logistic regression of `y_nok` on $(1, f_1, f_2, f_3)$, `sklearn.linear_model.LogisticRegression(C=1.0, penalty="l2", solver="lbfgs", max_iter=1000)` on standardized $f_1, f_2$ (mean and standard deviation of the training fold). **Leave-persona-out:** for each of the 40 personas the fit uses the other personas' items and scores the held-out persona's items; the out-of-fold scores of all 444 items form the reader's vector. No other hyperparameter, no feature beyond the three, no second fit. The scorer is `r82_counterfactual/tools/cf2_hybrid.py` (to be written before the freeze and hashed in it): it asserts the lookup gate 0.7663 and CR-nb1's 0.6623 before fitting, and writes `cf2/results/cf_scores_hybrid.json`.

## §4: Estimands

The CF-2 conventions: the reader's AUROC on the whole set and per state (within the state's items) with the persona-grouped interval; the paired difference against the name lookup, against the category-guessing reader and against each of the five models, item-level and persona-grouped bootstrap (1,000 draws, seed 42, `cf2_score.paired`); PN versus PRESENT and W/T/L (the post-hoc block's definitions); the fitted coefficients per fold, reported with their range. Every reader of Table 1 prints beside it in Appendix C.2.

## §5: Predictions

- **P-H1.** The hybrid reader exceeds the name lookup on the whole set, reliably: both intervals exclude zero.
- **P-H2.** The hybrid reader does not reach GPT-5.6 Sol: Sol minus the hybrid is positive with both intervals excluding zero.

Failure texts, frozen at the freeze: "P-H1 FAILS: the hybrid reads $A$ against the lookup's 0.7663, difference $D$ with intervals $I_{item}$ and $I_{persona}$." / "P-H2 FAILS: GPT-5.6 Sol minus the hybrid is $D$ with intervals $I_{item}$ and $I_{persona}$, not reliably positive."

## §6: Held texts, both branches (land only by ruling)

- Both hold: one Section 5 sentence after the count-reader sentences: "A fixed combination of the two, the name similarity and the guessed category's share fitted under leave-persona-out, reads $A$, above the lookup by $D$ and below GPT-5.6 Sol (Appendix C.2)."; the row in `tab:cf-main` under "Readers with no model in them"; the C.2 table.
- P-H1 fails: the sentence says the combination does not exceed the lookup, with the number; P-H2 fails: the sentence says the combination reaches the best model, with the number, and the reader claim of Section 1 is re-read by ruling. In every branch the C.2 table prints.

## §7: Budget, order, STOP

No call; the embedding matcher runs locally. Order: the scorer written and hashed → freeze (with E6, E7, E8) → run → ledger `cf2/NUMBERS_CF2.md` section 14 (`AUX-CF2-HYB-LOCK`, `-HYB-WHOLE`, `-HYB-PERSTATE`, `-HYB-VS-*`, `-HYB-COEF`, `-HYB-P-H1`, `-HYB-P-H2`). STOP on a gate mismatch (0.7663, 0.6623) before fitting.

## §8: The companion body sentence (item l, second part; lands by ruling, not by this registration)

Where Section 5 discusses the all-states summary ("The same lookup over a list naming all three non-active states scores $0.88$ on the whole set, and Haiku 4.5 gains a reliable $+0.30$ on the two counted states once they are named."), print Opus 5's margin over that lookup: "Opus 5 exceeds that lookup by a reliable $+0.03$ (Appendix C.2)." (AUX-R103-MARGIN / reviews/NUMBERS_R104.md: Opus 5 v3 0.9079 minus the all-states embedding lookup 0.8756 = $+0.0323$, intervals $[+0.0060, +0.0617]$ and $[+0.0077, +0.0608]$, both excluding zero; Haiku 4.5's $+0.0017$ is within tolerance.) The paper prints body numbers at two decimals; the three-decimal form $+0.032$ is available if the author wants it there.
