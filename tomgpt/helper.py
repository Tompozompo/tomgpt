from flask import Flask
from threading import Thread
import os

def start_flask_app():
    global app
    app = Flask(__name__)
    Thread(target=lambda: app.run(use_reloader=False)).start()

def get_root_directory():
    return os.path.dirname(os.path.abspath(__file__))








if __name__ == "__main__":
    string_to_pass = "Hello, Flask!"
    start_flask_app(string_to_pass)
