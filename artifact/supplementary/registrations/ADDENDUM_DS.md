# ADDENDUM_DS — registration for the downstream experiment DS

Frozen against baseline HEAD `43a094c` (branch `[BRANCH]`), 2026-09-13 (R100, FREEZE-3), **BEFORE any
policy artifact, assembled view, answer prompt or answer call exists, and before any RESP Phase B
artifact (no L2 retrieval, no reach row) exists**. Spec: the DS-REG instruction of
2026-09-13, and the author's Phase A rulings of the same day (`reviews/DS_REG_REPORT.md` §6: the 22
unflagged forbidding records disclosed as **D-DS-1**, not repaired; the probability reading of the
base-rate threshold; LOOKUP under the matched budget with the literal threshold descriptive; the
PRESENT Stage 2 calls run; `ds_downstream/`; C150 and C151 replaced together; DS Phase B after RESP
Phase B step 4; DS-P4 and DS-P5 exactly as written). Question: *does acting on the obligation
judgment change what the agent sees and uses?*
Rules inherited from R74/R76/R77/R81/R82/SIDE/RESP: nothing unregistered may be reported; no
committed value is recomputed; registered verdicts are never re-adjudicated; **publish-regardless**
— every result prints under its frozen text. Template: `ADDENDUM_RESP.md` (§C censuses, arms, §T,
§B, §L, §STOP order). Failure texts written before the predictions.

**Precondition (reported first, §C.1).** `registrations/ADDENDUM_RESP.md` exists and is frozen
(commit `17e6328`, "R98: RESP registration frozen", 2026-09-12; an ancestor of HEAD; unchanged since).
DS inherits from it L2's retriever (§C.3/§L2 there: `LifecycleBank.cosine_search_all`, k = 5,
unmasked, TRUE lifecycle metadata on every retrieved line), L2's populations (661 obligation, 307
coverage) and **L2's reach row (`AUX-RESP-L2-REACH`) as DS's baseline row**. **RESP's Phase B has
not run**: `resp_review/` holds only `NUMBERS_RESP.md` with `AUX-RESP-PAPER-Q4`; no
`l2/retrieval.json`, no `question_emb.npz`, no `verify_resp.py`. DS is therefore sequenced **after
RESP Phase B step 4** (`build_l2.py`, the retrieval artifact and the reach key); DS Phase B stops
if either is absent (§STOP). DS builds no retrieval of its own.

**Results print in the appendix. One paragraph in Section 7 replacing the sentence "This paper
establishes the pre-retrieval measurement; the downstream effect of FOK and NOK remains open"
(`paper_v8.tex:734`, CLAIMS C151, entered with C150 at `CLAIMS.md:3021`); one appendix table; no new
section. No headline number in the abstract or Section 1 changes on DS's account; the Section 1
scope sentence "downstream behavior is outside this paper" (L181) is not a number and is not
edited under this registration (`reviews/DS_REG_REPORT.md` §5 lists it for the author).**

**AI use.** The draft, the censuses and the ledger entries were prepared with Claude Code under the
author's instruction; every number traces to a committed artifact or to a script reproduced in
`reviews/DS_REG_REPORT.md`. Verdicts are mechanical under the frozen criteria.

