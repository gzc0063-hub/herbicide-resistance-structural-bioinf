# Independent verification log

This file records checks I (Claude Code) ran against primary sources before treating
`data/processed/PPO_Phase1_Final_Validated_Brief.md` as ground truth for the pipeline.
Not a substitute for `docs/DECISION_LOG.md` — that's the human decision record; this is
the machine-side spot-check that happened before building on top of it.

## Accession existence checks (NCBI, live query)

Confirmed all real and matching claimed species/isolate/gene:
- MH910646.1, MH910647.1 — *A. palmeri* IN/AL isolates, mitochondrial PPO mRNA (V361A pair)
- MK408971.1, MK408972.1, MK408978.1 — *A. palmeri* genotypes R1/R2/S3, PPX2L mRNA (G399A set)

## Citation identity checks (scite literature search, cross-checked by title + author + journal + year filters independently)

- DOI 10.1002/ps.4581 → "Two new PPX2 mutations associated with resistance to
  PPO-inhibiting herbicides in *Amaranthus palmeri*" — Pest Management Science,
  author filter "Giacomini" matches. Confirms brief's Giacomini et al. 2017 / R98G,R98M attribution.
- DOI 10.3389/fpls.2019.00568 → "A Novel Single-Site Mutation in the Catalytic
  Domain of Protoporphyrinogen Oxidase IX (PPO)..." — Frontiers in Plant Science,
  2019, author filter "Rangani" matches. Confirms brief's Rangani et al. 2019 / G399A attribution.
- Both DOIs resolve and match the brief's journal/author assignment — **the
  citation-mixup correction recorded in DECISION_LOG.md #4 is confirmed correct**,
  not a re-introduced error.

## Primary-source full-text check — Dayan et al. 2010 (PDF supplied directly by user, saved to `docs/references/Dayan_et_al_2010_PPO_Gly210_deletion.pdf`)

Confirmed against the actual paper text:
- Cavity volume 551 Å³ (S-PPO) → 848 Å³ (R-PPO) — exact match
- Gly207-carbonyl-to-FAD-N5 distance +1.5 Å average (S-PPO 6–8 Å, R-PPO 7–9 Å clusters) — exact match
- Km unchanged ~1 μM both — exact match (Table 1)
- Vmax/kcat ~10-fold lower in R-PPO — exact match (Table 1)
- Inhibition type competitive → mixed — exact match (Table 1)
- FAD content unchanged (0.27 vs 0.28 OD450) — exact match
- Accessions ABD52329 (S-PPO) / ABD52330 (R-PPO) used directly in Dayan's own Methods — exact match, confirms brief's claim word-for-word
- Hao et al. 2009 critique (mutant model not relaxed before docking; assumed competitive inhibition without testing) — confirmed nearly verbatim in Discussion section
- Evolutionary deletion-vs-substitution argument, including the exact steric-clash residue list (Phe467, Val360, Pro361, Leu362, Gly422, Gly423, Phe420) and the AF273767 Ala-in-sensitive-species point — exact match
- Heinemann et al. 2007 citation (Biochem J 402:575-580) — journal/volume/pages confirmed via Dayan's own reference list [6]

