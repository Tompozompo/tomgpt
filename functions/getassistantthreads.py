from tomgpt.functions.chatfunction import ChatFunction
from tomgpt.assistant_config_manager import AssistantConfigManager

class GetAssistantThreadsFunction(ChatFunction):

    @property
    def name(self):
        return "get_assistant_threads"

    @property
    def description(self):
        return "Retrieves a list of available assistant and thread ID pairs from the configuration file."

    @property
    def parameters(self):
        return {}

    def execute(self, **kwargs):
        return {'assistants': AssistantConfigManager.get_assistant_threads()}