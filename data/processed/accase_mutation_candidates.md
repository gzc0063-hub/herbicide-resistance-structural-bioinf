# ACCase Mutation Candidate Resolution

## Primary-source anchors

- **Delye et al. 2005, Plant Physiology 137:794-806** is the primary ACCase
  numbering and structure anchor. The paper states that the black-grass
  chloroplastic ACCase reference is **AJ310767** and that all positions use that
  numbering. It also uses yeast CT-domain structures **1UYT** and **1UYS** as
  templates and gives the aligned black-grass CT span as Leu1639-Leu2204.
- **Yu et al. 2007, Plant Physiology 145:547-558** independently detects the
  known ACCase mutations Ile1781Leu, Trp2027Cys, Ile2041Asn, Asp2078Gly and the
  new Cys2088Arg in resistant *Lolium* populations. It deposits the 2088-region
  sequence set as **EF538937-EF538943**.

## Accepted ACCase seed rows

| Mutation | Reference numbering | 1UYS mapped position | Primary evidence |
|---|---:|---|---|
| Ile1781Leu | AJ310767 1781 | chain C residue 1705 | Delye 2005 / Yu 2007 |
| Trp2027Cys | AJ310767 2027 | chain B residue 1953 | Delye 2005 / Yu 2007 |
| Ile2041Asn | AJ310767 2041 | chain B residue 1967 | Delye 2005 / Yu 2007 |
| Asp2078Gly | AJ310767 2078 | chain B residue 2004 | Delye 2005 / Yu 2007 |
| Cys2088Arg | AJ310767-equivalent 2088 | chain B residue 2014 | Yu 2007, EF538937-EF538943 |
| Gly2096Ala | AJ310767 2096 | chain B residue 2022 | Delye 2005 |

## Caveat

Unlike EPSPS, ACCase does not have a clean paired full-length resistant and
susceptible accession for each mutation. These rows are therefore treated as
**reference-numbered target-site substitutions**, not as resistant/susceptible
full-length allele pairs. This is acceptable because the source papers explicitly
state the reference accession/numbering system and mutation identities.
