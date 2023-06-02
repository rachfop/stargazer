from datetime import timedelta
from typing import Any, List

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from github_activity import GitHubRepo, star_gazers


@workflow.defn
class GitHubWorkflow:
    @workflow.run
    async def run(self, repo: GitHubRepo) -> List[Any]:
        return await workflow.execute_activity(
            star_gazers,
            repo,
            start_to_close_timeout=timedelta(seconds=3600),
        )
