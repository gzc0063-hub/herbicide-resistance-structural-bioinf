"""
Run inside ChimeraX (headless): ChimeraX --nogui --script chimerax_als_distance_sasa.py

For each chain-A residue of 1Z8N (Arabidopsis AHAS + imazaquin), computes:
  - CA-CA distance to the active-site core, defined from residues within
    4.5 A of either bound imazaquin (1IQ) copy plus interface residues from
    the neighboring subunit that form the same binding pocket. Core residues
    score 0 A for this metric.
  - CA-CA distance to the nearest other active-site core residue, preserving the
    ALS pilot's within-core spacing metric as a separate column.
  - percentile rank of distance-to-core within chain A's own distribution
  - per-residue SASA, computed on the full author-determined tetrameric
    biological assembly (assembly 1) for correct oligomeric context,
    same fix applied to PPO's dimer in Phase 1.
Writes data/processed/als_1z8n_distance_sasa.csv
"""
from chimerax.core.commands import run
import numpy as np
import csv

try:
    from scripts.active_site_metrics import distance_rows
except ImportError:
    from active_site_metrics import distance_rows

session = session  # noqa: F821

run(session, "open data/raw/1Z8N.pdb")
m1 = session.models[0]

# Active-site core: union of same-chain residues within 4.5 A of either 1IQ
# copy plus the residue numbers contributed by the neighboring subunit at the
# AHAS dimer interface. The interface residues are recorded as chain-A residue
# numbers so all downstream outputs remain in the Arabidopsis/PDB convention.
lig_residues = [r for r in m1.residues if r.name == "1IQ"]
core_numbers = set()
for lig in lig_residues:
    lig_atoms = np.array([a.coord for a in lig.atoms])
    for r in m1.residues:
        if r.polymer_type != 1:
            continue
        prot_atoms = np.array([a.coord for a in r.atoms])
        d = np.linalg.norm(prot_atoms[:, None, :] - lig_atoms[None, :, :], axis=-1)
        if d.min() < 4.5:
            core_numbers.add(r.number)
interface_core_numbers = {121, 122, 168, 195, 196, 197, 199, 200, 206, 207, 256}
core_numbers |= interface_core_numbers
core_numbers = sorted(core_numbers)
print("Active-site core (chain A residue numbers, 1IQ contacts plus dimer-interface residues):", core_numbers)

res_by_number = {r.number: r for r in m1.residues if r.chain_id == "A" and r.polymer_type == 1}
residue_coords = {}
residue_names = {}
for num, r in sorted(res_by_number.items()):
    ca = r.find_atom("CA")
    if ca is None:
        continue
    residue_coords[num] = tuple(float(x) for x in ca.coord)
    residue_names[num] = r.name

dist_rows = distance_rows(residue_coords, core_numbers)
for r in dist_rows:
    r["residue_name"] = residue_names[r["position"]]

# SASA on the full biological tetramer (assembly 1), restricted to that assembly's atoms
run(session, "sym #1 assembly 1")
run(session, "measure sasa #2")
assembly_copy1 = [mm for mm in session.models if mm.id == (2, 1)][0]  # first copy in the tetramer
res_by_number_assembly = {r.number: r for r in assembly_copy1.residues if r.polymer_type == 1}

sasa_by_pos = {}
for num, r in res_by_number_assembly.items():
    sasa = sum(a.area for a in r.atoms if a.area is not None)
    sasa_by_pos[num] = sasa

for r in dist_rows:
    r["sasa_A2"] = sasa_by_pos.get(r["position"])

with open("data/processed/als_1z8n_distance_sasa.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "position",
        "residue_name",
        "in_active_site_core",
        "distance_to_active_site_core_A",
        "distance_to_nearest_other_core_residue_A",
        "sasa_A2",
        "percentile_rank_distance_to_core",
    ])
    writer.writeheader()
    writer.writerows(dist_rows)

print(f"wrote {len(dist_rows)} residues to data/processed/als_1z8n_distance_sasa.csv")

by_pos = {r["position"]: r for r in dist_rows}
print("\n--- Validation check: Trp574 and Ser653 ---")
for label, pos in [("Trp574", 574), ("Ser653", 653)]:
    r = by_pos.get(pos)
    if r:
        print(f"{label}: in_core={r['in_active_site_core']}, dist_to_core={r['distance_to_active_site_core_A']:.2f} A, "
              f"dist_to_other_core={r['distance_to_nearest_other_core_residue_A']:.2f} A, "
              f"percentile={r['percentile_rank_distance_to_core']:.1f}, SASA={r['sasa_A2']:.1f} A^2")

run(session, "exit")
