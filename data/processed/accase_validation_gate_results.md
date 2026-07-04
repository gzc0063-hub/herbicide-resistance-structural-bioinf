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

## Numbering: black-grass (AJ310767) 2088 → yeast (1UYS) 2013

1UYS uses **native yeast numbering**, not black-grass numbering - checking the
structure's own position "2088" directly would have been wrong (it's Gln there,
not Cys). Resolved via pairwise alignment between AJ310767 (black-grass, full
2320 aa) and 1UYS chain B's own PDB-numbered sequence. **Cross-validated against
all 12 of Délye et al. 2005's own explicitly-stated yeast↔black-grass position
correspondences - 12/12 exact match** (e.g. black-grass 1781→yeast 1705,
black-grass 2041→yeast 1967, black-grass 2076→yeast 2002, etc.), giving strong
confidence in the alignment before trusting the derived 2088→2013 mapping for a
position not explicitly stated in the paper.

## Results

| Mutation | Native position | 1UYS position | In active-site core? | Percentile (distance) | SASA | Conservation (5 grass species) |
|---|---|---|---|---|---|---|
| Cys2088Arg | 2088 | 2013 | No (34% closer than most, but outside the strict <4.5 Å contact shell) | 32.1 | 7.2 Å² (buried) | 0.812 (fairly conserved) |

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
   with our finding that it's moderately close (32nd percentile) but outside the
   strict 4.5 Å contact shell. Buried (7.2 Å² SASA) and fairly conserved (0.812,
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
