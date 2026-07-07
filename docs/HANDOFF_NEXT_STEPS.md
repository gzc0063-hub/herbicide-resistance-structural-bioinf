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
  `WEED_RESIDUES` + `normalize_residue` in `scripts/build_phase4_tables.py`. The original 1UYS audit
  made the review's ACCase mismatch concern machine-visible; the active Phase 4 ACCase path now uses the
  SWISS-MODEL weed CT-domain dimer, so all six ACCase accepted positions match the weed wild-type residue
  in the current master table.
- [x] **1.2 ACCase SASA/RSA caveat.** DONE. Downloaded the SWISS-MODEL AJ310767 CT-domain homodimer
  built on 1UYS (`data/raw/ACCase_Alopecurus_AJ310767_CTdomain_SWISSMODEL_1UYS_homomer.pdb` plus JSON
  metadata), recomputed ACCase distance/SASA/RSA on the weed-sequence model with
  `scripts/accase_swissmodel_distance_sasa.py`, and switched Phase 4 to
  `data/processed/accase_swissmodel_1uys_distance_sasa.csv`. Remaining caveat is now narrower and
  explicit: SWISS-MODEL excluded H1L, so active-site-core membership is transferred from aligned 1UYS
  H1L-contact residues; side-chain metrics are homology-model-derived, not crystal-observed.
- [x] **1.3 Relabel EPSPS Pro106Ser** DONE — `allosteric_hinge` → `adjacent`, with corrected
  binding-site-associated text (Baerson 2002 / Salmonella homolog; 3.85 Å is a CA-cutoff artifact).
- [x] **1.4 De-uniform ACCase mechanism labels** DONE — now `direct_core` (2041, the one Délye modelled
  as direct steric clash), `second_shell_channel` (2027, 2078 — bottom-of-cavity, also reduce catalytic
  activity), `adjacent` (2096), `interface_induced_fit` (1781, 2088), each with APP/CHD selectivity and
  SWISS-MODEL/active-site-core-transfer caveats where needed. Added `second_shell_channel` to the figure
  color map.
- [x] **1.5 Enrichment excluding in-core positions** DONE — `build_phase4_analysis.py` now emits an
  `all` and a `non_core_only` row per family (new `position_set` column). **Key result: the signal
  survives** — PPO non-core p=0.0041 (n=3), ACCase non-core p=0.010199 (n=4) after the SWISS-MODEL
  ACCase rerun. ALS has no non-core row (all four current ALS positions are direct-core). This is the
  non-tautological version of the enrichment claim.
- [x] **1.6 Fill EPSPS DOI** DONE — `10.1104/pp.001560` in `data/processed/epsps_mutations.csv`.
- [x] **1.7 Clamp negative SASA/RSA** DONE — `clamp_nonneg` in `build_phase4_tables.py`; no negative
  values remain in the master table.
- [x] **1.8 Single-environment ACCase re-run.** DONE — re-ran `scripts/chimerax_accase_distance_sasa.py`
  in this machine's ChimeraX 1.12. All six reported ACCase mutation positions reproduced **exactly**
  (Ile1781Leu 0.00/pct3.2, Trp2027Cys 5.60/10.4, Ile2041Asn 0.00/3.2, Asp2078Gly 5.19/8.7,
  Cys2088Arg 11.83/25.9, Gly2096Ala 7.28/12.8), matching the original 1UYS metric CSV. This is now
  provenance only: active Phase 4 ACCase metrics are superseded by the SWISS-MODEL weed dimer in item
  1.2. ChimeraX is available in the Claude environment, so the PPO/ALS metric CSVs can also be
  re-verified the same way if desired.

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

- [x] **3.1 Published docking/MD as interpretation benchmark** DONE. Added sentence-level benchmark
  citations in the manuscript Discussion/typology sections: PPO DeltaG210 (Dayan 2010 + Hao 2009),
  PPO R98/substrate-recognition context (Heinemann 2007 + Hao 2013), and ACCase CT-domain cavity
  interpretation (Delye 2005 + Zhang 2004 + Yu 2007). This remains literature interpretation, not a
  new docking/MD analysis.
