# NUMBERS_R74 — canonical ledger for the R74 revision program

Registration: `registrations/ADDENDUM_R74.md`, frozen at the R74-R commit
`35f8416a555baf097350b9144393f245646e557a` (short form `35f8416a55`, printed in Table 15)
before any monitor call. One canonical value per figure; anything not in this file (or the ledgers
it inherits) does not go in a draft. Verifier: `r74/tools/verify_r74.py` (two-direction,
written with the first scored result). Bootstrap: committed scorers, 1,000 draws, seed
42, paired arms, single-class draws discarded; item-level primary, persona-clustered
sensitivity.

Manuscript scan: `iclr2027_monitoring_submission/tools/trace_scan_v12.py` = v11 + this
ledger. Declared in ADDENDUM_R74 (not a post-hoc instrument change).

## X1 — FOK question-prior probe

Run 2026-08-24, offline, $0. Apparatus: e1qp `oof_tfidf` (StratifiedGroupKFold,
persona-grouped, seed 42), target y_fok (non-ABSENT vs ABSENT). Source:
`r74/x1/x1_results.json`. **Branch taken: HIGH** (both lower bounds ≥ 0.65).

| Key | Population | n | pos | AUROC | 95% CI | Note |
|---|---|---:|---:|---:|---|---|
| **AUX-R74-X1-POOLED** | pooled hard tier | 588 | 35 | **0.9662** | **[0.9510, 0.9788]** | text carries coverage-label signal |
| **AUX-R74-X1-FRB** | FR-Bank hard | 307 | 35 | **0.9199** | **[0.8879, 0.9471]** | label-identical to the committed PN probe on this tier (y_fok ≡ y_nok on both populations: 0 differing items); point estimate reproduces the committed value exactly |

Instrument finding (D-R74-2): the hard tier contains no PRESENT items, so the FOK
positive class coincides with PN on both registered populations — the FOK probe is the
same label vector as the PN probe, not an independent measurement. Disclosed in the App D
row and the §7.1 sentence.

R75-F6 interval choice: the two label-identical n=307 rows print as ONE App D row
carrying the committed PN-probe interval [0.8869, 0.9472] (the earlier of the two
computations of the same label vector). AUX-R74-X1-FRB's re-derived interval
[0.8879, 0.9471] stays ledgered here and is NOT printed — same point, same labels,
seed-path difference only; no recomputation was performed for the collapse.

## X2 — index-ablation mechanism probe

