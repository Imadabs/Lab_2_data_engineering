WITH source AS (
    SELECT DISTINCT
        developer_id,
        developer_name
    FROM {{ ref('stg_playstore_apps') }}
    WHERE developer_id IS NOT NULL
)

SELECT
    md5(CAST(developer_id AS VARCHAR))  AS developer_sk,
    developer_id,
    developer_name
FROM source
