"""
consolidate_deviations.py -- E1.8 STEP 3(b): DEVIATIONS.md as one table.

The file grew by append across E1, E1.5, E1.6 and E1.7, and each append carried
a trailing chunk of the previous one with it, so D16/D17/D18-E1 each appear FOUR
times. The duplicates are byte-identical -- verified here, not assumed: if any
two copies of a deviation ever differ, this script refuses to run rather than
silently picking one.

Output: a summary table of every deviation with a one-line disposition, followed
by the full entries, deduplicated, in numeric order. Entry text is carried
through UNCHANGED. The pre-consolidation file is preserved in git history.

Usage:  python e1_metamemory/tools/consolidate_deviations.py
"""

from __future__ import annotations

import collections
import io
import re
from pathlib import Path

E1 = Path(__file__).resolve().parents[1]
SRC = E1 / "DEVIATIONS.md"

# `-E1` was hard-coded here, so a `-E2` heading parsed as nothing and its block was
# dropped on rewrite. That silently deleted D31-E2..D34-E2 once (D35-E2). The suffix
# is now any phase, and `main` asserts that every `### D` heading in the input was
# parsed -- a block this regex does not recognise is now a hard failure, never a
# silent deletion.
HEAD_RE = re.compile(r"### (D\d+)(?:-E\d+)?\s*(?:--|—)\s*(.*)")
COUNT_RE = re.compile(r"^### D", re.M)

