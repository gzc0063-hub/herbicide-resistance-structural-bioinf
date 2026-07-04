# EPSPS Phase 2 expansion - mutation candidates

Initial EPSPS scope follows the metric-schema cleanup decision in
`docs/DECISION_LOG.md` section 18: start the post-pilot expansion with EPSPS before
batching ACCase and HPPD.

## Structure candidate selected

**PDB 8UMJ** - wild-type *Zea mays* EPSPS complexed with glyphosate and
shikimate-3-phosphate.

Rationale:

- Plant/Viridiplantae source organism (*Zea mays*), unlike the classic *E. coli*
  glyphosate-bound structures 1G6S and 2AAY.
- Contains glyphosate and shikimate-3-phosphate, so the active-site core can be
  defined directly from ligand contacts rather than by literature residue lists.
- RCSB metadata checked directly: polymer entity source organism is *Zea mays*,
  UniProt A0A1D6NVZ6.

Files saved:

- `data/raw/8UMJ.pdb`
- `data/raw/8UMJ.fasta`

## Mutation/accession candidate selected

**Baerson et al. 2002, Plant Physiology 129:1265-1275, PMID 12114580**

Mutation: **Pro106Ser** in glyphosate-resistant goosegrass (*Eleusine indica*).

Why this is the EPSPS pilot mutation:

- Peer-reviewed primary source.
- PubMed metadata for the paper explicitly lists GenBank accessions **AJ417033**
  and **AJ417034**.
- GenBank records identify AJ417033 as `epsps-R` and AJ417034 as `epsps-S`, both
  tied directly to Baerson et al. 2002.
- The paper's abstract states that the resistant biotype carries a Pro106Ser
  substitution and that recombinant-enzyme/heterologous-expression evidence
  supports the Pro106 change as the main driver of reduced glyphosate sensitivity.

Accessions:

| Role | Accession | Record description | Peer-reviewed anchor |
|---|---|---|---|
| Resistant | AJ417033.1 | *E. indica* plastid partial mRNA, `epsps-R`; protein CAD01095.1 | Baerson et al. 2002 |
| Susceptible | AJ417034.1 | *E. indica* plastid partial mRNA, `epsps-S`; protein CAD01096.1 | Baerson et al. 2002 |

Important numbering note:

- In the GenBank translated partial protein, the relevant difference is at
  translated position **107**: AJ417033 has Ser, AJ417034 has Pro.
- Baerson reports this by mature-protein convention as **Pro106Ser**.
- A local sequence-alignment check maps Eleusine translated position 107 to
  8UMJ maize sequence position 107 and **PDB residue 106**. 8UMJ includes an
  initiating MET numbered 0, so FASTA sequence position 107 corresponds to PDB
  residue 106, not 108.

Second difference to keep explicit:

- AJ417033 and AJ417034 also differ at GenBank translated position 382
  (resistant Leu, susceptible Pro).
- Baerson's abstract states the second substitution does not contribute
  significantly to reduced glyphosate sensitivity. Treat it as background, not the
  EPSPS pilot mutation.

## Lower-confidence / context-only source

**Chong et al. 2008, Pakistan Journal of Biological Sciences 11:476-479,
DOI 10.3923/pjbs.2008.476.479**

PDF saved as `docs/references/Chong_et_al_2008_EPSPS_Eleusine.pdf`.

Useful context:

- Reports Pro106Ser and Pro106Thr variation across Malaysian *E. indica*
  resistant populations.
- Paper text cites AJ417034 as the GenBank sequence used for primer design and
  AY157643 as a Bidor resistant comparison sequence.

Limitations:

- AY157643 is marked "Unpublished" in the GenBank record and should be tagged
  `unpublished_lower_confidence` if used at all.
- Chong sequenced a short 202-bp region and does not provide new deposited
  per-population accessions for each sample in Table 1.
- Therefore Chong is useful for context and independent population evidence, but
  not the accession anchor for the EPSPS pilot.
