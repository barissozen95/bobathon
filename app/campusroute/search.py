"""Free-text search over places and rooms.

Students type things like "kutuphane", "eng b", "B204" or "cinar cafe".
Search is case-insensitive, accent-insensitive and Turkish-aware
("I", "ı", "İ" and "i" all fold to "i").
"""

from __future__ import annotations

import difflib
import unicodedata
from dataclasses import dataclass
from typing import List

_TURKISH_FOLD = str.maketrans({"ı": "i", "İ": "i", "I": "i"})


def normalize(text: str) -> str:
    """Fold text for comparison: lower-case, no accents, single spaces."""
    text = (text or "").translate(_TURKISH_FOLD).casefold()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("-", " ").replace("_", " ")
    return " ".join(text.split())


@dataclass(frozen=True)
class Hit:
    score: int
    kind: str        # "room" or "place"
    id: str          # room code or place id
    label: str       # what we show to the user
    place_id: str    # where to route to


def _score(query: str, candidate: str) -> int:
    if not candidate:
        return 0
    if query == candidate:
        return 100
    if candidate.startswith(query):
        return 80
    if query in candidate:
        return 60
    q_tokens, c_tokens = set(query.split()), set(candidate.split())
    if q_tokens and q_tokens <= c_tokens:
        return 50
    ratio = difflib.SequenceMatcher(None, query, candidate).ratio()
    return int(ratio * 50) if ratio >= 0.75 else 0


def search(campus, query: str, limit: int = 5) -> List[Hit]:
    """Return up to ``limit`` hits, best first. Ties are sorted by label."""
    q = normalize(query)
    if not q:
        return []
    hits = []
    for place in campus.places.values():
        if place.kind == "junction" and not place.aliases:
            continue  # unnamed path junctions are not useful search results
        names = [place.name, place.id] + list(place.aliases)
        best = max(_score(q, normalize(n)) for n in names)
        if best:
            hits.append(Hit(best, "place", place.id, place.name, place.id))
    for room in campus.rooms.values():
        best = max(_score(q, normalize(room.code)), _score(q, normalize(room.label)))
        if best:
            building = campus.places[room.place].name
            label = "%s - %s (%s, floor %d)" % (room.code, room.label, building, room.floor)
            hits.append(Hit(best, "room", room.code, label, room.place))
    hits.sort(key=lambda h: (-h.score, h.label))
    return hits[:limit]
