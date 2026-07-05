import csv
import tempfile
import unittest
from pathlib import Path

from scripts.build_review_driven_outputs import build_review_driven_outputs


class ReviewDrivenOutputsTest(unittest.TestCase):
    def test_builds_controlled_mechanism_annotations_and_manuscript_outputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            outputs = build_review_driven_outputs(
                repo_root=Path("."),
                table_dir=Path(tmpdir) / "tables",
                figure_dir=Path(tmpdir) / "figures",
            )

            with outputs["mechanism_table"].open(newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(14, len(rows))
            self.assertNotIn("HPPD", {row["family"] for row in rows})
            self.assertEqual(
                len(rows),
                len({(row["family"], row["structure_position"]) for row in rows}),
            )

            allowed_labels = {
                "direct_core",
                "adjacent",
                "second_shell_channel",
                "allosteric_hinge",
                "interface_induced_fit",
                "unresolved_static_candidate",
            }
            self.assertLessEqual({row["mechanism_label"] for row in rows}, allowed_labels)

            unresolved = [
                row
                for row in rows
                if row["mechanism_label"] == "unresolved_static_candidate"
            ]
            self.assertTrue(unresolved)
            self.assertTrue(
                all(row["mechanism_evidence_level"] != "literature_supported" for row in unresolved)
            )

            delta_g210 = next(row for row in rows if row["structure_position"] == "178")
            self.assertEqual("PPO", delta_g210["family"])
            self.assertEqual("allosteric_hinge", delta_g210["mechanism_label"])
            self.assertEqual("literature_supported", delta_g210["mechanism_evidence_level"])

            cys2088 = next(row for row in rows if row["mutation_ids"] == "Cys2088Arg")
            self.assertEqual("interface_induced_fit", cys2088["mechanism_label"])

            with outputs["table_3"].open(newline="") as handle:
                hppd_rows = list(csv.DictReader(handle))
            self.assertEqual(1, len(hppd_rows))
            self.assertEqual("HPPD", hppd_rows[0]["family"])
            self.assertEqual("0", hppd_rows[0]["accepted_tsr_rows"])

            expected_figures = {
                "figure_1_workflow.svg",
                "figure_2_permutation_enrichment.svg",
                "figure_3_position_screen.svg",
                "figure_4_distance_rsa_conservation.svg",
            }
            self.assertEqual(expected_figures, {path.name for path in outputs["figures"]})
            for figure in outputs["figures"]:
                text = figure.read_text(encoding="utf-8")
                self.assertIn("<svg", text)
                self.assertIn("</svg>", text)


if __name__ == "__main__":
    unittest.main()
