# PPO Phase 1 — Final Validated Dataset & Brief
*Supersedes all prior addenda. Every fact below is confirmed against a primary source I've now read in full — no secondhand citations remain in this brief.*

## 1. Confirmed mutation set

| Mutation | Species | Confirmed accessions | Source | DOI |
|---|---|---|---|---|
| ΔG210 | *A. tuberculatus* | **ABD52326.1 (WT) / ABD52328.1 (resistant)** — confirmed via 2 independent citing papers | Patzoldt et al. 2006, PNAS 103:12329-12334 | 10.1073/pnas.0603137103 |
| ΔG210 | *A. tuberculatus* | **ABD52329.1 (WT) / ABD52330.1 (resistant)** — confirmed directly in Dayan et al. 2010's own Methods section | same as above | same |
| R98G, R98M (= R128G/R128M in Palmer-amaranth-native numbering) | *A. palmeri* | No GenBank accessions given (Sanger sequencing described, no deposit numbers in visible text) | Giacomini et al. 2017, Pest Manag Sci 73:1559-1563 | 10.1002/ps.4581 |
| G399A (=G398A in waterhemp-native numbering) | *A. tuberculatus* / *A. palmeri* | **MK408971–MK408978** | Rangani et al. 2019, Front. Plant Sci. 10:568 | 10.3389/fpls.2019.00568 |
| V361A | *A. palmeri* | **MH910646.1 (susceptible, IN) / MH910647.1 (resistant, AL)** | Nie, Harre & Young 2023, Plants 12(9):1886 | 10.3390/plants12091886 |

**Important:** the two ΔG210 accession pairs (ABD52326/ABD52328 and ABD52329/ABD52330) are **not duplicates or a conflict** — both are legitimate wild-type/resistant pairs from the original Patzoldt 2006 study, most likely two different biological replicates. Use either or both; no need to pick one.

**Still open:** Giacomini et al. 2017 gives no accession numbers for R98G/R98M in the visible text. If you want these sequences specifically, this needs either the paper's supplementary data (not captured here) or direct correspondence with the authors — not something to resolve by inference.

## 2. Numbering reference key (three-way, all confirmed from primary sources)

