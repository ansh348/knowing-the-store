# NUMBERS_RESP — ledger for the review-response lanes L1, L2, L3

Registration: `registrations/ADDENDUM_RESP.md` (frozen at `17e6328`, R98; baseline `2a943d7`). Every
number printed for L1, L2 or L3 enters the manuscript through a key in this file and no other way.
Keys are reserved in the registration's §L. Entries are dated.

**State of this file.** Phase B (`reviews/RESP_REG_REPORT.md` §7) started 2026-09-13 on the
author's GO, after the freeze (`17e6328`) and after the DS registration froze at `a5a2036` (R100).
Steps 1–6 committed one at a time on 2026-09-13 (§2–§5 below); `tools/verify_resp.py` passes with
every check A–G; `DEVIATIONS_RESP.md` holds nothing. **Verdicts: L1-P1 HOLDS; L1-P2 FAILS (retraction);
L2-P1 FAILS; L2-P2 FAILS, adverse direction (retrieved items add what the index lacks); L2-P3 FAILS
(reach 0.5192); L3-P1 FAILS on (a) (two values). Billed $0.9415 of the $4 rule.** `AUX-RESP-PAPER-Q4` (§1
below) was written earlier under the R97 paper round (CLAIMS.md R97 block, entry 8) so that R97
could print it. Every other §L key lands with its step below; a key not yet computed is absent
here, never a placeholder. Steps are dated and committed one at a time.

---

## 1. AUX-RESP-PAPER-Q4 — the inexpressibility marker's share of the two structureless indexes (written 2026-09-13; recomputed from the committed file, no model call)

Source: `e1_metamemory/indexes_v2.json` (sha256 `a54152bf3698…`), keys `mem0:<persona>:FULL:<prov>` (37
personas) and `amem:<persona>:FULL:<prov>` (40 personas), the texts the indexed monitor read.
Tokeniser: `tiktoken` `o200k_base`; the marker `not expressible by this backend` is 6 tokens.
Method: per index, the line count, the o200k token count, the number of marker occurrences and
the lines carrying one; marker tokens = occurrences × 6; the fraction = marker tokens / index
tokens. Every index of a (backend, provenance) pair has the same counts, so one row per pair.
Equal to `registrations/ADDENDUM_RESP.md` §C.5 (computed 2026-09-12) to the token.

| Key / row | indexes | lines | o200k tokens | marker occurrences | marker lines | marker tokens | fraction |
|---|---:|---:|---:|---:|---|---|---:|
| **AUX-RESP-PAPER-Q4** Mem0, TRUE | 37 | 31 | 216 | 3 | 3 of 31 | 18 of 216 | 8.3% |
| **AUX-RESP-PAPER-Q4** A-MEM, TRUE | 40 | 31 | 216 | 3 | 3 of 31 | 18 of 216 | 8.3% |
| **AUX-RESP-PAPER-Q4** Mem0, BELIEVED | 37 | 31 | 232 | 7 | 7 of 31 | 42 of 232 | 18.1% |
| **AUX-RESP-PAPER-Q4** A-MEM, BELIEVED | 40 | 31 | 236 | 8 | 8 of 31 | 48 of 236 | 20.3% |

**What the paper prints (Appendix F.7, R97 entry 5e).** Under TRUE the marker occupies 3 of 31
lines and 18 of 216 tokens (8.3%) on both backends; under BELIEVED 7 lines and 18.1% of tokens on
Mem0, 8 lines and 20.3% on A-MEM. The persona named by §C.5 as the one of median joint size is
`leila`; its two TRUE indexes print verbatim. They are reproduced below byte for byte so that every
number inside them (entry counts, lifecycle totals, ages, age bands) has a ledger row; each is 31
lines and 216 o200k tokens.

`mem0:leila:FULL:TRUE` (sha256 `6dc20dbd66ae608ef8943c1510374688e15444b0fd8a318f84fd46cf7a6cdf48`):

```
MEMORY STORE INDEX  (metadata only; no fact content)
entries in this store: 259
Ages below are in days before the store's pinned current time.

LIFECYCLE TOTALS
  active                259
  superseded            0
  retracted             0
  expired               1
  supersession events   0

PER-CATEGORY BREAKDOWN
  not expressible by this backend

RECENCY
  newest entry          1
  oldest entry          550
  median entry age      291

AGE DISTRIBUTION  (entries by age band)
  0-30                  10
  31-90                 47
  91-180                32
  181-365               71
  over 365              99

ATTRIBUTE NAMES BY CATEGORY  (value-scrubbed)
  not expressible by this backend

ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT  (value-scrubbed)
  not expressible by this backend
```

`amem:leila:FULL:TRUE` (sha256 `9cef7ab469a0c5025c016bf2fe079900c0a736bb57b087f6c189d9095a775857`):

