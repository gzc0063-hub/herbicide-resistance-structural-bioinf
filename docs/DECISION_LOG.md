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
9. **Exact Dayan et al. 2010 benchmark numbers extracted and later corrected in wording:** active-site cavity volume 551 Å³ (WT) → 848 Å³ (resistant); Gly207-to-FAD distance +1.5 Å average; Km unchanged (~1 μM); Vmax/kcat ~10-fold lower; I50 100–500-fold higher; Ki ~10–55-fold higher depending on inhibitor; inhibition type switches competitive → mixed. The 100–500× value is an I50 claim, not a Ki claim.
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

## 8. Phase 1 validation gate: PASS — and a decision to finish Phase 1 before scaling

Static distance-to-active-site results (full data in `ppo_validation_gate_results.md`):

| Mutation | Distance to core | Percentile | SASA |
|---|---|---|---|
| ΔG210 | 8.37 Å | 8.2 (top ~8%) | buried |
| G399A | 4.20 Å | 2.8 | buried |
| V361A | 11.73 Å | 20.2 | buried |
| R98G/R98M | 0 Å (is a core residue) | 0.9 | solvent-exposed |

**Gate passed:** Gly210 lands close (top decile) but clearly outside the four-residue core — geometrically confirming Dayan's "adjacent to, not in, the active site" finding, with no MD required, exactly as scoped in section 7.

**Two items flagged before moving to Phase 2, rather than starting Phase 2 immediately:**

1. **Complete Phase 1's third metric (conservation score) before scaling**, not after. The original design specifies three metrics per mutation (distance, SASA, conservation); only two exist as of this gate. Building the conservation step now, on one target, is far cheaper than retrofitting it onto five targets later.
2. **V361A is a candidate outlier** (percentile 20.2, notably farther from the core than the other two causal TSR mutations) — earmarked for the panel review's "look for allosteric/non-obvious mechanisms" recommendation (section 2). Conservation data will help distinguish "genuine structural surprise" from "unremarkable, poorly-conserved position" — get this before moving past PPO, while the finding is still the active focus.
3. **Sanity-check the R98 SASA classification** before treating "buried vs. exposed" as a reliable feature for later cross-enzyme comparison. R98 coordinates the substrate's entry point per Heinemann 2007, so pocket-mouth solvent exposure is plausible — but confirm this isn't an artifact of chain selection or oligomeric state before it propagates into four more targets' worth of data.

**Decision: Phase 2 (ALS/AHAS, ACCase, EPSPS, HPPD) starts after the conservation step is built and the R98 SASA check is confirmed — not before.**

---

## 9. Phase 1 closed out: conservation metric built, flagship finding identified

All three items flagged in section 8 are resolved:

- **Conservation metric built** — Shannon entropy from a 10-species plant PPO2 MAFFT alignment (tobacco, both *Amaranthus* spp., Arabidopsis, soybean, tomato, sugar beet, poplar, rice, maize), mapped to tobacco numbering. Phase 1 is now complete against the original three-metric design (distance, SASA, conservation).
- **R98 SASA confirmed genuine, not an artifact** — correct dimer context, standard 1.4 Å probe, ligand (OMN) present and in direct contact (2.62 Å). R98 coordinates the substrate's peripheral propionate group at the pocket mouth, so partial solvent exposure is the expected result for that specific role, not a bug. Carrying "buried vs. exposed" forward as a feature for Phase 2, with the explicit caveat that pocket-rim residues coordinating peripheral substrate groups can legitimately read as exposed — don't assume "core residue ⇒ buried" as a blanket rule when interpreting other enzymes.
- **V361A re-evaluated and downgraded; ΔG210 promoted to flagship finding.** With conservation data in hand, V361A is the *least* conserved of the four positions (0.573) as well as the farthest from the core (percentile 20.2) — the profile of a naturally variable, structurally permissive site, not a hidden allosteric hotspot. **Decision: don't build the manuscript's central claim around V361A.** Its mechanism_class stays `pending`, and it remains a valid, correctly-cited resistance mutation in the dataset. **ΔG210 is the stronger candidate**: meaningfully conserved (0.769) *and* structurally adjacent-to-but-outside the core — a pattern independently corroborated by this project's own entropy calculation and by Dayan et al. 2010's own reported cross-species Gly/Ala survey at this position.

**Open quality check before leaning on "two independent lines of evidence" in the manuscript:** confirm whether the 10-species conservation panel includes the specific herbicide-sensitive species Dayan et al. 2010 cited as naturally carrying Ala at this position (GenBank AF273767 — species not confirmed in this log). If that species is already inside the 10-species panel, the two lines of evidence partially overlap rather than being fully independent, and the manuscript should say so rather than claim full independence. Cheap to check; do it before writing the convergent-evidence claim into a draft.

---

## 10. Phase 2 sequencing decision

**Decision: do not batch-launch ALS/AHAS, ACCase, EPSPS, and HPPD together. Pilot one enzyme fully first, the same way PPO was piloted in Phase 1, then batch the remaining three once that pilot clears its own validation gate.**

Reasoning: Phase 1's value wasn't just the pipeline — it was catching enzyme-specific wrinkles (wrong accessions, an ambiguous SASA reading, a numbering-layer nobody had accounted for) *before* they propagated across multiple targets. Batch-launching four enzymes at once would spend that same discipline four times as expensively, after the fact, instead of once, up front.

**ALS/AHAS selected as the Phase 2 pilot enzyme**, over ACCase, EPSPS, and HPPD, because it has the deepest combination of real crystal structures and well-characterized, structurally-mapped TSR mutations across many species (e.g., Pro197, Trp574, Ser653, Ala122, Asp376 substitutions, each independently documented) — the same kind of resource depth that made PPO the right Phase 1 choice over the originally-planned ALS pilot. EPSPS is the next-strongest candidate on the same grounds (extensive crystal structures, well-characterized Pro106 substitutions) if ALS turns up a blocking problem. HPPD is likely the weakest candidate to pilot with, since fewer TSR mutations are well-documented for it relative to NTSR/metabolic resistance, which sits outside this pipeline's scope.

