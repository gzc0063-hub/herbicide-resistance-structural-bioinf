# Phase 5 FAT/DHODH Emerging-Target Audit

Status: primary-source-verified audit (2026-07-05 update). Both target-site mutation
claims below have been read directly from the primary PDF text (not a secondary
summary) and cross-checked against RCSB's own data API for structures.

This note keeps Phase 5 as an evidence audit plus a separate **risk table**
(`data/processed/phase5_risk_table.csv`), not a pipeline integration. FAT and
DHODH should not be added to `scripts/build_phase4_tables.py`, the pooled
enrichment tests, or the manuscript tables until mutation evidence and
structure/model mapping pass the same gate used for PPO, ALS, EPSPS, ACCase,
and HPPD — and, critically, until a mutation is shown to be **weed-evolved**,
not engineered/predicted or lab-selected.

## Decision

Audit both targets is now substantially complete for the mutation-evidence
question. Neither target has a weed-evolved target-site mutation on record, so
neither qualifies for Phase 4 pooling. Both now have well-characterized
non-weed-evolved variants suitable for the separate Phase 5 risk table.

## FAT — findings

**Primary source:** Wagner, Lerchl, Betzt & Porri (2026), *Biochemical
Characterization of Fatty Acid Thioesterase Target Site Mutants and their
Implication on Herbicide Resistance*, bioRxiv, DOI `10.64898/2026.06.11.731613`
(bioRxiv's newer DOI prefix — confirm this resolves before final citation).
PDF archived at `docs/references/Wagner_et_al_2026_FAT_R171_biorxiv.pdf`.
**Not peer-reviewed** — a BASF-supervised bachelor thesis project (BASF
Agricultural Center, Limburgerhof, Germany), read in full from the actual PDF
text (extracted with `pypdf`, not a proxy/summary tool).

- FatA/FatB coding sequences are from **blackgrass (*Alopecurus myosuroides*)**,
  cross-checked against **Italian ryegrass (*Lolium multiflorum*)** (91.1%
  identity for FAT A, 93.2% for FAT B).
- 70 FAT A + 34 FAT B variants were screened. Candidate positions were chosen
  by **molecular docking simulation** (computational), then built as synthetic
  constructs and expressed in *E. coli* — **not observed in weed populations**.
  Assay: fluorescence-based acyl-CoA/CPM enzyme assay, dose-response IC50s via
  GraphPad Prism.
- **R171 is the standout FAT A position.** R171K: IC50 1.56e-5 M vs WT
  3.02e-8 M → resistance index **516.56**. R171Q/I/M showed no measurable IC50
  (too little residual inhibition to fit a curve) but only 10–24% inhibition
  at saturating cinmethylin. R171K requires **3 simultaneous nucleotide
  changes** from the wild-type codon (CGT → AAA or AAG); the paper's own
  conclusion is that this makes field evolution "extremely unlikely."
- Weaker but SNP-accessible hits: H112Q (RI 4.24, only **1** required
  nucleotide change — the paper flags this tension explicitly: the easy-to-evolve
  mutation is weak, the strong mutation is hard to evolve), W173L (RI 6.77, 2
  NPs).
- FAT B's largest shift is a **different position**, P192R (RI 9.76, 1–2 NPs) —
  the existing audit draft's focus on FAT A/R171 alone missed this.
- Full exact table (all IC50s, resistance indices, and NP-requirement codon
  paths) is now in `data/processed/phase5_risk_table.csv`.

**Real-world signal the earlier audit draft missed entirely — now fully
verified from the primary PDF (peer-reviewed, unlike the FAT preprint above):**
Goggin, Cawthray, Busi, Porri & Beckie (2022), *Enhanced production of
water-soluble cinmethylin metabolites by Lolium rigidum populations with
reduced cinmethylin sensitivity*, Pest Manag Sci, DOI `10.1002/ps.6947`. PDF
archived at `docs/references/Goggin_et_al_2022_Lolium_cinmethylin_metabolism.pdf`.
(Note the shared author, Aimone Porri/BASF, with the Wagner et al. FAT R171
preprint above — same research network on both sides of this question.)

- Three Western Australian field populations of **annual ryegrass (*Lolium
  rigidum*)** — R1 (Wickepin; field-collected, then given 2 rounds of
  sublethal-dose lab selection), R2 and R3 (Tammin; used directly from field
  screening, no further selection) — show reduced cinmethylin sensitivity vs
  a susceptible control (S). Resistance indices: R1 3.4x, R2 7.2x, R3 8.0x
  (soil survival basis, none statistically significant against S, n=3); on
  coleoptile elongation, R2 (2.7x, p=0.003) and R3 (3.2x, p=0.001) are
  statistically significant; R3 is also significant on radicle elongation
  (4.5x, p=0.043). The authors themselves caveat that these populations are
  "putatively" resistant, not officially confirmed.
- Mechanism: **enhanced P450-mediated oxidative metabolism**, not a target-site
  mutation. A specific water-soluble metabolite ("metabolite 4") correlates
  positively with resistance level; the P450 inhibitor phorate reverses this
  metabolite's production and synergizes cinmethylin's toxicity back toward
  susceptible levels — solid mechanistic evidence, not just correlation.
- This means cinmethylin resistance risk is **not purely hypothetical — it
  already exists in real field weed populations**, just not through the FAT
  active-site mechanism this repo's structural framework analyzes. It belongs
  in the Phase 5 risk table as a distinct, real, weed-evolved (or
  weed-derived-then-lab-selected, for R1) NTSR entry — clearly separate from
  the engineered FAT A/B target-site variants above.

**Structure — upgraded resource, verified directly against RCSB's data API:**
- `9GRR` = ***Arabidopsis thaliana* FatA bound to cinmethylin itself**
  (confirmed via `data.rcsb.org/rest/v1/core/entry/9GRR`) — Kot et al. 2026,
  *Crystal structure of fatty acid thioesterase A bound by 129 fragments*,
  Pest Manag Sci, DOI `10.1002/ps.70199`. PDF archived at
  `docs/references/Kot_et_al_2026_FatA_crystal_structure.pdf`. This is a better
  primary structural resource for cinmethylin specifically than the
  previously-cited Lemna entries.
- `9HRR` = same protein, apo state (confirmed).
- `7HQQ`–`7HQU` = FatA + XChem/Diamond Light Source PanDDA fragment-screening
  depositions (confirmed `7HQQ` = "Crystal Structure of FatA in complex with
  Z1198147845").
- `8P8K` (previously cited) is real but is ***Lemna aequinoctialis* FAT bound
  to a thiazolopyridine compound (X7C), not cinmethylin** — keep it as a
  secondary reference, not the lead citation.
- **Key residue naming question — now checked, and the answer is negative.**
  The crystal-structure paper calls the inhibitor-contact arginine **Arg176**
  (Arabidopsis, full-length precursor numbering including the 74-residue
  chloroplast transit peptide), while the resistance paper calls it **R171**
  (blackgrass numbering). No public *A. myosuroides* FatA sequence exists
  (checked NCBI protein/nuccore and UniProt directly — zero hits), so this was
  checked with wheat (*Triticum aestivum*, UniProt `Q8L6B1`) as a proxy —
  wheat and blackgrass are both Pooideae grasses, much closer to each other
  than either is to Arabidopsis. A global BLOSUM62 alignment (77.8% identity,
  `scripts/phase5_fat_numbering_check.py`, reproducible) shows Arabidopsis
  Arg176 aligns to **wheat Arg103**, not wheat position 171 (which is a
  threonine). Wheat's own UniProt numbering is already mature-protein
  (transit-peptide-excluded): 176 − 103 = 73, matching the 74-residue
  Arabidopsis transit peptide almost exactly. **Conclusion: if the blackgrass
  numbering in Wagner et al. 2026 follows the same mature-protein convention,
  R171 and Arg176 are most likely different residues, roughly 70 positions
  apart — not the same catalytic arginine at a small species offset.** This
  refutes the working hypothesis from the previous audit pass. Do not use
  9GRR's Arg176 to structurally contextualize R171 without first locating the
  actual blackgrass sequence Wagner et al. used (not deposited anywhere
  public) or otherwise confirming their numbering convention directly with
  the authors.

## DHODH — findings

**Primary source:** Kang et al. (2023), *A novel mechanism of herbicide action
through disruption of pyrimidine biosynthesis*, PNAS, DOI
`10.1073/pnas.2313197120`. Read directly from PMC full text (PMC10691210),
cross-checked twice independently for consistency.

- Solved a **rice (*Oryza sativa*) DHODH crystal structure bound to
  tetflupyrolimet** — a real plant structure exists, contradicting a
  literal reading of "no plant structure exists." **However, no PDB accession
  is given anywhere in the paper** — this reads as an internal/proprietary
  Syngenta structure, not a public RCSB deposition. Rat DHODH (PDB `1UUM`) was
  used only as a molecular-replacement search model, not deposited itself.
  Corrected framing: **no public plant DHODH structure**, not **no plant
  DHODH structure at all**.
- An **AlphaFold model of *Arabidopsis thaliana* DHODH (gene At5g23300)** was
  built and aligned to the internal rice structure for mutation mapping — also
  not stated as publicly available.
- Two independent **EMS (chemical) mutagenesis lines** in *Arabidopsis
  thaliana* (ecotype Landsberg erecta) — **lab-selected, not weed-evolved**:
  - Line **45R1**: **G198E** (nucleotide G593A, exon 4). Enzyme activity
    reduced ~290-fold vs WT. Re-created transgenically in WT plants, confirming
    causality.
  - Line **60R1**: **A141T** (nucleotide G421A, exon 3). Enzyme activity
    reduced ~140-fold vs WT. (An earlier secondary-source pass had this as
    "A141V" — the primary PMC text, read twice independently, confirms **A141T**.)
- Related but out-of-scope finding worth a documentation note: a 2026
  *Scientific Reports* paper (DOI `10.1038/s41598-026-43966-y`) reports
  tetflupyrolimet and the clinical antifungal drug olorofim share the DHODH
  mechanism, raising a cross-resistance concern in *Aspergillus* — not a weed
  target-site issue, but relevant to the target's broader biological stakes if
  DHODH is discussed further.

## Evidence Gate

No target can move from Phase 5 audit/risk-table to Phase 4 pooled analysis
until all of these are satisfied:

1. Target/MoA evidence is traceable to primary literature. — **met for both.**
2. Mutation evidence is traceable to a primary source. — **met for both** (FAT:
   engineered/computationally-guided; DHODH: EMS lab-selected).
3. The mutation is classified as weed-evolved, lab-selected, engineered, or
   hypothetical. — **classified: FAT R171/H112Q/W173L/P192R = engineered/
   predicted; DHODH G198E/A141T = lab-selected (EMS). Neither is weed-evolved.**
4. Species, exact substitution, sequence/accession or coordinate reference, and
   residue-numbering system are recorded. — **met**, see
   `data/processed/phase5_risk_table.csv`.
5. A structure or model maps the residue into the target's structural frame.
   — **FAT: 9GRR maps Arg176 in Arabidopsis, but a wheat-proxy alignment check
   found this is most likely NOT the same residue as blackgrass R171 — so
   9GRR does not currently map the R171 finding into a structural frame.
   DHODH: internal rice structure exists but is not public; AlphaFold AtDHODH
   model also not public.**
6. The limitation statement is clear enough that the project does not overclaim
   resistance mechanism, field evolution, or structural certainty. — this file
   plus `phase5_risk_table.csv`'s `confidence`/`notes` columns carry that.

**Conclusion: still `audit_first` for FAT and `hold_model_source` for DHODH**
with respect to Phase 4 pooling — but both now have a populated, citable Phase 5
risk table entry, which is the appropriate destination for non-weed-evolved
target-site evidence.

## Target Status

| Target | Current status | Go/no-go |
|---|---|---|
| FAT/acyl-ACP thioesterase | Weed genome sequence used; mutations engineered/docking-predicted, not weed-observed. Structure available and cinmethylin-bound (Arabidopsis, 9GRR); species-numbering offset to blackgrass not yet resolved. Separate real NTSR (metabolic) resistance exists in *Lolium rigidum*. | `audit_first` |
| DHODH | Mutation evidence now verified (EMS lab lines, Arabidopsis) but not weed-evolved. A real plant (rice) structure exists but is not publicly deposited; AlphaFold AtDHODH model also internal only. | `hold_model_source` |

## Do Not Do Yet

- Do not add FAT or DHODH rows to the Phase 4 pooled mutation table.
- Do not add FAT or DHODH to the cross-family enrichment analysis.
- Do not describe any of the FAT or DHODH variants above as weed-evolved TSR —
  all are engineered/predicted (FAT) or lab-selected via EMS (DHODH).
- Do not claim a public plant DHODH structure — the rice structure and the
  AlphaFold AtDHODH model in Kang et al. 2023 are not stated as publicly
  deposited anywhere in the paper.
- Do not treat R171 (blackgrass) and Arg176 (Arabidopsis) as the same aligned
  residue in any figure or structural discussion — the wheat-proxy alignment
  check found they most likely are not (see above).

## Open items for a future pass

- Confirm the bioRxiv DOI (`10.64898/2026.06.11.731613`) resolves cleanly
  through doi.org before using it in the manuscript reference list.
- If the actual *A. myosuroides* FatA construct sequence from Wagner et al.
  2026 ever becomes available (e.g. via correspondence with the authors or a
  future deposition), re-run `scripts/phase5_fat_numbering_check.py` against
  it directly rather than the wheat proxy used here.
