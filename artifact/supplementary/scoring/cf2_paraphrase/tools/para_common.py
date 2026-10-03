"""Shared pieces of the CF-2 paraphrase probe (registrations/ADDENDUM_PARA.md, sha256
45cad63d374d5215c4f79eee4192cabb16854238b7782f519cb9a14f8574c009).

Everything here is deterministic and makes no model call: the population (§2), the forbidden set
F(pair) and the screen (§3), the locks the registration's STOP list names (registration sha256,
CF-2 questions and indexes sha256), and the lookup gate on the original questions (§2).

Reuses verbatim: index_features.parse / toks / _sing (e1r_robustness/tools), index_v3.named_sections
(r82_counterfactual), score_cf.matcher and run_nb6.lex_scores through nb6_sweep/tools/sweep_common
(the committed lookups), draft_questions.intent_ok (r82_counterfactual/tools; the CF-1 intent gate).
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

ROOT = Path(__file__).resolve().parents[2]
for p in ("e1r_robustness/tools", "r82_counterfactual", "r82_counterfactual/tools", "nb6_sweep/tools", "e1_metamemory/tools"):
    sys.path.insert(0, str(ROOT / p))

from index_features import _sing, parse, toks  # noqa: E402
from index_v3 import named_sections  # noqa: E402

CF2 = ROOT / "r82_counterfactual" / "cf2"
PARA = ROOT / "cf2_paraphrase"
REG = ROOT / "registrations" / "ADDENDUM_PARA.md"
REG_SHA = "45cad63d374d5215c4f79eee4192cabb16854238b7782f519cb9a14f8574c009"   # CLAIMS.md R104 block
SHEET = ROOT / "reviews" / "v12" / "PARAPHRASE_READ.md"      # the author's name for the §5 sheet (dated line, 2026-09-14)
GATE = {"emb_v2": 0.7663, "emb_v3": 0.8756}      # AUX-CF2-NB6-V2, AUX-CF2-ALLSTATES-V3, four decimals


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True, default=float)
        f.write("\n")


FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."     # dated sections are appended below it after the freeze


def sha256_file(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()


def sha256_frozen(p):
    """sha256 of the registered text: the bytes above the FROZEN_END marker (the whole file when absent)."""
    b = io.open(p, "rb").read()
    i = b.find(FROZEN_END)
    return hashlib.sha256(b if i < 0 else b[:i]).hexdigest()


# ------------------------------------------------------------------ locks (STOP list, before any call)
def locks():
    """Registration sha256; CF-2 questions and indexes content hashes as the files record them."""
    out = {"registration_sha256": sha256_frozen(REG), "registration_expected": REG_SHA,
           "registration_ok": sha256_frozen(REG) == REG_SHA, "registration_file_sha256": sha256_file(REG)}
    q = jload(CF2 / "cf_questions_cf2.json")
    qh = hashlib.sha256("\x1f".join(r["question"] for r in q["questions"]).encode("utf-8")).hexdigest()
    out.update({"questions_sha256": qh, "questions_meta": q["meta"]["questions_sha256"],
                "questions_ok": qh == q["meta"]["questions_sha256"], "n_questions": len(q["questions"])})
    idx = jload(CF2 / "cf_indexes.json")
    ih = hashlib.sha256("\x1f".join(idx["indexes"][k]["v2"] + "\x1e" + idx["indexes"][k]["v3"]
                                    for k in sorted(idx["indexes"])).encode()).hexdigest()
    cell = jload(CF2 / "cf_cell.json")
    out.update({"indexes_sha256": ih, "indexes_meta": idx["meta"]["sha256"], "cell_meta": cell["meta"]["indexes_sha256"],
                "indexes_ok": ih == idx["meta"]["sha256"] == cell["meta"]["indexes_sha256"]})
    out["all_ok"] = bool(out["registration_ok"] and out["questions_ok"] and out["indexes_ok"])
    return out


# ------------------------------------------------------------------ population (§2)
def pairs():
    """The 148 pairs with their three versions' item ids and the committed summaries."""
    q = jload(CF2 / "cf_questions_cf2.json")["questions"]
    cell = jload(CF2 / "cf_cell.json")
    idx = jload(CF2 / "cf_indexes.json")["indexes"]
    by_pair = {}
    for it in cell["items"]:
        by_pair.setdefault(it["pair_id"], []).append(it)
    out = []
    for r in q:
        items = sorted(by_pair[r["pair_id"]], key=lambda it: it["version"])
        assert len(items) == 3, r["pair_id"]
        assert all(it["question"] == r["question"] for it in items), r["pair_id"]
        out.append({"pair_id": r["pair_id"], "persona": r["persona"], "entity": r["entity"], "slot": r["slot"],
                    "intent": r["intent"], "state": r["state"], "question": r["question"],
                    "items": [{"item_id": it["item_id"], "version": it["version"], "y_nok": it["y_nok"],
                               "y_fok": it["y_fok"], "v2": idx[it["item_id"]]["v2"], "v3": idx[it["item_id"]]["v3"]}
                              for it in items]})
    return out


