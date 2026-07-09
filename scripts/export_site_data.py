"""
Export the pipeline's own generated tables as JSON for the companion React site
(site/). This is a read-only export step - it never invents data, only converts
what scripts/rebuild_all.py already produced into a format the static site can
fetch at runtime. Run after rebuild_all.py, whenever the tables change:

    .venv/Scripts/python.exe scripts/export_site_data.py
"""
import csv
import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "site" / "public" / "data"
FIGURES_SRC_DIR = REPO_ROOT / "output" / "figures"
FIGURES_OUT_DIR = REPO_ROOT / "site" / "public" / "figures"

SOURCES = {
    "mutations.json": REPO_ROOT / "output/tables/phase4_master_mutation_table.csv",
    "permutation_summary.json": REPO_ROOT / "output/tables/manuscript_table_1_family_permutation_summary.csv",
    "mechanisms.json": REPO_ROOT / "output/tables/manuscript_table_2_unique_position_mechanisms.csv",
    "hppd_contrast.json": REPO_ROOT / "output/tables/manuscript_table_3_hppd_contrast_status.csv",
    "phase5_risk_table.json": REPO_ROOT / "data/processed/phase5_risk_table.csv",
    "phase5_target_status.json": REPO_ROOT / "data/processed/phase5_target_status.csv",
}

# Captions are copied verbatim from docs/MANUSCRIPT_DRAFT.md's "Figure Captions"
# section; "explanation" paraphrases the matching Results paragraph in plain
# language for a non-specialist reader. Keep both in sync with the manuscript
# by hand when the manuscript's figure text changes - these are prose, not a
# number derived from a CSV, so they cannot be auto-exported like the tables
# above.
FIGURES = [
    {
        "id": "figure_1_workflow",
        "svg": "figure_1_workflow.svg",
        "title": "Figure 1. Workflow and target families",
        "caption": (
            "The resource begins with source-verified mutation curation, maps accepted "
            "TSR positions to herbicide-relevant protein structures, defines active-site "
            "cores, calculates distance percentile/RSA/conservation, runs within-family "
            "permutation enrichment, and adds mechanism annotations. HPPD is retained as "
            "a contrast family with no accepted weed-evolved TSR mutation row."
        ),
        "explanation": (
            "This is the pipeline every other result on this site comes from. Verified "
            "resistance mutations are mapped onto real protein structures, an active site "
            "is defined for each enzyme, and every mutated residue is scored for how close "
            "it sits to that active site, how exposed it is to solvent, and how conserved "
            "it is across species. Four enzyme families - PPO, ALS/AHAS, ACCase, and EPSPS "
            "- go through this pipeline and are pooled into the main statistical analysis. "
            "A fifth, HPPD, is kept as a deliberate negative control: no weed-evolved "
            "target-site mutation was found for it, so it is shown separately rather than "
            "forced into the same analysis."
        ),
    },
    {
        "id": "figure_2_permutation_enrichment",
        "svg": "figure_2_permutation_enrichment.svg",
        "title": "Figure 2. Observed vs. random distance-to-core percentile by family",
        "caption": (
            "Accepted TSR positions in PPO, ALS/AHAS, ACCase, and EPSPS have much lower "
            "observed mean distance percentiles than same-size random residue sets sampled "
            "from the same family structures. EPSPS (n = 2 positions) is now directionally "
            "consistent and statistically significant, though still the smallest pooled "
            "family."
        ),
        "explanation": (
            "Across all four pooled families, the mutations weeds actually evolved sit far "
            "closer to the active site than random residues do. ACCase's six positions "
            "average the 13th percentile of closeness (random residues average the 50th); "
            "ALS/AHAS's five positions average the 5th percentile; PPO's four average the "
            "8th - all three highly significant (p ≤ 0.0004). EPSPS, now with two "
            "accepted positions instead of one, averages the 9th percentile and is also "
            "significant (p = 0.0147): a real improvement, since with only one position it "
            "wasn't statistically meaningful before."
        ),
    },
    {
        "id": "figure_3_position_screen",
        "svg": "figure_3_position_screen.svg",
        "title": "Figure 3. Unique mutation-position screen",
        "caption": (
            "Direct-core positions are separated from adjacent and non-core candidates so "
            "that the manuscript can distinguish direct ligand-pocket substitutions from "
            "mechanistically interesting second-shell, hinge, deletion, or "
            "interface-associated positions."
        ),
        "explanation": (
            "Not every resistance mutation touches the herbicide-binding pocket directly. "
            "This figure sorts mutations into direct-core (inside the pocket), "
            "adjacent/second-shell, and more distal categories. Direct-core mutations - "
            "like ALS Trp574Leu or PPO R98G - are the straightforward cases. The more "
            "interesting ones sit just outside the pocket: PPO ΔG210 is explained by a "
            "deletion that reshapes a nearby loop or helix rather than by direct contact, "
            "and EPSPS Pro106Ser reduces glyphosate binding despite sitting just outside "
            "the strict contact-distance cutoff."
        ),
    },
    {
        "id": "figure_4_distance_rsa_conservation",
        "svg": "figure_4_distance_rsa_conservation.svg",
        "title": "Figure 4. Distance percentile vs. RSA and conservation",
        "caption": (
            "The scatter view shows how accepted positions combine active-site proximity, "
            "solvent exposure, and conservation. These static metrics provide structural "
            "context but do not replace literature-supported dynamic or biochemical "
            "mechanism evidence."
        ),
        "explanation": (
            "This combines three structural measurements at once for each mutation: how "
            "close it is to the active site, how exposed it is to solvent, and how "
            "conserved it is across species. Most accepted resistance mutations are both "
            "close to the active site and highly conserved, consistent with resistance "
            "often arising at functionally constrained positions. But the metrics don't "
            "always agree - PPO V361A, for example, sits outside the core and has only "
            "modest conservation, so it is flagged here as an unresolved case rather than "
            "given a confident mechanism."
        ),
    },
    {
        "id": "figure_5_resistance_zone_map",
        "svg": "figure_5_resistance_zone_map.svg",
        "title": "Figure 5. Resistance-zone map",
        "caption": (
            "One lane per enzyme family; each accepted position is placed by its "
            "within-family distance-to-core percentile (left = closest to the "
            "ligand-contact core) and colored by mechanism label. The shaded left band "
            "marks the direct-contact core zone."
        ),
        "explanation": (
            "A single summary view: one lane per enzyme family, with each mutation placed "
            "by how close it sits to the active-site core (left = closest) and colored by "
            "its mechanism type. ALS/AHAS mutations cluster tightly in the direct-contact "
            "zone; PPO and ACCase span from direct-core out to more distal interface "
            "positions; EPSPS now shows one direct-core position (Thr102Ile) and one "
            "just-outside-the-pocket position (Pro106Ser)."
        ),
    },
]