- [x] **3.2 FAT/DHODH future-work verification.** UPDATED. Phase 5 design gate now exists at
  `docs/superpowers/specs/2026-07-05-fat-dhodh-phase5-design.md`. New structured RCSB audit found:
  FAT is structurally actionable first (plant acyl-ACP thioesterase structures include Lemna inhibitor
  complexes 8P8K, 8QRT, 8QS0 and Arabidopsis FatA fragment structures 7HQQ-7HQU), while structured DHODH
  entity search found 278 DHODH polymer entities across 273 entries but **zero plant-like organisms**.
  Decision: start Phase 5 as an emerging-target validation/audit module; do not merge FAT/DHODH into
  Phase 4 pooled enrichment unless mutation evidence and structure/model mapping pass the same evidence
  gate as PPO/ALS/EPSPS/ACCase.
- [x] **3.3 Reproducibility scaffolding.** DONE: pinned `requirements.txt`, added `CITATION.cff`,
  `LICENSE` (MIT, per user), and `scripts/rebuild_all.py` (one-command deterministic regen). **Remaining
  at submission time only:** cut a tagged release and Zenodo deposit for a data DOI; optionally note in
  README that data/tables are CC-BY-4.0 (code MIT).

## Tier 4 — Phase 5 / emerging targets

- [x] **4.1 FAT/DHODH design gate.** DONE. Wrote and committed
  `docs/superpowers/specs/2026-07-05-fat-dhodh-phase5-design.md` (`b92f5b0`). Recommendation: FAT-first
  because plant inhibitor-complex structures are available; keep DHODH behind source/model verification.
- [x] **4.2 Build Phase 5 audit artifacts.** DONE as starter audit. Created
  `docs/PHASE5_FAT_DHODH_AUDIT.md` and `data/processed/phase5_target_status.csv`. FAT is marked
  `audit_first`; DHODH is marked `hold_model_source`. These files classify target/MoA evidence,
  structure/model status, mutation evidence state, and go/no-go status. Do not add FAT/DHODH to
  `build_phase4_tables.py` during this audit.
- [x] **4.3 FAT mutation-source audit.** DONE. Verified directly from the primary PDF (user-supplied):
  Wagner et al. 2026 bioRxiv (`docs/references/Wagner_et_al_2026_FAT_R171_biorxiv.pdf`). R171K/Q/I/M
  (FAT A, *Alopecurus myosuroides*) and P192R (FAT B) are **engineered/docking-predicted, not
  weed-evolved** — site-directed mutants tested in vitro, not observed in weeds. R171K gives RI 516.56
  but needs 3 simultaneous nucleotide changes; paper itself concludes field risk is low. Full table now
  in `data/processed/phase5_risk_table.csv`. Separately found real (but non-target-site) cinmethylin
  resistance in field *Lolium rigidum* via enhanced metabolism (DOI 10.1002/ps.6947) — the audit draft
  had missed this entirely. See `docs/PHASE5_FAT_DHODH_AUDIT.md` and `docs/VERIFICATION_LOG.md` for
  full detail.
- [x] **4.4 DHODH mutation/model audit.** DONE. Verified directly from PMC full text: Kang et al. 2023
  PNAS (DOI 10.1073/pnas.2313197120) solved a rice DHODH-tetflupyrolimet crystal structure and built an
  AlphaFold *Arabidopsis* DHODH model, **neither publicly deposited** (no PDB ID given in the paper) —
  corrected framing from "no plant structure exists" to "no *public* plant structure exists." Mutation
  evidence: G198E and A141T (corrected from an earlier secondary-source "A141V") in two EMS-mutagenized
  *Arabidopsis thaliana* lines — **lab-selected, not weed-evolved**. Full detail in
  `docs/PHASE5_FAT_DHODH_AUDIT.md` and `docs/VERIFICATION_LOG.md`.
- [x] **4.5 Repo navigation index.** DONE. Added root `REPO_INDEX.md` and linked it from `README.md`
  (`a4100f2`). This is the first file to hand to any new agent before asking it to work in the repo.
