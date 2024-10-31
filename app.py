from flask import Flask, render_template, url_for, flash, redirect, request, get_flashed_messages, jsonify
import requests
import sqlite3
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import inspect

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize Flask application
app = Flask(__name__)

# Configure the SQLAlchemy database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "your secret key"
db = SQLAlchemy(app)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# User model for the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# db.init_app(app)
with app.app_context():
    db.create_all()

# ChatHistory model for storing chat conversations
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(username=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    # return redirect(url_for("home"))
    return render_template("chat.html")

@app.route('/home')
def home():
    return render_template("logged_in_chat.html")

@app.route('/Chat', methods=['POST'])
# @login_required

def chat():
    user_message = request.form['message']

    # Save user message to the database using SQLAlchemy
    new_user_message = ChatHistory(role='user', content=user_message)
    db.session.add(new_user_message)
    db.session.commit()

    # Retrieve chat history from the database
    history = ChatHistory.query.order_by(ChatHistory.timestamp).all()


    # Format chat history for API call
    formatted_history = [{"role": h.role, "content": h.content} for h in history]


    # API request data
    data = {
        "mode": "chat-instruct",
        "character": "C.A.I.S.E",
        "messages": formatted_history
    }

    # Send request to AI assistant API
    url = "http://127.0.0.1:5000/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data, verify=False)

    # Get the assistant's message from the response
    assistant_message = response.json()['choices'][0]['message']['content']

    # Save the assistant's message to the database
    new_assistant_message = ChatHistory(role='assistant', content=assistant_message)
    db.session.add(new_assistant_message)
    db.session.commit()
    
    # Return assistant's response to the frontend
    return jsonify({"response": assistant_message})



if __name__ == '__main__':
    with app.app_context():
            db.create_all()    
    app.run(debug=True)

