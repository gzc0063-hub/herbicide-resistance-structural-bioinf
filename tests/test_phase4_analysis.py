import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.build_phase4_analysis import build_phase4_analysis


class Phase4AnalysisTest(unittest.TestCase):
    def test_runs_family_permutation_analysis_on_unique_structural_positions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            summary_path, screen_path = build_phase4_analysis(
                repo_root=Path("."),
                output_dir=Path(tmpdir),
                iterations=200,
                seed=123,
            )

            with summary_path.open(newline="") as handle:
                summary_rows = list(csv.DictReader(handle))
            self.assertEqual(
                {"PPO", "ALS", "EPSPS", "ACCase"},
                {row["family"] for row in summary_rows},
            )
            # Each family has an "all" row; families with at least one non-core
            # accepted position also get a "non_core_only" row (ALS has none, since
            # both Trp574 and Ser653 are direct-core).
            all_rows = {row["family"]: row for row in summary_rows if row["position_set"] == "all"}
            expected_all_counts = {"PPO": "4", "ALS": "4", "EPSPS": "1", "ACCase": "6"}
            for family, count in expected_all_counts.items():
                self.assertEqual(count, all_rows[family]["n_unique_positions"])
            non_core_families = {
                row["family"] for row in summary_rows if row["position_set"] == "non_core_only"
            }
            self.assertEqual({"PPO", "EPSPS", "ACCase"}, non_core_families)
            for row in summary_rows:
                self.assertIn(row["position_set"], {"all", "non_core_only"})
                self.assertEqual("200", row["iterations"])
                self.assertGreaterEqual(float(row["empirical_p_value_lower_tail"]), 0.0)
                self.assertLessEqual(float(row["empirical_p_value_lower_tail"]), 1.0)
                self.assertNotEqual("", row["observed_mean_percentile"])
                self.assertNotEqual("", row["random_mean_percentile_mean"])

            with screen_path.open(newline="") as handle:
                screen_rows = list(csv.DictReader(handle))
            self.assertEqual(15, len(screen_rows))
            self.assertNotIn("HPPD", {row["family"] for row in screen_rows})

            delta_g210 = next(row for row in screen_rows if row["structure_position"] == "178")
            self.assertEqual("PPO", delta_g210["family"])
            self.assertEqual("deltaG210_pair1;deltaG210_pair2", delta_g210["mutation_ids"])
            self.assertEqual("non_core_adjacent", delta_g210["proximity_class"])

            cys2088 = next(row for row in screen_rows if row["mutation_ids"] == "Cys2088Arg")
            self.assertEqual("ACCase", cys2088["family"])
            self.assertEqual("B:450", cys2088["structure_position"])
            self.assertEqual("non_core_candidate", cys2088["proximity_class"])

    def test_cli_runs_from_repo_root(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_phase4_analysis.py",
                    "--output-dir",
                    tmpdir,
                    "--iterations",
                    "10",
                    "--seed",
                    "1",
                ],
                cwd=Path("."),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual("", result.stderr)
            self.assertEqual(0, result.returncode)
            self.assertTrue((Path(tmpdir) / "phase4_permutation_summary.csv").exists())
            self.assertTrue((Path(tmpdir) / "phase4_non_core_position_screen.csv").exists())


if __name__ == "__main__":
    unittest.main()
