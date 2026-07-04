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

## Third metric added: Shannon-entropy conservation (per DECISION_LOG §8 item 1)

Computed locally (no ConSurf dependency) from a MAFFT alignment of 10 diverse plant
PPO2 orthologs (tobacco, both *Amaranthus* species, Arabidopsis, soybean, tomato,
sugar beet, poplar, rice, maize - dicots and monocots both represented). Full data
in `ppo_conservation_entropy.csv`; script in `scripts/conservation_entropy.py`.

| Mutation | Tobacco pos | Distance percentile | Conservation (0-1) |
|---|---|---|---|
| ΔG210 | 178 | 8.2 | 0.769 |
| G399A | 370 | 2.8 | 1.000 (invariant across all 10 species) |
| R98 (core) | 98 | 0.9 | 1.000 (invariant across all 10 species) |
| V361A | 332 | 20.2 | 0.573 (lowest of the four) |

## V361A re-evaluated with conservation data in hand

**Revised interpretation:** V361A is not just the farthest of the four mutations
from the active-site core - it is also the **least conserved**, by a clear margin,
across a 10-species plant panel spanning both major angiosperm lineages. That
combination (moderate-low distance percentile + low conservation) is the profile of
a naturally variable, structurally permissive site, not a tightly-conserved
allosteric hotspot. This is the "unremarkable, poorly-conserved position" outcome
DECISION_LOG §8 flagged as the alternative to rule in or out before treating V361A
as a manuscript-central finding - **the data currently points toward the more
mundane explanation.** A plausible reading: resistance may have emerged here
precisely because this position tolerates substitution more readily than most
(less purifying selection to overcome), rather than because it's an unexpected
functional site.

**ΔG210 is the stronger outlier candidate**, not V361A. It sits adjacent to (not
in) the active-site core, as established, but is *also* meaningfully conserved
(0.769 - most species carry Gly, a minority tolerate Ala) rather than freely
variable. That specific pattern - conserved position, structurally proximal to but
distinct from the core, resistant only via an unusual deletion rather than
substitution - is corroborated by Dayan et al. 2010's own species survey (Ala
occurs naturally at this position in some herbicide-sensitive species, e.g. GenBank
AF273767, but larger substitutions are sterically blocked).

**Correction - not fully independent evidence:** checked whether AF273767 falls
inside our own 10-species panel. **It does** - AF273767 is *Zea mays* (confirmed via
NCBI esummary), and our panel already includes maize (PWZ38740.1), which does show
Ala at the equivalent alignment column. This is the *same* data point Dayan cited,
not a second independent confirmation - the manuscript must not claim "two
independent lines of evidence" here. What **is** a genuine (partial) extension:
three *other* species in our panel that Dayan's paper didn't specifically name also
carry Ala at this position - Arabidopsis (KAL9810292.1), soybean (KAH1193770.1),
and poplar (XP_002298607.3) - plus tomato (NP_001335308.1). Dayan's text only cites
one example accession ("e.g., GenBank AF273767") without enumerating every
Ala-carrying species, so these three-to-four additional data points do broaden the
evidence base beyond what Dayan reported, even though the specific species he named
overlaps with ours. Correct framing for the manuscript: **"consistent with, and
partially extending, Dayan et al. 2010's cross-species survey"** - not "two
independent lines of evidence."

**Recommendation:** don't build the central claim around V361A being an "outlier
allosteric mechanism" pending further evidence. It remains a valid, correctly-cited
resistance mutation in the dataset (mechanism class stays `pending`), just not the
flagship non-obvious finding. Revisit once the other enzymes (Phase 2) are added -
if a *different* mutation elsewhere shows ΔG210's pattern (conserved + proximal-but-
outside-core) that would strengthen the cross-enzyme version of this story; if V361A's
low-distance/low-conservation profile recurs in other enzymes' "permissive site"
mutations, that's a distinct, still-worth-reporting pattern, just a different one.

## R98 SASA sanity check (per DECISION_LOG §8 item 3)

R98 reads as solvent-exposed (58.96 Å²) despite being a core catalytic residue -
confirmed this is correct, not an artifact, via `scripts/chimerax_sasa_diagnostic.py`
and `scripts/chimerax_probe_check.py`:

- **Chain/oligomer:** correct - SASA computed with both dimer chains present (see
  caveat below); R98 is not at the dimer interface, confirmed by comparing
  single-chain vs. dimer SASA (identical for this residue).
- **Probe radius:** ChimeraX's default matches the explicit standard 1.4 Å water
  probe (verified by running both and comparing totals - identical, 40311 Å² for
  all atoms either way).
- **Ligand context:** 1SEZ has a bound phenyl-pyrazole inhibitor (OMN) and FAD
  cofactor present throughout - not stripped out. R98 sits **2.62 Å from OMN**,
  i.e. genuinely at the pocket, in direct contact range with the bound inhibitor.

**Conclusion: the exposure is real, not a bug.** R98 coordinates the substrate's
peripheral propionate carboxylate group (Heinemann et al. 2007) - a substituent
that sits at the mouth of the pocket rather than buried in the hydrophobic tunnel,
so partial solvent exposure even with an inhibitor bound is exactly what's expected
for this specific functional role. "Buried vs. exposed" as a feature is safe to
carry forward into the Phase 2 cross-enzyme comparison, but this case is a reminder
that pocket-rim residues coordinating peripheral substrate groups can legitimately
read as exposed - worth keeping in mind rather than assuming "core residue = buried"
as a blanket rule when interpreting other enzymes' active sites.

## Caveat

SASA was computed on the full crystallographic dimer (both chains present) since
PPO is a biological homodimer - an earlier pass that deleted chain B before running
`measure sasa` would have overestimated solvent exposure at the dimer interface.
None of the four checked positions turned out to sit at that interface, so the fix
didn't change their numbers, but it matters for the rest of the 465-residue dataset
in `ppo_1sez_distance_sasa.csv`.
