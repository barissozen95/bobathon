"""Crowd levels from student reports ("how busy is the cafe right now?").

Students tap one of five levels. A place's current level is the
recency-weighted average of reports from the last ``window`` minutes:
a report made just now counts fully, one made ``window`` minutes ago counts
nothing. Reports from the future (clock skew) are ignored.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional

LEVELS = ("empty", "quiet", "moderate", "busy", "packed")
DEFAULT_WINDOW_MIN = 30


@dataclass(frozen=True)
class Report:
    place: str
    level: int
    at: datetime


def parse_report(raw: dict) -> Report:
    level = raw.get("level")
    if not isinstance(level, int) or not 0 <= level < len(LEVELS):
        raise ValueError("level must be an integer 0-%d" % (len(LEVELS) - 1))
    return Report(str(raw["place"]), level, datetime.fromisoformat(raw["at"]))


def crowd_score(reports: Iterable[Report], place: str, now: datetime,
                window_min: int = DEFAULT_WINDOW_MIN) -> Optional[float]:
    total = weight_sum = 0.0
    for r in reports:
        if r.place != place:
            continue
        age_min = (now - r.at).total_seconds() / 60
        if age_min < 0 or age_min >= window_min:
            continue
        weight = 1 - age_min / window_min
        total += weight * r.level
        weight_sum += weight
    if weight_sum == 0:
        return None
    return total / weight_sum


def crowd_level(reports: Iterable[Report], place: str, now: datetime,
                window_min: int = DEFAULT_WINDOW_MIN) -> Optional[str]:
    """Label such as 'busy', or None when there are no recent reports."""
    score = crowd_score(reports, place, now, window_min)
    if score is None:
        return None
    return LEVELS[int(score + 0.5)]  # round half up, not Python's banker's rounding
