# Repository Index and Navigation Guide

This file is the practical map for moving around this repository. Use it when you
want to know where the data, code, figures, manuscript drafts, decisions, tests,
and current branches live.

## Start Here

Read these files in this order when opening the project fresh:

1. `REPO_INDEX.md`
   This navigation guide.
2. `docs/HANDOFF_NEXT_STEPS.md`
   Live work tracker: what was just completed and what is next.
3. `docs/DECISION_LOG.md`
   Why the project made each methodological decision.
4. `docs/VERIFICATION_LOG.md`
   What was checked against primary sources, structures, accessions, and outputs.
5. `docs/MANUSCRIPT_DRAFT.md`
   Current manuscript scaffold.
6. `README.md`
   Setup and one-command reproduction instructions.

`PROJECT_STATUS.md` is useful historical orientation, but some details lag behind
the latest commits. Prefer `docs/HANDOFF_NEXT_STEPS.md` plus
`docs/DECISION_LOG.md` for the freshest project state.

## Current Branches

Local and remote branch state at the time this index was written:

| Branch | Status | Notes |
|---|---|---|
| `master` | active local branch | Main working branch. |
| `origin/master` | remote tracking branch | GitHub remote branch. |
| `origin/HEAD` | points to `origin/master` | Default remote branch. |

Recent commits that define the current project state:

| Commit | Meaning |
|---|---|
| `a4100f2` | Added this repository navigation index and linked it from README. |
| `b92f5b0` | Designed Phase 5 FAT/DHODH validation gate. |
| `1c6f711` | Switched ACCase to SWISS-MODEL weed CT-domain dimer metrics. |
| `84e9cb3` | Prepared ACCase CT-domain sequence for homology modeling. |
| `ff4e2cc` | Added dynamic/docking benchmark manuscript polish. |
| `ebeadcf` | Verified and archived Nakka et al. 2017 HPPD citation. |

Useful commands:

```bash
git status --short --branch
git branch -a -vv
git log --oneline --decorate --max-count=12
```

## Repo Layout

| Path | What It Contains | How To Use It |
|---|---|---|
| `README.md` | Setup, dependencies, reproduction command. | Start here for environment setup. |
| `PROJECT_STATUS.md` | Broad historical status snapshot. | Good overview, but check handoff for latest changes. |
| `REPO_INDEX.md` | This navigation guide. | Use as the map. |
| `CONTRIBUTING.md` | Working convention for blocked papers/PDFs. | Read before source-audit work. |
| `requirements.txt` | Python dependencies. | Install before running scripts. |
| `CITATION.cff` | Citation metadata. | Use when preparing release/Zenodo. |
| `LICENSE` | MIT license. | Code licensing. |
| `data/raw/` | Raw source files: PDB, FASTA, downloaded model metadata, source tables. | Do not edit by hand; use as provenance. |
| `data/processed/` | Cleaned mutation tables, metric CSVs, conservation outputs, validation notes. | Main analysis inputs and intermediate outputs. |
| `scripts/` | Pipeline scripts. | Regenerate metrics, tables, analyses, figures. |
| `tests/` | Unit/integration tests. | Verify mapping, outputs, RSA, scripts. |
| `output/tables/` | Generated manuscript and Phase 4 tables. | Read for final numeric results. |
| `output/figures/` | Generated SVG figures. | Manuscript figure drafts. |
| `docs/` | Decisions, handoff, reviews, manuscript, references, specs. | Project memory and writing layer. |
| `docs/references/` | Archived source PDFs. | Primary-source evidence library. |
| `docs/superpowers/specs/` | Design specs for new work. | Phase 5 FAT/DHODH design lives here. |

## Core Workflow

### Rebuild Manuscript Tables And Figures

Use the one-command chain when the per-family metric CSVs already exist:

```bash
python scripts/rebuild_all.py
```

This runs:

1. `scripts/build_phase4_tables.py`
2. `scripts/build_phase4_analysis.py`
3. `scripts/build_review_driven_outputs.py`
4. `scripts/build_resistance_zone_figure.py`
5. `python -m pytest -q`

It does not recompute per-family metric CSVs such as `ppo_1sez_distance_sasa.csv`
or `accase_swissmodel_1uys_distance_sasa.csv`. Those only need rerunning when a
structure, model, active-site core, or family-specific metric method changes.

### Run Tests

Preferred:

```bash
python -m pytest -q
```

Fallback when pytest is unavailable:

```bash
python -m unittest discover -s tests -v
```

### Check Before Commit

```bash
git diff --check
git status --short --branch
git diff --stat
```

## Data Files

