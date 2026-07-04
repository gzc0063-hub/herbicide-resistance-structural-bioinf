import unittest

from scripts.reference_conservation import conservation_rows, translate_dna


class ReferenceConservationTest(unittest.TestCase):
    def test_conservation_rows_are_indexed_by_reference_positions(self):
        records = {
            "ref": "MPQT",
            "same": "MPQT",
            "variant": "MSQT",
            "insertion": "MAPQT",
        }

        rows = {row["position"]: row for row in conservation_rows(records, "ref")}

        self.assertEqual(rows[2]["residue"], "P")
        self.assertEqual(rows[2]["n_species_present"], 4)
        self.assertGreater(rows[2]["shannon_entropy"], 0.0)
        self.assertLess(rows[2]["normalized_conservation"], 1.0)
        self.assertEqual(rows[3]["residue"], "Q")
        self.assertEqual(rows[3]["shannon_entropy"], 0.0)

    def test_translate_dna_stops_at_first_stop_codon(self):
        self.assertEqual(translate_dna("ATGCCCTAAATG"), "MP")


if __name__ == "__main__":
    unittest.main()
