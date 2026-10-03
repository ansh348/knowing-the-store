# PREREG ADDENDUM — E1.5

**Dated:** 2026-08-10 · **Amends:** `PREREG_E1.md` (`875f726`) and `AMENDMENT_1_E1.md`
(`307865f`), both preserved unchanged. **Results basis:** `RESULTS_E1.md` (`5c5bae8`).

**Statement of prior data contact.** **No E1.5 call has been made.** Every number this addendum
reasons from already exists in `results/scores_e1.json` and `strong_model.json`. The two
interpretation rules below are frozen **before** the numbers they will be applied to exist.

**Scope fence, as instructed:** two runs only. No other workstream, no draft edits. **The NOK
factorial — separating the three simultaneous fixes that broke E0's null — is explicitly deferred
to E2 and its own pre-registration.** Budget cap **$5**.

---

## RUN A — the frontier-indexed cell

### Design

The same 150-item stratified subsample used for the strong-model blind check (seed 42; quota
PRESENT 50 / ABSENT 60 / PRESENT-NEGATIVE 40), which resolves by backend to **FR-Bank 84**
(14 PRESENT, 30 ABSENT, 40 PN), Mem0 29, A-MEM 37.

`gpt-5.6-sol` via `codex exec`, temperature 0, the frozen `prompts_e1` texts in their **indexed**
form (`SYSTEM` + `USER_INDEXED`), TRUE-state index at ladder level 0 — the level all six
(backend, provenance) cells passed at 0/30.

**All 150 items are run**, each against its own backend's TRUE index. **The primary Run A
comparison is the FR-Bank subset (n=84)**, per the instruction naming FR-Bank; the 66 external
items are an additional exploratory read, reported separately, and they bear directly on Run B.
Running all 150 rather than only the 84 costs nothing extra — the lane is subscription-billed —
and preserves the full paired structure against the existing frontier-blind draws.

### Interpretation rule, frozen before the number exists

Let Δ_frontier = frontier-indexed FOK AUROC − frontier-blind FOK AUROC on the FR-Bank subset,
with a paired bootstrap (1,000 resamples, seed 42, items resampled, both arms moving together).

- **(a)** If **Δ_frontier ≥ +0.10 and the 95% CI excludes 0** → report under
  **"the mechanism generalizes up the capability ladder"**.
- **(b)** Otherwise → report under **"cheap-model equalizer"**, stating the cost comparison
  explicitly: `gpt-4.1-mini` **indexed** reaches hard-tier AUROC **0.7530** while `gpt-5.6-sol`
  **blind** reaches **0.7154**, and the measured per-call cost of a mini indexed call is
  **$0.00056** (\$1.3176 over 2,366 indexed calls) against a frontier call that is
  subscription-billed with no per-call dollar price, consuming ~3,157 tokens and ~8 s of wall
  clock against the mini call's ~1.2 s. The ratio is stated in these measured terms rather than
  as a list-price ratio, which I cannot verify for `gpt-5.6-sol`.

**Both outcomes are reportable. There is no kill condition.**

### NOK on the subsample

The FR-Bank subset contains **40 PRESENT-NEGATIVE items**, so frontier NOK is reported blind and
indexed on those items. **Exploratory and ungated** — it does not touch H-NOK, whose verdict is
already fixed on the full FR-Bank cell. Frontier blind NOK is already captured for all 84 items.

---

## RUN B — the below-chance mechanism counterfactual

E1 found that on Mem0 and A-MEM the TRUE index puts FOK **below chance** (0.4777 and 0.4526
against blind 0.5746 and 0.5591). **The paper may not assert a cause for that without this run.**
Three hypotheses, each with the prediction it makes, frozen here.

### H-a — uniform suppression that lands harder on PRESENT

The index depresses FOK across the board; because the external cells are majority-ABSENT, a
uniform downward shift mechanically helps ABSENT and hurts PRESENT, inverting the ordering.

> **Prediction:** decomposing the per-item FOK shift (indexed − blind) by cell, the **negative
> shift is larger on PRESENT than on ABSENT**. No new calls.

### H-b — the inexpressibility markers drive pessimism

A 31-line index whose lifecycle rows all read *"not expressible by this backend"* reads as an
impoverished store, and the model lowers FOK for that reason rather than from anything about the
specific question.

> **Prediction:** with the marker lines **omitted rather than rendered**, the inversion shrinks or
> disappears. **One new elicitation arm**, on the 522 external scoreable items, identical in every
> other respect: same model (`gpt-4.1-mini`), same temperature, same seed, same `USER_INDEXED`
> wrapper, same index — only the lines whose value is the marker string are dropped, and the
> sentence in `USER_INDEXED` explaining the marker is dropped with them, since it would otherwise
> refer to something no longer present. That paragraph substitution is the **only** prompt
> difference and is recorded as a frozen variant `USER_INDEXED_NOMARKER` in `prompts_e1.py`.

### H-c — count anchoring

The model anchors FOK on the entry-count and per-category-count fields, which vary across stores
in ways uncorrelated with whether a particular question is answerable.

> **Prediction:** FOK correlates with the index's count fields. **Descriptive correlation only;
> no new calls.** Reported as Spearman ρ between indexed FOK and (entries-in-store, active count)
> per backend, with the same correlation on FR-Bank as the contrast.

### Verdict rule, frozen

Report which hypotheses survive their prediction. **If the results are mixed, the verdict is
"mechanism unresolved" and the paper's text stays agnostic. No winner is to be forced.** A
hypothesis counts as surviving only if its own stated prediction holds; a hypothesis is not
promoted by the failure of the others.

---

## Budget

Run A is subscription-billed (no dollar cost). Run B's H-b arm is 522 `gpt-4.1-mini` indexed calls
at a measured ~$0.00056 each ≈ **$0.30**. Projected total **≈$0.30** against the **$5** cap.
Runs A and B add no new labels and change no existing one.
