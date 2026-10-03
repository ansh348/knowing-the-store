"""Independent numeric-occurrence re-scan of a manuscript against the central number record.
R112 (2026-09-16, the integration pass): LEDGERS gains r85_graphiti/NUMBERS_R85.md. Reason: the forty-persona Graphiti census
(AUX-R85-G10-*) prints in Section 7 and Appendix G.4 with its printed forms ledgered there (AUX-R85-G10-PRINTED).
R111 (2026-09-15, the writing pass on paper_v18): LEDGERS gains reviews/NUMBERS_WP.md. Reason: the six body tables print two-decimal
forms of recorded four-decimal values (items 45, 50 to 55) and the population table prints the calls per question from the
recorded rows (AUX-WP-X5-DRAWS); the set-based match needs the printed strings in a ledger, each beside its source key.

v13 changes, each in response to a defect found while establishing the Pass 0 baseline:

  1. NO DEFAULT MANUSCRIPT. v12 defaulted to `paper.tex`, the FROZEN fallback. Every
     invocation in the gate battery therefore audited a manuscript nobody edits, while the
     live `paper_v2.tex` went unchecked. The path is now required and the tool exits 2
     without it.

  2. R82 LEDGER ADDED. v12's LEDGERS list stopped at R74, so every figure the R82
     counterfactual and calibration work introduced was reported unaccounted. Adding
     `r82_counterfactual/NUMBERS_R82.md` closes that. Registration files are deliberately
     NOT added: they are not number ledgers, they carry numbers by the hundred, and
     admitting them would weaken the check rather than complete it.

  3. STRICT PERCENT/RATIO BRIDGE. Ledgers record proportions (`0.0595`); the manuscript
     prints percentages (`5.95\\%`). v12 could not connect the two. The bridge applies ONLY
     to a token immediately followed by `\\%`, and only at the precision the manuscript
     actually printed: 5.95 -> 0.0595, 42.3 -> 0.423, 101.4 -> 1.014. Every bridged token is
     listed in the output so a reader can audit the substitution rather than trust it.

  4. DERIVED-RATIO REGISTRY. Two published percentages (42.3, 101.4) are ratios in their
     artifact and appear nowhere in any JSON as the printed string. They are verified here
     by recomputation against the artifact, not whitelisted.

  5. IDENTIFIER CLASSES WIDENED. v12 stripped `D93` but not `D-R82-4`, and did not strip the
     commit hashes in the registration table, so `82`, `3147`, `05` and `351` were reported
     as unaccounted research numbers. Spelled-out cross-references ("Section 4.4's sentence")
     were likewise counted as research numbers. All three classes are now stripped.

KNOWN LIMIT, stated so it is not mistaken for a guarantee. Matching is set-based: a token
counts as accounted when the string appears ANYWHERE in the ledger family, so an unrelated
figure of equal value passes it. This is not hypothetical. `0.0560`, the constant-predictor
Brier floor, passed v12 by matching a clustered CI endpoint in the E1-R retraction row and the
reliability diagram's observed frequency, neither of which is that quantity; it was caught by
hand, not by the tool, and now has its own ledger row. Value-plus-context matching would close
the class. This version does not attempt it.

v14 SPEC, agreed and not yet built:
  (a) Flag any token matching MORE THAN ONE ledger row as AMBIGUOUS rather than accounted. This
      is the general form of the 0.0560 defect; multiplicity is the cheap signal that separates
      "backed" from "coincidentally equal", and it needs no context model.
  (b) Add an EXTERNAL class for values quoted from cited work (the 7 and 28 of the multi-hop
      ceiling, the inherited 5% retrieval premise). Their authority is the refcheck ledger, not
      NUMBERS_*, and v14 should FAIL if an external value is found in NUMBERS_* at all: that is
      precisely how 28 earned a coincidental pass here. Externals are ours to cite, never ours
      to measure, and auditing them against our own ledgers is a category error.

Direction A: every numeric token printed by the manuscript is either (i) present in the
central ledger family, (ii) reachable from it by the declared percent bridge, (iii) a
verified derived ratio, or (iv) inside a declared non-research exclusion class.

Unlike v12, which always exited 0, this exits 1 when Direction A leaves anything unaccounted.

Usage:  python tools/trace_scan_v13.py paper_v2.tex
"""
import re
import sys
import json
import pathlib
from decimal import Decimal

