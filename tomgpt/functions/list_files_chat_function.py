# list_files_chat_function.py
from .chatfunction import ChatFunction
import os

class ListFilesChatFunction(ChatFunction):
    @property
    def name(self) -> str:
        return "list_files"

    @property
    def description(self) -> str:
        return "Lists the files and directories in a given path."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to list files from.",
                }
            },
            "required": ["path"]
        }

    def execute(self, **kwargs) -> dict:
        path = kwargs.get("path", ".")  # default to current directory if not specified
        try:
            file_list = os.listdir(path)
            return {"path": path, "files": file_list}
        except OSError as e:
            return {"error": str(e)}

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

# Example usage
if __name__ == "__main__":
    list_files_function = ListFilesChatFunction()
    files_info = list_files_function.execute(path=".")
    print(files_info)
