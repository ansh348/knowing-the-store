r"""_pass5_identifiers.py -- replace model nicknames with full identifiers in main text.

The rewrite's note 3 asks for GPT-4.1 mini / GPT-5.6 Luna / GPT-5.6 Sol throughout, in place
of mini / luna / sol. STYLE_SPEC S3 permits the nicknames after first use, so this is a
choice rather than a gate requirement, and the plan's rule for it is measure first and land
only if the census allows.

Vendor facts verified before landing: GPT-5.6 shipped 2026-07-09 in three tiers, Luna
cheapest, then Terra, then Sol as flagship, so the paper's "ascending in size and price"
ordering for mini / luna / sol is correct as written.

MAIN TEXT ONLY, up to \label{main-text-end}. The appendices, tables and registrations keep
the nicknames: they are ledger keys there (NUMBERS.md keys MINI-FOK, LUNA-FOK and the like)
and Table 22 cites them in frozen row text.

NOT REPLACED, so the identifiers stay honest:
  - anything inside \texttt{...}, which is where the literal API strings live;
  - the roster sentence, which is rewritten instead, since spelling both the nickname and the
    identifier there becomes redundant once the identifiers are used throughout;
  - "sol" or "mini" inside another word, guarded by word boundaries and a lookbehind for the
    hyphenated API forms.

Idempotent.
"""
import io
import re
import sys
import pathlib

TEX = pathlib.Path(__file__).resolve().parents[2] / "iclr2027_monitoring_submission" / "paper_v2.tex"
END = r"\label{main-text-end}"

# Applied AFTER the nickname pass, so this is the roster as it reads once the identifiers are
# in. Running it first put "mini" back inside "GPT-4.1 mini" and produced "GPT-4.1 GPT-4.1
# mini"; the lookbehind cannot see a space-separated repeat of what it just inserted.
ROSTER_OLD = ("The models are GPT-4.1 mini, GPT-5.6 Luna, and GPT-5.6 Sol (gpt-4.1-mini, "
              "gpt-5.6-luna, gpt-5.6-sol, ascending in size and price) and three additions, each "
              "a different model family and version: Anthropic's Opus 5 and Haiku 4.5, and Kimi "
              "K3, open weights under Moonshot's custom license.")
ROSTER_NEW = ("The models are GPT-4.1 mini, GPT-5.6 Luna, and GPT-5.6 Sol, in ascending size and "
              "price. Three additions each come from a different model family and version: "
              "Anthropic's Opus 5 and Haiku 4.5, and Kimi K3, open weights under Moonshot's "
              "custom license.")

NICKS = [("mini", "GPT-4.1 mini"), ("luna", "GPT-5.6 Luna"), ("sol", "GPT-5.6 Sol")]


def protect(text):
    r"""Blank out spans that must never be rewritten.

    \texttt{...} holds the literal API strings.

    tikzpicture blocks hold the figure's axis tick labels. R83 caught this the hard way: the
    first run rewrote "symbolic x coords={mini,luna,sol}" to the full identifiers, turning
    three 4-character tick labels into three 12-character ones inside a 0.48\textwidth plot.
    It compiled and every gate passed, because the census cannot see inside a float and
    trace_scan excludes tikz blocks by design. Only reading the figure source found it.
    """
    spans = []

    def stash(m):
        spans.append(m.group(0))
        return "\x00%d\x00" % (len(spans) - 1)

    text = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", stash, text, flags=re.S)
    return re.sub(r"\\texttt\{[^}]*\}", stash, text), spans


def restore(text, spans):
    for i, v in enumerate(spans):
        text = text.replace("\x00%d\x00" % i, v)
    return text


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()
    if ROSTER_NEW in s:
        print("_pass5_identifiers: already landed")
        return 0
    cut = s.index(END)
    head, tail = s[:cut], s[cut:]

    before = len(head)
    head, spans = protect(head)
    counts = {}
    for nick, full in NICKS:
        pat = re.compile(r"(?<![-\w])" + nick + r"(?![-\w])")
        head, n = pat.subn(full, head)
        counts[nick] = n
    head = restore(head, spans)
    if ROSTER_OLD not in head:
        print("ABORT: post-substitution roster anchor not found; nothing written")
        return 1
    head = head.replace(ROSTER_OLD, ROSTER_NEW, 1)

    io.open(TEX, "w", encoding="utf-8", newline="").write(head + tail)
    for nick, full in NICKS:
        print("  %-5s -> %-13s x%d" % (nick, full, counts[nick]))
    print("_pass5_identifiers: main text net %+d characters" % (len(head) - before))
    return 0


sys.exit(main())
