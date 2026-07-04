import csv
import unittest


class TestACCaseOutputs(unittest.TestCase):
    def test_mutation_sites_have_expected_mapping_and_metrics(self):
        with open("data/processed/accase_1uys_distance_sasa.csv", encoding="utf-8") as handle:
            distance_rows = list(csv.DictReader(handle))
        with open("data/processed/accase_conservation_entropy.csv", encoding="utf-8") as handle:
            conservation_rows = list(csv.DictReader(handle))

        by_site = {
            (row["chain_id"], int(float(row["blackgrass_position"]))): row
            for row in distance_rows
            if row["blackgrass_position"]
        }
        conservation_by_pos = {
            int(row["blackgrass_position"]): row
            for row in conservation_rows
        }

        expected = {
            ("C", 1781): ("1705", "LEU", "True"),
            ("B", 2027): ("1953", "TRP", "False"),
            ("B", 2041): ("1967", "VAL", "True"),
            ("B", 2078): ("2004", "ASP", "False"),
            ("B", 2088): ("2014", "MSE", "False"),
            ("B", 2096): ("2022", "ALA", "False"),
        }
        for key, (pdb_position, residue_name, in_core) in expected.items():
            self.assertIn(key, by_site)
            row = by_site[key]
            self.assertEqual(row["pdb_position"], pdb_position)
            self.assertEqual(row["residue_name"], residue_name)
            self.assertEqual(row["in_active_site_core"], in_core)
            self.assertIn(key[1], conservation_by_pos)

        self.assertEqual(len(distance_rows), 1328)
        self.assertEqual(len(conservation_rows), 562)
        self.assertAlmostEqual(
            float(by_site[("B", 2088)]["distance_to_active_site_core_A"]),
            11.830785350094052,
        )
        self.assertAlmostEqual(
            float(conservation_by_pos[2027]["normalized_conservation"]),
            1.0,
        )


if __name__ == "__main__":
    unittest.main()
