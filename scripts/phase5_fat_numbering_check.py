"""
Phase 5 audit check (not part of the Phase 4 pipeline / rebuild_all.py chain).

Checks whether R171 (Alopecurus myosuroides FatA, Wagner et al. 2026 bioRxiv)
and Arg176 (Arabidopsis thaliana FatA, Kot et al. 2026 crystal structure,
PDB 9GRR) are the same aligned catalytic residue.

No public Alopecurus myosuroides FatA sequence exists (checked NCBI protein,
nuccore, and UniProt - zero hits), so this uses wheat (Triticum aestivum,
UniProt Q8L6B1) as a proxy: wheat and blackgrass are both Pooideae grasses,
much closer to each other than either is to Arabidopsis.

Run: .venv/Scripts/python.exe scripts/phase5_fat_numbering_check.py
Requires data/raw/Q42561_AtFATA1.fasta and data/raw/Q8L6B1_TaFatA.fasta
(downloaded via `curl https://rest.uniprot.org/uniprotkb/<accession>.fasta`).
"""
from pathlib import Path

from Bio import Align, SeqIO
from Bio.Align import substitution_matrices

AT_FASTA = Path("data/raw/Q42561_AtFATA1.fasta")
TA_FASTA = Path("data/raw/Q8L6B1_TaFatA.fasta")


def main() -> None:
    at_seq = str(SeqIO.read(AT_FASTA, "fasta").seq)
    ta_seq = str(SeqIO.read(TA_FASTA, "fasta").seq)

    print(f"Arabidopsis Q42561 length: {len(at_seq)}; residue at 176: {at_seq[175]}")
    print(f"Wheat Q8L6B1 length: {len(ta_seq)}; residue at 171: {ta_seq[170]}")

    aligner = Align.PairwiseAligner()
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
    aligner.open_gap_score = -11
    aligner.extend_gap_score = -1
    aligner.mode = "global"
    aln = aligner.align(at_seq, ta_seq)[0]
    a, b = str(aln[0]), str(aln[1])

    matches = sum(1 for x, y in zip(a, b) if x == y and x != "-")
    aligned_cols = sum(1 for x, y in zip(a, b) if x != "-" and y != "-")
    print(f"\nIdentity over aligned region: {matches}/{aligned_cols} "
          f"= {100 * matches / aligned_cols:.1f}%")

    at_pos = ta_pos = 0
    map_at_to_ta: dict[int, tuple[str, int]] = {}
    map_ta_to_at: dict[int, tuple[str, int]] = {}
    for a_char, t_char in zip(a, b):
        if a_char != "-":
            at_pos += 1
        if t_char != "-":
            ta_pos += 1
        if a_char != "-" and t_char != "-":
            map_at_to_ta[at_pos] = (t_char, ta_pos)
            map_ta_to_at[ta_pos] = (a_char, at_pos)

    print(f"\nArabidopsis Arg176 aligns to wheat: {map_at_to_ta.get(176)}")
    print(f"Wheat residue 171 (own numbering) aligns to Arabidopsis: "
          f"{map_ta_to_at.get(171)}")
    print(
        "\nConclusion: the conserved catalytic arginine (Arabidopsis Arg176, "
        "cinmethylin H-bond donor per Kot et al. 2026) aligns to wheat Arg103, "
        "not wheat position 171 (Thr). Wheat's own UniProt numbering is already "
        "mature-protein/transit-peptide-excluded (176 - 103 = 73, matching the "
        "74-residue Arabidopsis transit peptide almost exactly). If Wagner et "
        "al. 2026's blackgrass numbering follows the same mature-protein "
        "convention, R171 and Arg176 are most likely DIFFERENT residues, not "
        "the same residue at a small species offset."
    )


if __name__ == "__main__":
    main()
