from functions.chatfunction import ChatFunction
from typing import Dict
import subprocess
import os

class SaveToGithubFunction(ChatFunction):

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
                    "description": "The commit message.",
                },
                "github_token": {
                    "type": "string",
                    "description": "GitHub token for authentication.",
                },
                "repository": {
                    "type": "string",
                    "description": "The GitHub repository to push to.",
                },
                "branch": {
                    "type": "string",
                    "description": "The branch to push to.",
                },
            },
            "required": ["message", "github_token", "repository", "branch"],
        }

    def execute(self, **kwargs) -> Dict:
        message = kwargs.get('message')
        github_token = kwargs.get('github_token')
        repository = kwargs.get('repository')
        branch = kwargs.get('branch')
        response = {}

        try:
            # Configure Git user (This should be set to the user's Git config)
            subprocess.run(['git', 'config', '--global', 'user.email', 'you@example.com'], check=True)
            subprocess.run(['git', 'config', '--global', 'user.name', 'Your Name'], check=True)

            # Add all changed files
            subprocess.run(['git', 'add', '.'], check=True)

            # Commit the changes
            subprocess.run(['git', 'commit', '-m', message], check=True)

            # Add the remote repository with the token for authentication
            subprocess.run(['git', 'remote', 'add', 'origin', f'https://x-access-token:{github_token}@github.com/{repository}.git'], check=True)

            # Pull the latest changes from the remote branch
            subprocess.run(['git', 'pull', 'origin', branch], check=True)

            # Push the commit to GitHub
            subprocess.run(['git', 'push', 'origin', branch], check=True)

            response['message'] = "Changes have been successfully committed and pushed to GitHub."
        except subprocess.CalledProcessError as e:
            response['error'] = f"A Git error occurred: {e.output}"

        return response
    
if __name__ == "__main__":
    save_to_github_function = SaveToGithubFunction()
    result = save_to_github_function.execute(
        message="Updated the project",
        github_token="your_github_token",
        repository="username/repo",
        branch="main"
    )
    print(result)