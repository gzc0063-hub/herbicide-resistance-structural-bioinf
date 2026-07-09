import argparse
import csv
import html
import math
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_phase4_tables import clamp_nonneg


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
    "bulkiness_delta",
    "hydropathy_delta",
    "charge_delta",
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
    ("ALS", "122"): (
        "direct_core",
        "literature_supported",
        "Ala122 is an established ALS dimer-interface pocket TSR site (Tranel & Wright 2002); the A. palmeri A122S allele (Larran 2017) co-occurs with A282D so its individual causality is not isolated - included with medium confidence.",
        "Direct-interface ALS position; report with the A282D-confound caveat.",
    ),
    ("ALS", "197"): (
        "direct_core",
        "literature_supported",
        "Pro197 is one of the most firmly established ALS TSR sites across weeds (Tranel & Wright 2002); Pro197Ala detected in A. palmeri by Singh et al. 2018 (with Trp574Leu). Direct-core dimer-interface pocket position.",
        "Direct-core ALS benchmark; note Singh's Pro197Ala co-occurs with Trp574Leu.",
    ),
    ("ALS", "376"): (
        "direct_core",
        "literature_supported",
        "Asp376Glu (Palma-Bautista et al. 2022) in Sinapis alba, GenBank OP681621/OP681622 - a clean single-SNP substitution with no co-occurring amino-acid change elsewhere in the gene, unlike Ala122Ser. Same Arabidopsis-convention numbering as every other ALS row; 1Z8N residue 376 verified ASP. Resistance in these populations is TSR (this mutation) plus a separate, unquantified NTSR metabolic contribution.",
        "Direct-core ALS benchmark; cleanest single-substitution case in the ALS set.",
    ),
    ("EPSPS", "106"): (
        "adjacent",
        "literature_supported",
        "Pro106 is a glyphosate-binding-site-associated residue (Baerson 2002; corresponds to the Salmonella glyphosate-insensitive EPSPS substitution), not an allosteric site. Its 3.85 A CA distance sits just outside the 4.5 A atomic-contact core - a cutoff artifact, not evidence of allostery.",
        "Treat as binding-site-adjacent / second-shell; EPSPS now has 2 unique accepted positions (Pro106, Thr102) after the Thr102Ile addition, still a small-n family relative to PPO/ALS/ACCase.",
    ),
    ("EPSPS", "102"): (
        "direct_core",
        "literature_supported",
        "Thr102Ile (Yu et al. 2015) is part of the TIPS double mutation (with Pro106Ser) in a real weed-evolved Eleusine indica allele (GenBank KM078728, Malaysia field population). CAVEAT (medium confidence): T102I has never been observed or shown viable as a standalone mutation - the paper's own authors state it would likely be unfit/non-viable alone, which is why it has only ever been reported coupled with Pro106Ser.",
        "Second EPSPS position; report with the TIPS-coupling caveat, analogous to the ALS Ala122Ser/A282D confound.",
    ),
    ("ACCase", "A:143"): (
        "interface_induced_fit",
        "literature_supported",
        "Ile1781Leu: direct-core CT dimer-interface position, near the cavity opening (Delye 2005); confers APP + some CHD resistance, catalytic activity unaltered. SWISS-MODEL residue is the weed wild-type Ile.",
        "ACCase direct-interface benchmark, now using weed-model side-chain metrics.",
    ),
    ("ACCase", "B:389"): (
        "second_shell_channel",
        "literature_supported",
        "Trp2027Cys: bottom-of-cavity CT-domain position (Delye 2005); APP-only resistance and reduced catalytic activity, consistent with a second-shell/catalytic-pocket role rather than direct herbicide contact.",
        "Report as second-shell/catalytic-pocket, APP-selective.",
    ),
    ("ACCase", "B:403"): (
        "direct_core",
        "literature_supported",
        "Ile2041Asn: the single ACCase substitution Delye 2005 modelled as directly interfering with herbicide binding (major steric clash with Phe2030); APP-selective. SWISS-MODEL residue is the weed wild-type Ile.",
        "ACCase direct-contact benchmark (APP-selective), now using weed-model side-chain metrics.",
    ),
    ("ACCase", "B:440"): (
        "second_shell_channel",
        "literature_supported",
        "Asp2078Gly: bottom-of-cavity CT-domain position (Delye 2005); confers APP + CHD resistance including clethodim and reduces catalytic activity - a polar catalytic-pocket residue, not a direct herbicide contact.",
        "Report as second-shell/catalytic-pocket, broad APP+CHD.",
    ),
    ("ACCase", "B:450"): (
        "interface_induced_fit",
        "literature_supported",
        "Cys2088Arg (Yu 2007): most distal accepted ACCase position; APP + CHD incl clethodim. The SWISS-MODEL residue is the weed wild-type Cys; active-site-core membership is transferred from 1UYS H1L contacts because SWISS-MODEL excluded H1L.",
        "Non-core candidate in the interface resistance zone; report with the transferred-core caveat.",
    ),
    ("ACCase", "B:458"): (
        "adjacent",
        "literature_supported",
        "Gly2096Ala: near-pocket CT-domain position (Delye 2005); an added methyl protrudes into the cavity, APP-only. SWISS-MODEL residue is the weed wild-type Gly.",
        "Report as adjacent, APP-selective, now using weed-model side-chain metrics.",
    ),
}


