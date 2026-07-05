# Senior Review — Cross-SOA Structural Bioinformatics of Herbicide Target-Site Resistance

Reviewer stance: senior structural bioinformatician + weed scientist + skeptical manuscript referee.
Scope of this pass: all MD files, the pooled Phase 4 data, the permutation code, the manuscript draft,
and independent re-verification of the EPSPS source (Baerson et al. 2002, read in full this session).
Date: 2026-07-05.

---

## 1. Overall verdict

**This is a genuinely well-curated, unusually honest descriptive resource that is *not yet* a
publishable finding paper — because its headline result is the one thing the project's own Phase 0
panel review explicitly warned would read as "a descriptive database, not a finding."**

- **Curation rigor: 8.5/10.** Accession provenance, primary-source verification, refusal to infer
  accessions, unpublished-source flagging, and the HPPD "we found no target-site mutation, so we say so"
  contrast case are all better than most published weed-resistance bioinformatics papers.
- **Statistical / structural rigor of the central claim: 4/10 as currently framed.** The enrichment
  result is real but semi-expected, underpowered (13 unique positions across 4 families; ALS n=2,
  EPSPS n=1), and rests on cross-species template mappings that at several key positions are not even
  the same amino acid.
- **Honesty of the writing: 9/10.** The manuscript pre-empts most criticisms in its own Limitations
  section. That is a real asset — but a reviewer will still act on the substance, not the disclaimer.

**Publishability today:** ~5/10 as a resource paper (PeerJ / Frontiers in Plant Science tier), *if*
the structural-mapping caveats below are moved from footnotes into the analysis itself. As a
finding/mechanistic paper (JAFC / Pest Management Science / Plant Physiology): not yet.

---

## 2. What is genuinely strong (keep, do not weaken)

1. **Source-verification discipline.** Every accepted mutation is traced to primary text, not a
   secondary citation. The V361A accession correction, the Giacomini "no accessions exist" full-text
   confirmation, the Larran Table-4 wild-type resolution, and the Yu-2007 EF538937-943 pairing are all
   defensible under referee scrutiny. **EPSPS Pro106Ser is now independently confirmed against the
   Baerson 2002 PDF this session:** four SNPs, two amino-acid changes, second change (position 382)
   kinetically shown non-causal, Pro106Ser corresponds to the *Salmonella* glyphosate-insensitive EPSPS
   substitution. This matches the dataset row exactly.
2. **HPPD as a declared negative/contrast family.** Refusing to fabricate an HPPD target-site row (and
   avoiding the "Gly336" *Pseudomonas* engineering-variant trap) is exactly right and is a credibility
   asset. Foreground it more, not less.
3. **Within-family percentile normalization + permutation design.** This is the correct answer to the
   panel's cross-enzyme-comparability and pseudoreplication concerns. The empirical p-value uses the
   proper `(k+1)/(n+1)` estimator and a fixed seed. Mechanics are sound.
4. **The static-vs-dynamic scope boundary is stated repeatedly and correctly.** Good.
5. **RSA (Tien 2013) normalization and dedup-to-unique-position** were added — both were outstanding
   items from the external review and are now done.

---

## 3. What is wrong or weak — by severity, with the science

### 3.1 CRITICAL — The central claim is the "expected" result, not the "citable" one

The project's own **panel review (DECISION_LOG §2, fix #5)** said in writing: *"'Mutations cluster near
the active site' is expected, not surprising — weak central claim... hunt for and foreground outlier
mutations."* The current manuscript's headline result (Table 1, Figure 2) is precisely
"accepted TSR positions are enriched near active-site cores" (p = 0.0002–0.0022). That is the expected
finding. For the direct-core positions it is close to tautological: the core is *defined* by ligand
contact, and those residues (PPO R98, ALS Trp574/Ser653, ACCase Ile1781/Ile2041) sit at distance 0 by
construction, so a low percentile is guaranteed, not discovered.

**Why it matters:** a skeptical referee will write "the enrichment analysis largely re-derives that
known target-site mutations are in or near the binding pocket, which is the definition of target-site
resistance." The genuinely novel material — the *outliers* (ΔG210, V361A, Cys2088Arg, Pro106Ser as a
non-contact position) — is present in Table 2 but is treated as secondary color, not the thesis.

**What to do:** invert the framing. Make the **outlier/non-core positions the central object** and the
enrichment the expected-baseline control. The paper's real contribution is a *typology*: direct-core vs
adjacent vs deletion-linked vs interface vs "close-but-not-contact." Lead with that. This is a
reframing, not new computation.

### 3.2 CRITICAL — Cross-species template residue-identity mismatches (worst in ACCase)

The static metrics are computed on the mapped structure residue, but at several key positions that
residue is **not the same amino acid as the weed residue**, because the template is a distantly related
ortholog:

