r"""_dedup_int.py -- remove the duplicated R82-INT insertions.

_r82_int.py replaced each anchor with anchor+insert, so re-running it matched the surviving
anchor and inserted a second copy. This removes the second copy of each block and leaves
exactly one. The script is a one-off repair; the guard added to _r82_int.py prevents the
duplication recurring.
"""
import io
import pathlib
import sys

TEX = pathlib.Path(__file__).resolve().parents[2] / "iclr2027_monitoring_submission" / "paper_v2.tex"
NL = "\r\n"

BLOCKS = [
    (NL + "% AUX-R82-CF-NOK, AUX-R82-CF-COUNTED, AUX-R82-CF-BASELINES" + NL +
     "On $90$ questions, each of $30$ asked of three versions of one store differing in a "
     "single attribute, a question-only reader scores $0.5000$ by construction. Naming the "
     "retracted and expired content raises the obligation judgment on those states from "
     "$0.5656$ to $0.8489$, and a match against the name lists reaches $0.7886$ against the "
     "monitor's $0.7656$ (Appendix~\\ref{app:counterfactual})."),
    (NL + "% AUX-R82-CF-INDIVIDUATION" + NL +
     "A self-description can only name what its scrubbing rule individuates, so naming "
     "granularity bounds what any reader can recover from the summary."),
]


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()
    for b in BLOCKS:
        n = s.count(b)
        if n > 1:
            s = s.replace(b + b, b, 1)
            print(f"collapsed {n} -> {s.count(b)}: {b.strip().splitlines()[-1][:56]}")
        elif n == 1:
            print(f"already single: {b.strip().splitlines()[-1][:56]}")
        else:
            sys.exit("STOP: block not found; nothing written")
    io.open(TEX, "w", encoding="utf-8", newline="").write(s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