### Raw Data

`data/raw/` holds unmodified downloaded or source-derived files.

Main structure/model files:

| File | Meaning |
|---|---|
| `1SEZ.pdb`, `1SEZ.fasta` | PPO structure/reference sequence. |
| `1Z8N.pdb`, `1Z8N.fasta` | ALS/AHAS herbicide-bound structure. |
| `8UMJ.pdb`, `8UMJ.fasta` | Maize EPSPS with glyphosate/S3P. |
| `1UYS.pdb`, `1UYS.fasta` | Yeast ACCase CT-domain haloxyfop-bound dimer, provenance/core source. |
| `ACCase_Alopecurus_AJ310767_CTdomain_SWISSMODEL_1UYS_homomer.pdb` | Current ACCase weed-sequence homology model used for active Phase 4 metrics. |
| `ACCase_Alopecurus_AJ310767_CTdomain_SWISSMODEL_1UYS_homomer.json` | SWISS-MODEL metadata. |
| `5YWG.pdb`, `5YWG.fasta` | HPPD contrast structure. |
| `1TG5.pdb`, `1TG5.fasta` | HPPD related structure/reference. |

Mutation/source FASTA files are named by target, species, accession, and often
wild-type/resistant state. Example groups:

| Group | Examples |
|---|---|
| PPO2 source sequences | `PPO2_Apalmeri_*`, `PPO2_Atuberculatus_*` |
| ALS source sequences | `ALS_Apalmeri_*`, `ALS_conservation_*` |
| ACCase source sequences | `ACCase_Alopecurus_*`, `ACCase_Lrigidum_*`, `ACCase_conservation_*` |
| EPSPS source sequences | `EPSPS_Eindica_*`, `EPSPS_conservation_*` |

### Processed Data

Mutation tables:

| File | Meaning |
|---|---|
| `data/processed/ppo_mutations.csv` | PPO accepted mutation rows. |
| `data/processed/als_mutations.csv` | ALS/AHAS accepted mutation rows. |
| `data/processed/epsps_mutations.csv` | EPSPS accepted mutation rows. |
| `data/processed/accase_mutations.csv` | ACCase accepted mutation rows. |

Distance/SASA/RSA metric tables:

| File | Meaning |
|---|---|
| `data/processed/ppo_1sez_distance_sasa.csv` | PPO per-residue static metrics. |
| `data/processed/als_1z8n_distance_sasa.csv` | ALS/AHAS per-residue static metrics. |
| `data/processed/epsps_8umj_distance_sasa.csv` | EPSPS per-residue static metrics. |
| `data/processed/accase_swissmodel_1uys_distance_sasa.csv` | Current ACCase weed-model per-residue static metrics. |
| `data/processed/accase_1uys_distance_sasa.csv` | Older 1UYS ACCase provenance metric table. |
| `data/processed/hppd_5ywg_active_site_metrics.csv` | HPPD contrast active-site metrics. |

Conservation tables:

| File | Meaning |
|---|---|
| `data/processed/ppo_conservation_entropy.csv` | PPO conservation scores. |
| `data/processed/als_conservation_entropy.csv` | ALS/AHAS conservation scores. |
| `data/processed/epsps_conservation_entropy.csv` | EPSPS conservation scores. |
| `data/processed/accase_conservation_entropy.csv` | ACCase conservation scores. |

Validation notes:

| File | Meaning |
|---|---|
| `data/processed/ppo_validation_gate_results.md` | PPO validation outcome. |
| `data/processed/als_validation_gate_results.md` | ALS/AHAS validation outcome. |
| `data/processed/epsps_validation_gate_results.md` | EPSPS validation outcome. |
| `data/processed/accase_validation_gate_results.md` | ACCase validation outcome. |
| `data/processed/hppd_tsr_audit.md` | HPPD no-verified-weed-TSR audit. |
| `data/processed/hppd_active_site_contrast_results.md` | HPPD contrast writeup. |

## Code Index

### Shared Helpers

| Script | Purpose |
|---|---|
| `scripts/active_site_metrics.py` | Shared distance-to-core and nearest-other-core helpers. |
| `scripts/pdb_static_metrics.py` | Lightweight PDB parser, contact detection, local SASA helper. |
| `scripts/rsa.py` | Adds Tien-normalized RSA columns while preserving raw SASA. |
| `scripts/reference_conservation.py` | Shared reference-indexed conservation helper. |

### Per-Family Metric Scripts

