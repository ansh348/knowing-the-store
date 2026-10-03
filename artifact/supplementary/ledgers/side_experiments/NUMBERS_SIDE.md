# NUMBERS_SIDE — ledger for the side experiments S1 and S2

Registration: `registrations/ADDENDUM_SIDE.md` (frozen at `e8b2630`, R95; baseline `35743cb`). Every number printed
for S1 or S2 enters the manuscript through a key in this file and no other way. Keys are
reserved in the registration's §L. Entries are dated. §1–§7 precede any elicitation; the monitor
rows of the two mini lanes enter in §8 (SIDE-BUILD-1 step 5).

---

## 1. AUX-SIDE-S1-SPOTCHECK — ruling (d), read complete 2026-09-12, before any elicitation

Sample: 30 mapped pairs per backend, `random.Random(42)` over the mapped pairs sorted by
(persona, backend entry id), frozen in `ADDENDUM_SIDE_DRAFT.md` §S1.a; texts in
`reviews/SIDE_REG_REPORT.md` appendix (Mem0 pairs 1–30 at L325–446, A-MEM pairs 1–30 at
L447–569). Pair numbers below are those.

**Criterion, frozen as read.** A pair is correct when the backend entry is about the same slot as
its mapped FR-Bank entry — same attribute, same subject. A value difference alone is not wrong. A
different subject, a different attribute, or an entry from which no single slot can be recovered
is wrong.

**Provenance.** Verdicts are the author's. The read was discussed with a language model; this is
disclosed in the registration's AI-use line.

| Key | Value |
|---|---|
| **AUX-SIDE-S1-SPOTCHECK-MEM0** | **17 / 30 correct, precision 0.567.** Borderline pairs (7): 3, 8, 11, 16, 19, 20, 21. **Below 0.80: the pre-specified fallback of §S1 step 2 fires.** Mem0's mapping becomes lexical-required; the Phase 1 census re-runs under it (§2 below) and rule (c) decides. Among the 16 lexically supported Mem0 pairs, 13 correct (0.81). The 13 wrong pairs are embedding-only or under cosine 0.55 in all but three (12, 18, 22). |
| **AUX-SIDE-S1-SPOTCHECK-AMEM** | **24 / 30 correct, precision 0.800.** Borderline pairs (7): 1, 3, 4, 9, 13, 17, 23. **Not below 0.80: the two-channel map stands on A-MEM; no fallback.** Among the 17 lexically supported A-MEM pairs, 16 correct (0.94). |
| **AUX-SIDE-S1-MULTI-AMEM** | 8 of the 30 A-MEM notes carry the mapped fact alongside other facts the index will not name: pairs 6, 7, 8, 11, 19, 20, 21, 28. Recorded as a stated reason the A-MEM GT index under-describes the store. |

## 2. AUX-SIDE-S1-FALLBACK-MEM0 — the lexical-required census on Mem0

Pending at the time of §1; filled below once the re-run completes (same session, before any
elicitation).

Re-run 2026-09-12, `census_s1_fallback.py` over the committed caches (`backend_entries/mem0.json`,
`backend_embeddings/mem0.npz`, `lifecycle_banks/*_embeddings.npz`), RENDERER LOCK identity 40/40
re-asserted before the census, no model call, 6.6 s.

| Key | Value |
|---|---|
| **AUX-SIDE-S1-FALLBACK-MEM0** | Lexical-required mapping on Mem0, 37 personas, 9,736 stored entries: **mapped 4,809 — 0.4939**; unmapped 4,927. Equals the pre-freeze lexical-supported count (0 lexical-only + 4,809 both) to the entry. **Rule (c): 0.4939 < 0.50 → S1 on Mem0 is a DESCRIPTIVE ROW**, reason "spot-check precision 0.567 under the two-channel map; lexical-required coverage 0.494". Per persona: 17 of 37 at or above 0.50; min 0.372, median 0.496, max 0.635; the 20 below: amara, billy, bruna, callum, david, diane, dmitri, elena, fatima, ingrid, joonho, kenji, leila, marcus, marley, mehmet, patrick, priya, tom, valentina. Frozen ambiguity (second candidate within 0.02 with a different `slot_key`, nearest wins): **1,214 — 25.2% of mapped**; any second candidate within 0.02 (descriptive): 1,519 — 31.6%; pre-freeze scrubbed-name variant, for continuity with the draft's table: 996 — 20.7%. GT index under the fallback: mean 54.1 lines / 814.9 o200k tokens against FR-Bank TRUE 63.2 / 1,074.1 on the same personas; lifecycle totals superseded 13 / retracted 3 / expired 74 against FR-Bank TRUE 97 / 21 / 264. The Mem0 INDEXED-GT arm still runs (238 calls) and prints, as descriptive, beside the A-MEM test rows. |
| **AUX-SIDE-S1-FALLBACK-AMEM** | — (the fallback did not fire; A-MEM stays on the two-channel map, §1) |

