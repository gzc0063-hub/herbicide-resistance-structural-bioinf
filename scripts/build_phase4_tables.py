import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FamilyConfig:
    family: str
    mutation_file: Path
    metric_file: Path
    conservation_file: Path
    mutation_structure_column: str
    metric_position_column: str
    conservation_position_column: str
    native_position_for_conservation: bool = False
    metric_chain_column: str | None = None


FAMILY_CONFIGS = (
    FamilyConfig(
        family="PPO",
        mutation_file=Path("data/processed/ppo_mutations.csv"),
        metric_file=Path("data/processed/ppo_1sez_distance_sasa.csv"),
        conservation_file=Path("data/processed/ppo_conservation_entropy.csv"),
        mutation_structure_column="position_tobacco_1SEZ",
        metric_position_column="tobacco_position",
        conservation_position_column="tobacco_position",
    ),
    FamilyConfig(
        family="ALS",
        mutation_file=Path("data/processed/als_mutations.csv"),
        metric_file=Path("data/processed/als_1z8n_distance_sasa.csv"),
        conservation_file=Path("data/processed/als_conservation_entropy.csv"),
        mutation_structure_column="position_1z8n_structure",
        metric_position_column="position",
        conservation_position_column="position",
    ),
    FamilyConfig(
        family="EPSPS",
        mutation_file=Path("data/processed/epsps_mutations.csv"),
        metric_file=Path("data/processed/epsps_8umj_distance_sasa.csv"),
        conservation_file=Path("data/processed/epsps_conservation_entropy.csv"),
        mutation_structure_column="position_8umj_structure",
        metric_position_column="position",
        conservation_position_column="position",
    ),
    FamilyConfig(
        family="ACCase",
        mutation_file=Path("data/processed/accase_mutations.csv"),
        metric_file=Path("data/processed/accase_1uys_distance_sasa.csv"),
        conservation_file=Path("data/processed/accase_conservation_entropy.csv"),
        mutation_structure_column="position_1uys_structure",
        metric_position_column="pdb_position",
        conservation_position_column="blackgrass_position",
        native_position_for_conservation=True,
        metric_chain_column="chain_id",
    ),
)


# Weed wild-type (and, where unambiguous, resistant) residue for each mutation row,
# used to flag where the mapped STRUCTURE residue is not the same amino acid as the
# weed residue (a real cross-species-template caveat, worst for the yeast ACCase
# template). 3-letter codes. Mutant is None for the PPO deletion (deltaG210) and for
# the two-allele R98G/R98M row where a single mutant residue is not defined.
WEED_RESIDUES = {
    "deltaG210_pair1": ("GLY", None),
    "deltaG210_pair2": ("GLY", None),
    "V361A": ("VAL", "ALA"),
    "G399A_R1": ("GLY", "ALA"),
    "G399A_R2": ("GLY", "ALA"),
    "R98G_R98M": ("ARG", None),
    "Trp574Leu": ("TRP", "LEU"),
    "Ser653Asn": ("SER", "ASN"),
    "Ala122Ser": ("ALA", "SER"),
    "Pro106Ser": ("PRO", "SER"),
    "Ile1781Leu": ("ILE", "LEU"),
    "Trp2027Cys": ("TRP", "CYS"),
    "Ile2041Asn": ("ILE", "ASN"),
    "Asp2078Gly": ("ASP", "GLY"),
    "Cys2088Arg": ("CYS", "ARG"),
    "Gly2096Ala": ("GLY", "ALA"),
}


def normalize_residue(name: str) -> str:
    """Map modified residues to their standard parent for identity comparison."""
    return {"MSE": "MET"}.get(name.upper(), name.upper())


