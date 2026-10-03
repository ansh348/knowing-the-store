# STOP notice — E1-R sub-step (a)

**Raised: 2026-08-15.** Governing rule: `SPEC_E1R.md` §(a) STOP condition, frozen at commit
`9ac91a2` before any number in this pass was computed.

> For any row whose published item-level CI excludes zero, if the persona-clustered CI
> **includes** zero, computation halts at the end of this sub-step and the result is reported
> to the principal investigator **before any manuscript sentence is edited**.

The condition fired on **exactly one row of eighteen**. Computation is halted at the end of
sub-step (a); sub-steps (b) and (d) are not started, and no manuscript sentence has been
touched.

## The triggered row

| Row | n | Published Δ | Item-level CI | Persona-clustered CI | Verdict |
|---|---:|---:|---|---|---|
| **Opus 5, FOK** | 84 | **+0.1213** | [+0.0047, +0.2449] | **[−0.0136, +0.2368]** | includes zero |

The item-level interval excluded zero by a margin of **+0.0047** — four ten-thousandths of an
AUROC point above the null. It was the most marginal interval in the manuscript. Under
persona clustering it crosses.

Leave-one-persona-out on the same row shows **zero sign changes** across 33 folds, so the
direction of the effect is stable; it is the *interval*, not the point estimate, that fails.

## Blast radius: contained to one appendix cell

The value `+0.1213 [+0.0047,+0.2449]` occurs exactly once in the manuscript, at `paper.tex`
line 747, inside appendix Table `tab:ladder-exact`. A literal scan confirms no other
occurrence.

No registered gate and no main-text sentence depends on this delta's interval excluding zero:

| Dependency checked | What it actually tests | Status under clustering |
|---|---|---|
| XV-2 (line 788) | positive indexed−blind **NOK** delta, interval excluding zero, on Opus 5 and K3 | **unaffected** — Opus 5 NOK clustered CI [+0.0923, +0.2392]; K3 NOK [+0.1653, +0.3933]; both exclude zero |
| XV-4 (line 790) | indexed **FOK level** inside the registered band | **unaffected** — a level, not a delta |
| P3 (line 769) | ordering of the mini/luna/sol FOK deltas | **unaffected** — Opus 5 is not in the ordering |
| Abstract / conclusion cross-vendor claim | "every new paired NOK delta remains positive with its interval excluding zero" | **unaffected** — all three new NOK rows survive clustering |

The paper's load-bearing cross-vendor claim is about **NOK**, and every NOK row survives.

## Every other row survives

All six E1 calibration rows and eleven of the twelve matched-cell rows keep intervals that
exclude zero under persona clustering. Leave-one-persona-out produces zero sign changes on
every row except K3 FOK, whose interval already includes zero at item level and is not
claimed as an effect.

## What a ruling is needed on

The frozen contingency reading for this branch is already fixed and is not open for
selection now: *the item-level interval overstates precision for that row; the row's claim is
restated as directional, the clustered interval is printed beside it.* What needs a decision
is the presentation:

1. **Print both intervals in Table 4 for this row**, with a footnote naming the clustering
   sensitivity — the minimal, most transparent change; or
2. **Print both intervals for all twelve matched-cell rows**, making the clustering
   sensitivity a uniform property of the table rather than a spotlight on the one row that
   moved; or
3. **Add the clustered column to the appendix sensitivity table only**, leaving Table 4 as
   the preregistered item-level record with a pointer.

Option 2 is the recommendation: it avoids the appearance of reporting the sensitivity only
where it hurts, and it is the option a skeptical reader would ask for.
