# NUMBERS_R87 — the number record for values R87 printed from an artifact no ledger carried

R87 is a readability program and produces no measurements. This file exists for one class of
value: a figure that sits in a **committed results artifact** and that the paper now prints,
but that no registered ledger carried. Each row states the artifact, the key, the commit that
wrote it, and the value, so a reader can open the file rather than trust the transcription.

Registered in `iclr2027_monitoring_submission/tools/trace_scan_v13.py`'s `LEDGERS` list, on
the precedent of `reviews/NUMBERS_R86.md`. Deviation D-R87-1 in `reviews/DEVIATIONS_R87.md`.

---

## `AUX-R87-CF-COUNTED-MINI` — CF-3's population, GPT-4.1 mini, individuating pairs only

**What the paper prints (R86-5 item 2).** Table 2 gains the row "Counted states,
individuating pairs ($n=45$)" for all three models. The program text says the row is
"transcribed from NUMBERS_R82 with no recomputation". That is true of two of the three models:
`r82_counterfactual/NUMBERS_R82.md` section 7 (`AUX-R82-CF-COUNTED`) carries Haiku 4.5
(0.5656 to 0.8489) and section 9 (`AUX-R82-CF-OP5`) carries Opus 5 (0.6122 to 0.9144). The
GPT-4.1 mini pair is in **no ledger**. It is in the committed results file the R82 ledger was
itself transcribed from, and in `reviews/R86_PHASE0.md` (a report, not a ledger).

**Source, verbatim from the artifact.** `r82_counterfactual/results/cf_scores.json`, key
`lanes["gpt-4.1-mini"].cf3_counted`, last written at commit `7e9ac39` (R82-CF-1d):

| Field | Value |
|---|---|
| `v2` (summary names superseded content only; Table 2 column "names sup.") | **0.5578** |
| `v3` (summary names all three states; Table 2 column "names all") | **0.6600** (`0.66` in the JSON) |
| `delta_v3_minus_v2` | +0.1022 |
| `item_ci` | [−0.0637, +0.2669], `excludes_zero: false` |
| `question_clustered_ci` | [−0.0689, +0.2778], `excludes_zero: false` |
| `pairs` / `n_items` / `pos` | 15 / 45 / 15 |

The same key for the other two lanes, read in the same pass so the row is transcribed from one
source: `claude-haiku-4-5-20251001` v2 0.5656, v3 0.8489, delta +0.2833, both intervals
exclude zero; `claude-opus-5` v2 0.6122, v3 0.9144, delta +0.3022, both intervals exclude
zero. These agree with NUMBERS_R82 sections 7 and 9 to the last digit.

**Adverse detail, recorded so it is not lost.** GPT-4.1 mini's counted-state paired delta
(+0.1022) includes zero on both interval conventions. The row is descriptive and carries no
registered prediction (CF-3 was registered on Haiku 4.5 only; `ADDENDUM_R82.md`), and Table 2
prints no interval for any per-state or counted-state row, so the paper prints the two AUROC
values and this file carries the interval. Table 10 (Appendix D.2) does not carry the row for
any model; only Table 2 does.

**Method.** No computation. `json.load` the file, read the six fields above. The comparison
with NUMBERS_R82 is by eye against sections 7 and 9.

---

## Tokens this file accounts for

`0.5578` · `0.6600` · `+0.1022` · `45` (already in `NUMBERS_R82.md`) · `15` (already in
`NUMBERS_R82.md`) · `0.5656` · `0.8489` · `0.6122` · `0.9144` (the last four already in
`NUMBERS_R82.md`, restated here because the row is transcribed from one source).
