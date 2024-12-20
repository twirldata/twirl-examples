select
    _airbyte_pull_requests_hashid as id,
    created_at,
    closed_at,
    merged_at,
    number as github_issue_nr,
    url,
    base,
    body,
    head,
    JSON_VALUE(user, "$.id") as user_id,
    JSON_VALUE(user, "$.login") as login,
    draft,
    state,
    title,
    _links,
    labels,
    locked,
    node_id,
    assignee,
    diff_url,
    html_url,
    assignees,
    issue_url,
    milestone,
    patch_url,
    auto_merge,
    repository,
    updated_at,
    commits_url,
    comments_url,
    statuses_url,
    requested_teams,
    merge_commit_sha,
    active_lock_reason,
    author_association,
    review_comment_url,
    requested_reviewers,
    review_comments_url
from `twirldata-demo.raw_github.pull_requests`