def clamp_nonneg(value: str) -> str:
    """Clamp tiny negative floating-point SASA/RSA noise to 0; pass other values through."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value
    return "0.0" if -1e-6 < number < 0 else value


MUTATION_FIELDNAMES = [
    "family",
    "mutation_id",
    "species",
    "wt_accession",
    "mut_accession",
    "native_position",
    "structure_position",
    "structure_chain_id",
    "structure_pdb_position",
    "structure_residue_name",
    "weed_wt_residue",
    "template_residue",
    "template_matches_weed_residue",
    "template_is_resistant_state",
    "in_active_site_core",
    "distance_to_active_site_core_A",
    "distance_to_nearest_other_core_residue_A",
    "percentile_rank_distance_to_core",
    "sasa_A2",
    "max_sasa_tien2013_A2",
    "rsa_tien2013",
    "shannon_entropy",
    "normalized_conservation",
    "n_species_present",
    "n_species_total",
    "mechanism_class",
    "confidence",
    "source_citation",
    "source_doi",
    "notes",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def split_structure_position(structure_position: str) -> tuple[str, str]:
    if ":" in structure_position:
        chain_id, pdb_position = structure_position.split(":", 1)
        return chain_id, pdb_position
    return "", structure_position


def metric_key(row: dict[str, str], config: FamilyConfig) -> tuple[str, str]:
    chain_id = row.get(config.metric_chain_column or "", "") if config.metric_chain_column else ""
    return chain_id, row[config.metric_position_column]


def conservation_key(row: dict[str, str], config: FamilyConfig) -> str:
    if config.native_position_for_conservation:
        return row["position_native_numbering"]
    return row[config.mutation_structure_column]


def build_family_rows(repo_root: Path, config: FamilyConfig) -> list[dict[str, str]]:
    mutations = read_csv(repo_root / config.mutation_file)
    metrics = {
        metric_key(row, config): row
        for row in read_csv(repo_root / config.metric_file)
    }
    conservation = {
        row[config.conservation_position_column]: row
        for row in read_csv(repo_root / config.conservation_file)
    }

    output_rows = []
    for mutation in mutations:
        structure_position = mutation[config.mutation_structure_column]
        chain_id, pdb_position = split_structure_position(structure_position)
        metric = metrics[(chain_id, pdb_position)]
        conservation_row = conservation.get(conservation_key(mutation, config), {})
        template_residue = metric["residue_name"]
        weed_wt_residue, weed_mut_residue = WEED_RESIDUES.get(
            mutation["mutation_id"], ("", None)
        )
        normalized_template = normalize_residue(template_residue)
        template_matches = (
            "" if not weed_wt_residue else str(normalized_template == weed_wt_residue)
        )
        template_is_resistant = (
            "True"
            if weed_mut_residue and normalized_template == weed_mut_residue
            else ("False" if weed_wt_residue else "")
        )
        output_rows.append(
            {
                "family": config.family,
                "mutation_id": mutation["mutation_id"],
                "species": mutation["species"],
                "wt_accession": mutation["wt_accession"],
                "mut_accession": mutation["mut_accession"],
                "native_position": mutation["position_native_numbering"],
                "structure_position": structure_position,
                "structure_chain_id": chain_id,
                "structure_pdb_position": pdb_position,
                "structure_residue_name": template_residue,
                "weed_wt_residue": weed_wt_residue,
                "template_residue": template_residue,
                "template_matches_weed_residue": template_matches,
                "template_is_resistant_state": template_is_resistant,
                "in_active_site_core": metric["in_active_site_core"],
                "distance_to_active_site_core_A": metric["distance_to_active_site_core_A"],
                "distance_to_nearest_other_core_residue_A": metric[
                    "distance_to_nearest_other_core_residue_A"
                ],
                "percentile_rank_distance_to_core": metric[
                    "percentile_rank_distance_to_core"
                ],
                "sasa_A2": clamp_nonneg(metric["sasa_A2"]),
                "max_sasa_tien2013_A2": metric["max_sasa_tien2013_A2"],
                "rsa_tien2013": clamp_nonneg(metric["rsa_tien2013"]),
                "shannon_entropy": conservation_row.get("shannon_entropy", ""),
                "normalized_conservation": conservation_row.get(
                    "normalized_conservation", ""
                ),
                "n_species_present": conservation_row.get("n_species_present", ""),
                "n_species_total": conservation_row.get("n_species_total", ""),
                "mechanism_class": mutation["mechanism_class"],
                "confidence": mutation["confidence"],
                "source_citation": mutation["source_citation"],
                "source_doi": mutation["source_doi"],
                "notes": mutation["notes"],
            }
        )
    return output_rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def build_phase4_tables(
    repo_root: Path = Path("."),
    output_dir: Path = Path("output/tables"),
) -> tuple[Path, Path]:
    repo_root = repo_root.resolve()
    output_dir = output_dir if output_dir.is_absolute() else repo_root / output_dir

    mutation_rows = []
    for config in FAMILY_CONFIGS:
        mutation_rows.extend(build_family_rows(repo_root, config))

    mutation_path = write_csv(
        output_dir / "phase4_master_mutation_table.csv",
        MUTATION_FIELDNAMES,
        mutation_rows,
    )
    contrast_path = write_csv(
        output_dir / "phase4_target_family_contrast.csv",
        [
            "family",
            "status",
            "accepted_tsr_rows",
            "active_site_metric_file",
            "notes",
        ],
        [
            {
                "family": "HPPD",
                "status": "no_verified_weed_tsr_accepted",
                "accepted_tsr_rows": "0",
                "active_site_metric_file": "data/processed/hppd_5ywg_active_site_metrics.csv",
                "notes": (
                    "Retained as a structural negative/contrast case after source audit; "
                    "do not pool fabricated mutation rows."
                ),
            }
        ],
    )
    return mutation_path, contrast_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build Phase 4 pooled mutation and target-family contrast tables."
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=Path("output/tables"))
    args = parser.parse_args()
    mutation_path, contrast_path = build_phase4_tables(args.repo_root, args.output_dir)
    print(f"Wrote {mutation_path}")
    print(f"Wrote {contrast_path}")


if __name__ == "__main__":
    main()
