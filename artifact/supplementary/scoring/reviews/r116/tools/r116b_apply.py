# -*- coding: utf-8 -*-
"""r116b_apply.py -- R116, the author's rulings of 19 September 2026 on REPORT_R116 / PHASE0_REPORT item 6:
(3) the app:resp sentence restored and the exception put on table b's caption; (4) the harness disclosure paragraph in Appendix B,
the row marker $^{h}$ at every listed site (tab:ladder-exact, tab:ladder-predictions, tab:inversion, tab:runs, Section 7), tab:runs'
"provider default" corrected for the harness rows, the Sol / Luna price constants printed in E.11. The Section 4 body pointer is NOT
applied here (its page cost is measured on a scratch copy and reported first; --pointer builds that copy's source into the scratchpad).

Same contract as r116_apply.py: each OLD occurs exactly once, LF preserved, idempotent, --check reports without writing. Carried v11
tables are edited through REPAIRS_R116_BLOCK in build_v19.py (block-keyed, asserted to their counts).
"""
from __future__ import annotations

import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v19" / "src"
BUILD = ROOT / "reviews" / "v19" / "tools" / "build_v19.py"
APPX, BODY = SRC / "appendix_v19.tex", SRC / "body_v19.tex"

HARNESS = (
    "%% R116 (2026-09-19, the author's ruling on the harness rows; reviews/r117/PHASE0_REPORT.md item 6; reviews/NUMBERS_R116.md AUX-R116-HARNESS): the transport disclosure and the row marker.\n"
    "The GPT-5.6 Luna and GPT-5.6 Sol rows on the cross-model set and on the pooled $66$ structureless questions, marked $^{h}$ here and in Tables~\\ref{tab:ladder-predictions}, \\ref{tab:inversion} and~\\ref{tab:runs}, were elicited in August through the vendor's command-line coding agent (\\texttt{codex exec}, reasoning effort low, ephemeral sessions, subscription-billed), which prepends its own system text and tool schemas and passes the frozen system and user texts to the model as one flattened user turn.\n"
    "No token telemetry survives those runs.\n"
    "When the expansion tried to complete GPT-5.6 Sol through the same agent, two twelve-call probe gates returned no parseable reply, $0$ of $12$ and $0$ of $12$ (the expansion's deviation ledger), so the agent transport is not one condition with the raw API; the same models' rows on the full populations are raw API calls under the provider default.\n"
    "\n"
)

E11 = (
    "%% R116 (2026-09-19): the price constants behind the two frontier lanes of the expansion (r74/tools/x4_run.py LANES; r74/NUMBERS_R74.md X4) and OpenAI's model pages of 18 September 2026 (reviews/NUMBERS_R116.md AUX-R116-PRICES).\n"
    "GPT-5.6 Luna and GPT-5.6 Sol on the full populations were metered at $0.20$ and $1.20$, and at $5$ and $30$, dollars per million input and output tokens, the constants of the expansion's lane code, to $2.67$ and $12.39$, the Sol run stopped; OpenAI's model pages of 18 September 2026 list $0.20$ and $1.20$ for Luna and $4$ and $20$ for Sol, with the first send of a long prompt billed at $1.25$ times the input rate, so the recorded figures are metered estimates rather than invoices.\n"
)