## 2a. AUX-SIDE-S1-AMBIG — the frozen slot-changing measure (ruling #3; D-SIDE-1)

Computed 2026-09-12 by `verify_side.py` under the frozen definition: a second FR-Bank candidate
within 0.02 cosine **of the target** whose `slot_key` differs; nearest wins. Rates are shares of
mapped entries. Written under the mapping each backend actually uses (ruling on D-SIDE-1).

| Key | Value |
|---|---|
| **AUX-SIDE-S1-AMBIG-MEM0** | **0.252** — lexical-required mapping (the map Mem0 uses after the spot-check; 1,214 of 4,809 mapped). Descriptive beside it: two-channel map, the map the spot-check did not admit, 0.2920 of 9,704 mapped. |
| **AUX-SIDE-S1-AMBIG-AMEM** | **0.4344** — two-channel map (the map A-MEM uses), of 10,974 mapped. |
| AUX-SIDE-S1-AMBIG-ANY-MEM0 (descriptive) | any second candidate within 0.02 of the target, regardless of slot: lexical-required 0.3159; two-channel 0.3410. |
| AUX-SIDE-S1-AMBIG-ANY-AMEM (descriptive) | 0.4736 under the two-channel map. |
| scrubbed-name variant, for D-SIDE-1 | target band 0.2461 (Mem0, two-channel) / 0.3763 (A-MEM); the registration's §C.1 row printed 0.2409 / 0.3648 under the global-best band. |

## 3. Keys reserved — all written

Every §L key is written: SPOTCHECK, MULTI, FALLBACK and AMBIG in §1–§2a; MAP and INDEXSIZE in
§4; S2-CENSUS and S2-CAP-RECALL in §5; the three LEAK keys in §6; the four NB keys in §7; the
MINI keys, H45, SPEND and BUDGETRULE in §8.

## 4. AUX-SIDE-S1-MAP and AUX-SIDE-S1-INDEXSIZE — the GT indexes built (SIDE-BUILD-1 step 1, 2026-09-12; `tools/build_s1.py`; no model call)

Built by `side_experiments/tools/build_s1.py` through `side_common.map_backend` (the §C.1 map,
moved verbatim out of `verify_side.py`; every census quantity stays pinned there) and the
RENDERER LOCK path (`index_v2.view` → `index_v2.render` under `AVAIL[("frbank","TRUE")]`,
`SLOT_CAP` 15). Gates at build, all passed, in order: `verify_side.py` (run as a subprocess
before any index was written); RENDERER LOCK identity 40 / 40; the sixty frozen §S1.a pairs
reproduced by the two-channel map on both backends — identity, target and channel 60 / 60, the
draw itself reproduced by `random.Random(42).sample` over the mapped pairs sorted by (persona,
entry id); the censuses under all three maps equal to the frozen values (§C.1, §2, §2a); no GT
index carries the inexpressibility marker or a name containing `:`. Re-running the build
reproduces every artifact byte for byte. Artifacts, `side_experiments/s1/`: `indexes_gt.json`
(77 indexes, keys `<backend>:<persona>:GT`), `mapping_gt.jsonl` (one record per stored entry
under the map its backend uses), `mapping_mem0_two_channel.jsonl` (Mem0 under the map the
spot-check did not admit; record only), `build_s1.json` (censuses, per-persona table, gate
outcomes). `verify_side.py` check I re-derives the 77 indexes from the committed caches and
compares them byte for byte on every run from here on.

