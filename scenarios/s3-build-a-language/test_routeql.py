"""Black-box acceptance tests for a RouteQL interpreter.

They run the interpreter as a separate process and only look at stdout,
stderr and the exit status, so they work for ANY implementation that follows
routeql-spec.md.

    # from the workspace root (the folder that contains app/ and scenarios/)
    python3 scenarios/s3-build-a-language/test_routeql.py              # tests out/routeql.py
    ROUTEQL=path/to/other.py python3 scenarios/s3-build-a-language/test_routeql.py
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = Path(os.environ.get("ROUTEQL", HERE / "out" / "routeql.py")).resolve()


def run_source(source):
    with tempfile.NamedTemporaryFile("w", suffix=".rql", delete=False, encoding="utf-8") as fh:
        fh.write(source)
        name = fh.name
    try:
        return run_file(name)
    finally:
        os.unlink(name)


def run_file(path):
    proc = subprocess.run([sys.executable, str(TARGET), str(path)], capture_output=True,
                          text=True, encoding="utf-8", timeout=20)
    return proc.returncode, proc.stdout, proc.stderr


@unittest.skipUnless(TARGET.exists(), "interpreter not found at %s" % TARGET)
class ExamplesTest(unittest.TestCase):
    def test_01_basics(self):
        code, out, err = run_file(HERE / "examples" / "01-basics.rql")
        self.assertEqual(code, 0, err)
        self.assertEqual(out.splitlines(), [
            "Morning route",
            "North Dormitory -> Engineering Building B: 580 m, 8 min",
            "  North Dormitory > North Path Junction > Engineering Building A > Engineering Building B",
            'find "cafe":',
            "  - Çınar Café",
        ])

    def test_02_avoid_stairs_changes_route(self):
        code, out, err = run_file(HERE / "examples" / "02-accessibility.rql")
        self.assertEqual(code, 0, err)
        lines = out.splitlines()
        self.assertEqual(lines[0], "Science Hall -> Engineering Building B: 270 m, 4 min (stairs)")
        self.assertEqual(lines[2], "Science Hall -> Engineering Building B: 540 m, 7 min")
        self.assertTrue(lines[4].startswith("Main Gate -> Sports Center: 1460 m"))

    def test_03_runtime_error_keeps_earlier_output(self):
        code, out, err = run_file(HERE / "examples" / "03-runtime-error.rql")
        self.assertEqual(code, 1)
        self.assertIn("Main Gate -> Sports Center: 870 m, 11 min", out)
        self.assertNotIn("never printed", out)
        self.assertIn("Error on line 3:", err)
        self.assertIn("undefined variable 'library'", err)

    def test_04_syntax_error_means_no_output(self):
        code, out, err = run_file(HERE / "examples" / "04-syntax-error.rql")
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("Error on line 2:", err)
        self.assertIn("syntax error", err)


@unittest.skipUnless(TARGET.exists(), "interpreter not found at %s" % TARGET)
class SpecTest(unittest.TestCase):
    def test_comments_blank_lines_and_hash_in_string(self):
        code, out, _ = run_source('# c\n\nprint "room #1"  # trailing\n')
        self.assertEqual((code, out), (0, "room #1\n"))

    def test_print_variable_and_reassign(self):
        code, out, _ = run_source('let a = "x"\nlet a = "y"\nprint a\n')
        self.assertEqual(out, "y\n")

    def test_unknown_place_offers_suggestion(self):
        code, _, err = run_source('route "Main Gate" to "Central Libary"\n')
        self.assertEqual(code, 1)
        self.assertIn("Error on line 1:", err)
        self.assertIn("Central Library", err)

    def test_fuzzy_place_not_accepted(self):
        code, out, _ = run_source('route "gate" to "libary"\n')
        self.assertEqual((code, out), (1, ""))

    def test_unterminated_string(self):
        code, _, err = run_source('print "oops\n')
        self.assertEqual(code, 1)
        self.assertIn("unterminated string", err)

    def test_keyword_cannot_be_variable(self):
        code, _, err = run_source('let route = "x"\n')
        self.assertEqual(code, 1)
        self.assertIn("syntax error", err)

    def test_line_numbers_count_comments(self):
        code, _, err = run_source('# one\n# two\nprint nope\n')
        self.assertIn("Error on line 3:", err)

    def test_find_no_matches(self):
        _, out, _ = run_source('find "zzzzqqq"\n')
        self.assertEqual(out, 'find "zzzzqqq":\n  (no matches)\n')

    def test_room_codes_and_accents(self):
        code, out, _ = run_source('route "inonu" to "eng-a101"\n')
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("İnönü Auditorium -> Engineering Building A:"))

    def test_python_code_is_never_executed(self):
        code, out, err = run_source('print __import__("os").getcwd()\n')
        self.assertEqual(code, 1)
        self.assertEqual(out, "")

    def test_usage_error_exit_2(self):
        proc = subprocess.run([sys.executable, str(TARGET)], capture_output=True, text=True, timeout=20)
        self.assertEqual(proc.returncode, 2)


class SourceSafetyTest(unittest.TestCase):
    @unittest.skipUnless(TARGET.exists(), "interpreter not found")
    def test_no_dangerous_calls(self):
        src = TARGET.read_text(encoding="utf-8")
        for banned in ("eval(", "exec(", "compile(", "os.system", "subprocess"):
            self.assertNotIn(banned, src, "%s found in interpreter" % banned)


if __name__ == "__main__":
    print("Testing interpreter:", TARGET, file=sys.stderr)
    unittest.main()
