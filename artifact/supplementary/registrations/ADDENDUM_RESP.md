# ADDENDUM_RESP — registration for the review-response lanes L1, L2, L3

Frozen against baseline HEAD `2a943d7` (branch `[BRANCH]`), 2026-09-12 (R98), **BEFORE any
V2-OWN index, retrieval artifact, prompt variant or monitor call exists**. Spec: the RESP-REG
instruction of 2026-09-12, answering an external review of `paper_v6.tex` (W1/Q1, W3/Q3, W4/Q2 and
the minor list), and the six Phase A rulings of the same day (`reviews/RESP_REG_REPORT.md` §6: the
`text-embedding-3-small` batch confirmed as the one non-mini call; TRUE-REDRAW kept; `resp_review/`;
Q5 per the artifacts; Amendment 1 to ADDENDUM_SIDE drafted; D-E1R-10 drafted). Rules inherited from R74/R76/R77/R81/R82/SIDE: nothing unregistered may be
reported; no committed value is recomputed; registered verdicts are never re-adjudicated;
**publish-regardless** — every result prints under its frozen text. The template is
`ADDENDUM_R77.md` §S and `ADDENDUM_SIDE.md`: committed populations, committed blind and TRUE rows
read and never re-elicited, only the manipulated input changed, failure texts written before the
predictions.

**Results print in the appendix. At most one main-text sentence per lane, at the site the
reviewer's point lands (§L1, §L2, §L3 "output cap"). No headline number in the abstract or
Section 1 changes on account of L1, L2 or L3.** The $0 paper items for R97 are listed in
`reviews/RESP_REG_REPORT.md` §5 and are not part of this registration, except that the Q4 marker
fraction enters through the ledger key `AUX-RESP-PAPER-Q4`.

**AI use.** The draft, the censuses and the ledger entries were prepared with Claude Code under
the author's instruction; every number traces to a committed artifact or to a script named in
`reviews/RESP_REG_REPORT.md`. Verdicts are mechanical under the frozen criteria.

Ledger: `resp_review/NUMBERS_RESP.md`, keys `AUX-RESP-*` (all reserved in §L; the directory name
is the author's call). Verifier: `resp_review/tools/verify_resp.py`, **required to exist and pass
on the empty cell before any V2-OWN index, retrieval artifact or prompt variant is written, and
again before the first monitor call**. Deviations: `resp_review/DEVIATIONS_RESP.md`, own numbering
from **D-RESP-1**. Bootstrap: the committed estimators (`e1r_robustness/tools/common_e1r.py`:
Mann-Whitney AUROC with ties at 0.5; paired item-level bootstrap, 1,000 draws, seed 42,
single-class draws discarded), persona-clustered interval printed beside; where the two disagree
on a prediction the text says so and the weaker reading governs (`ADDENDUM_R82.md` §6,
`ADDENDUM_SIDE.md` §T). Tolerance ±0.05 throughout, the count-destruction tolerance.

Metered budget: **the rule of §B, frozen: OpenAI key only, `gpt-4.1-mini` only for every monitor
call, under $4 in total for the three lanes; nothing on the Anthropic key.** The one call that is
not `gpt-4.1-mini` is the retriever's own encoder, `text-embedding-3-small`, for the question
vectors L2 needs (§C.3, §L2; about 302 short inputs, well under one cent), **confirmed by the
author's ruling (1) of 2026-09-12** and disclosed here and in the ledger as the one non-mini call.

---

## §C — Pre-freeze censuses (all $0, deterministic, local, disclosed rather than inferred)

Every quantity in this section was computed **before this draft** from committed artifacts with
local code and no model call (`reviews/RESP_REG_REPORT.md` Phases 1–3 name the scripts). Their
values are invariant to when they are computed. **No registered outcome quantity was computed**:
no V2-OWN score, no NB-6 on an ablated list, no retrieval reach, no rubric-variant score. What was
computed is structural — which items the ablation can touch, how the encoder scores names against
names, which questions the retriever can be run on — and it is needed to write the arms, the
projection and the failure texts.

### §C.1 — The own-name census, and the committed 7-of-104 figure

**The committed figure is wrong, and the reason is a key collision.** `paper_v6.tex:1861` and
`e1r_robustness/NUMBERS_E1R.md:340-372` (`AUX-E1R-NB6-COMPOSITION`, post hoc) print that each
obligation's own attribute name appears in the superseded-names section it was shown for **7 of
104** items under TRUE (5 of 63 supersession, 2 of 26 retraction, 0 of 15 expiry). The script
behind it, `e1r_robustness/tools/nb6_composition.py::slot_map`, builds `{entry_id: slot}` over
`backend_entries/frbank.json` **without the persona**: FR-Bank entry ids restart at `lb_00001`
in every persona bank (18,936 entries, 622 distinct ids, each reused by up to 40 personas), so the
map returns the slot of whichever persona came last in the file. Keyed by (persona, entry id), the
same check finds:

| Provenance | supersession (63) | retraction (26) | expiry (15) | all (104) |
|---|---:|---:|---:|---:|
| TRUE, committed figure (`nb6_composition.py`) | 5 | 2 | 0 | 7 (0.067) |
| **TRUE, persona-keyed** | **63 (1.000)** | **11 (0.423)** | **0** | **74 (0.712)** |
| BELIEVED, committed figure | 10 | 1 | 2 | 13 (0.125) |
| BELIEVED, persona-keyed | 24 | 3 | 4 | 31 (0.298) |

"Own name" here is the scrubbed slot (`index_v2.scrub`, the path up to the first colon) of each
`pn_members` entry, matched exactly against the section's names — the committed check's own
definition with the key fixed. **Every supersession-derived obligation carries its own name in the
TRUE section it was shown.** This is not a registered quantity of this addendum; it is a defect in
a committed post-hoc census that prints in the manuscript, reported to the author in
`reviews/RESP_REG_REPORT.md` §4 (F1); ruling (6) records it as **D-E1R-10** (drafted there,
Appendix C) with the R97 corrections under authorization blocks. It
is disclosed here because L1 is built on it: the ablation's reach is 63 of 63 on the state the
paper says the index names, not 5 of 63.

### §C.2 — L1: what V2-OWN can touch, and the neighbour threshold

**The committed TRUE indexes of the 661.** 242 distinct index keys (`index_features.index_key`,
the exact string each item was shown; FULL and CAT-ABLATED shared per persona, SLOT-ABLATED per
question). The superseded-names section holds **1 to 5 names** where it holds any (mean 1.785 over
keys); **63 of 242 keys (195 of 661 items) print `(none)`**. NB-6's committed 1.7474 names per
item counts `(none)` as a name, because `index_features._names` does not special-case it; the
committed NB-6 therefore scored those items against the string "(none)". That is the committed
behaviour and is not changed here; NB-6 on the ablated list (§L1) reads the ablated text through
the same parser. **35 distinct real names** appear across the 242 sections; **47 distinct
within-section pairs**.

**Section renderer lock (verified 2026-09-12).** Re-rendering the section body from its parsed
names through the renderer's own `name_block` rule (sorted set, `SLOT_CAP` 15, `textwrap.wrap` at
`WRAP` 150, indents `"  "` / `"    "`, `(none)` when empty) reproduces the committed text **byte
for byte on 242 of 242 keys**, and the section is the tail of every text. V2-OWN is therefore a
text surgery on the committed string: the section body is replaced by the same rule over the
reduced name set; every byte before the section header is untouched.

