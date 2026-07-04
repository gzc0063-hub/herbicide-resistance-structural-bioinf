"""
Shannon-entropy conservation for ALS, mirroring scripts/conservation_entropy.py.

Reference numbering: Arabidopsis thaliana (KAL9831686.1), matching 1Z8N's own PDB
numbering and the literature convention directly. NOTE: Amaranthus palmeri
(KY781916) is NOT used as the reference column here, despite the paper's
substitutions being reported in "Arabidopsis-equivalent" numbers - KY781916 has a
1-residue indel upstream of position 574 relative to Arabidopsis (669 vs 670 aa),
so its own raw sequence position is offset by -1 (confirmed by direct alignment:
Arabidopsis pos 574/653 = Trp/Ser maps to KY781916 raw pos 573/652). Using
Arabidopsis as master avoids re-deriving that offset here.
"""
import math
from collections import Counter
from Bio import SeqIO
import csv

records = list(SeqIO.parse("data/processed/als_conservation_aligned.fasta", "fasta"))
seqs = {r.id: str(r.seq) for r in records}
ref_id = [k for k in seqs if k.startswith("KAL9831686")][0]
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

with open("data/processed/als_conservation_entropy.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["position", "residue", "shannon_entropy", "normalized_conservation", "n_species_present", "n_species_total"])
    writer.writeheader()
    writer.writerows(rows)

print(f"wrote {len(rows)} positions from {n_seqs} species")
by_pos = {r["position"]: r for r in rows}
print("\n--- Conservation at mutation positions ---")
for label, pos in [("Trp574", 574), ("Ser653", 653)]:
    r = by_pos.get(pos)
    if r:
        print(f"{label} ({r['residue']}): entropy={r['shannon_entropy']:.3f}, conservation={r['normalized_conservation']:.3f}, present in {r['n_species_present']}/{r['n_species_total']}")
