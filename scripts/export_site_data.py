"""
Export the pipeline's own generated tables as JSON for the companion React site
(site/). This is a read-only export step - it never invents data, only converts
what scripts/rebuild_all.py already produced into a format the static site can
fetch at runtime. Run after rebuild_all.py, whenever the tables change:

    .venv/Scripts/python.exe scripts/export_site_data.py
"""
import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "site" / "public" / "data"

SOURCES = {
    "mutations.json": REPO_ROOT / "output/tables/phase4_master_mutation_table.csv",
    "permutation_summary.json": REPO_ROOT / "output/tables/manuscript_table_1_family_permutation_summary.csv",
    "mechanisms.json": REPO_ROOT / "output/tables/manuscript_table_2_unique_position_mechanisms.csv",
    "hppd_contrast.json": REPO_ROOT / "output/tables/manuscript_table_3_hppd_contrast_status.csv",
    "phase5_risk_table.json": REPO_ROOT / "data/processed/phase5_risk_table.csv",
    "phase5_target_status.json": REPO_ROOT / "data/processed/phase5_target_status.csv",
}

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


if __name__ == "__main__":
    main()
