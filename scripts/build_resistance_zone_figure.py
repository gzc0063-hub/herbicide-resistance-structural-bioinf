"""
OpenGL-free schematic 'resistance-zone map' (Figure 5). One horizontal lane per family;
x-axis = within-family distance-to-core percentile (0 = at the ligand-contact core).
A shaded core zone sits at the left; each accepted position is a dot placed by its
percentile, colored by mechanism label, and annotated with its mutation id(s).
Reads output/tables/manuscript_table_2_unique_position_mechanisms.csv.
Output: output/figures/figure_5_resistance_zone_map.svg
"""
import csv, html, math
from pathlib import Path

COLORS = {
    "direct_core": "#2f6fbb", "adjacent": "#46945f", "second_shell_channel": "#2f9fa8",
    "allosteric_hinge": "#c77f2f", "interface_induced_fit": "#7b5bc6",
    "unresolved_static_candidate": "#777777",
}
FAMILY_ORDER = ["PPO", "ALS", "EPSPS", "ACCase"]


def esc(t): return html.escape(str(t))


def main(repo=Path(".")):
    rows = list(csv.DictReader(open(repo / "output/tables/manuscript_table_2_unique_position_mechanisms.csv", encoding="utf-8-sig")))
    by_fam = {f: [] for f in FAMILY_ORDER}
    for r in rows:
        by_fam.setdefault(r["family"], []).append(r)

    left, right = 150, 60
    W = 900
    plot_w = W - left - right
    top = 44
    lane_h = 88
    # Axis max is rounded up from the real data so no point is clamped onto the
    # right edge (ACCase Cys2088Arg reaches ~32, above the old fixed 30).
    data_max = max((float(r["percentile_rank_distance_to_core"]) for r in rows), default=30.0)
    xmax = float(max(30, math.ceil(data_max / 5) * 5))
    H = top + lane_h * len(FAMILY_ORDER) + 70

    def px(pct): return left + plot_w * min(float(pct), xmax) / xmax

    # Title/caption supplied externally (site card heading + manuscript Figure
    # Captions), so it is not baked into the SVG image itself.
    body = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
            '<rect width="100%" height="100%" fill="white"/>']
    # core zone shading (percentile < ~5, the direct-contact zone)
    core_x = px(5)
    body.append(f'<rect x="{left}" y="{top-8}" width="{core_x-left}" height="{lane_h*len(FAMILY_ORDER)}" fill="#eef3f8"/>')
    body.append(f'<text x="{left+4}" y="{top+lane_h*len(FAMILY_ORDER)+2}" font-size="10" font-family="Arial" fill="#557">ligand-contact core zone</text>')

    for i, fam in enumerate(FAMILY_ORDER):
        y = top + i * lane_h + lane_h / 2
        body.append(f'<line x1="{left}" y1="{y:.0f}" x2="{left+plot_w}" y2="{y:.0f}" stroke="#ccc"/>')
        body.append(f'<text x="{left-12}" y="{y+4:.0f}" font-size="14" font-family="Arial" text-anchor="end">{esc(fam)}</text>')
        placed = []
        for r in sorted(by_fam.get(fam, []), key=lambda r: float(r["percentile_rank_distance_to_core"])):
            x = px(r["percentile_rank_distance_to_core"])
            col = COLORS.get(r["mechanism_label"], "#555")
            # stagger labels vertically to avoid overlap; a plain 2-way alternation
            # collides again every 2 points (e.g. 4 ALS positions sharing one percentile
            # would put points 1&3 and 2&4 at the same offset), so use a longer ladder
            dy_ladder = (-14, 16, -30, 32, -46, 48, -62, 64)
            nearby = len([p for p in placed if abs(p - x) < 70])
            dy = dy_ladder[nearby % len(dy_ladder)]
            placed.append(x)
            body.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{col}"/>')
            lbl = r["mutation_ids"].replace(";", ", ")
            body.append(f'<text x="{x:.0f}" y="{y+dy:.0f}" font-size="10" font-family="Arial" text-anchor="middle">{esc(lbl)}</text>')
    # x-axis
    ay = top + lane_h * len(FAMILY_ORDER) + 18
    body.append(f'<line x1="{left}" y1="{ay}" x2="{left+plot_w}" y2="{ay}" stroke="#333"/>')
    for t in range(0, int(xmax) + 1, 5):
        x = px(t)
        body.append(f'<line x1="{x:.0f}" y1="{ay}" x2="{x:.0f}" y2="{ay+5}" stroke="#333"/>')
        body.append(f'<text x="{x:.0f}" y="{ay+18}" font-size="10" font-family="Arial" text-anchor="middle">{t}</text>')
    body.append(f'<text x="{left+plot_w/2:.0f}" y="{ay+34:.0f}" font-size="12" font-family="Arial" text-anchor="middle">distance-to-core percentile (lower = closer to the ligand-contact core)</text>')
    # legend
    lx = left; ly = 24
    for k in ["direct_core", "adjacent", "second_shell_channel", "interface_induced_fit"]:
        body.append(f'<circle cx="{lx}" cy="{ly}" r="6" fill="{COLORS[k]}"/>')
        body.append(f'<text x="{lx+10}" y="{ly+4}" font-size="10" font-family="Arial">{esc(k)}</text>')
        lx += 175
    body.append("</svg>")
    out = repo / "output/figures/figure_5_resistance_zone_map.svg"
    out.write_text("\n".join(body) + "\n", encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
