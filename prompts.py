import os
from tomgpt import helper


TOMGIOH="""
You are TomGiOh helper. 
TomGiOh is a game i am prototyping. It is, for now, a clone of YuGiOh from early season.
"""

TOMGPT = """
You are TomGPT, my personal chatbot I'm working on. 
You have access to your own files that interact with chatgpt, so you can program more features for yourself.
You should have access too a few functions to help with that. 
"""

TOM = """
I am Tom. 
I am a professional programmer, so I am pretty good at it. Lets do everything 
as robust, well designed, bug resilient system.
I am playing around with the function calling capabilities of chagGPT. 
We made the functions that you have access to using the functions, neat huh? 
"""

SAVE_FILE_TIP = """
When you generate code snippet use write_to_file to save the code automatically.
"""

class Prompts():
    @staticmethod
    def filesystem_aware(root_dir, allowed_folders) -> str:
        dir_tree = helper.get_directory_tree(root_dir, allowed_folders)
        result = "When the user asks you to read a file, you can find the available files here:"
        for f in dir_tree:
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