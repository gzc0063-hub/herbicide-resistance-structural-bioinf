import argparse
import csv
import html
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


MECHANISM_FIELDNAMES = [
    "family",
    "structure_position",
    "mutation_ids",
    "residue_name",
    "proximity_class",
    "mechanism_label",
    "mechanism_evidence_level",
    "dynamic_review_relevance",
    "manuscript_interpretation",
    "percentile_rank_distance_to_core",
    "rsa_tien2013",
    "normalized_conservation",
]


MECHANISM_ANNOTATIONS = {
    ("PPO", "98"): (
        "direct_core",
        "literature_supported",
        "Direct active-site/core residue; static proximity is expected to be informative.",
        "Use as direct-pocket benchmark for PPO substitutions.",
    ),
    ("PPO", "178"): (
        "allosteric_hinge",
        "literature_supported",
        "Review's loop/helix critique is relevant; Dayan/Hao literature describes a deletion-linked structural mechanism not reducible to distance alone.",
        "Highlight as the flagship non-core mechanistic exception: close to the active-site zone but distinctive by helix/deletion effects.",
    ),
    ("PPO", "332"): (
        "unresolved_static_candidate",
        "static_supported",
        "Static screen places this outside the immediate core, but mechanism remains unresolved and conservation is modest.",
        "Keep as unresolved; do not overclaim dynamic mechanism without additional literature support.",
    ),
    ("PPO", "370"): (
        "adjacent",
        "literature_supported",
        "Adjacent non-core site where static proximity plus literature mechanism support a binding-pocket interpretation.",
        "Use as a near-core PPO resistance benchmark.",
    ),
    ("ALS", "574"): (
        "direct_core",
        "literature_supported",
        "Review agrees this is a direct pocket/contact example where static structural mapping is expected to work well.",
        "Use as direct-core ALS benchmark.",
    ),
    ("ALS", "653"): (
        "direct_core",
        "literature_supported",
        "Direct ALS pocket position; dynamic cross-resistance details are outside this static resource's prediction scope.",
        "Use as direct-core ALS benchmark.",
    ),
    ("EPSPS", "106"): (
        "allosteric_hinge",
        "literature_supported",
        "Review's open/closed and Pro106 allostery critique is relevant; Pro106 is near the glyphosate/S3P site but not a direct ligand-contact residue.",
        "Treat as directionally close but mechanistically allosteric/second-shell; EPSPS remains underpowered with one accepted position.",
    ),
    ("ACCase", "C:1705"): (
        "interface_induced_fit",
        "literature_supported",
        "ACCase dimer-interface induced-fit critique is relevant; this direct-core position sits in a ligand-induced interface pocket.",
        "Use as ACCase direct-interface benchmark, with induced-fit caveat.",
    ),
    ("ACCase", "B:1953"): (
        "interface_induced_fit",
        "literature_supported",
        "Review's ACCase induced-fit critique is relevant for this near-pocket CT-domain site.",
        "Report as near-core/interface-associated rather than pure static-contact mechanism.",
    ),
    ("ACCase", "B:1967"): (
        "interface_induced_fit",
        "literature_supported",
        "Direct-core ACCase CT-domain position in the dimer-interface pocket.",
        "Use as ACCase direct-interface benchmark, with induced-fit caveat.",
    ),
    ("ACCase", "B:2004"): (
        "interface_induced_fit",
        "literature_supported",
        "Near-core ACCase position; review's induced-fit/electrostatic pocket critique is relevant.",
        "Report as interface-associated adjacent resistance site.",
    ),
    ("ACCase", "B:2014"): (
        "interface_induced_fit",
        "literature_supported",
        "More distal ACCase accepted TSR site; review's induced-fit/dimer-interface critique is relevant.",
        "Highlight as a non-core candidate that still belongs to the ACCase interface resistance zone.",
    ),
    ("ACCase", "B:2022"): (
        "interface_induced_fit",
        "literature_supported",
        "Near-pocket ACCase CT-domain position where static distance captures zone membership but not induced-fit energetics.",
        "Report as interface-associated non-core candidate.",
    ),
}


COLORS = {
    "ACCase": "#3f6fb5",
    "ALS": "#44935f",
    "EPSPS": "#c28b2c",
    "PPO": "#9b4d8b",
    "direct_core": "#2f6fbb",
    "adjacent": "#46945f",
    "allosteric_hinge": "#c77f2f",
    "interface_induced_fit": "#7b5bc6",
    "unresolved_static_candidate": "#777777",
    "random": "#c8c8c8",
}


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


def svg_text(x: float, y: float, text: str, size: int = 12, anchor: str = "start") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'font-family="Arial, sans-serif" text-anchor="{anchor}">'
        f"{html.escape(text)}</text>"
    )


def svg_rect(x: float, y: float, width: float, height: float, fill: str, stroke: str = "none") -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'fill="{fill}" stroke="{stroke}" />'
    )


def write_svg(path: Path, width: int, height: int, body: list[str]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white" />',
        *body,
        "</svg>",
    ]
    path.write_text("\n".join(svg) + "\n", encoding="utf-8")
    return path