---

## 11. AF273767 resolved — ΔG210 evidence framing corrected

Checked directly (NCBI esummary) whether Dayan et al. 2010's cited example of a
naturally Ala-carrying herbicide-sensitive species (GenBank AF273767) falls inside
our own 10-species conservation panel. **It does** — AF273767 is *Zea mays*, and our
panel already includes maize (PWZ38740.1), which shows Ala at the equivalent
alignment column. This is the same data point Dayan reported, not a second,
independent confirmation of it.

**Decision: retract the "two independent lines of evidence converge" framing for
ΔG210.** Corrected framing, applied in `ppo_validation_gate_results.md`: "consistent
with, and partially extending, Dayan et al. 2010's cross-species survey." The
"partially extending" part is genuine, not just a hedge — three other panel species
Dayan's text didn't specifically name (Arabidopsis, soybean, poplar; also tomato)
independently carry Ala at this position too, so the panel does add real data beyond
his one cited example. But since one of our ten data points is the exact species he
already reported, this cannot be described as fully independent corroboration.

---

## 12. ALS/AHAS pilot — sign-off decisions

Three open items from the pilot's initial candidate research (`als_mutation_candidates.md`),
resolved as follows rather than by Claude Code's own inference:

1. **Reference/wild-type accession: not resolved by elimination.** The eight
   Larran et al. 2017 accessions (ASL69930–ASL69937) all share the same 8
   N-terminal differences relative to ASL69930, which looked at first glance like
   ASL69930 might be the odd one out. **Decision: don't treat that as grounds to
   pick a different diff baseline.** The N-terminus mismatch is more likely a
   different transcript start than a real biotype difference, but the correct fix
   is to find which accession Larran et al. 2017's own methods/supplementary text
   explicitly labels as the susceptible/wild-type population sample — not to guess
   from the sequence data alone, given how the QBB0236x accession inference went
   wrong in Phase 1. **Status: blocked** — Wiley blocked automated fetch attempts
   against this DOI (10.1002/ps.4662); waiting on the user to supply the PDF
   directly per the new standing convention (§13).
2. **Scope narrowed: Ala122 and Pro197 dropped from this pilot.** Trp574Leu and
   Ser653Asn (both present in the Larran et al. 2017 accession set) are sufficient
   to clear a pilot validation gate reusing PPO's proven pipeline. Adding the other
   three classically-documented ALS positions now would be scope creep on a
   quick second check, not the point of piloting one enzyme before batching the rest
   (§10). Ala122/Pro197 remain fair game for a fuller ALS pass later if warranted.
3. **QYC94980/QYC94981 excluded from the working mutation set.** These accessions
   ("Comparative analysis of five resistant acetolactate synthase isoforms from
   *Amaranthus palmeri*," Palmieri, Permingeat & Perotti) are marked "Unpublished"
   in the GenBank record itself — a direct database submission, not a peer-reviewed
   paper, the same category of problem as the original QBB0236x mistake. Tagged
   `unpublished_lower_confidence` and kept as a record in `als_mutation_candidates.md`
   only; excluded from anything the manuscript relies on.

**Decision: proceed with Trp574Leu and Ser653Asn only, once the reference accession
is confirmed from Larran et al. 2017's own text** — not before.

---

## 13. Standing convention — paywalled or bot-blocked sources

Raised after a Wiley fetch attempt against the Larran et al. 2017 DOI was blocked
(403, same pattern seen before with other publishers). **Convention going forward,
recorded in `CONTRIBUTING.md`:** if full-text verification requires a paper that's
paywalled or blocks automated access, stop after one attempt rather than spending
tokens on repeated workarounds (alternate URLs, scraping, proxies). Ask the user for
the paper by full citation instead — they can search for it, download it through
their own institutional access, and upload it directly to the session. This is the
same path already used successfully for Dayan et al. 2010, Hao et al. 2009, and
Giacomini et al. 2017 (§14).

---

## 14. ALS/AHAS reference accession and numbering resolved from Larran et al. 2017's own text

The user supplied the PDF directly (per §13's convention) after Wiley blocked the
automated fetch. Resolved, from the paper's own Table 4, not by inference:

- **Wild-type/susceptible reference: KY781916** — explicitly labeled the S
  population in Table 4, 8/8 clones with 100% amino acid identity to each other.
- **Trp574Leu: KY781918** (R1 population, allelic version C, 1/8 clones) — a clean,
  isolated substitution.
- **Ser653Asn: KY781923** (R2 population, allelic version H, 2/8 clones) — also
  clean and isolated.
- **A282D uses a third numbering reference** (*Amaranthus retroflexus*, not
  Arabidopsis) per the paper's own footnote, because it falls in an indel — this
  position is out of the pilot's scope (§12) but worth remembering if a fuller ALS
  pass is done later, as a fourth numbering layer alongside PPO's three.

**Cross-check:** these three accessions are byte-identical to protein accessions
already fetched during the initial candidate research - ASL69930.1 ≡ KY781916.1,
ASL69932.1 ≡ KY781918.1, and both ASL69931.1 and ASL69937.1 ≡ KY781923.1 (matching
Table 4's stated 2/8 frequency for that allelic version - two separate deposited
clones of the same sequence). The original elimination-based guess at a wild-type
reference (ASL69930) turned out to be correct, but per §12's decision it was
correctly left unconfirmed until the paper's text settled it - the sequence being
right doesn't retroactively justify skipping the verification step.

**Numbering resolved with no offset needed**, unlike PPO's tobacco/waterhemp/palmeri
system: the 1Z8N crystal structure's own PDB residue numbering already matches the
paper's stated Arabidopsis-convention positions exactly (verified directly - chain A
residue 574 is TRP, residue 653 is SER). The crystallographers used the standard
literature convention directly, so `als_mutations.csv` needed no numbering_maps.json
equivalent.

**Active-site reference resolved without McCourt et al. 2006's full text.** That
paper (*PNAS* 103:569-573) would be the natural Heinemann-2007-equivalent source,
but a literature-search fetch attempt for its full text came back empty. Rather than
pushing further on that specific source, the active site is defined directly from
which residues contact the bound imazaquin ligand in 1Z8N itself - the same
structural-contact approach already used to confirm PPO's R98-OMN relationship, and
arguably closer to the panel review's original intent (compute structural features
directly rather than depending on secondary literature more than necessary).

