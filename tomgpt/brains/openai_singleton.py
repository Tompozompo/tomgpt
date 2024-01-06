import json
from openai import OpenAI
from tomgpt.functions.chatfunction import ChatFunction
from tomgpt.interfaces.interface import Interface


class SingletonAssistant():
    _instance = None  # Singleton instance variables

    @classmethod
    def getInstance(cls, client=None, assistant_id=None, thread_id=None, functions=None):
        if not cls._instance:
            cls._instance = cls.__new__(cls)
        if client and assistant_id and thread_id and functions:
            cls._instance.initialize(client, assistant_id, thread_id, functions)
        return cls._instance

    @classmethod
    def create_assistant(
            cls,
            client: OpenAI,
            name: str, 
            prompt: str, 
            model: str, 
            functions: [ChatFunction], 
            interpreter: bool = False
        ):
        """
        returns assistant id of the new assistant
        """
        assistant = client.beta.assistants.create(
            name=name,
            instructions=prompt,
            model=model,
            tools=cls._get_tools_config(cls,
                functions=functions,
                interpreter=interpreter
            ),
            # file_ids=cls._get_files_config(client)  # this has always been shitty when i tried it
            # using ReadLocalFile has been more successful for me
        )
        return assistant.id
    
    @classmethod
    def create_thread(
            cls,
            client: OpenAI,
        ):
        """
        returns thread id of the new thread
        """    
        return (client.beta.threads.create()).id


    def __new__(cls):
        if not cls._instance:
            cls._instance = super(SingletonAssistant, cls).__new__(cls)
        return cls._instance

    def initialize(self, client, assistant_id, thread_id, functions):
        if '_is_initialized' not in self.__dict__:
            self.client = client
            self.assistant_id = assistant_id
            self.thread_id = thread_id
            self.functions = functions
            self._is_initialized = True
            # helper.start_flask_app() # i was using this for downloading from url tests
    
    def run(self, interface: Interface):
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        print("assistant_id: " + self.assistant_id)
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        print("thread_id: " + self.thread_id)
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        while True:
            # display messages
            messages = self.client.beta.threads.messages.list(
                order="asc",
                thread_id=self.thread_id
            )
            try:
                if messages: 
                    interface.display(messages) 
            except Exception as e:
                print(f'Exception during interface.display: {e}')

            # get input
            try:
                user_input = interface.get_input()
            except Exception as e:
                print(f'Exception during interface.get_input: {e}')
                continue

            # process run
            self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role="user",
                content=user_input
            )
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id,
            )
            self._process_run(run)
            

    def _get_function_by_name(self, name):
        """
        Gets function by name    
        """
        for function in self.functions:
            if function.name == name:
                return function
        return None

    def _get_tool_outputs(self, submit_tool_outputs):
        """
        https://platform.openai.com/docs/guides/function-calling/parallel-function-calling
        Calls all the functions and returns their values
        """
        tool_calls = submit_tool_outputs.tool_calls
        tool_output = [] 
        for tool_call in tool_calls:
            function_to_call = self._get_function_by_name(tool_call.function.name)
            if not function_to_call:
                tool_output.append({'error': f'Function {function_to_call.name} not found'})
                continue
            print(f"calling function {function_to_call.name}")
            try:
                function_args = json.loads(tool_call.function.arguments)
                print(f"function_args {function_args}")
                function_response = function_to_call.execute(**function_args)
            except Exception as e:
                function_response = {f'Exception during execute: {e}'}    
            print(f"function response {function_response}")
            tool_output.append({
                "tool_call_id": tool_call.id,
                "output": str(function_response)
            })   
        return tool_output

    def _process_run(self, run):
        """
        Process the Open AI run, which gets the next message or calls some available functions.
        self.client.beta.threads.messages will contain the new message when finished. 
        If the function you pass here is different than the ones passed to the assistant initially,
        you might still be able to talk it into using it haha
        """
        print('process_run!')
        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run.id
            )
            print('running...',end='')
            if run.status == "requires_action":
                print('calling function')
                function_outputs = self._get_tool_outputs(run.required_action.submit_tool_outputs)
                print('function_outputs {}'.format(function_outputs))
                run = self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.thread_id,
                    run_id=run.id,
                    tool_outputs=function_outputs
                )
            elif run.status == "failed":
                print('failed!')
                print(run)
                return
            elif run.status == "expired":
                print('expired!')
                print(run)
                return
            elif run.status == "cancelled":
                print('cancelled!')
                print(run)
                return
        print()

    def _get_files_config(
            cls,
            client,
            files
        ):
        """
        Add files directly to OpenAI client using files.create
        This never worked quite right. 
        """
        files_config = []
        for file in files:
            files_config.append(client.files.create(
                file=open(file, "rb"),
                purpose='assistants'
            ).id)
        return files_config

    def _get_tools_config(
            cls,
            functions=[ChatFunction],
            interpreter=False
        ):
        """
        Get the OpenAI client tools config, from a list of ChatFunctions.
        Also can enablue interpreter, which lets it run code. It was also shitty I just want it to make code not run it. 
        """
        tools_config = []
        if interpreter:
            tools_config = [{"type": "code_interpreter"}]
        for func in functions:
            tools_config.append({
                "type": "function",
                "function": func.to_dict(),
            })
        return tools_config
