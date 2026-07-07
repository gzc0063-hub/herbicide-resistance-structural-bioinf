# Project status — read this first

Snapshot of what's done, what every file is for, and what to do next. For a full
navigation map, read `REPO_INDEX.md` first; for current live work, read this file
plus `docs/HANDOFF_NEXT_STEPS.md`, `docs/DECISION_LOG.md`, and
`docs/VERIFICATION_LOG.md`. Check `git status` before assuming every listed
change has been committed and pushed to
https://github.com/gzc0063-hub/herbicide-resistance-structural-bioinf (private
repo).

---

## 1. What's done

- **Phase 0 (setup):** repo scaffolded, GitHub connected, Python venv + packages
  installed, ChimeraX 1.12 installed and confirmed working headlessly, R 4.4.1
  confirmed present, MAFFT installed (external, not in repo - see §4).
- **Phase 1 (PPO pilot): COMPLETE, validation gate PASSED.** Four mutations
  (ΔG210, G399A, V361A, R98G/R98M) fully sourced, cross-checked against four
  primary-source PDFs, and run through the full three-metric pipeline (distance,
  SASA, conservation). Flagship finding: ΔG210 is the strongest structural outlier
  candidate (conserved, adjacent-to-but-outside the active site); V361A was
  investigated as a candidate outlier but downgraded after conservation data showed
  it's a poorly-conserved, likely-permissive site instead.
- **Phase 2, ALS/AHAS pilot: COMPLETE, validation gate PASSED.** Originally four
  accepted mutation positions were represented (Ala122Ser, Pro197Ala, Trp574Leu,
  Ser653Asn; Larran et al. 2017 anchors Ala122/Trp574/Ser653, Singh et al. 2018
  anchors Pro197Ala in *A. palmeri*). External review correctly flagged that the
  AHAS pocket includes dimer-interface residues; fixed core size is 27 residues,
  including Ala122 and Pro197 as interface-pocket residues. Asp376 was initially
  left out because no primary *A. palmeri* source was verified; Phase 6 later
  added it from a different, non-*A. palmeri* weed source (see Phase 6 bullet
  below) - ALS is now five accepted positions.
- **Metric-schema cleanup: COMPLETE.** PPO and ALS distance/SASA tables now separate
  true distance-to-active-site-core from nearest-other-core spacing, so direct
  active-site residues score 0 Å for the primary cross-enzyme distance metric.
- **Phase 2, EPSPS pilot: COMPLETE, validation gate PASSED.** Structure and mutation anchors selected: 8UMJ
  (*Zea mays* EPSPS + glyphosate/S3P) and Baerson et al. 2002 Pro106Ser
  (*E. indica*, AJ417034 susceptible / AJ417033 resistant), mapped to 8UMJ PDB
  residue 106. Ligand-contact active-site core and fallback static SASA have been
  run on 8UMJ; conservation is 1.000 at Pro106 among sequences present at that
  column (7/8).
- **Phase 2, ACCase: COMPLETE, validation gate PASSED.** Six TSR rows
  (Ile1781Leu, Trp2027Cys, Ile2041Asn, Asp2078Gly, Cys2088Arg, Gly2096Ala)
  were verified from Delye et al. 2005 / Yu et al. 2007. Active Phase 4 metrics
  now use the SWISS-MODEL black-grass AJ310767 CT-domain homodimer built on 1UYS;
  H1L was not transferred by SWISS-MODEL, so active-site-core membership is
  transferred from aligned 1UYS H1L-contact residues.
- **Phase 2, HPPD: COMPLETE as structural contrast case, not TSR-positive.**
  Source audit found no accepted weed-evolved HPPD target-site amino-acid
  substitution. HPPD is retained using plant templates 5YWG/1TG5 and a
  metal/inhibitor-contact active-site core. Do not create or pool an HPPD mutation
  row unless a future primary source verifies a weed-evolved TSR accession.
- **External review reconciliation: COMPLETE.** See
  `docs/EXTERNAL_REVIEW_RESPONSE.md` and `docs/DECISION_LOG.md` §24. Adopted
  corrections: ALS interface core, raw-SASA-vs-RSA caveat, and HPPD go/no-go
  TSR audit before any metrics. Do not use engineered HPPD Gly336 as weed TSR.
