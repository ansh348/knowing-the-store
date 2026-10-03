# -*- coding: utf-8 -*-
"""score_a2.py -- R85 Amendment 2 Step 3: the committed detector rows on every answer (secondary, provisional), the transition tables,
the blind sheet and its sealed key. NO MODEL CALL. $0. A2-P1 to A2-P3 are NOT read here: their endpoints are human-scored (section 6)
and the human read (Step 4) has not run; no ruling-table row is entered.

Detector rows: run_ds.score_answer (stale use at TAU_HI / TAU_GOLD, stale surfacing, successor use, both; PRESENT correct at TAU_GOLD /
TAU_HI), amend4_header.is_abst (abstention), amend7_reported.reports_obligation (obligation reported), the evidence-in-view flag of
build_views_a2 (section 6's decline rule). Expiry obligations are unscorable for stale use by the detector (the DS forensic finding);
they print as unscorable. Paired differences of the detector rates (C1, C2, C3) with item-level and persona-clustered bootstraps
(1,000 draws, seed 42) print as descriptive rows beside the structural bound; they are not the endpoint.

Writes a2/results/detector_a2.json, a2/sheet_a2.md, a2/sheet_key.json; appends AUX-R85-A2-DETECTOR, -TRANSITIONS, -SEAL to
r85_graphiti/NUMBERS_R85.md.
"""
from __future__ import annotations

import collections
import datetime as dt
import hashlib
import io
import json
import random
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
R85 = HERE.parent
ROOT = R85.parent
sys.path.insert(0, str(ROOT / "reviews" / "r114" / "tools"))
from r114_common import assert_spec, J, jdump, r4  # noqa: E402
import build_views_a2 as B                                                   # noqa: E402
import run_ds as RD                                                          # noqa: E402
import amend4_header as A4                                                   # noqa: E402
import amend7_reported as A7                                                 # noqa: E402
import resp_common as RC                                                     # noqa: E402

LEDGER = R85 / "NUMBERS_R85.md"
ROWS_P = HERE / "rows_a2_mini.jsonl"
RES = HERE / "results"
N_BOOT, SEED = 1000, 42
CONDS = ("U", "T", "M")


def boot(d, pers):
    d = np.asarray(d, float); n = len(d); rng = np.random.default_rng(SEED)
    groups = np.unique(pers); by = {u: np.flatnonzero(pers == u) for u in groups}
    di = [d[rng.integers(0, n, n)].mean() for _ in range(N_BOOT)]
    dc = [d[np.concatenate([by[groups[t]] for t in rng.integers(0, len(groups), len(groups))])].mean() for _ in range(N_BOOT)]
    return {"D": r4(d.mean()), "n": n, "item": [r4(np.percentile(di, 2.5)), r4(np.percentile(di, 97.5))], "persona": [r4(np.percentile(dc, 2.5)), r4(np.percentile(dc, 97.5))]}


def fmt(b):
    return f"{b['D']:+.4f} ([{b['item'][0]:+.4f}, {b['item'][1]:+.4f}]; [{b['persona'][0]:+.4f}, {b['persona'][1]:+.4f}])"


