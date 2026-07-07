# Cross-Site-of-Action Comparative Structural Bioinformatics

Structural comparison of herbicide-resistance mutations across independently-evolved
sites of action (PPO, ALS/AHAS, ACCase, EPSPS, HPPD, FAT, DHODH), testing whether
resistance mutations cluster in a statistically distinguishable structural zone
relative to the active site.

**Start with [REPO_INDEX.md](REPO_INDEX.md)** for a practical map of the repo,
branches, code, data, figures, outputs, and next-step files. Then read
[PROJECT_STATUS.md](PROJECT_STATUS.md) for what's done, what every
file is for, and exactly what to do next. See
[docs/panel_review_and_plan.md](docs/panel_review_and_plan.md) for the original
panel review and phase-by-phase plan, [docs/DECISION_LOG.md](docs/DECISION_LOG.md)
for the full reasoning trail, [docs/SENIOR_REVIEW_2026-07-05.md](docs/SENIOR_REVIEW_2026-07-05.md)
for the latest referee-style review, and [docs/HANDOFF_NEXT_STEPS.md](docs/HANDOFF_NEXT_STEPS.md)
for the live task tracker (what was just done / what to do next).

## Reproduce the analysis outputs

After `pip install -r requirements.txt`, regenerate every pooled table, manuscript
table, and figure and run the tests with a single command:

```bash
python scripts/rebuild_all.py
```

This regenerates everything downstream of the per-family structural metric CSVs
(which need ChimeraX or the pure-Python fallback and change only when a structure or
active-site core changes). Regeneration is deterministic.

## Repo layout

- `data/raw/` — sequences, structures, and mutation lists as pulled from source (NCBI, UniProt, PDB, literature)
- `data/processed/` — cleaned/aligned/numbered data ready for analysis
- `scripts/` — Python (ChimeraX scripting, conservation, per-family and global-combined permutation tests, biophysical perturbation score). A cross-family generalized linear mixed-effects model (R/`lme4`) was considered but not implemented — no R installation was available in this project's environment; the global combined permutation test in `scripts/build_phase4_analysis.py` is the pure-Python cross-family statistic used instead (see `docs/DECISION_LOG.md`).
- `output/figures/`, `output/tables/` — generated results
- `docs/` — planning and methods notes

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

R with `lme4`/`ggplot2` is not required to reproduce any output in this repo. An R-based
mixed-effects model was an early design idea (see `docs/panel_review_and_plan.md`) but was
not implemented — no R installation was available, so the cross-family statistic actually
used is the pure-Python global combined permutation test in `scripts/build_phase4_analysis.py`.

ChimeraX must be installed separately: https://www.cgl.ucsf.edu/chimerax/download.html

MAFFT (multiple sequence alignment, used for the conservation-entropy metric) must
also be installed separately - no pip package, and no Windows binary is bundled in
this repo. Download the native Windows build (no Cygwin needed) from
https://mafft.cbrc.jp/alignment/software/windows_without_cygwin.html, unzip it
anywhere, and point scripts at `<unzip-dir>/mafft-win/mafft.bat`.

## Pipeline phases

0. Setup — repo scaffold, environment checks
1. Pilot enzyme: PPO (validate against Dayan et al. 2018)
2. Established targets: ALS/AHAS, ACCase, EPSPS, HPPD
3. New targets requiring ColabFold: FAT, DHODH
4. Cross-SOA synthesis and permutation analysis
5. Deposit (GitHub + Zenodo) and manuscript submission
