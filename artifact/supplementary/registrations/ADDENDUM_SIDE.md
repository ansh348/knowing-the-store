# ADDENDUM_SIDE — registration for the two side experiments S1 and S2

Frozen against baseline HEAD `35743cb`, 2026-09-12 (branch `[BRANCH]`), **BEFORE any
S1 or S2 index exists and before any monitor call**. Spec: the SIDE-REG instruction of
2026-09-12, the two rulings of the same day (the S1 mapping as a PROPOSED two-channel entry
map under conditions (a)–(e); S1 Haiku to October), and the four rulings of the same day on the
open items of `reviews/SIDE_REG_REPORT.md` (#2 spot-check fallback; #3 the frozen ambiguity
measure; #4 the S2 precision repair withdrawn and replaced by the descriptive arm S2-U; #7 NB-4
and NB-5 on the GT indexes, NB-6 not). Rules inherited from
R74/R76/R77/R81/R82: nothing unregistered may be reported; no committed value is recomputed;
registered verdicts are never re-adjudicated; **publish-regardless** — every result prints under
its frozen text. The template is `ADDENDUM_R77.md` §S, the registered wrong-index control:
committed populations, committed prompts, only the index text changed, blind and intact arms
read from the committed rows and never re-elicited.

**Results print in the appendix only. No headline number in the abstract or Section 1 changes
on account of S1 or S2.**

**AI use.** The ruling (d) spot-check verdicts are the author's; the read was discussed with a
language model. The censuses, the draft text and the ledger entries were prepared with Claude
Code under the author's rulings; every number traces to a committed artifact or to a script
named in `reviews/SIDE_REG_REPORT.md`.