| Script | Family | Purpose |
|---|---|---|
| `scripts/chimerax_distance_sasa.py` | PPO | ChimeraX PPO distance/SASA on 1SEZ. |
| `scripts/conservation_entropy.py` | PPO | PPO conservation entropy. |
| `scripts/chimerax_als_distance_sasa.py` | ALS/AHAS | ChimeraX ALS distance/SASA on 1Z8N with interface-aware core. |
| `scripts/als_conservation_entropy.py` | ALS/AHAS | ALS conservation entropy. |
| `scripts/epsps_distance_sasa.py` | EPSPS | EPSPS distance/SASA on 8UMJ with ligand-contact core. |
| `scripts/epsps_conservation_entropy.py` | EPSPS | EPSPS conservation entropy. |
| `scripts/chimerax_accase_distance_sasa.py` | ACCase | Older ChimeraX 1UYS ACCase metric path. |
| `scripts/accase_distance_sasa.py` | ACCase | Local 1UYS fallback/reference path. |
| `scripts/accase_swissmodel_distance_sasa.py` | ACCase | Current SWISS-MODEL weed CT-domain metric path. |
| `scripts/accase_conservation_entropy.py` | ACCase | ACCase conservation entropy. |
| `scripts/hppd_distance_sasa.py` | HPPD | HPPD contrast active-site metric script. |

### Phase 4 Builders

| Script | Output |
|---|---|
| `scripts/build_phase4_tables.py` | `phase4_master_mutation_table.csv`, `phase4_target_family_contrast.csv` |
| `scripts/build_phase4_analysis.py` | `phase4_permutation_summary.csv`, `phase4_non_core_position_screen.csv` |
| `scripts/build_review_driven_outputs.py` | mechanism annotations, manuscript tables, figures 1-4 |
| `scripts/build_resistance_zone_figure.py` | figure 5 schematic SVG |
| `scripts/rebuild_all.py` | Runs the full downstream regeneration chain and tests. |

### Diagnostic Or Optional Scripts

| Script | Purpose |
|---|---|
| `scripts/chimerax_sasa_diagnostic.py` | One-off SASA sanity diagnostics. |
| `scripts/chimerax_probe_check.py` | One-off probe/check helper. |
| `scripts/chimerax_resistance_zone_figures.py` | Optional 3D structure-rendered figure path, needs ChimeraX GUI/OpenGL. |
| `scripts/build_epsps_raw_sources.py` | EPSPS source-build helper. |

## Output Tables

| File | Meaning |
|---|---|
| `output/tables/phase4_master_mutation_table.csv` | Main joined mutation table for PPO, ALS/AHAS, EPSPS, ACCase. |
| `output/tables/phase4_target_family_contrast.csv` | HPPD contrast status, kept out of mutation pooling. |
| `output/tables/phase4_permutation_summary.csv` | Family-level enrichment/randomization results. |
| `output/tables/phase4_non_core_position_screen.csv` | Unique structural-position proximity screen. |
| `output/tables/phase4_mechanism_annotations.csv` | Controlled mechanism labels for manuscript interpretation. |
| `output/tables/manuscript_table_1_family_permutation_summary.csv` | Manuscript Table 1 source. |
| `output/tables/manuscript_table_2_unique_position_mechanisms.csv` | Manuscript Table 2 source. |
| `output/tables/manuscript_table_3_hppd_contrast_status.csv` | Manuscript Table 3 source. |

## Output Figures

| File | Meaning |
|---|---|
| `output/figures/figure_1_workflow.svg` | Workflow schematic. |
| `output/figures/figure_2_permutation_enrichment.svg` | Observed vs random enrichment figure. |
| `output/figures/figure_3_position_screen.svg` | Unique mutation position screen. |
| `output/figures/figure_4_distance_rsa_conservation.svg` | Distance/RSA/conservation scatter. |
| `output/figures/figure_5_resistance_zone_map.svg` | Resistance-zone schematic map. |

## Documentation Index

| File | Meaning |
|---|---|
| `docs/HANDOFF_NEXT_STEPS.md` | Live next-step tracker. Update this after meaningful work. |
| `docs/DECISION_LOG.md` | Chronological reasoning record. Add new decisions here. |
| `docs/VERIFICATION_LOG.md` | Evidence and verification record. Add audits/checks here. |
| `docs/MANUSCRIPT_DRAFT.md` | Current manuscript draft. |
| `docs/MANUSCRIPT_RESULTS_PHASE4.md` | Concise Phase 4 results draft. |
| `docs/EXTERNAL_REVIEW_RESPONSE.md` | Response to external review issues. |
| `docs/REVIEW_RESPONSE_STATIC_VS_DYNAMIC.md` | Static-vs-dynamic critique response. |
| `docs/SENIOR_REVIEW_2026-07-05.md` | Senior review artifact. |
| `docs/panel_review_and_plan.md` | Original panel review and long-term plan. |
| `docs/CLAUDE_CODE_NEXT_STEPS.md` | Older handoff prompt, mostly superseded. |
| `docs/superpowers/specs/2026-07-05-fat-dhodh-phase5-design.md` | Phase 5 FAT/DHODH validation-gate design. |

