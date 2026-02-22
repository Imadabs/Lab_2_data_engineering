WITH source AS (
    SELECT DISTINCT
        category_id,
        category_name
    FROM {{ ref('stg_playstore_apps') }}
    WHERE category_id IS NOT NULL
)

SELECT
    md5(CAST(category_id AS VARCHAR))   AS category_sk,
    category_id,
    category_name
FROM source
