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
