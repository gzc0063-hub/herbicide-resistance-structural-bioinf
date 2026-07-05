# Comparative Static Structural Mapping of Target-Site Herbicide Resistance Across Weed Enzyme Families

Status: first manuscript draft for internal review. This draft is built from the current Phase 4 outputs and should be citation-polished before submission.

## Abstract

Target-site herbicide resistance is usually studied one enzyme family at a time, which makes it difficult to compare whether resistance substitutions occupy similar structural zones across unrelated herbicide targets. Here, we built a comparative static structural-bioinformatics resource for verified weed target-site resistance positions in protoporphyrinogen oxidase (PPO), acetolactate synthase/acetohydroxyacid synthase (ALS/AHAS), 5-enolpyruvylshikimate-3-phosphate synthase (EPSPS), and acetyl-CoA carboxylase (ACCase), with 4-hydroxyphenylpyruvate dioxygenase (HPPD) retained as a contrast family after source audit found no accepted weed-evolved target-site amino-acid substitution for inclusion.

For each accepted mutation position, we mapped the site onto a ligand-bound or otherwise herbicide-relevant protein structure, defined an active-site core from ligand or validated pocket contacts, and calculated within-family distance-to-core percentile, raw solvent-accessible surface area, Tien-normalized relative solvent accessibility (RSA), and alignment-based conservation. We then de-duplicated repeated accession rows to unique structural positions and tested whether accepted resistance positions are enriched near active-site cores relative to random same-family residue sets.

Accepted resistance positions were strongly enriched in low distance-to-core percentiles for PPO, ALS/AHAS, and ACCase. ACCase showed an observed mean percentile of 10.68 versus a random mean of 49.81 (empirical p = 0.000200), ALS/AHAS 4.64 versus 50.24 (p = 0.000100), and PPO 8.01 versus 50.01 (p = 0.000500). Critically, the enrichment is not an artifact of direct-contact residues scoring zero by construction: when the direct-core positions are removed and only non-core accepted positions are tested, the signal survives for both PPO (n = 3, observed 10.39, p = 0.004300) and ACCase (n = 4, observed 14.44, p = 0.004300). EPSPS showed the same directional pattern for Pro106Ser (12.87 versus 50.57) but is underpowered as a family-level test because the current accepted set contains one mutation position. Mechanism annotation separated direct-core substitutions from adjacent, second-shell/channel, and interface-associated positions, preventing static proximity from being overinterpreted as a binding free-energy model. Because one template (yeast ACCase) is distantly related to the weed enzyme, we report per-position whether the mapped structure residue matches the weed residue, and we treat ACCase side-chain metrics (SASA/RSA) as template-derived rather than weed-specific.

That accepted TSR positions sit near the active site is expected — it is close to the definition of target-site resistance — so proximity enrichment is treated here as a baseline to be established and then moved past, not as the finding. The contribution of the resource is a reproducible cross-family *typology* of how resistance positions relate to the pocket: direct-contact substitutions, binding-site-adjacent and second-shell/channel positions, a deletion-linked helix case (PPO ΔG210), a poorly conserved permissive site (PPO V361A), and distal dimer-interface positions (ACCase Cys2088Arg). The non-core positions — those not explained by direct contact — are the mechanistically informative core of the paper and are where static mapping adds value beyond restating that pocket mutations are in the pocket. Static distance, RSA, and conservation identify where resistance positions sit; literature kinetic, docking, molecular-dynamics, and free-energy studies remain necessary to explain how specific substitutions alter binding, catalysis, conformational sampling, or herbicide selectivity.

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

PPO used the tobacco mitochondrial PPO2 structure 1SEZ. ALS/AHAS used 1Z8N with an interface-aware active-site core. EPSPS used maize EPSPS structure 8UMJ complexed with glyphosate and shikimate-3-phosphate. ACCase used the yeast ACCase carboxyltransferase-domain B+C dimer from 1UYS complexed with haloxyfop, preserving the dimer context needed for ACCase resistance-site interpretation. HPPD used Arabidopsis plant HPPD structures, especially 5YWG with mesotrione and metal, as a contrast structural module.

