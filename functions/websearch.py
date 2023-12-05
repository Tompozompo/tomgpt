from .chatfunction import ChatFunction
from typing import  Dict
import requests
import os

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
BRAVE_API_URL = "https://api.search.brave.com/res/v1/web/search"

class WebSearchFunction(ChatFunction):
    # https://api.search.brave.com
    @property
    def name(self) -> str:
        return "websearch"

    @property
    def description(self) -> str:
        return "Executes a web search for the given query \
                and returns a list of snippets of matching text from \
                top 10 pages"

    @property
    def parameters(self) -> Dict:
        return {
                "type": "object",
                "properties": {
                    "q": {
                        "type": "string",
                        "description": "the user query"
                    }
                }
            }


    def execute(self, **kwargs) -> Dict:
        """
        Execute the plugin and return a JSON response.
        The parameters are passed in the form of kwargs
        """

        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": BRAVE_API_KEY
        }

        params = {
            "q": kwargs["q"]
        }

        response = requests.get(BRAVE_API_URL,
                                headers=headers,
                                params=params)

        if response.status_code == 200:
            results = response.json()['web']['results']
            snippets = [r['description'] for r in results]
            return {"web_search_results": snippets}
        else:
            return {"error":
                    f"Request failed with status code: {response.status_code}"}