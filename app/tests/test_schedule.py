import unittest
from datetime import datetime, time

from campusroute.schedule import (ScheduleError, Session, find_conflicts, format_session,
                                  minutes_until, next_session, parse_schedule, parse_time,
                                  weekly_minutes)

SAMPLE = """\
day,start,end,course,room
Mon,09:00,10:50,CS201,eng-b204
Wed,09:00,10:50,CS201,ENG-B204
Mon,13:00,14:50,MATH203,SCI-202
Fri,14:00,15:50,HUM101,INO-AUD
""".splitlines()

MONDAY = datetime(2027, 3, 1)  # 1 March 2027 is a Monday


class ParseTest(unittest.TestCase):
    def test_sorted_by_day_then_time(self):
        s = parse_schedule(SAMPLE)
        self.assertEqual([(x.course, x.day) for x in s],
                         [("CS201", 0), ("MATH203", 0), ("CS201", 2), ("HUM101", 4)])

    def test_room_upper_cased(self):
        self.assertEqual(parse_schedule(SAMPLE)[0].room, "ENG-B204")

    def test_comments_and_blank_lines(self):
        lines = ["# my schedule", "", SAMPLE[0], "  ", SAMPLE[1]]
        self.assertEqual(len(parse_schedule(lines)), 1)

    def test_parse_time(self):
        self.assertEqual(parse_time("9:05"), time(9, 5))
        for bad in ("24:00", "09:5", "9h05", "", "12:60", "1²:00", "-1:00"):
            with self.assertRaises(ScheduleError, msg=bad):
                parse_time(bad)

    def test_error_reports_real_line_number(self):
        lines = ["# comment", SAMPLE[0], "Mon,10:00,09:00,X,R"]
        with self.assertRaisesRegex(ScheduleError, "^line 3: end time"):
            parse_schedule(lines)

    def test_bad_day(self):
        with self.assertRaisesRegex(ScheduleError, "line 2: invalid day 'Pzt'"):
            parse_schedule([SAMPLE[0], "Pzt,09:00,10:00,X,R"])

    def test_missing_column(self):
        with self.assertRaisesRegex(ScheduleError, "missing column"):
            parse_schedule(["day,start,end,course", "Mon,09:00,10:00,X"])

    def test_wrong_field_count(self):
        with self.assertRaisesRegex(ScheduleError, "expected 5 fields, got 4"):
            parse_schedule([SAMPLE[0], "Mon,09:00,10:00,X"])

    def test_quoted_course_with_comma(self):
        s = parse_schedule([SAMPLE[0], 'Tue,10:00,11:50,"CS203 Computer Organization, Section 2",ENG-A101'])
        self.assertEqual(s[0].course, "CS203 Computer Organization, Section 2")

    def test_day_names_case_insensitive(self):
        s = parse_schedule([SAMPLE[0], "THURSDAY,11:00,12:50,PHYS102,SCI-110"])
        self.assertEqual(s[0].day, 3)

    def test_empty(self):
        self.assertEqual(parse_schedule([]), [])


class NextSessionTest(unittest.TestCase):
    def setUp(self):
        self.s = parse_schedule(SAMPLE)

    def test_later_same_day(self):
        session, when = next_session(self.s, MONDAY.replace(hour=9, minute=30))
        self.assertEqual((session.course, when), ("MATH203", MONDAY.replace(hour=13)))

    def test_exact_start_time_is_not_next(self):
        session, _ = next_session(self.s, MONDAY.replace(hour=13))
        self.assertEqual(session.course, "CS201")  # Wednesday

    def test_wraps_to_next_week(self):
        saturday = datetime(2027, 3, 6, 12, 0)
        session, when = next_session(self.s, saturday)
        self.assertEqual(when, datetime(2027, 3, 8, 9, 0))

    def test_empty_schedule(self):
        self.assertIsNone(next_session([], MONDAY))

    def test_minutes_until_rounds_up(self):
        self.assertEqual(minutes_until(MONDAY, MONDAY.replace(second=1)), 1)
        self.assertEqual(minutes_until(MONDAY, MONDAY.replace(minute=2)), 2)
        self.assertEqual(minutes_until(MONDAY.replace(minute=5), MONDAY), 0)


class ReportsTest(unittest.TestCase):
    def test_conflicts(self):
        s = parse_schedule(SAMPLE + ["Mon,10:00,11:00,LAB,ENG-A214"])
        pairs = [(a.course, b.course) for a, b in find_conflicts(s)]
        self.assertEqual(pairs, [("CS201", "LAB")])

    def test_back_to_back_is_not_conflict(self):
        s = parse_schedule(SAMPLE + ["Mon,10:50,11:30,LAB,ENG-A214"])
        self.assertEqual(find_conflicts(s), [])

    def test_weekly_minutes_keeps_first_appearance_order(self):
        self.assertEqual(list(weekly_minutes(parse_schedule(SAMPLE)).items()),
                         [("CS201", 220), ("MATH203", 110), ("HUM101", 110)])

    def test_format(self):
        s = Session("CS201", 2, time(9, 0), time(10, 50), "ENG-B204")
        self.assertEqual(format_session(s), "Wed 09:00-10:50 CS201 @ ENG-B204")


if __name__ == "__main__":
    unittest.main()
