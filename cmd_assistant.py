import os
from openai import OpenAI
from tomgpt import helper

class CMDAssistant():
    def __init__(self, assistant_id, functions, client) -> None:
        self.assistant_id = assistant_id
        self.functions = functions
        self.client = client

    def run(self):
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        print("ASSISTANT_ID: " + self.assistant_id)
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        # Start a CMD based Thread
        thread = self.client.beta.threads.create()
        # helper.start_flask_app()
        while True:
            print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
            user_input = input('New Input: ')
            print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")

            message = self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_input
            )
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant_id,
            )
            helper.process_run(run, self.client, thread, self.functions)

            messages = self.client.beta.threads.messages.list(
                order="asc",
                thread_id=thread.id
            )
            for message in messages:
                print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
                print("{}: {}".format(message.role, message.content[0].text.value))
                print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
