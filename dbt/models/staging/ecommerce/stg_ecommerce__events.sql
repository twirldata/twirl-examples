select
    event_id,
    user_id,
    product_id,
    event_type,
    timestamp as event_at
from {{ dbt_twirl.twirl_ref('twirldata-demo', 'raw_ecommerce', 'events') }}