COLORS = {
    "ACCase": "#3f6fb5",
    "ALS": "#44935f",
    "EPSPS": "#c28b2c",
    "PPO": "#9b4d8b",
    "direct_core": "#2f6fbb",
    "adjacent": "#46945f",
    "second_shell_channel": "#2f9fa8",
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


def nice_axis_max(values: list[float], step: int) -> int:
    """Round the largest value up to the next multiple of step, so no data
    point ever needs to be clamped/clipped onto the axis edge - every figure
    should show its own real data range, not a range sized for the dataset
    that existed before Phase 6 added more mutation rows."""
    highest = max(values, default=step)
    return max(step, math.ceil(highest / step) * step)


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
                "rsa_tien2013": clamp_nonneg(row["rsa_tien2013"]),
                "normalized_conservation": row["normalized_conservation"],
                "bulkiness_delta": row.get("bulkiness_delta", ""),
                "hydropathy_delta": row.get("hydropathy_delta", ""),
                "charge_delta": row.get("charge_delta", ""),
            }
        )
    return rows


def copy_table(source: Path, destination: Path) -> Path:
    rows = read_csv(source)
    fieldnames = list(rows[0].keys()) if rows else []
    return write_csv(destination, fieldnames, rows)


def figure_1_workflow(path: Path) -> Path:
    # The figure title/caption is supplied externally (site card heading and the
    # manuscript's Figure Captions section), so it is intentionally NOT baked
    # into the SVG - a title inside the image would duplicate the caption on the
    # site and is not wanted for journal submission, where captions are typeset
    # separately from the figure file.
    boxes = [
        ("Curated TSR\nsource rows", 40, 36),
        ("Real structures\n+ active-site cores", 230, 36),
        ("Distance percentile\n+ RSA + conservation", 420, 36),
        ("Permutation enrichment\n+ mechanism screen", 610, 36),
        ("Static resource\nwith dynamic caveats", 800, 36),
    ]
    body = []
    for i, (label, x, y) in enumerate(boxes):
        body.append(svg_rect(x, y, 145, 74, "#f3f5f7", "#4c5967"))
        for j, line in enumerate(label.split("\n")):
            body.append(svg_text(x + 72, y + 30 + j * 18, line, 13, "middle"))
        if i < len(boxes) - 1:
            body.append(f'<line x1="{x + 145}" y1="{y + 37}" x2="{x + 185}" y2="{y + 37}" stroke="#4c5967" stroke-width="2" />')
            body.append(f'<polygon points="{x + 185},{y + 37} {x + 176},{y + 32} {x + 176},{y + 42}" fill="#4c5967" />')
    body.append(svg_text(40, 148, "Scope boundary: no new MD pipeline; literature dynamics/free-energy studies are cited as mechanism context.", 13))
    return write_svg(path, 990, 176, body)


def figure_2_permutation(path: Path, summary_rows: list[dict[str, str]]) -> Path:
    # Title/caption supplied externally; not baked into the SVG (see figure_1).
    width = 760
    # left is wide enough to hold the longest right-aligned row label
    # ("ACCase (non-core)") without it running into the bars.
    left, top, plot_w, row_h = 150, 48, 520, 58
    n = len(summary_rows)
    axis_y = top + n * row_h + 10
    height = axis_y + 60
    body = [svg_rect(left, 16, 18, 12, COLORS["random"])]
    body.append(svg_text(left + 24, 26, "random mean", 11))
    body.append(svg_rect(left + 150, 16, 18, 12, "#3f6fb5"))
    body.append(svg_text(left + 174, 26, "observed", 11))
    body.append(f'<line x1="{left}" y1="{axis_y}" x2="{left + plot_w}" y2="{axis_y}" stroke="#333" />')
    for tick in range(0, 101, 25):
        x = left + plot_w * tick / 100
        body.append(f'<line x1="{x:.1f}" y1="{axis_y - 4}" x2="{x:.1f}" y2="{axis_y + 4}" stroke="#333" />')
        body.append(svg_text(x, axis_y + 22, str(tick), 11, "middle"))
    for i, row in enumerate(summary_rows):
        y = top + i * row_h
        observed = float(row["observed_mean_percentile"])
        random_mean = float(row["random_mean_percentile_mean"])
        p_value = float(row["empirical_p_value_lower_tail"])
        position_set = "non-core" if row["position_set"] == "non_core_only" else "all"
        body.append(svg_text(left - 12, y + 19, f'{row["family"]} ({position_set})', 12, "end"))
        body.append(svg_rect(left, y, plot_w * random_mean / 100, 16, COLORS["random"]))
        body.append(svg_rect(left, y + 22, plot_w * observed / 100, 16, COLORS[row["family"]]))
        body.append(svg_text(left + plot_w + 10, y + 34, f"p={p_value:.4f}", 11))
    body.append(svg_text(left + 140, axis_y + 46, "Mean distance-to-core percentile (lower = closer)", 12))
    return write_svg(path, width, height, body)