Ledger: `ds_downstream/NUMBERS_DS.md`, keys `AUX-DS-*` (all reserved in §L; the directory name is
the author's call, `reviews/DS_REG_REPORT.md` §6 R4). Verifier: `ds_downstream/tools/verify_ds.py`,
**required to exist and pass on the empty cell before any policy artifact, view or prompt is
written, and again before the first answer call**. Deviations: `ds_downstream/DEVIATIONS_DS.md`,
own numbering from **D-DS-1**. Estimators: §T (proportions and paired proportion differences on
committed populations; the committed draw scheme of `common_e1r.boot_item` / `boot_cluster`, 1,000
draws, seed 42; the retention ratio under `run_side.boot_ratio`'s discard rule); persona-clustered
interval beside; where the two disagree on a prediction the text says so and the weaker reading
governs. Tolerance ±0.05 throughout.

Metered budget: **the rule of §B, frozen: OpenAI key only; `gpt-4.1-mini` only, for every answer
call; under $4 in total for DS; nothing on the Anthropic key; no Haiku, no Opus; no embedding call
(DS embeds nothing — the retrieval is L2's).** Stage 1 is $0. Stage 2 is projected at ≈ $0.20
**[est]**, at most $0.73 at the nominal call count, against a $2 line inside the $4 rule (§B).

---

## §C — Pre-freeze censuses (all $0, deterministic, local, disclosed rather than inferred)

Every quantity in this section was computed **before this draft** from committed artifacts with
local code and no model call (`reviews/DS_REG_REPORT.md` Phase 1 and its appendix name the
scripts; the local encoder `sentence-transformers/all-MiniLM-L6-v2` ran offline for the lookup
scores). **No retrieval exists and no reach was computed**; no view was assembled; no answer exists.
What was computed is structural — which records the store's own metadata flags, what each summary
names, how large each fetch set is, where the committed scores sit against the base rates — and it
is needed to write the policies, the failure texts and the cost table. §C.7 states what these
censuses already foretell about the registered items, so that the freeze is made with that known.

### §C.1 — Precondition and inheritance

| Inherited from L2 | Where | State on 2026-09-13 |
|---|---|---|
| Retriever: `LifecycleBank.cosine_search_all` (`lifecycle_bank.py:402-414`), cosine over every entry of the item's store variant, active or not, on the cached `text-embedding-3-small` bank vectors and the fresh question vector; top 5 | `ADDENDUM_RESP.md` §C.3 (L155-188), §L2 (L318-469; the retrieval paragraph L333-350) | spec frozen; **not yet run** |
| Retrieved-line format, one line per entry in rank order, TRUE lifecycle flags from `index_v2.true_lifecycle`, category, scrubbed attribute, age, text | §L2 (the `[1] lifecycle: … \| text: …` line) | frozen |
| Retrieval artifact `resp_review/l2/retrieval.json`: per item the five ids with cosines, the rendered block, and for PN items the reach flag (any `pn_members` entry among the five), best rank, reach at k = 10 | §L2 | **absent** |
| Reach row `AUX-RESP-L2-REACH` (reach at k = 5 overall and per state; L2-P3 verdict) | §L | **absent** |
| Populations: 661 obligation (104 PN), 307 coverage (35 non-ABSENT) | `r74/x4/cell_661.json`; `common_e1r.POPULATIONS` R-NOK-FRB / R-FOK-FRB | committed; verified 661 / 104 / 307 / 35 |

DS's ALWAYS row **is** L2's reach row: DS reads `retrieval.json`, recomputes the reach flag from the
five ids and `pn_members`, and asserts equality with `AUX-RESP-L2-REACH` (a lock, `AUX-DS-PRECOND`).
DS makes no embedding call.

### §C.2 — Populations, asserted by the runner

`r74/x4/cell_661.json` (sha256 `01ed4c05fc57c0b2…`): **661 items, 104 PN** — 63 supersession-
derived (`AV1`/`AV4`, YAML `supersession_events`), 26 retraction-derived (`AV7`, `retractions`), 15
expiry-derived (`AV2`, `expiring_logistics`), by `nb6_composition.AV_STATE`; **174 PRESENT**, all easy
tier; **383 ABSENT** (238 ablation, 145 natural-absent probes). Variants FULL 323 / CAT-ABLATED 176 /
SLOT-ABLATED 162. The coverage population is the hard tier, **307 items = 272 ABSENT + 35 PN**: its
35 positives are all obligation items; it holds no PRESENT item. The PN items' YAML records are
resolved for every one of the 104 (`PersonaJoin.rec_of`), and the detector's discriminator is defined
(|old − new| ≥ 3 and |new − old| ≥ 3 tokens) on all 104 — required for Stage 2 scoring. Successor
value: the 63 supersession records carry a `new_fact`; retraction records carry a retraction
statement, not a value; expiry records carry no successor. Subtype: with-replacement 36 of 63
supersession and 12 of 26 retraction; every expiry item is without-replacement.

### §C.3 — The forbidding record under the store's TRUE metadata (the ORACLE ceiling)

The view prints, and every fetch policy fetches by, the TRUE lifecycle flags of
`index_v2.true_lifecycle` (`index_v2.py:206-252`) — the join the committed TRUE index is rendered
from, and the flags L2's retrieved lines carry. Keyed by (persona, entry id), for each PN item the
`pn_members` entries (the records the label calls forbidding) are flagged **superseded, retracted or
expired** as follows:

| | supersession (63) | retraction (26) | expiry (15) | all (104) |
|---|---:|---:|---:|---:|
| every `pn_members` entry in the item's store variant | 63 | 26 | 15 | 104 |
| **at least one `pn_members` entry flagged non-active (TRUE)** | **63** | **8** | **11** | **82 (0.788)** |
| every `pn_members` entry flagged | 63 | 2 | 9 | 74 |
| flag kind carried | superseded | retracted | expired | — |

**22 forbidding records (18 retraction-derived, 4 expiry-derived) carry no TRUE lifecycle flag.**
The label rule and the index join are two committed rules that differ on these states:
`PersonaJoin._resolve` (`e0_common.py:256-294`; the retraction branch L284-290) admits a retraction fire at 1.0 for entries anchored
to the original fact's session at `TAU_GOLD` 0.50 and for `is_retracted` bank entries covering the
original fact at 0.50, while `true_lifecycle` flags retracted only through `detect(original_fact,
retraction)` at `TAU_HI` 0.80; for expiry the label uses `expired_neg` (gold entries whose
`event_time` precedes the pinned cutoff) while `true_lifecycle` flags expired through YAML
`status == expired` records at 0.50 token coverage. Neither rule is changed here (`reviews/DS_REG_REPORT.md`
§4 F1 reports it). **Consequences, stated now:** (i) a fetch by lifecycle state can reach the
forbidding record for at most **82 of 104** (0.788): that is ORACLE's ceiling, not one; on
retraction it is 8 of 26 (0.308), on expiry 11 of 15 (0.733). (ii) When one of the 22 is in a view
it prints `lifecycle: active`; DS prints reach by id (registered) and **tagged reach** (the record in
view *and* printed non-active) beside it. (iii) The fetch sets under the two name sets reach the
record for: v2 superseded names **65** (63 / 2 / 0); all-three names (v3) **82** (63 / 8 / 11) —
naming cannot reach what the metadata does not flag.

**Ruling of 2026-09-13, disclosed as D-DS-1 (`reviews/DS_REG_REPORT.md` Appendix B), not repaired.**
ORACLE is the oracle over the store's truthful metadata, so its ceiling is 0.788 **by construction**.
The 22 forbidding records the truthful summary cannot name (18 of 26 retraction-derived, 4 of 15
expiry-derived; 10 distinct questions across variants, listed in D-DS-1) are a store-side fact,
consistent with the Conflate row of the believed-state table (Table 24 in the v8 lineage,
`tab:believed`, `paper_v8.tex:2177`: FR-Bank's write path records retraction through the supersession
mechanism, so its metadata cannot separate retracted from superseded content), and they print as
such; they retrieve as `lifecycle: active`, and the paper says so (§PAPER, the paragraph's second
sentence and the table note).

### §C.4 — What each summary names, and the fetch sets

**Renderer lock (2026-09-13).** `index_v2.render` on `index_v2.view` of the item's store variant
(FULL; CAT-ABLATED minus the persona's planned categories; SLOT-ABLATED minus
`slot_ablations[persona:qid]`) reproduces the committed TRUE text of `indexes_v2.json` **byte for
byte on 661 of 661 items**, and `index_v3.render_v3` (`r82_counterfactual/index_v3.py:49-62`, the
CF-2 renderer that calls `render` and appends the retracted and expired name sections) asserts its
v2 prefix on every one. Names are read from the emitted text through `index_v3.named_sections`
(`:65-102`), so the fetch set is what the summary prints (cap 15; `(none)` is not a name). No v3
section reaches the cap on this population (retracted names per key: mean 0.23, max 3; expired:
mean 3.22, max 11). **No v3 monitor row exists for the 661** (CF-2 elicited v3 on its own 444-store
cell); the -ALL policies keep the committed v2-elicited gate and change only the fetch set (§D).

Own-name presence, persona-keyed (RESP §C.1 reproduced, and its v3 analogue):

| pn slot named in | supersession | retraction | expiry | all |
|---|---:|---:|---:|---:|
| v2 superseded section (`N2`) | 63 / 63 | 11 / 26 | 0 / 15 | 74 |
| v3 any section (`N3`) | 63 / 63 | 19 / 26 | 12 / 15 | 94 |

Fetch-set sizes under the fetch rule of §D (lifecycle records of the store variant whose scrubbed
slot is in the name set):

| fetch set | population | zero | median | mean | p90 | max |
|---|---|---:|---:|---:|---:|---:|
| `F(N2)` | 661 | 195 (the `(none)` sections) | 2 | 2.84 | 7 | 9 |
| `F(N2)` | 104 PN | — | 3 | 3.57 | 7 | 9 |
| `F(N3)` | 661 | 12 | 9 | 8.84 | 16 | 23 |
| `F(N3)` | 104 PN | — | 10 | 9.88 | 16 | 22 |
| `F(P)` (ORACLE, pn slots) | 104 PN | 22 (§C.3) | 2 | 2.64 | 7 | 8 |
| non-active entries per store variant | 661 | — | 9 | 8.98 | 16 | 24 |

### §C.5 — The committed scores against the base rates (the thresholds, fixed here)

**Base rates, from the committed rows:** obligation 104 / 661 = **0.157337**; coverage 35 / 307 =
**0.114007**.

**mini's committed INDEXED-TRUE scores** (`elicitation_main.json`, read through `common_e1r.load_e1`
/ `assemble`, the committed join): `nok` takes **nine values** on the 661 — 0.0 (450), 0.05 (126),
0.1 (10), 0.2 (3), 0.3 (18), 0.4 (29), 0.6 (17), 0.7 (7), 0.8 (1); AUROC 0.7339 reproduced. On the
104 PN: 0.0 (41), 0.05 (7), 0.2 (2), 0.3 (13), 0.4 (16), 0.6 (17), 0.7 (7), 0.8 (1). `fok` takes
twelve values on the 307 (AUROC 0.7003 reproduced) and is present on every one of the 661 (one call
returned both judgments).

**Reading of "thresholded at the base rate" (ruled R1, 2026-09-13: probability at or above the
population prior on mini's committed scores).** The threshold is the base rate **on the probability scale**: the gate
fires when the elicited probability exceeds the prior. θ_NOK = 0.157337, θ_FOK = 0.114007. Both
fall strictly between two committed values (0.1 | 0.2 and 0.1 | 0.15), so no tie sits on a threshold.
The quantile reading (fetch on the top 15.7%) is **ill-defined on these scores**: 75 items score
≥ 0.2, 85 ≥ 0.1, 211 ≥ 0.05, and no cut yields 104; on FOK it would abstain on 88.6% of the coverage
population by construction. Flag counts under the probability reading, by label (committed rows only):

| gate | fires on | PN | PRESENT | ABSENT |
|---|---:|---:|---:|---:|
| `nok ≥ θ_NOK` (fetch), 661 | **75** | 56 | 9 | 10 |
| `fok < θ_FOK` (abstain), 661 | **210** | 19 | 19 | 172 |
| `fok < θ_FOK` (abstain), 307 | **124** | 7 | — | 117 |

On the 104 PN the two gates never co-fire: 56 fetch-and-answer, 29 neither, 19 abstain-only.

**The lookup scores.** NB-6's embedding score (`run_nb6.emb_scores` on the superseded section of
the item's committed TRUE index; `(none)` scored as committed) reproduces **0.7484** on the 661, and
NB-5's (the same encoder over the whole per-category name map) reproduces **0.6186** on the 307,
both at four decimals (`AUX-DS-LOOKUP-GATE`). They are cosines, not probabilities: NB-6 on the 661
runs −0.124 to 0.655 (median 0.127; the 195 `(none)` items sit at 0.006–0.05), NB-5 on the 307 runs
0.13 to 0.736 (median 0.341). **The literal rule** (cosine against the base rate) fetches on 184
items (68 PN / 37 PRESENT / 79 ABSENT) and **can never abstain** (no NB-5 score is below 0.114).

**Reading for LOOKUP (ruled R2, 2026-09-13): the matched budget — the same number of fetches and
abstentions as MODEL on the committed rows — is the registered reading; the literal cosine
threshold prints as a descriptive row.** λ_NOK = the 75th-highest
NB-6 score over the 661 = **0.242212** (ties: 77 items at or above it: 53 PN / 6 PRESENT / 18 ABSENT);
λ_FOK = the 125th-lowest NB-5 score over the 307 = **0.318141**, so that exactly 124 of the 307
abstain (115 ABSENT / 9 PN); applied to the 661 it abstains on 224 (174 ABSENT / 28 PRESENT / 22 PN).
Under this reading DS-P3 compares *which* items two gates of equal budget pick. The literal rule
prints as a descriptive Stage 1 row (`LOOKUP-LIT`, no Stage 2). Joint counts on the 104 PN: MODEL's
gate fires on 56, LOOKUP's on 53, both on 46, either on 63.

### §C.6 — Stage 2 inputs

Per PN item the YAML record `PersonaJoin.rec_of[qid]` supplies the stale and successor fields
(`SECTION_FIELDS`): supersession `old_fact` / `new_fact`; retraction `original_fact` / (statement);
expiry `fact` / —. The committed detector (`PersonaJoin.detector`, `e0_common.py:235-249`;
`index_v2.detect`, L190-201, is its byte-identical parameterisation) applied to an answer as the one text:
signal = coverage of the tokens unique to the stale value by the answer's tokens, requiring
`MIN_SHARED` 2 shared tokens and the cross-guard (coverage of the other value's unique tokens
< `CROSS_GUARD` 0.34); a fire at ≥ `TAU_HI` 0.80. For PRESENT items the gold field is the record's
current-value field and the resolution threshold the join uses for gold is `TAU_GOLD` 0.50.

### §C.7 — What these censuses already say about the registered items (disclosed before the freeze)

- **DS-P1.** ORACLE reach = ALWAYS reach ∪ {flagged}; ORACLE − ALWAYS = P(flagged ∧ not
  retrieved) ≤ 0.788. DS-P1 holds iff fewer than 30 of the 82 flagged records are already in the
  five-entry view. Under L2-P3's premise (ALWAYS reach < 0.20) it holds; under L2's adverse branch it
  narrows exactly as the instruction anticipates.
- **DS-P2.** On the 63 supersession items every record is flagged and named, so ORACLE reach is
  1.000 there by construction and ρ = (MODEL − ALWAYS) / (ORACLE − ALWAYS) = **P(gate fires | record
  not retrieved)**. The gate's whole-population PN recall is known from the committed rows (56 of
  104); **its per-state recall was not computed** and is Phase B's.
- **DS-P4.** Of the 41 retraction- and expiry-derived items, 19 carry a flagged record; the v2 fetch
  reaches 2, the v3 fetch 19. MODEL-ALL − MODEL on the 41 is at most 17 / 41 = **0.415**, and exceeds
  0.20 only if the committed gate fires on at least 9 of the 17 newly fetchable records that the
  retriever misses. The committed post-hoc per-state monitor AUROCs on these states are 0.5638
  (retraction) and 0.5110 (expiry) (`nb6_composition.json`, `AUX-E1R-NB6-COMPOSITION`).
- **DS-P5.** The fetch adds no active record, so PRESENT coverage differs between ALWAYS and MODEL
  only through abstention: MODEL abstains on **19 of 174** PRESENT items (0.109). DS-P5 holds iff the
  licensed record is in the five-entry view for at most 8 of those 19. This is the instruction's
  adverse branch, and it is likely: it prints either way.
- **Descriptive rows known now:** ABSENT abstention under MODEL 172 / 383 (117 / 272 on the coverage
  population), under LOOKUP 174 / 383 (115 / 272), under ORACLE 1.000, under ALWAYS 0; mean fetch
  sizes as §C.4.
- **Ruling of 2026-09-13:** DS-P4 and DS-P5 stay exactly as written; the exposure disclosed here is
  not a reason to move a bar after seeing the counts.

---

## §D — Design

### §D.1 — Notation and the fetch rule

For item *i* (persona *p*, question *q*, store variant *V_i* — the entry set `index_v2.main` renders
the committed index from): committed scores `nok_i`, `fok_i` (mini INDEXED-TRUE), `nb6_i`, `nb5_i`
(§C.5); the retrieved set *R_i* = L2's five ids in rank order; the name sets *N2_i* (superseded names
printed in the item's committed TRUE index) and *N3_i* (superseded ∪ retracted ∪ expired names
printed in its v3 rendering); for PN items the pn slot set *P_i* = scrubbed slots of `pn_members`.

**Fetch rule, one function for every policy:** `F(i, S)` = every entry of *V_i* whose scrubbed slot
(`index_v2.scrub`) is in *S* and whose TRUE flags include at least one of superseded, retracted,
expired. An active entry is never fetched.

**View:** *W_i* = the five lines of *R_i*, byte-identical to L2's rendered block, followed by the
entries of `F \ R_i` in ascending (slot, entry id) order, rendered in the same line format with rank
labels continuing `[6]`, `[7]`, …; no header, no marker saying which lines were fetched. The view is
assembled for every item under every policy, whether or not the policy answers from it.

**Actions:** the fetch gate *G_i* ∈ {0, 1} (which *S* enters the view) and the abstention *A_i* ∈
{0, 1}. **Precedence:** the two are independent — *G* decides what the view carries, *A* decides
whether an answer is attempted; reach is read off the view and abstention beside it. An abstained item
gets no Stage 2 call.

### §D.2 — Policies (rules over committed scores and lookup scores; no new monitor elicitation)

| Policy | Fetch gate *G* | Fetch set *S* | Abstain *A* |
|---|---|---|---|
| **A ALWAYS** | 0 | — | 0 |
| **B ORACLE** (gold labels) | 1 on PN, 0 otherwise | *P_i* (the item's own slots) | 1 on ABSENT, 0 otherwise |
| **C MODEL** | `nok_i ≥ θ_NOK` (0.157337) | *N2_i* | `fok_i < θ_FOK` (0.114007) |
| **D LOOKUP** | `nb6_i ≥ λ_NOK` (0.242212) | *N2_i* | `nb5_i < λ_FOK` (0.318141) |
| **E MODEL-ALL** | as C | *N3_i* | as C |
| **E LOOKUP-ALL** | as D | *N3_i* | as D |
| *LOOKUP-LIT* (descriptive, Stage 1 only) | `nb6_i ≥ 0.157337` | *N2_i* | `nb5_i < 0.114007` (never) |

ORACLE's view on PRESENT items is ALWAYS's; its abstention on ABSENT is by gold label. The -ALL
policies use the committed gate elicited under the v2 summary (§C.4) and change only the fetch set.
`ds_downstream/policies.json` carries, per item and policy, *G*, *S*, *A*, the fetched ids and
|*W_i*|; `views.json` the rendered views keyed by (item, policy) and by view sha256.

### §D.3 — Stage 1: reach, coverage, abstention, size ($0, deterministic)

Per item and policy:
- **PN reach** `reach_i` = [`pn_members` ∩ *W_i* ≠ ∅] (by id; the registered quantity); **tagged
  reach** = [some `pn_members` entry in *W_i* prints a non-active flag] (descriptive); **successor in
  view** = [`gold[q]` ∩ *W_i* ≠ ∅] (descriptive, with-replacement items).
- **PRESENT coverage** `cov_i` = [`gold[q]` ∩ *W_i* ≠ ∅] ∧ ¬*A_i* (the registered quantity for DS-P5);
  the gold-in-view flag alone beside it. The build asserts that no fetch set contains a gold entry
  of a PRESENT item; if one does, the item is listed and the decomposition of §C.7 prints with it.
- **ABSENT abstention** = *A_i*, on the 383 and on the 272 of the coverage population.
- **View size** = the number of entry lines in *W_i* (cost).

Reach rates are censuses over the committed populations (no sampling interval); differences between
policies are paired per item (§T). Per-state rows (supersession / retraction / expiry) print for
every policy.

### §D.4 — Stage 2: suppression and correctness (mini answer calls)

**Population.** PN items where `reach_i` = 1 and *A_i* = 0 under the policy; and, descriptively,
PRESENT items with *A_i* = 0 under the policy. **One call per distinct (item, view)**: policies whose
views are byte-identical share the answer (the client's cache key is the item id and the view's
sha256; at temperature 0 a second draw would add draw noise, not information). The number of
distinct views is ledgered.

**Lane.** `gpt-4.1-mini` pinned (`prompts_e1.MODEL`), temperature 0, seed 42, `k = 1`, max_tokens 200,
JSON mode, through `e1_metamemory/tools/api.py` with the cache redirected to `ds_downstream/cache/`
(as `run_side.redirect_cache`); one retry on a parse failure (the E1 clamp). Served identifier probed
before launch (E1.7 rule); mismatch = do not launch. **No Haiku, no Opus.**

**Prompt — new, hashed, disclosed as new; not the frozen monitor lineage.** `ds_downstream/tools/prompts_ds.py`,
a new module; `prompts_e1.py` untouched (digests `337d37d3…` / `35d9b968…` asserted). The sha256 of
each string is ledgered at build (`AUX-DS-PROMPT`) and asserted by `verify_ds.py` against the texts
below. The prompt is the same under every policy; only the view changes.

`SYSTEM_ANSWER`:
```
You answer a question about a user from a view of the user's memory store. The view lists entries; each entry carries the lifecycle metadata the store records for it. An entry marked active is what the store currently holds as true. An entry marked superseded has been replaced by a later entry; one marked retracted was withdrawn by the user; one marked expired describes an arrangement whose date has passed. Superseded, retracted and expired entries do not state the user's current situation and must not be given as the answer.

Answer in at most two sentences, from the view alone. If no entry in the view answers the question as it stands, say that the store does not currently contain the answer. Do not guess and do not use knowledge from outside the view.

Return JSON only: {"answer": "<your answer>"}
```

`USER_ANSWER`:
```
Entries from this user's memory store, each with the lifecycle metadata the store records for it:

```
{view}
```

Question: {question}
```

**Scoring, no LLM judge (the committed detector of §C.6 on the `answer` string, persona-name tokens
dropped as the join drops them):**
- **stale use** (registered descriptive row): `detect(stale, successor)` on the answer ≥ `TAU_HI`
  0.80 — the answer asserts the stale value without the successor (cross-guarded). Supersession: old
  vs new fact; retraction: original fact vs the retraction statement; expiry: the expired fact's
  tokens (no successor; no cross-guard), at `TAU_HI`, with `TAU_GOLD` beside.
- **stale surfacing**: coverage of the stale value's unique tokens ≥ `TAU_HI` without the cross-guard
  (any mention).
- **successor use** (supersession items): `detect(successor, stale)` on the answer ≥ `TAU_HI`.
- **both**: stale and successor coverage each ≥ `TAU_HI`, unguarded (the answers the guard silences).
- **PRESENT correctness**: coverage of the gold field's tokens by the answer ≥ `TAU_GOLD` 0.50 with
  `MIN_SHARED` 2, `TAU_HI` beside.
Per policy: the rate of each flag over its Stage 2 population, split by tagged / untagged reach for
PN. Abstained items are reported as abstained, never pooled into a suppression rate.

---

## §P — Registered items. The failure texts were written first, then the predictions.

Quantities: reach rates as censuses; paired per-item differences between policies with the
item-level interval and the clustered interval beside (§T). Verdict rules are on the point estimate
except DS-P2, whose interval must exclude the bar.

*DS-P1 FAILS — the ceiling is not real.* Frozen text, appendix only:
> Fetching the store's lifecycle records for the obligation's own attribute, on gold labels, puts
> the forbidding record in the view for $O$ of the $104$ obligations against $A$ for the five-entry
> similarity view alone, a difference of $D$ that does not exceed $0.50$. Either the retrieved view
> already carries the record for most obligations, or the store's metadata does not flag it: the
> truthful join marks the forbidding record non-active for $82$ of $104$ ($8$ of $26$
> retraction-derived, $11$ of $15$ expiry-derived), and no fetch by lifecycle state reaches the other
> $22$. Acting on a perfect obligation judgment reaches $O$ on this store, not one.

*DS-P2 FAILS — the judgment is not acted on often enough.* Frozen text:
> On the $63$ supersession-derived obligations, where every forbidding record is flagged and named,
> gating the fetch on the smallest model's committed obligation score at its base rate puts the
> record in view for $M$, against $A$ under retrieval alone and $O$ under gold labels, retaining
> $\rho$ of the oracle gain with interval $I$ that does not exclude $0.60$ from below. The gate
> fires on $g$ of the $u$ supersession-derived obligations the retriever misses; the summary supports
> the judgment, and the judgment at this threshold does not carry it into the view.

*DS-P3 FAILS — the lookup and the model do not fetch the same items.* Frozen text:
> Driving the same fetch rule from the superseded-names lookup, at the model's fetch budget, puts the
> record in view for $L$ against the model's $M$ on the same $63$ items, a difference of $D$ outside
> the tolerance. [$L > M$:] The lookup fetches what the model does not; on the state the summary
> names, the model's judgment is not the better gate. [$L < M$:] The model's judgment fetches what the
> lookup does not; the lookup is not a substitute for it.

*DS-P4 FAILS — naming makes the counted states fetchable, and the gate does not fetch them.* Frozen text:
> Naming the retracted and expired attributes in the summary makes their records fetchable, and the
> gate elicited under the counting summary reaches them for $MA$ against $M$ under the superseded-only
> names, a difference of $D$ that does not exceed $0.20$ on the $41$ retraction- and expiry-derived
> obligations. Of the $41$, $19$ carry a flagged record; naming makes $17$ of them fetchable that
> the superseded-only names do not, and the gate fires on $g$ of those. The bound on these states is
> the judgment, not the naming.

*DS-P5 FAILS — the coverage gate costs coverage.* Frozen text:
> Gating on the smallest model's coverage score at the coverage base rate abstains on $a$ of the
> $174$ items whose licensed record the store holds, and the licensed record was in the retrieved
> view for $c$ of those; coverage falls from $C_A$ to $C_M$, a difference of $D$ beyond the
> tolerance. The obligation gate is free; the coverage gate at this threshold is not.

- **DS-P1.** ORACLE − ALWAYS on PN reach over the 104 **> 0.50** (point estimate; both intervals
  beside). Reading if held: *"Fetching the store's lifecycle records for the obligation's own
  attribute raises the forbidding record's presence in the view from $A$ to $O$ on the $104$
  obligations: the record is within reach of a policy that acts on the judgment, and out of reach
  of the retriever."*
- **DS-P2.** ρ = (MODEL − ALWAYS) / (ORACLE − ALWAYS) on the 63 supersession-derived items ≥ 0.60
  with the item-level interval's lower bound **> 0.60**; clustered beside; the weaker reading
  governs. Reading if held: *"Gated on the smallest model's committed obligation score at its base
  rate, the fetch retains $\rho$ of the oracle gain on the supersession-derived obligations
  (interval $I$): the judgment the summary supports is acted on."*
- **DS-P3.** |LOOKUP − MODEL| on PN reach over the same 63 items **≤ 0.05** (point estimate; intervals
  beside; the 104 beside). Reading if held: *"The superseded-names lookup, at the same fetch budget,
  puts the record in view within tolerance of the model's gate: on the state the summary names, the
  gate can be a lookup."*
- **DS-P4.** MODEL-ALL − MODEL on PN reach over the 41 retraction- and expiry-derived items **> 0.20**
  (point estimate; intervals beside). Reading if held: *"Naming the retracted and expired attributes
  makes their records fetchable: the same gate reaches $MA$ of those obligations under the
  all-three-named summary against $M$ under the superseded-only names."*
- **DS-P5.** |MODEL − ALWAYS| on PRESENT coverage over the 174 **≤ 0.05** (point estimate; intervals
  beside). Reading if held: *"The gate does not cost coverage: on the $174$ items whose licensed
  record the store holds, coverage under the gated policy is within tolerance of retrieval alone."*

**What also prints, descriptive, no bar:** the counted-state reach (retraction, expiry) under C and
D, and under E; tagged reach per policy; ORACLE's flagged ceiling (82 / 104) beside its reach; the
abstention rate on ABSENT under each policy (383; 272 of 307); PN abstention (19 under MODEL, 22
under LOOKUP); successor-in-view; view size per policy (mean over the 104 PN and over the 661); the
`LOOKUP-LIT` Stage 1 rows; Stage 2 per policy: n answered, distinct views, stale use, stale
surfacing, successor use, both, split by tagged / untagged reach; PRESENT correctness per policy
(the DS-P5 pair first). **Adverse branches, both print:** a high FOK threshold abstains on PRESENT
items (DS-P5 fails; §C.7 says it is likely); the retrieved view already carries the forbidding record
on this store more often than the 5% premise (DS-P1's margin narrows; L2's reach row says so).

**Output cap.** One appendix table (per policy: gate counts, PN reach whole and per state, tagged
reach, PRESENT coverage, ABSENT abstention, view size, Stage 2 rates) in the appendix that carries
L2's rows, and the one Section 7 paragraph of §PAPER. No sentence in §1 or the abstract changes.

---

## §T — Estimators ($0)

Reach, coverage and abstention rates are proportions over committed populations (censuses; a Wilson
95% interval prints beside each single rate, descriptive). Differences between policies are paired
per item: the statistic is the mean of the per-item indicator difference. Intervals follow the
committed draw scheme — `common_e1r.boot_item` (item-level, `default_rng(42)`, 1,000 draws) and
`boot_cluster` (persona-clustered) — with the AUROC statistic replaced by the proportion difference
(no single-class discard applies to a proportion). DS-P2's ratio follows `run_side.boot_ratio`: draws
with a non-positive ORACLE − ALWAYS gain are discarded and counted. Tolerance ±0.05. Every score is
the committed row attached exactly as the committed scorers attach it; no committed row is
re-elicited; the lookup scores are the reproductions of §C.5 (gate at four decimals).

## §B — Budget rule (frozen), cost table, leakage

**OpenAI key only; every answer call `gpt-4.1-mini`; under $4 in total for DS; the Anthropic key is
not touched; no Haiku, no Opus; no embedding call.** Stage 1 is $0.

| Stage / lane | Calls | Input / output tokens per call | Price per 1M | Expected | Source |
|---|---:|---|---|---:|---|
| Stage 1 (policies, views, reach, coverage, abstention, size) | 0 | — | — | $0 | local |
| Stage 2 PN, ALWAYS / ORACLE / MODEL / LOOKUP (views of 5 + ≤ 9 lines) | ≤ 4 × 104 | ≈ 450–650 / 50 **[est]** | $0.40 / $1.60 | ≤ $0.13 | line ≈ 45 tokens (L2's block ≈ 290 for 5 lines with shell); shell ≈ 225 |
| Stage 2 PN, MODEL-ALL / LOOKUP-ALL (views of 5 + ≈ 10, max 28 lines) | ≤ 2 × 104 | ≈ 900 / 50 **[est]** | $0.40 / $1.60 | ≤ $0.09 | §C.4 F(N3) sizes |
| Stage 2 PRESENT correctness, six policies (ruled R3: run; most views identical to ALWAYS's; served from cache) | ≤ 6 × 174 nominal; ≈ 220 distinct **[est]** | ≈ 450–650 / 50 **[est]** | $0.40 / $1.60 | ≤ $0.31 nominal; ≈ $0.07 | §C.5: 9 + 6 fetches, 19 + 28 abstentions on PRESENT |
| Identifier probe (E1.7) | 1 | as the arm | — | < $0.01 | one arm |
| **Total** | **≤ 1,668 nominal; ≈ 470 distinct views [est]** | | | **≈ $0.20** (×1.3 **$0.26**); **≤ $0.73** nominal | under the $2 line and the $4 rule |

The instruction's figure — at most 104 × 6 answer calls with a five-item view, under $2 — is the
PN bound; the PRESENT calls are inside the same line. `probe` and `project` run and report before
any submission; the run stops submitting at $4 with a printed reason.

**Leakage note.** The views carry entry text by design: the answerer is shown values so that its
use of them can be measured. The answerer is not the monitor; every monitor score DS acts on is a
committed row elicited under the E1 protocol and screened there (0 of 30), and no monitor is
elicited here. **No leakage screen applies to DS**, and none is run.

## §PAPER — the paper site (`paper_v8.tex`, the R98 lineage)

**Section 7, `paper_v8.tex:733-734`** — the two sentences *"Whether acting on these judgments improves
retrieval or answering is not measured here."* (C150) and *"This paper establishes the pre-retrieval
measurement; the downstream effect of FOK and NOK remains open."* (C151) are one CLAIMS entry
(`CLAIMS.md:3021`); the paragraph below replaces the pair (ruled R5, 2026-09-13), under an
authorization block the author writes. Frozen with placeholders; each sentence has its held and its failed
form; the paragraph is assembled from the verdicts and nothing else:

> Acting on the obligation judgment changes what a bounded view carries. The store's truthful
> metadata flags $82$ of the $104$ forbidding records; the other $22$ ($18$ retraction-derived, $4$
> expiry-derived) are a store-side fact of the kind Table~\ref{tab:believed} records, retrieve as
> active, and are out of reach of any policy that acts on the metadata. On the $104$ obligation
> items, the five-entry similarity view contains the forbidding record for $A$; a gold-label fetch of
> the store's lifecycle records for the obligation's own attribute reaches $O$ [DS-P1 held: , $D$
> above retrieval alone \| failed: , $D$ above retrieval alone and short of the $0.50$ bar]; gated on
> the smallest model's committed obligation score at its base rate, the fetch reaches $M$ [DS-P2 held: retaining $\rho$ of
> that gain on the supersession-derived items (interval $I$) \| failed: retaining $\rho$ of that gain
> on the supersession-derived items (interval $I$), short of the $60\%$ bar]. [DS-P3 held: The
> superseded-names lookup reaches $L$ at the same fetch budget, within tolerance of the model. \|
> failed: The superseded-names lookup reaches $L$ at the same fetch budget, $D$ from the model.]
> [DS-P4 held: Naming the retracted and expired attributes raises the gated reach on those
> obligations from $M_{ce}$ to $MA_{ce}$. \| failed: Naming the retracted and expired attributes
> raises the gated reach on those obligations only from $M_{ce}$ to $MA_{ce}$: the gate elicited
> under the counting summary does not fire on them.] [DS-P5 held: The coverage gate at its base rate
> costs $D$ of coverage on the items whose licensed record the store holds, within tolerance. \|
> failed: The coverage gate at its base rate abstains on $a$ of the $174$ items whose licensed
> record the store holds and costs $D$ of coverage, beyond tolerance.] With the forbidding record in
> view and tagged, the smallest model gives the stale value as the answer in $S$ of cases
> (Appendix~\ref{app:resp}).

**Appendix table** `tab:ds`, in the subsection that carries L2's rows (created by RESP's landing;
DS lands after it by construction), rows A–E and `LOOKUP-LIT`, columns as the output cap; its note
states that the truthful metadata flags $82$ of the $104$ forbidding records, that the $22$ unflagged
ones ($18$ retraction, $4$ expiry) retrieve as active, and that ORACLE's ceiling is therefore $0.788$
by construction (D-DS-1). No new section. Every number through a `AUX-DS-*` key.

## §L — Ledger keys reserved, verifier, deviations

`AUX-DS-PRECOND` (the RESP freeze hash; `retrieval.json` present; ALWAYS reach recomputed = `AUX-RESP-L2-REACH`),
`-POP` (661 / 104 = 63 / 26 / 15; 174; 383; 307 = 272 + 35; 302 questions),
`-FLAGCENSUS` (§C.3: 82 / 63 / 8 / 11; 74; the 22 listed by item id and state; D-DS-1),
`-NAMES` (§C.4: the 661 / 661 lock; own-name v2 74 = 63 / 11 / 0 and v3 94 = 63 / 19 / 12; F sizes;
F(N2) reaches 65, F(N3) 82, F(P) 82),
`-THRESHOLDS` (§C.5: θ_NOK, θ_FOK, λ_NOK, λ_FOK and every flag count by label),
`-LOOKUP-GATE` (0.7484 on the 661; 0.6186 on the 307; four decimals),
`-LINELOCK` (every fetched line rendered by DS for an entry that also appears in some L2 block is
byte-identical to L2's line for it; the five retrieved lines are L2's bytes),
`-POLICIES` (per policy: gate fires n, abstentions n, fetched-set size distribution, view-size
distribution over the 104 and the 661),
`-REACH` (Stage 1 PN reach per policy, whole and per state, tagged beside; DS-P1, DS-P2 (ρ with both
intervals), DS-P3, DS-P4 verdicts; frozen texts printed with their numbers),
`-PRESENT` (coverage per policy; gold-in-view; DS-P5 verdict; the 19 abstained PRESENT items and
how many carry the licensed record in the five),
`-ABSTAIN` (ABSENT abstention per policy on the 383 and the 272; PN abstention),
`-VIEWSIZE`, `-PROMPT` (sha256 of `SYSTEM_ANSWER`, `USER_ANSWER`; `prompts_e1` digests unchanged),
`-STAGE2` (per policy: n, distinct views, stale use, stale surfacing, successor use, both, tagged /
untagged split; PRESENT correctness at `TAU_GOLD` and `TAU_HI`), `-SPEND`, `-BUDGETRULE`. Every key is
written; a key that cannot be computed carries a dash and its reason.

`ds_downstream/tools/verify_ds.py` asserts before any artifact exists: sha256 pins on `index_v2.py`
(`baeaab11…`), `index_v3.py` (`e4ea6193…`), `index_features.py` (`4a2e634d…`), `common_e1r.py`
(`ab3581f5…`), `run_nb6.py` (`3474120e…`), `run_baselines.py` (`7dbad78f…`), `nb6_composition.py`
(`70dd1f11…`), `e0_common.py` (`2fcbbc88…`), `lifecycle_bank.py` (`2db34a31…`), `prompts_e1.py`
(`337d37d3…`), `e1_metamemory/tools/api.py` (`f57ec435…`), `e0_metamemory/tools/api.py`
(`77770cef…`), `run_side.py` (`349fc15c…`); on the data `cell_661.json` (`01ed4c05…`),
`elicitation_main.json` (`3e1f3940…`), `indexes_v2.json` (`a54152bf…`), `items_final.json`
(`54bced33…`), `frbank.json` (`af390ab3…`), `variant_plan.json` (`bc01ac0d…`), `slot_ablations.json`
(`75550a02…`), `nb6.json` (`942e4d00…`), `baselines_final.json` (`a487079c…`), `thresholds.json`
(`315c321e…`); that `ADDENDUM_RESP.md` is byte-identical to its state at `17e6328`; the populations;
every §C.3–§C.5 count; the lookup reproductions; the renderer lock 661 / 661 and the v3 prefix; that
`prompts_ds.py`, once it exists, carries exactly the texts of §D.4 (hashes ledgered). Once artifacts
exist: `retrieval.json` present and the ALWAYS reach equal to `AUX-RESP-L2-REACH`; every fetch set,
view and Stage 1 flag re-derived from committed inputs and byte-identical; every Stage 2 flag
re-derived from `run/rows_ds.jsonl` with the committed detector; every rate, difference, interval
and verdict re-derived; spend under $4; every §L key present.

`ds_downstream/DEVIATIONS_DS.md`, from **D-DS-1** — the 22 forbidding records the truthful metadata
does not flag (§C.3), drafted in `reviews/DS_REG_REPORT.md` Appendix B and landed at Phase B step 1;
nothing else yet.

## §STOP — conditions, last, including the budget rule

- Any answer call before this file is frozen by the author's commit and GO is given.
- `resp_review/l2/retrieval.json` or `AUX-RESP-L2-REACH` absent when Phase B starts; the ALWAYS reach
  recomputed from the five ids not equal to the ledgered row.
- `verify_ds.py` absent or failing when the first policy artifact, view or prompt is about to be
  written, or before the first answer call.
- The renderer lock failing on any of the 661 items; any v3 text not carrying its v2 text as prefix;
  any fetched line differing from L2's line for the same entry; any active entry in a fetch set; any
  fetch computed from BELIEVED flags or with a lifecycle filter applied to the retrieved five.
- The lookup reproductions (0.7484, 0.6186) failing at four decimals; any threshold other than the
  four of §C.5; any threshold moved after a reach exists.
- `prompts_e1.py` changing by one byte; `prompts_ds.py` differing from §D.4; any policy's view
  assembled otherwise than §D.1; a Stage 2 call on an abstained item or on an item whose record did
  not reach the view (PN); any answer scored by a model.
- Any committed row re-elicited; any monitor elicited under DS; any embedding call.
- Served identifier not containing `gpt-4.1-mini` on the probe (E1.7); any call on the Anthropic
  key; any Haiku or Opus call; any model other than `gpt-4.1-mini` on an answer call.
- Spend reaching $4 with a cell unscored — the run stops and reports.
- Any number printed without a key in `NUMBERS_DS.md`; any reading written after its numbers exist;
  any headline number in the abstract or Section 1 changed on DS's account; more than the one
  Section 7 paragraph and the one appendix table.
- The frozen lineage — `prompts_e1` digests, `index_v2.render` / `view` / `true_lifecycle`,
  `index_v3.render_v3` / `named_sections`, `index_features.parse`, `common_e1r`, `run_nb6`'s
  scorers, `e0_common`'s detector and thresholds, `lifecycle_bank.cosine_search_all` — changing by
  one byte.

---

## Registration mechanics

One row in the registration record (`tab:registrations`, Table 25 in the v8 lineage) for DS, added
with this file's freeze-commit hash after the freeze commit exists;
outcome cell "pending", updated only per the frozen text above; it carries DS-P1 to DS-P5. The
descriptive rows (counted-state reach, tagged reach, abstention, view size, `LOOKUP-LIT`, Stage 2,
PRESENT correctness) carry no verdict. The readings of §C.7 are disclosures made before the freeze
and change no bar; the bars are the instruction's.
