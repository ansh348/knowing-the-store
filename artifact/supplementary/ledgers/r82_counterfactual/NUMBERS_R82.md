# NUMBERS_R82.md — the R82 ledger

Every number R82 prints resolves to a key here, and `tools/verify_r82.py` checks the ledger
against the committed artifacts. Registration of record: `registrations/ADDENDUM_R82.md`.

**Restored 2026-09-12 (R96-4a).** Commit `be64244` (R82-CF-1c) wrote this file from §6 onward and
dropped the title, this header and §1 to §5; HEAD and the shipped `ARTIFACT/ledgers` copy began at
§6 until R96 (reviews/CF2_SCOPE.md finding 3). The title, the two lines above and §1 to §5 are
restored verbatim from `4c3a516` (`git show 4c3a516:r82_counterfactual/NUMBERS_R82.md`). The
`4c3a516` header's paragraph saying nothing below is a result is not restored, because §6 to §11
are the results. §5 is the `4c3a516` snapshot and carries a dated line with the completed lane
spends. `tools/verify_r82.py`, named above since `4c3a516` and absent until R96, now exists
(`R96-4b`). §12 (`AUX-R82-CF-LEAKSCREEN`, `R96-4c`) and the Opus 5 per-state table in §9
(`R96-4d`) were added at the same time; `DEVIATIONS_R82.md` D-R82-6 and D-R82-7 record why each
was missing.
One reading note on the restored text: §1's retraction-cosine "median 0.775" is the upper median
(`sorted(x)[n//2]` = 0.7747 over the ten `cosine_to_original` values in `cf_pn_texts.json`); the
mean-of-the-middle-two median is 0.757. `verify_r82.py` checks the figure under the convention it
was written with and prints the other. The value appears in no manuscript.

---

## 1. `AUX-R82-CF-CONSTRUCTION` — the cell as built

| Quantity | Value | Source |
|---|---|---|
| pairs | 30, one per persona over 30 distinct personas | `cf_pairs.json` |
| per state | 10 supersession, 10 retraction, 10 expiry | `cf_pairs.json` |
| store versions | 90, three per pair | `cf_cell.json` |
| labels | 30 PRESENT, 30 ABSENT, 30 PRESENT-NEGATIVE, all matching intent | `cf_cell.json` |
| questions | 30, all distinct, all passing the intent gate | `cf_questions.json` |
| question substitutions | 2, both UPCOMING pairs whose seeded pick carried no forward marker | `cf_questions.json` |
| question redrafts | 0 | `cf_questions.json` |
| drafting prompt sha256 | `b748247b3ff380d8c24a3e142e2c37c12718942438c3a96cce476531692a8c7f` | `cf_questions.json` |
| questions sha256 | `adec4c831571e409130d5c38282d0f3a56124e659506803c216857f430e9c035` | `cf_questions.json` |
| PN records authored | 20, plus 10 expiry anchors requiring no text | `cf_pn_texts.json` |
| PN authoring retries | 0 | `cf_pn_texts.json` |
| supersession detector signal on the original | 1.0 on all 10 | `cf_pn_texts.json` |
| retraction cosine to original | min 0.551, median 0.775, max 0.867; 1 of 10 above the 0.85 branch | `cf_pn_texts.json` |
| indexes | 90 versions by 2 arms, sha256 `cdb2a74827ce054503efe172420ea57f` | `cf_indexes.json` |

## 2. `AUX-R82-CF-ADJUDICATION` — eligibility, and what the corpus carries

| Class | Adjudicated | Eligible | Rate | Coverage |
|---|---:|---:|---:|---|
| Expiry | 46 | 34 | **0.7391** | exhaustive over the pool |
| Retraction | 62 | 11 | **0.1774** | every drawn candidate, seed-ordered walk |
| Supersession | 13 | 10 | **0.7692** | every drawn candidate |

