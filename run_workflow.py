import asyncio

from temporalio.client import Client

from github_activity import TASK_QUEUE_NAME, GitHubRepo
from github_workflows import GitHubWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")

    recent_reviewers = await client.execute_workflow(
        GitHubWorkflow.run,
        GitHubRepo(name="temporalio/documentation"),
        id="github-workflow",
        task_queue=TASK_QUEUE_NAME,
    )
    print(recent_reviewers)


if __name__ == "__main__":
    asyncio.run(main())