- [x] **4.6 Canonical presentation reset.** DONE. Removed old generated deck/preview outputs from
  `output/presentations/`, saved the user-attached deck as
  `output/presentations/herbicide_resistance_structural_bioinformatics_talk.pptx`, and archived the
  user-attached guide as `docs/PROJECT_HANDOFF_GUIDE.doc`. Future presentation edits should preserve
  the attached deck's style unless the user explicitly asks for design changes.
- [x] **4.7 FAT residue-numbering alignment.** DONE — result is negative. No public *A. myosuroides*
  FatA sequence exists (checked NCBI protein/nuccore + UniProt directly, zero hits), so used wheat
  (*Triticum aestivum*, UniProt Q8L6B1, both Pooideae grasses) as a proxy. Global BLOSUM62 alignment
  (`scripts/phase5_fat_numbering_check.py`, 77.8% identity) shows Arabidopsis Arg176 (the cinmethylin
  H-bond donor in PDB 9GRR) aligns to **wheat Arg103**, not wheat position 171 (a threonine) — a ~73
  residue gap matching the 74-residue Arabidopsis transit peptide almost exactly. **Conclusion: R171
  (blackgrass) and Arg176 (Arabidopsis) are most likely different residues, not the same catalytic
  arginine at a small species offset** — refutes the prior audit pass's working hypothesis. Do not
  structurally contextualize R171 using 9GRR without the actual blackgrass sequence. Full detail in
  `docs/VERIFICATION_LOG.md` and `docs/PHASE5_FAT_DHODH_AUDIT.md`.
- [x] **4.8 Lolium rigidum cinmethylin-metabolism full-text read.** DONE. Verified directly from the
  primary PDF (user-supplied, peer-reviewed): Goggin et al. 2022, Pest Manag Sci, DOI 10.1002/ps.6947.
  Three WA field populations (R1, R2, R3) show reduced cinmethylin sensitivity via **enhanced P450-mediated
  metabolism**, statistically significant for R2/R3 on coleoptile elongation (RI 2.7/3.2) and R3 on
  radicle elongation (RI 4.5); mechanism confirmed via phorate (P450 inhibitor) reversal. Real,
  weed-evolved/weed-derived NTSR — genuinely distinct from the engineered FAT target-site variants.
  Full detail now in `data/processed/phase5_risk_table.csv`, `docs/PHASE5_FAT_DHODH_AUDIT.md`, and
  `docs/VERIFICATION_LOG.md`.

## "Even better" ideas (beyond current scope — see final section of SENIOR_REVIEW)

- Homology-model every weed sequence onto its template and compute metrics on the weed (not template)
  residues, uniformly across all families — removes the cross-species caveat entirely.
