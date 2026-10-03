"""a1_apply.py -- review-2 A1 under the author's ruling of 2026-09-15 (program R112): the constrained rendering.

Rewrites reviews/v19/src/body_v19.tex and appendix_v19.tex in place by asserted replacements (each old string must occur
exactly once). The carried-block sites are REPAIRS_R112 in build_v19.py. Idempotent: a site already applied is skipped
with a note. Flags choose the ruling's conditional forms:

  --box              add the term to the notation box's ground-truth/store-written row (only if the row does not wrap:
                     build with and without and compare the fine number; the ruling)
  --t1=header        Table 1's FOK-panel header names both renderings (default; "if it fits on one line")
  --t1=footnote      the caption clause instead
  --swap             move Section 7's Mem0 history-call sentence to Appendix E.9 (only if the page gate needs it; the ruling)
  --undo-box / --undo-swap  reverse those two

Numbers: AUX-WP-A1-BELIEVED-BLIND (reviews/NUMBERS_WP.md section 6; reviews/v19/results/believed_blind_a1.json).
"""
from __future__ import annotations

import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v19" / "src"
BODY = SRC / "body_v19.tex"
APPX = SRC / "appendix_v19.tex"


def read(p):
    return io.open(p, encoding="utf-8").read()


def write(p, s):
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def rep(text, old, new, label):
    # "already applied" is decided on the new text first, because several new texts extend their old text (the definition
    # after its sentence, the E.7 sentences after their anchor), so the old text is still present once the site is applied
    if new and new != old and new not in old and text.count(new) >= 1:
        print(f"  [{label}] already applied")
        return text
    k = text.count(old)
    assert k == 1, f"[{label}] expected exactly one occurrence, found {k}"
    print(f"  [{label}] applied")
    return text.replace(old, new)


# ---------------------------------------------------------------- body
DEF_OLD = ("A ground-truth summary is built from ground truth and a store-written summary from the fields the backend itself exposes, "
           "rendered by the same code with a cap of fifteen names per list.\n")
DEF_NEW = DEF_OLD + (
    "%% R112 (2026-09-15), review-2 A1 (the author's ruling): the term defined once; on Mem0 and A-MEM the TRUE index is the manifest rendered\n"
    "%% under the backend's constraints (e1_metamemory/indexes_v2.json meta.availability). reviews/v19/A1_CONSTRAINED_RENDERING.md.\n"
    "On Mem0 and A-MEM, which carry no categories or attribute names, the ground-truth summary is the manifest rendered under the backend's "
    "constraints: exact lifecycle totals, every name section printed as not expressible.\n"
    "We call it the constrained rendering (Appendix~\\ref{app:inversion}).\n")

S7_OLD = (
    "On the two structureless stores a summary that names what they hold restores coverage, and the summary they can write loses it at every scale.\n"
    "A name-bearing summary rebuilt from ground truth restores coverage from $0.45$ to $0.90$ on A-MEM and from $0.48$ to $0.88$ on Mem0, so the loss belongs to the summary these stores write.\n"
    "Under that summary GPT-4.1 mini loses $0.10$ on Mem0 and $0.11$ on A-MEM, and on the pooled $66$ questions of both stores GPT-5.6 Luna loses $0.34$ and GPT-5.6 Sol $0.10$, every interval excluding zero.\n")
S7_NEW = (
    "%% R112 (2026-09-15), review-2 A1 (the author's ruling): the loss is on the constrained rendering; the store-written sentence's phrasing from\n"
    "%% AUX-WP-A1-BELIEVED-BLIND (reviews/NUMBERS_WP.md section 6: Mem0 -0.0005, A-MEM -0.0313, both intervals include zero, |delta| <= 0.05).\n"
    "On the two structureless stores the constrained rendering loses coverage at every scale, and a summary that names what they hold restores it.\n"
    "Under the constrained rendering GPT-4.1 mini loses $0.10$ on Mem0 and $0.11$ on A-MEM, and on the pooled $66$ questions of both stores GPT-5.6 Luna loses $0.34$ and GPT-5.6 Sol $0.10$, every interval excluding zero.\n"
    "The summaries the stores themselves write are within tolerance of blind, $0.57$ against $0.57$ on Mem0 and $0.53$ against $0.56$ on A-MEM (Appendix~\\ref{app:inversion}).\n"
    "A name-bearing summary rebuilt from ground truth restores coverage to $0.90$ on A-MEM and $0.88$ on Mem0, so what the constrained rendering loses is the names.\n")

T1_HDR_OLD = "Backend & $n$ / pos. & Blind & \\hd{Indexed}{(ground-truth summary)} & $\\Delta$ & item interval & persona interval \\\\\n"
T1_HDR_NEW = "Backend & $n$ / pos. & Blind & \\hd{Indexed}{(ground-truth; constrained on Mem0, A-MEM)} & $\\Delta$ & item interval & persona interval \\\\\n"
T1_CAP_OLD = "coverage by backend for GPT-4.1 mini (positives non-\\absent{})"
T1_CAP_NEW = "coverage by backend for GPT-4.1 mini (positives non-\\absent{}; the Mem0 and A-MEM rows under the constrained rendering, Section~\\ref{sec:setup})"