| Key | Value |
|---|---|
| **AUX-SIDE-S1-MAP-MEM0** | **Lexical-required map** (the ruling #2 fallback; `AUX-SIDE-S1-SPOTCHECK-MEM0` 0.567), 37 personas, 9,736 stored entries: **mapped 4,809 — 0.4939**; channels lexical-only 0 / embedding-only 0 / both 4,809; unmapped 4,927. Per persona 17 of 37 at or above 0.50 (the 20 below are those listed under `AUX-SIDE-S1-FALLBACK-MEM0`). **Frozen ambiguity, re-asserted at build against §2a:** slot-changing **1,214 — 0.252** of mapped (`AUX-SIDE-S1-AMBIG-MEM0`); any second candidate within 0.02 of the target 1,519 — 0.3159 (`AUX-SIDE-S1-AMBIG-ANY-MEM0`); scrubbed-name variant 996 — 0.2071. Lifecycle totals in the GT indexes, superseded / retracted / expired / supersession events **13 / 3 / 74 / 16** against FR-Bank TRUE 97 / 21 / 264 / 43 on the same personas. Mem0 points carrying `updated_at` (1,276 in the cache) → target state under this map: active 861, superseded 8, retracted 3, expired 8, unmapped 396 (descriptive; under the two-channel map 1,216 / 9 / 3 / 16, the §C.1 row). **Rule (c): 0.4939 < 0.50 — the Mem0 arm is a DESCRIPTIVE ROW** (§2). Descriptive beside it, the two-channel map the spot-check did not admit: mapped 9,704 — 0.9967, slot-changing ambiguity 0.2920, any-second 0.3410, lifecycle 20 / 6 / 138. |
| **AUX-SIDE-S1-MAP-AMEM** | **Two-channel map** (`AUX-SIDE-S1-SPOTCHECK-AMEM` 0.800; no fallback), 40 personas, 11,319 stored entries: **mapped 10,974 — 0.970** (0.9695); channels lexical-only 5 / embedding-only 4,962 / both 6,007; unmapped 345. Every persona at or above 0.50. **Frozen ambiguity, re-asserted at build against §2a:** slot-changing **4,767 — 0.4344** of mapped (`AUX-SIDE-S1-AMBIG-AMEM`); any second candidate within 0.02 of the target 5,197 — 0.4736 (`AUX-SIDE-S1-AMBIG-ANY-AMEM`); scrubbed-name variant 4,129 — 0.3763. Lifecycle totals in the GT indexes **40 / 13 / 123 / 34** against FR-Bank TRUE 104 / 23 / 276 / 46. Lexically supported share 6,012 — 0.531, for the record (§S1 step 2; it plays no role). **Rule (c): 0.970 ≥ 0.50 — the A-MEM arm is the registered test** (S1-P1, S1-P2). **MULTI note, carried from `AUX-SIDE-S1-MULTI-AMEM` (§1):** 8 of the 30 spot-checked A-MEM notes (pairs 6, 7, 8, 11, 19, 20, 21, 28) carry the mapped fact alongside other facts the index will not name — one entry maps to one target, so the GT index names one slot per note and under-describes what the store holds; this is the stated reason and it carries no prediction. |
| **AUX-SIDE-S1-INDEXSIZE** | Mean lines / o200k tokens per GT index, against FR-Bank TRUE FULL on the same personas. **Mem0 (lexical-required): 54.1 lines / 814.9 tokens** vs 63.2 / 1,074.1 (37 personas). **A-MEM (two-channel): 57.8 lines / 931.0 tokens** vs 63.2 / 1,077.1 (40 personas). The GT indexes run 259 (Mem0) and 146 (A-MEM) o200k tokens shorter than the committed TRUE index of the same persona; the §B projection took the gap at about 150 for both, so the Mem0 lane will bill under it. The Mem0 two-channel index, not used, was 57.8 / 918.8. |

**§S1.a, a labelling note recorded at build (D-SIDE-2).** The cosine column of the frozen
spot-check sample is the *global-best* cosine over the persona's FR-Bank entries, the quantity
the pre-freeze census keyed on (D-SIDE-1), not the cosine to the lexical target; the two differ
on 10 of the 60 pairs (Mem0 12, 18, 22, 24; A-MEM 6, 8, 9, 11, 15, 19), on every one of which
the lexical target sits below the global argmax. Identity, target and channel of all 60 pairs,
and the draw, reproduce exactly; the pair texts the author read and the verdicts of §1 are
unaffected. `build_s1.json["spotcheck_section_S1a"]` lists both cosines for the ten.
**Ruled 2026-09-12: a labelling error in the printed sample; the verdicts were on the texts and
stand; registration untouched.** The ten, printed (global-best) beside the target-band cosine:

| §S1.a cosines, for D-SIDE-2 | pair | persona → target | printed (global best) | target band | verdict (§1) |
|---|---:|---|---:|---:|---|
| Mem0 | 12 | aroha cdae3aed → lb_00056 | 0.740 | 0.590 | wrong (one of the three wrong pairs at or above 0.55) |
| Mem0 | 18 | aroha 74dd4910 → lb_00198 | 0.472 | 0.410 | wrong (one of the three) |
| Mem0 | 22 | omar 3fc6974d → lb_00341 | 0.639 | 0.398 | wrong (one of the three) |
| Mem0 | 24 | patrick 8e79e8aa → lb_00173 | 0.771 | 0.677 | correct |
| A-MEM | 6 | elena a52fba76 → lb_00244 | 0.618 | 0.468 | correct; MULTI |
| A-MEM | 8 | bruna e1a6df91 → lb_00440 | 0.641 | 0.576 | correct; MULTI |
| A-MEM | 9 | rosa 3961ab8e → lb_00461 | 0.652 | 0.389 | **WRONG regardless** (author, on the ruling); listed borderline in §1 |
| A-MEM | 11 | samuel e48fca2b → lb_00390 | 0.388 | 0.274 | correct; MULTI |
| A-MEM | 15 | bruna 6d5961a3 → lb_00502 | 0.567 | 0.546 | correct |
| A-MEM | 19 | thanh 83812823 → lb_00237 | 0.686 | 0.575 | correct; MULTI |

Verdict column, derived from §1 and the ruling, no verdict re-read: §1 names Mem0's three
wrong pairs at or above cosine 0.55 as 12, 18, 22 and puts every other wrong Mem0 pair below
0.55 or embedding-only, so pair 24 (lexical, 0.771) is correct; on A-MEM §1 counts one wrong
pair among the 17 lexically supported, and the author's statement on the ruling makes that pair
9, so 6, 8, 11, 15 and 19 (all lexically supported) are correct. The totals in §1 govern.

## 5. AUX-SIDE-S2-CENSUS, AUX-SIDE-S2-CAP-RECALL and the S2-U index built (SIDE-BUILD-1 step 2, 2026-09-12; `tools/build_s2u.py`; no model call)

Built by `side_experiments/tools/build_s2u.py`: each of the 661 committed obligation items'
BELIEVED store version through the frozen `index_v2.render` under `AVAIL[("frbank","BELIEVED")]`
with `SLOT_CAP` lifted. **Settled reading, disclosed:** the pinned renderer is parametric in one
knob, `SLOT_CAP`, which both slices every bucket and prints the header note "names only, max N
per category, alphabetical"; the cap is lifted by setting `SLOT_CAP = 100`, the smallest power
of ten above the largest bucket on the 661 items (86 names; largest superseded-names set 50), so
the header reads "max 100 per category" and the cap never binds. Gates, all passed: `verify_side.py`
before any index was written; **RENDERER LOCK — the same render at `SLOT_CAP = 15` reproduces
the committed BELIEVED text byte for byte on 661 / 661**; no S2-U text carries `(+N more)`, the
inexpressibility marker, or a name containing `:`; the rendered superseded list under S2-U
parsed by `index_features.parse` reproduces §C.2's uncapped columns. Re-running reproduces
every artifact byte for byte. Artifacts, `side_experiments/s2/`: `indexes_s2u.json` (242 texts —
40 FULL, 40 CAT-ABLATED, 162 SLOT-ABLATED — keyed `<index key>:S2U`, with the 661-item map),
`build_s2u.json`. `verify_side.py` check J re-renders all 661 and compares byte for byte from
here on.

| Key | Value |
|---|---|
| **AUX-SIDE-S2-CENSUS** | The §C.2 census, frozen as S2's result (ruling #4), every value re-derived at build (`verify_side.py` check D for the rule table; `build_s2u.py` gate 3 for the store facts). Rendered superseded list, micro-averaged over the 661 items, names / item · precision · recall: **TRUE 1.7474 · 1.000 · 1.000; BELIEVED (cap 15) 15.0378 · 0.0348 · 0.2996; BR-A 15.0378 · 0.0348 · 0.2996; BR-B 8.9592 · 0.0618 · 0.3169**; uncapped name sets BELIEVED 32.55 · 0.0357 · 0.6658, BR-A 32.51 · 0.0358 · 0.6658, BR-B 9.15 · 0.0633 · 0.3316 (§C.2 table; verify_side pins the rendered rows). **No candidate reaches precision 0.80; no rule is fixed; the precision repair is withdrawn.** Store facts, recomputed from the banks and the TRUE join: **5,968** entries inactive, **5,725** `supersedes` pointers, **104** TRUE-superseded entries of which **40 are still active** in the store; a same-slot successor points at every one of the 64 inactive TRUE-superseded entries and at 5,661 of the 5,904 other inactive entries. |
| **AUX-SIDE-S2-CAP-RECALL** | The cap effect S2-U measures. The BELIEVED superseded list holds **66.6%** of TRUE's names uncapped (micro-recall **0.6658**, 32.55 names / item) and **30.0%** as rendered under the cap of 15 (**0.2996**, 15.0378 names / item); precision 0.0357 uncapped, 0.0348 rendered. The S2-U render reproduces the uncapped figures exactly (32.5477 / 0.0357 / 0.6658 through NB-6's parser). A renderer effect, not a metadata rule. |
| S2-U index size (for the §B projection) | Mean per item **1361.7 o200k tokens / 72.3 lines** against the committed BELIEVED 1061.9 / 61.8 (max S2-U 1,925 tokens). The lift adds about 300 tokens, twice the 150 the §B projection assumed **[est]**; at the committed means that puts the 661-call lane near $0.52 rather than $0.48, inside the $2 rule by a wide margin. |

