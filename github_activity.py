import os
from dataclasses import dataclass
from typing import Any, List

from temporalio import activity

TASK_QUEUE_NAME = "temporal-community-task-queue"

from datetime import datetime, timedelta

from github import Github

# using an access token
g = Github(os.getenv("GITHUB_ACCESS_TOKEN"))


@dataclass
class GitHubRepo:
    name: str


@activity.defn
async def reviewers(gh: GitHubRepo) -> List[str]:
    repo = g.get_repo(gh.name)
    two_weeks_ago = datetime.utcnow() - timedelta(weeks=2)
    pull_requests = repo.get_pulls(state="all", sort="updated", direction="desc")
    recent_pull_requests = [
        pr
        for pr in pull_requests
        if pr.merged_at is not None and pr.merged_at >= two_weeks_ago
    ]
    activity.heartbeat("Getting reviewers and commenters")
    reviewers_and_commenters = [
        reviewer.login
        for pr in recent_pull_requests
        for reviewer in pr.requested_reviewers
    ] + [
        comment.user.login
        for pr in recent_pull_requests
        for comment in pr.get_issue_comments()
    ]
    return list(set(reviewers_and_commenters))


@activity.defn
async def get_name_of_user(reviewers_and_commenters) -> List[str]:
    print("Reviewers and commenters in the last two weeks:")
    user_name = []
    for user in reviewers_and_commenters:
        real_name = g.get_user(user).name
        if real_name is not None:
            user_name.append(real_name)
            print(real_name)
        else:
            user_name.append(user)
            print(user)

    return user_name
