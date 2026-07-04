# ALS/AHAS Phase 2 pilot - validation gate results

Pipeline: `scripts/chimerax_als_distance_sasa.py` + `scripts/als_conservation_entropy.py`
on 1Z8N (*Arabidopsis thaliana* AHAS + bound imazaquin, Mg2+, FAD, TPP
cofactors). Mirrors PPO's Phase 1 pipeline (percentile-rank distance, SASA,
Shannon-entropy conservation) with two ALS-specific adaptations:

- **Active-site core defined directly from the structure and dimer interface.**
  The original same-chain 1IQ contact set contained 16 residues:
  {220, 245, 246, 275, 276, 279, 280, 281, 351, 376, 377, 396, 397, 574,
  653, 654}. External review correctly flagged that AHAS inhibitor binding occurs
  at a dimer-interface pocket, so the core now also includes 11 neighboring-subunit
  interface residues projected into the same Arabidopsis/PDB numbering convention:
  {121, 122, 168, 195, 196, 197, 199, 200, 206, 207, 256}. Corrected core size:
  **27 residues**.
- **SASA computed on the author-determined biological tetramer** (assembly 1, via
  `sym #1 assembly 1`), not the single deposited chain - same oligomer-context fix
  applied to PPO's 1SEZ. Values are still raw SASA in A^2; residue-normalized RSA
  remains a cross-enzyme synthesis task before Phase 4 pooling.

## Results

| Mutation | Position | In active-site core? | Dist. to active-site core | Percentile | Dist. to nearest *other* core residue | SASA | Conservation (9 species) |
|---|---:|---|---:|---:|---:|---:|---|
| Trp574Leu | 574 | **Yes** (direct 1IQ contact) | 0.00 A | 4.64 | 10.61 A | 19.2 A^2 | **1.000 (invariant)** |
| Ser653Asn | 653 | **Yes** (direct 1IQ contact) | 0.00 A | 4.64 | 3.79 A | 32.6 A^2 | **1.000 (invariant)** |

The interface correction changes the biological completeness of the active-site
definition, but not the validation-gate interpretation for the two pilot mutations.
Trp574 and Ser653 remain direct herbicide-contact residues and fully conserved.
The added interface positions are important because they explain why other classic
ALS/AHAS resistance hotspots, especially Ala122 and Pro197, are real pocket
residues even though they were outside the intentionally narrow two-mutation pilot
scope.

## Validation gate: PASS - but a different kind of result than PPO's

**This is not an outlier finding like DeltaG210.** Trp574 and Ser653 are directly
in the herbicide-binding pocket in the crystal structure, and both are completely
invariant across a 9-species plant panel (Arabidopsis, *Amaranthus palmeri*,
soybean, rice, maize, tomato, sugar beet, tobacco, poplar). This is the textbook,
expected profile for genuine active-site substrate/inhibitor-contact residues:
highly conserved because they are functionally constrained, and resistant via
direct steric interference with herbicide binding.

**Why this still counts as a validation-gate pass:** the pipeline correctly
identifies genuine active-site residues as active-site residues when applied to a
known ALS case. This complements PPO's DeltaG210 gate, which checked whether the
pipeline could place a non-obvious mutation adjacent to, but outside, the active
site. Together, the pilots show that the static pipeline handles both direct-contact
and near-pocket resistance mechanisms.

**No new outlier candidate here.** Unlike V361A in PPO, neither Trp574Leu nor
Ser653Asn shows a "far from core + poorly conserved" profile. Both substitutions
are straightforwardly explained by direct binding-pocket interference.

## Note for cross-enzyme synthesis (Phase 4)

The ALS correction should be kept as the template for any multimeric target:
define the ligand-contact pocket in biological-assembly context, not only within a
single chain. ACCase already used the 1UYS B+C dimer for this reason. Before Phase
4, convert raw SASA to residue-normalized RSA so buried/exposed comparisons are not
biased by residue size or enzyme-family composition.