| Family | Mutation | Weed WT | Yeast/template residue at mapped position | Problem |
|---|---|---|---|---|
| ACCase | Ile1781Leu | Ile | **LEU** | Template already carries the *resistant* residue (yeast is naturally APP-tolerant — Délye 2005 says exactly this) |
| ACCase | Ile2041Asn | Ile | **VAL** | Different residue; SASA/side-chain context is not the weed's |
| ACCase | Cys2088Arg | Cys | **MSE (Met)** | Different residue (Délye Table III: yeast has Met here) |
| ACCase | Gly2096Ala | Gly | **ALA** | Template carries the *resistant* residue (Délye: yeast Ala2096, "as in a resistant black-grass mutant") |

So four of six ACCase positions are mapped onto a residue that differs from the weed's, and **two of
them the template already displays the resistance-conferring amino acid.** Distance-to-CA-core is
relatively robust to this (backbone geometry is conserved at 55% identity), but **SASA and any
side-chain/pocket interpretation are not** — the reported ACCase SASA/RSA values describe yeast side
chains, not weed side chains. Délye et al. 2005 themselves flag yeast as non-identical *at the very
positions of interest*.

**Why it matters:** an ACCase referee will catch this in one read. It does not invalidate the distance
percentile (the position is real), but it undermines the SASA/RSA column for ACCase and forbids any
side-chain-level claim from the yeast template.

