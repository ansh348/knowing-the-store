# Reproducibility artifact — "Knowing the Store: What a Memory Backend Must Write Down Before an Agent Can Read It"

This bundle is what the paper's reproducibility statement promises: **the frozen registrations with
their commit hashes, the prompts, the item manifests, the raw monitoring rows, the scoring scripts,
the summary renderer and the backend versions**. Appendix F of the paper records the design and
verification details needed to interpret the contents; Appendix G (**Tables 38, 39 and 40**) is the
registration record that this bundle's `registrations/` directory realizes; the supplement carries
the instrument ledger, the deviation index, the prediction texts written before scoring, the
per-provider run disclosures and the glossary that maps this bundle's internal names onto the
paper's terms.

**Refreshed 2026-09-14 for the submitted build (paper_v13).** The paper carries **40 tables and
1 figure**; the pilot table of earlier builds is in the supplement (Section S.7). Every table number in
this file is a **paper_v13** number, verified against `paper_v13.aux`. The bundle holds the row trees of
the counterfactual set (`rows/cf2/`) and its expiry extension with the candidate census (`rows/cf3/`), the mechanism tests (`rows/resp/`), the downstream experiment
(`rows/ds/`), the marker probe (`rows/q4/`), the full-population expansion (`rows/x4/`), the side
experiments (`rows/side/`) and the offline analyses of the v12 pass (`rows/v12/`); the scoring code
(`code/`); the ledgers of the last four passes; the registration texts of every experiment, including the
two registered checks whose results land after this build (`ADDENDUM_PAD.md`, run; `ADDENDUM_PARA.md`,
at the author's read), the expiry extension (`ADDENDUM_CF3.md`, run, Table 16, ratification line pending) and the placement amendment awaiting the author's ratification
(`AMENDMENT_MAIN_PLACEMENT.md`); and `BACKENDS.md`, the backend versions. Author names, machine paths, git
identities and institution strings were scrubbed from every text file; the scan report is in this bundle
as `ARTIFACT_SCAN.md`.

## Every printed table, and the file it comes from

Paths are relative to this directory. "Ledger" names the number record of last resort; the paper's
numeric gate (`trace_scan_v13.py`, shipped in `verifier/`) accounts every printed token against
that family (its `LEDGERS` list names the repository paths; the same files are in `ledgers/`).
Row files under `rows/cf2`, `rows/resp`, `rows/ds`, `rows/q4`, `rows/x4`, `rows/side` and
`rows/v12` are named by their basename; the older trees keep their original layout.
Each September runner's lock record, the registration's sha256 written at the run's start, sits beside its rows
(`rows/ds/lock_amend1.json` to `lock_amend4.json`, `rows/resp/lock_amend1.json`, `rows/q4/lock_q4.json`); Appendix F of
the paper names the registrations whose pre-run evidence is that record rather than a commit (R116).

| # | Label | What it reports | Row file(s) | Ledger |
|---|---|---|---|---|
| 1 | `tab:cf-main` | The counterfactual set, whole set: three models, two lookups, model minus lookup | `rows/cf2/cf_scores_cf2.json`, `rows/cf2/rows_MINI.jsonl`, `rows/cf2/rows_H45.jsonl`, `rows/cf2/rows_OP5.jsonl`, `rows/v12/margin_intervals.json` | `NUMBERS_CF2.md`, `NUMBERS_R103.md` |
| 2 | `tab:routes` | The retrieved view alone and with the summary, 661 questions | `rows/resp/scores_resp.json`, `rows/resp/rows_resp.jsonl`, `rows/resp/retrieval.json` | `NUMBERS_RESP.md` |
| 3 | `tab:believed` | What each backend writes about itself; retention under FR-Bank's own metadata | `rows/e1/backend_census.json`, `rows/e1/believed_frbank.json`, `manifests/cf_pairs.json`, `rows/e1r/believed_nok.json`, `rows/side/s2/` | `NUMBERS.md`, `NUMBERS_R82.md`, `NUMBERS_E1R.md`, `NUMBERS_SIDE.md` |
| 4 | `tab:e1` | Full populations: coverage by backend, obligation by model, the lookup on the coverage tiers | `rows/e1/elicitation_main.json`, `rows/e1_results/scores_e1.json`, `rows/x4/x4_scores.json`, `rows/v12/phase1.json` (key `item1`) | `NUMBERS.md`, `NUMBERS_R74.md`, `NUMBERS_R104.md` |
| 5 | `tab:ds-body` | The downstream experiment at matched budget | `rows/ds/scores_ds.json`, `rows/ds/views.json`, `rows/ds/policies.json`, `rows/ds/scores_amend1.json`, `rows/v12/phase1.json` (key `item4`) | `NUMBERS_DS.md`, `NUMBERS_R104.md` |
| 6 | `tab:ladder-exact` | Matched 84-item cell, 12 rows across six models | `rows/e1_results/ladder_scores.json`, `rows/e1xv/`, `rows/e1r/clustered_ladder.json` | `NUMBERS.md`, `NUMBERS_E1XV.md` |
| 7 | `tab:x4-expansion` | Full FR-Bank populations, four completed lanes | `rows/x4/x4_scores.json`, `rows/x4/rows_*.jsonl`, `rows/r74/x4/` | `NUMBERS_R74.md` |
| 8 | `tab:ladder-predictions` | Five registered capability items and outcomes | `registrations/LADDER_ADDENDUM_E1_7.md`, `rows/e1_results/ladder_scores.json` | `NUMBERS.md` |
| 9 | `tab:crossvendor-predictions` | Five registered cross-vendor items and outcomes | `registrations/PREREG_E1XV.md`, `rows/e1xv/` | `NUMBERS_E1XV.md` |
| 10 | `tab:questionprior` | Question-only probes | `rows/e1qp/probe_tfidf.json`, `rows/e1qp/probe_llm.json`, `rows/e1qp/e1qp_scores.json`, `rows/r74/x1/x1_results.json` | `NUMBERS_E1QP.md`, `NUMBERS_R74.md` |
| 11 | `tab:matched-cell` | The 36-question set rewritten in one voice | `rows/r74/x5/x5_scores.json`, `rows/r74/x6/x6_ns5_scores.json`, `rows/r74/x6/x6_probes.json` | `NUMBERS_R74.md` |
| 12 | `tab:av-census` | Label structure by item-construction category | `rows/r74/x6/x6_probes.json` key `AV_CENSUS` | `NUMBERS_R74.md` |
| 13 | `tab:counterfactual` | The counterfactual set by state, both summaries, the count-randomized control, the first form | `rows/cf2/cf_scores_cf2.json`, `rows/cf2/cf_cell.json`, `rows/cf2/cf_indexes.json`, `rows/r82/cf_scores.json` | `NUMBERS_CF2.md`, `NUMBERS_R82.md` |
| 14 | `tab:cf-fok` | Coverage on the counterfactual set | `rows/v12/phase1.json` (key `item2_fok_444`) | `NUMBERS_R104.md` |
| 15 | `tab:lex-444` | The lexical lookup on the counterfactual set and each model minus it | `rows/v12/phase1.json` (keys `item3_444_lookups`, `item3_444_margins`) | `NUMBERS_R104.md` |
| 16 | `tab:cf3-expiry` | The expiry state of the counterfactual set extended by a third descriptive draw: the 444's 30 expiry pairs, the 14-pair extension, and the two pooled (44 pairs) | `rows/cf3/cf_scores_cf3.json`, `rows/cf3/cf_cell.json`, `rows/cf3/cf_indexes.json`, `rows/cf3/rows_MINI.jsonl`, `rows/cf3/rows_H45.jsonl`, `rows/cf3/rows_OP5.jsonl`, `rows/cf2/rows_MINI.jsonl`, `rows/cf2/rows_H45.jsonl`, `rows/cf2/rows_OP5.jsonl` (the 444's expiry slice, never re-run) | `NUMBERS_CF3.md` |
| 17 | `tab:e1-construction` | Construction records and measured checks | `manifests/items_final.json`, `rows/e1/verify_results.json`, `rows/e1/verify_pending.json`, `rows/e1/probe_verification.json` | `NUMBERS.md` |
| 18 | `tab:wrongindex` | Wrong-summary and category-shuffle controls | `rows/r74/x7/x7_scores.json`, `rows/r74/x7/rows_SWAP.jsonl` | `NUMBERS_R74.md` |
| 19 | `tab:cluster-sensitivity` | Item-level beside persona-clustered intervals | `rows/e1r/clustered.json` | `NUMBERS_E1R.md` |
| 20 | `tab:destruction` | Pooled count-destruction probe, with ECE | `rows/e1_results/mechanism_scores.json`, `rows/e1r/ece.json` | `NUMBERS.md`, `NUMBERS_E1R.md` |
| 21 | `tab:destruction-fr` | FR-Bank count-destruction probe | `rows/e1_results/mechanism_scores.json` | `NUMBERS.md` |
| 22 | `tab:inversion` | Negative summary effects on the structureless stores | `rows/e1_results/scores_e1.json`, `rows/e1_results/ladder_scores.json` | `NUMBERS.md` |
| 23 | `tab:x2-ablation` | Summary-channel ablation on the external stores | `rows/r74/x2/x2_scores.json`, `rows/r74/x2/x2_elicitation.json` | `NUMBERS_R74.md` |
| 24 | `tab:q4-marker` | The marker-as-absence probe | `rows/q4/q4_scores.json`, `rows/q4/q4_elicitation.json`, `rows/q4/lock_q4.json` | `NUMBERS_Q4.md` |
| 25 | `tab:s1-names` | The name-bearing summary on the two structureless stores | `rows/side/s1/` | `NUMBERS_SIDE.md` |
| 26 | `tab:dist` | Score distributions on the structureless stores, blind and indexed | `rows/v12/phase1.json` (key `item5`) | `NUMBERS_R104.md` |
| 27 | `tab:baselines` | Six mechanical readers of the same summary | `rows/e1r/baselines_final.json`, `rows/e1r/baselines_final_r81.json`, `rows/e1r/nb6.json` | `NUMBERS_E1R.md` |
| 28 | `tab:nb6-composition` | Obligation population split by lifecycle state | `rows/e1r/nb6_composition.json` | `NUMBERS_E1R.md` |
| 29 | `tab:nb6-attrib` | Paired indexed-minus-blind difference per state | `rows/e1r/nb6_attribution.json` | `NUMBERS_E1R.md` |
| 30 | `tab:nb6-frontier` | Per-state split against the superseded-names lookup | `rows/e1r/nb6_perstate.json` | `NUMBERS_E1R.md` |
| 31 | `tab:margin-661` | Each model minus the two lookups on the 661 questions | `rows/v12/phase1.json` (key `item3_661`, with the paired intervals under `margins`) | `NUMBERS_R104.md` |
| 32 | `tab:cov-lookup` | The superseded-names lookup on the coverage tiers | `rows/v12/phase1.json` (key `item1`) | `NUMBERS_R104.md` |
| 33 | `tab:resp-l1` | The own-name ablation | `rows/resp/scores_resp.json`, `rows/resp/indexes_own.json`, `rows/resp/nb6_own.json` | `NUMBERS_RESP.md` |
| 34 | `tab:resp-l2` | The retrieved view and the hybrid monitor, per state | `rows/resp/scores_resp.json`, `rows/resp/retrieval.json`, `rows/resp/reach.json` | `NUMBERS_RESP.md` |
| 35 | `tab:ds` | The downstream experiment, every policy | `rows/ds/scores_ds.json`, `rows/ds/stage1.json`, `rows/ds/rows_ds.jsonl`, `rows/ds/cell_ds.json` | `NUMBERS_DS.md` |
| 36 | `tab:reach-k` | Reach by ranking depth | `rows/v12/phase1.json` (key `item4`) | `NUMBERS_R104.md` |
| 37 | `tab:registrations` | The registration record, part one | `registrations/` (one file per row) | all ledgers |
| 38 | `tab:registrations-b` | The registration record, part two: side experiments, the powered counterfactual set, the mechanism tests, the downstream experiment | `registrations/ADDENDUM_SIDE.md`, `ADDENDUM_CF2.md`, `ADDENDUM_RESP.md`, `ADDENDUM_DS.md` | `NUMBERS_SIDE.md`, `NUMBERS_CF2.md`, `NUMBERS_RESP.md`, `NUMBERS_DS.md` |
| 39 | `tab:registrations-c` | Five descriptive registrations (four run, one at the author's read) | `registrations/ADDENDUM_Q4.md`, `ADDENDUM_DS_AMENDMENT_1.md`, `ADDENDUM_PAD.md`, `ADDENDUM_PARA.md`, `ADDENDUM_CF3.md` | `NUMBERS_Q4.md`, `NUMBERS_DS.md`, `NUMBERS_CF3.md` |
| 40 | `tab:flag-split` | The counterfactual set split by whether the question names its attribute | `rows/v12/flag_split.json`, `rows/cf2/question_read_flags.json` | `NUMBERS_R103.md` |

| Fig. | Label | Source |
|---|---|---|
| 1 | `fig:reliability` | `rows/e1r/reliability.json`, rendered at `rows/e1r/reliability.pdf` |

## Directory layout

| Directory | Contents |
|---|---|
| `registrations/` | The frozen registration texts behind every row of Tables 37 to 39, plus `SPEC_E1R.md` (the offline robustness pass's frozen analysis rules) and `ADDENDUM_R85_GRAPHITI.md` (the fourth-backend trial). `ADDENDUM_PAD.md` (run), `ADDENDUM_PARA.md` (at the author's read) and `ADDENDUM_CF3.md` (run; Table 16) are the descriptive registrations whose sha256 prefixes print in Table 39. |
| `ledgers/` | The number records (`NUMBERS_*.md`) and the deviation records (`DEVIATIONS_*.md`) of every pass. A ledger key (for example `AUX-R104-COV-LOOKUP`) is the record the paper's numeric gate resolves a printed token to. |
| `manifests/` | The item manifests: `items_final.json` (the main-study items), `cf_pairs.json` (the counterfactual pairs) and the persona manifests the stores were built from. |
| `prompts/` | The elicitation rubric and the user prompts, blind and indexed. |
| `rows/` | Raw monitoring rows and scored results, one directory per experiment: `e0` (pilot), `e1` and `e1_results` (main study), `e1qp` (question-only probes), `e1r` (offline robustness), `e1xv` (cross-vendor), `e2`, `r74` (the x1 to x7 probes), `r82` (the first counterfactual form), `cf2` (the counterfactual set of Table 1), `cf3` (the expiry extension of Table 16, with `CF3_CENSUS.md` and `census_cf3.json`, the candidate census), `resp` (the mechanism tests), `ds` (the downstream experiment), `q4` (the marker probe), `x4` (the full-population expansion), `side` (the name-bearing summary and the lifted cap), `v12` (the offline analyses of the last pass, including the detector labeling sheet and sample). |
| `code/` | The scoring scripts, the summary renderers (`index_v2.py`, `index_v3.py`, `index_v2r.py`), the lookups (`run_nb6.py`, `score_cf.py`), the builders and runners of every experiment, and the verifiers of the counterfactual, mechanism, downstream and side experiments (`verify_cf2.py`, `verify_resp.py`, `verify_ds.py`, `verify_side.py`). Files are named by their repository path with `__` for `/`. `lifecycle_bank.py` is the lifecycle-tracking store. |
| `verifier/` | The value verifiers of the earlier passes (`verify_numbers.py`, `verify_e1qp.py`, `verify_e1r.py`, `verify_e1xv.py`, `verify_r74.py`), the scorers, and the numeric gates (`trace_scan_v10.py`, `trace_scan_v11.py`, `trace_scan_v13.py`). |
| `BACKENDS.md` | The version or pin of every backend that was run. |

## How the numbers were checked

Every printed number in the paper resolves, through `trace_scan_v13.py`, to a ledger row, a bridge
row or a verified derivation; the ledgers name the row file each value was read from. The
verifiers recompute the scored results from the raw rows and assert the ledgered values. The
registrations were frozen by sha256 (Table 39) or by commit hash (Tables 37 and 38) before the
first call of each experiment; the texts here are byte-identical to the frozen ones except for the
scrub of identifying strings.