if len(sys.argv) < 2:
    print("usage: python tools/trace_scan_v13.py <manuscript.tex>")
    print("error: no manuscript given; v13 has no default "
          "(v12 defaulted to the frozen paper.tex, which is why this exists)")
    sys.exit(2)

SUB = pathlib.Path(sys.argv[1])

LEDGERS = [
    pathlib.Path("../e1_metamemory/NUMBERS.md"),
    pathlib.Path("../e1xv_crossvendor/NUMBERS_E1XV.md"),
    pathlib.Path("../e1qp_questionprior/NUMBERS_E1QP.md"),
    pathlib.Path("../e1r_robustness/NUMBERS_E1R.md"),
    pathlib.Path("../r74/NUMBERS_R74.md"),
    pathlib.Path("../r82_counterfactual/NUMBERS_R82.md"),
    # R86 (2026-09-09). Same reason change note 2 added the R82 ledger: R86 corrected the
    # A-MEM link census onto the population the study actually scores, and the corrected
    # figure had no row anywhere. reviews/NUMBERS_R86.md carries it with its method.
    pathlib.Path("../reviews/NUMBERS_R86.md"),
    # R87 (2026-09-11). Table 2 gains the n=45 counted-states row; NUMBERS_R82.md carries the
    # Haiku 4.5 and Opus 5 pairs but not GPT-4.1 mini's, which reviews/NUMBERS_R87.md transcribes
    # from results/cf_scores.json with its method (D-R87-1).
    pathlib.Path("../reviews/NUMBERS_R87.md"),
    # R97 (2026-09-13). The SIDE registration's S1 and S2-U results enter the manuscript (Amendment 1)
    # from side_experiments/NUMBERS_SIDE.md; the Q4 marker fraction and the two verbatim structureless
    # indexes enter from resp_review/NUMBERS_RESP.md (AUX-RESP-PAPER-Q4); the rounded forms the SIDE
    # frozen texts print (15.04, 8.96, 1.75, 0.035, 0.062) are recorded against their four-decimal
    # ledger values in reviews/NUMBERS_R97.md, on the R86/R87 precedent.
    pathlib.Path("../side_experiments/NUMBERS_SIDE.md"),
    pathlib.Path("../resp_review/NUMBERS_RESP.md"),
    pathlib.Path("../reviews/NUMBERS_R97.md"),
    # R104 (2026-09-13): the Phase 1 values of the v11-to-v12 pass (reviews/v12/phase1.json) and the rounded forms the v12 body prints.
    pathlib.Path("../reviews/NUMBERS_R104.md"),
    # R98 (2026-09-13). The CF-2 store-counterfactual cell (registrations/ADDENDUM_CF2.md, frozen f016f03, R94)
    # enters the manuscript: Table 9, Appendix D.2, sections 6-8; every value from r82_counterfactual/cf2/NUMBERS_CF2.md
    # by key (sections 5b-5k; 5k carries the derived margins the text prints).
    pathlib.Path("../r82_counterfactual/cf2/NUMBERS_CF2.md"),
    # R101 (2026-09-13): the downstream experiment DS enters the manuscript (Section 7, Appendix F.9, Table 25);
    # every value from ds_downstream/NUMBERS_DS.md. The RESP ledger is already listed above.
    pathlib.Path("../ds_downstream/NUMBERS_DS.md"),
    # R105 (2026-09-14): the CF-3 expiry extension (registrations/ADDENDUM_CF3.md) and its sizing census enter the manuscript
    # (Appendix D.2 tab:cf3-expiry, Section 9, Table 3's conflate row); every value from r82_counterfactual/cf3/NUMBERS_CF3.md by key.
    pathlib.Path("../r82_counterfactual/cf3/NUMBERS_CF3.md"),
    # R106 (2026-09-14). The abstract, Section 10 and Appendix H print the post hoc nb6 sweep's fault decomposition;
    # nb6_sweep/NUMBERS_NB6SWEEP.md carries it from results/step4_recall.json (tools/ledger_nb6sweep.py).
    pathlib.Path("../nb6_sweep/NUMBERS_NB6SWEEP.md"),
    # R107 (2026-09-14). The padding probe lands in Section 5 and Appendix D.2 (pad_probe/NUMBERS_PAD.md, AUX-PAD-*); Section 4's
    # provenance sentence and the k = 5 census are reviews/NUMBERS_R107.md.
    pathlib.Path("../pad_probe/NUMBERS_PAD.md"),
    pathlib.Path("../reviews/NUMBERS_R107.md"),
    # R108 (2026-09-14). The licensed-record split, Table 22's intervals and the tag census: reviews/NUMBERS_R108.md.
    pathlib.Path("../reviews/NUMBERS_R108.md"),
    # R106. DS Amendment 2 (the LOOKUP-LIT answer stage; Haiku 4.5 as answerer) is in ds_downstream/NUMBERS_DS.md section 7, already listed.
    # R102 (2026-09-13): the v10 clarity rewrite prints two-decimal roundings of four-decimal ledger values
    # in main-text prose (the brief, rule 1.2); reviews/NUMBERS_R102.md records each printed form against its
    # source key, on the R86/R87/R97 precedent. No new measurement enters through it.
    pathlib.Path("../reviews/NUMBERS_R102.md"),
    # R103 (2026-09-13): the Q4 marker-as-absence probe's ledger (registrations/ADDENDUM_Q4.md, descriptive) and the
    # v11 pass's ledger of rounded forms and deterministic values (the attribute-naming split, the unflagged-record
    # census, precision and recall at the base rate; CLAIMS.md R103 block). DS Amendment 1 writes into NUMBERS_DS.md.
    pathlib.Path("../q4_inversion_probe/NUMBERS_Q4.md"),
    pathlib.Path("../reviews/NUMBERS_R103.md"),
    # R110 (2026-09-15, CC_PASS_v18). The Phase 1 analyses (count readers, tag baselines, single-draw scores, the lookup at 100
    # and 200 names; reviews/NUMBERS_R110.md, AUX-R110-*), Haiku 4.5 under the store's own metadata (believed_h/NUMBERS_BELIEVED_H.md,
    # AUX-BH-*) and the per-category increment moved within the triple (r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md, AUX-V2RCAT-*)
    # enter the manuscript: Tables 1, 2 and 4, Sections 4 to 8, Appendices C.2, E.9, E.10. DS Amendments 5 to 7 write into
    # ds_downstream/NUMBERS_DS.md sections 11 to 13, already listed.
    pathlib.Path("../reviews/NUMBERS_R110.md"),
    pathlib.Path("../believed_h/NUMBERS_BELIEVED_H.md"),
    pathlib.Path("../r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md"),
    # R111 (2026-09-15, the writing pass): the two-decimal forms of the six body tables and the calls per question of the population table (reviews/NUMBERS_WP.md, AUX-WP-*).
    pathlib.Path("../reviews/NUMBERS_WP.md"),
    # R112 (2026-09-16, the integration pass): the forty-persona Graphiti census (r85_graphiti/NUMBERS_R85.md, AUX-R85-G10-*) enters
    # Section 7 and Appendix G.4; the post-hoc recomputes (AUX-WP-B-*, -B4-*, -F1-*) are sections 8 to 10 of reviews/NUMBERS_WP.md, already listed.
    pathlib.Path("../r85_graphiti/NUMBERS_R85.md"),
    # R113 (2026-09-16, the zero-cost audit pass): the lexical lookup's paired rows at 100 and 200 padded names (tab:pad) are read from
    # R110's A4 artifact and ledgered in reviews/NUMBERS_R113.md (AUX-R113-PAD-LEX-PAIRED); the pass's other sections (AUX-R113-Z1 to -Z5)
    # print nothing in the manuscript.
    pathlib.Path("../reviews/NUMBERS_R113.md"),
    # R114 (2026-09-17, the remaining runnable paid experiments): the pass ledger; the numbers the manuscript prints from the pass live in
    # ds_downstream/NUMBERS_DS.md section 14 (AUX-DS-R114-*) and r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md section 8 (AUX-V2RCAT-OP5).
    pathlib.Path("../reviews/NUMBERS_R114.md"),
    # Completion 2026-09-17: versioned source repair, fixed cached-depth analysis and costs.
    pathlib.Path("../reviews/NUMBERS_COMPLETION_V1.md"),
    # R115 (2026-09-18, the Knowing-the-Store patch): no new measurement; the pass ledger records the two-decimal forms the patch
    # brings into the main text beside their source keys and the registered texts' filled placeholders (AUX-R115-PRINTED).
    pathlib.Path("../reviews/NUMBERS_R115.md"),
    # R116 (2026-09-19, the provenance fix and the harness disclosure): the probe-gate counts of the Appendix B disclosure and the
    # price constants of the two frontier lanes printed in E.11 (AUX-R116-HARNESS, AUX-R116-PRICES), beside their sources.
    pathlib.Path("../reviews/NUMBERS_R116.md"),
    # R123 (2026-09-19, the v21 update and writing pass): the no-human batch of R122 (reviews/r122/NUMBERS_R122.md, AUX-R122-*: the encoder rows,
    # the gate-reach rows, the intent-explicit rubric rows, the five-draw rows) prints in Appendix C.2 and E.10 and in Table 1; the pass ledger
    # (reviews/NUMBERS_R123.md) records the two-decimal forms new to the body, the supersession-only margins over the lookup (AUX-R123-SUP-MARGINS),
    # the recorded policies' 661-means (AUX-R123-REACH-ROWS) and the prediction tally (AUX-R123-TALLY). The intent crossover's values are
    # r82_counterfactual/cf2/NUMBERS_CF2.md section 14d, already listed.
    pathlib.Path("../reviews/r122/NUMBERS_R122.md"),
    pathlib.Path("../reviews/NUMBERS_R123.md"),
    # R124 (2026-09-19, the rulings on REPORT_R123): Opus 5's per-state margins over the all-states lookup and the five-draw per-state gains (AUX-R124-*).
    pathlib.Path("../reviews/NUMBERS_R124.md"),
    # R126 (2026-09-20, the readable body, v22): the state-by-intent-by-label counts of the 661 (tab:e3-intent, AUX-R126-E3-INTENT), the recorded rows added to
    # tab:gatereach (AUX-R126-GATEREACH), the day indices that replace the registration record's calendar dates (AUX-R126-DAYS) and Figure 3's values (AUX-R126-FIG3),
    # each written from its artifact by reviews/v22/tools/ledger_r126.py.
    pathlib.Path("../reviews/NUMBERS_R126.md"),
    # R128 (2026-09-20, the author's brief on v22): tab:ds-body's stale rates over both denominators (AUX-R128-DS-DENOM), Opus 5 read at draw 1 on every
    # pair in tab:cf3-expiry (AUX-R128-CF3-DRAW1), the pooled 66's sampling (AUX-R128-POOLED66) and the R127b group readings (AUX-R128-GROUPS), each written
    # from its artifact by reviews/v22/tools/ledger_r128.py.
    pathlib.Path("../reviews/NUMBERS_R128.md"),
    # R129 (2026-09-20, the author's rulings on R127b and R128's held items): the R127 group readings printed in E.3 (AUX-R129-GROUPS), mini's five-draw
    # row minus the hybrid (AUX-R129-HYB-MINI5), the inverted tag's arithmetic (AUX-R129-B9), the prediction count with E9 (AUX-R129-COUNT) and the
    # two-decimal forms Sections 5.1 and 5.2 print (AUX-R129-E9-PRINTED, -HYB-PRINTED), written from the artifacts by reviews/v22/tools/ledger_r129.py.
    pathlib.Path("../reviews/NUMBERS_R129.md"),
    # R131 (2026-09-20, the R125 results landed in the body): the two-decimal forms Sections 1, 5, 6, 9 and 10 and the abstract print from
    # r82_counterfactual/cf2/NUMBERS_CF2.md section 15 (AUX-R131-PRINTED, each beside its four-decimal source key), Table 1's matched column
    # from the printed W/T/L (AUX-R131-TAB1), the prediction count with the two R125 registrations (AUX-R131-COUNT), written from the R125
    # artifacts by reviews/v22/tools/ledger_r131.py (the checks of r131_number_gate.py).
    pathlib.Path("../reviews/NUMBERS_R131.md"),
    # R133 RULINGS 3 (2026-09-21): tab:routes' two per-state rows (the tagged view minus the summary alone on expiry and supersession, GPT-4.1 mini) print
    # two-decimal forms of resp_review/run/scores_resp.json values (AUX-RESP-L2-MINI-NOK); reviews/NUMBERS_R133.md AUX-R133-ROUTES-PERSTATE carries the printed forms,
    # written from the artifact by reviews/v23/tools/ledger_r133.py.
    pathlib.Path("../reviews/NUMBERS_R133.md"),
    # R134 (2026-09-21, the paraphrase check landed in v23): the six appendix tables of Appendix C.2 (tab:para-*) print four-decimal values of
    # cf2_paraphrase/results/para_scores.json, para_scores_all124.json, lookups.json and para_minus_lookup_posthoc.json (cf2_paraphrase/NUMBERS_PARA.md
    # AUX-PARA-*, written by cf2_paraphrase/tools/ledger_para.py); the two-decimal forms of Section 5.2, the abstract, Section 1, the Limitations and
    # the Conclusion and the counts of the appendix prose are reviews/NUMBERS_R134.md AUX-R134-PRINTED (reviews/v23/tools/ledger_r134.py, from the
    # checks of r134_number_gate.py), each beside its four-decimal source.
    pathlib.Path("../cf2_paraphrase/NUMBERS_PARA.md"),
    pathlib.Path("../reviews/NUMBERS_R134.md"),
    # R135 (2026-09-21, the last content pass): tab:robust's ten rows (reviews/v23/tools/robust_tex.py), the abstract's, Section 5.1's, the builders box's and
    # ADDENDUM 2's printed forms are reviews/NUMBERS_R135.md AUX-R135-ROBUST and AUX-R135-PRINTED (ledger_r135.py, from the checks of r135_number_gate.py), each beside its source.
    pathlib.Path("../reviews/NUMBERS_R135.md"),
    # R137 (2026-09-22, the long-list check landed): the six C.2 tables (tab:cfpad-*) print four-decimal values of cf_pad/results/cf_pad_scores.json (cf_pad/NUMBERS_CF_PAD.md AUX-CFP-*,
    # written by cf_pad/tools/report_cf_pad.py); the two-decimal forms of tab:robust row 9, Section 5.2, the abstract, Sections 1 and 10, the recount, Figure 1's transcribed totals and the
    # appendix prose's counts are reviews/NUMBERS_R137.md AUX-R137-* (reviews/v23/tools/ledger_r137.py, from the checks of r137_number_gate.py), each beside its source.
    pathlib.Path("../cf_pad/NUMBERS_CF_PAD.md"),
    pathlib.Path("../reviews/NUMBERS_R137.md"),
    # R139 (2026-09-23): the equivalence test, the length-only reader, the printed forms of B1, B2, B7, the comparison count and Figure 3's bars.
    pathlib.Path("../reviews/NUMBERS_R139.md"),
    # R141 (2026-09-23): the padded sibling control (SB-60): tab:sb60 prints four-decimal values of reviews/r141/results/scores_sb60.json and nomodel_sb60.json (reviews/NUMBERS_R141.md AUX-R141-NOMODEL, AUX-R141-RESULTS).
    pathlib.Path("../reviews/NUMBERS_R141.md"),
]

