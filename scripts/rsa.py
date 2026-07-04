"""Add residue-normalized solvent accessibility to static metric CSVs."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


# Tien et al. 2013 maximum allowed solvent accessibilities, A^2.
MAX_SASA_TIEN2013 = {
    "ALA": 129,
    "ARG": 274,
    "ASN": 195,
    "ASP": 193,
    "CYS": 167,
    "GLN": 225,
    "GLU": 223,
    "GLY": 104,
    "HIS": 224,
    "ILE": 197,
    "LEU": 201,
    "LYS": 236,
    "MET": 224,
    "PHE": 240,
    "PRO": 159,
    "SER": 155,
    "THR": 172,
    "TRP": 285,
    "TYR": 263,
    "VAL": 174,
    "MSE": 224,
    "CSD": 167,
}


DEFAULT_CSVS = (
    Path("data/processed/ppo_1sez_distance_sasa.csv"),
    Path("data/processed/als_1z8n_distance_sasa.csv"),
    Path("data/processed/epsps_8umj_distance_sasa.csv"),
    Path("data/processed/accase_1uys_distance_sasa.csv"),
    Path("data/processed/hppd_5ywg_active_site_metrics.csv"),
)


def max_sasa_tien2013(residue_name: str) -> int | None:
    """Return Tien et al. 2013 maximum ASA for a PDB residue name."""
    return MAX_SASA_TIEN2013.get((residue_name or "").strip().upper())


def _fieldnames(existing: list[str]) -> list[str]:
    fields = [field for field in existing if field not in {"max_sasa_tien2013_A2", "rsa_tien2013"}]
    try:
        idx = fields.index("sasa_A2") + 1
    except ValueError:
        fields.extend(["max_sasa_tien2013_A2", "rsa_tien2013"])
    else:
        fields[idx:idx] = ["max_sasa_tien2013_A2", "rsa_tien2013"]
    return fields


def add_rsa_to_csv(
    path: str | Path,
    *,
    residue_column: str = "residue_name",
    sasa_column: str = "sasa_A2",
    output_path: str | Path | None = None,
) -> None:
    """Add max-SASA and RSA columns to a metric CSV, preserving raw SASA."""
    path = Path(path)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        if reader.fieldnames is None:
            raise ValueError(f"{path} has no header")
        fieldnames = _fieldnames(reader.fieldnames)

    for row in rows:
        max_sasa = max_sasa_tien2013(row.get(residue_column, ""))
        row["max_sasa_tien2013_A2"] = "" if max_sasa is None else str(max_sasa)

        raw_sasa = (row.get(sasa_column) or "").strip()
        if max_sasa is None or raw_sasa == "":
            row["rsa_tien2013"] = ""
            continue
        row["rsa_tien2013"] = f"{float(raw_sasa) / max_sasa:.6f}"

    target = Path(output_path) if output_path is not None else path
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csvs", nargs="*", type=Path, default=list(DEFAULT_CSVS))
    args = parser.parse_args()

    for csv_path in args.csvs:
        add_rsa_to_csv(csv_path)
        print(f"added RSA: {csv_path}")


if __name__ == "__main__":
    main()