BOX_OLD = ("ground-truth summary; store-written summary & the summary built from ground truth; the summary built from the fields the backend itself exposes \\\\\n")
BOX_NEW = ("ground-truth summary; store-written summary & the summary built from ground truth; the summary built from the fields the backend itself exposes; "
           "on Mem0 and A-MEM the ground-truth summary is the constrained rendering \\\\\n")

HIST = ("Its per-memory history call, which keeps the prior text under a known identifier, was not consulted, so the erase reading is of the record as exposed and says nothing about the history log.\n")
HIST_E9_ANCHOR = "The manifests record $40$ retraction events, one per persona, and the ground-truth join resolves $9$ of them to a retracted entry ($23$ entries).\n"
HIST_E9 = ("%% R112 (2026-09-15), review-2 A1: the Section 7 history-call sentence, moved here as the page swap the ruling named.\n"
           "Mem0's per-memory history call, which keeps the prior text under a known identifier, was not consulted, so the erase reading is of the record as exposed and says nothing about the history log.\n")

# ---------------------------------------------------------------- appendix
E1_OLD = "\\textsc{true} (the truthful summary) & the ground-truth summary \\\\\n"
E1_NEW = "\\textsc{true} (the truthful summary) & the ground-truth summary; on Mem0 and A-MEM, the constrained rendering \\\\\n"

E7_ANCHOR = "What triggers the compression is unresolved, and the ablations that narrowed it follow.\n"
E7_NEW = E7_ANCHOR + (
    "%% R112 (2026-09-15), review-2 A1 (the author's ruling): the constrained rendering named where the verbatim summaries show it;\n"
    "%% the store-written deltas and intervals are AUX-WP-A1-BELIEVED-BLIND (reviews/NUMBERS_WP.md section 6; reviews/v19/results/believed_blind_a1.json).\n"
    "On these two stores the ground-truth summary is the constrained rendering: the manifest's lifecycle totals, with every name section printed as not expressible (the verbatim summaries below).\n"
    "The store-written summary carries the store's own fields alone, a superseded count on Mem0 and recency on A-MEM.\n"
    "The loss is measured on the constrained rendering.\n"
    "The store-written summary is within tolerance of blind: $-0.0005$ on Mem0, intervals $[-0.0663,+0.0644]$ item-level and $[-0.0672,+0.0635]$ persona-grouped, and $-0.0313$ on A-MEM, $[-0.0983,+0.0400]$ and $[-0.0798,+0.0208]$ (Table~\\ref{tab:baselines}).\n")

APPX_RENAMES = [
    ("Indexed under the ground-truth summary it takes five values", "Indexed under the constrained rendering it takes five values", "E.7 dist prose"),
    ("blind against indexed under the ground-truth summary, from the recorded rows", "blind against indexed under the constrained rendering, from the recorded rows", "tab:dist caption"),
    ("The monitor's indexed point estimates under the ground-truth summary fall below them", "The monitor's indexed point estimates under the constrained rendering fall below them", "E.8 sentence"),
]


def main(argv):
    box = "--box" in argv
    undo_box = "--undo-box" in argv
    swap = "--swap" in argv
    undo_swap = "--undo-swap" in argv
    t1 = "footnote" if "--t1=footnote" in argv else "header"

    body = read(BODY)
    print("body_v19.tex")
    body = rep(body, DEF_OLD, DEF_NEW, "Section 4 definition (a)")
    body = rep(body, S7_OLD, S7_NEW, "Section 7 paragraph (b)")
    if t1 == "header":
        body = rep(body, T1_HDR_OLD, T1_HDR_NEW, "Table 1 header (c, header form)")
    else:
        if T1_HDR_NEW in body:
            body = body.replace(T1_HDR_NEW, T1_HDR_OLD); print("  [Table 1 header] header form reverted")
        body = rep(body, T1_CAP_OLD, T1_CAP_NEW, "Table 1 caption (c, footnote form)")
    if box:
        body = rep(body, BOX_OLD, BOX_NEW, "box row")
    if undo_box:
        body = rep(body, BOX_NEW, BOX_OLD, "box row (undo)")
    write(BODY, body)

    appx = read(APPX)
    print("appendix_v19.tex")
    appx = rep(appx, E1_OLD, E1_NEW, "E.1 map (d)")
    appx = rep(appx, E7_ANCHOR, E7_NEW, "E.7 sentences (e)")
    for o, n, lab in APPX_RENAMES:
        appx = rep(appx, o, n, lab)
    if swap:
        body = read(BODY)
        body = rep(body, HIST, "", "history-call sentence out of Section 7")
        write(BODY, body)
        appx = rep(appx, HIST_E9_ANCHOR, HIST_E9_ANCHOR + HIST_E9, "history-call sentence into E.9")
    if undo_swap:
        appx = rep(appx, HIST_E9_ANCHOR + HIST_E9, HIST_E9_ANCHOR, "history-call sentence out of E.9")
        body = read(BODY)
        anchor = "because an \\texttt{UPDATE} replaces the record that \\texttt{search} and \\texttt{get\\_all} return (\\texttt{mem0ai} 1.0.5).\n"
        body = rep(body, anchor, anchor + HIST, "history-call sentence back into Section 7")
        write(BODY, body)
    write(APPX, appx)
    print("done")


if __name__ == "__main__":
    main(sys.argv[1:])