```
MEMORY STORE INDEX  (metadata only; no fact content)
entries in this store: 272
Ages below are in days before the store's pinned current time.

LIFECYCLE TOTALS
  active                271
  superseded            1
  retracted             0
  expired               2
  supersession events   2

PER-CATEGORY BREAKDOWN
  not expressible by this backend

RECENCY
  newest entry          1
  oldest entry          550
  median entry age      298

AGE DISTRIBUTION  (entries by age band)
  0-30                  14
  31-90                 35
  91-180                24
  181-365               82
  over 365              117

ATTRIBUTE NAMES BY CATEGORY  (value-scrubbed)
  not expressible by this backend

ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT  (value-scrubbed)
  not expressible by this backend
```

Numbers inside the two texts, for the trace: Mem0 — entries 259; active 259, superseded 0,
retracted 0, expired 1, supersession events 0; newest 1, oldest 550, median age 291; bands 0–30: 10,
31–90: 47, 91–180: 32, 181–365: 71, over 365: 99. A-MEM — entries 272; active 271, superseded 1,
retracted 0, expired 2, supersession events 2; newest 1, oldest 550, median age 298; bands 0–30: 14,
31–90: 35, 91–180: 24, 181–365: 82, over 365: 117.

---

## 2. Step 2 — the V2-OWN indexes and NB-6 on them (written 2026-09-13; no model call)

### AUX-RESP-L1-LOCK — section renderer lock

Re-rendering the superseded-names section of every committed TRUE index of the 661 (242 keys) from
its parsed names through `name_block`'s rule (`index_v3._name_block`: sorted set, cap 15, wrap 150,
indents `"  "` / `"    "`, `(none)` when empty) reproduces the committed text byte for byte on
**242 of 242** keys, and the section is the tail of every text. Every V2-OWN text of
`l1/indexes_own.json` is the committed text up to the section header, byte-identical, followed by
the section re-rendered over the remaining names; `verify_resp.py` check E re-derives all 661.
Marker absent from every text; no emitted name contains `:`.

### AUX-RESP-L1-TAU — the neighbour threshold

