with customers as (
    select distinct user_id as customer_id
    from {{ ref('stg_ecommerce__users') }}
),

customer_orders as (
    select
        user_id as customer_id,
        min(purchased_at) as first_order_date,
        max(purchased_at) as last_order_date,
        count(distinct purchase_id) as total_orders,
        sum(total_price) as total_spent
    from {{ ref('stg_ecommerce__purchases') }}
    group by 1
),

customer_events as (
    select
        user_id as customer_id,
        count(*) as total_events,
        count(distinct event_type) as unique_event_types
    from {{ ref('stg_ecommerce__events') }}
    group by 1
)

select
    c.customer_id,
    co.first_order_date,
    co.last_order_date,
    co.total_orders,
    co.total_spent,
    ce.total_events,
    ce.unique_event_types
from customers as c
left join customer_orders as co on c.customer_id = co.customer_id
left join customer_events as ce on c.customer_id = ce.customer_id