EDITS = [
    # ruling 3: the app:resp sentence restored
    (APPX,
     "Each was preregistered with its texts written before any call (Table~\\ref{tab:registrations-b}), by commit except DS Amendment 4 and Graphiti Amendment 2, which hold by the runner's record, so every outcome below is read against a text that predates it.",
     "Each was preregistered with its texts written before any call (Table~\\ref{tab:registrations-b}), so every outcome below is read against a text that predates it."),
    # ruling 3: the exception on table b's caption
    (APPX,
     "\\caption{The registration record, continued: the side experiments, the powered counterfactual set, the mechanism tests and the downstream experiment; the Outcome column lists each prediction's outcome.}",
     "\\caption{The registration record, continued: the side experiments, the powered counterfactual set, the mechanism tests and the downstream experiment; the Outcome column lists each prediction's outcome. Every row was committed before its first call except DS Amendment 4 and Graphiti Amendment 2, which are attested by the runner's lock (file hashes shown).}"),
    # ruling 4: the disclosure paragraph before the carried ladder table
    (APPX,
     "\n%%V11:913-943%%\n",
     "\n" + HARNESS + "%%V11:913-943%%\n"),
    # ruling 4: tab:runs, the two harness rows and the caption's marker definition
    (APPX,
     "GPT-5.6 Luna & OpenAI & not run & ran & ran & ran & five calls, provider default \\\\",
     "GPT-5.6 Luna & OpenAI & not run & ran & ran & ran$^{h}$ & five calls, provider default; the cross-model set through the agent harness at reasoning effort low \\\\"),
    (APPX,
     "GPT-5.6 Sol & OpenAI & not run & stopped at the budget & stopped at the budget & ran & five calls \\\\",
     "GPT-5.6 Sol & OpenAI & not run & stopped at the budget & stopped at the budget & ran$^{h}$ & five calls, through the agent harness at reasoning effort low \\\\"),
    (APPX,
     "\\caption{Run coverage, model by question set, in the words of the run records. Two runs stopped at the budget on the full populations, so their complete rows are on the cross-model set; three models ran on the counterfactual set.}",
     "\\caption{Run coverage, model by question set, in the words of the run records. Two runs stopped at the budget on the full populations, so their complete rows are on the cross-model set; three models ran on the counterfactual set. $^{h}$: elicited through the vendor's agent harness rather than the raw API (Appendix~\\ref{app:laddertable}).}"),
    # ruling 4: E.11, the price constants
    (APPX,
     "under a $40$ ceiling for that pass.\n",
     "under a $40$ ceiling for that pass.\n" + E11),
    # ruling 4: the Section 7 site (a listed site; the marker only)
    (BODY,
     "GPT-5.6 Luna loses $0.34$ and GPT-5.6 Sol $0.10$, every interval excluding zero.",
     "GPT-5.6 Luna loses $0.34$ and GPT-5.6 Sol $0.10$, every interval excluding zero$^{h}$."),
    # the carried tables: block-keyed repairs
    (BUILD,
     "REPAIRS_R116_BLOCK = {\n    (2084, 2118): [('\\\\texttt{2bb7fd9dc4}', '\\\\texttt{5c3621b75e}', 1)],\n}\n",
     "REPAIRS_R116_BLOCK = {\n    (2084, 2118): [('\\\\texttt{2bb7fd9dc4}', '\\\\texttt{5c3621b75e}', 1)],\n"
     "    # R116 (2026-09-19, the author's ruling on the harness rows): the marker $^{h}$ on every GPT-5.6 Luna / Sol row elicited through the\n"
     "    # vendor's agent harness (the August ladder runs), defined in the Appendix B paragraph before tab:ladder-exact. These rules run on the\n"
     "    # R112 output (the row labels already read 'GPT-5.6 Luna' / 'GPT-5.6 Sol').\n"
     "    (913, 943): [('GPT-5.6 Luna & FOK & $84$', 'GPT-5.6 Luna$^{h}$ & FOK & $84$', 1), ('GPT-5.6 Luna & NOK & $84$', 'GPT-5.6 Luna$^{h}$ & NOK & $84$', 1),\n"
     "                 ('GPT-5.6 Sol & FOK & $84$', 'GPT-5.6 Sol$^{h}$ & FOK & $84$', 1), ('GPT-5.6 Sol & NOK & $84$', 'GPT-5.6 Sol$^{h}$ & NOK & $84$', 1),\n"
     "                 ('while mini is the original primary elicitation.', \"while mini is the original primary elicitation; $^{h}$ marks the rows elicited through the vendor's agent harness (the paragraph above).\", 1)],\n"
     "    (980, 997): [('stratified set, $n=150$ per model', 'stratified set$^{h}$, $n=150$ per model', 1), ('stratified set, $n=150$ & failed', 'stratified set$^{h}$, $n=150$ & failed', 1),\n"
     "                 ('cross-model set, $n=84$', 'cross-model set$^{h}$, $n=84$', 3)],\n"
     "    (1575, 1766): [('GPT-5.6 Sol & external pooled & $66$', 'GPT-5.6 Sol$^{h}$ & external pooled & $66$', 1), ('GPT-5.6 Luna & external pooled & $66$', 'GPT-5.6 Luna$^{h}$ & external pooled & $66$', 1)],\n"
     "}\n"),
]

POINTER_OLD = "and GPT-5.6 Sol and Kimi K3 ran the cross-model set only (Table~\\ref{tab:setup})."
POINTER_NEW = "and GPT-5.6 Sol and Kimi K3 ran the cross-model set only (Table~\\ref{tab:setup}); the GPT-5.6 cross-model rows are harness rows (Appendix~\\ref{app:laddertable})."


def apply(edits, check):
    texts = {}
    for p, old, new in edits:
        t = texts.get(p)
        if t is None:
            raw = p.read_bytes()
            assert b"\r\n" not in raw, f"{p}: CRLF source, refusing"
            t = raw.decode("utf-8")
        n_old, n_new = t.count(old), t.count(new)
        if n_new == 1:
            print(f"  already applied : {p.name}: {new[:70]!r}")
        elif n_new == 0 and n_old == 1:
            print(f"  {'would apply' if check else 'applied'}     : {p.name}: {old[:70]!r}")
            if not check:
                t = t.replace(old, new)
        else:
            raise SystemExit(f"ANCHOR NOT UNIQUE ({n_old} old, {n_new} new) in {p}: {old[:90]!r}")
        texts[p] = t
    return texts


def main():
    check = "--check" in sys.argv
    if "--pointer" in sys.argv:       # the Section 4 pointer on a scratch copy of the body source, for the page-cost reading only
        out = pathlib.Path(sys.argv[sys.argv.index("--pointer") + 1])
        t = BODY.read_text(encoding="utf-8")
        assert t.count(POINTER_OLD) == 1
        out.write_text(t.replace(POINTER_OLD, POINTER_NEW), encoding="utf-8", newline="\n")
        print("pointer copy written:", out)
        return
    texts = apply(EDITS, check)
    if not check:
        for p, t in texts.items():
            io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("r116b_apply:", "check only" if check else "written", f"({len(EDITS)} edits over {len(texts)} files)")


if __name__ == "__main__":
    main()
