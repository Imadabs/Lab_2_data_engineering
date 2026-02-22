WITH source AS (
    SELECT * FROM {{ ref('src_playstore_reviews') }}
)

SELECT
    md5(CAST(reviewId AS VARCHAR))      AS review_sk,
    reviewId::VARCHAR                   AS review_id,
    appId                               AS app_id,
    userName                            AS user_name,
    CAST(score AS INT)                  AS review_score,
    content                             AS review_text,
    CAST("at" AS TIMESTAMP)               AS review_at,
    CAST(thumbsUpCount AS INT)          AS thumbs_up_count
FROM source
WHERE reviewId IS NOT NULL
