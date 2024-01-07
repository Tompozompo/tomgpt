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

# Example usage
if __name__ == "__main__":
    try:
        exception_throwing_function = ExceptionThrowingChatFunction()
        exception_throwing_function.execute()
    except Exception as e:
        print(f"Caught an exception as expected: {e}")
