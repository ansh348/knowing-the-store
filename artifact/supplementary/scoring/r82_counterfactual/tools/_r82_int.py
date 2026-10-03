r"""_r82_int.py -- R82-INT: apply the R82 diffs and the 5.1/8 demotion.

By TEXT ANCHOR only; no line numbers anywhere. Idempotent.
"""
# R83: anchors re-keyed from heading TEXT to \label{}. Retitling Appendix H broke
# _r82_int's guard because it keyed on the title; a heading is an identity key for prose,
# exemption tables AND splicer anchors, and only the label survives a rename.
import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SUB = ROOT / "iclr2027_monitoring_submission"
TEX = SUB / "paper_v2.tex"
CLAIMS = SUB / "CLAIMS.md"
NL = "\r\n"

# --------------------------------------------------------------- R82 diff 1
D1_ANCHOR = ("The quantities free of this signal are the paired gains, which compare "
             "identical questions and still measure the index's added information, and the "
             "balanced $36$-question set rewritten in one voice (Appendix~\\ref{app:matched}).")
D1 = (NL + "% AUX-R82-CF-NOK, AUX-R82-CF-COUNTED, AUX-R82-CF-BASELINES" + NL +
      "On $90$ questions, each of $30$ asked of three versions of one store differing in a "
      "single attribute, a question-only reader scores $0.5000$ by construction. Naming the "
      "retracted and expired content raises the obligation judgment on those states from "
      "$0.5656$ to $0.8489$, and a match against the name lists reaches $0.7886$ against the "
      "monitor's $0.7656$ (Appendix~\\ref{app:counterfactual}).")

# --------------------------------------------------------------- R82 diff 2
D2_ANCHOR = ("The name map carries only superseded content: an entry that expires or is "
             "retracted reaches the index as a count and is never named.")
D2 = (NL + "% AUX-R82-CF-INDIVIDUATION" + NL +
      "A self-description can only name what its scrubbing rule individuates, so naming "
      "granularity bounds what any reader can recover from the summary.")

# --------------------------------------------------------------- R82 diff 3
D3 = NL.join([
    "", r"\label{app:counterfactual}\label{app:counterfactual}", "",
    "% AUX-R82-CF-PERSTATE-V2",
    r"Thirty questions, each asked of three versions of one store differing in a single attribute, reproduce the naming boundary on questions that cannot carry the label: under the summary that names only superseded content, the one named state scores $0.6550$ to $0.8275$ across the three models tested, while the two states the summary only counts score $0.5225$ to $0.6225$.",
    r"A question-only reader scores $0.5000$ on this set as an identity, because the same question is asked of all three versions.", "",
    "% AUX-R82-CF-NOK",
    r"Registered prediction, outcome \textsc{fails}. The smallest model reaches $0.5939$ under the truthful summary against that $0.5000$. The prediction required an interval excluding chance; the preregistered item-level interval is $[-0.0345,+0.2315]$ and includes it, while the question-clustered interval is $[+0.0325,+0.1625]$ and excludes it. Mixed, so the weaker reading governs: the aggregate gain does not replicate at item level on this set.", "",
    r"The registered failure text continued that the gain measured on the larger population is therefore not free of what the question alone gives away. That clause is struck as defective and does not print (D-R82-4, following D93). At this size the set can neither establish the aggregate effect nor establish contamination: the point estimate is positive, the two interval conventions disagree, and the largest model tested, on which no prediction was registered, reaches $0.7122$ under the same summary with an item-level interval that excludes chance.", "",
    "% AUX-R82-CF-COUNTED, AUX-R82-CF-BASELINES, AUX-R82-CF-OP5",
    r"Naming the counted states raises the obligation judgment on them from $0.5656$ to $0.8489$ with a paired interval of $[+0.0772,+0.4945]$, and a direct match against the three name lists reaches $0.7886$ against that model's $0.7656$. The same matcher exceeds three other rows by more than the tolerance, which is reported rather than set aside. Five of the twenty counted-state questions are excluded from that comparison and reported here instead, because their scrubbed attribute name already sits on their own state's list before the change, so the summary does not individuate them.",
])

