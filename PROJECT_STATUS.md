# Project status — read this first

Snapshot of what's done, what every file is for, and what to do next. Everything
below is already committed and pushed to
https://github.com/gzc0063-hub/herbicide-resistance-structural-bioinf (private repo).

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
  pipeline. Result: both are themselves direct herbicide-contact residues, fully
  conserved across 9 species - a "textbook" confirmatory result, different in
  character from PPO's outlier finding but an equally valid pipeline validation.
- **Not started:** Phase 2 batch (ACCase, EPSPS, HPPD), Phase 3 (FAT, DHODH -
  needs ColabFold), Phase 4 (cross-enzyme synthesis), Phase 5 (deposit/submit).

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
| `CLAUDE_CODE_NEXT_STEPS.md` | An early working prompt from before Phase 1 execution - now superseded by DECISION_LOG, kept for history |
| `references/*.pdf` | The four primary-source papers now living directly in the repo: Dayan 2010, Hao 2009, Giacomini 2017 (all PPO), Larran 2017 (ALS) |

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
| `*_conservation_set.fasta` / `*_conservation_aligned.fasta` | The raw and MAFFT-aligned multi-species sequence sets behind each conservation score |

### `data/raw/` — everything pulled from external sources, unmodified
Sequences (FASTA) and structures (PDB) pulled from NCBI/RCSB, named by accession
and what they represent (species, mutation, wild-type-vs-resistant). Nothing in
here has been edited - if you need to re-derive anything, start here.

### `scripts/` — the actual pipeline code
| File | Purpose |
|---|---|
| `chimerax_distance_sasa.py` | PPO: percentile-rank distance-to-active-site + SASA on 1SEZ |
| `chimerax_als_distance_sasa.py` | ALS: same, on 1Z8N, with structure-derived active-site core |
| `chimerax_sasa_diagnostic.py` / `chimerax_probe_check.py` | One-off sanity checks (R98 SASA verification) - reference, not part of the main pipeline |
| `conservation_entropy.py` | PPO: Shannon entropy from the 10-species alignment |
| `als_conservation_entropy.py` | ALS: same, 9-species alignment |

### `output/`
Empty placeholders (`figures/`, `tables/`) - reserved for Phase 4 synthesis figures,
nothing generated yet.

---

## 3. What to do next (manually, step by step)

Per `DECISION_LOG.md` §10 and §16, the plan is: **batch ACCase, EPSPS, and HPPD
together now**, reusing the pipeline validated twice over (PPO, ALS). For each of
the three enzymes, repeat the same sequence of steps used for both pilots:

1. **Find a real crystal structure.** Search RCSB (`https://www.rcsb.org/search`)
   for the enzyme name + "herbicide" or a specific inhibitor name, restricted to
   plant/Viridiplantae source organism if possible. Note the PDB ID(s) and which
   herbicide chemical classes are represented.
2. **Find the documented resistance mutation(s).** Search Google Scholar / PubMed
   for "<enzyme> herbicide resistance mutation <weed species>" - prioritize
   *Amaranthus palmeri* or *A. tuberculatus* for continuity with the rest of the
   dataset if a paper exists for those species. Note candidate GenBank accessions.
3. **Verify before trusting.** Don't take a paper's abstract at face value -
   check Table/Figure data for the actual accession numbers and which population
   is explicitly labeled wild-type/susceptible (the ALS pilot's Larran et al. 2017
   Table 4 is the model to follow). If a paper is paywalled, this is exactly the
   `CONTRIBUTING.md` situation - get the PDF yourself and read the mutation table
   directly rather than trusting a secondary summary.
4. **Resolve numbering.** Check whether the crystal structure's own PDB residue
   numbers already match the literature convention (as they did for ALS - no work
   needed) or need an alignment-derived offset (as PPO did - see
   `scripts/als_conservation_entropy.py`'s docstring and `numbering_maps.json` for
   the pattern to follow either way).
5. **Define the active-site core.** Prefer deriving it directly from the structure
   (residues within ~4.5 Å of a bound inhibitor, as done for ALS) over hunting for
   a literature-defined core list - it's faster, avoids paywall dependencies, and
   is arguably more faithful to the original panel-review design.
6. **Run the pipeline.** Copy `chimerax_als_distance_sasa.py` as a template - swap
   the PDB ID, active-site residues, and check-positions. Same for
   `als_conservation_entropy.py` - swap in a diverse species panel (8-10 species,
   reuse the same species list as PPO/ALS where sequences exist for continuity).
7. **Write up results** in a `<enzyme>_validation_gate_results.md`, matching the
   PPO/ALS format, and add a new numbered section to `DECISION_LOG.md` documenting
   the outcome - that's what keeps this file useful as the project grows.
8. **Commit and push** after each enzyme, the way every step so far has been.

After all three are done, **Phase 4** is the cross-enzyme synthesis: pool
`ppo_mutations.csv` + `als_mutations.csv` + the three new CSVs into one table, run
the permutation/enrichment test the panel review recommended (see
`docs/panel_review_and_plan.md` §Part A, biostatistician reviewer) instead of a
naive logistic regression, and explicitly look for more outlier mutations like
ΔG210 across the full set.

**Phase 3 (FAT, DHODH)** is the one phase that needs something beyond what's set
up so far - these two targets don't have existing crystal structures, so they need
a ColabFold structure prediction run by hand in Google Colab (free tier), per the
original plan in `docs/panel_review_and_plan.md` Part B/D. Everything else in the
pipeline resumes normally once you have a predicted PDB file in hand.