- **RSA normalization: COMPLETE.** All five current static metric outputs retain
  raw `sasa_A2` and now add `max_sasa_tien2013_A2` plus `rsa_tien2013`, using
  Tien et al. 2013 maximum allowed solvent-accessibility values.
- **Phase 4 starter tables: COMPLETE.** `scripts/build_phase4_tables.py` pools
  the current PPO, ALS, EPSPS, and ACCase mutation rows into
  `output/tables/phase4_master_mutation_table.csv` with joined distance/RSA and
  conservation metrics, and writes HPPD separately to
  `output/tables/phase4_target_family_contrast.csv`.
- **Phase 4 permutation/enrichment analysis: COMPLETE for current targets.**
  `scripts/build_phase4_analysis.py` de-duplicates repeated accession rows to
  unique structural positions and runs the within-family random-residue
  permutation test recommended by the panel review. Current outputs are
  `output/tables/phase4_permutation_summary.csv` and
  `output/tables/phase4_non_core_position_screen.csv`.
- **Review-driven Phase 4 manuscript outputs: COMPLETE.** The later static-vs-
  dynamic critique is reconciled in `docs/REVIEW_RESPONSE_STATIC_VS_DYNAMIC.md`.
  `scripts/build_review_driven_outputs.py` writes mechanism annotations,
  manuscript summary tables, and five SVG figures. `docs/MANUSCRIPT_RESULTS_PHASE4.md`
  contains the first concise Results draft and limitations framing.
- **First manuscript draft: COMPLETE as an internal review draft, since fully
  updated through Phase 6 (below).** `docs/MANUSCRIPT_DRAFT.md` assembles the
  abstract, introduction, methods, results, discussion, limitations, data/code
  availability, figure captions, and submission to-do list around the Phase 4
  tables and figures, citation-formatted for *Pest Management Science* (PMS):
  superscript sequential in-text citations in strict first-appearance order
  (27 references, programmatically verified 1:1), 200-word abstract, author
  block, and required Acknowledgments/Funding/Competing Interests statements.
- **Phase 5 (FAT, DHODH): COMPLETE as an emerging-target audit, not pooled into
  Phase 4.** `docs/PHASE5_FAT_DHODH_AUDIT.md` and
  `data/processed/phase5_target_status.csv` / `phase5_risk_table.csv` document
  primary-source-verified mutation data for both targets, and both are
  explicitly excluded from the main statistical analysis because neither is
  weed-evolved target-site resistance: FAT's R171K/Q/I/M and P192R are
  docking-guided, site-directed *in vitro* mutants (Wagner et al. 2026 bioRxiv,
  not peer-reviewed) with no field TSR observed in *Alopecurus myosuroides*;
  DHODH's G198E/A141T are EMS chemical-mutagenesis lab lines in *Arabidopsis
  thaliana* (Kang et al. 2023 PNAS), not weed-evolved either. DHODH also has no
  public plant DHODH structure (rice structure exists per Kang et al. 2023 but
  is not deposited; only an internal Syngenta/AlphaFold model exists).
