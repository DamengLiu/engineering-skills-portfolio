"""Behavioral checks for the fictional migration's offline validator."""

import json
import tempfile
import unittest
from pathlib import Path

from check_job_columns import validate_mapping


EXAMPLE_DIR = Path(__file__).parent


class ColumnCheckTests(unittest.TestCase):
    def test_example_matches_mapping(self):
        errors = validate_mapping(
            EXAMPLE_DIR / "mapping.csv", EXAMPLE_DIR / "job-manifest.json"
        )
        self.assertEqual(errors, [])

    def test_changed_writer_column_is_rejected(self):
        manifest = json.loads((EXAMPLE_DIR / "job-manifest.json").read_text())
        manifest["writer_columns"][2] = "amount"
        with tempfile.TemporaryDirectory() as temporary_dir:
            changed_manifest = Path(temporary_dir) / "job-manifest.json"
            changed_manifest.write_text(json.dumps(manifest), encoding="utf-8")
            errors = validate_mapping(
                EXAMPLE_DIR / "mapping.csv", changed_manifest)
        self.assertIn("writer column order differs from mapping", errors)


if __name__ == "__main__":
    unittest.main()