**Decision: proceed to the ChimeraX distance/SASA/conservation pipeline for
Trp574Leu and Ser653Asn**, per §12.

---

## 16. ALS/AHAS pilot validation gate: PASS — a different kind of result than PPO's

Full results in `als_validation_gate_results.md`. Active-site core defined directly
from the 1Z8N structure (residues within 4.5 Å of either bound imazaquin copy),
sidestepping the need for McCourt et al. 2006's full text. SASA computed on the
author-determined biological tetramer (assembly 1), same fix applied to PPO's
dimer.

| Mutation | In active-site core? | Percentile (vs. rest of core) | Conservation (9 species) |
|---|---|---|---|
| Trp574Leu | Yes - direct imazaquin contact, 3.4 Å | 22.0 | 1.000 (invariant) |
| Ser653Asn | Yes - direct imazaquin contact, 3.65 Å | 1.7 | 1.000 (invariant) |

**Not an outlier finding like ΔG210** - both mutations are themselves genuine
ligand-contact residues, completely conserved across the 9-species panel. This is
the textbook profile for direct steric interference with herbicide binding,
matching decades of established ALS literature (Tranel & Wright 2002) for these
specific substitutions. **The gate still passes**: the pipeline correctly
identifies known active-site residues as active-site residues when applied to a
well-characterized case, a complementary check to PPO's gate (which confirmed the
pipeline could correctly place a genuinely non-obvious, surprising position).
Together the two pilots validate both ends of the spectrum.

**No new outlier/allosteric candidate surfaced from ALS.** Useful negative result
for the eventual cross-enzyme synthesis (Phase 4): PPO's ΔG210 and ALS's
Trp574/Ser653 sit at opposite ends of the distance-to-core spectrum while both
being highly conserved - a good internal check that the normalized distance metric
behaves sensibly across enzymes with different active-site architectures, matching
the panel review's original cross-enzyme-comparability concern (§2).

**Decision: ALS/AHAS pilot clears its validation gate. Proceed to batch ACCase,
EPSPS, and HPPD together, reusing the now twice-proven pipeline**, per §10's
original sequencing plan.

---

## 17. How the files in this repo relate

- **This file (`DECISION_LOG.md`)** — the *why*: every directional decision and correction, in the order they were made.
- **`CONTRIBUTING.md`** — working conventions for this repo (currently: how to handle paywalled/bot-blocked sources, §13).
- **`PPO_Phase1_Final_Validated_Brief.md`** — the *what*: the current, fully-cross-checked PPO dataset, numbering keys, mechanism classes, and validation-gate numbers.
- **`als_mutation_candidates.md`** / **`als_mutations.csv`** / **`als_validation_gate_results.md`** — the equivalent trio for the ALS/AHAS pilot: resolution trail, working dataset, and validation-gate results.
- **`rangani_2019_table2_cross_resistance.csv`** — external validation dataset (real IC50/resistance-factor data, 13 herbicides × 3 mutations, common genetic background).
- **`docs/references/`** — primary-source PDFs now available directly in the repo (Dayan et al. 2010, Hao et al. 2009, Giacomini et al. 2017, Larran et al. 2017), not just summarized secondhand in the briefs. Verification claims in `VERIFICATION_LOG.md` that cite these papers can be checked against the actual text.

---

## 18. Metric-schema cleanup before post-pilot scaling

Reviewing the project as both a bioinformatician and weed scientist surfaced one
methodological cleanup item that should happen before using ALS as the template for
ACCase/EPSPS/HPPD: ALS's pilot script reported "distance to nearest other active-site
core residue" for residues that were themselves in the active-site core. That value
is useful as a within-core spacing metric, but it is not the same as PPO's
distance-to-active-site-core metric, where core residues score 0 Å.

**Decision: standardize the structural schema before adding new enzymes.** Going
forward, per-residue distance/SASA tables should separate:

- `in_active_site_core`
- `distance_to_active_site_core_A` (0 Å for core residues)
- `distance_to_nearest_other_core_residue_A` (within-core spacing/context)
- `percentile_rank_distance_to_core`
- `sasa_A2`

This preserves the ALS pilot's useful "nearest other core residue" information while
making the primary cross-enzyme distance metric comparable to PPO. The ALS
validation gate still passes - Trp574 and Ser653 are direct imazaquin-contact core
residues and invariant in the conservation panel - but their primary distance-to-core
percentile is now interpreted as a core-residue percentile, not the old within-core
spacing percentile.

**Decision on next enzyme:** do not immediately batch ACCase, EPSPS, and HPPD until
this cleanup is in place. Start the post-pilot expansion with **EPSPS first** because
it has especially strong structural and agronomic precedent around glyphosate
target-site resistance. If EPSPS clears with the standardized schema, then proceed to
ACCase and HPPD using the same template.

---

## 19. EPSPS post-pilot setup decision

