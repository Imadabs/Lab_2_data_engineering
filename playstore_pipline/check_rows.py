import duckdb

con = duckdb.connect('data/db/playstore.db')

tables = ['dim_categories', 'dim_developers', 'dim_apps', 'dim_date', 'fact_reviews', 'dim_apps_scd']
print("=== FINAL ROW COUNTS ===")
for t in tables:
    try:
        n = con.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
        print(f'  {t}: {n:,} rows')
    except Exception as e:
        print(f'  {t}: ERROR - {e}')

print("\n=== SCD2 PROOF: com.whatsapp versions ===")
rows = con.execute("""
    SELECT app_id, category_name, dbt_valid_from, dbt_valid_to,
           CASE WHEN dbt_valid_to IS NULL THEN 'CURRENT' ELSE 'HISTORICAL' END AS version
    FROM snap_apps
    WHERE app_id = 'com.whatsapp'
    ORDER BY dbt_valid_from
""").fetchall()
for r in rows:
    print(f'  {r}')

con.close()
