"""
SaveCurrentThreadFunction retrieves all the messages from the current thread managed by CMDAssistant
and exports them into a JSON file in the saved_conversations folder.
"""

import json
import os
from datetime import datetime
from tomgpt.functions.chatfunction import ChatFunction
from tomgpt.cmd_assistant import CMDAssistant

class SaveCurrentThreadFunction(ChatFunction):

    @property
    def name(self):
        return "save_current_thread"

    @property
    def description(self):
        return "Saves all messages from the current thread to a JSON file."

    @property
    def parameters(self) -> dict:
        return {}

    def execute(self, **kwargs):
        assistant = CMDAssistant.getInstance()
        messages = assistant.client.beta.threads.messages.list(
            order="asc",
            thread_id=assistant.thread_id
        )

        # Extract the messages into a form suitable for JSON serialization
        messages_to_save = [{
            'who': message.role,
            'what': message.content[0].text.value
        } for message in messages]

        # Define the filename with timestamp
        filename = f'saved_thread_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        file_path = os.path.join('saved_conversations', filename)

        # Write the messages to the file
        with open(file_path, 'w') as file:
            json.dump(messages_to_save, file, indent=2)

        return {'message': f'Thread saved to {file_path}'}
