"""cell_e1xv.py -- E1-XV cell reconstruction, READ-ONLY over frozen E1 artifacts.

Rebuilds the matched FR-Bank cell that produced NUMBERS.md section 9 (the capability
table of record) and section 10, and rebuilds the two elicitation prompts for each
item from the FROZEN `prompts_e1` module.

Nothing is written to E1. Nothing in E1 is imported except `prompts_e1`, whose
sha256 is asserted before use -- if the frozen module has drifted, this raises
rather than silently porting different wording to a new vendor.

The cell is defined exactly as `score_ladder.py:main` defines it:
    frb = sorted(k for k in li if items[k]["backend"] == "frbank")
where `li` is the INDEXED-TRUE arm of the committed k=5 ladder file.

Label vectors, exactly as `score_ladder.py:cellset` maps them:
    FOK  positive = non-ABSENT
    NOK  positive = PRESENT-NEGATIVE
These are TWO LABEL VECTORS OVER ONE ITEM SET, not two subsets: n = 84 with 54 FOK
positives and 40 NOK positives, and 54 + 40 > 84 is expected, not an error.
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E1 = ROOT / "e1_metamemory"
sys.path.insert(0, str(E1 / "tools"))

# The frozen module, pinned by content. PREREG_E1.md records these two digests.
PROMPTS_FILE_SHA = "337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84"
PROMPTS_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"

import prompts_e1 as P  # noqa: E402

if P.file_sha256() != PROMPTS_FILE_SHA or P.texts_sha256() != PROMPTS_TEXTS_SHA:
    raise SystemExit(
        "FROZEN PROMPT MODULE HAS DRIFTED -- refusing to port.\n"
        f"  file  expected {PROMPTS_FILE_SHA}\n        got      {P.file_sha256()}\n"
        f"  texts expected {PROMPTS_TEXTS_SHA}\n        got      {P.texts_sha256()}")

EXPECT = {"n": 84, "n_fok_pos": 54, "n_nok_pos": 40}


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def ikey(it):
    """Index key, verbatim from redraw_frontier.py:main."""
    b, p, v = it["backend"], it["persona"], it["variant"]
    return f"{b}:{p}:SLOT:{it['question_id']}" if v == "SLOT-ABLATED" else f"{b}:{p}:{v}"


def label(it):
    """Label resolution, verbatim from score_ladder.py:cellset."""
    return it.get("label", it["label_pre"])


def build():
    items = {i["item_id"]: i for i in jload(E1 / "build" / "items_final.json")}
    ladder = jload(E1 / "ladder_gpt-5.6-luna.json")
    li = {r["item_id"] for r in ladder["rows"] if r["arm"] == "INDEXED-TRUE"}
    frb = sorted(k for k in li if items[k]["backend"] == "frbank")

    # cross-check the same cell against the OTHER committed k=5 file
    sol = jload(E1 / "redraw_frontier.json")
    si = {r["item_id"] for r in sol["rows"] if r["arm"] == "INDEXED-TRUE"}
    frb_sol = sorted(k for k in si if items[k]["backend"] == "frbank")

    questions = {r["item_id"]: r["question"]
                 for r in jload(E1 / "strong_model.json")["rows"]}
    idx = jload(E1 / "indexes_v2.json")["indexes"]

    rows = []
    for k in frb:
        it, q = items[k], questions[k]
        key = f"{ikey(it)}:TRUE"
        if key not in idx:
            raise SystemExit(f"no TRUE index for {k} ({key})")
        lab = label(it)
        rows.append({
            "item_id": k, "backend": it["backend"], "persona": it["persona"],
            "variant": it["variant"], "label": lab,
            "y_fok": 0 if lab == "ABSENT" else 1,
            "y_nok": 1 if lab == "PRESENT-NEGATIVE" else 0,
            "question": q,
            "user_blind": P.USER_BLIND.format(question=q),
            "user_indexed": P.USER_INDEXED.format(index=idx[key], question=q),
        })

    got = {"n": len(rows), "n_fok_pos": sum(r["y_fok"] for r in rows),
           "n_nok_pos": sum(r["y_nok"] for r in rows)}
    return rows, got, frb == frb_sol, ladder, sol


def main():
    rows, got, sol_agrees, ladder, sol = build()
    print("FROZEN PROMPT MODULE -- both digests match PREREG_E1.md")
    print(f"  file  sha256 {P.file_sha256()}")
    print(f"  texts sha256 {P.texts_sha256()}")
    print(f"  MODEL={P.MODEL!r} TEMPERATURE={P.TEMPERATURE} SEED={P.SEED} "
          f"MAX_TOKENS={P.MAX_TOKENS}")

    print("\nCELL RECONSTRUCTION vs NUMBERS.md section 9")
    for k, v in got.items():
        ok = v == EXPECT[k]
        print(f"  {'ok  ' if ok else 'FAIL'} {k:12s} rebuilt {v:4d}   expected {EXPECT[k]:4d}")
    print(f"  {'ok  ' if sol_agrees else 'FAIL'} same 84 item_ids in the sol k=5 file "
          f"({sol['model']}) as in the luna file ({ladder['model']})")
    if got != EXPECT or not sol_agrees:
        raise SystemExit("CELL DOES NOT REBUILD -- stop")

    print("\n  label composition")
    comp = {}
    for r in rows:
        comp[r["label"]] = comp.get(r["label"], 0) + 1
    for k in sorted(comp):
        print(f"    {k:20s} {comp[k]:3d}")
    print(f"    {'non-ABSENT (FOK pos)':20s} {got['n_fok_pos']:3d}")
    print("  54 + 40 = 94 > 84 because these are two label vectors over one item set.")

    ch_b = [len(r["user_blind"]) for r in rows]
    ch_i = [len(r["user_indexed"]) for r in rows]
    sysch = len(P.SYSTEM)
    print(f"\nPROMPT SIZE (characters)")
    print(f"  SYSTEM (shared by both arms)      {sysch:7d}")
    print(f"  USER_BLIND     min/mean/max       {min(ch_b):7d} {sum(ch_b)//len(ch_b):7d} {max(ch_b):7d}")
    print(f"  USER_INDEXED   min/mean/max       {min(ch_i):7d} {sum(ch_i)//len(ch_i):7d} {max(ch_i):7d}")

    out = Path(__file__).resolve().parents[1] / "manifests" / "cell_84.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {"n": got["n"], "expect": EXPECT, "rebuilt": got,
               "prompts_file_sha256": P.file_sha256(),
               "prompts_texts_sha256": P.texts_sha256(),
               "source_ladder": "e1_metamemory/ladder_gpt-5.6-luna.json",
               "source_crosscheck": "e1_metamemory/redraw_frontier.json",
               "items": [{k: r[k] for k in ("item_id", "persona", "variant", "label",
                                            "y_fok", "y_nok", "question")} for r in rows]}
    io.open(out, "w", encoding="utf-8").write(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"\nwritten: {out.relative_to(ROOT)}  (item ids + labels + questions; "
          f"prompts rebuilt on demand, never cached to disk)")


if __name__ == "__main__":
    main()