# KEY ASSERTIONS (R86 item 2.5 ruling, 2026-09-09). Set-based matching accounts a token when
# its string appears ANYWHERE in the ledger family, so an unrelated figure of equal value
# passes it. The docstring records `0.0560` as the first instance caught by hand. R86 found the
# second: Table 8's category census is 0.9736 from AV_CENSUS.auroc_one_feature (0.97357954...),
# and an unrelated precision_skipping_absent (0.97362637...) rounds to the same four decimals.
#
# An entry here is checked BY KEY NAME against the artifact, never by value, so a number that
# happens to equal another cannot satisfy it. This is the narrow form of the v14 spec item (a).
KEY_ASSERTIONS = [
    ("0.9736", "../r74/x6/x6_probes.json", "AV_CENSUS.auroc_one_feature",
     "Table 8, ranking the cross-model cell by item-construction category alone"),
    # The first instance of this class, caught by hand during R82: under v12 this value passed
    # only by matching an unrelated clustered CI endpoint and a reliability-diagram frequency.
    # It has had a ledger row since; R86 gives it the same by-name check as 0.9736.
    ("0.0560", "../r82_counterfactual/results/cal_floor.json", "P-FOK-HARD.brier",
     "Appendix H, the Brier score of a constant predictor at the base rate: the floor"),
]


