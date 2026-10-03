# NUMBERS_E1R — canonical ledger for the $0 robustness pass

Spec: `e1r_robustness/SPEC_E1R.md`, frozen at commit `9ac91a2` before any number below was
computed. Verifier: `e1r_robustness/tools/verify_e1r.py` (two-direction).
All AUROC and ECE estimators are transcribed from `e1_metamemory/tools/score_e1.py`.
Bootstrap: 1,000 draws, seed 42, paired arms, single-class draws discarded.

## 0. Reproduction gates (independent re-derivation of published values)

Every sensitivity below is gated on first re-deriving the published estimate from committed
artifacts. All three gates passed.

| Gate | Scope | Result |
|---|---|---|
| E1 calibration rows | n, blind, indexed, delta to 4 dp on 6 rows | **PASSED 6/6** |
| Matched-cell rows | n, blind, indexed, delta to 4 dp on 12 rows | **PASSED 12/12** |
| Calibration arms | ECE and AUROC to 4 dp on 5 arms | **PASSED 5/5** |

The item-level bootstrap intervals also re-derive: `R-FOK-HARD` `[+0.1177,+0.3504]`,
`R-FOK-FRB` `[+0.0935,+0.3191]`, `R-NOK-FRB` `[+0.1801,+0.2949]` reproduce the printed
endpoints exactly; `R-FOK-MEM0` `[-0.1686,-0.0250]` and `R-FOK-AMEM` `[-0.1726,-0.0403]`
reproduce the printed 3-dp roundings `[-0.169,-0.025]` and `[-0.173,-0.040]`.

## 1. `AUX-E1R-CLUSTER` — persona-clustered intervals, E1 calibration rows

Point estimates are unchanged; the primary endpoint remains the preregistered item-level
interval. n_pers = personas; +pers = personas carrying at least one positive.

| Row | n | pos | n_pers | +pers | Δ | item-level CI | **persona-clustered CI** | width ratio |
|---|---:|---:|---:|---:|---:|---|---|---:|
| R-FOK-HARD | 588 | 35 | 40 | 23 | +0.2272 | [+0.1177,+0.3504] | **[+0.1552,+0.2996]** | 0.62 |
| R-FOK-FRB | 307 | 35 | 40 | 23 | +0.2037 | [+0.0935,+0.3191] | **[+0.1259,+0.2767]** | 0.67 |
| R-FOK-EASY | 595 | 463 | 40 | 40 | +0.1914 | [+0.1179,+0.2596] | **[+0.1327,+0.2433]** | 0.78 |
| R-NOK-FRB | 661 | 104 | 40 | 28 | +0.2393 | [+0.1801,+0.2949] | **[+0.1552,+0.3237]** | 1.47 |
| R-FOK-MEM0 | 238 | 94 | 37 | 36 | −0.0969 | [−0.1686,−0.0250] | **[−0.1638,−0.0286]** | 0.94 |
| R-FOK-AMEM | 284 | 126 | 40 | 39 | −0.1065 | [−0.1726,−0.0403] | **[−0.1654,−0.0446]** | 0.91 |

**Every row's clustered interval excludes zero. The STOP condition did not fire on any E1
calibration row.** `R-FOK-EASY`'s item-level interval `[+0.1179,+0.2596]` is a new figure:
the manuscript currently prints no CI for that row.

## 2. `AUX-E1R-LOPO` — leave-one-persona-out

| Row | folds | Δ range | sign changes |
|---|---:|---|---:|
| R-FOK-HARD | 40 | [+0.2148, +0.2441] | **0** |
| R-FOK-FRB | 40 | [+0.1876, +0.2199] | **0** |
| R-FOK-EASY | 40 | [+0.1811, +0.2011] | **0** |
| R-NOK-FRB | 40 | [+0.2204, +0.2564] | **0** |
| R-FOK-MEM0 | 37 | [−0.1133, −0.0854] | **0** |
| R-FOK-AMEM | 40 | [−0.1180, −0.0977] | **0** |

No E1 calibration row depends on any single persona.

## 3. `AUX-E1R-ICC` — why clustering does not inflate these intervals

The clustered intervals came out *narrower* than the item-level intervals on four of six
rows, the opposite of the direction reviewer B2 assumed. Two independent checks confirm the
resampler:

