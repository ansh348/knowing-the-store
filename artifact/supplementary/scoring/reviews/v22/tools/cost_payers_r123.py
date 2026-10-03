# -*- coding: utf-8 -*-
"""cost_payers_r123.py -- program R123, Phase E: cost each payer candidate of the brief on a scratch build (the fine number of run_gates'
raggedbottom diagnostic, the label page), applying the candidate to the committed sources, building, reading, and restoring the sources
with git checkout. Nothing is landed; the author chooses. Candidates: rw2 (the second Related Work paragraph tightened), s6p2 (Section 6's
second paragraph moved whole to Appendix E.10), notation2 (two notation rows dropped: gain, and route A / route B), and their combinations.
Usage: python reviews/v21/tools/cost_payers_r123.py
"""
from __future__ import annotations

import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
SRC = ROOT / "reviews" / "v21" / "src"
BODY = SRC / "body_v21.tex"
APPX = SRC / "appendix_v21.tex"
sys.path.insert(0, str(ROOT / "reviews" / "v21" / "tools"))
import run_gates as RG  # noqa: E402

RW2_OLD = ("Adaptive retrieval, abstention and calibration each decide something before or about an answer, and none has an external store to be right about.\n"
           "Adaptive retrieval decides whether to query a static corpus from parametric or generated-content signals \\citep{lewis2020,flare,mallen2023,ren2025,wang2023,selfrag,su2024,seakr,verbrouting,metamem}, abstention benchmarks score whether a question admits an answer \\citep{rajpurkar2018,kamath2020,yang2024,abstentionbench}, and calibration work scores confidence in an answer \\citep{kadavath2022,lin2022,tian2023,xiong2024}.\n"
           "Those that retrieve observe a bounded view rather than a maintained summary (Section~\\ref{sec:framework}).\n")
RW2_NEW = ("Adaptive retrieval decides whether to query a static corpus from parametric or generated-content signals \\citep{lewis2020,flare,mallen2023,ren2025,wang2023,selfrag,su2024,seakr,verbrouting,metamem}, abstention benchmarks score whether a question admits an answer \\citep{rajpurkar2018,kamath2020,yang2024,abstentionbench}, and calibration work scores confidence in an answer \\citep{kadavath2022,lin2022,tian2023,xiong2024}.\n"
           "None has an external store to be right about, and those that retrieve observe a bounded view rather than a maintained summary (Section~\\ref{sec:framework}).\n")

S6P2_HEAD = "Per state the two routes are mirror images.\n"
S6P2_TAIL = "% AUX-RESP-RETRIEVED, AUX-RESP-HYBRID, AUX-RESP-A1-H45-HYBRID (0.7863), -H45-RETRIEVED (0.7134)\n"
S6P2_ANCHOR = "\\paragraph{The tagged view under the store's own tags, and Haiku 4.5 on the retrieved-view monitors.}\n"

NOTATION_ROWS = [
    "gain ($\\Delta$) & the indexed score minus the blind score on the same questions; on the counterfactual set the blind score is $0.50$ by construction, so there the AUROC and the gain carry the same information \\\\\n",
    "route A; route B & the summary route, read before any retrieval; the tag route, retrieval without a mask whose returned records keep their tags, read at retrieval time (Figure~\\ref{fig:framework}) \\\\\n",
]


CAP_OLD_HEAD = "\\caption{Reach on the full obligation set. Columns:"
CAP_NEW = ("\\caption{Reach on the full obligation set: the forbidding record in view for the $104$ obligations, the mean lines per question over the $661$ questions (the matched rows' shared budget; over the $104$ obligations alone the gated views average about seven lines), and the licensed record in view for the $174$ licensed items (Appendix~\\ref{app:resp}).}\n")


def tab3short(body):
    """Candidate: the Section 9 reach table's caption cut to one sentence and its row padding 0.85 (the table currently floats to the top of page 9
    and leaves the foot of page 8 empty)."""
    i = body.index(CAP_OLD_HEAD); j = body.index("}\n", body.index("no answer is scored here.", i)) + 2
    body = body[:i] + CAP_NEW + body[j:]
    old = "\\centering\\scriptsize\\setlength{\\tabcolsep}{4pt}\\renewcommand{\\arraystretch}{0.9}\n\\begin{tabular}{@{}lrrrr@{}}"
    assert body.count(old) == 1
    return body.replace(old, old.replace("0.9", "0.85"))