## 6. AUX-SIDE-S1-LEAK and AUX-SIDE-S2-LEAK — the leakage screens (SIDE-BUILD-1 step 3, 2026-09-12; `tools/leak_side.py`; 90 mini calls + 1 probe)

`ladder_e1.py` level 0, unchanged (working-tree blob equals HEAD's, `64e08ad90446`),
run by `leak_side.py` with only the index text swapped: the ladder's own sampler (FULL PRESENT
items per backend from `items_pre.json`, sorted by item id, `random.Random(42).sample(pool, 30)`),
asserted equal to the committed screen's 30 items per backend in `ladder_L0.json`; the frozen
`LEAKAGE_SYSTEM` / `LEAKAGE_USER` pair, digests asserted; `api.call` (`gpt-4.1-mini`, temperature 0,
seed 42, max_tokens 200, JSON mode), responses cached under `side_experiments/cache/`; scored by
`exp4_witnesses.supports_correct(response, correct_answer)`, a literal UNKNOWN never correct.
Served identifier probed first through the same client: `gpt-4.1-mini-2025-04-14`. Cells: the
Mem0 items against their persona's GT index under the lexical-required map; the A-MEM items
against the two-channel GT index; the FR-Bank items against `frbank:<p>:FULL:S2U` — the
committed `frbank:BELIEVED` cell with the cap lifted, paired item for item. Index digests:
`indexes_gt.json` `18095591689e`, `indexes_s2u.json` `f05e95565c82`.
Rows, D18 dump and cost in `side_experiments/leak/leak_side.json`.