| Row | cluster jackknife SE | clustered-bootstrap width ÷ jackknife width | ICC of paired contribution |
|---|---:|---:|---:|
| R-FOK-HARD | 0.0386 | 0.95 | +0.0129 |
| R-FOK-FRB | 0.0404 | 0.95 | −0.0238 |
| R-FOK-EASY | 0.0284 | 0.99 | +0.0870 |
| R-NOK-FRB | 0.0437 | 0.98 | +0.0769 |
| R-FOK-MEM0 | 0.0363 | 0.95 | −0.0340 |
| R-FOK-AMEM | 0.0311 | 0.99 | −0.0544 |

Two cluster-level variance estimators that share no machinery agree to within 5% on every
row. The measured intracluster correlation of the paired indexed−blind contribution lies in
**[−0.0544, +0.0870]** — effectively zero. With ρ ≈ 0 there is no variance for clustering to
inflate, and whole-persona resampling additionally preserves the balanced-by-persona item
construction that item-level resampling destroys.

**Pre-derived thresholds (frozen in the spec before computation).** The intracluster
correlation at which each interval would first touch zero: R-FOK-HARD **0.205**, R-FOK-FRB
**0.339**, R-NOK-FRB **1.055**, R-FOK-MEM0 **0.164**, R-FOK-AMEM **0.257**. The R-NOK-FRB
value exceeds 1 and is therefore unreachable by any correlation, as predicted in advance.
The other four thresholds were reachable in principle; the measured ρ simply came in near
zero.

## 4. `AUX-E1R-CLUSTER-CELL` — persona-clustered intervals, 84-item matched cell

33 personas. All 12 rows reproduce their published point estimates.

| Model | J | Δ | item-level CI | persona-clustered CI | LOPO sign changes |
|---|---|---:|---|---|---:|
| mini | FOK | +0.2602 | [+0.0851,+0.4213] | [+0.0913,+0.3912] | 0 |
| mini | NOK | +0.2139 | [+0.1242,+0.3070] | [+0.1093,+0.3245] | 0 |
| luna | FOK | +0.1682 | [+0.0340,+0.3033] | [+0.0367,+0.3001] | 0 |
| luna | NOK | +0.2940 | [+0.1696,+0.4172] | [+0.1984,+0.4051] | 0 |
| sol | FOK | +0.0364 | [−0.0930,+0.1600] | [−0.1095,+0.1609] | 0 |
| sol | NOK | +0.3298 | [+0.1994,+0.4470] | [+0.2117,+0.4500] | 0 |
| Opus 5 | FOK | +0.1213 | [+0.0047,+0.2449] | **[−0.0136,+0.2368]** | 0 |
| Opus 5 | NOK | +0.1528 | [+0.0659,+0.2509] | [+0.0923,+0.2392] | 0 |
| Haiku 4.5 | FOK | +0.4151 | [+0.2336,+0.5712] | [+0.1339,+0.6129] | 0 |
| Haiku 4.5 | NOK | +0.4511 | [+0.3265,+0.5741] | [+0.2925,+0.5981] | 0 |
| K3 | FOK | +0.0571 | [−0.0954,+0.2052] | [−0.1235,+0.2282] | 1 |
| K3 | NOK | +0.2605 | [+0.1456,+0.3866] | [+0.1653,+0.3933] | 0 |

**One STOP row: Opus 5 FOK.** Its item-level interval excluded zero by **+0.0047**, the
most marginal interval in the manuscript; the clustered interval includes zero. LOPO shows
zero sign changes, so the point estimate is stable and the interval is what fails. Every
NOK row, including all three cross-vendor lineages, survives clustering. mini's NOK row
carries the standing all-tie degeneracy flag and its interval is not a calibrated
uncertainty.

## 5. `AUX-E1R-BELIEVED-NOK` — the BELIEVED-index NOK result

Coverage census: FR-Bank scoreable items **661**; NOK-joinable under **TRUE 661**, under
**BELIEVED 661**. Full coverage. The result required no new monitor call.

| Row | n | blind | indexed | Δ | item-level CI | clustered CI |
|---|---:|---:|---:|---:|---|---|
| FOK FR-Bank TRUE | 661 | 0.5056 | 0.7442 | +0.2386 | [+0.1856,+0.2877] | — |
| FOK FR-Bank BELIEVED | 661 | 0.5056 | 0.7476 | +0.2420 | [+0.1891,+0.2879] | — |
| NOK FR-Bank TRUE | 661 | 0.4946 | 0.7339 | +0.2393 | [+0.1801,+0.2949] | [+0.1552,+0.3237] |
| **NOK FR-Bank BELIEVED** | 661 | 0.4946 | **0.5959** | **+0.1012** | **[+0.0458,+0.1543]** | **[+0.0217,+0.1744]** |

| Quantity | Value |
|---|---:|
| FOK believed-index retention (believed Δ ÷ true Δ) | **101.4%** (reproduces the published figure) |
| **NOK believed-index retention** | **42.3%** |
| NOK BELIEVED LOPO Δ range | [+0.0890, +0.1141], 0 sign changes |
| Frozen 60% retention gate | **not met** for NOK; met for FOK |

Frozen branch selected: *retention < 60% but CI excludes zero — NOK degrades materially
under believed metadata but remains positive.* The asymmetry is the finding: coverage
judgment is insensitive to the store's corrupted self-description, while obligation judgment
loses more than half its benefit.

## 6. `AUX-E1R-BASELINES` — non-LLM readers of the same serialized indexes

**Extended at R81 by §11 `AUX-E1R-NB6`**, which adds a sixth reader aimed at the
superseded-names section alone. On NOK-TRUE that reader displaces NB-5 as `best`.

Legitimate index-reading baselines only (see §7 for the disqualified one). "Best" is the
strongest of NB-1, NB-2, NB-4, NB-5, NB-3-idx on that row. Tolerance ±0.05, inherited from
the count-destruction probe.

| Population | prov | n | monitor | NB-1 | NB-2 | NB-4 | NB-5 | NB-3-idx | best | monitor − best | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| R-FOK-FRB | TRUE | 307 | 0.7003 | 0.5194 | 0.5228 | 0.6080 | 0.6186 | 0.5048 | 0.6186 | **+0.0817** | monitor wins |
| R-FOK-FRB | BELIEVED | 307 | 0.7005 | 0.5194 | 0.4630 | 0.6080 | 0.6186 | 0.5419 | 0.6186 | **+0.0819** | monitor wins |
| R-NOK-FRB | TRUE | 661 | 0.7339 | 0.5514 | 0.5834 | 0.5383 | 0.5974 | 0.4780 | 0.5974 | **+0.1365** | monitor wins |
| R-NOK-FRB | BELIEVED | 661 | 0.5959 | 0.4987 | 0.5459 | 0.5383 | 0.5974 | 0.4715 | 0.5974 | −0.0015 | matches |
| R-FOK-MEM0 | TRUE | 238 | 0.4777 | 0.4818 | 0.4923 | 0.5000 | 0.5000 | 0.4464 | 0.5000 | −0.0223 | matches |
| R-FOK-MEM0 | BELIEVED | 238 | 0.5741 | 0.4818 | 0.5372 | 0.5000 | 0.5000 | 0.4621 | 0.5372 | +0.0369 | matches |
| R-FOK-AMEM | TRUE | 284 | 0.4526 | 0.5226 | 0.4184 | 0.5000 | 0.5000 | 0.5163 | 0.5226 | −0.0700 | baseline wins |
| R-FOK-AMEM | BELIEVED | 284 | 0.5278 | 0.5226 | 0.4452 | 0.5000 | 0.5000 | 0.5098 | 0.5226 | +0.0052 | matches |
| R-FOK-HARD | TRUE | 588 | 0.7530 | 0.4513 | 0.7246 | 0.6983 | 0.8124 | 0.6827 | 0.8124 | −0.0594 | baseline wins† |
| R-FOK-HARD | BELIEVED | 588 | 0.7955 | 0.4513 | 0.7367 | 0.6983 | 0.8124 | 0.6909 | 0.8124 | −0.0169 | matches† |

† Pooled hard-tier **absolute levels are not interpretable**: all 35 positives in that
population are FR-Bank, so the one-bit rule "this item is FR-Bank" scores **0.7541**, above
the monitor's pooled indexed 0.7530. Paired deltas are unaffected, because a
constant-across-arms indicator cannot produce a delta.

**Reading.** On the two FR-Bank populations — the only ones whose backend exposes a usable
index — the monitor beats every mechanical index reader by **+0.0817 / +0.0819** on FOK and
**+0.1365** on NOK-TRUE. On the structureless backends every reader including the monitor
sits at chance, which is what "structureless" predicts. The single exception is
**NOK-BELIEVED**, where the monitor (0.5959) is indistinguishable from a local embedding
matcher (0.5974) — the same degradation that §5's 42.3% retention records, reached by an
independent route.

## 7. `AUX-E1R-NB3-DISQUALIFIED` — a baseline that read the question, not the store

NB-3 as frozen (TF–IDF over index text **concatenated with the question**) was disqualified
after its ablation. Index-only sits near chance while question-only exceeds the concatenated
version on every population.

