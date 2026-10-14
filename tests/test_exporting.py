import csv
import io
import unittest

from nexarack.exporting import records_to_csv


class ExportTests(unittest.TestCase):
    def test_csv_header_and_nested_json(self):
        text = records_to_csv([{"time_seconds": 1, "power": {"watts": 500}}])
        rows = list(csv.DictReader(io.StringIO(text)))
        self.assertEqual(rows[0]["time_seconds"], "1")
        self.assertEqual(rows[0]["power"], '{"watts":500}')

    def test_empty_records(self):
        self.assertEqual(records_to_csv([]), "")


if __name__ == "__main__":
    unittest.main()
