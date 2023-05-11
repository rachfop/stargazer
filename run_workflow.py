import asyncio
import os
from typing import Optional
from temporalio.client import Client, TLSConfig

from github_activity import TASK_QUEUE_NAME, GitHubRepo
from github_workflows import GitHubWorkflow


async def main() -> None:
    with open(os.getenv("TEMPORAL_MTLS_TLS_CERT"), "rb") as f:
            client_cert = f.read()

    with open(os.getenv("TEMPORAL_MTLS_TLS_KEY"), "rb") as f:
        client_key = f.read()


    server_root_ca_cert: Optional[bytes] = None
    
    client = await Client.connect(
        os.getenv("TEMPORAL_HOST_URL"),
        namespace=os.getenv("TEMPORAL_NAMESPACE"),
        tls=TLSConfig(
            server_root_ca_cert=server_root_ca_cert,
            client_cert=client_cert,
            client_private_key=client_key,
        ),
    )

    recent_reviewers = await client.execute_workflow(
        GitHubWorkflow.run,
        GitHubRepo(name="temporalio/documentation"),
        id="github-workflow",
        task_queue=TASK_QUEUE_NAME,
    )
    print(recent_reviewers)


if __name__ == "__main__":
    asyncio.run(main())
