r"""
lifecycle_bank.py - Standalone lifecycle memory bank with FR behavioral ontology.

Replaces Graphiti as the infrastructure layer while keeping all of FR's
lifecycle policies: category-specific decay, supersession, retraction,
expiry, numeric preservation, and category-forced retrieval.

Models (all GPT, no Grok):
    - Extraction + classification: gpt-4.1-mini (one combined call per fact)
    - Query classification: gpt-4.1-mini
    - Embeddings: text-embedding-3-small (1536-dim)
"""

import asyncio
import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

from eval_common import Candidate

# ===========================================================================
# Model constants
# ===========================================================================

EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536
INGESTION_MODEL = "gpt-4.1-mini"
QUERY_CLASSIFY_MODEL = "gpt-4.1-mini"

# Set to "flex" for 50% discount (Batch API rates). Callers toggle this.
FLEX_TIER = None

# ===========================================================================
# Category-specific parameters
# ===========================================================================

# Decay rate lambda (per hour) — how fast activation decays
DECAY_LAMBDA = {
    "IDENTITY_SELF_CONCEPT":  0.0015,
    "RELATIONAL_BONDS":       0.0015,
    "INTELLECTUAL_INTERESTS":  0.0020,
    "HEALTH_WELLBEING":       0.0025,
    "PROJECTS_ENDEAVORS":     0.0025,
    "HOBBIES_RECREATION":     0.0035,
    "PREFERENCES_HABITS":     0.0050,
    "FINANCIAL_MATERIAL":     0.0055,
    "OBLIGATIONS":            0.0060,
    "LOGISTICAL_CONTEXT":     0.0080,
    "OTHER":                  0.0050,
}

# Blending weight alpha: blended = alpha*activation + (1-alpha)*semantic
BLEND_ALPHA = {
    "FINANCIAL_MATERIAL":     0.05,
    "IDENTITY_SELF_CONCEPT":  0.10,
    "HEALTH_WELLBEING":       0.10,
    "RELATIONAL_BONDS":       0.10,
    "INTELLECTUAL_INTERESTS":  0.15,
    "PREFERENCES_HABITS":     0.20,
    "HOBBIES_RECREATION":     0.20,
    "PROJECTS_ENDEAVORS":     0.30,
    "OBLIGATIONS":            0.35,
    "LOGISTICAL_CONTEXT":     0.40,
    "OTHER":                  0.20,
}

# Semantic floor per category — applied when semantic >= 0.85
SEMANTIC_FLOOR = {
    "FINANCIAL_MATERIAL":     0.97,
    "IDENTITY_SELF_CONCEPT":  0.95,
    "HEALTH_WELLBEING":       0.95,
    "RELATIONAL_BONDS":       0.95,
    "INTELLECTUAL_INTERESTS":  0.90,
    "PREFERENCES_HABITS":     0.85,
    "HOBBIES_RECREATION":     0.92,
    "PROJECTS_ENDEAVORS":     0.75,
    "OBLIGATIONS":            0.70,
    "LOGISTICAL_CONTEXT":     0.00,
    "OTHER":                  0.50,
}

VALID_CATEGORIES = frozenset(DECAY_LAMBDA.keys())

# ===========================================================================
# Helpers — numeric detection
# ===========================================================================

_NUMERIC_RESCUE_RE = re.compile(
    r'(?:'
    r'[\$\u20ac\u00a3\u00a5\u20ab]\s*[\d,]+(?:\.\d+)?'
    r'|[\d,]+(?:\.\d+)?\s*(?:dong|pesos?|kroner?|kronor|dirhams?|euros?|dollars?|pounds?)'
    r'|[\d,]+(?:\.\d+)?\s+(?:million|billion|thousand)\b'
    r'|\d{1,3}(?:,\d{3}){2,}'
    r')', re.I,
)


def _contains_monetary_or_quantity(text: str) -> bool:
    return bool(_NUMERIC_RESCUE_RE.search(text))


# ===========================================================================
# Helpers — backward-looking / retraction query detection
# ===========================================================================


def _is_backward_looking(question: str) -> bool:
    q = question.lower()
    phrases = [
        "before switching", "before he moved", "before she stopped",
        "before they changed", "before she moved", "before he stopped",
        "used to", "previously", "prior to", "back when",
        "old ", "former ", "original ",
    ]
    if any(p in q for p in phrases):
        return True
    past_patterns = [
        r"\bhow (?:much|often|many) (?:was|were|did)\b",
        r"\bwhat (?:was|were|did)\b",
        r"\bbefore (?:he|she|they|it)\b",
        r"\bdid .+ before\b",
    ]
    return any(re.search(p, q) for p in past_patterns)


def _is_retraction_query(question: str) -> bool:
    q = question.lower()
    patterns = [
        r"\bis \w+ (?:still )?planning\b",
        r"\bis \w+ still (?:doing|going|working|looking|pursuing)\b",
        r"\bdoes \w+ still (?:plan|want|intend)\b",
        r"\bis \w+ still interested in\b",
        r"\bis \w+ (?:planning|going) to (?:buy|get|open|start|do)\b",
    ]
    return any(re.search(p, q) for p in patterns)


# ===========================================================================
# Helpers — lightweight entity extraction (for multi-hop retrieval)
# ===========================================================================

