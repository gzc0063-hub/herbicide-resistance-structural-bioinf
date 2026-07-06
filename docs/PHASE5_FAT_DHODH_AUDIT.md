# Phase 5 FAT/DHODH Emerging-Target Audit

Status: starter audit artifact.

This note starts Phase 5 as an evidence audit, not as a pipeline integration.
FAT and DHODH should not be added to `scripts/build_phase4_tables.py`, the
pooled enrichment tests, or the manuscript tables until mutation evidence and
structure/model mapping pass the same gate used for PPO, ALS, EPSPS, ACCase,
and HPPD.

## Decision

Audit FAT first. Hold DHODH behind mutation and model-source verification.

The current evidence state is asymmetric:

- FAT/acyl-ACP thioesterase has plant structural routes already identified,
  including Lemna inhibitor-complex structures 8P8K, 8QRT, and 8QS0 and
  Arabidopsis FatA fragment structures 7HQQ through 7HQU.
- DHODH has tetflupyrolimet target/MoA literature support, but the structured
  RCSB search found 278 DHODH polymer entities across 273 entries with zero
  plant-like organisms. A specific plant structure, paper-supplied coordinates,
  or defensible model route is still needed.

## Evidence Gate

No target can move from Phase 5 audit to a risk table or pooled analysis until
all of these are satisfied:

1. Target/MoA evidence is traceable to primary literature.
2. Mutation evidence is traceable to a primary source.
3. The mutation is classified as weed-evolved, lab-selected, engineered, or
   hypothetical.
4. Species, exact substitution, sequence/accession or coordinate reference, and
   residue-numbering system are recorded.
5. A structure or model maps the residue into the target's structural frame.
6. The limitation statement is clear enough that the project does not overclaim
   resistance mechanism, field evolution, or structural certainty.

## Target Status

| Target | Current status | Go/no-go |
|---|---|---|
| FAT/acyl-ACP thioesterase | Plant structures and inhibitor-complex entries are available. Mutation-source evidence still needs primary-source verification. | `audit_first` |
| DHODH | Tetflupyrolimet/DHODH target literature is identified. No public plant DHODH RCSB structure was found by the structured search. Mutation/model evidence remains unverified. | `hold_model_source` |

## FAT Next Questions

- What is the exact "FAT-A R171-region" substitution, if any?
- Which species and numbering system does it use?
- Is the evidence weed-evolved, lab-selected, engineered, or hypothetical?
- Is there a sequence accession or structure/model mapping that connects the
  source residue to the candidate plant FAT structures?
- Does the mutation justify a separate Phase 5 risk table, or only a future-work
  note?

## DHODH Next Questions

- Which primary source establishes tetflupyrolimet/DHODH target biology for the
  relevant plant/weed context?
- Are there any verified DHODH resistance mutations, and are they field-evolved,
  lab-selected, engineered, or hypothetical?
- Is there a public plant DHODH structure, paper-supplied coordinate/model, or
  usable modeling template?
- If modeling is needed, is SWISS-MODEL sufficient or should AlphaFold/ColabFold
  be used with clearly recorded provenance?

## Do Not Do Yet

- Do not add FAT or DHODH rows to the Phase 4 pooled mutation table.
- Do not add FAT or DHODH to the cross-family enrichment analysis.
- Do not describe any unverified variant as weed-evolved TSR.
- Do not claim a public plant DHODH structure unless a specific accession or
  paper-supplied coordinate/model source is identified.