**The target name set T(q), one rule for all 661 items.** For item *i* with persona *p* and
question id *q*: the scrubbed slots of *i*'s `pn_members` (hand-verified, PN items only), united
with the scrubbed slots of the question's resolved entries in the committed persona join
(`e0_common.PersonaJoin`: `gold[q]`, the entries of `fires[q]` at signal ≥ `TAU_HI` 0.80, and
`expired_neg[q]`), keyed by (persona, entry id), entries without a slot skipped. **145 natural-absent
probe items have no join record and no `pn_members`, so T = ∅ and they cannot change.** |T|
over the 661: 0 for 145, 1 for 219, 2 for 152, 3 for 83, 4 for 42, 5 or more for 20.

**Neighbour threshold τ, derived from NB-6's encoder before any ablation exists.** NB-6's
embedding variant scores a question by its maximum cosine to a section name under
`sentence-transformers/all-MiniLM-L6-v2` (local, offline; `run_baselines.encoder`), on the name
with underscores replaced by spaces. Under that encoder, over the 35 names: the 577 pairs of
distinct names sharing **no** content token (`index_features.toks`) form the null distribution of
"unrelated" name-name cosines — median 0.145, p90 0.313, p95 0.356, **p99 0.503637**, max 0.649.
**τ = 0.503637, the 99th percentile of that null.** A name *n* in the section is a neighbour of
a target name *t* when cos(*n*, *t*) ≥ τ, whether or not *t* itself is in the section. Under τ the
within-section pairs that count as neighbours are six: workspace|workspace_location 0.835,
placement_location|placement_status 0.725, employer|job_title 0.609, activity|hobby 0.593,
job_responsibility|job_title 0.580, current_neighborhood|current_residence 0.567. One
token-sharing within-section pair sits below τ and is **not** removed:
job_employer|job_night_shift_duration 0.342. NB-6's lexical variant is not closed by τ; the
disclosure stands and the lexical NB-6 prints beside the embedding one on the ablated list.
(Descriptive, not used: NB-6's Youden operating point on the committed 661 TRUE scores is a
question-to-name cosine of 0.2018; it is a question-side quantity and does not transfer to
name-name pairs, where the null median is already 0.145.)

**Census of the ablation under τ (`census_l1.py`, 2026-09-12):**

| | items | changed under V2-OWN | of which section emptied to `(none)` |
|---|---:|---:|---:|
| all | 661 | **102** | 41 |
| PRESENT-NEGATIVE | 104 | **74** | 34 |
| — supersession-derived | 63 | **63** | 30 |
| — retraction-derived | 26 | **11** | 4 |
| — expiry-derived | 15 | **0** | 0 |
| PRESENT | 174 | 16 | 4 |
| ABSENT (ablation 238, natural 145) | 383 | 12 (natural: 0) | 3 |
| by variant FULL / CAT-ABLATED / SLOT-ABLATED | 323 / 176 / 162 | 46 / 16 / 40 | — |
| items where a neighbour (not an own name) is removed | — | 6 | — |

The six neighbour removals are job_title beside employer or job_change_reason (3 items) and hobby
beside career or employer (3 items). **559 of 661 items have a V2-OWN text byte-identical to their
committed TRUE text.**

**Two consequences, stated now.** (i) On expiry-derived items the ablation removes nothing from
the positives; what can move the expiry AUROC is the 28 changed negatives, since every per-state
split scores against the same 557 negatives. The order's premise "the index never named them" is
exact for expiry and **not exact for retraction**: 11 of 26 retraction-derived obligations carry
their own name in the section (their slot also carries a supersession). L1-P2 is registered as
written and the retraction row prints with that census beside it. (ii) In 41 items the section
becomes `(none)` while LIFECYCLE TOTALS and the per-category SUPRSD column still count the
superseded entries — the ablation removes the name and nothing else, by order. A reader that
recovers the obligation from those counts is exactly the adverse branch of L1-P1.

### §C.3 — L2: the retriever the premise names, and what it needs