| Key | Value |
|---|---|
| **AUX-SIDE-S1-LEAK-MEM0** | **0 / 30 correct — PASS** (threshold: more than 3 of 30 is a STOP); non-UNKNOWN answers 3 / 30, parse failures 0; D18 band not entered. Paired committed cell `mem0:TRUE` (`ladder_L0.json`): 0 / 30, non-UNKNOWN 0 / 30. |
| **AUX-SIDE-S1-LEAK-AMEM** | **0 / 30 correct — PASS** (threshold: more than 3 of 30 is a STOP); non-UNKNOWN answers 1 / 30, parse failures 0; D18 band not entered. Paired committed cell `amem:TRUE` (`ladder_L0.json`): 0 / 30, non-UNKNOWN 0 / 30. |
| **AUX-SIDE-S2-LEAK** | **0 / 30 correct — PASS** (threshold: more than 3 of 30 is a STOP); non-UNKNOWN answers 1 / 30, parse failures 0; D18 band not entered. Paired committed cell `frbank:BELIEVED` (`ladder_L0.json`): 0 / 30, non-UNKNOWN 1 / 30. |
| leakage-screen cost (toward `AUX-SIDE-SPEND`) | 90 calls, 104,117 prompt / 807 completion tokens, **$0.0429**; served-identifier probe $0.0004; **$0.0433** billed. §B projected $0.04 + $0.02 **[est]**. |

