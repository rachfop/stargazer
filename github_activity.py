from dataclasses import dataclass
from typing import Any, List
import os
from github import Github
from temporalio import activity


TASK_QUEUE_NAME = "stargazers_02"

# using an access token
g = Github(os.environ["GITHUB_TOKEN"])


@dataclass
class GitHubRepo:
    name: str


@activity.defn
async def star_gazers(gh: GitHubRepo) -> List[Any]:
    repo = g.get_repo(gh.name)
    stargazers = repo.get_stargazers()
    users = []
    activity.heartbeat("Getting stargazers")
    for user in stargazers:
        user_row = {
            "login": user.login,
            "followers": user.followers,
            "following": user.following,
            "public_gists": user.public_gists,
            "public_repos": user.public_repos,
            "created_at": user.created_at.date().isoformat(),
            "email": user.email,
            "bio": user.bio,
            "blog": user.blog,
            "hireable": user.hireable,
        }
        users.append(user_row)
    return users