# --------------------------------------------------------------- R82 diff 5
D5 = NL.join([
    "", r"\section{Post-hoc analyses}\label{app:posthoc}", "",
    r"Everything in this appendix is post hoc and carries no registered prediction. It is collected here so that unregistered material has one home and is never read as though it had been predicted.", "",
    r"\subsection{Calibration after the fact}\label{app:posthoc-cal}", "",
    "% AUX-R82-CAL",
    r"The elicited score is rescaled by three monotone maps under leave-one-persona-out cross-validation on the pooled hard-tier coverage set of $588$ questions, so no question contributes to the fit that predicts it. Expected calibration error on the intact-summary score falls from $0.1741$ to $0.0146$ under an isotonic map and $0.0029$ under a logistic one. That comparison needs its floor: at a base rate of $5.95\%$ a constant predictor at the base rate scores an expected calibration error of $0.0000$ and a Brier score of $0.0560$, so the calibration numbers alone understate how little is being asked. Against that floor the rescaled score improves the Brier score to $0.0519$, and it improves selective risk from $0.0615$ to $0.0373$, which is where its resolution shows.", "",
    r"The rescaled probability never exceeds $0.375$ on the intact summary or $0.450$ on the names-only summary, so the value at which it would cross one half does not exist on either. The comparison is therefore reported at each population's own base rate, where the crossings sit at $0.3$ and $0.2$ in score space. A deployed monitor thresholds at the base rate.", "",
    r"Ordering is unchanged by construction, since every map is monotone. Monotonicity is checked on each fitted map rather than on the pooled out-of-fold values, which are a mixture of forty maps and whose pooled ordering statistic therefore moves: on the question-only arm it reads $0.2572$ against a raw $0.4946$, a diagnostic of the pooling and not a property of any map (D-R82-5).",
])

# --------------------------------------------------------------- Table 21 row
T21_ANCHOR = r"A-MEM & Invent & All $23{,}403$ link references resolve to $0$ note identifiers. \\"
T21 = (T21_ANCHOR + NL + r"\addlinespace" + NL +
       "% AUX-R82-CF-CONSTRUCTION (R82; write-path census)" + NL +
       r"FR-Bank & Conflate & Of $31$ entries marked retracted across the $40$ personas, $22$ share a slot key with another entry and $16$ carry a supersedes pointer, so the write path records retraction through the supersession mechanism and the backend's own metadata cannot separate retracted from superseded content. \\")

# --------------------------------------------------------------- Appendix G rows
G_ANCHOR = r"R81: superseded-names baseline (NB-6) & \texttt{2bb7fd9dc4}"
G_ROWS = (NL + r"R82-CF: store-counterfactual cell & \texttt{3147a05} & 2026-08-29 & thirty "
          r"(persona, slot) pairs, three store versions each, two index arms, four predictions "
          r"& CF-1 FAILS (second clause struck, D-R82-4); CF-2, CF-3, CF-4 held \\" + NL +
          r"R82-CAL: post-hoc calibration & \texttt{ef351e9} & 2026-08-30 & three monotone "
          r"maps under leave-one-persona-out cross-validation on two populations & CAL-1 held; "
          r"CAL-2 undefined by base rate, its registered branch \\")

# --------------------------------------------------------------- 5.1 demotion
BLIND_OLD = NL.join([
    r"Blind NOK, by contrast, points in different directions for different models: Opus 5 sits above chance, Haiku 4.5 below, and K3 spans it.",
    r"We had predicted that every new model's blind NOK would sit at chance; that prediction missed, in opposite directions (Appendix~\ref{app:crossvendor}).",
    r"What survives is the pairing: a blind prior can point either way, while every new paired NOK gain stays positive with its interval excluding zero.",
])
BLIND_NEW = (r"Blind NOK points above, below, or across chance depending on the model, against "
             r"a prediction that it would sit at chance, and what survives is the pairing: "
             r"every paired NOK gain stays positive with its interval excluding zero "
             r"(Appendix~\ref{app:crossvendor}).")

SPAN_OLD = NL.join([
    r"% CL-SPAN (the exploratory flag is the one inline provenance flag the consolidated sentence allows)",
    r"A convergence observation (exploratory) strengthens the result: across the five models with varying blind NOK, leaving out mini, whose blind score carries no information, the blind span of $0.3307$ contracts to $0.0389$ when indexed.",
    r"The indexed scores sit between $0.8199$ and $0.8588$ across three vendors.",
])
SPAN_APPX = NL.join([
    "", "% CL-SPAN relocated from Section 5.1 by the R82-INT demotion, 2026-08-30. Exploratory,",
    "% and its strength is unchanged by the move.",
    r"A convergence observation (exploratory) strengthens the result: across the five models with varying blind NOK, leaving out mini, whose blind score carries no information, the blind span of $0.3307$ contracts to $0.0389$ when indexed.",
    r"The indexed scores sit between $0.8199$ and $0.8588$ across three vendors.",
])

MINI_OLD = (r"Mini's blind NOK gives every question the same score, so its $0.5000$ carries no "
            r"information; luna produces varied scores and still fails to discriminate.")

