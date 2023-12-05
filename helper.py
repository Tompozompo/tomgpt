from functions.weather import WeatherFunction
from functions.websearch import WebSearchFunction
from functions.writefile import WriteToFileFunction
from functions.readlocalfile import ReadLocalFileFunction
from functions.readurl import ReadFromURLFunction
from functions.savetogithub import SaveToGithubFunction

from flask import Flask
from threading import Thread
from flaskapp import app
import json
import os

functions = [
    WeatherFunction(),
    WebSearchFunction(),
    WriteToFileFunction(),
    ReadFromURLFunction(),
    ReadLocalFileFunction()
]

allowed_folders = [
    "functions",
    "static",
    "templates",
    "output_files",
]

files = [ #old and not used at this point 6:31 PM December 4, 2023
    "create_assistant.py",
    "flaskapp.py",
    "helper.py",
    "templates/chat.html",
    "static/chat.css",
    "functions/chatfunction.py",
    "functions/weather.py",
    "functions/websearch.py",
    "functions/change_assistant.py"
]

def _get_function_by_name(name):
    for function in functions:
        if function.name == name:
            return function
    return None

def get_tool_outputs(submit_tool_outputs):
    tool_calls = submit_tool_outputs.tool_calls
    tool_output = [] 
    for tool_call in tool_calls:
        function_to_call = _get_function_by_name(tool_call.function.name)
        print("calling function {}".format(function_to_call))
        if not function_to_call:
            return "Function not found"
        function_args = json.loads(tool_call.function.arguments)
        print("function args {}".format(function_args))
        if not function_args:
            return "No arguments provided"
        function_response = function_to_call.execute(**function_args)
        print("function response {}".format(function_response))
        tool_output.append({
            "tool_call_id": tool_call.id,
            "output": str(function_response)
        })
    return tool_output

def process_run(run,client,thread):
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print('running...',end='')
        if run.status == "requires_action":
            print('calling function')
            function_outputs = get_tool_outputs(run.required_action.submit_tool_outputs)
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=function_outputs
            )
        elif run.status == "failed":
            return
        elif run.status == "expired":
            return
        elif run.status == "cancelled":
            return

def get_files_config(client):
    files_config = []
    for file in files:
        files_config.append(client.files.create(
            file=open(file, "rb"),
            purpose='assistants'
        ).id)
    return files_config

def get_tools_config(interpreter=True):
    tools_config = []
    if interpreter:
        tools_config = [{"type": "code_interpreter"}]
    for func in functions:
        tools_config.append({
            "type": "function",
            "function": func.to_dict(),
        })
    return tools_config


def get_directory_tree(dir_path):
    """
    Get the directory tree structure as a list of relative paths
    including files at the root and files from allowed folders.
    """
    directory_tree = []
    root_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    directory_tree.extend(root_files)

    for root, dirs, files in os.walk(dir_path): 
        if 'venv' in dirs:
            dirs.remove('venv')
        for folder in dirs:
            if folder in allowed_folders:
                folder_path = os.path.join(root, folder)
                for file in os.listdir(folder_path):
                    file_path = os.path.relpath(os.path.join(folder_path, file), dir_path)
                    directory_tree.append(file_path)

    return directory_tree

def start_flask_app():
    global app
    app = Flask(__name__)
    Thread(target=lambda: app.run(use_reloader=False)).start()

if __name__ == "__main__":
    string_to_pass = "Hello, Flask!"
    start_flask_app(string_to_pass)
