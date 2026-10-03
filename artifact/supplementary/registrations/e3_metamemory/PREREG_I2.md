# PREREG — I2, SELECTIVE CAUTION

# ✅ FROZEN 2026-08-11, BEFORE THE PRECONDITION IS COMPUTED

**Nothing in this file has been evaluated at the time of its commit.** The precondition below is
computed only after this file exists in the repository, and its result — either way — is reported
against the prediction frozen here.

**Scope.** I2 is a **pre-registered synthesis over pre-existing outputs**. It makes **no new model
call**: every context state it needs already exists on every eval cell. It is **not a gate**, it is
**not part of the frozen sequence**, and it is **not a rescue of H-E3a**. `RESULTS_E3.md` is
immutable and unaffected whatever this returns.

---

## 1. The question, and the measured payoff that motivates it

`FORENSIC_E3_REPORT.md` Q4 measured a **signed caution tax** on E3's 834 eval cells:

| stratum | n | Δ credit, (a″) − (b) | 95% CI |
|---|---|---|---|
| **PRESENT-NEGATIVE** | 99 | **+0.0909** | **[+0.0392, +0.1584]** — excludes zero |
| **PRESENT** | 250 | **−0.0400** | [−0.0878, +0.0052] |
| natural-absent | 484 | +0.0103 | [+0.0000, +0.0254] |
| all | 834 | +0.0165 | [−0.0078, +0.0400] |

**Generic caution gains 9.1 credit points where there is something to suppress and costs 4.0 where
there is not.** At E3's mix the two nearly cancel. **A policy that fired caution only where it pays
would capture the first without paying the second — if any available signal can make that
selection.** I2 asks exactly that, and nothing else.

## 2. The precondition — computed AFTER this commit, reported either way

> **PRECONDITION, FROZEN: NOK's AUROC for PRESENT-NEGATIVE vs everything else, on E3's committed
> eval gate signals, must EXCEED 0.65.**
>
> * **AUROC ≤ 0.65 → PRECONDITION FAILED. I2 is CLOSED**, no threshold is derived, no policy is
>   synthesized, and **the stated failure reason in §4 stands as the answer to "why not selective
>   caution".**
> * **AUROC > 0.65 → proceed to §3.**
>
> The number is reported to four decimals whichever side of 0.65 it lands, together with the PN
> prevalence and the n it is computed on.

**Why 0.65 and not another number.** A selector must beat the retrieval-rate-matched coin. At E3's
PN prevalence of 99/834 = 11.9%, an AUROC of 0.65 is roughly the point below which a threshold
capturing a useful share of PN cells necessarily also captures a majority of PRESENT cells — at
which point "selective" caution is caution with extra steps. It is set here, before the value is
known, and it is not moved afterwards.

## 3. If the precondition passes — the threshold is DERIVED, not fitted

The threshold `t` is set by the **frozen Amendment-4 break-even rule**, applied on the **8
calibration personas and nowhere else**:

```
B  = credit gain from the caution step on PN cells          (calibration)
C  = credit loss from the caution step on non-PN cells      (calibration)
q* = C / (B + C)
t  = the LOWEST threshold on the uniform grid {0.00, 0.05, ..., 1.00}
     whose CALIBRATION precision for PN is >= q*
```

**No eval quantity enters the choice of `t`.** `FORENSIC_E3_REPORT.md` Q5 swept this same policy
family **on eval data** and is used only to state in advance what `t` would have to beat; it is not
consulted to select `t`, and the two numbers are reported side by side so a reader can see the
difference between the derived point and the eval-fitted frontier.

**The policy, then synthesized from existing answers:** `choose[(a″) if NOK ≥ t else (b)]` per cell.
Both endpoints — credit and confabulation — reported against (a), (a″) and (b), with
persona-clustered CIs, under the label **"pre-registered synthesis over pre-existing outputs"**.

## 4. Frozen predictions

1. **The precondition FAILS: NOK's PN-vs-rest AUROC is ≤ 0.65.**
2. If it nonetheless passes, **the derived `t` lands at or below 0.05**, because the NOK distribution
   admits nothing higher without collapsing the fire rate — Q5 measured 43.4% of cells clearing 0.05
   and only 1.6% clearing 0.25.
3. If a policy is synthesized, **it lands within 0.5pp of (a″) on both endpoints** — firing on ~43%
   of cells at t = 0.05 is not selective.

**The stated failure reason, frozen here as the paper's answer if prediction 1 holds:**

> *"Selective caution is worth designing and this monitor cannot do the selecting. The caution
> instruction's benefit is concentrated on obligation-bearing questions and its cost on
> answerable ones — a payoff with an interval excluding zero — but the NOK channel does not separate
> those two populations: its scores are piled at the bottom of their range and its discrimination for
> PRESENT-NEGATIVE is at or below 0.65 AUROC. The selection problem is real; the signal available to
> solve it is not."*

## 5. What this can and cannot be called

**Can:** a pre-registered synthesis over pre-existing outputs; a descriptive; a negative result about
the NOK channel's usability as a selector.

**Cannot:** a gate, a hypothesis test, a member of the frozen sequence, evidence for or against
H-E3a / H-E3b / H-E3c / H-E3d, or a rescue of any of them. **No sentence quoting I2 may imply that
E3's primary result is other than FAILS.**

## 6. Cost

**$0.** Every context state I2 needs already exists on every eval cell, and the calibration
derivation reads committed calibration answers. No new elicitation, no new retrieval, no new store.
