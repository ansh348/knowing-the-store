# -*- coding: utf-8 -*-
"""wp_phase2.py -- Phase 2 of the writing pass on paper_v18 (paper_v18_writing_prompt.md section 16: renames and search-and-replace; items
34, 35, 61 with its addendum, 80, 83; item 36 was done in Phase 1), 2026-09-15, applied to reviews/v18/src/body_v18.tex and
reviews/v18/src/appendix_v18.tex after Phase 1 (commit 2f5ea33).

Rules of the script. (1) A frozen registered text is never touched: a line that carries one of slogan_scan's EXEMPT_FROZEN_REGISTERED
strings, or that follows a comment saying "ships verbatim" (R78-2c: frozen registered wording ships verbatim; style yields). (2) Only the
non-comment part of a line is edited, so the ledger keys in source comments (AUX-E1R-BELIEVED-NOK and the like) keep their names. (3) Every
replacement asserts its count, so a phrase that has moved or vanished stops the script instead of drifting. (4) The carried paper_v11 blocks
are repaired by build_v18.py's REPAIRS_R111 list (this script writes nothing there); see that file. (5) No number changes.
Usage: python reviews/v18/tools/wp_phase2.py [--check]
"""
from __future__ import annotations

import ast
import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
SRC = ROOT / "reviews" / "v18" / "src"
BODY = SRC / "body_v18.tex"
APPX = SRC / "appendix_v18.tex"


sys.path.insert(0, str(SUB / "tools"))
import frozen_diff as FD  # noqa: E402  (the gate's own normalization and registration fragments; no gate logic duplicated)


def frozen_fragments():
    """Every string frozen_diff protects as registered wording: slogan_scan's EXEMPT_FROZEN_REGISTERED strings and the quoted (>)
    paragraphs of ARTIFACT/registrations/*.md, split into sentences and placeholder-free fragments of MIN_LEN or more, normalized."""
    out = []
    src = (SUB / "tools" / "slogan_scan.py").read_text(encoding="utf-8")
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "EXEMPT_FROZEN_REGISTERED" for t in node.targets):
            out += [FD.norm(ast.literal_eval(e)) for e in node.value.elts]
    # the registration files through frozen_diff's own parser (registration_fragments(), the R111 fix: every run of ">"-prefixed
    # lines is a quoted block, whatever precedes it)
    for _, frag in FD.registration_fragments():
        out.append(FD.norm(frag))
    return [f for f in out if len(f) >= 8]


FRAGMENTS = frozen_fragments()
# registered texts the appendix quotes whose "ships verbatim" comment sits more than one prose line above them
EXTRA_FROZEN = ["Two filters on the metadata FR-Bank exposes ---"]
CHECK = "--check" in sys.argv
MISMATCH = []


def is_frozen(lines, i):
    """A line is frozen when it carries a registered fragment (normalized as frozen_diff normalizes), or follows a comment block that
    says 'ships verbatim' (the appendix marks its quoted registered texts that way; the block may run over several comment lines)."""
    ln = FD.norm(lines[i])
    if any(f in ln for f in FRAGMENTS) or any(h in lines[i] for h in EXTRA_FROZEN):
        return True
    if lines[i].lstrip().startswith("\\paragraph"):
        return False                                   # a paragraph title is never registered text
    j = i - 1
    while j >= 0 and lines[j].lstrip().startswith("%"):
        if "ships verbatim" in lines[j]:
            return True
        j -= 1
    return False


def split_comment(ln):
    m = re.search(r"(?<!\\)%", ln)
    return (ln, "") if m is None else (ln[:m.start()], ln[m.start():])


class Doc:
    """A source file as editable segments: the non-comment part of every non-frozen line."""

    def __init__(self, path):
        self.path = path
        self.lines = io.open(path, encoding="utf-8").read().replace("\r\n", "\n").split("\n")
        self.editable = [not is_frozen(self.lines, i) for i in range(len(self.lines))]
        self.log = []

    def text_parts(self):
        return [(i, *split_comment(l)) for i, l in enumerate(self.lines) if self.editable[i]]

    def count(self, old, regex=False):
        n = 0
        for _, t, _ in self.text_parts():
            n += len(re.findall(old, t)) if regex else t.count(old)
        return n

    def replace(self, old, new, expect, regex=False, note=""):
        n = self.count(old, regex)
        if n != expect and CHECK:
            MISMATCH.append((self.path.name, old[:90], n, expect))
        assert n == expect or CHECK, (self.path.name, old[:70], "count", n, "expected", expect)
        for i, t, c in self.text_parts():
            t2 = re.sub(old, new, t) if regex else t.replace(old, new)
            if t2 != t:
                self.lines[i] = t2 + c
        self.log.append((old[:60], new[:60], n, note))
        return n

    def delete_line(self, sentence):
        """Delete the one editable line whose text is exactly this sentence (a paragraph break is not created)."""
        hits = [i for i, t, c in self.text_parts() if t.strip() == sentence]
        assert len(hits) == 1 or CHECK, (self.path.name, sentence[:60], len(hits))
        if len(hits) != 1:
            MISMATCH.append((self.path.name, sentence[:90], len(hits), 1)); return
        del self.lines[hits[0]]; del self.editable[hits[0]]
        self.log.append((sentence[:60], "(deleted)", 1, ""))

    def write(self):
        io.open(self.path, "w", encoding="utf-8", newline="\n").write("\n".join(self.lines))


