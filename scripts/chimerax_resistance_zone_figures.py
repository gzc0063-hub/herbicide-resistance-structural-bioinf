"""
NOTE: headless (--nogui) image save requires OSMesa/OpenGL, which is NOT available on
the current machine. Run this in the ChimeraX GUI (Tools > ... or `runscript`) to produce the
3D PNGs, OR use the OpenGL-free schematic SVG produced by scripts/build_resistance_zone_figure.py
(committed as output/figures/figure_5_resistance_zone_map.svg).

Render a per-family "resistance-zone map" for each structure: protein cartoon (grey),
bound herbicide/cofactor where present (sticks), and the accepted resistance
positions as spheres colored by proximity class (direct-core = blue, non-core =
magenta). ACCase uses the SWISS-MODEL weed CT-domain homodimer; H1L is absent
from that model, so no ACCase ligand is rendered. Headless save.
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

# ACCase: SWISS-MODEL weed CT-domain homodimer, positions on chains A+B.
run(session, "close all")
run(session, "open data/raw/ACCase_Alopecurus_AJ310767_CTdomain_SWISSMODEL_1UYS_homomer.pdb")
run(session, "hide all")
run(session, "show /A,B cartoon")
run(session, "color /A,B gray")
# direct-core: A:143, B:403 ; non-core: B:389,440,450,458
run(session, "show /A:143 atoms"); run(session, "style /A:143 sphere"); run(session, "color /A:143 cornflower blue")
run(session, "show /B:403 atoms"); run(session, "style /B:403 sphere"); run(session, "color /B:403 cornflower blue")
run(session, "show /B:389,440,450,458 atoms"); run(session, "style /B:389,440,450,458 sphere"); run(session, "color /B:389,440,450,458 magenta")
run(session, "lighting soft"); run(session, "set bgColor white"); run(session, "view /A,B")
run(session, "save output/figures/figure_5_accase_resistance_zone.png width 1000 height 800 supersample 3")
print("saved output/figures/figure_5_accase_resistance_zone.png")
run(session, "exit")
