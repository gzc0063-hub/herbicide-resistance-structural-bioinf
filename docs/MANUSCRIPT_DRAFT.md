# Comparative Static Structural Mapping of Target-Site Herbicide Resistance Across Weed Enzyme Families

**Gourav Chahal**

Department of Crop, Soil and Environmental Sciences, Auburn University, Auburn, AL, USA

Corresponding author: Gourav Chahal, gzc0063@gmail.com

ORCID iD: [to be added]

Status: citation-formatted draft prepared for submission to *Pest Management Science*. In-text citations
use PMS's superscript sequential-numbering style; the reference list is ordered by first appearance in
the text. See the Citation and Submission To-Do section for remaining pre-submission items.

## Abstract

Target-site herbicide resistance (TSR) is usually studied one enzyme family at a time, obscuring whether resistance substitutions occupy similar structural zones across unrelated targets. We built a comparative static structural-bioinformatics resource for verified weed TSR positions in protoporphyrinogen oxidase (PPO), acetolactate synthase (ALS/AHAS), 5-enolpyruvylshikimate-3-phosphate synthase (EPSPS), and acetyl-CoA carboxylase (ACCase), with 4-hydroxyphenylpyruvate dioxygenase (HPPD) as a target-site-negative contrast. For each position we mapped a herbicide-relevant structure, defined an active-site core, and calculated distance-to-core percentile, relative solvent accessibility, conservation, and a static biophysical perturbation score (volume/hydropathy/charge change), then tested enrichment against random same-family residues. Accepted positions were strongly enriched near active-site cores in PPO, ALS/AHAS, and ACCase (p ≤ 0.0004); a pooled test combining all four families' non-core positions (n = 8) confirmed the signal is not tautological (p = 0.0001). Expanding EPSPS to two verified positions moved it from a single descriptive point to a significant test (p = 0.015). ACCase was evaluated on a homology-modeled black-grass carboxyltransferase dimer (53.3% identity to its 1UYS template, above the ~30% homology "twilight zone"). The resource's main contribution is a reproducible structural typology of direct-contact, adjacent, second-shell, deletion-linked, and dimer-interface positions, resolving how, not only whether, resistance positions relate to the active site.

## Introduction

Target-site resistance (TSR) remains one of the clearest molecular routes by which weeds survive herbicide selection. A single amino-acid substitution or deletion can reduce herbicide sensitivity while preserving enough enzyme function for plant survival. The most familiar examples are usually discussed within individual site-of-action families: PPO deletions or substitutions, ALS/AHAS pocket mutations, EPSPS Pro106 substitutions, and ACCase carboxyltransferase-domain substitutions. This family-by-family framing is useful for diagnosis, but it leaves a comparative question unresolved: do accepted TSR positions occupy a recurring structural landscape across unrelated herbicide targets?

Existing structural and biochemical work already shows that resistance mechanisms are not limited to direct ligand-contact replacements. Some positions sit in the binding pocket itself, while others act through adjacent loops, channel geometry, helix packing, allosteric opening/closing motions, or dimer-interface induced-fit effects. A purely static distance metric cannot reproduce those dynamic mechanisms. However, static structure can still answer a different and tractable question: whether known resistance positions occupy unusually close, conserved, or exposed/buried structural zones relative to the rest of the enzyme family.

This project was designed as a comparative static structural-bioinformatics resource, not as a mutant-state molecular dynamics or binding free-energy prediction engine. The goal is to standardize mutation curation, structure selection, active-site-core definition, distance percentile, RSA, and conservation across enzyme families, then use those outputs to identify broad enrichment patterns and mechanistically interesting exceptions. Where literature has already established dynamic or kinetic explanations, those studies are used as interpretation benchmarks rather than reimplemented.

We are explicit about what is expected versus what is novel. That accepted TSR positions cluster near the active-site core is the expected result, and for direct-contact residues it is nearly tautological because the core is defined by ligand contact. The intended contribution is therefore not the enrichment itself but the standardized, reproducible framework that (i) confirms the enrichment survives after removing guaranteed-zero direct-core positions, and (ii) resolves the accepted positions into a small typology of structural relationships to the pocket, foregrounding the non-obvious, non-contact cases that a single "near the active site" statement obscures.

We piloted and validated the workflow on PPO, then extended it to ALS/AHAS, EPSPS, ACCase, and HPPD. HPPD was retained differently: a primary-source audit found no accepted weed-evolved HPPD target-site amino-acid substitution suitable for the pooled TSR mutation table, so HPPD is included as a structural contrast case rather than forced into a false-positive mutation analysis.

## Materials and Methods

### Source Curation and Mutation Inclusion

Mutation rows were included only when supported by primary literature or accession-level evidence consistent with project curation rules. PPO, ALS/AHAS, EPSPS, and ACCase were represented by accepted weed target-site resistance positions. Repeated accessions or biological rows mapping to the same structural residue were retained in the master traceability table but de-duplicated to unique structural positions for the Phase 4 enrichment test.

The curation workflow intentionally avoided accession inference by sequence-length matching, pattern guessing, or elimination. When accessions were absent from visible source text, the mutation could remain as a literature-supported row if the paper itself established the amino-acid change, but it was not assigned a fabricated accession. Unpublished or lower-confidence contextual sequences were not used as manuscript-reliant anchors.

### Structure Selection

Each target family was mapped to a real protein structure selected for herbicide relevance, ligand state, plant/source relevance where possible, and interpretability of the active-site zone.