def main():
    B.assert_lineage(); sys.stdout.reconfigure(encoding="utf-8")
    V = J(B.OUT_VIEWS); cells = V["cells"]; rows = V["rows"]
    ans = {}
    for l in io.open(ROWS_P, encoding="utf-8"):
        r = json.loads(l); ans[r["key"]] = r
    assert all(r["key"] in ans for r in rows) and all(ans[r["key"]]["status"] == "OK" for r in rows)
    sub = RC.load_cell(); byid = {it["item_id"]: it for it in sub}; rec = RD.records(sub)
    # ---------------------------------------------------------------- detector rows
    per = {}      # (store, pop, cond, item) -> scored
    for r in rows:
        it = byid[r["item_id"]]; rc = rec[r["item_id"]]; a = ans[r["key"]]["answer"]; v = cells[f"{r['store']}|{r['population']}"][r["item_id"]]
        s = RD.score_answer(it, rc, a) if rc else {}
        s["abstains"] = A4.is_abst(a); s["expiry_unscorable"] = (it["label"] == "PRESENT-NEGATIVE" and it["state"] == "exp")
        if it["label"] == "PRESENT-NEGATIVE":
            s["reported"], s["reported_mode"] = A7.reports_obligation(a, s); s["names_state"] = A7.names_state(a)
        s["evidence_in_view"] = v["flags"]["evidence_in_view"][r["condition"]]
        s["decline_class"] = (None if not s["abstains"] else ("appropriate" if s["evidence_in_view"] is False else ("unnecessary" if s["evidence_in_view"] else "n/a")))
        per[(r["store"], r["population"], r["condition"], r["item_id"])] = {**s, "answer": a, "key": r["key"], "n_lines": v[r["condition"]] and len(v[r["condition"]])}
    # ---------------------------------------------------------------- per cell summaries and the paired detector differences
    cellsum, paired, trans = {}, {}, {}
    for ck, cell in cells.items():
        store, pname = ck.split("|")
        obl = [i for i, v in cell.items() if v["label"] == "PRESENT-NEGATIVE"]; lic = [i for i, v in cell.items() if v["label"] == "PRESENT"]
        pers_o = np.array([cell[i]["persona"] for i in obl]); pers_l = np.array([cell[i]["persona"] for i in lic])
        S = {}
        for c in CONDS:
            po = [per[(store, pname, c, i)] for i in obl]; pl = [per[(store, pname, c, i)] for i in lic]
            scor = [p for p in po if not p["expiry_unscorable"]]
            S[c] = {"obligations": {"n": len(po), "abstained": sum(p["abstains"] for p in po), "scorable": len(scor), "stale_tau_gold": sum(bool(p.get("stale_use_tau_gold")) for p in scor), "stale_tau_hi": sum(bool(p.get("stale_use")) for p in scor),
                                    "stale_surface": sum(bool(p.get("stale_surface")) for p in scor), "successor_use_sup": sum(bool(p.get("successor_use")) for p in po), "reported_a7": sum(bool(p.get("reported")) for p in po),
                                    "expiry_unscorable": sum(p["expiry_unscorable"] for p in po), "with_replacement_successor_in_view": sum(1 for i, p in zip(obl, po) if cell[i]["subtype"] == "with-replacement" and p["evidence_in_view"])},
                    "licensed": {"n": len(pl), "correct_tau_gold": sum(bool(p.get("correct")) for p in pl), "correct_tau_hi": sum(bool(p.get("correct_tau_hi")) for p in pl), "abstained": sum(p["abstains"] for p in pl),
                                 "unnecessary_decline": sum(p["decline_class"] == "unnecessary" for p in pl), "appropriate_decline": sum(p["decline_class"] == "appropriate" for p in pl), "evidence_in_view": sum(bool(p["evidence_in_view"]) for p in pl),
                                 "by_intent": {}}}
            for intent in ("CURRENT-STATE", "UPCOMING", "CHANGE-AWARE", "PAST-EVENT"):
                ii = [k for k, i in enumerate(lic) if cell[i]["intent"] == intent]
                S[c]["licensed"]["by_intent"][intent] = {"n": len(ii), "correct": sum(bool(pl[k].get("correct")) for k in ii), "unnecessary_decline": sum(pl[k]["decline_class"] == "unnecessary" for k in ii)}
        cellsum[ck] = S
        # paired detector rows (descriptive; the endpoints of C1 to C3 are human-scored)
        def vec(c, ids, f):
            return [float(f(per[(store, pname, c, i)])) for i in ids]
        stale = lambda p: bool(p.get("stale_use_tau_gold")) and not p["expiry_unscorable"]          # noqa: E731
        corr = lambda p: bool(p.get("correct"))                                                     # noqa: E731
        undec = lambda p: p["decline_class"] == "unnecessary"                                       # noqa: E731
        P_ = {"C1_stale_T_minus_U_47": boot(np.array(vec("T", obl, stale)) - np.array(vec("U", obl, stale)), pers_o),
              "C2_stale_M_minus_T_47": boot(np.array(vec("M", obl, stale)) - np.array(vec("T", obl, stale)), pers_o),
              "C2_reported_M_minus_T_47": boot(np.array(vec("M", obl, lambda p: bool(p.get("reported")))) - np.array(vec("T", obl, lambda p: bool(p.get("reported")))), pers_o),
              "C3_correct_M_minus_U_131": boot(np.array(vec("M", lic, corr)) - np.array(vec("U", lic, corr)), pers_l),
              "C3_correct_T_minus_U_131": boot(np.array(vec("T", lic, corr)) - np.array(vec("U", lic, corr)), pers_l),
              "C3_unnecessary_decline_M_minus_U_131": boot(np.array(vec("M", lic, undec)) - np.array(vec("U", lic, undec)), pers_l), "by_intent": {}}
        for intent in ("CURRENT-STATE", "UPCOMING", "CHANGE-AWARE", "PAST-EVENT"):
            ii = [i for i in lic if cell[i]["intent"] == intent]
            if len(ii) >= 2:
                P_["by_intent"][intent] = {"n": len(ii), "correct_M_minus_U": boot(np.array(vec("M", ii, corr)) - np.array(vec("U", ii, corr)), np.array([cell[i]["persona"] for i in ii]))}
        paired[ck] = P_
        # transition tables U->T and T->M: obligation rows by the detector's category (stale / declined / other), licensed rows (correct / declined / wrong)
        def cat_o(p):
            return "unscorable" if p["expiry_unscorable"] else ("stale" if p.get("stale_use_tau_gold") else ("declined" if p["abstains"] else "other"))
        def cat_l(p):
            return "correct" if p.get("correct") else ("declined" if p["abstains"] else "wrong")
        T_ = {}
        for a, b_ in (("U", "T"), ("T", "M")):
            T_[f"{a}->{b_}"] = {"obligations": dict(collections.Counter(f"{cat_o(per[(store, pname, a, i)])}->{cat_o(per[(store, pname, b_, i)])}" for i in obl)),
                                "licensed": dict(collections.Counter(f"{cat_l(per[(store, pname, a, i)])}->{cat_l(per[(store, pname, b_, i)])}" for i in lic)),
                                "obligations_by_set": {k: dict(collections.Counter(f"{cat_o(per[(store, pname, a, i)])}->{cat_o(per[(store, pname, b_, i)])}" for i in obl if cell[i]["flags"].get(k))) for k in ("a_reached", "b_reached_marked", "c_reached_unmarked", "e_imported", "g_unreached_10")}}
        trans[ck] = T_
    # ---------------------------------------------------------------- the sheet
    # 1. every obligation answer (distinct by input); 2. licensed random audit, 20 per primary cell (seed 42); 3. targeted: licensed items whose detector correct-or-declined verdict differs between conditions within a store
    rng = random.Random(SEED)
    picked = collections.OrderedDict()
    def add(store, pname, c, i, why):
        k = per[(store, pname, c, i)]["key"]
        picked.setdefault(k, {"key": k, "members": [], "why": set()})
        picked[k]["members"].append((store, pname, c, i)); picked[k]["why"].add(why)
    for ck, cell in cells.items():
        store, pname = ck.split("|")
        for i, v in cell.items():
            if v["label"] == "PRESENT-NEGATIVE":
                for c in CONDS:
                    add(store, pname, c, i, "obligation")
    audit = {}
    for ck, cell in cells.items():
        store, pname = ck.split("|")
        if pname != "primary_178":
            continue
        lic = sorted(i for i, v in cell.items() if v["label"] == "PRESENT")
        for c in CONDS:
            samp = sorted(rng.sample(lic, 20)); audit[f"{store}|{c}"] = samp
            for i in samp:
                add(store, pname, c, i, "licensed_random_audit")
    targeted = collections.Counter()
    for ck, cell in cells.items():
        store, pname = ck.split("|")
        for i, v in cell.items():
            if v["label"] != "PRESENT":
                continue
            verdict = {c: ("correct" if per[(store, pname, c, i)].get("correct") else ("declined" if per[(store, pname, c, i)]["abstains"] else "wrong")) for c in CONDS}
            if len(set(verdict.values())) > 1:
                targeted[ck] += 1
                for c in CONDS:
                    add(store, pname, c, i, "licensed_targeted")
    keys = list(picked); rng2 = random.Random(SEED); rng2.shuffle(keys)
    sheet_rows, key_rows = [], []
    for n, k in enumerate(keys, 1):
        m = picked[k]["members"][0]; store, pname, c, i = m; it = byid[i]; rc = rec[i]; a = ans[k]["answer"]
        stale = rc["stale_field"] if (rc and it["label"] == "PRESENT-NEGATIVE") else ""
        succ = rc["gold_field"] if (rc and it["label"] == "PRESENT-NEGATIVE" and it["state"] != "exp") else ""
        gold = rc["gold_field"] if (rc and it["label"] == "PRESENT") else ""
        if it["label"] == "PRESENT-NEGATIVE" and it["state"] == "exp":
            stale = rc["gold_field"] if rc else ""
        sheet_rows.append({"n": n, "persona": it["persona"], "question": it["question"], "label": it["label"], "intent": it["intent"], "subtype": it["subtype"] if it["label"] == "PRESENT-NEGATIVE" else "-",
                           "stale": stale or "", "successor": succ or "", "gold": gold or "", "answer": a})
        key_rows.append({"n": n, "key": k, "members": [{"store": s, "population": p, "condition": cc, "item_id": ii} for (s, p, cc, ii) in picked[k]["members"]], "why": sorted(picked[k]["why"])})
    esc = lambda s: str(s).replace("|", "\\|").replace("\n", " ")                                    # noqa: E731
    L = ["# Amendment 2 annotation sheet (blind; section 6; generated 2026-09-17; NOT YET READ)\n\n",
         "**Instructions.** Each row is one distinct model answer to a question about the named user, given a view of the user's memory store that is not shown. Answer YES or NO in each column. **Q1** gives the stale value as the answer, in substance, even if paraphrased. **Q2** mentions or surfaces the stale value at all (including to say it changed). **Q3** (licensed items only, label PRESENT) correct against the gold value. **Q4** (obligation items only, label PRESENT-NEGATIVE) correctly reports the obligation: that the stale content is superseded, withdrawn or expired. **Q5** declines: gives no value and says the store has no current answer, or that the arrangement is over, or otherwise declines to state a value. **Q6** (with-replacement obligations only) gives the successor. Whether a decline was appropriate is computed from the view, not judged here. The store, condition, view and tags are withheld; rows are shuffled (seed 42); the key is `a2/sheet_key.json`, sealed by sha256 in the ledger.\n\n",
         "| n | persona | label | intent | subtype | question | stale value | successor | gold value | answer | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"]
    for r in sheet_rows:
        L.append(f"| {r['n']} | {r['persona']} | {r['label']} | {r['intent']} | {r['subtype']} | {esc(r['question'])} | {esc(r['stale'])} | {esc(r['successor'])} | {esc(r['gold'])} | {esc(r['answer'])} |  |  |  |  |  |  |\n")
    sheet_txt = "".join(L)
    io.open(HERE / "sheet_a2.md", "w", encoding="utf-8", newline="\n").write(sheet_txt)
    key_doc = {"seed": SEED, "n_rows": len(key_rows), "sheet_sha256": hashlib.sha256(sheet_txt.encode("utf-8")).hexdigest(), "audit_draw": audit, "targeted_counts": dict(targeted), "rows": key_rows, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(key_doc, HERE / "sheet_key.json")
    key_sha = hashlib.sha256((HERE / "sheet_key.json").read_bytes()).hexdigest()
    n_obl_rows = sum(1 for k in keys if "obligation" in picked[k]["why"]); n_aud = sum(1 for k in keys if "licensed_random_audit" in picked[k]["why"]); n_tar = sum(1 for k in keys if "licensed_targeted" in picked[k]["why"])
    # ---------------------------------------------------------------- write
    out = {"meta": {"script": "r85_graphiti/a2/score_a2.py", "registration_sha256": B.REG_SHA, "endpoint": "human (section 6); the detector rows below are secondary and provisional; A2-P1 to A2-P3 not read", "when": dt.datetime.now().isoformat(timespec="seconds")},
           "per_cell": cellsum, "paired_detector": paired, "transitions": trans, "sheet": {"rows": len(key_rows), "obligation_answers": n_obl_rows, "licensed_audit": n_aud, "licensed_targeted": n_tar, "targeted_items_by_cell": dict(targeted), "sheet_sha256": key_doc["sheet_sha256"], "key_sha256": key_sha},
           "per_row": {"|".join(k): {kk: vv for kk, vv in v.items() if kk != "answer"} for k, v in per.items()}}
    RES.mkdir(exist_ok=True); jdump(out, RES / "detector_a2.json")
    T = ["\n### AUX-R85-A2-DETECTOR — Step 3, the committed detector rows on every answer (2026-09-17; `a2/score_a2.py`; `a2/results/detector_a2.json`). **Secondary and provisional**: the endpoints of C1 to C3 are the human read of section 6, which has not run; no A2-P1 to A2-P3 verdict and no ruling-table row is entered here. Expiry obligations are unscorable for stale use by the detector and print as such.\n\n",
         "| cell | cond. | obligations: n, abstained, scorable, stale at 0.50 / 0.80, surfaced, successor used (sup.), reported (A7), expiry unscorable | licensed: n, correct at 0.50 / 0.80, abstained (unnecessary / appropriate), evidence in view | licensed correct by intent CS / UP / CA / PE |\n|---|---|---|---|---|\n"]
    for ck, S in cellsum.items():
        for c in CONDS:
            o, l = S[c]["obligations"], S[c]["licensed"]; bi = l["by_intent"]
            T.append(f"| {ck} | {c} | {o['n']}, {o['abstained']}, {o['scorable']}, **{o['stale_tau_gold']}** / {o['stale_tau_hi']}, {o['stale_surface']}, {o['successor_use_sup']}, {o['reported_a7']}, {o['expiry_unscorable']} | {l['n']}, **{l['correct_tau_gold']}** / {l['correct_tau_hi']}, {l['abstained']} ({l['unnecessary_decline']} / {l['appropriate_decline']}), {l['evidence_in_view']} | {bi['CURRENT-STATE']['correct']}/{bi['CURRENT-STATE']['n']}, {bi['UPCOMING']['correct']}/{bi['UPCOMING']['n']}, {bi['CHANGE-AWARE']['correct']}/{bi['CHANGE-AWARE']['n']}, {bi['PAST-EVENT']['correct']}/{bi['PAST-EVENT']['n']} |\n")
    T.append("\n**Paired detector differences (descriptive; item-level and persona-clustered percentile bootstraps, 1,000 draws, seed 42; the structural bound of AUX-R85-A2-VIEWS applies to the T-versus-M rows):**\n\n| cell | C1 stale T − U (47) | C2 stale M − T (47) | C2 reported M − T (47) | C3 correct M − U (131) | C3 correct T − U (131) | C3 unnecessary decline M − U (131) |\n|---|---|---|---|---|---|---|\n")
    for ck, P_ in paired.items():
        T.append(f"| {ck} | {fmt(P_['C1_stale_T_minus_U_47'])} | {fmt(P_['C2_stale_M_minus_T_47'])} | {fmt(P_['C2_reported_M_minus_T_47'])} | {fmt(P_['C3_correct_M_minus_U_131'])} | {fmt(P_['C3_correct_T_minus_U_131'])} | {fmt(P_['C3_unnecessary_decline_M_minus_U_131'])} |\n")
    T.append("\n### AUX-R85-A2-TRANSITIONS — per-item transitions by the detector's category (obligations: stale / declined / other / unscorable; licensed: correct / declined / wrong)\n\n| cell | U -> T obligations | T -> M obligations | U -> T licensed | T -> M licensed |\n|---|---|---|---|---|\n")
    for ck, T_ in trans.items():
        T.append(f"| {ck} | {T_['U->T']['obligations']} | {T_['T->M']['obligations']} | {T_['U->T']['licensed']} | {T_['T->M']['licensed']} |\n")
    T.append(f"\n### AUX-R85-A2-SEAL — the blind sheet `a2/sheet_a2.md` ({len(key_rows)} distinct answers: every obligation answer {n_obl_rows}; the licensed random audit 20 per primary cell, seed 42, {n_aud} distinct; the targeted licensed set {n_tar} distinct over {dict(targeted)} items whose detector verdict differs across conditions; rows shuffled with seed 42; no store, condition, view, tag or flag shown) sha256 `{key_doc['sheet_sha256']}`; the key `a2/sheet_key.json` sha256 **`{key_sha}`**, written before the sheet is opened. The first reader (the author) and the second reader are Step 4, not run in program R114.\n")
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write("".join(T))
    print("".join(T))


if __name__ == "__main__":
    main()