**The retraction rate is a fact about the corpus.** One candidate in six in
`PROJECTS_ENDEAVORS` is a cancellable plan; the rest are standing practices, completed
history and third-party facts. This is the same reason the main population carries only 26
retraction obligations of 104.

Descriptive, never used for selection: a forward-looking plan-marker pre-filter over the
adjudicated retraction set scores precision **1.000** (6 of 6) and recall **0.545** (6 of
11), missing the "is considering", "wants to", "is writing" and "is preparing" forms.

## 3. `AUX-R82-CF-INDIVIDUATION` — what the scrubbing rule lets the index name

Computed on the constructed indexes before any monitor ran (`ADDENDUM_R82` §16). A pair
individuates when its scrubbed slot name is absent from its own state's v3 section in
PRESENT and present in PN.

| Class | Individuates | Scrubber collisions |
|---|---:|---:|
| Retraction | **6 of 10** | 4 |
| Expiry | **9 of 10** | 1 |
| Pooled counted-state scored | **15 of 20** | 5 |

Retraction individuation is at or above six, so CF-3 remains the pooled counted-state
prediction, scored on 15, with the 5 collisions reported descriptively.

## 4. `AUX-R82-CF-INDEXSIZE` — index size, and why the projection moved

Recorded because the paper's caching arithmetic (`ECONOMICS.md` §3) rests on a 1,201-token
figure and October will need the real one.

**Index text alone**, `tiktoken` `o200k_base`, over all 90 store versions:

| Arm | mean | median | min | max |
|---|---:|---:|---:|---:|
| v2 | **1074** | 1082 | 940 | 1156 |
| v3 | **1126** | 1134 | 987 | 1228 |

v2 renders at **63.2 lines** on average (58 to 67), above `index_v2`'s stated 40 to 60 design
target, because the cell uses 30 personas' FULL stores where E1's mean pools the smaller
ablated variants.

**Full prompt input tokens**, first item, each vendor's own tokenizer:

| Lane | blind | v2 | v3 |
|---|---:|---:|---:|
| `gpt-4.1-mini` | 482 | **1682** | 1738 |
| `claude-haiku-4-5-20251001` | 527 | 1777 | 1840 |
| `claude-opus-5` | 696 | 2475 | 2587 |

**The like-for-like comparison is mini against mini: 1,682 here against E1's committed
INDEXED-TRUE mean of 1,201, a factor of 1.40.** An earlier report of "about twice" was
wrong: it set Opus's 2,475 against E1's mini figure and so compared two tokenizers. The
factor that moved the projection is 1.40 on the shared lane, and the rest of the gap between
the $5.92 registered projection and the $10.63 measured one is Opus's pricing and output
length rather than index size.

At 1,074 tokens the index text clears the 1,024-token minimum cacheable prefix that
`ECONOMICS.md` §3 applies, so the caching argument carries to this cell.

## 5. `AUX-R82-CF-SPEND` — metered spend against the ceiling

| Item | Calls | USD |
|---|---:|---:|
| question drafting (`gpt-4.1-mini`) | 30 | 0.0060 |
| PN record authoring plus embeddings | 20 + 20 | 0.0034 |
| lane probes, three lanes | 9 | 0.0025 |
| `gpt-4.1-mini` lane, 210 of 210 OK, 0 parse failures | 210 | **0.1325** |
| `claude-haiku-4-5-20251001` batch, submitted | 1050 | in flight |
| `claude-opus-5` batch | 1050 | pending amendment |

Ceiling **$15** after Amendment 4 (`ADDENDUM_R82` §24); **$12** before it. Spend at the time
Opus was submitted: **$0.1444**.

**Completed lane spends (R96-4a, 2026-09-12).** The table above is the `4c3a516` snapshot, taken
while the Haiku batch was in flight and before Opus was submitted. The completed figures below are
summed from the committed rows' `usd` field (`rows/rows_H45.jsonl`, `rows/rows_OP5.jsonl`; the
mini row reproduces the table's 0.1325 from `rows/rows_MINI.jsonl` the same way) and agree with
the figures the `be64244` and `7e9ac39` commit messages record.

