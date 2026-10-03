# PREREG ADDENDUM — E1.8 STEP 2, MECHANISM PROBE

**Dated:** 2026-08-11 · **Extends:** `E1_7_ADDENDUM.md` (`6860ad0`).
`PREREG_E1.md` (`875f726`) and `AMENDMENT_1_E1.md` (`307865f`) are unchanged.
**Supersedes nothing.**

**Statement of prior data contact.** **No A1, A2 or A3 elicitation call of any kind has been
made.** The arms below were *built* before this file was committed, deliberately, so that the
frozen constants could be stated here as numbers rather than described as a procedure; the builder
(`tools/mechanism_arms.py`) reads only `indexes_v2.json` and `build/items_final.json`, and touches
no model response, no score and no outcome. It uses labels only to select the pre-registered
scoreable hard tier, exactly as `score_e1.py` already does.

The intact-index and blind results are of course already known — they are the reference this probe
is measured against, and are quoted below from `results/scores_e1.json` as committed at `5c5bae8`.

---

## The question

The E1 headline is a **+0.2272 hard-tier FOK delta** from a metadata index. The standing objection
is that the model is *"reading a table you built"* — that the index is an oracle in disguise. The
hard tier is built largely from **slot-ablated** stores, where removing the gold slot barely moves
any category count, so if counts were the whole signal the effect should not survive there. It
does. **Which channel carries it?**

Three arms, each destroying a different amount of count information while leaving everything else
byte-identical. If discrimination survives with counts corrupted, the signal is the
**category-coverage map × question-specificity** — a *structural* channel, not a numeric one, and
one that cannot be an oracle because it contains no values. If discrimination collapses as counts
are destroyed, the counts are load-bearing and the leakage question reopens.

---

## Item set — and one resolution recorded before the run

The instruction names *"the FR-Bank hard tier (272 items)"* and gives the reference as
*"the intact-index 0.7530"* against *"blind (0.5258)"*. Those two things are not the same slice,
and the frozen interpretation rule is stated as a distance from that reference, so the mismatch is
load-bearing and is resolved here rather than after scoring.

| slice | n | composition | blind | intact indexed |
|---|---|---|---|---|
| FR-Bank hard tier, ABSENT only | **272** | 127 slot-ABSENT + 145 natural-absent | — | — |
| FR-Bank hard tier, scoreable | **307** | 272 ABSENT + 35 PRESENT-NEGATIVE | 0.4966 | 0.7003 |
| **pooled hard tier, scoreable** | **588** | 307 FR-Bank + 145 A-MEM + 136 Mem0 | **0.5258** | **0.7530** |

**272 is the count of ABSENT items in the FR-Bank hard tier.** A FOK AUROC needs both classes, so
the smallest evaluable FR-Bank slice is **307**. And **0.7530 / 0.5258 are the *pooled* hard-tier
figures (n=588)**, the study's headline row — every positive in it is an FR-Bank PN item, which is
why the pooled row exists at all.

**Resolution: run all three arms on the pooled hard tier, n = 588.** It is a superset of both
candidate readings, it makes the instruction's own reference numbers apply exactly, and it costs
1,764 calls instead of 921 — a difference of about $0.45. **No choice is forced and nothing is
narrowed.**

- **PRIMARY row: pooled hard tier, n = 588**, reference **intact 0.7530 / blind 0.5258**. The
  frozen interpretation rules below are read off this row.
- **SECONDARY row: FR-Bank hard tier, n = 307**, reference **intact 0.7003 / blind 0.4966**. The
  same rules are reported against the arm-matched reference, and any disagreement between the two
  rows is reported as observed.
- Also reported, descriptively: the **slot-ablated slice** (162 items) alone, since it is the
  subset the mechanism question is actually about.

Logged as **D26-E1**.

---

## The three arms

Base for all three is the **intact TRUE index**, unchanged. One manipulation each, applied to
**counts only**.

**What is a count** — the complete rule, no discretion left:

| site | field |
|---|---|
| header | `entries in this store: N` |
| LIFECYCLE TOTALS | active / superseded / retracted / expired / supersession events |
| PER-CATEGORY BREAKDOWN | `ENTRIES`, `ACTIVE`, `SUPRSD`, `RETRACT`, `EXPIRED` |
| AGE DISTRIBUTION | the five band counts |
| attribute-name blocks | the `(+N more)` overflow |

**Ages are not counts.** The per-category `NEWEST` / `OLDEST` columns and the whole `RECENCY` block
(newest / oldest / median entry age) are **byte-identical in all four texts** — asserted, not
intended. Recency is therefore held constant and each arm remains single-channel. The
`not expressible by this backend` marker is not a count and is never altered.

Over the 276 hard-tier index keys there are **14,479 count sites**, 5,836 of them zero, across
**67 distinct count slots**.

