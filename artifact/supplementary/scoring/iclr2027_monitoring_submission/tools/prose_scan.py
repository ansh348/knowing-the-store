r"""prose_scan -- R79 plain-language gates for the paper_v2 lineage.

R112 (2026-09-16, the integration pass; CLAIMS.md R112 block): rule G4's anchor regex also accepts the narrowed thesis sentence ("the attribute
names carry most of the signal"), the author's correction of 2026-09-16 that replaced "read it by its names and not by its counts".
R111 (2026-09-15, the writing pass on paper_v18; CLAIMS.md R111 block): rule G4's anchor regex also accepts Section 1's
approved thesis sentence ("read a lifecycle summary by its names and not by its counts"). Reason: item 7 of the pass deletes
the four-finding paragraph that carried "name readers", the only anchor form the regex matched; the thesis sentence is the
reader claim itself and precedes the first mention of tags. The author's ruling: that sentence specifically, no wider form.

Called from slogan_scan.py (and runnable standalone). Scans the MAIN TEXT of
paper_v2.tex (\begin{document} through \label{main-text-end}: abstract through
Section 8, captions and footnotes included; comments stripped) and the appendices.

Checks (R79 Phase 1 spec):
  V   vocabulary: zero hits against the R79 Phase 0 internal-vocabulary list;
  H   hedge phrases: zero hits against the R79 hedge-phrase list;
  P   the word "preregistered": hard cap 4 in main text (reported with locations);
  L   sentences over 40 words: zero (math blob / cite / ref count as one word);
  M   mean sentence length: reported, target <= 22 (report only);
  D   near-duplicate sentence pairs sharing > 70% of tokens (overlap coefficient,
      intersection over the smaller token set, sentences of 7+ words): zero;
  PAR parentheticals over 10 words: reported (report only);
  A   appendix registration codes: allowed only in Appendix E (ledger), Appendix G
      (registration record + deviation index), inside tabular cells, and inside a
      parenthetical pointer that names the registration record
      (\ref{app:registration} or \ref{tab:registrations}). Anything else is a hit.
      Interpretation note (R79 report): NB-n are baseline instrument names, not
      registration codes, and are excluded from the appendix rule (they remain
      banned in main text); tabular-cell allowance covers appendices B-G because
      NB-n/P-n/E1 label columns and rows in F as well as B-D.
  G   reader-claim gate (R110, the author's ruling of 2026-09-14). Finding 1 is a claim
      about readers (the models read the summary as a name list and nothing else); the
      main text may not frame it as definitional, a sanity check, a tautology, or as a
      bound the summary sets, and the lookup is the ruler, never the headline. NO
      ALLOWLIST: the whitelist is not scrubbed for this rule, instrument boxes are
      scanned, and the one Section 5 clause CC_PASS_v18 allowed ("...is expected; the
      set measures whether...") is withdrawn. Four checks:
        G1 banned phrases in the main text (abstract included): "sanity check",
           "rather than its finding", "definitional", "tautolog-", "what the store
           writes about itself", "bounds what any reader", "boundary between named and
           counted states", "lies past that check", "undetectable"; and any line that
           names the lookup and calls its result expected, unsurprising or trivial.
           Appendix hits are reported, not gated.
        G2 no abstract sentence gives the lookup's own AUROC level ("at $0.xx$", "$0.xx$ AUROC",
           "with $0.xx$", "reaches $0.xx$"). R124 (2026-09-19) narrowed the rule to this, the
           14 September ruling's meaning; until then every abstract sentence carrying a math-mode
           numeral (a decimal or count; a percentage is not one, the ruling of 2026-09-15) also had
           to name the lookup and state a difference against it.
        G3 no labelled definition environment titled "Names, counts, reads": that
           vocabulary lives in the glossary.
        G4 in Section 1 the reader-claim anchor ("read names" / "name readers" / "list of
           names") precedes the first mention of tags; a Section 1 without the anchor fails.

HELD REGION: NONE, since 2026-09-09 (R86 Phase 3, D-R86-10). The abstract and Section 1
were [AUTHOR-1]-held during R79 so that a proposal could be written without the gate firing on
text nobody had landed yet. Both landed (the abstract at aa25e4e, Section 1 at 116211f), and
this file's own instruction was to delete the carve-out once they did. R86 adds prose to
Section 1 (items 3.1 and 2.7), which would otherwise have gone ungated. The whole main text
now gates.

GATE SCOPE. tools/prose_gate_sections.txt lists the sections currently under gate
(e.g. "S2,S3,S4"), reflecting the R79 Phase 2 commit sequence; "NONE" gates nothing
(Phase 1 state); "ALL" or a missing file gates every non-held section plus the
appendix rule. Phase 5 deletes the file so the strict gate is permanent.

WHITELIST. Byte-frozen strings (CLAIMS.md EXACTLY-ONCE blocks, frozen registered
branch wording, ordered R79 sentences) that trip a gate are excised before scanning;
each entry names its class and the gate it trips, and the R79 report lists them.
"""
import re, pathlib, sys, itertools

