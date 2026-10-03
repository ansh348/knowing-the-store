# DEVIATIONS_R97 — R97-RESPONSE (2026-09-13)

Own numbering from D-R97-1. Each entry records a point where the landed text differs from the
order or from a frozen text, with the rule that forced it and what the author can do about it.
Nothing here is a measurement; R97 made no model call.

---

## D-R97-1 — the limitations sentence lands without the clause "the authors' own prior system"

**What happened.** Order item (6) asked for a self-interest sentence: the lifecycle schema is
the authors' own prior system; the audit applies to it first; labels come from the manifests; S1
shows the benefit is the summary, not the system. The submission is under double-blind review
(`\author{Anonymous Authors}`, `% \iclrfinalcopy` commented), the R89 BRANCH A ruling requires
every reference to the prior store to be the named third-person citation, and `hygiene_scan`
rule 5 fails first-person self-reference near that citation. Writing "the authors' own" beside
"([AUTHOR-1] & [AUTHOR-2], 2026)" identifies the authors.

**What landed.** Two sentences after "One closed model family supplies the primary capability
comparison.": "The lifecycle schema this study builds on is that of the prior store \citep{fr},
so the audit of Section 6 applies to that store first." and "Every label comes from the manifests
we built, and Section 5.3 shows the benefit travels with the summary rather than with the
system." Every element of the order except the ownership clause is in them.

**Camera-ready wording, for the author to land at de-anonymization.** "The lifecycle schema this
study builds on is our own prior system \citep{fr}, so the audit of Section 6 applies to it first;
every label comes from the manifests we built, and Section 5.3 shows the benefit travels with the
summary rather than with the system." `hygiene_scan`'s first-person patterns would need the
BRANCH A carve-out lifted at the same time.

**Disposition.** CLAIMS.md R97 block, ruling R-d and entry 6.

---

## D-R97-2 — the main text ends on page 10: the page gate fails by nine review lines

**What happened.** `page_census_v2 paper_v7.pdf`: label on page **10**, reading **494**, slack
**−9** (v6: page 9, 469 / +16). The order's main-text additions come to about 27 review lines
(§1 +1.5, Figure 1 caption +1, Table 1 footnote +1, §4.3 +2, §5.1 +1.5, §5.3 +10.5, §6 +7.5,
§7 +3, §8 +1.5) against a slack of 16. The boxed closing paragraph of §8 is an unbreakable
nine-line minipage, so the last nine lines of main text sit on page 10 as one block.

**What was done.** Every non-frozen new sentence was taken to its shortest form under the
30-word target (merges that saved no line were undone, since they only lengthened sentences);
the Table 1 footnote is one line; the §6 weaker-reading sentence carries the disagreement and
points at F.9 for the two intervals. The frozen texts cannot be shortened. Nothing existing was
cut and no ordered content was moved on this program's judgment.

**What clears it — a ruling is needed; line costs are review lines at the current layout.**
Any combination reaching nine (ten for safety) brings the label back to page 9.

| Option | Lines | What it touches |
|---|---:|---|
| (a) The frozen Mem0 descriptive text moves to Appendix F.7 (its registered home under §S1 "appendix only"); §5.3 keeps one clause, "Mem0's row is descriptive: its summary covers $49.4\%$ of the store, below the coverage floor of one half (Appendix F.7)." | −2.5 | ADDENDUM_SIDE §A1's "prints beside in §5.3 in its frozen wording"; needs an amendment line |
| (b) The §6 interval sentence and the weaker-reading sentence move to F.9 only (F.9 already carries both) | −2.5 | §A1's "with its intervals ... and the weaker reading ... stated beside it" |
| (c) The §6 threshold-provenance sentence is dropped (F.3 carries the full statement) | −1 | order item (5), Q6's §6 site |
| (d) The §5.3 mechanical-readers sentence keeps only "and the mechanical readers recover it too"; the numbers stay in F.7 | −1 | order item (1) |
| (e) The second limitations sentence (labels from the manifests; S1 shows the benefit is the summary) is dropped; the first stays | −1.5 | order item (6) |
| (f) The §4.3 W6 sentence is dropped (both of its figures already print at L506 and L655) | −2 | order item (5) |
| (g) The Table 1 footnote is dropped and the ‡ is explained by the caption's existing fourth sentence | −1 | order item (5) |
| (h) An existing sentence is cut (candidates: the two ablation-hypothesis sentences of §5.3, about 4 lines; the Haiku 4.5 counterfactual pair of §6, about 3 lines) | −3 to −4 | text landed under earlier rulings |

**Disposition.** CLAIMS.md R97 block, GATES; `reviews/R97_REPORT.md` §2. The build is
delivered with the gate failing and reported as such.

---

## D-R97-3 — the Q6 clause is not appended to the 42.3 percent sentence

