import asyncio
import datetime

import matplotlib.pyplot as plt
import pandas as pd
from temporalio.client import Client

from github_activity import TASK_QUEUE_NAME, GitHubRepo
from github_workflows import GitHubWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    recent_reviewers = await client.execute_workflow(
        GitHubWorkflow.run,
        GitHubRepo(name="score-spec/spec"),
        id="github-workflow",
        task_queue=TASK_QUEUE_NAME,
    )
    df = pd.DataFrame(recent_reviewers)
    df["created_at"] = pd.to_datetime(
        df["created_at"]
    )  # Ensure 'created_at' is treated as a date
    df["qualifications"] = df.apply(
        lambda row: int(
            (row["followers"] < 2)
            and (row["following"] < 2)
            and (row["public_gists"] == 0)
            and (row["public_repos"] < 5)
            and (row["created_at"].date() > datetime.date(2022, 1, 1))
            and (row["email"] is None)
            and (row["bio"] is None)
            and (not row["blog"])
            and not isinstance(row["hireable"], bool)
        ),
        axis=1,
    )
    print(df)

    plt.scatter(df["followers"], df["public_repos"])
    plt.xlabel("Followers")
    plt.ylabel("Public Repos")
    plt.title("Followers vs Public Repos")
    plt.show()

    return df

    # print(recent_reviewers)


if __name__ == "__main__":
    asyncio.run(main())
