r"""numeric_diff -- every printed number before and after an edit, as a multiset.

WHY. R91 changes prose, layout and captions under a rule that no numeric value moves.
trace_scan_v13 proves each number resolves to a ledger; it cannot say whether a value
was dropped, added, or rounded between two builds. This tool compares the numeric
tokens of a committed revision with the working copy: the .tex source (comments
stripped, bibliography cut, lengths and layout options dropped, plot coordinates kept)
and, with --pdf, the text layers of the two PDFs (decimal, percent and comma-grouped
tokens only, so the review line ruler and page numbers never appear).

A value ADDED (present now, absent before) or VANISHED (absent now, present before) is a
failure. A COUNT-CHANGED value (same value, different multiplicity) is reported with the
lines that carry it now, because a relocation or a de-duplication is exactly that; it
fails only under --strict.

--figboxes compares the drawing bounding box of the pages that carry "Figure 1:" and
"Figure 2:" (main-text figures), rounded to 0.1pt, because R91 Phase 4 edits figure
captions and in-axis nodes under a rule that the figure boxes do not change. The gate
is the box's width and height; a shift of its page position (a shorter caption moves the
float) is reported and not failed.

LINE ENDINGS. Both sides are normalized CRLF -> LF before tokenizing.

Usage:
    python tools/numeric_diff.py --base=<git rev> [--tex=paper_v8.tex] [--base-tex=paper_v7.tex] [--pdf] [--figboxes] [--strict]
    --base-tex names the manuscript (and its PDF) to read at the base revision when the lineage file was
    renamed (R92: paper_v4 against paper_v3 at abac307; R93: paper_v5 against paper_v4 at fdd34c8;
    R96: paper_v6 against paper_v5 at the tree object 69c8d690, written from the uncommitted v5;
    R97: paper_v7 against paper_v6 at the tree object 43531d8b, written from the uncommitted v6;
    R98: paper_v8 against paper_v7 at the tree object a66254cb, written from the uncommitted v7); it defaults to --tex.
                                 [--figbox-accept="Figure 1"]   (an authorized box-size change; printed, not failed)
Exit 0 clean; 1 on ADDED, VANISHED, figbox change, or COUNT-CHANGED under --strict; 2 usage.
"""
import re, sys, pathlib, subprocess, collections

HERE = pathlib.Path(__file__).resolve().parent
SUB = HERE.parent
REPO = SUB.parent
BLANK_ARGS = r"\\(ref|label|cite[pt]?|eqref|includegraphics|usepackage|documentclass|setlength|vspace|hspace|resizebox|tabcolsep|pgfplotsset|definecolor)\*?(\[[^\]]*\])?\{[^}]*\}"
LENGTHS = r"[+-]?\d+(\.\d+)?\s*(pt|mm|cm|em|ex|in|pc|bp)\b|[+-]?\d*\.?\d+\s*\\(linewidth|textwidth|columnwidth)"
PGFOPTS = (r"\b(width|height|ymin|ymax|xmin|ymax|enlarge \w+ limits|xshift|yshift|inner sep|precision|opacity|fill opacity|"
           r"text opacity|column sep|row sep|scale|legend columns)\s*=\s*[^,\]]*"
           r"|\bat=\{?\([^)]*\)\}?|\bat \([^)]*\)|rel axis cs:[^)]*|axis description cs:[^)]*"
           r"|\b(?:black|gray|blue|red|white|green)!\d+")  # layout coordinates and colour mixes, not printed values
TOKEN = r"(?<![\w.])(?<!\w-)[+-]?\d[\d,]*(?:\.\d+)?%?(?![\w.])"   # (?<!\w-): NB-6, E1-R are identifiers, not numbers


def git_show(rev, rel):
    out = subprocess.run(["git", "show", f"{rev}:{rel}"], cwd=REPO, capture_output=True)
    if out.returncode:
        sys.exit(f"git show {rev}:{rel} failed: {out.stderr.decode(errors='replace').strip()}")
    return out.stdout


