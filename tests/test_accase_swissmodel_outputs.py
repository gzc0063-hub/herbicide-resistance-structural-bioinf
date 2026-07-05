import csv
from pathlib import Path
import unittest


class TestACCaseSwissModelOutputs(unittest.TestCase):
    def test_swissmodel_output_uses_weed_residues_and_transferred_core(self):
        path = Path("data/processed/accase_swissmodel_1uys_distance_sasa.csv")
        self.assertTrue(path.exists())

        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        self.assertEqual(1132, len(rows))
        by_site = {
            (row["chain_id"], int(row["blackgrass_position"])): row
            for row in rows
            if row["blackgrass_position"]
        }
        expected = {
            ("A", 1781): ("143", "ILE", "True"),
            ("B", 2027): ("389", "TRP", "False"),
            ("B", 2041): ("403", "ILE", "True"),
            ("B", 2078): ("440", "ASP", "False"),
            ("B", 2088): ("450", "CYS", "False"),
            ("B", 2096): ("458", "GLY", "False"),
        }
        for key, (model_position, residue_name, in_core) in expected.items():
            self.assertIn(key, by_site)
            row = by_site[key]
            self.assertEqual(model_position, row["pdb_position"])
            self.assertEqual(residue_name, row["residue_name"])
            self.assertEqual(in_core, row["in_active_site_core"])
            self.assertNotEqual("", row["sasa_A2"])
            self.assertNotEqual("", row["percentile_rank_distance_to_core"])


if __name__ == "__main__":
    unittest.main()