## 7. AUX-SIDE-S1-NB4 and AUX-SIDE-S1-NB5 — the mechanical readers on the GT indexes (SIDE-BUILD-1 step 4, 2026-09-12; `tools/nb_side.py`; local, $0)

Ruling #7. NB-4 (maximum content-token Jaccard between the question and each attribute name the
index exposes) and NB-5 (maximum cosine under `sentence-transformers/all-MiniLM-L6-v2` from the
local cache, offline) as `e1r_robustness/SPEC_E1R.md` (b) defines them and `run_baselines.py`
implements them, on every GT index (`indexes_gt.json` `18095591689e`), over the
committed FOK populations joined as `common_e1r.assemble` joins them (the committed blind and
INDEXED-TRUE AUROC reproduce from the same join to 1e-9). Scored directly, unsupervised, no fold.
**NB-6 does not run on the GT indexes.** The GT index names a mean 69.9 (Mem0) /
95.1 (A-MEM) attributes per item. Per-item scores in `side_experiments/s1/nb_side.json`.

| Key | Value |
|---|---|
| **AUX-SIDE-S1-NB4-MEM0** | **AUROC 0.7104** on the R-FOK-MEM0 population (n 238, 94 positive, 37 personas), persona-clustered interval [0.6627, 0.7588] (1000 draws); mean score 0.080, share of items scoring 0 0.618. Committed NB-4 on the paper's TRUE index of this backend: 0.50 (attribute names inexpressible there). Committed monitor on the same items: blind 0.5746, INDEXED-TRUE 0.4777 (gain -0.0969). Prints beside the S1 monitor row; carries no prediction. |
| **AUX-SIDE-S1-NB4-AMEM** | **AUROC 0.7000** on the R-FOK-AMEM population (n 284, 126 positive, 40 personas), persona-clustered interval [0.6572, 0.7429] (1000 draws); mean score 0.086, share of items scoring 0 0.585. Committed NB-4 on the paper's TRUE index of this backend: 0.50 (attribute names inexpressible there). Committed monitor on the same items: blind 0.5591, INDEXED-TRUE 0.4526 (gain -0.1065). Prints beside the S1 monitor row; carries no prediction. |
| **AUX-SIDE-S1-NB5-MEM0** | **AUROC 0.8700** on the R-FOK-MEM0 population (n 238, 94 positive, 37 personas), persona-clustered interval [0.8226, 0.9123] (1000 draws); mean score 0.330, share of items scoring 0 0.000. Committed NB-5 on the paper's TRUE index of this backend: 0.50 (attribute names inexpressible there). Committed monitor on the same items: blind 0.5746, INDEXED-TRUE 0.4777 (gain -0.0969). Prints beside the S1 monitor row; carries no prediction. |
| **AUX-SIDE-S1-NB5-AMEM** | **AUROC 0.8554** on the R-FOK-AMEM population (n 284, 126 positive, 40 personas), persona-clustered interval [0.8067, 0.9008] (1000 draws); mean score 0.349, share of items scoring 0 0.000. Committed NB-5 on the paper's TRUE index of this backend: 0.50 (attribute names inexpressible there). Committed monitor on the same items: blind 0.5591, INDEXED-TRUE 0.4526 (gain -0.1065). Prints beside the S1 monitor row; carries no prediction. |