def whitelist_authority():
    """R83. Verify every entry that CLAIMS an external authority actually has one.

    WHY. Two entries were labelled FROZEN-REGISTERED (X4 cap-stop) and neither phrase
    appears anywhere in registrations/. ADDENDUM_R74 section X4 freezes the cap-stop
    BRANCH BEHAVIOUR -- completed lanes print, the 84-item table stays primary, section 5.2
    gains one sentence citing the completed expanded lanes -- and it quotes verbatim text
    only for the NON-CONFIRMING branch, which did not fire. What fixes those two sentences
    is CLAIMS.md's CL-XV entry, and CLAIMS.md fixes STRENGTH, not bytes: "the rewrite may
    reorganize, reword, cut repetition, and change emphasis". Their wording was therefore
    always free, and the mislabel is what blocked a plain-language substitution in Pass 4.

    An entry naming a source file must be findable there. An entry naming none is declaring
    that its authority is a claim's strength rather than a frozen string, which leaves it
    reworadable.
    """
    import pathlib as _p
    root = _p.Path(__file__).resolve().parents[2]
    rows, bad = [], []
    for text, cls, gate, src in WHITELIST:
        if src is None:
            rows.append(("REWORDABLE", cls, "authority is claim strength, not a frozen string"))
            continue
        if not str(src).endswith(".md") or "/" not in str(src):
            rows.append(("IN-CLAIMS ", cls, str(src)))
            continue
        path = root / src
        frag = " ".join(text.split()[-6:]).rstrip('."')
        found = path.exists() and frag in path.read_text(encoding="utf-8", errors="replace")
        rows.append(("SOURCED  " if found else "MISLABELED", cls, "%s :: %r" % (src, frag)))
        if not found:
            bad.append(cls)
    return rows, bad


