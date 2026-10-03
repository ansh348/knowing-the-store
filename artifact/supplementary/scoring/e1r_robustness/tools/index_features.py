"""Parser and feature extractor for the committed serialized indexes.

Reads ONLY the exact index strings the monitor was shown
(e1_metamemory/indexes_v2.json), keyed backend:persona:variant[:qid]:PROVENANCE.
No ground-truth field, category, label, or tier is ever read here.
"""
from __future__ import annotations

import re

from common_e1r import E1, jload

_CACHE = {}

STOP = {
    "what", "whats", "which", "who", "whom", "whose", "when", "where", "why", "how",
    "does", "do", "did", "is", "are", "was", "were", "has", "have", "had", "the", "a",
    "an", "of", "for", "to", "in", "on", "at", "and", "or", "any", "his", "her", "their",
    "with", "about", "from", "s", "t", "be", "been", "this", "that", "there", "it",
    "currently", "current", "now", "still", "upcoming", "recently", "you", "your",
}


def indexes():
    if "idx" not in _CACHE:
        _CACHE["idx"] = jload(E1 / "indexes_v2.json")["indexes"]
    return _CACHE["idx"]


def index_key(item, provenance):
    """Resolve an item to the exact index string it was shown."""
    b, p, v = item["backend"], item["persona"], item["variant"]
    if v == "SLOT-ABLATED":
        return f"{b}:{p}:SLOT:{item['question_id']}:{provenance}"
    return f"{b}:{p}:{v}:{provenance}"


def toks(s):
    return {w for w in re.split(r"[^a-z0-9]+", s.lower()) if w and w not in STOP and len(w) > 1}


NUMLINE = re.compile(r"^\s{2}(\w[\w ]*?)\s{2,}(\d+|not expressible.*)$")
CATROW = re.compile(r"^([A-Z][A-Z_]+)\s+((?:\d+\s+){5,7}\d*)\s*$")


def parse(text):
    """Structured view of one serialized index. Missing fields stay None."""
    out = {
        "total_entries": None, "lifecycle": {}, "recency": {}, "age_bands": {},
        "categories": {}, "attr_by_cat": {}, "superseded_attrs": [],
        "expressible": True,
    }
    if text is None:
        return out
    if "not expressible by this backend" in text:
        out["expressible"] = False

    m = re.search(r"entries in this store:\s*(\d+)", text)
    if m:
        out["total_entries"] = int(m.group(1))

    section = None
    lines = text.split("\n")
    for ln in lines:
        s = ln.rstrip()
        u = s.strip()
        if u.startswith("LIFECYCLE TOTALS"):
            section = "life"; continue
        if u.startswith("PER-CATEGORY BREAKDOWN"):
            section = "cat"; continue
        if u.startswith("RECENCY"):
            section = "rec"; continue
        if u.startswith("AGE DISTRIBUTION"):
            section = "age"; continue
        if u.startswith("ATTRIBUTE NAMES BY CATEGORY"):
            section = "attr"; continue
        if u.startswith("ATTRIBUTE NAMES CARRYING SUPERSEDED"):
            section = "sup"; continue
        if not u:
            continue

        if section in ("life", "rec", "age"):
            mm = NUMLINE.match(s)
            if mm:
                k = mm.group(1).strip().lower().replace(" ", "_")
                v = mm.group(2)
                val = int(v) if v.isdigit() else None
                {"life": out["lifecycle"], "rec": out["recency"],
                 "age": out["age_bands"]}[section][k] = val
        elif section == "cat":
            if u.startswith("CATEGORY"):
                continue
            mm = CATROW.match(u)
            if mm:
                nums = [int(x) for x in mm.group(2).split()]
                nm = mm.group(1)
                keys = ["entries", "active", "suprsd", "retract", "expired",
                        "newest", "oldest"]
                out["categories"][nm] = dict(zip(keys, nums))
        elif section == "attr":
            mm = re.match(r"^([A-Z][A-Z_]+):\s*(.*)$", u)
            if mm:
                cur = mm.group(1)
                out["attr_by_cat"].setdefault(cur, [])
                out["attr_by_cat"][cur] += _names(mm.group(2))
            elif out["attr_by_cat"]:
                last = list(out["attr_by_cat"])[-1]
                out["attr_by_cat"][last] += _names(u)
        elif section == "sup":
            out["superseded_attrs"] += _names(u)
    return out


def _names(s):
    s = re.sub(r"\(\+\d+ more\)", "", s)
    return [x.strip() for x in s.split(",") if x.strip()]


def _sing(w):
    return w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w


def assign_category(parsed, question):
    """Assign the question to a category by maximum content-token overlap with that
    category's attribute names. Ties break by Jaccard, then to the higher-ENTRIES
    category.

    DISCLOSED REFINEMENT of SPEC_E1R (b) NB-1, adopted before any baseline AUROC was
    computed and recorded in DEVIATIONS_E1R.md as D-E1R-1. The frozen text said
    "maximum content-token overlap"; a first implementation scored overlap by Jaccard
    alone and assigned almost nothing, because attribute names are terse relative to
    question length. Scoring by overlap COUNT, singularizing tokens, and letting the
    category name itself act as an attribute name all make this baseline STRONGER.
    The refinement therefore works against the paper's interest, which is the direction
    a baseline adjustment is allowed to move after a freeze.

    Returns (category or None, overlap_count, n_matched_attrs, best_attr).
    """
    qt = {_sing(w) for w in toks(question)}
    best, best_c, best_j, best_n, best_attr = None, 0, 0.0, 0, None
    for cat, attrs in parsed["attr_by_cat"].items():
        cands = list(attrs) + [cat]          # category name counts as a surface form
        c_best, j_best, n, ba = 0, 0.0, 0, None
        for a in cands:
            at = {_sing(w) for w in toks(a.replace("_", " "))}
            if not at:
                continue
            inter = len(qt & at)
            if inter:
                n += 1
            j = inter / len(qt | at) if (qt | at) else 0.0
            if inter > c_best or (inter == c_best and j > j_best):
                c_best, j_best, ba = inter, j, a
        ent = parsed["categories"].get(cat, {}).get("entries", 0)
        better = (c_best > best_c
                  or (c_best == best_c and j_best > best_j)
                  or (c_best == best_c and j_best == best_j and best is not None
                      and ent > parsed["categories"].get(best, {}).get("entries", 0)))
        if c_best > 0 and better:
            best, best_c, best_j, best_n, best_attr = cat, c_best, j_best, n, ba
    return best, best_c, best_n, best_attr


def features(item, provenance, question):
    """Numeric feature vector for NB-2, plus the pieces NB-1/NB-4 need."""
    txt = indexes().get(index_key(item, provenance))
    p = parse(txt)
    cat, ov, nmatch, battr = assign_category(p, question)
    c = p["categories"].get(cat, {}) if cat else {}
    tot = p["total_entries"] or 0
    max_ent = max((v.get("entries", 0) for v in p["categories"].values()), default=0)
    stale = c.get("suprsd", 0) + c.get("retract", 0) + c.get("expired", 0)
    f = {
        "total_entries": tot,
        "n_categories": len(p["categories"]),
        "life_active": p["lifecycle"].get("active") or 0,
        "life_superseded": p["lifecycle"].get("superseded") or 0,
        "life_retracted": p["lifecycle"].get("retracted") or 0,
        "life_expired": p["lifecycle"].get("expired") or 0,
        "life_supersession_events": p["lifecycle"].get("supersession_events") or 0,
        "cat_entries": c.get("entries", 0),
        "cat_active": c.get("active", 0),
        "cat_suprsd": c.get("suprsd", 0),
        "cat_retract": c.get("retract", 0),
        "cat_expired": c.get("expired", 0),
        "cat_stale": stale,
        "cat_stale_frac": stale / max(1, c.get("entries", 0)),
        "overlap": ov,
        "n_matched_attrs": nmatch,
        "top_attr_is_superseded": int(bool(battr and battr in p["superseded_attrs"])),
        "n_superseded_attrs": len(p["superseded_attrs"]),
        "expressible": int(p["expressible"]),
        "age_0_30": p["age_bands"].get("0-30") or 0,
        "age_over_365": p["age_bands"].get("over_365") or 0,
        "median_age": p["recency"].get("median_entry_age") or 0,
    }
    # NB-1 deterministic rule scores
    fok_rule = (c.get("entries", 0) / max_ent) if max_ent else (tot / 1000.0)
    nok_rule = stale / max(1, c.get("entries", 0)) if cat else 0.0
    if not p["expressible"] or not p["categories"]:
        fok_rule = tot / 1000.0
        nok_rule = 0.0
    return f, float(fok_rule), float(nok_rule), p, txt
