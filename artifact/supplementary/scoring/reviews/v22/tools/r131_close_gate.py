# -*- coding: utf-8 -*-
"""r131_close_gate.py -- the R131 close (2026-09-20; the author's blocks 'R131 CONSOLIDATED ADDITIONS', 'ABSTRACT SWAP + ITS PAYER', 'R131 MERGED RULINGS'
and 'R131 FINAL RULINGS'): the number gate on every number the close's new texts print, each read from its artifact and compared at the printed
precision (half-up on the recorded four-decimal value, the convention of r131_number_gate.py), and the provenance facts of Appendix E.3's new
paragraph (A1''), each counted from the tree. A mismatch is listed; nothing is adjusted; exit 1 on any mismatch (the hard stop). CHECKS and PROV are
read by port_r131_close.py, appendix_r131_close.py and ledger_r131_close.py, so no number in those texts is typed by hand.
Usage: python reviews/v22/tools/r131_close_gate.py
"""
from __future__ import annotations

import glob
import json
import pathlib
import re
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parents[3]
R125 = ROOT / "reviews" / "r125" / "results"
M = json.load(open(R125 / "r125_matched.json", encoding="utf-8"))
T4 = json.load(open(R125 / "r125_t4_sibling.json", encoding="utf-8"))
RD, PD = M["readers"], M["paired"]
IX = json.load(open(ROOT / "r82_counterfactual" / "cf2" / "results" / "cf_scores_ix.json", encoding="utf-8"))
E1R = (ROOT / "e1r_robustness" / "NUMBERS_E1R.md").read_text(encoding="utf-8", errors="replace")
CF3 = (ROOT / "r82_counterfactual" / "cf3" / "NUMBERS_CF3.md").read_text(encoding="utf-8", errors="replace")
R85 = (ROOT / "r85_graphiti" / "NUMBERS_R85.md").read_text(encoding="utf-8", errors="replace")
FREEZE_FR = "5b097fb"   # the FR-Bank release's freeze commit (audit/FREEZE_MANIFEST.md; Zenodo 10.5281/zenodo.20067778)

CHECKS = []
PROV = {}


