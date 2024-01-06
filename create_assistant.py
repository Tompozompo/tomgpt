# create_assistant.py
# Fucking around with ChatGPT's Assistant API. 
# Will create a new assistant, then allow interacting via the cmd. 

import os
from openai import OpenAI
from tomgpt.interfaces.cmd_assistant import CMDInterface
from tomgpt.interfaces.voice_assistant import VoiceInterface
from tomgpt.assistant_config_manager import AssistantConfigManager

from tomgpt.functions.getassistantthreads import GetAssistantThreadsFunction
from tomgpt.functions.readlocalfile import ReadLocalFileFunction
from tomgpt.functions.weather import WeatherFunction
from tomgpt.functions.websearch import WebSearchFunction
from tomgpt.functions.writefile import WriteToFileFunction
from tomgpt.functions.updatethreadid import UpdateThreadIdChatFunction
from tomgpt.functions.savecurrentthread import SaveCurrentThreadFunction
from tomgpt.functions.list_files_chat_function import ListFilesChatFunction
from tomgpt.functions.creategithubbranch import CreateGithubBranchFunction
from tomgpt.functions.commitandcreatepr import CommitAndCreatePRFunction
from tomgpt.functions.mergegithubpr import MergeGithubPRFunction
from tomgpt.functions.execute_subprocess_chat_function import ExecuteSubprocessChatFunction

from tomgpt.prompts import *
from tomgpt.helper import *
from tomgpt.brains.openai_singleton import SingletonAssistant

# name and model 
name = 'TomGPT' 
model = 'gpt-4'

# build a prompt, i was surprised how well the worked for file io
pb = PromptBuilder()
pb.add(TOMGPT)
pb.add(TOM)
pb.add(SAVE_FILE_TIP)
prompt = pb.build()

# list of functions to use, any of these can be used by the bot
# there is some limit i forget like 20 or something
# functions are passed to the assistant at creation time, 
# so changes require new assistant for now (todo)
functions = [
    #misc
    WeatherFunction(),
    WebSearchFunction(),
    ExecuteSubprocessChatFunction(),

    #git
    CreateGithubBranchFunction('tomgpt'),
    CommitAndCreatePRFunction('tomgpt'),
    MergeGithubPRFunction('tomgpt'),

    #io
    ListFilesChatFunction(),
    WriteToFileFunction('output_files'),
    ReadLocalFileFunction(),
    # ExecutePythonCode(),

    #thread management
    SaveCurrentThreadFunction('saved_conversations'),
]


# https://platform.openai.com/docs/assistants/tools/code-interpreter
# i think i have recreated this with WriteToFileFunction + ExecutePythonScript lol 
# i bet theirs is better but also costs money so no
interpreter = False 

# create assistant and thread if needed
print('leave empty to create new')
print(AssistantConfigManager.get_assistant_threads())
assistant_id = '' or input("assistant_id: ")
thread_id = '' or input("thread_id: ")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
if not assistant_id:
    assistant_id = SingletonAssistant.create_assistant(
        client=client,
        name=name,
        prompt=prompt,
        model=model,
        functions=functions,
        interpreter=interpreter
    )
if not thread_id:
    thread_id = SingletonAssistant.create_thread(client)

AssistantConfigManager.update_assistant_config(assistant_id, thread_id)
ass = SingletonAssistant.getInstance(client, assistant_id, thread_id, functions)
ass.run(CMDInterface())