| Lane | Calls | OK | USD |
|---|---:|---:|---:|
| `gpt-4.1-mini` | 210 | 210 | 0.1325 |
| `claude-haiku-4-5-20251001` | 1050 | 1050 | **1.2641** |
| `claude-opus-5` | 1050 | 1050 | **8.6103** |

Metered total at the R82-CF-1d close: 10.0189 against the $15 ceiling (drafting 0.0060 + PN
authoring 0.0034 + probes 0.0025 + the three lanes), which is the "10.02 of the 15 ceiling" of
`7e9ac39`.

## 6. `AUX-R82-CF-NOK` — the counterfactual cell, NOK, n=90 with 30 positives

Blind is **0.5000 exactly on both lanes**, the identity registered in `ADDENDUM_R82` §6.
Item-level paired bootstrap is primary; question-clustered is printed beside it.

| Lane | Arm | Blind | Indexed | Delta | Item-level CI | Question-clustered CI |
|---|---|---:|---:|---:|---|---|
| `gpt-4.1-mini` | v2 | 0.5000 | **0.5939** | +0.0939 | [-0.0345,+0.2315] includes zero | [+0.0325,+0.1625] excludes zero |
| `gpt-4.1-mini` | v3 | 0.5000 | 0.6419 | +0.1419 | [+0.0126,+0.2668] excludes zero | [+0.0444,+0.2433] excludes zero |
| Haiku 4.5 | v2 | 0.5000 | 0.6406 | +0.1406 | [-0.0243,+0.2911] includes zero | [+0.0653,+0.2236] excludes zero |
| Haiku 4.5 | v3 | 0.5000 | 0.7656 | +0.2656 | [+0.1267,+0.4178] excludes zero | [+0.1800,+0.3536] excludes zero |

Per-state indexed AUROC, descriptive, ten positives each:

| Lane | Arm | Supersession | Retraction | Expiry |
|---|---|---:|---:|---:|
| `gpt-4.1-mini` | v2 | 0.6550 | 0.5700 | 0.5825 |
| `gpt-4.1-mini` | v3 | 0.6950 | 0.7500 | 0.4800 |
| Haiku 4.5 | v2 | 0.7825 | 0.6225 | 0.5225 |
| Haiku 4.5 | v3 | 0.7450 | 0.7375 | 0.8575 |

## 7. `AUX-R82-CF-COUNTED` — CF-3's population, Haiku 4.5, individuating pairs only

15 pairs, 45 items, 15 positives. v2 **0.5656** to v3
**0.8489**, paired delta **+0.2833**, item-level
[+0.0772,+0.4945] excluding zero,
question-clustered [+0.1509,+0.4311]
excluding zero.

## 8. `AUX-R82-CF-BASELINES` — matchers on the same 90

| Matcher | AUROC | Clustered CI |
|---|---:|---|
| Superseded-names, v2 | 0.6261 | [0.5567,0.7094] |
| All-states names, v3 | **0.7886** | [0.7013,0.8797] |
| Whole name map, v2 | 0.5347 | [0.5108,0.5670] |

**Adverse branch fires and prints.** The all-states matcher exceeds three monitor rows by
more than tolerance: `gpt-4.1-mini` v2 by +0.1947, `gpt-4.1-mini` v3 by +0.1467, and Haiku
4.5 v2 by +0.1480. It exceeds Haiku 4.5 v3 by +0.0230, inside tolerance. The superseded-names
matcher exceeds `gpt-4.1-mini` v2 by +0.0322, inside tolerance.

## 9. `AUX-R82-CF-OP5` — Opus 5, descriptive, carries no registered prediction

