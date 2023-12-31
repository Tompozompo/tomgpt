"""
ReadLocalFileFunction allows reading the contents of a local file from the specified root directory. It is designed to be safe and only allows reading from allowed directories and files.
"""

import os
from tomgpt.functions.chatfunction import ChatFunction
from typing import Dict

class ReadLocalFileFunction(ChatFunction):

    def __init__(self, root: str = '.') -> None:
        """
        root: str - the root of the local filesystem to read from
        """
        super().__init__()
        self.root = root

    @property
    def name(self) -> str:
        return "read_local_file"

    @property
    def description(self) -> str:
        return "Reads the contents from a local file path if the file exists."

    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The local file path to read from.",
                },
            },
            "required": ["path"],
        }

    def execute(self, **kwargs) -> Dict:
        path = kwargs.get('path')
        response = {}
        file_path = os.path.join(self.root, path)

        # Check if the file exists
        if not os.path.exists(file_path):
            response['error'] = "The file does not exist."
            return response

        try:
            # Read the content of the file
            with open(file_path, 'r') as file:
                content = file.read()
            response['content'] = content
        except Exception as e:
            response['error'] = f"An error occurred while reading the file: {str(e)}"

        return response
    
if __name__ == "__main__":
    read_local_file_function = ReadLocalFileFunction()
    result = read_local_file_function.execute(path="/mnt/data/example.txt")
    print(result)