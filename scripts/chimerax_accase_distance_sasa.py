"""
Run inside ChimeraX:
  ChimeraX-console.exe --nogui --script scripts/chimerax_accase_distance_sasa.py

For the 1UYS yeast ACCase CT-domain B+C biological dimer, computes static
distance/SASA metrics with active-site core defined from 4.5 A contacts to bound
haloxyfop (H1L).
"""

import bisect
import csv
import math
from pathlib import Path
import sys

from chimerax.core.commands import run
import numpy as np

sys.path.insert(0, str(Path("scripts").resolve()))
from reference_conservation import _align  # noqa: E402

session = session  # noqa: F821

PDB_PATH = Path("data/raw/1UYS.pdb")
AJ_FASTA = Path("data/raw/ACCase_Alopecurus_AJ310767_reference.fasta")
PDB_FASTA = Path("data/raw/1UYS.fasta")
OUTPUT_PATH = Path("data/processed/accase_1uys_distance_sasa.csv")

PDB_CHAIN_IDS = {"B", "C"}
PDB_SEQUENCE_START = 1482
BLACKGRASS_CT_START = 1639
BLACKGRASS_CT_END = 2204
CONTACT_CUTOFF_A = 4.5

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
    aligned_bg, aligned_pdb = _align(blackgrass[BLACKGRASS_CT_START - 1:BLACKGRASS_CT_END], pdb)
    bg_idx = 0
    pdb_idx = 0
    mapping = {}
    for bg_char, pdb_char in zip(aligned_bg, aligned_pdb):
        if bg_char != "-":
            bg_idx += 1
        if pdb_char != "-":
            pdb_idx += 1
        if bg_char != "-" and pdb_char != "-":
            mapping[BLACKGRASS_CT_START + bg_idx - 1] = PDB_SEQUENCE_START + pdb_idx - 1
    return mapping


def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def percentile_distance_rows(residue_coords, core_keys):
    core_coords = {key: residue_coords[key] for key in core_keys if key in residue_coords}
    if not core_coords:
        raise ValueError("No active-site core residues were found in CA coordinates")

    rows = []
    for key, coord in sorted(residue_coords.items()):
        in_core = key in core_coords
        distance_to_core = 0.0 if in_core else min(distance(coord, c) for c in core_coords.values())
        other_core = [c for core_key, c in core_coords.items() if core_key != key]
        rows.append({
            "chain_id": key[0],
            "pdb_position": key[1],
            "in_active_site_core": in_core,
            "distance_to_active_site_core_A": distance_to_core,
            "distance_to_nearest_other_core_residue_A": min(distance(coord, c) for c in other_core) if other_core else None,
        })

    dists = sorted(row["distance_to_active_site_core_A"] for row in rows)
    for row in rows:
        row["percentile_rank_distance_to_core"] = 100.0 * bisect.bisect_right(
            dists, row["distance_to_active_site_core_A"]
        ) / len(dists)
    return rows


run(session, f"open {PDB_PATH}")
model = session.models[0]

# Keep the B+C biological dimer only. Chain A is a separate crystallographic
# dimer representative in the deposited coordinates.
run(session, "delete /A")

ligand_residues = [
    r for r in model.residues
    if r.chain_id in PDB_CHAIN_IDS and r.name == "H1L"
]
ligand_atoms = np.array([a.coord for r in ligand_residues for a in r.atoms])
if ligand_atoms.size == 0:
    raise ValueError("No H1L atoms found in chains B/C")

core_keys = set()
residue_coords = {}
residue_names = {}
for residue in model.residues:
    if residue.chain_id not in PDB_CHAIN_IDS or residue.name in {"H1L", "HOH"}:
        continue
    ca = residue.find_atom("CA")
    if ca is None:
        continue
    key = (residue.chain_id, residue.number)
    residue_coords[key] = tuple(float(x) for x in ca.coord)
    residue_names[key] = residue.name

    atom_coords = np.array([a.coord for a in residue.atoms])
    if np.linalg.norm(atom_coords[:, None, :] - ligand_atoms[None, :, :], axis=-1).min() <= CONTACT_CUTOFF_A:
        core_keys.add(key)

run(session, "measure sasa #1")
sasa_by_key = {}
for residue in model.residues:
    key = (residue.chain_id, residue.number)
    if key in residue_coords:
        sasa_by_key[key] = sum(a.area for a in residue.atoms if a.area is not None)

bg_to_pdb = blackgrass_to_pdb_map()
pdb_to_bg = {pdb_pos: bg_pos for bg_pos, pdb_pos in bg_to_pdb.items()}

rows = percentile_distance_rows(residue_coords, core_keys)
for row in rows:
    key = (row["chain_id"], row["pdb_position"])
    row["blackgrass_position"] = pdb_to_bg.get(row["pdb_position"])
    row["residue_name"] = residue_names[key]
    row["sasa_A2"] = sasa_by_key.get(key)

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

print(f"Active-site core from {CONTACT_CUTOFF_A} A contacts to H1L: {len(core_keys)} residues")
print(f"wrote {len(rows)} chain-residue rows to {OUTPUT_PATH}")
print("\n--- ACCase mutation-position check ---")
by_key = {(row["chain_id"], row["blackgrass_position"]): row for row in rows}
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

run(session, "exit")
