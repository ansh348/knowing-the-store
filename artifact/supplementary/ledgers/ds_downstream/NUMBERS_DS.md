# NUMBERS_DS — ledger for the downstream experiment DS

Registration: `registrations/ADDENDUM_DS.md` (frozen at `a5a2036`, R100, 2026-09-13; baseline `43a094c`).
Inherits `registrations/ADDENDUM_RESP.md` (frozen `17e6328`) — L2's retriever, populations and reach
row (`resp_review/NUMBERS_RESP.md` `AUX-RESP-L2-REACH`, RESP Phase B step 4 at `b08757c`). Every number
printed for DS enters the manuscript through a key in this file and no other way. Keys are reserved in
the registration's §L. Entries are dated. Deviations: `DEVIATIONS_DS.md` (D-DS-1, D-DS-2).

**State of this file.** Phase B started 2026-09-13 after the freeze and after RESP Phase B step 4
committed (`b08757c`) with `AUX-RESP-L2-REACH` present (the queued trigger); steps 1–6 committed one at a
time the same day; `tools/verify_ds.py` passes with every check A–G; `DEVIATIONS_DS.md` carries D-DS-1 and
D-DS-2. **Verdicts: DS-P1 FAILS (+0.4327, under 0.50; the retriever already reaches 0.5192); DS-P2 FAILS by
the weaker reading (ρ 0.7561; item-level [0.610, 0.872] holds, persona-clustered [0.563, 0.939] does not);
DS-P3 HOLDS (LOOKUP = MODEL, 0.8413 on the 63); DS-P4 FAILS (+0.0000); DS-P5 HOLDS (−0.0287). Stage 2
descriptive: stale use at TAU_HI 0 everywhere; at TAU_GOLD 5.7–13.4% with the record tagged against
22–37% untagged. Billed $0.1093 of the $2 line.**

---

## 1. Step 1 — the pre-artifact keys (written 2026-09-13; no model call)

### AUX-DS-PRECOND

