{% snapshot snap_apps %}

{{ config(
    target_schema='main',
    unique_key='app_id',
    strategy='check',
    check_cols=['category_name', 'developer_name', 'price']
) }}

SELECT * FROM {{ ref('stg_playstore_apps') }}

{% endsnapshot %}