| Population | prov | index + question | index only | question only |
|---|---|---:|---:|---:|
| R-FOK-HARD | TRUE | 0.7637 | 0.6827 | **0.9598** |
| R-FOK-HARD | BELIEVED | 0.7602 | 0.6909 | **0.9598** |
| R-FOK-FRB | TRUE | 0.8070 | 0.5048 | **0.9164** |
| R-FOK-FRB | BELIEVED | 0.8333 | 0.5419 | **0.9164** |
| R-NOK-FRB | TRUE | 0.7221 | 0.4780 | **0.8707** |
| R-NOK-FRB | BELIEVED | 0.7024 | 0.4715 | **0.8707** |
| R-FOK-MEM0 | TRUE | 0.9625 | 0.4464 | **0.9667** |
| R-FOK-MEM0 | BELIEVED | 0.9622 | 0.4621 | **0.9667** |
| R-FOK-AMEM | TRUE | 0.9512 | 0.5163 | **0.9539** |
| R-FOK-AMEM | BELIEVED | 0.9528 | 0.5098 | **0.9539** |

This is the E1-QP question-authorship confound (D94) reappearing inside a baseline built for
this pass. It is retained in the ledger as an instrument-failure record, not as evidence
about the index.

## 8. `AUX-E1R-ECE` — calibration intervals

Pooled hard tier, n = 588, 35 positives, base rate 0.0595.

| Arm | AUROC | ECE | ECE CI (item) | ECE CI (persona-clustered) |
|---|---:|---:|---|---|
| blind | 0.5258 | 0.1596 | [0.1349, 0.1826] | [0.1378, 0.1823] |
| intact index | 0.7530 | 0.1741 | [0.1529, 0.1954] | [0.1556, 0.1939] |
| counts jittered | 0.7697 | 0.1720 | [0.1509, 0.1935] | [0.1527, 0.1928] |
| counts coarsened | 0.7625 | 0.1668 | [0.1453, 0.1882] | [0.1473, 0.1881] |
| names only | 0.8516 | 0.0583 | [0.0418, 0.0772] | [0.0410, 0.0795] |

Paired difference against the blind arm:

| Arm vs blind | ΔECE | CI (item) | excludes zero |
|---|---:|---|:-:|
| intact index | +0.0145 | [−0.0037, +0.0345] | **no** |
| counts jittered | +0.0124 | [−0.0063, +0.0317] | no |
| counts coarsened | +0.0072 | [−0.0113, +0.0256] | no |
| names only | −0.1013 | [−0.1171, −0.0815] | **yes** |

Frozen branch selected: *the blind−intact ECE difference includes zero — the intact index
leaves calibration statistically unchanged; the manuscript's existing word "unimproved" is
exactly right and may not be upgraded to "worse".* The names-only improvement is the one
calibration effect that survives an interval.

## 9. `AUX-E1R-RELIABILITY` — ranker or probability?

Bins with n ≥ 10; Spearman rank correlation between mean predicted FOK and observed
frequency. Figure: `results/reliability.pdf` / `.png`.

| Arm | bins | Spearman ρ | p | mean predicted | observed | worst over-confidence gap |
|---|---:|---:|---:|---:|---:|---:|
| blind | 5 | **0.1026** | 0.8696 | 0.219 | 0.060 | −0.700 |
| intact index | 5 | **0.9000** | 0.0374 | 0.217 | 0.056 | −0.440 |
| names only | 5 | **1.0000** | 0.0000 | 0.116 | 0.058 | −0.300 |

Every arm over-states coverage in every bin. The indexed arms rank well and scale badly:
mean predicted 0.217 against an observed 0.056, roughly **3.9×** over-confident. The blind
arm neither ranks (ρ = 0.10, p = 0.87) nor calibrates, consistent with its chance AUROC.

## 10. Do not use

| Value | Why |
|---|---|
| NB-3 index+question AUROCs (0.7024–0.9625) | reads question templates, not the store; §7 |
| Pooled hard-tier absolute baseline or monitor AUROCs as coverage discrimination | backend indicator alone reaches 0.7541; §6† |
| Any clustered interval for mini NOK | blind arm is constant at 0.0; all-tie artifact |
| "Persona clustering widens the intervals" | false here; ρ ≈ 0 and four of six narrow |

## 11. `AUX-E1R-NB6` — the superseded-names matcher (R81)

Registered in `registrations/ADDENDUM_R81.md` (HEAD `2bb7fd9`, Amendment 1 at `da0d4a0`),
frozen before any value below existed. Produced by `tools/run_nb6.py` +
`tools/finalize_nb6.py`; table of record `results/baselines_final_r81.json`.

