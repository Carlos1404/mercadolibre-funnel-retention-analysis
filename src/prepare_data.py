"""
prepare_data.py

Convierte el resumen ejecutivo original en archivos CSV procesados.
Uso:
    python src/prepare_data.py
"""
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_FILE = BASE_DIR / "data" / "raw" / "proyecto_4_resumen_ejecutivo_original.xlsx"
OUT_DIR = BASE_DIR / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SHEETS = {
    "Embudo General": "funnel_general.csv",
    "Embudo General x Pais": "funnel_by_country.csv",
    "Retencion x Pais": "retention_by_country.csv",
    "Retencion x Cohort": "retention_by_cohort.csv",
}

def main() -> None:
    for sheet_name, output_file in SHEETS.items():
        df = pd.read_excel(RAW_FILE, sheet_name=sheet_name)
        df = df.dropna(how="all").dropna(axis=1, how="all")

        if sheet_name == "Embudo General":
            df = df.T.reset_index()
            df.columns = ["stage", "conversion_pct"]

        if sheet_name == "Retencion x Cohort":
            df["cohort"] = pd.to_datetime(df["cohort"], unit="D", origin="1899-12-30", errors="coerce")
            df["cohort"] = df["cohort"].dt.strftime("%Y-%m-%d")

        df.to_csv(OUT_DIR / output_file, index=False, encoding="utf-8")

if __name__ == "__main__":
    main()
