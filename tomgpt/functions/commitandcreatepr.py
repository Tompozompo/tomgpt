"""
Function to commit changes and create a pull request on GitHub.
"""

from tomgpt.functions.chatfunction import ChatFunction
from typing import Dict
import subprocess
import requests
import os

from tomgpt.helper import get_root_directory

class CommitAndCreatePRFunction(ChatFunction):

    def __init__(self, repo: str) -> None:
        super().__init__()
        self.repo = repo

    @property
    def name(self) -> str:
        return "commit_and_create_pr"

    @property
    def description(self) -> str:
        return "Commits changes and creates a pull request on GitHub."

    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "branch": {
                    "type": "string",
                    "description": "The name of the branch to commit to."
                },
                "message": {
                    "type": "string",
                    "description": "The commit message."
                }
            },
            "required": ["branch", "message"]
        }

    def execute(self, **kwargs) -> Dict:
        branch = kwargs.get('branch')
        message = kwargs.get('message')
        response = {}
        try:
            # add changes
            subprocess.run(['git', 'add', '.'], check=True, cwd=get_root_directory())
            # commit changes
            subprocess.run(['git', 'commit', '-m', message], check=True, cwd=get_root_directory())
            # push the branch to the remote
            subprocess.run(['git', 'push', '--set-upstream', 'origin', branch], check=True, cwd=get_root_directory())
            # use GitHub API to create PR
            github_token = os.getenv('GITHUB_TOKEN')
            if github_token:
                headers = {'Authorization': f'token {github_token}'}
                payload = {
                    'title': message,
                    'head': branch,
                    'base': 'main',
                    'body': message
                }
                r = requests.post(f'https://api.github.com/repos/{self.repo}/pulls', headers=headers, json=payload)
                if r.status_code == 201:
                    response['message'] = 'Pull request created successfully.'
                else:
                    response['error'] = f"Failed to create pull request: {r.content}"
            else:
                response['error'] = 'GitHub token not found.'
        except subprocess.CalledProcessError as e:
            response['error'] = f"A Git error occurred: {str(e)}"
        return response

# Example usage
if __name__ == "__main__":
    try:
        ccpr = CommitAndCreatePRFunction('tomgpt')
        res = ccpr.execute(branch='test-branch', message='test message')
        print(res)
    except Exception as e:
        print(f"Caught an exception: {e}")