# ---- whitelist: frozen or ordered strings excised before every check ----------------
WHITELIST = [
    # (string, class, gate it would trip)
    ("Scope: the negative index effect is measured; the single-channel ablations do not identify its cause.",
     "BYTE-IDENTICAL U2", "hedge 'Scope:' + vocab single-channel",
     "CLAIMS.md U2"),
    ("The candidate mechanisms in Section~\\ref{sec:inversion} remain unresolved after the registered single-channel probe.",
     "BYTE-IDENTICAL U3", "vocab registered + single-channel",
     "CLAIMS.md U3"),
    ("which we record as a failed prediction",
     "BYTE-IDENTICAL U6", "hedge 'ships as' + vocab registered",
     "CLAIMS.md U6"),
    ("Permuting which counts and attribute-name lists belong to which category changes neither judgment, which bounds the mechanism rather than that specificity---per-category correspondence is not necessary on FR-Bank, consistent with the name map rather than the count structure carrying the effect (Definition~\\ref{def:index}), though the shuffle preserves the global name and count multiset and the flat superseded-names section and so bounds correspondence alone.",
     "BYTE-IDENTICAL U7", "sentence over 40 words",
     "CLAIMS.md U7"),
    ("All confirmatory claims were preregistered before data collection; Appendix~\\ref{app:registration} lists every registered prediction and its outcome, and any result we label exploratory was not preregistered.",
     "ORDERED-R79 (2b consolidation sentence)", "vocab registered (its two 'preregistered' still count toward the cap)",
     None),
    ("four ladder predictions held",
     "ORDERED-R79 (2e worked example)", "vocab held-as-outcome",
     None),
    ("On the authorship-matched cell the Haiku 4.5 blind NOK point stays below chance while its interval includes chance, so the matched cell is indeterminate at $n=36$ on whether the inverted prior of XV-1 reflects a property of the model or of question authorship; XV-1's registered verdict is unchanged",
     "FROZEN-REGISTERED (NS-5 branch iii, App C)", "appendix code XV-1",
     "registrations/ADDENDUM_R76.md"),
    # R97 (2026-09-13): the SIDE registration's frozen texts print in Section 5.3 under ADDENDUM_SIDE.md
    # Amendment 1 (R78-2c: frozen registered wording ships verbatim; style yields). Sourced to the file
    # that carries the last six words on one line (the registration wraps the Mem0 text mid-sentence).
    ("Given the manifest's names for what it holds, the store no longer inverts the benefit by the margin it did; the inversion was a property of the index the store was handed, not of the store alone.",
     "FROZEN-REGISTERED (SIDE S1-P1 held reading, Section 5.3)", "S9 contrastive ', not '",
     "registrations/ADDENDUM_SIDE.md"),
    ("On Mem0 the name-bearing index could be built for $49.4$ percent of the store's entries under the lexical-required mapping the spot-check forced (two-channel precision $0.567$); below the registered coverage floor of one half, its coverage gain of $+0.3006$ (interval $[+0.2208,+0.3728]$; \\trueidx{} $-0.0969$) is reported and carries no verdict.",
     "FROZEN-REGISTERED (SIDE Mem0 descriptive text, Section 5.3)", "vocab registered + verdict; sentence over 40 words",
     "side_experiments/NUMBERS_SIDE.md"),
    # R98 (2026-09-13): the CF-2 registration's frozen P1 HOLDS [MAIN] sentence prints in Section 7
    # (registrations/ADDENDUM_CF2.md section 8; R78-2c). It runs to 46 words. Sourced to the ledger line
    # that carries the printed form (NUMBERS_CF2.md section 5k, "Printed forms").
    ("On $148$ questions written before any version of the store existed, and asked of three versions of the same store that differ in one attribute each, the smallest model's obligation judgment reaches $0.7167$ against the $0.5$ a question-only reader attains here, with an interval of $[+0.1494,+0.2846]$.",
     "FROZEN-REGISTERED (CF-2 P1 held reading, Section 7)", "sentence over 40 words",
     "r82_counterfactual/cf2/NUMBERS_CF2.md"),
    # R101 (2026-09-13): the DS registration's frozen Section 7 paragraph (registrations/ADDENDUM_DS.md section PAPER,
    # frozen a5a2036; R78-2c) and the RESP registration's frozen L1-P1 held reading (ADDENDUM_RESP.md section L1);
    # both carry program vocabulary (gate, committed, elicited, registered) and run over 40 words. Sourced to the
    # printed-form keys (NUMBERS_DS.md AUX-DS-PARAGRAPH-PRINTED; NUMBERS_RESP.md AUX-RESP-PRINTED).
    ("Acting on the obligation judgment changes what a bounded view carries. The store's truthful metadata flags $82$ of the $104$ forbidding records; the other $22$ ($18$ retraction-derived, $4$ expiry-derived) are a store-side fact of the kind Table~\\ref{tab:believed} records, retrieve as active, and are out of reach of any policy that acts on the metadata. On the $104$ obligation items, the five-entry similarity view contains the forbidding record for $0.5192$; a gold-label fetch of the store's lifecycle records for the obligation's own attribute reaches $0.9519$, $0.4327$ above retrieval alone and short of the $0.50$ bar; gated on the smallest model's committed obligation score at its base rate, the fetch reaches $0.8173$, retaining $0.7561$ of that gain on the supersession-derived items (interval $[0.610, 0.872]$; $[0.562, 0.939]$ with questions grouped by user profile), short of the $60\\%$ bar under the weaker reading. The superseded-names lookup reaches $0.8173$ at the same fetch budget, within tolerance of the model. Naming the retracted and expired attributes raises the gated reach on those obligations only from $0.7805$ to $0.7805$: the gate elicited under the counting summary does not fire on them. The coverage gate at its base rate costs $0.0287$ of coverage on the items whose licensed record the store holds, within tolerance. With the forbidding record in view and tagged, the smallest model gives the stale value as the answer in $0$ of $82$ cases at the registered detector threshold ($11$ of $82$ at the join's gold threshold; $6$ of $17$ where the record printed as active) (Appendix~\\ref{app:resp}).",
     "FROZEN-REGISTERED (DS Section 7 paragraph)", "vocab gate/committed/elicited/registered; sentences over 40 words",
     "ds_downstream/NUMBERS_DS.md"),
    ("Removing the target's own name and its nearest neighbours from the superseded-names section costs the smallest model $0.3262$ of its supersession discrimination ($0.8572$ to $0.5310$; interval $[-0.3991,-0.2548]$, and $[-0.4327,-0.2167]$ with questions grouped by user profile): the obligation is read off the name, as the manuscript says.",
     "FROZEN-REGISTERED (RESP L1-P1 held reading, Section 4.2)", "sentence over 40 words",
     "resp_review/NUMBERS_RESP.md"),
    # R101 (2026-09-13): the author's ordered sentence after the frozen DS paragraph (D-DS-3 (a); the order of
    # 2026-09-13, verbatim; CLAIMS.md R101 block, R101-2). Carries "failed" as an outcome word; R79 ORDERED precedent.
    ('The two failed bars were fixed before the study measured the retrieval premise they rest on; the mechanism numbers stand and the bars are printed as set.',
     "ORDERED-R101 (the D-DS-3 (a) sentence, Section 7)", "vocab failed-as-outcome",
     "CLAIMS.md R101 block"),
    # R131 close (2026-09-20), the author's ruling B4 (ABSTRACT SWAP): the abstract is hand-tuned and its
    # last-but-one sentence restates Section 1's thesis by design ("Restating the thesis in both places is
    # intended."), so rule D's near-duplicate pair (85%) is overridden here rather than reworded.
    # R133 (2026-09-21), the author's swaps S3, S4 and S6: the thesis sentence is put verbatim in the abstract and in Section 1 and, with 'a store', in the Conclusion
    # (no gate rewords a swap; the R131 close's B4 precedent), so rule D's pairs are overridden here rather than reworded. Was the B4 entry: "In these tests, what the
    # store wrote down mattered more than which model read it." CLAIMS.md R133 block, R133-G.
    # R133 RULINGS 1 (2026-09-21): the abstract keeps S3 and Section 1 and the Conclusion take the author's sentences below, verbatim by instruction (no gate rewords a
    # swap; the R101 precedent of an ordered sentence carrying an outcome word). They carry rule V's 'held' and 'failed' in their ordinary senses, so rule V is overridden
    # here rather than reworded; the R133 thesis entry (rule D) is no longer needed and is replaced. CLAIMS.md R133 block, R133-RULINGS.
    ("In these tests, every reader we tried was held back by what the store had written down.",
     "AUTHOR-RULING R133 RULINGS 1 (Section 1's thesis sentence)", "vocab held",
     "CLAIMS.md R133 block (R133-RULINGS)"),
    ("In these tests, no reader we tried made up for what the store had failed to write down.",
     "AUTHOR-RULING R133 RULINGS 1 (the Conclusion's first sentence)", "vocab failed",
     "CLAIMS.md R133 block (R133-RULINGS)"),
    # R135 (2026-09-21): the two R134 entries for the R134 abstract's sentences ('held fixed'; the count-feature sentence) retired (gate_edits_r135.py): neither sentence is
    # in the abstract the R135 brief lands (section 3). CLAIMS.md R133 block, R135-G.
    # R139 (2026-09-23): the Conclusion's first sentence as Unit G7 words it (the author's text; 'failed' in its ordinary sense, as the R133 entry above). CLAIMS.md R133 block, R139-G7.
    ("In these monitoring tests, no reader we tried made up for what the store had failed to write down.",
     "AUTHOR-RULING R139 G7 (the Conclusion's first sentence)", "vocab failed",
     "CLAIMS.md R133 block (R139-G7)"),
]

