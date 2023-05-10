import asyncio
import os
from dataclasses import dataclass
from datetime import timedelta
from temporalio import activity, workflow
from typing import Optional
from temporalio.client import Client, TLSConfig
from temporalio.worker import Worker
with workflow.unsafe.imports_passed_through():
    from github_activity import TASK_QUEUE_NAME
@dataclass
class ComposeGreetingInput:
    greeting: str
    name: str


# Basic activity that logs and does string concatenation
@activity.defn
async def compose_greeting(input: ComposeGreetingInput) -> str:
    return f"{input.greeting}, {input.name}!"


# Basic workflow that logs and invokes an activity
@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            compose_greeting,
            ComposeGreetingInput("Hello", name),
            start_to_close_timeout=timedelta(seconds=10),
        )

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
    print("Connected to Temporal server with mTLS")

    async with Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[GreetingWorkflow],
        activities=[compose_greeting],
    ):

        # While the worker is running, use the client to run the workflow and
        # print out its result. Note, in many production setups, the client
        # would be in a completely separate process from the worker.
        result = await client.execute_workflow(
            GreetingWorkflow.run,
            "World",
            id="hello-mtls-workflow-id",
            task_queue=TASK_QUEUE_NAME,
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
