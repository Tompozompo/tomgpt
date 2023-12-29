import subprocess
from typing import Dict
from functions.chatfunction import ChatFunction
from conversation import Conversation

DEFAULT_MESSAGE_LIMIT = 3

class FriendFunction(ChatFunction):
    def __init__(self, conversation):
        self.parent_conversation = conversation

    @property
    def name(self) -> str:
        return "start_friend_conversation"

    @property
    def description(self) -> str:
        return "Start a new conversation with a friend, whos is another chatbot."

    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "friend_name": {
                    "type": "string",
                    "description": "The name of the friend to start a conversation with",
                },
                "opener": {
                    "type": "string",
                    "description": "The first message to send to the friend to start the conversation",
                },

            },
            "required": ["friend_name, opener"],
        }

    def execute(self, **kwargs) -> Dict:
        friend_name = kwargs.get("friend_name")
        opener = kwargs.get("opener")
        message_limit = kwargs.get("message_limit", DEFAULT_MESSAGE_LIMIT)
        conversation = Conversation(
            system_prompt=f"You are roleplaying as {friend_name}. You are a friend. Try to be a good friend.",
        )
        user_input = opener 
        preamble = f"You are roleplaying as a user, talking to another chatbot. Attached is you original system imformation. Please roleplay in this new one."
        clone = self.parent_conversation.sub(preamble)
        for i in range(message_limit):
            conversation.new_message("user", user_input)
            response = conversation.get_response()
            conversation.new_message("assistant", response)
            clone.new_message("user", response)
            user_input = clone.get_response()
            clone.new_message("assistant", user_input)

        return { "converstation_history": conversation.history }