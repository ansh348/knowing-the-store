# DEVIATIONS_R98 — the CF-2 landing in `paper_v8.tex` (2026-09-13)

Own numbering D-R98-n, the R82 form. Base: `paper_v7.tex` (the R97 close, uncommitted; read as the
tree object `a66254cb`). Registration: `registrations/ADDENDUM_CF2.md` (frozen `f016f03`, R94;
amendments §14–§17). Ledger: `r82_counterfactual/cf2/NUMBERS_CF2.md`. Authorization: `CLAIMS.md`
R98 AUTHORIZATION BLOCK, written before the edits.

---

## D-R98-1 — two surface forms inside the frozen texts

**What happened.** The §8 branch texts are frozen and ship verbatim (R78-2c). Two of their surface
forms do not match the manuscript's conventions: the P5 sentence names the smallest reader as
`gpt-4.1-mini` (the API identifier, in backticks), where the manuscript writes "GPT-4.1 mini"
everywhere; and the P1 sentence writes the blind level as "0.5", where PRECISION-R81-1 prints
four decimals ("0.5000").

**What changed.** The P5 sentence prints "GPT-4.1 mini's" and the P1 sentence prints "$0.5$" as
the registration wrote it. Nothing else in either sentence moves; every placeholder is filled at
the ledger's four decimals.

**Why this is admissible.** The identifier is a naming convention, not wording; the manuscript
has one name for the model and a second spelling would read as a second model. The "0.5" is the
registration's own text and is left as written rather than "corrected" to a form it did not
freeze. Both are disclosed here and in the CLAIMS block (R-a).

**Disposition.** `NUMBERS_CF2.md` §5k "Printed forms" carries the two [MAIN] sentences as they
print, one per line, which is what `prose_scan` and `slogan_scan` source their exemptions to.

---

## D-R98-2 — the page gate fails by sixteen review lines (nine at v7 under D-R97-2)

**What happened.** `page_census_v2 paper_v8.pdf`: label on page 10, reading 501, slack −16. At v7:
10, 494, −9 (D-R97-2). R98 adds about seven review lines to the main text: the frozen P1 HOLDS text
is two sentences where the failed-replication sentence was one, its history pointer is a third; the
§6 lookup sentence is split at the 30-word target; §7's lookup sentences grow by one clause.

**What changed.** Nothing was cut or moved to the appendix on this program's judgment. Every
non-frozen new sentence is at its shortest form; the frozen sentences cannot be shortened.

**Why this is admissible.** The gate is the author's to clear by a ruling on content; the D-R97-2
menu (items a–h, with line costs) stands, and R98 adds: (i) the §7 history pointer, "The first,
thirty-question form of that set did not replicate at item level (Appendix D.2)", −1 line, at the
cost of the main text no longer saying where the first form went; (j) the second half of the split
§6 lookup sentence ("It exceeds every GPT-4.1 mini score by more than the ±0.05 tolerance"), −1,
the fact remaining in Table 9 and D.2; (k) the §7 clause "and on the store-counterfactual set
($444$)", −0.5. Any combination of the R97 and R98 items reaching sixteen (seventeen for safety)
passes.

**Disposition.** Reported; awaits the ruling. `reviews/R98_REPORT.md` §2.

---

## D-R98-3 — the §1 count of preregistered predictions moves from 42 to 47

**What happened.** L396's promise that Appendix G "lists every registered prediction and its
outcome" means the CF-2 row enters Table 25 with its five predictions, and the §1 sentence "Of the
$42$ preregistered predictions, $8$ did not hold" counts registrations across that table.

**What changed.** 42 → 47; 8 unchanged, because the first form's failed replication keeps its own
row (R82-CF, "held / failed") and its failure is a fact of that registration, not undone by the
replication that holds.

**Why this is admissible.** A count of registrations, not a result; the R97-7 precedent moved the
same number from 40 to 42 for the S1 row. Recorded for the author's ruling; reverting is one
token and the Table 25 row's "five predictions" phrase.

**Disposition.** Printed; `CLAIMS.md` R98 entry 9c.

---

## D-R98-4 — Table 9's drafting layout changed at the first build

**What happened.** The layout the CLAIMS block described (gain columns in the whole-set block,
first-form values as a column of the counted block, a wide Table 10 row) produced two overfull
boxes (111 pt and 62 pt) at the first build.

**What changed.** The table went to six columns with the two interval columns shared by every
block; the CF-2 gain columns were dropped (the gain is the AUROC less $0.5000$, stated in the
caption) and the first form's gains kept as a column so no v7 value vanishes; the first form's
counted-state values print as three rows, Haiku 4.5's row carrying its paired interval
$[+0.0772,+0.4945]$; the first form's adverse margins moved from the old caption into D.2's history
paragraph; the Table 10 row lost the parenthetical "($90$ in its first form)". `numeric_diff`
reports 0 VANISHED on both sides after the change.

**Why this is admissible.** No value changes; the block was amended in place with the final
layout noted as such (entries 1, 2, 4, 5, 6), and `frozen_diff` was re-run after every change.

**Disposition.** `CLAIMS.md` R98 entries 1, 2, 4; `reviews/R98_REPORT.md` §3.
