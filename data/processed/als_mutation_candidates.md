# ALS/AHAS Phase 2 pilot — mutation candidates

Scope and sign-off decisions applied below; one item remains genuinely blocked
pending a paywalled source (see status).

## Scope (resolved)

**Pilot covers Trp574Leu and Ser653Asn only.** Ala122 and Pro197 are dropped from
this pilot's scope - they'd be scope creep on what's meant to be a quick second
validation-gate check reusing PPO's now-proven pipeline, not a full ALS survey.
They remain fair game for a later, fuller ALS pass if warranted.

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
numbering is also the field-standard convention for ALS mutations - less of a
numbering-offset problem than PPO's three-way tobacco/waterhemp/palmeri system,
**but** the crystallized sequence (1Z8N chain, starts "TFISRFAPDQ...") looks like a
transit-peptide-cleaved mature fragment, not the full preprotein - so raw sequence
position ≠ literature position without an alignment-derived offset. Not yet resolved.

## Candidate real accessions - Amaranthus palmeri (continuing species used in Phase 1)

**Source:** Larran, Palmieri, Perotti, Lieber, Tuesca & Permingeat, "Target-site
resistance to acetolactate synthase (ALS)-inhibiting herbicides in *Amaranthus
palmeri* from Argentina," *Pest Manag Sci* 2017, DOI 10.1002/ps.4662. Deposited
accessions **ASL69930-ASL69937** (8 sequences, 669 aa each).

Raw pairwise diffs (using ASL69930 as a provisional diff baseline only - **not
confirmed as the correct susceptible/wild-type genotype**, see status below):

| Accession | Raw diff positions vs ASL69930 | Candidate mutation (unconfirmed numbering) |
|---|---|---|
| ASL69931 | 652 (S→N) | possible Ser653Asn |
| ASL69932 | 573 (W→L) | possible Trp574Leu |
| ASL69933 | 573 (W→L), 600 (M→I) | possible Trp574Leu + unclear second change (out of pilot scope) |
| ASL69934 | 117 (A→S), 282 (A→D) | out of pilot scope (neither Trp574 nor Ser653) |
| ASL69935 | 282 (A→D), 652 (S→N) | Ser653Asn candidate, plus an out-of-scope second change |
| ASL69936 | 79 (P→H), 282 (A→D), 652 (S→N) | Ser653Asn candidate, plus two out-of-scope changes |
| ASL69937 | 652 (S→N) | possible Ser653Asn |

Cleanest single-mutation candidates for the pilot's narrowed scope: **ASL69932**
(Trp574Leu candidate, one clean diff besides the shared N-terminal block) and
**ASL69931 or ASL69937** (Ser653Asn candidate, one clean diff besides the shared block).

**Status: reference accession still blocked, not resolved by elimination.** All 8
sequences share the same 8 N-terminal differences from ASL69930 (positions 4, 6,
10, 11, 12, 16, 22, 31) before any of the diffs above. Per instruction, this is
more likely a different transcript start than an error, but ASL69930 is **not**
being used as the wild-type baseline until Larran et al. 2017's own methods or
supplementary text confirms which accession is the labeled susceptible/wild-type
population sample. Wiley blocked automated fetch attempts against this DOI (see
`CONTRIBUTING.md`) - **waiting on the user to supply the PDF directly.**

## Excluded from the working mutation set

**QYC94980 / QYC94981** ("Comparative analysis of five resistant acetolactate
synthase isoforms from *Amaranthus palmeri*," Palmieri, Permingeat & Perotti) -
**excluded**. Marked "Unpublished" in the GenBank record itself - a direct database
submission, not a peer-reviewed paper, the same category of problem as the original
QBB0236x mistake in Phase 1. Tag: `unpublished_lower_confidence`. Kept as a record
here only; not used in anything the manuscript relies on.

## Candidate structural/kinetic validation paper (Dayan-2010 role for ALS)

"Effects of resistance mutations of Pro197, Asp376 and Trp574 on the
characteristics of acetohydroxyacid synthase (AHAS) isozymes" (DOI 10.1002/ps.4889)
- found via literature search, not yet read in full, and covers Pro197/Asp376
(now out of pilot scope) alongside Trp574 (in scope). Given the scope narrowing,
this paper's usefulness as the ALS validation-gate anchor is now partial at best -
revisit once Trp574Leu/Ser653Asn numbering is resolved to see if it's still the
right anchor, or if a Ser653-specific paper is a better fit.

## Next step

Once the Larran et al. 2017 PDF is available, confirm the wild-type/susceptible
accession from its text, then proceed with numbering resolution (align to 1Z8N/
Arabidopsis) and the ChimeraX distance/SASA/conservation pipeline for Trp574Leu and
Ser653Asn only, mirroring PPO's Phase 1 pipeline exactly.
