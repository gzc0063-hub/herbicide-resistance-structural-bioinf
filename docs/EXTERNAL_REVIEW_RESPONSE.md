# Response to external "senior review" (compass_artifact, supplied by user)

## What this review actually is

The review's own text states it plainly: **the reviewer could not access our
GitHub repo** (404 on the web page, raw endpoints, and the API - meaning the repo
is private, which it is). It says explicitly: *"I therefore cannot verify the
actual contents of DECISION_LOG.md, PROJECT_STATUS.md, VERIFICATION_LOG.md,
scripts, or data — this review verifies the scientific claims described in the
task against primary sources."*

So this is **not** a review of our actual PPO/ALS work. It's a fact-check of some
*other* task brief/plan for ACCase, EPSPS, HPPD, FAT, and DHODH - enzymes we have
not started yet. Most of its specific claims (1UYS citation, "Gly336", 1G6S,
AJ310767) are about that plan, not our repo. Below: what genuinely applies to our
completed work (confirmed by direct re-checking, not taken on faith), and what to
carry forward into the enzymes we haven't built yet.

## Part 1 — What applied to our COMPLETED work (PPO, ALS), checked directly

### Confirmed and fixed: ALS active-site core was missing dimer-interface residues

The review's general point ("ALS/AHAS binding is at the dimer interface, not
solely the catalytic pocket, per McCourt et al. 2006") was **checked directly
against our own 1Z8N structure, not taken on the review's word**, and it held up:

- Generated the biological tetramer and searched for cross-chain contacts to
  either bound imazaquin copy.
- First attempt produced identical "distances" across three different symmetry
  copies - an obvious bug, traced to comparing atoms in different models' local
  coordinate frames without applying each copy's position transform
  (`atom.coord` vs `atom.scene_coord` in ChimeraX's API).
- Corrected check found **11 real interface residues** contributed by a
  neighboring subunit (121, 122, 168, 195, 196, 197, 199, 200, 206, 207, 256),
  missing from the original 16-residue chain-A-only core.
- **Ala122 and Pro197** - two classically-documented ALS resistance positions we
  had deliberately excluded from pilot scope (DECISION_LOG #12, to avoid scope
  creep) - are themselves genuine interface pocket residues. This doesn't mean the
  scope decision was wrong (it was made for legitimate reasons and still stands),
  but it explains mechanistically why those positions are real resistance hotspots,
  and means a fuller ALS pass revisiting them should use the corrected core.

**Fixed:** `scripts/chimerax_als_distance_sasa.py` now includes all 27 core
residues; `als_1z8n_distance_sasa.csv` and `als_validation_gate_results.md` are
recomputed. **The Trp574Leu/Ser653Asn conclusion is unchanged** - both remain
direct ligand-contact core members, fully conserved - only the secondary
"distance to nearest other core residue" percentiles shifted (22.0→31.8,
1.7→3.1). The SASA calculation was never affected - ChimeraX's own `measure sasa`
command already handles the biological assembly geometry correctly; the bug was
in a manual diagnostic script, not the actual pipeline's SASA step.

### Valid, not yet applied: raw SASA vs relative solvent accessibility (RSA)

The review's point stands: reporting raw Å² SASA isn't directly comparable across
residues of different sizes, let alone across enzymes. The rigorous standard is
**RSA = per-residue SASA ÷ that residue type's maximum possible SASA** (Tien et
al. 2013, *PLoS ONE* 8(11):e80635, DOI 10.1371/journal.pone.0080635), with
"exposed" conventionally RSA ≥ 0.25.

**Status: not yet applied to PPO or ALS.** Both used raw Å² SASA throughout. This
doesn't invalidate anything already concluded (R98's exposure and the general
buried/exposed calls for PPO's four mutations were all directionally clear-cut,
not borderline calls where a normalization would flip the conclusion), but it
should be adopted **before Phase 4's cross-enzyme synthesis**, where comparing
SASA values across enzymes with different residue-size distributions genuinely
requires it. Retrofitting PPO/ALS's existing SASA columns with RSA is cheap (just
divide by Tien et al.'s max-SASA table) and should happen before that phase.

