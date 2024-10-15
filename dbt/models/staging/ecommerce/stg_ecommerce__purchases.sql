select
    purchase_id,
    user_id,
    product_id,
    quantity,
    total_price,
    timestamp as purchased_at
from {{ dbt_twirl.twirl_ref('twirldata-demo', 'raw_ecommerce', 'purchases') }}
