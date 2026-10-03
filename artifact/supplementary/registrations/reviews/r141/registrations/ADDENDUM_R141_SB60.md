# ADDENDUM_R141_SB60: the sibling-name control at 60 names

Frozen 2026-09-24, after the author's GO. The rulings of the same day are settled into this text. It is committed alone before the first model call, and its sha256 is taken over the bytes above the end marker. Phase 0 of the brief 'KtS R141'.
This is the second and last exception to the experiment freeze, authorised by the author on 24 Sep.

## §1: Population and construction

- **Pairs.** The 88 supersession pairs of the counterfactual set.
- **PN-60.** The PN version with its superseded-names list padded to 60 names. This is the recorded R136 text: cf_pad/build/texts.json, sha256 `ce0df620…4343` under the lock's method, equal to cf_pad/build/lock.json.
- **SB-60.** The same text with the target's name in the superseded-names section replaced by a same-category sibling name.
  - It is re-rendered by the R136 renderer (pad_common.padded_text).
  - Nothing else changes: the section prefix (the count table and every other line) is byte-identical, and so is the pad.
  - Both lists hold exactly 60 distinct names.
  - Build: reviews/r141/tools/build_sb60.py → reviews/r141/build/build_sb60.json, SB-60 texts sha256 `9346d52dbf677c127f78b6aabfa630282b771151146cfb61af84bd69f925fa74`.
