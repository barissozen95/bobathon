import unittest

from campusroute.campus import CampusDataError, UnknownPlaceError, campus_from_dict, load_campus


class LoadCampusTest(unittest.TestCase):
    def setUp(self):
        self.campus = load_campus()

    def test_sample_campus_loads(self):
        self.assertIn("lib", self.campus.places)
        self.assertGreaterEqual(len(self.campus.edges), 20)

    def test_resolve_room_code_case_insensitive(self):
        self.assertEqual(self.campus.resolve("eng-b204").id, "eng-b")

    def test_resolve_turkish_name_without_accents(self):
        self.assertEqual(self.campus.resolve("inonu auditorium").id, "inonu")
        self.assertEqual(self.campus.resolve("ÇINAR CAFÉ").id, "caf")

    def test_resolve_alias(self):
        self.assertEqual(self.campus.resolve("kütüphane").id, "lib")

    def test_unknown_place_has_suggestions(self):
        with self.assertRaises(UnknownPlaceError) as ctx:
            self.campus.resolve("Central Libary")
        self.assertIn("Central Library", ctx.exception.suggestions)

    def test_fuzzy_match_is_not_auto_accepted(self):
        with self.assertRaises(UnknownPlaceError):
            self.campus.resolve("Scince Hall")


class ValidationTest(unittest.TestCase):
    def base(self):
        return {"places": [{"id": "a", "name": "A"}, {"id": "b", "name": "B"}],
                "edges": [{"a": "a", "b": "b", "meters": 10}], "rooms": []}

    def test_valid_minimal(self):
        self.assertEqual(len(campus_from_dict(self.base()).edges), 1)

    def test_duplicate_place(self):
        data = self.base()
        data["places"].append({"id": "a", "name": "Again"})
        with self.assertRaisesRegex(CampusDataError, "duplicate"):
            campus_from_dict(data)

    def test_edge_to_unknown_place(self):
        data = self.base()
        data["edges"].append({"a": "a", "b": "zzz", "meters": 5})
        with self.assertRaisesRegex(CampusDataError, "unknown place 'zzz'"):
            campus_from_dict(data)

    def test_non_positive_length(self):
        data = self.base()
        data["edges"][0]["meters"] = 0
        with self.assertRaises(CampusDataError):
            campus_from_dict(data)

    def test_room_must_point_to_place(self):
        data = self.base()
        data["rooms"].append({"code": "X-1", "place": "nope"})
        with self.assertRaises(CampusDataError):
            campus_from_dict(data)


if __name__ == "__main__":
    unittest.main()
