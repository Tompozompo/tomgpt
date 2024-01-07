"""
Function to create a new branch on GitHub if it doesn't exist, checking both remote and local branches.
"""

from tomgpt.functions.chatfunction import ChatFunction
from typing import Dict
import subprocess
import os

from tomgpt.helper import get_root_directory

class CreateGithubBranchFunction(ChatFunction):

    def __init__(self, repo: str) -> None:
        super().__init__()
        self.repo = repo

    @property
    def name(self) -> str:
        return "create_github_branch"

    @property
    def description(self) -> str:
        return "Creates a new branch on GitHub if it doesn't exist, after checking remote and local branches."

    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "branch": {
                    "type": "string",
                    "description": "The name of the branch to create."
                }
            },
            "required": ["branch"]
        }

    def execute(self, **kwargs) -> Dict:
        branch = kwargs.get('branch')
        response = {}
        try:
            # check local branch existence
            local_branches = subprocess.run(['git', 'branch'], check=True, stdout=subprocess.PIPE, cwd=get_root_directory()).stdout.decode()
            # check remote branch existence
            remote_branches = subprocess.run(['git', 'ls-remote', '--heads', 'origin'], check=True, stdout=subprocess.PIPE, cwd=get_root_directory()).stdout.decode()

            if branch not in local_branches and f'refs/heads/{branch}' not in remote_branches:
                # create new branch
                subprocess.run(['git', 'checkout', '-b', branch], check=True, cwd=get_root_directory())
                # push the newly created branch to remote
                subprocess.run(['git', 'push', '--set-upstream', 'origin', branch], check=True, cwd=get_root_directory())
                response['message'] = f"Branch {branch} created and pushed successfully."
            else:
                response['message'] = f"Branch {branch} already exists."
        except subprocess.CalledProcessError as e:
            response['error'] = f"A Git error occurred: {str(e)}"
        return response
    
# Example usage
if __name__ == "__main__":
    try:
        cghb = CreateGithubBranchFunction('tomgpt')
        res = cghb.execute(branch='test-branch')
        print(res)
    except Exception as e:
        print(f"Caught an exception: {e}")
