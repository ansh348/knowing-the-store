r"""_fix_d2.py -- move the store-counterfactual subsection from Appendix F into Appendix D.

_r82_int.py inserted it before the next \subsection after the authorship-matched cell.
Appendix D has only that one subsection, so "the next subsection" was Appendix F's first and
the block landed in F. It belongs beside the authorship-matched cell as D.2, which is where
the order puts it and where the two construction-control cells sit together.
"""
# R83: anchors re-keyed from heading TEXT to \label{}. Retitling Appendix H broke
# _r82_int's guard because it keyed on the title; a heading is an identity key for prose,
# exemption tables AND splicer anchors, and only the label survives a rename.
import io
import pathlib
import sys

TEX = pathlib.Path(__file__).resolve().parents[2] / "iclr2027_monitoring_submission" / "paper_v2.tex"
NL = "\r\n"
HEAD = r"\subsection{Store-counterfactual cell}\label{app:counterfactual}"
DEST = r"\label{app:ledger}"


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()
    if HEAD not in s:
        sys.exit("STOP: store-counterfactual subsection not found")
    a = s.index(HEAD)
    # the block runs to the next section or subsection heading
    nxt = min(x for x in (s.find(NL + r"\section{", a + 10),
                          s.find(NL + r"\subsection{", a + 10)) if x > 0)
    block = s[a:nxt].rstrip(NL + " ")
    # correct placement is BEFORE the instrument ledger, i.e. still inside Appendix D
    if a < s.index(DEST):
        print("already in Appendix D")
        return 0
    s = s[:a] + s[nxt:].lstrip(NL)
    d = s.index(DEST)
    s = s[:d] + block + NL + NL + s[d:]
    io.open(TEX, "w", encoding="utf-8", newline="").write(s)
    print(f"moved {len(block)} chars into Appendix D, before the instrument ledger")
    return 0


if __name__ == "__main__":
    sys.exit(main())
