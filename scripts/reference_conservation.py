"""Reference-indexed conservation metrics from protein sequences."""

import math
from collections import Counter


CODON_TABLE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}


def translate_dna(seq):
    seq = "".join(c for c in seq.upper().replace("U", "T") if c in "ACGTN")
    protein = []
    for idx in range(0, len(seq) - 2, 3):
        aa = CODON_TABLE.get(seq[idx:idx + 3], "X")
        if aa == "*":
            break
        protein.append(aa)
    return "".join(protein)


def _align(a, b):
    match = 2
    mismatch = -1
    gap = -2
    m, n = len(a), len(b)
    score = [[0] * (n + 1) for _ in range(m + 1)]
    trace = [[None] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        score[i][0] = i * gap
        trace[i][0] = "up"
    for j in range(1, n + 1):
        score[0][j] = j * gap
        trace[0][j] = "left"
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            diag = score[i - 1][j - 1] + (match if a[i - 1] == b[j - 1] else mismatch)
            up = score[i - 1][j] + gap
            left = score[i][j - 1] + gap
            best = max(diag, up, left)
            score[i][j] = best
            trace[i][j] = "diag" if best == diag else "up" if best == up else "left"

    aligned_a = []
    aligned_b = []
    i, j = m, n
    while i > 0 or j > 0:
        step = trace[i][j]
        if step == "diag":
            aligned_a.append(a[i - 1])
            aligned_b.append(b[j - 1])
            i -= 1
            j -= 1
        elif step == "up":
            aligned_a.append(a[i - 1])
            aligned_b.append("-")
            i -= 1
        else:
            aligned_a.append("-")
            aligned_b.append(b[j - 1])
            j -= 1
    return "".join(reversed(aligned_a)), "".join(reversed(aligned_b))


def _shannon_entropy(chars):
    residues = [c for c in chars if c != "-"]
    if not residues:
        return None
    counts = Counter(residues)
    total = len(residues)
    entropy = -sum((count / total) * math.log2(count / total) for count in counts.values())
    return 0.0 if abs(entropy) < 1e-12 else entropy


def conservation_rows(records, reference_id):
    reference = records[reference_id]
    columns = [[residue] for residue in reference]
    for seq_id, sequence in records.items():
        if seq_id == reference_id:
            continue
        aligned_ref, aligned_seq = _align(reference, sequence)
        ref_pos = 0
        for ref_char, seq_char in zip(aligned_ref, aligned_seq):
            if ref_char != "-":
                ref_pos += 1
                columns[ref_pos - 1].append(seq_char)

    max_entropy = math.log2(20)
    rows = []
    for idx, column in enumerate(columns, start=1):
        ent = _shannon_entropy(column)
        rows.append({
            "position": idx,
            "residue": reference[idx - 1],
            "shannon_entropy": ent,
            "normalized_conservation": 1 - (ent / max_entropy) if ent is not None else None,
            "n_species_present": sum(1 for char in column if char != "-"),
            "n_species_total": len(records),
        })
    return rows
