# chatfunction.py
"""
An abstract openai function. 
Doc at https://platform.openai.com/docs/guides/function-calling, summarized as 
Function calling allows you to more reliably get structured data back from the model. For example, you can:
  Create assistants that answer questions by calling external APIs (e.g. like ChatGPT Plugins)
    e.g. define functions like send_email(to: string, body: string), or get_current_weather(location: string)
  Convert natural language into API calls
    e.g. convert "Who are my top customers?" to get_customers(min_revenue: int, created_before: string, limit: int) and call your internal API
  Extract structured data from text
    e.g. define a function called extract_data(name: string, birthday: string), or sql_query(query: string)

Some conventions when implementing new children classes: 
  - file named 'examplethatdoesthing.py' 
  - class named 'ExampleThatDoesThingChatFunction' 
  - property name named 'example_that_does_thing'
  - include a comment at the top with a brief summary (like this one!) 
  - import this base file like like 'from tomgpt.functions.chatfunction import ChatFunction'
"""

from abc import ABC, abstractmethod, abstractproperty
from typing import Dict

class ChatFunction(ABC):

    @abstractproperty
    def name(self) -> str:
        """
        name_in_snake_case
        """
        pass

    @abstractproperty
    def description(self) -> str:
        """
        A short description of the function
        """
        pass

    @abstractproperty
    def parameters(self) -> Dict:
        """
        A JSON schema describing the parameters of the function. Example: 
        {
            "type": "object",
            "properties": {
                "test_property": {
                    "type": "string",
                    "description": "An example of a property",
                },
                "test_number": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Wow could even have enums?",
                },
            },
            "required": ["test_property", "test_number"],
        }
        """
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict:
        """
        Execute the function and return a JSON response.
        The parameters are passed in the form of kwargs
        """
        pass

    def to_dict(self) -> Dict:
        """
        Returns a dictionary representation of the class.
        This is what OpenAI expects.
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }
