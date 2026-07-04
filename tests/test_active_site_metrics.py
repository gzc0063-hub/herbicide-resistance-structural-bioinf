import math
import unittest

from scripts.active_site_metrics import distance_rows


class ActiveSiteMetricsTest(unittest.TestCase):
    def setUp(self):
        self.residues = {
            10: (0.0, 0.0, 0.0),
            20: (3.0, 0.0, 0.0),
            30: (10.0, 0.0, 0.0),
        }

    def test_core_residue_has_zero_distance_to_core_and_nonzero_distance_to_other_core(self):
        rows = {row["position"]: row for row in distance_rows(self.residues, core_positions=[10, 20])}

        self.assertIs(rows[10]["in_active_site_core"], True)
        self.assertEqual(rows[10]["distance_to_active_site_core_A"], 0.0)
        self.assertEqual(rows[10]["distance_to_nearest_other_core_residue_A"], 3.0)

    def test_noncore_residue_uses_nearest_core_for_both_distance_metrics(self):
        rows = {row["position"]: row for row in distance_rows(self.residues, core_positions=[10, 20])}

        self.assertIs(rows[30]["in_active_site_core"], False)
        self.assertEqual(rows[30]["distance_to_active_site_core_A"], 7.0)
        self.assertEqual(rows[30]["distance_to_nearest_other_core_residue_A"], 7.0)

    def test_percentile_rank_uses_distance_to_core_including_self(self):
        rows = {row["position"]: row for row in distance_rows(self.residues, core_positions=[10, 20])}

        self.assertTrue(math.isclose(rows[10]["percentile_rank_distance_to_core"], 66.6666666667))
        self.assertTrue(math.isclose(rows[20]["percentile_rank_distance_to_core"], 66.6666666667))
        self.assertEqual(rows[30]["percentile_rank_distance_to_core"], 100.0)


if __name__ == "__main__":
    unittest.main()
