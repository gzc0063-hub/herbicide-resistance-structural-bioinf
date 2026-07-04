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
