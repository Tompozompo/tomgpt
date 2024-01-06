import subprocess
import sys
import json
import os
import tempfile
from tomgpt.functions.chatfunction import ChatFunction

class ExecutePythonCode(ChatFunction):

    @property
    def name(self) -> str:
        return "execute_python_code"

    @property
    def description(self) -> str:
        return "Executes the provided Python code and returns its output."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "python_code": {
                    "type": "string",
                    "description": "The Python code to be executed.",
                },
            },
            "required": ["python_code"],
        }

    def execute(self, **kwargs) -> dict:
        python_code = kwargs.get("python_code")
        try:
            # Create a temporary file to write the Python code to
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp_file:
                tmp_file_path = tmp_file.name
                tmp_file.write(python_code.encode("utf-8"))

            result = subprocess.run(
                [sys.executable, tmp_file_path],
                capture_output=True, text=True, check=True
            )

            # Remove the temporary file
            os.remove(tmp_file_path)

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.CalledProcessError as e:
            # Remove the temporary file in case of a process error
            os.remove(tmp_file_path)

            return {
                "stdout": e.stdout,
                "stderr": e.stderr,
                "returncode": e.returncode
            }

# Example usage
if __name__ == "__main__":
    executor = ExecutePythonCode()
    python_code = "print('Hello, world!')"
    result = executor.execute(python_code=python_code)
    print(json.dumps(result, indent=4))
