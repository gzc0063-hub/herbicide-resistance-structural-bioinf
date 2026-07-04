"""
HPPD static active-site metrics on 5YWG.

5YWG is Arabidopsis thaliana HPPD complexed with mesotrione. The deposited
biological unit is a dimer with chains A+B, cobalt substituting for the catalytic
metal, and mesotrione as ligand 92L. This script intentionally writes a structural
active-site table, not a weed target-site mutation table, because the HPPD source
audit found no verified weed-evolved HPPD amino-acid substitution suitable for the
TSR validation-gate dataset.
"""

import bisect
import csv
import math
from pathlib import Path

try:
    from scripts.pdb_static_metrics import parse_pdb, residue_sasa
except ImportError:
    from pdb_static_metrics import parse_pdb, residue_sasa


PDB_PATH = Path("data/raw/5YWG.pdb")
OUTPUT_PATH = Path("data/processed/hppd_5ywg_active_site_metrics.csv")
PDB_CHAIN_IDS = {"A", "B"}
LIGAND_NAMES = {"92L", "CO"}
CONTACT_CUTOFF_A = 4.5
SASA_POINTS = 60


def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def residue_ca_coords_by_chain(atoms):
    coords = {}
    names = {}
    for atom in atoms:
        if atom.is_protein and atom.chain_id in PDB_CHAIN_IDS and atom.name == "CA":
            key = (atom.chain_id, atom.residue_number)
            coords[key] = atom.coord
            names[key] = atom.residue_name
    return coords, names


def ligand_contact_core_by_chain(atoms):
    ligand_atoms = [
        atom for atom in atoms
        if atom.chain_id in PDB_CHAIN_IDS and atom.residue_name in LIGAND_NAMES
    ]
    if not ligand_atoms:
        raise ValueError(f"No ligand/metal atoms found for {sorted(LIGAND_NAMES)}")

    core = set()
    nearest_ligand = {}
    for atom in atoms:
        if not atom.is_protein or atom.chain_id not in PDB_CHAIN_IDS:
            continue
        contacts = [
            (distance(atom.coord, ligand.coord), ligand.residue_name)
            for ligand in ligand_atoms
            if ligand.chain_id == atom.chain_id
        ]
        if not contacts:
            continue
        min_dist, ligand_name = min(contacts)
        if min_dist <= CONTACT_CUTOFF_A:
            key = (atom.chain_id, atom.residue_number)
            core.add(key)
            old = nearest_ligand.get(key)
            if old is None or min_dist < old[0]:
                nearest_ligand[key] = (min_dist, ligand_name)
    return sorted(core), nearest_ligand


def distance_rows(coords, core_positions):
    core_positions = set(core_positions)
    core_coords = {key: coords[key] for key in core_positions if key in coords}
    if not core_coords:
        raise ValueError("No HPPD active-site core positions were found")

    rows = []
    for key, coord in sorted(coords.items()):
        in_core = key in core_coords
        distance_to_core = 0.0 if in_core else min(distance(coord, c) for c in core_coords.values())
        other_core = [c for core_key, c in core_coords.items() if core_key != key]
        distance_to_other = min(distance(coord, c) for c in other_core) if other_core else None
        rows.append({
            "chain_id": key[0],
            "pdb_position": key[1],
            "in_active_site_core": in_core,
            "distance_to_active_site_core_A": distance_to_core,
            "distance_to_nearest_other_core_residue_A": distance_to_other,
        })

    dists = sorted(row["distance_to_active_site_core_A"] for row in rows)
    for row in rows:
        row["percentile_rank_distance_to_core"] = 100.0 * bisect.bisect_right(
            dists, row["distance_to_active_site_core_A"]
        ) / len(dists)
    return rows


def main():
    atoms = parse_pdb(PDB_PATH)
    dimer_atoms = [
        atom for atom in atoms
        if atom.chain_id in PDB_CHAIN_IDS and atom.residue_name != "HOH"
    ]
    coords, names = residue_ca_coords_by_chain(dimer_atoms)
    sasa = residue_sasa(dimer_atoms, n_sphere_points=SASA_POINTS)
    core, nearest_ligand = ligand_contact_core_by_chain(dimer_atoms)

    rows = distance_rows(coords, core)
    for row in rows:
        key = (row["chain_id"], row["pdb_position"])
        row["residue_name"] = names[key]
        row["sasa_A2"] = sasa.get(key)
        ligand_contact = nearest_ligand.get(key)
        row["nearest_core_ligand"] = ligand_contact[1] if ligand_contact else ""
        row["nearest_ligand_atom_distance_A"] = ligand_contact[0] if ligand_contact else ""

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "chain_id",
            "pdb_position",
            "residue_name",
            "in_active_site_core",
            "nearest_core_ligand",
            "nearest_ligand_atom_distance_A",
            "distance_to_active_site_core_A",
            "distance_to_nearest_other_core_residue_A",
            "sasa_A2",
            "percentile_rank_distance_to_core",
        ])
        writer.writeheader()
        writer.writerows(rows)

    by_chain = {}
    for chain_id, pos in core:
        by_chain.setdefault(chain_id, []).append(pos)
    print(
        f"Active-site core from {CONTACT_CUTOFF_A} A contacts to {sorted(LIGAND_NAMES)}: "
        f"{len(core)} chain-residue positions"
    )
    for chain_id in sorted(by_chain):
        print(f"chain {chain_id}: {by_chain[chain_id]}")
    print(f"wrote {len(rows)} chain-residue rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