| Arm | Blind | Indexed | Delta | Item-level CI | Question-clustered CI |
|---|---:|---:|---:|---|---|
| v2 | 0.5000 | **0.7122** | +0.2122 | [+0.0683,+0.3567] excludes zero | [+0.1286,+0.3039] excludes zero |
| v3 | 0.5000 | 0.8172 | +0.3172 | [+0.1695,+0.4658] excludes zero | [+0.2372,+0.4022] excludes zero |

CF-3 population, 15 individuating pairs: v2 0.6122 to v3 0.9144, delta +0.3022,
question-clustered [+0.2166,+0.3678] excluding zero.

Per-state indexed AUROC, descriptive, ten positives each. The v2 row is the Opus line of §10; the
v3 row was computed at `7e9ac39` beside it and left unledgered until R96 (`R96-4d`, D-R82-7), so
Table 9 printed dashes for its supersession and retraction cells. Source:
`results/cf_scores.json` `lanes/claude-opus-5/{v2,v3}/per_state/*/indexed`.

| Arm | Supersession | Retraction | Expiry |
|---|---:|---:|---:|
| v2 | 0.8275 | 0.5975 | 0.6150 |
| v3 | **0.8350** | **0.7300** | 0.9450 |

**Opus 5 is the only lane whose v2 aggregate gain excludes chance at item level.** It is also
the lane with the strongest question priors, which is why it was run.

## 10. `AUX-R82-CF-PERSTATE-V2` — the naming boundary on a leak-free cell

Indexed NOK under v2, ten positives per state. The registered descriptive block.

| Lane | Supersession | Retraction | Expiry |
|---|---:|---:|---:|
| `gpt-4.1-mini` | 0.6550 | 0.5700 | 0.5825 |
| Haiku 4.5 | 0.7825 | 0.6225 | 0.5225 |
| Opus 5 | 0.8275 | 0.5975 | 0.6150 |

Supersession, the one state v2 names, runs 0.6550 to 0.8275. The two states v2 only counts
run 0.5225 to 0.6225. The boundary holds on all three lanes, on questions that cannot carry
the label.

Under v3, where all three states are named, the counted states move: retraction to 0.7375
and expiry to 0.8575 on Haiku 4.5, and expiry to 0.9450 on Opus 5. The full Opus 5 row under v3 is
supersession 0.8350, retraction 0.7300, expiry 0.9450 (§9; the first two ledgered at R96, D-R82-7).

## 11. `AUX-R82-CAL` — post-hoc calibration, leave-one-persona-out, 40 folds

`P-FOK-HARD`, n=588, 35 positives, base rate 0.0595.

| Arm | raw AUROC | distinct values | raw ECE | Platt ECE | Isotonic ECE | Temperature ECE |
|---|---:|---:|---:|---:|---:|---:|
| blind | 0.5258 | 6 | 0.1596 | 0.0001 | 0.0003 | 0.1222 |
| intact | 0.7530 | 12 | **0.1741** | 0.0029 | **0.0146** | 0.1299 |
| names-only | 0.8516 | 9 | 0.0583 | 0.0134 | 0.0340 | 0.0296 |

Selective risk on the intact arm: AURC 0.0615 raw, 0.0373 under Platt, 0.0454 under
isotonic; excess AURC 0.0538 raw, 0.0355 under Platt.

`P-NOK-FRB`, n=661, 104 positives, base rate 0.1573: indexed BELIEVED raw ECE 0.1411 falls to
0.0261 under isotonic.

**Floor, resolution, and the pooling diagnostic.** Three figures Appendix H prints had no row in
this section. `trace_scan_v13` surfaced them; each is recorded here with the artifact key that
backs it. `0.0560` matters most: under the v12 scan it passed only by coincidental set-match
against an unrelated clustered CI endpoint (`NUMBERS_E1R.md` retraction row) and against the
reliability diagram's observed frequency, neither of which is this quantity.

