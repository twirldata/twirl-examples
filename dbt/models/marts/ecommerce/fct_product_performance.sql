with product_sales as (
    select
        product_id,
        date(purchased_at) as date,
        count(distinct purchase_id) as daily_orders,
        sum(quantity) as daily_quantity_sold,
        sum(total_price) as daily_revenue
    from {{ ref('stg_ecommerce__purchases') }}
    group by 1, 2
),

product_views as (
    select
        product_id,
        date(viewed_at) as date,
        count(*) as daily_views
    from {{ ref('stg_ecommerce__pageviews') }}
    group by 1, 2
),

product_events as (
    select
        product_id,
        date(event_at) as date,
        count(*) as daily_events,
        count(distinct event_type) as daily_unique_events
    from {{ ref('stg_ecommerce__events') }}
    group by 1, 2
)

select
    coalesce(ps.product_id, pv.product_id, pe.product_id) as product_id,
    coalesce(ps.date, pv.date, pe.date) as date,
    ps.daily_orders,
    ps.daily_quantity_sold,
    ps.daily_revenue,
    pv.daily_views,
    pe.daily_events,
    pe.daily_unique_events
from product_sales as ps
full outer join product_views as pv on ps.product_id = pv.product_id and ps.date = pv.date
full outer join product_events
    as pe on coalesce(ps.product_id, pv.product_id) = pe.product_id
and coalesce(ps.date, pv.date) = pe.date
