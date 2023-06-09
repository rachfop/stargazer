import asyncio
import os
from typing import Any, List, Optional

from temporalio.client import Client
from temporalio.worker import Worker

from github_activity import TASK_QUEUE_NAME, star_gazers
from github_workflows import GitHubWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[GitHubWorkflow],
        activities=[star_gazers],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