- **Phase 6 (biophysical perturbation score + global combined permutation
  test + real mutation expansion): COMPLETE.** Two new, real, primary-source-
  verified weed-evolved mutations were added and integrated through the full
  pipeline (tables, tests, manuscript): EPSPS Thr102Ile (*Eleusine indica*,
  GenBank KM078728, medium confidence) and ALS Asp376Glu (*Sinapis alba*,
  GenBank OP681622/OP681621, high confidence). EPSPS is now n=2 (was n=1) and
  statistically significant (p = 0.0147, no longer just descriptive); ALS is
  now n=5 (was n=4). A candidate third EPSPS mutation, Gly101Ala, was
  investigated and explicitly excluded because primary sources show it only
  as an engineered/transgenic construct, never observed in weed populations
  (see `docs/DECISION_LOG.md` #38 and `docs/VERIFICATION_LOG.md`). Two new
  analyses were added as native-Python substitutes for tools unavailable in
  this environment (no R/lme4, no FoldX/DDGun, no AlphaFold3/ESMFold access):
  a per-mutation **biophysical perturbation score**
  (`scripts/biophysical_perturbation.py` — bulkiness via Zimmerman et al. 1968,
  hydropathy via Kyte-Doolittle 1982, formal charge delta) as a proxy for
  ΔΔG-style tools, and a **global combined permutation test** that pools all
  17 unique accepted positions (and separately the 8 non-core-only positions)
  across all four families into one cohort (p = 0.0001 for both), documented
  everywhere as a pooled-cohort statistic and explicitly *not* a mixed-effects/
  GLMM model. All numbers below reflect this Phase 6 state; the ACCase percent-
  identity figure (53.3%) was independently re-checked against the repo's own
  SWISS-MODEL metadata JSON and corrected from a previously-circulated 55.3%.
- **Companion React site: COMPLETE, deployment pending final GitHub Pages
  verification.** `site/` is a static Vite/React app that reads only from
  JSON exported by `scripts/export_site_data.py` from the same verified CSVs
  the manuscript uses (never hand-typed). Deploys via
  `.github/workflows/deploy-site.yml` to GitHub Pages; the first deploy run
  failed because Pages was not yet enabled in repo settings, since patched
  with `enablement: true` on the `configure-pages` step — confirm in the repo's
  Actions tab that the latest run succeeded, or enable manually under
  Settings -> Pages -> Source -> "GitHub Actions" if it still fails.
- **PMS pre-submission items:** figure format (PDF/EPS vector figures in
  `output/figures_pms/`, not TIFF) and a Zenodo deposit skeleton
  (`.zenodo.json`) are prepared; the actual Zenodo release/DOI and the
  author's ORCID are intentionally left for the user to finalize at
  submission time, not done automatically.
- **Not completed:** final citation/gap sentence-level polish pass, the
  Zenodo release itself (DOI does not exist yet, only the metadata skeleton),
  ORCID (left blank on purpose), and any core-cutoff sensitivity analysis
  (tracked as future work in `docs/HANDOFF_NEXT_STEPS.md`, not implemented).

---

## 2. What each document is for

### Root level
| File | Purpose |
|---|---|
| `README.md` | Setup instructions (Python/R/ChimeraX/MAFFT), repo layout |
| `REPO_INDEX.md` | First navigation map for agents: branch state, commits, scripts, data, outputs, figures, tests, docs, and rules |
| `CONTRIBUTING.md` | One working convention so far: if a paper is paywalled/blocks automated fetch, stop after one try and ask for the PDF directly rather than burning effort on workarounds |
| `requirements.txt` | Python deps: biopython, pandas, numpy, requests, pyKVFinder, pypdf |
| **`PROJECT_STATUS.md`** | This file |

### `docs/` — the planning and decision record
| File | Purpose |
|---|---|
| `panel_review_and_plan.md` | The original 5-reviewer panel critique and phase-by-phase plan this whole project is built from |
| **`DECISION_LOG.md`** | **The most important file if you only read one.** Every directional decision, in order, with reasoning - project selection, methodology fixes, why PPO then ALS were piloted, every data correction, both validation-gate outcomes. Read this to understand *why* the project looks the way it does |
| `VERIFICATION_LOG.md` | The independent fact-checking record - which citations/accessions/claims were verified against primary sources and how |
| `HANDOFF_NEXT_STEPS.md` | Live next-step tracker and ready-to-paste prompt for a new Codex/Claude Code session |
| `EXTERNAL_REVIEW_RESPONSE.md` | Reconciled response to the external/Claude review: ALS interface-core correction, RSA caveat, HPPD reframing |
| `REVIEW_RESPONSE_STATIC_VS_DYNAMIC.md` | Response to the later static-vs-dynamic critique: accepted limitations, already-handled issues, out-of-scope MD requests, and future-work notes |
| `MANUSCRIPT_RESULTS_PHASE4.md` | Draft Phase 4 Results language using the current permutation, mechanism-annotation, and limitation outputs |
| `MANUSCRIPT_DRAFT.md` | First full manuscript scaffold with abstract, methods, results, discussion, limitations, embedded figure links, captions, tables, and submission to-do list |
| `superpowers/specs/2026-07-05-fat-dhodh-phase5-design.md` | Phase 5 FAT/DHODH design gate: FAT-first recommendation, DHODH audit/modeling constraints, and no-Phase-4-integration rule |
| `PHASE5_FAT_DHODH_AUDIT.md` | Completed Phase 5 audit writeup: FAT and DHODH mutation/structure evidence, both explicitly excluded from Phase 4 pooling as non-weed-evolved |
| `CLAUDE_CODE_NEXT_STEPS.md` | An early working prompt from before Phase 1 execution - now superseded by DECISION_LOG, kept for history |
| `PROJECT_HANDOFF_GUIDE.doc` | Standalone onboarding guide (HTML saved as `.doc`) for a new person picking up the project cold; kept in sync with the current Phase 6 state |
| `references/*.pdf` | Primary-source papers living directly in the repo, including PPO, ALS, EPSPS, and ACCase references |

### `data/processed/` — Phase 5 emerging-target audit
| File | Purpose |
|---|---|
| `phase5_target_status.csv` | FAT/DHODH go/no-go status: structure availability, mutation evidence status, and why neither is pooled into Phase 4 |
| `phase5_risk_table.csv` | Full FAT/DHODH mutation-level risk data (engineered/EMS-lab-selected, not weed-evolved) |

### `site/` — companion React app (not part of the analysis pipeline)
| File | Purpose |
|---|---|
| `site/` | Static Vite/React app that visualizes the Phase 4/5 results for a non-technical audience |
| `scripts/export_site_data.py` | Reads `output/tables/*.csv` and `data/processed/phase5_*.csv` and writes the JSON the site reads from - the site never hand-types a number |
| `.github/workflows/deploy-site.yml` | Builds and deploys `site/` to GitHub Pages on push |

### `data/processed/` — the working datasets and results (the "what")
| File | Purpose |
|---|---|
| `PPO_Phase1_Final_Validated_Brief.md` | The fully-verified PPO dataset reference: mutations, numbering keys, mechanism classes |
| `ppo_mutation_candidates.md` | PPO's original sign-off checkpoint doc (historical) |
| `ppo_mutations.csv` | **The working PPO dataset** - 6 mutation rows with accessions, positions, mechanism, confidence, citations |
| `ppo_numbering_key.csv` / `numbering_maps.json` | Tobacco ↔ waterhemp ↔ Palmer amaranth position conversions |
| `ppo_active_site_reference.md` | The Heinemann et al. 2007 4-residue PPO active-site core used as the distance reference |
| `ppo_1sez_distance_sasa.csv` | Per-residue distance/SASA/RSA output for all 465 residues of the PPO structure |
| `ppo_conservation_entropy.csv` | Raw per-residue Shannon-entropy conservation scores (10-species panel) |
| `ppo_validation_gate_results.md` | **The PPO results writeup** - the table, the ΔG210/V361A interpretation, the R98 SASA sanity check |
| `als_mutation_candidates.md` | ALS's sign-off/resolution trail (mirrors PPO's candidates doc) |
| `als_mutations.csv` | **The working ALS dataset** - 5 mutation rows (added Asp376Glu, Phase 6) |
| `als_1z8n_distance_sasa.csv` | Per-residue distance/SASA/RSA for the ALS structure |
| `als_conservation_entropy.csv` | Raw per-residue conservation scores (9-species panel) |
| `als_validation_gate_results.md` | **The ALS results writeup** |
| `epsps_mutation_candidates.md` | EPSPS setup/resolution trail: 8UMJ structure choice, Baerson accession anchor, Chong lower-confidence context |
| `epsps_mutations.csv` | **The working EPSPS mutation seed dataset** - Pro106Ser plus Thr102Ile (added Phase 6) |
| `epsps_8umj_distance_sasa.csv` | Per-residue EPSPS distance/SASA/RSA output for 8UMJ chain A |
| `epsps_conservation_entropy.csv` | Raw per-residue EPSPS conservation scores (8-sequence panel, reference-indexed to 8UMJ/PDB numbering) |
| `epsps_validation_gate_results.md` | **The EPSPS results writeup** |
| `accase_mutation_candidates.md` | ACCase setup/resolution trail: AJ310767 numbering, 1UYS structure, Yu 2007 2088 accessions |
| `accase_mutations.csv` | **The working ACCase mutation seed dataset** - 6 reference-numbered TSR rows |
| `accase_1uys_distance_sasa.csv` | Historical/provenance per-chain-residue ACCase distance/SASA/RSA output for the 1UYS B+C dimer |
| `accase_swissmodel_1uys_distance_sasa.csv` | **Current active ACCase metric file** from the SWISS-MODEL AJ310767 CT-domain homodimer |
| `accase_conservation_entropy.csv` | Raw per-residue ACCase conservation scores (14-sequence plastidic grass panel, reference-indexed to AJ310767) |
| `accase_validation_gate_results.md` | **The ACCase results writeup** |
| `hppd_tsr_audit.md` | HPPD source audit: no accepted weed-evolved target-site mutation; Gly336 excluded |
| `hppd_5ywg_active_site_metrics.csv` | Per-chain-residue HPPD active-site distance/SASA/RSA output for the 5YWG A+B mesotrione-bound dimer |
| `hppd_active_site_contrast_results.md` | **The HPPD contrast-case writeup** |
| `*_conservation_set.fasta` / `*_conservation_aligned.fasta` | The raw and MAFFT-aligned multi-species sequence sets behind each conservation score |

