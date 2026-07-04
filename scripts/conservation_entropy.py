"""
Shannon-entropy conservation score from the MAFFT alignment of 10 diverse
plant PPO2 orthologs (data/processed/ppo2_conservation_aligned.fasta).
Per the panel review fix: compute conservation locally from our own MSA
rather than depending on ConSurf's single-submission web tool.

Entropy is computed per alignment column (gaps excluded from the frequency
calculation), then mapped back to tobacco (1SEZ) residue numbering using
the tobacco sequence's own positions within the alignment - this makes the
conservation score directly indexable by the same tobacco-equivalent
numbering already used for distance/SASA in ppo_1sez_distance_sasa.csv.
"""
import math
from collections import Counter
from Bio import SeqIO
import csv

records = list(SeqIO.parse("data/processed/ppo2_conservation_aligned.fasta", "fasta"))
seqs = {r.id: str(r.seq) for r in records}
tobacco_id = [k for k in seqs if k.startswith("1SEZ")][0]
tobacco_aligned = seqs[tobacco_id]
alignment_length = len(tobacco_aligned)
n_seqs = len(seqs)

def shannon_entropy(column):
    residues = [c for c in column if c != "-"]
    if not residues:
        return None
    counts = Counter(residues)
    total = len(residues)
    ent = -sum((c / total) * math.log2(c / total) for c in counts.values())
    return ent

max_entropy = math.log2(20)  # 20 amino acids, theoretical max

rows = []
tobacco_pos = 0
for col_idx in range(alignment_length):
    column = [seqs[k][col_idx] for k in seqs]
    ent = shannon_entropy(column)
    tob_char = tobacco_aligned[col_idx]
    if tob_char != "-":
        tobacco_pos += 1
        n_present = sum(1 for c in column if c != "-")
        rows.append({
            "tobacco_position": tobacco_pos,
            "tobacco_residue": tob_char,
            "shannon_entropy": ent,
            "normalized_conservation": 1 - (ent / max_entropy) if ent is not None else None,
            "n_species_present": n_present,
            "n_species_total": n_seqs,
        })

with open("data/processed/ppo_conservation_entropy.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["tobacco_position", "tobacco_residue", "shannon_entropy", "normalized_conservation", "n_species_present", "n_species_total"])
    writer.writeheader()
    writer.writerows(rows)

print(f"wrote {len(rows)} tobacco-numbered positions from {n_seqs} species, alignment length {alignment_length}")

# Validation gate positions
CHECK = {"deltaG210": 178, "V361A": 332, "G399A": 370, "R98(core)": 98}
by_pos = {r["tobacco_position"]: r for r in rows}
print("\n--- Conservation at mutation positions ---")
for label, pos in CHECK.items():
    r = by_pos.get(pos)
    if r:
        print(f"{label} (tobacco {pos}, {r['tobacco_residue']}): entropy={r['shannon_entropy']:.3f}, "
              f"conservation={r['normalized_conservation']:.3f}, present in {r['n_species_present']}/{r['n_species_total']} species")
    else:
        print(f"{label}: not found")
