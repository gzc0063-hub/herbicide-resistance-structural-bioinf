"""
Shannon-entropy conservation for ACCase, mirroring conservation_entropy.py (PPO)
and als_conservation_entropy.py (ALS). Reference numbering: AJ310767 (black-grass),
the field-standard convention used throughout Delye et al. 2005 and Yu et al. 2007
- no offset needed at this step (that's only needed to map onto the yeast 1UYS
structure, done separately in accase_numbering_map.json).
"""
import math
from collections import Counter
from Bio import SeqIO
import csv

records = list(SeqIO.parse("data/processed/accase_conservation_aligned.fasta", "fasta"))
seqs = {r.id: str(r.seq) for r in records}
ref_id = [k for k in seqs if k.startswith("AJ310767")][0]
ref_aligned = seqs[ref_id]
n_seqs = len(seqs)

def shannon_entropy(column):
    residues = [c for c in column if c != "-"]
    if not residues:
        return None
    counts = Counter(residues)
    total = len(residues)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())

max_entropy = math.log2(20)

rows = []
ref_pos = 0
for col_idx in range(len(ref_aligned)):
    column = [seqs[k][col_idx] for k in seqs]
    ent = shannon_entropy(column)
    ref_char = ref_aligned[col_idx]
    if ref_char != "-":
        ref_pos += 1
        n_present = sum(1 for c in column if c != "-")
        rows.append({
            "position": ref_pos, "residue": ref_char, "shannon_entropy": ent,
            "normalized_conservation": 1 - (ent / max_entropy) if ent is not None else None,
            "n_species_present": n_present, "n_species_total": n_seqs,
        })

with open("data/processed/accase_conservation_entropy.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["position", "residue", "shannon_entropy", "normalized_conservation", "n_species_present", "n_species_total"])
    writer.writeheader()
    writer.writerows(rows)

print(f"wrote {len(rows)} positions from {n_seqs} species")
by_pos = {r["position"]: r for r in rows}
print("\n--- Conservation at Cys2088 (black-grass numbering) ---")
r = by_pos.get(2088)
if r:
    print(f"position 2088 ({r['residue']}): entropy={r['shannon_entropy']:.3f}, conservation={r['normalized_conservation']:.3f}, present in {r['n_species_present']}/{r['n_species_total']}")
