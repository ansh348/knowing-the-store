# -*- coding: utf-8 -*-
"""wp_vlines.py -- Phase 2 of the writing pass: every line of a carried paper_v11 block (the %%V11:a-b%% markers of body_v18.tex and
appendix_v18.tex) that holds a Phase 2 token, with its v11 line number and whether it is frozen registered text, so build_v18.py's
REPAIRS_R111 list can name each repair exactly. Usage: python reviews/v18/tools/wp_vlines.py"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "v18" / "tools"))
import wp_phase2 as P  # noqa: E402

TOKS = ["smallest model", "larger model", r"\\believed\{\}", r"\\trueidx\{\}", "truthful", "Truthful", "individuat", "the author",
        "The author", "user profile", "profile interval", "profile-grouped", "the lookup", "uperseded-names lookup", "tallies", "tally",
        "the join", "the marks", "lifecycle store", "increment moved", "reviewer", "the matcher"]


def main():
    v11 = (ROOT / "iclr2027_monitoring_submission" / "paper_v11.tex").read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    seen = set()
    for name in ("body_v18.tex", "appendix_v18.tex"):
        for ln in (P.SRC / name).read_text(encoding="utf-8").split("\n"):
            m = re.fullmatch(r"%%V11:(\d+)-(\d+)%%", ln)
            if not m:
                continue
            a, b = int(m.group(1)), int(m.group(2))
            for k in range(a - 1, b):
                l = v11[k]
                if l.lstrip().startswith("%"):
                    continue
                text = re.sub(r"(?<!\\)%.*$", "", l)
                hits = [t for t in TOKS if re.search(t, text)]
                if hits and k not in seen:
                    seen.add(k)
                    print(f"v11 L{k + 1:5d} {'FROZEN' if P.is_frozen(v11, k) else '      '} [{', '.join(hits)}]")
                    print(f"      {text.strip()[:420]}")


if __name__ == "__main__":
    main()