EPSPS was started as the first post-pilot enzyme per §18. Two structure choices were
checked directly against RCSB metadata:

- **Classic glyphosate-bound structures** such as 1G6S/2AAY are strong ligand-bound
  templates but are *E. coli* EPSPS.
- **8UMJ** is wild-type *Zea mays* EPSPS complexed with glyphosate and
  shikimate-3-phosphate, giving both a plant source organism and direct ligand
  contacts.

**Decision: use 8UMJ as the EPSPS structure/template.** This better matches the
project's preference for plant/Viridiplantae structures while preserving the ALS
active-site-definition strategy: define the core directly from ligand contacts.

For the mutation/accession anchor, Baerson et al. 2002 (*Plant Physiology*
129:1265-1275, PMID 12114580) was selected over Chong et al. 2008 as the pilot
source:

- PubMed metadata for Baerson explicitly lists **AJ417033** and **AJ417034**.
- GenBank labels AJ417033 as *E. indica* `epsps-R` and AJ417034 as `epsps-S`, both
  tied to Baerson et al. 2002.
- The paper reports mature-protein **Pro106Ser** and functional evidence that this
  substitution is the main driver of reduced glyphosate sensitivity.
- A local alignment maps the GenBank translated position 107 (resistant Ser,
  susceptible Pro) to 8UMJ maize sequence position 107 / PDB residue **106**.
  8UMJ includes an initiating MET numbered 0, so FASTA sequence position 107
  corresponds to PDB residue 106, not 108.

**Decision: EPSPS pilot mutation = Pro106Ser, using AJ417034.1 (susceptible) and
AJ417033.1 (resistant), mapped to 8UMJ residue 106.** Record the second Baerson
sequence difference (GenBank translated position 382; resistant Leu, susceptible
Pro) as background only, because Baerson reports it does not significantly explain
reduced glyphosate sensitivity.

Chong et al. 2008 was saved and retained as context because it reports Pro106Ser
and Pro106Thr variation across Malaysian *E. indica* populations. However, its
Bidor resistant comparison accession **AY157643** is marked "Unpublished" in
GenBank and the paper does not provide new deposited accessions for each sample in
its Table 1. **Decision: do not use Chong/AY157643 as the manuscript-reliant EPSPS
anchor; tag as context/lower-confidence only if referenced.**

---

## 20. EPSPS distance/SASA gate partial completion

ChimeraX was not available on PATH in the current Codex desktop session, so EPSPS
was run with a local static fallback rather than postponing the entire target. The
fallback uses:

- `scripts/pdb_static_metrics.py` for PDB ATOM/HETATM parsing, ligand-contact core
  selection, and Shrake-Rupley-style SASA.
- `scripts/active_site_metrics.py` for the same standardized distance schema now
  used by PPO and ALS.

The 8UMJ PDB header says each chain is a monomeric biological unit, so SASA was
computed on chain A alone. Bound glyphosate (`GPJ`) and shikimate-3-phosphate
(`S3P`) were included as occluding atoms for protein-residue SASA.

Active-site core was defined as all chain-A protein residues with any atom within
4.5 A of either `GPJ` or `S3P`: 24, 25, 29, 51, 99, 100, 101, 102, 105, 131,
177, 178, 179, 180, 205, 206, 209, 330, 331, 354, 358, 359, 362, 403, 404, 429.

Corrected EPSPS Pro106Ser result:

- 8UMJ residue: **106 PRO**.
- In ligand-contact core? **No**.
- Distance to active-site core: **3.85 A**.
- Percentile rank: **12.9**.
- SASA: **14.3 A^2**.

**Intermediate decision: treat EPSPS distance/SASA as complete but hold the
validation-gate decision until conservation is added.** The result is
qualitatively plausible for Pro106Ser
(adjacent-to-core, not a selected direct ligand-contact residue), but this target
must not be used as a completed third-family template until conservation is added.

An NCBI E-utilities attempt to fetch a broader EPSPS conservation panel succeeded
for the first few records but then returned HTTP 429. **Decision: do not burn more
effort on repeated NCBI retries in this session.** The fastest next step is to use
a manually/accession-seeded EPSPS protein FASTA panel, then fill the conservation
row for 8UMJ residue 106 before starting ACCase.

---

## 21. EPSPS validation-gate completion

The EPSPS conservation panel was built after checking the user-supplied IDs rather
than accepting them blindly. Several supplied IDs were excluded because they were
not usable EPSPS records:

- `A0A0R0H6D7` returned 404 from UniProt.
- `Q0DFI0`, `K4C1C4`, and `B9H6K7` returned empty FASTA bodies from UniProt's
  accession endpoint.
- `A0A2G2Y4X3` resolved to *Capsicum annuum* SAUR68-like, not *Beta vulgaris*
  EPSPS.
- `P24397` resolved to *Hyoscyamus niger* hyoscyamine 6-beta-hydroxylase, not
  *Zea mays* EPSPS.
- `AF349754` resolved to *Lolium rigidum* EPSPS, not *Eleusine indica*. The
  project therefore kept the already-verified Baerson *Eleusine* susceptible
  accession `AJ417034.1`.

Corrected panel used for the EPSPS conservation metric:

- 8UMJ / *Zea mays* reference sequence (`A0A1D6NVZ6` in PDB metadata)
- *Eleusine indica* susceptible Baerson sequence (`AJ417034.1`, translated locally)
- *Arabidopsis thaliana* `P05466`
- *Nicotiana tabacum* `P23981`
- *Glycine max* `I1JKP7`
- *Oryza sativa* `A0A0N7KLH2` (fragment; absent at the Pro106 column)
- *Solanum lycopersicum* `P10748`
- *Populus trichocarpa* `B9GPE8`

