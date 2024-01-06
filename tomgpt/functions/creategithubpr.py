"""
This ChatFunction commits changes and pushes them to a specified GitHub repository.
The GitHub authentication token is expected to be provided via an environment variable named GITHUB_TOKEN.
"""

from tomgpt.functions.chatfunction import ChatFunction
from typing import Dict
import subprocess
import os

from tomgpt.helper import get_root_directory

class CreateGithubPRFunction(ChatFunction):

    def __init__(self, repo: str) -> None:
        super().__init__()
        self.repo = repo

    @property
    def name(self) -> str:
        return "save_to_github"

    @property
    def description(self) -> str:
        return "Commits changes and pushes them to a GitHub repository."

    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The commit message. Please include brief description of any changes."
                },
                "branch": {
                    "type": "string",
                    "description": "The name of the branch to push to."
                }
            },
            "required": ["message", "branch"]
        }

    def execute(self, **kwargs) -> Dict:
        message = kwargs.get('message')
        branch = kwargs.get('branch')
        github_token = os.getenv('GITHUB_TOKEN')  # Expecting the token to be in an environment variable for security
        repository = self.repo
        response = {}

        try:
            # add changes
            subprocess.run(['git', 'add', '.'], check=True, cwd=get_root_directory())

            # check if the branch exists on the remote
            proc = subprocess.run(['git', 'ls-remote', '--heads', 'origin', branch], check=True, stdout=subprocess.PIPE, cwd=get_root_directory())
            branch_exists = branch in proc.stdout.decode()

            # create new branch if not exists
            if not branch_exists:
                subprocess.run(['git', 'checkout', '-b', branch], check=True, cwd=get_root_directory())

            # commit changes
            subprocess.run(['git', 'commit', '-m', message], check=True, cwd=get_root_directory())

            # pull the latest changes from the branch
            subprocess.run(['git', 'pull', 'origin', branch], check=True, cwd=get_root_directory())

            # push the branch to the remote
            subprocess.run(['git', 'push', '--set-upstream', 'origin', branch], check=True, cwd=get_root_directory())

            response['message'] = f"Changes have been successfully committed and pushed to {branch}."
        except subprocess.CalledProcessError as e:
            response['error'] = f"A Git error occurred: {str(e)}"

        return response
