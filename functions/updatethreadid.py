"""
This chat function updates the thread ID in the CMDAssistant singleton instance.
It provides an interface to change the thread ID for the running assistant programmatically.
"""

from tomgpt.cmd_assistant import CMDAssistant
from tomgpt.functions.chatfunction import ChatFunction

class UpdateThreadIdChatFunction(ChatFunction):

    @property
    def name(self):
        return "update_thread_id"

    @property
    def description(self):
        return "Updates the thread ID of the CMDAssistant singleton."

    @property
    def parameters(self):
        return {
            "type": "object",
            "properties": {
                "new_thread_id": {
                    "type": "string",
                    "description": "The new thread ID to set",
                },
            },
            "required": ["new_thread_id"],
        }
    
    def execute(self, new_thread_id):
        cmd_assistant = CMDAssistant.getInstance()
        cmd_assistant.thread_id = new_thread_id
        return {"result": "Thread ID updated to {}".format(new_thread_id)}
