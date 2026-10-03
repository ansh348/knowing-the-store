# -*- coding: utf-8 -*-
"""changes_r131_close.py -- writes reviews/v22/R131_CLOSE_CHANGES.md: every sentence changed since the R131 checkpoint 9b1b1ed, old beside new with
its reason, in one file (the author's request at the close). The pairs are read from the landing tools' own constants (port_r131_close.py,
appendix_r131_close.py, port_r131_w.py), so nothing is retyped. Usage: python reviews/v22/tools/changes_r131_close.py [--w-skip=3]
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
V22 = ROOT / "reviews" / "v22"
OUT = V22 / "R131_CLOSE_CHANGES.md"
sys.path.insert(0, str(V22 / "tools"))
import port_r131_close as C  # noqa: E402
import appendix_r131_close as A  # noqa: E402
import port_r131_w as W  # noqa: E402
import report_r131_close as R  # noqa: E402  (ABS_OLD)


def flat(t):
    return " ".join(l for l in t.strip().split("\n") if not l.startswith("%%")).replace("\n", " ").strip()


def cell(t):
    return flat(t).replace("|", "\\|") if t.strip() else "(none)"


def main():
    skip = {int(x) for x in next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--w-skip=")), "").split(",") if x.strip()}
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        A.G.main()
    prov = A.prov_paragraph(A.G.PROV)
    rows = []
    # the close (port_r131_close.py), in the order the tool applies them
    rows.append(("B1", "Abstract", R.ABS_OLD, C.ABS_NEW, "the author's abstract, verbatim (ABSTRACT SWAP); hand-tuned, no gate changed a word (B4); the last clause a placeholder until HV-1"))
    rows += [
        ("L4", "Section 4", C.L4_OLD, C.L4_NEW, "'(open weights)' at the first mention of Kimi K3 (the authors' assertion)"),
        ("A1'", "Section 4", C.A1_OLD, C.A1_NEW, "the provenance sentences, third person for the release; the Graphiti clause corrected to the released FR-Bank records"),
        ("L1", "Limitations", C.L1_OLD, C.L1_NEW, "the author's two sentences; 40 verified against the bank"),
        ("L2", "Limitations", C.L2_OLD, C.L2_NEW, "'completed only the cross-vendor replication'; the open-weights assertion"),
        ("L3", "Limitations", C.L3_OLD, C.L3_NEW, "cut; C.2 prints the within-0.02 result and Luna's margin"),
        ("A2'", "AI-use statement", C.A2_OLD, C.A2_NEW, "the author's statement with the verified Graphiti clause"),
        ("A5", "AI-use statement", C.A5_OLD, C.A5_NEW, "'preregistered,' dropped"),
        ("1A", "Table 1's caption", C.TAB1_CAP_OLD.rstrip("}"), C.TAB1_CAP_NEW.rstrip("}"), "the four-word note on the four-decimal difference sub-table"),
        ("1B", "the builders box", C.BOX_OLD, C.BOX_NEW, "the all-states clause in the author's words"),
        ("payer 5", "Section 5.1", C.P5_PAR, "", "the target-name paragraph out; E.10 tab:resp-l1 prints 0.8572 -> 0.5310 and 0.8897 -> 0.6759"),
        ("payer 5", "Section 5.1", C.P5_PTR_OLD, C.P5_PTR_NEW, "the pointer in the adjacent paragraph"),
        ("payer 5b", "Conclusion", C.P5B_OLD, C.P5B_NEW, "the author's sentence"),
        ("payer 6, P6a", "Section 5.3", C.P6A_OLD, "", "deleted; tab:cf-intent's caption says the body reads the draw-1 column"),
        ("payer 6, P6b", "Section 5.3", C.P6B_OLD, C.P6B_NEW, "the Sol sentence deleted; the caption carries 9 of 11"),
        ("payer 6, P6c", "Section 5.3", C.P6C_OLD, C.P6C_NEW, "the author's one sentence for two"),
        ("payer 6, P6d", "Section 5.3", C.P6D_OLD, C.P6D_NEW, "the tolerance sentence deleted; the caption prints the largest fall"),
        ("payer 7", "Figure 3", C.P7_OLD, C.P7_NEW, "height 5.0cm -> 4.5cm; rendered: no overlap near the 0.86 to 0.88 band"),
        ("payer 8", "Section 5.2", C.P8_OLD, C.P8_NEW, "two sentences after the lead"),
        ("payer B2", "Section 1", C.B2_OLD, C.B2_NEW, "the findings paragraph cut to two sentences"),
        # the appendix
        ("A1''", "Appendix E.3", "", prov, "the provenance paragraph, every count from the tree (AUX-R131-CLOSE-PROV)"),
        ("A3 follow-up", "Appendix E.9", A.E9_OLD, A.E9_NEW, "the earlier ingestion attributed to the release in the third person"),
        ("A5", "Appendix B", A.B_OLD, A.B_NEW, "'registered' (unpinned section)"),
        ("A5", "Appendix E.4", A.E4_OLD, A.E4_NEW, "'registered' (unpinned section)"),
        ("A5", "Appendix E.4, tab:cluster-sensitivity's caption", "reports the preregistered item-level interval", "reports the registered item-level interval", "REPAIRS_R131CLOSE_BLOCK"),
        # the page 8-9 payers
        ("W1", "Section 8", W.W1A_OLD, W.W1A_NEW, "the pointer joins the line above (W1b not needed)"),
        ("W2", "Limitations, paragraph 1", W.W2_OLD, W.W2_NEW, "two sentences -> one"),
    ]
    if 3 in skip:
        rows.append(("W3 (withdrawn pending the ruling)", "Limitations, paragraph 3", W.W3_OLD, W.W3_NEW, "the author's sentence opens its paragraph on the numeral 22 and trips q_scan Q-A; not applied; the R131 split stands; W3 bought no line"))
    else:
        rows.append(("W3", "Limitations, paragraph 3", W.W3_OLD, W.W3_NEW, "two sentences -> one (Q-A exempted by ruling)"))
    rows += [
        ("W4", "Section 7, the tested-rule paragraph", W.W4_OLD, W.W4_NEW, "the third sentence, which repeated the bold lead, folded into the second"),
        ("W5a", "Limitations, paragraph 2", W.W5A_OLD, W.W5A_NEW, "trim"),
        ("W5b", "Limitations, paragraph 2", W.W5B_OLD, W.W5B_NEW, "trim; the one-rewording design stays in C.2; replaced on 22 Sep"),
        ("W6", "Conclusion", W.W6_OLD, W.W6_NEW, "the all-states clause deleted (still short of +2); Section 5.2 keeps the Opus result"),
        ("W7", "Section 8, second paragraph", W.W7_OLD, W.W7_NEW, "the last sentence deleted (still short of +2); C.2 prints the intervals"),
        ("W7", "Appendix E.8", "", W.W7_APPX_NEW[len(W.W7_APPX_ANCHOR):], "the pointer sentence, so E.8 prints the claim the body dropped"),
    ]
    L = ["# R131_CLOSE_CHANGES.md — every sentence changed since the R131 checkpoint `9b1b1ed`, old beside new, with its reason (2026-09-20)\n\n",
         "In the order the tools apply them: the close (`port_r131_close.py`, `appendix_r131_close.py`, `build_v22.py` REPAIRS_R131CLOSE_BLOCK), then the page 8-9 payers (`port_r131_w.py`). "
         "Every pair is read from the tools' own constants. Rulings recorded beside the texts: rule D's abstract / Section 1 thesis pair overridden (prose_scan WHITELIST, B4); rule V not fired; G2 kept under its pattern reading; "
         "the only gate trip on a W text is Q-A on W3 (reported, not reworded).\n\n",
         "| item | where | before | after | reason |\n|---|---|---|---|---|\n"]
    for item, where, old, new, why in rows:
        L.append(f"| {item} | {where} | {cell(old)} | {cell(new)} | {why} |\n")
    OUT.write_text("".join(L), encoding="utf-8", newline="\n")
    print("->", OUT, len(rows), "rows")


if __name__ == "__main__":
    main()
