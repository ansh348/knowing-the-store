# DEVIATIONS_R101 — the RESP lanes and the downstream experiment DS landing in `paper_v9.tex`

Date 2026-09-13. Branch `[BRANCH]`. $0: no experiment, no model call, no embedding call. Nothing
here moves a registered bar, threshold, verdict or frozen text. Companion: `reviews/R101_REPORT.md`;
CLAIMS.md **R101 AUTHORIZATION BLOCK**; `ds_downstream/DEVIATIONS_DS.md` D-DS-3 (commit `e14c50e`).

## D-R101-1 — the count of preregistered predictions rises from 47 to 58, and the not-held count from 8 to 16 (for the author's ruling)

§1 (`paper_v9.tex`, the sentence after the contributions) counted 47 preregistered predictions with 8
not holding after R98 (D-R98-3). The RESP lanes registered six items (L1-P1, L1-P2, L2-P1, L2-P2,
L2-P3, L3-P1; one held) and DS five (DS-P1 to DS-P5; two held). On the R97-7 / R98-9c precedent the
sentence now reads 58 and 16. Both registrations froze their bars before any call, as CF-2's did, so
the count treats them as CF-2's five were treated; if the author reads "preregistered" more narrowly
(the submission-time registrations only), the sentence reverts and this entry records the reading.

## D-R101-2 — the page gate

`page_census_v2 paper_v9.pdf`: label on page **10**, reading 536, slack **−51**. The base of this round
(the R99 Phase 1 state, rebuilt from the base tree in a scratch directory): 10, 494, −9; v8 at the R98
close: 10, 501, −16. This round therefore adds 42 review lines to the main text. The order adds
main-text length — §1 three sentences for three (longer), one scope clause; §4.2 two sentences and
a clause; §7 the seven-sentence frozen paragraph, one sentence, and a six-sentence failures paragraph
in place of two sentences; §8 two sentences for two (longer) and a two-sentence box sentence for one;
the abstract one sentence — and cuts nothing on this program's judgment. The residual is the author's
(the R99 restructure, R-b to R-e, has not landed and is the round that moves material).

## D-R101-3 — gate fixes after the first run

The first slogan_scan / prose_scan run reported four failures, all in new prose, none in a frozen text:
(i) the abstract's sentence 2 with the ordered clause ran to 41 words (cap 40), so the clause prints as a
sentence of its own — eight sentences, inside the R99 6–10 band, numerals still in two sentences, the
thesis sentence still last; (ii) the L2 sentence in §4.2 ran to 42 words and loses three ("and the gain
sits on" → "the gain on"); (iii) prose V bans "failed" as an outcome word outside "failed prediction":
the failures paragraph says "did not hold" and "miss"; (iv) the author's authorized sentence ("The two
failed bars were fixed …") keeps its wording verbatim and is entered in prose_scan's WHITELIST as
ordered wording (ORDERED-R101), on the R79 ORDERED precedent. CLAIMS.md R101-17 records the four.

## D-R101-4 — the abstract's word budget

The R99 abstract (CLAIMS.md R99 block, R-a: "under 150 words") stands at 149 words by prose_scan's
counter at the base of this round. The ordered clause is 19 words; it cannot be added within 150
without cutting R99 text, which this order does not authorize. The abstract lands at **168 words**
(eight sentences, every other abstract gate met). The author rules: cut an R99 sentence (the candidate
by content is the sentence on the two structureless backends, since §5.3 and §8 carry it), shorten the
ordered clause, or accept 168.

## D-R101-5 — two instrument extensions, each minimal and recorded

(i) `tools/code_scan.py` ALLOWED gains two collocations that occur only inside the frozen DS paragraph,
"committed obligation score" and "registered detector threshold" (R97 precedent: "registered coverage
floor" for the SIDE frozen text); the bare words stay gated. (ii) `tools/hygiene_scan.py` CITE_TEXT: the
allowlist for the rendered prior-store citation admitted a review-line margin number only after the
second surname; this round's reflow put two citations across a line break so the number fell after the
first surname ("[AUTHOR-1] 219 & [AUTHOR-2], 2026") and between the comma and the year ("…[AUTHOR-2], 494 2026").
The regex now admits an optional 1–3 digit token at those two positions as well; the span must still
carry both surnames and the year, so nothing outside a rendered citation of the prior store is
admitted. Both tools PASS on v8 and on the pre-R101 v9 with the change.

## D-R101-6 — "three quarters" prints as "seven in ten"

The order's premise sentence for §1/§3/§8 says "three quarters a ten-item view". The ledgered reach at
ten items is 74 of 104 = 0.7115 (`AUX-RESP-L2-REACH`); three quarters would overstate it. The
manuscript prints "seven in ten ($74$ of $104$)" in §1 and the count in the appendix; §3 and the
Figure 1 caption carry the five-item figure only. CLAIMS.md R101 block, R-c.

## D-R101-7 — artifacts inside frozen texts, printed verbatim

(i) The frozen L1-P2 failure text says "The per-state reading of Table 20"; Table 20 is the
registration's numbering (v6), now Table 21 (`tab:nb6-composition`) in v9. Frozen wording ships
verbatim (R78-2c); the reader has the pointer in the same subsection. (ii) The frozen L1-P1 held
reading ends "as the manuscript says" — inside the manuscript. Verbatim likewise. (iii) The scorer
had appended the retraction census inside L1-P2's parenthesis; the appendix prints the census as a
sentence beside the frozen text, as the registration sites it ("prints with that census beside it").
(iv) `trace_scan_v13` reports one unaccounted token, `0.72` in the abstract — the R99 Phase 1
rounding of `0.7167`, present at the base of this round and not this round's.

## D-R101-8 — commits

Step 1 (D-DS-3) is committed (`e14c50e`), and the ledger printed forms and the ARTIFACT copies are
committed under this round. The manuscript, CLAIMS.md and the tools are **not** committed: they carry
R93–R99's uncommitted work (pending the author's word, per the R98 report), and a pathspec commit of
`CLAIMS.md` would sweep those blocks into a commit made under this round's name. Each state is instead
recorded as a tree object written from the working copy (`reviews/R101_REPORT.md` §4) so the round is
reproducible by hash; the author commits the paper files on their word.
