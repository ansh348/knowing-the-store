# ADDENDUM_PAD — descriptive probe on the length of the superseded-names list: the TRUE list padded with correct names to 15, 30 and 60

Written 2026-09-13 (program R104, the v11-to-v12 pass), BEFORE any call. Descriptive: this
addendum carries **no prediction, no bar and no verdict**; the branches of §5 are enumerated in
advance and every number prints whichever way it comes out, in Appendix D beside the
superseded-names lookup rows and in one sentence of Section 5 (the portability paragraph). It is
frozen by its sha256, recorded in `iclr2027_monitoring_submission/CLAIMS.md` (R104 block) and in
`pad_probe/NUMBERS_PAD.md` before the first call. Nothing here re-adjudicates NB6-1, NB6-2, the
SIDE S2 census or any registered item; the committed TRUE and BELIEVED rows are read and never
re-run.

## §1 — Question

The TRUE superseded-names list averages 1.75 names per item (`AUX-E1R-NB6`) and the only long-list
evidence in the paper is the BELIEVED list (15.04 names per item, 32.55 with the cap lifted), which
confounds list length with wrongness: the BELIEVED names are mostly not superseded in truth
(precision 0.035, `AUX-SIDE-S2-CENSUS`). Does the superseded-names lookup, and does GPT-4.1 mini,
read the obligation off a list that is long but not wrong? The probe pads every TRUE list with
attribute names that are real names of the persona's store (and, where those run out, of other
personas' stores) but that no scored question of the persona targets, so that length varies and
the labelled content of the list does not.

## §2 — Population

The **661 obligation items** of the main study (`common_e1r.POPULATIONS["R-NOK-FRB"]`; 104 PN =
63 supersession / 26 retraction / 15 expiry; 174 PRESENT; 383 ABSENT; 40 personas), resolved to
their committed TRUE summary texts by `index_features.index_key` (**242 distinct keys** of
`e1_metamemory/indexes_v2.json`). The recorded rows this probe is paired against, read and never
re-run: GPT-4.1 mini's `INDEXED-TRUE` obligation score (`e1_metamemory/elicitation_main.json`;
AUROC 0.7339 on the 661) and the superseded-names lookup on the committed TRUE section
(`run_nb6.emb_scores` 0.7484, `run_nb6.lex_scores` 0.5738; `AUX-E1R-NB6`, reproduced at build as
the gate). The BELIEVED rows print beside as the reference for the third branch and are never
re-run: mini 0.5959, embedding lookup 0.5858, lexical lookup 0.4718 (`AUX-E1R-NB6`, `AUX-E1R-BELIEVED-NOK`).

## §3 — Construction (deterministic, no model call)

**The padded section.** For each of the 242 keys and each target length **L ∈ {15, 30, 60}**, the
superseded-names section of the committed TRUE text is re-rendered over the committed list plus
padding names, under the v2 name-block grammar (`index_v3._name_block`: sorted set, wrap 150,
indents two and four spaces) with the per-bucket cap lifted to 100 as the SIDE S2-U build lifted
it (`SLOT_CAP_LIFTED`), so that every name prints and no `(+N more)` appears at any length. The
text above the section header is byte-identical to the committed text (the section is the tail of
every TRUE text, `AUX-RESP-L1-LOCK`). **The committed names are kept, the target's own name among
them**; a key whose committed section reads `(none)` receives L padding names and no committed
name. The padded list has exactly L names; a committed list longer than L (none exists: the
longest is 9) would be a STOP.

**Padding names, in draw order, under `random.Random(f"42:{key}:{L}")`, shuffled once per key and
length and taken in order so that the 15-name list is a prefix of the 30-name list and that of the
60-name list:**

1. **Pool A, the persona's own attributes**: every attribute name printed in the per-category
   name map of the same committed TRUE text (`index_features.parse` `attr_by_cat`, all buckets),
   excluding (i) every name in the committed superseded section, (ii) every scrubbed slot that any
   of the persona's 661-cell items targets — the `pn_members` slots of its PN items and the gold
   slots of its PRESENT items (`ds_common.pn_slots`, `ds_common.load_cell` `gold`, resolved to
   slots through `true_flags`), and (iii) any name containing `:`.