Ledger: `side_experiments/NUMBERS_SIDE.md`, keys `AUX-SIDE-*` (all reserved in §L; path is the
author's call). Verifier: `side_experiments/tools/verify_side.py`, **required to exist and pass
on the empty cell before any S1 or S2 index exists**. Deviations:
`side_experiments/DEVIATIONS_SIDE.md`, own numbering from **D-SIDE-1**. Bootstrap: the committed
estimators (`e1r_robustness/tools/common_e1r.py`: paired item-level bootstrap, 1,000 draws, seed
42, single-class draws discarded), persona-clustered interval printed beside.

Metered budget: **the budget rule of §B, frozen.** Mini lanes — S1 (522 calls) and S2-U (661
calls) plus the leakage screens — under $2 in total from the OpenAI key, unconditional. **No
Haiku lane runs under this registration**: the S1 Haiku lane moves to October (§S1) and the S2
Haiku lane is withdrawn with the repair arm (§S2). Opus is not run on either experiment. The
Anthropic key is not touched.

---

## §C — Pre-freeze censuses (both $0, deterministic, disclosed rather than inferred)

Both censuses below were computed **before this draft** from committed artifacts with local code
and no model call, exactly as R77 §C disclosed its structural check (D-R74-17 precedent). Their
values are invariant to when they are computed. Both are recorded in
`reviews/SIDE_REG_REPORT.md` Phases 1 and 2 with the scripts that produced them.

### §C.1 — S1: the two-channel entry map and what it populates

**No entry-to-slot mapping exists in the tree.** The committed presence control
(`e1_metamemory/tools/two_channel.py`, `two_channel_control.json`, `build/items_final.json`) is
question-level: it routes each external item PRESENT / ABSENT / UNRESOLVED and keeps no entry
id (`channels()` returns `any(...)` and a maximum cosine). Mem0 and A-MEM rows carry no origin,
category or slot field (`e1_metamemory/tools/backends.py:115-176`). The mapping below is
therefore **PROPOSED**, not the presence control; what it inherits from the presence control is
its two channels, its encoder and its threshold, unchanged.

**The mapping, per backend entry `e` of persona `p`, over the FR-Bank entries `F(p)`:**
- lexical channel: `exp4_witnesses.supports_correct(e.text, f.text)` — at least two shared
  content tokens and at least half of `f`'s content tokens covered — the presence control's
  own function, with the FR-Bank entry text in the answer role;
- embedding channel: cosine(`e`, `f`) ≥ **0.295** on the cached `text-embedding-3-small`
  vectors (`e1_metamemory/backend_embeddings/{mem0,amem}.npz`;
  `LifeMemEval/artifacts/lifecycle_banks/*_embeddings.npz`), no new embedding call;
- `e` is **mapped** iff some `f` passes the lexical channel or the maximum cosine reaches the
  threshold; its **target** is the argmax-cosine entry among lexical hits if any, else the
  argmax-cosine entry. **The threshold and the lexical channel are inherited as-is and are not
  tuned here** (ruling (b)).
- **State (ruling (a)):** a mapped entry carries its target's ground-truth lifecycle state from
  `index_v2.true_lifecycle`, its target's category and slot, and its own backend recency
  (`index_v2` R3). One rule for both backends, no per-backend case: Mem0's overwritten points
  map to the newest FR-Bank entry on the slot and show as ACTIVE, which is the truth about that
  store; A-MEM's mapped notes carry whatever state their target has. Unmapped entries are not in
  the index; the census discloses their share.
- **Ambiguity (frozen measure, ruling #3):** a mapped entry is **slot-changing ambiguous** when
  a second FR-Bank candidate lies within 0.02 cosine of the target and its `slot_key` differs
  from the target's. **Nearest wins**: the target stays the argmax entry. The slot-changing rate
  per backend prints in the ledger (`AUX-SIDE-S1-AMBIG-*`); the any-second-candidate rate (a
  second entry within 0.02 regardless of slot) prints beside it as descriptive
  (`AUX-SIDE-S1-AMBIG-ANY-*`). The pre-freeze census below computed the slot-changing variant on
  the *scrubbed* slot name; the frozen measure keys on the full `slot_key`, so the ledgered rate
  is re-computed by `verify_side.py` under the frozen definition and will be at or above the
  figure printed here.

**RENDERER LOCK.** The GT index is rendered by `index_v2.render` under
`AVAIL[("frbank","TRUE")]` through `view`, the same call path as every committed index. The
identity mapping on FR-Bank reproduces `indexes_v2.json["frbank:<p>:FULL:TRUE"]` **byte for
byte on all 40 personas** (verified 2026-09-12; a failure is a STOP at build).

**Census, 2026-09-12, from the committed caches:**

| | Mem0 (37 personas) | A-MEM (40 personas) |
|---|---:|---:|
| stored entries | 9,736 | 11,319 |
| mapped | **9,704 (0.997)** | **10,974 (0.970)** |
| of which lexical only / embedding only / both | 0 / 4,895 (50.4%) / 4,809 (49.6%) | 5 / 4,962 (45.2%) / 6,007 (54.7%) |
| unmapped | 32 | 345 |
| ambiguous, second-best within 0.02 (descriptive) | 29.8% | 38.4% |
| ambiguous, any second candidate within 0.02 (descriptive; ledgered beside the frozen rate) | 34.1% | 47.4% |
| **ambiguous, slot-changing — pre-freeze census on the scrubbed name; the frozen `slot_key` measure is ledgered at build** | **24.1%** | **36.5%** |
| GT index, mean lines / o200k tokens | 57.8 / 918.8 | 57.8 / 931.0 |
| FR-Bank TRUE FULL index, same personas | 63.2 / 1,074.1 | 63.2 / 1,077.1 |
| lifecycle totals GT vs FR TRUE (sup / ret / exp) | 20 / 6 / 138 vs 97 / 21 / 264 | 40 / 13 / 123 vs 104 / 23 / 276 |
| Mem0 points carrying `updated_at` → target state | active 1,216 · expired 16 · retracted 3 · superseded 9 | — |

**Rule (c) — fair test:** both backends are above 0.50 mapped, so S1 is a fair test on both
under the rule; the rows are predictions, not descriptive. The mapped share is high because
the encoder finds a nearest neighbour for almost every entry; **what the census cannot
establish is that the neighbour is the same fact**, which is why the spot-check of §S1 is
load-bearing. Half of all mapped entries rest on the embedding channel alone, and a quarter
(Mem0) to a third (A-MEM) of mapped entries have a competing FR-Bank entry with a different
slot name within 0.02 cosine.

**The lifecycle totals are thin by construction and are disclosed, not repaired.** The GT
index carries a fifth to two-fifths of FR-Bank's superseded and retracted states. On Mem0 that
is the store's truth: the superseded entries have been overwritten, so nothing maps to them.
On A-MEM, which keeps every note, it is a mapping effect. S1 is a FOK experiment and reads the
name map; the superseded-names section is printed as it falls out and carries no prediction.

### §C.2 — S2: the two candidate repair rules and the census that fixed neither

**Two rules, written before the census, over backend-exposed fields only** (`supersedes`,
`is_active`, `is_retracted`, `slot_key`, `created_at`; the manifests are never read):

- **BR-A, pointer rule (the simpler predicate).** `f` is superseded iff `f` is inactive, not
  retracted, and some entry `g` in the bank carries `supersedes == f.id`.
- **BR-B, terminal successor with a session gap.** BR-A, and the newest such `g` is active, and
  `created_at(g) − created_at(f) ≥ 14 days` — `EXPIRY_WINDOW`, a constant already frozen in
  `e0_common.py:60`, not tuned here.

**Selection rule, written in advance:** highest recall subject to precision ≥ 0.80, ties to the
simpler predicate; metrics micro-averaged over the 661 items on the **rendered** superseded list
(the list the reader and NB-6 see, parsed by `index_features.parse`, NB-6's own parser), with
the uncapped name-set metrics beside. INDEXED-BR would be the BELIEVED index with only the
superseded state replaced by the rule's set; retracted and expired stay the store's own.

**Gates, both passed 2026-09-12:** rendering BELIEVED states through the locked renderer
reproduces the committed BELIEVED index text byte for byte on **661 of 661** items; names per
item on the committed texts reproduce `e1r_robustness/results/nb6.json` — TRUE
**1.7473524962**, BELIEVED **15.0378214826** — to 1e-9.

| List | names / item, rendered | precision | recall | names / item, uncapped | precision | recall |
|---|---:|---:|---:|---:|---:|---:|
| TRUE (reference) | 1.7474 | 1.0000 | 1.0000 | — | — | — |
| BELIEVED (committed) | 15.0378 | 0.0348 | 0.2996 | 32.55 | 0.0357 | 0.6658 |
| BR-A | 15.0378 | 0.0348 | 0.2996 | 32.51 | 0.0358 | 0.6658 |
| BR-B | 8.9592 | 0.0618 | 0.3169 | 9.15 | 0.0633 | 0.3316 |

**Outcome: no candidate reaches precision 0.80; no rule is fixed.** BR-A is indistinguishable
from BELIEVED on the rendered list — the pointer removes 243 unpointed inactive entries and the
31 retracted ones, none of which reach the capped list. BR-B halves the list and raises
precision from 0.035 to 0.062. The floor is unreachable for a structural reason the census
establishes: the store marks **5,968** entries inactive and carries **5,725** `supersedes`
pointers, against **104** entries the manifest marks superseded, and on the allowed fields the
two groups are the same — every inactive TRUE-superseded entry is pointed at by a same-slot
successor, as are 5,661 of the 5,904 others, and the successor-gap distributions coincide
(median 0 days; 70.3% versus 71.8% same-day). **Forty of the 104 TRUE-superseded entries are
still active in the store**, out of reach of any rule keyed on inactivity. A rule that printed
only TRUE's 1.75 names would need precision above 0.80 on a list of about two names, and no
metadata predicate separates those two from the 15 the store believes.

**The cap figures, ledgered (ruling #4):** the BELIEVED list uncapped holds **66.6%** of TRUE's
names (micro-recall 0.6658); the alphabetical cap of 15 in the renderer cuts the rendered recall
to **30.0%** (0.2996); precision is 0.036 uncapped and 0.035 rendered. Both recall figures are
recorded under `AUX-SIDE-S2-CAP-RECALL`. This is a renderer effect, not a metadata rule, and it
is what the descriptive arm S2-U of §S2 measures.

**Consequence for this registration (ruling #4).** **The precision repair is withdrawn.** The
census above **is S2's result and is frozen as such**: no predicate over backend-exposed fields
separates the 5,968 store deactivations from the 104 manifest supersessions, because they are
metadata-identical, and 40 of the 104 remain active. S2-P1 and S2-P2 are **replaced** by one
descriptive arm, S2-U (§S2), with no pass bar. The S2 Haiku lane is withdrawn with the repair
arm. The census reading prints under its own frozen text (§S2, "S2 census reading").

## §S1 — name-bearing index for the structureless backends (metered, mini)

**Question.** Is the inversion on Mem0 and A-MEM (Table `tab:inversion`: mini −0.0969 on Mem0,
−0.1065 on A-MEM) a property of the backend or of the index it was handed? **After the ruling (d)
read of 2026-09-12 the question is registered on A-MEM and descriptive on Mem0** (step 2 below).

**Populations, from the committed E1 universe, asserted by the runner.** The committed external
FOK items: **Mem0 238** (94 non-ABSENT positives, 37 personas, 211 distinct questions) and
**A-MEM 284** (126 positives, 40 personas, 254 questions), `build/items_final.json` rows with
`label ∈ {PRESENT, ABSENT}`; `e1_metamemory/NUMBERS.md` `AUX-TABLE-POS`. **NOK is not
measurable on these backends** and is not scored: PN cannot exist in a store that overwrites
(Mem0) or that records no lifecycle state (A-MEM), so the obligation label has no referent there.
The registration says so and prints no NOK row.

**Lane.** `gpt-4.1-mini` pinned, temperature 0, seed 42, `k = 1`, E1 protocol, frozen
`prompts_e1` with both digests asserted (`run_cf.py:43-46` precedent). Served identifier checked
before launch (E1.7 rule); mismatch = do not launch. **Haiku 4.5 does not run on S1.** No
committed Haiku blind or TRUE rows exist on the external items (`r74/x4/rows_H45.jsonl` covers
`cell_661` only), so under "blind arms are the committed rows, never re-run" the lane has
nothing to pair against; re-eliciting them is October money. Every S1 Haiku row prints a dash
with that reason. Table 1's inversion rows are mini rows, so mini is the reader of record.

**Arms.** One manipulated arm replacing only the index text:
- **INDEXED-GT** — each item scored against the GT index of its own persona and backend, built
  by the §C.1 mapping through the locked renderer in the exact v2 format: header, lifecycle
  totals, per-category breakdown, recency, attribute names by category (scrubbed, `SLOT_CAP`
  15), attribute names carrying superseded content. **This departs from `index_v2` R1 on
  purpose**: R1 marks names inexpressible on these stores because they carry none. INDEXED-GT is
  the counterfactual "what the reader would do if this store carried the manifest's names for
  what it holds", not a description the store can produce; the paper's TRUE index on these
  backends stays as it is.
- **INDEXED-TRUE (committed)** — the intact arm, `elicitation_main.json` `INDEXED-TRUE` rows keyed
  by item id. Read, never re-elicited.
- **BLIND (committed)** — `elicitation_main.json` `BLIND` rows keyed by question text, re-derived
  per item exactly as the committed E1 scorer pairs them. Read, never re-elicited.

**Before any monitor call, in this order, each ledgered:**
1. **Census** (§C.1) re-run by `verify_side.py` and matched to the values above
   (`AUX-SIDE-S1-MAP-MEM0`, `-AMEM`).
2. **Spot-check, ruling (d) — READ COMPLETE 2026-09-12, ledgered before any elicitation.**
   Thirty mapped pairs per backend, `random.Random(42)` over the mapped pairs sorted by
   (persona, backend entry id) — the sixty pairs are frozen in §S1.a below; texts in
   `reviews/SIDE_REG_REPORT.md`, appendix. **Criterion, frozen as read:** a pair is correct when
   the backend entry is about the same slot as its mapped FR-Bank entry — same attribute, same
   subject; a value difference alone is not wrong; a different subject, a different attribute,
   or an entry from which no single slot can be recovered is wrong. Verdicts are the author's;
   the read was discussed with a language model (AI-use line, header).
   **Outcome (`side_experiments/NUMBERS_SIDE.md` §1):**
   - `AUX-SIDE-S1-SPOTCHECK-MEM0`: **17 / 30, precision 0.567**, 7 borderline (pairs 3, 8, 11,
     16, 19, 20, 21). Among the 16 lexically supported pairs 13 correct (0.81); the 13 wrong
     pairs are embedding-only or under cosine 0.55 in all but three (12, 18, 22). **Below 0.80:
     the fallback fires.**
   - `AUX-SIDE-S1-SPOTCHECK-AMEM`: **24 / 30, precision 0.800**, 7 borderline (pairs 1, 3, 4, 9,
     13, 17, 23). Among the 17 lexically supported pairs 16 correct (0.94). **Not below 0.80:
     the two-channel map stands; no fallback.** `AUX-SIDE-S1-MULTI-AMEM`: 8 of the 30 notes
     (pairs 6, 7, 8, 11, 19, 20, 21, 28) carry the mapped fact alongside other facts the index
     will not name — a stated reason the A-MEM GT index under-describes the store.
   **The pre-specified fallback, and no second (ruling #2) — FIRED ON MEM0.** Mem0's mapping is
   **lexical-required**: an entry maps only where the lexical channel supports some FR-Bank
   entry, and the embedding channel breaks ties among lexical hits only. The Phase 1 census
   re-ran under that mapping on 2026-09-12 (`AUX-SIDE-S1-FALLBACK-MEM0`): **4,809 of 9,736
   mapped, 0.4939**, equal to the pre-freeze lexical-supported count to the entry; 17 of 37
   personas at or above 0.50 (median 0.496); frozen slot-changing ambiguity 25.2% of mapped
   (any-second-candidate 31.6%); GT index 54.1 lines / 814.9 o200k tokens; lifecycle totals
   superseded 13 / retracted 3 / expired 74. **Rule (c): 0.4939 < 0.50 — S1 on Mem0 is a
   DESCRIPTIVE ROW**, reason "spot-check precision 0.567 under the two-channel map;
   lexical-required coverage 0.494". The Mem0 INDEXED-GT arm still runs, under the
   lexical-required indexes, and its rows print as descriptive beside A-MEM's. No further
   fallback exists. A-MEM's lexical-supported share (6,012 of 11,319, 0.531) is recorded for
   the record; it plays no role, since A-MEM's fallback did not fire.
3. **Leakage screen, ruling (e).** `ladder_e1.py` at level 0 on the GT indexes of both
   backends (under the fallback mapping where it applies), the same 30 PRESENT items per backend
   it draws for the committed screen, seed 42; more than 3 of 30 correct is a STOP. Sixty mini
   calls, priced in §B. (`AUX-SIDE-S1-LEAK-MEM0`, `-AMEM`.)
4. **Mechanical readers, ruling #7.** **NB-4** (lexical query-to-index match, maximum
   content-token Jaccard against every attribute name the index exposes) and **NB-5**
   (embedding match, `sentence-transformers/all-MiniLM-L6-v2` from the local cache, no network)
   run on **every** GT index as `e1r_robustness/SPEC_E1R.md` defines them, local and $0, and
   print beside the S1 monitor rows (`AUX-SIDE-S1-NB4-*`, `-NB5-*`). **NB-6 does not run on the
   GT indexes**: their superseded-names section is thin by construction (§C.1) and carries no
   prediction.

**Registered items — on A-MEM. The failure texts were written first, then the predictions.**
S1 is a **registered test on A-MEM** (two-channel map, spot-check 0.800, rule (c) 0.970) and a
**descriptive row on Mem0** (spot-check 0.567 → lexical-required map → coverage 0.494 < 0.50).
The same four quantities print for both backends; only A-MEM's carry a verdict.

*S1-P1 FAILS — the inversion is not repaired by naming.* Frozen text, appendix only:
> On the committed A-MEM items, handing the store a name-bearing index built from the manifest
> for the entries it holds moves the coverage gain from $X$ to $Y$, a paired difference of $D$
> with interval $I$, which does not clear the tolerance with an interval excluding zero. The
> inversion is not repaired by naming, and Section 5.3 keeps its wording.

*S1-P2 FAILS — the name-bearing index still inverts.* Frozen text:
> Under the name-bearing index the coverage gain on A-MEM is $Y$ with interval $I$ lying
> entirely below zero: on this store the index inverts the benefit even when it carries the
> manifest's names.

- **S1-P1 (A-MEM).** The paired FOK gain under INDEXED-GT exceeds the gain under the committed
  TRUE index by more than 0.05, with the paired interval of the difference excluding zero.
  Reading if held, appendix only: *"Given the manifest's names for what it holds, the store no
  longer inverts the benefit by the margin it did; the inversion was a property of the index
  the store was handed, not of the store alone."*
- **S1-P2 (A-MEM).** The INDEXED-GT gain itself is not negative: its interval does not lie
  entirely below zero. Reading if held: *"The name-bearing index does not invert."*

**Mem0 descriptive row — frozen text, prints regardless, appendix only:**
> On Mem0 the name-bearing index could be built for 49.4 percent of the store's entries under
> the lexical-required mapping the spot-check forced (two-channel precision 0.567); below the
> registered coverage floor of one half, its coverage gain of $Y$ (interval $I$; TRUE $X$) is
> reported and carries no verdict.

Both outcomes are informative on A-MEM. **No sentence in Section 5.3 or Section 6 is changed on
S1's account without a ruling**; the appendix table and, at most, one footnote at
`paper_v4.tex:1633` are the output cap. The NB-4 and NB-5 rows print beside the monitor rows on
both backends.

**Projection.** 522 indexed calls; GT indexes run about 150 o200k tokens shorter than FR-Bank
TRUE, so at the committed mini means less that difference (≈1,397 / 1,407 input, 24.4 output;
$0.40 / $1.60 per 1M): **≈ $0.31**, plus the 60-call leakage screen ≈ $0.04 **[est]**.

### §S1.a — the frozen spot-check sample (seed 42; texts in `reviews/SIDE_REG_REPORT.md` Phase 1)

Mem0, (persona, backend id prefix → FR-Bank entry, cosine, channel):
dariush 9354a305 → lb_00454 0.841 both · aroha 5faac89e → lb_00353 0.479 emb · kenji 965863a1
→ lb_00182 0.501 emb · jerome d8774039 → lb_00207 0.803 both · jake a673a507 → lb_00111 0.449
emb · diane 27d871c9 → lb_00158 0.530 emb · dariush 1b880e03 → lb_00412 0.908 both · tom
8abe7977 → lb_00390 0.522 emb · chenoa 453fd4bf → lb_00069 0.895 both · zara cfb6478e →
lb_00006 0.451 emb · omar 702ae907 → lb_00207 0.452 emb · aroha cdae3aed → lb_00056 0.740 both
· aroha a6d0f992 → lb_00006 0.881 both · chenoa a25fb5bd → lb_00440 0.891 both · jake 5ef892ce
→ lb_00065 0.925 both · jerome 24c1ae47 → lb_00020 0.491 emb · saga 020779aa → lb_00054 0.865
both · aroha 74dd4910 → lb_00198 0.472 both · yoli 140847f7 → lb_00064 0.565 emb · ingrid
00f616a0 → lb_00222 0.462 emb · tom 8599d9a3 → lb_00317 0.533 emb · omar 3fc6974d → lb_00341
0.639 both · jake 79fe7e01 → lb_00139 0.446 emb · patrick 8e79e8aa → lb_00173 0.771 both · zara
b7170754 → lb_00329 0.739 both · kenji c9467865 → lb_00100 0.302 emb · amara 69571810 →
lb_00017 0.670 both · dmitri 4722003d → lb_00288 0.788 both · omar 7e221961 → lb_00264 0.836
both · marcus ab4855a6 → lb_00060 0.384 emb.

A-MEM:
yoli 0088c8ad → lb_00425 0.513 emb · callum 5a8bea9f → lb_00236 0.306 emb · alex 5c01067c →
lb_00234 0.550 emb · jake cf2a248a → lb_00179 0.356 emb · fatima e7305eba → lb_00177 0.833 both
· elena a52fba76 → lb_00244 0.618 both · dariush 102e5aef → lb_00494 0.794 both · bruna
e1a6df91 → lb_00440 0.641 both · rosa 3961ab8e → lb_00461 0.652 both · bruna 06570479 →
lb_00265 0.741 both · samuel e48fca2b → lb_00390 0.388 both · mehmet fee0cdb9 → lb_00200 0.685
both · alex b71832ac → lb_00152 0.499 emb · alex a2ccf849 → lb_00382 0.552 emb · bruna 6d5961a3
→ lb_00502 0.567 both · elena 649a3f1b → lb_00215 0.494 emb · fatima 23d94105 → lb_00217 0.504
emb · patrick dc2e34ef → lb_00265 0.550 emb · thanh 83812823 → lb_00237 0.686 both · alex
71aa1c08 → lb_00073 0.536 emb · saga 1e106828 → lb_00274 0.502 both · dmitri 4a58ef05 →
lb_00281 0.630 emb · yoli 9ffa30d4 → lb_00367 0.401 emb · rosa 33265fe3 → lb_00400 0.820 both ·
mehmet d66c67c0 → lb_00369 0.711 both · elena 825adb03 → lb_00454 0.401 emb · nadia 79435f95 →
lb_00265 0.627 both · samuel d0cb7a2c → lb_00540 0.676 both · jerome 05064f16 → lb_00090 0.660
both · aisha 5eef914e → lb_00435 0.663 both.

## §S2 — BELIEVED on FR-Bank: the census result, frozen, and one descriptive arm (mini)

**Question, as asked.** Can a filter on metadata the backend itself exposes recover the
obligation gain that BELIEVED loses? The committed BELIEVED superseded list averages 15.04 names
per item against 1.75 under TRUE (`e1r_robustness/NUMBERS_E1R.md:257-258`, `:304`).

**Answer, at $0, frozen as S2's result (ruling #4).** The precision repair is **withdrawn**. The
Phase 2 census of §C.2 is S2's result: **no predicate over backend-exposed fields separates the
5,968 store deactivations from the 104 manifest supersessions, because they are
metadata-identical, and 40 of the 104 remain active.** No INDEXED-BR arm exists; S2-P1 and S2-P2
are replaced by the descriptive arm below; the S2 Haiku lane is withdrawn with the repair arm.

**S2 census reading — frozen, prints regardless, appendix only:**
> Two filters on the metadata FR-Bank exposes — the store's own supersession pointers, alone
> and restricted to an active successor at least fourteen days later — leave the superseded list
> at 15.04 and 8.96 names per item against 1.75 under ground truth, at precision 0.035 and
> 0.062. The store records 5,968 deactivations and the manifest 104 supersessions, and on the
> fields the store exposes the two are indistinguishable; forty of the 104 are still active in
> the store. The believed-state loss is not a filtering problem.

**Population, asserted by the runner.** The committed obligation population, `r74/x4/cell_661.json`:
**661 items, 104 PN**, FR-Bank FULL 323 / CAT-ABLATED 176 / SLOT-ABLATED 162.

**Lane.** `gpt-4.1-mini` as in §S1, **mini only**. No Haiku call on S2.

**Arm S2-U — the BELIEVED index with `SLOT_CAP` lifted (descriptive, no pass bar).** Each item
is scored against its own committed BELIEVED store version rendered by `index_v2.render` with
the per-bucket cap of 15 removed, so every name block — the per-category attribute names and
the superseded-names section — prints in full with no `(+N more)`. Nothing else in the renderer
or the states changes. **RENDERER LOCK:** the same render with `SLOT_CAP = 15` must reproduce the
committed BELIEVED text byte for byte on all 661 items (verified for the committed cap on
2026-09-12, §C.2); a mismatch is a STOP. What the arm changes is exactly the cap effect §C.2
measured: the superseded list's recall of ground-truth names rises from **30.0%** to **66.6%**
while its precision stays at **0.035**; the list grows from 15.04 to 32.55 names per item.
Contrast: the committed BELIEVED, TRUE and blind arms (`elicitation_main.json`), read, never
re-elicited. Before any monitor call: the census re-run by `verify_side.py`; the leakage screen
on a seed-42 sample of 30 S2-U indexes, more than 3 of 30 a STOP (`AUX-SIDE-S2-LEAK`).

**What prints.** Blind, TRUE, BELIEVED and S2-U NOK AUROC on the 661; the paired gains; **the
retention** of the TRUE gain under S2-U, `(S2-U − blind) / (TRUE − blind)`, printed against the
committed 42.3% and the 60% line as a descriptive figure with its paired interval; the paired
S2-U − BELIEVED difference with its interval. **No pass bar.** 661 mini calls.

**Expected direction, stated in advance.** Lifting the cap raises recall and leaves precision at
0.035: the list still names about 31 attributes for every one ground truth marks. **Retention is
expected to stay short of 60%.**

**Branch texts, written before any call, for both directions; appendix only.**

*S2-U — retention stays short of 60% (expected):*
> Lifting the cap on the believed list raises its recall of ground-truth superseded names from
> 30.0 to 66.6 percent and leaves its precision at 0.035; under that list the obligation gain
> retains $F$ percent of the TRUE gain, still short of the 60 percent threshold. The
> believed-state loss is not a cap effect.

*S2-U — retention reaches 60% (not expected):*
> Lifting the cap on the believed list, which raises its recall of ground-truth superseded names
> from 30.0 to 66.6 percent at unchanged precision, retains $F$ percent of the TRUE gain, at or
> above the 60 percent threshold. Part of the believed-state loss recorded at 42.3 percent is an
> effect of the renderer's cap of fifteen names rather than of the store's metadata.

**The 42.3 percent sentence in Section 6 (`paper_v4.tex:641`) stays as printed either way.**
Under the second branch any qualification is a ruling, recorded as an amendment, not a change
made here.

**Projection.** Mini 661 calls. The uncapped BELIEVED index is longer than the committed one —
about 17 more superseded names and every per-category list in full — so the input is taken at
the committed mean plus 150 tokens **[est]** (≈1,703 / 24.4; $0.40 / $1.60 per 1M): **≈ $0.48**,
plus the 30-call leakage screen ≈ $0.02 **[est]**. No Haiku, no Opus.

## §T — Estimators and the committed blind arms ($0)

Mann-Whitney AUROC with ties at 0.5 (`common_e1r.auroc`). The registered interval is the
**item-level paired bootstrap** (`common_e1r.boot_item`, 1,000 draws, seed 42, single-class draws
discarded) — the interval R77 §S and Table `tab:inversion` read — and the **persona-clustered
paired bootstrap** prints beside it; where the two disagree on a prediction the text says so
and the weaker reading governs, as `ADDENDUM_R82.md` §6 rules. Tolerance ±0.05 throughout.
For S1-P1 the quantity is the paired difference of two paired gains on the same items:
(INDEXED-GT − BLIND) − (INDEXED-TRUE − BLIND) = INDEXED-GT − INDEXED-TRUE per item. For S1-P2
it is INDEXED-GT − BLIND. For S2-U the quantities are descriptive: the paired gain S2-U − BLIND
with its interval, the retention `(S2-U − BLIND) / (TRUE − BLIND)` as a ratio of the two paired
gains, and the paired S2-U − BELIEVED difference with its interval; none carries a pass bar.
NB-4 and NB-5 on the GT indexes are scored as `SPEC_E1R.md` scores them (unsupervised, directly,
no fold). Blind scores are per question and are attached to items exactly as the committed E1
scorer attaches them; no blind row is re-elicited.

## §B — Budget rule (frozen) and telemetry

**Mini lanes:** S1 522 calls and S2-U 661 calls, with the two leakage screens (60 + 30 calls),
**under $2 total**, run unconditionally from the OpenAI key. **Haiku lanes: none run under this
registration.** S1's Haiku lane (2,610 calls, about $3.30 at Batch) has no committed blind or
TRUE arm to pair against and **moves to October**; every S1 Haiku row prints a dash with that
reason. S2's Haiku lane (3,305 calls, about $4.17 at Batch) is **withdrawn with the repair arm**
(ruling #4) and does not print. **Opus is not run on either experiment.** The Anthropic key is
not touched; the CF-2 Haiku line is not a condition of anything here.

| Lane | Calls | Input / output tokens per call | Price per 1M | Expected | Source |
|---|---:|---|---|---:|---|
| S1 mini, Mem0 (INDEXED-GT) | 238 | ≈1,397 / 24.4 **[est]** | $0.40 / $1.60 | $0.14 | R77 §S means less the GT–TRUE token gap of §C.1 |
| S1 mini, A-MEM (INDEXED-GT) | 284 | ≈1,407 / 24.4 **[est]** | $0.40 / $1.60 | $0.17 | same |
| S1 leakage screen, both backends | 60 | ≈1,402 / 24.4 **[est]** | $0.40 / $1.60 | $0.04 | same |
| S2-U mini (BELIEVED, `SLOT_CAP` lifted) | 661 | ≈1,703 / 24.4 **[est]** | $0.40 / $1.60 | $0.48 | R77 §S means plus 150 tokens for the uncapped lists |
| S2-U leakage screen | 30 | ≈1,703 / 24.4 **[est]** | $0.40 / $1.60 | $0.02 | same |
| **Mini total** | **1,273** | | | **$0.85** (×1.3 **$1.11**) | under the $2 rule |
| S1 Haiku (not run) | 2,610 | — | — | ($3.30) | October |
| S2 Haiku (withdrawn) | — | — | — | — | ruling #4 |
| NB-4 / NB-5 on the GT indexes | — | local | — | $0 | `SPEC_E1R.md` NB-4, NB-5 |

`probe` and `project` (the S-runner's equivalents of `run_cf.py`'s) run and report before any
submission; the run stops at $2.

## §L — Ledger keys reserved, verifier, deviations

`AUX-SIDE-S1-MAP-MEM0`, `-S1-MAP-AMEM`, `-S1-AMBIG-MEM0`, `-S1-AMBIG-AMEM` (the frozen
slot-changing rate), `-S1-AMBIG-ANY-MEM0`, `-S1-AMBIG-ANY-AMEM` (descriptive), `-S1-INDEXSIZE`,
`-S1-SPOTCHECK-MEM0`, `-S1-SPOTCHECK-AMEM`, `-S1-MULTI-AMEM` (**written 2026-09-12**),
`-S1-FALLBACK-MEM0` (**written 2026-09-12**), `-S1-FALLBACK-AMEM` (dash: did not fire), `-S1-LEAK-MEM0`, `-S1-LEAK-AMEM`,
`-S1-MINI-MEM0`, `-S1-MINI-AMEM` (blind, TRUE, GT AUROC; the two gains; the paired difference and
both intervals), `-S1-NB4-MEM0`, `-S1-NB4-AMEM`, `-S1-NB5-MEM0`, `-S1-NB5-AMEM`, `-S1-H45` (dash),
`-S2-CENSUS` (the §C.2 table and the 104 / 40 facts), `-S2-CAP-RECALL` (66.6% uncapped, 30.0%
rendered), `-S2-LEAK`, `-S2-MINI` (blind, TRUE, BELIEVED, S2-U AUROC; gains; retention; the
S2-U − BELIEVED difference), `-SPEND`, `-BUDGETRULE`. Every key is written; a key that cannot be
computed carries a dash and its reason.

`side_experiments/tools/verify_side.py` asserts before any index exists: the RENDERER LOCK
identity on all 40 personas and, for S2-U, that the render at `SLOT_CAP = 15` reproduces the
committed BELIEVED text on all 661 items; the §C.1 census values under both the frozen ambiguity
measure and the descriptive one; the §C.2 gates and table; the populations (238 / 284 / 661,
94 / 126 / 104 positives); the `prompts_e1` digests; the committed row counts
(`elicitation_main.json` 332 / 1,183 / 1,183); and, once they exist, that every §L key is present.

`side_experiments/DEVIATIONS_SIDE.md`, from **D-SIDE-1**; nothing yet.

## §STOP — conditions, last, including the budget rule

- Any monitor or matcher call before this file is frozen by the author's commit and GO is given.
- `verify_side.py` absent or failing when the first S1 or S2 index is about to be written.
- The RENDERER LOCK identity failing on any persona; the S2-U render at `SLOT_CAP = 15` not
  byte-identical to the committed BELIEVED text on any item; a GT or S2-U index containing the
  inexpressibility marker or a name containing `:`.
- The S1 spot-check not ledgered before elicitation; spot-check precision below 0.80 on a
  backend without the lexical-required fallback applied and its census ledgered; any second
  fallback.
- The leakage screen returning more than 3 of 30 on any S1 or S2-U index, or missing from the
  ledger.
- Any S2 call other than the 661 S2-U mini calls and its 30-call leakage screen; any repair-rule
  arm elicited.
- NB-6 scored on a GT index; NB-4 or NB-5 missing from the ledger for any backend.
- Any blind or intact row re-elicited rather than read from the committed files.
- **Any Haiku call on either experiment; any Opus call.**
- Mini spend reaching $2 with a cell unscored — the run stops and reports.
- Any number printed without a key in `NUMBERS_SIDE.md`; any reading written after its numbers
  exist; any headline number in the abstract or Section 1 changed on S1's or S2's account; the
  42.3 percent sentence at `paper_v4.tex:641` changed.
- The frozen lineage — `prompts_e1` digests, `index_v2.render`, `two_channel.py`'s threshold
  and channel functions, `exp4_witnesses.supports_correct`, `common_e1r` — changing by one byte.

---

## Registration mechanics

One Table 24 row per experiment, added with this file's freeze-commit hash after the freeze
commit exists. Outcome cells start "pending" and update only per the frozen text above; S1's row
carries a verdict for A-MEM and "descriptive (coverage 0.494)" for Mem0; S2's row reads
"census result frozen (§C.2); S2-U descriptive" and carries no verdict.

## §A1 — Amendment 1, dated 2026-09-12, AFTER the S1 and S2-U results were scored and ledgered

Precedent: `ADDENDUM_R82.md` §24 and `ADDENDUM_R81.md` §9A for the form. **This amendment is
post-result**: S1 and S2-U were scored at `f22ecdc` (2026-09-12) and their keys are written in
`side_experiments/NUMBERS_SIDE.md` §8. It is recorded with its reason so it cannot later be
read as a renegotiation of a result: it moves two frozen texts from the appendix to the main
text and changes nothing else.

**What the registration said.** §S1: "No sentence in Section 5.3 or Section 6 is changed on
S1's account without a ruling; the appendix table and, at most, one footnote at
`paper_v4.tex:1633` are the output cap." §S2: "The 42.3 percent sentence in Section 6
(`paper_v4.tex:641`) stays as printed either way. Under the second branch any qualification is
a ruling, recorded as an amendment, not a change made here." This is that ruling, taken by the
author on 2026-09-12 in the RESP-REG Phase A rulings (5).

**What changes — placement only.**
- **S1.** The frozen S1-P1 and S1-P2 held-readings and the A-MEM figures of
  `AUX-SIDE-S1-MINI-AMEM` (blind 0.5591, TRUE 0.4526, GT 0.8974; D = +0.4448, item-level
  [+0.3800, +0.5116], persona-clustered [+0.3875, +0.5042]) print in **Section 5.3** (after
  `paper_v6.tex:632`) and, as one restated sentence, in **Section 8** (`paper_v6.tex:744`), in
  addition to the appendix table. The Mem0 descriptive row prints beside in §5.3 in its frozen
  wording (49.4 percent coverage; gain +0.3006; no verdict). Proposed sentences:
  `reviews/RESP_REG_REPORT.md` §5 item 8.
- **S2-U.** The frozen not-expected-branch text ("Lifting the cap on the believed list, which
  raises its recall of ground-truth superseded names from 30.0 to 66.6 percent at unchanged
  precision, retains 65.5 percent of the TRUE gain, at or above the 60 percent threshold. Part
  of the believed-state loss recorded at 42.3 percent is an effect of the renderer's cap of
  fifteen names rather than of the store's metadata.") prints in **Section 6 immediately after
  the 42.3 percent sentence** (`paper_v6.tex:661`), with its intervals (item-level [44.6%,
  87.2%]; persona-clustered [31.5%, 93.6%]) and the weaker reading of the S2-U − BELIEVED
  difference stated beside it as §T rules (item-level [+0.0110, +0.0992] excludes zero;
  persona-clustered [−0.0019, +0.1173] includes it). The 42.3 percent sentence itself stays as
  printed. The U9 firewall stands: no connective joins the retention sentences to the text-match
  sentence that follows.

**What does not change.** Every frozen text, verbatim; every number, from `NUMBERS_SIDE.md` §8;
the verdicts (S1-P1 HOLDS, S1-P2 HOLDS; S2-U carries none); the Table 24 rows. **The abstract
and Section 1 stay as printed** under this amendment — the sentences carrying 42.3% / 60%
(`paper_v6.tex:55`, `:158`, `:743`) and the inversion (`:58`, `:159`, `:169`), the §5.3 heading
(`:615`) and its opener (`:618`), and §6 (`:681–684`). Any change there is a further ruling.

**Direction.** S2-U's placement is against the manuscript's interest: the 42.3 percent headline
is qualified in the section that carries it by a cap effect the registration expected not to
find. S1's placement cuts both ways and the text says so: it weakens "inverts at every scale"
as a statement about the store, and it supports the manuscript's thesis that the benefit is a
property of what the store is handed.

**Disposition.** R97 lands the sentences under authorization blocks in `CLAIMS.md`, citing
this amendment; `verify_side.py` is unaffected; no D-SIDE entry is opened, since a placement
ruling the registration anticipated is an amendment, not a deviation.
