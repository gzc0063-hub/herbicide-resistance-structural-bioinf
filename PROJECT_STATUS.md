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
- **An external methodology review was received and reconciled** (see
  `docs/EXTERNAL_REVIEW_RESPONSE.md`) - it couldn't access this private repo, so
  it reviewed a different plan/brief, not our actual work. One thing it flagged
  genuinely applied and was checked directly: **ALS's active-site core was
  missing 11 dimer-interface residues** (including Ala122/Pro197), now fixed -
  the Trp574/Ser653 conclusion is unchanged. One valid, not-yet-applied point:
  switch from raw SASA (Å²) to relative solvent accessibility (RSA, Tien et al.
  2013) before Phase 4's cross-enzyme comparison.
- **Not started:** Phase 2 batch (ACCase, EPSPS, HPPD), Phase 3 (FAT, DHODH -
  needs ColabFold, though DHODH may already have a public plant structure - see
  §3), Phase 4 (cross-enzyme synthesis), Phase 5 (deposit/submit).

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
| **`EXTERNAL_REVIEW_RESPONSE.md`** | Reconciliation of an external fact-check review: what applied to completed work and was fixed, what's valid-but-pending (RSA), and specific facts to adopt for ACCase/EPSPS/HPPD/FAT/DHODH before they're built - **read this before starting the next phase** |

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
together now**, reusing the pipeline validated twice over (PPO, ALS). **Read
`docs/EXTERNAL_REVIEW_RESPONSE.md` Part 2 first** - it has specific, checkable
facts for each of these three enzymes that will save you from repeating a mistake
before it happens. For each enzyme, repeat the same sequence of steps used for
both pilots, with two additions learned from the ALS correction:

1. **Find a real crystal structure.** Search RCSB (`https://www.rcsb.org/search`)
   for the enzyme name + "herbicide" or a specific inhibitor name, restricted to
   plant/Viridiplantae source organism if possible. Note the PDB ID(s) and which
   herbicide chemical classes are represented.
   - **ACCase:** consider 1UYS (yeast CT domain + haloxyfop) - if used, cite it
     correctly (Zhang, Tweel & Tong, *PNAS* 2004, 101(16):5910-5915) and note the
     numbering will need an offset from the field-standard *Alopecurus
     myosuroides* reference (AJ310767).
   - **EPSPS:** don't default to the *E. coli* structure (1G6S) without checking
     whether a genuine plant EPSPS structure exists first - numbering fidelity is
     much simpler if the template is a plant enzyme. Confirm the conformational
     state (glyphosate only binds the closed, S3P-bound conformation).
   - **HPPD:** verify candidate PDB IDs directly on RCSB rather than trusting any
     secondary list - "human 1SQD" would be wrong (1SQD is *Arabidopsis*; human
     HPPD is 3ISQ).
2. **Find the documented resistance mutation(s) - but for HPPD, check the premise
   first.** For ACCase/EPSPS, search Google Scholar/PubMed for "<enzyme> herbicide
   resistance mutation <weed species>" as before. **For HPPD specifically: verify
   whether a genuine, peer-reviewed, accession-backed weed target-site mutation
   exists at all before assuming this enzyme fits the same pilot shape as PPO/ALS.**
   Published evidence (Nakka et al. 2017, whole-gene sequencing of resistant
   Palmer amaranth) found no target-site mutation - resistance there is
   non-target-site (P450 metabolism) plus gene amplification. **Do not use
   "Gly336"/G336W as a weed mutation - it's an engineered *Pseudomonas
   fluorescens* crop-tolerance variant (FG72 soybean), not evolved resistance.**
   If no real weed target-site mutation turns up, frame HPPD as a
   substrate/inhibitor-contact structural analysis instead (see
   `EXTERNAL_REVIEW_RESPONSE.md`) rather than forcing a validation-gate mutation
   that doesn't exist.
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
5. **Define the active-site core - and explicitly check for dimer-interface
   contacts, don't assume a single-chain core is complete.** Derive it directly
   from the structure (residues within ~4.5 Å of a bound inhibitor, as done for
   ALS), but this time generate the biological assembly *first* and check for
   cross-chain contacts before finalizing the core - ALS's core was initially
   incomplete because this step was skipped, and ACCase's ligand is documented
   to sit at a dimer interface too, so this step is not optional there. **Use
   `atom.scene_coord`, not `atom.coord`, when comparing atoms across different
   symmetry-generated submodels** - the ALS correction was delayed by exactly
   this bug (identical local coordinates across copies gave a false negative).
6. **Run the pipeline.** Copy `chimerax_als_distance_sasa.py` as a template - swap
   the PDB ID, active-site residues, and check-positions. Same for
   `als_conservation_entropy.py` - swap in a diverse species panel (8-10 species,
   reuse the same species list as PPO/ALS where sequences exist for continuity).
7. **Report SASA as relative solvent accessibility (RSA), not raw Å².** Divide
   each residue's SASA by its residue-type maximum from Tien et al. 2013 (*PLoS
   ONE* 8(11):e80635) before writing up results - this wasn't done for PPO/ALS
   (retrofit those two before Phase 4 if time allows) but should be standard from
   ACCase onward, since cross-enzyme SASA comparison needs it.
8. **Write up results** in a `<enzyme>_validation_gate_results.md`, matching the
   PPO/ALS format, and add a new numbered section to `DECISION_LOG.md` documenting
   the outcome - that's what keeps this file useful as the project grows.
9. **Commit and push** after each enzyme, the way every step so far has been.

After all three are done, **Phase 4** is the cross-enzyme synthesis: pool
`ppo_mutations.csv` + `als_mutations.csv` + the three new CSVs into one table, run
the permutation/enrichment test the panel review recommended (see
`docs/panel_review_and_plan.md` §Part A, biostatistician reviewer) instead of a
naive logistic regression, use enzyme identity as a random/blocking effect, and
explicitly look for more outlier mutations like ΔG210 across the full set. Watch
for pseudoreplication (multiple mutations at one position, or multiple PDBs of
one enzyme, counted as independent) and never compare raw Å distances across
enzymes - only the within-structure percentile ranks are comparable.

**Phase 3 (FAT, DHODH)** needs something beyond what's set up so far - but check
DHODH first before assuming ColabFold is required: Kang, Emptage, Kim & Gutteridge
2023 (*PNAS* 120(48):e2313197120) reportedly includes a real plant DHODH
co-crystal structure (target of tetflupyrolimet) - if it's deposited in the PDB
with a public accession, Phase 3 may not need a ColabFold run for DHODH at all.
Verify this directly on RCSB before starting the Colab workflow. FAT (acyl-ACP
thioesterase, HRAC Group 30, target of cinmethylin/methiozolin - not the
mammalian thioesterase or FabB/FabF) is less clear; verify independently whether
a public structure exists before assuming either way.
