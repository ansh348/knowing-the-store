# -*- coding: utf-8 -*-
"""kts_patch.py -- program R115 (2026-09-18): the author's "Knowing the Store" patch to paper_v19 (reviews/r115/PATCH_KTS.md),
applied as asserted edits to reviews/v19/src/{abstract,body,appendix}_v19.tex, iclr2027_monitoring_submission/tools/refcheck_v11.py
and the bibliography.

Every edit names its OLD text, which must occur exactly `count` times (default once) in the file; NEW replaces it. Line endings
are preserved byte for byte (the sources are LF). Idempotent: an edit whose NEW is present and whose OLD is absent is reported
as already applied and skipped.

    python reviews/r115/tools/kts_patch.py --check          # read-only: every anchor present exactly once, or already applied
    python reviews/r115/tools/kts_patch.py --bib-inline     # phase A only: the %%V11:677-871%% marker replaced by the carried lines
    python reviews/r115/tools/kts_patch.py --apply          # phase B: every other edit (P1-P13, A1-A3, A5, A6a-c, the nine bibitems, refcheck)
    python reviews/r115/tools/kts_patch.py --words          # word deltas per edit (OLD -> NEW), main text and appendix separately

The rulings applied (the author, 18 September): P1 sentence 7 in the gap form; P7 "make no reliable difference" (D1); P9 "capped"
and the GR-1 clause "a gain over blind that includes zero" (rulings 2 and 3); P12 "responds to a moved count" (D2); A4 not
applied; A5 defines P2-P4 and GR-1-GR-5 and prints the frozen GR-1 / GR-3 texts verbatim (D3, ruling 3); A6(b) deletes all
nine uncited entries (D4); A6(c) "three main backends"; Part E not applied. After Step 1 (the ruling of 18 September): A5(b), the P2 to P4 outcome texts verbatim beside the GR texts.
"""
import io
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(os.environ.get("KTS_ROOT") or pathlib.Path(__file__).resolve().parents[3])
SRC = ROOT / "reviews" / "v19" / "src"
SUB = ROOT / "iclr2027_monitoring_submission"
BODY, ABS, APPX = SRC / "body_v19.tex", SRC / "abstract_v19.tex", SRC / "appendix_v19.tex"
REFCHECK = SUB / "tools" / "refcheck_v11.py"
V11 = SUB / "paper_v11.tex"

# ----------------------------------------------------------------------------------------------------------------------- texts
ABSTRACT_OLD = (
    "An agent with a persistent memory store can judge two things before retrieving. The first is whether the store covers a question (feeling of knowing, FOK). "
    "The second is whether the store holds something the agent must no longer use, such as a cancelled plan (negative-obligation knowledge, NOK). "
    "We define both as intent-dependent labels, build synthetic stores with exact labels, and measure them on three backends with six models. "
    "The monitor sees only a lifecycle summary: record counts per lifecycle state and a value-free list of attribute names, on which only superseded names appear. "
    "The attribute names carry most of the observed signal. "
    "Where the summary names the stale attribute, a similarity lookup over the list matches every model but the largest (three models; one question, three store versions). "
    "Where the summary only counts a state, every model discriminates more weakly, naming that state lifts it, and the count interventions do not establish consistent count use. "
    "Returning non-active records with their tags instead of masking them is a second route, at retrieval time, covering what the list misses. "
    "Graphiti's own name list retains useful signal; under FR-Bank's own metadata GPT-4.1 mini and the lookup fall near chance, while Haiku 4.5 keeps $72\\%$ of its gain. "
    "Downstream, gating retrieval on the judgment reaches more of the records the agent must not use without reducing detector-flagged stale answers, because the store keeps untagged duplicates. "
    "Reference-assisted retagging of those duplicates reduced the flagged answers, pointing to the write path, pending human validation of the detector. "
    "Preserving lifecycle evidence supports monitoring; practical utility still requires semantic validation."
)
ABSTRACT_NEW = (
    "An agent with a persistent memory store can judge two things before retrieving. The first is whether the store covers a question (feeling of knowing, FOK). "
    "The second is whether the store holds something the agent must no longer use, such as a cancelled plan (negative-obligation knowledge, NOK). "
    "We define both as intent-dependent labels, build synthetic stores with exact labels, and measure them on four backends with up to six models. "
    "The monitor sees only a lifecycle summary: record counts per lifecycle state and a value-free list of attribute names, on which only superseded names appear. "
    "The attribute names carry most of the signal. "
    "With one question asked of three store versions, GPT-4.1 mini and Haiku 4.5 do not exceed a similarity lookup over the list, and Opus 5 exceeds it by $0.07$. "
    "Where the summary only counts a state, every model discriminates more weakly than a reader of the counts, and naming that state lifts every model. "
    "Returning non-active records with their tags instead of masking them is a second route, at retrieval time, covering what the list misses. "
    "What the backend writes decides how much survives. "
    "Under FR-Bank's own metadata GPT-4.1 mini and the lookup fall near chance while Haiku 4.5 keeps $72\\%$ of its gain, and Graphiti's own name list serves a lookup better than the model. "
    "Downstream, gating retrieval on the judgment reaches more of the records the agent must not use without reducing detector-flagged stale answers, because the store keeps untagged duplicates. "
    "Reference-assisted retagging of those duplicates removes most of the flagged answers, which points to the write path; the detector's human validation is pending."
)

