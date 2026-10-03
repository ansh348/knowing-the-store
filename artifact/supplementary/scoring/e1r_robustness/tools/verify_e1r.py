"""Two-direction verifier for NUMBERS_E1R.md.

DIRECTION A -- every scientific figure printed in the ledger is re-derived here from the
committed raw artifacts (elicitation rows, item build, mechanism rows, serialized indexes,
cross-vendor JSONL) and compared to the printed value. Nothing is read back from this pass's
own results JSONs.

DIRECTION B -- every numeric token printed in the ledger is accounted for: matched to a
re-derived figure, to a declared published cross-reference, or to a declared structural
constant. Zero unaccounted is required to pass.
"""
from __future__ import annotations

import io
import os
import re
import sys
from pathlib import Path

import numpy as np

os.environ.setdefault("HF_HUB_OFFLINE", "1")
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common_e1r import (E1, POPULATIONS, XV, assemble, auroc, boot_cluster, boot_item,  # noqa
                        ece, jload, load_e1, lopo, reliability)

LEDGER = Path(__file__).resolve().parents[1] / "NUMBERS_E1R.md"
TOL = 5e-5

checks, failures, derived = [], [], set()


def chk(name, got, want, tol=TOL):
    ok = (got is not None and want is not None and abs(got - want) < tol)
    checks.append((name, got, want, ok))
    if not ok:
        failures.append((name, got, want))
    if got is not None:
        for dp in (1, 2, 3, 4):
            derived.add(norm(f"{got:.{dp}f}"))
            derived.add(norm(f"{abs(got):.{dp}f}"))
    return ok


def norm(t):
    t = str(t).replace(",", "").lstrip("+")
    neg = t.startswith("-")
    t = t.lstrip("-")
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return ("-" if neg and float(t or 0) else "") + (t or "0")


