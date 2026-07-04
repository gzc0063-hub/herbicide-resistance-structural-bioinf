"""
Run inside ChimeraX (headless): ChimeraX --nogui --script chimerax_als_distance_sasa.py

For each chain-A residue of 1Z8N (Arabidopsis AHAS + imazaquin), computes:
  - min CA-CA distance to the active-site core, defined directly from the
    structure as every residue within 4.5 A of either bound imazaquin (1IQ)
    copy - no need for a McCourt-et-al.-2006-style literature core list.
  - percentile rank of that distance within chain A's own distribution
  - per-residue SASA, computed on the full author-determined tetrameric
    biological assembly (assembly 1) for correct oligomeric context,
    same fix applied to PPO's dimer in Phase 1.
Writes data/processed/als_1z8n_distance_sasa.csv
"""
from chimerax.core.commands import run
import numpy as np
import csv
import bisect

session = session  # noqa: F821

run(session, "open 1z8n")
m1 = session.models[0]

# Active-site core: union of residues within 4.5 A of either 1IQ copy
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
core_numbers = sorted(core_numbers)
print("Active-site core (chain A residue numbers, contacts to either 1IQ copy):", core_numbers)

res_by_number = {r.number: r for r in m1.residues if r.chain_id == "A" and r.polymer_type == 1}
core_ca = {}
for num in core_numbers:
    r = res_by_number.get(num)
    ca = r.find_atom("CA") if r else None
    if ca is not None:
        core_ca[num] = ca.coord

def min_dist_to_core(ca_coord, exclude=None):
    coords = [c for n, c in core_ca.items() if n != exclude]
    return min(float(np.linalg.norm(np.asarray(ca_coord) - np.asarray(c))) for c in coords)

# Distances (single copy is enough - active site is intramolecular per the contacts found)
dist_rows = []
for num, r in sorted(res_by_number.items()):
    ca = r.find_atom("CA")
    if ca is None:
        continue
    dist = min_dist_to_core(ca.coord, exclude=num)
    dist_rows.append({"position": num, "residue_name": r.name, "min_dist_to_active_site_core_A": dist})

dists_sorted = sorted(r["min_dist_to_active_site_core_A"] for r in dist_rows)
n = len(dists_sorted)
for r in dist_rows:
    idx = bisect.bisect_right(dists_sorted, r["min_dist_to_active_site_core_A"])
    r["percentile_rank_distance"] = 100.0 * idx / n

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
    writer = csv.DictWriter(f, fieldnames=["position", "residue_name", "min_dist_to_active_site_core_A", "sasa_A2", "percentile_rank_distance"])
    writer.writeheader()
    writer.writerows(dist_rows)

print(f"wrote {len(dist_rows)} residues to data/processed/als_1z8n_distance_sasa.csv")

by_pos = {r["position"]: r for r in dist_rows}
print("\n--- Validation check: Trp574 and Ser653 ---")
for label, pos in [("Trp574", 574), ("Ser653", 653)]:
    r = by_pos.get(pos)
    if r:
        print(f"{label}: dist={r['min_dist_to_active_site_core_A']:.2f} A, percentile={r['percentile_rank_distance']:.1f}, SASA={r['sasa_A2']:.1f} A^2, in_core={pos in core_numbers}")

run(session, "exit")