Reading, descriptive: the manifest's names carry the presence signal a mechanical reader can
use — both readers sit well above their 0.50 on the paper's name-less TRUE index and above the
committed monitor on either arm. Whether the monitor reads that signal is what the S1 mini rows
measure (§8).

## 8. AUX-SIDE-S1-MINI, AUX-SIDE-S2-MINI, AUX-SIDE-SPEND, AUX-SIDE-BUDGETRULE — the mini lanes (SIDE-BUILD-1 step 5, 2026-09-12; `tools/run_side.py`; 1,183 calls + 2 probes on gpt-4.1-mini)

`run_side.py build → probe → project → run → score`. Populations asserted at build (Mem0 238 / 94,
A-MEM 284 / 126, the 661 / 104), joined to the committed rows exactly as `common_e1r.assemble`
joins them; blind (by question), INDEXED-TRUE and INDEXED-BELIEVED (by tag) read from
`elicitation_main.json`, never re-elicited. The E1 protocol of `elicit_e1.py`: `api.call`
(`gpt-4.1-mini`, temperature 0, seed 42, max_tokens 200, JSON mode), `prompts_e1.SYSTEM` +
`USER_INDEXED`, both digests asserted (`337d37d3…` / `35d9b968…`), the E1 clamp, one retry on a
parse failure; k = 1; synchronous, 8 workers; served identifier probed per arm before launch:
`gpt-4.1-mini-2025-04-14`. Index digests as in §6. Estimators (§T): `common_e1r.auroc`,
`boot_item` (registered interval), `boot_cluster` beside; the retention ratio bootstrapped
under the same draw scheme (`run_side.boot_ratio`; draws with a non-positive TRUE gain
discarded and counted: 0 item-level, 0 clustered). Rows in
`side_experiments/run/rows_side.jsonl`; scores in `scores_side.json`.

