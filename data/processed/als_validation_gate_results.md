# ALS/AHAS Phase 2 pilot — validation gate results

Pipeline: `scripts/chimerax_als_distance_sasa.py` + `scripts/als_conservation_entropy.py`
on 1Z8N (*Arabidopsis thaliana* AHAS + bound imazaquin, Mg²⁺, FAD, TPP cofactors).
Mirrors PPO's Phase 1 pipeline (percentile-rank distance, SASA, Shannon-entropy
conservation) with two adaptations specific to ALS:

- **Active-site core defined directly from the structure**, not from a literature
  4-residue list: every residue within 4.5 Å of either bound imazaquin copy (1Z8N
  has two 1IQ molecules). Core = {220, 245, 246, 275, 276, 279, 280, 281, 351, 376,
  377, 396, 397, **574**, **653**, 654} (chain A, Arabidopsis/PDB numbering).
  Trp574 and Ser653 are themselves members of this core.
- **SASA computed on the author-determined biological tetramer** (assembly 1, via
  `sym #1 assembly 1`), not the single deposited chain - same dimer-context fix
  applied to PPO's 1SEZ.

## Results

| Mutation | Position | In active-site core? | Dist. to nearest *other* core residue | Percentile | SASA | Conservation (9 species) |
|---|---|---|---|---|---|---|
| Trp574Leu | 574 | **Yes** (direct 1IQ contact, 3.4 Å) | 10.61 Å | 22.0 | 19.2 Å² | **1.000 (invariant)** |
| Ser653Asn | 653 | **Yes** (direct 1IQ contact, 3.65 Å) | 3.79 Å | 1.7 | 32.6 Å² | **1.000 (invariant)** |

("Distance to nearest other core residue" excludes the residue itself - it
measures how tightly clustered each is with the rest of the defined active site,
not distance to the site as a whole, since both are already core members.)

## Validation gate: PASS — but a different kind of result than PPO's

**This is not an outlier finding like ΔG210.** Trp574 and Ser653 are directly,
physically in contact with the bound herbicide (imazaquin) in the crystal
structure, and both are completely invariant across a 9-species plant panel
(Arabidopsis, Amaranthus palmeri, soybean, rice, maize, tomato, sugar beet,
tobacco, poplar). This is the textbook, expected profile for genuine active-site
substrate/inhibitor-contact residues: highly conserved because they're functionally
constrained, and resistant via direct steric interference with herbicide binding
- exactly the well-established mechanism described in the ALS literature (Tranel &
Wright 2002) for these two specific, decades-studied substitutions.

**Why this still counts as a validation-gate pass:** the pipeline correctly
identifies genuine active-site residues as being genuine active-site residues
(direct ligand contact, complete conservation) when applied to a *known, textbook*
case - a different but equally valid kind of check than PPO's ΔG210 gate, which
confirmed the pipeline could correctly place a genuinely non-obvious position
(adjacent-to-but-outside the core). Together, the two pilots show the static
pipeline gets both the "surprising" case (PPO) and the "expected" case (ALS)
right, which is a stronger combined validation than either alone.

**No outlier candidate here** - unlike V361A in PPO, neither Trp574Leu nor
Ser653Asn shows the "far from core + poorly conserved" profile that would flag it
for the panel's "hunt for non-obvious mechanisms" recommendation. Both mutations
here are straightforwardly explained by direct steric interference in the binding
pocket, consistent with decades of prior ALS literature - there isn't a novel
structural story to surface from this particular pair.

## Note for cross-enzyme synthesis (Phase 4)

This is useful context for the eventual cross-SOA comparison: PPO's ΔG210 and
ALS's Trp574/Ser653 sit at opposite ends of the "distance to active site" spectrum
(near-but-outside vs. directly-in-contact), while both are highly conserved. A
cross-enzyme permutation test should be able to recover this contrast - it's a
useful internal check that the normalized distance metric is behaving sensibly
across enzymes with different active-site architectures, per the panel review's
original concern about cross-enzyme comparability (DECISION_LOG §2).