_STOPWORDS = frozenset({
    'the', 'this', 'that', 'user', 'they', 'their', 'them',
    'she', 'her', 'his', 'him', 'has', 'had', 'was', 'were',
    'been', 'being', 'also', 'just', 'very', 'some', 'much',
    'not', 'but', 'and', 'for', 'with', 'from', 'about',
    'into', 'over', 'after', 'before', 'between', 'each',
    'than', 'when', 'where', 'while', 'which', 'would',
    'could', 'should', 'have', 'does', 'did', 'will',
    'may', 'can', 'are', 'now', 'new', 'per', 'recently',
})


def _extract_entities_regex(text: str) -> list[str]:
    """Extract named entities and key noun phrases via regex (no LLM/spaCy).

    Returns deduplicated list of:
    - Capitalized multi-word phrases (proper nouns)
    - Single capitalized words that aren't common stopwords
    - Quoted strings
    - Numbers with units / currency
    """
    entities: list[str] = []
    seen_lower: set[str] = set()

    def _add(phrase: str):
        phrase = phrase.strip()
        if len(phrase) < 2:
            return
        key = phrase.lower()
        if key not in seen_lower and key not in _STOPWORDS:
            seen_lower.add(key)
            entities.append(phrase)

    # 1. Quoted strings
    for m in re.finditer(r'"([^"]{2,60})"', text):
        _add(m.group(1))
    for m in re.finditer(r"'([^']{2,60})'", text):
        _add(m.group(1))

    # 2. Capitalized multi-word phrases (2-5 words): "New York", "Mount Everest"
    for m in re.finditer(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4})\b', text):
        _add(m.group(1))

    # 3. Single capitalized words (>= 3 chars, not at sentence start)
    for m in re.finditer(r'(?<![.!?]\s)(?<!^)\b([A-Z][a-z]{2,})\b', text):
        _add(m.group(1))

    # 4. Numbers with units / currency
    for m in re.finditer(
        r'[\$\u20ac\u00a3\u00a5]\s*[\d,]+(?:\.\d+)?'
        r'|\d[\d,]*(?:\.\d+)?\s*(?:kg|lbs?|miles?|km|hours?|minutes?|days?'
        r'|weeks?|months?|years?|dollars?|euros?|pounds?|percent|%|mg|ml)\b',
        text, re.I,
    ):
        _add(m.group(0))

    return entities[:10]  # cap to bound embedding cost


# ===========================================================================
# Helpers — date parsing
# ===========================================================================


def _parse_session_date_dt(date_str: str) -> datetime:
    """Convert session date string to UTC datetime."""
    if not date_str:
        return datetime.now(tz=timezone.utc)
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        pass
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return datetime.now(tz=timezone.utc)


# ===========================================================================
# LifecycleEntry
# ===========================================================================


@dataclass
class LifecycleEntry:
    id: str
    text: str                                       # extracted fact text
    embedding: np.ndarray                            # 1536-dim
    category: str                                    # primary behavioral category
    category_weights: dict                           # soft membership, sums to 1.0
    slot_key: tuple | None = None                    # (subject, attribute)
    event_time: datetime | None = None               # for obligations/logistics
    is_retracted: bool = False                       # explicit retraction detected
    confidence: float = 0.9                          # 0-1
    supersedes: str | None = None                    # ID of entry this supersedes
    is_active: bool = True                           # False if superseded
    created_at: datetime = field(
        default_factory=lambda: datetime.now(tz=timezone.utc))
    source_session: int = 0
    emotional_loading: float = 0.0                   # 0-1, placeholder
    numeric_value: bool = False                      # contains monetary/quantity


# ===========================================================================
# Serialization helpers
# ===========================================================================


def _entry_to_dict(e: LifecycleEntry) -> dict:
    return {
        "id": e.id,
        "text": e.text,
        "category": e.category,
        "category_weights": e.category_weights,
        "slot_key": list(e.slot_key) if e.slot_key else None,
        "event_time": e.event_time.isoformat() if e.event_time else None,
        "is_retracted": e.is_retracted,
        "confidence": e.confidence,
        "supersedes": e.supersedes,
        "is_active": e.is_active,
        "created_at": e.created_at.isoformat(),
        "source_session": e.source_session,
        "emotional_loading": e.emotional_loading,
        "numeric_value": e.numeric_value,
    }


def _dict_to_entry(d: dict, embedding: np.ndarray) -> LifecycleEntry:
    slot_raw = d.get("slot_key")
    slot_key = None
    if slot_raw and isinstance(slot_raw, (list, tuple)) and len(slot_raw) == 2:
        slot_key = (str(slot_raw[0]), str(slot_raw[1]))

    event_time = None
    raw_evt = d.get("event_time")
    if raw_evt:
        try:
            event_time = datetime.fromisoformat(str(raw_evt))
            if event_time.tzinfo is None:
                event_time = event_time.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            pass

    try:
        created_at = datetime.fromisoformat(d["created_at"])
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError, KeyError):
        created_at = datetime.now(tz=timezone.utc)

    return LifecycleEntry(
        id=d["id"],
        text=d["text"],
        embedding=embedding,
        category=d.get("category", "OTHER"),
        category_weights=d.get("category_weights", {"OTHER": 1.0}),
        slot_key=slot_key,
        event_time=event_time,
        is_retracted=d.get("is_retracted", False),
        confidence=d.get("confidence", 0.9),
        supersedes=d.get("supersedes"),
        is_active=d.get("is_active", True),
        created_at=created_at,
        source_session=d.get("source_session", 0),
        emotional_loading=d.get("emotional_loading", 0.0),
        numeric_value=d.get("numeric_value", False),
    )