Because MAFFT was not available in the current session, EPSPS conservation was
computed with a tested reference-indexed pairwise alignment helper
(`scripts/reference_conservation.py`). Rows are indexed by 8UMJ/PDB residue number,
not raw FASTA position. The same numbering correction from §19 applies: FASTA
position 107 maps to PDB residue 106 because 8UMJ includes an initiating MET
numbered 0.

Conservation result at the EPSPS pilot site:

- 8UMJ/PDB residue 106 = Pro.
- Shannon entropy = 0.000.
- Normalized conservation = 1.000.
- Present in 7/8 panel sequences; the Oryza fragment is absent at this column.

**Decision: EPSPS validation gate PASSED.** Pro106Ser is adjacent to, but not
inside, the ligand-contact active-site core (3.85 A; distance percentile 12.9),
has modest static SASA (14.3 A^2), and is fully conserved among sequences present
at the column. This gives the project a third validated target family with a
mechanistic profile distinct from both PPO and ALS.

---

## 22. ACCase anchor decision: use AJ310767 black-grass numbering plus Yu 2007's deposited 2088 region

The ACCase phase will use Delye et al. 2005 (*Plant Physiology* 137:794-806)
as the primary numbering/structure anchor and Yu et al. 2007 (*Plant Physiology*
145:547-558) as the source for the additional Cys2088Arg mutation in *Lolium*.

This is **not** the same accession pattern as EPSPS. EPSPS had paired resistant
and susceptible *Eleusine indica* GenBank records. ACCase instead has a
well-established reference coding sequence and mutation calls:

- Delye et al. 2005 states that all nucleotide and amino-acid positions use the
  black-grass chloroplastic ACCase reference **EMBL/GenBank AJ310767**, and that
  the sequenced CT-domain region corresponds to nucleotide positions 4368-7329
  in that coding sequence.
- The same paper identifies Trp2027Cys, Asp2078Gly, and Gly2096Ala from
  resistant black-grass seedlings, and discusses Ile1781Leu and Ile2041Asn as
  previously established ACCase resistance substitutions in the same AJ310767
  numbering system.
- Delye et al. 2005 explicitly uses yeast ACCase CT structures **1UYT** and
  **1UYS** as templates and reports that the aligned black-grass CT-domain span is
  Leu1639-Leu2204 of AJ310767.
- Yu et al. 2007 independently verifies ACCase mutations in resistant *Lolium*
  populations, including Ile1781Leu, Trp2027Cys, Ile2041Asn, Asp2078Gly, and the
  newly identified Cys2088Arg. It states that the 2088-region sequence data were
  deposited as **EF538937-EF538943** and that amino-acid positions correspond to
  the full-length plastidic ACCase in *Alopecurus myosuroides*.

**Decision:** ACCase can proceed using AJ310767 as the verified reference and
numbering accession, with EF538937-EF538943 recorded specifically for the
Yu 2007 Cys2088Arg sequence evidence. Do not describe the ACCase rows as paired
resistant/susceptible full-length accessions. In the manuscript and validation
tables, describe them as reference-numbered ACCase target-site substitutions
verified from Delye 2005 and Yu 2007 primary-source text/tables.

---

## 23. ACCase validation-gate completion

ACCase was run on the 1UYS yeast ACCase CT-domain B+C biological dimer, with
haloxyfop (`H1L`) defining the ligand-contact active-site core. AJ310767
black-grass CT-domain positions were aligned to 1UYS, preserving the Delye et al.
2005 dimer-side convention for the key resistance sites.

Mutation-position results:

- Ile1781Leu -> chain C residue 1705; direct ligand-contact-core residue.
- Trp2027Cys -> chain B residue 1953; 5.60 A from core; distance percentile 10.4.
- Ile2041Asn -> chain B residue 1967; direct ligand-contact-core residue.
- Asp2078Gly -> chain B residue 2004; 5.19 A from core; distance percentile 8.7.
- Cys2088Arg -> chain B residue 2014; 11.83 A from core; distance percentile 25.9.
- Gly2096Ala -> chain B residue 2022; 7.28 A from core; distance percentile 12.8.

Conservation was computed from a 14-sequence plastidic grass ACCase panel seeded
from the accessions named in Delye et al. 2005 and Yu et al. 2007. The sites are
all highly conserved (0.850-1.000 normalized conservation), with Trp2027,
Asp2078, and Gly2096 invariant among sequences present at those columns.

**Decision: ACCase validation gate PASSED.** ACCase adds a fourth target family
and a useful internal contrast: some TSR substitutions are direct ligand-contact
core residues, some are adjacent-to-core pocket residues, and Cys2088Arg is the
clearest ACCase candidate for a more distal cavity-context effect in the static
pipeline. At the time, the next planned target was HPPD using the same
verified-source-first workflow; that plan was later narrowed by the HPPD go/no-go
audit in §25.

---

## 24. External review reconciliation: ALS interface core fixed; HPPD becomes a go/no-go TSR audit

An external review artifact and a parallel Claude-side review were reconciled after
EPSPS and ACCase had already been completed in this workspace. The review's most
important valid criticism was that ALS/AHAS inhibitor binding occurs at a
dimer-interface pocket, so the original single-chain 1IQ contact core was
biologically incomplete.

Direct 1Z8N checking confirmed the issue. The ALS active-site core is therefore
expanded from the original 16 same-chain 1IQ-contact residues:

220, 245, 246, 275, 276, 279, 280, 281, 351, 376, 377, 396, 397, 574, 653, 654

to a 27-residue interface-aware core by adding the neighboring-subunit pocket
positions, expressed in the same Arabidopsis/PDB numbering convention:

121, 122, 168, 195, 196, 197, 199, 200, 206, 207, 256

