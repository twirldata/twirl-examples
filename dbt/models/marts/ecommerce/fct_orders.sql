with orders as (
    select * from {{ ref('stg_ecommerce__purchases') }}
),

products as (
    select * from {{ ref('stg_ecommerce__products') }}
)

select
    o.purchase_id,
    o.user_id as customer_id,
    o.product_id,
    o.quantity,
    o.total_price,
    o.purchased_at,
    p.product_name,
    p.category as product_category,
    p.price as unit_price,
    (o.total_price - (p.price * o.quantity)) as discount_amount
from orders as o
left join products as p on o.product_id = p.product_id
