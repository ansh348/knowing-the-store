r"""frozen_diff -- every mechanically frozen string, before and after an edit.

WHY. The frozen-sentence list lives in four places: CLAIMS.md (U-blocks and the quoted
fragments inside CL TEXT lines and dated authorization blocks), claims_diff.U_BLOCKS,
slogan_scan's PINNED and EXEMPT lists, and prose_scan's WHITELIST. claims_diff checks
U1-U7 exactly once; nothing checks that the other strings survive an edit. This tool
collects them all, records which occur verbatim in a committed revision of the
manuscript, and reports any whose occurrence count differs in the working copy.

A changed string is AUTHORIZED when it is quoted inside the program's own dated
`## <program> AUTHORIZATION BLOCK` in CLAIMS.md, which is where every touched frozen
sentence is recorded; otherwise it is UNAUTHORIZED and the tool fails. A string whose
count is unchanged but whose first line moved is MOVED (information only).

LIMIT, stated so nobody reads PASS as more than it is: CL TEXT lines that paraphrase a
claim rather than quote it are not protected here; STRENGTH remains a human reading, as
claims_diff already says. slogan_scan runs its scan at import, so its lists are read
with ast rather than imported.

NORMALIZATION (both sides): CRLF -> LF; comments stripped; `$` removed; `\%` -> `%`;
`~` -> space; `{,}` -> `,`; LaTeX quote forms -> `"`; \trueidx{} \believed{} \pn{}
\present{} \absent{} -> TRUE BELIEVED PN PRESENT ABSENT; \texttt|\emph|\textbf{x} -> x;
whitespace collapsed; \ref{...} kept.

REGISTRATION TEXT (source R, added at R91 Phase 1). Every blockquote paragraph in
ARTIFACT/registrations/*.md is split into sentences, each sentence into the fragments
between its placeholders ($X$, $Y$, $D$ and the like), and every fragment of MIN_LEN+
characters that occurs verbatim in the base manuscript is a frozen string: that is how a
landed branch sentence such as the NB6-1 failure text is watched without a hand-kept list.
  R111 (2026-09-15, the writing pass; the author's ruling on the Phase 2 report): a blockquote is any run of
  '>'-prefixed lines, whatever precedes it. The earlier split at a newline not followed by '>' saw a block only
  after a blank line, so a quoted registered text glued to its heading (ADDENDUM_SIDE.md's S2-U branch text) was
  invisible here and reached the gate through an older CLAIMS quote alone; an edit to it was caught that way and
  reverted. registration_fragments() is the one parser now, shared by the pass's own tools.

Usage:
    python tools/frozen_diff.py --base=<git rev> --program=R98 [--tex=paper_v8.tex] [--base-tex=paper_v7.tex]
    --base-tex names the manuscript to read at the base revision when the lineage file was renamed
    (R92: paper_v4.tex against paper_v3.tex at abac307; R93: paper_v5.tex against paper_v4.tex at fdd34c8;
    R96: paper_v6.tex against paper_v5.tex at the tree object 69c8d690, written from the uncommitted v5;
    R97: paper_v7.tex against paper_v6.tex at the tree object 43531d8b, written from the uncommitted v6;
    R98: paper_v8.tex against paper_v7.tex at the tree object a66254cb, written from the uncommitted v7); it defaults to --tex.
Exit 0 iff zero UNAUTHORIZED changes; 1 otherwise; 2 usage.
"""
import re, sys, ast, pathlib, subprocess, collections

HERE = pathlib.Path(__file__).resolve().parent
SUB = HERE.parent
REPO = SUB.parent
sys.path.insert(0, str(HERE))
MIN_LEN = 30


def norm(s):
    s = s.replace("\r\n", "\n")
    s = "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in s.split("\n"))
    for a, b in (("\\trueidx{}", "TRUE"), ("\\believed{}", "BELIEVED"), ("\\pn{}", "PN"),
                 ("\\present{}", "PRESENT"), ("\\absent{}", "ABSENT"), ("\\%", "%"), ("{,}", ","),
                 ("~", " "), ("``", '"'), ("''", '"'), ("\u201c", '"'), ("\u201d", '"'),
                 ("\u2019", "'"), ("\u2014", "---"), ("\u2013", "--")):
        s = s.replace(a, b)
    s = re.sub(r"\\(texttt|emph|textbf|textit)\{([^}]*)\}", r"\2", s)
    s = s.replace("$", "")
    return re.sub(r"\s+", " ", s).strip()


def git_show(rev, rel):
    out = subprocess.run(["git", "show", f"{rev}:{rel}"], cwd=REPO, capture_output=True)
    if out.returncode:
        sys.exit(f"git show {rev}:{rel} failed: {out.stderr.decode(errors='replace').strip()}")
    return out.stdout.decode("utf-8", errors="replace")


def ast_lists(path, names):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in names:
                try:
                    out[node.targets[0].id] = ast.literal_eval(node.value)
                except ValueError:
                    pass
    return out


def quoted(text):
    """Double-quoted fragments of MIN_LEN+ characters. Wrapped lines are joined first and
    quotes are paired in order within each paragraph (1st with 2nd, 3rd with 4th), so a
    short quote never swallows the opening quote of the long one after it."""
    out = []
    for para in re.split(r"\n\s*\n", text):
        joined = para.replace("\n", " ")
        pos = [m.start() for m in re.finditer('"', joined)]
        for a, b in zip(pos[0::2], pos[1::2]):
            frag = joined[a + 1:b]
            if len(frag) >= MIN_LEN:
                out.append(frag)
    return out


