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

## Not yet independently verified (flagging per the brief's own "don't resolve by inference" instruction)

- ABD52326/ABD52328 as a second legitimate ΔG210 pair, "confirmed via 2 independent
  citing papers" — Dayan 2010's methods only reference ABD52329/ABD52330 directly;
  I have not read the two citing papers said to confirm the other pair.
- Heinemann et al. 2007's specific 4-residue active-site core (Arg98, Phe392,
  Leu356, Leu372) and the claimed kcat/Ki effects of mutating each — not yet read
  from that paper directly, only cited correctly by Dayan 2010.
- Hao et al. 2009's specific "Gly210–Ser424 hydrogen bond" mechanism claim — Dayan
  2010 only vaguely summarizes Hao's finding as "affected the surrounding hydrogen
  bonding network"; the Ser424-specific detail isn't in the text I have.
- V361A mechanism class — per brief, genuinely still open.