# ------------------------------------------------------------------ forbidden set and screen (§3)
def content(s):
    """toks closed under _sing: the registration's token set for one string."""
    return {_sing(t) for t in toks(s)}


def forbidden(pair, scope="registered"):
    """F(pair): (a) content tokens of the slot path and (b) of every attribute name printed in the v3
    summaries of the pair's three versions -- the per-category name map (all buckets; the '(+N more)'
    overflow is not printed and not included) and the three state sections -- underscores replaced by
    spaces. Returns (F, provenance counts).

    scope "registered": (a) is the whole slot path split on ':' and '_' (§3 as frozen).
    scope "narrowed":   (a) is the scrubbed slot name only, the part before the first ':' (the only part
                        any summary prints) -- the author's ruling of 2026-09-14 (evening) on the §4 STOP,
                        applied to the redraft of the 61 excluded pairs and to the scoring-time re-run on
                        the whole set. (b) is unchanged under both scopes."""
    slot = pair["slot"] if scope == "registered" else pair["slot"].split(":", 1)[0]
    F = set(content(slot.replace(":", " ").replace("_", " ")))
    n_slot = len(F)
    names = set()
    for it in pair["items"]:
        p = parse(it["v3"])
        for lst in p["attr_by_cat"].values():
            names.update(lst)
        s = named_sections(it["v3"])
        for k in ("superseded", "retracted", "expired"):
            names.update(s[k])
    for n in names:
        F |= content(n.replace("_", " "))
    return F, {"slot_tokens": n_slot, "names": len(names), "F_size": len(F), "scope": scope}


def screen(candidate, original, F):
    """(passes, offending tokens). Passes when no content token of the candidate is in F and the
    candidate differs from the original after case-folding."""
    hit = sorted(content(candidate) & F)
    same = candidate.strip().casefold() == original.strip().casefold()
    return (not hit and not same), hit, same


# ------------------------------------------------------------------ the lookup gate (§2), $0
def lookup_gate(pairs_):
    """Both lookups on the ORIGINAL questions under v2 (superseded section) and v3 (three sections),
    exactly as cf2_score builds the lists; must reproduce AUX-CF2-NB6-V2 0.7663 and
    AUX-CF2-ALLSTATES-V3 0.8756 at four decimals."""
    import numpy as np
    from sweep_common import auroc, emb_cached, lex_cached
    rows, v2, v3 = [], {}, {}
    for pr in pairs_:
        for it in pr["items"]:
            rows.append({"pop": "cf2", "key": it["item_id"], "question": pr["question"], "y": it["y_nok"],
                         "persona": pr["persona"], "state": pr["state"]})
            s = named_sections(it["v3"])
            v2[it["item_id"]] = list(named_sections(it["v2"])["superseded"])
            v3[it["item_id"]] = list(s["superseded"] + s["retracted"] + s["expired"])
    y = np.array([r["y"] for r in rows], int)
    got = {"emb_v2": float(auroc(emb_cached(rows, v2), y)), "emb_v3": float(auroc(emb_cached(rows, v3), y)),
           "lex_v2": float(auroc(lex_cached(rows, v2), y)), "lex_v3": float(auroc(lex_cached(rows, v3), y))}
    ok = all(round(got[k], 4) == GATE[k] for k in GATE)
    return got, ok