# ===========================================================================
# LifecycleBank
# ===========================================================================


class LifecycleBank:
    """Flat in-memory store with vectorized cosine similarity and BM25."""

    def __init__(self):
        self.entries: dict[str, LifecycleEntry] = {}
        self._emb_matrix: np.ndarray | None = None  # stacked normalized
        self._emb_ids: list[str] = []                # parallel to rows
        self._bm25: BM25Okapi | None = None
        self._bm25_ids: list[str] = []               # parallel to BM25 corpus
        self._dirty: bool = True
        self._next_id: int = 0

    def _gen_id(self) -> str:
        self._next_id += 1
        return f"lb_{self._next_id:05d}"

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return text.lower().split()

    def _rebuild(self):
        active = [(eid, e) for eid, e in self.entries.items() if e.is_active]
        if not active:
            self._emb_matrix = None
            self._emb_ids = []
            self._bm25 = None
            self._bm25_ids = []
        else:
            self._emb_ids = [eid for eid, _ in active]
            mat = np.stack([e.embedding for _, e in active])
            norms = np.linalg.norm(mat, axis=1, keepdims=True) + 1e-12
            self._emb_matrix = mat / norms
            # BM25 index
            self._bm25_ids = [eid for eid, _ in active]
            corpus = [self._tokenize(e.text) for _, e in active]
            self._bm25 = BM25Okapi(corpus)
        self._dirty = False

    def _rebuild_matrix(self):
        """Alias for backward compat — calls unified _rebuild."""
        self._rebuild()

    # ---- mutations ----

    def add(self, entry: LifecycleEntry) -> str:
        if not entry.id:
            entry.id = self._gen_id()
        self.entries[entry.id] = entry
        self._dirty = True
        return entry.id

    def deactivate(self, entry_id: str) -> None:
        if entry_id in self.entries:
            self.entries[entry_id].is_active = False
            self._dirty = True

    # ---- queries ----

    def get_by_slot_key(self, slot_key: tuple) -> list[LifecycleEntry]:
        return [e for e in self.entries.values()
                if e.is_active and e.slot_key == slot_key]

    def get_by_category(self, category: str) -> list[LifecycleEntry]:
        return [e for e in self.entries.values()
                if e.is_active and e.category == category]

    def active_entries(self) -> list[LifecycleEntry]:
        return [e for e in self.entries.values() if e.is_active]

    def all_entries_list(self) -> list[LifecycleEntry]:
        """Return all entries regardless of is_active."""
        return list(self.entries.values())

    def get_by_category_all(self, category: str) -> list[LifecycleEntry]:
        """Return all entries (active + inactive) of given category."""
        return [e for e in self.entries.values() if e.category == category]

    def cosine_search_all(self, query_emb: np.ndarray,
                          k: int = 60) -> list[tuple[LifecycleEntry, float]]:
        """Like cosine_search but includes inactive (superseded) entries."""
        all_e = list(self.entries.values())
        if not all_e:
            return []
        mat = np.stack([e.embedding for e in all_e])
        norms = np.linalg.norm(mat, axis=1, keepdims=True) + 1e-12
        q_norm = query_emb / (np.linalg.norm(query_emb) + 1e-12)
        sims = (mat / norms) @ q_norm
        top_k = min(k, len(all_e))
        top_idx = np.argsort(-sims)[:top_k]
        return [(all_e[i], float(sims[i])) for i in top_idx]

    def bm25_search_all(self, query: str,
                        k: int = 20) -> list[LifecycleEntry]:
        """Like bm25_search but includes inactive (superseded) entries."""
        all_e = list(self.entries.values())
        if not all_e:
            return []
        corpus = [self._tokenize(e.text) for e in all_e]
        bm25 = BM25Okapi(corpus)
        tokens = self._tokenize(query)
        if not tokens:
            return []
        scores = bm25.get_scores(tokens)
        top_k = min(k, len(all_e))
        top_idx = np.argsort(-scores)[:top_k]
        return [all_e[i] for i in top_idx if scores[i] > 0]

    def cosine_search(self, query_emb: np.ndarray,
                      k: int = 60) -> list[tuple[LifecycleEntry, float]]:
        """Return (entry, cosine_similarity) for top-k active entries."""
        if self._dirty:
            self._rebuild()
        if self._emb_matrix is None or len(self._emb_ids) == 0:
            return []
        q_norm = query_emb / (np.linalg.norm(query_emb) + 1e-12)
        sims = self._emb_matrix @ q_norm
        top_k = min(k, len(self._emb_ids))
        top_idx = np.argsort(-sims)[:top_k]
        return [(self.entries[self._emb_ids[i]], float(sims[i]))
                for i in top_idx]

    def bm25_search(self, query: str, k: int = 20) -> list[LifecycleEntry]:
        """Return top-k active entries by BM25 keyword match."""
        if self._dirty:
            self._rebuild()
        if self._bm25 is None or not self._bm25_ids:
            return []
        tokens = self._tokenize(query)
        if not tokens:
            return []
        scores = self._bm25.get_scores(tokens)
        top_k = min(k, len(self._bm25_ids))
        top_idx = np.argsort(-scores)[:top_k]
        return [self.entries[self._bm25_ids[i]]
                for i in top_idx if scores[i] > 0]

    # ---- persistence ----

    def save(self, path: Path) -> None:
        """Save bank to JSON (metadata) + .npz (embeddings)."""
        path.parent.mkdir(parents=True, exist_ok=True)
        meta_path = path.with_suffix(".json")
        emb_path = path.with_name(path.stem + "_embeddings.npz")

        meta = {
            "next_id": self._next_id,
            "entries": [_entry_to_dict(e) for e in self.entries.values()],
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        if self.entries:
            ids = list(self.entries.keys())
            mat = np.stack([self.entries[eid].embedding for eid in ids])
            np.savez_compressed(emb_path, ids=np.array(ids, dtype=object),
                                embeddings=mat)
        else:
            np.savez_compressed(emb_path, ids=np.array([], dtype=object),
                                embeddings=np.zeros((0, EMBED_DIM)))

    @classmethod
    def load(cls, path: Path) -> "LifecycleBank":
        """Load bank from JSON + .npz."""
        meta_path = path.with_suffix(".json")
        emb_path = path.with_name(path.stem + "_embeddings.npz")
        if not emb_path.exists():
            emb_path = path.with_name(path.stem + "_embeddings.npy")

        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)

        data = np.load(emb_path, allow_pickle=True)
        ids = data["ids"]
        embeddings = data["embeddings"]
        emb_map = {str(ids[i]): embeddings[i] for i in range(len(ids))}

        bank = cls()
        bank._next_id = meta.get("next_id", 0)
        for d in meta["entries"]:
            emb = emb_map.get(d["id"], np.zeros(EMBED_DIM, dtype=np.float32))
            bank.entries[d["id"]] = _dict_to_entry(d, emb)
        bank._dirty = True
        return bank

    def __len__(self) -> int:
        return len(self.entries)


