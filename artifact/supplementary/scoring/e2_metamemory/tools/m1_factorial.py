"""
m1_factorial.py -- M1: the NOK three-fix 2^3 factorial. RAW RESPONSES ONLY.

Exactly per modules/M1_NOK_FACTORIAL.md. Computes NO factor effect, NO AUROC,
NO aggregate -- that happens at scoring, after the SP3 go.

Factors, each realised as a derived variant of a FROZEN artifact. Nothing frozen
is edited; the variants are built in memory from the committed originals.

  L  lifecycle signal in the index. OFF removes, from the rendered TRUE index:
     the LIFECYCLE TOTALS block, the per-category ACTIVE/SUPRSD/RETRACT/EXPIRED
     columns (CATEGORY / ENTRIES / NEWEST / OLDEST survive), and the
     "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT" block. Nothing else moves.
  W  worked examples. OFF deletes the two example paragraphs from SYSTEM.
  D  two-step decomposition. OFF collapses Step 1 + Step 2 into a single `nok`
     judgment and drops `nok_candidates_found` from the response schema. When D
     is OFF and W is ON, the examples' `nok_candidates_found = ...` clauses are
     dropped too, since the field no longer exists.

Index provenance is TRUE, matching E1's H_NOK row (indexed-TRUE, 0.7339), which
is the result this factorial decomposes.

  lane   gpt-4.1-mini, temperature 0, seed 42, k=1
  items  FR-Bank scoreable, all variants (661) x 8 cells = 5,288 calls
  cache  (item_id, cell, model, prompt_hash)

Usage:  python e2_metamemory/tools/m1_factorial.py
"""

from __future__ import annotations

import collections
import concurrent.futures as cf
import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e1_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import e2_api as api                                              # noqa: E402
import prompts_e1 as P1                                           # noqa: E402
from e2_common import E2, Indexes, jdump, load_items, sha         # noqa: E402

WORKERS = 12
E1_TEXTS_SHA = "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"

LIFECYCLE_LABELS = ("active", "superseded", "retracted", "expired",
                    "supersession events")
LIFE_COLS = {"ACTIVE", "SUPRSD", "RETRACT", "EXPIRED"}


def strip_lifecycle(text: str) -> str:
    """L=off. Removes only the three lifecycle-bearing regions."""
    lines = text.split("\n")
    out, block, cols, keep_idx = [], None, None, None
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("LIFECYCLE TOTALS"):
            block = "life"
            i += 1
            while i < len(lines) and (lines[i].strip() == ""
                                      or lines[i][2:24].strip() in LIFECYCLE_LABELS
                                      or lines[i].strip() == "not expressible by this backend"):
                if lines[i].strip() == "":
                    break
                i += 1
            continue
        if ln.startswith("ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT"):
            i += 1
            while i < len(lines) and lines[i].strip() != "":
                i += 1
            continue
        if ln.startswith("CATEGORY"):
            cols = ln.split()[1:]
            keep_idx = [n for n, c in enumerate(cols) if c not in LIFE_COLS]
            hdr = f"{'CATEGORY':<24s}"
            for n in keep_idx:
                hdr += f"{cols[n]:>{8 if n == 0 or cols[n] in ('NEWEST', 'OLDEST') else 9}s}"
            out.append(hdr)
            i += 1
            continue
        if cols is not None and ln and not ln.startswith(" ") and \
                len(ln.split()) == len(cols) + 1:
            parts = ln.split()
            row = f"{parts[0]:<24s}"
            for n in keep_idx:
                w = 8 if n == 0 or cols[n] in ("NEWEST", "OLDEST") else 9
                row += f"{parts[1 + n]:>{w}s}"
            out.append(row)
            i += 1
            continue
        if ln.startswith("RECENCY") or ln.startswith("AGE DISTRIBUTION") \
                or ln.startswith("ATTRIBUTE NAMES"):
            cols = None
        out.append(ln)
        i += 1
    # collapse any run of >1 blank line the removals produced
    res, prev_blank = [], False
    for ln in out:
        if ln.strip() == "":
            if prev_blank:
                continue
            prev_blank = True
        else:
            prev_blank = False
        res.append(ln)
    return "\n".join(res)