Under NB-6's encoder (`sentence-transformers/all-MiniLM-L6-v2`, local), over the **35** distinct
real names of the 242 sections (underscores → spaces), the **577** pairs of distinct names sharing no
content token form the null: median 0.142, p90 0.313, p95 0.356,
**p99 = τ = 0.503637**, max 0.649. (The registration's §C.2 prose printed the median as
0.145; the recomputation of the same script gives 0.142; p90 / p95 / p99 / max agree to
three decimals and τ to six, so the null set is the same and the 0.145 is a transcription in the
prose. Disclosed, not repaired; no verdict reads the median.) 47 distinct within-section
pairs; six at or above τ (workspace|workspace_location, placement_location|placement_status,
employer|job_title, activity|hobby, job_responsibility|job_title, current_neighborhood|current_residence).
Mean names per key: 1.785 counting `(none)` as one name (the committed parser's behaviour;
NB-6's 1.7474 per item likewise), 1.525 counting it as none.

### AUX-RESP-L1-CENSUS — the ablation census at τ (§C.2 reproduced at build)

| | items | changed under V2-OWN | of which section emptied to `(none)` |
|---|---:|---:|---:|
| all | 661 | **102** | 41 |
| PRESENT-NEGATIVE | 104 | **74** | 34 |
| — supersession-derived | 63 | **63** | 30 |
| — retraction-derived | 26 | **11** | 4 |
| — expiry-derived | 15 | **0** | 0 |
| PRESENT | 174 | 16 | — |
| ABSENT (natural-absent changed: 0) | 383 | 12 | — |
| by variant FULL / CAT-ABLATED / SLOT-ABLATED | 323 / 176 / 162 | 46 / 16 / 40 | — |
| items where a neighbour (not an own name) is removed | — | 6 | — |

|T(q)| over the 661: 0 for 145, 1 for 219, 2 for 152, 3 for 83, 4 for 42, ≥ 5 for 20.
**559 items are byte-identical to their committed TRUE text** and carry the committed TRUE score
under V2-OWN; 63 keys / 195 items print `(none)` under TRUE.

### AUX-RESP-L1-NB6-GATE — NB-6 reproduction on the committed TRUE texts

`run_nb6.emb_scores` / `lex_scores` on the committed TRUE texts of the 661 through
`index_features.parse`: embedding **0.7484** (committed 0.7484), lexical
**0.5738** (committed 0.5738); per state (embedding) supersession
0.9534 / expiry 0.4823 / retraction 0.4053
(committed 0.9534 / 0.4823 / 0.4053). **Gate PASS at four decimals.**

### AUX-RESP-L1-NB6 — NB-6 on the V2-OWN list (computed before any monitor call)

Per-state rows: positives of one state against the same 557 negatives (`nb6_composition.py`'s
construction). `(none)` scored as a name, as committed.

| NB-6 variant | population | TRUE (committed texts) | V2-OWN | difference |
|---|---|---:|---:|---:|
| embedding | all | 0.7484 | 0.4913 | -0.2571 |
| embedding | supersession | 0.9534 | 0.5108 | -0.4426 |
| embedding | expiry | 0.4823 | 0.4887 | +0.0065 |
| embedding | retraction | 0.4053 | 0.4455 | +0.0403 |
| lexical | all | 0.5738 | 0.4991 | -0.0747 |
| lexical | supersession | 0.6241 | 0.4991 | -0.1250 |
| lexical | expiry | 0.4964 | 0.4991 | +0.0027 |
| lexical | retraction | 0.4964 | 0.4991 | +0.0027 |

Mean names per item: TRUE 1.7474, V2-OWN 1.6051.
**Reading under the expectation stated in advance (§L1):** NB-6's supersession discrimination under
V2-OWN is 0.5108 (embedding), against 0.9534 under TRUE — toward chance, as expected: its signal on those items was the name.
The lexical variant prints beside it (0.4991 against 0.6241); τ does not close the lexical
variant (registration §C.2). Artifact: `l1/nb6_own.json` (per-item scores under both texts).

---

## 3. Step 3 — the prompt variants (written 2026-09-13; no model call)

### AUX-RESP-L2-PROMPTS — the L2 texts, hashed (`tools/prompts_resp.py`)

`prompts_e1.py` untouched: file digest `337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84`, texts digest `35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2` (both as pinned). Each variant is constructed in the module from the frozen strings by the edits §L2 lists, so the diff is a property of the file (verify check D re-derives it).

| text | construction | sha256 |
|---|---|---|
| `SYSTEM_RETRIEVED` | `prompts_e1.SYSTEM` with exactly one passage replaced ("You will be shown a question the user has just asked. BEFORE any retrieval is performed, give two judgments about what the store contains." → "You will be shown a question the user has just asked, together with the five entries a similarity retriever returned for it from the store, each with the lifecycle metadata the store records. Give two judgments about what the store as a whole contains."); every other byte unchanged | `602b9431b3fca99b3b1c987fd9a760d8433dd7c5c6ca929b077f92b63d68feca` |
| `USER_RETRIEVED` | the §L2 text verbatim (retrieved paragraph, fenced `{retrieved}`, question) | `d9031f6f5bedd7a67401c5c6d6e6f56cac71a1983cfad0d0299bdd61026653cc` |
| `USER_HYBRID` | `prompts_e1.USER_INDEXED`'s paragraph and fenced index unchanged, then the retrieved paragraph and fence, then the question | `b29d1e476c260279787c46c940e9b6af68b491dd0fa57486a040e8a222a7f552` |

### AUX-RESP-L3-PROMPT — the rubric variant, hashed

`SYSTEM_NOGATE` = `prompts_e1.SYSTEM` with the two-step decomposition removed and nothing else: " Judge this in two steps." removed; the Step 1 paragraph removed (with its preceding blank line); "  Step 2, nok: the probability, 0 to 100, that such content is present." → "  nok: the probability, 0 to 100, that there is content on this topic in the store that has been superseded by a later value, retracted by the user, or has passed its date."; the two example clauses "nok_candidates_found = false, " / "nok_candidates_found = true, " removed ("nok = 5" and "nok = 85" stay); the JSON schema loses its field: `{"fok": <0-100>, "nok": <0-100>, "would_search": <true|false>}`. Every other byte — the FOK line, the definition of negative obligation, the independence note, the "do not answer" instruction — unchanged (unified diff: 5 hunks, exactly those). sha256 `1ad8621c1953805d4ce71d762cbfcd6061a17b345d41b5de9fb2b28080ea69f2`.

---

## 4. Step 4 — the retriever and the reach row (written 2026-09-13; one embedding call, no chat call)

### AUX-RESP-L2-RETRIEVER — the retriever spec and the question vectors

Retriever: `LifecycleBank.cosine_search_all` (`lifecycle_bank.py:402-414`), cosine over **every entry the
item's store variant holds, active or not** (FULL; CAT-ABLATED minus the persona's planned categories;
SLOT-ABLATED minus `slot_ablations[persona:qid]` — the entry sets `index_v2.main` renders the committed
index from), on the bank's cached `text-embedding-3-small` vectors; top 10 taken, **top 5 used**. No
lifecycle mask, BM25, category forcing, multi-hop or distillation. Per retrieved entry the block carries
the store's **TRUE** lifecycle flags (`index_v2.true_lifecycle`, the join the TRUE index is rendered
from), category, scrubbed attribute, age in days before the persona's pinned `t_now`, and the text, one
line per entry in rank order (`retrieval.json` `meta.line_format`).

