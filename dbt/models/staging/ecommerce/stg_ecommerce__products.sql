select
    product_id,
    name as product_name,
    category,
    price
from {{ dbt_twirl.twirl_ref('twirldata-demo', 'raw_ecommerce', 'products') }}