### A1 — counts-jittered

`count → round(count × m[slot])`, round-half-up, with `m ~ U[0.5, 2.0]` drawn once per slot from
`random.Random(42)` and applied **identically to every item** ("same jitter across items"). Frozen
multipliers span **0.5097 – 1.9843** over the 67 slots and are recorded in
`mechanism_indexes.json`.

A slot is `total_entries`, `lifecycle.<state>`, `percat.<CATEGORY>.<COLUMN>`, `agedist.<band>`, or
`name_overflow`. Slot identity is stable across personas because the category ontology is fixed.

**Two properties of this specification, disclosed now rather than discovered later:**

1. Because a slot's multiplier is constant across items, **A1 preserves within-slot ordering across
   items** — it corrupts magnitudes and cross-field ratios, not the cross-item rank of any single
   field. That is what the instruction specifies and it is implemented as specified.
2. Independent per-slot multipliers **break internal arithmetic coherence** — a jittered `active`
   can exceed a jittered store total. A1 therefore destroys magnitude *and* introduces incoherence.
   If A1 degrades, those two causes are not separable by this design, and the report will say so.

### A2 — counts-coarsened

`count → "0" | "few" | "many"`, with **T = 28**: `0 → "0"`, `1..28 → "few"`, `>28 → "many"`.

T is the **median of every nonzero count in the intact hard-tier indexes** (8,643 values, range
1–622). The rule is label-blind by construction: it is computed from index text alone and can
never be tuned toward an outcome.

### A3 — names-only

Every count replaced by `-`. Category names, lifecycle-state names, attribute names, the marker and
all age fields are retained. This is the only arm that also destroys **zero-ness** — A1 and A2 both
preserve `0` exactly (asserted).

The ladder therefore destroys strictly more at each rung: **magnitude corrupted → magnitude
coarsened → magnitude and zero-ness both gone.**

### Build assertions (all PASS, enforced at build time)

1. re-masking every count in an arm reproduces the intact index's masked form exactly — **nothing
   but counts moved**;
2. A1 preserves zero-ness at every site;
3. A2 preserves zero-ness at every site;
4. A3 leaves no count anywhere;
5. the `RECENCY` block and every `NEWEST`/`OLDEST` value are byte-identical across all four texts.

---

## Elicitation

- **`gpt-4.1-mini` lane only.** No frontier call.
- Frozen `prompts_e1.py`, **`USER_INDEXED` unchanged** — only the index text differs. Prompt-texts
  sha verified at run time.
- temperature 0, seed 42, max_tokens 200; cache keyed `(item_id, arm, model, prompt_hash)`.
- **k = 1.** Licensed by this lane's measured stability: the E1 k=3 subsample gave **46/50
  questions identical across three draws, mean spread 0.012**. Noted as required: that measurement
  was taken on the **blind** arm; decoding parameters are identical on the indexed arm, and the
  indexed arm is the longer, more constrained prompt.
- 588 items × 3 arms = **1,764 calls**. Projected **≈ $0.92** at the study's own rates.
- **Hard cap $5.** Stop and report if the projection exceeds it.

---

## Scoring and the frozen interpretation rules

Scored with the E1 procedure unchanged: rank-based AUROC with ties at 0.5, positive class =
NON-ABSENT, plus ECE and Brier; paired bootstrap, 1,000 resamples, seed 42, items resampled.
Reported per arm: AUROC, delta vs the **intact** index (with paired CI), and delta vs **blind**
(with paired CI).

**Frozen, and read mechanically off the PRIMARY row:**

> **If A1/A2/A3 all remain within 0.05 of the reference (0.7530)** — the signal is the
> **category-coverage map × question-specificity, counts not load-bearing**. This **ANSWERS the
> "reading a table you built" objection with a mechanism.**
>
> **If discrimination collapses toward blind (0.5258) as count information is destroyed, with an
> A1 > A2 > A3 ordering** — **counts are load-bearing and the leakage question REOPENS.** Reported
> in those words.
>
> **Mixed or non-monotone** — **mechanism partially resolved**; report the pattern, **no forced
> story.**

The two clauses are not exhaustive; anything that is neither is the third case.

## Leakage note, re-stated

The **0/30 index-leakage control was run on the intact index** at ladder level 0 and returned zero
leaks on every backend and provenance. **A1–A3 inherit its value-scrubbing unchanged**: they
rewrite integers and nothing else, so no attribute *value* can enter through them — assertion 1
above is exactly that guarantee. Each arm carries **strictly less** information than the intact
index it was derived from, so the control transfers a fortiori and is **not re-run**.

## Scope fence

No E2 elicitation. No frontier call. No paper-text edit. No prompt change outside the three
registered arms. **Any non-routine deviation stops the run before scoring.**
