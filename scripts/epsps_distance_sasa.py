"""
EPSPS static distance/SASA metrics on 8UMJ.

For each chain-A residue of maize EPSPS complexed with glyphosate (GPJ) and
shikimate-3-phosphate (S3P), computes the standardized cross-enzyme metrics:
  - CA-CA distance to the ligand-contact active-site core
  - CA-CA distance to the nearest other core residue
  - percentile rank of distance-to-core within the chain
  - per-residue SASA, using a local Shrake-Rupley implementation because
    ChimeraX is not always available in headless Codex sessions.

Writes data/processed/epsps_8umj_distance_sasa.csv
"""
import csv

try:
    from scripts.active_site_metrics import distance_rows
    from scripts.pdb_static_metrics import ligand_contact_core, parse_pdb, residue_ca_coords, residue_sasa
except ImportError:
    from active_site_metrics import distance_rows
    from pdb_static_metrics import ligand_contact_core, parse_pdb, residue_ca_coords, residue_sasa

PDB_PATH = "data/raw/8UMJ.pdb"
OUTPUT_PATH = "data/processed/epsps_8umj_distance_sasa.csv"
CHAIN_ID = "A"
LIGAND_NAMES = {"GPJ", "S3P"}
CONTACT_CUTOFF_A = 4.5
SASA_POINTS = 240
CHECK_POSITIONS = {"Pro106Ser mature numbering (8UMJ residue 106)": 106}


def main():
    atoms = parse_pdb(PDB_PATH)
    core_numbers = ligand_contact_core(atoms, CHAIN_ID, LIGAND_NAMES, cutoff=CONTACT_CUTOFF_A)
    residue_coords, residue_names = residue_ca_coords(atoms, CHAIN_ID)
    sasa_by_residue = residue_sasa(
        [atom for atom in atoms if atom.chain_id == CHAIN_ID],
        n_sphere_points=SASA_POINTS,
    )

    rows = distance_rows(residue_coords, core_numbers)
    for row in rows:
        pos = row["position"]
        row["residue_name"] = residue_names[pos]
        row["sasa_A2"] = sasa_by_residue.get((CHAIN_ID, pos))

    with open(OUTPUT_PATH, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "position",
            "residue_name",
            "in_active_site_core",
            "distance_to_active_site_core_A",
            "distance_to_nearest_other_core_residue_A",
            "sasa_A2",
            "percentile_rank_distance_to_core",
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Active-site core from {CONTACT_CUTOFF_A} A contacts to {sorted(LIGAND_NAMES)}: {core_numbers}")
    print(f"wrote {len(rows)} residues to {OUTPUT_PATH}")
    by_pos = {row["position"]: row for row in rows}
    print("\n--- EPSPS mutation-position check ---")
    for label, pos in CHECK_POSITIONS.items():
        row = by_pos.get(pos)
        if row:
            print(
                f"{label}: residue={row['residue_name']}, in_core={row['in_active_site_core']}, "
                f"dist_to_core={row['distance_to_active_site_core_A']:.2f} A, "
                f"dist_to_other_core={row['distance_to_nearest_other_core_residue_A']:.2f} A, "
                f"percentile={row['percentile_rank_distance_to_core']:.1f}, "
                f"SASA={row['sasa_A2']:.1f} A^2"
            )


if __name__ == "__main__":
    main()
