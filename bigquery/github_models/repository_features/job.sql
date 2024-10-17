select
    repository,
    avg(
        timestamp_diff(
            coalesce(merged_at, closed_at), created_at, minute
        ) / 60
    ) as repository_average_pr_closing_time
from `twirldata-demo.clean.pull_requests`
where coalesce(merged_at, closed_at) is not null
group by repository
