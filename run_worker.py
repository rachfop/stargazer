import asyncio
import os
from typing import Any, List, Optional

from temporalio.client import Client
from temporalio.worker import Worker

from github_activity import TASK_QUEUE_NAME, StarGazersComposer
from github_workflows import GitHubWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    composer = StarGazersComposer(client)

    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[GitHubWorkflow],
        activities=[composer.compose_star_gazers, composer.complete_star_gazers],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
