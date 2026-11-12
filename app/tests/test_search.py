import unittest

from campusroute.campus import load_campus
from campusroute.search import normalize, search


class NormalizeTest(unittest.TestCase):
    def test_turkish_letters_fold(self):
        self.assertEqual(normalize("İnönü"), "inonu")
        self.assertEqual(normalize("ISIK ışık"), "isik isik")
        self.assertEqual(normalize("Çınar  Café"), "cinar cafe")

    def test_dashes_and_spaces(self):
        self.assertEqual(normalize("  ENG-B204 "), "eng b204")


class SearchTest(unittest.TestCase):
    def setUp(self):
        self.campus = load_campus()

    def test_room_code(self):
        self.assertEqual(search(self.campus, "B204")[0].id, "ENG-B204")

    def test_alias_in_turkish(self):
        self.assertEqual(search(self.campus, "kutuphane")[0].place_id, "lib")

    def test_typo_still_found(self):
        self.assertEqual(search(self.campus, "libary")[0].place_id, "lib")

    def test_junctions_hidden(self):
        ids = [h.id for h in search(self.campus, "junction", limit=20)]
        self.assertNotIn("j-north", ids)

    def test_empty_query(self):
        self.assertEqual(search(self.campus, "   "), [])

    def test_limit_and_order(self):
        hits = search(self.campus, "eng", limit=3)
        self.assertEqual(len(hits), 3)
        self.assertEqual(hits, sorted(hits, key=lambda h: (-h.score, h.label)))


if __name__ == "__main__":
    unittest.main()
