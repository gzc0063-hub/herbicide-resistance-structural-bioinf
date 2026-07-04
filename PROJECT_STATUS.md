# Project status — read this first

Snapshot of what's done, what every file is for, and what to do next. Treat this
file plus `docs/DECISION_LOG.md` as the handoff state for the current workspace;
check `git status` before assuming every listed change has been committed and
pushed to https://github.com/gzc0063-hub/herbicide-resistance-structural-bioinf
(private repo).

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
- **Phase 2, ALS/AHAS pilot: COMPLETE, validation gate PASSED.** Two mutations
  (Trp574Leu, Ser653Asn) sourced from Larran et al. 2017 and run through the same
  pipeline. External review correctly flagged that the AHAS pocket includes
  dimer-interface residues; fixed core size is now 27 residues, including Ala122
  and Pro197 as interface-pocket residues. The pilot result is unchanged: Trp574
  and Ser653 are direct herbicide-contact residues, fully conserved across 9
  species.
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
  were verified from Delye et al. 2005 / Yu et al. 2007, mapped from AJ310767
  black-grass numbering to the 1UYS yeast ACCase B+C haloxyfop-bound dimer, and
  run through distance/SASA/conservation.
- **Phase 2, HPPD: COMPLETE as structural contrast case, not TSR-positive.**
  Source audit found no accepted weed-evolved HPPD target-site amino-acid
  substitution. HPPD is retained using plant templates 5YWG/1TG5 and a
  metal/inhibitor-contact active-site core. Do not create or pool an HPPD mutation
  row unless a future primary source verifies a weed-evolved TSR accession.
- **External review reconciliation: COMPLETE.** See
  `docs/EXTERNAL_REVIEW_RESPONSE.md` and `docs/DECISION_LOG.md` §24. Adopted
  corrections: ALS interface core, raw-SASA-vs-RSA caveat, and HPPD go/no-go
  TSR audit before any metrics. Do not use engineered HPPD Gly336 as weed TSR.
- **Not completed:** RSA; Phase 3 (FAT,
  DHODH - needs ColabFold), Phase 4 (cross-enzyme synthesis), Phase 5
  (deposit/submit).

---

## 2. What each document is for

### Root level
| File | Purpose |
|---|---|
| `README.md` | Setup instructions (Python/R/ChimeraX/MAFFT), repo layout |
| `CONTRIBUTING.md` | One working convention so far: if a paper is paywalled/blocks automated fetch, stop after one try and ask for the PDF directly rather than burning effort on workarounds |
| `requirements.txt` | Python deps: biopython, pandas, numpy, requests, pyKVFinder, pypdf |
| **`PROJECT_STATUS.md`** | This file |

### `docs/` — the planning and decision record
| File | Purpose |
|---|---|
| `panel_review_and_plan.md` | The original 5-reviewer panel critique and phase-by-phase plan this whole project is built from |
| **`DECISION_LOG.md`** | **The most important file if you only read one.** Every directional decision, in order, with reasoning - project selection, methodology fixes, why PPO then ALS were piloted, every data correction, both validation-gate outcomes. Read this to understand *why* the project looks the way it does |
| `VERIFICATION_LOG.md` | The independent fact-checking record - which citations/accessions/claims were verified against primary sources and how |
| `EXTERNAL_REVIEW_RESPONSE.md` | Reconciled response to the external/Claude review: ALS interface-core correction, RSA caveat, HPPD reframing |
| `CLAUDE_CODE_NEXT_STEPS.md` | An early working prompt from before Phase 1 execution - now superseded by DECISION_LOG, kept for history |
| `references/*.pdf` | Primary-source papers living directly in the repo, including PPO, ALS, EPSPS, and ACCase references |