# One-line disposition per deviation, reflecting its FINAL state. The entry text
# below the table is never edited; this column is the index into it.
DISPOSITION = {
    "D1": ("design doc absent when Phase A began",
           "**Resolved** — v0.2 supplied verbatim in the instruction, committed unaltered, "
           "sha256 `c9ca79e8…` recorded in the prereg."),
    "D2": ("E0's frozen prompt module not reused",
           "**Resolved** — E0's system text asserts structure Mem0 and A-MEM lack; new frozen "
           "`prompts_e1.py`. E1 is therefore **not** prompt-level comparable to E0."),
    "D3": ("NOK worked examples drawn from out-of-scope material",
           "**Resolved** — both from AV8, out of scope by rule, paraphrased, no persona named."),
    "D4": ("SLOT-ABLATED stored as removal sets, not materialised banks",
           "**Resolved** — equivalent by construction; removal ids asserted against the bank."),
    "D5": ("**STOP** — the lexical presence sweep is only 70% recall",
           "**Escalated, then resolved by D6** — `ABSENT-by-ingestion-loss` asserted a cause the "
           "instrument could not establish; 207 labels renamed `sweep-negative` pending the "
           "decision, then re-routed by the two-channel instrument."),
    "D6": ("two-channel control gives epsilon = 0.5%",
           "**Resolved** — lexical .697 / embedding .965 / combined .995; external ABSENT "
           "collapses to Mem0 8 and A-MEM 13, 186 items to UNRESOLVED. Makes the probe corpus "
           "load-bearing for H-BELIEVED on the external backends."),
    "D7": ("natural-absent probe survival is 52%, not 83%",
           "**Resolved, imbalance reported not corrected** — 145/279 survived; 19 personas below "
           "target and one produced none. No re-draft: re-drafting only the shortfall personas "
           "would sample conditional on the screen having rejected their predecessors."),
    "D8": ("verification burden 393 reads, not the 341 budgeted",
           "**Logged** — all 393 performed."),
    "D9": ("6 membership exclusions outside the three named patterns",
           "**Resolved** — tagged and reported as subtype counts, never folded into the frozen "
           "criterion."),
    "D10": ("**STOP** — the conditional-GO checklist was not fully evaluable",
            "**Escalated, then cleared** — re-evaluated after the two outstanding passes; all "
            "four items PASS (`2085330`); proceeded under the standing conditional go."),
    "D11": ("index v2 line counts 31–71 against a ~40–60 target",
            "**Logged** — wrap width is cosmetic; the pre-registered slot cap was not tuned."),
    "D12": ("category/slot inexpressible on external backends under TRUE too",
            "**Logged, reversible** — settled reading R1: provenance sets the lifecycle source "
            "only; region structure follows the store under both provenances."),
    "D13": ("`recency_time` build-instrument correction",
            "**Resolved** — recency taken from each store's own content date, not the ingest "
            "wall-clock, which is one afternoon in 2026-05 for the entire external corpus."),
    "D14": ("E1 gained its own `api.py`; a thread-safety bug found in E0's",
            "**Logged** — `_load_cache()` ran outside the lock (180 calls, 179 records). Closed "
            "in E1's adapter; E0 left alone, its runs already spent and published."),
    "D15": ("probe sweep instrument tightened twice before use",
            "**Resolved** — corpus-measured document-frequency filter, then the house "
            "≥2-distinct-token rule: 127 → 114 → 3 probes needing a human read."),
    "D16": ("elicitation run on scoreable items only",
            "**Logged** — UNRESOLVED items are excluded from every metric by pre-elicitation "
            "rule, so eliciting them would have bought nothing and roughly doubled cost."),
    "D17": ("a test run collided with the in-flight full elicitation",
            "**Logged, no correctness impact** — the full run rewrote every output on "
            "completion; 2,698/2,698 parsed."),
    "D18": ("the strong-model lane needed a Windows path fix",
            "**Resolved** — `shutil.which` for the npm `.CMD` shim; 150/150 after."),
    "D19": ("`run_a.py` imported `strong_model.py`, which has no `__main__` guard",
            "**Resolved, and became a finding** — deduplicated keeping post-fix rows; the "
            "accidental duplicate pairs measured codex nondeterminism directly (98/129 "
            "disagreed), which is why every frontier figure is a k=5 mean."),
    "D20": ("Run B killed twice by parent-shell timeouts",
            "**Logged** — resumed from cache; no prompt or item changed."),
    "D21": ("the k=5 redraw supersedes every single-draw frontier figure",
            "**Resolved** — supersession chain resolved in `NUMBERS.md`; the single-draw run "
            "stays committed as the nondeterminism measurement."),
    "D22": ("Luna emits far more tokens per turn than Sol",
            "**Logged, corrected by D24** — 11,712 against 3,157 on a trivial probe, n=1 each."),
    "D23": ("mini's blind NOK is constant, so its 0.5000 is degenerate",
            "**Logged** — 0.0 on all 84 matched items, so every pair ties and the AUROC is 0.5 "
            "by arithmetic. Annotated wherever that cell appears."),
    "D24": ("D22-E1 was wrong on both of its numbers",
            "**Corrected in place** — measured luna 43.2 min vs sol 44.7 min (luna marginally "
            "*faster*, not ~80 min slower), and codex's \"tokens used\" is a turn total, not a "
            "reasoning-token count. No result depends on either."),
    "D25": ("E1's Phase-C usage records were written into E0's cache",
            "**Logged, not repaired** — `elicit_e1.py` puts E0's tools dir first on `sys.path`, "
            "so `import api` resolves to E0's. Split is exact and mechanical; repairing it would "
            "rewrite a frozen E0 artifact to fix a filing error that changed no result."),
    "D26": ("the E1.8 mechanism probe runs on the pooled hard tier",
            "**Resolved before any call** — \"272\" is the FR-Bank ABSENT count, the evaluable "
            "FR-Bank slice is 307, and the quoted 0.7530/0.5258 reference is the pooled n=588 "
            "row. Ran the superset so the reference applies exactly and nothing was narrowed."),
    "D27": ("a DNS drop killed the first A1–A3 run at 1,111 of 1,764 calls",
            "**Resolved** — resumed from cache at $0 for the completed calls; the $5 step cap "
            "check was made cumulative rather than per-process. The cap was never at risk."),
    "D28": ("two arms were mis-filed in the economics table",
            "**Corrected** — `draft` (40 records = one per E1 persona; E0 ran 20 and had no "
            "drafting step) and the E1.8 A1/A2/A3 arms were filed under E0. No headline figure "
            "moved. Adds a result: **A3 names-only is the cheapest index arm, $501/1M against "
            "the intact index's $519.**"),
    "D31": ("the answerer model was unspecified by the prereg",
            "**Resolved** — pinned at `gpt-4.1-mini`, temp 0, seed 42, metered, before any answer "
            "existed; the instrument that must match FR is the JUDGE and it does exactly. Carry: "
            "absolute confab rates are not comparable to FR's 12.0%/24.2%; the (vi)-vs-(v) contrast "
            "is. Also added `e2_api.call_text`, since E0's client forces JSON mode."),
    "D32": ("**STOP** — the retriever is not fit for purpose; calibration degenerate",
            "**STOPPED at SP2.** Every threshold collapsed to never-retrieve. Cause is retrieval, "
            "not gating: a retrieved fact covers ≥50% of the gold on **1/57** PRESENT/PN items "
            "against FR's own **23.8%**. The gate signal is intact (FOK medians 0.700/0.400/0.200). "
            "Options and costs in `e2_metamemory/SP2_STOP.md`."),
    "D33": ("the paired-difference SD was under-assumed; power collapses",
            "**Reported, bands untouched** — measured 0.3395 against an assumed 0.200, so power at "
            "the frozen bands falls to 38.6% (H-C1a) and 27.3% (H-C1b). The SP1 freeze rule forbids "
            "re-tuning; recorded so any re-freeze starts from a measured SD."),
    "D34": ("P5's registered spot-check subset is not computable as written",
            "**Flagged before any call** — P5 needs credit and confabulation, but 66 of the 150 "
            "registered items are external and get no E2 answers by construction. Resolution "
            "offered, not taken; folds into the D32 decision."),
    "D35": ("`consolidate_deviations.py` silently deleted four deviations",
            "**Fixed.** Its heading regex hard-coded `-E1`, so `-E2` blocks parsed as nothing and "
            "were dropped on rewrite — D31-E2..D34-E2 were lost and restored from the session "
            "record. Regex now accepts any phase, and the tool **asserts that every `### D` heading "
            "present was parsed**, so an unrecognised block is a hard failure rather than a silent "
            "deletion. The tool built to protect the record damaged it once."),
    "D36": ("**BRANCH B** — FR's retrieval runs, but its published run is not reproducible",
            "**STOPPED.** r1 pass (FULL only), r2 marginal (9/10 repeats), **r3 fail**: vs the fed "
            "context, gold coverage 35.6% fresh against 30.5% cached (5.1pp, outside the band) with "
            "item-level agreement of Jaccard 0.319 / top-1 37.3%; vs `fr_bank_results` Jaccard 0.035. "
            "Fresh retrieval BEATS the cache on coverage — what fails is comparability. Cache not "
            "adopted; surviving terrain would be 178 items with ZERO ABSENT, on which H-C1a is "
            "near-vacuous. See `e2_metamemory/SUBSTRATE_FINDINGS.md`."),
    "D37": ("**STOP** at SP2 round 2 — gates collapse for a substantive reason",
            "**STOPPED.** Substrate validated (0/338 leaks, coverage 35.4%), yet fitted rates are "
            "0.000/0.000/0.008. Retrieval gains +0.319 on PRESENT and loses −0.383 on ABSENT at 57% "
            "ABSENT, so always (0.4444) < never (0.5606) and the sweep is monotone. Oracle headroom "
            "+0.101; the FOK gate captures +0.0076 (7.5%). Damage is the hard tier: ablation-ABSENT "
            "1.000→0.510 with 45% confabulation vs probes 0.958→0.806 at 3%. Hierarchy rule fired "
            "(100% ≥ 60%) on a degenerate contrast and is flagged uninformative. See "
            "`e2_metamemory/SP2_STOP_2.md`."),
    "D38": ("**STOP** at SP2 round 3 — the calibration split cannot resolve the credit surface",
            "**STOPPED at the decision point.** gpt-5.4 pinned by the frozen bake-off rule; item 1 "
            "fails a third time (rates 0.000/0.000/0.008). The gate clears break-even precision "
            "(0.582–0.635 vs a required 0.566, base rate 0.432) but the credit surface is only "
            "~0.040 wide against a 132-item split where one item is worth 0.0076 — the argmax beats "
            "never-retrieve by exactly one item. At τ=0.50 the gate DOMINATES always-retrieve on "
            "both axes (0.5694 vs 0.4369 credit, 0.154 vs 0.386 confabulation). The hypotheses are "
            "alive; the selection rule is degenerate. See `e2_metamemory/SP2_STOP_3.md`."),
    "D39": ("variable shadowing in `run_answers.py` — invisible on calibration, fatal on eval",
            "**Resolved.** `frozen` named both the retrieval artifact and the thresholds dict; the "
            "collision only fires when `s2_all` is False, i.e. never on calibration. Failed loudly "
            "with a KeyError before any API call, so no eval answer was written. Also logs a cost "
            "projection error: eval gates $0.964 against a $0.38 projection."),
    "D40": ("the eval judge task was stopped by the harness mid-run",
            "**Resolved.** Stopped externally at ~150/1,179; `run_judge.py` checkpoints every 50 "
            "verdicts and skips cached keys, so the resume lost nothing and re-judged nothing."),
    "D41": ("five eval judgments failed on first pass, all on one question",
            "**Resolved.** 1,174/1,179 OK; the five failures were all `callum_q04` across two "
            "variants. The runner skips cached keys including failed ones, so the five were evicted "
            "by key and re-judged: **1,179/1,179 OK**, with `cached=1174, to judge=5` confirming no "
            "other verdict was touched."),
    "D42": ("eleven P5 frontier draws failed to parse; retried to full completeness",
            "**Resolved.** 829/840 OK on first pass (1.3%); no cell fell below E1.7's MIN_DRAWS "
            "floor of 3, checked before acting, so the retry was for completeness not necessity. "
            "Failed rows evicted by status from the resumable partial, resumed 829 done / 11 to go "
            "-> **840/840 OK**. Lane reproducibility 8/168 cells identical across 5 draws vs E1.7's "
            "sol 3/300 — same order, and why k=5 is by construction."),
    "D43": ("**ledger-class** — a cached failure is indistinguishable from a cached success",
            "**Logged as an instrument note.** The judge cache skips any present key including a "
            "`JUDGE_FAILED` one, so a failure becomes a permanent hole that no re-run fills. Same "
            "class as Incident 8 and D35. Standing lesson: **a cache that stores failures makes "
            "retry a no-op** — memoisation over a fallible call must refuse to store failures, or "
            "expose them as a state resumption re-attempts. E2's data is complete."),
    "D44": ("the answer component of the cost table is priced at the wrong model's rates",
            "**Logged, not corrected.** `usd()` prices at gpt-4.1-mini rates; the answerer is "
            "gpt-5.4, whose list price was never verified. Understates answer cost for every policy "
            "equally and therefore **overstates the gate's relative cost disadvantage**. Tokens are "
            "exact, dollars are not; `RESULTS_E2.md` §3.11 carries the caveat inline."),
    "D29": ("E1's Phase-C usage records were never committed",
            "**Resolved** — the 3,037 records D25-E1 located in E0's cache sat uncommitted "
            "through the `e1-complete` tag, and every measured figure in `ECONOMICS.md` reads "
            "from them. Committed unmodified; no record moved or rewritten. Found while checking "
            "the tree was clean before starting E2."),
}