def tex_tokens(text):
    text = text.replace("\r\n", "\n")
    text = "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in text.split("\n"))
    b0 = text.find("\\begin{thebibliography}")
    b1 = text.find("\\end{thebibliography}")
    if b0 >= 0 and b1 >= 0:
        text = text[:b0] + "\n" * text[b0:b1].count("\n") + text[b1:]
    lines = []
    for ln in text.split("\n"):
        ln = re.sub(BLANK_ARGS, " ", ln)
        ln = re.sub(PGFOPTS, " ", ln)
        ln = re.sub(LENGTHS, " ", ln)
        ln = ln.replace("{,}", ",").replace("\\%", "%")
        lines.append(ln)
    toks = collections.Counter()
    where = collections.defaultdict(list)
    for i, ln in enumerate(lines, start=1):
        for t in re.findall(TOKEN, ln):
            toks[t] += 1
            where[t].append(i)
    return toks, where


def pdf_tokens(data):
    import fitz
    doc = fitz.open(stream=data, filetype="pdf")
    toks, where = collections.Counter(), collections.defaultdict(list)
    pat = r"(?<![\w.])[+-]?(?:\d+\.\d+%?|\d{1,3}(?:,\d{3})+|\d+%)(?![\w.])"
    for p in doc:
        for t in re.findall(pat, p.get_text()):
            toks[t] += 1
            where[t].append(p.number + 1)
    return toks, where


def figboxes(data):
    """Union of the vector drawings above each main-text figure caption, below the
    running header rule (y > 60pt), so the box is the figure itself."""
    import fitz
    doc = fitz.open(stream=data, filetype="pdf")
    out = {}
    for p in doc:
        for b in p.get_text("blocks"):
            tag = b[4][:9]
            if tag in ("Figure 1:", "Figure 2:") and tag not in out:
                cap_y = b[1]
                rs = [d["rect"] for d in p.get_drawings() if d["rect"].y0 > 60 and d["rect"].y1 <= cap_y + 1]
                if rs:
                    box = (min(r.x0 for r in rs), min(r.y0 for r in rs), max(r.x1 for r in rs), max(r.y1 for r in rs))
                    out[tag] = (p.number + 1, tuple(round(v, 1) for v in box))
    return out


def _round2_source(a, base):
    """R102 (2026-09-13, the v10 brief, rule 1.2): under --round2 an ADDED token printed at exactly
    two decimals is accepted when some base token of three or more decimals rounds to it
    (Decimal, ROUND_HALF_UP), with the same sign form and the same percent suffix. Returns the
    source token or None. VANISHED tokens are never accepted this way (rule 1.3: no v9 number
    disappears), so the amendment can only excuse a rounding whose source still prints."""
    from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
    # R103 (2026-09-13, ruling R-d): an integer percent ("42%") is accepted when a base percent token with
    # decimals ("42.3%") rounds to it, the same rule one decimal place coarser; plain numbers keep two decimals.
    pct_int = re.fullmatch(r"[+-]?\d+%", a) is not None
    if not (pct_int or re.fullmatch(r"[+-]?\d+\.\d{2}%?", a)):
        return None
    num = lambda t: Decimal(t.replace(",", "").rstrip("%"))
    for g in base:
        if pct_int:
            if not re.fullmatch(r"[+-]?\d+\.\d+%", g):
                continue
            q = Decimal("1")
        else:
            if not re.fullmatch(r"[+-]?\d+\.\d{3,}%?", g):
                continue
            q = Decimal("0.01")
        if g.endswith("%") != a.endswith("%") or (g[0] in "+-") != (a[0] in "+-"):
            continue
        if g[0] in "+-" and g[0] != a[0]:
            continue
        try:
            if num(g).quantize(q, rounding=ROUND_HALF_UP) == num(a):
                return g
        except InvalidOperation:
            continue
    return None


def report(name, base, new, where, strict, round2=False):
    bad = 0
    added = sorted(set(new) - set(base), key=lambda t: (len(t), t))
    gone = sorted(set(base) - set(new), key=lambda t: (len(t), t))
    changed = sorted(t for t in set(base) & set(new) if base[t] != new[t])
    rounded = {}
    if round2:
        rounded = {a: g for a in added for g in [_round2_source(a, base)] if g}
        added = [a for a in added if a not in rounded]
    print(f"[{name}] tokens base={sum(base.values())} new={sum(new.values())} distinct base={len(base)} new={len(new)}")
    print(f"  ADDED ({len(added)}):    " + ", ".join(f"{t} @{where[t]}" for t in added))
    if round2:
        print(f"  ROUNDED-ACCEPTED ({len(rounded)}): " + ", ".join(f"{a} <- {g} @{where[a]}" for a, g in sorted(rounded.items())))
    print(f"  VANISHED ({len(gone)}): " + ", ".join(gone))
    print(f"  COUNT-CHANGED ({len(changed)}):")
    for t in changed:
        print(f"    {t}: {base[t]} -> {new[t]} now at {where[t]}")
    bad += len(added) + len(gone) + (len(changed) if strict else 0)
    return bad


