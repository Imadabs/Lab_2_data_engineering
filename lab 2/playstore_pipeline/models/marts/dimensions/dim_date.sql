WITH date_spine AS (
    SELECT UNNEST(
        generate_series(
            (SELECT MIN(review_at::DATE) FROM {{ ref('stg_playstore_reviews') }}),
            (SELECT MAX(review_at::DATE) FROM {{ ref('stg_playstore_reviews') }}),
            INTERVAL '1 day'
        )
    ) AS date_day
)

SELECT
    CAST(strftime(date_day::DATE, '%Y%m%d') AS INT)     AS date_key,
    date_day::DATE                                       AS date_day,
    YEAR(date_day)                                       AS year,
    QUARTER(date_day)                                    AS quarter,
    MONTH(date_day)                                      AS month,
    strftime(date_day::DATE, '%B')                       AS month_name,
    WEEKOFYEAR(date_day)                                 AS week_of_year,
    DAYOFWEEK(date_day)                                  AS day_of_week,
    strftime(date_day::DATE, '%A')                       AS day_name,
    CASE WHEN DAYOFWEEK(date_day) IN (0, 6) THEN TRUE ELSE FALSE END AS is_weekend
FROM date_spine
ORDER BY date_day