### Active-Site Core Definitions

Active-site cores were defined by family-specific structural evidence rather than a single arbitrary residue list. Ligand-contact cores were generated from residues within the adopted contact threshold around bound herbicides, substrates, cofactors, or metals when those ligands were present and relevant. For PPO, the validated Heinemann active-site reference was retained as the primary core. For ALS/AHAS, the core was expanded after review to include dimer-interface pocket residues, including the Ala122/Pro197 zone, because ALS inhibitor binding is not confined to a single-chain pocket.

The primary cross-family distance field is `distance_to_active_site_core_A`, where direct core residues have distance 0 A. A secondary nearest-other-core spacing field is retained where useful but is not the pooled distance metric.

### Distance Percentile, RSA, and Conservation

For every residue in each structure, the pipeline calculated distance to the active-site core and converted that value to a within-family percentile rank. This makes enzymes of different sizes and architectures comparable: a low percentile means a residue lies unusually close to the active-site core within its own protein.

Solvent exposure is recorded as both raw solvent-accessible surface area (`sasa_A2`) and Tien-normalized relative solvent accessibility (`rsa_tien2013`). Raw SASA is retained for traceability, while RSA is preferred for cross-enzyme comparisons because residue type affects maximum accessible area.

Conservation was estimated from curated multi-species sequence panels using alignment-based Shannon entropy and normalized conservation scores. Conservation values are interpreted as supporting structural constraint, not as direct evidence of herbicide resistance by themselves.

### Phase 4 Enrichment Analysis

For PPO, ALS/AHAS, EPSPS, and ACCase, accepted mutation rows were joined to their family-specific distance, RSA, and conservation tables. Rows were then collapsed to unique structural positions for the enrichment test so that repeated source rows did not overweight a single residue.

Within each family, the observed mean distance-to-core percentile for accepted resistance positions was compared against 10,000 random same-size residue sets drawn from that family structure. The empirical lower-tail p-value measures how often random residue sets are at least as close to the active-site core as the observed accepted positions. The randomization seed was 20260704. To guard against the enrichment being driven by direct-contact residues that score zero distance by construction, the test was run twice per family: once on all accepted positions (`all`) and once on non-core positions only (`non_core_only`), the latter removing the guaranteed-zero direct-core residues.

### Template-Residue Transparency

Because structures were selected for herbicide relevance rather than exact species match, the mapped structure residue is not always the same amino acid as the weed residue. This is negligible for PPO, ALS/AHAS, and EPSPS (the template residue matches the weed residue at every accepted position) but material for ACCase, whose only ligand-bound carboxyltransferase template is the distantly related yeast enzyme. Four of six ACCase positions map onto a differing yeast residue (2041→Val, 2088→Met, 1781→Leu, 2096→Ala), and at two of these (1781, 2096) the yeast template already carries the resistance-conferring residue. The master table records `weed_wt_residue`, `template_residue`, `template_matches_weed_residue`, and `template_is_resistant_state` for every position. Distance-to-core percentile is robust to this at 55% sequence identity because backbone geometry is conserved, but ACCase side-chain metrics (SASA/RSA) are interpreted as template-derived, not weed-specific, and no ACCase side-chain claim is made from the yeast template.

### Mechanism Annotation

Each unique mutation position was assigned a controlled mechanism label: `direct_core`, `adjacent`, `second_shell_channel`, `allosteric_hinge`, `interface_induced_fit`, or `unresolved_static_candidate`. These labels are interpretive annotations, not new mechanistic proofs. Literature-supported labels were used when prior biochemical, kinetic, docking, molecular-dynamics, or structural work supported the mechanism class. Static-supported unresolved positions were not promoted to high-confidence dynamic mechanisms.

## Results

### Workflow and Dataset Scope

The pipeline links source-verified TSR curation, structure selection, active-site-core definition, residue-level static metrics, family-level permutation testing, and mechanism annotation (Figure 1). The current pooled TSR table contains PPO, ALS/AHAS, EPSPS, and ACCase mutation rows. HPPD is retained separately as a contrast family because the source audit did not identify an accepted weed-evolved HPPD TSR amino-acid substitution suitable for mutation-row pooling.

