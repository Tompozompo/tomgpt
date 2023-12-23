# chatfunction.py

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
        Returns a dictionary representation of the function.
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }
