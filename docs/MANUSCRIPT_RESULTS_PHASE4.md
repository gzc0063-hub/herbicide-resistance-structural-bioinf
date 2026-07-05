# Phase 4 Results Draft

## Structural-Zone Enrichment Across Target Families

Accepted target-site resistance positions were pooled across PPO, ALS/AHAS,
EPSPS, and ACCase after joining each mutation row to its family-specific
distance-to-active-site-core percentile, RSA, and conservation metrics. Repeated
accession rows at the same structural site were de-duplicated for the
permutation analysis so that biological replicate rows did not overweight a
single residue position.

Within-family permutation testing showed that accepted resistance positions fall
substantially closer to the active-site core than random residues from the same
structure. PPO, ALS/AHAS, and ACCase each showed strong enrichment for low
distance-to-core percentiles. EPSPS showed the same directional pattern, but the
current EPSPS set contains only one accepted mutation position and should be
treated as descriptive rather than a family-level statistical test.

The current family-level results are:

| Family | Unique positions | Observed mean percentile | Random mean percentile | Empirical p-value |
|---|---:|---:|---:|---:|
| ACCase | 6 | 10.68 | 49.81 | 0.000200 |
| ALS/AHAS | 2 | 4.64 | 49.94 | 0.002200 |
| EPSPS | 1 | 12.87 | 50.35 | 0.131887 |
| PPO | 4 | 8.01 | 50.35 | 0.000400 |

## Direct-Core and Non-Core Resistance Positions

The unique-position mechanism screen separates direct active-site-core positions
from adjacent and more distal non-core candidates. Direct-core examples include
ALS Trp574Leu and Ser653Asn, PPO R98G/R98M, and ACCase Ile1781Leu/Ile2041Asn
under the current ligand-contact core definitions.

The non-core positions are central to the manuscript's novelty. PPO deltaG210 is
near the active-site zone but mechanistically distinctive because the supporting
literature describes helix/deletion effects that are not captured by distance
alone. EPSPS Pro106Ser is directionally close to the glyphosate/S3P site but is
best treated as an allosteric/hinge-position case, not a direct ligand-contact
substitution. ACCase Cys2088Arg is the most distal accepted ACCase position in
the current screen, yet remains within the broader dimer-interface resistance
zone.

## Review-Driven Limitation Statement

The static pipeline should be described as a structural context and enrichment
resource, not a dynamic binding model. Distance percentile, RSA, and conservation
identify where accepted resistance positions sit within each target family, but
they do not estimate ligand binding free energy, induced-fit cost, solvent
desolvation, loop breathing, or mutant-state thermodynamics. Literature
kinetic, docking, MD, and free-energy studies should be used to interpret
mechanisms where available.

This framing makes the external review's main critique part of the manuscript's
scope discipline rather than a reason to build a new MD pipeline.

