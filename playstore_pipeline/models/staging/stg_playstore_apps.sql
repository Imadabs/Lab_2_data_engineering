WITH source AS (
    SELECT * FROM {{ ref('src_playstore_apps') }}
)

SELECT
    md5(CAST(appId AS VARCHAR))         AS app_sk,
    CAST(appId AS VARCHAR)              AS app_id,
    title                               AS app_name,
    developer                           AS developer_name,
    developerId                         AS developer_id,
    genre                               AS category_name,
    genreId                             AS category_id,
    CAST(score AS DOUBLE)               AS avg_score,
    CAST(ratings AS BIGINT)             AS total_ratings,
    CAST(price AS DOUBLE)               AS price
FROM source
WHERE appId IS NOT NULL