### `data/raw/` — everything pulled from external sources, unmodified
Sequences (FASTA) and structures (PDB) pulled from NCBI/RCSB, named by accession
and what they represent (species, mutation, wild-type-vs-resistant). Nothing in
here has been edited - if you need to re-derive anything, start here.

### `scripts/` — the actual pipeline code
| File | Purpose |
|---|---|
| `chimerax_distance_sasa.py` | PPO: percentile-rank distance-to-active-site + SASA on 1SEZ |
| `chimerax_als_distance_sasa.py` | ALS: same, on local 1Z8N, with interface-aware structure-derived active-site core |
| `epsps_distance_sasa.py` | EPSPS: standardized distance/SASA on 8UMJ using ligand-contact active-site core and local SASA fallback |
| `epsps_conservation_entropy.py` | EPSPS: reference-indexed Shannon entropy from the 8-sequence EPSPS panel |
| `chimerax_accase_distance_sasa.py` | ACCase: standardized distance/SASA on the 1UYS B+C haloxyfop-bound dimer using ChimeraX SASA |
| `accase_distance_sasa.py` | ACCase: local fallback/reference implementation for 1UYS distance/SASA |
| `accase_conservation_entropy.py` | ACCase: reference-indexed Shannon entropy from the 14-sequence plastidic grass ACCase panel |
| `hppd_distance_sasa.py` | HPPD: standardized active-site distance/SASA on the 5YWG A+B mesotrione-bound dimer |
| `rsa.py` | Adds Tien et al. 2013 max-SASA and RSA columns to the current static metric CSV outputs while preserving raw SASA |
| `build_phase4_tables.py` | Phase 4 table builder: joins mutation rows to family-specific distance/RSA and conservation metrics, while keeping HPPD separate as a contrast family |
| `build_phase4_analysis.py` | Phase 4 permutation/enrichment analysis: samples same-size random residue sets within each enzyme and screens unique mutation positions by proximity class |
| `build_review_driven_outputs.py` | Builds review-driven mechanism annotations, manuscript-ready summary tables, and SVG figures from the Phase 4 outputs |
| `biophysical_perturbation.py` | Static, pure-Python per-mutation biophysical perturbation score (bulkiness/hydropathy/charge deltas) - substitutes for unavailable FoldX/DDGun ΔΔG tools |
| `export_site_data.py` | Exports the same verified `output/tables/*.csv` and `data/processed/phase5_*.csv` data to JSON for the companion React site in `site/` |
| `reference_conservation.py` | Shared helper for pairwise reference-indexed conservation when MAFFT is unavailable |
| `pdb_static_metrics.py` | Lightweight PDB parser/contact/SASA helpers used when ChimeraX is unavailable |
| `active_site_metrics.py` | Shared helper for standardized distance-to-core and nearest-other-core metrics |
| `chimerax_sasa_diagnostic.py` / `chimerax_probe_check.py` | One-off sanity checks (R98 SASA verification) - reference, not part of the main pipeline |
| `conservation_entropy.py` | PPO: Shannon entropy from the 10-species alignment |
| `als_conservation_entropy.py` | ALS: same, 9-species alignment |