### `data/processed/` — the working datasets and results (the "what")
| File | Purpose |
|---|---|
| `PPO_Phase1_Final_Validated_Brief.md` | The fully-verified PPO dataset reference: mutations, numbering keys, mechanism classes |
| `ppo_mutation_candidates.md` | PPO's original sign-off checkpoint doc (historical) |
| `ppo_mutations.csv` | **The working PPO dataset** - 6 mutation rows with accessions, positions, mechanism, confidence, citations |
| `ppo_numbering_key.csv` / `numbering_maps.json` | Tobacco ↔ waterhemp ↔ Palmer amaranth position conversions |
| `ppo_active_site_reference.md` | The Heinemann et al. 2007 4-residue PPO active-site core used as the distance reference |
| `ppo_1sez_distance_sasa.csv` | Raw per-residue distance/SASA output for all 465 residues of the PPO structure |
| `ppo_conservation_entropy.csv` | Raw per-residue Shannon-entropy conservation scores (10-species panel) |
| `ppo_validation_gate_results.md` | **The PPO results writeup** - the table, the ΔG210/V361A interpretation, the R98 SASA sanity check |
| `als_mutation_candidates.md` | ALS's sign-off/resolution trail (mirrors PPO's candidates doc) |
| `als_mutations.csv` | **The working ALS dataset** - 2 mutation rows |
| `als_1z8n_distance_sasa.csv` | Raw per-residue distance/SASA for the ALS structure |
| `als_conservation_entropy.csv` | Raw per-residue conservation scores (9-species panel) |
| `als_validation_gate_results.md` | **The ALS results writeup** |
| `epsps_mutation_candidates.md` | EPSPS setup/resolution trail: 8UMJ structure choice, Baerson accession anchor, Chong lower-confidence context |
| `epsps_mutations.csv` | **The working EPSPS mutation seed dataset** - currently Pro106Ser |
| `epsps_8umj_distance_sasa.csv` | Raw per-residue EPSPS distance/SASA output for 8UMJ chain A |
| `epsps_conservation_entropy.csv` | Raw per-residue EPSPS conservation scores (8-sequence panel, reference-indexed to 8UMJ/PDB numbering) |
| `epsps_validation_gate_results.md` | **The EPSPS results writeup** |
| `accase_mutation_candidates.md` | ACCase setup/resolution trail: AJ310767 numbering, 1UYS structure, Yu 2007 2088 accessions |
| `accase_mutations.csv` | **The working ACCase mutation seed dataset** - 6 reference-numbered TSR rows |
| `accase_1uys_distance_sasa.csv` | Raw per-chain-residue ACCase distance/SASA output for the 1UYS B+C dimer |
| `accase_conservation_entropy.csv` | Raw per-residue ACCase conservation scores (14-sequence plastidic grass panel, reference-indexed to AJ310767) |
| `accase_validation_gate_results.md` | **The ACCase results writeup** |
| `hppd_tsr_audit.md` | HPPD source audit: no accepted weed-evolved target-site mutation; Gly336 excluded |
| `hppd_5ywg_active_site_metrics.csv` | Raw per-chain-residue HPPD active-site distance/SASA output for the 5YWG A+B mesotrione-bound dimer |
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
| `reference_conservation.py` | Shared helper for pairwise reference-indexed conservation when MAFFT is unavailable |
| `pdb_static_metrics.py` | Lightweight PDB parser/contact/SASA helpers used when ChimeraX is unavailable |
| `active_site_metrics.py` | Shared helper for standardized distance-to-core and nearest-other-core metrics |
| `chimerax_sasa_diagnostic.py` / `chimerax_probe_check.py` | One-off sanity checks (R98 SASA verification) - reference, not part of the main pipeline |
| `conservation_entropy.py` | PPO: Shannon entropy from the 10-species alignment |
| `als_conservation_entropy.py` | ALS: same, 9-species alignment |

### `output/`
Empty placeholders (`figures/`, `tables/`) - reserved for Phase 4 synthesis figures,
nothing generated yet.

---

## 3. What to do next (manually, step by step)

Per `DECISION_LOG.md` §25, HPPD is now complete as a structural negative/contrast
case. Do not run HPPD as a TSR-positive validation gate unless a future
peer-reviewed source verifies a weed-evolved target-site HPPD amino-acid
substitution with accession-level support.

Before Phase 4 pooling, add residue-normalized RSA alongside the existing raw SASA
columns. Raw SASA remains useful for traceability, but RSA is the correct
cross-enzyme exposure covariate.

After RSA addition, **Phase 4** is the cross-enzyme synthesis: pool
`ppo_mutations.csv` + `als_mutations.csv` + `epsps_mutations.csv` +
`accase_mutations.csv` into one mutation table, and keep HPPD as a separate
target-family contrast status/active-site descriptor table. Then run
the permutation/enrichment test the panel review recommended (see
`docs/panel_review_and_plan.md` §Part A, biostatistician reviewer) instead of a
naive logistic regression, and explicitly look for more outlier mutations like
ΔG210 across the full set.

**Phase 3 (FAT, DHODH)** is the one phase that needs something beyond what's set
up so far - these two targets don't have existing crystal structures, so they need
a ColabFold structure prediction run by hand in Google Colab (free tier), per the
original plan in `docs/panel_review_and_plan.md` Part B/D. Everything else in the
pipeline resumes normally once you have a predicted PDB file in hand.
