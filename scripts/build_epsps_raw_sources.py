"""Copy fetched EPSPS source FASTAs into data/raw with stable names."""

from pathlib import Path


SOURCES = {
    "work/epsps_panel_fetch/Arabidopsis_thaliana_P05466.fasta": "data/raw/EPSPS_conservation_Arabidopsis_thaliana_P05466.fasta",
    "work/epsps_panel_fetch/Nicotiana_tabacum_P23981.fasta": "data/raw/EPSPS_conservation_Nicotiana_tabacum_P23981.fasta",
    "work/epsps_panel_fetch/Glycine_max_I1JKP7.fasta": "data/raw/EPSPS_conservation_Glycine_max_I1JKP7.fasta",
    "work/epsps_panel_fetch/Oryza_sativa_A0A0N7KLH2.fasta": "data/raw/EPSPS_conservation_Oryza_sativa_A0A0N7KLH2.fasta",
    "work/epsps_panel_fetch/Solanum_lycopersicum_P10748.fasta": "data/raw/EPSPS_conservation_Solanum_lycopersicum_P10748.fasta",
    "work/epsps_panel_fetch/Populus_trichocarpa_B9GPE8.fasta": "data/raw/EPSPS_conservation_Populus_trichocarpa_B9GPE8.fasta",
    "work/epsps_panel_fetch/Zea_mays_8UMJ_Uniprot_A0A1D6NVZ6.fasta": "data/raw/EPSPS_conservation_Zea_mays_A0A1D6NVZ6.fasta",
}


def main():
    for source, target in SOURCES.items():
        text = Path(source).read_text(encoding="utf-8")
        Path(target).write_text(text, encoding="utf-8")
        print(target, text.splitlines()[0])


if __name__ == "__main__":
    main()