2. **Pool B, other personas' attributes**, used only after pool A is exhausted: every attribute
   name printed in the per-category name map of every other persona's `frbank:<persona>:FULL:TRUE`
   text, excluding any name that appears anywhere in this persona's own map or committed section
   and the names excluded under (ii) and (iii) above; deduplicated.

Exclusion (ii) is what separates length from wrongness: a padding name is a real attribute name,
but no scored question of the persona asks about it, so the lookup and the model can only be moved
by the length of the list, not by a label the list now misstates. Every padded list is asserted
at build to have length L, to contain no excluded name, no `:` and no duplicate, and to contain
the committed names; the exclusion census (names per pool per key) is ledgered.

**Renderer lock.** For every key the section re-rendered over the committed names alone, under the
same function with the cap lifted, reproduces the committed text byte for byte (the cap of 15 never
binds on a TRUE list); 242 of 242 or STOP.

## §4 — Readers, protocol, estimands (descriptive)

**Lookups ($0).** The superseded-names lookup in both variants on the padded section:
embedding (`run_nb6.emb_scores`, `sentence-transformers/all-MiniLM-L6-v2`, local, max cosine) and
lexical (`run_nb6.lex_scores`, Jaccard over content tokens, NB-4's tokenizer); the committed
scores recomputed first as the gate (0.7484 / 0.5738 at four decimals, or STOP).

**GPT-4.1 mini (3 × 661 calls).** `prompts_e1.SYSTEM` and `prompts_e1.USER_INDEXED` verbatim
(digests `337d37d3…` / `35d9b968…` asserted at import), the padded text in place of the summary,
the recorded question; `gpt-4.1-mini` pinned, temperature 0, seed 42, max_tokens 200, JSON mode,
k = 1, one retry on a parse failure (the E1 clamp); through `e1_metamemory/tools/api.py` with the
cache redirected to `pad_probe/cache/` (arm names `PAD-15`, `PAD-30`, `PAD-60`). Served identifier
probed before launch (E1.7 rule). `nok` is the scored quantity; `fok` is recorded and not scored.

**Estimands, per reader and per length**, on the 661 with PN positive:
- AUROC on the whole population and per state (positives of one state against the same 557
  negatives, `nb6_composition.py`'s construction), Mann-Whitney with ties at 0.5 (`common_e1r.auroc`);
- the **paired difference against the 1.75-name row** (padded minus recorded, item by item), with
  the item-level paired bootstrap (1,000 draws, seed 42, single-class draws discarded,
  `common_e1r.boot_item`) and the persona-clustered paired bootstrap (`boot_cluster`, group =
  persona); both print; where they disagree the weaker reading is stated;
- for mini, the number of distinct `nok` values and the mean `nok` at each length; for every reader
  the mean names per item after padding (exactly L by construction, asserted).

## §5 — Branches (enumerated in advance; no pass bar; every one prints as it comes out)

Read per reader (embedding lookup, lexical lookup, GPT-4.1 mini), on the whole population, with
tolerance ±0.05 on the point estimate:

- **Flat.** At every length the paired difference against the 1.75-name row lies inside ±0.05.
- **Degrades.** At some length the paired difference is below −0.05 with both intervals excluding
  zero. The length at which this first happens prints.
- **Degrades past the BELIEVED row.** At some length the reader's AUROC is at or below its
  BELIEVED-row value (embedding 0.5858, lexical 0.4718, mini 0.5959).

A reader can fall under more than one heading (the third implies the second unless the intervals
include zero); every heading that applies prints, and a pattern that fits none (a rise beyond
tolerance, or a difference beyond tolerance whose intervals include zero) prints as described. The
per-state rows are descriptive and print beside; no branch reads them.

## §6 — Budget and STOP

Cost line: **$2.50** on the OpenAI key, inside the combined **$15** cap the author set for this
pass's two new jobs (this probe and `ADDENDUM_PARA`); the cap is shared and every projection prints
against the combined headroom. Projection from the committed TRUE prompts (o200k, mean 1,542 input
tokens on the 661) plus about 5.5 tokens per padded name: 1,983 calls, **$1.46** (×1.3 $1.90). The
runner re-projects from the probe's token counts before launch and refuses to launch if the
projection of this probe together with `ADDENDUM_PARA`'s lanes already run or projected exceeds the
combined cap; the client's hard cap is $2.50 on this namespace. This probe runs **first** of the two
jobs, because it is the cheaper and its lanes are all on one key.

STOP: registration sha256 mismatch; served-identifier mismatch; renderer lock failing on any key;
any padded list of the wrong length, containing an excluded name, a `:`, or a duplicate, or missing a
committed name; the lookup gate failing at four decimals; elicitation failures after the retry on
more than 2% of items at any length; projection over the line or over the combined headroom.

## §7 — Ledger and paper site

`pad_probe/NUMBERS_PAD.md` carries `AUX-PAD-LOCK` (renderer lock, exclusion census, pool sizes,
padded-list assertions), `AUX-PAD-GATE`, `AUX-PAD-PROBE`, `AUX-PAD-PROJECTION`, `AUX-PAD-LOOKUP-EMB`,
`AUX-PAD-LOOKUP-LEX`, `AUX-PAD-MINI` (each: AUROC whole and per state at 1.75 / 15 / 30 / 60, the
three paired differences with both intervals), `AUX-PAD-BRANCH` (the headings that apply, per
reader), `AUX-PAD-SPEND`. Paper: one table row block in Appendix D.2 (whole-set AUROC by length for
the three readers with the paired intervals) and one sentence of Section 5, two-decimal forms in the
body. No frozen number changes; no frozen text changes.

## Registration mechanics

Frozen by sha256 before the first call (recorded in CLAIMS.md R104 and NUMBERS_PAD.md). Copied to
`iclr2027_monitoring_submission/ARTIFACT/registrations/ADDENDUM_PAD.md`. Amendments, if any, are
appended as dated sections and never edit the text above. The author's freeze is the author's
commit of this file, or the author's written GO quoting its sha256.
<!-- REGISTERED TEXT ENDS ABOVE THIS LINE. The sections below are dated additions appended after the freeze; the registration's sha256 is taken over the bytes above this line and never changes. -->

## Amendment 1 (2026-09-14, author-instructed; appended before any call) — the contaminated lists on the 444

The author's instruction of 2026-09-14, verbatim: "Also score mini and Haiku 4.5 on the 444 under the
contaminated lists at c = 0.232 and 0.40 from the nb6 sweep, so the model and the lookup are compared
under the same faults." Descriptive: no prediction, no bar, no verdict. The protocol is fixed here
before the first call and nothing above this line changes.

- **Population.** The 444 items of the CF-2 cell under the **v2** summary (`r82_counterfactual/cf2/cf_cell.json`,
  `cf2/cf_indexes.json`; 148 PN = 88 supersession / 30 retraction / 30 expiry, 40 personas). The recorded
  rows this amendment is paired against, read and never re-run: `cf2/rows/rows_MINI.jsonl` and
  `cf2/rows/rows_H45.jsonl`, arm `INDEXED-V2`, X4 collapse through `score_cf.load_lane`.
- **Lists.** The nb6 sweep's contamination lists, regenerated by `nb6_sweep/tools/sweep_common.inject`
  (store-faithful injection of negatives' own scrubbed names into the summary they read, one name per
  chosen negative, seed 42, nested across rates) at target rates **0.232** and **0.40** over the
  marker-cleaned committed v2 superseded lists. Gate: both lookups on the regenerated lists reproduce
  `nb6_sweep/results/step2_contamination.json` (`cells.cf2.rate_0.232` and `rate_0.4`: embedding whole
  0.6740 / 0.6001 and supersession slice 0.8317 / 0.7567; lexical whole 0.7099 / 0.6630) at four
  decimals, or STOP.
- **Rendering.** As §3: the superseded-names section of the committed v2 text (its tail) re-rendered over
  the contaminated list under `index_v3._name_block` with the per-bucket cap lifted to 100, the text above
  the header byte-identical; renderer lock on the committed names alone, 444 of 444 or STOP; no
  `(+N more)`, no `:`, no duplicate; the injected name(s) print in the section's sorted order.
- **Readers.** Both lookups on the rendered lists ($0; the gate above). `gpt-4.1-mini` k = 1, temperature 0,
  max_tokens 200, synchronous, list price — the CF-2 mini lane's protocol (`run_cf.call_once`), so the
  row pairs with the recorded mini row under the same decoding. Haiku 4.5 (`claude-haiku-4-5-20251001`)
  k = 5, temperature 0, max_tokens 200, Batch — the CF-2 Haiku lane's protocol (X4 collapse, MIN_DRAWS 3,
  arithmetic mean). `prompts_e1.SYSTEM` / `USER_INDEXED` verbatim (digests asserted at import), the
  contaminated v2 text in place of the summary, the recorded question. Served identifiers probed before
  each lane (E1.7 rule). Rows under `pad_probe/rows/`; arms `INDEXED-V2-C0.232`, `INDEXED-V2-C0.40`.
- **Estimands, per reader × rate.** AUROC whole and per state (the CF-2 per-state convention: the items of
  that state, positives and negatives alike, `AUX-CF2-NB6-V2`); the paired difference contaminated −
  recorded on the same items (item-level paired bootstrap, 1,000 draws, seed 42, single-class draws
  discarded; persona-clustered paired bootstrap; both print, the weaker reading governs); the
  model-minus-lookup difference on the same lists under the same summary for both lookups (the
  `AUX-R103-MARGIN` construction); the census (achieved rate, names per item, negatives named).
- **Budget and lane order.** mini 888 calls ≈ **$0.62** (the CF-2 mini lane's per-call actual,
  `AUX-CF2-SPEND`); Haiku 4.5 4,440 calls ≈ **$5.44** (the CF-2 Haiku lane's per-call Batch actual). Both
  lanes join the combined order of `ADDENDUM_PARA` §8 under the same **$15** cap and the same headroom
  rule (a lane whose ×1.3 projection exceeds the headroom remaining at its turn is not submitted and
  prints a dash with the reason): **PAD (§4) → this amendment's mini lane → PARA drafting → the author's
  read → PARA mini → PARA Haiku 4.5 → this amendment's Haiku 4.5 lane → PARA Opus 5.** The registered
  lanes are never displaced by this amendment, which is why its Haiku lane follows PARA's. No lane is
  ever re-run to fit the cap.
- **Ledger.** `pad_probe/NUMBERS_PAD.md`: `AUX-PAD-C-LOCK`, `AUX-PAD-C-GATE`, `AUX-PAD-C-LOOKUP-EMB`,
  `AUX-PAD-C-LOOKUP-LEX`, `AUX-PAD-C-MINI`, `AUX-PAD-C-H45` (each: AUROC whole and per state at the two
  rates, the paired differences with both intervals, the model-minus-lookup rows), `AUX-PAD-C-SPEND`;
  a lane not run carries a dash and its reason. Paper: beside the §7 rows in Appendix D.2.

**2026-09-14 (evening) — the author's cap ruling for Amendment 1.** The author reviewed freeze `dab8956` and
adopted it as the author's registration. The Amendment 1 Haiku 4.5 lane (k = 5, Batch, ≈ $5.44) **runs
regardless of the ×1.3 headroom rule**, in its registered turn (after `ADDENDUM_PARA`'s Haiku 4.5 lane, before
Opus 5), under an **overall cap of $28** for everything in this pass; the combined cap for the registered lanes is
**$21** (`ADDENDUM_PARA` §8 ruling ii, Opus 5 runs once); registered lanes are never displaced.

**2026-09-14 (late) — the author's reorder.** The author's read of the paraphrase sheet is deferred to 2026-09-16 and `ADDENDUM_PARA` holds at the sheet; so that nothing waits on it, the Amendment 1 Haiku 4.5 lane (k = 5, Batch) runs **now**, before the `ADDENDUM_PARA` mini, Haiku 4.5 and Opus 5 lanes, under the rulings of the evening (regardless of the ×1.3 rule; overall cap $28; the registered lanes keep their $21 combined cap and are not displaced).
