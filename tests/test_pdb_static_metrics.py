import math
import unittest

from scripts.pdb_static_metrics import (
    Atom,
    ligand_contact_core,
    residue_sasa,
)


class PdbStaticMetricsTest(unittest.TestCase):
    def test_ligand_contact_core_uses_protein_atoms_within_cutoff(self):
        atoms = [
            Atom("CA", "ALA", "A", 10, (0.0, 0.0, 0.0), "C", True),
            Atom("CB", "ALA", "A", 10, (1.0, 0.0, 0.0), "C", True),
            Atom("CA", "GLY", "A", 20, (10.0, 0.0, 0.0), "C", True),
            Atom("P1", "GPJ", "A", 501, (2.0, 0.0, 0.0), "P", False),
        ]

        self.assertEqual(ligand_contact_core(atoms, "A", {"GPJ"}, cutoff=2.1), [10])

    def test_residue_sasa_drops_when_neighbor_blocks_surface(self):
        exposed = [Atom("CA", "ALA", "A", 10, (0.0, 0.0, 0.0), "C", True)]
        blocked = exposed + [Atom("CA", "GLY", "A", 20, (2.0, 0.0, 0.0), "C", True)]

        exposed_sasa = residue_sasa(exposed, n_sphere_points=120)[("A", 10)]
        blocked_sasa = residue_sasa(blocked, n_sphere_points=120)[("A", 10)]

        self.assertGreater(exposed_sasa, 100.0)
        self.assertLess(blocked_sasa, exposed_sasa)
        self.assertTrue(math.isfinite(blocked_sasa))


if __name__ == "__main__":
    unittest.main()
