# -*- coding: utf-8 -*-
"""r125_t4_build.py -- Task 4, the sibling-name control: the SIBLING summaries (offline construction; no model call). $0.

For each of the 88 supersession pairs of the counterfactual set, a fourth summary is rendered from the PN version's superseded-only (v2)
summary by replacing the target's name in the ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT section with a sibling attribute name from the
same category. Everything else, every count line and every name-map line included, is byte-identical to the PN text, so the SIBLING
version differs from PN only in WHICH name the list carries: a count reader and the random-token control are at chance (the count reader
exactly; the token control up to the token drawn for the sibling) and what remains is the binding of a name to the question.

Sibling rule (seed 12501, numpy default_rng, uniform over the sorted eligible names): the persona's name map is the ATTRIBUTE NAMES BY CATEGORY
section as printed (index_features.parse, attr_by_cat), the pool is the names printed under the target's category (cf_pairs_cf2.json
pairs[].category) in all three versions of the pair (PN, PRESENT, ABSENT: present in every version, HV-B's rule 6.4 (a)), minus: the target
slot (HV-B 6.4 (c)); any name already in the PN version's superseded-names list; any name in the target's encoder neighbourhood (HV-B 6.4 (d):
cosine under all-MiniLM-L6-v2 on the two names with underscores as spaces at or above tau 0.503637, registrations/ADDENDUM_RESP.md C.2);
any name sharing a content token (e0_common.toks with the persona's name dropped) with the question or with the target name. A pair with no
eligible sibling drops, with the count reported. Label: PRESENT under Definition 1 (the stale record the list names is not relevant to the
question). The section is re-rendered by the renderer's own rule (sorted names, ", "-joined, textwrap at 150, indents "  " / "    "), and
the lock asserts that every line outside the section is byte-identical to PN, that index_v3.named_sections reads the intended list, and
that index_features.parse agrees with PN on every field but superseded_attrs.
Writes reviews/r125/build/build_t4_sibling.json (the texts, the draws, the eligibility census, the locks, the texts' sha256).
"""
from __future__ import annotations

import hashlib
import sys
import textwrap

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r125_common as C  # noqa: E402
sys.path.insert(0, str(C.ROOT / "e0_metamemory" / "tools"))
from e0_common import toks  # noqa: E402
from index_features import parse as parse_index  # noqa: E402
from index_v3 import named_sections  # noqa: E402
from index_v2 import scrub  # noqa: E402

OUT = C.BUILD / "build_t4_sibling.json"
SEED = 12501
TAU_NEIGHBOUR = 0.503637
HDR = "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT  (value-scrubbed)"
WRAP = 150


def section_split(text):
    """(head lines up to and including the header, section body lines)."""
    lines = text.split("\n"); i = lines.index(HDR)
    return lines[: i + 1], lines[i + 1:]


def render_section(names):
    names = sorted(set(names))
    if not names:
        return ["  (none)"]
    return textwrap.wrap(", ".join(names), width=WRAP, initial_indent="  ", subsequent_indent="    ")


