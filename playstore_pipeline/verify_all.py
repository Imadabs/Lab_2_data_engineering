import duckdb

con = duckdb.connect('data/db/playstore.db')

print("--- dim_date content (all rows) ---")
for r in con.execute("SELECT date_key, date_day, year, month, day_name, is_weekend FROM dim_date ORDER BY date_key").fetchall():
    print(r)

print("\n--- fact_reviews date_key distribution ---")
for r in con.execute("SELECT date_key, COUNT(*) FROM fact_reviews GROUP BY date_key ORDER BY date_key").fetchall():
    print(r)

print("\n--- fact_reviews: Reviews with no matching dim_date ---")
orphans = con.execute("SELECT COUNT(*) FROM fact_reviews WHERE date_key NOT IN (SELECT date_key FROM dim_date)").fetchone()[0]
print(f"Orphan date_keys: {orphans} (should be 0)")

print("\n--- SCD2 full proof ---")
rows = con.execute("SELECT app_id, category_name, dbt_valid_from, dbt_valid_to FROM snap_apps WHERE app_id='com.whatsapp' ORDER BY dbt_valid_from").fetchall()
print(f"Total versions for com.whatsapp: {len(rows)}")
for i, r in enumerate(rows):
    status = 'CURRENT' if r[3] is None else 'HISTORICAL'
    print(f"  Version {i+1} [{status}]: category='{r[1]}', valid_from={r[2]}, valid_to={r[3]}")

con.close()
