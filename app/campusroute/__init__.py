"""CampusRoute: find rooms, walk the shortest route, never be late for class."""

__version__ = "1.4.0"

from .campus import Campus, CampusDataError, UnknownPlaceError, load_campus  # noqa: E402,F401