PPO used the tobacco (*Nicotiana tabacum*) mitochondrial PPO2 structure 1SEZ.<sup>1</sup> ALS/AHAS used 1Z8N with an interface-aware active-site core.<sup>2</sup> EPSPS used maize (*Zea mays*) EPSPS structure 8UMJ complexed with glyphosate and shikimate-3-phosphate; the RCSB-linked primary citation for 8UMJ concerns evolving dual-trait EPSPS variants using a synthetic yeast selection system and includes the wild-type *Z. mays* EPSPS-glyphosate-S3P structure used here.<sup>3</sup> ACCase used a SWISS-MODEL black-grass (*Alopecurus myosuroides*) carboxyltransferase-domain homodimer built from AJ310767 residues 1639-2204 on the yeast 1UYS template,<sup>4</sup> preserving the dimer context needed for ACCase resistance-site interpretation. HPPD used Arabidopsis plant HPPD structures, especially 5YWG with mesotrione and metal, as a contrast structural module; the RCSB-linked primary citation for 5YWG is an enzyme-kinetics, X-ray crystallography, and computational-simulation study of the HPPD inhibition mechanism, not a weed-resistance report.<sup>5</sup>

### Active-Site Core Definitions

Active-site cores were defined by family-specific structural evidence rather than a single arbitrary residue list. Ligand-contact cores were generated from residues within the adopted contact threshold around bound herbicides, substrates, cofactors, or metals when those ligands were present and relevant. For PPO, the validated active-site reference from Heinemann et al.<sup>6</sup> was retained as the primary core. For ALS/AHAS, the core was expanded after review to include dimer-interface pocket residues, including the Ala122/Pro197 zone, because ALS inhibitor binding is not confined to a single-chain pocket.

The primary cross-family distance field is `distance_to_active_site_core_A`, where direct core residues have distance 0 A. A secondary nearest-other-core spacing field is retained where useful but is not the pooled distance metric.

### Distance Percentile, RSA, and Conservation

For every residue in each structure, the pipeline calculated distance to the active-site core and converted that value to a within-family percentile rank. This makes enzymes of different sizes and architectures comparable: a low percentile means a residue lies unusually close to the active-site core within its own protein.

Solvent exposure is recorded as both raw solvent-accessible surface area (`sasa_A2`) and Tien-normalized relative solvent accessibility (`rsa_tien2013`).<sup>7</sup> Raw SASA is retained for traceability, while RSA is preferred for cross-enzyme comparisons because residue type affects maximum accessible area.

Conservation was estimated from curated multi-species sequence panels using alignment-based Shannon entropy and normalized conservation scores. Conservation values are interpreted as supporting structural constraint, not as direct evidence of herbicide resistance by themselves.

### Biophysical Perturbation Score

As a static, fully reproducible complement to distance percentile and RSA, we computed a per-position biophysical perturbation score from the absolute difference between the weed wild-type and mutant residue on three published, literature-tabulated scales: side-chain bulkiness<sup>8</sup> (a volume/length-ratio measure, used here in place of the classic Chothia volume table, which could not be independently re-verified against a live source during this work), Kyte-Doolittle hydropathy,<sup>9</sup> and formal side-chain charge at physiological pH. This is not a physics-based free-energy estimator: no licensed thermodynamic tool (FoldX, DDGun) or structure-prediction API (AlphaFold3, ESMFold) was available in this project's computing environment, so the score is reported as an orthogonal, transparent property-difference axis alongside distance percentile and RSA, not as a ΔΔG substitute.

### Phase 4 Enrichment Analysis

For PPO, ALS/AHAS, EPSPS, and ACCase, accepted mutation rows were joined to their family-specific distance, RSA, and conservation tables. Rows were then collapsed to unique structural positions for the enrichment test so that repeated source rows did not overweight a single residue.

Within each family, the observed mean distance-to-core percentile for accepted resistance positions was compared against 10,000 random same-size residue sets drawn from that family structure. The empirical lower-tail p-value measures how often random residue sets are at least as close to the active-site core as the observed accepted positions. The randomization seed was 20260704. To guard against the enrichment being driven by direct-contact residues that score zero distance by construction, the test was run twice per family: once on all accepted positions (`all`) and once on non-core positions only (`non_core_only`), the latter removing the guaranteed-zero direct-core residues.

### Global Combined Permutation Test

