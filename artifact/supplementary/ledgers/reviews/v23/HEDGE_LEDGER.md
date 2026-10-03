# HEDGE_LEDGER.md (R133, 2026-09-21): every qualifier in the running prose of Sections 4 to 8

Written before any edit, on the v23 base (reviews/v23/src/body_v23.tex at 77b0f07; the tex line is that file's). Running prose only: captions, table
cells and notes are not rows (they are acceptable homes). The test (the brief, section 3): a reviewer who reads only the main-text sentence and later
finds the qualifier in the appendix would feel misled (STAYS) or shrug (MOVES). Unsure rows are STAYS and marked `RULING?`. For MOVES the home is the
appendix label or paragraph that already states the fact, or `ADD` when none does (section 4.1: the fact is added to Appendix A's run-coverage table
`tab:runs` or to Table 74, `tab:provenance`, before the hedge leaves the main text). `PINNED` marks a hedge whose only home would be a pinned
(frozen registered or exactly-once) block. Numbers that are not qualifiers (a result's own value) are not rows; the number budget of section 6.1 is
handled in the rewrite and reported in REPORT_R133.md.

| # | Sec. | line | the qualifier (the sentence or clause) | class | reason (five words) | home |
|---|---|---|---|---|---|---|
| H01 | 4 | 237 | "masks non-active records in its stock retrieval configuration" | STAYS | scopes the mask to configuration | -- |
| H02 | 4 | 237 | "Our tag-route experiments turn it off." | STAYS | reader must know mask state | -- |
| H03 | 4 | 239 | "Mini supplies the main study's single-call rows." | MOVES | draw count, run setting | tab:runs (mini: one call, temperature 0) |
| H04 | 4 | 239 | "Haiku, Luna and Opus use repeated calls on the full populations" | MOVES | draw count, run setting | tab:runs (five calls) |
| H05 | 4 | 239 | "Sol also runs the counterfactual test through the raw API." | MOVES | access path, run setting | tab:runs (Sol: the counterfactual set through the raw API) |
| H06 | 4 | 239 | "Every model row in Table 1 averages five draws; its lookup and count readers are deterministic." | MOVES | draw count; Table 1 caption | tab:setup (calls per question) and tab:cf-main's caption (section 4.2: moved there if it costs no line) |
| H07 | 4 | 239 | "Luna's and Sol's shared cross-vendor rows are obtained through the vendor's agent tool." | MOVES | access path, run setting | tab:runs ($^{h}$ rows) and the Appendix A transport paragraph |
| H08 | 4 | 239 | "Sol and Kimi stop at the budget on the full populations." | MOVES | budget stop, run setting | tab:runs (stopped at the budget) |
| H09 | 4 | 239 | "Run coverage and call counts are in Appendix A." | MOVES | pointer; replaced by 4.2's | the one sentence of section 4.2 |
| H10 | 4 | 243 | "with every PN label checked by hand" | STAYS | label source scopes labels | (also tab:provenance, hand-verified) |
| H11 | 4 | 243 | "Intent is fixed by question construction and is not supplied as a label to the reader." | STAYS | what the reader gets | -- |
| H12 | 4 | 243 | "A presence control checks that targets are stored; at the observed base rate, an ABSENT claim still has a 5.2% chance of being wrong." | MOVES | residual error, bookkeeping (3.2) | Appendix E.3, the presence-control paragraph ("At that base rate the chance is 5.2%") |
| H13 | 4 | 245 | "The same renderer caps each list at fifteen names. This cap never binds on the ground-truth lists, but can bind on store-written lists, which we evaluate both capped and uncapped." | STAYS | the cap scopes Section 6 | (shortened to one sentence, 3.1) |
| H14 | 4 | 245 | "For Mem0 and A-MEM, we also render the manifest subject to each backend's constraints. This constrained rendering differs from a summary built from their own fields." | STAYS | constrained rendering is ours | -- |
| H15 | 4 | 248 | "Questions are written before any version exists, so wording cannot predict which version carries the obligation." | STAYS | design guarantee, not bookkeeping | -- |
| H16 | 4 | 252 | "using the sentence encoder all-MiniLM-L6-v2" | MOVES | instrument name, bookkeeping | Appendix C.2 tab:enc-lookup (the recorded encoder row) and Appendix E.8 |
| H17 | 4 | 252 | "It makes no generative-model call." | STAYS | defines the baseline class | -- |
| H18 | 4 | 252 | "Under the summary naming all states, the same lookup reads all non-active names." | STAYS | defines the all-states lookup | -- |
| H19 | 4 | 255 | "The metric fixed in advance pools all items. ... It is post hoc, and we say where the two metrics disagree." | STAYS | matched post hoc (3.1) | (once here, once in Limitations) |
| H20 | 4 | 255 | "A difference is reliable when both the item-level paired and persona-grouped bootstrap intervals exclude zero." | STAYS | defines reliable; S8 follows | -- |
| H21 | 4 | 255 | "Within tolerance means an absolute difference no greater than 0.05." | STAYS | defines the tolerance | -- |
| H22 | 4 | 255 | "A gain compares the same questions with and without the summary." | STAYS | defines gain | -- |
| H23 | 4 | 257 | "Question-only probes can recover labels from the original question wording, which motivates paired comparisons and the counterfactual design." | STAYS | scopes the question-only rows | -- |
| H24 | 4 | 257 | "The predictions were registered with a bar, each before the run that tests it: 31 of 98 came out otherwise. They include follow-ups rather than a single plan fixed before all data collection." | STAYS | 31 of 98; follow-ups (3.1) | -- |
| H25 | 5.1 | 294 | "(a privileged reader: the models must infer the category)" | STAYS | privileged reader (3.1) | -- |
| H26 | 5.1 | 295 | "For 26 of 30 retraction pairs and 15 of 30 expiry pairs that count starts at zero" | STAYS | counts unledgered; nothing added | RULING? (reclassified at the rewrite: no artifact row for the two counts was found, so no appendix note could be added under the numbers lock; the sentence stays in 5.1) |
| H27 | 5.1 | 299 | "on either metric" | STAYS | metrics agree; said once | -- |
| H28 | 5.1 | 299 | "(mini on its single-call row)" | MOVES | run setting (3.2 explicit) | ADD: tab:runs coverage note (the names-and-counts ablation on mini's one-call row); marker † |
| H29 | 5.1 | 300 | "by 0.14 for each model on the matched metric (0.12 and 0.16 pooled)" | MOVES | metrics agree; table carries pooled | tab:cf-names-counts (counts only minus names only, -0.1242 / -0.1562) and tab:cf-matched-ablations |
| H30 | 5.1 | 301 | "(0.77 and 0.75)" (the guessing count reader's per-state values) | MOVES | the ruler's own values | tab:cf-matched (count reader, guessed category: 0.7667 / 0.7500) |
| H31 | 5.1 | 301 | "(Appendix C.2; target-name ablation: Appendix E.10)" | MOVES | pointer; one per subsection | -- |
| H32 | 5.1 | 304 | "which the default summary only counts" | STAYS | names the counted states | -- |
| H33 | 5.1 | 304 | "none is reliably below the guessing count reader" | STAYS | reliability scopes the claim | -- |
| H34 | 5.1 | 305 | "each reliable; mini and Haiku show no reliable change" | STAYS | reliability scopes the claim | -- |
| H35 | 5.1 | 306 | "On the pooled metric the expiry falls are reliable for all three and the retraction falls for Opus alone." | STAYS | metrics disagree on reliability | -- |
| H36 | 5.1 | 307 | "on the pooled metric" (the count-removal costs) | STAYS | pooled only; matched unreliable | -- |
| H37 | 5.1 | 307 | "Sol was not run." | MOVES | run coverage (3.2 explicit) | tab:cf-nc-strong (Sol: not run, dropped by the budget rule) and Limitations; marker † |
| H38 | 5.2 | 361 | "on the matched metric" (first use in 5.2) | STAYS | first use in subsection | -- |
| H39 | 5.2 | 361 | "mini reliably below by 0.07" | STAYS | the one reliable difference | -- |
| H40 | 5.2 | 363 | "none reliably above the lookup" | STAYS | scopes the claim | -- |
| H41 | 5.2 | 363 | "while a list of meaningless tokens and the count reader fall to 0.47 and 0.50" | MOVES | control values, table | tab:cf-sibling (random-token lookup; count reader) |
| H42 | 5.2 | 366 | "(0.07 to 0.08 pooled)" | MOVES | metrics agree; table carries pooled | tab:sup-margins / tab:counterfactual (GPT-5.6 Sol +0.0836, Luna +0.0754; Opus) |
| H43 | 5.2 | 366 | "all of it from retraction and expiry, where the lookup ties every triple" | STAYS | locates the lead | -- |
| H44 | 5.2 | 367 | "fit with personas left out" | MOVES | fitting detail, in Table 1 | tab:cf-main note $^{b}$ and tab:cf-hybrid |
| H45 | 5.2 | 367 | "level with the three models" | STAYS | S7: values + no equivalence test | -- |
| H46 | 5.2 | 368 | "On the pooled metric the same reader scores 0.79 and the three stay a reliable 0.05 to 0.06 above it." | STAYS | metrics disagree (3.1) | -- |
| H47 | 5.2 | 368 | "Their remaining edge is in pairs that cross questions and states, where their scores stay comparable and the fitted reader's do not." | STAYS | explains the disagreement | -- |
| H48 | 5.2 | 371 | "on the two states that were only counted" | STAYS | locates Haiku's gain | -- |
| H49 | 5.2 | 372 | "Opus's 0.03 lead over that lookup is reliable on the pooled metric and not on the matched one, so with every state named no model is reliably ahead on both." | STAYS | metrics disagree (3.1) | -- |
| H50 | 5.2 | 373 | "Luna and Sol did not run this summary." | MOVES | run coverage (3.2 explicit) | tab:runs / tab:setup and Limitations ("only Opus ran the all-states summary"); S7 scopes the lead ("that ran it") |
| H51 | 5.2 | 377 | "scores 0.75 pooled and 0.50 matched" | STAYS | the two metrics disagree | -- |
| H52 | 5.2 | 378 | "on the matched metric" (the random-token margin) | STAYS | metric named, disagreement unknown | RULING? (kept; the pooled margin is in tab:cf-matched-vs) |
| H53 | 5.2 | 383 | "on the full obligation set" (the padded list) | STAYS | population scopes the claim | -- |
| H54 | 5.2 | 383 | "so short ground-truth lists do not establish robustness to longer store-written ones" | STAYS | scopes the claim | -- |
| H55 | 5.3 | 427 | "using the default summary" | STAYS | condition of the crossover | -- |
| H56 | 5.3 | 434 | "The test demonstrates following an explicit rule on cued questions; it establishes no general model advantage over deterministic intent handling." | STAYS | scopes the claim | -- |
| H57 | 5.3 | 438 | "consistent with a scored step that asks whether stale content exists" | STAYS | S10 makes it explicit | -- |
| H58 | 5.3 | 439 | "Opus's behaviour under this underspecified prompt differs from compliance with the explicit rule." | STAYS | scopes Opus's result | -- |
| H59 | 5.3 | 443 | "mini and Haiku do not separate the intents" | STAYS | a result, kept | -- |
| H60 | 5.3 | 444 | "Sol also separates expiry intents under the main-study rubric, scoring 0.64." | STAYS | a result; scopes 'only Opus' | RULING? (kept in the rewrite) |
| H61 | 5.3 | -- | the explicit-intent rows: mini and Luna rerun, the others from the first run (Limitations' sentence) | STAYS | run setting behind 5.3 | ADD: tab:runs coverage note; marker † in 5.3 |
| H62 | 6 | 450 | "at the retrieval surface we evaluated" (Mem0) | STAYS | Mem0 scope (3.1) | -- |
| H63 | 6 | 450 | "in our integration" (A-MEM) | STAYS | A-MEM scope (3.1) | -- |
| H64 | 6 | 487 | "On the full obligation set, its capped store-written summary" | STAYS | population and cap scope | -- |
| H65 | 6 | 488 | "Removing the rendering cap raises their scores without restoring their ground-truth results." | STAYS | capped and uncapped (3.1) | -- |
| H66 | 6 | 490 | "Haiku retains more of its gain than mini does." | STAYS | a result (Haiku 0.71) | -- |
| H67 | 6 | 490 | "The loss is not an artifact of the obligations the alignment misses: on the 82 it marks, the capped summary still costs mini 0.13, Haiku 0.13 and the lookup 0.20, each reliable." | STAYS | alignment can miss; robustness | -- |
| H68 | 6 | 494 | "Its invalidation marks 13 of the 34 full-store obligations it could express, and 11 of the 34 were never extracted into the graph; retraction is inexpressible under this backend's mapping." | STAYS | 11 of 34 (3.1) | -- |
| H69 | 6 | 495 | "over all 47 obligations" and "the store's own name lookup scores 0.68, a reliable 0.10 above mini" | MOVES | population detail; table | Appendix G.4 tab:graphiti-strata and the G.4 prose |
| H70 | 6 | 496 | "On the 23 obligations whose content the graph retains, mini scores 0.69 against 0.84 under ground truth, still a reliable loss." | STAYS | the 23 retained (3.1) | -- |
| H71 | 6 | 499 | "reliably costs mini 0.10 on Mem0 and 0.11 on A-MEM" | MOVES | printed in Table 2 | tab:census lower panel |
| H72 | 6 | 500 | "On questions pooled across them, Luna and Sol also lose reliably; Table 2 gives their losses." | STAYS | Luna raw API vs Sol tool | (Table 2's note keeps the access paths) |
| H73 | 6 | 502 | "Omitting or rewording the unavailable-field marker does not remove the Mem0 loss, and Luna loses 0.27 to 0.34 under every rendering tested through the raw API." | STAYS | U5 conditions, pinned paragraph | PINNED (claims_diff U5; slogan_scan PINNED closing sentence) |
| H74 | 6 | 504 | "Store-written summaries remain within tolerance of question only." | STAYS | a result, scopes the loss | -- |
| H75 | 6 | 505 | "restores mini's coverage to 0.88 on Mem0 and 0.90 on A-MEM" | MOVES | printed in Table 2 | tab:census lower panel |
| H76 | 7 | 512 | "both reliable" (the view's per-state effects) | STAYS | reliability scopes the claim | -- |
| H77 | 7 | 513 | "Haiku's score with both stays within tolerance of its summary alone." | STAYS | scopes 'for mini' | -- |
| H78 | 7 | 517 | "whose precision over retrieved lines is 0.14" | STAYS | quantifies 'despite over-marking' | -- |
| H79 | 7 | 517 | "A reader that merely counts tagged lines scores 0.62 under either tag source." | STAYS | rules out tag counting | RULING? (kept; no appendix row prints 0.62) |
| H80 | 7 | 518 | "On Graphiti, native tags on the same retrieved edges bring no reliable improvement." | STAYS | scopes to FR-Bank | -- |
| H81 | 7 | 522 | "at the matched budget" | STAYS | the comparison's condition | -- |
| H82 | 7 | 549 | "Unmatched, the always-on fetch spends 1.20 times the lines per question; truncated to the gated budget it loses licensed records, a reliable 0.04." | STAYS | the trade-off is the claim | -- |
| H83 | 7 | 552 | "At the matched budget" | STAYS | the comparison's condition | -- |
| H84 | 7 | 556 | "(34 once one inverted ground-truth tag is corrected)" | MOVES | correction bookkeeping | Appendix E.10, the inverted-tag paragraph |
| H85 | 7 | 558 | "An intervention that tags the copies uses the obligations' reference information, so it diagnoses a source of stale use rather than supplying a deployable repair." | STAYS | scopes the intervention | -- |
| H86 | 7 | 561 | "In the assembled views" | STAYS | where the rule runs | -- |
| H87 | 8 | 569 | "models whose question-only score varies" | STAYS | why mini is excluded | -- |
| H88 | 8 | 573 | "their margins fail the persona-grouped interval" | STAYS | the reliability statement | -- |
| H89 | 8 | 573 | "Haiku, Luna and Opus score 0.82 to 0.83" (Sol and Kimi stopped at the budget) | STAYS | comparison set incomplete | ADD: tab:runs coverage note; marker † |
| H90 | 8 | 574 | "mini's advantage over the superseded-name lookup disappears against a lookup over the whole name map" | STAYS | scopes the coverage claim | -- |

Counts: 90 rows; STAYS 68 (RULING? 4: H26, H52, H60, H79; two more, H61 and H89, needed a coverage note added to Appendix A for their marker), MOVES 22 (ADD 1: H28; the other 21 had a home already). Coverage notes added to Appendix A in all: H28 (i), H37 (ii), H50 (iii), H61 (iv), H89 (v). PINNED 1: H73.

## Outcome (the close, 2026-09-21)

Every MOVES row left the running prose of Sections 4 to 8 in the units of `port_r133.py`; REPORT_R133.md section 2 lists each with the appendix label where its fact now lives. H06 (the five-draw sentence) stays in Section 4's models paragraph by section 4.2's test (a caption line). H26 was reclassified STAYS (above). The RULING? rows H52, H60 and H79 stayed as written. The PINNED row H73 is verbatim in Section 6. The five daggers resolve to Appendix A's notes (i) to (v).
