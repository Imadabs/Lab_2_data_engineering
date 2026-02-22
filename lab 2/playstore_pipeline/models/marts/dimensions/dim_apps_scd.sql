WITH snapshot_data AS (
    SELECT * FROM {{ ref('snap_apps') }}
)

SELECT
    app_sk,
    app_id,
    app_name,
    developer_name,
    developer_id,
    category_name,
    category_id,
    avg_score,
    total_ratings,
    price,
    dbt_valid_from,
    dbt_valid_to,
    CASE WHEN dbt_valid_to IS NULL THEN TRUE ELSE FALSE END AS is_current
FROM snapshot_data