# ===========================================================================
# Embedding helpers
# ===========================================================================

_embed_sem = asyncio.Semaphore(200)


def _sanitize_text(text: str) -> str:
    """Strip null bytes and control characters that break JSON serialization."""
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text).strip() or "empty"


async def embed_text(text: str, openai_client) -> np.ndarray:
    async with _embed_sem:
        resp = await openai_client.embeddings.create(
            model=EMBED_MODEL, input=[_sanitize_text(text)], dimensions=EMBED_DIM,
        )
        return np.array(resp.data[0].embedding, dtype=np.float32)


async def embed_texts(texts: list[str], openai_client) -> list[np.ndarray]:
    if not texts:
        return []
    cleaned = [_sanitize_text(t) for t in texts]
    async with _embed_sem:
        try:
            resp = await openai_client.embeddings.create(
                model=EMBED_MODEL, input=cleaned, dimensions=EMBED_DIM,
            )
            return [np.array(d.embedding, dtype=np.float32) for d in resp.data]
        except Exception:
            # Fallback: embed one at a time, zero-vec on failure
            results = []
            for t in cleaned:
                try:
                    r = await openai_client.embeddings.create(
                        model=EMBED_MODEL, input=[t[:8000]], dimensions=EMBED_DIM,
                    )
                    results.append(np.array(r.data[0].embedding, dtype=np.float32))
                except Exception:
                    results.append(np.zeros(EMBED_DIM, dtype=np.float32))
            return results


# ===========================================================================
# Ingestion — combined extraction + classification in ONE LLM call
# ===========================================================================