- Add AlphaMissense / conservation-based pathogenicity-style scores per position as an orthogonal axis.
- Replace per-family permutation with a single cross-family mixed-effects model (enzyme as random
  effect) for one unified statistic (the biostatistician reviewer's original suggestion).
- Add a matched-null test (resistance positions vs. same-count non-resistance residues drawn from the
  same structural shell) to control for pocket geometry more tightly than a whole-protein random draw.

### Added from the 2026-07-06 handoff-guide (v2) expert-panel review

The v2 handoff guide's own Limitations section proposed several "workable within scope" fixes. Reviewed
against the actual repo state (no factual errors found in the guide) and worth tracking as concrete future
items rather than just praised in passing:

- ~~Expand EPSPS beyond n=1.~~ **Done 2026-07-07:** the Pro106 series (Ser/Thr/Ala/Leu) was correctly
  identified as *not* increasing power - de-duplication collapses them to the same structural position -
  so Thr102Ile (a genuinely distinct position, verified via Yu et al. 2015) was added instead, taking
  EPSPS to n=2, p=0.0147. Gly101Ala was investigated and excluded (engineered/transgenic only, not
  weed-evolved - see `docs/DECISION_LOG.md` #38 and `docs/VERIFICATION_LOG.md`). Further expansion beyond
  n=2 remains open if a third genuinely distinct, weed-evolved, primary-source-verified position is found.
- **Core-cutoff sensitivity analysis.** Still open. Re-run each family's enrichment test across a range of
  active-site-core distance thresholds (not just the one adopted cutoff) and report that the enrichment
  and typology are stable. This directly answers the "structure choice and core definition affect the
  output" limitation with an actual robustness check instead of just stating the caveat.
- **ACCase: check for new plant ACCase depositions + an AlphaFold cross-check.** Still open. Re-check RCSB
  for any grass/plastidic ACCase structure deposited since the last check, and add an AlphaFold model of
  the same black-grass CT domain as an independent cross-check alongside the current SWISS-MODEL homology
  model - blocked on GPU/API access in the current environment (confirmed 2026-07-07: no AlphaFold3/ESMFold
  API reachable). The SWISS-MODEL homology model's 53.3% identity to 1UYS (corrected from an initially
  proposed but wrong 55.3%) is now explicitly defended in the manuscript with the Rost 1999 twilight-zone
  citation in the meantime.
- **A single-structure ΔΔG proxy (FoldX or DDGun) per mutation.** Still open - no licensed FoldX/DDGun
  available in this environment (confirmed 2026-07-07). A pure-Python biophysical perturbation score
  (bulkiness/hydropathy/charge deltas) was added instead as an orthogonal, transparent property-difference
  axis - explicitly not a ΔΔG substitute. An actual physics-based ΔΔG would still more directly answer the
  "static metrics cannot estimate mutant binding free energy" scope boundary if a licensed tool becomes
  available in a future environment. Of the four
  items here, this is the one most likely to move the manuscript toward a higher-tier journal if pursued.

---

## Ready-to-paste Claude Code prompt (current handoff)

> You are continuing the repository `herbicide-resistance-structural-bioinf` on `master`.
> First read `REPO_INDEX.md`, then `docs/HANDOFF_NEXT_STEPS.md`, `docs/DECISION_LOG.md`,
> `docs/VERIFICATION_LOG.md`, and `docs/superpowers/specs/2026-07-05-fat-dhodh-phase5-design.md`.
> Current head should include:
> - `a4100f2 Add repository navigation index`
> - `b92f5b0 Design Phase 5 FAT DHODH validation gate`
> - `1c6f711 Use SWISS-MODEL ACCase weed dimer metrics`
>
> What was done in the latest Codex session and why:
> 1. ACCase was upgraded from yeast-template side-chain metrics to a SWISS-MODEL black-grass
>    AJ310767 CT-domain homodimer. The active ACCase metric file is now
>    `data/processed/accase_swissmodel_1uys_distance_sasa.csv`; H1L was excluded by SWISS-MODEL, so the
>    active-site core is transferred from aligned 1UYS H1L-contact residues. This closed the senior-review
>    ACCase caveat without overclaiming crystal-observed weed side chains.
> 2. Phase 5 FAT/DHODH was scoped as an emerging-target validation gate, not immediate Phase 4 pooling.
>    Structured RCSB checks found plant FAT/acyl-ACP thioesterase structures (Lemna 8P8K/8QRT/8QS0 and
>    Arabidopsis 7HQQ-7HQU), but structured DHODH entity search found 278 DHODH polymer entities across
>    273 entries with zero plant-like organisms. Therefore FAT is the likely first actionable Phase 5
>    target; DHODH needs mutation evidence plus a plant structure/model route.
> 3. `REPO_INDEX.md` was added as the navigation map for branches, data, scripts, figures, tests,
>    output tables, docs, and future-work rules.
> 4. The user-attached PowerPoint is now the canonical presentation deliverable at
>    `output/presentations/herbicide_resistance_structural_bioinformatics_talk.pptx`. Old generated
>    deck outputs, preview image folders, montages, inspect files, and failed asset folders were removed
>    from `output/presentations/`. Preserve this deck's style for future presentation edits unless the
>    user explicitly asks for changes.
> 5. The user-attached handoff/onboarding guide is archived at `docs/PROJECT_HANDOFF_GUIDE.doc`.
>
> Your next task is Phase 5 audit follow-through, not pipeline integration yet:
> - Read `docs/PHASE5_FAT_DHODH_AUDIT.md`.
> - Read `data/processed/phase5_target_status.csv`.
> - For FAT, verify primary-source evidence for the planned "FAT-A R171-region" resistant variant(s):
>   exact mutation, species, accession/source, evidence type (weed-evolved, lab-selected, engineered, or
>   hypothetical), and whether it can enter a separate Phase 5 risk table.
> - For DHODH, verify tetflupyrolimet/DHODH target evidence and any mutation/source/model evidence.
>   Do not claim a public plant DHODH structure unless you identify a specific PDB accession or
>   paper-supplied coordinate/model source.
> - Update `docs/HANDOFF_NEXT_STEPS.md`, `docs/DECISION_LOG.md`, and `docs/VERIFICATION_LOG.md` with all
>   evidence and decisions.
> - Do not add FAT or DHODH to `scripts/build_phase4_tables.py` or the pooled Phase 4 manuscript tables
>   until their mutation evidence and structure/model mapping pass the validation gate.
> - Keep the project rule: no mutation row without primary-source support, and never describe lab-selected
>   or engineered variants as weed-evolved TSR.

## Historical Codex prompt (paywalled ALS expansion, now closed)

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

- 2026-07-07 (w): "Phase 6" pipeline expansion, executed after rejecting a first version that
  asserted unverified mutations as fact and asked to fabricate documentation of unavailable
  tool integrations (see `docs/DECISION_LOG.md` #38 for the full back-and-forth). Confirmed
  R/rpy2/lme4/FoldX/DDGun/ESMFold are all unavailable in this environment before doing anything.
  **EPSPS expanded to n=2**: added Thr102Ile (Yu et al. 2015, real *Eleusine indica* TIPS allele,
  GenBank KM078728, medium confidence - never observed viable alone) alongside the existing
  Pro106Ser; EPSPS moves from a single descriptive point (p=0.129) to a significant 2-position
  test (p=0.0147). Investigated and **excluded Gly101Ala** - documented almost exclusively in
  engineered/transgenic contexts, not weed populations. **ALS expanded to n=5**: added Asp376Glu
  (Palma-Bautista et al. 2022, real *Sinapis alba* population, GenBank OP681621/OP681622, clean
  single-SNP, high confidence). Added a **biophysical perturbation score** (Zimmerman 1968
  bulkiness + Kyte-Doolittle 1982 hydropathy + formal charge deltas, `scripts/biophysical_perturbation.py`)
  as a pure-Python alternative to FoldX/DDGun. Added a **global combined permutation test**
  (`scripts/build_phase4_analysis.py`) pooling all 17 positions (p=0.0001) and all 8 non-core
  positions (p=0.0001) across every family, as a pure-Python alternative to an R/lme4 GLMM -
  documented everywhere as a pooled-cohort statistic, not a mixed-effects-model substitute.
  Corrected the ACCase SWISS-MODEL identity number to the actual recorded 53.27% (not the
  proposed 55.3%) and strengthened its defense with the Rost 1999 "twilight zone" citation.
  Updated `MANUSCRIPT_DRAFT.md` (renumbered to 27 references, re-verified programmatically),
  `MANUSCRIPT_RESULTS_PHASE4.md`, `README.md` (corrected the stale R/lme4 mention), and both
  `tests/test_phase4_tables.py` and `tests/test_phase4_analysis.py` for the new row/position
  counts. All 20 tests pass; `rebuild_all.py` and PMS figure conversion both ran clean. Full
  verification trail in `docs/VERIFICATION_LOG.md`.

- 2026-07-06 (v): Replaced `docs/PROJECT_HANDOFF_GUIDE.doc` and
  `output/presentations/herbicide_resistance_structural_bioinformatics_talk.pptx` with user-supplied
  version-2 updates (Claude Code). Fact-checked the guide's specific claims against the actual repo
  before adopting it (17 mutation rows by family, FAT/DHODH audit findings incl. the R171/Arg176
  refutation, PMS submission status) — all matched exactly, no corrections needed. Reviewed the guide's
  Limitations section as an expert panel per the user's request: no factual errors, and its own
  "workable within scope" fixes were judged good enough to track rather than just praise — added four
  items to the "Even better ideas" section (EPSPS expansion beyond n=1, core-cutoff sensitivity check,
  ACCase AlphaFold cross-check, single-structure ΔΔG proxy via FoldX/DDGun), flagging that the EPSPS
  candidate positions (Pro106 series, Thr102Ile, TIPS double) still need primary-source verification
  before curation, same as every other row in the dataset. Logged in `docs/DECISION_LOG.md` (#37).

- 2026-07-05 (u): Handled the three remaining submission-prep items (Claude Code, per user direction).
  (1) Figure format: confirmed Wiley's general vector-figure requirement applies to PMS (PDF/EPS, not
  TIFF, since all 5 figures are line-art/schematics). Added `scripts/convert_figures_for_pms.py`
  (svglib + reportlab) writing to a new `output/figures_pms/` folder; visually spot-checked all 5 PDFs.
  While checking Figure 5, found and fixed a real pre-existing bug in
  `scripts/build_resistance_zone_figure.py`: the label-stagger logic only alternated between 2 vertical
  offsets, so the 4 ALS direct-core positions (identical percentile) rendered as illegible overlapping
  text regardless of file format. Fixed with a longer offset ladder; confirmed all 4 labels now render
  distinctly. (2) Zenodo/data DOI: added `.zenodo.json` alongside the existing `CITATION.cff`, and wrote
  `docs/ZENODO_DEPOSIT_GUIDE.md` explaining what a Zenodo deposit is, why the journal wants it over a bare
  GitHub link, exactly what's already prepared, and the remaining account-linking + release steps only
  the user can do — deliberately not triggering a release yet since the manuscript is still being edited.
  (3) ORCID: added a `[to be added]` placeholder in the manuscript author block and a commented-out
  `orcid:` field in `CITATION.cff`, left for the user to fill in. Added `svglib`/`reportlab` to
  `requirements.txt`. All 20 tests pass, citation/reference consistency re-verified (22/22), `git diff
  --check` clean.

- 2026-07-05 (t): Resolved the two remaining structure-citation gaps flagged in the previous pass
  (Claude Code, per user-supplied RCSB citations, independently re-verified against RCSB's own data API
  before use — matched exactly). EPSPS structure 8UMJ's RCSB primary citation is Reed et al. 2024 (PNAS,
  evolving dual-trait EPSPS variants via yeast selection); HPPD structure 5YWG's is Lin et al. 2019
  (FEBS J, HPPD-inhibition kinetics/crystallography/computational study). Both added to
  `docs/MANUSCRIPT_DRAFT.md` with deliberately conservative wording ("RCSB-linked primary citation," not
  resistance evidence, since neither paper is about weed resistance) as refs 3 and 5, requiring a full
  renumbering of the reference list (prior refs 3-20 -> 4-22); re-verified programmatically that all 22
  references are cited exactly once in strict first-appearance order. Logged in `docs/VERIFICATION_LOG.md`
  and `docs/DECISION_LOG.md` (#36). `git diff --check` clean. Remaining real gaps: PMS figure-format
  confirmation, Zenodo/data DOI at submission, ORCID.

- 2026-07-05 (s): Prepared the manuscript for Pest Management Science submission (Claude Code, per user
  request and journal choice). Converted all in-text citations to PMS's superscript sequential-numbering
  style, added inline citations at every structure/mutation mention that previously lacked one (Koch 2004,
  McCourt 2006, Zhang 2004, Heinemann 2007, Tien 2013, Giacomini 2017, Larran 2017, Singh 2018, Ji 2025,
  Tranel & Wright 2002, Délye 2005, Patzoldt 2006, Rangani 2019, Nie 2023, Nakka 2017, Hao 2013 were all
  previously present only in the reference list with no inline citation point), reordered and reformatted
  the reference list to PMS style, and verified programmatically that all 20 references are cited exactly
  once each in strict first-appearance order with no gaps or orphans. Trimmed the abstract from 482 to 189
  words (PMS limit 150-200); body text is 2974 words (PMS limit 6000, no cut needed). Added the author
  block (Gourav Chahal, Dept. of Crop, Soil and Environmental Sciences, Auburn University), Acknowledgments,
  Funding (none), and Competing Interests (none) sections, none of which existed before. Added scientific
  names at first prose use of tobacco, maize, black-grass, and Palmer amaranth per PMS convention. Also
  found and fixed a real correctness bug while re-verifying the manuscript's own numbers: `clamp_nonneg` in
  `scripts/build_phase4_tables.py` failed on exact negative zero (`-0.0 < 0` is `False` in IEEE 754), so
  `-0.0`/`-0.000000` noise was slipping through uncaught in `shannon_entropy` and (via
  `build_review_driven_outputs.py`, now also patched) `manuscript_table_2`'s RSA column. Fixed the boundary
  condition, verified zero negative/negative-zero values remain in any `output/tables/*.csv`. All 20 tests
  still pass. Remaining real gaps before submission: citations for the EPSPS (8UMJ) and HPPD (5YWG)
  structure-origin papers are not yet identified (flagged in the manuscript's own to-do, not fabricated),
  confirm PMS's figure-file-format requirement, and the Zenodo/data-DOI step at submission time.

- 2026-07-05 (r): Completed Phase 5 item 4.7 (Claude Code) — ran the sequence-alignment check on
  whether blackgrass R171 (Wagner et al. 2026) and Arabidopsis Arg176 (Kot et al. 2026, PDB 9GRR) are
  the same residue. No public blackgrass FatA sequence exists, so used wheat (Q8L6B1) as a Pooideae
  proxy. Result: Arabidopsis Arg176 aligns to wheat Arg103, not wheat position 171 — strong evidence
  these are different residues, not a small species-numbering offset. New reproducible script:
  `scripts/phase5_fat_numbering_check.py` (inputs: `data/raw/Q42561_AtFATA1.fasta`,
  `data/raw/Q8L6B1_TaFatA.fasta`). Updated `docs/PHASE5_FAT_DHODH_AUDIT.md`,
  `data/processed/phase5_risk_table.csv`, and `docs/VERIFICATION_LOG.md` accordingly. All Tier 4 items
  (4.1-4.8) are now closed for this audit pass.

- 2026-07-05 (q): Completed Phase 5 item 4.8 with primary-source verification (Claude Code). User
  supplied the Goggin et al. 2022 PDF (Pest Manag Sci, DOI 10.1002/ps.6947). Confirmed three real WA
  *Lolium rigidum* field populations (R1/R2/R3) show reduced cinmethylin sensitivity via enhanced
  P450-mediated metabolism (not a FAT target-site mutation), with resistance indices up to 8.0x
  (R2/R3 statistically significant on coleoptile elongation) and clear phorate-reversal mechanistic
  evidence. Replaced the single placeholder NTSR row in `data/processed/phase5_risk_table.csv` with
  three per-population rows carrying exact ED50/RI/p-value data. All three Phase 5 mutation-audit PDFs
  (Wagner et al. 2026, Kot et al. 2026, Goggin et al. 2022) are now archived in `docs/references/` and
  logged in `docs/VERIFICATION_LOG.md`. Remaining open item: 4.7 (R171 vs Arg176 sequence alignment,
  not yet run).

- 2026-07-05 (p): Completed Phase 5 items 4.3 and 4.4 with primary-source verification (Claude Code).
  User supplied two PDFs directly: Wagner et al. 2026 bioRxiv (FAT R171/H112Q/W173L engineered mutants,
  P192R FAT B) and Kot et al. 2026 (Arabidopsis FatA crystal structures incl. cinmethylin-bound 9GRR,
  verified against RCSB's data API). Also independently verified the DHODH mutation evidence (G198E,
  A141T — corrected from an earlier "A141V") from Kang et al. 2023 PNAS PMC full text, twice. Created
  `data/processed/phase5_risk_table.csv` to hold both targets' non-weed-evolved mutation evidence
  separately from the Phase 4 pooled table. Found and logged a real (non-target-site) cinmethylin
  resistance signal in field *Lolium rigidum* that the original audit draft had missed. Added items 4.7
  (FAT residue-numbering alignment, R171 vs Arg176, not yet confirmed) and 4.8 (Lolium metabolism paper
  full-text read, not yet obtained) as the next open items. Full detail in
  `docs/PHASE5_FAT_DHODH_AUDIT.md` and `docs/VERIFICATION_LOG.md`.

- 2026-07-05 (o): Reset presentation deliverables to the user-attached canonical deck at
  `output/presentations/herbicide_resistance_structural_bioinformatics_talk.pptx`, removed old generated
  presentation previews/assets, archived the attached handoff guide as `docs/PROJECT_HANDOFF_GUIDE.doc`,
  and created starter Phase 5 audit artifacts: `docs/PHASE5_FAT_DHODH_AUDIT.md` plus
  `data/processed/phase5_target_status.csv`. FAT remains first for mutation-source audit; DHODH remains
  gated behind mutation/model verification.

- 2026-07-05 (n): Refreshed the handoff/log layer for cross-agent continuation. Added the current
  Claude Code prompt above, updated `PROJECT_STATUS.md`, and recorded that `REPO_INDEX.md` is now the
  first navigation file for future agents. This is a docs-only continuation commit.

- 2026-07-05 (l): Designed the Phase 5 FAT/DHODH validation gate and committed
  `docs/superpowers/specs/2026-07-05-fat-dhodh-phase5-design.md` (`b92f5b0`). Structured RCSB/Crossref
  checks found plant FAT/acyl-ACP thioesterase structures (Lemna 8P8K/8QRT/8QS0 and Arabidopsis
  7HQQ-7HQU), while DHODH had 278 polymer entities across 273 RCSB entries but zero plant-like
  organisms. Decision: FAT-first audit; DHODH remains behind mutation/model verification; neither joins
  the Phase 4 pooled tables yet.

- 2026-07-05 (m): Added root `REPO_INDEX.md` and linked it from `README.md` (`a4100f2`) so a new
  agent can understand branches, commits, scripts, data, outputs, figures, tests, and future-work rules
  before touching code.

- 2026-07-05 (k): Completed the ACCase SWISS-MODEL follow-through. Downloaded the AJ310767 CT-domain
  1UYS homomer model (GMQE 0.76; QMEANDisCo global 0.72 ± 0.05), added
  `scripts/accase_swissmodel_distance_sasa.py`, generated
  `data/processed/accase_swissmodel_1uys_distance_sasa.csv`, switched Phase 4 ACCase joins to the
  weed-model coordinates (`A:143`, `B:389`, `B:403`, `B:440`, `B:450`, `B:458`), regenerated manuscript
  tables/figures, and updated the manuscript caveat: H1L was excluded by SWISS-MODEL, so the core is
  transferred from aligned 1UYS H1L-contact residues.

- 2026-07-05 (j): Prepared and committed the public AJ310767 ACCase CT-domain sequence for SWISS-MODEL
  (`data/raw/ACCase_Alopecurus_AJ310767_CTdomain_1639_2204.fasta`), verified it exactly matches
  AJ310767 residues 1639-2204, and started the SWISS-MODEL template search at
  `https://swissmodel.expasy.org/interactive/u3jF6Y/`. Search was still running during browser polling.

- 2026-07-05 (i): Completed Tier 3 item 3.1 by weaving published dynamic/docking/kinetic benchmarks
  into `docs/MANUSCRIPT_DRAFT.md` at sentence level. No generated tables changed. Remaining true
  pre-submission work: optional ACCase weed homology model (requires SWISS-MODEL/downloaded PDB) and
  Zenodo release at submission time.

- 2026-07-05 (h): Nakka et al. 2017 PDF supplied and verified (A. palmeri HPPD resistance = P450
  metabolism + 4-12x overexpression, no target-site mutation - confirms the HPPD contrast). Finalized
  as manuscript ref 20; PDF archived. All manuscript citations now verified except none outstanding.
  Committed.

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
