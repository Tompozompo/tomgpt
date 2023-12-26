"""
ReadFromURLFunction is used to fetch and return the contents from a given URL. It encapsulates the logic needed to make HTTP GET requests and handle potential errors.
"""

import requests
from tomgpt.functions.chatfunction import ChatFunction
from typing import Dict

class ReadFromURLFunction(ChatFunction):

    @property
    def name(self) -> str:
        return "read_from_url"

    @property
    def description(self) -> str:
        return "Reads the contents from a specified URL."

    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "format": "uri",
                    "description": "The URL to fetch the content from.",
                }
            },
            "required": ["url"],
        }

    def execute(self, **kwargs) -> Dict:
        url = kwargs.get('url')
        response = {}

        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            response['content'] = r.text
        except Exception as e:
            response['error'] = str(e)

        return response
    
if __name__ == "__main__":
    read_from_url_function = ReadFromURLFunction()
    result = read_from_url_function.execute(url="http://127.0.0.1:5000/character/Mokuba%20Kaiba")
    print(result)
