# PPO Phase 1 validation gate — results

Pipeline: `scripts/chimerax_distance_sasa.py` on 1SEZ (tobacco PPO2 crystal structure,
both chains present for correct dimer-context SASA, chain A residues reported).
Active-site core: Heinemann et al. 2007 four residues (tobacco numbering Arg98,
Phe392, Leu356, Leu372). Distance = min CA-CA distance to nearest core residue.
Percentile rank = 0 (closest in the whole chain) to 100 (farthest).

Tobacco-equivalent positions from `data/processed/numbering_maps.json` (independently
derived via pairwise alignment, cross-validated against the hardcoded numbering key
for the two positions where both exist - R98/128 and G399/370 matched exactly).

| Mutation | Tobacco position | Distance to core (Å) | Percentile rank | SASA (Å²) |
|---|---|---|---|---|
| ΔG210 | 178 | 8.37 | 8.2 | 0.5 (buried) |
| G399A | 370 | 4.20 | 2.8 | 0.0 (buried) |
| V361A | 332 | 11.73 | 20.2 | ~0 (buried) |
| R98G/R98M | 98 (core itself) | 0.00 | 0.9 | 59.0 (solvent-exposed) |

## Validation gate: PASS

The gate (per the redefined scope in `docs/DECISION_LOG.md` §7): does the static
distance metric place Gly210 **outside** the Heinemann four-residue core, consistent
with Dayan et al. 2010's qualitative "adjacent to, not in, the active site" finding?

**Yes.** Gly210 sits in the top ~8% closest residues in the whole chain (spatially
proximal, consistent with "adjacent to") but at a real 8.37 Å CA-CA gap from the
nearest core residue and essentially fully buried (0.5 Å² SASA) rather than lining
the pocket itself (consistent with "not in" the defined catalytic core). This is a
directional, geometric confirmation of Dayan's finding using only the static
structure - no MD required, matching the scope decision.

## A secondary observation worth flagging

**V361A is farther from the active-site core (percentile 20.2) than ΔG210 or
G399A**, despite being causal for resistance (per Nie et al. 2023's site-directed
mutagenesis). Its mechanism class is still marked `pending` in the dataset - no
structural paper has resolved it yet. This is exactly the kind of "doesn't fit the
expected near-active-site pattern" case the panel review (DECISION_LOG §2, fix #5)
said would be the more citable finding if it turned up. Worth keeping an eye on once
the other enzymes are added - if V361A's relative distance holds up as an outlier
across the full permutation-test analysis (Phase 4), it's a candidate for the
"allosteric-acting resistance" angle the panel recommended foregrounding.

## Caveat

SASA was computed on the full crystallographic dimer (both chains present) since
PPO is a biological homodimer - an earlier pass that deleted chain B before running
`measure sasa` would have overestimated solvent exposure at the dimer interface.
None of the four checked positions turned out to sit at that interface, so the fix
didn't change their numbers, but it matters for the rest of the 465-residue dataset
in `ppo_1sez_distance_sasa.csv`.
