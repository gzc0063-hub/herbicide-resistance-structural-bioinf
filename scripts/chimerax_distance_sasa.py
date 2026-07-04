"""
Run inside ChimeraX (headless): ChimeraX --nogui --script chimerax_distance_sasa.py

For each residue in 1SEZ chain A, computes:
  - min CA-CA distance to the Heinemann et al. 2007 active-site core
    (tobacco numbering: Arg98, Phe392, Leu356, Leu372)
  - percentile rank of that distance within the chain's own distribution
    (per-panel-review fix: raw Angstroms aren't cross-enzyme comparable,
    percentile rank is)
  - per-residue solvent accessible surface area (SASA)
Writes results to data/processed/ppo_1sez_distance_sasa.csv
"""
from chimerax.core.commands import run
import csv
import numpy as np

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

core_ca = {}
for num in ACTIVE_SITE_CORE:
    r = res_by_number.get(num)
    if r is None:
        print(f"WARNING: active site residue {num} not found in structure")
        continue
    ca = r.find_atom("CA")
    if ca is None:
        print(f"WARNING: no CA atom for residue {num}")
        continue
    core_ca[num] = ca.coord

def min_dist_to_core(ca_coord):
    return min(float(np.linalg.norm(np.asarray(ca_coord) - np.asarray(c))) for c in core_ca.values())

rows = []
for num, r in sorted(res_by_number.items()):
    ca = r.find_atom("CA")
    if ca is None:
        continue
    dist = min_dist_to_core(ca.coord)
    sasa = sum(a.area for a in r.atoms if a.area is not None)
    rows.append({"tobacco_position": num, "residue_name": r.name, "min_dist_to_active_site_core_A": dist, "sasa_A2": sasa})

dists = sorted(r["min_dist_to_active_site_core_A"] for r in rows)
n = len(dists)
def percentile_rank(d):
    # fraction of residues with distance <= d (0 = closest, 100 = farthest)
    import bisect
    idx = bisect.bisect_right(dists, d)
    return 100.0 * idx / n

for r in rows:
    r["percentile_rank_distance"] = percentile_rank(r["min_dist_to_active_site_core_A"])

with open("data/processed/ppo_1sez_distance_sasa.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["tobacco_position", "residue_name", "min_dist_to_active_site_core_A", "sasa_A2", "percentile_rank_distance"])
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
        print(f"{label}: dist={r['min_dist_to_active_site_core_A']:.2f} A, percentile={r['percentile_rank_distance']:.1f}, SASA={r['sasa_A2']:.1f} A^2")
    else:
        print(f"{label}: NOT FOUND at tobacco position {num}")

run(session, "exit")
