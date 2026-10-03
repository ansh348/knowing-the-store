"""
probe_verdicts.py -- verdicts for the 3 natural-absent probes whose sweep returned a
>=2-term co-occurrence hit. The other 142 returned zero hits on every content term and
are verified absent by their transcripts.

Criterion: a probe FAILS verification if the store holds content that should shape the
answer. Generic word co-occurrence on an unrelated fact is not such content.
"""

from __future__ import annotations

VERDICTS = {
    ("leila", "What was the theme of the last book club meeting you attended?"):
        ("ABSENT",
         "sole hit lb_00038 'attended a meeting at the municipal heritage office' -- a work "
         "meeting, not a book club; 'attended'+'meeting' is generic co-occurrence"),
    ("lily", "What is your preferred brand and model of running shoes for exercise?"):
        ("ABSENT",
         "sole hit lb_00347 'Bonsoy oat milk as their preferred brand' -- oat milk, not "
         "running shoes; 'brand'+'preferred' is generic co-occurrence"),
    ("mirri", "Can you describe your favorite meal to cook at home and the recipe you use?"):
        ("ABSENT",
         "sole hit lb_00522 \"Bunjil's favorite birthday meal is damper with honey\" -- another "
         "person's birthday meal, not a recipe the user cooks; adjacent, not answering"),
}
