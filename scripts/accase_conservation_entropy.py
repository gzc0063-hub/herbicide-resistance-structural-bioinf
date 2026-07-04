"""
Reference-indexed Shannon entropy conservation for ACCase.

The reference is the black-grass plastidic ACCase protein CAC84161.1 from
AJ310767. Rows are filtered to the 1UYS-mapped CT-domain positions so they can be
joined directly to accase_1uys_distance_sasa.csv by blackgrass_position.
"""

import csv
import re
from pathlib import Path

try:
    from scripts.reference_conservation import _align, conservation_rows
except ImportError:
    from reference_conservation import _align, conservation_rows


INPUT_PANEL = Path("data/raw/ACCase_conservation_plastidic_grass_named_accessions.fasta")
AJ_FASTA = Path("data/raw/ACCase_Amyosuroides_AJ310767.fasta")
PDB_FASTA = Path("data/raw/1UYS.fasta")
OUTPUT_PANEL = Path("data/processed/accase_conservation_set.fasta")
OUTPUT_ENTROPY = Path("data/processed/accase_conservation_entropy.csv")

REFERENCE_ID = "AJ310767_Alopecurus_myosuroides_reference"
PDB_SEQUENCE_START = 1482
BLACKGRASS_CT_START = 1639
BLACKGRASS_CT_END = 2204


def read_fasta(path):
    records = []
    current_id = None
    seq = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_id is not None:
                    records.append((current_id, "".join(seq)))
                current_id = line[1:]
                seq = []
            else:
                seq.append(line)
    if current_id is not None:
        records.append((current_id, "".join(seq)))
    return records


def read_fasta_sequence(path):
    return next(seq for _, seq in read_fasta(path))


def accession_from_header(header):
    match = re.search(r"\|([A-Z]{1,3}\d{5,6}(?:\.\d+)?)_", header)
    if match:
        return match.group(1).split(".")[0]
    match = re.search(r"\|([A-Z]{1,3}\d{5,6}(?:\.\d+)?)\|", header)
    if match:
        return match.group(1).split(".")[0]
    match = re.search(r"lcl\|([A-Z]{1,3}\d{5,6})(?:\.\d+)?", header)
    if match:
        return match.group(1)
    raise ValueError(f"Could not parse accession from FASTA header: {header}")


def write_wrapped(handle, record_id, seq):
    handle.write(f">{record_id}\n")
    for idx in range(0, len(seq), 70):
        handle.write(seq[idx:idx + 70] + "\n")


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


def main():
    records = {}
    for header, seq in read_fasta(INPUT_PANEL):
        accession = accession_from_header(header)
        record_id = REFERENCE_ID if accession == "AJ310767" else accession
        records[record_id] = seq

    with open(OUTPUT_PANEL, "w", encoding="utf-8") as handle:
        for record_id, seq in records.items():
            write_wrapped(handle, record_id, seq)

    structured_map = blackgrass_to_pdb_map()
    rows = [
        row for row in conservation_rows(records, REFERENCE_ID)
        if row["position"] in structured_map
    ]
    for row in rows:
        row["blackgrass_position"] = row.pop("position")
        row["pdb_position"] = structured_map[row["blackgrass_position"]]

    with open(OUTPUT_ENTROPY, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "blackgrass_position",
            "pdb_position",
            "residue",
            "shannon_entropy",
            "normalized_conservation",
            "n_species_present",
            "n_species_total",
        ])
        writer.writeheader()
        writer.writerows(rows)

    by_pos = {row["blackgrass_position"]: row for row in rows}
    print(f"wrote {len(records)} sequences to {OUTPUT_PANEL}")
    print(f"wrote {len(rows)} structured AJ310767/1UYS positions to {OUTPUT_ENTROPY}")
    for pos in [1781, 2027, 2041, 2078, 2088, 2096]:
        row = by_pos[pos]
        print(
            f"{pos}: residue={row['residue']}, entropy={row['shannon_entropy']:.3f}, "
            f"conservation={row['normalized_conservation']:.3f}, "
            f"present={row['n_species_present']}/{row['n_species_total']}"
        )


if __name__ == "__main__":
    main()