**The 5% is a mask rate, not a ranking rate.** `paper_v6.tex:131` ("retraction records survive
similarity retrieval at only 5%"), the Figure 1 caption (L109), the abstract's third sentence
(L51) and Table 12's "Inherited retrieval premise" row (L1546) cite the FR paper. In the canonical
FR text (`neuripsv13.tex:206`, `:274`, `:2860`) the 5% is FR-Bank's **AV7 retrieval-pass rate under
its full lifecycle stack**, and the FR paper attributes it to the lifecycle state mask
($M_q(\xi)$: "retracted facts are correctly excluded from the retrieval set"), not to where the
record ranks by similarity. The monitoring paper's premise sentence glosses a mask effect as a
ranking effect. This addendum does not edit that sentence (`reviews/RESP_REG_REPORT.md` §4, F2 is
the author's); it registers the ranking quantity the sentence asserts, measured directly.

**The retriever.** The similarity stage of FR-Bank's own pipeline, `lifecycle_bank.py`
`LifecycleBank.cosine_search_all` (L402–414): cosine over **every entry the store variant holds,
active or not** (the `include_inactive=True` path of `lifecycle_search`, L916–), on the bank's
cached `text-embedding-3-small` vectors (`LifeMemEval/artifacts/lifecycle_banks/<persona>_embeddings.npz`;
verified 2026-09-12 to cover all 18,936 entries of the 40 personas), **top 5 by cosine**. The
store variant is the item's own: FULL, CAT-ABLATED (the persona's ablated categories,
`build/variant_plan.json`) or SLOT-ABLATED (`build/slot_ablations.json[persona:qid]`), the exact
entry sets `index_v2.main` renders the committed index from. BM25, category-forced retrieval,
multi-hop expansion, distillation, the lifecycle filters and the blended scoring are **not**
applied: the first needs the query classifier and the distiller (LLM calls), and the filters are
the mask whose effect the premise sentence does not describe. What is measured is whether the
forbidding record ranks in the top five by similarity.

**Question vectors.** 302 distinct questions across the 661 items. **187** are LifecycleBench
questions with a cached `text-embedding-3-small` vector (`artifacts/theory/query_emb_cache.npz`,
516 questions, the presence control's cache); **115** are natural-absent probe questions with no
cached vector. The registration embeds **all 302 fresh** with `text-embedding-3-small` (one batch
call path, about 4,500 input tokens, well under one cent), asserts that the 187 cached vectors
reproduce the fresh ones at cosine ≥ 0.99 each (a failure is a STOP), and pins the fresh matrix by
sha256 (`resp_review/l2/question_emb.npz`). This is the only call on any model other than
`gpt-4.1-mini` under this registration (ruling (1), 2026-09-12).

### §C.4 — L3: the committed blind arm the reviewer explains

On the 661, the committed mini blind `nok` takes **two values: 0.0 on 655 items and 0.1 on 6**;
`nok_candidates_found` is **false on all 661**; all 104 PN sit at 0.0; AUROC 0.4946
(`elicitation_main.json`, read). On the cross-model 84 it takes one value (Table 3's caption).
The reviewer's explanation — the Step 1 boolean gate pins the probability — is testable by
removing the gate and nothing else (§L3).

### §C.5 — Q4 marker fraction (ledger key `AUX-RESP-PAPER-Q4`, computed 2026-09-12)

Every committed Mem0 (37) and A-MEM (40) FULL index is 31 lines. Under TRUE the inexpressibility
marker (`not expressible by this backend`, 6 o200k tokens) occurs **3 times per index, on 3 of 31
lines, 18 of 216 tokens = 8.3%** on both backends (every index tokenises to exactly 216). Under
BELIEVED it occurs **7 times on Mem0, on 7 of 31 lines, 42 of 232 tokens = 18.1%**, and **8 times
on A-MEM, on 8 of 31 lines, 48 of 236 tokens = 20.3%** (every Mem0 BELIEVED index tokenises to
232, every A-MEM one to 236). The persona of median joint size is `leila`; its
two TRUE indexes are the verbatim texts proposed for the appendix (`reviews/RESP_REG_REPORT.md`
§5, item 4).

---

## §L1 — Own-name ablation (W3): does the reader take the obligation from the name?

**Question.** Under the TRUE index the superseded-names lookup matches the smallest model on
obligation (0.7484 against 0.7339, `paper_v6.tex:452`), and the manuscript says the obligation is
"read off the names it marks superseded" (L157). If the reader takes the obligation from the
target's own name, removing that name — and every name the encoder cannot tell from it — should
cost the reader its supersession discrimination and nothing else.

**Population, asserted by the runner.** `r74/x4/cell_661.json`: **661 items, 104 PN** (63
supersession / 15 expiry / 26 retraction by attack vector, `nb6_composition.AV_STATE`; FULL 323 /
CAT-ABLATED 176 / SLOT-ABLATED 162), joined to the committed rows exactly as `common_e1r.assemble`
joins them.

**Lane.** `gpt-4.1-mini` pinned, temperature 0, seed 42, `k = 1`, max_tokens 200, the E1 protocol
(`api.call`, JSON mode, the E1 clamp, one retry on a parse failure), frozen `prompts_e1.SYSTEM` +
`USER_INDEXED` with both digests asserted (`337d37d3…` / `35d9b968…`). Served identifier probed
before launch (E1.7 rule); mismatch = do not launch. **No Haiku, no Opus.**

**Arms.**
- **V2-OWN** — the item's committed TRUE index (`index_features.index_key(item, "TRUE")`) with
  the section under `ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT` re-rendered over the names that
  remain after removing every name in T(q) and every name at cosine ≥ τ = 0.503637 to a name in
  T(q) (§C.2). Everything before the section header is byte-identical. **Where nothing is removed
  (559 items, §C.2) the V2-OWN text equals the committed TRUE text and the item's V2-OWN score is
  the committed TRUE score, read, not re-elicited** — the same prompt at the same decoding would
  measure the model's draw noise (E1 D19/D21), not the ablation. The 102 changed items are
  elicited. `resp_review/l1/indexes_own.json` carries all 661 texts keyed by item id, with the
  removed names, the removal reason (own / neighbour) and a `changed` flag per item.
- **INDEXED-TRUE (committed)** — `elicitation_main.json` INDEXED-TRUE rows by item id. Read.
- **BLIND (committed)** — by question text. Read; descriptive only, since the mini blind arm
  anchors no gain on this population (R96, `paper_v6.tex:475–479`).
- **TRUE-REDRAW (descriptive noise floor; kept by ruling (2) of 2026-09-12: without it L1's drop
  has no reference).** The committed TRUE prompt of the 102 changed items, elicited once more
  under a distinct arm name so the cache cannot serve it. It is not a replacement for the TRUE
  arm, which stays the committed rows and is the comparator of every registered item; it prints
  the paired REDRAW − TRUE difference on the same 102 items as the draw-noise floor beside the
  V2-OWN − TRUE difference, whole population and per state. 102 calls. The "never re-run" rule is
  read as: no committed row is replaced or re-adjudicated; a new arm may re-send a committed
  prompt under its own key.

**Before any monitor call, in this order, each ledgered:**
1. `verify_resp.py` passes on the empty cell (§L).
2. **Build** `indexes_own.json`; `verify_resp.py` re-derives every text from the committed index
   and the census rule and asserts byte identity; asserts the §C.2 counts (102 / 74 / 63 / 11 / 0
   / 16 / 12 / 41 / 6) and τ; asserts no text contains the marker or a name containing `:`.
3. **NB-6 reproduction gate.** `run_nb6`'s `lex_scores` / `emb_scores` on the committed TRUE
   texts of the 661 reproduce `results/nb6.json` (embedding **0.7484**, lexical as committed) at
   four decimals; a failure is a STOP. Then NB-6 on the V2-OWN texts, both variants, whole
   population and per state, is computed and ledgered (`AUX-RESP-L1-NB6`) **before** any monitor
   call, since it is $0 and its expectation is stated below.
4. **No leakage screen.** Every V2-OWN text is a strict subsequence of a committed index that
   passed the E1 screen at 0 of 30; removing names cannot add a value.
5. **Probe, project** (§B) against the $4 line, then **run**, then **score**.

**Registered items. The failure texts were written first, then the predictions.** Per-state
scoring is the Table 20 split: positives of one state against **the same 557 negatives**
(`nb6_composition.py`'s construction), paired per item; the whole-population row beside. The
quantity for each is D_s = AUROC_s(V2-OWN) − AUROC_s(TRUE), paired item-level interval
(`common_e1r.boot_item` on the positives-of-s ∪ negatives subpopulation), persona-clustered
beside.

*L1-P1 FAILS — supersession NOK survives the ablation.* Frozen text, appendix only:
> With the target's own attribute name and its nearest neighbours under the matcher's encoder
> removed from the superseded-names section — the only place the summary names anything — the
> smallest model's obligation discrimination on supersession-derived items moves from $X$ to $Y$,
> a paired difference of $D$ with interval $I$, which does not fall below the truthful level by
> more than the tolerance with an interval excluding zero. The reader is recovering the
> obligation from something other than the name: the superseded counts survive in the lifecycle
> totals and the per-category table, and this ablation does not remove them.

*L1-P2 FAILS — the ablation moves a state the index never named.* Frozen text:
> On $S$-derived items, which the summary only counts and never names, the ablation moves the
> smallest model's discrimination by $D$ with interval $I$, outside the tolerance. The change
> cannot come from a name the positives carried; it comes through the negatives whose names were
> removed, or through the model's response to a section that now reads "(none)" against non-zero
> counts. The per-state reading of Table 20 is not clean of the ablation on this state.

- **L1-P1.** On the 63 supersession-derived items, D_sup < −0.05 with the paired item-level
  interval excluding zero (upper bound below zero); the clustered interval beside, the weaker
  reading governs. Reading if held, appendix only, plus at most one sentence in §4.2 beside the
  lookup sentence (L452–453): *"Removing the target's own name and its nearest neighbours from the
  superseded-names section costs the smallest model $|D|$ of its supersession discrimination:
  the obligation is read off the name, as the manuscript says."*
- **L1-P2.** On the 15 expiry-derived and the 26 retraction-derived items separately, |D_s| ≤
  0.05 (the paper's own "unchanged" rule, §4.3 L507); intervals print beside and carry no bar.
  Reading if held: *"On the two states the summary only counts, the ablation changes nothing
  within tolerance: those obligations were never read from a name."* The retraction row prints
  with its census beside it (11 of 26 named, §C.2), whichever way it goes.

**What also prints, descriptive, no bar:** the whole-population NOK under V2-OWN against TRUE
(0.7339) with the paired difference and both intervals; NB-6 (embedding and lexical) on the
ablated list, whole population and per state, against its committed TRUE values (0.7484;
0.9534 / 0.4823 / 0.4053). **Expectation stated in advance:** NB-6's supersession discrimination
falls toward chance under V2-OWN, since its signal on those items is the name (§C.1: 63 of 63
named); if NB-6 survives the ablation on supersession, its remaining signal is the `(none)`
string or the neighbours below τ, and the text says which. The TRUE-REDRAW difference on the 102
changed items, whole population and per state, beside the V2-OWN − TRUE difference; **reading
rule, stated in advance:** the V2-OWN drop is reported against the redraw floor, and where
|V2-OWN − TRUE| on a state does not exceed |REDRAW − TRUE| on the same state the text says the
ablation is inside the draw noise there.

**Output cap.** One appendix table (per state and whole population: TRUE, V2-OWN, NB-6 on each)
and at most one sentence in §4.2 at L452–453. No sentence in §1 or the abstract changes.

**Projection.** 102 V2-OWN calls and 102 TRUE-REDRAW calls at the committed mini means on this
population (1,552.7 input / 24.4 output tokens per indexed call, R77 §S; $0.40 / $1.60 per 1M):
**≈ $0.13** **[est]**.

## §L2 — k-bounded and hybrid monitors (W4): what a retrieved view carries

**Question.** The manuscript's argument is that no bounded retrieved view carries the record that
forbids use, so the obligation judgment must come from the store's summary (Figure 1; §8). The
reviewer asks for the comparison the argument implies: a monitor that sees the top-*k* retrieved
items with their lifecycle metadata, alone and beside the index.

**Populations, asserted by the runner.** NOK: the committed 661 (104 PN). FOK: the FR-Bank hard
tier ∩ the 661, **307 items (35 non-ABSENT)**, which is a subset of the 661 (verified
2026-09-12: 307 of 307 inside; the R77 registration's "union of 700" was 661 in the committed cell,
`r74/x7/x7_cell.json` `n_items` 661). **Each arm is 661 calls**; one call returns both judgments.

**Lane.** As §L1: `gpt-4.1-mini`, temperature 0, seed 42, `k = 1`, JSON mode, the E1 clamp, one
retry; served identifier probed per arm. **No Haiku, no Opus.**

**Retrieval (§C.3), built and ledgered before any monitor call.** For every item: cosine top-5
over the item's store variant, all entries active or not, on the cached bank vectors and the
fresh question vector. Per retrieved entry the view carries the store's **TRUE** lifecycle
metadata — the same join the TRUE index is rendered from (`index_v2.true_lifecycle`), so the
comparison against INDEXED-TRUE is like for like — plus the entry's category, its scrubbed
attribute name (`index_v2.scrub`, the index's own vocabulary), its age in days before the
persona's pinned `t_now` (`index_v2` R3), and its text. One line per entry, rank order, exactly:

```
[1] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: gym_location | age: 42 days | text: User goes to PureGym near Piccadilly, ...
```

`lifecycle:` lists every flag that applies from {retracted, superseded, expired} in that order,
or `active` when none does. The store's own (BELIEVED) flags are **not** used under this
registration; a BELIEVED-metadata retrieved arm is October scope and is named as such.
`resp_review/l2/retrieval.json` carries, per item, the five ids with cosines, the rendered block,
and for PN items the **reach** flag: whether any `pn_members` entry is among the five, plus the
rank of the best-ranked `pn_members` entry (or none) and, descriptively, reach at k = 10.

**Prompts — new, hashed, not the frozen lineage.** `resp_review/tools/prompts_resp.py`, a new
module; `prompts_e1.py` is untouched and its digests are asserted unchanged. The variants are
minimal extensions of the frozen texts; the diff is stated and the sha256 of each string is
ledgered at build (`AUX-RESP-L2-PROMPTS`) and asserted by `verify_resp.py` against the texts
below.

`SYSTEM_RETRIEVED` = `prompts_e1.SYSTEM` with exactly one sentence replaced. Frozen: *"You will be
shown a question the user has just asked. BEFORE any retrieval is performed, give two judgments
about what the store contains."* Variant: *"You will be shown a question the user has just asked,
together with the five entries a similarity retriever returned for it from the store, each with
the lifecycle metadata the store records. Give two judgments about what the store as a whole
contains."* Every other byte of `SYSTEM` — the definitions, the two-step obligation rubric, the
worked examples, the JSON schema — is unchanged.

`USER_RETRIEVED`:
```
Five entries a similarity retriever returned from this user's memory store for the question below (top 5 by cosine similarity over every entry the store holds, active or not), each with the lifecycle metadata the store records for it. No other part of the store is shown.

```
{retrieved}
```

Question: {question}
```

`USER_HYBRID` = `prompts_e1.USER_INDEXED`'s index paragraph and fenced index, unchanged, followed
by the retrieved paragraph and fence, then the question:
```
Metadata index of this user's memory store (structure and counts only -- no fact content). Fields this memory system cannot record are marked as such; a field marked "not expressible by this backend" means the system does not track it, which is different from tracking it and finding none.

```
{index}
```

Five entries a similarity retriever returned from this store for the question below (top 5 by cosine similarity over every entry the store holds, active or not), each with the lifecycle metadata the store records for it.

```
{retrieved}
```

Question: {question}
```

**Arms.**
- **RETRIEVED** — `SYSTEM_RETRIEVED` + `USER_RETRIEVED`: the question and the five retrieved
  entries with metadata; **no index**.
- **HYBRID** — `SYSTEM_RETRIEVED` + `USER_HYBRID`: the same five entries **and** the item's
  committed TRUE index (`index_features.index_key(item, "TRUE")`).
- **INDEXED-TRUE (committed)**, **BLIND (committed)** — read, never re-elicited.

**Leakage.** None screened: both arms show entry text by design. The system text's "Do not attempt
to answer the question" stands.

**Registered items. The failure texts were written first, then the predictions.** Quantities:
paired per-item differences on the 661 (NOK) — RETRIEVED − TRUE and HYBRID − TRUE — with the
item-level interval and the clustered interval beside; the FOK rows on the 307 print
descriptively with no bar. The reach rate is a census over the 104 PN items (no sampling
interval; a Wilson interval prints beside as descriptive).

*L2-P1 FAILS — the retrieved view reaches the truthful index.* Frozen text, appendix only:
> A monitor shown the five most similar entries with their lifecycle metadata, and no summary,
> scores $R$ on obligation against $T$ under the truthful summary, a paired difference of $D$ with
> interval $I$ that does not fall below the summary by more than the tolerance. On this
> population a five-item view carries the obligation signal the summary carries; the argument
> that a bounded retrieved view cannot settle the judgment is not supported at $k = 5$ here.

*L2-P2 FAILS, adverse — the retrieved items add what the index lacks.* Frozen text:
> Adding the five retrieved entries to the truthful summary raises the smallest model's
> obligation discrimination from $T$ to $H$, a paired difference of $D$ with interval $I$ above
> the tolerance. Retrieved items carry obligation signal the summary does not: the summary names
> superseded content and only counts the other two states, and a retrieved entry flagged
> retracted or expired is a name the summary never prints.

*L2-P2 FAILS, the other direction — the retrieved items distract.* Frozen text:
> Adding the five retrieved entries to the truthful summary lowers the smallest model's obligation
> discrimination from $T$ to $H$, a paired difference of $D$ with interval $I$ below the
> tolerance. The retrieved view does not add to the summary; it takes from it.

*L2-P3 FAILS — the forbidding record is within reach.* Frozen text:
> Over every entry the store holds, a five-item similarity view contains the record that forbids
> use for $F$ of the $104$ obligations, a reach rate of $R$. The record does not rank below the
> cutoff on this population for a retriever that does not mask inactive entries; the $5\%$ figure
> the manuscript cites is FR-Bank's AV7 retrieval-pass rate under its lifecycle mask, a different
> quantity, and the premise sentence is to be restated as a mask effect.

- **L2-P1.** RETRIEVED − TRUE on NOK < −0.05 with the paired item-level interval excluding zero;
  clustered beside, weaker reading governs. Reading if held, appendix plus at most one sentence
  in §8 beside the retrieval bound (L737) or in §1 beside the premise (L131–132) — one site: *"A monitor shown the five most similar entries
  with their lifecycle metadata, and no summary, falls $|D|$ short of the summary on obligation;
  the bounded retrieved view does not carry what the summary carries."*
- **L2-P2.** |HYBRID − TRUE| ≤ 0.05 on NOK (point estimate; intervals beside). Reading if held:
  *"Given the summary, the five retrieved entries add nothing within tolerance: the summary
  supplies what retrieval cannot, and retrieval adds nothing to it."* The two failure directions
  above are distinguished by the sign of D and whether the interval excludes zero; a D outside
  tolerance with an interval including zero prints under the matching direction's text with the
  words "with an interval that includes zero" appended, and carries no verdict.
- **L2-P3.** Reach rate of forbidding records under k = 5 on the 104 PN items **< 0.20**. Reading
  if held: *"On this population a five-item similarity view contains the record that forbids use
  for $F$ of $104$ obligations ($R$), re-measuring the below-cutoff premise on the monitoring
  population."* Per-state reach (supersession / expiry / retraction) and the rank distribution
  print beside, descriptive, whichever way L2-P3 goes; the retraction reach is the row the 5%
  sentence is about.

**What also prints, descriptive:** RETRIEVED and HYBRID FOK on the 307 against TRUE 0.7003 and
blind 0.4966, paired differences with intervals; the per-state NOK split (Table 20) for both arms
against TRUE's per-state values; reach at k = 10. **Expectation stated in advance, no bar:**
RETRIEVED FOK is at or above TRUE's, since retrieved content evidences coverage directly.

**Output cap.** One appendix table (NOK whole and per state; FOK; reach) and at most one
main-text sentence at L737 (§8) or beside L131–132 (§1) — one site, not both. The Figure 1
caption and the abstract do not change on L2's account; any restatement of the 5% premise is F2
of the report and the author's ruling.

**Projection [est].** RETRIEVED: 661 calls at ≈ 770 input tokens (blind mean 480 + the retrieved
block, five entries at ≈ 16 text tokens each plus metadata and shell ≈ 290) / 26 output:
≈ $0.23. HYBRID: 661 calls at ≈ 1,843 input (1,552.7 + 290) / 26: ≈ $0.52. Question embeddings
≈ $0.0001. **L2 ≈ $0.75.**

## §L3 — The mini blind gate (W1/Q1): is the constant blind score the Step 1 gate?

**Question.** The committed mini blind obligation score is constant on the cross-model set and
takes two values on the 661 (§C.4), and the manuscript reads its indexed level against the lookup
for that reason (R96). The reviewer's explanation is the rubric's Step 1 boolean gate
(`nok_candidates_found`), which the model answers false on every blind item and which then pins
Step 2 at 0. The test: remove the gate and elicit Step 2 directly, everything else frozen.

**Population.** The committed 661; the E1 blind protocol — **one draw per unique question text,
shared across variants** (`elicit_e1.py:93-98`): **302 calls**.

**Lane.** As §L1; the blind user prompt `prompts_e1.USER_BLIND` unchanged. **No Haiku, no Opus.**

**Rubric variant — new, hashed, disclosed as a rubric variant, not the frozen lineage.**
`prompts_resp.SYSTEM_NOGATE` = `prompts_e1.SYSTEM` with the two-step decomposition removed and
nothing else. The diff, exactly:
- *"Judge this in two steps."* — removed.
- *"Step 1, nok_candidates_found: is there content on this topic in the store that has been
  superseded by a later value, retracted by the user, or has passed its date? true or false."* —
  removed.
- *"Step 2, nok: the probability, 0 to 100, that such content is present."* → *"nok: the
  probability, 0 to 100, that there is content on this topic in the store that has been
  superseded by a later value, retracted by the user, or has passed its date."* (Step 1's
  description folded into the probability line, since "such content" no longer has a referent.)
- In the two worked examples, *"nok_candidates_found = false, "* and *"nok_candidates_found =
  true, "* — removed; *"nok = 5"* and *"nok = 85"* stay.
- The JSON schema loses its field: `{"fok": <0-100>, "nok": <0-100>, "would_search": <true|false>}`.
Every other byte — the FOK line, the definition of negative obligation, the independence note,
the "do not answer" instruction — is unchanged. The sha256 of the variant is ledgered at build
(`AUX-RESP-L3-PROMPT`) and asserted against this text.

**Arm.** **BLIND-NOGATE** — `SYSTEM_NOGATE` + `USER_BLIND`; scores attached to the 661 items by
question text exactly as the committed scorer attaches the committed blind scores. The committed
BLIND rows are read beside and never re-elicited.

**Registered item. The failure text was written first.** L3-P1 has two clauses, both required:
(a) the BLIND-NOGATE `nok` takes **more than two distinct values** across the 661; (b) its NOK
AUROC's one-sample item-level interval (the ladder rule, `paper_v6.tex:1579`) **includes 0.5**.

*L3-P1 FAILS on (a) — the score stays constant without the gate.* Frozen text, appendix only,
plus at most one sentence in §4.2 at L477:
> With the detection step removed and the probability elicited directly, the smallest model's
> blind obligation score still takes $V$ distinct values across the $661$ questions ($N$ at the
> modal value). The constant was not the gate: the reviewer's explanation is not supported, and
> the smallest model's blind obligation judgment is flat under either rubric.

*L3-P1 FAILS on (b) only — the score varies and separates the classes.* Frozen text:
> With the detection step removed, the smallest model's blind obligation score takes $V$ distinct
> values and reaches $A$ with interval $I$ excluding $0.5$. The gate was pinning the score, and
> without it the blind arm carries a ranking on these questions; the manuscript's reading of the
> smallest model's indexed level against the lookup, rather than against a blind gain, is then a
> consequence of the rubric and says so.

- **L3-P1.** Both (a) and (b). Reading if held: *"Without the detection step the smallest model's
  blind obligation score takes $V$ distinct values and its discrimination, $A$ with interval $I$,
  includes chance: the constant was the gate, and removing it does not give the blind arm a
  ranking to improve on. The manuscript says so at L477."*

**What also prints, descriptive:** the distribution of BLIND-NOGATE `nok` values; the paired
INDEXED-TRUE − BLIND-NOGATE difference with its intervals, **as a descriptive figure only** — the
committed indexed arm was elicited under the gated rubric, so the pair is not a rubric-matched
gain and the text says so; the FOK values are stored and not scored.

**Output cap.** One appendix paragraph or table row and at most one sentence in §4.2 at L477.

**Projection [est].** 302 calls at ≈ 420 input (blind mean 480 less the ≈ 60 tokens the gate
occupies) / 26 output: **≈ $0.06.**

## §T — Estimators, pairing and the committed arms ($0)

`common_e1r.auroc` (Mann-Whitney, ties 0.5). Registered interval: the **item-level paired
bootstrap** (`common_e1r.boot_item`, 1,000 draws, seed 42, single-class draws discarded);
**persona-clustered** (`boot_cluster`) beside; where they disagree on a prediction the text says so
and the weaker reading governs. Tolerance ±0.05. Per-state rows (L1, L2) are the Table 20
construction: the positives of one state with all 557 negatives, paired per item; the bootstrap
resamples that subpopulation. L3's one-sample interval against 0.5 uses the ladder's
draw-and-discard rule on the 661. The reach rate is a census; a Wilson 95% interval prints
beside as descriptive. Blind and INDEXED-TRUE scores are the committed rows attached exactly as
the committed scorers attach them; no committed row is re-elicited; V2-OWN's 559 unchanged items
carry the committed TRUE score by construction (§L1).

## §B — Budget rule (frozen) and telemetry

**OpenAI key only; every monitor call `gpt-4.1-mini`; under $4 in total across L1, L2, L3 and
their probes; the Anthropic key is not touched; no Haiku, no Opus.** The one non-`gpt-4.1-mini`
call is the `text-embedding-3-small` batch for 302 question vectors (§C.3), under one cent,
confirmed by ruling (1) and disclosed under `AUX-RESP-L2-RETRIEVER` and `AUX-RESP-SPEND`.

| Lane / arm | Calls | Input / output tokens per call | Price per 1M | Expected | Source |
|---|---:|---|---|---:|---|
| L1 V2-OWN (102 changed items) | 102 | ≈ 1,553 / 24 **[est]** | $0.40 / $1.60 | $0.07 | R77 §S means on this population |
| L1 TRUE-REDRAW (descriptive noise floor; ruling (2)) | 102 | ≈ 1,553 / 24 **[est]** | $0.40 / $1.60 | $0.07 | same |
| L2 RETRIEVED | 661 | ≈ 770 / 26 **[est]** | $0.40 / $1.60 | $0.23 | blind mean 480 (ECONOMICS.md) + ≈ 290 |
| L2 HYBRID | 661 | ≈ 1,843 / 26 **[est]** | $0.40 / $1.60 | $0.52 | indexed mean + ≈ 290 |
| L2 question embeddings (`text-embedding-3-small`; ruling (1), the one non-mini call) | 302 inputs | ≈ 15 in each | $0.02 | < $0.001 | §C.3 |
| L3 BLIND-NOGATE | 302 | ≈ 420 / 26 **[est]** | $0.40 / $1.60 | $0.06 | blind mean less the gate |
| Identifier probes (E1.7) | 5 | as the arm | — | < $0.01 | one per arm |
| **Total** | **1,833 calls** + 302 embedding inputs | | | **≈ $0.96** (×1.3 **$1.25**) | under the $4 rule |

`probe` and `project` (the RESP runner's equivalents of `run_side.py`'s) run and report before
any submission; the run stops submitting at $4 with a printed reason.

## §L — Ledger keys reserved, verifier, deviations

`AUX-RESP-L1-CENSUS` (T(q) sizes, changed / emptied / neighbour counts by label, state and
variant — the §C.2 table), `-L1-TAU` (0.503637 and the null quantiles), `-L1-LOCK` (242 / 242
section identity; every V2-OWN text re-derived), `-L1-NB6-GATE` (0.7484 reproduced),
`-L1-NB6` (NB-6 embedding and lexical on V2-OWN, whole and per state, beside the committed
TRUE values), `-L1-MINI` (TRUE and V2-OWN NOK AUROC whole and per state; D with both intervals;
L1-P1 and L1-P2 verdicts; frozen text printed with its numbers), `-L1-REDRAW` (REDRAW − TRUE on the 102
changed items, whole and per state, both intervals), `-L2-RETRIEVER` (the retriever spec; 302 vectors, 187 cached reproduced at
≥ 0.99, sha256 of the matrix), `-L2-REACH` (reach at k = 5 overall and per state, Wilson beside,
rank distribution, reach at k = 10; L2-P3 verdict), `-L2-PROMPTS` (sha256 of `SYSTEM_RETRIEVED`,
`USER_RETRIEVED`, `USER_HYBRID`; `prompts_e1` digests unchanged), `-L2-MINI-NOK` (RETRIEVED, HYBRID,
TRUE, blind; the two paired differences with both intervals; per state; L2-P1, L2-P2 verdicts),
`-L2-MINI-FOK` (descriptive), `-L3-PROMPT` (sha256 of `SYSTEM_NOGATE`; the diff as listed),
`-L3-MINI` (value distribution, distinct count, AUROC with its one-sample interval, L3-P1 verdict;
the descriptive indexed − nogate difference), `-PAPER-Q4` (§C.5), `-SPEND`, `-BUDGETRULE`. Every
key is written; a key that cannot be computed carries a dash and its reason.

`resp_review/tools/verify_resp.py` asserts before any artifact exists: the `prompts_e1` digests;
sha256 pins on `index_v2.py`, `index_features.py`, `common_e1r.py`, `run_nb6.py`,
`nb6_composition.py`, `e0_common.py`, `lifecycle_bank.py`; the §C.2 section lock (242 / 242) and
census (τ and every count in the table); the persona-keyed own-name census of §C.1 (74 / 63 / 11
/ 0 under TRUE); the populations (661 / 104; 307 / 35; 302 distinct questions; 187 cached
vectors); the committed blind value census of §C.4; the §C.5 marker fractions; that
`prompts_resp.py`, once it exists, carries exactly the texts of §L2 and §L3 (hashes ledgered).
Once artifacts exist: every V2-OWN text re-derived and byte-identical; the retrieval artifact
re-derived from the pinned vectors; NB-6 gate and NB-6 on V2-OWN reproduced; every score, interval
and verdict re-derived from `rows_resp.jsonl` and the committed rows with the committed
estimators; spend under $4; every §L key present.

`resp_review/DEVIATIONS_RESP.md`, from **D-RESP-1**; nothing yet.

## §STOP — conditions, last, including the budget rule

- Any monitor or embedding call before this file is frozen by the author's commit and GO is
  given.
- `verify_resp.py` absent or failing when the first V2-OWN text, retrieval artifact or prompt
  variant is about to be written, or before the first monitor call.
- The section renderer lock failing on any of the 242 keys; any V2-OWN text differing from its
  committed TRUE text anywhere before the section header; any V2-OWN text containing the marker
  or a name containing `:`; the census counts of §C.2 not reproduced at build.
- The NB-6 reproduction gate (0.7484 at four decimals on the committed TRUE texts) failing.
- Any cached question vector reproducing its fresh vector below cosine 0.99; any bank entry
  without a cached vector; any retrieval computed with a lifecycle filter, BM25, category
  forcing or distillation applied.
- `prompts_e1.py` changing by one byte; `prompts_resp.py` differing from the texts of §L2 and §L3;
  a variant prompt used on an arm it is not registered for.
- Any committed blind or INDEXED-TRUE row re-elicited in place of being read; the TRUE-REDRAW arm
  written into the TRUE arm's cache key; V2-OWN's unchanged items elicited.
- Served identifier not containing `gpt-4.1-mini` on any probe (E1.7); any call on the Anthropic
  key; any Haiku or Opus call; any model other than `gpt-4.1-mini` on a monitor call.
- Spend reaching $4 with a cell unscored — the run stops and reports.
- Any number printed without a key in `NUMBERS_RESP.md`; any reading written after its numbers
  exist; any headline number in the abstract or Section 1 changed on L1's, L2's or L3's account;
  more than one main-text sentence per lane.
- The frozen lineage — `prompts_e1` digests, `index_v2.render`, `index_features.parse`,
  `common_e1r`, `run_nb6`'s scorers, `lifecycle_bank.cosine_search_all` — changing by one byte.

---

## Registration mechanics

One Table 24 row per lane (L1, L2, L3), added with this file's freeze-commit hash after the freeze
commit exists. Outcome cells start "pending" and update only per the frozen text above; L1's row
carries L1-P1 and L1-P2; L2's carries L2-P1, L2-P2 and L2-P3; L3's carries L3-P1. The descriptive
rows (whole-population V2-OWN, NB-6 on the ablated list, TRUE-REDRAW, FOK under retrieval, reach
per state, the nogate distribution) carry no verdict. Amendment 1 to `ADDENDUM_SIDE.md` (the S1
and S2-U main-text placements) and D-E1R-10 (the own-name census) are drafted in
`reviews/RESP_REG_REPORT.md` Appendices B and C for the author to freeze in the same sitting;
neither is part of this registration's predictions.
