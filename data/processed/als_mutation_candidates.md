# ALS/AHAS Phase 2 pilot — mutation candidates, needs your sign-off before proceeding

Preliminary research only - mirroring the Phase 1 `ppo_mutation_candidates.md` checkpoint.
Nothing built on top of this yet.

## Candidate crystal structures (real, confirmed via RCSB search)

27 plant AHAS entries found. Best candidates: the McCourt et al. 2006 *PNAS* series -
**Arabidopsis thaliana AHAS**, each with a different herbicide class bound:

| PDB | Herbicide class | Compound |
|---|---|---|
| 1YBH | Sulfonylurea | Chlorimuron ethyl |
| 1YHY | Sulfonylurea | Metsulfuron methyl |
| 1YHZ | Sulfonylurea | Chlorsulfuron |
| 1YI0 | Sulfonylurea | Sulfometuron methyl |
| 1YI1 | Sulfonylurea | Tribenuron methyl |
| 1Z8N | Imidazolinone | Imazaquin |
| 5K3S | Pyrimidinyl-benzoate | Bispyribac-sodium |
| 5K6R | Sulfonylaminocarbonyltriazolinone | Thiencarbazone-methyl |

Broader herbicide-class coverage than PPO's single 1SEZ structure had. Arabidopsis
numbering is also the field-standard convention for ALS mutations (Pro197, Trp574,
Ser653, etc. are always reported in this numbering) - less of a numbering-offset
problem than PPO's three-way tobacco/waterhemp/palmeri system, **but** the
crystallized sequence (1Z8N chain, starts "TFISRFAPDQ...") looks like a
transit-peptide-cleaved mature fragment, not the full preprotein - so raw sequence
position ≠ literature position without an alignment-derived offset. Not yet resolved.

## Candidate real accessions - Amaranthus palmeri (continuing species used in Phase 1)

**Peer-reviewed source (preferred):** Larran, Palmieri, Perotti, Lieber, Tuesca &
Permingeat, "Target-site resistance to ALS-inhibiting herbicides in *Amaranthus
palmeri* from Argentina," *Pest Manag Sci* 2017 (matches DOI 10.1002/ps.4662 found
via literature search). Deposited accessions **ASL69930-ASL69937** (8 sequences,
669 aa each).

Raw pairwise diffs (using ASL69930 as reference - **not yet confirmed this is the
correct susceptible/wild-type genotype**, see caveat below):

| Accession | Raw diff positions vs ASL69930 | Candidate mutation (unconfirmed numbering) |
|---|---|---|
| ASL69931 | 652 (S→N) | possible Ser653Asn |
| ASL69932 | 573 (W→L) | possible Trp574Leu |
| ASL69933 | 573 (W→L), 600 (M→I) | possible Trp574Leu + unclear second change |
| ASL69934 | 117 (A→S), 282 (A→D) | unclear - doesn't cleanly match a classic hotspot at raw numbering |
| ASL69935 | 282 (A→D), 652 (S→N) | double mutant candidate |
| ASL69936 | 79 (P→H), 282 (A→D), 652 (S→N) | triple - two of three unclear |
| ASL69937 | 652 (S→N) | possible Ser653Asn |

**Caveat - all 8 sequences share the same 8 N-terminal differences from ASL69930**
(positions 4, 6, 10, 11, 12, 16, 22, 31), before any of the above. This looks like
ASL69930 has a different transit-peptide sequence/length than the other seven, not
a real biotype difference - likely means ASL69930 is *not* a clean wild-type
reference to diff against. Needs resolving before trusting any position number
above; the "cleanest" internal reference is probably one of the other seven, not
ASL69930. **Numbering also not yet converted to the standard Arabidopsis-based
convention** - the raw positions above may not equal the literature names even
after fixing the reference-choice issue.

**Lower-confidence source (flagging, not recommending yet):** Palmieri, Permingeat
& Perotti, "Comparative analysis of five resistant acetolactate synthase isoforms
from *Amaranthus palmeri*" - GenBank accessions QYC94980/QYC94981 (and reportedly
3 more not yet located). **This is marked "Unpublished" in the GenBank record
itself** - a direct database submission, not a peer-reviewed paper. Same
verification standard problem as the original QBB0236x mistake in Phase 1 -
recommend treating this as lower-priority until/unless it turns out to be published
elsewhere, or cross-confirmed against a peer-reviewed source.

## Candidate structural/kinetic validation paper (Dayan-2010 role for ALS)

"Effects of resistance mutations of Pro197, Asp376 and Trp574 on the
characteristics of acetohydroxyacid synthase (AHAS) isozymes" (DOI 10.1002/ps.4889)
- found via literature search, not yet read in full. Title suggests direct kinetic
characterization of exactly three of the five target mutations - a plausible
validation-gate anchor paper, but needs the same full-text verification pass PPO's
Dayan/Hao/Giacomini papers got before relying on it.

## Open questions for you (domain sign-off needed)

1. Is the Larran et al. 2017 Argentine population dataset (ASL69930-69937) the
   right primary source to build the ALS mutation set from, or is there a
   better-established reference paper/dataset you'd rather anchor to (e.g., a US
   Palmer amaranth population, given the PPO work's continuity with that context)?
2. Which accession should serve as the wild-type/susceptible reference within this
   set, given the apparent N-terminal issue with ASL69930?
3. Do you want Ala122 and Pro197 candidates specifically sourced (neither turned up
   in this particular 8-accession set - Pro197 does have its own dedicated paper,
   "A New Pro-197-Ile Mutation in *Amaranthus palmeri*," DOI 10.3390/plants14040525,
   not yet pulled), or is a subset of the five classic positions acceptable for the
   ALS pilot (mirroring how PPO's pilot only covered 4, not every documented
   mutation)?
4. Should the "Unpublished" QYC94980/94981 pair be excluded entirely, or kept with
   an explicit lower-confidence flag the way PPO's non-causal background variants were?