def r2(x):
    return str(Decimal(str(round(x, 4))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def check(where, printed, value, source, ok=None, reliable=None, actual_reliable=None):
    if ok is None:
        ok = (r2(value) == printed) if isinstance(value, float) else (str(value) == str(printed))
    CHECKS.append({"where": where, "printed": str(printed), "value": value, "source": source, "ok": bool(ok), "reliable": reliable, "actual_reliable": actual_reliable})


def e1r_row(label):
    """A row of NUMBERS_E1R.md section 11 (AUX-E1R-NB6): '| R-NOK-FRB | TRUE | 661 | 0.7339 | 0.5738 | **0.7484** | 0.7484 | ...' -> (monitor, NB-6)."""
    sec = E1R[E1R.index("## 11. `AUX-E1R-NB6`"):E1R.index("## 12. ")]
    for ln in sec.splitlines():
        if ln.startswith(label) and "**" in ln:
            nums = [float(x) for x in re.findall(r"\d\.\d{4}", ln)]
            return nums[0], float(re.search(r"\*\*(\d\.\d{4})\*\*", ln).group(1))
    raise KeyError(label)


def main():
    # ---------------------------------------------------------------------------------------------------------- the abstract (B1)
    n148 = RD["LOOKUP_v2"]["pn_vs_present"]["whole"]["n"]
    check("Abstract: 148 questions", "148", n148, "r125_matched.json readers/LOOKUP_v2/pn_vs_present/whole/n (the triples of the 444)")
    # the sibling floor: every model and the lookup at or above 0.88 (PN vs sibling, matched)
    sib = {k: v["pn_vs_sibling"]["matched"] if "pn_vs_sibling" in v else None for k, v in T4["readers"].items()}
    models = {k: v for k, v in sib.items() if v is not None and not k.startswith(("Random-token", "Count reader"))}
    floor = min(models.values())
    check("Abstract: 'at an AUROC of 0.88 or higher' (the lookup and every model, PN against the sibling, matched)", "0.88", floor,
          f"r125_t4_sibling.json readers/*/pn_vs_sibling/matched, minimum over {sorted(models)} = {floor:.4f}")
    check("Abstract: chance 0.50", "0.50", 0.5, "the definition (a tie scores half)")
    # the lead 0.08 to 0.10, the matched metric, reader minus lookup, whole set
    leads = {k: PD["vs_lookup"][k]["pn_vs_present"]["whole"] for k in ("LUNA_v2", "SOL_v2", "OP5_v2")}
    lo, hi = min(v["delta"] for v in leads.values()), max(v["delta"] for v in leads.values())
    check("Abstract: 'lead the lookup by 0.08 to 0.10 overall' (lower end)", "0.08", lo, "r125_matched.json paired/vs_lookup/{LUNA_v2,SOL_v2,OP5_v2}/pn_vs_present/whole/delta (+0.1014, +0.0811, +0.0980)",
          reliable=True, actual_reliable=all(v["both_exclude_zero"] for v in leads.values()))
    check("Abstract: 'lead the lookup by 0.08 to 0.10 overall' (upper end)", "0.10", hi, "as above")
    # the lead comes from retracted and expired records: supersession not reliable, every counted-state delta positive
    sup_ok = all(not PD["vs_lookup"][k]["pn_vs_present"]["per_state"]["SUPERSESSION"]["both_exclude_zero"] for k in leads)
    ctd_ok = all(PD["vs_lookup"][k]["pn_vs_present"]["per_state"][s]["delta"] > 0 for k in leads for s in ("RETRACTION", "EXPIRY"))
    check("Abstract: 'a lead that comes from retracted and expired records' (no stronger model reliably above the lookup on supersession; every retraction and expiry lead positive)",
          "holds", "holds" if (sup_ok and ctd_ok) else "fails", "r125_matched.json paired/vs_lookup/*/pn_vs_present/per_state", ok=sup_ok and ctd_ok)
    # FR-Bank's own metadata: the full obligation set, ground truth against the capped store-written summary
    t_true, t_bel = e1r_row("| R-NOK-FRB | TRUE |"), e1r_row("| R-NOK-FRB | BELIEVED |")
    mini_true, lookup_true = t_true
    mini_bel, lookup_bel = t_bel
    check("Abstract: mini under the ground-truth summary (full obligation set)", "0.73", mini_true, "e1r_robustness/NUMBERS_E1R.md AUX-E1R-TRUE-NOK / AUX-E1R-NB6 row R-NOK-FRB TRUE, monitor 0.7339")
    check("Abstract: the lookup under the ground-truth summary", "0.75", lookup_true, "NUMBERS_E1R.md AUX-E1R-NB6 row R-NOK-FRB TRUE, NB-6 0.7484")
    check("Abstract: mini under FR-Bank's capped store-written summary", "0.60", mini_bel, "NUMBERS_E1R.md AUX-E1R-BELIEVED-NOK row R-NOK-FRB BELIEVED, monitor 0.5959")
    check("Abstract: the lookup under FR-Bank's capped store-written summary", "0.59", lookup_bel, "NUMBERS_E1R.md AUX-E1R-NB6 row R-NOK-FRB BELIEVED, NB-6 0.5858")
    PROV["drops"] = (mini_true - mini_bel, lookup_true - lookup_bel)
    check("Abstract: five models, the two smaller (mini, Haiku) and three stronger (Luna, Sol, Opus)", "5", 5, "Section 4's model list (the five readers of Table 1)")

    # ---------------------------------------------------------------------------------------------------------- Section 5.2, payer 8
    cov = M["coverage_only"]
    check("Section 5.2 (payer 8): the coverage-only reader, pooled", "0.75", float(cov["pair_classes"]["pooled"]), "r125_matched.json coverage_only/pair_classes/pooled")
    check("Section 5.2 (payer 8): the coverage-only reader, matched", "0.50", float(cov["pn_vs_present"]["matched"]), "r125_matched.json coverage_only/pn_vs_present/matched")
    rt = PD["vs_lookup"]["RANDTOK_v2"]["pn_vs_present"]["whole"]
    check("Section 5.2 (payer 8): the lookup a reliable 0.13 above meaningless tokens on the matched metric", "0.13", -rt["delta"],
          "r125_matched.json paired/vs_lookup/RANDTOK_v2/pn_vs_present/whole/delta (-0.1318, both intervals clear of zero)", reliable=True, actual_reliable=bool(rt["both_exclude_zero"]))

    # ---------------------------------------------------------------------------------------------------------- the Conclusion, payer 5b (P5b)
    def same_store(lane, pop="A"):
        d = IX["readers"][lane][pop]["P1"]
        return float((d.get("draw1") or {}).get("same_store", {}).get("auroc") or d["same_store"]["auroc"])
    p1 = {k: same_store(k) for k in ("MINI", "H45", "LUNA", "SOL", "OP5")}
    cue = float(IX["lookups"]["A"]["keyword"]["same_store"]["auroc"])
    check("Conclusion (P5b): 'only the three stronger models apply it' (Luna, Sol, Opus each above 0.85 under the explicit rubric; mini and Haiku below 0.60)", "holds",
          "holds" if all(p1[k] > 0.85 for k in ("LUNA", "SOL", "OP5")) and all(p1[k] < 0.60 for k in ("MINI", "H45")) else "fails",
          f"cf_scores_ix.json readers/*/A/P1 same-store AUROC (draw 1 where five draws ran): {p1}", ok=all(p1[k] > 0.85 for k in ("LUNA", "SOL", "OP5")) and all(p1[k] < 0.60 for k in ("MINI", "H45")))
    check("Conclusion (P5b): 'a fixed cue list matches the best of them' (the cue list and the best model round to the same value)", r2(max(p1.values())), cue,
          f"cf_scores_ix.json lookups/A/keyword/same_store/auroc {cue:.4f} against the best model {max(p1.values()):.4f}")

    # ---------------------------------------------------------------------------------------------------------- Limitations L1 and the provenance paragraph (A1'')
    personas = sorted(p for p in glob.glob(str(ROOT / "LifeMemEval" / "[0-9]*_*")) if pathlib.Path(p).is_dir())
    yamls = glob.glob(str(ROOT / "LifeMemEval" / "[0-9]*_*" / "persona_*.yaml"))
    sessions = glob.glob(str(ROOT / "LifeMemEval" / "[0-9]*_*" / "sessions" / "session_*.json"))
    PROV.update(personas=len(personas), manifests=len(yamls), sessions=len(sessions))
    check("Limitations L1 / E.3: 40 personas (numbered persona directories of LifeMemEval/)", "40", len(personas), "LifeMemEval/<n>_<name>/ directories")
    check("E.3: 40 human-written manifests (one persona_*.yaml per directory)", "40", len(yamls), "LifeMemEval/<n>_<name>/persona_*.yaml")
    check("E.3: 1,400 sessions (35 per persona)", "1400", len(sessions), "LifeMemEval/<n>_<name>/sessions/session_*.json")
    # the three stores in the release's freeze
    ls = subprocess.run(["git", "ls-tree", "-d", "--name-only", FREEZE_FR, "LifeMemEval/artifacts/"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    stores = ["LifeMemEval/artifacts/lifecycle_banks", "LifeMemEval/artifacts/mem0_41mini_banks", "LifeMemEval/artifacts/amem_banks"]
    check("E.3: the three stores (FR-Bank, Mem0, A-MEM banks) are in the release's freeze commit", "3", sum(s in ls for s in stores),
          f"git ls-tree {FREEZE_FR} LifeMemEval/artifacts/ (the directories e1_metamemory/tools/backends.py:59-61 reads)")
    PROV["stores_in_freeze"] = sum(s in ls for s in stores)
    # the main study's items against the released questions
    rel = json.load(open(ROOT / "LifeMemEval" / "lifemembench_questions.json", encoding="utf-8"))
    rel_ids = {q["id"] for q in rel}
    items = json.load(open(ROOT / "e1_metamemory" / "build" / "items_final.json", encoding="utf-8"))
    items = items if isinstance(items, list) else items["items"]
    scored = ("ABSENT", "PRESENT", "PRESENT-NEGATIVE")
    fr = [it for it in items if it["backend"] == "frbank" and it["label"] in scored]
    fr_rel = [it for it in fr if it["question_id"] in rel_ids]
    fr_probe = [it for it in fr if it["question_id"].startswith("probe")]
    PROV.update(released_total=len(rel), fr_items=len(fr), fr_items_released=len(fr_rel), fr_released_distinct=len({it["question_id"] for it in fr_rel}),
                fr_probes=len(fr_probe), fr_probe_texts=len({it["question_id"] for it in fr_probe}),
                fr_released_by_variant={v: len({it["question_id"] for it in fr_rel if it["variant"] == v}) for v in ("FULL", "CAT-ABLATED", "SLOT-ABLATED")},
                released_distinct_all=len({it["question_id"] for it in items if it["label"] in scored and it["question_id"] in rel_ids}))
    check("E.3: the release's question file holds 516 questions", "516", len(rel), "LifeMemEval/lifemembench_questions.json")
    check("E.3: the full obligation set is 661 FR-Bank items", "661", len(fr), "e1_metamemory/build/items_final.json (backend frbank, labels ABSENT / PRESENT / PRESENT-NEGATIVE)")
    check("E.3: 516 of the 661 ask a released question", "516", len(fr_rel), "items_final.json question_id in lifemembench_questions.json ids")
    check("E.3: 187 distinct released questions among them", "187", PROV["fr_released_distinct"], "as above, distinct question_id")
    check("E.3: 145 natural-absent probe items", "145", len(fr_probe), "items_final.json question_id 'probe_*' (the hard tier's natural-absent items)")
    check("E.3: the released questions used on the full store, the category-removed and the slot-removed variants (178 / 176 / 162)", "178/176/162",
          "/".join(str(PROV["fr_released_by_variant"][v]) for v in ("FULL", "CAT-ABLATED", "SLOT-ABLATED")), "items_final.json by variant")
    assert len(fr_rel) + len(fr_probe) == len(fr), (len(fr_rel), len(fr_probe), len(fr))
    # the counterfactual set
    cfq = json.load(open(ROOT / "r82_counterfactual" / "cf2" / "cf_questions_cf2.json", encoding="utf-8"))
    check("E.3: 148 counterfactual questions drafted by GPT-4.1 mini", "148", len(cfq["questions"]), "r82_counterfactual/cf2/cf_questions_cf2.json questions")
    check("E.3: 444 counterfactual items (three versions each)", "444", 3 * len(cfq["questions"]), "3 x 148 (Table tab:setup; r125_matched.json n=148 triples)")
    m = re.search(r"\*\*AUX-CF3\*\*[^\n]*?(\d+) pairs, (\d+) items", CF3)
    check("E.3: the expiry extension, 14 pairs", "14", int(m.group(1)), "r82_counterfactual/cf3/NUMBERS_CF3.md AUX-CF3")
    check("E.3: the expiry extension, 42 items", "42", int(m.group(2)), "r82_counterfactual/cf3/NUMBERS_CF3.md AUX-CF3")
    PROV.update(cf_questions=len(cfq["questions"]), cf_items=3 * len(cfq["questions"]), ext_pairs=int(m.group(1)), ext_items=int(m.group(2)))
    # the crossed intent questions
    cnt = IX["lock"]["counts"]
    PROV.update(crossed_drafted=cnt["A_total"] + cnt["B_total"], crossed_asked=cnt["A_pass"] + cnt["B_pass"], crossed_dropped=cnt["drops"])
    check("E.3: crossed intent questions drafted (88 + 30)", "118", PROV["crossed_drafted"], "cf_scores_ix.json lock/counts A_total + B_total")
    check("E.3: crossed intent questions asked (87 + 26)", "113", PROV["crossed_asked"], "cf_scores_ix.json lock/counts A_pass + B_pass")
    assert PROV["crossed_drafted"] - PROV["crossed_asked"] == cnt["drops"] == 5
    # the paraphrases
    para = json.load(open(ROOT / "cf2_paraphrase" / "para_questions.json", encoding="utf-8"))
    check("E.3: 148 paraphrases drafted by GPT-4.1 mini", "148", len(para["rows"]), f"cf2_paraphrase/para_questions.json rows (meta.model {para['meta']['model']})")
    assert para["meta"]["model"] == "gpt-4.1-mini"
    PROV["paraphrases"] = len(para["rows"])
    # the cross-vendor set
    cell = json.load(open(ROOT / "e1xv_crossvendor" / "manifests" / "cell_84.json", encoding="utf-8"))
    xv = cell["items"]
    xv_rel = sum(it["item_id"].split(":")[2] in rel_ids for it in xv)
    xv_probe = sum(it["item_id"].startswith("probe:") for it in xv)
    PROV.update(xv_items=len(xv), xv_released=xv_rel, xv_probes=xv_probe)
    check("E.3: the cross-vendor set, 84 main-study items", "84", len(xv), "e1xv_crossvendor/manifests/cell_84.json items")
    check("E.3: of them 76 with a released question and 8 natural-absent probes", "76/8", f"{xv_rel}/{xv_probe}", "cell_84.json item ids against lifemembench_questions.json")
    assert xv_rel + xv_probe == len(xv)
    # Graphiti
    st = json.load(open(ROOT / "r85_graphiti" / "g10" / "ingest_all_status.json", encoding="utf-8"))
    m85 = re.search(r"Personas / episodes / records \| (\d+) / (\d+) / (\d+)", R85)
    done = st["done"] if isinstance(st["done"], int) else len(st["done"])
    PROV.update(graphs=done, episodes=int(m85.group(2)))
    check("E.3: 40 Graphiti graphs", "40", done, "r85_graphiti/g10/ingest_all_status.json done")
    check("E.3: 1,365 episodes rendered from FR-Bank's records", "1365", int(m85.group(2)), "r85_graphiti/NUMBERS_R85.md AUX-R85-G10-INGEST (Personas / episodes / records 40 / 1365 / 18936)")

    bad = [c for c in CHECKS if not c["ok"]]
    for c in CHECKS:
        v = c["value"]
        vs = f"{v:.4f}" if isinstance(v, float) else str(v)
        print(f"{'ok  ' if c['ok'] else 'FAIL'} {c['where']}: printed {c['printed']} <- {vs}  [{c['source']}]")
    print(f"\n{len(CHECKS)} checks, {len(bad)} mismatches")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
