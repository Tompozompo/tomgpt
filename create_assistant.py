# create_assistant.py
# Fucking around with ChatGPT's Assistant API. 
# Will create a new assistant, then allow interacting via the cmd. 

import os
from openai import OpenAI
from tomgpt.cmd_assistant import CMDAssistant
from tomgpt.functions.chatfunction import ChatFunction
from tomgpt.functions.executepython import ExecutePythonScript
from tomgpt.functions.readlocalfile import ReadLocalFileFunction
from tomgpt.functions.readurl import ReadFromURLFunction
from tomgpt.functions.weather import WeatherFunction
from tomgpt.functions.websearch import WebSearchFunction
from tomgpt.functions.writefile import WriteToFileFunction
from tomgpt.functions.exceptionthrowing import ExceptionThrowingChatFunction
from tomgpt.functions.saveconversation import SaveConversationChatFunction
from tomgpt.prompts import *
from tomgpt.helper import *


def create_assistant(
        client: OpenAI,
        name: str, 
        prompt: str, 
        model: str, 
        functions: [ChatFunction], 
        interpreter: bool = False
    ):
    assistant = client.beta.assistants.create(
        name=name,
        instructions=prompt,
        model=model,
        tools=helper.get_tools_config(
            functions=functions,
            interpreter=interpreter
        ),
        # file_ids=helper.get_files_config(client)  # this has always been shitty when i tried it
    )
    return assistant.id

if __name__=="__main__":
    root_dir = "tomgpt"
    allowed_folders = [
        "functions",
        "static",
        "templates",
        "output_files",
    ]

    name = 'TomGPT' # "With Functions" "Self-Code Aware"
    model = 'gpt-4-1106-preview'
    assistant_id = input('assistant_id: ')
    thread_id = input('thread_id: ')
    # if empty a new one will be made

    pb = PromptBuilder()
    pb.add(TOMGPT)
    pb.add(TOM)
    pb.add(SAVE_FILE_TIP)
    pb.add(Prompts.filesystem_aware(root_dir, allowed_folders))

    functions = [
        WeatherFunction(),
        WebSearchFunction(),
        ReadFromURLFunction(),
        WriteToFileFunction(root_dir),
        ReadLocalFileFunction(root_dir),
        ExecutePythonScript(),
        ExceptionThrowingChatFunction(),
        SaveConversationChatFunction(root_dir),
    ]
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if not assistant_id:
        assistant_id = create_assistant(
            client=client,
            name=name,
            prompt=pb.build(),
            model=model,
            functions=functions,
            interpreter=False
        )
    if not thread_id:
        thread_id = (client.beta.threads.create()).id

    cmd = CMDAssistant.getInstance(assistant_id, thread_id, functions, client)
    cmd.run()