## Tests

| Test File | What It Checks |
|---|---|
| `tests/test_active_site_metrics.py` | Distance-to-core and nearest-other-core behavior. |
| `tests/test_pdb_static_metrics.py` | PDB parsing/contact/SASA helper behavior. |
| `tests/test_rsa.py` | RSA/max-SASA calculations. |
| `tests/test_reference_conservation.py` | Reference-indexed conservation helpers. |
| `tests/test_als_outputs.py` | ALS interface-aware active-site output. |
| `tests/test_accase_outputs.py` | Original ACCase 1UYS metric invariants. |
| `tests/test_accase_swissmodel_outputs.py` | Current ACCase SWISS-MODEL metric invariants. |
| `tests/test_epsps_conservation_outputs.py` | EPSPS conservation/mapping invariants. |
| `tests/test_hppd_outputs.py` | HPPD contrast active-site metrics. |
| `tests/test_phase4_tables.py` | Phase 4 table builder outputs and joined fields. |
| `tests/test_phase4_analysis.py` | Phase 4 permutation and non-core screen outputs. |
| `tests/test_review_driven_outputs.py` | Mechanism annotations and manuscript outputs. |

## Target-Family Status

| Family | Status | Current Role |
|---|---|---|
| PPO | Complete validation gate. | Main pooled Phase 4 family. |
| ALS/AHAS | Complete validation gate, expanded to four accepted positions. | Main pooled Phase 4 family. |
| EPSPS | Complete validation gate with one accepted position. | Pooled Phase 4 family, underpowered as standalone family-level test. |
| ACCase | Complete validation gate; current metrics use SWISS-MODEL weed CT-domain dimer. | Main pooled Phase 4 family. |
| HPPD | Complete as contrast case; no accepted weed-evolved TSR row. | Separate contrast/status table. |
| FAT | Phase 5 design exists; structure route looks promising. | Emerging-target validation gate, not yet pooled. |
| DHODH | Phase 5 design exists; no public plant DHODH RCSB structure confirmed. | Emerging-target validation/modeling gate, not yet pooled. |

## Rules For Future Work

1. Do not add a mutation row without primary-source support.
2. Do not describe engineered or lab-selected mutations as weed-evolved TSR.
3. Do not hand-edit generated tables or figures; change scripts or source data, then regenerate.
4. Keep HPPD out of the pooled mutation table unless a future verified weed TSR source appears.
5. Treat old ACCase `1UYS` metric files as provenance; active ACCase Phase 4 metrics use the SWISS-MODEL weed dimer.
6. Update `docs/HANDOFF_NEXT_STEPS.md`, `docs/DECISION_LOG.md`, and `docs/VERIFICATION_LOG.md` when decisions or evidence change.
7. Before claiming completion, run verification and record the command output in the final summary.

## Common Questions

### Where are the manuscript numbers?

Start with:

- `output/tables/manuscript_table_1_family_permutation_summary.csv`
- `output/tables/manuscript_table_2_unique_position_mechanisms.csv`
- `output/tables/manuscript_table_3_hppd_contrast_status.csv`
- `docs/MANUSCRIPT_DRAFT.md`

### Where are the figures?

Use `output/figures/figure_*.svg`.

### Where do I change a result?

Usually not in `output/`. Change the relevant source CSV, metric script, or
builder script, then run `python scripts/rebuild_all.py`.

### Where do I add a new family?

Start with a design/audit note in `docs/superpowers/specs/` or `docs/`, then add:

1. raw structure/sequence files in `data/raw/`;
2. mutation table in `data/processed/`;
3. distance/SASA/RSA metric CSV;
4. conservation CSV;
5. family config in `scripts/build_phase4_tables.py` only after it passes the evidence gate;
6. tests for the new family.

### What should I read before working on FAT/DHODH?

Read:

- `docs/superpowers/specs/2026-07-05-fat-dhodh-phase5-design.md`
- `docs/HANDOFF_NEXT_STEPS.md`
- `docs/DECISION_LOG.md`

FAT has plant inhibitor-complex structures available. DHODH has strong
tetflupyrolimet target biology but still needs a verified plant structure/model
route and mutation evidence before pipeline integration.
