select
    user_id,
    name,
    email,
    registration_date
from {{ dbt_twirl.twirl_ref('twirldata-demo', 'raw_ecommerce', 'users') }}
