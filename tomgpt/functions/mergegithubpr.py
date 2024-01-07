"""
Function to merge a pull request into the main branch on GitHub, and clean up by removing the branch.
"""

from tomgpt.functions.chatfunction import ChatFunction
from typing import Dict
import subprocess
import requests
import os

from tomgpt.helper import get_root_directory

class MergeGithubPRFunction(ChatFunction):

    def __init__(self, repo: str) -> None:
        super().__init__()
        self.repo = repo

    @property
    def name(self) -> str:
        return "merge_github_pr"

    @property
    def description(self) -> str:
        return "Merges a pull request into the main branch and cleans up the feature branch both locally and remotely."

    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "branch": {
                    "type": "string",
                    "description": "The name of the branch to merge and then delete."
                },
                "pr_number": {
                    "type": "integer",
                    "description": "The number of the pull request to merge."
                }
            },
            "required": ["branch", "pr_number"]
        }

    def execute(self, **kwargs) -> Dict:
        branch = kwargs.get('branch')
        pr_number = kwargs.get('pr_number')
        response = {}
        try:
            github_token = os.getenv('GITHUB_TOKEN')
            if github_token:
                headers = {'Authorization': f'token {github_token}'}
                # Merge PR using GitHub API
                merge_url = f'https://api.github.com/repos/{self.repo}/pulls/{pr_number}/merge'
                merge_response = requests.put(merge_url, headers=headers)
                if merge_response.status_code == 200:
                    response['message'] = 'Pull request merged successfully.'
                    # Delete remote branch
                    delete_url = f'https://api.github.com/repos/{self.repo}/git/refs/heads/{branch}'
                    delete_response = requests.delete(delete_url, headers=headers)
                    if delete_response.status_code == 204:
                        response['message'] += ' Remote branch deleted successfully.'
                        # Delete local branch
                        subprocess.run(['git', 'branch', '-d', branch], check=True, cwd=get_root_directory())
                        response['message'] += ' Local branch deleted successfully.'
                    else:
                        response['warning'] = f"Failed to delete remote branch. {delete_response.content}"
                else:
                    response['error'] = f"Failed to merge pull request. {merge_response.content}"
            else:
                response['error'] = 'GitHub token not found.'
        except subprocess.CalledProcessError as e:
            response['error'] = f"A Git error requiring local intervention occurred: {str(e)}"
        return response
