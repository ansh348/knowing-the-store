r"""sentence_census -- R91 readability census of the main text (report, one optional gate).

WHY. prose_scan rule L has enforced the 40-word cap since R79, so the paper carries no
sentence over 40 words and "the count over 40 falls by half" cannot measure a prose pass.
R91 needs the distribution instead: per-section count, mean, median, the sentences over
30 words (R91 rule R8's target), four-decimal numbers in body prose, the artifact
vocabulary R91 Phase 1 replaces, and appendix pointers per paragraph.

REGION AND SPLIT. Identical to prose_scan: \begin{document} .. \label{main-text-end},
comments stripped, tikzpicture/tabular/instrument boxes excised, WHITELIST strings excised,
same sentence regex and the same _words. The extraction below is COPIED FROM
prose_scan.run() @664a460 rather than refactored out of it, so the gate is not edited
in flight; the copy is verified by reproducing prose_scan's "M mean sentence length"
line exactly (20.5 words over 222 sentences at the R91 baseline).

Paragraphs are LaTeX paragraphs: a blank raw line ends one; a comment-only line neither
ends nor counts. Four-decimal counting excludes \caption{...} (brace-matched) and every
excised block, so it measures body prose only.

Usage:
    python tools/sentence_census.py paper_v8.tex [--md] [--sections=S4,S5,S6]
                                                 [--max-over30=N]
Exit 0, except --max-over30=N exits 1 when the over-30 count in --sections exceeds N.
"""
import re, sys, pathlib, statistics
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from prose_scan import _strip_comments, _words, SEC_LABEL, WHITELIST  # noqa: E402

LEDGER_VOCAB = [(r"\bprints?\b|\bprinted\b", "prints"), (r"\bcells?\b", "cell"),
                (r"\blanes?\b", "lane"), (r"\barms?\b", "arm"), (r"\bcommitted\b", "committed"),
                (r"\bregistrations?\b", "registration"), (r"\bledgers?\b", "ledger")]
SET_NAMES = [(r"\$?84\$?-question set|cross-model (set|cell)", "84-set"),
             (r"\$?36\$?-question set|one-voice set|authorship-matched (set|slice|cell)", "36-set"),
             (r"store-counterfactual set|counterfactual set|\$?90\$?-question", "90-set"),
             (r"\$?661\$?-question population|full FR-Bank question sets|full populations?", "661/307")]


def load(tex_path):
    raw = pathlib.Path(tex_path).read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    stripped = [_strip_comments(l) for l in raw]
    find = lambda pred: next((i for i, l in enumerate(raw) if pred(l)), None)
    doc0 = find(lambda l: l.startswith("\\begin{document}"))
    mend = find(lambda l: "\\label{main-text-end}" in l)
    abs0, abs1 = find(lambda l: "\\begin{abstract}" in l), find(lambda l: "\\end{abstract}" in l)
    secs, cur, order = {}, "front", []
    for i in range(doc0, mend + 1):
        m = re.match(r"\\section\{([^}]*)\}", stripped[i])
        if i <= abs1:
            cur = "Abs"  # front matter carries no prose; the title line opens the abstract's first sentence
        elif m:
            cur = SEC_LABEL.get(m.group(1)) or ("S6" if order and order[-1] == "S5" else m.group(1))
            order.append(cur)
        secs[i] = cur
    return raw, stripped, doc0, mend, secs


def sentences(raw, stripped, doc0, mend, secs):
    # COPIED FROM prose_scan.run() @664a460 (sentence extraction block)
    body, skip, in_box = [], 0, False
    for i in range(doc0, mend + 1):
        l = stripped[i]
        if re.search(r"\\begin\{(tikzpicture|tabular)\}", l):
            skip += 1
        if "\\fbox{" in l:
            in_box = True
        if skip == 0 and not in_box:
            body.append((i, l))
        if in_box and "\\end{minipage}}" in l:
            in_box = False
        if re.search(r"\\end\{(tikzpicture|tabular)\}", l):
            skip = max(0, skip - 1)
    joined = " ".join(f"\x00{i}\x00 {l}" for i, l in body if l.strip())
    joined = re.sub(r"\s+", " ", joined)
    for s, _, _, _ in WHITELIST:
        joined = joined.replace(re.sub(r"\s+", " ", s), " ")
    joined = re.sub(r"\\label\{[^}]*\}", " ", joined)
    joined = re.sub(r"\\(sub)*section\*?\{[^}]*\}", " . ", joined)
    joined = re.sub(r"\\(begin|end)\{[a-zA-Z*]+\}(\[[^\]]*\])?", " ", joined)
    joined = re.sub(r"\\(label|vspace|hspace|resizebox|setlength|caption|item|centering|"
                    r"scriptsize|footnotesize|small|tiny|noindent|par|smallskip|FloatBarrier|"
                    r"protect|textsuperscript|multicolumn|toprule|midrule|bottomrule|fbox|"
                    r"ttfamily|textbf|textit|emph)\b(\[[^\]]*\])?", " ", joined)
    joined = re.sub(r"(?<![\\\w])[{}](?!\w)", " ", joined)
    joined = joined.replace("\\,", " ")
    joined = re.sub(r"(?<![\w\\])\*(?![\w])", " ", joined)
    out = []
    for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\\$\x00(`])", joined):
        m = re.search(r"\x00(\d+)\x00", s)
        ln = int(m.group(1)) if m else None
        sc = re.sub(r"\x00\d+\x00", " ", s).strip()
        w = _words(sc)
        if len(w) >= 4 and ln is not None:
            out.append((ln, secs.get(ln, "?"), re.sub(r"  +", " ", sc), w))
    return out


def body_prose(raw, stripped, doc0, mend):
    """(line, text) for body prose only: no captions, tabular, tikz, figure/table envs.
    Excised spans are replaced by their own newlines so line numbers are preserved."""
    text = "\n".join(stripped[doc0:mend + 1])
    blank = lambda m: "\n" * m.group(0).count("\n")
    text = re.sub(r"\\begin\{(tikzpicture|tabular|figure|table|center)\}.*?\\end\{\1\}", blank, text, flags=re.S)
    while True:  # brace-matched \caption{...}
        j = text.find("\\caption{")
        if j < 0:
            break
        k, depth = j + len("\\caption{"), 1
        while k < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[k], 0); k += 1
        text = text[:j] + "\n" * text[j:k].count("\n") + text[k:]
    return list(enumerate(text.split("\n"), start=doc0))


def paragraphs(raw, stripped, doc0, mend, secs):
    paras, cur = [], []
    for i in range(doc0, mend + 1):
        if raw[i].strip() == "":
            if cur:
                paras.append(cur); cur = []
        elif not raw[i].lstrip().startswith("%"):
            cur.append(i)
    if cur:
        paras.append(cur)
    out = []
    for p in paras:
        refs = [r for i in p for r in re.findall(r"\\ref\{(app:[^}]*)\}", stripped[i])]
        out.append((p[0] + 1, p[-1] + 1, secs.get(p[0], "?"), refs))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) if "=" in a else (a[2:], "1") for a in sys.argv[1:] if a.startswith("--"))
    if not args:
        sys.exit("usage: sentence_census.py paper_v8.tex [--md] [--sections=S4,S5] [--max-over30=N]")
    raw, stripped, doc0, mend, secs = load(args[0])
    sents = sentences(raw, stripped, doc0, mend, secs)
    order = ["Abs", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
    P = print
    P("| section | sentences | mean | median | >30 | >40 |"); P("|---|---|---|---|---|---|")
    for sec in order + ["ALL"]:
        ws = [len(w) for _, s, _, w in sents if sec == "ALL" or s == sec]
        if ws:
            P(f"| {sec} | {len(ws)} | {statistics.mean(ws):.1f} | {statistics.median(ws):g} | "
              f"{sum(x > 30 for x in ws)} | {sum(x > 40 for x in ws)} |")
    P(f"\nM mean sentence length: {statistics.mean(len(w) for *_, w in sents):.1f} words over {len(sents)} sentences (prose_scan cross-check)")
    for cap, title in ((40, "over 40"), (30, "over 30")):
        P(f"\nSentences {title} words:")
        for ln, sec, sc, w in sents:
            if len(w) > cap:
                P(f"  L{ln + 1} {sec} {len(w)}w :: {sc[:110]}")
    prose = body_prose(raw, stripped, doc0, mend)
    P("\nFour-decimal numbers in body prose (captions and tables excluded):")
    for sec in order:
        n = sum(len(re.findall(r"(?<![\d.])[+-]?\d\.\d{4}(?!\d)", l)) for i, l in prose if secs.get(i) == sec)
        P(f"  {sec}: {n}")
    P("\nLedger vocabulary in body prose (label names excluded):")
    for pat, name in LEDGER_VOCAB + SET_NAMES:
        hits = [(i + 1, secs.get(i)) for i, l in prose
                if re.search(pat, re.sub(r"\\(ref|label)\{[^}]*\}", " ", l), flags=re.I)]
        P(f"  {name}: {len(hits)} " + " ".join(f"L{a}({b})" for a, b in hits))
    P("\nParagraphs with two or more appendix pointers:")
    for a, b, sec, refs in paragraphs(raw, stripped, doc0, mend, secs):
        if len(refs) >= 2:
            P(f"  L{a}-{b} {sec}: {len(refs)} :: {', '.join(refs)}")
    if "max-over30" in opts:
        want = set(opts.get("sections", ",".join(order)).split(","))
        n = sum(1 for _, s, _, w in sents if s in want and len(w) > 30)
        P(f"\nover-30 count in {sorted(want)}: {n} (max {opts['max-over30']})")
        sys.exit(1 if n > int(opts["max-over30"]) else 0)


if __name__ == "__main__":
    main()
