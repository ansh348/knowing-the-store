# -*- coding: utf-8 -*-
"""finalize_opus.py -- program R114: once rows/rows_OP5.jsonl is collected, score the Opus lane (v2rcat_op5.py score), apply the Opus
manuscript edits (m1_apply_manuscript.py's opus_edits alone), the number dispositions (m2_gate_hunks.py, the Opus hunk) and the C.2 / E.11
pins (pin_appendix_r114.py), regenerate NUMBER_MOVES_V19.md, and fill the OPUS_* placeholders of REPORT_R114.md, claims_block_r114.md and
NUMBERS_R114.md from results/scores_v2rcat_op5.json. Run from the repository root; then run_gates.py r114.
"""
from __future__ import annotations

import io
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
PY = sys.executable
R114 = ROOT / "reviews" / "r114"
OP5 = ROOT / "r82_counterfactual" / "v2rcat" / "results" / "scores_v2rcat_op5.json"
ROWS = ROOT / "r82_counterfactual" / "v2rcat" / "rows" / "rows_OP5.jsonl"
assert ROWS.exists(), "no Opus rows yet"


def run(cmd, cwd=ROOT):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(" ".join(str(c) for c in cmd[1:]), "->", (r.stdout + r.stderr).strip().split("\n")[-1][:200])
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)


if not OP5.exists():
    run([PY, "r82_counterfactual/v2rcat/tools/v2rcat_op5.py", "score"])
S = json.load(open(OP5, encoding="utf-8")); M = S["opus"]; R, Ex, W = M["per_state"]["RETRACTION"], M["per_state"]["EXPIRY"], M["minus_v2"]
rows = [json.loads(l) for l in io.open(ROWS, encoding="utf-8")]
tin = sum(r.get("tok_in", 0) or 0 for r in rows); tout = sum(r.get("tok_out", 0) or 0 for r in rows)
# manuscript: the Opus edits alone (the composite edits are already applied; the script aborts on a missing Before, so run a stripped copy)
import importlib.util as ilu
spec = ilu.spec_from_file_location("m1", R114 / "tools" / "m1_apply_manuscript.py"); m1 = ilu.module_from_spec(spec); spec.loader.exec_module(m1)
m1.E.clear(); m1.opus_edits()
usd_all = M["usd"] + S["spend"]["probe"]
m1.rep(m1.X, "the forty-persona Graphiti ingestion $11.88$ of a $13.22$ stop, twelve aborted partial runs included (Appendix~\\ref{app:posthoc-graphiti}).",
       f"the forty-persona Graphiti ingestion $11.88$ of a $13.22$ stop, twelve aborted partial runs included (Appendix~\\ref{{app:posthoc-graphiti}}); two runs after this draft, the composite's answers on the actual expanded views $0.14$ and Opus 5 on the moved-count control ${usd_all:.2f}$, under a $40$ ceiling for that pass.")
files = {p: p.read_text(encoding="utf-8") for p in (m1.B, m1.X)}
for f, old, new in m1.E:
    n = files[f].count(old)
    if n == 0 and files[f].count(new) == 1:
        continue                                   # already applied by an earlier run
    assert n == 1, (f.name, n, old[:100])
    files[f] = files[f].replace(old, new)
for p, t in files.items():
    p.write_text(t, encoding="utf-8", newline="\n")
print(f"opus manuscript edits applied: {len(m1.E)}")
run([PY, "reviews/r114/tools/m2_gate_hunks.py"])
run([PY, "reviews/v19/tools/number_moves_wp.py"])
run([PY, "reviews/v19/tools/build_v19.py"])
run([PY, "reviews/r114/tools/pin_appendix_r114.py"])
# placeholders
def iv(d):
    return f"[{d['item_ci']['ci_lo']:+.4f}, {d['item_ci']['ci_hi']:+.4f}]; [{d['persona_ci']['ci_lo']:+.4f}, {d['persona_ci']['ci_hi']:+.4f}]"
