WITH events AS (
    SELECT * FROM {{ ref('stg_billing_events') }}
)

SELECT
    date(event_time) AS dt,
    product_id,
    category,
    count(*) AS event_count,
    sum(amount) AS total_amount,
    sum(CASE WHEN status = 'paid' THEN 1 ELSE 0 END) AS paid_count
FROM events
GROUP BY 1,2,3
ORDER BY 1 DESC