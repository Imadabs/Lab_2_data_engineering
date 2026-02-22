"""
export_to_powerbi.py
Exports all mart tables from playstore.db to CSV files ready for Power BI.
"""
import duckdb
import os

DB_PATH = r"playstore_pipeline\data\db\playstore.db"
OUT_DIR = r"powerbi_export"

os.makedirs(OUT_DIR, exist_ok=True)

con = duckdb.connect(DB_PATH)

tables = [
    "dim_apps",
    "dim_categories",
    "dim_developers",
    "dim_date",
    "fact_reviews",
    "dim_apps_scd",
]

print("Exporting tables to CSV...")
for t in tables:
    path = os.path.join(OUT_DIR, f"{t}.csv").replace("\\", "/")
    con.execute(f"COPY {t} TO '{path}' (HEADER, DELIMITER ',')")
    count = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  ✓ {t}.csv  ({count} rows)")

con.close()
print(f"\nDone! CSVs saved to: {os.path.abspath(OUT_DIR)}")
print("Open Power BI → Get Data → Text/CSV → import each file.")
