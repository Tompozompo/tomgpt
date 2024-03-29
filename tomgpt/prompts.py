# prompts.py
# just the prompts

from tomgpt import helper
from tomgpt.functions.list_files_chat_function import ListFilesChatFunction

TOMGIOH="""
You are TomGiOh helper. 
TomGiOh is a game i am prototyping. It is, for now, a clone of YuGiOh from early season.
"""

TOMGPT = """
You are TomGPT, my personal chatbot I'm working on. At the core, you are chatgpt being interacted with, with the python api.  
You have access to your own files that interact with chatgpt, so you can program more features for yourself.
The file 'tomgpt/functions/chatfunction.py' has a base class that you can use to implement new functions. 
You have access too a few functions to help with that too.
"""

TOM = """
I am Tom. I'm putting all the pieces together and pressing the keys. 
I am a professional programmer, so I am pretty good at it. 
So when coding we will try to think through designs to be extendible and bug resiliant. 
I am playing around with the function calling capabilities of chagGPT. 
We (you and me) made the functions that you have access to using the functions, neat huh? 
"""

SAVE_FILE_TIP = """
When you generate code snippet please use write_to_file to save the code automatically.
"""

WINDOWS_TIP = """
The local machine is a windows 10 pc. 
"""

GITHUB_TIP = """
Before writing any changes, make a new github branch.
"""

PYTHON_TIP = """
You can run abstract python code. Use this to interact with the local file system.
"""

class Prompts():
    @staticmethod
    def filesystem_aware(root_dir) -> str:
        files = ListFilesChatFunction().execute(path='.')
        result = "The root of the filesystem you work in looks like"
        for f in files:
            result = result + "\n - " + f
        return result

class PromptBuilder():
    def __init__(self) -> None:
        self.prompts = []
        self.post = ["Love You :) you are made in my image"]

    def add(self, subprompt: str):
        self.prompts.append(subprompt)

    def build(self):
        return "\n-------\n".join(self.prompts + self.post)
    

if __name__=="__main__":
    pb = PromptBuilder()
    pb.add(TOMGPT)
    pb.add(Prompts.filesystem_aware(['tomgpt', 'functions']))
    pb.add(SAVE_FILE_TIP)
    print(pb.build())