with products as (
    select * from {{ ref('stg_ecommerce__products') }}
),

product_orders as (
    select
        product_id,
        count(distinct purchase_id) as total_orders,
        sum(quantity) as total_quantity_sold,
        sum(total_price) as total_revenue
    from {{ ref('stg_ecommerce__purchases') }}
    group by 1
),

product_views as (
    select
        product_id,
        count(*) as total_views
    from {{ ref('stg_ecommerce__pageviews') }}
    group by 1
)

select
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    po.total_orders,
    po.total_quantity_sold,
    po.total_revenue,
    pv.total_views
from products as p
left join product_orders as po on p.product_id = po.product_id
left join product_views as pv on p.product_id = pv.product_id