**Question vectors (the one non-`gpt-4.1-mini` call, ruling (1)).** All 302 distinct question texts
embedded fresh with `text-embedding-3-small` in one call: 3297 input tokens,
**$0.000066** (2026-09-13T13:40:36). The **187** LifecycleBench questions with a cached vector
(`artifacts/theory/query_emb_cache.npz`) reproduce the fresh ones at cosine ≥ 0.99 each: minimum
0.998341, 0 below 0.99 — **check PASS**. Matrix `l2/question_emb.npz`,
sha256 `341354661e40b7f0508d11f7a7274833064a600c02c7155310f237ae88d023cf`. Artifact: `l2/retrieval.json` (per item the ten ids with cosines, the
five used, the rendered block; per PN item the reach flags and best rank); `verify_resp.py` check F
re-derives every top-10 from the pinned vectors and every block byte for byte.

### AUX-RESP-L2-REACH — reach of the forbidding record (the L2 baseline row; DS's ALWAYS row)

Census over the 104 PN items (no sampling interval; Wilson 95% beside, descriptive).

| | reached at k = 5 | of | rate | reached at k = 10 | rate |
|---|---:|---:|---:|---:|---:|
| **all PN** | **54** | 104 | **0.5192** (Wilson [0.4242, 0.6128]) | 74 | 0.7115 |
| supersession-derived | 22 | 63 | 0.3492 | 37 | 0.5873 |
| retraction-derived | 20 | 26 | 0.7692 | 25 | 0.9615 |
| expiry-derived | 12 | 15 | 0.8000 | 12 | 0.8000 |

Best rank of a `pn_members` entry within the top 10 (None = not in the ten): {'1': 17, '10': 4, '2': 16, '3': 15, '4': 3, '5': 3, '6': 6, '7': 2, '8': 7, '9': 1, 'None': 30}.
Flags printed on the reached records at k = 5: {'superseded': 36, 'active': 39, 'expired': 16, 'retracted': 8} (D-DS-1 of the DS registration: 22 forbidding
records carry no TRUE flag and print `active` when retrieved).

**L2-P3 (reach at k = 5 < 0.20): 0.5192 → FAILS.** Frozen text, printed with its numbers:
> Over every entry the store holds, a five-item similarity view contains the record that forbids use for 54 of the 104 obligations, a reach rate of 0.5192. The record does not rank below the cutoff on this population for a retriever that does not mask inactive entries; the 5% figure the manuscript cites is FR-Bank's AV7 retrieval-pass rate under its lifecycle mask, a different quantity, and the premise sentence is to be restated as a mask effect.

The retraction reach (20 of 26) is the row the 5% sentence is about. Rendered blocks and the reach
flags are DS's ALWAYS view and row (`registrations/ADDENDUM_DS.md` §C.1).

---

## 5. Steps 5–6 — the mini lanes, scored (written 2026-09-13)

Lane: `gpt-4.1-mini` (served identifier probed per arm, `run/probes_resp.json`), temperature 0, seed 42,
k = 1, max_tokens 200, JSON mode, the E1 clamp, one retry on a parse failure; rows `run/rows_resp.jsonl`
(V2-OWN 102, TRUE-REDRAW 102, RETRIEVED 661, HYBRID 661, BLIND-NOGATE 302); elicitation failures {'V2-OWN': 0, 'TRUE-REDRAW': 0, 'RETRIEVED': 0, 'HYBRID': 0, 'BLIND-NOGATE': 0}. Estimators: `common_e1r.auroc`
(Mann-Whitney, ties 0.5), `boot_item` (1,000 draws, seed 42, single-class draws discarded), `boot_cluster`
beside; the weaker reading governs where they disagree. Tolerance ±0.05. Per-state rows: positives of
one state against the same 557 negatives.

### AUX-RESP-L1-MINI — V2-OWN against the committed TRUE rows (NOK)

| row | n / positives | TRUE (committed) | arm | D | item-level 95% | persona-clustered 95% |
|---|---|---:|---:|---:|---|---|
| whole population | 661 / 104 | 0.7339 | 0.5016 | -0.2323 | [-0.2890, -0.1753] | [-0.3054, -0.1540] |
| supersession-derived (63) | 620 / 63 | 0.8572 | 0.5310 | -0.3262 | [-0.3991, -0.2548] | [-0.4327, -0.2167] |
| expiry-derived (15) | 572 / 15 | 0.5110 | 0.5136 | +0.0026 | [-0.0028, +0.0079] | [-0.0041, +0.0103] |
| retraction-derived (26) | 583 / 26 | 0.5638 | 0.4234 | -0.1404 | [-0.2569, -0.0508] | [-0.3305, -0.0028] |