def body_edits(B: Doc):
    # item 61: the smallest model -> GPT-4.1 mini; the larger model -> Haiku 4.5 where it is Haiku 4.5, the three larger models named
    B.replace("the smallest model's", "GPT-4.1 mini's", 1)
    B.replace("The smallest model", "GPT-4.1 mini", 1)
    B.replace("the smallest model", "GPT-4.1 mini", 6)
    B.replace("the three larger models sit", "Haiku 4.5, Opus 5 and GPT-5.6 Luna sit", 1)
    B.replace("costs the larger model about a quarter of its gain", "costs Haiku 4.5 about a quarter of its gain", 1)
    B.replace("The one lifecycle store's own metadata is enough for the larger model wherever it still writes the name, and not enough for GPT-4.1 mini or the lookup anywhere.",
              "FR-Bank's own metadata is enough for Haiku 4.5 wherever it still writes the name, and not enough for GPT-4.1 mini or the name lookup anywhere.", 1)
    # item 34: truthful / believed -> ground-truth summary / store-written summary
    B.replace("A truthful summary is built from ground truth and a believed summary from the fields the backend itself exposes",
              "A ground-truth summary is built from ground truth and a store-written summary from the fields the backend itself exposes", 1)
    B.replace("never binds on the truthful summary", "never binds on the ground-truth summary", 1)
    B.replace("tab:believed", "tab:census", 2)
    B.replace("app:believed-census", "app:census", 4)
    # item 35: the join / the marks -> ground-truth tags / the store's own tags (section 15's example for the paragraph opener)
    B.replace("Under the store's own marks the same view reads more, and the rise is the marks' reach of the forbidding records rather than their density.",
              "With the store's own tags instead of ground-truth tags, the same view scores higher. The reason is that the store's tags reach more of the forbidding records, not that there are more tags.", 1)
    B.replace("With FR-Bank's own marks in place of the join, the view reads the obligation at $0.81$ against $0.69$ for GPT-4.1 mini",
              "With FR-Bank's own tags in place of the ground-truth tags, the view reads the obligation at $0.81$ against $0.69$ for GPT-4.1 mini", 1)
    B.replace("The marks tag $1{,}389$ of the $3{,}305$ lines shown as non-active where the join tags $217$, and $1{,}273$ lines carry a different tag under the marks than under the join.",
              "The store's own tags mark $1{,}389$ of the $3{,}305$ lines shown as non-active where the ground-truth tags mark $217$, and $1{,}273$ lines carry a different tag under the store's own tags than under the ground-truth tags.", 1)
    B.replace("against the monitor's $0.81$ under the marks, and the tagged-name lookup", "against the monitor's $0.81$ under the store's own tags, and the tagged-name lookup", 1)
    B.replace("the marks tag $70$ non-active against the join's $60$", "the store's own tags mark $70$ non-active against the ground-truth tags' $60$", 1)
    B.replace("reads $0.72$ under the marks against $0.67$ under the join", "reads $0.72$ under the store's own tags against $0.67$ under the ground-truth tags", 1)
    B.replace("under the one store's own marks the tagged view kept its reading", "under FR-Bank's own tags the tagged view kept its reading", 1)
    # item 61 addendum: tally / tallies -> count / counts (section 15's examples where it gives them)
    B.replace("and counts it when it gives only a tally of it", "and counts it when it gives only a count of it", 1)
    B.replace("so the tally is the only thing that carries the label", "so the count is the only thing that carries the label", 1)
    B.replace("no model follows the tallies, and a reader that knows the question's category separates the states the summary only counts where no model does",
              "no model follows the counts, and a reader that knows the question's category separates the counted states where no model does", 1)
    B.replace("reads that category's retracted and expired tallies", "reads that category's retracted and expired counts", 1)
    B.replace("No model follows the tallies:", "No model follows the counts:", 1)
    B.replace("sends a reader of that tally to", "sends a reader of that count to", 1)
    B.replace("The tally individuates the version here because $26$ of the $30$ retraction pairs and $15$ of the $30$ expiry pairs have no other retracted or expired entry in the category.",
              "The count identifies the right version here because the category usually has no other retracted or expired entry ($26$ of $30$ retraction pairs, $15$ of $30$ expiry pairs), so the count goes from zero to one.", 1)
    B.delete_line("The store version that carries the obligation therefore reads its increment against zero.")
    B.replace("What a tally cannot carry is which attribute is in the state, and naming those attributes lifts the models.",
              "A count cannot say which attribute is retracted or expired.\nWhen the summary names those attributes, every model improves (Table~\\ref{tab:cf-main}).", 1)
    # item 61 addendum: the Conclusion's sentence (section 15's example); the ruler -> the baseline
    B.replace("The name that individuates the obligation carries the judgment, the tallies carry none of it for any model, and the lookup that reads the names is the level two of the three models measure identical to.",
              "The name of the stale attribute supplies the judgment.\nThe counts supply none of it, for any model.\nA lookup over the names is a baseline two of the three models do not exceed.", 1)
    B.replace("the lookup is the ruler, and every difference carries two intervals", "the name lookup is the baseline, and every difference carries two intervals", 1)
    # item 61: user profile -> persona; profile interval -> persona interval
    B.replace("the interval grouped by user profile is the sensitivity", "the interval grouped by persona is the sensitivity", 1)
    B.replace("profile interval", "persona interval", 3)
    B.replace("profile-grouped", "persona-grouped", 2)
    # item 61: the name lookup on first use in each section (Sections 4, 5, 7, 8); the definition sentence of Section 4
    B.replace("The similarity lookup scores each question by its maximum cosine similarity", "The name lookup scores each question by its maximum cosine similarity", 1)
    B.replace("It has no model in it and is the level every model is measured against", "It has no model in it and is the baseline every model is measured against", 1)
    B.replace("keeps its margin over the lookup on the counterfactual set", "keeps its margin over the name lookup on the counterfactual set", 1)
    B.replace("do not exceed the lookup and Opus 5 exceeds it by", "do not exceed the name lookup and Opus 5 exceeds it by", 1)
    B.replace("FR-Bank's own metadata leaves GPT-4.1 mini and the lookup close to chance", "FR-Bank's own metadata leaves GPT-4.1 mini and the name lookup close to chance", 1)
    B.replace("On the full obligation set the lookup scores $0.75$ against GPT-4.1 mini's $0.73$, inside tolerance, and Haiku 4.5, Opus 5 and GPT-5.6 Luna sit $+0.07$ to $+0.08$ above it with item-level intervals excluding zero and persona-grouped intervals including it",
              "On the full obligation set the name lookup scores $0.75$ against GPT-4.1 mini's $0.73$, inside tolerance.\nHaiku 4.5, Opus 5 and GPT-5.6 Luna sit $+0.07$ to $+0.08$ above it, with item-level intervals excluding zero and persona-grouped intervals including it", 1)
    B.replace("the superseded-names lookup scores coverage there", "the name lookup scores coverage there", 1)
    B.replace("One is the similarity lookup over the superseded-names list; the other is a count reader", "One is the name lookup, a similarity lookup over the superseded-names list; the other is a count reader", 1)
    # item 61: FR-Bank, not the lifecycle store (the author's item 83 sentence in Limitations keeps "one lifecycle store, FR-Bank")
    assert B.count("lifecycle store") == 1


