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
structure. PPO, ALS/AHAS, ACCase, and now EPSPS each show statistically
significant enrichment for low distance-to-core percentiles. EPSPS was expanded
from one accepted position (Pro106Ser) to two (adding Thr102Ile, part of the
naturally-evolved TIPS double mutation in *Eleusine indica*), moving it from a
purely descriptive single point to a genuine, significant two-position test.
ALS/AHAS was expanded from four accepted positions to five (adding Asp376Glu,
verified in *Sinapis alba*).

The current family-level results are:

| Family | Unique positions | Observed mean percentile | Random mean percentile | Empirical p-value |
|---|---:|---:|---:|---:|
| ACCase | 6 | 13.24 | 50.20 | 0.0003 |
| ALS/AHAS | 5 | 4.64 | 50.03 | 0.0001 |
| EPSPS | 2 | 9.37 | 50.03 | 0.0147 |
| PPO | 4 | 8.01 | 49.86 | 0.0004 |

A global combined permutation test additionally pools every unique accepted
position across all four families into one cohort, drawing random same-size
sets from the combined background residue pool:

| Combined test | Unique positions | Observed mean percentile | Random mean percentile | Empirical p-value |
|---|---:|---:|---:|---:|
| All positions, all families | 17 | 9.02 | 50.13 | 0.0001 |
| Non-core positions, all families | 8 | 14.51 | 50.22 | 0.0001 |

This pooled test is a simpler statistic than a family-random-effects mixed model
(no R/`rpy2`/`lme4` was available in this project's computing environment), but
it gives a single, more powerful cross-family statistic than any per-family test
alone, and is the strongest evidence in this resource that the non-core
enrichment signal is not an artifact of any one family's core definition or
sample size.

Each accepted position also now carries a static biophysical perturbation score
(absolute wild-type-to-mutant deltas in side-chain bulkiness, Kyte-Doolittle
hydropathy, and formal charge), reported alongside distance percentile and RSA
as an orthogonal, transparent property-difference axis. This is not a
physics-based free-energy estimate - no licensed thermodynamic tool (FoldX,
DDGun) was available in this environment - and should not be read as one.

## Direct-Core and Non-Core Resistance Positions

The unique-position mechanism screen separates direct active-site-core positions
from adjacent and more distal non-core candidates. Direct-core examples include
ALS Trp574Leu, Ser653Asn, Ala122Ser, Pro197Ala, and Asp376Glu, PPO R98G/R98M,
ACCase Ile1781Leu/Ile2041Asn, and EPSPS Thr102Ile under the current
ligand-contact core definitions. Thr102Ile carries its own caveat: it has only
ever been reported as part of the TIPS double mutation with Pro106Ser, never
observed or shown viable alone.

The non-core positions are central to the manuscript's novelty. PPO deltaG210 is
near the active-site zone but mechanistically distinctive because the supporting
literature describes helix/deletion effects that are not captured by distance
alone. EPSPS Pro106Ser is directionally close to the glyphosate/S3P site but is
best treated as a binding-site-adjacent case, not a direct ligand-contact
substitution. ACCase Cys2088Arg is the most distal accepted ACCase position in
the current screen, yet remains within the broader dimer-interface resistance
zone. Current ACCase distance/RSA values come from the SWISS-MODEL weed
CT-domain homodimer, with active-site-core membership transferred from 1UYS
H1L-contact residues because SWISS-MODEL excluded the ligand.

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