| Key | Value |
|---|---|
| **AUX-SIDE-S1-MINI-AMEM** | **Registered test** (two-channel map; spot-check 0.800; rule (c) 0.970). n 284 (126 positive, 40 personas; 284 of 284 items scored under INDEXED-GT (paired on those); 0 elicitation failures). FOK AUROC: **blind 0.5591, INDEXED-TRUE 0.4526, INDEXED-GT 0.8974** (blind and TRUE from the committed rows). Gains: X = TRUE − blind **-0.1065** [-0.1726, -0.0403]; Y = GT − blind **+0.3383**, item-level [+0.2673, +0.4122], persona-clustered [+0.2791, +0.3976]. Paired difference D = GT − TRUE per item **+0.4448**, item-level [+0.3800, +0.5116], persona-clustered [+0.3875, +0.5042] (1,000 draws each, seed 42, no draw discarded). **S1-P1 HOLDS** (D > 0.05 with the paired interval excluding zero; item-level holds, clustered holds; the two agree). **S1-P2 HOLDS** (the GT gain's interval does not lie below zero; item-level holds, clustered holds; the two agree). Frozen readings, appendix only: S1-P1 held — *"Given the manifest's names for what it holds, the store no longer inverts the benefit by the margin it did; the inversion was a property of the index the store was handed, not of the store alone."* S1-P2 held — *"The name-bearing index does not invert."* No sentence in Section 5.3 or Section 6 changes on S1's account without a ruling; the output cap is the appendix table and at most one footnote at `paper_v4.tex:1633`. NB-4 / NB-5 beside (§7): 0.7000 / 0.8554. |
| **AUX-SIDE-S1-MINI-MEM0** | **Descriptive row** (spot-check 0.567 → lexical-required map → coverage 0.494 < 0.50; no verdict). n 238 (94 positive, 37 personas; 238 of 238 items scored under INDEXED-GT (paired on those); 0 elicitation failures). FOK AUROC: **blind 0.5746, INDEXED-TRUE 0.4777, INDEXED-GT 0.8751** (blind and TRUE from the committed rows). Gains: X = TRUE − blind **-0.0969** [-0.1686, -0.0250]; Y = GT − blind **+0.3006**, item-level [+0.2208, +0.3728], persona-clustered [+0.2429, +0.3669]. Paired difference D = GT − TRUE per item **+0.3975**, item-level [+0.3218, +0.4747], persona-clustered [+0.3327, +0.4617] (1,000 draws each, seed 42, no draw discarded). Frozen text, prints regardless: *"On Mem0 the name-bearing index could be built for 49.4 percent of the store's entries under the lexical-required mapping the spot-check forced (two-channel precision 0.567); below the registered coverage floor of one half, its coverage gain of +0.3006 (interval [+0.2208, +0.3728]; TRUE -0.0969) is reported and carries no verdict."* NB-4 / NB-5 beside (§7): 0.7104 / 0.8700. |
| **AUX-SIDE-S1-H45** | — (no committed Haiku 4.5 blind or TRUE rows exist on the external items — `r74/x4/rows_H45.jsonl` covers `cell_661` only — so under "blind arms are the committed rows, never re-run" the lane has nothing to pair against; the S1 Haiku lane moves to October, §S1 / §B). |
| **AUX-SIDE-S2-MINI** | **Descriptive, no pass bar.** n 661 (104 PN, 40 personas; 661 of 661 items scored under S2-U (all four arms paired on those); 0 elicitation failures). NOK AUROC: **blind 0.4946, TRUE 0.7339, BELIEVED 0.5959, S2-U 0.6513** (the first three from the committed rows). Paired gains over blind: TRUE **+0.2393** [+0.1801, +0.2949]; BELIEVED **+0.1012** [+0.0458, +0.1543]; S2-U **+0.1567**, item-level [+0.0961, +0.2162], persona-clustered [+0.0552, +0.2536]. **Retention (S2-U − blind) / (TRUE − blind) = 65.5%**, item-level [44.6%, 87.2%], persona-clustered [31.5%, 93.6%], against the committed BELIEVED retention 42.3% (recomputed from the committed rows 42.3%) and the 60% line; the point estimate clears the line, the item-level interval spans it and the clustered interval spans both the line and 42.3%. Paired S2-U − BELIEVED **+0.0554**, item-level [+0.0110, +0.0992] (excludes zero), persona-clustered [-0.0019, +0.1173] (includes zero) — the two intervals disagree and the weaker reading is said beside the figure (§T). **Branch: retention reaches 60% (not expected).** Frozen text, appendix only: *"Lifting the cap on the believed list, which raises its recall of ground-truth superseded names from 30.0 to 66.6 percent at unchanged precision, retains 65.5 percent of the TRUE gain, at or above the 60 percent threshold. Part of the believed-state loss recorded at 42.3 percent is an effect of the renderer's cap of fifteen names rather than of the store's metadata."* **The 42.3 percent sentence at `paper_v4.tex:641` stays as printed; under this branch any qualification is a ruling, recorded as an amendment, not a change made here.** |
| **AUX-SIDE-SPEND** | **$0.8904 billed** on the OpenAI key, all on `gpt-4.1-mini`: leakage screens $0.0433 (90 calls + 1 identifier probe, §6), lane probes $0.0016 (2 calls), S1 + S2-U run $0.8455 (1,183 calls, 0 retries). §B projected $0.85 (×1.3 $1.11); the pre-launch projection from the probes was $0.99 + $0.05 billed. No Haiku call, no Opus call; the Anthropic key not touched. |
| **AUX-SIDE-BUDGETRULE** | The §B rule, frozen: the mini lanes and the two leakage screens under $2 in total, unconditional; no Haiku lane under this registration; Opus not run. **Held**: $0.8904 < $2.00 with every cell scored; `run_side.py run` stops submitting at the line and did not reach it. |
