# ADDENDUM_Q4 — descriptive probe on the structureless inversion: the inexpressibility marker read as absence

Written 2026-09-13 (program R103, the v10-to-v11 pass), BEFORE any call. Descriptive: this
addendum carries **no prediction, no bar and no verdict**; every number it produces prints
whichever way it comes out, in Appendix F.7 beside the summary-ablation table (`tab:x2-ablation`)
and in one sentence of Section 7 after the unresolved-mechanism paragraph. It is frozen by its
sha256, recorded in `iclr2027_monitoring_submission/CLAIMS.md` (R103 block) and in
`q4_inversion_probe/NUMBERS_Q4.md` before the first call. Nothing here re-adjudicates U1, U2, U3,
U4 or U5, the R74 X2 branch, or any registered item.

## §1 — Question

Fifth review, Q4: the two structureless summaries (Mem0, A-MEM) carry three lines whose body is
exactly the marker `not expressible by this backend`; the frozen indexed prompt tells the monitor
that such a field is one the system does not track, "which is different from tracking it and
finding none". Does an instruction to read the marker as plain absence change GPT-4.1 mini's
coverage judgment on these stores, and does the inversion recorded in `tab:inversion` persist under
it? R74 X2 removed the marker lines (X2c) and the count with them (X2d); this probe leaves the
summary byte-identical and appends one instruction line instead.

## §2 — Population

The recorded external-store coverage items of the main study, exactly the rows of `tab:inversion`
and `AUX-R74-X2-*-INTACT`: **Mem0 n = 238 (94 positive), A-MEM n = 284 (126 positive)**, the
scoreable items (PRESENT, ABSENT, PRESENT-NEGATIVE) of `e1_metamemory/build/items_final.json`
with `backend in {mem0, amem}`, 40 personas, 77 index keys. Positives for FOK are non-ABSENT
items, as in the main study. The blind and intact rows are the **recorded** rows of
`e1_metamemory/elicitation_main.json` (arms BLIND and INDEXED-TRUE), read and never re-run; the
runner asserts n = 238 / 284 and reproduces the intact AUROC 0.4777 / 0.4526 and the intact deltas
−0.0969 / −0.1065 before any call.

## §3 — Condition (one arm)

**Q4-MARKER-ABSENT.** The item's committed TRUE summary text (`e1_metamemory/indexes_v2.json`,
key `<backend>:<persona>:<variant>:TRUE`, the same key the intact row used) with **one line
appended** after a blank line, as the last line of the summary inside the code fence:

    Treat any field marked 'not expressible by this backend' as absent; the backend does not record it.

Nothing else changes: the system prompt and the indexed user template are `prompts_e1.SYSTEM` and
`prompts_e1.USER_INDEXED` verbatim (digests `337d37d3…` / `35d9b968…` asserted at import), the
question is the recorded question, the summary body is byte-identical to the intact text. The
runner asserts, per key, that the rendered summary equals the committed text plus exactly the
blank line and the instruction line.

**Model and protocol.** `gpt-4.1-mini` pinned (`prompts_e1.MODEL`), temperature 0, seed 42,
max_tokens 200, JSON mode, k = 1, one retry on a parse failure (the E1 clamp), through
`e1_metamemory/tools/api.py` with the cache redirected to `q4_inversion_probe/cache/` (a fresh
namespace; arm name `Q4-MARKER-ABSENT`). Served identifier probed before launch (E1.7 rule); a
mismatch means do not launch.

## §4 — Estimand and estimators (descriptive)

Per store, on the paired items:
- **D1 = AUROC(Q4) − AUROC(intact)**, the paired difference against the recorded intact rows,
  item-level paired bootstrap (1,000 draws, seed 42, single-class draws discarded; `common_e1r.boot_item`)
  and persona-clustered paired bootstrap (`common_e1r.boot_cluster`, group = persona), both at 95%.
- **D2 = AUROC(Q4) − AUROC(blind)**, the inversion under the condition, with the same two intervals.
- The condition's AUROC, mean FOK, and the number of distinct FOK values; the intact and blind
  reproductions beside them.
Estimators are the committed ones (`e1r_robustness/tools/common_e1r.py`: Mann-Whitney AUROC with
ties at 0.5). Both intervals print; where they disagree the weaker reading is stated. No tolerance
is applied and no recovery rule is evaluated, because nothing is predicted.

## §5 — Budget and STOP

Cost line: this probe and DS Amendment 1 together are capped at **$3.00** by the author. Before
launch the runner projects 522 calls from the probe's token counts at list price ($0.40 / $1.60
per 1M) and prints the projection beside the cap; the launch is refused if the projection of the
two runs together exceeds the cap. The E1 client's hard cap is set to $3.00 on this namespace.
STOP conditions: served-identifier mismatch; any elicitation failure after the retry on more than
2% of items; projection over the cap.

## §6 — Paper site and ledger

`q4_inversion_probe/NUMBERS_Q4.md` carries `AUX-Q4-PROBE` (served identifier, tokens),
`AUX-Q4-PROJECTION`, `AUX-Q4-LOCK` (the per-key byte check), `AUX-Q4-M0` and `AUX-Q4-AM` (the
condition's AUROC, D1 and D2 with both intervals), `AUX-Q4-SPEND`. Paper: Appendix F.7, a
two-row table beside `tab:x2-ablation` labelled descriptive, and one sentence in Section 7 after
the unresolved-mechanism paragraph, two-decimal forms in the body. No frozen number changes; no
frozen text changes.

## Registration mechanics

Frozen by sha256 before the first call (recorded in CLAIMS.md R103 and NUMBERS_Q4.md). Copied to
`iclr2027_monitoring_submission/ARTIFACT/registrations/ADDENDUM_Q4.md`. Amendments, if any, are
appended as dated sections and never edit the text above.
