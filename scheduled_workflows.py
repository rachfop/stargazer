# @@@SNIPSTART data-pipeline-schedule-workflow-python
import asyncio
from datetime import timedelta

from temporalio.client import (Client, Schedule, ScheduleActionStartWorkflow,
                               ScheduleIntervalSpec, ScheduleSpec)

from github_activity import TASK_QUEUE_NAME
from github_workflows import GitHubRepo, GitHubWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    await client.create_schedule(
        "reviewers-commenters-schedule",
        Schedule(
            action=ScheduleActionStartWorkflow(
                GitHubWorkflow.run,
                GitHubRepo(name="temporalio/documentation"),
                id="github-workflow",
                task_queue=TASK_QUEUE_NAME,
            ),
            spec=ScheduleSpec(
                intervals=[ScheduleIntervalSpec(every=timedelta(days=14))]
            ),
        ),
    )


if __name__ == "__main__":
    asyncio.run(main())
