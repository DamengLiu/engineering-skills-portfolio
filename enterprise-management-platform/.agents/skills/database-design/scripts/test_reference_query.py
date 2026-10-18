"""Focused completeness and invalidation tests using maintained catalogs."""
import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import reference_query as rq

REFS = Path(__file__).resolve().parents[1] / "references"


class QueryTests(unittest.TestCase):
    def rows(self, result, kind):
        return next(c["rows"] for c in result["catalogs"] if c["kind"] == kind)

    def test_aliases_and_complete_values(self):
        result = rq.query(REFS, ["REVIEW_RESULT"])
        rows = self.rows(result, "domain")
        self.assertEqual({c[0] for _, c in rows}, {"REVIEW_RESULT", "DECISION_STATUS"})
        self.assertEqual(len(rows), 4)
        self.assertTrue(any("不可跨场景" in line for _, line in result["catalogs"][1]["guidance"]))

    def test_chinese_and_batch(self):
        a = rq.query(REFS, ["审核结果"])
        self.assertEqual(len(self.rows(a, "domain")), 4)
        b = rq.query(REFS, ["REVIEW_RESULT", "REQUEST_STATUS"])
        expected = rq.read_catalog(REFS / "dictionary-domains.md", 7)["rows"]
        expected = [x for x in expected if x[1][0] == "REQUEST_STATUS"]
        actual = [x for x in self.rows(b, "domain") if x[1][0] == "REQUEST_STATUS"]
        self.assertEqual(actual, [[n, c] for n, c in expected])

    def test_retired_code(self):
        result = rq.query(REFS, ["OLD_ARCHIVE_FLAG"])
        self.assertIn("IS_ARCHIVED", {c[0] for _, c in self.rows(result, "domain")})
        self.assertTrue(any("已废弃" in line for _, line in result["catalogs"][1]["guidance"]))

    def test_ambiguous_primitive_and_unknown(self):
        result = rq.query(REFS, ["ACT"], "primitive")
        self.assertEqual(len(self.rows(result, "primitive")), 5)
        result = rq.query(REFS, ["NO_SUCH_FIELD_X"])
        self.assertFalse(result["found"])
        self.assertEqual(result["unmatched_terms"], ["NO_SUCH_FIELD_X"])

    def test_source_lines_and_all_rows_parse(self):
        expected = {"field": 132, "domain": 46, "primitive": 82}
        for kind, (name, width) in rq.CATALOGS.items():
            doc = rq.read_catalog(REFS / name, width)
            if kind in expected:
                self.assertEqual(len(doc["rows"]), expected[kind])
            lines = (REFS / name).read_text(encoding="utf-8").splitlines()
            for number, cells in doc["rows"]:
                self.assertIn(cells[0], lines[number - 1])

    def test_changes_invalidate_and_no_disk_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            refs = Path(temp)
            for name, _ in rq.CATALOGS.values():
                shutil.copyfile(REFS / name, refs / name)
            a = rq.query(refs, ["REVIEW_RESULT"])
            self.assertEqual(a["fingerprint"], rq.query(refs, ["REVIEW_RESULT"])["fingerprint"])
            self.assertNotEqual(a["fingerprint"], rq.query(refs, ["REQUEST_STATUS"])["fingerprint"])
            p = refs / "dictionary-domains.md"
            p.write_text(p.read_text(encoding="utf-8") + "\n新版说明\n", encoding="utf-8")
            self.assertNotEqual(a["fingerprint"], rq.query(refs, ["REVIEW_RESULT"])["fingerprint"])
            self.assertEqual(len(list(refs.iterdir())), 3)

    def test_cli_reuse(self):
        fp = rq.query(REFS, ["REVIEW_RESULT"])["fingerprint"]
        out = io.StringIO()
        with patch.object(sys, "argv", ["query", "REVIEW_RESULT", "--known", fp]):
            with contextlib.redirect_stdout(out):
                rq.main()
        self.assertEqual(json.loads(out.getvalue())["status"], "unchanged")

    def test_evidence_change(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "source.txt"
            p.write_text("before")
            first = rq.evidence([p])
            p.write_text("after")
            self.assertNotEqual(first, rq.evidence([p]))

    def test_escaped_pipe_and_invalid_table(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "table.md"
            p.write_text("| code | name |\n| --- | --- |\n| X | a\\|b |\n")
            self.assertEqual(rq.read_catalog(p, 2)["rows"][0][1], ["X", "a|b"])
            with self.assertRaises(ValueError):
                rq.read_catalog(p, 3)


if __name__ == "__main__":
    unittest.main()