P9_OLD = (
    "On Graphiti \\citep{zep}, a fourth backend whose validity intervals are the closest thing to lifecycle tags in a shipped store, a census over forty personas recovers some of the forbidding records.\n"
    "Its invalidation marks reach $13$ of the $34$ obligations of the full store that the ground truth marks superseded or expired, more than the quarter we had predicted.\n"
    "Its name lookup retains useful signal despite weak summary monitoring (Appendix~\\ref{app:posthoc-graphiti}).\n"
)
P9_NEW = (
    "Graphiti recovers some of the forbidding records and exposes names a lookup can use.\n"
    "Its invalidation marks reach $13$ of the $34$ full-store obligations that the ground truth marks superseded or expired, more than the quarter we had predicted.\n"
    "Under its capped store-written summary GPT-4.1 mini scores $0.58$ on the $323$ full-store questions, a gain over blind that includes zero, against $0.74$ under the ground-truth summary.\n"
    "A name lookup over Graphiti's own superseded names scores $0.68$, reliably above the model by $+0.10$ (Appendix~\\ref{app:posthoc-graphiti}).\n"
    "%% R115 (2026-09-18): AUX-R85-G10-P2 (0.5765 capped against INDEXED-TRUE 0.7424 on the 323); AUX-R85-G10-GR (GR-1 FAILS: +0.0801 over blind, item [-0.0031,+0.1604], persona [+0.0027,+0.1624]; GR-3 HOLDS: the lookup 0.6780, +0.1014 [+0.0102,+0.2086]; [+0.0094,+0.1988]); the frozen GR texts print in Appendix G.4 (ruling 3 of 18 September).\n"
)

P12_OLD = (
    "The models draw most of their signal from a lifecycle summary's attribute names; nothing we tried with the counts establishes that they use them consistently.\n"
    "Tags on returned records are another monitoring route, and Graphiti's name list carries useful signal.\n"
    "The detector-flagged stale answers downstream come from duplicates the store keeps active, and reference-assisted retagging removed most of them; semantic validation and practical utility remain unresolved.\n"
)
P12_NEW = (
    "The models draw most of their signal from a lifecycle summary's attribute names, and a name lookup over a clean list is not exceeded by two of the three.\n"
    "Only Opus 5 responds to a moved count.\n"
    "Tags on returned records are the second route.\n"
    "What a backend writes decides how much survives: under FR-Bank's own list GPT-4.1 mini and the lookup fall near chance while Haiku 4.5 keeps most of its gain.\n"
    "Graphiti's own names serve a lookup better than the model.\n"
    "Downstream, the flagged stale answers trace to duplicates the store keeps active, and answer-level benefit awaits the detector's human validation.\n"
)

