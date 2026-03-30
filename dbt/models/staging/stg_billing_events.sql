with raw as (
    select * from read_csv_auto('data/raw/billing_events.csv')
)

select
    event_id,
    customer_id,
    product_id,
    category,
    amount::double as amount,
    status,
    -- to_timestamp(event_time, 'YYYY-MM-DD HH24:MI:SS') as event_time
    -- to_timestamp(event_time) as event_time
    event_time
from raw