def figure_3_position_screen(path: Path, rows: list[dict[str, str]]) -> Path:
    # Title/caption supplied externally; not baked into the SVG (see figure_1).
    width = 900
    left, top, plot_w, row_h = 150, 40, 560, 28
    n = len(rows)
    axis_max = nice_axis_max(
        [float(row["percentile_rank_distance_to_core"]) for row in rows], step=10
    )
    axis_y = top + n * row_h + 10
    height = axis_y + 55
    body = [f'<line x1="{left}" y1="{axis_y}" x2="{left + plot_w}" y2="{axis_y}" stroke="#333" />']
    for tick in range(0, axis_max + 1, 10):
        x = left + plot_w * tick / axis_max
        body.append(f'<line x1="{x:.1f}" y1="{axis_y - 4}" x2="{x:.1f}" y2="{axis_y + 4}" stroke="#333" />')
        body.append(svg_text(x, axis_y + 20, str(tick), 11, "middle"))
    for i, row in enumerate(rows):
        y = top + i * row_h
        percentile = float(row["percentile_rank_distance_to_core"])
        x = left + plot_w * percentile / axis_max
        label = f"{row['family']} {row['structure_position']}"
        body.append(svg_text(28, y + 5, label, 11))
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{COLORS[row["mechanism_label"]]}" />')
        body.append(svg_text(x + 10, y + 4, row["mutation_ids"], 10))
    body.append(svg_text(left + 140, axis_y + 42, "Distance-to-core percentile", 12))
    return write_svg(path, width, height, body)


def figure_4_scatter(path: Path, rows: list[dict[str, str]]) -> Path:
    # Title/caption supplied externally; not baked into the SVG (see figure_1).
    left, top, plot_w, plot_h = 85, 30, 590, 320
    axis_max = nice_axis_max(
        [float(row["percentile_rank_distance_to_core"]) for row in rows], step=10
    )
    max_rsa = max((max(0.0, float(row["rsa_tien2013"])) for row in rows), default=0.0)
    rsa_max = max(0.3, math.ceil(max_rsa / 0.05) * 0.05)
    width = left + plot_w + 140
    height = top + plot_h + 100
    body = [f'<rect x="{left}" y="{top}" width="{plot_w}" height="{plot_h}" fill="none" stroke="#333" />']
    for tick in range(0, axis_max + 1, 10):
        x = left + plot_w * tick / axis_max
        body.append(f'<line x1="{x:.1f}" y1="{top + plot_h}" x2="{x:.1f}" y2="{top + plot_h + 6}" stroke="#333" />')
        body.append(svg_text(x, top + plot_h + 22, str(tick), 11, "middle"))
    rsa_ticks = [round(rsa_max * i / 3, 2) for i in range(4)]
    for tick in rsa_ticks:
        y = top + plot_h - plot_h * tick / rsa_max
        body.append(f'<line x1="{left - 6}" y1="{y:.1f}" x2="{left}" y2="{y:.1f}" stroke="#333" />')
        body.append(svg_text(left - 12, y + 4, f"{tick:.2f}", 11, "end"))
    for row in rows:
        percentile = float(row["percentile_rank_distance_to_core"])
        rsa = max(0.0, float(row["rsa_tien2013"]))
        conservation = float(row["normalized_conservation"] or 0)
        x = left + plot_w * percentile / axis_max
        y = top + plot_h - plot_h * rsa / rsa_max
        radius = 4 + 5 * conservation
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{COLORS[row["mechanism_label"]]}" opacity="0.82" />')
    body.append(svg_text(left + 160, top + plot_h + 60, "Distance-to-core percentile", 12))
    body.append(svg_text(18, top + plot_h / 2, "RSA", 12))
    body.append(svg_text(left, top + plot_h + 80, "Point size scales with normalized conservation; colors show mechanism annotation.", 11))
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
        figure_2_permutation(
            figure_dir / "figure_2_permutation_enrichment.svg",
            [row for row in summary if row["family"] != "ALL_FAMILIES_COMBINED"],
        ),
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