![Figure 1. Workflow and target families.](../output/figures/figure_1_workflow.svg)

### Accepted TSR Positions Are Enriched Near Active-Site Cores

We first establish the expected baseline before turning to the informative exceptions. Across the current target families, accepted TSR positions fall much closer to active-site cores than random same-family residues (Figure 2; Table 1). ACCase had six unique mutation positions with an observed mean percentile of 10.68, compared with a random mean of 49.81 (empirical p = 0.000200). ALS/AHAS had four unique positions (all direct-core) with an observed mean percentile of 4.64 versus 50.24 (p = 0.000100). PPO had four unique positions with an observed mean percentile of 8.01 versus 50.01 (p = 0.000500).

This enrichment is expected for direct ligand-contact residues, which score zero distance by the core definition, so it is important that the signal is not merely re-stating that definition. When the direct-core positions are removed and only non-core accepted positions are tested, the enrichment persists: PPO non-core positions (n = 3) have an observed mean percentile of 10.39 (p = 0.004300) and ACCase non-core positions (n = 4) 14.44 (p = 0.004300). ALS/AHAS has no non-core accepted position in the current set (Trp574, Ser653, Ala122, and Pro197 are all direct-core interface-pocket residues), so no non-core test is reported for it. The persistence of enrichment among non-core positions is the non-tautological form of the result and is the more informative finding.

EPSPS followed the same directional pattern: Pro106Ser lies at the 12.87th percentile relative to the glyphosate/S3P active-site core, compared with a random mean of 50.57. However, because the current accepted EPSPS set contains one unique position, the EPSPS p-value is best treated as descriptive and underpowered rather than as evidence for absence of enrichment.

![Figure 2. Observed versus random distance percentile by family.](../output/figures/figure_2_permutation_enrichment.svg)

### A Structural Typology of Resistance Positions (the main contribution)

The core contribution of this resource is not the enrichment above but the reproducible typology it enables: resolving accepted positions by *how* they relate to the pocket rather than only *whether* they are near it. The unique-position screen separates direct-core substitutions from adjacent, second-shell/channel, and more distal non-core candidates (Figure 3; Table 2). Direct-core examples include PPO R98G/R98M, ALS/AHAS Trp574Leu, Ser653Asn, Ala122Ser, and Pro197Ala, and ACCase Ile2041Asn under the current active-site-core definitions. These positions are useful positive controls: static proximity is expected to be informative because the residues lie in or at the validated binding pocket. They anchor one end of the typology but are not, on their own, a finding.

The non-core positions are the more mechanistically informative part of the resource. PPO DeltaG210 is adjacent to the active-site zone but is better interpreted through deletion-linked helix or loop effects than through distance alone. EPSPS Pro106Ser is close to the glyphosate/S3P site but sits just outside the 4.5 Å atomic-contact core; it is a binding-site-associated (second-shell) residue — the substitution corresponds to the *Salmonella typhimurium* glyphosate-insensitive EPSPS change (Baerson et al. 2002) and reduces glyphosate affinity — and its non-core classification reflects the contact-distance cutoff, not evidence of allostery. ACCase Cys2088Arg is the most distal accepted ACCase position in the current screen; it remains within the broader dimer-interface resistance zone, but its structural mapping carries an added caveat because it falls in a locally variable alignment region and maps onto a yeast methionine rather than the weed cysteine.

![Figure 3. Unique mutation-position screen.](../output/figures/figure_3_position_screen.svg)

### RSA and Conservation Add Context Without Replacing Mechanism

Distance percentile, RSA, and conservation jointly describe the structural context of each accepted position (Figure 4). Many accepted positions are both close to the active-site core and highly conserved, consistent with the expectation that TSR often arises at constrained functional sites where limited changes can alter herbicide response. However, these metrics are not interchangeable. A conserved adjacent residue may mark a mechanically important pocket feature, while a less-conserved non-core position may be a permissive site whose resistance mechanism remains unresolved.

