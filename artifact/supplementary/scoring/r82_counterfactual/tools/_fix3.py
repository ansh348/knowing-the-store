r"""_fix3.py -- three reported errors in the integrated build.

1. The one-third PN sentence describes the 36-question authorship-matched set but was left
   stranded after the 90-question counterfactual sentences by R82 diff 1, so "that set" had
   the wrong antecedent. It moves back above the insertion, next to the D.1 reference.
2. Appendix F.3 is a heading with nothing under it but one table, so when that table floated
   the heading was left alone at the foot of a page. The table is pinned with [H].
3. The two R82 rows in Appendix G carried 7-character commit hashes where every other row
   carries 10.
"""
# R83: anchors re-keyed from heading TEXT to \label{}. Retitling Appendix H broke
# _r82_int's guard because it keyed on the title; a heading is an identity key for prose,
# exemption tables AND splicer anchors, and only the label survives a rename.
import io
import pathlib
import sys

TEX = pathlib.Path(__file__).resolve().parents[2] / "iclr2027_monitoring_submission" / "paper_v2.tex"
NL = "\r\n"

MATCHED = ("On that set every slot carries the same one-third \\pn{} rate, and blind NOK is "
           "at chance for mini and Opus 5.")
D1_REF = ("balanced $36$-question set rewritten in one voice "
          "(Appendix~\\ref{app:matched}).")
F3 = "\\label{app:construction}" + NL + NL + "\\begin{table}[h]"
F3_NEW = "\\label{app:construction}" + NL + NL + "\\begin{table}[H]"


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()
    out = []

    # ---- 1. restore the antecedent
    if MATCHED in s and s.index(MATCHED) > s.index(D1_REF) + 400:
        s = s.replace(NL + MATCHED, "", 1)
        i = s.index(D1_REF) + len(D1_REF)
        s = s[:i] + NL + MATCHED + s[i:]
        out.append("1: the one-third sentence sits beside its D.1 reference again")
    else:
        out.append("1: already adjacent to its antecedent")

    # ---- 2. pin the F.3 table so the heading cannot be orphaned
    if F3 in s:
        s = s.replace(F3, F3_NEW, 1)
        out.append("2: F.3's table pinned with [H]")
    else:
        out.append("2: already pinned or anchor drifted")

    # ---- 3. hashes to the 10 characters every other row uses
    for short, full in (("3147a05", "3147a05adf"), ("ef351e9", "ef351e9be5")):
        old = "\\texttt{" + short + "}"
        if old in s:
            s = s.replace(old, "\\texttt{" + full + "}", 1)
            out.append(f"3: {short} -> {full}")

    io.open(TEX, "w", encoding="utf-8", newline="").write(s)
    for o in out:
        print("  " + o)
    return 0


if __name__ == "__main__":
    sys.exit(main())
