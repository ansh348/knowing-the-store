# -*- coding: utf-8 -*-
"""r130_validate.py -- program R130, Task B's validation: the judge against annotator A1's released labels on the 198 primary rows of the
human validation sample (HV-A), the token detector's same numbers beside. Offline, $0. Scoring only; no label is edited, no call is made.

    python r130_validate.py [--commit <hash>]     reads human_validation/hv1/results/labels_A1.json FROM GIT (git show <commit>:path; default HEAD),
                                                  never from the working tree and never a workbook; refuses if the path is not committed.
                                                  Writes results/r130_validation.json and results/R130_VALIDATION.md; appends AUX-R130-VALIDATION to
                                                  ds_downstream/NUMBERS_DS.md section 16 once.
    --dry-run <dir>                               reads labels_A1.json and the judge rows from <dir> (synthetic), writes there, touches no ledger.

Registration section 6: raw agreement (five-way) on the labelled primary rows; Cohen's kappa (four-way, rows where both labels are not UNSURE)
with the number excluded; the 5 x 5 confusion matrix (A1 rows, judge columns); precision and recall of ASSERTS and of MENTIONS with A1 as the
reference (UNSURE is neither in the primary reading; a sensitivity row drops the rows where either side gave UNSURE). The detector: flag_gold
(stale_use_tau_gold at 0.50, from the HV1 key) as a binary ASSERTS reading: its precision, recall, raw agreement and kappa on the binary.
Bars, per prediction: ASSERTS precision AND recall at or above 0.80 for P-L1, P-L1b, P-L2, P-L3, P-L3b; MENTIONS precision AND recall at or
above 0.80 for P-L4. A prediction whose label misses its bar is reported as unvalidated. The Haiku block, where labelled, prints beside.
"""
from __future__ import annotations

import collections
import io
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r130_common as C  # noqa: E402

LABELS_PATH = "human_validation/hv1/results/labels_A1.json"
BAR = 0.80


def committed_labels(commit):
    r = subprocess.run(["git", "show", f"{commit}:{LABELS_PATH}"], cwd=C.ROOT, capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, f"{LABELS_PATH} is not committed at {commit} -- STOP (the labels are read from git only, after hv1's own commit)"
    h = subprocess.run(["git", "rev-parse", commit], cwd=C.ROOT, capture_output=True, text=True, encoding="utf-8").stdout.strip()
    return json.loads(r.stdout), h


def prf(ref, pred):
    """precision / recall of the positive class (pred against ref), both binary lists."""
    tp = sum(1 for r, p in zip(ref, pred) if r and p); fp = sum(1 for r, p in zip(ref, pred) if p and not r); fn = sum(1 for r, p in zip(ref, pred) if r and not p)
    tn = len(ref) - tp - fp - fn
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": (round(tp / (tp + fp), 4) if tp + fp else None), "recall": (round(tp / (tp + fn), 4) if tp + fn else None),
            "precision_wilson": C.wilson(tp, tp + fp), "recall_wilson": C.wilson(tp, tp + fn), "agreement": round((tp + tn) / len(ref), 4) if ref else None,
            "kappa": C.kappa(list(zip([int(x) for x in ref], [int(x) for x in pred])), [0, 1])[0]}


BARS = {"ASSERTS": ("P-L1", "P-L1b", "P-L2", "P-L3", "P-L3b"), "MENTIONS": ("P-L4",)}