def mechanism_rows(screen_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for row in screen_rows:
        key = (row["family"], row["structure_position"])
        label, evidence, relevance, interpretation = MECHANISM_ANNOTATIONS[key]
        rows.append(
            {
                "family": row["family"],
                "structure_position": row["structure_position"],
                "mutation_ids": row["mutation_ids"],
                "residue_name": row["residue_name"],
                "proximity_class": row["proximity_class"],
                "mechanism_label": label,
                "mechanism_evidence_level": evidence,
                "dynamic_review_relevance": relevance,
                "manuscript_interpretation": interpretation,
                "percentile_rank_distance_to_core": row["percentile_rank_distance_to_core"],
                "rsa_tien2013": row["rsa_tien2013"],
                "normalized_conservation": row["normalized_conservation"],
            }
        )
    return rows


def copy_table(source: Path, destination: Path) -> Path:
    rows = read_csv(source)
    fieldnames = list(rows[0].keys()) if rows else []
    return write_csv(destination, fieldnames, rows)


def figure_1_workflow(path: Path) -> Path:
    boxes = [
        ("Curated TSR\nsource rows", 40, 82),
        ("Real structures\n+ active-site cores", 230, 82),
        ("Distance percentile\n+ RSA + conservation", 420, 82),
        ("Permutation enrichment\n+ mechanism screen", 610, 82),
        ("Static resource\nwith dynamic caveats", 800, 82),
    ]
    body = [svg_text(40, 38, "Figure 1. Static structural-bioinformatics workflow", 18)]
    for i, (label, x, y) in enumerate(boxes):
        body.append(svg_rect(x, y, 145, 74, "#f3f5f7", "#4c5967"))
        for j, line in enumerate(label.split("\n")):
            body.append(svg_text(x + 72, y + 30 + j * 18, line, 13, "middle"))
        if i < len(boxes) - 1:
            body.append(f'<line x1="{x + 145}" y1="{y + 37}" x2="{x + 185}" y2="{y + 37}" stroke="#4c5967" stroke-width="2" />')
            body.append(f'<polygon points="{x + 185},{y + 37} {x + 176},{y + 32} {x + 176},{y + 42}" fill="#4c5967" />')
    body.append(svg_text(40, 190, "Scope boundary: no new MD pipeline; literature dynamics/free-energy studies are cited as mechanism context.", 13))
    return write_svg(path, 990, 230, body)


def figure_2_permutation(path: Path, summary_rows: list[dict[str, str]]) -> Path:
    width, height = 760, 360
    left, top, plot_w = 120, 70, 560
    body = [svg_text(40, 34, "Figure 2. Observed TSR positions are enriched near active-site cores", 18)]
    body.append(f'<line x1="{left}" y1="{height - 58}" x2="{left + plot_w}" y2="{height - 58}" stroke="#333" />')
    for tick in range(0, 101, 25):
        x = left + plot_w * tick / 100
        body.append(f'<line x1="{x:.1f}" y1="{height - 62}" x2="{x:.1f}" y2="{height - 54}" stroke="#333" />')
        body.append(svg_text(x, height - 36, str(tick), 11, "middle"))
    for i, row in enumerate(summary_rows):
        y = top + i * 58
        observed = float(row["observed_mean_percentile"])
        random_mean = float(row["random_mean_percentile_mean"])
        p_value = float(row["empirical_p_value_lower_tail"])
        body.append(svg_text(35, y + 19, row["family"], 13))
        body.append(svg_rect(left, y, plot_w * random_mean / 100, 16, COLORS["random"]))
        body.append(svg_rect(left, y + 22, plot_w * observed / 100, 16, COLORS[row["family"]]))
        body.append(svg_text(left + plot_w + 10, y + 34, f"p={p_value:.4f}", 11))
    body.append(svg_text(left + 140, height - 10, "Mean distance-to-core percentile (lower = closer)", 12))
    body.append(svg_rect(520, 48, 18, 12, COLORS["random"]))
    body.append(svg_text(544, 58, "random mean", 11))
    body.append(svg_rect(620, 48, 18, 12, "#3f6fb5"))
    body.append(svg_text(644, 58, "observed", 11))
    return write_svg(path, width, height, body)


def figure_3_position_screen(path: Path, rows: list[dict[str, str]]) -> Path:
    width, height = 850, 500
    left, top, plot_w = 130, 70, 620
    body = [svg_text(40, 34, "Figure 3. Unique mutation positions by structural proximity class", 18)]
    body.append(f'<line x1="{left}" y1="{height - 55}" x2="{left + plot_w}" y2="{height - 55}" stroke="#333" />')
    for tick in range(0, 31, 10):
        x = left + plot_w * tick / 30
        body.append(f'<line x1="{x:.1f}" y1="{height - 59}" x2="{x:.1f}" y2="{height - 51}" stroke="#333" />')
        body.append(svg_text(x, height - 34, str(tick), 11, "middle"))
    for i, row in enumerate(rows):
        y = top + i * 28
        percentile = float(row["percentile_rank_distance_to_core"])
        x = left + plot_w * min(percentile, 30) / 30
        label = f"{row['family']} {row['structure_position']}"
        body.append(svg_text(28, y + 5, label, 11))
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{COLORS[row["mechanism_label"]]}" />')
        body.append(svg_text(x + 10, y + 4, row["mutation_ids"], 10))
    body.append(svg_text(left + 160, height - 8, "Distance-to-core percentile", 12))
    return write_svg(path, width, height, body)


def figure_4_scatter(path: Path, rows: list[dict[str, str]]) -> Path:
    width, height = 760, 460
    left, top, plot_w, plot_h = 85, 58, 590, 320
    body = [svg_text(40, 30, "Figure 4. Distance percentile, RSA, and conservation annotations", 18)]
    body.append(f'<rect x="{left}" y="{top}" width="{plot_w}" height="{plot_h}" fill="none" stroke="#333" />')
    for tick in range(0, 31, 10):
        x = left + plot_w * tick / 30
        body.append(f'<line x1="{x:.1f}" y1="{top + plot_h}" x2="{x:.1f}" y2="{top + plot_h + 6}" stroke="#333" />')
        body.append(svg_text(x, top + plot_h + 22, str(tick), 11, "middle"))
    for tick in [0, 0.1, 0.2, 0.3]:
        y = top + plot_h - plot_h * tick / 0.3
        body.append(f'<line x1="{left - 6}" y1="{y:.1f}" x2="{left}" y2="{y:.1f}" stroke="#333" />')
        body.append(svg_text(left - 12, y + 4, f"{tick:.1f}", 11, "end"))
    for row in rows:
        percentile = float(row["percentile_rank_distance_to_core"])
        rsa = max(0.0, float(row["rsa_tien2013"]))
        conservation = float(row["normalized_conservation"] or 0)
        x = left + plot_w * min(percentile, 30) / 30
        y = top + plot_h - plot_h * min(rsa, 0.3) / 0.3
        radius = 4 + 5 * conservation
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{COLORS[row["mechanism_label"]]}" opacity="0.82" />')
    body.append(svg_text(left + 160, height - 38, "Distance-to-core percentile", 12))
    body.append(svg_text(18, top + 170, "RSA", 12))
    body.append(svg_text(95, height - 12, "Point size scales with normalized conservation; colors show mechanism annotation.", 11))
    return write_svg(path, width, height, body)


def build_review_driven_outputs(
    repo_root: Path = Path("."),
    table_dir: Path = Path("output/tables"),
    figure_dir: Path = Path("output/figures"),
) -> dict[str, Path | list[Path]]:
    repo_root = repo_root.resolve()
    table_dir = table_dir if table_dir.is_absolute() else repo_root / table_dir
    figure_dir = figure_dir if figure_dir.is_absolute() else repo_root / figure_dir

    screen = read_csv(repo_root / "output/tables/phase4_non_core_position_screen.csv")
    summary = read_csv(repo_root / "output/tables/phase4_permutation_summary.csv")
    hppd = repo_root / "output/tables/phase4_target_family_contrast.csv"
    mechanisms = mechanism_rows(screen)

    mechanism_path = write_csv(
        table_dir / "phase4_mechanism_annotations.csv",
        MECHANISM_FIELDNAMES,
        mechanisms,
    )
    table_1 = copy_table(
        repo_root / "output/tables/phase4_permutation_summary.csv",
        table_dir / "manuscript_table_1_family_permutation_summary.csv",
    )
    table_2 = write_csv(
        table_dir / "manuscript_table_2_unique_position_mechanisms.csv",
        MECHANISM_FIELDNAMES,
        mechanisms,
    )
    table_3 = copy_table(
        hppd,
        table_dir / "manuscript_table_3_hppd_contrast_status.csv",
    )

    figures = [
        figure_1_workflow(figure_dir / "figure_1_workflow.svg"),
        figure_2_permutation(figure_dir / "figure_2_permutation_enrichment.svg", summary),
        figure_3_position_screen(figure_dir / "figure_3_position_screen.svg", mechanisms),
        figure_4_scatter(figure_dir / "figure_4_distance_rsa_conservation.svg", mechanisms),
    ]
    return {
        "mechanism_table": mechanism_path,
        "table_1": table_1,
        "table_2": table_2,
        "table_3": table_3,
        "figures": figures,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build review-driven Phase 4 mechanism annotations and manuscript outputs."
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--table-dir", type=Path, default=Path("output/tables"))
    parser.add_argument("--figure-dir", type=Path, default=Path("output/figures"))
    args = parser.parse_args()
    outputs = build_review_driven_outputs(args.repo_root, args.table_dir, args.figure_dir)
    for key, value in outputs.items():
        if isinstance(value, list):
            for path in value:
                print(f"Wrote {path}")
        else:
            print(f"Wrote {value}")


if __name__ == "__main__":
    main()
