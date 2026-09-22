import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from dashboard_generator.cli import main


class CliTests(unittest.TestCase):
    def test_build_json_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, output = root / "data.csv", root / "dashboard.html"
            source.write_text("item,value\nA,4\nB,8\n", encoding="utf-8")
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = main([str(source), "-o", str(output), "--json"])
            self.assertEqual(code, 0)
            self.assertTrue(output.exists())
            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["rows"], 2)

    def test_missing_input_returns_error(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = main(["definitely-missing.csv"])
        self.assertEqual(code, 2)
        self.assertIn("not found", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
