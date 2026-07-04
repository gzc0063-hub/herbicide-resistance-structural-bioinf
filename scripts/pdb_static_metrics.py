"""Small PDB geometry helpers for static herbicide-resistance metrics.

The project normally uses ChimeraX for SASA. These helpers keep EPSPS
reproducible in headless environments where ChimeraX is not installed.
"""

from dataclasses import dataclass
import math


VDW_RADII = {
    "H": 1.20,
    "C": 1.70,
    "N": 1.55,
    "O": 1.52,
    "P": 1.80,
    "S": 1.80,
}


@dataclass(frozen=True)
class Atom:
    name: str
    residue_name: str
    chain_id: str
    residue_number: int
    coord: tuple
    element: str
    is_protein: bool


def parse_pdb(path):
    atoms = []
    with open(path) as handle:
        for line in handle:
            record = line[:6].strip()
            if record not in {"ATOM", "HETATM"}:
                continue
            altloc = line[16].strip()
            if altloc not in {"", "A"}:
                continue
            element = line[76:78].strip() or line[12:16].strip()[0]
            is_protein = record == "ATOM" or line[17:20].strip() == "MSE"
            atoms.append(Atom(
                name=line[12:16].strip(),
                residue_name=line[17:20].strip(),
                chain_id=line[21].strip(),
                residue_number=int(line[22:26]),
                coord=(float(line[30:38]), float(line[38:46]), float(line[46:54])),
                element=element.upper(),
                is_protein=is_protein,
            ))
    return atoms


def _distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def ligand_contact_core(atoms, chain_id, ligand_names, cutoff=4.5):
    ligand_names = set(ligand_names)
    lig_atoms = [
        atom for atom in atoms
        if atom.chain_id == chain_id and atom.residue_name in ligand_names
    ]
    if not lig_atoms:
        raise ValueError(f"No ligand atoms found for chain {chain_id}: {sorted(ligand_names)}")

    core = set()
    for atom in atoms:
        if not atom.is_protein or atom.chain_id != chain_id:
            continue
        if any(_distance(atom.coord, lig.coord) <= cutoff for lig in lig_atoms):
            core.add(atom.residue_number)
    return sorted(core)


def residue_ca_coords(atoms, chain_id):
    coords = {}
    names = {}
    for atom in atoms:
        if atom.is_protein and atom.chain_id == chain_id and atom.name == "CA":
            coords[atom.residue_number] = atom.coord
            names[atom.residue_number] = atom.residue_name
    return coords, names


def _sphere_points(n_points):
    points = []
    offset = 2.0 / n_points
    increment = math.pi * (3.0 - math.sqrt(5.0))
    for i in range(n_points):
        y = ((i * offset) - 1.0) + (offset / 2.0)
        r = math.sqrt(max(0.0, 1.0 - y * y))
        phi = i * increment
        points.append((math.cos(phi) * r, y, math.sin(phi) * r))
    return points


def _atom_radius(atom):
    return VDW_RADII.get(atom.element.strip().upper(), 1.70)


def _cell_key(coord, cell_size):
    return tuple(math.floor(c / cell_size) for c in coord)


def _neighbor_cells(key):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                yield (key[0] + dx, key[1] + dy, key[2] + dz)


def residue_sasa(atoms, probe_radius=1.4, n_sphere_points=240):
    """Return per-protein-residue SASA, with all non-water atoms as blockers."""
    blockers = [atom for atom in atoms if atom.residue_name != "HOH"]
    protein_atoms = [atom for atom in blockers if atom.is_protein]
    max_radius = max(_atom_radius(atom) + probe_radius for atom in blockers)
    cell_size = 2 * max_radius
    grid = {}
    for idx, atom in enumerate(blockers):
        grid.setdefault(_cell_key(atom.coord, cell_size), []).append(idx)

    unit_points = _sphere_points(n_sphere_points)
    by_residue = {}
    for atom in protein_atoms:
        atom_radius = _atom_radius(atom) + probe_radius
        atom_area = 4.0 * math.pi * atom_radius * atom_radius
        atom_key = _cell_key(atom.coord, cell_size)
        candidates = []
        for cell in _neighbor_cells(atom_key):
            candidates.extend(grid.get(cell, []))

        accessible = 0
        for point in unit_points:
            surface_point = tuple(atom.coord[i] + atom_radius * point[i] for i in range(3))
            occluded = False
            for blocker_idx in candidates:
                blocker = blockers[blocker_idx]
                if blocker is atom:
                    continue
                blocker_radius = _atom_radius(blocker) + probe_radius
                if _distance(surface_point, blocker.coord) < blocker_radius:
                    occluded = True
                    break
            if not occluded:
                accessible += 1

        key = (atom.chain_id, atom.residue_number)
        by_residue[key] = by_residue.get(key, 0.0) + atom_area * accessible / n_sphere_points
    return by_residue
