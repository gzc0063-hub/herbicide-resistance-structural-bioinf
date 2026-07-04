# Decision Log — PPO Cross-SOA Structural Bioinformatics Project

This file records every decision that shaped this project's direction, and why. It exists so that anyone (including future-you) can see *why* the project looks the way it does without re-deriving it. Pair with `PPO_Phase1_Final_Validated_Brief.md` (the current data/validation reference) — this file is the *why*, that file is the *what*.

---

## 1. Project selection

Starting point was a broader research-planning exercise across four candidate desk-based projects (weedscience.org-driven meta-analyses, an *Amaranthus* co-occurrence network study, this structural bioinformatics project, and an open-source decision-support tool). Three were selected to run as a connected portfolio:

1. **Project 1 — *Amaranthus* multi-resistance network analysis** (finds the *pattern*: which resistance mechanisms co-occur, in which populations, over time)
2. **Project 2 — cross-site-of-action comparative structural bioinformatics** (this project; finds the *structural reason* some mutations exist and predicts risk for newer sites of action)
3. **Project 3 — open-source decision-support tool** (*ships* the curated output of 1 and 2, plus prior PPO database work, as something usable)

**Decision:** sequence Project 3 last. Building the tool before there's curated data to populate it would ship an empty shell.

---

## 2. Expert panel review of Project 2 — methodological corrections

Before any code was written, a five-lens review (structural biologist, weed geneticist, bioinformatics pipeline reviewer, biostatistician, journal-editor lens) surfaced five fixes, all adopted:

| Problem identified | Fix adopted |
|---|---|
| "Distance to active site" isn't comparable in raw Å across enzymes of different sizes/architectures | Normalize as a percentile rank within each protein's own residue-distance distribution |
| AlphaFold/ColabFold barely reacts to a single point mutation — re-predicting a "mutant structure" from a mutant sequence mostly just returns the wild-type fold | Predict the wild-type structure once per target; evaluate each mutation's position *within* that fixed structure rather than re-folding the mutant |
| ConSurf is single-submission, web-only — doesn't scale across 6+ targets × many species | Compute conservation locally via alignment Shannon-entropy (Biopython) as the primary metric; treat ConSurf as an optional spot-check only |
| Naive logistic regression on "known resistance position vs. every other residue" has severe class imbalance and non-independence | Use a permutation/enrichment test instead (draw random residue sets of matching size, thousands of times, per enzyme) |
| "Mutations cluster near the active site" is expected, not surprising — weak central claim | Explicitly hunt for and foreground *outlier* mutations that don't fit that pattern (allosteric-acting resistance) as the more citable finding |

**Outcome that validated fix #5 directly:** ΔG210 turned out to be exactly this kind of outlier — Gly210 sits *adjacent to*, not inside, the PPO active site (confirmed independently by Hao et al. 2009 and Dayan et al. 2010). The panel's recommendation to look for non-obvious mechanisms was borne out by the first real case examined.

---

## 3. Execution platform — Claude Code

**Question:** can this pipeline actually be run with Claude Code as the execution engine?

**Verdict: yes, with one hard boundary.** Claude Code can write, run, and debug every *scripted* step — API queries (NCBI/UniProt/PDB), sequence alignment, ChimeraX/PyMOL scripting for distance and solvent-accessibility calculations, local conservation scoring, the permutation-test statistics, figure generation, dataset assembly, and repo/version-control management — provided the underlying software (ChimeraX, Python with Biopython/freesasa, R) is installed locally.

**The one thing it can't do on a normal laptop:** GPU-heavy neural-network structure prediction (ColabFold), for any target lacking a usable existing structure or template. Workaround: run the free-tier Google Colab ColabFold notebook by hand for those specific sequences, then hand the resulting PDB file back to Claude Code, which resumes the pipeline exactly as if the structure had come from a database. Confirmed this only matters for the newest targets (FAT, DHODH) — PPO, ALS, ACCase, and EPSPS all turned out to already have usable crystal structures or strong templates, so this limitation ended up mattering less than initially expected.