This correction does **not** change the ALS pilot interpretation: Trp574Leu and
Ser653Asn remain direct active-site/contact residues, fully conserved, and score
0 A distance-to-core under the standardized metric schema. It does explain why
Ala122 and Pro197, which were intentionally excluded from the narrow ALS pilot, are
real binding-pocket resistance hotspots and should be treated as such in any fuller
ALS expansion.

The review also correctly flagged that the project at that point reported raw SASA
in A^2, not residue-normalized RSA. Existing buried/exposed interpretations
remained safe because the calls were clear-cut, but **Phase 4 cross-enzyme pooling
needed RSA while preserving raw SASA for traceability.** This was later implemented
in Decision 27.

HPPD is now reframed before any metric work. Do **not** use Gly336 as a weed
target-site resistance mutation: it is an engineered *Pseudomonas fluorescens*
HPPD crop-tolerance variant used in FG72 soybean, not an evolved weed-resistance
allele. HPPD should first undergo a primary-literature go/no-go audit for verified
weed-evolved target-site mutations with accessions. If no valid TSR rows are found,
HPPD should be written as an informative contrast case dominated by non-target-site
resistance/metabolism/gene amplification, not forced into the TSR validation-gate
template.

**Decision:** keep ACCase and EPSPS as completed validation-gate phases; merge the
ALS interface-core correction immediately; require RSA before Phase 4; and make
HPPD's next step a source-first TSR eligibility audit rather than structure-metric
generation. The RSA and HPPD follow-through are recorded in Decisions 27 and 25,
respectively.

---

## 25. HPPD source audit and structural contrast completion

The HPPD go/no-go audit was run before creating any mutation table. The audit found
no verified weed-evolved HPPD target-site amino-acid substitution suitable for the
comparative TSR dataset. Instead, the relevant weed-resistance papers point to
non-target-site mechanisms, especially enhanced metabolism/P450 or GST-linked
detoxification, expression changes, and polygenic stress-response differences.

Specific source-audit outcome:

- *Amaranthus tuberculatus* mesotrione resistance (PMID 28662111): no HPPD
  target-site mutation associated with resistance, no HPPD duplication or
  overexpression in that population; higher mesotrione metabolism observed.
- *Amaranthus palmeri* mesotrione resistance (PMID 28443128): no specific
  resistance-conferring HPPD mutation or HPPD gene amplification detected; increased
  HPPD expression and rapid detoxification reported.
- *Amaranthus tuberculatus* HPPD resistance reversal with P450 inhibitors
  (PMID 28799707): resistance described as non-target-site and metabolism-based.
- Multiple-resistant waterhemp topramezone work (PMID 30519248): rapid oxidative
  metabolism described as the resistance mechanism.
- Wild radish HPPD cross-resistance (PMID 37170102): enhanced metabolism via
  multiple candidate detoxification genes.
- *Leptochloa chinensis* HPPD resistance (PMID 37889480): no target-site amino-acid
  mutation; P450/GST-mediated detoxification implicated.

**Decision: do not create `hppd_mutations.csv` in this pass.** HPPD is not a
TSR-positive validation-gate family in the current resource. Gly336 remains excluded:
it is an engineered *Pseudomonas fluorescens* crop-tolerance variant used in FG72
soybean, not a weed-evolved resistance allele.

HPPD was nevertheless retained as a structural module using plant templates:

- **5YWG**: *Arabidopsis thaliana* HPPD complexed with mesotrione (`92L`) and
  cobalt (`CO`) in the deposited active site; used as the primary mesotrione-pocket
  contact map.
- **1TG5**: *Arabidopsis thaliana* HPPD complexed with Fe(II) (`FE2`) and DAS645
  (`645`); used as the Fe(II) plant-HPPD support structure.

The 5YWG active-site core is defined as every protein residue within 4.5 A of
mesotrione (`92L`) or the deposited metal (`CO`) across the A+B dimer. This gives
34 chain-residue core positions, 17 per chain:

226, 228, 267, 280, 282, 307, 308, 368, 379, 381, 392, 394, 419, 420, 421, 423,
424

The expected metal-site sanity checks pass: His226, His308, and Glu394 contact the
metal; Phe424 contacts mesotrione. The 1TG5 Fe(II)+DAS645 contact core gives the
same pocket logic under its shorter numbering convention, with His205, His287, and
Glu373 as the Fe-site anchor.

**Decision: HPPD phase is COMPLETE as a structural negative/contrast case.** It
should be included in the manuscript as evidence that the resource does not force
all herbicide targets into a TSR-positive template. For Phase 4 pooling, include
HPPD active-site descriptors and a categorical "no verified weed TSR accepted"
status, but do not pool fabricated mutation rows.

---

## 26. Post-rebase reconciliation and duplicate-source cleanup

After pushing the broad EPSPS/ACCase/HPPD completion commit, the local Codex work
was rebased on top of Claude Code's intervening ACCase commits, including the
correction that black-grass/AJ310767 Cys2088 maps to 1UYS chain B residue **2014**,
not 2013. The rebase preserved Claude's history and then applied the broader
six-mutation ACCase, EPSPS, ALS-interface, and HPPD contrast-case work on top.

A follow-up audit checked for:

- unresolved merge-conflict markers;
- stale ACCase `2088 -> 2013` wording;
- duplicate ACCase source PDFs/FASTA files;
- stale instructions saying HPPD was still next/not started;
- missing ALS interface-core correction;
- missing EPSPS/ACCase/HPPD output tests.

Two duplicate source artifacts were found and removed:

- `docs/references/Yu_et_al_2007_ACCase_Lolium_Cys2088Arg.pdf`, which was
  byte-identical to `docs/references/Yu_et_al_2007_ACCase_Lolium.pdf`;
- `data/raw/ACCase_Amyosuroides_AJ310767.fasta`, which contained the same
  2320-aa AJ310767 sequence as `data/raw/ACCase_Alopecurus_AJ310767_reference.fasta`
  but had a less accurate filename for the black-grass reference.

