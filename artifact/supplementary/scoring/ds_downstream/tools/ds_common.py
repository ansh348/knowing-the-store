"""ds_common.py -- shared loaders, censuses and the policy rules of registrations/ADDENDUM_DS.md
(frozen a5a2036, R100). NO API CALLS. Deterministic (local encoder for the lookup scores).

Reuses resp_review/tools/resp_common.py (the population join, the TRUE lifecycle flags, the store
variants, the L2 line renderer) so that DS's fetched lines are rendered by the same function as L2's
retrieved lines (AUX-DS-LINELOCK is then by construction, and asserted anyway).

  names            N2 (superseded names printed in the committed TRUE v2 index) and N3 (superseded u
                   retracted u expired names printed in its index_v3 rendering), read from the emitted
                   text through index_v3.named_sections (section C.4)
  fetch rule       F(i, S): every entry of the store variant whose scrubbed slot is in S and whose
                   TRUE flags include superseded / retracted / expired (section D.1)
  thresholds       theta_NOK = 104/661, theta_FOK = 35/307 on mini's committed probabilities; lambda_NOK =
                   the 75th-highest NB-6 score over the 661, lambda_FOK = the 125th-lowest NB-5 score over
                   the 307 (the matched budget; section C.5, rulings R1 / R2)
  lookup scores    NB-6 embedding on the superseded section and NB-5 embedding on the whole name map of
                   the committed TRUE index, through run_nb6.emb_scores (reproduction gate 0.7484 / 0.6186)
  policies         ALWAYS, ORACLE, MODEL, LOOKUP, MODEL-ALL, LOOKUP-ALL, LOOKUP-LIT (section D.2)
  views            the five L2 lines (byte-identical) followed by the fetched records in ascending
                   (slot, entry id) order with ranks continuing (section D.1)
"""
from __future__ import annotations

import collections
import hashlib
import io
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "resp_review" / "tools"))
import resp_common as RC                                                     # noqa: E402
from resp_common import J, jdump, sha, sha_text, true_flags, variant_ids, render_line, lifecycle_tag   # noqa: E402
from index_v2 import view, AVAIL, scrub, true_lifecycle, parse_dt, toks as e0_toks   # noqa: E402
from index_v3 import render_v3, named_sections                               # noqa: E402
from e0_common import load_joins                                             # noqa: E402
from backends import load_backend                                            # noqa: E402
from common_e1r import auroc                                                 # noqa: E402
from run_nb6 import build as nb6_build, emb_scores                           # noqa: E402

DS = ROOT / "ds_downstream"
RUN, CACHE, LEDGER = DS / "run", DS / "cache", DS / "NUMBERS_DS.md"
FREEZE, BASELINE, RESP_FREEZE, RESP_STEP4 = "a5a2036", "43a094c", "17e6328", "b08757c"
POLICIES = ("ALWAYS", "ORACLE", "MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT")
STAGE2_POLICIES = POLICIES[:6]
THETA_NOK, THETA_FOK = 104 / 661, 35 / 307
STATES = (("sup", "supersession"), ("ret", "retraction"), ("exp", "expiry"))

PINS = {**RC.PINS,
        "e1r_robustness/tools/run_baselines.py": "7dbad78f9bc6e250",
        "e1_metamemory/tools/api.py": "f57ec435997544cc",
        "e0_metamemory/tools/api.py": "77770cef4e96107d",
        "side_experiments/tools/run_side.py": "349fc15c7f1c3dd1",
        "e1_metamemory/build/items_final.json": "54bced336adc1aaf",
        "e1_metamemory/backend_entries/frbank.json": "af390ab3219a4518",
        "e1_metamemory/build/variant_plan.json": "bc01ac0d78bfef8a",
        "e1_metamemory/build/slot_ablations.json": "75550a02c7201597",
        "e1r_robustness/results/nb6.json": "942e4d0059c8efbe",
        "e1r_robustness/results/baselines_final.json": "a487079cc5ae6664",
        "e0_metamemory/thresholds.json": "315c321e21f0321a"}


# ------------------------------------------------------------------ population
def load_cell():
    sub = RC.load_cell()
    joins = load_joins()
    for it in sub:
        it["gold"] = sorted(joins[it["persona"]].gold.get(it["question_id"]) or []) if it["question_id"] in joins[it["persona"]].gold else []
    return sub


# ------------------------------------------------------------------ names (v2 / v3) per item
_P = {}


def persona_rows():
    """Raw FR-Bank rows with ages and the TRUE states per persona (index_v2.main's construction)."""
    if _P:
        return _P
    joins = load_joins()
    raw = collections.defaultdict(list)
    for r in load_backend("frbank"):
        raw[r["persona"]].append(r)
    for name in sorted(joins):
        Jp = joins[name]
        rows = sorted(raw[name], key=lambda r: r["entry_id"])
        for r in rows:
            d = parse_dt(r["recency_time"]); r["age"] = None if d is None else max(0, (Jp.t_now - d).days)
        etoks = {r["entry_id"]: e0_toks(r["text"], Jp.drop) for r in rows}
        sup, ret, exp, ev = true_lifecycle(Jp, etoks)
        _P[name] = {"rows": rows, "states": (sup, ret, exp), "events": ev}
    return _P


def removed_ids(it):
    return set(true_flags()[it["persona"]]) - set(variant_ids(it))


def names_for(it):
    """(v2_text, v3_text, N2, N3, ret_names, exp_names); v2_text must equal the committed TRUE text."""
    p = persona_rows()[it["persona"]]
    v3txt, v2txt = render_v3(view(p["rows"], p["states"], removed_ids(it)), p["events"], AVAIL[("frbank", "TRUE")])
    ns = named_sections(v3txt)
    N2 = set(ns["superseded"]); N3 = N2 | set(ns["retracted"]) | set(ns["expired"])
    return v2txt, v3txt, N2, N3, ns["retracted"], ns["expired"]


