"""
ACCase static distance/SASA metrics on 1UYS.

1UYS is the yeast ACCase carboxyltransferase domain bound to haloxyfop (H1L).
The biological dimer used here is chains B+C, matching the dimer explicitly used
in Delye et al. 2005's ACCase structural interpretation.
"""

import bisect
import csv
import math
from pathlib import Path

try:
    from scripts.pdb_static_metrics import parse_pdb, residue_sasa
    from scripts.reference_conservation import _align
except ImportError:
    from pdb_static_metrics import parse_pdb, residue_sasa
    from reference_conservation import _align


PDB_PATH = Path("data/raw/1UYS.pdb")
AJ_FASTA = Path("data/raw/ACCase_Amyosuroides_AJ310767.fasta")
PDB_FASTA = Path("data/raw/1UYS.fasta")
OUTPUT_PATH = Path("data/processed/accase_1uys_distance_sasa.csv")

PDB_CHAIN_IDS = {"B", "C"}
PDB_SEQUENCE_START = 1482
BLACKGRASS_CT_START = 1639
BLACKGRASS_CT_END = 2204
LIGAND_NAMES = {"H1L"}
CONTACT_CUTOFF_A = 4.5
# ACCase is run on a full B+C dimer, so the local fallback uses a lighter
# sphere sample than the smaller single-chain targets.
SASA_POINTS = 60

CHECK_POSITIONS = {
    "Ile1781Leu": ("C", 1781),
    "Trp2027Cys": ("B", 2027),
    "Ile2041Asn": ("B", 2041),
    "Asp2078Gly": ("B", 2078),
    "Cys2088Arg": ("B", 2088),
    "Gly2096Ala": ("B", 2096),
}


def read_fasta_sequence(path):
    seq = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            if not line.startswith(">"):
                seq.append(line.strip())
    return "".join(seq)


def blackgrass_to_pdb_map():
    blackgrass = read_fasta_sequence(AJ_FASTA)
    pdb = read_fasta_sequence(PDB_FASTA).replace("X", "M")
    blackgrass_ct = blackgrass[BLACKGRASS_CT_START - 1:BLACKGRASS_CT_END]
    aligned_bg, aligned_pdb = _align(blackgrass_ct, pdb)

    bg_idx = 0
    pdb_idx = 0
    mapping = {}
    for bg_char, pdb_char in zip(aligned_bg, aligned_pdb):
        if bg_char != "-":
            bg_idx += 1
        if pdb_char != "-":
            pdb_idx += 1
        if bg_char != "-" and pdb_char != "-":
            bg_pos = BLACKGRASS_CT_START + bg_idx - 1
            pdb_pos = PDB_SEQUENCE_START + pdb_idx - 1
            mapping[bg_pos] = pdb_pos
    return mapping


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
    lig_atoms = [
        atom for atom in atoms
        if atom.chain_id in PDB_CHAIN_IDS and atom.residue_name in LIGAND_NAMES
    ]
    if not lig_atoms:
        raise ValueError(f"No {sorted(LIGAND_NAMES)} ligand atoms found in chains {sorted(PDB_CHAIN_IDS)}")

    core = set()
    for atom in atoms:
        if not atom.is_protein or atom.chain_id not in PDB_CHAIN_IDS:
            continue
        if any(distance(atom.coord, lig.coord) <= CONTACT_CUTOFF_A for lig in lig_atoms):
            core.add((atom.chain_id, atom.residue_number))
    return sorted(core)


def distance_rows(coords, core_positions):
    core_positions = set(core_positions)
    core_coords = {key: coords[key] for key in core_positions if key in coords}
    if not core_coords:
        raise ValueError("No active-site core positions were found in residue coordinates")

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
    core = ligand_contact_core_by_chain(dimer_atoms)
    bg_to_pdb = blackgrass_to_pdb_map()
    pdb_to_bg = {pdb_pos: bg_pos for bg_pos, pdb_pos in bg_to_pdb.items()}

    rows = distance_rows(coords, core)
    for row in rows:
        key = (row["chain_id"], row["pdb_position"])
        row["residue_name"] = names[key]
        row["blackgrass_position"] = pdb_to_bg.get(row["pdb_position"])
        row["sasa_A2"] = sasa.get(key)

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "chain_id",
            "pdb_position",
            "blackgrass_position",
            "residue_name",
            "in_active_site_core",
            "distance_to_active_site_core_A",
            "distance_to_nearest_other_core_residue_A",
            "sasa_A2",
            "percentile_rank_distance_to_core",
        ])
        writer.writeheader()
        writer.writerows(rows)

    by_key = {(row["chain_id"], row["blackgrass_position"]): row for row in rows}
    print(f"Active-site core from {CONTACT_CUTOFF_A} A contacts to {sorted(LIGAND_NAMES)}: {len(core)} residues")
    print(f"wrote {len(rows)} chain-residue rows to {OUTPUT_PATH}")
    print("\n--- ACCase mutation-position check ---")
    for mutation_id, key in CHECK_POSITIONS.items():
        row = by_key[key]
        print(
            f"{mutation_id}: chain={row['chain_id']}, pdb={row['pdb_position']}, "
            f"blackgrass={row['blackgrass_position']}, residue={row['residue_name']}, "
            f"in_core={row['in_active_site_core']}, "
            f"dist_to_core={row['distance_to_active_site_core_A']:.2f} A, "
            f"percentile={row['percentile_rank_distance_to_core']:.1f}, "
            f"SASA={row['sasa_A2']:.1f} A^2"
        )


if __name__ == "__main__":
    main()
