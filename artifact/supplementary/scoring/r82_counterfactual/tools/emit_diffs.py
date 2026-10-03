"""emit_diffs.py -- R82: write the five main-text and appendix diffs.

Each diff is anchored by SURROUNDING TEXT rather than by line number, because R81 Phases 3
to 5 will still move paper_v2.tex before these land. A line-anchored diff would rot; an
anchor-anchored one splices cleanly wherever the paragraph ends up.

Every diff carries: its anchor, the exact text, its ledger key, its estimated review-line
cost, and its S8/S10 clearance. Nothing here is applied. R82-INT applies them only after a
commit titled R81-5 exists.
"""
import io
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "diffs"

D = {}

# --------------------------------------------------------------------------- 1
D["01_cf_main.md"] = r"""# Diff 1 — main text, the counterfactual result

**Site.** Section 4.3, after the paragraph ending "...and only expired logistics carries both
at usable size." Alternatively Section 7.1 beside the leakage discussion; Section 4.3 is
preferred because the result is a measurement rather than a limitation.

**Anchor (insert AFTER this sentence, which is present in paper_v2.tex today):**

> The quantities free of this signal are the paired gains, which compare identical questions
> and still measure the index's added information, and the balanced $36$-question set
> rewritten in one voice (Appendix~\ref{app:matched}).

**Insert:**

```latex
% AUX-R82-CF-NOK, AUX-R82-CF-COUNTED, AUX-R82-CF-BASELINES
On $90$ questions, each of $30$ asked of three versions of one store differing in a single
attribute, a question-only reader scores $0.5000$ by construction. Naming the retracted and
expired content raises the obligation judgment on those states from $0.5656$ to $0.8489$, and
a match against the name lists reaches $0.7886$ against the monitor's $0.7656$
(Appendix~\ref{app:counterfactual}).
```

**Ledger keys.** `AUX-R82-CF-NOK`, `AUX-R82-CF-COUNTED`, `AUX-R82-CF-BASELINES`.

**Estimated cost: 3 review lines.** LANDS. Yield source to be named at integration.

**S8** no em dash. **S9** no barred contrastive. **S10** no internal program vocabulary: no
"arm", "cell", "lane", "registered", "gate", or code name. "summary" is used for the index,
per the S10 preference.
"""

# --------------------------------------------------------------------------- 2
D["02_scrubber_main.md"] = r"""# Diff 2 — main text, Section 7.2, naming granularity

**Site.** Section 7.2, beside the existing limitation about what the index carries.

**Anchor (insert AFTER the sentence naming what the index counts rather than names).**

**Insert:**

```latex
% AUX-R82-CF-INDIVIDUATION
A self-description can only name what its scrubbing rule individuates, so naming granularity
bounds what any reader can recover from the summary.
```

**Ledger key.** `AUX-R82-CF-INDIVIDUATION`.

**Estimated cost: 2 review lines.** LANDS.

**S9 note.** The sentence as dictated read "naming granularity is a design parameter of the
index, not a property of the model", which is the barred `, not ` form. The content is
unchanged and the construction is dropped. Recorded in `ADDENDUM_R82` §16.
"""

# --------------------------------------------------------------------------- 3
D["03_cf_appendix_d2.md"] = r"""# Diff 3 — Appendix D.2, the counterfactual cell

**Site.** New subsection immediately after `\subsection{Authorship-matched cell}`
(`\label{app:matched}`), so the two construction-control cells sit together.

**Insert:**

```latex
\subsection{Store-counterfactual cell}\label{app:counterfactual}

% AUX-R82-CF-PERSTATE-V2 -- the result, stated first
Thirty questions, each asked of three versions of one store differing in a single attribute,
reproduce the naming boundary on questions that cannot carry the label: under the summary that
names only superseded content, the one named state scores $0.6550$ to $0.8275$ across the
three models tested, while the two states the summary only counts score $0.5225$ to $0.6225$.
A question-only reader scores $0.5000$ on this set as an identity, because the same question is
asked of all three versions.

% AUX-R82-CF-NOK
Registered prediction, outcome \textsc{fails}. The smallest model reaches $0.5939$ under the
truthful summary against that $0.5000$. The prediction required an interval excluding chance;
the preregistered item-level interval is $[-0.0345,+0.2315]$ and includes it, while the
question-clustered interval is $[+0.0325,+0.1625]$ and excludes it. Mixed, so the weaker
reading governs: the aggregate gain does not replicate at item level on this set.

The registered failure text continued that the gain measured on the larger population is
therefore not free of what the question alone gives away. That clause is struck as defective
and does not print (D-R82-4, following D93). At this size the set can neither establish the
aggregate effect nor establish contamination: the point estimate is positive, the two interval
conventions disagree, and the largest model tested, on which no prediction was registered,
reaches $0.7122$ under the same summary with an item-level interval that excludes chance.

% AUX-R82-CF-COUNTED, AUX-R82-CF-BASELINES, AUX-R82-CF-OP5
Naming the counted states raises the obligation judgment on them from $0.5656$ to $0.8489$
with a paired interval of $[+0.0772,+0.4945]$, and a direct match against the three name lists
reaches $0.7886$ against that model's $0.7656$. The same matcher exceeds three other rows by
more than the tolerance, which is reported rather than set aside. Five of the twenty
counted-state questions are excluded from that comparison and reported here instead, because
their scrubbed attribute name already sits on their own state's list before the change, so the
summary does not individuate them.
```

Table to accompany: blind $0.5000$ by identity, v2 and v3 for all three models, per-state
rows, all three matchers, the adverse rows, and the five collision pairs.

**Ledger keys.** `AUX-R82-CF-NOK`, `-COUNTED`, `-BASELINES`, `-OP5`, `-PERSTATE-V2`,
`-INDIVIDUATION`.

**Cost: 0 review lines.** Appendix material is uncounted against the page gate.
"""