# --------------------------------------------------------------- Section 8
S8_OLD_START = r"Scale improves a model's blind coverage guesses; the store's own description supplies obligations that scale does not."
S8_OLD_END = r"On the three backends tested, that description helps where it carries lifecycle structure and hurts where it does not."


def main():
    s = io.open(TEX, encoding="utf-8", newline="").read()
    done, miss = [], []

    def rep(old, new, tag, count=1):
        nonlocal s
        if old in s:
            s = s.replace(old, new, count)
            done.append(tag)
        else:
            miss.append(tag)

    rep(D1_ANCHOR, D1_ANCHOR + D1, "diff1")
    rep(D2_ANCHOR, D2_ANCHOR + D2, "diff2")

    # diff 3 goes after the authorship-matched subsection, before the next subsection
    if r"\label{app:counterfactual}" not in s:
        i = s.index(r"\label{app:matched}")
        j = s.index(r"\subsection{", i + 10)
        s = s[:j] + D3.replace("\n", NL) + NL + NL + s[j:]
        done.append("diff3")
    else:
        miss.append("diff3")

    # diff 5 becomes a new Appendix H, before end{document}
    # R83: keyed on the LABEL, not the title. This guard read "section{Post-hoc analyses}"
    # until Appendix H was retitled to "Analyses done after seeing the data", at which point
    # it stopped matching and a re-run would have inserted a SECOND Appendix H. The label is
    # stable across retitles; the title is not.
    if r"\\label{app:posthoc}" not in s:
        j = s.index(r"\end{document}")
        s = s[:j] + D5.replace("\n", NL) + NL + NL + s[j:]
        done.append("diff5")
    else:
        miss.append("diff5")

    if "AUX-R82-CF-CONSTRUCTION" not in s:
        rep(T21_ANCHOR, T21, "table21-conflate")
    else:
        miss.append("table21-conflate")
    rep(G_ANCHOR, G_ANCHOR, "appendixG-anchor-check")
    if "R82-CF: store-counterfactual cell" not in s:
        k = s.index(G_ANCHOR)
        eol = s.index(r"\\", k) + 2
        s = s[:eol] + G_ROWS + s[eol:]
        done.append("appendixG-rows")

    rep(BLIND_OLD, BLIND_NEW, "5.1-blind-one-sentence")
    if SPAN_OLD in s:
        s = s.replace(SPAN_OLD + NL, "", 1)
        a = s.index(r"\label{app:laddertable}")
        b = s.index(r"\begin{table}", a)
        s = s[:b] + SPAN_APPX.replace("\n", NL) + NL + NL + s[b:]
        done.append("5.1-span-to-appendixB")
    else:
        miss.append("5.1-span-to-appendixB")
    rep(MINI_OLD + NL, "", "5.1-mini-tie-cut")

    rep("That matcher reaches the smallest model tested.",
        "That matcher matches the smallest model tested.", "reaches->matches")

    # section 8 to the four moves
    if S8_OLD_START in s and "A bounded retrieved view cannot settle" not in s:
        a = s.index(S8_OLD_START)
        b = s.index(S8_OLD_END) + len(S8_OLD_END)
        s = s[:a] + NL.join([
            r"A bounded retrieved view cannot settle whether a store holds content that must not be used, because the record that forbids use can sit outside it, so the judgment has to come from what the store says about itself.",
            r"FOK measures intent-conditional coverage, and NOK names and measures a previously unformalized obligation judgment.",
            r"With a truthful summary the paired obligation gain is positive on every model tested, and a direct match against the names the store marks superseded matches the smallest of them.",
            r"No backend we tested supplies such a summary, and under the metadata real backends expose, coverage judgment survives while obligation judgment keeps part of its gain.",
            r"On the two backends whose self-descriptions carry no lifecycle structure the same summary hurts at every tested scale.",
            r"Scale improves a model's blind coverage guesses; the store's own description supplies obligations that scale does not.",
        ]) + s[b:]
        done.append("section8-four-moves")
    else:
        miss.append("section8-four-moves")

    # U-block integrity before writing
    for tag, blk in (("U7", "so bounds correspondence alone"),
                     ("U3", "rendered feature causes the inversion"),
                     ("U2", "Scope: the negative index effect")):
        if re.sub(r"\s+", " ", s).count(blk) != 1:
            sys.exit(f"STOP: {tag} no longer appears exactly once")

    io.open(TEX, "w", encoding="utf-8", newline="").write(s)
    print("applied:", ", ".join(done))
    if miss:
        print("not applied (already present or anchor drifted):", ", ".join(miss))
    return 0


if __name__ == "__main__":
    sys.exit(main())
