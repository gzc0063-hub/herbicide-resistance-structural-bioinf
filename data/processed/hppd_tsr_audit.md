# HPPD target-site-resistance audit

## Bottom line

No verified weed-evolved HPPD target-site amino-acid substitution was accepted for
the comparative TSR dataset in this pass. HPPD should be treated as a structural
active-site contrast case, not as a forced mutation-validation gate.

The key exclusion is **Gly336**: it is an engineered *Pseudomonas fluorescens*
HPPD crop-tolerance variant used in FG72 soybean, not an evolved weed-resistance
mutation. It must not be included as a weed TSR row.

## Source audit

PubMed searches were saved in `work/hppd_*pubmed*.json` and
`work/hppd_pubmed_candidates.xml`. The relevant peer-reviewed weed-resistance
records found in this audit point to non-target-site resistance, metabolism, and
expression effects rather than a validated weed-evolved HPPD amino-acid mutation:

| PMID | Organism/context | Audit interpretation |
|---|---|---|
| 28662111 | *Amaranthus tuberculatus* / mesotrione | Sequencing did not detect target-site HPPD mutations associated with resistance; no HPPD duplication or overexpression in the Nebraska population; higher mesotrione metabolism was observed. |
| 28443128 | *Amaranthus palmeri* / mesotrione | No specific resistance-conferring HPPD mutation or HPPD gene amplification was detected; resistant populations showed increased HPPD expression and rapid mesotrione detoxification. |
| 28799707 | *Amaranthus tuberculatus* / HPPD inhibitors | Resistance was described as non-target-site and metabolism-based, with cytochrome P450 inhibitors restoring herbicide activity. |
| 30519248 | Multiple-resistant *Amaranthus tuberculatus* / topramezone | HPPD-inhibitor resistance in waterhemp was described as rapid oxidative metabolism of the parent compound. |
| 37170102 | Wild radish / HPPD inhibitors | Cross-resistance was endowed by enhanced metabolism; candidate P450 and 2-oxoglutarate/Fe(II)-dependent dioxygenase genes were implicated. |
| 37889480 | *Leptochloa chinensis* / tripyrasulfone | The first reported grass-weed HPPD resistance case did not involve target-site amino-acid mutations; P450/GST-mediated detoxification was implicated. |

Several additional HPPD papers found by the search are herbicide-discovery,
crop-engineering, or directed-mutagenesis studies. Those are useful mechanistic
background but are not eligible as weed-evolved TSR evidence.

## Decision

Do not create `hppd_mutations.csv` until a peer-reviewed weed-evolved HPPD
target-site substitution with accession-level sequence support is found. For the
current project, HPPD advances as:

1. a plant HPPD structure module using 5YWG and 1TG5;
2. a Fe/metal + inhibitor active-site-contact core;
3. an explicit negative/contrast case showing that not all herbicide target
   families yield validated field-evolved TSR mutations.
