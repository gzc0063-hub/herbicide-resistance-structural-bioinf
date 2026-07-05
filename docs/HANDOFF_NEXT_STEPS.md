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
- [x] **1.8 Single-environment ACCase re-run.** DONE — re-ran `scripts/chimerax_accase_distance_sasa.py`
  in this machine's ChimeraX 1.12. All six reported ACCase mutation positions reproduced **exactly**
  (Ile1781Leu 0.00/pct3.2, Trp2027Cys 5.60/10.4, Ile2041Asn 0.00/3.2, Asp2078Gly 5.19/8.7,
  Cys2088Arg 11.83/25.9, Gly2096Ala 7.28/12.8), matching the committed metric CSV and the manuscript.
  The committed CSV was left unchanged (regen produced only line-ending churn). ChimeraX is available in
  the Claude environment, so the PPO/ALS metric CSVs can also be re-verified the same way if desired.

## Tier 2 — turns a resource into a finding

- [x] **2.1 Manuscript reframed around the outlier typology.** DONE. Corrected all p-values; added the
  non-core-survives result and template-residue transparency; Abstract conclusion now leads with the
  typology as the contribution and calls proximity enrichment the expected baseline; Introduction adds
  an explicit expected-vs-novel thesis paragraph; Results enrichment section is framed as "establish the
  baseline first," and the typology section is retitled "A Structural Typology of Resistance Positions
  (the main contribution)." EPSPS relabelled binding-site-associated. Remaining polish for a later pass:
  per-family "resistance-zone map" figure (2.3) and citation formatting.
- [x] **2.2 Expand ALS (n=2 → n=4).** DONE with verified primary sources.
  - **Ala122Ser** — Larran 2017 (KY781920), medium confidence (co-occurs with A282D, causality not isolated).
  - **Pro197Ala** — Singh et al. 2018 (DOI 10.1002/ps.5232, PDF read in full) detected it in A. palmeri
    (with Trp574Leu); reference-numbered to KT833339.1 (Singh's "accessions" are field localities, not
    GenBank deposits). Nie/Young 2025 is a second A. palmeri Pro197 report (its Data Availability oddly
    points to Larran's KY781922/923, so no new accession from it).
  - ALS now n=4, all direct-core; enrichment p=0.000100. All outputs/manuscript/tests updated; 19 pass.
  - **Asp376 deliberately NOT added:** Singh 2018 lists it only as a known locus and did not detect it in
    their A. palmeri plants; no A. palmeri Asp376 primary source is in hand. To add it later, either get a
    verified A. palmeri (or clearly-labelled other-species) Asp376 source, or drop it. Residue 376 is
    present in 1Z8N (ASP, in-core) so only the source is missing.
  - *Optional upgrade:* attach paired resistant/susceptible GenBank accessions for the reference-numbered
    ALS rows (Ala122, Pro197) if a source deposits them.
- [x] **2.3 Resistance-zone map figure.** DONE as an OpenGL-free schematic SVG (`figure_5_resistance_zone_map.svg`,
  built by `scripts/build_resistance_zone_figure.py`, wired into `rebuild_all.py`, referenced in the
  manuscript). A 3D structure-rendered version is scripted in `scripts/chimerax_resistance_zone_figures.py`
  but needs a ChimeraX GUI/OSMesa environment (headless --nogui has no OpenGL on this machine).

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
- [x] **3.3 Reproducibility scaffolding.** DONE: pinned `requirements.txt`, added `CITATION.cff`,
  `LICENSE` (MIT, per user), and `scripts/rebuild_all.py` (one-command deterministic regen). **Remaining
  at submission time only:** cut a tagged release and Zenodo deposit for a data DOI; optionally note in
  README that data/tables are CC-BY-4.0 (code MIT).

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

- 2026-07-05 (g): Added manuscript References section (19 grounded refs; corrected Ji et al. 2025).
  Added Figure 5 resistance-zone map (schematic SVG; 3D ChimeraX version scripted but needs OSMesa).
  Items 2.2, 2.3, 3.3, 1.8, LICENSE all closed. Remaining: 1.2 (weed homology model, needs SWISS-MODEL),
  3.1 (docking/MD citations), Nakka 2017 PDF, Zenodo at submission. Committed.

- 2026-07-05 (f): User confirmed MIT + supplied 6 PDFs. Added LICENSE (MIT). Expanded ALS with
  Pro197Ala (Singh 2018) -> ALS n=4, p=0.0001; Asp376 left out (no A. palmeri source). Added the 6
  PDFs to docs/references/ (Singh 2018, Nie/Young 2025, McCourt 2006, Tranel&Wright 2002, Heinemann
  2007, Hao 2013). Items 2.2, 3.3, 1.8 now closed. Committed.

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