**What happened.** `reviews/RESP_REG_REPORT.md` §5 item 6 drafted Q6 at two sites, Appendix F.3
and a clause on the §6 sentence "That keeps $42.3\%$ of the \trueidx{} gain, short of the $60\%$
we had set as the threshold" ("…, a round number fixed before any data (Appendix F.3)").
`ADDENDUM_SIDE.md` §STOP lists "the 42.3 percent sentence at `paper_v4.tex:641` changed" as a
stop condition and §A1 says the sentence "stays as printed".

**What landed.** F.3 carries the full sentence as drafted; §6 carries the provenance as a
sentence of its own after the S2-U block, "The $60\%$ threshold is a round number fixed before
any data (Appendix F.3)." The 42.3 percent sentence is byte-identical to v6.

**Disposition.** CLAIMS.md R97 block, ruling R-b and entry 5g. If the author prefers the
clause form, it needs a SIDE amendment line first.

---

## D-R97-4 — the RESP pointers are held back and no RESP row is printed in Table 24

**What happened.** `registrations/ADDENDUM_RESP.md` is frozen (`17e6328`, R98) and Phase B has
not run: no `resp_review/` artifact exists except the one ledger key written under R97-8. The
report's items 10 and 11 attach "is measured in Appendix~\ref{app:resp}" to the §1 premise, the
Figure 1 caption and the F.8 own-name sentence, and say the clause is held back if R97 lands
before Phase B. The RESP registration's mechanics add one Table 24 row per lane once the freeze
commit exists, with outcomes starting "pending".

**What landed.** The three sentences without the pointer clause (F.8's replacement says the
question "is a separate question that this census does not settle"). No Table 24 row for L1, L2
or L3: a row whose outcome reads "pending" in a paper under review was judged the author's call;
`reviews/RESP_REG_REPORT.md` §7 step 6 assigns the rows to R97 after Phase B.

**Disposition.** CLAIMS.md R97 block, ruling R-c. Both land with Phase B's results.

---

## D-R97-5 — one §1 number moves on S1's account: 40 preregistered predictions become 42

**What happened.** `ADDENDUM_SIDE.md` says no headline number in the abstract or §1 changes on
S1's or S2's account, and §A1 lists the §1 lines that stay as printed (:158, :159, :169). L174's
"Of the $40$ preregistered predictions, $8$ did not hold" is the count of registered predictions
in Table 24. L396 promises that Appendix G "lists every registered prediction and its outcome",
so once S1's two predictions print in §5.3 the S1 row enters Table 24 and the count is 42.

**What landed.** Table 24 gains the S1 and S2 rows (`e8b2630`, 2026-09-12) and L174 reads 42;
"8 did not hold" is unchanged. The 42 is a count of registrations, not a result, and L174 is
not among the lines §A1 names.

**Disposition.** CLAIMS.md R97 block, ruling R-e and entry 7. Reverting is one token and one
table row if the author reads the registration's rule as covering it.

---

## D-R97-6 — the Q4 ledger key is written before Phase B step 1

**What happened.** The order's Q4 figure prints the marker fraction; `ADDENDUM_RESP.md` routes
that number through `AUX-RESP-PAPER-Q4` in `resp_review/NUMBERS_RESP.md`, to be written at
Phase B step 1, and the report says R97 may print it only after the key exists.

**What landed.** `resp_review/NUMBERS_RESP.md` with its header naming the freeze and the one
key, recomputed from `e1_metamemory/indexes_v2.json` with `tiktoken` `o200k_base` (no model
call), equal to §C.5 to the token, and carrying the two verbatim `leila` texts so that every
number inside them has a ledger row. `verify_resp.py` and `DEVIATIONS_RESP.md` are not written;
they are Phase B step 1's.

**Disposition.** CLAIMS.md R97 block, entry 8.

---

## Cross-references

- **D-E1R-10** (`e1r_robustness/DEVIATIONS_E1R.md`, `cc06e2e`): the own-name census keyed entry
  ids without the persona; corrected in the manuscript under R97 entry 4a.
- **ADDENDUM_SIDE.md §A1** (`07506f1`): the S1 and S2-U main-text placements R97 lands.
- Sites that keep the ranking wording of the 5% premise and are not in the ruling (for the
  author): abstract L51 "can rank below the cutoff"; §3 L345 "pass similarity retrieval at $5\%$"
  (CL-C136); §8 L737 "can sit outside them"; the Figure 1 drawing's top-$k$ cutoff line with the
  retracted row below it.
- The order's two-decimal figures (A-MEM 0.45 → 0.90, Mem0 0.48 → 0.88) print at the ledger's
  four decimals (0.4526 → 0.8974, 0.4777 → 0.8751) under PRECISION-R81-1 and the numbers lock.
