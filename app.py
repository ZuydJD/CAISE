from flask import Flask, render_template, url_for, flash, redirect, request, get_flashed_messages, jsonify
import requests
import sqlite3
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    
    return render_template('chat.html')

def chat_page():
    conn = get_db_connection()
    chat_history = conn.execute('SELECT role, content FROM chat_history ORDER BY timestamp').fetchall()
    conn.close()
    return render_template('chat.html', chat_history=chat_history)


@app.route('/Chat', methods=['POST'])
def chat():
    user_message = request.form['message']

    # Connect to the database
    conn = get_db_connection()

    # Save the user message to the database
    conn.execute('INSERT INTO chat_history (role, content) VALUES (?, ?)', 
                 ('user', user_message))
    conn.commit()

    # Retrieve the updated chat history from the database
    history = conn.execute('SELECT role, content FROM chat_history ORDER BY timestamp').fetchall()

    # Prepare the data for the assistant API call
    formatted_history = [{"role": h['role'], "content": h['content']} for h in history]

    # API request data
    data = {
        "mode": "chat-instruct",
        "character": "C.A.I.S.E",
        "messages": formatted_history
    }

    # Send the request to the AI assistant API
    url = "http://127.0.0.1:5000/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data, verify=False)

    # Get the assistant's message from the response
    assistant_message = response.json()['choices'][0]['message']['content']

    # Save the assistant's message to the database
    conn.execute('INSERT INTO chat_history (role, content) VALUES (?, ?)', 
                 ('assistant', assistant_message))
    conn.commit()
    conn.close()

    # Return the assistant's response to the frontend
    return jsonify({"response": assistant_message})

if __name__ == '__main__':
    app.run(debug=True)
