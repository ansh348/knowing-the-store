# DEVIATIONS_SIDE — deviations from ADDENDUM_SIDE.md (frozen e8b2630)

Own numbering from D-SIDE-1. Entries follow the R82 form: what happened, what changed, why it
is admissible, disposition.

---

## D-SIDE-1 — §C.1's descriptive slot-changing ambiguity rates were computed with the band measured from the global-best cosine, not from the target

**What happened.** `ADDENDUM_SIDE.md` §C.1 prints a descriptive "ambiguous, slot-changing —
pre-freeze census on the scrubbed name" row of **24.1%** (Mem0) and **36.5%** (A-MEM). The
pre-freeze supplementary census that produced those figures measured the 0.02 band from the
best cosine over all FR-Bank candidates. The frozen definition in the same section (ruling #3)
reads "within 0.02 cosine **of the target**". Where a lexical target is not the global argmax
the target band sits lower and admits more neighbours. `verify_side.py`, implementing the frozen
definition, recomputes the scrubbed-name variant as **24.6%** (0.2461) and **37.6%** (0.3763),
and its two pins on the printed figures failed on 2026-09-12 (CF2-BUILD-1 step 2). Scan depth
was ruled out as a cause: top-50 and full scans agree to four decimals under either band.

**What changed.** Nothing frozen. The row is descriptive and labelled pre-freeze; §C.1's text is
not edited. `verify_side.py` pins the target-band values (0.2461 / 0.3763). The ledger keys the
registration reserves for the frozen measure are written under the mapping each backend
actually uses: `AUX-SIDE-S1-AMBIG-MEM0` = **0.252**, the slot-changing rate under the
lexical-required mapping the spot-check forced on Mem0 (target band); `AUX-SIDE-S1-AMBIG-AMEM`
= **0.4344** under the two-channel map A-MEM uses (target band). The two-channel Mem0 figure,
**0.2920**, prints beside as descriptive, labelled as the map the spot-check did not admit.

**Why this is admissible.** It corrects a construction detail of a descriptive, pre-freeze
figure toward the definition the registration froze, before any index or monitor call exists,
and the exact figures are larger, not smaller, than the ones printed — the correction moves
against the registration's convenience. No prediction, population, mapping rule or ledgered
spot-check value is touched. Ruling of 2026-09-12.

**Disposition.** The registration's §C.1 row stands as printed with this entry beside it; the
ledger carries the frozen rates; `verify_side.py` is the gate from here on.

## D-SIDE-2 — §S1.a's cosine column is the global-best cosine, not the cosine to the target, on 10 of the 60 frozen pairs

**What happened.** `ADDENDUM_SIDE.md` §S1.a prints each frozen spot-check pair as (persona,
backend id prefix → FR-Bank entry, cosine, channel). At build (SIDE-BUILD-1 step 1, 2026-09-12,
`tools/build_s1.py` gate 2) the two-channel map reproduced the identity, target and channel of
all 60 pairs, and the draw itself (`random.Random(42).sample` over the mapped pairs sorted by
(persona, entry id)), but the printed cosine matched the cosine to the target on only 50. On the
other ten — Mem0 pairs 12, 18, 22, 24 and A-MEM pairs 6, 8, 9, 11, 15, 19, every one a `both`
pair whose lexical target is not the global argmax — the printed figure is the *global-best*
cosine over the persona's FR-Bank entries (matched to 0.0005 on all 60), the quantity the
pre-freeze census keyed on, as D-SIDE-1 already records for its ambiguity band. The largest gap
is A-MEM pair 9 (rosa, printed 0.652, target 0.389); the ten are listed with both figures in
`s1/build_s1.json["spotcheck_section_S1a"]`.

**What changed.** Nothing frozen. The pairs the author read are the same pairs (same entry, same
target, same texts in `reviews/SIDE_REG_REPORT.md`), so the §1 verdicts, precisions and the
fallback decision stand. `build_s1.py` gate 2 keys on identity, target and channel exactly and
on the global-best cosine to 0.0015, which is what the registration printed. The ledger's §4
carries a note. The registration's text is not edited.

**Why this is admissible.** A labelling detail of a descriptive column in a frozen sample,
found and disclosed before any monitor call, touching no prediction, population, mapping rule
or verdict. The direction of the discrepancy is against the registration's convenience: the
printed cosines overstate how close the ten lexical targets sit to their notes.

**Disposition — ruled 2026-09-12.** Recorded as a labelling error in the printed §S1.a sample;
the verdicts were on the texts and stand. The target-band cosine is ledgered beside the printed
value for the ten pairs (`NUMBERS_SIDE.md` §4, "§S1.a cosines, for D-SIDE-2"); A-MEM pair 9
(rosa, the largest gap) was judged WRONG regardless. Registration untouched.