P13_OLD = (
    "Keep non-active records reachable with their lifecycle tags for the obligation judgment; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags, and whether unmasked retrieval also improves final answers is untested (Section~\\ref{sec:routes}).\n"
    "Maintain the list of attribute names that hold non-active content, superseded, retracted and expired alike: compare a name lookup with the model on the actual store before paying for monitoring (Sections~\\ref{sec:counterfactual} and~\\ref{sec:backends}).\n"
    "Tag the duplicates the store keeps active: in our reference-assisted retagging that removed most of the detector-flagged stale answers, while semantic gains from fetching corrections remain unvalidated (Section~\\ref{sec:downstream}).\n"
)
P13_NEW = (
    "Keep non-active records reachable with their lifecycle tags; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags (Section~\\ref{sec:routes}).\n"
    "Maintain the list of attribute names that hold non-active content, superseded, retracted and expired alike.\n"
    "Compare a name lookup with the model on the actual store before paying for the model call (Sections~\\ref{sec:counterfactual} and~\\ref{sec:backends}).\n"
    "Tag the duplicates the store keeps active, which is where the flagged stale answers came from (Section~\\ref{sec:downstream}).\n"
)

A5_ANCHOR = "The prediction that the native name lookup would remain near chance fails: its list carries useful matching signal despite weak summary monitoring.\n"
A5_INSERT = (
    "%% R115 (2026-09-18): the amendment's predictions and readings defined here (deviation D3), and the frozen GR-1 / GR-3 texts printed verbatim (ruling 3 of 18 September; GR-1's text is tagged [MAIN] in the registration and prints here for the page limit, a Section 7 clause carrying its content).\n"
    "Amendment 1's three monitoring predictions (P2 to P4 in Appendix~\\ref{app:registration}) are that the store-written summary falls below the ground-truth summary by more than the tolerance, that the superseded-names lookup sits within tolerance of chance, and that the tagged view sits within tolerance of the untagged view.\n"
    "Its five readings are GR-1, that the paired obligation gain on the store-written summary excludes zero; GR-2, the same for coverage; GR-3, that the superseded-names lookup sits within tolerance of the model or above it; GR-4, descriptive retention against FR-Bank's ground-truth gain; and GR-5, the census's failure mode.\n"
    "%% registrations/ADDENDUM_R85_GRAPHITI.md section 7, GR-1 FAILS and GR-3 HOLDS; the registration's wording ships verbatim with $D$, $Y$ and $X$ filled from AUX-R85-G10-GR.\n"
    "GR-1's text reads: ``On a second store that records when a fact stopped being true, the obligation judgment does not rise beyond $+0.0801$ when the summary is supplied, so the gain measured on our own store does not reproduce where the lifecycle record is thinner.''\n"
    "GR-3's reads: ``A matcher reading the store's own list of superseded names reaches $0.6780$ against the monitor's $0.5765$ on this store as well.''\n"
)

BIB_KEYS = ["knowbutnotact", "dunlosky2009", "knowact", "metcalfe1994", "naeini2015", "nosek2018", "pineau2021", "openaimemory", "memgate"]

REFCHECK_RETIRED = (
    "# R115 (2026-09-18): the nine bibitems no citation reached (Cao 2026, Dunlosky & Metcalfe 2009, Feng 2026, Metcalfe & Shimamura 1994,\n"
    "# Naeini 2015, Nosek 2018, Pineau 2021, OpenAI 2026, Zhang 2026) were removed from the bibliography under the author's ruling; their\n"
    "# records stay above for the history and are not orphans.\n"
    "RETIRED = {" + ", ".join(repr(k) for k in BIB_KEYS) + "}\n\n"
)