**What Claude Code does not replace:** domain judgment calls — is this the right reference template, is this mutation list complete and correctly sourced. Every domain sign-off in this log was a human decision point, not something the pipeline resolved on its own.

---

## 4. Pilot enzyme: PPO, not ALS — and why the recommendation changed

Initial recommendation was ALS/AHAS, on the reasoning that it had the strongest published structural precedent to validate a new pipeline against.

**Revised to PPO** once two things were confirmed during literature verification:
- A real PPO crystal structure exists and is directly usable (tobacco mitochondrial PPO2, PDB **1SEZ**, Koch et al. 2004, EMBO J 23:1720-1728) — not just a homology-modeling target.
- Franck Dayan (already identified as a potential collaborator) co-authored *two* directly relevant structural papers on PPO resistance (2010 mechanistic/kinetic study; 2018 broader review), giving an unusually strong, independently-published benchmark to validate a first pipeline run against.

Combined with PPO being the user's deepest existing domain expertise, this made PPO the stronger choice for a *validation* pilot — the goal of a pilot is to check the pipeline against ground truth, and PPO offered the most ground truth to check against.

---

## 5. Literature verification — corrections made to the working dataset

This was the largest single piece of work: verifying every mutation, accession, and mechanistic claim against primary sources rather than secondary citations. Corrections made, in the order discovered:

1. **Palmer amaranth V361A accessions were wrong.** Original candidates (QBB02367.1/QBB02368.1) were inferred from sequence-length matching and a clean single-position difference — reasonable logic, wrong answer. The actual paper (Nie, Harre & Young 2023, *Plants* 12(9):1886) deposited **MH910646.1** (susceptible) and **MH910647.1** (resistant) — confirmed directly from that paper's own Data Availability Statement.
2. **The resistant Palmer amaranth allele carries three substitutions, not one** (S68N, V361A, R480T). The source paper tested each individually by site-directed mutagenesis: V361A alone is causal; R480T alone is **experimentally proven non-causal**; S68N is background variation found in other non-resistant sequences too. Both non-causal variants were kept in the dataset as a validated negative-control set rather than discarded.
3. **Mutation nomenclature correction:** the Giacomini et al. 2017 mutation is **R98G and R98M** (Palmer-amaranth-native numbering: R128G/R128M) — not "R98L" or "R128L." R128L is real, but belongs to a *different species* (common ragweed, *Ambrosia artemisiifolia*).
4. **Citation mixup corrected:** G399A is **Rangani et al. 2019**, published in *Frontiers in Plant Science* 10:568 (DOI 10.3389/fpls.2019.00568) — not "Pest Management Science, DOI 10.1002/ps.4581." That DOI actually belongs to the Giacomini et al. 2017 paper (a different mutation, R98G/R98M). The two papers' identities had been conflated in an earlier pass.
5. **A third numbering layer surfaced:** G399 (Palmer amaranth numbering) = G398 in waterhemp-native numbering for the same physical residue — on top of the already-known tobacco-to-weed offset. Recorded as its own dataset field rather than folded into the "G399A" label.
6. **Active-site residue definition resolved into a hierarchy** after finding the original 2007 paper everyone else built on: Heinemann et al. 2007 (Biochem J 402:575-580) gives a validated 4-residue core (Arg98, Phe392, Leu356, Leu372) — adopted as primary. Rangani 2019's 9-residue table and Hao 2013's 8-residue list are broader, overlapping but not identical supplementary references (different methods, not an error).
7. **The two ΔG210 accession pairs found at the very start of the project (ABD52326/ABD52328 and ABD52329/ABD52330) are both legitimate**, not a conflict to resolve. Confirmed via Dayan et al. 2010's own Methods section, which used the second pair directly.
8. **A genuine disagreement found between two structural papers on ΔG210's mechanism** — this was the most important single finding of the verification process:
   - Hao et al. 2009 (purely computational, no wet-lab kinetics): proposed a lost Gly210–Ser424 hydrogen bond as the mechanism.
   - Dayan et al. 2010 (computational *and* real heterologous-expression kinetics): found a different mechanism — helix-capping destabilization via Ala206/Val205/Pro213 — and **directly critiqued Hao's method in print**, noting Hao's mutant model was never relaxed before docking, which biased the result toward "nothing changed."
   - **Decision: weight Dayan 2010 as the gold-standard benchmark**, not as one of two equally-weighted independent confirmations. Both accounts are recorded, but the pipeline's validation gate uses Dayan's numbers specifically.