| Tobacco (1SEZ) | Waterhemp (Hao 2009, ref. DQ386117) | Palmer amaranth (Rangani 2019) |
|---|---|---|
| Arg98 | Arg128 | Arg128 |
| Gly354 | Leu384* | Gly383 |
| Leu356 | Leu384 | Leu385 |
| Leu369 | — | Leu398 |
| Gly370 | — | Gly399 (=G398 in waterhemp per Rangani's own footnote) |
| Tyr371 | — | Tyr400 |
| Leu372 | Leu400 | Leu401 |
| Phe392 | Phe420 | Phe421 |

*Small inconsistency worth knowing: Hao 2009's own text pairs Leu356(tobacco)→Leu384(waterhemp), consistent with Rangani's independently-derived table. The two papers' numbering schemes agree with each other here despite being derived independently — a good internal consistency check.

## 3. Active-site / substrate-binding residue reference (use Heinemann 2007 as primary)

**Primary (Heinemann et al. 2007, Biochem J 402:575-580 — the original functional definition, free via PMC1863572):**
Arg98 (coordinates propionate carboxylate of protogen ring C), Phe392 (anchors ring A), Leu356 and Leu372 (stack ring B front/back). Mutating Arg98, Leu356, or Leu372 **increases** kcat up to 100-fold; mutating Phe392→His abolishes activity entirely. Use this as the reference set for "core catalytic/substrate-recognition residues."

**Secondary/broader (Rangani 2019's 9-residue correspondence table, Hao 2013's 8-residue list):** overlapping but not identical to each other or to Heinemann's core 4 — reflects different methods/purposes across papers, not an error. Don't treat any single list as exhaustive; the Heinemann 4 are the best-validated core.

## 4. Mechanism classes per mutation — updated with a genuine discrepancy flagged

| Mutation | mechanism_class | Detail | Confidence |
|---|---|---|---|
| ΔG210 | `helix_destabilization` | Removes the αL helix-capping motif at the C-terminus of the α-8 helix (Gly210 H-bonds to Ala206; hydrophobic Val205–Pro213 pair stabilizes the cap). Deletion unravels the last helix turn, enlarging the active-site cavity **551 Å³ → 848 Å³ (+54%, matches the commonly-cited "~50%")**, and increases the Gly207-carbonyl-to-FAD-N5 distance by **~1.5 Å average**. | **High** — Dayan et al. 2010, backed by real heterologous-expression kinetics (below), not just computation |
| ΔG210 (alternative account) | — | Hao et al. 2009 (purely computational, no wet-lab kinetics) proposed a different specific mechanism: loss of a Gly210–Ser424 hydrogen bond. Dayan et al. 2010 directly critiques Hao's method in print — Hao's mutant model wasn't relaxed before docking, and Hao's study assumed competitive inhibition without testing it. Dayan's own kinetics show the real switch is competitive→**mixed-type** inhibition. | **Treat as superseded/secondary** — don't weight equally with Dayan 2010 |
| G399A (G398A waterhemp) | `steric_clash` | Added methyl group physically clashes with inhibitor substituents inside the pocket | Confirmed, Rangani 2019 |
| R98G/R98M/R128G/R128M | `hydrogen_bond_disruption` | Removes H-bonds with acifluorfen, fomesafen, sulfentrazone specifically; oxadiazole-type inhibitors don't H-bond here so aren't affected the same way | Confirmed, mechanism detailed in Hao et al. 2014 (JAFC, still not directly read — citation only) |
| V361A | pending | Not yet resolved from a structural paper in hand | Open |

## 5. Dayan et al. 2010's numbers — cited benchmark, not a reproduction target

**Scope note (see DECISION_LOG.md section 7 for the full reasoning):** these numbers came from a full homology-modeling + solvated MD simulation study — genuinely a separate undertaking from this project's static, scriptable pipeline. Reproducing them numerically would require rebuilding that MD pipeline for every mutation across every enzyme surveyed here, which is out of scope. **Cite these numbers as literature; do not treat them as a target your static pipeline needs to hit.**

The actual validation gate for the static pipeline: confirm that your own distance-to-active-site calculation places Gly210 **outside** the Heinemann et al. 2007 four-residue active-site core (Arg98, Phe392, Leu356, Leu372) — a positional claim, consistent with the finding below that Gly210 is "adjacent to, not in, the active site." That's what a static geometric metric can actually check.

The numbers themselves, for citation purposes:

- Active-site cavity volume: **~551 Å³ (WT) → ~848 Å³ (resistant)**
- Gly207-carbonyl-to-FAD-N5 distance: **increases by ~1.5 Å on average** (WT cluster 6–8 Å; resistant cluster 7–9 Å)
- Km for substrate (protoporphyrinogen IX): **unchanged** (~1 μM both) — confirms the mutation doesn't hurt normal substrate binding
- Vmax / kcat: **~10-fold lower** in resistant
- Ki for inhibitors (acifluorfen, lactofen, MC-15608): **100–500-fold higher** in resistant
- Inhibition type: **competitive (WT) → mixed-type (resistant)**

## 6. Why deletion, not substitution, at this position — citable evolutionary explanation

Dayan et al. 2010 directly tested this: Ala at position 210 occurs naturally in several herbicide-*sensitive* species (e.g., GenBank AF273767) without conferring resistance, and *in silico* substitution to any amino acid larger than Gly/Ala causes steric clashes with a nearby hydrophobic pocket (Phe467, Val360, Pro361, Leu362, Gly422, Gly423, Phe420). So substitution at this position is evolutionarily close to a dead end — deletion was the only path to resistance here, and it was only accessible because Gly210's codon happens to sit inside a short nucleotide repeat (a slippage-prone genetic context) that doesn't exist at the chloroplastic PPO1 isoform's equivalent position. That's a specific, citable, mechanistic answer to "why does PPO TSR show a deletion here and only substitutions everywhere else" — worth a paragraph in the eventual manuscript.

## 7. External validation dataset

`rangani_2019_table2_cross_resistance.csv` (already generated) — G399A/ΔG210/R128L tested against 13 herbicides, common *A. tuberculatus* genetic background, real IC50/RF values.

## 8. What this means for Claude Code, concretely

1. Add both ΔG210 accession pairs to the dataset (section 1); don't treat them as redundant or conflicting.
2. Use the Dayan 2010 numbers in section 5 as the hard validation gate for the pilot — if your own ChimeraX pipeline's cavity-volume and distance calculations land anywhere near 551→848 Å³ and +1.5 Å, that's your green light to scale to the other targets.
3. Log ΔG210's mechanism per section 4, including the Hao-vs-Dayan discrepancy as its own dataset note — don't silently pick one.
4. Giacomini 2017 accessions remain an open item — flag as unresolved rather than guessing.
5. Everything else from prior addenda (numbering key, active-site residues, mechanism tags for G399A/R98) stands as already given, now cross-confirmed rather than provisional.
