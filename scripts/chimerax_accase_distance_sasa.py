"""
Run inside ChimeraX (headless): ChimeraX --nogui --script chimerax_accase_distance_sasa.py

For each chain-B residue of 1UYS (yeast ACCase CT domain + haloxyfop), computes:
  - min CA-CA distance to the active-site core, defined directly from the
    structure as every residue (chain B OR chain C) within 4.5 A of any bound
    haloxyfop (H1L) copy. Chains B+C are the real deposited biological dimer
    (REMARK 350 biomolecule 2, confirmed directly from the PDB file - no
    symmetry generation needed, unlike ALS's 1Z8N). Délye et al. 2005 used
    this same B/C chain pair as their homology-modeling template, confirming
    this is the correct functional pair, not assumed.
  - percentile rank of that distance within chain B's own distribution
  - per-residue SASA, computed on the B+C dimer as deposited (correct
    biological context directly, no assembly command needed this time)
Writes data/processed/accase_1uys_distance_sasa.csv

Learned from the ALS correction (DECISION_LOG #17): check cross-chain contacts
from the start, using consistent coordinates (both chains are in the same
asymmetric unit / same coordinate frame here, so plain atom.coord works for
both chains - no scene_coord issue, unlike ALS's symmetry-generated tetramer).
"""
from chimerax.core.commands import run
import numpy as np
import csv
import bisect

session = session  # noqa: F821

run(session, "open data/raw/1UYS.pdb")
m1 = session.models[0]

# Active-site core: union of B+C residues within 4.5 A of either bound haloxyfop (H1L) copy
lig_residues = [r for r in m1.residues if r.name == "H1L"]
print(f"Found {len(lig_residues)} haloxyfop (H1L) copies: {[(r.chain_id, r.number) for r in lig_residues]}")

core = set()  # (chain_id, number)
for lig in lig_residues:
    lig_atoms = np.array([a.coord for a in lig.atoms])
    for r in m1.residues:
        if r.polymer_type != 1 or r.chain_id not in ("B", "C"):
            continue
        prot_atoms = np.array([a.coord for a in r.atoms])
        d = np.linalg.norm(prot_atoms[:, None, :] - lig_atoms[None, :, :], axis=-1)
        if d.min() < 4.5:
            core.add((r.chain_id, r.number))

print("Active-site core (chain, residue number), contacts to either H1L copy:")
for c in sorted(core):
    print(" ", c)
n_chainB_core = sum(1 for c in core if c[0] == "B")
n_chainC_core = sum(1 for c in core if c[0] == "C")
print(f"chain B core residues: {n_chainB_core}, chain C core residues: {n_chainC_core}")

res_by_key = {(r.chain_id, r.number): r for r in m1.residues if r.polymer_type == 1 and r.chain_id in ("B", "C")}
core_ca = {}
for key in core:
    r = res_by_key.get(key)
    ca = r.find_atom("CA") if r else None
    if ca is not None:
        core_ca[key] = ca.coord

def min_dist_to_core(ca_coord, exclude=None):
    coords = [c for k, c in core_ca.items() if k != exclude]
    return min(float(np.linalg.norm(np.asarray(ca_coord) - np.asarray(c))) for c in coords)

# Report chain B residues only (chain C is symmetric/equivalent per Delye et al.)
chainB_residues = {r.number: r for r in m1.residues if r.chain_id == "B" and r.polymer_type == 1}
dist_rows = []
for num, r in sorted(chainB_residues.items()):
    ca = r.find_atom("CA")
    if ca is None:
        continue
    dist = min_dist_to_core(ca.coord, exclude=("B", num))
    dist_rows.append({"position": num, "residue_name": r.name, "min_dist_to_active_site_core_A": dist})

dists_sorted = sorted(r["min_dist_to_active_site_core_A"] for r in dist_rows)
n = len(dists_sorted)
for r in dist_rows:
    idx = bisect.bisect_right(dists_sorted, r["min_dist_to_active_site_core_A"])
    r["percentile_rank_distance"] = 100.0 * idx / n

# SASA on the B+C dimer as deposited (already the correct biological context)
run(session, "measure sasa /B,C")
sasa_by_pos = {}
for num, r in chainB_residues.items():
    sasa = sum(a.area for a in r.atoms if a.area is not None)
    sasa_by_pos[num] = sasa
for r in dist_rows:
    r["sasa_A2"] = sasa_by_pos.get(r["position"])

with open("data/processed/accase_1uys_distance_sasa.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["position", "residue_name", "min_dist_to_active_site_core_A", "sasa_A2", "percentile_rank_distance"])
    writer.writeheader()
    writer.writerows(dist_rows)

print(f"\nwrote {len(dist_rows)} chain-B residues to data/processed/accase_1uys_distance_sasa.csv")

# Validation check: Cys2088 equivalent position in this structure's own numbering
by_pos = {r["position"]: r for r in dist_rows}
print("\n--- Structure numbering check (residues 2085-2092, chain B) ---")
for num in range(2085, 2093):
    r = by_pos.get(num)
    if r:
        print(f"  {num}: {r['residue_name']}, dist={r['min_dist_to_active_site_core_A']:.2f} A, percentile={r['percentile_rank_distance']:.1f}, SASA={r['sasa_A2']:.1f} A^2, in_core={('B',num) in core}")

run(session, "exit")
