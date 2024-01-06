# execute_bash_command_chat_function.py
from .chatfunction import ChatFunction
import subprocess
import json

class ExecuteBashCommandChatFunction(ChatFunction):
    @property
    def name(self) -> str:
        return "execute_bash_command"

    @property
    def description(self) -> str:
        return "Executes an arbitrary bash command."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute.",
                }
            },
            "required": ["command"]
        }

    def execute(self, **kwargs) -> dict:
        command = kwargs.get('command')
        try:
            output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return {
                "command": command,
                "stdout": output.stdout,
                "stderr": output.stderr,
                "returncode": output.returncode
            }
        except subprocess.CalledProcessError as e:
            return {
                "command": command,
                "stdout": e.stdout,
                "stderr": e.stderr,
                "returncode": e.returncode,
                "error": "Command execution failed"
            }

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
