select
    id as pull_request_id,
    created_at,
    COALESCE(LENGTH(title), 0) as title_n_characters,
    COALESCE(LENGTH(body), 0) as body_n_characters,
    ARRAY_LENGTH(labels) as n_labels,
    repository,
    login
from
    `twirldata-demo.clean.pull_requests`