# ------------------------------------------------------------------ the fetch rule
def fetch(it, S):
    fl = true_flags()[it["persona"]]
    return sorted((e for e in variant_ids(it) if fl[e]["slot"] in S and (fl[e]["superseded"] or fl[e]["retracted"] or fl[e]["expired"])),
                  key=lambda e: (fl[e]["slot"], e))


def pn_slots(it):
    fl = true_flags()[it["persona"]]
    return {fl[m]["slot"] for m in it.get("pn_members") or [] if fl[m]["slot"]}


def flagged(it, eid):
    f = true_flags()[it["persona"]][eid]
    return f["superseded"] or f["retracted"] or f["expired"]


# ------------------------------------------------------------------ lookup scores and thresholds
def lookup_scores(sub):
    """NB-6 embedding (superseded section) and NB-5 embedding (whole map) on the committed TRUE index,
    per item, through run_nb6's committed scorer. Returns (nb6, nb5, gate) with the reproduction gate."""
    items, blind, idxT, idxB = RC.load_e1()
    from common_e1r import POPULATIONS
    src = [it for it in items if POPULATIONS["R-NOK-FRB"]["filt"](it)]
    rows = nb6_build(src, blind, idxT, "nok", "TRUE")
    ids = [r["item_id"] for r in rows]
    assert ids == [it["item_id"] for it in sub], "row order differs from the cell"
    nb6 = np.array(emb_scores(rows, "sup")); nb5 = np.array(emb_scores(rows, "all"))
    y = np.array([it["y_nok"] for it in sub]); hard = [k for k, it in enumerate(sub) if it["tier"] == "hard"]
    yh = np.array([sub[k]["y_fok"] for k in hard])
    gate = {"nb6_661": float(auroc(nb6, y)), "nb5_307": float(auroc(nb5[hard], yh))}
    gate["pass"] = round(gate["nb6_661"], 4) == 0.7484 and round(gate["nb5_307"], 4) == 0.6186
    return {it["item_id"]: float(v) for it, v in zip(sub, nb6)}, {it["item_id"]: float(v) for it, v in zip(sub, nb5)}, gate


def thresholds(sub, nb6, nb5):
    v6 = np.sort([nb6[it["item_id"]] for it in sub])[::-1]
    h5 = np.sort([nb5[it["item_id"]] for it in sub if it["tier"] == "hard"])
    return {"theta_nok": THETA_NOK, "theta_fok": THETA_FOK, "lambda_nok": float(v6[74]), "lambda_fok": float(h5[124])}


EXPECT_THRESH = {"theta_nok": 0.157337, "theta_fok": 0.114007, "lambda_nok": 0.242212, "lambda_fok": 0.318141}


# ------------------------------------------------------------------ policies
def policy_actions(it, nb6, nb5, th, N2, N3):
    """{policy: (fetch_gate, fetch_set_name, abstain)} per section D.2."""
    nok, fok = it["true"]["nok"], it["true"]["fok"]
    m_g, m_a = nok >= th["theta_nok"], fok < th["theta_fok"]
    l_g, l_a = nb6[it["item_id"]] >= th["lambda_nok"], nb5[it["item_id"]] < th["lambda_fok"]
    lit_g, lit_a = nb6[it["item_id"]] >= THETA_NOK, nb5[it["item_id"]] < THETA_FOK
    return {"ALWAYS": (False, None, False),
            "ORACLE": (it["label"] == "PRESENT-NEGATIVE", "P", it["label"] == "ABSENT"),
            "MODEL": (m_g, "N2", m_a), "LOOKUP": (l_g, "N2", l_a),
            "MODEL-ALL": (m_g, "N3", m_a), "LOOKUP-ALL": (l_g, "N3", l_a),
            "LOOKUP-LIT": (lit_g, "N2", lit_a)}


def build_policies(sub, nb6, nb5, th):
    out = {}
    for it in sub:
        v2txt, v3txt, N2, N3, ret_n, exp_n = names_for(it)
        sets = {"P": pn_slots(it) if it["label"] == "PRESENT-NEGATIVE" else set(), "N2": N2, "N3": N3}
        acts = policy_actions(it, nb6, nb5, th, N2, N3)
        rec = {"label": it["label"], "state": it["state"], "persona": it["persona"], "variant": it["variant"], "tier": it["tier"],
               "nok": it["true"]["nok"], "fok": it["true"]["fok"], "nb6": nb6[it["item_id"]], "nb5": nb5[it["item_id"]],
               "N2": sorted(N2), "N3": sorted(N3), "pn_slots": sorted(sets["P"]), "gold": it["gold"], "pn_members": it.get("pn_members") or [],
               "policies": {}}
        for pol, (g, sname, a) in acts.items():
            fetched = fetch(it, sets[sname]) if g and sname else []
            rec["policies"][pol] = {"gate": bool(g), "fetch_set": sname if g else None, "abstain": bool(a), "fetched": fetched}
        out[it["item_id"]] = rec
    return out


# ------------------------------------------------------------------ views
def assemble_view(it, block, top5_ids, fetched):
    """The five L2 lines byte-identical, then the fetched records not among the five, ranks continuing."""
    fl = true_flags()[it["persona"]]
    lines = block.split("\n") if block else []
    assert len(lines) == len(top5_ids)
    extra = [e for e in fetched if e not in set(top5_ids)]
    for k, e in enumerate(extra):
        lines.append(render_line(len(top5_ids) + k + 1, fl[e]))
    ids = list(top5_ids) + extra
    return "\n".join(lines), ids


def view_sha(text):
    return sha_text(text)[:16]