def block_analysis(items, lab, jl, uids, drop_unsure=False):
    us = [u for u in uids if lab.get(u) is not None and jl.get(u) is not None]
    if drop_unsure:
        us = [u for u in us if lab[u] != "UNSURE" and jl[u] != "UNSURE"]
    A = [lab[u] for u in us]; Jd = [jl[u] for u in us]
    conf = {a: {j: 0 for j in C.LABELS} for a in C.LABELS}
    for a, j in zip(A, Jd):
        conf[a][j] += 1
    det_bin = [bool(items[u]["flag_gold"]) for u in us]
    k4, n4 = C.kappa(list(zip(A, Jd)), [l for l in C.LABELS if l != "UNSURE"])
    k5, n5 = C.kappa(list(zip(A, Jd)), C.LABELS)
    out = {"rows": len(uids), "labelled_and_judged": len(us), "unlabelled": sum(1 for u in uids if lab.get(u) is None), "unjudged": sum(1 for u in uids if jl.get(u) is None),
           "drop_unsure": drop_unsure, "raw_agreement_5way": round(sum(1 for a, j in zip(A, Jd) if a == j) / len(us), 4) if us else None,
           "kappa_4way": k4, "kappa_4way_rows": n4, "kappa_4way_excluded": len(us) - n4, "kappa_5way": k5,
           "confusion_A1_rows_judge_cols": conf, "a1_distribution": dict(collections.Counter(A)), "judge_distribution": dict(collections.Counter(Jd)),
           "detector_ASSERTS": prf([a == "ASSERTS" for a in A], det_bin)}
    for lab_ in ("ASSERTS", "MENTIONS", "CLEAN", "ABSTAINS"):
        out[f"judge_{lab_}"] = prf([a == lab_ for a in A], [j == lab_ for j in Jd])
    out["bars"] = {}
    for lab_, preds in BARS.items():
        x = out[f"judge_{lab_}"]
        ok = bool(x["precision"] is not None and x["recall"] is not None and x["precision"] >= BAR and x["recall"] >= BAR)
        out["bars"][lab_] = {"precision": x["precision"], "recall": x["recall"], "at_least": BAR, "passes": ok, "predictions": list(preds)}
    out["disagreements"] = [{"uid": u, "A1": lab[u], "judge": jl[u], "flag": items[u]["flag_gold"], "cond": items[u]["cond"], "state": items[u]["state"]} for u in us if lab[u] != jl[u]]
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    dry = "--dry-run" in sys.argv; indir = pathlib.Path(sys.argv[sys.argv.index("--dry-run") + 1]) if dry else None
    commit = sys.argv[sys.argv.index("--commit") + 1] if "--commit" in sys.argv else "HEAD"
    if dry:
        la, h = C.J(indir / "labels_A1.json"), "dry-run"
        judge_rows = indir / "rows_ds_r130_judge.jsonl"
    else:
        C.assert_frozen(); C.assert_inputs()
        la, h = committed_labels(commit); judge_rows = C.RUN / "rows_ds_r130_judge_assembled.jsonl"
    assert la["meta"]["annotator"] == "A1", "not A1's file"
    b = C.J(C.BUILD / "build_r130.json"); lock = b["hv1_lock"]
    key = C.J(C.HV1 / "key" / "key_hv1.json"); items = key["hva"]["items"]
    judge = {json.loads(l)["unit_id"]: json.loads(l) for l in io.open(judge_rows, encoding="utf-8") if l.strip()}
    jl = {uid: judge[lock[uid]]["label"] for uid in lock if lock[uid] in judge and judge[lock[uid]]["status"] == "OK"}
    lab = {v["uid"]: v["label"] for v in la["labels"]["ANSWERS"].values() if v.get("label")}
    prim = [u for u, it in items.items() if it["block"] == "primary"]; haiku = [u for u, it in items.items() if it["block"] == "haiku"]
    S = {"program": C.PROGRAM, "labels_commit": h, "labels_source": LABELS_PATH if not dry else "synthetic", "when": C.now(),
         "primary": block_analysis(items, lab, jl, prim), "primary_drop_unsure": block_analysis(items, lab, jl, prim, drop_unsure=True),
         "haiku_block": block_analysis(items, lab, jl, haiku), "changed_148": block_analysis(items, lab, jl, [u for u in prim if items[u]["cond"] != "control"]),
         "controls_50": block_analysis(items, lab, jl, [u for u in prim if items[u]["cond"] == "control"])}
    P = S["primary"]; bars = P["bars"]
    S["validated_predictions"] = {pred: bars[lab_]["passes"] for lab_, x in bars.items() for pred in x["predictions"]}
    S["status"] = "; ".join(f"{lab_} bar (P and R >= 0.80) {'PASSES' if x['passes'] else 'FAILS'} (P {x['precision']}, R {x['recall']}): {', '.join(x['predictions'])} "
                            f"{'validated' if x['passes'] else 'UNVALIDATED'}" for lab_, x in bars.items())
    outdir = indir if dry else C.RES
    # the author's constraint of 2026-09-20: the aggregate file keeps disagreement counts only; the uid-level list goes to a separate, undisplayed file
    items = {}
    for k, blk in list(S.items()):
        if isinstance(blk, dict) and "disagreements" in blk:
            items[k] = blk.pop("disagreements")
            blk["n_disagreements"] = len(items[k]); blk["disagreements_by_pair"] = {f"{d['A1']}->{d['judge']}": n for (_, n) in [(0, 0)] for _ in []}
            blk["disagreements_by_pair"] = dict(collections.Counter(f"{d['A1']}->{d['judge']}" for d in items[k]))
    C.jdump({"note": "item-level material of r130_validation.json (the disagreement rows with uids); not displayed while A2's sheet is unlabelled", "disagreements": items}, outdir / "r130_validation_items.json")
    C.jdump(S, outdir / "r130_validation.json")
    jp, jm, dp = P["judge_ASSERTS"], P["judge_MENTIONS"], P["detector_ASSERTS"]; Pd = S["primary_drop_unsure"]
    L = [f"# R130 validation of the judge against A1 ({'synthetic dry run' if dry else 'labels at ' + h[:12]}; written {S['when']})\n", f"**{S['status']}**\n",
         f"Primary rows {P['rows']}: labelled and judged {P['labelled_and_judged']} (unlabelled {P['unlabelled']}, unjudged {P['unjudged']}).\n",
         "| reading | precision [Wilson] | recall [Wilson] | raw agreement | kappa | rows |\n|---|---|---|---|---|---:|",
         f"| judge, ASSERTS (five labels; kappa four-way, {P['kappa_4way_excluded']} UNSURE rows excluded) | {jp['precision']} {jp['precision_wilson']} | {jp['recall']} {jp['recall_wilson']} | {P['raw_agreement_5way']} (five-way) | {P['kappa_4way']} | {P['kappa_4way_rows']} |",
         f"| judge, MENTIONS | {jm['precision']} {jm['precision_wilson']} | {jm['recall']} {jm['recall_wilson']} | {jm['agreement']} (binary) | {jm['kappa']} | {P['labelled_and_judged']} |",
         f"| judge, ASSERTS binary | {jp['precision']} | {jp['recall']} | {jp['agreement']} | {jp['kappa']} | {P['labelled_and_judged']} |",
         f"| token detector at 0.50, ASSERTS binary | {dp['precision']} {dp['precision_wilson']} | {dp['recall']} {dp['recall_wilson']} | {dp['agreement']} | {dp['kappa']} | {P['labelled_and_judged']} |",
         f"| judge, CLEAN / ABSTAINS (P, R) | {P['judge_CLEAN']['precision']}, {P['judge_CLEAN']['recall']} | {P['judge_ABSTAINS']['precision']}, {P['judge_ABSTAINS']['recall']} | | | |",
         f"| sensitivity, UNSURE rows dropped: ASSERTS / MENTIONS (P, R) | {Pd['judge_ASSERTS']['precision']}, {Pd['judge_ASSERTS']['recall']} | {Pd['judge_MENTIONS']['precision']}, {Pd['judge_MENTIONS']['recall']} | {Pd['raw_agreement_5way']} | {Pd['kappa_4way']} | {Pd['labelled_and_judged']} |",
         "\nConfusion (A1 rows, judge columns):\n", "| A1 \\ judge | " + " | ".join(C.LABELS) + " |", "|---|" + "---:|" * len(C.LABELS)]
    for a in C.LABELS:
        L.append(f"| {a} | " + " | ".join(str(P["confusion_A1_rows_judge_cols"][a][j]) for j in C.LABELS) + " |")
    for name, X in (("changed_148", "The 148 (74 views before / after)"), ("controls_50", "The 50 controls"), ("haiku_block", "The Haiku block (labelled part)")):
        x = S[name]; jx, mx, dx = x["judge_ASSERTS"], x["judge_MENTIONS"], x["detector_ASSERTS"]
        L.append(f"\n{X}: {x['labelled_and_judged']} rows; judge ASSERTS P {jx['precision']} R {jx['recall']}, MENTIONS P {mx['precision']} R {mx['recall']}, agreement {x['raw_agreement_5way']}, kappa {x['kappa_4way']}; detector P {dx['precision']} R {dx['recall']}.")
    L.append(f"\nDisagreements (primary): {P['n_disagreements']}; by A1->judge: {P['disagreements_by_pair']}\n")
    txt = "\n".join(L) + "\n"
    io.open(outdir / "R130_VALIDATION.md", "w", encoding="utf-8", newline="\n").write(txt); print(txt)
    if not dry:
        led = C.LEDGER.read_text(encoding="utf-8")
        assert "## 16. Program R130" in led and "AUX-R130-VALIDATION" not in led, "section 16 missing or the validation key exists already -- STOP"
        C.append_ledger("AUX-R130-VALIDATION",
                        f"Judge against A1 on the {P['labelled_and_judged']} labelled primary rows (labels at commit `{h[:12]}`): ASSERTS precision {jp['precision']} {jp['precision_wilson']}, recall {jp['recall']} {jp['recall_wilson']}; "
                        f"MENTIONS precision {jm['precision']} {jm['precision_wilson']}, recall {jm['recall']} {jm['recall_wilson']}; raw agreement {P['raw_agreement_5way']}, kappa (four-way, {P['kappa_4way_excluded']} excluded) {P['kappa_4way']}; "
                        f"the token detector at 0.50: precision {dp['precision']}, recall {dp['recall']}, agreement {dp['agreement']}, kappa {dp['kappa']}. {S['status']}.")
        print("AUX-R130-VALIDATION appended")


if __name__ == "__main__":
    main()