FAMILY_META = {
    "PPO": {
        "name": "Protoporphyrinogen oxidase",
        "role": "Pilot family (validated first)",
        "pdb": "1SEZ",
        "species": "Nicotiana tabacum (tobacco)",
        "status": "pooled",
    },
    "ALS": {
        "name": "Acetohydroxyacid synthase (ALS/AHAS)",
        "role": "Pooled core family",
        "pdb": "1Z8N",
        "species": "reference structure",
        "status": "pooled",
    },
    "ACCase": {
        "name": "Acetyl-CoA carboxylase (CT domain)",
        "role": "Pooled core (homology model)",
        "pdb": "1UYS",
        "species": "Alopecurus myosuroides (black-grass) homology model",
        "status": "pooled",
    },
    "EPSPS": {
        "name": "5-enolpyruvylshikimate-3-phosphate synthase",
        "role": "Pooled core family",
        "pdb": "8UMJ",
        "species": "Zea mays (maize)",
        "status": "pooled",
    },
    "HPPD": {
        "name": "Hydroxyphenylpyruvate dioxygenase",
        "role": "Contrast / negative control",
        "pdb": "5YWG",
        "species": "Arabidopsis thaliana",
        "status": "contrast",
    },
    "FAT": {
        "name": "Acyl-ACP thioesterase",
        "role": "Phase 5 risk table (engineered variants only)",
        "pdb": "9GRR",
        "species": "Alopecurus myosuroides / Arabidopsis thaliana",
        "status": "phase5",
    },
    "DHODH": {
        "name": "Dihydroorotate dehydrogenase",
        "role": "Phase 5 risk table (no public structure)",
        "pdb": None,
        "species": "Arabidopsis thaliana (EMS lines)",
        "status": "phase5",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for out_name, src_path in SOURCES.items():
        rows = read_csv(src_path)
        out_path = OUT_DIR / out_name
        out_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        print(f"Wrote {out_path} ({len(rows)} rows)")

    families_path = OUT_DIR / "families.json"
    families_path.write_text(json.dumps(FAMILY_META, indent=2), encoding="utf-8")
    print(f"Wrote {families_path}")

    figures_path = OUT_DIR / "figures.json"
    figures_path.write_text(json.dumps(FIGURES, indent=2), encoding="utf-8")
    print(f"Wrote {figures_path}")

    FIGURES_OUT_DIR.mkdir(parents=True, exist_ok=True)
    for fig in FIGURES:
        src = FIGURES_SRC_DIR / fig["svg"]
        dst = FIGURES_OUT_DIR / fig["svg"]
        shutil.copyfile(src, dst)
        print(f"Copied {src} -> {dst}")


if __name__ == "__main__":
    main()