### `output/`
`tables/phase4_master_mutation_table.csv` is the current Phase 4 pooled mutation
table (19 mutation rows: PPO 6, ALS 5, EPSPS 2, ACCase 6, after the Phase 6
Asp376Glu and Thr102Ile additions), with `bulkiness_delta`/`hydropathy_delta`/
`charge_delta` biophysical perturbation columns joined alongside distance/SASA/RSA
and conservation metrics. HPPD is kept out of that mutation table and is
represented in `tables/phase4_target_family_contrast.csv` as a no-verified-weed-TSR
contrast family. `tables/phase4_permutation_summary.csv` reports both the
within-family permutation/enrichment results for unique structural mutation
positions (four families) and, since Phase 6, two additional
`ALL_FAMILIES_COMBINED` rows for the global combined permutation test (pooling
all 17 unique accepted positions, and separately the 8 non-core-only positions,
across every family). `tables/phase4_non_core_position_screen.csv` is the
de-duplicated screen for direct core, adjacent non-core, and more distal non-core
candidate positions. `tables/phase4_mechanism_annotations.csv` and
`tables/manuscript_table_*` are the review-driven manuscript tables, now including
mechanism annotations for Thr102Ile and Asp376Glu. `figures/` contains five SVG
figure drafts (workflow, permutation enrichment, position screen, distance/RSA/
conservation scatter, and the resistance-zone map), and `figures_pms/` contains the
PMS-submission vector (PDF/EPS) versions of those same figures.

