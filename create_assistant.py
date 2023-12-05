# create_assistant.py
# Fucking around with ChatGPT's Assistant API. 
# Will create a new assistant, then allow interacting via the cmd. 


from openai import OpenAI
import os
import helper

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
current_directory = os.getcwd()
dir_tree = helper.get_directory_tree(current_directory)

SELF_AWARE_PROMPT = """
You are TomGPT, my personal chatbot I'm working on. 

I am Tom. 
I am interacting with you via the openai python api, and 
I uploaded all the relevant files, heres a brief description of each. 
create_assistant.py - script that creates assistants and cmd interfact to chat
flaskapp.py - simple flask web app for interacting with assistants
helper.py - contains helper functions used in managing assistants
static/chat.css - css for flask app
templates/chat.html - html template for flask app
functions/chatfunction.py - a template that can be used to implement new functions accessable to you
functions/weather.py - allows you to find the weather
functions/websearch.py - allows you to websearch
functions/change_assistant - create a new assistant and switch to it in the flaskapp

My goal is for you to write more code to improve youself, and return it back to me so that I can update you.
DONOT try to run the code you write yourself. 

Love you, Tom. 
"""
SYSTEM_PROMPT ="""
You are TomGPT, my personal chatbot I'm working on. 

I am Tom. 
I gave you a few functions. Use them if you need.
The local directory you can run functions in is: {}
""".format(dir_tree)

NAME = "TomGPT" # "With Functions" "Self-Code Aware"
MODEL = "gpt-4-1106-preview"

# Create the assistant
assistant = client.beta.assistants.create(
    name=NAME,
    instructions=SYSTEM_PROMPT,
    model="gpt-4-1106-preview",
    tools=helper.get_tools_config(False),
    # file_ids=helper.get_files_config(client)
)
print("+-+-+-+-+-+-+-+-+-+-+-")
ASSISTANT_ID = assistant.id
print("assistant.id: " + assistant.id)
print("+-+-+-+-+-+-+-+-+-+-+-")

# Start a CMD based Thread
thread = client.beta.threads.create()
helper.start_flask_app()
while True:
    user_input = input('New Input: ')
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )
    with open('functions/chatfunction.py', 'r') as file:
        chatfunction_contents = file.read()
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Read and process all the provided files:{}".format(chatfunction_contents)
    )
    helper.process_run(run, client, thread)

    messages = client.beta.threads.messages.list(
        order="asc",
        thread_id=thread.id
    )
    for message in messages:
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        print("{}: {}".format(message.role, message.content[0].text.value))
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
