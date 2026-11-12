import json
import threading
import unittest
import urllib.error
import urllib.request
from datetime import datetime

from campusroute.api import build_api, make_server

FIXED_NOW = datetime(2027, 3, 1, 12, 30)


class ApiLogicTest(unittest.TestCase):
    """Calls the API object directly: fast, no sockets."""

    @classmethod
    def setUpClass(cls):
        cls.api = build_api(clock=lambda: FIXED_NOW)

    def test_route(self):
        body = self.api.handle("/api/route", {"from": ["Main Gate"], "to": ["ENG-B204"]})
        self.assertEqual(body["meters"], 790)
        self.assertEqual(body["names"][-1], "Engineering Building B")

    def test_next_class_uses_clock(self):
        body = self.api.handle("/api/next-class", {})
        self.assertEqual(body["next"]["session"], "Mon 13:00-14:50 MATH203 Probability @ SCI-202")
        self.assertEqual(body["next"]["in_minutes"], 30)
        self.assertEqual(body["next"]["place"], "sci")

    def test_crowd(self):
        levels = self.api.handle("/api/crowd", {})["levels"]
        self.assertEqual(levels["caf"], "packed")
        self.assertNotIn("health", levels)


class ApiHttpTest(unittest.TestCase):
    """Runs the real HTTP server on 127.0.0.1 with a random free port."""

    @classmethod
    def setUpClass(cls):
        cls.server = make_server(port=0, api=build_api(clock=lambda: FIXED_NOW))
        cls.base = "http://127.0.0.1:%d" % cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def get(self, path):
        try:
            with urllib.request.urlopen(self.base + path, timeout=5) as res:
                return res.status, res.headers, res.read()
        except urllib.error.HTTPError as err:
            return err.code, err.headers, err.read()

    def test_binds_to_localhost_only(self):
        self.assertEqual(self.server.server_address[0], "127.0.0.1")

    def test_index_served_with_security_headers(self):
        status, headers, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn(b"CampusRoute", body)
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("default-src 'self'", headers["Content-Security-Policy"])

    def test_search_json_utf8(self):
        status, _, body = self.get("/api/search?q=cinar")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["results"][0]["label"], "Çınar Café")

    def test_unknown_place_is_404_json(self):
        status, _, body = self.get("/api/route?from=gate&to=moon")
        self.assertEqual(status, 404)
        self.assertIn("unknown place", json.loads(body)["error"])

    def test_path_traversal_not_served(self):
        status, _, _ = self.get("/../data/campus.json")
        self.assertEqual(status, 404)

    def test_post_rejected(self):
        req = urllib.request.Request(self.base + "/api/route", data=b"{}", method="POST")
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req, timeout=5)
        self.assertEqual(ctx.exception.code, 405)


if __name__ == "__main__":
    unittest.main()