**L1-P1** (D_sup < −0.05, item-level interval excluding zero; clustered beside, weaker governs): item-level reading holds, persona-clustered reading holds → **HOLDS**. Frozen text with its numbers:
> Removing the target's own name and its nearest neighbours from the superseded-names section costs the smallest model 0.3262 of its supersession discrimination (0.8572 to 0.5310, interval [-0.3991, -0.2548]; persona-clustered [-0.4327, -0.2167]): the obligation is read off the name, as the manuscript says.

**L1-P2** (|D_exp| ≤ 0.05 and |D_ret| ≤ 0.05): expiry +0.0026, retraction -0.1404 → **FAILS**. Frozen text with its numbers:
> On retraction-derived items, which the summary only counts and never names, the ablation moves the smallest model's discrimination by -0.1404 with interval [-0.2569, -0.0508] (persona-clustered [-0.3305, -0.0028]), outside the tolerance. The change cannot come from a name the positives carried; it comes through the negatives whose names were removed, or through the model's response to a section that now reads "(none)" against non-zero counts. The per-state reading of Table 20 is not clean of the ablation on this state. (Retraction: 11 of 26 named in the section, §C.2.)

NB-6 on the ablated list is `AUX-RESP-L1-NB6` (§2).

### AUX-RESP-L1-REDRAW — the draw-noise floor on the 102 changed items (descriptive)

REDRAW − TRUE and V2-OWN − TRUE on the same 102 items (per state: positives of the state among the 102 against the 28 changed negatives).

| population | n / positives | REDRAW − TRUE (item-level; clustered) | V2-OWN − TRUE on the same items | inside the draw noise |
|---|---|---|---|---|
| all | 102 / 74 | +0.0179 [-0.0117, +0.0523]; [-0.0168, +0.0545] | -0.3250 [-0.4438, -0.2108] | no |
| supersession | 91 / 63 | +0.0170 [-0.0127, +0.0541]; [-0.0157, +0.0459] | -0.3271 [-0.4383, -0.2071] | no |
| expiry | 28 / 0 | — | — | no positives of this state among the 102 changed items |
| retraction | 39 / 11 | +0.0227 [-0.0272, +0.0877]; [-0.0367, +0.1053] | -0.3133 [-0.5336, -0.1129] | no |

**Reading rule (§L1):** where |V2-OWN − TRUE| on a state does not exceed |REDRAW − TRUE| on the same state, the ablation is inside the draw noise there: all outside, supersession outside, retraction outside.

### AUX-RESP-L2-MINI-NOK — RETRIEVED and HYBRID against the committed TRUE rows (NOK, 661)

| row | n / positives | TRUE (committed) | arm | D | item-level 95% | persona-clustered 95% |
|---|---|---:|---:|---:|---|---|
| RETRIEVED, whole | 661 / 104 | 0.7339 | 0.6851 | -0.0488 | [-0.1274, +0.0285] | [-0.1454, +0.0389] |
| RETRIEVED, supersession | 620 / 63 | 0.8572 | 0.6853 | -0.1719 | [-0.2641, -0.0734] | [-0.2764, -0.0682] |
| RETRIEVED, expiry | 572 / 15 | 0.5110 | 0.7474 | +0.2364 | [+0.1053, +0.3829] | [+0.0645, +0.4037] |
| RETRIEVED, retraction | 583 / 26 | 0.5638 | 0.6487 | +0.0850 | [-0.0682, +0.2235] | [-0.1435, +0.2764] |
| HYBRID, whole | 661 / 104 | 0.7339 | 0.8303 | +0.0964 | [+0.0415, +0.1554] | [+0.0227, +0.1635] |
| HYBRID, supersession | 620 / 63 | 0.8572 | 0.9044 | +0.0472 | [-0.0337, +0.1206] | [-0.0510, +0.1348] |
| HYBRID, expiry | 572 / 15 | 0.5110 | 0.6858 | +0.1747 | [+0.0320, +0.3287] | [+0.0195, +0.3335] |
| HYBRID, retraction | 583 / 26 | 0.5638 | 0.7342 | +0.1704 | [+0.0430, +0.2926] | [-0.0089, +0.3471] |

Committed blind NOK on the 661: 0.4946 (descriptive; anchors no gain, R96).

**L2-P1** (RETRIEVED − TRUE < −0.05, item-level interval excluding zero; clustered beside, weaker governs): item-level reading fails, persona-clustered reading fails → **FAILS**. Frozen text with its numbers:
> A monitor shown the five most similar entries with their lifecycle metadata, and no summary, scores 0.6851 on obligation against 0.7339 under the truthful summary, a paired difference of -0.0488 with interval [-0.1274, +0.0285] (persona-clustered [-0.1454, +0.0389]) that does not fall below the summary by more than the tolerance. On this population a five-item view carries the obligation signal the summary carries; the argument that a bounded retrieved view cannot settle the judgment is not supported at k = 5 here.

