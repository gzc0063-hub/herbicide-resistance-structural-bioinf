import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HppdOutputTests(unittest.TestCase):
    def test_5ywg_active_site_core(self):
        rows = {}
        with (ROOT / "data" / "processed" / "hppd_5ywg_active_site_metrics.csv").open(newline="") as f:
            for row in csv.DictReader(f):
                rows[(row["chain_id"], int(row["pdb_position"]))] = row

        core_positions = {
            key for key, row in rows.items()
            if row["in_active_site_core"].strip().lower() == "true"
        }
        expected_chain_core = {226, 228, 267, 280, 282, 307, 308, 368, 379, 381, 392, 394, 419, 420, 421, 423, 424}

        self.assertEqual(735, len(rows))
        self.assertEqual(34, len(core_positions))
        self.assertEqual(expected_chain_core, {pos for chain, pos in core_positions if chain == "A"})
        self.assertEqual(expected_chain_core, {pos for chain, pos in core_positions if chain == "B"})

        for pos, residue_name, ligand_name in [
            (226, "HIS", "CO"),
            (308, "HIS", "CO"),
            (394, "GLU", "CO"),
            (424, "PHE", "92L"),
        ]:
            row = rows[("A", pos)]
            self.assertEqual(residue_name, row["residue_name"])
            self.assertEqual("True", row["in_active_site_core"])
            self.assertEqual(ligand_name, row["nearest_core_ligand"])
            self.assertAlmostEqual(0.0, float(row["distance_to_active_site_core_A"]))
            self.assertAlmostEqual(4.625850340136054, float(row["percentile_rank_distance_to_core"]))


if __name__ == "__main__":
    unittest.main()