def appendix_edits(A: Doc):
    # item 61: the smallest model -> GPT-4.1 mini; the three larger models named
    A.replace("the smallest model's single call", "GPT-4.1 mini's single call", 1)
    A.replace("The smallest model is absent from that table", "GPT-4.1 mini is absent from that table", 1)
    A.replace("the smallest model", "GPT-4.1 mini", 5)
    A.replace("the three larger models lead by", "Haiku 4.5, Opus 5 and GPT-5.6 Luna lead by", 1)
    # item 34: truthful -> ground-truth; the word believed -> store-written; the macros expanded outside the frozen texts
    A.replace("truthful-summary rows", "ground-truth-summary rows", 1)
    A.replace("truthful-list score", "ground-truth-list score", 1)
    A.replace("against $0.8855$ truthful", "against $0.8855$ under the ground-truth summary", 1)
    A.replace("Haiku, \\believed{} & truthful & lookup & \\believed{} minus truthful", "Haiku, store-written & ground-truth & lookup & store-written minus ground-truth", 1)
    A.replace("truthful", "ground-truth", 13)
    A.replace("Believed-state census", "Census of the store-written state", 1)
    A.replace("app:believed-census", "app:census", 1)
    A.replace("tab:believed", "tab:census", 1)
    A.replace("records the believed superseded list", "records the store-written superseded list", 1)
    A.replace("The believed superseded list, and the renderer's cap.", "The store-written superseded list, and the renderer's cap.", 1)
    A.replace("believed-state cap (S2)", "store-written-state cap (S2)", 1)
    A.replace("Under \\trueidx{} it reaches", "Under the ground-truth summary it reaches", 1)
    A.replace("Under \\believed{} it reaches", "Under the store-written summary it reaches", 1)
    A.replace("$1.75$ under \\trueidx{}.", "$1.75$ under the ground-truth summary.", 1)
    A.replace("The whole-population difference under \\trueidx{}", "The whole-population difference under the ground-truth summary", 1)
    A.replace("\\trueidx{}", "ground-truth", 4)
    A.replace("\\believed{}", "store-written", 14)
    # item 35: the join / the marks
    A.replace("with FR-Bank's own lifecycle marks in place of the ground-truth join", "with FR-Bank's own lifecycle tags in place of the ground-truth join", 1)
    A.replace("The marks change the tag on $1,273$ of the $3,305$ lines shown, and against the join's non-active flag the store's mark has precision",
              "The store's own tags change the tag on $1,273$ of the $3,305$ lines shown, and against the ground-truth non-active flag the store's tag has precision", 1)
    A.replace("under the join's tags", "under ground-truth tags", 1)
    A.replace("The tagged view under the store's own marks,", "The tagged view under the store's own tags,", 1)
    A.replace("that the join tied to no lifecycle event", "that the ground-truth join tied to no lifecycle event", 1)
    A.replace("Negation: the join assigns the retracted state", "Negation: the ground-truth join assigns the retracted state", 1)
    A.replace("because the join reads no negation", "because the ground-truth join reads no negation", 1)
    A.replace("the join's gold threshold", "the ground-truth join's threshold", 1)
    A.replace("at the join's threshold", "at the ground-truth join's threshold", 1)
    A.replace("(the join's threshold)", "(the ground-truth join's threshold)", 1)
    # item 61 addendum: tally / tallies -> count / counts; individuates -> identifies; the moved-count control
    A.replace("so that what a tally carries can be measured", "so that what a count carries can be measured", 1)
    A.replace("retracted-plus-expired tally", "retracted-plus-expired count", 2)
    A.replace("The tally individuates the version because", "The count identifies the version because", 1)
    A.replace("A second tally check", "A second count check", 1)
    A.replace("the direction a tally reader falls", "the direction a count reader falls", 1)
    A.replace("and reads the same tally;", "and reads the same count;", 1)
    A.replace("the per-category tallies are not touched", "the per-category counts are not touched", 1)
    A.replace("so no model followed the tally", "so no model followed the count", 1)
    A.replace("the per-category tallies are untouched by that permutation", "the per-category counts are untouched by that permutation", 1)
    A.replace("the category-guessing reader the tally at the category", "the category-guessing reader the count at the category", 1)
    A.replace("gives only a tally of it", "gives only a count of it", 1)
    print("tally / tallies left in the appendix outside the frozen texts:", A.count(r"\btall(y|ies)\b", regex=True))
    A.replace("the states the summary only counts", "the counted states", 1)
    A.replace("The increment moved within the triple", "The moved-count control", 3)
    A.replace("increment moved &", "moved-count control &", 1)
    # item 61: user profile -> persona
    A.replace("grouped by user profile", "grouped by persona", 10)
    A.replace("by user profile \\\\", "by persona \\\\", 1)
    A.replace("profile interval", "persona interval", 13)
    A.replace("profile-grouped", "persona-grouped", 3)
    # item 61: the name lookup (first use per subsection), the superseded-names lookup renamed, the matcher never
    A.replace("compares the indexed level with the lookup instead", "compares the indexed level with the name lookup instead", 1)
    A.replace("the per-state split of the lookup against the models, and the lookup on the coverage tiers", "the per-state split of the name lookup against the models, and the lookup on the coverage tiers", 1)
    A.replace("and $+0.0776$ ($[+0.0272,+0.1355]$; $[-0.0031,+0.1498]$) above the lookup", "and $+0.0776$ ($[+0.0272,+0.1355]$; $[-0.0031,+0.1498]$) above the name lookup", 1)
    A.replace("whether the lookup's score rides on questions", "whether the name lookup's score rides on questions", 1)
    A.replace("superseded-names lookup", "name lookup", 12)
    A.replace("Superseded-names lookup", "Name lookup", 8)
    A.replace("The superseded-section lookup, lexical and embedding,", "The name lookup, lexical and embedding,", 1)
    A.replace("at the lifecycle store's measured rate", "at FR-Bank's measured rate", 2)
    A.replace("the lifecycle store's", "FR-Bank's", 2)
    # item 80: the author -> we (C.2, F, G.2); items 73's "the author read" too
    A.replace("failed the author's read", "failed our read", 1)
    A.replace("the author's label-transfer read had not been made at this build", "our label-transfer read had not been made at this build", 1)
    A.replace("that the author's read had passed", "that our read had passed", 1)
    A.replace("passes the author's read", "passes our read", 1)
    A.replace("The author read every question of the counterfactual set", "We read every question of the counterfactual set", 1)
    # the author's ruling on the Phase 2 report (2026-09-15): registered texts render verbatim; E.1 maps the artifact's names to the paper's
    # terms, and Appendix F says so in one sentence (item 74's lead-in will repeat it when that lands)
    A.replace("\\noindent A summary \\emph{names} a state when it lists the attribute names in that state and \\emph{counts} it when it gives only a count of it; a reader \\emph{reads} a state when its score separates that state's items from the rest.",
              "\\noindent A summary \\emph{names} a state when it lists the attribute names in that state and \\emph{counts} it when it gives only a count of it; a reader \\emph{reads} a state when its score separates that state's items from the rest.\n\n%% R111 Phase 2 (the author's ruling of 2026-09-15): the registered texts quoted in the appendices use the artifact's names, byte for byte; this map carries them to the paper's terms.\n\\paragraph{The artifact's names in the registered texts.}\nThe registered texts quoted in Appendices~\\ref{app:counterfactual}, \\ref{app:baselines}, \\ref{app:census}, \\ref{app:resp} and~\\ref{app:registration} are reproduced byte for byte, so they keep the artifact's names.\nSix of those names differ from this paper's terms.\n\\begin{center}\n\\scriptsize\n\\begin{tabular}{@{}ll@{}}\n\\toprule\nIn the registered texts & In this paper \\\\\n\\midrule\n\\textsc{true} (the truthful summary) & the ground-truth summary \\\\\n\\textsc{believed} (the believed summary) & the store-written summary \\\\\nthe join & ground-truth tags \\\\\nthe matcher & the name lookup \\\\\nthe smallest model & GPT-4.1 mini \\\\\nuser profile & persona \\\\\n\\bottomrule\n\\end{tabular}\n\\end{center}", 1)
    A.replace("This appendix is the registration record: each frozen artifact, its commit, freeze date, scope and outcome.",
              "This appendix is the registration record: each frozen artifact, its commit, freeze date, scope and outcome.\nRegistered texts are quoted verbatim and use the artifact's names; Appendix~\\ref{app:glossary} maps them to this paper's terms.", 1)
    A.replace("which waits on the author's read", "which waits on our read", 1)
    A.replace("screened and read by the author", "screened and read by us", 1)
    A.replace("Grouped by user profile that interval", "Grouped by persona that interval", 1)
    A.replace("The three larger models lead the embedding lookup", "Haiku 4.5, Opus 5 and GPT-5.6 Luna lead the embedding lookup", 1)
    A.replace("the believed summary with its fifteen-name cap lifted", "the store-written summary with its fifteen-name cap lifted", 1)


def main():
    check = "--check" in sys.argv
    B, A = Doc(BODY), Doc(APPX)
    print(f"frozen lines skipped: body {sum(not e for e in B.editable)}, appendix {sum(not e for e in A.editable)}")
    body_edits(B); appendix_edits(A)
    for d in (B, A):
        print(f"{d.path.name}: {len(d.log)} replacements, {sum(n for _, _, n, _ in d.log)} substitutions")
    if check:
        for m in MISMATCH:
            print(f"  MISMATCH {m[0]}: {m[1]!r} count {m[2]} expected {m[3]}")
        print(f"(check only, nothing written; {len(MISMATCH)} mismatches)"); return
    B.write(); A.write()


if __name__ == "__main__":
    main()
