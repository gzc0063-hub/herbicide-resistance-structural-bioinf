import csv
import unittest


class EpspsConservationOutputsTest(unittest.TestCase):
    def test_conservation_rows_are_limited_to_structured_8umj_residues(self):
        with open("data/processed/epsps_8umj_distance_sasa.csv", encoding="utf-8") as handle:
            distance_positions = {int(row["position"]) for row in csv.DictReader(handle)}
        with open("data/processed/epsps_conservation_entropy.csv", encoding="utf-8") as handle:
            conservation_positions = {int(row["position"]) for row in csv.DictReader(handle)}

        self.assertEqual(conservation_positions, distance_positions)
        self.assertNotIn(0, conservation_positions)
        self.assertNotIn(1, conservation_positions)

    def test_pro106_conservation_row_matches_distance_residue(self):
        with open("data/processed/epsps_conservation_entropy.csv", encoding="utf-8") as handle:
            conservation = {int(row["position"]): row for row in csv.DictReader(handle)}

        self.assertEqual(conservation[106]["sequence_position"], "107")
        self.assertEqual(conservation[106]["residue"], "P")
        self.assertEqual(conservation[106]["normalized_conservation"], "1.0")


if __name__ == "__main__":
    unittest.main()