def main():
    items, blind, idxT, idxB = load_e1()

    # ---------------- DIRECTION A
    print("DIRECTION A -- re-derivation from committed raw artifacts")
    print("\n  [1] persona-clustered intervals, E1 calibration rows")
    LED_A = {
        "R-FOK-HARD": (588, 35, 40, 23, +0.2272, (+0.1552, +0.2996),
                       (+0.2148, +0.2441), 0),
        "R-FOK-FRB":  (307, 35, 40, 23, +0.2037, (+0.1259, +0.2767),
                       (+0.1876, +0.2199), 0),
        "R-FOK-EASY": (595, 463, 40, 40, +0.1914, (+0.1327, +0.2433),
                       (+0.1811, +0.2011), 0),
        "R-NOK-FRB":  (661, 104, 40, 28, +0.2393, (+0.1552, +0.3237),
                       (+0.2204, +0.2564), 0),
        "R-FOK-MEM0": (238, 94, 37, 36, -0.0969, (-0.1638, -0.0286),
                       (-0.1133, -0.0854), 0),
        "R-FOK-AMEM": (284, 126, 40, 39, -0.1065, (-0.1654, -0.0446),
                       (-0.1180, -0.0977), 0),
    }
    LED_ITEM = {   # item-level CI endpoints and clustered/item width ratio
        "R-FOK-HARD": (+0.1177, +0.3504, 0.62), "R-FOK-FRB": (+0.0935, +0.3191, 0.67),
        "R-FOK-EASY": (+0.1179, +0.2596, 0.78), "R-NOK-FRB": (+0.1801, +0.2949, 1.47),
        "R-FOK-MEM0": (-0.1686, -0.0250, 0.94), "R-FOK-AMEM": (-0.1726, -0.0403, 0.91),
    }
    for rid, spec in POPULATIONS.items():
        n, npos, npers, pospers, d, ccl, lop, sc = LED_A[rid]
        sub = [it for it in items if spec["filt"](it)]
        b, i, y, g, _ = assemble(sub, blind, idxT, judgment=spec["judgment"])
        chk(f"{rid} n", float(len(y)), float(n), 0.5)
        chk(f"{rid} n_pos", float(y.sum()), float(npos), 0.5)
        chk(f"{rid} n_personas", float(len(set(g.tolist()))), float(npers), 0.5)
        chk(f"{rid} pos_personas", float(len(set(g[y == 1].tolist()))), float(pospers), 0.5)
        chk(f"{rid} delta", auroc(i, y) - auroc(b, y), d)
        cl = boot_cluster(b, i, y, g)
        chk(f"{rid} cluster CI lo", cl["ci_lo"], ccl[0])
        chk(f"{rid} cluster CI hi", cl["ci_hi"], ccl[1])
        L = lopo(b, i, y, g)
        chk(f"{rid} LOPO min", L["min_delta"], lop[0])
        chk(f"{rid} LOPO max", L["max_delta"], lop[1])
        chk(f"{rid} LOPO sign changes", float(L["n_sign_changes"]), float(sc), 0.5)
        bi = boot_item(b, i, y)
        chk(f"{rid} item CI lo", bi["ci_lo"], LED_ITEM[rid][0])
        chk(f"{rid} item CI hi", bi["ci_hi"], LED_ITEM[rid][1])
        chk(f"{rid} width ratio", (cl["ci_hi"] - cl["ci_lo"]) / (bi["ci_hi"] - bi["ci_lo"]),
            LED_ITEM[rid][2], 5e-3)

    print("  [2] BELIEVED-index NOK")
    frb = [it for it in items if it["backend"] == "frbank"]
    for nm, idx, judgment, want, wci in (
            ("FOK TRUE", idxT, "fok", (0.5056, 0.7442, +0.2386), (+0.1856, +0.2877)),
            ("FOK BELIEVED", idxB, "fok", (0.5056, 0.7476, +0.2420), (+0.1891, +0.2879)),
            ("NOK TRUE", idxT, "nok", (0.4946, 0.7339, +0.2393), (+0.1801, +0.2949)),
            ("NOK BELIEVED", idxB, "nok", (0.4946, 0.5959, +0.1012), (+0.0458, +0.1543))):
        b, i, y, g, _ = assemble(frb, blind, idx, judgment=judgment)
        chk(f"believed {nm} n", float(len(y)), 661.0, 0.5)
        chk(f"believed {nm} blind", auroc(b, y), want[0])
        chk(f"believed {nm} indexed", auroc(i, y), want[1])
        chk(f"believed {nm} delta", auroc(i, y) - auroc(b, y), want[2])
        bci = boot_item(b, i, y)
        chk(f"believed {nm} item CI lo", bci["ci_lo"], wci[0])
        chk(f"believed {nm} item CI hi", bci["ci_hi"], wci[1])
    bt, it_, yt, gt, _ = assemble(frb, blind, idxT, judgment="nok")
    bb, ib, yb, gb, _ = assemble(frb, blind, idxB, judgment="nok")
    dt = auroc(it_, yt) - auroc(bt, yt)
    db = auroc(ib, yb) - auroc(bb, yb)
    chk("NOK believed retention (%)", 100.0 * db / dt, 42.3, 0.05)
    ft, fi, fy, _, _ = assemble(frb, blind, idxT, judgment="fok")
    fbt, fbi, fby, _, _ = assemble(frb, blind, idxB, judgment="fok")
    chk("FOK believed retention (%)",
        100.0 * (auroc(fbi, fby) - auroc(fbt, fby)) / (auroc(fi, fy) - auroc(ft, fy)),
        101.4, 0.05)
    cb = boot_cluster(bb, ib, yb, gb)
    chk("NOK BELIEVED cluster CI lo", cb["ci_lo"], +0.0217)
    chk("NOK BELIEVED cluster CI hi", cb["ci_hi"], +0.1744)
    ib_item = boot_item(bb, ib, yb)
    chk("NOK BELIEVED item CI lo", ib_item["ci_lo"], +0.0458)
    chk("NOK BELIEVED item CI hi", ib_item["ci_hi"], +0.1543)
    Lb = lopo(bb, ib, yb, gb)
    chk("NOK BELIEVED LOPO min", Lb["min_delta"], +0.0890)
    chk("NOK BELIEVED LOPO max", Lb["max_delta"], +0.1141)
    chk("NOK BELIEVED LOPO sign changes", float(Lb["n_sign_changes"]), 0.0, 0.5)

    print("  [3] ECE arms and paired differences")
    mech = jload(E1 / "mechanism_elicitation.json")
    mech_by = {}
    for r in mech:
        if r["status"] == "OK" and r.get("fok") is not None:
            mech_by.setdefault(r["arm"], {})[r["item_id"]] = r["fok"]
    MECH = {"counts jittered": "A1-counts-jittered",
            "counts coarsened": "A2-counts-coarsened", "names only": "A3-names-only"}
    base = []
    for it in [x for x in items if x["tier"] == "hard"]:
        q, tag = it["question"], it["item_id"]
        if q not in blind or tag not in idxT:
            continue
        if blind[q].get("fok") is None or idxT[tag].get("fok") is None:
            continue
        if not all(tag in mech_by.get(a, {}) for a in MECH.values()):
            continue
        lab = it.get("label", it["label_pre"])
        base.append({"y": 0 if lab == "ABSENT" else 1, "persona": it["persona"],
                     "blind": blind[q]["fok"], "intact": idxT[tag]["fok"],
                     **{k: mech_by[a][tag] for k, a in MECH.items()}})
    y = np.array([r["y"] for r in base], int)
    arms = {k: np.array([r[k] for r in base], float)
            for k in ("blind", "intact", "counts jittered", "counts coarsened", "names only")}
    chk("ECE population n", float(len(base)), 588.0, 0.5)
    chk("ECE population n_pos", float(y.sum()), 35.0, 0.5)
    chk("ECE base rate", float(y.mean()), 0.0595, 5e-4)
    WANT = {"blind": (0.5258, 0.1596), "intact": (0.7530, 0.1741),
            "counts jittered": (0.7697, 0.1720), "counts coarsened": (0.7625, 0.1668),
            "names only": (0.8516, 0.0583)}
    from run_ece import boot_ece
    ECE_CI = {  # (item lo, item hi, cluster lo, cluster hi)
        "blind": (0.1349, 0.1826, 0.1378, 0.1823),
        "intact": (0.1529, 0.1954, 0.1556, 0.1939),
        "counts jittered": (0.1509, 0.1935, 0.1527, 0.1928),
        "counts coarsened": (0.1453, 0.1882, 0.1473, 0.1881),
        "names only": (0.0418, 0.0772, 0.0410, 0.0795),
    }
    gg = np.array([r["persona"] for r in base])
    for k, (wa, we) in WANT.items():
        chk(f"ECE {k} auroc", auroc(arms[k], y), wa)
        chk(f"ECE {k} ece", ece(arms[k], y), we)
        ci_i = boot_ece(arms[k], y, gg, False)
        ci_c = boot_ece(arms[k], y, gg, True)
        w = ECE_CI[k]
        chk(f"ECE {k} CI item lo", ci_i["ci_lo"], w[0])
        chk(f"ECE {k} CI item hi", ci_i["ci_hi"], w[1])
        chk(f"ECE {k} CI clus lo", ci_c["ci_lo"], w[2])
        chk(f"ECE {k} CI clus hi", ci_c["ci_hi"], w[3])
    from run_ece import boot_ece_diff
    for k, wd, wlo, whi in (("intact", +0.0145, -0.0037, +0.0345),
                            ("counts jittered", +0.0124, -0.0063, +0.0317),
                            ("counts coarsened", +0.0072, -0.0113, +0.0256),
                            ("names only", -0.1013, -0.1171, -0.0815)):
        chk(f"dECE {k} vs blind", ece(arms[k], y) - ece(arms["blind"], y), wd)
        dd = boot_ece_diff(arms[k], arms["blind"], y, gg, False)
        chk(f"dECE {k} CI lo", dd["ci_lo"], wlo)
        chk(f"dECE {k} CI hi", dd["ci_hi"], whi)

    print("  [4] baselines -- monitor side and structural facts")
    hard_joined = [x for x in items if x["tier"] == "hard"
                   and x["question"] in blind and x["item_id"] in idxT
                   and blind[x["question"]].get("fok") is not None
                   and idxT[x["item_id"]].get("fok") is not None]
    isfr = np.array([1.0 if x["backend"] == "frbank" else 0.0 for x in hard_joined], float)
    yy = np.array([0 if x.get("label", x["label_pre"]) == "ABSENT" else 1
                   for x in hard_joined], int)
    chk("backend-indicator AUROC, pooled hard", auroc(isfr, yy), 0.7541)
    for rid, prov, idx, judgment, want in (
            ("R-FOK-FRB", "TRUE", idxT, "fok", 0.7003),
            ("R-FOK-FRB", "BELIEVED", idxB, "fok", 0.7005),
            ("R-NOK-FRB", "TRUE", idxT, "nok", 0.7339),
            ("R-NOK-FRB", "BELIEVED", idxB, "nok", 0.5959)):
        sub = [it for it in items if POPULATIONS[rid]["filt"](it)]
        b, i, y2, _, _ = assemble(sub, blind, idx, judgment=judgment)
        chk(f"monitor {rid} {prov}", auroc(i, y2), want)

    print("  [5] cross-vendor matched cell, clustered endpoints")
    sys.path.insert(0, str(XV / "tools"))
    import score_e1xv
    cellm = jload(XV / "manifests" / "cell_84.json")
    cell = {x["item_id"]: x for x in cellm["items"]}
    XVW = {"claude-opus-5": {"FOK": (+0.1213, -0.0136, +0.2368),
                             "NOK": (+0.1528, +0.0923, +0.2392)},
           "claude-haiku-4-5-20251001": {"FOK": (+0.4151, +0.1339, +0.6129),
                                         "NOK": (+0.4511, +0.2925, +0.5981)},
           "kimi-k3": {"FOK": (+0.0571, -0.1235, +0.2282),
                       "NOK": (+0.2605, +0.1653, +0.3933)}}
    from run_clustered_ladder import arms_from_mini, arms_from_prescored, score as cellscore
    OAI = {"mini": (arms_from_mini(cell), {
               "FOK": (+0.2602, +0.0851, +0.4213, +0.0913, +0.3912),
               "NOK": (+0.2139, +0.1242, +0.3070, +0.1093, +0.3245)}),
           "luna": (arms_from_prescored(E1 / "ladder_gpt-5.6-luna.json", cell), {
               "FOK": (+0.1682, +0.0340, +0.3033, +0.0367, +0.3001),
               "NOK": (+0.2940, +0.1696, +0.4172, +0.1984, +0.4051)}),
           "sol": (arms_from_prescored(E1 / "redraw_frontier.json", cell), {
               "FOK": (+0.0364, -0.0930, +0.1600, -0.1095, +0.1609),
               "NOK": (+0.3298, +0.1994, +0.4470, +0.2117, +0.4500)})}
    for mname, (amap, want) in OAI.items():
        for J, (wd, ilo, ihi, clo, chi) in want.items():
            b, i, yv, g = cellscore(amap, cell, J.lower())
            chk(f"cell {mname} {J} delta", auroc(i, yv) - auroc(b, yv), wd)
            bi2 = boot_item(b, i, yv)
            chk(f"cell {mname} {J} item lo", bi2["ci_lo"], ilo)
            chk(f"cell {mname} {J} item hi", bi2["ci_hi"], ihi)
            cl2 = boot_cluster(b, i, yv, g)
            chk(f"cell {mname} {J} clus lo", cl2["ci_lo"], clo)
            chk(f"cell {mname} {J} clus hi", cl2["ci_hi"], chi)

    for mid, want in XVW.items():
        coll, meta, _ = score_e1xv.collapse(score_e1xv.load(mid))
        for J, (wd, wlo, whi) in want.items():
            j = J.lower()
            tags = sorted({t for (t, a) in coll
                           if (t, "BLIND") in coll and (t, "INDEXED-TRUE") in coll
                           and coll[(t, "BLIND")][j] is not None
                           and coll[(t, "INDEXED-TRUE")][j] is not None and t in cell})
            b = np.array([coll[(t, "BLIND")][j] for t in tags], float)
            i = np.array([coll[(t, "INDEXED-TRUE")][j] for t in tags], float)
            yv = np.array([cell[t]["y_fok" if j == "fok" else "y_nok"] for t in tags], int)
            g = np.array([t.split(":")[1] for t in tags])
            chk(f"XV {mid} {J} delta", auroc(i, yv) - auroc(b, yv), wd)
            cl = boot_cluster(b, i, yv, g)
            chk(f"XV {mid} {J} cluster lo", cl["ci_lo"], wlo)
            chk(f"XV {mid} {J} cluster hi", cl["ci_hi"], whi)

    print("  [6] baseline table, NB-3 ablation, reliability, cluster-validation")
    from run_baselines import build, supervised, embed_scores
    from diag_baselines import oof_text
    from validate_clustered import cluster_jackknife, icc_of_contribution
    from scipy.stats import spearmanr

    BASE_W = {
        ("R-FOK-FRB", "TRUE"):   (0.5194, 0.5228, 0.6080, 0.6186, 0.5048, 0.7003, 0.4966),
        ("R-FOK-FRB", "BELIEVED"): (0.5194, 0.4630, 0.6080, 0.6186, 0.5419, 0.7005, 0.4966),
        ("R-NOK-FRB", "TRUE"):   (0.5514, 0.5834, 0.5383, 0.5974, 0.4780, 0.7339, 0.4946),
        ("R-NOK-FRB", "BELIEVED"): (0.4987, 0.5459, 0.5383, 0.5974, 0.4715, 0.5959, 0.4946),
        ("R-FOK-MEM0", "TRUE"):  (0.4818, 0.4923, 0.5000, 0.5000, 0.4464, 0.4777, 0.5746),
        ("R-FOK-MEM0", "BELIEVED"): (0.4818, 0.5372, 0.5000, 0.5000, 0.4621, 0.5741, 0.5746),
        ("R-FOK-AMEM", "TRUE"):  (0.5226, 0.4184, 0.5000, 0.5000, 0.5163, 0.4526, 0.5591),
        ("R-FOK-AMEM", "BELIEVED"): (0.5226, 0.4452, 0.5000, 0.5000, 0.5098, 0.5278, 0.5591),
        ("R-FOK-HARD", "TRUE"):  (0.4513, 0.7246, 0.6983, 0.8124, 0.6827, 0.7530, 0.5258),
        ("R-FOK-HARD", "BELIEVED"): (0.4513, 0.7367, 0.6983, 0.8124, 0.6909, 0.7955, 0.5258),
    }
    MONBEST = {
        ("R-FOK-FRB", "TRUE"): +0.0817, ("R-FOK-FRB", "BELIEVED"): +0.0819,
        ("R-NOK-FRB", "TRUE"): +0.1365, ("R-NOK-FRB", "BELIEVED"): -0.0015,
        ("R-FOK-MEM0", "TRUE"): -0.0223, ("R-FOK-MEM0", "BELIEVED"): +0.0369,
        ("R-FOK-AMEM", "TRUE"): -0.0700, ("R-FOK-AMEM", "BELIEVED"): +0.0052,
        ("R-FOK-HARD", "TRUE"): -0.0594, ("R-FOK-HARD", "BELIEVED"): -0.0169,
    }
    NB3_W = {
        ("R-FOK-HARD", "TRUE"): (0.7637, 0.9598), ("R-FOK-HARD", "BELIEVED"): (0.7602, 0.9598),
        ("R-FOK-FRB", "TRUE"): (0.8070, 0.9164), ("R-FOK-FRB", "BELIEVED"): (0.8333, 0.9164),
        ("R-NOK-FRB", "TRUE"): (0.7221, 0.8707), ("R-NOK-FRB", "BELIEVED"): (0.7024, 0.8707),
        ("R-FOK-MEM0", "TRUE"): (0.9625, 0.9667), ("R-FOK-MEM0", "BELIEVED"): (0.9622, 0.9667),
        ("R-FOK-AMEM", "TRUE"): (0.9512, 0.9539), ("R-FOK-AMEM", "BELIEVED"): (0.9528, 0.9539),
    }
    for (rid, prov), w in BASE_W.items():
        idx = idxT if prov == "TRUE" else idxB
        spec = POPULATIONS[rid]
        sub = [it for it in items if spec["filt"](it)]
        rows = build(sub, blind, idx, spec["judgment"], prov)
        yv = np.array([r["y"] for r in rows], int)
        gv = np.array([r["persona"] for r in rows])
        keys = sorted(rows[0]["feat"].keys())
        Xn = np.array([[r["feat"][k] for k in keys] for r in rows], float)
        chk(f"NB-1 {rid} {prov}", auroc([r["nb1"] for r in rows], yv), w[0])
        chk(f"NB-2 {rid} {prov}", auroc(supervised(Xn, yv, gv, "nb2"), yv), w[1])
        chk(f"NB-4 {rid} {prov}", auroc([r["nb4"] for r in rows], yv), w[2])
        chk(f"NB-5 {rid} {prov}", auroc(embed_scores(rows), yv), w[3])
        chk(f"NB-3idx {rid} {prov}", auroc(oof_text([r["text"].split("\n\nQUESTION: ")[0]
                                                     for r in rows], yv, gv), yv), w[4])
        chk(f"monitor idx {rid} {prov}", auroc([r["monitor"] for r in rows], yv), w[5])
        chk(f"monitor blind {rid} {prov}", auroc([r["monitor_blind"] for r in rows], yv), w[6])
        best = max(w[0], w[1], w[2], w[3], w[4])
        chk(f"monitor-best {rid} {prov}", w[5] - best, MONBEST[(rid, prov)], 5e-4)
        nb3w = NB3_W[(rid, prov)]
        chk(f"NB-3 idx+q {rid} {prov}", auroc(oof_text([r["text"] for r in rows], yv, gv), yv),
            nb3w[0])
        chk(f"NB-3 q-only {rid} {prov}",
            auroc(oof_text([r["question"] for r in rows], yv, gv), yv), nb3w[1])

    print("  [4b] NB-6 -- the superseded-names matcher (R81, ledger section 11)")
    from run_nb6 import (build as nb6_build, emb_scores, lex_scores, matched84,  # noqa: E402
                         name_lists as nb6_names)

    # (lex, emb, monitor - best, mean names per item); field follows the judgment
    # monitor - best AFTER NB-6 enters. On BELIEVED, NB-5 (0.5974) still outranks NB-6
    # (0.5858), so that row's delta is unchanged from the committed table.
    MONBEST_AFTER_NB6 = {
        ("R-NOK-FRB", "TRUE"): -0.0145,
        ("R-NOK-FRB", "BELIEVED"): -0.0015,
    }
    NB6_W = {
        ("R-NOK-FRB", "TRUE"):     (0.5738, 0.7484, -0.0145, 1.75),
        ("R-NOK-FRB", "BELIEVED"): (0.4718, 0.5858, +0.0101, 15.04),
        ("R-FOK-FRB", "TRUE"):     (0.6080, 0.6186, +0.0817, 124.90),
        ("R-FOK-FRB", "BELIEVED"): (0.6080, 0.6186, +0.0819, 124.90),
    }
    for (rid, prov), w in NB6_W.items():
        idx = idxT if prov == "TRUE" else idxB
        spec = POPULATIONS[rid]
        sub = [it for it in items if spec["filt"](it)]
        rows = nb6_build(sub, blind, idx, spec["judgment"], prov)
        yv = np.array([r["y"] for r in rows], int)
        field = "sup" if spec["judgment"] == "nok" else "all"
        lex, emb = auroc(lex_scores(rows, field), yv), auroc(emb_scores(rows, field), yv)
        chk(f"NB-6 lexical {rid} {prov}", lex, w[0])
        chk(f"NB-6 embedding {rid} {prov}", emb, w[1])
        chk(f"NB-6 names/item {rid} {prov}",
            float(np.mean([len(r[field]) for r in rows])), w[3], 5e-3)
        mon = auroc([r["monitor"] for r in rows], yv)
        if spec["judgment"] == "nok":
            # the ledger's "monitor - NB-6" column, whether or not NB-6 takes `best`
            chk(f"NB-6 monitor-NB6 {rid} {prov}", mon - max(lex, emb), w[2], 5e-4)
            # and the post-NB-6 `best`, which NB-6 takes only where it is the strongest
            best_after = max(max(BASE_W[(rid, prov)][:5]), lex, emb)
            chk(f"NB-6 monitor-best after {rid} {prov}", mon - best_after,
                MONBEST_AFTER_NB6[(rid, prov)], 5e-4)
        else:
            # coverage rows: NB-6 prints no cell, so `best` and the delta stay as committed
            chk(f"NB-6 coverage delta unchanged {rid} {prov}",
                mon - max(BASE_W[(rid, prov)][:5]), w[2], 5e-4)
            # the declared identity: FOK-6 IS NB-4 and NB-5 (D-E1R-7)
            chk(f"NB-6 reproduces NB-4 {rid} {prov}", lex, BASE_W[(rid, prov)][2])
            chk(f"NB-6 reproduces NB-5 {rid} {prov}", emb, BASE_W[(rid, prov)][3])

    print("  [4c] NB-6 composition census (R81 post hoc, ledger section 12)")
    from nb6_composition import AV_STATE, slot_map, named as _named  # noqa: E402
    _slots = slot_map()
    # (n, NB-6 embedding AUROC, monitor AUROC) per lifecycle state of the positive, TRUE
    COMP_T = {"superseded": (63, 0.9534, 0.8572),
              "expired":    (15, 0.4823, 0.5110),
              "retracted":  (26, 0.4053, 0.5638)}
    COMP_B = {"superseded": 0.6583, "expired": 0.5926, "retracted": 0.4062}
    COMP_B_MON = {"superseded": 0.7010, "expired": 0.4983, "retracted": 0.3975}
    for prov, idx in (("TRUE", idxT), ("BELIEVED", idxB)):
        sub = [it for it in items if POPULATIONS["R-NOK-FRB"]["filt"](it)]
        crows = []
        for it in sub:
            q, tag = it["question"], it["item_id"]
            if q not in blind or tag not in idx:
                continue
            if blind[q].get("nok") is None or idx[tag].get("nok") is None:
                continue
            ypn = 1 if it.get("label", it["label_pre"]) == "PRESENT-NEGATIVE" else 0
            sup, alln = nb6_names(it, prov)
            crows.append({"y": ypn, "question": q, "sup": sup, "all": alln,
                          "av": it.get("attack_vector"),
                          "named": _named(it, prov, _slots)[0] if ypn == 1 else False,
                          "monitor": idx[tag].get("nok")})
        cemb = emb_scores(crows, "sup")
        negi = [i for i, r in enumerate(crows) if r["y"] == 0]
        npn = sum(1 for r in crows if r["y"] == 1)
        chk(f"composition PN total {prov}", float(npn), 104.0, 0.5)
        _nnamed = sum(1 for r in crows if r["y"] == 1 and r["named"])
        chk(f"composition PN named {prov}", float(_nnamed),
            7.0 if prov == "TRUE" else 13.0, 0.5)
        chk(f"composition PN named rate {prov}", _nnamed / npn,
            0.067 if prov == "TRUE" else 0.125, 5e-4)
        if prov == "TRUE":
            # per-variant naming counts, to show the rate is not an ablation artifact
            _byvar = {}
            for _it in sub:
                if _it.get("label", _it["label_pre"]) != "PRESENT-NEGATIVE":
                    continue
                _s = _byvar.setdefault(_it["variant"], [0, 0])
                _s[1] += 1
                _s[0] += int(_named(_it, prov, _slots)[0])
            for _v, _w in (("FULL", (3, 47)), ("SLOT-ABLATED", (3, 35)),
                           ("CAT-ABLATED", (1, 22))):
                chk(f"composition named {_v}", float(_byvar[_v][0]), float(_w[0]), 0.5)
                chk(f"composition n PN {_v}", float(_byvar[_v][1]), float(_w[1]), 0.5)
        for st in ("superseded", "expired", "retracted"):
            sel = [i for i, r in enumerate(crows)
                   if r["y"] == 1 and AV_STATE.get(r["av"]) == st]
            keep = sorted(sel + negi)
            yy = np.array([crows[i]["y"] for i in keep], int)
            if prov == "TRUE":
                wn, wemb, wmon = COMP_T[st]
                chk(f"composition n PN {st} {prov}", float(len(sel)), float(wn), 0.5)
                chk(f"composition NB-6 PN {st} {prov}",
                    auroc([cemb[i] for i in keep], yy), wemb)
                chk(f"composition monitor PN {st} {prov}",
                    auroc([crows[i]["monitor"] for i in keep], yy), wmon)
            else:
                chk(f"composition NB-6 PN {st} {prov}",
                    auroc([cemb[i] for i in keep], yy), COMP_B[st])
                chk(f"composition monitor PN {st} {prov}",
                    auroc([crows[i]["monitor"] for i in keep], yy), COMP_B_MON[st])
    # matched-84 composition and the two supersession shares
    _man = jload(XV / "manifests" / "cell_84.json")
    _byid = {i["item_id"]: i for i in items}
    _m84pn = [i for i in _man["items"] if i["y_nok"] == 1]
    _m84sup = sum(1 for i in _m84pn
                  if AV_STATE.get(_byid.get(i["item_id"], {}).get("attack_vector")) == "superseded")
    chk("composition matched-84 PN total", float(len(_m84pn)), 40.0, 0.5)
    chk("composition matched-84 superseded", float(_m84sup), 19.0, 0.5)
    chk("composition matched-84 share", _m84sup / len(_m84pn), 0.475, 5e-4)
    chk("composition n=661 share", 63.0 / 104.0, 0.606, 5e-4)

    print("  [4d] per-state intervals and the frontier split (R81 Phase 1c, section 13)")
    from nb6_perstate import paired_ci, single_ci                    # noqa: E402
    from x4_score import load_lane                                   # noqa: E402

    _prows = []
    for _it in [i for i in items if POPULATIONS["R-NOK-FRB"]["filt"](i)]:
        _q, _tag = _it["question"], _it["item_id"]
        if _q not in blind or _tag not in idxT:
            continue
        if blind[_q].get("nok") is None or idxT[_tag].get("nok") is None:
            continue
        _sup, _alln = nb6_names(_it, "TRUE")
        _prows.append({"y": 1 if _it.get("label", _it["label_pre"]) == "PRESENT-NEGATIVE" else 0,
                       "question": _q, "sup": _sup, "all": _alln,
                       "av": _it.get("attack_vector"), "item_id": _tag,
                       "mini": idxT[_tag].get("nok")})
    _match = emb_scores(_prows, "sup")
    _mini = [r["mini"] for r in _prows]
    _neg = [i for i, r in enumerate(_prows) if r["y"] == 0]
    _pos = {st: [i for i, r in enumerate(_prows)
                 if r["y"] == 1 and AV_STATE.get(r["av"]) == st]
            for st in ("superseded", "expired", "retracted")}
    chk("perstate n_neg", float(len(_neg)), 557.0, 0.5)

    # (matcher lo, matcher hi, monitor lo, monitor hi, diff, diff lo, diff hi)
    I2_W = {
        "superseded": (0.9281, 0.9760, 0.7946, 0.9142, -0.0962, -0.1520, -0.0495),
        "expired":    (0.3626, 0.6110, 0.3971, 0.6383, +0.0287, -0.1795, +0.2212),
        "retracted":  (0.2812, 0.5320, 0.4629, 0.6760, +0.1585, +0.0002, +0.3341),
    }
    for st, w in I2_W.items():
        mc = single_ci(_match, _pos[st], _neg)
        mo = single_ci(_mini, _pos[st], _neg)
        pd = paired_ci(_mini, _match, _pos[st], _neg)
        chk(f"perstate matcher lo {st}", mc["ci_lo"], w[0])
        chk(f"perstate matcher hi {st}", mc["ci_hi"], w[1])
        chk(f"perstate monitor lo {st}", mo["ci_lo"], w[2])
        chk(f"perstate monitor hi {st}", mo["ci_hi"], w[3])
        chk(f"perstate diff {st}", pd["delta"], w[4], 5e-4)
        chk(f"perstate diff lo {st}", pd["ci_lo"], w[5])
        chk(f"perstate diff hi {st}", pd["ci_hi"], w[6])

    # twelve frontier rows: (auroc, lo, hi, delta, dlo, dhi)
    I3_W = {
        ("LUNA", "superseded"): (0.8933, 0.8495, 0.9324, -0.0601, -0.1021, -0.0246),
        ("LUNA", "expired"):    (0.8248, 0.7825, 0.8656, +0.3425, +0.2093, +0.4636),
        ("LUNA", "retracted"):  (0.6323, 0.5255, 0.7361, +0.2270, +0.0836, +0.3679),
        ("OP5", "superseded"):  (0.8690, 0.8322, 0.9026, -0.0845, -0.1226, -0.0486),
        ("OP5", "expired"):     (0.8881, 0.8576, 0.9153, +0.4058, +0.2751, +0.5264),
        ("OP5", "retracted"):   (0.7129, 0.6526, 0.7736, +0.3077, +0.1772, +0.4386),
        ("H45", "superseded"):  (0.8897, 0.8382, 0.9306, -0.0637, -0.1166, -0.0159),
        ("H45", "expired"):     (0.6874, 0.5720, 0.7962, +0.2051, +0.0002, +0.3893),
        ("H45", "retracted"):   (0.7317, 0.6406, 0.8222, +0.3264, +0.1956, +0.4663),
    }
    _byid = {r["item_id"]: i for i, r in enumerate(_prows)}
    for _code in ("LUNA", "OP5", "H45"):
        _coll, _ = load_lane(_code)
        _lane = np.full(len(_prows), np.nan, float)
        for (_iid, _arm), _v in _coll.items():
            if _arm == "INDEXED-TRUE" and _iid in _byid and _v.get("nok") is not None:
                _lane[_byid[_iid]] = _v["nok"]
        for _st in ("superseded", "expired", "retracted"):
            w = I3_W[(_code, _st)]
            _pi = [i for i in _pos[_st] if not np.isnan(_lane[i])]
            _ni = [i for i in _neg if not np.isnan(_lane[i])]
            _lc = single_ci(_lane, _pi, _ni)
            _pd = paired_ci(_lane, _match, _pi, _ni)
            chk(f"frontier {_code} {_st} auroc", _lc["auroc"], w[0])
            chk(f"frontier {_code} {_st} lo", _lc["ci_lo"], w[1])
            chk(f"frontier {_code} {_st} hi", _lc["ci_hi"], w[2])
            chk(f"frontier {_code} {_st} delta", _pd["delta"], w[3], 5e-4)
            chk(f"frontier {_code} {_st} dlo", _pd["ci_lo"], w[4])
            chk(f"frontier {_code} {_st} dhi", _pd["ci_hi"], w[5])

    print("  [4e] attribution gate and clustered per-state rows (R81 Phase 1d, section 14)")
    from nb6_attribution import clustered_paired_ci                  # noqa: E402

    # (blind, indexed, delta, ci_lo, ci_hi) per lane per state, indexed minus blind
    ATTRIB_W = {
        ("LUNA", "superseded"): (0.3693, 0.8933, +0.5240, +0.4544, +0.5970),
        ("LUNA", "expired"): (0.7197, 0.8248, +0.1051, +0.0056, +0.2163),
        ("LUNA", "retracted"): (0.4881, 0.6323, +0.1442, -0.0077, +0.3041),
        ("OP5", "superseded"): (0.5387, 0.8690, +0.3303, +0.2814, +0.3831),
        ("OP5", "expired"): (0.8709, 0.8881, +0.0172, -0.0057, +0.0411),
        ("OP5", "retracted"): (0.7641, 0.7129, -0.0511, -0.0987, +0.0009),
        ("H45", "superseded"): (0.3264, 0.8897, +0.5634, +0.4936, +0.6292),
        ("H45", "expired"): (0.6542, 0.6874, +0.0332, -0.1263, +0.1773),
        ("H45", "retracted"): (0.4918, 0.7317, +0.2399, +0.1301, +0.3577),
    }
    _pers = []
    for _it in [i for i in items if POPULATIONS["R-NOK-FRB"]["filt"](i)]:
        _q, _tag = _it["question"], _it["item_id"]
        if _q in blind and _tag in idxT and blind[_q].get("nok") is not None \
                and idxT[_tag].get("nok") is not None:
            _pers.append(_it["persona"])
    assert len(_pers) == len(_prows)

    for _code in ("LUNA", "OP5", "H45"):
        _coll, _ = load_lane(_code)
        _ind = np.full(len(_prows), np.nan, float)
        _bl = np.full(len(_prows), np.nan, float)
        for (_iid, _arm), _v in _coll.items():
            if _iid not in _byid or _v.get("nok") is None:
                continue
            if _arm == "INDEXED-TRUE":
                _ind[_byid[_iid]] = _v["nok"]
            elif _arm == "BLIND":
                _bl[_byid[_iid]] = _v["nok"]
        _ok = ~(np.isnan(_ind) | np.isnan(_bl))
        for _st in ("superseded", "expired", "retracted"):
            w = ATTRIB_W[(_code, _st)]
            _pi = [i for i in _pos[_st] if _ok[i]]
            _ni = [i for i in _neg if _ok[i]]
            _sub = np.concatenate([np.asarray(_pi), np.asarray(_ni)])
            _yy = np.zeros(len(_prows), int)
            _yy[np.asarray(_pi)] = 1
            chk(f"attrib {_code} {_st} blind", auroc(_bl[_sub], _yy[_sub]), w[0])
            chk(f"attrib {_code} {_st} indexed", auroc(_ind[_sub], _yy[_sub]), w[1])
            _pd = paired_ci(_ind, _bl, _pi, _ni)
            chk(f"attrib {_code} {_st} delta", _pd["delta"], w[2], 5e-4)
            chk(f"attrib {_code} {_st} lo", _pd["ci_lo"], w[3])
            chk(f"attrib {_code} {_st} hi", _pd["ci_hi"], w[4])

    CLUST_W = {
        "superseded": (-0.1712, -0.0307),
        "expired": (-0.3115, +0.4296),
        "retracted": (-0.0560, +0.4152),
    }
    for _st, w in CLUST_W.items():
        _c = clustered_paired_ci(_mini, _match, _pos[_st], _neg, _pers)
        chk(f"clustered mini {_st} lo", _c["ci_lo"], w[0])
        chk(f"clustered mini {_st} hi", _c["ci_hi"], w[1])
    chk("clustered n_personas", float(_c["n_personas"]), 40.0, 0.5)

    M84_W = {"TRUE": (0.5375, 0.6023), "BELIEVED": (0.4815, 0.5563)}
    m84 = matched84()
    for prov, (wlex, wemb) in M84_W.items():
        chk(f"NB-6 matched-84 lexical {prov}", m84[prov]["nb6_lexical"], wlex)
        chk(f"NB-6 matched-84 embedding {prov}", m84[prov]["nb6_embedding"], wemb)

    VAL_W = {"R-FOK-HARD": (0.0386, 0.95, +0.0129), "R-FOK-FRB": (0.0404, 0.95, -0.0238),
             "R-FOK-EASY": (0.0284, 0.99, +0.0870), "R-NOK-FRB": (0.0437, 0.98, +0.0769),
             "R-FOK-MEM0": (0.0363, 0.95, -0.0340), "R-FOK-AMEM": (0.0311, 0.99, -0.0544)}
    for rid, (wse, wratio, wicc) in VAL_W.items():
        spec = POPULATIONS[rid]
        sub = [it for it in items if spec["filt"](it)]
        b, i, yv, gv, _ = assemble(sub, blind, idxT, judgment=spec["judgment"])
        se, _K = cluster_jackknife(b, i, yv, gv)
        bc = boot_cluster(b, i, yv, gv)
        chk(f"jackknife SE {rid}", se, wse)
        chk(f"clusterboot/jackknife {rid}", (bc["ci_hi"] - bc["ci_lo"]) / (2 * 1.96 * se),
            wratio, 5e-3)
        chk(f"ICC {rid}", icc_of_contribution(b, i, yv, gv)[0], wicc)

    REL_W = {"blind": (0.1026, 0.8696, 0.219, 0.060, -0.700),
             "intact": (0.9000, 0.0374, 0.217, 0.056, -0.440),
             "names only": (1.0000, 0.0000, 0.116, 0.058, -0.300)}
    for arm, (wrho, wp, wpred, wobs, wgap) in REL_W.items():
        rel = reliability(arms[arm], y)
        big = [bn for bn in rel if bn["n"] >= 10]
        pred = np.array([bn["mean_pred"] for bn in big])
        obs = np.array([bn["obs_freq"] for bn in big])
        ns = np.array([bn["n"] for bn in big], float)
        rho, pv = spearmanr(pred, obs)
        chk(f"reliability {arm} n_bins", float(len(big)), 5.0, 0.5)
        chk(f"reliability {arm} spearman", float(rho), wrho, 5e-4)
        chk(f"reliability {arm} p", float(pv), wp, 5e-4)
        chk(f"reliability {arm} mean pred", float(np.average(pred, weights=ns)), wpred, 5e-4)
        chk(f"reliability {arm} obs", float(np.average(obs, weights=ns)), wobs, 5e-4)
        chk(f"reliability {arm} worst gap", float(np.min(obs - pred)), wgap, 5e-4)
    chk("overconfidence ratio, intact", 0.217 / 0.056, 3.9, 0.05)

    for nm, got, want, ok in checks:
        print(f"  {'ok ' if ok else 'FAIL'} {nm:44s} {got:>12.4f} vs {want:>10.4f}")

    # ---------------- DIRECTION B
    print("\nDIRECTION B -- every ledger numeral accounted for")
    text = io.open(LEDGER, encoding="utf-8").read()
    text = text.replace("−", "-").replace("×", "x")  # unicode minus, times
    text = re.sub(r"`[^`]*`", " ", text)          # code spans: keys, paths, commits
    text = re.sub(r"^#.*$", " ", text, flags=re.M)
    # identifier classes: NB-1, R-FOK-HARD, D-E1R-4, XV-5, QP-2, D94, A4, B5, P3, §7
    for pat in (r"NB-\d(?:-idx)?", r"NB\d-\d", r"[FN]OK-\d", r"D-R\d+-\d+", r"\bR\d{2}\b", r"ADDENDUM_R\d+",
                r"matched-\d+", r"SLOT-ABLATED", r"CAT-ABLATED",
                r"R-[A-Z0-9]+(?:-[A-Z0-9]+)*", r"D-E1R-\d",
                r"\bXV-\d", r"\bQP-\d", r"\bD\d{1,3}\b", r"\b[ABC]\d\b", r"\bP\d\b",
                r"§\s*\d+", r"MiniLM-L\d+-v\d", r"all-MiniLM", r"Haiku\s+4\.5",
                r"Opus\s+5", r"K3", r"gpt-\S+"):
        text = re.sub(pat, " ", text)
    PUBLISHED = {  # printed for comparison, sourced from the manuscript/central ledger
        "0.2272", "0.2037", "0.2393", "-0.0969", "-0.1065", "0.1914", "0.1177", "0.3504",
        "0.0935", "0.3191", "0.1801", "0.2949", "-0.169", "-0.025", "-0.173", "-0.04",
        "0.5258", "0.753", "0.7697", "0.7625", "0.8516", "0.1596", "0.1741", "0.172",
        "0.1668", "0.0583", "0.2602", "0.2139", "0.1682", "0.294", "0.0364", "0.3298",
        "0.1213", "0.1528", "0.4151", "0.4511", "0.0571", "0.2605", "0.0851", "0.4213",
        "0.1242", "0.307", "0.034", "0.3033", "0.1696", "0.4172", "-0.093", "0.16",
        "0.1994", "0.447", "0.0047", "0.2449", "0.0659", "0.2509", "0.2336", "0.5712",
        "0.3265", "0.5741", "-0.0954", "0.2052", "0.1456", "0.3866", "101.4", "0.9199",
        # R81 POSTHOC-R81-1: the three five-call lanes, sourced from r74/NUMBERS_R74.md
        # keys LUNA-NOK / OP5-NOK / H45-NOK on the identical n=661 TRUE population
        "0.8182", "0.8327", "0.821",
    }
    STRUCTURAL = {  # spec constants, counts, thresholds, labels
        "0", "1", "2", "3", "4", "5", "6", "9", "10", "12", "23", "28", "33", "35", "36",
        "37", "39", "40", "41", "50", "60", "65", "84", "94", "98", "104", "126", "161",
        "175", "20", "238", "244", "266", "284", "307", "463", "588", "595", "661", "1000",
        "42", "0.05", "5", "399", "0.5", "1.055", "0.205", "0.339", "0.164", "0.257",
        "0.62", "0.67", "0.78", "1.47", "0.94", "0.91", "0.95", "0.98", "0.99", "8",
        "0.0595", "0.7541", "3.9", "0.9", "1.15", "7", "0.06", "13",
        # R81 Phase 1c: percentile constants of the frozen estimator, and the shared
        # negative-pool size printed in the section 13 header
        "2.5", "97.5", "557",
    }
    toks = [norm(m.group()) for m in re.finditer(r"-?\d[\d,]*(?:\.\d+)?", text)]
    unaccounted = [t for t in set(toks)
                   if t not in derived and t not in PUBLISHED and t not in STRUCTURAL]
    print(f"  ledger numerals: {len(toks)} occurrences, {len(set(toks))} distinct")
    print(f"  re-derived here: {len(derived)}   declared published: {len(PUBLISHED)}   "
          f"structural: {len(STRUCTURAL)}")
    print(f"  unaccounted: {len(unaccounted)}")
    for t in sorted(unaccounted):
        idx = text.find(t)
        ctx = re.sub(r"\s+", " ", text[max(0, idx - 60):idx + 40])
        sys.stdout.write(f"    {t:>10s} | ...{ctx}...\n".encode(
            sys.stdout.encoding or "utf-8", "replace").decode(
            sys.stdout.encoding or "utf-8", "replace"))

    nfail = len(failures) + len(unaccounted)
    print(f"\n{len(checks)} checks, {len(failures)} failures; "
          f"{len(unaccounted)} unaccounted numerals")
    print("VERIFIER PASSES -- both directions clean." if nfail == 0
          else "VERIFIER FAILS")
    sys.exit(0 if nfail == 0 else 1)


main()