PREAMBLE = """# DEVIATIONS — E1 full calibration study

Every departure from `E1_DESIGN.md` v0.2 and `PREREG_E1.md`, in the order encountered.
Entries marked **STOP** were escalated rather than resolved unilaterally.

**Consolidated at E1.8.** This file was appended to by each of E1, E1.5, E1.6 and E1.7, and every
append carried a trailing chunk of the previous one, so D16, D17 and D18-E1 each appeared four
times. All duplicate copies were verified byte-identical before removal. **No entry text has been
edited** — the entries below are as written, deduplicated and put in numeric order, with a summary
table added. The pre-consolidation file is in git history.

---

## Summary — every deviation, one line each

| # | what | disposition |
|---|---|---|
"""


def main():
    src = io.open(SRC, encoding="utf-8").read()
    blocks = re.split(r"\n(?=### )", src)
    entries, dupes = collections.OrderedDict(), collections.Counter()
    for b in blocks:
        m = HEAD_RE.match(b)
        if not m:
            continue
        key = m.group(1)
        body = b.strip()
        if key in entries and entries[key] != body:
            raise SystemExit(f"REFUSING TO CONSOLIDATE: two copies of {key} differ. "
                             "Resolve by hand; this script will not choose.")
        dupes[key] += 1
        entries[key] = body

    # A block this regex cannot parse must never be dropped on rewrite. Compare
    # what was parsed against every `### D` heading actually present.
    n_headings = len(COUNT_RE.findall(src))
    if n_headings != sum(dupes.values()):
        raise SystemExit(
            f"REFUSING TO CONSOLIDATE: {n_headings} '### D' headings in the file but "
            f"{sum(dupes.values())} parsed. An unrecognised heading would be deleted "
            f"on rewrite. Fix HEAD_RE before running again.")

    missing = set(entries) - set(DISPOSITION)
    extra = set(DISPOSITION) - set(entries)
    assert not missing, f"no disposition written for {sorted(missing)}"
    assert not extra, f"disposition for a deviation that does not exist: {sorted(extra)}"

    order = sorted(entries, key=lambda k: int(k[1:]))
    out = [PREAMBLE]
    for k in order:
        what, disp = DISPOSITION[k]
        out.append(f"| **{k}** | {what} | {disp} |\n")
    out.append("\n---\n\n## Full entries\n\n")
    out.append("\n\n---\n\n".join(entries[k] for k in order))
    out.append("\n")

    with io.open(SRC, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(out))

    n_dup = sum(v - 1 for v in dupes.values())
    print(f"consolidated {len(order)} deviations; removed {n_dup} duplicate copies "
          f"({', '.join(f'{k}x{v}' for k, v in dupes.items() if v > 1)})")
    print(f"  all duplicate copies verified byte-identical")
    print(f"wrote {SRC}")


if __name__ == "__main__":
    main()
