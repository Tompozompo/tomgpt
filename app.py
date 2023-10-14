# app.py
# Text window for interacting for ChatGPT. 
# Shows current chat history and a way to send a new message.

import openai
from flask import Flask, request, render_template, url_for

app = Flask(__name__)
openai.api_key = ""

def get_system_prompt():
    return "You are a fun lil ai manager buddy I'm playing with. You are running in a flask app."

conversation_history = [
    {"role": "system", "content": get_system_prompt()}
]

@app.route('/')
def chat():
    return render_template('chat.html', conversation=conversation_history)

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['user_input']
    conversation_history.append({"role": "user", "content": user_input})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        temperature=0.6,
        n=1
    )
    
    bot_reply = response['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": bot_reply})
    
    return render_template('chat.html', conversation=conversation_history)

if __name__ == '__main__':
    app.run()