def _dig(obj, dotted):
    for part in dotted.split("."):
        obj = obj[part]
    return obj


def check_key_assertions():
    """Each printed value must round to the value at its NAMED key. Returns a failure list."""
    bad = []
    print("\nKEY ASSERTIONS (checked by key name, never by value):")
    for printed, art, dotted, what in KEY_ASSERTIONS:
        p = pathlib.Path(art)          # CWD-relative, exactly as LEDGERS resolves
        try:
            val = _dig(json.loads(p.read_text(encoding="utf-8")), dotted)
            ok = f"{float(val):.4f}" == printed
        except Exception as e:                                # pragma: no cover
            val, ok = f"<{e}>", False
        print(f"  [{'OK ' if ok else 'FAIL'}] {printed} = {dotted}")
        print(f"         {art} -> {val}")
        print(f"         {what}")
        if not ok:
            bad.append((printed, dotted))
    return bad


# printed percentage -> (artifact, dotted json path, what the ratio is)
DERIVED = [
    ("42.3", "../e1r_robustness/results/believed_nok.json",
     "nok_retention", "BELIEVED NOK gain divided by TRUE NOK gain"),
    ("101.4", "../e1r_robustness/results/believed_nok.json",
     "fok_retention", "BELIEVED FOK gain divided by TRUE FOK gain"),
]

NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
PCT = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*\\%")


def norm(tok):
    t = str(tok).replace(",", "")
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return t or "0"


def to_ratio(tok):
    """Percent token -> proportion at the precision the manuscript printed. Strict."""
    return norm(Decimal(tok.replace(",", "")) / Decimal(100))


def dig(obj, path):
    for key in path.split("."):
        obj = obj[key]
    return obj


def ledger_numbers():
    found, missing = set(), []
    for p in LEDGERS:
        if not p.exists():
            missing.append(str(p))
            continue
        for m in NUM.finditer(p.read_text(encoding="utf-8", errors="replace")):
            found.add(norm(m.group()))
    return found, missing


def check_derived():
    rows = []
    for printed, art, path, note in DERIVED:
        p = pathlib.Path(art)
        if not p.exists():
            rows.append((printed, art, path, note, "ARTIFACT MISSING", False))
            continue
        try:
            raw = dig(json.loads(p.read_text(encoding="utf-8")), path)
        except (KeyError, TypeError, ValueError) as exc:
            rows.append((printed, art, path, note, "KEY ERROR %s" % exc, False))
            continue
        places = len(printed.split(".")[1]) if "." in printed else 0
        recomputed = round(Decimal(str(raw)) * 100, places)
        ok = norm(recomputed) == norm(printed)
        rows.append((printed, art, path, note,
                     "%s x100 -> %s" % (raw, recomputed), ok))
    return rows


