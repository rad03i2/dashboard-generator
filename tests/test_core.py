import json
import tempfile
import unittest
from pathlib import Path

from dashboard_generator import DashboardError, build_dashboard, load_records


class DashboardTests(unittest.TestCase):
    def test_load_csv_and_render_safe_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "input.csv"
            source.write_text("name,score\nAlice,10\n<script>alert(1)</script>,20\n", encoding="utf-8")
            records = load_records(source)
            output = root / "report.html"
            result = build_dashboard(records, output, title="A < B")
            text = output.read_text(encoding="utf-8")
            self.assertEqual(result.rows, 2)
            self.assertEqual(result.numeric_columns, ("score",))
            self.assertIn("A &lt; B", text)
            self.assertNotIn("<script>alert(1)</script>", text)
            self.assertIn("\\u003cscript", text)

    def test_json_union_of_columns_and_nested_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "input.json"
            source.write_text(json.dumps([{"a": 1}, {"b": {"x": 2}}]), encoding="utf-8")
            records = load_records(source)
            result = build_dashboard(records, root / "out.html")
            self.assertEqual(result.columns, ("a", "b"))
            self.assertEqual(result.rendered_rows, 2)

    def test_max_rows_does_not_change_total(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = build_dashboard([{"n": i} for i in range(5)], Path(tmp) / "out.html", max_rows=2)
            self.assertEqual((result.rows, result.rendered_rows), (5, 2))

    def test_rejects_invalid_options_and_json_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "bad.json"
            source.write_text('{"not":"an array"}', encoding="utf-8")
            with self.assertRaises(DashboardError):
                load_records(source)
            with self.assertRaises(DashboardError):
                build_dashboard([], root / "x.html", theme="blue")
            with self.assertRaises(DashboardError):
                build_dashboard([], root / "x.html", max_rows=0)

    def test_empty_dataset_renders(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = build_dashboard([], Path(tmp) / "empty.html")
            self.assertEqual(result.columns, ())
            self.assertEqual(result.rows, 0)


if __name__ == "__main__":
    unittest.main()
