# ALS/AHAS Phase 2 pilot — mutation candidates (resolved)

All sign-off items resolved directly from Larran et al. 2017's own text (PDF now in
`docs/references/Larran_et_al_2017_ALS_Argentina.pdf`). Working dataset is
`als_mutations.csv`. This file keeps the resolution trail for reference.

## Scope (resolved)

**Pilot covers Trp574Leu and Ser653Asn only.** Ala122 and Pro197 are dropped from
this pilot's scope - they'd be scope creep on what's meant to be a quick second
validation-gate check reusing PPO's now-proven pipeline, not a full ALS survey.
They remain fair game for a later, fuller ALS pass if warranted.

## Reference/wild-type accession (resolved from the paper's own Table 4)

Larran et al. 2017, *Pest Manag Sci*, DOI 10.1002/ps.4662, Table 4 ("Amino acid
differences found in the ALS open reading frame of resistant *Amaranthus palmeri*
populations compared with the susceptible population"):

| Population | Allelic version (frequency) | Substitution | Accession |
|---|---|---|---|
| S | A (8/8) | — (wild-type) | **KY781916** |
| R1 | C (1/8) | **W574L** | **KY781918** |
| R2 | H (2/8) | **S653N** | **KY781923** |

**S/KY781916 is explicitly labeled the susceptible/wild-type population in the
paper's own text and table** - not inferred by elimination. All 8/8 S-population
clones were identical (100% amino acid identity), so there's no internal ambiguity
about the reference.

**Cross-check against the earlier ASL-prefixed protein accessions:** confirmed
byte-identical - ASL69930.1 ≡ KY781916.1 (S/WT), ASL69932.1 ≡ KY781918.1 (W574L),
and both ASL69931.1 and ASL69937.1 ≡ KY781923.1 (S653N - matches Table 4's stated
2/8 frequency for this allelic version, i.e. two separately-deposited identical
clones). The original elimination-based guess (using ASL69930 as the diff baseline)
turned out to be the correct sequence, but per the process this project follows,
it wasn't trusted until the paper's own text confirmed it - the earlier "blocked,
not resolved by elimination" status was the right call even though the guess
happened to be right.

## Numbering (resolved - no offset needed)

The paper states substitutions are numbered per the *Arabidopsis thaliana* ALS
convention (except A282D, out of scope, which uses a third reference sequence -
*Amaranthus retroflexus* - because it falls in an indel). **Verified directly
against the 1Z8N crystal structure's own PDB numbering:** chain A residue 574 is
TRP and residue 653 is SER - matching the literature convention exactly, with no
alignment-derived offset required (unlike PPO's three-way tobacco/waterhemp/palmeri
numbering). The crystallographers already used the standard convention.

## Excluded from the working mutation set

**QYC94980 / QYC94981** ("Comparative analysis of five resistant acetolactate
synthase isoforms from *Amaranthus palmeri*," Palmieri, Permingeat & Perotti) -
**excluded**. Marked "Unpublished" in the GenBank record itself - a direct database
submission, not a peer-reviewed paper, the same category of problem as the original
QBB0236x mistake in Phase 1. Tag: `unpublished_lower_confidence`. Kept as a record
here only; not used in anything the manuscript relies on.

## Active-site reference — resolved without needing McCourt et al. 2006's full text

McCourt et al. 2006 (*PNAS* 103:569-573, the structural paper cited in Larran et
al.'s own reference list) would be the natural Heinemann-2007-equivalent source for
a defined active-site residue core, but a scite full-text fetch attempt for it came
back empty. Rather than pushing further on that source, the active site was defined
directly from the 1Z8N structure itself: residues in contact with the bound
imazaquin ligand (1Z8N is a real herbicide-bound crystal structure, same approach
used to confirm PPO's R98-OMN contact). This sidesteps the paywall/fetch-limit issue
entirely and is arguably more faithful to the original panel-review design (compute
structural features directly, don't lean on secondary literature more than needed).

## Candidate structural/kinetic paper, lower priority now

"Effects of resistance mutations of Pro197, Asp376 and Trp574 on the
characteristics of acetohydroxyacid synthase (AHAS) isozymes" (DOI 10.1002/ps.4889)
covers Trp574 (in scope) but leads with Pro197/Asp376 (out of scope) - not pursued
further given the narrowed pilot scope. Revisit if a Ser653-specific validation
anchor is wanted later.
