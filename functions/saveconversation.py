import json
import os
from tomgpt.functions.chatfunction import ChatFunction
from typing import Dict

class SaveConversationChatFunction(ChatFunction):
    
    def __init__(self, root) -> None:
        super().__init__()
        self.root = root

    @property
    def name(self) -> str:
        return "save_conversation"
    
    @property
    def description(self) -> str:
        return "Saves the current conversation to a JSON file."
    
    @property
    def parameters(self) -> Dict:
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
                "filename": {
                    "type": "string",
                    "description": "The name of the file to save the conversation to",
                },
            },
            "required": ["conversation", "filename"],
        }

    def execute(self, **kwargs) -> Dict:
        conversation = kwargs.get('conversation')
        filename = kwargs.get('filename')
        try:
            file_path = os.path.join(self.root, 'saved_conversations', filename)
            with open(file_path, 'w') as file:
                json.dump(conversation, file)
            return {"status": "success", "message": f"Conversation saved to {file_path}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