NB-6 scores each question against ONE section of the same serialized index the monitor
read: the flat list under `ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT`. NB-4 and NB-5
score the whole per-category name map, which dilutes that signal. Two variants, lexical
(NB-4's tokenizer, Jaccard) and embedding (NB-5's local offline encoder, cosine).
Unsupervised and intent-blind. Tolerance ±0.05.

### Obligation rows (the registered population)

| Population | prov | n | monitor | NB-6 lex | NB-6 emb | NB-6 best | monitor − NB-6 | names/item | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| R-NOK-FRB | TRUE | 661 | 0.7339 | 0.5738 | **0.7484** | 0.7484 | -0.0145 | 1.75 | NB-6 above the monitor, within tolerance |
| R-NOK-FRB | BELIEVED | 661 | 0.5959 | 0.4718 | **0.5858** | 0.5858 | +0.0101 | 15.04 | monitor above NB-6, within tolerance |

### Effect on the table of record

| Population | prov | best before NB-6 | monitor − best | best after NB-6 | monitor − best |
|---|---|---|---:|---|---:|
| R-NOK-FRB | TRUE | NB-5 embedding match (0.5974) | +0.1365 | NB-6 superseded-names match (0.7484) | -0.0145 |
| R-NOK-FRB | BELIEVED | NB-5 embedding match (0.5974) | -0.0015 | NB-5 embedding match (0.5974) | -0.0015 |

### Coverage rows — reproduction check, not a measurement

FOK-6 scores the whole per-category name map, which makes it definitionally NB-4
(lexical) and NB-5 (embedding): same name list, same tokenizer, same encoder, same
estimator. It is a reproduction check at 4dp, and it passes on both arms. **No NB-6 cell
is printed on a coverage row** (D-E1R-7, ADDENDUM_R81 §3).

| Population | prov | FOK-6 lex | committed NB-4 | FOK-6 emb | committed NB-5 | reproduces at 4dp |
|---|---|---:|---:|---:|---:|---|
| R-FOK-FRB | TRUE | 0.6080 | 0.6080 | 0.6186 | 0.6186 | yes |
| R-FOK-FRB | BELIEVED | 0.6080 | 0.6080 | 0.6186 | 0.6186 | yes |

### Matched-84, descriptive

Carries no prediction. Reported for the ladder comparison only; the monitor comparators
for this set are the cross-vendor rows in `e1xv_crossvendor`, not a single number, so no
delta is formed here.

| prov | n | n_pos | NB-6 lex | NB-6 emb | NB-6 best |
|---|---:|---:|---:|---:|---:|
| TRUE | 84 | 40 | 0.5375 | 0.6023 | 0.6023 |
| BELIEVED | 84 | 40 | 0.4815 | 0.5563 | 0.5563 |

### Registered outcomes

| Prediction | Statement | Outcome |
|---|---|---|
| **NB6-1** | monitor NOK-TRUE exceeds best NB-6 NOK-TRUE by more than the tolerance | **FAILS** (monitor 0.7339, NB-6 0.7484, margin -0.0145) |
| **NB6-2** | monitor NOK-BELIEVED and best NB-6 NOK-BELIEVED are within the tolerance | **HOLDS** (monitor 0.5959, NB-6 0.5858, margin +0.0101) |

**Reading.** Narrowing the embedding matcher from the whole name map (0.5974 on NOK-TRUE) to the
superseded-names list alone (0.7484)
carries it past the monitor's 0.7339.
Under the TRUE index the monitor's obligation judgment no longer holds a margin over a
mechanical reader: the margin of record falls from +0.1365 to -0.0145. Under the BELIEVED index the
matcher reaches 0.5858 against the monitor's 0.5959,
inside the tolerance. On both provenances the monitor is no better than a matcher reading
that one list. The TRUE superseded list averages 1.75 names per item; the BELIEVED list averages 15.04.

**Not drawn (U9).** This section states what NB-6 measures. It does **not** assert that the
BELIEVED NOK retention and the flat-lookup mechanism bound explain each other; that link
stays undrawn in the ledger and in the manuscript.

## 12. `AUX-E1R-NB6-COMPOSITION` — why the superseded-names matcher works where it does

**POST HOC and unregistered.** Designed after NB6-1 failed, to ask why a matcher over one
index section reaches the smallest monitor. It carries no prediction and prints whatever it
finds. Produced by `tools/nb6_composition.py`; artifact `results/nb6_composition.json`.
Deterministic, $0, no model call. **D-E1R-10 (2026-09-12):** the own-name rows below were
corrected in this ledger; the artifact's own-name fields (`pn_named_*`, `named_by_lifecycle_state`,
`n_{named,unnamed}_pn`, the `*_{named,unnamed}_pn` AUROCs and means) still carry the key
collision until the script is re-run under that entry's disposition. The per-state rows never
read the collided map and are unaffected.

