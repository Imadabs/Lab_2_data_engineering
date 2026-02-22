WITH apps AS (
    SELECT * FROM {{ ref('stg_playstore_apps') }}
),

categories AS (
    SELECT * FROM {{ ref('dim_categories') }}
),

developers AS (
    SELECT * FROM {{ ref('dim_developers') }}
)

SELECT
    a.app_sk,
    a.app_id,
    a.app_name,
    a.price,
    a.avg_score,
    a.total_ratings,
    c.category_sk,
    d.developer_sk
FROM apps a
LEFT JOIN categories c ON a.category_id = c.category_id
LEFT JOIN developers d ON a.developer_id = d.developer_id
