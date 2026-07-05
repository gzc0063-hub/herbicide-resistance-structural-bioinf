"""
ACCase static distance/SASA metrics on the SWISS-MODEL weed CT-domain dimer.

The SWISS-MODEL 1UYS homomer model preserves the black-grass AJ310767 CT-domain
sequence and dimer geometry, but the server excluded H1L ligand coordinates.
Therefore the active-site core is transferred from the existing 1UYS H1L-contact
metric file by black-grass residue number.
"""

import bisect
import csv
import math
from pathlib import Path

try:
    from scripts.pdb_static_metrics import parse_pdb, residue_sasa
    from scripts.rsa import add_rsa_to_csv
except ImportError:
    from pdb_static_metrics import parse_pdb, residue_sasa
    from rsa import add_rsa_to_csv


PDB_PATH = Path("data/raw/ACCase_Alopecurus_AJ310767_CTdomain_SWISSMODEL_1UYS_homomer.pdb")
TEMPLATE_METRIC_PATH = Path("data/processed/accase_1uys_distance_sasa.csv")
OUTPUT_PATH = Path("data/processed/accase_swissmodel_1uys_distance_sasa.csv")

MODEL_CHAIN_IDS = {"A", "B"}
BLACKGRASS_CT_START = 1639
CONTACT_CUTOFF_A = 4.5
SASA_POINTS = 60

CHECK_POSITIONS = {
    "Ile1781Leu": ("A", 1781),
    "Trp2027Cys": ("B", 2027),
    "Ile2041Asn": ("B", 2041),
    "Asp2078Gly": ("B", 2078),
    "Cys2088Arg": ("B", 2088),
    "Gly2096Ala": ("B", 2096),
}


def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def model_position_to_blackgrass(model_position: int) -> int:
    return BLACKGRASS_CT_START + model_position - 1


def transferred_core_positions() -> set[int]:
    """Return black-grass positions whose 1UYS template residues contact H1L."""
    with TEMPLATE_METRIC_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {
        int(row["blackgrass_position"])
        for row in rows
        if row["blackgrass_position"] and row["in_active_site_core"] == "True"
    }


def residue_ca_coords_by_chain(atoms):
    coords = {}
    names = {}
    for atom in atoms:
        if atom.is_protein and atom.chain_id in MODEL_CHAIN_IDS and atom.name == "CA":
            key = (atom.chain_id, atom.residue_number)
            coords[key] = atom.coord
            names[key] = atom.residue_name
    return coords, names


def distance_rows(coords, core_keys):
    core_coords = {key: coords[key] for key in core_keys if key in coords}
    if not core_coords:
        raise ValueError("No transferred active-site core positions were found in model coordinates")

    rows = []
    for key, coord in sorted(coords.items()):
        blackgrass_position = model_position_to_blackgrass(key[1])
        in_core = key in core_coords
        distance_to_core = 0.0 if in_core else min(distance(coord, c) for c in core_coords.values())
        other_core = [c for core_key, c in core_coords.items() if core_key != key]
        distance_to_other = min(distance(coord, c) for c in other_core) if other_core else None
        rows.append({
            "chain_id": key[0],
            "pdb_position": key[1],
            "blackgrass_position": blackgrass_position,
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
    model_atoms = [
        atom for atom in atoms
        if atom.chain_id in MODEL_CHAIN_IDS and atom.residue_name != "HOH"
    ]
    coords, names = residue_ca_coords_by_chain(model_atoms)
    sasa = residue_sasa(model_atoms, n_sphere_points=SASA_POINTS)

    core_blackgrass_positions = transferred_core_positions()
    core_keys = {
        key for key in coords
        if model_position_to_blackgrass(key[1]) in core_blackgrass_positions
    }

    rows = distance_rows(coords, core_keys)
    for row in rows:
        key = (row["chain_id"], row["pdb_position"])
        row["residue_name"] = names[key]
        row["sasa_A2"] = sasa.get(key)

    fieldnames = [
        "chain_id",
        "pdb_position",
        "blackgrass_position",
        "residue_name",
        "in_active_site_core",
        "distance_to_active_site_core_A",
        "distance_to_nearest_other_core_residue_A",
        "sasa_A2",
        "percentile_rank_distance_to_core",
    ]
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    add_rsa_to_csv(OUTPUT_PATH)

    by_key = {(row["chain_id"], row["blackgrass_position"]): row for row in rows}
    print(
        f"Transferred active-site core from {CONTACT_CUTOFF_A} A 1UYS-H1L contacts: "
        f"{len(core_blackgrass_positions)} black-grass positions, {len(core_keys)} model chain-residues"
    )
    print(f"wrote {len(rows)} chain-residue rows to {OUTPUT_PATH}")
    print("\n--- ACCase SWISS-MODEL mutation-position check ---")
    for mutation_id, key in CHECK_POSITIONS.items():
        row = by_key[key]
        print(
            f"{mutation_id}: chain={row['chain_id']}, model={row['pdb_position']}, "
            f"blackgrass={row['blackgrass_position']}, residue={row['residue_name']}, "
            f"in_core={row['in_active_site_core']}, "
            f"dist_to_core={row['distance_to_active_site_core_A']:.2f} A, "
            f"percentile={row['percentile_rank_distance_to_core']:.1f}, "
            f"SASA={row['sasa_A2']:.1f} A^2"
        )


if __name__ == "__main__":
    main()