The ACCase scripts now use the retained canonical file:
`data/raw/ACCase_Alopecurus_AJ310767_reference.fasta`.

**Decision:** treat GitHub `master` after commit `f2ac466` as the reconciled source
of truth across Codex and Claude Code. Do not reintroduce the duplicate Yu 2007 PDF
or duplicate AJ310767 FASTA unless a future source-audit reason requires separate
copies. The retained ACCase mapping remains: Cys2088Arg -> 1UYS chain B residue
2014.

---

## 27. RSA normalization before Phase 4 pooling

The external review correctly identified that raw per-residue SASA in A^2 is not
the right pooled cross-enzyme exposure covariate because amino-acid side-chain size
differs strongly among residue types. The existing raw `sasa_A2` values remain
useful for traceability and for comparing back to the ChimeraX/static-SASA pipeline,
but pooled buried/exposed analysis should use residue-normalized RSA.

Implemented a dedicated post-processing step, `scripts/rsa.py`, that appends two
columns to every current static metric output:

- `max_sasa_tien2013_A2`, using the Tien et al. 2013 maximum allowed solvent
  accessibility table;
- `rsa_tien2013`, calculated as `sasa_A2 / max_sasa_tien2013_A2`.

The script preserves raw `sasa_A2` and inserts the RSA columns directly beside it.
Modified PDB residue names already present in the project are mapped conservatively:
`MSE` uses the methionine maximum and `CSD` uses the cysteine maximum. Unknown
residue names are left blank rather than guessed.

Updated outputs:

- `data/processed/ppo_1sez_distance_sasa.csv`
- `data/processed/als_1z8n_distance_sasa.csv`
- `data/processed/epsps_8umj_distance_sasa.csv`
- `data/processed/accase_1uys_distance_sasa.csv`
- `data/processed/hppd_5ywg_active_site_metrics.csv`

**Decision:** Phase 4 cross-enzyme synthesis must use `rsa_tien2013` for exposure
comparisons and retain `sasa_A2` only as a traceable raw metric. This change does
not alter completed phase interpretations because the earlier buried/exposed calls
were qualitatively clear-cut; it removes the main metric-scaling caveat before
pooling targets.

---

## 28. Phase 4 pooled mutation table foundation

Phase 4 was started by building the pooled mutation table before any statistical
testing. The current accepted TSR-positive mutation families are PPO, ALS/AHAS,
EPSPS, and ACCase. HPPD remains excluded from the mutation pool because the HPPD
source audit found no accepted weed-evolved target-site amino-acid substitution.

Implemented `scripts/build_phase4_tables.py` as a deterministic join from the
family mutation tables to the matching per-residue static metrics and conservation
outputs. The resulting pooled table is:

- `output/tables/phase4_master_mutation_table.csv`

It contains 15 mutation rows: PPO 6, ALS 2, EPSPS 1, and ACCase 6. Each row carries
native and structure positions, active-site-core membership, distance-to-core,
raw SASA, Tien-normalized RSA, conservation, source, confidence, and mechanism
metadata. Family-specific numbering is preserved rather than flattened away:
ACCase keeps chain-qualified structure positions such as `B:2014`, while PPO,
ALS, and EPSPS use their established structure numbering columns.

HPPD is represented separately in:

- `output/tables/phase4_target_family_contrast.csv`

with `accepted_tsr_rows = 0` and status `no_verified_weed_tsr_accepted`.

**Decision:** use `phase4_master_mutation_table.csv` as the canonical input for
the next cross-enzyme permutation/enrichment analysis, and keep HPPD in a separate
contrast/status table unless a future primary source verifies a weed-evolved HPPD
TSR mutation with accession-level support. This step is table integration only;
the permutation/enrichment statistics and manuscript figures remain next.

---

## 29. Phase 4 permutation/enrichment test and non-core screen

The panel review's biostatistics recommendation was implemented as a within-family
permutation/enrichment test rather than a pooled logistic regression. For each
enzyme family, the analysis draws random residue sets from that same enzyme's
metric table, with set size equal to the number of accepted resistance positions
for that family, and compares the real mean percentile-rank distance-to-core
against the random-set distribution. Lower percentile means closer to the
active-site core.

Repeated accession/replicate rows at the same structural site are de-duplicated to
unique structural positions before the test. This prevents the two PPO ΔG210 rows
and the two PPO G399A rows from overweighting their sites merely because they have
multiple source rows. The pooled mutation table still retains those biological
replicate rows for traceability; only the permutation statistic uses unique
positions.

Implemented `scripts/build_phase4_analysis.py`, producing:

- `output/tables/phase4_permutation_summary.csv`
- `output/tables/phase4_non_core_position_screen.csv`

Current 10,000-iteration results (`seed = 20260704`):

- ACCase: 6 unique positions, observed mean percentile 10.68 vs random mean 49.81,
  empirical lower-tail p = 0.000200.
- ALS: 2 unique positions, observed mean percentile 4.64 vs random mean 49.94,
  empirical lower-tail p = 0.002200.
- EPSPS: 1 unique position, observed percentile 12.87 vs random mean 50.35,
  empirical lower-tail p = 0.131887.
- PPO: 4 unique positions, observed mean percentile 8.01 vs random mean 50.35,
  empirical lower-tail p = 0.000400.

**Interpretation decision:** PPO, ALS, and ACCase currently support the manuscript's
central structural-zone claim: accepted TSR positions are substantially closer to
the active-site core than same-family random residues. EPSPS is directionally
consistent but has only one accepted mutation position, so its p-value should be
treated as underpowered/descriptive, not as a family-level negative result.

