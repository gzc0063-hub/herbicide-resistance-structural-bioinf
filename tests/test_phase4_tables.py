import csv
import tempfile
import unittest
from pathlib import Path

from scripts.build_phase4_tables import build_phase4_tables


class Phase4TablesTest(unittest.TestCase):
    def test_builds_pooled_mutation_table_with_joined_static_metrics(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            mutation_path, contrast_path = build_phase4_tables(
                repo_root=Path("."),
                output_dir=Path(tmpdir),
            )

            with mutation_path.open(newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(19, len(rows))
            self.assertEqual(
                {"PPO", "ALS", "EPSPS", "ACCase"},
                {row["family"] for row in rows},
            )
            self.assertNotIn("HPPD", {row["family"] for row in rows})

            required_columns = {
                "family",
                "mutation_id",
                "native_position",
                "structure_position",
                "structure_residue_name",
                "in_active_site_core",
                "distance_to_active_site_core_A",
                "percentile_rank_distance_to_core",
                "sasa_A2",
                "max_sasa_tien2013_A2",
                "rsa_tien2013",
                "shannon_entropy",
                "normalized_conservation",
                "bulkiness_delta",
                "hydropathy_delta",
                "charge_delta",
                "confidence",
                "source_doi",
            }
            self.assertLessEqual(required_columns, set(rows[0]))

            delta_g210 = next(row for row in rows if row["mutation_id"] == "deltaG210_pair1")
            self.assertEqual("PPO", delta_g210["family"])
            self.assertEqual("178", delta_g210["structure_position"])
            self.assertEqual("GLY", delta_g210["structure_residue_name"])
            self.assertEqual("FALSE", delta_g210["in_active_site_core"])
            self.assertNotEqual("", delta_g210["rsa_tien2013"])
            self.assertNotEqual("", delta_g210["normalized_conservation"])

            trp574 = next(row for row in rows if row["mutation_id"] == "Trp574Leu")
            self.assertEqual("ALS", trp574["family"])
            self.assertEqual("TRUE", trp574["in_active_site_core"])
            self.assertEqual("0.0", trp574["distance_to_active_site_core_A"])

            cys2088 = next(row for row in rows if row["mutation_id"] == "Cys2088Arg")
            self.assertEqual("ACCase", cys2088["family"])
            self.assertEqual("B:450", cys2088["structure_position"])
            self.assertEqual("450", cys2088["structure_pdb_position"])
            self.assertEqual("CYS", cys2088["structure_residue_name"])
            self.assertEqual("True", cys2088["template_matches_weed_residue"])
            self.assertEqual("False", cys2088["template_is_resistant_state"])
            self.assertNotEqual("", cys2088["rsa_tien2013"])

            thr102 = next(row for row in rows if row["mutation_id"] == "Thr102Ile")
            self.assertEqual("EPSPS", thr102["family"])
            self.assertEqual("102", thr102["structure_position"])
            self.assertEqual("THR", thr102["structure_residue_name"])
            self.assertEqual("True", thr102["template_matches_weed_residue"])
            self.assertNotEqual("", thr102["bulkiness_delta"])
            self.assertNotEqual("", thr102["hydropathy_delta"])

            asp376 = next(row for row in rows if row["mutation_id"] == "Asp376Glu")
            self.assertEqual("ALS", asp376["family"])
            self.assertEqual("376", asp376["structure_position"])
            self.assertEqual("ASP", asp376["structure_residue_name"])
            self.assertEqual("True", asp376["template_matches_weed_residue"])
            self.assertEqual("TRUE", asp376["in_active_site_core"])

            with contrast_path.open(newline="") as handle:
                contrast_rows = list(csv.DictReader(handle))
            self.assertEqual(1, len(contrast_rows))
            self.assertEqual("HPPD", contrast_rows[0]["family"])
            self.assertEqual("0", contrast_rows[0]["accepted_tsr_rows"])
            self.assertEqual("no_verified_weed_tsr_accepted", contrast_rows[0]["status"])


if __name__ == "__main__":
    unittest.main()