# (file, tag, old, new, count)
EDITS = [
    (ABS, "P1", ABSTRACT_OLD, ABSTRACT_NEW, 1),
    (BODY, "A6c", "across three backends and six models from three vendors.", "across three main backends and six models from three vendors.", 1),
    (BODY, "P2a", "Of the three backends, FR-Bank \\citep{fr} is the only one", "Of the three main backends, FR-Bank \\citep{fr} is the only one", 1),
    (BODY, "P2b",
     "neither records lifecycle structure, so we call them the structureless backends.\n",
     "neither records lifecycle structure, so we call them the structureless backends.\n"
     "Graphiti \\citep{zep}, whose validity intervals resemble lifecycle tags, is a fourth backend, scored with GPT-4.1 mini on the same personas (Appendix~\\ref{app:posthoc-graphiti}).\n", 1),
    (BODY, "P3", "because resampling whole questions keeps each triple intact.", "because resampling whole personas keeps each triple intact and the item-level bootstrap does not.", 1),
    (BODY, "P4a",
     "Opus 5 exceeds it by $0.07$ (Table~\\ref{tab:cf-main}).\n",
     "Opus 5 exceeds it by $0.07$ (Table~\\ref{tab:cf-main}).\nOpus 5's first draw alone keeps that margin (Appendix~\\ref{app:counterfactual}).\n", 1),
    (BODY, "P4b", "Scored against the PRESENT versions alone,", "Scored post hoc against the PRESENT versions alone,", 1),
    (BODY, "P4c", "Table~\\ref{tab:cf-main} gives that score and the wins, ties and losses per triple, both post hoc.\n", "", 1),
    (BODY, "P5",
     "Opus 5, run once per item after this draft against its five-draw row, moves $-0.10$ on retraction and $-0.12$ on expiry.",
     "Opus 5, run once per item against its five-draw row, moves $-0.10$ on retraction and $-0.12$ on expiry, both intervals excluding zero.", 1),
    (BODY, "P6",
     "The counted-state evidence rests on $30$ retraction and $44$ expiry pairs, the $30$ plus the $14$ of the descriptive extension draw in Appendix~\\ref{app:counterfactual}.\n"
     "On the full obligation set the counted-state groups are $26$ retraction and $15$ expiry obligations, and their rows give only a direction (Section~\\ref{sec:populations}).\n",
     "These groups are small (Section~\\ref{sec:limitations}).\n", 1),
    (BODY, "P7",
     "while a count of tagged lines scores $0.62$ under either tag source (Table~\\ref{tab:routes-full}, Appendix~\\ref{app:resp}).\n",
     "while a count of tagged lines scores $0.62$ under either tag source (Table~\\ref{tab:routes-full}, Appendix~\\ref{app:resp}).\n"
     "On Graphiti, native tags on the same five retrieved edges make no reliable difference ($-0.01$, both intervals including zero; Appendix~\\ref{app:posthoc-graphiti}).\n"
     "% AUX-R85-G10-P4 (0.6854 against 0.6995, -0.0141; [-0.0786,+0.0554]; [-0.0613,+0.0325])\n", 1),
    (BODY, "P8", "rises from $0.69$ to a reliable $0.81$.", "rises from $0.69$ to a reliable $0.81$, a descriptive result with no prediction fixed in advance.", 1),
    (BODY, "P9a", "\\texttt{get\\_all} return (\\texttt{mem0ai} 1.0.5).", "\\texttt{get\\_all} return.", 1),
    (BODY, "P9b", "resolve to zero note identifiers (Table~\\ref{tab:census}).", "resolve to zero note identifiers.", 1),
    (BODY, "P9c", P9_OLD, P9_NEW, 1),
    (BODY, "P10a",
     "Two further results stand in Appendix~\\ref{app:resp}: a header naming the persona and the date raises in-view correct answers reliably for both answerers, and the composite below.\n",
     "Two further results are in Appendix~\\ref{app:resp}.\nA header naming the persona and the date raises in-view correct answers reliably for both answerers.\n", 1),
    (BODY, "P10b",
     "by a reliable $+0.03$ against retrieval alone for GPT-4.1 mini and stays level for Haiku 4.5 (Table~\\ref{tab:ds-a7}, Appendix~\\ref{app:resp}).",
     "by a reliable $+0.03$ for GPT-4.1 mini and stays level for Haiku 4.5 (Table~\\ref{tab:ds-a7}).", 1),
    (BODY, "P11",
     "The sixty-percent retention line was a conventional threshold, fixed before the main study, with no recorded reason for its value.\n"
     "The tagged route under the store's own tags is descriptive, with no prediction fixed in advance for its rise.\n", "", 1),
    (BODY, "P12", P12_OLD, P12_NEW, 1),
    (BODY, "P13", P13_OLD, P13_NEW, 1),
    (APPX, "A1", "was run after this draft once per item ($k=1$, the registered default)", "was run once per item ($k=1$, the registered default)", 1),
    (APPX, "A2", "two runs after this draft, the composite's answers", "two later runs, the composite's answers", 1),
    (APPX, "A3",
     "at or above the sixty-percent line under both renderings.\n",
     "at or above the sixty-percent line under both renderings.\n"
     "The sixty-percent line was a conventional threshold, fixed before the main study, with no recorded reason for its value.\n", 1),
    (APPX, "A5", A5_ANCHOR, A5_INSERT + A5_ANCHOR, 1),
    (APPX, "A5b",
     "GR-1's text reads: ``On a second store",
     "%% registrations/ADDENDUM_R85_GRAPHITI_AMENDMENT_1.md section 5, the outcome texts of P2 (HOLDS), P3 (FAILS) and P4 (HOLDS) verbatim, "
     "$G$, $T$, $D$, $I$, $Y$, $U$ filled from AUX-R85-G10-P2 / -P3 / -P4 (the ruling of 18 September after Step 1); P1's text is above.\n"
     "The summary-route prediction holds; its registered text reads: ``Under Graphiti's store-written summary GPT-4.1 mini reads $0.5765$ against $0.7424$ "
     "under the ground-truth summary on the same questions, $-0.1659$ below with interval $[-0.2593,-0.0764]$; a matcher reading Graphiti's own list of "
     "superseded names reads $0.6780$.''\n"
     "The lookup prediction fails: ``A matcher reading Graphiti's own list of superseded names reaches $0.6780$, $+0.1780$ from chance.''\n"
     "The tag-route prediction holds: ``Shown the five retrieved edges with Graphiti's own states, GPT-4.1 mini reads $0.6854$ against $0.6995$ without them, "
     "within tolerance: the states this store writes do not reach the records that forbid use.''\n"
     "GR-1's text reads: ``On a second store", 1),
    (APPX, "A6a-1", "profile $[0.6900,0.8090]$", "persona $[0.6900,0.8090]$", 1),
    (APPX, "A6a-2", "difference (item; profile)", "difference (item; persona)", 1),
    (APPX, "A6a-3", "intervals (item; profile)", "intervals (item; persona)", 1),
    (APPX, "A6a-4", " & profile & & & & & ", " & persona & & & & & ", 4),
    (REFCHECK, "refcheck-1",
     "# ---- direction 1: every checked record verifies (v10 logic, unchanged) --------------\n",
     REFCHECK_RETIRED + "# ---- direction 1: every checked record verifies (v10 logic, unchanged) --------------\n", 1),
    (REFCHECK, "refcheck-1b",
     "for k in sorted(official):\n",
     "for k in sorted(official):\n    if k in RETIRED:\n        continue                    # R115: the bibitem was removed; the record stays for the history\n", 1),
    (REFCHECK, "refcheck-2",
     "orphan_records = (checked | declared) - present\n",
     "orphan_records = (checked | declared) - present\n"
     "orphan_records -= RETIRED          # R115: removed bibitems whose records stay for the history\n", 1),
]

