# -*- coding: utf-8 -*-
"""build_sb60.py -- R141 Phase 0.1 and 0.2 (2026-09-24; $0, no model call): the sibling-name control at 60 names (SB-60).

For each of the 88 supersession pairs of the counterfactual set, SB-60 is the R136 padded PN text (cf_pad/build/texts.json, its sha256 under the lock's
method asserted equal to cf_pad/build/lock.json texts_sha256) with the target's name in the superseded-names section replaced by the pair's R125 sibling
name (reviews/r125/build/build_t4_sibling.json, rows[].sibling; ADDENDUM_R125_SIBLING's seed-12501 draw), re-rendered by the R136 renderer
(pad_common.padded_text) and nothing else changed: the section's prefix (the count table and every other line) byte-identical, the pad identical.
Collision rule (the brief, 0.1): when the R125 sibling is already a name of the PN-60 list (in the pad, or anywhere in the list), the first name of the
pair's recorded R125 eligible pool (rows[].eligible: the HV-B neighbourhood rule and the no-shared-content-token rule already applied, sorted) that is not
in the PN-60 list is taken; a pair with no such name is a STOP.

Checks (0.2): the renderer re-renders every SB-60 text byte for byte from its own printed names (88 of 88); every SB-60 list holds 60 distinct names;
the target is in no SB-60 list; the sibling is in no PN-60 list; the prefix equals the PN-60 text's prefix (so the count table is identical). The leak
screen is a model call (gpt-4.1-mini; R125's rule) and runs after the GO, as the registration's first call.
Writes reviews/r141/build/build_sb60.json. Usage: python reviews/r141/tools/build_sb60.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
for p in ("cf_pad/tools", "pad_probe/tools", "reviews/r125/tools"):
    sys.path.insert(0, str(ROOT / p))
import pad_common as PC  # noqa: E402

OUT = ROOT / "reviews" / "r141" / "build" / "build_sb60.json"


def J(rel):
    return json.load(open(ROOT / rel, encoding="utf-8"))


def sha_texts(texts):
    return hashlib.sha256("\x1f".join(texts[k] for k in sorted(texts)).encode("utf-8")).hexdigest()


def main():
    pad = J("cf_pad/build/texts.json")
    lock = J("cf_pad/build/lock.json")
    assert sha_texts(pad) == lock["texts_sha256"], "the R136 padded texts are not the locked ones"
    sb = J("reviews/r125/build/build_t4_sibling.json")
    assert sb["meta"]["n_kept"] == 88
    # Decision 4 (the author's ruling of 24 Sep): the collision substitute is a SEEDED draw, not the alphabetical first. numpy default_rng(42), one integer
    # draw per collision pair in pair-id order, uniform over the pair's remaining HV-B pool (the recorded R125 eligible names not in the PN-60 list), sorted.
    import numpy as np
    rng = np.random.default_rng(42)
    rows, texts, subs, stops = [], {}, [], []
    for r in sorted(sb["rows"], key=lambda x: x["pair_id"]):
        pid, tgt, sib = r["pair_id"], r["target"], r["sibling"]
        pn_text = pad[f"{pid}|PN"]
        pn60 = PC.committed_names(pn_text)
        assert len(pn60) == 60 and len(set(pn60)) == 60 and tgt in pn60, (pid, len(pn60))
        chosen, why, draw = sib, "R125 sibling", None
        if sib in pn60:
            alt = sorted(c for c in r["eligible"] if c not in pn60 and c != tgt)
            if not alt:
                stops.append(pid)
                continue
            draw = int(rng.integers(0, len(alt)))
            chosen, why = alt[draw], f"substitute, seeded draw {draw} of {len(alt)} (R125 sibling {sib} is in the PN-60 list)"
            subs.append(pid)
        new_list = [chosen if n == tgt else n for n in pn60]
        t = PC.padded_text(pn_text, new_list)
        texts[f"{pid}|SB60"] = t
        rows.append(dict(pair_id=pid, persona=r["persona"], category=r["category"], question=r["question"], target=tgt, r125_sibling=sib, sibling=chosen, rule=why, draw=draw,
                         in_pad_r125_sibling=sib in pn60))
    if stops:
        raise SystemExit(f"STOP: no eligible substitute outside the PN-60 list for {stops}")
    # checks
    chk = {}
    chk["renderer_bytes"] = sum(1 for k, t in texts.items() if PC.padded_text(t, PC.committed_names(t)) == t)
    chk["lists_60_distinct"] = sum(1 for t in texts.values() if len(PC.committed_names(t)) == 60 and len(set(PC.committed_names(t))) == 60)
    chk["target_in_no_sb60_list"] = sum(1 for r in rows if r["target"] not in PC.committed_names(texts[f"{r['pair_id']}|SB60"]))
    chk["sibling_in_no_pn60_list"] = sum(1 for r in rows if r["sibling"] not in PC.committed_names(pad[f"{r['pair_id']}|PN"]))
    chk["prefix_identical"] = sum(1 for r in rows if PC.split_section(texts[f"{r['pair_id']}|SB60"])[0] == PC.split_section(pad[f"{r['pair_id']}|PN"])[0])
    chk["one_name_differs"] = sum(1 for r in rows if len(set(PC.committed_names(pad[f"{r['pair_id']}|PN"])) ^ set(PC.committed_names(texts[f"{r['pair_id']}|SB60"]))) == 2)
    chk["no_overflow"] = sum(1 for t in texts.values() if "(+" not in PC.split_section(t)[1])
    assert all(v == 88 for v in chk.values()), chk
    doc = dict(meta=dict(script="reviews/r141/tools/build_sb60.py", model_calls=0, n_pairs=len(rows), n_substituted=len(subs), substituted=subs,
                         padded_texts_sha256=lock["texts_sha256"], r125_sibling_texts_sha256=sb["meta"]["texts_sha256"], texts_sha256=sha_texts(texts), checks=chk, substitute_rule="numpy default_rng(42), one integer draw per collision pair in pair-id order, uniform over the sorted remaining HV-B pool (R125 eligible names not in the PN-60 list)",
                         leak_screen="a model call (gpt-4.1-mini, R125's rule: 30 of the 88 sorted by item id, random.Random(42).sample; LEAKS iff more than 3 of 30 correct); first call after the GO"),
               rows=rows, texts=texts)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(json.dumps(doc["meta"], indent=1))


if __name__ == "__main__":
    main()