def apply(name):
    body = BODY.read_text(encoding="utf-8"); appx = APPX.read_text(encoding="utf-8")
    if "tab3short" in name:
        body = tab3short(body)
    if "tab3top" in name:      # candidate: the reach table placed [t], so it can sit at the top of the page it is met on instead of floating past the barrier
        old_t = "%% R123: tab:reach (the Section 9 reach table)"
        k = body.index(old_t); k2 = body.index("\\begin{table}[h]", k)
        body = body[:k2] + "\\begin{table}[t]" + body[k2 + len("\\begin{table}[h]"):]
    if "tab3first" in name:    # candidate: the reach table's source moved to just after Section 9's heading, so [h] can place it on the page it is met on
        old_t = "%% R123: tab:reach (the Section 9 reach table)"
        k = body.index(old_t); k2 = body.index("\\end{table}\n", k) + len("\\end{table}\n")
        tbl = body[k:k2]
        body = body[:k] + body[k2:].lstrip("\n")
        first = "Acting on the judgment changes what the agent sees; whether it changes what the agent answers is not established here.\n"
        assert body.count(first) == 1
        body = body.replace(first, tbl + "\n" + first)
    if "tab3appendix" in name:  # candidate: the reach table moved whole to Appendix E.10 (before tab:gatereach), the body keeping a pointer
        old_t = "%% R123: tab:reach (the Section 9 reach table)"
        k = body.index(old_t); k2 = body.index("\\end{table}\n", k) + len("\\end{table}\n")
        tbl = body[k:k2].replace("\\begin{table}[h]", "\\begin{table}[H]")
        body = body[:k] + body[k2:].lstrip("\n")
        body = body.replace("and the fetch reaches $0.82$ (Table~\\ref{tab:reach}).", "and the fetch reaches $0.82$ (Table~\\ref{tab:reach}, Appendix~\\ref{app:resp}).")
        anchor = "\\paragraph{What the gate buys, reach only.}\n"
        assert appx.count(anchor) == 1
        appx = appx.replace(anchor, anchor + tbl + "\n")
    if "rw2" in name:
        assert body.count(RW2_OLD) == 1; body = body.replace(RW2_OLD, RW2_NEW)
    if "s6p2" in name:
        i = body.index(S6P2_HEAD); j = body.index(S6P2_TAIL, i) + len(S6P2_TAIL)
        para = body[i:j]
        body = body[:i] + body[j:]
        assert appx.count(S6P2_ANCHOR) == 1
        appx = appx.replace(S6P2_ANCHOR, "\\paragraph{The two routes per state.}\n%% Section 6's second paragraph, moved whole.\n" + para + "\n" + S6P2_ANCHOR)
    if "notation2" in name:
        for r in NOTATION_ROWS:
            assert body.count(r) == 1, r[:40]; body = body.replace(r, "")
    io.open(BODY, "w", encoding="utf-8", newline="\n").write(body)
    io.open(APPX, "w", encoding="utf-8", newline="\n").write(appx)


def restore():
    subprocess.run(["git", "checkout", "--", str(BODY.relative_to(ROOT)), str(APPX.relative_to(ROOT))], cwd=ROOT, check=True)


def build_and_read():
    out = subprocess.run([sys.executable, str(ROOT / "reviews" / "v21" / "tools" / "build_v21.py")], cwd=ROOT, capture_output=True, text=True)
    assert out.returncode == 0, out.stdout[-500:] + out.stderr[-500:]
    RG.pdflatex("paper_v21", SUB)
    rb, page_no, where = RG.raggedbottom_reading()
    return rb, page_no, where


def main():
    restore()
    rows = []
    rb0, p0, w0 = build_and_read()
    rows.append(("as committed (50b99d6)", rb0, p0, w0))
    for name in ("rw2", "s6p2", "notation2", "rw2+notation2", "rw2+s6p2", "s6p2+notation2", "rw2+s6p2+notation2",
                 "tab3short", "tab3short+s6p2", "tab3short+rw2+s6p2", "tab3short+s6p2+notation2", "tab3short+rw2+s6p2+notation2",
                 "tab3appendix", "tab3appendix+rw2", "tab3appendix+notation2"):
        apply(name)
        try:
            rb, p, w = build_and_read()
        finally:
            restore()
        rows.append((name, rb, p, w))
    build_and_read()
    print(f"{'candidate':28s} {'fine number':>11s} {'against 485':>11s} {'label page':>10s}  AI-use statement")
    for name, rb, p, w in rows:
        print(f"{name:28s} {rb:11d} {485 - rb:+11d} {p:10d}  {w}")


if __name__ == "__main__":
    main()
