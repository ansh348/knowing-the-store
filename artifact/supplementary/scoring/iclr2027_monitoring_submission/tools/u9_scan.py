"""u9_scan -- mechanical enforcement of CLAIMS.md U9.

U9 was, until this tool, the last rule in the constitution with no mechanical enforcement. It
lived as three source comments and depended on a human noticing.

WHAT U9 ACTUALLY FORBIDS. Ruled from the constitution rather than inferred:

  CLAIMS.md:142  "U9: the retention<->flat-lookup LINK stays UNdrawn ... Drawing it in prose
                  is a VIOLATION."

  CLAIMS.md:202  "the link between the BELIEVED NOK retention and the flat-lookup mechanism
                  bound remains undrawn. R81 may place the two findings in ADJACENT
                  SENTENCES; it may not assert that ONE EXPLAINS THE OTHER. NB-6 does not
                  license that link."

  paper.tex:1220 the protected comment itself: "this flat-lookup reading is also consistent
                  with the BELIEVED-index NOK retention of 42.3% and with the
                  embedding-matcher tie ... Registering that link is R-DS scope."

So the prohibition is a CAUSAL OR IDENTITY JOIN, not co-occurrence. Two findings may sit in
one sentence; what may not be said is that the retention is explained by, or is the same
thing as, the flat-lookup bound. A pure co-occurrence rule would be wrong in both directions:
it would fire on constitutionally vetted prose, and it would miss an explanatory join spread
across a semicolon.

WHY THE ALLOWLIST HAS EXACTLY ONE ENTRY. Appendix F.8 contains a sentence tying the retention
to the EMBEDDING-matcher tie with an explicit independence qualifier ("reached by an
independent route"). It is inherited verbatim from the frozen paper.tex, where CLAIMS.md:1075
records that the only occurrence of the forbidden link is the comment above. It is therefore
vetted, and it names the wrong reader to be the forbidden link in any case: NB-5 the embedding
matcher, not NB-6 the flat lookup. It is pinned by sentence hash so that editing it re-opens
the question rather than inheriting this clearance.

THE QUALIFIER LIST IS THE WEAK POINT, AND IT IS A RULING RATHER THAN A SETTING. Reading 2
makes an independence qualifier a pass condition, so the tool can be defeated by attaching
"reached by an independent route" to a sentence that still asserts explanation. That is
tolerable only because INDEPENDENCE is tiny and every entry in it was adjudicated against the
constitution. Extending it is therefore a CONSTITUTIONAL CHANGE and needs a CLAIMS.md
departure, not an edit to this file. The same holds for ALLOW, which is empty on purpose. A
later session that widens either list to make a particular sentence pass has amended U9 by
editing a scanner, which is the failure this tool exists to prevent.

COMMENTS ARE STRIPPED FIRST. The three U9 firewall notes each mention the retention and the
lookup in one line, by design. Scanning them would make the tool fire on the very annotations
that record the rule.

SCOPE. The whole document, main text and appendix. U9 is not scoped to main text.

Usage:
    python tools/u9_scan.py [manuscript.tex]     defaults to paper_v8.tex
Exit 1 on any unallowlisted join.
"""
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT = HERE.parent / "paper_v8.tex"   # R90: lineage moved to v3; R92: to v4; R93: to v5 (v4 frozen at fdd34c8); R96: to v6; R97: to v7; R98: to v8

RETENTION = re.compile(r"42\.3")

# the flat-lookup mechanism bound, by any name the manuscript uses for it
LOOKUP = re.compile(
    r"\bNB-?6\b|superseded-names matcher|flat lookup|flat-lookup|direct lookup|"
    r"\bReader 6\b|lookup on the superseded|names it marks superseded|"
    # The protected comment names the embedding-matcher tie as part of the same unregistered
    # link, so matcher referents are in scope for DETECTION. Whether any given sentence is a
    # violation is then decided by the join and independence tests below, not here.
    r"embedding matcher|similarity matcher", re.I)

# a join asserting that one accounts for the other
JOIN = re.compile(
    r"\bwhich is\b|\bbecause\b|\bexplains?\b|\bexplained by\b|\baccounts for\b|"
    r"\breflects\b|\bis the same\b|\bthe same as\b|\btherefore\b|\bhence\b|"
    r"\bso that\b|\bthus\b|\bshows that\b|\bmeans that\b|\bdue to\b|\bowing to\b", re.I)

# language that marks the two as separately measured rather than one explaining the other
INDEPENDENCE = re.compile(
    r"independent route|independently|adjacent finding|no connective|"
    r"separate measurement|two measurements", re.I)

# sentence sha256 -> why it is cleared
ALLOW = {
    # Empty by design. The one sentence tying the retention to a matcher clears on its own
    # merits, by naming the embedding matcher rather than the flat lookup and by carrying an
    # independence qualifier. A standing waiver here would be the same failure appendix_identity
    # had before R83: authorization that outlives the thing it authorized.
}


def strip_comments(tex):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in tex.split("\n"))


def sentences(tex):
    tex = re.sub(r"\s+", " ", tex)
    parts, buf = [], ""
    for tok in re.split(r"(?<=[.:;])\s+", tex):
        buf = (buf + " " + tok).strip() if buf else tok
        if re.search(r"[.;:]$", tok):
            parts.append(buf)
            buf = ""
    if buf:
        parts.append(buf)
    return parts


def digest(s):
    return hashlib.sha256(" ".join(s.split()).encode("utf-8")).hexdigest()


def main():
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    tex = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
    body = tex[tex.index("\\begin{document}"):]

    hits, cleared = [], []
    for s in sentences(body):
        if not (RETENTION.search(s) and LOOKUP.search(s)):
            continue
        h = digest(s)
        joined = JOIN.search(s)
        independent = INDEPENDENCE.search(s)
        if h in ALLOW:
            cleared.append((h, s, ALLOW[h]))
        elif joined and not independent:
            hits.append((h, s, joined.group(0)))
        else:
            cleared.append((h, s, "co-occurrence without an explanatory join"
                            if not joined else "join carries an independence qualifier"))

    print("u9_scan: %s" % path.name)
    print("scope: whole document, LaTeX comments stripped")
    print("co-occurrences of the retention figure and the flat-lookup bound: %d"
          % (len(hits) + len(cleared)))

    for h, s, why in cleared:
        print("\n  CLEARED  %s" % why)
        print("           %s" % (s[:160] + ("..." if len(s) > 160 else "")))
        print("           sha256 %s" % h)
    for h, s, tok in hits:
        print("\n  VIOLATION  explanatory join on %r with no independence qualifier" % tok)
        print("             %s" % (s[:200] + ("..." if len(s) > 200 else "")))
        print("             sha256 %s" % h)

    if hits:
        print("\nFAIL -- %d U9 violation(s): the retention is joined to the flat-lookup bound"
              % len(hits))
        return 1
    print("\nPASS -- the retention<->flat-lookup link is undrawn")
    return 0


if __name__ == "__main__":
    sys.exit(main())