INGESTION_SYSTEM_PROMPT = """\
You are a memory extraction and classification system. Given a conversation turn with session context, extract all personal facts about the user.

Extract two kinds of facts worth remembering across future conversations:

1. PERSONAL FACTS about the user: durable traits, preferences, relationships, goals, life events. Do NOT extract transient states ("I have a migraine today"), session-specific logistics that expire within days, repetitions of previously stated facts, or conversational filler. Quality over quantity — aim for 0-3 meaningful facts per turn.

IMPORTANT — temporal context: When the conversation mentions specific dates, days of the week, times, or temporal references (e.g. "last Saturday", "on February 10th", "three days ago"), ALWAYS include the temporal context in the fact text. Write "User visited MoMA on January 8" not just "User visited MoMA". Write "User bought a necklace on February 10th, 2023" not just "User bought a necklace". This temporal detail is critical for answering questions about when events happened.

2. ASSISTANT-PROVIDED information the user may want to recall later: specific recommendations (restaurant names, book/movie titles, product names), generated lists or tables, factual answers the assistant gave to user questions, schedules or plans the assistant created, and specific names/terms/data the assistant provided. Write these as natural recall statements from the user's perspective (e.g. "By Chloe was recommended as a vegan restaurant in NYC", "The 27th prompt parameter is Sound Effects", "Admon was assigned to the Day Shift on Sundays"). Do NOT prefix with "Assistant provided:". Use category OTHER.

If a turn contains no new durable information of either kind, return [].

For EACH fact, return a JSON object with:
- text: the fact as a standalone statement (e.g. "User moved to Austin", "User's salary is $120,000")
- category: primary category, one of: IDENTITY_SELF_CONCEPT, RELATIONAL_BONDS, INTELLECTUAL_INTERESTS, HEALTH_WELLBEING, PROJECTS_ENDEAVORS, HOBBIES_RECREATION, PREFERENCES_HABITS, FINANCIAL_MATERIAL, OBLIGATIONS, LOGISTICAL_CONTEXT, OTHER
- category_weights: dict of category -> weight for soft membership (primary >= 0.3, all weights sum to 1.0, include only categories with weight > 0.05)
- slot_key: [subject, attribute] if this fact occupies a slot that could be superseded by a future update.

  For attributes that can have MULTIPLE INSTANCES (family members, hobbies, health conditions, relationships), qualify the slot_key with the specific instance:
  - ["user", "family_member:yasmin"] not ["user", "family_member"]
  - ["user", "hobby:fishing"] not ["user", "hobby_primary"]
  - ["user", "health_condition:anxiety"] not ["user", "medical_condition"]
  - ["user", "relationship:alex"] not ["user", "relationship_status"]
  - ["user", "project:startup"] not ["user", "project_status"]
  - ["user", "friend:jake"] not ["user", "friend"]

  For attributes that are truly SINGULAR (one value at a time), keep unqualified:
  - ["user", "current_city"] — user lives in one city
  - ["user", "employer"] — user has one employer
  - ["user", "job_title"] — user has one title
  - ["user", "dietary_preference"] — user has one diet
  - ["user", "salary"] — user has one salary
  - ["user", "rent"] — user has one rent amount
  - ["user", "marital_status"] — user has one status
  - ["user", "living_arrangement"] — user has one living situation
  - ["user", "exercise_routine"] — user has one current routine
  - ["user", "pet_status"] — user has one current pet situation

  The rule: if a person can have MULTIPLE simultaneous values, qualify with the instance name (the person's name, the hobby name, the condition name). If a person has ONE value that gets replaced over time, keep it unqualified so supersession fires correctly.

  Use EXACTLY these attribute patterns — do not invent synonyms. If a fact doesn't fit any canonical attribute, use a descriptive attribute but keep it short and generic (e.g. "vehicle" not "car_ownership_status").

  Multiple facts about the same real-world attribute MUST use the same key. "User is vegetarian", "User started eating fish", "User is pescatarian" should ALL use ["user", "dietary_preference"].

  null if the fact has no natural slot (e.g. a one-off observation with no update semantics).
- event_time: ISO date string (YYYY-MM-DD) if this fact has a specific deadline, appointment, or event date. null otherwise.
- is_retracted: true ONLY if the user is explicitly cancelling, abandoning, or retracting something they previously stated (e.g. "forget about the Denver move", "that plan is dead", "I quit vaping"). false for normal facts.
- confidence: 0.0 to 1.0. How certain is this fact? Use 0.9+ for definitive statements ("I moved to London"), 0.5-0.8 for tentative ones ("I'm thinking about moving"), 0.3-0.5 for uncertain mentions.
- has_numeric_value: true if the fact contains specific numbers, monetary amounts, or quantities (e.g. "$950/month", "7 bass", "3 siblings")

Use the full session context to make accurate classifications. A fact mentioned while discussing insurance paperwork might actually be an identity fact (name change), not an obligation.

Return a JSON array of fact objects. If no personal facts, return [].
Return JSON only, no explanation or markdown fences."""

_ingest_sem = asyncio.Semaphore(200)


DEDUP_THRESHOLD = 0.95  # cosine similarity above which a fact is a near-duplicate

# Accumulate categories: facts coexist, supersession requires higher confidence
ACCUMULATE_CATEGORIES = frozenset({
    "IDENTITY_SELF_CONCEPT", "RELATIONAL_BONDS", "HOBBIES_RECREATION",
    "INTELLECTUAL_INTERESTS", "HEALTH_WELLBEING",
})