**Structural premise, read off the generator rather than measured here.**
`e1_metamemory/tools/index_v2.py` emits per-category active, superseded, retracted and
expired **counts**, but names attributes in exactly one place: the flat section
`ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT`. Expiry and retraction therefore reach the
index as a count and never as a name.

### Obligation composition by lifecycle state

| Population | PN total | superseded | expired | retracted | supersession share |
|---|---:|---:|---:|---:|---:|
| R-NOK-FRB (n=661) | 104 | 63 | 15 | 26 | 0.606 |
| matched-84 | 40 | 19 | 8 | 13 | 0.475 |

### Discrimination by the lifecycle state of the obligation (\trueidx{}, same negatives)

| Positives | n | NB-6 embedding | monitor |
|---|---:|---:|---:|
| PN from superseded | 63 | **0.9534** | 0.8572 |
| PN from expired | 15 | **0.4823** | 0.5110 |
| PN from retracted | 26 | **0.4053** | 0.5638 |

Under \believed{} the same split gives NB-6 0.6583, 0.5926, 0.4062 against the monitor's 0.7010, 0.4983, 0.3975 on supersession, expiry and retraction respectively.

### Own-name presence in the section the matcher reads (corrected, D-E1R-10)

For each obligation item, the check asks whether any attribute name behind that item
appears in the superseded-names section it was shown. **Corrected 2026-09-12 (D-E1R-10):** the
printed rows keyed entry ids without the persona, and FR-Bank ids recur across personas; the
corrected rows key by (persona, entry id). The printed rows are retained as the pre-correction
record (D-E1R-8's convention) and are superseded.

| Provenance | obligations named | rate |
|---|---|---:|
| **\trueidx{}, corrected (persona-keyed)** | **74 of 104** (supersession 63 of 63, retraction 11 of 26, expiry 0 of 15) | **0.712** |
| **\believed{}, corrected (persona-keyed)** | **31 of 104** (supersession 24 of 63, retraction 3 of 26, expiry 4 of 15) | **0.298** |
| \trueidx{}, as printed before D-E1R-10 — SUPERSEDED (key collision) | 7 of 104 | 0.067 |
| \believed{}, as printed before D-E1R-10 — SUPERSEDED (key collision) | 13 of 104 | 0.125 |

Corrected per-variant rates under \trueidx{}: FULL 32 of 47, SLOT-ABLATED 29 of 35, CAT-ABLATED
13 of 22. (The printed "FULL 3 of 47, SLOT-ABLATED 3 of 35, CAT-ABLATED 1 of 22 … not an artifact
of the ablation construction" carried the collision and is superseded.)

**Reading.** NB-6's aggregate 0.7484 on NOK-\trueidx{} is carried by one class of
obligation. On supersession-derived items it reaches 0.9534; on expiry it sits at 0.4823 and on retraction at 0.4053, both at or below chance. That is the pattern the
structural premise predicts: the self-description names supersession and only counts the
other two. The monitor is also weaker off supersession (0.5110 on expiry, 0.5638 on retraction), and on retraction it is the higher of the two.

**What this test shows (corrected, D-E1R-10).** It is an EXACT SLOT MATCH: it asks whether an
attribute name behind the item appears verbatim in the named section. Keyed by (persona, entry
id) it finds 74 of 104 under \trueidx{}, and 63 of 63 on the supersession-derived items: on the
one state the index names, the matcher has the item's own name to read. The printed 7 of 104
keyed entry ids without their persona (D-E1R-10), and the near-synonym reading written for that
figure (D-E1R-9) loses its premise: the exact match is not a miss to be explained, it is a hit on
the whole state. Whether the *monitor* reads that name is the registered question of
`registrations/ADDENDUM_RESP.md` §L1 (the own-name ablation) and is not settled here. What IS
supported, by the per-state rows above, is that discrimination follows naming.
The composition figures are consistent with that: the matched-84 cell is
0.475 supersession against 0.606 on
the full population, and NB-6 scores 0.6023 there against 0.7484 on the full population.

**Not drawn (U9).** Nothing here joins the BELIEVED retention figure to the flat-lookup
bound. The two remain separate findings.

## 13. `AUX-E1R-NB6-PERSTATE` — per-state intervals and the frontier split (R81 Phase 1c)

Registered in `registrations/ADDENDUM_R81.md` §10, frozen at `e8ba22c` **before any**
interval below existed. Produced by `tools/nb6_perstate.py`; artifact
`results/nb6_perstate.json`. Deterministic, $0, no model call.

**Estimator (frozen §10.1).** Stratified paired item-level bootstrap: 1,000 draws, seed 42;
positives resampled with replacement within their lifecycle state, negatives from the shared
pool, both at observed counts; both readers scored on the identical resampled index set;
single-class draws discarded; 2.5/97.5 percentiles. Point estimates are computed on the same
subset the bootstrap resamples (this state's positives plus the shared negatives), so they
reproduce §12's per-state points exactly.

### Item 2 — mini census, per state (n_neg = 557)

| Obligation from | n | matcher | matcher CI | monitor | monitor CI | monitor − matcher | CI | excludes 0 |
|---|---:|---:|---|---:|---|---:|---|---|
| Supersession | 63 | 0.9534 | [+0.9281,+0.9760] | 0.8572 | [+0.7946,+0.9142] | -0.0962 | [-0.1520,-0.0495] | **yes** |
| Expiry | 15 | 0.4823 | [+0.3626,+0.6110] | 0.5110 | [+0.3971,+0.6383] | +0.0287 | [-0.1795,+0.2212] | no |
| Retraction | 26 | 0.4053 | [+0.2812,+0.5320] | 0.5638 | [+0.4629,+0.6760] | +0.1585 | [+0.0002,+0.3341] | **yes** |

**Frozen branch fired (retraction).** The difference interval excludes zero, so the branch
text is: *the monitor exceeds the matcher on retraction-derived obligations at n=26, by
+0.1585 [+0.0002,+0.3341]*. **The lower bound is +0.0002**, at the boundary of
exclusion; this row is marginal and is reported as marginal wherever it appears.

**Expiry, fixed text either way:** the index counts expired content, and neither reader
recovers it. Both one-sample intervals include 0.5 ([+0.3626,+0.6110] and [+0.3971,+0.6383]).

### Item 3 — the three completed n=661 lanes, per state

sol and K3 are absent because the budget directive stopped them and they were never scored
as cells on this population (D-R74-6). Twelve rows.

| Lane | Obligation from | n | lane | lane CI | lane − matcher | CI | excludes 0 |
|---|---|---:|---:|---|---:|---|---|
| luna | Supersession | 63 | 0.8933 | [+0.8495,+0.9324] | -0.0601 | [-0.1021,-0.0246] | **yes** |
| luna | Expiry | 15 | 0.8248 | [+0.7825,+0.8656] | +0.3425 | [+0.2093,+0.4636] | **yes** |
| luna | Retraction | 26 | 0.6323 | [+0.5255,+0.7361] | +0.2270 | [+0.0836,+0.3679] | **yes** |
| Opus 5 | Supersession | 63 | 0.8690 | [+0.8322,+0.9026] | -0.0845 | [-0.1226,-0.0486] | **yes** |
| Opus 5 | Expiry | 15 | 0.8881 | [+0.8576,+0.9153] | +0.4058 | [+0.2751,+0.5264] | **yes** |
| Opus 5 | Retraction | 26 | 0.7129 | [+0.6526,+0.7736] | +0.3077 | [+0.1772,+0.4386] | **yes** |
| Haiku 4.5 | Supersession | 63 | 0.8897 | [+0.8382,+0.9306] | -0.0637 | [-0.1166,-0.0159] | **yes** |
| Haiku 4.5 | Expiry | 15 | 0.6874 | [+0.5720,+0.7962] | +0.2051 | [+0.0002,+0.3893] | **yes** |
| Haiku 4.5 | Retraction | 26 | 0.7317 | [+0.6406,+0.8222] | +0.3264 | [+0.1956,+0.4663] | **yes** |

### Adjudication

- Condition 1, at least two of three lanes clear the matcher with intervals excluding zero
  on retraction **and** expiry: **True** (all three clear on both).
- Condition 2, no lane clears the matcher by more than 0.05 on supersession: **True** (all three sit *below* the matcher there, each interval excluding zero).

**Reading (i) fired.** Main-text sentence: *Larger models recover part of the obligation the index only counts.*

**Reading.** The split is a crossover rather than a level difference. On supersession, the
content the index names, the matcher (0.9534) is above all three lanes (0.8933, 0.8690, 0.8897), every difference excluding zero. On expiry and retraction, the content the index only
counts, all three lanes are above the matcher, every difference excluding zero.

**Superseded by §14 on the attribution.** An earlier draft of this paragraph concluded that
the larger models' margin over the lookup therefore comes from the states the
self-description does not name. That is an attribution, and the lane-versus-matcher
comparison cannot support it: the matcher is intent-blind and the lanes see the question.
§14 computes the prior-controlled quantity and reading (ii) fired. What survives here is the
description of where each reader scores higher, not a claim about what supplies it.

**Scope.** Expiry rests on 15 obligations and retraction on 26. The lane intervals are wide
and the mini retraction difference is marginal. What the rows support is the direction of
the crossover, not a calibrated size for it.

**Not drawn (U9).** Nothing here joins the BELIEVED retention figure to the flat-lookup
bound.

## 14. `AUX-E1R-NB6-ATTRIBUTION` — the prior-controlled test of the Phase 1c reading

Registered in `registrations/ADDENDUM_R81.md` §11, frozen at `cfe5415` **before any value**
below existed. Produced by `tools/nb6_attribution.py`; artifact
`results/nb6_attribution.json`. Deterministic, $0, no model call.

**Why.** Phase 1c compared each lane against the intent-blind matcher and read the gap on
expiry and retraction as the larger models recovering obligation from the index. That
comparison cannot establish it: the lanes see the question, and this paper's own
question-prior audit shows question text carries state-flavoured signal. The
prior-controlled quantity is the paired indexed-minus-blind delta, per state.

Mini is excluded: its blind NOK arm is constant, the standing all-tie degeneracy at §1.

### Item 1 — indexed minus blind, per lane per state

| Lane | Obligation from | n | blind | indexed | indexed − blind | CI | excludes 0 |
|---|---|---:|---:|---:|---:|---|---|
| luna | Supersession | 63 | 0.3693 | 0.8933 | +0.5240 | [+0.4544,+0.5970] | **yes** |
| luna | Expiry | 15 | 0.7197 | 0.8248 | +0.1051 | [+0.0056,+0.2163] | **yes** |
| luna | Retraction | 26 | 0.4881 | 0.6323 | +0.1442 | [-0.0077,+0.3041] | no |
| Opus 5 | Supersession | 63 | 0.5387 | 0.8690 | +0.3303 | [+0.2814,+0.3831] | **yes** |
| Opus 5 | Expiry | 15 | 0.8709 | 0.8881 | +0.0172 | [-0.0057,+0.0411] | no |
| Opus 5 | Retraction | 26 | 0.7641 | 0.7129 | -0.0511 | [-0.0987,+0.0009] | no |
| Haiku 4.5 | Supersession | 63 | 0.3264 | 0.8897 | +0.5634 | [+0.4936,+0.6292] | **yes** |
| Haiku 4.5 | Expiry | 15 | 0.6542 | 0.6874 | +0.0332 | [-0.1263,+0.1773] | no |
| Haiku 4.5 | Retraction | 26 | 0.4918 | 0.7317 | +0.2399 | [+0.1301,+0.3577] | **yes** |

### Adjudication

Reading (i) required the delta to exclude zero on at least two of three lanes on **both**
expiry and retraction. On expiry one lane qualifies (luna); on retraction one lane qualifies
(Haiku 4.5). **Reading (ii) fired.**

Landed §4.3 sentence: *That matcher reaches the smallest model tested. Larger models score
higher on the states the index only counts.* No attribution.

**Reading.** On supersession the index does the work for every lane: deltas +0.5240, +0.3303, +0.5634, all excluding zero.
On the two states the index only counts, the picture is question prior more than index.
Opus 5 blinds at 0.8709 on expiry and 0.7641 on retraction, so most of its apparent per-state
lead over the matcher was already available without the store. Its retraction delta is
-0.0511: the index moved it slightly the wrong way. The
Phase 1c crossover survives as a description of where each reader scores higher. It does
**not** survive as an attribution of the larger models' advantage to the index.

### Item 3 — persona-clustered intervals on the mini per-state differences

Monitor minus matcher, all three states, so no row is singled out. 40 personas.

| Obligation from | difference | item-level CI | persona-clustered CI | clustered excludes 0 |
|---|---:|---|---|---|
| Supersession | -0.0962 | [-0.1520,-0.0495] | [-0.1712,-0.0307] | **yes** |
| Expiry | +0.0287 | [-0.1795,+0.2212] | [-0.3115,+0.4296] | no |
| Retraction | +0.1585 | [+0.0002,+0.3341] | [-0.0560,+0.4152] | no |

**Frozen retraction sentence fired:** the retraction row is marginal at item level (lower
bound +0.0002) and not separated under persona clustering. The supersession row, where the
matcher leads the smallest reader, survives clustering.

**Not drawn (U9).** Nothing here joins the BELIEVED retention figure to the flat-lookup
bound.
