from flask import Flask
from threading import Thread
import os

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