async def ingest_turn(
    turn_text: str,
    session_context: str,
    session_id: int,
    session_date: str,
    bank: LifecycleBank,
    openai_client,
    role: str = "user",
    verbose: bool = False,
) -> list[str]:
    """Extract facts from one user turn and add to bank.

    Returns list of new entry IDs added.  Skips near-duplicates
    (cosine > DEDUP_THRESHOLD against existing active entries).
    """
    if not turn_text.strip():
        return []

    role_label = "ASSISTANT" if role == "assistant" else "USER"
    user_msg = (
        f"SESSION CONTEXT (previous turns this session):\n{session_context}\n\n"
        f"CURRENT TURN ({role_label}):\n{turn_text}\n\n"
        f"SESSION DATE: {session_date}\n\n"
        f"Extract and classify all personal facts."
    )

    async with _ingest_sem:
        try:
            resp = await openai_client.chat.completions.create(
                model=INGESTION_MODEL,
                temperature=0,
                messages=[
                    {"role": "system", "content": INGESTION_SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=2000,
                **({"service_tier": FLEX_TIER} if FLEX_TIER else {}),
            )
            raw = resp.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = re.sub(r"^```(?:json)?\s*", "", raw)
                raw = re.sub(r"\s*```$", "", raw)
            facts = json.loads(raw)
            if isinstance(facts, dict):
                for key in ("facts", "results", "data"):
                    if key in facts and isinstance(facts[key], list):
                        facts = facts[key]
                        break
                else:
                    facts = []
            if not isinstance(facts, list):
                return []
        except Exception:
            return []

    valid_facts = [f for f in facts if isinstance(f, dict) and f.get("text")]
    if not valid_facts:
        return []

    # Batch-embed all extracted fact texts
    fact_texts = [f["text"] for f in valid_facts]
    fact_embeddings = await embed_texts(fact_texts, openai_client)

    created_at = _parse_session_date_dt(session_date)

    new_ids: list[str] = []
    for fact_obj, fact_emb in zip(valid_facts, fact_embeddings):
        text = fact_obj["text"]

        # --- Parse category ---
        category = fact_obj.get("category", "OTHER")
        if category not in VALID_CATEGORIES:
            category = "OTHER"

        # --- Parse category weights ---
        cat_weights = {}
        raw_weights = fact_obj.get("category_weights", {})
        if isinstance(raw_weights, dict):
            for cat in VALID_CATEGORIES:
                w = raw_weights.get(cat, 0.0)
                if isinstance(w, (int, float)) and w > 0:
                    cat_weights[cat] = float(w)
        total_w = sum(cat_weights.values())
        if total_w > 0:
            cat_weights = {k: v / total_w for k, v in cat_weights.items()}
        else:
            cat_weights = {category: 1.0}

        # --- Parse slot_key ---
        slot_key = None
        raw_slot = fact_obj.get("slot_key")
        if raw_slot and isinstance(raw_slot, (list, tuple)) and len(raw_slot) == 2:
            slot_key = (str(raw_slot[0]), str(raw_slot[1]))

        # --- Parse event_time ---
        event_time = None
        raw_evt = fact_obj.get("event_time")
        if raw_evt:
            try:
                event_time = datetime.fromisoformat(str(raw_evt))
                if event_time.tzinfo is None:
                    event_time = event_time.replace(tzinfo=timezone.utc)
            except (ValueError, TypeError):
                pass

        is_retracted = bool(fact_obj.get("is_retracted", False))
        confidence = float(fact_obj.get("confidence", 0.9))
        has_numeric = bool(fact_obj.get("has_numeric_value", False))
        numeric_value = has_numeric or _contains_monetary_or_quantity(text)

        # --- Cosine deduplication (exempt numeric facts) ---
        if not numeric_value and bank.active_entries():
            top_match = bank.cosine_search(fact_emb, k=1)
            if top_match and top_match[0][1] > DEDUP_THRESHOLD:
                if verbose:
                    print(f"      DEDUP skip (sim={top_match[0][1]:.3f}): "
                          f"{text[:80]}")
                continue

        entry = LifecycleEntry(
            id="",
            text=text,
            embedding=fact_emb,
            category=category,
            category_weights=cat_weights,
            slot_key=slot_key,
            event_time=event_time,
            is_retracted=is_retracted,
            confidence=confidence,
            supersedes=None,
            is_active=True,
            created_at=created_at,
            source_session=session_id,
            emotional_loading=0.0,
            numeric_value=numeric_value,
        )

        # --- Supersession detection ---
        if slot_key is not None:
            existing = bank.get_by_slot_key(slot_key)
            if existing:
                # Accumulate categories need higher confidence to supersede
                threshold = (0.95 if category in ACCUMULATE_CATEGORIES
                             else 0.80)
                if confidence >= threshold:
                    existing.sort(key=lambda e: e.created_at, reverse=True)
                    entry.supersedes = existing[0].id
                    for old in existing:
                        bank.deactivate(old.id)

        # --- Retraction handling ---
        if is_retracted:
            results = bank.cosine_search(fact_emb, k=10)
            for related_entry, sim in results:
                if sim > 0.85:
                    bank.deactivate(related_entry.id)

        entry_id = bank.add(entry)
        new_ids.append(entry_id)

    return new_ids


# ===========================================================================
# Query classification
# ===========================================================================

QUERY_CLASSIFY_SYSTEM = """\
You classify questions about a user into the behavioral memory category most likely to store the answer.

Categories:
- IDENTITY_SELF_CONCEPT: core traits, occupation, heritage, values, name
- RELATIONAL_BONDS: family, friends, colleagues, relationships
- INTELLECTUAL_INTERESTS: curiosities, learning goals, academic interests
- HEALTH_WELLBEING: physical/mental health, medications, fitness, diet
- PROJECTS_ENDEAVORS: ongoing work, startups, research, creative projects
- HOBBIES_RECREATION: leisure activities, sports, active hobbies with skill/equipment
- PREFERENCES_HABITS: tastes, routines, media, food choices
- FINANCIAL_MATERIAL: budget, income, purchases, assets, salary
- OBLIGATIONS: tasks, deadlines, appointments, promises
- LOGISTICAL_CONTEXT: transient scheduling, one-time locations, errands
- OTHER: miscellaneous

Think about WHERE the answer lives in memory, not what the question asks about.
Return JSON: {"category": "CATEGORY_NAME"}"""

_query_classify_cache: dict[str, str] = {}


async def classify_query_gpt(query: str, openai_client) -> str:
    """Predict which category stores the answer to this query."""
    if query in _query_classify_cache:
        return _query_classify_cache[query]
    try:
        resp = await openai_client.chat.completions.create(
            model=QUERY_CLASSIFY_MODEL,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": QUERY_CLASSIFY_SYSTEM},
                {"role": "user", "content": query},
            ],
            max_tokens=50,
            **({"service_tier": FLEX_TIER} if FLEX_TIER else {}),
        )
        raw = json.loads(resp.choices[0].message.content.strip())
        cat = raw.get("category", "OTHER")
        if cat not in VALID_CATEGORIES:
            cat = "OTHER"
        _query_classify_cache[query] = cat
        return cat
    except Exception:
        return "OTHER"


# ===========================================================================
# Retrieval — FR's full lifecycle stack on flat bank
# ===========================================================================

CATEGORY_FORCED_FLOOR = 0.80  # minimum semantic for category-routed additions


BM25_SEMANTIC_FLOOR = 0.75  # semantic score for BM25-only entries

MULTIHOP_SEMANTIC_FLOOR = 0.70  # floor for second-hop entity-driven additions

_distill_sem = asyncio.Semaphore(30)

DISTILL_SYSTEM = """\
Given a question and a set of candidate memories about a user, select the memories most relevant to answering the question. Return the IDs of the selected memories as a JSON list, ordered by relevance. Select at most 20 memories."""

DISTILL_USER = """\
Question: {query}

Candidate memories:
{candidates}

Return JSON list of IDs only."""


async def _distill_candidates(
    query: str,
    pool: dict[str, tuple["LifecycleEntry", float]],
    openai_client,
) -> dict[str, tuple["LifecycleEntry", float]]:
    """Use GPT-4.1-mini to select top-20 most relevant candidates."""
    if len(pool) <= 20:
        return pool

    # Build numbered list
    lines = []
    for eid, (entry, _) in pool.items():
        lines.append(f"{eid}: {entry.text[:200]}")
    candidates_text = "\n".join(lines)

    user_msg = DISTILL_USER.format(query=query, candidates=candidates_text)

    async with _distill_sem:
        try:
            resp = await openai_client.chat.completions.create(
                model=INGESTION_MODEL,
                temperature=0,
                messages=[
                    {"role": "system", "content": DISTILL_SYSTEM},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=500,
                **({"service_tier": FLEX_TIER} if FLEX_TIER else {}),
            )
            raw = resp.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = re.sub(r"^```(?:json)?\s*", "", raw)
                raw = re.sub(r"\s*```$", "", raw)
            selected_ids = json.loads(raw)
            if not isinstance(selected_ids, list):
                return pool
            # Keep only selected IDs that exist in pool
            distilled = {}
            for eid in selected_ids:
                eid = str(eid)
                if eid in pool:
                    distilled[eid] = pool[eid]
            return distilled if distilled else pool
        except Exception:
            return pool


async def lifecycle_search(
    query: str,
    bank: LifecycleBank,
    t_now: datetime,
    openai_client,
    limit: int = 10,
    multihop: bool = True,
    no_lifecycle: bool = False,
    include_inactive: bool = False,
    temporal_query: bool = False,
    skip_distill: bool = False,
) -> list[tuple[Candidate, float, float, float]]:
    """FR's full lifecycle retrieval stack on LifecycleBank.

    Pipeline: cosine top-60 → BM25 top-20 → category-forced top-20
    → [multi-hop entity expansion] → merge/dedup → distillation to top-20
    → lifecycle filters → blended scoring → top-10.

    When no_lifecycle=True, disables all lifecycle operations (decay,
    supersession, expiry, retraction, category-specific blending) but
    keeps the retrieval pipeline (cosine, BM25, category-forced, multi-hop,
    distillation).  Used for ablation to isolate retrieval contribution.

    When include_inactive=True, searches all entries (active + inactive)
    but still applies lifecycle scoring.  Used for knowledge-update
    questions that ask about previous/superseded values.

    Returns (Candidate, activation, semantic, blended) tuples sorted by
    blended score descending — same format eval_common.score_question expects.
    """
    _search_all = no_lifecycle or include_inactive
    entries = bank.all_entries_list() if _search_all else bank.active_entries()
    if not entries:
        return []

    # =================================================================
    # 1. Embed query, cosine similarity over entries → top-60
    # =================================================================
    query_emb = await embed_text(query, openai_client)
    if _search_all:
        top60 = bank.cosine_search_all(query_emb, k=60)
    else:
        top60 = bank.cosine_search(query_emb, k=60)

    # Build candidate pool: {entry_id: (entry, semantic_score)}
    pool: dict[str, tuple[LifecycleEntry, float]] = {}
    cosine_ids: set[str] = set()
    for entry, sim in top60:
        pool[entry.id] = (entry, sim)
        cosine_ids.add(entry.id)

    # =================================================================
    # 2. BM25 keyword retrieval → top-20
    # =================================================================
    bm25_hits = (bank.bm25_search_all(query, k=20) if _search_all
                 else bank.bm25_search(query, k=20))
    bm25_only_ids: set[str] = set()
    q_norm = query_emb / (np.linalg.norm(query_emb) + 1e-12)
    for entry in bm25_hits:
        if entry.id not in pool:
            pool[entry.id] = (entry, BM25_SEMANTIC_FLOOR)
            bm25_only_ids.add(entry.id)

    # =================================================================
    # 3. Query classification + category-forced retrieval
    # =================================================================
    predicted_cat = await classify_query_gpt(query, openai_client)

    cat_entries = (bank.get_by_category_all(predicted_cat) if _search_all
                   else bank.get_by_category(predicted_cat))
    cat_additions = []
    for entry in cat_entries:
        if entry.id in pool:
            continue
        e_norm = entry.embedding / (np.linalg.norm(entry.embedding) + 1e-12)
        sim = float(np.dot(e_norm, q_norm))
        cat_additions.append((entry, sim))
    cat_additions.sort(key=lambda x: x[1], reverse=True)
    cat_only_ids: set[str] = set()
    for entry, sim in cat_additions[:20]:
        score = max(sim, CATEGORY_FORCED_FLOOR)
        pool[entry.id] = (entry, score)
        cat_only_ids.add(entry.id)

    # =================================================================
    # 3b. Multi-hop entity expansion
    # =================================================================
    hop2_ids: set[str] = set()
    if multihop and len(pool) >= 5:
        # Take top-5 entries by semantic score
        top5_by_sem = sorted(pool.items(),
                             key=lambda x: x[1][1], reverse=True)[:5]
        # Extract entities from their text
        all_ents: list[str] = []
        for _eid, (entry, _sim) in top5_by_sem:
            all_ents.extend(_extract_entities_regex(entry.text))
        # Deduplicate (case-insensitive, preserve first casing)
        seen_ent: set[str] = set()
        unique_ents: list[str] = []
        for e in all_ents:
            key = e.lower()
            if key not in seen_ent:
                seen_ent.add(key)
                unique_ents.append(e)
        if unique_ents:
            ent_embs = await embed_texts(unique_ents, openai_client)
            for ent_emb in ent_embs:
                _hop_search = (bank.cosine_search_all if _search_all
                               else bank.cosine_search)
                for entry, _sim in _hop_search(ent_emb, k=5):
                    if entry.id not in pool:
                        # Score against the QUERY for fair blending
                        e_norm = entry.embedding / (
                            np.linalg.norm(entry.embedding) + 1e-12)
                        query_sim = float(np.dot(e_norm, q_norm))
                        pool[entry.id] = (
                            entry, max(query_sim, MULTIHOP_SEMANTIC_FLOOR))
                        hop2_ids.add(entry.id)

    # =================================================================
    # 4. Memory distillation (LLM selects top-20 from merged pool)
    # =================================================================
    if skip_distill:
        if len(pool) > 20:
            top20 = sorted(pool.items(), key=lambda x: x[1][1],
                           reverse=True)[:20]
            pool = dict(top20)
    else:
        pool = await _distill_candidates(query, pool, openai_client)

    # =================================================================
    # 5. Lifecycle filtering (applied AFTER distillation)
    #    Skipped entirely when no_lifecycle=True.
    # =================================================================
    if no_lifecycle:
        filtered = dict(pool)
    else:
        backward = _is_backward_looking(query) or temporal_query
        retraction_q = _is_retraction_query(query)
        expiry_cutoff = t_now - timedelta(days=14)

        filtered: dict[str, tuple[LifecycleEntry, float]] = {}
        for eid, (entry, sim) in pool.items():
            # 5a. Active check — relaxed when include_inactive for KU queries
            if not entry.is_active and not include_inactive:
                continue

            if not backward:
                # 5b. Expiry filter — skip expired events, unless numeric
                if (entry.event_time is not None
                        and entry.event_time < expiry_cutoff
                        and not entry.numeric_value):
                    continue

                # 5c. Retraction filter
                if entry.is_retracted and not retraction_q:
                    continue

            filtered[eid] = (entry, sim)

        # 5d. Supersession: for entries sharing slot_key, keep only newest
        if not backward:
            slot_groups: dict[tuple, list[str]] = {}
            for eid, (entry, _) in filtered.items():
                if entry.slot_key:
                    slot_groups.setdefault(entry.slot_key, []).append(eid)
            superseded_ids: set[str] = set()
            for _, eids in slot_groups.items():
                if len(eids) < 2:
                    continue
                eids.sort(key=lambda x: filtered[x][0].created_at,
                          reverse=True)
                for old_eid in eids[1:]:
                    superseded_ids.add(old_eid)
            for eid in superseded_ids:
                filtered.pop(eid, None)

    # =================================================================
    # 6. Per-entry scoring
    #    When no_lifecycle: activation=1.0, blended=semantic (alpha=0).
    # =================================================================
    scored: list[tuple[Candidate, float, float, float]] = []
    for eid, (entry, semantic) in filtered.items():
        if no_lifecycle:
            activation = 1.0
            blended = semantic
        else:
            # 6a. Effective decay rate — weighted harmonic mean of lambda
            w_sum = 0.0
            w_over_lambda = 0.0
            for cat, w in entry.category_weights.items():
                if w <= 0 or cat not in DECAY_LAMBDA:
                    continue
                lam = DECAY_LAMBDA[cat]
                w_sum += w
                w_over_lambda += w / lam
            lambda_eff = (w_sum / w_over_lambda
                          if w_over_lambda > 0
                          else DECAY_LAMBDA.get("OTHER", 0.005))

            # 6b. Base activation from time since creation
            delta_hours = max(
                0.0,
                (t_now - entry.created_at).total_seconds() / 3600.0)
            activation = math.exp(-lambda_eff * delta_hours)

            # 6c. Anticipatory activation for future events — use max
            if entry.event_time is not None and entry.event_time > t_now:
                hours_until = (
                    (entry.event_time - t_now).total_seconds() / 3600.0)
                anticipatory = math.exp(-lambda_eff * hours_until)
                activation = max(activation, anticipatory)

            # 6d. Blending
            alpha = BLEND_ALPHA.get(entry.category, 0.20)
            blended = alpha * activation + (1.0 - alpha) * semantic

            # 6e. Semantic floor
            if semantic >= 0.85:
                floor = SEMANTIC_FLOOR.get(entry.category, 0.0)
                blended = max(blended, floor)

            # 6f. Numeric preservation floor
            if entry.numeric_value and semantic >= 0.85:
                blended = max(blended, 0.95 * semantic)

        # Track source
        source_tag = "fr_bank"
        if eid in hop2_ids:
            source_tag = "fr_bank_hop2"
        elif eid in bm25_only_ids:
            source_tag = "fr_bank_bm25"
        elif eid in cat_only_ids:
            source_tag = "fr_bank_cat"

        cand = Candidate(
            uuid=entry.id,
            fact=entry.text,
            source=source_tag,
            graphiti_score=semantic,
        )
        scored.append((cand, activation, semantic, blended))

    # =================================================================
    # 7. Sort by blended descending, then semantic descending
    # =================================================================
    scored.sort(key=lambda x: (-x[3], -x[2]))
    return scored[:limit]
