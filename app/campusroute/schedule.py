"""Weekly course schedule: parsing, conflicts and "what is my next class?".

A schedule is a small CSV file a student types in by hand:

    day,start,end,course,room
    Mon,09:00,10:50,CS201 Data Structures,ENG-B204

Days are Monday=0 ... Sunday=6, like ``datetime.weekday()``.
This module is pure: it never reads the clock. Callers pass ``now``.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import Dict, Iterable, List, Optional, Tuple

DAY_NAMES = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
_DAY_ALIASES = {
    "mon": 0, "monday": 0, "tue": 1, "tues": 1, "tuesday": 1,
    "wed": 2, "wednesday": 2, "thu": 3, "thur": 3, "thurs": 3, "thursday": 3,
    "fri": 4, "friday": 4, "sat": 5, "saturday": 5, "sun": 6, "sunday": 6,
}
REQUIRED_COLUMNS = ("day", "start", "end", "course", "room")


class ScheduleError(ValueError):
    """A schedule line could not be parsed or is inconsistent."""


@dataclass(frozen=True)
class Session:
    course: str
    day: int
    start: time
    end: time
    room: str

    @property
    def minutes(self) -> int:
        return (self.end.hour * 60 + self.end.minute) - (self.start.hour * 60 + self.start.minute)

    def overlaps(self, other: "Session") -> bool:
        return self.day == other.day and self.start < other.end and other.start < self.end


def parse_time(text: str) -> time:
    """Parse strict 24-hour 'HH:MM' (e.g. '09:05'). '9:05' is also accepted."""
    parts = (text or "").strip().split(":")
    # isascii() matters: str.isdigit() is also True for "²" or "٣", which int() rejects
    if len(parts) != 2 or not all(p.isascii() and p.isdigit() for p in parts) or len(parts[1]) != 2:
        raise ScheduleError("invalid time '%s' (expected HH:MM)" % text)
    hour, minute = int(parts[0]), int(parts[1])
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ScheduleError("invalid time '%s' (out of range)" % text)
    return time(hour, minute)


def parse_day(text: str) -> int:
    key = (text or "").strip().lower()
    if key not in _DAY_ALIASES:
        raise ScheduleError("invalid day '%s'" % text)
    return _DAY_ALIASES[key]


def parse_schedule(lines: Iterable[str]) -> List[Session]:
    """Parse CSV lines into sessions sorted by (day, start, course).

    Blank lines and lines starting with '#' are ignored. Errors mention the
    1-based line number of the offending row.
    """
    numbered = [(n, line) for n, line in enumerate(lines, start=1)
                if line.strip() and not line.lstrip().startswith("#")]
    if not numbered:
        return []
    reader = csv.reader([line for _, line in numbered])
    header = [h.strip().lower() for h in next(reader)]
    missing = [c for c in REQUIRED_COLUMNS if c not in header]
    if missing:
        raise ScheduleError("missing column(s): %s" % ", ".join(missing))
    sessions = []
    for (line_no, _), row in zip(numbered[1:], reader):
        if len(row) != len(header):
            raise ScheduleError("line %d: expected %d fields, got %d"
                                % (line_no, len(header), len(row)))
        rec = {h: v.strip() for h, v in zip(header, row)}
        try:
            session = Session(
                course=rec["course"],
                day=parse_day(rec["day"]),
                start=parse_time(rec["start"]),
                end=parse_time(rec["end"]),
                room=rec["room"].upper(),
            )
        except ScheduleError as exc:
            raise ScheduleError("line %d: %s" % (line_no, exc)) from None
        if not session.course:
            raise ScheduleError("line %d: course is empty" % line_no)
        if session.end <= session.start:
            raise ScheduleError("line %d: end time must be after start time" % line_no)
        sessions.append(session)
    sessions.sort(key=lambda s: (s.day, s.start, s.course))
    return sessions


def load_schedule(path) -> List[Session]:
    with open(path, encoding="utf-8", newline="") as fh:
        return parse_schedule(fh.read().splitlines())


def find_conflicts(sessions: List[Session]) -> List[Tuple[Session, Session]]:
    """All overlapping pairs, in schedule order."""
    ordered = sorted(sessions, key=lambda s: (s.day, s.start, s.course))
    clashes = []
    for i, first in enumerate(ordered):
        for second in ordered[i + 1:]:
            if second.day != first.day or second.start >= first.end:
                break
            clashes.append((first, second))
    return clashes


def _occurrence_after(session: Session, now: datetime) -> datetime:
    """The first start of ``session`` strictly after ``now`` (wraps weekly)."""
    days_ahead = (session.day - now.weekday()) % 7
    candidate = datetime.combine(now.date() + timedelta(days=days_ahead), session.start)
    if candidate <= now:
        candidate += timedelta(days=7)
    return candidate


def current_session(sessions: List[Session], now: datetime) -> Optional[Session]:
    for s in sessions:
        if s.day == now.weekday() and s.start <= now.time() < s.end:
            return s
    return None


def next_session(sessions: List[Session], now: datetime) -> Optional[Tuple[Session, datetime]]:
    """The next session that starts after ``now``, with its start datetime.

    Ties (two sessions starting at the same moment) go to the one that comes
    first in schedule order. Returns None for an empty schedule.
    """
    best = None
    for s in sessions:
        when = _occurrence_after(s, now)
        if best is None or when < best[1]:
            best = (s, when)
    return best


def minutes_until(now: datetime, then: datetime) -> int:
    """Whole minutes from now until then, rounded UP. Never negative."""
    seconds = int((then - now).total_seconds())
    if seconds <= 0:
        return 0
    return (seconds + 59) // 60


def weekly_minutes(sessions: List[Session]) -> Dict[str, int]:
    """Total scheduled minutes per course, in order of first appearance."""
    totals: Dict[str, int] = {}
    for s in sessions:
        totals[s.course] = totals.get(s.course, 0) + s.minutes
    return totals


def format_session(s: Session) -> str:
    return "%s %s-%s %s @ %s" % (DAY_NAMES[s.day], s.start.strftime("%H:%M"),
                                 s.end.strftime("%H:%M"), s.course, s.room)
