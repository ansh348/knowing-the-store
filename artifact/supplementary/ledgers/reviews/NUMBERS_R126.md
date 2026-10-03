# NUMBERS_R126.md: the pass ledger of program R126 (the readable body, v22; 2026-09-20)

Written by `reviews/v22/tools/ledger_r126.py` from the artifacts named in each section; no number is typed by hand. The readable body's own numbers are the v21 body's (every printed form resolves to an earlier ledger; `reviews/v22/INBOX_NUMBERS_R126.md` lists the 130 values with the inbox's provenance tags); this file carries what the pass adds.

## AUX-R126-E3-INTENT — the 661 by intent, label and the state of the question's own attribute (tab:e3-intent; `reviews/v22/results/e3_intent_table.json`, `reviews/v22/tools/e3_intent_table.py`)

Method: PN: the manifest's obligation state (item.state). PRESENT: the marks the ground-truth join puts on any entry of the question's own slot(s) in its store version (resp_common.true_flags restricted to variant_ids); the first of retracted, superseded, expired when several, else 'active only'. ABSENT: no gold entry in the store version (asserted).

| intent | label | superseded | retracted | expired | active only | unaligned | none | total |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| CURRENT-STATE | PRESENT-NEGATIVE | 63 | 26 | 0 | 0 | 0 | 0 | 89 |
| CURRENT-STATE | PRESENT | 1 | 1 | 15 | 68 | 0 | 0 | 85 |
| CURRENT-STATE | ABSENT | 0 | 0 | 0 | 0 | 0 | 274 | 274 |
| UPCOMING | PRESENT-NEGATIVE | 0 | 0 | 15 | 0 | 0 | 0 | 15 |
| UPCOMING | PRESENT | 5 | 3 | 8 | 18 | 0 | 0 | 34 |
| UPCOMING | ABSENT | 0 | 0 | 0 | 0 | 0 | 49 | 49 |
| PAST-EVENT | PRESENT | 0 | 0 | 0 | 0 | 10 | 0 | 10 |
| CHANGE-AWARE | PRESENT | 3 | 3 | 5 | 34 | 0 | 0 | 45 |
| CHANGE-AWARE | ABSENT | 0 | 0 | 0 | 0 | 0 | 60 | 60 |

PN by intent: {'CURRENT-STATE': 89, 'UPCOMING': 15, 'PAST-EVENT': 0, 'CHANGE-AWARE': 0} (every PN question has current or upcoming intent). PRESENT questions whose own attribute also holds a non-active record, by intent: {'CURRENT-STATE': 17, 'UPCOMING': 16, 'PAST-EVENT': 0, 'CHANGE-AWARE': 11}; total 44 of 174 PRESENT questions (33 under current or upcoming intent, 11 under change intent). Non-exclusive marks on PRESENT questions: {'CHANGE-AWARE|expired': 8, 'CHANGE-AWARE|retracted': 3, 'CHANGE-AWARE|superseded': 4, 'CURRENT-STATE|expired': 17, 'CURRENT-STATE|retracted': 1, 'CURRENT-STATE|superseded': 2, 'UPCOMING|expired': 13, 'UPCOMING|retracted': 3, 'UPCOMING|superseded': 6} (CHANGE-AWARE|superseded = 4, the 4 of the 45 that reviews/NUMBERS_WP.md section 9 B4b counts).

## AUX-R126-GATEREACH — the recorded policies' rows added to tab:gatereach's licensed panel (`reviews/v21/results/reach_rows_r123.json`, AUX-R123-REACH-ROWS; printed at two decimals)

| policy | licensed in view (of 174) | rate | mean lines, 661 (printed) | mean lines, 104 (printed) |
|---|---:|---:|---:|---:|
| top-five retrieval (ALWAYS) | 65 | 0.3736 | 5.0000 -> 5.00 | 5.0000 -> 5.00 |
| lookup rule (LOOKUP) | 65 | 0.3736 | 5.4569 -> 5.46 | 6.8750 -> 6.88 |
| oracle (ORACLE) | 65 | 0.3736 | 5.3253 -> 5.33 | 7.0673 -> 7.07 |

## AUX-R126-DAYS — the day index of the registration order (Phase 4.4, anonymity): the calendar date each index replaces in the PDF; day 0 is the first freeze (the E0 preregistration)

| date | day |
|---|---:|
| 2026-08-10 | 0 |
| 2026-08-11 | 1 |
| 2026-08-14 | 4 |
| 2026-08-24 | 14 |
| 2026-08-29 | 19 |
| 2026-08-30 | 20 |
| 2026-09-12 | 33 |
| 2026-09-13 | 34 |
| 2026-09-14 | 35 |
| 2026-09-15 | 36 |
| 2026-09-17 | 38 |
| 2026-09-18 | 39 |
| 2026-09-19 | 40 |

The artifact files that still carry these dates (for the 24 September sweep) are listed in `reviews/v22/REPORT_R126.md`, Phase 4.4; git history is not rewritten.

## AUX-R126-FIG3 — Figure 3's plotted values (`reviews/v22/src/fig3_data.tex`; the sources per reader in the file's header)

```
\pgfplotstableread[col sep=comma]{
x,state,mini,haiku,luna,sol,opus,lookup,count
0,Supersession,0.8793,0.8876,0.9426,0.9383,0.9325,0.9223,0.6573
1,Retraction,0.5761,0.5433,0.5458,0.5322,0.5872,0.5000,0.6669
2,Expiry,0.5594,0.5794,0.6167,0.6403,0.6150,0.5000,0.6872
}\figthreeSup
\pgfplotstableread[col sep=comma]{
x,state,mini,haiku,opus,lookup
0,Supersession,0.8829,0.8852,0.9319,0.8995
1,Retraction,0.8433,0.9042,0.8100,0.7975
2,Expiry,0.6719,0.8269,0.9267,0.8711
}\figthreeAll

```
