"""
WriteToFileFunction allows writing content to a specified file within the system. It includes safeguards to prevent unauthorized filesystem access.
"""

import os
from tomgpt.functions.chatfunction import ChatFunction
from typing import Dict

class WriteToFileFunction(ChatFunction):

    def __init__(self, root) -> None:
        super().__init__()
        self.root = root

    @property
    def name(self) -> str:
        return "write_to_file"

    @property
    def description(self) -> str:
        return "Writes the provided content to a file on the system."

    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the file to write to. Does not accept paths; names only",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write into the file.",
                },
            },
            "required": ["filename", "content"],
        }

    def execute(self, **kwargs) -> Dict:
        filename = kwargs.get('filename')
        content = kwargs.get('content')
        response = {}

        # Sanitize the filename to avoid directory traversal or overwriting important files
        if '..' in filename or '/' in filename:
            response['error'] = f'Invalid filename {filename}. Cannot contain ".." or "/".'
            return response

        try:
            file_path = os.path.join(self.root, 'output_files', filename)

            # Write the content to the file
            with open(file_path, 'w') as file:
                file.write(content)

            response['message'] = f"Content successfully written to {file_path}."
            response['file_path'] = file_path
        except Exception as e:
            response['error'] = str(e)

        return response
    

if __name__ == "__main__":
    write_function = WriteToFileFunction()
    
    test_filename = "test_file.txt"
    test_content = "Hello, this is a test content!"
    result = write_function.execute(filename=test_filename, content=test_content)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Success: {result['message']}")
        print(f"File Path: {result['file_path']}")
