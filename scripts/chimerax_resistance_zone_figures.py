"""
NOTE: headless (--nogui) image save requires OSMesa/OpenGL, which is NOT available on
the current machine. Run this in the ChimeraX GUI (Tools > ... or `runscript`) to produce the
3D PNGs, OR use the OpenGL-free schematic SVG produced by scripts/build_resistance_zone_figure.py
(committed as output/figures/figure_5_resistance_zone_map.svg).

Render a per-family "resistance-zone map" for each structure: protein cartoon (grey),
bound herbicide/cofactor (sticks), and the accepted resistance positions as spheres
colored by proximity class (direct-core = blue, non-core = magenta). Headless save.
Run: ChimeraX --nogui --script scripts/chimerax_resistance_zone_figures.py
Outputs: output/figures/figure_5_<family>_resistance_zone.png
"""
from chimerax.core.commands import run
session = session  # noqa: F821

FAMILIES = [
    # (name, pdb, chains, ligand_resnames, {position: proximity})
    ("ppo",   "data/raw/1SEZ.pdb", "A",  ["OMN", "FAD"],
     {98: "direct", 178: "noncore", 332: "noncore", 370: "noncore"}),
    ("als",   "data/raw/1Z8N.pdb", "A",  ["1IQ"],
     {122: "direct", 197: "direct", 574: "direct", 653: "direct"}),
    ("epsps", "data/raw/8UMJ.pdb", "A",  ["GPJ", "S3P"],
     {106: "noncore"}),
]
# ACCase spans two chains, handled separately below.

def render(name, pdb, chain, ligs, positions, chain_for_pos=None):
    run(session, "close all")
    run(session, f"open {pdb}")
    run(session, "hide all")
    run(session, f"show /{chain} cartoon")
    run(session, f"color /{chain} gray")
    ligsel = "|".join(f":{l}" for l in ligs)
    run(session, f"show ({ligsel}) atoms")
    run(session, f"style ({ligsel}) stick")
    run(session, f"color ({ligsel}) gold")
    direct = [p for p, c in positions.items() if c == "direct"]
    noncore = [p for p, c in positions.items() if c == "noncore"]
    cp = chain_for_pos or chain
    if direct:
        sel = ",".join(str(p) for p in direct)
        run(session, f"show /{cp}:{sel} atoms"); run(session, f"style /{cp}:{sel} sphere"); run(session, f"color /{cp}:{sel} cornflower blue")
    if noncore:
        sel = ",".join(str(p) for p in noncore)
        run(session, f"show /{cp}:{sel} atoms"); run(session, f"style /{cp}:{sel} sphere"); run(session, f"color /{cp}:{sel} magenta")
    run(session, "lighting soft")
    run(session, "set bgColor white")
    run(session, f"view /{chain}")
    out = f"output/figures/figure_5_{name}_resistance_zone.png"
    run(session, f"save {out} width 1000 height 800 supersample 3")
    print("saved", out)

for name, pdb, chain, ligs, positions in FAMILIES:
    render(name, pdb, chain, ligs, positions)

# ACCase: chains B+C, positions on both
run(session, "close all")
run(session, "open data/raw/1UYS.pdb")
run(session, "hide all")
run(session, "show /B,C cartoon")
run(session, "color /B,C gray")
run(session, "show :H1L atoms"); run(session, "style :H1L stick"); run(session, "color :H1L gold")
# direct-core: C:1705, B:1967 ; non-core: B:1953,2004,2014,2022
run(session, "show /C:1705 atoms"); run(session, "style /C:1705 sphere"); run(session, "color /C:1705 cornflower blue")
run(session, "show /B:1967 atoms"); run(session, "style /B:1967 sphere"); run(session, "color /B:1967 cornflower blue")
run(session, "show /B:1953,2004,2014,2022 atoms"); run(session, "style /B:1953,2004,2014,2022 sphere"); run(session, "color /B:1953,2004,2014,2022 magenta")
run(session, "lighting soft"); run(session, "set bgColor white"); run(session, "view /B,C")
run(session, "save output/figures/figure_5_accase_resistance_zone.png width 1000 height 800 supersample 3")
print("saved output/figures/figure_5_accase_resistance_zone.png")
run(session, "exit")
