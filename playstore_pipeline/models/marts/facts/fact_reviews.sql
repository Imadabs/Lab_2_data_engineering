{{ config(materialized='incremental', unique_key='review_sk') }}

WITH 
{% if is_incremental() %}
watermark AS (
    SELECT MAX(review_at) AS max_review_at FROM {{ this }}
),
{% endif %}

reviews AS (
    SELECT
        r.*
        {% if is_incremental() %},
        w.max_review_at
        {% endif %}
    FROM {{ ref('stg_playstore_reviews') }} r
    {% if is_incremental() %}
    CROSS JOIN watermark w
    WHERE r.review_at > w.max_review_at
    {% endif %}
),

apps AS (
    SELECT app_sk, app_id FROM {{ ref('dim_apps') }}
),

dates AS (
    SELECT date_key, date_day FROM {{ ref('dim_date') }}
)

SELECT
    r.review_sk,
    r.review_id,
    a.app_sk,
    d.date_key,
    r.review_at,
    r.review_score,
    r.thumbs_up_count,
    r.user_name,
    r.review_text
FROM reviews r
LEFT JOIN apps a ON r.app_id = a.app_id
LEFT JOIN dates d ON r.review_at::DATE = d.date_day
WHERE a.app_sk IS NOT NULL
  AND d.date_key IS NOT NULL
