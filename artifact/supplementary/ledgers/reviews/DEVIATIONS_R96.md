# DEVIATIONS_R96 — R96-RESTATEMENT (2026-09-12)

Own numbering from D-R96-1. The two R82-ledger deviations this program surfaced are entered where
they belong, `r82_counterfactual/DEVIATIONS_R82.md` D-R82-6 (the v3 leakage screen) and D-R82-7
(the two unledgered Opus 5 per-state values), and are cross-referenced here only.

---

## D-R96-1 — the abstract runs 191 words against the R92 R-a figure of 180

**What happened.** The R92 program's ruling R-a rewrote the abstract "to the prompt's seven-slot
order at 180 words or fewer"; it landed at 177 words in eight sentences. R96 item (1) restates
the abstract's slot-4 sentence (34 words) as two sentences (23 and 25 words), and the abstract
lands at **191 words in nine sentences** by `prose_scan`'s counter.

**Why it was not trimmed back.** The 180 figure is a prompt figure of R92, not a STYLE_SPEC
rule: S6 fixes the sentence band (7 to 11), the ends-on-headline rule and the no-parenthetical-CI
rule, all of which hold. Reaching 180 would have meant cutting words from the other seven R92
sentences, each of which was landed under its own ruling and none of which the R96 prompt names.
The restatement is the ordered change; the ceiling yields to it, and the overage is recorded here
rather than absorbed silently.

**Disposition.** Recorded in the CLAIMS.md R96 block (ruling R-c, entry 1a). If the ceiling is
to be restored, the candidate cut is inside the two new sentences ("spanning three vendors", three
words, and "and anchors no gain", four), which would land at 184; anything lower touches R92 text.

---

## Cross-references

- **D-R82-6** (`r82_counterfactual/DEVIATIONS_R82.md`): the v3 leakage screen was reserved, never
  run and never ledgered; the deterministic half ran at R96 without a model call (1 of 30 on the
  registered cell, inside the threshold); the model-mediated screen has not run. The R96 prompt's
  "(ladder_e1, deterministic)" is the point of departure: `ladder_e1` scores deterministically but
  answers by model call.
- **D-R82-7** (same file): two Opus 5 per-state values under v3 were computed at `7e9ac39` and
  never ledgered; ledgered at R96 and printed in Table 9.
- **Noted, not done** (outside the prompt's list): `DEVIATIONS_R82.md` lost D-R82-1 and D-R82-2 at
  `eb707fc` the same way `NUMBERS_R82.md` lost §1 to §5 at `be64244`; both entries are recoverable
  from `git show 2a35848:r82_counterfactual/DEVIATIONS_R82.md`. The R82 block in CLAIMS.md cites
  "D-R82-1 to D-R82-5".
