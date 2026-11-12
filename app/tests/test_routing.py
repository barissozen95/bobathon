import unittest

from campusroute.campus import UnknownPlaceError, campus_from_dict, load_campus
from campusroute.routing import NoRouteError, describe, shortest_route


class RoutingTest(unittest.TestCase):
    def setUp(self):
        self.campus = load_campus()

    def test_gate_to_eng_b(self):
        r = shortest_route(self.campus, "gate-main", "eng-b")
        self.assertEqual(r.path, ["gate-main", "inonu", "quad", "eng-a", "eng-b"])
        self.assertEqual(r.meters, 790)
        self.assertEqual(r.minutes, 10)

    def test_same_place(self):
        r = shortest_route(self.campus, "lib", "lib")
        self.assertEqual((r.path, r.meters, r.minutes), (["lib"], 0, 0))
        self.assertEqual(describe(r, self.campus), ["You are already at Central Library."])

    def test_stairs_shortcut_used_by_default(self):
        r = shortest_route(self.campus, "sci", "eng-b")
        self.assertEqual(r.path, ["sci", "j-east", "eng-b"])
        self.assertTrue(r.has_stairs)

    def test_avoid_stairs_takes_longer_step_free_route(self):
        r = shortest_route(self.campus, "sci", "eng-b", avoid_stairs=True)
        self.assertFalse(r.has_stairs)
        self.assertEqual(r.path, ["sci", "quad", "eng-a", "eng-b"])
        self.assertEqual(r.meters, 540)

    def test_route_is_symmetric_in_length(self):
        there = shortest_route(self.campus, "dorm", "sport")
        back = shortest_route(self.campus, "sport", "dorm")
        self.assertEqual(there.meters, back.meters)

    def test_via(self):
        r = shortest_route(self.campus, "gate-main", "eng-a", via=["caf"])
        self.assertIn("caf", r.path)
        self.assertEqual(r.path[0], "gate-main")
        self.assertEqual(r.path[-1], "eng-a")

    def test_unknown_id(self):
        with self.assertRaises(UnknownPlaceError):
            shortest_route(self.campus, "gate-main", "mars")

    def test_unreachable(self):
        island = campus_from_dict({"places": [{"id": "a", "name": "A"}, {"id": "b", "name": "B"}]})
        with self.assertRaises(NoRouteError):
            shortest_route(island, "a", "b")

    def test_describe_marks_covered_and_stairs(self):
        r = shortest_route(self.campus, "sci", "eng-b")
        lines = describe(r, self.campus)
        self.assertEqual(lines[-1], "Walk 120 m from East Stairs to Engineering Building B (stairs).")


if __name__ == "__main__":
    unittest.main()