**L2-P2** (|HYBRID − TRUE| ≤ 0.05, point estimate): → **FAILS**. Frozen text with its numbers:
> Adding the five retrieved entries to the truthful summary raises the smallest model's obligation discrimination from 0.7339 to 0.8303, a paired difference of +0.0964 with interval [+0.0415, +0.1554] (persona-clustered [+0.0227, +0.1635]) above the tolerance. Retrieved items carry obligation signal the summary does not: the summary names superseded content and only counts the other two states, and a retrieved entry flagged retracted or expired is a name the summary never prints.

**L2-P3** (reach at k = 5 < 0.20): 54 of 104 = 0.5192 → **FAILS** (`AUX-RESP-L2-REACH`, §4, frozen text printed there).

### AUX-RESP-L2-MINI-FOK — the FOK rows on the 307 (descriptive, no bar)

| arm | vs TRUE (0.7003): arm, D, item-level, clustered | vs blind (0.4966): D, item-level, clustered |
|---|---|---|
| RETRIEVED | 0.7870, +0.0867, [-0.0261, +0.1908], [+0.0041, +0.1683] | +0.2904, [+0.1826, +0.3823], [+0.1976, +0.3789] |
| HYBRID | 0.8241, +0.1238, [+0.0206, +0.2265], [+0.0471, +0.1994] | +0.3275, [+0.2240, +0.4244], [+0.2401, +0.4124] |

Expectation stated in advance (§L2): RETRIEVED FOK at or above TRUE's — as expected (+0.0867).

### AUX-RESP-L3-MINI — BLIND-NOGATE

Scores attached to the 661 items by question text (302 questions, 661 items). Value distribution of `nok`: {'0.0': 604, '0.1': 57} — **2 distinct values**, modal value 0.0 on 604 items. `fok` distribution (stored, not scored): {'0.0': 2, '0.1': 215, '0.2': 254, '0.3': 3, '0.4': 179, '0.7': 8}.
One-sample AUROC (the ladder rule, item-level, 1,000 draws, seed 42): **0.4888** [0.4646, 0.5165], includes 0.50: True.

**L3-P1** ((a) more than two distinct values: False; (b) interval includes 0.5: True) → **FAILS**. Frozen text with its numbers:
> With the detection step removed and the probability elicited directly, the smallest model's blind obligation score still takes 2 distinct values across the 661 questions (604 at the modal value). The constant was not the gate: the reviewer's explanation is not supported, and the smallest model's blind obligation judgment is flat under either rubric.

Descriptive only (not a rubric-matched gain — the committed indexed arm was elicited under the gated rubric): INDEXED-TRUE − BLIND-NOGATE = +0.2451 [+0.1773, +0.3117]; persona-clustered [+0.1432, +0.3445] (INDEXED-TRUE 0.7339).

### AUX-RESP-SPEND and AUX-RESP-BUDGETRULE

Billed on the OpenAI key, from response usage at $0.40 / $1.60 per 1M (`gpt-4.1-mini`) and $0.02 per 1M (`text-embedding-3-small`): embedding $0.000066, identifier probes $0.0028, run $0.9386 — **total $0.9415**, under the $4 rule (yes). Nothing on the Anthropic key; no Haiku, no Opus; no monitor call on any model other than `gpt-4.1-mini`. Projection before launch: `run/projection_resp.json`.

---

## 6. AUX-RESP-PRINTED — the main-text forms (written 2026-09-13, R101; no model call)