PPO V361A illustrates this caution. The static screen places it outside the immediate core, but its conservation score is modest relative to stronger mechanistic examples. It remains a valid resistance mutation row, but the current resource labels it as an unresolved static candidate rather than assigning a literature-supported dynamic mechanism.

![Figure 4. Distance percentile versus RSA and conservation.](../output/figures/figure_4_distance_rsa_conservation.svg)

### HPPD Is a Contrast Family, Not a Forced TSR-Positive Dataset

HPPD was not pooled into the mutation enrichment analysis because the project source audit found no accepted weed-evolved HPPD target-site amino-acid substitution suitable for inclusion. Instead, HPPD is represented by plant HPPD active-site metrics and a status table documenting `no_verified_weed_tsr_accepted` with zero accepted TSR rows (Table 3).

This contrast is important for the manuscript's credibility. It shows that the resource does not force every herbicide target into a TSR-positive framework when the literature points instead toward non-target-site mechanisms such as metabolism, expression changes, or polygenic detoxification.

## Discussion

This comparative analysis supports a structural-zone enrichment view of target-site herbicide resistance. Across PPO, ALS/AHAS, and ACCase, accepted TSR positions are concentrated in low within-family distance-to-core percentiles, despite major differences in enzyme architecture, herbicide chemistry, and resistance literature. EPSPS is directionally consistent but currently represented by one accepted position, so it is best used as a mapped case study rather than a family-level statistical result.

The main contribution is not that every resistance mutation directly contacts herbicide. That would be too narrow and, for several important cases, wrong. Instead, the resource shows that accepted positions cluster within an active-site-associated structural landscape that includes direct pocket residues, adjacent residues, second-shell or channel positions, allosteric/hinge positions, and dimer-interface induced-fit sites. This framing preserves both the quantitative enrichment signal and the mechanistic diversity emphasized by prior family-specific studies.

The review-driven static-versus-dynamic critique is therefore incorporated as a scope boundary. Static metrics can identify where a residue sits, whether that position is unusually close within its family, how exposed it is, and how conserved it appears across a curated sequence panel. Static metrics cannot estimate mutant binding free energy, induced-fit cost, loop breathing, solvent rearrangement, altered catalytic turnover, or cross-herbicide selectivity. Those questions require biochemical assays, docking, molecular dynamics, free-energy calculations, or other mechanism-specific studies.

PPO DeltaG210 is the clearest example of why the manuscript should pair static mapping with literature mechanism annotation. The position is close enough to the active-site zone to be captured by the enrichment framework, but the deletion's biological meaning depends on helix/deletion effects and prior biochemical interpretation. ACCase Cys2088Arg provides a different kind of non-core case: a more distal accepted TSR position that remains meaningful in the context of the ACCase dimer-interface pocket. EPSPS Pro106Ser similarly illustrates a close but non-direct position whose interpretation depends on EPSPS conformational and glyphosate-site literature.

By keeping HPPD as a contrast family, the analysis also avoids overextending the TSR framework. HPPD-inhibitor resistance in weeds is often explained by non-target-site processes, and no accepted weed-evolved HPPD amino-acid TSR row was identified for this resource. The contrast table makes that absence visible rather than hiding it as missing data.

## Limitations

This study is a static structural resource. It does not model mutant-state ensembles, free-energy changes, herbicide-specific resistance factors, metabolism, expression, copy-number variation, or field-level resistance evolution. Distance-to-core percentile is a structural-context metric, not a causal mechanism by itself.

The current EPSPS dataset is underpowered for family-level inference because it contains one accepted mutation position. The current ALS/AHAS set contains four accepted positions (Trp574Leu, Ser653Asn, Ala122Ser, Pro197Ala). Ala122Ser is included at medium confidence because in its source deposit it co-occurs with a second substitution (A282D); Pro197Ala was detected in Palmer amaranth together with Trp574Leu (Singh et al. 2018) but Pro197 is independently one of the most firmly established ALS TSR sites. Asp376, although an accepted ALS TSR locus in other species, was not added because no Palmer amaranth primary source detecting it is in hand (Singh et al. 2018 lists it only as a known locus). Adding Asp376 from a verified weed source, and paired resistant/susceptible accessions for the reference-numbered positions, would further strengthen the family-level section.

