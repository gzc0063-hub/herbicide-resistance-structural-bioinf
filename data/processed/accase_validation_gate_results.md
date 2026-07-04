# ACCase Phase 2 (batch) — validation gate results: Cys2088Arg

Pipeline: `scripts/chimerax_accase_distance_sasa.py` + `scripts/accase_conservation_entropy.py`
on 1UYS (*Saccharomyces cerevisiae* ACCase carboxyltransferase domain + bound
haloxyfop, chains B+C - the real deposited biological dimer, confirmed via
`REMARK 350`, same pair Délye et al. 2005 themselves used as their homology-
modeling template). Mutation: **Cys2088Arg** (Yu et al. 2007, *Lolium rigidum*),
sourced and verified per `accase_mutations.csv`.

## Dimer-interface lesson from ALS, applied from the start

Unlike ALS's 1Z8N (asymmetric unit held only one chain, requiring symmetry
generation to reveal the true tetramer), 1UYS's asymmetric unit already contains
both functional dimer partners (chains B and C, confirmed via `REMARK 350
BIOMOLECULE 2: APPLY THE FOLLOWING TO CHAINS: B, C` with identity transform -
no symmetry expansion needed). The active-site core was built from **both**
chains' contacts to either bound haloxyfop copy from the start, learning directly
from the ALS correction (DECISION_LOG #17) rather than repeating that mistake.

## Active-site core: independently reproduces the literature exactly

Core = union of chain-B and chain-C residues within 4.5 Å of either bound
haloxyfop (H1L) molecule: 21 residues per chain, including positions 1734, 1735,
1738, 1924, 1956, 1967, 1974, 1997, 1998, 1999, 2001, 2002, 2024 (yeast/1UYS
numbering). **This list matches, residue-for-residue, the APP-binding-site
residues Zhang et al. 2004 identified and Délye et al. 2005 cite directly**
(Gly-1734C, Ile-1735C, Tyr-1738C, Trp-1924B, Phe-1956C, Val-1967C, Ile-1974C,
Gly-1997C, Gly-1998C, Val-2002C, among others) - computed independently here via
a simple 4.5 Å ligand-contact search, not copied from the paper. This is a clean,
direct structural validation of the whole pipeline's core-definition method.

## Numbering: black-grass (AJ310767) 2088 → yeast (1UYS) 2014

1UYS uses **native yeast numbering**, not black-grass numbering - checking the
structure's own position "2088" directly would have been wrong (it's Gln there,
not Cys). Resolved via pairwise alignment between AJ310767 (black-grass, full
2320 aa) and 1UYS chain B's own PDB-numbered sequence. **Cross-validated against
all 12 of Délye et al. 2005's own explicitly-stated yeast↔black-grass position
correspondences - 12/12 exact match** (e.g. black-grass 1781→yeast 1705,
black-grass 2041→yeast 1967, black-grass 2076→yeast 2002, etc.), giving strong
confidence in the alignment method before trusting it for a position not
explicitly stated in the paper.

**Correction:** the position not explicitly given by Délye (2088) was initially
mapped to yeast position 2013. Caught via cross-check against an independent
parallel analysis of this same repository (a separate agent working from another
local clone) that computed 2014 instead. Direct verification: 1UYS position 2014
is **MSE (selenomethionine = Met)**, matching Délye et al. 2005's Table III
statement that yeast has Met at this position; position 2013 is **Glu**, which
does not match. **Corrected to 2014.** This position falls in a locally
ambiguous stretch - Délye's own text describes positions 2027-2096 as "a more
variable region," and the alignment places a 2-residue gap spanning yeast
2012-2014, all of which sit adjacent to or are themselves Met. Positions 2012
and 2014 give near-identical distance/SASA profiles (see below), so which exact
one is the true homolog doesn't change the qualitative conclusion - but 2013 was
clearly wrong, and is now fixed.

## Results (corrected)

| Mutation | Native position | 1UYS position | In active-site core? | Percentile (distance) | SASA | Conservation (5 grass species) |
|---|---|---|---|---|---|---|
| Cys2088Arg | 2088 | 2014 | No (moderately close, but outside the strict <4.5 Å contact shell) | 25.7 | 0.7 Å² (buried) | 0.812 (fairly conserved) |

(For reference, the adjacent candidate position 2012 - also Met, on the other
side of the ambiguous gap - gives percentile 27.4 and SASA 6.1 Å², essentially
the same qualitative picture.)

## Validation gate: PASS

Two independent checks both hold up:

1. **Structural reproduction check:** the pipeline's ligand-contact active-site
   definition, built from nothing but geometry (4.5 Å to bound haloxyfop),
   exactly reproduces the residue list the original crystallographers (Zhang et
   al. 2004) and Délye et al. 2005 identified by hand. This is the strongest
   direct structural validation across all three enzymes piloted so far, since
   the comparison is against an explicitly-published residue list, not just a
   qualitative description.
2. **Position/conservation profile is internally consistent with the literature's
   own account.** Délye et al. 2005 describe position 2088's side chain as
   "located close to that in residue Asp-2078B" (i.e., in the broader active-site
   cavity) without listing it among the direct APP-contact residues - consistent
   with our finding that it's moderately close (25.7th percentile) but outside the
   strict 4.5 Å contact shell. Buried (0.7 Å² SASA) and fairly conserved (0.812,
   "most frequently Cys or Met" per Délye's own Table III) - matches the
   literature's qualitative description of this position almost exactly.

## Not yet resolved (flagged, not inferred)

- **Mechanism class** for Cys2088Arg is not yet assigned - no structural/kinetic
  paper analogous to Dayan et al. 2010 (PPO) has been read for this specific
  substitution yet. Left `pending` in `accase_mutations.csv` per this project's
  standing rule against inferring mechanism without a primary source.
- **Délye et al. 2005's own three new mutations** (Trp2027Cys, Asp2078Gly,
  Gly2096Ala) are real, peer-reviewed, allele-specific-PCR-validated findings,
  but the paper does not deposit individual per-genotype GenBank accessions for
  them (only the reference sequences AJ310767 and AJ632096) - unlike Yu et al.
  2007's Cys2088Arg, there's no clean WT-vs-mutant accession pair to build a
  dataset row from without either using the paper's own reported sequence
  differences directly (not attempted here) or locating a later paper that
  deposited these specific alleles. Flagged as an open item for a possible fuller
  ACCase pass, not pursued in this pilot to keep scope narrow (same reasoning as
  ALS's Ala122/Pro197 exclusion, DECISION_LOG #12).

## Conservation panel

5 grass plastidic (chloroplastic) ACCase sequences, all pre-vetted by Délye et
al. 2005's own Table III rather than independently searched: black-grass
(AJ310767), Italian ryegrass (AF359515), wheat (AF029895), maize (U19183), green
foxtail (AF294805). Smaller panel than PPO/ALS's 9-10 species (additional grass
ACCase sequences were not readily found via a quick NCBI title search - not
pursued further to avoid over-spending effort on panel-broadening for this
pilot), but every accession here is one the primary literature itself already
validated as a genuine chloroplastic homomeric ACCase ortholog, arguably a higher
floor of confidence than an independently-assembled panel.
