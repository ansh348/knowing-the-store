# AMENDMENT 2 to PREREG_E0.md

**Dated:** 2026-08-10 · **Amends:** `PREREG_E0.md` frozen at `0f2fde2` and `AMENDMENT_1.md` at
`d4ef3be`, both preserved unchanged.

**Statement of prior data contact.** Elicitation has been run (Step 4, commit `dc72d09`) and its
raw responses are committed. **No scoring output has been computed** — no AUROC, ECE, Brier or
bootstrap exists at the time of this amendment. What is known about the elicited data is limited
to the parse-success count, the cost ledger, the response-value histograms, and the
label-conditional mean FOK reported in `STEP2-4_REPORT.md`. This amendment adds a sensitivity
row; **it changes no primary gate metric, no hypothesis, and no threshold.**

---

## The addition: a "blind-deduplicated" sensitivity row

**Construction.** For each question, the BLIND arm was called twice — once for the FULL item and
once for the ABLATED item — with a **byte-identical prompt**, because the blind arm carries no
information about which variant it is judging. Replace the blind FOK and the blind NOK of *both*
variants with the **mean of the two draws**. Then recompute:

- blind FOK AUROC,
- indexed FOK AUROC (unchanged by construction — the indexed prompts genuinely differ by variant
  and are **not** deduplicated),
- the H2 delta (indexed − blind) and its paired bootstrap 95% CI,

and report the row **directly beneath the primary gate table** in `RESULTS_E0.md`.

## Rationale

D19 established that the two byte-identical blind draws disagree on **90 of 255 question pairs
(35%)**, mean |Δ| 0.134, and that this within-question variance is **14.6% of total blind FOK
variance**. It is provider-side nondeterminism, not a harness defect.

That noise is **non-differential** — it has no preferred direction with respect to the label — so
in expectation it **attenuates** the blind FOK AUROC toward 0.5. Attenuation of the blind arm
favours **both** pre-registered hypotheses:

- **H1** is *blind FOK AUROC < 0.75*. Attenuation pushes the blind AUROC down, making H1 easier
  to satisfy.
- **H2** is *indexed − blind ≥ +0.10*. A depressed blind AUROC inflates the delta, making H2
  easier to satisfy.

Both effects point the same way, and it is the way the paper's hypotheses want. Every other bias
identified in this probe has been either neutral or self-cancelling across the two gates — the
Amendment 1 ABSENT contamination, for instance, helps H1 but hurts H2 and so cannot manufacture
a false GO. **This one does not self-cancel.** It is therefore the single most important
sensitivity check in the study, and it is added before any scoring output exists.

Averaging the two independent draws halves the variance of the blind noise term, so this row
**bounds the attenuation effect**: the gap between the primary blind AUROC and the deduplicated
blind AUROC is a direct estimate of how much of the primary result is attributable to
nondeterminism rather than to blind miscalibration. It does not eliminate the noise — two draws
averaged still carry half of it — so the row is a **lower bound on the correction**, and the true
noise-free blind AUROC lies at or beyond the deduplicated value.

## What does not change

**The primary gate remains exactly as frozen**: computed on the per-item blind draws, with the
thresholds, hypotheses, gate logic (GO / KILL-A / KILL-B / AMBER), metric definitions and
bootstrap specification of `PREREG_E0.md` §§1, 2, 11. The verdict is read from the primary table.
This row is reported beside it and **gates nothing**.

If the primary and deduplicated rows disagree about whether a gate is met, `RESULTS_E0.md` will
say so plainly and report the primary verdict as the verdict, with the disagreement stated as a
finding rather than resolved in either direction.

## Reporting requirements added

1. The blind-deduplicated row directly beneath the primary gate table.
2. The number of question pairs contributing two draws, and how single-variant questions are
   handled (they keep their single draw; averaging a singleton is the identity).
3. NOK is deduplicated on the same construction and reported in the exploratory NOK table.
