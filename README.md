# Cross-Site-of-Action Comparative Structural Bioinformatics

Structural comparison of herbicide-resistance mutations across independently-evolved
sites of action (PPO, ALS/AHAS, ACCase, EPSPS, HPPD, FAT, DHODH), testing whether
resistance mutations cluster in a statistically distinguishable structural zone
relative to the active site.

**Start with [PROJECT_STATUS.md](PROJECT_STATUS.md)** for what's done, what every
file is for, and exactly what to do next. See
[docs/panel_review_and_plan.md](docs/panel_review_and_plan.md) for the original
panel review and phase-by-phase plan, and [docs/DECISION_LOG.md](docs/DECISION_LOG.md)
for the full reasoning trail behind every decision made since.

## Repo layout

- `data/raw/` — sequences, structures, and mutation lists as pulled from source (NCBI, UniProt, PDB, literature)
- `data/processed/` — cleaned/aligned/numbered data ready for analysis
- `scripts/` — Python (ChimeraX scripting, conservation, permutation test) and R (mixed models) scripts
- `output/figures/`, `output/tables/` — generated results
- `docs/` — planning and methods notes

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

R packages (run once from an R console): `install.packages(c("lme4", "ggplot2"))`

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