The L1-P1 held reading as `paper_v9.tex` §4.2 prints it (the frozen §L1 sentence with $|D|$ filled, the levels and both
intervals inside the parenthesis in the manuscript's idiom):

> Removing the target's own name and its nearest neighbours from the superseded-names section costs the smallest model $0.3262$ of its supersession discrimination ($0.8572$ to $0.5310$; interval $[-0.3991,-0.2548]$, and $[-0.4327,-0.2167]$ with questions grouped by user profile): the obligation is read off the name, as the manuscript says.

The one L2 main-text sentence (descriptive; the L2 predictions failed and their frozen texts print in the appendix), every number
`AUX-RESP-L2-MINI-NOK`:

> A monitor reading the five retrieved items with their lifecycle tags, and no summary, reaches $0.6851$ on obligation against the summary's $0.7339$, within tolerance; the two together reach $0.8303$, the gain on the states the summary only counts (Appendix~\ref{app:resp}).

The L3 clause on the §4.2 blind-arm sentence: "with or without the rubric's detection step" (`AUX-RESP-L3-MINI`: two values).

---

## 7. Amendment 1 — the retrieved view under FR-Bank's own marks; Haiku 4.5 at k = 5 on the hybrid, retrieved-view and own-name monitors (descriptive; written 2026-09-14, R108)

Registration `registrations/ADDENDUM_RESP_AMENDMENT_1.md`, frozen sha256 `40b4c4084f89e41d38ff1b558c1db033bdcec88a5787a3feada9fe94ad321c9d` before the first call
(recorded here on 2026-09-14 before any call of the amendment; copy in `iclr2027_monitoring_submission/ARTIFACT/registrations/`). **Descriptive: no bar, no prediction,
no verdict; L1-P1, L1-P2, L2-P1 to L2-P3 stand.** Sources: `run/lock_amend1.json`, `l2/retrieval_believed.json`, `run/probes_amend1.json`, `run/projection_amend1.json`,
`run/rows_amend1_mini.jsonl`, `run/batch_amend1_*.json`, `run/rows_amend1_H45_*.jsonl`, `run/scores_amend1.json` (`tools/amend1_resp.py`). Nothing registered is written. The subsections below are appended by `amend1_resp.py score`.

### AUX-RESP-A1-LOCK, AUX-RESP-A1-TAGS — the believed blocks and the tag census (no call)

Registration sha256 holds; prompts_resp digests as AUX-RESP-L2-PROMPTS; prompts_e1 as pinned. The same `top5_ids` as `l2/retrieval.json`, re-rendered with FR-Bank's own marks (`l2/retrieval_believed.json`). Of the 3305 rendered lines, 1273 change tag between the join and the store's marks (565 of 661 views change at least one line). The store's non-active mark against the join's, over lines: tp 188, fp 1201, fn 29, tn 1887; precision 0.1353, recall 0.8664. Over the forbidding records in view (the 104 obligations' pn_members among the five): tp 47, fp 23, fn 13, tn 16; precision 0.6714, recall 0.7833.

### AUX-RESP-A1-PROBE, AUX-RESP-A1-BELIEVED — RETRIEVED-BELIEVED (gpt-4.1-mini, 661, k = 1)

Probe served `gpt-4.1-mini-2025-04-14` (754 in / 26 out). Rows 661, failures 0; billed $0.2310. Paired against the recorded RETRIEVED row (ground-truth tags) and against the committed INDEXED-TRUE row; item-level and persona-clustered paired bootstrap (1,000 draws, seed 42).

| row | n / positives | base | RETRIEVED-BELIEVED | D | item-level 95% | persona-clustered 95% |
|---|---|---:|---:|---:|---|---|
| vs RETRIEVED (join tags), all | 661 / 104 | 0.6851 | 0.8144 | +0.1292 | [+0.0666, +0.1826] | [+0.0606, +0.2060] |
| vs RETRIEVED (join tags), supersession | 620 / 63 | 0.6853 | 0.8189 | +0.1336 | [+0.0615, +0.1987] | [+0.0500, +0.2251] |
| vs RETRIEVED (join tags), expiry | 572 / 15 | 0.7474 | 0.7866 | +0.0392 | [-0.0784, +0.1823] | [-0.1222, +0.1748] |
| vs RETRIEVED (join tags), retraction | 583 / 26 | 0.6487 | 0.8194 | +0.1706 | [+0.0700, +0.2792] | [+0.0290, +0.3255] |
| vs INDEXED-TRUE (summary), all | 661 / 104 | 0.7339 | 0.8144 | +0.0805 | [+0.0177, +0.1439] | [-0.0081, +0.1660] |
| vs INDEXED-TRUE (summary), supersession | 620 / 63 | 0.8572 | 0.8189 | -0.0383 | [-0.1155, +0.0402] | [-0.1192, +0.0442] |
| vs INDEXED-TRUE (summary), expiry | 572 / 15 | 0.5110 | 0.7866 | +0.2756 | [+0.1209, +0.4275] | [-0.0346, +0.5094] |
| vs INDEXED-TRUE (summary), retraction | 583 / 26 | 0.5638 | 0.8194 | +0.2556 | [+0.1306, +0.3786] | [+0.0608, +0.3916] |

FOK on the 307 (descriptive): RETRIEVED-BELIEVED 0.7974 [0.7346, 0.8542] against RETRIEVED (join tags) 0.7870.

**Collapse rule (section A):** D vs RETRIEVED +0.1292; item interval excludes zero: True; persona interval excludes zero: True → **not collapsed: the tag clause stays unconditional**.

### AUX-RESP-A1-H45-HYBRID, -H45-RETRIEVED, -H45-OWN — Haiku 4.5 at k = 5 (Batch), against its recorded INDEXED-TRUE row on the 661

**AUX-RESP-A1-H45-HYBRID** — arm HYBRID: probe served `claude-haiku-4-5-20251001` (2053 in / 200 out); Batch rows 3305, OK 3305, units scored 661 (at least three draws, mean); billed $4.1024.

| row | n / positives | Haiku 4.5 INDEXED-TRUE (recorded) | arm | D | item-level 95% | persona-clustered 95% |
|---|---|---:|---:|---:|---|---|
| all | 661 / 104 | 0.8210 | 0.7863 | -0.0347 | [-0.0930, +0.0248] | [-0.1109, +0.0433] |
| supersession | 620 / 63 | 0.8897 | 0.7877 | -0.1020 | [-0.1739, -0.0265] | [-0.2006, +0.0014] |
| expiry | 572 / 15 | 0.6874 | 0.8270 | +0.1396 | [-0.0338, +0.3048] | [-0.0914, +0.3385] |
| retraction | 583 / 26 | 0.7317 | 0.7595 | +0.0278 | [-0.0928, +0.1408] | [-0.1534, +0.1843] |

FOK on the 307 (descriptive): HYBRID 0.8087 [0.7522, 0.8567] against the recorded TRUE row 0.7465.

**AUX-RESP-A1-H45-RETRIEVED** — arm RETRIEVED: probe served `claude-haiku-4-5-20251001` (811 in / 39 out); Batch rows 3305, OK 3305, units scored 661 (at least three draws, mean); billed $1.9409.

| row | n / positives | Haiku 4.5 INDEXED-TRUE (recorded) | arm | D | item-level 95% | persona-clustered 95% |
|---|---|---:|---:|---:|---|---|
| all | 661 / 104 | 0.8210 | 0.7134 | -0.1077 | [-0.1732, -0.0369] | [-0.1939, -0.0203] |
| supersession | 620 / 63 | 0.8897 | 0.6911 | -0.1986 | [-0.2834, -0.1039] | [-0.2994, -0.0967] |
| expiry | 572 / 15 | 0.6874 | 0.7743 | +0.0870 | [-0.0735, +0.2452] | [-0.0493, +0.1954] |
| retraction | 583 / 26 | 0.7317 | 0.7322 | +0.0005 | [-0.1390, +0.1288] | [-0.2181, +0.1773] |

FOK on the 307 (descriptive): RETRIEVED 0.8133 [0.7479, 0.8693] against the recorded TRUE row 0.7465.

**AUX-RESP-A1-H45-OWN** — arm V2-OWN: probe served `claude-haiku-4-5-20251001` (1775 in / 200 out); Batch rows 510, OK 510, units scored 102 (at least three draws, mean); billed $0.6690.

| row | n / positives | Haiku 4.5 INDEXED-TRUE (recorded) | arm | D | item-level 95% | persona-clustered 95% |
|---|---|---:|---:|---:|---|---|
| all | 661 / 104 | 0.8210 | 0.6882 | -0.1328 | [-0.1778, -0.0960] | [-0.1940, -0.0790] |
| supersession | 620 / 63 | 0.8897 | 0.6759 | -0.2139 | [-0.2752, -0.1584] | [-0.3005, -0.1388] |
| expiry | 572 / 15 | 0.6874 | 0.6914 | +0.0040 | [+0.0003, +0.0094] | [-0.0010, +0.0122] |
| retraction | 583 / 26 | 0.7317 | 0.7164 | -0.0153 | [-0.0516, +0.0164] | [-0.0478, +0.0136] |

### AUX-RESP-A1-SPEND

Haiku 4.5 (Batch prices): HYBRID $4.1024; RETRIEVED $1.9409; OWN $0.6690; probes $0.0068; **total $6.7192** against the $12.00 cap. GPT-4.1 mini (section A): $0.2310.

<!-- R109-PRINTED-BEGIN -->

### AUX-RESP-A1-PRINTED — the forms the paper prints (R109, 2026-09-14; Section 6 and Appendix E.10), each the two-decimal rounding of a value in this section

RETRIEVED-BELIEVED (GPT-4.1 mini, the view under FR-Bank's own marks): 0.81 (0.8144) against 0.69 (0.6851) under the join's tags, +0.13 (+0.1292; both intervals exclude zero); against the summary alone 0.73 (0.7339), +0.08 (+0.0805; item interval [+0.0177, +0.1439] excludes zero, persona interval [-0.0081, +0.1660] includes it). Store marks: precision 0.14 (0.1353) over the 3305 lines shown, 1273 changed; forbidding records in view marked by the store 70 of 99 against the join's 60. Haiku 4.5 (k = 5): HYBRID 0.79 (0.7863) against its summary 0.82 (0.8210), -0.03 (-0.0347; intervals include zero); RETRIEVED 0.71 (0.7134), -0.11 (-0.1077; both exclude zero); own-name ablation: all -0.13 (-0.1328); supersession 0.89 (0.8897) to 0.68 (0.6759), -0.21 (-0.2139; both exclude zero); retraction -0.02 (-0.0153). Spend: the Haiku 4.5 lanes billed \$6.72 ($6.7192). The collapse rule read not collapsed, so the box's tag clause states that the tagged view kept its reading under the store's own marks.

<!-- R109-PRINTED-END -->