**What to do (in order of preference):**
1. **Best:** build a homology model of the black-grass/*Lolium* CT domain on 1UYS (SWISS-MODEL, exactly
   what Délye did) and compute metrics on the *weed* sequence, or use a plant ACCase structure if one
   now exists (check the PDB — grass plastidic ACCase structures may have been deposited since 2005).
2. **Acceptable minimum:** restrict ACCase to **distance percentile only**, explicitly drop SASA/RSA
   claims for ACCase, and add a prominent per-position "template residue identity vs weed residue" column
   to Table 2 so the mismatch is visible, not buried in a notes field.
3. Either way, add a `template_matches_weed_residue` boolean to the master table for **every** family.

### 3.3 MAJOR — Statistical power and the ALS/EPSPS single-digit n

- EPSPS: n=1 (p=0.13, correctly non-significant). Fine to report as a mapped case study; **do not** put
  it in a "family enrichment" figure panel as if it were a test.
- ALS: n=2, p=0.0022. A two-point permutation p-value is fragile and will draw fire. The dataset itself
  says Ala122/Pro197/Asp376 are documented ALS TSR positions that were scoped out. **Expand ALS to the
  full accepted set before submission** (the manuscript's own Limitations already concedes this). That
  single change moves ALS from "n=2 curiosity" to a credible family test and is high-value.
- Across all four families there are ~13 unique positions. Report this honestly as a **descriptive
  resource with per-family enrichment as supporting evidence**, and add a **multiple-comparison note**
  (4 family tests; even a Bonferroni-trivial mention shows statistical self-awareness).

### 3.4 MAJOR — Mechanism labels overreach at two places

- **EPSPS Pro106Ser labeled `allosteric_hinge`.** This is a static-artifact-driven label. Pro106
  (Pro101 in *E. coli*, Pro106 mature-plant numbering) is a well-established **glyphosate-binding-site-
  associated** residue — Baerson explicitly ties it to the *Salmonella* glyphosate-insensitive EPSPS
  substitution, and it reduces glyphosate affinity while sparing PEP binding. Its 3.85 Å CA distance
  (just outside the 4.5 Å *atomic*-contact core) is a threshold artifact of a CA-based cutoff, **not**
  evidence of allostery. Calling it "allosteric/hinge" is exactly the overinterpretation the paper's
  own scope boundary forbids. **Relabel: `adjacent / binding-site-associated (second shell)`.**
- **All six ACCase positions labeled `interface_induced_fit`.** The CT dimer-interface framing is
  correct structurally, but a single uniform label flattens distinctions Délye 2005 *measured*:
  1781 and 2078 confer APP+CHD resistance; 2027/2041/2096 are APP-only; 2027 and 2078 also *reduce
  catalytic activity* (polar-core residues). Carry those biochemical distinctions into the mechanism
  annotation instead of one blanket label.

### 3.5 MODERATE — Semi-circularity of the enrichment for direct-core positions

Because the active-site core is ligand-defined and several accepted positions *are* core residues
(distance 0), the enrichment is partly built-in. The permutation test is still valid (random residues
can also be core), but the honest interpretation is "known pocket mutations are in the pocket." **Fix:**
run the enrichment **excluding in-core positions** (i.e., test only whether the *non-core* accepted
positions are still closer than random). If the adjacent/second-shell positions remain enriched after
removing the guaranteed-zero core residues, *that* is a real, non-tautological result worth leading with.

### 3.6 MINOR — data-quality and reproducibility polish

- **Negative SASA/RSA values** (`-1.1e-13`, `rsa_tien2013 = -0.000000`) are floating-point noise for
  fully buried residues. Clamp to 0 before writing; negative accessibility in a manuscript table looks
  sloppy to a referee.
- **EPSPS `source_doi = not_in_pubmed_metadata`.** The DOI is **10.1104/pp.001560** (verified this
  session). Fill it in.
- **ACCase five-of-six positions were computed in the parallel (Codex) ChimeraX run and have not been
  re-executed in this environment.** Cys2088Arg cross-checks (2088→2014, and the independent Claude run
  agreed), but re-run the ACCase pipeline end-to-end once in one environment so all numbers come from a
  single reproducible pass before submission.
- **A `tests/` suite exists** (good) — state in Methods that outputs are unit-tested; referees like that.
- Confirm every figure SVG regenerates from the committed tables via a single `make`/script (Phase 5
  reproducibility requirement).

---

## 4. Path to publication — prioritized, science-based

**Tier 1 (do before any submission — these are correctness/credibility, not polish):**
1. Add `template_residue`, `weed_residue`, and `template_matches_weed_residue` columns to the master
   table for all families; drop or homology-model the ACCase SASA/RSA where they mismatch (§3.2).
2. Relabel EPSPS Pro106Ser (§3.4) and de-uniform the ACCase mechanism labels (§3.4).
3. Re-run the enrichment excluding in-core positions and report both versions (§3.5).
4. Fill the EPSPS DOI, clamp negative SASA/RSA, re-run ACCase in one environment (§3.6).

**Tier 2 (turns a resource into a finding):**
5. **Reframe around the outlier typology** (§3.1): ΔG210 (deletion/helix), V361A (permissive,
   low-conservation), Cys2088Arg (distal interface), Pro106Ser (binding-site-adjacent) as the paper's
   core intellectual content; enrichment demoted to expected-baseline control.
6. **Expand ALS** to Ala122/Pro197/Asp376 (§3.3) — biggest single power gain, and the sequences/
   structure are already in hand.
7. Add a short **per-family "resistance-zone map" figure** (one structure cartoon per family with the
   accepted positions colored by proximity class). This is what a Pest Management Science reader wants
   and is more compelling than the current percentile scatter.

**Tier 3 (optional depth / higher-tier journals):**
8. For 2–3 flagship positions, add **published docking/MD as an interpretation benchmark** (already the
   stated method) with sentence-level citations — pushes toward JAFC-tier.
9. FAT/DHODH: keep as declared future work unless a public plant structure exists; verify the DHODH
   plant co-crystal (Kang et al. 2023, PNAS) PDB accession before promising it.
10. Zenodo deposit + `CITATION.cff` + pinned environment for the data-availability requirement.

**Journal targeting:** PeerJ or Frontiers in Plant Science as the honest first home for a reproducible
descriptive resource. Pest Management Science becomes realistic *if* Tier 2 (outlier reframing + ALS
expansion) is done. Plant Physiology / JAFC only with added functional or docking depth (Tier 3).

---

## 5. Tools / connectors that would help (and gaps)

- **scite (already connected):** keep using it for sentence-level citation verification during the
  "convert names to citations" to-do. It is well-suited to the "audit dynamic-mechanism claims against
  PDFs" task in the manuscript's own to-do list.
- **A PDB/RCSB or UniProt data connector** (not currently connected): would let structure/accession
  checks be scripted rather than done by ad-hoc `curl`. Worth adding for Phase 5 reproducibility.
- **SWISS-MODEL / homology-modeling** is the key missing capability for §3.2 (weed-sequence ACCase
  model). This is a web tool; it can be run by hand and the model committed, mirroring the ColabFold
  workflow already planned for FAT/DHODH.
- A **workflow-runner MCP** appears available in this session; only worth wiring up if you want the
  whole pipeline (fetch → align → metric → permute → figure) to run as one reproducible DAG for the
  Zenodo release. Optional, not required for the science.
- No connector replaces the two human/lab dependencies: (a) a homology model or plant ACCase structure,
  and (b) domain sign-off on the ALS expansion set.

---

## 6. One-paragraph summary for the cover note

The resource is honestly built and unusually well-verified, and the HPPD contrast case plus the
source-provenance discipline are real strengths. The blocking issues before publication are scientific,
not cosmetic: (1) the headline "enrichment near the active site" is the expected result the project's
own design review flagged as weak, so the paper should be reframed around the outlier typology it
already contains; (2) several ACCase positions are mapped onto a yeast template residue that differs
from the weed residue — two of them the template already carries the resistant amino acid — so ACCase
side-chain metrics (SASA/RSA) must be homology-modeled on the weed sequence or dropped; (3) ALS (n=2)
and EPSPS (n=1) are underpowered and ALS should be expanded to its full accepted set; and (4) two
mechanism labels (EPSPS "allosteric," uniform ACCase "interface") overreach the static evidence. None
of these require abandoning the approach — they require moving the caveats from the footnotes into the
analysis and leading with the genuinely novel outlier story.
