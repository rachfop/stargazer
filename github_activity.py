import asyncio
import os
from dataclasses import dataclass
from typing import Any, List

from github import Github
from temporalio import activity
from temporalio.client import Client

TASK_QUEUE_NAME = "stargazers"

# using an access token
g = Github(os.environ["GITHUB_ACCESS_TOKEN"])


@dataclass
class GitHubRepo:
    name: str


async def main():
    client = await Client.connect("localhost:7233")
    return client


class StarGazersComposer:
    def __init__(self, client: Client) -> None:
        self.client = client
        self.stargazers = []

    @activity.defn
    async def compose_star_gazers(self, gh: GitHubRepo) -> None:
        repo = g.get_repo(gh.name)
        stargazers = repo.get_stargazers()
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
            self.stargazers.append(user_row)

            # Check the rate limit and complete asynchronously if necessary
            if g.get_rate_limit().core.remaining == 0:
                _ = asyncio.create_task(
                    self.complete_star_gazers(activity.info().task_token)
                )
                activity.raise_complete_async()
                return  # Exit the method, so that the activity can be retried later

            # Complete asynchronously if we've gathered a batch of 100 users
            if len(self.stargazers) >= 100:
                _ = asyncio.create_task(
                    self.complete_star_gazers(activity.info().task_token)
                )
                activity.raise_complete_async()
                return  # Exit the method, so that the activity can be retried later

    @activity.defn
    async def complete_star_gazers(self, task_token) -> None:
        """
        This is an async function that completes a task using a task token and clears a list of stargazers.
        """
        handle = self.client.get_async_activity_handle(task_token=task_token)
        await handle.complete(self.stargazers)
        self.stargazers = []
