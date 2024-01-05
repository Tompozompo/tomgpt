from abc import ABC, abstractmethod

class Interface(ABC):
    @abstractmethod
    def get_input(self) -> str:
        pass
    
    @abstractmethod
    def display(self, messages) -> None:
        """
        messages is a list of OpenAI messages from self.client.beta.threads.messages.lists
        """
        pass