VOCAB = [
    (r"\barms?\b", "arm/arms"), (r"\bcells?\b", "cell/cells"), (r"\blanes?\b", "lane/lanes"),
    (r"\blineages?\b", "lineage/lineages"), (r"\bestimands?\b", "estimand"),
    (r"\bendpoints?\b", "endpoint"), (r"\belicitation\b", "elicitation"),
    (r"\belicited\b", "elicited"), (r"elicitation population", "elicitation population"),
    (r"single-draw", "single-draw"), (r"\bredraws?\b", "redraw"),
    (r"\$k\s*=\s*5\$", "k = 5"), (r"tie-degenerate", "tie-degenerate"),
    (r"all-tie|all tie", "all-tie"), (r"\bcommitted\b", "committed"),
    (r"\bfrozen\b|\bfreeze\b", "frozen/freeze"), (r"\bunregistered\b", "unregistered"),
    (r"\bpreregistration\b", "preregistration"),
    (r"(?<!un)(?<!pre)\bregistered\b", "registered"),
    (r"\bregistrations?\b", "registration"), (r"\bgates?\b", "gate"),
    (r"\bverdicts?\b", "verdict"), (r"\bbranch(es)?\b", "branch"),
    (r"\bheld\b", "held (outcome)"),
    # R86 item 2.5 narrowed this. "failed" was barred because it was a registration
    # outcome CODE; that item replaced the codes with plain English, and the plain
    # English is "a failed prediction". The bare word stays barred.
    (r"\bfailed\b(?!\s+prediction)", "failed (outcome)"),
    (r"registered items?", "registered item"), (r"matched cell", "matched cell"),
    (r"matched slice|matched \$?84\$?-item set|matched replication|matched robustness slice",
     "matched slice/set"),
    (r"\bpowered\b", "powered"), (r"slot token", "slot token"),
    (r"load-bearing", "load-bearing"), (r"one-bit", "one-bit"),
    (r"read-a-zero", "read-a-zero"), (r"\bstaircase\b", "staircase"),
    # R81 Phase 4 item 9. REFRAME 5 bars these as CLAIM words in main text: the design law
    # became an observation on three measured backends. "instrument" is already listed
    # below and keeps its Section 7.1 sense, so no separate carve-out is added here.
    (r"\bdesign law\b", "design law"), (r"\blaws?\b", "law"),
    (r"\bprecondition\b", "precondition"),
    (r"count[- ]destruction", "count-destruction"), (r"non-necessity", "non-necessity"),
    (r"monitoring-scoped", "monitoring-scoped"), (r"\binstruments?\b", "instrument"),
    (r"\bledgers?\b", "ledger"), (r"micro-run", "micro-run"),
    # "as-billed" is the banned compound; plain "billed prices"/"billed arithmetic" is
    # the prompt's own ordered replacement wording (2a: billed micro-run)
    (r"as-billed", "as-billed"), (r"cap-stop", "cap-stop"),
    (r"budget stop|stopped by budget", "budget stop"), (r"byte-identical", "byte-identical"),
    (r"hash-verified", "hash-verified"), (r"value-scrubbed", "value-scrubbed"),
    (r"prior-controlled", "prior-controlled"), (r"prior-contaminated", "prior-contaminated"),
    (r"question-side", "question-side"), (r"store-side", "store-side"),
    (r"resolution analysis", "resolution analysis"), (r"\bmanifested\b", "manifested"),
    (r"\bfactorial\b", "factorial"), (r"single-channel", "single-channel"),
    (r"retention of \$?\d", "retention-as-%"),
    (r"persona-clustered|clustered (CI|interval|sensitivity)", "clustered (extended)"),
    (r"supersession-event", "supersession-event (extended)"),
    (r"slot(-| )ablat(ion|ed)", "slot ablation (extended)"),
    (r"\bE0\b", "code E0"), (r"\bE1\b(?!-)", "code E1"),
    (r"\bE1-(R|NS|XV|QP)\b", "code E1-*"), (r"\bR7\d\b", "code R7x"),
    (r"\bX[1-7]\b", "code X1-X7"), (r"\bXP-\d\b", "code XP-n"),
    (r"\bNS-\d\b", "code NS-n"), (r"\bXV-\d\b", "code XV-n"),
    (r"\bSW-\d\b", "code SW-n"), (r"\bP[1-5]\b", "code P1-P5"),
    (r"\bD8\d\b|\bD9\d\b", "code D8x/D9x"), (r"D-R74-\d+", "code D-R74-n"),
    (r"D-E1R-\d", "code D-E1R-n"), (r"\bNB-\d\b", "code NB-n"), (r"\bC6\b", "code C6"),
]

HEDGES = ["Scope:", "rather than a choice", "descriptive check", "unregistered",
          "within sampling noise", "we make no claim", "is itself a finding",
          "it is worth saying", "must not be mixed", "ships as"]

# appendix registration-code rule (NB-n deliberately excluded; see header)
APPX_CODES = (r"\b(E0|E1(?:-(?:R|NS|XV|QP))?|R7\d|X[1-7]|XP-\d|NS-\d|XV-\d|SW-\d|"
              r"P[1-5]|D8\d|D9\d|D-R74-\d+|D-E1R-\d)\b")

HERE = pathlib.Path(__file__).resolve().parent
GATE_FILE = HERE / "prose_gate_sections.txt"

SEC_LABEL = {"Introduction": "S1", "Related work": "S2", "Framework": "S3",
             "Monitoring study": "S4", "Scale and vendors": "S5",
             "Instruments, discussion, and limitations": "S7", "Conclusion": "S8"}
# Section 6's title may change wording; anything between S5 and S7 is S6.


def _strip_comments(tex):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in tex.split("\n"))


def _words(s):
    s = re.sub(r"\$[^$]*\$", " NUM ", s)
    s = re.sub(r"\\cite[pt]?\{[^}]*\}", " CITE ", s)
    s = re.sub(r"\\(ref|url|href)\{[^}]*\}", " REF ", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{)?", " ", s)
    s = re.sub(r"[{}~]", " ", s)
    return [w for w in re.split(r"\s+", s) if re.search(r"[A-Za-z0-9]", w)]


def run(tex_path):
    fails, lines_out = [], []
    raw = pathlib.Path(tex_path).read_text(encoding="utf-8").split("\n")
    stripped = [_strip_comments(l) for l in raw]

    def find_line(pred, start=0):
        for i in range(start, len(raw)):
            if pred(raw[i]):
                return i
        return None

    doc0 = find_line(lambda l: l.startswith("\\begin{document}"))
    mend = find_line(lambda l: "\\label{main-text-end}" in l)
    appx0 = find_line(lambda l: l.startswith("\\appendix"))
    abs0 = find_line(lambda l: "\\begin{abstract}" in l)
    abs1 = find_line(lambda l: "\\end{abstract}" in l)
    s1_0 = find_line(lambda l: l.startswith("\\section{Introduction}"))
    s2_0 = find_line(lambda l: l.startswith("\\section{Related work}"))

    # D-R86-10: the carve-out is gone; the abstract and Section 1 gate like the rest.
    held = set()

    # section labels per line
    secs, cur = {}, "front"
    order = []
    for i in range(doc0, mend + 1):
        m = re.match(r"\\section\{([^}]*)\}", stripped[i])
        if abs0 <= i <= abs1:
            cur = "Abs"
        elif m:
            title = m.group(1)
            cur = SEC_LABEL.get(title)
            if cur is None:
                cur = "S6" if order and order[-1] == "S5" else title
            order.append(cur)
        secs[i] = cur

    # gate scope
    if GATE_FILE.exists():
        toks = [t.strip() for t in GATE_FILE.read_text().replace("\n", ",").split(",") if t.strip()]
    else:
        toks = ["ALL"]
    gate_all = "ALL" in toks
    gate_none = "NONE" in toks
    gate_secs = set(toks) - {"ALL", "NONE", "APPX"}
    gate_appx = gate_all or ("APPX" in toks)

    def gated(sec, line_no):
        if line_no in held or gate_none:
            return False
        return gate_all or (sec in gate_secs)

    def wl_scrub(text):
        for s, _, _, _ in WHITELIST:
            text = text.replace(s, " ")
            # tolerate whitespace-flattened variants
        return text

    # flattened whitespace variants of whitelist entries, for multi-line matches
    def wl_scrub_flat(text):
        flat = re.sub(r"\s+", " ", text)
        for s, _, _, _ in WHITELIST:
            flat = flat.replace(re.sub(r"\s+", " ", s), " ")
        return flat

    # ---- V vocabulary + H hedges + P cap: line-based over main text -----------------
    # exclude \ttfamily instrument boxes (serialized index + frozen prompts): the
    # excerpts are committed instruments, not drafted prose (class INSTRUMENT-EXCERPT)
    tt_final, in_box, has_tt, buf = set(), False, False, []
    for i in range(doc0, mend + 1):
        if "\\fbox{" in stripped[i]:
            in_box, has_tt, buf = True, False, []
        if in_box:
            buf.append(i)
            if "\\ttfamily" in stripped[i]:
                has_tt = True
            if "\\end{minipage}}" in stripped[i]:
                if has_tt:
                    tt_final.update(buf)
                in_box = False

    vocab_hits, hedge_hits, prereg = [], [], []
    for i in range(doc0, mend + 1):
        if i in tt_final:
            continue
        # cap count first, on the unscrubbed line, so whitelisted sentences still count
        for _ in re.finditer(r"(?<!un)\bpreregistered\b", stripped[i]):
            prereg.append((i + 1, secs.get(i, "?")))
        line = wl_scrub(stripped[i])
        # R102 (2026-09-13, author ruling on the v10 brief, rule R9): the outcome words "held" and
        # "failed" are allowed in main text ONLY inside the R9 clause "predicted X; observed Y;
        # held|failed[ adversely]". The clause is blanked before the V check; a bare "held" or
        # "failed" outside it still fails. The VOCAB entries themselves are unchanged.
        line = re.sub(r"predicted [^;]{1,200}; observed [^;]{1,160}; (held|failed)( adversely| by construction)?\b", " ", line)
        # R126 (2026-09-20, the readable body; the author's addendum, B2): the collocation "registered with a bar" (Section 4's prediction count: "The
        # predictions were registered with a bar, each before the run that tests it") is allowed in the main text; the bare word stays barred, as does
        # "registration(s)". CLAIMS.md R126 block, entry R126-9.
        line = re.sub(r"\bregistered with a bar\b", " ", line)
        if not line.strip():
            continue
        for pat, label in VOCAB:
            for m in re.finditer(pat, line):
                # label refs are structural, not prose
                span = line[max(0, m.start() - 20):m.end() + 20]
                if re.search(r"\\(ref|label|include|input)\{[^}]*$", line[:m.start()]):
                    continue
                vocab_hits.append((i + 1, secs.get(i, "?"), label, span.strip(), gated(secs.get(i), i)))
        for h in HEDGES:
            if h in line:
                hedge_hits.append((i + 1, secs.get(i, "?"), h, gated(secs.get(i), i)))

    for ln, sec, label, ctx, g in vocab_hits:
        tag = "GATE" if g else ("HELD" if (ln - 1) in held else "report")
        lines_out.append(f"  V [{tag}] L{ln} {sec}: {label} :: ...{ctx}...")
        if g:
            fails.append(f"prose V L{ln} {sec}: vocabulary '{label}'")
    for ln, sec, h, g in hedge_hits:
        tag = "GATE" if g else ("HELD" if (ln - 1) in held else "report")
        lines_out.append(f"  H [{tag}] L{ln} {sec}: hedge phrase '{h}'")
        if g:
            fails.append(f"prose H L{ln} {sec}: hedge phrase '{h}'")
    lines_out.append(f"  P 'preregistered' count in main text: {len(prereg)} (cap 4) at "
                     + ", ".join(f"L{l}({s})" for l, s in prereg))
    if len(prereg) > 4 and not gate_none:
        fails.append(f"prose P: 'preregistered' appears {len(prereg)} times, cap 4")

    # ---- sentence extraction over main text (captions in; tikz/tabular/boxes out) ---
    body, skip = [], 0
    in_box = False
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
    joined = wl_scrub_flat(joined)
    joined = re.sub(r"\\label\{[^}]*\}", " ", joined)
    joined = re.sub(r"\\(sub)*section\*?\{[^}]*\}", " . ", joined)
    joined = re.sub(r"\\(begin|end)\{[a-zA-Z*]+\}(\[[^\]]*\])?", " ", joined)
    joined = re.sub(r"\\(label|vspace|hspace|resizebox|setlength|caption|item|centering|"
                    r"scriptsize|footnotesize|small|tiny|noindent|par|smallskip|FloatBarrier|"
                    r"protect|textsuperscript|multicolumn|toprule|midrule|bottomrule|fbox|"
                    r"ttfamily|textbf|textit|emph)\b(\[[^\]]*\])?", " ", joined)
    joined = re.sub(r"(?<![\\\w])[{}](?!\w)", " ", joined)
    # caption footnote markers: a stray * or thin-space \, after a period must not
    # glue the caption to its footnote text
    joined = joined.replace("\\,", " ")
    joined = re.sub(r"(?<![\w\\])\*(?![\w])", " ", joined)
    sents = []
    for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\\$\x00(`])", joined):
        m = re.search(r"\x00(\d+)\x00", s)
        ln = int(m.group(1)) if m else None
        sc = re.sub(r"\x00\d+\x00", " ", s).strip()
        w = _words(sc)
        if len(w) >= 4 and ln is not None:
            sents.append((ln, secs.get(ln, "?"), sc, w))

    for ln, sec, sc, w in sents:
        if len(w) > 40:
            g = gated(sec, ln)
            tag = "GATE" if g else ("HELD" if ln in held else "report")
            lines_out.append(f"  L [{tag}] L{ln + 1} {sec}: {len(w)} words :: "
                             f"{re.sub(r'  +', ' ', sc)[:90]}...")
            if g:
                fails.append(f"prose L L{ln + 1} {sec}: sentence of {len(w)} words (cap 40)")
    mean_len = sum(len(w) for _, _, _, w in sents) / max(1, len(sents))
    lines_out.append(f"  M mean sentence length: {mean_len:.1f} words over {len(sents)} "
                     f"sentences (target <= 22; report only)")

    # ---- D near-duplicates ----------------------------------------------------------
    # Content tokens only: NUM/CITE/REF placeholders and function words are excluded so
    # a number-heavy sentence cannot collide with an unrelated one through placeholders;
    # pairs need six or more content tokens on each side.
    STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "is",
            "are", "as", "its", "it", "that", "this", "we", "by", "at", "so", "not",
            "no", "from", "under", "every", "each", "num", "cite", "ref"}
    cand = []
    for ln, sec, sc, w in sents:
        content = set(x.lower() for x in w) - STOP
        if len(content) >= 6:
            cand.append((ln, sec, sc, content))
    for (l1, s1, t1, w1), (l2, s2, t2, w2) in itertools.combinations(cand, 2):
        if not w1 or not w2:
            continue
        ov = len(w1 & w2) / min(len(w1), len(w2))
        if ov > 0.70:
            g = gated(s1, l1) or gated(s2, l2)
            both_held = l1 in held and l2 in held
            tag = "HELD" if both_held else ("GATE" if g else "report")
            lines_out.append(f"  D [{tag}] {ov:.0%} L{l1 + 1} {s1} <-> L{l2 + 1} {s2}\n"
                             f"      A: {re.sub(r'  +', ' ', t1)[:100]}\n"
                             f"      B: {re.sub(r'  +', ' ', t2)[:100]}")
            if g and not both_held:
                fails.append(f"prose D: near-duplicate pair L{l1 + 1} {s1} <-> L{l2 + 1} {s2} ({ov:.0%})")

    # ---- PAR parentheticals over 10 words (report only) -----------------------------
    n_par = 0
    for ln, sec, sc, w in sents:
        for m in re.finditer(r"\(([^()]{20,})\)", sc):
            if len(_words(m.group(1))) > 10:
                n_par += 1
                lines_out.append(f"  PAR [report] L{ln + 1} {sec}: parenthetical of "
                                 f"{len(_words(m.group(1)))} words")
    lines_out.append(f"  PAR total parentheticals over 10 words: {n_par} (report only)")

    # ---- A appendix code rule -------------------------------------------------------
    if appx0 is not None:
        appx_secs, cur = {}, "?"
        for i in range(appx0, len(raw)):
            m = re.match(r"\\section\{([^}]*)\}", stripped[i])
            if m:
                lab = m.group(1)
                cur = {"Proofs": "A", "Exact capability table": "B",
                       "Cross-vendor replication record": "C", "Question-prior audit": "D",
                       "Monitoring-scoped instrument ledger": "E",
                       "Experimental and reproducibility detail": "F",
                       "Registration record": "G"}.get(lab, lab)
            appx_secs[i] = cur
        in_tab = 0
        for i in range(appx0, len(raw)):
            l = stripped[i]
            if re.search(r"\\begin\{tabular\}", l):
                in_tab += 1
            allowed_sec = appx_secs.get(i) in ("E", "G")
            if not allowed_sec and in_tab == 0:
                line = wl_scrub(l)
                for m in re.finditer(APPX_CODES, line):
                    before = line[:m.start()]
                    # pointer allowance: inside parentheses whose content refs the
                    # registration record
                    op = before.rfind("(")
                    cl = before.rfind(")")
                    in_paren = op > cl
                    paren_txt = ""
                    if in_paren:
                        end = line.find(")", m.end())
                        paren_txt = line[op:end if end != -1 else len(line)]
                    ok = in_paren and ("app:registration" in paren_txt
                                       or "tab:registrations" in paren_txt)
                    if not ok:
                        g = gate_appx
                        tag = "GATE" if g else "report"
                        lines_out.append(f"  A [{tag}] L{i + 1} App {appx_secs.get(i)}: code "
                                         f"'{m.group(0)}' :: {l.strip()[:80]}")
                        if g:
                            fails.append(f"prose A L{i + 1} App {appx_secs.get(i)}: "
                                         f"registration code '{m.group(0)}' outside E/G/cells/pointer")
            if re.search(r"\\end\{tabular\}", l):
                in_tab = max(0, in_tab - 1)

    # ---- G reader-claim gate (R110, 2026-09-14) -------------------------------------
    # No allowlist: raw stripped lines, whitelist NOT scrubbed, boxes scanned. See docstring.
    G_BANNED = [
        (r"sanity[- ]check", "sanity check"),
        (r"rather than (its|the|our|this paper's) (finding|result|contribution)", "concession 'rather than its finding'"),
        (r"definitional", "definitional"),
        (r"tautolog", "tautology"),
        (r"what (a|the) store writes about itself", "thesis 'what the store writes about itself'"),
        (r"bounds? what any reader", "bounds what any reader"),
        (r"boundary between (the )?named and counted states", "boundary is the summary's"),
        (r"lies past that check", "echo 'past that check'"),
        (r"undetectable", "undetectable"),
    ]
    G_EXPECT = r"\b(is|are|was|were|as) expected\b|\bunsurprising|\bexpected result|\bno surprise|\btrivial(ly)?\b"
    G_LOOKUP = r"\b(lookup|matcher|similarity match|cosine)\b"
    G_DIFF = r"\$[+-]|\babove\b|\bbelow\b|\bwithin\b|\bgap\b|\bdifference\b|\badds?\b|\bexceeds?\b|\bminus\b|\bmore than\b|\bless than\b"
    G_LEVEL = r"\bat \$0\.\d+\$|\$0\.\d+\$ AUROC|\bwith \$0\.\d+\$|\breaches \$0\.\d+\$|\breads [^$]{0,60}at \$0\.\d+\$"
    g_hits = []
    last = len(raw) - 1
    for i in range(doc0, last + 1):
        line = stripped[i]
        if not line.strip():
            continue
        main = i <= mend
        for pat, label in G_BANNED:
            for m in re.finditer(pat, line, flags=re.IGNORECASE):
                g_hits.append((i + 1, secs.get(i, "App") if main else "App", "G1", label, main))
        if re.search(G_LOOKUP, line, flags=re.IGNORECASE) and re.search(G_EXPECT, line, flags=re.IGNORECASE):
            g_hits.append((i + 1, secs.get(i, "App") if main else "App", "G1", "lookup called expected/unsurprising/trivial", main))
    # G2: abstract numeral sentences
    if abs0 is not None and abs1 is not None:
        abs_text = " ".join(stripped[i] for i in range(abs0, abs1 + 1))
        abs_text = re.sub(r"\\(begin|end)\{abstract\}", " ", abs_text)
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\\$(`])", abs_text):
            s = s.strip()
            # G2 is about the lookup's LEVEL: a numeral is an AUROC-type number (a math-mode decimal or count), not a percentage.
            # The author's ruling of 2026-09-15 prints the registered retention as "72%"; STYLE T2 allows numerals in two sentences.
            s_num = re.sub(r"\$\s*\d+(\.\d+)?\s*\\%\s*\$", " ", s)
            if not re.search(r"\$[^$]*\d[^$]*\$", s_num):
                continue
            # R124 block C (2026-09-19, the author's ruling on REPORT_R123 section 5): the pattern is narrowed to what the 14 September ruling
            # means, the lookup's own AUROC level in the abstract. OLD: every abstract sentence carrying a math-mode numeral had to name the
            # lookup (G_LOOKUP) and state a difference against it (G_DIFF), and no sentence could state the lookup's level (G_LEVEL).
            # NEW: only the level check stands, and only on a sentence that names the lookup; a numeral sentence that names no lookup (the
            # diagnostic study's own numbers, such as a model's AUROC loss) is not a hit.
            if re.search(G_LOOKUP, s, flags=re.IGNORECASE) and re.search(G_LEVEL, s, flags=re.IGNORECASE):
                g_hits.append((abs0 + 1, "Abs", "G2", "abstract states the lookup's own level :: " + s[:90], True))
    # G3: no labelled definition of names/counts/reads
    for i in range(doc0, mend + 1):
        if re.search(r"\\begin\{definition\}\[[^\]]*Names, counts", stripped[i]):
            g_hits.append((i + 1, secs.get(i, "?"), "G3", "labelled definition 'Names, counts, reads' (vocabulary belongs in the glossary)", True))
    # G4: Section 1 order
    s1_lines = [i for i in range(doc0, mend + 1) if secs.get(i) == "S1"]
    if s1_lines:
        # R111 (2026-09-15, the writing pass): the approved thesis sentence of Section 1 is the anchor once item 7 deletes the
        # four-finding paragraph that carried "name readers"; the regex accepts that sentence specifically (the author's ruling), not
        # any sentence containing "by its names". Phase 4c (2026-09-15, the author's cold-read ruling, item 5): the thesis sentence now reads
        # "The three models tested on the summary alone read it by its names and not by its counts"; the regex accepts "read it by its names".
        anchor = next((i for i in s1_lines if re.search(r"name[- ]readers?|reads? (the )?names|as a (list|map) of names|name list|read (a lifecycle summary|it) by its names and not by its counts|attribute names carry most of the (observed )?signal", stripped[i], flags=re.IGNORECASE)), None)
        first_tag = next((i for i in s1_lines if re.search(r"\btag(s|ged)?\b", stripped[i], flags=re.IGNORECASE)), None)
        if anchor is None:
            g_hits.append((s1_lines[0] + 1, "S1", "G4", "Section 1 carries no reader-claim anchor (read names / name readers / list of names)", True))
        elif first_tag is not None and first_tag < anchor:
            g_hits.append((first_tag + 1, "S1", "G4", f"tags (L{first_tag + 1}) precede the reader-claim anchor (L{anchor + 1}) in Section 1", True))
    for ln, sec, sub, label, main in g_hits:
        g = main and not gate_none and (gate_all or sec in gate_secs or sec == "Abs")
        tag = "GATE" if g else "report"
        lines_out.append(f"  G [{tag}] L{ln} {sec}: {sub} {label}")
        if g:
            fails.append(f"prose G L{ln} {sec}: {sub} {label}")
    lines_out.append(f"  G reader-claim hits: {len(g_hits)} (main text gated; appendix reported; no allowlist)")

    _rows, _bad = whitelist_authority()
    lines_out.append("  WHITELIST AUTHORITY (R83):")
    for st, cls, note in _rows:
        lines_out.append("    %s %-46s %s" % (st, cls, note))
    if _bad:
        fails.append("whitelist: %d entry(ies) claim a source that does not contain them: %s"
                     % (len(_bad), "; ".join(_bad)))

    scope = ("ALL" if gate_all else ("NONE" if gate_none else
             ",".join(sorted(gate_secs)) + ("+APPX" if gate_appx else "")))
    lines_out.insert(0, f"prose_scan gate scope: {scope}; held region: none (D-R86-10) "
                        f"(Phase 4 pending); whitelist entries: {len(WHITELIST)}")
    return fails, lines_out


if __name__ == "__main__":
    fails, lines = run(sys.argv[1] if len(sys.argv) > 1 else "paper_v2.tex")
    for ln in lines:
        print(ln)
    print(f"prose_scan: {'PASS' if not fails else f'{len(fails)} FAILURES'}")
    for f in fails:
        print("  ", f)
    sys.exit(1 if fails else 0)
