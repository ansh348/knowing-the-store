# NUMBERS_Q4.md — the marker-as-absence probe (ADDENDUM_Q4, descriptive; R103, 2026-09-13)

Registration `registrations/ADDENDUM_Q4.md`, frozen sha256 `8b6ee9e3f7e2181edcab06e35d9a9efc0a0c21421ab841664a8f6e22da7ca608` before the first call (copy in
`iclr2027_monitoring_submission/ARTIFACT/registrations/`). Descriptive: no prediction, no bar, no verdict; every value prints
whichever way it came out. Source `q4_inversion_probe/results/q4_scores.json`; rows `run/q4_elicitation.json`; lock `run/lock_q4.json`.

### AUX-Q4-LOCK

Population 238 Mem0 (94 positive) and 284 A-MEM (126 positive), 77 summary keys, 3 marker lines per key. Each rendered
summary equals the committed TRUE text plus one blank line and the instruction line, byte for byte; the recorded intact rows reproduce
(Mem0 0.4777, Δ -0.0969; A-MEM 0.4526, Δ -0.1065). prompts_e1 digests 337d37d3… / 35d9b968….

### AUX-Q4-PROBE and AUX-Q4-PROJECTION

Served `gpt-4.1-mini-2025-04-14` (identifier ok: True), 780 in / 26 out on the first item; projection 522 calls,
$0.1846 (x1.3 $0.2400) against the combined $3.00 cap.

### AUX-Q4-M0 and AUX-Q4-AM — the condition beside the recorded rows

| Key | Store | n | blind | intact (recorded) | Q4 marker-as-absence | D1 = Q4 − intact | item CI | persona CI | D2 = Q4 − blind | item CI | persona CI |
|---|---|---:|---:|---:|---:|---:|---|---|---:|---|---|
| AUX-Q4-M0 | Mem0 | 238 | 0.5746 | 0.4777 | **0.5353** | +0.0577 | [-0.0074, +0.1157] | [-0.0149, +0.1292] | -0.0393 | [-0.1042, +0.0226] | [-0.1026, +0.0294] |
| AUX-Q4-AM | A-MEM | 284 | 0.5591 | 0.4526 | **0.5355** | +0.0829 | [+0.0277, +0.1411] | [+0.0285, +0.1403] | -0.0236 | [-0.0871, +0.0388] | [-0.0739, +0.0327] |

Mean FOK under the condition 0.1277 (Mem0; intact 0.1660) and 0.1329 (A-MEM; intact 0.1607);
distinct FOK values 6 and 6; items whose score equals the intact score exactly 141 of 238 and 167 of 284.
Reading rule stated, not applied: where the two intervals disagree the weaker reading governs; nothing here is a verdict.

### AUX-Q4-SPEND

Billed from response usage at $0.40 / $1.60 per 1M: probe $0.0004, run $0.1828 — **total $0.1831**; 522 calls
(0 served from cache, 0 failures). Nothing on any other key; no embedding call.