9. **Exact validation-gate numbers extracted** from Dayan et al. 2010 for the pilot to reproduce: active-site cavity volume 551 Å³ (WT) → 848 Å³ (resistant); Gly207-to-FAD distance +1.5 Å average; Km unchanged (~1 μM); Vmax/kcat ~10-fold lower; Ki 100–500-fold higher; inhibition type switches competitive → mixed.
10. **A citable evolutionary explanation surfaced** for why this position uses a deletion rather than a substitution: Ala210 occurs naturally in sensitive species without conferring resistance, and any larger substitution causes steric clashes with a nearby hydrophobic pocket — deletion was the only accessible path, and only because the codon sits in a slippage-prone short repeat not present at the equivalent position in the other PPO isoform.

---

## 6. Outstanding open items

- **Giacomini et al. 2017 accession numbers for R98G/R98M are still unresolved.** No accession numbers appear in the visible text of that paper. Needs either supplementary data or direct author correspondence — not something to resolve by inference, given how the V361A accession inference went wrong earlier.
- **V361A's structural mechanism class is still unassigned** — not yet checked against a structural paper (Nie et al. 2023's own text should be checked for this specifically before tagging).

---

## 7. Validation-gate scope clarified (raised by Claude Code during Phase 1 execution)

Claude Code correctly flagged that literally reproducing Dayan et al. 2010's cavity-volume and FAD-distance numbers would require rebuilding their homology models and running full solvated MD simulation from scratch — a genuinely separate, multi-day-to-multi-week undertaking, and one that would need repeating for every mutation across every enzyme to stay methodologically consistent. That's the same scope-explosion risk the panel review fix in section 2 was already designed to prevent, just recurring in a new form.

**Decision: keep the static, scriptable pipeline (percentile-rank distance-to-active-site + solvent accessibility, no MD) as designed. Redefine the validation gate accordingly:**

- **Not checked:** exact cavity-volume or FAD-distance numbers (551→848 Å³, +1.5 Å) — these require MD and are cited as literature, not reproduced computationally.
- **Actually checked:** whether the pipeline's own static distance metric places Gly210 outside the Heinemann et al. 2007 four-residue active-site core (Arg98, Phe392, Leu356, Leu372) — a positional/geometric claim, consistent with Dayan's "adjacent to, not in, the active site" finding, and something the static pipeline can genuinely verify.
- **Optional, not required:** a lightweight local energy minimization (ChimeraX, not full MD) on the region immediately around a deletion, before computing distance/SASA — cheap enough to apply at comparative scale, and partially reflects the conformational relaxation Dayan's MD captured, without adopting MD as the project's method.

This also fixes a wording problem in `PPO_Phase1_Final_Validated_Brief.md` section 5, which currently reads as if the pipeline should reproduce Dayan's exact numbers. That section's numbers stay as the literature benchmark to *cite*; they are not a target the static pipeline is expected to hit.

**Manuscript framing to carry forward:** the project's contribution is breadth — a systematic comparison across many enzymes and mutations using methods tractable at that scale — not per-target mechanistic depth. Where a deep MD study already exists for a given mutation (as it does for ΔG210), the lightweight pipeline's output is compared against that study's *qualitative* conclusions as an internal consistency check, not treated as a numerical replication exercise. State this explicitly in the methods section to preempt the reviewer question "why not MD everywhere."

---

## 8. How the files in this repo relate

- **This file (`DECISION_LOG.md`)** — the *why*: every directional decision and correction, in the order they were made.
- **`PPO_Phase1_Final_Validated_Brief.md`** — the *what*: the current, fully-cross-checked dataset, numbering keys, mechanism classes, and validation-gate numbers, ready to feed into the pipeline.
- **`rangani_2019_table2_cross_resistance.csv`** — external validation dataset (real IC50/resistance-factor data, 13 herbicides × 3 mutations, common genetic background).