MAIN_TAGS = {"P1", "A6c", "P2a", "P2b", "P3", "P4a", "P4b", "P4c", "P5", "P6", "P7", "P8", "P9a", "P9b", "P9c", "P10a", "P10b", "P11", "P12", "P13"}


# --------------------------------------------------------------------------------------------------------------------- helpers
def read(p):
    raw = p.read_bytes()
    crlf = b"\r\n" in raw
    return raw.decode("utf-8").replace("\r\n", "\n"), crlf


def write(p, text, crlf):
    p.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))


def words(s):
    s = re.sub(r"(?m)^%.*$", "", s)                     # comments carry no words
    s = re.sub(r"\\[A-Za-z]+~?\{[^}]*\}", "X", s)        # \ref{..}, \citep{..}, \texttt{..} count as one word
    s = re.sub(r"\$[^$]*\$", "N", s)                     # math as one word
    return len([w for w in re.split(r"\s+", s) if re.search(r"[A-Za-z0-9]", w)])


def bib_lines():
    v11, _ = read(V11)
    return v11.split("\n")[676:871]


def bib_inline(check):
    body, crlf = read(BODY)
    marker = "%%V11:677-871%%"
    if marker not in body:
        print("bib-inline: marker absent (already inlined)")
        return
    lines = bib_lines()
    assert lines[0].startswith("\\begin{thebibliography}") and lines[-1].startswith("\\end{thebibliography}"), (lines[0], lines[-1])
    assert body.count(marker) == 1
    if check:
        print(f"bib-inline: marker present once; {len(lines)} carried lines ready")
        return
    write(BODY, body.replace(marker, "\n".join(lines)), crlf)
    print(f"bib-inline: marker replaced by {len(lines)} lines")


