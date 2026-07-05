# Handoff / Next Steps — live work tracker

**Purpose:** single source of truth for "what we just did" and "what to do next," so any agent
(Claude or Codex) or a fresh session can resume without re-deriving context. Update the status boxes
below as each item is completed, and commit this file with every change.

**Context:** Two agents worked this repo in parallel (Claude Code + Codex). All work is now merged and
committed on `master`. A senior review (`docs/SENIOR_REVIEW_2026-07-05.md`) identified the blocking
pre-publication issues. This file tracks fixing them.

**Regeneration chain (run in this order after changing any source data/script):**
```
.venv/Scripts/python.exe scripts/build_phase4_tables.py          # master mutation table + contrast
.venv/Scripts/python.exe scripts/build_phase4_analysis.py        # permutation summary + non-core screen
.venv/Scripts/python.exe scripts/build_review_driven_outputs.py  # mechanism labels + manuscript tables + figures
.venv/Scripts/python.exe -m pytest -q                            # confirm tests pass
```
Per-family metric CSVs (`*_distance_sasa.csv`) require ChimeraX for PPO/ALS/ACCase or the pure-Python
fallback (`scripts/pdb_static_metrics.py`) for EPSPS; only re-run those if a structure/core changes.

---

## Tier 1 — correctness/credibility (do before any submission)

- [x] **1.1 Template-vs-weed residue transparency.** DONE. Added `weed_wt_residue`, `template_residue`,
  `template_matches_weed_residue`, `template_is_resistant_state` to the master table via
  `WEED_RESIDUES` + `normalize_residue` in `scripts/build_phase4_tables.py`. Audit result: PPO/ALS/EPSPS
  all match; ACCase mismatches at 2041(→Val), 2088(→Met/MSE), 1781(→Leu, template=resistant),
  2096(→Ala, template=resistant). Exactly the review's finding, now machine-visible.
- [~] **1.2 ACCase SASA/RSA caveat.** PARTIAL. The mismatch is now flagged per-row (1.1) and each
  affected ACCase mechanism annotation now carries an explicit "side-chain metrics are template-derived,
  not weed-specific" caveat (`scripts/build_review_driven_outputs.py`). *Still open (better fix):*
  homology-model the weed CT domain on 1UYS (SWISS-MODEL) and recompute ACCase SASA/RSA on the weed
  sequence. Needs a web homology-model step; deferred to Tier 2/3.
- [x] **1.3 Relabel EPSPS Pro106Ser** DONE — `allosteric_hinge` → `adjacent`, with corrected
  binding-site-associated text (Baerson 2002 / Salmonella homolog; 3.85 Å is a CA-cutoff artifact).
- [x] **1.4 De-uniform ACCase mechanism labels** DONE — now `direct_core` (2041, the one Délye modelled
  as direct steric clash), `second_shell_channel` (2027, 2078 — bottom-of-cavity, also reduce catalytic
  activity), `adjacent` (2096), `interface_induced_fit` (1781, 2088), each with APP/CHD selectivity and
  template-residue caveats in the annotation text. Added `second_shell_channel` to the figure color map.
- [x] **1.5 Enrichment excluding in-core positions** DONE — `build_phase4_analysis.py` now emits an
  `all` and a `non_core_only` row per family (new `position_set` column). **Key result: the signal
  survives** — PPO non-core p=0.0043 (n=3), ACCase non-core p=0.0043 (n=4). ALS has no non-core row
  (both positions direct-core). This is the non-tautological version of the enrichment claim.
- [x] **1.6 Fill EPSPS DOI** DONE — `10.1104/pp.001560` in `data/processed/epsps_mutations.csv`.
- [x] **1.7 Clamp negative SASA/RSA** DONE — `clamp_nonneg` in `build_phase4_tables.py`; no negative
  values remain in the master table.
- [ ] **1.8 Single-environment ACCase re-run.** Still open — needs ChimeraX. 5 of 6 ACCase positions
  came from the Codex ChimeraX run; re-run the ACCase distance/SASA pipeline once in one environment.
  (Cys2088Arg cross-checked; 2088→2014 confirmed independently.)

## Tier 2 — turns a resource into a finding

- [~] **2.1 Manuscript updated for Tier 1 (numbers + caveats); full reframe still pending.** DONE so far:
  corrected all enrichment p-values to the regenerated tables; added the non-core-survives result
  (the non-tautological finding) to Abstract + Results; added a "Template-Residue Transparency" Methods
  subsection and an ACCase side-chain caveat to Limitations; corrected the EPSPS Pro106Ser text from
  "allosteric" to binding-site-associated. *Still to do (the actual reframe):* restructure so the outlier
  typology (ΔG210 deletion, V361A permissive, Cys2088Arg distal, Pro106Ser second-shell) is the lead
  thesis and raw enrichment is the expected-baseline control — currently enrichment still leads.
- [ ] **2.2 Expand ALS** to Ala122/Pro197/Asp376 (biggest single power gain; structure + sequences in
  hand). Needs new `als_mutations.csv` rows + re-run.
- [ ] **2.3 Per-family "resistance-zone map" figure** (one structure cartoon per family, positions
  colored by proximity class).

## Tier 3 — depth / higher-tier journals

- [ ] **3.1 Published docking/MD as interpretation benchmark** for 2-3 flagship positions, with
  sentence-level citations.
- [ ] **3.2 FAT/DHODH** as declared future work; verify the DHODH plant co-crystal (Kang et al. 2023,
  PNAS) PDB accession before promising it.
- [ ] **3.3 Zenodo deposit + CITATION.cff + pinned env** for data-availability.

## "Even better" ideas (beyond current scope — see final section of SENIOR_REVIEW)

- Homology-model every weed sequence onto its template and compute metrics on the weed (not template)
  residues, uniformly across all families — removes the cross-species caveat entirely.
- Add AlphaMissense / conservation-based pathogenicity-style scores per position as an orthogonal axis.
- Replace per-family permutation with a single cross-family mixed-effects model (enzyme as random
  effect) for one unified statistic (the biostatistician reviewer's original suggestion).
- Add a matched-null test (resistance positions vs. same-count non-resistance residues drawn from the
  same structural shell) to control for pocket geometry more tightly than a whole-protein random draw.

---

## Change log (append newest at top)

- 2026-07-05 (c): Updated MANUSCRIPT_DRAFT.md to match regenerated tables — corrected all p-values,
  added the non-core-survives result and the template-residue transparency section + ACCase Limitations
  caveat, fixed EPSPS "allosteric"→binding-site-associated. 19 tests pass. Full outlier reframe (2.1)
  still pending. Committed.
- 2026-07-05 (b): Completed Tier 1 items 1.1, 1.3, 1.4, 1.5, 1.6, 1.7 (1.2 partial, 1.8 still needs
  ChimeraX). Regenerated master table + permutation summary + manuscript tables + figures; all 19 tests
  pass (added pytest to requirements). Committed.
- 2026-07-05 (a): Created this handoff tracker. Senior review committed. EPSPS verified vs Baerson PDF.
