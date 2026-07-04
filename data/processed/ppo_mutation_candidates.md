# PPO2 mutation candidates — needs your sign-off before Phase 1 proceeds

Pulled live from NCBI protein DB, aligned pairwise with Biopython. Raw sequences saved in `data/raw/`.

## Amaranthus tuberculatus (waterhemp)

| Accession | Length | Candidate role |
|---|---|---|
| ABD52326.1 / ABD52329.1 | 534 aa | candidate wild-type (Gly-210 present) |
| ABD52328.1 / ABD52330.1 | 533 aa | candidate resistant allele (Gly-210 deleted) |

- ABD52326 vs ABD52328: **single difference at position 210 (G → deletion)**, plus an unrelated S476C difference.
- ABD52326 vs ABD52330: gap at position 210 again, plus two other background differences (D75N, H219Y).
- ABD52326 vs ABD52329: single difference at position 133 (D→A) — unrelated to the deletion, looks like natural background polymorphism.
- All four are deposited under GenBank submission title **"A codon deletion confers resistance to herbicides inhibiting protoporphyrinogen oxidase"** — this is Patzoldt et al. 2006, *PNAS* (the original ΔG210 waterhemp paper).

**This matches the plan's ΔG210 case exactly, with no numbering discrepancy** — GenBank position 210 lines up with the published "Gly-210 deletion" name directly.

## Amaranthus palmeri (Palmer amaranth)

| Accession | Length | Candidate role |
|---|---|---|
| QBB02367.1 | 535 aa | candidate wild-type |
| QBB02368.1 | 535 aa | candidate V361A resistant allele |

- QBB02367 vs QBB02368 differ at 3 positions: 68 (S→N), **361 (V→A)**, 480 (R→T).
- Position 361 matches a real, distinct paper found via literature search: **"A New V361A Mutation in Amaranthus palmeri PPX2 Associated with PPO-Inhibiting Herbicide Resistance"** (*Plants*, 2023, DOI 10.3390/plants12091886). GenBank numbering lines up directly with the paper's own "V361A" name.
- The other two differences (68, 480) are presumably background polymorphism between biotypes, not the causal mutation — **not yet confirmed against the paper's full text**.

**Not yet found:** the G399A and R98L/R128L mutations mentioned in the original plan. Those come from a *different* paper — "Two new PPX2 mutations associated with resistance to PPO-inhibiting herbicides in Amaranthus palmeri" (Rangani et al. 2019, *Pest Management Science*, DOI 10.1002/ps.4581) — and would need a separate NCBI accession lookup if you want them included in the pilot.

## Open questions for you (domain sign-off needed)

1. Are ABD52326/ABD52328 (waterhemp) and QBB02367/QBB02368 (Palmer amaranth) actually the correct wild-type/resistant pairs, per your own knowledge of these papers?
2. Do you want the pilot to also include G399A and/or R98L/R128L (Rangani et al. 2019), or is ΔG210 + V361A sufficient for a first pass?
3. Any concern about the background polymorphisms (S476C, D75N, H219Y, S68N, R480T) confounding the structural analysis — should those be excluded from consideration as candidate resistance sites?
