select
    id as pull_request_id,
    created_at,
    timestamp_diff(
        coalesce(merged_at, closed_at), created_at, minute
    ) / 60 as closing_time_hours
from `twirldata-demo.clean.pull_requests`
where coalesce(merged_at, closed_at) is not null