`registrations/ADDENDUM_RESP.md` frozen at `17e6328` and byte-identical; RESP Phase B step 4 committed at
`b08757c` (an ancestor of HEAD); `resp_review/l2/retrieval.json` present; `AUX-RESP-L2-REACH` present in
`resp_review/NUMBERS_RESP.md`. ALWAYS reach recomputed from the five ids of `retrieval.json` and `pn_members`:
**54 of 104** = 0.5192 (ledgered 54 of 104; per state
sup 22 / 63, ret 20 / 26, exp 12 / 15) — equal. DS builds no retrieval and makes no embedding call.
**The instruction's 5% premise does not hold on this store (L2-P3 failed): the ALWAYS row is 0.5192, and DS-P1's
margin is narrowed accordingly (§C.7's second adverse branch).**

### AUX-DS-POP

661 items = 104 PN (63 supersession / 26 retraction / 15 expiry, `nb6_composition.AV_STATE`) + 174 PRESENT (all
easy tier) + 383 ABSENT (238 ablation, 145 natural-absent); the coverage population 307 = 272 ABSENT + 35 PN;
302 distinct questions. `r74/x4/cell_661.json` sha256 `01ed4c05fc57c0b2…`; joined as `common_e1r.assemble` joins.

### AUX-DS-FLAGCENSUS (D-DS-1)

Under `index_v2.true_lifecycle`, keyed by (persona, entry id): at least one `pn_members` entry flagged non-active
for **82 of 104** (sup 63 / 63, ret 8 / 26, exp 11 / 15); every `pn_members` entry flagged for 74.
The 22 unflagged: frbank:david:david_q06:CAT-ABLATED (exp), frbank:david:david_q06:FULL (exp), frbank:marcus:marcus_q10:CAT-ABLATED (exp), frbank:marcus:marcus_q10:FULL (exp), frbank:bruna:bruna_q06:CAT-ABLATED (ret), frbank:bruna:bruna_q06:FULL (ret), frbank:bruna:bruna_q06:SLOT-ABLATED (ret), frbank:dariush:dariush_q04:FULL (ret), frbank:dariush:dariush_q04:SLOT-ABLATED (ret), frbank:fatima:fatima_q06:FULL (ret), frbank:fatima:fatima_q06:SLOT-ABLATED (ret), frbank:ingrid:ingrid_q04:CAT-ABLATED (ret), frbank:ingrid:ingrid_q04:FULL (ret), frbank:ingrid:ingrid_q04:SLOT-ABLATED (ret), frbank:joonho:joonho_q04:FULL (ret), frbank:joonho:joonho_q04:SLOT-ABLATED (ret), frbank:mirri:mirri_q04:CAT-ABLATED (ret), frbank:rosa:rosa_q06:CAT-ABLATED (ret), frbank:rosa:rosa_q06:FULL (ret), frbank:rosa:rosa_q06:SLOT-ABLATED (ret), frbank:valentina:valentina_q04:FULL (ret), frbank:valentina:valentina_q04:SLOT-ABLATED (ret). ORACLE's ceiling is 0.7885 by construction (ruling of 2026-09-13).

### AUX-DS-NAMES

Renderer lock: `index_v2.render` on the item's store variant reproduces the committed TRUE text on **661 / 661**;
`index_v3.render_v3` asserts the v2 prefix on every one; no v3 name section at the cap. Own-name presence
(pn slots ∩ printed names): v2 superseded section 74 (sup 63 / ret 11 / exp 0);
v3 any section 94 (sup 63 / ret 19 / exp 12). Fetch sets reaching the forbidding record:
F(N2) 65 (63 / 2 / 0), F(N3) 82 (63 / 8 / 11), F(P) 82 (63 / 8 / 11).
Fetch-set sizes — F(N2) over the 661: zero 195, median 2, mean 2.84, p90 7, max 9; F(N3) over the 661: zero 12, median 9, mean 8.84, p90 16, max 23; F(P) over the 104 PN: zero 10, median 2, mean 2.64, p90 7, max 8
(the frozen §C.4 table's "22" in F(P)'s zero cell is D-DS-2; the zero count is 10).

### AUX-DS-THRESHOLDS

θ_NOK = 104 / 661 = 0.157337; θ_FOK = 35 / 307 = 0.114007 (probability at or above the population prior, ruling R1);
λ_NOK = the 75th-highest NB-6 score over the 661 = 0.242212; λ_FOK = the 125th-lowest NB-5 score over the 307 = 0.318141
(the matched budget, ruling R2); the literal rule (`LOOKUP-LIT`) uses θ_NOK / θ_FOK on the cosines, descriptive.

| gate | fires | PN | PRESENT | ABSENT |
|---|---:|---:|---:|---:|
| MODEL fetch (`nok ≥ θ_NOK`), 661 | 75 | 56 | 9 | 10 |
| MODEL abstain (`fok < θ_FOK`), 661 | 210 | 19 | 19 | 172 |
| MODEL abstain, 307 | 124 | 7 | — | 117 |
| LOOKUP fetch (`nb6 ≥ λ_NOK`), 661 | 77 | 53 | 6 | 18 |
| LOOKUP abstain (`nb5 < λ_FOK`), 661 | 224 | 22 | 28 | 174 |
| LOOKUP abstain, 307 | 124 | 9 | — | 115 |
| LOOKUP-LIT fetch (`nb6 ≥ θ_NOK`), 661 | 184 | 68 | 37 | 79 |
| LOOKUP-LIT abstain (`nb5 < θ_FOK`), 661 | 0 | 0 | — | 0 |

### AUX-DS-LOOKUP-GATE

`run_nb6.emb_scores` on the committed TRUE index texts: NB-6 (superseded section) **0.7484** on the 661
(committed 0.7484), NB-5 (whole name map) **0.6186** on the 307 (committed 0.6186) — **gate PASS at four decimals**.

---

## 2. Step 2 — policies, views, Stage 1 (written 2026-09-13; no model call)

### AUX-DS-LINELOCK

The five retrieved lines of every view are L2's rendered block byte for byte (`resp_review/l2/retrieval.json`); fetched
lines are rendered by the same function (`resp_common.render_line`) — 685 fetched lines whose entry also
appears in some L2 block match that block's line byte for byte after the rank label; no active entry in any fetch set;
gold entries of PRESENT items in a fetch set: 0 .
`verify_ds.py` check F re-derives every policy, view and Stage 1 flag.

### AUX-DS-POLICIES and AUX-DS-VIEWSIZE

| policy | gate fires (661) | abstentions (661) | mean view size, 661 | max | mean view size, 104 PN | max |
|---|---:|---:|---:|---:|---:|---:|
| ALWAYS | 0 | 0 | 5.00 | 5 | 5.00 | 5 |
| ORACLE | 104 | 383 | 5.33 | 13 | 7.07 | 13 |
| MODEL | 75 | 210 | 5.43 | 14 | 7.08 | 13 |
| LOOKUP | 77 | 224 | 5.46 | 14 | 6.88 | 13 |
| MODEL-ALL | 75 | 210 | 6.16 | 27 | 10.74 | 27 |
| LOOKUP-ALL | 77 | 224 | 6.26 | 27 | 10.36 | 27 |
| LOOKUP-LIT | 184 | 0 | 6.02 | 14 | 7.42 | 13 |

### AUX-DS-REACH — Stage 1 PN reach per policy (by id; tagged reach and successor-in-view beside)

| policy | gate fires | abstentions | PN reach all (Wilson) | sup | ret | exp | tagged all | successor in view (all) | PN abstained |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|
| ALWAYS | 0 | 0 | **54 / 104 = 0.5192** [0.424, 0.613] | 22 / 63 | 20 / 26 | 12 / 15 | 35 | 13 | 0 |
| ORACLE | 104 | 383 | **99 / 104 = 0.9519** [0.892, 0.979] | 63 / 63 | 22 / 26 | 14 / 15 | 82 | 13 | 0 |
| MODEL | 75 | 210 | **85 / 104 = 0.8173** [0.732, 0.880] | 53 / 63 | 20 / 26 | 12 / 15 | 66 | 13 | 19 |
| LOOKUP | 77 | 224 | **85 / 104 = 0.8173** [0.732, 0.880] | 53 / 63 | 20 / 26 | 12 / 15 | 66 | 13 | 22 |
| MODEL-ALL | 75 | 210 | **85 / 104 = 0.8173** [0.732, 0.880] | 53 / 63 | 20 / 26 | 12 / 15 | 66 | 13 | 19 |
| LOOKUP-ALL | 77 | 224 | **85 / 104 = 0.8173** [0.732, 0.880] | 53 / 63 | 20 / 26 | 12 / 15 | 66 | 13 | 22 |
| LOOKUP-LIT | 184 | 0 | **94 / 104 = 0.9038** [0.832, 0.947] | 62 / 63 | 20 / 26 | 12 / 15 | 75 | 13 | 0 |

ORACLE's flagged ceiling: 82 / 104 (D-DS-1). Tagged reach = the record in view *and* printed non-active.

**DS-P1** (ORACLE − ALWAYS on the 104 > 0.50): 0.9519 − 0.5192 = **+0.4327** (item-level [+0.3365, +0.5288]; persona-clustered [+0.2815, +0.5680]) → **FAILS**. Frozen text with its numbers:
> Fetching the store's lifecycle records for the obligation's own attribute, on gold labels, puts the forbidding record in the view for 99 of the 104 obligations against 54 for the five-entry similarity view alone, a difference of +0.4327 (interval [+0.3365, +0.5288]; persona-clustered [+0.2815, +0.5680]) that does not exceed 0.50. Either the retrieved view already carries the record for most obligations, or the store's metadata does not flag it: the truthful join marks the forbidding record non-active for 82 of 104 (8 of 26 retraction-derived, 11 of 15 expiry-derived), and no fetch by lifecycle state reaches the other 22. Acting on a perfect obligation judgment reaches 0.9519 on this store, not one.

**DS-P2** (ρ = (MODEL − ALWAYS) / (ORACLE − ALWAYS) on the 63 supersession-derived items ≥ 0.60 with the item-level interval's lower bound > 0.60; clustered beside, weaker governs): ALWAYS 0.3492, MODEL 0.8413, ORACLE 1.0000; **ρ = 0.7561**, item-level [0.6097, 0.8718] (1000 draws, 0 discarded), persona-clustered [0.5625, 0.9394] (1000 draws, 0 discarded); the gate fires on 31 of the 41 supersession items the retriever misses; item-level reading holds, clustered reading fails → **FAILS**. Frozen text with its numbers:
> On the 63 supersession-derived obligations, where every forbidding record is flagged and named, gating the fetch on the smallest model's committed obligation score at its base rate puts the record in view for 0.8413, against 0.3492 under retrieval alone and 1.0000 under gold labels, retaining 0.7561 of the oracle gain with interval [0.6097, 0.8718] (persona-clustered [0.5625, 0.9394]) that does not exclude 0.60 from below. The gate fires on 31 of the 41 supersession-derived obligations the retriever misses; the summary supports the judgment, and the judgment at this threshold does not carry it into the view. The item-level and the persona-clustered intervals disagree on this prediction; the weaker reading governs.

**DS-P3** (|LOOKUP − MODEL| on the same 63 ≤ 0.05): LOOKUP 0.8413, MODEL 0.8413, **D = +0.0000** ([-0.0794, +0.0794]; [-0.0938, +0.1035]); on the 104: 0.8173 vs 0.8173, +0.0000 ([-0.0481, +0.0481]; [-0.0594, +0.0612]) → **HOLDS**. Frozen text with its numbers:
> The superseded-names lookup, at the same fetch budget, puts the record in view within tolerance of the model's gate (0.8413 against 0.8413 on the 63, +0.0000, interval [-0.0794, +0.0794]; persona-clustered [-0.0938, +0.1035]): on the state the summary names, the gate can be a lookup.

**DS-P4** (MODEL-ALL − MODEL on the 41 retraction- and expiry-derived items > 0.20): MODEL-ALL 0.7805, MODEL 0.7805, **D = +0.0000** ([+0.0000, +0.0000]; [+0.0000, +0.0000]); newly fetchable under v3: 17, of which the gate fires on 0 that the retriever misses → **FAILS**. Frozen text with its numbers:
> Naming the retracted and expired attributes in the summary makes their records fetchable, and the gate elicited under the counting summary reaches them for 0.7805 against 0.7805 under the superseded-only names, a difference of +0.0000 (interval [+0.0000, +0.0000]; persona-clustered [+0.0000, +0.0000]) that does not exceed 0.20 on the 41 retraction- and expiry-derived obligations. Of the 41, 19 carry a flagged record; naming makes 17 of them fetchable that the superseded-only names do not, and the gate fires on 0 of those. The bound on these states is the judgment, not the naming.

### AUX-DS-PRESENT — coverage on the 174 PRESENT items

| policy | coverage (gold in view ∧ not abstained) | rate (Wilson) | gold in view | abstained | abstained with gold in view |
|---|---:|---|---:|---:|---:|
| ALWAYS | 65 / 174 | 0.3736 [0.305, 0.447] | 65 | 0 | 0 |
| ORACLE | 65 / 174 | 0.3736 [0.305, 0.447] | 65 | 0 | 0 |
| MODEL | 60 / 174 | 0.3448 [0.278, 0.418] | 65 | 19 | 5 |
| LOOKUP | 56 / 174 | 0.3218 [0.257, 0.394] | 65 | 28 | 9 |
| MODEL-ALL | 60 / 174 | 0.3448 [0.278, 0.418] | 65 | 19 | 5 |
| LOOKUP-ALL | 56 / 174 | 0.3218 [0.257, 0.394] | 65 | 28 | 9 |
| LOOKUP-LIT | 65 / 174 | 0.3736 [0.305, 0.447] | 65 | 0 | 0 |

The fetch adds no active record, so gold-in-view is the same under every policy; coverage differs only through abstention (§C.7).

**DS-P5** (|MODEL − ALWAYS| coverage ≤ 0.05): ALWAYS 0.3736, MODEL 0.3448, **D = -0.0287** ([-0.0519, -0.0057]; [-0.0680, -0.0050]); MODEL abstains on 19 PRESENT items, 5 with the licensed record in the five → **HOLDS**. Frozen text with its numbers:
> The gate does not cost coverage: on the 174 items whose licensed record the store holds, coverage under the gated policy is within tolerance of retrieval alone (0.3448 against 0.3736, -0.0287, interval [-0.0519, -0.0057]; persona-clustered [-0.0680, -0.0050]).

### AUX-DS-ABSTAIN — abstention on ABSENT items (descriptive)

| policy | abstain on the 383 ABSENT | rate | on the 272 ABSENT of the coverage population | rate | PN abstained (104) |
|---|---:|---:|---:|---:|---:|
| ALWAYS | 0 | 0.0000 | 0 | 0.0000 | 0 |
| ORACLE | 383 | 1.0000 | 272 | 1.0000 | 0 |
| MODEL | 172 | 0.4491 | 117 | 0.4301 | 19 |
| LOOKUP | 174 | 0.4543 | 115 | 0.4228 | 22 |
| MODEL-ALL | 172 | 0.4491 | 117 | 0.4301 | 19 |
| LOOKUP-ALL | 174 | 0.4543 | 115 | 0.4228 | 22 |
| LOOKUP-LIT | 0 | 0.0000 | 0 | 0.0000 | 0 |

---

## 3. Step 3 — the answer prompt (written 2026-09-13; no model call)

### AUX-DS-PROMPT

`tools/prompts_ds.py` carries the two §D.4 texts verbatim (equal, byte for byte, to the fenced blocks of the frozen
`registrations/ADDENDUM_DS.md`; `verify_ds.py` check E extracts and compares them). `prompts_e1.py` untouched
(digests as pinned). The same prompt under every policy; only the view changes.

| text | sha256 |
|---|---|
| `SYSTEM_ANSWER` | `af1c69c8817d286727e44027a9d469c875a4da1eb111d7351eb76094b48ea4a9` |
| `USER_ANSWER` | `c6dd6926a3c9e8d44d7d5a480540c554dbec510101c8c39e616a8c77299d83a5` |


---

## 4. Steps 4–6 — Stage 2, the answer calls, scored (written 2026-09-13)

### AUX-DS-STAGE2

Lane `gpt-4.1-mini` (served identifier probed, `run/probes_ds.json`), temperature 0, seed 42, max_tokens 200, JSON mode,
one retry on a parse failure. **422 distinct (item, view) calls** for 1391 nominal
(policy, item) pairs (225 PN views, 197 PRESENT views); rows 422, failures 0.
Scoring: the committed detector (`e0_common` / `index_v2.detect`) on the `answer` string, persona-name tokens dropped:
stale use = `detect(stale, successor)` ≥ TAU_HI 0.80 (cross-guarded; expiry: the expired fact's tokens at TAU_HI, no
successor); stale surfacing = unguarded coverage ≥ 0.80; successor use (supersession) = `detect(successor, stale)` ≥ 0.80;
both = both coverages ≥ 0.80 unguarded; PRESENT correctness = gold-field coverage ≥ TAU_GOLD 0.50 (TAU_HI beside).
Abstained items are reported as abstained, never pooled. **Reading note (descriptive):** TAU_HI 0.80 was calibrated on entry
texts; on a two-sentence answer the stale value's unique tokens are paraphrased (coverage 0.5–0.67 on the answers that give
the stale value as the answer), so the registered TAU_HI row reads zero everywhere and the TAU_GOLD row beside it is the
sensitive one; the tagged / untagged split of that row is where the tag's effect shows.

| policy | PN reached ∧ answered | PN abstained | stale use (all) | stale use, tagged reach | stale use, untagged reach | stale surfacing | stale use at TAU_GOLD (all) | at TAU_GOLD, tagged | at TAU_GOLD, untagged | successor use (of supersession) | both | PRESENT answered | PRESENT correct (TAU_GOLD) | at TAU_HI |
|---|---:|---:|---|---|---|---:|---|---|---|---|---:|---:|---|---:|
| ALWAYS | 54 | 0 | 0 / 54 = 0.0000 | 0 / 35 = 0.0000 | 0 / 19 = 0.0000 | 0 | 9 / 54 = 0.1667 | 2 / 35 = 0.0571 | 7 / 19 = 0.3684 | 1 / 22 = 0.0455 | 0 | 174 | 46 / 174 = 0.2644 | 14 |
| ORACLE | 99 | 0 | 0 / 99 = 0.0000 | 0 / 82 = 0.0000 | 0 / 17 = 0.0000 | 0 | 17 / 99 = 0.1717 | 11 / 82 = 0.1341 | 6 / 17 = 0.3529 | 1 / 63 = 0.0159 | 0 | 174 | 46 / 174 = 0.2644 | 14 |
| MODEL | 74 | 19 | 0 / 74 = 0.0000 | 0 / 61 = 0.0000 | 0 / 13 = 0.0000 | 0 | 9 / 74 = 0.1216 | 5 / 61 = 0.0820 | 4 / 13 = 0.3077 | 1 / 49 = 0.0204 | 0 | 155 | 44 / 155 = 0.2839 | 14 |
| LOOKUP | 70 | 22 | 0 / 70 = 0.0000 | 0 / 61 = 0.0000 | 0 / 9 = 0.0000 | 0 | 7 / 70 = 0.1000 | 5 / 61 = 0.0820 | 2 / 9 = 0.2222 | 1 / 50 = 0.0200 | 0 | 146 | 40 / 146 = 0.2740 | 12 |
| MODEL-ALL | 74 | 19 | 0 / 74 = 0.0000 | 0 / 61 = 0.0000 | 0 / 13 = 0.0000 | 0 | 9 / 74 = 0.1216 | 5 / 61 = 0.0820 | 4 / 13 = 0.3077 | 1 / 49 = 0.0204 | 0 | 155 | 44 / 155 = 0.2839 | 14 |
| LOOKUP-ALL | 70 | 22 | 0 / 70 = 0.0000 | 0 / 61 = 0.0000 | 0 / 9 = 0.0000 | 0 | 6 / 70 = 0.0857 | 4 / 61 = 0.0656 | 2 / 9 = 0.2222 | 1 / 50 = 0.0200 | 0 | 146 | 39 / 146 = 0.2671 | 12 |

Per state (stale use / answered): ALWAYS: sup 0/22, ret 0/20, exp 0/12; ORACLE: sup 0/63, ret 0/22, exp 0/14; MODEL: sup 0/49, ret 0/13, exp 0/12; LOOKUP: sup 0/50, ret 0/8, exp 0/12; MODEL-ALL: sup 0/49, ret 0/13, exp 0/12; LOOKUP-ALL: sup 0/50, ret 0/8, exp 0/12.

### AUX-DS-SPEND and AUX-DS-BUDGETRULE

Billed on the OpenAI key from response usage at $0.40 / $1.60 per 1M: probe $0.0002, run $0.1091 — **total
$0.1093**, under the $2 line (yes) and the $4 rule (yes). Nothing on the Anthropic key; no Haiku,
no Opus; no embedding call; no monitor elicited. Projection before launch: `run/projection_ds.json`.

---

## 5. The frozen Section 7 paragraph, assembled from the verdicts (written 2026-09-13)

### AUX-DS-PARAGRAPH

`registrations/ADDENDUM_DS.md` §PAPER, each bracket resolved to its held or failed form by the verdicts of §2
(DS-P1 failed, DS-P2 failed, DS-P3 held, DS-P4 failed, DS-P5 held) and the numbers of §2 and §4; the last
sentence's $S$ is filled with the registered TAU_HI count on ORACLE's tagged-reach population, with the TAU_GOLD
reading and the untagged reading beside it as §D.4 provides. Replaces C150 and C151 (`paper_v8.tex:733-734`)
under the author's authorization block; `M` and `L` are the 104-item reach rates (on the 63 supersession-derived
items both are 0.8413, DS-P3's registered quantity).

> Acting on the obligation judgment changes what a bounded view carries. The store's truthful metadata flags $82$ of the $104$ forbidding records; the other $22$ ($18$ retraction-derived, $4$ expiry-derived) are a store-side fact of the kind Table~\ref{tab:believed} records, retrieve as active, and are out of reach of any policy that acts on the metadata. On the $104$ obligation items, the five-entry similarity view contains the forbidding record for $0.5192$; a gold-label fetch of the store's lifecycle records for the obligation's own attribute reaches $0.9519$, $0.4327$ above retrieval alone and short of the $0.50$ bar; gated on the smallest model's committed obligation score at its base rate, the fetch reaches $0.8173$, retaining $0.7561$ of that gain on the supersession-derived items (interval $[0.610, 0.872]$; persona-clustered $[0.562, 0.939]$), short of the $60\%$ bar under the weaker reading. The superseded-names lookup reaches $0.8173$ at the same fetch budget, within tolerance of the model. Naming the retracted and expired attributes raises the gated reach on those obligations only from $0.7805$ to $0.7805$: the gate elicited under the counting summary does not fire on them. The coverage gate at its base rate costs $0.0287$ of coverage on the items whose licensed record the store holds, within tolerance. With the forbidding record in view and tagged, the smallest model gives the stale value as the answer in $0$ of $82$ cases at the registered detector threshold ($11$ of $82$ at the join's gold threshold; $6$ of $17$ where the record printed as active) (Appendix~\ref{app:resp}).

### AUX-DS-PARAGRAPH-PRINTED (written 2026-09-13, R101)

The Section 7 form of `AUX-DS-PARAGRAPH` as `paper_v9.tex` prints it: the one interval placeholder of the frozen
text carries the item-level interval first and the interval grouped by user profile beside it in the manuscript's
idiom (`with questions grouped by user profile`) in place of the ledger's `persona-clustered`; every number is the
paragraph's. Verbatim:

> Acting on the obligation judgment changes what a bounded view carries. The store's truthful metadata flags $82$ of the $104$ forbidding records; the other $22$ ($18$ retraction-derived, $4$ expiry-derived) are a store-side fact of the kind Table~\ref{tab:believed} records, retrieve as active, and are out of reach of any policy that acts on the metadata. On the $104$ obligation items, the five-entry similarity view contains the forbidding record for $0.5192$; a gold-label fetch of the store's lifecycle records for the obligation's own attribute reaches $0.9519$, $0.4327$ above retrieval alone and short of the $0.50$ bar; gated on the smallest model's committed obligation score at its base rate, the fetch reaches $0.8173$, retaining $0.7561$ of that gain on the supersession-derived items (interval $[0.610, 0.872]$; $[0.562, 0.939]$ with questions grouped by user profile), short of the $60\%$ bar under the weaker reading. The superseded-names lookup reaches $0.8173$ at the same fetch budget, within tolerance of the model. Naming the retracted and expired attributes raises the gated reach on those obligations only from $0.7805$ to $0.7805$: the gate elicited under the counting summary does not fire on them. The coverage gate at its base rate costs $0.0287$ of coverage on the items whose licensed record the store holds, within tolerance. With the forbidding record in view and tagged, the smallest model gives the stale value as the answer in $0$ of $82$ cases at the registered detector threshold ($11$ of $82$ at the join's gold threshold; $6$ of $17$ where the record printed as active) (Appendix~\ref{app:resp}).

Followed, as authorized under D-DS-3 (a), by: "The two failed bars were fixed before the study measured the retrieval premise they rest on; the mechanism numbers stand and the bars are printed as set."

---

## 6. Amendment 1 — the fetch gate elicited under the all-states summary (descriptive; D-DS-3 (b) repair; written 2026-09-13, R103)

Registration `registrations/ADDENDUM_DS_AMENDMENT_1.md`, frozen sha256 `72ab84dae2c7e464b1488570d4098aebf59b1de0d442ddc7b6f79a57bfcbbcf5` before the first call (copy in
`iclr2027_monitoring_submission/ARTIFACT/registrations/`). **Descriptive: no bar, no prediction, no verdict; DS-P4 stands as FAILS.**
Sources: `run/lock_amend1.json`, `run/probes_amend1.json`, `run/projection_amend1.json`, `run/elicitation_v3_amend1.json`,
`run/stage1_amend1.json`, `run/projection_stage2_amend1.json`, `run/rows_ds_amend1.jsonl`, `run/scores_amend1.json`. Nothing
registered was written.

### AUX-DS-A1-LOCK, AUX-DS-A1-PROBE, AUX-DS-A1-PROJECTION

Renderer lock 661 / 661 v2 prefixes byte-identical to the committed TRUE text; population 661 / 104 = 63 / 26 / 15; 174 PRESENT; 383 ABSENT; counted-state items 41,
newly fetchable under the v3 names 17; θ_NOK 0.157337. Served `gpt-4.1-mini-2025-04-14` (identifier ok: True), 1636 in /
24 out on a 67-line v3 summary. Projection: 661 elicitation calls $0.4490, Stage 2 upper bound
278 calls $0.0620, total $0.5111 (x1.3 $0.6644) against the combined $3.00 cap.

### AUX-DS-A1-V3ROW — mini's obligation score under the all-states summary, the row §C.4 said did not exist

Lane `gpt-4.1-mini`, temperature 0, seed 42, max_tokens 200, JSON mode, k = 1, one retry on a parse failure; 661 rows,
0 failures. NOK AUROC on the 661: **0.7354** under the all-states summary against 0.7339 committed under the
superseded-only summary, paired difference +0.0015 (item-level [-0.0385, +0.0494]; persona-clustered
[-0.0473, +0.0503]); `nok` takes 12 distinct values. Per state (positives of one state against the 557 negatives):
expiry 0.3770 against 0.5110 (paired [-0.2779, +0.0144]); retraction 0.5941 against 0.5638 (paired [-0.0615, +0.1418]); supersession 0.8790 against 0.8572 (paired [-0.0229, +0.0711]).
FOK under the v3 summary on the 307 (descriptive, unused by any gate): 0.7224.

### AUX-DS-A1-GATE — `nok3 ≥ θ_NOK`, by label and state, beside the committed gate (75 = 56 / 9 / 10)

Fires on **110** of 661: PN 63 / PRESENT 22 / ABSENT 25; by state sup 51 of 63,
ret 11 of 26, exp 1 of 15. Agreement with the committed v2 gate: both fire 65, v3 only
45, v2 only 10. Abstention is the committed coverage gate (210 abstentions, 19 on PN), unchanged.

### AUX-DS-A1-REACH, -PRESENT, -ABSTAIN, -VIEWSIZE — Stage 1 for MODEL-ALL-V3 (the AUX-DS-REACH row format)

| policy | gate fires | abstentions | PN reach all (Wilson) | sup | ret | exp | tagged all | successor in view (all) | PN abstained |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|
| MODEL-ALL-V3 | 110 | 210 | **89 / 104 = 0.8558** [0.776, 0.911] | 54 / 63 | 22 / 26 | 13 / 15 | 72 | 13 | 19 |

PRESENT coverage 60 / 174 = 0.3448 [0.278, 0.418] (gold in view 65, abstained 19); ABSENT abstention
172 / 383 and 117 / 272; view size mean 6.65 on the 661 (max 27), 11.42 on the 104 (max 27).

### AUX-DS-A1-P4DESC — the DS-P4 quantity under the v3-elicited gate (descriptive; the verdict is not re-adjudicated)

On the 41 retraction- and expiry-derived obligations: ALWAYS 0.7805, MODEL 0.7805, **MODEL-ALL-V3 0.8537**, ORACLE
0.8780; MODEL-ALL-V3 − MODEL = **+0.0732** (item-level [+0.0000, +0.1707]; persona-clustered
[+0.0000, +0.1875]). Of the 17 records naming makes fetchable, the v3 gate fires on **5** (3 of them ones the
retriever misses) and 16 are reached. On the 104: MODEL-ALL-V3 0.8558 against MODEL 0.8173, +0.0385
(item-level [-0.0096, +0.0962]; persona-clustered [-0.0206, +0.0981]).

### AUX-DS-A1-STAGE2 — the answer stage for MODEL-ALL-V3

Stage 2 population 233 distinct (item, view) pairs: 212 answered by a registered policy's byte-identical view (the recorded answer
is read; `ds_downstream/cache` is not written), 21 new calls (7 PN, 14 PRESENT), prompts_ds verbatim, the committed detector as §D.4.

| policy | PN reached ∧ answered | PN abstained | stale use (all) | tagged | untagged | stale surfacing | stale use at TAU_GOLD (all) | tagged | untagged | successor use (of supersession) | both | PRESENT answered | correct (TAU_GOLD) | at TAU_HI |
|---|---:|---:|---|---|---|---:|---|---|---|---|---:|---:|---|---:|
| MODEL-ALL-V3 | 78 | 19 | 0 / 78 = 0.0000 | 0 / 67 = 0.0000 | 0 / 11 = 0.0000 | 0 | 12 / 78 = 0.1538 | 10 / 67 = 0.1493 | 2 / 11 = 0.1818 | 1 / 50 = 0.0200 | 0 | 155 | 44 / 155 = 0.2839 | 14 |

Per state (stale use at TAU_HI / at TAU_GOLD / answered): sup 0 / 5 / 50; ret 0 / 6 / 15;
exp 0 / 1 / 13.

### AUX-DS-A1-SPEND

Billed from response usage at $0.40 / $1.60 per 1M: probe $0.0007, elicitation $0.4489 (0 served from cache), Stage 2 $0.0083
— **total $0.4579** against the combined $3.00 cap shared with the Q4 probe. No Haiku, no Opus, no embedding call.

---

## 7. Amendment 2 — the answer stage of the literal-threshold lookup rule (LOOKUP-LIT), and Haiku 4.5 as a second answerer (descriptive; written 2026-09-14, R106)

Registration `registrations/ADDENDUM_DS_AMENDMENT_2.md`, frozen sha256 `a3ff9d89c7b330d1243bc50d9b619b8497239f7f3757cb59816cf2e17fe3bdec` before the first call
(recorded here on 2026-09-14 before any call of the amendment; copy in `iclr2027_monitoring_submission/ARTIFACT/registrations/`). **Descriptive: no bar, no prediction,
no verdict; DS-P1 to DS-P5 stand.** Sources: `run/lock_amend2.json`, `run/probes_amend2.json`, `run/projection_amend2.json`, `run/rows_ds_amend2.jsonl`,
`run/rows_ds_amend2_h45.jsonl`, `run/scores_amend2.json` (`tools/amend2_lit.py`). Nothing registered is written. The subsections below are appended by `amend2_lit.py score`.

### AUX-DS-A2-LOCK, AUX-DS-A2-POP, AUX-DS-A2-PROBE-MINI, AUX-DS-A2-PROBE-H45, AUX-DS-A2-PROJECTION

Registration sha256 holds; prompts_ds digests as AUX-DS-PROMPT; prompts_e1 digests as pinned. Population (section A2.2 / A2.4, reproduced): 268 nominal LOOKUP-LIT (item, view) pairs, 238 reuse a recorded answer, 30 new calls (6 PN / 24 PRESENT); Haiku 4.5 views 452.
Probe mini: served `gpt-4.1-mini-2025-04-14` (identifier ok: True), 727 in / 18 out on a 12-line view. Probe Haiku 4.5: served `claude-haiku-4-5-20251001` (506 in / 28 out, 7 lines); served `claude-haiku-4-5-20251001` (477 in / 33 out, 5 lines); served `claude-haiku-4-5-20251001` (1593 in / 57 out, 27 lines). Projection: mini 30 calls $0.0078 (total against the $4 rule $0.1258); Haiku 4.5 452 calls $0.3744 (x1.3 $0.4867 against the $5 line; runs: True).

### AUX-DS-A2-STAGE2-LIT — Stage 2 for LOOKUP-LIT under GPT-4.1 mini (the §D.4 protocol; the AUX-DS-STAGE2 columns)

30 new calls, 238 recorded answers reused; failures 0; PN abstained 0 (the rule never abstains).

| answerer, policy | PN reached ∧ answered | stale use (all) | stale use, tagged reach | stale use, untagged reach | stale surfacing | stale use at TAU_GOLD (all) | at TAU_GOLD, tagged | at TAU_GOLD, untagged | successor use (of supersession) | both | PRESENT answered | PRESENT correct (TAU_GOLD) | at TAU_HI |
|---|---:|---|---|---|---:|---|---|---|---|---:|---:|---|---:|
| GPT-4.1 mini, LOOKUP-LIT | 94 | 0 / 94 = 0.0000 | 0 / 75 = 0.0000 | 0 / 19 = 0.0000 | 0 | 14 / 94 = 0.1489 | 7 / 75 = 0.0933 | 7 / 19 = 0.3684 | 1 / 62 = 0.0161 | 0 | 174 | 46 / 174 = 0.2644 | 14 |

Per state (stale use at TAU_HI / at TAU_GOLD / answered): sup 0 / 6 / 62; ret 0 / 7 / 20; exp 0 / 1 / 12.

### AUX-DS-A2-STAGE2-H45 — Stage 2 under Claude Haiku 4.5, every policy (rows 452, failed 0, served ['claude-haiku-4-5-20251001']; temperature 0, max_tokens 200, k = 1)

| answerer, policy | PN reached ∧ answered | stale use (all) | stale use, tagged reach | stale use, untagged reach | stale surfacing | stale use at TAU_GOLD (all) | at TAU_GOLD, tagged | at TAU_GOLD, untagged | successor use (of supersession) | both | PRESENT answered | PRESENT correct (TAU_GOLD) | at TAU_HI |
|---|---:|---|---|---|---:|---|---|---|---|---:|---:|---|---:|
| Haiku 4.5, ALWAYS | 54 | 7 / 54 = 0.1296 | 6 / 35 = 0.1714 | 1 / 19 = 0.0526 | 7 | 19 / 54 = 0.3519 | 8 / 35 = 0.2286 | 11 / 19 = 0.5789 | 0 / 22 = 0.0000 | 0 | 174 | 48 / 174 = 0.2759 | 14 |
| Haiku 4.5, ORACLE | 99 | 9 / 99 = 0.0909 | 7 / 82 = 0.0854 | 2 / 17 = 0.1176 | 9 | 27 / 99 = 0.2727 | 17 / 82 = 0.2073 | 10 / 17 = 0.5882 | 1 / 63 = 0.0159 | 0 | 174 | 48 / 174 = 0.2759 | 14 |
| Haiku 4.5, MODEL | 74 | 9 / 74 = 0.1216 | 8 / 61 = 0.1311 | 1 / 13 = 0.0769 | 9 | 23 / 74 = 0.3108 | 15 / 61 = 0.2459 | 8 / 13 = 0.6154 | 1 / 49 = 0.0204 | 0 | 155 | 45 / 155 = 0.2903 | 15 |
| Haiku 4.5, LOOKUP | 70 | 7 / 70 = 0.1000 | 7 / 61 = 0.1148 | 0 / 9 = 0.0000 | 7 | 19 / 70 = 0.2714 | 14 / 61 = 0.2295 | 5 / 9 = 0.5556 | 1 / 50 = 0.0200 | 0 | 146 | 41 / 146 = 0.2808 | 14 |
| Haiku 4.5, MODEL-ALL | 74 | 5 / 74 = 0.0676 | 4 / 61 = 0.0656 | 1 / 13 = 0.0769 | 5 | 20 / 74 = 0.2703 | 12 / 61 = 0.1967 | 8 / 13 = 0.6154 | 1 / 49 = 0.0204 | 0 | 155 | 45 / 155 = 0.2903 | 14 |
| Haiku 4.5, LOOKUP-ALL | 70 | 5 / 70 = 0.0714 | 5 / 61 = 0.0820 | 0 / 9 = 0.0000 | 5 | 18 / 70 = 0.2571 | 13 / 61 = 0.2131 | 5 / 9 = 0.5556 | 1 / 50 = 0.0200 | 0 | 146 | 40 / 146 = 0.2740 | 12 |
| Haiku 4.5, LOOKUP-LIT | 94 | 10 / 94 = 0.1064 | 9 / 75 = 0.1200 | 1 / 19 = 0.0526 | 10 | 29 / 94 = 0.3085 | 18 / 75 = 0.2400 | 11 / 19 = 0.5789 | 1 / 62 = 0.0161 | 0 | 174 | 47 / 174 = 0.2701 | 16 |

Per state under Haiku 4.5 (stale use at TAU_HI / at TAU_GOLD / answered): ALWAYS: sup 2 / 3 / 22, ret 1 / 8 / 20, exp 4 / 8 / 12 · ORACLE: sup 3 / 10 / 63, ret 2 / 9 / 22, exp 4 / 8 / 14 · MODEL: sup 5 / 11 / 49, ret 1 / 5 / 13, exp 3 / 7 / 12 · LOOKUP: sup 3 / 9 / 50, ret 0 / 2 / 8, exp 4 / 8 / 12 · MODEL-ALL: sup 1 / 8 / 49, ret 1 / 5 / 13, exp 3 / 7 / 12 · LOOKUP-ALL: sup 1 / 8 / 50, ret 0 / 2 / 8, exp 4 / 8 / 12 · LOOKUP-LIT: sup 5 / 13 / 62, ret 1 / 8 / 20, exp 4 / 8 / 12.

### AUX-DS-A2-SPEND

Probe mini $0.0003; probe Haiku $0.0032; mini lane $0.0084; Haiku lane $0.4023; **total $0.4141** (the Haiku lane against the author's $5 line; the mini lane under the DS $4 rule).

---

## 8. Amendment 3 — the answer stage once more, with an instruction to treat tagged records as not to be used (descriptive; written 2026-09-14, R107)

Registration `registrations/ADDENDUM_DS_AMENDMENT_3.md`, frozen sha256 `eca19607629c03d122f0e0ac66c50c3068978dcecd3be35296191aa3e2f3bce1` before the first call
(recorded here on 2026-09-14 before any call of the amendment; copy in `iclr2027_monitoring_submission/ARTIFACT/registrations/`). **Descriptive: no bar, no prediction,
no verdict; DS-P1 to DS-P5 and Amendments 1 and 2 stand.** Sources: `run/lock_amend3.json`, `run/probes_amend3.json`, `run/projection_amend3.json`,
`run/rows_ds_amend3_mini.jsonl`, `run/rows_ds_amend3_h45.jsonl`, `run/scores_amend3.json` (`tools/amend3_instruct.py`). Nothing registered is written. The subsections below are appended by `amend3_instruct.py score`.

### AUX-DS-A3-LOCK, AUX-DS-A3-PROMPT, AUX-DS-A3-POP, AUX-DS-A3-PROBE-MINI, AUX-DS-A3-PROBE-H45, AUX-DS-A3-PROJECTION

Registration sha256 holds; `SYSTEM_ANSWER_A3` sha256 `3cca2c0b42bdcc8939a3878250967c229c5ae04b876fd58b90b882df92f6499f` (the D.4 system text with the added paragraph, sha256 `6ac9e20ce503c1c86229030f901e42c8e8102cfdde8c5c657a285955d34a87a9`, verbatim from section A3.2); `USER_ANSWER` as AUX-DS-PROMPT; prompts_e1 digests as pinned. Population 452 distinct (item, view) pairs (231 PN, 221 PRESENT), the 452 of Amendment 2's Haiku lane. Probe mini: served `gpt-4.1-mini-2025-04-14` (548 in / 19 out); probe Haiku 4.5: served `claude-haiku-4-5-20251001` (571 in / 28 out). Projection: mini $0.1196, Haiku $0.3382, sum with probes $0.4587 (x1.3 $0.5963) against the $2.00 line; runs: True.

### AUX-DS-A3-STAGE2-MINI — Stage 2 under GPT-4.1 mini with the added instruction, every policy (rows 452, failed 0, served ['gpt-4.1-mini']; temperature 0, k = 1)

| answerer, policy | PN reached ∧ answered | stale use (all) | stale use, tagged reach | stale use, untagged reach | stale surfacing | stale use at TAU_GOLD (all) | at TAU_GOLD, tagged | at TAU_GOLD, untagged | successor use (of supersession) | both | PRESENT answered | PRESENT correct (TAU_GOLD) | at TAU_HI |
|---|---:|---|---|---|---:|---|---|---|---|---:|---:|---|---:|
| GPT-4.1 mini + instruction, ALWAYS | 54 | 0 / 54 = 0.0000 | 0 / 35 = 0.0000 | 0 / 19 = 0.0000 | 0 | 10 / 54 = 0.1852 | 2 / 35 = 0.0571 | 8 / 19 = 0.4211 | 1 / 22 = 0.0455 | 0 | 174 | 47 / 174 = 0.2701 | 12 |
| GPT-4.1 mini + instruction, ORACLE | 99 | 0 / 99 = 0.0000 | 0 / 82 = 0.0000 | 0 / 17 = 0.0000 | 0 | 18 / 99 = 0.1818 | 11 / 82 = 0.1341 | 7 / 17 = 0.4118 | 1 / 63 = 0.0159 | 0 | 174 | 47 / 174 = 0.2701 | 12 |
| GPT-4.1 mini + instruction, MODEL | 74 | 0 / 74 = 0.0000 | 0 / 61 = 0.0000 | 0 / 13 = 0.0000 | 0 | 10 / 74 = 0.1351 | 6 / 61 = 0.0984 | 4 / 13 = 0.3077 | 0 / 49 = 0.0000 | 0 | 155 | 44 / 155 = 0.2839 | 12 |
| GPT-4.1 mini + instruction, LOOKUP | 70 | 0 / 70 = 0.0000 | 0 / 61 = 0.0000 | 0 / 9 = 0.0000 | 0 | 8 / 70 = 0.1143 | 6 / 61 = 0.0984 | 2 / 9 = 0.2222 | 0 / 50 = 0.0000 | 0 | 146 | 40 / 146 = 0.2740 | 10 |
| GPT-4.1 mini + instruction, MODEL-ALL | 74 | 2 / 74 = 0.0270 | 1 / 61 = 0.0164 | 1 / 13 = 0.0769 | 2 | 10 / 74 = 0.1351 | 6 / 61 = 0.0984 | 4 / 13 = 0.3077 | 1 / 49 = 0.0204 | 0 | 155 | 44 / 155 = 0.2839 | 12 |
| GPT-4.1 mini + instruction, LOOKUP-ALL | 70 | 1 / 70 = 0.0143 | 1 / 61 = 0.0164 | 0 / 9 = 0.0000 | 1 | 7 / 70 = 0.1000 | 5 / 61 = 0.0820 | 2 / 9 = 0.2222 | 1 / 50 = 0.0200 | 0 | 146 | 40 / 146 = 0.2740 | 10 |
| GPT-4.1 mini + instruction, LOOKUP-LIT | 94 | 0 / 94 = 0.0000 | 0 / 75 = 0.0000 | 0 / 19 = 0.0000 | 0 | 16 / 94 = 0.1702 | 8 / 75 = 0.1067 | 8 / 19 = 0.4211 | 0 / 62 = 0.0000 | 0 | 174 | 46 / 174 = 0.2644 | 12 |

Per state under GPT-4.1 mini + instruction (stale use at TAU_HI / at TAU_GOLD / answered): ALWAYS: sup 0 / 1 / 22, ret 0 / 8 / 20, exp 0 / 1 / 12 · ORACLE: sup 0 / 7 / 63, ret 0 / 10 / 22, exp 0 / 1 / 14 · MODEL: sup 0 / 5 / 49, ret 0 / 4 / 13, exp 0 / 1 / 12 · LOOKUP: sup 0 / 5 / 50, ret 0 / 2 / 8, exp 0 / 1 / 12 · MODEL-ALL: sup 1 / 5 / 49, ret 1 / 4 / 13, exp 0 / 1 / 12 · LOOKUP-ALL: sup 1 / 4 / 50, ret 0 / 2 / 8, exp 0 / 1 / 12 · LOOKUP-LIT: sup 0 / 7 / 62, ret 0 / 8 / 20, exp 0 / 1 / 12.

### AUX-DS-A3-STAGE2-H45 — Stage 2 under Claude Haiku 4.5 with the added instruction, every policy (rows 452, failed 0, served ['claude-haiku-4-5-20251001']; temperature 0, k = 1)

| answerer, policy | PN reached ∧ answered | stale use (all) | stale use, tagged reach | stale use, untagged reach | stale surfacing | stale use at TAU_GOLD (all) | at TAU_GOLD, tagged | at TAU_GOLD, untagged | successor use (of supersession) | both | PRESENT answered | PRESENT correct (TAU_GOLD) | at TAU_HI |
|---|---:|---|---|---|---:|---|---|---|---|---:|---:|---|---:|
| Claude Haiku 4.5 + instruction, ALWAYS | 54 | 3 / 54 = 0.0556 | 2 / 35 = 0.0571 | 1 / 19 = 0.0526 | 3 | 17 / 54 = 0.3148 | 5 / 35 = 0.1429 | 12 / 19 = 0.6316 | 0 / 22 = 0.0000 | 0 | 174 | 49 / 174 = 0.2816 | 16 |
| Claude Haiku 4.5 + instruction, ORACLE | 99 | 3 / 99 = 0.0303 | 2 / 82 = 0.0244 | 1 / 17 = 0.0588 | 3 | 24 / 99 = 0.2424 | 15 / 82 = 0.1829 | 9 / 17 = 0.5294 | 1 / 63 = 0.0159 | 0 | 174 | 49 / 174 = 0.2816 | 16 |
| Claude Haiku 4.5 + instruction, MODEL | 74 | 7 / 74 = 0.0946 | 6 / 61 = 0.0984 | 1 / 13 = 0.0769 | 7 | 24 / 74 = 0.3243 | 16 / 61 = 0.2623 | 8 / 13 = 0.6154 | 1 / 49 = 0.0204 | 0 | 155 | 47 / 155 = 0.3032 | 16 |
| Claude Haiku 4.5 + instruction, LOOKUP | 70 | 5 / 70 = 0.0714 | 5 / 61 = 0.0820 | 0 / 9 = 0.0000 | 5 | 19 / 70 = 0.2714 | 14 / 61 = 0.2295 | 5 / 9 = 0.5556 | 1 / 50 = 0.0200 | 0 | 146 | 40 / 146 = 0.2740 | 12 |
| Claude Haiku 4.5 + instruction, MODEL-ALL | 74 | 4 / 74 = 0.0541 | 3 / 61 = 0.0492 | 1 / 13 = 0.0769 | 4 | 18 / 74 = 0.2432 | 10 / 61 = 0.1639 | 8 / 13 = 0.6154 | 1 / 49 = 0.0204 | 0 | 155 | 47 / 155 = 0.3032 | 16 |
| Claude Haiku 4.5 + instruction, LOOKUP-ALL | 70 | 3 / 70 = 0.0429 | 3 / 61 = 0.0492 | 0 / 9 = 0.0000 | 3 | 15 / 70 = 0.2143 | 10 / 61 = 0.1639 | 5 / 9 = 0.5556 | 1 / 50 = 0.0200 | 0 | 146 | 40 / 146 = 0.2740 | 12 |
| Claude Haiku 4.5 + instruction, LOOKUP-LIT | 94 | 7 / 94 = 0.0745 | 6 / 75 = 0.0800 | 1 / 19 = 0.0526 | 7 | 28 / 94 = 0.2979 | 16 / 75 = 0.2133 | 12 / 19 = 0.6316 | 1 / 62 = 0.0161 | 0 | 174 | 47 / 174 = 0.2701 | 16 |

Per state under Claude Haiku 4.5 + instruction (stale use at TAU_HI / at TAU_GOLD / answered): ALWAYS: sup 1 / 2 / 22, ret 1 / 9 / 20, exp 1 / 6 / 12 · ORACLE: sup 1 / 10 / 63, ret 1 / 8 / 22, exp 1 / 6 / 14 · MODEL: sup 5 / 12 / 49, ret 1 / 5 / 13, exp 1 / 7 / 12 · LOOKUP: sup 4 / 11 / 50, ret 0 / 2 / 8, exp 1 / 6 / 12 · MODEL-ALL: sup 2 / 7 / 49, ret 1 / 5 / 13, exp 1 / 6 / 12 · LOOKUP-ALL: sup 2 / 7 / 50, ret 0 / 2 / 8, exp 1 / 6 / 12 · LOOKUP-LIT: sup 5 / 13 / 62, ret 1 / 9 / 20, exp 1 / 6 / 12.

### AUX-DS-A3-SPEND

Probe mini $0.0002; probe Haiku $0.0007; mini lane $0.1288; Haiku lane $0.4279; **total $0.5576** against the author's $2.00 line.

<!-- AUDIT-R109-BEGIN -->

## 9. The forensic audit of the downstream pipeline (descriptive; written 2026-09-14, R109; `reviews/DOWNSTREAM_AUDIT.md`)

Every value in this section is read from an artifact under `reviews/downstream_audit/` written by `audit_ds.py` and `audit_step8.py` (input and output sha256s in `manifest.json`; script sha256 `55c636183799da00…`). No model call. The 15 expiry obligations are **unscorable** for every stale diagnostic (their YAML gold field is the expired fact, so the gold string equals the stale string); the registered columns above stand as registered and the diagnostic columns below run on the scorable (supersession + retraction) reached set. The step-4 classes are the auditor's read (`step4_labels.json`); the v12/v16 labeling sheets remain the human-validation instrument. **No bar, no prediction, no verdict re-adjudicated; DS-P1 to DS-P5 and Amendments 1 to 3 stand as printed.**

### AUX-DS-AUDIT-GATES

A verbatim replica of `run_ds.records` / `run_ds.score_answer` reproduces every registered per-row score: 0 mismatches over 2041 rows (five lanes: D.4 mini incl. LOOKUP-LIT, D.4 Haiku, A3 mini, A3 Haiku, MODEL-ALL-V3) and 0 of 852 registered per-policy cells differ. The retrieval replay (`LifecycleBank.cosine_search_all` over the pinned question and bank vectors) reproduces the ALWAYS top-5 and the L2 top-10 for 661 / 661 items. Every one of the 26213 view lines parses and equals the TRUE-join entry text (0 failures); the ORACLE view equals the ALWAYS view for 174 / 174 PRESENT items (by construction; ORACLE fetches nothing on a PRESENT item). Prompt digests as `AUX-DS-PROMPT` and `AUX-DS-A3-PROMPT`.

### AUX-DS-AUDIT-DETECTOR — validity by construction (`step1_synthetic.json`)

On the YAML reference strings: gold → correct 174 / 174; abstention string → correct 0; stale string → stale use 89 / 89 at TAU_GOLD and 89 at TAU_HI; gold string → stale 0; abstention → any flag 0; unscorable expiry 15. On the rendered store texts: a gold entry text passes `correct` for 161 / 164 PRESENT items with a licensed id (none for frbank:billy:billy_q06:FULL, frbank:callum:callum_q05:FULL, frbank:kenji:kenji_q05:FULL); 10 PRESENT items have no licensed id. A forbidding entry text fires stale use for 84 / 89 scorable obligations at TAU_GOLD (71 at TAU_HI); none fires for frbank:bruna:bruna_q06:CAT-ABLATED, frbank:fatima:fatima_q06:SLOT-ABLATED, frbank:rosa:rosa_q06:FULL, frbank:rosa:rosa_q06:CAT-ABLATED, frbank:rosa:rosa_q06:SLOT-ABLATED. 6 of 237 successor entry texts fire stale use (frbank:valentina:valentina_q04:FULL, frbank:valentina:valentina_q04:SLOT-ABLATED). On the 65 in-view licensed items Haiku 4.5's detector-correct count includes 12 abstentions whose explanation restates the gold line (GPT-4.1 mini 0).

### AUX-DS-AUDIT-RATES — stale use at TAU_GOLD as a rate on the reached set, registered (all states) beside scorable (expiry removed), Wilson 95% (`step2_rescore.json`)

| answerer, prompt | policy | registered | scorable |
|---|---|---|---|
| GPT-4.1 mini, D.4 | ALWAYS | 9 / 54 | 8 / 42 = 0.1905 [0.100, 0.333] |
| GPT-4.1 mini, D.4 | MODEL | 9 / 74 | 8 / 62 = 0.1290 [0.067, 0.234] |
| GPT-4.1 mini, D.4 | LOOKUP | 7 / 70 | 6 / 58 = 0.1034 [0.048, 0.208] |
| GPT-4.1 mini, D.4 | MODEL-ALL | 9 / 74 | 8 / 62 = 0.1290 [0.067, 0.234] |
| GPT-4.1 mini, D.4 | LOOKUP-ALL | 6 / 70 | 5 / 58 = 0.0862 [0.037, 0.186] |
| GPT-4.1 mini, D.4 | LOOKUP-LIT | 14 / 94 | 13 / 82 = 0.1585 [0.095, 0.253] |
| GPT-4.1 mini, D.4 | ORACLE | 17 / 99 | 16 / 85 = 0.1882 [0.119, 0.284] |
| Haiku 4.5, D.4 | ALWAYS | 19 / 54 | 11 / 42 = 0.2619 [0.153, 0.411] |
| Haiku 4.5, D.4 | MODEL | 23 / 74 | 16 / 62 = 0.2581 [0.166, 0.379] |
| Haiku 4.5, D.4 | LOOKUP | 19 / 70 | 11 / 58 = 0.1897 [0.109, 0.308] |
| Haiku 4.5, D.4 | MODEL-ALL | 20 / 74 | 13 / 62 = 0.2097 [0.127, 0.326] |
| Haiku 4.5, D.4 | LOOKUP-ALL | 18 / 70 | 10 / 58 = 0.1724 [0.096, 0.289] |
| Haiku 4.5, D.4 | LOOKUP-LIT | 29 / 94 | 21 / 82 = 0.2561 [0.174, 0.360] |
| Haiku 4.5, D.4 | ORACLE | 27 / 99 | 19 / 85 = 0.2235 [0.148, 0.323] |
| GPT-4.1 mini + instruction | ALWAYS | 10 / 54 | 9 / 42 = 0.2143 [0.117, 0.359] |
| GPT-4.1 mini + instruction | MODEL | 10 / 74 | 9 / 62 = 0.1452 [0.078, 0.253] |
| GPT-4.1 mini + instruction | LOOKUP | 8 / 70 | 7 / 58 = 0.1207 [0.060, 0.229] |
| GPT-4.1 mini + instruction | MODEL-ALL | 10 / 74 | 9 / 62 = 0.1452 [0.078, 0.253] |
| GPT-4.1 mini + instruction | LOOKUP-ALL | 7 / 70 | 6 / 58 = 0.1034 [0.048, 0.208] |
| GPT-4.1 mini + instruction | LOOKUP-LIT | 16 / 94 | 15 / 82 = 0.1829 [0.114, 0.280] |
| GPT-4.1 mini + instruction | ORACLE | 18 / 99 | 17 / 85 = 0.2000 [0.129, 0.297] |
| Haiku 4.5 + instruction | ALWAYS | 17 / 54 | 11 / 42 = 0.2619 [0.153, 0.411] |
| Haiku 4.5 + instruction | MODEL | 24 / 74 | 17 / 62 = 0.2742 [0.179, 0.396] |
| Haiku 4.5 + instruction | LOOKUP | 19 / 70 | 13 / 58 = 0.2241 [0.136, 0.347] |
| Haiku 4.5 + instruction | MODEL-ALL | 18 / 74 | 12 / 62 = 0.1935 [0.114, 0.308] |
| Haiku 4.5 + instruction | LOOKUP-ALL | 15 / 70 | 9 / 58 = 0.1552 [0.084, 0.269] |
| Haiku 4.5 + instruction | LOOKUP-LIT | 28 / 94 | 22 / 82 = 0.2683 [0.184, 0.373] |
| Haiku 4.5 + instruction | ORACLE | 24 / 99 | 18 / 85 = 0.2118 [0.138, 0.310] |

### AUX-DS-AUDIT-PAIRED — the ALWAYS → ORACLE decomposition on the scorable obligations (`step8_verdicts.json`)

| answerer, prompt | reached under ALWAYS | stale under ALWAYS | stale under ORACLE on the same items | identical views (n; stale) | extended views: F→F / T→T / F→T / T→F | newly reached under ORACLE | ORACLE, all scorable | not reached under ALWAYS but an active line of the top-5 asserts the stale value |
|---|---:|---|---|---|---|---|---|---:|
| GPT-4.1 mini, D.4 | 42 | 8 / 42 = 0.1905 [0.100, 0.333] | 9 / 42 = 0.2143 [0.117, 0.359] | 10; 3 | 25 / 4 / 2 / 1 | 7 / 43 = 0.1628 [0.081, 0.300] | 16 / 85 = 0.1882 [0.119, 0.284] | 18 |
| Haiku 4.5, D.4 | 42 | 11 / 42 = 0.2619 [0.153, 0.411] | 11 / 42 = 0.2619 [0.153, 0.411] | 10; 3 | 23 / 7 / 1 / 1 | 8 / 43 = 0.1860 [0.097, 0.326] | 19 / 85 = 0.2235 [0.148, 0.323] | 18 |
| GPT-4.1 mini + instruction | 42 | 9 / 42 = 0.2143 [0.117, 0.359] | 10 / 42 = 0.2381 [0.135, 0.385] | 10; 3 | 25 / 6 / 1 / 0 | 7 / 43 = 0.1628 [0.081, 0.300] | 17 / 85 = 0.2000 [0.129, 0.297] | 18 |
| Haiku 4.5 + instruction | 42 | 11 / 42 = 0.2619 [0.153, 0.411] | 10 / 42 = 0.2381 [0.135, 0.385] | 10; 3 | 24 / 7 / 0 / 1 | 8 / 43 = 0.1860 [0.097, 0.326] | 18 / 85 = 0.2118 [0.138, 0.310] | 18 |

### AUX-DS-AUDIT-SOURCE — what the view itself asserts (`step4b_view_lines.json`)

Of the 89 scorable obligations, the ORACLE view holds an **active** line whose text asserts the stale value (the item's own detector at TAU_GOLD on the line) for **35** (supersession 21, retraction 14); the same 35 under ALWAYS, since every fetched line is tagged; no tagged line asserts the successor (0). Stale use at TAU_GOLD × an active stale line in the view, ORACLE (stale with such a line / stale without / not stale with / not stale without): GPT-4.1 mini, D.4 16 / 0 / 19 / 50; Haiku 4.5, D.4 14 / 5 / 21 / 45; GPT-4.1 mini + instruction 17 / 0 / 18 / 50; Haiku 4.5 + instruction 15 / 3 / 20 / 47; ALWAYS: GPT-4.1 mini, D.4 8 / 0 / 9 / 25; Haiku 4.5, D.4 9 / 2 / 8 / 23. Negation mis-tag (one item, both variants): `frbank:fatima:fatima_q06` — the retraction statement ("decided not to launch a home fragrance line called Oud and Geometry ...") carries the `retracted` tag because it covers 4 of the 5 original-plan tokens at TAU_HI and the join has no negation handling, while the plan records stay active ("launching" is not "launch").

### AUX-DS-AUDIT-READ — the flagged answers classified (`step4_labels.json`, `step4_counts.json`; the auditor's read)

| answerer, D.4 | flagged under ORACLE | unscorable expiry | gives the stale value | mentions it, states superseded / retracted / cancelled | partial-overlap artifact | other |
|---|---:|---:|---:|---:|---:|---:|
| GPT-4.1 mini, D.4 | 17 | 1 | 11 | 3 | 2 | 0 |
| Haiku 4.5, D.4 | 27 | 8 | 8 | 8 | 0 | 3 |

| answerer, D.4 | in-view licensed items marked incorrect | abstained | correct value in a different format | wrong value | other |
|---|---:|---:|---:|---:|---:|
| GPT-4.1 mini, D.4 | 28 | 15 | 6 | 5 | 2 |
| Haiku 4.5, D.4 | 27 | 26 | 0 | 1 | 0 |

Paired on the 85 scorable ORACLE keys: both flagged 10, GPT-4.1 mini only 6, Haiku 4.5 only 9 (exact McNemar p = 0.6072); by the read, 'gives the stale value': both 8, mini only 3, Haiku only 0. Of the registered ORACLE flags, 8 (Haiku) and 1 (mini) are expiry items.

### AUX-DS-AUDIT-LENGTH — answer length and the stale flag (`step7_length.json`, `step3_scored_text.json`)

Median answer length on the same 452 views: Haiku 4.5 210 characters, GPT-4.1 mini 73.5; sentences per answer mini {'1': 444, '2': 8}, Haiku {'1': 106, '2': 318, '3': 28}. Point-biserial r of stale use at TAU_GOLD with log length on the scorable obligation rows: mini 0.2255 (p = 0.0009), Haiku 0.2316 (p = 0.0007); odds ratio per doubling of length 2.3414 / 2.9928. Pooled logistic on 424 rows, logit P(stale) = b0 + b1 log(chars) + b2 is_haiku: b1 = 1.3701 (z 4.55), b2 = -0.7435 (z -2.05). ORACLE, scorable, stale at TAU_GOLD / TAU_HI: mini registered 16 / 85 = 0.1882 / 0 / 85 = 0.0000; Haiku registered 19 / 85 = 0.2235 / 5 / 85 = 0.0588; Haiku first sentence 8 / 85 = 0.0941 / 1 / 85 = 0.0118; Haiku cut to mini's length 7 / 85 = 0.0824 / 0 / 85 = 0.0000. First-sentence stale at TAU_GOLD under ORACLE, every lane: GPT-4.1 mini, D.4 16 / 85 = 0.1882; Haiku 4.5, D.4 8 / 85 = 0.0941; GPT-4.1 mini + instruction 17 / 85 = 0.2000; Haiku 4.5 + instruction 8 / 85 = 0.0941.

### AUX-DS-AUDIT-IDENTITY — the persona binding and the in-view abstentions (`step4b_view_lines.json`, `step8_verdicts.json`)

The persona's name appears in 47 / 174 PRESENT views and 26 / 104 obligation views; 172 / 174 PRESENT questions name the persona. PRESENT abstentions (rows): Haiku 4.5, D.4 145 / 221, 94 giving the identity reason in the answer text; GPT-4.1 mini, D.4 66 / 221 (the bare phrase). On the 65 licensed items whose gold record is in the retrieval view (ALWAYS = ORACLE view): Haiku 4.5 + instruction detector-correct 41 (of which 16 abstentions), abstained 40, answered wrongly 0, correct among the answered 25 / 25; Haiku 4.5, D.4 detector-correct 38 (of which 12 abstentions), abstained 38, answered wrongly 1, correct among the answered 26 / 27; GPT-4.1 mini + instruction detector-correct 39 (of which 0 abstentions), abstained 15, answered wrongly 11, correct among the answered 39 / 50; GPT-4.1 mini, D.4 detector-correct 37 (of which 0 abstentions), abstained 15, answered wrongly 13, correct among the answered 37 / 50. Of GPT-4.1 mini's 15 in-view abstentions, 13 fall on a key where Haiku 4.5 states the identity reason; Haiku states it on 34 of its 38 (computed in the registration of Amendment 4).

### AUX-DS-AUDIT-RANK — the licensed record under the unmasked top-5 retriever (`step5_ranks.json`, `step5_coverage.json`)

| population | n | median best rank | q25 | q75 | share ≤ 5 | share ≤ 10 | share > 10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PRESENT | 164 | 8.5 | 3.0 | 35.25 | 0.3963 | 0.5427 | 0.4573 |
| PRESENT-NEGATIVE | 104 | 5.0 | 2.0 | 13.0 | 0.5192 | 0.7115 | 0.2885 |
| PRESENT-NEGATIVE|sup | 63 | 8.0 | 3.0 | 16.0 | 0.3492 | 0.5873 | 0.4127 |
| PRESENT-NEGATIVE|ret | 26 | 3.0 | 2.0 | 4.75 | 0.7692 | 0.9615 | 0.0385 |
| PRESENT-NEGATIVE|exp | 15 | 2.0 | 1.0 | 2.5 | 0.8000 | 0.8000 | 0.2000 |

Licensed record in view by entry id / normalized text / MiniLM cosine ≥ 0.90: PRESENT 65 / 65 / 65 of 174 (cosine ≥ 0.80: 75); obligations under ALWAYS 54 / 54 / 59 of 104, under ORACLE 99 / 99 / 99. In-view correct under retrieval alone is the same under the three definitions (37 / 65 mini, 38 / 65 Haiku). 28 licensed records are absent from their item's store variant; no item loses all of them.

### AUX-DS-AUDIT-A3 — the D.4 → Amendment 3 transitions on the 452 views (`step8_verdicts.json`)

- Haiku 4.5, D.4 → + instruction: 103 / 452 answers byte-identical; stale use at TAU_GOLD on the scorable obligations F→T 9, T→F 11 (exact McNemar p = 0.8238); at TAU_HI F→T 2, T→F 4; correct F→T 5, T→F 6; PRESENT abstention 145 / 221 → 144 / 221.
- GPT-4.1 mini, D.4 → + instruction: 310 / 452 answers byte-identical; stale use at TAU_GOLD on the scorable obligations F→T 4, T→F 1 (exact McNemar p = 0.375); at TAU_HI F→T 2, T→F 0; correct F→T 4, T→F 3; PRESENT abstention 66 / 221 → 70 / 221.

### AUX-DS-AUDIT-PRINTED — the forms the paper prints (R109, Section 8 and Appendix E.10, the downstream appendix; F.10 before the R108 letter shift), each the two-decimal rounding of, or equal to, a value above

Stale rate on the scorable reached set, GPT-4.1 mini: retrieval alone 0.19 (0.1905), oracle 0.19 (0.1882); Haiku 4.5: 0.26 (0.2619), 0.22 (0.2235). Odds ratio per doubling of answer length: 2.34 (2.3414), 2.99 (2.9928). Counts: 89 scorable obligations; 35 views with an active stale line (21 supersession, 14 retraction); 16 of 16 (mini, oracle) and 14 of 19 (Haiku, oracle); 42 obligations reached under both, 8 -> 9 (mini) and 11 -> 11 (Haiku); 43 newly reached, 7 and 8; first sentence 8 of 85 against 19 (Haiku) and 16 (mini), cut to mini's length 7; by the read 11 of 16 (mini) and 8 of 19 (Haiku); 310 of 452 answers byte-identical under the instruction; 65 in-view licensed items, mini 37 correct and 15 abstentions, Haiku 38 abstentions of which 12 counted correct; 28 in-view misses; persona name in 47 of 174 views, 172 of 174 questions name the persona; Haiku 94 of 145 abstentions with the identity reason; median best rank 8.5; 15 expiry obligations unscorable; five retraction obligations unflaggable, 6 successor texts flagged, 3 licensed items unmarkable; Amendment 4: +0.10, 15 -> 7, 38 -> 19, cap $8.00.

### AUX-DS-AUDIT-VERDICTS — the author's rulings of 2026-09-14 (evening), as recorded in `reviews/DOWNSTREAM_AUDIT.md`

(a) flat correct: construction for ALWAYS versus ORACLE; the gated drop is abstention, driven by the persona-binding gap and bounded by retrieval rank. (b) stale rising with reach: a reporting artifact — rates flat with Wilson intervals; stale answers arise only from active lines asserting the stale value (none from tagged lines for GPT-4.1 mini; five qualified mentions for Haiku 4.5). (c) Haiku above mini: instrument — unscorable expiry plus qualified mentions in second sentences; on 'gives the stale value' Haiku is at or below mini. (d) inert instruction: redundant for mini, mis-targeted for both, since the stale sources are untagged.

## 10. Amendment 4 — a view header binding "User" to the persona and pinning the current date (two predictions; registered 2026-09-14, R109; NOT YET RUN)

### AUX-DS-A4-REG

Registration `registrations/ADDENDUM_DS_AMENDMENT_4.md`, frozen sha256 `fb4b2ca8c8e280cbe6815c9782145abd93082e67b311fa1aeca60804f7dd6d8d`, recorded here on 2026-09-14 **before any call** (copy in `iclr2027_monitoring_submission/ARTIFACT/registrations/`). Predictions A4-P1 (in-view correct on the 65 rises by at least +0.10 with both bootstrap intervals excluding zero, each answerer) and A4-P2 (in-view abstentions fall by more than half: GPT-4.1 mini 15 → 7 or fewer, Haiku 4.5 38 → 19 or fewer), failure texts written in §A4.4; stale use reported by first sentence and by active-versus-tagged source beside the registered column (descriptive); the 452 views, both answerers, cap $8.00 (projection ≈ $0.71 with the ×1.3 rule). The runner (`ds_downstream/tools/amend4_header.py`) is not yet written and no call has been made; the keys `AUX-DS-A4-LOCK`, `-PROMPT`, `-POP`, `-PROBE-MINI`, `-PROBE-H45`, `-PROJECTION`, `-P1`, `-P2`, `-STAGE2-MINI`, `-STAGE2-H45`, `-FIRSTSENT`, `-SOURCE`, `-PRESENT`, `-EXPIRY`, `-SPEND` are appended by it after the author's word.

<!-- AUDIT-R109-END -->

### AUX-DS-A4-LOCK, AUX-DS-A4-PROMPT, AUX-DS-A4-POP, AUX-DS-A4-PROBE-MINI, AUX-DS-A4-PROBE-H45, AUX-DS-A4-PROJECTION (appended by `tools/amend4_header.py score`)

Registration sha256 holds; `USER_ANSWER_A4` sha256 `e6c155364f8c69bef8af0c86941b3bf8fc5e739e043ac3ef2f86f422ff40cd7d` (the D.4 user text with the header, sha256 `1fe1eb17795796bb95617a28ac7b7628b9607abc2fb8b51989cbf70d1de08d6b`, verbatim from section A4.2; example first line: The user is Aisha Mohammed. Every entry below that says "User" is about Aisha Mohammed. Today's date is 2026-05-26; each entry's age is counted back from today.); `SYSTEM_ANSWER` and `USER_ANSWER` as AUX-DS-PROMPT; prompts_e1 digests as pinned. Population 452 distinct (item, view) pairs (231 PN, 221 PRESENT); the prediction population 65 licensed items in view over 29 personas; 40 personas with a name and a pinned date. Probe mini: served `gpt-4.1-mini-2025-04-14` (473 in / 21 out); probe Haiku 4.5: served `claude-haiku-4-5-20251001` (523 in / 33 out). Projection: mini $0.1237, Haiku $0.3685, sum with probes $0.4931 (x1.3 $0.6410) against the $8.00 cap; runs: True.

### AUX-DS-A4-P1-MINI, AUX-DS-A4-P2-MINI — the two predictions, GPT-4.1 mini (the 65 licensed items in view; item-level and persona-clustered percentile bootstrap, 10000 draws, seed 42, 29 personas)

A4-P1: correct 37 → 48 of 65, Δ₁ = +0.1692, item interval [+0.0769, +0.2769], persona interval [+0.0678, +0.2603], bar +0.10 with both intervals above zero: **HOLDS**. A4-P1 HOLDS for GPT-4.1 mini: the header raises the correct count on the 65 licensed items in view from 37 to 48, Δ₁ = +0.1692 with intervals [+0.0769, +0.2769] (item) and [+0.0678, +0.2603] (persona), both above zero and the point estimate at or above +0.10.

A4-P2: abstentions 15 → 3 of 65, bar 7 or fewer: **HOLDS**. A4-P2 HOLDS for GPT-4.1 mini: abstentions on the 65 licensed items in view fall from 15 to 3, at or under the bar of 7.

Beside: detector-correct answers that are abstentions restating the gold line, D.4 0 → A4 0; correct among the answered under A4 48 / 62.

### AUX-DS-A4-PRESENT-MINI — the licensed items under GPT-4.1 mini with the header

Under retrieval alone (ALWAYS view, the ORACLE view on every licensed item): correct 56 / 174 (D.4: 46), abstained 33 / 174, of which 0 counted correct; over all 221 licensed views abstained 42.

### AUX-DS-A4-STAGE2-MINI — Stage 2 under GPT-4.1 mini with the header, every policy, the committed detector, all states (rows 452, failed 0, served ['gpt-4.1-mini']; temperature 0, k = 1)

| answerer, policy | PN reached ∧ answered | stale use (all) | stale use, tagged reach | stale use, untagged reach | stale surfacing | stale use at TAU_GOLD (all) | at TAU_GOLD, tagged | at TAU_GOLD, untagged | successor use (of supersession) | both | PRESENT answered | PRESENT correct (TAU_GOLD) | at TAU_HI |
|---|---:|---|---|---|---:|---|---|---|---|---:|---:|---|---:|
| GPT-4.1 mini + header, ALWAYS | 54 | 3 / 54 = 0.0556 | 2 / 35 = 0.0571 | 1 / 19 = 0.0526 | 3 | 11 / 54 = 0.2037 | 2 / 35 = 0.0571 | 9 / 19 = 0.4737 | 1 / 22 = 0.0455 | 0 | 174 | 56 / 174 = 0.3218 | 20 |
| GPT-4.1 mini + header, ORACLE | 99 | 2 / 99 = 0.0202 | 2 / 82 = 0.0244 | 0 / 17 = 0.0000 | 2 | 18 / 99 = 0.1818 | 11 / 82 = 0.1341 | 7 / 17 = 0.4118 | 1 / 63 = 0.0159 | 0 | 174 | 56 / 174 = 0.3218 | 20 |
| GPT-4.1 mini + header, MODEL | 74 | 2 / 74 = 0.0270 | 2 / 61 = 0.0328 | 0 / 13 = 0.0000 | 2 | 11 / 74 = 0.1486 | 6 / 61 = 0.0984 | 5 / 13 = 0.3846 | 1 / 49 = 0.0204 | 0 | 155 | 53 / 155 = 0.3419 | 20 |
| GPT-4.1 mini + header, LOOKUP | 70 | 2 / 70 = 0.0286 | 2 / 61 = 0.0328 | 0 / 9 = 0.0000 | 2 | 9 / 70 = 0.1286 | 6 / 61 = 0.0984 | 3 / 9 = 0.3333 | 1 / 50 = 0.0200 | 0 | 146 | 48 / 146 = 0.3288 | 16 |
| GPT-4.1 mini + header, MODEL-ALL | 74 | 2 / 74 = 0.0270 | 1 / 61 = 0.0164 | 1 / 13 = 0.0769 | 2 | 12 / 74 = 0.1622 | 7 / 61 = 0.1148 | 5 / 13 = 0.3846 | 1 / 49 = 0.0204 | 0 | 155 | 53 / 155 = 0.3419 | 20 |
| GPT-4.1 mini + header, LOOKUP-ALL | 70 | 1 / 70 = 0.0143 | 1 / 61 = 0.0164 | 0 / 9 = 0.0000 | 1 | 9 / 70 = 0.1286 | 6 / 61 = 0.0984 | 3 / 9 = 0.3333 | 1 / 50 = 0.0200 | 0 | 146 | 47 / 146 = 0.3219 | 16 |
| GPT-4.1 mini + header, LOOKUP-LIT | 94 | 3 / 94 = 0.0319 | 2 / 75 = 0.0267 | 1 / 19 = 0.0526 | 3 | 17 / 94 = 0.1809 | 8 / 75 = 0.1067 | 9 / 19 = 0.4737 | 1 / 62 = 0.0161 | 0 | 174 | 55 / 174 = 0.3161 | 19 |

### AUX-DS-A4-FIRSTSENT-MINI, AUX-DS-A4-SOURCE-MINI — stale use at TAU_GOLD on the scorable (supersession + retraction) reached obligations, GPT-4.1 mini + header: the registered flag beside the first-sentence flag and the source in the view (expiry unscorable: 14 of the oracle's 99)

| policy | reached | expiry (unscorable) | scorable | registered flag, all states | registered flag, scorable (Wilson) | first sentence (Wilson) | active line asserts the stale value: views / stale | tagged-only: views / stale | no line: views / stale | abstentions |
|---|---:|---:|---:|---|---|---|---|---|---|---|
| ALWAYS | 54 | 12 | 42 | 11 / 54 | 10 / 42 = 0.2381 [0.1348, 0.3853] | 10 / 42 = 0.2381 [0.1348, 0.3853] | 17 / 10 | 21 / 0 | 4 / 0 | 8 / 42 |
| ORACLE | 99 | 14 | 85 | 18 / 99 | 17 / 85 = 0.2000 [0.1288, 0.2972] | 17 / 85 = 0.2000 [0.1288, 0.2972] | 35 / 17 | 46 / 0 | 4 / 0 | 12 / 85 |
| MODEL | 74 | 12 | 62 | 11 / 74 | 10 / 62 = 0.1613 [0.09, 0.2721] | 10 / 62 = 0.1613 [0.09, 0.2721] | 20 / 10 | 38 / 0 | 4 / 0 | 11 / 62 |
| LOOKUP | 70 | 12 | 58 | 9 / 70 | 8 / 58 = 0.1379 [0.0716, 0.2493] | 8 / 58 = 0.1379 [0.0716, 0.2493] | 17 / 8 | 38 / 0 | 3 / 0 | 8 / 58 |
| MODEL-ALL | 74 | 12 | 62 | 12 / 74 | 11 / 62 = 0.1774 [0.1021, 0.2904] | 11 / 62 = 0.1774 [0.1021, 0.2904] | 20 / 11 | 38 / 0 | 4 / 0 | 10 / 62 |
| LOOKUP-ALL | 70 | 12 | 58 | 9 / 70 | 8 / 58 = 0.1379 [0.0716, 0.2493] | 8 / 58 = 0.1379 [0.0716, 0.2493] | 17 / 8 | 38 / 0 | 3 / 0 | 8 / 58 |
| LOOKUP-LIT | 94 | 12 | 82 | 17 / 94 | 16 / 82 = 0.1951 [0.1238, 0.2937] | 16 / 82 = 0.1951 [0.1238, 0.2937] | 32 / 16 | 46 / 0 | 4 / 0 | 12 / 82 |

### AUX-DS-A4-EXPIRY-MINI — the 14 expiry obligations under the oracle, GPT-4.1 mini + header (unscorable; descriptive): abstained 10, registered flag fires 1. Answers, read as a list:

- `frbank:bruna:bruna_q11:CAT-ABLATED|2f1e0bbeda1d7d38`: The store does not currently contain the answer.
- `frbank:bruna:bruna_q11:FULL|bde60a4f4f1b951d`: The store does not currently contain the answer.
- `frbank:david:david_q06:CAT-ABLATED|c65c804ae433b38e`: The store does not currently contain the answer.
- `frbank:david:david_q06:FULL|3277b5b20f7f6e86`: The store does not currently contain the answer.
- `frbank:david:david_q11:CAT-ABLATED|549afd6257cd321a`: The store does not currently contain the answer.
- `frbank:david:david_q11:FULL|549afd6257cd321a`: The store does not currently contain the answer.
- `frbank:elena:elena_q05:CAT-ABLATED|0e2f57e75bdc4d34`: The store does not currently contain the answer.
- `frbank:elena:elena_q05:FULL|0e2f57e75bdc4d34`: The store does not currently contain the answer.
- `frbank:elena:elena_q10:FULL|d3628568bf1ac42e`: Elena's lease is currently locked in until March 2026 and ends then, so she does not need to make any lease decisions at this time.
- `frbank:jake:jake_q11:FULL|131f342b26ed61a3`: Jake has no upcoming exams, but he currently holds a journeyman electrician certification.
- `frbank:marcus:marcus_q10:FULL|b857289930965af8`: Marcus has a new alignment rack that was delivered and installed on April 22, but there are no current equipment deliveries coming.
- `frbank:marcus:marcus_q12:FULL|0f32feef9e8d196c`: The store does not currently contain the answer.
- `frbank:thanh:thanh_q02:CAT-ABLATED|7b07977c9ad1ce46`: No, Thanh does not have any upcoming government inspections; the last scheduled aquaculture inspection on February 15, 2025, has expired.
- `frbank:thanh:thanh_q02:FULL|40773509689c6a9e`: The store does not currently contain the answer.

### AUX-DS-A4-P1-H45, AUX-DS-A4-P2-H45 — the two predictions, Claude Haiku 4.5 (the 65 licensed items in view; item-level and persona-clustered percentile bootstrap, 10000 draws, seed 42, 29 personas)

A4-P1: correct 38 → 59 of 65, Δ₁ = +0.3231, item interval [+0.2000, +0.4462], persona interval [+0.1833, +0.4714], bar +0.10 with both intervals above zero: **HOLDS**. A4-P1 HOLDS for Claude Haiku 4.5: the header raises the correct count on the 65 licensed items in view from 38 to 59, Δ₁ = +0.3231 with intervals [+0.2000, +0.4462] (item) and [+0.1833, +0.4714] (persona), both above zero and the point estimate at or above +0.10.

A4-P2: abstentions 38 → 3 of 65, bar 19 or fewer: **HOLDS**. A4-P2 HOLDS for Claude Haiku 4.5: abstentions on the 65 licensed items in view fall from 38 to 3, at or under the bar of 19.

Beside: detector-correct answers that are abstentions restating the gold line, D.4 12 → A4 3; correct among the answered under A4 56 / 62.

### AUX-DS-A4-PRESENT-H45 — the licensed items under Claude Haiku 4.5 with the header

Under retrieval alone (ALWAYS view, the ORACLE view on every licensed item): correct 73 / 174 (D.4: 48), abstained 45 / 174, of which 8 counted correct; over all 221 licensed views abstained 56.

### AUX-DS-A4-STAGE2-H45 — Stage 2 under Claude Haiku 4.5 with the header, every policy, the committed detector, all states (rows 452, failed 0, served ['claude-haiku-4-5-20251001']; temperature 0, k = 1)

| answerer, policy | PN reached ∧ answered | stale use (all) | stale use, tagged reach | stale use, untagged reach | stale surfacing | stale use at TAU_GOLD (all) | at TAU_GOLD, tagged | at TAU_GOLD, untagged | successor use (of supersession) | both | PRESENT answered | PRESENT correct (TAU_GOLD) | at TAU_HI |
|---|---:|---|---|---|---:|---|---|---|---|---:|---:|---|---:|
| Claude Haiku 4.5 + header, ALWAYS | 54 | 5 / 54 = 0.0926 | 4 / 35 = 0.1143 | 1 / 19 = 0.0526 | 5 | 18 / 54 = 0.3333 | 7 / 35 = 0.2000 | 11 / 19 = 0.5789 | 1 / 22 = 0.0455 | 0 | 174 | 73 / 174 = 0.4195 | 27 |
| Claude Haiku 4.5 + header, ORACLE | 99 | 7 / 99 = 0.0707 | 7 / 82 = 0.0854 | 0 / 17 = 0.0000 | 9 | 32 / 99 = 0.3232 | 25 / 82 = 0.3049 | 7 / 17 = 0.4118 | 2 / 63 = 0.0317 | 0 | 174 | 73 / 174 = 0.4195 | 27 |
| Claude Haiku 4.5 + header, MODEL | 74 | 8 / 74 = 0.1081 | 8 / 61 = 0.1311 | 0 / 13 = 0.0000 | 10 | 27 / 74 = 0.3649 | 19 / 61 = 0.3115 | 8 / 13 = 0.6154 | 1 / 49 = 0.0204 | 0 | 155 | 64 / 155 = 0.4129 | 24 |
| Claude Haiku 4.5 + header, LOOKUP | 70 | 7 / 70 = 0.1000 | 7 / 61 = 0.1148 | 0 / 9 = 0.0000 | 9 | 24 / 70 = 0.3429 | 18 / 61 = 0.2951 | 6 / 9 = 0.6667 | 1 / 50 = 0.0200 | 0 | 146 | 58 / 146 = 0.3973 | 21 |
| Claude Haiku 4.5 + header, MODEL-ALL | 74 | 7 / 74 = 0.0946 | 6 / 61 = 0.0984 | 1 / 13 = 0.0769 | 9 | 23 / 74 = 0.3108 | 14 / 61 = 0.2295 | 9 / 13 = 0.6923 | 2 / 49 = 0.0408 | 0 | 155 | 64 / 155 = 0.4129 | 24 |
| Claude Haiku 4.5 + header, LOOKUP-ALL | 70 | 6 / 70 = 0.0857 | 6 / 61 = 0.0984 | 0 / 9 = 0.0000 | 8 | 20 / 70 = 0.2857 | 14 / 61 = 0.2295 | 6 / 9 = 0.6667 | 2 / 50 = 0.0400 | 0 | 146 | 58 / 146 = 0.3973 | 21 |
| Claude Haiku 4.5 + header, LOOKUP-LIT | 94 | 8 / 94 = 0.0851 | 7 / 75 = 0.0933 | 1 / 19 = 0.0526 | 10 | 31 / 94 = 0.3298 | 20 / 75 = 0.2667 | 11 / 19 = 0.5789 | 1 / 62 = 0.0161 | 0 | 174 | 72 / 174 = 0.4138 | 28 |

### AUX-DS-A4-FIRSTSENT-H45, AUX-DS-A4-SOURCE-H45 — stale use at TAU_GOLD on the scorable (supersession + retraction) reached obligations, Claude Haiku 4.5 + header: the registered flag beside the first-sentence flag and the source in the view (expiry unscorable: 14 of the oracle's 99)

| policy | reached | expiry (unscorable) | scorable | registered flag, all states | registered flag, scorable (Wilson) | first sentence (Wilson) | active line asserts the stale value: views / stale | tagged-only: views / stale | no line: views / stale | abstentions |
|---|---:|---:|---:|---|---|---|---|---|---|---|
| ALWAYS | 54 | 12 | 42 | 18 / 54 | 10 / 42 = 0.2381 [0.1348, 0.3853] | 6 / 42 = 0.1429 [0.0672, 0.2784] | 17 / 9 | 21 / 1 | 4 / 0 | 14 / 42 |
| ORACLE | 99 | 14 | 85 | 32 / 99 | 23 / 85 = 0.2706 [0.1876, 0.3734] | 15 / 85 = 0.1765 [0.11, 0.271] | 35 / 16 | 46 / 7 | 4 / 0 | 25 / 85 |
| MODEL | 74 | 12 | 62 | 27 / 74 | 19 / 62 = 0.3065 [0.2058, 0.4297] | 12 / 62 = 0.1935 [0.1143, 0.3085] | 20 / 12 | 38 / 7 | 4 / 0 | 16 / 62 |
| LOOKUP | 70 | 12 | 58 | 24 / 70 | 16 / 58 = 0.2759 [0.1775, 0.402] | 11 / 58 = 0.1897 [0.1093, 0.3085] | 17 / 9 | 38 / 7 | 3 / 0 | 14 / 58 |
| MODEL-ALL | 74 | 12 | 62 | 23 / 74 | 15 / 62 = 0.2419 [0.1525, 0.3615] | 11 / 62 = 0.1774 [0.1021, 0.2904] | 20 / 12 | 38 / 3 | 4 / 0 | 16 / 62 |
| LOOKUP-ALL | 70 | 12 | 58 | 20 / 70 | 12 / 58 = 0.2069 [0.1225, 0.3277] | 9 / 58 = 0.1552 [0.0838, 0.2693] | 17 / 9 | 38 / 3 | 3 / 0 | 14 / 58 |
| LOOKUP-LIT | 94 | 12 | 82 | 31 / 94 | 23 / 82 = 0.2805 [0.1948, 0.3859] | 15 / 82 = 0.1829 [0.1141, 0.2801] | 32 / 17 | 46 / 6 | 4 / 0 | 21 / 82 |

### AUX-DS-A4-EXPIRY-H45 — the 14 expiry obligations under the oracle, Claude Haiku 4.5 + header (unscorable; descriptive): abstained 13, registered flag fires 9. Answers, read as a list:

- `frbank:bruna:bruna_q11:CAT-ABLATED|2f1e0bbeda1d7d38`: The memory store does not currently contain information about Bruna being registered for any races or sporting events. The only race entries in the store are expired entries about a past Dubai Marathon completion from January 2025.
- `frbank:bruna:bruna_q11:FULL|bde60a4f4f1b951d`: Bruna has a training plan for cycling and is preparing for amateur cycling races, but the store does not currently contain information about specific race registrations.
- `frbank:david:david_q06:CAT-ABLATED|c65c804ae433b38e`: The store does not currently contain information about David preparing students for exams. The entries show that David has a personal AP European History exam scheduled for May 8, 2026, and is considering taking over AP US History sections next year, but do not indicate that he teaches or prepares students for exams.
- `frbank:david:david_q06:FULL|3277b5b20f7f6e86`: The store does not currently contain the answer. The entries describe David's own upcoming AP European History exam on May 8 and his plans to run a mock exam, but do not indicate whether he is preparing students for any exams.
- `frbank:david:david_q11:CAT-ABLATED|549afd6257cd321a`: The store does not currently contain information about upcoming parent events. The parent-teacher conference entries from March 2025 have expired, and the only active obligation is a coaching responsibility for a debate tournament on May 9th.
- `frbank:david:david_q11:FULL|549afd6257cd321a`: The store does not currently contain information about upcoming parent events. The parent-teacher conference entries from March 2025 have expired, and the only active obligation is a coaching responsibility for a debate tournament on May 9th.
- `frbank:elena:elena_q05:CAT-ABLATED|0e2f57e75bdc4d34`: The store does not currently contain information about any upcoming exams or certifications. The only exam-related entries are either expired (entries 2-4 from March 2025) or describe a past professional exam (entry 5).
- `frbank:elena:elena_q05:FULL|0e2f57e75bdc4d34`: The store does not currently contain information about any upcoming exams or certifications. The only exam-related entries are either expired (entries 2-4 from March 2025) or describe a past professional exam (entry 5).
- `frbank:elena:elena_q10:FULL|d3628568bf1ac42e`: The store does not currently contain the answer. Elena's lease was locked in until March 2026, and today is April 3, 2026, which means that date has passed; however, the store does not contain information about her current lease status or any upcoming decisions she needs to make.
- `frbank:jake:jake_q11:FULL|131f342b26ed61a3`: The store does not currently contain information about upcoming exams or certifications. The exam entries are expired (the March 8, 2025 exam date has passed), and the active entries only confirm that Jake passed the journeyman electrician exam last year.
- `frbank:marcus:marcus_q10:FULL|b857289930965af8`: The store does not currently contain the answer. The alignment rack delivery scheduled for April 22 (entry [2]) has already passed as of today's date (2026-05-11), so it is no longer a future delivery.
- `frbank:marcus:marcus_q12:FULL|0f32feef9e8d196c`: The store does not currently contain the answer. The only meeting entry in the memory store is expired (from 462 days ago), so there is no active record of any upcoming meetings that Marcus needs to prepare for.
- `frbank:thanh:thanh_q02:CAT-ABLATED|7b07977c9ad1ce46`: The memory store shows that Thanh has a farm subject to government aquaculture inspections, but the specific inspection date (February 15, 2025) has expired and is no longer current. The store does not contain information about any upcoming inspection dates.
- `frbank:thanh:thanh_q02:FULL|40773509689c6a9e`: The memory store does not currently contain information about upcoming government inspections. While the store shows that Thanh has a farm subject to government aquaculture inspections, the specific inspection date entry (February 15, 2025) has expired and is no longer current.

### AUX-DS-A4-SPEND

Probe mini $0.0002; probe Haiku $0.0007; mini lane $0.1267; Haiku lane $0.4166; **total $0.5441** against the author's $8.00 cap.

<!-- R109-A4-PRINTED-BEGIN -->

### AUX-DS-A4-PRINTED — the forms the paper prints for Amendment 4 (R109; Section 8 and Appendix E.10), each read from `run/scores_amend4.json`

In-view correct (the 65): GPT-4.1 mini 37 → 48 (a rise of 11; Δ₁ +0.1692); Haiku 4.5 38 → 59 (a rise of 21; Δ₁ +0.3231). In-view abstentions: 15 → 3 and 38 → 3; Haiku 4.5's detector-correct abstentions 12 → 3. Correct over the 174 under retrieval alone: GPT-4.1 mini 46 → 56 (a rise of 10), Haiku 4.5 48 → 73 (a rise of 25); abstentions over the 221 licensed-item views 66 → 42 and 145 → 56 (the D.4 values are AUX-DS-AUDIT-IDENTITY). Scorable obligations under the oracle: GPT-4.1 mini stale 17 of 85 (D.4: 16; AUX-DS-AUDIT-RATES), all on views with an active stale line (17 of 35), none on the 50 tagged-only or empty views; Haiku 4.5 stale 23 of 85 (D.4: 19), first sentence 15, from tagged-only views 7; obligation abstentions under the oracle GPT-4.1 mini 12 against 21 under D.4 and Haiku 4.5 25 against 44 (D.4 values from the audit's `step7_length.json`). Expiry under the oracle (unscorable): GPT-4.1 mini abstains 10 of 14, Haiku 4.5 13. Spend $0.5441 of the $8.00 cap.

<!-- R109-A4-PRINTED-END -->

## 11. DS Amendment 5: the active duplicates tagged from the manifest (registrations/ADDENDUM_DS_AMENDMENT_5.md; descriptive)

### AUX-DS-A5-REG

Registered text sha256 **`a820195f93ffdf5b1d25c336b81bfcc59afaa27d67c5fd28ae1e97d9ae41e7a0`** (the bytes above the marker line), frozen at `54f4ade` on 2026-09-14, recorded here before the first call. Descriptive: no prediction, no bar, no verdict. Runner `tools/amend5_tagdup.py`.

### AUX-DS-A5-LOCK, AUX-DS-A5-POP, AUX-DS-A5-PROBE-MINI, AUX-DS-A5-PROBE-H45, AUX-DS-A5-PROJECTION (appended by `tools/amend5_tagdup.py score`)

Registration sha256 holds (frozen at `54f4ade`); the Amendment 4 header and user text reproduce AUX-DS-A4-LOCK (`e6c155364f8c69be...`); prompt digests as pinned. The duplicate rule: an active line whose text asserts the item's stale value by the item's own committed detector at TAU_GOLD (old-only coverage >= 0.50 with >= 2 shared tokens, new-only coverage < 0.34); the tag is the obligation's state (superseded, retracted). Population: 452 views, of which **74 change** (70 of the 422 with 124 lines tagged, 4 of the 30 LOOKUP-LIT views; 132 lines in all), covering 35 obligations (by state {"ret": 29, "sup": 45}; by the policies the views serve {"ALWAYS": 17, "LOOKUP": 17, "LOOKUP-ALL": 17, "LOOKUP-LIT": 32, "MODEL": 20, "MODEL-ALL": 20, "ORACLE": 35}); every count as registered. asserted on every changed view; unchanged views byte-identical (not re-run). Probe mini: served `gpt-4.1-mini-2025-04-14` (528 in / 19 out); probe Haiku 4.5: served `claude-haiku-4-5-20251001` (547 in / 29 out). Projection: mini $0.0204, Haiku $0.0576, sum with probes $0.0789 (x1.3 $0.1026) against the $2.00 cap; runs: True.

### AUX-DS-A5-STAGE2-MINI: Stage 2 under GPT-4.1 mini with the duplicates tagged, every policy, the committed detector, all states (452 rows: 74 new answers on the changed views, the rest Amendment 4's; new rows failed 0, served ['gpt-4.1-mini']); each row beside its Amendment 4 row

| answerer, policy | PN reached ∧ answered | stale use (all) | stale use, tagged reach | stale use, untagged reach | stale surfacing | stale use at TAU_GOLD (all) | at TAU_GOLD, tagged | at TAU_GOLD, untagged | successor use (of supersession) | both | PRESENT answered | PRESENT correct (TAU_GOLD) | at TAU_HI |
|---|---:|---|---|---|---:|---|---|---|---|---:|---:|---|---:|
| GPT-4.1 mini + header, duplicates tagged, ALWAYS | 54 | 1 / 54 = 0.0185 | 1 / 35 = 0.0286 | 0 / 19 = 0.0000 | 1 | 3 / 54 = 0.0556 | 1 / 35 = 0.0286 | 2 / 19 = 0.1053 | 1 / 22 = 0.0455 | 0 | 174 | 56 / 174 = 0.3218 | 20 |
| GPT-4.1 mini + header (Amendment 4, recorded), ALWAYS | 54 | 3 / 54 = 0.0556 | 2 / 35 = 0.0571 | 1 / 19 = 0.0526 | 3 | 11 / 54 = 0.2037 | 2 / 35 = 0.0571 | 9 / 19 = 0.4737 | 1 / 22 = 0.0455 | 0 | 174 | 56 / 174 = 0.3218 | 20 |
| GPT-4.1 mini + header, duplicates tagged, ORACLE | 99 | 1 / 99 = 0.0101 | 1 / 82 = 0.0122 | 0 / 17 = 0.0000 | 1 | 3 / 99 = 0.0303 | 3 / 82 = 0.0366 | 0 / 17 = 0.0000 | 1 / 63 = 0.0159 | 0 | 174 | 56 / 174 = 0.3218 | 20 |
| GPT-4.1 mini + header (Amendment 4, recorded), ORACLE | 99 | 2 / 99 = 0.0202 | 2 / 82 = 0.0244 | 0 / 17 = 0.0000 | 2 | 18 / 99 = 0.1818 | 11 / 82 = 0.1341 | 7 / 17 = 0.4118 | 1 / 63 = 0.0159 | 0 | 174 | 56 / 174 = 0.3218 | 20 |
| GPT-4.1 mini + header, duplicates tagged, MODEL | 74 | 1 / 74 = 0.0135 | 1 / 61 = 0.0164 | 0 / 13 = 0.0000 | 1 | 2 / 74 = 0.0270 | 1 / 61 = 0.0164 | 1 / 13 = 0.0769 | 1 / 49 = 0.0204 | 0 | 155 | 53 / 155 = 0.3419 | 20 |
| GPT-4.1 mini + header (Amendment 4, recorded), MODEL | 74 | 2 / 74 = 0.0270 | 2 / 61 = 0.0328 | 0 / 13 = 0.0000 | 2 | 11 / 74 = 0.1486 | 6 / 61 = 0.0984 | 5 / 13 = 0.3846 | 1 / 49 = 0.0204 | 0 | 155 | 53 / 155 = 0.3419 | 20 |
| GPT-4.1 mini + header, duplicates tagged, LOOKUP | 70 | 1 / 70 = 0.0143 | 1 / 61 = 0.0164 | 0 / 9 = 0.0000 | 1 | 1 / 70 = 0.0143 | 1 / 61 = 0.0164 | 0 / 9 = 0.0000 | 1 / 50 = 0.0200 | 0 | 146 | 48 / 146 = 0.3288 | 16 |
| GPT-4.1 mini + header (Amendment 4, recorded), LOOKUP | 70 | 2 / 70 = 0.0286 | 2 / 61 = 0.0328 | 0 / 9 = 0.0000 | 2 | 9 / 70 = 0.1286 | 6 / 61 = 0.0984 | 3 / 9 = 0.3333 | 1 / 50 = 0.0200 | 0 | 146 | 48 / 146 = 0.3288 | 16 |
| GPT-4.1 mini + header, duplicates tagged, MODEL-ALL | 74 | 1 / 74 = 0.0135 | 1 / 61 = 0.0164 | 0 / 13 = 0.0000 | 1 | 2 / 74 = 0.0270 | 1 / 61 = 0.0164 | 1 / 13 = 0.0769 | 1 / 49 = 0.0204 | 0 | 155 | 53 / 155 = 0.3419 | 20 |
| GPT-4.1 mini + header (Amendment 4, recorded), MODEL-ALL | 74 | 2 / 74 = 0.0270 | 1 / 61 = 0.0164 | 1 / 13 = 0.0769 | 2 | 12 / 74 = 0.1622 | 7 / 61 = 0.1148 | 5 / 13 = 0.3846 | 1 / 49 = 0.0204 | 0 | 155 | 53 / 155 = 0.3419 | 20 |
| GPT-4.1 mini + header, duplicates tagged, LOOKUP-ALL | 70 | 1 / 70 = 0.0143 | 1 / 61 = 0.0164 | 0 / 9 = 0.0000 | 1 | 1 / 70 = 0.0143 | 1 / 61 = 0.0164 | 0 / 9 = 0.0000 | 1 / 50 = 0.0200 | 0 | 146 | 47 / 146 = 0.3219 | 16 |
| GPT-4.1 mini + header (Amendment 4, recorded), LOOKUP-ALL | 70 | 1 / 70 = 0.0143 | 1 / 61 = 0.0164 | 0 / 9 = 0.0000 | 1 | 9 / 70 = 0.1286 | 6 / 61 = 0.0984 | 3 / 9 = 0.3333 | 1 / 50 = 0.0200 | 0 | 146 | 47 / 146 = 0.3219 | 16 |
| GPT-4.1 mini + header, duplicates tagged, LOOKUP-LIT | 94 | 1 / 94 = 0.0106 | 1 / 75 = 0.0133 | 0 / 19 = 0.0000 | 1 | 5 / 94 = 0.0532 | 3 / 75 = 0.0400 | 2 / 19 = 0.1053 | 1 / 62 = 0.0161 | 0 | 174 | 55 / 174 = 0.3161 | 19 |
| GPT-4.1 mini + header (Amendment 4, recorded), LOOKUP-LIT | 94 | 3 / 94 = 0.0319 | 2 / 75 = 0.0267 | 1 / 19 = 0.0526 | 3 | 17 / 94 = 0.1809 | 8 / 75 = 0.1067 | 9 / 19 = 0.4737 | 1 / 62 = 0.0161 | 0 | 174 | 55 / 174 = 0.3161 | 19 |

### AUX-DS-A5-CHANGED-MINI: the 74 changed views before (Amendment 4) and after (this amendment), GPT-4.1 mini

Stale at TAU_GOLD: **37 before, 8 after** of 74; rate difference (after minus before) -0.3919, item-level [-0.5135, -0.2838], persona-grouped [-0.6491, -0.1818] (10000 draws, seed 42, 14 personas; no bar). Stale at TAU_HI: 3 before, 0 after. Abstentions: 2 before, 9 after. Per policy (changed views only, stale at TAU_GOLD before -> after): ALWAYS 10 -> 2 of 17; ORACLE 17 -> 2 of 35; MODEL 10 -> 1 of 20; LOOKUP 8 -> 0 of 17; MODEL-ALL 11 -> 1 of 20; LOOKUP-ALL 8 -> 0 of 17; LOOKUP-LIT 16 -> 4 of 32.

Transitions (stale at TAU_GOLD):

- `frbank:bruna:bruna_q06:FULL|ec2b9f9d36cb55c2` (ret; ALWAYS, ORACLE, LOOKUP-LIT): 1 -> 0; before: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025 and also enrolled in a dry needling certification course a couple months ag; after: Bruna is currently enrolled in a dry needling certification course started a couple of months ago, indicating she is pursuing a new certification.
- `frbank:bruna:bruna_q06:SLOT-ABLATED|ec2b9f9d36cb55c2` (ret; ALWAYS, ORACLE, LOOKUP-LIT): 1 -> 0; before: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025 and also enrolled in a similar course a couple of months ago.; after: Yes, Bruna is currently enrolled in a dry needling certification course.
- `frbank:dariush:dariush_q04:SLOT-ABLATED|94c96d033edb1991` (ret; ALWAYS, LOOKUP-LIT): 1 -> 0; before: Dariush Farhadi is planning to open a second periodontal surgical suite in La Jolla on Prospect Street and is considering opening a second practice location the; after: Dariush Farhadi is considering opening a second practice location in La Jolla but has not confirmed opening it yet.
- `frbank:dariush:dariush_q04:SLOT-ABLATED|a821ddcdd5768637` (ret; MODEL-ALL): 1 -> 0; before: Yes, Dariush Farhadi is planning to open a second periodontal surgical suite in La Jolla on Prospect Street and is considering opening a second practice locatio; after: Dariush Farhadi is considering opening a second practice location in La Jolla and currently splits time between two practice locations, including the La Jolla l
- `frbank:dariush:dariush_q04:SLOT-ABLATED|d67c2ca9d3628556` (ret; ORACLE, MODEL): 1 -> 0; before: Yes, Dariush Farhadi is planning to open a second periodontal surgical suite in La Jolla on Prospect Street.; after: Dariush Farhadi is considering opening a second practice location in La Jolla but has not confirmed opening it yet.
- `frbank:elena:elena_q01:CAT-ABLATED|9a04fd185b365bcc` (sup; MODEL-ALL): 1 -> 0; before: Elena works on a nursing unit at a hospital, specifically as a pediatric nurse who works shifts helping children.; after: Elena works on a nursing unit with day and night shifts.
- `frbank:fatima:fatima_q06:FULL|d17a217596fb18b8` (ret; ORACLE): 1 -> 0; before: Fatima Al-Rashidi is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of their design brand and is developing it as a bran; after: Fatima Al-Rashidi is considering extending her firm into home fragrance products but has not launched any new products or brands yet.
- `frbank:ingrid:ingrid_q04:CAT-ABLATED|766a0fa846b1578c` (ret; ORACLE): 1 -> 0; before: Ingrid Solberg is not planning a sabbatical; her sabbatical at Woods Hole Oceanographic Institution is cancelled, but she plans to be a Guest Investigator there; after: Ingrid Solberg's sabbatical at Woods Hole Oceanographic Institution is cancelled, but she plans to be a Guest Investigator at Woods Hole from August 2026 throug
- `frbank:joonho:joonho_q04:SLOT-ABLATED|4ee9bd7760077288` (ret; LOOKUP-ALL): 1 -> 0; before: Yes, Park Joon-ho is currently writing a textbook on combinatorial game theory applied to go.; after: Yes, Park Joon-ho is currently working on a mathematics textbook about combinatorial game theory with twelve chapters.
- `frbank:joonho:joonho_q04:SLOT-ABLATED|8af5cc0b4f378251` (ret; ORACLE): 1 -> 0; before: Yes, Park Joon-ho is writing a textbook on combinatorial game theory applied to go and has been working on a mathematics textbook about combinatorial game theor; after: Yes, Joon-ho is working on a mathematics textbook about combinatorial game theory with twelve chapters.
- `frbank:joonho:joonho_q04:SLOT-ABLATED|94ed40c788ee6aa4` (ret; ALWAYS, MODEL, MODEL-ALL): 1 -> 0; before: Yes, Park Joon-ho is writing a textbook on combinatorial game theory applied to go and has been working on a mathematics textbook about combinatorial game theor; after: Yes, Joon-ho is currently working on a mathematics textbook about combinatorial game theory with twelve chapters.
- `frbank:joonho:joonho_q04:SLOT-ABLATED|ed91dffd8750aa41` (ret; LOOKUP, LOOKUP-LIT): 1 -> 0; before: Yes, Park Joon-ho is writing a textbook on combinatorial game theory applied to go and has been working on a mathematics textbook about combinatorial game theor; after: Yes, Joon-ho is currently working on a mathematics textbook about combinatorial game theory with twelve chapters.
- `frbank:mirri:mirri_q01:FULL|259ec0c4d9eaf246` (sup; MODEL-ALL, LOOKUP-ALL): 1 -> 0; before: Mirri Yunupingu does patrol work in Kakadu, focusing on the East Alligator River corridor.; after: Mirri Yunupingu has a patrol sector as part of their work responsibilities and does patrol work in Kakadu.
- `frbank:mirri:mirri_q01:FULL|28988d92b56155aa` (sup; ORACLE, MODEL, LOOKUP, LOOKUP-LIT): 1 -> 0; before: Mirri Yunupingu does patrol work in Kakadu, focusing on the East Alligator River corridor.; after: Mirri Yunupingu has a patrol sector as part of their work responsibilities, conducting patrol work in Kakadu.
- `frbank:mirri:mirri_q01:SLOT-ABLATED|2ae3f399928196d9` (sup; ORACLE, MODEL, LOOKUP, LOOKUP-LIT): 1 -> 0; before: Mirri Yunupingu patrols alone most days on the East Alligator corridor.; after: User has a patrol sector as part of their work responsibilities.
- `frbank:mirri:mirri_q01:SLOT-ABLATED|d78671dbbc630ccb` (sup; MODEL-ALL, LOOKUP-ALL): 1 -> 0; before: Mirri Yunupingu patrols alone most days on the East Alligator corridor.; after: Mirri Yunupingu has a patrol sector as part of their work responsibilities, but the current memory store does not specify the exact patrol route.
- `frbank:mirri:mirri_q04:FULL|31762bb09df8f889` (ret; ALWAYS, MODEL, LOOKUP, MODEL-ALL, LOOKUP-ALL, LOOKUP-LIT): 1 -> 0; before: Yes, Mirri Yunupingu is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.; after: Mirri Yunupingu currently wants to write a children's book but is not actively writing one.
- `frbank:mirri:mirri_q04:FULL|ee0ce2e8298516c7` (ret; ORACLE): 1 -> 0; before: Yes, Mirri Yunupingu is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.; after: Mirri Yunupingu currently wants to write a children's book, but is not actively writing one at the moment.
- `frbank:mirri:mirri_q04:SLOT-ABLATED|31762bb09df8f889` (ret; ALWAYS, MODEL, LOOKUP, MODEL-ALL, LOOKUP-ALL, LOOKUP-LIT): 1 -> 0; before: Yes, Mirri Yunupingu is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.; after: Mirri Yunupingu currently wants to write a children's book but is not actively writing one.
- `frbank:mirri:mirri_q04:SLOT-ABLATED|ee0ce2e8298516c7` (ret; ORACLE): 1 -> 0; before: Yes, Mirri Yunupingu is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.; after: Mirri Yunupingu currently wants to write a children's book, but is not actively writing one at the moment.
- `frbank:pan:pan_q01:CAT-ABLATED|6ea1fd8525e79794` (sup; MODEL-ALL, LOOKUP-ALL): 1 -> 0; before: Pan buys her rice every morning from Auntie Somjit at Khlong Toei market.; after: The store does not currently contain the answer.
- `frbank:pan:pan_q01:CAT-ABLATED|f436fcbaccfffbff` (sup; ALWAYS, ORACLE, MODEL, LOOKUP, LOOKUP-LIT): 1 -> 0; before: Pan buys her jasmine long grain rice from Auntie Somjit at Khlong Toei market.; after: The store does not currently contain the answer.
- `frbank:tom:tom_q06:FULL|20e59418eb9ecbe3` (ret; ORACLE): 1 -> 0; before: Tom had plans to convert the barn into a honey processing space but has now cancelled the project due to planning refusal and high cost, so he is not currently ; after: Tom is not currently planning any building projects; his barn conversion project was cancelled due to planning refusal and high cost.
- `frbank:valentina:valentina_q03:FULL|499f59436e5454af` (sup; ORACLE, MODEL, LOOKUP, LOOKUP-LIT): 1 -> 0; before: Yes, Valentina smokes cigarettes but is trying to quit.; after: The store does not currently contain the answer.
- `frbank:valentina:valentina_q03:FULL|e0bb5c533dbe6090` (sup; MODEL-ALL, LOOKUP-ALL): 1 -> 0; before: Yes, Valentina smokes cigarettes but is trying to quit.; after: The store does not currently contain the answer.
- `frbank:valentina:valentina_q03:SLOT-ABLATED|499f59436e5454af` (sup; ORACLE, MODEL, LOOKUP, LOOKUP-LIT): 1 -> 0; before: Yes, Valentina smokes cigarettes but is trying to quit.; after: The store does not currently contain the answer.
- `frbank:valentina:valentina_q03:SLOT-ABLATED|e0bb5c533dbe6090` (sup; MODEL-ALL, LOOKUP-ALL): 1 -> 0; before: Yes, Valentina smokes cigarettes but is trying to quit.; after: The store does not currently contain the answer.
- `frbank:valentina:valentina_q04:SLOT-ABLATED|3f501d1a7d87924e` (ret; ALWAYS, LOOKUP-LIT): 1 -> 0; before: Yes, Valentina is writing a book about the generation of journalists who reported on the narco years and the war, including their own father.; after: The store does not currently contain the answer.
- `frbank:valentina:valentina_q04:SLOT-ABLATED|c975e15427a8fbe2` (ret; ORACLE): 1 -> 0; before: Yes, Valentina Herrera is writing a book about the generation of journalists who reported on the narco years and the war, including their own father.; after: The store does not currently contain the answer.

### AUX-DS-A5-SOURCE-MINI: the source split on the changed views after the rewrite (no active line asserts the stale value on any of them, asserted): {"src=tagged_only|stale=False": 66, "src=tagged_only|stale=True": 8}

### AUX-DS-A5-STAGE2-H45: Stage 2 under Claude Haiku 4.5 with the duplicates tagged, every policy, the committed detector, all states (452 rows: 74 new answers on the changed views, the rest Amendment 4's; new rows failed 0, served ['claude-haiku-4-5-20251001']); each row beside its Amendment 4 row

| answerer, policy | PN reached ∧ answered | stale use (all) | stale use, tagged reach | stale use, untagged reach | stale surfacing | stale use at TAU_GOLD (all) | at TAU_GOLD, tagged | at TAU_GOLD, untagged | successor use (of supersession) | both | PRESENT answered | PRESENT correct (TAU_GOLD) | at TAU_HI |
|---|---:|---|---|---|---:|---|---|---|---|---:|---:|---|---:|
| Claude Haiku 4.5 + header, duplicates tagged, ALWAYS | 54 | 4 / 54 = 0.0741 | 4 / 35 = 0.1143 | 0 / 19 = 0.0000 | 4 | 11 / 54 = 0.2037 | 7 / 35 = 0.2000 | 4 / 19 = 0.2105 | 1 / 22 = 0.0455 | 0 | 174 | 73 / 174 = 0.4195 | 27 |
| Claude Haiku 4.5 + header (Amendment 4, recorded), ALWAYS | 54 | 5 / 54 = 0.0926 | 4 / 35 = 0.1143 | 1 / 19 = 0.0526 | 5 | 18 / 54 = 0.3333 | 7 / 35 = 0.2000 | 11 / 19 = 0.5789 | 1 / 22 = 0.0455 | 0 | 174 | 73 / 174 = 0.4195 | 27 |
| Claude Haiku 4.5 + header, duplicates tagged, ORACLE | 99 | 5 / 99 = 0.0505 | 5 / 82 = 0.0610 | 0 / 17 = 0.0000 | 5 | 22 / 99 = 0.2222 | 18 / 82 = 0.2195 | 4 / 17 = 0.2353 | 2 / 63 = 0.0317 | 0 | 174 | 73 / 174 = 0.4195 | 27 |
| Claude Haiku 4.5 + header (Amendment 4, recorded), ORACLE | 99 | 7 / 99 = 0.0707 | 7 / 82 = 0.0854 | 0 / 17 = 0.0000 | 9 | 32 / 99 = 0.3232 | 25 / 82 = 0.3049 | 7 / 17 = 0.4118 | 2 / 63 = 0.0317 | 0 | 174 | 73 / 174 = 0.4195 | 27 |
| Claude Haiku 4.5 + header, duplicates tagged, MODEL | 74 | 6 / 74 = 0.0811 | 6 / 61 = 0.0984 | 0 / 13 = 0.0000 | 6 | 17 / 74 = 0.2297 | 13 / 61 = 0.2131 | 4 / 13 = 0.3077 | 1 / 49 = 0.0204 | 0 | 155 | 64 / 155 = 0.4129 | 24 |
| Claude Haiku 4.5 + header (Amendment 4, recorded), MODEL | 74 | 8 / 74 = 0.1081 | 8 / 61 = 0.1311 | 0 / 13 = 0.0000 | 10 | 27 / 74 = 0.3649 | 19 / 61 = 0.3115 | 8 / 13 = 0.6154 | 1 / 49 = 0.0204 | 0 | 155 | 64 / 155 = 0.4129 | 24 |
| Claude Haiku 4.5 + header, duplicates tagged, LOOKUP | 70 | 6 / 70 = 0.0857 | 6 / 61 = 0.0984 | 0 / 9 = 0.0000 | 6 | 16 / 70 = 0.2286 | 13 / 61 = 0.2131 | 3 / 9 = 0.3333 | 1 / 50 = 0.0200 | 0 | 146 | 58 / 146 = 0.3973 | 21 |
| Claude Haiku 4.5 + header (Amendment 4, recorded), LOOKUP | 70 | 7 / 70 = 0.1000 | 7 / 61 = 0.1148 | 0 / 9 = 0.0000 | 9 | 24 / 70 = 0.3429 | 18 / 61 = 0.2951 | 6 / 9 = 0.6667 | 1 / 50 = 0.0200 | 0 | 146 | 58 / 146 = 0.3973 | 21 |
| Claude Haiku 4.5 + header, duplicates tagged, MODEL-ALL | 74 | 4 / 74 = 0.0541 | 4 / 61 = 0.0656 | 0 / 13 = 0.0000 | 4 | 13 / 74 = 0.1757 | 9 / 61 = 0.1475 | 4 / 13 = 0.3077 | 2 / 49 = 0.0408 | 0 | 155 | 64 / 155 = 0.4129 | 24 |
| Claude Haiku 4.5 + header (Amendment 4, recorded), MODEL-ALL | 74 | 7 / 74 = 0.0946 | 6 / 61 = 0.0984 | 1 / 13 = 0.0769 | 9 | 23 / 74 = 0.3108 | 14 / 61 = 0.2295 | 9 / 13 = 0.6923 | 2 / 49 = 0.0408 | 0 | 155 | 64 / 155 = 0.4129 | 24 |
| Claude Haiku 4.5 + header, duplicates tagged, LOOKUP-ALL | 70 | 4 / 70 = 0.0571 | 4 / 61 = 0.0656 | 0 / 9 = 0.0000 | 4 | 12 / 70 = 0.1714 | 9 / 61 = 0.1475 | 3 / 9 = 0.3333 | 2 / 50 = 0.0400 | 0 | 146 | 58 / 146 = 0.3973 | 21 |
| Claude Haiku 4.5 + header (Amendment 4, recorded), LOOKUP-ALL | 70 | 6 / 70 = 0.0857 | 6 / 61 = 0.0984 | 0 / 9 = 0.0000 | 8 | 20 / 70 = 0.2857 | 14 / 61 = 0.2295 | 6 / 9 = 0.6667 | 2 / 50 = 0.0400 | 0 | 146 | 58 / 146 = 0.3973 | 21 |
| Claude Haiku 4.5 + header, duplicates tagged, LOOKUP-LIT | 94 | 5 / 94 = 0.0532 | 5 / 75 = 0.0667 | 0 / 19 = 0.0000 | 5 | 18 / 94 = 0.1915 | 14 / 75 = 0.1867 | 4 / 19 = 0.2105 | 1 / 62 = 0.0161 | 0 | 174 | 72 / 174 = 0.4138 | 28 |
| Claude Haiku 4.5 + header (Amendment 4, recorded), LOOKUP-LIT | 94 | 8 / 94 = 0.0851 | 7 / 75 = 0.0933 | 1 / 19 = 0.0526 | 10 | 31 / 94 = 0.3298 | 20 / 75 = 0.2667 | 11 / 19 = 0.5789 | 1 / 62 = 0.0161 | 0 | 174 | 72 / 174 = 0.4138 | 28 |

### AUX-DS-A5-CHANGED-H45: the 74 changed views before (Amendment 4) and after (this amendment), Claude Haiku 4.5

Stale at TAU_GOLD: **38 before, 12 after** of 74; rate difference (after minus before) -0.3514, item-level [-0.4595, -0.2432], persona-grouped [-0.5942, -0.1429] (10000 draws, seed 42, 14 personas; no bar). Stale at TAU_HI: 7 before, 0 after. Abstentions: 12 before, 27 after. Per policy (changed views only, stale at TAU_GOLD before -> after): ALWAYS 9 -> 2 of 17; ORACLE 16 -> 6 of 35; MODEL 12 -> 2 of 20; LOOKUP 9 -> 1 of 17; MODEL-ALL 12 -> 2 of 20; LOOKUP-ALL 9 -> 1 of 17; LOOKUP-LIT 17 -> 4 of 32.

Transitions (stale at TAU_GOLD):

- `frbank:dariush:dariush_q04:SLOT-ABLATED|94c96d033edb1991` (ret; ALWAYS, LOOKUP-LIT): 1 -> 0; before: Yes, Dariush is opening a second practice in La Jolla. According to the memory store, he is planning to open a second periodontal surgical suite in La Jolla on ; after: Yes, according to the active entries, Dariush is opening a second practice location in La Jolla and currently splits time between two practice locations, spendi
- `frbank:dariush:dariush_q04:SLOT-ABLATED|a821ddcdd5768637` (ret; MODEL-ALL): 1 -> 0; before: Yes, according to the memory store, Dariush is planning to open a second periodontal surgical suite in La Jolla on Prospect Street. He currently splits time bet; after: Yes, according to the memory store, Dariush is considering opening a second practice location in La Jolla. Additionally, he currently splits time between two pr
- `frbank:elena:elena_q01:CAT-ABLATED|20a14635103a2dba` (sup; ORACLE): 1 -> 0; before: The store does not currently contain the answer. While entries [6] and [7] indicate Elena works at Lurie Children's hospital, both are marked as superseded and ; after: The store does not currently contain the answer. While there are active entries indicating Elena works on a nursing unit with day and night shifts in 12-hour sh
- `frbank:elena:elena_q01:CAT-ABLATED|90c444c941500e93` (sup; MODEL, LOOKUP-LIT): 1 -> 0; before: The store does not currently contain the answer. While there are superseded entries indicating Elena previously worked at Lurie Children's hospital, the active ; after: The store does not currently contain the answer. While there is an active entry stating Elena works on a nursing unit with day and night shifts, the specific em
- `frbank:ingrid:ingrid_q01:SLOT-ABLATED|2b00d3d299fee09e` (sup; MODEL-ALL, LOOKUP-ALL): 1 -> 0; before: According to the memory store, Ingrid's primary research interest includes kelp aquaculture and nearshore habitat monitoring. The store does not contain a curre; after: Ingrid's primary research interest includes kelp aquaculture and nearshore habitat monitoring, as recorded in her active memory entry.
- `frbank:ingrid:ingrid_q01:SLOT-ABLATED|f0a292a92f80ae35` (sup; ORACLE, MODEL, LOOKUP, LOOKUP-LIT): 1 -> 0; before: According to the memory store, Ingrid's primary research interest includes kelp aquaculture and nearshore habitat monitoring. While she previously focused on Ar; after: Ingrid's primary research interest includes kelp aquaculture and nearshore habitat monitoring. She conducts research at coastal field sites in the Arctic.
- `frbank:ingrid:ingrid_q04:CAT-ABLATED|9e515bcb2cb596d9` (ret; ALWAYS, LOOKUP-LIT): 1 -> 0; before: The memory store contains conflicting active entries about Ingrid's sabbatical plans. Entry [4] indicates she plans to be a Guest Investigator at Woods Hole Oce; after: No. While Ingrid has an active entry stating she plans to be a Guest Investigator at Woods Hole Oceanographic Institution from August 2026 through July 2027, th
- `frbank:jerome:jerome_q02:CAT-ABLATED|5953d48a3007c7c2` (sup; ORACLE): 1 -> 0; before: Jerome drives for ABF as a company driver. However, there is also an active entry indicating he has been driving for Southeastern Freight Lines out of Atlanta f; after: Jerome drives for ABF as a company driver.
- `frbank:joonho:joonho_q04:SLOT-ABLATED|4ee9bd7760077288` (ret; LOOKUP-ALL): 1 -> 0; before: Yes, Park Joon-ho is writing a textbook on combinatorial game theory applied to go, which has twelve chapters and he intends to publish initially with a Korean ; after: Yes, Park Joon-ho is writing a mathematics textbook about combinatorial game theory with twelve chapters.
- `frbank:joonho:joonho_q04:SLOT-ABLATED|8af5cc0b4f378251` (ret; ORACLE): 1 -> 0; before: Yes, Park Joon-ho is writing a textbook on combinatorial game theory applied to go, which has twelve chapters and he intends to publish initially with a Korean ; after: Yes, Park Joon-ho is writing a mathematics textbook about combinatorial game theory with twelve chapters.
- `frbank:joonho:joonho_q04:SLOT-ABLATED|94ed40c788ee6aa4` (ret; ALWAYS, MODEL, MODEL-ALL): 1 -> 0; before: Yes, Park Joon-ho is writing a textbook on combinatorial game theory applied to go, which has twelve chapters.; after: Yes, Park Joon-ho is writing a mathematics textbook about combinatorial game theory with twelve chapters.
- `frbank:joonho:joonho_q04:SLOT-ABLATED|ed91dffd8750aa41` (ret; LOOKUP, LOOKUP-LIT): 1 -> 0; before: Yes, Park Joon-ho is writing a textbook on combinatorial game theory applied to go, which has twelve chapters and he intends to publish initially with a Korean ; after: Yes, Park Joon-ho is writing a mathematics textbook about combinatorial game theory with twelve chapters, which he intends to publish initially with a Korean ac
- `frbank:mirri:mirri_q01:FULL|259ec0c4d9eaf246` (sup; MODEL-ALL, LOOKUP-ALL): 1 -> 0; before: Mirri covers the East Alligator River corridor as part of their patrol work in Kakadu, patrolling this sector three days a week on Tuesday, Thursday, and Saturd; after: The store does not currently contain the answer. While active entries indicate that Mirri has a patrol sector and does patrol work in Kakadu on a schedule of th
- `frbank:mirri:mirri_q01:FULL|28988d92b56155aa` (sup; ORACLE, MODEL, LOOKUP, LOOKUP-LIT): 1 -> 0; before: Mirri covers the East Alligator River corridor as part of their patrol work in Kakadu. The patrol sector involves driving on varied terrain including sand, corr; after: The store does not currently contain the answer. While active entries indicate that Mirri has a patrol sector as part of work responsibilities and does patrol w
- `frbank:mirri:mirri_q01:SLOT-ABLATED|2ae3f399928196d9` (sup; ORACLE, MODEL, LOOKUP, LOOKUP-LIT): 1 -> 0; before: Mirri patrols the East Alligator corridor, typically alone most days. The patrol route involves varied terrain including sand, corrugated dirt, clay after rain,; after: The store does not currently contain the answer. The most recent active entries describe that the user has a patrol sector and patrols three days a week (Tuesda
- `frbank:mirri:mirri_q01:SLOT-ABLATED|d78671dbbc630ccb` (sup; MODEL-ALL, LOOKUP-ALL): 1 -> 0; before: Mirri patrols the East Alligator corridor, patrolling alone most days on this route as part of work responsibilities with a schedule of three days a week (Tuesd; after: The store does not currently contain the answer. The entry describing the East Alligator corridor patrol route is superseded, and the current active entries onl
- `frbank:mirri:mirri_q04:FULL|31762bb09df8f889` (ret; ALWAYS, MODEL, LOOKUP, MODEL-ALL, LOOKUP-ALL, LOOKUP-LIT): 1 -> 0; before: Yes, Mirri is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.; after: The store does not currently contain the answer. Entry [1] states the user wants to write a children's book (active), but entries describing the user actively w
- `frbank:mirri:mirri_q04:SLOT-ABLATED|31762bb09df8f889` (ret; ALWAYS, MODEL, LOOKUP, MODEL-ALL, LOOKUP-ALL, LOOKUP-LIT): 1 -> 0; before: Yes, Mirri is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.; after: The store does not currently contain the answer. Entry [1] states the user wants to write a children's book (active), but entries describing the user as activel
- `frbank:valentina:valentina_q03:FULL|499f59436e5454af` (sup; ORACLE, MODEL, LOOKUP, LOOKUP-LIT): 1 -> 0; before: Yes, Valentina smokes cigarettes and is trying to quit, according to an active entry in her memory store.; after: The store does not currently contain an active entry that directly answers whether Valentina currently smokes. The entries that describe her smoking habits (ent
- `frbank:valentina:valentina_q03:FULL|e0bb5c533dbe6090` (sup; MODEL-ALL, LOOKUP-ALL): 1 -> 0; before: Yes, according to the memory store, Valentina smokes cigarettes and is trying to quit.; after: The store does not currently contain the answer. The most recent entries about Valentina's smoking habit are superseded (entries [5] and [10-11]), and no active
- `frbank:valentina:valentina_q03:SLOT-ABLATED|499f59436e5454af` (sup; ORACLE, MODEL, LOOKUP, LOOKUP-LIT): 1 -> 0; before: Yes, Valentina smokes cigarettes and is trying to quit, according to an active entry in her memory store.; after: The store does not currently contain an active entry that directly answers whether Valentina currently smokes. The entries that describe her smoking habits (ent
- `frbank:valentina:valentina_q03:SLOT-ABLATED|e0bb5c533dbe6090` (sup; MODEL-ALL, LOOKUP-ALL): 1 -> 0; before: Yes, according to the memory store, Valentina smokes cigarettes and is trying to quit.; after: The store does not currently contain the answer. The most recent entries about Valentina's smoking habit are superseded (entries [5] and [10-11]), and no active
- `frbank:valentina:valentina_q04:FULL|07c08bad80a3cc48` (ret; ORACLE): 1 -> 0; before: The memory store contains conflicting active entries about this topic. Entry [4] states that Valentina decided to stop writing a book about journalists covering; after: No, Valentina is not writing a book. According to her active memory entry, she decided to stop writing a book about journalists covering narco years in order to
- `frbank:valentina:valentina_q04:FULL|7c2e65cf3afde185` (ret; ALWAYS, MODEL, MODEL-ALL, LOOKUP-LIT): 1 -> 0; before: The memory store contains conflicting active entries about this project. Entry [4] states that Valentina decided to stop writing a book about journalists coveri; after: No, Valentina is not writing a book. According to her active memory entry, she decided to stop writing a book about journalists covering narco years in order to
- `frbank:valentina:valentina_q04:SLOT-ABLATED|3f501d1a7d87924e` (ret; ALWAYS, LOOKUP-LIT): 1 -> 0; before: Yes, Valentina is writing a book about the generation of Colombian journalists who reported during the narco years and the war, including their own father.; after: The store does not currently contain the answer. All entries about Valentina writing a book have been retracted, and the only active entry in the store concerns
- `frbank:valentina:valentina_q04:SLOT-ABLATED|c975e15427a8fbe2` (ret; ORACLE): 1 -> 0; before: Yes, Valentina is writing a book about the generation of Colombian journalists who reported during the narco years and the war, including her own father's exper; after: The store does not currently contain the answer. All entries describing Valentina's book writing project have been retracted, so they do not reflect her current

### AUX-DS-A5-SOURCE-H45: the source split on the changed views after the rewrite (no active line asserts the stale value on any of them, asserted): {"src=tagged_only|stale=False": 62, "src=tagged_only|stale=True": 12}

### AUX-DS-A5-SPEND

Probe mini $0.0002; probe Haiku $0.0007; mini lane $0.0228; Haiku lane $0.0740; **total $0.0977** against the author's $2.00 cap.

### AUX-DS-A5-FIRSTSENT-MINI, AUX-DS-A5-FIRSTSENT-H45: stale use at TAU_GOLD on the scorable (supersession + retraction) reached obligations, the registered flag on the whole answer beside the flag on the first sentence, Amendment 5 with Amendment 4 beside (the author's addition of 2026-09-14; appended by `tools/amend5_tagdup.py firstsent`)

| answerer | policy | scorable | A5 registered (Wilson) | A5 first sentence (Wilson) | A4 registered | A4 first sentence |
|---|---|---:|---|---|---:|---:|
| GPT-4.1 mini | ALWAYS | 42 | 2 / 42 = 0.0476 [0.0132, 0.1579] | 2 / 42 = 0.0476 [0.0132, 0.1579] | 10 / 42 | 10 / 42 |
| GPT-4.1 mini | ORACLE | 85 | 2 / 85 = 0.0235 [0.0065, 0.0818] | 2 / 85 = 0.0235 [0.0065, 0.0818] | 17 / 85 | 17 / 85 |
| GPT-4.1 mini | MODEL | 62 | 1 / 62 = 0.0161 [0.0029, 0.0859] | 1 / 62 = 0.0161 [0.0029, 0.0859] | 10 / 62 | 10 / 62 |
| GPT-4.1 mini | LOOKUP | 58 | 0 / 58 = 0.0000 [-0.0, 0.0621] | 0 / 58 = 0.0000 [-0.0, 0.0621] | 8 / 58 | 8 / 58 |
| GPT-4.1 mini | MODEL-ALL | 62 | 1 / 62 = 0.0161 [0.0029, 0.0859] | 1 / 62 = 0.0161 [0.0029, 0.0859] | 11 / 62 | 11 / 62 |
| GPT-4.1 mini | LOOKUP-ALL | 58 | 0 / 58 = 0.0000 [-0.0, 0.0621] | 0 / 58 = 0.0000 [-0.0, 0.0621] | 8 / 58 | 8 / 58 |
| GPT-4.1 mini | LOOKUP-LIT | 82 | 4 / 82 = 0.0488 [0.0191, 0.1188] | 4 / 82 = 0.0488 [0.0191, 0.1188] | 16 / 82 | 16 / 82 |

Residual on the 74 changed views, GPT-4.1 mini: 8 stale on the whole answer, 8 on the first sentence, 0 only beyond it; source tagged lines only (no active stale line survives the rewrite; AUX-DS-A5-SOURCE).
- `frbank:fatima:fatima_q06:FULL|71a7fb9cbf2ef87e`: Fatima Al-Rashidi is considering extending her firm into home fragrance products and has decided that launching the Oud and Geometry fragrance line would require building a second business with its own supply chain, regu
- `frbank:fatima:fatima_q06:FULL|76820499dbdbc738`: Fatima is considering extending her firm into home fragrance products and has decided that launching the Oud and Geometry fragrance line would require building a second business with its own supply chain, regulatory comp
- `frbank:fatima:fatima_q06:FULL|ef304ed5812e1f0b`: Fatima Al-Rashidi is considering extending her firm into home fragrance products and has decided that launching the Oud and Geometry fragrance line would require building a second business with its own supply chain, regu
- `frbank:ingrid:ingrid_q04:SLOT-ABLATED|b17273a99f545c47`: Ingrid is not planning a sabbatical; her sabbatical at Woods Hole Oceanographic Institution is cancelled, but she plans to be a Guest Investigator there from August 2026 through July 2027.
- `frbank:kofi:kofi_q01:FULL|859bafc244b8d70e`: Kofi's cooperative sells cocoa through Kuapa.
- `frbank:kofi:kofi_q01:FULL|a6614376f94a4437`: Kofi's cooperative sells cocoa through Kuapa.
- `frbank:kofi:kofi_q01:SLOT-ABLATED|859bafc244b8d70e`: Kofi's cooperative sells cocoa through Kuapa.
- `frbank:kofi:kofi_q01:SLOT-ABLATED|a6614376f94a4437`: Kofi's cooperative sells cocoa through Kuapa.
| Claude Haiku 4.5 | ALWAYS | 42 | 3 / 42 = 0.0714 [0.0246, 0.1901] | 0 / 42 = 0.0000 [0.0, 0.0838] | 10 / 42 | 6 / 42 |
| Claude Haiku 4.5 | ORACLE | 85 | 13 / 85 = 0.1529 [0.0916, 0.2443] | 7 / 85 = 0.0824 [0.0405, 0.1604] | 23 / 85 | 15 / 85 |
| Claude Haiku 4.5 | MODEL | 62 | 9 / 62 = 0.1452 [0.0783, 0.2534] | 3 / 62 = 0.0484 [0.0166, 0.1329] | 19 / 62 | 12 / 62 |
| Claude Haiku 4.5 | LOOKUP | 58 | 8 / 58 = 0.1379 [0.0716, 0.2493] | 3 / 58 = 0.0517 [0.0177, 0.1414] | 16 / 58 | 11 / 58 |
| Claude Haiku 4.5 | MODEL-ALL | 62 | 5 / 62 = 0.0806 [0.0349, 0.1753] | 1 / 62 = 0.0161 [0.0029, 0.0859] | 15 / 62 | 11 / 62 |
| Claude Haiku 4.5 | LOOKUP-ALL | 58 | 4 / 58 = 0.0690 [0.0271, 0.1643] | 1 / 58 = 0.0172 [0.0031, 0.0914] | 12 / 58 | 9 / 58 |
| Claude Haiku 4.5 | LOOKUP-LIT | 82 | 10 / 82 = 0.1220 [0.0676, 0.2101] | 5 / 82 = 0.0610 [0.0263, 0.1349] | 23 / 82 | 15 / 82 |

Residual on the 74 changed views, Claude Haiku 4.5: 12 stale on the whole answer, 6 on the first sentence, 6 only beyond it; source tagged lines only (no active stale line survives the rewrite; AUX-DS-A5-SOURCE).
- `frbank:fatima:fatima_q06:FULL|71a7fb9cbf2ef87e`: The store does not currently contain a clear answer to this question. While there is an active entry indicating Fatima is considering extending her firm into home fragrance products, the retracted entries show she previo
- `frbank:fatima:fatima_q06:FULL|76820499dbdbc738`: The store does not currently contain the answer. While there is an active entry indicating Fatima is considering extending her firm into home fragrance products, and another active entry describing the complexity of laun
- `frbank:fatima:fatima_q06:FULL|d17a217596fb18b8`: The store does not currently contain a definitive answer to this question. While Fatima is considering extending her firm into home fragrance products (active entry), she decided that launching the Oud and Geometry fragr
- `frbank:fatima:fatima_q06:FULL|ef304ed5812e1f0b`: The store does not currently contain a clear answer to this question. While there is an active entry indicating Fatima is considering extending her firm into home fragrance products, the entries describing specific produ
- `frbank:kofi:kofi_q01:FULL|859bafc244b8d70e`: Kofi's cooperative sells cocoa through Kuapa. He is the chairman of a cooperative of 147 families that uses this selling method.
- `frbank:kofi:kofi_q01:FULL|a6614376f94a4437`: Kofi's cooperative sells cocoa through Kuapa.
- `frbank:kofi:kofi_q01:SLOT-ABLATED|859bafc244b8d70e`: Kofi's cooperative sells cocoa through Kuapa. He is the chairman of a cooperative of 147 families that uses this selling method.
- `frbank:kofi:kofi_q01:SLOT-ABLATED|a6614376f94a4437`: Kofi's cooperative sells cocoa through Kuapa.
- `frbank:mirri:mirri_q04:FULL|ee0ce2e8298516c7`: The store shows that Mirri wants to write a children's book (active entry from 425 days ago) and had an idea for a bilingual children's book with stories from their country in their language and in English (active entry 
- `frbank:mirri:mirri_q04:SLOT-ABLATED|ee0ce2e8298516c7`: The store shows that Mirri wants to write a children's book (active entry from 425 days ago) and had an idea for a bilingual children's book with stories from their country in their language and in English (active entry 
- `frbank:pan:pan_q01:CAT-ABLATED|6ea1fd8525e79794`: The store does not currently contain the answer. The entries that specify where Pan buys rice (from Auntie Somjit at Khlong Toei market) have been superseded and are no longer current information.
- `frbank:pan:pan_q01:CAT-ABLATED|f436fcbaccfffbff`: The store does not currently contain the answer. The entries that specify where Pan buys rice (from Auntie Somjit at Khlong Toei market) are marked as superseded and therefore do not reflect her current situation.

## 13. DS Amendment 7: an obligation-reported detector and a composite per policy (registrations/ADDENDUM_DS_AMENDMENT_7.md; descriptive; $0)

### AUX-DS-A7-REG

Registered text sha256 **`6566bf097f41ccd289c888f4c467d64786eea3230b7f23f279377b6c8a1a7201`** (the bytes above the marker line), frozen at `12c63f9` on 2026-09-15, recorded here before any scoring. Descriptive: no prediction, no bar, no verdict; no model call. Runner `tools/amend7_reported.py`.

### AUX-DS-A7-RULE

An answer reports the obligation iff (a) it names the lifecycle state, a word-boundary match on the closed list superseded, retracted, expired, no longer, not current, outdated, out of date, cancelled, canceled, replaced, withdrawn, discontinued, past (or 'is / was / has / had passed'), with previous / previously / former / formerly counting only in a sentence that also carries one of those, and (b) the committed detector's stale flag at TAU_GOLD on the whole answer is false; on an expiry obligation (b) is unscorable and (a) alone prints, marked. Word list and pattern sha256 `835329c6650279e0e7f2ca8c5a62bd7d9742f34678d3b1b8cbe0cdfe8962cbeb`; not revised after the sheet is read.

### AUX-DS-A7-REPORTED, AUX-DS-A7-SPLIT, AUX-DS-A7-COMPOSITE (appended by `tools/amend7_reported.py score`; rule sha256 `835329c6650279e0...`)

Obligation reported per answerer, prompt variant and policy: the count and rate over the reached and answered obligations (all states; the expiry obligations by condition (a) alone), Wilson interval; beside it the registered stale flag at TAU_GOLD on the scorable set; the split; and the composite over the 661 in the coverage-gate reading (a licensed item counts if correct at 0.50; an obligation if reached, answered and reported; an absent item if the registered coverage gate abstained on it under that policy: zero under ALWAYS, which has no gate, and 383 of 383 under ORACLE, whose gate is the label itself, a settled reading recorded as D-DS-A7-1 against section A7.4's 'zero under ALWAYS and ORACLE').

| variant | answerer | policy | reached | reported (rate; Wilson) | of which expiry by (a) alone | stale at 0.50 (scorable) | reported and abstaining / answering / with successor | names the state but gives the stale value | stale without naming | neither | composite: licensed correct + reported + absent abstained = of 661 |
|---|---|---|---:|---|---|---:|---|---:|---:|---:|---|
| D4 | MINI | ALWAYS | 54 | 1 (0.0185; [0.0033, 0.0977]) | 0 / 12 | 8 / 42 | 0 / 1 / 0 | 1 | 7 | 44 | 46 of 174 + 1 of 104 + 0 of 383 = **47** of 661 |
| D4 | MINI | ORACLE | 99 | 1 (0.0101; [0.0018, 0.055]) | 0 / 14 | 16 / 85 | 0 / 1 / 0 | 3 | 13 | 81 | 46 of 174 + 1 of 104 + 383 of 383 = **430** of 661 |
| D4 | MINI | MODEL | 74 | 0 (0.0000; [0.0, 0.0493]) | 0 / 12 | 8 / 62 | 0 / 0 / 0 | 0 | 8 | 65 | 44 of 174 + 0 of 104 + 172 of 383 = **216** of 661 |
| D4 | MINI | LOOKUP | 70 | 0 (0.0000; [0.0, 0.052]) | 0 / 12 | 6 / 58 | 0 / 0 / 0 | 0 | 6 | 63 | 40 of 174 + 0 of 104 + 174 of 383 = **214** of 661 |
| D4 | MINI | MODEL-ALL | 74 | 0 (0.0000; [0.0, 0.0493]) | 0 / 12 | 8 / 62 | 0 / 0 / 0 | 0 | 8 | 65 | 44 of 174 + 0 of 104 + 172 of 383 = **216** of 661 |
| D4 | MINI | LOOKUP-ALL | 70 | 0 (0.0000; [0.0, 0.052]) | 0 / 12 | 5 / 58 | 0 / 0 / 0 | 0 | 5 | 64 | 39 of 174 + 0 of 104 + 174 of 383 = **213** of 661 |
| D4 | MINI | LOOKUP-LIT | 6 | 0 (0.0000; [0.0, 0.3903]) | 0 / 0 | 2 / 6 | 0 / 0 / 0 | 0 | 2 | 4 | 3 of 174 + 0 of 104 + 0 of 383 = **3** of 661 |
| A1-allstates-gate | MINI | MODEL-ALL-V3 | 78 | 0 (0.0000; [0.0, 0.0469]) | 0 / 13 | 11 / 65 | 0 / 0 / 0 | 2 | 9 | 66 | 44 of 174 + 0 of 104 + 0 of 383 = **44** of 661 |
| D4 | H45 | ALWAYS | 54 | 19 (0.3519; [0.2382, 0.4852]) | 8 / 12 | 11 / 42 | 17 / 2 / 0 | 2 | 9 | 21 | 48 of 174 + 19 of 104 + 0 of 383 = **67** of 661 |
| D4 | H45 | ORACLE | 99 | 24 (0.2424; [0.1687, 0.3354]) | 9 / 14 | 19 / 85 | 21 / 3 / 0 | 8 | 11 | 53 | 48 of 174 + 24 of 104 + 383 of 383 = **455** of 661 |
| D4 | H45 | MODEL | 74 | 18 (0.2432; [0.1598, 0.3521]) | 7 / 12 | 16 / 62 | 17 / 1 / 0 | 8 | 8 | 37 | 45 of 174 + 18 of 104 + 172 of 383 = **235** of 661 |
| D4 | H45 | LOOKUP | 70 | 18 (0.2571; [0.1693, 0.3703]) | 8 / 12 | 11 / 58 | 17 / 1 / 0 | 5 | 6 | 38 | 41 of 174 + 18 of 104 + 174 of 383 = **233** of 661 |
| D4 | H45 | MODEL-ALL | 74 | 20 (0.2703; [0.1823, 0.3809]) | 7 / 12 | 13 / 62 | 19 / 1 / 0 | 4 | 9 | 38 | 45 of 174 + 20 of 104 + 172 of 383 = **237** of 661 |
| D4 | H45 | LOOKUP-ALL | 70 | 18 (0.2571; [0.1693, 0.3703]) | 8 / 12 | 10 / 58 | 17 / 1 / 0 | 3 | 7 | 39 | 40 of 174 + 18 of 104 + 174 of 383 = **232** of 661 |
| D4 | H45 | LOOKUP-LIT | 94 | 22 (0.2340; [0.1599, 0.329]) | 8 / 12 | 21 / 82 | 20 / 2 / 0 | 8 | 13 | 48 | 47 of 174 + 22 of 104 + 0 of 383 = **69** of 661 |
| A3-instruction | MINI | ALWAYS | 54 | 1 (0.0185; [0.0033, 0.0977]) | 1 / 12 | 9 / 42 | 0 / 1 / 0 | 2 | 7 | 44 | 47 of 174 + 1 of 104 + 0 of 383 = **48** of 661 |
| A3-instruction | MINI | ORACLE | 99 | 3 (0.0303; [0.0104, 0.0853]) | 1 / 14 | 17 / 85 | 0 / 3 / 0 | 3 | 14 | 79 | 47 of 174 + 3 of 104 + 383 of 383 = **433** of 661 |
| A3-instruction | MINI | MODEL | 74 | 1 (0.0135; [0.0024, 0.0727]) | 1 / 12 | 9 / 62 | 0 / 1 / 0 | 0 | 9 | 64 | 44 of 174 + 1 of 104 + 172 of 383 = **217** of 661 |
| A3-instruction | MINI | LOOKUP | 70 | 1 (0.0143; [0.0025, 0.0766]) | 1 / 12 | 7 / 58 | 0 / 1 / 0 | 0 | 7 | 62 | 40 of 174 + 1 of 104 + 174 of 383 = **215** of 661 |
| A3-instruction | MINI | MODEL-ALL | 74 | 1 (0.0135; [0.0024, 0.0727]) | 1 / 12 | 9 / 62 | 0 / 1 / 0 | 0 | 9 | 64 | 44 of 174 + 1 of 104 + 172 of 383 = **217** of 661 |
| A3-instruction | MINI | LOOKUP-ALL | 70 | 1 (0.0143; [0.0025, 0.0766]) | 1 / 12 | 6 / 58 | 0 / 1 / 0 | 0 | 6 | 63 | 40 of 174 + 1 of 104 + 174 of 383 = **215** of 661 |
| A3-instruction | MINI | LOOKUP-LIT | 94 | 1 (0.0106; [0.0019, 0.0578]) | 1 / 12 | 15 / 82 | 0 / 1 / 0 | 2 | 13 | 78 | 46 of 174 + 1 of 104 + 0 of 383 = **47** of 661 |
| A3-instruction | H45 | ALWAYS | 54 | 11 (0.2037; [0.1177, 0.329]) | 5 / 12 | 11 / 42 | 10 / 1 / 0 | 2 | 9 | 29 | 49 of 174 + 11 of 104 + 0 of 383 = **60** of 661 |
| A3-instruction | H45 | ORACLE | 99 | 18 (0.1818; [0.1182, 0.2692]) | 6 / 14 | 18 / 85 | 18 / 0 / 0 | 5 | 13 | 60 | 49 of 174 + 18 of 104 + 383 of 383 = **450** of 661 |
| A3-instruction | H45 | MODEL | 74 | 13 (0.1757; [0.1056, 0.2777]) | 6 / 12 | 17 / 62 | 13 / 0 / 0 | 9 | 8 | 41 | 47 of 174 + 13 of 104 + 172 of 383 = **232** of 661 |
| A3-instruction | H45 | LOOKUP | 70 | 10 (0.1429; [0.0795, 0.2434]) | 5 / 12 | 13 / 58 | 10 / 0 / 0 | 7 | 6 | 44 | 40 of 174 + 10 of 104 + 174 of 383 = **224** of 661 |
| A3-instruction | H45 | MODEL-ALL | 74 | 11 (0.1486; [0.0851, 0.2469]) | 5 / 12 | 12 / 62 | 11 / 0 / 0 | 4 | 8 | 48 | 47 of 174 + 11 of 104 + 172 of 383 = **230** of 661 |
| A3-instruction | H45 | LOOKUP-ALL | 70 | 8 (0.1143; [0.0591, 0.2096]) | 5 / 12 | 9 / 58 | 8 / 0 / 0 | 3 | 6 | 50 | 40 of 174 + 8 of 104 + 174 of 383 = **222** of 661 |
| A3-instruction | H45 | LOOKUP-LIT | 94 | 14 (0.1489; [0.0908, 0.2346]) | 5 / 12 | 22 / 82 | 13 / 1 / 0 | 10 | 12 | 55 | 47 of 174 + 14 of 104 + 0 of 383 = **61** of 661 |
| A4-header | MINI | ALWAYS | 54 | 3 (0.0556; [0.0191, 0.1511]) | 1 / 12 | 10 / 42 | 0 / 3 / 0 | 1 | 9 | 41 | 56 of 174 + 3 of 104 + 0 of 383 = **59** of 661 |
| A4-header | MINI | ORACLE | 99 | 4 (0.0404; [0.0158, 0.0993]) | 1 / 14 | 17 / 85 | 0 / 4 / 0 | 2 | 15 | 78 | 56 of 174 + 4 of 104 + 383 of 383 = **443** of 661 |
| A4-header | MINI | MODEL | 74 | 1 (0.0135; [0.0024, 0.0727]) | 1 / 12 | 10 / 62 | 0 / 1 / 0 | 0 | 10 | 63 | 53 of 174 + 1 of 104 + 172 of 383 = **226** of 661 |
| A4-header | MINI | LOOKUP | 70 | 1 (0.0143; [0.0025, 0.0766]) | 1 / 12 | 8 / 58 | 0 / 1 / 0 | 0 | 8 | 61 | 48 of 174 + 1 of 104 + 174 of 383 = **223** of 661 |
| A4-header | MINI | MODEL-ALL | 74 | 1 (0.0135; [0.0024, 0.0727]) | 1 / 12 | 11 / 62 | 0 / 1 / 0 | 0 | 11 | 62 | 53 of 174 + 1 of 104 + 172 of 383 = **226** of 661 |
| A4-header | MINI | LOOKUP-ALL | 70 | 1 (0.0143; [0.0025, 0.0766]) | 1 / 12 | 8 / 58 | 0 / 1 / 0 | 0 | 8 | 61 | 47 of 174 + 1 of 104 + 174 of 383 = **222** of 661 |
| A4-header | MINI | LOOKUP-LIT | 94 | 3 (0.0319; [0.0109, 0.0897]) | 1 / 12 | 16 / 82 | 0 / 3 / 0 | 1 | 15 | 75 | 55 of 174 + 3 of 104 + 0 of 383 = **58** of 661 |
| A4-header | H45 | ALWAYS | 54 | 15 (0.2778; [0.1762, 0.4089]) | 9 / 12 | 10 / 42 | 13 / 2 / 0 | 2 | 8 | 26 | 73 of 174 + 15 of 104 + 0 of 383 = **88** of 661 |
| A4-header | H45 | ORACLE | 99 | 25 (0.2525; [0.1773, 0.3462]) | 11 / 14 | 23 / 85 | 23 / 2 / 0 | 4 | 19 | 49 | 73 of 174 + 25 of 104 + 383 of 383 = **481** of 661 |
| A4-header | H45 | MODEL | 74 | 15 (0.2027; [0.1269, 0.3079]) | 7 / 12 | 19 / 62 | 14 / 1 / 0 | 6 | 13 | 37 | 64 of 174 + 15 of 104 + 172 of 383 = **251** of 661 |
| A4-header | H45 | LOOKUP | 70 | 16 (0.2286; [0.1459, 0.3395]) | 9 / 12 | 16 / 58 | 15 / 1 / 0 | 5 | 11 | 35 | 58 of 174 + 16 of 104 + 174 of 383 = **248** of 661 |
| A4-header | H45 | MODEL-ALL | 74 | 19 (0.2568; [0.171, 0.3665]) | 8 / 12 | 15 / 62 | 18 / 1 / 0 | 2 | 13 | 37 | 64 of 174 + 19 of 104 + 172 of 383 = **255** of 661 |
| A4-header | H45 | LOOKUP-ALL | 70 | 17 (0.2429; [0.1575, 0.355]) | 9 / 12 | 12 / 58 | 16 / 1 / 0 | 2 | 10 | 38 | 58 of 174 + 17 of 104 + 174 of 383 = **249** of 661 |
| A4-header | H45 | LOOKUP-LIT | 94 | 20 (0.2128; [0.1422, 0.3059]) | 9 / 12 | 23 / 82 | 18 / 2 / 0 | 6 | 17 | 48 | 72 of 174 + 20 of 104 + 0 of 383 = **92** of 661 |
| A5-duplicates-tagged | MINI | ALWAYS | 54 | 3 (0.0556; [0.0191, 0.1511]) | 1 / 12 | 2 / 42 | 0 / 3 / 0 | 1 | 1 | 49 | 56 of 174 + 3 of 104 + 0 of 383 = **59** of 661 |
| A5-duplicates-tagged | MINI | ORACLE | 99 | 6 (0.0606; [0.0281, 0.126]) | 1 / 14 | 2 / 85 | 0 / 6 / 0 | 0 | 2 | 91 | 56 of 174 + 6 of 104 + 383 of 383 = **445** of 661 |
| A5-duplicates-tagged | MINI | MODEL | 74 | 1 (0.0135; [0.0024, 0.0727]) | 1 / 12 | 1 / 62 | 0 / 1 / 0 | 0 | 1 | 72 | 53 of 174 + 1 of 104 + 172 of 383 = **226** of 661 |
| A5-duplicates-tagged | MINI | LOOKUP | 70 | 1 (0.0143; [0.0025, 0.0766]) | 1 / 12 | 0 / 58 | 0 / 1 / 0 | 0 | 0 | 69 | 48 of 174 + 1 of 104 + 174 of 383 = **223** of 661 |
| A5-duplicates-tagged | MINI | MODEL-ALL | 74 | 1 (0.0135; [0.0024, 0.0727]) | 1 / 12 | 1 / 62 | 0 / 1 / 0 | 0 | 1 | 72 | 53 of 174 + 1 of 104 + 172 of 383 = **226** of 661 |
| A5-duplicates-tagged | MINI | LOOKUP-ALL | 70 | 1 (0.0143; [0.0025, 0.0766]) | 1 / 12 | 0 / 58 | 0 / 1 / 0 | 0 | 0 | 69 | 47 of 174 + 1 of 104 + 174 of 383 = **222** of 661 |
| A5-duplicates-tagged | MINI | LOOKUP-LIT | 94 | 3 (0.0319; [0.0109, 0.0897]) | 1 / 12 | 4 / 82 | 0 / 3 / 0 | 1 | 3 | 87 | 55 of 174 + 3 of 104 + 0 of 383 = **58** of 661 |
| A5-duplicates-tagged | H45 | ALWAYS | 54 | 19 (0.3519; [0.2382, 0.4852]) | 9 / 12 | 3 / 42 | 15 / 4 / 0 | 3 | 0 | 29 | 73 of 174 + 19 of 104 + 0 of 383 = **92** of 661 |
| A5-duplicates-tagged | H45 | ORACLE | 99 | 31 (0.3131; [0.2302, 0.41]) | 11 / 14 | 13 / 85 | 26 / 5 / 0 | 3 | 10 | 53 | 73 of 174 + 31 of 104 + 383 of 383 = **487** of 661 |
| A5-duplicates-tagged | H45 | MODEL | 74 | 21 (0.2838; [0.1937, 0.3952]) | 7 / 12 | 9 / 62 | 20 / 1 / 0 | 6 | 3 | 41 | 64 of 174 + 21 of 104 + 172 of 383 = **257** of 661 |
| A5-duplicates-tagged | H45 | LOOKUP | 70 | 21 (0.3000; [0.2054, 0.4154]) | 9 / 12 | 8 / 58 | 20 / 1 / 0 | 5 | 3 | 38 | 58 of 174 + 21 of 104 + 174 of 383 = **253** of 661 |
| A5-duplicates-tagged | H45 | MODEL-ALL | 74 | 24 (0.3243; [0.2286, 0.4373]) | 8 / 12 | 5 / 62 | 23 / 1 / 0 | 4 | 1 | 42 | 64 of 174 + 24 of 104 + 172 of 383 = **260** of 661 |
| A5-duplicates-tagged | H45 | LOOKUP-ALL | 70 | 22 (0.3143; [0.2176, 0.4303]) | 9 / 12 | 4 / 58 | 21 / 1 / 0 | 3 | 1 | 41 | 58 of 174 + 22 of 104 + 174 of 383 = **254** of 661 |
| A5-duplicates-tagged | H45 | LOOKUP-LIT | 94 | 28 (0.2979; [0.2148, 0.3968]) | 9 / 12 | 10 / 82 | 24 / 4 / 0 | 5 | 5 | 53 | 72 of 174 + 28 of 104 + 0 of 383 = **100** of 661 |

### AUX-DS-A7-Q4: dash: the second annotator's sheet is not yet labeled (reviews/v18/annotator_agreement.py carries the detector's Q4 counterpart)

## 12. DS Amendment 6: coverage-gated depth expansion of the retrieval view (registrations/ADDENDUM_DS_AMENDMENT_6.md; descriptive)

### AUX-DS-A6-REG

Registered text sha256 **`52effd8d7911a62505f2ee0a7d97fc42ca600a595dbffb46463ec05598fec65a`** (the bytes above the marker line), frozen at `12c63f9` on 2026-09-15, recorded here before the first call; the author's cap ruling of 2026-09-15 below the marker ($4.00 to $6.00 for the k = 6, 8, 9 flat policies added at the freeze). Descriptive: no prediction, no bar, no verdict. Runner `tools/amend6_depth.py`. The registered call count (2,994 per answerer) is an arithmetic slip for 3,168 (D-DS-A6-1, `DEVIATIONS_DS.md`); every other count reproduces at the lock.

### AUX-DS-A6-LOCK, AUX-DS-A6-POP, AUX-DS-A6-PROBE-MINI, AUX-DS-A6-PROBE-H45, AUX-DS-A6-PROJECTION (appended by `tools/amend6_depth.py score`)

Registration sha256 holds (frozen at `12c63f9`); the cap ruling below the marker read ($6.00); the Amendment 4 header reproduces AUX-DS-A4-LOCK; prompt digests as pinned. 557 of 557 k = 5 renderings byte-identical to views.json ALWAYS; the ALWAYS ids the ranking's first five on all. Population 557 items (174 licensed, 383 absent); the recorded coverage score at or above theta_fok = 0.114007 on 366 (155 licensed, 211 absent), so GATED renders ten lines there and five elsewhere: mean view **8.29** lines; the targeting figure **9.45 lines per licensed item and 7.75 per absent item** at the flat policy's 8.29 everywhere. The licensed record in view along the flat curve k = 5 to 10: 65, 72, 77, 82, 88, 89 of 174; under GATED 87. 3168 calls per answerer. Probes: mini served `gpt-4.1-mini-2025-04-14` (703 in / 30 out on a ten-line view); Haiku 4.5 served `claude-haiku-4-5-20251001` (782 in / 40 out). Projection printed before submission: mini $0.9082, Haiku $2.7742, sum with probes $3.6836 (x1.3 $4.7887) against the $6.00 line; runs: True.

### AUX-DS-A6-INVIEW, AUX-DS-A6-CORRECT-MINI, AUX-DS-A6-ABSENT-MINI: the flat curve and GATED under GPT-4.1 mini (rows 3168, failed 0, served ['gpt-4.1-mini']; the licensed k = 5 rows are Amendment 4's)

| policy | mean depth (all; licensed) | licensed record in view (Wilson) | correct at 0.50 (Wilson) | correct at 0.80 | correct among in view | abstain, licensed | abstain, absent (Wilson) | claims on absent |
|---|---|---|---|---:|---|---|---|---:|
| FLAT-5 | 5.0; 5.0 | 65 / 174 = 0.3736 [0.3051, 0.4474] | 56 / 174 = 0.3218 [0.2569, 0.3945] | 20 | 48 / 65 | 33 / 174 | 241 / 383 = 0.6292 [0.5798, 0.6761] | 142 |
| FLAT-6 | 6.0; 6.0 | 72 / 174 = 0.4138 [0.3432, 0.4881] | 59 / 174 = 0.3391 [0.2729, 0.4122] | 21 | 50 / 72 | 30 / 174 | 236 / 383 = 0.6162 [0.5666, 0.6635] | 147 |
| FLAT-7 | 7.0; 7.0 | 77 / 174 = 0.4425 [0.3708, 0.5168] | 62 / 174 = 0.3563 [0.289, 0.4299] | 23 | 54 / 77 | 25 / 174 | 228 / 383 = 0.5953 [0.5454, 0.6433] | 155 |
| FLAT-8 | 8.0; 8.0 | 82 / 174 = 0.4713 [0.3985, 0.5453] | 65 / 174 = 0.3736 [0.3051, 0.4474] | 20 | 57 / 82 | 21 / 174 | 218 / 383 = 0.5692 [0.5192, 0.6179] | 165 |
| FLAT-9 | 9.0; 9.0 | 88 / 174 = 0.5057 [0.4321, 0.5791] | 67 / 174 = 0.3851 [0.316, 0.4591] | 22 | 60 / 88 | 18 / 174 | 219 / 383 = 0.5718 [0.5218, 0.6204] | 164 |
| FLAT-10 | 10.0; 10.0 | 89 / 174 = 0.5115 [0.4378, 0.5847] | 70 / 174 = 0.4023 [0.3323, 0.4765] | 23 | 62 / 89 | 21 / 174 | 214 / 383 = 0.5587 [0.5087, 0.6076] | 169 |
| GATED | 8.29; 9.45 | 87 / 174 = 0.5000 [0.4265, 0.5735] | 69 / 174 = 0.3966 [0.3269, 0.4707] | 23 | 61 / 87 | 24 / 174 | 219 / 383 = 0.5718 [0.5218, 0.6204] | 164 |

### AUX-DS-A6-MATCHED-MINI: GATED against the flat curve interpolated at its mean depth d = 8.29 (between FLAT-8 and FLAT-9); the matched difference GATED minus flat(d), both bootstraps (10000 draws, seed 42, 40 personas; the three policies resampled together; descriptive, no bar)

- correct: GATED 0.3966, flat at d 0.3769, **difference +0.0197**, item [-0.0106, +0.0517], persona [-0.0161, +0.0575]
- inview: GATED 0.5000, flat at d 0.4813, **difference +0.0187**, item [-0.0091, +0.0473], persona [+0.0028, +0.0374]
- abstain_absent: GATED 0.5718, flat at d 0.5699, **difference +0.0019**, item [-0.0202, +0.0235], persona [-0.0191, +0.0239]

### AUX-DS-A6-INVIEW, AUX-DS-A6-CORRECT-H45, AUX-DS-A6-ABSENT-H45: the flat curve and GATED under Claude Haiku 4.5 (rows 3168, failed 0, served ['claude-haiku-4-5-20251001']; the licensed k = 5 rows are Amendment 4's)

| policy | mean depth (all; licensed) | licensed record in view (Wilson) | correct at 0.50 (Wilson) | correct at 0.80 | correct among in view | abstain, licensed | abstain, absent (Wilson) | claims on absent |
|---|---|---|---|---:|---|---|---|---:|
| FLAT-5 | 5.0; 5.0 | 65 / 174 = 0.3736 [0.3051, 0.4474] | 73 / 174 = 0.4195 [0.3487, 0.4938] | 27 | 59 / 65 | 45 / 174 | 280 / 383 = 0.7311 [0.6845, 0.773] | 103 |
| FLAT-6 | 6.0; 6.0 | 72 / 174 = 0.4138 [0.3432, 0.4881] | 75 / 174 = 0.4310 [0.3597, 0.5053] | 26 | 64 / 72 | 36 / 174 | 268 / 383 = 0.6997 [0.652, 0.7435] | 115 |
| FLAT-7 | 7.0; 7.0 | 77 / 174 = 0.4425 [0.3708, 0.5168] | 74 / 174 = 0.4253 [0.3542, 0.4996] | 28 | 65 / 77 | 34 / 174 | 263 / 383 = 0.6867 [0.6386, 0.7311] | 120 |
| FLAT-8 | 8.0; 8.0 | 82 / 174 = 0.4713 [0.3985, 0.5453] | 78 / 174 = 0.4483 [0.3763, 0.5225] | 31 | 67 / 82 | 35 / 174 | 261 / 383 = 0.6815 [0.6332, 0.7261] | 122 |
| FLAT-9 | 9.0; 9.0 | 88 / 174 = 0.5057 [0.4321, 0.5791] | 80 / 174 = 0.4598 [0.3874, 0.5339] | 34 | 70 / 88 | 33 / 174 | 257 / 383 = 0.6710 [0.6225, 0.7162] | 126 |
| FLAT-10 | 10.0; 10.0 | 89 / 174 = 0.5115 [0.4378, 0.5847] | 85 / 174 = 0.4885 [0.4153, 0.5622] | 33 | 72 / 89 | 32 / 174 | 255 / 383 = 0.6658 [0.6171, 0.7112] | 128 |
| GATED | 8.29; 9.45 | 87 / 174 = 0.5000 [0.4265, 0.5735] | 85 / 174 = 0.4885 [0.4153, 0.5622] | 33 | 72 / 87 | 34 / 174 | 261 / 383 = 0.6815 [0.6332, 0.7261] | 122 |

### AUX-DS-A6-MATCHED-H45: GATED against the flat curve interpolated at its mean depth d = 8.29 (between FLAT-8 and FLAT-9); the matched difference GATED minus flat(d), both bootstraps (10000 draws, seed 42, 40 personas; the three policies resampled together; descriptive, no bar)

- correct: GATED 0.4885, flat at d 0.4516, **difference +0.0369**, item [+0.0156, +0.0623], persona [+0.0136, +0.0639]
- inview: GATED 0.5000, flat at d 0.4813, **difference +0.0187**, item [-0.0091, +0.0473], persona [+0.0028, +0.0374]
- abstain_absent: GATED 0.6815, flat at d 0.6784, **difference +0.0030**, item [-0.0186, +0.0251], persona [-0.0169, +0.0235]

### AUX-DS-A6-SPEND: {"MINI": 0.8574, "H45": 2.7744, "probes": 0.0013, "total": 3.6331, "line": 6.0}

### AUX-DS-A7-COMPOSITE-DIFF: the composite under each gated rule minus under retrieval alone (the author's addition of 2026-09-15, after the registration; descriptive, no bar): a paired difference of rates over the 661 items, item-level and persona-grouped percentile bootstraps (10,000 draws, seed 42, 40 personas). The oracle is excluded from every comparison: its absent component is the label itself (D-DS-A7-1). Retrieval alone and the literal rule have no coverage rule, so their absent component is 0 of 383 and the difference is carried mostly by the absent items.

| answerer | prompt | comparison | composite (rule; retrieval alone) | difference (count; rate) | item 95% | persona 95% |
|---|---|---|---|---|---|---|
| MINI | A4-header | MODEL minus ALWAYS, same prompt | 226; 59 of 661 | +167; +0.2526 | [+0.2179, +0.2874] | [+0.2191, +0.2884] |
| MINI | A4-header | LOOKUP minus ALWAYS, same prompt | 223; 59 of 661 | +164; +0.2481 | [+0.2118, +0.2844] | [+0.2168, +0.2808] |
| MINI | A4-header | MODEL-ALL minus ALWAYS, same prompt | 226; 59 of 661 | +167; +0.2526 | [+0.2179, +0.2874] | [+0.2191, +0.2884] |
| MINI | A4-header | LOOKUP-ALL minus ALWAYS, same prompt | 222; 59 of 661 | +163; +0.2466 | [+0.2103, +0.2829] | [+0.2149, +0.2795] |
| MINI | A4-header | LOOKUP-LIT minus ALWAYS, same prompt | 58; 59 of 661 | -1; -0.0015 | [-0.0061, +0.0030] | [-0.0065, +0.0031] |
| H45 | A4-header | MODEL minus ALWAYS, same prompt | 251; 88 of 661 | +163; +0.2466 | [+0.2118, +0.2829] | [+0.2095, +0.2847] |
| H45 | A4-header | LOOKUP minus ALWAYS, same prompt | 248; 88 of 661 | +160; +0.2421 | [+0.2042, +0.2784] | [+0.2072, +0.2785] |
| H45 | A4-header | MODEL-ALL minus ALWAYS, same prompt | 255; 88 of 661 | +167; +0.2526 | [+0.2179, +0.2890] | [+0.2157, +0.2907] |
| H45 | A4-header | LOOKUP-ALL minus ALWAYS, same prompt | 249; 88 of 661 | +161; +0.2436 | [+0.2057, +0.2814] | [+0.2075, +0.2809] |
| H45 | A4-header | LOOKUP-LIT minus ALWAYS, same prompt | 92; 88 of 661 | +4; +0.0061 | [-0.0015, +0.0151] | [-0.0015, +0.0149] |
| MINI | A5-duplicates-tagged | MODEL minus ALWAYS, same prompt | 226; 59 of 661 | +167; +0.2526 | [+0.2179, +0.2874] | [+0.2191, +0.2884] |
| MINI | A5-duplicates-tagged | MODEL minus ALWAYS under the header | 226; 59 of 661 | +167; +0.2526 | [+0.2179, +0.2874] | [+0.2191, +0.2884] |
| MINI | A5-duplicates-tagged | LOOKUP minus ALWAYS, same prompt | 223; 59 of 661 | +164; +0.2481 | [+0.2118, +0.2844] | [+0.2168, +0.2808] |
| MINI | A5-duplicates-tagged | LOOKUP minus ALWAYS under the header | 223; 59 of 661 | +164; +0.2481 | [+0.2118, +0.2844] | [+0.2168, +0.2808] |
| MINI | A5-duplicates-tagged | MODEL-ALL minus ALWAYS, same prompt | 226; 59 of 661 | +167; +0.2526 | [+0.2179, +0.2874] | [+0.2191, +0.2884] |
| MINI | A5-duplicates-tagged | MODEL-ALL minus ALWAYS under the header | 226; 59 of 661 | +167; +0.2526 | [+0.2179, +0.2874] | [+0.2191, +0.2884] |
| MINI | A5-duplicates-tagged | LOOKUP-ALL minus ALWAYS, same prompt | 222; 59 of 661 | +163; +0.2466 | [+0.2103, +0.2829] | [+0.2149, +0.2795] |
| MINI | A5-duplicates-tagged | LOOKUP-ALL minus ALWAYS under the header | 222; 59 of 661 | +163; +0.2466 | [+0.2103, +0.2829] | [+0.2149, +0.2795] |
| MINI | A5-duplicates-tagged | LOOKUP-LIT minus ALWAYS, same prompt | 58; 59 of 661 | -1; -0.0015 | [-0.0061, +0.0030] | [-0.0065, +0.0031] |
| MINI | A5-duplicates-tagged | LOOKUP-LIT minus ALWAYS under the header | 58; 59 of 661 | -1; -0.0015 | [-0.0061, +0.0030] | [-0.0065, +0.0031] |
| H45 | A5-duplicates-tagged | MODEL minus ALWAYS, same prompt | 257; 92 of 661 | +165; +0.2496 | [+0.2133, +0.2874] | [+0.2115, +0.2887] |
| H45 | A5-duplicates-tagged | MODEL minus ALWAYS under the header | 257; 88 of 661 | +169; +0.2557 | [+0.2194, +0.2920] | [+0.2158, +0.2965] |
| H45 | A5-duplicates-tagged | LOOKUP minus ALWAYS, same prompt | 253; 92 of 661 | +161; +0.2436 | [+0.2057, +0.2814] | [+0.2062, +0.2820] |
| H45 | A5-duplicates-tagged | LOOKUP minus ALWAYS under the header | 253; 88 of 661 | +165; +0.2496 | [+0.2118, +0.2859] | [+0.2117, +0.2892] |
| H45 | A5-duplicates-tagged | MODEL-ALL minus ALWAYS, same prompt | 260; 92 of 661 | +168; +0.2542 | [+0.2179, +0.2920] | [+0.2158, +0.2932] |
| H45 | A5-duplicates-tagged | MODEL-ALL minus ALWAYS under the header | 260; 88 of 661 | +172; +0.2602 | [+0.2239, +0.2965] | [+0.2202, +0.3008] |
| H45 | A5-duplicates-tagged | LOOKUP-ALL minus ALWAYS, same prompt | 254; 92 of 661 | +162; +0.2451 | [+0.2072, +0.2829] | [+0.2068, +0.2842] |
| H45 | A5-duplicates-tagged | LOOKUP-ALL minus ALWAYS under the header | 254; 88 of 661 | +166; +0.2511 | [+0.2118, +0.2890] | [+0.2127, +0.2912] |
| H45 | A5-duplicates-tagged | LOOKUP-LIT minus ALWAYS, same prompt | 100; 92 of 661 | +8; +0.0121 | [+0.0030, +0.0227] | [+0.0029, +0.0230] |
| H45 | A5-duplicates-tagged | LOOKUP-LIT minus ALWAYS under the header | 100; 88 of 661 | +12; +0.0182 | [+0.0076, +0.0303] | [+0.0046, +0.0336] |

### AUX-DS-A7-COMPOSITE-ANSWERED: the composite per policy in the answered reading (the author's instruction of 2026-09-15, evening; descriptive, after the registration). A licensed item counts when correct at 0.50; an obligation when reached, answered and reported, where reported is the registered rule (names the state, no stale value) or, on a supersession item, the successor given (the committed detector's successor_use at TAU_HI); an absent item when the coverage rule abstained on it or the answerer abstained on its recorded five-line view (Amendment 6's FLAT-5 answers under the header, the same for both prompt variants; the absent items a gated rule answers on a longer view, 10 under the model rule, 17 under the lookup rule and 72 under the literal rule, are read on the five-line view as a proxy). The oracle's absent component is the label itself (D-DS-A7-1); it prints and enters no comparison. The rule-only reading is AUX-DS-A7-COMPOSITE above.

| prompt | answerer | policy | licensed correct (of 174) | reported, answered reading (of 104) | of which by the successor alone | reported, registered rule | absent abstained (of 383) = by the rule + by the answerer | absent read on a five-line proxy | composite (of 661) |
|---|---|---|---:|---:|---:|---:|---|---:|---:|
| A4-header | MINI | ALWAYS | 56 | 4 | 1 | 3 | 241 = 0 + 241 | 0 | **301** |
| A4-header | MINI | MODEL | 53 | 2 | 1 | 1 | 264 = 172 + 92 | 10 | **319** |
| A4-header | MINI | LOOKUP | 48 | 2 | 1 | 1 | 276 = 174 + 102 | 17 | **326** |
| A4-header | MINI | MODEL-ALL | 53 | 2 | 1 | 1 | 264 = 172 + 92 | 10 | **319** |
| A4-header | MINI | LOOKUP-ALL | 47 | 2 | 1 | 1 | 276 = 174 + 102 | 17 | **325** |
| A4-header | MINI | LOOKUP-LIT | 55 | 4 | 1 | 3 | 241 = 0 + 241 | 72 | **300** |
| A4-header | MINI | ORACLE | 56 | 5 | 1 | 4 | 383 = 383 + 0 | 0 | **444** |
| A4-header | H45 | ALWAYS | 73 | 16 | 1 | 15 | 280 = 0 + 280 | 0 | **369** |
| A4-header | H45 | MODEL | 64 | 16 | 1 | 15 | 291 = 172 + 119 | 10 | **371** |
| A4-header | H45 | LOOKUP | 58 | 17 | 1 | 16 | 304 = 174 + 130 | 17 | **379** |
| A4-header | H45 | MODEL-ALL | 64 | 21 | 2 | 19 | 291 = 172 + 119 | 10 | **376** |
| A4-header | H45 | LOOKUP-ALL | 58 | 19 | 2 | 17 | 304 = 174 + 130 | 17 | **381** |
| A4-header | H45 | LOOKUP-LIT | 72 | 21 | 1 | 20 | 280 = 0 + 280 | 72 | **373** |
| A4-header | H45 | ORACLE | 73 | 27 | 2 | 25 | 383 = 383 + 0 | 0 | **483** |
| A5-duplicates-tagged | MINI | ALWAYS | 56 | 4 | 1 | 3 | 241 = 0 + 241 | 0 | **301** |
| A5-duplicates-tagged | MINI | MODEL | 53 | 2 | 1 | 1 | 264 = 172 + 92 | 10 | **319** |
| A5-duplicates-tagged | MINI | LOOKUP | 48 | 2 | 1 | 1 | 276 = 174 + 102 | 17 | **326** |
| A5-duplicates-tagged | MINI | MODEL-ALL | 53 | 2 | 1 | 1 | 264 = 172 + 92 | 10 | **319** |
| A5-duplicates-tagged | MINI | LOOKUP-ALL | 47 | 2 | 1 | 1 | 276 = 174 + 102 | 17 | **325** |
| A5-duplicates-tagged | MINI | LOOKUP-LIT | 55 | 4 | 1 | 3 | 241 = 0 + 241 | 72 | **300** |
| A5-duplicates-tagged | MINI | ORACLE | 56 | 7 | 1 | 6 | 383 = 383 + 0 | 0 | **446** |
| A5-duplicates-tagged | H45 | ALWAYS | 73 | 20 | 1 | 19 | 280 = 0 + 280 | 0 | **373** |
| A5-duplicates-tagged | H45 | MODEL | 64 | 22 | 1 | 21 | 291 = 172 + 119 | 10 | **377** |
| A5-duplicates-tagged | H45 | LOOKUP | 58 | 22 | 1 | 21 | 304 = 174 + 130 | 17 | **384** |
| A5-duplicates-tagged | H45 | MODEL-ALL | 64 | 26 | 2 | 24 | 291 = 172 + 119 | 10 | **381** |
| A5-duplicates-tagged | H45 | LOOKUP-ALL | 58 | 24 | 2 | 22 | 304 = 174 + 130 | 17 | **386** |
| A5-duplicates-tagged | H45 | LOOKUP-LIT | 72 | 29 | 1 | 28 | 280 = 0 + 280 | 72 | **381** |
| A5-duplicates-tagged | H45 | ORACLE | 73 | 33 | 2 | 31 | 383 = 383 + 0 | 0 | **489** |

### AUX-DS-A7-COMPOSITE-ANSWERED-DIFF: each gated rule minus retrieval alone under the same prompt, the answered reading; a paired difference of rates over the 661 items, item-level and persona-grouped percentile bootstraps (10,000 draws, seed 42, 40 personas); the oracle excluded

| prompt | answerer | policy | composite (rule; retrieval alone) | difference (count; rate) | item 95% | persona 95% |
|---|---|---|---|---|---|---|
| A4-header | MINI | MODEL | 319; 301 | +18; +0.0272 | [+0.0121, +0.0439] | [+0.0113, +0.0443] |
| A4-header | MINI | LOOKUP | 326; 301 | +25; +0.0378 | [+0.0182, +0.0575] | [+0.0194, +0.0564] |
| A4-header | MINI | MODEL-ALL | 319; 301 | +18; +0.0272 | [+0.0121, +0.0439] | [+0.0113, +0.0443] |
| A4-header | MINI | LOOKUP-ALL | 325; 301 | +24; +0.0363 | [+0.0166, +0.0560] | [+0.0171, +0.0554] |
| A4-header | MINI | LOOKUP-LIT | 300; 301 | -1; -0.0015 | [-0.0061, +0.0030] | [-0.0065, +0.0031] |
| A4-header | H45 | MODEL | 371; 369 | +2; +0.0030 | [-0.0121, +0.0182] | [-0.0132, +0.0191] |
| A4-header | H45 | LOOKUP | 379; 369 | +10; +0.0151 | [-0.0045, +0.0348] | [-0.0056, +0.0354] |
| A4-header | H45 | MODEL-ALL | 376; 369 | +7; +0.0106 | [-0.0061, +0.0272] | [-0.0059, +0.0264] |
| A4-header | H45 | LOOKUP-ALL | 381; 369 | +12; +0.0182 | [-0.0030, +0.0393] | [-0.0045, +0.0413] |
| A4-header | H45 | LOOKUP-LIT | 373; 369 | +4; +0.0061 | [-0.0015, +0.0151] | [-0.0015, +0.0149] |
| A5-duplicates-tagged | MINI | MODEL | 319; 301 | +18; +0.0272 | [+0.0121, +0.0439] | [+0.0113, +0.0443] |
| A5-duplicates-tagged | MINI | LOOKUP | 326; 301 | +25; +0.0378 | [+0.0182, +0.0575] | [+0.0194, +0.0564] |
| A5-duplicates-tagged | MINI | MODEL-ALL | 319; 301 | +18; +0.0272 | [+0.0121, +0.0439] | [+0.0113, +0.0443] |
| A5-duplicates-tagged | MINI | LOOKUP-ALL | 325; 301 | +24; +0.0363 | [+0.0166, +0.0560] | [+0.0171, +0.0554] |
| A5-duplicates-tagged | MINI | LOOKUP-LIT | 300; 301 | -1; -0.0015 | [-0.0061, +0.0030] | [-0.0065, +0.0031] |
| A5-duplicates-tagged | H45 | MODEL | 377; 373 | +4; +0.0061 | [-0.0106, +0.0242] | [-0.0124, +0.0240] |
| A5-duplicates-tagged | H45 | LOOKUP | 384; 373 | +11; +0.0166 | [-0.0045, +0.0378] | [-0.0062, +0.0397] |
| A5-duplicates-tagged | H45 | MODEL-ALL | 381; 373 | +8; +0.0121 | [-0.0061, +0.0303] | [-0.0074, +0.0304] |
| A5-duplicates-tagged | H45 | LOOKUP-ALL | 386; 373 | +13; +0.0197 | [-0.0030, +0.0408] | [-0.0048, +0.0450] |
| A5-duplicates-tagged | H45 | LOOKUP-LIT | 381; 373 | +8; +0.0121 | [+0.0030, +0.0227] | [+0.0029, +0.0230] |

## 14. Program R114 (2026-09-17): the composite's answered reading on the ACTUAL expanded views (the 99 inputs R113 Z1 found unanswered; `reviews/r114/tools/p1_composite_views.py`; billed)

### AUX-DS-R114-VIEWS

The 99 distinct (item, view sha) inputs of `reviews/r113/results/z1_composite_proxy.json` (10 / 17 / 10 / 17 / 72 policy rows over 75 ABSENT items; 1,061 view lines) rebuilt from `stage1.json`, `views.json`, `policies.json` and asserted equal; no recorded answer existed on any of them at run. Answered once each under `SYSTEM_ANSWER` + `USER_ANSWER_A4` (the Amendment 4 header, sha256 `e6c155364f8c69be…`), the answer shared by every policy whose view is byte-identical. GPT-4.1 mini: 99 rows, 99 OK, served ['gpt-4.1-mini'], 99 calls, abstained on 58 of 99. Claude Haiku 4.5: 99 rows, 99 OK, served ['claude-haiku-4-5-20251001'], 99 calls, abstained on 68 of 99. Rows `run/rows_ds_r114_mini.jsonl`, `run/rows_ds_r114_h45.jsonl`; cache `cache_r114/`; probes `run/probes_r114.json`.

### AUX-DS-R114-COMPOSITE-ACTUAL: the composite per policy, the proxy reading (AUX-DS-A7-COMPOSITE-ANSWERED, reproduced) beside the actual-view reading (the absent items a gated rule answers on a longer view read on that view). Detector-scored, provisional pending the human validation of the stale-answer detector.

| prompt | answerer | policy | absent read on the actual view (n) | abstained on it | abstained on the FLAT-5 proxy (same items) | flipped | absent abstained: proxy -> actual (of 383) | composite: proxy -> actual (of 661) |
|---|---|---|---:|---:|---:|---:|---|---|
| A4-header | MINI | ALWAYS | 0 | 0 | 0 | 0 | 241 -> **241** | 301 -> **301** |
| A4-header | MINI | MODEL | 10 | 2 | 1 | 1 | 264 -> **265** | 319 -> **320** |
| A4-header | MINI | LOOKUP | 17 | 10 | 10 | 0 | 276 -> **276** | 326 -> **326** |
| A4-header | MINI | MODEL-ALL | 10 | 1 | 1 | 0 | 264 -> **264** | 319 -> **319** |
| A4-header | MINI | LOOKUP-ALL | 17 | 10 | 10 | 0 | 276 -> **276** | 325 -> **325** |
| A4-header | MINI | LOOKUP-LIT | 72 | 47 | 46 | 1 | 241 -> **242** | 300 -> **301** |
| A4-header | MINI | ORACLE | 0 | 0 | 0 | 0 | 383 -> **383** | 444 -> **444** |
| A4-header | H45 | ALWAYS | 0 | 0 | 0 | 0 | 280 -> **280** | 369 -> **369** |
| A4-header | H45 | MODEL | 10 | 5 | 4 | 1 | 291 -> **292** | 371 -> **372** |
| A4-header | H45 | LOOKUP | 17 | 10 | 11 | 1 | 304 -> **303** | 379 -> **378** |
| A4-header | H45 | MODEL-ALL | 10 | 5 | 4 | 1 | 291 -> **292** | 376 -> **377** |
| A4-header | H45 | LOOKUP-ALL | 17 | 10 | 11 | 1 | 304 -> **303** | 381 -> **380** |
| A4-header | H45 | LOOKUP-LIT | 72 | 51 | 51 | 2 | 280 -> **280** | 373 -> **373** |
| A4-header | H45 | ORACLE | 0 | 0 | 0 | 0 | 383 -> **383** | 483 -> **483** |
| A5-duplicates-tagged | MINI | ALWAYS | 0 | 0 | 0 | 0 | 241 -> **241** | 301 -> **301** |
| A5-duplicates-tagged | MINI | MODEL | 10 | 2 | 1 | 1 | 264 -> **265** | 319 -> **320** |
| A5-duplicates-tagged | MINI | LOOKUP | 17 | 10 | 10 | 0 | 276 -> **276** | 326 -> **326** |
| A5-duplicates-tagged | MINI | MODEL-ALL | 10 | 1 | 1 | 0 | 264 -> **264** | 319 -> **319** |
| A5-duplicates-tagged | MINI | LOOKUP-ALL | 17 | 10 | 10 | 0 | 276 -> **276** | 325 -> **325** |
| A5-duplicates-tagged | MINI | LOOKUP-LIT | 72 | 47 | 46 | 1 | 241 -> **242** | 300 -> **301** |
| A5-duplicates-tagged | MINI | ORACLE | 0 | 0 | 0 | 0 | 383 -> **383** | 446 -> **446** |
| A5-duplicates-tagged | H45 | ALWAYS | 0 | 0 | 0 | 0 | 280 -> **280** | 373 -> **373** |
| A5-duplicates-tagged | H45 | MODEL | 10 | 5 | 4 | 1 | 291 -> **292** | 377 -> **378** |
| A5-duplicates-tagged | H45 | LOOKUP | 17 | 10 | 11 | 1 | 304 -> **303** | 384 -> **383** |
| A5-duplicates-tagged | H45 | MODEL-ALL | 10 | 5 | 4 | 1 | 291 -> **292** | 381 -> **382** |
| A5-duplicates-tagged | H45 | LOOKUP-ALL | 17 | 10 | 11 | 1 | 304 -> **303** | 386 -> **385** |
| A5-duplicates-tagged | H45 | LOOKUP-LIT | 72 | 51 | 51 | 2 | 280 -> **280** | 381 -> **381** |
| A5-duplicates-tagged | H45 | ORACLE | 0 | 0 | 0 | 0 | 383 -> **383** | 489 -> **489** |

### AUX-DS-R114-COMPOSITE-ACTUAL-DIFF: each gated rule minus retrieval alone under the same prompt, the actual-view reading; paired difference of rates over the 661, item-level and persona-grouped percentile bootstraps (10,000 draws, seed 42, 40 personas); the proxy reading's row (AUX-DS-A7-COMPOSITE-ANSWERED-DIFF, reproduced) beside it; the oracle excluded

| prompt | answerer | policy | reading | composite (rule; retrieval alone) | difference (count; rate) | item 95% | persona 95% |
|---|---|---|---|---|---|---|---|
| A4-header | MINI | MODEL | proxy | 319; 301 | +18; +0.0272 | [+0.0121, +0.0439] | [+0.0113, +0.0443] |
| A4-header | MINI | MODEL | actual | 320; 301 | +19; +0.0287 | [+0.0136, +0.0454] | [+0.0127, +0.0459] |
| A4-header | MINI | LOOKUP | proxy | 326; 301 | +25; +0.0378 | [+0.0182, +0.0575] | [+0.0194, +0.0564] |
| A4-header | MINI | LOOKUP | actual | 326; 301 | +25; +0.0378 | [+0.0182, +0.0575] | [+0.0194, +0.0564] |
| A4-header | MINI | MODEL-ALL | proxy | 319; 301 | +18; +0.0272 | [+0.0121, +0.0439] | [+0.0113, +0.0443] |
| A4-header | MINI | MODEL-ALL | actual | 319; 301 | +18; +0.0272 | [+0.0121, +0.0439] | [+0.0113, +0.0443] |
| A4-header | MINI | LOOKUP-ALL | proxy | 325; 301 | +24; +0.0363 | [+0.0166, +0.0560] | [+0.0171, +0.0554] |
| A4-header | MINI | LOOKUP-ALL | actual | 325; 301 | +24; +0.0363 | [+0.0166, +0.0560] | [+0.0171, +0.0554] |
| A4-header | MINI | LOOKUP-LIT | proxy | 300; 301 | -1; -0.0015 | [-0.0061, +0.0030] | [-0.0065, +0.0031] |
| A4-header | MINI | LOOKUP-LIT | actual | 301; 301 | +0; +0.0000 | [-0.0061, +0.0061] | [-0.0059, +0.0060] |
| A4-header | H45 | MODEL | proxy | 371; 369 | +2; +0.0030 | [-0.0121, +0.0182] | [-0.0132, +0.0191] |
| A4-header | H45 | MODEL | actual | 372; 369 | +3; +0.0045 | [-0.0106, +0.0212] | [-0.0120, +0.0206] |
| A4-header | H45 | LOOKUP | proxy | 379; 369 | +10; +0.0151 | [-0.0045, +0.0348] | [-0.0056, +0.0354] |
| A4-header | H45 | LOOKUP | actual | 378; 369 | +9; +0.0136 | [-0.0061, +0.0333] | [-0.0075, +0.0344] |
| A4-header | H45 | MODEL-ALL | proxy | 376; 369 | +7; +0.0106 | [-0.0061, +0.0272] | [-0.0059, +0.0264] |
| A4-header | H45 | MODEL-ALL | actual | 377; 369 | +8; +0.0121 | [-0.0045, +0.0287] | [-0.0045, +0.0279] |
| A4-header | H45 | LOOKUP-ALL | proxy | 381; 369 | +12; +0.0182 | [-0.0030, +0.0393] | [-0.0045, +0.0413] |
| A4-header | H45 | LOOKUP-ALL | actual | 380; 369 | +11; +0.0166 | [-0.0045, +0.0378] | [-0.0062, +0.0401] |
| A4-header | H45 | LOOKUP-LIT | proxy | 373; 369 | +4; +0.0061 | [-0.0015, +0.0151] | [-0.0015, +0.0149] |
| A4-header | H45 | LOOKUP-LIT | actual | 373; 369 | +4; +0.0061 | [-0.0030, +0.0151] | [-0.0029, +0.0156] |
| A5-duplicates-tagged | MINI | MODEL | proxy | 319; 301 | +18; +0.0272 | [+0.0121, +0.0439] | [+0.0113, +0.0443] |
| A5-duplicates-tagged | MINI | MODEL | actual | 320; 301 | +19; +0.0287 | [+0.0136, +0.0454] | [+0.0127, +0.0459] |
| A5-duplicates-tagged | MINI | LOOKUP | proxy | 326; 301 | +25; +0.0378 | [+0.0182, +0.0575] | [+0.0194, +0.0564] |
| A5-duplicates-tagged | MINI | LOOKUP | actual | 326; 301 | +25; +0.0378 | [+0.0182, +0.0575] | [+0.0194, +0.0564] |
| A5-duplicates-tagged | MINI | MODEL-ALL | proxy | 319; 301 | +18; +0.0272 | [+0.0121, +0.0439] | [+0.0113, +0.0443] |
| A5-duplicates-tagged | MINI | MODEL-ALL | actual | 319; 301 | +18; +0.0272 | [+0.0121, +0.0439] | [+0.0113, +0.0443] |
| A5-duplicates-tagged | MINI | LOOKUP-ALL | proxy | 325; 301 | +24; +0.0363 | [+0.0166, +0.0560] | [+0.0171, +0.0554] |
| A5-duplicates-tagged | MINI | LOOKUP-ALL | actual | 325; 301 | +24; +0.0363 | [+0.0166, +0.0560] | [+0.0171, +0.0554] |
| A5-duplicates-tagged | MINI | LOOKUP-LIT | proxy | 300; 301 | -1; -0.0015 | [-0.0061, +0.0030] | [-0.0065, +0.0031] |
| A5-duplicates-tagged | MINI | LOOKUP-LIT | actual | 301; 301 | +0; +0.0000 | [-0.0061, +0.0061] | [-0.0059, +0.0060] |
| A5-duplicates-tagged | H45 | MODEL | proxy | 377; 373 | +4; +0.0061 | [-0.0106, +0.0242] | [-0.0124, +0.0240] |
| A5-duplicates-tagged | H45 | MODEL | actual | 378; 373 | +5; +0.0076 | [-0.0106, +0.0257] | [-0.0109, +0.0257] |
| A5-duplicates-tagged | H45 | LOOKUP | proxy | 384; 373 | +11; +0.0166 | [-0.0045, +0.0378] | [-0.0062, +0.0397] |
| A5-duplicates-tagged | H45 | LOOKUP | actual | 383; 373 | +10; +0.0151 | [-0.0061, +0.0363] | [-0.0079, +0.0387] |
| A5-duplicates-tagged | H45 | MODEL-ALL | proxy | 381; 373 | +8; +0.0121 | [-0.0061, +0.0303] | [-0.0074, +0.0304] |
| A5-duplicates-tagged | H45 | MODEL-ALL | actual | 382; 373 | +9; +0.0136 | [-0.0045, +0.0318] | [-0.0060, +0.0319] |
| A5-duplicates-tagged | H45 | LOOKUP-ALL | proxy | 386; 373 | +13; +0.0197 | [-0.0030, +0.0408] | [-0.0048, +0.0450] |
| A5-duplicates-tagged | H45 | LOOKUP-ALL | actual | 385; 373 | +12; +0.0182 | [-0.0045, +0.0394] | [-0.0075, +0.0439] |
| A5-duplicates-tagged | H45 | LOOKUP-LIT | proxy | 381; 373 | +8; +0.0121 | [+0.0030, +0.0227] | [+0.0029, +0.0230] |
| A5-duplicates-tagged | H45 | LOOKUP-LIT | actual | 381; 373 | +8; +0.0121 | [+0.0015, +0.0242] | [+0.0015, +0.0236] |

### AUX-DS-R114-SPEND

GPT-4.1 mini $0.0328 (74100 in / 1986 out), Claude Haiku 4.5 $0.1006 (80056 in / 4117 out), probes $0.0023; **total $0.1357** metered from the rows at list price against the phase line $0.40.

## 15. DS Amendment 8: label propagation inside the view (registrations/ADDENDUM_DS_AMENDMENT_8.md; E4, program R117)

### AUX-DS-A8-REG, AUX-DS-A8-LOCK (written 2026-09-19, before the first call)

Registered text sha256 `c57cda878aa80df7902e4ae35fc49504483a27a3032497a76e1c3b2e8050502c`, frozen at `177697a`; the Amendment 4 header and prompt digests reproduce AUX-DS-A4-LOCK; the rule is `tools/amend8_propagate.py propagate` with the census constants unchanged (MIN_SHARED 2, CROSS_GUARD 0.34, TAU_HI 0.8, MIN_DISCR 3); the ground-truth views' tags reproduce from the true flags on 3538 lines; the own-tag views re-render each line's lifecycle field from FR-Bank's own marks (resp_review amend1 believed_flags).

### AUX-DS-A8-RULE-CENSUS

`{"gt": {"primary": {"views": 452, "changed": 1, "lines": 1, "second_pass_would_change": 0, "unresolvable_pairs": 49, "unknown_age": 0, "changed_ORACLE": 1, "changed_MODEL": 1, "changed_ALWAYS": 1}, "secondary": {"views": 452, "changed": 1, "lines": 1, "second_pass_would_change": 0, "unresolvable_pairs": 49, "unknown_age": 0, "changed_ORACLE": 1, "changed_MODEL": 1, "changed_ALWAYS": 1}}, "own": {"primary": {"views": 452, "changed": 90, "lines": 117, "second_pass_would_change": 4, "unresolvable_pairs": 189, "unknown_age": 0, "changed_ORACLE": 40, "changed_MODEL": 34, "changed_ALWAYS": 28}, "secondary": {"views": 452, "changed": 123, "lines": 152, "second_pass_would_change": 5, "unresolvable_pairs": 189, "unknown_age": 0, "changed_ORACLE": 58, "changed_MODEL": 46, "changed_ALWAYS": 34}}}`

### AUX-DS-A8-DUP35

`{"gt/primary": {"views": 158, "views_fully_tagged": 0, "items": 35, "items_fully_tagged": 0, "t4_views": 72, "t4_views_fully_tagged": 0, "t4_items": 35, "t4_items_fully_tagged": 0}, "gt/secondary": {"views": 158, "views_fully_tagged": 0, "items": 35, "items_fully_tagged": 0, "t4_views": 72, "t4_views_fully_tagged": 0, "t4_items": 35, "t4_items_fully_tagged": 0}, "own/primary": {"views": 158, "views_fully_tagged": 69, "items": 35, "items_fully_tagged": 15, "t4_views": 72, "t4_views_fully_tagged": 35, "t4_items": 35, "t4_items_fully_tagged": 15}, "own/secondary": {"views": 158, "views_fully_tagged": 69, "items": 35, "items_fully_tagged": 15, "t4_views": 72, "t4_views_fully_tagged": 35, "t4_items": 35, "t4_items_fully_tagged": 15}}`

### AUX-DS-A8-FALSEPROP

`{"gt/primary": {"view_instances": 503, "active_lines_gt": 2333, "false_propagations": 3, "share": 0.0013}, "gt/secondary": {"view_instances": 503, "active_lines_gt": 2333, "false_propagations": 3, "share": 0.0013}, "own/primary": {"view_instances": 503, "active_lines_gt": 2333, "false_propagations": 69, "share": 0.0296}, "own/secondary": {"view_instances": 503, "active_lines_gt": 2333, "false_propagations": 83, "share": 0.0356}}`

Re-answer jobs (the primary arm; views serving ALWAYS, MODEL or ORACLE): 107 = {'own/before': 53, 'own/after': 53, 'gt/after': 1}.

### AUX-DS-A8-STAGE2 (scored 2026-09-19; `run/scores_amend8.json`)


**MINI** (107 rows, 0 failed, served ['gpt-4.1-mini']):

| source / policy | views | obligation views | stale at 0.50 before -> after | answered before -> after | stale rate before -> after | stale at 0.80 before -> after | correct licensed before -> after | paired (item; persona) |
|---|---:|---:|---|---|---|---|---|---|
| gt/ALWAYS | 1 | 0 | 0 -> 0 | 0 -> 0 | None -> None | 0 -> 0 | 0 -> 0 (of 1) | - |
| gt/MODEL | 1 | 0 | 0 -> 0 | 0 -> 0 | None -> None | 0 -> 0 | 0 -> 0 (of 1) | - |
| gt/ORACLE | 1 | 0 | 0 -> 0 | 0 -> 0 | None -> None | 0 -> 0 | 0 -> 0 (of 1) | - |
| gt/all | 1 | 0 | 0 -> 0 | 0 -> 0 | None -> None | 0 -> 0 | 0 -> 0 (of 1) | - |
| own/ALWAYS | 28 | 8 | 1 -> 0 | 7 -> 2 | 0.1429 -> 0.0 | 0 -> 0 | 11 -> 7 (of 20) | -0.1250 [-0.3750, +0.0000]; [-0.5000, +0.0000] |
| own/MODEL | 34 | 14 | 7 -> 3 | 12 -> 7 | 0.5833 -> 0.4286 | 6 -> 2 | 9 -> 7 (of 20) | -0.2857 [-0.5000, -0.0714]; [-0.5714, +0.0000] |
| own/ORACLE | 40 | 20 | 6 -> 1 | 17 -> 8 | 0.3529 -> 0.125 | 4 -> 0 | 11 -> 7 (of 20) | -0.2500 [-0.4500, -0.1000]; [-0.5000, -0.0526] |
| own/all | 53 | 31 | 13 -> 3 | 27 -> 14 | 0.4815 -> 0.2143 | 10 -> 2 | 11 -> 7 (of 22) | -0.3226 [-0.4839, -0.1613]; [-0.5714, -0.0714] |

**H45** (107 rows, 0 failed, served ['claude-haiku-4-5-20251001']):

| source / policy | views | obligation views | stale at 0.50 before -> after | answered before -> after | stale rate before -> after | stale at 0.80 before -> after | correct licensed before -> after | paired (item; persona) |
|---|---:|---:|---|---|---|---|---|---|
| gt/ALWAYS | 1 | 0 | 0 -> 0 | 0 -> 0 | None -> None | 0 -> 0 | 0 -> 0 (of 1) | - |
| gt/MODEL | 1 | 0 | 0 -> 0 | 0 -> 0 | None -> None | 0 -> 0 | 0 -> 0 (of 1) | - |
| gt/ORACLE | 1 | 0 | 0 -> 0 | 0 -> 0 | None -> None | 0 -> 0 | 0 -> 0 (of 1) | - |
| gt/all | 1 | 0 | 0 -> 0 | 0 -> 0 | None -> None | 0 -> 0 | 0 -> 0 (of 1) | - |
| own/ALWAYS | 28 | 8 | 1 -> 0 | 7 -> 2 | 0.1429 -> 0.0 | 0 -> 0 | 11 -> 7 (of 20) | -0.1250 [-0.3750, +0.0000]; [-0.5000, +0.0000] |
| own/MODEL | 34 | 14 | 6 -> 3 | 12 -> 5 | 0.5 -> 0.6 | 5 -> 3 | 9 -> 7 (of 20) | -0.2143 [-0.5000, +0.0714]; [-0.5455, +0.1538] |
| own/ORACLE | 40 | 20 | 4 -> 2 | 15 -> 5 | 0.2667 -> 0.4 | 2 -> 1 | 11 -> 7 (of 20) | -0.1000 [-0.3000, +0.1000]; [-0.3000, +0.1000] |
| own/all | 53 | 31 | 10 -> 4 | 25 -> 10 | 0.4 -> 0.4 | 7 -> 3 | 11 -> 7 (of 22) | -0.1935 [-0.3548, -0.0323]; [-0.4194, +0.0000] |

### AUX-DS-A8-P-L1

**P-L1 FAILS: 0 of 35 duplicate views are fully tagged by propagation.**

### AUX-DS-A8-P-L2

**P-L2 HOLDS: propagation tags 0.13% of the licensed items' active lines under ground-truth tags.**

### AUX-DS-A8-P-L5

**P-L5 FAILS: under the store's own tags false propagation is 2.96%, at or under 5%.**

### AUX-DS-A8-SPEND

mini $0.0290, Haiku 4.5 $0.0974, probes $0.0014, against the cap $5.


### AUX-DS-A8-P-L3

**P-L3 FAILS: under the model rule the flagged stale rate moves from its recorded value to the same value, because under ground-truth tags the rule changed one view of 452 (a licensed item's view, no obligation view), so no re-answer under the model rule exists and the rate is unchanged.**

### AUX-DS-A8-P-L4

**P-L4: not defined; the reduction is zero under both the model rule and top-five retrieval (no obligation view changed under ground-truth tags).**

### AUX-DS-A8-DIAGNOSIS (descriptive, computed after the lock on the recorded views; no call)

Of the 272 audited active-stale line instances (the 35 items' views under every policy), 187 have no tagged line of the same attribute in the view (the duplicate is written under a different slot key from its tagged twin), 45 have plain coverage below 0.50 of every same-attribute tagged line, 40 between 0.50 and 0.80, and none at or above the census threshold 0.80; the audit's duplicates were found by the item's own detector at TAU_GOLD 0.50 across attributes.

### D-DS-A8-1 (deviation, recorded at the lock)

The registration's lock "the rule reproduces itself on a second pass (idempotent)" contradicts its own one-pass rule (a second pass is chaining from newly tagged lines, which section 3 forbids); the one-pass definition governs, and the views a second pass would change are counted in AUX-DS-A8-RULE-CENSUS (`second_pass_would_change`: ground truth 0, own tags 4 primary / 5 secondary), never applied.

## 16. Program R130 (2026-09-20): GPT-5.6 Luna as a third answerer on the recorded E.10 views, and a semantic judge (Opus 5) over the three answerers' answers (reviews/r130/; exploratory; registration reviews/r130/registrations/REGISTRATION_R130.md, sha `2e95beab2451ab8d`)

### AUX-R130-POP

305 views (231 of the Amendment 4 population, label PRESENT-NEGATIVE, over the seven policies; 74 retagged); judge units 915 (915 OK). Luna rows 305 (305 OK), served `['gpt-5.6-luna']`.

### AUX-R130-POLICY-TABLE

| answerer | policy | views judged | ASSERTS | MENTIONS | CLEAN | ABSTAINS | UNSURE | ASSERTS rate [Wilson] | safe (M+C) of non-abstaining |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| GPT-4.1 mini | Top-five retrieval | 54 | 19 | 6 | 11 | 18 | 0 | 0.3519 [0.2382, 0.4852] | 0.4722 |
| GPT-4.1 mini | Model rule | 74 | 25 | 6 | 22 | 21 | 0 | 0.3378 [0.2405, 0.4512] | 0.5283 |
| GPT-4.1 mini | Lookup rule | 70 | 22 | 5 | 25 | 18 | 0 | 0.3143 [0.2176, 0.4303] | 0.5769 |
| GPT-4.1 mini | Model rule, all states | 74 | 24 | 6 | 24 | 20 | 0 | 0.3243 [0.2286, 0.4373] | 0.5556 |
| GPT-4.1 mini | Lookup rule, all states | 70 | 22 | 5 | 25 | 18 | 0 | 0.3143 [0.2176, 0.4303] | 0.5769 |
| GPT-4.1 mini | Literal lookup rule | 94 | 31 | 8 | 32 | 23 | 0 | 0.3298 [0.2431, 0.4299] | 0.5634 |
| GPT-4.1 mini | Oracle | 99 | 30 | 12 | 33 | 24 | 0 | 0.303 [0.2213, 0.3995] | 0.6 |
| GPT-4.1 mini | Retag variant (diagnostic) | 74 | 19 | 11 | 28 | 16 | 0 | 0.2568 [0.171, 0.3665] | 0.6724 |
| Claude Haiku 4.5 | Top-five retrieval | 54 | 21 | 16 | 7 | 10 | 0 | 0.3889 [0.2704, 0.5221] | 0.5227 |
| Claude Haiku 4.5 | Model rule | 74 | 27 | 22 | 16 | 9 | 0 | 0.3649 [0.2644, 0.4787] | 0.5846 |
| Claude Haiku 4.5 | Lookup rule | 70 | 23 | 20 | 18 | 9 | 0 | 0.3286 [0.23, 0.445] | 0.623 |
| Claude Haiku 4.5 | Model rule, all states | 74 | 27 | 21 | 17 | 9 | 0 | 0.3649 [0.2644, 0.4787] | 0.5846 |
| Claude Haiku 4.5 | Lookup rule, all states | 70 | 23 | 19 | 19 | 9 | 0 | 0.3286 [0.23, 0.445] | 0.623 |
| Claude Haiku 4.5 | Literal lookup rule | 94 | 31 | 22 | 25 | 16 | 0 | 0.3298 [0.2431, 0.4299] | 0.6026 |
| Claude Haiku 4.5 | Oracle | 99 | 32 | 25 | 26 | 16 | 0 | 0.3232 [0.2392, 0.4205] | 0.6145 |
| Claude Haiku 4.5 | Retag variant (diagnostic) | 74 | 17 | 17 | 26 | 14 | 0 | 0.2297 [0.1487, 0.3375] | 0.7167 |
| GPT-5.6 Luna | Top-five retrieval | 54 | 22 | 4 | 10 | 18 | 0 | 0.4074 [0.2868, 0.5403] | 0.3889 |
| GPT-5.6 Luna | Model rule | 74 | 28 | 1 | 19 | 26 | 0 | 0.3784 [0.2765, 0.4923] | 0.4167 |
| GPT-5.6 Luna | Lookup rule | 70 | 25 | 0 | 22 | 23 | 0 | 0.3571 [0.255, 0.4741] | 0.4681 |
| GPT-5.6 Luna | Model rule, all states | 74 | 28 | 1 | 22 | 23 | 0 | 0.3784 [0.2765, 0.4923] | 0.451 |
| GPT-5.6 Luna | Lookup rule, all states | 70 | 25 | 0 | 26 | 19 | 0 | 0.3571 [0.255, 0.4741] | 0.5098 |
| GPT-5.6 Luna | Literal lookup rule | 94 | 31 | 4 | 29 | 30 | 0 | 0.3298 [0.2431, 0.4299] | 0.5156 |
| GPT-5.6 Luna | Oracle | 99 | 33 | 3 | 31 | 32 | 0 | 0.3333 [0.2482, 0.4309] | 0.5075 |
| GPT-5.6 Luna | Retag variant (diagnostic) | 74 | 21 | 7 | 27 | 19 | 0 | 0.2838 [0.1937, 0.3952] | 0.6182 |

### AUX-R130-PL1, AUX-R130-PL1B, AUX-R130-PL4, AUX-R130-PL2, AUX-R130-PL3, AUX-R130-PL3B (primary reading; the drop-UNSURE sensitivity in results/R130_TABLES.md)

P-L1 (mini -> Luna, oracle view, tagged reach, all states; ASSERTS below): n 82, 20 -> 19, delta -0.0122, discordant 4 / 3, McNemar p 1.0, item [-0.0732, 0.0488], persona [-0.0921, 0.0674]: **FAILED (direction as predicted, not reliable)**.

P-L1b (mini -> Luna, lookup view, tagged reach; ASSERTS below; secondary): n 61, 15 -> 16, delta +0.0164, discordant 4 / 5, McNemar p 1.0, item [-0.082, 0.1148], persona [-0.125, 0.1406]: **FAILED (direction against)**.

P-L4 (mini -> Luna, the P-L1 pairs; MENTIONS above): n 82, 7 -> 2, delta -0.0610, discordant 5 / 0, McNemar p 0.0625, item [-0.122, -0.0122], persona [-0.1183, -0.0122]: **FAILED (direction against)**.

P-L2 (Luna: top-five -> lookup, the 40 answered under both; ASSERTS below): n 40, 16 -> 14, delta -0.0500, discordant 2 / 0, McNemar p 0.5, item [-0.125, 0.0], persona [-0.1714, 0.0]: **FAILED (direction as predicted, not reliable)**.

P-L3 (Luna, oracle view: active copy vs without; ASSERTS above): with 16 / 35 = 0.4571 against without 14 / 50 = 0.28, delta +0.1771, Fisher p 0.1102, item [-0.0286, 0.3829], persona [-0.0789, 0.4519]: **FAILED (direction as predicted, not reliable)**.

P-L3b (Luna, lookup view: active copy vs without; ASSERTS above; secondary): with 10 / 17 = 0.5882 against without 12 / 41 = 0.2927, delta +0.2956, Fisher p 0.043, item [0.0172, 0.5595], persona [-0.0929, 0.666]: **FAILED (direction as predicted, not reliable)**.

### AUX-R130-RETAG

GPT-4.1 mini: n 74, 34 -> 19, delta -0.2027, discordant 15 / 0, McNemar p 0.0001, item [-0.2973, -0.1081], persona [-0.3572, -0.0482]: **HELD**; Claude Haiku 4.5: n 74, 39 -> 17, delta -0.2973, discordant 23 / 1, McNemar p 0.0, item [-0.4054, -0.1892], persona [-0.5455, -0.0723]: **HELD**; GPT-5.6 Luna: n 74, 40 -> 21, delta -0.2568, discordant 21 / 2, McNemar p 0.0001, item [-0.3649, -0.1486], persona [-0.4925, -0.0377]: **HELD**

### AUX-R130-SPEND

Token-metered at the page prices: OpenAI $0.0629 of the $4.00 cap (Luna 0.0628, probe 0.0002); Anthropic $9.0221 against the registered $8.00 cap, raised to $10.00 for the judge lane by D-R130-5 (the cancelled-then-settled Batch 2.2816 at the 0.5 rate, the synchronous run 5.7092, the re-asks at max_tokens 1024 0.9410, the insurance check 0.0862, probe 0.0041). Judge transports in the assembled lane: {'batch': 780, 'synchronous (D-R130-2)': 68, 'synchronous re-ask at max_tokens 1024 (D-R130-4)': 67}.

Validation against the human labels: labels not yet released (AUX-R130-VALIDATION to follow).
