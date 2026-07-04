"""
Reference-indexed Shannon entropy conservation for EPSPS.

The reference is 8UMJ chain A / UniProt A0A1D6NVZ6_MAIZE so rows are directly
indexable by the same PDB residue numbering used in epsps_8umj_distance_sasa.csv.
"""

import csv
from pathlib import Path

try:
    from scripts.reference_conservation import conservation_rows, translate_dna
except ImportError:
    from reference_conservation import conservation_rows, translate_dna


OUTPUT_PANEL = Path("data/processed/epsps_conservation_set.fasta")
OUTPUT_ENTROPY = Path("data/processed/epsps_conservation_entropy.csv")
PANEL_FASTAS = {
    "8UMJ_A0A1D6NVZ6_Zea_mays_reference": Path("data/raw/8UMJ.fasta"),
    "P05466_Arabidopsis_thaliana": Path("data/raw/EPSPS_conservation_Arabidopsis_thaliana_P05466.fasta"),
    "P23981_Nicotiana_tabacum": Path("data/raw/EPSPS_conservation_Nicotiana_tabacum_P23981.fasta"),
    "I1JKP7_Glycine_max": Path("data/raw/EPSPS_conservation_Glycine_max_I1JKP7.fasta"),
    "A0A0N7KLH2_Oryza_sativa": Path("data/raw/EPSPS_conservation_Oryza_sativa_A0A0N7KLH2.fasta"),
    "P10748_Solanum_lycopersicum": Path("data/raw/EPSPS_conservation_Solanum_lycopersicum_P10748.fasta"),
    "B9GPE8_Populus_trichocarpa": Path("data/raw/EPSPS_conservation_Populus_trichocarpa_B9GPE8.fasta"),
}

REFERENCE_ID = "8UMJ_A0A1D6NVZ6_Zea_mays_reference"


def read_fasta(path):
    records = {}
    current_id = None
    seq = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_id is not None:
                    records[current_id] = "".join(seq)
                current_id = line[1:].split()[0]
                seq = []
            else:
                seq.append(line)
    if current_id is not None:
        records[current_id] = "".join(seq)
    return records


def write_wrapped(handle, name, seq):
    handle.write(f">{name}\n")
    for idx in range(0, len(seq), 70):
        handle.write(seq[idx:idx + 70] + "\n")


def load_eleusine_susceptible():
    records = read_fasta("data/raw/EPSPS_Eindica_AJ417033_AJ417034.fasta")
    dna = records["AJ417034.1"]
    return translate_dna(dna)


def main():
    records = {}
    for record_id, path in PANEL_FASTAS.items():
        fasta_records = read_fasta(path)
        records[record_id] = next(iter(fasta_records.values()))
    records["AJ417034_Eleusine_indica_susceptible_Baerson2002"] = load_eleusine_susceptible()

    with open(OUTPUT_PANEL, "w", encoding="utf-8") as handle:
        for record_id, seq in records.items():
            write_wrapped(handle, record_id, seq)

    structured_positions = {
        int(row["position"])
        for row in csv.DictReader(open("data/processed/epsps_8umj_distance_sasa.csv", encoding="utf-8"))
    }
    rows = conservation_rows(records, REFERENCE_ID)
    for row in rows:
        row["sequence_position"] = row["position"]
        row["position"] = row["sequence_position"] - 1
    rows = [row for row in rows if row["position"] in structured_positions]
    with open(OUTPUT_ENTROPY, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "position",
            "sequence_position",
            "residue",
            "shannon_entropy",
            "normalized_conservation",
            "n_species_present",
            "n_species_total",
        ])
        writer.writeheader()
        writer.writerows(rows)

    by_pos = {row["position"]: row for row in rows}
    row = by_pos[106]
    print(f"wrote {len(records)} sequences to {OUTPUT_PANEL}")
    print(f"wrote {len(rows)} structured 8UMJ/PDB positions to {OUTPUT_ENTROPY}")
    print(
        "Pro106 site: "
        f"residue={row['residue']}, entropy={row['shannon_entropy']:.3f}, "
        f"conservation={row['normalized_conservation']:.3f}, "
        f"present={row['n_species_present']}/{row['n_species_total']}"
    )


if __name__ == "__main__":
    main()
