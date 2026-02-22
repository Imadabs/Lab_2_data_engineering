# Google Play Store Data Pipeline Documentation

This document explains the end-to-end flow of the data pipeline, from raw data scraping to the final export for visualization.

## Project Structure Overview

The project is structured into three main phases: Ingestion, Transformation (dbt), and Export.

```text
c:\Users\bellm\Desktop\lab 2\
│
├── ingest.py                           # 1. Data Ingestion script
├── export_to_powerbi.py                # 3. Data Export script
├── requirements.txt                    # Python dependencies
├── dbt_run_output.txt                  # Logs for the dbt run execution
│
├── playstore_pipeline/                 # 2. dbt Project (Data Transformation)
│   ├── dbt_project.yml                 # dbt configuration
│   ├── profiles.yml                    # DuckDB connection profile
│   ├── data/                           
│   │   ├── raw/                        # Raw JSONL files from ingest.py
│   │   └── db/                         # DuckDB database (playstore.db)
│   ├── models/                         # SQL Transformation models
│   │   ├── staging/                    # Base views over raw jsonl files
│   │   └── marts/                      # Dimension and Fact tables
│   │       ├── dimensions/             
│   │       └── facts/                  
│   └── ...                             # Other standard dbt folders (macros, tests, etc.)
│
└── powerbi_export/                     # Final output directory containing CSVs
```

## End-to-End Pipeline Flow

### 1. Data Ingestion (`ingest.py`)
**Input:** A hardcoded list of popular Google Play Store App IDs.
**Process:** 
- The script uses the `google-play-scraper` Python package to fetch live data from the Google Play Store.
- It scrapes **App Metadata** (title, developer, category, ratings, etc.).
- It scrapes **User Reviews** (filtered to the last 100 days, up to a maximum of 5,000 reviews per app).
**Output:** The script saves the scraped data into two JSONL (JSON Lines) files in the `playstore_pipeline\data\raw\` directory:
- `apps.jsonl`
- `reviews.jsonl`

### 2. Data Transformation (`playstore_pipeline` using dbt & DuckDB)
**Input:** The raw JSONL files (`apps.jsonl` and `reviews.jsonl`).
**Process:** 
- The project uses **dbt (data build tool)** backed by **DuckDB** as the analytical database engine.
- DuckDB directly reads the JSONL files.
- The dbt models inside `playstore_pipeline\models\` structure the data linearly:
  - **Staging (`models/staging/`):** Cleans, casts, and renames columns from the raw unstructured JSON into tabular formats (`stg_playstore_apps.sql`, `stg_playstore_reviews.sql`).
  - **Marts - Dimensions (`models/marts/dimensions/`):** Creates descriptive lookup tables for analysis (`dim_apps`, `dim_categories`, `dim_developers`, `dim_date`, `dim_apps_scd`).
  - **Marts - Facts (`models/marts/facts/`):** Creates the central `fact_reviews` table storing the individual review transactions and associated scores.
**Output:** Structured tables within the DuckDB database file located at `playstore_pipeline\data\db\playstore.db`.

### 3. Data Export (`export_to_powerbi.py`)
**Input:** The mart-level tables inside the compiled DuckDB database (`playstore.db`).
**Process:** 
- The script connects to the DuckDB database.
- It queries the dimension tables (`dim_apps`, `dim_categories`, `dim_developers`, `dim_date`, `dim_apps_scd`) and the fact table (`fact_reviews`).
- It extracts the complete records from these analytical tables.
**Output:** The tables are written out as individual `CSV` files in the `powerbi_export\` folder:
- `powerbi_export\dim_apps.csv`
- `powerbi_export\dim_categories.csv`
- `powerbi_export\dim_developers.csv`
- `powerbi_export\dim_date.csv`
- `powerbi_export\dim_apps_scd.csv`
- `powerbi_export\fact_reviews.csv`

---
*Note: The final .csv files are then ready to be loaded into business intelligence tools for visualization.*