n_bad = M["n_rows_bad"]; usd = M["usd"]; probe = S["spend"]["probe"]
status = "**completed**" if n_bad == 0 else f"**completed with {n_bad} failed requests**"
ran = f"444 Batch requests at k = 1, {n_bad} not OK; scored against the recorded k = 5 row (AUX-CF2-OP5-V2 0.8405)"
results = (f"`claude-opus-5` (served {S['served']}), k = 1, Batch, temperature unset, max_tokens 1024; 444 requests, {n_bad} not OK; ${usd:.4f} (probe ${probe:.4f}). "
           f"Comparator: the recorded CF-2 Opus v2 row at k = 5 (0.8405), disclosed as section 4 requires; the totals-randomized row (v2r, k = 5) prints beside as a distinct construction.\n\n"
           f"| row | recorded v2 (k = 5) | recorded v2r (k = 5) | V2R-CAT (k = 1) | minus v2 (item; persona) | band reading |\n|---|---:|---:|---:|---|---|\n"
           f"| whole set (444, 148 positives) | {M['v2_recorded']:.4f} | {M['v2r_recorded_totals_randomized']:.4f} | **{M['v2rcat']:.4f}** | {W['delta']:+.4f} ({iv(W)}) | — |\n"
           f"| supersession (88 pairs) | {M['per_state']['SUPERSESSION']['v2']:.4f} | {M['per_state']['SUPERSESSION']['v2r']:.4f} | {M['per_state']['SUPERSESSION']['v2rcat']:.4f} | {M['per_state']['SUPERSESSION']['delta']:+.4f} ({iv(M['per_state']['SUPERSESSION'])}) | texts unchanged |\n"
           f"| retraction (30 pairs) | {R['v2']:.4f} | {R['v2r']:.4f} | **{R['v2rcat']:.4f}** | {R['delta']:+.4f} ({iv(R)}) | {'inside the band, both intervals' if R['inside_band_both'] else ('beyond the band, both intervals' if R['beyond_band_both'] else 'neither')}; point within 0.05: {R['point_within_band']} |\n"
           f"| expiry (30 pairs) | {Ex['v2']:.4f} | {Ex['v2r']:.4f} | **{Ex['v2rcat']:.4f}** | {Ex['delta']:+.4f} ({iv(Ex)}) | {'inside the band, both intervals' if Ex['inside_band_both'] else ('beyond the band, both intervals' if Ex['beyond_band_both'] else 'neither')}; point within 0.05: {Ex['point_within_band']} |\n\n"
           f"Reference readers under the same text: the state-cell reader 0.3028 / 0.3611, CR-totals 0.4044 / 0.3894. Section 5 branch for this model: **{M['branch']['reading']}**. "
           f"The k = 1 draw against the recorded k = 5 row carries draw-count noise the two registered lanes did not (disclosed in the ledger, the table and the prose); "
           f"the totals-randomized construction (v2r) and the moved-count construction (V2R-CAT) stay distinct rows. Landed: three rows in `tab:v2rcat`, one prose sentence in Appendix C.2, the Section 5 sentence \"Opus 5 was not run on this control\" replaced by the two-decimal deltas; the branch wording for three models is the author's.")
subs = {"OPUS_STATUS": status, "OPUS_RAN": ran, "OPUS_CALLS": f"444 + 1 probe", "OPUS_TOKENS": f"{tin:,} / {tout:,}", "OPUS_USD": f"{usd:.4f} + {probe:.4f}",
        "OPUS_RESULTS": results, "OPUS_MANUSCRIPT": "the Opus 5 row in `tab:v2rcat` (three rows), its prose sentence in Appendix C.2 and the Section 5 sentence",
        "TOTAL_USD": f"{1.5725 - 0.0158 + usd + probe:.4f}"}
for p in (R114 / "REPORT_R114.md",):
    t = p.read_text(encoding="utf-8")
    for k, v in subs.items():
        t = t.replace(k, v)
    p.write_text(t, encoding="utf-8", newline="\n")
c = R114 / "claims_block_r114.md"; t = c.read_text(encoding="utf-8")
entry = (f"(1 to 0 in Section 5; 3 rows and 1 sentence in Appendix C.2). Before: \"Opus 5 was not run on this control.\" and tab:v2rcat without an Opus row. After: Section 5 reads \"Opus 5, run once per item after this draft against its five-draw row, moves ${R['delta']:+.2f}$ on retraction and ${Ex['delta']:+.2f}$ on expiry.\"; tab:v2rcat gains the whole-set, retraction and expiry rows (k = 1; recorded row k = 5) with both intervals; the C.2 prose gains one sentence with the draw-count disclosure. Basis: `r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md` section 8, AUX-V2RCAT-OP5 (444 Batch requests, {n_bad} not OK, ${usd:.4f}); D-V2RCAT-2.")
claim = (f"TEXT | Opus 5, run once per item on the moved-count control against its recorded five-draw superseded-only row (0.8405), reads {M['v2rcat']:.4f} on the whole set ({W['delta']:+.4f}); retraction {R['v2']:.4f} to {R['v2rcat']:.4f} ({R['delta']:+.4f}, {iv(R)}); expiry {Ex['v2']:.4f} to {Ex['v2rcat']:.4f} ({Ex['delta']:+.4f}, {iv(Ex)}); branch: {M['branch']['reading']}. KEYS | AUX-V2RCAT-OP5, AUX-CF2-OP5-V2. CLASS | robustness.")
t = t.replace("OPUS_ENTRY", entry).replace("OPUS_CLAIM", claim)
c.write_text(t, encoding="utf-8", newline="\n")
with io.open(ROOT / "reviews" / "NUMBERS_R114.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(f"\n## 4. AUX-R114-P4: Phase 4 done (`r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md` section 8, AUX-V2RCAT-OP5; D-V2RCAT-2). Opus 5 k = 1 Batch, 444 requests, {n_bad} not OK, ${usd:.4f} + probe ${probe:.4f}. Whole set {M['v2rcat']:.4f} against the recorded 0.8405 ({W['delta']:+.4f}); retraction {R['delta']:+.4f}, expiry {Ex['delta']:+.4f}; branch: {M['branch']['reading']}.\n\n## 6. AUX-R114-SPEND: the pass total, metered from the rows files: Phase 1 $0.1357, Phase 2 $1.1851, Phase 3 $0.2359, Phase 4 ${usd + probe:.4f}, Phase 5 $0; **${1.5725 - 0.0158 + usd + probe:.4f}** against the $40 ceiling (manifest expected $5.70, conservative $7.55). No retries were needed in any lane.\n")
print("placeholders filled; now: python reviews/v19/tools/run_gates.py r114 \"R114: the composite's actual views and the Opus 5 moved-count row\"")