**One correction found:** the brief states "Ki 100–500-fold higher in resistant."
The paper's actual Ki fold-changes are ~10–55× (e.g. lactofen 0.009→0.50 μM ≈ 55×).
The 100–500× figure in the paper describes **I50** ("R-PPO was 100 to 500 times less
sensitive"), not Ki. Both are real findings in the paper — just attributed to the
wrong parameter in the brief. Use I50 fold-change for the "100–500×" claim, Ki
fold-change (~10–55×) if citing Ki specifically.

## Primary-source full-text check — Hao et al. 2009 (PDF supplied by user, saved to `docs/references/Hao_et_al_2009_PPO_Gly210_computational.pdf`)

- **Confirmed directly from the paper's own abstract:** "An interchain hydrogen bond
  between Gly210 with Ser424... disappeared after Gly210 deletion." Matches the
  brief's claim exactly — no longer just Dayan 2010's secondhand summary of it.
- Confirmed: purely computational study (homology modeling, MD, MM-PBSA), no
  wet-lab kinetics — matches the brief's characterization used to justify weighting
  Dayan 2010 as the primary account.

## Primary-source full-text check — Giacomini et al. 2017 (PDF supplied by user, saved to `docs/references/Giacomini_et_al_2017_R98G_R98M.pdf`)

- Confirmed: R98G and R98M mutations, DOI 10.1002/ps.4581, Pest Manag Sci 73:1559-1563.
- **No GenBank accession numbers appear anywhere in the full text**, including
  References and Acknowledgements — this was a full read, not just a visible-text
  search, so the "open item" status in the brief is now confirmed rather than assumed.
  Sequencing was cDNA from individual plants (Table 1: populations GPW/LPW/SPW
  resistant, KPW sensitive, per-plant genotype calls), not deposited full-length
  sequences with accessions.
- Confirmed verbatim: R98L (a related but distinct substitution at the homologous
  site) belongs to *Ambrosia artemisiifolia* (common ragweed), not *Amaranthus* —
  matches DECISION_LOG's nomenclature correction exactly.

## Primary-source full-text check — Wagner et al. 2026 FAT R171 preprint (PDF supplied by user, saved to `docs/references/Wagner_et_al_2026_FAT_R171_biorxiv.pdf`)

- bioRxiv DOI as given by both the search index and Europe PMC:
  `10.64898/2026.06.11.731613` (bioRxiv's newer DOI prefix, not the legacy
  `10.1101` — confirm it resolves via doi.org before final manuscript citation).
  Europe PMC record (`PPR1252330`) independently confirms title, authors
  (Wagner P, Lerchl J, Betzt M, Porri A), and abstract verbatim — cross-checked
  before the PDF arrived, then confirmed again against the PDF's own text.
- Full text extracted directly with `pypdf` (not a summarization tool) and read
  page-by-page. Confirms exactly: FAT A/B sequences from *Alopecurus
  myosuroides*, cross-checked against *Lolium multiflorum*; 70 FAT A + 34 FAT B
  variants screened; candidate positions chosen by molecular docking simulation
  (computational), built as synthetic constructs, expressed in *E. coli*, tested
  with a fluorescence acyl-CoA/CPM assay.
- Table 3 read directly: R171K IC50 1.56×10⁻⁵ M (WT 3.02×10⁻⁸ M), resistance
  index 516.56, 60.87% residual activity, 56.56% inhibition at saturation.
  R171Q/I/M: no measurable IC50, 24.32%/15.53%/10.96% inhibition respectively.
  H112Q RI 4.24 (1 nucleotide polymorphism required — the paper's own tension
  point: easiest-to-evolve mutation is the weakest). FAT B's largest shift is
  P192R (RI 9.76), a different position from FAT A's R171 — the original audit
  draft only mentioned FAT A/R171 and missed this.
- Table 4 (codon-level nucleotide-polymorphism requirements) confirms R171K
  needs 3 simultaneous nucleotide changes via either codon path (CGT→AAA or
  CGT→AAG) — matches the paper's own "extremely unlikely under field
  conditions" conclusion, now traced to the actual codon-substitution table
  rather than taken on faith from the abstract.
- **Correction to an earlier (pre-PDF) characterization of this paper:** an
  initial proxy-summarized read described the screen as happening in
  "generations" (implying iterative rounds). The actual paper describes a
  single docking-guided screen of 70+34 variants with no generational
  structure — that framing was inaccurate and has been dropped from
  `docs/PHASE5_FAT_DHODH_AUDIT.md`.
- This is a bachelor-thesis project supervised at BASF (Limburgerhof, Germany),
  **not yet peer-reviewed** — treat with correspondingly lower evidentiary
  weight than a published, peer-reviewed paper, independent of how precisely
  the numbers above were read.

## Primary-source full-text check — Kot et al. 2026 FatA crystal structure (PDF supplied by user, saved to `docs/references/Kot_et_al_2026_FatA_crystal_structure.pdf`)

- Confirmed directly from the PDF text (`pypdf` extraction): solved structure is
  ***Arabidopsis thaliana* FatA**, 1.5 Å resolution, plus a 129-fragment XChem
  screening campaign at Diamond Light Source.
- PDB codes confirmed present in the paper's own text: `9HRR` (apo),
  `9HRQ` (ligand-bound), `9GRR` (cinmethylin-bound), `9HMT`
  (methiozolin-fluorine analogue), `9GS1` (oxaziclomefone-bound), `9S4H`
  (optimized lead x1816-FU1), plus group deposition `G_1002328` for the
  129 fragment hits, and reference structures `4KEH` (*E. coli* FabA-ACP) and
  `5X04` (*Umbellularia californica* FatB).
- Independently cross-checked `9GRR` and `9HRR` against RCSB's own data API
  (`data.rcsb.org/rest/v1/core/entry/...`), not just the paper's claim —
  both real, titles match exactly ("...Acyl-ACP Thioesterase (At-FatA)
  complexed with Cinmethylin" / "...FatA in an apo state").
- The paper calls the key inhibitor-contact residue **Arg176** throughout
  (never mentions R171). The crystallized construct has the 74-residue
  chloroplast transit peptide removed before expression but is still numbered
  from the full-length precursor. This supports — but does not confirm — the
  hypothesis that Arg176 (Arabidopsis) and R171 (blackgrass, per the Wagner
  et al. paper above) are the same catalytic residue at a ~5-residue
  species-numbering offset. **No sequence alignment has been run to confirm
  this** — treat as an open item, not a fact, until one is.

## Primary-source full-text check — Goggin et al. 2022 Lolium rigidum cinmethylin metabolism (PDF supplied by user, saved to `docs/references/Goggin_et_al_2022_Lolium_cinmethylin_metabolism.pdf`)

- Confirmed: Goggin, Cawthray, Busi, Porri & Beckie (2022), *Pest Manag Sci*
  78:3173-3182, DOI `10.1002/ps.6947`, peer-reviewed and open access.
- Populations: R1 (Wickepin, WA — field-collected then given 2 rounds of
  sublethal-dose lab selection), R2 and R3 (Tammin, WA — used directly from
  field screening, no further selection), vs susceptible control S, plus
  cinmethylin-tolerant wheat as a positive control. Table 1 read directly:
  survival-basis resistance indices R1 3.4 (p=0.393, n.s.), R2 7.2 (p=0.335,
  n.s.), R3 8.0 (p=0.324, n.s.); coleoptile-basis R1 1.4 (n.s.), R2 2.7
  (p=0.003, significant), R3 3.2 (p=0.001, significant); radicle-basis R3 4.5
  (p=0.043, significant). The authors themselves caveat these populations as
  "putatively" resistant, not officially confirmed as cinmethylin-resistant.
- Mechanism confirmed from Results 3.2: a specific water-soluble oxidative
  metabolite ("metabolite 4") correlates positively with resistance level
  (regression against ED50, Table 2); the cytochrome P450 inhibitor phorate
  decreased metabolite 4 production and synergized cinmethylin toxicity back
  toward susceptible-like levels (Colby analysis, Fig. 2) — this is
  mechanistic evidence of P450-mediated detoxification, not just a
  correlation.
- Confirms this is genuinely a **non-target-site (metabolic) resistance**
  finding, unrelated to the FAT active-site/R171 question — correctly kept as
  a separate row category in `data/processed/phase5_risk_table.csv`.
- Note the shared author (Aimone Porri, BASF) with the Wagner et al. 2026 FAT
  R171 preprint verified above — same institutional research thread on both
  the target-site and non-target-site sides of the cinmethylin-resistance
  question.

## R171 (blackgrass FatA) vs Arg176 (Arabidopsis FatA) numbering check — sequence alignment

- No public *Alopecurus myosuroides* FatA sequence exists to test this
  directly — checked NCBI protein (`esearch db=protein`), NCBI nuccore
  (`esearch db=nuccore`), and UniProt (`organism_name:"Alopecurus myosuroides"`)
  independently; all returned zero relevant hits. Confirms the earlier
  reading of the Wagner et al. 2026 PDF (no GenBank accession given anywhere
  in the text) — this sequence is genuinely not deposited publicly.
- Used wheat (*Triticum aestivum*, UniProt `Q8L6B1`, confirmed via
  `rest.uniprot.org` direct download, not a summarized fetch) as a proxy:
  wheat and blackgrass are both Pooideae grasses, much closer to each other
  than either is to Arabidopsis.
- Downloaded both sequences directly with `curl` (not WebFetch, to rule out
  summarization error) — `data/raw/Q42561_AtFATA1.fasta` (Arabidopsis FATA1,
  362 aa canonical UniProt sequence — note an earlier WebFetch-summarized read
  of this same page had misreported the length as 407 aa; the raw downloaded
  file is authoritative and was independently confirmed by direct
  byte-counting the sequence lines, not just Biopython's parser) and
  `data/raw/Q8L6B1_TaFatA.fasta` (wheat FatA, 289 aa).
- Confirmed directly: Arabidopsis position 176 (1-indexed) is Arg, matching
  Kot et al. 2026's "Arg176" exactly — validates that this is native/UniProt
  numbering, not an arbitrary construct-specific renumbering.
- Ran a global BLOSUM62 alignment (`scripts/phase5_fat_numbering_check.py`,
  reproducible, `.venv/Scripts/python.exe scripts/phase5_fat_numbering_check.py`).
  77.8% identity over the aligned region — high-confidence orthologous
  alignment, not a weak/spurious one. **Result: Arabidopsis Arg176 aligns to
  wheat Arg103, not to wheat position 171 (a threonine).** Wheat's own UniProt
  numbering is already mature-protein (transit-peptide-excluded): 176 − 103 =
  73, matching the 74-residue Arabidopsis transit peptide almost exactly.
- **Conclusion: if blackgrass's numbering in Wagner et al. 2026 follows the
  same mature-protein convention as wheat's UniProt entry (a reasonable
  assumption for a synthetic E. coli expression construct), R171 and Arg176
  are most likely different residues, roughly 70 positions apart — not the
  same catalytic arginine at a small species-numbering offset.** This refutes
  the working hypothesis recorded in the previous audit pass. Residual
  uncertainty: this was tested via a wheat proxy, not the actual blackgrass
  sequence (which is not publicly available), so it is not a 100% conclusive
  refutation — but it is strong enough evidence to stop treating the
  correspondence as a live open hypothesis.

## RCSB primary-citation check — EPSPS structure 8UMJ and HPPD structure 5YWG

- Both had previously been named by PDB ID only in `docs/MANUSCRIPT_DRAFT.md`'s Methods section with no
  origin-paper citation, because none had been located as of the 2026-07-05 PMS citation-formatting pass.
- Confirmed independently via `data.rcsb.org/rest/v1/core/entry/8UMJ` and `.../5YWG` (the same RCSB data
  API used elsewhere in this log, not a secondary summary):
  - **8UMJ** — `struct.title`: "Wild type EPSP synthase complexed with glyphosate and shikimate-3-phosphate".
    `rcsb_primary_citation`: Reed KB, Kim W, Lu H, Larue CT, Guo S, Brooks SM, Montez MR, Wagner JW,
    Zhang YJ, Alper HS (2024) Evolving dual-trait EPSP synthase variants using a synthetic yeast selection
    system. *Proc Natl Acad Sci USA* 121:e2317027121. DOI 10.1073/pnas.2317027121. Matches exactly, field
    for field, what the user independently reported from RCSB.
  - **5YWG** — `struct.title`: "Crystal structure of Arabidopsis thaliana HPPD complexed with Mesotrione".
    `rcsb_primary_citation`: Lin HY, Yang JF, Wang DW, Hao GF, Dong JQ, Wang YX, Yang WC, Wu JW, Zhan CG,
    Yang GF (2019) Molecular insights into the mechanism of 4-hydroxyphenylpyruvate dioxygenase inhibition:
    enzyme kinetics, X-ray crystallography and computational simulations. *FEBS J* 286:975-990. DOI
    10.1111/febs.14747. Matches exactly what the user independently reported.
- **Important distinction, kept deliberately conservative in the manuscript's wording:** neither paper is
  about weed herbicide resistance. 8UMJ's paper is about *engineering* dual-trait EPSPS variants via a
  synthetic yeast selection system (it happens to include the wild-type maize EPSPS-glyphosate-S3P
  structure used here as the structural anchor); 5YWG's paper is a kinetics/crystallography/computational
  study of the HPPD inhibition mechanism. Both are cited in the manuscript only as the RCSB-linked
  structure-provenance record for the PDB entry, not as resistance evidence — worded that way explicitly
  in both the Methods text and the reference-list bracketed notes.
- Added as manuscript references 3 (8UMJ/Reed 2024) and 5 (5YWG/Lin 2019), which required renumbering
  every subsequent reference by +2 (previously-numbered refs 3-20 became 4-22). Re-verified programmatically
  afterward: all 22 references are cited exactly once, in strict first-appearance order, no gaps or orphans.

## Not yet independently verified

- ABD52326/ABD52328 as a second legitimate ΔG210 pair, "confirmed via 2 independent
  citing papers" — Dayan 2010's methods only reference ABD52329/ABD52330 directly;
  I have not read the two citing papers said to confirm the other pair.
- Heinemann et al. 2007's specific 4-residue active-site core (Arg98, Phe392,
  Leu356, Leu372) and the claimed kcat/Ki effects of mutating each — not yet read
  from that paper directly, only cited correctly by Dayan 2010.
- Hao et al. 2014 (JAFC) — R98/hydrogen-bond-disruption mechanism detail still
  citation-only, not read directly.
- V361A mechanism class — per brief, genuinely still open.

## EPSPS setup checks (NCBI/RCSB live queries)

- RCSB metadata checked for EPSPS structures:
  - 8UMJ = wild-type *Zea mays* EPSPS complexed with glyphosate and
    shikimate-3-phosphate; selected as the EPSPS structure anchor.
  - 1G6S/2AAY = *E. coli* glyphosate-bound EPSPS structures; useful precedent but
    not selected because 8UMJ gives a plant glyphosate-bound template.
  - 7PXY = *Arabidopsis thaliana* EPSPS, but open conformation/no glyphosate ligand;
    not selected for ligand-contact active-site definition.
- PubMed metadata for Baerson et al. 2002, PMID 12114580, explicitly lists GenBank
  accessions AJ417033 and AJ417034.
- GenBank records fetched directly:
  - AJ417033.1 = *Eleusine indica* `epsps-R`, protein CAD01095.1, reference Baerson
    et al. 2002.
  - AJ417034.1 = *Eleusine indica* `epsps-S`, protein CAD01096.1, reference Baerson
    et al. 2002.
- Local translation comparison of AJ417033/AJ417034 found two differences:
  - translated position 107: resistant Ser, susceptible Pro. This corresponds to
    Baerson's mature-protein Pro106Ser convention.
  - translated position 382: resistant Leu, susceptible Pro. Baerson's abstract
    states the second substitution does not contribute significantly to reduced
    glyphosate sensitivity.
- Local alignment maps Eleusine translated position 107 to 8UMJ maize sequence
  position 107 and PDB residue 106. Correction note: 8UMJ includes an initiating
  MET numbered 0, so FASTA sequence position 107 corresponds to PDB residue 106,
  not the naive ATOM-list index result of 108.
- Chong et al. 2008 PDF was saved and OCR-read. Its text cites AJ417034 for primer
  design and AY157643 as a Bidor resistant comparison sequence, but AY157643 is
  marked "Unpublished" in GenBank. Treat Chong as context/lower-confidence, not the
  manuscript-reliant EPSPS accession anchor.

## EPSPS distance/SASA checks (local 8UMJ run)

- 8UMJ PDB header checked directly:
  - Chains A and B are both *Zea mays* EPSPS.
  - REMARK 350 marks each chain as a monomeric biological unit.
  - Chain A contains glyphosate (`GPJ`) and shikimate-3-phosphate (`S3P`).
- Active-site core defined from 4.5 A contacts between chain-A protein atoms and
  either `GPJ` or `S3P`, using `scripts/epsps_distance_sasa.py`.
- Core residues returned by the run:
  24, 25, 29, 51, 99, 100, 101, 102, 105, 131, 177, 178, 179, 180, 205, 206,
  209, 330, 331, 354, 358, 359, 362, 403, 404, 429.
- Corrected Pro106Ser check from `data/processed/epsps_8umj_distance_sasa.csv`:
  - PDB residue 106 = PRO.
  - `in_active_site_core = False`.
  - `distance_to_active_site_core_A = 3.847435769444372`.
  - `percentile_rank_distance_to_core = 12.866817155756207`.
  - `sasa_A2 = 14.30848846052983`.
- ChimeraX was not available on PATH in this Codex session. SASA was therefore
  computed with the local `scripts/pdb_static_metrics.py` Shrake-Rupley-style
  fallback, with bound ligands included as occluding atoms.
- A first NCBI E-utilities attempt to fetch a broader plant EPSPS panel worked
  initially but then returned HTTP 429. The completed conservation panel below
  uses UniProt records plus the already verified Baerson `AJ417034.1` sequence.

## EPSPS conservation checks

- User-supplied UniProt/NCBI IDs were checked directly before inclusion:
  - Included as supplied: `P05466` (*Arabidopsis thaliana*), `P23981`
    (*Nicotiana tabacum*).
  - Excluded: `A0A0R0H6D7` returned UniProt 404.
  - Excluded: `Q0DFI0`, `K4C1C4`, `B9H6K7` returned empty FASTA bodies from
    UniProt accession endpoint.
  - Excluded: `A0A2G2Y4X3` is *Capsicum annuum* SAUR68-like, not *Beta vulgaris*
    EPSPS.
  - Excluded: `P24397` is *Hyoscyamus niger* hyoscyamine 6-beta-hydroxylase, not
    *Zea mays* EPSPS.
  - Excluded for Eleusine use: `AF349754` is *Lolium rigidum* EPSPS, not
    *Eleusine indica*. The verified Baerson *Eleusine* susceptible accession
    remains `AJ417034.1`.
- UniProt search found corrected EPSPS records:
  - `I1JKP7` = *Glycine max* 3-phosphoshikimate 1-carboxyvinyltransferase.
  - `A0A0N7KLH2` = *Oryza sativa* EPSPS fragment.
  - `P10748` = *Solanum lycopersicum* EPSPS.
  - `B9GPE8` = *Populus trichocarpa* EPSPS.
  - `A0A1D6NVZ6` = *Zea mays* EPSPS and matches 8UMJ PDB metadata.
- `scripts/epsps_conservation_entropy.py` wrote:
  - `data/processed/epsps_conservation_set.fasta` (8 sequences).
  - `data/processed/epsps_conservation_entropy.csv` (443 structured
    8UMJ/PDB-numbered rows matching the distance/SASA table).
- Pro106 conservation result:
  - PDB residue 106 / sequence position 107 = Pro.
  - Shannon entropy = 0.000.
  - Normalized conservation = 1.000.
  - Present in 7/8 sequences; the Oryza fragment is absent at this column.
  - EPSPS validation gate can now be marked passed.

## ACCase primary-source checks

- User-provided PDFs were copied into `docs/references/`:
  - `Delye_et_al_2005_ACCase_blackgrass.pdf`
  - `Yu_et_al_2007_ACCase_Lolium.pdf`
- Delye et al. 2005 was checked directly:
  - It states that the reference sequence for ACCase is black-grass
    chloroplastic ACCase **AJ310767**, and that all nucleotide and amino-acid
    positions correspond to that sequence.
  - It identifies Trp2027Cys, Asp2078Gly, and Gly2096Ala from resistant
    black-grass seedlings, while discussing Ile1781Leu and Ile2041Asn as
    previously established ACCase resistance substitutions.
  - It uses yeast ACCase CT-domain structures **1UYT** and **1UYS** as templates
    and gives the aligned black-grass CT span as residues 1639-2204 of AJ310767.
- Yu et al. 2007 was checked directly:
  - It identifies Ile1781Leu, Trp2027Cys, Ile2041Asn, Asp2078Gly, and the new
    Cys2088Arg mutation in resistant *Lolium* populations.
  - It states that the Cys2088Arg-region sequences were deposited as
    **EF538937-EF538943**.
  - Its methods name the plastidic ACCase sequences used for primer design,
    including *Alopecurus myosuroides* AJ310767 and *Lolium rigidum* AY995232.
- ACCase is therefore verified as a reference-numbered mutation set, not as a set
  of paired full-length resistant/susceptible accessions.

## ACCase structure/metric checks

- RCSB 1UYS PDB header checked directly:
  - 1UYS is yeast ACCase CT-domain in complex with haloxyfop (`H1L`).
  - The PDB header lists B+C as a dimeric biological unit.
  - Chains B and C were used for ACCase metrics; chain A was deleted before
    ChimeraX SASA.
- Local AJ310767-to-1UYS alignment maps:
  - 1781 -> chain C residue 1705 for the Delye dimer-side convention.
  - 2027 -> chain B residue 1953.
  - 2041 -> chain B residue 1967.
  - 2078 -> chain B residue 2004.
  - 2088 -> chain B residue 2014.
  - 2096 -> chain B residue 2022.
- `scripts/chimerax_accase_distance_sasa.py` wrote
  `data/processed/accase_1uys_distance_sasa.csv`:
  - 42 active-site core chain-residue positions from 4.5 A contacts to `H1L`.
  - 1328 B/C chain-residue rows.
- Key ACCase static results:
  - Ile1781Leu: in core, distance 0.00 A, percentile 3.2, SASA ~0.0 A^2.
  - Trp2027Cys: 5.60 A from core, percentile 10.4, SASA 3.2 A^2.
  - Ile2041Asn: in core, distance 0.00 A, percentile 3.2, SASA 1.6 A^2.
  - Asp2078Gly: 5.19 A from core, percentile 8.7, SASA 0.5 A^2.
  - Cys2088Arg: 11.83 A from core, percentile 25.9, SASA 0.7 A^2.
  - Gly2096Ala: 7.28 A from core, percentile 12.8, SASA 1.4 A^2.
- `scripts/accase_conservation_entropy.py` wrote:
  - `data/processed/accase_conservation_set.fasta` (14 sequences).
  - `data/processed/accase_conservation_entropy.csv` (562 structured
    AJ310767/1UYS-mapped positions).
- Conservation at ACCase sites:
  - 1781: 0.909, present 13/14.
  - 2027: 1.000, present 12/14.
  - 2041: 0.850, present 12/14.
  - 2078: 1.000, present 12/14.
  - 2088: 0.904, present 12/14.
  - 2096: 1.000, present 12/14.
  - ACCase validation gate can now be marked passed.

## External review reconciliation / ALS interface-core check

- External review and parallel Claude-side review flagged that AHAS inhibitor
  binding occurs at a dimer-interface pocket, so the original ALS core based only
  on same-chain 1IQ contacts was incomplete.
- 1Z8N was rechecked in biological-interface context. The original same-chain
  1IQ-contact core remains:
  - 220, 245, 246, 275, 276, 279, 280, 281, 351, 376, 377, 396, 397, 574, 653,
    654.
- Added interface-pocket residue numbers, expressed in the same Arabidopsis/PDB
  numbering convention:
  - 121, 122, 168, 195, 196, 197, 199, 200, 206, 207, 256.
- `data/processed/als_1z8n_distance_sasa.csv` was regenerated for the distance
  and core-membership columns using local 1Z8N chain-A CA coordinates while
  preserving the previously computed ChimeraX biological-tetramer SASA column.
- Corrected ALS output checks:
  - Active-site core size: 27 residues.
  - Ala122: now in core, nearest-other-core distance 3.805 A.
  - Pro197: now in core, nearest-other-core distance 3.839 A.
  - Trp574: still in core, distance-to-core 0.000 A, nearest-other-core distance
    10.607 A, SASA 19.206 A^2.
  - Ser653: still in core, distance-to-core 0.000 A, nearest-other-core distance
    3.795 A, SASA 32.562 A^2.
- ChimeraX 1.12 console stalled during this session before emitting structure
  output, even when pointed at the local `data/raw/1Z8N.pdb`. Because this review
  correction only changes core membership and CA-distance calculations, not SASA,
  the verified CSV update preserved existing ChimeraX SASA values and recomputed
  the affected distance fields offline from the local PDB.

## HPPD source audit and structure checks

- RCSB raw files downloaded to `data/raw/`:
  - `5YWG.pdb` / `5YWG.fasta`.
  - `1TG5.pdb` / `1TG5.fasta`.
- 5YWG PDB header checked directly:
  - Title: crystal structure of *Arabidopsis thaliana* HPPD complexed with
    mesotrione.
  - Chains A and B are HPPD.
  - Biological unit is dimeric.
  - Ligands: mesotrione (`92L`) and cobalt (`CO`).
  - Metal coordination links include His226, His308, and Glu394 to `CO`.
  - Primary citation: Lin et al., FEBS Journal 2019, PMID 30632699,
    DOI 10.1111/FEBS.14747.
- 1TG5 PDB header checked directly:
  - Title: plant HPPD complexed with DAS645.
  - Chain A is *Arabidopsis thaliana* HPPD.
  - Biological unit is dimeric.
  - Ligands: Fe(II) (`FE2`) and DAS645 (`645`).
  - Metal coordination links include His205, His287, and Glu373 to `FE2`.
  - Primary citation: Yang et al., Biochemistry 2004, PMID 15301540,
    DOI 10.1021/BI049323O.
- PubMed HPPD weed-resistance search artifacts saved in `work/`:
  - `hppd_pubmed_esearch.json`.
  - `hppd_overexpression_pubmed_esearch.json`.
  - `hppd_tsr_pubmed_esearch.json`.
  - `hppd_pubmed_candidates.xml`.
- Source-audit interpretation:
  - PMID 28662111 (*A. tuberculatus* mesotrione): no target-site HPPD mutations
    associated with resistance; no HPPD duplication or overexpression in the NEB
    population; higher mesotrione metabolism observed.
  - PMID 28443128 (*A. palmeri* mesotrione): no specific resistance-conferring
    HPPD mutation or HPPD gene amplification; increased HPPD expression and rapid
    detoxification reported.
  - PMID 28799707 (*A. tuberculatus* HPPD inhibitors): non-target-site,
    metabolism-based resistance; P450 inhibitors restored herbicide activity.
  - PMID 30519248 (*A. tuberculatus* topramezone): HPPD-inhibitor resistance
    described as rapid oxidative metabolism of the parent herbicide.
  - PMID 37170102 wild radish: HPPD cross-resistance endowed by enhanced
    metabolism; candidate P450 and dioxygenase detoxification genes implicated.
  - PMID 37889480 *Leptochloa chinensis*: no HPPD target-site amino-acid mutation;
    P450/GST detoxification implicated.
- `scripts/hppd_distance_sasa.py` wrote
  `data/processed/hppd_5ywg_active_site_metrics.csv`:
  - 735 A/B dimer chain-residue rows.
  - 34 active-site core chain-residue positions from 4.5 A contacts to `92L` or
    `CO`.
  - Symmetric core per chain: 226, 228, 267, 280, 282, 307, 308, 368, 379, 381,
    392, 394, 419, 420, 421, 423, 424.
  - His226, His308, and Glu394 are metal-contact residues.
  - Phe424 is a mesotrione-pocket residue.
- 1TG5 Fe(II)+DAS645 contact-core check:
  - Fe/inhibitor core: 205, 207, 242, 244, 246, 248, 259, 261, 287, 289, 358,
    360, 371, 373, 398, 399, 400, 402, 403, 406.
  - Fe-only core includes His205, His287, and Glu373.
- HPPD conclusion:
  - No `hppd_mutations.csv` was created.
  - HPPD is complete as a structural negative/contrast case, not a TSR-positive
    validation-gate family.
  - Gly336 remains excluded as engineered crop tolerance, not weed resistance.

## RSA normalization check

- Added `scripts/rsa.py` as a deterministic post-processing step for the current
  static metric CSV outputs.
- Reference values: Tien et al. 2013 maximum allowed solvent-accessibility table
  for the 20 standard amino acids. Project-specific modified residue aliases:
  - `MSE -> MET` maximum ASA = 224 A^2.
  - `CSD -> CYS` maximum ASA = 167 A^2.
- Formula checked in tests: `rsa_tien2013 = sasa_A2 / max_sasa_tien2013_A2`.
- Raw `sasa_A2` values are preserved; the new columns are appended immediately
  after `sasa_A2`.
- Files verified by `tests/test_rsa.py`:
  - `data/processed/ppo_1sez_distance_sasa.csv`
  - `data/processed/als_1z8n_distance_sasa.csv`
  - `data/processed/epsps_8umj_distance_sasa.csv`
  - `data/processed/accase_1uys_distance_sasa.csv`
  - `data/processed/hppd_5ywg_active_site_metrics.csv`
- Verification command used in this session:
  - `python -m unittest tests.test_rsa`

## Phase 4 pooled table foundation check

- Reconciled the local checkout to pushed `origin/master` commit `6b34186` before
  starting Phase 4 work. The pre-reconciliation dirty local state was preserved as
  git stash entry `stash@{0}` named `pre-phase4-reconcile-local-dirty-state`.
- Baseline unit test command after reconciliation:
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`
  - Result: 15 tests run, all passed.
- Added `scripts/build_phase4_tables.py` and `tests/test_phase4_tables.py`.
- Test-driven check:
  - First focused run failed because `scripts.build_phase4_tables` did not exist,
    confirming the test covered missing Phase 4 behavior.
  - After implementation, `.venv\Scripts\python.exe -m unittest tests.test_phase4_tables -v`
    passed.
- Generated outputs:
  - `output/tables/phase4_master_mutation_table.csv`
  - `output/tables/phase4_target_family_contrast.csv`
- Output sanity checks:
  - Master mutation table row count: 15.
  - Family counts: PPO 6, ALS 2, EPSPS 1, ACCase 6.
  - HPPD is absent from the pooled mutation table and appears only in the contrast
    table with `accepted_tsr_rows = 0` and status
    `no_verified_weed_tsr_accepted`.
  - Spot-checked joined rows include PPO `deltaG210_pair1`, ALS `Trp574Leu`,
    EPSPS `Pro106Ser`, and ACCase `Cys2088Arg`; each has joined RSA and
    conservation values.

## Phase 4 permutation/enrichment analysis check

- Added `scripts/build_phase4_analysis.py` and `tests/test_phase4_analysis.py`.
- Test-driven checks:
  - First focused run failed because `scripts.build_phase4_analysis` did not
    exist.
  - A second focused run caught a direct-script execution bug:
    `ModuleNotFoundError: No module named 'scripts'` when running
    `scripts/build_phase4_analysis.py` from the repo root. The script now inserts
    the repo root into `sys.path` when run as a direct file.
- Focused verification command:
  - `.venv\Scripts\python.exe -m unittest tests.test_phase4_analysis -v`
  - Result: 2 tests run, all passed.
- Analysis generation command:
  - `.venv\Scripts\python.exe scripts\build_phase4_analysis.py --iterations 10000 --seed 20260704`
- Generated outputs:
  - `output/tables/phase4_permutation_summary.csv`
  - `output/tables/phase4_non_core_position_screen.csv`
- Output checks:
  - Unique structural-position counts: PPO 4, ALS 2, EPSPS 1, ACCase 6.
  - HPPD is absent from both mutation-position analysis outputs.
  - Empirical lower-tail p-values from 10,000 permutations:
    - ACCase: 0.000200.
    - ALS: 0.002200.
    - EPSPS: 0.131887.
    - PPO: 0.000400.
  - Non-core candidate screen highlights the most distal accepted positions by
    distance percentile: ACCase Cys2088Arg (25.9), PPO V361A (20.2), EPSPS
    Pro106Ser (12.9), ACCase Gly2096Ala (12.8), and ACCase Trp2027Cys (10.4).

## Review-driven mechanism annotation and manuscript-output check

- Added `scripts/build_review_driven_outputs.py` and
  `tests/test_review_driven_outputs.py`.
- Test-driven check:
  - First focused run failed because `scripts.build_review_driven_outputs` did not
    exist.
  - After implementation, `.venv\Scripts\python.exe -m unittest tests.test_review_driven_outputs -v`
    passed.
- Generated outputs:
  - `output/tables/phase4_mechanism_annotations.csv`
  - `output/tables/manuscript_table_1_family_permutation_summary.csv`
  - `output/tables/manuscript_table_2_unique_position_mechanisms.csv`
  - `output/tables/manuscript_table_3_hppd_contrast_status.csv`
  - `output/figures/figure_1_workflow.svg`
  - `output/figures/figure_2_permutation_enrichment.svg`
  - `output/figures/figure_3_position_screen.svg`
  - `output/figures/figure_4_distance_rsa_conservation.svg`
- Output checks in `tests/test_review_driven_outputs.py`:
  - Mechanism table contains 13 unique structural mutation positions.
  - HPPD is excluded from mutation rows and retained in the manuscript contrast
    table with `accepted_tsr_rows = 0`.
  - Mechanism labels are limited to the controlled vocabulary.
  - Unresolved mechanisms are not labeled `literature_supported`.
  - PPO deltaG210 is annotated as `allosteric_hinge` with
    `literature_supported` evidence.
  - ACCase Cys2088Arg is annotated as `interface_induced_fit`.
- Added interpretive docs:
  - `docs/REVIEW_RESPONSE_STATIC_VS_DYNAMIC.md`
  - `docs/MANUSCRIPT_RESULTS_PHASE4.md`

## First manuscript draft check

- Added `docs/MANUSCRIPT_DRAFT.md` as an internal first draft assembled from
  existing Phase 4 outputs rather than new analysis.
- Draft inputs checked before writing:
  - `docs/MANUSCRIPT_RESULTS_PHASE4.md`
  - `docs/REVIEW_RESPONSE_STATIC_VS_DYNAMIC.md`
  - `output/tables/manuscript_table_1_family_permutation_summary.csv`
  - `output/tables/manuscript_table_2_unique_position_mechanisms.csv`
  - `output/tables/manuscript_table_3_hppd_contrast_status.csv`
  - `output/tables/phase4_non_core_position_screen.csv`
- The draft explicitly preserves the current scope boundary: no new molecular
  dynamics pipeline and no ColabFold expansion inside the current Phase 4 claim.
  ColabFold remains future work for FAT/DHODH or other targets lacking adequate
  structures.

## ACCase SWISS-MODEL rerun check

- SWISS-MODEL project checked in the browser:
  - Project URL: `https://swissmodel.expasy.org/interactive/u3jF6Y/`
  - Selected 1UYS homomer template because the ACCase resistance-zone metric
    depends on dimer context.
  - Completed model metadata: GMQE 0.76; QMEANDisCo global 0.72 +/- 0.05;
    template `1uys.2.A` / `1uys.2.B`; sequence identity 53.27%; coverage 0.998.
  - SWISS-MODEL excluded H1L with the metadata reason that the binding site was
    not conserved, so ligand-contact core membership must be transferred from
    aligned 1UYS H1L contacts.
- Downloaded files:
  - `data/raw/ACCase_Alopecurus_AJ310767_CTdomain_SWISSMODEL_1UYS_homomer.pdb`
  - `data/raw/ACCase_Alopecurus_AJ310767_CTdomain_SWISSMODEL_1UYS_homomer.json`
- PDB spot checks:
  - 8,800 ATOM/HETATM records.
  - Chains A and B.
  - Each chain spans model residues 1-566.
  - No ligand records were present.
- Added and ran `scripts/accase_swissmodel_distance_sasa.py`.
  - It transfers active-site-core positions from 21 black-grass positions in
    1UYS H1L contact space to 42 model chain residues in the homodimer.
  - It generated `data/processed/accase_swissmodel_1uys_distance_sasa.csv`
    with 1,132 residue rows.
- Mutation-position checks from the generated metric table:
  - Ile1781Leu: A:143, ILE, direct core, percentile 3.71, RSA 0.020434.
  - Trp2027Cys: B:389, TRP, non-core, percentile 12.46, RSA 0.
  - Ile2041Asn: B:403, ILE, direct core, percentile 3.71, RSA 0.107777.
  - Asp2078Gly: B:440, ASP, non-core, percentile 12.28, RSA 0.010429.
  - Cys2088Arg: B:450, CYS, non-core, percentile 31.98, RSA 0.084807.
  - Gly2096Ala: B:458, GLY, non-core, percentile 15.28, RSA 0.017171.
- Focused unit checks added:
  - `tests/test_accase_swissmodel_outputs.py`
  - Updated Phase 4 table/analysis expectations so Cys2088Arg maps to `B:450`
    in the active master/non-core outputs.

## Phase 5 FAT/DHODH structure-evidence audit check

- Wrote the Phase 5 design spec:
  - `docs/superpowers/specs/2026-07-05-fat-dhodh-phase5-design.md`
- FAT/acyl-ACP thioesterase evidence checked through structured RCSB and Crossref
  lookups:
  - Lemna FAT inhibitor-complex structures identified: 8P8K, 8QRT, 8QS0.
  - Arabidopsis FatA fragment structures identified: 7HQQ, 7HQR, 7HQS, 7HQT,
    7HQU.
  - 8P8K citation metadata: DOI `10.1021/acs.jafc.3c02490`, Journal of
    Agricultural and Food Chemistry 2023, thiazolopyridine FAT inhibitor
    discovery/optimization.
  - 8QRT/8QS0 citation metadata: DOI `10.1002/ps.8015`, Pest Management Science
    2025, spirocyclic lactam FAT inhibitor discovery/optimization.
- DHODH evidence checked through structured RCSB entity search:
  - Query target: polymer entity description containing "dihydroorotate
    dehydrogenase".
  - Result: 278 DHODH polymer entities across 273 unique RCSB entries.
  - Metadata filtering found zero plant-like organisms among those DHODH entries.
  - Interpretation: no public plant DHODH structure was identified by this
    structured search; DHODH needs a plant structure/model route before structural
    metrics can be claimed.
- Tetflupyrolimet/DHODH literature anchor checked through Crossref:
  - DOI `10.1021/acs.jafc.3c01634` for the JAFC 2023 tetflupyrolimet discovery
    paper.
- Verification decision:
  - FAT is structurally actionable first.
  - DHODH remains a target/MoA audit item until mutation evidence and structure or
    model provenance are verified.
  - Neither target should be added to the Phase 4 pooled outputs during the audit.

## Repository index and handoff refresh check

- Added root navigation map:
  - `REPO_INDEX.md`
- Linked the index from:
  - `README.md`
- Updated the active handoff:
  - `docs/HANDOFF_NEXT_STEPS.md`
- Added a ready-to-paste Claude Code prompt that tells the next agent to read:
  - `REPO_INDEX.md`
  - `docs/HANDOFF_NEXT_STEPS.md`
  - `docs/DECISION_LOG.md`
  - `docs/VERIFICATION_LOG.md`
  - `docs/superpowers/specs/2026-07-05-fat-dhodh-phase5-design.md`
- Handoff prompt records the three current-session reasons:
  - ACCase moved to SWISS-MODEL weed CT-domain metrics to close the senior-review
    side-chain caveat.
  - FAT/DHODH moved forward as Phase 5 audit work, not Phase 4 integration.
  - `REPO_INDEX.md` is now the first-file navigation map for new agents.

## Canonical presentation reset and Phase 5 starter audit check

- Removed old generated presentation outputs from `output/presentations/`,
  including generated decks, preview image folders, montage PNGs, inspect
  NDJSON files, and the failed asset folder.
- Saved the user-attached deck as:
  - `output/presentations/herbicide_resistance_structural_bioinformatics_talk.pptx`
- Rendered the canonical deck to temporary PNGs outside the repo:
  - Render output: 21 slides.
  - Temporary montage visually inspected; all slides rendered in the attached
    academic green/cream style.
- Ran `slides_test.py` on the canonical PPTX:
  - Result: `Test passed. No overflow detected.`
- Archived the user-attached handoff guide as:
  - `docs/PROJECT_HANDOFF_GUIDE.doc`
- Updated project memory:
  - `REPO_INDEX.md`
  - `docs/HANDOFF_NEXT_STEPS.md`
  - `docs/DECISION_LOG.md`
  - `docs/VERIFICATION_LOG.md`
- Created Phase 5 starter audit artifacts:
  - `docs/PHASE5_FAT_DHODH_AUDIT.md`
  - `data/processed/phase5_target_status.csv`
- Verification decision:
  - FAT remains the first Phase 5 audit target.
  - DHODH remains gated behind mutation evidence plus a verified plant
    structure/model route.
  - The canonical presentation is a saved baseline and should not be restyled
    unless the user asks.
