import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("id", twirl.String()),
                twirl.Column("created_at", twirl.Timestamp(unit="us", tz="UTC")),
                twirl.Column("closed_at", twirl.Timestamp(unit="us", tz="UTC")),
                twirl.Column("merged_at", twirl.Timestamp(unit="us", tz="UTC")),
                twirl.Column("github_issue_nr", twirl.Integer()),
                twirl.Column("url", twirl.String()),
                twirl.Column("base", twirl.String()),
                twirl.Column("body", twirl.String()),
                twirl.Column("head", twirl.String()),
                twirl.Column("user_id", twirl.String()),
                twirl.Column("login", twirl.String()),
                twirl.Column("draft", twirl.Bool()),
                twirl.Column("state", twirl.String()),
                twirl.Column("title", twirl.String()),
                twirl.Column("_links", twirl.String()),
                twirl.Column("labels", twirl.Array(value_type=twirl.String())),
                twirl.Column("locked", twirl.Bool()),
                twirl.Column("node_id", twirl.String()),
                twirl.Column("assignee", twirl.String()),
                twirl.Column("diff_url", twirl.String()),
                twirl.Column("html_url", twirl.String()),
                twirl.Column("assignees", twirl.Array(value_type=twirl.String())),
                twirl.Column("issue_url", twirl.String()),
                twirl.Column("milestone", twirl.String()),
                twirl.Column("patch_url", twirl.String()),
                twirl.Column("auto_merge", twirl.String()),
                twirl.Column("repository", twirl.String()),
                twirl.Column("updated_at", twirl.Timestamp(unit="us", tz="UTC"), is_event_time=True),
                twirl.Column("commits_url", twirl.String()),
                twirl.Column("comments_url", twirl.String()),
                twirl.Column("statuses_url", twirl.String()),
                twirl.Column("requested_teams", twirl.Array(value_type=twirl.String())),
                twirl.Column("merge_commit_sha", twirl.String()),
                twirl.Column("active_lock_reason", twirl.String()),
                twirl.Column("author_association", twirl.String()),
                twirl.Column("review_comment_url", twirl.String()),
                twirl.Column("requested_reviewers", twirl.Array(value_type=twirl.String())),
                twirl.Column("review_comments_url", twirl.String()),
            ]
        ),
        inputs=[
            twirl.Input("bigquery/raw_github/pull_requests"),
        ],
        job=twirl.BigQueryJob(update_method=twirl.UpdateMethod.REPLACE),
        tags=["engineering", "github_predictions"],
    )
)
