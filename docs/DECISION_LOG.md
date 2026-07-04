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

## 17. External review received and reconciled — ALS active-site core corrected, HPPD plan revised before it starts

User supplied an external "senior review" (a fact-check tool) that could not
access this private repo (confirmed 404 on all endpoints) and so reviewed a
*different* task brief describing ACCase/EPSPS/HPPD/FAT/DHODH plans - not our
actual completed PPO/ALS work. Full reconciliation in
`docs/EXTERNAL_REVIEW_RESPONSE.md`. Two things genuinely applied to completed
work, checked directly rather than taken on faith:

1. **Confirmed and fixed: ALS's active-site core was missing dimer-interface
   residues.** Re-checked the review's general claim (AHAS binding occurs at a
   dimer interface, McCourt et al. 2006) directly against 1Z8N. Found and fixed a
   coordinate-frame bug in the diagnostic (`atom.coord` vs `atom.scene_coord`
   across symmetry copies gave a false negative first), then confirmed 11 real
   interface residues from a neighboring subunit, including **Ala122 and Pro197**
   - two positions this pilot deliberately scoped out (§12) - which turn out to
   be genuine interface pocket residues, explaining mechanistically why they're
   documented resistance hotspots. Core expanded from 16 to 27 residues; Trp574/
   Ser653 conclusion unchanged (both remain direct ligand-contact core members,
   fully conserved); only secondary percentile figures shifted (22.0→31.8,
   1.7→3.1). `als_1z8n_distance_sasa.csv` and `als_validation_gate_results.md`
   recomputed accordingly.
2. **Valid, not yet applied: raw SASA should become relative solvent
   accessibility (RSA)** per Tien et al. 2013 before Phase 4's cross-enzyme
   comparison, where raw Å² isn't comparable across enzymes with different
   residue-size distributions. Doesn't change any PPO/ALS conclusion so far (all
   buried/exposed calls were clear-cut, not borderline), but needs doing before
   pooling data across enzymes.

**For the enzymes not yet started (ACCase, EPSPS, HPPD, FAT, DHODH), see
`EXTERNAL_REVIEW_RESPONSE.md` Part 2** for the specific facts to adopt -
critically, **do not use "Gly336" as an HPPD weed resistance mutation** (it's an
engineered *Pseudomonas fluorescens* crop-tolerance variant, not evolved
resistance; real weed HPPD resistance is predominantly non-target-site per Nakka
et al. 2017) - and a reminder to repeat the dimer-interface cross-chain check
(item 1 above) for ACCase's CT domain before assuming a single-chain active-site
core there too.

---

## 18. How the files in this repo relate

- **This file (`DECISION_LOG.md`)** — the *why*: every directional decision and correction, in the order they were made.
- **`CONTRIBUTING.md`** — working conventions for this repo (currently: how to handle paywalled/bot-blocked sources, §13).
- **`PPO_Phase1_Final_Validated_Brief.md`** — the *what*: the current, fully-cross-checked PPO dataset, numbering keys, mechanism classes, and validation-gate numbers.
- **`als_mutation_candidates.md`** / **`als_mutations.csv`** / **`als_validation_gate_results.md`** — the equivalent trio for the ALS/AHAS pilot: resolution trail, working dataset, and validation-gate results.
- **`rangani_2019_table2_cross_resistance.csv`** — external validation dataset (real IC50/resistance-factor data, 13 herbicides × 3 mutations, common genetic background).
- **`docs/references/`** — primary-source PDFs now available directly in the repo (Dayan et al. 2010, Hao et al. 2009, Giacomini et al. 2017, Larran et al. 2017), not just summarized secondhand in the briefs. Verification claims in `VERIFICATION_LOG.md` that cite these papers can be checked against the actual text.
- **`EXTERNAL_REVIEW_RESPONSE.md`** — reconciliation of an external fact-check review against this repo's actual state: what genuinely applied and was fixed (ALS interface core), what's valid but not yet applied (RSA normalization), and what to adopt when ACCase/EPSPS/HPPD/FAT/DHODH are built (§17).