To move beyond four isolated per-family p-values toward a single cross-family statistical statement, we additionally pooled every unique accepted position across all four families into one combined cohort and drew random same-size sets from the combined background (every family's per-residue percentile pool concatenated), repeating the same 10,000-iteration empirical-p-value procedure. This was run once on all pooled positions (`combined_all`, n = 17) and once on pooled non-core positions only (`combined_non_core_only`, n = 8). This pooled test is deliberately simpler than a generalized linear mixed-effects model with family as a random effect: no R, `rpy2`, or `lme4` installation was available in this project's computing environment, so a mixed-effects implementation was not attempted. In the pooled test, each background residue - not each family - is equally likely to be drawn, so larger protein structures contribute proportionally more to the random distribution; the result should be read as a pooled-cohort permutation p-value, not as a family-random-effects estimate.

### Template and Homology-Model Transparency

Because structures were selected for herbicide relevance rather than exact species match, the mapped structure residue is not always guaranteed to be the same amino acid as the weed residue. The master table records `weed_wt_residue`, `template_residue`, `template_matches_weed_residue`, and `template_is_resistant_state` for every position. PPO, ALS/AHAS, EPSPS, and the current ACCase SWISS-MODEL rows all match the weed wild-type residue at the accepted positions. ACCase remains model-based rather than experimentally solved: the black-grass CT-domain dimer was homology-modeled on 1UYS, and the ligand-contact core was transferred from 1UYS because SWISS-MODEL excluded H1L. Thus ACCase SASA/RSA are weed-sequence homology-model metrics, not direct crystal-observed side-chain measurements.

### Mechanism Annotation

Each unique mutation position was assigned a controlled mechanism label: `direct_core`, `adjacent`, `second_shell_channel`, `allosteric_hinge`, `interface_induced_fit`, or `unresolved_static_candidate`. These labels are interpretive annotations, not new mechanistic proofs. Literature-supported labels were used when prior biochemical, kinetic, docking, molecular-dynamics, or structural work supported the mechanism class. Static-supported unresolved positions were not promoted to high-confidence dynamic mechanisms.

## Results

### Workflow and Dataset Scope

The pipeline links source-verified TSR curation, structure selection, active-site-core definition, residue-level static metrics, family-level permutation testing, and mechanism annotation (Figure 1). The current pooled TSR table contains PPO, ALS/AHAS, EPSPS, and ACCase mutation rows. HPPD is retained separately as a contrast family because the source audit did not identify an accepted weed-evolved HPPD TSR amino-acid substitution suitable for mutation-row pooling.

![Figure 1. Workflow and target families.](../output/figures/figure_1_workflow.svg)

### Accepted TSR Positions Are Enriched Near Active-Site Cores

We first establish the expected baseline before turning to the informative exceptions. Across the current target families, accepted TSR positions fall much closer to active-site cores than random same-family residues (Figure 2; Table 1). ACCase had six unique mutation positions with an observed mean percentile of 13.24, compared with a random mean of 50.20 (empirical p = 0.0003). ALS/AHAS had five unique positions (all direct-core, after adding Asp376Glu<sup>10</sup>) with an observed mean percentile of 4.64 versus 50.03 (p = 0.0001). PPO had four unique positions with an observed mean percentile of 8.01 versus 49.86 (p = 0.0004).

This enrichment is expected for direct ligand-contact residues, which score zero distance by the core definition, so it is important that the signal is not merely re-stating that definition. When the direct-core positions are removed and only non-core accepted positions are tested, the enrichment persists: PPO non-core positions (n = 3) have an observed mean percentile of 10.39 (p = 0.0059) and ACCase non-core positions (n = 4) 18.00 (p = 0.0102). ALS/AHAS has no non-core accepted position in the current set (Trp574, Ser653, Ala122, Pro197, and Asp376 are all direct-core interface-pocket residues), so no non-core test is reported for it. The persistence of enrichment among non-core positions is the non-tautological form of the result and is the more informative finding; the global combined permutation test below strengthens this further.

EPSPS now has two unique accepted positions after adding Thr102Ile<sup>11</sup> alongside Pro106Ser: an observed mean percentile of 9.37 versus a random mean of 50.03 (p = 0.0147). This is a genuine improvement, not a cosmetic one - EPSPS moves from a single descriptive point (previously p = 0.129, not significant) to a directionally consistent, statistically significant two-position test. It remains the smallest of the four pooled families, and its non-core-only subset (Pro106Ser alone, n = 1) is still best read as descriptive (p = 0.130).

![Figure 2. Observed versus random distance percentile by family.](../output/figures/figure_2_permutation_enrichment.svg)

### A Global Combined Permutation Test Strengthens the Cross-Family Signal

Reporting four separate per-family p-values leaves open the question of whether a single, more powerful cross-family statistical statement is possible without the four tests being pseudo-independent restatements of each other. We addressed this with a global combined permutation test that pools every unique accepted position across all four families into one cohort and draws random same-size sets from the combined background residue pool (Methods). Pooling all 17 accepted positions gives an observed mean percentile of 9.02 against a combined random mean of 50.13 (p = 0.0001). Critically, pooling only the 8 non-core accepted positions across all four families - the non-tautological subset - gives an observed mean percentile of 14.51 against a combined random mean of 50.22 (p = 0.0001), a substantially more powerful result than any individual family's non-core test alone (PPO p = 0.0059, n = 3; ACCase p = 0.0102, n = 4, reported above). This combined result is the single strongest piece of evidence in this resource that the non-core enrichment signal is real and not an artifact of any one family's core definition, template choice, or sample size.

### A Structural Typology of Resistance Positions (the main contribution)

The core contribution of this resource is not the enrichment above but the reproducible typology it enables: resolving accepted positions by *how* they relate to the pocket rather than only *whether* they are near it. The unique-position screen separates direct-core substitutions from adjacent, second-shell/channel, and more distal non-core candidates (Figure 3; Table 2). Direct-core examples include PPO R98G/R98M,<sup>12</sup> ALS/AHAS Trp574Leu, Ser653Asn, and Ala122Ser,<sup>13</sup> and Pro197Ala,<sup>14,15</sup> the latter two among the most firmly established ALS TSR sites,<sup>16</sup> ALS/AHAS Asp376Glu<sup>10</sup> (a clean single-SNP substitution in *Sinapis alba* with no co-occurring amino-acid change elsewhere in the gene, unlike Ala122Ser), ACCase Ile2041Asn,<sup>17,18</sup> and EPSPS Thr102Ile<sup>11</sup> (part of the naturally-evolved TIPS double mutation with Pro106Ser in *Eleusine indica*, though Thr102Ile has never been observed or shown viable as a standalone mutation) under the current active-site-core definitions. These positions are useful positive controls: static proximity is expected to be informative because the residues lie in or at the validated binding pocket. They anchor one end of the typology but are not, on their own, a finding.

The non-core positions are the more mechanistically informative part of the resource. PPO ΔG210<sup>19,20</sup> is adjacent to the active-site zone but is better interpreted through deletion-linked helix or loop effects than through distance alone; G399A<sup>21</sup> is a second PPO adjacent (non-core) position supported by the same active-site-region literature. EPSPS Pro106Ser is close to the glyphosate/S3P site but sits just outside the 4.5 Å atomic-contact core; it is a binding-site-associated (second-shell) residue — the substitution corresponds to the *Salmonella typhimurium* glyphosate-insensitive EPSPS change<sup>22</sup> and reduces glyphosate affinity — and its non-core classification reflects the contact-distance cutoff, not evidence of allostery. ACCase Cys2088Arg<sup>18</sup> is the most distal accepted ACCase position in the current screen; it remains within the broader dimer-interface resistance zone, and the SWISS-MODEL residue is the expected weed wild-type cysteine. Its remaining caveat is that ACCase active-site-core membership is transferred from the ligand-bound 1UYS template because the homology model itself lacks H1L.

For interpretation benchmarks, the flagship non-core cases now map cleanly to source-supported mechanisms: Dayan et al.<sup>20</sup> provide the kinetic/MD benchmark for PPO ΔG210, Hao et al.<sup>23</sup> are retained as the secondary computational account, and the ACCase CT-domain interpretation is grounded in Délye et al.,<sup>17</sup> Yu et al.,<sup>18</sup> and the inhibitor-bound 1UYS structure from Zhang et al.<sup>4</sup>

![Figure 3. Unique mutation-position screen.](../output/figures/figure_3_position_screen.svg)

### RSA and Conservation Add Context Without Replacing Mechanism

Distance percentile, RSA, and conservation jointly describe the structural context of each accepted position (Figure 4). Many accepted positions are both close to the active-site core and highly conserved, consistent with the expectation that TSR often arises at constrained functional sites where limited changes can alter herbicide response. However, these metrics are not interchangeable. A conserved adjacent residue may mark a mechanically important pocket feature, while a less-conserved non-core position may be a permissive site whose resistance mechanism remains unresolved.

PPO V361A<sup>24</sup> illustrates this caution. The static screen places it outside the immediate core, but its conservation score is modest relative to stronger mechanistic examples. It remains a valid resistance mutation row, but the current resource labels it as an unresolved static candidate rather than assigning a literature-supported dynamic mechanism.

![Figure 4. Distance percentile versus RSA and conservation.](../output/figures/figure_4_distance_rsa_conservation.svg)

### HPPD Is a Contrast Family, Not a Forced TSR-Positive Dataset

HPPD was not pooled into the mutation enrichment analysis because the project source audit found no accepted weed-evolved HPPD target-site amino-acid substitution suitable for inclusion. Nakka et al.<sup>25</sup> instead documented non-target-site cytochrome P450-mediated mesotrione metabolism plus 4-12-fold HPPD overexpression as the resistance mechanism in the audited Palmer amaranth (*Amaranthus palmeri*) case, with no target-site amino-acid mutation. Accordingly, HPPD is represented here by plant HPPD active-site metrics and a status table documenting `no_verified_weed_tsr_accepted` with zero accepted TSR rows (Table 3).

This contrast is important for the manuscript's credibility. It shows that the resource does not force every herbicide target into a TSR-positive framework when the literature points instead toward non-target-site mechanisms such as metabolism, expression changes, or polygenic detoxification.

## Discussion

This comparative analysis supports a structural-zone enrichment view of target-site herbicide resistance. Across PPO, ALS/AHAS, and ACCase, accepted TSR positions are concentrated in low within-family distance-to-core percentiles, despite major differences in enzyme architecture, herbicide chemistry, and resistance literature. EPSPS, now represented by two accepted positions rather than one, is directionally consistent and statistically significant (p = 0.0147), though it remains the smallest pooled family and should be interpreted with that caveat in mind. The global combined permutation test - pooling all 17 accepted positions, and separately all 8 non-core positions, across every family - gives a single, more powerful cross-family statistic (p = 0.0001 for both) than any per-family test alone, without requiring a mixed-effects modeling framework this project's computing environment could not support.

The main contribution is not that every resistance mutation directly contacts herbicide. That would be too narrow and, for several important cases, wrong. Instead, the resource shows that accepted positions cluster within an active-site-associated structural landscape that includes direct pocket residues, adjacent residues, second-shell or channel positions, allosteric/hinge positions, and dimer-interface induced-fit sites. This framing preserves both the quantitative enrichment signal and the mechanistic diversity emphasized by prior family-specific studies.

The review-driven static-versus-dynamic critique is therefore incorporated as a scope boundary. Static metrics can identify where a residue sits, whether that position is unusually close within its family, how exposed it is, and how conserved it appears across a curated sequence panel. Static metrics cannot estimate mutant binding free energy, induced-fit cost, loop breathing, solvent rearrangement, altered catalytic turnover, or cross-herbicide selectivity. Those questions require biochemical assays, docking, molecular dynamics, free-energy calculations, or other mechanism-specific studies.

PPO ΔG210 is the clearest example of why the manuscript should pair static mapping with literature mechanism annotation. The position is close enough to the active-site zone to be captured by the enrichment framework, but the deletion's biological meaning depends on helix-capping destabilization, active-site cavity expansion, and altered inhibition behavior reported by Dayan et al.;<sup>20</sup> Hao et al.<sup>23</sup> is retained as a secondary computational benchmark because it proposed a different hydrogen-bond mechanism that Dayan et al. later critiqued. PPO R98G/R98M anchors the opposite end of the typology: a direct pocket residue whose interpretation is supported by substrate-recognition and docking work on the PPO active-site region (Heinemann et al.;<sup>6</sup> Hao et al.<sup>26</sup>). ACCase provides a third benchmark class. Délye et al.<sup>17</sup> modeled black-grass CT-domain substitutions around the inhibitor-binding cavity and distinguished direct APP-interference, bottom-of-cavity second-shell positions, and broader APP/CHD effects, while Zhang et al.<sup>4</sup> supplies the inhibitor-bound CT-domain template used here and Yu et al.<sup>18</sup> verifies Cys2088Arg as an accepted ACCase resistance substitution. EPSPS Pro106Ser similarly illustrates a close but non-direct position whose interpretation depends on EPSPS conformational and glyphosate-site literature.

By keeping HPPD as a contrast family, the analysis also avoids overextending the TSR framework. HPPD-inhibitor resistance in weeds is often explained by non-target-site processes, and no accepted weed-evolved HPPD amino-acid TSR row was identified for this resource. The contrast table makes that absence visible rather than hiding it as missing data.

## Limitations

This study is a static structural resource. It does not model mutant-state ensembles, free-energy changes, herbicide-specific resistance factors, metabolism, expression, copy-number variation, or field-level resistance evolution. Distance-to-core percentile is a structural-context metric, not a causal mechanism by itself.

The current EPSPS dataset contains two accepted mutation positions (Pro106Ser and Thr102Ile) - a real improvement over the single-position case, but still the smallest pooled family, and its own non-core-only subset (Pro106Ser alone, n = 1) remains descriptive. Thr102Ile carries its own caveat: it has only ever been reported as part of the TIPS double mutation with Pro106Ser in *Eleusine indica*,<sup>11</sup> and the source paper's own authors state that Thr102Ile alone would likely be unfit or non-viable, which is why it has never been observed in isolation in nature; its independent causal contribution to resistance is therefore not isolated, analogous to the Ala122Ser/A282D confound below. The current ALS/AHAS set contains five accepted positions (Trp574Leu, Ser653Asn, Ala122Ser, Pro197Ala, and Asp376Glu). Ala122Ser is included at medium confidence because in its source deposit it co-occurs with a second substitution (A282D); Pro197Ala was detected in Palmer amaranth (*Amaranthus palmeri*) together with Trp574Leu<sup>14</sup> but Pro197 is independently one of the most firmly established ALS TSR sites.<sup>16</sup> Asp376Glu was not found in *A. palmeri* (Singh et al.<sup>14</sup> lists position 376 only as a known locus, undetected in their plants), but a clean, isolated Asp376Glu substitution was verified in a different weed, *Sinapis alba*;<sup>10</sup> its source paper attributes resistance in those populations to this target-site mutation together with a separate, unquantified enhanced-metabolism (NTSR) contribution, so the TSR component recorded here should not be read as the sole resistance mechanism in that population. Paired resistant/susceptible accessions for the remaining reference-numbered positions would further strengthen the family-level section.

We also considered and excluded Gly101Ala, a second EPSPS position sometimes discussed alongside Thr102/Pro106. Gly101Ala is documented almost exclusively in engineered/transgenic contexts (e.g. petunia, canola, and maize herbicide-tolerance biotechnology), not in naturally weed-evolved populations; the *Eleusine indica* primary-source literature checked for this project explicitly reports Gly101 as unmutated in its resistant field populations. Consistent with this project's rule against pooling engineered variants as weed-evolved TSR, Gly101Ala was not added.

Mechanism annotations are only as strong as their evidence level. Rows marked `literature_supported` can be discussed as literature-supported mechanism classes; rows marked `static_supported` or unresolved should not be treated as proven dynamic mechanisms.

A specific structural caveat still applies to ACCase, but it is now a homology-model caveat rather than a yeast-side-chain identity caveat, and it is a defensible one. Its only ligand-bound carboxyltransferase template is the yeast 1UYS structure, which is 53.3% identical to the modeled black-grass CT-domain sequence (confirmed directly from the SWISS-MODEL alignment record) - comfortably above the approximately 30% sequence-identity "twilight zone" below which homology-model backbone and active-site geometry become unreliable.<sup>27</sup> No GPU infrastructure or AlphaFold3/ESMFold API access was available in this project's computing environment to attempt an independent ab initio fold of the weed sequence as a cross-check, so the existing SWISS-MODEL homology model - built specifically on the weed sequence rather than reported on the yeast template directly - remains the structural basis for ACCase. We built a SWISS-MODEL weed CT-domain homodimer on 1UYS and recomputed distance, SASA, and RSA on weed-sequence residues. The model has good global support for this use (GMQE 0.76; QMEANDisCo global 0.72 ± 0.05), but SWISS-MODEL excluded haloxyfop because the binding site was not conserved under its ligand-transfer rules. The active-site core was therefore transferred from aligned 1UYS H1L-contact residues. ACCase side-chain metrics should be read as homology-model-derived structural context, not as measurements from an experimentally solved weed ACCase complex.

Finally, structure choice and active-site-core definition affect the output. The project reduces this risk by documenting each family-specific decision, preserving source files and scripts, using within-family percentiles rather than raw distance across enzymes, running the enrichment both with and without direct-core positions, and recording HPPD as a contrast case rather than fabricating mutation rows.

Two further additions in this analysis carry their own explicit boundaries. The biophysical perturbation score (volume/hydropathy/charge deltas) is a static property-difference axis computed from published amino-acid scales, not a physics-based free-energy estimate; no licensed thermodynamic tool (FoldX, DDGun) was available to compute an actual ΔΔG, and the score should not be read as one. The global combined permutation test is a pooled-cohort statistic, not a generalized linear mixed-effects model with family as a random effect; no R, `rpy2`, or `lme4` installation was available in this project's computing environment to attempt the latter. Both simplifications are reported explicitly here rather than left implicit, and both remain candidates for a future pass in an environment with the relevant licensed software or R installation available.

## Acknowledgments

No acknowledgments to declare.

## Funding

This research received no specific grant from any funding agency, commercial sector, or not-for-profit sector.

## Competing Interests

The author declares no competing interests.

## Data and Code Availability

All curated datasets, scripts, generated tables, generated figures, decision records, and verification logs are maintained in a public GitHub repository: https://github.com/gzc0063-hub/herbicide-resistance-structural-bioinf (MIT license for code; data/tables are CC-BY-4.0). A versioned Zenodo deposit with a permanent data DOI will be created at submission time (see `docs/ZENODO_DEPOSIT_GUIDE.md` for the prepared metadata and remaining steps). The key outputs for this draft are:

- `output/tables/phase4_master_mutation_table.csv`
- `output/tables/manuscript_table_1_family_permutation_summary.csv`
- `output/tables/manuscript_table_2_unique_position_mechanisms.csv`
- `output/tables/manuscript_table_3_hppd_contrast_status.csv`
- `output/figures/figure_1_workflow.svg` (submission-format PDF: `output/figures_pms/figure_1_workflow.pdf`)
- `output/figures/figure_2_permutation_enrichment.svg` (PDF: `output/figures_pms/figure_2_permutation_enrichment.pdf`)
- `output/figures/figure_3_position_screen.svg` (PDF: `output/figures_pms/figure_3_position_screen.pdf`)
- `output/figures/figure_4_distance_rsa_conservation.svg` (PDF: `output/figures_pms/figure_4_distance_rsa_conservation.pdf`)
- `output/figures/figure_5_resistance_zone_map.svg` (PDF: `output/figures_pms/figure_5_resistance_zone_map.pdf`)
- `data/raw/ACCase_Alopecurus_AJ310767_CTdomain_SWISSMODEL_1UYS_homomer.pdb`
- `data/processed/accase_swissmodel_1uys_distance_sasa.csv`

Figures are authored as SVG and regenerated by the scripts in `scripts/`; PMS-submission-format PDFs (Wiley's
general vector-figure requirement, since all five figures are line-art/schematics rather than photographs)
are produced from the SVGs by `scripts/convert_figures_for_pms.py` and live in `output/figures_pms/`,
regenerated whenever the source SVGs change.

## Tables

Table 1. Family-level permutation summary. Source file: `output/tables/manuscript_table_1_family_permutation_summary.csv`.

Table 2. Unique mutation-position mechanism annotations. Source file: `output/tables/manuscript_table_2_unique_position_mechanisms.csv`.

Table 3. HPPD contrast/status summary. Source file: `output/tables/manuscript_table_3_hppd_contrast_status.csv`.

## Figure Captions

Figure 1. Workflow and target families. The resource begins with source-verified mutation curation, maps accepted TSR positions to herbicide-relevant protein structures, defines active-site cores, calculates distance percentile/RSA/conservation, runs within-family permutation enrichment, and adds mechanism annotations. HPPD is retained as a contrast family with no accepted weed-evolved TSR mutation row.

Figure 2. Observed versus random distance-to-core percentile by family. Accepted TSR positions in PPO, ALS/AHAS, ACCase, and EPSPS have much lower observed mean distance percentiles than same-size random residue sets sampled from the same family structures. EPSPS (n = 2 positions) is now directionally consistent and statistically significant, though still the smallest pooled family.

Figure 3. Unique mutation-position screen. Direct-core positions are separated from adjacent and non-core candidates so that the manuscript can distinguish direct ligand-pocket substitutions from mechanistically interesting second-shell, hinge, deletion, or interface-associated positions.

Figure 4. Distance percentile versus RSA and conservation. The scatter view shows how accepted positions combine active-site proximity, solvent exposure, and conservation. These static metrics provide structural context but do not replace literature-supported dynamic or biochemical mechanism evidence.

Figure 5. Resistance-zone map. One lane per enzyme family; each accepted position is placed by its within-family distance-to-core percentile (left = closest to the ligand-contact core) and colored by mechanism label. The shaded left band marks the direct-contact core zone. This schematic view summarizes the typology: ALS positions cluster in the direct-contact zone, PPO and ACCase span direct-core through second-shell/adjacent to more distal interface positions, and EPSPS now shows both a direct-core position (Thr102Ile) and a position just outside the contact core (Pro106Ser). A structure-rendered version (per-family cartoons with positions as spheres) can be produced from `scripts/chimerax_resistance_zone_figures.py` in a ChimeraX GUI/OSMesa environment. Source: `output/figures/figure_5_resistance_zone_map.svg`.

## Citation and Submission To-Do

- ~~Identify and cite the origin papers for the EPSPS structure 8UMJ and the HPPD structure 5YWG.~~
  **Resolved 2026-07-05:** verified directly against RCSB's own entry records. 8UMJ's RCSB primary
  citation is Reed et al. 2024 (ref. 3; PNAS, evolving dual-trait EPSPS variants via yeast selection,
  includes the wild-type *Z. mays* EPSPS-glyphosate-S3P structure used here). 5YWG's RCSB primary
  citation is Lin et al. 2019 (ref. 5; FEBS J, HPPD-inhibition kinetics/crystallography/computational
  study). Neither paper is about weed resistance — both are cited here strictly as the PDB's own
  structure-provenance record, not as resistance evidence.
- ~~Confirm PMS's current figure-file format requirement.~~ **Resolved 2026-07-05:** Wiley's general
  guidelines (PMS has no journal-specific override) require vector figures (plots/graphs/line diagrams)
  as PDF, PS, or EPS — not TIFF, which is for bitmap/photographic figures. All five manuscript figures are
  vector schematics, so PDF is correct. Converted via `scripts/convert_figures_for_pms.py` (svglib +
  reportlab) into `output/figures_pms/`; visually spot-checked all five renders. While re-verifying this,
  found and fixed a real pre-existing bug in `scripts/build_resistance_zone_figure.py`: the label-stagger
  logic only alternated between 2 vertical offsets, so the 4 ALS direct-core positions (which all share
  one percentile) collided into illegible overlapping text in Figure 5. Fixed with a longer offset ladder;
  regenerated and confirmed all 4 labels are now distinct and legible.
- Zenodo deposit: metadata prepared (`CITATION.cff`, `.zenodo.json`), full explanation and remaining
  account-linking/release steps in `docs/ZENODO_DEPOSIT_GUIDE.md`. Deliberately not triggered yet — the
  manuscript is still being edited, and cutting a release now would archive a stale snapshot.
- ORCID: placeholder added (`[to be added]` in the author block; commented-out field in `CITATION.cff`
  and omitted from `.zenodo.json`) — left for the author to fill in.
- Reference DOIs are retained in the list below for verifiability; confirm whether PMS's final production
  style wants them displayed or suppressed at proof stage.
- ~~Decide whether FAT and DHODH belong in this manuscript or should remain future work.~~ **Resolved
  2026-07-05:** a dedicated Phase 5 primary-source audit (`docs/PHASE5_FAT_DHODH_AUDIT.md`,
  `data/processed/phase5_risk_table.csv`) found neither target has a weed-evolved target-site mutation on
  record — the FAT R171/H112Q/W173L/P192R variants (Wagner et al. 2026) are docking-guided engineered
  mutants, and the DHODH G198E/A141T variants (Kang et al. 2023) are EMS lab-selected Arabidopsis lines.
  Both remain future work; neither is pooled into this manuscript's Phase 4 tables or enrichment analysis.
- **2026-07-07 (Phase 6 pass):** expanded EPSPS to n=2 (Thr102Ile added; Gly101Ala verified and excluded
  as engineered/transgenic-only), expanded ALS to n=5 (Asp376Glu added, verified in *Sinapis alba*), added
  a static biophysical perturbation score (bulkiness/hydropathy/charge deltas) and a global combined
  permutation test as pure-Python alternatives to FoldX/DDGun and an R/lme4 GLMM, neither of which is
  available in this project's computing environment. See `docs/DECISION_LOG.md` and
  `docs/VERIFICATION_LOG.md` for the full rationale and source-verification trail. Remaining: confirm the
  Zimmerman 1968 and Kyte-Doolittle 1982 reference page numbers against the primary journal articles
  (used here from independently cross-checked secondary reproductions, e.g. ExPASy ProtScale, rather than
  the original papers themselves) before final submission.

## References

Ordered by first appearance in the text, per PMS style (superscript sequential citation numbers).
(†) = full-text PDF archived in `docs/references/`. DOIs are retained here for verification; see the
Citation and Submission To-Do for whether PMS's final style displays them.

1. Koch M, Breithaupt C, Kiefersauer R, Freigang J, Huber R and Messerschmidt A, Crystal structure of protoporphyrinogen IX oxidase: a key enzyme in haem and chlorophyll biosynthesis. *EMBO J* **23**:1720–1728 (2004). DOI 10.1038/sj.emboj.7600189 [PDB 1SEZ]
2. McCourt JA, Pang SS, King-Scott J, Guddat LW and Duggleby RG, Herbicide-binding sites revealed in the structure of plant acetohydroxyacid synthase. *Proc Natl Acad Sci USA* **103**:569–573 (2006). DOI 10.1073/pnas.0509229103 (†) [PDB 1Z8N]
3. Reed KB, Kim W, Lu H, Larue CT, Guo S, Brooks SM, Montez MR, Wagner JW, Zhang YJ and Alper HS, Evolving dual-trait EPSP synthase variants using a synthetic yeast selection system. *Proc Natl Acad Sci USA* **121**:e2317027121 (2024). DOI 10.1073/pnas.2317027121 [PDB 8UMJ — RCSB primary citation for the wild-type *Zea mays* EPSPS-glyphosate-shikimate-3-phosphate structure used here as the EPSPS structural anchor; the paper's own focus is engineered dual-trait EPSPS variants via yeast selection, not weed resistance]
4. Zhang H, Tweel B and Tong L, Molecular basis for the inhibition of the carboxyltransferase domain of acetyl-coenzyme-A carboxylase by haloxyfop and diclofop. *Proc Natl Acad Sci USA* **101**:5910–5915 (2004). DOI 10.1073/pnas.0400891101 [PDB 1UYS]
5. Lin HY, Yang JF, Wang DW, Hao GF, Dong JQ, Wang YX, Yang WC, Wu JW, Zhan CG and Yang GF, Molecular insights into the mechanism of 4-hydroxyphenylpyruvate dioxygenase inhibition: enzyme kinetics, X-ray crystallography and computational simulations. *FEBS J* **286**:975–990 (2019). DOI 10.1111/febs.14747 [PDB 5YWG — RCSB primary citation for the *Arabidopsis thaliana* HPPD-mesotrione structure used as the HPPD contrast module; an enzyme-kinetics/crystallography/computational mechanism study, not a weed-resistance report]
6. Heinemann IU, Diekmann N, Masoumi A, Koch M, Messerschmidt A, Jahn M and Jahn D, Functional definition of the tobacco protoporphyrinogen IX oxidase substrate-binding site. *Biochem J* **402**:575–580 (2007). DOI 10.1042/BJ20061321 (†)
7. Tien MZ, Meyer AG, Sydykova DK, Spielman SJ and Wilke CO, Maximum allowed solvent accessibilities of residues in proteins. *PLoS ONE* **8**:e80635 (2013). DOI 10.1371/journal.pone.0080635
8. Zimmerman JM, Eliezer N and Simha R, The characterization of amino acid sequences in proteins by statistical methods. *J Theor Biol* **21**:170–201 (1968). [side-chain bulkiness scale, used for the volume component of the biophysical perturbation score in place of the classic Chothia volume table, which could not be independently re-verified against a live source during this work; values cross-checked against ExPASy ProtScale before use]
9. Kyte J and Doolittle RF, A simple method for displaying the hydropathic character of a protein. *J Mol Biol* **157**:105–132 (1982). [hydropathy scale for the biophysical perturbation score; values cross-checked against two independent sources before use]
10. Palma-Bautista C, Vazquez-Garcia JG, Osuna MD, Garcia-Garcia B, Torra J, Portugal J and De Prado R, An Asp376Glu substitution in ALS gene and enhanced metabolism confers high tribenuron-methyl resistance in *Sinapis alba*. *Front Plant Sci* **13**:1011596 (2022). DOI 10.3389/fpls.2022.1011596
11. Yu Q, Jalaludin A, Han H, Chen M, Sammons RD and Powles SB, Evolution of a double amino acid substitution in the 5-enolpyruvylshikimate-3-phosphate synthase in *Eleusine indica* conferring high-level glyphosate resistance. *Plant Physiol* **167**:1440–1447 (2015). DOI 10.1104/pp.15.00146
12. Giacomini DA, Umphres AM, Nie H, Mueller TC, Steckel LE, Young BG, Scott RC and Tranel PJ, Two new PPX2 mutations associated with resistance to PPO-inhibiting herbicides in *Amaranthus palmeri*. *Pest Manag Sci* **73**:1559–1563 (2017). DOI 10.1002/ps.4581 (†)
13. Larran AS, Palmieri VE, Perotti VE, Lieber L, Tuesca D and Permingeat HR, Target-site resistance to acetolactate synthase (ALS)-inhibiting herbicides in *Amaranthus palmeri* from Argentina. *Pest Manag Sci* **73**:2578–2584 (2017). DOI 10.1002/ps.4662 (†)
14. Singh S, Singh V, Salas-Perez RA, Bagavathiannan MV, Lawton-Rauh A and Roma-Burgos N, Target-site mutation accumulation among ALS inhibitor-resistant Palmer amaranth. *Pest Manag Sci* **74**:2286–2295 (2018). DOI 10.1002/ps.5232 (†)
15. Ji M, Yu H, Cui H, Chen J, Yu J and Li X, A new Pro-197-Ile mutation in *Amaranthus palmeri* associated with acetolactate synthase-inhibiting herbicide resistance. *Plants* **14**:525 (2025). DOI 10.3390/plants14040525 (†)
16. Tranel PJ and Wright TR, Resistance of weeds to ALS-inhibiting herbicides: what have we learned?. *Weed Sci* **50**:700–712 (2002). DOI 10.1614/0043-1745(2002)050[0700:RROWTA]2.0.CO;2 (†)
17. Délye C, Zhang X-Q, Michel S, Matéjicek A and Powles SB, Molecular bases for sensitivity to acetyl-coenzyme A carboxylase inhibitors in black-grass. *Plant Physiol* **137**:794–806 (2005). DOI 10.1104/pp.104.046144 (†)
18. Yu Q, Collavo A, Zheng M-Q, Owen M, Sattin M and Powles SB, Diversity of acetyl-coenzyme A carboxylase mutations in resistant *Lolium* populations: evaluation using clethodim. *Plant Physiol* **145**:547–558 (2007). DOI 10.1104/pp.107.105262 (†)
19. Patzoldt WL, Hager AG, McCormick JS and Tranel PJ, A codon deletion confers resistance to herbicides inhibiting protoporphyrinogen oxidase. *Proc Natl Acad Sci USA* **103**:12329–12334 (2006). DOI 10.1073/pnas.0603137103
20. Dayan FE, Daga PR, Duke SO, Lee RM, Tranel PJ and Doerksen RJ, Biochemical and structural consequences of a glycine deletion in the alpha-8 helix of protoporphyrinogen oxidase. *Biochim Biophys Acta* **1804**:1548–1556 (2010). DOI 10.1016/j.bbapap.2010.04.004 (†)
21. Rangani G, Salas-Perez RA, Aponte RA, Knapp M, Craig IR, Mietzner T, Langaro AC, Noguera MM, Porri A and Roma-Burgos N, A novel single-site mutation in the catalytic domain of protoporphyrinogen oxidase IX (PPO) confers resistance to PPO-inhibiting herbicides. *Front Plant Sci* **10**:568 (2019). DOI 10.3389/fpls.2019.00568
22. Baerson SR, Rodriguez DJ, Tran M, Feng Y, Biest NA and Dill GM, Glyphosate-resistant goosegrass. Identification of a mutation in the target enzyme 5-enolpyruvylshikimate-3-phosphate synthase. *Plant Physiol* **129**:1265–1275 (2002). DOI 10.1104/pp.001560 (†)
23. Hao G-F, Zhu X-L, Ji F-Q, Zhang L, Yang G-F and Zhan C-G, Understanding the mechanism of drug resistance due to a codon deletion in protoporphyrinogen oxidase through computational modeling. *J Phys Chem B* **113**:4865–4875 (2009). DOI 10.1021/jp807442n (†)
24. Nie H, Harre NT and Young BG, A new V361A mutation in *Amaranthus palmeri* PPX2 associated with PPO-inhibiting herbicide resistance. *Plants* **12**:1886 (2023). DOI 10.3390/plants12091886
25. Nakka S, Godar AS, Wani PS, Thompson CR, Peterson DE, Roelofs J and Jugulam M, Physiological and molecular characterization of hydroxyphenylpyruvate dioxygenase (HPPD)-inhibitor resistance in Palmer amaranth (*Amaranthus palmeri* S. Wats.). *Front Plant Sci* **8**:555 (2017). DOI 10.3389/fpls.2017.00555 (†)
26. Hao G-F, Tan Y, Yang S-G, Wang Z-F, Zhan C-G, Xi Z and Yang G-F, Computational and experimental insights into the mechanism of substrate recognition and feedback inhibition of protoporphyrinogen oxidase. *PLoS ONE* **8**:e69198 (2013). DOI 10.1371/journal.pone.0069198 (†)
27. Rost B, Twilight zone of protein sequence alignments. *Protein Eng* **12**:85–94 (1999). DOI 10.1093/protein/12.2.85

Structures and models not otherwise cited above: SWISS-MODEL black-grass ACCase CT-domain homodimer built from AJ310767 residues 1639-2204 using 1UYS (ref. 4) as template.
