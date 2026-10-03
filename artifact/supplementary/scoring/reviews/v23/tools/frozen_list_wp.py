"""frozen_list_wp.py -- the writing pass (R111): every frozen string changed between the pass base (reviews/v18/base_tree_wp.txt, paper_v18.tex before Phase 1) and the built paper_v18.tex, in full,
so the R110 authorization block can quote each one (reviews/v18/claims_r111_block.md). Reads frozen_diff's own functions; no gate logic
is duplicated. Usage: python reviews/v18/tools/frozen_list_wp.py <base tree> [--json=out.json]"""
from __future__ import annotations

import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
sys.path.insert(0, str(SUB / "tools"))
import frozen_diff as FD  # noqa: E402


def main():
    base_rev = sys.argv[1]
    out_json = next((a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--json=")), None)
    base_tex = next((a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--base-tex=")), "paper_v22.tex")   # v19 (R112): the base is the v18 close
    tex = next((a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--tex=")), "paper_v23.tex")
    base = FD.norm(FD.git_show(base_rev, "iclr2027_monitoring_submission/" + base_tex))
    new_raw = (SUB / tex).read_text(encoding="utf-8", errors="replace")
    extra = next((a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--extra-tex=")), None)   # v19 (R112): the supplement only on request, as frozen_diff
    if extra:
        new_raw += "\n" + (SUB / extra).read_text(encoding="utf-8", errors="replace")
    new = FD.norm(new_raw)
    claims = (SUB / "CLAIMS.md").read_text(encoding="utf-8", errors="replace")
    program = next((a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--program=")), "R133")
    outside, inside = FD.claims_sections(claims, program)
    auth = {FD.norm(q) for q in FD.quoted(inside)}
    import claims_diff, prose_scan  # noqa: E401
    src = [("U", k, v) for k, v in claims_diff.U_BLOCKS.items()]
    sl = FD.ast_lists(SUB / "tools" / "slogan_scan.py", {"PINNED", "EXEMPT_S8", "EXEMPT_S9", "EXEMPT_S10", "EXEMPT_FROZEN_REGISTERED"})
    src += [("S", k, v) for k, vs in sl.items() for v in vs]
    src += [("W", f"WHITELIST[{i}]", w[0]) for i, w in enumerate(prose_scan.WHITELIST)]
    src += [("Q", "CLAIMS", q) for q in FD.quoted(outside)]
    src += [("R", name, frag) for name, frag in FD.registration_fragments()]   # the R111 parser, shared
    seen, rows = set(), []
    for tag, key, text in src:
        t = FD.norm(text)
        if len(t) < 8 or t in seen:
            continue
        seen.add(t)
        nb, nn = base.count(t), new.count(t)
        if nb == 0 or nb == nn:
            continue
        status = "AUTHORIZED" if any(t in a or a in t for a in auth) else "UNAUTHORIZED"
        rows.append({"status": status, "tag": tag, "key": key, "base": nb, "new": nn, "text": t})
    for r in rows:
        print(f"{r['status']} [{r['tag']} {r['key']}] {r['base']} -> {r['new']} :: {r['text']}")
    print(collections.Counter(r["status"] for r in rows))
    if out_json:
        pathlib.Path(out_json).write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
