"""
This ChatFunction commits changes and pushes them to a specified GitHub repository.
The GitHub authentication token is expected to be provided via an environment variable named GITHUB_TOKEN.
"""

from functions.chatfunction import ChatFunction
from typing import Dict
import subprocess
import os

from tomgpt.helper import get_root_directory

class SaveToGithubFunction(ChatFunction):

    def __init__(self, root, repository, branch):
        self.root = root
        self.repository = repository
        self.branch = branch

    @property
    def name(self) -> str:
        return "save_to_github"

    @property
    def description(self) -> str:
        return "Commits changes and pushes them to a GitHub repository using an authentication token from an environment variable."

    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The commit message."
                }
            },
            "required": ["message"]
        }

    def execute(self, **kwargs) -> Dict:
        message = kwargs.get('message')
        github_token = os.getenv('GITHUB_TOKEN')  # Expecting the token to be in an environment variable for security
        response = {}
        print(get_root_directory())
        try:
            subprocess.run(['git', 'add', '.'], check=True, cwd=get_root_directory())
            subprocess.run(['git', 'commit', '-m', message], check=True, cwd=self.root)
            subprocess.run(['git', 'remote', 'add', 'origin', f'https://x-access-token:{github_token}@github.com/{self.repository}.git'], check=True, cwd=self.root)
            subprocess.run(['git', 'pull', 'origin', self.branch], check=True, cwd=self.root)
            subprocess.run(['git', 'push', 'origin', self.branch], check=True, cwd=self.root)

            response['message'] = "Changes have been successfully committed and pushed to GitHub."
        except subprocess.CalledProcessError as e:
            response['error'] = f"A Git error occurred: {e.stderr}"

        return response
