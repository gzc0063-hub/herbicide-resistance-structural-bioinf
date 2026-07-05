import argparse
import csv
import random
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_phase4_tables import FAMILY_CONFIGS


SUMMARY_FIELDNAMES = [
    "family",
    "n_unique_positions",
    "n_background_residues",
    "iterations",
    "seed",
    "observed_mean_percentile",
    "observed_median_percentile",
    "random_mean_percentile_mean",
    "random_mean_percentile_sd",
    "empirical_p_value_lower_tail",
    "effect_observed_minus_random_mean",
]


SCREEN_FIELDNAMES = [
    "family",
    "structure_position",
    "mutation_ids",
    "residue_name",
    "in_active_site_core",
    "distance_to_active_site_core_A",
    "percentile_rank_distance_to_core",
    "rsa_tien2013",
    "normalized_conservation",
    "proximity_class",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def median(values: list[float]) -> float:
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return (ordered[midpoint - 1] + ordered[midpoint]) / 2


def sample_standard_deviation(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    value_mean = mean(values)
    variance = sum((value - value_mean) ** 2 for value in values) / (len(values) - 1)
    return variance ** 0.5


def metric_position(row: dict[str, str], config) -> str:
    if config.metric_chain_column:
        return f"{row[config.metric_chain_column]}:{row[config.metric_position_column]}"
    return row[config.metric_position_column]


def unique_mutation_positions(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped = {}
    for row in rows:
        key = (row["family"], row["structure_position"])
        if key not in grouped:
            grouped[key] = dict(row)
            grouped[key]["mutation_ids"] = row["mutation_id"]
        else:
            grouped[key]["mutation_ids"] += f";{row['mutation_id']}"
    return list(grouped.values())


def proximity_class(row: dict[str, str]) -> str:
    if row["in_active_site_core"].lower() == "true":
        return "direct_core"
    percentile = float(row["percentile_rank_distance_to_core"])
    if percentile < 10:
        return "non_core_adjacent"
    return "non_core_candidate"


def format_float(value: float) -> str:
    return f"{value:.6f}"


def family_background(repo_root: Path) -> dict[str, list[float]]:
    backgrounds = {}
    for config in FAMILY_CONFIGS:
        rows = read_csv(repo_root / config.metric_file)
        backgrounds[config.family] = [
            float(row["percentile_rank_distance_to_core"])
            for row in rows
            if row.get("percentile_rank_distance_to_core", "") != ""
        ]
    return backgrounds


def permutation_summary_rows(
    mutation_rows: list[dict[str, str]],
    backgrounds: dict[str, list[float]],
    iterations: int,
    seed: int,
) -> list[dict[str, str]]:
    rng = random.Random(seed)
    rows_by_family = defaultdict(list)
    for row in unique_mutation_positions(mutation_rows):
        rows_by_family[row["family"]].append(row)

    summary_rows = []
    for family in sorted(rows_by_family):
        observed = [
            float(row["percentile_rank_distance_to_core"])
            for row in rows_by_family[family]
        ]
        background = backgrounds[family]
        n_positions = len(observed)
        random_means = [
            mean(rng.sample(background, n_positions))
            for _ in range(iterations)
        ]
        observed_mean = mean(observed)
        random_mean = mean(random_means)
        lower_or_equal = sum(value <= observed_mean for value in random_means)
        p_value = (lower_or_equal + 1) / (iterations + 1)
        summary_rows.append(
            {
                "family": family,
                "n_unique_positions": str(n_positions),
                "n_background_residues": str(len(background)),
                "iterations": str(iterations),
                "seed": str(seed),
                "observed_mean_percentile": format_float(observed_mean),
                "observed_median_percentile": format_float(median(observed)),
                "random_mean_percentile_mean": format_float(random_mean),
                "random_mean_percentile_sd": format_float(
                    sample_standard_deviation(random_means)
                ),
                "empirical_p_value_lower_tail": format_float(p_value),
                "effect_observed_minus_random_mean": format_float(
                    observed_mean - random_mean
                ),
            }
        )
    return summary_rows


def screen_rows(mutation_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for row in unique_mutation_positions(mutation_rows):
        rows.append(
            {
                "family": row["family"],
                "structure_position": row["structure_position"],
                "mutation_ids": row["mutation_ids"],
                "residue_name": row["structure_residue_name"],
                "in_active_site_core": row["in_active_site_core"],
                "distance_to_active_site_core_A": row["distance_to_active_site_core_A"],
                "percentile_rank_distance_to_core": row[
                    "percentile_rank_distance_to_core"
                ],
                "rsa_tien2013": row["rsa_tien2013"],
                "normalized_conservation": row["normalized_conservation"],
                "proximity_class": proximity_class(row),
            }
        )
    rows.sort(
        key=lambda row: (
            row["family"],
            float(row["percentile_rank_distance_to_core"]),
            row["structure_position"],
        )
    )
    return rows


def build_phase4_analysis(
    repo_root: Path = Path("."),
    output_dir: Path = Path("output/tables"),
    iterations: int = 10000,
    seed: int = 20260704,
) -> tuple[Path, Path]:
    repo_root = repo_root.resolve()
    output_dir = output_dir if output_dir.is_absolute() else repo_root / output_dir
    mutation_rows = read_csv(
        repo_root / "output/tables/phase4_master_mutation_table.csv"
    )
    backgrounds = family_background(repo_root)
    summary_path = write_csv(
        output_dir / "phase4_permutation_summary.csv",
        SUMMARY_FIELDNAMES,
        permutation_summary_rows(mutation_rows, backgrounds, iterations, seed),
    )
    screen_path = write_csv(
        output_dir / "phase4_non_core_position_screen.csv",
        SCREEN_FIELDNAMES,
        screen_rows(mutation_rows),
    )
    return summary_path, screen_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Phase 4 within-family permutation/enrichment analysis."
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=Path("output/tables"))
    parser.add_argument("--iterations", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260704)
    args = parser.parse_args()
    summary_path, screen_path = build_phase4_analysis(
        repo_root=args.repo_root,
        output_dir=args.output_dir,
        iterations=args.iterations,
        seed=args.seed,
    )
    print(f"Wrote {summary_path}")
    print(f"Wrote {screen_path}")


if __name__ == "__main__":
    main()
