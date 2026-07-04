from chimerax.core.commands import run
import numpy as np

session = session  # noqa: F821

run(session, "open data/raw/1SEZ.pdb")
model = session.models[0]

# 1. What hetero residues (ligands, excluding water) are present, and which chain are they assigned to?
hets = [r for r in model.residues if not r.polymer_type and r.name != "HOH"]
print("--- Non-polymer, non-water (ligand) residues ---")
for r in hets:
    print(f"  chain={r.chain_id} number={r.number} name={r.name} natoms={len(r.atoms)}")

# 2. distance from R98 (chain A) to nearest atom of each hetero residue
res_by_number = {r.number: r for r in model.residues if r.chain_id == "A" and r.polymer_type}
r98 = res_by_number.get(98)
r98_atoms = np.array([a.coord for a in r98.atoms])
print("\n--- R98 (chain A) distance to each hetero group's nearest atom ---")
for r in hets:
    het_atoms = np.array([a.coord for a in r.atoms])
    dists = np.linalg.norm(r98_atoms[:, None, :] - het_atoms[None, :, :], axis=-1)
    print(f"  {r.chain_id}/{r.name}{r.number}: min dist = {dists.min():.2f} A")

run(session, "usage measure sasa")

run(session, "exit")
