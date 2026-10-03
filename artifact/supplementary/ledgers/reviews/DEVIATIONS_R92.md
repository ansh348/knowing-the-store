# DEVIATIONS_R92 — R92-PRESENTATION deviation ledger

Every departure from the presentation-revision prompt (Review G), with a one-line reason.
This program assigns only `D-R92-n` identifiers; the last identifier before it is `D-R91-17`.

Opened 2026-09-11.

| ID | Phase | Deviation | Reason |
|---|---|---|---|
| **D-R92-1** | 2 | The abstract lands as eight sentences, not the seven the prompt orders, in the prompt's order: the text-match result ("There the model does no better than a text match against the summary.") is its own sentence after the 42.3 % sentence. | Joining it to the 42.3 % sentence takes that sentence past the 40-word cap (prose_scan rule L) and joins the retention to the text-match result, which the U9 firewall (L637–638, "no connective joins them, and none may be added") forbids. Ruled at planning (R-a amends S6's band to 7 to 11, which covers eight). |
| **D-R92-2** | 1 | Section 7's kept measurement sentence prints the probe range as $0.7972$ to $0.9662$, not the prompt's "0.80 to 0.97". | The prompt's values are roundings; no ledger carries them and `trace_scan_v13` would report them unaccounted (FR9 precedent, `R91_REPORT.md` section 9). Both exact values print at L699 and L702 already. |
| **D-R92-3** | 4 | The sentence "The monitor scores $0.5959$ on that row and the matcher $0.5858$" (§6 L640), which the prompt names as the form that is not allowed, is not rewritten; the paragraph's free topic sentence (L633) names the judgment, the BELIEVED condition and the full obligation population ($n=661$) instead. | L639–640 are the NB6-2 HOLDS registration pair (`ADDENDUM_R81.md`), frozen registration wording under the ground rule R91 applied at D-R91-3; `frozen_diff` watches them (source R). |
| **D-R92-4** | 4 | No `n` is attached to the three question-set mentions in §7.2 (L727, L730, L733). | They are limitation sentences, not results sentences, and L727 and L730 are R91-quoted forms that `frozen_diff` watches; the prompt's rule is scoped to results sentences. |
| **D-R92-5** | 2, 5 | The mandated finding sentence prints without its contrastive: "… depends on what the memory store writes about itself; the model reading the store does not change that." in place of "…, not on the model reading it." | STYLE_SPEC S9 bars ", not " constructions in main text and `slogan_scan` fails on them; ruling R-b (STYLE_SPEC wins). |
| **D-R92-6** | 1 | The category-shuffle sentences are not moved into Appendix F.5: the pointer sentence stays in §4.4 with a Table 16 pointer added, and the bound clause ("Per-category correspondence is therefore unnecessary on FR-Bank, and the shuffle preserves the global name and count multiset, so it bounds correspondence alone.") is deleted from the main text. | U7 (CLAIMS.md, byte-identical) and the Table 16 footnote already carry the bound in F.5, and R87 D1 deleted the plain-words repeat of U7 that stood beside it; moving the sentences there would re-create that repeat. The prompt's "leave a single pointer sentence for each" is what the retained sentence does. |

Closed 2026-09-11 at R92-6: six deviations, D-R92-1 to D-R92-6; none moves a number.