def main():
    opts = dict(a[2:].split("=", 1) if "=" in a else (a[2:], "1") for a in sys.argv[1:] if a.startswith("--"))
    if "base" not in opts:
        print(__doc__); sys.exit(2)
    texname = opts.get("tex", "paper_v8.tex")   # R92: lineage moved to v4; R93: to v5 (v4 frozen at fdd34c8); R96: to v6 (v5 is the uncommitted R93 close; the R96 base is the tree object 69c8d690 written from it); R97: to v7 (v6 is the uncommitted R96 close; the R97 base is the tree object 43531d8b written from it)
    basename = opts.get("base-tex", texname)
    rel = f"iclr2027_monitoring_submission/{basename}"
    base_tex = git_show(opts["base"], rel).decode("utf-8", errors="replace")
    new_tex = (SUB / texname).read_text(encoding="utf-8", errors="replace")
    # R103 (2026-09-13, ruling R-f): --extra-tex=SUPPLEMENT.tex appends the supplement's source (and, under --pdf,
    # its PDF's text layer) to the working side, so a number that moved from the paper to the supplement is
    # neither VANISHED nor ADDED. The base side is unchanged.
    extra = opts.get("extra-tex")
    if extra:
        new_tex += "\n" + (SUB / extra).read_text(encoding="utf-8", errors="replace")
    bt, _ = tex_tokens(base_tex)
    nt, nw = tex_tokens(new_tex)
    bad = report("tex", bt, nt, nw, "strict" in opts, "round2" in opts)
    if "pdf" in opts or "figboxes" in opts:
        pdfrel = rel[:-4] + ".pdf"
        base_pdf = git_show(opts["base"], pdfrel)
        new_pdf = (SUB / (texname[:-4] + ".pdf")).read_bytes()   # the working lineage's PDF, not the base name's
        if "pdf" in opts:
            bp, _ = pdf_tokens(base_pdf)
            np_, npw = pdf_tokens(new_pdf)
            if extra and (SUB / (extra[:-4] + ".pdf")).exists():
                ep, epw = pdf_tokens((SUB / (extra[:-4] + ".pdf")).read_bytes())
                for t, c in ep.items():
                    np_[t] = np_.get(t, 0) + c
                    npw.setdefault(t, epw[t])
            bad += report("pdf", bp, np_, npw, "strict" in opts, "round2" in opts)
        if "figboxes" in opts:
            fb, fn = figboxes(base_pdf), figboxes(new_pdf)
            for tag in sorted(set(fb) | set(fn)):
                b_, n_ = fb.get(tag), fn.get(tag)
                dims = lambda r: (round(r[1][2] - r[1][0], 1), round(r[1][3] - r[1][1], 1)) if r else None
                same = bool(b_ and n_) and all(abs(x - y) <= 0.5 for x, y in zip(dims(b_), dims(n_)))   # size within 0.5pt; position may move
                moved = "" if (b_ and n_ and b_[1] == n_[1]) else " (position moved)"
                # --figbox-accept="Figure 1,Figure 2": a dimension change authorized in the program's
                # report (R91 Phase 4 set Figure 1 at print size for the 7pt floor); printed, not failed
                accepted = (not same) and tag.rstrip(":") in [t.strip() for t in opts.get("figbox-accept", "").split(",")]
                verdict = "same" if same else ("CHANGED, ACCEPTED by --figbox-accept" if accepted else "CHANGED")
                print(f"[figbox] {tag} base={b_} new={n_} size {dims(b_)} -> {dims(n_)} {verdict}{moved}")
                bad += 0 if (same or accepted) else 1
    print("numeric_diff: " + ("PASS" if not bad else f"{bad} FAILURES"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