| Figure | Value | Artifact | JSON key |
|---|---:|---|---|
| Constant-predictor Brier at the base rate (the floor) | 0.0560 | `results/cal_floor.json` | `P-FOK-HARD.brier` |
| Rescaled Brier, intact arm, logistic map | 0.0519 | `results/cal_scores.json` | `P-FOK-HARD/intact.maps.platt.brier` |
| Pooled out-of-fold AUROC, question-only NOK arm | 0.2572 | `results/cal_scores.json` | `P-NOK-FRB/blind.maps.platt.auroc_pooled_oof` |

The third is the pooling diagnostic recorded under D-R82-5. It is a mixture statistic over forty
per-fold maps rather than a property of any one map, which is why the manuscript reports it beside
the raw 0.4946 and not in place of it.

**Crossing thresholds.** Under isotonic, the map CAL-1 names, the calibrated probability
reaches a maximum of 0.375 on the intact arm and 0.450 on names-only, so the 0.50 crossing is
**undefined on both**. At each population's own base rate the crossings are 0.3 and 0.2 in
raw-score space.

## 12. `AUX-R82-CF-LEAKSCREEN` — the v3 leakage screen, deterministic half, run retroactively (R96-4c, 2026-09-12)

Registered (`ADDENDUM_R82` §5): `ladder_e1.py`, 30 PRESENT items, seed 42, at most 3 of 30
answered correctly from the index alone. Not run at R82: §9 reserved this key and nothing wrote it
(D-R82-6). What ran at R96, **with no model call**: the registered scorer applied to the index
text itself, `exp4_witnesses.supports_correct(index_text, entry_text)`, over all 90 v3 indexes and
the 90 v2 indexes beside them (`tools/leakscreen_v3.py`; artifact `results/leakscreen_v3.json`;
`cf_indexes.json` content sha256 `cdb2a74827ce0545…`, file sha256
`deb9fc32699cf726…`). The gold is the pair's `entry_text`, the stored value the question
targets; the drafted questions carry no `correct_answer` field. The registered seed-42 sample of
30 PRESENT items is the whole PRESENT pool, so the sample is exhaustive.

| Version | Arm | n | Correct (leaks iff > 3) | Items sharing any gold token | Max coverage | Verdict |
|---|---|---:|---:|---:|---:|---|
| PRESENT (the registered cell) | v3 | 30 | **1** | 26 | 0.500 | PASS |
| PRESENT | v2 | 30 | 1 | 26 | 0.500 | PASS |
| ABSENT | v3 | 30 | 1 | 23 | 0.500 | PASS |
| ABSENT | v2 | 30 | 1 | 23 | 0.500 | PASS |
| PN | v3 | 30 | 1 | 27 | 0.500 | PASS |
| PN | v2 | 30 | 1 | 26 | 0.500 | PASS |

The one item scored correct is the same in all six cells, `cf:kenji:project:case_studies`: its entry text
"User is preparing case studies for freelance subcontractor work" shares `case`, `studies`, `work`
(3 of 6 content tokens) with attribute NAMES in the per-category name
map (`case_studies_count` under PROJECTS_ENDEAVORS, and the `work_*` names), which the v2 prefix
carries and v3 inherits. The index carries no value text; the hit is on attribute names that name
the slot's topic, the disclosure of `ADDENDUM_R82` §4 meeting the scorer's threshold on one item. The v3 sections (retracted and
expired names) add no hit: every count is identical between v2 and v3 within a version. The 26 of
30 PRESENT indexes sharing at least one gold token share topic words with attribute names for the
same reason.

**What this does and does not establish.** It bounds the index side: an index that does not carry
the gold's tokens at threshold cannot be read for them, whatever a model says. It does not run
the registered instrument, whose answers come from a model, and the model-mediated screen remains
to be run (D-R82-6: 30 to 90 `gpt-4.1-mini` calls under the frozen LEAKAGE prompt, `ladder_e1`'s
`one()` with the CF indexes and `entry_text` as gold).
