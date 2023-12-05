# chatfunction.py

from abc import ABC, abstractmethod
from typing import Dict

class ChatFunction(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """
        name_in_snake_case
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        A short description of the function
        """
        pass


    @property 
    @abstractmethod
    def parameters(self) -> Dict:
        """
        A JSON schema describing the parameters of the function. Example: 
        {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
            "format": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "The temperature unit to use. Infer this from the users location.",
            },
        },
        "required": ["location", "format"],
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
        Returns a dictionary representation of the function.
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }