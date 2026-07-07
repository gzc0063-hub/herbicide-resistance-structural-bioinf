"""
Static, pure-Python biophysical perturbation score for each accepted mutation.

This is deliberately NOT a substitute for a physics-based free-energy estimator
(FoldX, DDGun) -- neither is installed/licensed in this environment. Instead it
computes three orthogonal, literature-tabulated per-residue property deltas
between the weed wild-type and mutant amino acid, giving a static, fully
reproducible, no-external-binary axis alongside distance percentile and RSA.

Three components (each |wt - mut|, using published scales verified against
their primary sources rather than recalled from memory):

1. bulkiness_delta_A3: Zimmerman JM, Eliezer N, Simha R (1968) The
   characterization of amino acid sequences in proteins by statistical
   methods. J Theor Biol 21:170-201. (Table of side-chain "bulkiness" =
   volume/length ratio.) Used in place of the classic Chothia volume table,
   which could not be re-verified against a live source in this session --
   using an unverified table risked citing wrong numbers, so this
   independently-confirmed table was used instead.
2. hydropathy_delta: Kyte J, Doolittle RF (1982) A simple method for
   displaying the hydropathic character of a protein. J Mol Biol 157:105-132.
3. charge_delta: formal side-chain charge at physiological pH (Asp/Glu = -1,
   Lys/Arg = +1, His = 0 -- mostly deprotonated/neutral at pH 7.4, all others
   = 0). Standard biochemistry, not a literature table lookup.

Run standalone: .venv/Scripts/python.exe scripts/biophysical_perturbation.py
(prints a self-check). Normally imported by build_phase4_tables.py.
"""

# Zimmerman et al. 1968, Table 3 ("bulkiness"), verified against
# web.expasy.org/protscale/pscale/Bulkiness.html before use.
BULKINESS = {
    "ALA": 11.50, "ARG": 14.28, "ASN": 12.82, "ASP": 11.68, "CYS": 13.46,
    "GLN": 14.45, "GLU": 13.57, "GLY": 3.40, "HIS": 13.69, "ILE": 21.40,
    "LEU": 21.40, "LYS": 15.71, "MET": 16.25, "PHE": 19.80, "PRO": 17.43,
    "SER": 9.47, "THR": 15.77, "TRP": 21.67, "TYR": 18.03, "VAL": 21.57,
}

# Kyte & Doolittle 1982, verified against two independent sources before use.
HYDROPATHY = {
    "ILE": 4.5, "VAL": 4.2, "LEU": 3.8, "PHE": 2.8, "CYS": 2.5, "MET": 1.9,
    "ALA": 1.8, "GLY": -0.4, "THR": -0.7, "SER": -0.8, "TRP": -0.9,
    "TYR": -1.3, "PRO": -1.6, "HIS": -3.2, "GLU": -3.5, "GLN": -3.5,
    "ASP": -3.5, "ASN": -3.5, "LYS": -3.9, "ARG": -4.5,
}

# Formal side-chain charge at physiological pH (~7.4). Standard biochemistry.
CHARGE = {
    "ASP": -1, "GLU": -1, "LYS": 1, "ARG": 1, "HIS": 0,
}


def residue_deltas(wt_residue: str, mut_residue: str) -> tuple[str, str, str]:
    """Return (bulkiness_delta, hydropathy_delta, charge_delta) as strings,
    or empty strings if either residue is unknown/missing (e.g. a deletion)."""
    wt = (wt_residue or "").upper()
    mut = (mut_residue or "").upper()
    if wt not in BULKINESS or mut not in BULKINESS:
        return "", "", ""
    bulkiness_delta = abs(BULKINESS[wt] - BULKINESS[mut])
    hydropathy_delta = abs(HYDROPATHY[wt] - HYDROPATHY[mut])
    charge_delta = abs(CHARGE.get(wt, 0) - CHARGE.get(mut, 0))
    return f"{bulkiness_delta:.2f}", f"{hydropathy_delta:.2f}", str(charge_delta)


def _self_check() -> None:
    # Pro106Ser: small, polar-neutral swap -> small deltas expected.
    b, h, c = residue_deltas("PRO", "SER")
    print(f"Pro->Ser: bulkiness_delta={b} hydropathy_delta={h} charge_delta={c}")
    # Asp376Glu: same charge family, small size increase.
    b, h, c = residue_deltas("ASP", "GLU")
    print(f"Asp->Glu: bulkiness_delta={b} hydropathy_delta={h} charge_delta={c}")
    # Cys2088Arg: large bulkiness jump, charge introduced.
    b, h, c = residue_deltas("CYS", "ARG")
    print(f"Cys->Arg: bulkiness_delta={b} hydropathy_delta={h} charge_delta={c}")
    # Deletion (no mutant residue): should return blanks, not crash.
    b, h, c = residue_deltas("GLY", None)
    print(f"Gly->(deletion): bulkiness_delta={b!r} hydropathy_delta={h!r} charge_delta={c!r}")


if __name__ == "__main__":
    _self_check()
