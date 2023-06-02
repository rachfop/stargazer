# README

This repo uses GitHub's API to get the users who've starred a repo, and then sends those users to a Pandas DataFrame.

The Asynchronous Activity returns data back to the Workflow while the Activity is running, so you can begin to process some data, without having to wait for the Activity to finish, in cases where you've reached the API's rate limit.

## Getting started

The GitHub API requires authentication. To authenticate, you'll need to create a personal access token. You can do that by following the instructions [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

To use the token, export it as an environmental variable:


```bash
export GITHUB_TOKEN=`<your token>`
```

## Run the Workflow
Then, you can run the Workflow with the following command:

```bash
# terminal one
poetry run python run_worker.py
# terminal two
poetry run python run_workflow.py
```


