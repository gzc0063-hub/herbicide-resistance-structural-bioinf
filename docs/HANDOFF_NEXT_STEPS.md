# Handoff / Next Steps — live work tracker

**Purpose:** single source of truth for "what we just did" and "what to do next," so any agent
(Claude or Codex) or a fresh session can resume without re-deriving context. Update the status boxes
below as each item is completed, and commit this file with every change.

**Context:** Two agents worked this repo in parallel (Claude Code + Codex). All work is now merged and
committed on `master`. A senior review (`docs/SENIOR_REVIEW_2026-07-05.md`) identified the blocking
pre-publication issues. This file tracks fixing them.

**Regeneration chain — one command** (or run the four steps individually if debugging):
```
.venv/Scripts/python.exe scripts/rebuild_all.py   # runs the 3 build scripts + pytest, in order
```
Individual steps:
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

- [x] **2.1 Manuscript reframed around the outlier typology.** DONE. Corrected all p-values; added the
  non-core-survives result and template-residue transparency; Abstract conclusion now leads with the
  typology as the contribution and calls proximity enrichment the expected baseline; Introduction adds
  an explicit expected-vs-novel thesis paragraph; Results enrichment section is framed as "establish the
  baseline first," and the typology section is retitled "A Structural Typology of Resistance Positions
  (the main contribution)." EPSPS relabelled binding-site-associated. Remaining polish for a later pass:
  per-family "resistance-zone map" figure (2.3) and citation formatting.
- [~] **2.2 Expand ALS.** PARTIAL. Added **Ala122Ser** (A. palmeri, Larran 2017 / KY781920, medium
  confidence — co-occurs with A282D so individual causality not isolated). ALS is now n=3, all
  direct-core; enrichment strengthened to obs=4.64 vs 50.28, p=0.000200 (was p=0.0027 at n=2). Master
  table, permutation, manuscript tables/figures, manuscript numbers, and tests all regenerated/updated;
  19 tests pass. **Still to add: Pro197 and Asp376** — both are established ALS TSR sites and are already
  present + mapped in 1Z8N (residue 197=PRO, 376=ASP, both in-core, fully conserved), so only a verified
  clean single-allele Palmer amaranth SOURCE is missing. The best source is paywalled:
  **Küpper et al., "Target-site mutation accumulation among ALS inhibitor-resistant Palmer amaranth,"
  Pest Manag Sci, DOI 10.1002/ps.5232** — user should supply this PDF (Wiley, blocked automated fetch).
  The "A New Pro-197-Ile Mutation in Amaranthus palmeri" paper (Plants 2025, DOI 10.3390/plants14040525)
  is an alternative Pro197 source to verify. Once a PDF is in hand, add rows exactly like Ala122Ser
  (add to `als_mutations.csv`, add WEED_RESIDUES entry in build_phase4_tables.py, add MECHANISM_ANNOTATIONS
  ("ALS","197")/("ALS","376") in build_review_driven_outputs.py, bump the row-count asserts in the three
  affected tests, regenerate the chain, update manuscript ALS numbers).
- [ ] **2.3 Per-family "resistance-zone map" figure** (one structure cartoon per family, positions
  colored by proximity class).

## Tier 3 — depth / higher-tier journals

- [ ] **3.1 Published docking/MD as interpretation benchmark** for 2-3 flagship positions, with
  sentence-level citations.
