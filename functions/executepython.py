# chatfunction.py

from typing import Dict
import subprocess
import sys
import json

from tomgpt.functions.chatfunction import ChatFunction

class ExecutePythonScript(ChatFunction):

    @property
    def name(self) -> str:
        return "execute_python_script"

    @property
    def description(self) -> str:
        return "Executes a given Python script and returns its output."

    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "script_path": {
                    "type": "string",
                    "description": "Path to the Python script to be executed.",
                },
            },
            "required": ["script_path"],
        }

    def execute(self, **kwargs) -> Dict:
        script_path = kwargs.get("script_path")
        try:
            result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, check=True)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.CalledProcessError as e:
            return {
                "stdout": e.stdout,
                "stderr": e.stderr,
                "returncode": e.returncode
            }

# Example usage
if __name__ == "__main__":
    executor = ExecutePythonScript()
    script_path = "output_files\helper.py"  # Replace with an actual script path
    result = executor.execute(script_path=script_path)
    print(json.dumps(result, indent=4))
