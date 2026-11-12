"""Opening hours for CampusRoute places (backlog CR-11).

Implement is_open(). Read README.md for the rules. Standard library only.
"""

from datetime import datetime


def is_open(hours: str, now: datetime) -> bool:
    """True if a place with this ``hours`` string is open at ``now``.

    >>> is_open("Mon-Fri 08:00-17:00", datetime(2027, 3, 1, 9, 0))   # a Monday
    True
    """
    raise NotImplementedError("your code here")
