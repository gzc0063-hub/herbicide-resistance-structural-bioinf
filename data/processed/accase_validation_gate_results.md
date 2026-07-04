# ACCase Validation Gate Results

## Setup

- **Structure:** 1UYS, yeast ACCase carboxyltransferase domain bound to haloxyfop
  (`H1L`).
- **Biological unit used:** chains B+C, the dimeric unit identified in the PDB
  header and used for Delye et al. 2005's structural interpretation.
- **Active-site core:** all B/C protein residues with any atom within 4.5 A of
  bound `H1L`; 42 chain-residue positions.
- **Numbering:** black-grass AJ310767 CT-domain positions aligned to 1UYS.
- **SASA:** ChimeraX `measure sasa` on the B+C dimer after deleting chain A.

## Mutation Metrics

| Mutation | 1UYS chain:residue | In ligand-contact core? | Distance to core (A) | Distance percentile | SASA (A^2) | Conservation |
|---|---:|---:|---:|---:|---:|---:|
| Ile1781Leu | C:1705 | yes | 0.00 | 3.2 | 0.0 | 0.909 |
| Trp2027Cys | B:1953 | no | 5.60 | 10.4 | 3.2 | 1.000 |
| Ile2041Asn | B:1967 | yes | 0.00 | 3.2 | 1.6 | 0.850 |
| Asp2078Gly | B:2004 | no | 5.19 | 8.7 | 0.5 | 1.000 |
| Cys2088Arg | B:2014 | no | 11.83 | 25.9 | 0.7 | 0.904 |
| Gly2096Ala | B:2022 | no | 7.28 | 12.8 | 1.4 | 1.000 |

## Interpretation

ACCase clears the validation gate. The result is not a single uniform pattern:
Ile1781Leu and Ile2041Asn are direct ligand-contact-core substitutions; Trp2027Cys,
Asp2078Gly, and Gly2096Ala sit just outside the contact core; Cys2088Arg is a
more distant pocket/cavity-context mutation in the static 1UYS mapping. That mix
matches Delye et al. 2005's qualitative interpretation that these residues cluster
around the CT herbicide-binding cavity but differ in exact pocket position and
mechanistic effect.

The conservation panel is reference-indexed to AJ310767 and built from plastidic
grass ACCase accessions explicitly named in Delye et al. 2005 and Yu et al. 2007.
Partial CT-domain sequences are included only through the reference-indexed
alignment; missing coverage is reflected in `n_species_present`.