### Not applicable / no action needed

Everything else in the review (1UYS citation, AJ310767, EF538937-943, 1G6S,
"Gly336", FAT/DHODH identity) concerns enzymes not yet started in this repo. See
Part 2 for what to carry forward.

## Part 2 — What to adopt when building ACCase, EPSPS, HPPD (next per DECISION_LOG #16)

### ACCase

- **Numbering reference:** AJ310767 (*Alopecurus myosuroides*/black-grass
  plastidic ACCase) is the genuine field-standard, used by Délye et al. 2005 and
  downstream literature. Legitimate to adopt directly.
- **Real, peer-reviewed accessions:** EF538937-EF538943, from Yu, Collavo, Zheng,
  Owen, Sattin & Powles (2007), *Plant Physiol.* 145(2):547-558, DOI
  10.1104/pp.107.105262 - documents Cys2088Arg in *Lolium*, CAPS-validated.
  **Caveat carried forward: these are partial CDS (sequenced CT-domain region
  only), not full-length** - note this explicitly if used, the same way PPO's
  partial-vs-full-length distinctions were tracked.
- **Structure: 1UYS** (yeast *S. cerevisiae* ACC carboxyltransferase domain +
  haloxyfop). **Correct citation to use from the start: Zhang H, Tweel B, Tong L
  (2004), "Molecular basis for the inhibition of the carboxyltransferase domain
  of acetyl-coenzyme-A carboxylase by haloxyfop and diclofop," *PNAS*
  101(16):5910-5915, DOI 10.1073/pnas.0400891101.** (Not "Science 2004" / "Yang,
  Chun" - whatever citation appeared in the reviewed brief was wrong; make sure
  it's never introduced into our own repo.)
- **Critical structural note - verify before building, don't assume:** the
  haloxyfop site sits at the CT-domain dimer interface, per the review's citation
  of the structure's own description. **Before defining the active-site core for
  ACCase, repeat exactly the cross-chain contact check just done for ALS** -
  generate the biological assembly, check for interface contacts using scene
  coordinates, don't assume a single-chain core is complete. Also confirm the
  correct biological dimer chains (A+B, or another pairing) from RCSB's actual
  assembly record for 1UYS directly - don't take the review's "B+C" guess at
  face value either; it flagged this itself as unconfirmed.
- **Numbering offset:** yeast vs. black-grass numbering will need an alignment-
  derived offset table, exactly like PPO's `numbering_maps.json` - Délye 2005
  itself notes Gly2096 is conserved in all ACCases except yeast (which has Ala
  there), a concrete reminder the template isn't identical at the positions of
  interest.

### EPSPS

- **Don't default to 1G6S (*E. coli*) without deciding explicitly.** Mapping
  plant Pro106Ser onto a bacterial numbering scheme needs a documented alignment
  and offset, the same rigor as everything else in this project. Check whether a
  genuine plant EPSPS crystal structure (e.g., an *Arabidopsis* EPSPS structure)
  exists and is a better numbering-fidelity choice before committing to 1G6S.
- **Conformational state matters:** glyphosate binds only the closed
  (shikimate-3-phosphate-bound) conformation. Confirm which conformation any
  candidate structure is in before computing distances - an open-conformation
  structure would give meaningless numbers for this specific mechanism.

### HPPD — the most important correction to internalize before starting

**Do not use "Gly336" as an HPPD weed resistance mutation.** Per the review: this
is an **engineered *Pseudomonas fluorescens* HPPD variant** used for crop
tolerance (FG72 soybean), not something that evolved in a resistant weed
population. This is exactly the kind of mistake this project's own verification
discipline exists to catch - the same category of error as the original
QBB0236x/unpublished-GenBank issues in Phase 1, just caught before it happened
rather than after.

**The actual biology, which changes the shape of this pilot:** documented HPPD
resistance in *Amaranthus palmeri* and waterhemp is predominantly **non-target-site**
- cytochrome P450 metabolic detoxification (CYP72A219, CYP81B, CYP81E8,
CYP72A1182) plus HPPD gene amplification/overexpression - **not** a target-site
point mutation. Per the review, Nakka et al. 2017 sequenced the entire HPPD gene
in resistant Palmer amaranth and found no causal target-site substitution and no
amplification in their material, attributing resistance to P450-mediated
mesotrione metabolism.

**Recommended plan for HPPD, to verify ourselves before locking in:** don't force
this enzyme into the same "find a weed target-site mutation, build the
validation gate" shape as PPO/ALS. Instead:
1. Search independently (don't take the review's "essentially absent" as final)
   for any genuinely peer-reviewed, accession-backed weed HPPD target-site
   mutation published since - the field moves fast, and this project's standard
   has been to verify from primary text, not accept a secondary claim, in either
   direction.
2. If none exists, frame the HPPD chapter as a **substrate/inhibitor-contact
   structural analysis** (Fe(II)-coordinating His/His/Glu triad, the two
   π-stacking Phe residues, the pocket around a bound triketone/benzoylpyrazole
   inhibitor or the natural substrate HPPA) rather than a resistance-mutation
   validation gate - and state plainly in any manuscript that evolved HPPD
   resistance in these weeds is non-target-site, contrasting with the
   target-site-rich PPO/ALS/ACCase/EPSPS chapters. This is a legitimate,
   citable framing, not a weaker one.
- **Structure candidates to verify (not yet confirmed by us):** the review lists
  *Arabidopsis* 1TG5/1SP9/1SQD/1TFZ, maize 1SP8, and 5YWG (HPPA-bound). It also
  flags that **"human 1SQD" would be wrong** - 1SQD is *Arabidopsis* (UniProt
  P93836); human HPPD is 3ISQ, rat is 1SQI. Confirm all of these directly on
  RCSB before use, the same way every PDB ID in this project has been verified
  by direct download rather than assumed from a citation.

### FAT and DHODH (Phase 3)

- **FAT = acyl-ACP thioesterase** (HRAC Group 30; target of cinmethylin,
  methiozolin), **not** mammalian cytosolic thioesterase and **not** FabB/FabF.
  Worth confirming this identity ourselves before searching for structures,
  given how easy a name collision like this is to get wrong.
- **DHODH = dihydroorotate dehydrogenase**, target of tetflupyrolimet (Kang,
  Emptage, Kim & Gutteridge 2023, *PNAS* 120(48):e2313197120, DOI
  10.1073/pnas.2313197120), which reportedly includes a **plant DHODH co-crystal
  structure** with inhibitor bound at the ubiquinone site.
- **Action before assuming Phase 3 still needs ColabFold for DHODH:** if that
  2023 PNAS paper's plant DHODH structure is actually deposited in the PDB with a
  public accession, **Phase 3 may not need a ColabFold prediction for DHODH at
  all** - check this directly (RCSB search, or the paper itself) before doing any
  Colab work. FAT's status is less clear (the review mentions a 2024 bioRxiv
  fragment-screen co-crystal but flags its PDB codes as unconfirmed) - verify
  independently rather than assuming either way.

### Cross-enzyme synthesis (Phase 4) - reinforces, doesn't change, the existing plan

The review's recommended statistics approach (within-structure percentile-rank
or z-score normalization; enzyme as a random/blocking effect in a mixed model;
resistance residues vs. a matched null set via permutation test; avoid
pseudoreplication from multiple mutations at one position or multiple PDBs of one
enzyme) **matches what the original panel review already specified**
(DECISION_LOG #2) and what this project has followed throughout. No change of
direction needed here - just a reminder to actually build it that way when Phase
4 starts, and to add RSA normalization (Part 1) alongside the existing
percentile-rank distance normalization.

## Part 3 — Not urgent right now

The review flags repo privacy as a blocking problem for "data availability."
**Correct, but only relevant at Phase 5 (deposit/submit)**, not during active
development - per DECISION_LOG #12 background context, the repo was
deliberately made private pre-publication. No action needed now; revisit before
submission.
