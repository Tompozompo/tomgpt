import os
from openai import OpenAI
from tomgpt import helper

class CMDAssistant():
    _instance = None  # Singleton instance variable

    @classmethod
    def getInstance(cls, assistant_id=None, thread_id=None, functions=None, client=None):
        if not cls._instance:
            cls._instance = cls.__new__(cls)
        if assistant_id and thread_id and functions and client:
            cls._instance.initialize(assistant_id, thread_id, functions, client)
        return cls._instance

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(CMDAssistant, cls).__new__(cls)
        return cls._instance

    def initialize(self, assistant_id, thread_id, functions, client):
        if '_is_initialized' not in self.__dict__:
            self.assistant_id = assistant_id
            self.thread_id = thread_id
            self.functions = functions
            self.client = client
            self._is_initialized = True
            # helper.start_flask_app() # i was using this for downloading from url tests

    def end_conversation(self, final_message: str):
        thread_id = self.get_thread_id()  # Extract the thread_id from the instance
        final_message_with_id = f"{final_message} (Thread ID: {thread_id})"
        # Send final message - the actual method of sending this would be implemented as needed
        self.send_message(final_message_with_id)

    def get_thread_id(self):
        # Extract the thread_id attribute from the instance
        return getattr(self, 'thread_id', 'unknown')

    def run(self):
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        print("ASSISTANT_ID: " + self.assistant_id)
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        print("self.thread.id: " + self.thread_id)
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        while True:
            print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
            user_input = input('New Input: ')
            print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")

            message = self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role="user",
                content=user_input
            )
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id,
            )
            helper.process_run(run, self.client, self.thread_id, self.functions)

            messages = self.client.beta.threads.messages.list(
                order="asc",
                thread_id=self.thread_id
            )
            for message in messages:
                print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
                print("{}: {}".format(message.role, message.content[0].text.value))
                print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