def system_variant(W: bool, D: bool) -> str:
    s = P1.SYSTEM
    if not D:
        old = (" Judge this in two steps.\n\n"
               "  Step 1, nok_candidates_found: is there content on this topic in the "
               "store that has been superseded by a later value, retracted by the user, "
               "or has passed its date? true or false.\n\n"
               "  Step 2, nok: the probability, 0 to 100, that such content is present.")
        new = ("\n\nnok: the probability, 0 to 100, that such content is present.")
        assert old in s, "D-off anchor not found in frozen SYSTEM"
        s = s.replace(old, new, 1)
        s = s.replace('{"fok": <0-100>, "nok_candidates_found": <true|false>, '
                      '"nok": <0-100>, "would_search": <true|false>}',
                      '{"fok": <0-100>, "nok": <0-100>, "would_search": <true|false>}', 1)
        s = s.replace("nok_candidates_found = false, nok = 5", "nok = 5", 1)
        s = s.replace("nok_candidates_found = true, nok = 85", "nok = 85", 1)
    if not W:
        a = s.index("Two worked examples.")
        b = s.index("Note that FOK and the negative-obligation judgment are independent.")
        s = s[:a] + s[b:]
    return s


def clamp(v):
    try:
        return min(100.0, max(0.0, float(v))) / 100.0
    except (TypeError, ValueError):
        return None


def main():
    got = P1.texts_sha256()
    assert got == E1_TEXTS_SHA, f"frozen prompts changed: {got}"
    print(f"E1 frozen prompt texts sha verified {got[:16]}...")

    items = load_items()
    IX = Indexes()
    cells = list(itertools.product((1, 0), repeat=3))   # (L, W, D)
    idx_cache = {}
    variants = {}
    for L, W, D in cells:
        variants[(L, W, D)] = system_variant(bool(W), bool(D))
    for k, v in variants.items():
        print(f"  cell L{k[0]}W{k[1]}D{k[2]}: system {len(v)} chars, "
              f"sha {sha(v)[:12]}")

    jobs = []
    for it in items:
        base = IX.text(it, "TRUE")
        key = sha(base)
        if key not in idx_cache:
            idx_cache[key] = {1: base, 0: strip_lifecycle(base)}
        for (L, W, D) in cells:
            jobs.append((it, L, W, D, idx_cache[key][L]))
    print(f"{len(items)} items x {len(cells)} cells = {len(jobs)} calls")

    def run(job):
        it, L, W, D, index = job
        cell = f"L{L}W{W}D{D}"
        msgs = [{"role": "system", "content": variants[(L, W, D)]},
                {"role": "user", "content": P1.USER_INDEXED.format(
                    index=index, question=it["question"])}]
        r = api.call(it["item_id"], f"m1-{cell}", msgs)
        o = api.parse_json(r["content"]) or {}
        api.check_cap()
        return {"item_id": it["item_id"], "cell": cell, "L": L, "W": W, "D": D,
                "label": it["label_final"], "variant": it["variant"],
                "split": it["split"], "persona": it["persona"],
                "fok": clamp(o.get("fok")), "nok": clamp(o.get("nok")),
                "nok_candidates_found": (bool(o.get("nok_candidates_found"))
                                         if D else None),
                "status": "OK" if clamp(o.get("nok")) is not None else "PARSE_FAIL",
                "cached": r["cached"]}

    out = []
    try:
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
            for n, rec in enumerate(ex.map(run, jobs), 1):
                out.append(rec)
                if n % 500 == 0:
                    api.flush()
                    print(f"  {n}/{len(jobs)}  ${api.spend()[0]:.4f}", flush=True)
    finally:
        api.flush()

    jdump({"module": "M1", "design": "2^3 full factorial (L, W, D)",
           "index_provenance": "TRUE (matches E1's H_NOK row)",
           "model": "gpt-4.1-mini", "k": 1, "n": len(out),
           "system_sha_by_cell": {f"L{L}W{W}D{D}": sha(variants[(L, W, D)])
                                  for (L, W, D) in cells},
           "rows": out}, E2 / "m1_factorial_raw.json")

    c = collections.Counter((r["cell"], r["status"]) for r in out)
    print("\nper-cell parse census (RAW, no effect computed):")
    for (L, W, D) in cells:
        cell = f"L{L}W{W}D{D}"
        print(f"  {cell}: OK {c[(cell,'OK')]:4d}  PARSE_FAIL {c[(cell,'PARSE_FAIL')]:3d}")
    print(f"E2 cumulative ${api.spend()[0]:.4f} of ${api.E2_CAP_USD}")
    print("wrote m1_factorial_raw.json -- no factor effect computed")


if __name__ == "__main__":
    main()