def main():
    tex = SUB.read_text(encoding="utf-8")
    tex = tex[tex.index("\\begin{document}"):]

    b0 = tex.index("\\begin{thebibliography}")
    b1 = tex.index("\\end{thebibliography}")
    bib = tex[b0:b1]
    tex = tex[:b0] + tex[b1:]

    tikz = []
    tex = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}",
                 lambda m: (tikz.append(m.group(0)), "\n")[1], tex, flags=re.S)

    tex = "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in tex.split("\n"))
    tex = tex.replace("{,}", ",")

    # identifier classes (v13 item 5)
    tex = re.sub(r"\\texttt\{[0-9a-f]{6,}\}", " ", tex)
    tex = re.sub(r"\b(?:Section|Sections|Appendix|Appendices|Table|Tables|Figure|Figures)~?\s?\d+(?:\.\d+)*", " ", tex)
    tex = re.sub(r"\b[A-Z]{1,4}-R\d{1,3}(?:-[A-Za-z0-9]+)*", " ", tex)
    tex = re.sub(r"\bD\d{1,3}\b", " ", tex)
    tex = re.sub(r"\bR\d{2,3}\b", " ", tex)

    drop = [
        r"p\{[^}]*\}",
        r"\\setlength\{[^}]*\}\{[^}]*\}",
        r"\\multicolumn\{\d+\}",
        r"\\newtheorem[^\n]*",
        r"\\(?:v|h)space\{[^}]*\}",
        r"0\.\d+\\linewidth",
        r"\\hspace\*?\{[^}]*\}",
        r"\\char\d+",
        r"\\begin\{minipage\}\[?t?\]?\{[^}]*\}",
        r"\\thebibliography\{\d+\}",
    ]
    for d in drop:
        tex = re.sub(d, " ", tex)

    ledger, missing = ledger_numbers()
    pct_tokens = {norm(m.group(1)) for m in PCT.finditer(tex)}

    hits = [(m.group(), m.start()) for m in NUM.finditer(tex)]
    counts, where = {}, {}
    for tok, pos in hits:
        t = norm(tok)
        counts[t] = counts.get(t, 0) + 1
        where.setdefault(t, pos)

    derived_rows = check_derived()
    derived_ok = set(r[0] for r in derived_rows if r[5])

    bridged, unaccounted = {}, {}
    for t, c in counts.items():
        if t in ledger:
            continue
        if t in pct_tokens and to_ratio(t) in ledger:
            bridged[t] = (c, to_ratio(t))
        elif t in derived_ok:
            continue
        else:
            unaccounted[t] = c

    print("manuscript: %s" % SUB)
    for m in missing:
        print("  !! missing ledger %s" % m)
    print("central-ledger distinct tokens: %d  (ledger files: %d)" % (len(ledger), len(LEDGERS)))
    print("manuscript numeric occurrences (research classes): %d" % len(hits))
    print("distinct tokens: %d   bridged: %d   derived: %d   unaccounted: %d"
          % (len(counts), len(bridged), len(derived_ok), len(unaccounted)))

    print("\nPERCENT BRIDGE (printed with \\%, matched to its proportion in a ledger):")
    if not bridged:
        print("  (none)")
    for t in sorted(bridged):
        c, r = bridged[t]
        print("  %10s%%  x%-3d -> ledger %s" % (t, c, r))

    print("\nDERIVED RATIOS (recomputed from the artifact, not whitelisted):")
    for printed, art, path, note, shown, ok in derived_rows:
        print("  [%s] %s%% = %s" % ("OK " if ok else "FAIL", printed, note))
        print("         %s :: %s = %s" % (art, path, shown))

    print("\nDIRECTION A -- tokens with no central-ledger match:")
    if not unaccounted:
        print("  (none)")
    for t in sorted(unaccounted, key=lambda x: -unaccounted[x]):
        p = where[t]
        ctx = re.sub(r"\s+", " ", tex[max(0, p - 70):p + 60])
        print("  %12s x%-3d | ...%s..." % (t, unaccounted[t], ctx))

    bibn = set(norm(m.group()) for m in NUM.finditer(bib))
    tk = set(norm(m.group()) for m in NUM.finditer("".join(tikz)))
    print("\nEXCLUSION CLASS bibliographic metadata: %d distinct tokens (not audited as research)" % len(bibn))
    print("EXCLUSION CLASS tikz/pgfplots: %d distinct; not in ledger: %s"
          % (len(tk), sorted(x for x in tk if x not in ledger)))

    bad = bool(unaccounted) or any(not r[5] for r in derived_rows)
    key_bad = check_key_assertions()
    bad = bad or key_bad
    print("\n" + ("FAIL -- see DIRECTION A / DERIVED / KEY ASSERTIONS above" if bad else
                  "PASS -- every printed number resolves to a ledger, a bridge, or a verified derivation"))
    sys.exit(1 if bad else 0)


main()
