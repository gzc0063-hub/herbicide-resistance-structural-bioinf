# EPSPS validation gate results

Pipeline status: `scripts/epsps_distance_sasa.py` completed distance/SASA on 8UMJ
chain A. `scripts/epsps_conservation_entropy.py` completed reference-indexed
Shannon-entropy conservation on an 8-sequence plant EPSPS panel.

## Active-site definition

Structure: 8UMJ, wild-type *Zea mays* EPSPS complexed with glyphosate (`GPJ`) and
shikimate-3-phosphate (`S3P`).

PDB biological assembly note: 8UMJ REMARK 350 marks each chain as a monomeric
biological unit, so SASA was computed on chain A alone, with bound ligands included
as occluding atoms.

Active-site core: all chain-A protein residues with any atom within 4.5 A of
either `GPJ` or `S3P`.

Core residues:

`24, 25, 29, 51, 99, 100, 101, 102, 105, 131, 177, 178, 179, 180, 205, 206, 209,
330, 331, 354, 358, 359, 362, 403, 404, 429`

## Mutation-position result

| Mutation | Native convention | 8UMJ PDB residue | Residue | In active-site core? | Dist. to active-site core | Percentile | SASA | Conservation |
|---|---:|---:|---|---|---:|---:|---:|---:|
| Pro106Ser | 106 | 106 | PRO | False | 3.85 A | 12.9 | 14.3 A^2 | 1.000 (7/8 present) |

Interpretation: the EPSPS Pro106Ser site is adjacent to, but not inside, the
ligand-contact active-site core under this definition. That matches the known
weed-science mechanism qualitatively: Pro106 substitutions reduce glyphosate
sensitivity near the binding pocket rather than replacing one of the direct
glyphosate/S3P contact residues selected by the 4.5 A rule.

## Conservation panel

Conservation is indexed by 8UMJ/PDB residue numbering. Because 8UMJ includes an
initiating MET numbered 0, FASTA sequence position 107 maps to PDB residue 106.

Panel used:

* 8UMJ / *Zea mays* reference sequence (`A0A1D6NVZ6` in PDB metadata)
* *Eleusine indica* susceptible Baerson sequence (`AJ417034.1`; translated locally)
* *Arabidopsis thaliana* `P05466`
* *Nicotiana tabacum* `P23981`
* *Glycine max* `I1JKP7`
* *Oryza sativa* `A0A0N7KLH2` (fragment; absent at the Pro106 column)
* *Solanum lycopersicum* `P10748`
* *Populus trichocarpa* `B9GPE8`

Residue 106 result from `epsps_conservation_entropy.csv`:

| PDB residue | Sequence position | Residue | Shannon entropy | Normalized conservation | Present |
|---:|---:|---|---:|---:|---:|
| 106 | 107 | P | 0.000 | 1.000 | 7/8 |

Excluded supplied IDs:

* `A0A0R0H6D7` returned 404 from UniProt.
* `Q0DFI0`, `K4C1C4`, and `B9H6K7` returned empty FASTA from UniProt's accession
  endpoint.
* `A0A2G2Y4X3` fetched but is Capsicum annuum SAUR68-like, not Beta vulgaris EPSPS.
* `P24397` fetched but is Hyoscyamus niger hyoscyamine 6-beta-hydroxylase, not
  maize EPSPS.
* `AF349754` fetched from NCBI but is Lolium rigidum EPSPS, not Eleusine indica;
  the verified Baerson Eleusine accession remains `AJ417034.1`.

## Numbering correction

Earlier scratch mapping incorrectly reported 8UMJ residue 108 by indexing the
coordinate residue list directly. That was wrong. 8UMJ includes an initiating MET
numbered 0, and the FASTA sequence position corresponding to the Baerson GenBank
translated position 107 maps to PDB residue 106. The corrected residue is PRO in
8UMJ, as expected for Pro106Ser.

## Validation-gate decision

EPSPS passes the validation gate. Pro106Ser is not a direct ligand-contact core
residue by the 4.5 A definition, but it is adjacent to the ligand-contact core,
modestly solvent-accessible in the static structure, and fully conserved among
the sequences present at that column. This is a strong static-structure signature
for a known target-site resistance substitution and is complementary to PPO's
outside-core deletion and ALS's direct-contact mutations.
