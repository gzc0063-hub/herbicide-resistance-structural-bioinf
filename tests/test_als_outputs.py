import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AlsOutputTests(unittest.TestCase):
    def test_interface_corrected_active_site_core(self):
        rows = {}
        with (ROOT / "data" / "processed" / "als_1z8n_distance_sasa.csv").open(newline="") as f:
            for row in csv.DictReader(f):
                rows[int(row["position"])] = row

        core_positions = {
            pos for pos, row in rows.items()
            if row["in_active_site_core"].strip().upper() == "TRUE"
        }
        self.assertEqual(27, len(core_positions))
        self.assertTrue({121, 122, 168, 195, 196, 197, 199, 200, 206, 207, 256}.issubset(core_positions))

        for pos, name, nearest_other in [
            (122, "ALA", 3.8050826535043862),
            (197, "PRO", 3.8390739768855795),
            (574, "TRP", 10.606712450142123),
            (653, "SER", 3.7948288498956098),
        ]:
            row = rows[pos]
            self.assertEqual(name, row["residue_name"])
            self.assertEqual("TRUE", row["in_active_site_core"])
            self.assertAlmostEqual(0.0, float(row["distance_to_active_site_core_A"]))
            self.assertAlmostEqual(nearest_other, float(row["distance_to_nearest_other_core_residue_A"]))
            self.assertAlmostEqual(4.639175257731959, float(row["percentile_rank_distance_to_core"]))


if __name__ == "__main__":
    unittest.main()