- [~] **3.2 FAT/DHODH future-work verification.** CHECKED: RCSB full-text search for
  "dihydroorotate dehydrogenase tetflupyrolimet" returned **no hit**, and the broad Viridiplantae-DHODH
  hits were false matches (phototropin LOV domains). So a public plant DHODH inhibitor-bound structure is
  **not confirmed available** — Phase 3 DHODH must stay "future work, structure availability unconfirmed"
  (do not promise the Kang et al. 2023 PNAS structure without a specific verified PDB accession from the
  user or the paper's own Data Availability). FAT (acyl-ACP thioesterase) likewise unverified. Both remain
  out of the current manuscript's pooled analysis.
- [~] **3.3 Reproducibility scaffolding.** DONE: pinned `requirements.txt` to exact tested versions
  (Python 3.14.4) and added `CITATION.cff`. **Still to do:** add a `LICENSE` file (user's call — review
  recommended MIT for code + CC-BY-4.0 for data; CITATION.cff currently declares MIT), and cut a tagged
  release + Zenodo deposit at submission time.

## "Even better" ideas (beyond current scope — see final section of SENIOR_REVIEW)

- Homology-model every weed sequence onto its template and compute metrics on the weed (not template)
  residues, uniformly across all families — removes the cross-species caveat entirely.
- Add AlphaMissense / conservation-based pathogenicity-style scores per position as an orthogonal axis.
- Replace per-family permutation with a single cross-family mixed-effects model (enzyme as random
  effect) for one unified statistic (the biostatistician reviewer's original suggestion).
- Add a matched-null test (resistance positions vs. same-count non-resistance residues drawn from the
  same structural shell) to control for pocket geometry more tightly than a whole-protein random draw.

---

## Ready-to-paste Codex prompt (for the paywalled ALS expansion, 2.2 remainder)

> In the repo `herbicide-resistance-structural-bioinf`, expand the ALS family with Pro197 and Asp376.
> I have supplied the PDF(s): Küpper et al. Pest Manag Sci (DOI 10.1002/ps.5232) and/or the A. palmeri
> Pro197Ile paper (Plants 2025, DOI 10.3390/plants14040525). For each position, verify from the PDF's
> own text/tables the exact substitution and any deposited accession (do NOT infer). Then, mirroring the
> existing `Ala122Ser` row: (1) append a row to `data/processed/als_mutations.csv` with
> position_1z8n_structure = 197 or 376 (both verified present in 1Z8N chain A as PRO/ASP, in-core, fully
> conserved); (2) add the weed WT/mut residues to `WEED_RESIDUES` in `scripts/build_phase4_tables.py`
> (Pro197→("PRO", mut); Asp376→("ASP", mut)); (3) add `("ALS","197")` / `("ALS","376")` entries to
> `MECHANISM_ANNOTATIONS` in `scripts/build_review_driven_outputs.py` (both direct_core); (4) bump the
> row-count assertions in `tests/test_phase4_tables.py` (16→N), `tests/test_review_driven_outputs.py`
> (14→N), and the ALS count + screen count in `tests/test_phase4_analysis.py`; (5) run the regeneration
> chain (build_phase4_tables → build_phase4_analysis → build_review_driven_outputs) and `pytest -q`;
> (6) update the ALS numbers in `docs/MANUSCRIPT_DRAFT.md` to the regenerated `manuscript_table_1`
> values; (7) tick item 2.2 in `docs/HANDOFF_NEXT_STEPS.md` and commit. Keep the project's rule: no row
> without a primary-source-verified substitution.

## Change log (append newest at top)

- 2026-07-05 (e): Verified no public plant DHODH inhibitor structure via RCSB (3.2 → stays unconfirmed
  future work). Added pinned requirements.txt + CITATION.cff (3.3); LICENSE still a user decision.
  Committed.
- 2026-07-05 (d): Expanded ALS with Ala122Ser (Larran 2017, in-repo verified); ALS now n=3, p=0.0002.
  Regenerated everything, updated manuscript, 19 tests pass. Pro197/Asp376 handed off (need paywalled
  ps.5232 PDF) with a ready-to-paste Codex prompt above. Committed.
- 2026-07-05 (c): Updated MANUSCRIPT_DRAFT.md to match regenerated tables — corrected all p-values,
  added the non-core-survives result and the template-residue transparency section + ACCase Limitations
  caveat, fixed EPSPS "allosteric"→binding-site-associated. 19 tests pass. Full outlier reframe (2.1)
  still pending. Committed.
- 2026-07-05 (b): Completed Tier 1 items 1.1, 1.3, 1.4, 1.5, 1.6, 1.7 (1.2 partial, 1.8 still needs
  ChimeraX). Regenerated master table + permutation summary + manuscript tables + figures; all 19 tests
  pass (added pytest to requirements). Committed.
- 2026-07-05 (a): Created this handoff tracker. Senior review committed. EPSPS verified vs Baerson PDF.
