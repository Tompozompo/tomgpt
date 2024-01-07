# execute_bash_command_chat_function.py
from .chatfunction import ChatFunction
import subprocess
import json

class ExecuteSubprocessChatFunction(ChatFunction):
    @property
    def name(self) -> str:
        return "execute_subprocess"

    @property
    def description(self) -> str:
        return "Executes an arbitrary command to the underlying os with subprocess.run"

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to execute.",
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

# Example usage
if __name__ == "__main__":
    bash_executor = ExecuteSubprocessChatFunction()
    command = "echo 'Hello, world!'"
    result = bash_executor.execute(command=command)
    print(json.dumps(result, indent=4))