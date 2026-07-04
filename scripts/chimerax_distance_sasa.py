"""
Run inside ChimeraX (headless): ChimeraX --nogui --script chimerax_distance_sasa.py

For each residue in 1SEZ chain A, computes:
  - CA-CA distance to the Heinemann et al. 2007 active-site core
    (tobacco numbering: Arg98, Phe392, Leu356, Leu372). Core residues
    score 0 A for this metric.
  - CA-CA distance to the nearest other active-site core residue
  - percentile rank of that distance within the chain's own distribution
    (per-panel-review fix: raw Angstroms aren't cross-enzyme comparable,
    percentile rank is)
  - per-residue solvent accessible surface area (SASA)
Writes results to data/processed/ppo_1sez_distance_sasa.csv
"""
from chimerax.core.commands import run
import csv

try:
    from scripts.active_site_metrics import distance_rows
except ImportError:
    from active_site_metrics import distance_rows

session = session  # noqa: F821  (ChimeraX injects this)

run(session, "open data/raw/1SEZ.pdb")
# Keep both chains for the SASA calculation - PPO is a biological homodimer
# (Dayan et al. 2010), so deleting chain B would overestimate solvent exposure
# at the dimer interface. Distance-to-active-site and reported per-residue rows
# are restricted to chain A below; chain B stays present only to give SASA the
# correct biological context.
run(session, "measure sasa")

ACTIVE_SITE_CORE = [98, 392, 356, 372]  # Heinemann et al. 2007, tobacco numbering

model = session.models[0]
residues = model.residues
res_by_number = {r.number: r for r in residues if r.chain_id == "A"}

residue_coords = {}
residue_names = {}
sasa_by_pos = {}
for num, r in sorted(res_by_number.items()):
    ca = r.find_atom("CA")
    if ca is None:
        continue
    residue_coords[num] = tuple(float(x) for x in ca.coord)
    residue_names[num] = r.name
    sasa_by_pos[num] = sum(a.area for a in r.atoms if a.area is not None)

rows = distance_rows(residue_coords, ACTIVE_SITE_CORE)
for r in rows:
    r["tobacco_position"] = r.pop("position")
    r["residue_name"] = residue_names[r["tobacco_position"]]
    r["sasa_A2"] = sasa_by_pos[r["tobacco_position"]]

with open("data/processed/ppo_1sez_distance_sasa.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "tobacco_position",
        "residue_name",
        "in_active_site_core",
        "distance_to_active_site_core_A",
        "distance_to_nearest_other_core_residue_A",
        "sasa_A2",
        "percentile_rank_distance_to_core",
    ])
    writer.writeheader()
    writer.writerows(rows)

print(f"wrote {len(rows)} residues to data/processed/ppo_1sez_distance_sasa.csv")

# Validation gate: check the four mutation positions (tobacco-equivalent numbering)
CHECK_POSITIONS = {"deltaG210 (tobacco 178)": 178, "V361A (tobacco 332)": 332, "G399A (tobacco 370)": 370, "R98G/R98M (tobacco 98, core itself)": 98}
by_num = {r["tobacco_position"]: r for r in rows}
print("\n--- Validation gate check ---")
for label, num in CHECK_POSITIONS.items():
    r = by_num.get(num)
    if r:
        print(f"{label}: in_core={r['in_active_site_core']}, dist_to_core={r['distance_to_active_site_core_A']:.2f} A, "
              f"dist_to_other_core={r['distance_to_nearest_other_core_residue_A']:.2f} A, "
              f"percentile={r['percentile_rank_distance_to_core']:.1f}, SASA={r['sasa_A2']:.1f} A^2")
    else:
        print(f"{label}: NOT FOUND at tobacco position {num}")

run(session, "exit")
