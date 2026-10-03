# -*- coding: utf-8 -*-
"""r130_report.py -- program R130: writes reviews/r130/REPORT_R130.md from the artifacts (scores, validation if present, probes, lock,
projection, batch record, the git log of the program's commits). Offline, $0. Re-runnable: the report is regenerated whole from the artifacts.

    python r130_report.py [--dry-run <dir>]
"""
from __future__ import annotations

import io
import pathlib
import subprocess
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r130_common as C  # noqa: E402


def commits():
    r = subprocess.run(["git", "log", "--format=%h %ad %s", "--date=short", "-n", "20", "--", "reviews/r130", "ds_downstream/run/rows_ds_r130_luna.jsonl", "ds_downstream/run/rows_ds_r130_judge.jsonl", "ds_downstream/NUMBERS_DS.md"],
                       cwd=C.ROOT, capture_output=True, text=True, encoding="utf-8")
    return [l for l in r.stdout.splitlines() if l.strip()]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    dry = "--dry-run" in sys.argv; d = pathlib.Path(sys.argv[sys.argv.index("--dry-run") + 1]) if dry else C.RES
    S = C.J(d / "r130_scores.json"); V = C.J(d / "r130_validation.json") if (d / "r130_validation.json").exists() else None
    tables = io.open(d / "R130_TABLES.md", encoding="utf-8").read()
    vtxt = io.open(d / "R130_VALIDATION.md", encoding="utf-8").read() if V else "**Labels not yet released.** The judge's validation against A1's labels (registration §6) is appended when hv1 commits `human_validation/hv1/results/labels_A1.json`; no other number changes.\n"
    pr = C.J(C.RUN / "probes_r130.json") if (C.RUN / "probes_r130.json").exists() else {}
    lk = C.J(C.RUN / "lock_r130.json") if (C.RUN / "lock_r130.json").exists() else {}
    pj = C.J(C.RUN / "projection_r130.json") if (C.RUN / "projection_r130.json").exists() else {}
    bt = C.J(C.RUN / "batch_r130_judge.json") if (C.RUN / "batch_r130_judge.json").exists() else {}
    sp = S["spend"]; P = S["predictions"]
    status = V["status"] if V else "labels not yet released; every prediction below is marked 'judge not yet validated' (registration §6)"
    vp = V["validated_predictions"] if V else {}
    LAB = {"P-L1": "ASSERTS", "P-L1b": "ASSERTS", "P-L4": "MENTIONS", "P-L2": "ASSERTS", "P-L3": "ASSERTS", "P-L3b": "ASSERTS"}

    def tag(k):
        if not V:
            return " — judge not yet validated"
        return f" — {LAB[k]} bar {'passes: validated' if vp.get(k) else 'FAILS: UNVALIDATED'}"

    def verd(k, x):
        return f"**{x.get('verdict', 'NOT EVALUABLE')}**{tag(k)}"
    L = [f"# REPORT_R130 — a stronger answerer on the recorded answer-stage views, and a semantic judge (exploratory; written {C.now()})\n",
         f"Program R130; registration `reviews/r130/registrations/REGISTRATION_R130.md` (registered-text sha256 `{S['registration_sha256']}`), frozen in `FREEZE_R130.md` before any call (commit 6f1e76e); deviations in `DEVIATIONS_R130.md`. "
         f"**Everything here is exploratory; no paper text lands from this program.** The judge (Claude Opus 5) shares a vendor with one answerer (Claude Haiku 4.5). "
         f"The human validation sample holds GPT-4.1 mini answers only, so the judge's validated accuracy transfers to Luna's and Haiku's answers by assumption (registration §2i).\n",
         f"## 1. Spend per provider\n\nToken-metered from the rows at the page prices (not an invoice): **OpenAI ${sp['openai']:.4f} of the $4.00 cap** (Luna rows ${sp['luna_rows']:.4f}, probe ${sp['probe_luna']:.4f}); "
         f"**Anthropic ${sp['anthropic']:.4f}** against the registered $8.00 cap, raised to $10.00 for the judge lane by D-R130-5 (the cancelled-then-settled Batch ${sp['judge_batch']:.4f} at the 0.5 rate, "
         f"the synchronous run ${sp['judge_sync_rows']:.4f}, the re-asks at max_tokens 1024 ${sp['judge_reask_rows']:.4f}, the insurance check ${sp['judge_insurance']:.4f}, probe ${sp['probe_judge']:.4f}); "
         f"judge transports in the assembled lane {S['transports']}. "
         + (f"Projection before launch: Luna ${pj.get('LUNA', {}).get('usd', float('nan')):.4f}, judge ${pj.get('JUDGE', {}).get('usd', float('nan')):.4f} at Batch (`run/projection_r130.json`). " if pj else "")
         + (f"Probes: Luna served `{pr['LUNA']['served']}` ({pr['LUNA']['tok_in']} in / {pr['LUNA']['tok_out']} out, {pr['LUNA']['tok_reasoning']} reasoning); judge served `{pr['JUDGE']['served']}` ({pr['JUDGE']['tok_in']} in / {pr['JUDGE']['tok_out']} out). " if pr else "")
         + (f"Judge Batch `{bt.get('id')}` ({bt.get('n')} requests). " if bt else "") + "\n",
         f"## 2. The judge's validation\n\n**Status: {status}**\n\n{vtxt}",
         "## 3. Predictions (registration §5; HELD needs the predicted direction AND reliability: exact McNemar or Fisher p < 0.05 and the persona-grouped interval excluding zero; primary reading, UNSURE neither ASSERTS nor MENTIONS)\n"]

    def pline(k, x, what):
        if "n1" in x:
            return (f"with {x['group1']['asserts']} / {x['n1']} = {x['group1']['rate']} {x['group1']['wilson']}, without {x['group0']['asserts']} / {x['n0']} = {x['group0']['rate']} {x['group0']['wilson']}; delta {x['delta_group1_minus_group0']:+.4f}; "
                    f"Fisher p {x['fisher_p']}; item {x['ci_item']}, persona {x['ci_persona']} ({x['n_personas']} personas): {verd(k, x)}." if x.get("n1") and x.get("n0") else f"**NOT EVALUABLE**{tag(k)}.")
        return (f"n {x['n']}; {what[0]} {x['first']['asserts']} ({x['first']['rate']}), {what[1]} {x['second']['asserts']} ({x['second']['rate']}); delta {x['delta_second_minus_first']:+.4f}; "
                f"discordant {what[0]}-only {x['discordant']['first_only']} / {what[1]}-only {x['discordant']['second_only']}; McNemar p {x['mcnemar_p']}; item {x['ci_item']}, persona {x['ci_persona']} ({x['n_personas']} personas): {verd(k, x)}."
                if x.get("n") else f"**NOT EVALUABLE**{tag(k)}.")
    L.append("- **P-L1** (the answerer link, primary; the 82 obligations answered under the oracle fetch with the tagged forbidding record in view, all states; mini → Luna, ASSERTS below, paired): " + pline("P-L1", P["P-L1"], ("mini", "Luna")))
    L.append("- **P-L1b** (secondary; the 61 lookup-rule pairs with the tagged record in view): " + pline("P-L1b", P["P-L1b"], ("mini", "Luna")))
    L.append("- **P-L4** (the safe form, primary; the P-L1 pairs; mini → Luna, MENTIONS above, paired): " + pline("P-L4", P["P-L4"], ("mini", "Luna")))
    L.append("- **P-L2** (reach helps a strong answerer, primary; within Luna, top-five → lookup on the 40 obligations answered under both, 24 concordant by construction, expected underpowered): " + pline("P-L2", P["P-L2"], ("top-five", "lookup")))
    L.append("- **P-L3** (the copies still bind, primary; Luna under the oracle fetch, an untagged active copy in view against none, 85 of the 89 audited scorable views): " + pline("P-L3", P["P-L3"], None))
    L.append("- **P-L3b** (secondary; the lookup-rule version, 17 against 41): " + pline("P-L3b", P["P-L3b"], None))
    L.append("- The two matched-budget policies of the brief (similarity at the matched budget; the always-on fetch at the matched budget): **NOT EVALUABLE** (registration §2a, ruling 1: reach-only interpolated rows with no recorded answer under the E.10 harness).\n")
    L.append("## 4. The per-policy label table for the three answerers, the readings beside, the retag variant, the sensitivity rows\n")
    L.append(tables.split("\n", 1)[1] if tables.startswith("#") else tables)
    L.append("## 5. Commits\n\n" + "\n".join(f"- `{c}`" for c in commits()) + "\n")
    L.append("## 6. Files\n\n`reviews/r130/build/build_r130.json`, `build/judge_units_r130.json`; `ds_downstream/run/{lock,probes,projection}_r130.json`, `run/rows_ds_r130_luna.jsonl`, `run/batch_r130_judge.json`, `run/rows_ds_r130_judge.jsonl`; "
             "`reviews/r130/results/r130_scores.json`, `results/R130_TABLES.md`" + (", `results/r130_validation.json`, `results/R130_VALIDATION.md`" if V else "") + "; `ds_downstream/NUMBERS_DS.md` section 16. No held texts.\n")
    out = (d if dry else C.R130) / "REPORT_R130.md"
    io.open(out, "w", encoding="utf-8", newline="\n").write("\n".join(L))
    print("written", out)


if __name__ == "__main__":
    main()
