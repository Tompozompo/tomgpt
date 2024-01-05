import json
import os
from datetime import datetime
from tomgpt.functions.chatfunction import ChatFunction

class SummarizeConversationChatFunction(ChatFunction):

    def __init__(self, output_dir):
        # Create the directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.output_dir = output_dir

    @property
    def name(self):
        return "summarize_conversation"

    @property
    def description(self):
        return "Save a summary of the current coverstation to a file."

    @property
    def parameters(self):
        return {
            "type": "object",
            "properties": {
                "conversation": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "who": {
                                "type": "string",
                                "description": "Identifier of who sent the message",
                            },
                            "what": {
                                "type": "string",
                                "description": "The content of the message",
                            }
                        },
                        "required": ["who", "what"],
                    },
                    "description": "The conversation to be saved",
                },
            },
            "required": ["conversation"],
        }

    def execute(self, **kwargs):
        conversation = kwargs.get('conversation')

        # Generate a timestamped filename
        filename = f'summarized_thread_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        file_path = os.path.join(self.output_dir, filename)

        with open(file_path, 'w') as file:
            json.dump(conversation, file, indent=2)

        return {'status': 'success', 'message': f"Conversation summarized to {file_path}"}
