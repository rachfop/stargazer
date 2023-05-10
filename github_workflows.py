# @@@SNIPSTART data-pipeline-your-workflow-python
from datetime import timedelta
from typing import Any, List

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from github_activity import GitHubRepo, get_name_of_user, reviewers


@workflow.defn
class GitHubWorkflow:
    @workflow.run
    async def run(self, repo: GitHubRepo):
        reviewer_user_name = await workflow.execute_activity(
            reviewers,
            repo,
            start_to_close_timeout=timedelta(seconds=360),
        )
        return await workflow.execute_activity(
            get_name_of_user,
            reviewer_user_name,
            start_to_close_timeout=timedelta(seconds=360),
        )
