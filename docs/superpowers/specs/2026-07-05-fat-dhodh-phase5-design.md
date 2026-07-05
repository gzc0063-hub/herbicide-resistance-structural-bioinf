# Phase 5 FAT/DHODH Validation-Gate Design

Date: 2026-07-05

## Goal

Extend the project beyond the current Phase 4 manuscript set by evaluating FAT
and DHODH as emerging herbicide target families. The expansion must preserve the
project rule: no target family enters the pooled resistance-position enrichment
analysis unless its mutation evidence and structural anchor pass the same
traceability standard used for PPO, ALS/AHAS, EPSPS, and ACCase.

## Current Evidence Snapshot

### FAT

FAT is structurally actionable first. RCSB structured entity searches found plant
acyl-ACP thioesterase structures:

- Arabidopsis FatA fragment-screen structures, for example 7HQQ-7HQU. RCSB marks
  these as "To Be Published" PanDDA depositions.
- Lemna acyl-ACP thioesterase inhibitor-complex structures:
  - 8P8K, "A Study in Scaffold Hopping: Discovery and Optimization of
    Thiazolopyridines as Potent Herbicides That Inhibit Acyl-ACP Thioesterase,"
    Journal of Agricultural and Food Chemistry, DOI 10.1021/acs.jafc.3c02490.
  - 8QRT and 8QS0, "Discovery and optimization of spirocyclic lactams that
    inhibit acyl-ACP thioesterase," Pest Management Science, DOI
    10.1002/ps.8015.

The open question is mutation evidence. The original project plan mentions
"FAT-A R171-region" lab-generated resistant variants, but the exact mutation,
species, accession/source, and whether it is weed-evolved versus lab-selected
remain unverified in the current repo.

### DHODH

DHODH has a strong mode-of-action story but not yet a public plant structure in
RCSB:

- Tetflupyrolimet discovery paper: "Bioisosteric Tactics in the Discovery of
  Tetflupyrolimet: A New Mode-of-Action Herbicide," Journal of Agricultural and
  Food Chemistry, DOI 10.1021/acs.jafc.3c01634.
- Crossref also lists a 2026 book chapter, "Validation of Dihydroorotate
  Dehydrogenase as a Herbicide Target: Discovery of Tetflupyrolimet," DOI
  10.1002/9783527843879.ch16.
- Structured RCSB search for polymer entity description containing
  "dihydroorotate dehydrogenase" returned 278 DHODH polymer entities across 273
  unique entries; metadata filtering found zero plant-like organisms among those
  entries. The true DHODH structures are currently human, rat, microbial, parasite,
  and fungal/protist systems.

The open questions are mutation evidence and structure/model route. If no public
plant DHODH structure or paper-supplied coordinates exist, DHODH needs a
homology-model or AlphaFold/SWISS-MODEL route before metrics can be computed.

## Scope Decision

Phase 5 should start as an "emerging targets / resistance-risk" module, not an
immediate rewrite of Phase 4.

Do not merge FAT or DHODH into the pooled Phase 4 enrichment table until each
target has:

1. A verified target enzyme and herbicide-relevant active-site or inhibitor-site
   definition.
2. A usable structure or model with residue numbering mapped to the mutation
   source.
3. At least one verified target-site substitution or experimentally selected
   resistance variant with primary-source support.
4. A clear classification of evidence type:
   - weed-evolved TSR,
   - lab-selected resistance,
   - engineered/crop-tolerance,
   - structure-only target biology,
   - or hypothetical/future-risk.

Only weed-evolved or otherwise explicitly accepted TSR rows should enter the
main Phase 4-style pooled enrichment table. Lab-selected FAT/DHODH mutants can
be analyzed in a separate Phase 5 table and figure as prospective risk evidence.

## Recommended Approach

### Approach A: FAT-first, DHODH audit in parallel

Start with FAT because RCSB already has plant inhibitor-complex structures. Audit
the FAT mutation evidence next. If a verified mutation exists, build FAT metrics
using the best Lemna inhibitor-bound structure as the first structural anchor,
then decide whether Arabidopsis FatA fragment structures help with residue
mapping or conservation.

Keep DHODH in source-audit mode until the exact lab mutant and a plant
structure/model route are identified.

This is the recommended route because it produces one likely structure-backed
Phase 5 target quickly while avoiding unsupported DHODH claims.

### Approach B: DHODH-first

Start with tetflupyrolimet/DHODH because it is the newest mode-of-action story.
This is scientifically attractive but structurally riskier. It likely requires a
modeling step before the project can compute distance/SASA/RSA metrics, and the
mutation evidence remains unverified in the current repo.

Use this only if the user supplies the DHODH paper, coordinates, or exact lab
mutation source.

### Approach C: Treat both as contrast-only

Create a short manuscript appendix stating that FAT and DHODH are emerging
targets with useful target biology but insufficient verified TSR evidence for
the current pooled analysis. This is safest for submission but does not advance
the project as much.

## Proposed Phase 5 Outputs

Initial audit outputs:

- `docs/PHASE5_FAT_DHODH_AUDIT.md`
- `data/processed/phase5_target_status.csv`
- updated `docs/HANDOFF_NEXT_STEPS.md`
- updated `docs/DECISION_LOG.md`

If FAT passes:

- `data/raw/<fat_structure>.pdb`
- `data/processed/fat_mutations.csv`
- `data/processed/fat_<structure>_distance_sasa.csv`
- `data/processed/fat_conservation_entropy.csv`
- tests for FAT structure mapping and output invariants

If DHODH passes or gets a model:

- `data/raw/<dhodh_structure_or_model>.pdb`
- `data/processed/dhodh_mutations.csv`
- `data/processed/dhodh_<structure_or_model>_distance_sasa.csv`
- `data/processed/dhodh_conservation_entropy.csv`
- tests for DHODH structure/model mapping and output invariants

## Stop Conditions

Stop before pipeline integration if:

- the mutation is not primary-source verified;
- the evidence is only crop-tolerance engineering but is being described as weed
  TSR;
- the structure is not the target enzyme family;
- a model cannot be tied to a sequence with clear numbering;
- the active-site or inhibitor-site core cannot be defined reproducibly.

## Next Implementation Plan

1. Build `docs/PHASE5_FAT_DHODH_AUDIT.md` from primary-source and RCSB evidence.
2. Add a small status CSV summarizing FAT and DHODH evidence class and go/no-go
   state.
3. Update handoff/decision logs.
4. If FAT mutation evidence passes, implement FAT metrics first.
5. Keep DHODH behind a modeling/evidence gate unless a verified plant structure
   or model input is supplied.
