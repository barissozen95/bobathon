"""Campus data model: places, walkways (edges) and rooms.

The campus is loaded from a JSON file (see data/campus.json) and validated
before use. Everything downstream (search, routing, API) works on a
``Campus`` object and never touches the raw JSON.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data" / "campus.json"


class CampusDataError(ValueError):
    """The campus file is malformed or internally inconsistent."""


class UnknownPlaceError(LookupError):
    """A place, room or alias could not be resolved."""

    def __init__(self, query: str, suggestions: Optional[List[str]] = None):
        self.query = query
        self.suggestions = suggestions or []
        msg = "unknown place '%s'" % query
        if self.suggestions:
            msg += " (did you mean: %s?)" % ", ".join(self.suggestions)
        super().__init__(msg)


@dataclass(frozen=True)
class Place:
    id: str
    name: str
    kind: str
    x: int
    y: int
    aliases: tuple = ()
    hours: Optional[str] = None


@dataclass(frozen=True)
class Edge:
    a: str
    b: str
    meters: int
    stairs: bool = False
    covered: bool = False

    def other(self, place_id: str) -> str:
        return self.b if place_id == self.a else self.a


@dataclass(frozen=True)
class Room:
    code: str
    place: str
    floor: int
    label: str


@dataclass
class Campus:
    name: str
    places: Dict[str, Place] = field(default_factory=dict)
    rooms: Dict[str, Room] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)
    _adjacency: Dict[str, List[Edge]] = field(default_factory=dict, repr=False)

    def place(self, place_id: str) -> Place:
        try:
            return self.places[place_id]
        except KeyError:
            raise UnknownPlaceError(place_id) from None

    def neighbors(self, place_id: str, avoid_stairs: bool = False) -> List[Edge]:
        edges = self._adjacency.get(place_id, [])
        if avoid_stairs:
            return [e for e in edges if not e.stairs]
        return list(edges)

    def resolve(self, query: str) -> Place:
        """Resolve a place id, room code, exact name or alias to a Place.

        Matching is case-insensitive and accent-insensitive. Fuzzy matches
        are NOT accepted here; they are only offered as suggestions.
        """
        from .search import normalize, search  # local import avoids a cycle

        key = normalize(query)
        if not key:
            raise UnknownPlaceError(query)
        for room in self.rooms.values():
            if normalize(room.code) == key:
                return self.places[room.place]
        for place in self.places.values():
            if key == normalize(place.id) or key == normalize(place.name):
                return place
            if any(key == normalize(alias) for alias in place.aliases):
                return place
        suggestions = [hit.label for hit in search(self, query, limit=3)]
        raise UnknownPlaceError(query, suggestions)


def _require(cond: bool, message: str) -> None:
    if not cond:
        raise CampusDataError(message)


def campus_from_dict(data: dict) -> Campus:
    _require(isinstance(data, dict), "campus file must contain a JSON object")
    campus = Campus(name=str(data.get("campus", "Campus")))

    for raw in data.get("places", []):
        pid = raw.get("id")
        _require(isinstance(pid, str) and pid, "place without id")
        _require(pid not in campus.places, "duplicate place id '%s'" % pid)
        campus.places[pid] = Place(
            id=pid,
            name=str(raw["name"]),
            kind=str(raw.get("kind", "other")),
            x=int(raw.get("x", 0)),
            y=int(raw.get("y", 0)),
            aliases=tuple(raw.get("aliases", [])),
            hours=raw.get("hours"),
        )
    _require(bool(campus.places), "campus has no places")

    campus._adjacency = {pid: [] for pid in campus.places}
    for raw in data.get("edges", []):
        a, b = raw.get("a"), raw.get("b")
        _require(a in campus.places, "edge refers to unknown place '%s'" % a)
        _require(b in campus.places, "edge refers to unknown place '%s'" % b)
        _require(a != b, "edge from '%s' to itself" % a)
        meters = raw.get("meters")
        _require(isinstance(meters, int) and meters > 0,
                 "edge %s-%s must have a positive integer length" % (a, b))
        edge = Edge(a, b, meters, bool(raw.get("stairs")), bool(raw.get("covered")))
        campus.edges.append(edge)
        campus._adjacency[a].append(edge)
        campus._adjacency[b].append(edge)

    for raw in data.get("rooms", []):
        code = str(raw.get("code", "")).upper()
        _require(bool(code), "room without code")
        _require(code not in campus.rooms, "duplicate room code '%s'" % code)
        _require(raw.get("place") in campus.places,
                 "room %s refers to unknown place '%s'" % (code, raw.get("place")))
        campus.rooms[code] = Room(code, raw["place"], int(raw.get("floor", 0)),
                                  str(raw.get("label", code)))
    return campus


def load_campus(path: Optional[Path] = None) -> Campus:
    """Load and validate a campus file. Defaults to data/campus.json."""
    path = Path(path) if path else DEFAULT_DATA
    with open(path, encoding="utf-8") as fh:
        try:
            data = json.load(fh)
        except json.JSONDecodeError as exc:
            raise CampusDataError("%s: invalid JSON (%s)" % (path.name, exc)) from None
    return campus_from_dict(data)
