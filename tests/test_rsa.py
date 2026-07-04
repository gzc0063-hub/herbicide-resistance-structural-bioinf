import csv
import io
import math
import tempfile
import unittest
from pathlib import Path

from scripts.rsa import DEFAULT_CSVS, add_rsa_to_csv, max_sasa_tien2013


class RsaTest(unittest.TestCase):
    def test_max_sasa_tien2013_handles_standard_and_modified_residues(self):
        self.assertEqual(max_sasa_tien2013("ALA"), 129)
        self.assertEqual(max_sasa_tien2013("MSE"), 224)
        self.assertEqual(max_sasa_tien2013("CSD"), 167)
        self.assertIsNone(max_sasa_tien2013("UNK"))

    def test_add_rsa_to_csv_preserves_raw_sasa_and_adds_normalized_columns(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "metrics.csv"
            path.write_text(
                "position,residue_name,sasa_A2\n"
                "1,ALA,64.5\n"
                "2,MSE,112\n"
                "3,UNK,10\n"
                "4,GLY,\n",
                encoding="utf-8",
            )

            add_rsa_to_csv(path)

            rows = list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8"))))

        self.assertEqual(rows[0]["sasa_A2"], "64.5")
        self.assertEqual(rows[0]["max_sasa_tien2013_A2"], "129")
        self.assertTrue(math.isclose(float(rows[0]["rsa_tien2013"]), 0.5))
        self.assertEqual(rows[1]["max_sasa_tien2013_A2"], "224")
        self.assertTrue(math.isclose(float(rows[1]["rsa_tien2013"]), 0.5))
        self.assertEqual(rows[2]["max_sasa_tien2013_A2"], "")
        self.assertEqual(rows[2]["rsa_tien2013"], "")
        self.assertEqual(rows[3]["max_sasa_tien2013_A2"], "104")
        self.assertEqual(rows[3]["rsa_tien2013"], "")

    def test_processed_metric_outputs_include_rsa_for_standard_residues(self):
        for path in DEFAULT_CSVS:
            with self.subTest(path=path):
                with path.open(newline="", encoding="utf-8") as handle:
                    rows = list(csv.DictReader(handle))

                self.assertGreater(len(rows), 0)
                for row in rows:
                    self.assertIn("max_sasa_tien2013_A2", row)
                    self.assertIn("rsa_tien2013", row)
                    if row["sasa_A2"] and max_sasa_tien2013(row["residue_name"]) is not None:
                        self.assertGreater(float(row["max_sasa_tien2013_A2"]), 0.0)
                        self.assertTrue(math.isfinite(float(row["rsa_tien2013"])))


if __name__ == "__main__":
    unittest.main()
