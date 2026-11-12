"""Shortest walking routes across campus (Dijkstra).

Distances are in meters. Walking time uses a fixed average speed; it is an
estimate shown to students, not a guarantee.
"""

from __future__ import annotations

import heapq
import itertools
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from .campus import Campus, Edge

WALKING_SPEED_M_PER_MIN = 80  # about 4.8 km/h


class NoRouteError(LookupError):
    """No path exists between the two places under the given options."""


@dataclass
class Route:
    start: str
    goal: str
    path: List[str]
    legs: List[Edge] = field(default_factory=list)

    @property
    def meters(self) -> int:
        return sum(edge.meters for edge in self.legs)

    @property
    def minutes(self) -> int:
        if self.meters == 0:
            return 0
        return max(1, math.ceil(self.meters / WALKING_SPEED_M_PER_MIN))

    @property
    def has_stairs(self) -> bool:
        return any(edge.stairs for edge in self.legs)

    def to_dict(self, campus: Campus) -> dict:
        return {
            "start": self.start,
            "goal": self.goal,
            "path": self.path,
            "names": [campus.places[p].name for p in self.path],
            "meters": self.meters,
            "minutes": self.minutes,
            "has_stairs": self.has_stairs,
            "steps": describe(self, campus),
        }


def _dijkstra(campus: Campus, start: str, goal: str, avoid_stairs: bool):
    dist: Dict[str, int] = {start: 0}
    came_by: Dict[str, Edge] = {}
    order = itertools.count()  # tie-breaker: keeps the heap deterministic
    heap = [(0, next(order), start)]
    done = set()
    while heap:
        cost, _, here = heapq.heappop(heap)
        if here in done:
            continue
        done.add(here)
        if here == goal:
            break
        for edge in campus.neighbors(here, avoid_stairs=avoid_stairs):
            there = edge.other(here)
            new_cost = cost + edge.meters
            if new_cost < dist.get(there, math.inf):
                dist[there] = new_cost
                came_by[there] = edge
                heapq.heappush(heap, (new_cost, next(order), there))
    if goal not in done:
        return None
    path, legs = [goal], []
    while path[-1] != start:
        edge = came_by[path[-1]]
        legs.append(edge)
        path.append(edge.other(path[-1]))
    path.reverse()
    legs.reverse()
    return path, legs


def shortest_route(campus: Campus, start: str, goal: str,
                   avoid_stairs: bool = False,
                   via: Optional[Sequence[str]] = None) -> Route:
    """Shortest route from ``start`` to ``goal`` (place ids).

    ``via`` is an optional ordered list of place ids to pass through.
    Raises NoRouteError if any segment is unreachable.
    """
    stops = [start] + list(via or []) + [goal]
    for stop in stops:
        campus.place(stop)  # raises UnknownPlaceError for bad ids
    path: List[str] = [start]
    legs: List[Edge] = []
    for a, b in zip(stops, stops[1:]):
        if a == b:
            continue
        found = _dijkstra(campus, a, b, avoid_stairs)
        if found is None:
            how = " without stairs" if avoid_stairs else ""
            raise NoRouteError("no route from %s to %s%s" % (
                campus.places[a].name, campus.places[b].name, how))
        seg_path, seg_legs = found
        path.extend(seg_path[1:])
        legs.extend(seg_legs)
    return Route(start, goal, path, legs)


def describe(route: Route, campus: Campus) -> List[str]:
    """Human-readable walking directions, one line per leg."""
    if not route.legs:
        return ["You are already at %s." % campus.places[route.start].name]
    lines = []
    here = route.path[0]
    for edge in route.legs:
        there = edge.other(here)
        notes = []
        if edge.stairs:
            notes.append("stairs")
        if edge.covered:
            notes.append("covered")
        suffix = " (%s)" % ", ".join(notes) if notes else ""
        lines.append("Walk %d m from %s to %s%s." % (
            edge.meters, campus.places[here].name, campus.places[there].name, suffix))
        here = there
    return lines
