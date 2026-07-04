# HPPD active-site contrast results

Pipeline: `scripts/hppd_distance_sasa.py` on 5YWG, with 1TG5 used as the Fe(II)
plant-HPPD support structure.

## Structure choice

Primary structure: **5YWG**, *Arabidopsis thaliana* HPPD complexed with
mesotrione (`92L`) and cobalt (`CO`) in the deposited active site.

Supporting Fe(II) plant template: **1TG5**, *Arabidopsis thaliana* HPPD complexed
with Fe(II) (`FE2`) and the herbicidal inhibitor DAS645 (`645`).

Rationale:

- Both are plant HPPD structures, avoiding bacterial template drift.
- 5YWG contains mesotrione, the HPPD inhibitor most relevant to the weed-resistance
  literature found in the audit.
- 1TG5 preserves the native Fe(II) metallocenter in a plant HPPD inhibitor complex.
- Both PDB headers identify the biological assembly as dimeric.

## Active-site core definition

HPPD was not run as a mutation validation gate because the audit did not find a
verified weed-evolved HPPD target-site amino-acid substitution. Instead, the
structural output is an active-site-contact map.

For 5YWG, the active-site core is every protein residue with any atom within 4.5 A
of either:

- mesotrione (`92L`), or
- the deposited active-site metal (`CO`, cobalt substituting for the catalytic
  metal in 5YWG).

This gives **34 chain-residue core positions** across the A+B dimer, symmetric
between chains:

- Chain A: 226, 228, 267, 280, 282, 307, 308, 368, 379, 381, 392, 394, 419, 420,
  421, 423, 424.
- Chain B: 226, 228, 267, 280, 282, 307, 308, 368, 379, 381, 392, 394, 419, 420,
  421, 423, 424.

Key active-site sanity checks:

| Chain | Position | Residue | Contact class | Nearest ligand/metal distance | SASA |
|---|---:|---|---|---:|---:|
| A | 226 | HIS | metal coordinator | 2.50 A to `CO` | 0.0 A^2 |
| A | 308 | HIS | metal coordinator | 2.37 A to `CO` | 0.0 A^2 |
| A | 394 | GLU | metal coordinator | 2.07 A to `CO` | 0.0 A^2 |
| A | 424 | PHE | inhibitor-pocket residue | 3.38 A to `92L` | 66.6 A^2 |

For 1TG5, the equivalent Fe(II)+DAS645 contact core is:

- 205, 207, 242, 244, 246, 248, 259, 261, 287, 289, 358, 360, 371, 373, 398,
  399, 400, 402, 403, 406.

The 1TG5 metal-only contact check returns His205, His287, Glu373 plus nearby
positions, matching the 5YWG His226/His308/Glu394 metal-site logic after the
5YWG N-terminal extension/numbering difference.

## Interpretation

HPPD is included in the resource, but not as a TSR-positive family. Its role is to
show that the structural pipeline can still define a real plant herbicide-binding
pocket when the weed-resistance biology is dominated by non-target-site mechanisms.

Current manuscript-safe wording:

> HPPD was retained as a structural contrast case. Plant HPPD structures support a
> clear metal/inhibitor active-site definition, but the reviewed weed-resistance
> literature did not provide a verified field-evolved target-site amino-acid
> substitution suitable for mutation-level validation. Reported evolved weed
> resistance instead points primarily to enhanced metabolism, detoxification gene
> expression, and in some populations HPPD expression differences.

Do not report Gly336 as a weed-resistance mutation.