The non-core screen keeps the novelty/outlier question visible. More distal
non-core candidate positions under the current percentile threshold include
ACCase Cys2088Arg (25.9th percentile), PPO V361A (20.2nd percentile), EPSPS
Pro106Ser (12.9th percentile), ACCase Gly2096Ala (12.8th percentile), and ACCase
Trp2027Cys (10.4th percentile). PPO ΔG210 remains classified as non-core-adjacent
(8.2nd percentile), matching its established story as adjacent to the active-site
zone but mechanistically distinctive by deletion/helix effects.

**Decision:** use the permutation summary and non-core screen as the quantitative
Phase 4 backbone for manuscript figures and Results text. Do not treat HPPD as a
mutation-family datapoint; keep it as the contrast case recorded in §25 and §28.

---

## 30. Static-vs-dynamic review response and manuscript framing

A later critical review argued that static distance/RSA/conservation metrics cannot
capture molecular dynamics, induced fit, loop breathing, solvent effects, or binding
free energy. That critique is scientifically valid as a limitation, but it does not
change the project scope. The project remains a comparative static structural
bioinformatics resource, not a mutant-state MD or free-energy prediction pipeline.

The review was reconciled in `docs/REVIEW_RESPONSE_STATIC_VS_DYNAMIC.md` by sorting
its points into: already addressed, valid limitation, out of scope, and future work.
Key decisions:

- Do **not** add a new molecular dynamics pipeline.
- Cite literature MD/docking/kinetic/free-energy studies as mechanism benchmarks
  where they exist.
- Present the central claim as structural-zone enrichment plus mechanism
  annotation, not prediction of binding energetics.
- Keep HPPD as a no-verified-weed-TSR contrast case.
- Treat EPSPS Pro106Ser as directionally close but underpowered in the current
  permutation analysis and mechanistically allosteric/hinge-like rather than a
  direct ligand-contact residue.

Implemented `scripts/build_review_driven_outputs.py`, producing:

- `output/tables/phase4_mechanism_annotations.csv`
- `output/tables/manuscript_table_1_family_permutation_summary.csv`
- `output/tables/manuscript_table_2_unique_position_mechanisms.csv`
- `output/tables/manuscript_table_3_hppd_contrast_status.csv`
- `output/figures/figure_1_workflow.svg`
- `output/figures/figure_2_permutation_enrichment.svg`
- `output/figures/figure_3_position_screen.svg`
- `output/figures/figure_4_distance_rsa_conservation.svg`

The mechanism annotation table uses a controlled vocabulary:
`direct_core`, `adjacent`, `second_shell_channel`, `allosteric_hinge`,
`interface_induced_fit`, and `unresolved_static_candidate`. Unresolved mechanisms
are not promoted to literature-supported conclusions; PPO V361A remains
`unresolved_static_candidate` with `static_supported` evidence only.

**Decision:** manuscript development should now proceed from these outputs. The
Results text should emphasize that static metrics identify structural context and
enrichment, while literature mechanism annotations explain dynamic/biophysical
interpretation where supported.

---

## 31. First manuscript draft assembled from Phase 4 outputs

The first full manuscript scaffold was assembled in `docs/MANUSCRIPT_DRAFT.md`.
It is a review-ready internal draft, not a final submission file. The draft uses
the current Phase 4 outputs as its evidence spine:

- family-level permutation/enrichment results;
- unique-position mechanism annotations;
- HPPD as a no-verified-weed-TSR contrast family;
- four generated SVG figures;
- the static-vs-dynamic scope boundary recorded in section 30.

**Decision:** make the next review step a citation/gap audit rather than new
pipeline expansion. The manuscript draft should be polished by adding
sentence-level citations, checking mechanism claims against the saved PDFs, and
deciding whether ALS/AHAS should be expanded to additional accepted positions
before submission. ColabFold remains a future tool for FAT/DHODH or other targets
without adequate structures; it is not part of the current Phase 4 manuscript
claim.

---

## 32. ACCase weed-sequence homology model replaces yeast side-chain metrics

The senior-review ACCase caveat was resolved by building the black-grass
AJ310767 carboxyltransferase-domain sequence on the inhibitor-bound 1UYS template
through SWISS-MODEL. The completed model is a homodimer with GMQE 0.76 and
QMEANDisCo global 0.72 +/- 0.05. It preserves the weed wild-type residues at the
accepted ACCase positions and removes the previous yeast-side-chain mismatch at
Ile1781, Ile2041, Cys2088, and Gly2096.

SWISS-MODEL did not transfer haloxyfop (`H1L`) because the binding site failed
its ligand-transfer conservation rule. Therefore the ACCase active-site core is
still defined from the aligned 1UYS H1L-contact residues, while distance, SASA,
RSA, and structural coordinates are computed on the weed-sequence homology model.

The active Phase 4 ACCase metric file is now
`data/processed/accase_swissmodel_1uys_distance_sasa.csv`, generated by
`scripts/accase_swissmodel_distance_sasa.py`. Current ACCase accepted positions
map to model coordinates:

- Ile1781Leu -> A:143.
- Trp2027Cys -> B:389.
- Ile2041Asn -> B:403.
- Asp2078Gly -> B:440.
- Cys2088Arg -> B:450.
- Gly2096Ala -> B:458.

The rerun changed the ACCase enrichment values because the background is now the
1,132-residue SWISS-MODEL dimer rather than the older 1UYS B+C metric table:
all accepted ACCase positions have observed mean percentile 13.24 versus random
50.20 (p = 0.000300), and non-core-only ACCase positions have observed mean
percentile 18.00 versus random 50.14 (p = 0.010199).

**Decision:** use the SWISS-MODEL weed CT-domain dimer for ACCase Phase 4
metrics and manuscript tables. Keep the old 1UYS metric files/scripts as
provenance, but describe current ACCase side-chain metrics as homology-model
derived, with active-site-core membership transferred from 1UYS H1L contacts.