Run 2026-08-24: 1,566 mini calls, $0.5244, 0 failures. Blind and intact arms = committed
E1 rows (reproduction gate: Mem0 intact delta −0.0969, A-MEM −0.1065 — both re-derive the
committed Table 1 values exactly). Source: `r74/x2/x2_scores.json`,
`r74/x2/x2_indexes.json` (arm builder assertions passed). **Branch taken:
ii-multiple/partial** — sole recovering pair is the compound arm on one store:
X2d-count-markers-removed@amem via the shrink rule (|−0.0368| ≤ 0.5·|−0.1065| and the
intact delta lies outside the arm CI). No single channel recovers anywhere. The names arm
(X2b) has **no ablation site**: all 77 external index keys expose zero category names
(every name section's body is exactly the marker line), so X2b equals intact by
construction.

| Key (AUX-R74-X2-…) | Store | Arm | n | indexed AUROC | Δ vs blind | item CI | clustered CI |
|---|---|---|---:|---:|---:|---|---|
| M0-INTACT | Mem0 | intact (committed) | 238 | 0.4777 | −0.0969 | [−0.169,−0.025] | [−0.1638,−0.0286] |
| M0-A | Mem0 | count removed | 238 | 0.4802 | −0.0943 | [−0.1674,−0.0233] | [−0.1482,−0.0440] |
| M0-C | Mem0 | markers removed | 238 | 0.4796 | −0.0949 | [−0.1654,−0.0250] | [−0.1553,−0.0320] |
| M0-D | Mem0 | count+markers removed | 238 | 0.4664 | −0.1082 | [−0.1769,−0.0392] | [−0.1723,−0.0431] |
| AM-INTACT | A-MEM | intact (committed) | 284 | 0.4526 | −0.1065 | [−0.173,−0.040] | [−0.1654,−0.0446] |
| AM-A | A-MEM | count removed | 284 | 0.4587 | −0.1004 | [−0.1699,−0.0309] | [−0.1575,−0.0427] |
| AM-C | A-MEM | markers removed | 284 | 0.4705 | −0.0886 | [−0.1550,−0.0269] | [−0.1449,−0.0300] |
| AM-D | A-MEM | count+markers removed | 284 | 0.5223 | −0.0368 | [−0.1041,+0.0268] | [−0.0974,+0.0225] |

## X3 — billed economics micro-run — NON-CONFIRMING BRANCH (both numbers print)

Run 2026-08-24, telemetry only: 10,000 INDEXED-TRUE cached + 2,000 BLIND mini calls,
$4.07 billed total. Source: `r74/x3/x3_billed.json`, raw `r74/x3/telemetry.jsonl`.
Prices pinned at run date (developers.openai.com/api/docs/pricing): input $0.40 /
cached input $0.10 / output $1.60 per 1M tokens — cached input is **25% of list**, not
the 10% the committed asymptotic projection assumed.

| Key | Quantity | Value |
|---|---|---|
| AUX-R74-X3-IDX | indexed cached, as-billed | **$360.33 per 1M calls** (print $360); mean prompt 1,552.7 tok, mean cached 999.1 tok, cache-hit token share **64.3%**, mean output 24.4 tok |
| AUX-R74-X3-BLIND | blind, as-billed | **$233.39 per 1M calls** (print $233); mean prompt 479.5 tok, 0 cached; confirms the committed $234 projection |
| AUX-R74-X3-VERDICT | ordering indexed-cached < blind | **NOT CONFIRMED as billed** — frozen rule: both numbers print; the projection sentence stays; the text states the discrepancy (25% cached price; 64.3% block-aligned hit share) |

Do-not-use reminder: the 12,000 calls' FOK/NOK outputs are telemetry-only by
registration and are not scored anywhere.

## X4 — matched-cell expansion — CAP-STOP BRANCH (4 completed lanes)

Run 2026-08-24. Source: `r74/x4/x4_scores.json`, rows in `r74/x4/rows_*.jsonl`, cell
`r74/x4/cell_661.json` (asserted 661 / 104 PN / 307 hard / 35 FOK-pos). Completed lanes:
mini (committed E1 rows, $0), luna ($2.67), Opus 5 ($40.20, batch), Haiku 4.5 ($5.36,
batch). **Stopped incomplete under D-R74-6 (PI budget directive): sol (1,422 rows,
$12.39), K3 (231 rows, $3.16) — never scored as cells.** Per the frozen cap-stop branch:
no Table-4 primary swap; completed lanes print in the expansion appendix table; §5.2
gains one sentence. Mini rows cite the committed canonical intervals; the expansion
scorer re-derives mini's points exactly (XP-5) and its clustered CIs reproduce
AUX-E1R-CLUSTER to the digit.

| Key (AUX-R74-X4-…) | Lane | Cell | n | Blind | Indexed | Δ | item CI | clustered CI |
|---|---|---|---:|---:|---:|---:|---|---|
| MINI-NOK | mini (committed) | NOK | 661 | 0.4946 | 0.7339 | +0.2393 | [+0.1801,+0.2949] | [+0.1552,+0.3237] |
| MINI-FOK | mini (committed) | FOK | 307 | 0.4966 | 0.7003 | +0.2037 | [+0.0935,+0.3191] | [+0.1259,+0.2767] |
| LUNA-NOK | luna | NOK | 661 | 0.4495 | 0.8182 | **+0.3687** | [+0.2932,+0.4358] | [+0.2656,+0.4666] |
| LUNA-FOK | luna | FOK | 307 | 0.5720 | 0.7605 | +0.1885 | [+0.0439,+0.3352] | [+0.0770,+0.3071] |
| OP5-NOK | Opus 5 | NOK | 661 | 0.6429 | 0.8327 | **+0.1898** | [+0.1437,+0.2411] | [+0.1241,+0.2523] |
| OP5-FOK | Opus 5 | FOK | 307 | 0.6793 | 0.8099 | +0.1306 | [+0.0557,+0.2148] | [+0.0523,+0.2026] |
| H45-NOK | Haiku 4.5 | NOK | 661 | 0.4150 | 0.8210 | **+0.4060** | [+0.3283,+0.4791] | [+0.3063,+0.5026] |
| H45-FOK | Haiku 4.5 | FOK | 307 | 0.3781 | 0.7465 | +0.3684 | [+0.2629,+0.4755] | [+0.2700,+0.4747] |

**Registered predictions — all held on the completed lanes:**
XP-1 (every completed new lane's NOK delta CI excludes zero): luna ✓ Opus ✓ Haiku ✓.
XP-2 (FOK deltas positive): ✓ all three.
XP-3 (indexed-NOK span < blind span): indexed **0.0988** vs blind **0.2279** ✓.
XP-4 (direction persistence): Haiku blind NOK 0.4150 below chance (CI [0.3611,0.4676]) ✓;
Opus blind NOK 0.6429 above chance (CI [0.5976,0.6889]) ✓.
XP-5 (mini reproduction): exact ✓.

## X5 — authorship-matched slice — S1 cured by ruling (a); monitor run COMPLETE (R75)

History: first spot-check 34/36 = 0.9444 → HARD-STOP S1 (D-R74-5 records the checker
instrument failure that preceded it). PI ruling (a): the two `relationship`-slot items
re-rendered slot-disambiguated; fixed checker reads **36/36 = 1.0**; launch approved
in-session (R75 block; D-R74-10 logs the metered-transport deviation before any call).
Run 2026-08-24: mini 216 calls sync ($0.0994), Opus 5 360 calls Batch ($2.3739);
**0 parse failures in all four arms**; total **$2.47** against the $2.40 pre-launch
projection. Sources: `r74/x5/x5_scores.json`, rows in `r74/x5/rows_{MINI,OP5}.jsonl`,
probes `r74/x5/x5_probes.json`.

| Key | Value |
|---|---|
| AUX-R74-X5-CELL | definite post-removal cell n **36** (12 PN, 17 PRESENT, 7 ABSENT), 29 personas, 4 slot tokens, reconstructed by the registered removal rule (routed-back treated as removed) |
| AUX-R74-X5-TRANSFER | label-transfer accuracy after ruling (a): **36/36 = 1.0** (bar 0.95); the S1-firing 0.9444 is the pre-ruling value |
| AUX-R74-X5-MINI-NOK | blind **0.4774** [0.2991, 0.6623] (includes 0.50); indexed **0.6771**; delta **+0.2028** [−0.1121, +0.4984] — includes zero |
| AUX-R74-X5-OP5-NOK | blind **0.3993** [0.2008, 0.6232] (includes 0.50); indexed **0.6962**; delta **+0.2978** [+0.0752, +0.5292] — excludes zero |
| AUX-R74-X5-MINI-FOK (descriptive) | blind 0.5788; indexed 0.8867; delta +0.3110 [+0.1133, +0.5222] |
| AUX-R74-X5-OP5-FOK (descriptive) | blind 0.6675; indexed 1.0000; delta +0.3372 [+0.1399, +0.5709] |
| AUX-R74-X5-ORACLE | index-oracle on the definite cell: AUROC **0.6042**, 3/12 PN slots named, 4/36 items named; registered 99-cell value 0.5379 (3/33) — the indexed arm cannot answer by lookup on more than a handful of items |
| AUX-R74-X5-DEGEN | NOK degeneracy flags: mini blind 4 distinct / modal 0.64, mini indexed 9 / 0.39; Opus blind 32 / 0.08, indexed 31 / 0.06 — no near-constant arm |

**Registered verdicts:**
- **NS-1 (blind NOK at chance) HOLDS on both lanes.**
- **NS-2 (indexed−blind NOK delta > 0, CI excluding 0): HOLDS on Opus 5; FAILS on mini.**
  Frozen FAILS text, verbatim: "NS-2 FAILS. The indexed NOK delta does not exclude zero
  on the probe-neutral slice for mini."
- Prereg §5 pre-commitment: the confirming sentence + appendix row required NS-2 on BOTH
  lanes → **not added**; the failure ships in its frozen words and adds nothing.
- R74 branches (i)/(ii): neither trigger matches the measured pattern (blind FOK ordering
  survives descriptively 0.5788 < 0.6675; blind NOK at chance per NS-1's own registered
  prediction; NS-2 split across lanes) → reported as its own cell per the D-E1R-5
  precedent, **no §7.1 upgrade, no slogan demotion** (D-R74-11). §7.2's
  under-construction sentence is replaced by the measured statement (R75 instruction).

Do-not-use note (R75-F6 vocabulary discipline): "(CI not centrally keyed)" and any other
internal-ledger phrasing never prints; the mini Δ interval cells in `tab:ladder-exact`
print --- with a footnote.

The two failures are both `relationship`-slot items (ns:saga:relationship,
ns:zara:relationship) whose matched-voice renders drifted to partner-directed phrasing
("who is … in a relationship with / seeing anyone"); the independent extractor re-derived
slot = `partner`, an adjacent but distinct store slot, so the carried label does not
provably transfer. 34 of 36 renders re-derive (entity, slot, CURRENT) exactly.

Checker instrument note (D-R74-5): the first extraction pass returned empty on all 36
rows because Windows shell quoting mangled prompts containing quotes; the renders (quote-
free prompts) were unaffected and were kept verbatim; only the extraction re-ran after
the spawn fix. The 0.9444 is from the fixed checker.

Disposition: X5 monitor calls do not launch. The exhibits (all 36 renders beside their
templates, labels, and extraction verdicts) are staged for [AUTHOR-1] with the S1 record; the
ruling on the two drifted items (re-render under slot-disambiguated instruction and
re-check, drop with the registered removal arithmetic, or an explicit deviation) is
[AUTHOR-1]'s.

## R76 — NS-5 and the two $0 items

Registration: `registrations/ADDENDUM_R76.md`, frozen at the R76-A commit
`692e379bdcd0537fcd01baf69bc3a938210c0066` (short `692e379bdc`) before any call; branch
sentences amended pre-launch per D-R74-14, window closed at Batch submission. NS-3 and NS-4
are **struck** (§A1: the matched-84 cannot be authorship-matched, and NS-4 is unreachable
from the E1-NS pool) — no key exists for them and none may be created. Estimators, cell,
and renders are the committed R75 X5 ones, unchanged.

### NS-5 — Haiku 4.5 on the authorship-matched n=36 cell

Run 2026-08-24: 360 Batch calls (`msgbatch_018hCZkAZFxg6iwz92rKKaSM`), 360/360 succeeded,
**0 parse failures in both arms**, billed **$0.2959** against a $0.2421 probe-mean
projection and a $0.4612 max_tokens ceiling. Lane `claude-haiku-4-5-20251001`, served
identifier exact (E1.7). Scored as the Opus lane was: per-item mean over parse-OK draws,
MIN_DRAWS=3. Source: `r74/x6/x6_ns5_scores.json`, rows `r74/x6/rows_H45.jsonl`.

| Key | Value |
|---|---|
| **AUX-R76-NS5-NOK** | blind **0.4427** [0.2582, 0.6522] (includes 0.50); indexed **0.6562**; delta **+0.2208** [−0.0522, +0.4809] — includes zero |
| **AUX-R76-NS5-FOK** (descriptive) | blind 0.5419; indexed 0.9901; delta +0.4470 [+0.2148, +0.6723] |
| **AUX-R76-NS5-BRANCH** | **branch (iii)** — interval includes 0.50 and point < 0.45: indeterminate at n=36. **Boundary disclosure: the point sits 0.0073 below the 0.45 cut**, so the branch label is close-run and carries no more weight than "indeterminate" states; the frozen rule was applied as written and not adjusted to the measurement |
| **AUX-R76-NS5-DEGEN** | NOK degeneracy: blind 10 distinct / modal 0.50, indexed 13 / 0.44 — no near-constant arm. Draw stability: mean per-item NOK sd 0.0266 blind, 0.0041 indexed; 31/36 and 33/36 items identical across all five draws |

**XV-1 is untouched.** Its registered failed verdict is never re-adjudicated; NS-5 reports
and does not test it. The delta side is **not** a registered endpoint here (NS-4 struck) and
is descriptive only — though it corroborates §A1.2's arithmetic: all three lanes on this
cell give a positive NOK delta of similar size (mini +0.2028, Haiku +0.2208, Opus 5
+0.2978) and only Opus 5's interval excludes zero, which is what an n=36 cell can resolve.

### The two $0 items

Source: `r74/x6/x6_probes.json`. No metered calls.

| Key | Value |
|---|---|
| **AUX-R76-AVCENSUS** | one-feature attack-vector rule on the committed matched-84 cell: AUROC **0.9736** (0.5 tie credit; 77 tied pairs of 1,760), against the committed TF–IDF **0.7972** on the same cell; **6 of 8 strata single-class**; strata as n/PN/P(PN): AV3 21/0/0.000, AV2 16/8/0.500, AV1 14/13/**0.929**, AV7 13/13/1.000, NATURAL_ABSENT 8/0/0.000, AV4 6/6/1.000, AV9 4/0/0.000, AV6 2/0/0.000. **Deterministic census on committed labels — NO INTERVAL**, same family as the committed one-bit is-FR-Bank rule 0.7541 and the Table 16 census. Provenance: computed pre-freeze as the R76 STOP premise diagnostic (D-R74-13); seedless and sampling-free, so invariant to run order |
| **AUX-R76-MATCHED-PROBE** | committed E1-QP `oof_tfidf`, unchanged, on the 36 authorship-matched renders (12 PN, 29 personas, 5 splits): AUROC **0.3472** [0.1673, 0.5424] — **includes 0.50**. Wide interval expected at n=36 with 12 positives and disclosed as such; a construction check on the E1-NS cell, not a measurement of the FR-Bank populations, and not compared against 0.7972 as if the two sat on one population |
| **AUX-R76-ZEROSHOT** | **SKIPPED (registered)** — the committed cache `probe_llm_raw.jsonl` holds 362 rows and **0** `ns:*` rows, and the matched questions are newly rendered text, so the row would require fresh metered calls ($0 rule) |

Reproduction note: the four committed `AUX-R74-X5-*` rows re-derive exactly from
`r74/x5/x5_scores.json` (checked, not recomputed — the committed scorer output was read,
not re-run). FOK blind CIs exist in that artifact but are **not** ledgered and do not print.


## R77 — review-fix pass (registration `registrations/ADDENDUM_R77.md`, freeze commit `41e31e70ab`, printed in Table 15)

### AUX-R77-SWAP — registered wrong-index control (D2b)

Run 2026-08-24: mini, temperature 0, k=1, 1,322 sync calls (661 items x 2 manipulated arms),
**0 parse failures**, billed **$0.9069** against a $0.8937 projection and the $5 ceiling.
INTACT is the committed E1 `INDEXED-TRUE` arm, read via the same loader the X4 scorer uses
(`elicitation_main.json`), never re-elicited. Shuffle preserved byte length exactly on all
661 indexes (delta 0) and preserves column alignment, so only the number/name-to-category
correspondence changes. Derangement of all 40 personas, no fixed point. Source:
`r74/x7/x7_scores.json`, rows `r74/x7/rows_SWAP.jsonl`, cell `r74/x7/x7_cell.json`.

| Key | Arm | Judgment | n | pos | intact | manipulated | intact - manipulated | 95% CI |
|---|---|---|---:|---:|---:|---:|---:|---|
| **AUX-R77-SWAP-WP-FOK** | WRONG-PERSON | FOK | 307 | 35 | 0.7003 | **0.3631** | **+0.3383** | [+0.2169,+0.4506] |
| **AUX-R77-SWAP-WP-NOK** | WRONG-PERSON | NOK | 661 | 104 | 0.7339 | **0.4659** | **+0.2668** | [+0.2010,+0.3298] |
| **AUX-R77-SWAP-SH-FOK** | SHUFFLED | FOK | 307 | 35 | 0.7003 | 0.7053 | -0.0031 | [-0.0546,+0.0499] |
| **AUX-R77-SWAP-SH-NOK** | SHUFFLED | NOK | 661 | 104 | 0.7339 | 0.7116 | +0.0217 | [-0.0178,+0.0611] |

**Registered verdicts.**
- **SW-1 HOLDS** on both judgments: replacing the index with another persona's costs the
  monitor its entire advantage, and on FOK drives it below chance (0.3631) — the wrong index
  actively misleads rather than merely failing to help.
- **SW-2 FAILS** on both judgments: permuting which counts and which attribute-name lists
  belong to which category changes nothing.
- **SW-3 adverse branch fired** on `SHUFFLED/fok` and `SHUFFLED/nok`; integration was held
  and then **ruled** (ADDENDUM_R77 §S post-result ruling, 2026-08-24). SW-1 prints at full
  strength as the store-specificity result; SW-2 prints as a **mechanism bound**, never as a
  failure of store specificity, and its scope-limit sentence travels with it verbatim. The
  frozen SW-3 sentence is retained in the registration marked
  NOT-APPLICABLE-TO-THIS-PATTERN and does **not** print (D-R74-19).

**Scope limit that must travel with the SHUFFLED null (do not drop).** The SHUFFLED arm
permutes the per-category count rows and the per-category attribute-name lists. It does
**not** touch the flat `ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT` section, and it
preserves the global multiset of names and counts. Its null therefore shows that the
**per-category correspondence** is not load-bearing; it does **not** show that the name
material or the superseded-names section is irrelevant, and it is consistent with a monitor
that checks whether a question-matching name appears anywhere in the index and whether it is
flagged superseded.

### AUX-R77-POSTERIOR — the presence-control posterior (D6)

Deterministic arithmetic on the committed `e1_metamemory/two_channel_control.json`; no
sampling, no seed, **no interval** (census class, as `AUX-R76-AVCENSUS`). Combined recall
**0.9950248756**, so ε = **0.0049751244**. Routing verdicts: ABSENT **21**, PRESENT **220**,
UNRESOLVED 554. At specificity 1 (a truly absent target cannot be found), implied truly
present among the 241 resolved = 220/0.995 = **221.10**, base rate **0.917**, of which
**1.10** are missed into the 21 ABSENT verdicts.

| Key | Quantity | Value |
|---|---|---|
| **AUX-R77-POSTERIOR** | P(present \| check claimed ABSENT) | **0.052** (5.2%), against ε = 0.005 — **~10× larger**; ε is a miss rate conditional on presence, not a posterior |
| **AUX-R77-BASERATE** | P(present) among resolved targets | **0.917** |

The manuscript previously stated the posterior as "at most 0.5%". The honest value is larger
and prints; every dependent sentence was adjusted (§4.2 and the App F presence-control line).

### AUX-R78-SWAP-GAP — endpoint-vs-delta bound for the flipped wrong-index table (R78, A2 Option 3)

Added at R78 under the A2 Option-3 pre-ruling (D-R74-20). Each printed Δ in the wrong-index
table is the committed paired-bootstrap mean (`score_e1.boot`: 1,000 item-level draws, seed
42, single-class draws discarded) — not the difference of the two displayed AUROC columns.
Deterministic arithmetic on the committed `r74/x7/x7_scores.json` fields (the D-R74-13
admissibility class; nothing re-run): max |delta_intact_minus_manipulated − (intact_auroc −
manipulated_auroc)| over the four cells = **0.0019** at 4dp (unrounded 0.001864, attained on
SHUFFLED/FOK), so the printed bound is **0.002**. paper_v2's table footnote prints the bound
and names the estimator; `verify_r74` re-derives the gap from the artifact.

| Key | Quantity | Value | Source |
|---|---|---:|---|
| **AUX-R78-SWAP-GAP** | max endpoint-vs-delta gap (4dp) / printed bound | **0.0019** / **0.002** | `r74/x7/x7_scores.json` |

## Do not use

| value | why |
|---|---|
| X3 call outputs (FOK/NOK values from the telemetry runs) | telemetry-only by registration; never scored, never reported |
| any "matched-84" blind/indexed/delta figure | NS-3 and NS-4 were struck before computation (ADDENDUM_R76 §A1); no such measurement exists and none may be created for this submission |
| AUX-R76-NS5-* as evidence about XV-1 | NS-5 reports, it does not test; XV-1's registered failed verdict stands |