def main():
    cell = C.Cell()
    from run_baselines import encoder
    enc = encoder(); vcache = {}

    def vec(n):
        if n not in vcache:
            vcache[n] = enc.encode([n.replace("_", " ")], normalize_embeddings=True)[0]
        return vcache[n]

    persona_names = C.jload(C.CF2 / "_names_cf2.json")
    rng = np.random.default_rng(SEED)
    rows = []; dropped = []; texts = {}
    for pid in cell.pids("SUPERSESSION"):
        pair = cell.pairs[pid]; ind = cell.meta["individuation"][pid]; target = ind["slot_scrubbed"]; cat = pair["category"]; persona = pair["persona"]
        assert scrub(pair["slot_key"][1]) == target if isinstance(pair["slot_key"], list) else True
        t = {v: cell.idx[cell.ids[cell.pos_of[(pid, v)]]]["v2"] for v in C.VERSIONS}
        q = cell.qs[cell.pos_of[(pid, "PN")]]
        pn_list = named_sections(t["PN"])["superseded"]
        assert target in pn_list, (pid, target, pn_list)
        maps = {v: set(parse_index(t[v])["attr_by_cat"].get(cat, [])) for v in C.VERSIONS}
        pool = sorted(maps["PN"] & maps["PRESENT"] & maps["ABSENT"])
        drop = toks(persona_names.get(persona) or "")
        qtok = toks(q, drop); ttok = toks(target.replace("_", " "), drop)
        census = {"pool_in_all_three": len(pool), "not_target": 0, "not_in_pn_list": 0, "not_neighbour": 0, "no_shared_token": 0}
        elig = []; reasons = {}
        for n in pool:
            if n == target:
                reasons[n] = "target"; continue
            census["not_target"] += 1
            if n in pn_list:
                reasons[n] = "already in the PN list"; continue
            census["not_in_pn_list"] += 1
            cos = float(vec(n) @ vec(target))
            if cos >= TAU_NEIGHBOUR:
                reasons[n] = f"neighbour (cos {cos:.4f})"; continue
            census["not_neighbour"] += 1
            nt = toks(n.replace("_", " "), drop)
            if nt & (qtok | ttok):
                reasons[n] = f"shares a token with the question or the target: {sorted(nt & (qtok | ttok))}"; continue
            census["no_shared_token"] += 1
            elig.append((n, cos))
        if not elig:
            dropped.append({"pair_id": pid, "target": target, "category": cat, "census": census, "reasons": reasons}); continue
        k = int(rng.integers(0, len(elig)))
        sib, cos = elig[k]
        head, body = section_split(t["PN"])
        new_list = [sib if n == target else n for n in pn_list]
        sib_text = "\n".join(head + render_section(new_list))
        # locks
        assert sib_text.split("\n")[: len(head)] == head
        assert named_sections(sib_text)["superseded"] == sorted(set(new_list)), (pid, named_sections(sib_text)["superseded"], new_list)
        p_pn, p_sib = parse_index(t["PN"]), parse_index(sib_text)
        for key in p_pn:
            if key == "superseded_attrs":
                continue
            assert p_pn[key] == p_sib[key], (pid, key)
        assert set(p_sib["superseded_attrs"]) == set(new_list) and len(new_list) == len(pn_list)
        assert sib in p_pn["attr_by_cat"][cat] and sib_text.count(sib) == t["PN"].count(sib) + 1
        assert render_section(pn_list) == body, (pid, "the PN section does not re-render byte-identically")
        item_id = f"{pid}|SIBLING"
        texts[item_id] = sib_text
        rows.append({"pair_id": pid, "item_id": item_id, "persona": persona, "question": q, "category": cat, "target": target, "sibling": sib, "cos_sibling_target": round(cos, 4),
                     "pn_list": pn_list, "sibling_list": sorted(set(new_list)), "n_eligible": len(elig), "eligible": [n for n, _ in elig], "census": census, "draw_index": k,
                     "label": "PRESENT", "y_nok": 0, "state": "SUPERSESSION"})
    shas = [hashlib.sha256(texts[r["item_id"]].encode("utf-8")).hexdigest() for r in rows]
    rec = {"meta": {"script": "reviews/r125/tools/r125_t4_build.py", "seed": SEED, "rng": "numpy default_rng(12501); one integer draw per kept pair in pair-id order", "tau_neighbour": TAU_NEIGHBOUR,
                    "encoder": "sentence-transformers/all-MiniLM-L6-v2 (run_baselines.encoder)", "label": "PRESENT under Definition 1", "n_pairs": 88, "n_kept": len(rows), "n_dropped": len(dropped),
                    "texts_sha256": hashlib.sha256("".join(shas).encode()).hexdigest(), "model_calls": 0},
           "rows": rows, "dropped": dropped, "texts": texts}
    C.jdump(rec, OUT)
    print(f"kept {len(rows)} of 88 pairs; dropped {len(dropped)}: {[d['pair_id'] for d in dropped]}")
    print(f"eligible per kept pair: min {min(r['n_eligible'] for r in rows)}, median {int(np.median([r['n_eligible'] for r in rows]))}, max {max(r['n_eligible'] for r in rows)}; texts sha256 {rec['meta']['texts_sha256'][:16]}")
    for r in rows[:5]:
        print(f"  {r['pair_id']:46s} {r['target']:32s} -> {r['sibling']:32s} cos {r['cos_sibling_target']} of {r['n_eligible']}")
    print(f"-> {OUT.relative_to(C.ROOT)}")


if __name__ == "__main__":
    main()
