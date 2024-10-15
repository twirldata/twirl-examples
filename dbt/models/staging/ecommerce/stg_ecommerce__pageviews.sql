select
    pageview_id,
    user_id,
    product_id,
    timestamp as viewed_at
from {{ dbt_twirl.twirl_ref('twirldata-demo', 'raw_ecommerce', 'pageviews') }}
