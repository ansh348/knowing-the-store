# REPRODUCE: every table and figure, and how its numbers are checked

Two kinds of row. **Regenerated** rows are rebuilt from the stored scores by the named
script and compared byte for byte with the fragment shipped here. **Verified** rows print
numbers that enter the source by hand from a ledger; every one of those numerals is
accounted against that ledger family by `trace_scan_v13`, and the pass's own numbers are
re-derived from their artifacts, independently of the printed forms, by
`r141_number_gate` (which chains R140's, R139's, R137's, R135's and R134's checks: 232 checks (233 inside a git checkout, where the recorded freeze date is also compared with git) in all).

**A verified row is not a regenerated one.** Only the regenerated rows are rebuilt from the
stored scores; the verified rows are checked, number by number, against the ledger their
value was recorded in. `trace_scan_v13` matches set-wise and says so itself: a token counts
as accounted when the string appears anywhere in the ledger family, so an unrelated figure
of equal value would pass it. README.md, under "What 'reproduce' means here", gives the
four layers and what each covers.

`reproduce_all.py` runs all of it. Nothing below needs an API key, a network connection,
a GPU or a LaTeX installation.

```
python reproduce_all.py
```

The paper carries **108 labelled tables and figures**: 15 regenerated, 93 verified.

## Regenerated from the stored scores

| label | what it reports | command | reads | writes |
|---|---|---|---|---|
| `fig:perstate` | Per-state matched AUROC on the counterfactual set ( against within the triple; post hoc); the dashed line is chance. Mini uses five draws, matching Ta | `python reviews/v22/tools/fig3_data_r131.py` | reviews/r125/results/r125_matched.json, fig3_data_matched.tex | `reviews/v22/src/fig3_data_matched.tex` |
| `fig:perstate-pooled` | The pooled version of Figure~ fig:perstate: per-state pooled obligation AUROC on the counterfactual set, each state's positives against all of its ite | `python reviews/v22/tools/fig3_data.py` | reviews/r122/results/scores_r122_oai.json; r82_counterfactual/cf2/results/cf_scores_cf2.json, cf_scores_openai.json; reviews/v18/results/a1_count_readers.json | `reviews/v22/src/fig3_data.tex` |
| `tab:cfpad-counted` | The long-list check on retraction and expiry, 90 items and 30 triples each (descriptive): unpadded/padded/the paired difference, pooled and matched, p | `python cf_pad/tools/cfpad_tex.py` | cf_pad/results/cf_pad_scores.json, cfpad_printed.json | `cf_pad/results/cfpad_tab_<name>.tex` |
| `tab:cfpad-minus-lookup` | The long-list check, supersession (registered): each model minus the name lookup on the same lists, pooled (item-level and persona-grouped intervals)  | `python cf_pad/tools/cfpad_tex.py` | cf_pad/results/cf_pad_scores.json, cfpad_printed.json | `cf_pad/results/cfpad_tab_<name>.tex` |
| `tab:cfpad-other-lookups` | The long-list check, supersession (descriptive): each model minus the lexical lookup and minus the random-token lookup on the same lists, padded and u | `python cf_pad/tools/cfpad_tex.py` | cf_pad/results/cf_pad_scores.json, cfpad_printed.json | `cf_pad/results/cfpad_tab_<name>.tex` |
| `tab:cfpad-position` | The target's alphabetical rank in the version's 60-name list over the 88 supersession triples against each reader (descriptive): Spearman correlation  | `python cf_pad/tools/cfpad_tex.py` | cf_pad/results/cf_pad_scores.json, cfpad_printed.json | `cf_pad/results/cfpad_tab_<name>.tex` |
| `tab:cfpad-sup` | The long-list check, supersession (registered): the 264 items of the 88 supersession triples with the superseded-names list padded to 60 names, every  | `python cf_pad/tools/cfpad_tex.py` | cf_pad/results/cf_pad_scores.json, cfpad_printed.json | `cf_pad/results/cfpad_tab_<name>.tex` |
| `tab:cfpad-whole` | The long-list check on the whole counterfactual set, 444 items and 148 triples (descriptive; the registered comparisons are the supersession slice): e | `python cf_pad/tools/cfpad_tex.py` | cf_pad/results/cf_pad_scores.json, cfpad_printed.json | `cf_pad/results/cfpad_tab_<name>.tex` |
| `tab:para-flags` | The attribute-naming split of Appendix~ app:posthoc-flags recomputed on the paraphrase set (a disclosure; it excludes nothing), under two rules for th | `python cf2_paraphrase/tools/para_tex.py` | cf2_paraphrase/results/para_scores*.json, lookups*.json, sheet.json | `cf2_paraphrase/results/para_tab_<name>.tex` |
| `tab:para-matched` | The same 115 pairs under the matched metric (post hoc): within each triple the version against the version, W/T/L and (W+T/2)/115, on the original que | `python cf2_paraphrase/tools/para_tex.py` | cf2_paraphrase/results/para_scores*.json, lookups*.json, sheet.json | `cf2_paraphrase/results/para_tab_<name>.tex` |
| `tab:para-minus-lookup` | Each model minus the name lookup under the same summary on the whole set of 115 pairs, pooled AUROC with the item-level and the persona-clustered pair | `python cf2_paraphrase/tools/para_tex.py` | cf2_paraphrase/results/para_scores*.json, lookups*.json, sheet.json | `cf2_paraphrase/results/para_tab_<name>.tex` |
| `tab:para-pooled` | The paraphrase check on the 115 accepted pairs (345 items, 115 obligations; registered, descriptive): obligation AUROC on the original questions and o | `python cf2_paraphrase/tools/para_tex.py` | cf2_paraphrase/results/para_scores*.json, lookups*.json, sheet.json | `cf2_paraphrase/results/para_tab_<name>.tex` |
| `tab:para-sens` | Sensitivity, not registered: the same scoring on all 124 screen-passing pairs (372 items), the 115 accepted and the 9 an author's read excluded; origi | `python cf2_paraphrase/tools/para_tex.py` | cf2_paraphrase/results/para_scores*.json, lookups*.json, sheet.json | `cf2_paraphrase/results/para_tab_<name>.tex` |
| `tab:para-sup` | Supersession only (post hoc): each model minus the name lookup under the same summary on the 76 supersession pairs (228 items), on the paraphrases and | `python cf2_paraphrase/tools/para_tex.py` | cf2_paraphrase/results/para_scores*.json, lookups*.json, sheet.json | `cf2_paraphrase/results/para_tab_<name>.tex` |
| `tab:robust` | The checks we ran to break the lookup result, what each removes, and what happened. Short ground-truth lists do not establish robustness to longer sto | `python reviews/v23/tools/robust_tex.py` | reviews/r125/results/r125_matched.json, r125_t4_sibling.json, r125_t5_nc.json; r82_counterfactual/cf2/results/cf_scores_cf2.json, cf_scores_nc.json; cf2_paraphrase/results/para_scores.json; reviews/r122/results/enc_lookup.json; cf_pad/results/cf_pad_scores.json | `reviews/v23/src/robust_table.tex` |

Runtimes are printed by `reproduce_all.py`; the whole chain, including the scoring
bootstraps, finishes in minutes on a laptop without a GPU.

## Verified number by number against the ledgers

Commands (both are run by `reproduce_all.py`):

```
python reviews/r141/tools/r141_number_gate.py --built
cd iclr2027_monitoring_submission && python tools/trace_scan_v13.py paper_v23.tex
```

| label | what it reports | ledger family |
|---|---|---|
| `fig:example` | The Carnival retraction triple: one question, three store versions differing in one attribute. Only the count distinguishes from ; also loses the cate | named by `trace_scan_v13` at the failing token |
| `fig:framework` | A lifecycle summary as a reader sees it: counts by state and attribute names with the values removed. The summary route reads this before retrieval; t | named by `trace_scan_v13` at the failing token |
| `fig:reliability` | Reliability diagram for the pooled hard tier (bins with n 10). The indexed conditions rank well (Spearman =0.9000 intact, 1.0000 names-only) and scale | named by `trace_scan_v13` at the failing token |
| `tab:av-census` | Label structure by item-construction category on the cross-model set (n=84, 40 ). Ranking by category alone attains AUROC 0.9736, above the supervised | named by `trace_scan_v13` at the failing token |
| `tab:baselines` | Mechanical readers of the same serialized summary. ``Best'' is the strongest baseline on that row; the final column is the monitor minus that best, un | named by `trace_scan_v13` at the failing token |
| `tab:believed` |  | e1_metamemory/NUMBERS.md, e1r_robustness/NUMBERS_E1R.md, believed_h/NUMBERS_BELIEVED_H.md |
| `tab:bh-split` | Haiku 4.5 under the store's own metadata, the 63 supersession obligations split by whether the item's own scrubbed name survives in the store-written  | named by `trace_scan_v13` at the failing token |
| `tab:census` | Backend census: counts of disagreement with the manifest-and-alignment reference, without hand adjudication or sampling intervals. Lower panel: covera | r85_graphiti/NUMBERS_R85.md |
| `tab:cf-classes` | The pooled AUROC decomposed by pair class (post hoc). Of the 43,808 positive-negative pairs the pooled AUROC averages over, 296 are within a triple, 1 | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-cr` | The count readers on the counterfactual set beside the models, under the superseded-only summary: AUROC on the whole set and per state, the persona in | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-emptiness` | How much of the lookup is list length and emptiness (post hoc). Upper panel: the superseded-names list of the 88 supersession pairs per store version  | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-fok` | Coverage AUROC on the counterfactual set (n=444; positives the and versions, 296) from the recorded coverage scores, by model and summary, with the in | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-hybrid` | A hybrid reader with no generative-model call on the counterfactual set (registered; ADDENDUM_CF2_HYBRID_READER): a logistic regression of the label o | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-intent` | The intent crossover on the counterfactual set (registered; ADDENDUM_CF2_INTENT_CROSSOVER and its Amendment 1). Each supersession pair of the set is a | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-intent-b` | The intent crossover, continued from Table~ tab:cf-intent: the interaction, the mean of the two-by-two contrast (the original question's version minus | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-main` | Counterfactual obligation AUROC: 88 supersession, 30 retraction and 30 expiry positives. Brackets: persona intervals. The matched column is the within | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-matched` | Every reader of Table~ tab:cf-main under both metrics (post hoc; the matched metric was defined after the pooled rows were known). Pooled: the recorde | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-matched-ablations` | The ablations under the matched metric (post hoc). Upper panel: the names-only, counts-only, totals-randomized and moved-count rows, W/T/L against the | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-matched-vs` | Paired differences under the matched metric (post hoc): the mean over triples of the two readers' per-triple outcomes (a win 1, a tie 12, a loss 0), w | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-names-counts` | Names against counts on the counterfactual set (E2; registered, ADDENDUM_CF2_NAMES_COUNTS). The superseded-only summary with every count line removed  | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-nc-strong` | Names against counts on the three stronger models (E2, Amendment 1; registered, ADDENDUM_R125_E2_AMENDMENT_1). E2's two renderings, byte-identical to  | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-p1` | The counterfactual set under the intent-explicit rubric (registered; ADDENDUM_R122_CF2_P1): GPT-5.6 Luna at five draws and GPT-4.1 mini at one, each a | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf-sibling` | The sibling-name control (registered; ADDENDUM_R125_SIBLING): a fourth version of each of the 88 supersession pairs, rendered from the version's text  | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cf3-expiry` | The expiry state of the counterfactual set extended by a third descriptive draw: the 444's 30 expiry pairs (90 items), the 14 eligible pairs the first | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cluster-sensitivity` | The clustered-sensitivity table reports the registered item-level interval beside the persona-clustered interval for every calibration row. Every clus | named by `trace_scan_v13` at the failing token |
| `tab:counterfactual` | The store-counterfactual set: 148 questions, each asked of three versions of one store differing in a single attribute, so n=444 with 148 positives (8 | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:cov-lookup` | The name lookup, lexical and embedding, on the coverage populations, beside GPT-4.1 mini's recorded blind and indexed coverage AUROC, with the model m | e1_metamemory/NUMBERS.md, e1r_robustness/NUMBERS_E1R.md, believed_h/NUMBERS_BELIEVED_H.md |
| `tab:crossvendor-predictions` | Five items were registered for the three new models. The indexed separation and FOK band held, while the universal blind-NOK baseline failed in opposi | named by `trace_scan_v13` at the failing token |
| `tab:destruction` | The pooled count-destruction probe compares intact, altered-count, and names-only summaries on the hard tier. It shows flat intact-summary calibration | named by `trace_scan_v13` at the failing token |
| `tab:destruction-fr` | The FR-Bank count-destruction probe compares each altered summary with the intact summary. Every manipulated-condition interval includes zero; the dif | named by `trace_scan_v13` at the failing token |
| `tab:dist` | The distribution of GPT-4.1 mini's coverage score on the two structureless stores, question only (blind) against with the summary (indexed) under the  | reviews/r122/NUMBERS_R122.md |
| `tab:ds` | The downstream experiment. Seven registered policies assemble a view from the five retrieved entries and, where a rule fires, the store's non-active r | ds_downstream/NUMBERS_DS.md, reviews/NUMBERS_R130.md |
| `tab:ds-a5` | The answer stage with the store's untagged duplicates tagged (DS Amendment 5, descriptive; no prediction was registered). For each of the 35 obligatio | ds_downstream/NUMBERS_DS.md, reviews/NUMBERS_R130.md |
| `tab:ds-a6` | The answer stage along the depth of the retrieval view (DS Amendment 6, descriptive; no prediction was registered). Views are the first k lines of the | ds_downstream/NUMBERS_DS.md, reviews/NUMBERS_R130.md |
| `tab:ds-a7` | The composite per policy over the full obligation set (661 questions) with its three components (DS Amendment 7, descriptive; no prediction was regist | ds_downstream/NUMBERS_DS.md, reviews/NUMBERS_R130.md |
| `tab:ds-a8` | Label propagation inside the view (E4; registered, DS Amendment 8). A rule that reads only the assembled view propagates a tagged line's lifecycle tag | ds_downstream/NUMBERS_DS.md, reviews/NUMBERS_R130.md |
| `tab:ds-body` | The downstream policies for GPT-4.1 mini on the full obligation set: forbidding records put in view, detector-flagged stale answers at the 0.50 thresh | ds_downstream/NUMBERS_DS.md, reviews/NUMBERS_R130.md |
| `tab:ds-body-lower` | The downstream policies, the columns Table~ tab:ds-body leaves out: the items on which each rule fires, the reach of the forbidding record as a rate ( | ds_downstream/NUMBERS_DS.md, reviews/NUMBERS_R130.md |
| `tab:ds-h45` | The answer stage under Claude Haiku 4.5 as the answerer, every policy, on the same 452 distinct views GPT-4.1 mini answered; the columns of the second | ds_downstream/NUMBERS_DS.md, reviews/NUMBERS_R130.md |
| `tab:e1` | Blind and indexed judgments with the paired gain and both intervals: coverage by backend for GPT-4.1 mini (positives non- ) and the obligation judgmen | e1_metamemory/NUMBERS.md, e1r_robustness/NUMBERS_E1R.md, believed_h/NUMBERS_BELIEVED_H.md |
| `tab:e1-construction` | The main-study record separates frozen design choices from measured checks in pipeline order. It shows how the labels, presence control, leakage scree | named by `trace_scan_v13` at the failing token |
| `tab:e3-groups` | The 104 obligations against the three groups of Table~ tab:e3-intent: (a) the 33 whose own attribute holds a non-active record under current or upcomi | e3_metamemory/DEVIATIONS_E3.md, r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md |
| `tab:e3-intent` | The 661 questions of the full obligation set by intent, label and the state of the question's own attribute. For a question the state is the forbiddin | e3_metamemory/DEVIATIONS_E3.md, r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md |
| `tab:enc-lookup` | The name lookup under two further sentence encoders, and the random-token control (registered; ADDENDUM_R122_ENCODERS): the same lookup code with the  | reviews/r122/NUMBERS_R122.md |
| `tab:equiv` | Equivalence within 0.05 (post hoc): each model minus the name lookup under the same summary, every row printed for the default summary (Tables~ tab:su | named by `trace_scan_v13` at the failing token |
| `tab:equiv-para` | Equivalence within 0.05 on the paraphrase set (post hoc): every row of Tables~ tab:para-minus-lookup and~ tab:para-sup, on the paraphrases and on the  | named by `trace_scan_v13` at the failing token |
| `tab:faults` | The lookup's loss under FR-Bank's measured faults, decomposed after the fact. Each row gives the ground-truth-list score, the score with all three fau | e1_metamemory/NUMBERS.md, e1r_robustness/NUMBERS_E1R.md, believed_h/NUMBERS_BELIEVED_H.md |
| `tab:flag-split` | Obligation AUROC on the counterfactual set by whether the question names the plan or value its attribute is about (89 flagged questions, n=267; 59 unf | named by `trace_scan_v13` at the failing token |
| `tab:gatereach` | What the gate buys, reach only (registered; ADDENDUM_R122_GATE_REACH): three policies assembled from the recorded ranking and the store's records with | resp_review/NUMBERS_RESP.md |
| `tab:graphiti-completed` | Completed Graphiti monitoring on 323 full-store questions, 47 positive obligations. GPT-4.1 mini, one call per input; the name lookup uses the local e | r85_graphiti/NUMBERS_R85.md |
| `tab:graphiti-g10` | The forty-persona Graphiti census against the manifests. Recall is the share of ground-truth events, or forbidding records, on which some Graphiti edg | r85_graphiti/NUMBERS_R85.md |
| `tab:graphiti-strata` | The rows of Table~ tab:graphiti-completed re-scored on strata of the 47 full-store obligations, the 276 negatives unchanged (post hoc; the edges read  | r85_graphiti/NUMBERS_R85.md |
| `tab:inversion` | The table records negative summary effects on structureless stores for every tested model scale. It shows inversion at every scale, while only some sc | named by `trace_scan_v13` at the failing token |
| `tab:ladder-exact` | The exact capability table records the cross-model set on FR-Bank with n=84; luna, sol, and the three new models use k=5, while mini is the original p | named by `trace_scan_v13` at the failing token |
| `tab:ladder-predictions` | Five capability items were registered before the cross-model run. The first four held, while the sol threshold failed, revising the earlier one-call a | named by `trace_scan_v13` at the failing token |
| `tab:length` | The length-only reader (post hoc): its score is the number of names in the superseded-names section of the summary it is given, and nothing else, scor | named by `trace_scan_v13` at the failing token |
| `tab:levels` | Obligation AUROC on the full obligation set (661 questions, 104 obligations) under the ground-truth summary and under FR-Bank's store-written summary, | e1_metamemory/NUMBERS.md, e1r_robustness/NUMBERS_E1R.md, believed_h/NUMBERS_BELIEVED_H.md |
| `tab:levels-strata` | The rows of Table~ tab:levels re-scored on strata of the 104 obligations, the 557 negatives unchanged (post hoc). The alignment of manifest events to  | e1_metamemory/NUMBERS.md, e1r_robustness/NUMBERS_E1R.md, believed_h/NUMBERS_BELIEVED_H.md |
| `tab:lex-444` | The lexical lookup on the counterfactual set beside the embedding lookup, whole set and by state, and each model minus the lexical lookup on the same  | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:margin-661` | Each model minus the name lookup on the 661 obligation questions, for the embedding and the lexical variant of the lookup, with the item-level and the | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:marker` | The inexpressibility marker on the two structureless stores (E3; registered, ADDENDUM_MARKER_ABLATION): coverage AUROC under the constrained rendering | pad_probe/NUMBERS_PAD.md, q4_inversion_probe/NUMBERS_Q4.md |
| `tab:matched-cell` | The authorship-matched set (n=36; 12 , 29 non- ; one generator voice for every label; label transfer 36/36). Blind NOK includes chance on all three mo | named by `trace_scan_v13` at the failing token |
| `tab:mini-k5` | GPT-4.1 mini at five draws on the counterfactual set (registered; ADDENDUM_R122_MINI_K5), under the default and the all-states summary, beside its rec | reviews/r122/NUMBERS_R122.md |
| `tab:nb6-attrib` | Test of the per-state split, controlled for the question signal: blind and indexed discrimination for the three models scored on the full obligation p | named by `trace_scan_v13` at the failing token |
| `tab:nb6-composition` | Post-hoc census of the obligation population under the ground-truth summary, split by the lifecycle state each obligation arises from and scored again | named by `trace_scan_v13` at the failing token |
| `tab:nb6-frontier` | Per-state split for the three models scored on the full obligation population under five calls per question, against the name lookup, with the differe | named by `trace_scan_v13` at the failing token |
| `tab:pad` | The list-length check and its amendment. Upper block: the superseded-names list of each of the 661 main-study summaries padded with correct attribute  | pad_probe/NUMBERS_PAD.md, q4_inversion_probe/NUMBERS_Q4.md |
| `tab:pnpresent` | PN-versus-PRESENT discrimination and within-triple ordering on the counterfactual set, per reader, summary and state (post hoc, specified before recom | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:provenance` | Provenance of the headline numbers: the population, the label source, how records are aligned to labels, the tag source the reader saw, the evaluator, | reviews/NUMBERS_R137.md, reviews/NUMBERS_R135.md (the run and registration records) |
| `tab:q4-marker` | The marker read as absence: GPT-4.1 mini's coverage AUROC on the two structureless stores when one instruction line is appended to the otherwise uncha | named by `trace_scan_v13` at the failing token |
| `tab:questionprior` | Question-only probes measure how much PN label signal is available without a store. Label-supervised term-frequency--inverse-document-frequency (TF--I | named by `trace_scan_v13` at the failing token |
| `tab:reach` | Reach on the full obligation set: forbidding records among the 104 obligations, mean lines over the 661 questions, and licensed records among the 174  | resp_review/NUMBERS_RESP.md |
| `tab:reach-k` | Reach of the forbidding record by the depth of the retrieval view, a census over the 104 obligations from the recorded ten-deep ranking, whole and by  | resp_review/NUMBERS_RESP.md |
| `tab:registrations` | The registration record lists each frozen monitoring artifact, commit, freeze day (day 0 is the first freeze), scope, and outcome. It distinguishes he | named by `trace_scan_v13` at the failing token |
| `tab:registrations-b` | The registration record, continued: the side experiments, the powered counterfactual set, the mechanism tests and the downstream experiment; the Outco | reviews/NUMBERS_R137.md, reviews/NUMBERS_R135.md (the run and registration records) |
| `tab:registrations-c` | The registration record, continued: twelve descriptive registrations, each hashed by the runner before its first call (the commits of day 39 do not da | reviews/NUMBERS_R137.md, reviews/NUMBERS_R135.md (the run and registration records) |
| `tab:registrations-d` | The registration record, continued: the fourth backend's frozen readings, the five registrations of the counterfactual and downstream follow-ups, the  | reviews/NUMBERS_R137.md, reviews/NUMBERS_R135.md (the run and registration records) |
| `tab:registrations-e` | The registration record, continued: the sibling-name control and the names-against-counts amendment on the three stronger models, both registered afte | reviews/NUMBERS_R137.md, reviews/NUMBERS_R135.md (the run and registration records) |
| `tab:repair-completion` | Provisional automated outcomes on the fixed 31-question repair sample. Strict correct / consequential stale endorsement; historical mention alone is n | ds_downstream/NUMBERS_DS.md, reviews/NUMBERS_R130.md |
| `tab:resp-l1` | Own-name ablation. The superseded-names section of the ground-truth summary is re-rendered without the item's own attribute name and every name within | resp_review/NUMBERS_RESP.md |
| `tab:resp-l2` | Retrieved-view and hybrid monitors. The five entries a similarity retriever returns from the item's store, active or not, each with the lifecycle flag | resp_review/NUMBERS_RESP.md |
| `tab:routes` | Obligation AUROC of GPT-4.1 mini on the tagged view, on the full obligation set (661 questions, 104 obligations). is the monitor minus the comparison  | resp_review/NUMBERS_RESP.md |
| `tab:routes-full` | The tagged view, the rows Table~ tab:routes leaves out: Haiku 4.5 on the view and on summary plus view under ground-truth tags, and the four readers w | resp_review/NUMBERS_RESP.md |
| `tab:runs` | Run coverage, model by question set, in the words of the run records. Two runs stopped at the budget on the full populations, so their complete rows a | reviews/NUMBERS_R137.md, reviews/NUMBERS_R135.md (the run and registration records) |
| `tab:s1-names` | The name-bearing summary on the two structureless stores. Each store's recorded coverage items are scored by GPT-4.1 mini against a summary built from | named by `trace_scan_v13` at the failing token |
| `tab:sb60` | The sibling-name control at 60 names (registered; ADDENDUM_R141_SB60): the version with its list padded to 60 names against a fourth version with one  | named by `trace_scan_v13` at the failing token |
| `tab:setup` | The populations, with their sizes and positives and the models that ran on each (calls per question in parentheses). The body refers to a population b | reviews/NUMBERS_R137.md, reviews/NUMBERS_R135.md (the run and registration records) |
| `tab:sup-margins` | Each model's supersession-only margin over the name lookup on the counterfactual set under the default summary (88 pairs, 264 items; the lookup reads  | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:sup-triple` | The supersession triple of the counterfactual set that Figure~ fig:example leaves out: the question is fixed, the three store versions differ in one a | r82_counterfactual/cf2/NUMBERS_CF2.md, r82_counterfactual/NUMBERS_R82.md |
| `tab:v2rcat` | The moved-count control: each model under the moved text against its recorded superseded-only row, whole set and per state, with the paired difference | e3_metamemory/DEVIATIONS_E3.md, r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md |
| `tab:wrongindex` | The registered wrong-summary control replaces only the summary text and holds the question, prompts, protocol, and populations fixed; the intact condi | named by `trace_scan_v13` at the failing token |
| `tab:x2-ablation` | The summary-ablation probe removes candidate channels from the external-store summaries. No single channel separates from the intact inversion; removi | named by `trace_scan_v13` at the failing token |
| `tab:x4-expansion` | The full-population runs: blind and indexed FOK and NOK for every model that completed, with the paired gain and both intervals. The paired separation | named by `trace_scan_v13` at the failing token |

## Path (b): how the API runs were made

Nothing in this section is needed for any printed number. The runners are in `runners/`,
their frozen prompts in `prompts/`, the registration that preceded each run in
`registrations/`, and the lock record each runner wrote at the run's start (the
registration's sha256, the model id, the cap) beside it. Each runner reads its key from an
environment variable and refuses to start without one. They are shipped so a reader can
see exactly what was sent, not so the runs are repeated: provider availability, model
changes and sampling make an exact historical regeneration impossible, and the stored rows
are the record.

Requires API keys and budget; not needed for any printed number.

### Costing a run before it is made

Two runners take a literal `--dry-run` flag: `cf_pad/tools/run_cf_pad.py` and
`r85_graphiti/g10/ingest_all.py`. The rest use this project's own convention instead, which
is what the registrations require and what the ledgers record, so it is what is shipped:

1. **`probe <lane>`**: one real call on one unit, to confirm the served model identifier
   matches the pinned one and to measure tokens in and out. It writes `probes.json` with
   the served identifier, the per-unit tokens, and a projection of the whole lane's cost
   (`projection.usd`) together with that figure multiplied by 1.3.
2. **the headroom rule**: a lane is submitted only if its 1.3x projection fits inside both
   the registered cap and the overall cap, computed from every lane already billed. A lane
   that does not fit prints a dash and is not run. `score_para.py`'s `headrooms()` and
   `billed_so_far()` are the reference implementation.
3. **the lock record**: written at the run's start, before the first scored call, namely the
   registration's sha256, the model identifier, the cap. Those are in `registrations/`
   beside the registration each one seals.

So the cost of every run was projected before it was made and the projection is on record;
it was done by a one-call probe against a cap rather than by a no-call dry run. To read a
lane's prompts without calling anything, the builders that assemble them
(`build_*.py`, `*_build.py`, `draft_*.py` in `scoring/`) run offline and write the prompt
texts to disk.

