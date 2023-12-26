# create_assistant.py
# Fucking around with ChatGPT's Assistant API. 
# Will create a new assistant, then allow interacting via the cmd. 

import os
from openai import OpenAI
import tomgpt

from tomgpt.cmd_assistant import CMDAssistant
from tomgpt.assistant_config_manager import AssistantConfigManager
from tomgpt.functions import getassistantthreads

from tomgpt.functions.chatfunction import ChatFunction
from tomgpt.functions.executepython import ExecutePythonScript
from tomgpt.functions.getassistantthreads import GetAssistantThreadsFunction
from tomgpt.functions.readlocalfile import ReadLocalFileFunction
from tomgpt.functions.readurl import ReadFromURLFunction
from tomgpt.functions.weather import WeatherFunction
from tomgpt.functions.websearch import WebSearchFunction
from tomgpt.functions.writefile import WriteToFileFunction
from tomgpt.functions.exceptionthrowing import ExceptionThrowingChatFunction
from tomgpt.functions.summarizeconversation import SummarizeConversationChatFunction
from tomgpt.functions.creategithubpr import CreateGithubPRFunction
from tomgpt.functions.updatethreadid import UpdateThreadIdChatFunction
from tomgpt.functions.savecurrentthread import SaveCurrentThreadFunction
from tomgpt.functions.change_assistant import ChangeAssistantFunction

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
    """
    returns assistant id of the new assistant
    """
    assistant = client.beta.assistants.create(
        name=name,
        instructions=prompt,
        model=model,
        tools=helper.get_tools_config(
            functions=functions,
            interpreter=interpreter
        ),
        # file_ids=helper.get_files_config(client)  # this has always been shitty when i tried it
        # using ReadLocalFile has been more successful for me
    )
    return assistant.id

def create_thread(
        client: OpenAI,
    ):
    """
    returns thread id of the new thread
    """    
    return (client.beta.threads.create()).id

if __name__=="__main__":

    # used for any functions that do file io shit (WriteToFileFunction, ReadLocalFileFunction)
    # will be the directory the agent assumes it is existing inside, and will be prepended to io things
    # files at the root will also be made available to it
    root_dir = "tomgpt"

    # the folders that I want scaned for files for use in ReadLocalFileFunction
    allowed_folders = [
        "functions",  # eg tomgpt/functions
        "static",
        "templates",
        "output_files",
    ]

    # name and model 
    name = 'TomGPT' 
    model = 'gpt-3.5-turbo'

    # build a prompt, i was surprised how well the worked for file io
    pb = PromptBuilder()
    pb.add(TOMGPT)
    pb.add(TOM)
    pb.add(SAVE_FILE_TIP)
    pb.add(Prompts.filesystem_aware(root_dir, allowed_folders))
    prompt = pb.build()

    # list of functions to use, any of these can be used by the bot
    # there is some limit i forget like 20 or something
    # functions are passed to the assistant at creation time, 
    # so changes require new assistant for now (todo)
    functions = [
        #misc
        WeatherFunction(),
        WebSearchFunction(),
        ExceptionThrowingChatFunction(),
        ChangeAssistantFunction(),

        #io
        ReadFromURLFunction(),
        WriteToFileFunction(root_dir),
        ReadLocalFileFunction(root_dir),
        ExecutePythonScript(),
        
        #thread management
        SummarizeConversationChatFunction(root_dir),
        GetAssistantThreadsFunction(),
        UpdateThreadIdChatFunction(),
        SaveCurrentThreadFunction(),
        CreateGithubPRFunction('tomgpt', 'auto-branch'),
    ]


    # https://platform.openai.com/docs/assistants/tools/code-interpreter
    # i think i have recreated this with WriteToFileFunction + ExecutePythonScript lol 
    # i bet theirs is better but also costs money so no
    interpreter = False 
    
    # create assistant and thread if needed
    print('leave empty to create new')
    print(AssistantConfigManager.get_assistant_threads())
    assistant_id = input("assistant_id: ")
    thread_id = input("thread_id: ")
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if not assistant_id:
        assistant_id = create_assistant(
            client=client,
            name=name,
            prompt=prompt,
            model=model,
            functions=functions,
            interpreter=interpreter
        )
    if not thread_id:
        thread_id = create_thread(client)

    AssistantConfigManager.update_assistant_config(assistant_id, thread_id)
    cmd = CMDAssistant.getInstance(client, assistant_id, thread_id, functions)
    cmd.run()