- **The sibling** is the pair's R125 sibling: ADDENDUM_R125_SIBLING, seed 12501, reviews/r125/build/build_t4_sibling.json rows[].sibling.
- **Collision rule** (the author's ruling of 24 Sep: a seeded draw).
  - It applies when the R125 sibling is already a name of the PN-60 list.
  - The substitute is drawn from the pair's remaining HV-B pool: the recorded R125 eligible names (rows[].eligible, with the HV-B neighbourhood rule and the no-shared-content-token rule already applied), less every name of the PN-60 list, sorted.
  - The draw is `numpy.random.default_rng(42)`, one integer draw per collision pair in pair-id order, uniform over that pool. Each draw is recorded in the build (rows[].draw).
  - **35 of the 88 pairs** took a substitute. In every case the R125 sibling was in the pad, since R125 had already excluded the short list.
  - No pair lacked a candidate. 23 of the 35 draws differ from the pool's first name.
- **Checks, all 88 of 88:**
  - the renderer reproduces every SB-60 text byte for byte from its own printed names;
  - every SB-60 list holds 60 distinct names;
  - the target is in no SB-60 list;
  - the sibling is in no PN-60 list;
  - the prefix, and so the count table, is identical to PN-60's;
  - exactly one name differs between the two lists;
  - no overflow marker.

## §2: The leak screen (the first model call after the freeze)

It follows R125's rule:
- take the 88 SB-60 items sorted by item id, and draw `random.Random(42).sample(pool, 30)`;
- call gpt-4.1-mini at temperature 0, seed 42, max_tokens 200, with `prompts_e1.LEAKAGE_SYSTEM` / `LEAKAGE_USER`;
- gold is the pair's entry_text; scoring is `exp4_witnesses.supports_correct`;
- the control LEAKS iff more than 3 of 30 score correct.

A leak is a STOP before any lane runs. Its cost counts against the cap.

## §3: Endpoints

- **Primary:** the matched score (W + T/2)/88 of PN-60 against SB-60, with the triple-level and persona-grouped 95% intervals.
- **Secondary:** the pooled AUROC over the 176 items, with the item-level and persona-grouped intervals.
- **Estimation:** 1,000 draws, seed 42, the r125_common estimators.
- **Reliable:** both 95% intervals exclude zero.
- **Equivalent within 0.05:** both 90% intervals lie inside [-0.05, +0.05] (the same draws).
- **Model minus the name lookup:** paired on the same pairs, on both metrics.
- **Sensitivity:** seeds 43 to 46 on every registered difference.

## §4: Readers and lanes

Only the SB-60 rows are new calls. The PN-60 model rows are the R136 recorded rows (cf_pad/rows/rows_{MINI,LUNA,SOL}.jsonl, arm INDEXED-V2-PAD60, the PN items).

| lane | model id | draws | settings (R136 Table 44 rows; R136's code paths, called) |
|---|---|---|---|
| SB60-LUNA | `gpt-5.6-luna` | 5 | reasoning effort and temperature unset, `max_completion_tokens` 2048, raw Chat Completions (`cf2_openai.call_once`) |
| SB60-MINI | `gpt-4.1-mini` | 5 | `max_tokens` 200, temperature unset (provider default; Table 1's five-draw row), Chat Completions |
| SB60-SOL | `gpt-5.6-sol` | 5 | as Luna |

- **Order:** Luna, then mini, then Sol, draw-major.
- **Rows:** 440 per lane; none unparseable.
- **Served identifier:** checked on a probe call before each lane and on every row at scoring. A mismatch is a STOP for that lane.
- **Prompts:** `prompts_e1.SYSTEM` / `USER_INDEXED`, byte for byte.
- **Not run:** Haiku 4.5 and Opus 5 are not run on this control (no Anthropic call), and the paper says so.

## §5: Caps

- **OpenAI $12.00 for this run**, metered from the rows at the page prices recorded in cf_pad/build/lock.json.
- **Projection** from the R136 rows' metered cost per row, times 440:
  - Luna $0.17;
  - mini $0.30;
  - Sol $2.60;
  - the leak screen about $0.015.
  - Total $3.08; ×1.3 is $4.00.
- **Cap rule:** a lane whose projection would exceed the remaining cap is dropped by rule, Sol first, and printed as not run.
- **Balance:** the account balance could not be read. The key lacks `api.usage.read`, and the credit-grants endpoint needs a browser session (both 403 on 2026-09-24). The author reports a top-up.

## §6: Recorded before the freeze (not predictions)

These no-model values were computed on 2026-09-24, before this text was frozen, on the texts of §1 (reviews/r141/tools/score_nomodel_sb60.py → reviews/r141/results/nomodel_sb60.json). The predictions are about the models relative to them.

| reader | PN-60 vs SB-60, matched | W/T/L | pooled |
|---|---|---|---|
| name lookup (embedding) | 0.8239, triple [0.7727, 0.8750], persona [0.7670, 0.8816] | 57/31/0 | 0.7395 |
| lexical lookup | 0.7386 | 42/46/0 | 0.6815 |
| random-token lookup | 0.5000 | 1/86/1 | 0.5006 |
| length-only reader | 0.5000 | 0/88/0 | 0.5000 |
| count reader (guessed category) | 0.5000 | 0/88/0 | 0.5000 |

SB-60 against the padded PRESENT version (the list-length component, descriptive):

| reader | matched |
|---|---|
| name lookup | 0.5227 |
| lexical lookup | 0.5114 |
| random-token lookup | 0.5057 |
| length-only reader | 1.0000 |
| count reader | 0.6932 |

The PN-60 lookups recomputed on the printed lists equal the recorded R136 vectors.

## §7: Predictions

Each is read on the matched endpoint, with the pooled reading beside it. Every prediction prints as it comes out; a failed one is reported in its frozen failure text.

- **P-S1:** Luna exceeds the name lookup on PN-60 vs SB-60, with both intervals clear of zero.
- **P-S2:** Sol exceeds the name lookup on PN-60 vs SB-60, with both intervals clear of zero.
- **P-S3:** mini does not reliably exceed the name lookup.
- **P-S4:** each of Luna and Sol scores at or above 0.80 matched on PN-60 vs SB-60, with the persona interval above 0.50.

## §8: Branch sentences (verbatim; fire by P-S1 and P-S2)

### B-i (both hold)

- **Abstract:** "On lists longer than the stores we tested write, padded to 60 names, the lookup loses 0.18; GPT-5.6 Luna and Sol lose 0.06 to 0.07 and lead it by 0.13 to 0.14, while the other three fall with it. The lead holds against a sibling padded to the same length and counts." Drop "A list-length cue is uncontrolled there."
- **5.2**, replacing "the padded set has no such control (Appendix C.2)": "A sibling padded to the same length and counts, run on Luna, Sol and mini, removes that cue: the length-only reader ties every pair, the lookup scores [x], and Luna and Sol lead it by a reliable [d] and [d] (Appendix C.2)."
- **Limitations:** "The padded sibling control ran on Luna, Sol and mini; Haiku and Opus were not run on it, and the padded lists' counts stay as written, so the superseded total disagrees with the list length in both versions alike."
  - This sentence is an addition. The length-cue sentence it was written to replace was never landed; that is the R139 report's error, recorded in reviews/NUMBERS_R141.md.
- **Conclusion:** "On a 60-name list Luna and Sol lead the lookup by 0.13 to 0.14 and, with list length and counts fixed, by [d] and [d]; the other three fall with it."
- **Landing payers under B-i**, in order, stopping as soon as the probe's slack is at least 1:
  - (a) 5.2's cue paragraph drops "where readers still picked the PN version at 0.88 or higher".
  - (b) The 5.2 sentence loses "the length-only reader ties every pair," and reads "A sibling padded to the same length and counts, run on Luna, Sol and mini, removes that cue: the lookup scores [x], and Luna and Sol lead it by a reliable [d] and [d] (Appendix C.2)."
  - (c) The Limitations sentence is shortened to its first clause: "The padded sibling control ran on Luna, Sol and mini; Haiku and Opus were not run on it."

### B-ii (exactly one holds)

- As B-i, with the reader named in each sentence.
- The abstract's second sentence reads "The lead holds for [reader] against a sibling padded to the same length and counts."
- For the other reader, 5.2 adds "[reader]'s lead is not separated from the cue", and Limitations keeps that clause for it.
- B-i's landing payers apply.

### B-iii (neither holds)

- **Abstract:** "On lists longer than the stores we tested write, padded to 60 names, the lookup loses 0.18 and GPT-5.6 Luna and Sol keep more of their score. Against a sibling padded to the same length and counts, no model reliably beats the lookup."
- **5.2 lead sentence:** "On the named state, no model reliably beats the lookup on the short list, and on a 60-name list none does once list length and counts are fixed."
- **5.2 paragraph:** its padded sentences stay as the stress-test record. The replacement sentence reads: "A sibling padded to the same length and counts, run on Luna, Sol and mini, removes that cue and the lead with it: the lookup scores [x] and no model is reliably above it (Appendix C.2)."
- **Intro bullet 2 and the Conclusion:** drop "two of five do when it is padded to 60 names" and "Luna and Sol lead the lookup by 0.13 to 0.14". The Conclusion reads "no model reliably exceeds the name lookup on the short list, nor on a 60-name list once its length is fixed".
- **Limitations:** "The padded sibling control ran on Luna, Sol and mini; Haiku and Opus were not run on it."
- The thesis line in the abstract stands in every branch.

## §9: Disclosures

- This registration follows every earlier result on the same items, so no confirmatory design is claimed.
- The no-model values in §6 were computed before the freeze.
- 35 of 88 siblings are collision substitutes, each a seeded draw (numpy default_rng(42), pair-id order) from the pair's remaining HV-B pool.
  - An alphabetical-first rule was built first and replaced by the author's ruling before the freeze.
  - The recorded no-model values of §6 are the same under both rules, because the pad names, not the sibling, supply the lookups' maxima.
- Only mini's, Luna's and Sol's SB-60 rows are new.
- The PN-60 rows are those of R136, which ran under ADDENDUM_CF_PAD.

<!-- REGISTERED TEXT ENDS ABOVE THIS LINE -->
