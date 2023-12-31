# this was my first attempt, uses a older OpenAI API. 
# no concept of assistants or threads, just raw chat completions
# might not work right, I forget how far along this was. 

import openai
import json

DEFAULT_SYSTEM_PROMPT = """You are TomGPT, my personal chatbot I'm working on. 
Love you, Tom.
Some other tips:
You have some functions, use them if you want.
NEVER make up an answer if you don't know, say so."""
DEFAULT_MODEL = "gpt-3.5-turbo"

class Conversation:
    def __init__(self, system_prompt=DEFAULT_SYSTEM_PROMPT, model=DEFAULT_MODEL, history=[], functions=[]):
        self.system_prompt = system_prompt
        self.history = []
        self.new_message("system", system_prompt)
        self.model = model
        self.functions = functions
        if history:
            self.history = history

    def _function_call(self, response_message):
        # get the function name and arguments from the response message
        function_name = response_message["function_call"]["name"]
        function_to_call = self._get_function_by_name(function_name)
        if not function_to_call:
            return "Function not found"

        function_args = json.loads(response_message["function_call"]["arguments"])
        if not function_args:
            return "No arguments provided"

        # call the function
        function_response = function_to_call.execute(**function_args)

        # create a temporary conversation to get the response to the function        
        temp_conversation = self._clone()
        temp_conversation.add_message(response_message)
        temp_conversation.new_message("function", json.dumps(function_response), function_name)
        second_response = temp_conversation.get_response()
        return second_response

    def _get_function_by_name(self, name):
        for function in self.functions:
            if function.name == name:
                return function
        return None
    
    def _clone(self):
        return Conversation(
            system_prompt=self.system_prompt,
            model=self.model,
            history=self.history.copy(),
            functions=self.functions.copy()
        )
    
    def sub(self, context):
        system_prompt = f"{context}\n{self.history}"
        return Conversation(
            system_prompt=system_prompt,
            model=self.model,
        )
    
    def new_message(self, role, content, name=None):
        """
        Adds a new message to the chat log.

        Args:
            role (str): The role of the message sender.
            content (str): The content of the message.
            name (str, optional): The name of the message sender. Defaults to None.
        """
        message = {"role": role, "content": content}
        if name is not None:
            message["name"] = name
        self.add_message(message)

    def add_message(self, message):
        """
        Add a message to the conversation history
        """
        self.history.append(message)

    def get_response(self):
        """
        Generates a response from the OpenAI chatbot model based on the conversation history and any defined functions.

        Returns:
            str: The response message generated by the OpenAI chatbot model.
        """
        if self.functions is None or len(self.functions) == 0:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.history,
                temperature=0.6,
                n=1
            )
        else:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.history,
                temperature=0.6,
                n=1,
                functions=[f.to_dict() for f in self.functions],
                function_call="auto",
            )
        response_message = response['choices'][0]['message']

        if response_message.get("function_call"):
            return self._function_call(response_message)
        else:
            return response_message['content']

