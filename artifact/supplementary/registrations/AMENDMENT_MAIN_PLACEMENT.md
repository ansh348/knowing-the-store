# AMENDMENT_MAIN_PLACEMENT — the placement of the registration texts marked [MAIN]

Drafted and applied 2026-09-14 (program R105, the presentation pass) on the author's instruction of that evening
("the [MAIN] placement amendment drafted and applied (frozen texts verbatim to the appendix, one body pointer each,
the rewritten duplicates around them deleted, a dated ledger line left for the author to ratify)"). **Pending the
author's ratification.** Until the author ratifies it, the R104 placement (`paper_v12.tex`, CLAIMS.md R-b of the R104
block) is the registered placement, and `paper_v13.tex` is a draft that departs from it in placement only.

## 1. What the amendment changes, and what it does not

Four registrations mark sentences **[MAIN]** ("destined for main text"): `ADDENDUM_CF2.md` §8 (P1, P3),
`ADDENDUM_R81.md` §6 and Amendment 1 (NB6-1, NB6-2) and §10.3 (the per-state reading (i)), `ADDENDUM_SIDE.md` §S2
(the 42.3 percent sentence and the S2-U branch text, "Section 6 immediately after the 42.3 percent sentence") and
`ADDENDUM_DS.md` §PAPER (the Section 7 paragraph). The main study's frozen verdict sentence on the BELIEVED obligation
row ("NOK degrades materially under believed metadata but remains positive.", CLAIMS.md) sat beside them in the body.

Under this amendment each of those texts prints **verbatim** in the appendix that already holds its siblings (the CF-2
P2 and P4 texts, the R81 branch texts, the SIDE census reading, the RESP and DS appendix texts), and the body keeps
**one pointer sentence per text** naming that appendix. The body's own statement of each finding, written in the pass's
voice, stays; the sentences whose only purpose was to introduce or gloss the pasted text (the lead-in to the DS
paragraph, the gloss on its last sentence, the "weaker reading" gloss) are deleted or rewritten to stand on their own.

Nothing else changes: **no frozen text changes a byte** (section 3 records the sha256 of each text as it stood in the
body and as it stands in its appendix; `reviews/v13/moved_texts.json`), no number changes, no bar, threshold, verdict
or outcome changes, and no registration text above its own marker line is edited. The U9 firewall of `ADDENDUM_R81.md`
(no connective between the NB6-2 pair and any retention sentence) is kept in the appendix as in the body
(`tools/u9_scan.py` PASS on `paper_v13.tex`).

## 2. Why

Three rounds of the R104 acceptance test scored presentation 2 of 4 from both reviewers, and both round-3 reviews
named the frozen texts pasted into the body as a cause ("frozen prediction paragraphs pasted verbatim (end of
Section 8)"; "belongs in the supplement (S.3 already carries it)"; "the DS paragraph both reviews call a repetition of
Table 5"). The registrations fixed the texts' wording before scoring so that the outcome would be reported in words
chosen before it was known; they fixed the placement so that the reported outcome could not be hidden. Printing the
same words verbatim in the appendix, with a body pointer and the body's own statement of the same finding, keeps both
purposes.

## 3. The texts, their registrations, their old and new homes

| tag | registration and section | text (first words) | sha256 of the text | old home (v12) | new home (v13) | body pointer (v13) |
|---|---|---|---|---|---|---|
| CF2-P1 | `ADDENDUM_CF2.md` §8, P1 HOLDS [MAIN] | "On $148$ questions written before any version of the store existed, …" | `77ca09faf977…` | Section 5 | Appendix D.2 | "Appendix~\ref{app:counterfactual} holds the wording fixed before scoring for the smallest model's result here." |
| CF2-P3 | `ADDENDUM_CF2.md` §8, P3 HOLDS [MAIN] | "Naming retracted and expired content lifts Haiku 4.5's judgment …" | `94a9179f5dba…` | Section 5 | Appendix D.2 | "… $+0.30$ with both intervals excluding zero (its pre-scoring wording is in Appendix~\ref{app:counterfactual})." |
| NB6-2 | `ADDENDUM_R81.md` Amendment 1, NB6-2 HOLDS [MAIN] (two sentences) | "Under the metadata the backend actually exposes, …" | `71cb6dae3f29…` | Section 7 | Appendix F.8 | "The model scores $0.60$ on that row and the lookup $0.59$, inside tolerance (Appendix~\ref{app:baselines} carries the two sentences fixed before scoring for this row)." |
| SIDE-S2 | `ADDENDUM_SIDE.md` §S2, the 42.3 percent sentence | "Under the \believed{} index the NOK gain is $+0.1012$ …" | `97376a161687…` | Section 7 | Appendix F.9 | "Appendix~\ref{app:believed-census} reproduces the three sentences fixed before scoring on this row." (one pointer for the three) |
| SIDE-S2U | `ADDENDUM_SIDE.md` §S2, the S2-U not-expected branch (two sentences) | "Lifting the cap on the believed list, …" | `3837adf406ad…` | Section 7 | Appendix F.9 | (as above) |
| E1-VERDICT | the main study's frozen verdict sentence (CLAIMS.md) | "NOK degrades materially under believed metadata but remains positive." | `bbfb02a56b9a…` | Section 7 | Appendix F.9 | (as above) |
| NB6-1 | `ADDENDUM_R81.md` §6, NB6-1 FAILS [MAIN] (two sentences) | "A matcher that scores each question directly against …" | `6da34360b00f…` | Section 8 | Appendix F.8 | "Both readings were fixed before scoring, the whole-population comparison as a sentence pair and the per-state one as a single reading, and Appendix~\ref{app:baselines} carries them." (one sentence, two pointers) |
| NB6-PERSTATE-i | `ADDENDUM_R81.md` §10.3, the per-state reading (i) [MAIN] | "The superseded-names matcher matches the smallest model tested. …" | `d1920ecfa9aa…` | Section 8 | Appendix F.8 | (as above) |
| DS-PARAGRAPH | `ADDENDUM_DS.md` §PAPER, the Section 7 paragraph (AUX-DS-PARAGRAPH-PRINTED) | "Acting on the obligation judgment changes what a bounded view carries. …" | `4297cec12d5c…` | Section 8 | Appendix F.10 | "The paragraph fixed before scoring is reproduced with its numbers in Appendix~\ref{app:resp}, where the $22$ unflagged records are traced to the store's write path." |

The full sha256 of each text, computed over the exact bytes moved (LaTeX source, LF), is in `reviews/v13/moved_texts.json`;
`frozen_diff --program=R105` reports every one of them MOVED with count 1 → 1 and none CHANGED. The NB6-2 second
sentence and the DS paragraph end in a pointer to the appendix they now sit in ("(Appendix~\ref{app:baselines})",
"(Appendix~\ref{app:resp})"); the pointer is part of the printed form the ledgers record and is kept as it is.

Outside this amendment but in the same pass, on the author's order: the CLAIMS-untouchable sentence U6 ("… which we
record as a failed prediction.") moves from Section 9 to the supplement (Section S.9) with a body pointer, byte-identical
and exactly once across paper and supplement (`claims_diff --extra-tex`, `slogan_scan --extra-tex`).

## 4. The body sentences deleted around the moved texts (R105-11 to R105-13, R105-16)

- Section 8: "The paragraph that follows was fixed before scoring and is reported with its numbers; its two bars are …"
  → "The two bars fixed before scoring were a reach gain of $0.50$ for the gold-label fetch and $60\%$ retention of that gain for the gated fetch."
- Section 8: "The paragraph's last sentence counts the oracle policy's $82$ tagged views …" → deleted (it glossed the moved paragraph).
- Section 8: "The weaker reading is the interval grouped by user profile, whose lower end of $0.56$ falls below the $60\%$ bar."
  → "The gated fetch retains $0.76$ of that gain, and under the weaker reading, the interval grouped by user profile, the lower end of $0.56$ falls below the $60\%$ bar."
- Section 3: Remark 1's closing sentence ("The remark's force is that measured premise rather than a deep theorem, …") → deleted (the author's order; not a [MAIN] text).

## 5. Ratification

**Dated line for the author to ratify (2026-09-14):** _The author ratifies AMENDMENT_MAIN_PLACEMENT.md: the [MAIN]
texts of ADDENDUM_CF2, ADDENDUM_R81, ADDENDUM_SIDE and ADDENDUM_DS, and the main study's frozen verdict sentence,
print verbatim in Appendices D.2, F.8, F.9 and F.10 with one body pointer each, as `paper_v13.tex` prints them._ — signed: ______

On ratification, the same line is appended, dated, below the marker of each of the four registrations and to
CLAIMS.md (R105 block, PENDING RATIFICATION → RATIFIED). If the author does not ratify, `paper_v12.tex` stands and the
R105 entries R105-1 to R105-10 are void; the other R105 edits (Remark 1, the tier arithmetic, the Section 8
enumeration, the supplement moves) are independent of this amendment.
