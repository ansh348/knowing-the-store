# ADDENDUM_RESP — Amendment 1: the retrieved view under FR-Bank's own lifecycle marks, and Haiku 4.5 on the retrieved-view, hybrid and own-name monitors

Written 2026-09-14 (program R108, the author's pass from the ninth review), BEFORE any call, as a
separate file because `verify_resp.py` check A pins `registrations/ADDENDUM_RESP.md` byte-identical
to `17e6328`. **Descriptive: no bar, no prediction, no verdict; L1-P1, L1-P2, L2-P1 to L2-P3 and the
L3 row stand as printed.** The author's instruction of 2026-09-14: "(2) Register and run the
retrieved-view monitor under FR-Bank's own lifecycle marks in place of the ground-truth join,
GPT-4.1 mini, 661; report beside the oracle-tag row; the box's tag clause becomes conditional on tag
accuracy if it collapses. (3) Register and run Haiku 4.5 at k=5 on the hybrid monitor, then the
retrieved view, then the own-name ablation, cap $12, in that order, stopping if the cap is reached."
Every number prints whichever way it comes out. Frozen by sha256 before the first call (CLAIMS.md
R108 block; `resp_review/NUMBERS_RESP.md` section 7).

## §A — The retrieved view under the store's own marks (GPT-4.1 mini, 661)

**What changes and what does not.** ADDENDUM_RESP §L2 shows the monitor the five entries the store's
own cosine search returns for the question (`l2/retrieval.json`, `top5_ids`, unchanged here), each
rendered by `resp_common.render_line` with the lifecycle tag of the ground-truth join
(`resp_common.true_flags`). This lane re-renders the same five lines with the tag FR-Bank's own
fields give, under the BELIEVED provenance rule of `index_v2.believed_lifecycle`: superseded if the
store marks the entry inactive (`believed_superseded`), retracted if it marks it retracted
(`believed_retracted`), expired if the entry's own `event_time` precedes the persona's cutoff
(`PersonaJoin.cutoff`, the rule the BELIEVED summary uses); category, attribute, age and text are the
same fields as before, so only the `lifecycle:` token of a line can differ. Arm name
`RETRIEVED-BELIEVED`. Prompts `SYSTEM_RETRIEVED` / `USER_RETRIEVED` verbatim (digests `602b9431…` /
`d9031f6f…`, `AUX-RESP-L2-PROMPTS`). `gpt-4.1-mini`, temperature 0, seed 42, max_tokens 200, JSON
mode, k = 1, one retry on a parse failure, the E1 clamp; cache under `resp_review/cache_amend1/`;
served identifier probed before launch (one call).

**Computed before the calls ($0):** the tag census of the 3,305 rendered lines — how many change
tag between the two provenances, and the precision and recall of the store's non-active mark
against the join's, over lines and over the 104 obligations' forbidding records in view
(`AUX-RESP-A1-TAGS`).

**Computed after ($0):** NOK AUROC of `RETRIEVED-BELIEVED` on the 661 and per state (positives of one
state against the same 557 negatives), the paired difference against the recorded `RETRIEVED` row
(`AUX-RESP-L2-MINI-NOK`, 0.6851) and against the committed `INDEXED-TRUE` row (0.7339), item-level
and persona-clustered paired bootstrap (1,000 draws, seed 42), the weaker reading stated; FOK on the
307 descriptive (`AUX-RESP-A1-BELIEVED`).

**The box's tag clause (a reading rule fixed here, no bar):** the paper's system-builder rule
"return non-active records with their lifecycle tags" becomes conditional on tag accuracy if the
view under the store's own marks *collapses*: its whole-population NOK AUROC falls below the
recorded `RETRIEVED` row by more than the tolerance (0.05) with both intervals excluding zero. If it
does not collapse, the clause stays unconditional and the row prints beside the oracle-tag row
either way.

## §B — Haiku 4.5 at k = 5 on the hybrid monitor, the retrieved view, and the own-name ablation

**Lanes, in the order they are submitted:** (1) `HYBRID` on the 661 (`USER_HYBRID`: the committed
TRUE summary and the five ground-truth-tagged lines; digest `b29d1e47…`); (2) `RETRIEVED` on the 661
(`USER_RETRIEVED`, ground-truth tags, as mini's L2 arm); (3) `V2-OWN` on the 102 changed items of
`l1/indexes_own.json` (`prompts_e1.USER_INDEXED` over the own-name-ablated summary, as mini's L1 arm;
the 559 unchanged items take Haiku 4.5's recorded `INDEXED-TRUE` score, as §L1 reads them for mini).
Every lane: `claude-haiku-4-5-20251001`, temperature 0, max_tokens 200, k = 5 (five draws per
item, distinct `custom_id`s), the Anthropic Batch API at its price ($0.50 / $2.50 per 1M), the
system text as the system prompt and the user text as the one user message, the JSON read from the
reply by `run_cf.last_json` and the X4 clamp (`run_cf.make_row`); 3,305 + 3,305 + 510 = 7,120
requests if every lane runs. Served identifier probed before launch (one synchronous call per lane).

**Cap and order:** $12.00 for the three lanes together. Before each lane is submitted, its cost is
projected from its probe's token counts over its requests at Batch prices; a lane is submitted only
if its projection times 1.3 fits within the cap net of what the earlier lanes billed (metered from
their returned rows); a lane that does not fit is not submitted and prints a dash with the reason.
The next lane's turn comes when the previous lane's rows are in. No lane is re-run to fit the cap.

**Scoring ($0):** per lane, draws collapsed as X4 does (`score_cf.load_lane`: at least three draws,
arithmetic mean); NOK AUROC on the population and per state; the paired difference against Haiku
4.5's recorded `INDEXED-TRUE` row (`r74/x4/rows_H45.jsonl`, mean of five draws; 0.8210 on the 661),
item-level and persona-clustered, the weaker reading stated; for `V2-OWN` the difference on the
whole population and per state as `AUX-RESP-L1-MINI` prints them (the unchanged 559 carry the
recorded score on both sides); FOK on the 307 descriptive. Keys `AUX-RESP-A1-H45-HYBRID`,
`-H45-RETRIEVED`, `-H45-OWN`, `-H45-SPEND`.

## §C — Ledger and paper sites

`resp_review/NUMBERS_RESP.md` gains section 7 (`AUX-RESP-A1-LOCK`, `-TAGS`, `-PROBE`, `-PROJECTION`,
`-BELIEVED`, `-H45-HYBRID`, `-H45-RETRIEVED`, `-H45-OWN`, `-SPEND`). Paper (program R108): the
`RETRIEVED-BELIEVED` row beside the `RETRIEVED` row in `tab:resp-l2` (Appendix F.10) and one sentence
in Section 6; the box's tag clause per the reading rule of §A; Haiku 4.5's rows in a block of
`tab:resp-l2` and one sentence per lane in Section 6 (the hybrid and retrieved-view results beside
GPT-4.1 mini's; the ablation beside the own-name sentence). `verify_resp.py` is unaffected.

## Registration mechanics

Frozen by sha256 before the first call (recorded in CLAIMS.md R108 and NUMBERS_RESP.md section 7).
Copied to `iclr2027_monitoring_submission/ARTIFACT/registrations/ADDENDUM_RESP_AMENDMENT_1.md`.
Further amendments append dated sections and never edit the text above.