def bib_delete(check):
    body, crlf = read(BODY)
    n_before = body.count("\\bibitem[")
    removed = []
    for k in BIB_KEYS:
        pat = re.compile(r"\\bibitem\[[^\]]*\]\{" + re.escape(k) + r"\}\n[^\n]*\n")
        m = list(pat.finditer(body))
        if not m:
            assert "{" + k + "}" not in body, f"bibitem {k} present in an unexpected shape"
            removed.append((k, "already gone"))
            continue
        assert len(m) == 1, k
        assert not re.search(r"\\cite[pt]?\{[^}]*\b" + re.escape(k) + r"\b", body), f"{k} is cited"
        if not check:
            body = body[:m[0].start()] + body[m[0].end():]
        removed.append((k, "removed" if not check else "present, will be removed"))
    if not check:
        write(BODY, body, crlf)
    print(f"bib-delete: {n_before} bibitems before; " + "; ".join(f"{k} {s}" for k, s in removed))
    if not check:
        print(f"bib-delete: {body.count(chr(92) + 'bibitem[')} bibitems after")


def run(mode):
    if mode == "--bib-inline":
        bib_inline(check=False)
        return
    check = mode == "--check"
    texts = {}
    problems = 0
    for p, tag, old, new, count in EDITS:
        if p not in texts:
            texts[p] = read(p)
        text, crlf = texts[p]
        n_old, n_new = text.count(old), (text.count(new) if new else 0)
        # NEW is tested first: for an insertion edit OLD is a prefix of NEW and still occurs after applying, so the
        # applied state is recognised by NEW's count, never by OLD's absence (a second --apply must not re-insert).
        if (new and n_new == count) or (new == "" and n_old == 0):
            status = "already applied"
        elif n_old == count and n_new == 0:
            status = "ready" if check else "applied"
            if not check:
                text = text.replace(old, new)
                texts[p] = (text, crlf)
        else:
            status = f"PROBLEM: old x{n_old} (expected {count}), new x{n_new}"
            problems += 1
        print(f"  {tag:10s} {p.name:22s} {status}")
    if mode == "--words":
        main = appx = 0
        for p, tag, old, new, count in EDITS:
            if p in (ABS, BODY, APPX):
                d = (words(new) - words(old)) * count
                print(f"  {tag:10s} {d:+4d} words")
                if tag in MAIN_TAGS:
                    main += d
                else:
                    appx += d
        print(f"main text {main:+d} words; appendix {appx:+d} words")
        return
    if check:
        bib_inline(check=True)
        bib_delete(check=True)
        print("check:", "every anchor in place" if not problems else f"{problems} PROBLEM(S)")
        sys.exit(1 if problems else 0)
    assert not problems, "anchors missing; nothing written"
    assert "%%V11:677-871%%" not in texts[BODY][0], "run --bib-inline first (and confirm the build is byte-identical) before --apply"
    for p, (text, crlf) in texts.items():
        write(p, text, crlf)
    bib_delete(check=False)
    print("apply: done")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    assert mode in ("--check", "--apply", "--bib-inline", "--words"), mode
    run(mode)