def registration_fragments():
    """(file name, fragment) for every blockquote of ARTIFACT/registrations/*.md: a blockquote is any run of '>'-prefixed
    lines, whatever precedes it (R111); each is split into sentences and each sentence into the fragments between its
    placeholders ($X$, $Y$, $D$ and the like); fragments of MIN_LEN+ characters are returned, unnormalized."""
    out = []
    for reg in sorted((SUB / "ARTIFACT" / "registrations").glob("*.md")):
        blocks, cur = [], []
        for ln in reg.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").split("\n"):
            if ln.lstrip().startswith(">"):
                cur.append(ln.lstrip()[1:].strip())
            elif cur:
                blocks.append(" ".join(cur)); cur = []
        if cur:
            blocks.append(" ".join(cur))
        for text in blocks:
            for sent in re.split(r"(?<=[.!?])\s+", text):
                for frag in re.split(r"\$[A-Z](?:_\w+)?\$", sent):
                    frag = frag.strip(" ,;:")
                    if len(frag) >= MIN_LEN:
                        out.append((reg.name, frag))
    return out


def claims_sections(claims, program):
    """(outside, inside): CLAIMS.md text outside and inside the program's block."""
    m = re.search(r"^## %s AUTHORIZATION BLOCK.*?(?=^## |\Z)" % re.escape(program), claims, flags=re.S | re.M)
    if not m:
        return claims, ""
    return claims[:m.start()] + claims[m.end():], m.group(0)


def main():
    opts = dict(a[2:].split("=", 1) if "=" in a else (a[2:], "1") for a in sys.argv[1:] if a.startswith("--"))
    if "base" not in opts or "program" not in opts:
        print(__doc__); sys.exit(2)
    texname = opts.get("tex", "paper_v8.tex")   # R92: lineage moved to v4; R93: to v5 (v4 frozen at fdd34c8); R96: to v6 (v5 is the uncommitted R93 close; the R96 base is the tree object 69c8d690 written from it); R97: to v7 (v6 is the uncommitted R96 close; the R97 base is the tree object 43531d8b written from it)
    basename = opts.get("base-tex", texname)
    base = norm(git_show(opts["base"], f"iclr2027_monitoring_submission/{basename}"))
    new_raw = (SUB / texname).read_text(encoding="utf-8", errors="replace")
    # R103 (2026-09-13, ruling R-f): --extra-tex=SUPPLEMENT.tex appends the supplement's source to the working
    # side, so a frozen string that moved from the paper to the supplement reports MOVED rather than CHANGED.
    if opts.get("extra-tex"):
        new_raw += "\n" + (SUB / opts["extra-tex"]).read_text(encoding="utf-8", errors="replace")
    new = norm(new_raw)
    claims = (SUB / "CLAIMS.md").read_text(encoding="utf-8", errors="replace")
    outside, inside = claims_sections(claims, opts["program"])
    auth = {norm(q) for q in quoted(inside)}

    import claims_diff, prose_scan
    src = []
    src += [("U", k, v) for k, v in claims_diff.U_BLOCKS.items()]
    sl = ast_lists(HERE / "slogan_scan.py", {"PINNED", "EXEMPT_S8", "EXEMPT_S9", "EXEMPT_S10", "EXEMPT_FROZEN_REGISTERED"})
    src += [("S", k, v) for k, vs in sl.items() for v in vs]
    src += [("W", f"WHITELIST[{i}]", w[0]) for i, w in enumerate(prose_scan.WHITELIST)]
    src += [("Q", "CLAIMS", q) for q in quoted(outside)]
    src += [("R", name, frag) for name, frag in registration_fragments()]

    seen, rows, per_src = set(), [], collections.Counter()
    for tag, key, text in src:
        t = norm(text)
        if len(t) < 8 or t in seen:
            continue
        seen.add(t)
        nb, nn = base.count(t), new.count(t)
        if nb == 0:
            continue  # not a manuscript string (a slogan_scan structural entry, or a CLAIMS quote of a ledger)
        per_src[tag] += 1
        if nb == nn:  # MOVED when the 40 characters before the first occurrence changed
            ib, inn = base.find(t), new.find(t)
            status = "KEPT" if base[max(0, ib - 40):ib] == new[max(0, inn - 40):inn] else "MOVED"
        else:
            status = "CHANGED-AUTHORIZED" if any(t in a or a in t for a in auth) else "CHANGED-UNAUTHORIZED"
        rows.append((status, tag, key, nb, nn, t))

    counts = collections.Counter(r[0] for r in rows)
    print(f"frozen strings found in base: {len(rows)} " + " ".join(f"{k}={v}" for k, v in sorted(per_src.items())))
    print("  " + " ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    for status, tag, key, nb, nn, t in rows:
        if status != "KEPT":
            print(f"  {status} [{tag} {key}] {nb} -> {nn} :: {t[:100]}")
    bad = counts.get("CHANGED-UNAUTHORIZED", 0)
    print("frozen_diff: " + ("PASS" if not bad else f"{bad} UNAUTHORIZED"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