---

## 3. What to do next (manually, step by step)

Per `DECISION_LOG.md` §25, HPPD is now complete as a structural negative/contrast
case. Do not run HPPD as a TSR-positive validation gate unless a future
peer-reviewed source verifies a weed-evolved target-site HPPD amino-acid
substitution with accession-level support.

RSA normalization is now complete. Raw SASA remains useful for traceability, but
Phase 4 should use `rsa_tien2013` as the cross-enzyme exposure covariate.

**Phase 4** now has pooled/contrast tables, the recommended permutation/enrichment
test, review-driven mechanism annotations, five manuscript figure drafts, a concise
Results draft, a PMS-citation-formatted full manuscript in
`docs/MANUSCRIPT_DRAFT.md`, a per-mutation biophysical perturbation score, and a
global combined permutation test (see Phase 6 above). Current statistical signal:
PPO, ALS, ACCase, and now EPSPS are all significantly enriched for low
distance-to-core percentile positions - EPSPS remains the smallest family and
should still be interpreted with that caveat, but it is no longer a single-point
descriptive case. Current within-family all-position p-values (from
`output/tables/phase4_permutation_summary.csv`) are ACCase 0.0003, ALS 0.0001,
EPSPS 0.0147, and PPO 0.0004; the global combined test across all 17 unique
accepted positions (and separately the 8 non-core-only positions) gives p = 0.0001
for both. Remaining pre-submission work: a final sentence-level citation/gap
polish pass, and the actual Zenodo release/DOI (metadata skeleton only exists so
far in `.zenodo.json`). See `docs/HANDOFF_NEXT_STEPS.md` for the live, itemized
tracker - it supersedes the step list in this section for anything not covered
above.

**Phase 5 (FAT, DHODH)** is complete as an emerging-target audit and is
deliberately *not* pooled into Phase 4: both targets' known mutations are
engineered/lab-selected rather than weed-evolved (see Phase 5 bullet above and
`docs/PHASE5_FAT_DHODH_AUDIT.md`). No further action is planned unless a future
peer-reviewed source reports a weed-evolved target-site mutation for either
target, or DHODH's structure becomes publicly deposited.

**Companion site (`site/`)** is built and wired to deploy via GitHub Actions to
GitHub Pages; confirm the latest Actions run under the repo's Actions tab
succeeded (see Phase 6 note above for the fix applied after the first failed
run).
