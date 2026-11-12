import json
import unittest
from datetime import datetime
from pathlib import Path

from opening_hours import is_open


def at(day, hh, mm=0):
    """1 March 2027 is a Monday, so at(1, ...) is Monday and at(6, ...) is Saturday."""
    return datetime(2027, 3, day, hh, mm)


class BasicTest(unittest.TestCase):
    def test_open_during_hours(self):
        self.assertTrue(is_open("Mon-Fri 08:00-17:00", at(1, 9)))

    def test_closed_before_opening(self):
        self.assertFalse(is_open("Mon-Fri 08:00-17:00", at(1, 7, 59)))

    def test_start_inclusive_end_exclusive(self):
        self.assertTrue(is_open("Mon-Fri 08:00-17:00", at(1, 8, 0)))
        self.assertFalse(is_open("Mon-Fri 08:00-17:00", at(1, 17, 0)))

    def test_unlisted_day_is_closed(self):
        self.assertFalse(is_open("Mon-Fri 08:00-17:00", at(6, 10)))

    def test_multiple_segments(self):
        hours = "Mon-Fri 08:00-17:00; Sat 10:00-14:00"
        self.assertTrue(is_open(hours, at(6, 13, 59)))
        self.assertFalse(is_open(hours, at(7, 12)))  # Sunday

    def test_spaces_and_case(self):
        self.assertTrue(is_open("  mon-FRI   08:00-17:00 ;  sat 10:00-12:00 ", at(6, 11)))


class EdgeCaseTest(unittest.TestCase):
    def test_24_00_means_end_of_day(self):
        self.assertTrue(is_open("Mon 08:00-24:00", at(1, 23, 59)))
        self.assertFalse(is_open("Mon 08:00-24:00", at(2, 0, 0)))

    def test_always_open(self):
        self.assertTrue(is_open("Mon-Sun 00:00-24:00", at(7, 3)))

    def test_overnight_interval(self):
        hours = "Fri 20:00-02:00"
        self.assertTrue(is_open(hours, at(5, 23)))       # Friday night
        self.assertTrue(is_open(hours, at(6, 1, 30)))    # early Saturday
        self.assertFalse(is_open(hours, at(6, 2, 0)))
        self.assertFalse(is_open(hours, at(5, 19, 59)))

    def test_closed_overrides_earlier_segment(self):
        hours = "Mon-Fri 08:00-17:00; Wed closed"
        self.assertFalse(is_open(hours, at(3, 10)))      # Wednesday
        self.assertTrue(is_open(hours, at(4, 10)))       # Thursday


class ErrorTest(unittest.TestCase):
    def test_unknown_day(self):
        with self.assertRaises(ValueError):
            is_open("Pzt 08:00-17:00", at(1, 9))

    def test_invalid_times(self):
        for bad in ("Mon 25:00-26:00", "Mon 8-17", "Mon 09:00-09:00", "Mon 24:00-02:00"):
            with self.assertRaises(ValueError, msg=bad):
                is_open(bad, at(1, 9))

    def test_backwards_range_and_empty(self):
        for bad in ("Sat-Mon 10:00-12:00", "", "Mon"):
            with self.assertRaises(ValueError, msg=repr(bad)):
                is_open(bad, at(1, 9))


class RealDataTest(unittest.TestCase):
    def test_every_hours_string_in_campus_json_parses(self):
        campus = Path(__file__).resolve().parents[3] / "app" / "data" / "campus.json"
        places = json.loads(campus.read_text(encoding="utf-8"))["places"]
        monday_noon = at(1, 12)
        library = next(p for p in places if p["id"] == "lib")
        for place in places:
            if place["hours"]:
                is_open(place["hours"], monday_noon)  # must not raise
        self.assertTrue(is_open(library["hours"], at(1, 23, 30)))
        self.assertFalse(is_open(library["hours"], at(6, 19)))


if __name__ == "__main__":
    unittest.main()
