# External Review Response

This document records how the external review artifact and the parallel Claude-side
review were reconciled into the current working repository. The review was useful,
but it mixed valid method concerns with several points that were already solved or
superseded in the current workspace. The decisions below are the adopted project
state.

## Adopted Corrections

### ALS/AHAS active-site core

The review's main valid criticism was that AHAS inhibitor binding is a dimer-interface
pocket, so a single-chain ligand-contact core under-counts real binding-pocket
residues. This was verified against 1Z8N and fixed.

Current ALS core:

- Same-chain 1IQ contact residues: 220, 245, 246, 275, 276, 279, 280, 281, 351,
  376, 377, 396, 397, 574, 653, 654.
- Added interface-pocket residues: 121, 122, 168, 195, 196, 197, 199, 200, 206,
  207, 256.
- Corrected core size: 27 residues.

This correction explains why Ala122 and Pro197 are classic ALS resistance hotspots:
they are genuine interface-pocket residues, even though they were deliberately
outside the narrow two-mutation ALS pilot. The pilot interpretation itself is
unchanged: Trp574Leu and Ser653Asn remain direct active-site/contact residues,
fully conserved, with distance-to-core = 0 A under the standardized metric schema.

### Raw SASA vs RSA

The project has been reporting raw per-residue SASA in A^2, not relative solvent
accessibility (RSA). That does not change current buried/exposed calls, which are
clear-cut, but raw SASA is not the right pooled cross-enzyme covariate because amino
acid size and family composition can bias comparisons.

Decision implemented: retain raw SASA columns for traceability and add
`max_sasa_tien2013_A2` plus `rsa_tien2013` to the current static metric CSVs before
Phase 4 cross-enzyme pooling. Phase 4 should use RSA, not raw SASA, for pooled
exposure comparisons.

### HPPD framing

Do not use Gly336 as a weed target-site resistance mutation. It is an engineered
*Pseudomonas fluorescens* HPPD crop-tolerance variant used in FG72 soybean, not an
evolved weed-resistance allele.

Current HPPD stance after the audit: no peer-reviewed, weed-evolved HPPD
target-site amino-acid mutation with verified accession-level support was accepted.
HPPD is therefore completed as an informative negative/contrast case dominated by
non-target-site resistance, expression effects, and metabolism rather than forced
into the TSR validation-gate template.

### ACCase and EPSPS

The review's ACCase/EPSPS cautions were adopted in the completed work:

- ACCase now uses a SWISS-MODEL black-grass AJ310767 CT-domain homodimer for
  distance/SASA/RSA metrics, preserving the dimer context rather than a
  single-chain pocket assumption.
- Because SWISS-MODEL excluded haloxyfop (`H1L`), ACCase active-site-core
  membership is transferred from aligned 1UYS H1L-contact residues.
- ACCase numbering is anchored to black-grass AJ310767 and independently checked
  for the Cys2088Arg case from Yu et al. 2007; the current weed-model mapping is
  2088 -> chain B residue 450.
- EPSPS uses the plant 8UMJ maize EPSPS structure with glyphosate/S3P, not the
  bacterial 1G6S structure.
- EPSPS Pro106Ser maps to 8UMJ PDB residue 106; the apparent one-residue offset is
  due to 8UMJ numbering its initiating Met as residue 0.

## Not Adopted as Immediate Work

No molecular dynamics will be added. Literature MD or cavity-volume results remain
benchmarks, not quantities this static pipeline tries to reproduce.

No batch launch across unresolved targets. HPPD has now cleared the go/no-go audit
as a structural contrast case; FAT/DHODH stay behind the already validated
real-structure targets unless a verified structure and target-site mutation set are
established.

## Next Decisions Forced by This Review

1. Build Phase 4 pooled mutation and target-family contrast tables using RSA as
   the exposure covariate.
2. Keep HPPD out of the pooled mutation table unless a future verified weed TSR is
   found.
3. Check DHODH for newer plant structures before assuming ColabFold is required.