# --------------------------------------------------------------------------- 4
D["04_cal_main.md"] = r"""# Diff 4 — main text, Section 4.3, calibration

**Site.** Section 4.3, appended to the existing calibration paragraph, after the sentence
ending "...so a deployed monitor must threshold it per index
(Figure~\ref{fig:reliability})."

**Insert:**

```latex
% AUX-R82-CAL
Rescaling the score after the fact does make it calibrated, and the calibrated value still
never exceeds $0.375$, so a deployed threshold sits at the base rate rather than at one half
(Appendix~\ref{app:posthoc}).
```

**Ledger key.** `AUX-R82-CAL`.

**Estimated cost: 2 review lines. HELD, cut first under the standing cut order.** The
result lands in Appendix H, which is uncounted.

**Why this sentence rather than the CAL-1 fact alone.** CAL-1 holds, isotonic bringing the
intact-index error to $0.0146$, and on its own that overclaims: at a $5.95\%$ base rate a
constant predictor at the base rate already scores an expected calibration error of $0.0000$,
so most of the apparent gain is the base rate. What recalibration actually buys is resolution,
worth $0.0036$ of Brier score against that floor. The operator-relevant fact is the ceiling on
the calibrated value, which is what this sentence carries.

**S9** no barred contrastive. **S10** no program vocabulary.
"""

# --------------------------------------------------------------------------- 5
D["05_cal_appendix_h.md"] = r"""# Diff 5 — Appendix H, the standing post-hoc section

**Site.** New appendix section after `\section{Registration record}` (`\label{app:registration}`),
immediately before `\end{document}`.

**Insert:**

```latex
\section{Post-hoc analyses}\label{app:posthoc}

Everything in this appendix is post hoc and carries no registered prediction. It is collected
here so that unregistered material has one home and is never read as though it had been
predicted.

\subsection{Calibration after the fact}\label{app:posthoc-cal}

% AUX-R82-CAL
The elicited score is rescaled by three monotone maps under leave-one-persona-out
cross-validation on the pooled hard-tier coverage set of $588$ questions, so no question
contributes to the fit that predicts it. Expected calibration error on the intact-summary
score falls from $0.1741$ to $0.0146$ under an isotonic map and $0.0029$ under a logistic one.
That comparison needs its floor: at a base rate of $5.95\%$ a constant predictor at the base
rate scores an expected calibration error of $0.0000$ and a Brier score of $0.0560$, so the
calibration numbers alone understate how little is being asked. Against that floor the
rescaled score improves the Brier score to $0.0519$, and it improves selective risk from
$0.0615$ to $0.0373$, which is where its resolution shows.

The rescaled probability never exceeds $0.375$ on the intact summary or $0.450$ on the
names-only summary, so the value at which it would cross one half does not exist on either.
The comparison is therefore reported at each population's own base rate, where the crossings
sit at $0.3$ and $0.2$ in score space. A deployed monitor thresholds at the base rate.

Ordering is unchanged by construction, since every map is monotone. Monotonicity is checked on
each fitted map rather than on the pooled out-of-fold values, which are a mixture of forty maps
and whose pooled ordering statistic therefore moves: on the question-only arm it reads $0.2572$
against a raw $0.4946$, a diagnostic of the pooling and not a property of any map (D-R82-5).
```

Table to accompany: per arm and per map, expected calibration error, Brier, area under the
risk-coverage curve, excess area, and the constant-predictor floor as its own row.

**Ledger key.** `AUX-R82-CAL`.

**Cost: 0 review lines.**
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tot = 0
    for name, body in sorted(D.items()):
        p = OUT / name
        io.open(p, "w", encoding="utf-8", newline="\n").write(body)
        cost = 0
        for ln in body.split("\n"):
            if ln.startswith("**Estimated cost:") or ln.startswith("**Cost:"):
                cost = int("".join(c for c in ln.split(":")[1] if c.isdigit()) or 0)
        tot += cost
        print(f"{name:26s} {cost} review lines")
    print(f"\nR82 main-text total: {tot} review lines "
          f"(plus 2 for related work) against a budget of 5")


if __name__ == "__main__":
    main()
