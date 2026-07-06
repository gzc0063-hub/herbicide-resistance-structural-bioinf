"""
Convert the manuscript's SVG figures to PDF for Pest Management Science submission.

Wiley's general author guidelines (PMS has no journal-specific override) require vector
figures (plots, graphs, line diagrams) as PDF, PS, or EPS -- not the SVGs this repo
generates by default. All five manuscript figures are vector line-art/schematics, so PDF
is the correct target (not TIFF, which is for bitmap/photographic figures).

This is a submission-formatting step, not part of the Phase 4 analysis pipeline, so it is
not wired into rebuild_all.py. Run it after rebuild_all.py, whenever the SVGs change:

    .venv/Scripts/python.exe scripts/convert_figures_for_pms.py
"""
from pathlib import Path

from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

FIGURES = [
    "figure_1_workflow",
    "figure_2_permutation_enrichment",
    "figure_3_position_screen",
    "figure_4_distance_rsa_conservation",
    "figure_5_resistance_zone_map",
]


def convert_figures_for_pms(
    repo_root: Path = Path("."),
    source_dir: Path = Path("output/figures"),
    output_dir: Path = Path("output/figures_pms"),
) -> list[Path]:
    repo_root = repo_root.resolve()
    source_dir = source_dir if source_dir.is_absolute() else repo_root / source_dir
    output_dir = output_dir if output_dir.is_absolute() else repo_root / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    written = []
    for name in FIGURES:
        svg_path = source_dir / f"{name}.svg"
        pdf_path = output_dir / f"{name}.pdf"
        drawing = svg2rlg(str(svg_path))
        renderPDF.drawToFile(drawing, str(pdf_path))
        written.append(pdf_path)
        print(f"Wrote {pdf_path}")
    return written


if __name__ == "__main__":
    convert_figures_for_pms()
