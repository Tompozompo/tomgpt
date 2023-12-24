# ExceptionThrowingChatFunction.py
# A mock implementation of ChatFunction that simply throws an exception.

from tomgpt.functions.chatfunction import ChatFunction

class ExceptionThrowingChatFunction(ChatFunction):

    @property
    def name(self) -> str:
        return 'exception_throwing_chat_function'

    @property
    def description(self) -> str:
        return 'A mock implementation that throws an error for testing purposes.'

    @property
    def parameters(self) -> dict:
        return {}

    def execute(self, **kwargs) -> dict:
        raise Exception('This function is designed to throw an exception.')
