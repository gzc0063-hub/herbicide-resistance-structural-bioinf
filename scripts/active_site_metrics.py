"""Shared active-site distance metrics for herbicide resistance mapping."""

import bisect
import math


def _distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def distance_rows(residue_coords, core_positions):
    """Return standardized distance rows from residue CA coordinates.

    residue_coords maps residue position to an xyz coordinate. Core residues
    get distance_to_active_site_core_A = 0, while
    distance_to_nearest_other_core_residue_A keeps the within-core spacing that
    was previously used in the ALS pilot.
    """
    core_positions = set(core_positions)
    core_coords = {pos: residue_coords[pos] for pos in core_positions if pos in residue_coords}
    if not core_coords:
        raise ValueError("No active-site core positions were found in residue coordinates")

    rows = []
    for pos, coord in sorted(residue_coords.items()):
        in_core = pos in core_coords
        distance_to_core = 0.0 if in_core else min(_distance(coord, c) for c in core_coords.values())
        other_core_coords = [c for core_pos, c in core_coords.items() if core_pos != pos]
        distance_to_other = min(_distance(coord, c) for c in other_core_coords) if other_core_coords else None
        rows.append({
            "position": pos,
            "in_active_site_core": in_core,
            "distance_to_active_site_core_A": distance_to_core,
            "distance_to_nearest_other_core_residue_A": distance_to_other,
        })

    dists = sorted(row["distance_to_active_site_core_A"] for row in rows)
    n = len(dists)
    for row in rows:
        idx = bisect.bisect_right(dists, row["distance_to_active_site_core_A"])
        row["percentile_rank_distance_to_core"] = 100.0 * idx / n

    return rows
