import unittest
from datetime import datetime, timedelta

from campusroute.occupancy import Report, crowd_level, crowd_score, parse_report

NOW = datetime(2027, 3, 1, 12, 30)


def ago(minutes, level, place="caf"):
    return Report(place, level, NOW - timedelta(minutes=minutes))


class CrowdTest(unittest.TestCase):
    def test_no_reports(self):
        self.assertIsNone(crowd_level([], "caf", NOW))

    def test_recent_report_dominates(self):
        reports = [ago(0, 4), ago(27, 0)]
        self.assertEqual(crowd_level(reports, "caf", NOW), "packed")

    def test_old_and_future_reports_ignored(self):
        reports = [ago(30, 4), ago(-5, 4), ago(10, 1)]
        self.assertEqual(crowd_level(reports, "caf", NOW), "quiet")

    def test_other_places_ignored(self):
        self.assertIsNone(crowd_level([ago(1, 3, place="lib")], "caf", NOW))

    def test_half_rounds_up(self):
        reports = [ago(0, 1), ago(0, 2)]
        self.assertAlmostEqual(crowd_score(reports, "caf", NOW), 1.5)
        self.assertEqual(crowd_level(reports, "caf", NOW), "moderate")

    def test_parse_report_validates_level(self):
        with self.assertRaises(ValueError):
            parse_report({"place": "caf", "level": 7, "at": "2027-03-01T12:00:00"})


if __name__ == "__main__":
    unittest.main()
