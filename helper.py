from flask import Flask
from threading import Thread
import json
import os

from openai import OpenAI
from tomgpt.functions.chatfunction import ChatFunction

def _get_function_by_name(name, functions):
    for function in functions:
        if function.name == name:
            return function
    return None

def _get_tool_outputs(submit_tool_outputs, functions):
    tool_calls = submit_tool_outputs.tool_calls
    tool_output = [] 
    for tool_call in tool_calls:
        function_to_call = _get_function_by_name(tool_call.function.name, functions)
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

def process_run(run, client, thread_id, functions):
    print('process_run!')
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        print('running...',end='')
        if run.status == "requires_action":
            print('calling function')
            function_outputs = _get_tool_outputs(run.required_action.submit_tool_outputs, functions)
            print('function_outputs {}'.format(function_outputs))
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=function_outputs
            )
        elif run.status == "failed":
            return
        elif run.status == "expired":
            return
        elif run.status == "cancelled":
            return
    print()

def get_files_config(client, files):
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

def get_tools_config(functions: [ChatFunction], interpreter=False):
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


def get_directory_tree(dir_path, allowed_folders=None):
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
            if not allowed_folders or folder in allowed_folders:
                folder_path = os.path.join(root, folder)
                for file in os.listdir(folder_path):
                    file_path = os.path.relpath(os.path.join(folder_path, file), dir_path)
                    directory_tree.append(file_path)

    return directory_tree

def get_directory_tree(root_dir, allowed_folders=None):
    """
    Get the directory tree structure as a list of relative paths,
    including files at root_dir and any files in allowed_folders.
    """
    directory_tree = []
    
    for root, dirs, files in os.walk(root_dir, topdown=True): 
        relative_root = os.path.relpath(root, root_dir)
        if relative_root == '.' or relative_root in allowed_folders:
            for file in files:
                file_path = os.path.join(relative_root, file)
                directory_tree.append(file_path)

    return directory_tree        

def start_flask_app():
    global app
    app = Flask(__name__)
    Thread(target=lambda: app.run(use_reloader=False)).start()

def get_root_directory():
    return os.path.dirname(os.path.abspath(__file__))









if __name__ == "__main__":
    string_to_pass = "Hello, Flask!"
    start_flask_app(string_to_pass)