Mechanism annotations are only as strong as their evidence level. Rows marked `literature_supported` can be discussed as literature-supported mechanism classes; rows marked `static_supported` or unresolved should not be treated as proven dynamic mechanisms.

A specific structural caveat applies to ACCase. Its only ligand-bound carboxyltransferase template is the yeast enzyme, which is ~55% identical to grass plastidic ACCase and differs in residue identity at four of six accepted positions, including two (Ile1781, Gly2096) where the yeast template already carries the resistance-conferring residue. Distance-to-core percentile is robust to this because backbone geometry is conserved, and the non-core enrichment result holds for ACCase after removing direct-core positions. However, ACCase side-chain metrics (SASA/RSA) describe yeast side chains and are reported as template-derived, not weed-specific; a weed-sequence homology model built on the yeast template (as in Délye et al. 2005) would be required before making any ACCase side-chain claim. The master table exposes this per position via `template_matches_weed_residue` and `template_is_resistant_state`.

Finally, structure choice and active-site-core definition affect the output. The project reduces this risk by documenting each family-specific decision, preserving source files and scripts, using within-family percentiles rather than raw distance across enzymes, running the enrichment both with and without direct-core positions, and recording HPPD as a contrast case rather than fabricating mutation rows.

## Data and Code Availability

All curated datasets, scripts, generated tables, generated SVG figures, decision records, and verification logs are maintained in the project repository. The key outputs for this draft are:

- `output/tables/phase4_master_mutation_table.csv`
- `output/tables/manuscript_table_1_family_permutation_summary.csv`
- `output/tables/manuscript_table_2_unique_position_mechanisms.csv`
- `output/tables/manuscript_table_3_hppd_contrast_status.csv`
- `output/figures/figure_1_workflow.svg`
- `output/figures/figure_2_permutation_enrichment.svg`
- `output/figures/figure_3_position_screen.svg`
- `output/figures/figure_4_distance_rsa_conservation.svg`

## Tables

Table 1. Family-level permutation summary. Source file: `output/tables/manuscript_table_1_family_permutation_summary.csv`.

Table 2. Unique mutation-position mechanism annotations. Source file: `output/tables/manuscript_table_2_unique_position_mechanisms.csv`.

Table 3. HPPD contrast/status summary. Source file: `output/tables/manuscript_table_3_hppd_contrast_status.csv`.

## Figure Captions

Figure 1. Workflow and target families. The resource begins with source-verified mutation curation, maps accepted TSR positions to herbicide-relevant protein structures, defines active-site cores, calculates distance percentile/RSA/conservation, runs within-family permutation enrichment, and adds mechanism annotations. HPPD is retained as a contrast family with no accepted weed-evolved TSR mutation row.

Figure 2. Observed versus random distance-to-core percentile by family. Accepted TSR positions in PPO, ALS/AHAS, and ACCase have much lower observed mean distance percentiles than same-size random residue sets sampled from the same family structures. EPSPS is directionally consistent but underpowered because it currently contains one accepted position.

Figure 3. Unique mutation-position screen. Direct-core positions are separated from adjacent and non-core candidates so that the manuscript can distinguish direct ligand-pocket substitutions from mechanistically interesting second-shell, hinge, deletion, or interface-associated positions.

Figure 4. Distance percentile versus RSA and conservation. The scatter view shows how accepted positions combine active-site proximity, solvent exposure, and conservation. These static metrics provide structural context but do not replace literature-supported dynamic or biochemical mechanism evidence.

## Citation and Submission To-Do

- Convert the source-paper names in this draft into journal-formatted citations.
- Audit claims about dynamic mechanisms against the project PDFs and add citations at sentence level.
- Decide whether to expand ALS/AHAS beyond Trp574Leu and Ser653Asn before submission.
- Decide whether FAT and DHODH belong in this manuscript or should remain future work requiring ColabFold/manual structure prediction.
- Review figure aesthetics and labels for the target journal format.
